# Reporting History (Supabase)

- **Generators:** `push_to_supabase.py` (write) → `history.py` (read)
- **HTML:** `history.html`
- **Data marker:** `<!-- HISTORY_DATA_START -->…<!-- HISTORY_DATA_END -->`
- **Supporting:** `supabase_migration.py` (schema), `month_end.py` (freezes a month)

## What the page shows

**The New Products Sort follows the reader** (19 Oct 2026): it pins at the top while the New Products section of the chosen month is on screen, also after a month change redraws it (`assets/sticky_controls.js`, docs/sticky-controls.md).


**Sidebar** ([page sidebar](README.md#page-sidebar)) — **Months** picker (calendar tile, % of target, colour meter) replaces the month buttons, then Bottom line + the month's numbered sections.

The frozen monthly snapshots stored in Supabase — the read side of the Supabase
round-trip. For each archived month: Current Performance, New Products, Offer Type
Analysis (all locations), Posting Yields, and each month's Timed Offer campaigns with
their bags and daily sales series.

**Newer pages** (from September 2026) sit inside the month's own sections: Power Deals vs Deal of
the Week under 3 · Offer Type, the posting yield + dead stock clearance under 4 · Posting Yields,
monetary implication / weekly goal / combo button usage under 6 · Self-Made Combos, and a new
7 · Bags On vs Off Offer, and **8 · Shop Corporate Orders** (1 Nov 2026, user's call: the month's Shop corporate
tab — clients quoted in Odoo Sales who paid at the shop tills: paid, owed, per hunting shop, per client; rebuilt
from Odoo for that month by `lib/shop_corporate.build(month)` when the month is archived, and also saved to
`data/shop_corporate_history.json` as a local backup). Data: `denri_mkt_monthly.extras`.

**Added 1 Nov 2026 (user's call), rebuilt from Odoo for the month when it's archived (`lib/month_extras.py`):**
- **Inside 1 · Current Performance** (`extras.cpMore`):
  - **Revenue:** the month's POS bag revenue (single bags, combos, gift bags, discounts — `sql/bag_revenue.sql`),
    Corporate-app KES received, their total vs the month's Odoo revenue target, and bags vs the bag target.
  - **Why did we move — month on month:** the full month vs the month before as a **waterfall chart** like the live
    page's (last month → selling days → each region, biggest rise first → this month; numbers on every bar; the
    biggest bar in the direction the month moved boxed amber as "the reason"; With / Without bulk orders buttons;
    a bar's tooltip lists its shops). The same numbers sit under it as a table you can unfold
    (`lib/why_moved.build_month`; 1 Nov 2026, user's call).
  - **Followers & reach (Kenya):** month-end Facebook / Instagram followers, new follows in the month, Instagram
    reach and views on both (Odoo Meta sync — from 18 Oct 2026, so October is part-month and says so).
- **2 · New Products chart in the waterfall style** (1 Nov 2026, user's call): headline "N bags sold of T target (P%), S short",
  then one bar per new product stacking up from 0 (its bags sold, number on top) to a **Total sold** bar, a dashed
  **Target** line, the top seller boxed amber ("top seller"); hover a bar for its own target and what's left. The Sort
  menu sets the bar order.
- **7 · Bags On vs Off Offer charts in the waterfall style** (1 Nov 2026): a headline (the month's money, % on offer), then
  **Money per week** — each week's money stacking up to the month total (best week boxed; hover = on / not on / others) —
  and **Where the money came from** — each offer source (green), Not on offer (red), Others (grey) stacking up to the
  total (biggest boxed). Numbers on every bar.
- **9 · Product Performance: Top bags and Shops as waterfalls** (1 Nov 2026): month before (those bags' / every shop's
  total) → each bag's / shop's change (biggest rise first) → this month, numbers on every bar, the biggest bar in the
  direction of the move boxed as "the reason", axis starting near the lowest level; hover = month before → this
  month, money and share. The tables stay underneath, folded ("Show the numbers as a table").
- **6 · Self-Made Combos: Kenya · Sinza · Uganda buttons** (`extras.selfMadeRegions`, 1 Nov 2026, user's call). Kenya is
  the CBR view as before. Sinza / Uganda come from their till receipts (`lib/receipt_combos.market_summary` for the
  month): combos that fit a listed offer = running, other combos = self-made, in the market's own currency — summary
  cards, the running offers and the self-made combos. The **combo request log** shows the first 10 rows with
  "Show all N" / "Show fewer" (also for the self-made lists); "nan" reject reasons are no longer printed.
- **9 · Product Performance** (`extras.productPerformance`): the Product Performance page's **Last month** view for
  that month vs the month before — bag of the month (top seller, biggest mover and why it moved, with its support
  score and verdict) per market, the top bags table and the shop breakdown. Built with
  `product_performance.build(the 1st of the next month)`. See [MONTH_END.md](../MONTH_END.md#the-newer-pages-in-history-extras).

## Data flow

```
month_end.py ──► push_to_supabase.py ──► Supabase (denri_mkt_* tables) ──► history.py ──► history.html
   (freeze)         (write months)                                          (read back)
```

- `supabase_migration.py` / `push_to_supabase.py` **write** the monthly snapshots.
- `history.py` **reads** the `denri_mkt_*` tables back for display.

## Connection & resilience

- Uses `psycopg2` + `.env` (Supabase **session pooler** host — the direct host is
  IPv6-only). Never commit/print `.env`.
- If `psycopg2` is missing or Supabase is unreachable, `history.py` **leaves the page's
  existing data untouched** and prints why, so the launcher never fails on it.

## Regenerate

```
python generators/push_to_supabase.py        # ensure months are written
python generators/history.py                 # read them back into the page
```
</content>
</invoke>
