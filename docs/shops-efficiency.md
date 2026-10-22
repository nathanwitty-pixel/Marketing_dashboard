# Shops Efficiency Tracking

- **Generators:** `shops_dispatch.py` (Odoo → dispatch/receiving/sold JSON) →
  `shops_efficiency.py`
- **HTML:** `shops_efficiency.html`

## What the page shows

**Each table's filters follow the reader** (19 Oct 2026): the Shop, Category and Bag type filters of every Stocks Remaining table pin at the top while that table is on screen, also after the page redraws them (`assets/sticky_controls.js`, docs/sticky-controls.md).


**Sidebar** ([page sidebar](README.md#page-sidebar)) — every block title / card / table rendered at runtime (period prefix dropped — the Weekly/Monthly toggle says it; clashing names keep "· weekly"/"· monthly"); the toggle rebuilds the list.

How well each Kenya shop converts the bags it holds and the bags dispatched to it.
Per-shop metrics (D = dispatched, C = sold):

| Metric | Meaning |
|--------|---------|
| No. of bags at the shop | stock on hand |
| Total bags sold | C |
| No. of bags dispatched | D |
| Bags sold from dispatch help | C where D>0 |
| Stocks remaining after dispatch | max(D−C, 0) where D>0 |
| Cleared bags without dispatch | C where D=0 (the shop's own buffer stock) |

There is also a **region-level** roll-up (Kenya only, so region totals equal the
Kenya-shop totals).

## Combos & Power Deals — by shop

A per-shop panel (`#combo-shop`, at the bottom of the page) with a **shop selector**: pick a shop
(e.g. Hilton) to see, for that shop:

- **Best combo here** — its highest-`rung` running combo (rung vs "could-have"/`pot`).
- **Running combos here** — every combo rung at the shop with rung vs could-have, the **red
  under-ringing** flag (rings below half its region's best shop → "ring the combo button instead
  of separate bags"), and its **Deal-of-the-Week overlap** using that shop's own solo-sale counts
  (the same red-chip explanation from the Self-Made Combos page, now shop-scoped).
- **Deal of the Week here — Tier 2 (latest)** — **only the deals assigned to this shop** (its own
  DoW lineup, ~6 deals), bag · tier · units sold there, highest first — not every deal that
  happened to sell at the shop. `combos_by_shop()` filters `dealOfWeek` by each deal's `locations`
  (the shops it runs at, incl. the `DOW_MIRROR` expansion Starmall→Hazina/Hilton/KTDA); the page
  then shows the **Tier 2** subset (latest 2-week window). Power Deals run the whole month (tier
  "All", no tier) so they aren't in this tiered table, but still feed the push-via flags below.
- **Bags to push here — stock on hand** — the bags physically sitting at the shop (live Odoo
  on-hand, highest stock first), **filterable by Colour / Category / Product / Bag Type / Push via**
  (the reusable `DenriTableFilter` bar). The **Push via** filter picks bags by their tag —
  **None** (no active deal), **power deal**, or **deal of the week** — so you can isolate, say, only
  the on-hand bags that already have a deal to push them, or only the ones with none. Each row is
  flagged with that tag; the computed value is attached to the row as `pushVia` ('None' for blanks)
  so it's selectable. This is the "which bags to push" list.
  Source: `compute_period()` emits `pushDetail` per period (`{shop, product, stock, colour,
  category, bagType}`) from the live Odoo stock (`odoo_stock_levels()`, keyed by product name).
  Colour/bagType are split out of the product name using the bag types the sheet meta knows, and
  category is looked up per bag type from that meta (`bt_cat`); combo/promo and accessory lines
  (`+`, FREE/BUY/GET, WIPE) are dropped. It reports **on-hand only** (not a per-bag sold/remaining
  split): the Odoo dispatch feed is shop-level, and Odoo stock keys `(PRODUCT, "")` don't share the
  sheet sales' `(BAG TYPE, COLOUR)` keys, so a reliable per-bag sold join isn't available — on-hand
  stock is the dependable per-bag push signal.

**Data flow — live from Odoo.** `shops_efficiency.py`'s `_load_combos_by_shop()` builds this
**live from Odoo** by importing `self_made_combos` and calling its `fetch()`, then reading
`combosByShop` (from `combos_by_shop()`: running-card `usage.shops[]` for rung/red/DoW soloTok +
`deals.soldByLoc` for power-deal per-shop sales). So the panel reads Odoo like the rest of the
page. To avoid rebuilding the combos payload twice when `main.py` runs the combos generator
seconds earlier, a `combos_by_shop.json` **written in the last 15 minutes is reused**; anything
older (or a standalone Shops-Efficiency refresh) recomputes live and rewrites that file. If the DB
is unreachable it falls back to the last file. Injected as `SE.combos`; keys re-cased UPPER to
match `KENYA_SHOPS`. The panel is client-side and hides itself if there's no data.

> Note: the client reads the page's `const SE` directly (a top-level `const` is **not** on
> `window`), so the panel script guards with `typeof SE !== 'undefined'`, not `window.SE`.

## Stock record accuracy (22 Oct 2026, user's call)

Which shops keep their stock sheet honest: every time a shop's stock cell on the STOCK_LEVELS sheet goes
**negative** (more sold than the sheet says it had), a fix is logged. Fewer fixes for the bags a shop sells =
better record keeping.

- **Source:** Google spreadsheet *STOCKS LEVELS 2026* (`1xWmk1CJldzs8H7G8QcNk7Q7xDbQMQpN454jy-bm-teY`), tab
  **NEGATIVE FIX LOG**, read only by `lib/negative_fixes.py` (allowed in `tests/test_sheet_reads.py`). Columns:
  Time (date, month/day/year), Mode, Shop, Sheet, Row, Item (col B), Negative, Cell adjusted, Old value, New
  value, Status. The log starts **4 Oct 2026**.
- **Which rows count:** Mode **APPLIED** only (PREVIEW rows are dry runs that repeat the applied ones), and not
  `SKIPPED - total row`. Shop names are stripped of spaces.
- **Shop mapping to the tills (bags sold):** KTDA → `ktda shop`; SINZA → `sinza` + `dar-es-alam`; UGANDA →
  `uganda`; every other shop → its lower-case name. Bags sold = Odoo POS with the `sql/bags_sold_total.sql`
  filters, grouped by till.
- **Periods** (the dashboard schedule): **Last week** (default, the full Sun–Sat week before this one), This
  week, This month, Last month, each against the period before of the same length, plus **Since the log
  started** (4 Oct 2026 → today; its "before" is empty).
- **Measures per shop:** fixes; negative units; **fixes per 1,000 bags sold** (the ranking measure, lower is
  better, worked out **without big one-offs**); days with at least one fix; **repeat items** (shop-items fixed
  in the period that had already been fixed earlier since the log started); big one-offs.
- **Big one-off:** a single fix of **10+ units**. Listed with ⚠ (shop, item, date, units), left out of the
  ranking measure, and the fixes including them are shown too.
- **Ranking:** best first by fixes per 1,000 bags (without big one-offs); a shop with no fixes is best; a shop
  that sold no bags in the period is listed last with no rate.
- **Where it shows:** the **Stock record accuracy** panel on this page, with its own period select: a ranked
  bar chart (green = best third, red = worst third, the number on each bar, a green / red change badge against
  the period before), a table (Shop, Fixes, Negative units, Bags sold, Fixes per 1,000 bags, Days with fixes,
  Repeat items, change), the Repeat items list and the ⚠ Big one-offs list. Also from the command line:
  `python scripts/negative_fixes_report.py --period lastweek|thisweek|thismonth|lastmonth|sincelog`.

## Data sources

Spreadsheet `1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0`, all in
`COLOUR / [CATEGORY] / PRODUCT NAME / BAG TYPE` shape with one column per location:

- **WEEKLY_DISPATCH / MONTHLY_DISPATCH** — bags dispatched to shops.
- **WEEKLY_SALES / MONTHLY_SALES** — bags sold / converted.
- **STOCK_LEVELS** — bags currently at each shop.

Live dispatch/receiving/sold comes from Odoo via `shops_dispatch.py`, which
`shops_efficiency.py` reads from its JSON.

## Shops

Kenya shops only (`KENYA_SHOPS` in `shops_efficiency.py`): STARMALL, MOMBASA, NAKURU,
ELDORET, KISUMU, MERU, THIKA, HAZINA, KITENGELA, NANYUKI, KAKAMEGA, HILTON, KISII, KTDA,
BUSIA, RONGAI. WEBSITE / SINZA / UGANDA are excluded on purpose. Each name is matched to
its sheet column by header.


## Shop birthdays

Opening anniversaries from [shop-birthdays.md](shop-birthdays.md) (shown from 30 days before to 1 day after): a 🎂 badge beside the shop name in the shop performance table, the per-shop metric columns and the receiving table, plus a "Shop birthdays coming up" strip under the title (`SE.birthdays`).

## Regenerate

```
python generators/shops_dispatch.py          # refresh dispatch/receiving/sold from Odoo
python generators/shops_efficiency.py
```
</content>
</invoke>
