-- CORPORATE BAGS BY PRODUCT (dynamic) — what the corporate_bags.sql bags are, one row per product on
-- the Denri Corporate app invoices. Same rule: an invoice counts by the money received in the
-- period, so each line gives qty × (paid in the period ÷ agreed, capped at 1) bags, and the KES
-- received on the invoice (capped at agreed) is shared across its lines by subtotal (the invoice
-- total carries VAT the lines don't, so subtotal × share would come up short). Fee / sponsorship / logo origination / sample lines come back as
-- one 'Fees and other' row with 0 bags, so the KES adds up to the corporate KES received.
-- Product names are typed by hand on the app, so they're upper-cased and trimmed to group.
-- Params :start_date / :end_date over the payment date.
WITH inv AS (
    SELECT i.id, i.date_invoice, i.company,
           GREATEST(i.amount_total - COALESCE(i.wht_amount, 0), 0) AS agreed
    FROM denri_corporate_invoice i
    WHERE i.status NOT IN ('draft', 'cancelled')
),
paid AS (
    SELECT inv.id, inv.company,
           LEAST(SUM(p.amount) / NULLIF(inv.agreed, 0), 1) AS share,
           LEAST(SUM(p.amount), inv.agreed)                AS received
    FROM inv
    JOIN denri_corporate_payment p ON p.invoice_id = inv.id
    WHERE GREATEST(p.date, inv.date_invoice) BETWEEN :start_date AND :end_date
    GROUP BY inv.id, inv.company, inv.agreed
),
line AS (
    SELECT l.*, COALESCE(l.subtotal, l.qty * l.price_unit) AS sub,
           SUM(COALESCE(l.subtotal, l.qty * l.price_unit)) OVER (PARTITION BY l.invoice_id) AS inv_sub
    FROM denri_corporate_invoice_line l
)
SELECT CASE WHEN COALESCE(l.product, '') ~* '(fee|sponsor|origination|sample)' THEN 'Fees and other'
            ELSE upper(trim(COALESCE(l.product, '?'))) END                   AS product,
       SUM(CASE WHEN COALESCE(l.product, '') ~* '(fee|sponsor|origination|sample)' THEN 0
                ELSE l.qty * paid.share END)::float                         AS bags,
       SUM(paid.received * l.sub / NULLIF(l.inv_sub, 0))::float              AS kes,
       string_agg(DISTINCT trim(paid.company), ', ')                         AS clients
FROM paid
JOIN line l ON l.invoice_id = paid.id
WHERE paid.share > 0
GROUP BY 1
ORDER BY kes DESC
