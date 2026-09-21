# Monthly Report

- **Generator:** `monthly_report.py`
- **HTML:** `monthly_report.html`

## What the page shows

An executive monthly report that runs each area through a four-step framework:

1. **Get attention** → lead with the conclusion
2. **Deliver the insight** → answer a business question
3. **Recommendation** → Stop / Start / Start-testing
4. **Business impact** → quantified, assumptions stated

Areas covered: Current Performance, New Products, Offer Type Analysis (combo/offer data),
Posting Yields.

## Response-ladder tag (single appropriate step, per metric)

A **single small tag** attached to each key metric — the **one appropriate response** on a
four-step ladder **Update · New Timing · Acknowledge · Collaborate**, followed by its one-line
action. (Earlier this showed the whole strip lit up to the peak; now only the one step is shown.
**Apologize was removed** — it wasn't useful.)

- `ladder_strip(pct_val, action)` picks the deepest step the metric needs and renders just that
  one `.lstep` chip: **Update** by default; each deeper step when `pct_val` is below its
  threshold (`_LADDER` thresholds descend 100 / 80 / 65, so the deepest applicable is
  **Collaborate** at < 65%). When the chosen step is the deepest rung (Collaborate) it takes the
  amber `peak` style. The `action` line follows it (`→ Step: …`); a hover title notes the metric %.
- Applied across the report — each with its own driving metric and action copy:
  - **The Bottom Line** — one tag per point: sales % of target (`achieved`), posting coverage
    (`100 − unposted_pct`), weekly pace (`avg_weekly / bare_min`), weakest region
    (`min(ke/sz/ug)`).
  - **Current Performance** (`achieved`), **New Products** (`salesPct`), **Posting Yields**
    (`ke_mo_mkt`).
- Because it's metric-driven, the tag differs per metric: e.g. at the Sept numbers most metrics
  land on **Collaborate** (well below 65%), posting on **New Timing**. A metric at/above 100%
  shows **Update**.
- Reuse for any other metric by calling `ladder_strip(pct_val, action)`. `.lstrip` / `.lstep` /
  `.laction` styling in HEAD.

## Data sources

Like Insights, it reads the **already-injected** data blocks from the other pages — so it
runs **after** them:

- `current_performance.html` → `PERF_DATA`, `PROJ_DATA`
- `new_products.html` → `NEW_PROD_DATA`
- `self_made_combos.html` → **`OFFER_DATA`** (the offer/combo source since
  `offer_type_analysis` was retired)
- `POSTING (…).html` → `POST_DATA`

## Report month & finalized months

- Live report = the **current** month (`report_month.live_anchor()`), matching the live
  dashboards — on 1 Sep it reports September (day 1), not closed August. A pin
  (`DENRI_REPORT_MONTH`, set by `month_end.py`) points it at a specific month being
  archived.
- A **finalized** month is static — its report HTML is frozen and never regenerated.

## Manual input

- `AVG_PRICE` (default 2500 KES/bag) — set to the real average selling price to quantify
  the revenue lines.

## Regenerate

```
python monthly_report.py          # run AFTER the data pages
```
</content>
</invoke>
