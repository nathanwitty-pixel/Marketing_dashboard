# Reject Sale (`reject_sales.py` → `reject_sales.html`, `RJ`)

A **clearance-sale pricing board** for the reject/second-grade bags — built for the
**Kitengela** offer sale. It takes the **uploaded reject list** (`reject_stock.csv`, ~599
units — *this list only*, not Kitengela's or any shop's live Odoo stock) and puts every bag
into one of three sale prices — **KES 1,000 / 1,200 / 1,500** — chosen against the bag's **BOM
production cost** so nothing is knowingly sold below cost.

## The pricing rule (two tiers + hand pins)

There are **two sale prices — KES 1,000 and 1,500** (no 1,200). The auto rule is a single
cost band (`BAND` in `reject_sales.py`):

| BOM cost | Sale price |
|---|---|
| ≤ **900** | KES **1,000** |
| > 900 | KES **1,500** (flagged "below cost" if cost > 1,500) |

The **mid-range bags are set one by one by hand** in `reject_overrides.json` (a pin overrides
the cost rule), because whether a ~KES 700–900 bag sells at 1,000 or 1,500 is a desirability
call, not a pure cost call. Current pins: **1,500** — Loop BP, Code 3, Big Man Bag, Monah BP,
Liam, Karina, Mini Zuri, Spark, Tyler, Kaz; **1,000** — Man Bag, Kate, Zane Man, Leila, Avana
HB, Oval Handbag, Aria Pro. Split with these pins: **34 bags @ 1,000 · 43 @ 1,500** (599 units,
≈ KES 756k revenue). Every bag keeps a positive margin — except:

- **Below cost** (`flag: "below"`) — bag costs **more than 1,500**, so even the top tier loses
  money. Currently: *Alpha Travel, Baby Bag, Jamela, Pocket Travel, Sarai*. Hold them, or pin
  a higher price. Shown with a red pill and listed in the flags footer.
- **Thin** (`flag: "thin"`) — margin under `THIN` (KES 250); still positive.
- **No BOM** (`flag: "nobom"`) — no cost on file; priced at the default tier
  (`DEFAULT_PRICE` = 1,200) and flagged to verify. *(None in the current list — every bag
  matches a BOM row.)*
- **Pinned** (`flag: "pinned"`) — price set by hand (see overrides below).

Edit `BAND` to move the auto split; edit `reject_overrides.json` to change a pin.

## Excel export

`build()` also writes **`reject_sales_export.xlsx`** — the **whole pricing board**: **Bag ·
Category · Units · Colours · BOM Cost · Sale Price · Margin/Unit · Margin % · Revenue · Flag**,
sorted by category then bag, with a **TOTAL** row (units + revenue, total margin in the label). The
dashboard shows a **⬇ Excel** download button beside Refresh on the Reject Sale page
(`streamlit_app.py`), serving that file (falls back to `reject_sales_export.csv` if the xlsx
writer/openpyxl is unavailable).

## What the page shows (`RJ`)

- **KPIs** — bag types, total units to clear, **projected revenue** (Σ price × units) and
  **projected margin** (Σ (price − cost) × units) if everything sells.
- **Price tiers** — one card per tier: bag count, units, revenue and a revenue bar.
- **By category** — the stock grouped by **bag category** (`byCategory`): a clickable chip per
  category (bag types, units, revenue) plus a **totals line** (categories, bag types, units,
  revenue, margin). Clicking a chip **filters** the board to that category.
- **Pricing board** — a **sortable, searchable** table: bag (with its BOM match in grey if
  the name differs, e.g. *Mega Bagpack → MEGA*), **category**, units, colour count (hover for
  the colour split), BOM cost, **sale price** (tier-coloured), margin/unit, margin %, revenue,
  and a flag pill. Search matches bag **or** category; a **TOTAL footer row** sums the units,
  revenue and margin of whatever is currently shown (respects the search + category filter).

## Categories

Each bag's **category** comes from the **offers sheet** (col C) via `offer_picking._read_offers`
(exact name, then alias, then a word-boundary match). Bags not on the offers sheet fall back to
a keyword rule (`_CAT_KEYWORDS` — e.g. *Mega Bagpack → Backpack*, *Moon Bags / Skye →
Handbag*), so every bag gets a bucket (no "Other" at present).
14 categories over the current list — Handbag, Backpack, Travel, Sling, Man Bag, School Bag,
Briefcase, Chest Bag, Lunch Bag, Waist Bag, Baby Bag, Messenger, Sport, Washbag.

## Data sources

- **`reject_stock.csv`** (repo root) — the physical reject stock: `BAG TYPE, COLOR, UNITS`,
  one row per colour. **This is the file to update** before/around the sale — add, remove or
  re-count rows and re-run. Aggregated to per-bag-type units (with a colour breakdown).
- **"Updated BOMs" sheet** — per-bag production cost, via `offer_picking._read_bom_costs`
  (reuses its BOM reader + name aliases / `_resolve_bag`). Mirrored to **`bom_costs.json`**
  on every successful run and used as the **offline fallback** when the sheet is unreachable
  (same pattern as `offers_prices.json`). The page's cost-source note says which was used.
- **`reject_overrides.json`** (optional) — pin a bag's price by hand: `{ "BABY BAG": 2000 }`.
  Keys starting with `_` are ignored; the bag name must match the CSV (upper-case). Delete an
  entry to return to the cost-based tier.

## Regenerating

`python reject_sales.py` (NAV entry **Products → Reject Sale**, dependency
`["reject_sales.py"]`). Prints the tier split, projected revenue/margin and the flagged bags.
`reject_sales.py` imports `offer_picking` only for its BOM helpers (no DB work at import).

## Notes / next steps

- The three tiers and bands are business choices — tweak `TIERS`, `BAND1`, `BAND2`, `THIN`,
  `DEFAULT_PRICE` at the top of the generator.
- If you want the below-cost bags in the sale, decide per bag: hold them, or pin a price that
  covers cost in `reject_overrides.json`.
