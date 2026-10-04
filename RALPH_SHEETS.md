# Ralph task — only three sheet tabs left

Goal: the dashboard reads **only** MONTHLY_TARGET, MONTHLY_MARKETING_POST and WEEKLY_MARKETING_POST from
Google Sheets. Everything else comes from the files the user uploads each month or from Odoo.
Orient with graphify (`graphify explain offer_data_fetch_offer_data`, `graphify query`). Log in
OOS_PROGRESS.md › "Sheets cut". Never commit / push / run publish.bat.

## Monthly inputs (user uploads)
- `offers_monthly.csv` — Kenya / Sinza / Uganda combos + singles (was offers_outside.csv; Kenya combos added).
- `deals_kenya.csv` — Kenya Power Deals + Deals of the Week (posters).

## Steps (verify each)
1. CSV — rename to offers_monthly.csv, add October's 10 Kenya combos (the sheet's list, one last copy).
   VERIFY: lib/receipt_combos loads it; Kenya 10 / Sinza 20 / Uganda 10 rows.
2. Docs — README "Where data comes from", self-made-combos, offer-picking, timed-offers. VERIFY grep.
3. offer_data.py — no COMBOS read: Kenya combos / power deals / Sinza & Uganda lists from the two CSVs;
   MONTHLY_TARGET still from the sheet; STOCK_LEVELS from Odoo only.
4. self_made_combos.py — no deals sheet, no COMBOS fallback; "Offer sales vs stock" weekly sales and the
   combo-button "expected" come from Odoo (week_combos by list label), not hand-typed sheet columns.
5. Other readers — lib/odoo_tabs.get_rows: no sheet fallback (empty instead); timed_offers: no
   STOCK_LEVELS fallback; offer_picking: local bom_costs.json + offers_prices.json only.
6. Guard — tests/test_sheet_reads.py scans the live .py files (not export/) and fails on any sheet tab
   other than the three, or any other spreadsheet id.
7. Rebuild all generators (exit 0), pytest, AppTest, `graphify update .`, summary.

Done → `<promise>THREE_TABS_ONLY</promise>`.

## Added mid-task (user)
8. Sinza & Uganda: the Kenya-style "self-made vs running" view (repeating self-made combos, running list,
   units / revenue split) from the till receipts — no Request Hub (CBR) for those markets.
9. Sinza & Uganda money: Kenya shillings in brackets beside TSh / USh everywhere on those views.
