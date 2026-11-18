# Graph Report - Marketing_dashboard  (2026-11-09)

## Corpus Check
- 250 files · ~1,206,726 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: .csv 14, (none) 2, .toml 1)

## Summary
- 2755 nodes · 5385 edges · 210 communities (164 shown, 46 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 196 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e13dc56a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- month_extras.py
- laya.py
- lib/receipt_combos.py
- oos_chip.js
- chart_switcher.js
- graw(block, key) function (bare numeric getter)
- Kitengela Rejects tracker (timed offer)
- publish.py
- oos_callbacks.py
- v5_theme.js
- name_match.py
- bare_minimum setting (weekly target floor)
- norm
- lib/db.py
- fetch_posting_data
- check_connection
- forward_projections.py
- ads.py
- build_payload
- self_made_combos_bundle/self_made_combos.py
- sticky_controls.js
- shop_requests.py
- main.py
- Self-made combos vs running combos (doc)
- shop_stock_levels.py
- build
- _combo_button_usage
- Dashboard Menu Docs (spec index)
- signals
- _enrich_deals
- bag_classifier
- insights.html
- streamlit_app.py
- product_performance.py
- monthly_report.py
- lib/report_month.py
- chronos_train.py
- stock.py
- build_payload
- Shops Efficiency Tracking spec doc
- _enrich_deals
- get_gspread_client
- push_rules.py
- page_sidebar.js
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- Combos & Power Deals by Shop panel (#combo-shop)
- self_made_combos_bundle/offer_data.py
- Self-made combos bundle Python dependencies (requirements.txt)
- CLAUDE.md
- history.py (read months back)
- Self-made combos vs Running combos portable bundle README
- runway_bags.py
- shops_efficiency.py
- Bags on offer vs not on offer
- algorithmic-art skill
- dataviz-charts skill
- scripts/test_receipt_combos.py
- excluded_products
- weekly_sales.py
- High-End Visual Design skill
- Stock record accuracy (NEGATIVE FIX LOG) — progress
- ads_panel.js
- fetch_new_products_data
- daydream skill (Vault Daydream)
- realistic_rates
- snapshot.py
- _combo_button_usage
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- bag_tracking.py
- bag_quant.py
- marketing_dashboard.sql
- OOS call-back progress (Ralph loop log)
- build
- shop_birthdays.py
- push_planner.py
- Denri Africa Dashboard Design System (skill)
- shops_dispatch.py
- why_moved.js
- theme.py
- push_laya.py
- _post_yield
- facts
- generators/self_made_combos.py
- supabase_migration.py
- json
- test_push_planner.py
- safe_int
- datetime
- Out-of-stock demand — people, not requests
- shop-birthdays.md
- odoo_marketing.py
- _fetch_monthly_kenya
- bag_key_fn
- negative_fixes.py
- custom_range.py
- self_made_combos_bundle/lib/__init__.py
- generators/bag_signals.py
- Bag Signals — quant view of each bag (posting · stock · selling)
- offer_picking.py
- current_performance.html
- attach
- self_made_combos.py generator (build_payload + SQL + injection)
- _build_catalog
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- why_moved.py
- lib/offer_data.py
- Ralph task — only three sheet tabs left
- timed_offers.py
- Bag targets October 2026_3acbad00.md
- run_scripts
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- _bags_not_on_offer
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- Monthly Report (doc)
- fetch
- What the page shows
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- Product (bag) targets
- POST_DATA data block (Posting)
- followup
- read_block(file, start, end) function
- moves
- current_performance.py
- footfall.py
- contextlib
- Chart type switcher (every chart, every menu)
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- New Products Analytics (doc)
- _alignment_region
- Offer Picking (doc)
- start_server
- reject_sales.py
- google_auth.py (shared auth module)
- scripts/receipt_combos.py
- test_sheet_reads.py
- new_products.py
- generate_insights.py
- _dead_stock_region
- Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)
- Ralph task — "Out of stock — call back" demand per shop
- _apply_receipt_offers
- timed_offers.py (generator)
- compute_period
- Footfall and Marketing (21 Oct 2026, user's call)
- Marketing Dashboard — Google Sheets access & setup (doc)
- Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)
- odoo_tabs.py
- _resolve_bag
- Product Performance — Shop breakdown: progress
- odoo_month_product_bags
- colours.py
- run.py
- Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)
- base_name
- _combo_norm_option
- bags_on_offer.py
- Ads impact — on every page (21 Oct 2026, user's call)
- reject_variants
- os
- _read_offers
- Ralph loop brief — Footfall and Marketing page
- names
- run_query
- Bag signals — quant finance applied to product sales
- ambiguous_python_import_17686b6faac5
- lib
- Bag Tracking
- Sales-share targets per product
- _match
- Combos from receipts — running vs self-made
- render
- product_targets.py
- posting_yields.py
- data
- Odoo marketing data audit
- ODOO_MARKETING_AUDIT.md
- monthly_sales.py
- marketing_posts.py

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 90 edges
2. `fetch()` - 41 edges
3. `data()` - 40 edges
4. `fetch_posting_data()` - 38 edges
5. `check_connection()` - 34 edges
6. `get_gspread_client()` - 33 edges
7. `build_payload()` - 30 edges
8. `excluded_products()` - 26 edges
9. `build()` - 25 edges
10. `build_payload()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `Buckets` --references--> `bag_classifier()`  [INFERRED]
  docs/bags-on-offer.md → generators/self_made_combos.py
- `The split — by each bag's share of recent sales` --references--> `bag_classifier()`  [INFERRED]
  docs/product-targets.md → generators/self_made_combos.py
- `Inputs (read only — nothing is written to Odoo or the sheet)` --references--> `bag_classifier()`  [INFERRED]
  docs/push-planner.md → generators/self_made_combos.py
- `What each page shows` --references--> `new_bags()`  [INFERRED]
  docs/ads-impact.md → generators/shop_stock_levels.py
- `Sales pace to month end (19 Oct 2026)` --references--> `month_end_lift()`  [INFERRED]
  docs/shop-stock-levels.md → generators/shop_stock_levels.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Self-made combos bundle: generator, Sheets auth, DB access, and dependency manifest working together to build the combos page** — export_self_made_combos_bundle_self_made_combos_py, export_self_made_combos_bundle_offer_data_py, export_self_made_combos_bundle_google_auth_py, export_self_made_combos_bundle_lib_db_py, export_self_made_combos_bundle_requirements [EXTRACTED 0.90]
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]

## Communities (210 total, 46 thin omitted)

### Community 0 - "month_extras.py"
Cohesion: 0.07
Nodes (48): load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, _bags_on_offer(), _block(), build_extras(), cp_more_month(), _deals() (+40 more)

### Community 1 - "laya.py"
Cohesion: 0.09
Nodes (26): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket() (+18 more)

### Community 2 - "lib/receipt_combos.py"
Cohesion: 0.06
Nodes (58): collections, csv, What the page shows (per period), _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, _fill_units(), _infer(), _power_products() (+50 more)

### Community 3 - "oos_chip.js"
Cohesion: 0.08
Nodes (38): attach(), close(), esc(), form(), go(), iso(), mountPanel(), open() (+30 more)

### Community 4 - "chart_switcher.js"
Cohesion: 0.12
Nodes (35): alpha(), apply(), attach(), axisOpts(), build(), changeTxt(), Chart(), clone() (+27 more)

### Community 6 - "Kitengela Rejects tracker (timed offer)"
Cohesion: 0.07
Nodes (28): bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source), Offline fallback pattern (mirror sheet data to local JSON), Reject Sale (doc: reject_sales.py -> reject_sales.html, RJ), reject_sales_export.csv (fallback export) (+20 more)

### Community 7 - "publish.py"
Cohesion: 0.19
Nodes (15): fnmatch, main(), node_check(), Run the sticky-controls checks on every wired page and print the markdown…, py_compile, changed_files(), git(), group() (+7 more)

### Community 8 - "oos_callbacks.py"
Cohesion: 0.06
Nodes (55): Out of stock — call back, fixture, aggregate(), flat(), split(), attach_stock(), in_stock(), stk() (+47 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 12 - "norm"
Cohesion: 0.13
Nodes (18): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, ({PRODUCT: {SHOP CODE: units}}, {PRODUCT: {SHOP CODE: [[colour, units], …]}})…, shop_sales(), _aliases(), build_rows(), _Deriver, _flag_cells() (+10 more)

### Community 13 - "lib/db.py"
Cohesion: 0.09
Nodes (30): check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, Run a read query and return a DataFrame, or None if the DB is unreachable.… (+22 more)

### Community 14 - "fetch_posting_data"
Cohesion: 0.13
Nodes (12): count_complete_weeks_in_month(), _dead_clear(), fetch_posting_data(), _clear(), _fold_bag_level(), _offer_bagtypes_by_region(), Bags whose posts marketing logs only per BAG (the posting sheet's TOTAL row,…, Count Mon–Sun weeks in the reporting month that have ≥5 days falling within it. (+4 more)

### Community 15 - "check_connection"
Cohesion: 0.09
Nodes (26): build_offer(), _name_sql(), odoo_bag_daily_value(), odoo_bag_prices(), odoo_bulk_lines(), odoo_daily_kenya(), odoo_list_price(), odoo_offer_price() (+18 more)

### Community 16 - "forward_projections.py"
Cohesion: 0.09
Nodes (22): _bag_revenue(), _bag_revenue_range(), _corporate_bags(), _corporate_lines(), fmt_opt_pct(), fmt_pct(), _orow(), _perfect_week_index() (+14 more)

### Community 17 - "ads.py"
Cohesion: 0.22
Nodes (12): Charts (21 Oct 2026, user's call), campaigns(), _f(), market_week(), notes(), date, lib/ads.py — marketing's Weekly Ads Performance Report, as data (spec:…, Every campaign-week row, with spend_kes added (USD × USD_KES). (+4 more)

### Community 18 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 19 - "self_made_combos_bundle/self_made_combos.py"
Cohesion: 0.16
Nodes (13): get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, fetch(), fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py… (+5 more)

### Community 20 - "sticky_controls.js"
Cohesion: 0.20
Nodes (15): bind(), embedHost(), headerOf(), init(), initSections(), injectCss(), place(), setPinned() (+7 more)

### Community 21 - "shop_requests.py"
Cohesion: 0.16
Nodes (18): Shop requests vs received (this month · last month) and the production approved…, requests_block(), _d(), _f(), _match(), _offers(), _pct(), production() (+10 more)

### Community 22 - "main.py"
Cohesion: 0.12
Nodes (17): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, Denri Africa — Marketing Dashboard Launcher… (+9 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.18
Nodes (13): Bags not on offer per market (Kenya/Sinza/Uganda), Combo button usage / rung vs pot. (till check), Self-made combos vs running combos (doc), DoW mirror shops (DOW_MIRROR), Monetary implication panel (bundling discount), Rank chip (follows active Sort filter), Running-combo classification by bag composition (slot-aware sheet match), Standalone SQL (self_made_vs_running_combos.sql) (+5 more)

### Community 24 - "shop_stock_levels.py"
Cohesion: 0.10
Nodes (35): bag_categories(), buffer_stock(), build(), dispatch_shop(), fit(), grand_total(), leads(), month_end_lift() (+27 more)

### Community 25 - "build"
Cohesion: 0.26
Nodes (17): build(), acts(), campaign_table(), money(), chart_data(), ser(), cpr(), focus_tiles() (+9 more)

### Community 26 - "_combo_button_usage"
Cohesion: 0.15
Nodes (12): _build_sheet_slots(), _combo_button_usage(), _combo_norm_option(), _combo_odoo_slots(), _combo_sheet_slots(), _matches_sheet(), One combo slot-option → its distinctive bag token(s), colours/category words…, Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+4 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.18
Nodes (14): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes) (+6 more)

### Community 28 - "signals"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

### Community 29 - "_enrich_deals"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "bag_classifier"
Cohesion: 0.19
Nodes (14): _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _load_bag_prices(), _norm_combo() (+6 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.05
Nodes (37): cache_resource, SCRIPT_TIMEOUT = 600s config, fragment, html, generator(), clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.… (+29 more)

### Community 33 - "product_performance.py"
Cohesion: 0.08
Nodes (36): build(), corp(), categories(), corporate_period(), _d(), explain(), _fmt_d(), _load_json() (+28 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.06
Nodes (38): _bag_stock(), _cause(), _collect_comments(), _combo_bags(), esc(), fmt(), _garr_line(), gnum() (+30 more)

### Community 35 - "lib/report_month.py"
Cohesion: 0.16
Nodes (21): odoo_weekly_breakdown(), Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key() (+13 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.13
Nodes (28): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+20 more)

### Community 37 - "stock.py"
Cohesion: 0.18
Nodes (14): odoo_stock_levels(), Live per-shop Odoo on-hand in the SAME shape parse_sheet(STOCK_LEVELS) returns:…, lib — shared data-access for the marketing dashboard (Postgres migration).…, _codes_for(), _inlist(), odoo_stock_by_product(), odoo_stock_by_shop_code(), _ok() (+6 more)

### Community 38 - "build_payload"
Cohesion: 0.12
Nodes (18): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+10 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "_enrich_deals"
Cohesion: 0.19
Nodes (9): dow_tier_weeks(), _enrich_deals(), _tdigit(), _tier_agg(), _tier_window(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Sun-Sat week numbers a Deal-of-the-Week runs in. With a Start / End date… (+1 more)

### Community 41 - "get_gspread_client"
Cohesion: 0.12
Nodes (27): build(), _add(), launch_curve(), _cfg(), _day_expr(), first_sale(), kenya_posts(), load_categories() (+19 more)

### Community 42 - "push_rules.py"
Cohesion: 0.13
Nodes (17): action(), _cover_txt(), _kind(), _n(), not_moving(), posting_median(), rank(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).… (+9 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

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

### Community 51 - "runway_bags.py"
Cohesion: 0.16
Nodes (19): load_posts(), num(), tally(), ({BAG: [kenya, outside]} last week, {BAG: [kenya, outside]} this month) from…, build(), lib/runway_bags.py — RUNWAY BAGS: bag types first created in Odoo in the last…, {TYPE: {"kes", "shops": {SHOP: {"n", "kes"}}}} for the runway types over…, ({TYPE: Kenya shop on-hand}, {TYPE: Sinza + Uganda on-hand}) — live Odoo. (+11 more)

### Community 52 - "shops_efficiency.py"
Cohesion: 0.11
Nodes (17): apply_odoo(), apply_walkins(), compute_regions(), fmt_pct(), load(), _metric(), metric_byshop(), parse_sheet() (+9 more)

### Community 53 - "Bags on offer vs not on offer"
Cohesion: 0.14
Nodes (14): Bags on offer vs not on offer, Buckets, Corporate-lead till orders, Counted by how it was sold, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Regenerate (+6 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.17
Nodes (12): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+4 more)

### Community 56 - "scripts/test_receipt_combos.py"
Cohesion: 0.32
Nodes (15): classify(), lines: [{receipt, d, product, qty, amount}] → per-market summary: {running:…, infer(), L(), Tests for receipt_combos.py + name_match.py — python -m pytest scripts -q, test_alternatives_and_singles(), test_bulk_receipts_are_not_combos(), test_four_bags_at_two_prices_are_two_combos() (+7 more)

### Community 57 - "excluded_products"
Cohesion: 0.12
Nodes (15): corporate_return(), market_sales(), posts_by_market(), posts_lead_sales(), ads_impact.py — the Ads impact panel shown on every page (spec: docs/ads-…, {market: {bags, kes, orders}} over [start, end]., {market: [posts per week]} from marketing's posting sheets; None if they can't…, Kenya bag types: change in posts one week vs change in bags sold the next,… (+7 more)

### Community 58 - "weekly_sales.py"
Cohesion: 0.16
Nodes (11): fetch_monthly_target(), fetch_sheet_data(), main(), date, _query_ready(), weekly_sales.py — the weekly-sales fix. Computes the CURRENT Sun–Sat week's…, The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's…, week_window() (+3 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "Stock record accuracy (NEGATIVE FIX LOG) — progress"
Cohesion: 0.17
Nodes (11): _negfix(), Stock record accuracy per shop for every period (docs/shops-efficiency.md ›…, 1. Spec — DONE, 2. Library — DONE, 3. Script — DONE, 4. Generator and data — DONE, 5. Page section — DONE, 6. Visual check — DONE (+3 more)

### Community 61 - "ads_panel.js"
Cohesion: 0.22
Nodes (16): act(), axes(), cell(), charts(), drawCmp(), drawWow(), values(), esc() (+8 more)

### Community 62 - "fetch_new_products_data"
Cohesion: 0.20
Nodes (14): fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_sales_window() (+6 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "realistic_rates"
Cohesion: 0.53
Nodes (6): _clamp(), ({SHOP: {BAG: units a week}}, {SHOP: {"recent", "season", "growth"}}) — recent…, realistic_rates(), growth(), season(), tot()

### Community 65 - "snapshot.py"
Cohesion: 0.16
Nodes (17): _age_min(), _cleanup(), fresh_meta(), _meta(), _p(), query(), lib/snapshot.py — local DuckDB snapshot of the tills (docs/README.md › DuckDB…, The snapshot to read, refreshing it first when it's too old; None if there's… (+9 more)

### Community 66 - "_combo_button_usage"
Cohesion: 0.14
Nodes (11): _combo_button_usage(), _matches_sheet(), _opt_close(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Same slot count and every slot overlaps under SOME pairing (any order: the…, The sheet label this Odoo combo maps to, or None if it isn't on the sheet.…, _slots_fit() (+3 more)

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.11
Nodes (18): Bag health (by bag, 18 Oct 2026), Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026), Page, Product rating and core 5 vs other 13 categories (18 Oct 2026) (+10 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "bag_tracking.py"
Cohesion: 0.36
Nodes (8): build(), _cfg(), _colour(), _folder(), canon(), _moves(), generators/bag_tracking.py — Bag Tracking: the chosen bags' Kenya shop stock at…, Odoo product name → the dashboard's bag name (Offer Picking's _build_catalog…

### Community 71 - "bag_quant.py"
Cohesion: 0.13
Nodes (23): build(), action(), bag_posts(), load(), _mean(), _phi(), posting_beta(), lib/bag_quant.py — quant signals per bag: drift, volatility, Sharpe-style… (+15 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.13
Nodes (14): _as_day(), _local_deal_rows(), _in_month(), 2026-10-25' / date / None → date or None., Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), Blocker counter (+6 more)

### Community 74 - "build"
Cohesion: 0.18
Nodes (11): actions(), build(), agg(), week_tot(), num(), pearson(), footfall_marketing.py — Footfall and Marketing page (spec: docs/footfall-…, What we can do' — by rule (docs/footfall-marketing.md › Actions). Each names a… (+3 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "push_planner.py"
Cohesion: 0.12
Nodes (24): build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), load_data(), main() (+16 more)

### Community 77 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.08
Nodes (29): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards) (+21 more)

### Community 78 - "shops_dispatch.py"
Cohesion: 0.21
Nodes (15): build_period(), distributed_in(), main(), q(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only. (+7 more)

### Community 79 - "why_moved.js"
Cohesion: 0.36
Nodes (12): bestWeek(), bestWeeks(), build(), fillWeeks(), getW(), hasKey(), mark(), onClick() (+4 more)

### Community 80 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), lib/theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 81 - "push_laya.py"
Cohesion: 0.14
Nodes (19): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+11 more)

### Community 82 - "_post_yield"
Cohesion: 0.20
Nodes (8): _onoff(), _bt_on_offer(), _yield(), _post_yield(), Marketing & Sales Alignment — posting yield, measured the way marketing…, Is this bag type on offer, matched against the Self-Made-Combos offer set with…, _offer_label(), offer()

### Community 83 - "facts"
Cohesion: 0.15
Nodes (18): Per bag × market: the facts (`push_rules.facts`, `add_peers`), add_peers(), _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), ISO date n days before END (0 = END). (+10 more)

### Community 84 - "generators/self_made_combos.py"
Cohesion: 0.14
Nodes (17): _bag_sales_daily_sql(), _bag_sales_sql(), _bags_not_on_offer(), fetch(), fmt(), inject(), _load_shop_regions(), main() (+9 more)

### Community 85 - "supabase_migration.py"
Cohesion: 0.21
Nodes (11): dotenv, main(), push_to_supabase.py — run the marketing migration against Supabase. Regenerates…, main(), month_block(), num(), q(), supabase_migration.py — export the marketing dashboard's monthly data to a SQL… (+3 more)

### Community 86 - "json"
Cohesion: 0.18
Nodes (14): One-off: restore August's Offer Type figures into monthly_report_history.json…, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers… (+6 more)

### Community 87 - "test_push_planner.py"
Cohesion: 0.16
Nodes (25): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m…, A facts row with sensible defaults, overridden by kw. (+17 more)

### Community 88 - "safe_int"
Cohesion: 0.18
Nodes (17): _bag_level_bags(), _build_no_convert(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), _is_checked(), _is_x(), _posted_stock() (+9 more)

### Community 89 - "datetime"
Cohesion: 0.06
Nodes (54): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+46 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.14
Nodes (10): Agent skills — retail analytics, Test a skill, Use in another project, Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods (+2 more)

### Community 91 - "shop-birthdays.md"
Cohesion: 0.22
Nodes (7): Shop birthdays, Shop → opening date, Where it shows, Per-shop combo-button chips (red when < half best-in-region), self_made_combos.py, Shops & Regions (doc — source of truth), Shop -> Region table

### Community 92 - "odoo_marketing.py"
Cohesion: 0.22
Nodes (12): followers_daily(), _q(), lib/odoo_marketing.py — marketing data the Odoo "Marketing OS" app keeps (spec:…, {week ISO: {"site": {orders, bags, kes}, "people": {…}}}., Shopify title → bag key, via the dashboard's bag key: the longest run of words…, ({bag: {"clicks", "visitors", "colours": {colour: clicks}}}, combo_clicks,…, [{platform, date, followers, newFollows, reach, views}] oldest first (from 18…, [{week (Monday), sessions, users, orders, revenue, carts, checkouts, abandoned,… (+4 more)

### Community 93 - "_fetch_monthly_kenya"
Cohesion: 0.18
Nodes (17): _analyze_region(), _fetch_monthly_kenya(), _fetch_sinza_monthly(), _fetch_sinza_weekly(), _fetch_uganda_monthly(), fmt_int(), _mmp_key(), _ms_key() (+9 more)

### Community 94 - "bag_key_fn"
Cohesion: 0.24
Nodes (10): _odoo_post_check(), (start, end) → {bag: {"clicks", …}} website WhatsApp taps, one Odoo pull per…, _wa_taps(), get(), tally(), meta_posts_by_bag(), ({bag: {"posts", "reach", "views"}}, {"posts", "tagged"}) — Facebook +…, bag_key_fn() (+2 more)

### Community 95 - "negative_fixes.py"
Cohesion: 0.16
Nodes (21): bags_sold(), block(), by_shop(), _date(), _int(), label(), _month_end(), _month_start() (+13 more)

### Community 96 - "custom_range.py"
Cohesion: 0.17
Nodes (15): calendar, block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each… (+7 more)

### Community 97 - "self_made_combos_bundle/lib/__init__.py"
Cohesion: 0.25
Nodes (6): lib — shared data-access for the marketing dashboard (Postgres migration).…, master_products(), _norm_name(), lib/queries.py — SQL for the Litmus Postgres source of truth (Odoo POS). Bags…, Match the SQL normalisation: lower-case, '.'→space, collapse whitespace., Normalised, de-duplicated master catalogue names (master_products.txt), for the…

### Community 98 - "generators/bag_signals.py"
Cohesion: 0.25
Nodes (6): _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), webbrowser

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "offer_picking.py"
Cohesion: 0.13
Nodes (22): _alt_cost(), build(), _combo_cost(), _combo_slots(), offer_picking.py…, {BAG TYPE (upper): production cost} from bom_costs.json — the local copy of the…, Save a local, human-editable copy of the offers prices to OFFERS_CACHE., Parse `const SMC = {…}` out of self_made_combos.html (no DB round-trip). (+14 more)

### Community 101 - "current_performance.html"
Cohesion: 0.50
Nodes (4): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance)

### Community 102 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 103 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.29
Nodes (7): lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, lib/report_month.py (which month are we reporting?), self_made_combos.html static page (reads const SMC), self_made_combos.py generator (build_payload + SQL + injection)

### Community 104 - "_build_catalog"
Cohesion: 0.22
Nodes (10): _build_catalog(), _is_full_price(), _next_month(), bag(), Letters and digits only, so 'CODE3' meets 'CODE 3' and 'FANNYPACK(N)' meets…, {_staff_key(catalogue bag type): staff price} from staff_prices.json (a 0 = no…, Every bag the user can pick for a slot, with two prices from the offers sheet:…, Reference-month combos matched to current Odoo stock, laid out like the offers… (+2 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "why_moved.py"
Cohesion: 0.10
Nodes (32): day_for(), load(), lib/sales_date_fix.py — sales keyed in late, moved back to the day they…, [{"till", "shop", "from", "to", "asDate"}] — datetimes / dates parsed; [] if…, The day a till's sales of `day` count on (day granularity)., load(), lib/shop_regions.py — Shop → Region from docs/shop-regions.md (the source of…, {SHOP (upper): region} parsed from the markdown table under the heading that… (+24 more)

### Community 107 - "lib/offer_data.py"
Cohesion: 0.20
Nodes (12): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), offer_data.py ─────────────────────────────────────────────────────────────────… (+4 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "timed_offers.py"
Cohesion: 0.10
Nodes (29): _acc(), _bags_from_file(), _bucket(), build_compare(), _cmp_lines(), _days(), _derive_month(), _kenya_net_moves_since() (+21 more)

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "run_scripts"
Cohesion: 0.36
Nodes (8): _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, _run_one(), run_scripts(), _handle_refresh(), _run_ref(), _timeout_for()

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 114 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 121 - "Monthly Report (doc)"
Cohesion: 0.22
Nodes (9): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+1 more)

### Community 122 - "fetch"
Cohesion: 0.12
Nodes (26): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), combo_slots(), make_classifier() (+18 more)

### Community 123 - "What the page shows"
Cohesion: 0.18
Nodes (11): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 2b. Shop breakdown (22 Oct 2026, user's call), 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Bulk orders, Data (+3 more)

### Community 126 - "Product (bag) targets"
Cohesion: 0.25
Nodes (8): A month with only a revenue target (November 2026), Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 128 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 130 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 131 - "current_performance.py"
Cohesion: 0.08
Nodes (21): corporate_clients_from_db(), corporate_from_db(), corporate_target_from_db(), last_week_from_db(), _months(), current_performance.py…, Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Bags sold in the previous complete Sun–Sat week, straight from Postgres (same… (+13 more)

### Community 132 - "footfall.py"
Cohesion: 0.27
Nodes (11): daily(), DataFrame, date, lib/footfall.py — footfall (visitors counted per shop per day) joined to walk-…, The Sunday that starts d's Sun–Sat week., One row per footfall shop per day: visitors (NaN = not counted), walk-in orders…, One row per shop per Sun–Sat week. Conversion and revenue use COUNTED days…, Paid-ad WhatsApp leads per WhatsApp shop per Sun–Sat week: chats, bought,… (+3 more)

### Community 138 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.22
Nodes (7): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does, Current Performance (doc)

### Community 145 - "Shop Launch"
Cohesion: 0.18
Nodes (10): Config, Launch day, Marketing posts, Prices (30 Oct 2026, user's call), Race lines, sales by day, product performance, folding (9 Nov 2026, user's call), Sales, Sales keyed in late (9 Nov 2026, user's call), Shop Launch (+2 more)

### Community 153 - "New Products Analytics (doc)"
Cohesion: 0.16
Nodes (14): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix) (+6 more)

### Community 154 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 155 - "Offer Picking (doc)"
Cohesion: 0.29
Nodes (8): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES)

### Community 156 - "start_server"
Cohesion: 0.31
Nodes (8): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_to_config(), _json()

### Community 157 - "reject_sales.py"
Cohesion: 0.18
Nodes (14): _assign_price(), _bom_costs(), build(), _category_of(), _norm_cat(), reject_stock.csv → {BAG (upper): {units, colours:{COLOUR: units}}}., (price, flag) from BOM cost — two tiers. flag ∈ {'', 'thin', 'below', 'nobom'}., Write an Excel (xlsx, or CSV fallback) of EVERYTHING on the pricing board —… (+6 more)

### Community 158 - "google_auth.py (shared auth module)"
Cohesion: 0.25
Nodes (8): google_auth.py (shared auth module), google_credentials.json (OAuth desktop client), google_token.json (OAuth token), main.py (refresh + serve dashboard), OAuth token expiry issue (Testing mode, ~7 day expiry), reauth.py (re-login script), service_account.json (recommended, permanent auth), Service account chosen for zero-maintenance auth + enabling in-dashboard Refresh

### Community 159 - "scripts/receipt_combos.py"
Cohesion: 0.29
Nodes (6): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…, itertools

### Community 160 - "test_sheet_reads.py"
Cohesion: 0.47
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 161 - "new_products.py"
Cohesion: 0.12
Nodes (14): _base_colour(), _merge_rows_by_base_colour(), _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky… (+6 more)

### Community 162 - "generate_insights.py"
Cohesion: 0.20
Nodes (7): card(), esc(), fmt(), generate_insights.py…, read_block(), region_card(), html()

### Community 163 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 165 - "Ralph task — "Out of stock — call back" demand per shop"
Cohesion: 0.25
Nodes (7): match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, Established facts (do not re-investigate), Every iteration, Periods (dates in Africa/Nairobi), Ralph task — "Out of stock — call back" demand per shop, Stopping

### Community 166 - "_apply_receipt_offers"
Cohesion: 0.25
Nodes (6): _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region…, _region_goal(), _till_targets()

### Community 167 - "timed_offers.py (generator)"
Cohesion: 0.29
Nodes (7): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers.html (output), timed_offers.py (generator)

### Community 168 - "compute_period"
Cohesion: 0.29
Nodes (4): compute_period(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period., sum_by_shop()

### Community 169 - "Footfall and Marketing (21 Oct 2026, user's call)"
Cohesion: 0.20
Nodes (9): Actions (rules), Correlations ("Posts and ads vs visitors"), Data traps (said on the page), Definitions, Footfall and Marketing (21 Oct 2026, user's call), Regenerate, Shop mapping (`lib/footfall.SHOPS`), Sources (+1 more)

### Community 170 - "Marketing Dashboard — Google Sheets access & setup (doc)"
Cohesion: 0.29
Nodes (7): timed_offers_config.json (config), Vercel hosted version (static snapshot), Secrets excluded via .gitignore / .vercelignore, Marketing Dashboard — Google Sheets access & setup (doc), Timed Offers snapshot-over-window workflow, vercel.json, Vercel static deployment (serves committed HTML, no build step)

### Community 172 - "odoo_tabs.py"
Cohesion: 0.14
Nodes (21): _build(), catalog_rows(), default_window(), get_rows(), last_complete_week(), load_catalog(), offer_flags(), _ok() (+13 more)

### Community 173 - "_resolve_bag"
Cohesion: 0.29
Nodes (7): _apply_alias(), _monthly_bag_sales(), Resolve any bag wording → (canonical BOM bag type, cost or None, in_bom).…, Apply bag aliases, longest key first (so 'STANDARD TRAVEL' wins over…, {"months": ["Jun", …], "keys": ["2026-06", …], "bags": [{bag, category, stock,…, _resolve_bag(), price_of()

### Community 174 - "Product Performance — Shop breakdown: progress"
Cohesion: 0.22
Nodes (8): 1. Spec — DONE, 2. Data — DONE, 3. Page section — DONE, 4. Sidebar and sticky bar — DONE, 5. Visual check — DONE, 6. Wrap-up — DONE, Product Performance — Shop breakdown: progress, Summary

### Community 175 - "odoo_month_product_bags"
Cohesion: 0.33
Nodes (6): odoo_combo_product_bags(), odoo_lifetime_product_bags(), odoo_month_product_bags(), All-time bags per product from Odoo (no month window) — the lifetime sales of…, [(product name, bags)] for bags sold INSIDE combos (sub_product_line) in the…, Reporting month's bags per product from Odoo (Postgres), or None if the DB…

### Community 177 - "colours.py"
Cohesion: 0.36
Nodes (7): ({BAG: units}, {BAG: {colour: units}}) at CBD/Stock., warehouse_stock(), family(), _load(), _norm(), lib/colours.py — colour FAMILY of a product (Brown, Black, Red, Beige, Grey,…, Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…

### Community 178 - "run.py"
Cohesion: 0.36
Nodes (9): action_js(), edge_dump(), embedded(), inline_local(), js_str(), main(), Sticky-controls checks (docs/sticky-controls.md › Checks). python…, JS act(d, cb): optionally set a <select> (setv = "SEL=VALUE", fires change),… (+1 more)

### Community 179 - "Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)"
Cohesion: 0.20
Nodes (9): 1. Spec — DONE, 2. SQL + library — DONE, 3. Generator — DONE, 4. Page — DONE, 5. Actions — DONE, 6. Visual check — DONE, 7. Wrap-up — DONE, Findings (16 weeks, 28 Jun – 17 Oct 2026; last fully counted week 11–17 Oct) (+1 more)

### Community 180 - "base_name"
Cohesion: 0.33
Nodes (7): base_name(), dispatch_by_product_shop(), _num(), The catalogue key for an Odoo product name: norm() without the "[REJECT]" tag…, {NORM(product): {SHOP: bags}} of POS bag sales in [start, end]; None if DB…, {NORM(product): {SHOP: bags distributed in}} from combined_distribution.sql's…, sales_by_product_shop()

### Community 181 - "_combo_norm_option"
Cohesion: 0.38
Nodes (6): _combo_norm_option(), combos_by_shop(), _norm(), _tokmatch(), Per-shop view for Shops Efficiency, keyed by shop-location label (e.g.…, One combo slot-option → its distinctive bag token(s), colours/category words…

### Community 182 - "bags_on_offer.py"
Cohesion: 0.09
Nodes (23): _bag_tiers(), _base_windows(), _build_period(), _custom_range(), fmt(), inject(), main(), _offer_types() (+15 more)

### Community 183 - "Ads impact — on every page (21 Oct 2026, user's call)"
Cohesion: 0.33
Nodes (5): Actions ("what we can do"), Ads impact — on every page (21 Oct 2026, user's call), Figures, Refresh, What each page shows

### Community 184 - "reject_variants"
Cohesion: 0.33
Nodes (7): _parse_colour(), First primary colour token found in a name (longest-first), Title-cased; '' if…, Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share…, Per-[REJECT]-product variant rows for a name-filtered offer, for the filterable…, reject_variants(), _match_bag(), _singular_tokens()

### Community 185 - "os"
Cohesion: 0.08
Nodes (20): argparse, Shared Google Sheets authentication for every dashboard generator. Two modes,…, lib/new_products_list.py — which bag types count as this month's NEW PRODUCTS.…, doc(), lib/paths.py — where every kind of file lives. Use these instead of building…, openpyxl, openpyxl_comments, openpyxl_styles (+12 more)

### Community 186 - "_read_offers"
Cohesion: 0.40
Nodes (5): Offer type summary (matrix), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, _read_offers(), _read_offers_cache()

### Community 187 - "Ralph loop brief — Footfall and Marketing page"
Cohesion: 0.25
Nodes (7): DATA FACTS (verified 21 Oct 2026), DONE, ESCAPE HATCH, PROJECT RULES (must hold every iteration), Ralph loop brief — Footfall and Marketing page, SELF-CORRECTION, SUB-GOALS (do in order; tick each in notes/footfall_progress.md with the command output that proved it)

### Community 188 - "names"
Cohesion: 0.50
Nodes (4): _new_products(), This month's new products: data/new_products.txt (lib/new_products_list) — the…, names(), Upper-cased bag types from new_products.txt in file order ([] = no new…

### Community 189 - "run_query"
Cohesion: 0.33
Nodes (6): Run a read query and return a DataFrame, or None if the DB is unreachable.…, run_query(), expand(), Replace each POS_LINES(alias) with the fixed-lines subquery for that pos_order…, odoo_stock_at_location(), {UPPER(product name): on-hand units} at ONE exact internal location…

### Community 191 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 194 - "Bag Tracking"
Cohesion: 0.33
Nodes (5): Bag Tracking, Page, Prices, Stock, The bags

### Community 198 - "Sales-share targets per product"
Cohesion: 0.40
Nodes (4): Deliver, Sales-share targets per product, Steps, Tests

### Community 202 - "_match"
Cohesion: 0.50
Nodes (3): _match(), _full(), _full_of()

### Community 204 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 205 - "render"
Cohesion: 0.60
Nodes (5): growthData(), render(), drawGrowth(), table(), wf()

### Community 207 - "product_targets.py"
Cohesion: 0.11
Nodes (26): allocate(), available_days(), base_period(), build(), load_targets(), lib/product_targets.py — each month's units-to-sell target per bag, from Odoo…, (total units, info) — the month's Odoo target units, or (no Odoo targets yet)…, The three complete months before month_start → (start, end). (+18 more)

### Community 209 - "posting_yields.py"
Cohesion: 0.18
Nodes (12): load_dead_thresholds(), _mkt_perfect_week_index(), _mkt_week_label(), posting_yields.py…, STOCK_LEVELS: colour=A(0), product_name=C(2), Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]., current = {region: {key: {productName,colour,category,bagType,stock}}}. A new… (+4 more)

### Community 210 - "data"
Cohesion: 0.12
Nodes (18): cache_data, _db_count(), monthly_from_db(), Reporting month's subset count (e.g. rejectBags, giftBags) from…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,…, _live_bags(), _growth_tracking(), data/growth_tracking.json + the report month: live (so far + projected + this… (+10 more)

### Community 218 - "monthly_sales.py"
Cohesion: 0.32
Nodes (6): main(), month_window(), date, _query_ready(), monthly_sales.py — the current month's real bags sold, from Postgres. The…, First → last calendar day of the LIVE month (today's month; see…

### Community 220 - "marketing_posts.py"
Cohesion: 0.16
Nodes (21): _bag_category(), _category(), daily(), _date(), is_bag_level(), _load_backup(), _num(), parse() (+13 more)

## Knowledge Gaps
- **262 isolated node(s):** `PERF`, `graphify`, `Python environment`, `Use in another project`, `Test a skill` (+257 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1135 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **46 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_query()` connect `run_query` to `month_extras.py`, `lib/receipt_combos.py`, `current_performance.py`, `footfall.py`, `oos_callbacks.py`, `norm`, `lib/db.py`, `fetch_posting_data`, `check_connection`, `forward_projections.py`, `build_payload`, `shop_requests.py`, `shop_stock_levels.py`, `_combo_button_usage`, `_enrich_deals`, `product_performance.py`, `lib/report_month.py`, `chronos_train.py`, `stock.py`, `build_payload`, `_apply_receipt_offers`, `_enrich_deals`, `get_gspread_client`, `_resolve_bag`, `odoo_month_product_bags`, `runway_bags.py`, `shops_efficiency.py`, `excluded_products`, `weekly_sales.py`, `fetch_new_products_data`, `snapshot.py`, `_combo_button_usage`, `bag_tracking.py`, `bag_quant.py`, `product_targets.py`, `generators/self_made_combos.py`, `monthly_sales.py`, `odoo_marketing.py`, `negative_fixes.py`, `offer_picking.py`, `why_moved.py`, `_bags_not_on_offer`, `fetch`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `bag_classifier()` connect `bag_classifier` to `_apply_receipt_offers`, `oos_callbacks.py`, `Push Planner (`push_planner.py` → `push_planner.html`, `PP`)`, `push_planner.py`, `generators/self_made_combos.py`, `Bags on offer vs not on offer`, `fetch`, `Product (bag) targets`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `Bags on offer vs not on offer` connect `Bags on offer vs not on offer` to `oos_callbacks.py`, `lib/receipt_combos.py`, `_read_offers`, `shop-birthdays.md`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **What connects `PERF`, `graphify`, `Python environment` to the rest of the system?**
  _262 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `month_extras.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07474600870827286 - nodes in this community are weakly interconnected._
- **Should `laya.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._
- **Should `lib/receipt_combos.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._