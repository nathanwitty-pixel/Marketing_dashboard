# Graph Report - Marketing_dashboard  (2026-10-28)

## Corpus Check
- 230 files · ~1,099,449 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: .csv 13, (none) 2, .toml 1)

## Summary
- 2619 nodes · 5071 edges · 196 communities (154 shown, 42 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 189 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c4ed74cf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- shop_corporate.py
- laya.py
- self_made_combos_bundle/lib/__init__.py
- oos_chip.js
- chart_switcher.js
- graw(block, key) function (bare numeric getter)
- Kitengela Rejects tracker (timed offer)
- push_rules.py
- publish.py
- v5_theme.js
- name_match.py
- bare_minimum setting (weekly target floor)
- lib/offer_data.py
- current_performance.py
- month_extras.py
- marketing_posts.py
- scripts/test_receipt_combos.py
- oos_callbacks.py
- build_payload
- _combo_button_usage
- sticky_controls.js
- timed_offers.py
- _matches_sheet
- Self-made combos vs running combos (doc)
- shop_stock_levels.py
- snapshot.py
- shop_requests.py
- Dashboard Menu Docs (spec index)
- new_products.py
- _enrich_deals
- chronos_preview.py
- insights.html
- streamlit_app.py
- odoo_tabs.py
- monthly_report.py
- lib/report_month.py
- chronos_train.py
- run_query
- build_payload
- Shops Efficiency Tracking spec doc
- ads_panel.js
- shop_launch.py
- os
- page_sidebar.js
- generators/self_made_combos.py
- Combos & Power Deals by Shop panel (#combo-shop)
- self_made_combos_bundle/offer_data.py
- Self-made combos bundle Python dependencies (requirements.txt)
- CLAUDE.md
- history.py (read months back)
- Self-made combos vs Running combos portable bundle README
- start_server
- shops_efficiency.py
- Bags on offer vs not on offer
- algorithmic-art skill
- dataviz-charts skill
- data
- build_offer
- bag_classifier
- High-End Visual Design skill
- Monthly Report (doc)
- self_made_combos_bundle/self_made_combos.py
- _bg_jobs
- daydream skill (Vault Daydream)
- _enrich_deals
- Month-End Routine
- colours.py
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- signals
- forward_projections.py
- marketing_dashboard.sql
- safe_int
- queries.py
- shop_birthdays.py
- push_planner.py
- Denri Africa Dashboard Design System (skill)
- offer_picking.py
- month_end.py
- theme.py
- push_laya.py
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- test_push_planner.py
- get_engine
- moves
- num
- F
- load_pages
- datetime
- Out-of-stock demand — people, not requests
- shop-birthdays.md
- run.py
- _combo_button_usage
- runway_bags.py
- negative_fixes.py
- custom_range.py
- product_targets.py
- shop_regions.py
- Bag Signals — quant view of each bag (posting · stock · selling)
- excluded_products
- current_performance.html
- attach
- self_made_combos.py generator (build_payload + SQL + injection)
- OOS call-back progress (Ralph loop log)
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- reject_variants
- posting_yields.py
- Ralph task — only three sheet tabs left
- _base_colour
- Bag targets October 2026_3acbad00.md
- odoo_month_product_bags
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- generator
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- bag_quant.py
- bags_on_offer.py
- What the page shows
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- Product (bag) targets
- POST_DATA data block (Posting)
- _bg_rebuild
- read_block(file, start, end) function
- pos_lines.py
- product_performance.py
- _reveal_page
- contextlib
- Chart type switcher (every chart, every menu)
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- New Products Analytics (doc)
- ads.py
- Offer Picking (doc)
- weekly_sales.py
- _month_archived
- footfall.py
- scripts/receipt_combos.py
- _fetch_sinza_monthly
- posts_lead_sales
- generate_insights.py
- Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)
- followup
- _bags_not_on_offer
- lib/db.py
- Footfall and Marketing (21 Oct 2026, user's call)
- timed_offers.py (generator)
- Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)
- Bag signals — quant finance applied to product sales
- re
- Product Performance — Shop breakdown: progress
- _bag_stock
- norm
- Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)
- check_connection
- sendable_by_month_end
- history.py
- build
- json
- fetch_posting_data
- Ralph loop brief — Footfall and Marketing page
- sys
- build
- ambiguous_python_import_17686b6faac5
- main.py
- _apply_receipt_offers
- _dead_stock_region
- _alignment_region
- Combos from receipts — running vs self-made
- Sales-share targets per product

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 81 edges
2. `fetch()` - 41 edges
3. `fetch_posting_data()` - 38 edges
4. `check_connection()` - 33 edges
5. `data()` - 33 edges
6. `get_gspread_client()` - 32 edges
7. `build_payload()` - 30 edges
8. `build()` - 25 edges
9. `build_payload()` - 24 edges
10. `excluded_products()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Sales pace to month end (19 Oct 2026)` --references--> `month_end_lift()`  [INFERRED]
  docs/shop-stock-levels.md → generators/shop_stock_levels.py
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

## Communities (196 total, 42 thin omitted)

### Community 0 - "shop_corporate.py"
Cohesion: 0.17
Nodes (22): _acronym(), build(), _maybe(), owns(), corporate_team_receipts(), _d(), _domain(), _phone9() (+14 more)

### Community 1 - "laya.py"
Cohesion: 0.09
Nodes (26): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket() (+18 more)

### Community 2 - "self_made_combos_bundle/lib/__init__.py"
Cohesion: 0.08
Nodes (44): What the page shows (per period), lib — shared data-access for the marketing dashboard (Postgres migration).…, _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, bag_key(), classify(), _fits(), _groups() (+36 more)

### Community 3 - "oos_chip.js"
Cohesion: 0.08
Nodes (38): attach(), close(), esc(), form(), go(), iso(), mountPanel(), open() (+30 more)

### Community 4 - "chart_switcher.js"
Cohesion: 0.12
Nodes (35): alpha(), apply(), attach(), axisOpts(), build(), changeTxt(), Chart(), clone() (+27 more)

### Community 6 - "Kitengela Rejects tracker (timed offer)"
Cohesion: 0.07
Nodes (28): bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source), Offline fallback pattern (mirror sheet data to local JSON), Reject Sale (doc: reject_sales.py -> reject_sales.html, RJ), reject_sales_export.csv (fallback export) (+20 more)

### Community 7 - "push_rules.py"
Cohesion: 0.10
Nodes (21): action(), _cover_txt(), _kind(), _n(), not_moving(), posting_median(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).…, {market: median postsMonth of the bags that were posted at all} — the 'below… (+13 more)

### Community 8 - "publish.py"
Cohesion: 0.29
Nodes (11): fnmatch, py_compile, changed_files(), git(), group(), is_secret(), main(), publish.py — one-click, VERIFIED publish of the dashboard to GitHub (Streamlit… (+3 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 12 - "lib/offer_data.py"
Cohesion: 0.20
Nodes (12): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), offer_data.py ─────────────────────────────────────────────────────────────────… (+4 more)

### Community 13 - "current_performance.py"
Cohesion: 0.07
Nodes (25): corporate_clients_from_db(), corporate_from_db(), corporate_target_from_db(), _db_count(), last_week_from_db(), monthly_from_db(), _months(), current_performance.py… (+17 more)

### Community 14 - "month_extras.py"
Cohesion: 0.25
Nodes (13): _bags_on_offer(), _block(), build_extras(), _deals(), _pick(), _posting(), _posting_block(), region() (+5 more)

### Community 15 - "marketing_posts.py"
Cohesion: 0.22
Nodes (16): _bag_category(), _category(), daily(), _date(), _num(), parse(), posts(), lib/marketing_posts.py — marketing POSTS per bag, from marketing's own daily… (+8 more)

### Community 16 - "scripts/test_receipt_combos.py"
Cohesion: 0.32
Nodes (15): classify(), lines: [{receipt, d, product, qty, amount}] → per-market summary: {running:…, infer(), L(), Tests for receipt_combos.py + name_match.py — python -m pytest scripts -q, test_alternatives_and_singles(), test_bulk_receipts_are_not_combos(), test_four_bags_at_two_prices_are_two_combos() (+7 more)

### Community 17 - "oos_callbacks.py"
Cohesion: 0.05
Nodes (60): Out of stock — call back, fixture, match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, bag(), aggregate(), flat(), split() (+52 more)

### Community 18 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 19 - "_combo_button_usage"
Cohesion: 0.22
Nodes (8): _combo_button_usage(), _combo_norm_option(), combos_by_shop(), _norm(), _tokmatch(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Per-shop view for Shops Efficiency, keyed by shop-location label (e.g.…, One combo slot-option → its distinctive bag token(s), colours/category words…

### Community 20 - "sticky_controls.js"
Cohesion: 0.20
Nodes (15): bind(), embedHost(), headerOf(), init(), initSections(), injectCss(), place(), setPinned() (+7 more)

### Community 21 - "timed_offers.py"
Cohesion: 0.13
Nodes (19): _acc(), _bags_from_file(), build_compare(), _cmp_lines(), _days(), _derive_month(), load_config(), _norm_offer() (+11 more)

### Community 22 - "_matches_sheet"
Cohesion: 0.20
Nodes (9): _matches_sheet(), _opt_close(), Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Same slot count and every slot overlaps under SOME pairing (any order: the…, The sheet label this Odoo combo maps to, or None if it isn't on the sheet.…, _slots_fit(), Inputs (from the user, Oct 2026), Ralph task — Sinza & Uganda offers + receipt-based combo counting (+1 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.18
Nodes (13): Bags not on offer per market (Kenya/Sinza/Uganda), Combo button usage / rung vs pot. (till check), Self-made combos vs running combos (doc), DoW mirror shops (DOW_MIRROR), Monetary implication panel (bundling discount), Rank chip (follows active Sort filter), Running-combo classification by bag composition (slot-aware sheet match), Standalone SQL (self_made_vs_running_combos.sql) (+5 more)

### Community 24 - "shop_stock_levels.py"
Cohesion: 0.12
Nodes (28): What each page shows, bag_categories(), buffer_stock(), build(), dispatch_shop(), fit(), grand_total(), leads() (+20 more)

### Community 25 - "snapshot.py"
Cohesion: 0.18
Nodes (16): _age_min(), _cleanup(), fresh_meta(), _meta(), _p(), query(), lib/snapshot.py — local DuckDB snapshot of the tills (docs/README.md › DuckDB…, The snapshot to read, refreshing it first when it's too old; None if there's… (+8 more)

### Community 26 - "shop_requests.py"
Cohesion: 0.14
Nodes (21): _onoff(), Shop requests vs received (this month · last month) and the production approved…, requests_block(), _d(), _f(), _match(), _offer_label(), _offers() (+13 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.18
Nodes (14): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes) (+6 more)

### Community 28 - "new_products.py"
Cohesion: 0.12
Nodes (22): fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed(), _np_complete_weeks_in_month(), _np_perfect_week_index() (+14 more)

### Community 29 - "_enrich_deals"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "chronos_preview.py"
Cohesion: 0.20
Nodes (14): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+6 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.09
Nodes (13): SCRIPT_TIMEOUT = 600s config, hashlib, html, streamlit, _load_secrets_into_env(), _month_end_running(), streamlit_app.py — Denri Marketing Dashboard on Streamlit. Serves the existing…, A Streamlit secret by name — top level, or pasted by mistake under a [table]… (+5 more)

### Community 33 - "odoo_tabs.py"
Cohesion: 0.11
Nodes (28): base_name(), _build(), catalog_rows(), default_window(), dispatch_by_product_shop(), get_rows(), last_complete_week(), load_catalog() (+20 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.15
Nodes (10): _cause(), esc(), fmt(), ladder_strip(), pct(), monthly_report.py…, read_block(), _read_timed_offers() (+2 more)

### Community 35 - "lib/report_month.py"
Cohesion: 0.19
Nodes (17): anchor(), is_pinned(), live_anchor(), live_month_key(), month_key(), month_name(), month_window(), _pinned() (+9 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.26
Nodes (12): active_tills(), daily_by_till(), fine_tune(), history(), main(), project(), quantiles(), chronos_train.py… (+4 more)

### Community 37 - "run_query"
Cohesion: 0.14
Nodes (20): _drop_shared_conn(), Run a read query and return a DataFrame, or None if the DB is unreachable.…, run_query(), lib — shared data-access for the marketing dashboard (Postgres migration).…, _codes_for(), _inlist(), odoo_stock_at_location(), odoo_stock_by_product() (+12 more)

### Community 38 - "build_payload"
Cohesion: 0.12
Nodes (18): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+10 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "ads_panel.js"
Cohesion: 0.22
Nodes (16): act(), axes(), cell(), charts(), drawCmp(), drawWow(), values(), esc() (+8 more)

### Community 41 - "shop_launch.py"
Cohesion: 0.20
Nodes (14): build(), _cfg(), first_sale(), kenya_posts(), load_workplan(), make_matcher(), match(), _parse_workplan() (+6 more)

### Community 42 - "os"
Cohesion: 0.10
Nodes (15): get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, lib/new_products_list.py — which bag types count as this month's NEW PRODUCTS.…, lib/paths.py — where every kind of file lives. Use these instead of building…, openpyxl, openpyxl_comments, openpyxl_styles, openpyxl_utils (+7 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "generators/self_made_combos.py"
Cohesion: 0.16
Nodes (15): _bag_sales_daily_sql(), _bag_sales_sql(), _bags_not_on_offer(), fetch(), fmt(), inject(), main(), self_made_combos.py… (+7 more)

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
Cohesion: 0.27
Nodes (10): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_refresh(), _run_ref() (+2 more)

### Community 52 - "shops_efficiency.py"
Cohesion: 0.05
Nodes (43): build_period(), distributed_in(), main(), q(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only. (+35 more)

### Community 53 - "Bags on offer vs not on offer"
Cohesion: 0.15
Nodes (13): Bags on offer vs not on offer, Corporate-lead till orders, Counted by how it was sold, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Regenerate, Shop birthdays (+5 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.17
Nodes (12): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+4 more)

### Community 56 - "data"
Cohesion: 0.15
Nodes (13): _live_bags(), load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if…, _till_to_shop(), kenya_stock_by_bag(), {BAG_UPPER: category} — the bag's category label only, from the product… (+5 more)

### Community 57 - "build_offer"
Cohesion: 0.17
Nodes (6): build_offer(), _name_sql(), _price_sql(), Compute the full TO payload for a single offer dict. Rebinds the per-offer…, _shop_sql(), _time_sql()

### Community 58 - "bag_classifier"
Cohesion: 0.16
Nodes (16): Buckets, _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), is_on_offer(), _norm() (+8 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "Monthly Report (doc)"
Cohesion: 0.22
Nodes (9): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+1 more)

### Community 61 - "self_made_combos_bundle/self_made_combos.py"
Cohesion: 0.16
Nodes (13): get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, fetch(), fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py… (+5 more)

### Community 62 - "_bg_jobs"
Cohesion: 0.25
Nodes (8): cache_resource, fragment, _bg_done_msg(), _bg_jobs(), _bg_watch(), _fmt_secs(), Background rebuilds shared by every session: label → job (see _bg_rebuild)., The refresh_msg for a finished background rebuild (None: the job vanished).

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "_enrich_deals"
Cohesion: 0.14
Nodes (12): dow_tier_weeks(), _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg(), _tier_window() (+4 more)

### Community 65 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

### Community 66 - "colours.py"
Cohesion: 0.36
Nodes (7): ({BAG: units}, {BAG: {colour: units}}) at CBD/Stock., warehouse_stock(), family(), _load(), _norm(), lib/colours.py — colour FAMILY of a product (Brown, Black, Red, Beige, Grey,…, Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.11
Nodes (18): Bag health (by bag, 18 Oct 2026), Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026), Page, Product rating and core 5 vs other 13 categories (18 Oct 2026) (+10 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "signals"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

### Community 71 - "forward_projections.py"
Cohesion: 0.07
Nodes (32): _bag_revenue(), _bag_revenue_range(), _corporate_lines(), fetch_sheet_data(), fmt_opt_pct(), fmt_pct(), odoo_weekly_breakdown(), _orow() (+24 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "safe_int"
Cohesion: 0.14
Nodes (24): _bag_level_bags(), _build_no_convert(), _fetch_monthly_kenya(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int() (+16 more)

### Community 74 - "queries.py"
Cohesion: 0.16
Nodes (11): main(), month_window(), date, _query_ready(), monthly_sales.py — the current month's real bags sold, from Postgres. The…, First → last calendar day of the LIVE month (today's month; see…, master_products(), _norm_name() (+3 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "push_planner.py"
Cohesion: 0.13
Nodes (22): build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), main(), month_progress() (+14 more)

### Community 77 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.08
Nodes (29): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards) (+21 more)

### Community 78 - "offer_picking.py"
Cohesion: 0.06
Nodes (53): Offer type summary (matrix), _alt_cost(), _apply_alias(), build(), _build_catalog(), _combo_cost(), _combo_slots(), _is_full_price() (+45 more)

### Community 79 - "month_end.py"
Cohesion: 0.36
Nodes (7): clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.…, YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that…, After the closing month's timed offers are safely in Supabase, empty the config…, run(), target_month()

### Community 80 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), lib/theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 81 - "push_laya.py"
Cohesion: 0.13
Nodes (20): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+12 more)

### Community 82 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

### Community 83 - "test_push_planner.py"
Cohesion: 0.17
Nodes (19): Per bag × market: the facts (`push_rules.facts`, `add_peers`), add_peers(), _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m… (+11 more)

### Community 84 - "get_engine"
Cohesion: 0.17
Nodes (13): check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, Run a read query and return a DataFrame, or None if the DB is unreachable.…, Build a SQLAlchemy URL from the environment, or None if unset. Accepts… (+5 more)

### Community 85 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 86 - "num"
Cohesion: 0.20
Nodes (11): _garr_line(), gnum(), num(), _offers(), _parse_offers(), _units(), This month's timed-offer campaigns, flattened for storage. The live TO payload…, Greedy single-line array extractor — handles nested [[...],[...]] arrays. (+3 more)

### Community 87 - "F"
Cohesion: 0.24
Nodes (16): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), A facts row with sensible defaults, overridden by kw., test_fallback_slow_seller_or_overstocked() (+8 more)

### Community 88 - "load_pages"
Cohesion: 0.29
Nodes (7): read_block(), load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, names(), Upper-cased bag types from new_products.txt in file order ([] = no new…, html()

### Community 89 - "datetime"
Cohesion: 0.06
Nodes (54): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+46 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.14
Nodes (10): Agent skills — retail analytics, Test a skill, Use in another project, Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods (+2 more)

### Community 91 - "shop-birthdays.md"
Cohesion: 0.22
Nodes (7): Shop birthdays, Shop → opening date, Where it shows, Per-shop combo-button chips (red when < half best-in-region), self_made_combos.py, Shops & Regions (doc — source of truth), Shop -> Region table

### Community 92 - "run.py"
Cohesion: 0.36
Nodes (9): action_js(), edge_dump(), embedded(), inline_local(), js_str(), main(), Sticky-controls checks (docs/sticky-controls.md › Checks). python…, JS act(d, cb): optionally set a <select> (setv = "SEL=VALUE", fires change),… (+1 more)

### Community 93 - "_combo_button_usage"
Cohesion: 0.15
Nodes (12): _build_sheet_slots(), _combo_button_usage(), _combo_norm_option(), _combo_odoo_slots(), _combo_sheet_slots(), _matches_sheet(), One combo slot-option → its distinctive bag token(s), colours/category words…, Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+4 more)

### Community 94 - "runway_bags.py"
Cohesion: 0.22
Nodes (15): build(), lib/runway_bags.py — RUNWAY BAGS: bag types first created in Odoo in the last…, {TYPE: {"kes", "shops": {SHOP: {"n", "kes"}}}} for the runway types over…, ({TYPE: Kenya shop on-hand}, {TYPE: Sinza + Uganda on-hand}) — live Odoo., The NP.runway payload: {days, bags: [{name, created, category, stockKe,…, Product name → bag type (see the module docstring)., [{name, created, category}] newest first — the runway bag types as of today; []…, {TYPE: bags sold} for the given runway types over [start, end] — POS bags,… (+7 more)

### Community 95 - "negative_fixes.py"
Cohesion: 0.07
Nodes (36): argparse, collections, _negfix(), Stock record accuracy per shop for every period (docs/shops-efficiency.md ›…, bags_sold(), block(), by_shop(), _date() (+28 more)

### Community 96 - "custom_range.py"
Cohesion: 0.19
Nodes (14): block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each…, (from, to) dates for the page's Custom period, or None. Swapped if reversed;… (+6 more)

### Community 97 - "product_targets.py"
Cohesion: 0.09
Nodes (35): calendar, allocate(), available_days(), bag_key_fn(), key(), base_period(), build(), load_targets() (+27 more)

### Community 98 - "shop_regions.py"
Cohesion: 0.29
Nodes (6): _load_shop_regions(), Shop → Region from docs/shop-regions.md (lib/shop_regions); the built-in…, doc(), load(), lib/shop_regions.py — Shop → Region from docs/shop-regions.md (the source of…, {SHOP (upper): region} parsed from the markdown table under the heading that…

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "excluded_products"
Cohesion: 0.23
Nodes (12): _clamp(), month_end_lift(), ({SHOP: {BAG: units a week}}, {SHOP: {"recent", "season", "growth"}}) — recent…, ({SHOP: {BAG: units}}, {SHOP: {BAG: {colour: units}}}) over [start, end]., How much faster the shops sell in the rest of the month than before it, from…, realistic_rates(), growth(), season() (+4 more)

### Community 101 - "current_performance.html"
Cohesion: 0.50
Nodes (4): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance)

### Community 102 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 103 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.29
Nodes (7): lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, lib/report_month.py (which month are we reporting?), self_made_combos.html static page (reads const SMC), self_made_combos.py generator (build_payload + SQL + injection)

### Community 104 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.13
Nodes (14): _as_day(), _local_deal_rows(), _in_month(), 2026-10-25' / date / None → date or None., Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), Blocker counter (+6 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "reject_variants"
Cohesion: 0.33
Nodes (7): _parse_colour(), First primary colour token found in a name (longest-first), Title-cased; '' if…, Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share…, Per-[REJECT]-product variant rows for a name-filtered offer, for the filterable…, reject_variants(), _match_bag(), _singular_tokens()

### Community 107 - "posting_yields.py"
Cohesion: 0.12
Nodes (16): count_complete_weeks_in_month(), _fold_bag_level(), load_dead_thresholds(), _mkt_perfect_week_index(), _mkt_week_label(), _offer_bagtypes_by_region(), posting_yields.py…, Bags whose posts marketing logs only per BAG (the posting sheet's TOTAL row,… (+8 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "_base_colour"
Cohesion: 0.33
Nodes (6): _base_colour(), _merge_rows_by_base_colour(), Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across…, _strip_colour_qualifiers()

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "odoo_month_product_bags"
Cohesion: 0.33
Nodes (6): odoo_combo_product_bags(), odoo_lifetime_product_bags(), odoo_month_product_bags(), All-time bags per product from Odoo (no month window) — the lifetime sales of…, [(product name, bags)] for bags sold INSIDE combos (sub_product_line) in the…, Reporting month's bags per product from Odoo (Postgres), or None if the DB…

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 114 - "generator"
Cohesion: 0.33
Nodes (6): generator(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, start_daily_snapshot(), run_scripts()

### Community 121 - "bag_quant.py"
Cohesion: 0.09
Nodes (30): build(), _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), action(), bag_posts() (+22 more)

### Community 122 - "bags_on_offer.py"
Cohesion: 0.06
Nodes (49): _archived_source(), _as_date(), _bag_tiers(), _base_windows(), _build_period(), _custom_range(), fetch(), cat_tier() (+41 more)

### Community 123 - "What the page shows"
Cohesion: 0.18
Nodes (11): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 2b. Shop breakdown (22 Oct 2026, user's call), 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Bulk orders, Data (+3 more)

### Community 126 - "Product (bag) targets"
Cohesion: 0.25
Nodes (8): A month with only a revenue target (November 2026), Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 128 - "_bg_rebuild"
Cohesion: 0.40
Nodes (6): _bg_rebuild(), work(), Seconds the last good `kind` rebuild of `lbl` took (any kind as a fallback),…, Rebuild `lbl` in the background. kind: "auto" (skipped if a rebuild was tried…, _rebuild_secs(), _save_rebuild_secs()

### Community 130 - "pos_lines.py"
Cohesion: 0.50
Nodes (3): expand(), lib/pos_lines.py — till lines with refunded combos fixed (docs/README.md ›…, Replace each POS_LINES(alias) with the fixed-lines subquery for that pos_order…

### Community 131 - "product_performance.py"
Cohesion: 0.07
Nodes (40): build(), corp(), categories(), corporate_period(), _d(), explain(), _fmt_d(), _load_json() (+32 more)

### Community 132 - "_reveal_page"
Cohesion: 0.50
Nodes (4): Run script-only HTML in an invisible frame (same origin, so it can reach…, Fade the page area back in on a page that has no dashboard frame (password…, _reveal_page(), _run_js()

### Community 138 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.22
Nodes (7): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does, Current Performance (doc)

### Community 145 - "Shop Launch"
Cohesion: 0.29
Nodes (6): Config, Launch day, Marketing posts, Sales, Shop Launch, What the page shows

### Community 153 - "New Products Analytics (doc)"
Cohesion: 0.16
Nodes (14): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix) (+6 more)

### Community 154 - "ads.py"
Cohesion: 0.11
Nodes (19): csv, Actions ("what we can do"), Ads impact — on every page (21 Oct 2026, user's call), Charts (21 Oct 2026, user's call), Figures, Refresh, chart_data(), ser() (+11 more)

### Community 155 - "Offer Picking (doc)"
Cohesion: 0.29
Nodes (8): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES)

### Community 156 - "weekly_sales.py"
Cohesion: 0.28
Nodes (7): fetch_monthly_target(), main(), date, _query_ready(), weekly_sales.py — the weekly-sales fix. Computes the CURRENT Sun–Sat week's…, The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's…, week_window()

### Community 157 - "_month_archived"
Cohesion: 0.67
Nodes (3): cache_data, _month_archived(), True when `key` is in Supabase (falls back to monthly_report_history.json). If…

### Community 158 - "footfall.py"
Cohesion: 0.27
Nodes (11): daily(), DataFrame, date, lib/footfall.py — footfall (visitors counted per shop per day) joined to walk-…, The Sunday that starts d's Sun–Sat week., One row per footfall shop per day: visitors (NaN = not counted), walk-in orders…, One row per shop per Sun–Sat week. Conversion and revenue use COUNTED days…, Paid-ad WhatsApp leads per WhatsApp shop per Sun–Sat week: chats, bought,… (+3 more)

### Community 159 - "scripts/receipt_combos.py"
Cohesion: 0.29
Nodes (6): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…, itertools

### Community 160 - "_fetch_sinza_monthly"
Cohesion: 0.18
Nodes (14): _analyze_region(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), MONTHLY_SALES: colour=A(0), product_name=B(1), MONTHLY_MARKETING_POST: colour=A(0), product_name=C(2), STOCK_LEVELS: colour=A(0), product_name=C(2) (+6 more)

### Community 162 - "generate_insights.py"
Cohesion: 0.24
Nodes (5): card(), esc(), fmt(), generate_insights.py…, region_card()

### Community 165 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 167 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 168 - "lib/db.py"
Cohesion: 0.15
Nodes (17): dotenv, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, functools, _cache_path(), _env(), get_engine(), Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME… (+9 more)

### Community 169 - "Footfall and Marketing (21 Oct 2026, user's call)"
Cohesion: 0.20
Nodes (9): Actions (rules), Correlations ("Posts and ads vs visitors"), Data traps (said on the page), Definitions, Footfall and Marketing (21 Oct 2026, user's call), Regenerate, Shop mapping (`lib/footfall.SHOPS`), Sources (+1 more)

### Community 170 - "timed_offers.py (generator)"
Cohesion: 0.09
Nodes (22): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+14 more)

### Community 172 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 173 - "re"
Cohesion: 0.28
Nodes (6): One-off: restore August's Offer Type figures into monthly_report_history.json…, re, Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 174 - "Product Performance — Shop breakdown: progress"
Cohesion: 0.22
Nodes (8): 1. Spec — DONE, 2. Data — DONE, 3. Page section — DONE, 4. Sidebar and sticky bar — DONE, 5. Visual check — DONE, 6. Wrap-up — DONE, Product Performance — Shop breakdown: progress, Summary

### Community 175 - "_bag_stock"
Cohesion: 0.40
Nodes (5): _bag_stock(), _combo_bags(), _norm_bag(), Space/punctuation-insensitive key so 'MINIZURI' matches 'MINI ZURI'., Component bags of an offer, each with its stock, sorted most-stock first.

### Community 177 - "norm"
Cohesion: 0.13
Nodes (18): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, ({PRODUCT: {SHOP CODE: units}}, {PRODUCT: {SHOP CODE: [[colour, units], …]}})…, shop_sales(), _aliases(), build_rows(), _Deriver, _flag_cells() (+10 more)

### Community 179 - "Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)"
Cohesion: 0.20
Nodes (9): 1. Spec — DONE, 2. SQL + library — DONE, 3. Generator — DONE, 4. Page — DONE, 5. Actions — DONE, 6. Visual check — DONE, 7. Wrap-up — DONE, Findings (16 weeks, 28 Jun – 17 Oct 2026; last fully counted week 11–17 Oct) (+1 more)

### Community 180 - "check_connection"
Cohesion: 0.10
Nodes (29): _corporate_bags(), The month's revenue target (KES): Odoo sales_pos_target amount (pos +…, (corporate bags, corporate KES received) in the given month, live from Odoo…, _revenue_target(), _bucket(), _kenya_net_moves_since(), odoo_bag_daily_value(), odoo_bag_prices() (+21 more)

### Community 181 - "sendable_by_month_end"
Cohesion: 0.50
Nodes (4): {shop: units} — `left` units shared over {shop: gap} in proportion, leftovers…, What can still be sent (docs › Shop requests — realistic performance): per shop…, sendable_by_month_end(), _share_out()

### Community 183 - "history.py"
Cohesion: 0.31
Nodes (10): fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers…, Like _num, but leaves booleans alone and renders dates as ISO strings — the… (+2 more)

### Community 184 - "build"
Cohesion: 0.18
Nodes (24): build(), acts(), campaign_table(), money(), cpr(), focus_tiles(), market_table(), overview_tiles() (+16 more)

### Community 185 - "json"
Cohesion: 0.21
Nodes (11): main(), push_to_supabase.py — run the marketing migration against Supabase. Regenerates…, json, main(), month_block(), num(), q(), supabase_migration.py — export the marketing dashboard's monthly data to a SQL… (+3 more)

### Community 186 - "fetch_posting_data"
Cohesion: 0.15
Nodes (11): _bt_on_offer(), _dead_clear(), fetch_posting_data(), _clear(), _yield(), _post_yield(), Marketing & Sales Alignment — posting yield, measured the way marketing…, {catalogue name: net units moved INTO the region's shops on/after `since`} from… (+3 more)

### Community 187 - "Ralph loop brief — Footfall and Marketing page"
Cohesion: 0.25
Nodes (7): DATA FACTS (verified 21 Oct 2026), DONE, ESCAPE HATCH, PROJECT RULES (must hold every iteration), Ralph loop brief — Footfall and Marketing page, SELF-CORRECTION, SUB-GOALS (do in order; tick each in notes/footfall_progress.md with the command output that proved it)

### Community 190 - "sys"
Cohesion: 0.25
Nodes (7): main(), node_check(), Run the sticky-controls checks on every wired page and print the markdown…, build_all.py ────────────────────────────────────────────────────────────────…, subprocess, sys, tempfile

### Community 191 - "build"
Cohesion: 0.18
Nodes (11): actions(), build(), agg(), week_tot(), num(), pearson(), footfall_marketing.py — Footfall and Marketing page (spec: docs/footfall-…, What we can do' — by rule (docs/footfall-marketing.md › Actions). Each names a… (+3 more)

### Community 193 - "main.py"
Cohesion: 0.13
Nodes (18): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, Denri Africa — Marketing Dashboard Launcher… (+10 more)

### Community 194 - "_apply_receipt_offers"
Cohesion: 0.25
Nodes (6): _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region…, _region_goal(), _till_targets()

### Community 195 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 197 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 202 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 205 - "Sales-share targets per product"
Cohesion: 0.40
Nodes (4): Deliver, Sales-share targets per product, Steps, Tests

## Knowledge Gaps
- **251 isolated node(s):** `Log`, `Blocker counter`, `Final summary`, `Log`, `Sheets cut to three tabs (RALPH_SHEETS.md) — 2026-10-04` (+246 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1083 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `bag_classifier()` connect `bag_classifier` to `_apply_receipt_offers`, `push_planner.py`, `generators/self_made_combos.py`, `oos_callbacks.py`, `Push Planner (`push_planner.py` → `push_planner.html`, `PP`)`, `Bags on offer vs not on offer`, `data`, `Product (bag) targets`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `Bags on offer vs not on offer` connect `Bags on offer vs not on offer` to `self_made_combos_bundle/lib/__init__.py`, `offer_picking.py`, `oos_callbacks.py`, `bag_classifier`, `shop-birthdays.md`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `run_query()` connect `run_query` to `shop_corporate.py`, `pos_lines.py`, `product_performance.py`, `self_made_combos_bundle/lib/__init__.py`, `current_performance.py`, `build_payload`, `_combo_button_usage`, `shop_stock_levels.py`, `snapshot.py`, `shop_requests.py`, `new_products.py`, `_enrich_deals`, `chronos_preview.py`, `weekly_sales.py`, `footfall.py`, `posts_lead_sales`, `chronos_train.py`, `build_payload`, `_bags_not_on_offer`, `lib/db.py`, `shop_launch.py`, `generators/self_made_combos.py`, `norm`, `check_connection`, `shops_efficiency.py`, `build`, `fetch_posting_data`, `_enrich_deals`, `_apply_receipt_offers`, `forward_projections.py`, `queries.py`, `offer_picking.py`, `_combo_button_usage`, `runway_bags.py`, `negative_fixes.py`, `product_targets.py`, `excluded_products`, `odoo_month_product_bags`, `bag_quant.py`, `bags_on_offer.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **What connects `Log`, `Blocker counter`, `Final summary` to the rest of the system?**
  _251 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `laya.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._
- **Should `self_made_combos_bundle/lib/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08078431372549019 - nodes in this community are weakly interconnected._
- **Should `oos_chip.js` be split into smaller, more focused modules?**
  _Cohesion score 0.08067375886524823 - nodes in this community are weakly interconnected._