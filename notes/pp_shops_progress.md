# Product Performance — Shop breakdown: progress

## 1. Spec — DONE
docs/product-performance.md: new "### 2b. Shop breakdown" (follows Market / Period / Share by, shop naming,
chart, table with ⚠ bulk flag + without-bulk change, drill-down, PP.shops data shape); sidebar line lists
Shop breakdown. Verify: `grep -c "Shop breakdown" docs/product-performance.md` → 2.

## 2. Data — DONE
generators/product_performance.py: shop_name() + shop_breakdown(lines, P) from the lines build() already
loads (no new query) → PP.shops[period][ALL|KE|TZ|UG] = {total, rev, shops:[{shop, mkt, units, rev, pUnits,
pRev, chg, chgPct, share, revShare, bulkUnits, pBulkUnits, chgNoBulk, chgPctNoBulk, bags[top 10]}]}.
Verify: generator exit=0 (only SQLAlchemy "Exception during reset" pool noise from a dropped connection);
injected PP: `periods with shops: ['lastmonth', 'lastweek', 'monthly', 'weekly']`,
`lastweek ALL shops: 21 sum units: 3628 total: 3628 botw total: 3628`.
Bulk check on real data: Hazina last week +456 units (+241%) is a 500-unit FEROZ line; without it −44.
Names: added `website sales` → Website, `staff pos` → Staff POS (doc updated).
## 3. Page section — DONE
html/product_performance.html: panel #pp-shops-panel (h2 "Shop breakdown") after Top-selling bags:
HTML/CSS bar chart (the page has no Chart.js; bars share one scale, coloured by market KE #3987e5 / TZ #d95926 /
UG #199e70, thin tick = the period before on the same scale, value + share at the bar end), table (Shop,
Market, Units, Share, Week on week / Month on month change with %, Revenue, ⚠ bulk lines + change without them),
click a bar or row → that shop's top 10 bags (units, share of the shop, change, revenue).
Verify: generator `gen exit=0`; `PP_DATA_START 1 PP_DATA_END 1`; `Shop breakdown h2: 1`;
`node --check all inline: True` (4 inline scripts).

## 4. Sidebar and sticky bar — DONE
Read the code: PageSidebar.init sections = every `.panel > h2` in `.psb-main`, name = text before " — "
(lines 678–679) → the new h2 "Shop breakdown — units by shop (…)" is listed as "Shop breakdown"; draw()
calls PageSidebar.refresh (646). Period select change → `state.per = per.value; save(); draw();` (664);
Market / Share by seg buttons → draw() (657, 661); draw() → drawShops() (628).
## 5. Visual check — DONE
pixelshot html/product_performance.html --viewport-width 1400 --tile-height 1568 (4 tiles, complete): Shop
breakdown shows 21 shops with bars, ticks and the table (real numbers: Hilton 773, Hazina 645, Ktda 326 …),
sidebar lists "Shop breakdown" beside the content, no clipped labels. Bulk wording fixed for a shop with bulk
lines only in the period before ("… in the period before, none now. Change without them: …").
Drill-down tested on a copy that clicks the Hazina row on load: `CLICK TEST: row found=true drill html
length=1609`, panel "Hazina: top bags" with FEROZ 502 (new, 77.8%), JUMBO 11, TRAVEL 11 …
Scrollbar check on every tile's bottom row: `looks like a scrollbar: False` ×4.
Middle dots: `in section HTML: 0 | in section JS: 0`.

## 6. Wrap-up — DONE
`python -m py_compile generators/product_performance.py` → py_compile ok; `graphify update .` → "Code graph updated".

### Summary
- **Top 3 shops by units last week (11–17 Oct, all markets):** Hilton 773 (−518, −40.1%; the week before had
  440 units on bulk lines, so without bulk it's −78, −9.2%), Hazina 645 (+456, +241.3%; 500 of them on one
  FEROZ bulk line, so without bulk it's −44, −23.3%), Ktda 326 (−42, −11.4%, no bulk).
- **Bulk orders found (last week vs the week before):** Hazina 500 units now; Hilton 440 units before;
  Kisumu 20 now and 199 before. All stay in the totals and are flagged ⚠ with the without-bulk change.
- **Left out / to know:** corporate-app invoices are not in this page (POS only, like the rest of Product
  Performance); Staff POS and Jumia tills show as their own rows (Jumia 0 units last week, listed because it
  sold the week before); the chart is HTML/CSS bars (the page has no Chart.js), so the chart menu doesn't
  apply to it.
