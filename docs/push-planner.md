# Push Planner (`push_planner.py` → `push_planner.html`, `PP`)

**What to push this week, where, and why some bags aren't moving** — Kenya, Sinza and Uganda.
A weekly decision page. It sits beside **Offer Picking**: Offer Picking plans *next month's*
combos and Power Deals; the Push Planner works *inside* the month, week by week, per bag and per
shop, and checks whether last week's calls worked.

Decisions come from the dashboard's own numbers (rules + a score). **Laya** (the on-device decision
model) is a **second opinion**: it reads each bag's facts and says which reason it thinks matters
most, and whether an offer is the right move. Laya never overrides the numbers, and an opinion is
only shown when Laya is clearly surer than it is for healthy bags (see *Laya* below). It runs on this
PC only (model in `~/models/laya-int4/`); on Streamlit Cloud (no model) the page builds the same and
says Laya isn't available.

Code: data loading and the page payload in `push_planner.py`; every rule below is a pure function in
`lib/push_rules.py`; Laya's questions in `lib/push_laya.py`; the model itself in `lib/laya.py`.
Tests: `tests/test_push_planner.py`.

## Inputs (read only — nothing is written to Odoo or the sheet)

| Signal | From |
|---|---|
| Units sold per bag per day, last 28 days (ending yesterday), per market | Odoo POS — `self_made_combos.BAG_SALES_DAILY_*_SQL` (same product filters as the other pages) |
| Live stock per bag per market | `lib/stock.odoo_stock_by_product(market)` (shop stock, not warehouse) |
| Kenya stock and sales per bag **per shop** (last 14 days) | `lib/stock.odoo_stock_by_shop_code()` + POS lines by till (`push_planner.SHOP_SALES_SQL`, shops named via `lib/odoo_tabs.STOCK_CODE_TO_SHOP`) |
| Posts per bag this month / last week, posting yield, on-offer flag, dead-stock clearance | `POSTING (…).html` data block `PA` (`postYield.monthly/lastweek`, `deadClear.monthly`, and the same under `sinza` / `uganda`) |
| Bags on offer | the Posting rows' own `onOffer` flag per region (docs/posting-yields.md › "On offer"), plus `self_made_combos.html` `SMC.onOfferSources` for Kenya |
| New products | `lib/new_products_list.names()` |
| Price (full price, KES) | `bag_original_prices.json` (the monetary-implication table) |
| Category | `bag_tiers.csv` (the Bags on offer menu's editable table) — used for the peer comparison |
| Kenya month target | `current_performance.html` `PERF.totalTarget` |
| Month progress | `lib/report_month.live_month_window()` |

Bag names are matched like everywhere else (product-matching.md): Odoo variant names
("ANTITHEFT BLACK") roll up to the bag type ("ANTITHEFT") via `self_made_combos.bag_classifier()`,
the same resolver Bags on offer uses. **Gift bags are left out** (given away, never sold).

## Per bag × market: the facts (`push_rules.facts`, `add_peers`)

`stock`, `sold7` (last 7 days), `soldPrev7` (the 7 before), `sold28`, `perDay` (= sold28 ÷ 28),
`daysCover` = stock ÷ perDay (**none** when it sold nothing — it never runs out at that pace),
`momentum` (% change sold7 vs soldPrev7), `postsMonth`, `postsLastWeek`, `yieldPct` (posting yield),
`clearPct` (dead-stock clearance this month), `onOffer`, `isNew`, `price`, `category`,
`firstSoldDaysAgo`, and the **peer** figures — the median pace and price of the *other* bags in the
same category and market that sold at least one in the 28 days.

## Actions (one per bag × market, then ranked)

Tried in this order; the first that fits wins.

| Code | Action | When | Says (example) |
|---|---|---|---|
| `RESTOCK` | **Restock** | sells ≥ 2 a day and has < 7 days of stock in the market | "Sells 37.75 a day and has 6.5 days of stock left (244 units). Pause its posts until stock lands." |
| `STOP_POSTS` | **Stop posting** | ≥ 10 posts this month and 0 sold | "Posted 24 times this month and sold 0 — move those posts to bags that convert." |
| `PUT_ON_OFFER` | **Put on an offer** (Deal of the Week candidate) | not on offer, stock above the market's floor (Kenya 20, Sinza / Uganda 5 — `dead_stock_thresholds.txt`), ≥ 45 days of stock (or no sales), cleared < 30% | "144 in stock, sold 25 in 28 days — 161.3 days of stock. Try it as a Deal of the Week." |
| `POST_MORE` | **Post more** | posts work (yield ≥ 50%), stock above the floor and ≥ 14 days of it, posted less than the market's median | "Posts turn into sales (100% of expected) but it was posted only 19 times (typical: 30.5)…" |
| `MOVE_STOCK` | **Move stock** (Kenya, shop-level pass `push_rules.moves`) | a shop holds ≥ 5 and sold 0 in 14 days, while another shop sells it and has < 7 days left; sends two weeks at the receiving shop's pace | "Move 24 from Meru (sold 0 in 14 days) to Hilton (sells 2.7 a day, 6 left)." |
| `WATCH` | — | nothing clear | — |

**Score** = units at stake × price × urgency × confidence (`push_rules.score`). Urgency grows from 1
to 2 as the month's days run out. The page shows the **top 15** for the week (at most 5 of any one
action, so the list stays mixed) and a **top 8 per market** (at most 3 per action): Kenya's volumes are
~10× the others', so without it Sinza and Uganda never reach the overall list.

## Why it isn't moving — reasons, per market (`push_rules.reasons`)

A bag is **not moving** when it holds more than a quarter of its market's stock floor and has
cleared < 30% this month, or has > 45 days of stock, or sold nothing. For each, the rules flag
**every** reason that applies, in plain words with its numbers:

| Code | Label | Plain reason (example) |
|---|---|---|
| `NOT_POSTED` | Not posted | Nobody has seen it — 0 posts this month. |
| `POSTED_NOT_CONVERTING` | Posts not converting | Posted 20 times this month, but sales reached only 11.1% of what those posts should bring — the posts aren't selling it (price, photo or the bag itself). |
| `PRICE_ABOVE_PEERS` | Priced above similar bags | KES 3,600 vs KES 2,400 for the handbags that do sell in Kenya. (≥ 25% above.) |
| `WRONG_SHOPS` (Kenya) | Stock in the wrong shops | 79% of its shop stock (57 of 72) sits in shops that sold none of it in 14 days. |
| `OFFER_SHADOW` | Similar bags on offer | Similar handbags on offer (Cathy Handbag, Elyse) are taking the buyers. |
| `NEW_UNTESTED` | New — too early | New — first sold 5 days ago, too early to judge. |
| `MARKET_FIT` (Sinza / Uganda) | May not suit this market | Sells 5 a day in Kenya but 0 in 28 days in Uganda — may not suit this market. |
| `SLOWING` | Slowing down | Sold 3 this week vs 10 the week before (-70%). (Needs ≥ 5 the week before.) |
| `SLOW_SELLER` | Slow seller | *Only when nothing above fits:* sells under half the pace of similar bags here. |
| `OVERSTOCKED` | More stock than it sells | *Only when nothing above fits:* sells about as well as similar bags, but holds more than the market moves in a month. |

## Laya's second opinion (`lib/push_laya.py`)

Laya reads the bag's facts as short sentences (`state_text`) and is asked:

- **Main reason** — for a bag with 2+ reasons, a *choice* among those reasons only ("Which is the
  main reason this bag isn't selling?"); for a bag with one reason, a yes/no on it.
- **Offer check** — for each *Put on an offer* row, a yes/no ("This bag should go on a price offer
  next week to clear its stock.").

The **baseline** is the mean "yes" Laya gives the same question for 5 bags that are selling fine. A
yes/no counts as *agrees* when `yes ≥ max(0.5, baseline + 0.25)` and *disagrees* when
`yes ≤ baseline − 0.25`; a choice only counts as a pick when it clearly beats an even split. Unsure
answers aren't shown.

**Reliability gate (offers).** The offer opinion is shown only when Laya rates the stuck bags at
least 5 points higher than the healthy ones. On the first real run (1 Oct 2026) it did the
opposite — 28% yes for the stuck bags vs 61% for healthy ones — so its offer verdicts were hidden and
the page says so in plain words. Laya can't read the numbers; on the *reason* question it did better
(Amaya "priced above similar bags" 85%, Aurora "not posted" 86%, Bonita 94%).

Asking order (so the budget goes where it matters): the two baselines, the offer rows in the top 15,
the other offer rows, then not-moving bags by stock value.

## Did last week's calls work? (`push_rules.record_week`, `followup`)

Each run saves the week's top 15 to `push_planner_history.json` under the week's **Sunday**
(Sun–Sat weeks); re-running in the same week replaces that week, and 12 weeks are kept. The page then
shows the most recent previous week's calls: sold a day **since** that Sunday vs before.
Put on an offer / Post more: ✓ selling faster (≥ +15% and +0.1 a day) · = about the same · ✗ slower.
Restock: ✓ once stock is above what it was. Stop posting / Move stock: "check by hand" (sales alone
don't show it). `--dry-run` never writes the history.

## The page

1. **This week's top actions** — ranked cards; filters by market (All = the top 15, a market = its
   top 8) and by action.
2. **The month so far** — sold this month, day N of M, pace and the last-28-days pace; Kenya also
   shows the target and the bags a day still needed. Sinza and Uganda show pace only (no target in
   the dashboard).
3. **Why it isn't moving** — Kenya / Sinza / Uganda tabs: a chart of how many bags each reason
   covers, Laya's note, and the 40 stuck bags with the most stock value (stock, sold 28 d, a day,
   stock lasts, posts, reason chips, Laya's line).
4. **Move stock — Kenya shops** — up to 30 shop → shop moves.
5. **Last week's calls** — moved or not (the first week says the calls are saved).

Usual shared layers: page sidebar, chart switcher, V5 theme (dark page, light mode automatic).

## Laya model (`lib/laya.py`)

Python port of the Kotlin reference (laya-on-device skill): `tokenizers` reads `tokenizer.json`,
`onnxruntime` runs `model_int4.onnx`. Sequence `[CLS] <type> question: <ins> [SEP] ([MASK] opt)…
[SEP] state [SEP]`, 48 tokens per option, head budget 192, max 512; logits ÷ temperature (from
`rl_agent_config.json`, clamped 0.5–5) → softmax; yes/no = `[no, yes]`. Self-test on load: the
model-card example (billed twice → billing 0.986, churn yes 0.854); a model that fails it isn't
used. Answers are cached by question + facts in `laya_cache.json` (gitignored); each run makes at
most 80 new model calls (~1.8 s each here — the first run took ~2½ min, later runs reuse the cache).
`LAYA_DIR` overrides the folder; `--no-laya` skips it. Needs `onnxruntime` + `tokenizers` in the
dashboard's Python; without them (or the model) the page builds without Laya and says why.

## Regenerate

```
python push_planner.py              # build the page (~20–35 s once Laya's answers are cached)
python push_planner.py --dry-run    # print the summary, write nothing
python push_planner.py --no-laya    # skip Laya
python -m pytest tests/test_push_planner.py -q
python -m lib.laya --selftest
```
Runs after Posting and Self-made combos (it reads their pages), before Insights (`main.py`).
