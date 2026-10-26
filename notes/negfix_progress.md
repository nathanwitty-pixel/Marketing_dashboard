# Stock record accuracy (NEGATIVE FIX LOG) — progress

## 1. Spec — DONE
docs/shops-efficiency.md: "## Stock record accuracy (22 Oct 2026, user's call)" (source, which rows count,
shop → till mapping, periods incl. Since the log started, measures, ranking, big one-off rule, where it shows,
the script). docs/README.md: data-source paragraph for the NEGATIVE FIX LOG.
Verify: `grep -c "Stock record accuracy" docs/shops-efficiency.md` → 2; `grep -c "NEGATIVE FIX LOG" docs/README.md` → 1.

## 2. Library — DONE
lib/negative_fixes.py: read() (APPLIED only, total rows skipped, m/d/Y dates, shops stripped, cached),
periods(today) (Last week, This week, This month, Last month + Since the log started), bags_sold() (POS,
bags_sold_total.sql filters by till), by_shop(), ranked(), block(). tests/test_sheet_reads.py: NEGFIX_MODULE /
NEGFIX_SHEET / NEGFIX_TAB allow exactly that sheet + tab from that module.
Verify: pytest is not installed here, so the test functions were run directly with Python →
`PASS test_only_the_main_spreadsheet`, `PASS test_only_three_tabs_are_read`, `PASS test_posting_sheets_tabs`,
`3 tests passed`. by_shop(4 Oct, 22 Oct 2026): `shops 17`; `HILTON fixes 23 big 0`; `KTDA fixes 23 big 0`;
`HAZINA fixes 19 big 3 [129, 60, 51]`.
## 3. Script — DONE
scripts/negative_fixes_report.py --period lastweek|thisweek|thismonth|lastmonth|sincelog (default lastweek):
ranked table (best first, fixes per 1,000 bags without big one-offs), change vs the period before, repeat
items, ⚠ big one-offs.
Verify: `--period sincelog` → ranked table of 17 shops (1 Kisii 7.7 … 17 Uganda 79.2), repeat items,
big one-offs (Hazina 13 Oct SPICE 129, BEIGE 60, CRACKED 51), `exit=0`; `lastweek exit=0`, `thisweek exit=0`,
`thismonth exit=0`, `lastmonth exit=0`.
## 4. Generator and data — DONE
generators/shops_efficiency.py: `_negfix()` → `SE.negfix = negative_fixes.block()` (None + a printed warning
if the sheet can't be read). Each period: label, start, end, prevStart, prevEnd, shops (ranked best first,
with prevFixes / prevRate), repeats, big, totalFixes; plus logStart, lastLogDate, big (10).
Verify: `DENRI_LAUNCHER=1 python generators/shops_efficiency.py` → `gen exit=0`; injected SE:
`negfix present: True`, `{'lastweek': 17, 'thisweek': 17, 'thismonth': 17, 'lastmonth': 17, 'sincelog': 17}`.
Note for the page: Last month (Sep) ends before the log starts (4 Oct) → must say "no log for this period",
not show 17 perfect shops.
## 5. Page section — DONE
html/shops_efficiency.html: `#negfix` after `#combo-shop` with `<h2 class="block-title">Stock record accuracy</h2>`
(the page sidebar collects `.block-title`) and a card rendered by its own script: period select (Last week
default, This week, This month, Last month, Since the log started; remembered per browser), HTML/CSS ranked bars
of fixes per 1,000 bags (green best third, grey middle, red worst third, number on the bar, ▼ green / ▲ red badge
for the change in rate vs the period before), table (Shop, Fixes + ⚠ big, Negative units, Bags sold, Fixes per
1,000 bags, Days with fixes, Repeat items, Fixes before with the change), Repeat items list, ⚠ Big one-offs list.
A period that ends before the log starts says "No log for this period" instead of 17 perfect shops.
Verify: `node --check all inline: True`, `SHOPS_DATA markers 1 1`, `h2: 1`.
## 6. Visual check — DONE
pixelshot html/shops_efficiency.html --viewport-width 1400 --tile-height 1568 (13 tiles, complete). The
section shows real shops and numbers (Last week: Busia, Kakamega, Kisii, Meru, Sinza, Thika 0 fixes … Uganda
108.1 per 1,000), no clipped labels, no empty chart, listed in the sidebar as "15 Stock record accuracy".
Fix: zero-rate shops had invisible green bars → a 1.2% stub so the colour shows.
`tiles with a sideways scrollbar row: 0 of 13`; middle dots `in section HTML: 0 | in section JS: 0`.
Last month (before the log): test copy → `noLogMessage=true rows=0`.

## 7. Wrap-up — DONE
`python -m py_compile lib/negative_fixes.py scripts/negative_fixes_report.py generators/shops_efficiency.py
tests/test_sheet_reads.py` → all ok. tests/test_sheet_reads.py (run directly; pytest isn't installed): 3 PASS.
`graphify update .` → "Code graph updated".

### Summary (since the log started, 4 to 22 Oct 2026; fixes per 1,000 bags sold, big one-offs left out)
- **Best 3:** Kisii 7.7 (2 fixes, 259 bags), Sinza 8.5 (2 fixes, 236 bags), Hilton 9.7 (23 fixes, 2,381 bags —
  the most fixes, but it sells the most).
- **Worst 3:** Uganda 79.2 (8 fixes, 101 bags), Nanyuki 73.0 (10 fixes, 137 bags), Kitengela 62.2 (12 fixes, 193 bags).
- **Top repeat items** (negative again after a fix): Hilton BLACK, Starmall A4, Thika BLACK (5 times again
  each); Ktda BLACK, Nakuru A3, Nakuru BLACK, Eldoret BLACK, Kitengela BLACK (4). BLACK and A4 are the usual suspects.
- **Big one-offs:** Hazina 13 Oct, SPICE 129, BEIGE 60, CRACKED 51 units (sheet rows 497–499).
- **Where:** Shops Efficiency → Stock record accuracy (own period select). **Script:**
  `python scripts/negative_fixes_report.py --period lastweek` (or thisweek, thismonth, lastmonth, sincelog).
