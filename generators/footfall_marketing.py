"""
footfall_marketing.py — Footfall and Marketing page (spec: docs/footfall-marketing.md).

Shop by shop and week by week: visitors counted at the door (denri_footfall_count), walk-in buyers on the
POS, paid-ad WhatsApp leads, and the shop's market posts and ad spend — do posting and ads bring people in,
and do the shops turn them into buyers?

Writes data/footfall_marketing.json and the FOOT_DATA block in html/footfall_marketing.html.

    python generators/footfall_marketing.py
"""
import datetime as dt
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root → lib/
from lib import paths, footfall, ads

WEEKS = 16                     # complete Sun–Sat weeks shown
MIN_DAYS = 5                   # a shop-week with fewer counted days is 'partly counted'
MKT_LABEL = {"KENYA": "Kenya", "SINZA": "Tanzania", "UGANDA": "Uganda"}


def wk_label(s):
    e = s + dt.timedelta(days=6)
    return (f"{s.day}–{e.day} {e.strftime('%b')}" if s.month == e.month
            else f"{s.day} {s.strftime('%b')}–{e.day} {e.strftime('%b')}")


def num(v, nd=None):
    """JSON-safe number: NaN / None → None."""
    if v is None:
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or math.isinf(f):
        return None
    return round(f, nd) if nd is not None else (int(f) if f == int(f) else f)


def pearson(xs, ys):
    pts = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    n = len(pts)
    if n < 6:
        return None, n
    mx = sum(x for x, _ in pts) / n
    my = sum(y for _, y in pts) / n
    vx = sum((x - mx) ** 2 for x, _ in pts)
    vy = sum((y - my) ** 2 for _, y in pts)
    if not vx or not vy:
        return None, n
    return sum((x - mx) * (y - my) for x, y in pts) / math.sqrt(vx * vy), n


def strength(r):
    if r is None:
        return "not enough weeks to tell"
    a = abs(r)
    word = "no link" if a < 0.1 else "a weak" if a < 0.3 else "a moderate" if a < 0.5 else "a strong"
    if word == "no link":
        return "no link"
    return f"{word} {'positive' if r > 0 else 'negative'} link"


def build():
    today = dt.date.today()
    last_end = today - dt.timedelta(days=(today.weekday() + 2) % 7 or 7)       # the last complete Saturday
    if last_end >= today:
        last_end -= dt.timedelta(days=7)
    first = footfall.week_start(last_end) - dt.timedelta(days=7 * (WEEKS - 1))
    weeks = [first + dt.timedelta(days=7 * i) for i in range(WEEKS)]
    W = footfall.weekly(first, last_end)
    if W is None or W.empty:
        print("Footfall: no data (Odoo unreachable?) — nothing written.")
        return None
    WA = footfall.whatsapp_weekly(first, last_end)
    wa = {(r.shop, r.week): r for r in WA.itertuples()}

    # Market posts per week (one before the window too, for 'last week's posts').
    posts = {m: {} for m in footfall.MARKET.values()}
    try:
        from lib import marketing_posts
        for w in [first - dt.timedelta(days=7)] + weeks:
            p = marketing_posts.posts(w, w + dt.timedelta(days=6))
            for m in posts:
                posts[m][w] = sum(v.get(m, 0) for v in p.values())
    except Exception as e:                                   # noqa: BLE001
        print(f"  Footfall: posts unavailable ({e})")
    rows = ads.campaigns()
    adw = {m: {w: ads.market_week(rows, m, w)["spend"] for w in ads.weeks()} for m in posts}

    # ── per shop per week ──
    shops = []
    for shop in footfall.SHOPS:
        label, market = footfall.SHOPS[shop]
        sw = W[W["shop"] == shop].set_index("week")
        out = []
        for w in weeks:
            r = sw.loc[w] if w in sw.index else None
            v = wa.get((label, w))
            item = {"week": w.isoformat()}
            if r is not None:
                item.update({
                    "visitors": num(r["visitors"]), "orders": num(r["orders"]), "conversion": num(r["conversion"], 1),
                    "rpv": num(r["rev_per_visitor"]), "rpvAll": num(r["rev_per_visitor_all"]),
                    "kes": num(r["kes"], 0), "bulkOrders": num(r["bulk_orders"]), "bulkKes": num(r["bulk_kes"], 0),
                    "bulkUnits": num(r["bulk_units"]), "bulkMaxLine": num(r["bulk_max_line"]),
                    "days": num(r["days"]), "notCountedDays": num(r["not_counted_days"]),
                    "notCountedOrders": num(r["not_counted_orders"]), "lowCount": bool(r["low_count"]),
                    "partial": bool((r["days"] or 0) < MIN_DAYS)})
            if v is not None:
                item.update({"waChats": num(v.ad_chats), "waBought": num(v.ad_bought),
                             "waConv": num(v.ad_bought / v.ad_chats * 100, 1) if v.ad_chats else None,
                             "waReply": num(v.med_reply, 1)})
            item["postsLast"] = posts[market].get(w - dt.timedelta(days=7))
            item["posts"] = posts[market].get(w)
            item["adSpend"] = num(adw[market].get(w), 0)
            out.append(item)
        shops.append({"shop": shop, "label": label, "market": market, "marketLabel": MKT_LABEL[market],
                      "hilton": shop == footfall.HILTON, "weeks": out})

    def agg(items, key):
        return sum(i.get(key) or 0 for i in items)

    def judged(s, i):           # a shop-week that can be judged: fully counted, count not low, not Hilton
        x = s["weeks"][i]
        return (not s["hilton"]) and x.get("visitors") and not x.get("lowCount") and (x.get("days") or 0) >= MIN_DAYS

    # A week is 'partly counted' when its shops counted fewer than 70% of their days (e.g. 6–10 Oct 2026).
    full = []
    for i in range(WEEKS):
        d = sum(s["weeks"][i].get("days") or 0 for s in shops)
        full.append(d >= 0.7 * 7 * len(shops))
    partial_weeks = [{"week": wk_label(weeks[i]), "days": sum(s["weeks"][i].get("days") or 0 for s in shops),
                      "of": 7 * len(shops)} for i in range(WEEKS) if not full[i]]
    last_i = max(i for i in range(WEEKS) if full[i])
    prev_i = max((i for i in range(last_i) if full[i]), default=last_i)

    # ── tiles: last complete week vs the week before (Hilton left out) ──
    def week_tot(i):
        xs = [s["weeks"][i] for s in shops if not s["hilton"] and s["weeks"][i].get("visitors")]
        v, o = agg(xs, "visitors"), agg(xs, "orders")
        k = sum((x.get("kes") or 0) - (x.get("bulkKes") or 0) for x in xs)
        c, b = agg(xs, "waChats"), agg(xs, "waBought")
        return {"visitors": v, "orders": o, "conv": o / v * 100 if v else None, "rpv": k / v if v else None,
                "waConv": b / c * 100 if c else None, "waChats": c}
    T, P = week_tot(last_i), week_tot(prev_i)

    def chg(a, b):
        return None if a is None or not b else round((a / b - 1) * 100, 1)
    tiles = [
        {"k": "Visitors", "v": f"{T['visitors']:,.0f}", "chg": chg(T["visitors"], P["visitors"]), "good": "up",
         "n": f"counted at the door, all shops but Hilton (was {P['visitors']:,.0f} in {wk_label(weeks[prev_i])})"},
        {"k": "Walk-in conversion", "v": f"{T['conv']:.1f}%" if T["conv"] else "", "pts": round(T["conv"] - P["conv"], 1) if T["conv"] and P["conv"] else None,
         "good": "up", "n": f"{T['orders']:,.0f} walk-in buyers ÷ visitors (was {P['conv']:.1f}%)" if P["conv"] else ""},
        {"k": "Revenue per visitor", "v": f"KES {T['rpv']:,.0f}" if T["rpv"] else "", "chg": chg(T["rpv"], P["rpv"]), "good": "up",
         "n": f"walk-in KES ÷ visitors, bulk orders out (was KES {P['rpv']:,.0f})" if P["rpv"] else ""},
        {"k": "WhatsApp ad-lead conversion", "v": f"{T['waConv']:.1f}%" if T["waConv"] else "",
         "pts": round(T["waConv"] - P["waConv"], 1) if T["waConv"] and P["waConv"] else None, "good": "up",
         "n": f"{T['waChats']:,.0f} paid-ad chats (was {P['waConv']:.1f}%)" if P["waConv"] else ""},
    ]

    # ── ranking: last 4 weeks ──
    L4 = range(WEEKS - 4, WEEKS)
    ranking = []
    for s in shops:
        xs = [s["weeks"][i] for i in L4 if s["weeks"][i].get("visitors")]
        v, o = agg(xs, "visitors"), agg(xs, "orders")
        k = sum((x.get("kes") or 0) - (x.get("bulkKes") or 0) for x in xs)
        c, b = agg([s["weeks"][i] for i in L4], "waChats"), agg([s["weeks"][i] for i in L4], "waBought")
        replies = [s["weeks"][i].get("waReply") for i in L4 if s["weeks"][i].get("waReply") is not None]
        low = sum(1 for i in L4 if s["weeks"][i].get("lowCount"))
        bulk = agg([s["weeks"][i] for i in L4], "bulkOrders")
        ranking.append({"shop": s["label"], "market": s["marketLabel"], "visitors": v, "orders": o,
                        "conversion": round(o / v * 100, 1) if v else None, "rpv": round(k / v) if v else None,
                        "waChats": c, "waConv": round(b / c * 100, 1) if c else None,
                        "waReply": round(sorted(replies)[len(replies) // 2], 1) if replies else None,
                        "lowWeeks": low, "bulkOrders": bulk, "hilton": s["hilton"]})
    ranking.sort(key=lambda r: (r["hilton"] or r["lowWeeks"] >= 2, -(r["conversion"] or 0)))

    # ── correlations per market: each shop against its own average ──
    corr = []
    for m in ("KENYA", "SINZA", "UGANDA"):
        ms = [s for s in shops if s["market"] == m and not s["hilton"]]
        pairs = {"postsVisitors": ([], []), "postsOrders": ([], []), "adsVisitors": ([], []), "adsOrders": ([], [])}
        for s in ms:
            ok = [i for i in range(WEEKS) if judged(s, i)]
            if len(ok) < 4:
                continue
            mv = sum(s["weeks"][i]["visitors"] for i in ok) / len(ok)
            mo = sum(s["weeks"][i]["orders"] for i in ok) / len(ok)
            for i in ok:
                x = s["weeks"][i]
                iv, io = x["visitors"] / mv * 100 if mv else None, x["orders"] / mo * 100 if mo else None
                if x.get("postsLast") is not None:
                    pairs["postsVisitors"][0].append(x["postsLast"]); pairs["postsVisitors"][1].append(iv)
                    pairs["postsOrders"][0].append(x["postsLast"]); pairs["postsOrders"][1].append(io)
                if x.get("adSpend") is not None:
                    pairs["adsVisitors"][0].append(x["adSpend"]); pairs["adsVisitors"][1].append(iv)
                    pairs["adsOrders"][0].append(x["adSpend"]); pairs["adsOrders"][1].append(io)
        item = {"market": MKT_LABEL[m], "shops": len(ms)}
        for k, (xs, ys) in pairs.items():
            r, n = pearson(xs, ys)
            nweeks = len(adw[m]) if k.startswith("ads") else WEEKS
            if nweeks < 6:
                r = None
            item[k] = {"r": round(r, 2) if r is not None else None, "n": n, "weeks": nweeks, "words": strength(r)}
        corr.append(item)

    # ── data quality ──
    quality = {"lowCount": [], "notCounted": [], "bulk": [], "hilton": None}
    for s in shops:
        for i, x in enumerate(s["weeks"]):
            wl = wk_label(weeks[i])
            if x.get("lowCount") and not s["hilton"]:
                quality["lowCount"].append({"shop": s["label"], "week": wl, "visitors": x["visitors"],
                                            "orders": x["orders"], "conversion": x["conversion"]})
            if x.get("notCountedDays"):
                quality["notCounted"].append({"shop": s["label"], "week": wl, "days": x["notCountedDays"],
                                              "orders": x["notCountedOrders"]})
            if x.get("bulkOrders"):
                quality["bulk"].append({"shop": s["label"], "week": wl, "orders": x["bulkOrders"], "kes": x["bulkKes"],
                                        "units": x["bulkUnits"], "maxLine": x["bulkMaxLine"],
                                        "rpvAll": x["rpvAll"], "rpv": x["rpv"]})
        if s["hilton"]:
            v = sum(x.get("visitors") or 0 for x in s["weeks"]); o = sum(x.get("orders") or 0 for x in s["weeks"])
            quality["hilton"] = {"visitors": v, "orders": o, "conversion": round(o / v * 100, 1) if v else None,
                                 "weeks": WEEKS}

    quality["partialWeeks"] = partial_weeks
    out = {"generated": today.isoformat(), "weeks": [{"start": w.isoformat(), "label": wk_label(w), "full": full[i]}
                                                     for i, w in enumerate(weeks)],
           "lastWeek": wk_label(weeks[last_i]), "prevWeek": wk_label(weeks[prev_i]), "tiles": tiles, "shops": shops, "ranking": ranking,
           "correlations": corr, "quality": quality, "adsWeeks": [w.isoformat() for w in ads.weeks()],
           "actions": actions(shops, weeks, ranking, posts, adw, quality, last_i, prev_i)}

    with open(paths.data("footfall_marketing.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    page = paths.html("footfall_marketing.html")
    if os.path.exists(page):
        with open(page, encoding="utf-8") as f:
            html = f.read()
        block = ("<!-- FOOT_DATA_START -->\n<script>\nconst FOOT = " +
                 json.dumps(out, ensure_ascii=False).replace("</", "<\\/") + ";\n</script>\n<!-- FOOT_DATA_END -->")
        html = re.sub(r"<!-- FOOT_DATA_START -->.*?<!-- FOOT_DATA_END -->", lambda _m: block, html, flags=re.DOTALL)
        with open(page, "w", encoding="utf-8") as f:
            f.write(html)
    print(f"Footfall and Marketing: {len(shops)} shops, {WEEKS} weeks ({wk_label(weeks[0])} to {wk_label(weeks[-1])}), "
          f"{len(out['actions'])} actions.")
    return out


def actions(shops, weeks, ranking, posts, adw, quality, L, P):
    """'What we can do' — by rule (docs/footfall-marketing.md › Actions). Each names a shop or market,
    the numbers and the week."""
    acts = []
    lw = wk_label(weeks[L])
    span = f"{wk_label(weeks[L - 3])} to {wk_label(weeks[L])}"
    fair = [r for r in ranking if not r["hilton"] and r["lowWeeks"] < 2 and r["conversion"] is not None]

    # Fix counting first: one item listing every shop with 2+ low-count weeks in the last 4.
    low = sorted([r for r in ranking if r["lowWeeks"] >= 2 and not r["hilton"]], key=lambda r: -(r["conversion"] or 0))
    if low:
        acts.append({"kind": "watch", "who": ", ".join(r["shop"] for r in low),
                     "text": f"The visitor count looks low at {len(low)} shops ({span}): "
                             + ", ".join(f"{r['shop']} {r['conversion']}% ({r['orders']:,} buyers, {r['visitors']:,} visitors)"
                                         for r in low)
                             + ". Real walk-in conversion is rarely above 80%: fix the counting at the door before "
                               "judging these shops' conversion."})
    # Hilton.
    h = quality.get("hilton")
    if h:
        acts.append({"kind": "watch", "who": "Hilton",
                     "text": f"Hilton: {h['visitors']:,} visitors in {h['weeks']} weeks, far above any other shop. The clicker "
                             f"seems to count mall or event traffic, so its {h['conversion']}% conversion isn't comparable. "
                             f"Count only people who enter the shop."})
    # High traffic, low conversion.
    if len(fair) >= 6:
        vs = sorted(r["visitors"] for r in fair)
        cs = sorted(r["conversion"] for r in fair)
        med_v, low_c = vs[len(vs) // 2], cs[len(cs) // 3]
        for r in fair:
            if r["visitors"] > med_v and r["conversion"] <= low_c:
                acts.append({"kind": "do", "who": r["shop"],
                             "text": f"{r['shop']}: {r['visitors']:,} visitors in the last 4 weeks (above the middle shop's "
                                     f"{med_v:,}) but only {r['conversion']}% bought ({span}). People come in and leave: "
                                     f"check staffing at busy hours and whether the bags they ask for are in stock."})
    # Fast WhatsApp, few walk-ins: only a shop whose walk-ins fell 10+ points more than all shops together.
    def orders_at(i):
        return sum(s["weeks"][i].get("orders") or 0 for s in shops if not s["hilton"])
    all_chg = (orders_at(L) / orders_at(P) - 1) * 100 if orders_at(P) else 0
    wa_conv = sorted(r["waConv"] for r in fair if r["waConv"] is not None)
    med_wa = wa_conv[len(wa_conv) // 2] if wa_conv else None
    for s in shops:
        if s["hilton"]:
            continue
        r = next((x for x in ranking if x["shop"] == s["label"]), None)
        a, b = s["weeks"][L], s["weeks"][P]
        if (r and r["waReply"] is not None and r["waReply"] <= 2 and med_wa is not None and r["waConv"] is not None
                and r["waConv"] > med_wa and a.get("orders") and b.get("orders")
                and (a["orders"] / b["orders"] - 1) * 100 < all_chg - 10):
            acts.append({"kind": "watch", "who": s["label"],
                         "text": f"{s['label']}: WhatsApp replies fast ({r['waReply']} min) and ad leads convert well "
                                 f"({r['waConv']}%), yet walk-in buyers fell from {b['orders']:,} ({wk_label(weeks[P])}) to "
                                 f"{a['orders']:,} ({lw}), {(a['orders'] / b['orders'] - 1) * 100:+.0f}% against "
                                 f"{all_chg:+.0f}% for all shops. The online push isn't bringing people to the door: invite "
                                 f"chats to visit the shop."})
    # Posts / ads didn't lift visitors.
    for m in ("KENYA", "SINZA", "UGANDA"):
        ms = [s for s in shops if s["market"] == m and not s["hilton"]]
        def vis(i):
            return sum(s["weeks"][i].get("visitors") or 0 for s in ms if s["weeks"][i].get("visitors") and not s["weeks"][i].get("lowCount"))
        # posts in the week before each compared week (posts lead visits by about a week)
        p0, p1 = posts[m].get(weeks[P] - dt.timedelta(days=7)), posts[m].get(weeks[L] - dt.timedelta(days=7))
        v1, v2 = vis(P), vis(L)
        if p0 and p1 and v1 and v2:
            if p1 > p0 * 1.1 and v2 < v1:
                acts.append({"kind": "do", "who": MKT_LABEL[m],
                             "text": f"{MKT_LABEL[m]}: posts the week before rose from {p0:,.0f} to {p1:,.0f}, but visitors fell "
                                     f"from {v1:,.0f} ({wk_label(weeks[P])}) to {v2:,.0f} ({lw}). Those posts didn't bring people "
                                     f"in: check which bags and shops they pushed."})
            elif p1 > p0 * 1.1 and v2 >= v1:
                acts.append({"kind": "win", "who": MKT_LABEL[m],
                             "text": f"{MKT_LABEL[m]}: posts the week before rose from {p0:,.0f} to {p1:,.0f}, and visitors went "
                                     f"from {v1:,.0f} ({wk_label(weeks[P])}) to {v2:,.0f} ({lw}). Keep that posting level."})
        a0, a1 = adw[m].get(weeks[P]), adw[m].get(weeks[L])
        if a0 and a1 and v1 and v2 and a1 > a0 * 1.05 and v2 < v1:
            acts.append({"kind": "do", "who": MKT_LABEL[m],
                         "text": f"{MKT_LABEL[m]}: ad spend rose from KES {a0:,.0f} ({wk_label(weeks[P])}) to KES {a1:,.0f} ({lw}) "
                                 f"while visitors fell from {v1:,.0f} to {v2:,.0f}. Rethink where that spend goes."})
        elif a0 and a1 and v1 and v2 and a1 < a0 * 0.95 and v2 >= v1:
            acts.append({"kind": "win", "who": MKT_LABEL[m],
                         "text": f"{MKT_LABEL[m]}: ad spend fell from KES {a0:,.0f} ({wk_label(weeks[P])}) to KES {a1:,.0f} ({lw}) "
                                 f"and visitors still went from {v1:,.0f} to {v2:,.0f}. The cut didn't cost footfall."})
    # Bulk orders.
    for b in quality["bulk"]:
        if b["rpvAll"] and b["rpv"] and b["rpvAll"] > b["rpv"] * 1.25:
            acts.append({"kind": "watch", "who": b["shop"],
                         "text": f"⚠ {b['shop']}, week of {b['week']}: bulk order ({b['orders']:,} {'order' if b['orders'] == 1 else 'orders'} with a line of "
                                 f"{b['maxLine']:,} units, KES {b['kes']:,.0f}) lifts revenue per visitor to KES {b['rpvAll']:,.0f}. "
                                 f"Without the bulk order it is KES {b['rpv']:,.0f}."
                                 + (" A line that size is unusual for a walk-in: check it is a real sale and not a "
                                    "transfer or a typing error." if (b["maxLine"] or 0) >= 100 else "")})
    order = {"watch": 0, "do": 1, "win": 2}
    acts.sort(key=lambda a: order.get(a["kind"], 9))
    return acts


if __name__ == "__main__":
    build()
