-- Reject bags sold — the subset of the GRAND TOTAL (bags_sold_total.sql) that are the
-- Kitengela clearance items: distinct Odoo products tagged "[REJECT]" in the name. Same
-- filters as the total (so it is a true subset), plus the "[REJECT]" tag. Postgres LIKE
-- treats only % and _ as special, so the [ ] are literal.
WITH params AS (
  SELECT
    CAST(:start_date AS DATE) AS start_date,
    CAST(:end_date AS DATE) AS end_date
)
SELECT
  COALESCE(SUM(pl.qty), 0)::numeric AS bags,
  COUNT(*) AS lines,
  ROUND(COALESCE(SUM(
    CASE
      WHEN lower(pc."name") IN ('sinza','dar-es-alam') THEN pl.price_subtotal_incl / 25
      WHEN lower(pc."name") = 'uganda'                 THEN pl.price_subtotal_incl / 29
      ELSE pl.price_subtotal_incl
    END
  ), 0)) AS value
FROM pos_order p
CROSS JOIN params dp
JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
WHERE p.date_order::date BETWEEN dp.start_date AND dp.end_date
  AND p.state IN ('done', 'paid')
  AND pl.qty <> 0
  AND COALESCE(pt."name", '') NOT LIKE '%+%'
  AND COALESCE(pt."name", '') NOT ILIKE '%delivery%'
  AND COALESCE(pt."name", '') NOT ILIKE '%customization%'
  AND COALESCE(pt."name", '') NOT ILIKE '%strap%'
  AND COALESCE(pt."name", '') NOT ILIKE '%KES discount%'
  AND COALESCE(pt."name", '') NOT ILIKE '%sample%'
  AND COALESCE(pcat."name", '') NOT ILIKE '%Pos%'
  AND lower(COALESCE(pt."name", '')) <> ALL(:excluded)
  AND COALESCE(pt."name", '') ILIKE '%[REJECT]%'          -- the clearance tag
