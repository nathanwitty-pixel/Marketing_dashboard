"""lib/push_rules.py — the Push Planner's pure logic (spec: docs/push-planner.md).

No Odoo, no files: push_planner.py loads the data and calls these, and tests/test_push_planner.py
tests them on small made-up inputs.

  facts()      one bag × market: stock, sales pace, days of stock, momentum, posting, offer, price
  add_peers()  each bag's category peers in the same market (median pace and price of bags that sell)
"""
from __future__ import annotations

import datetime
import statistics


def _days_back(end, n):
    end = end if isinstance(end, datetime.date) else datetime.date.fromisoformat(str(end))
    return [(end - datetime.timedelta(days=i)).isoformat() for i in range(n)]


def facts(bag, market, daily, stock, end, posting=None, on_offer=False, is_new=False, price=None,
          category="", window=28):
    """The facts for one bag in one market.

    daily   {iso date: units} over the last `window` days ending `end` (missing days = 0)
    posting the bag's row from push_planner.load_pages (postsMonth, postsLastWeek, yieldPct, clearPct…)
    daysCover is None when the bag sold nothing in the window (stock never runs out at this pace).
    """
    days = _days_back(end, window)
    sold7 = sum(int(daily.get(d, 0)) for d in days[:7])
    prev7 = sum(int(daily.get(d, 0)) for d in days[7:14])
    sold28 = sum(int(daily.get(d, 0)) for d in days)
    per_day = sold28 / float(window)
    stock = max(0, int(stock or 0))
    cover = round(stock / per_day, 1) if per_day > 0 else None
    if prev7 > 0:
        momentum = round(100.0 * (sold7 - prev7) / prev7, 1)
    else:
        momentum = None if sold7 == 0 else 100.0          # from nothing to something
    sold_days = [i for i, d in enumerate(days) if int(daily.get(d, 0)) > 0]
    p = posting or {}
    return {
        "bag": bag, "market": market, "category": category or "", "price": price,
        "stock": stock, "sold7": sold7, "soldPrev7": prev7, "sold28": sold28,
        "perDay": round(per_day, 2), "daysCover": cover, "momentum": momentum,
        "postsMonth": int(p.get("postsMonth") or 0), "postsLastWeek": int(p.get("postsLastWeek") or 0),
        "yieldPct": p.get("yieldPct"), "clearPct": p.get("clearPct"),
        "soldMonth": p.get("soldMonth"), "available": p.get("available"),
        "onOffer": bool(on_offer), "isNew": bool(is_new),
        "firstSoldDaysAgo": max(sold_days) if sold_days else None,   # within the window
    }


def add_peers(rows):
    """Adds peerPerDay / peerPrice / peerCount to every row: the median pace and price of the OTHER
    bags in the same market + category that sold at least one unit in the window. None when a bag
    has no selling peers (or no category)."""
    groups = {}
    for r in rows:
        if r.get("category") and r["sold28"] > 0:
            groups.setdefault((r["market"], r["category"]), []).append(r)
    for r in rows:
        peers = [x for x in groups.get((r["market"], r.get("category")), []) if x["bag"] != r["bag"]]
        r["peerCount"] = len(peers)
        r["peerPerDay"] = round(statistics.median(x["perDay"] for x in peers), 2) if peers else None
        prices = [x["price"] for x in peers if x.get("price")]
        r["peerPrice"] = round(statistics.median(prices)) if prices else None
    return rows


# ── Actions ──────────────────────────────────────────────────
# Per-market "high stock" floors — the same knobs as Dead Stock Accountability (dead_stock_thresholds.txt).
STOCK_FLOOR = {"kenya": 20, "sinza": 5, "uganda": 5}
ACTIONS = ("RESTOCK", "STOP_POSTS", "PUT_ON_OFFER", "POST_MORE", "MOVE_STOCK", "WATCH")
LABEL = {"RESTOCK": "Restock", "STOP_POSTS": "Stop posting", "PUT_ON_OFFER": "Put on an offer",
         "POST_MORE": "Post more", "MOVE_STOCK": "Move stock", "WATCH": "Watch"}
MARKET = {"kenya": "Kenya", "sinza": "Sinza", "uganda": "Uganda"}


def _n(v):
    return f"{int(round(v)):,}"


def _times(n):
    return "once" if n == 1 else f"{n} times"


def _kind(cat):
    """'HANDBAG' → 'handbags', 'SCHOOL BAG' → 'school bags', 'SPORT' → 'sport bags', '' → 'bags'."""
    c = (cat or "").strip().lower()
    if not c:
        return "bags"
    return c + "s" if c.endswith(("bag", "pack", "case")) else c + " bags"


def _cover_txt(c):
    return "never runs out at this pace" if c is None else f"{c:g} days of stock"


def posting_median(rows):
    """{market: median postsMonth of the bags that were posted at all} — the 'below median' line for Post more."""
    out = {}
    for mk in MARKET:
        xs = [r["postsMonth"] for r in rows if r["market"] == mk and r["postsMonth"] > 0]
        out[mk] = statistics.median(xs) if xs else 0
    return out


def action(f, floors=None, post_median=0):
    """(code, plain sentence, units at stake, confidence 0..1) for one bag × market. First rule that fits wins."""
    floors = floors or STOCK_FLOOR
    floor = floors.get(f["market"], 20)
    cover, pd, stock = f["daysCover"], f["perDay"], f["stock"]
    sold_month = f.get("soldMonth")
    y = f.get("yieldPct")

    # 1. Selling out: a fast seller with under a week of stock left.
    if pd >= 2 and cover is not None and cover < 7:
        extra = " Pause its posts until stock lands." if f["postsLastWeek"] else ""
        conf = 0.9 if (f["momentum"] or 0) >= 0 else 0.7
        return ("RESTOCK", f"Sells {pd:g} a day and has {cover:g} days of stock left ({_n(stock)} units).{extra}",
                pd * 7, conf)
    # 2. Posts that sell nothing.
    if f["postsMonth"] >= 10 and sold_month == 0:
        return ("STOP_POSTS", f"Posted {f['postsMonth']} times this month and sold 0 — move those posts to bags that convert.",
                max(1.0, f["postsMonth"] * 0.25), 0.8)
    # 3. Stuck stock, not on offer.
    clear = f.get("clearPct")
    if (not f["onOffer"] and stock > floor and (cover is None or cover >= 45)
            and (clear is None or clear < 30)):
        signals = sum([cover is None or cover >= 90, clear is not None and clear < 10,
                       f["postsMonth"] >= 5 and (y or 0) < 30])
        sold_txt = f"sold {f['sold28']} in 28 days" if f["sold28"] else "sold nothing in 28 days"
        return ("PUT_ON_OFFER", f"{_n(stock)} in stock, {sold_txt} — {_cover_txt(cover)}. Try it as a Deal of the Week.",
                stock * 0.25, 0.5 + 0.15 * signals)
    # 4. Posts work for it and there is stock to sell.
    if (y is not None and y >= 50 and stock > floor and cover is not None and cover >= 14
            and f["postsMonth"] < max(post_median, 1)):
        return ("POST_MORE", f"Posts turn into sales ({y:g}% of expected) but it was posted only {_times(f['postsMonth'])} "
                             f"(typical: {post_median:g}). {cover:g} days of stock — post it daily this week.",
                pd * 7 * 0.5, 0.75)
    return ("WATCH", "", 0.0, 0.0)


def moves(shop_stock, shop_sales, days=14, min_from=5, max_to_cover=7):
    """Kenya shop → shop moves: a shop holding ≥ min_from of a bag that sold 0 there in `days`, while
    another shop sells it and has under `max_to_cover` days left. Sends enough for two weeks at the
    receiving shop's pace (never more than the sender has). Returns a list of dicts, biggest first."""
    out = []
    bags = {b for s in shop_stock.values() for b in s}
    for b in bags:
        donors = [(s, shop_stock[s].get(b, 0)) for s in shop_stock
                  if shop_stock[s].get(b, 0) >= min_from and shop_sales.get(s, {}).get(b, 0) == 0]
        takers = []
        for s, sales in shop_sales.items():
            sold = sales.get(b, 0)
            if sold <= 0 or s in ("WEBSITE", "STAFF POS"):
                continue
            pd = sold / float(days)
            have = shop_stock.get(s, {}).get(b, 0)
            if have / pd < max_to_cover:
                takers.append((s, pd, have, max(1, int(round(pd * 14 - have)))))
        donors.sort(key=lambda d: -d[1])
        takers.sort(key=lambda t: -t[1])
        for to, pd, have, need in takers:
            for i, (frm, avail) in enumerate(donors):
                if avail <= 0 or need <= 0:
                    continue
                q = min(avail, need)
                out.append({"bag": b, "from": frm, "to": to, "qty": q, "toPerDay": round(pd, 2), "toStock": have,
                            "says": f"Move {q} from {frm.title()} (sold 0 in {days} days) to {to.title()} "
                                    f"(sells {pd:.1f} a day, {have} left)."})
                donors[i] = (frm, avail - q)
                need -= q
    out.sort(key=lambda m: -m["qty"] * m["toPerDay"])
    return out


def urgency(days_elapsed, days_in_month, pace_gap=0.0):
    """More weight as the month runs out and when the market is behind its pace (gap 0..1)."""
    frac = days_elapsed / float(max(1, days_in_month))
    return round((1.0 + frac) * (1.0 + max(0.0, min(1.0, pace_gap))), 3)


def score(units, price, urg, conf):
    """Value at stake (units × price) × urgency × confidence. Price missing → KES 2,500 (a typical bag)."""
    return round(units * (price or 2500) * urg * conf)


def rank(rows, n=15, per_action=5):
    """Top `n` by score, at most `per_action` of any one action, so one kind never fills the list."""
    out, used = [], {}
    for r in sorted((r for r in rows if r["action"] != "WATCH" and r["score"] > 0), key=lambda r: -r["score"]):
        if used.get(r["action"], 0) >= per_action:
            continue
        used[r["action"]] = used.get(r["action"], 0) + 1
        out.append(r)
        if len(out) >= n:
            break
    return out


# ── Why it isn't moving ──────────────────────────────────────
REASONS = ("NOT_POSTED", "POSTED_NOT_CONVERTING", "PRICE_ABOVE_PEERS", "WRONG_SHOPS", "OFFER_SHADOW",
           "NEW_UNTESTED", "MARKET_FIT", "SLOWING", "SLOW_SELLER", "OVERSTOCKED")
REASON_LABEL = {"NOT_POSTED": "Not posted", "POSTED_NOT_CONVERTING": "Posts not converting",
                "PRICE_ABOVE_PEERS": "Priced above similar bags", "WRONG_SHOPS": "Stock in the wrong shops",
                "OFFER_SHADOW": "Similar bags on offer", "NEW_UNTESTED": "New — too early",
                "MARKET_FIT": "May not suit this market", "SLOWING": "Slowing down",
                "SLOW_SELLER": "Slow seller", "OVERSTOCKED": "More stock than it sells"}


def not_moving(f, floors=None):
    """A bag with stock that isn't clearing: cleared < 30% this month, or > 45 days of stock (or no sales)."""
    floor = (floors or STOCK_FLOOR).get(f["market"], 20)
    if f["stock"] <= max(2, floor // 4):
        return False
    clear = f.get("clearPct")
    return (clear is not None and clear < 30) or f["daysCover"] is None or f["daysCover"] > 45


def context(rows, shop_stock=None, shop_sales=None):
    """What the reasons need beyond one row: Kenya pace per bag, the on-offer sellers per market +
    category, and (Kenya) the share of each bag's shop stock sitting in shops that sold none of it."""
    kenya_pd = {r["bag"]: r["perDay"] for r in rows if r["market"] == "kenya"}
    offered = {}
    for r in rows:
        if r["onOffer"] and r.get("category") and r["perDay"] > 0:
            offered.setdefault((r["market"], r["category"]), []).append(r)
    dead_share = {}
    for s, items in (shop_stock or {}).items():
        for b, q in items.items():
            tot, dead = dead_share.get(b, (0, 0))
            sold = (shop_sales or {}).get(s, {}).get(b, 0)
            dead_share[b] = (tot + q, dead + (q if sold == 0 else 0))
    return {"kenyaPerDay": kenya_pd, "offered": offered,
            "deadShare": {b: (d / t if t else 0.0, d, t) for b, (t, d) in dead_share.items()}}


def reasons(f, ctx):
    """Every reason that applies to a not-moving bag, each {code, label, text} with its numbers."""
    out = []

    def add(code, text):
        out.append({"code": code, "label": REASON_LABEL[code], "text": text})

    mk, here = f["market"], MARKET.get(f["market"], f["market"])
    posts, y = f["postsMonth"], f.get("yieldPct")
    if posts == 0:
        add("NOT_POSTED", "Nobody has seen it — 0 posts this month.")
    elif posts >= 5 and (y is None or y < 30):
        got = "none" if not y else f"only {y:g}%"
        add("POSTED_NOT_CONVERTING", f"Posted {_times(posts)} this month, but sales reached {got} of what those posts "
                                     "should bring — the posts aren't selling it (price, photo or the bag itself).")
    if f.get("price") and f.get("peerPrice") and f["price"] >= 1.25 * f["peerPrice"]:
        add("PRICE_ABOVE_PEERS", f"KES {_n(f['price'])} vs KES {_n(f['peerPrice'])} for the "
                                 f"{_kind(f.get('category'))} that do sell in {here}.")
    if mk == "kenya":
        share, dead, tot = ctx.get("deadShare", {}).get(f["bag"], (0.0, 0, 0))
        if tot >= 10 and share >= 0.6:
            add("WRONG_SHOPS", f"{round(100 * share)}% of its shop stock ({_n(dead)} of {_n(tot)}) sits in shops "
                               "that sold none of it in 14 days.")
    if not f["onOffer"] and f.get("category"):
        rivals = [r for r in ctx.get("offered", {}).get((mk, f["category"]), [])
                  if r["bag"] != f["bag"] and r["perDay"] >= max(0.5, 2 * f["perDay"])]
        if len(rivals) >= 1:
            names = ", ".join(r["bag"].title() for r in sorted(rivals, key=lambda r: -r["perDay"])[:2])
            add("OFFER_SHADOW", f"Similar {_kind(f['category'])} on offer ({names}) are taking the buyers.")
    if f.get("isNew") and (f.get("firstSoldDaysAgo") is None or f["firstSoldDaysAgo"] < 14):
        when = "hasn't sold yet" if f.get("firstSoldDaysAgo") is None else f"first sold {f['firstSoldDaysAgo']} days ago"
        add("NEW_UNTESTED", f"New — {when}, too early to judge.")
    if mk != "kenya":
        kpd = ctx.get("kenyaPerDay", {}).get(f["bag"], 0)
        if kpd >= 1 and f["sold28"] <= 1:
            add("MARKET_FIT", f"Sells {kpd:g} a day in Kenya but {f['sold28']} in 28 days in {here} — "
                              "may not suit this market.")
    if f["soldPrev7"] >= 5 and f["momentum"] is not None and f["momentum"] <= -40:
        add("SLOWING", f"Sold {f['sold7']} this week vs {f['soldPrev7']} the week before ({f['momentum']:g}%).")
    # Nothing above fits: say plainly whether it sells slowly for its kind, or just holds too much stock.
    if not out:
        cover = "it hasn't sold in 28 days" if f["daysCover"] is None else f"{f['daysCover']:g} days of stock"
        peer = f.get("peerPerDay")
        if peer and f["perDay"] < 0.5 * peer:
            add("SLOW_SELLER", f"Sells {f['perDay']:g} a day vs {peer:g} for similar bags in {here} — {cover}.")
        else:
            add("OVERSTOCKED", f"Sells about as well as similar bags here ({f['perDay']:g} a day), but {_n(f['stock'])} "
                               f"in stock is {cover} — more than {here} moves in a month.")
    return out


# ── Did last week's calls work? ──────────────────────────────
def week_start(d):
    """Sunday on/before `d` — the dashboard's Sun–Sat weeks."""
    d = d if isinstance(d, datetime.date) else datetime.date.fromisoformat(str(d))
    return d - datetime.timedelta(days=(d.weekday() + 1) % 7)


def record_week(history, wk, top):
    """Store this week's top actions under its Sunday. Re-running in the same week REPLACES that week
    (never duplicates). Keeps the last 12 weeks."""
    wk = str(wk)
    history = dict(history or {})
    history[wk] = [{"bag": r["bag"], "market": r["market"], "action": r["action"], "says": r.get("says", ""),
                    "perDayBefore": r.get("perDay"), "stockBefore": r.get("stock"),
                    "move": r.get("move")} for r in top]
    for old in sorted(history)[:-12]:
        del history[old]
    return history


def followup(history, daily, stock, today):
    """The most recent PREVIOUS week's calls and what happened since: sold/day since that week began vs
    before. RESTOCK is judged on stock going up; STOP_POSTS and MOVE_STOCK can't be judged from sales.
    daily = {market: {bag: {iso: units}}}, stock = {market: {bag: units}}. Returns (week, rows)."""
    cur = str(week_start(today))
    past = sorted(w for w in (history or {}) if w < cur)
    if not past:
        return None, []
    wk = past[-1]
    start = datetime.date.fromisoformat(wk)
    today = today if isinstance(today, datetime.date) else datetime.date.fromisoformat(str(today))
    ndays = max(1, (today - start).days)               # full days since the week began (today excluded)
    out = []
    for p in history[wk]:
        dl = (daily.get(p["market"]) or {}).get(p["bag"], {})
        sold = sum(int(u) for d, u in dl.items() if wk <= d < today.isoformat())
        after = round(sold / ndays, 2)
        before = p.get("perDayBefore") or 0
        now_stock = (stock.get(p["market"]) or {}).get(p["bag"], 0)
        if p["action"] == "RESTOCK":
            ok = now_stock > (p.get("stockBefore") or 0)
            res = "✓ restocked" if ok else "✗ not restocked yet"
        elif p["action"] in ("STOP_POSTS", "MOVE_STOCK"):
            ok, res = None, "check by hand"
        else:                                             # PUT_ON_OFFER / POST_MORE should lift sales
            ok = after >= max(before * 1.15, before + 0.1)
            res = "✓ selling faster" if ok else ("= about the same" if after >= before * 0.85 else "✗ slower")
        out.append({**p, "perDayAfter": after, "stockNow": now_stock, "worked": ok, "result": res, "days": ndays})
    return wk, out
