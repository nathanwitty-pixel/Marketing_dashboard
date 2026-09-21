# New Products Analytics

- **Generator:** `new_products.py`
- **HTML:** `new_products.html`
- **Data marker:** `<!-- NEW_PROD_DATA_START -->…<!-- NEW_PROD_DATA_END -->` (const `NP`)
- **State file:** `new_products_weekly_history.json` (per-week posts/sales snapshots)

## What the page shows

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
- **STOCK_LEVELS** — col Y Kenya, Z Outside, AA restock (per colour).

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

> Note: New Products counts standalone `full_product_name` sales and excludes
> combo/reward/strap/gift lines (via `_BAGS_WHERE`), so its Lamora lifetime is 227 /
> Black 118. A raw template-name count is 229 / Black 120 — the 2-unit gap is Black units
> sold on excluded line types. Both are correct; they answer different questions.

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
attributed correctly) and `NP.weeklyTarget`. Per-week sales are **Kenya-only** (matching the
`Weekly Sales % Achieved` KPI); the footer's "last week (incl. outside)" stat is the
Kenya+Outside `lastWeekPct`/`lastWeekTotal`, labelled to flag the scope difference.

## Regenerate

```
python new_products.py            # DENRI_LAUNCHER=1 to skip the browser tab
```
Console prints the sold + lifetime match per product (watch for "(no Odoo match)").
</content>
</invoke>
