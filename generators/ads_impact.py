"""
ads_impact.py — the Ads impact panel shown on every page (spec: docs/ads-impact.md).

Joins marketing's Weekly Ads Performance Report (data/ads_weekly.csv + data/ads_notes.csv, lib/ads.py)
to Odoo sales and marketing posts, week by week and market by market, works out what to do, and writes
data/ads_impact.json — one section per page html. assets/ads_panel.js draws it; streamlit_app.py injects it.

    python generators/ads_impact.py
"""
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root → lib/
from lib import paths, ads

# Which section each page gets: (kind, note tags it shows).
PAGES = {
    "current_performance.html": ("overview", ["all", "corporate"]),
    "monthly_report.html":      ("overview", ["all", "corporate"]),
    "history.html":             ("overview", ["all"]),
    "reject_sales.html":        ("overview", ["all"]),
    "bag_signals.html":         ("posting",  ["all", "new_bags"]),
    "posting_yields.html":      ("posting",  ["all"]),
    "product_performance.html": ("new_bags", ["all", "new_bags"]),
    "new_products.html":        ("new_bags", ["new_bags"]),
    "timed_offers.html":        ("offers",   ["offers"]),
    "bags_on_offer.html":       ("offers",   ["offers"]),
    "offer_picking.html":       ("offers",   ["offers"]),
    "self_made_combos.html":    ("offers",   ["offers", "combos"]),
    "shop_stock_levels.html":   ("shops",    ["shops"]),
    "shops_efficiency.html":    ("shops",    ["shops"]),
    "push_planner.html":        ("shops",    ["shops"]),
    "shop_launch.html":         ("shops",    ["shops"]),
}
MKT_LABEL = {"KENYA": "Kenya", "SINZA": "Tanzania", "UGANDA": "Uganda"}

# Same bag / revenue definition as sql/bag_revenue.sql, per market: bags leave the combo '+' wrapper out,
# revenue keeps it (a combo's price sits on the wrapper).
SALES_SQL = """
SELECT CASE WHEN lower(pc.name) IN ('sinza','dar-es-alam') THEN 'SINZA'
            WHEN lower(pc.name) = 'uganda' THEN 'UGANDA' ELSE 'KENYA' END AS market,
       SUM(CASE WHEN COALESCE(pt.name,'') LIKE '%%+%%' THEN 0 ELSE pl.qty END) AS bags,
       ROUND(SUM(CASE WHEN lower(pc.name) IN ('sinza','dar-es-alam') THEN pl.price_subtotal_incl/25
                      WHEN lower(pc.name)='uganda' THEN pl.price_subtotal_incl/29 ELSE pl.price_subtotal_incl END)) AS kes,
       COUNT(DISTINCT p.id) AS orders
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id LEFT JOIN pos_config pc ON ps.config_id=pc.id
LEFT JOIN product_product pp ON pl.product_id=pp.id LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
LEFT JOIN product_category pcat ON pcat.id=pt.categ_id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done','invoiced','paid') AND pl.qty<>0
  AND COALESCE(pt.name,'') NOT ILIKE '%%delivery%%' AND COALESCE(pt.name,'') NOT ILIKE '%%customization%%'
  AND COALESCE(pt.name,'') NOT ILIKE '%%strap%%' AND COALESCE(pt.name,'') NOT ILIKE '%%sample%%'
  AND COALESCE(pcat.name,'') NOT ILIKE '%%Pos%%' AND lower(COALESCE(pt.name,'')) <> ALL(:x)
GROUP BY 1
""".replace("%%", "%")

BAG_SALES_SQL = """
SELECT pt.name AS product, SUM(pl.qty) AS q
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id LEFT JOIN pos_config pc ON ps.config_id=pc.id
JOIN product_product pp ON pl.product_id=pp.id JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done','invoiced','paid') AND pl.qty<>0
  AND lower(pc.name) NOT IN ('sinza','dar-es-alam','uganda') AND pt.name NOT LIKE '%+%'
GROUP BY 1
"""


# ── helpers ────────────────────────────────────────────────────

def kes(n):
    return ("-" if n < 0 else "") + "KES " + f"{abs(round(n)):,}"

def pct(a, b):
    return (a / b - 1) * 100 if b else None

def spct(p, dp=0):
    return "" if p is None else (f"+{p:.{dp}f}%" if p > 0 else f"{p:.{dp}f}%")

def tone(p, good_up=True):
    if p is None or abs(p) < 0.5:
        return ""
    return "up" if (p > 0) == good_up else "down"

def wk_label(s):
    e = s + dt.timedelta(days=6)
    return (f"{s.day}–{e.day} {e.strftime('%b')}" if s.month == e.month
            else f"{s.day} {s.strftime('%b')}–{e.day} {e.strftime('%b')}")


# ── data ───────────────────────────────────────────────────────

def sales_by_market(weeks):
    """{market: [ {bags, kes, orders} per week ]} from Odoo; None if Postgres is down."""
    try:
        from lib import db, queries
        ok, _ = db.check_connection()
        if not ok:
            return None
        x = queries.excluded_products()
        out = {m: [] for m in ads.MARKETS}
        for s in weeks:
            df = db.run_query(SALES_SQL, {"s": s.isoformat(), "e": (s + dt.timedelta(days=6)).isoformat(), "x": x})
            got = {r.market: {"bags": int(r.bags or 0), "kes": int(r.kes or 0), "orders": int(r.orders or 0)}
                   for r in df.itertuples()} if df is not None else {}
            for m in ads.MARKETS:
                out[m].append(got.get(m, {"bags": 0, "kes": 0, "orders": 0}))
        return out
    except Exception as e:                                   # noqa: BLE001
        print(f"  Ads impact: no Odoo sales ({e})")
        return None


def market_sales(start, end):
    """{market: {bags, kes, orders}} over [start, end]."""
    try:
        from lib import db, queries
        df = db.run_query(SALES_SQL, {"s": start.isoformat(), "e": end.isoformat(), "x": queries.excluded_products()})
        return {r.market: {"bags": int(r.bags or 0), "kes": int(r.kes or 0), "orders": int(r.orders or 0)}
                for r in df.itertuples()} if df is not None else {}
    except Exception:                                        # noqa: BLE001
        return {}


def posts_by_market(weeks):
    """{market: [posts per week]} from marketing's posting sheets; None if they can't be read."""
    try:
        from lib import marketing_posts
        out = {m: [] for m in ads.MARKETS}
        for s in weeks:
            p = marketing_posts.posts(s, s + dt.timedelta(days=6))
            for m in ads.MARKETS:
                out[m].append(sum(v.get(m, 0) for v in p.values()))
        return out
    except Exception as e:                                   # noqa: BLE001
        print(f"  Ads impact: no posts ({e})")
        return None


def posts_lead_sales(weeks):
    """Kenya bag types: change in posts one week vs change in bags sold the next, pooled over the weeks.
    Returns {more: %, fewer: %, nMore, nFewer} or None."""
    try:
        from lib import db, marketing_posts, product_targets
        key = product_targets.bag_key_fn()
        span = [weeks[0] - dt.timedelta(days=7)] + list(weeks)
        sales, posts = [], []
        for s in span:
            e = s + dt.timedelta(days=6)
            df = db.run_query(BAG_SALES_SQL, {"s": s.isoformat(), "e": e.isoformat()})
            d = {}
            for r in df.itertuples():
                b = (key(r.product) or r.product).upper()
                d[b] = d.get(b, 0) + float(r.q)
            sales.append(d)
            p = {}
            for (bt, _c), mk in marketing_posts.posts(s, e).items():
                p[bt.upper()] = p.get(bt.upper(), 0) + mk.get("KENYA", 0)
            posts.append(p)

        def match(pd, b):
            if b in pd:
                return pd[b]
            hits = [v for k, v in pd.items() if k and b.startswith(k + " ")]
            return sum(hits) if hits else None

        grp = {"more": [0, 0, 0], "fewer": [0, 0, 0]}          # bags before, after, n
        for i in range(2, len(span)):
            for b in set(sales[i]) | set(sales[i - 1]):
                s0, s1 = sales[i - 1].get(b, 0), sales[i].get(b, 0)
                if s0 + s1 < 10:
                    continue
                p0, p1 = match(posts[i - 2], b), match(posts[i - 1], b)
                if p0 is None and p1 is None:
                    continue
                p0, p1 = p0 or 0, p1 or 0
                g = "more" if p1 > p0 else "fewer" if p1 < p0 else None
                if g:
                    grp[g][0] += s0; grp[g][1] += s1; grp[g][2] += 1
        if not grp["more"][0] or not grp["fewer"][0]:
            return None
        return {"more": round(pct(grp["more"][1], grp["more"][0]), 1), "nMore": grp["more"][2],
                "fewer": round(pct(grp["fewer"][1], grp["fewer"][0]), 1), "nFewer": grp["fewer"][2]}
    except Exception as e:                                   # noqa: BLE001
        print(f"  Ads impact: posts → sales skipped ({e})")
        return None


def corporate_return(rows):
    """Corporate campaign spend since it started vs corporate bags / KES paid in that time."""
    corp = [r for r in rows if r["focus"] == "corporate"]
    if not corp:
        return None
    start = min(r["week"] for r in corp)
    end = max(r["week"] for r in corp) + dt.timedelta(days=6)
    spend = sum(r["spend_kes"] for r in corp)
    msgs = sum(r["results"] for r in corp)
    try:
        from lib import db, queries
        df = db.run_query(queries.CORPORATE_BAGS, {"start_date": start.isoformat(), "end_date": end.isoformat()})
        bags, got = int(df.iloc[0]["bags"] or 0), float(df.iloc[0]["kes"] or 0)
    except Exception:                                        # noqa: BLE001
        return None
    return {"start": start, "end": end, "spend": spend, "messages": msgs, "bags": bags, "kes": got}


# ── build ──────────────────────────────────────────────────────

def build():
    rows = ads.campaigns()
    weeks = ads.weeks()
    if not rows or not weeks:
        print("Ads impact: no data/ads_weekly.csv rows — nothing written.")
        return None
    last, prev = weeks[-1], (weeks[-2] if len(weeks) > 1 else None)
    L = len(weeks) - 1
    sales = sales_by_market(weeks)
    posts = posts_by_market(weeks)
    week_txt = wk_label(last)

    adw = {m: [ads.market_week(rows, m, w) for w in weeks] for m in ads.MARKETS}

    def tot(i):
        a = {"spend": sum(adw[m][i]["spend"] for m in ads.MARKETS),
             "messages": sum(adw[m][i]["messages"] for m in ads.MARKETS),
             "chat_spend": sum(adw[m][i]["chat_spend"] for m in ads.MARKETS)}
        if sales:
            for k in ("bags", "kes", "orders"):
                a[k] = sum(sales[m][i][k] for m in ads.MARKETS)
        if posts:
            a["posts"] = sum(posts[m][i] for m in ads.MARKETS)
        return a

    T, P = tot(L), (tot(L - 1) if prev else None)
    actions = []   # {kind, text, tags, market}

    # ── overview tiles ──
    def overview_tiles():
        t = [{"k": "Ad spend", "v": "≈" + kes(T["spend"]),
              "n": (spct(pct(T["spend"], P["spend"])) + " week on week" if P else "") + ", all markets and channels",
              "tone": ""},
             {"k": "Messages", "v": f"{round(T['messages']):,}",
              "n": (spct(pct(T["messages"], P["messages"])) + " week on week, " if P else "")
                   + kes(T["chat_spend"] / T["messages"] if T["messages"] else 0) + " each",
              "tone": tone(pct(T["messages"], P["messages"])) if P else ""}]
        if sales and T.get("kes"):
            sh, psh = T["spend"] / T["kes"] * 100, (P["spend"] / P["kes"] * 100 if P and P.get("kes") else None)
            t.append({"k": "Ads as % of revenue", "v": f"{sh:.1f}%",
                      "n": (f"was {psh:.1f}% the week before, " if psh is not None else "") + kes(T["kes"]) + " revenue",
                      "tone": tone((sh - psh) if psh is not None else None, good_up=False)})
            cpb, pcpb = T["spend"] / T["bags"], (P["spend"] / P["bags"] if P and P.get("bags") else None)
            t.append({"k": "Ad cost per bag sold", "v": kes(cpb),
                      "n": (f"was {kes(pcpb)}, " if pcpb is not None else "") + f"{T['bags']:,} bags sold",
                      "tone": tone(pct(cpb, pcpb), good_up=False) if pcpb else ""})
        return t

    # ── market table ──
    def market_table():
        head = ["Market", "Ad spend", "Messages", "KES per message", "Bags", "Orders", "Revenue",
                "Ads % of revenue", "Ad cost per bag", "Messages, week on week", "Orders, week on week"]
        out = []
        for m in ads.MARKETS:
            a, pa = adw[m][L], (adw[m][L - 1] if prev else None)
            row = [MKT_LABEL[m], "≈" + kes(a["spend"]), f"{round(a['messages']):,}",
                   kes(a["chat_spend"] / a["messages"]) if a["messages"] else ""]
            if sales:
                s, ps = sales[m][L], (sales[m][L - 1] if prev else None)
                sh = a["spend"] / s["kes"] * 100 if s["kes"] else None
                row += [f"{s['bags']:,}", f"{s['orders']:,}", kes(s["kes"]),
                        {"t": f"{sh:.1f}%" if sh is not None else "", "c": "down" if sh and sh > 6 else ""},
                        {"t": kes(a["spend"] / s["bags"]) if s["bags"] else "", "c": "down" if s["bags"] and a["spend"] / s["bags"] > 150 else ""}]
                mp, op = (pct(a["messages"], pa["messages"]) if pa else None), (pct(s["orders"], ps["orders"]) if ps else None)
                row += [{"t": spct(mp), "c": tone(mp)}, {"t": spct(op), "c": tone(op)}]
            else:
                row += [""] * 7
            out.append(row)
        return {"title": f"By market, week of {week_txt}", "head": head, "rows": out}

    # ── weekly trend per market (posting pages) ──
    def trend_table():
        head = ["Market", "Week", "Posts", "Ad spend", "Messages", "Bags", "Orders", "Revenue", "Ads % of revenue"]
        out = []
        for m in ads.MARKETS:
            for i, w in enumerate(weeks):
                a = adw[m][i]
                s = sales[m][i] if sales else None
                out.append([MKT_LABEL[m] if i == 0 else "", wk_label(w),
                            f"{posts[m][i]:,.0f}" if posts else "", "≈" + kes(a["spend"]), f"{round(a['messages']):,}",
                            f"{s['bags']:,}" if s else "", f"{s['orders']:,}" if s else "", kes(s["kes"]) if s else "",
                            f"{a['spend'] / s['kes'] * 100:.1f}%" if s and s["kes"] else ""])
        return {"title": "Posts, ads and sales, week by week", "head": head, "rows": out}

    # ── campaign tables ──
    def cpr(r):
        return r["spend"] / r["results"] if r["results"] else None

    def campaign_table(focus, title):
        sel = sorted({(r["market"], r["platform"], r["campaign"]) for r in rows if r["focus"] in focus},
                     key=lambda k: (ads.MARKETS.index(k[0]), k[1], k[2]))
        head = ["Campaign", "Market", "Spend", "Results", "Cost per result", "vs 3-week average"] + [wk_label(w) for w in weeks]
        out = []
        for mk, pf, cp in sel:
            byw = {r["week"]: r for r in rows if (r["market"], r["platform"], r["campaign"]) == (mk, pf, cp)}
            r = byw.get(last)
            if not r:
                continue
            cur = "$" if r["currency"].upper() == "USD" else "KES "
            def money(v, cur=cur):
                return (f"${v:,.2f}" if cur == "$" else kes(v)) if v is not None else ""
            past = [byw[w] for w in weeks[:-1][-3:] if w in byw]
            avg = (sum(p["spend"] for p in past) / sum(p["results"] for p in past)) if past and sum(p["results"] for p in past) else None
            d = pct(cpr(r), avg) if avg else None
            out.append([f"{pf} {cp}", MKT_LABEL[mk], money(r["spend"]), f"{r['results']:,.0f} {r['result_type']}",
                        money(cpr(r)), {"t": spct(d) if d is not None else "New", "c": tone(d, good_up=False)}]
                       + [money(cpr(byw[w])) if w in byw else "" for w in weeks])
        return {"title": title, "head": head, "rows": out,
                "note": "Cost per result per week on the right. Lower is better."}

    # ── computed actions ──
    if sales:
        for m in ads.MARKETS:
            a, s = adw[m][L], sales[m][L]
            if not s["bags"]:
                continue
            sh, cpb = a["spend"] / s["kes"] * 100 if s["kes"] else 0, a["spend"] / s["bags"]
            if sh > 6 or cpb > 150:
                actions.append({"kind": "watch", "market": m, "tags": ["all", "shops", "offers"],
                                "text": f"{MKT_LABEL[m]}: ads cost {kes(cpb)} per bag sold, {sh:.1f}% of revenue, in the week of {week_txt} "
                                        f"({kes(a['spend'])} for {s['bags']:,} bags). Ads aren't paying back at the till here: "
                                        f"test a lower budget or move it to the cheapest campaign."})
            if prev:
                pa, ps = adw[m][L - 1], sales[m][L - 1]
                mp, op = pct(a["messages"], pa["messages"]), pct(s["orders"], ps["orders"])
                if mp is not None and op is not None and mp >= 5 and op <= -5:
                    actions.append({"kind": "watch", "market": m, "tags": ["all", "offers"],
                                    "text": f"{MKT_LABEL[m]}: messages {spct(mp)} but orders {spct(op)} week on week. The extra chats "
                                            f"aren't buying: check which campaign's messages turn into sales before adding budget."})
    for key in sorted({(r["market"], r["platform"], r["campaign"]) for r in rows if r["week"] == last}):
        byw = {r["week"]: r for r in rows if (r["market"], r["platform"], r["campaign"]) == key}
        r = byw[last]
        past = [byw[w] for w in weeks[:-1][-3:] if w in byw]
        if not past or not r["results"] or r["focus"] == "website" and r["result_type"] != "purchases":
            continue
        avg = sum(p["spend"] for p in past) / sum(p["results"] for p in past) if sum(p["results"] for p in past) else None
        d = pct(cpr(r), avg) if avg else None
        if d is None:
            continue
        unit = "$" if r["currency"].upper() == "USD" else "KES "
        val = (f"${cpr(r):,.2f}" if unit == "$" else kes(cpr(r)))
        name = f"{r['platform']} {r['campaign']} ({MKT_LABEL[r['market']]})"
        if d >= 15:
            actions.append({"kind": "do", "market": r["market"], "tags": [r["focus"]],
                            "text": f"{name}: {val} per {r['result_type'].rstrip('s')}, {spct(d)} on its 3-week average. Refresh the creative or move budget."})
        elif d <= -15:
            actions.append({"kind": "win", "market": r["market"], "tags": [r["focus"]],
                            "text": f"{name}: {val} per {r['result_type'].rstrip('s')}, {spct(d)} on its 3-week average. Keep what changed."})

    lead = posts_lead_sales(weeks) if sales else None
    if lead:
        actions.append({"kind": "do", "market": "KENYA", "tags": ["all", "offers", "new_bags", "shops"],
                        "text": f"Posts pay off a week later: Kenya bags posted more sold {spct(lead['more'], 1)} the following week, "
                                f"bags posted less {spct(lead['fewer'], 1)} ({lead['nMore'] + lead['nFewer']} bag-week comparisons). "
                                f"Plan posts a week before the sales are wanted, and judge a post by next week's sales."})

    corp = corporate_return(rows)
    if corp:
        ret = corp["kes"] / corp["spend"] if corp["spend"] else 0
        actions.append({"kind": "win" if ret >= 5 else "watch", "market": "KENYA", "tags": ["corporate", "all"],
                        "text": f"Corporate offers campaign: {kes(corp['spend'])} spent and {corp['messages']:,.0f} messages "
                                f"({corp['start'].day} {corp['start'].strftime('%b')} to {corp['end'].day} {corp['end'].strftime('%b')}); corporate clients paid "
                                f"{kes(corp['kes'])} for {corp['bags']:,} bags in that time, {ret:,.0f} times the spend. "
                                f"Not all of it came from the ads: tag each corporate chat with its source to see the real share."})

    # A paused campaign: that market's sales since the report week vs the same days a week earlier.
    today = dt.date.today()
    after_start = last + dt.timedelta(days=7)
    after_end = min(today - dt.timedelta(days=1), after_start + dt.timedelta(days=6))
    if sales and after_end >= after_start:
        for n in ads.notes():
            if n["kind"] != "event" or "paused" not in n["text"].lower():
                continue
            m = n["market"]
            now = market_sales(after_start, after_end).get(m)
            was = market_sales(after_start - dt.timedelta(days=7), after_end - dt.timedelta(days=7)).get(m)
            if now and was:
                days = (after_end - after_start).days + 1
                d = pct(now["bags"], was["bags"])
                actions.append({"kind": "event", "market": m, "tags": ["all", "offers", "shops"],
                                "text": f"{MKT_LABEL[m]} since the pause: {now['bags']} bags and {now['orders']} orders in the first {days} days, "
                                        f"against {was['bags']} bags and {was['orders']} orders on the same days a week earlier ({spct(d)}). "
                                        + ("No drop so far, so those ads weren't driving till sales." if d is not None and d >= -10
                                           else "Sales fell, so the ads were pulling customers in: relaunch once the account is safe.")})

    for n in ads.notes():
        actions.append({"kind": n["kind"], "market": n["market"], "tags": n["tags"], "text": n["text"]})

    order = {"event": 0, "watch": 1, "do": 2, "win": 3}
    actions.sort(key=lambda a: order.get(a["kind"], 9))

    # ── sections ──
    foot = (f"Ads from marketing's Weekly Ads Performance Report, week of {week_txt} (Sun–Sat). USD channels (Google, X) "
            f"at ≈KES {ads.USD_KES:,.0f} per $. Sales from Odoo, posts from the posting sheets. Ads and sales are compared by week "
            f"and market; no ad is linked to a single till sale.")
    def acts(tags):
        # The page's own tag first (offers on an offers page), then by kind: event, watch, do, win.
        own = tags[0]
        sel = [a for a in actions if set(a["tags"]) & set(tags)]
        sel.sort(key=lambda a: (0 if own in a["tags"] else 1, order.get(a["kind"], 9)))
        return [{"kind": a["kind"], "market": MKT_LABEL.get(a["market"], a["market"]), "text": a["text"]} for a in sel]

    def focus_tiles(focus, label):
        # Tiles for one group of campaigns (offers / new bags): spend, results, cost per result, week on week.
        def agg(w):
            sel = [r for r in rows if r["focus"] == focus and r["week"] == w]
            chat = [r for r in sel if r["result_type"] in ads.CHAT_TYPES]
            return sum(r["spend_kes"] for r in sel), sum(r["results"] for r in chat), sum(r["spend_kes"] for r in chat)
        sp, ms, cs = agg(last)
        psp, pms, pcs = agg(prev) if prev else (0, 0, 0)
        cpm, pcpm = (cs / ms if ms else None), (pcs / pms if pms else None)
        t = [{"k": label + " spend", "v": kes(sp), "n": (spct(pct(sp, psp)) + " week on week" if psp else ""), "tone": ""},
             {"k": label + " messages", "v": f"{round(ms):,}", "n": (spct(pct(ms, pms)) + " week on week" if pms else ""),
              "tone": tone(pct(ms, pms)) if pms else ""},
             {"k": "Cost per message", "v": kes(cpm) if cpm else "",
              "n": (f"was {kes(pcpm)} the week before" if pcpm else ""), "tone": tone(pct(cpm, pcpm), good_up=False) if cpm and pcpm else ""}]
        return t + [x for x in overview_tiles() if x["k"] == "Ad cost per bag sold"]

    def chart_data(focus=None, scope="All ads"):
        # Week on week by market (spend / messages limited to the page's campaigns) + last week's campaigns.
        def ser(fn):
            return {MKT_LABEL[m]: [round(fn(m, i), 1) for i in range(len(weeks))] for m in ads.MARKETS}
        def sel(m, i):
            return [r for r in rows if r["market"] == m and r["week"] == weeks[i] and (focus is None or r["focus"] == focus)]
        series = {
            "spend":     ser(lambda m, i: sum(r["spend_kes"] for r in sel(m, i))),
            "chatSpend": ser(lambda m, i: sum(r["spend_kes"] for r in sel(m, i) if r["result_type"] in ads.CHAT_TYPES)),
            "messages":  ser(lambda m, i: sum(r["results"] for r in sel(m, i) if r["result_type"] in ads.CHAT_TYPES)),
        }
        if sales:
            series["bags"] = ser(lambda m, i: sales[m][i]["bags"])
            series["revenue"] = ser(lambda m, i: sales[m][i]["kes"])
        if posts:
            series["posts"] = ser(lambda m, i: posts[m][i])
        camps = []
        for key in sorted({(r["market"], r["platform"], r["campaign"]) for r in rows
                           if r["week"] == last and (focus is None or r["focus"] == focus)}):
            byw = {r["week"]: r for r in rows if (r["market"], r["platform"], r["campaign"]) == key}
            r = byw[last]
            past = [byw[w] for w in weeks[:-1][-3:] if w in byw]
            pr = sum(p["results"] for p in past)
            chat = r["result_type"] in ads.CHAT_TYPES
            short = (r["campaign"].replace("UG Monthly Offers | Traffic", "website traffic").replace("Tanzania ", "").replace("Uganda ", "").replace("UG ", "")
                     .replace(" | Sales", "").replace(" | Traffic", " traffic"))
            tag = {"SINZA": " (TZ)", "UGANDA": " (UG)"}.get(r["market"], "")
            camps.append({"name": f"{r['platform']} {short}{tag}", "market": MKT_LABEL[r["market"]],
                          "spend": round(r["spend_kes"]), "usd": r["currency"].upper() == "USD",
                          "results": r["results"], "type": r["result_type"], "chat": chat,
                          "cpr": round(r["spend_kes"] / r["results"], 1) if chat and r["results"] else None,
                          "avg3": round(sum(p["spend_kes"] for p in past) / pr, 1) if chat and pr else None})
        return {"scope": scope, "weeks": [wk_label(w) for w in weeks], "markets": [MKT_LABEL[m] for m in ads.MARKETS],
                "series": series, "campaigns": camps}

    def section(kind, tags):
        sec = {"week": week_txt, "tiles": overview_tiles(), "tables": [], "actions": acts(tags), "foot": foot,
               "chart": chart_data({"offers": "offers", "new_bags": "new_bags"}.get(kind),
                                   {"offers": "Offer ads", "new_bags": "New Bags ads"}.get(kind, "All ads"))}
        if kind == "overview":
            sec["lead"] = "What the ads cost and what sold, by market."
            sec["tables"] = [market_table()]
        elif kind == "shops":
            sec["lead"] = "What the ads cost per bag sold in each market, and which branches are cheap or dear to advertise."
            sec["tables"] = [market_table()]
        elif kind == "offers":
            sec["lead"] = "The offer campaigns behind these bags: what they cost and whether they're getting cheaper."
            sec["tiles"] = focus_tiles("offers", "Offer ads")
            sec["tables"] = [campaign_table({"offers"}, "Offer campaigns")]
        elif kind == "new_bags":
            sec["lead"] = "The New Bags campaign and what the ads cost against sales."
            sec["tiles"] = focus_tiles("new_bags", "New Bags ads")
            sec["tables"] = [campaign_table({"new_bags"}, "New Bags campaign"), market_table()]
        elif kind == "posting":
            sec["lead"] = "Posts, ads and sales side by side, week by week."
            if lead:
                sec["tiles"] = sec["tiles"][:2] + [
                    {"k": "Posted more, next week", "v": spct(lead["more"], 1), "n": f"sales change for {lead['nMore']} bag-weeks posted more", "tone": tone(lead["more"])},
                    {"k": "Posted less, next week", "v": spct(lead["fewer"], 1), "n": f"sales change for {lead['nFewer']} bag-weeks posted less", "tone": tone(lead["fewer"])}]
            sec["tables"] = [trend_table()]
        return sec

    out = {"generated": dt.date.today().isoformat(), "week": last.isoformat(),
           "pages": {page: section(kind, tags) for page, (kind, tags) in PAGES.items()}}
    out["pages"]["_default"] = section("overview", ["all"])
    with open(paths.data("ads_impact.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"Ads impact written: week of {week_txt}, {len(actions)} actions, sales {'from Odoo' if sales else 'unavailable'}, "
          f"posts {'read' if posts else 'unavailable'}.")
    return out


if __name__ == "__main__":
    build()
