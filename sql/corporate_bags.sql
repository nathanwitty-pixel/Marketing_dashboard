-- CORPORATE BAGS SOLD (dynamic) — from the Denri Corporate app (denriafrica.com/denri_corporate,
-- Odoo module denri_corporate), not POS. Its invoices / payments live in denri_corporate_invoice,
-- denri_corporate_invoice_line and denri_corporate_payment.
-- Bags are counted by the money received: whole bags of an invoice's bags × (paid by the period end ÷
-- agreed amount), less the whole bags already counted before the period. Paid → all its bags; part-paid at month end → only the paid %, and the balance
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
paid AS (      -- paid = in the period; paid_before = before it (so instalments don't each round down)
    SELECT inv.id, inv.bags, inv.agreed,
           SUM(p.amount) FILTER (WHERE GREATEST(p.date, inv.date_invoice) >= :start_date)            AS paid,
           COALESCE(SUM(p.amount) FILTER (WHERE GREATEST(p.date, inv.date_invoice) < :start_date), 0) AS paid_before
    FROM inv
    JOIN denri_corporate_payment p ON p.invoice_id = inv.id
    WHERE GREATEST(p.date, inv.date_invoice) <= :end_date
    GROUP BY inv.id, inv.bags, inv.agreed
    HAVING COUNT(*) FILTER (WHERE GREATEST(p.date, inv.date_invoice) >= :start_date) > 0
)
SELECT COUNT(*)                                                                      AS invoices,
       -- whole bags paid for up to the period end minus whole bags already paid for before it, per invoice
       -- (same rule as corporate_clients.sql, so the Sales card and the client table always agree): 11 bags
       -- paid half + half count 5 then 6, not 5 + 5. The tiny epsilon guards float error (12.9999 → 13)
       COALESCE(SUM(FLOOR((bags * LEAST((paid_before + paid) / NULLIF(agreed, 0), 1))::numeric + 0.000001)
                  - FLOOR((bags * LEAST(paid_before / NULLIF(agreed, 0), 1))::numeric + 0.000001)), 0)::int AS bags,
       COALESCE(SUM(bags), 0)::int                                                   AS invoiced_bags,
       -- KES received in the period, capped at each invoice's agreed amount (Forward Projections revenue)
       COALESCE(SUM(LEAST(paid, agreed)), 0)::float                                  AS kes
FROM paid
