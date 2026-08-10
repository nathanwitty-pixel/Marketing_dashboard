-- ═══════════════════════════════════════════════════════════════
-- Denri Africa · Marketing Dashboard — browse queries (Supabase)
-- Paste any block into Supabase → SQL Editor → Run.
-- Tables: denri_mkt_monthly / _weekly / _new_products / _offers
-- (loaded by push_to_supabase.py; keyed by month_key e.g. '2026-07')
-- ═══════════════════════════════════════════════════════════════


-- 0 · What's stored — row counts per table -----------------------
select 'monthly'      as table, count(*) from denri_mkt_monthly
union all select 'weekly',       count(*) from denri_mkt_weekly
union all select 'new_products', count(*) from denri_mkt_new_products
union all select 'offers',       count(*) from denri_mkt_offers;


-- 1 · Monthly summary (the headline numbers) ---------------------
select month, year,
       achieved_pct        as "achieved %",
       total_sales         as "sales (bags)",
       total_target        as "target (bags)",
       gap                 as "missed by",
       avg_weekly          as "avg / week",
       posting_kenya_pct   as "posting KE %",
       posting_sinza_pct   as "posting SZ %",
       posting_uganda_pct  as "posting UG %",
       posted_stock, unposted_stock
from denri_mkt_monthly
order by month_key desc;


-- 2 · Current Performance — weekly climb to target ---------------
--     (Sales % Achieved · Sales Bags · Target to Beat · Declined By)
select seq,
       label || ' ' || coalesce(week_month,'') as week,
       pct              as "sales % achieved",
       bags             as "sales bags",
       target_to_beat   as "target to beat",
       declined_by      as "declined by",
       cum              as "cumulative %"
from denri_mkt_weekly
where month_key = '2026-07'
order by seq;


-- 3 · New Products — sold vs target, posts vs stock --------------
select name,
       sold, remaining,
       sold + remaining as target,
       posts            as "posts done",
       stock            as "stock on hand"
from denri_mkt_new_products
where month_key = '2026-07'
order by sold desc;


-- 4 · Offer Type Analysis — every offer, all locations ----------
select region, name, offer_type,
       units as "units moved",
       value as "value (KES)",
       stock as "stock on hand"
from denri_mkt_offers
where month_key = '2026-07'
order by region, units desc nulls last;


-- 4a · Kenya only — individual offers, combo vs power deal -------
select name, offer_type, units
from denri_mkt_offers
where month_key = '2026-07' and region = 'Kenya'
order by units desc;


-- 4b · Offer mix — by count & by units, per region --------------
select region,
       offer_type,
       count(*)                                   as offers,
       sum(units)                                 as units,
       round(100.0 * count(*)  / sum(count(*))  over (partition by region), 0) as "% by count",
       round(100.0 * sum(units)/ sum(sum(units))over (partition by region), 0) as "% by units"
from denri_mkt_offers
where month_key = '2026-07'
group by region, offer_type
order by region, units desc;


-- 5 · One-row "report card" per month (summary join) ------------
select m.month, m.year, m.achieved_pct,
       (select count(*) from denri_mkt_weekly       w where w.month_key = m.month_key) as weeks,
       (select count(*) from denri_mkt_new_products n where n.month_key = m.month_key) as new_products,
       (select count(*) from denri_mkt_offers       o where o.month_key = m.month_key) as offers
from denri_mkt_monthly m
order by m.month_key desc;
