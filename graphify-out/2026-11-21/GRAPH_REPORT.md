# Graph Report - Marketing_dashboard  (2026-11-21)

## Corpus Check
- 241 files · ~1,222,473 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 21 file(s) not represented in the graph (top: .csv 14, (none) 2, .toml 1)

## Summary
- 2820 nodes · 5649 edges · 199 communities (157 shown, 42 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 188 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `55a05d48`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- shop_corporate.py
- add_laya
- tests/test_receipt_combos.py
- oos_chip.js
- chart_switcher.js
- he
- Kitengela Rejects tracker (timed offer)
- signals
- design-taste-frontend (anti-slop frontend skill)
- v5_theme.js
- name_match.py
- bare_minimum setting (weekly target floor)
- get_gspread_client
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
- signals
- si
- Bags on offer vs not on offer
- self_made_combos.py
- streamlit_app.py
- odoo_stock_by_product
- monthly_report.py
- live_anchor
- chronos_train.py
- os
- build_payload
- Shops Efficiency Tracking spec doc
- month_extras.py
- build
- build_actions
- page_sidebar.js
- _build_period
- Combos & Power Deals by Shop panel (#combo-shop)
- test_fixC_sql.py
- lib/db.py (Supabase session pooler DB access)
- CLAUDE.md
- history.py (read months back)
- je
- bag_key_fn
- compute_period
- _combo_button_usage
- algorithmic-art skill
- dataviz-charts skill
- scripts/test_receipt_combos.py
- Shop Launch
- run_query
- High-End Visual Design skill
- safe_int
- ns
- fetch_new_products_data
- daydream skill (Vault Daydream)
- write_bags_offer_source
- db.py
- load_rows
- Shop Stock Levels — min / max per shop, stocks report and next-month preparedness
- TTL disk-cache rationale (.odoo_cache/)
- welcome_screen.js
- Month-End Routine
- live_month_window
- marketing_dashboard.sql
- fetch_posting_data
- build
- shop_birthdays.py
- kpi_anim.js
- Denri Africa Dashboard Design System (skill)
- shops_dispatch.py
- why_moved.js
- theme.py
- push_laya.py
- family
- test_push_planner.py
- build_offer
- history.py
- offer_picking.py
- F
- test_fixB_offer_units.py
- test_stockout_demand.py
- README.md
- shop-birthdays.md
- monthly_target_rows
- _odoo_colour
- Dashboard Architecture (static HTML + Python generator + injected data block)
- negative_fixes.py
- custom_range.py
- test_oos_callbacks.py
- master_products
- Bag Signals — quant view of each bag (posting · stock · selling)
- beats.py
- current_performance.html
- attach
- Fix merge conflicts (two-machine workflow)
- snapshot.py
- Pricing rule — two tiers (BAND cost cutoff) + hand pins
- build
- reject_variants
- Ralph task — only three sheet tabs left
- check_connection
- Bag targets October 2026_3acbad00.md
- main
- Semantic color rules (green=good, amber=risk, red=critical, cyan=info)
- perf_data.js
- Out-of-stock demand — people, not requests
- reject_sales_export_302c9b30.md
- PROFILE_README.md
- previous_snapshot.json
- reject_from_db() function
- bag_classifier
- fetch
- What the page shows
- Product (bag) targets
- test_share_targets.py
- contextlib
- Chart type switcher (every chart, every menu)
- denri_mkt_timed_offer* Supabase tables
- _bag_stock
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
- num
- Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)
- odoo_month_product_bags
- Menu 1 Current Performance in the 3-beat layout (preview)
- odoo_marketing_audit.py
- Footfall and Marketing (21 Oct 2026, user's call)
- Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)
- get_rows
- load_pages
- Product Performance — Shop breakdown: progress
- _seasonality
- norm
- lib
- Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)
- shops_efficiency.py
- bags_on_offer.py
- _is_checked
- test_sheet_reads.py
- Ralph loop brief — Footfall and Marketing page
- attach_stock
- _bag_tiers
- Bag signals — quant finance applied to product sales
- ambiguous_python_import_17686b6faac5
- Bag Tracking
- build
- Ralph task — "Out of stock — call back" demand per shop
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
- load_catalog

## God Nodes (most connected - your core abstractions)
1. `run_query()` - 81 edges
2. `fetch()` - 41 edges
3. `fetch_posting_data()` - 39 edges
4. `data()` - 39 edges
5. `check_connection()` - 32 edges
6. `le` - 31 edges
7. `build_payload()` - 30 edges
8. `get_gspread_client()` - 27 edges
9. `ls` - 26 edges
10. `build_offer()` - 24 edges

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
- **Multiple menus share product-matching.md as the canonical name-matching reference** — docs_product_matching_doc, docs_self_made_combos_doc, docs_new_products_doc, docs_offer_picking_doc [EXTRACTED 0.95]

## Communities (199 total, 42 thin omitted)

### Community 0 - "shop_corporate.py"
Cohesion: 0.15
Nodes (25): Corporate orders the shops handle (Odoo Sales quotes paid at the tills) for the…, shop_corporate_from_db(), _acronym(), build(), _maybe(), owns(), corporate_team_receipts(), _d() (+17 more)

### Community 1 - "add_laya"
Cohesion: 0.07
Nodes (25): add_laya(), Laya's second opinion (lib/push_laya) when the model is on this PC; else a…, Answer, _ask(), ask_choice(), ask_yes_no(), available(), _bucket() (+17 more)

### Community 2 - "tests/test_receipt_combos.py"
Cohesion: 0.05
Nodes (64): What the page shows (per period), _market_records(), Tanzania (Sinza) & Uganda till receipts → sales in KES for the all-country rows…, _fill_units(), _apply_receipt_offers(), Kenya's combosGoal for a Sinza / Uganda market, from receipts: last month's…, {prev, cur}: the till's Odoo monthly target (KES + bags) vs what it sold (bags;…, Sinza & Uganda: when offers_monthly.csv lists the month's offers, the region… (+56 more)

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

### Community 8 - "design-taste-frontend (anti-slop frontend skill)"
Cohesion: 0.18
Nodes (12): design-taste-frontend (related skill), design-taste-frontend (anti-slop frontend skill), Brief-First Process (8-step design workflow), Hard Bans (typography, color, layout, code, content clichés), Pre-Flight Checklist (90+ items), Redesign Protocol (upgrading existing UI), Three Dials — DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, Three AI-generated design clusters (calibration reference) (+4 more)

### Community 9 - "v5_theme.js"
Cohesion: 0.19
Nodes (25): apply(), contrastOnCanvas(), cutColor(), ensureLink(), fixChipText(), hsl(), hslToRgb(), luminance() (+17 more)

### Community 10 - "name_match.py"
Cohesion: 0.16
Nodes (16): combo_list_slots(), _combo_norm_option(), combo_till_slots(), match_offer(), opt_close(), name_match.py — match a till's combo product name to a combo on the offer list…, One combo slot-option → its distinctive bag token(s), colours/category words…, Offer-list label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]. (+8 more)

### Community 12 - "get_gspread_client"
Cohesion: 0.08
Nodes (27): kenya_posts(), load_workplan(), _parse_workplan(), (opening stock, source) — the live sheet, else the saved CSV., ({BAG: posts this month}, {BAG: posts last week}) from col D / col E (Kenya),…, [[bag, colour, qty], …] → {BAG: {COLOUR: qty}} (TOTAL and blank rows skipped,…, get_gspread_client(), Shared Google Sheets authentication for every dashboard generator. Two modes,… (+19 more)

### Community 13 - "get_engine"
Cohesion: 0.29
Nodes (7): Engine, _env(), get_engine(), The process's reused connection (opened on first query). Every generator runs…, Build a SQLAlchemy URL from the environment, or None if unset. Accepts…, _shared_conn(), _url()

### Community 14 - "_enrich_deals"
Cohesion: 0.06
Nodes (29): _as_day(), dow_tier_weeks(), _enrich_deals(), _match(), _full(), _full_of(), _tdigit(), _tier_agg() (+21 more)

### Community 15 - "Push Planner (`push_planner.py` → `push_planner.html`, `PP`)"
Cohesion: 0.25
Nodes (8): Inputs (read only — nothing is written to Odoo or the sheet), Laya model (`lib/laya.py`), Laya's second opinion (`lib/push_laya.py`), Push Planner (`push_planner.py` → `push_planner.html`, `PP`), Regenerate, Shop birthdays, The page, Why it isn't moving — reasons, per market (`push_rules.reasons`)

### Community 16 - "forward_projections.py"
Cohesion: 0.11
Nodes (18): inject(), fmt_opt_pct(), fmt_pct(), _inject(), _orow(), _perfect_week_index(), forward_projections.py…, One table row, month-end projected. expected = what the targets expect from… (+10 more)

### Community 17 - "le"
Cohesion: 0.09
Nodes (3): Ht, le, Ut

### Community 19 - "push_rules.py"
Cohesion: 0.14
Nodes (16): action(), _cover_txt(), _kind(), _n(), lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).…, (code, plain sentence, units at stake, confidence 0..1) for one bag × market.…, HANDBAG' → 'handbags', 'SCHOOL BAG' → 'school bags', 'SPORT' → 'sport bags', ''…, _times() (+8 more)

### Community 20 - "sticky_controls.js"
Cohesion: 0.20
Nodes (15): bind(), embedHost(), headerOf(), init(), initSections(), injectCss(), place(), setPinned() (+7 more)

### Community 21 - "shop_requests.py"
Cohesion: 0.14
Nodes (21): _onoff(), Shop requests vs received (this month · last month) and the production approved…, requests_block(), _d(), _f(), _match(), _offer_label(), _offers() (+13 more)

### Community 22 - "main.py"
Cohesion: 0.08
Nodes (26): http_server, generator(), ensure_firewall_rule(), free_port(), get_lan_ip(), _offer_active_today(), True if ANY timed-offer window is set and today falls inside it. Handles the…, Once per calendar day, while an offer window is active, re-run timed_offers.py… (+18 more)

### Community 23 - "Self-made combos vs running combos (doc)"
Cohesion: 0.14
Nodes (18): Data Sources table (PERF/PROJ, NP, OA, PA), Dashboard Insights skill, Insight Categories & Thresholds (velocity_factor distortion, WoW decline), Monthly Report (doc), Finalized month pin (DENRI_REPORT_MONTH), Response-ladder tag (Update / New Timing / Acknowledge / Collaborate), Alignment universe (sold ∪ stock ∪ posted, region-present bags), Posting - Sales Yields from Accurate Posting (doc) (+10 more)

### Community 26 - "anime.umd.min.js"
Cohesion: 0.15
Nodes (8): ce(), de(), Me, Oe(), rs, St(), ts(), Ye

### Community 27 - "Dashboard Menu Docs (spec index)"
Cohesion: 0.13
Nodes (17): Menu 1: Current Performance, Menu 7: Dashboard Insights, Dashboard Menu Docs (spec index), domharness.js verification shim, google_auth.py (Sheets auth), Rule: correct the .md spec first, then make the code match it, Menu 8: Monthly Report, Menu 2: New Products Analytics (+9 more)

### Community 28 - "signals"
Cohesion: 0.07
Nodes (35): build(), _posts(), MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read., Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the…, _save_history(), action(), bag_posts(), tally() (+27 more)

### Community 29 - "si"
Cohesion: 0.24
Nodes (3): ii(), ri, si

### Community 30 - "Bags on offer vs not on offer"
Cohesion: 0.12
Nodes (16): Bags on offer vs not on offer, Buckets, Corporate-lead till orders, Laptop sleeves are bags (27 Sep 2026), Layout (laptop / tablet / phone), Regenerate, Shop birthdays, Shop metrics (vs the Odoo revenue target) (+8 more)

### Community 31 - "self_made_combos.py"
Cohesion: 0.16
Nodes (12): Per-shop combo-button chips (red when < half best-in-region), Shop -> Region table, _bag_sales_daily_sql(), _bag_sales_sql(), fmt(), inject(), main(), self_made_combos.py… (+4 more)

### Community 32 - "streamlit_app.py"
Cohesion: 0.06
Nodes (33): cache_data, cache_resource, SCRIPT_TIMEOUT = 600s config, fragment, html, streamlit, _bg_done_msg(), _bg_jobs() (+25 more)

### Community 33 - "odoo_stock_by_product"
Cohesion: 0.18
Nodes (14): odoo_stock_levels(), Live per-shop Odoo on-hand in the SAME shape parse_sheet(STOCK_LEVELS) returns:…, _codes_for(), _inlist(), odoo_stock_at_location(), odoo_stock_by_product(), odoo_stock_by_shop_code(), _ok() (+6 more)

### Community 34 - "monthly_report.py"
Cohesion: 0.15
Nodes (10): _cause(), esc(), fmt(), ladder_strip(), pct(), monthly_report.py…, read_block(), _read_timed_offers() (+2 more)

### Community 35 - "live_anchor"
Cohesion: 0.09
Nodes (30): corporate_clients_from_db(), corporate_target_from_db(), _db_count(), monthly_from_db(), _months(), Reporting month's subset count (e.g. rejectBags, giftBags) from…, A text cell from a query row: '' for NULL / NaN., 2026-09,2026-10' → [{"m": "Sep", "cur": False}, {"m": "Oct", "cur": True}],… (+22 more)

### Community 36 - "chronos_train.py"
Cohesion: 0.13
Nodes (24): inject(), inject_train(), main(), forecast(), Put `data` into the page as `const <name>` between the <marker>_START/END…, The latest chronos_train.py results, if it has been run., Daily walk-ins (denri_footfall_count) and new walk-in leads (denri_lead), as…, walkins_and_leads() (+16 more)

### Community 37 - "os"
Cohesion: 0.08
Nodes (26): One-off: restore August's Offer Type figures into monthly_report_history.json…, chronos_preview.py…, calendar, datetime, generators/bag_tracking.py — Bag Tracking: the chosen bags' Kenya shop stock at…, current_performance.py…, monthly_sales.py — the current month's real bags sold, from Postgres. The…, push_planner.py — Push Planner: what to push this week, where, and why bags… (+18 more)

### Community 38 - "build_payload"
Cohesion: 0.14
Nodes (16): _self_made_combos(), build_payload(), _anchor_sunday(), _combo_bags(), _fill_from_odoo(), _groups(), _match_bag(), _month_weekly() (+8 more)

### Community 39 - "Shops Efficiency Tracking spec doc"
Cohesion: 0.20
Nodes (10): Market Split convention (Kenya vs Sinza vs Uganda), Menu 6: Shops Efficiency Tracking, combos_by_shop.json 15-minute reuse cache, Shops Efficiency Tracking spec doc, KENYA_SHOPS list (16 Kenya shops), _load_combos_by_shop() function, shops_dispatch.py generator (Odoo dispatch/receiving/sold JSON), shops_efficiency.html page (+2 more)

### Community 40 - "month_extras.py"
Cohesion: 0.16
Nodes (22): _bags_on_offer(), _block(), build_extras(), cp_more_month(), _deals(), _month_dates(), _pick(), _posting() (+14 more)

### Community 41 - "build"
Cohesion: 0.15
Nodes (17): build(), _add(), launch_curve(), _cfg(), _day_expr(), first_sale(), load_categories(), load_prices() (+9 more)

### Community 42 - "build_actions"
Cohesion: 0.13
Nodes (17): Actions (one per bag × market, then ranked), build_actions(), Adds action / says / units / confidence / score to each facts row; returns…, moves(), posting_median(), rank(), {market: median postsMonth of the bags that were posted at all} — the 'below…, Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there… (+9 more)

### Community 43 - "page_sidebar.js"
Cohesion: 0.35
Nodes (12): behaviour(), embedHost(), esc(), init(), injectCss(), parentScroller(), pin(), refresh() (+4 more)

### Community 44 - "_build_period"
Cohesion: 0.17
Nodes (7): _build_period(), _offer_types(), _pick_target(), Latest target row for `shop` with this period that overlaps [start, end]. A…, Matrix payload: rows, per-row category / tier cells, and the period's Top-5…, _region_of(), _shop_label()

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

### Community 51 - "bag_key_fn"
Cohesion: 0.12
Nodes (23): _odoo_post_check(), get(), names(), Upper-cased bag types from new_products.txt in file order ([] = no new…, meta_posts_by_bag(), ({bag: {"posts", "reach", "views"}}, {"posts", "tagged"}) — Facebook +…, bag_key_fn(), key() (+15 more)

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

### Community 57 - "Shop Launch"
Cohesion: 0.20
Nodes (9): Config, Launch day, Marketing posts, Race lines, sales by day, product performance, folding (9 Nov 2026, user's call), Sales, Sales keyed in late (9 Nov 2026, user's call), Shop Launch, What the page shows (+1 more)

### Community 58 - "run_query"
Cohesion: 0.09
Nodes (27): daily_bags(), last_week_from_db(), Bags sold in the previous complete Sun–Sat week, straight from Postgres (same…, _bag_revenue(), _bag_revenue_range(), _corporate_lines(), _range_totals(), {bags, kes, corpBags, corpKes} for s..e — POS bags (bags_sold_total), POS bag… (+19 more)

### Community 59 - "High-End Visual Design skill"
Cohesion: 0.40
Nodes (5): Creative Variance Engine (vibe/layout archetypes), Double-Bezel Card Architecture, Glassmorphism recipe, Motion Requirements (custom cubic-bezier, GPU-safe transforms), High-End Visual Design skill

### Community 60 - "safe_int"
Cohesion: 0.15
Nodes (17): _bag_level_bags(), _build_no_convert(), _fetch_weekly_kenya(), _fetch_weekly_region(), _is_x(), _posted_stock(), Return True if the cell at col_idx holds an 'x' / cross mark (marks 'not…, Bag types with posts logged without a colour in any of the posting tabs. (+9 more)

### Community 62 - "fetch_new_products_data"
Cohesion: 0.20
Nodes (14): fetch_new_products_data(), _apply_stock(), _bag_post_rows(), _post_lookup(), _key(), _keyed(), _np_week_bags(), odoo_sales_window() (+6 more)

### Community 63 - "daydream skill (Vault Daydream)"
Cohesion: 0.50
Nodes (4): Daydream Architecture (orchestrator + Sonnet synthesis + Haiku critique), Gwern's LLM Daydreaming (inspiration source), history.json dedup tracking file, daydream skill (Vault Daydream)

### Community 64 - "write_bags_offer_source"
Cohesion: 0.29
Nodes (7): Counted by how it was sold, _has_deals(), _load_source(), True when the on-offer source carries any Power Deal / Deal of the Week — a…, bags_offer_source.json if written in the last 15 min for this month (and it has…, Kenya on-offer bag set (tagged by offer) + the not-on-offer list, for…, write_bags_offer_source()

### Community 65 - "db.py"
Cohesion: 0.12
Nodes (17): functools, hashlib, lib/db.py — Postgres access for the marketing dashboard. Deliberately the SAME…, lib/footfall.py — footfall (visitors counted per shop per day) joined to walk-…, lib/laya.py — Laya, the on-device decision model, for the dashboard (spec:…, lib/pos_lines.py — till lines with refunded combos fixed (docs/README.md ›…, pandas, pickle (+9 more)

### Community 66 - "load_rows"
Cohesion: 0.15
Nodes (16): Out of stock — call back, fixture, _date(), load_rows(), _online_rows(), oos_by_bag_shop(), {period: {product name: {shop: people}}} straight from Odoo names, or {} if…, Odoo translatable names can come back as {'en_US': …}. (+8 more)

### Community 67 - "Shop Stock Levels — min / max per shop, stocks report and next-month preparedness"
Cohesion: 0.11
Nodes (17): Bag health (by bag, 18 Oct 2026), Data, Each shop's monthly need per bag ("the way we did the targets"), Min / Max (per shop, per bag — colours folded; colours on hover), Next month (preparedness) — from the 15th, November preparedness — shops only vs with CBD + VLD (buffer stock, 18 Oct 2026), Page, Product rating and core 5 vs other 13 categories (18 Oct 2026) (+9 more)

### Community 68 - "TTL disk-cache rationale (.odoo_cache/)"
Cohesion: 0.67
Nodes (3): DENRI_FORCE_FRESH=1 env var, lib/db.run_query_cached() TTL disk cache, TTL disk-cache rationale (.odoo_cache/)

### Community 70 - "Month-End Routine"
Cohesion: 0.14
Nodes (12): _collect_comments(), _html_text(), Automatic (no need to remember), Live vs. archive — how the current month and past months split, Month-End Routine, Notes & gotchas, Optional: schedule it, Run it by hand (+4 more)

### Community 71 - "live_month_window"
Cohesion: 0.11
Nodes (18): Period selector (Monthly / Weekly / Last week / Custom), corporate_from_db(), Current month's corporate bags, live from Odoo invoices. 0 when the DB isn't…, odoo_weekly_breakdown(), Current month's Weekly Performance, live from Odoo. Cuts the month into Sun–Sat…, main(), month_window(), date (+10 more)

### Community 72 - "marketing_dashboard.sql"
Cohesion: 0.32
Nodes (11): denri_mkt_combo_requests, denri_mkt_combo_sales, denri_mkt_monthly, denri_mkt_new_products, denri_mkt_offers, denri_mkt_self_made_summary, denri_mkt_timed_offer_bags, denri_mkt_timed_offer_days (+3 more)

### Community 73 - "fetch_posting_data"
Cohesion: 0.15
Nodes (11): _bt_on_offer(), _dead_clear(), fetch_posting_data(), _clear(), _yield(), _post_yield(), Marketing & Sales Alignment — posting yield, measured the way marketing…, {catalogue name: net units moved INTO the region's shops on/after `since`} from… (+3 more)

### Community 74 - "build"
Cohesion: 0.05
Nodes (46): actions(), build(), agg(), week_tot(), num(), pearson(), What we can do' — by rule (docs/footfall-marketing.md › Actions). Each names a…, JSON-safe number: NaN / None → None. (+38 more)

### Community 75 - "shop_birthdays.py"
Cohesion: 0.14
Nodes (24): by_shop(), _entry(), for_shop(), in_month(), _key(), load(), next_up(), _on() (+16 more)

### Community 76 - "kpi_anim.js"
Cohesion: 0.60
Nodes (5): count(), fmt(), key(), parse(), scan()

### Community 77 - "Denri Africa Dashboard Design System (skill)"
Cohesion: 0.18
Nodes (12): Card component (base building block), Card entrance animation via CSS @keyframes + animation-fill-mode: both, dashboard-insights (related skill), Data Injection Block pattern (SECTION_DATA_START/END markers), Denri Africa Dashboard Design System (skill), Signature Element — Flowing Border (achievement cards), high-end-visual-design (related skill), KPI Tile component (+4 more)

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
Cohesion: 0.13
Nodes (20): baseline(), main_reason(), offer_check(), lib/push_laya.py — Laya's second opinion on the Push Planner (spec: docs/push-…, The bag's facts as short plain sentences — what Laya reads., agrees when yes ≥ max(0.5, baseline + 0.25); disagrees when yes ≤ baseline -…, Mean 'yes' Laya gives `statement` for up to n bags that are fine (None if it…, {"code", "label", "confidence", "verdict"} or None. Choice among the bag's own… (+12 more)

### Community 82 - "family"
Cohesion: 0.40
Nodes (6): ({BAG: units}, {BAG: {colour: units}}) at CBD/Stock., warehouse_stock(), family(), _load(), _norm(), Colour family for a product name (Odoo or sheet spelling; "[REJECT]" ignored).…

### Community 83 - "test_push_planner.py"
Cohesion: 0.16
Nodes (20): build_facts(), Facts for every bag × market that has stock or sold in the window…, add_peers(), _days_back(), facts(), The facts for one bag in one market. daily {iso date: units} over the last…, Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price…, day() (+12 more)

### Community 84 - "build_offer"
Cohesion: 0.15
Nodes (8): build_offer(), offer_kenya_posts(), post_window(), _price_sql(), Compute the full TO payload for a single offer dict. Rebinds the per-offer…, (first, last) date of an offer's posting window: POST_LEAD_DAYS before…, {BAG_UPPER: kenya_posts} over the offer's posting window, from marketing's…, _shop_sql()

### Community 85 - "history.py"
Cohesion: 0.13
Nodes (21): dotenv, fetch_months(), bucket(), inject(), main(), _num(), history.py — build the dashboard History page from Supabase. Reads the…, psycopg2 numerics come back as Decimal — make them JSON-friendly. Whole numbers… (+13 more)

### Community 86 - "offer_picking.py"
Cohesion: 0.10
Nodes (32): _alt_cost(), _apply_alias(), build(), _build_catalog(), _combo_cost(), _combo_slots(), _is_full_price(), _monthly_bag_sales() (+24 more)

### Community 87 - "F"
Cohesion: 0.17
Nodes (21): build_reasons(), Adds notMoving + reasons to every row (lib/push_rules.reasons). Returns the…, context(), not_moving(), A bag with stock that isn't clearing: cleared < 30% this month, or > 45 days of…, What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers…, Every reason that applies to a not-moving bag, each {code, label, text} with…, reasons() (+13 more)

### Community 88 - "test_fixB_offer_units.py"
Cohesion: 0.53
Nodes (5): Tests for lib/offer_units.py Kenya combo units (20 Nov 2026 audit fix #19).…, _run(), test_returned_combo_comes_off(), test_split_by_bag_not_by_list_order(), test_two_lines_of_one_combo_count_two()

### Community 89 - "test_stockout_demand.py"
Cohesion: 0.14
Nodes (23): aggregate(), attach_stock(), collect(), _in(), stockout_demand.py — distinct people who asked for each product while it was…, Add each shop's on-hand to an aggregate() block, in place: [shop, people]…, {period: (start, end)} for the dated periods. month_window = (first, last day)…, {period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or… (+15 more)

### Community 90 - "README.md"
Cohesion: 0.17
Nodes (7): Agent skills — retail analytics, Test a skill, Use in another project, Deliver, Sales-share targets per product, Steps, Tests

### Community 91 - "shop-birthdays.md"
Cohesion: 0.33
Nodes (4): Shop birthdays, Shop → opening date, Where it shows, Shops & Regions (doc — source of truth)

### Community 92 - "monthly_target_rows"
Cohesion: 0.14
Nodes (14): fetch_monthly_target(), fetch_sheet_data(), date, The Sun–Sat week containing `ref` (defaults to today) — matches the dashboard's…, week_window(), monthly_target_rows(), monthly_target_sheet_rows(), MONTHLY_TARGET rows with column C = the bag's target from Odoo (docs/product-… (+6 more)

### Community 93 - "_odoo_colour"
Cohesion: 0.25
Nodes (8): _odoo_colour(), The colour as the product itself is named — the product name minus its bag…, ({PRODUCT: {SHOP CODE: units}}, {PRODUCT: {SHOP CODE: [[colour, units], …]}})…, shop_sales(), _aliases(), odoo_name(), {NORM(odoo name): NORM(sheet name)} from product_aliases.csv — products Odoo…, Odoo's spelling of a catalogue name (the reverse of product_aliases.csv), for…

### Community 94 - "Dashboard Architecture (static HTML + Python generator + injected data block)"
Cohesion: 0.40
Nodes (5): DATA_START/DATA_END comment marker injection pattern, build_all.py (rebakes every page), Dashboard Architecture (static HTML + Python generator + injected data block), .github/workflows/refresh.yml CI workflow, shell.html (sidebar nav frame, loads each page into an iframe)

### Community 95 - "negative_fixes.py"
Cohesion: 0.08
Nodes (35): argparse, _negfix(), Stock record accuracy per shop for every period (docs/shops-efficiency.md ›…, bags_sold(), block(), by_shop(), _date(), _int() (+27 more)

### Community 96 - "custom_range.py"
Cohesion: 0.19
Nodes (14): block(), from_argv(), label(), load(), month_share(), path(), Per-page Custom period: the From – To dates a page was last built for. Each…, (from, to) dates for the page's Custom period, or None. Swapped if reversed;… (+6 more)

### Community 97 - "test_oos_callbacks.py"
Cohesion: 0.17
Nodes (20): aggregate(), flat(), split(), {shop: set(person)} → (distinct people, [[shop, people], …] high → low)., The page block: {period: {key: {"total": people, "shops": [[shop, people],…, _shops(), _base_sql(), _kai() (+12 more)

### Community 98 - "master_products"
Cohesion: 0.50
Nodes (4): master_products(), _norm_name(), Match the SQL normalisation: lower-case, '.'→space, collapse whitespace., Normalised, de-duplicated master catalogue names (master_products.txt), for the…

### Community 99 - "Bag Signals — quant view of each bag (posting · stock · selling)"
Cohesion: 0.40
Nodes (4): Action (first rule that fits), Bag Signals — quant view of each bag (posting · stock · selling), Page, Per bag

### Community 100 - "beats.py"
Cohesion: 0.20
Nodes (14): Per bag × market: the facts (`push_rules.facts`, `add_peers`), Prices (30 Oct 2026, user's call), _n(), price(), projections(), Three beats for each Current Performance card (docs/current-performance.md ›…, Forward Projections cards: bags and revenue together, and what the gap between…, Price per Bag card: the price gap, and the group that drags revenue most. (+6 more)

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
Cohesion: 0.08
Nodes (37): fnmatch, _age_min(), _cleanup(), fresh_meta(), _meta(), _p(), query(), lib/snapshot.py — local DuckDB snapshot of the tills (docs/README.md › DuckDB… (+29 more)

### Community 105 - "Pricing rule — two tiers (BAND cost cutoff) + hand pins"
Cohesion: 0.33
Nodes (6): "Below cost" flag, "No BOM" flag, "Pinned" flag, Pricing rule — two tiers (BAND cost cutoff) + hand pins, reject_overrides.json (hand-pinned prices), "Thin" margin flag

### Community 106 - "build"
Cohesion: 0.08
Nodes (33): why_moved(), _load_shop_regions(), Shop → Region from docs/shop-regions.md (lib/shop_regions); the built-in…, doc(), day_for(), load(), [{"till", "shop", "from", "to", "asDate"}] — datetimes / dates parsed; [] if…, The day a till's sales of `day` count on (day granularity). (+25 more)

### Community 107 - "reject_variants"
Cohesion: 0.12
Nodes (17): Kenya timed-offer campaigns from timed_offers_config.json (normalised by…, _timed_offers(), _bags_from_file(), _derive_month(), load_config(), _norm_offer(), _parse_colour(), Multi-offer config: {"month": "YYYY-MM", "offers": [offer, ...]}. Back-compat:… (+9 more)

### Community 108 - "Ralph task — only three sheet tabs left"
Cohesion: 0.40
Nodes (4): Added mid-task (user), Monthly inputs (user uploads), Ralph task — only three sheet tabs left, Steps (verify each)

### Community 109 - "check_connection"
Cohesion: 0.11
Nodes (24): _corporate_bags(), The month's revenue target (KES): Odoo sales_pos_target amount (pos +…, (corporate bags, corporate KES received) in the given month, live from Odoo…, _revenue_target(), odoo_bag_daily_value(), odoo_bulk_lines(), odoo_daily_kenya(), odoo_list_price() (+16 more)

### Community 110 - "Bag targets October 2026_3acbad00.md"
Cohesion: 0.50
Nodes (3): Sheet: Bag targets, Sheet: Inputs, Sheet: Method

### Community 111 - "main"
Cohesion: 0.12
Nodes (18): Did last week's calls work? (`push_rules.record_week`, `followup`), main(), month_progress(), payload(), Last week's calls checked against what happened (lib/push_rules.followup), then…, Per market: sold this month so far (from the daily sales), days elapsed / left,…, _slim(), weekly() (+10 more)

### Community 112 - "Semantic color rules (green=good, amber=risk, red=critical, cyan=info)"
Cohesion: 0.50
Nodes (4): Design Tokens (colors, typography, spacing), Semantic color rules (green=good, amber=risk, red=critical, cyan=info), Analytics Dashboard specific rules (VISUAL_DENSITY: dense), Region colour palette (reference for Executive Dashboard)

### Community 114 - "Out-of-stock demand — people, not requests"
Cohesion: 0.29
Nodes (7): Input rows — one per enquiry × product asked for, Keying, Out-of-stock demand — people, not requests, Output block, Periods, Show it as, Tests

### Community 121 - "bag_classifier"
Cohesion: 0.16
Nodes (16): _add_noffer_posts(), per_bag(), _add_oos(), bag_classifier(), infer(), _norm(), _load_bag_prices(), _norm_combo() (+8 more)

### Community 122 - "fetch"
Cohesion: 0.13
Nodes (24): _archived_source(), _as_date(), fetch(), cat_tier(), classify(), classify_for(), combo_slots(), make_classifier() (+16 more)

### Community 123 - "What the page shows"
Cohesion: 0.20
Nodes (10): 1. Bag of the Week / Month, 2. Top-selling bags — % share, 2b. Shop breakdown (22 Oct 2026, user's call), 3. Categories — % share, 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call), 4. Colours — % share, Data, Popover waterfall — why the units moved (26 Oct 2026, user's call) (+2 more)

### Community 126 - "Product (bag) targets"
Cohesion: 0.20
Nodes (10): A month with only a revenue target (November 2026), Estimated targets — the method without Odoo's total (16 Oct 2026, user's call), No zero targets, Output columns, Product (bag) targets, The split — by each bag's share of recent sales, The total, Used as the monthly bag target (from October 2026) (+2 more)

### Community 128 - "test_share_targets.py"
Cohesion: 0.22
Nodes (11): allocate(), available_days(), share_targets.py — split a period's total target across products by recent…, Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.…, Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale},…, Tests for share_targets.py — python -m pytest scripts -q, test_available_days_rebuilt_backwards_from_today(), test_min_days_stops_a_brand_new_bag_inflating() (+3 more)

### Community 138 - "Chart type switcher (every chart, every menu)"
Cohesion: 0.22
Nodes (7): Chart type switcher (every chart, every menu), Layout rules, Skipped charts, Types offered (only when the data suits them), Week change (9 Oct 2026), What it does, Current Performance (doc)

### Community 145 - "_bag_stock"
Cohesion: 0.40
Nodes (5): _bag_stock(), _combo_bags(), _norm_bag(), Space/punctuation-insensitive key so 'MINIZURI' matches 'MINI ZURI'., Component bags of an offer, each with its stock, sorted most-stock first.

### Community 153 - "New Products Analytics (doc)"
Cohesion: 0.16
Nodes (14): New Products Analytics (doc), KPI card layout (one card-grid, primary Monthly Sales card), match_odoo_bags [S_0] internal-reference prefix fix, Weekly Performance chart (Week 1 to latest), Combo component attribution (combo_product_attribute_values, ast.literal_eval), Deals matcher _match (_full/_rooted/_stock_match, DEAL_ALIASES), Product / name matching (doc), match_odoo_bags prefix matcher ([S_0] fix) (+6 more)

### Community 154 - "_matches_sheet"
Cohesion: 0.18
Nodes (10): Three countries, one page (9 Oct 2026), _matches_sheet(), _opt_close(), Two normalised slot options name the same bag, loosely: equal ignoring spaces…, Same slot count and every slot overlaps under SOME pairing (any order: the…, The sheet label this Odoo combo maps to, or None if it isn't on the sheet.…, _slots_fit(), Inputs (from the user, Oct 2026) (+2 more)

### Community 155 - "Offer Picking (doc)"
Cohesion: 0.25
Nodes (9): Baseline forecast (frozen snapshot), Offer Picking (doc), Forecast (picked combos) — PICK/PRODUCE tiers, offers_prices.json downloaded copy & offline fallback / lock override, WAS vs NOW pricing (offers sheet, FULL_PRICE_BAGS), Profit computation (cost/price/margin), Seasonality (2025 combo calendar x POS sales), Bag-type matching for combo components (_match_bag / BAG_ALIASES) (+1 more)

### Community 156 - "start_server"
Cohesion: 0.18
Nodes (16): _is_quota_error(), _is_transient(), A one-off network hiccup worth an immediate retry — a Google Sheets read…, _run_one(), run_scripts(), start_server(), copyfile(), do_GET() (+8 more)

### Community 157 - "build"
Cohesion: 0.12
Nodes (16): Offer type summary (matrix), Load the downloaded copy: ({BAG: {category, price, offer}}, locked?)., {BAG (upper): {category, price, offer}} → (offers, source), from…, _read_offers(), _read_offers_cache(), _assign_price(), build(), _category_of() (+8 more)

### Community 158 - "timed_offers.py (generator)"
Cohesion: 0.09
Nodes (22): month_end.py (rollover archiver), monthly_report_history.json, monthly_report.py._read_timed_offers(), renderOffer(TO, root) function, Timed Offers Analytics (doc), timed_offers_config.json (config), timed_offers.html (output), timed_offers.py (generator) (+14 more)

### Community 159 - "scripts/receipt_combos.py"
Cohesion: 0.33
Nodes (5): bag_key(), _fits(), receipt_combos.py — find combos in till receipts that ring every item as its…, Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'., Bag types fill the offer's slots one-to-one in some order (alternatives per…

### Community 160 - "_dead_stock_region"
Cohesion: 0.29
Nodes (7): _dead_stock_region(), pct(), summarise(), _dead(), True only for a genuine MONTHLY_MARKETING_POST product row (colour A, name C)., Dead Stock Accountability for one region, one period (month or week). Dead…, _real_mmp()

### Community 161 - "new_products.py"
Cohesion: 0.18
Nodes (7): _base_colour(), _merge_rows_by_base_colour(), new_products.py…, Upper-case, punctuation-normalised string with known qualifier tokens…, Canonical base-colour grouping key: 'Black 018'/'CN Black' -> 'Black'; 'Sky…, Group rows by (bagType upper, base-colour upper) and SUM numeric_fields across…, _strip_colour_qualifiers()

### Community 162 - "timed_offers.py"
Cohesion: 0.13
Nodes (21): _acc(), _bucket(), build_compare(), _cmp_lines(), _days(), _kenya_net_moves_since(), kenya_stock_by_bag(), odoo_bag_prices() (+13 more)

### Community 163 - "num"
Cohesion: 0.20
Nodes (11): _garr_line(), gnum(), num(), _offers(), _parse_offers(), _units(), This month's timed-offer campaigns, flattened for storage. The live TO payload…, Greedy single-line array extractor — handles nested [[...],[...]] arrays. (+3 more)

### Community 166 - "odoo_month_product_bags"
Cohesion: 0.33
Nodes (6): odoo_combo_product_bags(), odoo_lifetime_product_bags(), odoo_month_product_bags(), All-time bags per product from Odoo (no month window) — the lifetime sales of…, [(product name, bags)] for bags sold INSIDE combos (sub_product_line) in the…, Reporting month's bags per product from Odoo (Postgres), or None if the DB…

### Community 167 - "Menu 1 Current Performance in the 3-beat layout (preview)"
Cohesion: 0.15
Nodes (12): 0. New: an executive summary strip at the top of the page, 1. Sales, Weekly Sales and Remaining Target cards, 2. Followers & Reach, 3. Weekly Performance — Week 1 to Latest, 4. Why Did We Move?, 5. Sales vs Monthly Target, Week-over-Week, Bare Minimum, 6. Forward Projections (Standard and Forecasted), 7. Price per Bag, and On offer vs not on offer (+4 more)

### Community 168 - "odoo_marketing_audit.py"
Cohesion: 0.39
Nodes (8): root(), audit(), _expected(), main(), _period(), _range(), scripts/odoo_marketing_audit.py — how complete and up to date each marketing…, _step()

### Community 169 - "Footfall and Marketing (21 Oct 2026, user's call)"
Cohesion: 0.20
Nodes (9): Actions (rules), Correlations ("Posts and ads vs visitors"), Data traps (said on the page), Definitions, Footfall and Marketing (21 Oct 2026, user's call), Regenerate, Shop mapping (`lib/footfall.SHOPS`), Sources (+1 more)

### Community 172 - "get_rows"
Cohesion: 0.14
Nodes (15): load(), _build(), default_window(), get_rows(), last_complete_week(), offer_flags(), _ok(), prime_offer_flags() (+7 more)

### Community 173 - "load_pages"
Cohesion: 0.20
Nodes (10): _growth_tracking(), data/growth_tracking.json + the report month: live (so far + projected + this…, _kenya_target(), load_pages(), bag_of(), Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.…, Kenya's month target from current_performance.html (PERF.totalTarget), or None., html() (+2 more)

### Community 174 - "Product Performance — Shop breakdown: progress"
Cohesion: 0.22
Nodes (8): 1. Spec — DONE, 2. Data — DONE, 3. Page section — DONE, 4. Sidebar and sticky bar — DONE, 5. Visual check — DONE, 6. Wrap-up — DONE, Product Performance — Shop breakdown: progress, Summary

### Community 175 - "_seasonality"
Cohesion: 0.20
Nodes (11): Per combo in the 2025 monthly calendar: planned months, actual sales by…, _region_of(), _seasonality(), best_match(), price_of(), _build_sheet_slots(), _combo_odoo_slots(), _combo_sheet_slots() (+3 more)

### Community 177 - "norm"
Cohesion: 0.23
Nodes (10): build_rows(), _Deriver, _flag_cells(), _fmt(), norm(), _products(), Name key shared by the catalogue and Odoo: upper-case, '.'→space, collapsed…, Labels for an Odoo product the catalogue doesn't know yet, learnt from the… (+2 more)

### Community 178 - "lib"
Cohesion: 0.11
Nodes (24): collections, csv, bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend,…, footfall_marketing.py — Footfall and Marketing page (spec: docs/footfall-…, shop_launch.py — the Shop Launch page: a new shop from its first sale (spec:…, lib, lib/ads.py — marketing's Weekly Ads Performance Report, as data (spec:…, lib/bag_quant.py — quant signals per bag: drift, volatility, Sharpe-style… (+16 more)

### Community 179 - "Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)"
Cohesion: 0.20
Nodes (9): 1. Spec — DONE, 2. SQL + library — DONE, 3. Generator — DONE, 4. Page — DONE, 5. Actions — DONE, 6. Visual check — DONE, 7. Wrap-up — DONE, Findings (16 weeks, 28 Jun – 17 Oct 2026; last fully counted week 11–17 Oct) (+1 more)

### Community 180 - "shops_efficiency.py"
Cohesion: 0.22
Nodes (7): metric_byshop(), parse_sheet(), shops_efficiency.py…, Return (data, meta) for the Kenya shops, locating columns by header name…, safe_int(), update_history(), pathlib

### Community 182 - "bags_on_offer.py"
Cohesion: 0.26
Nodes (11): _base_windows(), _custom_range(), fmt(), inject(), main(), bags_on_offer.py…, (from, to) dates from boo_custom_range.json — the Custom period — or None., Write (or with a=None, delete) the Custom period's dates. (+3 more)

### Community 183 - "_is_checked"
Cohesion: 0.14
Nodes (23): _analyze_region(), _fetch_monthly_kenya(), _fetch_sinza_monthly(), _fetch_sinza_weekly(), _fetch_uganda_monthly(), _fetch_uganda_weekly(), fmt_int(), _is_checked() (+15 more)

### Community 185 - "test_sheet_reads.py"
Cohesion: 0.47
Nodes (4): Guard: the dashboard reads ONLY three Google-Sheet tabs — MONTHLY_TARGET,…, _sources(), test_only_the_main_spreadsheet(), test_only_three_tabs_are_read()

### Community 187 - "Ralph loop brief — Footfall and Marketing page"
Cohesion: 0.25
Nodes (7): DATA FACTS (verified 21 Oct 2026), DONE, ESCAPE HATCH, PROJECT RULES (must hold every iteration), Ralph loop brief — Footfall and Marketing page, SELF-CORRECTION, SUB-GOALS (do in order; tick each in notes/footfall_progress.md with the command output that proved it)

### Community 188 - "attach_stock"
Cohesion: 0.24
Nodes (11): bag(), attach_stock(), in_stock(), stk(), collect(), _in(), is_combo_request(), True when the request names a whole combo ("Amaya Handbag or Elyse Handbag +… (+3 more)

### Community 189 - "_bag_tiers"
Cohesion: 0.50
Nodes (4): _bag_tiers(), _price_tier(), Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000…, {BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments).…

### Community 191 - "Bag signals — quant finance applied to product sales"
Cohesion: 0.33
Nodes (6): Action — first rule that fits, Bag signals — quant finance applied to product sales, How to deliver it, Inputs you must build from the project's data, Maths (per product), Tests

### Community 194 - "Bag Tracking"
Cohesion: 0.33
Nodes (5): Bag Tracking, Page, Prices, Stock, The bags

### Community 195 - "build"
Cohesion: 0.20
Nodes (11): build(), _cfg(), _colour(), _folder(), canon(), _moves(), Odoo product name → the dashboard's bag name (Offer Picking's _build_catalog…, {BAG TYPE (upper): production cost} from bom_costs.json — the local copy of the… (+3 more)

### Community 197 - "Ralph task — "Out of stock — call back" demand per shop"
Cohesion: 0.25
Nodes (8): match_odoo_bags(), Sum Odoo bags whose product name is the new product's — matched by name prefix…, Established facts (do not re-investigate), Every iteration, Periods (dates in Africa/Nairobi), Ralph task — "Out of stock — call back" demand per shop, Stopping, Sub-goals (in order)

### Community 200 - "shop_stock_levels.py"
Cohesion: 0.08
Nodes (44): Sales pace to month end (19 Oct 2026), bag_categories(), buffer_stock(), build(), _clamp(), dispatch_shop(), fit(), grand_total() (+36 more)

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
Cohesion: 0.12
Nodes (16): count_complete_weeks_in_month(), _fold_bag_level(), load_dead_thresholds(), _mkt_perfect_week_index(), _mkt_week_label(), _offer_bagtypes_by_region(), posting_yields.py…, Bags whose posts marketing logs only per BAG (the posting sheet's TOTAL row,… (+8 more)

### Community 221 - "base_name"
Cohesion: 0.20
Nodes (11): apply_walkins(), base_name(), dispatch_by_product_shop(), _num(), The catalogue key for an Odoo product name: norm() without the "[REJECT]" tag…, {NORM(product): {SHOP: bags}} of POS bag sales in [start, end]; None if DB…, {NORM(product): {SHOP: bags distributed in}} from combined_distribution.sql's…, {NORM(product): {SHOP: on-hand}} live, Kenya shops + Sinza (DAR) + Uganda (UG). (+3 more)

### Community 223 - "data"
Cohesion: 0.11
Nodes (20): Update the rolling snapshot. Returns (carryover_bags | None, captured_on,…, Sunday that starts the Sun–Sat sales week containing d., Prefer the real current-week bags from Postgres (weekly_sales_db.json, written…, update_month_boundary(), week_start_of(), weekly_from_db(), _live_bags(), _categories() (+12 more)

### Community 227 - "product_performance.py"
Cohesion: 0.06
Nodes (47): Bulk orders, build(), corp(), categories(), corporate_period(), _d(), explain(), _fmt_d() (+39 more)

### Community 235 - "load_catalog"
Cohesion: 0.50
Nodes (4): catalog_rows(), load_catalog(), [{colour, category, name, bag}] in sheet order, from product_catalog.csv., [header] + [[COLOUR, CATEGORY, PRODUCT NAME, BAG TYPE], …] — the label columns…

## Knowledge Gaps
- **253 isolated node(s):** `PERF`, `The rule`, `Steps`, `Preventing it`, `graphify` (+248 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1107 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Shops & Regions (doc — source of truth)` connect `shop-birthdays.md` to `Semantic color rules (green=good, amber=risk, red=critical, cyan=info)`, `Chart type switcher (every chart, every menu)`, `self_made_combos.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `run_query()` connect `run_query` to `shop_corporate.py`, `tests/test_receipt_combos.py`, `get_engine`, `_enrich_deals`, `shop_requests.py`, `signals`, `Bags on offer vs not on offer`, `odoo_stock_by_product`, `live_anchor`, `chronos_train.py`, `odoo_month_product_bags`, `build_payload`, `month_extras.py`, `build`, `odoo_marketing_audit.py`, `_seasonality`, `bag_key_fn`, `_combo_button_usage`, `fetch_new_products_data`, `db.py`, `build`, `Ralph task — "Out of stock — call back" demand per shop`, `live_month_window`, `shop_stock_levels.py`, `fetch_posting_data`, `build`, `build`, `offer_picking.py`, `_odoo_colour`, `base_name`, `negative_fixes.py`, `test_oos_callbacks.py`, `product_performance.py`, `snapshot.py`, `build`, `check_connection`, `fetch`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `Monthly Report (doc)` connect `Self-made combos vs running combos (doc)` to `New Products Analytics (doc)`, `shop-birthdays.md`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **What connects `PERF`, `The rule`, `Steps` to the rest of the system?**
  _253 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `shop_corporate.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14532019704433496 - nodes in this community are weakly interconnected._
- **Should `add_laya` be split into smaller, more focused modules?**
  _Cohesion score 0.07386363636363637 - nodes in this community are weakly interconnected._
- **Should `tests/test_receipt_combos.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05432595573440644 - nodes in this community are weakly interconnected._