-- BAG REVENUE for Forward Projections — the money behind the bags in bags_sold_total.sql.
-- Same bag lines as that query (same filters), but the money is counted where it actually sits:
--   * single bags and gift bags        → their own line price
--   * bags inside a combo              → KES 0 on their own line; the combo's price sits on the
--                                        '+' wrapper line, which bags_sold_total drops. Added here
--                                        so combo bags don't count as bags that brought in nothing.
--   * 'KES discount' lines             → negative price adjustments against bags, so they're subtracted.
-- Delivery, customisation and straps stay out (not bag sales); samples are in, like Sales (26 Oct 2026).
-- Value is KES-normalised (Sinza/Dar ÷25, Uganda ÷29), VAT-inclusive, like the Sales card.
-- Params :start_date / :end_date / :excluded (sales_exclusions.txt).
WITH params AS (
  SELECT CAST(:start_date AS DATE) AS start_date, CAST(:end_date AS DATE) AS end_date
),
lines AS (
  SELECT
    pt."name" AS product,
    COALESCE(pcat."name", '') AS categ,
    -- a bag inside a combo: a sub-line of the '+' wrapper (parent_id), or a KES 0 line in an order
    -- that has a wrapper (combo returns come back without the parent link)
    (pl.parent_id IS NOT NULL
     OR (pl.price_subtotal_incl = 0 AND EXISTS (
           SELECT 1 FROM pos_order_line w
           JOIN product_product wp ON wp.id = w.product_id
           JOIN product_template wt ON wt.id = wp.product_tmpl_id
           WHERE w.order_id = pl.order_id AND wt."name" LIKE '%+%'))) AS in_combo,
    pl.qty,
    CASE
      WHEN lower(pc."name") IN ('sinza','dar-es-alam') THEN pl.price_subtotal_incl / 25
      WHEN lower(pc."name") = 'uganda'                 THEN pl.price_subtotal_incl / 29
      ELSE pl.price_subtotal_incl
    END AS kes
  FROM pos_order p
  CROSS JOIN params dp
  JOIN POS_LINES(p) pl ON pl.order_id = p.id
  LEFT JOIN pos_session ps ON p.session_id = ps.id
  LEFT JOIN pos_config pc ON ps.config_id = pc.id
  LEFT JOIN product_product pp ON pl.product_id = pp.id
  LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
  LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
  WHERE p.date_order::date BETWEEN dp.start_date AND dp.end_date
    AND p.state IN ('done', 'invoiced', 'paid')
    AND pl.qty <> 0
),
bag AS (   -- exactly the bags_sold_total.sql bag lines
  SELECT * FROM lines
  WHERE COALESCE(product, '') NOT LIKE '%+%'
    AND COALESCE(product, '') NOT ILIKE '%delivery%'
    AND COALESCE(product, '') NOT ILIKE '%customization%'
    AND COALESCE(product, '') NOT ILIKE '%strap%'
    AND COALESCE(product, '') NOT ILIKE '%KES discount%'
    AND categ NOT ILIKE '%Pos%'
    AND lower(COALESCE(product, '')) <> ALL(:excluded)
)
SELECT
  (SELECT COALESCE(SUM(qty), 0) FROM bag)                                                    AS bags,
  (SELECT COALESCE(SUM(qty), 0) FROM bag WHERE NOT in_combo AND product NOT ILIKE 'gift bag%') AS single_bags,
  (SELECT ROUND(COALESCE(SUM(kes), 0)) FROM bag WHERE NOT in_combo AND product NOT ILIKE 'gift bag%') AS single_kes,
  (SELECT COALESCE(SUM(qty), 0) FROM bag WHERE in_combo)                                     AS combo_bags,
  (SELECT ROUND(COALESCE(SUM(kes), 0)) FROM bag WHERE in_combo)
    + (SELECT ROUND(COALESCE(SUM(kes), 0)) FROM lines WHERE COALESCE(product, '') LIKE '%+%') AS combo_kes,
  (SELECT COALESCE(SUM(qty), 0) FROM bag WHERE NOT in_combo AND product ILIKE 'gift bag%')   AS gift_bags,
  (SELECT ROUND(COALESCE(SUM(kes), 0)) FROM bag WHERE NOT in_combo AND product ILIKE 'gift bag%') AS gift_kes,
  (SELECT ROUND(COALESCE(SUM(kes), 0)) FROM lines WHERE product ILIKE '%KES discount%')      AS discount_kes
