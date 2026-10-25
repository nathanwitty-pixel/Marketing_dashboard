# Dashboard Menu Docs

One file per menu in the Denri / Bagware Marketing Dashboard. **These are the spec.**
When a page needs changing, correct the relevant `.md` here first, then make the code
match it.

## Where the data comes from (Oct 2026)

**Google Sheets — only three tabs** of the main spreadsheet (`1Zb8Ly6v…`):
`MONTHLY_TARGET` (on-offer ✅ col F; New Products now use `data/new_products.txt` + Odoo targets), `MONTHLY_MARKETING_POST` and
`WEEKLY_MARKETING_POST` (posts — now only a fallback, see below). Nothing else is read from any sheet —
`tests/test_sheet_reads.py` fails if code reads another tab or another spreadsheet.

**Marketing posts (16 Oct 2026):** read from marketing's own daily posting sheets by `lib/marketing_posts.py` —
Kenya: *MARKETING POSTS KENYA* (`1Os81Lhn…`) tab `2026`; Sinza / Uganda: *STOCKS & POSTING RECORDS* (`1DGrRYrv…`)
tabs `MARKETING POSTS_SINZA` / `MARKETING POSTS_UGANDA`. Row 2 = BAG TYPE · COLOUR · one column per day. Summed into
the old tabs' layout: **weekly = last complete Sun–Sat week, monthly = the live month to date**. From Sep 2026
marketing logs posts only on each bag's TOTAL row (no colour) → those come through as bag-level rows
(`<BAG>` / "(all colours)"), compared per bag on New Products and Posting Yields. Both spreadsheets must be shared
(Viewer) with the service account; until they are, the old two tabs are read (with a warning).

**Monthly uploads (the user sends them, Claude transcribes):**
- `offers_monthly.csv` — Kenya / Sinza / Uganda combos and singles with prices (the old COMBOS tab).
- `deals_kenya.csv` — Kenya Power Deals + Deals of the Week from the poster images (the old deals sheet).
- **Weekly:** `ads_weekly.csv` + `ads_notes.csv` — marketing's Weekly Ads Performance Report (Drive .pptx).
  Was the Ads impact panel on every page; **hidden on every page since 26 Oct 2026** — spec: [ads-impact.md](ads-impact.md).

**Stock record accuracy (Oct 2026):** the **NEGATIVE FIX LOG** tab of *STOCKS LEVELS 2026* (`1xWmk1CJ…`, read only by
`lib/negative_fixes.py`) ranks shops by negative-stock fixes per 1,000 bags sold on Shops Efficiency — spec:
[shops-efficiency.md](shops-efficiency.md#stock-record-accuracy-22-oct-2026-users-call).

**Footfall (Oct 2026):** `denri_footfall_count` (visitors per shop per day) joined to walk-in POS orders,
WhatsApp chats, posts and ads on the Footfall and Marketing page — spec: [footfall-marketing.md](footfall-marketing.md).

**Odoo** — sales, stock, dispatch, combos rung, WhatsApp call-backs. If Odoo is down, those figures are
empty (no sheet fallback any more). **Local files** — `bom_costs.json` and `offers_prices.json` (Offer
Picking costs / prices), `product_catalog.csv`, `bag_original_prices.json`, `bag_names.csv`.

**Combo refunds — one rule on every menu (25 Oct 2026, user's call).** Every query that counts till bags reads
the order's lines through `POS_LINES(p) pl` (expanded by `lib/pos_lines.py` inside `db.run_query`), not
`pos_order_line` directly. That source fixes refunded combos, so each returned bag is taken off exactly once:
- A refund that brought the combo's bags back on their own **KES 0 lines** (no parent link) → those lines are
  marked as the combo's sub-lines. Sales-style counts still subtract them; single-bag counts (Bags on offer,
  Combos, Push planner…) no longer take them off a second time as singles.
- A refund that has **only the combo line** → the original sale's bags (via `refunded_orderline_id`, exact
  colours) are added as KES 0 sub-lines with negative qty, so Sales-style counts take them off too.
- Oct 2026: 14 combo refunds, 28 bags. Before: Sales missed 12 (6 combo-line-only refunds) and Bags on offer
  took 16 off twice.
- The offer page also counts customized bags (they are bags; only the "Customization" fee is not) and
  Tanzania / Uganda **Mini Washbags and gift bags** like Kenya's, so its All bags = Sales + samples.

## Refresh performance

Each `/api/refresh` (the "Refreshing data…" spinner) runs a generator as a fresh
subprocess, so the Supabase pool is cold every time (~5s first connect). The pooler has
~0.5s latency and `lib/db.py` uses `pool_pre_ping`, so a fresh-per-query connection would
pay a ping round-trip before **every** query — ~1s each, ~15 per page. Instead
`lib/db.run_query` **reuses one connection for the whole process** (`_shared_conn`, opened
on the first query, reconnected once if it goes stale). Because every generator is its own
short-lived subprocess and the long-lived `main.py` server never runs queries, this is safe
and needs no per-generator wrapping — it roughly **halves** query time everywhere. Google
Sheets reads are the other big cost: `offer_data.build` (cached per run) fetches all its
ranges (COMBOS, MONTHLY_TARGET, STOCK_LEVELS) in **one `values_batch_get`** instead of a
`worksheet()` lookup + read per sheet — ~5s → ~3s. Together these took a self_made_combos
refresh from ~50s to ~32s.

**DuckDB till snapshot (26 Oct 2026, user's call).** Heavy till-sales queries read a local snapshot instead of
the replica. `lib/snapshot.py` pulls, in one go, the last **150 days** of `pos_order` and its lines (already
through `POS_LINES`, so combo refunds are fixed) plus the small lookup tables (`pos_session`, `pos_config`,
`product_product`, `product_template`, `product_category`) into versioned Parquet files under `.snapshots/`
(gitignored), then swaps `.snapshots/current.json` to point at them. `db.run_query_snap(sql, params)` runs the
page's **own SQL unchanged** in an in-memory DuckDB over those files (`POS_LINES(p) pl` → the snapshot's fixed
lines; `:name` → `$name`). It falls back to live Postgres when the snapshot is missing, older than **30 min**
(a manual Refresh renews it if older than **5 min**), doesn't cover the dates asked for, or the SQL needs a table
it doesn't hold. A failed refresh keeps the old snapshot; the last 3 are kept. Proof: `tests/test_snapshot.py`
runs live vs snapshot for a fixed past window and compares. Used by: Timed offers (its sales / daily / price /
bulk queries).

## How the dashboard is built

Each menu is a **static HTML page** with a hand-written render layer (JS + CSS). A
**Python generator** fetches live data (Google Sheets and/or the Odoo Postgres
read-replica), serialises it to a JS object, and injects it into the HTML **between
comment markers** — it replaces only the data block, never the render code. So:

- Editing **layout / charts / wording** → edit the `.html` render layer directly.
- Editing **what data is pulled / how it's computed** → edit the `.py` generator.
- The markers (e.g. `<!-- SMC_DATA_START -->…<!-- SMC_DATA_END -->`) must stay intact.

The dashboard people use is the **Streamlit app** (`streamlit_app.py`) — see
[Where changes go](#where-changes-go). `shell.html` is the local fallback frame that loads
each page into an iframe.
Every Chart.js chart on every page gets a chart-type menu from the shared
`chart_switcher.js` — see [chart-switcher.md](chart-switcher.md).
`scripts/build_all.py` re-bakes every page headlessly (no server, no browser tab).
Every menu page also gets the shared **page sidebar** from `page_sidebar.js` — see
[Page sidebar](#page-sidebar) below.
Pages with a filter bar also pin it at the top while scrolling with `sticky_controls.js` —
see [docs/sticky-controls.md](sticky-controls.md).

## Page sidebar

A sticky frosted panel beside each page (below 980px it folds into one scrollable
strip above the page). Top to bottom:

- **Picker** (optional) — **Months** on Reporting History; **Regions** (Kenya / Sinza /
  Uganda) on Self-made combos and Posting. Each item: a tile, a name, and a sub-line
  taken from data already in the page (never an invented figure).
- **In this report** — one numbered, colour-coded link per section; the highlight
  follows the section on screen (scroll-spy). Sub-items (`·`) can fold so only the
  current group shows (`collapseSubs`).
- **Back to top.**

API (plain JS, no deps):

```js
PageSidebar.init({
  content: 'body > .wrap',   // the page's main container (several matches are wrapped together)
  picker: null | { label, items: [{ id, label, sub, pct, color, tile }], active, onSelect(id) },
  sections: () => [{ el, name, num, color, sub }],
  collapseSubs: false
});
PageSidebar.setActive(id);   // picker highlight
PageSidebar.refresh();       // rebuild the section list after the page re-renders
PageSidebar.headings(sel, wrapSel)   // helper: sections from headings
```

Rules:

- **Region proxy.** A Regions picker never re-implements switching: it clicks the page's
  own region control (hidden, kept in the DOM), so the page's switch code stays the one
  place that changes region. Only real Kenya / Sinza / Uganda switches become a picker —
  Bags on offer's region chips are Kenyan sales areas filtering one table, so they stay
  beside it.
- **Styling.** The CSS ships inside `page_sidebar.js` and is injected as a `<style>`
  element, in the pages' dark palette: `v5_theme.js` only remaps in-page `<style>` rules,
  so light theme recolours the sidebar with everything else.
- **Exports.** The aside carries `data-export-hide`; the shell's Word/PDF export and
  `@media print` leave it out.
- **Whole-file generators.** `generate_insights.py` and `monthly_report.py` write their
  page in full, so the sidebar snippet lives in their templates (`PAGE_SIDEBAR` in
  `monthly_report.py`); every other page keeps it in the `.html` render layer.
- **Scroll-spy** is bound straight to `scroll` (no `requestAnimationFrame`).
- **Embedded mode (Streamlit).** When the page's frame is stretched to full height (the page
  itself can't scroll), the sidebar listens to the parent's scrolling, measures sections against
  the parent viewport, pins itself with a transform and scrolls the parent on click. Smooth
  scrolling is skipped under `prefers-reduced-motion`.

## Where changes go

**One real version: the Streamlit app.** Run `streamlit_app.py` locally (VS Code ▶, `python streamlit_app.py`
or double-click — it launches `streamlit run` itself); Streamlit Cloud runs the same file from GitHub `main`.
`python main.py` → `shell.html` is only a local fallback.

What each piece reads, so a change lands everywhere at once:

| Change | Edit | Reaches |
|---|---|---|
| Add / rename / reorder a page, its purpose, icon, generator scripts | `dashboard_pages.json` | Streamlit menu + `shell.html` nav (both read it) |
| Owner name / title / email | `dashboard_pages.json` → `owner` | Streamlit owner card + welcome card + `shell.html` |
| A page's layout / charts / wording | that page's `.html` (or its generator for Insights / Monthly Report) | every host (Streamlit inlines the page) |
| Page sidebar, theme engine, chart menu | `page_sidebar.js`, `v5_theme.js`, `chart_switcher.js` | every page on every host |
| Streamlit chrome (top bar, owner card) | `streamlit_app.py` | Streamlit (local + cloud) |
| Tab scrolling in the top bar (wheel, drag, slim scroll bar, ‹ › arrows, edge fades) + the travelling border light on the nav bar / date pill (`.tn-glow`) | `top_nav.js` | Streamlit top bar + `shell.html` |
| Travelling purple → pink border light on KPI tiles (`.kpi`, `.mini`, cards with a value inside) | `v5_theme.css` | every page in both shells |
| Welcome / loading card, Dark Reader lock | `welcome_screen.js` | Streamlit |

**Three copies of every page exist — this is why they drift:**
1. **Your local files** — what you edit, and what the generators rewrite on every refresh.
2. **GitHub `main`** — only what was committed *and pushed*. Uncommitted work never leaves this PC.
3. **Streamlit Cloud's runtime** — starts from GitHub `main`, then **regenerates each page from
   Odoo** when it is older than `AUTO_REFRESH_MIN` (60 min) and someone opens it. So its numbers
   are newer than GitHub's, and its code is only as new as the last push.

**Publishing (local → GitHub → Streamlit Cloud):** double-click `publish.bat` (or
`python scripts/publish.py "what changed"`). It refuses secrets (`.env*`, credentials, `*.pem`, …),
runs the checks (every `.py` compiles, every `.js` and every page's inline scripts pass
`node --check`, every `*_DATA_START/END` pair exactly once, `dashboard_pages.json` loads and its
pages exist), refuses if GitHub is ahead (pull first), shows the changes grouped
(code / pages / docs / data refresh / knowledge graph), asks y/N, then commits and pushes `main`;
Streamlit Cloud redeploys within a minute or two. `publish.bat --dry-run` runs everything but
commits nothing.

**Testing without touching Odoo:** set `DASH_NO_AUTOREFRESH=1` before `streamlit run
streamlit_app.py` — pages are never rebuilt on a page view and idle tabs don't reload
(the manual *Refresh this page* button still works).

**Refreshing (Oct 2026):** every rebuild runs in the background: the hourly auto-refresh, the
**Refresh** button (which bypasses the Odoo cache) and a custom range Apply / Clear. The last-built page
stays on screen. Above it, a progress bar shows the percentage, the time left and the step (when a page
has more than one script). The estimate is how long that page and kind of rebuild took last time
(`.rebuild_times.json`, local only). The first run has no estimate, so the bar just creeps and shows
the seconds so far. When the rebuild ends, the app reruns and the new page swaps in. There is one rebuild
per page, shared by every viewer. A Refresh or range change made while one is running is queued to run
straight after it.

**Hover popovers (Oct 2026), one rule on every page:**
- A popover you can read or scroll gets a **220 ms grace** after the pointer leaves its trigger, so you can
  cross the gap onto it.
- It **stays open while the pointer is on it**, and closes once the pointer has left both the trigger and the popover.
- Entering a **different** trigger (the next row, tile or chip) while one is open **waits 220 ms** before
  swapping, and the swap is cancelled if the pointer reaches the popover. Moving down across the next row no
  longer replaces it.
- Click or tap still pins.
- **Movable (New Products tile / table popovers, `npTilePopover`, 19 Oct 2026):** drag the top bar ("⠿ drag to
  move") to put the popover anywhere; once moved it stays put (no close on leave, scroll or outside click) until
  **×**, Esc, or a click on another number. Drag works from anywhere on it (4 px threshold, so clicks still work).
- **No hover while scrolling (Streamlit, 19 Oct 2026):** `streamlit_app.py` EMBED_FIX sets `html.st-scrolling`
  (body `pointer-events:none`) until 200 ms after the last wheel / parent scroll, so popovers don't open as rows
  pass under the mouse and the wheel isn't caught by tables with their own scroll bar.
- **Scroll speed rules:** `v5_theme.js` re-checks only the element whose `style` changed (not its parent);
  `page_sidebar.js` and `sticky_controls.js` treat the frame as embedded when it carries `data-dash-page`
  (the height test flipped mid-scroll → sticky bars pinned / unpinned every step and the page jumped).

Covered:
- `oos_chip.js` (📞 chips on New Products, Combos and Bags on Offer).
- Combos: shop self-made table (`#smc-smshop-table`) and Deal-of-the-Week shop / category tooltips (`wireDowHover`).
- New Products: KPI card popovers (`attachNpPopover`), KPI tiles (`npTilePopover`) and colour-guidance tiles (`cgPop`).
- Current Performance: Sales card (`attachPopover`, already compliant).

Exempt: browser `title` tooltips, the Posting Yields chart label that follows the cursor (nothing to read
inside), and the Combos "shares …" CSS popover (it sits flush on its chip).

**Navigation:** there is no sidebar. One sticky top bar (like `shell.html`'s header) holds the brand,
every page as a pill tab (a `?page=` link, so reloads and shared links keep the page and theme), the
Light/Dark switch, contact and the owner card. The tab track scrolls left ↔ right (`top_nav.js`); below
1340px the tabs get their own full-width row. Page sidebars sit just below the bar.
A plain click on a tab does **not** reload the browser: it presses that page's hidden button
(`pgnav_<n>`), so Streamlit reruns in place. The clicked tab lights up at once, the current page dims
while the next one is built, hides when its frame is swapped, then fades + rises in once it has drawn
(`EMBED_FIX` → `__dashReveal`). Ctrl/middle-click still opens the `?page=` link in a new tab.

**Embedding details:** Streamlit shows each page in a component iframe stretched to the page's
full height (EMBED_FIX), so the Streamlit page scrolls, not the page — `page_sidebar.js` detects
this and pins / scroll-spies against the parent. `welcome_screen.js` runs in a zero-height
component and draws into the Streamlit page (same origin).

**Stale copies (not used by the dashboard; kept for the owner to decide):**
- `shell_preview.html` — the design preview; its look now lives in `streamlit_app.py`.
- `export/self_made_combos_bundle/` (+ `.zip`) — a portable snapshot from 2026-09-10; 9 of its
  files differ from the live ones (`self_made_combos.py/.html`, `offer_data.py`, `lib/db.py`,
  `google_auth.py`, `requirements.txt`, `README.md`, `.env.example`,
  `docs/self-made-combos.md`).
- `report_2026_july.html`, `report_2026_august.html` — frozen monthly reports; History
  (Supabase) is the live archive.

## The menus (sidebar order)

The live order and labels are in `dashboard_pages.json` (12 pages — also Offer Picking and
Reject Sale); this table is the per-menu spec index.

| # | Menu | Doc | Generator | HTML |
|---|------|-----|-----------|------|
| 1 | Current Performance | [current-performance.md](current-performance.md) | `current_performance.py` (+ `weekly_sales.py`, `monthly_sales.py`, `forward_projections.py`) | `current_performance.html` |
| 1a | Product Performance (top bags / categories / colours by share · Bag of the Week + why it moved) | [product-performance.md](product-performance.md) | `product_performance.py` (reads `bags_offer_source_<month>.json`, `bag_posts_history.json`) | `product_performance.html` |
| 2 | New Products Analytics | [new-products.md](new-products.md) | `new_products.py` | `new_products.html` |
| 3 | Timed Offers Analytics | [timed-offers.md](timed-offers.md) | `timed_offers.py` | `timed_offers.html` |
| 4 | Self made combos vs running combos | [self-made-combos.md](self-made-combos.md) | `self_made_combos.py` (+ `offer_data.py`) | `self_made_combos.html` |
| 5 | Bags on offer vs not on offer | [bags-on-offer.md](bags-on-offer.md) | `bags_on_offer.py` (reads `bags_offer_source.json` from `self_made_combos.py`) | `bags_on_offer.html` |
| 5a | Shop Stock Levels (min / max per shop · stocks report · next-month preparedness · OOS leads) | [shop-stock-levels.md](shop-stock-levels.md) | `shop_stock_levels.py` | `shop_stock_levels.html` |
| 6 | Posting – Sales Yields from Accurate Posting | [posting-yields.md](posting-yields.md) | `posting_yields.py` | `posting_yields.html` |
| 7 | Shops Efficiency Tracking | [shops-efficiency.md](shops-efficiency.md) | `shops_dispatch.py` → `shops_efficiency.py` | `shops_efficiency.html` |
| 7a | Shop Launch (a new shop from its first sale · Nyeri, Oct 2026) | [shop-launch.md](shop-launch.md) | `shop_launch.py` (config `shop_launch_config.json`) | `shop_launch.html` |
| 7b | Push Planner (what to push, where, why bags aren't moving · Laya second opinion) | [push-planner.md](push-planner.md) | `push_planner.py` | `push_planner.html` |
| — | ~~Dashboard Insights~~ (menu removed Oct 2026; `generate_insights.py` kept, not run) | [dashboard-insights.md](dashboard-insights.md) | `generate_insights.py` | `insights.html` |
| 9 | Monthly Report | [monthly-report.md](monthly-report.md) | `monthly_report.py` | `monthly_report.html` |
| 10 | Reporting History (Supabase) | [reporting-history.md](reporting-history.md) | `push_to_supabase.py` → `history.py` | `history.html` |

**Cross-cutting reference:** [product-matching.md](product-matching.md) — how a sheet name
is matched to its Odoo product(s). Read this first for any "shows 0 but I know it sold" bug.

**Editable data:** [shop-regions.md](shop-regions.md) — the Shop → Region table the
dashboard reads at build time (drives the per-shop combo-button red/green chips). Edit the
table there to change a shop's region; no code change needed.

## Run order (`main.py` / `build_all.py`)

Pages that only re-read data already injected into other pages (Insights, Monthly
Report, History) **must run last**. The ordered list:

1. `weekly_sales.py`, `monthly_sales.py` (Postgres → sheet-backed figures)
2. `current_performance.py`, `forward_projections.py`
3. `new_products.py`
4. `timed_offers.py`
5. `self_made_combos.py` → `bags_on_offer.py`
5a. `shop_stock_levels.py`
6. `posting_yields.py`
7. `shops_dispatch.py` → `shops_efficiency.py`
7c. `bag_signals.py` → `product_performance.py` (reads Self-made Combos' offer source + Bag Signals' posts history)
8. ~~`generate_insights.py`~~ — not run any more (Insights menu removed Oct 2026)
9. `monthly_report.py` (reads the pages above)
10. `push_to_supabase.py` → `history.py`

Regenerate everything headlessly: `python scripts/build_all.py`
Regenerate one page: `python generators/<generator>.py` (set `DENRI_LAUNCHER=1` to suppress the
browser tab).

## Custom range (Oct 2026)

Pages whose **Period** dropdowns can take any From – To window get a **Custom** period. Each page keeps
**its own** range (picking one on New Products doesn't change Posting Yields):

| Page | Range file | Custom covers |
|---|---|---|
| Bags On vs Off Offer | `boo_custom_range.json` | the whole page ([bags-on-offer.md](bags-on-offer.md#period-selector-monthly--weekly--last-week--custom)) |
| New Products | `np_custom_range.json` | Sales by Shop, Sold vs Target, Top 10, Colour Movement ([new-products.md](new-products.md#custom-range-oct-2026)) |
| Posting Yields | `py_custom_range.json` | Posting yield + Dead Stock Clearance, **sales & stock only** ([posting-yields.md](posting-yields.md#custom-range-oct-2026)) |

- **Sidebar panel:** a **Custom range** panel sits right under the page sidebar's **↑ Back to top**
  (`custom_range.js` mounts it into `page_sidebar.js`'s aside) on every page with a Custom period — always
  visible on wide screens, showing **In use: dd Mon – dd Mon** (or "Not set"), From / To, quick picks and
  **Apply / Clear**. Hidden on phones (≤ 980 px, where the sidebar is a top strip) — use the dropdown there.
- **Also in the page's own Period dropdown** (`custom_range.js`, Oct 2026 — the separate date bar above
  the page is gone): every Period dropdown has **Custom range…** (**Change range…** once one is set). It
  opens a From / To picker with quick picks (last 7 / 30 days, last month, this month) and **Apply / Clear /
  Cancel**. Apply reloads the app with `?page=<label>&crange=<key>:<from>:<to>` (Clear: `<key>:clear`;
  keys `boo` / `np` / `py`); `streamlit_app.py` (`CUSTOM_RANGE_KEYS`) writes the page's range file, rebuilds
  the page from Odoo in the background (the previous build stays up with a progress bar; see
  *Refreshing*), drops `crange` from the URL and swaps the new page in when it's ready — its
  dropdowns then show **Custom (dd Mon – dd Mon)**. The range stays (auto-refresh keeps rebuilding it) until
  **Clear**. The page frame's sandbox can't navigate the app itself, so the picker schedules the navigation
  on the (same-origin) app window. Opened as a plain file, the picker shows the command to run instead.
  Tested end to end 6 Oct 2026 (Apply 08–14 Sep and Clear on New Products in a local app).
- **Locally:** `python generators/new_products.py 2026-09-01 2026-09-30` sets it, `python generators/new_products.py clear`
  drops it (same for the Posting Yields script). Helper: `lib/custom_range.py` (`load / save / block`,
  up to 366 days, a future To date is pulled back to today).
- **Posts:** marketing posts exist only as monthly / weekly sheet totals, so a custom range never has a
  post count — posts, expected sales and yields show "—".
- **Targets** for a range = the monthly target × the months the range covers (each day = 1 ÷ days in
  its month: 01–30 Sep = 1.0, 01–15 Sep = 0.5) — `custom.months` in the page data.
- Out-of-stock call-backs take the same window (`oos_callbacks.aggregate(..., custom=(from, to))`).

## Shared conventions

- **Month scope:** the live month comes from `lib/report_month.py`
  (`live_month_window()` = first→last day of the current month; today 2026-09 →
  `2026-09-01`…`2026-09-30`). All "this month" Odoo queries bind
  `date_order::date BETWEEN :start_date AND :end_date`. Sheet readers that carry a
  Month column filter on the current month name.
- **Market split:** Kenya = every POS till except `sinza`, `dar-es-alam`, `uganda`.
  "Outside" = those three (Sinza & Dar → the Sinza region; Uganda → Uganda).
- **Odoo stock codes:** real sellable stock lives in shop-code stock locations
  (`split_part(complete_name,'/',1)`); `WIP`/`WRKWH`/`PURCH`/`PREWH`/`ASSWH`/`CORP`/
  `VLD`/etc. are production/holding and carry a bogus ~44,444/variant placeholder —
  **never count them**. Kenya shops: STAR, MSA, NAKS, ELD, KSM, MERU, THK, HAZ,
  KITE, NAN, KAK, HTN, KSI, KTDA, BUSIA, RONG. Sinza → DAR, Uganda → UG.
- **Python:** `C:\ProgramData\anaconda3\python.exe`. Sheets auth via
  `google_auth.py`. DB via `lib/db.py` (Supabase **session pooler** host — the direct
  host is IPv6-only). Never commit/print `.env`.
- **Verifying HTML JS:** the reusable `domharness.js` shim (in the session scratchpad)
  evals every `<script>` block and fires `DOMContentLoaded` to catch load-time errors;
  `node --check` on an extracted block catches syntax errors.
</content>
</invoke>
