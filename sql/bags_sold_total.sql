-- Total bags sold — the GRAND TOTAL of the Product Sales query, as one number.
-- Mirrors that query's filters EXACTLY (drop the combo wrapper '+', delivery,
-- customisation, straps; keep combo contents, gift bags, all order states;
-- date_order::date). Value is KES-normalised (Sinza/25, Uganda/29) like the
-- Product Sales report, so it is comparable across shops.
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
  AND p.state IN ('done', 'paid')                          -- drop draft / cancelled
  AND pl.qty > 0                                           -- drop refund / return lines
  AND COALESCE(pt."name", '') NOT LIKE '%+%'
  AND COALESCE(pt."name", '') NOT ILIKE '%delivery%'
  AND COALESCE(pt."name", '') NOT ILIKE '%customization%'
  AND COALESCE(pt."name", '') NOT ILIKE '%strap%'
  AND COALESCE(pt."name", '') NOT ILIKE '%KES discount%'   -- price adjustment, not a bag
  AND COALESCE(pcat."name", '') NOT ILIKE '%Pos%'          -- non-bag POS lines
  AND lower(COALESCE(pt."name", '')) <> ALL(:excluded)     -- editable not-a-sale list (sales_exclusions.txt)
