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

**Shown as one span (9 Nov 2026, user's call).** The Sales by day table gives the printed sales **one row** for the
days they cover ("Days 2–3, Sat 7 Nov to Sun 8 Nov"): the total, how many days the printout took (2) and about how
many bags a day, with a Total row at the foot. **The race chart** gives that span **one point** ("2–3" on the
launch-day axis, a yellow dot labelled "Sat 7–Sun 8 Nov: 374 bags, printed over 2 days"); every line is read at the
end of the span (day 3), so the comparison stays like for like. The axis shows short day numbers; the hover gives
the dates and the printed-sales span.
- **Opening waterfall: "Opening sales vs the best opening" (9 Nov 2026, user's call):** under the race chart, in the
  style of the other waterfalls. A shop's **opening** = what it sold over the days it took to record its opening sales
  (`openingDays` in the config: **Nyeri 3, Rongai 1, Kisii 3, KTDA Shop 1**; usually 2 to 3 days, the time it takes to
  key in the opening sales). **First bar** = the best opening (Kisii, 656) or the shop picked with **Start from**;
  **one bar per opening day** = this shop's day minus the other shop's same opening day (a day past a shop's opening
  counts 0), printed sales one bar for the days they cover ("Days 2–3", marked "printed"); **last bar** = this shop's
  opening (Nyeri 436). The biggest step is boxed "biggest change"; the axis starts below the lowest level; the hover
  gives both shops' bags for that day; the note gives each opening's days and bags a day.
**Other pages:** `lib/sales_date_fix.py` reads the same `salesDateFix` for the **Why did we move?** waterfall
(`lib/why_moved.py`, Current Performance / Product Performance / New Products). It has only a day per till, so it
moves whole days: the window's first day up to the day before it ends (Nyeri: 7 and 8 Nov → Sat 7 Nov; 9 Nov stays).
Under the waterfall a **Printed sales** line names the shop, the bags, the span and the day they count on, whenever
that day is in a period shown.

## Race lines, sales by day, product performance, folding (9 Nov 2026, user's call)

- **More launches on the race chart:** `alsoCompare` in the config (`[{"shop", "till"}]`) draws extra dotted lines
  beside the main `benchmark`: Nyeri races **Rongai** (main, used by the KPI cards), **Kisii** (day 1 = 27 Nov 2025)
  and **KTDA Shop** (day 1 = 30 Jan 2026), each from its own first sale. The note under the chart gives each one's
  bags on today's day number and whether the shop is ahead or behind. Chart labels carry the date ("Day 2 Sat 7 Nov").
- **Sales by day:** a table under the race chart, one row per launch day (date, bags, KES). A day carrying a
  `salesDateFix` says which span it really covers ("Sales from Sat 7 Nov morning to Mon 9 Nov morning … all counted
  as Saturday 7 Nov"); a day those sales were moved off reads "No sales of its own: counted in Saturday 7 Nov".
- **Product performance at {shop}:** which bags, categories and colours carry the shop's sales, from the same till
  lines (`SL.perf` = `[launch day, bag, colour family, category, units, KES]`; category from `product_catalog.csv`,
  colours folded with `lib/colours.family`). Controls: **Since launch** or any single launch day (a fixed day is marked
  `*` with its span on hover), **Share by** Units / Revenue. Cards: bags sold, top bag, top category, top colour.
  Tables: top-selling bags (top 15, "Show all"), categories (bags stocked), colour families, each with share bars;
  **sell-through** (sold ÷ opening) for Since launch only.
- **Every bag in the opening stock folds:** the panel starts **collapsed** (its heading shows bags, opening, sold);
  tap the heading to open it. **Expand all colours** / **Collapse all colours** open or close every listed bag's
  colour row (they follow the filters and search).

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
