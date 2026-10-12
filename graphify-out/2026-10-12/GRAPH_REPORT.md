# Graph Report - Marketing_dashboard  (2026-10-12)

## Corpus Check
- 194 files · ~798,589 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 17 file(s) not represented in the graph (top: .csv 9, (none) 2, .bat 2)

## Summary
- 2267 nodes · 4159 edges · 157 communities (136 shown, 21 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 197 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `48a25d3d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- safe_int
- laya.py
- tests/test_receipt_combos.py
- offer_data.py
- Offer Picking Dashboard Page
- generate_insights.py
- Kitengela Rejects tracker (timed offer)
- monthly_report.py
- check_connection
- run_query
- fetch
- datetime
- norm
- self_made_combos_bundle/lib/db.py
- load_data
- fetch_new_products_data
- publish.py
- forward_projections.py
- build_payload
- main.py
- build_payload
- Dashboard Insights skill
- lib/db.py
- Product / name matching (doc)
- v5_theme.js
- signals
- os
- Dashboard Menu Docs (spec index)
- Self-made combos vs running combos (doc)
- _enrich_deals
- oos_chip.js
- Sidebar Navigation (icon rail / expanded drawer)
- streamlit_app.py
- Marketing Dashboard Insights Page
- design-taste-frontend (anti-slop frontend skill)
- stock.py
- chronos_train.py
- build
- theme.py
- Shops Efficiency Tracking spec doc
- _dead_stock_region
- _enrich_deals
- chart_switcher.js
- On-offer definition per region (from SMC block)
- Offer Picking (doc)
- Combos & Power Deals by Shop panel (#combo-shop)
- self_made_combos_bundle/offer_data.py
- self_made_combos.py generator (build_payload + SQL + injection)
- CLAUDE.md
- history.py (read months back)
- Self-made combos vs Running combos portable bundle README
- timed_offers.py (generator)
- scripts/test_receipt_combos.py
- fetch_posting_data
- algorithmic-art skill
- dataviz-charts skill
- July 2026 Monthly Report Page
- test_oos_callbacks.py
- get_gspread_client
- High-End Visual Design skill
- bag_quant.py
- product_targets.py
- oos_callbacks.py
- daydream skill (Vault Daydream)
- custom_range.py
- render(idx) function
- _seasonality
- buildExportDoc(mode) function
- TTL disk-cache rationale (.odoo_cache/)
- perf_data.js
- attachPopover(cardId, popId) function
- _date
- welcome_screen.js
- attach_stock
- compute_period
- shop_birthdays.py
- shops_efficiency.py
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- shops_dispatch.py
- OOS call-back progress (Ralph loop log)
- _combo_button_usage
- push_laya.py
- build_offer
- test_push_planner.py
- followup
- self_made_combos.py
- Chart type switcher (every chart, every menu)
- F
- history.py
- test_stockout_demand.py
- Out-of-stock demand — people, not requests
- Denri Africa Dashboard Design System (skill)
- build_actions
- marketing_dashboard.sql
- timed_offers.py
- Ralph task — deals from the posters (deals_kenya.csv)
- Bags on offer vs not on offer
- update_np_weekly_history
- attach
- Bag Signals — quant view of each bag (posting · stock · selling)
- new_products.py
- _fetch_monthly_kenya
- page_sidebar.js
- _apply_receipt_offers
- Ralph task — only three sheet tabs left
- base_name
- test_share_targets.py
- main
- online
- family
- _load_combos_by_shop
- shop-birthdays.md
- test_stocks_picking.py
- odoo_tabs.py
- load_offers
- Product (bag) targets
- POSTING (SALES YIELDS FROM ACCURATE POSTING).py
- _bg_jobs
- fallback_bag
- load
- bucket
- Stocks Picking (Redundancy rate) — every bag's colours side by side (Kenya · Sinza · Uganda)
- contextlib
- _bag_tiers
- self_made_combos_bundle/lib/__init__.py
- Month-End Routine (doc)
- kenya_shop_codes
- Bag targets October 2026_b78d9f88.md
- moves_sql
- month_end.py (script)
- Shop Launch
- sum_shops
- Ralph task — "Out of stock — call back" demand per shop
- _page
- stocks_picking_app.py
- push_to_supabase.py
- bag_classifier
- _alignment_region
- corporate_clients_from_db
- test_sheet_reads.py
- push_rules.py

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 49 edges
2. `fetch_posting_data()` - 35 edges
3. `fetch()` - 34 edges
4. `get_gspread_client()` - 33 edges
5. `build_payload()` - 30 edges
6. `check_connection()` - 29 edges
7. `build_payload()` - 24 edges
8. `build_offer()` - 22 edges
9. `F()` - 22 edges
10. `Self-made combos vs running combos (doc)` - 22 edges

## Surprising Connections (you probably didn't know these)
- `Marketing Bags For Shoot — Stock rate (the first section on the page)` --references--> `bag_classifier()`  [INFERRED]
  docs/stocks-picking.md → self_made_combos.py
- `Buckets` --references--> `bag_classifier()`  [INFERRED]
  docs/bags-on-offer.md → self_made_combos.py
- `The split — by each bag's share of recent sales` --references--> `bag_classifier()`  [INFERRED]
  docs/product-targets.md → self_made_combos.py
- `Inputs (read only — nothing is written to Odoo or the sheet)` --references--> `bag_classifier()`  [INFERRED]
  docs/push-planner.md → self_made_combos.py
- `Laya's second opinion (`lib/push_laya.py`)` --references--> `state_text()`  [INFERRED]
  docs/push-planner.md → lib/push_laya.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shell navigation ties sidebar items to their generator-backed dashboard pages** — shell_sidebarnavigation, shell_scriptmap, shell_pagepurposemap, shell_dashframeiframe, shell_currentperformancehtml [EXTRACTED 0.85]
- **Self-made combos bundle: generator, Sheets auth, DB access, and dependency manifest working together to build the combos page** — export_self_made_combos_bundle_self_made_combos_py, export_self_made_combos_bundle_offer_data_py, export_self_made_combos_bundle_google_auth_py, export_self_made_combos_bundle_lib_db_py, export_self_made_combos_bundle_requirements [EXTRACTED 0.90]
- **Month-end archive pipeline: rebuild pinned month, snapshot report, push to Supabase, render History** — month_end_monthendpy, monthly_report, push_to_supabase, history, month_end_historyhtml [EXTRACTED 0.90]
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]
- **Dashboard Insights skill synthesizes across four dashboard data objects (PERF/PROJ, NP, OA, PA)** — _claude_skills_dashboard_insights_skill, current_performance_html_perf_data, docs_new_products_doc, docs_self_made_combos_doc, docs_posting_yields_doc [EXTRACTED 1.00]
- **Monthly Report reads injected data blocks from the generator pages that run before it** — docs_monthly_report_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_posting_yields_doc, current_performance_html_current_performance_page [EXTRACTED 1.00]
- **Static HTML + Python generator + injected JSON data-block pattern shared across dashboard pages** — docs_readme_dashboard_architecture, offer_picking_op_data_block, forward_projections_proj_data_block, report_2026_july_rpt_data_object, claude_skills_dataviz_charts_data_marker_pattern [INFERRED 0.85]
- **Cross-report 'unmarketed stock / posting gap' finding echoed across Monthly Report, Insights, and Forward Projections** — report_2026_july_unmarketed_stock_finding, insights_unposted_stock_finding, report_2026_july_regional_unevenness_finding, insights_uganda_conversion_finding [INFERRED 0.85]
- **Kitengela reject clearance tracked across pricing, timed-offer, and performance pages** — docs_timed_offers_kitengelarejectstracker, reject_sales_rejectsalepage, docs_current_performance_rejectsplitline, docs_reject_sales_rejectsaledoc, docs_timed_offers_rejectstockcsv [INFERRED 0.85]

## Communities (157 total, 21 thin omitted)

### Community 0 - "safe_int"
Cohesion: 0.18
Nodes (20): _build_no_convert(), _fetch_sinza_monthly(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int(), _is_checked() (+12 more)

### Community 1 - "laya.py"
Cohesion: 0.10
Nodes (26): Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket(), _cache_get(), _cache_put() (+18 more)

### Community 2 - "tests/test_receipt_combos.py"
Cohesion: 0.08
Nodes (43): _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, What the page shows (per period), bag_key(), classify(), _fits(), _groups(), load_offers() (+35 more)

### Community 3 - "offer_data.py"
Cohesion: 0.20
Nodes (13): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), rows_of() (+5 more)

### Community 4 - "Offer Picking Dashboard Page"
Cohesion: 0.17
Nodes (12): DATA_START/DATA_END comment marker injection pattern, build_all.py (rebakes every page), Dashboard Architecture (static HTML + Python generator + injected data block), .github/workflows/refresh.yml CI workflow, shell.html (sidebar nav frame, loads each page into an iframe), Baseline Forecast Section (fixed recommended picks), Forecast Section (live picks for next month), Next Month's Combos to Run Section (+4 more)

### Community 5 - "generate_insights.py"
Cohesion: 0.12
Nodes (12): graw(block, key) function (bare numeric getter), gstr(block, key) function (string field regex getter), Key-rename / run-order gotcha (blanks or zeros), NEW_PROD data block (New Products), OFFER_DATA data block (Self Made Combos), POST_DATA data block (Posting), read_block(file, start, end) function, card() (+4 more)

### Community 6 - "Kitengela Rejects tracker (timed offer)"
Cohesion: 0.05
Nodes (42): Card entrance animation via CSS @keyframes + animation-fill-mode: both, "Below cost" flag, bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, "No BOM" flag, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source) (+34 more)

### Community 7 - "monthly_report.py"
Cohesion: 0.05
Nodes (47): _bags_on_offer(), _block(), build_extras(), _deals(), _pick(), _posting(), _posting_block(), region() (+39 more)

### Community 8 - "check_connection"
Cohesion: 0.11
Nodes (24): corporate_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, _corporate_bags(), Corporate bags sold in the given month, live from Odoo invoices. Returns 0 when…, _cache_path(), check_connection(), DataFrame, run_query with a TTL disk cache. Identical to run_query for callers, but a… (+16 more)

### Community 9 - "run_query"
Cohesion: 0.10
Nodes (24): corporate_target_from_db(), This month's Odoo corporate target {bags, kes} (sales_pos_target, scope…, _drop_shared_conn(), _env(), get_engine(), Engine, The process's reused connection (opened on first query). Every generator runs…, Run a read query and return a DataFrame, or None if the DB is unreachable.… (+16 more)

### Community 10 - "fetch"
Cohesion: 0.09
Nodes (29): _archived_source(), _as_date(), _build_period(), fetch(), cat_tier(), classify(), classify_for(), make_classifier() (+21 more)

### Community 11 - "datetime"
Cohesion: 0.06
Nodes (31): calendar, _db_count(), monthly_from_db(), current_performance.py…, Reporting month's subset count (e.g. rejectBags, giftBags) from…, Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written… (+23 more)

### Community 12 - "norm"
Cohesion: 0.15
Nodes (16): _aliases(), build_rows(), _Deriver, _flag_cells(), _fmt(), norm(), odoo_name(), _products() (+8 more)

### Community 13 - "self_made_combos_bundle/lib/db.py"
Cohesion: 0.15
Nodes (18): check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, Run a read query and return a DataFrame, or None if the DB is unreachable.… (+10 more)

### Community 14 - "load_data"
Cohesion: 0.40
Nodes (5): load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if…, _till_to_shop()

### Community 15 - "fetch_new_products_data"
Cohesion: 0.19
Nodes (14): fetch_new_products_data(), _apply_stock(), _post_lookup(), is_checked(), _key(), _keyed(), _np_week_bags(), odoo_sales_window() (+6 more)

### Community 16 - "publish.py"
Cohesion: 0.13
Nodes (21): argparse, fnmatch, clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.…, YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that…, After the closing month's timed offers are safely in Supabase, empty the config…, run() (+13 more)

### Community 17 - "forward_projections.py"
Cohesion: 0.10
Nodes (16): build_all.py ────────────────────────────────────────────────────────────────…, fetch_monthly_target(), Current Performance (doc), fetch_sheet_data(), odoo_weekly_breakdown(), _perfect_week_index(), forward_projections.py…, Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at… (+8 more)

### Community 18 - "build_payload"
Cohesion: 0.06
Nodes (35): _bags_not_on_offer(), _infer(), _norm(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups() (+27 more)

### Community 19 - "main.py"
Cohesion: 0.06
Nodes (45): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the… (+37 more)

### Community 20 - "build_payload"
Cohesion: 0.14
Nodes (16): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+8 more)

### Community 21 - "Dashboard Insights skill"
Cohesion: 0.17
Nodes (16): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Current Performance Dashboard Page, Forward Projections section, PERF data block (weekly/monthly sales KPIs), PROJ data block (forward projections, velocity factor, bare minimum), Monthly Report (doc) (+8 more)

### Community 22 - "lib/db.py"
Cohesion: 0.18
Nodes (12): fetch(), fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py…, Read the Shop → Region table from docs/shop-regions.md so the mapping can be…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A… (+4 more)

### Community 23 - "Product / name matching (doc)"
Cohesion: 0.18
Nodes (14): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix) (+6 more)

### Community 24 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 25 - "signals"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

### Community 26 - "os"
Cohesion: 0.06
Nodes (42): One-off: restore August's Offer Type figures into monthly_report_history.json…, _base_windows(), _custom_range(), fmt(), inject(), main(), _new_products(), _previous_payload() (+34 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.19
Nodes (13): Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes), Menu 5: Posting - Sales Yields from Accurate Posting (+5 more)

### Community 28 - "Self-made combos vs running combos (doc)"
Cohesion: 0.18
Nodes (13): Bags not on offer per market (Kenya/Sinza/Uganda), Combo button usage / rung vs pot. (till check), Self-made combos vs running combos (doc), DoW mirror shops (DOW_MIRROR), Monetary implication panel (bundling discount), Rank chip (follows active Sort filter), Running-combo classification by bag composition (slot-aware sheet match), Standalone SQL (self_made_vs_running_combos.sql) (+5 more)

### Community 29 - "_enrich_deals"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "oos_chip.js"
Cohesion: 0.08
Nodes (38): attach(), close(), esc(), form(), go(), iso(), mountPanel(), open() (+30 more)

### Community 31 - "Sidebar Navigation (icon rail / expanded drawer)"
Cohesion: 0.12
Nodes (19): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), insights.html, PERF/PROJ data block (Current Performance), Live view vs archive split (lib/report_month.py live_*), Denri Africa · Marketing Dashboard (README, project overview), current_performance.html (nav target) (+11 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.10
Nodes (14): SCRIPT_TIMEOUT = 600s config, hashlib, _bg_done_msg(), _bg_watch(), _fmt_secs(), _load_secrets_into_env(), _month_end_running(), streamlit_app.py — Denri Marketing Dashboard on Streamlit. Serves the existing… (+6 more)

### Community 33 - "Marketing Dashboard Insights Page"
Cohesion: 0.13
Nodes (15): Menu 1: Current Performance, Bare Minimum (Bags to be Sold) KPI, Bare Minimum (Growth %) KPI, Declined By KPI (bags missed that week), Forecasted Projection KPI (with corporate in mind), Forward Projections Page, PROJ_DATA_START/PROJ_DATA_END injected JSON data block, Standard Projection KPI (% of Total Target) (+7 more)

### Community 34 - "design-taste-frontend (anti-slop frontend skill)"
Cohesion: 0.18
Nodes (12): design-taste-frontend (related skill), design-taste-frontend (anti-slop frontend skill), Brief-First Process (8-step design workflow), Hard Bans (typography, color, layout, code, content clichés), Pre-Flight Checklist (90+ items), Redesign Protocol (upgrading existing UI), Three Dials — DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, Three AI-generated design clusters (calibration reference) (+4 more)

### Community 35 - "stock.py"
Cohesion: 0.20
Nodes (15): _codes_for(), _inlist(), odoo_stock_at_location(), odoo_stock_by_product(), odoo_stock_by_shop_code(), _ok(), _qty(), lib/stock.py — live Odoo on-hand stock, per product / market / shop. Single… (+7 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.10
Nodes (33): chronos, daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END… (+25 more)

### Community 37 - "build"
Cohesion: 0.06
Nodes (40): Offer type summary (matrix), _alt_cost(), _apply_alias(), build(), _build_catalog(), _combo_cost(), _combo_slots(), _is_full_price() (+32 more)

### Community 38 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 41 - "_enrich_deals"
Cohesion: 0.16
Nodes (9): _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,… (+1 more)

### Community 42 - "chart_switcher.js"
Cohesion: 0.13
Nodes (33): alpha(), apply(), attach(), axisOpts(), build(), changeTxt(), Chart(), clone() (+25 more)

### Community 43 - "On-offer definition per region (from SMC block)"
Cohesion: 0.25
Nodes (8): Dead Stock Accountability tuning knobs, Per-region high-stock floors (Kenya 20, Sinza 5, Uganda 5), weak_max threshold (sold < 5 = weak sales), On-offer definition per region (from SMC block), Reject Sale margin report (converted xlsx), 'below cost' margin flag, 'pinned' flag, 'thin' margin flag

### Community 44 - "Offer Picking (doc)"
Cohesion: 0.29
Nodes (8): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES)

### Community 45 - "Combos & Power Deals by Shop panel (#combo-shop)"
Cohesion: 0.25
Nodes (8): Combos & Power Deals by Shop panel (#combo-shop), compute_period() function (emits pushDetail per period), Deal of the Week — Tier 2 (latest 2-week window) shop-scoped view, DenriTableFilter reusable filter bar component, DOW_MIRROR expansion (Starmall to Hazina/Hilton/KTDA), odoo_stock_levels() function, Push via filter (None / power deal / deal of the week tag), shops_efficiency.html page

### Community 46 - "self_made_combos_bundle/offer_data.py"
Cohesion: 0.14
Nodes (18): Shared Google Sheets authentication for every dashboard generator. Two modes,…, build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), cell(), find_row(), find_row_any() (+10 more)

### Community 47 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.13
Nodes (17): google_auth.py (Sheets auth), offer_data.build (batched Sheets range fetch), lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, google_auth.py (service account or OAuth desktop), gspread>=6.0 dependency (Google Sheets access) (+9 more)

### Community 49 - "history.py (read months back)"
Cohesion: 0.20
Nodes (11): lib/db.py (Supabase session pooler DB access), lib/db.run_query (shared connection reuse per subprocess), Refresh Performance (shared connection reuse, batched Sheets reads), denri_mkt_* Supabase tables, history.html page, history.py (read months back), month_end.py (freezes a month), push_to_supabase.py (write months) (+3 more)

### Community 50 - "Self-made combos vs Running combos portable bundle README"
Cohesion: 0.17
Nodes (13): shop-regions.md (editable Shop to Region table), Composition-based classification rationale (Running vs Self-made), _matches_sheet / _build_sheet_slots slot-aware matching functions, Self-made combos vs Running combos portable bundle README, Returns netting rationale (qty <> 0, returns subtract), docs/self-made-combos.md full spec for the menu, docs/shop-regions.md editable shop to region map, sql/self_made_vs_running_combos.sql (standalone pure-SQL classification) (+5 more)

### Community 51 - "timed_offers.py (generator)"
Cohesion: 0.20
Nodes (10): renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator), Timed Offers Section — Back to School Edition (Report), Timed Offers snapshot-over-window workflow, /api/refresh endpoint (+2 more)

### Community 52 - "scripts/test_receipt_combos.py"
Cohesion: 0.08
Nodes (42): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+34 more)

### Community 53 - "fetch_posting_data"
Cohesion: 0.14
Nodes (12): _onoff(), _bt_on_offer(), _dead_clear(), fetch_posting_data(), _clear(), _yield(), _post_yield(), Marketing & Sales Alignment — posting yield, measured the way marketing… (+4 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.29
Nodes (7): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.)

### Community 56 - "July 2026 Monthly Report Page"
Cohesion: 0.18
Nodes (12): What Needs Attention Section, Finding: Uganda marketing conversion at 7.4%, below critical threshold, Finding: 5,572 bags in stock not posted, 53% of stock invisible, Section 1: Current Performance, July 2026 Monthly Report Page, Section 2: New Products, Section 3: Offer Type Analysis, Section 4: Posting Yields (Sales from Accurate Posting) (+4 more)

### Community 57 - "test_oos_callbacks.py"
Cohesion: 0.22
Nodes (16): aggregate(), flat(), split(), The page block: {period: {key: {"total": people, "shops": [[shop, people],…, pytest, _kai(), Tests for lib/oos_callbacks.py (WhatsApp "Out of stock — call back" demand).…, test_attach_stock_per_shop_and_colour() (+8 more)

### Community 58 - "get_gspread_client"
Cohesion: 0.11
Nodes (22): _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, main(), One-command Google re-authorization. python reauth.py Deletes any stale…, build() (+14 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "bag_quant.py"
Cohesion: 0.11
Nodes (26): build(), Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), action(), bag_posts(), tally(), load(), _mean() (+18 more)

### Community 61 - "product_targets.py"
Cohesion: 0.11
Nodes (28): allocate(), available_days(), bag_key_fn(), key(), base_period(), build(), load_targets(), monthly_target_rows() (+20 more)

### Community 62 - "oos_callbacks.py"
Cohesion: 0.14
Nodes (18): combo_key_fn(), load_rows(), _online_rows(), oos_by_bag_shop(), lib/oos_callbacks.py — "Out of stock — call back" demand, ONLINE and WALK-IN.…, Mark a key_fn as combo-aware: collect() then passes combo-named requests to it…, {shop: set(person)} → (distinct people, [[shop, people], …] high → low)., {period: {key: people}} from an aggregate() block. (+10 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "custom_range.py"
Cohesion: 0.19
Nodes (14): block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each…, (from, to) dates for the page's Custom period, or None. Swapped if reversed;… (+6 more)

### Community 65 - "render(idx) function"
Cohesion: 0.50
Nodes (4): buildCharts(m, wk, prevM) function, render(idx) function, selfMadeHtml(m) function, timedOffersHtml(m) function

### Community 66 - "_seasonality"
Cohesion: 0.15
Nodes (16): Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), _build_sheet_slots(), _combo_norm_option(), _combo_odoo_slots(), _combo_sheet_slots() (+8 more)

### Community 67 - "buildExportDoc(mode) function"
Cohesion: 0.50
Nodes (4): buildExportDoc(mode) function, colorizeForPaper() function, exportPDF() function, exportWord() function

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 71 - "_date"
Cohesion: 0.11
Nodes (25): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+17 more)

### Community 73 - "attach_stock"
Cohesion: 0.21
Nodes (12): attach_stock(), in_stock(), stk(), collect(), _in(), is_combo_request(), {period: (start, end)} for the dated periods (lifetime / current are undated).…, True when the request names a whole combo ("Amaya Handbag or Elyse Handbag +… (+4 more)

### Community 74 - "compute_period"
Cohesion: 0.12
Nodes (11): apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _metric(), pct(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period. (+3 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.10
Nodes (30): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+22 more)

### Community 76 - "shops_efficiency.py"
Cohesion: 0.20
Nodes (7): pathlib, metric_byshop(), parse_sheet(), shops_efficiency.py…, Return (data, meta) for the Kenya shops, locating columns by header name…, safe_int(), update_history()

### Community 77 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.25
Nodes (8): Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page, Why it isn't moving — reasons, per market (`push_rules.reasons`)

### Community 78 - "shops_dispatch.py"
Cohesion: 0.21
Nodes (14): build_period(), distributed_in(), main(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only., Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).… (+6 more)

### Community 79 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.13
Nodes (13): Blocker counter, Deals from posters (RALPH_DEALS.md) — 2026-10-04, Final summary, Log, OOS call-back progress (Ralph loop log), Sheets cut to three tabs (RALPH_SHEETS.md) — 2026-10-04, Sinza & Uganda (RALPH_OUTSIDE.md) — 2026-10-04, _local_deal_rows() (+5 more)

### Community 80 - "_combo_button_usage"
Cohesion: 0.14
Nodes (11): Inputs (from the user, Oct 2026), Ralph task — Sinza & Uganda offers + receipt-based combo counting, Steps, _combo_button_usage(), _matches_sheet(), _opt_close(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Two normalised slot options name the same bag, loosely: equal ignoring spaces… (+3 more)

### Community 81 - "push_laya.py"
Cohesion: 0.13
Nodes (20): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+12 more)

### Community 82 - "build_offer"
Cohesion: 0.18
Nodes (5): build_offer(), odoo_list_price(), _price_sql(), {BAG_UP: incl-tax Sales Price} — the product's normal price ("was"), the…, Compute the full TO payload for a single offer dict. Rebinds the per-offer…

### Community 83 - "test_push_planner.py"
Cohesion: 0.17
Nodes (19): Per bag × market: the facts (`push_rules.facts`, `add_peers`), add_peers(), _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m… (+11 more)

### Community 84 - "followup"
Cohesion: 0.18
Nodes (13): Did last week's calls work? (`push_rules.record_week`, `followup`), followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., Store this week's top actions under its Sunday. Re-running in the same week…, The most recent PREVIOUS week's calls and what happened since: sold/day since…, record_week(), week_start(), Last week's calls checked against what happened (lib/push_rules.followup), then… (+5 more)

### Community 85 - "self_made_combos.py"
Cohesion: 0.10
Nodes (24): _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…, Counted by how it was sold, _bag_sales_sql(), _bags_not_on_offer(), dow_tier_weeks() (+16 more)

### Community 86 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.29
Nodes (6): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does

### Community 87 - "F"
Cohesion: 0.17
Nodes (21): context(), not_moving(), A bag with stock that isn't clearing: cleared < 30% this month, or > 45 days of…, What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), build_reasons(), Adds notMoving + reasons to every row (lib/push_rules.reasons). Returns the… (+13 more)

### Community 88 - "history.py"
Cohesion: 0.24
Nodes (12): fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers…, Like _num, but leaves booleans alone and renders dates as ISO strings — the… (+4 more)

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.08
Nodes (20): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests, Agent skills — retail analytics, Test a skill (+12 more)

### Community 91 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.18
Nodes (12): Card component (base building block), dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), Signature Element — Flowing Border (achievement cards), high-end-visual-design (related skill), KPI Tile component, Page Structure Template (new dashboard page starting point) (+4 more)

### Community 92 - "build_actions"
Cohesion: 0.13
Nodes (17): Actions (one per bag × market, then ranked), moves(), posting_median(), rank(), {market: median postsMonth of the bags that were posted at all} — the 'below…, Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES… (+9 more)

### Community 93 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 94 - "timed_offers.py"
Cohesion: 0.11
Nodes (25): _bags_from_file(), _derive_month(), kenya_stock_by_bag(), load_config(), _name_sql(), _norm_offer(), _parse_colour(), timed_offers.py… (+17 more)

### Community 95 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 96 - "Bags on offer vs not on offer"
Cohesion: 0.20
Nodes (10): Bags on offer vs not on offer, Buckets, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Regenerate, Shop birthdays, Shop metrics (vs the Odoo revenue target) (+2 more)

### Community 97 - "update_np_weekly_history"
Cohesion: 0.29
Nodes (7): _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)., Ordinal among the month's perfect weeks (>=5 days in month), so the first FULL…, Snapshot each Sun–Sat week (sales, Kenya/Outside posts) into…, update_np_weekly_history()

### Community 98 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "new_products.py"
Cohesion: 0.22
Nodes (7): _base_colour(), _merge_rows_by_base_colour(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across…, _strip_colour_qualifiers()

### Community 101 - "_fetch_monthly_kenya"
Cohesion: 0.18
Nodes (14): _analyze_region(), _fetch_monthly_kenya(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), Monthly Kenya figures for the S1 KPI cards. MONTHLY_MARKETING_POST: sum col E…, MONTHLY_SALES: colour=A(0), product_name=B(1), MONTHLY_MARKETING_POST: colour=A(0), product_name=C(2) (+6 more)

### Community 102 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 104 - "_apply_receipt_offers"
Cohesion: 0.25
Nodes (6): _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region…, _region_goal(), _till_targets()

### Community 105 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 107 - "base_name"
Cohesion: 0.33
Nodes (7): base_name(), dispatch_by_product_shop(), _num(), The catalogue key for an Odoo product name: norm() without the "[REJECT]" tag…, {NORM(product): {SHOP: bags}} of POS bag sales in [start, end]; None if DB…, {NORM(product): {SHOP: bags distributed in}} from combined_distribution.sql's…, sales_by_product_shop()

### Community 109 - "test_share_targets.py"
Cohesion: 0.22
Nodes (11): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+3 more)

### Community 120 - "main"
Cohesion: 0.33
Nodes (6): build_facts(), _categories(), inject(), main(), {BAG: CATEGORY} from bag_tiers.csv (the Bags on offer menu's editable table)., Facts for every bag × market that has stock or sold in the window…

### Community 121 - "online"
Cohesion: 0.40
Nodes (5): Out of stock — call back, fixture, live(), online(), Lifetime {product: {shop: people}} from the WhatsApp channel only —…

### Community 122 - "family"
Cohesion: 0.67
Nodes (4): family(), _load(), _norm(), Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…

### Community 123 - "_load_combos_by_shop"
Cohesion: 0.67
Nodes (4): _load_combos_by_shop(), _from_file(), _nonempty(), Per-shop combo / power-deal view for the panel — built **live from Odoo** via…

### Community 124 - "shop-birthdays.md"
Cohesion: 0.13
Nodes (12): Design Tokens (colors, typography, spacing), Semantic color rules (green=good, amber=risk, red=critical, cyan=info), Analytics Dashboard specific rules (VISUAL_DENSITY: dense), Shop birthdays, Shop → opening date, Where it shows, Per-shop combo-button chips (red when < half best-in-region), Region colour palette (reference for Executive Dashboard) (+4 more)

### Community 125 - "test_stocks_picking.py"
Cohesion: 0.24
Nodes (6): Fold Odoo products into Category → Bag → Colour rows. sold: {name:…, rollup(), Tests for stocks_picking.py's pure logic (no Odoo). Run: python -m pytest…, test_rollup_folds_shades_and_counts_unmatched(), test_rollup_keeps_colour_with_only_older_sales(), test_rollup_sums_daily_series_per_colour()

### Community 126 - "odoo_tabs.py"
Cohesion: 0.12
Nodes (22): lib — shared data-access for the marketing dashboard (Postgres migration).…, _build(), catalog_rows(), default_window(), get_rows(), last_complete_week(), load_catalog(), offer_flags() (+14 more)

### Community 127 - "load_offers"
Cohesion: 0.17
Nodes (12): _kenya_offers(), load_offers(), _market_offers(), month_starts(), offer_tags(), prefix(), {bag: [tags]} for the bags on offer (others left out). offers: [(offer bag…, [(name, tags)] from the dashboard's on-offer source for the month… (+4 more)

### Community 128 - "Product (bag) targets"
Cohesion: 0.29
Nodes (6): No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 129 - "POSTING (SALES YIELDS FROM ACCURATE POSTING).py"
Cohesion: 0.14
Nodes (14): count_complete_weeks_in_month(), load_dead_thresholds(), _mkt_perfect_week_index(), _mkt_week_label(), _offer_bagtypes_by_region(), POSTING (SALES YIELDS FROM ACCURATE POSTING).py…, Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]. (+6 more)

### Community 130 - "_bg_jobs"
Cohesion: 0.22
Nodes (10): cache_resource, _bg_jobs(), _bg_rebuild(), work(), Seconds the last good `kind` rebuild of `lbl` took (any kind as a fallback),…, Background rebuilds shared by every session: label → job (see _bg_rebuild)., Rebuild `lbl` in the background. kind: "auto" (skipped if a rebuild was tried…, _rebuild_secs() (+2 more)

### Community 131 - "fallback_bag"
Cohesion: 0.40
Nodes (6): fallback_bag(), make_resolver(), resolve(), Bag type of a product the catalogue doesn't know: drop "(…)" and the trailing…, resolve(product name) -> (category, bag, colour family) or None when it isn't a…, test_fallback_bag_drops_colour_words()

### Community 132 - "load"
Cohesion: 0.18
Nodes (11): daily_series(), kenya_shop_sales_filter(), load(), periods(), SQL filter for the Kenya shop tills: not the Sinza / Uganda tills, not the…, {name: {date iso: n}} ×3 -> {name: {"s","n","r": {day index: n}}} (day index =…, The Marketing dashboard's periods (bags_on_offer._base_windows): Monthly = the…, Per market: rows + unmatched. None if Odoo is unreachable. (+3 more)

### Community 133 - "bucket"
Cohesion: 0.67
Nodes (3): bucket(), {name: {date iso: units}} -> {name: {"d7", "d28", "mtd"}} for the 7 / 28 days…, test_bucket_periods()

### Community 134 - "Stocks Picking (Redundancy rate) — every bag's colours side by side (Kenya · Sinza · Uganda)"
Cohesion: 0.18
Nodes (10): Inputs (read only), Marketing Bags For Shoot — Stock rate (the first section on the page), Other columns, Page, Periods and offer (one choice for the whole page), Signals (one per colour, first that fits), Stocks Picking (Redundancy rate) — every bag's colours side by side (Kenya · Sinza · Uganda), The number: redundancy rate (+2 more)

### Community 137 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

### Community 138 - "self_made_combos_bundle/lib/__init__.py"
Cohesion: 0.28
Nodes (6): lib — shared data-access for the marketing dashboard (Postgres migration).…, main(), month_window(), _query_ready(), monthly_sales.py — the current month's real bags sold, from Postgres. The…, First → last calendar day of the LIVE month (today's month; see…

### Community 139 - "Month-End Routine (doc)"
Cohesion: 0.12
Nodes (16): denri_mkt_timed_offer* Supabase tables, denri_mkt_combo_requests table, denri_mkt_combo_sales table, denri_mkt_self_made_summary table, denri_mkt_timed_offer_weeks table (week-by-week bags/day view), Month-End Routine (doc), Odoo pos_combo_request table (SELECT granted 2026-09-02), Windows Task Scheduler setup (monthly, day 1, ~06:00) (+8 more)

### Community 140 - "kenya_shop_codes"
Cohesion: 0.67
Nodes (3): kenya_shop_codes(), lib/stock's Kenya shop codes + the shops it doesn't list yet (Machakos, Nyeri)…, test_kenya_shop_codes_add_machakos_and_nyeri_once()

### Community 141 - "Bag targets October 2026_b78d9f88.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 142 - "moves_sql"
Cohesion: 0.67
Nodes (3): moves_sql(), MOVES_SQL for one market's shop location codes (lib/stock's allow-list)., test_moves_sql_uses_market_codes()

### Community 144 - "month_end.py (script)"
Cohesion: 0.25
Nodes (8): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), DENRI_REPORT_MONTH env var (pin target month), FINALIZED_MONTHS set (frozen-report guard), month_end.py (script), Phase 2 — restore the live view (unpinned), SUPABASE_DB_URL env var (Session Pooler connection string)

### Community 145 - "Shop Launch"
Cohesion: 0.29
Nodes (6): Config, Launch day, Marketing posts, Sales, Shop Launch, What the page shows

### Community 146 - "sum_shops"
Cohesion: 0.67
Nodes (3): {shop code: {name: on-hand}} -> {name: on-hand summed over the shops}, only…, sum_shops(), test_sum_shops_nets_each_product_over_the_shops()

### Community 147 - "Ralph task — "Out of stock — call back" demand per shop"
Cohesion: 0.25
Nodes (7): match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, Established facts (do not re-investigate), Every iteration, Periods (dates in Africa/Nairobi), Ralph task — "Out of stock — call back" demand per shop, Stopping

### Community 150 - "_page"
Cohesion: 0.33
Nodes (7): cache_data, _page(), inline(), The page HTML as the dashboard serves its pages: local scripts inlined (the…, _read(), _month_archived(), True when `key` is in Supabase (falls back to monthly_report_history.json). If…

### Community 152 - "stocks_picking_app.py"
Cohesion: 0.14
Nodes (16): fragment, html, _idle_check(), _job(), _page_age_secs(), stocks_picking_app.py — STOCKS PICKING (Redundancy rate) as its own Streamlit…, Start a rebuild unless one is running. kind: "manual" (Refresh) or "auto" (page…, Run script-only HTML in an invisible frame (same origin, so it can reach… (+8 more)

### Community 154 - "push_to_supabase.py"
Cohesion: 0.21
Nodes (11): dotenv, Phase 1 — archive the target month, main(), push_to_supabase.py — run the marketing migration against Supabase. Regenerates…, main(), month_block(), num(), q() (+3 more)

### Community 157 - "bag_classifier"
Cohesion: 0.19
Nodes (14): _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _load_bag_prices(), _norm_combo() (+6 more)

### Community 158 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 160 - "corporate_clients_from_db"
Cohesion: 0.40
Nodes (6): corporate_clients_from_db(), _months(), A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],…, Current month's corporate activity per client (quoted · invoiced · paid · sold)…, _txt()

### Community 162 - "test_sheet_reads.py"
Cohesion: 0.60
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 163 - "push_rules.py"
Cohesion: 0.14
Nodes (16): action(), _cover_txt(), _kind(), _n(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).…, (code, plain sentence, units at stake, confidence 0..1) for one bag × market.…, HANDBAG' → 'handbags', 'SCHOOL BAG' → 'school bags', 'SPORT' → 'sport bags', ''…, _times() (+8 more)

## Ambiguous Edges - Review These
- `August 2026 Monthly Report` → `Legacy dated report_YYYY_month.html archive pattern`  [AMBIGUOUS]
  report_2026_august.html · relation: conceptually_related_to
- `Reject Sale page (reject_sales.html)` → `Card entrance animation via CSS @keyframes + animation-fill-mode: both`  [AMBIGUOUS]
  .claude/skills/dashboard-design.md · relation: conceptually_related_to

## Knowledge Gaps
- **216 isolated node(s):** `The number: redundancy rate`, `Periods and offer (one choice for the whole page)`, `Other columns`, `Signals (one per colour, first that fits)`, `Page` (+211 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 917 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `August 2026 Monthly Report` and `Legacy dated report_YYYY_month.html archive pattern`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Reject Sale page (reject_sales.html)` and `Card entrance animation via CSS @keyframes + animation-fill-mode: both`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Current Performance (doc)` connect `forward_projections.py` to `self_made_combos_bundle/lib/__init__.py`, `datetime`, `Month-End Routine (doc)`, `Product / name matching (doc)`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `New Products Analytics (doc)` connect `Product / name matching (doc)` to `forward_projections.py`, `Dashboard Insights skill`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `run_query()` connect `run_query` to `tests/test_receipt_combos.py`, `check_connection`, `fetch`, `self_made_combos_bundle/lib/__init__.py`, `fetch_new_products_data`, `forward_projections.py`, `build_payload`, `build_payload`, `lib/db.py`, `_enrich_deals`, `corporate_clients_from_db`, `stock.py`, `chronos_train.py`, `_enrich_deals`, `fetch_posting_data`, `get_gspread_client`, `bag_quant.py`, `product_targets.py`, `_seasonality`, `_combo_button_usage`, `self_made_combos.py`, `_apply_receipt_offers`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **What connects `The number: redundancy rate`, `Periods and offer (one choice for the whole page)`, `Other columns` to the rest of the system?**
  _216 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `laya.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09803921568627451 - nodes in this community are weakly interconnected._