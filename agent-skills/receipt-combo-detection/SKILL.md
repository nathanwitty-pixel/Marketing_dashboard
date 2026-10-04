---
name: receipt-combo-detection
description: Detect bundles/combos from POS receipts when the till rings every item as its own line (items on one receipt at a shared or split price), and classify each as running (matches a combo on the month's offer list, any order, alternatives, closest-name matching for misspelt or short names) or self-made, with bulk receipts, refunds and rounding handled. Use when measuring combo/bundle sales, running vs self-made combos, what customers pair together, or matching till product names to an offer list.
---

# Combos from receipts — running vs self-made

Some tills don't have a combo button: a customer buying two bags gets two lines on one receipt. This skill
turns receipts into combos and singles, and matches them to the month's offer list.

Scripts (pure Python): `scripts/receipt_combos.py` (`classify`) and `scripts/name_match.py`
(`match_offer` for till products that **are** named combos, e.g. "Jumbo Grey + Jumbo Black Combo").

## Receipt rule (per receipt)

1. **Drop refunded receipts** — a `<ref> REFUND` receipt cancels the original (pass `ref` on each line).
2. **≥ BULK_MIN (5) items = bulk** (wholesale) — reported apart, never a combo.
3. Items at the **same unit price** (rounded to the nearest 10 so 40,000 / 40,001 match) = **one combo per
   price** (a 4-item receipt at two prices = two combos).
4. Items left over: **two or more = one combo** (some tills split a combo's price unevenly, e.g. 115,000 +
   70,000); **one = a single**.
5. Delivery, gift wrap, discount lines, straps and customisation are not products (`_SKIP`).

A combo is **running** if its item types fill a listed combo's **slots** one-to-one (same count, **any
order**, alternatives allowed); otherwise **self-made**, labelled by its sorted item types. A single counts
against a listed single when its type matches.

## Inputs

- `lines` — `{receipt, ref, d, product, qty, amount}` per receipt line (all lines incl. refunds), for the market's tills.
- `offers` — the month's list: `{"combos": [{name, slots: [set(types)]}], "singles": [...]}`; build slots from
  labels like `"AMAYA/ELYSE + MOON/NIZANA"` (`+` between slots, `/` between alternatives) in catalogue types.
  Keep the list in a monthly CSV the user sends (Month, Market, Type, Name, Bags, Was, Now, Disc, Currency).
- `infer(name)` — product name → catalogue type (longest-prefix match against the catalogue), None for non-products.

## Outputs to show

- Running vs self-made: combos sold, distinct pairings, revenue (local currency + home currency in brackets
  when markets differ, with the rate stated); self-made share.
- Repeating self-made combos list with **sale dates** (`days`), and "bags customers keep pairing" (types that
  recur in self-made combos and whether they're on the list — candidates for next month's list).
- Per running combo: weekly sales, and **what people chose instead** — the self-made combos that contained
  each of its items.
- Weekly "target to beat last month": last month's combos (running + self-made) vs this month so far.

## Name matching (`name_match.py`)

Normalise each slot option (drop category and colour words, apply promo aliases), then: exact slot overlap in
list order → exact in any order → **closest names** (`opt_close`: equal ignoring spaces, word-prefix unless the
short word is too vague like "MINI", or ≥ 85 % spelling). Configure `_COMBO_CATEGORY`, `_COMBO_COLOURS`,
`_COMBO_PHRASE_ALIAS`, `_BARE_CATEGORY_ALIAS`, `_OPT_TOO_VAGUE` for the catalogue. Before switching on a new
matcher, compare old vs new matches across all product names — none of the old matches should change.

## Tests

`scripts/test_receipt_combos.py` — `python -m pytest scripts -q`.
