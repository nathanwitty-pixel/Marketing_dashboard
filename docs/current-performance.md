# Current Performance

- **Generators:** `weekly_sales.py`, `monthly_sales.py` (Postgres → figures),
  `current_performance.py`, `forward_projections.py`
- **HTML:** `current_performance.html`
- **Data markers:** `<!-- PERF_DATA_START -->…<!-- PERF_DATA_END -->` (const `PERF`) and
  `<!-- PROJ_DATA_START -->…<!-- PROJ_DATA_END -->` (const `PROJ`, from
  `forward_projections.py`)
- **State files:** `previous_snapshot.json` (last period's values),
  `monthly_report_history.json` (prior-month weekly series for the comparison chart)

## What the page shows

The month's headline performance — total target vs sales vs deficit, sales % achieved,
week-over-week movement, and a **September-vs-August weekly comparison chart** (current
month solid, previous month dashed — `cpPrevWeekly` from `monthly_report_history.json`),
plus forward projections.

## Sales card — reject split

The Sales-card breakdown line shows the POS/corporate split **and the reject-clearance subset**:
"N POS + C corporate · R rejects (X%)". `rejectBags` is the `[REJECT]`-tagged products (the
Kitengela clearance) computed by `monthly_sales.py` (`sql/reject_bags_sold.sql` — same grand-total
definition as `bags_sold_total.sql` plus the `[REJECT]` tag, so it's a true subset), surfaced via
`current_performance.py` (`reject_from_db` → `PERF.rejectBags` / `rejectPct`, % of the POS total).
So you can see how many of the bags sold were rejects vs normal stock.

## Data sources

- **MONTHLY_TARGET** sheet: col C target, D sales, E deficit (summed).
- Real weekly/monthly **bags** are refreshed from Postgres first (`weekly_sales.py`,
  `monthly_sales.py`) so the sales figures are live, not stale sheet values.
- `previous_snapshot.json` auto-loads the previous period so week-over-week deltas render
  without manual entry (keyed on ISO week).

## Manual inputs

- `bare_minimum` in `current_performance.py` — the week's minimum bags target (0 = unset).
- `forward_projections.py` holds the projection assumptions (re-run to pick up edits).

## Month scope

Figures belong to the month `report_month` reports — the **live/current** month, matching
the other dashboards. `projMonth` (from the PROJ block) names it.

## Regenerate

```
python weekly_sales.py
python monthly_sales.py
python current_performance.py
python forward_projections.py
```
(Or just `python build_all.py` for the whole set in the right order.)
</content>
</invoke>
