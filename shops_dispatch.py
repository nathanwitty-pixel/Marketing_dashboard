"""shops_dispatch.py — live dispatch & receiving for Shops Efficiency, from Odoo.

Runs two Postgres queries (ported from the Dispatch Tracking app) for the
current Sun–Sat week and the current month, and writes shops_dispatch_db.json
for shops_efficiency.py to fold into the page:

  COMBINED_DISTRIBUTION  → bags distributed IN to each shop  ("the in for the shops")
  SHOPS_RECEIVING        → how quickly each shop received: same-day / next-day /
                           two-days / later / in-transit, plus a 0–100 score.

Safe to run any time. If Postgres is unreachable it prints why and leaves the
old JSON in place, so the launcher never fails on it.

Run:
    python shops_dispatch.py
"""
from __future__ import annotations

import calendar
import datetime
import json
import os

from lib import db

BASE = os.path.dirname(os.path.abspath(__file__))
SQL_DIR = os.path.join(BASE, "sql")
OUT_FILE = os.path.join(BASE, "shops_dispatch_db.json")

# Kenya shops shown on the efficiency page (matches shops_efficiency.KENYA_SHOPS).
KENYA_SHOPS = [
    "STARMALL", "MOMBASA", "NAKURU", "ELDORET", "KISUMU", "MERU",
    "THIKA", "HAZINA", "KITENGELA", "NANYUKI", "KAKAMEGA", "HILTON",
    "KISII", "KTDA", "BUSIA", "RONGAI",
]

# How each receipt outcome is credited when scoring a shop (bags-weighted).
RECEIPT_WEIGHTS = {"Same day": 1.0, "Next day": 0.6, "Two days": 0.35, "Later": 0.15, "In transit": 0.0}
RECEIPT_ORDER = ["Same day", "Next day", "Two days", "Later", "In transit"]


def _sql(name):
    with open(os.path.join(SQL_DIR, name), encoding="utf-8") as f:
        return f.read()


def week_window(ref=None):
    """Shops-efficiency week runs Wednesday → Tuesday (i.e. Wednesday-to-Wednesday).
    weekday(): Mon=0 … Wed=2 … Sun=6."""
    ref = ref or datetime.date.today()
    start = ref - datetime.timedelta(days=(ref.weekday() - 2) % 7)   # back to the most recent Wednesday
    return start, start + datetime.timedelta(days=6)


def month_window(ref=None):
    ref = ref or datetime.date.today()
    return ref.replace(day=1), ref.replace(day=calendar.monthrange(ref.year, ref.month)[1])


def _num(v):
    try:
        return int(round(float(v)))
    except (TypeError, ValueError):
        return 0


def distributed_in(df):
    """Per-shop bags distributed IN (Combined Distribution grand-total row)."""
    out = {s: 0 for s in KENYA_SHOPS}
    if df is None or df.empty:
        return out
    gt = df[df["sort_order"] == 2]
    if gt.empty:
        return out
    row = gt.iloc[0]
    for s in KENYA_SHOPS:
        if s in df.columns:
            out[s] = _num(row[s])
    return out


def receiving(df):
    """Per-shop receiving breakdown + 0–100 score, Kenya shops only."""
    out = {}
    if df is None or df.empty:
        return out
    for shop, g in df.groupby("Shop"):
        if shop not in KENYA_SHOPS:
            continue
        bags = float(g["Qty"].sum())
        if not bags:
            continue
        by_status = {st: float(g.loc[g["Status"] == st, "Qty"].sum()) for st in RECEIPT_ORDER}
        credit = sum(by_status.get(st, 0) * w for st, w in RECEIPT_WEIGHTS.items())
        landed = g[g["Status"] != "In transit"]
        median = float(landed["Days"].median()) if not landed.empty else None
        out[shop] = {
            "sent":      _num(bags),
            "sameDay":   _num(by_status["Same day"]),
            "nextDay":   _num(by_status["Next day"]),
            "twoDays":   _num(by_status["Two days"]),
            "later":     _num(by_status["Later"]),
            "inTransit": _num(by_status["In transit"]),
            "score":     round(credit / bags * 100, 1) if bags else 0.0,
            "medianDays": (round(median, 1) if median is not None else None),
        }
    return out


def sold_by_shop(df):
    """Per-shop bags SOLD from Odoo POS, Kenya shops only."""
    out = {s: 0 for s in KENYA_SHOPS}
    if df is None or df.empty:
        return out
    for _, r in df.iterrows():
        shop = str(r["Shop"])
        if shop in out:
            out[shop] = _num(r["Bags"])
    return out


def build_period(comb_df, recv_df, sold_df, start, end):
    return {
        "start": start.isoformat(),
        "end":   end.isoformat(),
        "distributedIn": distributed_in(comb_df),
        "sold":          sold_by_shop(sold_df),
        "receiving":     receiving(recv_df),
    }


def main():
    ok, detail = db.check_connection()
    if not ok:
        print(f"Postgres not reachable — {detail}. shops_dispatch_db.json left as-is.")
        return

    comb_sql = _sql("combined_distribution.sql")
    recv_sql = _sql("shops_receiving.sql")
    sold_sql = _sql("shop_bags_sold.sql")

    wk_s, wk_e = week_window()
    mo_s, mo_e = month_window()

    # The six queries are independent and each is heavy — run them concurrently
    # (separate pooled connections) so the whole step finishes well inside the
    # dashboard's refresh timeout instead of ~6× a single query back-to-back.
    from concurrent.futures import ThreadPoolExecutor

    def q(sql, s, e):
        return db.run_query(sql, {"start_date": s.isoformat(), "end_date": e.isoformat()})

    jobs = {
        "wk_comb": (comb_sql, wk_s, wk_e), "wk_recv": (recv_sql, wk_s, wk_e), "wk_sold": (sold_sql, wk_s, wk_e),
        "mo_comb": (comb_sql, mo_s, mo_e), "mo_recv": (recv_sql, mo_s, mo_e), "mo_sold": (sold_sql, mo_s, mo_e),
    }
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = {k: ex.submit(q, sql, s, e) for k, (sql, s, e) in jobs.items()}
        r = {k: f.result() for k, f in futs.items()}

    payload = {
        "computedOn": datetime.date.today().isoformat(),
        "shops":      KENYA_SHOPS,
        "weekly":     build_period(r["wk_comb"], r["wk_recv"], r["wk_sold"], wk_s, wk_e),
        "monthly":    build_period(r["mo_comb"], r["mo_recv"], r["mo_sold"], mo_s, mo_e),
    }
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    for label, per in (("WEEKLY", payload["weekly"]), ("MONTHLY", payload["monthly"])):
        di = sum(per["distributedIn"].values())
        so = sum(per["sold"].values())
        rec = per["receiving"]
        same = sum(r["sameDay"] for r in rec.values())
        print(f"  {label:8s} {per['start']}→{per['end']}  distributed-in={di:,}  sold={so:,}  "
              f"remaining={max(di-so,0):,}  same-day={same:,}  shops={len(rec)}")
    print("shops_dispatch_db.json written.")


if __name__ == "__main__":
    main()
