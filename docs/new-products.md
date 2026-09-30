# New Products Analytics

- **Generator:** `new_products.py`
- **HTML:** `new_products.html`
- **Data marker:** `<!-- NEW_PROD_DATA_START -->…<!-- NEW_PROD_DATA_END -->` (const `NP`)
- **State file:** `new_products_weekly_history.json` (per-week posts/sales snapshots)

## What the page shows

**Sidebar** ([page sidebar](README.md#page-sidebar)) — one entry per block — Overview, Weekly Sales vs Marketing Posts, Weekly Performance, Sold vs Remaining to Target, Top 10, Colour Movement & Stock Guidance, Sales vs Posts (per Colour).

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

## Regenerate

```
python new_products.py            # DENRI_LAUNCHER=1 to skip the browser tab
```
Console prints the sold + lifetime match per product (watch for "(no Odoo match)").
</content>
</invoke>
