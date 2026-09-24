# Offer Picking (`offer_picking.py` → `offer_picking.html`, `OP`)

A planning menu for **which offers/combos to run**. The page **leads with the Forecast**
(the picked combos ranked for next month), then the picker, power deals and seasonality.

> The **Offer profit ranking** table and the **Profit contribution** bar chart were removed
> from the page (per user request) — the page opens on the Forecast instead. The generator
> still computes `OP.offers` (used for the console summary and available in the payload), it
> is just no longer rendered, so the Chart.js CDN include was dropped too.

1. **Forecast (picked combos)** — see item 4 below; it is now the **first card** on the page.
2. **Next-month picker** — the reference-month combos (`OCT_2025_COMBOS`) matched to
   **current Odoo stock**, laid out as the sheet's **fixed 3-pair grid** (`_next_month` emits
   `grid` = `[[s,s],[s,s],[s,s]]`, pre-filled from each combo). **Every slot is a searchable
   combobox** (`.cbx` — type to filter the catalog; `Zero` = empty; picking fires a bubbling
   `cbxchange`); the title + WAS→NOW price, cost, profit, buildable recompute live. See the
   pricing section below.
3. **Power deal choosing** — **10 editable single-bag slots**. Each slot is a searchable
   combobox over the priced bags, defaulting to the highest-margin ones; it shows **price was
   (full D) → now (offer F)**, cost, margin (on the offer price) and stock, with a combined
   total. `OP.powerDeals`. **Bags used in the combos above are excluded** (a bag is either in
   a combo or a power deal): the list reads the combo grids' current selections
   (`usedInCombos`), filters `OPTSETS.deal`, and **refills reactively** — editing a combo
   (a bubbling `cbxchange` on a `.cbx[data-ci]`) re-runs `refill()`/`render()`.
4. **Forecast (picked combos)** — for the **next calendar month** (from today; Sep → Oct),
   each combo gets `forecastUnits`/`forecastPct` (share of that month's combo sales),
   `inRange` (offer price **3,399–6,199**), `stockReady` (buildable ≥ **`stockMin` = 100**),
   `scarce` (bags of the tightest pair), and **`clientDemand`** — how much its bags are requested
   in **this month's self-made combos** (`smc.selfMade`, the CBR client-driven pairings), a
   leading demand signal. **Demand** = it sold that month last year **OR** clients are
   self-making its bags now. Three tiers: **★ PICK** = in-band + demand + stock-ready;
   **🔧 PRODUCE** = in-band + demand but low stock (make the `scarce` bag); else plain.
   Candidates sort **best → least** (pick, then produce, then rest; by forecast units, then
   client demand). The Forecast card shows all **10 combos ranked 1–10** (rank, was→now, cost,
   margin, live buildable, forecast %, **Client req.**, status) and mirrors the picker live
   (`renderForecast`). The **Status** cell has a **hover** (and the column header a legend
   hover) spelling out the three gates for that row — *PRICE* (now vs the band), *DEMAND*
   (sold that month last year, from the forecast %, **or** clients requesting its bags now,
   from Client req.), and *STOCK* (buildable vs `stockMin`) — so it's clear whether a **★ Pick
   — sells in Oct** came from last year's sales, **clients requesting it** from current
   self-made demand, a **🔧 Make** from low stock, or **off-band** from price alone.

   **Baseline forecast (fixed)** — a second card (`#fc-baseline`) directly below the live
   Forecast holds a **frozen snapshot** of the recommendation as first generated. The JS
   captures the very first `renderForecast()` output once (`fcBaselineCaptured`) and never
   touches it again, so as you edit combos the live Forecast changes while the baseline stays
   put — the reference to compare your picks against. Self-made-driven picks (e.g. Jumbo+Standard/Antitheft, client demand 30,
   no Oct sales history) surface here that pure seasonality would miss.
5. **Seasonality** — the **2025 monthly combo calendar** (`MONTHLY_COMBOS_2025`, user-supplied)
   × **actual POS sales**. `_seasonality()` / `OP.seasonality`. Per combo: planned months
   (● featured), actual sales by calendar month (green, **row-normalised** so you see when it
   peaks, not the adoption growth trend), total units, formula price, top **region**, and an
   EVERGREEN (5+ months) / SEASONAL (1 month) / N× (2–4 months) badge — **each badge has a
   hover** explaining that combo (planned months, total sold, strongest month, top region).
   Month headers carry Kenya-calendar overlays (the `FACT` map, `{tag, full}` per month):
   a short purple **tag** under the month name, and on **hover** the full entry — **Kenya
   public holidays** (New Year Jan 1, Good Friday/Easter Monday Mar–Apr, Labour Day May 1,
   Madaraka Jun 1, Huduma Oct 10 & Mashujaa Oct 20, Jamhuri Dec 12, Christmas Dec 25 & Boxing
   Day Dec 26), plus school terms and retail events (Valentine's, Black Friday). The table is **sortable**
   like the profit ranking — every header clicks to sort, **including each month** (e.g. click
   Oct to rank combos by October sales); default Total ▼. A **search box** (`se-search`)
   filters the table to combos containing a typed bag (e.g. "Nizana") and shows a one-line
   summary (`se-count`) — how many combos contain it, their total units sold, and the
   best-selling one — so you can tell at a glance whether that bag's combos performed.

   **Sales caveats (documented on the page):** combos are rung as POS products only from
   **Jul 2025**, so earlier months show the plan only; calendar months mix years (Jan–Sep =
   2026, Oct–Dec = 2025), so compare **within a row, not down a column**. Sold combo products
   are matched to the 2025 list by **most-specific slot overlap** (`best_match` — same slot
   count, every slot overlaps, tightest alternatives win, so *Safiri+Standard/Antitheft* beats
   the looser *Safiri+Antitheft*); ~64% of combo units match the 2025 list (the rest are
   current combos not on it, e.g. Sarai+Prime). The 0-price serial component lines (from the
   POS combo structure) are never counted as sales — only the priced `+` line is.
   Region from `self_made_combos._SHOP_REGION_DEFAULT` via `_region_of`.

## Pricing — WAS vs NOW, from the offers sheet

The **offers sheet** (`_read_offers`, `OFFERS_SHEET_ID`) gives every bag two prices:
col **D = full price** and col **F = offer price**, plus col **C = category**. The catalog
(`_build_catalog`) stores per bag `valueWas` (full D) and `valueNow` (offer F); bags not on
the sheet fall back to **2 × production cost** for both.

**Never-discounted bags** (`FULL_PRICE_BAGS` = MEGA, TAJI, LOOP, ZULA — matched by name /
word-prefix via `_is_full_price`, so "LOOP" catches "LOOP BP", "MEGA" catches "MEGA BAGPACK")
are priced at the **original full price for NOW too** — `valueNow` is forced equal to
`valueWas`, so they carry no offer reduction anywhere they're used (combos, power deals).

### Alternate offer prices — `offerAlts` and the per-bag price picker

Some bags may be sold at **any one of several offer prices** — the price list writes them with a
slash, e.g. `JUMBO 3200/2400/2000`, `ZURI 3200/3000/2000`, `AMAYA 2700/3200`. The engine stores
this as two fields per bag in `offers_prices.json`:

- **`offer`** — a plain number, the **default** price (the first one listed). Everything that runs
  server-side uses it: the catalog's `valueNow`, `_next_month`'s Σ max-per-pair pricing, the
  3,399–6,199 band test, and the frozen baseline forecast.
- **`offerAlts`** — the list of *all* allowed prices for that bag, including the default.

> **`offer` must stay a single number.** `_read_offers_cache` coerces it with `float()` inside a
> `try/except (ValueError, TypeError)` that `pass`es — so a **list** in `offer` silently drops the
> whole bag from the catalog, with no error anywhere. That is why the alternates live in a
> separate key.

The catalog exposes the list as **`valueAlts`** (rounded, sorted high→low, always containing
`valueNow`), and each power deal carries the same list as **`priceAlts`**.

**The picker.** Wherever a bag with more than one allowed price appears — each combo slot in the
next-month grid, and each of the 10 power-deal slots — it gets a small `.price-sel` dropdown of
its allowed prices, built to match the `.basis-tog` toggle beside it. Changing it recomputes that
combo's NOW / margin / band status, or that power deal's margin and the running total, live.

Rules:

- **Live-only.** The choice lives in the DOM, exactly like `.basis-tog` — it is not written to the
  payload and does not survive a rebuild. The frozen **baseline forecast** therefore always shows
  the default-price picture, which is what makes it a useful comparison.
- **A BOM pair ignores its picker.** Flip a pair to **BOM** and it contributes production cost to
  NOW, so the price choice is irrelevant there and its selects are disabled.
- **Never-discounted bags get no alternates.** `FULL_PRICE_BAGS` (MEGA, TAJI, LOOP, ZULA) have
  `valueAlts = [valueWas]`, so there is nothing to pick.
- **Changing the bag in a slot rebuilds that slot's picker**, since the alternates belong to the
  bag, not the slot.
- **The sheet has no alternates column.** `offerAlts` is local-only: a live sheet read merges the
  cached alternates back in by bag name, and `_write_offers_cache` preserves them. Set
  `"_lock": true` to make the local file the source of truth outright.

### Downloaded copy & offline fallback — `offers_prices.json`

The prices are also kept as a **local downloaded copy** in the dashboard root
(`OFFERS_CACHE` = `offers_prices.json`), so the page never depends on the sheet being
reachable at build time:

- **Live run** — when the sheet is reachable, `_read_offers` reads it *and rewrites*
  `offers_prices.json` (`_write_offers_cache`), so the copy is always the latest. Every run
  keeps it current — that is how you "update the downloaded version".
- **Sheet down** — if the fetch throws, `_read_offers` falls back to `offers_prices.json`
  (`_read_offers_cache`) and the build still succeeds on the last good prices.
- **Hand-edited override** — set `"_lock": true` in the file to make the downloaded copy the
  **source of truth**: it is used directly and the sheet is *not even consulted* (nor
  overwritten), so your manual edits stick. Set it back to `false` to resume auto-refresh.
- The file is human-readable JSON: `{ _note, _updated, _source, _lock, offers: { BAG:
  {category, price, offer} } }`. `_read_offers` returns `(offers, source)` and the page's
  **Price source** note (`OP.priceSource`) shows which path was used — e.g. *"offers sheet
  (live — downloaded copy refreshed)"*, *"(sheet unreachable)"*, or *"(locked — hand-edited
  override)"* — so you can always see whether the page is on live or downloaded prices.

A combo is laid out like the sheet — a **fixed 3-pair grid** (`slot / slot ➕ slot / slot ➕
slot / slot`), where `/` = or and `➕` = added, and any slot can be **Zero** (empty). Per pair
the price is the **MAX** of its two slots; summed across pairs:
- **price NOW** = Σ max(`valueNow`) per pair — the discounted offer price.
- **price WAS** = Σ max(`valueWas`) per pair — the full price.
- **cost** = the now-max bag's production cost per pair; **buildable** = min pair stock (each
  pair's stock = sum of its two slots, since either fills it).

**Per-pair offer/BOM toggle.** Each pair carries a small **offer ⇄ BOM** toggle (`.basis-tog`,
default `offer`). Flip a pair to **BOM** and that pair contributes the bag's **production cost**
to **NOW** instead of its offer price — i.e. the bag is added to the combo *at cost* (that
pair's margin becomes ~0), while WAS still shows the full price. Example: `SARAI + PRIME` with
Sarai left at **offer** (e.g. 3,700) and Prime flipped to **BOM** → NOW = Sarai offer + Prime
cost. It's client-side in `recompute()` (reads each pair's `data-basis`) and updates the live
Forecast; the fixed baseline stays at the all-offer pricing, so you can compare.

Verified against the sheet: `LOLA + MINI ZURI/TRECENTO` → now = 1,700 + max(2,200, 1,700) =
**3,900** (exact), was = 2,100 + 2,600 = 4,700. Each combo pre-fills its grid from the
reference month but **every slot is a searchable combobox** the user can change freely.

## Data sources

- **`self_made_combos.html` → `SMC`** — reused (no re-query) for the running combos:
  units, revenue, component bags + live Odoo stock, and `monetaryImplication` (clean
  button-based unit price). So `offer_picking.py` runs **after** `self_made_combos.py`
  (the NAV chains both: `["self_made_combos.py", "offer_picking.py"]`).
- **"Updated BOMs" sheet** (`BOM_SHEET_ID`, gid `678614335`) — per-bag production cost,
  **col A = bag type, col G = total cost**. Read via `get_gspread_client()`.
- **Offers sheet** (`OFFERS_SHEET_ID`, shared & live) — B = product, C = category,
  D = official price, F = offer price. WAS/NOW pricing comes from here (col D / col F).
  Mirrored to the local **`offers_prices.json`** downloaded copy on every successful run,
  which is the offline fallback — see *Downloaded copy & offline fallback* above.

## How profit is computed

- **Production cost** (`_combo_cost`): the combo name is split on `+` into slots; each
  slot's cost = the **average** production cost of its matched alternatives (on `/` / `or`).
  Summing per slot means a same-bag combo (Jumbo+Jumbo) counts the bag **twice** — the
  `×2` the BOM formula uses. Alternatives are matched to a BOM bag type by alias
  (`Laptop Backpack→Code 3`, `Standard Travel→Standard`), then colour/category words
  dropped, then longest-prefix. Unmatched alternatives are surfaced in `OP.unmatched`
  (cost estimated from the ones that did match).
- **Price**: currently `monetaryImplication.actual / units` per combo (button-rung, so it
  is unaffected by the week-1 JUMBO+JUMBO backfill). Swap to offers-sheet F when shared.
- **Profit/unit** = price − cost; **margin %** = profit ÷ price; **total profit** =
  profit × units sold this month.
- **Buildable**: min over slots of the combined current Odoo stock of that slot's bags
  (from `SMC.runningCards[].bags[].stock`).

## Payload (`OP`)

`{ month, priceSource, offers[], bomBags, unmatched[], nextMonth }` where each offer is
`{ combo, category, price, cost, profit, margin, units, totalProfit, revenue, buildable,
bags[] }`. `nextMonth = { ready, refMonth, candidates[] }` — `ready:false` until the
reference-month combos are supplied.

## Pending / next steps

- **Bag-name matching reuses the stock-levels aliases** (`_ALIAS` / `_apply_alias`,
  mirroring self_made_combos `BAG_ALIASES`): a bag missing its own BOM row is matched under
  another name — e.g. `STANDARD` → `TRAVEL` (it's sold as "Standard Travel" but the BOM
  lists TRAVEL). Add new aliases there if a bag comes up unmatched.
- Consider a per-shop layer (which profitable combos each shop should push, vs the
  Jumbo+Jumbo cap) — see [self-made-combos.md](self-made-combos.md) combo-button section.
