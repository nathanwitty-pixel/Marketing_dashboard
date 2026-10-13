# Graph Report - Marketing_dashboard  (2026-10-13)

## Corpus Check
- 192 files · ~785,621 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 16 file(s) not represented in the graph (top: .csv 9, (none) 2, .toml 1)

## Summary
- 2088 nodes · 3982 edges · 136 communities (115 shown, 21 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 157 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b911fd54`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- posting_yields.py
- laya.py
- tests/test_receipt_combos.py
- oos_chip.js
- chart_switcher.js
- graw(block, key) function (bare numeric getter)
- Kitengela Rejects tracker (timed offer)
- generators/self_made_combos.py
- check_connection
- v5_theme.js
- timed_offers.py
- bare_minimum setting (weekly target floor)
- generators/bag_signals.py
- lib/db.py
- month_extras.py
- stock.py
- publish.py
- forward_projections.py
- build_payload
- main.py
- shop_corporate.py
- push_planner.py
- self_made_combos_bundle/self_made_combos.py
- Self-made combos vs running combos (doc)
- shops_efficiency.py
- signals
- paths.py
- Dashboard Menu Docs (spec index)
- bags_on_offer.py
- _enrich_deals
- fetch
- insights.html
- streamlit_app.py
- current_performance.py
- monthly_report.py
- _combo_button_usage
- chronos_train.py
- offer_picking.py
- build_payload
- Shops Efficiency Tracking spec doc
- shop_launch.py
- shops_dispatch.py
- lib/offer_data.py
- page_sidebar.js
- Month-End Routine
- Combos & Power Deals by Shop panel (#combo-shop)
- self_made_combos_bundle/offer_data.py
- Self-made combos bundle Python dependencies (requirements.txt)
- CLAUDE.md
- history.py (read months back)
- Self-made combos vs Running combos portable bundle README
- timed_offers.py (generator)
- datetime
- new_products.py
- algorithmic-art skill
- dataviz-charts skill
- bag_classifier
- _combo_button_usage
- _enrich_deals
- High-End Visual Design skill
- bag_quant.py
- product_targets.py
- oos_callbacks.py
- daydream skill (Vault Daydream)
- data
- OOS call-back progress (Ralph loop log)
- google_auth.py (shared auth module)
- fetch_new_products_data
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- history.py
- lib/report_month.py
- num
- base_name
- moves
- shop_birthdays.py
- test_product_targets.py
- _build_period
- _bags_not_on_offer
- os
- theme.py
- push_laya.py
- queries.py
- test_push_planner.py
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- start_server
- Chart type switcher (every chart, every menu)
- F
- weekly_sales.py
- test_stockout_demand.py
- Out-of-stock demand — people, not requests
- Denri Africa Dashboard Design System (skill)
- push_rules.py
- get_gspread_client
- Ralph task — "Out of stock — call back" demand per shop
- update_np_weekly_history
- Bags on offer vs not on offer
- _apply_receipt_offers
- _opt_close
- Bag Signals — quant view of each bag (posting · stock · selling)
- get_rows
- current_performance.html
- attach
- self_made_combos.py generator (build_payload + SQL + injection)
- followup
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- _odoo_colour
- _bag_stock
- Ralph task — only three sheet tabs left
- _load_combos_by_shop
- Bag targets October 2026_3acbad00.md
- _offer_active_today
- Ralph task — deals from the posters (deals_kenya.csv)
- perf_data.js
- self_made_combos_bundle/lib/__init__.py
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- gstr(block, key) function (string field regex getter)
- Key-rename / run-order gotcha (blanks or zeros)
- _build_sheet_slots
- colours.py
- lib
- NEW_PROD data block (New Products)
- OFFER_DATA data block (Self Made Combos)
- odoo_tabs.py
- POST_DATA data block (Posting)
- Product (bag) targets
- read_block(file, start, end) function
- html
- contextlib
- run_query
- denri_mkt_timed_offer* Supabase tables
- Shop Launch
- json

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 50 edges
2. `fetch_posting_data()` - 35 edges
3. `fetch()` - 34 edges
4. `get_gspread_client()` - 29 edges
5. `build_payload()` - 28 edges
6. `check_connection()` - 28 edges
7. `data()` - 25 edges
8. `build_payload()` - 24 edges
9. `build_offer()` - 22 edges
10. `F()` - 22 edges

## Surprising Connections (you probably didn't know these)
- `Buckets` --references--> `bag_classifier()`  [INFERRED]
  docs/bags-on-offer.md → generators/self_made_combos.py
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

## Communities (136 total, 21 thin omitted)

### Community 0 - "posting_yields.py"
Cohesion: 0.05
Nodes (74): _alignment_region(), _for(), _onoff(), _sold(), _stk(), _units(), _analyze_region(), _bt_on_offer() (+66 more)

### Community 1 - "laya.py"
Cohesion: 0.09
Nodes (26): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket() (+18 more)

### Community 2 - "tests/test_receipt_combos.py"
Cohesion: 0.08
Nodes (43): What the page shows (per period), _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, bag_key(), classify(), _fits(), _groups(), load_offers() (+35 more)

### Community 3 - "oos_chip.js"
Cohesion: 0.08
Nodes (38): attach(), close(), esc(), form(), go(), iso(), mountPanel(), open() (+30 more)

### Community 4 - "chart_switcher.js"
Cohesion: 0.13
Nodes (33): alpha(), apply(), attach(), axisOpts(), build(), changeTxt(), Chart(), clone() (+25 more)

### Community 6 - "Kitengela Rejects tracker (timed offer)"
Cohesion: 0.07
Nodes (28): bom_costs.json (offline fallback mirror), build() function (writes xlsx export), _CAT_KEYWORDS fallback rule, offer_picking._read_bom_costs (BOM reader), offer_picking._read_offers (category source), Offline fallback pattern (mirror sheet data to local JSON), Reject Sale (doc: reject_sales.py -> reject_sales.html, RJ), reject_sales_export.csv (fallback export) (+20 more)

### Community 7 - "generators/self_made_combos.py"
Cohesion: 0.10
Nodes (25): Counted by how it was sold, _load_source(), bags_offer_source.json if written in the last 15 min for this month (and it has…, _bag_sales_daily_sql(), _bag_sales_sql(), _bags_not_on_offer(), dow_tier_weeks(), fetch() (+17 more)

### Community 8 - "check_connection"
Cohesion: 0.10
Nodes (22): build_offer(), odoo_bag_daily_value(), odoo_bag_prices(), odoo_bulk_lines(), odoo_daily_kenya(), odoo_list_price(), odoo_offer_price(), odoo_window_sales() (+14 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "timed_offers.py"
Cohesion: 0.12
Nodes (24): _bags_from_file(), _bucket(), _derive_month(), kenya_stock_by_bag(), load_config(), _norm_offer(), _parse_colour(), timed_offers.py… (+16 more)

### Community 12 - "generators/bag_signals.py"
Cohesion: 0.18
Nodes (11): build(), _posts(), bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), bag_posts(), load() (+3 more)

### Community 13 - "lib/db.py"
Cohesion: 0.09
Nodes (30): dotenv, check_connection(), _drop_shared_conn(), _env(), get_engine(), DataFrame, Engine, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME… (+22 more)

### Community 14 - "month_extras.py"
Cohesion: 0.17
Nodes (18): load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, _bags_on_offer(), _block(), build_extras(), _deals(), _pick() (+10 more)

### Community 15 - "stock.py"
Cohesion: 0.24
Nodes (13): _codes_for(), _inlist(), odoo_stock_at_location(), odoo_stock_by_product(), odoo_stock_by_shop_code(), _ok(), _qty(), lib/stock.py — live Odoo on-hand stock, per product / market / shop. Single… (+5 more)

### Community 16 - "publish.py"
Cohesion: 0.21
Nodes (14): argparse, fnmatch, py_compile, changed_files(), git(), group(), is_secret(), main() (+6 more)

### Community 17 - "forward_projections.py"
Cohesion: 0.15
Nodes (11): _corporate_bags(), _live_bags(), odoo_weekly_breakdown(), _perfect_week_index(), forward_projections.py…, Ordinal of d's Sun–Sat week within the month, counting EVERY week that has at…, Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, Corporate bags sold in the given month, live from Odoo invoices. Returns 0 when… (+3 more)

### Community 18 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 19 - "main.py"
Cohesion: 0.12
Nodes (21): http_server, ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), Denri Africa — Marketing Dashboard Launcher…, This machine's address on the local network (for the share URL). (+13 more)

### Community 20 - "shop_corporate.py"
Cohesion: 0.17
Nodes (21): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), _acronym(), build(), _maybe(), owns(), _d(), _domain() (+13 more)

### Community 21 - "push_planner.py"
Cohesion: 0.13
Nodes (22): build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), main(), month_progress() (+14 more)

### Community 22 - "self_made_combos_bundle/self_made_combos.py"
Cohesion: 0.20
Nodes (11): fetch(), fmt(), inject(), _load_shop_regions(), main(), self_made_combos.py…, Read the Shop → Region table from docs/shop-regions.md so the mapping can be…, Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the Offer… (+3 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.06
Nodes (45): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Current Performance (doc), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), New Products Analytics (doc) (+37 more)

### Community 24 - "shops_efficiency.py"
Cohesion: 0.11
Nodes (16): apply_odoo(), compute_regions(), fmt_pct(), load_dispatch(), _metric(), metric_byshop(), odoo_stock_levels(), parse_sheet() (+8 more)

### Community 25 - "signals"
Cohesion: 0.09
Nodes (29): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+21 more)

### Community 26 - "paths.py"
Cohesion: 0.15
Nodes (11): lib/new_products_list.py — which bag types count as this month's NEW PRODUCTS.…, generator(), lib/paths.py — where every kind of file lives. Use these instead of building…, clear_timed_offers(), main(), month_end.py — the end-of-month archival routine.…, YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month that…, After the closing month's timed offers are safely in Supabase, empty the config… (+3 more)

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.18
Nodes (14): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics, Odoo Stock Codes convention (shop-code locations vs WIP/holding codes) (+6 more)

### Community 28 - "bags_on_offer.py"
Cohesion: 0.13
Nodes (19): _bag_tiers(), _base_windows(), _custom_range(), fmt(), _has_deals(), inject(), main(), _new_products() (+11 more)

### Community 29 - "_enrich_deals"
Cohesion: 0.18
Nodes (7): _enrich_deals(), _match(), _full(), _full_of(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,…, Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to…

### Community 30 - "fetch"
Cohesion: 0.15
Nodes (21): _as_date(), fetch(), cat_tier(), classify(), classify_for(), make_classifier(), base(), classify() (+13 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.07
Nodes (26): cache_resource, SCRIPT_TIMEOUT = 600s config, fragment, hashlib, streamlit, _bg_done_msg(), _bg_jobs(), _bg_rebuild() (+18 more)

### Community 33 - "current_performance.py"
Cohesion: 0.12
Nodes (13): corporate_clients_from_db(), _months(), current_performance.py…, Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],…, Current month's corporate activity per client (quoted · invoiced · paid · sold)…, Sunday that starts the Sun–Sat sales week containing d. (+5 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.14
Nodes (10): _cause(), esc(), fmt(), ladder_strip(), pct(), monthly_report.py…, read_block(), _read_timed_offers() (+2 more)

### Community 35 - "_combo_button_usage"
Cohesion: 0.12
Nodes (17): best_match(), _build_sheet_slots(), _combo_button_usage(), _combo_norm_option(), _combo_odoo_slots(), _combo_sheet_slots(), combos_by_shop(), _norm() (+9 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.12
Nodes (29): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+21 more)

### Community 37 - "offer_picking.py"
Cohesion: 0.06
Nodes (49): csv, Offer type summary (matrix), _alt_cost(), _apply_alias(), build(), _build_catalog(), _combo_cost(), _combo_slots() (+41 more)

### Community 38 - "build_payload"
Cohesion: 0.15
Nodes (15): build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly(), _num2() (+7 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.22
Nodes (9): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.py generator (+1 more)

### Community 40 - "shop_launch.py"
Cohesion: 0.20
Nodes (14): build(), _cfg(), first_sale(), kenya_posts(), load_workplan(), make_matcher(), match(), _parse_workplan() (+6 more)

### Community 41 - "shops_dispatch.py"
Cohesion: 0.21
Nodes (14): build_period(), distributed_in(), main(), month_window(), _num(), shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.…, Per-shop bags SOLD from Odoo POS, Kenya shops only., Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).… (+6 more)

### Community 42 - "lib/offer_data.py"
Cohesion: 0.20
Nodes (12): build(), complete_weeks_remaining(), data_rows_count(), fetch_offer_data(), fmt_int(), is_checked(), _offer_tables(), offer_data.py ─────────────────────────────────────────────────────────────────… (+4 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

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

### Community 51 - "timed_offers.py (generator)"
Cohesion: 0.22
Nodes (9): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+1 more)

### Community 52 - "datetime"
Cohesion: 0.06
Nodes (57): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+49 more)

### Community 53 - "new_products.py"
Cohesion: 0.16
Nodes (10): _base_colour(), is_checked(), _merge_rows_by_base_colour(), odoo_stock_kenya_outside(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across… (+2 more)

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.17
Nodes (12): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), DATA_START/DATA_END comment marker injection pattern, dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.) (+4 more)

### Community 56 - "bag_classifier"
Cohesion: 0.19
Nodes (14): _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _load_bag_prices(), _norm_combo() (+6 more)

### Community 57 - "_combo_button_usage"
Cohesion: 0.22
Nodes (8): _combo_button_usage(), _combo_norm_option(), _combo_odoo_slots(), _matches_sheet(), One combo slot-option → its distinctive bag token(s), colours/category words…, Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…, The sheet label this Odoo combo maps to (same slot count, every slot overlaps),…, Per running combo: units rung through the combo button (Odoo) vs the sheet's…

### Community 58 - "_enrich_deals"
Cohesion: 0.16
Nodes (9): _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg(), _odoo_stock_by_shop(), {sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,… (+1 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "bag_quant.py"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), lib/bag_quant.py — quant signals per bag: drift, volatility, Sharpe-style…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

### Community 61 - "product_targets.py"
Cohesion: 0.13
Nodes (22): collections, tally(), available_days(), bag_key_fn(), key(), base_period(), build(), load_targets() (+14 more)

### Community 62 - "oos_callbacks.py"
Cohesion: 0.07
Nodes (52): Out of stock — call back, fixture, bag(), aggregate(), flat(), split(), attach_stock(), in_stock() (+44 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "data"
Cohesion: 0.15
Nodes (13): cache_data, _archived_source(), bags_offer_source_<YYYY-MM>.json — that month's archived on-offer list, or None., load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if…, _till_to_shop() (+5 more)

### Community 65 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.15
Nodes (11): _local_deal_rows(), Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), Blocker counter, Deals from posters (RALPH_DEALS.md) — 2026-10-04, Final summary, Log (+3 more)

### Community 66 - "google_auth.py (shared auth module)"
Cohesion: 0.15
Nodes (13): Vercel hosted version (static snapshot), Secrets excluded via .gitignore / .vercelignore, google_auth.py (shared auth module), google_credentials.json (OAuth desktop client), Marketing Dashboard — Google Sheets access & setup (doc), google_token.json (OAuth token), main.py (refresh + serve dashboard), OAuth token expiry issue (Testing mode, ~7 day expiry) (+5 more)

### Community 67 - "fetch_new_products_data"
Cohesion: 0.26
Nodes (11): fetch_new_products_data(), _apply_stock(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_sales_window(), Re-key an Odoo {name: value} dict by _key(), merging values of names that… (+3 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "history.py"
Cohesion: 0.31
Nodes (10): fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers…, Like _num, but leaves booleans alone and renders dates as ISO strings — the… (+2 more)

### Community 71 - "lib/report_month.py"
Cohesion: 0.08
Nodes (40): calendar, anchor(), is_pinned(), live_anchor(), live_month_key(), live_month_window(), month_key(), month_name() (+32 more)

### Community 72 - "num"
Cohesion: 0.20
Nodes (11): _garr_line(), gnum(), num(), _offers(), _parse_offers(), _units(), This month's timed-offer campaigns, flattened for storage. The live TO payload…, Greedy single-line array extractor — handles nested [[...],[...]] arrays. (+3 more)

### Community 73 - "base_name"
Cohesion: 0.20
Nodes (11): apply_walkins(), base_name(), dispatch_by_product_shop(), _num(), The catalogue key for an Odoo product name: norm() without the "[REJECT]" tag…, {NORM(product): {SHOP: bags}} of POS bag sales in [start, end]; None if DB…, {NORM(product): {SHOP: bags distributed in}} from combined_distribution.sql's…, {NORM(product): {SHOP: on-hand}} live, Kenya shops + Sinza (DAR) + Uganda (UG). (+3 more)

### Community 74 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "test_product_targets.py"
Cohesion: 0.31
Nodes (8): allocate(), Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for lib/product_targets.py (bag targets from Odoo; spec docs/product-…, test_min_days_stops_a_brand_new_bag_inflating(), test_monthly_target_rows_swaps_column_c(), test_new_bag_is_scaled_to_the_days_it_was_in_shops(), test_no_zero_targets_and_exact_total(), test_out_of_stock_days_do_not_count()

### Community 77 - "_build_period"
Cohesion: 0.20
Nodes (6): _build_period(), _offer_types(), _pick_target(), Latest target row for `shop` with this period that overlaps [start, end]. A…, Matrix payload: rows, per-row category / tier cells, and the period's Top-5…, _region_of()

### Community 78 - "_bags_not_on_offer"
Cohesion: 0.33
Nodes (6): _bags_not_on_offer(), _infer(), _norm(), _load_bag_prices(), {BAG_UPPER: original full price} from bag_original_prices.json — the baseline…, Bags with sales this month that are on NO offer — i.e. not a running-combo…

### Community 79 - "os"
Cohesion: 0.09
Nodes (22): ambiguous_python_import_17686b6faac5, main(), push_to_supabase.py — run the marketing migration against Supabase. Regenerates…, lib — shared data-access for the marketing dashboard (Postgres migration).…, main(), month_block(), num(), q() (+14 more)

### Community 80 - "theme.py"
Cohesion: 0.20
Nodes (9): css_variables(), gradient_css(), hex_to_rgba(), product_swatch(), lib/theme.py ─────────────────────────────────────────────────────────────────…, Return the display hex for a product colour NAME (case-insensitive)., #1e2130', 0.5 -> 'rgba(30, 33, 48, 0.5)'., gradient_css('green') -> 'linear-gradient(90deg, #10b981, #06b6d4)'. (+1 more)

### Community 81 - "push_laya.py"
Cohesion: 0.13
Nodes (20): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+12 more)

### Community 82 - "queries.py"
Cohesion: 0.18
Nodes (10): main(), month_window(), _query_ready(), monthly_sales.py — the current month's real bags sold, from Postgres. The…, First → last calendar day of the LIVE month (today's month; see…, master_products(), _norm_name(), lib/queries.py — SQL for the Litmus Postgres source of truth (Odoo POS). Bags… (+2 more)

### Community 83 - "test_push_planner.py"
Cohesion: 0.17
Nodes (19): Per bag × market: the facts (`push_rules.facts`, `add_peers`), add_peers(), _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m… (+11 more)

### Community 84 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

### Community 85 - "start_server"
Cohesion: 0.31
Nodes (8): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_to_config(), _json()

### Community 86 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.29
Nodes (6): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does

### Community 87 - "F"
Cohesion: 0.24
Nodes (16): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), A facts row with sensible defaults, overridden by kw., test_fallback_slow_seller_or_overstocked() (+8 more)

### Community 88 - "weekly_sales.py"
Cohesion: 0.32
Nodes (6): fetch_monthly_target(), main(), _query_ready(), weekly_sales.py — the weekly-sales fix. Computes the CURRENT Sun–Sat week's…, The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's…, week_window()

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.08
Nodes (20): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests, Agent skills — retail analytics, Test a skill (+12 more)

### Community 91 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.06
Nodes (36): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), design-taste-frontend (related skill), Design Tokens (colors, typography, spacing), Signature Element — Flowing Border (achievement cards) (+28 more)

### Community 92 - "push_rules.py"
Cohesion: 0.10
Nodes (21): action(), _cover_txt(), _kind(), _n(), not_moving(), posting_median(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).…, {market: median postsMonth of the bags that were posted at all} — the 'below… (+13 more)

### Community 93 - "get_gspread_client"
Cohesion: 0.32
Nodes (5): fetch_sheet_data(), get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,…, main(), One-command Google re-authorization. python scripts/reauth.py Deletes any stale…

### Community 94 - "Ralph task — "Out of stock — call back" demand per shop"
Cohesion: 0.25
Nodes (7): match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, Established facts (do not re-investigate), Every iteration, Periods (dates in Africa/Nairobi), Ralph task — "Out of stock — call back" demand per shop, Stopping

### Community 95 - "update_np_weekly_history"
Cohesion: 0.29
Nodes (7): _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)., Ordinal among the month's perfect weeks (>=5 days in month), so the first FULL…, Snapshot each Sun–Sat week (sales, Kenya/Outside posts) into…, update_np_weekly_history()

### Community 96 - "Bags on offer vs not on offer"
Cohesion: 0.20
Nodes (10): Bags on offer vs not on offer, Buckets, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Regenerate, Shop birthdays, Shop metrics (vs the Odoo revenue target) (+2 more)

### Community 97 - "_apply_receipt_offers"
Cohesion: 0.25
Nodes (6): _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region…, _region_goal(), _till_targets()

### Community 98 - "_opt_close"
Cohesion: 0.25
Nodes (7): _opt_close(), Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Same slot count and every slot overlaps under SOME pairing (any order: the…, _slots_fit(), Inputs (from the user, Oct 2026), Ralph task — Sinza & Uganda offers + receipt-based combo counting, Steps

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "get_rows"
Cohesion: 0.25
Nodes (8): load(), default_window(), get_rows(), last_complete_week(), The most recent COMPLETE Sun–Sat week before `ref` (today) — what the sheet's…, Sheet-shaped rows for `tab` built from Odoo, or None when Postgres is…, The tab's rows in the sheet's layout, built from Odoo. No sheet fallback (Oct…, tab_rows()

### Community 101 - "current_performance.html"
Cohesion: 0.50
Nodes (4): current_performance.html, monthly_report_history.json, Sales-card reject split line ("N POS + C corporate · R rejects"), PERF/PROJ data block (Current Performance)

### Community 102 - "attach"
Cohesion: 0.43
Nodes (5): attach(), page(), behaviour(), injectCss(), reveal()

### Community 103 - "self_made_combos.py generator (build_payload + SQL + injection)"
Cohesion: 0.29
Nodes (7): lib/report_month.py live_month_window(), Menu 4: Self made combos vs running combos, bag_original_prices.json full-price catalogue, self_made_combos.build_payload(month_start, month_end) function, lib/report_month.py (which month are we reporting?), self_made_combos.html static page (reads const SMC), self_made_combos.py generator (build_payload + SQL + injection)

### Community 104 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "_odoo_colour"
Cohesion: 0.33
Nodes (6): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, _aliases(), odoo_name(), {NORM(odoo name): NORM(sheet name)} from product_aliases.csv — products Odoo…, Odoo's spelling of a catalogue name (the reverse of product_aliases.csv), for…

### Community 107 - "_bag_stock"
Cohesion: 0.40
Nodes (5): _bag_stock(), _combo_bags(), _norm_bag(), Space/punctuation-insensitive key so 'MINIZURI' matches 'MINI ZURI'., Component bags of an offer, each with its stock, sorted most-stock first.

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "_load_combos_by_shop"
Cohesion: 0.67
Nodes (4): _load_combos_by_shop(), _from_file(), _nonempty(), Per-shop combo / power-deal view for the panel — built **live from Odoo** via…

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "_offer_active_today"
Cohesion: 0.50
Nodes (4): _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py…, start_daily_snapshot()

### Community 112 - "Ralph task — deals from the posters (deals_kenya.csv)"
Cohesion: 0.50
Nodes (3): Facts, Ralph task — deals from the posters (deals_kenya.csv), Steps (verify each before the next)

### Community 121 - "_build_sheet_slots"
Cohesion: 0.50
Nodes (4): _build_sheet_slots(), _combo_sheet_slots(), Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]., [(label, slots)] for each running combo on the offer sheet (skips the TOTAL…

### Community 122 - "colours.py"
Cohesion: 0.19
Nodes (9): compute_period(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period., sum_by_shop(), family(), _load(), _norm(), lib/colours.py — colour FAMILY of a product (Brown, Black, Red, Beige, Grey,… (+1 more)

### Community 126 - "odoo_tabs.py"
Cohesion: 0.14
Nodes (21): _build(), build_rows(), catalog_rows(), _Deriver, _flag_cells(), _fmt(), load_catalog(), norm() (+13 more)

### Community 128 - "Product (bag) targets"
Cohesion: 0.29
Nodes (6): No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026)

### Community 138 - "run_query"
Cohesion: 0.12
Nodes (19): corporate_from_db(), corporate_target_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, This month's Odoo corporate target {bags, kes} (sales_pos_target, scope…, odoo_combo_product_bags(), odoo_lifetime_product_bags(), odoo_month_product_bags(), All-time bags per product from Odoo (no month window) — the lifetime sales of… (+11 more)

### Community 145 - "Shop Launch"
Cohesion: 0.29
Nodes (6): Config, Launch day, Marketing posts, Sales, Shop Launch, What the page shows

### Community 162 - "json"
Cohesion: 0.12
Nodes (14): One-off: restore August's Offer Type figures into monthly_report_history.json…, card(), esc(), fmt(), generate_insights.py…, read_block(), region_card(), json (+6 more)

## Knowledge Gaps
- **185 isolated node(s):** `PERF`, `graphify`, `Use in another project`, `Test a skill`, `Inputs you must build from the project's data` (+180 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 853 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Bags on offer vs not on offer` connect `Bags on offer vs not on offer` to `tests/test_receipt_combos.py`, `offer_picking.py`, `generators/self_made_combos.py`, `Denri Africa Dashboard Design System (skill)`, `oos_callbacks.py`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `run_query()` connect `run_query` to `posting_yields.py`, `tests/test_receipt_combos.py`, `generators/self_made_combos.py`, `check_connection`, `generators/bag_signals.py`, `lib/db.py`, `stock.py`, `forward_projections.py`, `build_payload`, `shop_corporate.py`, `_enrich_deals`, `fetch`, `current_performance.py`, `_combo_button_usage`, `chronos_train.py`, `offer_picking.py`, `build_payload`, `shop_launch.py`, `_combo_button_usage`, `_enrich_deals`, `product_targets.py`, `fetch_new_products_data`, `base_name`, `_bags_not_on_offer`, `queries.py`, `weekly_sales.py`, `_apply_receipt_offers`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `bag_classifier()` connect `bag_classifier` to `Bags on offer vs not on offer`, `Product (bag) targets`, `data`, `_apply_receipt_offers`, `generators/self_made_combos.py`, `Push Planner (`push_planner.py` → `push_planner.html`, `PP`)`, `push_planner.py`, `fetch`, `oos_callbacks.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **What connects `PERF`, `graphify`, `Use in another project` to the rest of the system?**
  _185 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `posting_yields.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05048766494549627 - nodes in this community are weakly interconnected._
- **Should `laya.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09411764705882353 - nodes in this community are weakly interconnected._
- **Should `tests/test_receipt_combos.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08418367346938775 - nodes in this community are weakly interconnected._