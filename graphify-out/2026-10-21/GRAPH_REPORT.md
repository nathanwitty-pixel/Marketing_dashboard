# Graph Report - Marketing_dashboard  (2026-10-21)

## Corpus Check
- 213 files · ~978,798 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: .csv 13, (none) 2, .toml 1)

## Summary
- 2415 nodes · 4691 edges · 189 communities (148 shown, 41 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 179 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7fc2efdd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- forward_projections.py
- _ask
- tests/test_receipt_combos.py
- oos_chip.js
- chart_switcher.js
- graw(block, key) function (bare numeric getter)
- Kitengela Rejects tracker (timed offer)
- push_rules.py
- name_match.py
- v5_theme.js
- current_performance.py
- bare_minimum setting (weekly target floor)
- signals
- last_week_from_db
- month_extras.py
- type_fn
- run_query
- test_oos_callbacks.py
- build_payload
- shop_corporate.py
- sticky_controls.js
- fetch_posting_data
- fetch
- Self-made combos vs running combos (doc)
- build
- scripts/test_receipt_combos.py
- norm
- Dashboard Menu Docs (spec index)
- build
- _enrich_deals
- bags_on_offer.py
- insights.html
- streamlit_app.py
- moves
- monthly_report.py
- anchor
- chronos_train.py
- odoo_stock_by_product
- build_payload
- Shops Efficiency Tracking spec doc
- signals
- get_gspread_client
- _mkt_week_label
- page_sidebar.js
- test_product_targets.py
- Combos & Power Deals by Shop panel (#combo-shop)
- self_made_combos_bundle/offer_data.py
- Self-made combos bundle Python dependencies (requirements.txt)
- CLAUDE.md
- history.py (read months back)
- Self-made combos vs Running combos portable bundle README
- start_server
- Month-End Routine
- Bags on offer vs not on offer
- algorithmic-art skill
- dataviz-charts skill
- bag_classifier
- compute_period
- _enrich_deals
- High-End Visual Design skill
- self_made_combos_bundle/self_made_combos.py
- _combo_button_usage
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- daydream skill (Vault Daydream)
- os
- OOS call-back progress (Ralph loop log)
- timed_offers.py (generator)
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- history.py
- self_made_combos_bundle/lib/report_month.py
- marketing_dashboard.sql
- shop_requests.py
- num
- shop_birthdays.py
- _fetch_monthly_kenya
- check_connection
- push_planner.py
- load_pages
- theme.py
- push_laya.py
- data
- test_push_planner.py
- html
- Bag signals — quant finance applied to product sales
- lib/offer_data.py
- F
- fetch_new_products_data
- test_stockout_demand.py
- README.md
- Denri Africa Dashboard Design System (skill)
- _build_period
- test_share_targets.py
- safe_int
- publish.py
- reject_sales.py
- new_products.py
- excluded_products
- Bag Signals — quant view of each bag (posting · stock · selling)
- bag_key_fn
- current_performance.html
- attach
- self_made_combos.py generator (build_payload + SQL + injection)
- run.py
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- timed_offers.py
- shops_dispatch.py
- Ralph task — only three sheet tabs left
- scripts/receipt_combos.py
- Bag targets October 2026_3acbad00.md
- get_rows
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- test_deals_csv.py
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- write_bags_offer_source
- _bg_jobs
- What the page shows
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- Product (bag) targets
- POST_DATA data block (Posting)
- Combos from receipts — running vs self-made
- read_block(file, start, end) function
- load_rows
- fetch
- ambiguous_python_import_17686b6faac5
- contextlib
- Ralph task — "Out of stock — call back" demand per shop
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- shops_efficiency.py
- live_month_window
- attach_stock
- load
- generators/self_made_combos.py
- base_name
- _bag_stock
- Ads impact — on every page (21 Oct 2026, user's call)
- _month_end_running
- generate_insights.py
- _bags_not_on_offer
- Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)
- followup
- update_np_weekly_history
- _dead_stock_region
- _alignment_region
- _odoo_colour
- Out-of-stock demand — people, not requests
- Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)
- posting_yields.py
- load_catalog
- corporate_clients_from_db
- _bg_rebuild
- odoo_weekly_breakdown
- odoo_month_product_bags
- online
- test_sheet_reads.py
- _match
- block
- _month_archived
- daily
- _bag_tiers
- master_products
- _secret
- lib

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 70 edges
2. `fetch()` - 39 edges
3. `fetch_posting_data()` - 38 edges
4. `data()` - 32 edges
5. `check_connection()` - 31 edges
6. `get_gspread_client()` - 31 edges
7. `build_payload()` - 30 edges
8. `build_payload()` - 24 edges
9. `build()` - 24 edges
10. `fetch_new_products_data()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `The split — by each bag's share of recent sales` --references--> `bag_classifier()`  [INFERRED]
  docs/product-targets.md → generators/self_made_combos.py
- `Inputs (read only — nothing is written to Odoo or the sheet)` --references--> `bag_classifier()`  [INFERRED]
  docs/push-planner.md → generators/self_made_combos.py
- `Laya's second opinion (`lib/push_laya.py`)` --references--> `state_text()`  [INFERRED]
  docs/push-planner.md → lib/push_laya.py
- `Why it isn't moving — reasons, per market (`push_rules.reasons`)` --references--> `reasons()`  [INFERRED]
  docs/push-planner.md → lib/push_rules.py
- `The comments` --references--> `section()`  [INFERRED]
  notes/MONTH_END.md → generators/ads_impact.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Self-made combos bundle: generator, Sheets auth, DB access, and dependency manifest working together to build the combos page** — export_self_made_combos_bundle_self_made_combos_py, export_self_made_combos_bundle_offer_data_py, export_self_made_combos_bundle_google_auth_py, export_self_made_combos_bundle_lib_db_py, export_self_made_combos_bundle_requirements [EXTRACTED 0.90]
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]

## Communities (189 total, 41 thin omitted)

### Community 0 - "forward_projections.py"
Cohesion: 0.17
Nodes (6): fetch_sheet_data(), fmt_opt_pct(), fmt_pct(), forward_projections.py…, One table row, month-end projected. expected = what the targets expect from…, _row()

### Community 1 - "_ask"
Cohesion: 0.08
Nodes (21): Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket(), _cache_get(), _cache_put() (+13 more)

### Community 2 - "tests/test_receipt_combos.py"
Cohesion: 0.07
Nodes (46): What the page shows (per period), _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region…, _region_goal() (+38 more)

### Community 3 - "oos_chip.js"
Cohesion: 0.07
Nodes (41): act(), cell(), esc(), attach(), close(), esc(), form(), go() (+33 more)

### Community 4 - "chart_switcher.js"
Cohesion: 0.12
Nodes (35): alpha(), apply(), attach(), axisOpts(), build(), changeTxt(), Chart(), clone() (+27 more)

### Community 6 - "Kitengela Rejects tracker (timed offer)"
Cohesion: 0.07
Nodes (28): bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source), Offline fallback pattern (mirror sheet data to local JSON), Reject Sale (doc: reject_sales.py -> reject_sales.html, RJ), reject_sales_export.csv (fallback export) (+20 more)

### Community 7 - "push_rules.py"
Cohesion: 0.11
Nodes (17): _cover_txt(), _days_back(), _kind(), _n(), not_moving(), posting_median(), rank(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).… (+9 more)

### Community 8 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "current_performance.py"
Cohesion: 0.13
Nodes (8): fetch_monthly_target(), current_performance.py…, main(), date, _query_ready(), weekly_sales.py — the weekly-sales fix. Computes the CURRENT Sun–Sat week's…, The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's…, week_window()

### Community 12 - "signals"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

### Community 13 - "last_week_from_db"
Cohesion: 0.25
Nodes (8): last_week_from_db(), Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary(), week_start_of(), weekly_from_db()

### Community 14 - "month_extras.py"
Cohesion: 0.25
Nodes (13): _bags_on_offer(), _block(), build_extras(), _deals(), _pick(), _posting(), _posting_block(), region() (+5 more)

### Community 15 - "type_fn"
Cohesion: 0.15
Nodes (17): posts_between(), fn(), fn(start, end) → {BAG: {"KE", "TZ", "UG": posts}} from marketing's daily…, build(), {TYPE: {"kes", "shops": {SHOP: {"n", "kes"}}}} for the runway types over…, ({TYPE: Kenya shop on-hand}, {TYPE: Sinza + Uganda on-hand}) — live Odoo., The NP.runway payload: {days, bags: [{name, created, category, stockKe,…, Product name → bag type (see the module docstring). (+9 more)

### Community 16 - "run_query"
Cohesion: 0.09
Nodes (24): corporate_from_db(), corporate_target_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, This month's Odoo corporate target {bags, kes} (sales_pos_target, scope…, _corporate_bags(), (corporate bags, corporate KES received) in the given month, live from Odoo…, The month's revenue target (KES): Odoo sales_pos_target amount (pos +…, _revenue_target() (+16 more)

### Community 17 - "test_oos_callbacks.py"
Cohesion: 0.19
Nodes (18): aggregate(), flat(), split(), {shop: set(person)} → (distinct people, [[shop, people], …] high → low)., The page block: {period: {key: {"total": people, "shops": [[shop, people],…, _shops(), pytest, _kai() (+10 more)

### Community 18 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 19 - "shop_corporate.py"
Cohesion: 0.15
Nodes (24): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), _acronym(), build(), _maybe(), owns(), corporate_team_receipts(), _d() (+16 more)

### Community 20 - "sticky_controls.js"
Cohesion: 0.20
Nodes (15): bind(), embedHost(), headerOf(), init(), initSections(), injectCss(), place(), setPinned() (+7 more)

### Community 21 - "fetch_posting_data"
Cohesion: 0.12
Nodes (15): _bt_on_offer(), _dead_clear(), fetch_posting_data(), _clear(), _yield(), _fold_bag_level(), load_dead_thresholds(), _post_yield() (+7 more)

### Community 22 - "fetch"
Cohesion: 0.13
Nodes (24): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), combo_slots(), make_classifier() (+16 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.05
Nodes (51): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026) (+43 more)

### Community 24 - "build"
Cohesion: 0.09
Nodes (32): Sales pace to month end (19 Oct 2026), bag_categories(), build(), fit(), grand_total(), last_month_need(), leads(), month_end_lift() (+24 more)

### Community 25 - "scripts/test_receipt_combos.py"
Cohesion: 0.32
Nodes (15): classify(), lines: [{receipt, d, product, qty, amount}] → per-market summary: {running:…, infer(), L(), Tests for receipt_combos.py + name_match.py — python -m pytest scripts -q, test_alternatives_and_singles(), test_bulk_receipts_are_not_combos(), test_four_bags_at_two_prices_are_two_combos() (+7 more)

### Community 26 - "norm"
Cohesion: 0.23
Nodes (10): build_rows(), _Deriver, _flag_cells(), _fmt(), norm(), _products(), Name key shared by the catalogue and Odoo: upper-case, '.'→space, collapsed…, Labels for an Odoo product the catalogue doesn't know yet, learnt from the… (+2 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.18
Nodes (14): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes) (+6 more)

### Community 28 - "build"
Cohesion: 0.08
Nodes (42): build(), acts(), campaign_table(), money(), cpr(), focus_tiles(), market_table(), overview_tiles() (+34 more)

### Community 29 - "_enrich_deals"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "bags_on_offer.py"
Cohesion: 0.27
Nodes (10): _base_windows(), _custom_range(), fmt(), inject(), main(), bags_on_offer.py…, (from, to) dates from boo_custom_range.json — the Custom period — or None., Write (or with a=None, delete) the Custom period's dates. (+2 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.12
Nodes (7): SCRIPT_TIMEOUT = 600s config, html, streamlit, _load_secrets_into_env(), streamlit_app.py — Denri Marketing Dashboard on Streamlit. Serves the existing…, streamlit_components_v1, urllib_parse

### Community 33 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.16
Nodes (8): _cause(), esc(), fmt(), ladder_strip(), pct(), monthly_report.py…, _smc_srow(), _stock_rows()

### Community 35 - "anchor"
Cohesion: 0.11
Nodes (22): _db_count(), monthly_from_db(), Reporting month's subset count (e.g. rejectBags, giftBags) from…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,…, count_complete_weeks_in_month(), Count Mon–Sun weeks in the reporting month that have ≥5 days falling within it., anchor(), is_pinned() (+14 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.07
Nodes (44): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+36 more)

### Community 37 - "odoo_stock_by_product"
Cohesion: 0.15
Nodes (16): buffer_stock(), {location: {BAG: units}} at CBD/Stock and VLD/Stock (exact locations)., odoo_stock_levels(), Live per-shop Odoo on-hand in the SAME shape parse_sheet(STOCK_LEVELS) returns:…, _codes_for(), _inlist(), odoo_stock_at_location(), odoo_stock_by_product() (+8 more)

### Community 38 - "build_payload"
Cohesion: 0.05
Nodes (41): _self_made_combos(), Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), build_payload(), _anchor_sunday(), _combo_bags() (+33 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "signals"
Cohesion: 0.17
Nodes (16): action(), _mean(), _phi(), posting_beta(), The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json…, _sd() (+8 more)

### Community 41 - "get_gspread_client"
Cohesion: 0.10
Nodes (24): _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., build(), _cfg(), first_sale(), kenya_posts(), load_workplan() (+16 more)

### Community 42 - "_mkt_week_label"
Cohesion: 0.29
Nodes (7): _mkt_perfect_week_index(), _mkt_week_label(), Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]., current = {region: {key: {productName,colour,category,bagType,stock}}}. A new…, update_clearance(), update_mkt_history()

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "test_product_targets.py"
Cohesion: 0.19
Nodes (13): allocate(), available_days(), Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, _add_months(), _d(), main(), Tests for lib/product_targets.py (bag targets from Odoo; spec docs/product-… (+5 more)

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
Cohesion: 0.09
Nodes (27): generator(), _is_quota_error(), _is_transient(), _offer_active_today(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, _run_one() (+19 more)

### Community 52 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

### Community 53 - "Bags on offer vs not on offer"
Cohesion: 0.20
Nodes (10): Bags on offer vs not on offer, Corporate-lead till orders, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Regenerate, Shop birthdays, Shop metrics (vs the Odoo revenue target) (+2 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.17
Nodes (12): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+4 more)

### Community 56 - "bag_classifier"
Cohesion: 0.17
Nodes (15): Buckets, _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _norm_combo() (+7 more)

### Community 57 - "compute_period"
Cohesion: 0.12
Nodes (11): apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _metric(), pct(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period. (+3 more)

### Community 58 - "_enrich_deals"
Cohesion: 0.25
Nodes (6): _enrich_deals(), _tdigit(), _tier_agg(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "self_made_combos_bundle/self_made_combos.py"
Cohesion: 0.16
Nodes (13): get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, fetch(), fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py… (+5 more)

### Community 61 - "_combo_button_usage"
Cohesion: 0.15
Nodes (12): _build_sheet_slots(), _combo_button_usage(), _combo_norm_option(), _combo_odoo_slots(), _combo_sheet_slots(), _matches_sheet(), One combo slot-option → its distinctive bag token(s), colours/category words…, Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+4 more)

### Community 62 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "os"
Cohesion: 0.06
Nodes (41): One-off: restore August's Offer Type figures into monthly_report_history.json…, lib — shared data-access for the marketing dashboard (Postgres migration).…, ads_impact.py — the Ads impact panel shown on every page (spec: docs/ads-…, monthly_sales.py — the current month's real bags sold, from Postgres. The…, offer_picking.py…, Save a local, human-editable copy of the offers prices to OFFERS_CACHE., _write_offers_cache(), hashlib (+33 more)

### Community 65 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.15
Nodes (11): _local_deal_rows(), Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), Blocker counter, Deals from posters (RALPH_DEALS.md) — 2026-10-04, Final summary, Log (+3 more)

### Community 66 - "timed_offers.py (generator)"
Cohesion: 0.09
Nodes (22): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+14 more)

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.12
Nodes (16): Bag health (by bag, 18 Oct 2026), Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026), Page, Product rating and core 5 vs other 13 categories (18 Oct 2026) (+8 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "history.py"
Cohesion: 0.13
Nodes (21): dotenv, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers… (+13 more)

### Community 71 - "self_made_combos_bundle/lib/report_month.py"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "shop_requests.py"
Cohesion: 0.05
Nodes (51): _onoff(), build(), _d(), explain(), _fmt_d(), _load_json(), load_lines(), load_posts() (+43 more)

### Community 74 - "num"
Cohesion: 0.20
Nodes (11): _garr_line(), gnum(), num(), _offers(), _parse_offers(), _units(), This month's timed-offer campaigns, flattened for storage. The live TO payload…, Greedy single-line array extractor — handles nested [[...],[...]] arrays. (+3 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "_fetch_monthly_kenya"
Cohesion: 0.17
Nodes (16): _analyze_region(), _fetch_monthly_kenya(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), Monthly Kenya figures for the S1 KPI cards. MONTHLY_MARKETING_POST: sum col E…, MONTHLY_SALES: colour=A(0), product_name=B(1) (+8 more)

### Community 77 - "check_connection"
Cohesion: 0.10
Nodes (22): build_offer(), odoo_bag_daily_value(), odoo_bag_prices(), odoo_bulk_lines(), odoo_daily_kenya(), odoo_list_price(), odoo_offer_price(), odoo_window_sales() (+14 more)

### Community 78 - "push_planner.py"
Cohesion: 0.12
Nodes (23): add_laya(), build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), main() (+15 more)

### Community 79 - "load_pages"
Cohesion: 0.29
Nodes (7): _new_products(), This month's new products: data/new_products.txt (lib/new_products_list) — the…, load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, names(), Upper-cased bag types from new_products.txt in file order ([] = no new…

### Community 80 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), lib/theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 81 - "push_laya.py"
Cohesion: 0.13
Nodes (20): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+12 more)

### Community 82 - "data"
Cohesion: 0.13
Nodes (16): _live_bags(), {BAG (upper): official full price} from bag_original_prices.json (fallback)., _read_bag_prices(), load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if…, _till_to_shop() (+8 more)

### Community 83 - "test_push_planner.py"
Cohesion: 0.18
Nodes (18): Per bag × market: the facts (`push_rules.facts`, `add_peers`), add_peers(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m…, ISO date n days before END (0 = END). (+10 more)

### Community 84 - "html"
Cohesion: 0.29
Nodes (6): read_block(), read_block(), _read_timed_offers(), _offer_bagtypes_by_region(), On-offer bag types per region, read from self_made_combos.html's SMC block:…, html()

### Community 85 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 86 - "lib/offer_data.py"
Cohesion: 0.20
Nodes (12): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), offer_data.py ─────────────────────────────────────────────────────────────────… (+4 more)

### Community 87 - "F"
Cohesion: 0.15
Nodes (24): action(), context(), (code, plain sentence, units at stake, confidence 0..1) for one bag × market.…, What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F() (+16 more)

### Community 88 - "fetch_new_products_data"
Cohesion: 0.20
Nodes (14): fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_sales_window() (+6 more)

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "README.md"
Cohesion: 0.17
Nodes (7): Agent skills — retail analytics, Test a skill, Use in another project, Deliver, Sales-share targets per product, Steps, Tests

### Community 91 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.06
Nodes (36): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards) (+28 more)

### Community 92 - "_build_period"
Cohesion: 0.20
Nodes (6): _build_period(), _offer_types(), _pick_target(), Latest target row for `shop` with this period that overlaps [start, end]. A…, Matrix payload: rows, per-row category / tier cells, and the period's Top-5…, _region_of()

### Community 93 - "test_share_targets.py"
Cohesion: 0.22
Nodes (11): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+3 more)

### Community 94 - "safe_int"
Cohesion: 0.15
Nodes (22): _bag_level_bags(), _build_no_convert(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int(), _is_checked() (+14 more)

### Community 95 - "publish.py"
Cohesion: 0.26
Nodes (12): argparse, fnmatch, py_compile, changed_files(), git(), group(), is_secret(), main() (+4 more)

### Community 96 - "reject_sales.py"
Cohesion: 0.06
Nodes (41): Offer type summary (matrix), _alt_cost(), _apply_alias(), build(), _build_catalog(), _combo_cost(), _combo_slots(), _is_full_price() (+33 more)

### Community 97 - "new_products.py"
Cohesion: 0.16
Nodes (8): _base_colour(), _merge_rows_by_base_colour(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across…, _strip_colour_qualifiers(), lib/new_products_list.py — which bag types count as this month's NEW PRODUCTS.…

### Community 98 - "excluded_products"
Cohesion: 0.13
Nodes (14): market_sales(), {market: {bags, kes, orders}} over [start, end]., {market: [ {bags, kes, orders} per week ]} from Odoo; None if Postgres is down., sales_by_market(), _bag_revenue(), _bag_revenue_range(), POS bag revenue for the month, split by how the bags were sold…, main() (+6 more)

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "bag_key_fn"
Cohesion: 0.16
Nodes (14): build(), Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), bag_posts(), tally(), load(), (daily, total, stock, launch, start, end) for Kenya from Odoo; daily per bag…, {BAG: (posts this month, posts last week)} — Kenya posts (col E) from the two… (+6 more)

### Community 101 - "current_performance.html"
Cohesion: 0.50
Nodes (4): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance)

### Community 102 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 103 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.29
Nodes (7): lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, lib/report_month.py (which month are we reporting?), self_made_combos.html static page (reads const SMC), self_made_combos.py generator (build_payload + SQL + injection)

### Community 104 - "run.py"
Cohesion: 0.36
Nodes (9): action_js(), edge_dump(), embedded(), inline_local(), js_str(), main(), Sticky-controls checks (docs/sticky-controls.md › Checks). python…, JS act(d, cb): optionally set a <select> (setv = "SEL=VALUE", fires change),… (+1 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "timed_offers.py"
Cohesion: 0.11
Nodes (26): Kenya timed-offer campaigns from timed_offers_config.json (normalised by…, _timed_offers(), _bags_from_file(), _bucket(), _derive_month(), kenya_stock_by_bag(), load_config(), _norm_offer() (+18 more)

### Community 107 - "shops_dispatch.py"
Cohesion: 0.23
Nodes (14): build_period(), distributed_in(), main(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only., Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).… (+6 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "scripts/receipt_combos.py"
Cohesion: 0.33
Nodes (5): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "get_rows"
Cohesion: 0.12
Nodes (17): load(), _build(), default_window(), get_rows(), last_complete_week(), offer_flags(), _ok(), prime_offer_flags() (+9 more)

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 114 - "test_deals_csv.py"
Cohesion: 0.33
Nodes (3): self_made_combos, Tests for the poster-sourced deals (deals_kenya.csv →…, test_month_not_in_csv_has_no_deals_and_no_sheet_read()

### Community 121 - "write_bags_offer_source"
Cohesion: 0.17
Nodes (12): Counted by how it was sold, _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…, dow_tier_weeks(), fmt(), inject() (+4 more)

### Community 122 - "_bg_jobs"
Cohesion: 0.25
Nodes (8): cache_resource, fragment, _bg_done_msg(), _bg_jobs(), _bg_watch(), _fmt_secs(), Background rebuilds shared by every session: label → job (see _bg_rebuild)., The refresh_msg for a finished background rebuild (None: the job vanished).

### Community 123 - "What the page shows"
Cohesion: 0.20
Nodes (9): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Bulk orders, Data, Product Performance — which bags, categories and colours carry the sales, and why (+1 more)

### Community 126 - "Product (bag) targets"
Cohesion: 0.25
Nodes (8): A month with only a revenue target (November 2026), Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 128 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 130 - "load_rows"
Cohesion: 0.21
Nodes (11): _date(), load_rows(), _online_rows(), oos_by_bag_shop(), {period: {product name: {shop: people}}} straight from Odoo names, or {} if…, Odoo translatable names can come back as {'en_US': …}., [{date, shop, kind, person, purchased, product, channel}] — one per OOS request…, _txt() (+3 more)

### Community 131 - "fetch"
Cohesion: 0.25
Nodes (7): _bags_not_on_offer(), fetch(), Bags with sales this month (in the market `sql` scopes to) that are on NO…, The component bag names across a region's sheet combos/singles/specials cards…, Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer…, _read_offer_analysis(), _region_on_offer_bags()

### Community 138 - "Ralph task — "Out of stock — call back" demand per shop"
Cohesion: 0.25
Nodes (8): match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, Established facts (do not re-investigate), Every iteration, Periods (dates in Africa/Nairobi), Ralph task — "Out of stock — call back" demand per shop, Stopping, Sub-goals (in order)

### Community 145 - "Shop Launch"
Cohesion: 0.29
Nodes (6): Config, Launch day, Marketing posts, Sales, Shop Launch, What the page shows

### Community 153 - "shops_efficiency.py"
Cohesion: 0.22
Nodes (7): metric_byshop(), parse_sheet(), shops_efficiency.py…, Return (data, meta) for the Kenya shops, locating columns by header name…, safe_int(), update_history(), pathlib

### Community 154 - "live_month_window"
Cohesion: 0.22
Nodes (11): {period: (start, end)} for the dated periods (lifetime / current are undated).…, windows(), build(), load_targets(), (total units, info) — the month's Odoo target units, or (no Odoo targets yet)…, (rows, total, base start, base end) for the month, from Odoo., {BAG: target units} for the month from product_targets_<YYYY-MM>.csv (built…, total_for() (+3 more)

### Community 155 - "attach_stock"
Cohesion: 0.27
Nodes (10): attach_stock(), in_stock(), stk(), collect(), _in(), is_combo_request(), True when the request names a whole combo ("Amaya Handbag or Elyse Handbag +…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+2 more)

### Community 156 - "load"
Cohesion: 0.29
Nodes (7): from_argv(), load(), path(), (from, to) dates for the page's Custom period, or None. Swapped if reversed;…, Write the range, or with a=None delete it (Clear)., `<script> FROM TO` saves a range, `<script> clear` deletes it; anything else is…, save()

### Community 157 - "generators/self_made_combos.py"
Cohesion: 0.10
Nodes (18): _bag_sales_daily_sql(), _bag_sales_sql(), _build_sheet_slots(), _combo_sheet_slots(), _load_shop_regions(), self_made_combos.py…, Shop → Region from docs/shop-regions.md (lib/shop_regions); the built-in…, Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+10 more)

### Community 158 - "base_name"
Cohesion: 0.25
Nodes (9): apply_walkins(), base_name(), dispatch_by_product_shop(), _num(), The catalogue key for an Odoo product name: norm() without the "[REJECT]" tag…, {NORM(product): {SHOP: bags}} of POS bag sales in [start, end]; None if DB…, {NORM(product): {SHOP: bags distributed in}} from combined_distribution.sql's…, sales_by_product_shop() (+1 more)

### Community 159 - "_bag_stock"
Cohesion: 0.40
Nodes (5): _bag_stock(), _combo_bags(), _norm_bag(), Space/punctuation-insensitive key so 'MINIZURI' matches 'MINI ZURI'., Component bags of an offer, each with its stock, sorted most-stock first.

### Community 160 - "Ads impact — on every page (21 Oct 2026, user's call)"
Cohesion: 0.25
Nodes (7): Actions ("what we can do"), Ads impact — on every page (21 Oct 2026, user's call), Figures, Refresh, What each page shows, new_bags(), Bags launched inside the base period (the bag-targets CSV's Launch column).

### Community 162 - "generate_insights.py"
Cohesion: 0.24
Nodes (5): card(), esc(), fmt(), generate_insights.py…, region_card()

### Community 163 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 165 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 166 - "update_np_weekly_history"
Cohesion: 0.29
Nodes (7): _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)., Ordinal among the month's perfect weeks (>=5 days in month), so the first FULL…, Snapshot each Sun–Sat week (sales, Kenya/Outside posts) into…, update_np_weekly_history()

### Community 167 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 168 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 169 - "_odoo_colour"
Cohesion: 0.25
Nodes (8): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, ({PRODUCT: {SHOP CODE: units}}, {PRODUCT: {SHOP CODE: [[colour, units], …]}})…, shop_sales(), _aliases(), odoo_name(), {NORM(odoo name): NORM(sheet name)} from product_aliases.csv — products Odoo…, Odoo's spelling of a catalogue name (the reverse of product_aliases.csv), for…

### Community 170 - "Out-of-stock demand — people, not requests"
Cohesion: 0.29
Nodes (7): Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods, Show it as, Tests

### Community 172 - "posting_yields.py"
Cohesion: 0.12
Nodes (23): calendar, collections, csv, datetime, posting_yields.py…, product_performance.py — the Product Performance page: % share of the top-…, shop_stock_levels.py — the Shop Stock Levels page: min / max per shop × bag…, lib/bag_quant.py — quant signals per bag: drift, volatility, Sharpe-style… (+15 more)

### Community 173 - "load_catalog"
Cohesion: 0.29
Nodes (6): categories(), {BAG: category} — the bag type's usual catalogue category, else its Odoo…, catalog_rows(), load_catalog(), [{colour, category, name, bag}] in sheet order, from product_catalog.csv., [header] + [[COLOUR, CATEGORY, PRODUCT NAME, BAG TYPE], …] — the label columns…

### Community 174 - "corporate_clients_from_db"
Cohesion: 0.40
Nodes (6): corporate_clients_from_db(), _months(), A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],…, Current month's corporate activity per client (quoted · invoiced · paid · sold)…, _txt()

### Community 175 - "_bg_rebuild"
Cohesion: 0.33
Nodes (7): _bg_rebuild(), work(), Seconds the last good `kind` rebuild of `lbl` took (any kind as a fallback),…, Rebuild `lbl` in the background. kind: "auto" (skipped if a rebuild was tried…, _rebuild_secs(), run_scripts(), _save_rebuild_secs()

### Community 177 - "odoo_weekly_breakdown"
Cohesion: 0.40
Nodes (6): odoo_weekly_breakdown(), _perfect_week_index(), Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, update_weekly_history(), _week_start()

### Community 178 - "odoo_month_product_bags"
Cohesion: 0.33
Nodes (6): odoo_combo_product_bags(), odoo_lifetime_product_bags(), odoo_month_product_bags(), All-time bags per product from Odoo (no month window) — the lifetime sales of…, [(product name, bags)] for bags sold INSIDE combos (sub_product_line) in the…, Reporting month's bags per product from Odoo (Postgres), or None if the DB…

### Community 179 - "online"
Cohesion: 0.40
Nodes (5): Out of stock — call back, fixture, live(), online(), Lifetime {product: {shop: people}} from the WhatsApp channel only —…

### Community 180 - "test_sheet_reads.py"
Cohesion: 0.47
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 181 - "_match"
Cohesion: 0.50
Nodes (3): _match(), _full(), _full_of()

### Community 182 - "block"
Cohesion: 0.20
Nodes (10): block(), label(), month_share(), 01 Sep – 30 Sep' (years added when the range crosses one or isn't this year)., How many months the range covers — each day counts 1/(days in its month). A…, The page's NP/PA `custom` data block: None, or {from, to, label, days, months}., Run script-only HTML in an invisible frame (same origin, so it can reach…, Fade the page area back in on a page that has no dashboard frame (password… (+2 more)

### Community 183 - "_month_archived"
Cohesion: 0.67
Nodes (3): cache_data, _month_archived(), True when `key` is in Supabase (falls back to monthly_report_history.json). If…

### Community 184 - "daily"
Cohesion: 0.40
Nodes (5): daily(), _num(), parse(), One tab's rows → {(BAG TYPE, COLOUR): {date: posts}}., {(BAG TYPE, COLOUR): {market: {date: posts}}} from the three sheets (cached for…

### Community 185 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

### Community 186 - "master_products"
Cohesion: 0.50
Nodes (4): master_products(), _norm_name(), Match the SQL normalisation: lower-case, '.'→space, collapse whitespace., Normalised, de-duplicated master catalogue names (master_products.txt), for the…

## Knowledge Gaps
- **216 isolated node(s):** `PERF`, `graphify`, `Use in another project`, `Test a skill`, `Inputs you must build from the project's data` (+211 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 990 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **41 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_query()` connect `run_query` to `tests/test_receipt_combos.py`, `fetch`, `current_performance.py`, `last_week_from_db`, `type_fn`, `build_payload`, `shop_corporate.py`, `fetch_posting_data`, `fetch`, `build`, `live_month_window`, `build`, `_enrich_deals`, `base_name`, `_bags_not_on_offer`, `chronos_train.py`, `odoo_stock_by_product`, `build_payload`, `_odoo_colour`, `get_gspread_client`, `test_product_targets.py`, `corporate_clients_from_db`, `odoo_weekly_breakdown`, `odoo_month_product_bags`, `_enrich_deals`, `_combo_button_usage`, `os`, `shop_requests.py`, `check_connection`, `fetch_new_products_data`, `excluded_products`, `bag_key_fn`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `bag_classifier()` connect `bag_classifier` to `tests/test_receipt_combos.py`, `fetch`, `build_payload`, `push_planner.py`, `data`, `online`, `fetch`, `write_bags_offer_source`, `Product (bag) targets`, `generators/self_made_combos.py`, `Push Planner (`push_planner.py` → `push_planner.html`, `PP`)`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `build_payload()` connect `build_payload` to `monthly_report.py`, `tests/test_receipt_combos.py`, `fetch`, `run_query`, `generators/self_made_combos.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **What connects `PERF`, `graphify`, `Use in another project` to the rest of the system?**
  _216 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `_ask` be split into smaller, more focused modules?**
  _Cohesion score 0.08374384236453201 - nodes in this community are weakly interconnected._
- **Should `tests/test_receipt_combos.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07039187227866474 - nodes in this community are weakly interconnected._
- **Should `oos_chip.js` be split into smaller, more focused modules?**
  _Cohesion score 0.07111756168359942 - nodes in this community are weakly interconnected._