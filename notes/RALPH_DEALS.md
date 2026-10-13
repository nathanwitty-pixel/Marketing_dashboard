# Ralph task — deals from the posters (deals_kenya.csv)

Repo: `c:\Users\jonat\Desktop\Marketing_dashboard`. From October 2026 the Deals of the Week (and Power
Deals) come from the **poster images** the user sends, transcribed into `deals_kenya.csv` — not the
Google deals sheet. Log progress in `OOS_PROGRESS.md` (section "Deals from posters"). Orient with
`graphify query` / `graphify explain self_made_combos_read_deals` first. Never commit, push or run publish.bat.

## Facts
- `deals_kenya.csv` = the deals-sheet columns (Tier, Month, Product, Location, Type, Original, Current,
  Discount) + `Poster name` (as printed) + `Poster` (which poster). **Product = the Odoo root name**
  (poster "Fayola messenger" → `Fayola`, "Briefcase" → `Brief Case`, "College handbag" → `College HB`,
  "Doublepress backpack" → `Double Press`, "Neo man bag" → `Neo Man`, Power "Standard" → `Standard Travel`).
- Poster rules: crossed-out price = **Original** (full price), the price beside it = **Current**;
  location = the shop after "Only available at"; "Nairobi Town stores" = Starmall + Hazina + Hilton + KTDA.
- Tier 1 = weeks 1–2, Tier 2 = week 3+ (docs/self-made-combos.md).
- `_read_deals(month)` is the only reader; it feeds SMC.deals → bags_offer_source.json → Bags on Offer,
  combos_by_shop.json → Shops Efficiency, and the Push Planner.

## Steps (verify each before the next)
1. **CSV** — 112 rows: 102 Tier-1 DoW rows (17 locations × 6) + 10 Power Deals, every Product resolving
   to Odoo products. VERIFY: script counts rows/locations and checks each Product prefix-matches ≥ 1
   active Odoo template.
2. **Docs** — docs/self-made-combos.md: deals source order (CSV rows for the month win over the sheet;
   sheet; then COMBOS-sheet Power Deals fallback) + poster transcription rules. VERIFY: grep.
3. **Code** — `_read_deals` reads the CSV month rows first. VERIFY: tests/test_deals_csv.py passes
   (October from CSV: 10 power, DoW products dedup'd with all locations, prices/discounts kept;
   a month not in the CSV falls back to the sheet path).
4. **Rebuild** — self_made_combos.py, bags_on_offer.py, shops_efficiency.py, push_planner.py exit 0;
   SMC.deals has 10 Power Deals + Tier-1 DoW with sold/stock; Bags on Offer builds (not "unchanged").
5. **Finish** — pytest all, AppTest the pages, `graphify update .`, summary in OOS_PROGRESS.md.

Done → `<promise>DEALS_FROM_POSTERS_DONE</promise>`. Stuck 3× on one error → note it and delete
`.claude/ralph-loop.local.md`.
