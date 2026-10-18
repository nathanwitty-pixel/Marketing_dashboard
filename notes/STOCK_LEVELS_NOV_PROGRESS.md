# Shop Stock Levels — November finish (Ralph loop, started 18 Oct 2026)

- [x] 1. Bag health categories + health % in Stocks report — by bag (chips filter, columns)
- [x] 2. November bag targets from KES 66,632,243 (product_targets_2026-11.csv) → next month's need
- [x] 3. November preparedness: shops only vs with CBD + VLD, buffer stock, KPI pair, by-bag table
- [x] 4. Corporate by Client: % labels on both tabs' bar charts
- [x] graphify update . run after the last code change

## Log
- 1: spec 'Bag health' table (Out of stock / Low cover / Overstocked / Healthy / Dead stock, need-weighted Health %). Page: chips + Health + Health % columns. node --check OK. dump-dom: All 175 = oos 13 + low 33 + over 51 + ok 49 + dead 29; 134 visible rows (Needs action), every row has a category.
- 2 (partial): product_targets.REVENUE_TARGETS {"2026-11": 66,632,243} + total_for(); `python -m lib.product_targets 2026-11` → 33,313 bags (KES 2,000.17/bag from October's Odoo targets), CSV 133 bags summing exactly 33,313. Top: JUMBO 2,279 · ANTITHEFT 2,241 · CODE 3 1,995 · MAN BAG 1,593 · FABELA 1,448 · TRAVEL 1,196 · PRIME 928 · MINI MAYA 901 · BIG MAN BAG 785 · MEGA 752. Generator wired (Oct shop targets × 33,313 / Oct grand total; Nov base Aug–today). Page note added. Awaiting generator run for the page check.
- 4: docs/current-performance.md rule; corpBarLabels(f, extra) — end labels "N · share% · x% of target", tooltip lines. node --check all 6 scripts OK. Probe (headless Edge): app shares [44,36,2,2,2,1,0,0,0,11,2] = 100; shop shares [41,38,4,16,1] = 100; PERF.corporateTarget = 1,163 bags.
- Also (pre-loop request): Right qty counted once per shop × product — Sep 13,467 asked vs 20,716 suggested (was 43,683).
- 2: generator run 21:52 — nextMonth source=revenue, 33,313 bags, KES 2,000.17/bag, shops 31,930 (Oct shop targets × 33,313 / Oct grand total). IPF fitted every shop exactly to its scaled target (Ktda 3,017, Starmall 2,237, Website 2,263 …). Shop rows sum 29,697 = 31,930 − Website 2,263 (online, no shelf) ± rounding. Page note "from the KES 66.6M revenue target" shown.
- 3: CBD/Stock 3,165 + VLD/Stock 5,058 = lib/stock odoo_stock_at_location exactly. dump-dom: KPI block + table present; 130 rows, 0 with buffer ≠ with − without. Footer = payload sums: need 29,696 (1 unit sits on a hidden 'none' row), shops 14,554, with 22,768, buffer 8,214. Prepared Nov: shops only 10% → with CBD + VLD 34%; short 26,785 → 19,510.
- graphify update . run after the last code change (graph.json 22:02).
