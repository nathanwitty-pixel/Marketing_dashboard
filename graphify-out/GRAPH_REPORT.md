# Graph Report - Marketing_dashboard  (2026-11-22)

## Corpus Check
- 252 files · ~1,266,204 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 22 file(s) not represented in the graph (top: .csv 15, (none) 2, .toml 1)

## Summary
- 3013 nodes · 6072 edges · 226 communities (184 shown, 42 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 197 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c489f4cb`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- shop_corporate.py
- laya.py
- tests/test_receipt_combos.py
- oos_chip.js
- chart_switcher.js
- he
- Kitengela Rejects tracker (timed offer)
- signals
- Denri Africa Dashboard Design System (skill)
- v5_theme.js
- name_match.py
- bare_minimum setting (weekly target floor)
- offer_data.py
- _fetch_monthly_kenya
- run_query
- tab_rows
- json
- le
- Ps
- os
- sticky_controls.js
- .week
- generator
- Self-made combos vs running combos (doc)
- ls
- vs
- anime.umd.min.js
- Dashboard Menu Docs (spec index)
- check_connection
- si
- live_month_window
- push_rules.py
- streamlit_app.py
- stock.py
- monthly_report.py
- live_anchor
- chronos_train.py
- attach_stock
- build_payload
- Shops Efficiency Tracking spec doc
- offer_picking.py
- shop_requests.py
- shop_launch.py
- page_sidebar.js
- weekly_report.py
- Combos & Power Deals by Shop panel (#combo-shop)
- test_fixC_sql.py
- lib/db.py (Supabase session pooler DB access)
- CLAUDE.md
- history.py (read months back)
- je
- bag_classifier
- odoo_tabs.py
- estimated_targets.py
- algorithmic-art skill
- dataviz-charts skill
- scripts/test_receipt_combos.py
- weekly_products.py
- fetch_months
- High-End Visual Design skill
- _is_checked
- publish.py
- fetch_new_products_data
- daydream skill (Vault Daydream)
- posting_yields.py
- oos_callbacks.py
- lib/weekly_sales.py
- datetime
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- test_oos_callbacks.py
- _enrich_deals
- marketing_dashboard.sql
- fetch_posting_data
- build
- shop_birthdays.py
- kpi_anim.js
- build
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- why_moved.js
- theme.py
- push_laya.py
- build
- test_push_planner.py
- fetch
- actions_ui.py
- weekly_combos.py
- F
- ads.py
- test_stockout_demand.py
- README.md
- push_planner.py
- main
- ns
- Dashboard Architecture (static HTML + Python generator + injected data block)
- negative_fixes.py
- custom_range.py
- lib
- signals
- Bag Signals — quant view of each bag (posting · stock · selling)
- beats.py
- current_performance.html
- attach
- Fix merge conflicts (two-machine workflow)
- snapshot.py
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- build
- live_month_key
- Ralph task — only three sheet tabs left
- Product Performance slides (23 Nov 2026, user's call)
- Bag targets October 2026_3acbad00.md
- offer_kenya_posts
- actions.py
- perf_data.js
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- _load
- excluded_products
- daily
- fetch
- What the page shows
- Product (bag) targets
- sales
- load_lines
- _q
- test_share_targets.py
- build
- start_server
- odoo_weekly_breakdown
- summary
- bag_key_fn
- contextlib
- Chart type switcher (every chart, every menu)
- denri_mkt_timed_offer* Supabase tables
- timed_offers.py (generator)
- New Products Analytics (doc)
- Shop Launch
- Offer Picking (doc)
- weekly_newproducts.py
- build
- google_auth.py (shared auth module)
- scripts/receipt_combos.py
- _dead_stock_region
- design-taste-frontend (anti-slop frontend skill)
- write_atomic
- get_engine
- Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)
- _build_period
- Bags on offer vs not on offer
- Menu 1 Current Performance in the 3-beat layout (preview)
- update_np_weekly_history
- Footfall and Marketing (21 Oct 2026, user's call)
- Offers
- Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)
- realistic_rates
- follower_test.py
- Product Performance — Shop breakdown: progress
- Ralph task — "Out of stock — call back" demand per shop
- _matches_sheet
- timed_offers.py
- Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)
- main.py
- Weekly Report
- html
- family
- base_name
- _reveal_page
- Out-of-stock demand — people, not requests
- Ralph loop brief — Footfall and Marketing page
- last_week_from_db
- data
- Bag signals — quant finance applied to product sales
- ambiguous_python_import_17686b6faac5
- _alignment_region
- Bag Tracking
- _combo_button_usage
- _build_catalog
- compute_period
- shop_stock_levels.py
- shops_dispatch.py
- Combos from receipts — running vs self-made
- render
- followup
- test_sheet_reads.py
- Slide 2: Did new followers sell bags? (Kenya)
- norm
- main
- shop-birthdays.md
- reject_variants
- Odoo marketing data audit
- ODOO_MARKETING_AUDIT.md
- shop_breakdown
- price
- requests_block
- _bag_tiers
- test_no_google.py
- bag_gender.py
- safe_int
- _analyze_region
- load_posts
- sendable_by_month_end

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 87 edges
2. `fetch()` - 41 edges
3. `data()` - 40 edges
4. `fetch_posting_data()` - 39 edges
5. `check_connection()` - 32 edges
6. `le` - 31 edges
7. `build_payload()` - 30 edges
8. `get_gspread_client()` - 27 edges
9. `excluded_products()` - 27 edges
10. `ls` - 26 edges

## Surprising Connections (you probably didn't know these)
- `What the page shows (per period)` --references--> `_market_records()`  [INFERRED]
  docs/bags-on-offer.md → generators/bags_on_offer.py
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
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]

## Communities (226 total, 42 thin omitted)

### Community 0 - "shop_corporate.py"
Cohesion: 0.15
Nodes (25): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), _acronym(), build(), _maybe(), owns(), corporate_team_receipts(), _d() (+17 more)

### Community 1 - "laya.py"
Cohesion: 0.09
Nodes (26): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket() (+18 more)

### Community 2 - "tests/test_receipt_combos.py"
Cohesion: 0.05
Nodes (65): _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, _fill_units(), _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region…, _region_goal() (+57 more)

### Community 3 - "oos_chip.js"
Cohesion: 0.08
Nodes (38): attach(), close(), esc(), form(), go(), iso(), mountPanel(), open() (+30 more)

### Community 4 - "chart_switcher.js"
Cohesion: 0.12
Nodes (35): alpha(), apply(), attach(), axisOpts(), build(), changeTxt(), Chart(), clone() (+27 more)

### Community 5 - "he"
Cohesion: 0.09
Nodes (4): cs, er, get(), he()

### Community 6 - "Kitengela Rejects tracker (timed offer)"
Cohesion: 0.07
Nodes (28): bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source), Offline fallback pattern (mirror sheet data to local JSON), Reject Sale (doc: reject_sales.py -> reject_sales.html, RJ), reject_sales_export.csv (fallback export) (+20 more)

### Community 7 - "signals"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

### Community 8 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.18
Nodes (12): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), Signature Element — Flowing Border (achievement cards), high-end-visual-design (related skill), KPI Tile component (+4 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 12 - "offer_data.py"
Cohesion: 0.20
Nodes (12): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), offer_data.py ─────────────────────────────────────────────────────────────────… (+4 more)

### Community 13 - "_fetch_monthly_kenya"
Cohesion: 0.23
Nodes (12): _fetch_monthly_kenya(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), Monthly Kenya figures for the S1 KPI cards. MONTHLY_MARKETING_POST: sum col E…, MONTHLY_SALES: colour=A(0), product_name=B(1), MONTHLY_MARKETING_POST: colour=A(0), product_name=C(2) (+4 more)

### Community 14 - "run_query"
Cohesion: 0.08
Nodes (27): _corporate_bags(), _corporate_lines(), The month's revenue target (KES): Odoo sales_pos_target amount (pos +…, (corporate bags, corporate KES received) in the given month, live from Odoo…, The corporate app bags behind _corporate_bags(), one row per product with its…, _revenue_target(), odoo_combo_product_bags(), odoo_lifetime_product_bags() (+19 more)

### Community 15 - "tab_rows"
Cohesion: 0.29
Nodes (10): _bag_category(), _category(), _date(), posts(), {(BAG TYPE, COLOUR): {market: posts}} over [start, end]., The old WEEKLY_ / MONTHLY_MARKETING_POST tab — same header and columns A–H —…, The posting tab's rows: from marketing's daily sheets (tab_rows); if they can't…, read() (+2 more)

### Community 16 - "json"
Cohesion: 0.11
Nodes (10): One-off: restore August's Offer Type figures into monthly_report_history.json…, fetch_monthly_target(), current_performance.py…, main(), date, _query_ready(), weekly_sales.py — the weekly-sales fix. Computes the CURRENT Sun–Sat week's…, The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's… (+2 more)

### Community 17 - "le"
Cohesion: 0.09
Nodes (3): Ht, le, Ut

### Community 19 - "os"
Cohesion: 0.05
Nodes (44): dotenv, generators/bag_tracking.py — Bag Tracking: the chosen bags' Kenya shop stock at…, history.py — build the dashboard History page from Supabase. Reads the…, monthly_sales.py — the current month's real bags sold, from Postgres. The…, main(), push_to_supabase.py — run the marketing migration against Supabase. Regenerates…, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, Shared Google Sheets authentication for every dashboard generator. Two modes,… (+36 more)

### Community 20 - "sticky_controls.js"
Cohesion: 0.20
Nodes (15): bind(), embedHost(), headerOf(), init(), initSections(), injectCss(), place(), setPinned() (+7 more)

### Community 21 - ".week"
Cohesion: 0.33
Nodes (6): _month_end(), _month_start(), periods(), {period: (cur start, cur end, prev start, prev end, label)} — each compared…, {power, combo:[labels], dow:[{tier, shops}], timed:[{name, s, e, was, now}]}…, _sunday()

### Community 22 - "generator"
Cohesion: 0.25
Nodes (8): generator(), _buyer_lines(), _load_lines(), [{d, mkt, bag, units, g}] — the Product Performance sales lines with the…, _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, start_daily_snapshot()

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.14
Nodes (18): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+10 more)

### Community 26 - "anime.umd.min.js"
Cohesion: 0.15
Nodes (8): ce(), de(), Me, Oe(), rs, St(), ts(), Ye

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.13
Nodes (17): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, google_auth.py (Sheets auth), Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics (+9 more)

### Community 28 - "check_connection"
Cohesion: 0.11
Nodes (20): build_offer(), odoo_bag_daily_value(), odoo_bag_prices(), odoo_bulk_lines(), odoo_daily_kenya(), odoo_list_price(), odoo_offer_price(), odoo_window_sales() (+12 more)

### Community 29 - "si"
Cohesion: 0.24
Nodes (3): ii(), ri, si

### Community 30 - "live_month_window"
Cohesion: 0.25
Nodes (9): Period selector (Monthly / Weekly / Last week / Custom), corporate_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, load_targets(), {BAG: target units} for the month from product_targets_<YYYY-MM>.csv (built…, write_csv(), live_month_window(), (first day, last day) of the LIVE month (today's month, unless pinned). (+1 more)

### Community 31 - "push_rules.py"
Cohesion: 0.13
Nodes (17): action(), _cover_txt(), _days_back(), _kind(), _n(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).…, (code, plain sentence, units at stake, confidence 0..1) for one bag × market.…, HANDBAG' → 'handbags', 'SCHOOL BAG' → 'school bags', 'SPORT' → 'sport bags', ''… (+9 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.08
Nodes (26): cache_resource, SCRIPT_TIMEOUT = 600s config, fragment, hashlib, html, _bg_done_msg(), _bg_jobs(), _bg_rebuild() (+18 more)

### Community 33 - "stock.py"
Cohesion: 0.13
Nodes (22): odoo_stock_kenya_outside(), ({UPPER name: kenya on-hand}, {UPPER name: outside on-hand}) — live Odoo stock.…, load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if…, _till_to_shop(), odoo_stock_levels() (+14 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.06
Nodes (38): _bag_stock(), _cause(), _collect_comments(), _combo_bags(), esc(), fmt(), _garr_line(), gnum() (+30 more)

### Community 35 - "live_anchor"
Cohesion: 0.13
Nodes (20): corporate_target_from_db(), This month's Odoo corporate target {bags, kes} (sales_pos_target, scope…, count_complete_weeks_in_month(), count_complete_weeks_in_month(), Count Mon–Sun weeks in the reporting month that have ≥5 days falling within it., anchor(), live_anchor(), month_key() (+12 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.12
Nodes (29): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+21 more)

### Community 37 - "attach_stock"
Cohesion: 0.19
Nodes (13): col(), attach_stock(), in_stock(), stk(), collect(), _in(), is_combo_request(), {period: (start, end)} for the dated periods (lifetime / current are undated).… (+5 more)

### Community 38 - "build_payload"
Cohesion: 0.11
Nodes (20): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+12 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.20
Nodes (10): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.html page (+2 more)

### Community 40 - "offer_picking.py"
Cohesion: 0.10
Nodes (33): _alt_cost(), _apply_alias(), build(), _combo_cost(), _combo_slots(), _monthly_bag_sales(), _next_month(), bag() (+25 more)

### Community 41 - "shop_requests.py"
Cohesion: 0.18
Nodes (17): _onoff(), _d(), _f(), _match(), _offer_label(), _pct(), production(), lib/shop_requests.py — what each shop REQUESTED in the Odoo dispatch module… (+9 more)

### Community 42 - "shop_launch.py"
Cohesion: 0.12
Nodes (26): build(), _add(), launch_curve(), _cfg(), _day_expr(), first_sale(), kenya_posts(), load_categories() (+18 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "weekly_report.py"
Cohesion: 0.10
Nodes (16): field(), fmt(), _ft_band(), kes_m(), other(), proj_field(), weekly_report.py — the weekly marketing report as slides (Headline / Graph /…, {label: [chats, bought]} for one market's shops (KE = all but Sinza and Uganda)… (+8 more)

### Community 45 - "Combos & Power Deals by Shop panel (#combo-shop)"
Cohesion: 0.29
Nodes (7): Combos & Power Deals by Shop panel (#combo-shop), compute_period() function (emits pushDetail per period), Deal of the Week — Tier 2 (latest 2-week window) shop-scoped view, DenriTableFilter reusable filter bar component, DOW_MIRROR expansion (Starmall to Hazina/Hilton/KTDA), odoo_stock_levels() function, Push via filter (None / power deal / deal of the week tag)

### Community 46 - "test_fixC_sql.py"
Cohesion: 0.29
Nodes (12): pytest, _bind(), _corp_db(), _dist_db(), Fix batch C (Nov 2026): SQL rules run on fake rows in DuckDB (no Odoo needed)…, _read(), test_combined_distribution_keeps_identical_moves_but_collapses_two_sources(), test_corporate_bags_instalments_add_up_to_whole_invoice() (+4 more)

### Community 47 - "lib/db.py (Supabase session pooler DB access)"
Cohesion: 0.40
Nodes (5): lib/db.py (Supabase session pooler DB access), lib/db.run_query (shared connection reuse per subprocess), offer_data.build (batched Sheets range fetch), Refresh Performance (shared connection reuse, batched Sheets reads), Supabase session pooler host rule (direct host is IPv6-only)

### Community 49 - "history.py (read months back)"
Cohesion: 0.33
Nodes (7): denri_mkt_* Supabase tables, history.html page, history.py (read months back), month_end.py (freezes a month), push_to_supabase.py (write months), Resilience fallback: history.py leaves existing page data untouched if Supabase unreachable, supabase_migration.py (schema)

### Community 51 - "bag_classifier"
Cohesion: 0.17
Nodes (15): Buckets, _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _norm_combo() (+7 more)

### Community 52 - "odoo_tabs.py"
Cohesion: 0.12
Nodes (24): load(), _build(), build_rows(), catalog_rows(), default_window(), _flag_cells(), _fmt(), get_rows() (+16 more)

### Community 53 - "estimated_targets.py"
Cohesion: 0.17
Nodes (14): allocate(), available_days(), Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, _add_months(), _d(), main(), scripts/estimated_targets.py — what the monthly bag target WOULD have been, by… (+6 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.29
Nodes (7): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.)

### Community 56 - "scripts/test_receipt_combos.py"
Cohesion: 0.32
Nodes (15): classify(), lines: [{receipt, d, product, qty, amount}] → per-market summary: {running:…, infer(), L(), Tests for receipt_combos.py + name_match.py — python -m pytest scripts -q, test_alternatives_and_singles(), test_bulk_receipts_are_not_combos(), test_four_bags_at_two_prices_are_two_combos() (+7 more)

### Community 57 - "weekly_products.py"
Cohesion: 0.17
Nodes (19): _buyer_slide(), _d(), _fmt(), _gender_split(), _market_slides(), _pct(), _pp_page(), date (+11 more)

### Community 58 - "fetch_months"
Cohesion: 0.28
Nodes (9): fetch_months(), bucket(), inject(), main(), _num(), psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers…, Like _num, but leaves booleans alone and renders dates as ISO strings — the…, _rows() (+1 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "_is_checked"
Cohesion: 0.18
Nodes (17): _build_no_convert(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int(), _is_checked(), _is_x() (+9 more)

### Community 61 - "publish.py"
Cohesion: 0.09
Nodes (32): fnmatch, action_js(), main(), node_check(), Run the sticky-controls checks on every wired page and print the markdown…, edge_dump(), embedded(), inline_local() (+24 more)

### Community 62 - "fetch_new_products_data"
Cohesion: 0.24
Nodes (12): fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_sales_window() (+4 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "posting_yields.py"
Cohesion: 0.12
Nodes (15): _mkt_perfect_week_index(), _mkt_week_label(), posting_yields.py…, Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]., current = {region: {key: {productName,colour,category,bagType,stock}}}. A new…, update_clearance(), update_mkt_history() (+7 more)

### Community 65 - "oos_callbacks.py"
Cohesion: 0.16
Nodes (17): _date(), load_rows(), _online_rows(), oos_by_bag_shop(), lib/oos_callbacks.py — "Out of stock — call back" demand, ONLINE and WALK-IN.…, {shop: set(person)} → (distinct people, [[shop, people], …] high → low)., {period: {key: people}} from an aggregate() block., {period: {product name: {shop: people}}} straight from Odoo names, or {} if… (+9 more)

### Community 66 - "lib/weekly_sales.py"
Cohesion: 0.25
Nodes (14): _corporate(), _fmt(), _kes(), _n(), _Page, _pct(), _price(), date (+6 more)

### Community 67 - "datetime"
Cohesion: 0.06
Nodes (42): calendar, datetime, _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., footfall_marketing.py — Footfall and Marketing page (spec: docs/footfall-…, fetch_sheet_data(), fmt_opt_pct() (+34 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "test_oos_callbacks.py"
Cohesion: 0.20
Nodes (18): aggregate(), flat(), split(), The page block: {period: {key: {"total": people, "shops": [[shop, people],…, _base_sql(), _kai(), Tests for lib/oos_callbacks.py (WhatsApp "Out of stock — call back" demand).…, test_attach_stock_per_shop_and_colour() (+10 more)

### Community 71 - "_enrich_deals"
Cohesion: 0.06
Nodes (29): _as_day(), dow_tier_weeks(), _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg() (+21 more)

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
Cohesion: 0.10
Nodes (30): _kenya_target(), month_progress(), payload(), Kenya's month target from current_performance.html (PERF.totalTarget), or None., Per market: sold this month so far (from the daily sales), days elapsed / left,…, _slim(), by_shop(), _entry() (+22 more)

### Community 76 - "kpi_anim.js"
Cohesion: 0.60
Nodes (5): count(), fmt(), key(), parse(), scan()

### Community 77 - "build"
Cohesion: 0.33
Nodes (6): base_period(), build(), (total units, info) — the month's Odoo target units, or (no Odoo targets yet)…, The three complete months before month_start → (start, end)., (rows, total, base start, base end) for the month, from Odoo., total_for()

### Community 78 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.15
Nodes (12): Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Page, Production — shop requests vs approved list (18 Oct 2026), Requests by category (18 Oct 2026), Shop requests and Production — Region / Shop filter and tiles (19 Oct 2026), Shop requests — realistic performance (26 Oct 2026, user's call) (+4 more)

### Community 79 - "why_moved.js"
Cohesion: 0.36
Nodes (12): bestWeek(), bestWeeks(), build(), fillWeeks(), getW(), hasKey(), mark(), onClick() (+4 more)

### Community 80 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), lib/theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 81 - "push_laya.py"
Cohesion: 0.13
Nodes (20): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+12 more)

### Community 82 - "build"
Cohesion: 0.15
Nodes (15): Bulk orders, build(), categories(), explain(), _fmt_d(), _load_json(), offer_days(), {BAG: category} — the bag type's usual catalogue category, else its Odoo… (+7 more)

### Community 83 - "test_push_planner.py"
Cohesion: 0.17
Nodes (19): build_facts(), Facts for every bag × market that has stock or sold in the window…, add_peers(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m… (+11 more)

### Community 84 - "fetch"
Cohesion: 0.11
Nodes (18): Counted by how it was sold, Regenerate, _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…, _bags_not_on_offer(), fetch() (+10 more)

### Community 85 - "actions_ui.py"
Cohesion: 0.21
Nodes (15): _field(), _month_key(), _open_quotes(), _plain(), lib/actions_ui.py — the "Act on this page" panel shown above Current…, Draw the panel. `rebuild()` rebuilds the page in the background (after a…, A one-line JSON value from the page's PERF / PROJ blocks (` name: <json>,`)., Quotes this month not invoiced yet (and not declined / cancelled). (+7 more)

### Community 86 - "weekly_combos.py"
Cohesion: 0.26
Nodes (14): _d(), _fmt(), _gen(), _market_slide(), _offer_mix(), _pct(), date, lib/weekly_combos.py — the Weekly Report's combos and offers slides: one per… (+6 more)

### Community 87 - "F"
Cohesion: 0.17
Nodes (21): build_reasons(), Adds notMoving + reasons to every row (lib/push_rules.reasons). Returns the…, context(), not_moving(), A bag with stock that isn't clearing: cleared < 30% this month, or > 45 days of…, What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons() (+13 more)

### Community 88 - "ads.py"
Cohesion: 0.23
Nodes (11): campaigns(), _f(), market_week(), notes(), date, lib/ads.py — marketing's Weekly Ads Performance Report, as data (spec:…, Every campaign-week row, with spend_kes added (USD × USD_KES)., The report's Sun–Sat weeks (week starts), oldest first. (+3 more)

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "README.md"
Cohesion: 0.17
Nodes (7): Agent skills — retail analytics, Test a skill, Use in another project, Deliver, Sales-share targets per product, Steps, Tests

### Community 91 - "push_planner.py"
Cohesion: 0.13
Nodes (25): push_planner.py — Push Planner: what to push this week, where, and why bags…, _bags_on_offer(), _block(), build_extras(), cp_more_month(), _deals(), _month_dates(), _pick() (+17 more)

### Community 92 - "main"
Cohesion: 0.12
Nodes (19): Actions (one per bag × market, then ranked), build_actions(), inject(), main(), Adds action / says / units / confidence / score to each facts row; returns…, moves(), posting_median(), rank() (+11 more)

### Community 94 - "Dashboard Architecture (static HTML + Python generator + injected data block)"
Cohesion: 0.40
Nodes (5): DATA_START/DATA_END comment marker injection pattern, build_all.py (rebakes every page), Dashboard Architecture (static HTML + Python generator + injected data block), .github/workflows/refresh.yml CI workflow, shell.html (sidebar nav frame, loads each page into an iframe)

### Community 95 - "negative_fixes.py"
Cohesion: 0.08
Nodes (34): argparse, _negfix(), Stock record accuracy per shop for every period (docs/shops-efficiency.md ›…, bags_sold(), block(), by_shop(), _date(), _int() (+26 more)

### Community 96 - "custom_range.py"
Cohesion: 0.19
Nodes (14): block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each…, (from, to) dates for the page's Custom period, or None. Swapped if reversed;… (+6 more)

### Community 97 - "lib"
Cohesion: 0.08
Nodes (34): collections, csv, Per-shop combo-button chips (red when < half best-in-region), Shop -> Region table, _base_windows(), _custom_range(), fmt(), inject() (+26 more)

### Community 98 - "signals"
Cohesion: 0.17
Nodes (16): action(), _mean(), _phi(), posting_beta(), The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json…, _sd() (+8 more)

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "beats.py"
Cohesion: 0.29
Nodes (10): _n(), projections(), Three beats for each Current Performance card (docs/current-performance.md ›…, Forward Projections cards: bags and revenue together, and what the gap between…, The strip at the top of the page: where the month will land and what it takes…, Weekly Performance card: the last complete week against the one before (per…, summary(), _tone_for() (+2 more)

### Community 101 - "current_performance.html"
Cohesion: 0.67
Nodes (3): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects")

### Community 102 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 103 - "Fix merge conflicts (two-machine workflow)"
Cohesion: 0.40
Nodes (4): Fix merge conflicts (two-machine workflow), Preventing it, Steps, The rule

### Community 104 - "snapshot.py"
Cohesion: 0.18
Nodes (16): _age_min(), _cleanup(), fresh_meta(), _meta(), _p(), query(), lib/snapshot.py — local DuckDB snapshot of the tills (docs/README.md › DuckDB…, The snapshot to read, refreshing it first when it's too old; None if there's… (+8 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "build"
Cohesion: 0.08
Nodes (33): why_moved(), _load_shop_regions(), Shop → Region from docs/shop-regions.md (lib/shop_regions); the built-in…, doc(), day_for(), load(), [{"till", "shop", "from", "to", "asDate"}] — datetimes / dates parsed; [] if…, The day a till's sales of `day` count on (day granularity). (+25 more)

### Community 107 - "live_month_key"
Cohesion: 0.18
Nodes (12): corporate_clients_from_db(), _db_count(), monthly_from_db(), _months(), Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,…, Reporting month's subset count (e.g. rejectBags, giftBags) from…, A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],… (+4 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "Product Performance slides (23 Nov 2026, user's call)"
Cohesion: 0.22
Nodes (9): The total, A. Bag of the Month: week by week vs the whole month, B. Top-selling bags: the top 10 moving and the 5 stuck, C. Top 5 categories: best and weakest bags, D. Male vs female bags (23 Nov 2026, user's call), E. Who buys: women vs men (23 Nov 2026, user's call), Product Performance slides (23 Nov 2026, user's call), corporate() (+1 more)

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "offer_kenya_posts"
Cohesion: 0.14
Nodes (14): Kenya timed-offer campaigns from timed_offers_config.json (normalised by…, _timed_offers(), _bags_from_file(), _derive_month(), load_config(), _norm_offer(), offer_kenya_posts(), post_window() (+6 more)

### Community 112 - "actions.py"
Cohesion: 0.25
Nodes (14): _audit(), available(), _connect(), _jsonable(), lib/actions.py — what people DO on the dashboard, kept in Supabase. The…, For carried-over rows: change only the status., A connection with the tables in place, or None (LAST_ERROR says why)., _row() (+6 more)

### Community 114 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.25
Nodes (8): Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page, Why it isn't moving — reasons, per market (`push_rules.reasons`)

### Community 119 - "_load"
Cohesion: 0.19
Nodes (14): carried_over(), followups(), get_setting(), date, {beat: row} for this page and month., Tasks from earlier months that aren't Done yet., The Sunday that starts `day`'s Sun–Sat week (the dashboard's weeks)., The weekly minimum someone set for `day`'s week, or None (use the worked-out… (+6 more)

### Community 120 - "excluded_products"
Cohesion: 0.17
Nodes (13): _bag_revenue(), _bag_revenue_range(), _range_totals(), {bags, kes, corpBags, corpKes} for s..e — POS bags (bags_sold_total), POS bag…, Average POS bags per weekday (0 = Mon) over s..e (bags_sold_daily.sql). None if…, POS bag revenue for the month, split by how the bags were sold…, _weekday_base(), daily_bags() (+5 more)

### Community 121 - "daily"
Cohesion: 0.18
Nodes (11): posts_between(), fn(), fn(start, end) → {BAG: {"KE", "TZ", "UG": posts}} from marketing's daily…, daily(), _load_backup(), _num(), parse(), {(BAG TYPE, COLOUR): {market: {date: posts}}} from the three sheets (cached for… (+3 more)

### Community 122 - "fetch"
Cohesion: 0.13
Nodes (25): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), combo_slots(), make_classifier() (+17 more)

### Community 123 - "What the page shows"
Cohesion: 0.20
Nodes (10): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 2b. Shop breakdown (22 Oct 2026, user's call), 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Data, Popover waterfall — why the units moved (26 Oct 2026, user's call) (+2 more)

### Community 124 - "Product (bag) targets"
Cohesion: 0.29
Nodes (7): A month with only a revenue target (November 2026), Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, Used as the monthly bag target (from October 2026)

### Community 125 - "sales"
Cohesion: 0.20
Nodes (10): Bag health (by bag, 18 Oct 2026), Next month (preparedness) — from the 15th, November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026), Product rating and core 5 vs other 13 categories (18 Oct 2026), Sales pace to month end (19 Oct 2026), Stocks report, month_end_lift(), ({SHOP: {BAG: units}}, {SHOP: {BAG: {colour: units}}}) over [start, end]. (+2 more)

### Community 126 - "load_lines"
Cohesion: 0.25
Nodes (7): _d(), load_lines(), _market(), _num(), float, with None / NaN as 0., ({mkt: {BAG: now}}, {mkt: {BAG: {date: end-of-day level}}}, {mkt: {BAG: {date:…, stock_facts()

### Community 127 - "_q"
Cohesion: 0.22
Nodes (9): _q(), [{week (Monday), sessions, users, orders, revenue, carts, checkouts, abandoned,…, {week ISO: {"site": {orders, bags, kes}, "people": {…}}}., Shopify title → bag key, via the dashboard's bag key: the longest run of words…, ({bag: {"clicks", "visitors", "colours": {colour: clicks}}}, combo_clicks,…, _title_bag(), wa_clicks_by_bag(), website_till_by_payment() (+1 more)

### Community 128 - "test_share_targets.py"
Cohesion: 0.22
Nodes (11): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+3 more)

### Community 129 - "build"
Cohesion: 0.25
Nodes (8): build(), Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), bag_posts(), tally(), load(), (daily, total, stock, launch, start, end) for Kenya from Odoo; daily per bag…, {BAG: (posts this month, posts last week)} — Kenya posts (col E) from the two…

### Community 130 - "start_server"
Cohesion: 0.31
Nodes (8): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_to_config(), _json()

### Community 131 - "odoo_weekly_breakdown"
Cohesion: 0.29
Nodes (8): _floor_for(), odoo_weekly_breakdown(), _perfect_week_index(), The weekly floor for the week starting `seg_start`: the override for its week,…, Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, update_weekly_history(), _week_start()

### Community 132 - "summary"
Cohesion: 0.24
Nodes (10): Kenya: insight and recommendation read the band with the chart (23 Nov 2026, user's call), market(), _pct(), DataFrame, date, Sinza → TZ, Uganda → UG, every other shop → KE (footfall Location or WhatsApp…, One row per shop-day: visitors (NaN = not counted) beside the order types, with…, The Foot Traffic page's three KPI rows for each market over [start, end]. (+2 more)

### Community 133 - "bag_key_fn"
Cohesion: 0.19
Nodes (12): _odoo_post_check(), (start, end) → {bag: {"clicks", …}} website WhatsApp taps, one Odoo pull per…, _wa_taps(), get(), meta_posts_by_bag(), ({bag: {"posts", "reach", "views"}}, {"posts", "tagged"}) — Facebook +…, bag_key_fn(), key() (+4 more)

### Community 138 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.22
Nodes (7): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does, Current Performance (doc)

### Community 145 - "timed_offers.py (generator)"
Cohesion: 0.14
Nodes (14): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+6 more)

### Community 153 - "New Products Analytics (doc)"
Cohesion: 0.16
Nodes (14): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix) (+6 more)

### Community 154 - "Shop Launch"
Cohesion: 0.20
Nodes (9): Config, Launch day, Marketing posts, Race lines, sales by day, product performance, folding (9 Nov 2026, user's call), Sales, Sales keyed in late (9 Nov 2026, user's call), Shop Launch, What the page shows (+1 more)

### Community 155 - "Offer Picking (doc)"
Cohesion: 0.25
Nodes (9): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES) (+1 more)

### Community 156 - "weekly_newproducts.py"
Cohesion: 0.12
Nodes (26): New Products slides (23 Nov 2026, user's call), build(), {TYPE: {"kes", "shops": {SHOP: {"n", "kes"}}}} for the runway types over…, ({TYPE: Kenya shop on-hand}, {TYPE: Sinza + Uganda on-hand}) — live Odoo., The NP.runway payload: {days, bags: [{name, created, category, stockKe,…, Product name → bag type (see the module docstring)., [{name, created, category}] newest first — the runway bag types as of today; []…, {TYPE: bags sold} for the given runway types over [start, end] — POS bags,… (+18 more)

### Community 157 - "build"
Cohesion: 0.12
Nodes (16): Offer type summary (matrix), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, _read_offers(), _read_offers_cache(), _assign_price(), build(), _category_of() (+8 more)

### Community 158 - "google_auth.py (shared auth module)"
Cohesion: 0.25
Nodes (8): google_auth.py (shared auth module), google_credentials.json (OAuth desktop client), google_token.json (OAuth token), main.py (refresh + serve dashboard), OAuth token expiry issue (Testing mode, ~7 day expiry), reauth.py (re-login script), service_account.json (recommended, permanent auth), Service account chosen for zero-maintenance auth + enabling in-dashboard Refresh

### Community 159 - "scripts/receipt_combos.py"
Cohesion: 0.33
Nodes (5): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…

### Community 160 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 161 - "design-taste-frontend (anti-slop frontend skill)"
Cohesion: 0.18
Nodes (12): design-taste-frontend (related skill), design-taste-frontend (anti-slop frontend skill), Brief-First Process (8-step design workflow), Hard Bans (typography, color, layout, code, content clichés), Pre-Flight Checklist (90+ items), Redesign Protocol (upgrading existing UI), Three Dials — DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, Three AI-generated design clusters (calibration reference) (+4 more)

### Community 162 - "write_atomic"
Cohesion: 0.12
Nodes (18): inject(), build(), _cfg(), _colour(), _folder(), canon(), _moves(), Odoo product name → the dashboard's bag name (Offer Picking's _build_catalog… (+10 more)

### Community 163 - "get_engine"
Cohesion: 0.29
Nodes (7): Engine, _env(), get_engine(), The process's reused connection (opened on first query). Every generator runs…, Build a SQLAlchemy URL from the environment, or None if unset. Accepts…, _shared_conn(), _url()

### Community 165 - "_build_period"
Cohesion: 0.18
Nodes (6): _build_period(), _offer_types(), _pick_target(), Latest target row for `shop` with this period that overlaps [start, end]. A…, Matrix payload: rows, per-row category / tier cells, and the period's Top-5…, _region_of()

### Community 166 - "Bags on offer vs not on offer"
Cohesion: 0.15
Nodes (13): Bags on offer vs not on offer, Corporate-lead till orders, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Out of stock — call back, Shop birthdays, Shop metrics (vs the Odoo revenue target), Sinza & Uganda (Oct 2026) — replaced 9 Oct 2026 (+5 more)

### Community 167 - "Menu 1 Current Performance in the 3-beat layout (preview)"
Cohesion: 0.15
Nodes (12): 0. New: an executive summary strip at the top of the page, 1. Sales, Weekly Sales and Remaining Target cards, 2. Followers & Reach, 3. Weekly Performance — Week 1 to Latest, 4. Why Did We Move?, 5. Sales vs Monthly Target, Week-over-Week, Bare Minimum, 6. Forward Projections (Standard and Forecasted), 7. Price per Bag, and On offer vs not on offer (+4 more)

### Community 168 - "update_np_weekly_history"
Cohesion: 0.29
Nodes (7): _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)., Ordinal among the month's perfect weeks (>=5 days in month), so the first FULL…, Snapshot each Sun–Sat week (sales, Kenya/Outside posts) into…, update_np_weekly_history()

### Community 169 - "Footfall and Marketing (21 Oct 2026, user's call)"
Cohesion: 0.20
Nodes (9): Actions (rules), Correlations ("Posts and ads vs visitors"), Data traps (said on the page), Definitions, Footfall and Marketing (21 Oct 2026, user's call), Regenerate, Shop mapping (`lib/footfall.SHOPS`), Sources (+1 more)

### Community 170 - "Offers"
Cohesion: 0.29
Nodes (5): Offers, Kenya offers per day (each day reads its own month's bags_offer_source file) +…, {mkt: {BAG: [text]}} for Sinza / Uganda from offers_monthly.csv., _offers(), Offers lookup (Kenya) — or None when the offer data can't be loaded.

### Community 172 - "realistic_rates"
Cohesion: 0.53
Nodes (6): _clamp(), ({SHOP: {BAG: units a week}}, {SHOP: {"recent", "season", "growth"}}) — recent…, realistic_rates(), growth(), season(), tot()

### Community 173 - "follower_test.py"
Cohesion: 0.27
Nodes (9): _best(), _link(), DataFrame, _rank(), lib/follower_test.py — does a new follower become a sale? Pins new follows,…, Best Spearman score of x[t] vs y[t+lag] over lags 0..max_lag → (score, lag)., One link in plain words for the slide., run() (+1 more)

### Community 174 - "Product Performance — Shop breakdown: progress"
Cohesion: 0.22
Nodes (8): 1. Spec — DONE, 2. Data — DONE, 3. Page section — DONE, 4. Sidebar and sticky bar — DONE, 5. Visual check — DONE, 6. Wrap-up — DONE, Product Performance — Shop breakdown: progress, Summary

### Community 175 - "Ralph task — "Out of stock — call back" demand per shop"
Cohesion: 0.25
Nodes (7): match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, Established facts (do not re-investigate), Every iteration, Periods (dates in Africa/Nairobi), Ralph task — "Out of stock — call back" demand per shop, Stopping

### Community 177 - "_matches_sheet"
Cohesion: 0.18
Nodes (10): Three countries, one page (9 Oct 2026), _matches_sheet(), _opt_close(), Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Same slot count and every slot overlaps under SOME pairing (any order: the…, The sheet label this Odoo combo maps to, or None if it isn't on the sheet.…, _slots_fit(), Inputs (from the user, Oct 2026) (+2 more)

### Community 178 - "timed_offers.py"
Cohesion: 0.14
Nodes (19): _acc(), _bucket(), build_compare(), _cmp_lines(), _days(), _kenya_net_moves_since(), kenya_stock_by_bag(), _offer_compare() (+11 more)

### Community 179 - "Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)"
Cohesion: 0.20
Nodes (9): 1. Spec — DONE, 2. SQL + library — DONE, 3. Generator — DONE, 4. Page — DONE, 5. Actions — DONE, 6. Visual check — DONE, 7. Wrap-up — DONE, Findings (16 weeks, 28 Jun – 17 Oct 2026; last fully counted week 11–17 Oct) (+1 more)

### Community 180 - "main.py"
Cohesion: 0.11
Nodes (22): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, Denri Africa — Marketing Dashboard Launcher… (+14 more)

### Community 181 - "Weekly Report"
Cohesion: 0.22
Nodes (8): Colours for up and down, totals strips (23 Nov 2026, user's call), Combos and offers slides (23 Nov 2026, user's call), Data sources, Regenerate, Slide 1: Sales this month (the Sales card and its hover), Two reports in one page: Marketing and Sales (23 Nov 2026, user's call), Weekly Report, What it is (22 Nov 2026, user's call)

### Community 182 - "html"
Cohesion: 0.12
Nodes (15): _new_products(), This month's new products: data/new_products.txt (lib/new_products_list) — the…, _growth_tracking(), data/growth_tracking.json + the report month: live (so far + projected + this…, _offer_bagtypes_by_region(), On-offer bag types per region, read from self_made_combos.html's SMC block:…, load_pages(), bag_of() (+7 more)

### Community 183 - "family"
Cohesion: 0.29
Nodes (8): leads(), ({BAG: units}, {BAG: {colour: units}}) at CBD/Stock., {period: {SHOP: {BAG: {"n", "online", "walkin", "colours": {c: n}}}}} — people…, warehouse_stock(), family(), _load(), _norm(), Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…

### Community 184 - "base_name"
Cohesion: 0.33
Nodes (7): base_name(), dispatch_by_product_shop(), _num(), The catalogue key for an Odoo product name: norm() without the "[REJECT]" tag…, {NORM(product): {SHOP: bags}} of POS bag sales in [start, end]; None if DB…, {NORM(product): {SHOP: bags distributed in}} from combined_distribution.sql's…, sales_by_product_shop()

### Community 185 - "_reveal_page"
Cohesion: 0.50
Nodes (4): Run script-only HTML in an invisible frame (same origin, so it can reach…, Fade the page area back in on a page that has no dashboard frame (password…, _reveal_page(), _run_js()

### Community 186 - "Out-of-stock demand — people, not requests"
Cohesion: 0.29
Nodes (7): Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods, Show it as, Tests

### Community 187 - "Ralph loop brief — Footfall and Marketing page"
Cohesion: 0.25
Nodes (7): DATA FACTS (verified 21 Oct 2026), DONE, ESCAPE HATCH, PROJECT RULES (must hold every iteration), Ralph loop brief — Footfall and Marketing page, SELF-CORRECTION, SUB-GOALS (do in order; tick each in notes/footfall_progress.md with the command output that proved it)

### Community 188 - "last_week_from_db"
Cohesion: 0.25
Nodes (8): last_week_from_db(), Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary(), week_start_of(), weekly_from_db()

### Community 189 - "data"
Cohesion: 0.15
Nodes (14): _live_bags(), {BAG (upper): official full price} from bag_original_prices.json (fallback)., _read_bag_prices(), _categories(), {BAG: CATEGORY} from bag_tiers.csv (the Bags on offer menu's editable table)., _load_combos_by_shop(), _from_file(), _nonempty() (+6 more)

### Community 191 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 193 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 194 - "Bag Tracking"
Cohesion: 0.33
Nodes (5): Bag Tracking, Page, Prices, Stock, The bags

### Community 195 - "_combo_button_usage"
Cohesion: 0.22
Nodes (8): _combo_button_usage(), _combo_norm_option(), combos_by_shop(), _norm(), _tokmatch(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Per-shop view for Shops Efficiency, keyed by shop-location label (e.g.…, One combo slot-option → its distinctive bag token(s), colours/category words…

### Community 197 - "_build_catalog"
Cohesion: 0.33
Nodes (7): _build_catalog(), _is_full_price(), Letters and digits only, so 'CODE3' meets 'CODE 3' and 'FANNYPACK(N)' meets…, {_staff_key(catalogue bag type): staff price} from staff_prices.json (a 0 = no…, Every bag the user can pick for a slot, with two prices from the offers sheet:…, _read_staff_prices(), _staff_key()

### Community 198 - "compute_period"
Cohesion: 0.12
Nodes (11): apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _metric(), pct(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period. (+3 more)

### Community 200 - "shop_stock_levels.py"
Cohesion: 0.14
Nodes (23): bag_categories(), buffer_stock(), build(), fit(), grand_total(), needs(), new_bags(), _next_month() (+15 more)

### Community 203 - "shops_dispatch.py"
Cohesion: 0.21
Nodes (15): build_period(), distributed_in(), main(), q(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only. (+7 more)

### Community 204 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 205 - "render"
Cohesion: 0.60
Nodes (5): growthData(), render(), drawGrowth(), table(), wf()

### Community 207 - "followup"
Cohesion: 0.18
Nodes (13): Did last week's calls work? (`push_rules.record_week`, `followup`), Last week's calls checked against what happened (lib/push_rules.followup), then…, weekly(), followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., Store this week's top actions under its Sunday. Re-running in the same week…, The most recent PREVIOUS week's calls and what happened since: sold/day since…, record_week() (+5 more)

### Community 208 - "test_sheet_reads.py"
Cohesion: 0.47
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 209 - "Slide 2: Did new followers sell bags? (Kenya)"
Cohesion: 0.33
Nodes (6): Follower test: does a new follower become a sale? (23 Nov 2026, user's call), Foot traffic band (22 Nov 2026, user's call), Slide 2: Did new followers sell bags? (Kenya), Slide 2b: Followers vs sales, Sinza and Uganda (23 Nov 2026, user's call), What it found first (22 Nov 2026), WhatsApp buyers by source (23 Nov 2026, user's call)

### Community 210 - "norm"
Cohesion: 0.16
Nodes (14): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, _aliases(), _Deriver, norm(), odoo_name(), prime_offer_flags(), _products() (+6 more)

### Community 211 - "main"
Cohesion: 0.33
Nodes (5): main(), month_window(), date, _query_ready(), First → last calendar day of the LIVE month (today's month; see…

### Community 212 - "shop-birthdays.md"
Cohesion: 0.20
Nodes (8): Design Tokens (colors, typography, spacing), Semantic color rules (green=good, amber=risk, red=critical, cyan=info), Analytics Dashboard specific rules (VISUAL_DENSITY: dense), Shop birthdays, Shop → opening date, Where it shows, Region colour palette (reference for Executive Dashboard), Shops & Regions (doc — source of truth)

### Community 213 - "reject_variants"
Cohesion: 0.33
Nodes (7): _parse_colour(), First primary colour token found in a name (longest-first), Title-cased; '' if…, Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share…, Per-[REJECT]-product variant rows for a name-filtered offer, for the filterable…, reject_variants(), _match_bag(), _singular_tokens()

### Community 216 - "shop_breakdown"
Cohesion: 0.33
Nodes (6): corp(), corporate_period(), [(product, bags, kes)] — Corporate app bags paid in [s, e]…, {period: {market: {total, rev, shops: [...]}}} — units / revenue per shop…, shop_breakdown(), shop_name()

### Community 217 - "price"
Cohesion: 0.50
Nodes (4): Per bag × market: the facts (`push_rules.facts`, `add_peers`), Prices (30 Oct 2026, user's call), price(), Price per Bag card: the price gap, and the group that drags revenue most.

### Community 218 - "requests_block"
Cohesion: 0.33
Nodes (5): dispatch_shop(), Dispatch-module shop name (ELDORET, DAR-ES-ALAM, NYERI…) → the page's shop name., Shop requests vs received (this month · last month) and the production approved…, requests_block(), _shop()

### Community 219 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

### Community 220 - "test_no_google.py"
Cohesion: 0.47
Nodes (4): _BrokenSheet, Pages build without a Google login: MONTHLY_TARGET falls back to a bare header,…, test_target_total_is_the_odoo_targets_without_the_sheet(), test_unreadable_sheet_gives_header_only()

### Community 221 - "bag_gender.py"
Cohesion: 0.50
Nodes (4): functools, gender(), lib/bag_gender.py — who a bag is for (Male / Female / Unisex), from…, _table()

### Community 222 - "safe_int"
Cohesion: 0.40
Nodes (5): _bag_level_bags(), Bag types with posts logged without a colour in any of the posting tabs., safe_int(), is_bag_level(), A tab_rows() row of posts with no colour (from the bag type's TOTAL row):…

### Community 223 - "_analyze_region"
Cohesion: 0.50
Nodes (4): _analyze_region(), STOCK_LEVELS: colour=A(0), product_name=C(2), Runs all three posting sections for one region. sales_col – column index in…, _sl_key()

### Community 224 - "load_posts"
Cohesion: 0.67
Nodes (4): load_posts(), num(), tally(), ({BAG: [kenya, outside]} last week, {BAG: [kenya, outside]} this month) from…

### Community 225 - "sendable_by_month_end"
Cohesion: 0.50
Nodes (4): {shop: units} — `left` units shared over {shop: gap} in proportion, leftovers…, What can still be sent (docs › Shop requests — realistic performance): per shop…, sendable_by_month_end(), _share_out()

## Knowledge Gaps
- **269 isolated node(s):** `PERF`, `The rule`, `Steps`, `Preventing it`, `graphify` (+264 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1183 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_query()` connect `run_query` to `shop_corporate.py`, `build`, `tests/test_receipt_combos.py`, `odoo_weekly_breakdown`, `summary`, `json`, `os`, `generator`, `weekly_newproducts.py`, `live_month_window`, `stock.py`, `write_atomic`, `live_anchor`, `chronos_train.py`, `get_engine`, `build_payload`, `offer_picking.py`, `shop_requests.py`, `shop_launch.py`, `weekly_report.py`, `estimated_targets.py`, `last_week_from_db`, `fetch_new_products_data`, `oos_callbacks.py`, `_combo_button_usage`, `test_oos_callbacks.py`, `_enrich_deals`, `shop_stock_levels.py`, `fetch_posting_data`, `build`, `build`, `main`, `fetch`, `shop_breakdown`, `push_planner.py`, `negative_fixes.py`, `snapshot.py`, `build`, `live_month_key`, `excluded_products`, `fetch`, `sales`, `load_lines`, `_q`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `Vercel hosted version (static snapshot)` connect `timed_offers.py (generator)` to `main.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **What connects `PERF`, `The rule`, `Steps` to the rest of the system?**
  _269 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `shop_corporate.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14532019704433496 - nodes in this community are weakly interconnected._
- **Should `laya.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09243697478991597 - nodes in this community are weakly interconnected._
- **Should `tests/test_receipt_combos.py` be split into smaller, more focused modules?**
  _Cohesion score 0.053208137715179966 - nodes in this community are weakly interconnected._
- **Should `oos_chip.js` be split into smaller, more focused modules?**
  _Cohesion score 0.08067375886524823 - nodes in this community are weakly interconnected._