# Graph Report - Marketing_dashboard  (2026-11-16)

## Corpus Check
- 251 files · ~1,296,531 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: .csv 14, (none) 2, .toml 1)

## Summary
- 2770 nodes · 5419 edges · 222 communities (174 shown, 48 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 198 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9d37a013`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- month_extras.py
- laya.py
- tests/test_receipt_combos.py
- oos_chip.js
- chart_switcher.js
- graw(block, key) function (bare numeric getter)
- Kitengela Rejects tracker (timed offer)
- publish.py
- tab_rows
- v5_theme.js
- name_match.py
- bare_minimum setting (weekly target floor)
- lib/offer_data.py
- self_made_combos_bundle/lib/db.py
- self_made_combos_bundle/lib/report_month.py
- run_query_cached
- forward_projections.py
- weeks
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
- fetch
- insights.html
- streamlit_app.py
- product_performance.py
- monthly_report.py
- anchor
- chronos_train.py
- odoo_stock_by_product
- build_payload
- Shops Efficiency Tracking spec doc
- _enrich_deals
- build
- push_rules.py
- page_sidebar.js
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- Combos & Power Deals by Shop panel (#combo-shop)
- self_made_combos_bundle/offer_data.py
- Self-made combos bundle Python dependencies (requirements.txt)
- CLAUDE.md
- history.py (read months back)
- Self-made combos vs Running combos portable bundle README
- type_fn
- compute_period
- Bags on offer vs not on offer
- algorithmic-art skill
- dataviz-charts skill
- scripts/test_receipt_combos.py
- excluded_products
- test_oos_callbacks.py
- High-End Visual Design skill
- _is_checked
- ads_panel.js
- fetch_new_products_data
- daydream skill (Vault Daydream)
- _fetch_monthly_kenya
- lib/db.py
- oos_callbacks.py
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- live_month_window
- signals
- marketing_dashboard.sql
- fetch_posting_data
- build
- shop_birthdays.py
- main
- Denri Africa Dashboard Design System (skill)
- shops_dispatch.py
- why_moved.js
- theme.py
- push_laya.py
- os
- facts
- _seasonality
- history.py
- _build_catalog
- test_push_planner.py
- test_share_targets.py
- test_stockout_demand.py
- README.md
- shop-birthdays.md
- bag_key_fn
- offer_kenya_posts
- self_made_combos_bundle/lib/__init__.py
- negative_fixes.py
- block
- Month-End Routine
- run_query
- Bag Signals — quant view of each bag (posting · stock · selling)
- attach_stock
- current_performance.html
- attach
- self_made_combos.py generator (build_payload + SQL + injection)
- build
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- build
- reject_variants
- Ralph task — only three sheet tabs left
- check_connection
- Bag targets October 2026_3acbad00.md
- _growth_tracking
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- _bags_not_on_offer
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- bag_classifier
- fetch
- What the page shows
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- Product (bag) targets
- POST_DATA data block (Posting)
- followup
- read_block(file, start, end) function
- generator
- last_week_from_db
- generate_insights.py
- contextlib
- Chart type switcher (every chart, every menu)
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- New Products Analytics (doc)
- _combo_button_usage
- Offer Picking (doc)
- start_server
- build
- timed_offers.py (generator)
- scripts/receipt_combos.py
- _dead_stock_region
- new_products.py
- _bucket
- _bg_rebuild
- Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)
- Ralph task — "Out of stock — call back" demand per shop
- update_np_weekly_history
- _alignment_region
- odoo_marketing_audit.py
- Footfall and Marketing (21 Oct 2026, user's call)
- num
- Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)
- odoo_tabs.py
- design-taste-frontend (anti-slop frontend skill)
- Product Performance — Shop breakdown: progress
- build
- Out-of-stock demand — people, not requests
- family
- Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)
- corporate_clients_from_db
- _read_offers
- bags_on_offer.py
- _bg_jobs
- _bag_tiers
- posting_yields.py
- _build_period
- Ralph loop brief — Footfall and Marketing page
- Offers
- master_products
- Bag signals — quant finance applied to product sales
- ambiguous_python_import_17686b6faac5
- _kind
- Bag Tracking
- test_sheet_reads.py
- data
- monthly_target_rows
- month_end_lift
- build
- Combos from receipts — running vs self-made
- render
- load_lines
- realistic_rates
- safe_int
- main
- sendable_by_month_end
- load_data
- names
- Odoo marketing data audit
- ODOO_MARKETING_AUDIT.md
- _analyze_region
- new_bags
- test_product_targets.py
- categories
- posts_between
- lib

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 89 edges
2. `fetch()` - 41 edges
3. `data()` - 40 edges
4. `fetch_posting_data()` - 38 edges
5. `check_connection()` - 34 edges
6. `get_gspread_client()` - 32 edges
7. `build_payload()` - 30 edges
8. `excluded_products()` - 26 edges
9. `build()` - 25 edges
10. `build_payload()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `Bulk orders` --references--> `offer_days()`  [INFERRED]
  docs/product-performance.md → generators/product_performance.py
- `The split — by each bag's share of recent sales` --references--> `bag_classifier()`  [INFERRED]
  docs/product-targets.md → generators/self_made_combos.py
- `Inputs (read only — nothing is written to Odoo or the sheet)` --references--> `bag_classifier()`  [INFERRED]
  docs/push-planner.md → generators/self_made_combos.py
- `Laya's second opinion (`lib/push_laya.py`)` --references--> `state_text()`  [INFERRED]
  docs/push-planner.md → lib/push_laya.py
- `Why it isn't moving — reasons, per market (`push_rules.reasons`)` --references--> `reasons()`  [INFERRED]
  docs/push-planner.md → lib/push_rules.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Self-made combos bundle: generator, Sheets auth, DB access, and dependency manifest working together to build the combos page** — export_self_made_combos_bundle_self_made_combos_py, export_self_made_combos_bundle_offer_data_py, export_self_made_combos_bundle_google_auth_py, export_self_made_combos_bundle_lib_db_py, export_self_made_combos_bundle_requirements [EXTRACTED 0.90]
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]

## Communities (222 total, 48 thin omitted)

### Community 0 - "month_extras.py"
Cohesion: 0.07
Nodes (50): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, _bags_on_offer(), _block(), build_extras() (+42 more)

### Community 1 - "laya.py"
Cohesion: 0.09
Nodes (26): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket() (+18 more)

### Community 2 - "tests/test_receipt_combos.py"
Cohesion: 0.06
Nodes (59): What the page shows (per period), _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, _fill_units(), _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region… (+51 more)

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
Cohesion: 0.12
Nodes (25): fnmatch, action_js(), main(), node_check(), Run the sticky-controls checks on every wired page and print the markdown…, edge_dump(), embedded(), inline_local() (+17 more)

### Community 8 - "tab_rows"
Cohesion: 0.14
Nodes (18): _bag_category(), _category(), daily(), _date(), _load_backup(), _num(), parse(), posts() (+10 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 12 - "lib/offer_data.py"
Cohesion: 0.07
Nodes (34): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, ({PRODUCT: {SHOP CODE: units}}, {PRODUCT: {SHOP CODE: [[colour, units], …]}})…, shop_sales(), Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer…, _read_offer_analysis(), _aliases(), build_rows() (+26 more)

### Community 13 - "self_made_combos_bundle/lib/db.py"
Cohesion: 0.15
Nodes (18): check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, Run a read query and return a DataFrame, or None if the DB is unreachable.… (+10 more)

### Community 14 - "self_made_combos_bundle/lib/report_month.py"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 15 - "run_query_cached"
Cohesion: 0.20
Nodes (12): odoo_list_price(), {BAG_UP: incl-tax Sales Price} — the product's normal price ("was"), the…, _cache_path(), run_query with a TTL disk cache. Identical to run_query for callers, but a…, run_query_cached(), base_name(), dispatch_by_product_shop(), _num() (+4 more)

### Community 16 - "forward_projections.py"
Cohesion: 0.07
Nodes (15): fetch_monthly_target(), current_performance.py…, fetch_sheet_data(), fmt_opt_pct(), fmt_pct(), _orow(), forward_projections.py…, One table row, month-end projected. expected = what the targets expect from… (+7 more)

### Community 17 - "weeks"
Cohesion: 0.12
Nodes (16): Actions ("what we can do"), Ads impact — on every page (21 Oct 2026, user's call), Charts (21 Oct 2026, user's call), Figures, Refresh, ser(), campaigns(), _f() (+8 more)

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
Cohesion: 0.15
Nodes (19): _onoff(), Shop requests vs received (this month · last month) and the production approved…, requests_block(), _d(), _f(), _match(), _offer_label(), _pct() (+11 more)

### Community 22 - "main.py"
Cohesion: 0.12
Nodes (21): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, Denri Africa — Marketing Dashboard Launcher… (+13 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.14
Nodes (18): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+10 more)

### Community 24 - "shop_stock_levels.py"
Cohesion: 0.14
Nodes (24): bag_categories(), build(), dispatch_shop(), fit(), grand_total(), leads(), needs(), _next_month() (+16 more)

### Community 25 - "build"
Cohesion: 0.28
Nodes (16): build(), acts(), campaign_table(), money(), chart_data(), cpr(), focus_tiles(), market_table() (+8 more)

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

### Community 30 - "fetch"
Cohesion: 0.14
Nodes (15): Counted by how it was sold, _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…, _bags_not_on_offer(), fetch(), fmt() (+7 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.08
Nodes (18): cache_data, SCRIPT_TIMEOUT = 600s config, hashlib, html, streamlit, _load_secrets_into_env(), _month_archived(), _month_end_running() (+10 more)

### Community 33 - "product_performance.py"
Cohesion: 0.17
Nodes (13): corp(), corporate_period(), _month_end(), _month_start(), periods(), product_performance.py — the Product Performance page: % share of the top-…, {period: (cur start, cur end, prev start, prev end, label)} — each compared…, {power, combo:[labels], dow:[{tier, shops}], timed:[{name, s, e, was, now}]}… (+5 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.12
Nodes (15): _bag_stock(), _cause(), _combo_bags(), esc(), fmt(), ladder_strip(), _norm_bag(), pct() (+7 more)

### Community 35 - "anchor"
Cohesion: 0.27
Nodes (10): count_complete_weeks_in_month(), Count Mon–Sun weeks in the reporting month that have ≥5 days falling within it., anchor(), month_key(), month_name(), month_window(), date, The date whose month is the reporting month: yesterday, unless pinned. Pinned… (+2 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.13
Nodes (26): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+18 more)

### Community 37 - "odoo_stock_by_product"
Cohesion: 0.14
Nodes (15): odoo_stock_kenya_outside(), ({UPPER name: kenya on-hand}, {UPPER name: outside on-hand}) — live Odoo stock.…, odoo_stock_levels(), Live per-shop Odoo on-hand in the SAME shape parse_sheet(STOCK_LEVELS) returns:…, {NORM(product): {SHOP: on-hand}} live, Kenya shops + Sinza (DAR) + Uganda (UG)., stock_by_product_shop(), _codes_for(), odoo_stock_by_product() (+7 more)

### Community 38 - "build_payload"
Cohesion: 0.12
Nodes (18): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+10 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "_enrich_deals"
Cohesion: 0.07
Nodes (26): _as_day(), dow_tier_weeks(), _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg() (+18 more)

### Community 41 - "build"
Cohesion: 0.13
Nodes (19): build(), _add(), launch_curve(), _cfg(), _day_expr(), first_sale(), load_categories(), load_prices() (+11 more)

### Community 42 - "push_rules.py"
Cohesion: 0.11
Nodes (24): Actions (one per bag × market, then ranked), build_actions(), Adds action / says / units / confidence / score to each facts row; returns…, action(), _cover_txt(), moves(), _n(), posting_median() (+16 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.15
Nodes (14): Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Per bag × market: the facts (`push_rules.facts`, `add_peers`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+6 more)

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

### Community 51 - "type_fn"
Cohesion: 0.15
Nodes (18): load_posts(), num(), tally(), ({BAG: [kenya, outside]} last week, {BAG: [kenya, outside]} this month) from…, build(), {TYPE: {"kes", "shops": {SHOP: {"n", "kes"}}}} for the runway types over…, ({TYPE: Kenya shop on-hand}, {TYPE: Sinza + Uganda on-hand}) — live Odoo., The NP.runway payload: {days, bags: [{name, created, category, stockKe,… (+10 more)

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

### Community 57 - "excluded_products"
Cohesion: 0.11
Nodes (18): corporate_return(), market_sales(), posts_by_market(), posts_lead_sales(), ads_impact.py — the Ads impact panel shown on every page (spec: docs/ads-…, {market: {bags, kes, orders}} over [start, end]., {market: [posts per week]} from marketing's posting sheets; None if they can't…, Kenya bag types: change in posts one week vs change in bags sold the next,… (+10 more)

### Community 58 - "test_oos_callbacks.py"
Cohesion: 0.22
Nodes (16): aggregate(), flat(), split(), The page block: {period: {key: {"total": people, "shops": [[shop, people],…, pytest, _kai(), Tests for lib/oos_callbacks.py (WhatsApp "Out of stock — call back" demand).…, test_attach_stock_per_shop_and_colour() (+8 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "_is_checked"
Cohesion: 0.18
Nodes (17): _build_no_convert(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int(), _is_checked(), _is_x() (+9 more)

### Community 61 - "ads_panel.js"
Cohesion: 0.22
Nodes (16): act(), axes(), cell(), charts(), drawCmp(), drawWow(), values(), esc() (+8 more)

### Community 62 - "fetch_new_products_data"
Cohesion: 0.15
Nodes (18): fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_combo_product_bags() (+10 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "_fetch_monthly_kenya"
Cohesion: 0.23
Nodes (12): _fetch_monthly_kenya(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), Monthly Kenya figures for the S1 KPI cards. MONTHLY_MARKETING_POST: sum col E…, MONTHLY_SALES: colour=A(0), product_name=B(1), MONTHLY_MARKETING_POST: colour=A(0), product_name=C(2) (+4 more)

### Community 65 - "lib/db.py"
Cohesion: 0.11
Nodes (23): push_planner.py — Push Planner: what to push this week, where, and why bags…, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, lib/footfall.py — footfall (visitors counted per shop per day) joined to walk-…, lib/pos_lines.py — till lines with refunded combos fixed (docs/README.md ›…, _age_min(), _cleanup(), fresh_meta(), _meta() (+15 more)

### Community 66 - "oos_callbacks.py"
Cohesion: 0.16
Nodes (17): _date(), load_rows(), _online_rows(), oos_by_bag_shop(), lib/oos_callbacks.py — "Out of stock — call back" demand, ONLINE and WALK-IN.…, {shop: set(person)} → (distinct people, [[shop, people], …] high → low)., {period: {key: people}} from an aggregate() block., {period: {product name: {shop: people}}} straight from Odoo names, or {} if… (+9 more)

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.15
Nodes (12): Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Page, Production — shop requests vs approved list (18 Oct 2026), Requests by category (18 Oct 2026), Shop requests and Production — Region / Shop filter and tiles (19 Oct 2026), Shop requests — realistic performance (26 Oct 2026, user's call) (+4 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "live_month_window"
Cohesion: 0.19
Nodes (13): odoo_weekly_breakdown(), Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, build(), load_targets(), (rows, total, base start, base end) for the month, from Odoo., {BAG: target units} for the month from product_targets_<YYYY-MM>.csv (built…, {BAG: col C} from MONTHLY_TARGET — for the comparison column only., _sheet_targets() (+5 more)

### Community 71 - "signals"
Cohesion: 0.17
Nodes (16): action(), _mean(), _phi(), posting_beta(), The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json…, _sd() (+8 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "fetch_posting_data"
Cohesion: 0.12
Nodes (15): _bt_on_offer(), _dead_clear(), fetch_posting_data(), _clear(), _yield(), _fold_bag_level(), load_dead_thresholds(), _post_yield() (+7 more)

### Community 74 - "build"
Cohesion: 0.11
Nodes (20): actions(), build(), agg(), week_tot(), num(), pearson(), What we can do' — by rule (docs/footfall-marketing.md › Actions). Each names a…, JSON-safe number: NaN / None → None. (+12 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.09
Nodes (34): read_block(), _offer_bagtypes_by_region(), On-offer bag types per region, read from self_made_combos.html's SMC block:…, _kenya_target(), month_progress(), payload(), Kenya's month target from current_performance.html (PERF.totalTarget), or None., Per market: sold this month so far (from the daily sales), days elapsed / left,… (+26 more)

### Community 76 - "main"
Cohesion: 0.25
Nodes (8): build_facts(), build_reasons(), inject(), main(), Facts for every bag × market that has stock or sold in the window…, Adds notMoving + reasons to every row (lib/push_rules.reasons). Returns the…, not_moving(), A bag with stock that isn't clearing: cleared < 30% this month, or > 45 days of…

### Community 77 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.17
Nodes (13): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), Signature Element — Flowing Border (achievement cards), high-end-visual-design (related skill), KPI Tile component (+5 more)

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

### Community 82 - "os"
Cohesion: 0.10
Nodes (19): One-off: restore August's Offer Type figures into monthly_report_history.json…, generators/bag_tracking.py — Bag Tracking: the chosen bags' Kenya shop stock at…, offer_picking.py…, Save a local, human-editable copy of the offers prices to OFFERS_CACHE., _write_offers_cache(), Reject Sale pricing (Kitengela) → reject_sales.html (payload `RJ`). A…, json, openpyxl (+11 more)

### Community 83 - "facts"
Cohesion: 0.21
Nodes (12): _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, day(), ISO date n days before END (0 = END)., test_days_cover_is_none_when_nothing_sold(), test_first_sold_days_ago(), test_momentum_up_down_and_from_zero() (+4 more)

### Community 84 - "_seasonality"
Cohesion: 0.15
Nodes (16): Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), _build_sheet_slots(), _combo_norm_option(), _combo_odoo_slots(), _combo_sheet_slots() (+8 more)

### Community 85 - "history.py"
Cohesion: 0.13
Nodes (21): dotenv, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers… (+13 more)

### Community 86 - "_build_catalog"
Cohesion: 0.33
Nodes (7): _build_catalog(), _is_full_price(), Letters and digits only, so 'CODE3' meets 'CODE 3' and 'FANNYPACK(N)' meets…, {_staff_key(catalogue bag type): staff price} from staff_prices.json (a 0 = no…, Every bag the user can pick for a slot, with two prices from the offers sheet:…, _read_staff_prices(), _staff_key()

### Community 87 - "test_push_planner.py"
Cohesion: 0.16
Nodes (25): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m…, A facts row with sensible defaults, overridden by kw. (+17 more)

### Community 88 - "test_share_targets.py"
Cohesion: 0.22
Nodes (11): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+3 more)

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "README.md"
Cohesion: 0.17
Nodes (7): Agent skills — retail analytics, Test a skill, Use in another project, Deliver, Sales-share targets per product, Steps, Tests

### Community 91 - "shop-birthdays.md"
Cohesion: 0.15
Nodes (11): Design Tokens (colors, typography, spacing), Semantic color rules (green=good, amber=risk, red=critical, cyan=info), Analytics Dashboard specific rules (VISUAL_DENSITY: dense), Shop birthdays, Shop → opening date, Where it shows, Per-shop combo-button chips (red when < half best-in-region), Region colour palette (reference for Executive Dashboard) (+3 more)

### Community 92 - "bag_key_fn"
Cohesion: 0.11
Nodes (21): build(), Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), _odoo_post_check(), load(), (daily, total, stock, launch, start, end) for Kenya from Odoo; daily per bag…, followers_daily(), meta_posts_by_bag() (+13 more)

### Community 93 - "offer_kenya_posts"
Cohesion: 0.14
Nodes (14): Kenya timed-offer campaigns from timed_offers_config.json (normalised by…, _timed_offers(), _bags_from_file(), _derive_month(), load_config(), _norm_offer(), offer_kenya_posts(), post_window() (+6 more)

### Community 94 - "self_made_combos_bundle/lib/__init__.py"
Cohesion: 0.08
Nodes (33): calendar, collections, csv, datetime, lib — shared data-access for the marketing dashboard (Postgres migration).…, footfall_marketing.py — Footfall and Marketing page (spec: docs/footfall-…, monthly_sales.py — the current month's real bags sold, from Postgres. The…, _bag_sales_daily_sql() (+25 more)

### Community 95 - "negative_fixes.py"
Cohesion: 0.08
Nodes (34): argparse, _negfix(), Stock record accuracy per shop for every period (docs/shops-efficiency.md ›…, bags_sold(), block(), by_shop(), _date(), _int() (+26 more)

### Community 96 - "block"
Cohesion: 0.15
Nodes (13): block(), from_argv(), label(), load(), month_share(), path(), (from, to) dates for the page's Custom period, or None. Swapped if reversed;…, Write the range, or with a=None delete it (Clear). (+5 more)

### Community 97 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

### Community 98 - "run_query"
Cohesion: 0.08
Nodes (27): corporate_target_from_db(), This month's Odoo corporate target {bags, kes} (sales_pos_target, scope…, _corporate_lines(), Average POS bags per weekday (0 = Mon) over s..e (bags_sold_daily.sql). None if…, The corporate app bags behind _corporate_bags(), one row per product with its…, _weekday_base(), apply_walkins(), _drop_shared_conn() (+19 more)

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "attach_stock"
Cohesion: 0.19
Nodes (13): col(), attach_stock(), in_stock(), stk(), collect(), _in(), is_combo_request(), {period: (start, end)} for the dated periods (lifetime / current are undated).… (+5 more)

### Community 101 - "current_performance.html"
Cohesion: 0.50
Nodes (4): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance)

### Community 102 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 103 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.29
Nodes (7): lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, lib/report_month.py (which month are we reporting?), self_made_combos.html static page (reads const SMC), self_made_combos.py generator (build_payload + SQL + injection)

### Community 104 - "build"
Cohesion: 0.15
Nodes (17): _alt_cost(), build(), _combo_cost(), _combo_slots(), _monthly_bag_sales(), _next_month(), bag(), Parse `const SMC = {…}` out of self_made_combos.html (no DB round-trip). (+9 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "build"
Cohesion: 0.08
Nodes (33): why_moved(), _load_shop_regions(), Shop → Region from docs/shop-regions.md (lib/shop_regions); the built-in…, doc(), day_for(), load(), [{"till", "shop", "from", "to", "asDate"}] — datetimes / dates parsed; [] if…, The day a till's sales of `day` count on (day granularity). (+25 more)

### Community 107 - "reject_variants"
Cohesion: 0.12
Nodes (17): kenya_stock_by_bag(), _parse_colour(), {BAG_UPPER: category} — the bag's category label only, from the product…, {BAG_UPPER: units} — physical stock summed per BAG TYPE from a repo CSV's UNITS…, First primary colour token found in a name (longest-first), Title-cased; '' if…, Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share…, Per-[REJECT]-product variant rows for a name-filtered offer, for the filterable…, {BAG_UPPER: {stock, category}} for the configured bags. STOCK is LIVE Kenya… (+9 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "check_connection"
Cohesion: 0.08
Nodes (25): corporate_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, _corporate_bags(), The month's revenue target (KES): Odoo sales_pos_target amount (pos +…, (corporate bags, corporate KES received) in the given month, live from Odoo…, _revenue_target(), build_offer(), odoo_bag_daily_value() (+17 more)

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "_growth_tracking"
Cohesion: 0.33
Nodes (6): _growth_tracking(), data/growth_tracking.json + the report month: live (so far + projected + this…, is_pinned(), _pinned(), (year, month) from DENRI_REPORT_MONTH=YYYY-MM, or None when unset/invalid., True when DENRI_REPORT_MONTH pins the month (a deliberate rebuild).

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 114 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 121 - "bag_classifier"
Cohesion: 0.17
Nodes (15): Buckets, _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _norm_combo() (+7 more)

### Community 122 - "fetch"
Cohesion: 0.13
Nodes (25): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), combo_slots(), make_classifier() (+17 more)

### Community 123 - "What the page shows"
Cohesion: 0.18
Nodes (11): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 2b. Shop breakdown (22 Oct 2026, user's call), 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Bulk orders, Data (+3 more)

### Community 126 - "Product (bag) targets"
Cohesion: 0.25
Nodes (8): A month with only a revenue target (November 2026), Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 128 - "followup"
Cohesion: 0.18
Nodes (13): Did last week's calls work? (`push_rules.record_week`, `followup`), Last week's calls checked against what happened (lib/push_rules.followup), then…, weekly(), followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., Store this week's top actions under its Sunday. Re-running in the same week…, The most recent PREVIOUS week's calls and what happened since: sold/day since…, record_week() (+5 more)

### Community 130 - "generator"
Cohesion: 0.17
Nodes (12): generator(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, start_daily_snapshot(), clear_timed_offers(), main(), YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that… (+4 more)

### Community 131 - "last_week_from_db"
Cohesion: 0.25
Nodes (8): last_week_from_db(), Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary(), week_start_of(), weekly_from_db()

### Community 132 - "generate_insights.py"
Cohesion: 0.24
Nodes (5): card(), esc(), fmt(), generate_insights.py…, region_card()

### Community 138 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.22
Nodes (7): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does, Current Performance (doc)

### Community 145 - "Shop Launch"
Cohesion: 0.18
Nodes (10): Config, Launch day, Marketing posts, Prices (30 Oct 2026, user's call), Race lines, sales by day, product performance, folding (9 Nov 2026, user's call), Sales, Sales keyed in late (9 Nov 2026, user's call), Shop Launch (+2 more)

### Community 153 - "New Products Analytics (doc)"
Cohesion: 0.14
Nodes (16): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Bag-type matching for combo components (_match_bag / BAG_ALIASES), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES) (+8 more)

### Community 154 - "_combo_button_usage"
Cohesion: 0.14
Nodes (11): _combo_button_usage(), _matches_sheet(), _opt_close(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Same slot count and every slot overlaps under SOME pairing (any order: the…, The sheet label this Odoo combo maps to, or None if it isn't on the sheet.…, _slots_fit() (+3 more)

### Community 155 - "Offer Picking (doc)"
Cohesion: 0.22
Nodes (10): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Combo button usage / rung vs pot. (till check), Self-made combos vs running combos (export bundle copy) (+2 more)

### Community 156 - "start_server"
Cohesion: 0.31
Nodes (8): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_to_config(), _json()

### Community 157 - "build"
Cohesion: 0.15
Nodes (12): {BAG TYPE (upper): production cost} from bom_costs.json — the local copy of the…, _read_bom_costs(), _assign_price(), _bom_costs(), build(), reject_stock.csv → {BAG (upper): {units, colours:{COLOUR: units}}}., (price, flag) from BOM cost — two tiers. flag ∈ {'', 'thin', 'below', 'nobom'}., Write an Excel (xlsx, or CSV fallback) of EVERYTHING on the pricing board —… (+4 more)

### Community 158 - "timed_offers.py (generator)"
Cohesion: 0.09
Nodes (22): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+14 more)

### Community 159 - "scripts/receipt_combos.py"
Cohesion: 0.33
Nodes (5): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…

### Community 160 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 161 - "new_products.py"
Cohesion: 0.18
Nodes (7): _base_colour(), _merge_rows_by_base_colour(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across…, _strip_colour_qualifiers()

### Community 162 - "_bucket"
Cohesion: 0.19
Nodes (12): _acc(), _bucket(), build_compare(), _cmp_lines(), _days(), _kenya_net_moves_since(), _offer_compare(), Which configured bag (if any) an Odoo/​sheet product name belongs to, by… (+4 more)

### Community 163 - "_bg_rebuild"
Cohesion: 0.40
Nodes (6): _bg_rebuild(), work(), Seconds the last good `kind` rebuild of `lbl` took (any kind as a fallback),…, Rebuild `lbl` in the background. kind: "auto" (skipped if a rebuild was tried…, _rebuild_secs(), _save_rebuild_secs()

### Community 165 - "Ralph task — "Out of stock — call back" demand per shop"
Cohesion: 0.25
Nodes (7): match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, Established facts (do not re-investigate), Every iteration, Periods (dates in Africa/Nairobi), Ralph task — "Out of stock — call back" demand per shop, Stopping

### Community 166 - "update_np_weekly_history"
Cohesion: 0.29
Nodes (7): _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)., Ordinal among the month's perfect weeks (>=5 days in month), so the first FULL…, Snapshot each Sun–Sat week (sales, Kenya/Outside posts) into…, update_np_weekly_history()

### Community 167 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 168 - "odoo_marketing_audit.py"
Cohesion: 0.39
Nodes (8): root(), audit(), _expected(), main(), _period(), _range(), scripts/odoo_marketing_audit.py — how complete and up to date each marketing…, _step()

### Community 169 - "Footfall and Marketing (21 Oct 2026, user's call)"
Cohesion: 0.20
Nodes (9): Actions (rules), Correlations ("Posts and ads vs visitors"), Data traps (said on the page), Definitions, Footfall and Marketing (21 Oct 2026, user's call), Regenerate, Shop mapping (`lib/footfall.SHOPS`), Sources (+1 more)

### Community 170 - "num"
Cohesion: 0.20
Nodes (11): _garr_line(), gnum(), num(), _offers(), _parse_offers(), _units(), This month's timed-offer campaigns, flattened for storage. The live TO payload…, Greedy single-line array extractor — handles nested [[...],[...]] arrays. (+3 more)

### Community 172 - "odoo_tabs.py"
Cohesion: 0.10
Nodes (22): load(), metric_byshop(), parse_sheet(), shops_efficiency.py…, Return (data, meta) for the Kenya shops, locating columns by header name…, safe_int(), update_history(), lib — shared data-access for the marketing dashboard (Postgres migration).… (+14 more)

### Community 173 - "design-taste-frontend (anti-slop frontend skill)"
Cohesion: 0.18
Nodes (12): design-taste-frontend (related skill), design-taste-frontend (anti-slop frontend skill), Brief-First Process (8-step design workflow), Hard Bans (typography, color, layout, code, content clichés), Pre-Flight Checklist (90+ items), Redesign Protocol (upgrading existing UI), Three Dials — DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, Three AI-generated design clusters (calibration reference) (+4 more)

### Community 174 - "Product Performance — Shop breakdown: progress"
Cohesion: 0.22
Nodes (8): 1. Spec — DONE, 2. Data — DONE, 3. Page section — DONE, 4. Sidebar and sticky bar — DONE, 5. Visual check — DONE, 6. Wrap-up — DONE, Product Performance — Shop breakdown: progress, Summary

### Community 175 - "build"
Cohesion: 0.21
Nodes (11): build(), explain(), _fmt_d(), offer_days(), Start-of-week stock, units dispatched in, biggest delivery, days in stock for…, {period: {BAG: {...}}} — for EVERY bag sold in Kenya in the period: Kenya walk-…, {lw, pw, lwNb, pwNb, head, lines:[[group, dir, text]]} for bag b in market mkt…, (start, end) → {bag: {"clicks", …}} website WhatsApp taps, one Odoo pull per… (+3 more)

### Community 177 - "Out-of-stock demand — people, not requests"
Cohesion: 0.29
Nodes (7): Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods, Show it as, Tests

### Community 178 - "family"
Cohesion: 0.18
Nodes (12): buffer_stock(), ({SHOP: {BAG: units}}, {SHOP: {BAG: {colour: units}}}) — on hand in the shops…, ({BAG: units}, {BAG: {colour: units}}) at CBD/Stock., {location: {BAG: units}} at CBD/Stock and VLD/Stock (exact locations)., shop_stock(), warehouse_stock(), family(), _load() (+4 more)

### Community 179 - "Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)"
Cohesion: 0.20
Nodes (9): 1. Spec — DONE, 2. SQL + library — DONE, 3. Generator — DONE, 4. Page — DONE, 5. Actions — DONE, 6. Visual check — DONE, 7. Wrap-up — DONE, Findings (16 weeks, 28 Jun – 17 Oct 2026; last fully counted week 11–17 Oct) (+1 more)

### Community 180 - "corporate_clients_from_db"
Cohesion: 0.40
Nodes (6): corporate_clients_from_db(), _months(), A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],…, Current month's corporate activity per client (quoted · invoiced · paid · sold)…, _txt()

### Community 181 - "_read_offers"
Cohesion: 0.20
Nodes (10): Offer type summary (matrix), _apply_alias(), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, Apply bag aliases, longest key first (so 'STANDARD TRAVEL' wins over…, _read_offers(), _read_offers_cache(), _category_of() (+2 more)

### Community 182 - "bags_on_offer.py"
Cohesion: 0.26
Nodes (11): _base_windows(), _custom_range(), fmt(), inject(), main(), bags_on_offer.py…, (from, to) dates from boo_custom_range.json — the Custom period — or None., Write (or with a=None, delete) the Custom period's dates. (+3 more)

### Community 183 - "_bg_jobs"
Cohesion: 0.25
Nodes (8): cache_resource, fragment, _bg_done_msg(), _bg_jobs(), _bg_watch(), _fmt_secs(), Background rebuilds shared by every session: label → job (see _bg_rebuild)., The refresh_msg for a finished background rebuild (None: the job vanished).

### Community 184 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

### Community 185 - "posting_yields.py"
Cohesion: 0.08
Nodes (25): _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., _mkt_perfect_week_index(), _mkt_week_label(), posting_yields.py…, Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]. (+17 more)

### Community 186 - "_build_period"
Cohesion: 0.18
Nodes (6): _build_period(), _offer_types(), _pick_target(), Latest target row for `shop` with this period that overlaps [start, end]. A…, Matrix payload: rows, per-row category / tier cells, and the period's Top-5…, _region_of()

### Community 187 - "Ralph loop brief — Footfall and Marketing page"
Cohesion: 0.25
Nodes (7): DATA FACTS (verified 21 Oct 2026), DONE, ESCAPE HATCH, PROJECT RULES (must hold every iteration), Ralph loop brief — Footfall and Marketing page, SELF-CORRECTION, SUB-GOALS (do in order; tick each in notes/footfall_progress.md with the command output that proved it)

### Community 188 - "Offers"
Cohesion: 0.24
Nodes (6): _load_json(), Offers, Kenya offers per day (each day reads its own month's bags_offer_source file) +…, {mkt: {BAG: [text]}} for Sinza / Uganda from offers_monthly.csv., _offers(), Offers lookup (Kenya) — or None when the offer data can't be loaded.

### Community 189 - "master_products"
Cohesion: 0.50
Nodes (4): master_products(), _norm_name(), Match the SQL normalisation: lower-case, '.'→space, collapse whitespace., Normalised, de-duplicated master catalogue names (master_products.txt), for the…

### Community 191 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 193 - "_kind"
Cohesion: 0.67
Nodes (3): _kind(), HANDBAG' → 'handbags', 'SCHOOL BAG' → 'school bags', 'SPORT' → 'sport bags', ''…, test_kind_wording()

### Community 194 - "Bag Tracking"
Cohesion: 0.33
Nodes (5): Bag Tracking, Page, Prices, Stock, The bags

### Community 195 - "test_sheet_reads.py"
Cohesion: 0.47
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 197 - "data"
Cohesion: 0.11
Nodes (21): _db_count(), monthly_from_db(), Reporting month's subset count (e.g. rejectBags, giftBags) from…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,…, _live_bags(), _perfect_week_index(), Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, update_weekly_history() (+13 more)

### Community 198 - "monthly_target_rows"
Cohesion: 0.22
Nodes (8): get(), bag_posts(), tally(), {BAG: (posts this month, posts last week)} — Kenya posts (col E) from the two…, key(), monthly_target_rows(), MONTHLY_TARGET rows with column C = the bag's target from Odoo (docs/product-…, test_monthly_target_rows_swaps_column_c()

### Community 200 - "month_end_lift"
Cohesion: 0.25
Nodes (8): Bag health (by bag, 18 Oct 2026), Next month (preparedness) — from the 15th, November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026), Product rating and core 5 vs other 13 categories (18 Oct 2026), Sales pace to month end (19 Oct 2026), Stocks report, month_end_lift(), How much faster the shops sell in the rest of the month than before it, from…

### Community 203 - "build"
Cohesion: 0.29
Nodes (8): build(), _cfg(), _colour(), _folder(), canon(), _moves(), Odoo product name → the dashboard's bag name (Offer Picking's _build_catalog…, _inlist()

### Community 204 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 205 - "render"
Cohesion: 0.60
Nodes (5): growthData(), render(), drawGrowth(), table(), wf()

### Community 207 - "load_lines"
Cohesion: 0.29
Nodes (7): _d(), load_lines(), _market(), _num(), float, with None / NaN as 0., ({mkt: {BAG: now}}, {mkt: {BAG: {date: end-of-day level}}}, {mkt: {BAG: {date:…, stock_facts()

### Community 208 - "realistic_rates"
Cohesion: 0.53
Nodes (6): _clamp(), ({SHOP: {BAG: units a week}}, {SHOP: {"recent", "season", "growth"}}) — recent…, realistic_rates(), growth(), season(), tot()

### Community 209 - "safe_int"
Cohesion: 0.40
Nodes (5): _bag_level_bags(), Bag types with posts logged without a colour in any of the posting tabs., safe_int(), is_bag_level(), A tab_rows() row of posts with no colour (from the bag type's TOTAL row):…

### Community 210 - "main"
Cohesion: 0.33
Nodes (5): main(), month_window(), date, _query_ready(), First → last calendar day of the LIVE month (today's month; see…

### Community 211 - "sendable_by_month_end"
Cohesion: 0.50
Nodes (4): {shop: units} — `left` units shared over {shop: gap} in proportion, leftovers…, What can still be sent (docs › Shop requests — realistic performance): per shop…, sendable_by_month_end(), _share_out()

### Community 212 - "load_data"
Cohesion: 0.40
Nodes (5): load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if…, _till_to_shop()

### Community 213 - "names"
Cohesion: 0.50
Nodes (4): _new_products(), This month's new products: data/new_products.txt (lib/new_products_list) — the…, names(), Upper-cased bag types from new_products.txt in file order ([] = no new…

### Community 216 - "_analyze_region"
Cohesion: 0.50
Nodes (4): _analyze_region(), STOCK_LEVELS: colour=A(0), product_name=C(2), Runs all three posting sections for one region. sales_col – column index in…, _sl_key()

### Community 217 - "new_bags"
Cohesion: 0.67
Nodes (3): What each page shows, new_bags(), Bags launched inside the base period (the bag-targets CSV's Launch column).

### Community 218 - "test_product_targets.py"
Cohesion: 0.16
Nodes (15): allocate(), available_days(), base_period(), The three complete months before month_start → (start, end)., Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, _add_months(), _d() (+7 more)

### Community 220 - "posts_between"
Cohesion: 0.67
Nodes (3): posts_between(), fn(), fn(start, end) → {BAG: {"KE", "TZ", "UG": posts}} from marketing's daily…

## Knowledge Gaps
- **261 isolated node(s):** `PERF`, `graphify`, `Python environment`, `Use in another project`, `Test a skill` (+256 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1141 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_query()` connect `run_query` to `month_extras.py`, `tests/test_receipt_combos.py`, `last_week_from_db`, `lib/offer_data.py`, `run_query_cached`, `forward_projections.py`, `build_payload`, `shop_requests.py`, `shop_stock_levels.py`, `_combo_button_usage`, `_combo_button_usage`, `_enrich_deals`, `fetch`, `product_performance.py`, `chronos_train.py`, `odoo_stock_by_product`, `build_payload`, `_enrich_deals`, `build`, `odoo_marketing_audit.py`, `family`, `type_fn`, `corporate_clients_from_db`, `excluded_products`, `fetch_new_products_data`, `lib/db.py`, `live_month_window`, `fetch_posting_data`, `build`, `build`, `load_lines`, `main`, `_seasonality`, `test_product_targets.py`, `bag_key_fn`, `negative_fixes.py`, `build`, `build`, `check_connection`, `_bags_not_on_offer`, `fetch`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `bag_classifier()` connect `bag_classifier` to `tests/test_receipt_combos.py`, `build_payload`, `Push Planner (`push_planner.py` → `push_planner.html`, `PP`)`, `main`, `load_data`, `Bags on offer vs not on offer`, `fetch`, `self_made_combos_bundle/lib/__init__.py`, `fetch`, `Product (bag) targets`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Why does `Bags on offer vs not on offer` connect `Bags on offer vs not on offer` to `tests/test_receipt_combos.py`, `_read_offers`, `bag_classifier`, `shop-birthdays.md`, `fetch`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **What connects `PERF`, `graphify`, `Python environment` to the rest of the system?**
  _261 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `month_extras.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0707070707070707 - nodes in this community are weakly interconnected._
- **Should `laya.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._
- **Should `tests/test_receipt_combos.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05641025641025641 - nodes in this community are weakly interconnected._