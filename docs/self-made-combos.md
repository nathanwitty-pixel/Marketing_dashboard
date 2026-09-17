# Self made combos vs running combos

- **Generator:** `self_made_combos.py` (also writes the `OFFER_DATA` block via `offer_data.py`)
- **HTML:** `self_made_combos.html`
- **Data markers:** `<!-- SMC_DATA_START -->…<!-- SMC_DATA_END -->` (const `SMC`) and,
  embedded just after it, `<!-- OFFER_DATA_START -->…<!-- OFFER_DATA_END -->` (read by
  the Monthly Report). Region-selector render JS + Power-Deals view are hand-written in
  the HTML; the generator only replaces the data blocks.
- **Global JS data:** `SMC` (combos, running cards, regions, deals) and `OA` (offer data).

## What the page shows

Three areas, all scoped to the **current live month** (`report_month.live_month_window()`):

1. **Self-made combos vs Running combos.** Combos sold this month, classified against
   the **authoritative offer sheet** (the SEPT COMBOS list, `oa["combos"]`), not a flag:
   - **Running (official) combo** = the Odoo combo's **bag composition matches a combo on
     the offer sheet**, *however it was rung* (official button or CBR). Matching is
     slot-aware (`_matches_sheet` / `_build_sheet_slots`): each combo is split on `+` into
     slots, each slot on `/` (sheet) or `or` (Odoo) into options, options normalised
     (colours/category words dropped, promo aliases applied — Laptop Backpack→Code 3,
     Standard Travel→Standard, Neo Man Bag→Neo Man). A combo matches if it has the same
     slot count and every slot overlaps.
   - We classify on **composition alone** (not `include_all`, not `is_cbr`): a combo is
     JUMBO+JUMBO if *both* bags are Jumbo (any colours) — so the official `Jumbo + Jumbo`
     AND every CBR pairing like `Jumbo Grey + Jumbo Black Combo` all count as running. A
     Jumbo + a **different** bag (`Jumbo + Prime`, `Baby + Jumbo`) matches no sheet combo,
     so it is self-made. This also keeps `Amaya + Avana` self-made (Avana isn't on the
     sheet).
   - **Self-made combo** = any `+` combo whose composition matches **no** sheet combo.
   - **Merge by sheet label:** several Odoo products can map to one sheet combo (e.g.
     `Jumbo + Jumbo` + `Jumbo green+Jumbo black` → JUMBO+JUMBO). They're collapsed into a
     single running card (`running_products` keeps the unmerged list for the usage calc;
     `running` is merged, carrying a `tmpls` list so weekly + component data aggregate).
     The **weekly breakdown** (`combos_goal.weeklyDetail`, from `week_combos`) also maps
     each product to its sheet label via `_matches_sheet`, so every Jumbo+Jumbo pairing
     rolls into one **JUMBO+JUMBO** row per week — week 1 carries the early self-made-style
     CBRs that ran before the official product existed, and it keeps tracking as
     JUMBO+JUMBO from week 2 on. Self-made combos keep their own name in the breakdown.
   - **Week-1 JUMBO+JUMBO "sold as singles" backfill** (`JJ_WK1_PAIRS_SQL`, `jj_wk1_pairs`):
     in week 1 the combo button wasn't in use, so pairs were rung as two separate single
     Jumbos. We count them at the **receipt level** — a sale with 2+ single Jumbos =
     `floor(units/2)` combos (a lone single Jumbo is a genuine one-bag customer and is
     NOT counted) — and add that to JUMBO+JUMBO's **week-1 sold + unit total** (both the
     card `weeks[0]` and the weekly breakdown). Applied to **week 1 only** (button is used
     from week 2). **Units only** — the credit is added *after* `monetary_implication`, so
     revenue / discount % stay on the actual button-rung combos (the pairs' money is
     already counted as single-bag sales). The card shows a note: "Wk 1 includes N rung as
     single Jumbos". Validated Sep 2026: 10 rung + 51 sold-as-singles = 61 (Hilton 10,
     Mombasa 7, Hazina 6, … matching the shops' own tallies).
   - **The sheet is the source of truth for the monthly running list** — any extra combo
     in Odoo that isn't on it is self-made. If the sheet can't be read, the code falls
     back to the old heuristic (`include_all` AND not CBR).
   - Only products whose name matches `LIKE '%+%'` are combos ("A + B").
   - Running cards show each component **bag** with `· N sold` = the units of that bag
     *printed inside combos* (component attribution, see below).
2. **Region selector** (Kenya / Sinza / Uganda pills) — combo/singles/specials guidance
   cards per region with a Type dropdown, a sales-vs-stock chart, and per-bag stock
   (never summed across bags).
3. **Power Deals vs Deal of the Week** — the Kenya deals sheet, enriched with live Odoo
   sales, per-week series, stock, and a per-shop breakdown.

## Data sources

- **Odoo combos:** `COMBO_SQL` (name `LIKE '%+%'`, `is_cbr`, `include_all`,
  `colour_options`), `COMBO_WEEKLY_SQL`, `MONTH_WEEKLY_SQL` (Aug baseline + Sept-so-far),
  `REQUEST_SQL` (CBR log).
- **Component attribution:** `COMBO_COMPONENTS_SQL` reads
  `combo_product_attribute_values` (a Python-literal string on `pos_order_line`) →
  `ast.literal_eval` → the actual bag colour chosen → matched to a bag type. This is how
  a running card's component `sold` count is computed (what was *printed*, not the
  standalone sale of the same bag).
- **Deals sheet:** `DEALS_SHEET_ID` → worksheet **"Kenya"**. Columns: A Tier · B Month ·
  C Product · D Location · E Type · F Original · G Current · H Discount. Rows filtered to
  the current month name (`mon.lower() == "september"`). `Type` = "Power Deals"
  (Tier "All", location "All", runs all month) or "Deal of the Week" (Tier 1/2, per
  location). Location alias: `"Nairobi Town" → "Starmall"`.
- **Deal sales:** `DEAL_SALES_SQL` / `DEAL_WEEKLY_SQL` (Kenya tills, `name NOT LIKE '%+%'`
  so combo products don't leak into deals), `DEAL_SALES_BY_SHOP_SQL` (per-till).
- **Region combos/singles/stock:** `offer_data.py` (COMBOS sheet — Sinza B34:C57,
  Uganda B61:B63) surfaced via `_read_offer_analysis()`.
- **Stock:** the offer sheet's Kenya stock, with an **Odoo live fallback** for any bag the
  sheet reports as 0 (`_odoo_stock_for(codes)`), plus **per-shop** live stock
  (`_odoo_stock_by_shop`).

## Returns netting — `qty <> 0` (correct "bags sold")

Every **units-sold** figure on this page is a **net** number: genuine sales **minus
returns**. This is done by summing the POS line quantity with the filter `pl.qty <> 0`
(not `pl.qty > 0`), so a return line — which Odoo records as a **negative** qty on a
separate order — is *subtracted* from the total instead of being ignored.

- **Why it matters.** With `qty > 0` a return is silently dropped: the original sale is
  counted but the give-back is not, overstating "bags sold". Example: **Lola** had a
  genuine sale of **+777** (Order `24685-009-0011`) and a matching return of **−776**
  (Order `24685-010-0017`) the same day. `qty > 0` reported **777**; `qty <> 0` reports the
  correct **net 1**.
- **Where it applies.** The netting is in the SQL of every sold-count query the page uses:
  combo component prints (`COMBO_COMPONENTS_SQL` / `COMBO_BY_SHOP_SQL`), singles
  (`SINGLES_BY_SHOP_SQL`), bag sales (`BAG_SALES_SQL`), and the deal queries
  (`DEAL_SALES_SQL`, `DEAL_WEEKLY_SQL`, `DEAL_SALES_BY_SHOP_SQL`). A return dated inside the
  reporting month nets against that month; the [standalone SQL](../sql/self_made_vs_running_combos.sql)
  uses the same `qty <> 0` so it agrees with the page.
- **Same rule, other menus.** The identical change was applied to **Current Performance**
  and **New Products** (`new_products.py` → `odoo_sales_window`), so "bags sold" means the
  same thing everywhere. Timed Offers still counts gross (`qty > 0`).

## Deal enrichment & name matching (`_enrich_deals` / `_match`)

> Full matching reference: [product-matching.md](product-matching.md).

Odoo product names are colour-only ("JAMELA BLACK", "KAI BLACK"); deal labels add a
category word ("Jamela handbag", "Kai backpack"). Matching:

- **Full label first** (`_full`): exact / prefix either direction.
- **Category-stripped root fallback** (`_rooted`): if the label's last word is in
  `_CATEGORY_WORDS` (HANDBAG, BACKPACK, TRAVEL, SLING, MESSENGER, BAG, LUNCHBAG,
  LUNCHSET, HB, BP…), retry on the root ("JAMELA", "KAI", "LIAM").
- **Aliases** (`DEAL_ALIASES`): STANDARD TRAVEL→TRAVEL, CAIRO BACKPACK→CAIRO BP,
  LAPTOP BACKPACK→CODE 3, NEO MAN BAG→NEO MAN, **BRIEFCASE→BRIEF CASE** (the sheet writes
  it one word; Odoo stores "BRIEF CASE …"). The alias is applied to **sales, weekly and
  stock** matching via one shared selector — so a spelling variant matches everywhere, not
  just for stock. If a deal shows 0 sold/stock but you know it sells, the label almost
  certainly differs from the Odoo name — add a `DEAL_ALIASES` entry.
- **Dedup:** a bag that runs as **both** a Power Deal and a Deal of the Week is one bag's
  sales — counted once in the combined "Deal units sold" headline (`dedupSold`,
  `dedupRevenue`, `dedupProducts`, `overlapProducts`).
- **Exclude combo bags from the headline:** the "Deal units sold" KPI uses
  `dedupSoldExCombo` / `dedupRevenueExCombo`, which **drop deal bags that are also running-
  combo components** (Lola, Antitheft, Man Bag, Nizana, …) — they're already represented
  under the combos, so the cumulative doesn't mix deal bags with combo bags. Passed in via
  `payload["comboBags"]` (the running cards' component bag names) → `_enrich_deals(…,
  combo_bags)`; `comboBagDeals` counts how many were dropped (shown in the KPI subtext).
  The same exclusion applies to each side's own "· N sold" sub-total
  (`powerSoldExCombo`, `dowSoldExCombo`). The **cards still render** every deal, and the
  Discount KPI still uses every deal.

### DoW mirror shops (`DOW_MIRROR` in `_read_deals`)

Some shops run the **same** Deal of the Week as another shop but aren't listed
separately in the sheet. `DOW_MIRROR = {"Starmall": ["Hazina", "Hilton", "KTDA"]}` — each
mirror shop inherits every DoW product its parent runs (appended to that product's
`locations`), so it gets its own per-shop card with its **own** sold + stock. Edit this
map to add/remove mirrors; no sheet rows needed. (The sheet only lists 14 DoW locations
for September; the mirror brings the total to 17.)

### Per-shop Deal-of-the-Week numbers (`soldByLoc` / `stockByLoc`)

Each DoW deal carries **per-shop** figures so a shop's card shows *its own* September
numbers, not the bag's Kenya-wide total:

- `soldByLoc` = per-till units (`DEAL_SALES_BY_SHOP_SQL`), keyed by the sheet's location
  label via `_SHOP_TO_LOC` (POS config name → label, e.g. `KTDA SHOP`→`KTDA`,
  `WEBSITE SALES`→`Website`). Matched with the **same full-vs-root mode** chosen for the
  Kenya-wide figure, so a shop's number is a true subset of the total.
- `stockByLoc` = per-shop live Odoo stock (`_odoo_stock_by_shop` over `_STOCK_CODE_TO_LOC`,
  the shop stock codes; Website has **no** stock code — it's online). The per-shop stock
  map holds **colour-level** names ("KAI BLACK"), so it is matched with
  `_full`/`_rooted`/`_stock_match` — **not** the bag-type-level `_stock_match` alone.
- In the HTML `dowMetrics`, a location's `sold`/`stk` come from `d.soldByLoc[L]` /
  `d.stockByLoc[L]` (0 when absent), falling back to the global only if the maps are
  missing entirely. Website (`isWebL`) is judged on **sales alone** — `stk = null`, so it
  is never flagged out-of-stock, and the tooltip shows "online" instead of "0 stk".

### Tier 1 vs Tier 2 gauge (`deals["tierCompare"]`, `tierGauge()`)

A metric that gauges the two **Deal-of-the-Week phases** against each other. **Tier 1** runs
the first fortnight (**Wk 1–2**); **Tier 2** runs the remaining weeks (**Wk 3+**, the "last two
weeks"). Each tier is scored on **its own week window** (not the whole month), so the phases
compare like-for-like. Per tier: **products**, **units sold**, **revenue** (window units ×
deal price), **discount given** (window units × per-unit discount), and a **per-week
run-rate** (units ÷ weeks elapsed in its window) — the headline, so a still-running Tier 2 is
judged fairly against a finished Tier 1.

- Tier membership is the sheet's **Tier** column (col A); a product listed under both tiers
  runs in both phases and counts its own-window sales in each. Digit-matched (`_tdigit`), so
  "Tier 1" / "1" both work.
- `inProgress` = the tier's window includes the **live (partial) week** (`deals["curWeek"]`),
  so the gauge marks it "· wk N live" and the verdict notes Tier 2 is still filling in — its
  run-rate is a floor, not a final figure.
- Rendered by `tierGauge(D.tierCompare)` as a panel **above the Deal of the Week table** in
  `renderDeals()`; two colour-coded columns (Tier 1 amber, Tier 2 cyan) + a run-rate verdict
  (`+/-%` Tier 2 vs Tier 1).

**Deal of the Week split by tier** — the DoW panel itself carries a segmented control
(**All tiers / Tier 1 / Tier 2**, with counts). Picking a tier re-renders `dowMetrics` for
just that tier (`renderDowTier` → `dowTierList` filters `D.dealOfWeek` by `dowTierDigit`), so
each phase's **selling / not-selling / out-of-stock / idle** breakdown and per-location table
stand on their own. Only one tier is shown at a time, so the `dowCatDetail` / `dowLocDetail`
hover globals stay consistent; `wireDowHover()` re-runs after each switch.

## Combo button usage (till check)

Rendered **inside each running combo card** (in `renderRunningCards`). The headline
benchmarks the current week against the combo's **best week**: `rung <current week>` vs
`best <best completed week>`, `% = current ÷ best` — both from the card's own weekly series
(`c.weeks`), so it's live Odoo, not the stale sheet snapshot (which read >100% once the
month passed week 1). The current (in-progress) week is excluded when picking the best week
so it's a real benchmark; with only two weeks so far, "best" is just week 1. Below it, a per-shop
chip row (from `card.usage`, this month) shows `rung` vs `pot.`, **ordered by `rung`
(highest first)**. A chip is **red** when the shop rings **less than half of the best-
performing shop in its own region**. The shop→region map is read from
[shop-regions.md](shop-regions.md) at build time (`_load_shop_regions`, fallback
`_SHOP_REGION_DEFAULT`) — edit that table to change regions, no code change;
`_combo_button_usage` computes each region's best `rung` per combo and sets `red`. The standalone panel `#smc-usage-panel` still exists but is
`display:none` (kept as a fallback / for `SMC.comboUsage`), built by `_combo_button_usage()`:

- **Expected** — the offer sheet's COMBO figure for that combo.
- **Rung** — combo-product units recorded in Odoo this month (`COMBO_BY_SHOP_SQL`),
  matched to the combo via `_matches_sheet`.
- **Adherence %** = rung ÷ expected; rows sorted worst-first, so an under-rung combo
  leads. (The original Jumbo+Jumbo finding was `rung ≈ 1` vs a sheet 45 — the tills rang
  two **single** Jumbos, and some got tangled with self-made CBR pairings. **Now resolved:**
  the bag-composition match routes every all-Jumbo pairing to the running combo, which
  rings ~84/mo — no self-made leakage.)
- **Per-shop** (click a row): each shop's `rung` and `implied` "potential" — the combos
  that shop's single-bag sales *could* have formed, computed as the **min across slots**
  of component-bag singles ÷ how many that slot repeats (`SINGLES_BY_SHOP_SQL`,
  `_implied`). Shops with `rung 0` but `implied > 0` are flagged red (selling the combo as
  separate bags). **`implied` is an upper bound** — most single-bag sales are genuine
  standalone demand — so it's a ceiling to investigate, never a target.

**Reading `rung` vs `pot.` (green vs salmon).** The green **`rung` is the number of combos
actually sold** on the combo button; `pot.` is the ceiling of combos the shop's loose-bag
sales *could* have formed. The gap is **opportunity, not lost money** — a combo is a ~20%
bundling *discount* (see Monetary implication), so a pair sold as two **separate full-price
bags** earns **more** than the same pair rung as a combo. Worked example — Hilton,
`AMAYA/ELYSE+MOON/NIZANA` (combo KES 3,799 vs KES 4,753 for the two bags apart):

| Scenario | Revenue |
|---|--:|
| Ring all 42 as combos | 42 × 3,799 = **159,558** |
| 26 combos + 16 sold separately | 26 × 3,799 + 16 × 4,753 = **174,822** |
| Difference | **+15,264** for the mix |

So `pot.` measures **attachment opportunity**: chasing it only wins where the discount is
what tips a one-bag customer into buying two. Where the customer would have bought both
bags anyway, keeping them as full-price singles is the better outcome — a "missed" combo
is not automatically a loss.

This exists because combos sold as individual bags never enter Odoo as combos (the
original Jumbo+Jumbo finding: 45 on the sheet, 1 in Odoo — the tills rang two single
Jumbos). That specific case is now fixed (all-Jumbo pairings route to the running combo,
~84 rung/mo); the panel remains to catch the same pattern on other combos.

## Rank chip — follows the active Sort filter (whole menu)

Every card list in this menu uses the same chip: it shows the value of **whatever metric
the Sort dropdown is set to**, and its colour **ranks it against its peers — the bottom 3
get a red `▼` chip, the rest green `▲`**. So on "Total sales" the figure is units sold and
the 3 lowest-selling go red; on "Weekly gain" the figure is `latest week − previous week`
(most negative ranks lowest → red); on "Stock"/"Remaining"/"cross-sell shares" likewise.
Shared helpers at the top of the main `<script>`:
`window.smcSortMetric(sortV, c)` → `{val, lbl, rank}` (the number, its label, and the
rank value where higher = better; for `rem`, more-remaining ranks worse),
`window.smcRankChipText(metric, isLow)` (the chip text), and
`window.smcBottom3(list, valOf, keyOf)` (the 3 lowest keys). Applied in:

- **Running combos** — `renderRunningCards(sortV)` (sortV from `#smc-og-sort`), ranked
  across all `SMC.runningCards`.
- **Power deals** — `powerCards` (sortV from `#smc-pd-sort`), ranked across all
  `D.powerDeals` (keyed by `product`).
- **Region cards** (Sinza/Uganda) — `renderCards` → `cardHtml(c, cur, lowSet, sortV)`,
  ranked within the current group's `cards` (keyed by `name`).
- **Offer-guidance combos** (`O.combos`, sheet-order, not filter-sorted) — kept on a simple
  latest-week rank; it's a secondary panel.

The rank is computed from the **full** list (not the filtered/sorted view), so it's stable
as the Sort/Stock filters change, and it re-ranks whenever the Sort dropdown changes.

`window.smcWeekTrend(weeks)` (defined at the **top**, before the `DOMContentLoaded`
listener) is the older week-on-week trend; the rank chips replaced it on these cards, and
its `diff` is still used by the power-deal / running-card **verdict text**. `mature = new
Date().getDay() >= 4`. **Keep it defined above `DOMContentLoaded`** — it's called during
`draw()`; defining it later throws `smcWeekTrend is not a function` and aborts the rest of
the script (this once broke the Power-Deals toggle).

## Monetary implication (`#smc-mi-panel`, `SMC.monetaryImplication`)

The money given away by bundling. Per combo, **Expected** = the combo's bags valued at
their **full individual price** (`bag_original_prices.json`, editable) × units printed;
**Actual** = the combo's real revenue; **Discount** = Expected − Actual. Running uses the
card's component prints (`bags[].sold`); self-made uses the name's component bags ×
combo units. Shown as two tables (running / self-made) + KPI cards comparing the two
(e.g. running ~22% discount vs self-made ~10%). Prices missing from the JSON are flagged
per row (ⓘ) and understate that combo's Expected.

## Bags not on offer — per market (Kenya / Sinza / Uganda)

Bags **selling this month but on no offer**, computed for **each market** by
`_bags_not_on_offer(m_start, m_end, on_offer_raw, sql, currency)`. It sums standalone bag
sales for that market's tills, resolves each Odoo product to a catalogue bag
(`bag_original_prices.json` keys, longest-prefix — the bag *names* are shared across
markets, so the same keys resolve Sinza/Uganda products; revenue stays in the local
currency), and marks a bag on-offer if it matches (equal or word-prefix, aliases applied:
Cairo Backpack→Cairo BP, Briefcase→Brief Case, …) any of that market's on-offer bags.

- **Kenya** (`#smc-noffer-panel`, `SMC.bagsNotOnOffer`, KES) — till scope
  `BAG_SALES_SQL` (every till except sinza/dar-es-alam/uganda). On-offer = running-combo
  components + Deal-of-Week + Power-Deal products.
- **Sinza** (`#smc-noffer-sinza-panel`, `SMC.bagsNotOnOfferSinza`, TSh) — till scope
  `BAG_SALES_SINZA_SQL` (sinza + dar-es-alam). On-offer = the component bags of the Sinza
  sheet **combos + singles + specials** (`_region_on_offer_bags(payload, "sinza")`).
- **Uganda** (`#smc-noffer-uganda-panel`, `SMC.bagsNotOnOfferUganda`, USh) — till scope
  `BAG_SALES_UGANDA_SQL` (uganda). On-offer = the Uganda sheet **combos + singles**.

Each panel shows count/units/revenue not on offer + the on-offer coverage %, and lists the
not-on-offer bags by units (candidates to put on an offer). The Sinza/Uganda panels are
hidden until they have data (`total > 0`). All three share one JS `renderNoffer(N, panel,
kpi, list)` that reads `N.currency`.

## Standalone SQL

`sql/self_made_vs_running_combos.sql` — a runnable query classifying every `%+%` combo as
Running (`product_combo.include_all`) vs Self-made (`pos_combo_request`, not include_all),
with monthly units/revenue, Kenya only, `qty <> 0` (nets returns). Detail + summary forms.
(Pure SQL can't match the offer sheet, so it uses `include_all`, not the app's sheet-match.)

## Gotchas / history

- **Combo products must be excluded from deal totals** — `DEAL_SALES_SQL` has
  `AND pt."name" NOT LIKE '%+%'` (else e.g. the "Amaya +" running combo leaked 54 units
  into the DoW total).
- **DoW "0 sold" bug** (fixed): deal labels carry a category word Odoo names don't, so the
  full-label match found nothing → 0. The `_CATEGORY_WORDS` root fallback fixed it
  (Jamela 0→37, Kai 0→94, Liam 0→43; DoW total 412→1059).
- **Per-shop card showed the global total** (fixed): the location card used `d.sold`
  (Kenya-wide) for every shop — Starmall showed Kai 94. Now uses `soldByLoc`/`stockByLoc`
  (Starmall Kai 5 sold · 14 stk).
- **`offer_type_analysis` is fully retired** — the Monthly Report reads combo/offer data
  from the `OFFER_DATA` block this page writes.

## Regenerate

```
python self_made_combos.py        # DENRI_LAUNCHER=1 to skip the browser tab
```
Reads Odoo + the deals/COMBOS sheets; rewrites the `SMC_DATA` and `OFFER_DATA` blocks.
</content>
</invoke>
