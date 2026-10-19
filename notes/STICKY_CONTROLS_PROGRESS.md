# Sticky controls — filter bar follows the reader (Ralph loop, started 19 Oct 2026)

- [x] 1. assets/sticky_controls.js (StickyControls.init) + docs/sticky-controls.md
- [x] 2. Test harness notes/sticky_test/ (standalone + embedded checks)
- [x] 3. product_performance wired + redraw check
- [x] 4. Other 10 pages wired
- [x] 5. Final table + graphify update .

## Log
- 1: assets/sticky_controls.js (StickyControls.init/update; transform pin standalone + embedded below .tn-bar; pinned bg + shadow + compact; bottom-margin compensation; clamp to page end). node --check OK. docs/sticky-controls.md + README pointer.
- 2: notes/sticky_test/run.py (standalone probe copy in html/ scrolled 3000; embedded harness: fixed 56px .tn-bar + srcdoc iframe with local scripts inlined, sized to full height, parent scrolled 3000; --set SEL=VAL / --click / --read redraw check). Baseline before wiring: top -2683 both, no errors.
- 3: product_performance wired (.controls) + spec line. standalone top 0, embedded top 56, pinned; after --set #pp-period=lastmonth + click Kenya: change heading reads "Month on month", bar still at 0 / 56; no JS errors; node --check all scripts OK. Also removed the " · Market" dots from 5 panel titles.
- 4 (in progress): script reworked for many bars (init per bar, within = section bound, stacking, ResizeObserver, overflow-anchor none, ceil rounding). Harness: --at, --set, instant scroll, frame re-sync every 100 ms, one frame-scroll event before measuring (headless dump-dom delivers no frame scroll events after anchoring). Passing: shop_stock_levels (.controls, 0 / 56, Show All redraw), bags_on_offer (#boo-ctl, 0 / 57, period weekly redraw), self_made_combos (#smc-oos-bar + Type bar within Kenya view, 1 / 57, Power Deals redraw).
- 4: wired the other 10 pages (new_products, posting_yields via initSections; shops_efficiency, timed_offers, history with watch; offer_picking search wrapped in .se-ctl; monthly_report Sort). Script gained within / watch / stacking by visible part / headerOf + initSections. Each spec has its line.
- 5: first full run caught a 'ResizeObserver loop completed with undelivered notifications' error on shop_stock_levels (re-measuring inside the observer changed the bar margin) → re-measure deferred and only on a real height change. run_all.py then passed all 11 rows twice in a row (standalone 0–1 px, embedded 56–57 px, redraw while pinned ok where the page has a period / sort, node --check ok, 0 JS errors); graphify update . run after:

| Page | Bar selector | Standalone top (0–8) | Embedded top (56–72) | Redraw while pinned | node --check | JS errors | Result |
|---|---|---|---|---|---|---|---|
| product_performance.html | `.controls` | 1 | 57 | ok | ok | 0 | pass |
| shop_stock_levels.html | `.controls` | 1 | 57 | ok | ok | 0 | pass |
| bags_on_offer.html | `#boo-ctl` | 1 | 57 | ok | ok | 0 | pass |
| self_made_combos.html | `#smc-oos-bar` | 1 | 57 | ok | ok | 0 | pass |
| new_products.html | `div:has(> #pt-title)` | 1 | 57 | ok | ok | 0 | pass |
| posting_yields.html | `[data-sticky-controls]:has(#py-k-period)` | 1 | 57 | ok | ok | 0 | pass |
| shops_efficiency.html | `.filter-bar` | 1 | 57 | ok | ok | 0 | pass |
| timed_offers.html | `.to-ctl` | 0 | 56 | ok | ok | 0 | pass |
| offer_picking.html | `.se-ctl` | 0 | 56 | n/a (search box) | ok | 0 | pass |
| monthly_report.html | `[data-sticky-controls]:has(#np-sort)` | 1 | 57 | ok | ok | 0 | pass |
| history.html | `.sortbar` | 0 | 56 | ok | ok | 0 | pass |
- 19 Oct: Shop Stock Levels removed again (user: make it static); run_all.py now 10 pages.
