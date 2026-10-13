# Push Planner — build checklist (Ralph loop)

Spec: [docs/push-planner.md](docs/push-planner.md). Work ONE unchecked item per iteration, top to
bottom. For each item: do it, verify it (the check written under it), tick it `[x]`, and add a
one-line note under "Log" (what was done + how it was checked). If an item can't pass its check,
leave it unchecked, write why in the Log, and fix it next iteration. Never tick an item whose
check didn't pass.

Python: `C:\ProgramData\anaconda3\python.exe`. graphify: `C:\Users\nate\AppData\Roaming\Python\Python313\Scripts\graphify.exe`
(`graphify query "<question>"` before reading unfamiliar code; `graphify update .` after code changes).
Don't change existing pages' behaviour. Never print or commit `.env`.

- [x] 1. Spec written (docs/push-planner.md) and this checklist.
- [x] 2. `lib/laya.py` — Python Laya: tokenizer + ONNX session + sequence/collate/decode, `ask_choice`,
      `ask_yes_no`, cache file, budget, self-test, `available()`.
      Check: `python -m lib.laya --selftest` prints billing ≈ 0.98 for the double-charged email and a
      sensible yes/no; a missing folder returns `available() == False` without raising.
- [x] 3. `push_planner.py` — data loading: per-day bag sales per market (28 days), stock per market,
      Kenya per-shop stock + 14-day sales, list price; rolled up to bag type.
      Check: run it with `--dry-run`; it prints counts per market (bags with stock, bags sold) that are
      non-zero for Kenya, and finishes in under ~2 minutes.
- [x] 4. Read the page data blocks: PA (posts, yield, on-offer, dead clearance per region), SMC (on-offer
      sets, deals), new products.
      Check: `--dry-run` prints how many bags got posts / on-offer flags per market (non-zero for Kenya).
- [x] 5. Facts per bag × market (pure function) + `tests/test_push_planner.py`.
      Check: `python -m pytest tests/test_push_planner.py -q` passes (cover: daysCover ∞ on 0 sales,
      momentum, peers).
- [x] 6. Actions + score (pure) + tests for each action rule.
      Check: pytest passes; `--dry-run` prints the top 15 with a plausible mix (not all one action).
- [x] 7. Reasons engine (pure) + tests for each reason code, plain-language text with numbers.
      Check: pytest passes; `--dry-run` prints reasons for 5 Kenya + 5 Sinza/Uganda non-moving bags.
- [x] 8. Laya second opinion wired in (choice for main reason, yes/no for offers, baseline rule, cache,
      budget) + test with a fake model.
      Check: pytest passes; a real run reports how many questions Laya answered and how long it took.
- [x] 9. Weekly history + "did last week's calls work" (pure compare) + test.
      Check: pytest passes; running twice doesn't duplicate a week.
- [x] 10. `push_planner.html` render layer (dark palette like the other pages, Chart.js, chart_switcher,
      page_sidebar, `<!-- PP_DATA_START/END -->`), generator injects the data.
      Check: real run writes the page; a headless Edge screenshot shows all 5 sections with data
      (no blank sections, no JS errors visible).
- [x] 11. Wire in: `dashboard_pages.json` (new page), `main.py` SCRIPTS order (after Posting, before
      Insights), `docs/README.md` menu table, `.gitignore` for `laya_cache.json`.
      Check: Streamlit AppTest opens `?page=Push Planner` with no exceptions.
- [x] 12. End-to-end real run + sanity review of the output (top actions make sense against the
      Bags on offer and Posting pages; numbers match).
      Check: write 3 spot-checks in the Log (bag, figure here, figure on the source page).
- [x] 13. `graphify update .`, docs final pass (spec matches what was built).
      Check: spec's tables match the code's action/reason codes.

## Log
- 1: spec + checklist written.
- 2: lib/laya.py (Python port: tokenizers + onnxruntime 1.30, cache, budget, self-test). `python -m lib.laya --selftest` → billing 0.986, churn yes 0.854 (= Kotlin reference); LAYA_DIR missing → available() False, no raise. Note: bag yes/no gave 0.520 (slow bag) vs 0.497 (selling-out bag) — Laya can't read the numbers, so the baseline rule in item 8 is essential.
- 3: push_planner.py load_data() — reuses smc.BAG_SALES_DAILY_*_SQL + bag_classifier, lib/stock per market + per shop, new till-level SQL for Kenya shops. `--dry-run`: Kenya 122 bags in stock (10,791 u; SMC page says 10,865) / 119 sold (11,610 u in 28 d), Sinza 66/51, Uganda 65/51; 18 Kenya shops matched stock↔sales; 18.3 s.
- 4: load_pages() — PA postYield (monthly + lastweek) + deadClear per region, on-offer = Posting rows' onOffer (+ SMC onOfferSources for Kenya), new products via lib/new_products_list. `--dry-run`: Kenya 54 bags posted this month / 34 last week / 27 on offer; Sinza 62/40/30; Uganda 69/45/7. Posting window = Sep (report month), SMC = October (no Oct offers yet). New products not resolving to a bag type: ['LAFEMME'].
- 5: lib/push_rules.facts() + add_peers() (pure), wired via push_planner.build_facts (categories from bag_tiers.csv). pytest 8 passed (cover None on 0 sales, pace/cover, window edges, momentum up/down/from-zero, peers same market+category, selling-only, self-excluded). Real dry-run: 275 rows, 250 with peers; REO TRAVEL Kenya 109 stock · 7.5/day · 14.5 d (Bags on offer page: 109 · 7.8/day · 14 d).
- 6: push_rules.action() (RESTOCK / STOP_POSTS / PUT_ON_OFFER / POST_MORE / WATCH, first fit wins), moves() (Kenya shop→shop), urgency/score/rank (≤5 per action in the top 15) + per-market top 8 (Kenya volumes ~10x drown Sinza/Uganda). pytest 18 passed. Dry-run top 15: 4 Restock (Antitheft 6.5 d, Man Bag 4.8 d…), 5 Put on offer (Zuri 161 d, Double Press 91 d…), 5 Post more, 1 Move (Prime Meru→Hilton). Uganda list shows Stop posting for Lola (24 posts, 0 sold).
- 7: push_rules.not_moving/context/reasons — 8 spec codes + 2 fallbacks so every stuck bag gets a reason (SLOW_SELLER, OVERSTOCKED; add to spec in item 13). pytest 31 passed. Dry-run: not moving Kenya 40 / Sinza 37 / Uganda 36; e.g. Kenya ZURI "posted 20 times, sales reached only 11.1%… · KES 3,600 vs 2,400 for handbags… · Cathy Handbag, Elyse on offer"; Sinza GYM BAG "KES 2,600 vs 1,200 for sport bags"; Uganda: MARKET_FIT ×12 ("sells N a day in Kenya but 0 here").
- 8: lib/push_laya.py (state_text, baseline from 5 healthy bags, verdict rule, main_reason choice/yes-no, offer_check, budget order) + push_planner.add_laya (--no-laya). pytest 36 passed (fake model incl. budget/None-safe). Real run: 80 model calls in ~142 s, cache works (2nd run +80 cached). FOUND: on offers Laya says yes 28% for stuck bags vs 61% for healthy → anti-signal; added a reliability gate (offer verdicts "hidden" + plain note unless stuck ≥ healthy + 0.05). Main reason: agrees/picks 14, disagrees 3, unsure 90 (e.g. AMAYA price-above 85%, AURORA not-posted 86%).
- 9: push_rules.week_start/record_week (replace same week, keep 12)/followup (sold/day since the pick's week vs before; RESTOCK judged on stock; STOP_POSTS/MOVE "check by hand") + push_planner.weekly() → push_planner_history.json (not written on --dry-run). pytest 40 passed. Ran the real generator twice: history = {"2026-09-27": 15} (one week, no duplicate).
- 10: push_planner.html render layer (dark, Chart.js + chart_switcher + page_sidebar, PP markers) + payload()/inject()/month_progress() (Kenya target from PERF.totalTarget). Real run writes the page in 22–32 s (Laya cached). Headless Edge screenshot: all 5 sections drawn with data — 15 action cards with market/action filters, 3 month cards, reasons chart + 40-row table with chips and Laya lines, 30 shop moves, first-week note. Fixed from the screenshot: GIFT BAG (530, never sold) showed as stuck → gift bags excluded.
- 11: dashboard_pages.json — Push Planner = order 10, Marketing section (after Shops Efficiency; Insights/Report/History → 11–13), icon trending_up; main.py SCRIPTS (after Shops Efficiency, before Insights) + refresh map; docs/README menu row 7b; .gitignore laya_cache.json (git check-ignore confirms). Streamlit AppTest ?page=Push Planner (DASH_NO_AUTOREFRESH=1): 0 exceptions, 0 warnings, title + purpose rendered.
- 12: spot-checks (planner page vs source):
  · REO TRAVEL Kenya — planner stock 109, 7.5/day, 14.5 d · Bags on offer page 109, 7.8/day, 14 d (28-day window vs the page's own window).
  · ANTITHEFT Kenya — planner 64 posts, yield 93.4% · Posting page 64 posts, 93.4% (3 colour rows) — exact.
  · ZURI Kenya — planner stock 144, sold 25, 20 posts · Bags on offer 144 / 25 · Posting dead-stock rows count 15 posts (yield rows count 20; the planner uses the yield rows, as its yield % does).
  · PRIME move Meru→Hilton 24, Hilton has 6 · Odoo per-shop stock now: Meru 24, Hilton 6 — exact.
  · ANTITHEFT Sinza — planner stock 4, 2.11/day · Posting page Sinza stockNow 4, 61 sold in Sep — consistent.
  Top actions read sensibly against Bags on offer (Zuri/Double Press/Nala/Imani/Cess are its slow off-offer bags; Antitheft/Man Bag/Mini Maya are its fastest on-offer bags).
- 13: docs/push-planner.md rewritten to match the build (inputs incl. prices/categories/target sources, gift bags excluded, action table with codes + order, top 15 + per-market top 8, 10 reason codes incl. SLOW_SELLER/OVERSTOCKED, Laya baseline + reliability gate + first-run findings, weekly rules, page, commands). Check script: spec action codes == push_rules.ACTIONS, reason codes == REASONS, labels == REASON_LABEL (all True). graphify update . done; graphify query finds push_laya.second_opinion / push_rules.reasons / lib/laya. pytest 40 passed.
