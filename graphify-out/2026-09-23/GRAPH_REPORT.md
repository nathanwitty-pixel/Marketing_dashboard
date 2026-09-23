# Graph Report - Marketing_dashboard  (2026-09-22)

## Corpus Check
- 128 files · ~483,617 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 2, .toml 1, .zip 1)

## Summary
- 1147 nodes · 1860 edges · 79 communities (69 shown, 10 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 67 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Google Auth & Posting Analysis
- Offer Picking Catalogue
- TTL Cache & Timed Offers
- Shared DB Access Library
- Dataviz & Theme Skills
- Current Performance & Insights
- Reject Sales Pricing
- Monthly Report Generator
- Shops Efficiency Generator
- Dashboard Design Skill
- Database Connection Core
- Current Performance Generator
- Offer Data & Sheets Auth
- Sales Exclusion Rules
- Forward Projections Generator
- Report Month Resolver
- Report Month Resolver (2)
- Offer Data Builder
- Self-Made Combos Payload
- Dashboard Local Server
- Combos in Monthly Report
- Dashboard Data Sources
- Shops Dispatch Generator
- New Products Analytics Spec
- Shared Connection Reuse Rules
- Self-Made Combos Fetch & Inject
- Self-Made Combos SQL Helpers
- Dashboard Menu Docs Spec
- Self-Made vs Running Combos Doc
- Deal Enrichment Matching
- History Snapshot Builder
- Supabase Schema Tables
- August Offer Restore Script
- Streamlit App Config
- Local HTTP Server
- Combo Button Usage Calc
- Month-End Archival Routine
- Google Sheets Setup Doc
- Dashboard Theme CSS
- Shops Efficiency Spec Doc
- Timed Offers Supabase Tables
- Deal Tier Aggregation
- Power Deals & DoW Fetch
- Dead Stock Tuning Knobs
- Offer Picking Forecast Doc
- Combos by Shop Panel
- Timed Offers Rollover
- Supabase Migration Export
- Self-Made Combos README Spec
- Reporting History Pipeline
- Product Matching Rules
- Bags Not On Offer Logic
- Bags Not On Offer Logic (2)
- Combos By Shop Function
- Algorithmic Art Skill
- Combos Bundle Export README
- Supabase Comments Push
- Month-End Archive Phases
- Combo Sheet Matching
- High-End Visual Design Skill
- Vercel Static Deployment
- Dashboard Shell & Refresh
- Deal Matching Helpers
- Daydream Skill
- Combo Sheet Slot Parsing
- History Page Rendering
- Daily Timed-Offer Snapshot
- Dashboard PDF/Word Export
- TTL Disk-Cache Rationale
- Perf Data JS Shim
- Current Performance Popover

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 30 edges
2. `build_payload()` - 28 edges
3. `get_gspread_client()` - 26 edges
4. `fetch_posting_data()` - 24 edges
5. `build_payload()` - 24 edges
6. `check_connection()` - 22 edges
7. `Self-made combos vs running combos (doc)` - 22 edges
8. `Dashboard Menu Docs (spec index)` - 21 edges
9. `build_offer()` - 20 edges
10. `safe_int()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `August 2026 Monthly Report` --semantically_similar_to--> `monthly_report.html (nav target)`  [INFERRED] [semantically similar]
  report_2026_august.html → shell.html
- `Sidebar Navigation (icon rail / expanded drawer)` --semantically_similar_to--> `Reject Sale page (reject_sales.html)`  [INFERRED] [semantically similar]
  shell.html → reject_sales.html
- `Self-made combos vs running combos (export bundle copy)` --semantically_similar_to--> `Self-made combos vs running combos (doc)`  [INFERRED] [semantically similar]
  export/self_made_combos_bundle/docs/self-made-combos.md → docs/self-made-combos.md
- `Product Name Matching Rules (case-insensitive, ignores spaces/full-stops)` --semantically_similar_to--> `_matches_sheet / _build_sheet_slots slot-aware matching functions`  [INFERRED] [semantically similar]
  master_products.txt → export/self_made_combos_bundle/README.md
- `Bare Minimum (Bags to be Sold) KPI` --semantically_similar_to--> `Headline Numbers KPI Grid`  [INFERRED] [semantically similar]
  forward_projections.html → insights.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Static HTML + Python generator + injected JSON data-block pattern shared across dashboard pages** — docs_readme_dashboard_architecture, offer_picking_op_data_block, forward_projections_proj_data_block, report_2026_july_rpt_data_object, claude_skills_dataviz_charts_data_marker_pattern [INFERRED 0.85]
- **Cross-report 'unmarketed stock / posting gap' finding echoed across Monthly Report, Insights, and Forward Projections** — report_2026_july_unmarketed_stock_finding, insights_unposted_stock_finding, report_2026_july_regional_unevenness_finding, insights_uganda_conversion_finding [INFERRED 0.85]
- **Self-made combos bundle: generator, Sheets auth, DB access, and dependency manifest working together to build the combos page** — export_self_made_combos_bundle_self_made_combos_py, export_self_made_combos_bundle_offer_data_py, export_self_made_combos_bundle_google_auth_py, export_self_made_combos_bundle_lib_db_py, export_self_made_combos_bundle_requirements [EXTRACTED 0.90]
- **Kitengela reject clearance tracked across pricing, timed-offer, and performance pages** — docs_timed_offers_kitengelarejectstracker, reject_sales_rejectsalepage, docs_current_performance_rejectsplitline, docs_reject_sales_rejectsaledoc, docs_timed_offers_rejectstockcsv [INFERRED 0.85]
- **Month-end archive pipeline: rebuild pinned month, snapshot report, push to Supabase, render History** — month_end_monthendpy, monthly_report, push_to_supabase, history, month_end_historyhtml [EXTRACTED 0.90]
- **Shell navigation ties sidebar items to their generator-backed dashboard pages** — shell_sidebarnavigation, shell_scriptmap, shell_pagepurposemap, shell_dashframeiframe, shell_currentperformancehtml [EXTRACTED 0.85]
- **Monthly Report reads injected data blocks from the generator pages that run before it** — docs_monthly_report_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_posting_yields_doc, current_performance_html_current_performance_page [EXTRACTED 1.00]
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]
- **Dashboard Insights skill synthesizes across four dashboard data objects (PERF/PROJ, NP, OA, PA)** — _claude_skills_dashboard_insights_skill, current_performance_html_perf_data, docs_new_products_doc, docs_self_made_combos_doc, docs_posting_yields_doc [EXTRACTED 1.00]

## Communities (79 total, 10 thin omitted)

### Community 0 - "Google Auth & Posting Analysis"
Cohesion: 0.05
Nodes (71): get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, os, _alignment_region(), _for(), _onoff(), _sold(), _stk() (+63 more)

### Community 1 - "Offer Picking Catalogue"
Cohesion: 0.06
Nodes (53): csv, _alt_cost(), _apply_alias(), build(), _build_catalog(), _combo_cost(), _combo_slots(), _is_full_price() (+45 more)

### Community 2 - "TTL Cache & Timed Offers"
Cohesion: 0.07
Nodes (48): check_connection(), run_query with a TTL disk cache. Identical to run_query for callers, but a…, (ok, detail). Never raises — the callers show `detail` in the UI., run_query_cached(), _bags_from_file(), _bucket(), build_offer(), _derive_month() (+40 more)

### Community 3 - "Shared DB Access Library"
Cohesion: 0.07
Nodes (42): _drop_shared_conn(), DataFrame, Run a read query and return a DataFrame, or None if the DB is unreachable.…, run_query(), lib — shared data-access for the marketing dashboard (Postgres migration).…, _codes_for(), _inlist(), odoo_stock_by_product() (+34 more)

### Community 4 - "Dataviz & Theme Skills"
Cohesion: 0.04
Nodes (46): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+38 more)

### Community 5 - "Current Performance & Insights"
Cohesion: 0.05
Nodes (38): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), graw(block, key) function (bare numeric getter), gstr(block, key) function (string field regex getter), insights.html, Key-rename / run-order gotcha (blanks or zeros), NEW_PROD data block (New Products) (+30 more)

### Community 6 - "Reject Sales Pricing"
Cohesion: 0.05
Nodes (41): Card entrance animation via CSS @keyframes + animation-fill-mode: both, "Below cost" flag, bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, "No BOM" flag, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source) (+33 more)

### Community 7 - "Monthly Report Generator"
Cohesion: 0.07
Nodes (27): monthly_report_history.json, _bag_stock(), _cause(), _collect_comments(), _combo_bags(), fmt(), _garr_line(), gnum() (+19 more)

### Community 8 - "Shops Efficiency Generator"
Cohesion: 0.07
Nodes (24): apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _load_combos_by_shop(), _from_file(), _nonempty(), _metric() (+16 more)

### Community 9 - "Dashboard Design Skill"
Cohesion: 0.07
Nodes (33): Card component (base building block), dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards), high-end-visual-design (related skill) (+25 more)

### Community 10 - "Database Connection Core"
Cohesion: 0.09
Nodes (31): dotenv, check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME… (+23 more)

### Community 11 - "Current Performance Generator"
Cohesion: 0.08
Nodes (19): corporate_from_db(), fetch_monthly_target(), master_from_db(), monthly_from_db(), current_performance.py…, Reporting month's NET catalogue bags from Postgres (monthly_sales_db.json,…, Reporting month's reject-clearance bags ([REJECT] tag) from…, Update the rolling snapshot. Returns (carryover_bags | None, captured_on,… (+11 more)

### Community 12 - "Offer Data & Sheets Auth"
Cohesion: 0.14
Nodes (18): Shared Google Sheets authentication for every dashboard generator. Two modes,…, build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), cell(), find_row(), find_row_any() (+10 more)

### Community 13 - "Sales Exclusion Rules"
Cohesion: 0.13
Nodes (18): datetime, Current Performance (doc), lib — shared data-access for the marketing dashboard (Postgres migration).…, excluded_products(), Lower-cased product names to drop from Total Sales. Returns a sentinel when the…, main(), month_window(), date (+10 more)

### Community 14 - "Forward Projections Generator"
Cohesion: 0.12
Nodes (12): calendar, _corporate_bags(), fetch_sheet_data(), odoo_weekly_breakdown(), _perfect_week_index(), forward_projections.py…, Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat… (+4 more)

### Community 15 - "Report Month Resolver"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 16 - "Report Month Resolver (2)"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 17 - "Offer Data Builder"
Cohesion: 0.17
Nodes (17): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), cell(), find_row(), find_row_any(), process_table() (+9 more)

### Community 18 - "Self-Made Combos Payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 19 - "Dashboard Local Server"
Cohesion: 0.13
Nodes (18): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), Denri Africa — Marketing Dashboard Launcher…, This machine's address on the local network (for the share URL). (+10 more)

### Community 20 - "Combos in Monthly Report"
Cohesion: 0.16
Nodes (15): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+7 more)

### Community 21 - "Dashboard Data Sources"
Cohesion: 0.17
Nodes (16): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Current Performance Dashboard Page, Forward Projections section, PERF data block (weekly/monthly sales KPIs), PROJ data block (forward projections, velocity factor, bare minimum), Monthly Report (doc) (+8 more)

### Community 22 - "Shops Dispatch Generator"
Cohesion: 0.21
Nodes (14): build_period(), distributed_in(), main(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only., Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).… (+6 more)

### Community 23 - "New Products Analytics Spec"
Cohesion: 0.18
Nodes (14): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix) (+6 more)

### Community 24 - "Shared Connection Reuse Rules"
Cohesion: 0.15
Nodes (14): google_auth.py (Sheets auth), lib/db.py (Supabase session pooler DB access), lib/db.run_query (shared connection reuse per subprocess), offer_data.build (batched Sheets range fetch), Refresh Performance (shared connection reuse, batched Sheets reads), Supabase session pooler host rule (direct host is IPv6-only), google_auth.py (service account or OAuth desktop), gspread>=6.0 dependency (Google Sheets access) (+6 more)

### Community 25 - "Self-Made Combos Fetch & Inject"
Cohesion: 0.20
Nodes (11): fetch(), fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py…, Read the Shop → Region table from docs/shop-regions.md so the mapping can be…, Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer… (+3 more)

### Community 26 - "Self-Made Combos SQL Helpers"
Cohesion: 0.16
Nodes (13): _bag_sales_daily_sql(), _bag_sales_sql(), _build_sheet_slots(), _dstr(), fmt(), inject(), _load_shop_regions(), main() (+5 more)

### Community 27 - "Dashboard Menu Docs Spec"
Cohesion: 0.19
Nodes (13): Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes), Menu 5: Posting - Sales Yields from Accurate Posting (+5 more)

### Community 28 - "Self-Made vs Running Combos Doc"
Cohesion: 0.18
Nodes (13): Bags not on offer per market (Kenya/Sinza/Uganda), Combo button usage / rung vs pot. (till check), Self-made combos vs running combos (doc), DoW mirror shops (DOW_MIRROR), Monetary implication panel (bundling discount), Rank chip (follows active Sort filter), Running-combo classification by bag composition (slot-aware sheet match), Standalone SQL (self_made_vs_running_combos.sql) (+5 more)

### Community 29 - "Deal Enrichment Matching"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "History Snapshot Builder"
Cohesion: 0.27
Nodes (11): fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers…, Like _num, but leaves booleans alone and renders dates as ISO strings — the… (+3 more)

### Community 31 - "Supabase Schema Tables"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 32 - "August Offer Restore Script"
Cohesion: 0.20
Nodes (8): One-off: restore August's Offer Type figures into monthly_report_history.json…, json, master_products(), _norm_name(), lib/queries.py — SQL for the Litmus Postgres source of truth (Odoo POS). Bags…, Match the SQL normalisation: lower-case, '.'→space, collapse whitespace., Normalised, de-duplicated master catalogue names (master_products.txt), for the…, re

### Community 33 - "Streamlit App Config"
Cohesion: 0.18
Nodes (6): SCRIPT_TIMEOUT = 600s config, streamlit, _load_secrets_into_env(), streamlit_app.py — Denri Marketing Dashboard on Streamlit. Serves the existing…, streamlit_components_v1, time

### Community 34 - "Local HTTP Server"
Cohesion: 0.27
Nodes (10): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_refresh(), _run_ref() (+2 more)

### Community 35 - "Combo Button Usage Calc"
Cohesion: 0.22
Nodes (8): _combo_button_usage(), _combo_norm_option(), _combo_odoo_slots(), _matches_sheet(), One combo slot-option → its distinctive bag token(s), colours/category words…, Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…, The sheet label this Odoo combo maps to (same slot count, every slot overlaps),…, Per running combo: units rung through the combo button (Odoo) vs the sheet's…

### Community 36 - "Month-End Archival Routine"
Cohesion: 0.27
Nodes (9): clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.…, YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that…, After the closing month's timed offers are safely in Supabase, empty the config…, run(), target_month(), subprocess (+1 more)

### Community 37 - "Google Sheets Setup Doc"
Cohesion: 0.20
Nodes (10): Secrets excluded via .gitignore / .vercelignore, google_auth.py (shared auth module), google_credentials.json (OAuth desktop client), Marketing Dashboard — Google Sheets access & setup (doc), google_token.json (OAuth token), main.py (refresh + serve dashboard), OAuth token expiry issue (Testing mode, ~7 day expiry), reauth.py (re-login script) (+2 more)

### Community 38 - "Dashboard Theme CSS"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 39 - "Shops Efficiency Spec Doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "Timed Offers Supabase Tables"
Cohesion: 0.22
Nodes (9): denri_mkt_timed_offer* Supabase tables, denri_mkt_combo_requests table, denri_mkt_combo_sales table, denri_mkt_self_made_summary table, denri_mkt_timed_offer_weeks table (week-by-week bags/day view), Month-End Routine (doc), Odoo pos_combo_request table (SELECT granted 2026-09-02), Windows Task Scheduler setup (monthly, day 1, ~06:00) (+1 more)

### Community 41 - "Deal Tier Aggregation"
Cohesion: 0.25
Nodes (6): _enrich_deals(), _tdigit(), _tier_agg(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 42 - "Power Deals & DoW Fetch"
Cohesion: 0.22
Nodes (7): fetch(), Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, The component bag names across a region's sheet combos/singles/specials cards…, _read_deals(), _read_offer_analysis(), _region_on_offer_bags()

### Community 43 - "Dead Stock Tuning Knobs"
Cohesion: 0.25
Nodes (8): Dead Stock Accountability tuning knobs, Per-region high-stock floors (Kenya 20, Sinza 5, Uganda 5), weak_max threshold (sold < 5 = weak sales), On-offer definition per region (from SMC block), Reject Sale margin report (converted xlsx), 'below cost' margin flag, 'pinned' flag, 'thin' margin flag

### Community 44 - "Offer Picking Forecast Doc"
Cohesion: 0.29
Nodes (8): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES)

### Community 45 - "Combos by Shop Panel"
Cohesion: 0.25
Nodes (8): Combos & Power Deals by Shop panel (#combo-shop), compute_period() function (emits pushDetail per period), Deal of the Week — Tier 2 (latest 2-week window) shop-scoped view, DenriTableFilter reusable filter bar component, DOW_MIRROR expansion (Starmall to Hazina/Hilton/KTDA), odoo_stock_levels() function, Push via filter (None / power deal / deal of the week tag), shops_efficiency.html page

### Community 46 - "Timed Offers Rollover"
Cohesion: 0.25
Nodes (8): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.py (generator), Timed Offers Section — Back to School Edition (Report), Timed Offers snapshot-over-window workflow

### Community 47 - "Supabase Migration Export"
Cohesion: 0.36
Nodes (7): main(), month_block(), num(), q(), supabase_migration.py — export the marketing dashboard's monthly data to a SQL…, SQL string literal (or NULL)., SQL numeric literal (or NULL). Ints print without a trailing .0.

### Community 48 - "Self-Made Combos README Spec"
Cohesion: 0.29
Nodes (7): lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, lib/report_month.py (which month are we reporting?), self_made_combos.html static page (reads const SMC), self_made_combos.py generator (build_payload + SQL + injection)

### Community 49 - "Reporting History Pipeline"
Cohesion: 0.33
Nodes (7): denri_mkt_* Supabase tables, history.html page, history.py (read months back), month_end.py (freezes a month), push_to_supabase.py (write months), Resilience fallback: history.py leaves existing page data untouched if Supabase unreachable, supabase_migration.py (schema)

### Community 50 - "Product Matching Rules"
Cohesion: 0.33
Nodes (7): Composition-based classification rationale (Running vs Self-made), _matches_sheet / _build_sheet_slots slot-aware matching functions, Master Products Catalogue List, Product Name Matching Rules (case-insensitive, ignores spaces/full-stops), Net Bags Sold (catalogue) KPI, Always-on exclusion rules (combo wrappers, delivery, customisation, straps, KES discounts, POS-category lines, refunds, unpaid/cancelled orders), sales_exclusions.txt (products not counted as bag sales)

### Community 51 - "Bags Not On Offer Logic"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 52 - "Bags Not On Offer Logic (2)"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month (in the market `sql` scopes to) that are on NO…

### Community 53 - "Combos By Shop Function"
Cohesion: 0.38
Nodes (6): _combo_norm_option(), combos_by_shop(), _norm(), _tokmatch(), Per-shop view for Shops Efficiency, keyed by shop-location label (e.g.…, One combo slot-option → its distinctive bag token(s), colours/category words…

### Community 54 - "Algorithmic Art Skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "Combos Bundle Export README"
Cohesion: 0.33
Nodes (6): shop-regions.md (editable Shop to Region table), Self-made combos vs Running combos portable bundle README, Returns netting rationale (qty <> 0, returns subtract), docs/self-made-combos.md full spec for the menu, docs/shop-regions.md editable shop to region map, sql/self_made_vs_running_combos.sql (standalone pure-SQL classification)

### Community 56 - "Supabase Comments Push"
Cohesion: 0.33
Nodes (5): _collect_comments() (pulls prose from rendered report), denri_mkt_monthly.comments (jsonb list), psycopg2, main(), push_to_supabase.py — run the marketing migration against Supabase. Regenerates…

### Community 57 - "Month-End Archive Phases"
Cohesion: 0.33
Nodes (6): DENRI_REPORT_MONTH env var (pin target month), FINALIZED_MONTHS set (frozen-report guard), month_end.py (script), Phase 1 — archive the target month, Phase 2 — restore the live view (unpinned), SUPABASE_DB_URL env var (Session Pooler connection string)

### Community 58 - "Combo Sheet Matching"
Cohesion: 0.33
Nodes (4): _combo_button_usage(), _matches_sheet(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, The sheet label this Odoo combo maps to (same slot count, every slot overlaps),…

### Community 59 - "High-End Visual Design Skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "Vercel Static Deployment"
Cohesion: 0.40
Nodes (4): build_all.py ────────────────────────────────────────────────────────────────…, Vercel hosted version (static snapshot), vercel.json, Vercel static deployment (serves committed HTML, no build step)

### Community 61 - "Dashboard Shell & Refresh"
Cohesion: 0.40
Nodes (5): renderOffer(TO, root) function, timed_offers.html (output), /api/refresh endpoint, reloadFrame() function, SCRIPT_MAP (dashboard filename to generator script map)

### Community 62 - "Deal Matching Helpers"
Cohesion: 0.50
Nodes (3): _match(), _full(), _full_of()

### Community 63 - "Daydream Skill"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "Combo Sheet Slot Parsing"
Cohesion: 0.50
Nodes (4): _build_sheet_slots(), _combo_sheet_slots(), Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]., [(label, slots)] for each running combo on the offer sheet (skips the TOTAL…

### Community 65 - "History Page Rendering"
Cohesion: 0.50
Nodes (4): buildCharts(m, wk, prevM) function, render(idx) function, selfMadeHtml(m) function, timedOffersHtml(m) function

### Community 66 - "Daily Timed-Offer Snapshot"
Cohesion: 0.50
Nodes (4): _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, start_daily_snapshot()

### Community 67 - "Dashboard PDF/Word Export"
Cohesion: 0.50
Nodes (4): buildExportDoc(mode) function, colorizeForPaper() function, exportPDF() function, exportWord() function

### Community 68 - "TTL Disk-Cache Rationale"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

## Ambiguous Edges - Review These
- `August 2026 Monthly Report` → `Legacy dated report_YYYY_month.html archive pattern`  [AMBIGUOUS]
  report_2026_august.html · relation: conceptually_related_to
- `Reject Sale page (reject_sales.html)` → `Card entrance animation via CSS @keyframes + animation-fill-mode: both`  [AMBIGUOUS]
  .claude/skills/dashboard-design.md · relation: conceptually_related_to

## Knowledge Gaps
- **138 isolated node(s):** `PERF`, `Forecast Section (live picks for next month)`, `Baseline Forecast Section (fixed recommended picks)`, `Next Month's Combos to Run Section`, `Power Deal Choosing Section (10 single-bag slots)` (+133 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 503 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `August 2026 Monthly Report` and `Legacy dated report_YYYY_month.html archive pattern`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Reject Sale page (reject_sales.html)` and `Card entrance animation via CSS @keyframes + animation-fill-mode: both`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `get_gspread_client()` connect `Google Auth & Posting Analysis` to `Offer Picking Catalogue`, `TTL Cache & Timed Offers`, `Shared DB Access Library`, `Shops Efficiency Generator`, `Power Deals & DoW Fetch`, `Current Performance Generator`, `Offer Data & Sheets Auth`, `Forward Projections Generator`, `Offer Data Builder`, `Self-Made Combos Fetch & Inject`, `Self-Made Combos SQL Helpers`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `Sidebar Navigation (icon rail / expanded drawer)` connect `Current Performance & Insights` to `Dashboard Design Skill`, `Reject Sales Pricing`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `Denri Africa Dashboard Design System (skill)` connect `Dashboard Design Skill` to `Reject Sales Pricing`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **What connects `PERF`, `Forecast Section (live picks for next month)`, `Baseline Forecast Section (fixed recommended picks)` to the rest of the system?**
  _138 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Google Auth & Posting Analysis` be split into smaller, more focused modules?**
  _Cohesion score 0.054203180785459264 - nodes in this community are weakly interconnected._