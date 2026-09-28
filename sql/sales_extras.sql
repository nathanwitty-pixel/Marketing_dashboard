-- Samples and customisation sold — shown next to Sales on the Current Performance card.
-- All tills, done/paid, refunds netted (qty <> 0), same window as bags_sold_total.sql.
--   samples      : "Sample …" products — NOT in Sales (display units, excluded there).
--   custom_bags  : customised bags ("… Customised …") — a bag, so IN Sales.
--   custom_fees  : customisation charges ("Customization …") — a service line, NOT in Sales.
WITH params AS (
  SELECT
    CAST(:start_date AS DATE) AS start_date,
    CAST(:end_date AS DATE) AS end_date
)
SELECT
  COALESCE(SUM(pl.qty) FILTER (WHERE pt."name" ILIKE '%sample%'), 0)::numeric        AS samples,
  COALESCE(SUM(pl.qty) FILTER (WHERE pt."name" ILIKE '%customi%'
                                 AND pt."name" NOT ILIKE '%customization%'
                                 AND pt."name" NOT LIKE '%+%'), 0)::numeric          AS custom_bags,
  COALESCE(SUM(pl.qty) FILTER (WHERE pt."name" ILIKE '%customization%'), 0)::numeric AS custom_fees
FROM pos_order p
CROSS JOIN params dp
JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN dp.start_date AND dp.end_date
  AND p.state IN ('done', 'invoiced', 'paid')
  AND pl.qty <> 0
  AND (pt."name" ILIKE '%sample%' OR pt."name" ILIKE '%customi%')
