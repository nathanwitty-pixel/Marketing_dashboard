# Graph Report - Marketing_dashboard  (2026-10-14)

## Corpus Check
- 192 files · ~786,292 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 16 file(s) not represented in the graph (top: .csv 9, (none) 2, .toml 1)

## Summary
- 2124 nodes · 4027 edges · 150 communities (115 shown, 35 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 156 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7b29f467`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- posting_yields.py
- _ask
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
- bag_quant.py
- custom_range.py
- month_extras.py
- stock.py
- publish.py
- datetime
- build_payload
- fetch_posting_data
- shop_corporate.py
- push_planner.py
- lib/db.py
- Self-made combos vs running combos (doc)
- shops_efficiency.py
- signals
- self_made_combos_bundle/lib/db.py
- Dashboard Menu Docs (spec index)
- _mkt_week_label
- _enrich_deals
- fetch
- insights.html
- streamlit_app.py
- current_performance.py
- monthly_report.py
- _seasonality
- chronos_train.py
- reject_sales.py
- build_payload
- Shops Efficiency Tracking spec doc
- os
- moves
- lib/offer_data.py
- page_sidebar.js
- Month-End Routine
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
- bags_on_offer.py
- _enrich_deals
- High-End Visual Design skill
- followup
- test_sheet_reads.py
- oos_callbacks.py
- daydream skill (Vault Daydream)
- sys
- OOS call-back progress (Ralph loop log)
- timed_offers.py (generator)
- _alignment_region
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- lib/report_month.py
- _date
- marketing_dashboard.sql
- num
- test_share_targets.py
- shop_birthdays.py
- _build_period
- monthly_target_rows
- fetch
- history.py
- theme.py
- push_laya.py
- live_month_window
- test_push_planner.py
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- re
- Chart type switcher (every chart, every menu)
- F
- update_np_weekly_history
- test_stockout_demand.py
- Out-of-stock demand — people, not requests
- Bags on offer vs not on offer
- push_rules.py
- load_pages
- reject_variants
- get_engine
- Product (bag) targets
- _apply_receipt_offers
- _combo_button_usage
- Bag Signals — quant view of each bag (posting · stock · selling)
- check_connection
- current_performance.html
- attach
- self_made_combos.py generator (build_payload + SQL + injection)
- corporate_clients_from_db
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- forward_projections.py
- self_made_combos_bundle/self_made_combos.py
- Ralph task — only three sheet tabs left
- _bag_stock
- Bag targets October 2026_3acbad00.md
- _bag_tiers
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- last_week_from_db
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- colours.py
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- odoo_tabs.py
- POST_DATA data block (Posting)
- data
- read_block(file, start, end) function
- ambiguous_python_import_17686b6faac5
- contextlib
- run_query
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- generate_insights.py

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 51 edges
2. `fetch()` - 39 edges
3. `fetch_posting_data()` - 35 edges
4. `build_payload()` - 30 edges
5. `check_connection()` - 28 edges
6. `get_gspread_client()` - 28 edges
7. `data()` - 25 edges
8. `build_payload()` - 24 edges
9. `build_offer()` - 22 edges
10. `F()` - 22 edges

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

## Communities (150 total, 35 thin omitted)

### Community 0 - "posting_yields.py"
Cohesion: 0.13
Nodes (35): _analyze_region(), _build_no_convert(), _fetch_monthly_kenya(), _fetch_sinza_monthly(), _fetch_sinza_weekly(), _fetch_uganda_monthly(), _fetch_uganda_weekly(), _fetch_weekly_kenya() (+27 more)

### Community 1 - "_ask"
Cohesion: 0.08
Nodes (21): Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket(), _cache_get(), _cache_put() (+13 more)

### Community 2 - "tests/test_receipt_combos.py"
Cohesion: 0.09
Nodes (43): What the page shows (per period), _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, bag_key(), classify(), _fits(), _groups(), load_offers() (+35 more)

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
Cohesion: 0.15
Nodes (16): Counted by how it was sold, _bag_sales_daily_sql(), _bag_sales_sql(), dow_tier_weeks(), fmt(), inject(), _load_shop_regions(), main() (+8 more)

### Community 8 - "timed_offers.py"
Cohesion: 0.18
Nodes (13): Kenya timed-offer campaigns from timed_offers_config.json (normalised by…, _timed_offers(), _bags_from_file(), _derive_month(), load_config(), _norm_offer(), timed_offers.py…, Multi-offer config: {"month": "YYYY-MM", "offers": [offer, ...]}. Back-compat:… (+5 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "test_product_targets.py"
Cohesion: 0.24
Nodes (10): allocate(), available_days(), Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for lib/product_targets.py (bag targets from Odoo; spec docs/product-…, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating(), test_new_bag_is_scaled_to_the_days_it_was_in_shops() (+2 more)

### Community 12 - "bag_quant.py"
Cohesion: 0.17
Nodes (18): collections, action(), _mean(), _phi(), posting_beta(), lib/bag_quant.py — quant signals per bag: drift, volatility, Sharpe-style…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not… (+10 more)

### Community 13 - "custom_range.py"
Cohesion: 0.17
Nodes (15): calendar, block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each… (+7 more)

### Community 14 - "month_extras.py"
Cohesion: 0.25
Nodes (13): _bags_on_offer(), _block(), build_extras(), _deals(), _pick(), _posting(), _posting_block(), region() (+5 more)

### Community 15 - "stock.py"
Cohesion: 0.17
Nodes (16): odoo_stock_levels(), Live per-shop Odoo on-hand in the SAME shape parse_sheet(STOCK_LEVELS) returns:…, lib — shared data-access for the marketing dashboard (Postgres migration).…, _codes_for(), _inlist(), odoo_stock_at_location(), odoo_stock_by_product(), odoo_stock_by_shop_code() (+8 more)

### Community 16 - "publish.py"
Cohesion: 0.23
Nodes (13): argparse, fnmatch, py_compile, changed_files(), git(), group(), is_secret(), main() (+5 more)

### Community 17 - "datetime"
Cohesion: 0.09
Nodes (17): datetime, _base_colour(), _merge_rows_by_base_colour(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across…, _strip_colour_qualifiers() (+9 more)

### Community 18 - "build_payload"
Cohesion: 0.06
Nodes (38): _bags_not_on_offer(), _infer(), _norm(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups() (+30 more)

### Community 19 - "fetch_posting_data"
Cohesion: 0.10
Nodes (18): _onoff(), _bt_on_offer(), count_complete_weeks_in_month(), _dead_clear(), fetch_posting_data(), _clear(), _yield(), load_dead_thresholds() (+10 more)

### Community 20 - "shop_corporate.py"
Cohesion: 0.20
Nodes (19): _acronym(), build(), _maybe(), owns(), _d(), _domain(), _phone9(), lib/shop_corporate.py — corporate orders the SHOPS handle (Sales popover, "Shop… (+11 more)

### Community 21 - "push_planner.py"
Cohesion: 0.12
Nodes (23): add_laya(), build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), main() (+15 more)

### Community 22 - "lib/db.py"
Cohesion: 0.13
Nodes (16): lib — shared data-access for the marketing dashboard (Postgres migration).…, main(), month_window(), _query_ready(), monthly_sales.py — the current month's real bags sold, from Postgres. The…, First → last calendar day of the LIVE month (today's month; see…, offer_picking.py…, Save a local, human-editable copy of the offers prices to OFFERS_CACHE. (+8 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.06
Nodes (45): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Current Performance (doc), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), New Products Analytics (doc) (+37 more)

### Community 24 - "shops_efficiency.py"
Cohesion: 0.06
Nodes (37): build_period(), distributed_in(), main(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only., Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).… (+29 more)

### Community 25 - "signals"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

### Community 26 - "self_made_combos_bundle/lib/db.py"
Cohesion: 0.16
Nodes (17): check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, Run a read query and return a DataFrame, or None if the DB is unreachable.… (+9 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.18
Nodes (14): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes) (+6 more)

### Community 28 - "_mkt_week_label"
Cohesion: 0.29
Nodes (7): _mkt_perfect_week_index(), _mkt_week_label(), Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]., current = {region: {key: {productName,colour,category,bagType,stock}}}. A new…, update_clearance(), update_mkt_history()

### Community 29 - "_enrich_deals"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "fetch"
Cohesion: 0.13
Nodes (24): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), combo_slots(), make_classifier() (+16 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.07
Nodes (28): cache_resource, SCRIPT_TIMEOUT = 600s config, fragment, html, streamlit, _bg_done_msg(), _bg_jobs(), _bg_rebuild() (+20 more)

### Community 33 - "current_performance.py"
Cohesion: 0.09
Nodes (13): corporate_from_db(), corporate_target_from_db(), _db_count(), fetch_monthly_target(), monthly_from_db(), current_performance.py…, Reporting month's subset count (e.g. rejectBags, giftBags) from…, Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't… (+5 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.15
Nodes (9): _cause(), esc(), fmt(), ladder_strip(), pct(), monthly_report.py…, _self_made_combos(), _smc_srow() (+1 more)

### Community 35 - "_seasonality"
Cohesion: 0.15
Nodes (16): Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), _build_sheet_slots(), _combo_norm_option(), _combo_odoo_slots(), _combo_sheet_slots() (+8 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.12
Nodes (29): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+21 more)

### Community 37 - "reject_sales.py"
Cohesion: 0.06
Nodes (41): Offer type summary (matrix), _alt_cost(), _apply_alias(), build(), _build_catalog(), _combo_cost(), _combo_slots(), _is_full_price() (+33 more)

### Community 38 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "os"
Cohesion: 0.09
Nodes (26): _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., build(), _cfg(), first_sale(), kenya_posts(), load_workplan() (+18 more)

### Community 41 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 42 - "lib/offer_data.py"
Cohesion: 0.20
Nodes (12): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), offer_data.py ─────────────────────────────────────────────────────────────────… (+4 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

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
Cohesion: 0.18
Nodes (16): _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, _run_one(), run_scripts(), start_server(), copyfile(), do_GET() (+8 more)

### Community 52 - "scripts/test_receipt_combos.py"
Cohesion: 0.08
Nodes (42): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+34 more)

### Community 53 - "fetch_new_products_data"
Cohesion: 0.16
Nodes (16): fetch_new_products_data(), _apply_stock(), _post_lookup(), is_checked(), _key(), _keyed(), _np_week_bags(), odoo_sales_window() (+8 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.17
Nodes (12): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+4 more)

### Community 56 - "bag_classifier"
Cohesion: 0.19
Nodes (14): _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _load_bag_prices(), _norm_combo() (+6 more)

### Community 57 - "bags_on_offer.py"
Cohesion: 0.19
Nodes (13): _base_windows(), _custom_range(), fmt(), inject(), main(), _new_products(), _previous_payload(), bags_on_offer.py… (+5 more)

### Community 58 - "_enrich_deals"
Cohesion: 0.16
Nodes (9): _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,… (+1 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 61 - "test_sheet_reads.py"
Cohesion: 0.60
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 62 - "oos_callbacks.py"
Cohesion: 0.05
Nodes (61): Out of stock — call back, fixture, match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, aggregate(), flat(), split(), attach_stock() (+53 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "sys"
Cohesion: 0.08
Nodes (29): http_server, generator(), ensure_firewall_rule(), free_port(), get_lan_ip(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py… (+21 more)

### Community 65 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.15
Nodes (11): _local_deal_rows(), Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), Blocker counter, Deals from posters (RALPH_DEALS.md) — 2026-10-04, Final summary, Log (+3 more)

### Community 66 - "timed_offers.py (generator)"
Cohesion: 0.09
Nodes (22): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+14 more)

### Community 67 - "_alignment_region"
Cohesion: 0.17
Nodes (14): _alignment_region(), _for(), _sold(), _stk(), _units(), _dead_stock_region(), pct(), summarise() (+6 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "lib/report_month.py"
Cohesion: 0.17
Nodes (16): anchor(), is_pinned(), live_anchor(), live_month_key(), month_key(), month_name(), month_window(), _pinned() (+8 more)

### Community 71 - "_date"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "num"
Cohesion: 0.20
Nodes (11): _garr_line(), gnum(), num(), _offers(), _parse_offers(), _units(), This month's timed-offer campaigns, flattened for storage. The live TO payload…, Greedy single-line array extractor — handles nested [[...],[...]] arrays. (+3 more)

### Community 74 - "test_share_targets.py"
Cohesion: 0.22
Nodes (11): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+3 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "_build_period"
Cohesion: 0.20
Nodes (6): _build_period(), _offer_types(), _pick_target(), Latest target row for `shop` with this period that overlaps [start, end]. A…, Matrix payload: rows, per-row category / tier cells, and the period's Top-5…, _region_of()

### Community 77 - "monthly_target_rows"
Cohesion: 0.18
Nodes (12): build(), Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), bag_posts(), tally(), {BAG: (posts this month, posts last week)} — Kenya posts (col E) from the two…, bag_key_fn(), key() (+4 more)

### Community 78 - "fetch"
Cohesion: 0.17
Nodes (11): _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…, _bags_not_on_offer(), fetch(), Bags with sales this month (in the market `sql` scopes to) that are on NO…, The component bag names across a region's sheet combos/singles/specials cards… (+3 more)

### Community 79 - "history.py"
Cohesion: 0.13
Nodes (21): dotenv, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers… (+13 more)

### Community 80 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), lib/theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 81 - "push_laya.py"
Cohesion: 0.13
Nodes (20): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+12 more)

### Community 82 - "live_month_window"
Cohesion: 0.22
Nodes (11): base_period(), build(), load_targets(), The three complete months before month_start → (start, end)., (rows, total, base start, base end) for the month, from Odoo., {BAG: target units} for the month from product_targets_<YYYY-MM>.csv (built…, {BAG: col C} from MONTHLY_TARGET — for the comparison column only., _sheet_targets() (+3 more)

### Community 83 - "test_push_planner.py"
Cohesion: 0.18
Nodes (18): Per bag × market: the facts (`push_rules.facts`, `add_peers`), add_peers(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m…, ISO date n days before END (0 = END). (+10 more)

### Community 84 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

### Community 85 - "re"
Cohesion: 0.22
Nodes (7): One-off: restore August's Offer Type figures into monthly_report_history.json…, master_products(), _norm_name(), lib/queries.py — SQL for the Litmus Postgres source of truth (Odoo POS). Bags…, Match the SQL normalisation: lower-case, '.'→space, collapse whitespace., Normalised, de-duplicated master catalogue names (master_products.txt), for the…, re

### Community 86 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.29
Nodes (6): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does

### Community 87 - "F"
Cohesion: 0.15
Nodes (24): action(), context(), (code, plain sentence, units at stake, confidence 0..1) for one bag × market.…, What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F() (+16 more)

### Community 88 - "update_np_weekly_history"
Cohesion: 0.29
Nodes (7): _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)., Ordinal among the month's perfect weeks (>=5 days in month), so the first FULL…, Snapshot each Sun–Sat week (sales, Kenya/Outside posts) into…, update_np_weekly_history()

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.08
Nodes (20): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests, Agent skills — retail analytics, Test a skill (+12 more)

### Community 91 - "Bags on offer vs not on offer"
Cohesion: 0.05
Nodes (46): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards) (+38 more)

### Community 92 - "push_rules.py"
Cohesion: 0.11
Nodes (17): _cover_txt(), _days_back(), _kind(), _n(), not_moving(), posting_median(), rank(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).… (+9 more)

### Community 93 - "load_pages"
Cohesion: 0.29
Nodes (7): read_block(), read_block(), _read_timed_offers(), load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, html()

### Community 94 - "reject_variants"
Cohesion: 0.19
Nodes (13): _bucket(), kenya_stock_by_bag(), _parse_colour(), Which configured bag (if any) an Odoo/​sheet product name belongs to, by…, {BAG_UPPER: category} — the bag's category label only, from the product…, First primary colour token found in a name (longest-first), Title-cased; '' if…, Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share…, Per-[REJECT]-product variant rows for a name-filtered offer, for the filterable… (+5 more)

### Community 95 - "get_engine"
Cohesion: 0.29
Nodes (7): _env(), get_engine(), Engine, The process's reused connection (opened on first query). Every generator runs…, Build a SQLAlchemy URL from the environment, or None if unset. Accepts…, _shared_conn(), _url()

### Community 96 - "Product (bag) targets"
Cohesion: 0.29
Nodes (6): No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 97 - "_apply_receipt_offers"
Cohesion: 0.25
Nodes (6): _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region…, _region_goal(), _till_targets()

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

### Community 106 - "forward_projections.py"
Cohesion: 0.13
Nodes (13): fetch_sheet_data(), odoo_weekly_breakdown(), _perfect_week_index(), forward_projections.py…, Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, update_weekly_history(), _week_start() (+5 more)

### Community 107 - "self_made_combos_bundle/self_made_combos.py"
Cohesion: 0.32
Nodes (7): fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py…, Read the Shop → Region table from docs/shop-regions.md so the mapping can be…, pathlib

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "_bag_stock"
Cohesion: 0.40
Nodes (5): _bag_stock(), _combo_bags(), _norm_bag(), Space/punctuation-insensitive key so 'MINIZURI' matches 'MINI ZURI'., Component bags of an offer, each with its stock, sorted most-stock first.

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 114 - "last_week_from_db"
Cohesion: 0.25
Nodes (8): last_week_from_db(), Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary(), week_start_of(), weekly_from_db()

### Community 122 - "colours.py"
Cohesion: 0.43
Nodes (6): csv, family(), _load(), _norm(), lib/colours.py — colour FAMILY of a product (Brown, Black, Red, Beige, Grey,…, Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…

### Community 126 - "odoo_tabs.py"
Cohesion: 0.08
Nodes (43): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, _aliases(), base_name(), _build(), build_rows(), catalog_rows(), default_window() (+35 more)

### Community 128 - "data"
Cohesion: 0.14
Nodes (14): cache_data, _live_bags(), {BAG (upper): official full price} from bag_original_prices.json (fallback)., _read_bag_prices(), load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if… (+6 more)

### Community 138 - "run_query"
Cohesion: 0.12
Nodes (18): _corporate_bags(), Corporate bags sold in the given month, live from Odoo invoices. Returns 0 when…, odoo_combo_product_bags(), odoo_lifetime_product_bags(), odoo_month_product_bags(), All-time bags per product from Odoo (no month window) — the lifetime sales of…, [(product name, bags)] for bags sold INSIDE combos (sub_product_line) in the…, Reporting month's bags per product from Odoo (Postgres), or None if the DB… (+10 more)

### Community 145 - "Shop Launch"
Cohesion: 0.29
Nodes (6): Config, Launch day, Marketing posts, Sales, Shop Launch, What the page shows

### Community 162 - "generate_insights.py"
Cohesion: 0.24
Nodes (5): card(), esc(), fmt(), generate_insights.py…, region_card()

## Knowledge Gaps
- **185 isolated node(s):** `Log`, `Added mid-task (user)`, `Monthly inputs (user uploads)`, `Steps (verify each)`, `Sheet: Bag targets` (+180 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 871 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Bags on offer vs not on offer` connect `Bags on offer vs not on offer` to `tests/test_receipt_combos.py`, `reject_sales.py`, `oos_callbacks.py`, `generators/self_made_combos.py`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `Monthly Report (doc)` connect `Self-made combos vs running combos (doc)` to `Bags on offer vs not on offer`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `bag_classifier()` connect `bag_classifier` to `Product (bag) targets`, `data`, `_apply_receipt_offers`, `generators/self_made_combos.py`, `fetch`, `Push Planner (`push_planner.py` → `push_planner.html`, `PP`)`, `push_planner.py`, `fetch`, `Bags on offer vs not on offer`, `oos_callbacks.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `fetch()` (e.g. with `classify()` and `oos_key()`) actually correct?**
  _`fetch()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Log`, `Added mid-task (user)`, `Monthly inputs (user uploads)` to the rest of the system?**
  _185 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `posting_yields.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12762762762762764 - nodes in this community are weakly interconnected._
- **Should `_ask` be split into smaller, more focused modules?**
  _Cohesion score 0.08374384236453201 - nodes in this community are weakly interconnected._