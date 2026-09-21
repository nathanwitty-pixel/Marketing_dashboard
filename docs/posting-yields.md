# Posting – Sales Yields from Accurate Posting

- **Generator:** `POSTING (SALES YIELDS FROM ACCURATE POSTING).py`
- **HTML:** `POSTING (SALES YIELDS FROM ACCURATE POSTING).html`
- **Data marker:** `<!-- POST_DATA_START -->…<!-- POST_DATA_END -->` (const `PA`)

## What the page shows

How well marketing's **posting** lines up with actual **sales**, per region (Kenya /
Sinza / Uganda), with a weekly/monthly toggle.

1. **Marketing & Sales Alignment — POSTED × SOLD.** The posted-vs-sold universe split into
   **On-Offer** vs **Not-On-Offer** bags. Each side reports: posted & sold, posted & not
   sold, sales-driven (sold, no marketing), not-posted & unsold — with percentages and a
   bar chart per metric.
2. **NOT POSTED × SOLD** companion — bags that sold with **no** marketing activity
   ("Sold · no marketing (Sales-driven)") vs "Not sold · untouched".
3. **Marketing Alignment with Clearing Dead Stock** — a gauge (reframed from the old
   dead-stock donut) showing how aligned marketing is with clearing dead stock.
4. **Visibility carry-over** — will last week's posts still be relevant this week, given
   live stock (`_post_relevance`).
5. Header `<th title=…>` tooltips explain Alignment, Dead-stock effort, Sold · no
   marketing, Not sold · untouched.

## "On offer" definition (per region)

A bag is **on offer** if it appears in that region's active promos — read live from the
`self_made_combos.html` SMC block (`_offer_bagtypes_by_region`), the **single source of truth**:

- **Kenya:** running-combo component bags **+** Power Deals **+** Deal of the Week.
  (Running combos are split into their individual component bags.)
- **Sinza:** Combos **+** Singles.
- **Uganda:** Combos.

This SMC offer set (per region: `_ob_ke` / `_ob_sz` / `_ob_ug`) now drives **every** on/not-on-offer
split — the marketing alignment, **Dead Stock**, and the **on/not-on-offer STOCK** figures
(Kenya `s3NotPosted`, Sinza/Uganda `stockNotOnOffer`, which the Monthly Report §4 consumes). It
**replaces the old STOCK_LEVELS / MONTHLY_TARGET ✅/x sheet flags**, which were manually maintained
and stale — they misfiled bags that were genuinely in a combo/DoW/Power-Deal, over-counting
"not on offer" (e.g. Kenya not-on-offer stock **5,572 → 2,613**). Matching uses `_bt_on_offer()`
with the **same prefix logic** as the combos page, so a stock bag "Jumbo" matches a "Jumbo travel"
deal and vice-versa (exact membership missed those). Only the MMP/WMP posted-alignment split
(sheet col I/AB) still reads its flag from the sheet.

## Alignment universe (the ~654, not ~1,200)

`_alignment_region()` builds the universe as `sold_keys ∪ stock_keys ∪ posted_keys`,
**restricted to region-present bags**. The whole catalogue (~1,200, incl. 0-stock/0-sales
items) is *not* the universe — that over-counted. Kenya lands ~654 (week) / ~700 (month).

## Data sources

- Marketing posts + sales + stock from the same sheets New Products uses
  (WEEKLY/MONTHLY_MARKETING_POST, WEEKLY/MONTHLY_SALES, STOCK_LEVELS).
- **Live stock fallback** from Odoo when the sheet shows 0 — 16 named Kenya shops for
  Kenya, DAR for Sinza, UG for Uganda (see [README](README.md) stock codes).
- Combo component sales are attributed to the **actual bag printed** (same principle as
  Self Made Combos), so an on-offer bag's sales reflect what really moved.

## Regenerate

```
python "POSTING (SALES YIELDS FROM ACCURATE POSTING).py"
```
Run **after** `self_made_combos.py` (it reads that page's SMC block for the on-offer sets).
Injects `alignment` (per region, `{monthly, weekly}`) and `postRelevance`.
</content>
</invoke>
