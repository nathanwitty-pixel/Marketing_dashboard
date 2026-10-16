# Graph Report - Marketing_dashboard  (2026-10-16)

## Corpus Check
- 197 files · ~843,391 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 16 file(s) not represented in the graph (top: .csv 9, (none) 2, .toml 1)

## Summary
- 2220 nodes · 4262 edges · 172 communities (135 shown, 37 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 157 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4d42ce8b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- fetch_posting_data
- laya.py
- tests/test_receipt_combos.py
- oos_chip.js
- chart_switcher.js
- graw(block, key) function (bare numeric getter)
- Kitengela Rejects tracker (timed offer)
- generators/self_made_combos.py
- timed_offers.py
- v5_theme.js
- test_product_targets.py
- bare_minimum setting (weekly target floor)
- signals
- block
- month_extras.py
- stock.py
- publish.py
- current_performance.py
- build_payload
- family
- shop_corporate.py
- main
- self_made_combos_bundle/self_made_combos.py
- Self-made combos vs running combos (doc)
- compute_period
- signals
- shops_dispatch.py
- Dashboard Menu Docs (spec index)
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- _enrich_deals
- fetch
- insights.html
- streamlit_app.py
- week_start_of
- monthly_report.py
- _seasonality
- main
- load_data
- build_payload
- Shops Efficiency Tracking spec doc
- shop_launch.py
- push_rules.py
- self_made_combos_bundle/lib/db.py
- page_sidebar.js
- _combo_button_usage
- Combos & Power Deals by Shop panel (#combo-shop)
- self_made_combos_bundle/offer_data.py
- Self-made combos bundle Python dependencies (requirements.txt)
- CLAUDE.md
- history.py (read months back)
- Self-made combos vs Running combos portable bundle README
- start_server
- scripts/test_receipt_combos.py
- fetch_new_products_data
- algorithmic-art skill
- dataviz-charts skill
- bag_classifier
- sys
- _enrich_deals
- High-End Visual Design skill
- test_share_targets.py
- test_sheet_reads.py
- oos_callbacks.py
- daydream skill (Vault Daydream)
- main.py
- OOS call-back progress (Ralph loop log)
- timed_offers.py (generator)
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- update_np_weekly_history
- _date
- marketing_dashboard.sql
- build
- Month-End Routine
- push_planner.py
- lib/offer_data.py
- os
- data
- history.py
- theme.py
- push_laya.py
- build
- facts
- followup
- label
- Chart type switcher (every chart, every menu)
- test_push_planner.py
- new_products.py
- test_stockout_demand.py
- Out-of-stock demand — people, not requests
- Denri Africa Dashboard Design System (skill)
- _kind
- monthly_target_rows
- reject_variants
- month_end.py
- odoo_weekly_breakdown
- market_summary
- _combo_button_usage
- Bag Signals — quant view of each bag (posting · stock · selling)
- check_connection
- current_performance.html
- attach
- self_made_combos.py generator (build_payload + SQL + injection)
- corporate_clients_from_db
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- _bags_not_on_offer
- get_rows
- Ralph task — only three sheet tabs left
- Bags on offer vs not on offer
- Bag targets October 2026_3acbad00.md
- bags_on_offer.py
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- lib
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- live_month_window
- shops_efficiency.py
- What the page shows
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- norm
- POST_DATA data block (Posting)
- _build_period
- read_block(file, start, end) function
- _resolve_bag
- anchor
- ambiguous_python_import_17686b6faac5
- contextlib
- run_query
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- build
- base_name
- _mkt_week_label
- load_catalog
- type_fn
- get_engine
- odoo_month_product_bags
- product_targets_workbook.py
- _read_offers
- generate_insights.py
- _category_of
- _build_sheet_slots
- _bag_tiers
- _load_source
- _read_bom_costs
- _load_combos_by_shop
- prime_offer_flags
- master_products
- _write_offers_cache

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 59 edges
2. `fetch()` - 40 edges
3. `fetch_posting_data()` - 35 edges
4. `build_payload()` - 30 edges
5. `get_gspread_client()` - 29 edges
6. `check_connection()` - 28 edges
7. `data()` - 26 edges
8. `build_payload()` - 24 edges
9. `build_offer()` - 22 edges
10. `_date()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `Buckets` --references--> `bag_classifier()`  [INFERRED]
  docs/bags-on-offer.md → generators/self_made_combos.py
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

## Communities (172 total, 37 thin omitted)

### Community 0 - "fetch_posting_data"
Cohesion: 0.05
Nodes (64): _alignment_region(), _for(), _onoff(), _sold(), _stk(), _units(), _analyze_region(), _bt_on_offer() (+56 more)

### Community 1 - "laya.py"
Cohesion: 0.09
Nodes (26): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket() (+18 more)

### Community 2 - "tests/test_receipt_combos.py"
Cohesion: 0.10
Nodes (36): What the page shows (per period), _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, bag_key(), classify(), _fits(), _groups(), load_offers() (+28 more)

### Community 3 - "oos_chip.js"
Cohesion: 0.08
Nodes (38): attach(), close(), esc(), form(), go(), iso(), mountPanel(), open() (+30 more)

### Community 4 - "chart_switcher.js"
Cohesion: 0.13
Nodes (33): alpha(), apply(), attach(), axisOpts(), build(), changeTxt(), Chart(), clone() (+25 more)

### Community 6 - "Kitengela Rejects tracker (timed offer)"
Cohesion: 0.07
Nodes (28): bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source), Offline fallback pattern (mirror sheet data to local JSON), Reject Sale (doc: reject_sales.py -> reject_sales.html, RJ), reject_sales_export.csv (fallback export) (+20 more)

### Community 7 - "generators/self_made_combos.py"
Cohesion: 0.11
Nodes (23): Counted by how it was sold, _bag_sales_daily_sql(), _bag_sales_sql(), _bags_not_on_offer(), dow_tier_weeks(), fetch(), fmt(), inject() (+15 more)

### Community 8 - "timed_offers.py"
Cohesion: 0.17
Nodes (14): Kenya timed-offer campaigns from timed_offers_config.json (normalised by…, _timed_offers(), _bags_from_file(), _derive_month(), load_config(), _norm_offer(), timed_offers.py…, Multi-offer config: {"month": "YYYY-MM", "offers": [offer, ...]}. Back-compat:… (+6 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "test_product_targets.py"
Cohesion: 0.24
Nodes (10): allocate(), available_days(), Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for lib/product_targets.py (bag targets from Odoo; spec docs/product-…, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating(), test_new_bag_is_scaled_to_the_days_it_was_in_shops() (+2 more)

### Community 12 - "signals"
Cohesion: 0.17
Nodes (16): action(), _mean(), _phi(), posting_beta(), The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json…, _sd() (+8 more)

### Community 13 - "block"
Cohesion: 0.18
Nodes (11): block(), from_argv(), load(), month_share(), path(), (from, to) dates for the page's Custom period, or None. Swapped if reversed;…, Write the range, or with a=None delete it (Clear)., `<script> FROM TO` saves a range, `<script> clear` deletes it; anything else is… (+3 more)

### Community 14 - "month_extras.py"
Cohesion: 0.15
Nodes (20): _new_products(), This month's new products: data/new_products.txt (lib/new_products_list) — the…, load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, _bags_on_offer(), _block(), build_extras() (+12 more)

### Community 15 - "stock.py"
Cohesion: 0.20
Nodes (15): odoo_stock_levels(), Live per-shop Odoo on-hand in the SAME shape parse_sheet(STOCK_LEVELS) returns:…, _codes_for(), _inlist(), odoo_stock_at_location(), odoo_stock_by_product(), odoo_stock_by_shop_code(), _ok() (+7 more)

### Community 16 - "publish.py"
Cohesion: 0.23
Nodes (13): argparse, fnmatch, py_compile, changed_files(), git(), group(), is_secret(), main() (+5 more)

### Community 17 - "current_performance.py"
Cohesion: 0.08
Nodes (14): _posts(), MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., fetch_monthly_target(), current_performance.py…, fetch_sheet_data(), forward_projections.py…, The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's…, week_window() (+6 more)

### Community 18 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 19 - "family"
Cohesion: 0.12
Nodes (24): build(), fit(), grand_total(), leads(), needs(), _next_month(), _num(), ({SHOP: {BAG: units}}, {SHOP: {BAG: {colour: units}}}) over [start, end]. (+16 more)

### Community 20 - "shop_corporate.py"
Cohesion: 0.16
Nodes (23): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), _acronym(), build(), _maybe(), owns(), corporate_team_receipts(), _d() (+15 more)

### Community 21 - "main"
Cohesion: 0.25
Nodes (8): build_facts(), build_reasons(), inject(), main(), Facts for every bag × market that has stock or sold in the window…, Adds notMoving + reasons to every row (lib/push_rules.reasons). Returns the…, not_moving(), A bag with stock that isn't clearing: cleared < 30% this month, or > 45 days of…

### Community 22 - "self_made_combos_bundle/self_made_combos.py"
Cohesion: 0.20
Nodes (11): fetch(), fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py…, Read the Shop → Region table from docs/shop-regions.md so the mapping can be…, Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer… (+3 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.05
Nodes (51): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Current Performance (doc), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), New Products Analytics (doc) (+43 more)

### Community 24 - "compute_period"
Cohesion: 0.12
Nodes (11): apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _metric(), pct(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period. (+3 more)

### Community 25 - "signals"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

### Community 26 - "shops_dispatch.py"
Cohesion: 0.21
Nodes (14): build_period(), distributed_in(), main(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only., Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).… (+6 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.18
Nodes (14): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes) (+6 more)

### Community 28 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.15
Nodes (14): Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Per bag × market: the facts (`push_rules.facts`, `add_peers`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+6 more)

### Community 29 - "_enrich_deals"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "fetch"
Cohesion: 0.14
Nodes (23): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), combo_slots(), make_classifier() (+15 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.06
Nodes (29): cache_data, cache_resource, SCRIPT_TIMEOUT = 600s config, fragment, hashlib, html, streamlit, _bg_done_msg() (+21 more)

### Community 33 - "week_start_of"
Cohesion: 0.33
Nodes (6): Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary(), week_start_of(), weekly_from_db()

### Community 34 - "monthly_report.py"
Cohesion: 0.08
Nodes (26): _bag_stock(), _cause(), _combo_bags(), esc(), fmt(), _garr_line(), gnum(), ladder_strip() (+18 more)

### Community 35 - "_seasonality"
Cohesion: 0.15
Nodes (16): Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), _build_sheet_slots(), _combo_norm_option(), _combo_odoo_slots(), _combo_sheet_slots() (+8 more)

### Community 36 - "main"
Cohesion: 0.13
Nodes (20): inject(), inject_train(), main(), forecast(), Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run., Daily walk-ins (denri_footfall_count) and new walk-in leads (denri_lead), as…, walkins_and_leads() (+12 more)

### Community 37 - "load_data"
Cohesion: 0.40
Nodes (5): load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if…, _till_to_shop()

### Community 38 - "build_payload"
Cohesion: 0.14
Nodes (16): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+8 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "shop_launch.py"
Cohesion: 0.20
Nodes (14): build(), _cfg(), first_sale(), kenya_posts(), load_workplan(), make_matcher(), match(), _parse_workplan() (+6 more)

### Community 41 - "push_rules.py"
Cohesion: 0.11
Nodes (24): Actions (one per bag × market, then ranked), build_actions(), Adds action / says / units / confidence / score to each facts row; returns…, action(), _cover_txt(), moves(), _n(), posting_median() (+16 more)

### Community 42 - "self_made_combos_bundle/lib/db.py"
Cohesion: 0.15
Nodes (18): check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, Run a read query and return a DataFrame, or None if the DB is unreachable.… (+10 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "_combo_button_usage"
Cohesion: 0.22
Nodes (8): _combo_button_usage(), _combo_norm_option(), _combo_odoo_slots(), _matches_sheet(), One combo slot-option → its distinctive bag token(s), colours/category words…, Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…, The sheet label this Odoo combo maps to (same slot count, every slot overlaps),…, Per running combo: units rung through the combo button (Odoo) vs the sheet's…

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

### Community 51 - "start_server"
Cohesion: 0.31
Nodes (8): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_to_config(), _json()

### Community 52 - "scripts/test_receipt_combos.py"
Cohesion: 0.08
Nodes (42): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+34 more)

### Community 53 - "fetch_new_products_data"
Cohesion: 0.21
Nodes (13): fetch_new_products_data(), _apply_stock(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_sales_window(), odoo_stock_kenya_outside() (+5 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.17
Nodes (12): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+4 more)

### Community 56 - "bag_classifier"
Cohesion: 0.19
Nodes (14): _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _load_bag_prices(), _norm_combo() (+6 more)

### Community 57 - "sys"
Cohesion: 0.15
Nodes (12): chronos_preview.py…, chronos_train.py…, chronos, numpy, pandas, build_all.py ────────────────────────────────────────────────────────────────…, self_made_combos, sys (+4 more)

### Community 58 - "_enrich_deals"
Cohesion: 0.16
Nodes (9): _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,… (+1 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "test_share_targets.py"
Cohesion: 0.22
Nodes (11): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+3 more)

### Community 61 - "test_sheet_reads.py"
Cohesion: 0.60
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 62 - "oos_callbacks.py"
Cohesion: 0.06
Nodes (58): Out of stock — call back, fixture, match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, aggregate(), flat(), split(), attach_stock() (+50 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "main.py"
Cohesion: 0.10
Nodes (25): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), _offer_active_today(), A one-off network hiccup worth an immediate retry — a Google Sheets read… (+17 more)

### Community 65 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.15
Nodes (11): _local_deal_rows(), Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), Blocker counter, Deals from posters (RALPH_DEALS.md) — 2026-10-04, Final summary, Log (+3 more)

### Community 66 - "timed_offers.py (generator)"
Cohesion: 0.09
Nodes (22): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+14 more)

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.25
Nodes (7): Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, Page, Shop Stock Levels — min / max per shop, stocks report and next-month preparedness, Stocks report

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "update_np_weekly_history"
Cohesion: 0.29
Nodes (7): _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)., Ordinal among the month's perfect weeks (>=5 days in month), so the first FULL…, Snapshot each Sun–Sat week (sales, Kenya/Outside posts) into…, update_np_weekly_history()

### Community 71 - "_date"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "build"
Cohesion: 0.10
Nodes (23): build(), _d(), explain(), _fmt_d(), _load_json(), load_lines(), _market(), _month_end() (+15 more)

### Community 74 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

### Community 75 - "push_planner.py"
Cohesion: 0.10
Nodes (31): _kenya_target(), month_progress(), payload(), push_planner.py — Push Planner: what to push this week, where, and why bags…, Kenya's month target from current_performance.html (PERF.totalTarget), or None., Per market: sold this month so far (from the daily sales), days elapsed / left,…, _slim(), by_shop() (+23 more)

### Community 76 - "lib/offer_data.py"
Cohesion: 0.20
Nodes (12): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), offer_data.py ─────────────────────────────────────────────────────────────────… (+4 more)

### Community 77 - "os"
Cohesion: 0.09
Nodes (33): One-off: restore August's Offer Type figures into monthly_report_history.json…, calendar, collections, csv, datetime, lib — shared data-access for the marketing dashboard (Postgres migration).…, bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, monthly_sales.py — the current month's real bags sold, from Postgres. The… (+25 more)

### Community 78 - "data"
Cohesion: 0.14
Nodes (15): _db_count(), monthly_from_db(), Reporting month's subset count (e.g. rejectBags, giftBags) from…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,…, _live_bags(), {BAG (upper): official full price} from bag_original_prices.json (fallback)., _read_bag_prices(), _categories() (+7 more)

### Community 79 - "history.py"
Cohesion: 0.13
Nodes (21): dotenv, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers… (+13 more)

### Community 80 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), lib/theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 81 - "push_laya.py"
Cohesion: 0.14
Nodes (19): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+11 more)

### Community 82 - "build"
Cohesion: 0.28
Nodes (9): _alt_cost(), build(), _combo_cost(), _combo_slots(), Parse `const SMC = {…}` out of self_made_combos.html (no DB round-trip)., One combo alternative (e.g. 'Amaya Handbag') → its BOM production cost., Combo name → list of slots, each a list of alternative strings., Production cost = Σ over slots of the average matched-alternative cost. Same-… (+1 more)

### Community 83 - "facts"
Cohesion: 0.21
Nodes (12): _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, day(), ISO date n days before END (0 = END)., test_days_cover_is_none_when_nothing_sold(), test_first_sold_days_ago(), test_momentum_up_down_and_from_zero() (+4 more)

### Community 84 - "followup"
Cohesion: 0.18
Nodes (13): Did last week's calls work? (`push_rules.record_week`, `followup`), Last week's calls checked against what happened (lib/push_rules.followup), then…, weekly(), followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., Store this week's top actions under its Sunday. Re-running in the same week…, The most recent PREVIOUS week's calls and what happened since: sold/day since…, record_week() (+5 more)

### Community 85 - "label"
Cohesion: 0.33
Nodes (6): label(), 01 Sep – 30 Sep' (years added when the range crosses one or isn't this year)., Run script-only HTML in an invisible frame (same origin, so it can reach…, Fade the page area back in on a page that has no dashboard frame (password…, _reveal_page(), _run_js()

### Community 86 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.29
Nodes (6): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does

### Community 87 - "test_push_planner.py"
Cohesion: 0.16
Nodes (25): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m…, A facts row with sensible defaults, overridden by kw. (+17 more)

### Community 88 - "new_products.py"
Cohesion: 0.20
Nodes (7): _base_colour(), _merge_rows_by_base_colour(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across…, _strip_colour_qualifiers()

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.08
Nodes (20): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests, Agent skills — retail analytics, Test a skill (+12 more)

### Community 91 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.06
Nodes (36): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards) (+28 more)

### Community 92 - "_kind"
Cohesion: 0.67
Nodes (3): _kind(), HANDBAG' → 'handbags', 'SCHOOL BAG' → 'school bags', 'SPORT' → 'sport bags', ''…, test_kind_wording()

### Community 93 - "monthly_target_rows"
Cohesion: 0.18
Nodes (12): build(), Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), bag_posts(), tally(), {BAG: (posts this month, posts last week)} — Kenya posts (col E) from the two…, bag_key_fn(), key() (+4 more)

### Community 94 - "reject_variants"
Cohesion: 0.16
Nodes (15): _bucket(), kenya_stock_by_bag(), _parse_colour(), Which configured bag (if any) an Odoo/​sheet product name belongs to, by…, {BAG_UPPER: category} — the bag's category label only, from the product…, {BAG_UPPER: units} — physical stock summed per BAG TYPE from a repo CSV's UNITS…, First primary colour token found in a name (longest-first), Title-cased; '' if…, Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share… (+7 more)

### Community 95 - "month_end.py"
Cohesion: 0.27
Nodes (9): generator(), clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.…, YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that…, After the closing month's timed offers are safely in Supabase, empty the config…, run(), target_month() (+1 more)

### Community 96 - "odoo_weekly_breakdown"
Cohesion: 0.18
Nodes (12): odoo_weekly_breakdown(), _perfect_week_index(), Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, update_weekly_history(), _week_start(), is_pinned(), live_anchor() (+4 more)

### Community 97 - "market_summary"
Cohesion: 0.15
Nodes (12): _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region…, _region_goal(), _till_targets(), market_summary(), classify() for a market's tills over the month, with that month's offers; None… (+4 more)

### Community 98 - "_combo_button_usage"
Cohesion: 0.14
Nodes (11): _combo_button_usage(), _matches_sheet(), _opt_close(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Same slot count and every slot overlaps under SOME pairing (any order: the…, The sheet label this Odoo combo maps to, or None if it isn't on the sheet.…, _slots_fit() (+3 more)

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "check_connection"
Cohesion: 0.10
Nodes (22): build_offer(), odoo_bag_daily_value(), odoo_bag_prices(), odoo_bulk_lines(), odoo_daily_kenya(), odoo_list_price(), odoo_offer_price(), odoo_window_sales() (+14 more)

### Community 101 - "current_performance.html"
Cohesion: 0.50
Nodes (4): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance)

### Community 102 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 103 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.29
Nodes (7): lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, lib/report_month.py (which month are we reporting?), self_made_combos.html static page (reads const SMC), self_made_combos.py generator (build_payload + SQL + injection)

### Community 104 - "corporate_clients_from_db"
Cohesion: 0.40
Nodes (6): corporate_clients_from_db(), _months(), A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],…, Current month's corporate activity per client (quoted · invoiced · paid · sold)…, _txt()

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 107 - "get_rows"
Cohesion: 0.18
Nodes (12): load(), _build(), default_window(), get_rows(), last_complete_week(), _ok(), The most recent COMPLETE Sun–Sat week before `ref` (today) — what the sheet's…, {NORM(product): {SHOP: on-hand}} live, Kenya shops + Sinza (DAR) + Uganda (UG). (+4 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "Bags on offer vs not on offer"
Cohesion: 0.18
Nodes (11): Bags on offer vs not on offer, Buckets, Corporate-team till orders, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Regenerate, Shop birthdays (+3 more)

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "bags_on_offer.py"
Cohesion: 0.27
Nodes (10): _base_windows(), _custom_range(), fmt(), inject(), main(), bags_on_offer.py…, (from, to) dates from boo_custom_range.json — the Custom period — or None., Write (or with a=None, delete) the Custom period's dates. (+2 more)

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 121 - "live_month_window"
Cohesion: 0.22
Nodes (11): corporate_team_till_bags(), Bags of this month's till receipts paid by Corporate-team clients (a Corporate-…, month_window(), First → last calendar day of the LIVE month (today's month; see…, build(), load_targets(), (rows, total, base start, base end) for the month, from Odoo., {BAG: target units} for the month from product_targets_<YYYY-MM>.csv (built… (+3 more)

### Community 122 - "shops_efficiency.py"
Cohesion: 0.22
Nodes (7): metric_byshop(), parse_sheet(), shops_efficiency.py…, Return (data, meta) for the Kenya shops, locating columns by header name…, safe_int(), update_history(), pathlib

### Community 123 - "What the page shows"
Cohesion: 0.22
Nodes (8): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 3. Categories — % share, 4. Colours — % share, Bulk orders, Data, Product Performance — which bags, categories and colours carry the sales, and why, What the page shows

### Community 126 - "norm"
Cohesion: 0.13
Nodes (18): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, ({PRODUCT: {SHOP CODE: units}}, {PRODUCT: {SHOP CODE: [[colour, units], …]}})…, shop_sales(), _aliases(), build_rows(), _Deriver, _flag_cells() (+10 more)

### Community 128 - "_build_period"
Cohesion: 0.20
Nodes (6): _build_period(), _offer_types(), _pick_target(), Latest target row for `shop` with this period that overlaps [start, end]. A…, Matrix payload: rows, per-row category / tier cells, and the period's Top-5…, _region_of()

### Community 130 - "_resolve_bag"
Cohesion: 0.25
Nodes (9): _build_catalog(), _is_full_price(), _next_month(), bag(), Resolve any bag wording → (canonical BOM bag type, cost or None, in_bom).…, Every bag the user can pick for a slot, with two prices from the offers sheet:…, Reference-month combos matched to current Odoo stock, laid out like the offers…, _resolve_bag() (+1 more)

### Community 131 - "anchor"
Cohesion: 0.22
Nodes (9): count_complete_weeks_in_month(), Count Mon–Sun weeks in the reporting month that have ≥5 days falling within it., anchor(), month_key(), month_name(), month_window(), The date whose month is the reporting month: yesterday, unless pinned. Pinned…, (first day, last day) of the reporting month. There are no future sales rows,… (+1 more)

### Community 138 - "run_query"
Cohesion: 0.10
Nodes (24): daily_bags(), corporate_from_db(), corporate_target_from_db(), last_week_from_db(), Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, This month's Odoo corporate target {bags, kes} (sales_pos_target, scope…, _corporate_bags() (+16 more)

### Community 145 - "Shop Launch"
Cohesion: 0.29
Nodes (6): Config, Launch day, Marketing posts, Sales, Shop Launch, What the page shows

### Community 153 - "build"
Cohesion: 0.22
Nodes (8): _assign_price(), build(), reject_stock.csv → {BAG (upper): {units, colours:{COLOUR: units}}}., (price, flag) from BOM cost — two tiers. flag ∈ {'', 'thin', 'below', 'nobom'}., Write an Excel (xlsx, or CSV fallback) of EVERYTHING on the pricing board —…, _read_overrides(), _read_stock(), _write_export()

### Community 154 - "base_name"
Cohesion: 0.25
Nodes (9): apply_walkins(), base_name(), dispatch_by_product_shop(), _num(), The catalogue key for an Odoo product name: norm() without the "[REJECT]" tag…, {NORM(product): {SHOP: bags}} of POS bag sales in [start, end]; None if DB…, {NORM(product): {SHOP: bags distributed in}} from combined_distribution.sql's…, sales_by_product_shop() (+1 more)

### Community 155 - "_mkt_week_label"
Cohesion: 0.29
Nodes (7): _mkt_perfect_week_index(), _mkt_week_label(), Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]., current = {region: {key: {productName,colour,category,bagType,stock}}}. A new…, update_clearance(), update_mkt_history()

### Community 156 - "load_catalog"
Cohesion: 0.29
Nodes (6): categories(), {BAG: category} — the bag type's usual catalogue category, else its Odoo…, catalog_rows(), load_catalog(), [{colour, category, name, bag}] in sheet order, from product_catalog.csv., [header] + [[COLOUR, CATEGORY, PRODUCT NAME, BAG TYPE], …] — the label columns…

### Community 157 - "type_fn"
Cohesion: 0.17
Nodes (16): load_posts(), num(), tally(), ({BAG: [kenya, outside]} last week, {BAG: [kenya, outside]} this month) from…, build(), ({TYPE: Kenya shop on-hand}, {TYPE: Sinza + Uganda on-hand}) — live Odoo., The NP.runway payload: {days, bags: [{name, created, category, stockKe,…, Product name → bag type (see the module docstring). (+8 more)

### Community 158 - "get_engine"
Cohesion: 0.29
Nodes (7): _env(), get_engine(), Engine, The process's reused connection (opened on first query). Every generator runs…, Build a SQLAlchemy URL from the environment, or None if unset. Accepts…, _shared_conn(), _url()

### Community 159 - "odoo_month_product_bags"
Cohesion: 0.33
Nodes (6): odoo_combo_product_bags(), odoo_lifetime_product_bags(), odoo_month_product_bags(), All-time bags per product from Odoo (no month window) — the lifetime sales of…, [(product name, bags)] for bags sold INSIDE combos (sub_product_line) in the…, Reporting month's bags per product from Odoo (Postgres), or None if the DB…

### Community 160 - "product_targets_workbook.py"
Cohesion: 0.33
Nodes (5): openpyxl, openpyxl_comments, openpyxl_styles, openpyxl_utils, product_targets_workbook.py — the month's bag targets as an Excel workbook with…

### Community 161 - "_read_offers"
Cohesion: 0.40
Nodes (5): Offer type summary (matrix), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, _read_offers(), _read_offers_cache()

### Community 162 - "generate_insights.py"
Cohesion: 0.20
Nodes (7): card(), esc(), fmt(), generate_insights.py…, read_block(), region_card(), html()

### Community 163 - "_category_of"
Cohesion: 0.40
Nodes (5): _apply_alias(), Apply bag aliases, longest key first (so 'STANDARD TRAVEL' wins over…, _category_of(), _norm_cat(), Category for a bag: the offers-sheet category (col C), else a keyword fallback.

### Community 164 - "_build_sheet_slots"
Cohesion: 0.50
Nodes (4): _build_sheet_slots(), _combo_sheet_slots(), Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]., [(label, slots)] for each running combo on the offer sheet (skips the TOTAL…

### Community 165 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

### Community 166 - "_load_source"
Cohesion: 0.50
Nodes (4): _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…

### Community 167 - "_read_bom_costs"
Cohesion: 0.50
Nodes (4): {BAG TYPE (upper): production cost} from bom_costs.json — the local copy of the…, _read_bom_costs(), _bom_costs(), {BAG (upper): cost} from bom_costs.json (via offer_picking._read_bom_costs).…

### Community 168 - "_load_combos_by_shop"
Cohesion: 0.67
Nodes (4): _load_combos_by_shop(), _from_file(), _nonempty(), Per-shop combo / power-deal view for the panel — built **live from Odoo** via…

### Community 169 - "prime_offer_flags"
Cohesion: 0.50
Nodes (4): offer_flags(), prime_offer_flags(), Seed offer_flags() from MONTHLY_TARGET rows the caller already read (saves a…, {BAG TYPE: (kenya, sinza, uganda) on-offer bools} from MONTHLY_TARGET cols…

### Community 170 - "master_products"
Cohesion: 0.50
Nodes (4): master_products(), _norm_name(), Match the SQL normalisation: lower-case, '.'→space, collapse whitespace., Normalised, de-duplicated master catalogue names (master_products.txt), for the…

## Knowledge Gaps
- **197 isolated node(s):** `PERF`, `graphify`, `Use in another project`, `Test a skill`, `Inputs you must build from the project's data` (+192 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 915 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_query()` connect `run_query` to `fetch_posting_data`, `tests/test_receipt_combos.py`, `generators/self_made_combos.py`, `stock.py`, `build_payload`, `family`, `shop_corporate.py`, `base_name`, `_enrich_deals`, `fetch`, `odoo_month_product_bags`, `get_engine`, `type_fn`, `_seasonality`, `main`, `build_payload`, `shop_launch.py`, `_combo_button_usage`, `fetch_new_products_data`, `_enrich_deals`, `build`, `os`, `odoo_weekly_breakdown`, `market_summary`, `_combo_button_usage`, `check_connection`, `corporate_clients_from_db`, `_bags_not_on_offer`, `live_month_window`, `norm`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `build_payload()` connect `build_payload` to `market_summary`, `monthly_report.py`, `_seasonality`, `_combo_button_usage`, `generators/self_made_combos.py`, `run_query`, `bag_classifier`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `bag_classifier()` connect `bag_classifier` to `market_summary`, `load_data`, `generators/self_made_combos.py`, `Bags on offer vs not on offer`, `fetch`, `main`, `Self-made combos vs running combos (doc)`, `Push Planner (`push_planner.py` → `push_planner.html`, `PP`)`, `oos_callbacks.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `fetch()` (e.g. with `classify()` and `oos_key()`) actually correct?**
  _`fetch()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `PERF`, `graphify`, `Use in another project` to the rest of the system?**
  _197 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `fetch_posting_data` be split into smaller, more focused modules?**
  _Cohesion score 0.05203442879499218 - nodes in this community are weakly interconnected._
- **Should `laya.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._