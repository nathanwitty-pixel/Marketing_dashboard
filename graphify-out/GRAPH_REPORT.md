# Graph Report - Marketing_dashboard  (2026-11-01)

## Corpus Check
- 240 files · ~1,184,684 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: .csv 14, (none) 2, .toml 1)

## Summary
- 2701 nodes · 5256 edges · 208 communities (164 shown, 44 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 192 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `659cfee7`
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
- last_week_from_db
- v5_theme.js
- name_match.py
- bare_minimum setting (weekly target floor)
- lib/offer_data.py
- odoo_marketing.py
- fetch_posting_data
- check_connection
- forward_projections.py
- test_oos_callbacks.py
- build_payload
- current_performance.py
- sticky_controls.js
- Offers
- self_made_combos_bundle/lib/report_month.py
- Self-made combos vs running combos (doc)
- shop_stock_levels.py
- build
- signals
- Dashboard Menu Docs (spec index)
- new_products.py
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
- shop_launch.py
- push_rules.py
- page_sidebar.js
- fetch
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
- live_month_window
- bag_classifier
- High-End Visual Design skill
- shops_dispatch.py
- generators/self_made_combos.py
- build
- daydream skill (Vault Daydream)
- oos_callbacks.py
- lib/db.py
- signals
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- build
- get_rows
- marketing_dashboard.sql
- weekly_kenya_posts
- publish.py
- shop_birthdays.py
- push_planner.py
- Denri Africa Dashboard Design System (skill)
- data
- why_moved.js
- theme.py
- push_laya.py
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- test_push_planner.py
- self_made_combos_bundle/lib/db.py
- moves
- Monthly Report (doc)
- F
- _is_checked
- test_stockout_demand.py
- Out-of-stock demand — people, not requests
- shop-birthdays.md
- attach_stock
- _build_period
- marketing_posts.py
- negative_fixes.py
- custom_range.py
- ads_impact.py
- build
- Bag Signals — quant view of each bag (posting · stock · selling)
- Month-End Routine
- current_performance.html
- attach
- self_made_combos.py generator (build_payload + SQL + injection)
- _enrich_deals
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- why_moved.py
- _mkt_week_label
- Ralph task — only three sheet tabs left
- build
- Bag targets October 2026_3acbad00.md
- os
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- footfall.py
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- _bg_jobs
- fetch
- What the page shows
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- Product (bag) targets
- POST_DATA data block (Posting)
- odoo_marketing_audit.py
- read_block(file, start, end) function
- _fetch_monthly_kenya
- product_performance.py
- num
- contextlib
- Chart type switcher (every chart, every menu)
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- New Products Analytics (doc)
- monthly_target_rows
- Offer Picking (doc)
- start_server
- json
- timed_offers.py (generator)
- scripts/receipt_combos.py
- Ralph task — "Out of stock — call back" demand per shop
- main
- generate_insights.py
- _dead_stock_region
- Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)
- followup
- test_product_targets.py
- update_np_weekly_history
- _alignment_region
- Footfall and Marketing (21 Oct 2026, user's call)
- html
- Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)
- reject_variants
- test_sheet_reads.py
- Product Performance — Shop breakdown: progress
- safe_int
- generator
- corporate_clients_from_db
- Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)
- shops_efficiency.py
- shop_breakdown
- _analyze_region
- timed_offers.py
- ads.py
- sys
- explain
- Ralph loop brief — Footfall and Marketing page
- _bag_stock
- _bag_tiers
- Bag signals — quant finance applied to product sales
- ambiguous_python_import_17686b6faac5
- main.py
- _collect_comments
- load_posts
- load_catalog
- run_query
- master_products
- _month_archived
- _garr_line
- Combos from receipts — running vs self-made
- Sales-share targets per product
- Odoo marketing data audit
- ODOO_MARKETING_AUDIT.md

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 86 edges
2. `fetch()` - 41 edges
3. `fetch_posting_data()` - 38 edges
4. `data()` - 36 edges
5. `check_connection()` - 34 edges
6. `get_gspread_client()` - 32 edges
7. `build_payload()` - 30 edges
8. `build()` - 25 edges
9. `excluded_products()` - 25 edges
10. `build_payload()` - 24 edges

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

## Communities (208 total, 44 thin omitted)

### Community 0 - "shop_corporate.py"
Cohesion: 0.07
Nodes (52): _new_products(), This month's new products: data/new_products.txt (lib/new_products_list) — the…, Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, _bags_on_offer() (+44 more)

### Community 1 - "laya.py"
Cohesion: 0.09
Nodes (26): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket() (+18 more)

### Community 2 - "lib/receipt_combos.py"
Cohesion: 0.07
Nodes (50): What the page shows (per period), _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region…, _region_goal() (+42 more)

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

### Community 8 - "last_week_from_db"
Cohesion: 0.25
Nodes (8): last_week_from_db(), Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary(), week_start_of(), weekly_from_db()

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 12 - "lib/offer_data.py"
Cohesion: 0.16
Nodes (14): Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer…, _read_offer_analysis(), build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked() (+6 more)

### Community 13 - "odoo_marketing.py"
Cohesion: 0.16
Nodes (17): _odoo_post_check(), followers_daily(), meta_posts_by_bag(), _q(), lib/odoo_marketing.py — marketing data the Odoo "Marketing OS" app keeps (spec:…, {week ISO: {"site": {orders, bags, kes}, "people": {…}}}., ({bag: {"posts", "reach", "views"}}, {"posts", "tagged"}) — Facebook +…, Shopify title → bag key, via the dashboard's bag key: the longest run of words… (+9 more)

### Community 14 - "fetch_posting_data"
Cohesion: 0.12
Nodes (15): _bt_on_offer(), _dead_clear(), fetch_posting_data(), _clear(), _yield(), _fold_bag_level(), load_dead_thresholds(), _post_yield() (+7 more)

### Community 15 - "check_connection"
Cohesion: 0.10
Nodes (21): build_offer(), _name_sql(), odoo_bag_daily_value(), odoo_bag_prices(), odoo_bulk_lines(), odoo_daily_kenya(), odoo_list_price(), odoo_offer_price() (+13 more)

### Community 16 - "forward_projections.py"
Cohesion: 0.10
Nodes (22): _bag_revenue(), _bag_revenue_range(), fmt_opt_pct(), fmt_pct(), _live_bags(), odoo_weekly_breakdown(), _orow(), _perfect_week_index() (+14 more)

### Community 17 - "test_oos_callbacks.py"
Cohesion: 0.19
Nodes (19): aggregate(), flat(), split(), The page block: {period: {key: {"total": people, "shops": [[shop, people],…, pytest, _base_sql(), _kai(), Tests for lib/oos_callbacks.py (WhatsApp "Out of stock — call back" demand).… (+11 more)

### Community 18 - "build_payload"
Cohesion: 0.06
Nodes (38): _bags_not_on_offer(), _infer(), _norm(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups() (+30 more)

### Community 19 - "current_performance.py"
Cohesion: 0.08
Nodes (15): fetch_monthly_target(), current_performance.py…, main(), date, _query_ready(), weekly_sales.py — the weekly-sales fix. Computes the CURRENT Sun–Sat week's…, The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's…, week_window() (+7 more)

### Community 20 - "sticky_controls.js"
Cohesion: 0.20
Nodes (15): bind(), embedHost(), headerOf(), init(), initSections(), injectCss(), place(), setPinned() (+7 more)

### Community 21 - "Offers"
Cohesion: 0.21
Nodes (7): _load_json(), Offers, Kenya offers per day (each day reads its own month's bags_offer_source file) +…, {power, combo:[labels], dow:[{tier, shops}], timed:[{name, s, e, was, now}]}…, {mkt: {BAG: [text]}} for Sinza / Uganda from offers_monthly.csv., _offers(), Offers lookup (Kenya) — or None when the offer data can't be loaded.

### Community 22 - "self_made_combos_bundle/lib/report_month.py"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.18
Nodes (13): Bags not on offer per market (Kenya/Sinza/Uganda), Combo button usage / rung vs pot. (till check), Self-made combos vs running combos (doc), DoW mirror shops (DOW_MIRROR), Monetary implication panel (bundling discount), Rank chip (follows active Sort filter), Running-combo classification by bag composition (slot-aware sheet match), Standalone SQL (self_made_vs_running_combos.sql) (+5 more)

### Community 24 - "shop_stock_levels.py"
Cohesion: 0.05
Nodes (67): What each page shows, _onoff(), bag_categories(), buffer_stock(), build(), _clamp(), dispatch_shop(), fit() (+59 more)

### Community 25 - "build"
Cohesion: 0.28
Nodes (16): build(), acts(), campaign_table(), money(), chart_data(), cpr(), focus_tiles(), market_table() (+8 more)

### Community 26 - "signals"
Cohesion: 0.09
Nodes (29): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+21 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.18
Nodes (14): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes) (+6 more)

### Community 28 - "new_products.py"
Cohesion: 0.18
Nodes (7): _base_colour(), _merge_rows_by_base_colour(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across…, _strip_colour_qualifiers()

### Community 29 - "_enrich_deals"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "fetch_new_products_data"
Cohesion: 0.24
Nodes (12): fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_sales_window() (+4 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.08
Nodes (20): SCRIPT_TIMEOUT = 600s config, fragment, hashlib, html, streamlit, _bg_done_msg(), _bg_watch(), _fmt_secs() (+12 more)

### Community 33 - "odoo_tabs.py"
Cohesion: 0.12
Nodes (26): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, _aliases(), base_name(), build_rows(), _Deriver, dispatch_by_product_shop(), _flag_cells() (+18 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.16
Nodes (8): _cause(), esc(), fmt(), ladder_strip(), pct(), monthly_report.py…, _smc_srow(), _stock_rows()

### Community 35 - "anchor"
Cohesion: 0.11
Nodes (22): _db_count(), monthly_from_db(), Reporting month's subset count (e.g. rejectBags, giftBags) from…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,…, count_complete_weeks_in_month(), Count Mon–Sun weeks in the reporting month that have ≥5 days falling within it., anchor(), is_pinned() (+14 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.13
Nodes (27): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+19 more)

### Community 37 - "stock.py"
Cohesion: 0.13
Nodes (22): odoo_stock_kenya_outside(), ({UPPER name: kenya on-hand}, {UPPER name: outside on-hand}) — live Odoo stock.…, load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if…, _till_to_shop(), odoo_stock_levels() (+14 more)

### Community 38 - "build_payload"
Cohesion: 0.05
Nodes (41): _self_made_combos(), Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), build_payload(), _anchor_sunday(), _combo_bags() (+33 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "ads_panel.js"
Cohesion: 0.22
Nodes (16): act(), axes(), cell(), charts(), drawCmp(), drawWow(), values(), esc() (+8 more)

### Community 41 - "shop_launch.py"
Cohesion: 0.14
Nodes (20): build(), _add(), _cfg(), first_sale(), kenya_posts(), load_prices(), load_workplan(), make_matcher() (+12 more)

### Community 42 - "push_rules.py"
Cohesion: 0.10
Nodes (21): action(), _cover_txt(), _kind(), _n(), not_moving(), posting_median(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).…, {market: median postsMonth of the bags that were posted at all} — the 'below… (+13 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "fetch"
Cohesion: 0.14
Nodes (15): Counted by how it was sold, _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…, _bags_not_on_offer(), fetch(), fmt() (+7 more)

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

### Community 57 - "live_month_window"
Cohesion: 0.22
Nodes (11): build(), load_targets(), (total units, info) — the month's Odoo target units, or (no Odoo targets yet)…, (rows, total, base start, base end) for the month, from Odoo., {BAG: target units} for the month from product_targets_<YYYY-MM>.csv (built…, {BAG: col C} from MONTHLY_TARGET — for the comparison column only., _sheet_targets(), total_for() (+3 more)

### Community 58 - "bag_classifier"
Cohesion: 0.17
Nodes (15): Buckets, _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _norm_combo() (+7 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "shops_dispatch.py"
Cohesion: 0.21
Nodes (15): build_period(), distributed_in(), main(), q(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only. (+7 more)

### Community 61 - "generators/self_made_combos.py"
Cohesion: 0.11
Nodes (18): fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py…, Read the Shop → Region table from docs/shop-regions.md so the mapping can be…, _bag_sales_daily_sql(), _bag_sales_sql() (+10 more)

### Community 62 - "build"
Cohesion: 0.05
Nodes (44): Offer type summary (matrix), _alt_cost(), _apply_alias(), build(), _build_catalog(), _combo_cost(), _combo_slots(), _is_full_price() (+36 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "oos_callbacks.py"
Cohesion: 0.16
Nodes (17): _date(), load_rows(), _online_rows(), oos_by_bag_shop(), lib/oos_callbacks.py — "Out of stock — call back" demand, ONLINE and WALK-IN.…, {shop: set(person)} → (distinct people, [[shop, people], …] high → low)., {period: {key: people}} from an aggregate() block., {period: {product name: {shop: people}}} straight from Odoo names, or {} if… (+9 more)

### Community 65 - "lib/db.py"
Cohesion: 0.11
Nodes (23): _env(), lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, Build a SQLAlchemy URL from the environment, or None if unset. Accepts…, _url(), lib/pos_lines.py — till lines with refunded combos fixed (docs/README.md ›…, _age_min(), _cleanup(), fresh_meta() (+15 more)

### Community 66 - "signals"
Cohesion: 0.17
Nodes (16): action(), _mean(), _phi(), posting_beta(), The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json…, _sd() (+8 more)

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.11
Nodes (18): Bag health (by bag, 18 Oct 2026), Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026), Page, Product rating and core 5 vs other 13 categories (18 Oct 2026) (+10 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "build"
Cohesion: 0.18
Nodes (11): actions(), build(), agg(), week_tot(), num(), pearson(), footfall_marketing.py — Footfall and Marketing page (spec: docs/footfall-…, What we can do' — by rule (docs/footfall-marketing.md › Actions). Each names a… (+3 more)

### Community 71 - "get_rows"
Cohesion: 0.14
Nodes (15): load(), _build(), default_window(), get_rows(), last_complete_week(), offer_flags(), _ok(), date (+7 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "weekly_kenya_posts"
Cohesion: 0.17
Nodes (12): Kenya timed-offer campaigns from timed_offers_config.json (normalised by…, _timed_offers(), _bags_from_file(), _derive_month(), load_config(), _norm_offer(), Multi-offer config: {"month": "YYYY-MM", "offers": [offer, ...]}. Back-compat:…, Bag list from a repo CSV's 'BAG TYPE' column — unique, order-preserving. Lets… (+4 more)

### Community 74 - "publish.py"
Cohesion: 0.12
Nodes (25): fnmatch, action_js(), main(), node_check(), Run the sticky-controls checks on every wired page and print the markdown…, edge_dump(), embedded(), inline_local() (+17 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "push_planner.py"
Cohesion: 0.13
Nodes (22): build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), main(), month_progress() (+14 more)

### Community 77 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.08
Nodes (29): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards) (+21 more)

### Community 78 - "data"
Cohesion: 0.22
Nodes (10): {BAG (upper): official full price} from bag_original_prices.json (fallback)., _read_bag_prices(), _load_combos_by_shop(), _from_file(), _nonempty(), load_dispatch(), Per-shop combo / power-deal view for the panel — built **live from Odoo** via…, {BAG_UPPER: units} — physical stock summed per BAG TYPE from a repo CSV's UNITS… (+2 more)

### Community 79 - "why_moved.js"
Cohesion: 0.36
Nodes (12): bestWeek(), bestWeeks(), build(), fillWeeks(), getW(), hasKey(), mark(), onClick() (+4 more)

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

### Community 84 - "self_made_combos_bundle/lib/db.py"
Cohesion: 0.15
Nodes (18): check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, Run a read query and return a DataFrame, or None if the DB is unreachable.… (+10 more)

### Community 85 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 86 - "Monthly Report (doc)"
Cohesion: 0.22
Nodes (9): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+1 more)

### Community 87 - "F"
Cohesion: 0.24
Nodes (16): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), A facts row with sensible defaults, overridden by kw., test_fallback_slow_seller_or_overstocked() (+8 more)

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
Cohesion: 0.22
Nodes (7): Shop birthdays, Shop → opening date, Where it shows, Per-shop combo-button chips (red when < half best-in-region), self_made_combos.py, Shops & Regions (doc — source of truth), Shop -> Region table

### Community 92 - "attach_stock"
Cohesion: 0.21
Nodes (12): attach_stock(), in_stock(), stk(), collect(), _in(), is_combo_request(), {period: (start, end)} for the dated periods (lifetime / current are undated).…, True when the request names a whole combo ("Amaya Handbag or Elyse Handbag +… (+4 more)

### Community 93 - "_build_period"
Cohesion: 0.18
Nodes (6): _build_period(), _offer_types(), _pick_target(), Latest target row for `shop` with this period that overlaps [start, end]. A…, Matrix payload: rows, per-row category / tier cells, and the period's Top-5…, _region_of()

### Community 94 - "marketing_posts.py"
Cohesion: 0.22
Nodes (16): _bag_category(), _category(), daily(), _date(), _num(), parse(), posts(), lib/marketing_posts.py — marketing POSTS per bag, from marketing's own daily… (+8 more)

### Community 95 - "negative_fixes.py"
Cohesion: 0.08
Nodes (35): argparse, _negfix(), Stock record accuracy per shop for every period (docs/shops-efficiency.md ›…, bags_sold(), block(), by_shop(), _date(), _int() (+27 more)

### Community 96 - "custom_range.py"
Cohesion: 0.19
Nodes (14): block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each…, (from, to) dates for the page's Custom period, or None. Swapped if reversed;… (+6 more)

### Community 97 - "ads_impact.py"
Cohesion: 0.15
Nodes (11): corporate_return(), market_sales(), posts_by_market(), posts_lead_sales(), ads_impact.py — the Ads impact panel shown on every page (spec: docs/ads-…, {market: {bags, kes, orders}} over [start, end]., {market: [posts per week]} from marketing's posting sheets; None if they can't…, Kenya bag types: change in posts one week vs change in bags sold the next,… (+3 more)

### Community 98 - "build"
Cohesion: 0.18
Nodes (10): build(), categories(), posts_between(), fn(), {BAG: category} — the bag type's usual catalogue category, else its Odoo…, fn(start, end) → {BAG: {"KE", "TZ", "UG": posts}} from marketing's daily…, (start, end) → {bag: {"clicks", …}} website WhatsApp taps, one Odoo pull per…, shade() (+2 more)

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "Month-End Routine"
Cohesion: 0.20
Nodes (9): Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand, The newer pages in History (`extras`), What it does (+1 more)

### Community 101 - "current_performance.html"
Cohesion: 0.50
Nodes (4): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance)

### Community 102 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 103 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.29
Nodes (7): lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, lib/report_month.py (which month are we reporting?), self_made_combos.html static page (reads const SMC), self_made_combos.py generator (build_payload + SQL + injection)

### Community 104 - "_enrich_deals"
Cohesion: 0.07
Nodes (26): _as_day(), dow_tier_weeks(), _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg() (+18 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "why_moved.py"
Cohesion: 0.11
Nodes (29): _load_shop_regions(), Shop → Region from docs/shop-regions.md (lib/shop_regions); the built-in…, doc(), load(), {SHOP (upper): region} parsed from the markdown table under the heading that…, build(), build_month(), _corporate() (+21 more)

### Community 107 - "_mkt_week_label"
Cohesion: 0.29
Nodes (7): _mkt_perfect_week_index(), _mkt_week_label(), Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]., current = {region: {key: {productName,colour,category,bagType,stock}}}. A new…, update_clearance(), update_mkt_history()

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "build"
Cohesion: 0.22
Nodes (9): build(), _posts(), MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), bag_posts(), tally(), {BAG: (posts this month, posts last week)} — Kenya posts (col E) from the two… (+1 more)

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "os"
Cohesion: 0.10
Nodes (28): calendar, collections, csv, datetime, lib — shared data-access for the marketing dashboard (Postgres migration).…, bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, monthly_sales.py — the current month's real bags sold, from Postgres. The…, offer_picking.py… (+20 more)

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 114 - "footfall.py"
Cohesion: 0.27
Nodes (11): daily(), DataFrame, date, lib/footfall.py — footfall (visitors counted per shop per day) joined to walk-…, The Sunday that starts d's Sun–Sat week., One row per footfall shop per day: visitors (NaN = not counted), walk-in orders…, One row per shop per Sun–Sat week. Conversion and revenue use COUNTED days…, Paid-ad WhatsApp leads per WhatsApp shop per Sun–Sat week: chats, bought,… (+3 more)

### Community 121 - "_bg_jobs"
Cohesion: 0.25
Nodes (9): cache_resource, _bg_jobs(), _bg_rebuild(), work(), Seconds the last good `kind` rebuild of `lbl` took (any kind as a fallback),…, Background rebuilds shared by every session: label → job (see _bg_rebuild)., Rebuild `lbl` in the background. kind: "auto" (skipped if a rebuild was tried…, _rebuild_secs() (+1 more)

### Community 122 - "fetch"
Cohesion: 0.13
Nodes (24): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), combo_slots(), make_classifier() (+16 more)

### Community 123 - "What the page shows"
Cohesion: 0.18
Nodes (11): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 2b. Shop breakdown (22 Oct 2026, user's call), 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Bulk orders, Data (+3 more)

### Community 126 - "Product (bag) targets"
Cohesion: 0.25
Nodes (8): A month with only a revenue target (November 2026), Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 128 - "odoo_marketing_audit.py"
Cohesion: 0.39
Nodes (8): root(), audit(), _expected(), main(), _period(), _range(), scripts/odoo_marketing_audit.py — how complete and up to date each marketing…, _step()

### Community 130 - "_fetch_monthly_kenya"
Cohesion: 0.23
Nodes (12): _fetch_monthly_kenya(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), Monthly Kenya figures for the S1 KPI cards. MONTHLY_MARKETING_POST: sum col E…, MONTHLY_SALES: colour=A(0), product_name=B(1), MONTHLY_MARKETING_POST: colour=A(0), product_name=C(2) (+4 more)

### Community 131 - "product_performance.py"
Cohesion: 0.19
Nodes (13): _d(), load_lines(), _market(), _month_end(), _month_start(), _num(), periods(), product_performance.py — the Product Performance page: % share of the top-… (+5 more)

### Community 132 - "num"
Cohesion: 0.29
Nodes (8): gnum(), num(), _parse_offers(), _units(), This month's timed-offer campaigns, flattened for storage. The live TO payload…, Parse an offer table (Kenya combos/deals, Sinza, Uganda) → [{name, units,…, Numeric field reader that handles BOTH quoted ("1,211") and bare (7, 89.7)…, _timed_offer_snapshots()

### Community 138 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.22
Nodes (7): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does, Current Performance (doc)

### Community 145 - "Shop Launch"
Cohesion: 0.22
Nodes (8): Config, Launch day, Marketing posts, Prices (30 Oct 2026, user's call), Sales, Shop Launch, What the page shows, Where the stock is (30 Oct 2026, user's call)

### Community 153 - "New Products Analytics (doc)"
Cohesion: 0.16
Nodes (14): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix) (+6 more)

### Community 154 - "monthly_target_rows"
Cohesion: 0.33
Nodes (4): fetch_sheet_data(), monthly_target_rows(), MONTHLY_TARGET rows with column C = the bag's target from Odoo (docs/product-…, test_monthly_target_rows_swaps_column_c()

### Community 155 - "Offer Picking (doc)"
Cohesion: 0.29
Nodes (8): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES)

### Community 156 - "start_server"
Cohesion: 0.31
Nodes (9): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_refresh(), _handle_to_config() (+1 more)

### Community 157 - "json"
Cohesion: 0.24
Nodes (8): One-off: restore August's Offer Type figures into monthly_report_history.json…, json, clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.…, YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that…, After the closing month's timed offers are safely in Supabase, empty the config…, target_month()

### Community 158 - "timed_offers.py (generator)"
Cohesion: 0.09
Nodes (22): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+14 more)

### Community 159 - "scripts/receipt_combos.py"
Cohesion: 0.29
Nodes (6): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…, itertools

### Community 160 - "Ralph task — "Out of stock — call back" demand per shop"
Cohesion: 0.25
Nodes (7): match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, Established facts (do not re-investigate), Every iteration, Periods (dates in Africa/Nairobi), Ralph task — "Out of stock — call back" demand per shop, Stopping

### Community 161 - "main"
Cohesion: 0.33
Nodes (5): main(), month_window(), date, _query_ready(), First → last calendar day of the LIVE month (today's month; see…

### Community 162 - "generate_insights.py"
Cohesion: 0.24
Nodes (5): card(), esc(), fmt(), generate_insights.py…, region_card()

### Community 163 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 165 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 166 - "test_product_targets.py"
Cohesion: 0.16
Nodes (15): allocate(), available_days(), base_period(), The three complete months before month_start → (start, end)., Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, _add_months(), _d() (+7 more)

### Community 167 - "update_np_weekly_history"
Cohesion: 0.29
Nodes (7): _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)., Ordinal among the month's perfect weeks (>=5 days in month), so the first FULL…, Snapshot each Sun–Sat week (sales, Kenya/Outside posts) into…, update_np_weekly_history()

### Community 168 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 169 - "Footfall and Marketing (21 Oct 2026, user's call)"
Cohesion: 0.20
Nodes (9): Actions (rules), Correlations ("Posts and ads vs visitors"), Data traps (said on the page), Definitions, Footfall and Marketing (21 Oct 2026, user's call), Regenerate, Shop mapping (`lib/footfall.SHOPS`), Sources (+1 more)

### Community 170 - "html"
Cohesion: 0.29
Nodes (6): read_block(), read_block(), _read_timed_offers(), _offer_bagtypes_by_region(), On-offer bag types per region, read from self_made_combos.html's SMC block:…, html()

### Community 172 - "reject_variants"
Cohesion: 0.33
Nodes (7): _parse_colour(), First primary colour token found in a name (longest-first), Title-cased; '' if…, Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share…, Per-[REJECT]-product variant rows for a name-filtered offer, for the filterable…, reject_variants(), _match_bag(), _singular_tokens()

### Community 173 - "test_sheet_reads.py"
Cohesion: 0.47
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 174 - "Product Performance — Shop breakdown: progress"
Cohesion: 0.22
Nodes (8): 1. Spec — DONE, 2. Data — DONE, 3. Page section — DONE, 4. Sidebar and sticky bar — DONE, 5. Visual check — DONE, 6. Wrap-up — DONE, Product Performance — Shop breakdown: progress, Summary

### Community 175 - "safe_int"
Cohesion: 0.40
Nodes (5): _bag_level_bags(), Bag types with posts logged without a colour in any of the posting tabs., safe_int(), is_bag_level(), A tab_rows() row of posts with no colour (from the bag type's TOTAL row):…

### Community 177 - "generator"
Cohesion: 0.29
Nodes (7): generator(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, start_daily_snapshot(), run(), run_scripts()

### Community 178 - "corporate_clients_from_db"
Cohesion: 0.40
Nodes (6): corporate_clients_from_db(), _months(), A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],…, Current month's corporate activity per client (quoted · invoiced · paid · sold)…, _txt()

### Community 179 - "Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)"
Cohesion: 0.20
Nodes (9): 1. Spec — DONE, 2. SQL + library — DONE, 3. Generator — DONE, 4. Page — DONE, 5. Actions — DONE, 6. Visual check — DONE, 7. Wrap-up — DONE, Findings (16 weeks, 28 Jun – 17 Oct 2026; last fully counted week 11–17 Oct) (+1 more)

### Community 180 - "shops_efficiency.py"
Cohesion: 0.20
Nodes (8): apply_walkins(), metric_byshop(), parse_sheet(), shops_efficiency.py…, Return (data, meta) for the Kenya shops, locating columns by header name…, safe_int(), update_history(), sql()

### Community 181 - "shop_breakdown"
Cohesion: 0.33
Nodes (6): corp(), corporate_period(), [(product, bags, kes)] — Corporate app bags paid in [s, e]…, {period: {market: {total, rev, shops: [...]}}} — units / revenue per shop…, shop_breakdown(), shop_name()

### Community 182 - "_analyze_region"
Cohesion: 0.50
Nodes (4): _analyze_region(), STOCK_LEVELS: colour=A(0), product_name=C(2), Runs all three posting sections for one region. sales_col – column index in…, _sl_key()

### Community 183 - "timed_offers.py"
Cohesion: 0.16
Nodes (17): _acc(), _bucket(), build_compare(), _cmp_lines(), _days(), _kenya_net_moves_since(), kenya_stock_by_bag(), _offer_compare() (+9 more)

### Community 184 - "ads.py"
Cohesion: 0.13
Nodes (17): Actions ("what we can do"), Ads impact — on every page (21 Oct 2026, user's call), Charts (21 Oct 2026, user's call), Figures, Refresh, ser(), campaigns(), _f() (+9 more)

### Community 185 - "sys"
Cohesion: 0.11
Nodes (23): dotenv, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers… (+15 more)

### Community 186 - "explain"
Cohesion: 0.40
Nodes (5): explain(), _fmt_d(), Start-of-week stock, units dispatched in, biggest delivery, days in stock for…, {lw, pw, lwNb, pwNb, head, lines:[[group, dir, text]]} for bag b in market mkt…, week_stock()

### Community 187 - "Ralph loop brief — Footfall and Marketing page"
Cohesion: 0.25
Nodes (7): DATA FACTS (verified 21 Oct 2026), DONE, ESCAPE HATCH, PROJECT RULES (must hold every iteration), Ralph loop brief — Footfall and Marketing page, SELF-CORRECTION, SUB-GOALS (do in order; tick each in notes/footfall_progress.md with the command output that proved it)

### Community 188 - "_bag_stock"
Cohesion: 0.40
Nodes (5): _bag_stock(), _combo_bags(), _norm_bag(), Space/punctuation-insensitive key so 'MINIZURI' matches 'MINI ZURI'., Component bags of an offer, each with its stock, sorted most-stock first.

### Community 189 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

### Community 191 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 193 - "main.py"
Cohesion: 0.12
Nodes (20): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, Denri Africa — Marketing Dashboard Launcher… (+12 more)

### Community 194 - "_collect_comments"
Cohesion: 0.50
Nodes (3): _collect_comments(), _html_text(), The comments

### Community 195 - "load_posts"
Cohesion: 0.67
Nodes (4): load_posts(), num(), tally(), ({BAG: [kenya, outside]} last week, {BAG: [kenya, outside]} this month) from…

### Community 197 - "load_catalog"
Cohesion: 0.50
Nodes (4): catalog_rows(), load_catalog(), [{colour, category, name, bag}] in sheet order, from product_catalog.csv., [header] + [[COLOUR, CATEGORY, PRODUCT NAME, BAG TYPE], …] — the label columns…

### Community 198 - "run_query"
Cohesion: 0.07
Nodes (33): corporate_from_db(), corporate_target_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, This month's Odoo corporate target {bags, kes} (sales_pos_target, scope…, _corporate_bags(), _corporate_lines(), The month's revenue target (KES): Odoo sales_pos_target amount (pos +…, (corporate bags, corporate KES received) in the given month, live from Odoo… (+25 more)

### Community 199 - "master_products"
Cohesion: 0.50
Nodes (4): master_products(), _norm_name(), Match the SQL normalisation: lower-case, '.'→space, collapse whitespace., Normalised, de-duplicated master catalogue names (master_products.txt), for the…

### Community 200 - "_month_archived"
Cohesion: 0.67
Nodes (3): cache_data, _month_archived(), True when `key` is in Supabase (falls back to monthly_report_history.json). If…

### Community 202 - "_garr_line"
Cohesion: 0.67
Nodes (3): _garr_line(), _offers(), Greedy single-line array extractor — handles nested [[...],[...]] arrays.

### Community 204 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 205 - "Sales-share targets per product"
Cohesion: 0.40
Nodes (4): Deliver, Sales-share targets per product, Steps, Tests

## Knowledge Gaps
- **255 isolated node(s):** `Log`, `Blocker counter`, `Final summary`, `Log`, `Sheets cut to three tabs (RALPH_SHEETS.md) — 2026-10-04` (+250 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1114 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `run_query()` connect `run_query` to `shop_corporate.py`, `odoo_marketing_audit.py`, `lib/receipt_combos.py`, `product_performance.py`, `type_fn`, `last_week_from_db`, `odoo_marketing.py`, `fetch_posting_data`, `forward_projections.py`, `test_oos_callbacks.py`, `build_payload`, `current_performance.py`, `shop_stock_levels.py`, `_enrich_deals`, `fetch_new_products_data`, `main`, `chronos_train.py`, `stock.py`, `build_payload`, `test_product_targets.py`, `shop_launch.py`, `fetch`, `corporate_clients_from_db`, `shops_efficiency.py`, `shop_breakdown`, `live_month_window`, `lib/db.py`, `negative_fixes.py`, `ads_impact.py`, `_enrich_deals`, `why_moved.py`, `footfall.py`, `fetch`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `Bags on offer vs not on offer` connect `Bags on offer vs not on offer` to `lib/receipt_combos.py`, `fetch`, `bag_classifier`, `shop-birthdays.md`, `build`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `bag_classifier()` connect `bag_classifier` to `lib/receipt_combos.py`, `stock.py`, `build_payload`, `fetch`, `push_planner.py`, `Push Planner (`push_planner.py` → `push_planner.html`, `PP`)`, `Bags on offer vs not on offer`, `fetch`, `generators/self_made_combos.py`, `Product (bag) targets`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **What connects `Log`, `Blocker counter`, `Final summary` to the rest of the system?**
  _255 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `shop_corporate.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06578947368421052 - nodes in this community are weakly interconnected._
- **Should `laya.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._
- **Should `lib/receipt_combos.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06545879602571596 - nodes in this community are weakly interconnected._