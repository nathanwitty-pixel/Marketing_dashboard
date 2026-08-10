-- Per-shop bags SOLD from Odoo POS, over a date range.
-- Same shop-mapping and exclusions as the Dispatch app's PRODUCT_SALES_BY_SHOP,
-- but aggregated to one row per shop. Combos ('+'), gift bags, delivery,
-- discounts and the POS holding category are excluded; refunds net via SUM(qty).
WITH params AS (
  SELECT
    CAST(:start_date AS DATE) AS start_date,
    CAST(:end_date AS DATE) AS end_date
)
SELECT
  CASE
    WHEN lower(pc."name") IN ('website sales','website','jumia') OR p.session_id IS NULL THEN 'WEBSITE'
    WHEN lower(pc."name") IN ('sinza','dar-es-alam')             THEN 'SINZA'
    WHEN lower(pc."name") IN ('ktda','ktda shop')                THEN 'KTDA'
    ELSE UPPER(pc."name")
  END AS "Shop",
  SUM(pl.qty) AS "Bags"
FROM pos_order p
JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
CROSS JOIN params dr
WHERE p.date_order::date BETWEEN dr.start_date AND dr.end_date
  AND p.state IN ('done', 'paid')
  AND COALESCE(pt."name", '') NOT LIKE '%+%'
  AND COALESCE(pt."name", '') NOT ILIKE '%Delivery Fee%'
  AND COALESCE(pt."name", '') NOT ILIKE '%Gift Bag%'
  AND COALESCE(pt."name", '') NOT ILIKE '%KES discount%'
  AND COALESCE(pcat."name", '') NOT ILIKE '%Pos%'
  AND pl.qty > 0
  AND (p.session_id IS NULL OR COALESCE(pc."name", '') <> '')
  AND (p.session_id IS NULL OR pc."name" NOT ILIKE '%Flash Sale%')
  AND (p.session_id IS NULL OR pc."name" NOT ILIKE '%Staff%')
GROUP BY 1
HAVING SUM(pl.qty) <> 0
ORDER BY "Bags" DESC;
