# Reject Sale (`reject_sales.py` → `reject_sales.html`, `RJ`)

A **clearance-sale pricing board** for the reject/second-grade bags — built for the
**Kitengela** offer sale. It takes the physical reject stock and puts every bag into one of
three sale prices — **KES 1,000 / 1,200 / 1,500** — chosen against the bag's **BOM production
cost** so nothing is knowingly sold below cost.

## The pricing rule (cost-banded tiers)

Each bag's sale price is the **cheapest tier that still clears its BOM cost**, so bigger /
costlier bags land in the higher tiers and cheap ones in 1,000 — reject prices that still
track value. Bands (the constants `BAND1`, `BAND2` in `reject_sales.py`):

| BOM cost | Sale price |
|---|---|
| ≤ **650** | KES **1,000** |
| 650 – **900** | KES **1,200** |
| > 900 | KES **1,500** |

Chosen from the real BOM spread (77 bag types, cost ≈ 400–2,700, median ≈ 820) so the split
is balanced (~24 / 20 / 33 bags) and every tier keeps a positive margin — except:

- **Below cost** (`flag: "below"`) — bag costs **more than 1,500**, so even the top tier loses
  money. Currently: *Alpha Travel, Baby Bag, Jamela, Pocket Travel, Sarai*. Hold them, or pin
  a higher price. Shown with a red pill and listed in the flags footer.
- **Thin** (`flag: "thin"`) — margin under `THIN` (KES 250); still positive.
- **No BOM** (`flag: "nobom"`) — no cost on file (*Mandy Handbag, Spack*); priced at the
  default tier (`DEFAULT_PRICE` = 1,200) and flagged to verify.
- **Pinned** (`flag: "pinned"`) — price set by hand (see overrides below).

Edit the band constants to re-tier everything at once.

## What the page shows (`RJ`)

- **KPIs** — bag types, total units to clear, **projected revenue** (Σ price × units) and
  **projected margin** (Σ (price − cost) × units) if everything sells.
- **Price tiers** — one card per tier: bag count, units, revenue and a revenue bar.
- **Pricing board** — a **sortable, searchable** table: bag (with its BOM match in grey if
  the name differs, e.g. *Mega Bagpack → MEGA*), units, colour count (hover for the colour
  split), BOM cost, **sale price** (tier-coloured), margin/unit, margin %, revenue, and a
  flag pill. Search filters to a bag and summarises its units + revenue.

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
