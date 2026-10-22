"""lib/negative_fixes.py — stock-record accuracy per shop, from the NEGATIVE FIX LOG
(spec: docs/shops-efficiency.md › Stock record accuracy).

Every time a shop's stock cell on the STOCK_LEVELS sheet goes negative, a fix is logged in the NEGATIVE FIX LOG
tab of the STOCKS LEVELS 2026 spreadsheet. This module is the ONLY reader of that spreadsheet / tab
(tests/test_sheet_reads.py allows it here only).

    read()                       → cleaned APPLIED fixes (not total rows), oldest first
    periods(today)               → {key: (start, end, prev start, prev end, label)} — the dashboard schedule
    by_shop(start, end, ...)     → per-shop measures for one period (fixes, units, per 1,000 bags sold, …)
    block(today)                 → every period, ready for the page / the script
"""
from __future__ import annotations

import collections
import datetime as _dt

SHEET_ID = "1xWmk1CJldzs8H7G8QcNk7Q7xDbQMQpN454jy-bm-teY"      # STOCKS LEVELS 2026
TAB = "NEGATIVE FIX LOG"
LOG_START = _dt.date(2026, 10, 4)
BIG = 10                      # a single fix of 10+ units = big one-off (left out of the ranking measure)

# Log shop → the POS till(s) whose bags sold are its denominator.
TILLS = {"KTDA": ["ktda shop"], "SINZA": ["sinza", "dar-es-alam"], "UGANDA": ["uganda"]}
LABEL = {"KTDA": "Ktda"}

BAGS_BY_TILL_SQL = """
SELECT lower(COALESCE(pc."name", '')) AS till, COALESCE(SUM(pl.qty), 0)::float AS bags
FROM pos_order p
JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
WHERE p.date_order::date BETWEEN :s AND :e
  AND p.state IN ('done', 'invoiced', 'paid')
  AND pl.qty <> 0
  AND COALESCE(pt."name", '') NOT LIKE '%+%'
  AND COALESCE(pt."name", '') NOT ILIKE '%delivery%'
  AND COALESCE(pt."name", '') NOT ILIKE '%customization%'
  AND COALESCE(pt."name", '') NOT ILIKE '%strap%'
  AND COALESCE(pt."name", '') NOT ILIKE '%KES discount%'
  AND COALESCE(pt."name", '') NOT ILIKE '%sample%'
  AND COALESCE(pcat."name", '') NOT ILIKE '%Pos%'
  AND lower(COALESCE(pt."name", '')) <> ALL(:x)
GROUP BY 1
"""          # same filters as sql/bags_sold_total.sql, grouped by till


def label(shop: str) -> str:
    return LABEL.get(shop, shop.title())


def tills(shop: str) -> list[str]:
    return TILLS.get(shop, [shop.lower()])


def _date(v):
    v = str(v or "").strip()
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return _dt.datetime.strptime(v, fmt).date()
        except ValueError:
            pass
    return None


def _int(v):
    try:
        return int(float(str(v).replace(",", "").strip()))
    except (TypeError, ValueError):
        return 0


_CACHE = None


def read(sh=None) -> list[dict]:
    """APPLIED fixes from the NEGATIVE FIX LOG (not total rows), cleaned, oldest first. Cached for the run."""
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    if sh is None:
        from lib.google_auth import get_gspread_client
        sh = get_gspread_client().open_by_key(SHEET_ID)
    rows = sh.worksheet("NEGATIVE FIX LOG").get_all_values()
    if not rows:
        _CACHE = []
        return _CACHE
    hd = [h.strip().lower() for h in rows[0]]

    def col(name):
        return next(i for i, h in enumerate(hd) if h.startswith(name))
    iT, iM, iS, iR, iI, iN, iSt = (col("time"), col("mode"), col("shop"), col("row"), col("item"),
                                   col("negative"), col("status"))
    out = []
    for n, r in enumerate(rows[1:], start=2):
        r = r + [""] * (len(hd) - len(r))
        if r[iM].strip().upper() != "APPLIED" or r[iSt].strip().upper().startswith("SKIPPED"):
            continue
        d = _date(r[iT])
        shop = r[iS].strip().upper()
        if not d or not shop:
            continue
        out.append({"date": d, "shop": shop, "row": r[iR].strip(), "item": r[iI].strip(),
                    "units": abs(_int(r[iN])), "status": r[iSt].strip(), "line": n})
    out.sort(key=lambda x: (x["date"], x["line"]))
    _CACHE = out
    return out


def _sunday(d):
    return d - _dt.timedelta(days=(d.weekday() + 1) % 7)


def _month_start(d):
    return d.replace(day=1)


def _month_end(d):
    return (d.replace(day=28) + _dt.timedelta(days=4)).replace(day=1) - _dt.timedelta(days=1)


def periods(today: _dt.date) -> dict:
    """The dashboard period schedule (generators/product_performance.py periods()) + Since the log started."""
    ws = _sunday(today)
    m1 = _month_start(today)
    pm1 = _month_start(m1 - _dt.timedelta(days=1))
    ppm1 = _month_start(pm1 - _dt.timedelta(days=1))
    same = min(pm1 + (today - m1), _month_end(pm1))
    D = _dt.timedelta
    return {
        "lastweek":  (ws - D(days=7), ws - D(days=1), ws - D(days=14), ws - D(days=8), "Last week"),
        "thisweek":  (ws, today, ws - D(days=7), today - D(days=7), "This week"),
        "thismonth": (m1, today, pm1, same, "This month"),
        "lastmonth": (pm1, _month_end(pm1), ppm1, _month_end(ppm1), "Last month"),
        "sincelog":  (LOG_START, today, None, None, "Since the log started"),
    }


def bags_sold(start, end) -> dict:
    """{till (lower case): bags sold} over [start, end] from Odoo POS; {} if Postgres is down."""
    try:
        from lib import db, queries
        df = db.run_query(BAGS_BY_TILL_SQL, {"s": start.isoformat(), "e": end.isoformat(), "x": queries.excluded_products()})
        return {} if df is None else {r.till: float(r.bags) for r in df.itertuples()}
    except Exception:                                      # noqa: BLE001
        return {}


def by_shop(start, end, fixes=None, bags=None) -> dict:
    """{SHOP: measures} for fixes dated in [start, end]. Repeat = a shop-item fixed in the period that had
    already been fixed earlier since the log started (an earlier date, or an earlier line the same day)."""
    fixes = read() if fixes is None else fixes
    bags = bags_sold(start, end) if bags is None else bags
    first_seen = {}
    for f in fixes:                                         # oldest first → the first time each shop-item went negative
        first_seen.setdefault((f["shop"], f["item"]), (f["date"], f["line"]))
    out = {}
    shops = sorted({f["shop"] for f in fixes})
    for shop in shops:
        fs = [f for f in fixes if f["shop"] == shop and start <= f["date"] <= end]
        big = [f for f in fs if f["units"] >= BIG]
        normal = [f for f in fs if f["units"] < BIG]
        sold = sum(bags.get(t, 0) for t in tills(shop))
        rep = collections.Counter(f["item"] for f in fs if first_seen[(shop, f["item"])] < (f["date"], f["line"]))
        out[shop] = {
            "shop": shop, "label": label(shop),
            "fixes": len(fs), "fixesNoBig": len(normal),
            "units": sum(f["units"] for f in fs), "unitsNoBig": sum(f["units"] for f in normal),
            "bags": round(sold),
            "rate": round(len(normal) / sold * 1000, 2) if sold else None,          # the ranking measure
            "rateAll": round(len(fs) / sold * 1000, 2) if sold else None,
            "days": len({f["date"] for f in fs}),
            "repeatItems": len(rep), "repeatFixes": sum(rep.values()),
            "repeats": [[item, n] for item, n in rep.most_common()],
            "big": [{"date": f["date"].isoformat(), "item": f["item"], "units": f["units"], "row": f["row"]} for f in big],
        }
    return out


def ranked(rows: dict) -> list[dict]:
    """Best first: fewest fixes per 1,000 bags (without big one-offs); no fixes = best; no bags sold = last."""
    return sorted(rows.values(), key=lambda r: (r["rate"] is None, r["rate"] if r["rate"] is not None else 0, r["fixesNoBig"], r["label"]))


def block(today: _dt.date | None = None) -> dict:
    """Every period with its per-shop measures, the period before, the order, repeats and big one-offs."""
    today = today or _dt.date.today()
    fixes = read()
    out = {}
    for key, (s, e, ps, pe, lbl) in periods(today).items():
        cur = by_shop(s, e, fixes)
        prev = by_shop(ps, pe, fixes) if ps else {}
        order = ranked(cur)
        for r in order:
            p = prev.get(r["shop"])
            r["prevFixes"] = p["fixesNoBig"] if p else None
            r["prevRate"] = p["rate"] if p else None
        out[key] = {"label": lbl, "start": s.isoformat(), "end": e.isoformat(),
                    "prevStart": ps.isoformat() if ps else None, "prevEnd": pe.isoformat() if pe else None,
                    "shops": order,
                    "repeats": sorted(([r["label"], it, n] for r in order for it, n in r["repeats"]), key=lambda x: -x[2]),
                    "big": [dict(b, shop=r["label"]) for r in order for b in r["big"]],
                    "totalFixes": sum(r["fixes"] for r in order)}
    return {"logStart": LOG_START.isoformat(), "big": BIG, "periods": out,
            "lastLogDate": max((f["date"] for f in fixes), default=LOG_START).isoformat()}
