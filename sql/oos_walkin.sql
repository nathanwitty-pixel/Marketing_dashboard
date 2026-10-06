-- "Out of stock — call back" WALK-IN requests from the Odoo leads module (denri_lead) — the shop
-- side of the out-of-stock demand; sql/oos_callbacks.sql is the online (WhatsApp Monitoring) side.
-- A lead is an out-of-stock request when its status is "Awaiting stock" now OR was at any time:
-- leads that later bought move to "Purchased", and only the chatter tracking (mail_tracking_value,
-- field "Lead status") remembers they were waiting for stock (431 such leads by Oct 2026).
-- One row per lead; the lib maps the branch to the WhatsApp shop names and builds the person key.
WITH ever_oos AS (
  SELECT DISTINCT m.res_id AS lead_id
  FROM mail_tracking_value v
  JOIN mail_message m ON m.id = v.mail_message_id
  WHERE m.model = 'denri.lead' AND v.field_desc = 'Lead status'
    AND 'Awaiting stock' IN (v.old_value_char, v.new_value_char)
)
SELECT
  l.id                                        AS lead_id,
  l.capture_date                              AS req_date,
  b."name"                                    AS branch,
  l.phone                                     AS phone,
  l.customer_name                             AS customer_name,
  l.state                                     AS state,
  pt."name"                                   AS product,          -- the catalogue product when picked
  l.product_text                              AS product_text,     -- free text otherwise ("MINI MAYA")
  l.colour_text                               AS colour_text
FROM denri_lead l
LEFT JOIN denri_lead_branch b  ON b.id = l.branch_id
LEFT JOIN product_product pp   ON pp.id = l.product_id
LEFT JOIN product_template pt  ON pt.id = pp.product_tmpl_id
WHERE l.active
  AND l.capture_date IS NOT NULL
  AND (l.state = 'awaiting_stock' OR l.id IN (SELECT lead_id FROM ever_oos))
