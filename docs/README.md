# Dashboard Menu Docs

One file per menu in the Denri / Bagware Marketing Dashboard. **These are the spec.**
When a page needs changing, correct the relevant `.md` here first, then make the code
match it.

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

## How the dashboard is built

Each menu is a **static HTML page** with a hand-written render layer (JS + CSS). A
**Python generator** fetches live data (Google Sheets and/or the Odoo Postgres
read-replica), serialises it to a JS object, and injects it into the HTML **between
comment markers** — it replaces only the data block, never the render code. So:

- Editing **layout / charts / wording** → edit the `.html` render layer directly.
- Editing **what data is pulled / how it's computed** → edit the `.py` generator.
- The markers (e.g. `<!-- SMC_DATA_START -->…<!-- SMC_DATA_END -->`) must stay intact.

`shell.html` is the frame (sidebar nav) that loads each page into an iframe.
`build_all.py` re-bakes every page headlessly (no server, no browser tab).

## The menus (sidebar order)

| # | Menu | Doc | Generator | HTML |
|---|------|-----|-----------|------|
| 1 | Current Performance | [current-performance.md](current-performance.md) | `current_performance.py` (+ `weekly_sales.py`, `monthly_sales.py`, `forward_projections.py`) | `current_performance.html` |
| 2 | New Products Analytics | [new-products.md](new-products.md) | `new_products.py` | `new_products.html` |
| 3 | Timed Offers Analytics | [timed-offers.md](timed-offers.md) | `timed_offers.py` | `timed_offers.html` |
| 4 | Self made combos vs running combos | [self-made-combos.md](self-made-combos.md) | `self_made_combos.py` (+ `offer_data.py`) | `self_made_combos.html` |
| 5 | Bags on offer vs not on offer | [bags-on-offer.md](bags-on-offer.md) | `bags_on_offer.py` (reads `bags_offer_source.json` from `self_made_combos.py`) | `bags_on_offer.html` |
| 6 | Posting – Sales Yields from Accurate Posting | [posting-yields.md](posting-yields.md) | `POSTING (SALES YIELDS FROM ACCURATE POSTING).py` | `POSTING (SALES YIELDS FROM ACCURATE POSTING).html` |
| 7 | Shops Efficiency Tracking | [shops-efficiency.md](shops-efficiency.md) | `shops_dispatch.py` → `shops_efficiency.py` | `shops_efficiency.html` |
| 8 | Dashboard Insights | [dashboard-insights.md](dashboard-insights.md) | `generate_insights.py` | `insights.html` |
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
6. `POSTING (SALES YIELDS FROM ACCURATE POSTING).py`
7. `shops_dispatch.py` → `shops_efficiency.py`
8. `generate_insights.py` (reads the pages above)
9. `monthly_report.py` (reads the pages above)
10. `push_to_supabase.py` → `history.py`

Regenerate everything headlessly: `python build_all.py`
Regenerate one page: `python <generator>.py` (set `DENRI_LAUNCHER=1` to suppress the
browser tab).

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
