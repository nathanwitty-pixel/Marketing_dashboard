# New Products Analytics

- **Generator:** `new_products.py`
- **HTML:** `new_products.html`
- **Data marker:** `<!-- NEW_PROD_DATA_START -->…<!-- NEW_PROD_DATA_END -->` (const `NP`)
- **State file:** `new_products_weekly_history.json` (per-week posts/sales snapshots)

## What the page shows

**Sidebar** ([page sidebar](README.md#page-sidebar)) — one entry per block — Overview, Weekly Sales vs Marketing Posts, Weekly Performance, Sales by Shop, Sold vs Remaining to Target, Top 10, Colour Movement & Stock Guidance.

Per new-product KPIs (target vs sold vs deficit), monthly and weekly sales split
Kenya vs Outside, marketing posts, stock levels, a weekly-sales-vs-posts chart, and a
lifetime tally. **The product LIST + TARGET come from the sheet; every SOLD figure comes
from Odoo** (falls back to the sheet only if Postgres is unreachable).

## Data sources

Spreadsheet `1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0`:

- **MONTHLY_TARGET** — col A bag, C target, D sales, E deficit, **col I flag** = is a new
  product. Only flagged rows become cards.
- **MONTHLY_SALES / WEEKLY_SALES** — colour-level rows (colour / category / product /
  bag type + sales columns). Sales are **overwritten** by Odoo.
- **MONTHLY_MARKETING_POST / WEEKLY_MARKETING_POST** — col E Kenya posts, col H Outside.
- **Stock (live Odoo on-hand, `lib/stock.py`; the STOCK_LEVELS sheet is not read):**
  **Kenya Stock** = the 16 Kenya shop locations (`KENYA_SHOP_CODES`);
  **Sinza+UG Stock** = DAR (Sinza) + UG (Uganda); **Restock** = the exact location
  `CBD/Stock` (`RESTOCK_LOCATION`, via `odoo_stock_at_location()`). Restock was 0 before 28 Sep 2026.

Odoo:

- `odoo_month_product_bags()` / `odoo_lifetime_product_bags()` — bags per product
  (`queries.WEEKLY_BAGS_SOLD`, grouped by `full_product_name`) for the report month and
  all-time. `match_odoo_bags()` sums by name prefix.
- `odoo_sales_window(start,end)` — `{UPPER(name): {kenya, outside}}` for a window, used to
  replace the sheet's monthly / this-week / last-complete-week sales.

## Matching (`match_odoo_bags`) — the `[S_0]` fix

> Full matching reference: [product-matching.md](product-matching.md).

Sold figures match a new product to its Odoo variants by **name prefix**
("LAMORA" → "LAMORA BLACK", "LAMORA SKY BLUE"…), being careful that "AMORA" does not catch
"LAMORA".

**Odoo prepends an internal-reference code to some `full_product_name` values**, e.g.
`[S_0] Lamora Sky Blue`. The matcher strips a leading `[...]` code before the prefix test
(`re.sub(r"^\[[^\]]*\]\s*", "", p)`) — without it, that variant is silently dropped.
This once cost Lamora 4 units this month (10 vs 14) and 38 lifetime.

> Note: New Products counts `full_product_name` sales via `_BAGS_WHERE` (reward/strap/gift
> lines excluded) **plus** the bags inside combos (sub-lines, added by
> `odoo_combo_product_bags()` — see *Odoo sales window* below).

## Per-product chart (Sold vs Still needed) — targets per period

The target the bars are measured against matches the **Period** selector:

| Period | Sold so far | Target / Still needed |
|---|---|---|
| Monthly | month-to-date sold | the product's **monthly** target (MONTHLY_TARGET col C) |
| Weekly | this Sun–Sat week's sold | **weekly** target = monthly target ÷ `perfectWeeks` (same rule as the *Weekly Target* card) |
| Last week | previous complete week's sold | **weekly** target, as above |
| Lifetime | all-time sold | monthly target (reference only) |

**% sold** (Oct 2026) = sold ÷ that period's target, rounded. It sits after the target at the end of each
bar (`262 · 5%` — green ≥ 100 %, amber ≥ 50 %, red below), in the hover footer, and as **% sold** in the
totals row (total sold ÷ total target). The **Sort by** dropdown has **Highest % sold**. Lifetime % is
against the monthly target, so it is reference only.

**Tiles view** (Oct 2026, the default **View**; Bars and Trend line still there): one KPI tile per product
in the **Sort by** order — **% of target sold** (big, coloured like the bar label), `sold of target`, a
progress bar, still needed, posts (— for Weekly / Lifetime), KE stock, Sinza+UG stock, and a **rank badge
by % of target sold**. Hover / tap a tile: sold · target · still needed · % sold, posts, stock (Kenya shops,
Sinza+Uganda), people who asked while out of stock (`NP.oos`, same period) and **what to do** (target
reached → keep it moving; no stock → restock first; stock below still needed → restock while pushing;
else push it, and post it more when < 3 posts).

(Before 25 Sep 2026 the Weekly / Last-week views compared one week's sales with the whole
**monthly** target — e.g. Loop BP "32 sold · 190 still needed of 222" for last week, which
read as far behind when 32 vs a weekly share of ~55 was the real picture.)

## Odoo sales window (`odoo_sales_window`) — same rules as the monthly total

The per-colour monthly / this-week / last-week figures come from `odoo_sales_window`. It uses
the **Nairobi-local order date** (`date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi'`)
and order states **done / invoiced / paid**.

**Bags sold inside combos count** (decided 28 Sep 2026). A new bag sold in a combo is still a
sale of that bag, so every period includes the combo **sub-lines** (`sub_product_line` — one
line per bag inside the combo, exact colour, KES 0); only the combo line itself
(`is_combo_line`, e.g. "Zula + Antitheft Combo") is left out. The product totals
(monthly Sold, Lifetime) add the same sub-lines via `odoo_combo_product_bags()` on top of
`queries.WEEKLY_BAGS_SOLD`, so per-colour and per-product figures agree. E.g. last week
(20–26 Sep) Zula = 24 standalone + 2 in combos = **26**; Voyage = 0 + 1 = **1**.

**Invoiced orders count.** A till order re-rung as an invoice has state `invoiced`, not
`done` — e.g. HAZINA/29593 (Amora Black, 26 Sep) was refunded and re-rung as HAZINA/29594
(`invoiced`); a done/paid-only filter nets the pair to 0 and drops the sale (Amora showed 1,
really 2). All POS queries in the repo now use `('done', 'invoiced', 'paid')`.

## Month / week windows

- Monthly = `report_month.month_window()` (the report month).
- Weekly = the current Sun–Sat week to date; **last week** = the previous complete Sun–Sat
  week (`lastWeekKenya/Outside/Total/Pct`) — powers the "last week's performance" hover on
  the Weekly Sales vs Marketing Posts card (useful for Mon–Wed presentations).
- Lifetime = open range `2000-01-01 … today` (labelled "Lifetime" — the only deliberately
  all-time figure on the page).
- Week numbering: the opening partial week = Wk 1 (`_np_perfect_week_index`).

## KPI card layout

All five KPIs sit in **one `card-grid`**, arranged like the Current Performance page: **Monthly
Sales** is the `primary` card (spans two columns via `.card.primary`, larger value), followed by
**New Products · Sales % Achieved · Weekly Target · Weekly Sales % Achieved** — no sub-header
splits them. The **new-product name tags** (`#product-tags`, from `NP.productNames`) live **in
the New Products hover popover** (`#np-target-popover`, which also shows Monthly Target) — hover
the New Products card to see the list; the card itself says "· hover for the list". Each card
keeps its hover popover (deficit, monthly target + product list, Kenya/Outside split, weekly
posts & stock, weekly sales & restock). No sparklines on the tiles. The **Weekly Sales vs
Marketing Posts** sub-header now heads the Weekly Performance chart section below, not the cards.

## Weekly Performance chart (Week 1 → latest)

In the **Weekly Sales vs Marketing Posts** subsection, a Current-Performance-style chart +
table (mirrors the [Current Performance](current-performance.md) weekly panel). Chart: each
week's **Weekly Sales % of the weekly target** as an amber line with value labels, **this
month only** (no last-month dashed line). Table columns: Week · Sales % Achieved · Sales Bags
(▲ green if it cleared the weekly floor, red if short) · Target to Beat (`weeklyTarget`) ·
Declined By (`weeklyTotal − weeklyTarget`) · **Kenya Posts · Outside Posts** (the marketing
effort behind each week). Fed by `NP.weeklyPostsHistory` **filtered to the current month by
each entry's `month` field** (not `weekStart`, so the Aug-starting opening week of a month is
attributed correctly) and `NP.weeklyTarget`.

**One rule for every weekly figure (28 Sep 2026):** weekly sales = **Kenya + outside**, same
counting as everywhere else (bags in combos, invoiced orders), so a week shows the **same bags
and %** in the table, the chart, the Weekly Sales % KPI (this week) and the last-week popup /
footer (`lastWeekPct`). Before this the history was Kenya-only and frozen when the week ran
(Wk 4 showed 48.89% / 88 bags in the table vs 51.67% / 93 bags in the popup).
- **This month's weeks are recalculated live from Odoo on every run** (not frozen), and their
  `pct` recomputed; earlier months' rows stay as stored.
- **Posts a week in arrears:** WEEKLY_MARKETING_POST (read now) is the **last complete week's**
  posting, so it is written to that week's row; the current week's row carries 0 posts.

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
> **Long popovers scroll:** the pointer can move from the chip onto the popover (220 ms grace) and it stays open
> while hovered, scrolled or clicked inside; scrolling the page or moving away closes it.

Who asked for each new product on WhatsApp while it was out of stock — per shop.

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

**On this page:** `NP.oos = {period: {product: {total, shops}}}`, one entry per product card
(`productTargets[].name`), matched with the page's own prefix rule (`match_odoo_bags`: the Odoo
name equals the product or starts with it + space/hyphen, `[S_0]` codes dropped) — **colour shades
are kept** (no family fold). All shops (Kenya + outside). The chip sits on each product card and
follows the **Period** dropdown (Weekly → `weekly`, Last week → `lastweek`, Monthly → `monthly`,
Lifetime → `lifetime`); a **Waiting now** toggle switches every chip to `current`.
**Colours:** each bag entry carries `colours: [[colour, people, [[shop, people], …]], …]`, high → low;
the colour is the **exact colour** as the product is named (`_odoo_colour`, e.g. `CN Black`) — New Products never folds shades. A request whose product has no colour shows as "No colour".

## Top 10 Products — Tiles view (Oct 2026)

Top 10 colour-level products (`NP.monthlyCombined` / `NP.weeklyCombined`) by sold for the **Period**
(Monthly / Weekly / Last week). **View** = **Tiles** (default) · Bars · Trend line. Each tile: rank (#1…,
top edge in the rank colour), product name, sold this period, KE / Out posts, KE stock, Sinza+UG stock,
% of the top-10 total and a **Push / Restock / Out of stock** pill. **Hover or tap a tile** (Enter on
keyboard; tap outside / Esc closes) for: bag + category, share of the top 10, sold **Kenya vs outside**
(Weekly shows one total — the week has no split), Kenya / outside posts, stock Kenya shops · Sinza+Uganda ·
Restock (CBD/Stock), and **what to do** — stock: 0 → restock urgently; stock ≥ max(sold, 10) → push more;
else restock soon — and posts: < 3 → post it more (Weekly: posts are a week in arrears). Totals row and the
runway guidance below are unchanged.

**Rank badges (all three tile sections — Sold vs Target, Top 10, Colour Movement):** every tile carries
its rank for the period — Top 10 and Colour Movement by **bags sold**, Sold vs Target by **% of target
sold**. Colours make the number readable at a glance: **★ 1 gold**, **#2 silver**, **#3 bronze**, then
solid **green → amber → red** from #4 down to the last place. Ties share a rank (1, 1, 3, 4…).

## Colour Movement & Stock Guidance — one KPI tile per bag (Oct 2026)

Period (Monthly / Weekly / Last week) and Product dropdowns, the colour trend line, then **one KPI tile per
new product** (high → low by bags sold): bags sold this period, KE / Out posts, KE stock, Sinza+UG stock,
its top colour and `N best · M slow` chips. **Hover or tap a tile** (Enter on keyboard; tap outside / Esc
closes) for that bag's guidance — the content of the old long list, now per bag:
- **Best-moving** = the bag's top 3 colours by bags sold (sold > 0), each with sold · posts · stock and
  advice (out of stock → restock urgently; stock ≥ max(sold, 10) → push more; else restock soon).
- **Least-moving** = colours **below the bag's own average** (or unsold) that still hold stock, not already
  best; advice: < 3 posts → post it more, else keep posting.
- Posts follow the page rules (Weekly = 0, Last week = WEEKLY_MARKETING_POST, Monthly = monthly posts).
  Colours are exact (no family fold). Data: `NP.monthlyCombined` / `NP.weeklyCombined` (colour rows).
  Before Oct 2026 this was one list across all bags, with the average taken over every colour.
- Tiles carry the same **★ 1 … last** rank badge as Top 10 (by bags sold).

## Sales by Shop (replaced "Sales vs Posts (per Colour)", Oct 2026)

A **new product × shop** table, placed **before** Sold vs Remaining to Target: one row per new product (`productTargets` order by total, high → low), one
column per shop — **STR MSA NAK ELD KSM MER THK HAZ KIT WEB NAN KAK HTN SNZ UGD KSII KTD BSA RGI** — a
**TOTAL** column and a **TOTAL** row, plus a **Posts** column (Kenya + outside posts for the period: Monthly =
MONTHLY_MARKETING_POST, Last week = WEEKLY_MARKETING_POST, Weekly = 0 — posts are a week in arrears).
- **Sales** = Odoo POS bags per till for the period, the dashboard's bag rules: combo contents counted per bag
  (the `+` wrapper isn't), refunds netted, POS-category lines out. **Staff POS is left out**; Sinza and
  Dar-es-Salaam = **SNZ**; Uganda = **UGD**; any other till goes to **OTH** (shown only when non-zero).
  **CORP** = corporate invoices (posted, paid / in payment / ≤ 25 % unpaid — the dashboard's corporate rule),
  after the shop columns.
  Product names match by the page's prefix rule (`match_odoo_bags`), all colours together.
- **Period** dropdown: Weekly (this Sun–Sat to date) · Last week (previous Sun–Sat) · Monthly (live month) ·
  **Lifetime** (all-time, `2000-01-01 … today`; Posts shows "—" — no single all-time post count).
- Zero cells show "0" dimmed. **Top 6 shops per row are colour-ranked** (Oct 2026): 1st gold · 2nd silver · 3rd
  bronze · 4th green · 5th cyan · 6th violet (rank = 1 + shops that sold more, ties share a place); the **TOTAL** row
  ranks the shops across all new bags. CORP and OTH are counted but never ranked (not shops). Each ranked cell's
  tooltip says `#n shop for <bag>`.
- **"How to read this table"** guide under it (for presenting): the colour key, what rows / columns / CORP / OTH /
  SNZ / Posts mean, the hover tip, and live **highlights** for the period — new bags sold, top 3 shops, the best
  shop for the top 4 bags, and shops with no new-bag sales (`#pc-highlights`). Data: `NP.shopSales = {period: {shops:
  [codes], rows: {PRODUCT: {CODE: units}}, window}}`.
- Checked 4 Oct 2026 against the hand-made Last-week table (27 Sep – 3 Oct): identical, 115 bags.

## Custom range (Oct 2026)

Every Period dropdown on the page (Sales by Shop, Sold vs Target, Top 10, Colour Movement) gets
**Custom (dd Mon – dd Mon)** when a range is set — see [README › Custom range](README.md#custom-range-oct-2026)
for the picker. Range file `np_custom_range.json`; data `NP.custom = {from, to, label, days, months}` (null
when none).
- **Sales:** `odoo_sales_window(from, to)` per colour → `customKenya / customOutside` on
  `NP.weeklyCombined` rows (same rules as every other period: combo contents counted, invoiced orders,
  Nairobi dates). Product totals = the sum of their colours.
- **Sales by Shop:** `NP.shopSales.custom` (same table rules, CORP included, Staff POS out).
- **Sold vs Target:** target = monthly target × `NP.custom.months` (pro-rated); the popover says so.
- **Posts:** none for a range — shown "—" everywhere (tiles, popovers, the Posts column).
- **OOS chips:** `NP.oos.custom`, same window.
- Checked 6 Oct 2026 with 01–30 Sep: colour rows and the shop table agree per bag (the shop table leaves
  out Staff POS — Loop BP 147 vs 145, Taji 63 vs 62).

## Sales by Shop — colour hover (Oct 2026)

**Hover or tap any number** in the Sales by Shop table (a product × shop cell, or the row's **Total**) for the
colours behind it: that shop's colours for the bag, high → low, with a bar each (`LOOP BP — Hilton · 28 sold:
CN Black 16 · CN Grey 11 · Maroon 1`); the Total cell sums the colours across all shops. Colours are exact as
named (`_odoo_colour`, no family fold; rejects show as their own colour, e.g. `CN Grey [Reject]`). Follows the
Period dropdown. Data: `NP.shopSales[period].colours = {PRODUCT: {CODE: [[colour, units], …]}}`.

## Regenerate

```
python new_products.py            # DENRI_LAUNCHER=1 to skip the browser tab
```
Console prints the sold + lifetime match per product (watch for "(no Odoo match)").
</content>
</invoke>
