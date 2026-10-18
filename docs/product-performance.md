# Product Performance — which bags, categories and colours carry the sales, and why

- **Generator:** `generators/product_performance.py` → `html/product_performance.html`
- **Data marker:** `<!-- PP_DATA_START -->…<!-- PP_DATA_END -->` (const `PP`)
- **Menu:** Products section, **just before New Products** (`dashboard_pages.json`).
- **Regenerate:** `python generators/product_performance.py`

## What the page shows

**Sidebar** ([page sidebar](README.md#page-sidebar)): Bag of the Week, Top-selling bags, Categories, Colours.

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
Hover / tap a bag: units, revenue, both shares, previous period, Kenya / Sinza / Uganda split, its top colours,
its stock now, its offer tags and posts — and the same *Why it moved* lines (for the chosen period) as the Bag of the Week.

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
  ('+' name) is not a bag. Left out: delivery, customisation, straps, KES discount, samples, gift bags, POS
  category lines, `sales_exclusions.txt`. Corporate invoices are **not** included (POS only).
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

## Bulk orders

**Corporate-lead till orders (16 Oct 2026, user's call — revised the same day):** when a client the **Corporate team** brought in (a Corporate-app lead) pays at a shop till, the sale is **credited to that shop** like any till sale, but it's still marked as a Corporate lead (October: ESK Company, HAZINA/29958 + 29613, KES 1,707,197 → Hazina, "Corporate app lead 17 Sep · Scola Mithiri"). One that hasn't paid yet goes to the shop that hunted it (quote note → bought there before → client's town), still noted as a Corporate lead; with no shop link it isn't shown at all until something is paid at a till. Here: they stay in the totals and are flagged ⚠ like bulk orders, noted as a Corporate lead credited to the shop.


A POS line of **10+ units** is a corporate / bulk order. It stays in every total (it was a real sale), is
listed with ⚠ wherever a change is shown, and the change is also given **without** it. The Biggest mover is
picked on the without-bulk change.
