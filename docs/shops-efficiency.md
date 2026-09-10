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
