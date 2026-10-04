# Product (bag) targets

**Generator:** `lib/product_targets.py` → `product_targets_<YYYY-MM>.csv` (`python -m lib.product_targets`).
Each month's **units to sell per bag**, derived from Odoo — no per-bag sheet column needed.

## The total

The month's Odoo targets (`sales_pos_target`, `period = 'month'`): **every shop till** (scope `pos`, all 19 —
Sinza / Dar-es-Salaam and Uganda included) **plus Corporate** (scope `corporate`), `target_qty` summed.
October 2026: 26,850 + 1,163 = **28,013 bags** (KES 56.0M). Shops keep their own Odoo targets on the
pages that show shops; this file splits the same total by bag.

## The split — by each bag's share of recent sales

- **Base period:** the last three complete months (Oct 2026 → 1 Jul – 30 Sep).
- **Sales counted** like the dashboard's bag count (`sql/bags_sold_total.sql` rules): every shop till, combo
  contents counted per bag, refunds netted, delivery / straps / customisation / samples / discount lines and
  **gift bags** left out — **plus Corporate's invoiced bags** (paid / ≤ 25 % unpaid customer invoices;
  embroidery and customisation fees are not bags). Products fold into their catalogue bag
  (`bag_classifier` infer — all colours of Jumbo = JUMBO; laptop sleeves = LAPTOP SLEEVE; new products
  not yet in the catalogue by their name, e.g. LAFEMME).
- **New bags are scaled to the days they were in the shops.** A bag's launch = its **first sale on any till,
  ever**. Days available = from max(launch, period start) to the period end, **at least 14** (so a bag a few
  days old doesn't get an inflated rate). Its **full-period equivalent** = sold in the period ÷ days available ×
  days in the period. A bag on sale the whole period keeps its actual sales (equivalent = actual).
- **…and to the days it actually had stock.** A bag that ran out for part of the period isn't penalised for
  days it couldn't sell. Each bag's **daily on-hand in the shops** (every shop stock location incl. WEB, DAR,
  UG — never warehouses) is rebuilt from Odoo: today's on-hand (`stock_quant`), walked back day by day with
  the done stock moves into / out of the shop locations. A day counts as **available** if the bag (any
  colour) had stock in a shop at the start or end of that day, or sold that day. **Days available** = available
  days between max(launch, period start) and the period end (at least 14). Full-period equivalent = sold ÷
  days available × days in the period.
- **Share** = the bag's full-period equivalent ÷ the sum of all bags' equivalents.
- **Target** = share × the month's total, rounded so the targets add up exactly (largest remainder).

## No zero targets

A bag that sold nothing in the base period gets **no row** (no target), and a bag whose target rounds to
0 is dropped. (Bags that only exist on the sheet and never sold — Ella Sling, Mradi Travel, … — are not
targeted until they sell.)

## Output columns

`Bag · Launch (first sale) · Days available · Jul · Aug · Sep sold · Period sold · Full-period equivalent ·
Share % · Target (units) · Sheet target (col C, for comparison)`.

## Used as the monthly bag target (from October 2026)

These targets **replace MONTHLY_TARGET column C** everywhere the dashboard reads it — Current Performance,
Forward Projections, New Products, Posting Yields and the offer data (combo / Power Deal targets). One helper,
`product_targets.monthly_target_rows(sheet_rows)`, takes the sheet's rows and returns them with **column C =
the bag's target** (matched by bag, colours folded; a bag on several sheet rows gets it once) and **column E =
max(C − D, 0)**; bags with a target but no sheet row are appended. Everything else on the sheet is kept —
the **New Products tick (col I)** and the **on-offer tick (col F)** still come from it. Sheet bags with no
target (no sales in the base period) get **0**.

Targets come from `product_targets_<YYYY-MM>.csv` for the month (built from Odoo by
`python -m lib.product_targets` if it's missing). If it can't be built (Odoo down, no file), the sheet's rows
are used unchanged and a warning is printed. The reference workbook `Bag targets <Month YYYY>.xlsx` has the
same calculation as live Excel formulas.
