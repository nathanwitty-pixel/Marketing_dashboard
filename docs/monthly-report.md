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
