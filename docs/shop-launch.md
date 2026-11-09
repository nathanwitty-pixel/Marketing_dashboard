# Shop Launch

How a newly opened shop is doing from its first sale: sales, sell-through of its opening stock, a
day-by-day race against the last shop opened, and whether marketing posted the bags it stocks.
Built for **Nyeri** (Oct 2026); the next launch only needs a new config.

- **Generator:** `shop_launch.py`
- **HTML:** `shop_launch.html` (render layer; the generator replaces the data block)
- **Data marker:** `<!-- LAUNCH_DATA_START -->…<!-- LAUNCH_DATA_END -->` → `const SL = {…}`
- **Config:** `shop_launch_config.json`

## Config

```json
{"shop": "Nyeri", "till": "NYERI", "stockCode": "NYERI", "transitLocation": "FINWH/Goods in Transit/NYERI",
 "workplanSheet": "17CQvuuvNUhNBp4LUImdxJ6pGeTmAC-D1Ediei9v0Yjs", "workplanCsv": "nyeri_workplan.csv",
 "benchmark": {"shop": "Rongai", "till": "RONGAI"}, "days": 28}
```

- `till`: the Odoo POS till (`pos_config.name`). `stockCode`: its stock location's top code
  (`NYERI/Stock` → `NYERI`). `transitLocation`: where the warehouse parks stock on its way to the shop
  (default `FINWH/Goods in Transit/{stockCode}`). `days`: how many launch days the race chart and benchmark cover.
- **Opening stock = the workplan sheet** ("NYERI WORKPLAN": bag type, colour, quantity, with a TOTAL row per
  bag). It's read live with the dashboard's Google service account. If the sheet can't be read (not shared
  with `marketing-and-predictive-sales@steadfast-sign-498718-d9.iam.gserviceaccount.com`), the page falls back
  to `workplanCsv`, a saved copy (`BAG TYPE, COLOUR, QTY`, non-zero rows), and says so. The 8 Oct 2026 copy
  has 1,243 bags across 72 bag types (158 listed), and every TOTAL row matches its colours.

## Sales keyed in late (9 Nov 2026, user's call)

Days are Nairobi dates of the till order (the query converts Odoo's UTC `date_order`). When a shop's sales
are keyed in after the day they happened, as with paper receipts, `salesDateFix` in the config moves them back:
a list of `{"from": "YYYY-MM-DD HH:MM", "to": "…", "asDate": "YYYY-MM-DD"}` (Nairobi time, `to` exclusive).
Every sale keyed in that window counts on `asDate`. **Nyeri:** Saturday 7 Nov's printed sales ran from Saturday
morning to Monday 9 Nov morning, and were keyed in through Sunday night and early Monday. So Sat 7 Nov 06:00 to
Mon 9 Nov 06:00 all counts as **Saturday 7 Nov** (374 bags, KES 645,169), and Nyeri has **no Sunday 8 Nov sales**.
Friday 6 Nov stays as the till recorded it (62 bags).

## Launch day

**Day 1 = the first day the till sells a bag** (by the sales rules below; a test or non-bag line doesn't count).
Until then the page shows "Not open yet" with the opening stock ready. Days are counted in Nairobi
dates; "today" is day N.

## Sales

Bags sold use the dashboard's headline rules (`sql/bags_sold_total.sql`): every till line with qty ≠ 0
(refunds net), **no** combo wrappers ("A + B"), delivery, customisation, straps, KES-discount lines,
samples, POS-category lines or excluded products; bags **inside** combos (sub-lines) are counted. Revenue
= `price_subtotal_incl`. Each line's product resolves to a workplan bag type: `product_catalog.csv`
(`PRODUCT NAME → BAG TYPE`), else the longest workplan bag type the name starts with; Odoo's
"Standard Travel …" is the workplan's TRAVEL. The colour is what
follows the bag type in the name ("ACE BLACK TT" → BLACK TT). Lines that match no bag go under
**Other** (shown, not in sell-through).

## What the page shows

1. **Status line:** Day N since the first sale on {date} (or "Not open yet"), the opening-stock source
   (live sheet / saved copy), and when it was built.
2. **KPI cards:** bags sold · revenue · **sell-through** (sold ÷ opening stock) · bags per day vs Rongai's
   first N days · at shop · in transit · not sent yet (see below).
3. **Race vs Rongai:** cumulative bags by launch day, Nyeri vs Rongai's first `days` days (Rongai day 1 =
   22 Apr 2026). The gap on today's day number reads "ahead / behind Rongai by N bags".
4. **Per-bag table** (every stocked bag type, plus any bag sold that wasn't in the workplan): price, opening
   stock, not sent, in transit, at shop, where now, sold, sell-through %, Kenya posts this month and last week, and a **marketing verdict**:
   - **Posted & selling:** posted this month and sold here.
   - **Posted, not selling:** posted but 0 sold here; check display and pricing.
   - **Selling without posts:** sold here with no Kenya posts this month; a candidate to post.
   - **Not posted, not selling:** neither.
   Each bag opens to its colours (opening, not sent, in transit with its sent date, at shop with its arrival
   date, sold). Sorted by sold, then opening stock.
   **Total row (26 Oct 2026, user's call):** at the foot of the table, the bags listed (it follows the filter and the
   search): opening, not sent, in transit, at shop, sold, sell-through (sold ÷ opening), posts this month and last week, and how many of the
   listed bags were posted this month.
   **Export (30 Oct 2026, user's call):** two buttons above the table download a CSV (opens in Excel) of the
   bags listed, so they follow the status filter, the marketing filter and the search:
   - **Export bags:** one row per bag: bag, in workplan, price, opening, not sent, in transit, at shop, where now,
     sent on, at shop since, sold, sell-through %, revenue, value of opening / at shop / in transit / not sent at
     the price, posts this month, posts last week, marketing.
   - **Export by colour:** one row per bag × colour: bag, colour, price, opening, not sent, in transit, sent on,
     at shop, at shop since, sold.
   File name: `{shop}_opening_stock_{date}.csv` / `{shop}_opening_stock_by_colour_{date}.csv`.
5. **Marketing panel:** how many stocked bags were posted this month (Kenya), and the average sell-through of
   posted vs unposted bags at this shop.

## Where the stock is (30 Oct 2026, user's call)

Every bag in the opening stock is tracked from the warehouse to the shop, per bag and colour, live from Odoo:

- **At shop** = on-hand at `stockCode` (e.g. everything under `NYERI/`).
- **In transit** = on-hand at `transitLocation` (sent by the warehouse, not yet received at the shop).
- **Not sent** = opening − sold − at shop − in transit (never below 0).
- **Sent on:** the dates of the warehouse moves into transit that haven't been received yet (moves out of
  transit are taken off the oldest send first).
- **At shop since:** the date of the last move that brought that bag into the shop (from transit or straight
  from CBD; customer returns don't count). A bag is **all at shop** when nothing is in transit or unsent.
- Each bag gets a **Where now** status: **All at shop** (since {date}), **Part at shop** (some still in
  transit or unsent), **In transit** (sent {date}, N days ago), **Not sent**. Filter buttons pick a status.
- KPI cards **At shop**, **In transit** (oldest send still on the road) and **Not sent yet**, each in bags and KES
  at the price below. They replace the old "Stock left" card; the table's "Left" column is now "At shop".
- **Stock sent that isn't in the workplan** (extra bags the warehouse added) is listed as its own row, marked
  "not in workplan", so the at-shop and in-transit totals match Odoo. Bag types for these come from the price
  list's names too.

**All received (9 Nov 2026, user's call):** `"allReceived": true` in the config means the shop confirmed every
bag arrived. Stock is then the **at-shop** figure only: in transit and not sent are 0 (the Odoo transit location
isn't read, even if a transfer there was never validated), so every bag reads "All at shop". **Opening stock** is
then **bags sold + at shop**, per bag and colour, instead of the workplan quantity, so sell-through = sold ÷ (sold
+ at shop). The workplan still decides which bags are listed and which are marked "not in workplan"; the opening
KPI totals the workplan bags only, matching the sold figure the sell-through card uses. Nyeri is set this way.

## Prices (30 Oct 2026, user's call)

Each bag's price is the dashboard's own full price: `offers_prices.json` (`price`, the list Offer Picking uses),
else `bag_original_prices.json`. The table shows it per bag, and the stock cards value bags at it
(opening stock value, value at shop / in transit / not sent). Revenue stays the till's real takings.

## Marketing posts

Posts are recorded **per market, not per shop**: `MONTHLY_MARKETING_POST` and `WEEKLY_MARKETING_POST`
(col D bag type, col E Kenya). The page uses the **Kenya** count for each bag Nyeri stocks. Weekly posts are
a week in arrears, so "last week" is the sheet's weekly figure. Sheet unreachable → posting columns show "–"
and the verdicts are hidden.
