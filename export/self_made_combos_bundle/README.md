# Self-made combos vs Running combos — portable bundle

A self-contained copy of the *Self-made combos vs Running combos* analytics page
(generator + static HTML + its dependencies), ready to drop into another project.

It reads **live from Odoo POS (Postgres)** and two **Google Sheets**, classifies every
combo sold this month as **Running** (matches the offer sheet's composition) or
**Self-made** (anything else with a `+` in the name), and injects a JSON payload into
`self_made_combos.html`. It also computes Deal-of-the-Week / Power-Deal enrichment, the
combo-button till check, the monetary implication, and the "bags not on offer" split.

## Contents

```
self_made_combos.py        the generator (build_payload + all SQL + injection)
self_made_combos.html      static page; reads the injected `const SMC = {…}`
offer_data.py              reads the offer sheet (COMBOS / MONTHLY_TARGET / STOCK_LEVELS)
google_auth.py             Google Sheets auth (service account or OAuth desktop)
bag_original_prices.json   full-price catalogue (drives the monetary implication)
lib/db.py                  Postgres access — run_query(sql, params) -> DataFrame
lib/report_month.py        "which month are we reporting?" (live vs pinned)
lib/__init__.py
docs/self-made-combos.md   the full spec for this menu (READ THIS — how every number is built)
docs/shop-regions.md       editable shop → region map (red/green chips) — edit, don't touch code
sql/self_made_vs_running_combos.sql  standalone pure-SQL version of the classification
requirements.txt
.env.example
```

## Setup

1. **Python deps** (Python 3.10+ recommended):
   ```
   pip install -r requirements.txt
   ```
2. **Database**: copy `.env.example` → `.env` and set `DATABASE_URL` to the Odoo POS
   Postgres (read-only is enough). The queries use the standard Odoo POS schema:
   `pos_order`, `pos_order_line`, `pos_session`, `pos_config`, `product_product`,
   `product_template`, `product_category`, `product_combo`, `pos_combo_request`,
   `stock_quant`, `stock_location`. If the DB is unreachable the page still builds from
   the sheet, with combo/deal sales showing 0.
3. **Google Sheets**: add a service-account key as `service_account.json` next to
   `google_auth.py` (or set `SERVICE_ACCOUNT_JSON` in `.env`), then share **both** sheets
   below with the service account's email (Viewer). To use your **own** sheets instead,
   point the two IDs at them and reproduce the tabs/columns:
   - `offer_data.py` → `SPREADSHEET_ID` — the offer sheet. Tabs used: **COMBOS**,
     **MONTHLY_TARGET**, **STOCK_LEVELS**.
   - `self_made_combos.py` → `DEALS_SHEET_ID` — the deals sheet, worksheet **"Kenya"**,
     columns A Tier · B Month · C Product · D Location · E Type · F Original · G Current ·
     H Discount (Type = "Power Deals" or "Deal of the Week").

## Run

```
python self_made_combos.py
# set DENRI_LAUNCHER=1 to skip opening a browser tab
# set DENRI_REPORT_MONTH=YYYY-MM to pin/rebuild a specific month
```

This regenerates `self_made_combos.html` in place (data injected between the
`<!-- SMC_DATA_START -->…<!-- SMC_DATA_END -->` markers) and opens it. To embed the page
in another app, either serve the regenerated HTML file directly, or call
`self_made_combos.build_payload(month_start, month_end)` and render the returned dict
however you like — that function is the whole analytical core and is DB-driven, so it is
correct for a live or a pinned past month.

## Porting notes

- **Classification is composition-based.** The offer sheet is the authoritative list of
  running combos; a combo whose slots match a sheet entry is Running, everything else with
  a `+` is Self-made. `_matches_sheet` / `_build_sheet_slots` do the slot-aware matching
  (split on `+` into slots, `/` or `or` into options, normalise colours/category words).
- **Returns are netted** — every units-sold figure uses `pl.qty <> 0` (returns are
  negative-qty lines, so they subtract). See the "Returns netting" section in
  `docs/self-made-combos.md`.
- **Shop → region map** lives in `docs/shop-regions.md` (loaded at runtime); edit that
  table to change regions or the red/green under-performance chips — no code change.
- **`lib/db.py` mirrors a Streamlit `lib.db`** (same `run_query`/`check_connection`
  surface), so it drops into most Python stacks unchanged.
- No secrets are included in this bundle — supply your own `.env` and Google key.
```
