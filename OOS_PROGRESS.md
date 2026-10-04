# OOS call-back progress (Ralph loop log)

Task: see `RALPH_TASK.md`. Update this file at the end of every iteration.

| # | Sub-goal | Status | Verified |
|---|---|---|---|
| 1 | Docs | done | grep lists all 3 docs |
| 2 | Module + tests | done | pytest 9 passed (Anaconda python — Python314 has no pytest) |
| 3 | New Products | done | build exit 0; NP.oos has 5 periods (0 people — no OOS asks for current new products) |
| 4 | Combos | done | build exit 0; SMC.oos kenya/sinza/uganda; 73 chips render (headless Chrome) |
| 5 | Bags on Offer | done | build exit 0 (Oct 2026); BOO.oos 5 periods; Call-backs column renders |
| 6 | Chip UX | done | node --check all scripts; harness: tap opens/outside closes/fits 375px/0 hidden; AppTest 3 pages no exceptions |
| 7 | Offline | done | exit codes NP 0 · SMC 0 · BOO 0 (SMC/BOO leave pages unchanged; NP uses sheet + cached OOS copy); pages restored |
| 8 | Finish | done | pytest 49 passed; graphify update run |

## Blocker counter

(none)

## Log

- 2026-10-04: worked directly (plugin not loaded in the session). Shared UI in `oos_chip.js` (chip, popover, toggle),
  included next to chart_switcher.js; v5_theme.js remaps its dark palette for light mode.
  New Products: strip under 'Sold vs Remaining to Target', follows #pt-period + 'Waiting now'.
  Run generators with PYTHONIOENCODING=utf-8 (pre-existing cp1252 print crash otherwise).

- Mid-task requests (user): (a) month must follow the live month — 'Sept Combos' card label was hardcoded → now
  offerKpis.comboMonth from the sheet header (OCTOBER COMBOS → 'Oct Combos'); '<MONTH> COMBOS' header skip made generic;
  deals sheet has no October rows yet → Power Deals fall back to the COMBOS sheet's POWER DEALS list (_deals_from_offer_sheet),
  which also unblocks Bags on Offer. (b) running combos: closest Odoo name — _matches_sheet now matches slots in any order,
  bare 'Travel' = Standard, and a closest-name fallback (_opt_close: spaces/word-prefix/≥85% spelling; 'MINI' etc too vague).
  Oct check: 56 → 87 Odoo combo names matched, none of the 56 changed; Amaya+Avana / Jumbo+Prime / Reo Travel+Code 3 stay self-made.

## Final summary

Files: sql/oos_callbacks.sql, lib/oos_callbacks.py, tests/test_oos_callbacks.py, oos_chip.js (new);
new_products.py/.html, self_made_combos.py/.html, bags_on_offer.py/.html, docs/new-products.md,
docs/self-made-combos.md, docs/bags-on-offer.md (changed).

Top 5 most-requested bags (lifetime, Kenya, distinct people): MINI MAYA 70 (Ktda 24 · Website 9 · Eldoret 8) ·
NIZANA 15 (Eldoret 4 · Kisii 3 · Website 3) · LOLA 13 (Kisumu 3 · Website 3) · ZANE MAN 11 (Mombasa 3 · Eldoret 2) ·
KAI 11 (Ktda 3 · Mombasa 3 · Kisumu 2).

Unmatched requested names (no catalogue bag; 35 products): mostly non-bags — DRAWER REPAIR, China Material…, flour,
CANDLE, machines, samples — plus a few real bags missing from bag_original_prices.json: Sarina Black, Venus Black,
Safiri 2 Travel, Safarilink Travel, Old Messenger, ankara jumbo, LCG Bag. Asked-for bags not in the Bags on Offer
tables this month (no sales): CLEO, ELLA SLING, MAYA, MONTANA, TWAIN TRAVEL. New Products: 0 asks for the 9 current new products.

## Deals from posters (RALPH_DEALS.md) — 2026-10-04

| # | Step | Status | Verified |
|---|---|---|---|
| 1 | CSV | done | 112 rows: 102 Tier-1 DoW (17 locations × 6) + 10 Power; every Product prefix-matches Odoo |
| 2 | Docs | done | docs/self-made-combos.md › Deals from the posters |
| 3 | Code | done | `_local_deal_rows` + `_read_deals`; tests/test_deals_csv.py 2 passed |
| 4 | Rebuild | done | 4 generators exit 0; SMC.deals 10 Power + 31 DoW bags / 17 locations from the CSV; BOO built for Oct |
| 5 | Finish | done | pytest all; AppTest 4 pages; graphify update |

## Sinza & Uganda (RALPH_OUTSIDE.md) — 2026-10-04

| # | Step | Status | Verified |
|---|---|---|---|
| 1 | CSV | done | offers_outside.csv: Sinza 10 singles + 10 combos, Uganda 5 + 5; every bag type in the catalogue |
| 2 | Docs | done | docs/self-made-combos.md › Sinza & Uganda — combos counted from receipts |
| 3 | Code | done | lib/receipt_combos.py; tests/test_receipt_combos.py 6 passed |
| 4 | Page | done | region cards from the CSV + till-counted weeks; Self-made panel renders (Sinza: 8 running, 15 self-made) |
| 5 | Finish | done | pytest all; AppTest; graphify update |
