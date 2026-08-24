-- CORPORATE BAGS SOLD (dynamic) — from customer invoices, not POS.
-- Corporate sales live in account_move (out_invoice), NOT the POS tills, so
-- they are naturally absent from Total Sales / Weekly Sales / Net Bags Sold.
-- A corporate invoice counts as "bags sold" (they've been sent) when EITHER:
--   • it is settled            → payment_state in ('paid','in_payment'), OR
--   • it is at least 75% paid  → balance is <= 25% of the invoice value.
-- Bags = SUM(quantity) over the invoice's PRODUCT lines only
-- (display_type IS NULL AND product_id IS NOT NULL drops tax / section /
--  payment-term rows). Params :start_date / :end_date over invoice_date.
WITH qinv AS (
    SELECT am.id
    FROM account_move am
    WHERE am.move_type = 'out_invoice'
      AND am.state = 'posted'
      AND am.invoice_date BETWEEN :start_date AND :end_date
      AND ( am.payment_state IN ('paid', 'in_payment')
            OR (am.amount_total > 0
                AND am.amount_residual / am.amount_total <= 0.25) )
)
SELECT COUNT(DISTINCT aml.move_id)          AS invoices,
       COALESCE(SUM(aml.quantity), 0)::int  AS bags,
       COUNT(*)                             AS lines
FROM account_move_line aml
JOIN qinv ON qinv.id = aml.move_id
WHERE aml.display_type IS NULL
  AND aml.product_id IS NOT NULL
