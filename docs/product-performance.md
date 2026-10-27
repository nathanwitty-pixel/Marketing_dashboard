# Product Performance — which bags, categories and colours carry the sales, and why

- **Generator:** `generators/product_performance.py` → `html/product_performance.html`
- **Data marker:** `<!-- PP_DATA_START -->…<!-- PP_DATA_END -->` (const `PP`)
- **Menu:** Products section, **just before New Products** (`dashboard_pages.json`).
- **Regenerate:** `python generators/product_performance.py`

## What the page shows

**The filter bar follows the reader** (Market, Period, Share by; 19 Oct 2026): it pins at the top while scrolling, so
the period can be changed beside any chart (`assets/sticky_controls.js`, docs/sticky-controls.md).

**Sidebar** ([page sidebar](README.md#page-sidebar)): Bag of the Week, Top-selling bags, Shop breakdown, Categories, Colours.

**Controls (top of the page, drive every section below):**

- **Market:** All markets (default) · Kenya · Sinza · Uganda.
- **Period:** Last week (default — the full Sun–Sat week before this one) · This week (to date) · This month (to
  date) · Last month. Each is compared with the period before it, the same length: last week vs the week
  before · this week vs last week's same days · this month vs last month's same days · last month vs the month
  before.
- **Share by:** Units (default) · Revenue (KES).

### 1. Bag of the Week / Month

Follows the **Period** and market (16 Oct 2026 — it used to stay on last week): *Bag of the Week* for Last week /
This week, *Bag of the Month* for This month / Last month, each compared with the period before it. Two cards:

- **Top seller** — the most units sold in the period.
- **Biggest mover** — the largest rise in units vs the period before, among bags that sold **≥ 10 a week**
  (scaled to the period's length — 23 for 16 days). Judged **without bulk orders** (below).

The reasons use the same comparison. Posts (marketing's daily posting sheets, `lib/marketing_posts`, 18 Oct 2026):
Last week compares with the week before and Last month with the month before, both counted day by day from the
sheets (Kenya / Sinza / Uganda per market, all three for All); This week's posts aren't counted until next week;
This month shows the month's posts. If the sheets can't be read, Last week falls back to the week Bag Signals saved.

Each card: bag, units (and share of the week), revenue, change vs the week before (units and %), and
**Why it moved** — the evidence, grouped:

| Group | Evidence (last week vs the week before) |
|---|---|
| **Stock** | shop stock at the start of each week · units dispatched into the shops in each week from a warehouse (with the date of the biggest delivery). Combo products ('+' names) are left out of stock — they carry their own stock in Odoo · days in stock each week. *Back in stock* = in stock more days than the week before; *Restocked* (▲) = dispatched ≥ 10 units and ≥ 30 % of the week's sales **and** the shops started the week with less than the week sold (bulk orders aside) (otherwise it's context: "stock was already enough"); *Ran short* = fewer days in stock than the week before. |
| **Offer** | Power Deal (all month) · Deal of the Week (tier, shops, weeks) · Timed offer (dates, was → now) · running combo component — plus units sold **inside combos** each week. *Started* / *Ended* when an offer runs in one week and not the other. Sinza / Uganda: listed combos / singles from `offers_monthly.csv`. |
| **Marketing** | posts last week vs the week before (Kenya + outside) and posts this month. |
| **⚠ Bulk** | any single POS line of **10+ units** in either week: qty × product, receipt, till, date — and the change **without** it (rule: [bulk orders flag](#bulk-orders)). |

Each line is marked ▲ (helped), ▼ (held it back) or · (context only). The headline reason is the first ▲
in the order Stock → Offer → Marketing; if there is none, "no single driver — steady demand". **When a bulk
order explains the change** (the change without bulk orders is under half the raw change), the headline is the
bulk order itself, with the without-bulk figures.

### 2. Top-selling bags — % share

The top 15 bags for the chosen market + period, each with its **% of all bags sold** (or of revenue), a share
bar, units, revenue, and the change in share vs the previous period (pp). The rest are one **Other bags** row.
**Top 5 categories — suggestions (19 Oct 2026):** under each top-3 / bottom-3 bag, one action from its shop stock now,
units sold in the period, Kenya offers this month and posts. **Top 3:** stock 0 → *Sold out: restock now* · stock below
the units it sold → *Restock* · no posts last week → *Keep it posted* · stock over 6× its sales and not on offer →
*Feature it on Deal of the Week* · else *Protect stock and keep posting*. **Bottom 3:** stock ≤ 2 → *Let it run out, do
not reorder* · not posted this month → *Post it first* · not on offer → *Put it on an offer or in a combo with the
category's top seller* · on offer and still slow → *Check price or design, or clear it*.

**Popovers and wording (19 Oct 2026):** values sit in small tables (columns), never strung together with dots; the
change column is titled **Week on week** (weekly views) / **Month on month** (monthly) / *vs previous* (custom).

**Support score (19 Oct 2026, user's choice — weights 40 / 30 / 30):** every "why it moved" box opens with a score
out of 100 for how much **support** the bag had in the period vs the one before:

| Pillar | Points | Rule |
|---|---|---|
| **Stock** | 40 | 40 × the share of days it was in stock this period (in stock every day = 40) |
| **Offer** | 30 | Kenya offers (Power Deal · Deal of the Week · timed offers): kept or added = **30**; one ended, or none in either period = **15**. Sinza / Uganda: not scored (no offer history) |
| **Marketing** | 30 | posts this period ÷ posts the period before × 30, capped at 30; none in either = 15. Only when both periods' posts are known (last week · last month) |

A pillar that can't be judged is left out and the total is scaled to 100. **Verdict** = the score against the sales
change (bulk orders aside): support ≥ 70 and up = **Working — keep going** · < 70 and up = **Selling on its own —
strong demand** · ≥ 70 and down = **Demand problem — check price / design** · < 70 and down = **Support pulled — put
back the offer / posts** · a change under max(3 units, 10 % of the period before) = **Steady**. Payload `why[...][BAG].score = {total, stock, offer, mkt, verdict}`.

**The ▲ / ▼ marks (19 Oct 2026):** **pp** = percentage points of the **share of sales** — ▲ green = a bigger slice
(10.0 % → 10.1 % = +0.1 pp), ▼ red = a smaller slice, grey 0.0 = same (under 0.05 pp). Share, not units: a bag can
sell more and still go red if the rest grew faster. Every mark has a hover with the share before → after; the
% marks (units / revenue) hover with before → after and the % change. The table hint carries the same legend.
Hover / tap a bag: units, revenue, both shares, previous period, Kenya / Sinza / Uganda split, its top colours,
its stock now, its offer tags and posts — and the same *Why it moved* lines (for the chosen period) as the Bag of the Week.

### 2b. Shop breakdown (22 Oct 2026, user's call)

Units (and revenue) sold **per shop**, after Top-selling bags. Built from the same sales lines as the rest of the
page (no extra Odoo query), so the shop units add up to the period's total in Bag of the Week.

- **Follows the filter bar:** **Market** (All shows every shop; Kenya / Sinza / Uganda only that market's tills),
  **Period** (Last week, This week, This month, Last month, each against the period before it of the same
  length) and **Share by** (Units ranks and sizes by units, Revenue by KES).
- **Shop = the till** (`pos_config` name), shown tidy: `ktda shop` → Ktda, `dar-es-alam` → Sinza, `uganda` →
  Uganda, `website` / `website sales` → Website, `staff pos` → Staff POS, the rest in title case. A shop's market is its till's market (Sinza = `sinza` +
  `dar-es-alam`).
- **Chart:** one horizontal bar per shop, ranked, coloured by market (Kenya blue, Sinza orange, Uganda aqua —
  palette slots 1–3). The **number sits in the bar** (just past it, and past the tick, when the bar is short);
  the period before is a thin tick on the same scale (never a second axis). At the row end: the share, ⚠ when a
  bulk order is in it, and a **change badge** against the period before on the chosen basis — green ▲ +% up,
  red ▼ % down, grey 0.0% (under 0.5%), blue "new" when nothing sold before (22 Oct 2026, user's call).
- **Corporate row (26 Oct 2026, user's call):** the Corporate app's bags paid in the period sit as their own row,
  **Corporate** (Kenya, so on All and Kenya), with units, revenue (KES received), share of the total, the period
  before and its change — the Sales card's rule (`sql/corporate_bag_lines.sql`, money received on the payment date).
  Click it for the bags on the invoices. **It is a sales channel like a till, not a bulk order** (user, 26 Oct
  2026): no ⚠, and it stays in *Without bulk orders*. Bulk orders are only 10+ unit lines rung at a shop till —
  including Corporate-team clients who pay at a shop (those stay the shop's sale, flagged ⚠).
- **Total row (25 Oct 2026, user's call):** under the last bar, **Total**: all the shops' units (or revenue on
  Revenue), the same figure for the period before, 100% share and the change badge, with no bar. The table
  ends with the same **Total** row (units, 100%, change, revenue, and the bulk units in all shops). Follows
  every filter, the bulk switch included.
- **Table** (collapsed by default under "▸ Show the shop table (N shops, with change and bulk orders)"; open / closed is
  remembered per browser, 22 Oct 2026): Shop, Market, Units, Share, Change vs the period before (units and %, green up, red down),
  Revenue, and a ⚠ bulk flag: the shop's units on POS lines of **10+ units** in the period and its change
  **without** them (the [bulk orders](#bulk-orders) rule; they stay in the totals).
- **Bulk orders switch (22 Oct 2026, user's call):** *With bulk orders* (default) or *Without bulk orders*, in the
  section's header, remembered with the other filters. *Without* takes every POS line of **10+ units** out of
  both periods — units, revenue, shares (of the total without bulk), the bars, the change badges, the table and
  the drill-down — so a corporate / bulk sale can't make a shop look like it jumped or collapsed. The table's
  bulk column then says how many units were left out.
- **Drill-down:** click a shop (bar or row) to open its **top 10 bags** in the period: units, revenue and
  the change in units vs the period before. Click again (or another shop) to switch.
- Data: `PP.shops[period][market]` = `{total, rev, shops: [{shop, mkt, units, rev, pUnits, pRev, chg, chgPct,
  share, revShare, bulkUnits, pBulkUnits, bulkRev, pBulkRev, chgNoBulk, bags: [[bag, units, rev, pUnits, bulkUnits,
  bulkRev, pBulkUnits]]}]}` (bags: top 15 by units), market keys
  ALL / KE / TZ / UG.

### 3. Categories — % share

Every category (catalogue category of the bag type — `product_catalog.csv`; else Odoo's category), same share
bars, units, revenue, change in share. Hover: its top 5 bags with their share of the category.
**Top 5 vs the rest (16 Oct 2026, user's call):** the 5 biggest categories get their own rows; all the others are
one "Other categories (N)" row with their combined share, units, revenue and change. Its ▸ lists each of them
(ranked 6, 7, …, share of all bags).

### 3b. Top 5 categories — best & weakest bags (16 Oct 2026, user's call)

One card per top-5 category (same period / market / basis): its **top 3** and **bottom 3** bags by rank inside the
category (only bags that sold ≥1 in the period), with units, share of the category and **shop stock now**
(`info.stock`: KE · Sinza · UG, summed for All markets). Stock red = 0; amber = below what the bag sold in the
period. Bags in stock that sold nothing aren't listed. Hover / tap a bag: the usual bag popover.

### 4. Colours — % share

Colour **families** (`lib/colours.family()` — all browns → Brown, CN/TT/Croc/018 → base colour, Nude → Beige,
Maroon → Red; [colour families rule](README.md)), same share bars. Hover: its top 5 bags in that colour.
**▸ Shades (16 Oct 2026, user's call):** a family with 2+ shades has a ▸ toggle that opens every shade under it
(Brown → Brown, Cracked, Spice, Chocolate, Dark Brown…), each with its **% of the family**, units, revenue and change.
Shade = the product name after its bag type, minus edition / material words (Wooven, HB, CN, TT, 018, Ankara, Croc,
Custom) and [REJECT]; Choco / Chocolate Brown → Chocolate, D.Brown → Dark Brown. Family totals don't change.
**No colour** has no shades, so its ▸ lists the **bags** instead (Laptop Sleeve, Cathy Handbag…). Discount lines
(KES or % — "10.0% Discount On Total Amount") are never bags and are left out of the page.

## Data

- **Sales (Odoo POS, line level):** every till, `done / invoiced / paid`, Nairobi dates, refunds netted
  (qty ≠ 0). Bags = every bag line **including bags inside combos** (`sub_product_line`); the combo wrapper
  ('+' name) is not a bag. Left out: delivery, customisation, straps, KES discount, POS category lines,
  `sales_exclusions.txt`. **Gift bags and samples are counted** (26 Oct 2026, user's call), so the totals match
  the Sales card and Bags on Offer (before: Wk 4 Oct showed 3,408 here vs 3,449 there = 41 gift bags + 1 sample).
  Corporate is a row of its own (see Corporate row).
- **Revenue (KES):** line `price_subtotal_incl`; Sinza ÷ 25, Uganda ÷ 29 (as `sql/bags_sold_total.sql`).
  Bags inside a combo ring at 0 — the **combo line's money is split across the bag lines that follow it on
  the same receipt**, in proportion to each bag's full price (`bag_original_prices.json`; equal split when a
  price is missing).
- **Markets:** Sinza = `sinza` + `dar-es-alam` tills; Uganda = `uganda`; Kenya = every other till (Website
  included).
- **Bag type:** `lib/runway_bags.type_fn()` (catalogue bag when known, else the name minus its colour words).
- **Stock:** shop on-hand rebuilt per day from `stock_quant` now and the done stock moves (the
  `lib/product_targets` method), per market: Kenya shops + WEB · DAR · UG (never warehouses).
- **Offers:** `bags_offer_source_<YYYY-MM>.json` (written by Self-made Combos) per day's month — Power Deal /
  Combo component tags and Deal-of-the-Week runs (weeks counted Sun–Sat from the Sunday on or before the 1st);
  `timed_offers_config.json`; `offers_monthly.csv` for Sinza / Uganda.
- **Posts:** WEEKLY_MARKETING_POST (= last week, posts are a week in arrears) and MONTHLY_MARKETING_POST, Kenya
  col E + outside col H; the week before from `bag_posts_history.json` (Bag Signals saves it each run — shows
  "—" when that week isn't saved).

## Popover waterfall — why the units moved (26 Oct 2026, user's call)

Every bag, category and colour popover has a small waterfall under the This period / Previous table:
**Before → Days → parts → Now** (`wfHtml()` in `product_performance.html`, HTML/CSS bars, no Chart.js).
Parts are the bag's **colours** (bag popover) or the **bags** in the group (category / colour popover).
The 4 biggest movers show; the rest join "Other colours" / "Other bags". The method is the same as
[Current Performance › Why Did We Move?](current-performance.md): Days = old pace × day difference (shows
only when the periods differ, e.g. Last month 30 vs 31 days); a part's bar = its units/day change × days now; the
bars add up exactly. The amber box and "The reason" line mark the biggest move in the direction of the total.
In the bag popover, a bag with bulk orders adds "⚠ Bulk orders are in these units. Without them: X → Y".

## Bulk orders

**Corporate-lead till orders (16 Oct 2026, user's call — revised the same day):** when a client the **Corporate team** brought in (a Corporate-app lead) pays at a shop till, the sale is **credited to that shop** like any till sale, but it's still marked as a Corporate lead (October: ESK Company, HAZINA/29958 + 29613, KES 1,707,197 → Hazina, "Corporate app lead 17 Sep · Scola Mithiri"). One that hasn't paid yet goes to the shop that hunted it (quote note → bought there before → client's town), still noted as a Corporate lead; with no shop link it isn't shown at all until something is paid at a till. Here: they stay in the totals and are flagged ⚠ like bulk orders, noted as a Corporate lead credited to the shop.


**Corporate app ≠ corporate bulk orders (26 Oct 2026, user's call):** the Corporate app (denri_corporate invoices)
is its own sales channel, like a till, and is **never** a bulk order. "Corporate bulk orders" means big **till** orders only.

A POS line of **10+ units** is a corporate / bulk order. It stays in every total (it was a real sale), is
listed with ⚠ wherever a change is shown, and the change is also given **without** it. The Biggest mover is
picked on the without-bulk change.
