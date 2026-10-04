"""share_targets.py — split a period's total target across products by recent sales share, scaling new and
out-of-stock products to the days they were actually available (skill: sales-share-targets). Pure Python.

    avail = available_days(onhand_now, net_moves, sold_days, start, end, today)   # optional
    rows  = allocate(sold, launch, total, start, end, months, avail=avail)
"""
import datetime
import math

MIN_DAYS = 14   # a product a few days old isn't judged on fewer days than this


def available_days(onhand_now, net_moves, sold_days, start, end, today):
    """Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.
    onhand_now = {bag: units now}; net_moves = {bag: {date: net into shops}}; sold_days = {bag: set(dates)}.
    End-of-day stock is rebuilt backwards from today: end(d-1) = end(d) - net(d)."""
    out = {}
    for b in set(onhand_now) | set(net_moves) | set(sold_days):
        moves = net_moves.get(b, {})
        level = onhand_now.get(b, 0)               # end of `today`
        d = today
        days = set()
        while d >= start:
            prev = level - moves.get(d, 0)          # end of the day before = start of d
            if d <= end and (level > 0 or prev > 0 or d in sold_days.get(b, ())):
                days.add(d)
            level, d = prev, d - datetime.timedelta(days=1)
        out[b] = days
    return out


def allocate(sold, launch, total, start, end, months, min_days=MIN_DAYS, avail=None):
    """Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale}, avail = {bag: set(dates
    with stock)} (optional). Returns rows sorted by target: {bag, launch, days, months{}, sold, equiv, share,
    target} — no row with target 0."""
    period_days = (end - start).days + 1
    eq = {}
    meta = {}
    for b, by_m in sold.items():
        units = sum(by_m.values())
        if units <= 0:
            continue
        first = max(launch.get(b) or start, start)
        if avail is not None and b in avail:
            raw_days = sum(1 for d in avail[b] if d >= first)      # stocked days since launch
        else:
            raw_days = (end - first).days + 1
        days = min(max(raw_days, min_days), period_days)
        eq[b] = units / days * period_days
        meta[b] = (first if (launch.get(b) or start) > start else None, days, units, raw_days)
    s = sum(eq.values())
    if not s:
        return []
    raw = {b: total * v / s for b, v in eq.items()}
    tgt = {b: math.floor(v) for b, v in raw.items()}
    for b in sorted(raw, key=lambda b: -(raw[b] - tgt[b]))[:total - sum(tgt.values())]:
        tgt[b] += 1
    rows = [{"bag": b, "launch": meta[b][0], "days": meta[b][1], "rawDays": meta[b][3], "months": {m: int(round(sold[b].get(m, 0))) for m in months},
             "sold": int(round(meta[b][2])), "equiv": round(eq[b]), "share": round(eq[b] / s * 100, 2), "target": tgt[b]}
            for b in eq if tgt[b] > 0]
    return sorted(rows, key=lambda r: (-r["target"], r["bag"]))
