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
  - **Why did we move — month on month:** the full month vs the month before, per region (with and without bulk
    orders), the selling-days effect and each region's change (`lib/why_moved.build_month`).
  - **Followers & reach (Kenya):** month-end Facebook / Instagram followers, new follows in the month, Instagram
    reach and views on both (Odoo Meta sync — from 18 Oct 2026, so October is part-month and says so).
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
