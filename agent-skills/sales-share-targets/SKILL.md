---
name: sales-share-targets
description: Split a month's total sales target (units) across products by each product's share of recent sales, scaling new and out-of-stock products to the days they were actually available (launch date + daily stock rebuilt from stock moves), with largest-remainder rounding so targets add up exactly and no zero targets. Use when asked to set per-product / per-SKU monthly targets from a shop-level or company target, to replace hand-set targets, or to explain how product targets were derived (includes an Excel-with-formulas pattern for reference).
---

# Sales-share targets per product

**Target per product = month total × (product's full-period sales ÷ all products' full-period sales).**

`scripts/share_targets.py` is pure Python: `available_days()` and `allocate()`.

## Steps

1. **Total** — the month's target in units, e.g. the sum of every shop's / channel's target in the POS or ERP
   (+ corporate / B2B if it has its own). Shops keep their own targets; this splits the same total by product.
2. **Base period** — the three complete months before the target month.
3. **Sales per product per month** in that period — every channel that the total covers (POS + invoices),
   bundle contents per item, refunds netted, non-products out, variants folded into the product.
4. **Launch** = each product's first sale ever.
5. **Days available** (optional but recommended) — rebuild each product's **daily on-hand in the shops**:
   start from today's on-hand and walk back day by day subtracting the done stock moves *into* the shops and
   adding those *out of* them (shop↔shop moves cancel). A day counts if the product had stock at the start or
   end of the day or sold that day. Pass `onhand_now`, `net_moves {product: {date: net into shops}}`,
   `sold_days {product: set(dates)}` to `available_days()`. Sanity check: the rebuilt stock should never go far
   below zero; if it does for a product, its moves are incomplete — trust launch dates only for it.
6. `allocate(sold, launch, total, start, end, months, avail=…)`:
   - days used = stocked days since launch (or days since launch), **at least 14**, at most the period;
   - **full-period equivalent** = sold ÷ days used × days in period (a product in stock all period keeps its
     actual sales);
   - share → raw target → **largest-remainder rounding** so the targets sum exactly to the total;
   - products that didn't sell get **no row**; targets that round to 0 are dropped.
7. Optional guard: products with very little evidence (e.g. < 5 sold) can be excluded or hand-set.

## Deliver

- A CSV per month (`product_targets_<YYYY-MM>.csv`): product · launch · days available · each month's sales ·
  period sold · full-period equivalent · share % · target · old target (for comparison).
- A reference **Excel workbook** with live formulas: *Method* (steps + a worked example row), *Inputs*
  (each channel's target summing to the total, period dates, minimum days — blue inputs), *Bag targets*
  (sales and stocked days as blue values; days used `=MIN(MAX(days,min),period)`, equivalent, share
  `=J/SUM(J)`, raw `=share*total`, rounding via `RANK` of the fractional part, final target, a total-check
  cell). Recalculate it in Excel/LibreOffice and confirm 0 formula errors and the check reads OK.
- Explain with one worked example: "Jumbo: 3,672 sold over 92 days → 7.26 % × 28,013 = 2,035".

## Tests

`scripts/test_share_targets.py` — `python -m pytest scripts -q`.
