# Graph Report - Marketing_dashboard  (2026-09-24)

## Corpus Check
- 110 files · ~504,071 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 2, .toml 1, .zip 1)

## Summary
- 1193 nodes · 1950 edges · 80 communities (67 shown, 13 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 74 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `30c29631`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- POSTING (SALES YIELDS FROM ACCURATE POSTING).py
- offer_picking.py
- timed_offers.py
- new_products.py
- Offer Picking Dashboard Page
- generate_insights.py
- Kitengela Rejects tracker (timed offer)
- monthly_report.py
- shops_efficiency.py
- Denri Africa Dashboard Design System (skill)
- lib/db.py
- current_performance.py
- self_made_combos_bundle/offer_data.py
- json
- lib/report_month.py
- self_made_combos_bundle/lib/report_month.py
- Marketing Dashboard Insights Page
- fetch_offer_data
- build_payload
- main.py
- build_payload
- Dashboard Insights skill
- shops_dispatch.py
- Product / name matching (doc)
- July 2026 Monthly Report Page
- self_made_combos_bundle/self_made_combos.py
- fetch
- Dashboard Menu Docs (spec index)
- Self-made combos vs running combos (doc)
- _enrich_deals
- history.py
- marketing_dashboard.sql
- bags_on_offer.py
- streamlit_app.py
- start_server
- _combo_button_usage
- month_end.py
- timed_offers.py (generator)
- theme.py
- Shops Efficiency Tracking spec doc
- forward_projections.py
- _enrich_deals
- Forward Projections Page
- On-offer definition per region (from SMC block)
- Offer Picking (doc)
- Combos & Power Deals by Shop panel (#combo-shop)
- Sidebar Navigation (icon rail / expanded drawer)
- self_made_combos.py generator (build_payload + SQL + injection)
- CLAUDE.md
- history.py (read months back)
- Self-made combos vs Running combos portable bundle README
- _bags_not_on_offer
- datetime
- _combo_norm_option
- algorithmic-art skill
- current_performance.html
- August 2026 Monthly Report
- build_all.py
- _combo_button_usage
- High-End Visual Design skill
- self_made_combos.py
- insights.html
- daydream skill (Vault Daydream)
- _build_sheet_slots
- render(idx) function
- _offer_active_today
- buildExportDoc(mode) function
- TTL disk-cache rationale (.odoo_cache/)
- perf_data.js
- attachPopover(cardId, popId) function
- lib
- self_made_combos.py

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 30 edges
2. `get_gspread_client()` - 28 edges
3. `build_payload()` - 28 edges
4. `fetch_posting_data()` - 24 edges
5. `build_payload()` - 24 edges
6. `check_connection()` - 23 edges
7. `Self-made combos vs running combos (doc)` - 22 edges
8. `Dashboard Menu Docs (spec index)` - 21 edges
9. `build_offer()` - 20 edges
10. `fetch()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Buckets` --references--> `bag_classifier()`  [INFERRED]
  docs/bags-on-offer.md → self_made_combos.py
- `Self-made combos vs running combos (export bundle copy)` --semantically_similar_to--> `Self-made combos vs running combos (doc)`  [INFERRED] [semantically similar]
  export/self_made_combos_bundle/docs/self-made-combos.md → docs/self-made-combos.md
- `August 2026 Monthly Report` --semantically_similar_to--> `monthly_report.html (nav target)`  [INFERRED] [semantically similar]
  report_2026_august.html → shell.html
- `Sidebar Navigation (icon rail / expanded drawer)` --semantically_similar_to--> `Reject Sale page (reject_sales.html)`  [INFERRED] [semantically similar]
  shell.html → reject_sales.html
- `Bare Minimum (Bags to be Sold) KPI` --semantically_similar_to--> `Headline Numbers KPI Grid`  [INFERRED] [semantically similar]
  forward_projections.html → insights.html

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

## Communities (80 total, 13 thin omitted)

### Community 0 - "POSTING (SALES YIELDS FROM ACCURATE POSTING).py"
Cohesion: 0.05
Nodes (71): get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, os, _alignment_region(), _for(), _onoff(), _sold(), _stk() (+63 more)

### Community 1 - "offer_picking.py"
Cohesion: 0.06
Nodes (53): csv, _alt_cost(), _apply_alias(), build(), _build_catalog(), _combo_cost(), _combo_slots(), _is_full_price() (+45 more)

### Community 2 - "timed_offers.py"
Cohesion: 0.07
Nodes (48): check_connection(), run_query with a TTL disk cache. Identical to run_query for callers, but a…, (ok, detail). Never raises — the callers show `detail` in the UI., run_query_cached(), _bags_from_file(), _bucket(), build_offer(), _derive_month() (+40 more)

### Community 3 - "new_products.py"
Cohesion: 0.09
Nodes (29): _base_colour(), fetch_new_products_data(), _apply_stock(), _fix_name(), is_checked(), match_odoo_bags(), _merge_rows_by_base_colour(), _np_complete_weeks_in_month() (+21 more)

### Community 4 - "Offer Picking Dashboard Page"
Cohesion: 0.11
Nodes (19): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+11 more)

### Community 5 - "generate_insights.py"
Cohesion: 0.12
Nodes (12): graw(block, key) function (bare numeric getter), gstr(block, key) function (string field regex getter), Key-rename / run-order gotcha (blanks or zeros), NEW_PROD data block (New Products), OFFER_DATA data block (Self Made Combos), POST_DATA data block (Posting), read_block(file, start, end) function, card() (+4 more)

### Community 6 - "Kitengela Rejects tracker (timed offer)"
Cohesion: 0.05
Nodes (41): Card entrance animation via CSS @keyframes + animation-fill-mode: both, "Below cost" flag, bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, "No BOM" flag, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source) (+33 more)

### Community 7 - "monthly_report.py"
Cohesion: 0.07
Nodes (27): monthly_report_history.json, _bag_stock(), _cause(), _collect_comments(), _combo_bags(), fmt(), _garr_line(), gnum() (+19 more)

### Community 8 - "shops_efficiency.py"
Cohesion: 0.08
Nodes (22): apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _load_combos_by_shop(), _from_file(), _nonempty(), _metric() (+14 more)

### Community 9 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.06
Nodes (35): Card component (base building block), dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards), high-end-visual-design (related skill) (+27 more)

### Community 10 - "lib/db.py"
Cohesion: 0.06
Nodes (47): corporate_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine (+39 more)

### Community 11 - "current_performance.py"
Cohesion: 0.08
Nodes (17): fetch_monthly_target(), master_from_db(), monthly_from_db(), current_performance.py…, Reporting month's NET catalogue bags from Postgres (monthly_sales_db.json,…, Reporting month's reject-clearance bags ([REJECT] tag) from…, Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Sunday that starts the Sun–Sat sales week containing d. (+9 more)

### Community 12 - "self_made_combos_bundle/offer_data.py"
Cohesion: 0.14
Nodes (18): Shared Google Sheets authentication for every dashboard generator. Two modes,…, build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), cell(), find_row(), find_row_any() (+10 more)

### Community 13 - "json"
Cohesion: 0.12
Nodes (18): One-off: restore August's Offer Type figures into monthly_report_history.json…, Current Performance (doc), json, excluded_products(), master_products(), _norm_name(), lib/queries.py — SQL for the Litmus Postgres source of truth (Odoo POS). Bags…, Lower-cased product names to drop from Total Sales. Returns a sentinel when the… (+10 more)

### Community 14 - "lib/report_month.py"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 15 - "self_made_combos_bundle/lib/report_month.py"
Cohesion: 0.17
Nodes (19): anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name(), month_window() (+11 more)

### Community 16 - "Marketing Dashboard Insights Page"
Cohesion: 0.25
Nodes (8): Bare Minimum (Bags to be Sold) KPI, What's Going Well Section, Headline Numbers KPI Grid, Marketing Dashboard Insights Page, Recommended Actions This Week Section, Regional Posting Comparison Section (Kenya/Sinza/Uganda), Spectral Edge aura backdrop (decorative fixed gradient layers), Top 5 New Products by Monthly Sales Table

### Community 17 - "fetch_offer_data"
Cohesion: 0.17
Nodes (18): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), cell(), find_row(), find_row_any(), header_at_or_below() (+10 more)

### Community 18 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 19 - "main.py"
Cohesion: 0.12
Nodes (18): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), Denri Africa — Marketing Dashboard Launcher…, This machine's address on the local network (for the share URL). (+10 more)

### Community 20 - "build_payload"
Cohesion: 0.16
Nodes (15): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+7 more)

### Community 21 - "Dashboard Insights skill"
Cohesion: 0.17
Nodes (16): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Current Performance Dashboard Page, Forward Projections section, PERF data block (weekly/monthly sales KPIs), PROJ data block (forward projections, velocity factor, bare minimum), Monthly Report (doc) (+8 more)

### Community 22 - "shops_dispatch.py"
Cohesion: 0.21
Nodes (14): build_period(), distributed_in(), main(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only., Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).… (+6 more)

### Community 23 - "Product / name matching (doc)"
Cohesion: 0.18
Nodes (14): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix) (+6 more)

### Community 24 - "July 2026 Monthly Report Page"
Cohesion: 0.18
Nodes (12): What Needs Attention Section, Finding: Uganda marketing conversion at 7.4%, below critical threshold, Finding: 5,572 bags in stock not posted, 53% of stock invisible, Section 1: Current Performance, July 2026 Monthly Report Page, Section 2: New Products, Section 3: Offer Type Analysis, Section 4: Posting Yields (Sales from Accurate Posting) (+4 more)

### Community 25 - "self_made_combos_bundle/self_made_combos.py"
Cohesion: 0.20
Nodes (11): fetch(), fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py…, Read the Shop → Region table from docs/shop-regions.md so the mapping can be…, Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer… (+3 more)

### Community 26 - "fetch"
Cohesion: 0.18
Nodes (9): _bags_not_on_offer(), fetch(), The component bag names across a region's sheet combos/singles/specials cards…, Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, Bags with sales this month (in the market `sql` scopes to) that are on NO…, _read_deals(), _read_offer_analysis() (+1 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.16
Nodes (16): Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, lib/db.py (Supabase session pooler DB access), lib/db.run_query (shared connection reuse per subprocess), Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics (+8 more)

### Community 28 - "Self-made combos vs running combos (doc)"
Cohesion: 0.18
Nodes (13): Bags not on offer per market (Kenya/Sinza/Uganda), Combo button usage / rung vs pot. (till check), Self-made combos vs running combos (doc), DoW mirror shops (DOW_MIRROR), Monetary implication panel (bundling discount), Rank chip (follows active Sort filter), Running-combo classification by bag composition (slot-aware sheet match), Standalone SQL (self_made_vs_running_combos.sql) (+5 more)

### Community 29 - "_enrich_deals"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "history.py"
Cohesion: 0.06
Nodes (42): denri_mkt_timed_offer* Supabase tables, month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), dotenv, fetch_months(), bucket(), inject() (+34 more)

### Community 31 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 32 - "bags_on_offer.py"
Cohesion: 0.09
Nodes (31): _as_date(), _build_period(), fetch(), base(), classify(), new_of(), resolve(), rows() (+23 more)

### Community 33 - "streamlit_app.py"
Cohesion: 0.17
Nodes (7): SCRIPT_TIMEOUT = 600s config, streamlit, _load_secrets_into_env(), streamlit_app.py — Denri Marketing Dashboard on Streamlit. Serves the existing…, streamlit_components_v1, subprocess, time

### Community 34 - "start_server"
Cohesion: 0.26
Nodes (11): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_refresh(), _run_ref() (+3 more)

### Community 35 - "_combo_button_usage"
Cohesion: 0.22
Nodes (8): _combo_button_usage(), _combo_norm_option(), _combo_odoo_slots(), _matches_sheet(), One combo slot-option → its distinctive bag token(s), colours/category words…, Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…, The sheet label this Odoo combo maps to (same slot count, every slot overlaps),…, Per running combo: units rung through the combo button (Odoo) vs the sheet's…

### Community 36 - "month_end.py"
Cohesion: 0.31
Nodes (8): clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.…, YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that…, After the closing month's timed offers are safely in Supabase, empty the config…, run(), target_month(), sys

### Community 37 - "timed_offers.py (generator)"
Cohesion: 0.10
Nodes (20): renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator), Timed Offers Section — Back to School Edition (Report), Secrets excluded via .gitignore / .vercelignore, google_auth.py (shared auth module) (+12 more)

### Community 38 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.20
Nodes (10): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.html page (+2 more)

### Community 40 - "forward_projections.py"
Cohesion: 0.13
Nodes (11): calendar, _corporate_bags(), fetch_sheet_data(), odoo_weekly_breakdown(), _perfect_week_index(), forward_projections.py…, Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat… (+3 more)

### Community 41 - "_enrich_deals"
Cohesion: 0.16
Nodes (9): _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,… (+1 more)

### Community 42 - "Forward Projections Page"
Cohesion: 0.29
Nodes (7): Menu 1: Current Performance, Bare Minimum (Growth %) KPI, Declined By KPI (bags missed that week), Forecasted Projection KPI (with corporate in mind), Forward Projections Page, PROJ_DATA_START/PROJ_DATA_END injected JSON data block, Standard Projection KPI (% of Total Target)

### Community 43 - "On-offer definition per region (from SMC block)"
Cohesion: 0.25
Nodes (8): Dead Stock Accountability tuning knobs, Per-region high-stock floors (Kenya 20, Sinza 5, Uganda 5), weak_max threshold (sold < 5 = weak sales), On-offer definition per region (from SMC block), Reject Sale margin report (converted xlsx), 'below cost' margin flag, 'pinned' flag, 'thin' margin flag

### Community 44 - "Offer Picking (doc)"
Cohesion: 0.29
Nodes (8): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES)

### Community 45 - "Combos & Power Deals by Shop panel (#combo-shop)"
Cohesion: 0.29
Nodes (7): Combos & Power Deals by Shop panel (#combo-shop), compute_period() function (emits pushDetail per period), Deal of the Week — Tier 2 (latest 2-week window) shop-scoped view, DenriTableFilter reusable filter bar component, DOW_MIRROR expansion (Starmall to Hazina/Hilton/KTDA), odoo_stock_levels() function, Push via filter (None / power deal / deal of the week tag)

### Community 46 - "Sidebar Navigation (icon rail / expanded drawer)"
Cohesion: 0.20
Nodes (12): Live view vs archive split (lib/report_month.py live_*), Denri Africa · Marketing Dashboard (README, project overview), dash-frame iframe (dashboard content loader), exportExcel() function, history.html (nav target — Reporting History, Supabase), Marketing Dashboard Shell (shell.html), navigate() function, new_products.html (nav target) (+4 more)

### Community 47 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.13
Nodes (17): google_auth.py (Sheets auth), offer_data.build (batched Sheets range fetch), lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, google_auth.py (service account or OAuth desktop), gspread>=6.0 dependency (Google Sheets access) (+9 more)

### Community 49 - "history.py (read months back)"
Cohesion: 0.29
Nodes (8): denri_mkt_* Supabase tables, Reporting History (Supabase) spec doc, history.html page, history.py (read months back), month_end.py (freezes a month), push_to_supabase.py (write months), Resilience fallback: history.py leaves existing page data untouched if Supabase unreachable, supabase_migration.py (schema)

### Community 50 - "Self-made combos vs Running combos portable bundle README"
Cohesion: 0.17
Nodes (13): shop-regions.md (editable Shop to Region table), Composition-based classification rationale (Running vs Self-made), _matches_sheet / _build_sheet_slots slot-aware matching functions, Self-made combos vs Running combos portable bundle README, Returns netting rationale (qty <> 0, returns subtract), docs/self-made-combos.md full spec for the menu, docs/shop-regions.md editable shop to region map, sql/self_made_vs_running_combos.sql (standalone pure-SQL classification) (+5 more)

### Community 51 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 52 - "datetime"
Cohesion: 0.24
Nodes (8): datetime, lib — shared data-access for the marketing dashboard (Postgres migration).…, main(), date, _query_ready(), weekly_sales.py — the weekly-sales fix. Computes the CURRENT Sun–Sat week's…, The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's…, week_window()

### Community 53 - "_combo_norm_option"
Cohesion: 0.38
Nodes (6): _combo_norm_option(), combos_by_shop(), _norm(), _tokmatch(), Per-shop view for Shops Efficiency, keyed by shop-location label (e.g.…, One combo slot-option → its distinctive bag token(s), colours/category words…

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "current_performance.html"
Cohesion: 0.25
Nodes (6): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance), Net-of-refunds rule (pl.qty <> 0 via _QTY_SQL), current_performance.html (nav target)

### Community 56 - "August 2026 Monthly Report"
Cohesion: 0.33
Nodes (6): August 2026 Monthly Report, New Products Section (Report), Offer Type Analysis Section (Report), Posting Yields Section (Report), monthly_report.html (nav target), POSTING (SALES YIELDS FROM ACCURATE POSTING).html (nav target)

### Community 57 - "build_all.py"
Cohesion: 0.40
Nodes (4): build_all.py ────────────────────────────────────────────────────────────────…, Vercel hosted version (static snapshot), vercel.json, Vercel static deployment (serves committed HTML, no build step)

### Community 58 - "_combo_button_usage"
Cohesion: 0.33
Nodes (4): _combo_button_usage(), _matches_sheet(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, The sheet label this Odoo combo maps to (same slot count, every slot overlaps),…

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "self_made_combos.py"
Cohesion: 0.50
Nodes (4): Per-shop combo-button chips (red when < half best-in-region), self_made_combos.py, Shop -> Region table, self_made_combos.html (nav target)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "_build_sheet_slots"
Cohesion: 0.50
Nodes (4): _build_sheet_slots(), _combo_sheet_slots(), Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]., [(label, slots)] for each running combo on the offer sheet (skips the TOTAL…

### Community 65 - "render(idx) function"
Cohesion: 0.50
Nodes (4): buildCharts(m, wk, prevM) function, render(idx) function, selfMadeHtml(m) function, timedOffersHtml(m) function

### Community 66 - "_offer_active_today"
Cohesion: 0.50
Nodes (4): _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, start_daily_snapshot()

### Community 67 - "buildExportDoc(mode) function"
Cohesion: 0.50
Nodes (4): buildExportDoc(mode) function, colorizeForPaper() function, exportPDF() function, exportWord() function

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 85 - "self_made_combos.py"
Cohesion: 0.14
Nodes (17): _bag_sales_daily_sql(), _bag_sales_sql(), _build_sheet_slots(), dow_tier_weeks(), _dstr(), fmt(), inject(), _load_shop_regions() (+9 more)

## Ambiguous Edges - Review These
- `Legacy dated report_YYYY_month.html archive pattern` → `August 2026 Monthly Report`  [AMBIGUOUS]
  report_2026_august.html · relation: conceptually_related_to
- `Reject Sale page (reject_sales.html)` → `Card entrance animation via CSS @keyframes + animation-fill-mode: both`  [AMBIGUOUS]
  .claude/skills/dashboard-design.md · relation: conceptually_related_to

## Knowledge Gaps
- **144 isolated node(s):** `PERF`, `graphify`, `Period selector (Monthly / Weekly / Last week)`, `Counted by how it was sold`, `What the page shows (per period)` (+139 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 521 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Legacy dated report_YYYY_month.html archive pattern` and `August 2026 Monthly Report`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Reject Sale page (reject_sales.html)` and `Card entrance animation via CSS @keyframes + animation-fill-mode: both`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `Current Performance (doc)` connect `json` to `forward_projections.py`, `current_performance.py`, `datetime`, `Product / name matching (doc)`, `build_all.py`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `New Products Analytics (doc)` connect `Product / name matching (doc)` to `json`, `Dashboard Insights skill`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `get_gspread_client()` connect `POSTING (SALES YIELDS FROM ACCURATE POSTING).py` to `bags_on_offer.py`, `offer_picking.py`, `timed_offers.py`, `new_products.py`, `forward_projections.py`, `shops_efficiency.py`, `current_performance.py`, `self_made_combos_bundle/offer_data.py`, `fetch_offer_data`, `self_made_combos.py`, `self_made_combos_bundle/self_made_combos.py`, `fetch`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **What connects `PERF`, `graphify`, `Period selector (Monthly / Weekly / Last week)` to the rest of the system?**
  _144 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `POSTING (SALES YIELDS FROM ACCURATE POSTING).py` be split into smaller, more focused modules?**
  _Cohesion score 0.054203180785459264 - nodes in this community are weakly interconnected._