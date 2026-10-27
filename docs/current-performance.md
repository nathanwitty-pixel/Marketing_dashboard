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

## Weekly Performance — corporate in each week (26 Oct 2026, user's call)

Each Sun–Sat week's **Sales bags** = its till bags (`BAGS_SOLD_TOTAL`) **+ the corporate bags paid that week**
(`CORPORATE_BAGS` over the week — the Corporate app, money received on the payment date, the Sales card's rule).
Any rounding left between the weeks' corporate and the month's (part-paid invoices round down per window) goes on
the latest week, so the rows **add up to the Sales card** (Oct 2026: 2,235 + 4,334 + 3,700 + 3,449 + 188 = 13,906).
The cell names the corporate part ("3,449 bags, 537 corporate"); `weeklyHistory` rows carry `posBags` and
`corporateBags`. Sales % achieved, Declined By and the chart follow the same totals. The dashed previous-month line
is that month's saved month-end report (September 2026 had 63–77 corporate bags, so it is left as recorded).

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

**September vs October, week on week (18 Oct 2026, user's call):**
- Each month's week-on-week change shows as pills: October's above its points ("Oct ▲108%"), the
  previous month's under its own ("Sep ▲20%"). The pills come from the shared weekChange code
  ([chart-switcher](chart-switcher.md)).
- **Short weeks are labelled** under the x axis with their day counts, e.g. "Oct 3 days, Sep 5 days" for Wk 1, and
  "Oct 1 day so far, Sep 7 days" for the week still running (words, no dot separators, 26 Oct 2026). Weeks are Sun–Sat inside the month, so the first and last
  weeks are often short. Full 7-day weeks show no day line.
- **The running week** (`partialWks`, from today's date) is passed as `weekChange.partial`. Its pills read grey
  "… so far", not a red crash.
- **No overshoot:** both lines use `cubicInterpolationMode: 'monotone'`, so the curve never rises above a
  week's real figure.
- **The tooltip** adds last month's same week and its move from the week before.

The control's markup, CSS and JS all live **outside** the `PERF_DATA_*` and `PROJ_DATA_*` markers,
so `current_performance.py`'s regex rewrite never touches them.

## Why Did We Move? — waterfall (26 Oct 2026, user's call)

A full-width card under Weekly Performance (`#wm-grid`, canvas `#chart-why-moved`, chart switcher off).
It explains a rise or drop as a waterfall: **last period → Selling days → one bar per region → this period**.
Toggle **Week on week / Month on month** (`#wm-period`, remembered in `localStorage` key `cp-wm-period`).

- **Data:** `PROJ.whyMoved = {wow, mom}`, built by `why_moved()` in `generators/forward_projections.py`.
  Per-till bags come from `sql/bags_sold_by_shop.sql` (`BAGS_SOLD_TOTAL` split by till, so it adds up exactly),
  grouped by [shop-regions.md](shop-regions.md); corporate paid bags (`CORPORATE_BAGS`) are their own bar.
  Till names: `DAR-ES-ALAM` → Sinza, `KTDA SHOP` → KTDA, `WEBSITE SALES` / no session → Website, unknown → Other.
- **Periods:** complete days only (up to yesterday). `wow` = the two latest complete dashboard weeks
  (Sun–Sat cut at month ends, so Wk 1 Oct = 1–3 Oct). `mom` = 1st → yesterday vs the same days last month;
  on the 1st, the month just finished vs the one before.
- **Maths:** Selling days = then bags/day × (days now − days then). Region bar = (its bags/day now − then) × days now.
  Rounding leftovers go on the biggest mover, so the bars always land on the end total. The days bar hides when
  the day counts match.
- **The reason** (amber box) = the biggest bar in the direction of the total move. The line under the chart names
  its top shops; the tooltip lists every shop's change in that region.
- The y axis starts below the lowest level (stated in the sub-line), so small moves stay visible.
- **Bulk filter** (`#wm-mode`, `localStorage` key `cp-wm-mode`): **With bulk orders / Without bulk orders**
  (26 Oct 2026, user's call; data keys `with` / `without`). **Corporate is in both** — it is treated as a shop
  and is never a bulk order. With = every sale (= the Sales card); Without = every sale minus the bulk till orders.
  Bulk order = a **till** order with any counted line of 10+ units (the dashboard's rule, see
  [product-performance.md](product-performance.md#bulk-orders)). **The Corporate app is not a bulk order**
  (user, 26 Oct 2026): it is its own sales channel.
  `bags_sold_by_shop.sql` returns `bulk_bags` per till, and `whyMoved.{wow,mom}` holds `{with, without}`.
  With shows "without bulk orders: ±N" beside the title and "⚠ bulk orders X → Y" on regions where bulk moved.
  Oct 2026, week on week: with bulk −251 (3,701 → 3,450), Nairobi CBD −700; without bulk +274 (3,176 → 3,450),
  Corporate +534, Nairobi CBD only −200 — the rest was a 500-bag Hazina bulk order in Wk 3.

## Sales card — the one bags figure (reject + gift-bag split)

**Sales is the only bags-sold KPI** (27 Sep 2026: the separate *Net Bags Sold · Catalogue* card —
master-list products only, ~313 bags lower in Sep — was merged away, and the *Weekly vs Last
Month* pace card was removed). Sales = `sql/bags_sold_total.sql` (every bag the tills sold incl.
bags inside combos, gift bags, rejects and **samples** (sold display units, counted since 26 Oct 2026, user's
call); refunds netted; **straps**, delivery, customisation, the combo wrapper, the KES discount line and
POS-category lines are **not** counted)
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
- **Samples** (`name ILIKE '%sample%'`) — sold display units, **in Sales** since 26 Oct 2026 (user's call); shown here
  so you can see how many of the bags were samples.
- **Customisation** = customised bags (`'%customi%'` but not `'%customization%'`, e.g. *KCB
  Briefcase Customised Brown* — a bag, **in** Sales) **+** customisation charges
  (`'%customization%'` — a service line, **not** in Sales). The tooltip gives the split.
Sep 2026: 4 samples, 1 customised bag, 0 customisation charges.

**Corporate-lead till orders (16 Oct 2026, user's call — revised the same day):** when a client the **Corporate team** brought in (a Corporate-app lead) pays at a shop till, the sale is **credited to that shop** like any till sale, but it's still marked as a Corporate lead (October: ESK Company, HAZINA/29958 + 29613, KES 1,707,197 → Hazina, "Corporate app lead 17 Sep · Scola Mithiri"). One that hasn't paid yet goes to the shop that hunted it (quote note → bought there before → client's town), still noted as a Corporate lead; with no shop link it isn't shown at all until something is paid at a till. Here: their bags count in **POS** in the Sales-card split; **corporate** shows only the Corporate-app figures. The "Shop corporate" tab credits them to the shop and notes the Corporate lead under it. **Shop corporate tab (16 Oct 2026, user's call):** an unpaid quote with no shop link (no till payment, no shop on the quote note, never bought at a shop, no shop town) and not in the Corporate app is left off the tab until it is part-paid.

**Corporate by client** (its own section after Forward Projections since 18 Oct 2026 — it used to sit in the Sales popover. Each tab opens with a chart: Corporate app = bags per client stacked Sold (paid) · Invoiced, not paid yet · Quoted, to invoice; Shop corporate = KES paid vs owed per hunting shop, a bar click filters the table like the shop boxes; `sql/corporate_clients.sql` → `PERF.corporateClients`. **% on the bars** (18 Oct 2026): each bar's end label adds its **share of the tab's bags** (client bags ÷ all bars' bags; Shop corporate = the shop's bags ÷ all hunting shops' bags) and its **% of the corporate target** (bags ÷ `PERF.corporateTarget.bags`, the Odoo corporate target — the same target on both tabs); the tooltip shows the share too. Shares on a tab add up to 100 % (± rounding)):
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
**Quoted total = still to invoice:** the header total under Quoted counts only bags on this month's quotes that
haven't become an invoice ("111 · to invoice" on 8 Oct: safarilink 100 + George Eshuchi 10 + H.k 1). Rows still
show every quoted bag. A not-invoiced tag reads "sent · 100 to invoice". When the client already has invoiced bags
in the table, the hover adds "If accepted: 100 more bags to invoice, on top of the 100 already invoiced". Safarilink
reorders the same 100 Safarilink Travel Brown: Jan paid, Jul draft, Aug paid 5 Oct, and a **new** quote on 5 Oct
with 100% payment on order. So its open quote is a likely repeat order, not the August one again.
**Corporate target (Oct 2026):** a strip at the top of "Corporate by client" sets the month against the Odoo
corporate target (`sales_pos_target`, `target_scope = 'corporate'`, `period = 'month'`, the row covering this
month: `target_qty` bags, `target_amount` KES → `PERF.corporateTarget {bags, kes}`). It shows:
- **Bags:** Sold total ÷ target bags.
- **Money:** KES received this month ÷ target KES. Received = payments dated in the month (a deposit before
  its invoice counts on the invoice date), summed from `received` in `sql/corporate_clients.sql`.
- **Month gone:** days elapsed ÷ days in the month. Each % is green when at or above it, amber below.
- **Pipeline:** the Quoted "to invoice" bags.
Example, 8 Oct 2026: target 1,163 bags · KES 2,325,368; sold 312 (27%); received KES 737,646 (32%); day 8 of 31
(26%); 111 to invoice. No target row → no strip.
**Whole bags only (Oct 2026):** a part-paid invoice counts the **whole** bags its payment covers, rounded
down per invoice (`FLOOR`, in both `corporate_bags.sql` and `corporate_clients.sql`). So the Sales card's
"N corporate", the table's Sold total and Forward Projections always agree. Example: CIArb paid 75% of
250 bags = 187.5, which counts as 187; the half bag counts when the balance arrives. Before, the card rounded the
total (312.5 → 312) while the table rounded each client (187.5 → 188, total 313).
**Layout (Oct 2026):** the whole client area (table, the "Why …" note and the legend) is one scrolling box
(`.corp-scroll`, max 300 px, about the donut column's height). The column header is pinned at the top and
shows the **totals** beside each name: Quoted · Invoiced · Paid (all paid ÷ all agreed, after WHT) · Sold.
They stay in view while you scroll.

## Forward Projections — revenue (21 Oct 2026, user's call)

Each projection card shows the **revenue** it lands on, under the % of target, so the bags % and
the money read together:

- **Standard** → POS **bag revenue** month-to-date (`sql/bag_revenue.sql`) × velocity factor. Same
  pace and month as the bags %. Bag revenue = the same bag lines as the Sales card, **plus the
  combo '+' wrapper lines** (a combo's price sits on the wrapper; the bags inside are KES 0
  sub-lines, `parent_id`), minus 'KES discount' lines. Delivery / customisation / straps stay out; samples are in,
  like Sales (26 Oct 2026). **Not** `monthlyValue`: that drops the wrapper, so combo bags counted as KES 0 and
  revenue read ~6% low (fixed 21 Oct 2026).
- **Forecasted** → (POS revenue + corporate KES received) × velocity factor. Corporate KES =
  `kes` in `sql/corporate_bags.sql`: money paid on Corporate-app invoices in the month, capped at
  each invoice's agreed amount (after WHT). That's the same payments that give the corporate bags.
- **Revenue target** = the month's Odoo `sales_pos_target` amount (scope pos + corporate), or
  `REVENUE_TARGETS` in `lib/product_targets.py` when Odoo has none. When there's a target, the
  card also shows the projected revenue as a % of it. With no target, it shows only the KES.
- Postgres down / no live month figure → the revenue line is left off (no stale number).

PROJ fields: `standardRevenue`, `forecastedRevenue`, `revenueTarget`, `standardRevenuePct`,
`forecastedRevenuePct`, `corporateKes`.

**Price per bag card** (full width, under the two projection cards) explains why the revenue %
and the bags % differ, so the reader can judge it:

- **Target price per bag** = revenue target ÷ bag target (what the targets assume a bag brings in).
- **Actual price per bag** = POS bag revenue ÷ bags sold, month to date.
- **Gap** = actual ÷ target − 1. Above target → revenue % runs ahead of bags %; below → it trails.
  revenue % ≈ bags % × (1 + gap).
- **22 Oct 2026 (user's call):** the single bags / combos / gift bags / discounts table is **no longer shown**. The
  On offer vs not on offer table carries the data. The verdict's Biggest lift / drag and the month-end
  "Altogether" figure now come from that table (`priceMix.offerMix`). `priceMix.rows` is still computed
  (the headline Actual price per bag uses it). Rows opened in the On offer table list their bags **grouped by
  category** (subtotal row per category, biggest revenue first, then its bags). Corporate app and the till
  discount stay flat lists.
  - **Collapse / expand:** click a row to open its categories, click a category to open its bags.
    **Expand all** / **Collapse all** buttons sit next to the table heading.
  - **Hover** on Effect at month end: projected KES minus what the targets expect (projected bags x target price,
    or gift bags' own target), worked out in words. Hover on Effect on revenue rate: that KES / revenue target x 100,
    e.g. +4.11 = +KES 2,304,620 / KES 56,030,805 x 100. All the rows' points add up to the All bags total.
- (Old, not shown) A table split the month by how bags were sold: **single bags, combos, gift bags, discounts**,
  with bags, revenue, KES per bag and each row's gap to the target price. That shows what's
  lifting or pulling down the average.
- Bags and revenue show **so far → month end** (× velocity factor, same pace as the cards).
- **Gift bags have their own target (21 Oct 2026, user's call).** The Odoo bag target has no gift
  bags, so the KES ~2,000 price and the headline Actual price per bag cover **single bags + combos
  (after discounts)** only. Gift bags are judged on their own target: the average month of the three
  complete months before (`product_targets.base_period`, Oct 2026 → Jul–Sep: 251 a month) at their
  own average price then (KES 194). The row shows "294 of 251 target" and "−2.2% vs KES 194".
- **Effect at month end (KES)** = the row's projected revenue − what its target expects: projected
  bags × KES ~2,000 for single bags / combos, gift target × gift price for gift bags, 0 for
  discounts. **Effect on revenue rate (pts)** = that ÷ revenue target × 100. The total = how far
  month-end revenue sits above / below what the targets expect for the bags on course to be sold.
- **Bags still to sell for revenue target** = (revenue target − revenue so far) ÷ actual price per bag.
- The card's top strip is **green** when bags sell at or above the target price, **red** below.
- Rows are computed in `forward_projections.py` (`priceMix.rows`); the page only renders them.
- Hidden when there's no revenue target or no live revenue. PROJ field: `priceMix`.
- **On offer vs not on offer** (22 Oct 2026, under the table): the same month's bags sorted the way the
  Bags On vs Off Offer page sorts them (`bags_on_offer.py` writes `data/offer_mix.json`, monthly period).
  Rows: Not on offer, **On offer** (= Power deals + Combos + Deal of wk + Mid-month offers, each shown under
  it), then Corporate, Samples, Gift bags, Not yet sorted. Same columns and prices as the table above:
  KES ~2,000 a bag, gift bags on their own target, samples expect nothing, Not yet sorted (returns and
  unmatched names) is not judged (effect 0). **Click a row to see the bags inside it**: each bag's bags,
  share of the row, revenue, KES per bag and gap to the target price. A verdict line compares the offer
  and full-price KES per bag. Totals can differ a little from the table above (different sorting, and the
  offer page's build time is shown). `main.py` runs Forward Projections after Bags On vs Off Offer so the
  split is fresh. PROJ field: `priceMix.offerMix`.
  - **Mid-month offers** is split into its parts, each its own row with its own bags: **New products**,
    **Runway bags**, **Timed offers** (Kenya), **Listed singles** (Tanzania / Uganda).
  - **Corporate app** row: bags on Corporate app invoices (`sql/corporate_bag_lines.sql`, same paid-share rule
    as `corporate_bags.sql`; the received KES is shared across each invoice's lines by subtotal, so it adds
    up to the Forecasted card's corporate KES). Click for each bag and its client(s); fees are one row with 0
    bags. Not POS, so All bags here is above the table above. The offer page's own Corporate row is the same
    Corporate app (26 Oct 2026), so it isn't shown here: corporate is counted once, in this row.
  - **KES 300 till discount** (was "Not yet sorted", 22 Oct 2026, user's call): only the till's KES 300 discount
    line. No bags, nothing expected, so its effect = the money off (same as Discounts in the table above).
    The few other unsorted lines (PPM, Passport Holder…: names with no bag type) are added to **Not on offer**
    and listed there as "not in the bag list yet".
  - Each row shows **where it sells** (Kenya only / Kenya, Tanzania, Uganda), from the offer page's country
    split. Mid-month parts carry it in the label, e.g. "Timed offers (Kenya)", "Listed singles (Tanzania, Uganda)".
  - **Corporate (Odoo invoices)** = the offer page's Corporate row: paid customer invoices in Odoo Accounting
    (Sales orders, S-numbers), not the Corporate app. Hidden when 0.

## Data sources

- **MONTHLY_TARGET** sheet: col C target, D sales, E deficit (summed).
- Real weekly/monthly **bags** are refreshed from Postgres first (`weekly_sales.py`,
  `monthly_sales.py`) so the sales figures are live, not stale sheet values.
- **The page's Refresh also rebuilds the offer split** (`self_made_combos.py` → `bags_on_offer.py`, before
  `forward_projections.py`), so the On offer table's All bags matches the Sales card. *Fixed 25 Oct 2026:* the
  refresh skipped it, so the table read a 22 Oct `offer_mix.json` (All bags 12,492 vs Sales 13,918).
- **Sales counts each refunded combo's bags once** (docs/README.md › Combo refunds, 25 Oct 2026): 6 Oct combos
  refunded without their bag lines had never been taken off, so POS Sales read 13,053 instead of 13,041. With that
  and the offer page's fixes, the On offer table's All bags = Sales + the 3 samples it lists. With samples in Sales
  (26 Oct 2026) the two are equal.
- **Last week's bags** (`PERF.previousSalesBags`, the week-over-week base) are read straight from Postgres for
  the previous complete **Sun–Sat** week (`BAGS_SOLD_TOTAL`, the same definition as this week's figure).
  `previous_snapshot.json` is only the fallback when the DB is down. *Fixed 14 Oct 2026:* the snapshot rolled
  over on the ISO (Monday) week, so a Sunday build saved Sunday's 197 bags as "last week" (real 4–10 Oct: 4,221),
  and Week-over-week read +744%.
- **Previous sales % achieved (N bags):** the % is (Sales − this week's bags) ÷ target, so N is that same
  numerator, the bags sold before this week (`PERF.previousAchievedBags`), e.g. 8,238 − 1,664 = 6,574 on 14 Oct.

## Manual inputs

- `bare_minimum` in `current_performance.py` — the week's minimum bags target (0 = unset).
- `forward_projections.py` holds the projection assumptions (re-run to pick up edits).

## Month scope

Figures belong to the month `report_month` reports — the **live/current** month, matching
the other dashboards. `projMonth` (from the PROJ block) names it.

## Regenerate

```
python generators/weekly_sales.py
python generators/monthly_sales.py
python generators/current_performance.py
python generators/forward_projections.py
```
(Or just `python scripts/build_all.py` for the whole set in the right order.)
</content>
</invoke>
