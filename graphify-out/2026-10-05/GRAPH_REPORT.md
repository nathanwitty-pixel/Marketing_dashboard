# Graph Report - Marketing_dashboard  (2026-10-05)

## Corpus Check
- 176 files · ~713,282 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .csv 8, (none) 2, .toml 1)

## Summary
- 1999 nodes · 3585 edges · 147 communities (129 shown, 18 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 167 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bad955c9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- fetch_posting_data
- bag_quant.py
- datetime
- POSTING (SALES YIELDS FROM ACCURATE POSTING).py
- Offer Picking Dashboard Page
- generate_insights.py
- Kitengela Rejects tracker (timed offer)
- monthly_report.py
- shops_efficiency.py
- oos_callbacks.py
- reject_variants
- current_performance.py
- odoo_tabs.py
- lib/db.py
- push_planner.py
- check_connection
- self_made_combos_bundle/lib/report_month.py
- forward_projections.py
- build_payload
- main.py
- build_payload
- Dashboard Insights skill
- Bags on offer vs not on offer
- Product / name matching (doc)
- v5_theme.js
- self_made_combos_bundle/self_made_combos.py
- fetch
- Dashboard Menu Docs (spec index)
- Self-made combos vs running combos (doc)
- _enrich_deals
- oos_chip.js
- Sidebar Navigation (icon rail / expanded drawer)
- streamlit_app.py
- Marketing Dashboard Insights Page
- design-taste-frontend (anti-slop frontend skill)
- new_products.py
- lib/report_month.py
- offer_picking.py
- theme.py
- Shops Efficiency Tracking spec doc
- August 2026 Monthly Report
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
- json
- scripts/test_receipt_combos.py
- _combo_norm_option
- algorithmic-art skill
- dataviz-charts skill
- July 2026 Monthly Report Page
- laya.py
- queries.py
- High-End Visual Design skill
- run_query
- month_end.py
- build
- daydream skill (Vault Daydream)
- start_server
- render(idx) function
- _combo_button_usage
- buildExportDoc(mode) function
- TTL disk-cache rationale (.odoo_cache/)
- perf_data.js
- attachPopover(cardId, popId) function
- product_targets.py
- welcome_screen.js
- _bags_not_on_offer
- get_gspread_client
- shop_birthdays.py
- current_performance.html
- _build_sheet_slots
- publish.py
- colours.py
- _combo_button_usage
- push_laya.py
- push_to_supabase.py
- facts
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- self_made_combos.py
- Chart type switcher (every chart, every menu)
- test_push_planner.py
- moves
- test_stockout_demand.py
- Out-of-stock demand — people, not requests
- os
- push_rules.py
- marketing_dashboard.sql
- monthly_sales.py
- Ralph task — deals from the posters (deals_kenya.csv)
- _post_yield
- signals
- attach
- Bag Signals — quant view of each bag (posting · stock · selling)
- timed_offers.html (output)
- google_auth.py (shared auth module)
- page_sidebar.js
- sys
- Ralph task — only three sheet tabs left
- _fetch_monthly_kenya
- Product (bag) targets
- streamlit_components_v1
- _dead_clear
- bags_on_offer.py
- _seasonality
- bag_classifier
- Denri Africa Dashboard Design System (skill)
- shop_bday.js
- shop-birthdays.md
- timed_offers.py
- Marketing Dashboard — Google Sheets access & setup (doc)
- _dead_stock_region
- self_made_combos_bundle/lib/__init__.py
- supabase_migration.py
- OOS call-back progress (Ralph loop log)
- _alignment_region
- reject_sales.py
- Month-End Routine (doc)
- base_name
- self_made_combos.py
- get_rows
- followup
- Bag targets October 2026_b78d9f88.md
- timed_offers.py (generator)
- _aliases
- _read_offers
- parse_sheet
- _bag_tiers

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 42 edges
2. `fetch()` - 33 edges
3. `fetch_posting_data()` - 32 edges
4. `build_payload()` - 30 edges
5. `check_connection()` - 27 edges
6. `get_gspread_client()` - 25 edges
7. `build_payload()` - 24 edges
8. `F()` - 22 edges
9. `Self-made combos vs running combos (doc)` - 22 edges
10. `Dashboard Menu Docs (spec index)` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Buckets` --references--> `bag_classifier()`  [INFERRED]
  docs/bags-on-offer.md → self_made_combos.py
- `Counted by how it was sold` --references--> `bag_classifier()`  [INFERRED]
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

## Communities (147 total, 18 thin omitted)

### Community 0 - "fetch_posting_data"
Cohesion: 0.20
Nodes (19): _build_no_convert(), fetch_posting_data(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int(), _is_checked() (+11 more)

### Community 1 - "bag_quant.py"
Cohesion: 0.10
Nodes (27): build(), _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), action(), bag_posts() (+19 more)

### Community 2 - "datetime"
Cohesion: 0.09
Nodes (38): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+30 more)

### Community 3 - "POSTING (SALES YIELDS FROM ACCURATE POSTING).py"
Cohesion: 0.14
Nodes (14): count_complete_weeks_in_month(), load_dead_thresholds(), _mkt_perfect_week_index(), _mkt_week_label(), _offer_bagtypes_by_region(), POSTING (SALES YIELDS FROM ACCURATE POSTING).py…, Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]. (+6 more)

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
Nodes (45): _bags_on_offer(), _block(), build_extras(), _deals(), _pick(), _posting(), _posting_block(), region() (+37 more)

### Community 8 - "shops_efficiency.py"
Cohesion: 0.10
Nodes (19): pathlib, apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _load_combos_by_shop(), _from_file(), _nonempty() (+11 more)

### Community 9 - "oos_callbacks.py"
Cohesion: 0.06
Nodes (49): fixture, lib — shared data-access for the marketing dashboard (Postgres migration).…, aggregate(), attach_stock(), collect(), _in(), load_rows(), oos_by_bag_shop() (+41 more)

### Community 10 - "reject_variants"
Cohesion: 0.17
Nodes (13): kenya_stock_by_bag(), _parse_colour(), {BAG_UPPER: category} — the bag's category label only, from the product…, {BAG_UPPER: units} — physical stock summed per BAG TYPE from a repo CSV's UNITS…, First primary colour token found in a name (longest-first), Title-cased; '' if…, Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share…, Per-[REJECT]-product variant rows for a name-filtered offer, for the filterable…, {BAG_UPPER: {stock, category}} for the configured bags. STOCK is LIVE Kenya… (+5 more)

### Community 11 - "current_performance.py"
Cohesion: 0.10
Nodes (14): _db_count(), monthly_from_db(), current_performance.py…, Reporting month's subset count (e.g. rejectBags, giftBags) from…, Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,… (+6 more)

### Community 12 - "odoo_tabs.py"
Cohesion: 0.14
Nodes (21): _build(), build_rows(), catalog_rows(), _Deriver, _flag_cells(), _fmt(), load_catalog(), norm() (+13 more)

### Community 13 - "lib/db.py"
Cohesion: 0.06
Nodes (44): dotenv, check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME… (+36 more)

### Community 14 - "push_planner.py"
Cohesion: 0.12
Nodes (24): build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), load_data(), main() (+16 more)

### Community 15 - "check_connection"
Cohesion: 0.12
Nodes (22): corporate_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, _corporate_bags(), Corporate bags sold in the given month, live from Odoo invoices. Returns 0 when…, check_connection(), run_query with a TTL disk cache. Identical to run_query for callers, but a…, (ok, detail). Never raises — the callers show `detail` in the UI., run_query_cached() (+14 more)

### Community 16 - "self_made_combos_bundle/lib/report_month.py"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 17 - "forward_projections.py"
Cohesion: 0.17
Nodes (8): calendar, odoo_weekly_breakdown(), _perfect_week_index(), forward_projections.py…, Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, update_weekly_history(), _week_start()

### Community 18 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 19 - "main.py"
Cohesion: 0.10
Nodes (24): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the… (+16 more)

### Community 20 - "build_payload"
Cohesion: 0.13
Nodes (18): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+10 more)

### Community 21 - "Dashboard Insights skill"
Cohesion: 0.17
Nodes (16): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Current Performance Dashboard Page, Forward Projections section, PERF data block (weekly/monthly sales KPIs), PROJ data block (forward projections, velocity factor, bare minimum), Monthly Report (doc) (+8 more)

### Community 22 - "Bags on offer vs not on offer"
Cohesion: 0.20
Nodes (10): Bags on offer vs not on offer, Buckets, Counted by how it was sold, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Regenerate, Shop birthdays (+2 more)

### Community 23 - "Product / name matching (doc)"
Cohesion: 0.18
Nodes (14): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix) (+6 more)

### Community 24 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 25 - "self_made_combos_bundle/self_made_combos.py"
Cohesion: 0.20
Nodes (11): fetch(), fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py…, Read the Shop → Region table from docs/shop-regions.md so the mapping can be…, Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer… (+3 more)

### Community 26 - "fetch"
Cohesion: 0.14
Nodes (22): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), make_classifier(), base() (+14 more)

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
Cohesion: 0.33
Nodes (6): chip(), close(), esc(), open(), seg(), shopItem()

### Community 31 - "Sidebar Navigation (icon rail / expanded drawer)"
Cohesion: 0.16
Nodes (14): insights.html, Live view vs archive split (lib/report_month.py live_*), Denri Africa · Marketing Dashboard (README, project overview), dash-frame iframe (dashboard content loader), exportExcel() function, history.html (nav target — Reporting History, Supabase), insights.html (nav target), Marketing Dashboard Shell (shell.html) (+6 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.08
Nodes (15): cache_data, SCRIPT_TIMEOUT = 600s config, hashlib, html, streamlit, _load_secrets_into_env(), _month_archived(), _month_end_running() (+7 more)

### Community 33 - "Marketing Dashboard Insights Page"
Cohesion: 0.13
Nodes (15): Menu 1: Current Performance, Bare Minimum (Bags to be Sold) KPI, Bare Minimum (Growth %) KPI, Declined By KPI (bags missed that week), Forecasted Projection KPI (with corporate in mind), Forward Projections Page, PROJ_DATA_START/PROJ_DATA_END injected JSON data block, Standard Projection KPI (% of Total Target) (+7 more)

### Community 34 - "design-taste-frontend (anti-slop frontend skill)"
Cohesion: 0.18
Nodes (12): design-taste-frontend (related skill), design-taste-frontend (anti-slop frontend skill), Brief-First Process (8-step design workflow), Hard Bans (typography, color, layout, code, content clichés), Pre-Flight Checklist (90+ items), Redesign Protocol (upgrading existing UI), Three Dials — DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, Three AI-generated design clusters (calibration reference) (+4 more)

### Community 35 - "new_products.py"
Cohesion: 0.05
Nodes (47): lib, names(), lib/new_products_list.py — which bag types count as this month's NEW PRODUCTS.…, Upper-cased bag types from new_products.txt in file order ([] = use the sheet…, _base_colour(), fetch_new_products_data(), _apply_stock(), _post_lookup() (+39 more)

### Community 36 - "lib/report_month.py"
Cohesion: 0.19
Nodes (17): anchor(), is_pinned(), live_anchor(), live_month_key(), month_key(), month_name(), month_window(), _pinned() (+9 more)

### Community 37 - "offer_picking.py"
Cohesion: 0.15
Nodes (15): _apply_alias(), _build_catalog(), _is_full_price(), _next_month(), offer_picking.py…, {BAG (upper): official full price} from bag_original_prices.json (fallback)., Save a local, human-editable copy of the offers prices to OFFERS_CACHE., Resolve any bag wording → (canonical BOM bag type, cost or None, in_bom).… (+7 more)

### Community 38 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "August 2026 Monthly Report"
Cohesion: 0.33
Nodes (6): August 2026 Monthly Report, New Products Section (Report), Offer Type Analysis Section (Report), Posting Yields Section (Report), monthly_report.html (nav target), POSTING (SALES YIELDS FROM ACCURATE POSTING).html (nav target)

### Community 41 - "_enrich_deals"
Cohesion: 0.16
Nodes (9): _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,… (+1 more)

### Community 42 - "chart_switcher.js"
Cohesion: 0.21
Nodes (21): alpha(), apply(), attach(), axisOpts(), build(), Chart(), clone(), closeMenu() (+13 more)

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

### Community 51 - "json"
Cohesion: 0.19
Nodes (14): One-off: restore August's Offer Type figures into monthly_report_history.json…, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers… (+6 more)

### Community 52 - "scripts/test_receipt_combos.py"
Cohesion: 0.08
Nodes (42): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+34 more)

### Community 53 - "_combo_norm_option"
Cohesion: 0.38
Nodes (6): _combo_norm_option(), combos_by_shop(), _norm(), _tokmatch(), Per-shop view for Shops Efficiency, keyed by shop-location label (e.g.…, One combo slot-option → its distinctive bag token(s), colours/category words…

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.29
Nodes (7): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.)

### Community 56 - "July 2026 Monthly Report Page"
Cohesion: 0.18
Nodes (12): What Needs Attention Section, Finding: Uganda marketing conversion at 7.4%, below critical threshold, Finding: 5,572 bags in stock not posted, 53% of stock invisible, Section 1: Current Performance, July 2026 Monthly Report Page, Section 2: New Products, Section 3: Offer Type Analysis, Section 4: Posting Yields (Sales from Accurate Posting) (+4 more)

### Community 57 - "laya.py"
Cohesion: 0.10
Nodes (26): Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket(), _cache_get(), _cache_put() (+18 more)

### Community 58 - "queries.py"
Cohesion: 0.11
Nodes (17): fetch_monthly_target(), fetch_sheet_data(), load(), (daily, total, stock, launch, start, end) for Kenya from Odoo; daily per bag…, excluded_products(), master_products(), _norm_name(), lib/queries.py — SQL for the Litmus Postgres source of truth (Odoo POS). Bags… (+9 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "run_query"
Cohesion: 0.20
Nodes (11): _drop_shared_conn(), DataFrame, Run a read query and return a DataFrame, or None if the DB is unreachable.…, run_query(), _bags_not_on_offer(), _kenya_till_targets(), Bags with sales this month (in the market `sql` scopes to) that are on NO…, {prev, cur} for Kenya: the Kenya tills' Odoo monthly POS targets (every till… (+3 more)

### Community 61 - "month_end.py"
Cohesion: 0.31
Nodes (8): clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.…, YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that…, After the closing month's timed offers are safely in Supabase, empty the config…, run(), target_month(), subprocess

### Community 62 - "build"
Cohesion: 0.22
Nodes (11): _alt_cost(), build(), _combo_cost(), _combo_slots(), {BAG TYPE (upper): production cost} from bom_costs.json — the local copy of the…, Parse `const SMC = {…}` out of self_made_combos.html (no DB round-trip)., One combo alternative (e.g. 'Amaya Handbag') → its BOM production cost., Combo name → list of slots, each a list of alternative strings. (+3 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "start_server"
Cohesion: 0.31
Nodes (9): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_refresh(), _handle_to_config() (+1 more)

### Community 65 - "render(idx) function"
Cohesion: 0.50
Nodes (4): buildCharts(m, wk, prevM) function, render(idx) function, selfMadeHtml(m) function, timedOffersHtml(m) function

### Community 66 - "_combo_button_usage"
Cohesion: 0.22
Nodes (8): _combo_button_usage(), _combo_norm_option(), _combo_odoo_slots(), _matches_sheet(), One combo slot-option → its distinctive bag token(s), colours/category words…, Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…, The sheet label this Odoo combo maps to (same slot count, every slot overlaps),…, Per running combo: units rung through the combo button (Odoo) vs the sheet's…

### Community 67 - "buildExportDoc(mode) function"
Cohesion: 0.50
Nodes (4): buildExportDoc(mode) function, colorizeForPaper() function, exportPDF() function, exportWord() function

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 71 - "product_targets.py"
Cohesion: 0.11
Nodes (28): allocate(), available_days(), bag_key_fn(), key(), base_period(), build(), load_targets(), monthly_target_rows() (+20 more)

### Community 73 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 74 - "get_gspread_client"
Cohesion: 0.15
Nodes (17): get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked() (+9 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "current_performance.html"
Cohesion: 0.40
Nodes (5): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance), current_performance.html (nav target)

### Community 77 - "_build_sheet_slots"
Cohesion: 0.50
Nodes (4): _build_sheet_slots(), _combo_sheet_slots(), Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]., [(label, slots)] for each running combo on the offer sheet (skips the TOTAL…

### Community 78 - "publish.py"
Cohesion: 0.23
Nodes (13): argparse, fnmatch, changed_files(), git(), group(), is_secret(), main(), publish.py — one-click, VERIFIED publish of the dashboard to GitHub (Streamlit… (+5 more)

### Community 79 - "colours.py"
Cohesion: 0.43
Nodes (6): collections, family(), _load(), _norm(), lib/colours.py — colour FAMILY of a product (Brown, Black, Red, Beige, Grey,…, Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…

### Community 80 - "_combo_button_usage"
Cohesion: 0.14
Nodes (11): Inputs (from the user, Oct 2026), Ralph task — Sinza & Uganda offers + receipt-based combo counting, Steps, _combo_button_usage(), _matches_sheet(), _opt_close(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Two normalised slot options name the same bag, loosely: equal ignoring spaces… (+3 more)

### Community 81 - "push_laya.py"
Cohesion: 0.14
Nodes (19): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+11 more)

### Community 82 - "push_to_supabase.py"
Cohesion: 0.25
Nodes (7): denri_mkt_timed_offer* Supabase tables, _collect_comments() (pulls prose from rendered report), denri_mkt_monthly.comments (jsonb list), denri_mkt_timed_offer_weeks table (week-by-week bags/day view), psycopg2, main(), push_to_supabase.py — run the marketing migration against Supabase. Regenerates…

### Community 83 - "facts"
Cohesion: 0.15
Nodes (18): Per bag × market: the facts (`push_rules.facts`, `add_peers`), add_peers(), _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), ISO date n days before END (0 = END). (+10 more)

### Community 84 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

### Community 85 - "self_made_combos.py"
Cohesion: 0.12
Nodes (21): _load_source(), bags_offer_source.json if written in the last 15 min for this month (and it has…, _bag_sales_daily_sql(), _bag_sales_sql(), dow_tier_weeks(), fetch(), fmt(), inject() (+13 more)

### Community 86 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.33
Nodes (5): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), What it does

### Community 87 - "test_push_planner.py"
Cohesion: 0.16
Nodes (25): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m…, A facts row with sensible defaults, overridden by kw. (+17 more)

### Community 88 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.08
Nodes (20): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests, Agent skills — retail analytics, Test a skill (+12 more)

### Community 91 - "os"
Cohesion: 0.24
Nodes (8): build_all.py ────────────────────────────────────────────────────────────────…, Current Performance (doc), os, Current Performance Section (Report), Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 92 - "push_rules.py"
Cohesion: 0.13
Nodes (17): action(), _cover_txt(), _kind(), _n(), not_moving(), posting_median(), rank(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).… (+9 more)

### Community 93 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 94 - "monthly_sales.py"
Cohesion: 0.16
Nodes (12): DENRI_REPORT_MONTH env var (pin target month), FINALIZED_MONTHS set (frozen-report guard), month_end.py (script), Phase 1 — archive the target month, Phase 2 — restore the live view (unpinned), SUPABASE_DB_URL env var (Session Pooler connection string), main(), month_window() (+4 more)

### Community 95 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 96 - "_post_yield"
Cohesion: 0.25
Nodes (6): _onoff(), _bt_on_offer(), _yield(), _post_yield(), Marketing & Sales Alignment — posting yield, measured the way marketing…, Is this bag type on offer, matched against the Self-Made-Combos offer set with…

### Community 97 - "signals"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

### Community 98 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "timed_offers.html (output)"
Cohesion: 0.40
Nodes (5): renderOffer(TO, root) function, timed_offers.html (output), /api/refresh endpoint, reloadFrame() function, SCRIPT_MAP (dashboard filename to generator script map)

### Community 101 - "google_auth.py (shared auth module)"
Cohesion: 0.25
Nodes (8): google_auth.py (shared auth module), google_credentials.json (OAuth desktop client), google_token.json (OAuth token), main.py (refresh + serve dashboard), OAuth token expiry issue (Testing mode, ~7 day expiry), reauth.py (re-login script), service_account.json (recommended, permanent auth), Service account chosen for zero-maintenance auth + enabling in-dashboard Refresh

### Community 102 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 104 - "sys"
Cohesion: 0.20
Nodes (9): Deals from posters (RALPH_DEALS.md) — 2026-10-04, _local_deal_rows(), Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), sys, Tests for the poster-sourced deals (deals_kenya.csv →…, test_month_not_in_csv_has_no_deals_and_no_sheet_read() (+1 more)

### Community 105 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 107 - "_fetch_monthly_kenya"
Cohesion: 0.17
Nodes (16): _analyze_region(), _fetch_monthly_kenya(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), Monthly Kenya figures for the S1 KPI cards. MONTHLY_MARKETING_POST: sum col E…, MONTHLY_SALES: colour=A(0), product_name=B(1) (+8 more)

### Community 109 - "Product (bag) targets"
Cohesion: 0.29
Nodes (6): No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 121 - "_dead_clear"
Cohesion: 0.29
Nodes (5): _dead_clear(), _clear(), {catalogue name: net units moved INTO the region's shops on/after `since`} from…, Dead-stock clearance for ONE region and ONE period, posted vs not posted × on…, _region_net_moves()

### Community 122 - "bags_on_offer.py"
Cohesion: 0.10
Nodes (21): _base_windows(), _build_period(), _custom_range(), fmt(), inject(), main(), _new_products(), _offer_types() (+13 more)

### Community 123 - "_seasonality"
Cohesion: 0.29
Nodes (8): Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), _combo_odoo_slots(), _combo_sheet_slots(), Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]., Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…

### Community 124 - "bag_classifier"
Cohesion: 0.15
Nodes (14): _add_oos(), _apply_receipt_offers(), bag_classifier(), infer(), _norm(), _load_bag_prices(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;… (+6 more)

### Community 125 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.18
Nodes (12): Card component (base building block), dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), Signature Element — Flowing Border (achievement cards), high-end-visual-design (related skill), KPI Tile component, Page Structure Template (new dashboard page starting point) (+4 more)

### Community 126 - "shop_bday.js"
Cohesion: 0.52
Nodes (6): badge(), esc(), key(), ordinal(), short(), strip()

### Community 127 - "shop-birthdays.md"
Cohesion: 0.18
Nodes (8): Design Tokens (colors, typography, spacing), Semantic color rules (green=good, amber=risk, red=critical, cyan=info), Analytics Dashboard specific rules (VISUAL_DENSITY: dense), Shop birthdays, Shop → opening date, Where it shows, Region colour palette (reference for Executive Dashboard), Shops & Regions (doc — source of truth)

### Community 128 - "timed_offers.py"
Cohesion: 0.12
Nodes (17): _bags_from_file(), build_offer(), _derive_month(), load_config(), _name_sql(), _norm_offer(), _price_sql(), timed_offers.py… (+9 more)

### Community 129 - "Marketing Dashboard — Google Sheets access & setup (doc)"
Cohesion: 0.29
Nodes (7): timed_offers_config.json (config), Vercel hosted version (static snapshot), Secrets excluded via .gitignore / .vercelignore, Marketing Dashboard — Google Sheets access & setup (doc), Timed Offers snapshot-over-window workflow, vercel.json, Vercel static deployment (serves committed HTML, no build step)

### Community 130 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 131 - "self_made_combos_bundle/lib/__init__.py"
Cohesion: 0.25
Nodes (6): lib — shared data-access for the marketing dashboard (Postgres migration).…, openpyxl, openpyxl_comments, openpyxl_styles, openpyxl_utils, product_targets_workbook.py — the month's bag targets as an Excel workbook with…

### Community 132 - "supabase_migration.py"
Cohesion: 0.36
Nodes (7): main(), month_block(), num(), q(), supabase_migration.py — export the marketing dashboard's monthly data to a SQL…, SQL string literal (or NULL)., SQL numeric literal (or NULL). Ints print without a trailing .0.

### Community 133 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.29
Nodes (6): Blocker counter, Final summary, Log, OOS call-back progress (Ralph loop log), Sheets cut to three tabs (RALPH_SHEETS.md) — 2026-10-04, Sinza & Uganda (RALPH_OUTSIDE.md) — 2026-10-04

### Community 134 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 135 - "reject_sales.py"
Cohesion: 0.17
Nodes (15): csv, _assign_price(), _bom_costs(), build(), _category_of(), _norm_cat(), reject_stock.csv → {BAG (upper): {units, colours:{COLOUR: units}}}., (price, flag) from BOM cost — two tiers. flag ∈ {'', 'thin', 'below', 'nobom'}. (+7 more)

### Community 136 - "Month-End Routine (doc)"
Cohesion: 0.29
Nodes (7): denri_mkt_combo_requests table, denri_mkt_combo_sales table, denri_mkt_self_made_summary table, Month-End Routine (doc), Odoo pos_combo_request table (SELECT granted 2026-09-02), Windows Task Scheduler setup (monthly, day 1, ~06:00), Legacy dated report_YYYY_month.html archive pattern

### Community 137 - "base_name"
Cohesion: 0.25
Nodes (9): base_name(), dispatch_by_product_shop(), _num(), The catalogue key for an Odoo product name: norm() without the "[REJECT]" tag…, {NORM(product): {SHOP: bags}} of POS bag sales in [start, end]; None if DB…, {NORM(product): {SHOP: bags distributed in}} from combined_distribution.sql's…, {NORM(product): {SHOP: on-hand}} live, Kenya shops + Sinza (DAR) + Uganda (UG)., sales_by_product_shop() (+1 more)

### Community 138 - "self_made_combos.py"
Cohesion: 0.50
Nodes (4): Per-shop combo-button chips (red when < half best-in-region), self_made_combos.py, Shop -> Region table, self_made_combos.html (nav target)

### Community 139 - "get_rows"
Cohesion: 0.22
Nodes (9): default_window(), get_rows(), last_complete_week(), date, The most recent COMPLETE Sun–Sat week before `ref` (today) — what the sheet's…, Sheet-shaped rows for `tab` built from Odoo, or None when Postgres is…, The tab's rows in the sheet's layout, built from Odoo. No sheet fallback (Oct…, tab_rows() (+1 more)

### Community 140 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 141 - "Bag targets October 2026_b78d9f88.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 142 - "timed_offers.py (generator)"
Cohesion: 0.33
Nodes (6): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), Timed Offers Analytics (doc), timed_offers.py (generator), Timed Offers Section — Back to School Edition (Report)

### Community 143 - "_aliases"
Cohesion: 0.33
Nodes (6): _aliases(), odoo_name(), {NORM(odoo name): NORM(sheet name)} from product_aliases.csv — products Odoo…, Odoo's spelling of a catalogue name (the reverse of product_aliases.csv), for…, _odoo_colour(), The colour as the product itself is named — the product name minus its bag…

### Community 144 - "_read_offers"
Cohesion: 0.40
Nodes (5): Offer type summary (matrix), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, _read_offers(), _read_offers_cache()

### Community 145 - "parse_sheet"
Cohesion: 0.40
Nodes (3): parse_sheet(), Return (data, meta) for the Kenya shops, locating columns by header name…, safe_int()

### Community 146 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

## Ambiguous Edges - Review These
- `Legacy dated report_YYYY_month.html archive pattern` → `August 2026 Monthly Report`  [AMBIGUOUS]
  report_2026_august.html · relation: conceptually_related_to
- `Reject Sale page (reject_sales.html)` → `Card entrance animation via CSS @keyframes + animation-fill-mode: both`  [AMBIGUOUS]
  .claude/skills/dashboard-design.md · relation: conceptually_related_to

## Knowledge Gaps
- **202 isolated node(s):** `Period selector (Monthly / Weekly / Last week / Custom)`, `What the page shows (per period)`, `Laptop sleeves are bags (27 Sep 2026)`, `Shop metrics (vs the Odoo revenue target)`, `Shop birthdays` (+197 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 826 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Legacy dated report_YYYY_month.html archive pattern` and `August 2026 Monthly Report`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Reject Sale page (reject_sales.html)` and `Card entrance animation via CSS @keyframes + animation-fill-mode: both`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Current Performance (doc)` connect `os` to `current_performance.py`, `forward_projections.py`, `Product / name matching (doc)`, `queries.py`, `monthly_sales.py`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `New Products Analytics (doc)` connect `Product / name matching (doc)` to `os`, `Dashboard Insights skill`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `Sidebar Navigation (icon rail / expanded drawer)` connect `Sidebar Navigation (icon rail / expanded drawer)` to `August 2026 Monthly Report`, `self_made_combos.py`, `current_performance.html`, `Kitengela Rejects tracker (timed offer)`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `fetch()` (e.g. with `classify()` and `oos_key()`) actually correct?**
  _`fetch()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Period selector (Monthly / Weekly / Last week / Custom)`, `What the page shows (per period)`, `Laptop sleeves are bags (27 Sep 2026)` to the rest of the system?**
  _202 weakly-connected nodes found - possible documentation gaps or missing edges._