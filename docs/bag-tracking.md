# Bag Tracking

Menu: **Products › Bag Tracking** (`html/bag_tracking.html`, built by `generators/bag_tracking.py`).
Asked for 2 Nov 2026 (user's call): the bags chosen to sell after the power deals, tracked from a fixed start.

## The bags

Listed in `data/bag_tracking.json` (`bags`), by the dashboard's bag name (the same names as Offer Picking):
CODE 3, AMAYA, ZURI, MINI ZURI, DOUBLE PRESS, GYM BAG, LIAM, PIONEER, BIG MAN BAG, NEO MAN, MAN BAG, KAI, TRAVEL,
FABELA, TRECENTO, AURORA, AVANA HB, BELT BAG, MOON BAG, MONAH BP. Add or remove bags there; a bag added later gets
its start stock worked out the same way (back from the stock now to the start time).

## Stock

- **Where:** Kenya shop stock (the 16 Kenya shop codes, `lib/stock.KENYA_SHOP_CODES`), all colours of the bag added up.
  Warehouse, CBD store, Sinza and Uganda are not counted — the same stock Offer Picking uses.
- **Stock was** = the stock at the **start: Monday 2 Nov 2026, 8:00 am** (`start` in the config). The page was built
  at 14:32 that day, so it is worked back from Odoo: stock now − bags received since 8 am − bags returned by
  customers + bags sold + bags sent out. Odoo moves stock the moment a till sale is rung (checked: the first customer
  move today 08:20:42 = the first POS order 08:20:41), so this is exact. Worked out once and **frozen** in
  `data/bag_tracking_baseline.json` (per bag and colour); later runs don't recompute it.
- **Stock now** = live Kenya shop stock at the time the page was built.
- **Since 8 am** (all from done Odoo stock moves since the start):
  - **Sold** = moves from a Kenya shop to a customer (till sales, bags inside combos included), less customer returns.
  - **Received** = moves into a Kenya shop from anywhere that isn't a Kenya shop (restocks from the warehouse / CBD).
  - **Sent out** = moves from a Kenya shop to anywhere else (back to the warehouse, other markets, write-offs).
  - Shop-to-shop moves inside Kenya cancel out.
  - **Change** = Stock now − Stock was.
- **Sell-through** = Sold ÷ (Stock was + Received).

## Prices

- **Price was** = full price, **Price now** = offer price, from the offers sheet (Offer Picking's prices, `valueWas`
  / `valueNow`). A `now` in the config overrides it: PIONEER 2,200, KAI 2,400 (user's prices, 2 Nov 2026).
- **Discount** = (was − now) ÷ was. **Sold value** = Sold × Price now.

## Page

- Cards: bags tracked, stock was, stock now, sold since 8 am (and its value), received.
- One table, a row per bag; click a row to see its colours (stock was / now / sold per colour).
- Like the "Bags not on offer we can still sell" card on Offer Picking:
  - **Filters:** search by bag, category, movement (sold since 8 am / no sales yet / restocked), "Clear";
    "Showing X of Y" when a filter is on.
  - **Sort:** click a heading (▼/▲); numbers biggest first, names A→Z; again flips, a third click is the default
    order (most sold first).
  - **Export CSV:** the bags that pass the filters, in the on-screen order (`bag_tracking_<date>.csv`).
  - **Collapse / Expand** on the table card, remembered per browser.
