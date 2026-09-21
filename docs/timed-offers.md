# Timed Offers Analytics

- **Generator:** `timed_offers.py`
- **HTML:** `timed_offers.html`
- **Data marker:** `<!-- TIMED_DATA_START -->…<!-- TIMED_DATA_END -->` — injects
  `const TO_DATA = {"month", "offers":[…]}`, then `const TO_LIST = TO_DATA.offers` and
  `const TO = TO_LIST[0]` (back-compat).
- **Config:** `timed_offers_config.json`

## What the page shows

**Every** timed-offer **campaign** running in the month, **stacked** on one page (Kenya):
each shows per-bag sales over that campaign's exact date window, alongside the marketing
posting that ran with it. One `<template id="to-offer-tpl">` is cloned per offer and filled
by `renderOffer(TO, root)` (data hooks are `data-el="…"`, scoped to each offer's clone, so
several offers coexist without id clashes).

## Multiple offers & month rollover

- **Add an offer:** append an item to the `offers` list in the config (below). All offers
  in the list run live and stack on the page — you don't remove the old ones by hand.
- **Rollover (automatic, at month end):** `month_end.py` archives the closing month's
  offers to Supabase (via `monthly_report.py._read_timed_offers()` → `timedOffers` in
  `monthly_report_history.json` → `push_to_supabase.py` → `denri_mkt_timed_offer*` tables),
  then **clears** the config (`offers: []`, `month` bumped to the new month) so the timed
  offers start free. The clear only fires on a real unpinned 1st-of-month run and only after
  every archive step succeeds — `timed_offers.py` itself never archives or clears (it runs
  on every refresh/snapshot and must not race the archive).

## Data sources

- **Sales:** LIVE from Odoo POS for the **exact** `startDate…endDate` (end-of-day
  inclusive), Kenya market (every till except Sinza/Dar/Uganda), per bag type. Excludes
  combo wrappers / delivery / customisation / straps / samples / POS-category lines (same
  rules as the Total Sales figure).
- **Posting:** last week's Kenya marketing posting (WEEKLY_MARKETING_POST col E) per bag
  type, borrowed alongside the sales.
- **Config** (`timed_offers_config.json`): `{"month": "YYYY-MM", "offers": [offer, …]}`.
  Each **offer**: `name`, `market`, `shops[]` (limit sales to those POS tills — e.g. Nairobi
  CBD = Hazina/Hilton/Starmall/KTDA Shop; empty = whole market), `startDate`, `endDate`,
  `bags[]` (default Kai, Pioneer, Double Press, Antitheft, Code 3, School bag), `prices{}`
  (`{BAG: {was, now}}` — config prices win over Odoo's pricelist for a manual cut like "300
  off"). A legacy single-offer file (top-level `name`/`bags`/`startDate`) is still read and
  auto-wrapped into a one-item `offers` list.
- **`bagsFrom`** (optional, per offer): a repo CSV filename whose **`BAG TYPE`** column supplies
  the bag list, overriding inline `bags[]`. Keeps a tracker in sync with that list instead of
  hand-copying it. Used by the **Kitengela Rejects** campaign → `reject_stock.csv` (all reject
  bag types), so editing the reject stock updates the tracker automatically.
- **`stockFrom`** (optional, per offer): source the **In-stock** figure from a repo CSV's
  **`UNITS`** column (summed per `BAG TYPE`) instead of live Odoo on-hand — the Kitengela tracker
  uses `reject_stock.csv`, so In-stock = the physical reject pile (599 units), not Odoo's Kenya
  on-hand of those bag types. `kenya_stock_by_bag` reads `CFG["stockFrom"]`.
- **`nameLike`** (optional, per offer): a product-name substring filter (`ILIKE '%…%'`) applied
  to every sales query via `_name_sql` → `_NAME_SQL`. The **exact** way to isolate a tagged
  range — the Kitengela rejects are distinct Odoo products with **`[REJECT]`** in the name, so
  `nameLike: "[REJECT]"` counts precisely those (Postgres LIKE treats only `%`/`_` as special, so
  `[ ]` are literal).
- **`minPrice` / `maxPrice`** (optional, per offer): a unit-price band (`pl.price_unit`) via
  `_price_sql` → `_PRICE_SQL`. A cruder isolation than `nameLike` (superseded for Kitengela once
  the `[REJECT]` tag was found), still available for price-banded offers.

## Kitengela Rejects tracker

Tracks the **Kitengela reject clearance** as a timed offer: `shops: ["KITENGELA"]` (the Kitengela
POS till — the dormant "REJECTS" till is unused), **`nameLike: "[REJECT]"`** (the rejects are
distinct Odoo products tagged `[REJECT]` in the name — the exact filter; **166 net units** in Sept
(175 gross − 9 refunds/returns; see the net note below), all
at KITENGELA, bucketed to ~163 in the per-bag table), `bagsFrom: reject_stock.csv` (bag universe
for the per-bag breakdown), the month window, **`stockFrom: reject_stock.csv`** (In-stock = the
physical reject pile, 599 units, not Odoo on-hand), and **no fixed prices** (`prices: {}`). An
earlier `maxPrice: 1600` price-band proxy was replaced by the precise `[REJECT]` name filter.

**Performance:** the per-bag SQL fetches all bag products in scope and **buckets in Python**
(`_bucket`) instead of OR-ing 60–70+ `ILIKE` patterns (~3× faster on a month of Kenya sales), and
respects the offer's shop/price/name scope. The Streamlit refresh subprocess budget was raised to
**`SCRIPT_TIMEOUT = 600s`** (from 240s) in `streamlit_app.py` for the Odoo-heavy chain.

**TTL disk-cache (`lib/db.run_query_cached`).** The slow Odoo lookups are cached to disk
(`.odoo_cache/`, gitignored) keyed by exact SQL+params: POS sales scans at `ODOO_CACHE_MIN`
(30 min), the per-bag list/pricelist metadata loops at `META_CACHE_MIN` (12 h, since they were
77 round-trips of near-static data). A **manual Refresh** sets `DENRI_FORCE_FRESH=1` (via
`run_scripts(..., force_fresh=True)`) to bypass the read and repopulate; auto-refresh/page-load
reuse the cache within TTL; if Odoo is unreachable a stale cached copy is returned. Measured:
cold ~251s → warm ~62s. Reusable for any generator's slow query — swap `run_query` →
`run_query_cached(sql, params, ttl_min=…)`.

**"Why these bags?" table — reject-only + totals.** The per-bag table (Bag · Sold · In stock ·
Price was · Price now · Discount · Sales lift · Category) drops zero rows (so for the Kitengela
offer only the reject bags with sales/stock show). The **TOTAL row is pinned on top** (in a sticky
`thead`, above the column header) carrying a **hover** — units sold, stock remaining, **% of the
clearance sold** (`sold ÷ (sold+stock)`), revenue was→now, and discount given. Revenue-now is
capped at was per bag so a stray pricelist value can't inflate the total. The body **scrolls**
(`.why-scroll`, ~first 10 rows visible) while the TOTAL and header stay fixed. A **Sort** control
above the table re-orders the rows client-side (Sold / In stock / Discount, largest↔smallest); the
catch-all **Other rejects** row always sinks to the bottom.

**"Other rejects" catch-all (accurate totals).** `_bucket` maps an Odoo product to a listed bag by
longest-prefix, so a `[REJECT]` unit whose product name doesn't match a listed reject bag —
colour/condition or plural/variant spellings (**Moon Bag …** vs the sheet's **Moon Bags**, **Mega
…** vs **Mega Bagpack**, **Standard Travel …** vs **Travel**) — used to be silently dropped,
under-counting the reject total (165 shown vs the true count in Sept). Those unbucketed matches
are now collected under a single **`Other rejects`** row (`_OTHER_REJECTS`), added only when a
`nameLike` filter is active, so the headline **TOTAL sold** and the table both equal every reject
sold. The row is flagged `isOther` (italic, with a hover explaining it) and carries no
price/stock (category "Other / variant names"). To itemise those units, align the Odoo product
name or `reject_stock.csv`'s `BAG TYPE` spelling.

**Net of refunds — matches Current Performance.** The reject tracker's queries use `pl.qty <> 0`
(via `_QTY_SQL`, set in `build_offer` only when `nameLike` is present) so refunds/returns net out —
Sept is **175 gross − 9 reject refunds = 166 net**. This matches the Monthly Sales /
Current-Performance reject figure (166, `reject_bags_sold.sql` also uses `qty <> 0`), whose Sales
total is likewise net, so "166 rejects of 10,594" is a true subset. A normal campaign (no
`nameLike`) keeps the gross `pl.qty > 0`.

**In-stock is reject-only.** The In-stock column comes from `stockFrom: reject_stock.csv`
(`_stock_from_file`, summed per `BAG TYPE` = 599 units) — the physical reject pile, never Odoo's
Kitengela on-hand of all bag types.

**Per-variant table + Colour/Category/Product/Bag Type filter.** For a name-filtered offer
(`nameLike`, i.e. the reject tracker) `reject_variants()` emits `why.variants` — one row per Odoo
`[REJECT]` **product** (Product · Colour · Bag Type · Sold · In stock · Price was · Price now ·
Discount · Category). Sold and realised price come live from Odoo; stock is merged from
`reject_stock.csv` per (bag, colour); colour is parsed via a primary-colour vocabulary and bag via
singular-token matching (best-effort, but the totals still sum to the true **166 net sold / 599
stock**). Stock-only variants (in the pile, nothing sold in the window) are appended. The table
renders these rows behind a **`DenriTableFilter`** bar (Colour / Category / Product / Bag Type);
the pinned TOTAL row and % cleared **recompute on every filter**, and the Sort control orders the
filtered rows. The two CBD offers (no `nameLike`) keep the per-bag table and hide the filter bar.

**Reusable filter widget (`window.DenriTableFilter`).** A self-contained script (defined once at
the top of the `<script>` region, injects its own `.dtf-bar` CSS): `DenriTableFilter.attach({bar,
rows, dims, onChange})` populates a dropdown per dim from the rows' unique values (skipping a dim
with no data), and calls `onChange(filteredRows)` on every change/reset. Drop-in for any page's
table — the same component is used across the dashboard's tables.

It reuses the same per-bag sales + posting view as every
other offer. Because it has no configured price cuts, the page shows the **neutral "Tracking
live" verdict** (not the back-to-school narrative — that only fires when every bag has a real
cut), and the **lift** reads `n/a` when the window starts on the 1st (no pre-offer days). The
scope label is no longer hardcoded "Nairobi CBD": it shows that only for the CBD shop set,
otherwise `market · shops` (e.g. `Kenya · KITENGELA`) or just the market.

## Clearance start split + clearance-rate chart (Kitengela)

- **`clearanceStart`** (optional, per offer): the day a clearance actually began when it's partway
  through the window (the window may span the whole month for counting every unit). The **"Did the
  offer lift sales?"** panel then splits **before vs during at that date** — e.g. Kitengela
  `clearanceStart: "2026-09-18"` compares Sep 1–17 (before, ~0/day) against the clearance days
  (Sep 18→). The "during" per-day divides by **elapsed** days only (`_oe_eff = min(endDate,
  today)`), so a still-running window isn't diluted across future days (fixed a case showing
  12.1/day that should read ~39/day). Empty = split at the offer start as before.
- **Clearance-rate chart** (`clearance-panel`, reject offers only): a horizontal bar chart of
  **% cleared = sold ÷ (sold + stock)** per group, with a **Bag type ↔ Category** toggle
  (`clearance-mode`). Bag type aggregates all colours (e.g. every Prime colour as one). Built
  client-side from `why.variants`; bars are colour-coded green ≥80 / amber ≥50 / red below.
- **Bags Sold revenue hover**: the Bags-Sold KPI shows a hover with the actual realised revenue
  (`sum(variant.rev)`, incl-tax) — e.g. Kitengela 166 sold → KES 231,500.

## Editing a campaign

Edit `timed_offers_config.json` — add/adjust items in `offers[]` (dates + shops + bag list +
prices) — then regenerate. Each window is literal: set `startDate`/`endDate` to the
campaign's real span. (The inline page control edits **offer[0]**'s shops/window only;
multi-offer editing is done in the file.)

## Regenerate

```
python timed_offers.py            # DENRI_LAUNCHER=1 to skip the browser tab
```
`main.py` also re-runs this daily so it records that day's shop-scoped snapshot.
