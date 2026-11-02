# Graph Report - Marketing_dashboard  (2026-11-02)

## Corpus Check
- 244 files · ~1,202,318 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: .csv 14, (none) 2, .toml 1)

## Summary
- 2722 nodes · 5315 edges · 209 communities (160 shown, 49 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 195 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d34adade`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- shop_corporate.py
- laya.py
- lib/receipt_combos.py
- oos_chip.js
- chart_switcher.js
- graw(block, key) function (bare numeric getter)
- Kitengela Rejects tracker (timed offer)
- type_fn
- corporate_clients_from_db
- v5_theme.js
- name_match.py
- bare_minimum setting (weekly target floor)
- lib/offer_data.py
- self_made_combos_bundle/lib/db.py
- fetch_posting_data
- check_connection
- forward_projections.py
- test_oos_callbacks.py
- build_payload
- posting_yields.py
- sticky_controls.js
- shop_requests.py
- oos_callbacks.py
- Self-made combos vs running combos (doc)
- shop_stock_levels.py
- build
- signals
- Dashboard Menu Docs (spec index)
- self_made_combos_bundle/lib/report_month.py
- _enrich_deals
- fetch_new_products_data
- insights.html
- streamlit_app.py
- odoo_tabs.py
- monthly_report.py
- anchor
- chronos_train.py
- stock.py
- build_payload
- Shops Efficiency Tracking spec doc
- ads_panel.js
- build
- push_rules.py
- page_sidebar.js
- attach_stock
- Combos & Power Deals by Shop panel (#combo-shop)
- self_made_combos_bundle/offer_data.py
- Self-made combos bundle Python dependencies (requirements.txt)
- CLAUDE.md
- history.py (read months back)
- Self-made combos vs Running combos portable bundle README
- bags_on_offer.py
- compute_period
- Bags on offer vs not on offer
- algorithmic-art skill
- dataviz-charts skill
- scripts/test_receipt_combos.py
- data
- bag_classifier
- High-End Visual Design skill
- ads.py
- _load_shop_regions
- offer_picking.py
- daydream skill (Vault Daydream)
- design-taste-frontend (anti-slop frontend skill)
- snapshot.py
- _combo_button_usage
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- _q
- bag_key_fn
- marketing_dashboard.sql
- _enrich_deals
- build
- shop_birthdays.py
- push_planner.py
- Denri Africa Dashboard Design System (skill)
- signals
- why_moved.js
- theme.py
- push_laya.py
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- facts
- fetch
- Month-End Routine
- test_share_targets.py
- test_push_planner.py
- _is_checked
- test_stockout_demand.py
- Out-of-stock demand — people, not requests
- shop-birthdays.md
- shops_dispatch.py
- _fetch_monthly_kenya
- generator
- negative_fixes.py
- custom_range.py
- reject_sales.py
- run_query
- Bag Signals — quant view of each bag (posting · stock · selling)
- _bg_jobs
- current_performance.html
- attach
- self_made_combos.py generator (build_payload + SQL + injection)
- new_products.py
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- month_extras.py
- Ralph task — "Out of stock — call back" demand per shop
- Ralph task — only three sheet tabs left
- timed_offers.py
- Bag targets October 2026_3acbad00.md
- odoo_marketing_audit.py
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- daily
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- get_engine
- fetch
- What the page shows
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- Product (bag) targets
- POST_DATA data block (Posting)
- _growth_tracking
- read_block(file, start, end) function
- moves
- build
- _bg_rebuild
- contextlib
- Chart type switcher (every chart, every menu)
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- New Products Analytics (doc)
- _alignment_region
- Offer Picking (doc)
- start_server
- _dead_clear
- timed_offers.py (generator)
- scripts/receipt_combos.py
- test_sheet_reads.py
- safe_int
- generate_insights.py
- _dead_stock_region
- Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)
- followup
- _collect_comments
- _combo_norm_option
- html
- Footfall and Marketing (21 Oct 2026, user's call)
- num
- Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)
- _read_offers
- week_start_of
- Product Performance — Shop breakdown: progress
- _build_period
- realistic_rates
- run.py
- Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)
- corporate_return
- _write_offers_cache
- os
- _bucket
- test_product_targets.py
- sys
- _bag_sales_daily_sql
- Ralph loop brief — Footfall and Marketing page
- Bag signals — quant finance applied to product sales
- ambiguous_python_import_17686b6faac5
- main.py
- _seasonality
- _bag_tiers
- Sales-share targets per product
- Ads impact — on every page (21 Oct 2026, user's call)
- _bag_stock
- Combos from receipts — running vs self-made
- render
- live_month_window
- _analyze_region
- Odoo marketing data audit
- ODOO_MARKETING_AUDIT.md
- master_products
- read
- lib

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 88 edges
2. `fetch()` - 41 edges
3. `data()` - 39 edges
4. `fetch_posting_data()` - 38 edges
5. `check_connection()` - 34 edges
6. `get_gspread_client()` - 33 edges
7. `build_payload()` - 30 edges
8. `build()` - 25 edges
9. `excluded_products()` - 25 edges
10. `build_payload()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `The split — by each bag's share of recent sales` --references--> `bag_classifier()`  [INFERRED]
  docs/product-targets.md → generators/self_made_combos.py
- `Inputs (read only — nothing is written to Odoo or the sheet)` --references--> `bag_classifier()`  [INFERRED]
  docs/push-planner.md → generators/self_made_combos.py
- `Sales pace to month end (19 Oct 2026)` --references--> `month_end_lift()`  [INFERRED]
  docs/shop-stock-levels.md → generators/shop_stock_levels.py
- `Laya's second opinion (`lib/push_laya.py`)` --references--> `state_text()`  [INFERRED]
  docs/push-planner.md → lib/push_laya.py
- `Why it isn't moving — reasons, per market (`push_rules.reasons`)` --references--> `reasons()`  [INFERRED]
  docs/push-planner.md → lib/push_rules.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Self-made combos bundle: generator, Sheets auth, DB access, and dependency manifest working together to build the combos page** — export_self_made_combos_bundle_self_made_combos_py, export_self_made_combos_bundle_offer_data_py, export_self_made_combos_bundle_google_auth_py, export_self_made_combos_bundle_lib_db_py, export_self_made_combos_bundle_requirements [EXTRACTED 0.90]
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]

## Communities (209 total, 49 thin omitted)

### Community 0 - "shop_corporate.py"
Cohesion: 0.15
Nodes (25): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), _acronym(), build(), _maybe(), owns(), corporate_team_receipts(), _d() (+17 more)

### Community 1 - "laya.py"
Cohesion: 0.09
Nodes (26): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket() (+18 more)

### Community 2 - "lib/receipt_combos.py"
Cohesion: 0.06
Nodes (54): What the page shows (per period), _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, _fill_units(), _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region… (+46 more)

### Community 3 - "oos_chip.js"
Cohesion: 0.08
Nodes (38): attach(), close(), esc(), form(), go(), iso(), mountPanel(), open() (+30 more)

### Community 4 - "chart_switcher.js"
Cohesion: 0.12
Nodes (35): alpha(), apply(), attach(), axisOpts(), build(), changeTxt(), Chart(), clone() (+27 more)

### Community 6 - "Kitengela Rejects tracker (timed offer)"
Cohesion: 0.07
Nodes (28): bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source), Offline fallback pattern (mirror sheet data to local JSON), Reject Sale (doc: reject_sales.py -> reject_sales.html, RJ), reject_sales_export.csv (fallback export) (+20 more)

### Community 7 - "type_fn"
Cohesion: 0.20
Nodes (14): build(), {TYPE: {"kes", "shops": {SHOP: {"n", "kes"}}}} for the runway types over…, ({TYPE: Kenya shop on-hand}, {TYPE: Sinza + Uganda on-hand}) — live Odoo., The NP.runway payload: {days, bags: [{name, created, category, stockKe,…, Product name → bag type (see the module docstring)., [{name, created, category}] newest first — the runway bag types as of today; []…, {TYPE: bags sold} for the given runway types over [start, end] — POS bags,…, runway_bags() (+6 more)

### Community 8 - "corporate_clients_from_db"
Cohesion: 0.40
Nodes (6): corporate_clients_from_db(), _months(), A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],…, Current month's corporate activity per client (quoted · invoiced · paid · sold)…, _txt()

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 12 - "lib/offer_data.py"
Cohesion: 0.06
Nodes (43): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, ({PRODUCT: {SHOP CODE: units}}, {PRODUCT: {SHOP CODE: [[colour, units], …]}})…, shop_sales(), apply_walkins(), _aliases(), base_name(), build_rows() (+35 more)

### Community 13 - "self_made_combos_bundle/lib/db.py"
Cohesion: 0.15
Nodes (18): check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, Run a read query and return a DataFrame, or None if the DB is unreachable.… (+10 more)

### Community 14 - "fetch_posting_data"
Cohesion: 0.15
Nodes (11): fetch_posting_data(), _clear(), _yield(), _fold_bag_level(), load_dead_thresholds(), _post_yield(), Bags whose posts marketing logs only per BAG (the posting sheet's TOTAL row,…, Marketing & Sales Alignment — posting yield, measured the way marketing… (+3 more)

### Community 15 - "check_connection"
Cohesion: 0.08
Nodes (27): corporate_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, _corporate_bags(), The month's revenue target (KES): Odoo sales_pos_target amount (pos +…, (corporate bags, corporate KES received) in the given month, live from Odoo…, _revenue_target(), build_offer(), odoo_bag_daily_value() (+19 more)

### Community 16 - "forward_projections.py"
Cohesion: 0.08
Nodes (14): fetch_monthly_target(), current_performance.py…, fetch_sheet_data(), fmt_opt_pct(), fmt_pct(), _orow(), forward_projections.py…, One table row, month-end projected. expected = what the targets expect from… (+6 more)

### Community 17 - "test_oos_callbacks.py"
Cohesion: 0.19
Nodes (19): aggregate(), flat(), split(), The page block: {period: {key: {"total": people, "shops": [[shop, people],…, pytest, _base_sql(), _kai(), Tests for lib/oos_callbacks.py (WhatsApp "Out of stock — call back" demand).… (+11 more)

### Community 18 - "build_payload"
Cohesion: 0.05
Nodes (41): _bags_not_on_offer(), _infer(), _norm(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups() (+33 more)

### Community 19 - "posting_yields.py"
Cohesion: 0.07
Nodes (25): _posts(), MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., _mkt_perfect_week_index(), _mkt_week_label(), posting_yields.py…, Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]., current = {region: {key: {productName,colour,category,bagType,stock}}}. A new… (+17 more)

### Community 20 - "sticky_controls.js"
Cohesion: 0.20
Nodes (15): bind(), embedHost(), headerOf(), init(), initSections(), injectCss(), place(), setPinned() (+7 more)

### Community 21 - "shop_requests.py"
Cohesion: 0.16
Nodes (18): Shop requests vs received (this month · last month) and the production approved…, requests_block(), _d(), _f(), _match(), _offers(), _pct(), production() (+10 more)

### Community 22 - "oos_callbacks.py"
Cohesion: 0.13
Nodes (21): _cache_path(), DataFrame, run_query with a TTL disk cache. Identical to run_query for callers, but a…, run_query_cached(), _date(), load_rows(), _online_rows(), oos_by_bag_shop() (+13 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.14
Nodes (18): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+10 more)

### Community 24 - "shop_stock_levels.py"
Cohesion: 0.08
Nodes (42): What each page shows, bag_categories(), buffer_stock(), build(), dispatch_shop(), fit(), grand_total(), leads() (+34 more)

### Community 25 - "build"
Cohesion: 0.26
Nodes (17): build(), acts(), campaign_table(), money(), chart_data(), ser(), cpr(), focus_tiles() (+9 more)

### Community 26 - "signals"
Cohesion: 0.17
Nodes (16): action(), _mean(), _phi(), posting_beta(), The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json…, _sd() (+8 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.18
Nodes (14): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes) (+6 more)

### Community 28 - "self_made_combos_bundle/lib/report_month.py"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 29 - "_enrich_deals"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "fetch_new_products_data"
Cohesion: 0.06
Nodes (37): _new_products(), This month's new products: data/new_products.txt (lib/new_products_list) — the…, fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed() (+29 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.08
Nodes (18): cache_data, SCRIPT_TIMEOUT = 600s config, hashlib, html, streamlit, _load_secrets_into_env(), _month_archived(), _month_end_running() (+10 more)

### Community 33 - "odoo_tabs.py"
Cohesion: 0.10
Nodes (22): load(), metric_byshop(), parse_sheet(), shops_efficiency.py…, Return (data, meta) for the Kenya shops, locating columns by header name…, safe_int(), update_history(), lib — shared data-access for the marketing dashboard (Postgres migration).… (+14 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.16
Nodes (8): _cause(), esc(), fmt(), ladder_strip(), pct(), monthly_report.py…, _smc_srow(), _stock_rows()

### Community 35 - "anchor"
Cohesion: 0.27
Nodes (10): count_complete_weeks_in_month(), Count Mon–Sun weeks in the reporting month that have ≥5 days falling within it., anchor(), month_key(), month_name(), month_window(), date, The date whose month is the reporting month: yesterday, unless pinned. Pinned… (+2 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.13
Nodes (27): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+19 more)

### Community 37 - "stock.py"
Cohesion: 0.20
Nodes (15): odoo_stock_levels(), Live per-shop Odoo on-hand in the SAME shape parse_sheet(STOCK_LEVELS) returns:…, _codes_for(), _inlist(), odoo_stock_at_location(), odoo_stock_by_product(), odoo_stock_by_shop_code(), _ok() (+7 more)

### Community 38 - "build_payload"
Cohesion: 0.12
Nodes (18): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+10 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "ads_panel.js"
Cohesion: 0.22
Nodes (16): act(), axes(), cell(), charts(), drawCmp(), drawWow(), values(), esc() (+8 more)

### Community 41 - "build"
Cohesion: 0.19
Nodes (13): build(), _add(), _cfg(), first_sale(), load_prices(), make_matcher(), match(), extra: more bag types to recognise (the price list's), for stock sent that… (+5 more)

### Community 42 - "push_rules.py"
Cohesion: 0.13
Nodes (17): action(), _cover_txt(), _kind(), _n(), not_moving(), posting_median(), rank(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).… (+9 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "attach_stock"
Cohesion: 0.18
Nodes (14): bag(), col(), attach_stock(), in_stock(), stk(), collect(), _in(), is_combo_request() (+6 more)

### Community 45 - "Combos & Power Deals by Shop panel (#combo-shop)"
Cohesion: 0.25
Nodes (8): Combos & Power Deals by Shop panel (#combo-shop), compute_period() function (emits pushDetail per period), Deal of the Week — Tier 2 (latest 2-week window) shop-scoped view, DenriTableFilter reusable filter bar component, DOW_MIRROR expansion (Starmall to Hazina/Hilton/KTDA), odoo_stock_levels() function, Push via filter (None / power deal / deal of the week tag), shops_efficiency.html page

### Community 46 - "self_made_combos_bundle/offer_data.py"
Cohesion: 0.15
Nodes (19): get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), cell(), find_row() (+11 more)

### Community 47 - "Self-made combos bundle Python dependencies (requirements.txt)"
Cohesion: 0.15
Nodes (14): google_auth.py (Sheets auth), lib/db.py (Supabase session pooler DB access), lib/db.run_query (shared connection reuse per subprocess), offer_data.build (batched Sheets range fetch), Refresh Performance (shared connection reuse, batched Sheets reads), Supabase session pooler host rule (direct host is IPv6-only), google_auth.py (service account or OAuth desktop), gspread>=6.0 dependency (Google Sheets access) (+6 more)

### Community 49 - "history.py (read months back)"
Cohesion: 0.33
Nodes (7): denri_mkt_* Supabase tables, history.html page, history.py (read months back), month_end.py (freezes a month), push_to_supabase.py (write months), Resilience fallback: history.py leaves existing page data untouched if Supabase unreachable, supabase_migration.py (schema)

### Community 50 - "Self-made combos vs Running combos portable bundle README"
Cohesion: 0.25
Nodes (8): shop-regions.md (editable Shop to Region table), Composition-based classification rationale (Running vs Self-made), _matches_sheet / _build_sheet_slots slot-aware matching functions, Self-made combos vs Running combos portable bundle README, Returns netting rationale (qty <> 0, returns subtract), docs/self-made-combos.md full spec for the menu, docs/shop-regions.md editable shop to region map, sql/self_made_vs_running_combos.sql (standalone pure-SQL classification)

### Community 51 - "bags_on_offer.py"
Cohesion: 0.26
Nodes (11): _base_windows(), _custom_range(), fmt(), inject(), main(), bags_on_offer.py…, (from, to) dates from boo_custom_range.json — the Custom period — or None., Write (or with a=None, delete) the Custom period's dates. (+3 more)

### Community 52 - "compute_period"
Cohesion: 0.12
Nodes (11): apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _metric(), pct(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period. (+3 more)

### Community 53 - "Bags on offer vs not on offer"
Cohesion: 0.13
Nodes (15): Bags on offer vs not on offer, Corporate-lead till orders, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Out of stock — call back, Period selector (Monthly / Weekly / Last week / Custom), Regenerate, Shop birthdays (+7 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.17
Nodes (12): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+4 more)

### Community 56 - "scripts/test_receipt_combos.py"
Cohesion: 0.32
Nodes (15): classify(), lines: [{receipt, d, product, qty, amount}] → per-market summary: {running:…, infer(), L(), Tests for receipt_combos.py + name_match.py — python -m pytest scripts -q, test_alternatives_and_singles(), test_bulk_receipts_are_not_combos(), test_four_bags_at_two_prices_are_two_combos() (+7 more)

### Community 57 - "data"
Cohesion: 0.12
Nodes (19): _db_count(), monthly_from_db(), Reporting month's subset count (e.g. rejectBags, giftBags) from…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,…, _live_bags(), _perfect_week_index(), Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, update_weekly_history() (+11 more)

### Community 58 - "bag_classifier"
Cohesion: 0.17
Nodes (15): Buckets, _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _norm_combo() (+7 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "ads.py"
Cohesion: 0.22
Nodes (12): Charts (21 Oct 2026, user's call), campaigns(), _f(), market_week(), notes(), date, lib/ads.py — marketing's Weekly Ads Performance Report, as data (spec:…, Every campaign-week row, with spend_kes added (USD × USD_KES). (+4 more)

### Community 62 - "offer_picking.py"
Cohesion: 0.12
Nodes (27): _alt_cost(), _apply_alias(), build(), _build_catalog(), _combo_cost(), _combo_slots(), _is_full_price(), _monthly_bag_sales() (+19 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "design-taste-frontend (anti-slop frontend skill)"
Cohesion: 0.18
Nodes (12): design-taste-frontend (related skill), design-taste-frontend (anti-slop frontend skill), Brief-First Process (8-step design workflow), Hard Bans (typography, color, layout, code, content clichés), Pre-Flight Checklist (90+ items), Redesign Protocol (upgrading existing UI), Three Dials — DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, Three AI-generated design clusters (calibration reference) (+4 more)

### Community 65 - "snapshot.py"
Cohesion: 0.18
Nodes (16): _age_min(), _cleanup(), fresh_meta(), _meta(), _p(), query(), lib/snapshot.py — local DuckDB snapshot of the tills (docs/README.md › DuckDB…, The snapshot to read, refreshing it first when it's too old; None if there's… (+8 more)

### Community 66 - "_combo_button_usage"
Cohesion: 0.14
Nodes (11): _combo_button_usage(), _matches_sheet(), _opt_close(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Same slot count and every slot overlaps under SOME pairing (any order: the…, The sheet label this Odoo combo maps to, or None if it isn't on the sheet.…, _slots_fit() (+3 more)

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.11
Nodes (18): Bag health (by bag, 18 Oct 2026), Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026), Page, Product rating and core 5 vs other 13 categories (18 Oct 2026) (+10 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "_q"
Cohesion: 0.18
Nodes (11): followers_daily(), _q(), {week ISO: {"site": {orders, bags, kes}, "people": {…}}}., Shopify title → bag key, via the dashboard's bag key: the longest run of words…, ({bag: {"clicks", "visitors", "colours": {colour: clicks}}}, combo_clicks,…, [{platform, date, followers, newFollows, reach, views}] oldest first (from 18…, [{week (Monday), sessions, users, orders, revenue, carts, checkouts, abandoned,…, _title_bag() (+3 more)

### Community 71 - "bag_key_fn"
Cohesion: 0.13
Nodes (18): build(), Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), _odoo_post_check(), (start, end) → {bag: {"clicks", …}} website WhatsApp taps, one Odoo pull per…, _wa_taps(), get(), bag_posts() (+10 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "_enrich_deals"
Cohesion: 0.07
Nodes (26): _as_day(), dow_tier_weeks(), _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg() (+18 more)

### Community 74 - "build"
Cohesion: 0.11
Nodes (20): actions(), build(), agg(), week_tot(), num(), pearson(), What we can do' — by rule (docs/footfall-marketing.md › Actions). Each names a…, JSON-safe number: NaN / None → None. (+12 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "push_planner.py"
Cohesion: 0.12
Nodes (24): build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), load_data(), main() (+16 more)

### Community 77 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.17
Nodes (13): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), Signature Element — Flowing Border (achievement cards), high-end-visual-design (related skill), KPI Tile component (+5 more)

### Community 78 - "signals"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

### Community 79 - "why_moved.js"
Cohesion: 0.36
Nodes (12): bestWeek(), bestWeeks(), build(), fillWeeks(), getW(), hasKey(), mark(), onClick() (+4 more)

### Community 80 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), lib/theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 81 - "push_laya.py"
Cohesion: 0.14
Nodes (19): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+11 more)

### Community 82 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

### Community 83 - "facts"
Cohesion: 0.15
Nodes (18): Per bag × market: the facts (`push_rules.facts`, `add_peers`), add_peers(), _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), ISO date n days before END (0 = END). (+10 more)

### Community 84 - "fetch"
Cohesion: 0.12
Nodes (17): Counted by how it was sold, _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…, _bags_not_on_offer(), fetch(), fmt() (+9 more)

### Community 85 - "Month-End Routine"
Cohesion: 0.20
Nodes (9): Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand, The newer pages in History (`extras`), What it does (+1 more)

### Community 86 - "test_share_targets.py"
Cohesion: 0.22
Nodes (11): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+3 more)

### Community 87 - "test_push_planner.py"
Cohesion: 0.16
Nodes (25): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m…, A facts row with sensible defaults, overridden by kw. (+17 more)

### Community 88 - "_is_checked"
Cohesion: 0.18
Nodes (17): _build_no_convert(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int(), _is_checked(), _is_x() (+9 more)

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.14
Nodes (10): Agent skills — retail analytics, Test a skill, Use in another project, Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods (+2 more)

### Community 91 - "shop-birthdays.md"
Cohesion: 0.15
Nodes (11): Design Tokens (colors, typography, spacing), Semantic color rules (green=good, amber=risk, red=critical, cyan=info), Analytics Dashboard specific rules (VISUAL_DENSITY: dense), Shop birthdays, Shop → opening date, Where it shows, Per-shop combo-button chips (red when < half best-in-region), Region colour palette (reference for Executive Dashboard) (+3 more)

### Community 92 - "shops_dispatch.py"
Cohesion: 0.21
Nodes (15): build_period(), distributed_in(), main(), q(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only. (+7 more)

### Community 93 - "_fetch_monthly_kenya"
Cohesion: 0.23
Nodes (12): _fetch_monthly_kenya(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), Monthly Kenya figures for the S1 KPI cards. MONTHLY_MARKETING_POST: sum col E…, MONTHLY_SALES: colour=A(0), product_name=B(1), MONTHLY_MARKETING_POST: colour=A(0), product_name=C(2) (+4 more)

### Community 94 - "generator"
Cohesion: 0.17
Nodes (12): generator(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, start_daily_snapshot(), clear_timed_offers(), main(), YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that… (+4 more)

### Community 95 - "negative_fixes.py"
Cohesion: 0.06
Nodes (46): argparse, fnmatch, _negfix(), Stock record accuracy per shop for every period (docs/shops-efficiency.md ›…, bags_sold(), block(), by_shop(), _date() (+38 more)

### Community 96 - "custom_range.py"
Cohesion: 0.19
Nodes (14): block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each…, (from, to) dates for the page's Custom period, or None. Swapped if reversed;… (+6 more)

### Community 97 - "reject_sales.py"
Cohesion: 0.18
Nodes (14): _assign_price(), _bom_costs(), build(), _category_of(), _norm_cat(), reject_stock.csv → {BAG (upper): {units, colours:{COLOUR: units}}}., (price, flag) from BOM cost — two tiers. flag ∈ {'', 'thin', 'below', 'nobom'}., Write an Excel (xlsx, or CSV fallback) of EVERYTHING on the pricing board —… (+6 more)

### Community 98 - "run_query"
Cohesion: 0.08
Nodes (31): market_sales(), {market: {bags, kes, orders}} over [start, end]., {market: [ {bags, kes, orders} per week ]} from Odoo; None if Postgres is down., sales_by_market(), corporate_target_from_db(), last_week_from_db(), Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, This month's Odoo corporate target {bags, kes} (sales_pos_target, scope… (+23 more)

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "_bg_jobs"
Cohesion: 0.25
Nodes (8): cache_resource, fragment, _bg_done_msg(), _bg_jobs(), _bg_watch(), _fmt_secs(), Background rebuilds shared by every session: label → job (see _bg_rebuild)., The refresh_msg for a finished background rebuild (None: the job vanished).

### Community 101 - "current_performance.html"
Cohesion: 0.50
Nodes (4): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance)

### Community 102 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 103 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.29
Nodes (7): lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, lib/report_month.py (which month are we reporting?), self_made_combos.html static page (reads const SMC), self_made_combos.py generator (build_payload + SQL + injection)

### Community 104 - "new_products.py"
Cohesion: 0.18
Nodes (7): _base_colour(), _merge_rows_by_base_colour(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across…, _strip_colour_qualifiers()

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "month_extras.py"
Cohesion: 0.06
Nodes (55): why_moved(), load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, _load_shop_regions(), Shop → Region from docs/shop-regions.md (lib/shop_regions); the built-in…, _bags_on_offer(), _block() (+47 more)

### Community 107 - "Ralph task — "Out of stock — call back" demand per shop"
Cohesion: 0.25
Nodes (7): match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, Established facts (do not re-investigate), Every iteration, Periods (dates in Africa/Nairobi), Ralph task — "Out of stock — call back" demand per shop, Stopping

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "timed_offers.py"
Cohesion: 0.11
Nodes (24): _bags_from_file(), _derive_month(), kenya_stock_by_bag(), load_config(), _norm_offer(), _parse_colour(), timed_offers.py…, Multi-offer config: {"month": "YYYY-MM", "offers": [offer, ...]}. Back-compat:… (+16 more)

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "odoo_marketing_audit.py"
Cohesion: 0.39
Nodes (8): root(), audit(), _expected(), main(), _period(), _range(), scripts/odoo_marketing_audit.py — how complete and up to date each marketing…, _step()

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 114 - "daily"
Cohesion: 0.25
Nodes (8): daily(), _load_backup(), _num(), parse(), {(BAG TYPE, COLOUR): {market: {date: posts}}} from the three sheets (cached for…, (out, order, savedAt) from the saved copy, or None., One tab's rows → {(BAG TYPE, COLOUR): {date: posts}}., _save_backup()

### Community 121 - "get_engine"
Cohesion: 0.29
Nodes (7): _env(), get_engine(), Engine, The process's reused connection (opened on first query). Every generator runs…, Build a SQLAlchemy URL from the environment, or None if unset. Accepts…, _shared_conn(), _url()

### Community 122 - "fetch"
Cohesion: 0.12
Nodes (26): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), combo_slots(), make_classifier() (+18 more)

### Community 123 - "What the page shows"
Cohesion: 0.18
Nodes (11): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 2b. Shop breakdown (22 Oct 2026, user's call), 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Bulk orders, Data (+3 more)

### Community 126 - "Product (bag) targets"
Cohesion: 0.25
Nodes (8): A month with only a revenue target (November 2026), Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 128 - "_growth_tracking"
Cohesion: 0.33
Nodes (6): _growth_tracking(), data/growth_tracking.json + the report month: live (so far + projected + this…, is_pinned(), _pinned(), (year, month) from DENRI_REPORT_MONTH=YYYY-MM, or None when unset/invalid., True when DENRI_REPORT_MONTH pins the month (a deliberate rebuild).

### Community 130 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 131 - "build"
Cohesion: 0.06
Nodes (37): build(), corp(), corporate_period(), _d(), explain(), _fmt_d(), _load_json(), load_lines() (+29 more)

### Community 132 - "_bg_rebuild"
Cohesion: 0.40
Nodes (6): _bg_rebuild(), work(), Seconds the last good `kind` rebuild of `lbl` took (any kind as a fallback),…, Rebuild `lbl` in the background. kind: "auto" (skipped if a rebuild was tried…, _rebuild_secs(), _save_rebuild_secs()

### Community 138 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.22
Nodes (7): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does, Current Performance (doc)

### Community 145 - "Shop Launch"
Cohesion: 0.22
Nodes (8): Config, Launch day, Marketing posts, Prices (30 Oct 2026, user's call), Sales, Shop Launch, What the page shows, Where the stock is (30 Oct 2026, user's call)

### Community 153 - "New Products Analytics (doc)"
Cohesion: 0.14
Nodes (16): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Bag-type matching for combo components (_match_bag / BAG_ALIASES), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES) (+8 more)

### Community 154 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 155 - "Offer Picking (doc)"
Cohesion: 0.22
Nodes (10): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Combo button usage / rung vs pot. (till check), Self-made combos vs running combos (export bundle copy) (+2 more)

### Community 156 - "start_server"
Cohesion: 0.31
Nodes (8): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_to_config(), _json()

### Community 157 - "_dead_clear"
Cohesion: 0.22
Nodes (7): _onoff(), _bt_on_offer(), _dead_clear(), Dead-stock clearance for ONE region and ONE period, posted vs not posted × on…, Is this bag type on offer, matched against the Self-Made-Combos offer set with…, _offer_label(), offer()

### Community 158 - "timed_offers.py (generator)"
Cohesion: 0.09
Nodes (22): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+14 more)

### Community 159 - "scripts/receipt_combos.py"
Cohesion: 0.29
Nodes (6): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…, itertools

### Community 160 - "test_sheet_reads.py"
Cohesion: 0.47
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 161 - "safe_int"
Cohesion: 0.40
Nodes (5): _bag_level_bags(), Bag types with posts logged without a colour in any of the posting tabs., safe_int(), is_bag_level(), A tab_rows() row of posts with no colour (from the bag type's TOTAL row):…

### Community 162 - "generate_insights.py"
Cohesion: 0.24
Nodes (5): card(), esc(), fmt(), generate_insights.py…, region_card()

### Community 163 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 165 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 166 - "_collect_comments"
Cohesion: 0.50
Nodes (3): _collect_comments(), _html_text(), The comments

### Community 167 - "_combo_norm_option"
Cohesion: 0.22
Nodes (10): _build_sheet_slots(), _combo_norm_option(), _combo_sheet_slots(), combos_by_shop(), _norm(), _tokmatch(), Per-shop view for Shops Efficiency, keyed by shop-location label (e.g.…, One combo slot-option → its distinctive bag token(s), colours/category words… (+2 more)

### Community 168 - "html"
Cohesion: 0.29
Nodes (6): read_block(), read_block(), _read_timed_offers(), _offer_bagtypes_by_region(), On-offer bag types per region, read from self_made_combos.html's SMC block:…, html()

### Community 169 - "Footfall and Marketing (21 Oct 2026, user's call)"
Cohesion: 0.20
Nodes (9): Actions (rules), Correlations ("Posts and ads vs visitors"), Data traps (said on the page), Definitions, Footfall and Marketing (21 Oct 2026, user's call), Regenerate, Shop mapping (`lib/footfall.SHOPS`), Sources (+1 more)

### Community 170 - "num"
Cohesion: 0.20
Nodes (11): _garr_line(), gnum(), num(), _offers(), _parse_offers(), _units(), This month's timed-offer campaigns, flattened for storage. The live TO payload…, Greedy single-line array extractor — handles nested [[...],[...]] arrays. (+3 more)

### Community 172 - "_read_offers"
Cohesion: 0.40
Nodes (5): Offer type summary (matrix), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, _read_offers(), _read_offers_cache()

### Community 173 - "week_start_of"
Cohesion: 0.33
Nodes (6): Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary(), week_start_of(), weekly_from_db()

### Community 174 - "Product Performance — Shop breakdown: progress"
Cohesion: 0.22
Nodes (8): 1. Spec — DONE, 2. Data — DONE, 3. Page section — DONE, 4. Sidebar and sticky bar — DONE, 5. Visual check — DONE, 6. Wrap-up — DONE, Product Performance — Shop breakdown: progress, Summary

### Community 175 - "_build_period"
Cohesion: 0.18
Nodes (6): _build_period(), _offer_types(), _pick_target(), Latest target row for `shop` with this period that overlaps [start, end]. A…, Matrix payload: rows, per-row category / tier cells, and the period's Top-5…, _region_of()

### Community 177 - "realistic_rates"
Cohesion: 0.53
Nodes (6): _clamp(), ({SHOP: {BAG: units a week}}, {SHOP: {"recent", "season", "growth"}}) — recent…, realistic_rates(), growth(), season(), tot()

### Community 178 - "run.py"
Cohesion: 0.22
Nodes (13): action_js(), main(), node_check(), Run the sticky-controls checks on every wired page and print the markdown…, edge_dump(), embedded(), inline_local(), js_str() (+5 more)

### Community 179 - "Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)"
Cohesion: 0.20
Nodes (9): 1. Spec — DONE, 2. SQL + library — DONE, 3. Generator — DONE, 4. Page — DONE, 5. Actions — DONE, 6. Visual check — DONE, 7. Wrap-up — DONE, Findings (16 weeks, 28 Jun – 17 Oct 2026; last fully counted week 11–17 Oct) (+1 more)

### Community 182 - "os"
Cohesion: 0.07
Nodes (45): One-off: restore August's Offer Type figures into monthly_report_history.json…, calendar, collections, csv, datetime, lib — shared data-access for the marketing dashboard (Postgres migration).…, self_made_combos.py…, ads_impact.py — the Ads impact panel shown on every page (spec: docs/ads-… (+37 more)

### Community 183 - "_bucket"
Cohesion: 0.19
Nodes (12): _acc(), _bucket(), build_compare(), _cmp_lines(), _days(), _kenya_net_moves_since(), _offer_compare(), Which configured bag (if any) an Odoo/​sheet product name belongs to, by… (+4 more)

### Community 184 - "test_product_targets.py"
Cohesion: 0.16
Nodes (15): allocate(), available_days(), base_period(), The three complete months before month_start → (start, end)., Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, _add_months(), _d() (+7 more)

### Community 185 - "sys"
Cohesion: 0.11
Nodes (23): dotenv, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers… (+15 more)

### Community 187 - "Ralph loop brief — Footfall and Marketing page"
Cohesion: 0.25
Nodes (7): DATA FACTS (verified 21 Oct 2026), DONE, ESCAPE HATCH, PROJECT RULES (must hold every iteration), Ralph loop brief — Footfall and Marketing page, SELF-CORRECTION, SUB-GOALS (do in order; tick each in notes/footfall_progress.md with the command output that proved it)

### Community 191 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 193 - "main.py"
Cohesion: 0.12
Nodes (21): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, Denri Africa — Marketing Dashboard Launcher… (+13 more)

### Community 194 - "_seasonality"
Cohesion: 0.33
Nodes (7): Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), price_of(), _combo_odoo_slots(), Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…

### Community 195 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

### Community 198 - "Sales-share targets per product"
Cohesion: 0.40
Nodes (4): Deliver, Sales-share targets per product, Steps, Tests

### Community 202 - "Ads impact — on every page (21 Oct 2026, user's call)"
Cohesion: 0.40
Nodes (4): Actions ("what we can do"), Ads impact — on every page (21 Oct 2026, user's call), Figures, Refresh

### Community 203 - "_bag_stock"
Cohesion: 0.40
Nodes (5): _bag_stock(), _combo_bags(), _norm_bag(), Space/punctuation-insensitive key so 'MINIZURI' matches 'MINI ZURI'., Component bags of an offer, each with its stock, sorted most-stock first.

### Community 204 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 205 - "render"
Cohesion: 0.60
Nodes (5): growthData(), render(), drawGrowth(), table(), wf()

### Community 207 - "live_month_window"
Cohesion: 0.24
Nodes (11): odoo_weekly_breakdown(), Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, build(), load_targets(), (rows, total, base start, base end) for the month, from Odoo., {BAG: target units} for the month from product_targets_<YYYY-MM>.csv (built…, write_csv(), live_anchor() (+3 more)

### Community 211 - "_analyze_region"
Cohesion: 0.50
Nodes (4): _analyze_region(), STOCK_LEVELS: colour=A(0), product_name=C(2), Runs all three posting sections for one region. sales_col – column index in…, _sl_key()

### Community 218 - "master_products"
Cohesion: 0.50
Nodes (4): master_products(), _norm_name(), Match the SQL normalisation: lower-case, '.'→space, collapse whitespace., Normalised, de-duplicated master catalogue names (master_products.txt), for the…

### Community 220 - "read"
Cohesion: 0.17
Nodes (14): posts_by_market(), posts_lead_sales(), {market: [posts per week]} from marketing's posting sheets; None if they can't…, Kenya bag types: change in posts one week vs change in bags sold the next,…, _bag_category(), _category(), _date(), posts() (+6 more)

## Knowledge Gaps
- **255 isolated node(s):** `PERF`, `graphify`, `Use in another project`, `Test a skill`, `Inputs you must build from the project's data` (+250 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1119 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **49 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Bags on offer vs not on offer` connect `Bags on offer vs not on offer` to `lib/receipt_combos.py`, `_read_offers`, `fetch`, `bag_classifier`, `shop-birthdays.md`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `run_query()` connect `run_query` to `shop_corporate.py`, `lib/receipt_combos.py`, `build`, `type_fn`, `corporate_clients_from_db`, `lib/offer_data.py`, `fetch_posting_data`, `check_connection`, `forward_projections.py`, `test_oos_callbacks.py`, `build_payload`, `shop_requests.py`, `oos_callbacks.py`, `shop_stock_levels.py`, `_enrich_deals`, `fetch_new_products_data`, `chronos_train.py`, `stock.py`, `build_payload`, `build`, `corporate_return`, `os`, `test_product_targets.py`, `offer_picking.py`, `snapshot.py`, `_seasonality`, `_combo_button_usage`, `_q`, `_enrich_deals`, `build`, `live_month_window`, `fetch`, `read`, `negative_fixes.py`, `month_extras.py`, `odoo_marketing_audit.py`, `get_engine`, `fetch`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `bag_classifier()` connect `bag_classifier` to `lib/receipt_combos.py`, `build_payload`, `push_planner.py`, `Push Planner (`push_planner.py` → `push_planner.html`, `PP`)`, `fetch`, `Bags on offer vs not on offer`, `os`, `fetch`, `Product (bag) targets`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **What connects `PERF`, `graphify`, `Use in another project` to the rest of the system?**
  _255 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `shop_corporate.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14532019704433496 - nodes in this community are weakly interconnected._
- **Should `laya.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._
- **Should `lib/receipt_combos.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06246799795186892 - nodes in this community are weakly interconnected._