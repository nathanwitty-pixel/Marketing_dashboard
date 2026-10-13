# Ralph task — Sinza & Uganda in Bags On vs Off Offer

Repo `c:\Users\jonat\Desktop\Marketing_dashboard`. Orient with graphify first (`graphify query "<q>"`,
`graphify explain "<symbol>"`); read raw files only to edit/debug specific lines. Spec first: change
`docs/bags-on-offer.md` before code. Log each finished step (date, what, verification output) under
"## Progress" at the bottom of THIS file. Never commit, push or run publish.bat. Rebuilding pages from Odoo is fine.

## The rules (fixed — user, 8 Oct 2026; Kenya already follows them, do not change Kenya)
On offer = **combo sales + the market's deal singles** only. A combo bag bought on its own and timed-offer sales
are **not on offer**. For Sinza (tills `sinza`, `dar-es-alam`, TSh) and Uganda (till `uganda`, USh) there is no
Power Deal / Deal of the Week; the deals are the market's **listed singles** in `offers_monthly.csv`. So, from the
till receipts (`lib/receipt_combos.py`: refunds dropped; 5+ bags = bulk; same-price bags = a combo; leftover 2+ bags
= a combo; 1 bag = a single; combo that fits a listed combo = running, else self-made):
- **On offer** = every combo (running + self-made) + single sales of a bag that is on that market's listed singles.
- **Not on offer** = every other single sale (incl. a listed-combo bag bought alone).
- **Others** = bulk receipts (5+ bags), reported apart.
- Money in the market's currency with KSh in brackets (`FX_PER_KSH`: 25 TSh = 1 KSh, 35 USh = 1 KSh).

## Steps (do in order; after each, run its VERIFY; if it fails, fix before moving on)
1. **Spec.** Add a "## Sinza & Uganda" section to `docs/bags-on-offer.md` with the rules above, the data shape
   (`BOO.markets[m].periods[p]` = same keys as Kenya's period where they apply: totals {on, off, oth}, sources,
   onBags, offBags) and the market switch. VERIFY: `grep -n "## Sinza & Uganda" docs/bags-on-offer.md`.
2. **Library.** In `lib/receipt_combos.py` add `offer_split(lines, offers, infer)` (pure function, reuses the
   receipt grouping in `classify`) returning per window: `combos {running:{count,bags,revenue}, selfMade:{…}}`,
   `onSingles {bag: {units, revenue}}`, `offSingles {bag: {units, revenue}}`, `bulk {receipts, bags, revenue}`,
   `comboBags {bag: units}` (bags inside self-made combos; running combos counted by combo only). Add tests to
   `tests/test_receipt_combos.py` (listed single → on; combo bag alone → off; same-price pair → combo on; bulk →
   oth; refund dropped). VERIFY: run every test function in that file with a plain Python runner (pytest is not
   installed: import the module with a stub `pytest`, call each `test_*`), 0 failures.
3. **Generator.** In `bags_on_offer.py` build `BOO.markets = {sinza: {...}, uganda: {...}}`, each with the same
   period windows as Kenya (monthly, weekly, lastweek, custom when set), currency and `fx`. VERIFY: rebuild
   (`DENRI_LAUNCHER=1 python self_made_combos.py` then `python bags_on_offer.py`, exit 0) and a reconciliation
   script: for each market and the monthly window, on bags + off bags + bulk bags == the receipts' total bags from
   `receipt_combos.market_summary` (exact), and on + off + oth revenue == receipts revenue.
4. **Page.** In `bags_on_offer.html` add a market switch (Kenya | Sinza | Uganda, Kenya default, remembered in
   localStorage with try/catch). For Sinza / Uganda show: KPI cards (on / not on / others, money + bags + share),
   "Where the on-offer money comes from" (Running combos · Self-made combos · Listed singles), and the on / not-on
   bag tables (bag, units, money, in self-made combos). Kenya rendering must not change. VERIFY: every inline
   script passes `node --check`; headless Edge (`msedge --headless=new --dump-dom` with an injected test script)
   shows the three markets' KPI text and no JS errors.
5. **Finish.** `graphify update .`; Streamlit AppTest on page "Bags On vs Off Offer" with no exceptions; summary
   of the monthly numbers per market in the Progress log. VERIFY: AppTest prints `exceptions: []`.

If stuck on the same error for 3 consecutive iterations, output `<promise>STUCK ON <problem></promise>` and stop.
Done (all 5 VERIFY steps passed and logged) → output `<promise>BOO MARKETS DONE</promise>`.

## Progress
- 2026-10-08 Step 1 done: "## Sinza & Uganda (Oct 2026)" spec added to docs/bags-on-offer.md (rules, market switch, data shape). VERIFY: grep → line 346.
- 2026-10-08 Step 2 done: lib/receipt_combos.py — shared _receipts/_groups (classify unchanged), new offer_split() + market_lines(); 3 new tests. VERIFY: 14 tests, 0 failures (plain runner, pytest not installed).
- 2026-10-08 Step 3 done: bags_on_offer._market_periods() → BOO.markets {sinza, uganda} × monthly/weekly/lastweek/custom. VERIFY: rebuild exit 0; monthly reconciliation exact — Sinza 86 bags / TSh 4,115,480, Uganda 47 bags / USh 3,459,300 (on+off+bulk = receipts).
- 2026-10-08 Step 4 done: market switch (Kenya | Sinza | Uganda, remembered) + #boo-mkt-view (KPIs, money sources, on/off tables, TSh/USh + KSh). VERIFY: all inline scripts pass node --check; headless Edge shows Sinza on TSh 3,952,980 (96.1%), Uganda on USh 1,950,300 (56.4%), Kenya unchanged, JS errors: none.
- 2026-10-08 Step 5 done: graphify update . (code graph updated); AppTest page 'Bags On vs Off Offer' → exceptions: []. Monthly (Oct 1–8): Sinza on 82 bags / TSh 3,952,980 (13 running + 24 self-made combos + 2 listed singles), not on 4 / TSh 162,500, bulk 0; Uganda on 28 / USh 1,950,300 (14 self-made combos; Uganda list has no running sales yet), not on 7 / USh 669,000, bulk 12 bags / USh 840,000.
