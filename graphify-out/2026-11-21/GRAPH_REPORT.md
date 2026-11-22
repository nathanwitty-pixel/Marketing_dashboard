# Graph Report - Marketing_dashboard  (2026-11-21)

## Corpus Check
- 241 files · ~1,222,473 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: .csv 14, (none) 2, .toml 1)

## Summary
- 2821 nodes · 5629 edges · 191 communities (147 shown, 44 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 198 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c7bb7ca8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- month_extras.py
- _ask
- lib/receipt_combos.py
- oos_chip.js
- chart_switcher.js
- he
- Kitengela Rejects tracker (timed offer)
- signals
- Denri Africa Dashboard Design System (skill)
- v5_theme.js
- name_match.py
- bare_minimum setting (weekly target floor)
- offer_data.py
- get_engine
- _enrich_deals
- Push Planner (`push_planner.py` → `push_planner.html`, `PP`)
- forward_projections.py
- le
- Ps
- push_rules.py
- sticky_controls.js
- shop_requests.py
- main.py
- Self-made combos vs running combos (doc)
- ls
- vs
- anime.umd.min.js
- Dashboard Menu Docs (spec index)
- odoo_marketing.py
- si
- Bags on offer vs not on offer
- self_made_combos.py
- streamlit_app.py
- stock.py
- monthly_report.py
- current_performance.py
- chronos_train.py
- _read_deals
- build_payload
- Shops Efficiency Tracking spec doc
- build
- marketing_posts.py
- moves
- page_sidebar.js
- _build_period
- Combos & Power Deals by Shop panel (#combo-shop)
- test_fixC_sql.py
- lib/db.py (Supabase session pooler DB access)
- CLAUDE.md
- history.py (read months back)
- je
- type_fn
- compute_period
- _combo_button_usage
- algorithmic-art skill
- dataviz-charts skill
- scripts/test_receipt_combos.py
- run.py
- run_query
- High-End Visual Design skill
- safe_int
- ns
- fetch_new_products_data
- daydream skill (Vault Daydream)
- write_bags_offer_source
- Monthly Report (doc)
- _read_offers
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- Month-End Routine
- _resolve_bag
- marketing_dashboard.sql
- fetch_posting_data
- build
- shop_birthdays.py
- kpi_anim.js
- _apply_receipt_offers
- shops_dispatch.py
- why_moved.js
- theme.py
- push_laya.py
- family
- facts
- build_offer
- sys
- offer_picking.py
- test_push_planner.py
- write_atomic
- test_stockout_demand.py
- Out-of-stock demand — people, not requests
- followup
- monthly_target_rows
- norm
- Dashboard Architecture (static HTML + Python generator + injected data block)
- negative_fixes.py
- custom_range.py
- oos_callbacks.py
- master_products
- Bag Signals — quant view of each bag (posting · stock · selling)
- beats.py
- current_performance.html
- attach
- Fix merge conflicts (two-machine workflow)
- snapshot.py
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- why_moved.py
- _bucket
- Ralph task — only three sheet tabs left
- check_connection
- Bag targets October 2026_3acbad00.md
- push_planner.py
- OOS call-back progress (Ralph loop log)
- perf_data.js
- realistic_rates
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- Sales-share targets per product
- DataFrame
- bag_classifier
- fetch
- What the page shows
- date
- Product (bag) targets
- test_share_targets.py
- contextlib
- Chart type switcher (every chart, every menu)
- denri_mkt_timed_offer* Supabase tables
- New Products Analytics (doc)
- _matches_sheet
- Offer Picking (doc)
- start_server
- build
- timed_offers.py (generator)
- scripts/receipt_combos.py
- _dead_stock_region
- new_products.py
- timed_offers.py
- Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)
- Menu 1 Current Performance in the 3-beat layout (preview)
- odoo_marketing_audit.py
- Footfall and Marketing (21 Oct 2026, user's call)
- Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)
- odoo_tabs.py
- Product Performance — Shop breakdown: progress
- _seasonality
- os
- Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)
- bags_on_offer.py
- _fetch_sinza_monthly
- Ralph loop brief — Footfall and Marketing page
- _bag_tiers
- Bag signals — quant finance applied to product sales
- ambiguous_python_import_17686b6faac5
- Bag Tracking
- shop_stock_levels.py
- Combos from receipts — running vs self-made
- render
- update_np_weekly_history
- build
- Odoo marketing data audit
- ODOO_MARKETING_AUDIT.md
- _alignment_region
- posting_yields.py
- base_name
- data
- product_performance.py

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 81 edges
2. `fetch()` - 41 edges
3. `fetch_posting_data()` - 39 edges
4. `data()` - 39 edges
5. `check_connection()` - 32 edges
6. `le` - 31 edges
7. `build_payload()` - 30 edges
8. `ls` - 26 edges
9. `build_offer()` - 24 edges
10. `excluded_products()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `What the page shows (per period)` --references--> `_market_records()`  [INFERRED]
  docs/bags-on-offer.md → generators/bags_on_offer.py
- `The split — by each bag's share of recent sales` --references--> `bag_classifier()`  [INFERRED]
  docs/product-targets.md → generators/self_made_combos.py
- `Inputs (read only — nothing is written to Odoo or the sheet)` --references--> `bag_classifier()`  [INFERRED]
  docs/push-planner.md → generators/self_made_combos.py
- `Sales pace to month end (19 Oct 2026)` --references--> `month_end_lift()`  [INFERRED]
  docs/shop-stock-levels.md → generators/shop_stock_levels.py
- `Period selector (Monthly / Weekly / Last week / Custom)` --references--> `live_month_window()`  [INFERRED]
  docs/bags-on-offer.md → lib/report_month.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]

## Communities (191 total, 44 thin omitted)

### Community 0 - "month_extras.py"
Cohesion: 0.07
Nodes (50): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, _bags_on_offer(), _block(), build_extras() (+42 more)

### Community 1 - "_ask"
Cohesion: 0.08
Nodes (21): Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket(), _cache_get(), _cache_put() (+13 more)

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

### Community 7 - "signals"
Cohesion: 0.18
Nodes (17): action(), _mean(), _phi(), posting_beta(), bag_signals.py — quant signals per product from daily sales + stock (skill:…, The first rule that fits (docs/bag-signals.md › Action)., Pure. daily = {bag: [units per day, oldest first]} over the window (None = not…, Slope of weekly sales on weekly posts for a bag from bag_posts_history.json… (+9 more)

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

### Community 13 - "get_engine"
Cohesion: 0.29
Nodes (7): Engine, _env(), get_engine(), The process's reused connection (opened on first query). Every generator runs…, Build a SQLAlchemy URL from the environment, or None if unset. Accepts…, _shared_conn(), _url()

### Community 14 - "_enrich_deals"
Cohesion: 0.14
Nodes (12): dow_tier_weeks(), _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg(), _tier_window() (+4 more)

### Community 15 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.17
Nodes (12): Did last week's calls work? (`push_rules.record_week`, `followup`), Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page (+4 more)

### Community 16 - "forward_projections.py"
Cohesion: 0.17
Nodes (12): calendar, count_complete_weeks_in_month(), fmt_opt_pct(), fmt_pct(), _orow(), _perfect_week_index(), forward_projections.py…, One table row, month-end projected. expected = what the targets expect from… (+4 more)

### Community 17 - "le"
Cohesion: 0.09
Nodes (3): Ht, le, Ut

### Community 19 - "push_rules.py"
Cohesion: 0.13
Nodes (17): action(), _cover_txt(), _kind(), _n(), not_moving(), posting_median(), rank(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).… (+9 more)

### Community 20 - "sticky_controls.js"
Cohesion: 0.20
Nodes (15): bind(), embedHost(), headerOf(), init(), initSections(), injectCss(), place(), setPinned() (+7 more)

### Community 21 - "shop_requests.py"
Cohesion: 0.14
Nodes (21): _onoff(), Shop requests vs received (this month · last month) and the production approved…, requests_block(), _d(), _f(), _match(), _offer_label(), _offers() (+13 more)

### Community 22 - "main.py"
Cohesion: 0.07
Nodes (33): http_server, generator(), ensure_firewall_rule(), free_port(), get_lan_ip(), _is_quota_error(), _is_transient(), _offer_active_today() (+25 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.17
Nodes (16): Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), Net returns rule (qty <> 0, subtract refunds), Normalisation rules (upper-case, strip ref prefix, exclude combos/non-sellable stock), Bags not on offer per market (Kenya/Sinza/Uganda), Deal enrichment & name matching (_enrich_deals / _match), Self-made combos vs running combos (doc) (+8 more)

### Community 26 - "anime.umd.min.js"
Cohesion: 0.15
Nodes (8): ce(), de(), Me, Oe(), rs, St(), ts(), Ye

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.13
Nodes (17): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, google_auth.py (Sheets auth), Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics (+9 more)

### Community 28 - "odoo_marketing.py"
Cohesion: 0.06
Nodes (47): build(), _posts(), MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), _new_products(), This month's new products: data/new_products.txt (lib/new_products_list) — the…, _odoo_post_check() (+39 more)

### Community 29 - "si"
Cohesion: 0.24
Nodes (3): ii(), ri, si

### Community 30 - "Bags on offer vs not on offer"
Cohesion: 0.13
Nodes (13): Bags on offer vs not on offer, Corporate-lead till orders, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Period selector (Monthly / Weekly / Last week / Custom), Shop birthdays, Shop metrics (vs the Odoo revenue target), Sinza & Uganda (Oct 2026) — replaced 9 Oct 2026 (+5 more)

### Community 31 - "self_made_combos.py"
Cohesion: 0.12
Nodes (20): Regenerate, Per-shop combo-button chips (red when < half best-in-region), Shop -> Region table, _bag_sales_daily_sql(), _bag_sales_sql(), _bags_not_on_offer(), _build_sheet_slots(), fetch() (+12 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.06
Nodes (34): cache_data, cache_resource, SCRIPT_TIMEOUT = 600s config, fragment, html, streamlit, _bg_done_msg(), _bg_jobs() (+26 more)

### Community 33 - "stock.py"
Cohesion: 0.13
Nodes (22): build(), _cfg(), _colour(), _folder(), canon(), _moves(), Odoo product name → the dashboard's bag name (Offer Picking's _build_catalog…, odoo_stock_levels() (+14 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.08
Nodes (29): _bag_stock(), _cause(), _combo_bags(), esc(), fmt(), _garr_line(), gnum(), _growth_tracking() (+21 more)

### Community 35 - "current_performance.py"
Cohesion: 0.05
Nodes (49): corporate_clients_from_db(), corporate_from_db(), corporate_target_from_db(), _db_count(), monthly_from_db(), _months(), current_performance.py…, Reporting month's subset count (e.g. rejectBags, giftBags) from… (+41 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.13
Nodes (28): daily_bags(), inject(), inject_train(), main(), forecast(), chronos_preview.py…, Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run. (+20 more)

### Community 37 - "_read_deals"
Cohesion: 0.18
Nodes (11): _as_day(), _local_deal_rows(), _in_month(), 2026-10-25' / date / None → date or None., Sheet-shaped rows ([header] + [Tier, Month, Product, Location, Type, Original,…, Power Deals & Deal of the Week for the given month (Kenya sheet). Columns: A…, _read_deals(), Deals from posters (RALPH_DEALS.md) — 2026-10-04 (+3 more)

### Community 38 - "build_payload"
Cohesion: 0.14
Nodes (16): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+8 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.20
Nodes (10): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.html page (+2 more)

### Community 40 - "build"
Cohesion: 0.24
Nodes (11): _alt_cost(), _apply_alias(), build(), _combo_cost(), _combo_slots(), Parse `const SMC = {…}` out of self_made_combos.html (no DB round-trip)., One combo alternative (e.g. 'Amaya Handbag') → its BOM production cost., Combo name → list of slots, each a list of alternative strings. (+3 more)

### Community 41 - "marketing_posts.py"
Cohesion: 0.06
Nodes (54): build(), _add(), launch_curve(), _cfg(), _day_expr(), first_sale(), kenya_posts(), load_categories() (+46 more)

### Community 42 - "moves"
Cohesion: 0.20
Nodes (10): Actions (one per bag × market, then ranked), moves(), Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there…, More weight as the month runs out and when the market is behind its pace (gap…, Value at stake (units × price) × urgency × confidence. Price missing → KES…, score(), urgency(), test_moves_from_dead_shop_to_selling_low_shop() (+2 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "_build_period"
Cohesion: 0.18
Nodes (6): _build_period(), _offer_types(), _pick_target(), Latest target row for `shop` with this period that overlaps [start, end]. A…, Matrix payload: rows, per-row category / tier cells, and the period's Top-5…, _region_of()

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

### Community 51 - "type_fn"
Cohesion: 0.20
Nodes (14): build(), {TYPE: {"kes", "shops": {SHOP: {"n", "kes"}}}} for the runway types over…, ({TYPE: Kenya shop on-hand}, {TYPE: Sinza + Uganda on-hand}) — live Odoo., The NP.runway payload: {days, bags: [{name, created, category, stockKe,…, Product name → bag type (see the module docstring)., [{name, created, category}] newest first — the runway bag types as of today; []…, {TYPE: bags sold} for the given runway types over [start, end] — POS bags,…, runway_bags() (+6 more)

### Community 52 - "compute_period"
Cohesion: 0.12
Nodes (11): apply_odoo(), compute_period(), compute_regions(), fmt_pct(), _metric(), pct(), Total per location across all bag rows (Kenya shops by default)., Build every per-shop metric + the summary rows for one period. (+3 more)

### Community 53 - "_combo_button_usage"
Cohesion: 0.22
Nodes (8): _combo_button_usage(), _combo_norm_option(), combos_by_shop(), _norm(), _tokmatch(), Per running combo: units rung through the combo button (Odoo) vs the sheet's…, Per-shop view for Shops Efficiency, keyed by shop-location label (e.g.…, One combo slot-option → its distinctive bag token(s), colours/category words…

### Community 54 - "algorithmic-art skill"
Cohesion: 0.47
Nodes (6): Algorithmic Philosophy (Step 1 - named computational aesthetic movement), Flow Field Particle pattern (Organic Turbulence), p5.js library, Seeded Randomness pattern (randomSeed/noiseSeed for reproducibility), algorithmic-art skill, Voronoi/Crystallization relaxation pattern

### Community 55 - "dataviz-charts skill"
Cohesion: 0.29
Nodes (7): Chart.js 4.4.0 (CDN), Chart Recipes (bar, line/area, donut, sparkline, grouped bar), dataviz-charts skill, THEME JS design-system color object, For Dark Dashboards guidance (surface palette, contrast rules), theme-factory skill, 10 Pre-set Themes (Ocean Depths, Sunset Boulevard, etc.)

### Community 56 - "scripts/test_receipt_combos.py"
Cohesion: 0.32
Nodes (15): classify(), lines: [{receipt, d, product, qty, amount}] → per-market summary: {running:…, infer(), L(), Tests for receipt_combos.py + name_match.py — python -m pytest scripts -q, test_alternatives_and_singles(), test_bulk_receipts_are_not_combos(), test_four_bags_at_two_prices_are_two_combos() (+7 more)

### Community 57 - "run.py"
Cohesion: 0.36
Nodes (9): action_js(), edge_dump(), embedded(), inline_local(), js_str(), main(), Sticky-controls checks (docs/sticky-controls.md › Checks). python…, JS act(d, cb): optionally set a <select> (setv = "SEL=VALUE", fires change),… (+1 more)

### Community 58 - "run_query"
Cohesion: 0.07
Nodes (34): last_week_from_db(), Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, _bag_revenue(), _bag_revenue_range(), _corporate_lines(), _range_totals(), The month's revenue target (KES): Odoo sales_pos_target amount (pos +…, {bags, kes, corpBags, corpKes} for s..e — POS bags (bags_sold_total), POS bag… (+26 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "safe_int"
Cohesion: 0.16
Nodes (22): _bag_level_bags(), _build_no_convert(), _fetch_monthly_kenya(), _fetch_sinza_weekly(), _fetch_uganda_weekly(), _fetch_weekly_kenya(), _fetch_weekly_region(), fmt_int() (+14 more)

### Community 62 - "fetch_new_products_data"
Cohesion: 0.20
Nodes (14): fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_sales_window() (+6 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "write_bags_offer_source"
Cohesion: 0.29
Nodes (7): Counted by how it was sold, _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…, Kenya on-offer bag set (tagged by offer) + the not-on-offer list, for…, write_bags_offer_source()

### Community 65 - "Monthly Report (doc)"
Cohesion: 0.22
Nodes (9): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+1 more)

### Community 66 - "_read_offers"
Cohesion: 0.25
Nodes (8): Offer type summary (matrix), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, _read_offers(), _read_offers_cache(), _category_of(), _norm_cat(), Category for a bag: the offers-sheet category (col C), else a keyword fallback.

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.11
Nodes (18): Bag health (by bag, 18 Oct 2026), Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026), Page, Product rating and core 5 vs other 13 categories (18 Oct 2026) (+10 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

### Community 71 - "_resolve_bag"
Cohesion: 0.25
Nodes (8): _monthly_bag_sales(), Resolve any bag wording → (canonical BOM bag type, cost or None, in_bom).…, {"months": ["Jun", …], "keys": ["2026-06", …], "bags": [{bag, category, stock,…, {BAG: {"days": [{d, name, was, now, units, today}], "offerDays", "offerUnits",…, _resolve_bag(), price_of(), _timed_offer_history(), canon()

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "fetch_posting_data"
Cohesion: 0.09
Nodes (19): _bt_on_offer(), count_complete_weeks_in_month(), _dead_clear(), fetch_posting_data(), _clear(), _yield(), _fold_bag_level(), load_dead_thresholds() (+11 more)

### Community 74 - "build"
Cohesion: 0.08
Nodes (33): actions(), build(), agg(), week_tot(), num(), pearson(), footfall_marketing.py — Footfall and Marketing page (spec: docs/footfall-…, What we can do' — by rule (docs/footfall-marketing.md › Actions). Each names a… (+25 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "kpi_anim.js"
Cohesion: 0.60
Nodes (5): count(), fmt(), key(), parse(), scan()

### Community 77 - "_apply_receipt_offers"
Cohesion: 0.25
Nodes (6): _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region…, _region_goal(), _till_targets()

### Community 78 - "shops_dispatch.py"
Cohesion: 0.21
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

### Community 82 - "family"
Cohesion: 0.67
Nodes (4): family(), _load(), _norm(), Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…

### Community 83 - "facts"
Cohesion: 0.15
Nodes (17): add_peers(), _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day(), ISO date n days before END (0 = END)., _row() (+9 more)

### Community 84 - "build_offer"
Cohesion: 0.17
Nodes (7): build_offer(), offer_kenya_posts(), post_window(), Compute the full TO payload for a single offer dict. Rebinds the per-offer…, (first, last) date of an offer's posting window: POST_LEAD_DAYS before…, {BAG_UPPER: kenya_posts} over the offer's posting window, from marketing's…, _shop_sql()

### Community 85 - "sys"
Cohesion: 0.09
Nodes (26): dotenv, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers… (+18 more)

### Community 86 - "offer_picking.py"
Cohesion: 0.18
Nodes (14): _build_catalog(), _is_full_price(), _next_month(), offer_picking.py…, Letters and digits only, so 'CODE3' meets 'CODE 3' and 'FANNYPACK(N)' meets…, {_staff_key(catalogue bag type): staff price} from staff_prices.json (a 0 = no…, {BAG (upper): official full price} from bag_original_prices.json (fallback)., Save a local, human-editable copy of the offers prices to OFFERS_CACHE. (+6 more)

### Community 87 - "test_push_planner.py"
Cohesion: 0.16
Nodes (25): context(), What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons(), codes(), F(), Tests for lib/push_rules.py (the Push Planner's pure logic). Run: python -m…, A facts row with sensible defaults, overridden by kw. (+17 more)

### Community 88 - "write_atomic"
Cohesion: 0.29
Nodes (7): inject(), _inject(), inject(), inject(), inject(), Write text to path so a reader never sees a half-written file: write a temp…, write_atomic()

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "Out-of-stock demand — people, not requests"
Cohesion: 0.14
Nodes (10): Agent skills — retail analytics, Test a skill, Use in another project, Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods (+2 more)

### Community 91 - "followup"
Cohesion: 0.29
Nodes (7): followup(), Sunday on/before `d` — the dashboard's Sun–Sat weeks., The most recent PREVIOUS week's calls and what happened since: sold/day since…, week_start(), test_followup_compares_since_week_start(), test_followup_ignores_the_current_week(), test_week_start_is_sunday()

### Community 92 - "monthly_target_rows"
Cohesion: 0.14
Nodes (14): fetch_monthly_target(), fetch_sheet_data(), load(), get_rows(), The tab's rows in the sheet's layout, built from Odoo. No sheet fallback (Oct…, monthly_target_rows(), monthly_target_sheet_rows(), MONTHLY_TARGET rows with column C = the bag's target from Odoo (docs/product-… (+6 more)

### Community 93 - "norm"
Cohesion: 0.16
Nodes (14): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, ({PRODUCT: {SHOP CODE: units}}, {PRODUCT: {SHOP CODE: [[colour, units], …]}})…, shop_sales(), _aliases(), _Deriver, norm(), odoo_name() (+6 more)

### Community 94 - "Dashboard Architecture (static HTML + Python generator + injected data block)"
Cohesion: 0.40
Nodes (5): DATA_START/DATA_END comment marker injection pattern, build_all.py (rebakes every page), Dashboard Architecture (static HTML + Python generator + injected data block), .github/workflows/refresh.yml CI workflow, shell.html (sidebar nav frame, loads each page into an iframe)

### Community 95 - "negative_fixes.py"
Cohesion: 0.06
Nodes (46): argparse, fnmatch, _negfix(), Stock record accuracy per shop for every period (docs/shops-efficiency.md ›…, bags_sold(), block(), by_shop(), _date() (+38 more)

### Community 96 - "custom_range.py"
Cohesion: 0.19
Nodes (14): block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each…, (from, to) dates for the page's Custom period, or None. Swapped if reversed;… (+6 more)

### Community 97 - "oos_callbacks.py"
Cohesion: 0.05
Nodes (61): Out of stock — call back, fixture, match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, bag(), lib — shared data-access for the marketing dashboard (Postgres migration).…, col(), aggregate() (+53 more)

### Community 98 - "master_products"
Cohesion: 0.50
Nodes (4): master_products(), _norm_name(), Match the SQL normalisation: lower-case, '.'→space, collapse whitespace., Normalised, de-duplicated master catalogue names (master_products.txt), for the…

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "beats.py"
Cohesion: 0.09
Nodes (26): The total, Per bag × market: the facts (`push_rules.facts`, `add_peers`), Config, Launch day, Marketing posts, Prices (30 Oct 2026, user's call), Race lines, sales by day, product performance, folding (9 Nov 2026, user's call), Sales (+18 more)

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
Cohesion: 0.18
Nodes (16): _age_min(), _cleanup(), fresh_meta(), _meta(), _p(), query(), lib/snapshot.py — local DuckDB snapshot of the tills (docs/README.md › DuckDB…, The snapshot to read, refreshing it first when it's too old; None if there's… (+8 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "why_moved.py"
Cohesion: 0.09
Nodes (36): why_moved(), _load_shop_regions(), Shop → Region from docs/shop-regions.md (lib/shop_regions); the built-in…, doc(), day_for(), load(), lib/sales_date_fix.py — sales keyed in late, moved back to the day they…, [{"till", "shop", "from", "to", "asDate"}] — datetimes / dates parsed; [] if… (+28 more)

### Community 107 - "_bucket"
Cohesion: 0.19
Nodes (13): _bucket(), kenya_stock_by_bag(), _parse_colour(), Which configured bag (if any) an Odoo/​sheet product name belongs to, by…, {BAG_UPPER: category} — the bag's category label only, from the product…, First primary colour token found in a name (longest-first), Title-cased; '' if…, Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share…, Per-[REJECT]-product variant rows for a name-filtered offer, for the filterable… (+5 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "check_connection"
Cohesion: 0.09
Nodes (29): DataFrame, _corporate_bags(), (corporate bags, corporate KES received) in the given month, live from Odoo…, load_data(), _prices(), POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')., Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if…, _till_to_shop() (+21 more)

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "push_planner.py"
Cohesion: 0.12
Nodes (23): add_laya(), build_actions(), build_facts(), build_reasons(), _categories(), inject(), _kenya_target(), main() (+15 more)

### Community 112 - "OOS call-back progress (Ralph loop log)"
Cohesion: 0.29
Nodes (6): Blocker counter, Final summary, Log, OOS call-back progress (Ralph loop log), Sheets cut to three tabs (RALPH_SHEETS.md) — 2026-10-04, Sinza & Uganda (RALPH_OUTSIDE.md) — 2026-10-04

### Community 114 - "realistic_rates"
Cohesion: 0.53
Nodes (6): _clamp(), ({SHOP: {BAG: units a week}}, {SHOP: {"recent", "season", "growth"}}) — recent…, realistic_rates(), growth(), season(), tot()

### Community 119 - "Sales-share targets per product"
Cohesion: 0.40
Nodes (4): Deliver, Sales-share targets per product, Steps, Tests

### Community 121 - "bag_classifier"
Cohesion: 0.17
Nodes (15): Buckets, _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _load_bag_prices() (+7 more)

### Community 122 - "fetch"
Cohesion: 0.12
Nodes (26): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), combo_slots(), make_classifier() (+18 more)

### Community 123 - "What the page shows"
Cohesion: 0.20
Nodes (10): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 2b. Shop breakdown (22 Oct 2026, user's call), 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Data, Popover waterfall — why the units moved (26 Oct 2026, user's call) (+2 more)

### Community 126 - "Product (bag) targets"
Cohesion: 0.29
Nodes (7): A month with only a revenue target (November 2026), Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, Used as the monthly bag target (from October 2026)

### Community 128 - "test_share_targets.py"
Cohesion: 0.22
Nodes (11): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+3 more)

### Community 138 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.22
Nodes (7): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does, Current Performance (doc)

### Community 153 - "New Products Analytics (doc)"
Cohesion: 0.25
Nodes (7): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), match_odoo_bags prefix matcher ([S_0] fix), Python dependencies list (requirements.txt), Postgres source-of-truth migration (off Google Sheets, weekly first)

### Community 154 - "_matches_sheet"
Cohesion: 0.18
Nodes (10): Three countries, one page (9 Oct 2026), _matches_sheet(), _opt_close(), Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Same slot count and every slot overlaps under SOME pairing (any order: the…, The sheet label this Odoo combo maps to, or None if it isn't on the sheet.…, _slots_fit(), Inputs (from the user, Oct 2026) (+2 more)

### Community 155 - "Offer Picking (doc)"
Cohesion: 0.25
Nodes (9): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES) (+1 more)

### Community 156 - "start_server"
Cohesion: 0.26
Nodes (11): start_server(), copyfile(), do_GET(), end_headers(), finish(), handle_one_request(), _handle_refresh(), _run_ref() (+3 more)

### Community 157 - "build"
Cohesion: 0.15
Nodes (12): {BAG TYPE (upper): production cost} from bom_costs.json — the local copy of the…, _read_bom_costs(), _assign_price(), _bom_costs(), build(), reject_stock.csv → {BAG (upper): {units, colours:{COLOUR: units}}}., (price, flag) from BOM cost — two tiers. flag ∈ {'', 'thin', 'below', 'nobom'}., Write an Excel (xlsx, or CSV fallback) of EVERYTHING on the pricing board —… (+4 more)

### Community 158 - "timed_offers.py (generator)"
Cohesion: 0.09
Nodes (22): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+14 more)

### Community 159 - "scripts/receipt_combos.py"
Cohesion: 0.29
Nodes (6): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…, itertools

### Community 160 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 161 - "new_products.py"
Cohesion: 0.13
Nodes (13): _base_colour(), _merge_rows_by_base_colour(), odoo_combo_product_bags(), odoo_lifetime_product_bags(), odoo_month_product_bags(), new_products.py…, All-time bags per product from Odoo (no month window) — the lifetime sales of…, Upper-case, punctuation-normalised string with known qualifier tokens… (+5 more)

### Community 162 - "timed_offers.py"
Cohesion: 0.13
Nodes (19): _acc(), _bags_from_file(), build_compare(), _cmp_lines(), _days(), _derive_month(), _kenya_net_moves_since(), load_config() (+11 more)

### Community 167 - "Menu 1 Current Performance in the 3-beat layout (preview)"
Cohesion: 0.15
Nodes (12): 0. New: an executive summary strip at the top of the page, 1. Sales, Weekly Sales and Remaining Target cards, 2. Followers & Reach, 3. Weekly Performance — Week 1 to Latest, 4. Why Did We Move?, 5. Sales vs Monthly Target, Week-over-Week, Bare Minimum, 6. Forward Projections (Standard and Forecasted), 7. Price per Bag, and On offer vs not on offer (+4 more)

### Community 168 - "odoo_marketing_audit.py"
Cohesion: 0.39
Nodes (8): root(), audit(), _expected(), main(), _period(), _range(), scripts/odoo_marketing_audit.py — how complete and up to date each marketing…, _step()

### Community 169 - "Footfall and Marketing (21 Oct 2026, user's call)"
Cohesion: 0.20
Nodes (9): Actions (rules), Correlations ("Posts and ads vs visitors"), Data traps (said on the page), Definitions, Footfall and Marketing (21 Oct 2026, user's call), Regenerate, Shop mapping (`lib/footfall.SHOPS`), Sources (+1 more)

### Community 172 - "odoo_tabs.py"
Cohesion: 0.13
Nodes (22): _build(), build_rows(), catalog_rows(), default_window(), _flag_cells(), _fmt(), last_complete_week(), load_catalog() (+14 more)

### Community 174 - "Product Performance — Shop breakdown: progress"
Cohesion: 0.22
Nodes (8): 1. Spec — DONE, 2. Data — DONE, 3. Page section — DONE, 4. Sidebar and sticky bar — DONE, 5. Visual check — DONE, 6. Wrap-up — DONE, Product Performance — Shop breakdown: progress, Summary

### Community 175 - "_seasonality"
Cohesion: 0.29
Nodes (8): Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), _combo_odoo_slots(), _combo_sheet_slots(), Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]., Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same…

### Community 178 - "os"
Cohesion: 0.08
Nodes (38): One-off: restore August's Offer Type figures into monthly_report_history.json…, collections, csv, datetime, functools, bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, generators/bag_tracking.py — Bag Tracking: the chosen bags' Kenya shop stock at…, monthly_sales.py — the current month's real bags sold, from Postgres. The… (+30 more)

### Community 179 - "Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)"
Cohesion: 0.20
Nodes (9): 1. Spec — DONE, 2. SQL + library — DONE, 3. Generator — DONE, 4. Page — DONE, 5. Actions — DONE, 6. Visual check — DONE, 7. Wrap-up — DONE, Findings (16 weeks, 28 Jun – 17 Oct 2026; last fully counted week 11–17 Oct) (+1 more)

### Community 182 - "bags_on_offer.py"
Cohesion: 0.10
Nodes (21): _base_windows(), _custom_range(), fmt(), inject(), main(), bags_on_offer.py…, (from, to) dates from boo_custom_range.json — the Custom period — or None., Write (or with a=None, delete) the Custom period's dates. (+13 more)

### Community 183 - "_fetch_sinza_monthly"
Cohesion: 0.18
Nodes (14): _analyze_region(), _fetch_sinza_monthly(), _fetch_uganda_monthly(), _mmp_key(), _ms_key(), MONTHLY_SALES: colour=A(0), product_name=B(1), MONTHLY_MARKETING_POST: colour=A(0), product_name=C(2), STOCK_LEVELS: colour=A(0), product_name=C(2) (+6 more)

### Community 187 - "Ralph loop brief — Footfall and Marketing page"
Cohesion: 0.25
Nodes (7): DATA FACTS (verified 21 Oct 2026), DONE, ESCAPE HATCH, PROJECT RULES (must hold every iteration), Ralph loop brief — Footfall and Marketing page, SELF-CORRECTION, SUB-GOALS (do in order; tick each in notes/footfall_progress.md with the command output that proved it)

### Community 189 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

### Community 191 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 194 - "Bag Tracking"
Cohesion: 0.33
Nodes (5): Bag Tracking, Page, Prices, Stock, The bags

### Community 200 - "shop_stock_levels.py"
Cohesion: 0.09
Nodes (38): bag_categories(), buffer_stock(), build(), dispatch_shop(), fit(), grand_total(), leads(), month_end_lift() (+30 more)

### Community 204 - "Combos from receipts — running vs self-made"
Cohesion: 0.40
Nodes (5): Combos from receipts — running vs self-made, Inputs, Outputs to show, Receipt rule (per receipt), Tests

### Community 205 - "render"
Cohesion: 0.60
Nodes (5): growthData(), render(), drawGrowth(), table(), wf()

### Community 211 - "update_np_weekly_history"
Cohesion: 0.29
Nodes (7): _np_complete_weeks_in_month(), _np_perfect_week_index(), _np_week_start(), Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)., Ordinal among the month's perfect weeks (>=5 days in month), so the first FULL…, Snapshot each Sun–Sat week (sales, Kenya/Outside posts) into…, update_np_weekly_history()

### Community 213 - "build"
Cohesion: 0.13
Nodes (19): allocate(), available_days(), base_period(), build(), (total units, info) — the month's Odoo target units, or (no Odoo targets yet)…, The three complete months before month_start → (start, end)., Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},… (+11 more)

### Community 216 - "_alignment_region"
Cohesion: 0.43
Nodes (7): _alignment_region(), _for(), _sold(), _stk(), _units(), _align(), Marketing–Sales alignment (posted × sold) over ALL bags, one region/period.…

### Community 217 - "posting_yields.py"
Cohesion: 0.27
Nodes (8): _mkt_perfect_week_index(), _mkt_week_label(), posting_yields.py…, Ordinal of d's Sun–Sat week within the month, counting every week that has at…, vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]., current = {region: {key: {productName,colour,category,bagType,stock}}}. A new…, update_clearance(), update_mkt_history()

### Community 221 - "base_name"
Cohesion: 0.33
Nodes (7): base_name(), dispatch_by_product_shop(), _num(), The catalogue key for an Odoo product name: norm() without the "[REJECT]" tag…, {NORM(product): {SHOP: bags}} of POS bag sales in [start, end]; None if DB…, {NORM(product): {SHOP: bags distributed in}} from combined_distribution.sql's…, sales_by_product_shop()

### Community 223 - "data"
Cohesion: 0.14
Nodes (15): Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary(), week_start_of(), weekly_from_db(), _live_bags(), _load_combos_by_shop() (+7 more)

### Community 227 - "product_performance.py"
Cohesion: 0.06
Nodes (47): Bulk orders, build(), corp(), categories(), corporate_period(), _d(), explain(), _fmt_d() (+39 more)

## Knowledge Gaps
- **253 isolated node(s):** `Log`, `Preventing it`, `Steps`, `The rule`, `Added mid-task (user)` (+248 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1109 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Shops & Regions (doc — source of truth)` connect `Bags on offer vs not on offer` to `Denri Africa Dashboard Design System (skill)`, `Chart type switcher (every chart, every menu)`, `self_made_combos.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `match_offer()` connect `name_match.py` to `Combos from receipts — running vs self-made`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `Combos from receipts — running vs self-made` connect `Combos from receipts — running vs self-made` to `Out-of-stock demand — people, not requests`, `name_match.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **What connects `Log`, `Preventing it`, `Steps` to the rest of the system?**
  _253 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `month_extras.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0707070707070707 - nodes in this community are weakly interconnected._
- **Should `_ask` be split into smaller, more focused modules?**
  _Cohesion score 0.08374384236453201 - nodes in this community are weakly interconnected._
- **Should `lib/receipt_combos.py` be split into smaller, more focused modules?**
  _Cohesion score 0.060641627543035995 - nodes in this community are weakly interconnected._