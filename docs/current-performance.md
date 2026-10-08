# Current Performance

- **Generators:** `weekly_sales.py`, `monthly_sales.py` (Postgres → figures),
  `current_performance.py`, `forward_projections.py`
- **HTML:** `current_performance.html`
- **Data markers:** `<!-- PERF_DATA_START -->…<!-- PERF_DATA_END -->` (const `PERF`) and
  `<!-- PROJ_DATA_START -->…<!-- PROJ_DATA_END -->` (const `PROJ`, from
  `forward_projections.py`)
- **State files:** `previous_snapshot.json` (last period's values),
  `monthly_report_history.json` (prior-month weekly series for the comparison chart)

## What the page shows

**Sidebar** ([page sidebar](README.md#page-sidebar)) — Current Performance and Forward Projections, with Weekly Performance as a sub-item.

The month's headline performance — total target vs sales vs deficit, sales % achieved,
week-over-week movement, and a **current-vs-previous-month weekly comparison chart** (current
month solid, previous month dashed — `cpPrevWeekly` from `monthly_report_history.json`; the
month names are dynamic, from `PERF.cpCurLabel` / `PERF.cpPrevLabel`), plus forward projections.

## Weekly Performance chart — type filter

The **Weekly Performance — Week 1 to Latest** card carries a segmented control (`#cp-wp-type`,
classes `.cp-seg-wrap` / `.cp-seg`, ported from `.se-seg-wrap` / `.se-seg` in
`shops_efficiency.html`) that redraws the *same* data in four shapes. The numbers never change —
only the shape does.

| Button | Chart.js type | What it's for |
| --- | --- | --- |
| **Area** (default) | `line`, `fill:true` with the amber gradient | Today's look — the trend and its weight |
| **Line** | `line`, `fill:false` | Same trend, unfilled, when the two months overlap closely |
| **Bar** | `bar`, grouped | Head-to-head per week — easiest read of "Wk 2 this month vs Wk 2 last month" |
| **Radar** | `radar`, `r` scale | Shape of the month — which weeks carry it and which sag |

Rules the implementation must hold to:

- **Default is Area**, so a fresh load looks exactly as it always has.
- **Re-render is destroy + recreate**, per the `dataviz-charts` skill: the instance lives on
  `window._chartWeeklyPerf` and is destroyed before each `new Chart(...)`. Never mutate
  `chart.config.type` — the `wpPts` plugin and the radar `r` scale make that fragile.
- **The tooltip is shared across all four types** — `ttDefaults` plus the `afterBody` lines
  (weekly bags, cumulative % to date, points vs the previous week). A type switch must not
  lose them.
- **`wpPts` (the `%` label above each point) is suppressed on radar** — it positions labels at
  `pt.y - 8`, which collides with polar coordinates. It runs on area, line and bar only.
- **On Bar, the previous-month dataset drops its `borderDash`** (dashes are meaningless on bars)
  and becomes flat `rgba(148,163,184,0.55)`.
- **The canvas wrapper stays 210px tall.** The fill gradient is built once via
  `createLinearGradient(0, 0, 0, 210)` and is only correct at that height.
- **The choice persists** in `localStorage` under `cp_wp_chart_type`; reads and writes are
  `try`-wrapped, and an unknown or missing value falls back to `area`.

The control's markup, CSS and JS all live **outside** the `PERF_DATA_*` and `PROJ_DATA_*` markers,
so `current_performance.py`'s regex rewrite never touches them.

## Sales card — the one bags figure (reject + gift-bag split)

**Sales is the only bags-sold KPI** (27 Sep 2026: the separate *Net Bags Sold · Catalogue* card —
master-list products only, ~313 bags lower in Sep — was merged away, and the *Weekly vs Last
Month* pace card was removed). Sales = `sql/bags_sold_total.sql` (every bag the tills sold incl.
bags inside combos, gift bags and rejects; refunds netted; **straps**, delivery, customisation,
the combo wrapper, the KES discount line, samples and POS-category lines are **not** counted)
**plus** corporate invoice bags.

The Sales-card breakdown line shows the POS/corporate split **and two subsets of the POS total**:
"N POS + C corporate · R rejects (X%) · G gift bags (Y%)".
- `rejectBags` = the `[REJECT]`-tagged products (the Kitengela clearance), `sql/reject_bags_sold.sql`.
- `giftBags` = gift bags (`name ILIKE 'gift bag%'` — A3 / A4 / A5 and colours), `sql/gift_bags_sold.sql`.
Both use the same grand-total definition as `bags_sold_total.sql` plus their tag (true subsets),
are computed by `monthly_sales.py` into `monthly_sales_db.json`, and surfaced by
`current_performance.py` (`_db_count` → `PERF.rejectBags` / `rejectPct`, `PERF.giftBags` /
`giftPct`, % of the POS total). Each part is hidden when it is 0.

The same line also shows **samples** and **customisation** (`sql/sales_extras.sql`, all tills,
refunds netted, → `PERF.samples` / `customBags` / `customFees`):
- **Samples** (`name ILIKE '%sample%'`) — sold but **not** in Sales (display units).
- **Customisation** = customised bags (`'%customi%'` but not `'%customization%'`, e.g. *KCB
  Briefcase Customised Brown* — a bag, **in** Sales) **+** customisation charges
  (`'%customization%'` — a service line, **not** in Sales). The tooltip gives the split.
Sep 2026: 4 samples, 1 customised bag, 0 customisation charges.

**Corporate by client** (Sales popover, `sql/corporate_clients.sql` → `PERF.corporateClients`):
one row per client: quoted · invoiced · paid % · sold. In the Invoiced column, a **month badge** marks
when each counted invoice was raised (`invMonths`, Oct 2026), so you can see which month a client
converted. This month's badge is **green** (quoted and invoiced this month). Older months are **grey**
(invoiced then, paid this month). Those older ones are also listed in the "Why Aug / Sep invoices are
here" note (`earlier`, `earlierPaidOn`). A client with only a quote gets no badge. A NULL month from
the DB is blank, never "nan".
**Quoted, explained (Oct 2026):** Quoted = bags on quotations dated this month (declined / cancelled left out),
whether or not they became an invoice. Under each Quoted figure, a small tag says what became of the quote:
**invoiced 2 Oct** (green) when an invoice (not cancelled) was raised from it (`invoice.quote_id`), otherwise its
status, **draft / sent / accepted · not invoiced** (grey). Several quotes read "1 invoiced · 1 not invoiced".
Hovering the figure lists each quote: number, status, quoted on, bags, KES, then "→ invoiced as INV-… (status)
on …" or "→ not invoiced yet, valid until …" (`quotes` in `sql/corporate_clients.sql` → `quotes`). Example
(8 Oct 2026): Zakale 10 = QUO-00062, invoiced as INV-00134 (paid) on 2 Oct. safarilink 100 = QUO-00064, sent 5 Oct,
not invoiced yet; its 100 under Invoiced is a different, older August invoice. (A separate Pending column was
tried on 8 Oct and dropped in favour of this.)
**Whole bags only (Oct 2026):** a part-paid invoice counts the **whole** bags its payment covers, rounded
down per invoice (`FLOOR`, in both `corporate_bags.sql` and `corporate_clients.sql`). So the Sales card's
"N corporate", the table's Sold total and Forward Projections always agree. Example: CIArb paid 75% of
250 bags = 187.5, which counts as 187; the half bag counts when the balance arrives. Before, the card rounded the
total (312.5 → 312) while the table rounded each client (187.5 → 188, total 313).
**Layout (Oct 2026):** the whole client area (table, the "Why …" note and the legend) is one scrolling box
(`.corp-scroll`, max 300 px, about the donut column's height). The column header is pinned at the top and
shows the **totals** beside each name: Quoted · Invoiced · Paid (all paid ÷ all agreed, after WHT) · Sold.
They stay in view while you scroll.

## Data sources

- **MONTHLY_TARGET** sheet: col C target, D sales, E deficit (summed).
- Real weekly/monthly **bags** are refreshed from Postgres first (`weekly_sales.py`,
  `monthly_sales.py`) so the sales figures are live, not stale sheet values.
- `previous_snapshot.json` auto-loads the previous period so week-over-week deltas render
  without manual entry (keyed on ISO week).

## Manual inputs

- `bare_minimum` in `current_performance.py` — the week's minimum bags target (0 = unset).
- `forward_projections.py` holds the projection assumptions (re-run to pick up edits).

## Month scope

Figures belong to the month `report_month` reports — the **live/current** month, matching
the other dashboards. `projMonth` (from the PROJ block) names it.

## Regenerate

```
python weekly_sales.py
python monthly_sales.py
python current_performance.py
python forward_projections.py
```
(Or just `python build_all.py` for the whole set in the right order.)
</content>
</invoke>
