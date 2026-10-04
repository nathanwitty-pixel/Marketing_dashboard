"""bag_signals.py — quant signals per product from daily sales + stock (skill: bag-signals).

Pure Python, no dependencies. Feed it your own data:
    daily = {product: [units sold per day, oldest first; None for days before launch]}
    total = [all products' units per day]           (same length)
    stock = {product: units on hand now}
    signals(daily, total, stock) -> {product: {...}}
"""
import math

DAYS = 91          # look-back window (13 weeks)
RECENT = 28        # "recent" part of the window for the trend test
HORIZON = 14       # days ahead for run-out risk and safe stock
Z95 = 1.645        # one-sided 95 % service level
MIN_SALES = 10     # fewer sales than this in the window = too little to judge


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
