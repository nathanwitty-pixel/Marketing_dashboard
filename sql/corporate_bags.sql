-- CORPORATE BAGS SOLD (dynamic) — from the Denri Corporate app (denriafrica.com/denri_corporate,
-- Odoo module denri_corporate), not POS. Its invoices / payments live in denri_corporate_invoice,
-- denri_corporate_invoice_line and denri_corporate_payment.
-- Bags are counted by the money received: an invoice's bags × (paid in the period ÷ agreed
-- amount). Paid → all its bags; part-paid at month end → only the paid %, and the balance
-- adds the rest in the month it arrives. Agreed amount = total − withholding tax (WHT is
-- deducted by the client, so a "Paid" invoice is 100% even though less cash came in).
-- A payment dated before its invoice (deposit at quotation stage) counts on the invoice date.
-- Draft and cancelled invoices are left out. Bags = SUM(qty) over bag lines only — fees,
-- logo origination, sponsorships and samples aren't bags.
-- Params :start_date / :end_date over the payment date.
WITH inv AS (
    SELECT i.id, i.date_invoice,
           GREATEST(i.amount_total - COALESCE(i.wht_amount, 0), 0) AS agreed,
           (SELECT COALESCE(SUM(l.qty), 0) FROM denri_corporate_invoice_line l
             WHERE l.invoice_id = i.id
               AND COALESCE(l.product, '') !~* '(fee|sponsor|origination|sample)') AS bags
    FROM denri_corporate_invoice i
    WHERE i.status NOT IN ('draft', 'cancelled')
),
paid AS (
    SELECT inv.id, inv.bags, inv.agreed, SUM(p.amount) AS paid
    FROM inv
    JOIN denri_corporate_payment p ON p.invoice_id = inv.id
    WHERE GREATEST(p.date, inv.date_invoice) BETWEEN :start_date AND :end_date
    GROUP BY inv.id, inv.bags, inv.agreed
)
SELECT COUNT(*)                                                                      AS invoices,
       -- whole bags paid for, rounded down per invoice (same rule as corporate_clients.sql, so the
       -- Sales card and the client table always agree); the tiny epsilon guards float error (12.9999 → 13)
       COALESCE(SUM(FLOOR((bags * LEAST(paid / NULLIF(agreed, 0), 1))::numeric + 0.000001)), 0)::int AS bags,
       COALESCE(SUM(bags), 0)::int                                                   AS invoiced_bags
FROM paid
