---
name: stockout-demand
description: Count distinct people who asked for a product while it was out of stock (WhatsApp/CRM/call-back enquiries), per product, shop and colour, over lifetime / this month / this week / last week / still waiting, with each shop's current stock beside the count. Use when asked for lost or unmet demand, out-of-stock call-back lists, which shops need which colours, or to show "N people asked" chips with a per-shop and per-colour breakdown.
---

# Out-of-stock demand — people, not requests

`scripts/stockout_demand.py` (pure Python): `aggregate()`, `totals()`, `attach_stock()`.

## Input rows — one per enquiry × product asked for

`{date, shop, person, purchased, product}` from the CRM / enquiry log:
- an enquiry counts when its reason is "out of stock";
- `person` = phone number, else username, else the enquiry id — **count distinct persons**, never add counts
  (a customer who asked twice, for two shades, or at two shops counts once in the total);
- `purchased` = they bought since (for **still waiting**);
- skip junk shops / test rows; note when the product field started being recorded — lifetime only starts then.

## Periods

`lifetime` · `monthly` (pass `month_window`) · `weekly` (this Sun–Sat to date) · `lastweek` (previous complete
Sun–Sat) · `current` = still waiting (any date, not purchased).

## Keying

`key_fn(product name)` → the page's product key (reuse the page's own matching so counts line up with its
rows); return None to drop non-products. `colour_fn(name)` → colour (family or exact, as the page uses).
Re-keying several names onto one product **unions person sets**.

## Output block

`{period: {product: {"total": people, "shops": [[shop, people, stock], …], "colours": [[colour, people,
[[shop, people, stock], …]], …]}}}` — shops high → low; `attach_stock(block, key_fn, colour_fn,
{shop: {name: qty}})` adds each shop's on-hand (per colour under colours); shops without a shelf get None.

## Show it as

A chip "📞 N asked" (or "N waiting") per product; hover/tap → product name, shops with "x stk" badges (red at
0), then each colour with its shops — so you see where a call-back can be served now. Hide at 0. If the data
source is unreachable, return empty blocks and hide chips (never fail the page).

## Tests

`scripts/test_stockout_demand.py` — `python -m pytest scripts -q`.
