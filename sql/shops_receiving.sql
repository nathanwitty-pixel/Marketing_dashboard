WITH params AS (
  SELECT
    CAST(:start_date AS DATE) AS start_date,
    CAST(:end_date AS DATE) AS end_date
),
dispatched AS (
  SELECT
    m.id,
    dest.complete_name AS node,
    SPLIT_PART(dest.complete_name, '/', 3) AS node_name,
    COALESCE(pt."name", pp.id::text) AS bag_name,
    m.product_qty AS qty,
    DATE(m."date") AS sent_on
  FROM stock_move m
  JOIN stock_location src  ON m.location_id = src.id
  JOIN stock_location dest ON m.location_dest_id = dest.id
  JOIN product_product pp  ON m.product_id = pp.id
  LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
  CROSS JOIN params p
  WHERE src.complete_name  ILIKE '%FINWH%'
    AND src.complete_name  NOT ILIKE '%Goods in Transit%'
    AND dest.complete_name ILIKE 'FINWH/Goods in Transit/%'
    AND m.state != 'cancel'
    AND COALESCE(pt."name",'') NOT LIKE '%+%'
    AND DATE(m."date") BETWEEN p.start_date AND p.end_date
    AND EXTRACT(DOW FROM m."date") != 0
),
receipts AS (
  SELECT
    src.complete_name AS node,
    COALESCE(pt."name", pp.id::text) AS bag_name,
    m.product_qty AS qty,
    DATE(m."date") AS received_on
  FROM stock_move m
  JOIN stock_location src  ON m.location_id = src.id
  JOIN stock_location dest ON m.location_dest_id = dest.id
  JOIN product_product pp  ON m.product_id = pp.id
  LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
  WHERE src.complete_name ILIKE 'FINWH/Goods in Transit/%'
    AND dest.complete_name NOT ILIKE '%Goods in Transit%'
    AND dest.complete_name NOT ILIKE 'FINWH%'
    AND dest.complete_name NOT ILIKE 'PURCH%'
    AND m.state = 'done'
    AND COALESCE(pt."name",'') NOT LIKE '%+%'
),
reversals AS (
  SELECT
    src.complete_name AS node,
    COALESCE(pt."name", pp.id::text) AS bag_name,
    m.product_qty AS qty,
    DATE(m."date") AS returned_on
  FROM stock_move m
  JOIN stock_location src  ON m.location_id = src.id
  JOIN stock_location dest ON m.location_dest_id = dest.id
  JOIN product_product pp  ON m.product_id = pp.id
  LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
  WHERE src.complete_name ILIKE 'FINWH/Goods in Transit/%'
    AND (dest.complete_name ILIKE 'FINWH%' OR dest.complete_name ILIKE 'PURCH%')
    AND dest.complete_name NOT ILIKE '%Goods in Transit%'
    AND m.state = 'done'
    AND COALESCE(pt."name",'') NOT LIKE '%+%'
),
paired AS (
  SELECT
    d.node_name,
    d.bag_name,
    d.qty,
    d.sent_on,
    r.received_on,
    v.returned_on
  FROM dispatched d
  LEFT JOIN LATERAL (
    SELECT rv.returned_on
    FROM reversals rv
    WHERE rv.node = d.node
      AND rv.bag_name = d.bag_name
      AND rv.qty = d.qty
      AND rv.returned_on >= d.sent_on
    ORDER BY rv.returned_on
    LIMIT 1
  ) v ON TRUE
  LEFT JOIN LATERAL (
    SELECT rc.received_on
    FROM receipts rc
    WHERE rc.node = d.node
      AND rc.bag_name = d.bag_name
      AND rc.qty = d.qty
      AND rc.received_on >= d.sent_on
    ORDER BY rc.received_on
    LIMIT 1
  ) r ON TRUE
  WHERE v.returned_on IS NULL
     OR (r.received_on IS NOT NULL AND r.received_on <= v.returned_on)
)
SELECT
  CASE UPPER(node_name)
    WHEN 'CBD STOCKS'    THEN 'KTDA'
    WHEN 'KTDA SHOP'     THEN 'KTDA SHOP'
    WHEN 'DAR-ES-ALAM'   THEN 'SINZA'
    WHEN 'WEBSITE STORE' THEN 'WEBSITE'
    ELSE UPPER(node_name)
  END                                          AS "Shop",
  bag_name                                     AS "Product",
  qty                                          AS "Qty",
  TO_CHAR(sent_on, 'Dy')                       AS "Sent Day",
  sent_on                                      AS "Sent",
  TO_CHAR(received_on, 'Dy')                   AS "Recd Day",
  received_on                                  AS "Received",
  (received_on - sent_on)                      AS "Days",
  CASE
    WHEN received_on IS NULL              THEN 'In transit'
    WHEN received_on = sent_on            THEN 'Same day'
    WHEN received_on = sent_on + 1        THEN 'Next day'
    WHEN received_on = sent_on + 2        THEN 'Two days'
    ELSE 'Later'
  END                                          AS "Status"
FROM paired
ORDER BY sent_on DESC, "Shop", bag_name;
