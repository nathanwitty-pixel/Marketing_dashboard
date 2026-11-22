# Graph Report - Marketing_dashboard  (2026-11-22)

## Corpus Check
- 250 files · ~1,256,813 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 22 file(s) not represented in the graph (top: .csv 15, (none) 2, .toml 1)

## Summary
- 2971 nodes · 5966 edges · 215 communities (171 shown, 44 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 197 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `11a13fd7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- shop_corporate.py
- laya.py
- lib/receipt_combos.py
- oos_chip.js
- chart_switcher.js
- he
- Kitengela Rejects tracker (timed offer)
- bag_quant.py
- Denri Africa Dashboard Design System (skill)
- v5_theme.js
- name_match.py
- bare_minimum setting (weekly target floor)
- offer_data.py
- _fetch_sinza_monthly
- run_query
- month_extras.py
- actions.py
- le
- Ps
- Month-End Routine
- sticky_controls.js
- shop_requests.py
- main.py
- Monthly Report (doc)
- ls
- vs
- anime.umd.min.js
- Dashboard Menu Docs (spec index)
- timed_offers.py
- si
- Bags on offer vs not on offer
- push_rules.py
- streamlit_app.py
- stock.py
- monthly_report.py
- report_month.py
- db.py
- _read_deals
- build_payload
- Shops Efficiency Tracking spec doc
- build
- marketing_posts.py
- shop_launch.py
- page_sidebar.js
- weekly_report.py
- Combos & Power Deals by Shop panel (#combo-shop)
- test_fixC_sql.py
- lib/db.py (Supabase session pooler DB access)
- CLAUDE.md
- history.py (read months back)
- je
- ads.py
- shops_efficiency.py
- datetime
- algorithmic-art skill
- dataviz-charts skill
- scripts/test_receipt_combos.py
- footfall.py
- Product (bag) targets
- High-End Visual Design skill
- safe_int
- publish.py
- fetch_new_products_data
- daydream skill (Vault Daydream)
- posting_yields.py
- _enrich_deals
- num
- new_products.py
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- _combo_button_usage
- build
- marketing_dashboard.sql
- fetch_posting_data
- build
- shop_birthdays.py
- kpi_anim.js
- Weekly Report
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- why_moved.js
- theme.py
- push_laya.py
- os
- test_push_planner.py
- self_made_combos.py
- json
- _load_combos_by_shop
- F
- foot_traffic.py
- test_stockout_demand.py
- Out-of-stock demand — people, not requests
- push_planner.py
- moves
- ns
- Dashboard Architecture (static HTML + Python generator + injected data block)
- negative_fixes.py
- custom_range.py
- Shop Launch
- product_targets.py
- Bag Signals — quant view of each bag (posting · stock · selling)
- beats.py
- current_performance.html
- attach
- Fix merge conflicts (two-machine workflow)
- snapshot.py
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- why_moved.py
- follower_test.py
- Ralph task — only three sheet tabs left
- product_performance.py
- Bag targets October 2026_3acbad00.md
- _resolve_bag
- Laya
- perf_data.js
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- _bg_jobs
- Offers
- names
- fetch
- What the page shows
- data
- forward_projections.py
- Self-made combos vs running combos (doc)
- Ralph task — "Out of stock — call back" demand per shop
- _reveal_page
- run_scripts
- start_server
- load_config
- Marketing Dashboard — Google Sheets access & setup (doc)
- odoo_marketing.py
- contextlib
- Chart type switcher (every chart, every menu)
- denri_mkt_timed_offer* Supabase tables
- get_engine
- New Products Analytics (doc)
- Slide 2: Did new followers sell bags? (Kenya)
- Offer Picking (doc)
- re
- build
- google_auth.py (shared auth module)
- scripts/receipt_combos.py
- _dead_stock_region
- write_atomic
- bag_tracking.py
- _seasonality
- Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)
- followup
- Stock record accuracy (NEGATIVE FIX LOG) — progress
- Menu 1 Current Performance in the 3-beat layout (preview)
- odoo_marketing_audit.py
- Footfall and Marketing (21 Oct 2026, user's call)
- explain
- Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)
- get_rows
- Product / name matching (doc)
- Product Performance — Shop breakdown: progress
- family
- Sales-share targets per product
- price
- Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)
- _read_bom_costs
- Answer
- timed_offers.py (generator)
- bags_on_offer.py
- __init__.py
- odoo_tabs.py
- Ralph loop brief — Footfall and Marketing page
- oos_callbacks.py
- Bag signals — quant finance applied to product sales
- ambiguous_python_import_17686b6faac5
- _alignment_region
- Bag Tracking
- realistic_rates
- offer_picking.py
- compute_period
- shop_stock_levels.py
- shops_dispatch.py
- Combos from receipts — running vs self-made
- render
- shop_breakdown
- _odoo_colour
- test_sheet_reads.py
- Odoo marketing data audit
- ODOO_MARKETING_AUDIT.md
- load_posts
- queries.py
- load_catalog
- posts_between
- _month_archived

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 86 edges
2. `fetch()` - 41 edges
3. `data()` - 40 edges
4. `fetch_posting_data()` - 39 edges
5. `check_connection()` - 32 edges
6. `le` - 31 edges
7. `build_payload()` - 30 edges
8. `get_gspread_client()` - 27 edges
9. `ls` - 26 edges
10. `excluded_products()` - 26 edges

## Surprising Connections (you probably didn't know these)
- `What the page shows (per period)` --references--> `_market_records()`  [INFERRED]
  docs/bags-on-offer.md → generators/bags_on_offer.py
- `The split — by each bag's share of recent sales` --references--> `bag_classifier()`  [INFERRED]
  docs/product-targets.md → generators/self_made_combos.py
- `Inputs (read only — nothing is written to Odoo or the sheet)` --references--> `bag_classifier()`  [INFERRED]
  docs/push-planner.md → generators/self_made_combos.py
- `Regenerate` --references--> `fetch()`  [INFERRED]
  docs/bags-on-offer.md → generators/self_made_combos.py
- `Sales pace to month end (19 Oct 2026)` --references--> `month_end_lift()`  [INFERRED]
  docs/shop-stock-levels.md → generators/shop_stock_levels.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]

## Communities (215 total, 44 thin omitted)

### Community 0 - "shop_corporate.py"
Cohesion: 0.15
Nodes (25): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), _acronym(), build(), _maybe(), owns(), corporate_team_receipts(), _d() (+17 more)

### Community 1 - "laya.py"
Cohesion: 0.16
Nodes (19): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, _ask(), ask_choice(), ask_yes_no(), available(), _cache_get(), _cache_put() (+11 more)

### Community 2 - "lib/receipt_combos.py"
Cohesion: 0.06
Nodes (64): _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, _fill_units(), _infer(), _power_products(), lib/offer_units.py — units moved per listed offer for a month, from Odoo…, units(), bag_key() (+56 more)

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

### Community 7 - "bag_quant.py"
Cohesion: 0.05
Nodes (51): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+43 more)

### Community 8 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.08
Nodes (28): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards) (+20 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 12 - "offer_data.py"
Cohesion: 0.20
Nodes (12): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), offer_data.py ─────────────────────────────────────────────────────────────────… (+4 more)

### Community 13 - "_fetch_sinza_monthly"
Cohesion: 0.18
Nodes (14): _analyze_region(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), MONTHLY_SALES: colour=A(0), product_name=B(1), MONTHLY_MARKETING_POST: colour=A(0), product_name=C(2), STOCK_LEVELS: colour=A(0), product_name=C(2) (+6 more)

### Community 14 - "run_query"
Cohesion: 0.10
Nodes (26): last_week_from_db(), Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, _bag_revenue_range(), _corporate_lines(), odoo_weekly_breakdown(), _range_totals(), {bags, kes, corpBags, corpKes} for s..e — POS bags (bags_sold_total), POS bag…, Average POS bags per weekday (0 = Mon) over s..e (bags_sold_daily.sql). None if… (+18 more)

### Community 15 - "month_extras.py"
Cohesion: 0.16
Nodes (22): _bags_on_offer(), _block(), build_extras(), cp_more_month(), _deals(), _month_dates(), _pick(), _posting() (+14 more)

### Community 16 - "actions.py"
Cohesion: 0.08
Nodes (44): _floor_for(), The weekly floor for the week starting `seg_start`: the override for its week,…, _audit(), available(), carried_over(), _connect(), followups(), get_setting() (+36 more)

### Community 17 - "le"
Cohesion: 0.09
Nodes (3): Ht, le, Ut

### Community 19 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

### Community 20 - "sticky_controls.js"
Cohesion: 0.20
Nodes (15): bind(), embedHost(), headerOf(), init(), initSections(), injectCss(), place(), setPinned() (+7 more)

### Community 21 - "shop_requests.py"
Cohesion: 0.14
Nodes (21): _onoff(), Shop requests vs received (this month · last month) and the production approved…, requests_block(), _d(), _f(), _match(), _offer_label(), _offers() (+13 more)

### Community 22 - "main.py"
Cohesion: 0.12
Nodes (17): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, Denri Africa — Marketing Dashboard Launcher… (+9 more)

### Community 23 - "Monthly Report (doc)"
Cohesion: 0.22
Nodes (9): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+1 more)

### Community 26 - "anime.umd.min.js"
Cohesion: 0.15
Nodes (8): ce(), de(), Me, Oe(), rs, St(), ts(), Ye

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.13
Nodes (17): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, google_auth.py (Sheets auth), Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics (+9 more)

### Community 28 - "timed_offers.py"
Cohesion: 0.05
Nodes (59): _corporate_bags(), The month's revenue target (KES): Odoo sales_pos_target amount (pos +…, (corporate bags, corporate KES received) in the given month, live from Odoo…, _revenue_target(), _acc(), _bucket(), build_compare(), build_offer() (+51 more)

### Community 29 - "si"
Cohesion: 0.24
Nodes (3): ii(), ri, si

### Community 30 - "Bags on offer vs not on offer"
Cohesion: 0.12
Nodes (14): Bags on offer vs not on offer, Corporate-lead till orders, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Regenerate, Shop birthdays, Shop metrics (vs the Odoo revenue target) (+6 more)

### Community 31 - "push_rules.py"
Cohesion: 0.11
Nodes (17): _cover_txt(), _days_back(), _kind(), _n(), not_moving(), posting_median(), rank(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).… (+9 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.09
Nodes (20): SCRIPT_TIMEOUT = 600s config, hashlib, html, streamlit, _bg_rebuild(), work(), _load_secrets_into_env(), _month_end_running() (+12 more)

### Community 33 - "stock.py"
Cohesion: 0.24
Nodes (13): _codes_for(), _inlist(), odoo_stock_at_location(), odoo_stock_by_product(), odoo_stock_by_shop_code(), _ok(), _qty(), lib/stock.py — live Odoo on-hand stock, per product / market / shop. Single… (+5 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.12
Nodes (15): _bag_stock(), _cause(), _combo_bags(), esc(), fmt(), ladder_strip(), _norm_bag(), pct() (+7 more)

### Community 35 - "report_month.py"
Cohesion: 0.13
Nodes (25): calendar, count_complete_weeks_in_month(), anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key() (+17 more)

### Community 36 - "db.py"
Cohesion: 0.09
Nodes (35): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+27 more)

### Community 37 - "_read_deals"
Cohesion: 0.11
Nodes (17): _as_day(), _local_deal_rows(), _in_month(), 2026-10-25' / date / None → date or None., Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), Blocker counter (+9 more)

### Community 38 - "build_payload"
Cohesion: 0.12
Nodes (18): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+10 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.20
Nodes (10): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.html page (+2 more)

### Community 40 - "build"
Cohesion: 0.24
Nodes (11): _alt_cost(), _apply_alias(), build(), _combo_cost(), _combo_slots(), Parse `const SMC = {…}` out of self_made_combos.html (no DB round-trip)., One combo alternative (e.g. 'Amaya Handbag') → its BOM production cost., Combo name → list of slots, each a list of alternative strings. (+3 more)

### Community 41 - "marketing_posts.py"
Cohesion: 0.16
Nodes (21): _bag_category(), _category(), daily(), _date(), is_bag_level(), _load_backup(), _num(), parse() (+13 more)

### Community 42 - "shop_launch.py"
Cohesion: 0.12
Nodes (26): build(), _add(), launch_curve(), _cfg(), _day_expr(), first_sale(), kenya_posts(), load_categories() (+18 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "weekly_report.py"
Cohesion: 0.10
Nodes (17): field(), fmt(), _ft_band(), kes_m(), n(), other(), proj_field(), weekly_report.py — the weekly marketing report as slides (Headline / Graph /… (+9 more)

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

### Community 51 - "ads.py"
Cohesion: 0.23
Nodes (11): campaigns(), _f(), market_week(), notes(), date, lib/ads.py — marketing's Weekly Ads Performance Report, as data (spec:…, Every campaign-week row, with spend_kes added (USD × USD_KES)., The report's Sun–Sat weeks (week starts), oldest first. (+3 more)

### Community 52 - "shops_efficiency.py"
Cohesion: 0.11
Nodes (16): apply_odoo(), apply_walkins(), fmt_pct(), load(), _metric(), metric_byshop(), odoo_stock_levels(), parse_sheet() (+8 more)

### Community 53 - "datetime"
Cohesion: 0.10
Nodes (19): datetime, Reject Sale pricing (Kitengela) → reject_sales.html (payload `RJ`). A…, weekly_sales.py — the weekly-sales fix. Computes the CURRENT Sun–Sat week's…, lib, lib/new_products_list.py — which bag types count as this month's NEW PRODUCTS.…, lib/paths.py — where every kind of file lives. Use these instead of building…, lib/shop_regions.py — Shop → Region from docs/shop-regions.md (the source of…, openpyxl (+11 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.29
Nodes (7): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.)

### Community 56 - "scripts/test_receipt_combos.py"
Cohesion: 0.32
Nodes (15): classify(), lines: [{receipt, d, product, qty, amount}] → per-market summary: {running:…, infer(), L(), Tests for receipt_combos.py + name_match.py — python -m pytest scripts -q, test_alternatives_and_singles(), test_bulk_receipts_are_not_combos(), test_four_bags_at_two_prices_are_two_combos() (+7 more)

### Community 57 - "footfall.py"
Cohesion: 0.27
Nodes (11): daily(), DataFrame, date, lib/footfall.py — footfall (visitors counted per shop per day) joined to walk-…, Paid-ad WhatsApp leads per WhatsApp shop per Sun–Sat week: chats, bought,…, The Sunday that starts d's Sun–Sat week., One row per footfall shop per day: visitors (NaN = not counted), walk-in orders…, One row per shop per Sun–Sat week. Conversion and revenue use COUNTED days… (+3 more)

### Community 58 - "Product (bag) targets"
Cohesion: 0.18
Nodes (11): A month with only a revenue target (November 2026), Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026) (+3 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "safe_int"
Cohesion: 0.16
Nodes (22): _bag_level_bags(), _build_no_convert(), _fetch_monthly_kenya(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int() (+14 more)

### Community 61 - "publish.py"
Cohesion: 0.12
Nodes (24): fnmatch, action_js(), main(), node_check(), Run the sticky-controls checks on every wired page and print the markdown…, edge_dump(), embedded(), inline_local() (+16 more)

### Community 62 - "fetch_new_products_data"
Cohesion: 0.20
Nodes (14): fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_sales_window() (+6 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "posting_yields.py"
Cohesion: 0.27
Nodes (8): _mkt_perfect_week_index(), _mkt_week_label(), posting_yields.py…, Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]., current = {region: {key: {productName,colour,category,bagType,stock}}}. A new…, update_clearance(), update_mkt_history()

### Community 65 - "_enrich_deals"
Cohesion: 0.15
Nodes (10): _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg(), _tier_window(), _odoo_stock_by_shop() (+2 more)

### Community 66 - "num"
Cohesion: 0.20
Nodes (11): _garr_line(), gnum(), num(), _offers(), _parse_offers(), _units(), This month's timed-offer campaigns, flattened for storage. The live TO payload…, Greedy single-line array extractor — handles nested [[...],[...]] arrays. (+3 more)

### Community 67 - "new_products.py"
Cohesion: 0.10
Nodes (20): _base_colour(), _merge_rows_by_base_colour(), _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), odoo_combo_product_bags(), odoo_lifetime_product_bags(), odoo_month_product_bags() (+12 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "_combo_button_usage"
Cohesion: 0.10
Nodes (18): Three countries, one page (9 Oct 2026), _combo_button_usage(), _combo_norm_option(), combos_by_shop(), _norm(), _tokmatch(), _matches_sheet(), _opt_close() (+10 more)

### Community 71 - "build"
Cohesion: 0.18
Nodes (12): Bulk orders, build(), categories(), _load_json(), offer_days(), {BAG: category} — the bag type's usual catalogue category, else its Odoo…, {period: {BAG: {...}}} — for EVERY bag sold in Kenya in the period: Kenya walk-…, {BAG: {"now", "full", "lines", "days"}} — the Kenya price a bag is selling at:… (+4 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "fetch_posting_data"
Cohesion: 0.09
Nodes (19): _bt_on_offer(), count_complete_weeks_in_month(), _dead_clear(), fetch_posting_data(), _clear(), _yield(), _fold_bag_level(), load_dead_thresholds() (+11 more)

### Community 74 - "build"
Cohesion: 0.18
Nodes (11): actions(), build(), agg(), week_tot(), num(), pearson(), footfall_marketing.py — Footfall and Marketing page (spec: docs/footfall-…, What we can do' — by rule (docs/footfall-marketing.md › Actions). Each names a… (+3 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "kpi_anim.js"
Cohesion: 0.60
Nodes (5): count(), fmt(), key(), parse(), scan()

### Community 77 - "Weekly Report"
Cohesion: 0.18
Nodes (10): A. Bag of the Month: week by week vs the whole month, B. Top-selling bags: the top 10 moving and the 5 stuck, C. Top 5 categories: best and weakest bags, D. Male vs female bags (23 Nov 2026, user's call), Data sources, Product Performance slides (23 Nov 2026, user's call), Regenerate, Slide 1: Sales this month (the Sales card and its hover) (+2 more)

### Community 78 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.11
Nodes (18): Bag health (by bag, 18 Oct 2026), Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026), Page, Product rating and core 5 vs other 13 categories (18 Oct 2026) (+10 more)

### Community 79 - "why_moved.js"
Cohesion: 0.36
Nodes (12): bestWeek(), bestWeeks(), build(), fillWeeks(), getW(), hasKey(), mark(), onClick() (+4 more)

### Community 80 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), lib/theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 81 - "push_laya.py"
Cohesion: 0.13
Nodes (20): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+12 more)

### Community 82 - "os"
Cohesion: 0.12
Nodes (17): build(), _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,… (+9 more)

### Community 83 - "test_push_planner.py"
Cohesion: 0.19
Nodes (17): add_peers(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m…, ISO date n days before END (0 = END)., _row() (+9 more)

### Community 84 - "self_made_combos.py"
Cohesion: 0.07
Nodes (41): Buckets, Counted by how it was sold, Per-shop combo-button chips (red when < half best-in-region), Shop -> Region table, _load_source(), bags_offer_source.json if written in the last 15 min for this month (and it has…, _add_noffer_posts(), per_bag() (+33 more)

### Community 85 - "json"
Cohesion: 0.11
Nodes (23): One-off: restore August's Offer Type figures into monthly_report_history.json…, dotenv, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the… (+15 more)

### Community 86 - "_load_combos_by_shop"
Cohesion: 0.67
Nodes (4): _load_combos_by_shop(), _from_file(), _nonempty(), Per-shop combo / power-deal view for the panel — built **live from Odoo** via…

### Community 87 - "F"
Cohesion: 0.15
Nodes (24): action(), context(), (code, plain sentence, units at stake, confidence 0..1) for one bag × market.…, What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F() (+16 more)

### Community 88 - "foot_traffic.py"
Cohesion: 0.27
Nodes (10): market(), _pct(), DataFrame, date, lib/foot_traffic.py — the Denri dashboard's Foot Traffic page figures, per…, Sinza → TZ, Uganda → UG, every other shop → KE (footfall Location or WhatsApp…, One row per shop-day: visitors (NaN = not counted) beside the order types, with…, The Foot Traffic page's three KPI rows for each market over [start, end]. (+2 more)

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.14
Nodes (10): Agent skills — retail analytics, Test a skill, Use in another project, Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods (+2 more)

### Community 91 - "push_planner.py"
Cohesion: 0.12
Nodes (24): build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), load_data(), main() (+16 more)

### Community 92 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 94 - "Dashboard Architecture (static HTML + Python generator + injected data block)"
Cohesion: 0.40
Nodes (5): DATA_START/DATA_END comment marker injection pattern, build_all.py (rebakes every page), Dashboard Architecture (static HTML + Python generator + injected data block), .github/workflows/refresh.yml CI workflow, shell.html (sidebar nav frame, loads each page into an iframe)

### Community 95 - "negative_fixes.py"
Cohesion: 0.15
Nodes (21): argparse, block(), by_shop(), _date(), _int(), label(), _month_end(), _month_start() (+13 more)

### Community 96 - "custom_range.py"
Cohesion: 0.19
Nodes (14): block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each…, (from, to) dates for the page's Custom period, or None. Swapped if reversed;… (+6 more)

### Community 97 - "Shop Launch"
Cohesion: 0.20
Nodes (9): Config, Launch day, Marketing posts, Race lines, sales by day, product performance, folding (9 Nov 2026, user's call), Sales, Sales keyed in late (9 Nov 2026, user's call), Shop Launch, What the page shows (+1 more)

### Community 98 - "product_targets.py"
Cohesion: 0.06
Nodes (44): collections, csv, fetch_monthly_target(), fetch_sheet_data(), date, The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's…, week_window(), lib/colours.py — colour FAMILY of a product (Brown, Black, Red, Beige, Grey,… (+36 more)

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
Cohesion: 0.16
Nodes (17): _age_min(), _cleanup(), fresh_meta(), _meta(), _p(), query(), lib/snapshot.py — local DuckDB snapshot of the tills (docs/README.md › DuckDB…, The snapshot to read, refreshing it first when it's too old; None if there's… (+9 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "why_moved.py"
Cohesion: 0.09
Nodes (34): _load_shop_regions(), Shop → Region from docs/shop-regions.md (lib/shop_regions); the built-in…, doc(), day_for(), load(), lib/sales_date_fix.py — sales keyed in late, moved back to the day they…, [{"till", "shop", "from", "to", "asDate"}] — datetimes / dates parsed; [] if…, The day a till's sales of `day` count on (day granularity). (+26 more)

### Community 107 - "follower_test.py"
Cohesion: 0.27
Nodes (9): _best(), _link(), DataFrame, _rank(), lib/follower_test.py — does a new follower become a sale? Pins new follows,…, Best Spearman score of x[t] vs y[t+lag] over lags 0..max_lag → (score, lag)., One link in plain words for the slide., run() (+1 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "product_performance.py"
Cohesion: 0.19
Nodes (13): _d(), load_lines(), _market(), _month_end(), _month_start(), _num(), periods(), product_performance.py — the Product Performance page: % share of the top-… (+5 more)

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "_resolve_bag"
Cohesion: 0.25
Nodes (8): _monthly_bag_sales(), Resolve any bag wording → (canonical BOM bag type, cost or None, in_bom).…, {"months": ["Jun", …], "keys": ["2026-06", …], "bags": [{bag, category, stock,…, {BAG: {"days": [{d, name, was, now, units, today}], "offerDays", "offerUnits",…, _resolve_bag(), price_of(), _timed_offer_history(), canon()

### Community 112 - "Laya"
Cohesion: 0.27
Nodes (6): _bucket(), _clamp(), Laya, Probabilities over `options` for each state (one batch)., One loaded model. Use the module functions below (they share one instance)., softmax()

### Community 114 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

### Community 119 - "_bg_jobs"
Cohesion: 0.25
Nodes (8): cache_resource, fragment, _bg_done_msg(), _bg_jobs(), _bg_watch(), _fmt_secs(), Background rebuilds shared by every session: label → job (see _bg_rebuild)., The refresh_msg for a finished background rebuild (None: the job vanished).

### Community 120 - "Offers"
Cohesion: 0.32
Nodes (4): Offers, Kenya offers per day (each day reads its own month's bags_offer_source file) +…, {power, combo:[labels], dow:[{tier, shops}], timed:[{name, s, e, was, now}]}…, {mkt: {BAG: [text]}} for Sinza / Uganda from offers_monthly.csv.

### Community 121 - "names"
Cohesion: 0.20
Nodes (10): _new_products(), This month's new products: data/new_products.txt (lib/new_products_list) — the…, _growth_tracking(), data/growth_tracking.json + the report month: live (so far + projected + this…, load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, names() (+2 more)

### Community 122 - "fetch"
Cohesion: 0.08
Nodes (33): Out of stock — call back, _archived_source(), _as_date(), _build_period(), fetch(), cat_tier(), classify(), classify_for() (+25 more)

### Community 123 - "What the page shows"
Cohesion: 0.20
Nodes (10): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 2b. Shop breakdown (22 Oct 2026, user's call), 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Data, Popover waterfall — why the units moved (26 Oct 2026, user's call) (+2 more)

### Community 124 - "data"
Cohesion: 0.08
Nodes (24): corporate_clients_from_db(), corporate_from_db(), corporate_target_from_db(), _db_count(), monthly_from_db(), _months(), current_performance.py…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,… (+16 more)

### Community 125 - "forward_projections.py"
Cohesion: 0.17
Nodes (12): _bag_revenue(), fmt_opt_pct(), fmt_pct(), _orow(), _perfect_week_index(), forward_projections.py…, One table row, month-end projected. expected = what the targets expect from…, Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at… (+4 more)

### Community 126 - "Self-made combos vs running combos (doc)"
Cohesion: 0.25
Nodes (9): Bags not on offer per market (Kenya/Sinza/Uganda), Self-made combos vs running combos (doc), DoW mirror shops (DOW_MIRROR), Monetary implication panel (bundling discount), Rank chip (follows active Sort filter), Running-combo classification by bag composition (slot-aware sheet match), Standalone SQL (self_made_vs_running_combos.sql), Tier 1 vs Tier 2 Deal-of-the-Week gauge (+1 more)

### Community 127 - "Ralph task — "Out of stock — call back" demand per shop"
Cohesion: 0.25
Nodes (7): match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, Established facts (do not re-investigate), Every iteration, Periods (dates in Africa/Nairobi), Ralph task — "Out of stock — call back" demand per shop, Stopping

### Community 128 - "_reveal_page"
Cohesion: 0.50
Nodes (4): Run script-only HTML in an invisible frame (same origin, so it can reach…, Fade the page area back in on a page that has no dashboard frame (password…, _reveal_page(), _run_js()

### Community 129 - "run_scripts"
Cohesion: 0.36
Nodes (8): _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, _run_one(), run_scripts(), _handle_refresh(), _run_ref(), _timeout_for()

### Community 130 - "start_server"
Cohesion: 0.31
Nodes (8): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_to_config(), _json()

### Community 131 - "load_config"
Cohesion: 0.22
Nodes (9): Kenya timed-offer campaigns from timed_offers_config.json (normalised by…, _timed_offers(), _bags_from_file(), _derive_month(), load_config(), _norm_offer(), Multi-offer config: {"month": "YYYY-MM", "offers": [offer, ...]}. Back-compat:…, Bag list from a repo CSV's 'BAG TYPE' column — unique, order-preserving. Lets… (+1 more)

### Community 132 - "Marketing Dashboard — Google Sheets access & setup (doc)"
Cohesion: 0.29
Nodes (7): timed_offers_config.json (config), Vercel hosted version (static snapshot), Secrets excluded via .gitignore / .vercelignore, Marketing Dashboard — Google Sheets access & setup (doc), Timed Offers snapshot-over-window workflow, vercel.json, Vercel static deployment (serves committed HTML, no build step)

### Community 133 - "odoo_marketing.py"
Cohesion: 0.16
Nodes (17): _odoo_post_check(), followers_daily(), meta_posts_by_bag(), _q(), lib/odoo_marketing.py — marketing data the Odoo "Marketing OS" app keeps (spec:…, [{week (Monday), sessions, users, orders, revenue, carts, checkouts, abandoned,…, {week ISO: {"site": {orders, bags, kes}, "people": {…}}}., ({bag: {"posts", "reach", "views"}}, {"posts", "tagged"}) — Facebook +… (+9 more)

### Community 138 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.22
Nodes (7): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does, Current Performance (doc)

### Community 145 - "get_engine"
Cohesion: 0.29
Nodes (7): Engine, _env(), get_engine(), The process's reused connection (opened on first query). Every generator runs…, Build a SQLAlchemy URL from the environment, or None if unset. Accepts…, _shared_conn(), _url()

### Community 153 - "New Products Analytics (doc)"
Cohesion: 0.25
Nodes (7): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), Weekly Performance chart (Week 1 to latest), Net returns rule (qty <> 0, subtract refunds), Returns netting rule (qty <> 0), Python dependencies list (requirements.txt), Postgres source-of-truth migration (off Google Sheets, weekly first)

### Community 154 - "Slide 2: Did new followers sell bags? (Kenya)"
Cohesion: 0.29
Nodes (7): Follower test: does a new follower become a sale? (23 Nov 2026, user's call), Foot traffic band (22 Nov 2026, user's call), Kenya: insight and recommendation read the band with the chart (23 Nov 2026, user's call), Slide 2: Did new followers sell bags? (Kenya), Slide 2b: Followers vs sales, Sinza and Uganda (23 Nov 2026, user's call), What it found first (22 Nov 2026), WhatsApp buyers by source (23 Nov 2026, user's call)

### Community 155 - "Offer Picking (doc)"
Cohesion: 0.25
Nodes (9): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES) (+1 more)

### Community 156 - "re"
Cohesion: 0.06
Nodes (56): New Products slides (23 Nov 2026, user's call), functools, gender(), lib/bag_gender.py — who a bag is for (Male / Female / Unisex), from…, _table(), generator(), expand(), lib/pos_lines.py — till lines with refunded combos fixed (docs/README.md ›… (+48 more)

### Community 157 - "build"
Cohesion: 0.12
Nodes (16): Offer type summary (matrix), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, _read_offers(), _read_offers_cache(), _assign_price(), build(), _category_of() (+8 more)

### Community 158 - "google_auth.py (shared auth module)"
Cohesion: 0.25
Nodes (8): google_auth.py (shared auth module), google_credentials.json (OAuth desktop client), google_token.json (OAuth token), main.py (refresh + serve dashboard), OAuth token expiry issue (Testing mode, ~7 day expiry), reauth.py (re-login script), service_account.json (recommended, permanent auth), Service account chosen for zero-maintenance auth + enabling in-dashboard Refresh

### Community 159 - "scripts/receipt_combos.py"
Cohesion: 0.29
Nodes (6): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…, itertools

### Community 160 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 161 - "write_atomic"
Cohesion: 0.29
Nodes (7): inject(), _inject(), inject(), inject(), inject(), Write text to path so a reader never sees a half-written file: write a temp…, write_atomic()

### Community 162 - "bag_tracking.py"
Cohesion: 0.36
Nodes (8): build(), _cfg(), _colour(), _folder(), canon(), _moves(), generators/bag_tracking.py — Bag Tracking: the chosen bags' Kenya shop stock at…, Odoo product name → the dashboard's bag name (Offer Picking's _build_catalog…

### Community 163 - "_seasonality"
Cohesion: 0.29
Nodes (8): Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), _combo_odoo_slots(), _combo_sheet_slots(), Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]., Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…

### Community 165 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 166 - "Stock record accuracy (NEGATIVE FIX LOG) — progress"
Cohesion: 0.17
Nodes (11): _negfix(), Stock record accuracy per shop for every period (docs/shops-efficiency.md ›…, 1. Spec — DONE, 2. Library — DONE, 3. Script — DONE, 4. Generator and data — DONE, 5. Page section — DONE, 6. Visual check — DONE (+3 more)

### Community 167 - "Menu 1 Current Performance in the 3-beat layout (preview)"
Cohesion: 0.15
Nodes (12): 0. New: an executive summary strip at the top of the page, 1. Sales, Weekly Sales and Remaining Target cards, 2. Followers & Reach, 3. Weekly Performance — Week 1 to Latest, 4. Why Did We Move?, 5. Sales vs Monthly Target, Week-over-Week, Bare Minimum, 6. Forward Projections (Standard and Forecasted), 7. Price per Bag, and On offer vs not on offer (+4 more)

### Community 168 - "odoo_marketing_audit.py"
Cohesion: 0.39
Nodes (8): root(), audit(), _expected(), main(), _period(), _range(), scripts/odoo_marketing_audit.py — how complete and up to date each marketing…, _step()

### Community 169 - "Footfall and Marketing (21 Oct 2026, user's call)"
Cohesion: 0.20
Nodes (9): Actions (rules), Correlations ("Posts and ads vs visitors"), Data traps (said on the page), Definitions, Footfall and Marketing (21 Oct 2026, user's call), Regenerate, Shop mapping (`lib/footfall.SHOPS`), Sources (+1 more)

### Community 170 - "explain"
Cohesion: 0.40
Nodes (5): explain(), _fmt_d(), Start-of-week stock, units dispatched in, biggest delivery, days in stock for…, {lw, pw, lwNb, pwNb, head, lines:[[group, dir, text]]} for bag b in market mkt…, week_stock()

### Community 172 - "get_rows"
Cohesion: 0.25
Nodes (8): default_window(), get_rows(), last_complete_week(), date, The most recent COMPLETE Sun–Sat week before `ref` (today) — what the sheet's…, Sheet-shaped rows for `tab` built from Odoo, or None when Postgres is…, The tab's rows in the sheet's layout, built from Odoo. No sheet fallback (Oct…, tab_rows()

### Community 173 - "Product / name matching (doc)"
Cohesion: 0.33
Nodes (7): match_odoo_bags [S_0] internal-reference prefix fix, Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix), Normalisation rules (upper-case, strip ref prefix, exclude combos/non-sellable stock), Deal enrichment & name matching (_enrich_deals / _match)

### Community 174 - "Product Performance — Shop breakdown: progress"
Cohesion: 0.22
Nodes (8): 1. Spec — DONE, 2. Data — DONE, 3. Page section — DONE, 4. Sidebar and sticky bar — DONE, 5. Visual check — DONE, 6. Wrap-up — DONE, Product Performance — Shop breakdown: progress, Summary

### Community 175 - "family"
Cohesion: 0.40
Nodes (6): ({BAG: units}, {BAG: {colour: units}}) at CBD/Stock., warehouse_stock(), family(), _load(), _norm(), Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…

### Community 177 - "Sales-share targets per product"
Cohesion: 0.40
Nodes (4): Deliver, Sales-share targets per product, Steps, Tests

### Community 178 - "price"
Cohesion: 0.50
Nodes (4): Per bag × market: the facts (`push_rules.facts`, `add_peers`), Prices (30 Oct 2026, user's call), price(), Price per Bag card: the price gap, and the group that drags revenue most.

### Community 179 - "Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)"
Cohesion: 0.20
Nodes (9): 1. Spec — DONE, 2. SQL + library — DONE, 3. Generator — DONE, 4. Page — DONE, 5. Actions — DONE, 6. Visual check — DONE, 7. Wrap-up — DONE, Findings (16 weeks, 28 Jun – 17 Oct 2026; last fully counted week 11–17 Oct) (+1 more)

### Community 180 - "_read_bom_costs"
Cohesion: 0.50
Nodes (4): {BAG TYPE (upper): production cost} from bom_costs.json — the local copy of the…, _read_bom_costs(), _bom_costs(), {BAG (upper): cost} from bom_costs.json (via offer_picking._read_bom_costs).…

### Community 182 - "timed_offers.py (generator)"
Cohesion: 0.29
Nodes (7): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers.html (output), timed_offers.py (generator)

### Community 183 - "bags_on_offer.py"
Cohesion: 0.18
Nodes (15): _bag_tiers(), _base_windows(), _custom_range(), fmt(), inject(), main(), _price_tier(), bags_on_offer.py… (+7 more)

### Community 186 - "odoo_tabs.py"
Cohesion: 0.11
Nodes (30): _aliases(), base_name(), _build(), build_rows(), _Deriver, dispatch_by_product_shop(), _flag_cells(), _fmt() (+22 more)

### Community 187 - "Ralph loop brief — Footfall and Marketing page"
Cohesion: 0.25
Nodes (7): DATA FACTS (verified 21 Oct 2026), DONE, ESCAPE HATCH, PROJECT RULES (must hold every iteration), Ralph loop brief — Footfall and Marketing page, SELF-CORRECTION, SUB-GOALS (do in order; tick each in notes/footfall_progress.md with the command output that proved it)

### Community 189 - "oos_callbacks.py"
Cohesion: 0.06
Nodes (59): fixture, bag(), _add_oos(), _norm_combo(), A combo name compared loosely: lower case, letters / digits / '+' only., Out of stock — call back (WhatsApp Monitoring): distinct people who asked for…, col(), aggregate() (+51 more)

### Community 191 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 193 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 194 - "Bag Tracking"
Cohesion: 0.33
Nodes (5): Bag Tracking, Page, Prices, Stock, The bags

### Community 195 - "realistic_rates"
Cohesion: 0.53
Nodes (6): _clamp(), ({SHOP: {BAG: units a week}}, {SHOP: {"recent", "season", "growth"}}) — recent…, realistic_rates(), growth(), season(), tot()

### Community 197 - "offer_picking.py"
Cohesion: 0.18
Nodes (14): _build_catalog(), _is_full_price(), _next_month(), offer_picking.py…, Letters and digits only, so 'CODE3' meets 'CODE 3' and 'FANNYPACK(N)' meets…, {_staff_key(catalogue bag type): staff price} from staff_prices.json (a 0 = no…, {BAG (upper): official full price} from bag_original_prices.json (fallback)., Save a local, human-editable copy of the offers prices to OFFERS_CACHE. (+6 more)

### Community 198 - "compute_period"
Cohesion: 0.17
Nodes (7): compute_period(), compute_regions(), pct(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period., Aggregate every metric by region (using SHOP_REGION_MAP). Independent of the…, sum_by_shop()

### Community 200 - "shop_stock_levels.py"
Cohesion: 0.10
Nodes (36): bag_categories(), buffer_stock(), build(), dispatch_shop(), fit(), grand_total(), leads(), month_end_lift() (+28 more)

### Community 203 - "shops_dispatch.py"
Cohesion: 0.21
Nodes (15): build_period(), distributed_in(), main(), q(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only. (+7 more)

### Community 204 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 205 - "render"
Cohesion: 0.60
Nodes (5): growthData(), render(), drawGrowth(), table(), wf()

### Community 208 - "shop_breakdown"
Cohesion: 0.33
Nodes (6): corp(), corporate_period(), [(product, bags, kes)] — Corporate app bags paid in [s, e]…, {period: {market: {total, rev, shops: [...]}}} — units / revenue per shop…, shop_breakdown(), shop_name()

### Community 210 - "_odoo_colour"
Cohesion: 0.50
Nodes (4): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, ({PRODUCT: {SHOP CODE: units}}, {PRODUCT: {SHOP CODE: [[colour, units], …]}})…, shop_sales()

### Community 211 - "test_sheet_reads.py"
Cohesion: 0.47
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 216 - "load_posts"
Cohesion: 0.67
Nodes (4): load_posts(), num(), tally(), ({BAG: [kenya, outside]} last week, {BAG: [kenya, outside]} this month) from…

### Community 217 - "queries.py"
Cohesion: 0.16
Nodes (11): main(), month_window(), date, _query_ready(), monthly_sales.py — the current month's real bags sold, from Postgres. The…, First → last calendar day of the LIVE month (today's month; see…, master_products(), _norm_name() (+3 more)

### Community 218 - "load_catalog"
Cohesion: 0.50
Nodes (4): catalog_rows(), load_catalog(), [{colour, category, name, bag}] in sheet order, from product_catalog.csv., [header] + [[COLOUR, CATEGORY, PRODUCT NAME, BAG TYPE], …] — the label columns…

### Community 219 - "posts_between"
Cohesion: 0.67
Nodes (3): posts_between(), fn(), fn(start, end) → {BAG: {"KE", "TZ", "UG": posts}} from marketing's daily…

### Community 223 - "_month_archived"
Cohesion: 0.67
Nodes (3): _month_archived(), cache_data, True when `key` is in Supabase (falls back to monthly_report_history.json). If…

## Knowledge Gaps
- **266 isolated node(s):** `PERF`, `The rule`, `Steps`, `Preventing it`, `graphify` (+261 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1169 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_query()` connect `run_query` to `shop_corporate.py`, `lib/receipt_combos.py`, `odoo_marketing.py`, `month_extras.py`, `get_engine`, `shop_requests.py`, `timed_offers.py`, `re`, `stock.py`, `bag_tracking.py`, `_seasonality`, `db.py`, `build_payload`, `odoo_marketing_audit.py`, `shop_launch.py`, `weekly_report.py`, `shops_efficiency.py`, `footfall.py`, `oos_callbacks.py`, `fetch_new_products_data`, `_enrich_deals`, `new_products.py`, `_combo_button_usage`, `shop_stock_levels.py`, `fetch_posting_data`, `shop_breakdown`, `_odoo_colour`, `self_made_combos.py`, `foot_traffic.py`, `queries.py`, `product_targets.py`, `snapshot.py`, `why_moved.py`, `product_performance.py`, `_resolve_bag`, `fetch`, `data`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `Shops & Regions (doc — source of truth)` connect `Bags on offer vs not on offer` to `Denri Africa Dashboard Design System (skill)`, `Chart type switcher (every chart, every menu)`, `self_made_combos.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `Vercel hosted version (static snapshot)` connect `Marketing Dashboard — Google Sheets access & setup (doc)` to `main.py`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **What connects `PERF`, `The rule`, `Steps` to the rest of the system?**
  _266 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `shop_corporate.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14532019704433496 - nodes in this community are weakly interconnected._
- **Should `lib/receipt_combos.py` be split into smaller, more focused modules?**
  _Cohesion score 0.060641627543035995 - nodes in this community are weakly interconnected._
- **Should `oos_chip.js` be split into smaller, more focused modules?**
  _Cohesion score 0.08067375886524823 - nodes in this community are weakly interconnected._