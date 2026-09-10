# Reporting History (Supabase)

- **Generators:** `push_to_supabase.py` (write) → `history.py` (read)
- **HTML:** `history.html`
- **Data marker:** `<!-- HISTORY_DATA_START -->…<!-- HISTORY_DATA_END -->`
- **Supporting:** `supabase_migration.py` (schema), `month_end.py` (freezes a month)

## What the page shows

The frozen monthly snapshots stored in Supabase — the read side of the Supabase
round-trip. For each archived month: Current Performance, New Products, Offer Type
Analysis (all locations), Posting Yields, and each month's Timed Offer campaigns with
their bags and daily sales series.

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
