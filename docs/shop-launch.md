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
{"shop": "Nyeri", "till": "NYERI", "stockCode": "NYERI",
 "workplanSheet": "17CQvuuvNUhNBp4LUImdxJ6pGeTmAC-D1Ediei9v0Yjs", "workplanCsv": "nyeri_workplan.csv",
 "benchmark": {"shop": "Rongai", "till": "RONGAI"}, "days": 28}
```

- `till`: the Odoo POS till (`pos_config.name`). `stockCode`: its stock location's top code
  (`NYERI/Stock` → `NYERI`). `days`: how many launch days the race chart and benchmark cover.
- **Opening stock = the workplan sheet** ("NYERI WORKPLAN": bag type, colour, quantity, with a TOTAL row per
  bag). It's read live with the dashboard's Google service account. If the sheet can't be read (not shared
  with `marketing-and-predictive-sales@steadfast-sign-498718-d9.iam.gserviceaccount.com`), the page falls back
  to `workplanCsv`, a saved copy (`BAG TYPE, COLOUR, QTY`, non-zero rows), and says so. The 8 Oct 2026 copy
  has 1,243 bags across 72 bag types (158 listed), and every TOTAL row matches its colours.

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
   first N days · stock left (live Odoo on-hand at `stockCode`; until stock lands there, opening − sold).
3. **Race vs Rongai:** cumulative bags by launch day, Nyeri vs Rongai's first `days` days (Rongai day 1 =
   22 Apr 2026). The gap on today's day number reads "ahead / behind Rongai by N bags".
4. **Per-bag table** (every stocked bag type, plus any bag sold that wasn't in the workplan): opening stock,
   sold, sell-through %, stock left, Kenya posts this month and last week, and a **marketing verdict**:
   - **Posted & selling:** posted this month and sold here.
   - **Posted, not selling:** posted but 0 sold here; check display and pricing.
   - **Selling without posts:** sold here with no Kenya posts this month; a candidate to post.
   - **Not posted, not selling:** neither.
   Each bag opens to its colours (opening, sold, left). Sorted by sold, then opening stock.
5. **Marketing panel:** how many stocked bags were posted this month (Kenya), and the average sell-through of
   posted vs unposted bags at this shop.

## Marketing posts

Posts are recorded **per market, not per shop**: `MONTHLY_MARKETING_POST` and `WEEKLY_MARKETING_POST`
(col D bag type, col E Kenya). The page uses the **Kenya** count for each bag Nyeri stocks. Weekly posts are
a week in arrears, so "last week" is the sheet's weekly figure. Sheet unreachable → posting columns show "–"
and the verdicts are hidden.
