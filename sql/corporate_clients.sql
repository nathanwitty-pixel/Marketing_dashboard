-- CORPORATE BY CLIENT (dynamic) — one row per client/company for the period, from the Denri
-- Corporate app, for the Sales card's "Corporate by client" list. Same bag and paid-% rules as
-- corporate_bags.sql. A client's top-ups (another quotation or invoice) add into the same row:
-- rows group on the company name with case, punctuation and Ltd / Limited ignored, so
-- "Safarilink" and "safarilink", or "Page Capital" and "Page Capital Ltd", are one client.
--   quoted     bags on quotations dated in the period (declined / cancelled left out)
--   invoiced   bags on invoices dated in the period (draft / cancelled left out)
--   agreed     value of those invoices less WHT (KES)
--   paid       paid on those invoices so far (any date)
--   sold       bags counted as sold in the period = bags × (paid in the period ÷ agreed),
--              over ANY of the client's invoices (a balance cleared this month for last
--              month's invoice lands here) — this is what goes into Sales
-- Params :start_date / :end_date.
WITH inv AS (
    SELECT i.id, i.date_invoice, i.company,
           GREATEST(i.amount_total - COALESCE(i.wht_amount, 0), 0) AS agreed,
           (SELECT COALESCE(SUM(l.qty), 0) FROM denri_corporate_invoice_line l
             WHERE l.invoice_id = i.id
               AND COALESCE(l.product, '') !~* '(fee|sponsor|origination|sample)') AS bags
    FROM denri_corporate_invoice i
    WHERE i.status NOT IN ('draft', 'cancelled')
),
inv_rows AS (
    SELECT inv.company, inv.date_invoice AS dated,
           0::numeric AS quoted,
           CASE WHEN inv.date_invoice BETWEEN :start_date AND :end_date THEN inv.bags ELSE 0 END AS invoiced,
           CASE WHEN inv.date_invoice BETWEEN :start_date AND :end_date THEN inv.agreed ELSE 0 END AS agreed,
           CASE WHEN inv.date_invoice BETWEEN :start_date AND :end_date
                THEN (SELECT COALESCE(SUM(p.amount), 0) FROM denri_corporate_payment p WHERE p.invoice_id = inv.id)
                ELSE 0 END AS paid,
           inv.bags * LEAST((SELECT COALESCE(SUM(p.amount), 0) FROM denri_corporate_payment p
                              WHERE p.invoice_id = inv.id
                                AND GREATEST(p.date, inv.date_invoice) BETWEEN :start_date AND :end_date)
                            / NULLIF(inv.agreed, 0), 1) AS sold
    FROM inv
),
quote_rows AS (
    SELECT q.company, q.date_quote AS dated,
           (SELECT COALESCE(SUM(l.qty), 0) FROM denri_corporate_quote_line l
             WHERE l.quote_id = q.id
               AND COALESCE(l.product, '') !~* '(fee|sponsor|origination|sample)') AS quoted,
           0::numeric AS invoiced, 0::numeric AS agreed, 0::numeric AS paid, 0::numeric AS sold
    FROM denri_corporate_quote q
    WHERE q.status NOT IN ('declined', 'cancelled')
      AND q.date_quote BETWEEN :start_date AND :end_date
),
rows AS (
    SELECT x.*,
           regexp_replace(regexp_replace(LOWER(COALESCE(x.company, '')),
                          '\m(limited|ltd|ld|plc|the)\M', '', 'g'), '[^a-z0-9]', '', 'g') AS client_key
    FROM (SELECT * FROM inv_rows UNION ALL SELECT * FROM quote_rows) x
)
SELECT (ARRAY_AGG(company ORDER BY dated DESC))[1] AS client,    -- latest spelling
       SUM(quoted)::int                 AS quoted,
       SUM(invoiced)::int               AS invoiced,
       ROUND(SUM(agreed))::bigint       AS agreed_kes,
       ROUND(SUM(paid))::bigint         AS paid_kes,
       ROUND(SUM(sold)::numeric, 1)     AS sold
FROM rows
GROUP BY client_key
HAVING SUM(quoted) > 0 OR SUM(invoiced) > 0 OR SUM(sold) > 0
ORDER BY SUM(sold) DESC, SUM(invoiced) DESC, SUM(quoted) DESC
