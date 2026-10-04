# Bag Signals — quant view of each bag (posting · stock · selling)

- **Generator:** `bag_signals.py` (maths in `lib/bag_quant.py`) → `bag_signals.html`
- **Data marker:** `<!-- BAGQ_DATA_START -->…<!-- BAGQ_DATA_END -->` (const `BQ`)
- **Locked:** password `BAG_SIGNALS_PASSWORD` in the app's Secrets (like Push Planner; open locally without one).
- **State file:** `bag_posts_history.json` — each bag's posts per week, saved every run (for the posting beta).

The four ideas from the "Quant Finance From Scratch" lessons (random walk, volatility, Sharpe ratio, beta),
applied to each bag's **Kenya daily sales** (every Kenya till + Website, bags_sold_total rules: combo contents
per bag, refunds netted, gift bags / delivery / samples out; colours fold into the bag) over the last
**91 days**, its **live Kenya shop stock** and its **marketing posts**.

## Per bag

| Column | Maths | Meaning |
|---|---|---|
| **Avg / day** (drift) | mean daily sales μ over the 91 days (days before launch excluded) | the bag's underlying pace |
| **Swing / day** (volatility) | standard deviation σ of daily sales | how much a day's sales jump around |
| **Reliability** (Sharpe-style) | μ ÷ σ | sales per unit of swing — high = a steady seller, safe to push and post; low = erratic |
| **Trend** (drift vs noise) | z = (μ last 28 d − μ previous 63 d) ÷ (σ·√(1/28 + 1/63)) | **real** rise/fall only when \|z\| ≥ 2; smaller moves are chance (random walk) |
| **Market beta** | β = Cov(bag, all bags) ÷ Var(all bags) on daily sales, scaled so β = 1 moves in proportion to its share | β > 1.3 booms on busy days (paydays, weekends) — stock up before them; β < 0.7 sells regardless |
| **Stock** | live on-hand in the Kenya shops (`lib/stock`) | |
| **Days of cover** | stock ÷ μ | |
| **Run-out risk (14 d)** | P(demand over 14 days > stock), demand ~ Normal(14μ, σ√14) — the square-root rule | chance of a stock-out in the next two weeks |
| **Safe stock (14 d)** | 14μ + 1.645·σ·√14 | stock needed to be 95 % sure of not running out in 14 days; **Restock** = safe stock − stock when positive |
| **Posts** (last week / this month) | WEEKLY / MONTHLY_MARKETING_POST, Kenya | |
| **Posting beta** | slope of weekly sales on weekly posts once ≥ 6 weeks of `bag_posts_history.json` exist | extra bags sold per post; "learning" until then |

## Action (first rule that fits)

1. **Restock first** — run-out risk ≥ 50 %: don't post or push a bag you can't sell; order / move stock.
2. **Falling — act** — trend z ≤ −2: a real decline; put it on an offer or post it, check price / placement.
3. **Post more** — reliability ≥ 1 and cover ≥ 21 days and no real decline: a steady seller with stock — posts
   convert reliably.
4. **Clear stock** — cover ≥ 90 days: slow mover with too much stock — offer / combo / move to a better shop.
5. **Rising — feed it** — trend z ≥ 2: a real rise; keep posting and keep it stocked.
6. **Hold** — otherwise.

Bags with fewer than 10 sales in the 91 days are listed under "too few sales to judge".
Website has no shelf; stock = the Kenya shops only.

## Page

KPI strip (bags at run-out risk, real risers / fallers, post-more list size, stock to restock), the action
counts, then one sortable / filterable table (search, action, category) with the columns above. Every number
has a hover explaining it in plain words.
