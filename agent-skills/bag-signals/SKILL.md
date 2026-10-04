---
name: bag-signals
description: Quant signals per product from daily sales and stock — real trend vs luck, sales volatility, Sharpe-style reliability, market beta, 14-day run-out risk, safe stock to restock, and posting beta (extra sales per marketing post), each turned into an action (Restock first / Falling — act / Post more / Clear stock / Rising — feed it / Hold). Use when asked what to post, push, restock or clear for a retail catalogue, whether a product is really rising or falling, how much safety stock to hold, or to apply random-walk / volatility / Sharpe / beta ideas to sales data.
---

# Bag signals — quant finance applied to product sales

Four ideas from quant finance, applied to each product's **daily unit sales**:

| Idea | Applied to a product | Tells you |
|---|---|---|
| **Random walk: drift + noise** | daily sales = average pace (drift) + luck | a rise/fall is **real** only when it beats the luck |
| **Volatility** | standard deviation of daily sales | swing; with the **square-root rule** it sets safe stock and run-out risk |
| **Sharpe ratio** | average ÷ swing | **reliability** — steady sellers are safe to post / push |
| **Beta** | Cov(product, all products) ÷ Var(all), scaled to the product's share | > 1.3 booms on busy days (paydays, weekends) — stock before them |

`scripts/bag_signals.py` is pure Python (no dependencies). Copy it into the project.

## Inputs you must build from the project's data

- `daily = {product: [units per day, oldest first]}` over the last **91 days**, **None for days before the
  product launched** (its first sale ever) so new products aren't judged on days they didn't exist.
  Count units the way the business counts a "sale": items inside bundles/combos per item, refunds netted,
  non-products (delivery, gift wrap, samples, discount lines) out, colour/size variants folded into the product.
  End on the **last complete day**.
- `total = [all products' units per day]` — same days.
- `stock = {product: units on hand now}` — sellable locations only (shops), never bulk warehouses.
- Optional: weekly posts per product (from the marketing tracker) saved every week to a history file
  `[{week, bags: {product: {posts, sold}}}]` → `posting_beta(history, product)` once ≥ 6 weeks exist.

## Maths (per product)

- **Avg / day** μ, **Swing / day** σ (sample std dev) over the days since launch.
- **Reliability** = μ ÷ σ. ≥ 1 steady · < 0.5 erratic.
- **Trend z** = (mean last 28 d − mean previous 63 d) ÷ (σ·√(1/28 + 1/63)). **≥ +2 really rising, ≤ −2 really
  falling**; between = chance — don't react.
- **Beta** = Cov(product, total) ÷ Var(total) ÷ (μ ÷ mean total) → 1 = moves in proportion to its share.
- **Days of cover** = stock ÷ μ.
- **Run-out risk (14 d)** = P(14-day demand > stock), demand ~ Normal(14μ, σ√14).
- **Safe stock (14 d)** = 14μ + 1.645·σ·√14; **Restock** = max(safe − stock, 0).
- Fewer than 10 units in the window → "too few sales to judge".

## Action — first rule that fits

1. **Restock first** — run-out risk ≥ 50 % (don't post or push what you can't sell).
2. **Falling — act** — trend z ≤ −2 (offer / post it; check price, placement).
3. **Post more** — reliability ≥ 1 and cover ≥ 21 days.
4. **Clear stock** — cover ≥ 90 days (offer, bundle, move to a shop that sells it).
5. **Rising — feed it** — trend z ≥ 2.
6. **Hold**.

## How to deliver it

- A table: product · action · avg · swing · reliability · trend · beta · stock · cover · run-out % · restock ·
  posts · per-post — sortable, with a plain-language hover on each number; plus counts per action.
- Explain results in plain words ("Antitheft has 7 days of cover; add 370 to be 95 % safe for two weeks").
- Validate on real data before presenting: action counts should look plausible (a few % falling, best sellers
  usually reliable); spot-check one product's μ, σ and run-out by hand.

## Tests

`scripts/test_bag_signals.py` — run `python -m pytest scripts -q` from this folder.
