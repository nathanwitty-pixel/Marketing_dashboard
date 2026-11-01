"""
"Why did we move?" waterfall data — shared by Current Performance (every bag) and New Products
(only the new-product bags) (moved here from forward_projections.py, 30 Oct 2026).

Splits the change between two periods into a selling-days bar plus one bar per
region (docs/shop-regions.md) and Corporate, so the dashboard can draw
  last period → days → regions … → this period.
Days bar  = last period's bags/day × (days now − days then).
Region r  = (r's bags/day now − r's bags/day then) × days now.
The bars add up to the change exactly. Both ends use the Sales definition
(bags_sold_by_shop.sql = bags_sold_total.sql per till, + corporate paid).
Each period comes in two filters (user, 26 Oct 2026):
  with    = "With bulk orders": every sale — shop tills + Corporate (treated as a shop)
  without = "Without bulk orders": the same, minus the bulk till orders, so one big order
            can't hide the everyday selling rate. Corporate stays: it is never a bulk order.
  weeks: the dashboard weeks of last month and this month (Sun–Sat, cut at month ends —
       so Oct Wk 1 is 1–3 Oct and the days bar explains the short week), plus the current
       week so far. The page picks any two (default: last full week vs the current week)
       and marks last month's and this month's best full weeks (29–30 Oct 2026).
  mom: month to date (1st → yesterday) vs the same days last month; on the
       1st, the month just finished vs the one before it.
build(match): match(product name) → bool limits every count to those products (the
New Products page passes its list); None = every bag.
"""
import calendar
import re
from datetime import date, timedelta

from lib import report_month

_REGION_ALIAS = {"DAR-ES-ALAM": "SINZA", "KTDA SHOP": "KTDA", "WEBSITE SALES": "WEBSITE",
                 "WEBSITE": "WEBSITE", "JUMIA": "WEBSITE"}


def _shop_label(shop):
    return _REGION_ALIAS.get(shop, shop).title().replace("Ktda", "KTDA")


def _product(name):
    """Odoo / Corporate-app product name, upper-cased, without a leading "[CODE] "."""
    return re.sub(r"^\[[^\]]*\]\s*", "", str(name or "").upper().strip())


def _week_start(d):                       # Sunday that starts d's week
    return d - timedelta(days=(d.weekday() + 1) % 7)


def _perfect_week_index(d):
    """Ordinal of d's Sun–Sat week within the month, counting every week with a day in the month
    (the opening partial week is Week 1) — forward_projections._perfect_week_index."""
    year, month = d.year, d.month
    ms = date(year, month, 1)
    me = (date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)) - timedelta(days=1)
    ws, target, idx = _week_start(ms), _week_start(d), 0
    while ws <= me:
        idx += 1
        if ws == target:
            return idx
        ws += timedelta(days=7)
    return idx


def _till_days(start, end, regions, match=None):
    """[(day, region, shop, bags, bulk bags)] for start..end: one row per till per day, so one query
    can be cut into any number of weeks. With match, only those products' lines (per-product SQL)."""
    from lib import db, queries
    win = {"start_date": start.isoformat(), "end_date": end.isoformat(), "excluded": queries.excluded_products()}
    sql = queries.BAGS_SOLD_BY_SHOP if match is None else queries.BAGS_SOLD_BY_SHOP_PRODUCT
    df = db.run_query(sql, win)
    rows = []
    for _, row in (df.iterrows() if df is not None else []):
        if match is not None and not match(_product(row["product"])):
            continue
        shop = _REGION_ALIAS.get(str(row["shop"]).upper(), str(row["shop"]).upper())
        day = row["day"].date() if hasattr(row["day"], "hour") else row["day"]
        rows.append((day, regions.get(shop, "Other"), _shop_label(shop),
                     float(row["bags"] or 0), float(row["bulk_bags"] or 0)))
    return rows


def _corporate(start, end, match=None):
    """Corporate-app bags paid in start..end (all, or only the matching products)."""
    from lib import db, queries
    win = {"start_date": start.isoformat(), "end_date": end.isoformat()}
    if match is None:
        cdf = db.run_query(queries.CORPORATE_BAGS, win)
        return int(cdf.iloc[0]["bags"] or 0) if cdf is not None and not cdf.empty else 0
    cdf = db.run_query(queries.CORPORATE_BAG_LINES, win)
    return int(round(sum(float(r.bags or 0) for r in (cdf.itertuples() if cdf is not None else [])
                         if match(_product(r.product)))))


def _period_bags(start, end, regions, tills=None, match=None):
    """Corporate app ≠ corporate bulk orders: Corporate app is a sales channel, never bulk.
    Returns [(region, shop, bags, bulk bags)] for start..end, plus the day count. Bulk = a TILL order
    with a 10+ unit line (bags_sold_by_shop.sql) — that includes Corporate-team clients paying at a shop.
    The Corporate app (denri_corporate invoices) is its own channel, like a till (user, 26 Oct 2026 —
    same rule as product_performance.shop_breakdown): it is treated as a shop, so it is in both "With
    bulk orders" and "Without bulk orders", and "without" never takes it off as a bulk order.
    tills: _till_days() rows already fetched for a wider window (cut to start..end here)."""
    if tills is None:
        tills = _till_days(start, end, regions, match)
    merged = {}                                   # (region, shop) → [bags, bulk], days added up
    for day, reg, shop, bags, bulk in tills:
        if start <= day <= end:
            m = merged.setdefault((reg, shop), [0.0, 0.0])
            m[0] += bags; m[1] += bulk
    rows = [(reg, shop, b, k) for (reg, shop), (b, k) in merged.items()]
    corp = _corporate(start, end, match)
    if corp:
        rows.append(("Corporate", None, float(corp), 0.0))     # Corporate app: a channel, never bulk
    return {"days": (end - start).days + 1, "rows": rows}


def _view(p, mode):
    """One filter of a period: {"days", "total", "regions": {region: {"bags", "bulk", "shops"}}}.
    mode: "with" (every sale, bulk till orders included), "without" (bulk till orders taken out).
    Corporate is in both — it is treated as a shop, and its bulk is always 0 (never a bulk order)."""
    out = {}
    for reg, shop, bags, bulk in p["rows"]:
        v = bags if mode == "with" else bags - bulk
        r = out.setdefault(reg, {"bags": 0.0, "bulk": 0.0, "shops": {}})
        r["bags"] += v
        r["bulk"] += bulk if mode != "without" else 0
        if shop:
            r["shops"][shop] = r["shops"].get(shop, 0) + v
    out = {k: r for k, r in out.items() if round(r["bags"]) or r["shops"]}
    return {"days": p["days"], "total": sum(r["bags"] for r in out.values()), "regions": out}


def _views(a, b, *labels):
    """{with, without} waterfalls between raw periods a and b."""
    return {m: _waterfall(_view(a, m), _view(b, m), *labels) for m in ("with", "without")}


def _waterfall(a, b, a_label, b_label, a_range, b_range):
    """The bars between period a (then) and period b (now); ints that add up to b − a."""
    scale = b["days"] / a["days"] if a["days"] else 1
    days_eff = round(a["total"] * scale) - round(a["total"])
    names = sorted(set(a["regions"]) | set(b["regions"]))
    raw = {n: b["regions"].get(n, {}).get("bags", 0) - a["regions"].get(n, {}).get("bags", 0) * scale
           for n in names}
    bars = {n: round(v) for n, v in raw.items()}
    # Rounding leftovers go on the biggest mover so the bars land exactly on b.
    left = round(b["total"]) - round(a["total"]) - days_eff - sum(bars.values())
    if left and bars:
        bars[max(bars, key=lambda n: abs(raw[n]))] += left
    rows = []
    for n in names:
        ra, rb = a["regions"].get(n, {}), b["regions"].get(n, {})
        shops = sorted(set(ra.get("shops", {})) | set(rb.get("shops", {})))
        rows.append({
            "region": n, "delta": bars[n],
            "then": round(ra.get("bags", 0)), "now": round(rb.get("bags", 0)),
            "bulkThen": round(ra.get("bulk", 0)), "bulkNow": round(rb.get("bulk", 0)),
            "shops": [{"shop": s,
                       "then": round(ra.get("shops", {}).get(s, 0)),
                       "now": round(rb.get("shops", {}).get(s, 0)),
                       "delta": round(rb.get("shops", {}).get(s, 0) - ra.get("shops", {}).get(s, 0) * scale)}
                      for s in shops],
        })
    return {"then": {"label": a_label, "range": a_range, "days": a["days"], "bags": round(a["total"])},
            "now":  {"label": b_label, "range": b_range, "days": b["days"], "bags": round(b["total"])},
            "daysEffect": days_eff, "regions": rows}


def _rng(s, e):                                  # "1 Oct", "18–24 Oct", "27 Sep–3 Oct"
    if s == e:
        return f"{s.day} {s:%b}"
    return f"{s.day}–{e.day} {e:%b}" if s.month == e.month else f"{s.day} {s:%b}–{e.day} {e:%b}"


def build(match=None):
    """{"weeks": [...], "mom": {with, without}} for the page's waterfall, or None if Odoo is unreachable."""
    try:
        from lib import db, shop_regions
    except Exception:
        return None
    if not db.check_connection()[0]:
        return None
    regions = {k.upper(): v for k, v in shop_regions.load().items()}
    m_start, m_end = report_month.live_month_window()
    last_day = min(date.today() - timedelta(days=1), m_end)     # last COMPLETE day
    out = {}

    # weeks — the dashboard weeks (Sun–Sat cut at month ends) of last month and this month, plus the
    # current week so far (to last_day) (user, 29 Oct 2026). The page builds the waterfall between ANY
    # two of them and marks the best weeks. One till query for the whole span, split by day.
    first = (last_day.replace(day=1) - timedelta(days=1)).replace(day=1)   # 1st of last month
    segs, ws = [], _week_start(first)
    while ws <= last_day:
        we, s = ws + timedelta(days=6), ws
        while s <= we and s <= last_day:
            me = (date(s.year + (s.month == 12), s.month % 12 + 1, 1) - timedelta(days=1))
            e = min(we, me)
            if s >= first:
                segs.append((s, min(e, last_day), e > last_day))       # (start, end, current week?)
            s = e + timedelta(days=1)
        ws += timedelta(days=7)
    tills = _till_days(first, last_day, regions, match) if segs else []
    if len(segs) >= 2:
        out["weeks"] = []
        for s, e, cur in segs:
            p = _period_bags(s, e, regions, tills, match)
            wk = {
                "label": f"Wk {_perfect_week_index(s)} {s:%b}" + (" so far" if cur else ""),
                "range": _rng(s, e), "start": s.isoformat(), "days": p["days"],
                "rows": [[reg, shop, round(b), round(k)] for reg, shop, b, k in p["rows"] if round(b) or round(k)],
            }
            if cur:
                wk["current"] = True
            out["weeks"].append(wk)

    # mom — month to date vs the same days last month (or, on the 1st, the full months).
    if last_day >= m_start:
        b_s, b_e = m_start, last_day
        a_s = (m_start - timedelta(days=1)).replace(day=1)
        a_e = a_s.replace(day=min(last_day.day, calendar.monthrange(a_s.year, a_s.month)[1]))
    else:
        b_e = m_start - timedelta(days=1); b_s = b_e.replace(day=1)
        a_e = b_s - timedelta(days=1);     a_s = a_e.replace(day=1)
    inside = first <= a_s and b_e <= last_day                 # the week query already covers both months
    out["mom"] = _views(_period_bags(a_s, a_e, regions, tills if inside else None, match),
                        _period_bags(b_s, b_e, regions, tills if inside else None, match),
                        a_s.strftime("%B"), b_s.strftime("%B"), _rng(a_s, a_e), _rng(b_s, b_e))
    return out


def build_month(year, month, match=None):
    """{"with", "without"} waterfalls of a finished month vs the month before (full months) — for History
    (docs/reporting-history.md). None if Odoo is unreachable."""
    try:
        from lib import db, shop_regions
    except Exception:
        return None
    if not db.check_connection()[0]:
        return None
    regions = {k.upper(): v for k, v in shop_regions.load().items()}
    b_s = date(year, month, 1)
    b_e = date(year, month, calendar.monthrange(year, month)[1])
    a_e = b_s - timedelta(days=1)
    a_s = a_e.replace(day=1)
    tills = _till_days(a_s, b_e, regions, match)
    return _views(_period_bags(a_s, a_e, regions, tills, match), _period_bags(b_s, b_e, regions, tills, match),
                  a_s.strftime("%B"), b_s.strftime("%B"), _rng(a_s, a_e), _rng(b_s, b_e))
