# Bags on offer vs not on offer

- **Generator:** `bags_on_offer.py` (reads `bags_offer_source.json`, written by `self_made_combos.py`)
- **HTML:** `bags_on_offer.html`
- **Data markers:** `<!-- BOO_DATA_START -->…<!-- BOO_DATA_END -->` (const `BOO`)
- **Scope:** **Kenya only** (every till except `sinza`, `dar-es-alam`, `uganda`), plus Kenya
  corporate invoices.

A new metric **next to** Menu 4 — it does **not** replace anything there. The Self made combos
page keeps its Combos / Power Deals views and its own "Bags not on offer" panel unchanged.

## Period selector (Monthly / Weekly / Last week)

A **Period** dropdown (top right, same wording as New Products) switches the whole page. All three
are pre-computed by the generator into `BOO.periods.{monthly, weekly, lastweek}`:

| Period | Window | Trend chart | Odoo target used |
|---|---|---|---|
| **Monthly** | the live report month (`report_month.live_month_window()`), to date | revenue per Sun–Sat week | `period = 'month'` |
| **Weekly** | the current Sun–Sat week, to date | revenue per day | `period = 'week'` |
| **Last week** | the previous complete Sun–Sat week (may straddle the month boundary) | revenue per day | `period = 'week'` |

The chosen period is remembered per viewer (browser storage). Stock / days-of-cover on the
not-on-offer table are point-in-time (today's stock, this month's selling pace) in every period.

## Buckets

Every Kenya POS line in the window (returns netted, `qty <> 0`; delivery, customisation and
straps excluded) and every qualifying corporate invoice line falls into exactly one bucket:

| Bucket | Rule | Tag |
|---|---|---|
| **On offer** | a combo product (`name LIKE '%+%'`) — running *and* self-made, rung on the combo button | `Combo sale` |
| **On offer** | a single bag that resolves to a bag that is a **running-combo component**, a **Deal of the Week** or a **Power Deal** | `Combo component` / `Deal of the Week` / `Power Deal` (several allowed; money counted **once** — see *Counted by how it was sold*) |
| **Not on offer** | a single bag that resolves to a catalogue bag on no offer | — |
| **Not on offer** | a **new product** (MONTHLY_TARGET sheet, col I ✅ — the New Products list) that is on no offer, **even if it isn't in the price catalogue yet** (e.g. LaFemme) | `NEW` |
| **Others** | **gift bags** (POS `name ILIKE 'gift bag%'`), **laptop sleeves** (`LAPTOP SLEEVE…`), **samples** (`SAMPLE…`) and **corporate** sales (customer invoices, same qualifying rule as `sql/corporate_bags.sql`: posted `out_invoice`, paid / in payment or ≤25 % outstanding; product lines; `price_total`) | `Gift bags` / `Laptop sleeves` / `Samples` / `Corporate` |
| **Unclassified** | a single POS product that matches no catalogue bag and no new product | footnote count/revenue |

- A new product that **is** on an offer (Sep 2026: **Lola** — combo component, **Zoezi** — deal)
  stays **on offer** (its sales are offer sales) and carries the `NEW` tag there.
- The on-offer set and the bag resolver are the ones Menu 4 uses: `self_made_combos.py` exports
  `onOffer` (= `kenya_on`: `comboBags` + DoW + Power-Deal products) to `bags_offer_source.json`, and
  both pages classify with the shared `bag_classifier()`. So the Monthly not-on-offer revenue equals
  Menu 4's `SMC.bagsNotOnOffer.notOnOfferRevenue` **plus** the new products Menu 4 can't resolve
  (the generator prints both figures).
- New-product list: read from the sheet at build time; if the sheet can't be read, the list from
  the previous build (`BOO.newProducts`) is reused.

## Counted by how it was sold

Every sale is counted **once**, in the channel it actually went through (agreed Sep 2026):

- **Printed inside a combo** (rung on the combo button) → the **Combo sales** row — whatever
  else the bag is on. E.g. Sep 1–24: **367 Jumbos** were printed inside combos (290 in
  Jumbo + Jumbo, 77 in Jumbo + Standard/Liam + …) → Combos.
- **Sold singly** → the offer the single sale belongs to, in this order:
  **Power Deal → Deal of the Week → Combo bag sold singly**, and if none applies → **not on offer**.
  A sale is a **Deal of the Week** sale only if it happened **at a shop running that deal, in its
  tier's weeks** (Tier 1 = Wk 1–2, Tier 2 = Wk 3+; `dowRuns` in `bags_offer_source.json`). A DoW
  bag sold elsewhere / at another time is not a deal sale — e.g. Jumbo sold at Hilton counts as a
  combo bag sold singly, Kai sold outside its deal shops/weeks is not on offer. A Power Deal runs at every shop
  all month, so a single sale of a bag that is both (e.g. Jamela) is a Power-Deal sale; the
  722 single Jumbos (a Deal of the Week + combo bag) → Deal of the Week.
- The rows of *Where the on-offer money comes from* therefore sum exactly to the on-offer total.

**Bags printed inside combos** come from Odoo's combo **sub-lines** (`sub_product_line = true`):
one line per bag inside every combo, with the exact colour variant and a KES 0 price — they cover
every combo exactly (Sep: 2,053 bags across 946 combo orders). Sub-lines are therefore **excluded
from single sales** (else each combo bag counted twice). Combo **returns** have no sub-lines, so for a
returned combo the bags come from `combo_product_attribute_values` (padded to the combo's bag count,
name split on `+` if empty). Units only — combo **money** stays on the combo line in Combo sales.

**Colour coverage (audited 25 Sep 2026):** every product variant resolves to its bag — colours,
finishes (CRACKED, SPICE, WOOVEN, CHOCO, CN, ANTELOPE, PATTERN), `[REJECT]` clearance variants and
`[S_0]`-style codes. New products are matched on every variant too (e.g. Lamora Black / Brown /
Red / Sky Blue; LaFemme's four colours exist in Odoo, created 21 Sep, none sold yet). Laptop sleeves and
samples are counted as sales under **Others** (added 25 Sep 2026); only foam cleaner, the 300-KES
discount reward and a couple of one-off items (Enzo, KCB briefcase) stay unclassified.

## What the page shows (per period)

1. **Money KPIs** — on-offer, not-on-offer and others revenue (KES) + units; on-offer share of
   all revenue; average price per unit (on vs not on offer); under-performing shops.
2. **Trend** — on offer / not on offer / others revenue per week (Monthly) or per day (weekly periods).
3. **On-offer breakdown by source** — Combo sales / Deal of the Week / Power Deal / combo bags
   sold singly — counted by how it was sold (above). Bar length is relative to the largest row.
4. **Shops by region** vs their Odoo target (below). Gift bags show in each shop's **Others** column.
5. **Bag tables** — on-offer bags: offer tags, `NEW`, **in combos** (units printed inside combos),
   **sold singly** (units), which row the singles count in, and singles revenue. Not-on-offer bags:
   `NEW`, sold singly, in combos (self-made combos), revenue, stock, days of cover.

## Shop metrics (vs the Odoo revenue target)

- **Target:** `sales_pos_target`, `target_scope = 'pos'`, `period` = month or week (see the period
  table), latest row whose `start_date…end_date` overlaps the window; `config_id → pos_config.name`.
- **Corporate** gets its own row (region **Corporate**) against the `target_scope = 'corporate'`
  row of the same period; its revenue is the corporate invoices above.
- **Revenue vs target:** the shop's **total till revenue** in the window (all POS lines,
  `SUM(price_subtotal_incl)`, returns netted) — the target covers the whole till.
- **Attainment %** = revenue ÷ target. **Pace %** = revenue ÷ (target × days elapsed ÷ days in the
  period) — Last week is complete, so its pace = attainment.
- **Region:** till name → shop label (`_SHOP_TO_LOC`) → region from [shop-regions.md](shop-regions.md);
  sorted by pace; best pace = **Region leader**.
- **Red = under-performing:** pace **< 100 %** **and** below its **benchmark** — the region's pace
  (2+ targeted shops) or the Kenya-wide POS pace (one-shop regions: Coastal, Online, Corporate).
  Behind target alone flagged every shop mid-month (Sep 2026 day 24: all 17 at 43–81 %).
- **Amber** = behind target but at/above its benchmark; **green** = pace ≥ 100 %. No target row
  (Staff Pos, Jumia) → "no target", never red; tills not in shop-regions.md → **Other**.

## Regenerate

```
python self_made_combos.py    # writes bags_offer_source.json (on-offer set + not-on-offer list)
python bags_on_offer.py       # DENRI_LAUNCHER=1 to skip the browser tab
```
If `bags_offer_source.json` is missing or older than 15 minutes, `bags_on_offer.py` rebuilds it
live by running `self_made_combos.fetch()`.

## Layout (laptop / tablet / phone)

- **Laptop (> 820px):** full tables; the six KPI cards sit in one row; the two bag tables are
  stacked full-width (side by side they were too narrow — columns were cut off).
- **≤ 820px (tablet, narrow window, Streamlit with the sidebar open on a small laptop):** every
  table (`table.rt`) turns each row into a labelled card (`td[data-label]`), 4 values per line on a
  tablet, 2 on a phone — nothing scrolls sideways. Under-performing shops keep the red card.
- **≤ 700px (phone):** KPI cards 2 per row, tighter padding/fonts, shorter chart. The bag lists
  keep their own scroll (36rem) so the page doesn't become endless.
- Stock / days of cover are filled for **every** not-on-offer bag from `stockMap` in
  `bags_offer_source.json` (Kenya stock, sheet + Odoo live) ÷ this month's pace on the days the bag
  sold (single sales + combo prints).
- Check changes at 390px in a real narrow frame — headless Chrome won't shrink a window below
  ~500px, so a plain `--window-size=390` screenshot is cropped, not reflowed.
