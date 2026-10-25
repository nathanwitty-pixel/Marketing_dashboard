"""lib/pos_lines.py — till lines with refunded combos fixed (docs/README.md › Combo refunds).

Queries write `JOIN POS_LINES(p) pl ON pl.order_id = p.id` (p = the pos_order alias) and
db.run_query expands it to a LATERAL subquery with pos_order_line's columns, where:
  * a refund's KES 0 bag lines in an order that refunds a combo ('+' product) become that combo's
    sub-lines (sub_product_line true, parent_id = the combo product) — so single-bag counts that skip
    sub-lines don't take them off a second time;
  * a combo refunded with no bag lines of its own gets the original sale's bags (refunded_orderline_id →
    the sale's sub-lines, exact colours) as KES 0 sub-lines with negative qty — so Sales-style counts
    (sub-lines kept, '+' dropped) take those bags off too.
Inner aliases are prefixed `posl_` so they can't capture the caller's aliases (o, p, pl, …).
"""

import re

_MARK = re.compile(r"\bPOS_LINES\(\s*(\w+)\s*\)")
# The caller's `ON pl.order_id = p.id` is already inside the subquery; left on top it makes the planner
# guess 1 row per query and pick a product × line nested loop (Product Performance: 7s → 88s).
_MARK_ON = re.compile(r"\bPOS_LINES\(\s*(\w+)\s*\)\s+(\w+)\s+ON\s+\2\.order_id\s*=\s*\1\.id\b")

_TEMPLATE = """LATERAL (
  SELECT posl_l.id, posl_l.order_id, posl_l.product_id, posl_l.qty, posl_l.price_unit, posl_l.price_subtotal,
         posl_l.price_subtotal_incl, posl_l.discount, posl_l.full_product_name, posl_l.is_combo_line,
         posl_l.is_program_reward, posl_l.combo_product_attribute_values, posl_l.refunded_orderline_id,
         (COALESCE(posl_l.sub_product_line, false) OR posl_rw.product_id IS NOT NULL) AS sub_product_line,
         COALESCE(posl_l.parent_id, posl_rw.product_id) AS parent_id
  FROM pos_order_line posl_l
  LEFT JOIN LATERAL (
      SELECT posl_w.product_id FROM pos_order_line posl_w
      JOIN product_product posl_wp ON posl_wp.id = posl_w.product_id
      JOIN product_template posl_wt ON posl_wt.id = posl_wp.product_tmpl_id
      WHERE posl_l.qty < 0 AND posl_l.price_subtotal_incl = 0 AND posl_l.parent_id IS NULL
        AND posl_w.order_id = posl_l.order_id AND posl_w.qty < 0 AND posl_w.id <> posl_l.id
        AND posl_wt."name" LIKE '%+%'
      LIMIT 1
  ) posl_rw ON true
  WHERE posl_l.order_id = {a}.id
  UNION ALL
  SELECT posl_s.id, posl_w.order_id, posl_s.product_id,
         posl_s.qty * posl_w.qty / NULLIF((SELECT SUM(posl_x.qty) FROM pos_order_line posl_x
                                           WHERE posl_x.order_id = posl_o.order_id
                                             AND posl_x.product_id = posl_o.product_id AND posl_x.qty > 0), 0),
         0, 0, 0, 0, posl_s.full_product_name, posl_s.is_combo_line, posl_s.is_program_reward,
         posl_s.combo_product_attribute_values, posl_w.id, true, posl_s.parent_id
  FROM pos_order_line posl_w
  JOIN product_product posl_wp ON posl_wp.id = posl_w.product_id
  JOIN product_template posl_wt ON posl_wt.id = posl_wp.product_tmpl_id
  JOIN pos_order_line posl_o ON posl_o.id = posl_w.refunded_orderline_id
  JOIN pos_order_line posl_s ON posl_s.order_id = posl_o.order_id AND posl_s.parent_id = posl_o.product_id
                            AND COALESCE(posl_s.sub_product_line, false)
  WHERE posl_w.order_id = {a}.id AND posl_w.qty < 0 AND posl_wt."name" LIKE '%+%'
    AND NOT EXISTS (SELECT 1 FROM pos_order_line posl_r
                    WHERE posl_r.order_id = posl_w.order_id AND posl_r.qty < 0
                      AND posl_r.price_subtotal_incl = 0 AND posl_r.id <> posl_w.id)
)"""


def expand(sql: str) -> str:
    """Replace each POS_LINES(alias) with the fixed-lines subquery for that pos_order alias."""
    if "POS_LINES(" not in sql:
        return sql
    sql = _MARK_ON.sub(lambda m: _TEMPLATE.replace("{a}", m.group(1)) + f" {m.group(2)} ON true", sql)
    return _MARK.sub(lambda m: _TEMPLATE.replace("{a}", m.group(1)), sql)
