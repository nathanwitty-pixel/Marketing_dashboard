# Ralph task — Sinza & Uganda offers + receipt-based combo counting

Repo `c:\Users\jonat\Desktop\Marketing_dashboard`. Orient with graphify (`graphify query`, `graphify explain`).
Log in `OOS_PROGRESS.md` › "Sinza & Uganda". Never commit / push / run publish.bat.

## Inputs (from the user, Oct 2026)
- Sinza (Tanzania) singles + combos and Uganda singles + combos with prices — transcribed into
  `offers_monthly.csv` (Month, Market, Type, Name as given, Odoo name(s), Was, Now, Disc, currency, KSH).
  Sinza combos: the user's sheet columns are offer KSH · offer TSH · S.P (TSh selling price) · was KSH ·
  was TSH · DISC (= was TSH − S.P). Uganda: was / now / disc in USh; the last number = KSH equivalent.
- POS rule (Sinza = tills `sinza`, `dar-es-alam`; Uganda = `uganda`): these tills ring every bag as its own
  line. **A receipt's bags that share one unit price = one combo** (≥ 2 bags); a bag alone at its price =
  a single. A combo whose bags match a listed combo (any order, `_opt_close` closest names) = **running**,
  else **self-made**. Receipts with ≥ 7 bags = bulk, reported apart. Delivery / gift bags / non-bags ignored.

## Steps
1. CSV — all 30 offers, every Odoo name resolves (prefix-match ≥ 1 active product). VERIFY script.
2. Docs — docs/self-made-combos.md: new section (source file, receipt rule, bulk, matching). VERIFY grep.
3. Code — `lib/receipt_combos.py`: receipts → groups → classify; tests/test_receipt_combos.py (price
   grouping, 4-bag receipt = 2 combos, single, bulk, delivery ignored, running vs self-made, any order).
4. Page — Sinza/Uganda region cards use the CSV list (fallback: sheet) and POS weekly sold; new
   self-made panel per region; singles sold from single receipts. VERIFY build exit 0 + data keys.
5. Finish — pytest all, AppTest, `graphify update .`, summary.

Done → `<promise>OUTSIDE_COMBOS_DONE</promise>`.
