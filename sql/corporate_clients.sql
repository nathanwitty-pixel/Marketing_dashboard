-- CORPORATE BY CLIENT (dynamic) — one row per client/company for the period, from the Denri
-- Corporate app, for the Sales card's "Corporate by client" list. Same bag and paid-% rules as
-- corporate_bags.sql. A client's top-ups (another quotation or invoice) add into the same row:
-- rows group on the company name with case, punctuation and Ltd / Limited ignored, so
-- "Safarilink" and "safarilink", or "Page Capital" and "Page Capital Ltd", are one client.
--   quoted     bags on quotations dated in the period (declined / cancelled left out)
--   quotes     the quotations behind "quoted", '|'-joined, oldest first: number~status~quoted on~valid until~
--              bags~KES~invoice ('INV-00134~paid~2 Oct', empty when none raised from it), e.g.
--              'QUO-00062~accepted~2 Oct~1 Nov~10~37000~INV-00134 paid 2 Oct'
--   invoiced   bags on invoices dated in the period, plus older invoices that received money
--              in the period (draft / cancelled left out)
--   agreed     value of those invoices less WHT (KES)
--   paid       paid on those invoices up to the period end
--   earlier    month(s) those older invoices were raised, e.g. 'Sep' (NULL when none)
--   earlier_paid_on  latest date in the period money came in on those older invoices, e.g. '1 Oct'
--   inv_months month(s) the counted invoices were raised, 'YYYY-MM' comma-joined, e.g. '2026-09,2026-10'
--              (NULL for a quote-only client) — the "converted in" badges
--   sold       bags counted as sold in the period = whole bags of bags × (paid in the period ÷ agreed),
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
inv_pay AS (
    SELECT inv.*,
           (SELECT COALESCE(SUM(p.amount), 0) FROM denri_corporate_payment p
             WHERE p.invoice_id = inv.id AND p.date <= :end_date) AS paid_to_date,
           (SELECT COALESCE(SUM(p.amount), 0) FROM denri_corporate_payment p
             WHERE p.invoice_id = inv.id
               AND GREATEST(p.date, inv.date_invoice) BETWEEN :start_date AND :end_date) AS paid_in_period,
           (SELECT MAX(GREATEST(p.date, inv.date_invoice)) FROM denri_corporate_payment p
             WHERE p.invoice_id = inv.id
               AND GREATEST(p.date, inv.date_invoice) BETWEEN :start_date AND :end_date) AS last_paid_in_period
    FROM inv
),
inv_rows AS (       -- invoices raised in the period, plus earlier invoices that got paid in it
    SELECT company, date_invoice AS dated,
           0::numeric AS quoted,
           bags AS invoiced, agreed, paid_to_date AS paid,
           -- whole bags paid for, rounded down per invoice (same rule as corporate_bags.sql)
           COALESCE(FLOOR((bags * LEAST(paid_in_period / NULLIF(agreed, 0), 1))::numeric + 0.000001), 0) AS sold,
           CASE WHEN date_invoice < :start_date THEN date_invoice END AS earlier_on,
           CASE WHEN date_invoice < :start_date THEN last_paid_in_period END AS earlier_paid,
           NULL::text AS quote_info
    FROM inv_pay
    WHERE date_invoice BETWEEN :start_date AND :end_date OR paid_in_period > 0
),
quote_rows AS (
    SELECT q.company, q.date_quote AS dated, qb.bags AS quoted,
           0::numeric AS invoiced, 0::numeric AS agreed, 0::numeric AS paid, 0::numeric AS sold,
           NULL::date AS earlier_on, NULL::date AS earlier_paid,
           -- what became of the quote: its status, validity, and the invoice raised from it (if any)
           q.name || '~' || q.status || '~' || TO_CHAR(q.date_quote, 'FMDD Mon') || '~'
             || TO_CHAR(q.date_quote + COALESCE(q.validity_days, 30), 'FMDD Mon') || '~'
             || qb.bags::int || '~' || ROUND(q.amount_total)::bigint || '~'
             || COALESCE((SELECT i.name || ' ' || i.status || ' ' || TO_CHAR(i.date_invoice, 'FMDD Mon')
                            FROM denri_corporate_invoice i
                           WHERE i.quote_id = q.id AND i.status <> 'cancelled'
                           ORDER BY i.date_invoice DESC, i.id DESC LIMIT 1), '') AS quote_info
    FROM denri_corporate_quote q
    CROSS JOIN LATERAL (SELECT COALESCE(SUM(l.qty), 0) AS bags FROM denri_corporate_quote_line l
                         WHERE l.quote_id = q.id
                           AND COALESCE(l.product, '') !~* '(fee|sponsor|origination|sample)') qb
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
       STRING_AGG(quote_info, '|' ORDER BY dated) AS quotes,      -- the quotes behind "quoted"
       SUM(invoiced)::int               AS invoiced,
       ROUND(SUM(agreed))::bigint       AS agreed_kes,
       ROUND(SUM(paid))::bigint         AS paid_kes,
       ROUND(SUM(sold)::numeric, 1)     AS sold,
       STRING_AGG(DISTINCT TO_CHAR(earlier_on, 'Mon'), ', ') AS earlier,  -- months of older invoices paid in the period
       TO_CHAR(MAX(earlier_paid), 'FMDD Mon')                AS earlier_paid_on,  -- when that money came in
       STRING_AGG(DISTINCT TO_CHAR(dated, 'YYYY-MM'), ',')
           FILTER (WHERE invoiced > 0 OR agreed > 0)          AS inv_months        -- months invoiced in
FROM rows
GROUP BY client_key
HAVING SUM(quoted) > 0 OR SUM(invoiced) > 0 OR SUM(sold) > 0
ORDER BY SUM(sold) DESC, SUM(invoiced) DESC, SUM(quoted) DESC
