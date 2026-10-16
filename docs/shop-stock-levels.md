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
- **Send now** = Max − stock, for a shop at or below Min. **Warehouse** (CBD/Stock — the store that restocks
  the Kenya shops) is shown only here, as what can cover the send-now today. Sinza and Uganda are restocked
  from their own stores — send-now shows the units, no warehouse figure.

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

### Next month (preparedness) — from the 15th

From the 15th of the month the report adds next month: **next month's need** (next month's Odoo shop and bag
targets; while next month's targets aren't in Odoo yet, **this month's need is used as the estimate** and the page
says so), and **short for next month** = next month's need − the expected balance at month end, when positive.
Rolled up per bag across shops, this is the list to produce / buy before the month starts. Before the 15th the
section shows when it opens.

## Page

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
