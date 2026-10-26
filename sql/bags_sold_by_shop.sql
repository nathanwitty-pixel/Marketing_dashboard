-- Bags sold PER TILL — bags_sold_total.sql split by shop, so the rows add up to the
-- Sales total exactly (same filters, same refund netting). Used by the "Why did we move?"
-- waterfall (generators/forward_projections.py), which groups the tills into regions via
-- docs/shop-regions.md. No session = website order. Params :start_date / :end_date / :excluded.
-- bulk_bags = the part of `bags` on BULK orders: an order with any counted line of 10+ units (the
-- dashboard's bulk rule — docs/product-performance.md › Bulk orders, footfall_walkins.sql). ABS(qty),
-- so the refund of a bulk sale is bulk too and nets against it.
WITH params AS (
  SELECT
    CAST(:start_date AS DATE) AS start_date,
    CAST(:end_date AS DATE) AS end_date
),
lines AS (
SELECT
  CASE WHEN p.session_id IS NULL THEN 'WEBSITE' ELSE UPPER(COALESCE(pc."name", '')) END AS shop,
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
SELECT shop,
       COALESCE(SUM(qty), 0)::numeric                                        AS bags,
       COALESCE(SUM(CASE WHEN order_max_line >= 10 THEN qty END), 0)::numeric AS bulk_bags
FROM lines
GROUP BY 1
