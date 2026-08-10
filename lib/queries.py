"""lib/queries.py — SQL for the Litmus Postgres source of truth (Odoo POS).

Bags sold come from pos_order_line (the tills). The rules match the Streamlit
report so figures agree:
  • bags  = SUM(qty). POS refunds are negative qty lines, so this nets refunds.
  • value = SUM(price_subtotal_incl), tax-inclusive.
  • combos/bundles excluded: native is_combo_line / sub_product_line flags AND
    any product name containing '+'.
  • program-reward (free) lines excluded.
  • Gift Bag, delivery, customisation and straps excluded by name.
  • order states done / invoiced / paid (cancelled orders never counted).
  • dates bucketed in Africa/Nairobi local time (date_order is stored UTC).

NOTE (basis): value is each order's own currency total (Sinza/Uganda not yet
converted to KES); the BAGS figure is currency-agnostic and is what the weekly
card uses. Master-list-only scoping isn't applied yet — that lands when we
migrate the rest of the dashboard.
"""

import os as _os

_SQL_DIR = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "sql")


def _load_sql(name):
    with open(_os.path.join(_SQL_DIR, name), encoding="utf-8") as _f:
        return _f.read()


# Editable list of product names that are NOT counted as bag sales — see
# sales_exclusions.txt at the project root. Maintained by the user; read fresh
# each run so edits take effect on the next refresh.
_EXCLUSIONS_FILE = _os.path.join(_os.path.dirname(_SQL_DIR), "sales_exclusions.txt")


def excluded_products():
    """Lower-cased product names to drop from Total Sales. Returns a sentinel
    when the list is empty so `<> ALL(:excluded)` stays a valid text[]."""
    names = []
    try:
        with open(_EXCLUSIONS_FILE, encoding="utf-8") as _f:
            for line in _f:
                s = line.split("#", 1)[0].strip()
                if s:
                    names.append(s.lower())
    except OSError:
        pass
    return names or ["~~no~exclusions~~"]


# TOTAL BAGS SOLD — the headline "total sales" figure. Matches the Product Sales
# report's GRAND TOTAL exactly: counts every individual bag sold (including bags
# inside combos, and gift bags), dropping only the combo WRAPPER ('+' name),
# delivery, customisation and straps. This is the number the dashboard's
# Current Performance "Sales", the Weekly Sales card and the weekly-performance
# breakdown all use, so they reconcile. Params :start_date / :end_date.
BAGS_SOLD_TOTAL = _load_sql("bags_sold_total.sql")


# Shared WHERE body so TOTAL and the per-product detail can't drift apart.
_BAGS_WHERE = """
    (o.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date
        BETWEEN :start_date AND :end_date
  AND o.state IN ('done', 'invoiced', 'paid')
  AND l.product_id IS NOT NULL
  AND COALESCE(l.is_combo_line, false)      = false
  AND COALESCE(l.sub_product_line, false)   = false
  AND COALESCE(l.is_program_reward, false)  = false
  AND l.full_product_name NOT ILIKE '%+%'
  AND l.full_product_name NOT ILIKE 'gift bag%'
  AND l.full_product_name NOT ILIKE '%delivery%'
  AND l.full_product_name NOT ILIKE '%customi%'
  AND l.full_product_name NOT ILIKE '%strap%'
"""

# One number: the week's total bags + value (used by the Weekly Sales card).
WEEKLY_BAGS_TOTAL = f"""
SELECT COALESCE(SUM(l.qty), 0)::numeric              AS bags,
       COALESCE(SUM(l.price_subtotal_incl), 0)::numeric AS value,
       COUNT(*)                                       AS lines
FROM pos_order_line l
JOIN pos_order o ON o.id = l.order_id
WHERE {_BAGS_WHERE}
"""

# Monthly total — the SAME bags query, just fed a whole-month date window
# (first→last day of the month). Used by monthly_sales.py for the current
# month's Sales / target-achievement figure. Kept as its own name so callers
# read clearly, but the SQL is identical because _BAGS_WHERE is window-driven.
MONTHLY_BAGS_TOTAL = WEEKLY_BAGS_TOTAL

# Per-product detail for the same window (bags + value per product name).
WEEKLY_BAGS_SOLD = f"""
SELECT l.full_product_name                            AS product,
       SUM(l.qty)::numeric                            AS bags,
       SUM(l.price_subtotal_incl)::numeric            AS value
FROM pos_order_line l
JOIN pos_order o ON o.id = l.order_id
WHERE {_BAGS_WHERE}
GROUP BY l.full_product_name
ORDER BY bags DESC
"""
