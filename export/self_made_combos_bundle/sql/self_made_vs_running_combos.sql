-- ============================================================================
-- Self-Made Combos vs Running Combos — Kenya, one month
-- ----------------------------------------------------------------------------
-- Combos follow the "A + B" naming convention (pt.name LIKE '%+%').
--   • RUNNING (official) combo  = the POS combo offers the full range of a
--     category (product_combo.include_all = TRUE) — the shop attendant picks
--     the colour. This is the mark of an official running combo.
--   • SELF-MADE combo           = a staff Combo-Request (the combo product id
--     appears in pos_combo_request) that is NOT an include_all combo — a fixed,
--     specific pairing created on the shop floor.
--
-- Set the month window below (BETWEEN start AND end). Kenya tills only
-- (Sinza / Dar-es-Salaam / Uganda excluded). qty <> 0 so SUM nets returns.
-- ============================================================================

WITH params AS (
    SELECT DATE '2026-09-01' AS start_date,
           DATE '2026-09-30' AS end_date
),
cbr AS (   -- combo products that have at least one Combo-Request (self-made)
    SELECT DISTINCT combo_product_id AS tmpl_id
    FROM pos_combo_request
    WHERE combo_product_id IS NOT NULL
),
combo_flags AS (   -- every "A + B" product, with its running / self-made marks
    SELECT pt.id AS tmpl_id,
           pt."name" AS combo,
           (pt.id IN (SELECT tmpl_id FROM cbr)) AS is_cbr,
           COALESCE((SELECT BOOL_OR(pcx.include_all)
                     FROM product_combo pcx
                     WHERE pcx.product_template_id = pt.id), FALSE) AS include_all
    FROM product_template pt
    WHERE pt."name" LIKE '%+%'
      AND pt."name" NOT ILIKE '%delivery%'
      AND pt."name" NOT ILIKE '%customi%'
),
combo_sales AS (   -- this month's Kenya sales for each combo product
    SELECT cf.combo,
           CASE WHEN cf.include_all THEN 'Running (official)'
                WHEN cf.is_cbr      THEN 'Self-made (CBR)'
                ELSE 'Other (' || CASE WHEN cf.is_cbr THEN 'cbr' ELSE 'fixed' END || ')'
           END AS combo_type,
           SUM(pl.qty)::int                              AS units,
           ROUND(SUM(pl.price_subtotal_incl))::int       AS revenue
    FROM params pr
    JOIN pos_order      p  ON p.date_order::date BETWEEN pr.start_date AND pr.end_date
                          AND p.state IN ('done', 'paid')
    JOIN pos_order_line pl ON pl.order_id = p.id AND pl.qty <> 0
    JOIN product_product  pp ON pp.id = pl.product_id
    JOIN combo_flags      cf ON cf.tmpl_id = pp.product_tmpl_id
    LEFT JOIN pos_session ps ON ps.id = p.session_id
    LEFT JOIN pos_config  pc ON pc.id = ps.config_id
    WHERE lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
    GROUP BY cf.combo, combo_type
)
-- ── Per-combo detail (comment out this SELECT to run the summary below) ──────
SELECT combo_type, combo, units, revenue,
       ROUND(revenue::numeric / NULLIF(units, 0))::int AS avg_unit_price
FROM combo_sales
ORDER BY combo_type, units DESC, revenue DESC;

-- ── Summary by type (uncomment to run instead) ──────────────────────────────
-- SELECT combo_type,
--        COUNT(*)      AS combos,
--        SUM(units)    AS units,
--        SUM(revenue)  AS revenue
-- FROM combo_sales
-- GROUP BY combo_type
-- ORDER BY revenue DESC;
