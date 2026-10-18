# Graph Report - Marketing_dashboard  (2026-10-18)

## Corpus Check
- 200 files · ~896,612 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: .csv 10, (none) 2, .toml 1)

## Summary
- 2284 nodes · 4411 edges · 175 communities (140 shown, 35 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 160 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bb8a492c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- current_performance.py
- laya.py
- lib/receipt_combos.py
- oos_chip.js
- chart_switcher.js
- graw(block, key) function (bare numeric getter)
- Kitengela Rejects tracker (timed offer)
- generators/self_made_combos.py
- name_match.py
- v5_theme.js
- scripts/test_receipt_combos.py
- bare_minimum setting (weekly target floor)
- signals
- _reveal_page
- month_extras.py
- type_fn
- publish.py
- data
- build_payload
- shop_launch.py
- shop_corporate.py
- Bags on offer vs not on offer
- bags_on_offer.py
- Self-made combos vs running combos (doc)
- shop_stock_levels.py
- signals
- shops_dispatch.py
- Dashboard Menu Docs (spec index)
- followup
- _enrich_deals
- fetch
- insights.html
- streamlit_app.py
- moves
- monthly_report.py
- _combo_norm_option
- chronos_train.py
- stock.py
- build_payload
- Shops Efficiency Tracking spec doc
- Product (bag) targets
- push_rules.py
- datetime
- page_sidebar.js
- lib/db.py
- Combos & Power Deals by Shop panel (#combo-shop)
- self_made_combos_bundle/offer_data.py
- Self-made combos bundle Python dependencies (requirements.txt)
- CLAUDE.md
- history.py (read months back)
- Self-made combos vs Running combos portable bundle README
- start_server
- odoo_tabs.py
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- algorithmic-art skill
- dataviz-charts skill
- bag_classifier
- compute_period
- _enrich_deals
- High-End Visual Design skill
- self_made_combos_bundle/self_made_combos.py
- _combo_button_usage
- oos_callbacks.py
- daydream skill (Vault Daydream)
- paths.py
- OOS call-back progress (Ralph loop log)
- timed_offers.py (generator)
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- month_window
- self_made_combos_bundle/lib/report_month.py
- marketing_dashboard.sql
- product_performance.py
- Month-End Routine
- shop_birthdays.py
- lib/offer_data.py
- _fetch_sinza_monthly
- push_planner.py
- history.py
- theme.py
- push_laya.py
- _read_offers
- facts
- os
- lib/report_month.py
- Chart type switcher (every chart, every menu)
- test_push_planner.py
- new_products.py
- test_stockout_demand.py
- Out-of-stock demand — people, not requests
- Denri Africa Dashboard Design System (skill)
- num
- shop_requests.py
- safe_int
- run_query
- offer_picking.py
- test_share_targets.py
- _combo_button_usage
- Bag Signals — quant view of each bag (posting · stock · selling)
- timed_offers.py
- current_performance.html
- attach
- self_made_combos.py generator (build_payload + SQL + injection)
- posting_yields.py
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- _bg_jobs
- forward_projections.py
- Ralph task — only three sheet tabs left
- design-taste-frontend (anti-slop frontend skill)
- Bag targets October 2026_3acbad00.md
- get_rows
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- fetch_posting_data
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- load_pages
- shop-birthdays.md
- What the page shows
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- Monthly Report (doc)
- POST_DATA data block (Posting)
- _dead_stock_region
- read_block(file, start, end) function
- New Products Analytics (doc)
- Offer Picking (doc)
- ambiguous_python_import_17686b6faac5
- contextlib
- write_bags_offer_source
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- excluded_products
- Product / name matching (doc)
- _alignment_region
- custom_range.py
- build
- family
- build
- scripts/receipt_combos.py
- _bag_stock
- json
- _bags_not_on_offer
- Bag signals — quant finance applied to product sales
- _bag_tiers
- _seasonality
- Combos from receipts — running vs self-made
- Sales-share targets per product
- Semantic color rules (green=good, amber=risk, red=critical, cyan=info)
- _read_bom_costs
- load_catalog
- _bg_rebuild
- offer_flags
- _month_archived

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 62 edges
2. `fetch()` - 39 edges
3. `fetch_posting_data()` - 38 edges
4. `build_payload()` - 30 edges
5. `get_gspread_client()` - 29 edges
6. `check_connection()` - 28 edges
7. `data()` - 28 edges
8. `build_payload()` - 24 edges
9. `build_offer()` - 22 edges
10. `F()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `Inputs (read only — nothing is written to Odoo or the sheet)` --references--> `bag_classifier()`  [INFERRED]
  docs/push-planner.md → generators/self_made_combos.py
- `Why it isn't moving — reasons, per market (`push_rules.reasons`)` --references--> `reasons()`  [INFERRED]
  docs/push-planner.md → lib/push_rules.py
- `Laya's second opinion (`lib/push_laya.py`)` --references--> `state_text()`  [INFERRED]
  docs/push-planner.md → lib/push_laya.py
- `Buckets` --references--> `bag_classifier()`  [INFERRED]
  docs/bags-on-offer.md → generators/self_made_combos.py
- `The split — by each bag's share of recent sales` --references--> `bag_classifier()`  [INFERRED]
  docs/product-targets.md → generators/self_made_combos.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Self-made combos bundle: generator, Sheets auth, DB access, and dependency manifest working together to build the combos page** — export_self_made_combos_bundle_self_made_combos_py, export_self_made_combos_bundle_offer_data_py, export_self_made_combos_bundle_google_auth_py, export_self_made_combos_bundle_lib_db_py, export_self_made_combos_bundle_requirements [EXTRACTED 0.90]
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]

## Communities (175 total, 35 thin omitted)

### Community 0 - "current_performance.py"
Cohesion: 0.12
Nodes (10): fetch_monthly_target(), last_week_from_db(), current_performance.py…, Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary() (+2 more)

### Community 1 - "laya.py"
Cohesion: 0.09
Nodes (26): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket() (+18 more)

### Community 2 - "lib/receipt_combos.py"
Cohesion: 0.08
Nodes (44): What the page shows (per period), _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, lib — shared data-access for the marketing dashboard (Postgres migration).…, bag_key(), classify(), _fits(), _groups() (+36 more)

### Community 3 - "oos_chip.js"
Cohesion: 0.08
Nodes (38): attach(), close(), esc(), form(), go(), iso(), mountPanel(), open() (+30 more)

### Community 4 - "chart_switcher.js"
Cohesion: 0.12
Nodes (35): alpha(), apply(), attach(), axisOpts(), build(), changeTxt(), Chart(), clone() (+27 more)

### Community 6 - "Kitengela Rejects tracker (timed offer)"
Cohesion: 0.07
Nodes (28): bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source), Offline fallback pattern (mirror sheet data to local JSON), Reject Sale (doc: reject_sales.py -> reject_sales.html, RJ), reject_sales_export.csv (fallback export) (+20 more)

### Community 7 - "generators/self_made_combos.py"
Cohesion: 0.11
Nodes (20): _bag_sales_daily_sql(), _bag_sales_sql(), _bags_not_on_offer(), fetch(), fmt(), inject(), _load_shop_regions(), main() (+12 more)

### Community 8 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "scripts/test_receipt_combos.py"
Cohesion: 0.32
Nodes (15): classify(), lines: [{receipt, d, product, qty, amount}] → per-market summary: {running:…, infer(), L(), Tests for receipt_combos.py + name_match.py — python -m pytest scripts -q, test_alternatives_and_singles(), test_bulk_receipts_are_not_combos(), test_four_bags_at_two_prices_are_two_combos() (+7 more)

### Community 12 - "signals"
Cohesion: 0.17
Nodes (16): action(), _mean(), _phi(), posting_beta(), The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json…, _sd() (+8 more)

### Community 13 - "_reveal_page"
Cohesion: 0.50
Nodes (4): Run script-only HTML in an invisible frame (same origin, so it can reach…, Fade the page area back in on a page that has no dashboard frame (password…, _reveal_page(), _run_js()

### Community 14 - "month_extras.py"
Cohesion: 0.25
Nodes (13): _bags_on_offer(), _block(), build_extras(), _deals(), _pick(), _posting(), _posting_block(), region() (+5 more)

### Community 15 - "type_fn"
Cohesion: 0.19
Nodes (14): build(), ({TYPE: Kenya shop on-hand}, {TYPE: Sinza + Uganda on-hand}) — live Odoo., The NP.runway payload: {days, bags: [{name, created, category, stockKe,…, Product name → bag type (see the module docstring)., [{name, created, category}] newest first — the runway bag types as of today; []…, {TYPE: bags sold} for the given runway types over [start, end] — POS bags,…, runway_bags(), sold_by_type() (+6 more)

### Community 16 - "publish.py"
Cohesion: 0.21
Nodes (14): argparse, fnmatch, py_compile, changed_files(), git(), group(), is_secret(), main() (+6 more)

### Community 17 - "data"
Cohesion: 0.25
Nodes (9): _archived_source(), bags_offer_source_<YYYY-MM>.json — that month's archived on-offer list, or None., _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, _load_combos_by_shop(), _from_file(), _nonempty(), Per-shop combo / power-deal view for the panel — built **live from Odoo** via… (+1 more)

### Community 18 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 19 - "shop_launch.py"
Cohesion: 0.20
Nodes (14): build(), _cfg(), first_sale(), kenya_posts(), load_workplan(), make_matcher(), match(), _parse_workplan() (+6 more)

### Community 20 - "shop_corporate.py"
Cohesion: 0.15
Nodes (24): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), _acronym(), build(), _maybe(), owns(), corporate_team_receipts(), _d() (+16 more)

### Community 21 - "Bags on offer vs not on offer"
Cohesion: 0.18
Nodes (11): Bags on offer vs not on offer, Buckets, Corporate-lead till orders, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Regenerate, Shop birthdays (+3 more)

### Community 22 - "bags_on_offer.py"
Cohesion: 0.27
Nodes (10): _base_windows(), _custom_range(), fmt(), inject(), main(), bags_on_offer.py…, (from, to) dates from boo_custom_range.json — the Custom period — or None., Write (or with a=None, delete) the Custom period's dates. (+2 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.18
Nodes (13): Bags not on offer per market (Kenya/Sinza/Uganda), Combo button usage / rung vs pot. (till check), Self-made combos vs running combos (doc), DoW mirror shops (DOW_MIRROR), Monetary implication panel (bundling discount), Rank chip (follows active Sort filter), Running-combo classification by bag composition (slot-aware sheet match), Standalone SQL (self_made_vs_running_combos.sql) (+5 more)

### Community 24 - "shop_stock_levels.py"
Cohesion: 0.15
Nodes (23): build(), dispatch_shop(), fit(), grand_total(), leads(), needs(), new_bags(), _next_month() (+15 more)

### Community 25 - "signals"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

### Community 26 - "shops_dispatch.py"
Cohesion: 0.21
Nodes (14): build_period(), distributed_in(), main(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only., Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).… (+6 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.18
Nodes (14): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes) (+6 more)

### Community 28 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 29 - "_enrich_deals"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "fetch"
Cohesion: 0.10
Nodes (27): _as_date(), _build_period(), fetch(), cat_tier(), classify(), classify_for(), combo_slots(), make_classifier() (+19 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.10
Nodes (11): SCRIPT_TIMEOUT = 600s config, hashlib, html, streamlit, _load_secrets_into_env(), _month_end_running(), streamlit_app.py — Denri Marketing Dashboard on Streamlit. Serves the existing…, A Streamlit secret by name — top level, or pasted by mistake under a [table]… (+3 more)

### Community 33 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.16
Nodes (8): _cause(), esc(), fmt(), ladder_strip(), pct(), monthly_report.py…, _smc_srow(), _stock_rows()

### Community 35 - "_combo_norm_option"
Cohesion: 0.28
Nodes (8): _combo_norm_option(), _combo_sheet_slots(), combos_by_shop(), _norm(), _tokmatch(), Per-shop view for Shops Efficiency, keyed by shop-location label (e.g.…, One combo slot-option → its distinctive bag token(s), colours/category words…, Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ].

### Community 36 - "chronos_train.py"
Cohesion: 0.13
Nodes (26): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+18 more)

### Community 37 - "stock.py"
Cohesion: 0.20
Nodes (15): odoo_stock_levels(), Live per-shop Odoo on-hand in the SAME shape parse_sheet(STOCK_LEVELS) returns:…, _codes_for(), _inlist(), odoo_stock_at_location(), odoo_stock_by_product(), odoo_stock_by_shop_code(), _ok() (+7 more)

### Community 38 - "build_payload"
Cohesion: 0.12
Nodes (18): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+10 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "Product (bag) targets"
Cohesion: 0.29
Nodes (7): Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 41 - "push_rules.py"
Cohesion: 0.13
Nodes (17): action(), _cover_txt(), _kind(), _n(), not_moving(), posting_median(), rank(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).… (+9 more)

### Community 42 - "datetime"
Cohesion: 0.09
Nodes (29): calendar, collections, csv, datetime, lib — shared data-access for the marketing dashboard (Postgres migration).…, Reject Sale pricing (Kitengela) → reject_sales.html (payload `RJ`). A…, lib/bag_quant.py — quant signals per bag: drift, volatility, Sharpe-style…, lib/colours.py — colour FAMILY of a product (Brown, Black, Red, Beige, Grey,… (+21 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "lib/db.py"
Cohesion: 0.09
Nodes (31): dotenv, check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME… (+23 more)

### Community 45 - "Combos & Power Deals by Shop panel (#combo-shop)"
Cohesion: 0.25
Nodes (8): Combos & Power Deals by Shop panel (#combo-shop), compute_period() function (emits pushDetail per period), Deal of the Week — Tier 2 (latest 2-week window) shop-scoped view, DenriTableFilter reusable filter bar component, DOW_MIRROR expansion (Starmall to Hazina/Hilton/KTDA), odoo_stock_levels() function, Push via filter (None / power deal / deal of the week tag), shops_efficiency.html page

### Community 46 - "self_made_combos_bundle/offer_data.py"
Cohesion: 0.17
Nodes (17): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), cell(), find_row(), find_row_any(), process_table() (+9 more)

### Community 47 - "Self-made combos bundle Python dependencies (requirements.txt)"
Cohesion: 0.15
Nodes (14): google_auth.py (Sheets auth), lib/db.py (Supabase session pooler DB access), lib/db.run_query (shared connection reuse per subprocess), offer_data.build (batched Sheets range fetch), Refresh Performance (shared connection reuse, batched Sheets reads), Supabase session pooler host rule (direct host is IPv6-only), google_auth.py (service account or OAuth desktop), gspread>=6.0 dependency (Google Sheets access) (+6 more)

### Community 49 - "history.py (read months back)"
Cohesion: 0.33
Nodes (7): denri_mkt_* Supabase tables, history.html page, history.py (read months back), month_end.py (freezes a month), push_to_supabase.py (write months), Resilience fallback: history.py leaves existing page data untouched if Supabase unreachable, supabase_migration.py (schema)

### Community 50 - "Self-made combos vs Running combos portable bundle README"
Cohesion: 0.25
Nodes (8): shop-regions.md (editable Shop to Region table), Composition-based classification rationale (Running vs Self-made), _matches_sheet / _build_sheet_slots slot-aware matching functions, Self-made combos vs Running combos portable bundle README, Returns netting rationale (qty <> 0, returns subtract), docs/self-made-combos.md full spec for the menu, docs/shop-regions.md editable shop to region map, sql/self_made_vs_running_combos.sql (standalone pure-SQL classification)

### Community 51 - "start_server"
Cohesion: 0.18
Nodes (16): _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, _run_one(), run_scripts(), start_server(), copyfile(), do_GET() (+8 more)

### Community 52 - "odoo_tabs.py"
Cohesion: 0.14
Nodes (22): _aliases(), base_name(), build_rows(), _Deriver, dispatch_by_product_shop(), _flag_cells(), _fmt(), norm() (+14 more)

### Community 53 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.17
Nodes (12): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+4 more)

### Community 56 - "bag_classifier"
Cohesion: 0.13
Nodes (18): _add_noffer_posts(), per_bag(), _add_oos(), _apply_receipt_offers(), bag_classifier(), infer(), _norm(), _norm_combo() (+10 more)

### Community 57 - "compute_period"
Cohesion: 0.12
Nodes (11): apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _metric(), pct(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period. (+3 more)

### Community 58 - "_enrich_deals"
Cohesion: 0.16
Nodes (9): _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,… (+1 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "self_made_combos_bundle/self_made_combos.py"
Cohesion: 0.16
Nodes (13): get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, fetch(), fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py… (+5 more)

### Community 61 - "_combo_button_usage"
Cohesion: 0.15
Nodes (12): _build_sheet_slots(), _combo_button_usage(), _combo_norm_option(), _combo_odoo_slots(), _combo_sheet_slots(), _matches_sheet(), One combo slot-option → its distinctive bag token(s), colours/category words…, Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+4 more)

### Community 62 - "oos_callbacks.py"
Cohesion: 0.06
Nodes (56): Out of stock — call back, fixture, bag(), aggregate(), flat(), split(), attach_stock(), in_stock() (+48 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "paths.py"
Cohesion: 0.07
Nodes (29): apply_walkins(), http_server, generator(), lib/paths.py — where every kind of file lives. Use these instead of building…, sql(), ensure_firewall_rule(), free_port(), get_lan_ip() (+21 more)

### Community 65 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.20
Nodes (9): _local_deal_rows(), Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Blocker counter, Deals from posters (RALPH_DEALS.md) — 2026-10-04, Final summary, Log, OOS call-back progress (Ralph loop log), Sheets cut to three tabs (RALPH_SHEETS.md) — 2026-10-04 (+1 more)

### Community 66 - "timed_offers.py (generator)"
Cohesion: 0.09
Nodes (22): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+14 more)

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.20
Nodes (9): Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, Page, Production — shop requests vs approved list (18 Oct 2026), Shop requests — requested vs received (18 Oct 2026), Shop Stock Levels — min / max per shop, stocks report and next-month preparedness (+1 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "month_window"
Cohesion: 0.67
Nodes (3): month_window(), date, First → last calendar day of the LIVE month (today's month; see…

### Community 71 - "self_made_combos_bundle/lib/report_month.py"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "product_performance.py"
Cohesion: 0.05
Nodes (56): build(), categories(), _d(), explain(), _fmt_d(), _load_json(), load_lines(), load_posts() (+48 more)

### Community 74 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "lib/offer_data.py"
Cohesion: 0.20
Nodes (12): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), offer_data.py ─────────────────────────────────────────────────────────────────… (+4 more)

### Community 77 - "_fetch_sinza_monthly"
Cohesion: 0.18
Nodes (14): _analyze_region(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), MONTHLY_SALES: colour=A(0), product_name=B(1), MONTHLY_MARKETING_POST: colour=A(0), product_name=C(2), STOCK_LEVELS: colour=A(0), product_name=C(2) (+6 more)

### Community 78 - "push_planner.py"
Cohesion: 0.12
Nodes (24): build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), load_data(), main() (+16 more)

### Community 79 - "history.py"
Cohesion: 0.13
Nodes (20): fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers…, Like _num, but leaves booleans alone and renders dates as ISO strings — the… (+12 more)

### Community 80 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), lib/theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 81 - "push_laya.py"
Cohesion: 0.14
Nodes (19): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+11 more)

### Community 82 - "_read_offers"
Cohesion: 0.20
Nodes (10): Offer type summary (matrix), _apply_alias(), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, Apply bag aliases, longest key first (so 'STANDARD TRAVEL' wins over…, _read_offers(), _read_offers_cache(), _category_of() (+2 more)

### Community 83 - "facts"
Cohesion: 0.15
Nodes (18): Per bag × market: the facts (`push_rules.facts`, `add_peers`), add_peers(), _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), ISO date n days before END (0 = END). (+10 more)

### Community 84 - "os"
Cohesion: 0.08
Nodes (26): build(), _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), load(), load_dispatch() (+18 more)

### Community 85 - "lib/report_month.py"
Cohesion: 0.13
Nodes (23): _db_count(), monthly_from_db(), Reporting month's subset count (e.g. rejectBags, giftBags) from…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,…, anchor(), is_pinned(), live_anchor(), live_month_key() (+15 more)

### Community 86 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.25
Nodes (7): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does, Current Performance (doc)

### Community 87 - "test_push_planner.py"
Cohesion: 0.16
Nodes (25): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m…, A facts row with sensible defaults, overridden by kw. (+17 more)

### Community 88 - "new_products.py"
Cohesion: 0.05
Nodes (49): _new_products(), This month's new products: data/new_products.txt (lib/new_products_list) — the…, _base_colour(), fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key() (+41 more)

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.14
Nodes (10): Agent skills — retail analytics, Test a skill, Use in another project, Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods (+2 more)

### Community 91 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.17
Nodes (13): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), Signature Element — Flowing Border (achievement cards), high-end-visual-design (related skill), KPI Tile component (+5 more)

### Community 92 - "num"
Cohesion: 0.20
Nodes (11): _garr_line(), gnum(), num(), _offers(), _parse_offers(), _units(), This month's timed-offer campaigns, flattened for storage. The live TO payload…, Greedy single-line array extractor — handles nested [[...],[...]] arrays. (+3 more)

### Community 93 - "shop_requests.py"
Cohesion: 0.23
Nodes (12): lib, _d(), _f(), _offer_label(), _pct(), production(), lib/shop_requests.py — what each shop REQUESTED in the Odoo dispatch module…, Per shop: requests in [start, end] — totals, the three checks, effectiveness %,… (+4 more)

### Community 94 - "safe_int"
Cohesion: 0.16
Nodes (22): _bag_level_bags(), _build_no_convert(), _fetch_monthly_kenya(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int() (+14 more)

### Community 95 - "run_query"
Cohesion: 0.20
Nodes (11): corporate_clients_from_db(), corporate_target_from_db(), _months(), A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],…, Current month's corporate activity per client (quoted · invoiced · paid · sold)…, This month's Odoo corporate target {bags, kes} (sales_pos_target, scope…, _txt() (+3 more)

### Community 96 - "offer_picking.py"
Cohesion: 0.19
Nodes (13): _build_catalog(), _is_full_price(), _next_month(), offer_picking.py…, {BAG (upper): official full price} from bag_original_prices.json (fallback)., Save a local, human-editable copy of the offers prices to OFFERS_CACHE., Resolve any bag wording → (canonical BOM bag type, cost or None, in_bom).…, Every bag the user can pick for a slot, with two prices from the offers sheet:… (+5 more)

### Community 97 - "test_share_targets.py"
Cohesion: 0.22
Nodes (11): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+3 more)

### Community 98 - "_combo_button_usage"
Cohesion: 0.14
Nodes (11): _combo_button_usage(), _matches_sheet(), _opt_close(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Same slot count and every slot overlaps under SOME pairing (any order: the…, The sheet label this Odoo combo maps to, or None if it isn't on the sheet.…, _slots_fit() (+3 more)

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "timed_offers.py"
Cohesion: 0.06
Nodes (54): corporate_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, _corporate_bags(), Corporate bags sold in the given month, live from Odoo invoices. Returns 0 when…, _bags_from_file(), _bucket(), build_offer(), _derive_month() (+46 more)

### Community 101 - "current_performance.html"
Cohesion: 0.50
Nodes (4): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance)

### Community 102 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 103 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.29
Nodes (7): lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, lib/report_month.py (which month are we reporting?), self_made_combos.html static page (reads const SMC), self_made_combos.py generator (build_payload + SQL + injection)

### Community 104 - "posting_yields.py"
Cohesion: 0.12
Nodes (16): count_complete_weeks_in_month(), _fold_bag_level(), load_dead_thresholds(), _mkt_perfect_week_index(), _mkt_week_label(), _offer_bagtypes_by_region(), posting_yields.py…, Bags whose posts marketing logs only per BAG (the posting sheet's TOTAL row,… (+8 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "_bg_jobs"
Cohesion: 0.25
Nodes (8): cache_resource, fragment, _bg_done_msg(), _bg_jobs(), _bg_watch(), _fmt_secs(), Background rebuilds shared by every session: label → job (see _bg_rebuild)., The refresh_msg for a finished background rebuild (None: the job vanished).

### Community 107 - "forward_projections.py"
Cohesion: 0.11
Nodes (15): fetch_sheet_data(), _live_bags(), odoo_weekly_breakdown(), _perfect_week_index(), forward_projections.py…, Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, update_weekly_history() (+7 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "design-taste-frontend (anti-slop frontend skill)"
Cohesion: 0.18
Nodes (12): design-taste-frontend (related skill), design-taste-frontend (anti-slop frontend skill), Brief-First Process (8-step design workflow), Hard Bans (typography, color, layout, code, content clichés), Pre-Flight Checklist (90+ items), Redesign Protocol (upgrading existing UI), Three Dials — DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, Three AI-generated design clusters (calibration reference) (+4 more)

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "get_rows"
Cohesion: 0.18
Nodes (12): _build(), default_window(), get_rows(), last_complete_week(), _ok(), date, The most recent COMPLETE Sun–Sat week before `ref` (today) — what the sheet's…, {NORM(product): {SHOP: on-hand}} live, Kenya shops + Sinza (DAR) + Uganda (UG). (+4 more)

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 114 - "fetch_posting_data"
Cohesion: 0.15
Nodes (11): _bt_on_offer(), _dead_clear(), fetch_posting_data(), _clear(), _yield(), _post_yield(), Marketing & Sales Alignment — posting yield, measured the way marketing…, {catalogue name: net units moved INTO the region's shops on/after `since`} from… (+3 more)

### Community 121 - "load_pages"
Cohesion: 0.29
Nodes (7): read_block(), read_block(), _read_timed_offers(), load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, html()

### Community 122 - "shop-birthdays.md"
Cohesion: 0.22
Nodes (7): Shop birthdays, Shop → opening date, Where it shows, Per-shop combo-button chips (red when < half best-in-region), self_made_combos.py, Shops & Regions (doc — source of truth), Shop -> Region table

### Community 123 - "What the page shows"
Cohesion: 0.20
Nodes (9): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Bulk orders, Data, Product Performance — which bags, categories and colours carry the sales, and why (+1 more)

### Community 126 - "Monthly Report (doc)"
Cohesion: 0.22
Nodes (9): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+1 more)

### Community 128 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 130 - "New Products Analytics (doc)"
Cohesion: 0.25
Nodes (7): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), Weekly Performance chart (Week 1 to latest), Net returns rule (qty <> 0, subtract refunds), Returns netting rule (qty <> 0), Python dependencies list (requirements.txt), Postgres source-of-truth migration (off Google Sheets, weekly first)

### Community 131 - "Offer Picking (doc)"
Cohesion: 0.29
Nodes (8): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES)

### Community 138 - "write_bags_offer_source"
Cohesion: 0.22
Nodes (9): Counted by how it was sold, _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…, dow_tier_weeks(), Kenya on-offer bag set (tagged by offer) + the not-on-offer list, for…, Sun-Sat week numbers a Deal-of-the-Week tier runs in: Tier 1 = Wk 1–2, Tier 2 =… (+1 more)

### Community 145 - "Shop Launch"
Cohesion: 0.29
Nodes (6): Config, Launch day, Marketing posts, Sales, Shop Launch, What the page shows

### Community 153 - "excluded_products"
Cohesion: 0.08
Nodes (30): bag_posts(), tally(), load(), (daily, total, stock, launch, start, end) for Kenya from Odoo; daily per bag…, {BAG: (posts this month, posts last week)} — Kenya posts (col E) from the two…, allocate(), available_days(), bag_key_fn() (+22 more)

### Community 154 - "Product / name matching (doc)"
Cohesion: 0.33
Nodes (7): match_odoo_bags [S_0] internal-reference prefix fix, Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix), Normalisation rules (upper-case, strip ref prefix, exclude combos/non-sellable stock), Deal enrichment & name matching (_enrich_deals / _match)

### Community 155 - "_alignment_region"
Cohesion: 0.36
Nodes (8): _alignment_region(), _for(), _onoff(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 156 - "custom_range.py"
Cohesion: 0.19
Nodes (14): block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each…, (from, to) dates for the page's Custom period, or None. Swapped if reversed;… (+6 more)

### Community 157 - "build"
Cohesion: 0.28
Nodes (9): _alt_cost(), build(), _combo_cost(), _combo_slots(), Parse `const SMC = {…}` out of self_made_combos.html (no DB round-trip)., One combo alternative (e.g. 'Amaya Handbag') → its BOM production cost., Combo name → list of slots, each a list of alternative strings., Production cost = Σ over slots of the average matched-alternative cost. Same-… (+1 more)

### Community 158 - "family"
Cohesion: 0.40
Nodes (6): ({BAG: units}, {BAG: {colour: units}}) at CBD/Stock., warehouse_stock(), family(), _load(), _norm(), Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…

### Community 159 - "build"
Cohesion: 0.22
Nodes (8): _assign_price(), build(), reject_stock.csv → {BAG (upper): {units, colours:{COLOUR: units}}}., (price, flag) from BOM cost — two tiers. flag ∈ {'', 'thin', 'below', 'nobom'}., Write an Excel (xlsx, or CSV fallback) of EVERYTHING on the pricing board —…, _read_overrides(), _read_stock(), _write_export()

### Community 160 - "scripts/receipt_combos.py"
Cohesion: 0.29
Nodes (6): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…, itertools

### Community 161 - "_bag_stock"
Cohesion: 0.40
Nodes (5): _bag_stock(), _combo_bags(), _norm_bag(), Space/punctuation-insensitive key so 'MINIZURI' matches 'MINI ZURI'., Component bags of an offer, each with its stock, sorted most-stock first.

### Community 162 - "json"
Cohesion: 0.13
Nodes (10): One-off: restore August's Offer Type figures into monthly_report_history.json…, card(), esc(), fmt(), generate_insights.py…, region_card(), main(), _query_ready() (+2 more)

### Community 163 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 164 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 165 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

### Community 166 - "_seasonality"
Cohesion: 0.40
Nodes (6): Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), _combo_odoo_slots(), Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…

### Community 167 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 168 - "Sales-share targets per product"
Cohesion: 0.40
Nodes (4): Deliver, Sales-share targets per product, Steps, Tests

### Community 169 - "Semantic color rules (green=good, amber=risk, red=critical, cyan=info)"
Cohesion: 0.50
Nodes (4): Design Tokens (colors, typography, spacing), Semantic color rules (green=good, amber=risk, red=critical, cyan=info), Analytics Dashboard specific rules (VISUAL_DENSITY: dense), Region colour palette (reference for Executive Dashboard)

### Community 170 - "_read_bom_costs"
Cohesion: 0.50
Nodes (4): {BAG TYPE (upper): production cost} from bom_costs.json — the local copy of the…, _read_bom_costs(), _bom_costs(), {BAG (upper): cost} from bom_costs.json (via offer_picking._read_bom_costs).…

### Community 171 - "load_catalog"
Cohesion: 0.50
Nodes (4): catalog_rows(), load_catalog(), [{colour, category, name, bag}] in sheet order, from product_catalog.csv., [header] + [[COLOUR, CATEGORY, PRODUCT NAME, BAG TYPE], …] — the label columns…

### Community 172 - "_bg_rebuild"
Cohesion: 0.33
Nodes (7): _bg_rebuild(), work(), Seconds the last good `kind` rebuild of `lbl` took (any kind as a fallback),…, Rebuild `lbl` in the background. kind: "auto" (skipped if a rebuild was tried…, _rebuild_secs(), run_scripts(), _save_rebuild_secs()

### Community 173 - "offer_flags"
Cohesion: 0.50
Nodes (4): offer_flags(), prime_offer_flags(), Seed offer_flags() from MONTHLY_TARGET rows the caller already read (saves a…, {BAG TYPE: (kenya, sinza, uganda) on-offer bools} from MONTHLY_TARGET cols…

### Community 178 - "_month_archived"
Cohesion: 0.67
Nodes (3): cache_data, _month_archived(), True when `key` is in Supabase (falls back to monthly_report_history.json). If…

## Knowledge Gaps
- **200 isolated node(s):** `The page`, `Laya model (`lib/laya.py`)`, `Shop birthdays`, `Regenerate`, `Log` (+195 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 938 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `bag_classifier()` connect `bag_classifier` to `generators/self_made_combos.py`, `Product (bag) targets`, `write_bags_offer_source`, `push_planner.py`, `data`, `Push Planner (`push_planner.py` → `push_planner.html`, `PP`)`, `Bags on offer vs not on offer`, `fetch`, `oos_callbacks.py`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `Bags on offer vs not on offer` connect `Bags on offer vs not on offer` to `lib/receipt_combos.py`, `write_bags_offer_source`, `_read_offers`, `shop-birthdays.md`, `oos_callbacks.py`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `run_query()` connect `run_query` to `current_performance.py`, `lib/receipt_combos.py`, `generators/self_made_combos.py`, `type_fn`, `build_payload`, `shop_launch.py`, `shop_corporate.py`, `shop_stock_levels.py`, `excluded_products`, `_enrich_deals`, `fetch`, `json`, `_bags_not_on_offer`, `chronos_train.py`, `stock.py`, `_seasonality`, `build_payload`, `datetime`, `lib/db.py`, `bag_classifier`, `_enrich_deals`, `_combo_button_usage`, `oos_callbacks.py`, `paths.py`, `product_performance.py`, `new_products.py`, `shop_requests.py`, `_combo_button_usage`, `timed_offers.py`, `forward_projections.py`, `fetch_posting_data`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `fetch()` (e.g. with `classify()` and `oos_key()`) actually correct?**
  _`fetch()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `The page`, `Laya model (`lib/laya.py`)`, `Shop birthdays` to the rest of the system?**
  _200 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `current_performance.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12280701754385964 - nodes in this community are weakly interconnected._
- **Should `laya.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._