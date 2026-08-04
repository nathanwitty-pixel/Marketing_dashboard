"""lib/queries.py — SQL for the Postgres source of truth.

WEEKLY_BAGS_SOLD below is a TEMPLATE. It encodes the "bags sold" rules the
Streamlit report already uses, but the table/column names are placeholders,
because the schema lives in your Streamlit project, not here. To finish the
weekly fix, do ONE of:

  (a) paste your real query here (e.g. the weekly slice of BAGS_SOLD_REPORT /
      PRODUCT_LINE_ITEMS from your lib/queries.py), or
  (b) tell me the sale-line table + column names and I'll fill the template.

The rules baked in (matching your report, so the weekly figure agrees with it):
  • bags sold = summed line quantity, NET of refunds (returns count negative)
  • combos/bundles excluded  (product name contains '+')
  • Gift Bag, delivery/customisation charges, straps/spares excluded
  • only lines with a real product record
  • date filter is on the sale/order date, inclusive of both ends
"""

# ── EDIT ME: point at your real sale-line table & columns ─────
# Placeholders are wrapped in {{ }} so they're easy to find:
#   {{sale_line}}   the per-line sales table          (e.g. sale_order_line, pos_order_line)
#   {{qty}}         units on the line                 (e.g. qty, quantity, product_uom_qty)
#   {{value}}       line total incl. tax in KES       (e.g. price_total, total)
#   {{product}}     product display name              (e.g. p.name, product_name)
#   {{sale_date}}   the date to filter/bucket on      (e.g. o.date_order::date)
WEEKLY_BAGS_SOLD = """
SELECT
    {{sale_date}}                          AS sale_date,
    {{product}}                            AS product,
    SUM({{qty}})::numeric                   AS bags,
    SUM({{value}})::numeric                 AS value
FROM {{sale_line}}
WHERE {{sale_date}} BETWEEN :start_date AND :end_date
  AND {{product}} IS NOT NULL
  AND {{product}} NOT ILIKE '%+%'                      -- combos/bundles excluded
  AND {{product}} NOT ILIKE 'gift bag%'                -- gift bag excluded
  AND {{product}} NOT ILIKE '%delivery%'
  AND {{product}} NOT ILIKE '%customi%'
  AND {{product}} NOT ILIKE '%strap%'
GROUP BY 1, 2
ORDER BY bags DESC
"""

# A one-number version — the same rules, just the weekly total (used by the
# dashboard's Weekly Sales card). Kept separate so the detail query can grow.
WEEKLY_BAGS_TOTAL = """
SELECT
    COALESCE(SUM({{qty}}), 0)::numeric      AS bags,
    COALESCE(SUM({{value}}), 0)::numeric    AS value,
    COUNT(*)                                AS lines
FROM {{sale_line}}
WHERE {{sale_date}} BETWEEN :start_date AND :end_date
  AND {{product}} IS NOT NULL
  AND {{product}} NOT ILIKE '%+%'
  AND {{product}} NOT ILIKE 'gift bag%'
  AND {{product}} NOT ILIKE '%delivery%'
  AND {{product}} NOT ILIKE '%customi%'
  AND {{product}} NOT ILIKE '%strap%'
"""
