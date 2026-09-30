# Reporting History (Supabase)

- **Generators:** `push_to_supabase.py` (write) → `history.py` (read)
- **HTML:** `history.html`
- **Data marker:** `<!-- HISTORY_DATA_START -->…<!-- HISTORY_DATA_END -->`
- **Supporting:** `supabase_migration.py` (schema), `month_end.py` (freezes a month)

## What the page shows

**Sidebar** ([page sidebar](README.md#page-sidebar)) — **Months** picker (calendar tile, % of target, colour meter) replaces the month buttons, then Bottom line + the month's numbered sections.

The frozen monthly snapshots stored in Supabase — the read side of the Supabase
round-trip. For each archived month: Current Performance, New Products, Offer Type
Analysis (all locations), Posting Yields, and each month's Timed Offer campaigns with
their bags and daily sales series.

**Newer pages** (from September 2026) sit inside the month's own sections: Power Deals vs Deal of
the Week under 3 · Offer Type, the posting yield + dead stock clearance under 4 · Posting Yields,
monetary implication / weekly goal / combo button usage under 6 · Self-Made Combos, and a new
7 · Bags On vs Off Offer. Data: `denri_mkt_monthly.extras`. See [MONTH_END.md](../MONTH_END.md#the-newer-pages-in-history-extras).

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
python push_to_supabase.py        # ensure months are written
python history.py                 # read them back into the page
```
</content>
</invoke>
