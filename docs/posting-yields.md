# Posting – Sales Yields from Accurate Posting

- **Generator:** `POSTING (SALES YIELDS FROM ACCURATE POSTING).py`
- **HTML:** `POSTING (SALES YIELDS FROM ACCURATE POSTING).html`
- **Data marker:** `<!-- POST_DATA_START -->…<!-- POST_DATA_END -->` (const `PA`)

## What the page shows

**Sidebar** ([page sidebar](README.md#page-sidebar)) — **Regions** picker (Kenya · Sinza · Uganda) replaces the three in-page tab rows (hidden; one click switches all of them), then the region's headline cards and its Accuracy / Dead Stock groups with folding sub-items.

How well marketing's **posting** lines up with actual **sales**, per region (Kenya /
Sinza / Uganda), with a weekly/monthly toggle.

1. **Marketing & Sales Alignment — posting yield (rebuilt 28 Sep 2026).** Measured the way
   marketing measures it, per region, Monthly / Weekly:
   - **Posts** = every post on MONTHLY / WEEKLY_MARKETING_POST (col E Kenya, F Sinza, G Uganda) —
     **all rows**, not only col-I ✅ (col I is the on-offer flag; the weekly Kenya total is 974 =
     667 x + 307 ✅). Rows keyed by product name (a blank colour cell no longer drops posts).
   - **Expected** = posts × expected sales per post (Kenya 225,000 × 5% × 1% × 2% = **2.25**;
     Sinza 1.4; Uganda 0.0216). E.g. 974 × 2.25 = 2,191.5.
   - **Sold** = Odoo sales of that bag in the **same window** as the sheet: monthly = report
     month; weekly = last complete Sun–Sat week (the week the weekly sheet describes).
   - **Credited** = min(sold, expected) per bag — selling above expected counts as 100%
     (Antitheft Black: 17 posts → 38.25 expected; 12 sold = 31%).
   - **Achieved** = Σ credited ÷ Σ expected. This is now also the headline
     `wkMktPct / moMktPct / szMoMktPct / ugMoMktPct` (and the Monthly Report's figure). The old
     figure divided sales by *posts* (not posts × 2.25) and averaged per bag.
   - **Shop stock** = live Odoo on-hand at the region's shops — bags already received by the shops
     (not warehouse / in transit).
   - **On offer vs not on offer** (added 28 Sep 2026): each posted bag is tagged `onOffer` from
     the region's live offers (Self-Made Combos set, `_bt_on_offer` on its bag type), and the same
     yield is given for each side (`on` / `off`) — shown as two comparison tiles plus a
     **Segment** filter (All / On offer / Not on offer) and an On-offer column. Both sides are
     measured identically (posts × spp, capped per bag).
   - **Periods:** *Monthly* (report month) · *Last week* (weekly posting sheet + Odoo sales for
     the same Sun–Sat days) · *This week* (0 posts — marketing tallies a week's posts the
     following week, so there is nothing to measure until it closes).
     Data: `PA.postYield`, `PA.sinza.postYield`, `PA.uganda.postYield` (`_post_yield()`), keys
     `monthly` / `lastweek` / `thisweek` (`weekly` = `lastweek`, kept for older readers).
2. *(Removed 28 Sep 2026: the old POSTED × SOLD / NOT POSTED × SOLD on-offer cards.)*
2b. **Dead Stock Clearance (added 28 Sep 2026)** — sits under the alignment card in each region,
   same windows (Monthly / Last week) and the same on-offer set. Instead of sales vs posts it asks
   *is the stock we hold clearing*, split **posted vs not posted × on offer vs not on offer**
   (2×2 tiles, click a tile to filter the table; Group by bag + colour family):
   - **Universe** = every bag the region's shops had stock of (Odoo on-hand at the shops — bags
     already received, not warehouse / in-transit).
   - **Available** = stock at the period end + units sold in the period. Period-end stock = today's
     shop on-hand with Odoo stock moves after the period rolled back (`_region_net_moves`).
   - **Cleared %** = sold ÷ available (per bag and per segment, Σ sold ÷ Σ available).
   - **Still dead** = had stock available and sold 0.
   - **Posted** = ≥1 post on the period's posting sheet. Data `PA.deadClear` (+ sinza/uganda),
     `_dead_clear()`.
3. **Marketing Alignment with Clearing Dead Stock** — a gauge (reframed from the old
   dead-stock donut) showing how aligned marketing is with clearing dead stock.
4. **Visibility carry-over** — will last week's posts still be relevant this week, given
   live stock (`_post_relevance`).
5. Header `<th title=…>` tooltips explain Alignment, Dead-stock effort, Sold · no
   marketing, Not sold · untouched.

## Custom range (Oct 2026)

The **Posting yield** and **Dead Stock Clearance** Period dropdowns (all three regions) get **Custom
(dd Mon – dd Mon)** when a range is set — picker and rules in
[README › Custom range](README.md#custom-range-oct-2026); range file `py_custom_range.json`, data
`PA.custom`. **Sales & stock only** — the posting sheets only hold monthly / weekly post totals, so a
custom range has no post count:
- **Posting yield** (`postYield.custom`, `_post_yield(..., sales_only=True)`): every bag **sold** in the
  range (Odoo `MONTHLY_SALES` layout built for the window), with sold, on-offer flag and shop stock;
  Posts / Expected / Credited / Achieved show "—". The on / not-on-offer tiles show bags sold, units sold
  and shop stock. Sorting by expected or % falls back to sold.
- **Dead Stock Clearance** (`deadClear.custom`): same clearance maths (available = stock at the range end
  + sold in it; stock rolled back with `_region_net_moves` when the range ends before today) — one row,
  **On offer vs Not on offer**, and "All bags N% cleared"; the posted split isn't shown.
- **Dead Stock Accountability** (Monthly / Weekly) has **no** Custom: its coverage and conversion are
  built on post counts, so a range would read as 0 % posted.
- Checked 6 Oct 2026 with 01–30 Sep: Kenya 15,450 sold over 593 bags, dead stock 59.4 % cleared.

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

**Non-bags excluded from stock (28 Sep 2026):** STOCK_LEVELS rows for `sales_exclusions.txt`
products, gift bags, wipes/cleaners and "Buy X get Y free" promo products are dropped before any
section runs — they are never posted, so they inflated "in stock, not posted" (1,673 promo units +
1,144 wipes). `s3Posted / s3NotPosted` are Kenya stock **on offer / not on offer**; the monthly
never-posted figure is `moInstockNotPostedSum`, with its bags in `moInstockNotPostedList`.
