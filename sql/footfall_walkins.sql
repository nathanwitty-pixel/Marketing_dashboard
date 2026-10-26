-- FOOTFALL × WALK-IN SALES, per shop per day (spec: docs/footfall-marketing.md).
-- Visitors = denri_footfall_count.manual_count (counted at close of day; NULL = not counted).
-- Walk-in orders = pos_order with customer_type 'walkin', done / invoiced / paid, amount_total > 0,
-- dated in Kenya time (date_order + 3 h), shop = pos_session.config_id.
-- KES-normalised like sql/bag_revenue.sql: DAR-ES-ALAM / Sinza ÷ 25, UGANDA ÷ 29.
-- Bulk order = an order with any line of 10+ units: its KES and units are returned apart.
-- Params :start_date / :end_date (Kenya dates).
WITH params AS (
  SELECT CAST(:start_date AS DATE) AS s, CAST(:end_date AS DATE) AS e
),
orders AS (
  SELECT p.id, ps.config_id, (p.date_order + interval '3 hours')::date AS day,
         CASE WHEN lower(pc.name) IN ('sinza','dar-es-alam') THEN p.amount_total / 25
              WHEN lower(pc.name) = 'uganda'                 THEN p.amount_total / 29
              ELSE p.amount_total END AS kes,
         (SELECT MAX(pl.qty) FROM pos_order_line pl WHERE pl.order_id = p.id) AS max_line,
         (SELECT SUM(pl.qty) FROM pos_order_line pl WHERE pl.order_id = p.id) AS units
  FROM pos_order p
  CROSS JOIN params
  JOIN pos_session ps ON ps.id = p.session_id
  JOIN pos_config pc  ON pc.id = ps.config_id
  WHERE p.customer_type = 'walkin'
    AND p.state IN ('done', 'invoiced', 'paid')
    AND p.amount_total > 0
    AND (p.date_order + interval '3 hours')::date BETWEEN params.s AND params.e
),
sales AS (
  SELECT config_id, day,
         COUNT(*)                                                    AS orders,
         SUM(kes)                                                    AS kes,
         SUM(CASE WHEN max_line >= 10 THEN 1 ELSE 0 END)             AS bulk_orders,
         SUM(CASE WHEN max_line >= 10 THEN kes ELSE 0 END)           AS bulk_kes,
         SUM(CASE WHEN max_line >= 10 THEN units ELSE 0 END)         AS bulk_units,
         MAX(CASE WHEN max_line >= 10 THEN max_line ELSE 0 END)      AS bulk_max_line
  FROM orders GROUP BY 1, 2
),
counts AS (
  SELECT f.config_id, f.date AS day, SUM(f.manual_count) AS visitors
  FROM denri_footfall_count f CROSS JOIN params
  WHERE f.date BETWEEN params.s AND params.e
  GROUP BY 1, 2
)
SELECT COALESCE(c.config_id, s.config_id) AS config_id,
       pc.name                            AS shop,
       COALESCE(c.day, s.day)             AS day,
       c.visitors,
       COALESCE(s.orders, 0)              AS orders,
       COALESCE(s.kes, 0)                 AS kes,
       COALESCE(s.bulk_orders, 0)         AS bulk_orders,
       COALESCE(s.bulk_kes, 0)            AS bulk_kes,
       COALESCE(s.bulk_units, 0)          AS bulk_units,
       COALESCE(s.bulk_max_line, 0)       AS bulk_max_line
FROM counts c
FULL OUTER JOIN sales s ON s.config_id = c.config_id AND s.day = c.day
JOIN pos_config pc ON pc.id = COALESCE(c.config_id, s.config_id)
ORDER BY 2, 3
