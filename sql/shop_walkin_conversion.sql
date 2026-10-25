-- Walk-in conversion per shop over a date range: how many of the people who walked in bought.
--   walkins  = denri_footfall_count.manual_count (the shop's daily count, entered at the till)
--   buyers   = in-shop POS receipts (paid, amount > 0) WITHOUT a delivery line — phone/online
--              orders rung on the shop till never walked in. One receipt per buyer, so combos and
--              multi-bag purchases don't inflate it (bags per buyer is reported separately).
-- Only days on which the shop entered a walk-in count are used for BOTH sides, so late entry
-- doesn't make conversion look high. Shop names follow sql/shop_bags_sold.sql.
WITH params AS (
  SELECT CAST(:start_date AS DATE) AS start_date, CAST(:end_date AS DATE) AS end_date
),
shop_of AS (
  SELECT pc.id AS config_id,
    CASE
      WHEN lower(pc."name") IN ('ktda','ktda shop')     THEN 'KTDA'
      WHEN lower(pc."name") IN ('sinza','dar-es-alam') THEN 'SINZA'
      ELSE UPPER(pc."name")
    END AS shop
  FROM pos_config pc
),
counts AS (
  SELECT s.shop, f.date AS day, SUM(f.manual_count) AS walkins
  FROM denri_footfall_count f
  JOIN shop_of s ON s.config_id = f.config_id
  CROSS JOIN params dr
  WHERE f.date BETWEEN dr.start_date AND dr.end_date
  GROUP BY 1, 2
),
receipts AS (
  SELECT s.shop, p.date_order::date AS day, p.id,
    SUM(CASE WHEN pl.qty > 0
              AND COALESCE(pt."name", '') NOT ILIKE '%Delivery%'
              AND COALESCE(pt."name", '') NOT ILIKE '%Gift Bag%'
              AND COALESCE(pt."name", '') NOT ILIKE '%discount%'
             THEN pl.qty ELSE 0 END) AS items,
    BOOL_OR(COALESCE(pt."name", '') ILIKE '%Delivery%') AS delivery
  FROM pos_order p
  JOIN pos_session ps ON ps.id = p.session_id
  JOIN shop_of s ON s.config_id = ps.config_id
  JOIN POS_LINES(p) pl ON pl.order_id = p.id
  LEFT JOIN product_product pp ON pp.id = pl.product_id
  LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
  CROSS JOIN params dr
  WHERE p.date_order::date BETWEEN dr.start_date AND dr.end_date
    AND p.state IN ('done', 'invoiced', 'paid')
    AND p.amount_total > 0
  GROUP BY 1, 2, 3
),
buyers AS (
  SELECT shop, day, COUNT(*) AS buyers, SUM(items) AS items
  FROM receipts
  WHERE NOT delivery
  GROUP BY 1, 2
)
SELECT c.shop,
  COUNT(*)                     AS counted_days,
  MAX(c.day)                   AS counted_to,
  SUM(c.walkins)               AS walkins,
  COALESCE(SUM(b.buyers), 0)   AS buyers,
  COALESCE(SUM(b.items), 0)    AS items
FROM counts c
LEFT JOIN buyers b ON b.shop = c.shop AND b.day = c.day
GROUP BY 1
ORDER BY 1;
