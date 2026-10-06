# Graph Report - Marketing_dashboard  (2026-10-06)

## Corpus Check
- 176 files · ~717,185 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: .csv 8, (none) 2, .toml 1)

## Summary
- 2000 nodes · 3584 edges · 156 communities (137 shown, 19 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 167 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bec20fd1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- fetch_posting_data
- bag_quant.py
- tests/test_receipt_combos.py
- POSTING (SALES YIELDS FROM ACCURATE POSTING).py
- Offer Picking Dashboard Page
- generate_insights.py
- Kitengela Rejects tracker (timed offer)
- monthly_report.py
- shops_efficiency.py
- supabase_migration.py
- reject_variants
- datetime
- odoo_tabs.py
- self_made_combos_bundle/lib/db.py
- push_planner.py
- timed_offers.py
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
- history.py
- scripts/test_receipt_combos.py
- Month-End Routine (doc)
- algorithmic-art skill
- dataviz-charts skill
- July 2026 Monthly Report Page
- laya.py
- queries.py
- High-End Visual Design skill
- run_query
- month_end.py
- load_rows
- daydream skill (Vault Daydream)
- test_oos_callbacks.py
- render(idx) function
- _combo_button_usage
- buildExportDoc(mode) function
- TTL disk-cache rationale (.odoo_cache/)
- perf_data.js
- attachPopover(cardId, popId) function
- live_month_window
- welcome_screen.js
- _bags_not_on_offer
- offer_data.py
- shop_birthdays.py
- current_performance.html
- _build_sheet_slots
- publish.py
- sys
- _combo_button_usage
- push_laya.py
- google_auth.py (shared auth module)
- test_push_planner.py
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- self_made_combos.py
- Chart type switcher (every chart, every menu)
- F
- moves
- test_stockout_demand.py
- Bag signals — quant finance applied to product sales
- test_product_targets.py
- push_rules.py
- marketing_dashboard.sql
- Phase 1 — archive the target month
- Ralph task — deals from the posters (deals_kenya.csv)
- _post_yield
- signals
- attach
- Bag Signals — quant view of each bag (posting · stock · selling)
- load_config
- push_to_supabase.py
- page_sidebar.js
- monthly_target_rows
- Ralph task — only three sheet tabs left
- _fetch_monthly_kenya
- bag_classifier
- streamlit_components_v1
- _dead_clear
- bags_on_offer.py
- test_sheet_reads.py
- reject_sales.py
- Denri Africa Dashboard Design System (skill)
- shop_bday.js
- shop-birthdays.md
- os
- _build_period
- _dead_stock_region
- self_made_combos_bundle/lib/__init__.py
- re
- timed_offers.py (generator)
- _alignment_region
- oos_callbacks.py
- Marketing Dashboard — Google Sheets access & setup (doc)
- _combo_norm_option
- self_made_combos.py
- lib/db.py
- followup
- Bag targets October 2026_b78d9f88.md
- build
- Laya
- Combos from receipts — running vs self-made
- update_np_weekly_history
- scripts/receipt_combos.py
- Out-of-stock demand — people, not requests
- Product (bag) targets
- OOS call-back progress (Ralph loop log)
- _seasonality
- Sales-share targets per product
- _read_offers
- Answer
- _month_archived
- _kind

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 41 edges
2. `fetch()` - 33 edges
3. `fetch_posting_data()` - 32 edges
4. `build_payload()` - 29 edges
5. `get_gspread_client()` - 27 edges
6. `check_connection()` - 27 edges
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

## Communities (156 total, 19 thin omitted)

### Community 0 - "fetch_posting_data"
Cohesion: 0.20
Nodes (19): _build_no_convert(), fetch_posting_data(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int(), _is_checked() (+11 more)

### Community 1 - "bag_quant.py"
Cohesion: 0.12
Nodes (26): build(), action(), bag_posts(), tally(), load(), _mean(), _phi(), posting_beta() (+18 more)

### Community 2 - "tests/test_receipt_combos.py"
Cohesion: 0.13
Nodes (27): csv, lib — shared data-access for the marketing dashboard (Postgres migration).…, bag_key(), classify(), _fits(), load_offers(), market_summary(), lib/receipt_combos.py — Sinza & Uganda combos counted from POS receipts. Those… (+19 more)

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
Cohesion: 0.06
Nodes (40): _bags_on_offer(), build_extras(), _deals(), _pick(), _posting(), _posting_block(), region(), lib/month_extras.py — the newer pages' figures, kept in each month's History… (+32 more)

### Community 8 - "shops_efficiency.py"
Cohesion: 0.05
Nodes (38): build_period(), distributed_in(), main(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only., Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).… (+30 more)

### Community 9 - "supabase_migration.py"
Cohesion: 0.36
Nodes (7): main(), month_block(), num(), q(), supabase_migration.py — export the marketing dashboard's monthly data to a SQL…, SQL string literal (or NULL)., SQL numeric literal (or NULL). Ints print without a trailing .0.

### Community 10 - "reject_variants"
Cohesion: 0.16
Nodes (15): _bucket(), kenya_stock_by_bag(), _parse_colour(), Which configured bag (if any) an Odoo/​sheet product name belongs to, by…, {BAG_UPPER: category} — the bag's category label only, from the product…, {BAG_UPPER: units} — physical stock summed per BAG TYPE from a repo CSV's UNITS…, First primary colour token found in a name (longest-first), Title-cased; '' if…, Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share… (+7 more)

### Community 11 - "datetime"
Cohesion: 0.11
Nodes (13): calendar, current_performance.py…, Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary(), week_start_of(), weekly_from_db() (+5 more)

### Community 12 - "odoo_tabs.py"
Cohesion: 0.06
Nodes (50): collections, family(), _load(), _norm(), lib/colours.py — colour FAMILY of a product (Brown, Black, Red, Beige, Grey,…, Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…, _aliases(), base_name() (+42 more)

### Community 13 - "self_made_combos_bundle/lib/db.py"
Cohesion: 0.13
Nodes (20): dotenv, check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME… (+12 more)

### Community 14 - "push_planner.py"
Cohesion: 0.10
Nodes (28): _block(), The JSON object in `const NAME = {...};` of a generated page, or None., names(), Upper-cased bag types from new_products.txt in file order ([] = use the sheet…, build_actions(), build_facts(), build_reasons(), _categories() (+20 more)

### Community 15 - "timed_offers.py"
Cohesion: 0.11
Nodes (24): check_connection(), run_query with a TTL disk cache. Identical to run_query for callers, but a…, (ok, detail). Never raises — the callers show `detail` in the UI., run_query_cached(), build_offer(), _name_sql(), odoo_bag_daily_value(), odoo_bag_prices() (+16 more)

### Community 16 - "self_made_combos_bundle/lib/report_month.py"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 17 - "forward_projections.py"
Cohesion: 0.13
Nodes (11): build_all.py ────────────────────────────────────────────────────────────────…, Current Performance (doc), odoo_weekly_breakdown(), _perfect_week_index(), forward_projections.py…, Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, update_weekly_history() (+3 more)

### Community 18 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 19 - "main.py"
Cohesion: 0.09
Nodes (31): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the… (+23 more)

### Community 20 - "build_payload"
Cohesion: 0.15
Nodes (16): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+8 more)

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
Cohesion: 0.13
Nodes (23): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), make_classifier(), base() (+15 more)

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
Nodes (15): contextlib, SCRIPT_TIMEOUT = 600s config, html, streamlit, game_loading(), _load_secrets_into_env(), _month_end_running(), streamlit_app.py — Denri Marketing Dashboard on Streamlit. Serves the existing… (+7 more)

### Community 33 - "Marketing Dashboard Insights Page"
Cohesion: 0.13
Nodes (15): Menu 1: Current Performance, Bare Minimum (Bags to be Sold) KPI, Bare Minimum (Growth %) KPI, Declined By KPI (bags missed that week), Forecasted Projection KPI (with corporate in mind), Forward Projections Page, PROJ_DATA_START/PROJ_DATA_END injected JSON data block, Standard Projection KPI (% of Total Target) (+7 more)

### Community 34 - "design-taste-frontend (anti-slop frontend skill)"
Cohesion: 0.18
Nodes (12): design-taste-frontend (related skill), design-taste-frontend (anti-slop frontend skill), Brief-First Process (8-step design workflow), Hard Bans (typography, color, layout, code, content clichés), Pre-Flight Checklist (90+ items), Redesign Protocol (upgrading existing UI), Three Dials — DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, Three AI-generated design clusters (calibration reference) (+4 more)

### Community 35 - "new_products.py"
Cohesion: 0.09
Nodes (30): lib, _base_colour(), fetch_new_products_data(), _apply_stock(), _post_lookup(), is_checked(), _key(), _keyed() (+22 more)

### Community 36 - "lib/report_month.py"
Cohesion: 0.14
Nodes (21): _db_count(), monthly_from_db(), Reporting month's subset count (e.g. rejectBags, giftBags) from…, Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,…, anchor(), is_pinned(), live_anchor(), live_month_key() (+13 more)

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

### Community 51 - "history.py"
Cohesion: 0.27
Nodes (11): fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers…, Like _num, but leaves booleans alone and renders dates as ISO strings — the… (+3 more)

### Community 52 - "scripts/test_receipt_combos.py"
Cohesion: 0.32
Nodes (15): classify(), lines: [{receipt, d, product, qty, amount}] → per-market summary: {running:…, infer(), L(), Tests for receipt_combos.py + name_match.py — python -m pytest scripts -q, test_alternatives_and_singles(), test_bulk_receipts_are_not_combos(), test_four_bags_at_two_prices_are_two_combos() (+7 more)

### Community 53 - "Month-End Routine (doc)"
Cohesion: 0.22
Nodes (9): denri_mkt_timed_offer* Supabase tables, denri_mkt_combo_requests table, denri_mkt_combo_sales table, denri_mkt_self_made_summary table, denri_mkt_timed_offer_weeks table (week-by-week bags/day view), Month-End Routine (doc), Odoo pos_combo_request table (SELECT granted 2026-09-02), Windows Task Scheduler setup (monthly, day 1, ~06:00) (+1 more)

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
Cohesion: 0.15
Nodes (21): hashlib, _ask(), ask_choice(), ask_yes_no(), available(), _cache_get(), _cache_put(), _load() (+13 more)

### Community 58 - "queries.py"
Cohesion: 0.15
Nodes (13): excluded_products(), master_products(), _norm_name(), lib/queries.py — SQL for the Litmus Postgres source of truth (Odoo POS). Bags…, Lower-cased product names to drop from Total Sales. Returns a sentinel when the…, Match the SQL normalisation: lower-case, '.'→space, collapse whitespace., Normalised, de-duplicated master catalogue names (master_products.txt), for the…, main() (+5 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "run_query"
Cohesion: 0.14
Nodes (21): corporate_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, _corporate_bags(), Corporate bags sold in the given month, live from Odoo invoices. Returns 0 when…, _drop_shared_conn(), DataFrame, Run a read query and return a DataFrame, or None if the DB is unreachable.…, run_query() (+13 more)

### Community 61 - "month_end.py"
Cohesion: 0.31
Nodes (8): clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.…, YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that…, After the closing month's timed offers are safely in Supabase, empty the config…, run(), target_month(), subprocess

### Community 62 - "load_rows"
Cohesion: 0.13
Nodes (16): fixture, load_rows(), oos_by_bag_shop(), {period: {product name: {shop: people}}} straight from Odoo names, or {} if…, [{date, shop, kind, person, purchased, product}] — one per OOS request × bag…, match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, parametrize (+8 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "test_oos_callbacks.py"
Cohesion: 0.23
Nodes (14): aggregate(), The page block: {period: {key: {"total": people, "shops": [[shop, people],…, pytest, _base_sql(), _kai(), Tests for lib/oos_callbacks.py (WhatsApp "Out of stock — call back" demand).…, test_attach_stock_per_shop_and_colour(), test_colours_break_down_each_bag() (+6 more)

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

### Community 71 - "live_month_window"
Cohesion: 0.22
Nodes (11): base_period(), build(), load_targets(), The three complete months before month_start → (start, end)., (rows, total, base start, base end) for the month, from Odoo., {BAG: target units} for the month from product_targets_<YYYY-MM>.csv (built…, {BAG: col C} from MONTHLY_TARGET — for the comparison column only., _sheet_targets() (+3 more)

### Community 73 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 74 - "offer_data.py"
Cohesion: 0.20
Nodes (13): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), rows_of() (+5 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.13
Nodes (26): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+18 more)

### Community 76 - "current_performance.html"
Cohesion: 0.40
Nodes (5): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance), current_performance.html (nav target)

### Community 77 - "_build_sheet_slots"
Cohesion: 0.50
Nodes (4): _build_sheet_slots(), _combo_sheet_slots(), Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]., [(label, slots)] for each running combo on the offer sheet (skips the TOTAL…

### Community 78 - "publish.py"
Cohesion: 0.23
Nodes (13): argparse, fnmatch, changed_files(), git(), group(), is_secret(), main(), publish.py — one-click, VERIFIED publish of the dashboard to GitHub (Streamlit… (+5 more)

### Community 79 - "sys"
Cohesion: 0.20
Nodes (9): Deals from posters (RALPH_DEALS.md) — 2026-10-04, _local_deal_rows(), Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), sys, Tests for the poster-sourced deals (deals_kenya.csv →…, test_month_not_in_csv_has_no_deals_and_no_sheet_read() (+1 more)

### Community 80 - "_combo_button_usage"
Cohesion: 0.14
Nodes (11): Inputs (from the user, Oct 2026), Ralph task — Sinza & Uganda offers + receipt-based combo counting, Steps, _combo_button_usage(), _matches_sheet(), _opt_close(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Two normalised slot options name the same bag, loosely: equal ignoring spaces… (+3 more)

### Community 81 - "push_laya.py"
Cohesion: 0.13
Nodes (20): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+12 more)

### Community 82 - "google_auth.py (shared auth module)"
Cohesion: 0.25
Nodes (8): google_auth.py (shared auth module), google_credentials.json (OAuth desktop client), google_token.json (OAuth token), main.py (refresh + serve dashboard), OAuth token expiry issue (Testing mode, ~7 day expiry), reauth.py (re-login script), service_account.json (recommended, permanent auth), Service account chosen for zero-maintenance auth + enabling in-dashboard Refresh

### Community 83 - "test_push_planner.py"
Cohesion: 0.18
Nodes (18): Per bag × market: the facts (`push_rules.facts`, `add_peers`), add_peers(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m…, ISO date n days before END (0 = END). (+10 more)

### Community 84 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

### Community 85 - "self_made_combos.py"
Cohesion: 0.11
Nodes (23): _load_source(), bags_offer_source.json if written in the last 15 min for this month (and it has…, _bag_sales_daily_sql(), _bag_sales_sql(), _bags_not_on_offer(), dow_tier_weeks(), fetch(), fmt() (+15 more)

### Community 86 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.33
Nodes (5): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), What it does

### Community 87 - "F"
Cohesion: 0.24
Nodes (16): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), A facts row with sensible defaults, overridden by kw., test_fallback_slow_seller_or_overstocked() (+8 more)

### Community 88 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.15
Nodes (9): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests, Agent skills — retail analytics, Test a skill (+1 more)

### Community 91 - "test_product_targets.py"
Cohesion: 0.24
Nodes (10): allocate(), available_days(), Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for lib/product_targets.py (bag targets from Odoo; spec docs/product-…, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating(), test_new_bag_is_scaled_to_the_days_it_was_in_shops() (+2 more)

### Community 92 - "push_rules.py"
Cohesion: 0.10
Nodes (22): action(), _cover_txt(), _days_back(), _n(), not_moving(), posting_median(), rank(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).… (+14 more)

### Community 93 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 94 - "Phase 1 — archive the target month"
Cohesion: 0.33
Nodes (6): DENRI_REPORT_MONTH env var (pin target month), FINALIZED_MONTHS set (frozen-report guard), month_end.py (script), Phase 1 — archive the target month, Phase 2 — restore the live view (unpinned), SUPABASE_DB_URL env var (Session Pooler connection string)

### Community 95 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 96 - "_post_yield"
Cohesion: 0.25
Nodes (6): _onoff(), _bt_on_offer(), _yield(), _post_yield(), Marketing & Sales Alignment — posting yield, measured the way marketing…, Is this bag type on offer, matched against the Self-Made-Combos offer set with…

### Community 97 - "signals"
Cohesion: 0.09
Nodes (29): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+21 more)

### Community 98 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "load_config"
Cohesion: 0.20
Nodes (10): Kenya timed-offer campaigns from timed_offers_config.json (normalised by…, _timed_offers(), _bags_from_file(), _derive_month(), load_config(), _norm_offer(), Multi-offer config: {"month": "YYYY-MM", "offers": [offer, ...]}. Back-compat:…, Bag list from a repo CSV's 'BAG TYPE' column — unique, order-preserving. Lets… (+2 more)

### Community 101 - "push_to_supabase.py"
Cohesion: 0.33
Nodes (5): _collect_comments() (pulls prose from rendered report), denri_mkt_monthly.comments (jsonb list), psycopg2, main(), push_to_supabase.py — run the marketing migration against Supabase. Regenerates…

### Community 102 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 104 - "monthly_target_rows"
Cohesion: 0.16
Nodes (11): fetch_monthly_target(), fetch_sheet_data(), monthly_target_rows(), MONTHLY_TARGET rows with column C = the bag's target from Odoo (docs/product-…, test_monthly_target_rows_swaps_column_c(), main(), date, _query_ready() (+3 more)

### Community 105 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 107 - "_fetch_monthly_kenya"
Cohesion: 0.17
Nodes (16): _analyze_region(), _fetch_monthly_kenya(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), Monthly Kenya figures for the S1 KPI cards. MONTHLY_MARKETING_POST: sum col E…, MONTHLY_SALES: colour=A(0), product_name=B(1) (+8 more)

### Community 109 - "bag_classifier"
Cohesion: 0.14
Nodes (15): bag_of(), _add_oos(), _apply_receipt_offers(), bag_classifier(), infer(), _norm(), _load_bag_prices(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's… (+7 more)

### Community 121 - "_dead_clear"
Cohesion: 0.29
Nodes (5): _dead_clear(), _clear(), {catalogue name: net units moved INTO the region's shops on/after `since`} from…, Dead-stock clearance for ONE region and ONE period, posted vs not posted × on…, _region_net_moves()

### Community 122 - "bags_on_offer.py"
Cohesion: 0.15
Nodes (17): _bag_tiers(), _base_windows(), _custom_range(), fmt(), inject(), main(), _new_products(), _previous_payload() (+9 more)

### Community 123 - "test_sheet_reads.py"
Cohesion: 0.60
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 124 - "reject_sales.py"
Cohesion: 0.18
Nodes (14): _assign_price(), _bom_costs(), build(), _category_of(), _norm_cat(), reject_stock.csv → {BAG (upper): {units, colours:{COLOUR: units}}}., (price, flag) from BOM cost — two tiers. flag ∈ {'', 'thin', 'below', 'nobom'}., Write an Excel (xlsx, or CSV fallback) of EVERYTHING on the pricing board —… (+6 more)

### Community 125 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.18
Nodes (12): Card component (base building block), dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), Signature Element — Flowing Border (achievement cards), high-end-visual-design (related skill), KPI Tile component, Page Structure Template (new dashboard page starting point) (+4 more)

### Community 126 - "shop_bday.js"
Cohesion: 0.52
Nodes (6): badge(), esc(), key(), ordinal(), short(), strip()

### Community 127 - "shop-birthdays.md"
Cohesion: 0.18
Nodes (8): Design Tokens (colors, typography, spacing), Semantic color rules (green=good, amber=risk, red=critical, cyan=info), Analytics Dashboard specific rules (VISUAL_DENSITY: dense), Shop birthdays, Shop → opening date, Where it shows, Region colour palette (reference for Executive Dashboard), Shops & Regions (doc — source of truth)

### Community 128 - "os"
Cohesion: 0.13
Nodes (14): One-off: restore August's Offer Type figures into monthly_report_history.json…, _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,… (+6 more)

### Community 129 - "_build_period"
Cohesion: 0.20
Nodes (6): _build_period(), _offer_types(), _pick_target(), Latest target row for `shop` with this period that overlaps [start, end]. A…, Matrix payload: rows, per-row category / tier cells, and the period's Top-5…, _region_of()

### Community 130 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 131 - "self_made_combos_bundle/lib/__init__.py"
Cohesion: 0.25
Nodes (6): lib — shared data-access for the marketing dashboard (Postgres migration).…, openpyxl, openpyxl_comments, openpyxl_styles, openpyxl_utils, product_targets_workbook.py — the month's bag targets as an Excel workbook with…

### Community 132 - "re"
Cohesion: 0.18
Nodes (14): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]., Till name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same… (+6 more)

### Community 133 - "timed_offers.py (generator)"
Cohesion: 0.18
Nodes (11): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers.html (output), timed_offers.py (generator), Timed Offers Section — Back to School Edition (Report) (+3 more)

### Community 134 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 135 - "oos_callbacks.py"
Cohesion: 0.17
Nodes (13): attach_stock(), collect(), _in(), lib/oos_callbacks.py — "Out of stock — call back" demand from the WhatsApp…, {period: {key: people}} from an aggregate() block., Add each shop's live on-hand to an aggregate() block, in place: every [shop,…, {period: (start, end)} for the dated periods (lifetime / current are undated)., {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+5 more)

### Community 136 - "Marketing Dashboard — Google Sheets access & setup (doc)"
Cohesion: 0.29
Nodes (7): timed_offers_config.json (config), Vercel hosted version (static snapshot), Secrets excluded via .gitignore / .vercelignore, Marketing Dashboard — Google Sheets access & setup (doc), Timed Offers snapshot-over-window workflow, vercel.json, Vercel static deployment (serves committed HTML, no build step)

### Community 137 - "_combo_norm_option"
Cohesion: 0.22
Nodes (10): _build_sheet_slots(), _combo_norm_option(), _combo_sheet_slots(), combos_by_shop(), _norm(), _tokmatch(), Per-shop view for Shops Efficiency, keyed by shop-location label (e.g.…, One combo slot-option → its distinctive bag token(s), colours/category words… (+2 more)

### Community 138 - "self_made_combos.py"
Cohesion: 0.50
Nodes (4): Per-shop combo-button chips (red when < half best-in-region), self_made_combos.py, Shop -> Region table, self_made_combos.html (nav target)

### Community 139 - "lib/db.py"
Cohesion: 0.24
Nodes (10): _cache_path(), _env(), get_engine(), Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, The process's reused connection (opened on first query). Every generator runs…, Build a SQLAlchemy URL from the environment, or None if unset. Accepts…, _shared_conn() (+2 more)

### Community 140 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 141 - "Bag targets October 2026_b78d9f88.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 142 - "build"
Cohesion: 0.22
Nodes (11): _alt_cost(), build(), _combo_cost(), _combo_slots(), {BAG TYPE (upper): production cost} from bom_costs.json — the local copy of the…, Parse `const SMC = {…}` out of self_made_combos.html (no DB round-trip)., One combo alternative (e.g. 'Amaya Handbag') → its BOM production cost., Combo name → list of slots, each a list of alternative strings. (+3 more)

### Community 143 - "Laya"
Cohesion: 0.27
Nodes (6): _bucket(), _clamp(), Laya, Probabilities over `options` for each state (one batch)., One loaded model. Use the module functions below (they share one instance)., softmax()

### Community 144 - "Combos from receipts — running vs self-made"
Cohesion: 0.25
Nodes (8): opt_close(), Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Combos from receipts — running vs self-made, Inputs, Name matching (`name_match.py`), Outputs to show, Receipt rule (per receipt), Tests

### Community 145 - "update_np_weekly_history"
Cohesion: 0.29
Nodes (7): _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)., Ordinal among the month's perfect weeks (>=5 days in month), so the first FULL…, Snapshot each Sun–Sat week (sales, Kenya/Outside posts) into…, update_np_weekly_history()

### Community 146 - "scripts/receipt_combos.py"
Cohesion: 0.29
Nodes (6): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…, itertools

### Community 147 - "Out-of-stock demand — people, not requests"
Cohesion: 0.29
Nodes (7): Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods, Show it as, Tests

### Community 148 - "Product (bag) targets"
Cohesion: 0.29
Nodes (6): No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 149 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.29
Nodes (6): Blocker counter, Final summary, Log, OOS call-back progress (Ralph loop log), Sheets cut to three tabs (RALPH_SHEETS.md) — 2026-10-04, Sinza & Uganda (RALPH_OUTSIDE.md) — 2026-10-04

### Community 150 - "_seasonality"
Cohesion: 0.40
Nodes (6): Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), _combo_odoo_slots(), Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…

### Community 151 - "Sales-share targets per product"
Cohesion: 0.40
Nodes (4): Deliver, Sales-share targets per product, Steps, Tests

### Community 152 - "_read_offers"
Cohesion: 0.40
Nodes (5): Offer type summary (matrix), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, _read_offers(), _read_offers_cache()

### Community 154 - "_month_archived"
Cohesion: 0.67
Nodes (3): cache_data, _month_archived(), True when `key` is in Supabase (falls back to monthly_report_history.json). If…

### Community 155 - "_kind"
Cohesion: 0.67
Nodes (3): _kind(), HANDBAG' → 'handbags', 'SCHOOL BAG' → 'school bags', 'SPORT' → 'sport bags', ''…, test_kind_wording()

## Ambiguous Edges - Review These
- `August 2026 Monthly Report` → `Legacy dated report_YYYY_month.html archive pattern`  [AMBIGUOUS]
  report_2026_august.html · relation: conceptually_related_to
- `Reject Sale page (reject_sales.html)` → `Card entrance animation via CSS @keyframes + animation-fill-mode: both`  [AMBIGUOUS]
  .claude/skills/dashboard-design.md · relation: conceptually_related_to

## Knowledge Gaps
- **202 isolated node(s):** `Added mid-task (user)`, `Monthly inputs (user uploads)`, `Steps (verify each)`, `No zero targets`, `Output columns` (+197 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 828 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `August 2026 Monthly Report` and `Legacy dated report_YYYY_month.html archive pattern`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Reject Sale page (reject_sales.html)` and `Card entrance animation via CSS @keyframes + animation-fill-mode: both`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Current Performance (doc)` connect `forward_projections.py` to `monthly_target_rows`, `queries.py`, `datetime`, `Product / name matching (doc)`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Why does `New Products Analytics (doc)` connect `Product / name matching (doc)` to `forward_projections.py`, `Dashboard Insights skill`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Why does `Sidebar Navigation (icon rail / expanded drawer)` connect `Sidebar Navigation (icon rail / expanded drawer)` to `August 2026 Monthly Report`, `self_made_combos.py`, `current_performance.html`, `Kitengela Rejects tracker (timed offer)`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `fetch()` (e.g. with `classify()` and `oos_key()`) actually correct?**
  _`fetch()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Added mid-task (user)`, `Monthly inputs (user uploads)`, `Steps (verify each)` to the rest of the system?**
  _202 weakly-connected nodes found - possible documentation gaps or missing edges._