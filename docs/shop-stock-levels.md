# Shop Stock Levels — min / max per shop, stocks report and next-month preparedness

- **Generator:** `generators/shop_stock_levels.py` → `html/shop_stock_levels.html`
- **Data marker:** `<!-- SSL_DATA_START -->…<!-- SSL_DATA_END -->` (const `SSL`)
- **Menu:** Products section, **right after Bags On vs Off Offer** (`dashboard_pages.json`).
- **Regenerate:** `python generators/shop_stock_levels.py`

A stock monitor for the shops: what each shop has, what it needs this month, when to refill it (min / max),
who is waiting for a bag it doesn't have, what will be left at month end, and — from mid-month — what next
month will be short of.

## Each shop's monthly need per bag ("the way we did the targets")

1. **Bag targets** — the month's company bag targets (`lib/product_targets`, docs/product-targets.md): Odoo total
   split by each bag's Jul–Sep share, scaled to days in stock.
2. **Shop targets** — each till's Odoo monthly target (`sales_pos_target`, scope `pos`, `target_qty`); Corporate is
   not a shop (its share of each bag target is left out pro rata).
3. **Shop × bag need** — the two are matched by **iterative proportional fitting** starting from where each bag
   actually sold in the base period (Jul–Sep, POS, combo contents per bag, the bag-count rules): the grid is
   scaled so **each shop's row adds up to its Odoo target and each bag's column adds up to its bag target**
   (×  the shops' share of the grand total). New bags (launched inside the base period) start every shop at the
   shop's overall share, so they get a need wherever the shop sells. A bag that never sold at a shop and isn't
   new gets no need there.
4. **Daily need** = monthly need ÷ days in the month.

## Min / Max (per shop, per bag — colours folded; colours on hover)

- **Min** = 7 days of need (round up) — at or below it, **refill**.
- **Max** = 21 days of need (round up) — refill **up to** it; above it is **overstocked**.
- **Status:** Out of stock (0 on hand, has a need) · Below min (at or below Min and below Max) · OK · Over max ·
  Stock, no need (on the shelf but no need this month) · Not stocked (no need, no stock — hidden).
- **Stock health %** (18 Oct 2026, per shop and all shops) = the target need of the bags sitting **within Min–Max**
  (status OK) ÷ the shop's total target need — bags weighted by their monthly need, so a fast bag out of stock
  counts more than a slow one. Shown on each shop block (with its over-max count) and as the first KPI.
- **Send now** = Max − stock, for a shop at or below Min. **Warehouse** (CBD/Stock — the store that restocks
  the Kenya shops) is shown only here, as what can cover the send-now today. Sinza and Uganda are restocked
  from their own stores — send-now shows the units, no warehouse figure.

## Stock monitor — grouped, and what each shop should request (19 Oct 2026)

Every shop block (e.g. KTDA) lists its bags **grouped by status** — Out of stock → Below min → Over max → OK → Stock,
no need — then **by category inside each status** (core 5 first; `data/bag_tiers.csv`), each group with its
**% covered** = Σ min(have, Max) ÷ Σ Max (how much of the stock the shop should hold it actually holds), then the bags.
The Show filter (Needs action / All) still decides which bags are listed. **Bags as tiles** (19 Oct 2026): under each category row
the bags are tiles, ranked inside the category by this month's need (**#1** = the bag the shop needs most); a tile
shows the status, **send now** (big), then have, Min, Max, sold, need, month-end and people waiting as labelled values
(no dots); its top edge takes the status colour; click / tap for the full detail. The month-end balance is shown in words (19 Oct 2026): **Short by 31 Oct** with the
number of sales the shop can't make before month end at the target pace (when have − daily need × days left is
negative), or **Left on 31 Oct** with what will remain for next month; hovering it (and the bag's detail) gives the
sum — e.g. Claire Handbag at KTDA: stock 0 − 1.06 a day × 13 days = −14 → *Short by 31 Oct 14*, still to sell 25,
send now 23 covers it and the rest carries into November. Each **category row collapses / expands** its tiles (click the row; ▾ open, ▸ closed); open by default, remembered while the page is open. **Status rows collapse too** (Out of stock, Below min…: click the row to hide or show everything inside it), and each shop has **Collapse all groups / Expand all groups** buttons for its statuses and categories. The column headings (Bag, Status, Have, Min, Max, Sold / need, Month-end, Waiting, Send now) repeat, small and muted, just above every category row so they stay next to the numbers when scrolling.

**Request list** (per shop, in the block): what the shop should ask for, in line with what it must sell through
**November**, so whatever is left at the end of October is used next month:

| Column | Rule |
|---|---|
| **Request now** | bags at or below Min: refill to Max (= send now) **if November still needs the bag**; if November has no need for it, only what is still to sell this month beyond the shelf (max(still to sell − have, 0), capped at the refill) — nothing is sent that would be stranded |
| **Ask before 1 Nov** | what November will still be short after this month: max(short for November − request now, 0) |

Listed core 5 first, then by request; totals per shop. **Shown as a closed section** (19 Oct 2026): the header carries the totals (request now, ask before 1 Nov, bags); it opens only when clicked, so the shop block stays short; remembered per shop while the page is open. Still to sell = max(need − sold, 0); November need = the
November row need (from the KES 66.6M revenue target).

## Stocks report

| Column | Meaning |
|---|---|
| **Have** | shop stock now (shops only — the warehouse is not "have") |
| **Need (month)** | the shop × bag monthly need |
| **Sold (MTD)** | sold this month so far |
| **Still to sell** | max(need − sold, 0) |
| **Missing** | still to sell − have, when positive (this month can't be met from the shelf) |
| **Expected balance at month end** | have − daily need × days left (negative = runs out before month end; the day it runs out is on hover) |
| **Waiting** | out-of-stock call-backs (online + walk-in) for that bag at that shop, still waiting, asked in the chosen Leads period (`lib/oos_callbacks`); only requests for a bag we sell or stock (free-text repairs / spare parts are left out) |

### Bag health (by bag, 18 Oct 2026)

**Grouped (19 Oct 2026):** the table is grouped by **health category** first (Out of stock → Low cover → Overstocked →
Healthy → Dead stock), then by **bag category inside each health group** (core 5 first) with its **% covered**
(Σ over the shops of min(have, Max) ÷ Σ Max), then the bags. Each group and category row carries the summed numbers. **Tiles and collapse (19 Oct 2026):** the bags under each category are tiles ranked by
this month's need (#1 gold) showing the health, **missing this month** (big), Health %, Covered %, have, need, sold,
still to sell, the month-end balance in words (Short by / Left on 31 Oct, the sum on hover), shops out and the
warehouse; health groups and categories collapse / expand (click the row), plus Collapse all / Expand all groups; the
column headings repeat above every category.

Each bag, folded across the shops (have, need, sold and each shop's Min / Max summed), gets **one category**:

| Category | Rule (in this order) |
|---|---|
| **Out of stock** | need > 0 and 0 on the shelves |
| **Low cover** | need > 0 and have ≤ the summed Min (7 days of need) |
| **Overstocked** | need > 0 and have > the summed Max (21 days) — or no need this month but stock that is selling |
| **Healthy** | need > 0, within Min–Max |
| **Dead stock** | stock on the shelves, no need this month and nothing sold this month |
| *No stock, no need* | hidden |

**Health %** per bag = the need of the shops where that bag sits within Min–Max ÷ the bag's total need (need-weighted,
like the per-shop Stock health %; — when the bag has no need). Folding hides shop gaps — a bag can be Healthy in
total with shops out — so Health % shows how much of its need is actually covered shop by shop.
Page: category chips with counts (all bags, whatever the Show filter) that filter the table; with **All** the usual
Show filter applies. Category and Health % columns.

### Next month (preparedness) — from the 15th

From the 15th of the month the report adds next month: **next month's need** (next month's Odoo shop and bag
targets; while next month's targets aren't in Odoo yet, **this month's need is used as the estimate** and the page
says so). **November 2026:** next month's need comes from the **KES 66.6M revenue target**
(docs/product-targets.md — bag targets split from the revenue-derived total) with shop targets = October's Odoo shop
targets scaled to the November total (each shop keeps its share; Corporate's share left out as usual), fitted with the
same IPF from where each bag sold in November's own base period (Aug – Oct); the page labels it
"from the KES 66.6M revenue target". Check (18 Oct 2026): 33,313 bags (KES 2,000.17 a bag) → shops 31,930, Corporate
1,383; the shop rows add up to 29,697 = the shops less **Website** (2,263 — online, no shelf rows), ± rounding. Then **short for next month** = next month's need − the expected balance at month end, when positive.
Rolled up per bag across shops, this is the list to produce / buy before the month starts. Before the 15th the
section shows when it opens.

### November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026)

- **Without** = the shops' own shelves (the "have" above; no warehouse). **With** = the shops plus the two stores that
  restock the Kenya shops: **CBD/Stock** and **VLD/Stock** (exact locations, `lib/stock.odoo_stock_at_location`;
  VLD's dispatch staging, returns verification and samples are left out — not sendable stock).
- **Buffer stock** = with − without = CBD/Stock + VLD/Stock, per bag.
- Per bag: **November need** (shops) · stock shops only · stock with CBD + VLD · buffer · **short without** (Σ over shops
  of max(November need − expected month-end balance, 0) — the "short for next month" above) · **short with** = the
  Sinza / Uganda shops' short (CBD / VLD don't restock them) + max(Kenya shops' short − buffer, 0).
- KPI pair: **prepared % without** = (need − short without) ÷ need, **prepared % with** = (need − short with) ÷ need.

### Product rating and core 5 vs other 13 categories (18 Oct 2026)

- **Category** = `data/bag_tiers.csv` CATEGORY (the Bags on offer table). **Core 5** = BACKPACK · TRAVEL · HANDBAG ·
  MAN BAG · SLING — about **75 %** of bags sold (user's week 3 of October: 2,764 of 3,662); **Other 13** = every other
  category (BRIEFCASE, GIFT BAG, WAIST BAG, CHEST BAG, SCHOOL BAG, SPORT, BABY BAG, MESSENGER, LUNCH BAG, WASHBAG,
  THIGH BAG, MAKE UP, HOOD) — about **25 %**. The page shows the live mix from this month's sales beside it.
- **Rating** per bag, from **November cover % with the buffer** = (November need − short with buffer) ÷ November need:

  | Rating | Covered | Meaning |
  |---|---|---|
  | ★★★★★ | ≥ 90 % | ready |
  | ★★★★ | 70–89 % | top up |
  | ★★★ | 50–69 % | produce soon |
  | ★★ | 25–49 % | produce now |
  | ★ | < 25 % | urgent |

  Shown with both % (shops only · with buffer). E.g. ANTITHEFT (BACKPACK, core): 0 % → 25 % = ★★.
- **Split strip:** November short with buffer in the core 5 vs the other 13 — units and % of the short, beside each
  group's share of sales. A group whose share of the short is above its share of sales is the less prepared one.
- **The table is grouped by rating** (18 Oct 2026), most urgent first: ★ → ★★★★★, one collapsible block per rating
  (★ and ★★ open) with its bag count, need, short with buffer and cover %. Inside each rating the bags are grouped
  **by category** (core-5 categories first, then by short), each category with a subtotal row; bags within a
  category by short with buffer. The column headings repeat (small, muted) just above every category row, so the
  headings are always next to the numbers in a long table. **Tiles and collapse (19 Oct 2026):** the bags under each category are tiles ranked by November need (#1
gold) showing the stars, covered shops only → with buffer, **short after buffer** (big), November need, shops only, with
CBD + VLD, buffer, the month-end balance in words, short with shops only and shops short; each category row collapses /
expands its tiles, the rating groups as before, plus Collapse all / Expand all groups.

## Page

**The filter bar is static** (19 Oct 2026, user's call): it stays at the top of the page and does not follow the reader (sticky controls removed here).


- **Controls:** Leads period (Last week · This week · This month · Lifetime — the periods the other pages use) ·
  Show (Needs action · All) · find a bag. No shop filter (16 Oct 2026): every shop is its own block.
- **KPI strip:** shop-bags out of stock · below min · units to send now (and how much the warehouse can cover) ·
  people waiting · units missing this month · short for next month (from the 15th).
- **Stock monitor** — **one block per shop** (most out-of-stock / below-min first; summary: out · below min ·
  send now · waiting; Expand / collapse all), each with its bags, status, have, min, max, sold / need, month-end,
  waiting and send now (Needs action = out of stock, below min, or someone waiting). Hover a bag: colours on hand
  (shop + warehouse) and the colours people are waiting for.
- **Website is an online shop** — no shelf stock, so no min / max, status, missing or next-month rows; its block
  shows only the customers waiting there (they still count in the waiting totals).
- **Stocks report — by bag** — every bag across all shops (or the chosen shop): have · need · sold · still to sell ·
  missing · month-end balance · next month need · short for next month. Hover: per shop.
- **Customers waiting** — per shop, the bags people are waiting for in the leads period, with online / walk-in.

## Data

- **Corporate-lead till orders (16 Oct 2026, user's call — revised the same day):** when a client the **Corporate team** brought in (a Corporate-app lead) pays at a shop till, the sale is **credited to that shop** like any till sale, but it's still marked as a Corporate lead (October: ESK Company, HAZINA/29958 + 29613, KES 1,707,197 → Hazina, "Corporate app lead 17 Sep · Scola Mithiri"). One that hasn't paid yet goes to the shop that hunted it (quote note → bought there before → client's town), still noted as a Corporate lead; with no shop link it isn't shown at all until something is paid at a till. Here: they count in each shop's sales history (the base period and month-to-date) — the bags left that shop.

- Stock: `stock_quant` at the shop locations (top code → till: `lib/odoo_tabs.STOCK_CODE_TO_SHOP` + WEB =
  Website), combo products ('+') left out; warehouse = `CBD/Stock`.
- Sales: POS lines, `done / invoiced / paid`, Nairobi dates, refunds netted, combo contents counted per bag, the
  usual exclusions (delivery, customisation, straps, samples, gift bags, KES discount, `sales_exclusions.txt`).
- Bag type: `lib/runway_bags.type_fn()` (catalogue bag, else name minus colour words) — the same keys as the
  bag targets.

## Shop requests — requested vs received (18 Oct 2026)

Source: the Odoo **dispatch module** (`denri_dispatch_*`), which every shop orders through — `lib/shop_requests.py`.

- **Request** = a shop's original order (`denri_dispatch_order`, request type *shop*, not a backorder, not cancelled)
  from a retail shop. Unsent quantities move to backorders (`backorder_root_id`); sent / received / still pending
  are summed over the request and its backorders, per product. Cancelled orders are left out — most are
  "Cancelled from pending queue adjustment" (the shop re-ordered and the new order carries the quantity again).
- **Stock before ordering** = the order line's own snapshot: on hand, incoming, Min / Max (dispatch stock policy),
  Odoo's suggested quantity (Max − on hand − incoming) and its alert (stockout / below min / healthy).
- **Offers** on the order date: Power Deal · Deal of the Week · timed offers · running combos (Kenya; the
  Product Performance source).
- **Effectiveness %** per shop = the average of three checks, units-weighted (user's choice, 18 Oct 2026):
  1. **Right bag** — out of stock / at or below Min when asked, or on an offer while under half of Max
     (Power Deal runs all month, so an offer alone isn't a reason).
  2. **Right qty** — asked ÷ Odoo's suggested quantity (capped at 100 %). Odoo already blocks ordering above Max,
     so the miss is **under-ordering** (Sep 2026: 13,467 asked against 20,716 suggested). Counted **once per shop × product**: all the period's asks vs the largest suggestion at any of its requests — summing each request's suggestion (the first version: 43,683) counted the same shortfall again on every re-order.
  3. **Sold through** — of what arrived, the share sold at that shop within 14 days of the first receipt (only
     arrivals 14+ days ago).
- **Fill** = sent ÷ asked (capped per line) — the warehouse's score, shown beside the shop's, never in it.
- **Sent without a request** = per shop × product, warehouse sends into the shop's stock in the period (the Shops
  menu's dispatch basis: FINWH / CBD → `<CODE>/Stock`) beyond what the shop asked for (dispatch + the old SRQ
  module, asks from 14 days before the period count). "Never asked" = no ask for that product at all. Online shops
  are left out. Shown with how many sold since they arrived and what's on the shelf now.
- **Asked, not got** (18 Oct 2026) = per request line, asked − sent − still pending: what the shop asked for that
  the warehouse closed without sending. Still-pending units are shown beside it but not counted as a miss yet.
- **Got what it asked %** (18 Oct 2026, e.g. Hilton) — one figure for both directions:
  **matched ÷ (matched + asked, not got + sent without a request)**, where matched = Σ min(asked, sent) per line.
  100 % = the shop got exactly what it asked for and nothing else. Shown on each shop's row, as a check card,
  and for all shops in the strip — it scores the asking/sending match, not the shop, so it is not in effectiveness.
- **Asked vs target** (18 Oct 2026) — the shop's asks judged against its **target need** (the page's own Min / Max,
  not Odoo's dispatch Min / Max). Once per shop × bag (colours folded), **target refill** = max(target Max − stock
  − incoming at the bag's first request in the period, 0) + the daily target need × days from that request to the
  period end (or today) — what the target says should have been brought in. Target Max = 21 days of the shop × bag
  need. **Asked vs target %** = Σ min(asked, target refill) ÷ Σ target refill (under 100 % = under-asking).
  Counted once per bag, not per request line: Hilton asks many times a month, and summing each line's gap (or
  comparing one colour's stock with the whole bag's Max) inflates the refill several times over. Also: **over target** (asked beyond the refill), **no target**
  (asked for a bag with no need at that shop) and, this month only, **needed, not asked** = bags the target needs
  now (at or below target Min on the shelf) with no ask this month, units = target Max − on the shelf. Last month
  is judged on last month's own targets (skipped when they aren't in Odoo).
- **Requested but not converting** = requested bags received 14+ days ago that sold under 25 % of what arrived
  within 14 days.
- Page: period This month · Last month; one block per shop (effectiveness · fill · requests · asked · sent ·
  received · pending), opening to the three checks and a bag table (asked · suggested · sent · received ·
  pending · stock when asked / Max · out / below min · sold in 14 days · offer), then the **Asked, not got**,
  **Sent without a request** and **Requested but not converting** tables. Hover a bag for each request.

## Shop vs shop and regions — request checks compared (18 Oct 2026)

At the top of the Shop requests section (same period switch):

- **Shop vs shop** — one row per shop: effectiveness · right bag · right qty · sold through · dispatch fill · asked vs
  target · got what it asked, each as a % chip, plus units asked. Each column is ranked: the best shop's chip is
  marked **#1** and the worst **last**; click a column heading to sort by it (default: effectiveness). A dash = the
  check had nothing to judge.
- **Regions** (`docs/shop-regions.md`, the source of truth — `lib/shop_regions.py`): the same checks per region, each
  **units-weighted** from its shops (right bag by units asked, right qty by Odoo's suggestion, sold through by units
  received 14+ days ago, fill by units asked, asked vs target by the target refill, got what it asked by matched +
  not got + unasked). Effectiveness = the average of the region's three shop checks.
- **Dispatch balance** per region: share of all units **asked** · share of units **sent** · share of the **target
  refill** (what the targets said to bring in) → **balance** = share sent − share of target refill, in points
  (+ = the region got more than its target share, − = less), plus sent without a request and asked, not got.

## Requests by category (18 Oct 2026)

Category = `data/bag_tiers.csv` (core 5 first). One table for all shops (under Dispatch balance) and one inside each
shop's block, same period switch. Per category, summed from the per-bag lists:

| Group | Columns | Reads as |
|---|---|---|
| **Target vs asks** | target refill · asked · **asked vs target %** (Σ min(asked, refill) ÷ Σ refill) · **under-asked** (refill − asked within it, + "needed, not asked") | which category the shops under-ask against their targets |
| **Left out** | **asked, not got** · **left out %** = asked, not got ÷ asked | which category the warehouse leaves out most |
| **Sent without a request** | units · **sold since arriving** · **moved %** = sold ÷ unasked units | does sending a bag nobody asked for create demand (it sells straight away) or sit |
| **Requested but not converting** | bags · received · sold within 14 days · **converting %** | which categories shops ask for in anticipation that don't sell yet |

## Shop requests and Production — Region / Shop filter and tiles (19 Oct 2026)

- **Shop requests:** a **Region** and a **Shop** filter in the top bar (regions from `docs/shop-regions.md`) narrow
  everything in the section (totals strip, shop vs shop, regions, dispatch balance, by category). The shops are
  **tiles** ranked by units asked: effectiveness (big), fill, got what it asked, asked vs target, asked, sent,
  received, pending, not got, unasked; edge colour by effectiveness (green 75 %+, amber 50–74 %, red under 50 %).
  Click a tile (or pick one shop in the filter) to open that shop's full detail underneath; click it again to close.
- **Production:** the same **Region / Shop** filter. Filtered, a product's **asked** = the chosen shops' asks only,
  and its **allowed** = the product's allowed units shared out by those shops' part of the asks (the approved list is
  per product, not per shop); approved stays the whole list's figure. Products are **tiles** ranked by units asked:
  status, % of asks allowed (big), asked, approved, allowed, tailors, priority, number of shops and the top shops
  asking (in words).

## Production — shop requests vs approved list (18 Oct 2026)

The weekly **Approved list** (`denri_production_plan`, KE-… / UG-… / TZ-…; new-shop and corporate plans left out)
is the final submission to production. Each list is set against the shops' requests of that country placed since
the country's previous list, up to the plan date, per product:
**Allowed in full** (approved ≥ asked) · **Cut** (approved < asked) · **Not allowed** (asked, not on the list) ·
**Added** (on the list, no shop asked — the planner's choice). **Asks allowed %** = Σ min(asked, approved) ÷ asked;
**approved beyond the asks** = approved − allowed. **Tailors** = units on the tailor plan (`denri_tailor_plan_line`).
The last **16** lists per country (about four months). **Period** (18 Oct 2026): pick the country, then **One list**
(choose it) · **This month** · **Last month** · **Date range** (from – to, by list date) — the lists inside the period
are added together per product (each list's asks window starts the day after the previous list, so they don't
overlap). Hover a product for the shops that asked.
- **Asks allowed %** = Σ min(asked, approved) ÷ Σ asked: of every unit the shops asked for, the share that made it onto
  the approved production list. 28 % = of each 100 bags asked, 28 were put into production; the other 72 were cut or
  not allowed. Approved units beyond the asks (planner's choice) don't raise it.
  In a period (several lists) asks and approvals are added up **per product first**, so a bag cut in one list and
  approved the next week counts as allowed — October 2026: the last list alone 28 %, the month's three lists 56 %.
- **By category** (`data/bag_tiers.csv`): asked · approved · allowed · **allowed %** · not allowed (asked − allowed) ·
  added (approved − allowed).
- **By region** (`docs/shop-regions.md`): each region's asks; its allowed units = each product's allowed units shared
  out by the shops' part of that product's asks (the list is per product, not per shop) → **allowed %** per region.
