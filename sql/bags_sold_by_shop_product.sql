-- Bags sold PER TILL PER PRODUCT — bags_sold_by_shop.sql with the product name kept, so a page can count
-- only some products (New Products' "Why did we move?" waterfall, lib/why_moved.build(match)).
-- Same filters, same refund netting, same bulk rule: an order is bulk when ANY counted line in it has
-- 10+ units, judged on the whole order (not only the matched products).
WITH params AS (
  SELECT
    CAST(:start_date AS DATE) AS start_date,
    CAST(:end_date AS DATE) AS end_date
),
lines AS (
SELECT
  CASE WHEN p.session_id IS NULL THEN 'WEBSITE' ELSE UPPER(COALESCE(pc."name", '')) END AS shop,
  p.date_order::date AS day,
  COALESCE(pt."name", '') AS product,
  pl.qty,
  MAX(ABS(pl.qty)) OVER (PARTITION BY p.id) AS order_max_line
FROM pos_order p
CROSS JOIN params dp
JOIN POS_LINES(p) pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
WHERE p.date_order::date BETWEEN dp.start_date AND dp.end_date
  AND p.state IN ('done', 'invoiced', 'paid')                          -- drop draft / cancelled
  AND pl.qty <> 0                                          -- NET refunds: a returned sale subtracts (was qty>0, which double-counted refunded bulk orders)
  AND COALESCE(pt."name", '') NOT LIKE '%+%'
  AND COALESCE(pt."name", '') NOT ILIKE '%delivery%'
  AND COALESCE(pt."name", '') NOT ILIKE '%customization%'
  AND COALESCE(pt."name", '') NOT ILIKE '%strap%'
  AND COALESCE(pt."name", '') NOT ILIKE '%KES discount%'   -- price adjustment, not a bag
  -- samples (display units sold) ARE counted since 26 Oct 2026 (user's call)
  AND COALESCE(pcat."name", '') NOT ILIKE '%Pos%'          -- non-bag POS lines
  AND lower(COALESCE(pt."name", '')) <> ALL(:excluded)     -- editable not-a-sale list (sales_exclusions.txt)
)
SELECT shop, day, product,
       COALESCE(SUM(qty), 0)::numeric                                        AS bags,
       COALESCE(SUM(CASE WHEN order_max_line >= 10 THEN qty END), 0)::numeric AS bulk_bags
FROM lines
GROUP BY 1, 2, 3
