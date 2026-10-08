# Bags on offer vs not on offer

- **Generator:** `bags_on_offer.py` (reads `bags_offer_source.json`, written by `self_made_combos.py`)
- **HTML:** `bags_on_offer.html`
- **Data markers:** `<!-- BOO_DATA_START -->…<!-- BOO_DATA_END -->` (const `BOO`)
- **Scope:** **Kenya only** (every till except `sinza`, `dar-es-alam`, `uganda`), plus Kenya
  corporate invoices.

A new metric **next to** Menu 4 — it does **not** replace anything there. The Self made combos
page keeps its Combos / Power Deals views and its own "Bags not on offer" panel unchanged.

## Period selector (Monthly / Weekly / Last week / Custom)

A **Period** dropdown (top right, same wording as New Products) switches the whole page. All three
are pre-computed by the generator into `BOO.periods.{monthly, weekly, lastweek}`:

| Period | Window | Trend chart | Odoo target used |
|---|---|---|---|
| **Monthly** | the live report month (`report_month.live_month_window()`), to date | revenue per Sun–Sat week | `period = 'month'` |
| **Weekly** | the current Sun–Sat week, to date | revenue per day | `period = 'week'` |
| **Last week** | the previous complete Sun–Sat week (may straddle the month boundary) | revenue per day | `period = 'week'` |
| **Custom** | any From – To dates you pick (up to 366 days; both days included) | revenue per day (≤ 31 days) or per Sun–Sat week | each overlapping `period = 'month'` target × the share of its days inside the range |

**Custom range.** Pick it in the **Period** dropdown itself: **Custom range…** (or **Change range…**) opens a
From / To picker (quick picks: last 7 / 30 days, last month, this month). Apply saves the dates to
`boo_custom_range.json` (`{"from", "to"}`) and rebuilds the page from Odoo; the dropdown then shows
**Custom (dd Mon – dd Mon)** and selects it. (The separate date bar above the page was removed Oct 2026 —
[README › Custom range](README.md#custom-range-oct-2026).)
The range stays (auto-refresh keeps rebuilding it) until a new one is applied or **Clear** is
pressed (deletes the file). Locally: `python bags_on_offer.py 2026-09-15 2026-10-03` (or
`python bags_on_offer.py clear`). Days of any month whose offer list is archived
(`bags_offer_source_<YYYY-MM>.json`) use that month's list; other months fall back to the
current month's list (the build log says which). The Offer type › weekly split stays Monthly-only.

**Each sale is judged by the offers of its own month.** A window that straddles the month boundary
(Last week = 27 Sep – 3 Oct) classifies the September days with September's offer list (Power
Deals, Deal of the Week runs + weeks, combo components) and the October days with October's. Every
month's list is archived as `bags_offer_source_<YYYY-MM>.json` (written by self_made_combos.py
alongside `bags_offer_source.json`); if the previous month's archive is missing, those days fall
back to the current month's list. Deal-of-the-Week week numbers count from each month's own
Sunday anchor.

The chosen period is remembered per viewer (browser storage). Stock / days-of-cover on the
not-on-offer table are point-in-time (today's stock, this month's selling pace) in every period.

## Buckets

Every Kenya POS line in the window (returns netted, `qty <> 0`; delivery, customisation and
straps excluded) and every qualifying corporate invoice line falls into exactly one bucket:

| Bucket | Rule | Tag |
|---|---|---|
| **On offer** | a combo product (`name LIKE '%+%'`) — running *and* self-made, rung on the combo button | `Combo sale` |
| **On offer** | a single bag sold inside a **timed offer** campaign, or that resolves to a bag that is a **running-combo component**, a **Deal of the Week** or a **Power Deal** | `Timed offer` / `Combo component` / `Deal of the Week` / `Power Deal` (several allowed; money counted **once** — see *Counted by how it was sold*) |
| **Not on offer** | a single bag that resolves to a catalogue bag on no offer | — |
| **Not on offer** | a **new product** (MONTHLY_TARGET sheet, col I ✅ — the New Products list) that is on no offer, **even if it isn't in the price catalogue yet** (e.g. LaFemme) | `NEW` |
| **Others** | **gift bags** (POS `name ILIKE 'gift bag%'`), **samples** (`SAMPLE…`) and **corporate** sales (customer invoices, same qualifying rule as `sql/corporate_bags.sql`: posted `out_invoice`, paid / in payment or ≤25 % outstanding; product lines; `price_total`) | `Gift bags` / `Samples` / `Corporate` |
| **Unclassified** | a single POS product that matches no catalogue bag and no new product | footnote count/revenue |

- A new product that **is** on an offer (Sep 2026: **Lola** — combo component, **Zoezi** — deal)
  stays **on offer** (its sales are offer sales) and carries the `NEW` tag there.
- The on-offer set and the bag resolver are the ones Menu 4 uses: `self_made_combos.py` exports
  `onOffer` (= `kenya_on`: `comboBags` + DoW + Power-Deal products) to `bags_offer_source.json`, and
  both pages classify with the shared `bag_classifier()`. So the Monthly not-on-offer revenue equals
  Menu 4's `SMC.bagsNotOnOffer.notOnOfferRevenue` **plus** the new products Menu 4 can't resolve
  (the generator prints both figures).
- **Deals guard:** if the on-offer source has **no Power Deal and no Deal of the Week** bags (the
  deals sheet failed to load — the 25 Sep 15:55 build lost ~KES 3M of on-offer money this way,
  all of it shown as combo bags or not on offer), the source is rebuilt live once; if it is still
  deal-less the build stops and bags_on_offer.html is left unchanged. For a month that genuinely
  has no deals, run with `BOO_ALLOW_NO_DEALS=1`.
- New-product list: read from the sheet at build time; if the sheet can't be read, the list from
  the previous build (`BOO.newProducts`) is reused.

## Counted by how it was sold

Every sale is counted **once**, in the channel it actually went through (agreed Sep 2026):

- **Printed inside a combo** (rung on the combo button) → the **Combo sales** row — whatever
  else the bag is on. E.g. Sep 1–24: **367 Jumbos** were printed inside combos (290 in
  Jumbo + Jumbo, 77 in Jumbo + Standard/Liam + …) → Combos.
- **Sold singly** → the offer the single sale belongs to, in this order:
  **Timed offer → Power Deal → Deal of the Week → Combo bag sold singly**, and if none applies → **not on offer**.
- **Timed offer** (added 27 Sep 2026) = a single-bag sale inside a campaign from
  `timed_offers_config.json` (the Timed Offers menu), matched **per till line** with that menu's
  own filters (`timed_offers._shop_sql / _time_sql / _price_sql / _name_sql`): its **shops**
  (empty = all Kenya), **dates** (from `clearanceStart` when set — the day the clearance really
  began), **hours** (`startTime`–`endTime`, Nairobi time) and **bags** (`bags` resolved with
  `bag_classifier`; a `nameLike` offer such as `[REJECT]` takes every matching bag instead).
  It comes first because the campaign is how the sale was actually priced. A line in two
  overlapping campaigns counts once, for the first in the config. Sep 2026: *KES 300 Off — Bags
  Not On Offer* (CBD 10–11 Sep; all Kenya 4–7 pm 11–12 Sep) and *Kitengela Rejects* (from 18 Sep).
- The **KES 300 discount** till line ("300.0 KES DISCOUNT ON TOTAL AMOUNT") is a general reward
  rung all month at almost every shop, not the timed offer's discount — it stays **Unclassified**.
  A sale is a **Deal of the Week** sale only if it happened **at a shop running that deal, in its
  tier's weeks** (Tier 1 = Wk 1–2, Tier 2 = Wk 3+; `dowRuns` in `bags_offer_source.json`). A DoW
  bag sold elsewhere / at another time is not a deal sale — e.g. Jumbo sold at Hilton counts as a
  combo bag sold singly, Kai sold outside its deal shops/weeks is not on offer. A Power Deal runs at every shop
  all month, so a single sale of a bag that is both (e.g. Jamela) is a Power-Deal sale; the
  722 single Jumbos (a Deal of the Week + combo bag) → Deal of the Week.
- The rows of *Where the on-offer money comes from* therefore sum exactly to the on-offer total.

**Bags printed inside combos** come from Odoo's combo **sub-lines** (`sub_product_line = true`):
one line per bag inside every combo, with the exact colour variant and a KES 0 price — they cover
every combo exactly (Sep: 2,053 bags across 946 combo orders). Sub-lines are therefore **excluded
from single sales** (else each combo bag counted twice). Combo **returns** have no sub-lines, so for a
returned combo the bags come from `combo_product_attribute_values` (padded to the combo's bag count,
name split on `+` if empty). Units only — combo **money** stays on the combo line in Combo sales.

**Colour coverage (audited 25 Sep 2026):** every product variant resolves to its bag — colours,
finishes (CRACKED, SPICE, WOOVEN, CHOCO, CN, ANTELOPE, PATTERN), `[REJECT]` clearance variants and
`[S_0]`-style codes. New products are matched on every variant too (e.g. Lamora Black / Brown /
Red / Sky Blue; LaFemme's four colours exist in Odoo, created 21 Sep, none sold yet). Laptop sleeves and
samples are counted as sales under **Others** (added 25 Sep 2026); only foam cleaner, the 300-KES
discount reward and a couple of one-off items (Enzo, KCB briefcase) stay unclassified.

## What the page shows (per period)

**Sidebar** ([page sidebar](README.md#page-sidebar)) — sections only (Money per week … Bags not on offer). No picker: the region chips here are Kenyan sales areas that filter the shops table, so they stay beside it.

1. **Money KPIs** — on-offer, not-on-offer and others revenue (KES) + units; on-offer share of
   all revenue; average price per unit (on vs not on offer); under-performing shops.
2. **Trend** — on offer / not on offer / others revenue per week (Monthly) or per day (weekly periods).
3. **On-offer breakdown by source** — Combo sales / Deal of the Week / Power Deal / combo bags
   sold singly — counted by how it was sold (above). Bar length is relative to the largest row.
4. **Offer type summary** (below) — one matrix of offer type × category group × tier.
5. **Shops by region** vs their Odoo target (below). Gift bags show in each shop's **Others** column.
   A **By region / All shops** toggle (remembered per browser): *By region* groups shops under
   their region (with the region filter buttons); *All shops* is one table of every shop with a
   **Region** column, ranked by pace (no-target shops last, then by revenue). Badges are unchanged.
   All shops has filters — region, status (red / amber / green / no target), shop search — and
   click-to-sort headers; **#** stays the Kenya-wide pace rank whatever the filter or sort.
6. **Bag tables** — on-offer bags: offer tags, `NEW`, **in combos** (units printed inside combos),
   **sold singly** (units), which row the singles count in, and singles revenue. Not-on-offer bags:
   `NEW`, sold singly, in combos (self-made combos), revenue, stock, days of cover.
   Both tables have a **Tier** column — a coloured tag per bag (**Premium** violet, **Core** blue,
   **Entry** green, dim **No tier**), from `bag_tiers.csv` (each `onBags` / `offBags` row carries
   `tier` + `category`) — with a **Tier** filter, and it sorts Premium → Core → Entry → No tier.
   Both tables sort by clicking a header (default revenue high→low; blanks always last) and filter
   by bag search + `NEW` only. On-offer adds an **Offer** filter (Power / DoW / Combo); not-on-offer
   adds **Stock** (30+ / 1–29 / out), **Cover** (<14 / 14–90 / >90 days) and **DoW elsewhere**.

## Laptop sleeves are bags (27 Sep 2026)

Any product with **`LAPTOP SLEEVE`** in its name (incl. *Handled Laptop Sleeve…*) resolves to the
bag **LAPTOP SLEEVE** (category BRIEFCASE) and is counted like any other bag — **not on offer**
unless an offer covers it. It is no longer an *Others* group.

## Offer type summary (matrix)

Every sale in the period lands in exactly one **offer type** row (same money as the buckets, so
the rows add up to on + not on + others):

| Row | What it holds |
|---|---|
| NOT ON OFFER | the *Not on offer* bucket |
| POWER DEALS | single sales counted as Power Deal |
| COMBOS | combo-button sales **+** combo bags sold singly |
| DEAL OF WK | single sales counted as Deal of the Week |
| MID-MONTH / OTHERS | timed-offer sales **+** samples |
| GIFT BAG | gift bags |
| CORPORATE | corporate invoices |

Columns (revenue / units / share toggle): **All**, **Top 5 categories**, **Other 13 categories**,
**Premium**, **Core**, **Entry**, and **Unassigned** when anything has no category / tier.
- **Category** of a bag: `bag_tiers.csv` (`CATEGORY`) when set, else the offer sheet's category
  (`offer_picking._read_offers` + `reject_sales._category_of`: aliases, then name keywords). The 18
  categories are the offer sheet's `bag_names` list: BABY BAG, BACKPACK, BRIEFCASE, CHEST BAG,
  GIFT BAG, HANDBAG, HOOD, LUNCH BAG, MAKE UP, MAN BAG, MESSENGER, SCHOOL BAG, SLING, SPORT,
  THIGH BAG, TRAVEL, WAIST BAG, WASHBAG.
- **Top 5** = the 5 categories with the most revenue **in the selected period**; **Other 13** = the
  rest of the 18. Hovering a header lists its categories.
- **Tier** of a bag comes from its **price** (`bag_tiers.csv` › `PRICE`, KES; price list of 5 Oct 2026),
  the same rule as the sheet formula `=IFS(B3<=2000,"Entry",AND(B3>=2001,B3<=3000),"Core",B3>3000,"Premium")`:
  | Price (KES) | Tier |
  |---|---|
  | ≤ 2,000 | **Entry** |
  | 2,001 – 3,000 | **Core** |
  | > 3,000 | **Premium** |

  Change a bag's tier by editing its PRICE; the `TIER` column is written alongside for reading and
  is used only for a bag with no price (LILY, STANDARD — Unassigned until priced). CODE 3 BP takes
  CODE 3's price, LAPTOP SLEEVE takes SLEEVE 1's. GIFT BAG (KES 250) is Entry.
- **Three tabs** (27 Sep 2026). A shared Revenue / Units / Mix % toggle and an **Offer types**
  filter (chips — show / hide any offer type; totals and Mix % recompute over the ones shown)
  drive all of them; tab, filters and toggle are remembered in the browser.
  - **Offer type** —
    - *Offer mix by period*: stacked bars + **By period** table for **Monthly, Weekly, Last week**,
      with a **Periods** filter (pick any of the three; the page's selected period is highlighted).
    - *Weekly breakdown*: Wk 1 … the current week (Sun–Sat weeks, clipped to the month, same as
      the trend chart), from `periods.monthly.offerTypesByWeek`: stacked chart + table with a
      **Weeks** filter; the change column compares the **first and last week picked** (absolute
      and %). **Totals / Per day** divides each week by its days so far, so a part-week compares
      fairly.
    - *Week 1 → latest week*: grouped bars per offer type — the first picked week beside the last
      (default Wk 1 vs the current week), each bar labelled with its number and the change
      (▲ / ▼ %) above the pair; a Total pair on the right. Same filters and switches as above.
  - **Numbers on the bars:** the Offer type tab's charts print each segment's value inside it
    (when the segment is big enough to hold it) and each stacked bar's total above it.
  - **Category** — for the page's selected period: the 18 categories ranked by revenue (Top 5
    tagged), each split by offer type — stacked chart + table (total, share). Mix % = each offer
    type's share within the category.
  - **Tier** — a **Tier → Category → Bag** tree (like the tier pivot), for the selected period:
    Premium / Core / Entry / No tier, each expanding to its categories, each to its individual
    bags, with every level split by offer type (+ total, share) and a stacked chart per tier.
    Each **bag row carries its offer tags** (Timed / Power / DoW / Combo — the same pills as the
    on-offer bag table). Data: `offerTypes.tree` = `{row: {"tier|category|bag": {units, revenue}}}`. Bags without a
    tier in `bag_tiers.csv` sit under **No tier** — the tree shows exactly which ones.
- **A combo is one sale:** *Jumbo + Jumbo* rung on the combo button is **1** combo sale (1 unit in
  the Combos row, its money once) containing **2** bags (the bag tables' *In combos* count 2). For
  category / tier / bag its money and unit are split evenly over its slots (½ + ½ to JUMBO).
- **Checked 27 Sep 2026** against independent SQL (`pos_order_line` / `account_move`): every row
  (Combos' combo-button part, Gift bag, samples + timed = Mid-month, Corporate) and every
  period / week total matched to rounding (≤ KES 15); category and tier columns each sum to the
  total; the Top 5 are the 5 highest-revenue categories; Last week = Wk 4.
- A **combo sale** is split evenly across its slots (each slot's bag → its category / tier).
  **Corporate** and **samples** have no bag, so they sit in **Unassigned**.

## Shop metrics (vs the Odoo revenue target)

- **Target:** `sales_pos_target`, `target_scope = 'pos'`, `period` = month or week (see the period
  table), latest row whose `start_date…end_date` overlaps the window; `config_id → pos_config.name`.
- **Corporate** gets its own row (region **Corporate**) against the `target_scope = 'corporate'`
  row of the same period; its revenue is the corporate invoices above.
- **Revenue vs target:** the shop's **total till revenue** in the window (all POS lines,
  `SUM(price_subtotal_incl)`, returns netted) — the target covers the whole till.
- **Attainment %** = revenue ÷ target. **Pace %** = revenue ÷ (target × days elapsed ÷ days in the
  period) — Last week is complete, so its pace = attainment.
- **Region:** till name → shop label (`_SHOP_TO_LOC`) → region from [shop-regions.md](shop-regions.md);
  sorted by pace; best pace = **Region leader**.
- **Red = under-performing:** pace **< 100 %** **and** below its **benchmark** — the region's pace
  (2+ targeted shops) or the Kenya-wide POS pace (one-shop regions: Coastal, Online, Corporate).
  Behind target alone flagged every shop mid-month (Sep 2026 day 24: all 17 at 43–81 %).
- **Amber** = behind target but at/above its benchmark; **green** = pace ≥ 100 %. No target row
  (Staff Pos, Jumia) → "no target", never red; tills not in shop-regions.md → **Other**.

## Out of stock — call back

> **Online + walk-in (Oct 2026).** The demand now comes from **two** Odoo modules, split everywhere:
> **Online** = WhatsApp Monitoring (below; bag recorded from Jun 2026) and **Walk-in** = the **leads module**
> (`denri_lead`, `sql/oos_walkin.sql`): leads whose status **is or ever was "Awaiting stock"** (the status history
> is read from the chatter, `mail_tracking_value` — 431 leads moved Awaiting stock → Purchased by Oct 2026), from
> Jan 2026. Lead branches map onto the WhatsApp shop names (KTDA SHOP → Ktda, DAR-ES-ALAM → Sinza, WEBSITE SALES /
> JUMIA → Website, Flash Sale tills → their shop; Marketing / Shoot / Staff POS / Rejects dropped); a lead's person
> = last 9 phone digits (same key as WhatsApp, so someone who asked in both counts once in the total), else
> name@shop, else the lead. "Still waiting" for a walk-in = status still Awaiting stock. A free-text lead bag takes its
> colour when one is given ("MINI MAYA" + Black). The chip reads **📞 24 asked · 7 online · 17 walk-in**; the
> popover adds Online / Walk-in totals and tags every shop and colour (`Hilton 6 · 1 online · 5 walk-in · 42 stk`).
> Data per bag: `online`, `walkin`, `shopCh {shop: [online, walkin]}`, and a 4th item on each colour
> `{shop: [online, walkin]}` (`lib/oos_callbacks.py`, `oos_chip.js`). Mis-picked lead products (e.g. "Ajab
> Homebaking Flour", "Drawer Repair") never match a bag, so they drop out.
> **Net counts (Oct 2026):** every 📞 number is **people still waiting** — asked in the period and **not bought
> since** (WhatsApp `is_purchased` unset / lead still "Awaiting stock"); people who bought drop out. Chip:
> `📞 12 waiting · 2 online · 10 walk-in`; popover header: `12 still waiting · 15 asked, 3 already bought` (entry
> `asked` = gross). The separate **"Waiting now"** toggles were removed (redundant). On Combos the Marketing guide's
> 📞 and "remind all N" are the same number.
> **Call now vs waiting (Oct 2026):** a still-waiting client counts as **📲 call now** when their bag is in stock at
> the shop where they asked. If they named a colour, that colour must be in stock there. Everyone else stays **📞 waiting**
> (no stock at their shop yet). A person is "call now" if any of their requests for that bag is in stock. Entry
> `callNow` = those people (`lib/oos_callbacks.attach_stock(..., rows=…)`). The chip reads **📲 11 call now · 📞 1
> waiting** when anyone can be called. Otherwise it stays as before (**📞 N waiting · online · walk-in**). The popover
> header repeats the split, and the online / walk-in totals stay in the popover. Example (8 Oct 2026): all 12 Amaya
> clients asked at shops that hold Amaya (Hilton 21, Starmall 11, Mombasa 25 …), so 11 are "call now" and 1 is still
> waiting (Thika, Black: 0 there).
> **Popover (8 Oct 2026):** hover or tap a bag's 📞 chip for the full popover: the call-now / waiting header and what
> "call now" means, the "N asked, M already bought" line, the Online / Walk-in totals, By shop (with stock) and
> By colour, then the source note.
> **Any colour:** a request that names no colour (e.g. a lead that just says "Amaya") can take **any** colour. The
> popover lists it as **"Any colour"**, and each shop's stock there is the bag's stock in **every** colour (Hilton
> Amaya 21 stk), not stock with no colour. Internally the group is still keyed "No colour". Call-now uses the same
> rule (any colour in stock).
> **Combo requests:** a request whose product names a whole combo (contains "+", e.g. "Amaya Handbag or Elyse
> Handbag + Moon Bag or Nizana") is **not** counted on any single bag. It counts only on that combo's
> "📞 clients to convert" chip (Combos page). The bag matcher used to file it under the first bag (Amaya).
> **Long popovers scroll:** the pointer can move from the chip onto the popover (220 ms grace) and it stays open
> while hovered, scrolled or clicked inside; scrolling the page or moving away closes it.

Who asked for each bag on WhatsApp while it was out of stock — per shop.

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

**On this page:** `BOO.oos = {period: {bag: {total, shops}}}`, keyed exactly like the `onBags` /
`offBags` rows — the page's own `base()` classification (`bag_classifier` infer, laptop sleeves,
new products), so colour shades fold into the bag. **Kenya only**, like the page: Sinza and Uganda
requests are left out (Website stays — it's a Kenya till). Both bag tables get a sortable
**Call-backs** column (the chip). It follows the **Period** dropdown (Monthly / Weekly / Last week);
a **Waiting now** toggle switches the column to `current`.
**Colours:** each bag entry carries `colours: [[colour, people, [[shop, people], …]], …]`, high → low;
the colour is the colour **family** (`lib/colours.family` — Maroon → Red, Choco → Brown). A request whose product has no colour shows as "No colour".


## Shop birthdays

Opening anniversaries from [shop-birthdays.md](shop-birthdays.md) (shown from 30 days before to 1 day after): a 🎂 badge beside the shop name in the shops table (`BOO.birthdays`).

## Regenerate

```
python self_made_combos.py    # writes bags_offer_source.json (on-offer set + not-on-offer list)
python bags_on_offer.py       # DENRI_LAUNCHER=1 to skip the browser tab
```
If `bags_offer_source.json` is missing or older than 15 minutes, `bags_on_offer.py` rebuilds it
live by running `self_made_combos.fetch()`.

## Layout (laptop / tablet / phone)

- **Laptop (> 820px):** full tables; the six KPI cards sit in one row; the two bag tables are
  stacked full-width (side by side they were too narrow — columns were cut off).
- **≤ 820px (tablet, narrow window, Streamlit with the sidebar open on a small laptop):** every
  table (`table.rt`) turns each row into a labelled card (`td[data-label]`), 4 values per line on a
  tablet, 2 on a phone — nothing scrolls sideways. Under-performing shops keep the red card.
- **≤ 700px (phone):** KPI cards 2 per row, tighter padding/fonts, shorter chart. The bag lists
  keep their own scroll (36rem) so the page doesn't become endless.
- Stock / days of cover are filled for **every** not-on-offer bag from `stockMap` in
  `bags_offer_source.json` (Kenya stock, sheet + Odoo live) ÷ this month's pace on the days the bag
  sold (single sales + combo prints).
- Check changes at 390px in a real narrow frame — headless Chrome won't shrink a window below
  ~500px, so a plain `--window-size=390` screenshot is cropped, not reflowed.
