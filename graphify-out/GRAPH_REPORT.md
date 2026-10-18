# Graph Report - Marketing_dashboard  (2026-10-18)

## Corpus Check
- 200 files · ~907,246 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: .csv 10, (none) 2, .toml 1)

## Summary
- 2286 nodes · 4419 edges · 174 communities (137 shown, 37 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 160 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a94ec007`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- current_performance.py
- laya.py
- lib/receipt_combos.py
- oos_chip.js
- chart_switcher.js
- graw(block, key) function (bare numeric getter)
- Kitengela Rejects tracker (timed offer)
- _load_shop_regions
- name_match.py
- v5_theme.js
- scripts/test_receipt_combos.py
- bare_minimum setting (weekly target floor)
- signals
- _reveal_page
- month_extras.py
- type_fn
- publish.py
- data
- build_payload
- shop_launch.py
- shop_corporate.py
- Bags on offer vs not on offer
- bags_on_offer.py
- Self-made combos vs running combos (doc)
- shop_stock_levels.py
- signals
- shops_dispatch.py
- Dashboard Menu Docs (spec index)
- followup
- _enrich_deals
- fetch
- insights.html
- streamlit_app.py
- moves
- monthly_report.py
- _combo_norm_option
- chronos_train.py
- stock.py
- build_payload
- Shops Efficiency Tracking spec doc
- Product (bag) targets
- push_rules.py
- datetime
- page_sidebar.js
- run_query
- Combos & Power Deals by Shop panel (#combo-shop)
- self_made_combos_bundle/offer_data.py
- Self-made combos bundle Python dependencies (requirements.txt)
- CLAUDE.md
- history.py (read months back)
- Self-made combos vs Running combos portable bundle README
- start_server
- norm
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- algorithmic-art skill
- dataviz-charts skill
- generators/self_made_combos.py
- compute_period
- _enrich_deals
- High-End Visual Design skill
- lib/db.py
- _combo_button_usage
- oos_callbacks.py
- daydream skill (Vault Daydream)
- main.py
- OOS call-back progress (Ralph loop log)
- timed_offers.py (generator)
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- live_month_window
- self_made_combos_bundle/lib/report_month.py
- marketing_dashboard.sql
- product_performance.py
- Month-End Routine
- shop_birthdays.py
- lib/offer_data.py
- check_connection
- push_planner.py
- self_made_combos_bundle/lib/__init__.py
- theme.py
- push_laya.py
- new_products.py
- test_push_planner.py
- paths.py
- lib/report_month.py
- Chart type switcher (every chart, every menu)
- F
- fetch_new_products_data
- test_stockout_demand.py
- Out-of-stock demand — people, not requests
- Denri Africa Dashboard Design System (skill)
- num
- shop_requests.py
- fetch_posting_data
- corporate_clients_from_db
- offer_picking.py
- month_end.py
- _combo_button_usage
- Bag Signals — quant view of each bag (posting · stock · selling)
- timed_offers.py
- current_performance.html
- attach
- self_made_combos.py generator (build_payload + SQL + injection)
- posting_yields.py
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- update_np_weekly_history
- os
- Ralph task — only three sheet tabs left
- fetch
- Bag targets October 2026_3acbad00.md
- odoo_tabs.py
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- reject_variants
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- load_pages
- base_name
- What the page shows
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- Monthly Report (doc)
- POST_DATA data block (Posting)
- odoo_weekly_breakdown
- read_block(file, start, end) function
- New Products Analytics (doc)
- Offer Picking (doc)
- ambiguous_python_import_17686b6faac5
- contextlib
- odoo_month_product_bags
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- monthly_target_rows
- Product / name matching (doc)
- kenya_stock_by_bag
- custom_range.py
- generator
- family
- product_targets_workbook.py
- scripts/receipt_combos.py
- _bag_stock
- generate_insights.py
- _bags_not_on_offer
- Bag signals — quant finance applied to product sales
- _match
- _build_sheet_slots
- Combos from receipts — running vs self-made
- Sales-share targets per product
- _odoo_stock_for
- lib
- _bg_jobs
- offer_flags
- _month_archived

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 62 edges
2. `fetch()` - 39 edges
3. `fetch_posting_data()` - 38 edges
4. `get_gspread_client()` - 31 edges
5. `build_payload()` - 30 edges
6. `check_connection()` - 28 edges
7. `data()` - 28 edges
8. `build_payload()` - 24 edges
9. `fetch_new_products_data()` - 22 edges
10. `build_offer()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `The split — by each bag's share of recent sales` --references--> `bag_classifier()`  [INFERRED]
  docs/product-targets.md → generators/self_made_combos.py
- `Inputs (read only — nothing is written to Odoo or the sheet)` --references--> `bag_classifier()`  [INFERRED]
  docs/push-planner.md → generators/self_made_combos.py
- `Laya's second opinion (`lib/push_laya.py`)` --references--> `state_text()`  [INFERRED]
  docs/push-planner.md → lib/push_laya.py
- `Why it isn't moving — reasons, per market (`push_rules.reasons`)` --references--> `reasons()`  [INFERRED]
  docs/push-planner.md → lib/push_rules.py
- `What the page shows (per period)` --references--> `_market_records()`  [INFERRED]
  docs/bags-on-offer.md → generators/bags_on_offer.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Self-made combos bundle: generator, Sheets auth, DB access, and dependency manifest working together to build the combos page** — export_self_made_combos_bundle_self_made_combos_py, export_self_made_combos_bundle_offer_data_py, export_self_made_combos_bundle_google_auth_py, export_self_made_combos_bundle_lib_db_py, export_self_made_combos_bundle_requirements [EXTRACTED 0.90]
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]

## Communities (174 total, 37 thin omitted)

### Community 0 - "current_performance.py"
Cohesion: 0.14
Nodes (9): last_week_from_db(), current_performance.py…, Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary(), week_start_of() (+1 more)

### Community 1 - "laya.py"
Cohesion: 0.06
Nodes (44): check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, Run a read query and return a DataFrame, or None if the DB is unreachable.… (+36 more)

### Community 2 - "lib/receipt_combos.py"
Cohesion: 0.09
Nodes (41): lib — shared data-access for the marketing dashboard (Postgres migration).…, bag_key(), classify(), _fits(), _groups(), load_offers(), market_lines(), market_summary() (+33 more)

### Community 3 - "oos_chip.js"
Cohesion: 0.08
Nodes (38): attach(), close(), esc(), form(), go(), iso(), mountPanel(), open() (+30 more)

### Community 4 - "chart_switcher.js"
Cohesion: 0.12
Nodes (35): alpha(), apply(), attach(), axisOpts(), build(), changeTxt(), Chart(), clone() (+27 more)

### Community 6 - "Kitengela Rejects tracker (timed offer)"
Cohesion: 0.07
Nodes (28): bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source), Offline fallback pattern (mirror sheet data to local JSON), Reject Sale (doc: reject_sales.py -> reject_sales.html, RJ), reject_sales_export.csv (fallback export) (+20 more)

### Community 7 - "_load_shop_regions"
Cohesion: 0.67
Nodes (3): _load_shop_regions(), Read the Shop → Region table from docs/shop-regions.md so the mapping can be…, doc()

### Community 8 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "scripts/test_receipt_combos.py"
Cohesion: 0.32
Nodes (15): classify(), lines: [{receipt, d, product, qty, amount}] → per-market summary: {running:…, infer(), L(), Tests for receipt_combos.py + name_match.py — python -m pytest scripts -q, test_alternatives_and_singles(), test_bulk_receipts_are_not_combos(), test_four_bags_at_two_prices_are_two_combos() (+7 more)

### Community 12 - "signals"
Cohesion: 0.17
Nodes (16): action(), _mean(), _phi(), posting_beta(), The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json…, _sd() (+8 more)

### Community 13 - "_reveal_page"
Cohesion: 0.50
Nodes (4): Run script-only HTML in an invisible frame (same origin, so it can reach…, Fade the page area back in on a page that has no dashboard frame (password…, _reveal_page(), _run_js()

### Community 14 - "month_extras.py"
Cohesion: 0.25
Nodes (13): _bags_on_offer(), _block(), build_extras(), _deals(), _pick(), _posting(), _posting_block(), region() (+5 more)

### Community 15 - "type_fn"
Cohesion: 0.16
Nodes (16): names(), Upper-cased bag types from new_products.txt in file order ([] = no new…, build(), ({TYPE: Kenya shop on-hand}, {TYPE: Sinza + Uganda on-hand}) — live Odoo., The NP.runway payload: {days, bags: [{name, created, category, stockKe,…, Product name → bag type (see the module docstring)., [{name, created, category}] newest first — the runway bag types as of today; []…, {TYPE: bags sold} for the given runway types over [start, end] — POS bags,… (+8 more)

### Community 16 - "publish.py"
Cohesion: 0.23
Nodes (13): argparse, fnmatch, py_compile, changed_files(), git(), group(), is_secret(), main() (+5 more)

### Community 17 - "data"
Cohesion: 0.20
Nodes (11): _db_count(), monthly_from_db(), Reporting month's subset count (e.g. rejectBags, giftBags) from…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,…, _live_bags(), _load_combos_by_shop(), _from_file(), _nonempty() (+3 more)

### Community 18 - "build_payload"
Cohesion: 0.18
Nodes (13): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+5 more)

### Community 19 - "shop_launch.py"
Cohesion: 0.20
Nodes (14): build(), _cfg(), first_sale(), kenya_posts(), load_workplan(), make_matcher(), match(), _parse_workplan() (+6 more)

### Community 20 - "shop_corporate.py"
Cohesion: 0.15
Nodes (24): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), _acronym(), build(), _maybe(), owns(), corporate_team_receipts(), _d() (+16 more)

### Community 21 - "Bags on offer vs not on offer"
Cohesion: 0.12
Nodes (17): Bags on offer vs not on offer, Corporate-lead till orders, Counted by how it was sold, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Regenerate, Shop birthdays (+9 more)

### Community 22 - "bags_on_offer.py"
Cohesion: 0.09
Nodes (24): _bag_tiers(), _base_windows(), _build_period(), _custom_range(), fmt(), inject(), main(), _new_products() (+16 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.18
Nodes (13): Bags not on offer per market (Kenya/Sinza/Uganda), Combo button usage / rung vs pot. (till check), Self-made combos vs running combos (doc), DoW mirror shops (DOW_MIRROR), Monetary implication panel (bundling discount), Rank chip (follows active Sort filter), Running-combo classification by bag composition (slot-aware sheet match), Standalone SQL (self_made_vs_running_combos.sql) (+5 more)

### Community 24 - "shop_stock_levels.py"
Cohesion: 0.15
Nodes (23): build(), dispatch_shop(), fit(), grand_total(), leads(), needs(), new_bags(), _next_month() (+15 more)

### Community 25 - "signals"
Cohesion: 0.09
Nodes (29): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+21 more)

### Community 26 - "shops_dispatch.py"
Cohesion: 0.21
Nodes (14): build_period(), distributed_in(), main(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only., Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).… (+6 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.18
Nodes (14): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes) (+6 more)

### Community 28 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 29 - "_enrich_deals"
Cohesion: 0.29
Nodes (4): _enrich_deals(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "fetch"
Cohesion: 0.13
Nodes (24): What the page shows (per period), _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), combo_slots() (+16 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.09
Nodes (16): SCRIPT_TIMEOUT = 600s config, fragment, hashlib, html, streamlit, _bg_done_msg(), _bg_watch(), _fmt_secs() (+8 more)

### Community 33 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.16
Nodes (8): _cause(), esc(), fmt(), ladder_strip(), pct(), monthly_report.py…, _smc_srow(), _stock_rows()

### Community 35 - "_combo_norm_option"
Cohesion: 0.38
Nodes (6): _combo_norm_option(), combos_by_shop(), _norm(), _tokmatch(), Per-shop view for Shops Efficiency, keyed by shop-location label (e.g.…, One combo slot-option → its distinctive bag token(s), colours/category words…

### Community 36 - "chronos_train.py"
Cohesion: 0.12
Nodes (29): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+21 more)

### Community 37 - "stock.py"
Cohesion: 0.20
Nodes (15): odoo_stock_levels(), Live per-shop Odoo on-hand in the SAME shape parse_sheet(STOCK_LEVELS) returns:…, _codes_for(), _inlist(), odoo_stock_at_location(), odoo_stock_by_product(), odoo_stock_by_shop_code(), _ok() (+7 more)

### Community 38 - "build_payload"
Cohesion: 0.12
Nodes (18): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+10 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "Product (bag) targets"
Cohesion: 0.29
Nodes (7): Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 41 - "push_rules.py"
Cohesion: 0.10
Nodes (21): action(), _cover_txt(), _kind(), _n(), not_moving(), posting_median(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).…, {market: median postsMonth of the bags that were posted at all} — the 'below… (+13 more)

### Community 42 - "datetime"
Cohesion: 0.09
Nodes (31): calendar, collections, csv, datetime, lib/bag_quant.py — quant signals per bag: drift, volatility, Sharpe-style…, lib/colours.py — colour FAMILY of a product (Brown, Black, Red, Beige, Grey,…, lib/new_products_list.py — which bag types count as this month's NEW PRODUCTS.…, allocate() (+23 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "run_query"
Cohesion: 0.12
Nodes (17): corporate_from_db(), corporate_target_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, This month's Odoo corporate target {bags, kes} (sales_pos_target, scope…, _corporate_bags(), Corporate bags sold in the given month, live from Odoo invoices. Returns 0 when…, _drop_shared_conn(), _env() (+9 more)

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

### Community 52 - "norm"
Cohesion: 0.16
Nodes (14): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, ({PRODUCT: {SHOP CODE: units}}, {PRODUCT: {SHOP CODE: [[colour, units], …]}})…, shop_sales(), _aliases(), _Deriver, norm(), odoo_name() (+6 more)

### Community 53 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.17
Nodes (12): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+4 more)

### Community 56 - "generators/self_made_combos.py"
Cohesion: 0.08
Nodes (36): Buckets, _add_noffer_posts(), per_bag(), _add_oos(), _apply_receipt_offers(), bag_classifier(), infer(), _norm() (+28 more)

### Community 57 - "compute_period"
Cohesion: 0.12
Nodes (11): apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _metric(), pct(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period. (+3 more)

### Community 58 - "_enrich_deals"
Cohesion: 0.14
Nodes (11): dow_tier_weeks(), _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg(), _odoo_stock_by_shop() (+3 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "lib/db.py"
Cohesion: 0.14
Nodes (14): One-off: restore August's Offer Type figures into monthly_report_history.json…, fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py…, Read the Shop → Region table from docs/shop-regions.md so the mapping can be…, main() (+6 more)

### Community 61 - "_combo_button_usage"
Cohesion: 0.22
Nodes (8): _combo_button_usage(), _combo_norm_option(), _combo_odoo_slots(), _matches_sheet(), One combo slot-option → its distinctive bag token(s), colours/category words…, Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…, The sheet label this Odoo combo maps to (same slot count, every slot overlaps),…, Per running combo: units rung through the combo button (Odoo) vs the sheet's…

### Community 62 - "oos_callbacks.py"
Cohesion: 0.05
Nodes (63): Out of stock — call back, fixture, match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, bag(), aggregate(), flat(), split() (+55 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "main.py"
Cohesion: 0.11
Nodes (22): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, Denri Africa — Marketing Dashboard Launcher… (+14 more)

### Community 65 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.15
Nodes (11): _local_deal_rows(), Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), Blocker counter, Deals from posters (RALPH_DEALS.md) — 2026-10-04, Final summary, Log (+3 more)

### Community 66 - "timed_offers.py (generator)"
Cohesion: 0.09
Nodes (22): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+14 more)

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.20
Nodes (9): Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, Page, Production — shop requests vs approved list (18 Oct 2026), Shop requests — requested vs received (18 Oct 2026), Shop Stock Levels — min / max per shop, stocks report and next-month preparedness (+1 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "live_month_window"
Cohesion: 0.15
Nodes (15): month_window(), date, First → last calendar day of the LIVE month (today's month; see…, load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if…, _till_to_shop() (+7 more)

### Community 71 - "self_made_combos_bundle/lib/report_month.py"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "product_performance.py"
Cohesion: 0.05
Nodes (56): build(), categories(), _d(), explain(), _fmt_d(), _load_json(), load_lines(), load_posts() (+48 more)

### Community 74 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "lib/offer_data.py"
Cohesion: 0.20
Nodes (12): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), offer_data.py ─────────────────────────────────────────────────────────────────… (+4 more)

### Community 77 - "check_connection"
Cohesion: 0.14
Nodes (21): _bucket(), odoo_bag_daily_value(), odoo_bag_prices(), odoo_bulk_lines(), odoo_daily_kenya(), odoo_list_price(), odoo_offer_price(), odoo_window_sales() (+13 more)

### Community 78 - "push_planner.py"
Cohesion: 0.13
Nodes (22): build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), main(), month_progress() (+14 more)

### Community 79 - "self_made_combos_bundle/lib/__init__.py"
Cohesion: 0.11
Nodes (24): dotenv, lib — shared data-access for the marketing dashboard (Postgres migration).…, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the… (+16 more)

### Community 80 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), lib/theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 81 - "push_laya.py"
Cohesion: 0.13
Nodes (20): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+12 more)

### Community 82 - "new_products.py"
Cohesion: 0.20
Nodes (7): _base_colour(), _merge_rows_by_base_colour(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across…, _strip_colour_qualifiers()

### Community 83 - "test_push_planner.py"
Cohesion: 0.17
Nodes (19): Per bag × market: the facts (`push_rules.facts`, `add_peers`), add_peers(), _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m… (+11 more)

### Community 84 - "paths.py"
Cohesion: 0.13
Nodes (10): apply_walkins(), metric_byshop(), parse_sheet(), shops_efficiency.py…, Return (data, meta) for the Kenya shops, locating columns by header name…, safe_int(), update_history(), lib/paths.py — where every kind of file lives. Use these instead of building… (+2 more)

### Community 85 - "lib/report_month.py"
Cohesion: 0.16
Nodes (19): count_complete_weeks_in_month(), Count Mon–Sun weeks in the reporting month that have ≥5 days falling within it., anchor(), is_pinned(), live_anchor(), live_month_key(), month_key(), month_name() (+11 more)

### Community 86 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.25
Nodes (7): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does, Current Performance (doc)

### Community 87 - "F"
Cohesion: 0.24
Nodes (16): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), A facts row with sensible defaults, overridden by kw., test_fallback_slow_seller_or_overstocked() (+8 more)

### Community 88 - "fetch_new_products_data"
Cohesion: 0.20
Nodes (14): fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_sales_window() (+6 more)

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.14
Nodes (10): Agent skills — retail analytics, Test a skill, Use in another project, Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods (+2 more)

### Community 91 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.06
Nodes (36): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards) (+28 more)

### Community 92 - "num"
Cohesion: 0.20
Nodes (11): _garr_line(), gnum(), num(), _offers(), _parse_offers(), _units(), This month's timed-offer campaigns, flattened for storage. The live TO payload…, Greedy single-line array extractor — handles nested [[...],[...]] arrays. (+3 more)

### Community 93 - "shop_requests.py"
Cohesion: 0.21
Nodes (14): _onoff(), _d(), _f(), _match(), _offer_label(), _pct(), production(), lib/shop_requests.py — what each shop REQUESTED in the Odoo dispatch module… (+6 more)

### Community 94 - "fetch_posting_data"
Cohesion: 0.05
Nodes (65): _alignment_region(), _for(), _sold(), _stk(), _units(), _analyze_region(), _bag_level_bags(), _bt_on_offer() (+57 more)

### Community 95 - "corporate_clients_from_db"
Cohesion: 0.40
Nodes (6): corporate_clients_from_db(), _months(), A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],…, Current month's corporate activity per client (quoted · invoiced · paid · sold)…, _txt()

### Community 96 - "offer_picking.py"
Cohesion: 0.06
Nodes (52): Offer type summary (matrix), _alt_cost(), _apply_alias(), build(), _build_catalog(), _combo_cost(), _combo_slots(), _is_full_price() (+44 more)

### Community 97 - "month_end.py"
Cohesion: 0.31
Nodes (8): clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.…, YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that…, After the closing month's timed offers are safely in Supabase, empty the config…, run(), target_month(), subprocess

### Community 98 - "_combo_button_usage"
Cohesion: 0.14
Nodes (11): _combo_button_usage(), _matches_sheet(), _opt_close(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Same slot count and every slot overlaps under SOME pairing (any order: the…, The sheet label this Odoo combo maps to, or None if it isn't on the sheet.…, _slots_fit() (+3 more)

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "timed_offers.py"
Cohesion: 0.11
Nodes (17): _bags_from_file(), build_offer(), _derive_month(), load_config(), _name_sql(), _norm_offer(), _price_sql(), timed_offers.py… (+9 more)

### Community 101 - "current_performance.html"
Cohesion: 0.50
Nodes (4): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance)

### Community 102 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 103 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.29
Nodes (7): lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, lib/report_month.py (which month are we reporting?), self_made_combos.html static page (reads const SMC), self_made_combos.py generator (build_payload + SQL + injection)

### Community 104 - "posting_yields.py"
Cohesion: 0.15
Nodes (12): _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., _mkt_perfect_week_index(), _mkt_week_label(), posting_yields.py…, Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]. (+4 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "update_np_weekly_history"
Cohesion: 0.29
Nodes (7): _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)., Ordinal among the month's perfect weeks (>=5 days in month), so the first FULL…, Snapshot each Sun–Sat week (sales, Kenya/Outside posts) into…, update_np_weekly_history()

### Community 107 - "os"
Cohesion: 0.08
Nodes (19): fetch_monthly_target(), fetch_sheet_data(), forward_projections.py…, main(), date, _query_ready(), weekly_sales.py — the weekly-sales fix. Computes the CURRENT Sun–Sat week's…, The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's… (+11 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "fetch"
Cohesion: 0.29
Nodes (5): fetch(), Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), _read_offer_analysis()

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "odoo_tabs.py"
Cohesion: 0.13
Nodes (22): load(), _build(), build_rows(), catalog_rows(), default_window(), _flag_cells(), _fmt(), get_rows() (+14 more)

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 114 - "reject_variants"
Cohesion: 0.33
Nodes (7): _parse_colour(), First primary colour token found in a name (longest-first), Title-cased; '' if…, Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share…, Per-[REJECT]-product variant rows for a name-filtered offer, for the filterable…, reject_variants(), _match_bag(), _singular_tokens()

### Community 121 - "load_pages"
Cohesion: 0.20
Nodes (9): read_block(), read_block(), _read_timed_offers(), _offer_bagtypes_by_region(), On-offer bag types per region, read from self_made_combos.html's SMC block:…, load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.… (+1 more)

### Community 122 - "base_name"
Cohesion: 0.33
Nodes (7): base_name(), dispatch_by_product_shop(), _num(), The catalogue key for an Odoo product name: norm() without the "[REJECT]" tag…, {NORM(product): {SHOP: bags}} of POS bag sales in [start, end]; None if DB…, {NORM(product): {SHOP: bags distributed in}} from combined_distribution.sql's…, sales_by_product_shop()

### Community 123 - "What the page shows"
Cohesion: 0.20
Nodes (9): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Bulk orders, Data, Product Performance — which bags, categories and colours carry the sales, and why (+1 more)

### Community 126 - "Monthly Report (doc)"
Cohesion: 0.22
Nodes (9): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+1 more)

### Community 128 - "odoo_weekly_breakdown"
Cohesion: 0.40
Nodes (6): odoo_weekly_breakdown(), _perfect_week_index(), Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, update_weekly_history(), _week_start()

### Community 130 - "New Products Analytics (doc)"
Cohesion: 0.25
Nodes (7): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), Weekly Performance chart (Week 1 to latest), Net returns rule (qty <> 0, subtract refunds), Returns netting rule (qty <> 0), Python dependencies list (requirements.txt), Postgres source-of-truth migration (off Google Sheets, weekly first)

### Community 131 - "Offer Picking (doc)"
Cohesion: 0.29
Nodes (8): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES)

### Community 138 - "odoo_month_product_bags"
Cohesion: 0.33
Nodes (6): odoo_combo_product_bags(), odoo_lifetime_product_bags(), odoo_month_product_bags(), All-time bags per product from Odoo (no month window) — the lifetime sales of…, [(product name, bags)] for bags sold INSIDE combos (sub_product_line) in the…, Reporting month's bags per product from Odoo (Postgres), or None if the DB…

### Community 145 - "Shop Launch"
Cohesion: 0.29
Nodes (6): Config, Launch day, Marketing posts, Sales, Shop Launch, What the page shows

### Community 153 - "monthly_target_rows"
Cohesion: 0.16
Nodes (14): build(), Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), bag_posts(), tally(), load(), (daily, total, stock, launch, start, end) for Kenya from Odoo; daily per bag…, {BAG: (posts this month, posts last week)} — Kenya posts (col E) from the two… (+6 more)

### Community 154 - "Product / name matching (doc)"
Cohesion: 0.33
Nodes (7): match_odoo_bags [S_0] internal-reference prefix fix, Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix), Normalisation rules (upper-case, strip ref prefix, exclude combos/non-sellable stock), Deal enrichment & name matching (_enrich_deals / _match)

### Community 155 - "kenya_stock_by_bag"
Cohesion: 0.33
Nodes (6): kenya_stock_by_bag(), {BAG_UPPER: category} — the bag's category label only, from the product…, {BAG_UPPER: units} — physical stock summed per BAG TYPE from a repo CSV's UNITS…, {BAG_UPPER: {stock, category}} for the configured bags. STOCK is LIVE Kenya…, _sheet_category_by_bag(), _stock_from_file()

### Community 156 - "custom_range.py"
Cohesion: 0.19
Nodes (14): block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each…, (from, to) dates for the page's Custom period, or None. Swapped if reversed;… (+6 more)

### Community 157 - "generator"
Cohesion: 0.33
Nodes (6): generator(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, start_daily_snapshot(), run_scripts()

### Community 158 - "family"
Cohesion: 0.40
Nodes (6): ({BAG: units}, {BAG: {colour: units}}) at CBD/Stock., warehouse_stock(), family(), _load(), _norm(), Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…

### Community 159 - "product_targets_workbook.py"
Cohesion: 0.33
Nodes (5): openpyxl, openpyxl_comments, openpyxl_styles, openpyxl_utils, product_targets_workbook.py — the month's bag targets as an Excel workbook with…

### Community 160 - "scripts/receipt_combos.py"
Cohesion: 0.29
Nodes (6): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…, itertools

### Community 161 - "_bag_stock"
Cohesion: 0.40
Nodes (5): _bag_stock(), _combo_bags(), _norm_bag(), Space/punctuation-insensitive key so 'MINIZURI' matches 'MINI ZURI'., Component bags of an offer, each with its stock, sorted most-stock first.

### Community 162 - "generate_insights.py"
Cohesion: 0.24
Nodes (5): card(), esc(), fmt(), generate_insights.py…, region_card()

### Community 163 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 164 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 165 - "_match"
Cohesion: 0.50
Nodes (3): _match(), _full(), _full_of()

### Community 166 - "_build_sheet_slots"
Cohesion: 0.50
Nodes (4): _build_sheet_slots(), _combo_sheet_slots(), Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]., [(label, slots)] for each running combo on the offer sheet (skips the TOTAL…

### Community 167 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 168 - "Sales-share targets per product"
Cohesion: 0.40
Nodes (4): Deliver, Sales-share targets per product, Steps, Tests

### Community 172 - "_bg_jobs"
Cohesion: 0.25
Nodes (9): cache_resource, _bg_jobs(), _bg_rebuild(), work(), Seconds the last good `kind` rebuild of `lbl` took (any kind as a fallback),…, Background rebuilds shared by every session: label → job (see _bg_rebuild)., Rebuild `lbl` in the background. kind: "auto" (skipped if a rebuild was tried…, _rebuild_secs() (+1 more)

### Community 173 - "offer_flags"
Cohesion: 0.50
Nodes (4): offer_flags(), prime_offer_flags(), Seed offer_flags() from MONTHLY_TARGET rows the caller already read (saves a…, {BAG TYPE: (kenya, sinza, uganda) on-offer bools} from MONTHLY_TARGET cols…

### Community 178 - "_month_archived"
Cohesion: 0.67
Nodes (3): cache_data, _month_archived(), True when `key` is in Supabase (falls back to monthly_report_history.json). If…

## Knowledge Gaps
- **200 isolated node(s):** `PERF`, `graphify`, `Use in another project`, `Test a skill`, `Inputs you must build from the project's data` (+195 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 940 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `bag_classifier()` connect `generators/self_made_combos.py` to `live_month_window`, `Product (bag) targets`, `push_planner.py`, `Push Planner (`push_planner.py` → `push_planner.html`, `PP`)`, `Bags on offer vs not on offer`, `fetch`, `oos_callbacks.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `Bags on offer vs not on offer` connect `Bags on offer vs not on offer` to `offer_picking.py`, `fetch`, `generators/self_made_combos.py`, `Denri Africa Dashboard Design System (skill)`, `oos_callbacks.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `run_query()` connect `run_query` to `current_performance.py`, `odoo_weekly_breakdown`, `lib/receipt_combos.py`, `odoo_month_product_bags`, `type_fn`, `build_payload`, `shop_launch.py`, `shop_corporate.py`, `shop_stock_levels.py`, `monthly_target_rows`, `_enrich_deals`, `fetch`, `_bags_not_on_offer`, `chronos_train.py`, `stock.py`, `build_payload`, `_odoo_stock_for`, `datetime`, `norm`, `generators/self_made_combos.py`, `_enrich_deals`, `lib/db.py`, `_combo_button_usage`, `oos_callbacks.py`, `live_month_window`, `product_performance.py`, `check_connection`, `paths.py`, `fetch_new_products_data`, `shop_requests.py`, `fetch_posting_data`, `corporate_clients_from_db`, `offer_picking.py`, `_combo_button_usage`, `os`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `fetch()` (e.g. with `classify()` and `oos_key()`) actually correct?**
  _`fetch()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `PERF`, `graphify`, `Use in another project` to the rest of the system?**
  _200 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `current_performance.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13970588235294118 - nodes in this community are weakly interconnected._
- **Should `laya.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0573025856044724 - nodes in this community are weakly interconnected._