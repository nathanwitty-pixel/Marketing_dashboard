WITH params AS (
  SELECT
    CAST(:start_date AS DATE) AS start_date,
    CAST(:end_date AS DATE) AS end_date
),
moves AS MATERIALIZED (
  SELECT
    m.id,
    m.state,
    m.product_qty            AS qty,
    DATE(m."date")           AS move_date,
    EXTRACT(DOW FROM m."date") = 0 AS is_sunday,
    src.id                   AS src_id,
    dest.id                  AS dest_id,
    src.complete_name        AS src_path,
    dest.complete_name        AS dest_path,
    src."name"               AS src_short,
    dest."name"              AS dest_short,
    COALESCE(pt."name", pp.id::text) AS bag_name
  FROM stock_move m
  JOIN stock_location src  ON m.location_id = src.id
  JOIN stock_location dest ON m.location_dest_id = dest.id
  JOIN product_product pp  ON m.product_id = pp.id
  LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
  CROSS JOIN params p
  WHERE DATE(m."date") BETWEEN p.start_date AND p.end_date
    AND COALESCE(pt."name",'') NOT LIKE '%+%'
),
code_mapping AS (
  SELECT 'STAR' AS code, 'STARMALL' AS full_name
  UNION ALL SELECT 'STARMALL', 'STARMALL'
  UNION ALL SELECT 'MSA', 'MOMBASA'
  UNION ALL SELECT 'MOMBASA', 'MOMBASA'
  UNION ALL SELECT 'NAKS', 'NAKURU'
  UNION ALL SELECT 'NAKURU', 'NAKURU'
  UNION ALL SELECT 'ELD', 'ELDORET'
  UNION ALL SELECT 'ELDORET', 'ELDORET'
  UNION ALL SELECT 'KSM', 'KISUMU'
  UNION ALL SELECT 'KISUMU', 'KISUMU'
  UNION ALL SELECT 'MERU', 'MERU'
  UNION ALL SELECT 'THK', 'THIKA'
  UNION ALL SELECT 'THIKA', 'THIKA'
  UNION ALL SELECT 'HAZ', 'HAZINA'
  UNION ALL SELECT 'HAZINA', 'HAZINA'
  UNION ALL SELECT 'KITE', 'KITENGELA'
  UNION ALL SELECT 'KITENGELA', 'KITENGELA'
  UNION ALL SELECT 'RONG', 'RONGAI'
  UNION ALL SELECT 'RONGAI', 'RONGAI'
  UNION ALL SELECT 'NAN', 'NANYUKI'
  UNION ALL SELECT 'NANYUKI', 'NANYUKI'
  UNION ALL SELECT 'KAK', 'KAKAMEGA'
  UNION ALL SELECT 'KAKAMEGA', 'KAKAMEGA'
  UNION ALL SELECT 'HTN', 'HILTON'
  UNION ALL SELECT 'HILTON', 'HILTON'
  UNION ALL SELECT 'DAR', 'SINZA'
  UNION ALL SELECT 'SINZA', 'SINZA'
  UNION ALL SELECT 'UG', 'UGANDA'
  UNION ALL SELECT 'UGANDA', 'UGANDA'
  UNION ALL SELECT 'KSI', 'KISII'
  UNION ALL SELECT 'KISII', 'KISII'
  UNION ALL SELECT 'BUSIA', 'BUSIA'
  UNION ALL SELECT 'WEBSITE', 'WEBSITE'
  UNION ALL SELECT 'WEB', 'WEBSITE'
  UNION ALL SELECT 'JUMIA', 'JUMIA'
  UNION ALL SELECT 'JMA', 'JUMIA'
  UNION ALL SELECT 'MRKT', 'MRKT'
  UNION ALL SELECT 'MKT', 'MRKT'
  UNION ALL SELECT 'MARKET', 'MRKT'
),
receipts_raw AS (
  SELECT
    m.bag_name AS bag_name,
    CASE
      WHEN m.dest_path ILIKE '%MSA/Stock%'    THEN 'MOMBASA'
      WHEN m.dest_path ILIKE '%NAKS/Stock%'   THEN 'NAKURU'
      WHEN m.dest_path ILIKE '%ELD/Stock%'    THEN 'ELDORET'
      WHEN m.dest_path ILIKE '%KSM/Stock%'    THEN 'KISUMU'
      WHEN m.dest_path ILIKE '%MERU/Stock%'   THEN 'MERU'
      WHEN m.dest_path ILIKE '%THK/Stock%'    THEN 'THIKA'
      WHEN m.dest_path ILIKE '%HAZ/Stock%'    THEN 'HAZINA'
      WHEN m.dest_path ILIKE '%KITE/Stock%'   THEN 'KITENGELA'
      WHEN m.dest_path ILIKE '%NAN/Stock%'    THEN 'NANYUKI'
      WHEN m.dest_path ILIKE '%KAK/Stock%'    THEN 'KAKAMEGA'
      WHEN m.dest_path ILIKE '%KSI/Stock%'    THEN 'KISII'
      WHEN m.dest_path ILIKE '%BUSIA/Stock%'  THEN 'BUSIA'
      WHEN m.dest_path ILIKE '%RONG/Stock%'   THEN 'RONGAI'
      WHEN m.dest_path ILIKE '%STAR/Stock%'   THEN 'STARMALL'
      WHEN m.dest_path ILIKE '%CORP/Stock%'   THEN 'CORPORATE'
      WHEN m.dest_path ILIKE '%MRKT%' OR m.dest_path ILIKE '%MARKET%' THEN 'MRKT'
      WHEN m.dest_path ILIKE '%JUMIA%'        THEN 'JUMIA'
      WHEN m.dest_path ILIKE '%WEB/Stock%' OR m.dest_path ILIKE '%WEBSITE%' THEN 'WEBSITE'
      ELSE NULL
    END AS dest_name,
    m.qty,
    m.move_date
  FROM moves m
  WHERE m.src_path ILIKE 'FINWH/Goods in Transit/%'
    AND m.state = 'done'
    AND NOT m.is_sunday
    AND m.dest_path NOT ILIKE '%DAR%'
    AND m.dest_path NOT ILIKE '%SINZA%'
    AND m.dest_path NOT ILIKE '%UG/Stock%'
    AND m.dest_path NOT ILIKE '%UGANDA%'
    AND m.dest_path NOT ILIKE '%CBD/Stock%'
    AND m.dest_path NOT ILIKE '%KTDA/Stock%'
    AND m.dest_path NOT ILIKE '%HTN/Stock%'
),
arrivals_dedup AS (
  SELECT DISTINCT bag_name, dest_name, qty, move_date, 'Direct' AS src, NULL::int AS dedup_key
  FROM receipts_raw
  WHERE dest_name IS NOT NULL
),
cbd_out_to_shops_raw AS (
  SELECT
    m.bag_name AS bag_name,
    CASE
      WHEN m.dest_path ILIKE '%MSA/Stock%'    THEN 'MOMBASA'
      WHEN m.dest_path ILIKE '%NAKS/Stock%'   THEN 'NAKURU'
      WHEN m.dest_path ILIKE '%ELD/Stock%'    THEN 'ELDORET'
      WHEN m.dest_path ILIKE '%KSM/Stock%'    THEN 'KISUMU'
      WHEN m.dest_path ILIKE '%MERU/Stock%'   THEN 'MERU'
      WHEN m.dest_path ILIKE '%THK/Stock%'    THEN 'THIKA'
      WHEN m.dest_path ILIKE '%HAZ/Stock%'    THEN 'HAZINA'
      WHEN m.dest_path ILIKE '%KITE/Stock%'   THEN 'KITENGELA'
      WHEN m.dest_path ILIKE '%NAN/Stock%'    THEN 'NANYUKI'
      WHEN m.dest_path ILIKE '%KAK/Stock%'    THEN 'KAKAMEGA'
      WHEN m.dest_path ILIKE '%KSI/Stock%'    THEN 'KISII'
      WHEN m.dest_path ILIKE '%BUSIA/Stock%'  THEN 'BUSIA'
      WHEN m.dest_path ILIKE '%RONG/Stock%' OR m.dest_path ILIKE '%RONG%' THEN 'RONGAI'
      WHEN m.dest_path ILIKE '%STAR/Stock%'   THEN 'STARMALL'
      WHEN m.dest_path ILIKE '%HTN/Stock%'    THEN 'HILTON'
      WHEN m.dest_path ILIKE '%CORP/Stock%'   THEN 'CORPORATE'
      WHEN m.dest_path ILIKE '%MRKT%' OR m.dest_path ILIKE '%MARKET%' THEN 'MRKT'
      WHEN m.dest_path ILIKE '%JUMIA%'        THEN 'JUMIA'
      WHEN m.dest_path ILIKE '%WEB/Stock%' OR m.dest_path ILIKE '%WEBSITE%' THEN 'WEBSITE'
      ELSE NULL
    END AS dest_name,
    m.qty AS qty,
    m.state AS move_state,
    m.move_date AS move_date,
    'CBD' AS src,
    m.id AS dedup_key
  FROM moves m
  WHERE m.src_path ILIKE '%CBD/Stock%'
    AND m.dest_path NOT ILIKE '%CBD/Stock%'
    AND m.dest_path NOT ILIKE '%KTDA/Stock%'
    AND m.dest_path NOT ILIKE '%SINZA%'
    AND m.dest_path NOT ILIKE '%DAR%'
    AND m.dest_path NOT ILIKE '%UGANDA%'
    AND m.dest_path NOT ILIKE '%UG/Stock%'
    AND m.state != 'cancel'
),
cbd_out_to_shops AS (
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key
  FROM cbd_out_to_shops_raw
  WHERE dest_name IS NOT NULL
),
su_receipts AS (
  SELECT
    m.bag_name AS bag_name,
    CASE
      WHEN m.dest_path ILIKE 'DAR/Stock%' THEN 'SINZA'
      WHEN m.dest_path ILIKE 'UG/Stock%'  THEN 'UGANDA'
      WHEN m.src_path  ILIKE 'UG/Stock%'  THEN 'UGANDA'
    END AS dest_name,
    CASE WHEN m.src_path ILIKE 'UG/Stock%' THEN -m.qty ELSE m.qty END AS qty,
    m.move_date AS move_date,
    'Direct' AS src,
    m.id AS dedup_key
  FROM moves m
  WHERE m.state = 'done'
    AND (
      ( (m.dest_path ILIKE 'DAR/Stock%' OR m.dest_path ILIKE 'UG/Stock%')
        AND (m.src_path ILIKE '%FINWH%' OR m.src_path ILIKE '%CBD/Stock%')
        AND NOT m.is_sunday )
      OR
      ( m.dest_path ILIKE 'UG/Stock%'
        AND m.src_path ILIKE '%Inventory adjustment%' )
      OR
      ( m.src_path  ILIKE 'UG/Stock%'
        AND m.dest_path ILIKE '%Inventory adjustment%' )
    )
),
v2_finwh AS (
  SELECT
    m.bag_name AS bag_name,
    CASE
      WHEN m.dest_path ILIKE '%Goods in Transit/STARMALL%'
        OR m.dest_path ILIKE '%STAR/Stock%'                THEN 'STARMALL'
      WHEN m.dest_path ILIKE '%Goods in Transit/HAZINA%'
        OR m.dest_path ILIKE '%HAZ/Stock%'                 THEN 'HAZINA'
      WHEN m.dest_path ILIKE '%Goods in Transit/HILTON%'
        OR m.dest_path ILIKE '%HTN/Stock%'                 THEN 'HILTON'
      ELSE NULL
    END AS dest_name,
    m.qty AS qty,
    m.move_date AS move_date,
    m.is_sunday AS is_sunday
  FROM moves m
  WHERE m.src_path ILIKE '%FINWH%'
    AND m.src_path NOT ILIKE '%Goods in Transit%'
    AND m.src_id != m.dest_id
    AND m.state != 'cancel'
),
v2_transit AS (
  SELECT
    COALESCE(pt."name", pp.id::text) AS bag_name,
    CASE
      WHEN UPPER(s."name") = 'STARMALL'         THEN 'STARMALL'
      WHEN UPPER(s."name") = 'HAZINA'           THEN 'HAZINA'
      WHEN UPPER(s."name") IN ('HILTON','HTN')  THEN 'HILTON'
      ELSE NULL
    END AS dest_name,
    l.qty_dispatched AS qty,
    DATE(t.dispatch_date) AS move_date,
    EXTRACT(DOW FROM t.dispatch_date) = 0 AS is_sunday
  FROM denri_dispatch_transit_line l
  JOIN denri_dispatch_transit t ON l.transit_id = t.id
  JOIN denri_dispatch_shop s ON t.shop_id = s.id
  JOIN product_product pp ON l.product_id = pp.id
  LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
  CROSS JOIN params p
  WHERE COALESCE(pt."name",'') NOT LIKE '%+%'
    AND DATE(t.dispatch_date) BETWEEN p.start_date AND p.end_date
),
v2_arrivals AS (
  SELECT DISTINCT bag_name, dest_name, qty, move_date,
         'Direct' AS src, NULL::int AS dedup_key
  FROM (
    SELECT bag_name, dest_name, qty, move_date FROM v2_finwh
     WHERE dest_name IS NOT NULL
       AND (dest_name = 'HILTON' OR NOT is_sunday)
    UNION ALL
    SELECT bag_name, dest_name, qty, move_date FROM v2_transit
     WHERE dest_name IS NOT NULL
       AND (dest_name = 'HILTON' OR NOT is_sunday)
  ) z
),
ktda_receipts AS (
  SELECT
    m.bag_name AS bag_name,
    'KTDA' AS dest_name,
    m.qty AS qty,
    m.move_date AS move_date,
    'Direct' AS src,
    m.id AS dedup_key
  FROM moves m
  WHERE m.src_path  ILIKE 'FINWH/Goods in Transit%'
    AND m.dest_path ILIKE '%CBD/Stock%'
    AND m.state = 'done'
),
v2_cbd_forward AS (
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key
  FROM cbd_out_to_shops_raw
  WHERE dest_name IS NOT NULL
    AND dest_name <> 'WEBSITE'
    AND move_state = 'done'
),
cbd_gave_out AS (
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key
  FROM cbd_out_to_shops_raw
  WHERE dest_name IS NOT NULL
    AND move_state = 'done'
),
v2_cbd_add AS (
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key
  FROM v2_cbd_forward
),
v2_cbd_deduct AS (
  SELECT bag_name, 'KTDA' AS dest_name, -qty AS qty, move_date, src, dedup_key
  FROM v2_cbd_forward
),
v2_hilton_forward AS (
  SELECT
    m.bag_name AS bag_name,
    CASE
      WHEN m.dest_path ILIKE '%MSA/Stock%'    THEN 'MOMBASA'
      WHEN m.dest_path ILIKE '%NAKS/Stock%'   THEN 'NAKURU'
      WHEN m.dest_path ILIKE '%ELD/Stock%'    THEN 'ELDORET'
      WHEN m.dest_path ILIKE '%KSM/Stock%'    THEN 'KISUMU'
      WHEN m.dest_path ILIKE '%MERU/Stock%'   THEN 'MERU'
      WHEN m.dest_path ILIKE '%THK/Stock%'    THEN 'THIKA'
      WHEN m.dest_path ILIKE '%HAZ/Stock%'    THEN 'HAZINA'
      WHEN m.dest_path ILIKE '%KITE/Stock%'   THEN 'KITENGELA'
      WHEN m.dest_path ILIKE '%NAN/Stock%'    THEN 'NANYUKI'
      WHEN m.dest_path ILIKE '%KAK/Stock%'    THEN 'KAKAMEGA'
      WHEN m.dest_path ILIKE '%KSI/Stock%'    THEN 'KISII'
      WHEN m.dest_path ILIKE '%BUSIA/Stock%'  THEN 'BUSIA'
      WHEN m.dest_path ILIKE '%RONG%'         THEN 'RONGAI'
      WHEN m.dest_path ILIKE '%STAR/Stock%'   THEN 'STARMALL'
      WHEN m.dest_path ILIKE '%CORP/Stock%'   THEN 'CORPORATE'
      WHEN m.dest_path ILIKE '%MRKT%' OR m.dest_path ILIKE '%MARKET%' THEN 'MRKT'
      WHEN m.dest_path ILIKE '%JUMIA%'        THEN 'JUMIA'
      WHEN m.dest_path ILIKE '%CBD/Stock%'
        OR m.dest_path ILIKE '%KTDA%'
        OR m.dest_path ILIKE '%WEB/Stock%'
        OR m.dest_path ILIKE '%WEBSITE%'      THEN 'KTDA'
      ELSE NULL
    END AS dest_name,
    m.qty AS qty,
    m.move_date AS move_date,
    'Hilton' AS src,
    m.id AS dedup_key
  FROM moves m
  WHERE m.src_path ILIKE '%HTN/Stock%'
    AND m.dest_path NOT ILIKE '%HTN/Stock%'
    AND m.dest_path NOT ILIKE '%SINZA%'
    AND m.dest_path NOT ILIKE '%DAR%'
    AND m.dest_path NOT ILIKE '%UGANDA%'
    AND m.dest_path NOT ILIKE '%UG/Stock%'
    AND m.state != 'cancel'
),
v2_hilton_add AS (
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key
  FROM v2_hilton_forward
  WHERE dest_name IS NOT NULL
    AND dest_name <> 'KTDA'
),
v2_hilton_deduct AS (
  SELECT bag_name, 'HILTON' AS dest_name, -qty AS qty, move_date, src, dedup_key
  FROM v2_hilton_forward
  WHERE dest_name IS NOT NULL
),
ktda_new AS (
  SELECT
    m.bag_name AS bag_name,
    'KTDA NEW' AS dest_name,
    SUM(CASE
          WHEN m.dest_path ILIKE '%KTDA/Stock%'
           AND m.src_path  ILIKE '%CBD/Stock%'  THEN  m.qty
          WHEN m.src_path  ILIKE '%KTDA/Stock%'
           AND m.dest_path ILIKE '%CBD/Stock%'  THEN -m.qty
          ELSE 0 END) AS qty
  FROM moves m
  WHERE ( (m.dest_path ILIKE '%KTDA/Stock%' AND m.src_path ILIKE '%CBD/Stock%')
          OR (m.src_path ILIKE '%KTDA/Stock%' AND m.dest_path ILIKE '%CBD/Stock%') )
    AND m.src_id != m.dest_id
    AND m.state != 'cancel'
  GROUP BY m.bag_name
),
denri_shops AS (
  SELECT bag_name, SUM(qty) AS denri_qty
  FROM cbd_gave_out
  GROUP BY bag_name
),
all_moves AS (
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key
  FROM (
    SELECT bag_name,
           CASE WHEN dest_name = 'WEBSITE' THEN 'KTDA' ELSE dest_name END AS dest_name,
           qty, move_date, src, dedup_key
    FROM arrivals_dedup
  ) v1_legs
  WHERE dest_name NOT IN ('STARMALL','HAZINA','KTDA','HILTON')
  UNION ALL
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key FROM su_receipts
  UNION ALL
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key FROM v2_arrivals
  UNION ALL
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key FROM ktda_receipts
  UNION ALL
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key FROM v2_cbd_add
  UNION ALL
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key FROM v2_hilton_add
  UNION ALL
  SELECT bag_name, dest_name, qty, move_date, src, dedup_key FROM v2_hilton_deduct
),
distinct_moves AS (
  SELECT DISTINCT bag_name, dest_name, qty, move_date, src, dedup_key
  FROM all_moves
),
shop_agg AS (
  SELECT bag_name, dest_name, SUM(qty) AS qty
  FROM distinct_moves
  GROUP BY bag_name, dest_name
),
aggregated_moves AS (
  SELECT bag_name, dest_name, qty FROM shop_agg
  UNION ALL
  SELECT bag_name, dest_name, qty FROM ktda_new WHERE qty <> 0
),
jumia_src AS (
  SELECT bag_name,
         STRING_AGG(src || ': ' || s_qty, ', ' ORDER BY src) AS src_txt
  FROM (
    SELECT bag_name, src, SUM(qty) AS s_qty
    FROM distinct_moves
    WHERE dest_name = 'JUMIA'
    GROUP BY bag_name, src
    HAVING SUM(qty) <> 0
  ) z
  GROUP BY bag_name
),
mrkt_src AS (
  SELECT bag_name,
         STRING_AGG(src || ': ' || s_qty, ', ' ORDER BY src) AS src_txt
  FROM (
    SELECT bag_name, src, SUM(qty) AS s_qty
    FROM distinct_moves
    WHERE dest_name = 'MRKT'
    GROUP BY bag_name, src
    HAVING SUM(qty) <> 0
  ) z
  GROUP BY bag_name
),
bag_universe AS (
  SELECT bag_name FROM aggregated_moves
  UNION
  SELECT bag_name FROM denri_shops
),
pivoted_detail AS (
  SELECT
    b.bag_name,
    SUM(CASE WHEN dest_name = 'STARMALL' THEN qty ELSE 0 END)   AS "STARMALL",
    SUM(CASE WHEN dest_name = 'MOMBASA' THEN qty ELSE 0 END)    AS "MOMBASA",
    SUM(CASE WHEN dest_name = 'NAKURU' THEN qty ELSE 0 END)     AS "NAKURU",
    SUM(CASE WHEN dest_name = 'ELDORET' THEN qty ELSE 0 END)    AS "ELDORET",
    SUM(CASE WHEN dest_name = 'KISUMU' THEN qty ELSE 0 END)     AS "KISUMU",
    SUM(CASE WHEN dest_name = 'MERU' THEN qty ELSE 0 END)       AS "MERU",
    SUM(CASE WHEN dest_name = 'THIKA' THEN qty ELSE 0 END)      AS "THIKA",
    SUM(CASE WHEN dest_name = 'HAZINA' THEN qty ELSE 0 END)     AS "HAZINA",
    SUM(CASE WHEN dest_name = 'KITENGELA' THEN qty ELSE 0 END)  AS "KITENGELA",
    SUM(CASE WHEN dest_name = 'WEBSITE' THEN qty ELSE 0 END)    AS "WEBSITE",
    SUM(CASE WHEN dest_name = 'NANYUKI' THEN qty ELSE 0 END)    AS "NANYUKI",
    SUM(CASE WHEN dest_name = 'KAKAMEGA' THEN qty ELSE 0 END)   AS "KAKAMEGA",
    SUM(CASE WHEN dest_name = 'HILTON' THEN qty ELSE 0 END)     AS "HILTON",
    SUM(CASE WHEN dest_name = 'JUMIA' THEN qty ELSE 0 END)      AS "JUMIA",
    SUM(CASE WHEN dest_name = 'MRKT' THEN qty ELSE 0 END)       AS "MRKT",
    SUM(CASE WHEN dest_name = 'SINZA' THEN qty ELSE 0 END)      AS "SINZA",
    SUM(CASE WHEN dest_name = 'UGANDA' THEN qty ELSE 0 END)     AS "UGANDA",
    SUM(CASE WHEN dest_name = 'KISII' THEN qty ELSE 0 END)      AS "KISII",
    SUM(CASE WHEN dest_name = 'KTDA' THEN qty ELSE 0 END)       AS "KTDA",
    SUM(CASE WHEN dest_name = 'KTDA NEW' THEN qty ELSE 0 END)   AS "KTDA NEW",
    SUM(CASE WHEN dest_name = 'BUSIA' THEN qty ELSE 0 END)      AS "BUSIA",
    SUM(CASE WHEN dest_name = 'RONGAI' THEN qty ELSE 0 END)     AS "RONGAI",
    SUM(CASE WHEN dest_name = 'CORPORATE' THEN qty ELSE 0 END)  AS "CORPORATE",
    COALESCE(ds.denri_qty,0)                                    AS "DENRI SHOPS"
  FROM bag_universe b
  LEFT JOIN aggregated_moves a ON a.bag_name = b.bag_name
  LEFT JOIN denri_shops ds     ON ds.bag_name = b.bag_name
  GROUP BY b.bag_name, ds.denri_qty
),
pivoted_valued AS (
  SELECT *
  FROM pivoted_detail
  WHERE ("STARMALL" <> 0 OR "MOMBASA" <> 0 OR "NAKURU" <> 0 OR "ELDORET" <> 0
      OR "KISUMU" <> 0 OR "MERU" <> 0 OR "THIKA" <> 0 OR "HAZINA" <> 0
      OR "KITENGELA" <> 0 OR "NANYUKI" <> 0 OR "KAKAMEGA" <> 0 OR "HILTON" <> 0
      OR "JUMIA" <> 0 OR "MRKT" <> 0 OR "SINZA" <> 0 OR "UGANDA" <> 0
      OR "KISII" <> 0 OR "KTDA" <> 0 OR "KTDA NEW" <> 0 OR "BUSIA" <> 0
      OR "RONGAI" <> 0 OR "CORPORATE" <> 0 OR "DENRI SHOPS" <> 0)
),
family_map AS (
  SELECT DISTINCT bag_name, SPLIT_PART(bag_name, ' ', 1) AS family
  FROM pivoted_valued
),
family_subtotals AS (
  SELECT
    f.family || ' TOTAL' AS bag_name,
    SUM(p."STARMALL")   AS "STARMALL", SUM(p."MOMBASA")  AS "MOMBASA",
    SUM(p."NAKURU")     AS "NAKURU",   SUM(p."ELDORET")  AS "ELDORET",
    SUM(p."KISUMU")     AS "KISUMU",   SUM(p."MERU")     AS "MERU",
    SUM(p."THIKA")      AS "THIKA",    SUM(p."HAZINA")   AS "HAZINA",
    SUM(p."KITENGELA")  AS "KITENGELA",SUM(p."WEBSITE")  AS "WEBSITE",
    SUM(p."NANYUKI")    AS "NANYUKI",  SUM(p."KAKAMEGA") AS "KAKAMEGA",
    SUM(p."HILTON")     AS "HILTON",   SUM(p."JUMIA")    AS "JUMIA",
    SUM(p."MRKT")       AS "MRKT",     SUM(p."SINZA")    AS "SINZA",
    SUM(p."UGANDA")     AS "UGANDA",   SUM(p."KISII")    AS "KISII",
    SUM(p."KTDA")       AS "KTDA",     SUM(p."KTDA NEW") AS "KTDA NEW",
    SUM(p."BUSIA")      AS "BUSIA",    SUM(p."RONGAI")   AS "RONGAI",
    SUM(p."CORPORATE")  AS "CORPORATE",
    SUM(p."DENRI SHOPS") AS "DENRI SHOPS"
  FROM pivoted_valued p
  JOIN family_map f ON p.bag_name = f.bag_name
  GROUP BY f.family
),
grand_total AS (
  SELECT
    'GRAND TOTAL' AS bag_name,
    SUM("STARMALL")   AS "STARMALL", SUM("MOMBASA")  AS "MOMBASA",
    SUM("NAKURU")     AS "NAKURU",   SUM("ELDORET")  AS "ELDORET",
    SUM("KISUMU")     AS "KISUMU",   SUM("MERU")     AS "MERU",
    SUM("THIKA")      AS "THIKA",    SUM("HAZINA")   AS "HAZINA",
    SUM("KITENGELA")  AS "KITENGELA",SUM("WEBSITE")  AS "WEBSITE",
    SUM("NANYUKI")    AS "NANYUKI",  SUM("KAKAMEGA") AS "KAKAMEGA",
    SUM("HILTON")     AS "HILTON",   SUM("JUMIA")    AS "JUMIA",
    SUM("MRKT")       AS "MRKT",     SUM("SINZA")    AS "SINZA",
    SUM("UGANDA")     AS "UGANDA",   SUM("KISII")    AS "KISII",
    SUM("KTDA")       AS "KTDA",     SUM("KTDA NEW") AS "KTDA NEW",
    SUM("BUSIA")      AS "BUSIA",    SUM("RONGAI")   AS "RONGAI",
    SUM("CORPORATE")  AS "CORPORATE",
    SUM("DENRI SHOPS") AS "DENRI SHOPS"
  FROM pivoted_valued
),
combined AS (
  SELECT p.bag_name,
    "STARMALL","MOMBASA","NAKURU","ELDORET","KISUMU","MERU","THIKA","HAZINA",
    "KITENGELA","WEBSITE","NANYUKI","KAKAMEGA","HILTON","JUMIA","MRKT","SINZA","UGANDA",
    "KISII","KTDA","KTDA NEW","BUSIA","RONGAI","CORPORATE","DENRI SHOPS",
    js.src_txt AS jumia_src_txt, ms.src_txt AS mrkt_src_txt,
    SPLIT_PART(p.bag_name, ' ', 1) AS family, 0 AS sort_order
  FROM pivoted_valued p
  LEFT JOIN jumia_src js ON js.bag_name = p.bag_name
  LEFT JOIN mrkt_src  ms ON ms.bag_name = p.bag_name
  UNION ALL
  SELECT bag_name,
    "STARMALL","MOMBASA","NAKURU","ELDORET","KISUMU","MERU","THIKA","HAZINA",
    "KITENGELA","WEBSITE","NANYUKI","KAKAMEGA","HILTON","JUMIA","MRKT","SINZA","UGANDA",
    "KISII","KTDA","KTDA NEW","BUSIA","RONGAI","CORPORATE","DENRI SHOPS",
    NULL, NULL,
    bag_name AS family, 1 AS sort_order
  FROM family_subtotals
  UNION ALL
  SELECT bag_name,
    "STARMALL","MOMBASA","NAKURU","ELDORET","KISUMU","MERU","THIKA","HAZINA",
    "KITENGELA","WEBSITE","NANYUKI","KAKAMEGA","HILTON","JUMIA","MRKT","SINZA","UGANDA",
    "KISII","KTDA","KTDA NEW","BUSIA","RONGAI","CORPORATE","DENRI SHOPS",
    NULL, NULL,
    '~~~~' AS family, 2 AS sort_order
  FROM grand_total
)
SELECT
  bag_name AS "Product",
  "STARMALL","MOMBASA","NAKURU","ELDORET","KISUMU","MERU","THIKA","HAZINA",
  "KITENGELA","WEBSITE","NANYUKI","KAKAMEGA","HILTON","JUMIA","MRKT","SINZA","UGANDA",
  "KISII","KTDA","KTDA NEW","BUSIA","RONGAI",
  ("STARMALL"+"MOMBASA"+"NAKURU"+"ELDORET"+"KISUMU"+"MERU"+"THIKA"+"HAZINA"+
   "KITENGELA"+"WEBSITE"+"NANYUKI"+"KAKAMEGA"+"HILTON"+"JUMIA"+"MRKT"+"SINZA"+"UGANDA"+
   "KISII"+"KTDA"+"KTDA NEW"+"BUSIA"+"RONGAI") AS "TOTAL",
  "CORPORATE",
  "DENRI SHOPS",
  CASE WHEN "JUMIA" <> 0 THEN "JUMIA" || ' (' || COALESCE(jumia_src_txt,'') || ')' END AS "JUMIA SRC",
  CASE WHEN "MRKT"  <> 0 THEN "MRKT"  || ' (' || COALESCE(mrkt_src_txt,'')  || ')' END AS "MRKT SRC",
  family AS "Family",
  sort_order
FROM combined
ORDER BY family, sort_order, bag_name;
