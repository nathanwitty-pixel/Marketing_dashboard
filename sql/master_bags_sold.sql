-- Net bags sold for products on the master catalogue list (master_products.txt).
-- "Net" = SUM(qty) so POS refunds (negative qty) net out. States done/paid.
-- Names are normalised the same way on both sides: lower-cased, full-stops made
-- spaces, and runs of whitespace collapsed — so "Red.Pattern" == "Red Pattern".
-- :master is the normalised list; :start_date / :end_date bound the range.
WITH params AS (
  SELECT
    CAST(:start_date AS DATE) AS start_date,
    CAST(:end_date AS DATE) AS end_date
)
SELECT
  COALESCE(SUM(pl.qty), 0)::numeric AS bags,
  COUNT(*) AS lines,
  COUNT(DISTINCT trim(regexp_replace(lower(replace(COALESCE(pt."name", ''), '.', ' ')), '\s+', ' ', 'g'))) AS products
FROM pos_order p
CROSS JOIN params dp
JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN dp.start_date AND dp.end_date
  AND p.state IN ('done', 'paid')
  AND trim(regexp_replace(lower(replace(COALESCE(pt."name", ''), '.', ' ')), '\s+', ' ', 'g')) = ANY(:master)
