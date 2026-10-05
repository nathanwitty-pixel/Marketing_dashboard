# Self made combos vs running combos

- **Generator:** `self_made_combos.py` (also writes the `OFFER_DATA` block via `offer_data.py`)
- **HTML:** `self_made_combos.html`
- **Data markers:** `<!-- SMC_DATA_START -->…<!-- SMC_DATA_END -->` (const `SMC`) and,
  embedded just after it, `<!-- OFFER_DATA_START -->…<!-- OFFER_DATA_END -->` (read by
  the Monthly Report). Region-selector render JS + Power-Deals view are hand-written in
  the HTML; the generator only replaces the data blocks.
- **Global JS data:** `SMC` (combos, running cards, regions, deals) and `OA` (offer data).

## What the page shows

**Sidebar** ([page sidebar](README.md#page-sidebar)) — **Regions** picker (Kenya · Sinza · Uganda — sub-lines from `runTotals` / `regions[*].totalStock`) replaces the in-page region buttons (hidden; the picker clicks them), then the visible region's sections; Combos ↔ Power Deals rebuilds the list.

Three areas, all scoped to the **current live month** (`report_month.live_month_window()`):

1. **Self-made combos vs Running combos.** Combos sold this month, classified against
   the **authoritative offer sheet** (the SEPT COMBOS list, `oa["combos"]`), not a flag:
   - **Running (official) combo** = the Odoo combo's **bag composition matches a combo on
     the offer sheet**, *however it was rung* (official button or CBR). Matching is
     slot-aware (`_matches_sheet` / `_build_sheet_slots`): each combo is split on `+` into
     slots, each slot on `/` (sheet) or `or` (Odoo) into options, options normalised
     (colours/category words dropped, promo aliases applied — Laptop Backpack→Code 3,
     Standard Travel→Standard, Neo Man Bag→Neo Man; a **bare "Travel"** slot is the
     Standard Travel bag → Standard). A combo matches if it has the same slot count and
     every slot overlaps — **in any order** (the sheet's `Code 3+Travel` is rung in Odoo as
     `Standard Travel Black + Code 3 Black Combo`).
   - **Closest name in Odoo (fallback, Oct 2026).** When no sheet combo matches exactly, the
     Odoo combo is matched to the sheet combo whose names are **closest**: per slot, an
     option counts as the same bag if it is equal ignoring spaces (`Anti Theft` =
     `Antitheft`), one is a word-prefix of the other (`Code` = `Code 3`), or the spelling is
     ≥ 85 % similar. Same slot count, any order. Exact matches always win, so this only
     catches short / misspelt Odoo names — `Reo Travel + Code 3` stays self-made.
   - **The sheet's month drives the labels.** The Kenya section header (`OCTOBER COMBOS`,
     `SEPT COMBOS`, …) names the month: the "<Mon> Combos" KPI card reads it
     (`offerKpis.comboMonth`), and any `<MONTH> COMBOS` header row is skipped, whatever the month.
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
   **New month, deals sheet not filled yet** (`_deals_from_offer_sheet`): if the deals sheet
   has no rows for the live month, the page still moves to the new month — Power Deals come
   from the COMBOS sheet's own **POWER DEALS** table (`TRAVEL` → Standard Travel; price from its
   KES column where filled), `deals.source` says so, and there's no Deal of the Week until the
   deals sheet gets the month's rows. Bags on vs off Offer then builds too (it needs ≥ 1 deal).

> **Oct 2026 — no COMBOS / deals sheet any more.** The month's Kenya combo list (running vs self-made),
> the Sinza / Uganda lists and the Power Deals / Deals of the Week come from `offers_monthly.csv` and
> `deals_kenya.csv` (see README › Where the data comes from). The "Offer sales vs stock" weekly sales and
> the combo-button **expected** figure are Odoo counts (`week_combos` by list label: every combo whose bags
> match the list, however it was rung) — no hand-typed sheet columns. Bullets below that mention the COMBOS
> tab or the deals sheet describe the old source.

## Data sources

- **Odoo combos:** `COMBO_SQL` (name `LIKE '%+%'`, `is_cbr`, `include_all`,
  `colour_options`), `COMBO_WEEKLY_SQL`, `MONTH_WEEKLY_SQL` (Aug baseline + Sept-so-far),
  `REQUEST_SQL` (CBR log).
- **Component attribution:** `COMBO_COMPONENTS_SQL` reads
  `combo_product_attribute_values` (a Python-literal string on `pos_order_line`) →
  `ast.literal_eval` → the actual bag colour chosen → matched to a bag type. This is how
  a running card's component `sold` count is computed (what was *printed*, not the
  standalone sale of the same bag).
- **Deals from the posters — `deals_kenya.csv` (from October 2026, wins over the sheet).** The
  user now picks the deals from the **"Denri's Weekly Hot Picks" poster images**, transcribed into
  `deals_kenya.csv`: the sheet's columns (Tier · Month · Product · Location · Type · Original ·
  Current · Discount) plus `Poster name` (as printed) and `Poster`. `_read_deals(month)` uses the
  CSV's rows for that month when it has any; otherwise the deals sheet below; otherwise (no rows
  anywhere) the COMBOS sheet's Power Deals (`_deals_from_offer_sheet`). Transcription rules:
  - **crossed-out price = Original** (full price), the price beside it = **Current**; Discount = the gap;
  - **Location** = the shop after "Only available at …"; "Nairobi Town stores" = **Starmall, Hazina,
    Hilton, KTDA** (one row each); "the Website" = `Website`;
  - **Product = the Odoo root name**, so `_enrich_deals`' prefix match finds every colour:
    Fayola messenger → `Fayola`, Briefcase → `Brief Case`, College handbag → `College HB`,
    Doublepress backpack → `Double Press`, Neo man bag → `Neo Man`, Zane man bag → `Zane Man`,
    Pioneer / Tyler / Kai / Remi / Mega backpack → the bag name alone, Lola / Aurora / Karina /
    Amaya handbag → the name alone, Kate sling → `Kate`, Liam / Fabela travel → `Liam` / `Fabela`,
    Power "Standard" → `Standard Travel`. Check each new name prefix-matches an active Odoo product;
  - each poster = **Tier 1** (wk 1–2) or Tier 2 (wk 3+) as the user says; Power Deals = Tier "All",
    Location "All".
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

## Combo sub-lines are not single sales — `NOT sub_product_line`

Odoo writes every combo sale **twice**: the combo line (`is_combo_line`, the `A + B` product, which
carries **all** the money) and one **sub-line per bag inside it** (`sub_product_line = true`, the
actual colour variant, **KES 0**). Sep 1–24, Kenya: 968 combo lines → 2,053 bag sub-lines, exactly
one per bag slot across all 946 combo orders (only 7 combo *returns* have no sub-lines).

Until 25 Sep 2026 the single-bag queries didn't exclude sub-lines, so a bag printed inside a combo
was **also** counted as a single sale (units only — revenue was unaffected since sub-lines are 0).
Every single-bag query now has `AND NOT COALESCE(pl.sub_product_line, false)`: the deal queries
(`DEAL_SALES_SQL`, `DEAL_WEEKLY_SQL`, `DEAL_SALES_BY_SHOP_SQL`, `DEAL_SALES_SHOP_WEEK_SQL`), the
not-on-offer bag sales (`_bag_sales_sql`, `_bag_sales_daily_sql`), `SINGLES_BY_SHOP_SQL` and
`JJ_WK1_PAIRS_SQL`. Combo queries (`LIKE '%+%'`) never matched sub-lines, so they're unchanged.

- **Week-1 Jumbo + Jumbo backfill:** the 10 JUMBO+JUMBO combos rung in week 1 each carried two Jumbo
  sub-lines on one receipt, which the "2+ single Jumbos" rule counted as 10 extra pairs — 51 became
  **41** once sub-lines are excluded, so the week-1 figure is 10 rung + 41 sold-as-singles = **51**
  (previously reported as 61 and said to match the shops' tallies — that total included the rung
  combos twice). Put `JJ_WK1_PAIRS_SQL` back to include sub-lines if the shops' 61 is confirmed.
- The New Products page (`queries._BAGS_WHERE`) already excluded sub-lines; the Current Performance
  "bags sold" total deliberately **includes** them (every bag that left the shop).

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

### Deal of the Week sold = its shops × its tier's weeks (`DEAL_SALES_SHOP_WEEK_SQL`)

A Deal of the Week runs **only at its locations** (sheet col D, plus `DOW_MIRROR` shops) and
**only in its tier's window** — Tier 1 = Wk 1–2, Tier 2 = Wk 3 onward (Sun–Sat weeks, `_WK_EXPR`).
So each DoW row's `sold` / `revenue` sum **only** the sales at those shops in those weeks, and
`soldByLoc` is each shop's sales inside the window; `weeks` is the per-week series at its shops.
(Before 24 Sep 2026 it summed the bag at **every** Kenya shop **all month** — e.g. "Jumbo travel",
a Tier-2 deal at Rongai + Busia only, showed **724 sold**, which was every single Jumbo in Kenya.)
The old Kenya-wide monthly figure is kept as `kenyaSold` / `kenyaRevenue` for reference.
**Power Deals are unchanged** — they run at every shop all month, so their `sold` is Kenya-wide.
The deduped headline counts a bag on both offers once via its Power Deal (which already covers
every shop/day), and otherwise sums its DoW rows (tiers are disjoint windows).

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

## Combo ⇄ Deal-of-the-Week cross-links (tier-aware hovers)

Shared global helpers (top of the main `<script>`, keyed off the live `SMC`): `smcCurTier()` =
the tier we're measuring now (the `tierCompare` tier whose window holds the live week — Tier 2
in-period); `smcCombosForBag(name)` = running combos a bag is a component of (prefix-matched
both ways); `smcDowForBag(name)` = the **current-tier** Deal-of-the-Week entry for a bag. Used in
three places so the combo and DoW sides show how they affect each other:

- **Combo card DoW overlap** — surfaced **only in the red shop-chip hover** (below), scoped to that
  shop. (The earlier all-shops card-level note was removed as redundant — the per-shop hover already
  explains it. `_dowov` is still computed for the hover.)
- **Red shop chips → shop-specific explanation** (`u.shops`): a per-shop rung/pot chip is red when
  it under-rings (below half its region's best shop). Its **hover carries the DoW-overlap reason
  scoped to that shop** — "under-rings this combo; at [shop], its bags also sold solo on the Tier 2
  Deal of the Week: [bag] N solo here — the sale likely went to the solo deal." The per-shop solo
  counts come from `card.usage.shops[].soloTok` (a `{token: units}` map of that shop's single-bag
  sales, restricted to the combo's tokens; built in `_combo_button_usage` from `shop_tok`). Each
  combo bag carries its `tok` (`_combo_norm_option`), so `_dowov` matches a DoW bag to its shop
  solo figure. If a red shop sold none of the DoW bags solo, the hover falls back to "ring the
  combo button instead of separate bags."
- **Shop hover → inline combo note** (`buildDowTip`, the per-shop DoW tooltip): each bag that is
  also a running-combo component gets an inline "↳ in [combo]" — so you see a DoW bag that may be
  tied up in / split with a combo (the reverse direction).
- **Per-shop export → Shops Efficiency** (`combos_by_shop()` → `combos_by_shop.json`, written in
  `main()`): a compact per-shop view — each shop's running combos (rung vs could-have, red
  under-ringing, DoW overlap from `usage.shops[].soloTok`), its best combo, and its Power Deals /
  Deal-of-the-Week sales (`deals.soldByLoc`). `shops_efficiency.py` reads it into `SE.combos` and
  renders a shop-selector panel; needs no extra Odoo queries. `_LAST_SHOP_TOK` also exposes the
  raw per-shop single-bag token sales.
- **Same-bag-two-offers hover** (`dowConns`): the tier label now marks whether that deal's tier
  is the **current** one (`· current`) or notes "now measuring Tier N", via `smcCurTier()`.

**Click-to-pin tooltips** (`wireDowHover`): the shop (`.dow-loc`) and category (`.dow-cat`)
tooltips can be **clicked to pin** — the tooltip stays open and becomes interactive
(`pointer-events:auto`) so you can read/click inside it (e.g. the inline combo notes); clicking
the same cell again, or anywhere outside, closes it, and hover still previews when nothing is
pinned. A hint line ("click to pin" / "pinned — click outside to close") shows the state.

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

- **Offer Sales vs Stock Guidance chart removed (Oct 2026).** Its **Sort** (`#smc-og-sort`) and **Stock**
  (`#smc-og-stock`) dropdowns now sit in the **Running combos** panel header and drive the running cards only.
- **Kenya till target cards removed (5 Oct 2026).** The last-month / this-month till target cards are
  no longer shown on the Kenya side (Sinza / Uganda keep theirs).
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

The resolver/matcher is the module-level `bag_classifier(on_offer_raw)` → `(infer,
is_on_offer)`, shared with the **Bags on vs not on offer** menu
([bags-on-offer.md](bags-on-offer.md)). `main()` also writes `bags_offer_source.json` —
the Kenya on-offer set tagged by offer (`payload["onOfferSources"]`: Combo component /
Deal of the Week / Power Deal) + `bagsNotOnOffer` — which `bags_on_offer.py` reads.

## Out of stock — call back

Who asked for each bag on WhatsApp while it was out of stock — per shop, per market.

**Source** — the Odoo **WhatsApp Monitoring** module (`denri_monitor_*`), via `lib/oos_callbacks.py`
(query: `sql/oos_callbacks.sql`). An **out-of-stock request** = a `denri_monitor_interaction` whose
reason has `is_out_of_stock` ("Out Of Stock"); the bags asked for are its
`denri_monitor_interaction_oos_product_rel` products plus `oos_product_id`, named by
`product_template.name`. Shops = `denri_monitor_shop` (rows with no `code` — webi / webs / sina / rong — are junk and skipped).

- **People, not requests.** One person = `phone_key`, else WhatsApp username, else the
  interaction itself; every number is **distinct people** for that bag (a customer who asked
  twice, or at two shops, counts once in the total and once per shop).
- **Periods** — `lifetime` (all), `monthly` (live report month), `weekly` (this Sun–Sat week to
  date), `lastweek` (previous complete Sun–Sat week), **`current` = still waiting** (any date,
  `is_purchased` not set — the live call-back list).
- **Bags are recorded from June 2026** — older OOS requests have no product, so Lifetime really
  starts in June 2026 (the hover says so).
- **Chip:** `📞 N asked` (`📞 N waiting` for Waiting now), hidden when 0. Hover **or tap** opens the
  per-shop list, high → low (`Hilton 4 · Thika 2 · …`), then **each colour asked for** with its own
  shops (`Black 63 — Ktda 23 · Eldoret 6`); an outside tap closes it.
- **Stock beside every shop (live Odoo on-hand):** each shop count carries that shop's current
  stock of the bag — at bag level in "By shop", and of **that colour** under "By colour"
  (`Mombasa 2 · 0 in stock`, red at 0, green above). Same bag/colour matching as the counts;
  stock is today's whatever the period. Website has no shelf (shows "online"); a shop with no
  stock code shows nothing. Data: `lib/oos_callbacks.attach_stock` over `lib/stock.odoo_stock_by_shop_code`,
  so `shops` / colour shops are `[shop, people, stock|null]`.
- **Offline:** if Odoo can't be read (and there's no cached copy) the block is empty and no chips show;
  the page still builds.

**On this page:** `SMC.oos = {kenya|sinza|uganda: {period: {bag: {total, shops}}}}`. Each Odoo product
is resolved to its catalogue bag with the page's `bag_classifier()` `infer` (longest prefix, promo
aliases — so colour shades fold into the bag), and markets follow the till scopes: **Kenya** = every
shop except Sinza / Uganda (Website included), **Sinza** = Sinza, **Uganda** = Uganda.
`SMC.oosAlias` maps a displayed bag name to its catalogue key when they differ.
Chips sit on every component bag of the running-combo cards (Kenya), the Sinza / Uganda guidance
cards (their market), and every row of the three **Bags not on offer** lists. The page has no period
dropdown, so a compact toggle — **Lifetime / Monthly / Last week / Waiting now** — sits by the combo
cards (remembered in this browser).
**Colours:** each bag entry carries `colours: [[colour, people, [[shop, people], …]], …]`, high → low;
the colour is the colour **family** (`lib/colours.family` — Maroon → Red, Choco → Brown), like every other colour on this page. A request whose product has no colour shows as "No colour".

## Sinza & Uganda — combos counted from receipts (Oct 2026)

**Offers list:** `offers_monthly.csv` — the month's Sinza (Tanzania) and Uganda singles + combos as the user
sends them: `Month · Market · Type (Single/Combo) · Name (as given) · Bags · Was · Now · Disc · Currency ·
Was KSH · Now KSH`. When it has rows for the live month they replace the COMBOS sheet's Sinza / Uganda
combos + singles (specials still come from the sheet). Transcription:
- Sinza singles: "PRICES BEFORE" KSH/TSH → Was, "OFFER PRICE" → Now (TSh). Sinza combos: the columns are
  offer KSH · offer TSH · **S.P** (TSh it sells at = Now) · was KSH · was TSH (= Was) · DISC (= Was − S.P).
  Uganda: was / now / disc in USh; the trailing number = the KSH equivalent of Now.
- **Bags** = catalogue bag types (`bag_classifier` infer), `+` between slots, `/` between alternatives:
  Bigman → BIG MAN BAG, Zane → ZANE MAN, Cairo → CAIRO BP, Mandy → MANDY HB, Standard → TRAVEL,
  Safiri → SAFIRI TRAVEL/SAFIRI BP, Sky → SKYE HB, Mistque → MYSTIQUE, Luna manbag → LUNA (not Luna
  Amapiano), Ari sling → ARIA SLING; `*SLEEVE` = any product with SLEEVE in its name.

**Receipt rule (`lib/receipt_combos.py`, corrected 4 Oct 2026).** Sinza (`sinza`, `dar-es-alam` tills) and Uganda
(`uganda`) ring every bag as its own line; a client printed out with more than one bag bought a combo. Per receipt
(state paid/done/invoiced; delivery / gift bags / non-bags ignored):
1. **Refunded receipts are dropped** (a `… REFUND` receipt cancels its original).
2. **≥ 5 bags = bulk** (e.g. 6 Monah backpacks) — reported apart, never a combo.
3. Bags at the **same unit price** (rounded to the nearest 10, so 40,000 / 40,001 match) = **one combo** per price
   (a 4-bag receipt at two prices = two combos).
4. The bags left over: **two or more = one combo** sold at different prices — Uganda splits a combo's price
   unevenly (Jumbo 115,000 + Big Man Bag 70,000); **exactly one = a single**.
A combo whose bag types fill a listed combo's slots (same count, **any order**, alternatives allowed) is
**running**; otherwise **self-made** (labelled by its bags, sorted). A single counts against a listed single
when its bag type matches. (Before the fix, unequal-price pairs were wrongly counted as two singles and
refunds and 5–6-bag receipts were included — Uganda showed 3 self-made instead of 9 for 1–3 Oct.)
Weeks are the month's Sun–Sat weeks (Wk 1 = the week holding day 1).

**On the page** each Sinza / Uganda region view shows the listed combos and singles as cards with
**POS-measured** weekly sold (not the sheet's), a **Self-made combos** list (combo · times · revenue),
and the bulk receipts line. `SMC.regions[r].receipts = {running, selfMade, singles, bulk, receipts}`.

### Sinza & Uganda — the Kenya-style view (Oct 2026)

Each region view opens like Kenya's **Self-made vs running combos** panel, but measured from the till
receipts (no Request Hub / CBR in those markets): two bars (combos sold, revenue — self-made vs running),
and cards **Self-made** (combos sold · distinct pairings · revenue; hover the number for *Sold as self-made
instead*), **Running** (same, plus *On the <month> list: N combos* and *Sold from the list: N units (x of N
listed have sold)*) and **Self-made share** of all combos sold. No separate list-summary card row. Below the running cards: the **repeating self-made combos** list (each bag mix ×
times, revenue) and **Bags clients keep pairing** — the bag types that recur most across that market's
self-made combos, whether each is in one of its listed combos, and its stock there.
Data: `SMC.regions[r].receipts` → `smTotals` / `runTotals` ({count, units, value}), `selfMade`, `topBags`.

**What people chose instead (on each running card).** Like Kenya's "shares … self-made" chip: a running combo
card lists, per bag of that combo, the **self-made combos that contained the bag** — e.g. SAFIRI + CODE 3 →
*Safiri Travel: Jade + Safiri Travel ×1, Remi + Safiri Travel ×1* — with times and revenue (KSh in brackets),
so you see what customers prefer to pair the bag with. **Combo cards only** — singles don't get the chip. Data: each Sinza / Uganda combo card's
`connections: [{bag, selfMade:[{name, qty, value}], smUnits, smValue}]`, `connUnits`, `connValue`, `connCombos`.

**Sale dates.** Every Sinza / Uganda self-made combo carries the days it was sold (`dates: [[YYYY-MM-DD, times], …]`,
from the receipt date) — shown as `3 Oct, 4 Oct ×2` beside the combo in the self-made list and in the
"What people chose instead" hover.

### Sinza & Uganda — last month vs this month (Oct 2026)

Like Kenya, each region view's offer panel has **no Sales vs Stock Guidance chart** — its **Sort** / **Stock**
dropdowns sit in the panel header and drive the cards — and opens with a **target block**:
- **Combos — target to beat last month:** last month's combos sold (running + self-made, from that month's
  receipts, same receipt rule) vs this month so far, the weekly pace needed over the weeks left, and a weekly
  line chart (this month solid vs last month dashed; hover a week for the combos that sold).
- **Till target (Odoo `sales_pos_target`, monthly, `DAR-ES-ALAM` / `UGANDA`):** for last month and this month —
  the target (KES and bags) vs what the till actually sold (bags; revenue converted to KSh with `FX_PER_KSH`),
  as % of target; this month also shows the pace needed per day.
Data: `SMC.regions[r].goal` (Kenya's `combosGoal` shape) and `SMC.regions[r].tillTarget = {prev, cur}`.

### Kenya shillings beside TSh / USh

Every money figure on the Sinza and Uganda views shows the local amount with Kenya shillings in brackets —
`TSh 128,000 (KSh 5,120)`, `USh 172,500 (KSh 4,929)`. Rates = the user's own price lists
(`SMC.fx`, `FX_PER_KSH` in self_made_combos.py): **25 TSh = 1 KSh** (TSh 42,500 ↔ KSh 1,700) and
**35 USh = 1 KSh** (USh 76,500 ↔ KSh 2,186). Change the rate there when the lists change.

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
- **"SEPT COMBOS 0" / empty Offer Sales vs Stock Guidance** (fixed 24 Sep 2026): the COMBOS
  sheet was edited so the `KENYA` marker sits on its own row (`KENYA | PRICE`) with the
  `SEPT COMBOS` header one row below. `offer_data.py` expected the marker ON the header row, found
  no section title and read 0 combos. `header_at_or_below()` now steps down (up to 3 rows) to the
  first row carrying a section keyword — for KENYA, SINZA and UGANDA alike.
- **`offer_type_analysis` is fully retired** — the Monthly Report reads combo/offer data
  from the `OFFER_DATA` block this page writes.

## Regenerate

```
python self_made_combos.py        # DENRI_LAUNCHER=1 to skip the browser tab
```
Reads Odoo + the deals/COMBOS sheets; rewrites the `SMC_DATA` and `OFFER_DATA` blocks.
</content>
</invoke>
