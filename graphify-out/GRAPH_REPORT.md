# Graph Report - Marketing_dashboard  (2026-11-16)

## Corpus Check
- 251 files · ~1,292,032 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: .csv 14, (none) 2, .toml 1)

## Summary
- 2768 nodes · 5413 edges · 212 communities (162 shown, 50 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 197 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f7032399`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- shop_corporate.py
- add_laya
- tests/test_receipt_combos.py
- oos_chip.js
- chart_switcher.js
- graw(block, key) function (bare numeric getter)
- Kitengela Rejects tracker (timed offer)
- publish.py
- marketing_posts.py
- v5_theme.js
- name_match.py
- bare_minimum setting (weekly target floor)
- norm
- self_made_combos_bundle/lib/db.py
- self_made_combos_bundle/lib/report_month.py
- check_connection
- forward_projections.py
- weeks
- build_payload
- shops_efficiency.py
- sticky_controls.js
- shop_requests.py
- main.py
- Self-made combos vs running combos (doc)
- build
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
- anchor
- chronos_train.py
- odoo_stock_by_product
- build_payload
- Shops Efficiency Tracking spec doc
- _enrich_deals
- shop_launch.py
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
- month_extras.py
- test_oos_callbacks.py
- High-End Visual Design skill
- safe_int
- ads_panel.js
- fetch_new_products_data
- daydream skill (Vault Daydream)
- _fetch_sinza_monthly
- lib/db.py
- load_rows
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
- _bag_sales_daily_sql
- history.py
- _build_catalog
- test_push_planner.py
- test_share_targets.py
- test_stockout_demand.py
- README.md
- shop-birthdays.md
- bag_key_fn
- load_config
- self_made_combos_bundle/lib/__init__.py
- negative_fixes.py
- custom_range.py
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
- lib/offer_data.py
- Ralph task — only three sheet tabs left
- timed_offers.py
- Bag targets October 2026_3acbad00.md
- load_pages
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- _bags_not_on_offer
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- get_gspread_client
- fetch
- What the page shows
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- Product (bag) targets
- POST_DATA data block (Posting)
- followup
- read_block(file, start, end) function
- json
- last_week_from_db
- generate_insights.py
- contextlib
- Chart type switcher (every chart, every menu)
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- New Products Analytics (doc)
- Monthly Report (doc)
- Offer Picking (doc)
- start_server
- build
- timed_offers.py (generator)
- scripts/receipt_combos.py
- _dead_stock_region
- new_products.py
- fetch_offer_data
- generator
- Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)
- Ralph task — "Out of stock — call back" demand per shop
- update_np_weekly_history
- _alignment_region
- odoo_marketing_audit.py
- Footfall and Marketing (21 Oct 2026, user's call)
- num
- Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)
- get_rows
- google_auth.py (shared auth module)
- Product Performance — Shop breakdown: progress
- _resolve_bag
- Out-of-stock demand — people, not requests
- fetch
- Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)
- corporate_clients_from_db
- _category_of
- bags_on_offer.py
- _bg_jobs
- _bag_tiers
- posting_yields.py
- _read_offers
- Ralph loop brief — Footfall and Marketing page
- _read_bom_costs
- master_products
- Bag signals — quant finance applied to product sales
- ambiguous_python_import_17686b6faac5
- _kind
- Bag Tracking
- test_sheet_reads.py
- data
- _write_offers_cache
- _bag_sales_sql
- totals
- Combos from receipts — running vs self-made
- render
- excluded_products
- sendable_by_month_end
- Odoo marketing data audit
- ODOO_MARKETING_AUDIT.md
- test_product_targets.py

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 89 edges
2. `fetch()` - 41 edges
3. `data()` - 40 edges
4. `fetch_posting_data()` - 38 edges
5. `check_connection()` - 34 edges
6. `get_gspread_client()` - 31 edges
7. `build_payload()` - 30 edges
8. `excluded_products()` - 26 edges
9. `build()` - 25 edges
10. `build_offer()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `Sales pace to month end (19 Oct 2026)` --references--> `month_end_lift()`  [INFERRED]
  docs/shop-stock-levels.md → generators/shop_stock_levels.py
- `Buckets` --references--> `bag_classifier()`  [INFERRED]
  docs/bags-on-offer.md → generators/self_made_combos.py
- `The split — by each bag's share of recent sales` --references--> `bag_classifier()`  [INFERRED]
  docs/product-targets.md → generators/self_made_combos.py
- `Inputs (read only — nothing is written to Odoo or the sheet)` --references--> `bag_classifier()`  [INFERRED]
  docs/push-planner.md → generators/self_made_combos.py
- `Laya's second opinion (`lib/push_laya.py`)` --references--> `state_text()`  [INFERRED]
  docs/push-planner.md → lib/push_laya.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Self-made combos bundle: generator, Sheets auth, DB access, and dependency manifest working together to build the combos page** — export_self_made_combos_bundle_self_made_combos_py, export_self_made_combos_bundle_offer_data_py, export_self_made_combos_bundle_google_auth_py, export_self_made_combos_bundle_lib_db_py, export_self_made_combos_bundle_requirements [EXTRACTED 0.90]
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]

## Communities (212 total, 50 thin omitted)

### Community 0 - "shop_corporate.py"
Cohesion: 0.15
Nodes (25): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), _acronym(), build(), _maybe(), owns(), corporate_team_receipts(), _d() (+17 more)

### Community 1 - "add_laya"
Cohesion: 0.07
Nodes (25): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket() (+17 more)

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

### Community 8 - "marketing_posts.py"
Cohesion: 0.16
Nodes (21): _bag_category(), _category(), daily(), _date(), is_bag_level(), _load_backup(), _num(), parse() (+13 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 12 - "norm"
Cohesion: 0.09
Nodes (27): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, ({PRODUCT: {SHOP CODE: units}}, {PRODUCT: {SHOP CODE: [[colour, units], …]}})…, shop_sales(), apply_walkins(), _aliases(), base_name(), build_rows() (+19 more)

### Community 13 - "self_made_combos_bundle/lib/db.py"
Cohesion: 0.16
Nodes (17): check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, Run a read query and return a DataFrame, or None if the DB is unreachable.… (+9 more)

### Community 14 - "self_made_combos_bundle/lib/report_month.py"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 15 - "check_connection"
Cohesion: 0.18
Nodes (14): odoo_daily_kenya(), odoo_list_price(), odoo_offer_price(), {date_iso: bags} — daily Kenya bags for the offer bags across [start,end], used…, {BAG_UP: incl-tax Sales Price} — the product's normal price ("was"), the…, {BAG_UP: incl-tax offer price} — the offer's "now" price, the dominant fixed…, _cache_path(), check_connection() (+6 more)

### Community 16 - "forward_projections.py"
Cohesion: 0.13
Nodes (9): bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, fmt_opt_pct(), fmt_pct(), _orow(), forward_projections.py…, One table row, month-end projected. expected = what the targets expect from…, _row(), lib/odoo_marketing.py — marketing data the Odoo "Marketing OS" app keeps (spec:… (+1 more)

### Community 17 - "weeks"
Cohesion: 0.11
Nodes (18): Actions ("what we can do"), Ads impact — on every page (21 Oct 2026, user's call), Charts (21 Oct 2026, user's call), Figures, Refresh, What each page shows, new_bags(), Bags launched inside the base period (the bag-targets CSV's Launch column). (+10 more)

### Community 18 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 19 - "shops_efficiency.py"
Cohesion: 0.14
Nodes (13): fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py…, Read the Shop → Region table from docs/shop-regions.md so the mapping can be…, metric_byshop(), parse_sheet() (+5 more)

### Community 20 - "sticky_controls.js"
Cohesion: 0.20
Nodes (15): bind(), embedHost(), headerOf(), init(), initSections(), injectCss(), place(), setPinned() (+7 more)

### Community 21 - "shop_requests.py"
Cohesion: 0.14
Nodes (21): _onoff(), Shop requests vs received (this month · last month) and the production approved…, requests_block(), _d(), _f(), _match(), _offer_label(), _offers() (+13 more)

### Community 22 - "main.py"
Cohesion: 0.12
Nodes (20): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, Denri Africa — Marketing Dashboard Launcher… (+12 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.18
Nodes (13): Bags not on offer per market (Kenya/Sinza/Uganda), Combo button usage / rung vs pot. (till check), Self-made combos vs running combos (doc), DoW mirror shops (DOW_MIRROR), Monetary implication panel (bundling discount), Rank chip (follows active Sort filter), Running-combo classification by bag composition (slot-aware sheet match), Standalone SQL (self_made_vs_running_combos.sql) (+5 more)

### Community 24 - "build"
Cohesion: 0.08
Nodes (38): build(), _clamp(), dispatch_shop(), fit(), grand_total(), leads(), month_end_lift(), needs() (+30 more)

### Community 25 - "build"
Cohesion: 0.14
Nodes (28): build(), acts(), campaign_table(), money(), chart_data(), ser(), cpr(), focus_tiles() (+20 more)

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
Cohesion: 0.07
Nodes (33): Counted by how it was sold, _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…, _add_noffer_posts(), per_bag(), _add_oos() (+25 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.08
Nodes (17): cache_data, SCRIPT_TIMEOUT = 600s config, html, streamlit, _load_secrets_into_env(), _month_archived(), _month_end_running(), streamlit_app.py — Denri Marketing Dashboard on Streamlit. Serves the existing… (+9 more)

### Community 33 - "product_performance.py"
Cohesion: 0.06
Nodes (47): build(), corp(), categories(), corporate_period(), _d(), explain(), _fmt_d(), _load_json() (+39 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.12
Nodes (15): _bag_stock(), _cause(), _combo_bags(), esc(), fmt(), ladder_strip(), _norm_bag(), pct() (+7 more)

### Community 35 - "anchor"
Cohesion: 0.19
Nodes (14): count_complete_weeks_in_month(), Count Mon–Sun weeks in the reporting month that have ≥5 days falling within it., anchor(), live_anchor(), month_key(), month_name(), month_window(), _pinned() (+6 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.13
Nodes (26): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+18 more)

### Community 37 - "odoo_stock_by_product"
Cohesion: 0.09
Nodes (27): build(), _cfg(), _colour(), _folder(), canon(), _moves(), Odoo product name → the dashboard's bag name (Offer Picking's _build_catalog…, odoo_stock_kenya_outside() (+19 more)

### Community 38 - "build_payload"
Cohesion: 0.05
Nodes (43): _self_made_combos(), Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), build_payload(), _anchor_sunday(), _combo_bags() (+35 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "_enrich_deals"
Cohesion: 0.07
Nodes (26): _as_day(), dow_tier_weeks(), _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg() (+18 more)

### Community 41 - "shop_launch.py"
Cohesion: 0.15
Nodes (20): build(), _add(), launch_curve(), _cfg(), _day_expr(), first_sale(), load_categories(), load_prices() (+12 more)

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
Cohesion: 0.19
Nodes (11): get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, build(), complete_weeks_remaining(), data_rows_count(), fmt_int(), is_checked(), offer_data.py ─────────────────────────────────────────────────────────────────… (+3 more)

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
Cohesion: 0.16
Nodes (16): _new_products(), This month's new products: data/new_products.txt (lib/new_products_list) — the…, names(), Upper-cased bag types from new_products.txt in file order ([] = no new…, build(), {TYPE: {"kes", "shops": {SHOP: {"n", "kes"}}}} for the runway types over…, The NP.runway payload: {days, bags: [{name, created, category, stockKe,…, Product name → bag type (see the module docstring). (+8 more)

### Community 52 - "compute_period"
Cohesion: 0.12
Nodes (11): apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _metric(), pct(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period. (+3 more)

### Community 53 - "Bags on offer vs not on offer"
Cohesion: 0.18
Nodes (11): Bags on offer vs not on offer, Buckets, Corporate-lead till orders, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Regenerate, Shop birthdays (+3 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.17
Nodes (12): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+4 more)

### Community 56 - "scripts/test_receipt_combos.py"
Cohesion: 0.32
Nodes (15): classify(), lines: [{receipt, d, product, qty, amount}] → per-market summary: {running:…, infer(), L(), Tests for receipt_combos.py + name_match.py — python -m pytest scripts -q, test_alternatives_and_singles(), test_bulk_receipts_are_not_combos(), test_four_bags_at_two_prices_are_two_combos() (+7 more)

### Community 57 - "month_extras.py"
Cohesion: 0.18
Nodes (20): _bags_on_offer(), _block(), build_extras(), cp_more_month(), _deals(), _month_dates(), _pick(), _posting() (+12 more)

### Community 58 - "test_oos_callbacks.py"
Cohesion: 0.16
Nodes (21): aggregate(), flat(), split(), {shop: set(person)} → (distinct people, [[shop, people], …] high → low)., The page block: {period: {key: {"total": people, "shops": [[shop, people],…, _shops(), pytest, _base_sql() (+13 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "safe_int"
Cohesion: 0.16
Nodes (22): _bag_level_bags(), _build_no_convert(), _fetch_monthly_kenya(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int() (+14 more)

### Community 61 - "ads_panel.js"
Cohesion: 0.22
Nodes (16): act(), axes(), cell(), charts(), drawCmp(), drawWow(), values(), esc() (+8 more)

### Community 62 - "fetch_new_products_data"
Cohesion: 0.15
Nodes (18): fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_combo_product_bags() (+10 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "_fetch_sinza_monthly"
Cohesion: 0.18
Nodes (14): _analyze_region(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), MONTHLY_SALES: colour=A(0), product_name=B(1), MONTHLY_MARKETING_POST: colour=A(0), product_name=C(2), STOCK_LEVELS: colour=A(0), product_name=C(2) (+6 more)

### Community 65 - "lib/db.py"
Cohesion: 0.10
Nodes (25): hashlib, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, lib/footfall.py — footfall (visitors counted per shop per day) joined to walk-…, lib/laya.py — Laya, the on-device decision model, for the dashboard (spec:…, lib/pos_lines.py — till lines with refunded combos fixed (docs/README.md ›…, _age_min(), _cleanup(), fresh_meta() (+17 more)

### Community 66 - "load_rows"
Cohesion: 0.14
Nodes (17): Out of stock — call back, fixture, _date(), load_rows(), _online_rows(), oos_by_bag_shop(), {period: {product name: {shop: people}}} straight from Odoo names, or {} if…, Odoo translatable names can come back as {'en_US': …}. (+9 more)

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.11
Nodes (18): Bag health (by bag, 18 Oct 2026), Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026), Page, Product rating and core 5 vs other 13 categories (18 Oct 2026) (+10 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "live_month_window"
Cohesion: 0.14
Nodes (16): load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if…, _till_to_shop(), build(), load_targets(), (total units, info) — the month's Odoo target units, or (no Odoo targets yet)… (+8 more)

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
Cohesion: 0.10
Nodes (29): _kenya_target(), month_progress(), payload(), Kenya's month target from current_performance.html (PERF.totalTarget), or None., Per market: sold this month so far (from the daily sales), days elapsed / left,…, _slim(), by_shop(), _entry() (+21 more)

### Community 76 - "main"
Cohesion: 0.25
Nodes (8): build_facts(), build_reasons(), inject(), main(), Facts for every bag × market that has stock or sold in the window…, Adds notMoving + reasons to every row (lib/push_rules.reasons). Returns the…, not_moving(), A bag with stock that isn't clearing: cleared < 30% this month, or > 45 days of…

### Community 77 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.08
Nodes (29): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards) (+21 more)

### Community 78 - "shops_dispatch.py"
Cohesion: 0.23
Nodes (14): build_period(), distributed_in(), main(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only., Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).… (+6 more)

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
Cohesion: 0.08
Nodes (16): current_performance.py…, weekly_sales.py — the weekly-sales fix. Computes the CURRENT Sun–Sat week's…, Shared Google Sheets authentication for every dashboard generator. Two modes,…, openpyxl, openpyxl_comments, openpyxl_styles, openpyxl_utils, os (+8 more)

### Community 83 - "facts"
Cohesion: 0.21
Nodes (12): _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, day(), ISO date n days before END (0 = END)., test_days_cover_is_none_when_nothing_sold(), test_first_sold_days_ago(), test_momentum_up_down_and_from_zero() (+4 more)

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
Cohesion: 0.22
Nodes (7): Shop birthdays, Shop → opening date, Where it shows, Per-shop combo-button chips (red when < half best-in-region), self_made_combos.py, Shops & Regions (doc — source of truth), Shop -> Region table

### Community 92 - "bag_key_fn"
Cohesion: 0.08
Nodes (30): build(), _posts(), MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), _odoo_post_check(), bag_posts(), tally() (+22 more)

### Community 93 - "load_config"
Cohesion: 0.40
Nodes (5): Kenya timed-offer campaigns from timed_offers_config.json (normalised by…, _timed_offers(), _derive_month(), load_config(), Multi-offer config: {"month": "YYYY-MM", "offers": [offer, ...]}. Back-compat:…

### Community 94 - "self_made_combos_bundle/lib/__init__.py"
Cohesion: 0.08
Nodes (35): calendar, collections, csv, datetime, lib — shared data-access for the marketing dashboard (Postgres migration).…, generators/bag_tracking.py — Bag Tracking: the chosen bags' Kenya shop stock at…, footfall_marketing.py — Footfall and Marketing page (spec: docs/footfall-…, monthly_sales.py — the current month's real bags sold, from Postgres. The… (+27 more)

### Community 95 - "negative_fixes.py"
Cohesion: 0.08
Nodes (34): argparse, _negfix(), Stock record accuracy per shop for every period (docs/shops-efficiency.md ›…, bags_sold(), block(), by_shop(), _date(), _int() (+26 more)

### Community 96 - "custom_range.py"
Cohesion: 0.19
Nodes (14): block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each…, (from, to) dates for the page's Custom period, or None. Swapped if reversed;… (+6 more)

### Community 97 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

### Community 98 - "run_query"
Cohesion: 0.07
Nodes (29): corporate_from_db(), corporate_target_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, This month's Odoo corporate target {bags, kes} (sales_pos_target, scope…, _bag_revenue(), _bag_revenue_range(), _corporate_bags(), _corporate_lines() (+21 more)

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
Cohesion: 0.28
Nodes (9): _alt_cost(), build(), _combo_cost(), _combo_slots(), Parse `const SMC = {…}` out of self_made_combos.html (no DB round-trip)., One combo alternative (e.g. 'Amaya Handbag') → its BOM production cost., Combo name → list of slots, each a list of alternative strings., Production cost = Σ over slots of the average matched-alternative cost. Same-… (+1 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "build"
Cohesion: 0.08
Nodes (33): why_moved(), _load_shop_regions(), Shop → Region from docs/shop-regions.md (lib/shop_regions); the built-in…, doc(), day_for(), load(), [{"till", "shop", "from", "to", "asDate"}] — datetimes / dates parsed; [] if…, The day a till's sales of `day` count on (day granularity). (+25 more)

### Community 107 - "lib/offer_data.py"
Cohesion: 0.20
Nodes (12): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), offer_data.py ─────────────────────────────────────────────────────────────────… (+4 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "timed_offers.py"
Cohesion: 0.06
Nodes (49): _acc(), _bags_from_file(), _bucket(), build_compare(), build_offer(), _cmp_lines(), _days(), _kenya_net_moves_since() (+41 more)

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "load_pages"
Cohesion: 0.14
Nodes (13): read_block(), _growth_tracking(), data/growth_tracking.json + the report month: live (so far + projected + this…, _offer_bagtypes_by_region(), On-offer bag types per region, read from self_made_combos.html's SMC block:…, load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.… (+5 more)

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 114 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 121 - "get_gspread_client"
Cohesion: 0.17
Nodes (12): kenya_posts(), load_workplan(), _parse_workplan(), (opening stock, source) — the live sheet, else the saved CSV., ({BAG: posts this month}, {BAG: posts last week}) from col D / col E (Kenya),…, [[bag, colour, qty], …] → {BAG: {COLOUR: qty}} (TOTAL and blank rows skipped,…, get_gspread_client(), offer_flags() (+4 more)

### Community 122 - "fetch"
Cohesion: 0.10
Nodes (27): _archived_source(), _as_date(), _build_period(), fetch(), cat_tier(), classify(), classify_for(), combo_slots() (+19 more)

### Community 123 - "What the page shows"
Cohesion: 0.18
Nodes (11): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 2b. Shop breakdown (22 Oct 2026, user's call), 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Bulk orders, Data (+3 more)

### Community 126 - "Product (bag) targets"
Cohesion: 0.25
Nodes (8): A month with only a revenue target (November 2026), Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 128 - "followup"
Cohesion: 0.18
Nodes (13): Did last week's calls work? (`push_rules.record_week`, `followup`), Last week's calls checked against what happened (lib/push_rules.followup), then…, weekly(), followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., Store this week's top actions under its Sunday. Re-running in the same week…, The most recent PREVIOUS week's calls and what happened since: sold/day since…, record_week() (+5 more)

### Community 130 - "json"
Cohesion: 0.24
Nodes (9): One-off: restore August's Offer Type figures into monthly_report_history.json…, json, clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.…, YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that…, After the closing month's timed offers are safely in Supabase, empty the config…, run() (+1 more)

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
Cohesion: 0.16
Nodes (14): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix) (+6 more)

### Community 154 - "Monthly Report (doc)"
Cohesion: 0.22
Nodes (9): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+1 more)

### Community 155 - "Offer Picking (doc)"
Cohesion: 0.29
Nodes (8): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES)

### Community 156 - "start_server"
Cohesion: 0.31
Nodes (9): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_refresh(), _handle_to_config() (+1 more)

### Community 157 - "build"
Cohesion: 0.22
Nodes (8): _assign_price(), build(), reject_stock.csv → {BAG (upper): {units, colours:{COLOUR: units}}}., (price, flag) from BOM cost — two tiers. flag ∈ {'', 'thin', 'below', 'nobom'}., Write an Excel (xlsx, or CSV fallback) of EVERYTHING on the pricing board —…, _read_overrides(), _read_stock(), _write_export()

### Community 158 - "timed_offers.py (generator)"
Cohesion: 0.14
Nodes (14): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+6 more)

### Community 159 - "scripts/receipt_combos.py"
Cohesion: 0.33
Nodes (5): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…

### Community 160 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 161 - "new_products.py"
Cohesion: 0.18
Nodes (7): _base_colour(), _merge_rows_by_base_colour(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across…, _strip_colour_qualifiers()

### Community 162 - "fetch_offer_data"
Cohesion: 0.42
Nodes (8): fetch_offer_data(), cell(), find_row(), find_row_any(), process_table(), section_name_col(), section_raw(), section_title()

### Community 163 - "generator"
Cohesion: 0.18
Nodes (12): generator(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, start_daily_snapshot(), _bg_rebuild(), work(), Seconds the last good `kind` rebuild of `lbl` took (any kind as a fallback),… (+4 more)

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

### Community 172 - "get_rows"
Cohesion: 0.10
Nodes (20): fetch_monthly_target(), fetch_sheet_data(), load(), main(), date, _query_ready(), The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's…, week_window() (+12 more)

### Community 173 - "google_auth.py (shared auth module)"
Cohesion: 0.25
Nodes (8): google_auth.py (shared auth module), google_credentials.json (OAuth desktop client), google_token.json (OAuth token), main.py (refresh + serve dashboard), OAuth token expiry issue (Testing mode, ~7 day expiry), reauth.py (re-login script), service_account.json (recommended, permanent auth), Service account chosen for zero-maintenance auth + enabling in-dashboard Refresh

### Community 174 - "Product Performance — Shop breakdown: progress"
Cohesion: 0.22
Nodes (8): 1. Spec — DONE, 2. Data — DONE, 3. Page section — DONE, 4. Sidebar and sticky bar — DONE, 5. Visual check — DONE, 6. Wrap-up — DONE, Product Performance — Shop breakdown: progress, Summary

### Community 175 - "_resolve_bag"
Cohesion: 0.25
Nodes (8): _monthly_bag_sales(), _next_month(), bag(), Resolve any bag wording → (canonical BOM bag type, cost or None, in_bom).…, Reference-month combos matched to current Odoo stock, laid out like the offers…, {"months": ["Jun", …], "keys": ["2026-06", …], "bags": [{bag, category, stock,…, _resolve_bag(), price_of()

### Community 177 - "Out-of-stock demand — people, not requests"
Cohesion: 0.29
Nodes (7): Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods, Show it as, Tests

### Community 178 - "fetch"
Cohesion: 0.29
Nodes (5): fetch(), Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), _read_offer_analysis()

### Community 179 - "Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)"
Cohesion: 0.20
Nodes (9): 1. Spec — DONE, 2. SQL + library — DONE, 3. Generator — DONE, 4. Page — DONE, 5. Actions — DONE, 6. Visual check — DONE, 7. Wrap-up — DONE, Findings (16 weeks, 28 Jun – 17 Oct 2026; last fully counted week 11–17 Oct) (+1 more)

### Community 180 - "corporate_clients_from_db"
Cohesion: 0.40
Nodes (6): corporate_clients_from_db(), _months(), A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],…, Current month's corporate activity per client (quoted · invoiced · paid · sold)…, _txt()

### Community 181 - "_category_of"
Cohesion: 0.40
Nodes (5): _apply_alias(), Apply bag aliases, longest key first (so 'STANDARD TRAVEL' wins over…, _category_of(), _norm_cat(), Category for a bag: the offers-sheet category (col C), else a keyword fallback.

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
Cohesion: 0.24
Nodes (9): _mkt_perfect_week_index(), _mkt_week_label(), posting_yields.py…, Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]., current = {region: {key: {productName,colour,category,bagType,stock}}}. A new…, update_clearance(), update_mkt_history() (+1 more)

### Community 186 - "_read_offers"
Cohesion: 0.40
Nodes (5): Offer type summary (matrix), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, _read_offers(), _read_offers_cache()

### Community 187 - "Ralph loop brief — Footfall and Marketing page"
Cohesion: 0.25
Nodes (7): DATA FACTS (verified 21 Oct 2026), DONE, ESCAPE HATCH, PROJECT RULES (must hold every iteration), Ralph loop brief — Footfall and Marketing page, SELF-CORRECTION, SUB-GOALS (do in order; tick each in notes/footfall_progress.md with the command output that proved it)

### Community 188 - "_read_bom_costs"
Cohesion: 0.50
Nodes (4): {BAG TYPE (upper): production cost} from bom_costs.json — the local copy of the…, _read_bom_costs(), _bom_costs(), {BAG (upper): cost} from bom_costs.json (via offer_picking._read_bom_costs).…

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
Cohesion: 0.12
Nodes (19): _db_count(), monthly_from_db(), Reporting month's subset count (e.g. rejectBags, giftBags) from…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,…, _live_bags(), {BAG (upper): official full price} from bag_original_prices.json (fallback)., _read_bag_prices(), _categories() (+11 more)

### Community 204 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 205 - "render"
Cohesion: 0.60
Nodes (5): growthData(), render(), drawGrowth(), table(), wf()

### Community 210 - "excluded_products"
Cohesion: 0.13
Nodes (15): odoo_weekly_breakdown(), _perfect_week_index(), Average POS bags per weekday (0 = Mon) over s..e (bags_sold_daily.sql). None if…, Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, update_weekly_history(), _week_start(), _weekday_base() (+7 more)

### Community 211 - "sendable_by_month_end"
Cohesion: 0.50
Nodes (4): {shop: units} — `left` units shared over {shop: gap} in proportion, leftovers…, What can still be sent (docs › Shop requests — realistic performance): per shop…, sendable_by_month_end(), _share_out()

### Community 218 - "test_product_targets.py"
Cohesion: 0.16
Nodes (15): allocate(), available_days(), base_period(), The three complete months before month_start → (start, end)., Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, _add_months(), _d() (+7 more)

## Knowledge Gaps
- **262 isolated node(s):** `Log`, `1. Spec — DONE`, `2. Library — DONE`, `3. Script — DONE`, `5. Page section — DONE` (+257 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1141 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **50 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_query()` connect `run_query` to `shop_corporate.py`, `tests/test_receipt_combos.py`, `last_week_from_db`, `norm`, `check_connection`, `build_payload`, `shop_requests.py`, `build`, `build`, `_combo_button_usage`, `_enrich_deals`, `bag_classifier`, `product_performance.py`, `chronos_train.py`, `odoo_stock_by_product`, `build_payload`, `_enrich_deals`, `shop_launch.py`, `odoo_marketing_audit.py`, `get_rows`, `_resolve_bag`, `type_fn`, `corporate_clients_from_db`, `month_extras.py`, `test_oos_callbacks.py`, `fetch_new_products_data`, `lib/db.py`, `live_month_window`, `fetch_posting_data`, `build`, `excluded_products`, `test_product_targets.py`, `bag_key_fn`, `negative_fixes.py`, `build`, `_bags_not_on_offer`, `fetch`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `Bags on offer vs not on offer` connect `Bags on offer vs not on offer` to `tests/test_receipt_combos.py`, `load_rows`, `_read_offers`, `shop-birthdays.md`, `bag_classifier`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `Shops & Regions (doc — source of truth)` connect `shop-birthdays.md` to `Chart type switcher (every chart, every menu)`, `Denri Africa Dashboard Design System (skill)`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **What connects `Log`, `1. Spec — DONE`, `2. Library — DONE` to the rest of the system?**
  _262 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `shop_corporate.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14532019704433496 - nodes in this community are weakly interconnected._
- **Should `add_laya` be split into smaller, more focused modules?**
  _Cohesion score 0.07386363636363637 - nodes in this community are weakly interconnected._
- **Should `tests/test_receipt_combos.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05641025641025641 - nodes in this community are weakly interconnected._