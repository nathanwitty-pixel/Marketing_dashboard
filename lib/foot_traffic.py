"""lib/foot_traffic.py — the Denri dashboard's Foot Traffic page figures, per market, for the weekly report.

Ported from Denri-dashboard (Nate): lib/footfall.py (combine + its rules), lib/queries.py FOOTFALL_COUNTS,
FOOTFALL_SALES and WA_SHOP_KPIS, views/9_Footfall_Traffic.py (the three KPI rows). Keep the two in step.

    summary(start, end) → {"KE": {...}, "UG": {...}, "TZ": {...}}, each with three groups:
      walkins     — the people who came into the shops (counted days only)
      not_walkins — orders that are not part of the conversion
      whatsapp    — chats handled by every shop of that market, from the WhatsApp Monitor

Rules (as on the Foot Traffic page):
  * A count of 0 stands only when no walk-in bought that day; otherwise it is "not counted" (NaN).
  * Conversion and revenue per walk-in use counted days only.
  * A walk-in order rung under a shop's own number or a shop attendant's is not a purchased
    walk-in (its money still counts in walk-in revenue).
  * Hilton is left out of Kenya's walk-ins: it counts mall / event traffic (lib/footfall.HILTON), as on the
    Followers vs sales chart.
"""
from __future__ import annotations

import datetime as _dt

import numpy as np
import pandas as pd

from lib import db

_SHOP = """
    CASE
        WHEN COALESCE(sw.name, sl.complete_name) ILIKE '%Dar-Es-Alam%' THEN 'Sinza'
        ELSE INITCAP(TRIM(REGEXP_REPLACE(
                 COALESCE(sw.name, sl.complete_name, 'N/A'), '\\s*Shop\\s*', '', 'gi')))
    END"""

_TILL_JOINS = """
LEFT JOIN stock_picking_type spt ON spt.id = pconf.picking_type_id
LEFT JOIN stock_warehouse sw ON sw.id = spt.warehouse_id
LEFT JOIN stock_location sl ON sl.id = spt.default_location_src_id"""

COUNTS_SQL = f"""
SELECT f.date AS "Date", {_SHOP} AS "Location", SUM(f.manual_count) AS "Visitors"
FROM denri_footfall_count f
JOIN pos_config pconf ON pconf.id = f.config_id{_TILL_JOINS}
WHERE f.date BETWEEN CAST(:start_date AS DATE) AND CAST(:end_date AS DATE)
GROUP BY 1, 2
"""

# Denri's own numbers (each shop's receipt phones, and the shop attendants under
# HR → Employees → Sales / Shop Attendants): a walk-in order rung under one of
# them is not a purchased walk-in (Denri dashboard queries._STAFF_PHONE_KEYS).
_STAFF_KEYS = """
    SELECT RIGHT(REGEXP_REPLACE(num, '[^0-9]', '', 'g'), 9) AS key
    FROM pos_config pc
    CROSS JOIN LATERAL unnest(string_to_array(pc.receipt_phones, ',')) AS num
    WHERE pc.active AND COALESCE(TRIM(pc.receipt_phones), '') <> ''
    UNION
    SELECT RIGHT(REGEXP_REPLACE(p.phone, '[^0-9]', '', 'g'), 9)
    FROM hr_employee e
    JOIN hr_department d ON d.id = e.department_id
    CROSS JOIN LATERAL (VALUES (e.mobile_phone), (e.work_phone)) AS p(phone)
    WHERE e.active AND d.complete_name ILIKE 'Sales / Shop Attendants%'
      AND COALESCE(TRIM(p.phone), '') <> ''"""

SALES_SQL = f"""
WITH staff_keys AS ({_STAFF_KEYS}
),
shops AS (
    SELECT DISTINCT spt.warehouse_id
    FROM denri_footfall_count f
    JOIN pos_config pc ON pc.id = f.config_id
    JOIN stock_picking_type spt ON spt.id = pc.picking_type_id
),
orders AS (
    SELECT po.id,
           (po.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::DATE AS day,
           {_SHOP} AS location,
           po.customer_type,
           po.amount_total < 0 AS refund,
           RIGHT(REGEXP_REPLACE(COALESCE(rp.phone, rp.mobile, ''), '[^0-9]', '', 'g'), 9)
               IN (SELECT key FROM staff_keys WHERE LENGTH(key) = 9) AS staff_number,
           SUM(pol.price_subtotal_incl / po.currency_rate) AS revenue
    FROM pos_order po
    JOIN pos_order_line pol ON pol.order_id = po.id
    LEFT JOIN res_partner rp ON rp.id = po.partner_id
    LEFT JOIN pos_session ps ON ps.id = po.session_id
    LEFT JOIN pos_config pconf ON pconf.id = ps.config_id{_TILL_JOINS}
    WHERE po.state NOT IN ('draft', 'cancel')
      AND spt.warehouse_id IN (SELECT warehouse_id FROM shops)
      AND po.date_order >= (CAST(:start_date AS TIMESTAMP) AT TIME ZONE 'Africa/Nairobi' AT TIME ZONE 'UTC')
      AND po.date_order <  ((CAST(:end_date AS TIMESTAMP) + INTERVAL '1 day')
                            AT TIME ZONE 'Africa/Nairobi' AT TIME ZONE 'UTC')
    GROUP BY po.id, 2, 3, 6
)
SELECT day AS "Date", location AS "Location",
       COUNT(*) FILTER (WHERE customer_type = 'walkin' AND NOT refund AND NOT staff_number)     AS "Walk-in Orders",
       COALESCE(SUM(revenue) FILTER (WHERE customer_type = 'walkin' AND NOT refund), 0)         AS "Walk-in Revenue",
       COUNT(*) FILTER (WHERE customer_type = 'online' AND NOT refund)                          AS "Online Orders",
       COUNT(*) FILTER (WHERE customer_type IN ('activation', 'employee') AND NOT refund)        AS "Other Orders",
       COUNT(*) FILTER (WHERE refund)                                                           AS "Refunds"
FROM orders GROUP BY 1, 2
"""

# Matched to the WhatsApp Monitor's own shop card (see the Denri dashboard's queries.WA_SHOP_KPIS).
WA_SQL = """
SELECT COALESCE(sh.name, 'Not recorded') AS "Shop",
       COUNT(*) FILTER (WHERE i.activity IS DISTINCT FROM 'transferred') AS "Chats",
       COUNT(*) FILTER (WHERE i.activity IS DISTINCT FROM 'transferred'
                          AND (i.activity = 'purchased' OR COALESCE(i.is_purchased, FALSE))) AS "Purchased",
       COUNT(*) FILTER (WHERE src.name ILIKE 'Meta Ad%' OR src.name ILIKE 'Status Ad%') AS "Ad Chats",
       COUNT(*) FILTER (WHERE (src.name ILIKE 'Meta Ad%' OR src.name ILIKE 'Status Ad%')
                          AND (i.activity = 'purchased' OR COALESCE(i.is_purchased, FALSE))) AS "Ad Purchased",
       COALESCE(SUM(i.response_time_avg) FILTER (
           WHERE i.response_time_avg > 0 AND i.response_time_avg <= 1440), 0) AS "Response Minutes",
       COUNT(*) FILTER (WHERE i.response_time_avg > 0 AND i.response_time_avg <= 1440) AS "Response Sampled"
FROM denri_monitor_interaction i
LEFT JOIN denri_monitor_shop   sh  ON sh.id  = i.shop_id
LEFT JOIN denri_monitor_source src ON src.id = i.source_id
WHERE i.date BETWEEN CAST(:start_date AS DATE) AND CAST(:end_date AS DATE)
GROUP BY 1
"""

MARKETS = ("KE", "UG", "TZ")


def market(shop: str) -> str:
    """Sinza → TZ, Uganda → UG, every other shop → KE (footfall Location or WhatsApp Monitor shop)."""
    s = str(shop).strip().lower()
    return "TZ" if s in ("sinza", "dar-es-alam") else "UG" if s == "uganda" else "KE"


def _pct(part: float, whole: float) -> float | None:
    return round(part / whole * 100, 1) if whole else None


def shop_days(start: _dt.date, end: _dt.date) -> pd.DataFrame:
    """One row per shop-day: visitors (NaN = not counted) beside the order types, with the 0-count rule."""
    p = {"start_date": start.isoformat(), "end_date": end.isoformat()}
    counts, sales = db.run_query(COUNTS_SQL, p), db.run_query(SALES_SQL, p)
    counts = counts if counts is not None else pd.DataFrame(columns=["Date", "Location", "Visitors"])
    sales = sales if sales is not None else pd.DataFrame(columns=["Date", "Location"])
    df = counts.merge(sales, on=["Date", "Location"], how="outer")
    cols = ["Walk-in Orders", "Walk-in Revenue", "Online Orders", "Other Orders", "Refunds"]
    for c in cols:
        df[c] = pd.to_numeric(df.get(c), errors="coerce").fillna(0)
    df["Visitors"] = pd.to_numeric(df["Visitors"], errors="coerce")
    df["Visitors"] = df["Visitors"].mask((df["Visitors"] == 0) & (df["Walk-in Orders"] > 0))
    df["Didn't Buy"] = np.where(df["Visitors"].isna(), np.nan,
                                (df["Visitors"] - df["Walk-in Orders"]).clip(lower=0))
    df["Market"] = df["Location"].map(market)
    return df


def summary(start: _dt.date, end: _dt.date) -> dict:
    """The Foot Traffic page's three KPI rows for each market over [start, end]."""
    days = shop_days(start, end)
    days = days[days["Location"].str.strip().str.upper() != "HILTON"]
    wa = db.run_query(WA_SQL, {"start_date": start.isoformat(), "end_date": end.isoformat()})
    if wa is not None and not wa.empty:
        wa = wa[wa["Shop"] != "Not recorded"].assign(Market=lambda f: f["Shop"].map(market))
    out = {}
    for m in MARKETS:
        shown = days[days["Market"] == m]
        counted = shown[shown["Visitors"].notna()]
        walkins, bought = float(counted["Visitors"].sum()), float(counted["Walk-in Orders"].sum())
        w = (wa[wa["Market"] == m].sum(numeric_only=True) if wa is not None and not wa.empty
             else pd.Series(dtype=float))
        chats, sampled, ads = float(w.get("Chats", 0)), float(w.get("Response Sampled", 0)), float(w.get("Ad Chats", 0))
        out[m] = {
            "walkins": {
                "counted": round(walkins), "shopDays": int(len(counted)),
                "purchased": round(bought), "didntBuy": round(float(counted["Didn't Buy"].sum())),
                "conversion": _pct(bought, walkins),
                "revPerWalkin": round(float(counted["Walk-in Revenue"].sum()) / walkins) if walkins else None,
            },
            "not_walkins": {
                "online": round(float(shown["Online Orders"].sum())),
                "other": round(float(shown["Other Orders"].sum())),
                "refunds": round(float(shown["Refunds"].sum())),
                "daysNotCounted": int(shown["Visitors"].isna().sum()),
                "undercounted": int((counted["Walk-in Orders"] > counted["Visitors"]).sum()),
            },
            "whatsapp": {
                "chats": round(chats), "purchased": round(float(w.get("Purchased", 0))),
                "performance": _pct(float(w.get("Purchased", 0)), chats),
                "ads": round(ads), "adConversion": _pct(float(w.get("Ad Purchased", 0)), ads),
                "adPurchased": round(float(w.get("Ad Purchased", 0))),
                "avgResponse": round(float(w.get("Response Minutes", 0)) / sampled, 1) if sampled else None,
                "sampled": round(sampled),
            },
        }
    return out
