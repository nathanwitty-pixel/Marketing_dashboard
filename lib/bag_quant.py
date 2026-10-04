"""lib/bag_quant.py — quant signals per bag: drift, volatility, Sharpe-style reliability, trend z, market beta,
run-out risk and safe stock (spec: docs/bag-signals.md). Pure maths in `signals()`; Odoo loaders below."""
import collections
import datetime
import math
import re

DAYS = 91
RECENT = 28
HORIZON = 14
Z95 = 1.645
MIN_SALES = 10


def _phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _sd(xs):
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def action(s):
    """The first rule that fits (docs/bag-signals.md › Action)."""
    if s["runOut"] is not None and s["runOut"] >= 0.5:
        return "Restock first"
    if s["trendZ"] is not None and s["trendZ"] <= -2:
        return "Falling — act"
    if s["reliability"] >= 1 and (s["cover"] is None or s["cover"] >= 21):
        return "Post more"
    if s["cover"] is not None and s["cover"] >= 90:
        return "Clear stock"
    if s["trendZ"] is not None and s["trendZ"] >= 2:
        return "Rising — feed it"
    return "Hold"


def signals(daily, total, stock, start_day=None, horizon=HORIZON, recent=RECENT):
    """Pure. daily = {bag: [units per day, oldest first]} over the window (None = not launched yet);
    total = [all bags' units per day]; stock = {bag: on hand}. Returns {bag: signal dict}."""
    n = len(total)
    tm = _mean(total)
    tvar = sum((t - tm) ** 2 for t in total) / (n - 1) if n > 1 else 0
    out = {}
    for b, series in daily.items():
        idx = [i for i, v in enumerate(series) if v is not None]
        xs = [series[i] for i in idx]
        sold = sum(xs)
        if not xs or sold < MIN_SALES:
            out[b] = {"sold": round(sold), "tooFew": True, "stock": round(stock.get(b, 0))}
            continue
        mu, sd = _mean(xs), _sd(xs)
        cut = n - recent
        rec = [series[i] for i in idx if i >= cut]
        old = [series[i] for i in idx if i < cut]
        trend = None
        if len(rec) >= 7 and len(old) >= 14 and sd > 0:
            trend = (_mean(rec) - _mean(old)) / (sd * math.sqrt(1 / len(rec) + 1 / len(old)))
        tt = [total[i] for i in idx]
        tmm = _mean(tt)
        cov = sum((x - mu) * (t - tmm) for x, t in zip(xs, tt)) / (len(xs) - 1) if len(xs) > 1 else 0
        var_t = sum((t - tmm) ** 2 for t in tt) / (len(tt) - 1) if len(tt) > 1 else 0
        share = mu / tmm if tmm else 0
        beta = (cov / var_t) / share if var_t and share else None     # 1 = moves in proportion to its share
        st = stock.get(b, 0)
        dem, dsd = horizon * mu, sd * math.sqrt(horizon)
        run_out = (1 - _phi((st - dem) / dsd)) if dsd > 0 else (1.0 if st < dem else 0.0)
        safe = dem + Z95 * dsd
        s = {"sold": round(sold), "days": len(xs), "avg": round(mu, 2), "swing": round(sd, 2),
             "reliability": round(mu / sd, 2) if sd else 0, "trendZ": round(trend, 1) if trend is not None else None,
             "recentAvg": round(_mean(rec), 2) if rec else None, "beta": round(beta, 2) if beta is not None else None,
             "stock": round(st), "cover": round(st / mu) if mu else None, "runOut": round(run_out, 3),
             "safeStock": round(safe), "restock": max(round(safe - st), 0), "tooFew": False}
        s["action"] = action(s)
        out[b] = s
    return out


def posting_beta(history, bag, min_weeks=6):
    """Slope of weekly sales on weekly posts for a bag from bag_posts_history.json rows
    [{week, bags: {BAG: {posts, sold}}}], or None until min_weeks weeks with data."""
    pts = [(w["bags"][bag]["posts"], w["bags"][bag]["sold"]) for w in history if bag in w.get("bags", {})]
    if len(pts) < min_weeks:
        return None
    px = [p for p, _ in pts]
    if _sd(px) == 0:
        return None
    mx, my = _mean(px), _mean([s for _, s in pts])
    return round(sum((p - mx) * (s - my) for p, s in pts) / sum((p - mx) ** 2 for p in px), 2)


# ── Odoo loaders ─────────────────────────────────────────────────────────

DAILY_SQL = """
SELECT pt."name" AS product, p.date_order::date AS d, SUM(pl.qty) AS q
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0
  AND COALESCE(pt."name", '') NOT LIKE '%+%' AND COALESCE(pt."name", '') NOT ILIKE '%delivery%'
  AND COALESCE(pt."name", '') NOT ILIKE '%customization%' AND COALESCE(pt."name", '') NOT ILIKE '%strap%'
  AND COALESCE(pt."name", '') NOT ILIKE '%KES discount%' AND COALESCE(pt."name", '') NOT ILIKE '%sample%'
  AND COALESCE(pt."name", '') NOT ILIKE '%gift bag%'
  AND COALESCE(pcat."name", '') NOT ILIKE '%Pos%' AND lower(COALESCE(pt."name", '')) <> ALL(:excluded)
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
GROUP BY 1, 2
"""


def load(end=None, days=DAYS):
    """(daily, total, stock, launch, start, end) for Kenya from Odoo; daily per bag with None before launch."""
    from lib import db, queries, stock as lstock, product_targets
    end = end or (datetime.date.today() - datetime.timedelta(days=1))      # last complete day
    start = end - datetime.timedelta(days=days - 1)
    key = product_targets.bag_key_fn()
    df = db.run_query(DAILY_SQL, {"s": start.isoformat(), "e": end.isoformat(), "excluded": queries.excluded_products()})
    by = collections.defaultdict(collections.Counter)
    for r in (df.itertuples() if df is not None else []):
        k = key(r.product)
        if k:
            d = r.d if isinstance(r.d, datetime.date) else datetime.date.fromisoformat(str(r.d)[:10])
            by[k][(d - start).days] += float(r.q)
    launch = {}
    fs = db.run_query(product_targets.FIRST_SALE_SQL)
    for r in (fs.itertuples() if fs is not None else []):
        k = key(r.product)
        d = r.first_sale if isinstance(r.first_sale, datetime.date) else datetime.date.fromisoformat(str(r.first_sale)[:10])
        if k and (k not in launch or d < launch[k]):
            launch[k] = d
    daily = {}
    for b, c in by.items():
        first = max(((launch.get(b) or start) - start).days, 0)
        daily[b] = [None if i < first else c.get(i, 0.0) for i in range(days)]
    total = [sum(c.get(i, 0.0) for c in by.values()) for i in range(days)]
    stock = collections.Counter()
    for name, q in (lstock.odoo_stock_by_product("kenya") or {}).items():
        k = key(name)
        if k:
            stock[k] += q
    return daily, total, dict(stock), launch, start, end


def bag_posts(rows_month, rows_week, key):
    """{BAG: (posts this month, posts last week)} — Kenya posts (col E) from the two MARKETING_POST tabs."""
    def tally(rows):
        out = collections.Counter()
        for r in (rows or [])[1:]:          # col C product name · col D bag type · col E Kenya posts (as New Products)
            if len(r) < 5:
                continue
            name, bag_type = str(r[2]).strip(), str(r[3]).strip()
            if not name or not bag_type or bag_type.upper() in ("SUM TOTAL", "TOTAL", "GRAND TOTAL"):
                continue
            k = key(name) or key(bag_type)
            try:
                v = float(str(r[4]).replace(",", "") or 0)
            except ValueError:
                v = 0
            if k and v:
                out[k] += v
        return out
    m, w = tally(rows_month), tally(rows_week)
    return {b: (int(m.get(b, 0)), int(w.get(b, 0))) for b in set(m) | set(w)}
