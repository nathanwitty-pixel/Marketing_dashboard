"""lib/footfall.py — footfall (visitors counted per shop per day) joined to walk-in sales and WhatsApp
chats, per shop per Sun–Sat week (spec: docs/footfall-marketing.md).

    daily(start, end)          → DataFrame, one row per shop-day (visitors NaN = not counted)
    weekly(start, end)         → DataFrame, one row per shop-week, with conversion and data flags
    whatsapp_weekly(start, end)→ DataFrame, paid-ad WhatsApp leads per shop-week
    SHOPS                      → {pos_config name: (WhatsApp shop, market)}
"""
from __future__ import annotations

import datetime as _dt

import pandas as pd

from lib import db, paths

# Footfall shop (pos_config.name) → (WhatsApp Monitoring shop, market). The only names that differ are
# KTDA Shop → Ktda and DAR-ES-ALAM → Sinza; the rest are the same name in title case.
SHOPS = {
    "BUSIA": ("Busia", "KENYA"), "DAR-ES-ALAM": ("Sinza", "SINZA"), "ELDORET": ("Eldoret", "KENYA"),
    "HAZINA": ("Hazina", "KENYA"), "HILTON": ("Hilton", "KENYA"), "KAKAMEGA": ("Kakamega", "KENYA"),
    "KISII": ("Kisii", "KENYA"), "KISUMU": ("Kisumu", "KENYA"), "KITENGELA": ("Kitengela", "KENYA"),
    "KTDA Shop": ("Ktda", "KENYA"), "MERU": ("Meru", "KENYA"), "MOMBASA": ("Mombasa", "KENYA"),
    "NAKURU": ("Nakuru", "KENYA"), "NANYUKI": ("Nanyuki", "KENYA"), "RONGAI": ("Rongai", "KENYA"),
    "STARMALL": ("Starmall", "KENYA"), "THIKA": ("Thika", "KENYA"), "UGANDA": ("Uganda", "UGANDA"),
}
LABEL = {k: v[0] for k, v in SHOPS.items()}          # display name = the WhatsApp shop name
MARKET = {k: v[1] for k, v in SHOPS.items()}
HILTON = "HILTON"          # counts mall / event traffic: flagged and kept out of rankings and correlations
LOW_COUNT_PCT = 80         # conversion above this (or orders > visitors) = visitors under-counted

_SQL = paths.sql("footfall_walkins.sql")

WA_SQL = """
SELECT s.name AS shop, (i.date - ((EXTRACT(DOW FROM i.date)::int) * INTERVAL '1 day'))::date AS week,
       COUNT(*) AS ad_chats,
       SUM(CASE WHEN i.is_purchased THEN 1 ELSE 0 END) AS ad_bought,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY i.response_time_first) AS med_reply
FROM denri_monitor_interaction i
JOIN denri_monitor_shop s   ON s.id = i.shop_id AND s.code IS NOT NULL
JOIN denri_monitor_source src ON src.id = i.source_id AND src.is_paid
WHERE i.date BETWEEN :s AND :e
GROUP BY 1, 2
"""


def week_start(d) -> _dt.date:
    """The Sunday that starts d's Sun–Sat week."""
    d = d if isinstance(d, _dt.date) else pd.Timestamp(d).date()
    return d - _dt.timedelta(days=(d.weekday() + 1) % 7)


def daily(start: _dt.date, end: _dt.date) -> pd.DataFrame:
    """One row per footfall shop per day: visitors (NaN = not counted), walk-in orders / KES, bulk apart."""
    with open(_SQL, encoding="utf-8") as f:
        sql = f.read()
    df = db.run_query(sql, {"start_date": start.isoformat(), "end_date": end.isoformat()})
    if df is None or df.empty:
        return pd.DataFrame()
    df = df[df["shop"].isin(SHOPS)].copy()
    df["day"] = pd.to_datetime(df["day"]).dt.date
    for c in ("orders", "kes", "bulk_orders", "bulk_kes", "bulk_units", "bulk_max_line"):
        df[c] = pd.to_numeric(df[c]).fillna(0)
    df["visitors"] = pd.to_numeric(df["visitors"])
    df["counted"] = df["visitors"].notna()
    df["week"] = df["day"].map(week_start)
    return df


def weekly(start: _dt.date, end: _dt.date) -> pd.DataFrame:
    """One row per shop per Sun–Sat week. Conversion and revenue use COUNTED days only; days with walk-in
    orders but no count are counted in `not_counted_days`, never as 0 visitors."""
    d = daily(start, end)
    if d.empty:
        return d
    c = d[d["counted"]]
    g = c.groupby(["shop", "week"]).agg(
        visitors=("visitors", "sum"), orders=("orders", "sum"), kes=("kes", "sum"),
        bulk_orders=("bulk_orders", "sum"), bulk_kes=("bulk_kes", "sum"), bulk_units=("bulk_units", "sum"),
        bulk_max_line=("bulk_max_line", "max"), days=("day", "nunique"))
    nc = (d[~d["counted"] & (d["orders"] > 0)].groupby(["shop", "week"])
          .agg(not_counted_days=("day", "nunique"), not_counted_orders=("orders", "sum")))
    w = g.join(nc, how="outer").fillna(0).reset_index()
    w["conversion"] = (w["orders"] / w["visitors"].where(w["visitors"] > 0) * 100).round(1)
    w["kes_ex_bulk"] = w["kes"] - w["bulk_kes"]
    w["orders_ex_bulk"] = w["orders"] - w["bulk_orders"]
    w["rev_per_visitor"] = (w["kes_ex_bulk"] / w["visitors"].where(w["visitors"] > 0)).round(0)
    w["rev_per_visitor_all"] = (w["kes"] / w["visitors"].where(w["visitors"] > 0)).round(0)
    w["low_count"] = (w["conversion"] > LOW_COUNT_PCT) | (w["orders"] > w["visitors"])
    w["hilton"] = w["shop"] == HILTON
    w["label"] = w["shop"].map(LABEL)
    w["market"] = w["shop"].map(MARKET)
    return w.sort_values(["shop", "week"]).reset_index(drop=True)


def whatsapp_weekly(start: _dt.date, end: _dt.date) -> pd.DataFrame:
    """Paid-ad WhatsApp leads per WhatsApp shop per Sun–Sat week: chats, bought, median first reply (min)."""
    df = db.run_query(WA_SQL, {"s": start.isoformat(), "e": end.isoformat()})
    if df is None or df.empty:
        return pd.DataFrame(columns=["shop", "week", "ad_chats", "ad_bought", "med_reply"])
    df["week"] = pd.to_datetime(df["week"]).dt.date
    for c in ("ad_chats", "ad_bought", "med_reply"):
        df[c] = pd.to_numeric(df[c])
    return df
