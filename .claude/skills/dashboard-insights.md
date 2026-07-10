---
name: dashboard-insights
description: Generate a human-readable insights report from the Denri Africa marketing dashboard data. Reads PERF, PROJ, NP, OA, and PA data objects from the existing HTML files and produces a narrative summary of what's working, what's at risk, and what actions to take. Use when the user wants a plain-English analysis of current performance, trends, or anomalies across any of the 4 dashboards.
---

# Dashboard Insights Skill

Analyze the current data injected into the Denri Africa marketing dashboard HTML files and produce a clear, actionable insights report.

## What This Skill Does

Reads the live data already in the dashboard HTML files (no re-running scripts needed) and produces:
1. **Headline numbers** — the most important KPIs at a glance
2. **What's going well** — green signals worth celebrating
3. **What's at risk** — amber/red signals that need attention
4. **Anomalies** — anything that looks out of place (e.g., velocity_factor > 10x suggests month-start distortion)
5. **Recommended actions** — 3–5 specific, concrete next steps
6. **Cross-dashboard patterns** — connections between posting activity, offer types, and sales achieved

## Data Sources

| Dashboard | File | Key Object | Key Fields |
|---|---|---|---|
| Current Performance | `current_performance.html` | `PERF`, `PROJ` | `sales`, `salesPctAchieved`, `remainingTarget`, `weeklySalesTotal`, `wowSalesPct`, `bareMinimum`, `standardProjection` |
| New Products | `new_products.html` | `NP` | `salesPct`, `totalSales`, `totalDeficit`, `monthlyKenya`, `monthlyOutside`, `monthlyCombined` |
| Offer Type Analysis | `offer_type_analysis.html` | `OA` | `totalKenyaStock`, `totalUgandaStock`, `totalSinzaStock`, `comboCount`, `powerDealCount`, `offerCount` |
| Posting Yields | `POSTING (SALES YIELDS FROM ACCURATE POSTING).html` | `PA` | `wkMktPct`, `moMktPct`, `weeklySalesTotal`, `weeklyPostsMade`, `wkInstockPosted`, `wkInstockNotPosted` |

## How to Extract Data

Use Grep to find the injected data blocks:

```
<!-- PERF_DATA_START -->   in current_performance.html
<!-- NEW_PROD_DATA_START --> in new_products.html
<!-- OFFER_DATA_START -->   in offer_type_analysis.html
<!-- POST_DATA_START -->    in POSTING (SALES YIELDS FROM ACCURATE POSTING).html
```

Read the JSON/JS assignment between those markers to get the current values.

## Insight Categories & Thresholds

### Sales Performance (from PERF + PROJ)
- **On track**: `salesPctAchieved` ≥ current day / days_in_month × 100
- **At risk**: `salesPctAchieved` < 40% before the 15th of the month
- **Critical**: `remainingTarget` > `sales` × 2 (need to more than double pace)
- **Projection distortion**: `velocityFactor` > 10 = month-start artifact, projections unreliable
- **WoW decline**: `wowSalesPct` < 0 = flag as concern; `wowSalesPct` < -20% = urgent

### Marketing Posting (from PA)
- **Good posting rate**: `wkMktPct` ≥ 40% (40%+ of sales came from posted bags)
- **Low posting rate**: `wkMktPct` < 25% = marketing not converting to sales
- **Accuracy concern**: `wkInstockNotPosted` > `wkInstockPosted` = more bags unposted than posted
- **Cross-check**: if `weeklyPostsMade` is high but `weeklySalesTotal` is low = posts not converting

### New Products (from NP)
- **Strong new product**: any product in `monthlyCombined` with `sKenya + sOutside + sRestock` > 50 in first month
- **Slow mover**: deficit products (in `totalDeficit`) with < 5 total sales
- **Regional imbalance**: `monthlyOutside` > `monthlyKenya` × 2 = outside demand outpacing Kenya

### Offer Types (from OA)
- **Stock coverage**: compare `totalKenyaStock` vs `totalUgandaStock` vs `totalSinzaStock` — flag if one region has < 20% of Kenya's stock
- **Combo vs singles**: high `comboCount` relative to `offerCount` = product mix skewed toward bundles

## Report Format

Produce a structured report in this format:

```markdown
## Marketing Dashboard Insights — [Date]

### Headline Numbers
- Monthly Sales: X bags (Y% of target)
- This Week: X bags (WoW: +/-X%)
- Bags Still Needed: X
- Marketing Post Conversion: X%

### What's Going Well
- [Green signal 1]
- [Green signal 2]

### What Needs Attention
- [Amber/red signal 1 with specific numbers]
- [Amber/red signal 2]

### Anomalies Detected
- [Any data that looks distorted or unusual]

### Recommended Actions (This Week)
1. [Specific action with numbers]
2. [Specific action with numbers]
3. [Specific action with numbers]

### Cross-Dashboard Connections
- [Pattern linking posting data to sales outcomes]
- [Pattern linking offer types to conversion]
```

## Rules for Good Insights

- **Always cite numbers** — "posting rate is low" is weak; "posting rate is 18% vs 40% target" is actionable
- **Distinguish correlation from causation** — say "coincides with" not "caused by" unless the data clearly shows causation
- **Flag projection distortion** — if `velocityFactor` > 10 (month start), note that projection % figures are unreliable artifacts
- **Regional comparison** — always compare Kenya vs Sinza vs Uganda where data exists; imbalances are often the most actionable insight
- **Time-awareness** — factor in `currentDay` / `daysInMonth` when assessing whether % achieved is on pace
- **Don't summarize what the user can already see** — focus on the non-obvious connections and risks, not just restating the KPI numbers
