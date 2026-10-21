# Footfall and Marketing — progress (brief: notes/footfall_ralph_prompt.md)

## 1. Spec — DONE
docs/footfall-marketing.md written; docs/README.md links it.
Verify (grep counts, every name ≥1): denri_footfall_count 1, config_id 2, manual_count 2, counted_by 1, note 1,
customer_type 1, walkin 2, 3 hours 1, amount_total 1, denri_monitor_interaction 1, response_time_first 2,
is_purchased 2, is_paid 2, shop_id 1, marketing_posts 1, ads_weekly.csv 2, ÷ 25 1, ÷ 29 1; README link 1.

## 2. SQL + library — DONE
sql/footfall_walkins.sql + lib/footfall.py (daily, weekly, whatsapp_weekly, SHOPS mapping).
Verify output (weekly Jul 1 – Oct 17 2026): `rows 288 shops 18 weeks 16`, `Eldoret Jul-Oct conversion 93.1%`,
WhatsApp shops cover every mapped shop: `mapping gaps: set()`.
Low-count shop-weeks: Eldoret 15, Nakuru 15, Meru 13, Starmall 13, Kakamega 12; Hilton 16,951 visitors.
## 3. Generator — DONE
generators/footfall_marketing.py → data/footfall_marketing.json (+ FOOT_DATA block once the page exists).
Verify: `Footfall and Marketing: 18 shops, 16 weeks (28 Jun–4 Jul to 11–17 Oct), 9 actions.` exit=0;
JSON `shops 18 weeks 16`.
Fixes found while verifying: 6–10 Oct was barely counted (38 of 126 shop-days) → weeks with < 70% of
shop-days are 'partly counted' (shop-weeks < 5 days too): left out of correlations, tiles compare the last
fully counted weeks (11–17 Oct vs 27 Sep–3 Oct). Ads correlations need 6+ weeks (only 4 in ads_weekly.csv)
→ "not enough weeks to tell". Kakamega 6–12 Sep has a 4,444-unit line (KES 12M) → bulk, flagged as suspect.
## 4. Page — DONE
html/footfall_marketing.html (tiles, shop week-on-week chart + separate posts / ad-spend charts, ranking,
posts and ads vs visitors, what we can do, data quality; page_sidebar.js, Chart.js 4.4.0, chart_switcher.js).
dashboard_pages.json: "Footfall and Marketing" order 12 (after Shops Efficiency, later pages +1), scripts
[footfall_marketing.py]. generators/ads_impact.py PAGES: footfall_marketing.html → ("shops", ["shops"]).
Verify: `FOOT_DATA_START 1 FOOT_DATA_END 1`, `inline script 0/1/2: ok` (node --check), `dashboard_pages.json loads`,
`dot separators in page: 0`, `ads section for footfall page: True`.

## 5. Actions — DONE
Built in generators/footfall_marketing.py actions(): count looks low (one item listing shops), Hilton, high
traffic low conversion, fast WhatsApp but walk-ins falling more than all shops, posts / ads vs next-week
visitors per market, bulk orders (⚠ + reason + without-bulk figure, 100+ unit lines flagged as suspect).
Verify: `actions 9 each has a name and a number: True`.
## 6. Visual check — DONE
pixelshot html/footfall_marketing.html --viewport-width 1400 (3 tiles, complete). First pass failed: the main
chart drew before page_sidebar.js narrowed the column (last bar cut off, sideways scroll) and the chart
menu icon covered the ad-spend axis label. Fixed: charts resize on load / 300 ms / 1 s, min-width 0 on chart
boxes, chartSwitch off on the two small charts. Re-shot: all 16 weeks inside the panel (4–10 Oct shown as a
gap), no clipped labels, no empty charts, no sideways scrollbar, tables fit, sidebar beside the content,
`grep -c " · "` = 0.

## 7. Wrap-up — DONE
`python -m py_compile lib/footfall.py generators/footfall_marketing.py generators/ads_impact.py lib/ads.py
streamlit_app.py` → all ok. `graphify update .` → "Code graph updated".

### Findings (16 weeks, 28 Jun – 17 Oct 2026; last fully counted week 11–17 Oct)
- **Top 3 shops by walk-in conversion with a believable count (last 4 weeks):** Kisumu 78.1% (253 buyers
  of 324 visitors, count low in 1 of 4 weeks), Nanyuki 65.2% (107 of 164), Mombasa 59.0% (422 of 715).
  Ktda has by far the most visitors among comparable shops (2,023) but the lowest conversion (47.9%).
- **Counting is the biggest problem:** 10 shops have a "count looks low" week in 2+ of the last 4
  (Eldoret 87.4%, Nakuru 85.9%, Meru 85.4%, Hazina 84.0% …); 116 shop-weeks over the 16 weeks.
  Hilton counts mall traffic (17,370 visitors, 58.0%). 4–10 Oct barely counted (38 of 126 shop-days).
- **Posts and visitors (each shop vs its own average, posts a week earlier):** Kenya weak negative
  (r = -0.15, 110 shop-weeks), Tanzania moderate positive (r = 0.33, 12), Uganda weak positive (r = 0.15, 15).
  Posts and walk-in buyers: no link in Kenya and Uganda, weak positive in Tanzania. So in Kenya more
  posts did not bring more people to the door; posts work on online / WhatsApp sales more than footfall.
- **Ads and visitors:** not enough weeks yet (4 weeks of ads data); the page will say once 6+ weeks are in.
- **Bulk orders:** Kakamega 6–12 Sep has a 4,444-unit line (KES 12.0M) and Mombasa 20–26 Sep a 721-unit
  line (KES 1.9M): probably not real walk-in sales, flagged for checking.
- WhatsApp ad-lead conversion fell from 10.8% to 7.5% week on week; visitors −14.4%, walk-in conversion
  −6.5 points (11–17 Oct vs 27 Sep–3 Oct).
