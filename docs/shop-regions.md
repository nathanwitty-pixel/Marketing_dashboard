# Shops & Regions

**This file is the source of truth for which region each shop belongs to.** Edit the
**Shop → Region** table below and re-run the generators — `self_made_combos.py` reads this
file at build time to group shops into regions (used for the per-shop combo-button chips,
where a shop turns **red** if it rings less than half of the best-performing shop in its
own region). No code change needed; just update the table.

Rules for editing:
- Keep the two-column pipe format (`| Shop | Region |`). The **first column is the shop
  name** (matched case-insensitively to the till/location name), the **second is its
  region**.
- Add a row per shop. Remove a shop's row and it falls back to being its own region.
- If this file is missing or unreadable, the code falls back to a built-in default.

**Adding a new shop (Nyeri, 9 Nov 2026, user's call).** Besides this table, a shop must be in the per-page shop
lists, or its sales, stock and dispatches drop out of the per-shop and per-region views (the headline Kenya totals
count every till, so they already include it). Nyeri (till `NYERI`, stock code `NYERI`, Central Region) was added to:
`lib/odoo_tabs.py` (`EXTRA_SHOPS`: counted in every TOTAL / KENYA figure, its column at the **end** of each row so
the positional reads such as col X don't move), `sql/combined_distribution.sql` (dispatch column),
`generators/shops_efficiency.py` + `shops_dispatch.py` (`KENYA_SHOPS`, region map, stock code),
`generators/self_made_combos.py` (till, region default, stock code), `generators/shop_stock_levels.py` (till and
stock code), `generators/new_products.py` + `html/new_products.html` (shop code `NYR`), `lib/footfall.py`.
The next new shop needs the same list.

## Shop → Region

| Shop | Region |
|---|---|
| Hazina | Nairobi CBD |
| Hilton | Nairobi CBD |
| Starmall | Nairobi CBD |
| KTDA | Nairobi CBD |
| Kitengela | Nairobi Metropolitan |
| Rongai | Nairobi Metropolitan |
| Rejects | Rejects |
| Mombasa | Coastal Region |
| Kakamega | Western & Nyanza |
| Kisumu | Western & Nyanza |
| Kisii | Western & Nyanza |
| Busia | Western & Nyanza |
| Meru | Central Region |
| Nanyuki | Central Region |
| Nyeri | Central Region |
| Thika | Central Region |
| Eldoret | Rift Valley |
| Nakuru | Rift Valley |
| Sinza | Diaspora |
| Tanzania | Diaspora |
| Uganda | Diaspora |
| Website | Online |

## Region colours

Reference palette for regions (used by the Executive Dashboard; kept here so the region
list stays in one place). Not required by the marketing dashboard's red/green chips.

| Region | Colour |
|---|---|
| Nairobi Metropolitan | #3498db |
| Nairobi CBD | #1eda66 |
| Coastal Region | #e74c3c |
| Western & Nyanza | #2ecc71 |
| Central Region | #f39c12 |
| Rift Valley | #9b59b6 |
| Diaspora | #1abc9c |
| Online | #27c2f5 |
| Rejects | #27c2f5 |
