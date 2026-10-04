-- "Out of stock — call back" requests from the Odoo WhatsApp Monitoring module.
-- One row per OOS request × requested product: an interaction whose reason is flagged
-- is_out_of_stock, joined to every bag the customer asked for (the many2many rel table
-- plus the single oos_product_id field). The bag is only recorded from June 2026 on, so
-- earlier OOS requests (no product) drop out here. Junk shop rows (no code) are skipped.
-- "person" = phone_key, else WhatsApp username, else the interaction itself.
WITH req_bags AS (
  SELECT interaction_id AS iid, product_id AS pid FROM denri_monitor_interaction_oos_product_rel
  UNION
  SELECT id, oos_product_id FROM denri_monitor_interaction WHERE oos_product_id IS NOT NULL
)
SELECT
  i.id                                                              AS interaction_id,
  i."date"                                                          AS req_date,
  s."name"                                                          AS shop,
  s.kind                                                            AS shop_kind,
  COALESCE(NULLIF(i.phone_key, ''), NULLIF(i.wa_username_key, ''), 'i' || i.id) AS person,
  COALESCE(i.is_purchased, FALSE)                                   AS is_purchased,
  pt."name"                                                         AS product
FROM denri_monitor_interaction i
JOIN denri_monitor_reason r  ON r.id = i.reason_id AND r.is_out_of_stock
JOIN denri_monitor_shop s    ON s.id = i.shop_id AND s.code IS NOT NULL
JOIN req_bags b              ON b.iid = i.id
JOIN product_product pp      ON pp.id = b.pid
JOIN product_template pt     ON pt.id = pp.product_tmpl_id
