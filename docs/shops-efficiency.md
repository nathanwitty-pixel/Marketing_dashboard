# Shops Efficiency Tracking

- **Generators:** `shops_dispatch.py` (Odoo → dispatch/receiving/sold JSON) →
  `shops_efficiency.py`
- **HTML:** `shops_efficiency.html`

## What the page shows

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

## Regenerate

```
python shops_dispatch.py          # refresh dispatch/receiving/sold from Odoo
python shops_efficiency.py
```
</content>
</invoke>
