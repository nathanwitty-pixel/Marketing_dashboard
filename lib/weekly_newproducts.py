"""lib/weekly_newproducts.py — the Weekly Report's New Products slides (all markets, as on New Products Analytics):
1 month to date and week by week, 2 runway bags sold, 3 sales by shop, 4 sold vs monthly target,
5 in stock: could move well vs least performers.
Spec: docs/weekly-report.md › New Products slides.

    slides(week_start, week_end) → [slide dicts] (the Weekly Report's shape)
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import re
import sys

from lib import paths

# till (pos_config name, lower case) → the New Products page's shop code
SHOP_CODE = {"starmall": "STR", "mombasa": "MSA", "nakuru": "NAK", "eldoret": "ELD", "kisumu": "KSM", "meru": "MER",
             "thika": "THK", "hazina": "HAZ", "kitengela": "KIT", "website": "WEB", "website sales": "WEB",
             "nanyuki": "NAN", "kakamega": "KAK", "hilton": "HTN", "sinza": "SNZ", "dar-es-alam": "SNZ",
             "uganda": "UGD", "kisii": "KSII", "ktda shop": "KTD", "busia": "BSA", "rongai": "RGI", "nyeri": "NYR"}
SKIP_TILLS = {"staff pos"}
MIN_STOCK = 5          # colours with less stock aren't judged on slide 5
COVER_OK = 2           # could move well: stock lasts at least this many weeks of last week's pace


def _fmt(x):
    return "—" if x is None else f"{round(x):,}"


def _pct(a, b):
    return (a - b) / b * 100 if b else None


def _signed(p):
    return "new" if p is None else f"{'+' if p >= 0 else ''}{p:.0f}%"


def _d(d):
    return f"{d.day} {d:%b}"


def _t(name):
    return str(name).title()


def _np_fields():
    t = open(paths.html("new_products.html"), encoding="utf-8").read()
    i, j = t.index("<!-- NEW_PROD_DATA_START -->"), t.index("<!-- NEW_PROD_DATA_END -->")
    out = {}
    for line in t[i:j].splitlines():
        m = re.match(r"^\s{2}([A-Za-z_]\w*):\s*(.+?),?\s*$", line)
        if m:
            try:
                out[m.group(1)] = json.loads(m.group(2))
            except ValueError:
                pass
    return out


def _lines(s, e):
    gen = paths.generator()
    if gen not in sys.path:
        sys.path.insert(0, gen)
    import product_performance as pp                       # main-guarded: importing doesn't rebuild the page
    from lib import runway_bags
    return pp.load_lines(s, e, runway_bags.type_fn())


def _weeks(m1, end):
    out, s, i = [], m1, 1
    while s <= end:
        e = min(s + dt.timedelta(days=(5 - s.weekday()) % 7), end)
        out.append((f"Wk {i}", s, e))
        s, i = e + dt.timedelta(days=1), i + 1
    return out


def slides(week_start: dt.date, week_end: dt.date) -> list:
    NP = _np_fields()
    names = [str(n).upper() for n in NP.get("productNames") or []]
    if not names:
        return []
    targets = {str(p["name"]).upper(): p for p in NP.get("productTargets") or []}
    m1 = week_end.replace(day=1)
    pw_s, pw_e = week_start - dt.timedelta(days=7), week_end - dt.timedelta(days=7)
    lines = [x for x in _lines(min(m1, pw_s), week_end) if x["bag"] in names]
    weeks = _weeks(m1, week_end)
    days_in_month = ((m1 + dt.timedelta(days=32)).replace(day=1) - m1).days
    gone = ((week_end - m1).days + 1) / days_in_month

    def units(s, e, by="bag"):
        c = collections.Counter()
        for x in lines:
            if s <= x["d"] <= e and (by != "shop" or x["till"] not in SKIP_TILLS):
                c[x["bag"] if by == "bag" else SHOP_CODE.get(x["till"], "OTH")] += x["units"]
        return c

    mtd, lw, pw = units(m1, week_end), units(week_start, week_end), units(pw_s, pw_e)
    wk_units = [units(s, e) for _, s, e in weeks]
    # stock per product and per colour (Kenya shops + Sinza and Uganda), sales / posts per colour this month
    colours = [r for r in NP.get("monthlyCombined") or [] if str(r.get("bagType", "")).upper() in names]
    lastwk = {r["productName"]: (r.get("lastWeekKenya") or 0) + (r.get("lastWeekOutside") or 0)
              for r in NP.get("weeklyCombined") or []}
    stock = collections.Counter()
    for r in colours:
        stock[str(r["bagType"]).upper()] += (r.get("sKenya") or 0) + (r.get("sOutside") or 0)
    hist = {h["weekStart"]: h for h in NP.get("weeklyPostsHistory") or []}
    wtarget = float(str(NP.get("weeklyTarget") or 0).replace(",", "") or 0)
    src = "Odoo tills (combo bags included) to the report Saturday; targets, stock and posts from the New Products page."
    out = []

    # ── 1. Month to date and week by week ──
    tot_t = sum((targets.get(n) or {}).get("target", 0) for n in names)
    tot_m, tot_lw, tot_pw = sum(mtd.values()), sum(lw.values()), sum(pw.values())
    wk_tot = [round(sum(w.values())) for w in wk_units]
    rows = []
    tgt_of = lambda n: (targets.get(n) or {}).get("target", 0)                       # noqa: E731
    for n in sorted(names, key=lambda n: (-(mtd[n] / tgt_of(n) if tgt_of(n) else -1), -mtd[n])):   # highest % of target first
        tg = (targets.get(n) or {}).get("target", 0)
        rows.append([_t(n)] + [_fmt(w[n]) for w in wk_units] + [_fmt(mtd[n]), _fmt(tg), f"{mtd[n] / tg * 100:.0f}%" if tg else "—"])
    rows.append(["Total"] + [_fmt(v) for v in wk_tot] + [_fmt(tot_m), _fmt(tot_t), f"{tot_m / tot_t * 100:.0f}%" if tot_t else "—"])
    pct_of = {n: mtd[n] / targets[n]["target"] * 100 for n in names if (targets.get(n) or {}).get("target")}
    s1 = {"id": "np-weeks", "kicker": f"New products, month to date and week by week ({_d(m1)} to {_d(week_end)})",
          "tone": "bad" if tot_t and tot_m / tot_t < gone * 0.9 else "neutral", "insight": [], "rec": [], "source": src,
          "graph": {"ok": True, "kind": "npweeks", "labels": [f"{k} ({s.day}–{e.day} {e:%b})" for k, s, e in weeks],
                    "bags": wk_tot, "target": round(wtarget) if wtarget else None,
                    "posts": [(hist.get(s.isoformat()) or {}).get("kenyaPosts") for _, s, _ in weeks],
                    "table": {"title": "Bags sold per new product", "rows": rows,
                              "cols": ["Product"] + [k for k, _, _ in weeks] + ["Month", "Target", "% of target"],
                              "trend": [1, len(weeks)]}}}
    s1["headline"] = (f"New products sold {_fmt(tot_m)} of their {_fmt(tot_t)} target ({tot_m / tot_t * 100:.0f}%) by "
                      f"{_d(week_end)}, with {gone * 100:.0f}% of the month gone; last week {_fmt(tot_lw)} bags "
                      f"({_signed(_pct(tot_lw, tot_pw))} on the week before)" + (f" against a weekly target of {_fmt(wtarget)}." if wtarget else "."))
    if pct_of:
        best, worst = max(pct_of, key=pct_of.get), min(pct_of, key=pct_of.get)
        s1["insight"].append(f"Best against target: <b>{_t(best)}</b> {pct_of[best]:.0f}% ({_fmt(mtd[best])} of "
                             f"{_fmt(targets[best]['target'])}); weakest: <b>{_t(worst)}</b> {pct_of[worst]:.0f}% "
                             f"({_fmt(mtd[worst])} of {_fmt(targets[worst]['target'])}).")
    ch = {n: lw[n] - pw[n] for n in names}
    up, dn = max(ch, key=ch.get), min(ch, key=ch.get)
    if ch[up] > 0 or ch[dn] < 0:
        s1["insight"].append("Last week vs the week before: " + ", ".join(
            f"{_t(n)} {_fmt(pw[n])} → {_fmt(lw[n])}" for n in dict.fromkeys([up, dn]) if ch[n]) + ".")
    h1, h0 = hist.get(week_start.isoformat()) or {}, hist.get(pw_s.isoformat()) or {}
    posted = lambda h: (h.get("kenyaPosts") or 0) + (h.get("outsidePosts") or 0)    # noqa: E731
    if h1 and posted(h1):
        s1["insight"].append(f"Posts last week: {_fmt(h1.get('kenyaPosts'))} in Kenya and {_fmt(h1.get('outsidePosts'))} outside"
                             + (f" (the week before: {_fmt(h0.get('kenyaPosts'))} and {_fmt(h0.get('outsidePosts'))})." if h0 else "."))
    elif h0:          # posts reach the sheet a week late (memory: posts are a week in arrears)
        s1["insight"].append(f"Posts (a week behind, last week's aren't in yet): week of {_d(pw_s)} {_fmt(h0.get('kenyaPosts'))} "
                             f"in Kenya and {_fmt(h0.get('outsidePosts'))} outside.")
    left = (week_end.replace(day=days_in_month) - week_end).days
    need = max(tot_t - tot_m, 0)
    if left and need:
        s1["rec"].append(f"Sell {_fmt(need / left)} new-product bags a day for the rest of the month to reach "
                         f"{_fmt(tot_t)} (last week: {_fmt(tot_lw / 7)} a day).")
    gap = sorted((n for n in names if (targets.get(n) or {}).get("target")),
                 key=lambda n: -(targets[n]["target"] - mtd[n]))
    with_stock = [n for n in gap if stock[n] > 0]
    if with_stock:
        n = with_stock[0]
        s1["rec"].append(f"Push {_t(n)} first: {_fmt(targets[n]['target'] - mtd[n])} still needed and {_fmt(stock[n])} in stock.")
    if h1 and h0 and posted(h1) and (h1.get("kenyaPosts") or 0) < (h0.get("kenyaPosts") or 0):
        s1["rec"].append("Post the new products more: Kenya posts fell last week.")
    out.append(s1)

    # ── 2. Runway Bags Sold: last month's runway styles (created in the previous calendar month) ──
    from lib import runway_bags
    typ = runway_bags.type_fn()
    p_end = m1 - dt.timedelta(days=1)
    p_start = p_end.replace(day=1)
    try:
        rbags = runway_bags.runway_bags(today=p_end, days=(p_end - p_start).days, typ=typ)
    except Exception as e:                                  # noqa: BLE001
        print(f"  WARNING: runway styles skipped: {e}")
        rbags = []
    rbags = [b for b in rbags if p_start.isoformat() <= b["created"] <= p_end.isoformat()]
    rnames = [b["name"] for b in rbags]
    styles = {}
    if rnames:
        first = min(dt.date.fromisoformat(b["created"]) for b in rbags)
        sold_m = runway_bags.sold_by_type(rnames, m1, week_end, typ)
        sold_l = runway_bags.sold_by_type(rnames, week_start, week_end, typ)
        sold_p = runway_bags.sold_by_type(rnames, pw_s, pw_e, typ)
        sold_a = runway_bags.sold_by_type(rnames, first, week_end, typ)
        st_ke, st_out = runway_bags.stock_by_type(rnames, typ)
        for b in rbags:
            n = b["name"]
            styles[n] = {"created": b["created"], "month": sold_m.get(n, 0), "last": sold_l.get(n, 0),
                         "prev": sold_p.get(n, 0), "life": sold_a.get(n, 0),
                         "stockKe": st_ke.get(n, 0), "stock": st_ke.get(n, 0) + st_out.get(n, 0)}
    # only styles that reached the shops (sold or in stock): the rest were created but never stocked or sold
    unproven = sorted(s for s, v in styles.items() if v["life"] == 0 and v["stock"] <= 0)
    styles = {s: v for s, v in styles.items() if s not in unproven}
    order = sorted(styles, key=lambda s: (-styles[s]["month"], -styles[s]["life"], s))
    s2 = {"id": "np-runway", "kicker": f"Runway bags sold: last month's new styles (created in {p_start:%B})",
          "tone": "neutral", "insight": [], "rec": [],
          "source": f"Odoo: bag styles first created {_d(p_start)} to {_d(p_end)} (New Products left out); POS bags "
                    f"(combo bags included) to {_d(week_end)}; live stock, Kenya shops + Sinza and Uganda.",
          "graph": {"ok": bool(order), "kind": "runway", "rows": [
              {"style": _t(s), "month": styles[s]["month"], "last": styles[s]["last"], "prev": styles[s]["prev"],
               "life": styles[s]["life"], "stock": styles[s]["stock"], "created": styles[s]["created"],
               "age": (week_end - dt.date.fromisoformat(styles[s]["created"])).days,
               "state": ("cleared" if styles[s]["stock"] <= 0 else "selling" if styles[s]["month"] > 0 else "idle")}
              for s in order[:14]]}}
    if order:                                        # the styles together: what they sold this month and last week
        s2["graph"]["total"] = {"label": f"All {p_start:%B} styles", "month": sum(v["month"] for v in styles.values()),
                                "last": sum(v["last"] for v in styles.values()), "prev": sum(v["prev"] for v in styles.values()),
                                "life": sum(v["life"] for v in styles.values()), "stock": sum(v["stock"] for v in styles.values())}
    if order:
        tot = sum(v["month"] for v in styles.values())
        tl, tp = sum(v["last"] for v in styles.values()), sum(v["prev"] for v in styles.values())
        top = order[0]
        s2["headline"] = (f"{p_start:%B}'s {len(styles)} new styles in the shops sold {_fmt(tot)} bags this month"
                          + (f", led by {_t(top)} ({_fmt(styles[top]['month'])})" if styles[top]["month"] else "")
                          + f"; last week {_fmt(tl)} ({_signed(_pct(tl, tp))} on the week before).")
        s2["insight"].append("Sold since created: " + ", ".join(
            f"{_t(s)} {_fmt(styles[s]['life'])}" for s in sorted(styles, key=lambda s: -styles[s]["life"])[:6]) + ".")
        moved = [s for s in order if styles[s]["last"] != styles[s]["prev"]]
        if moved:
            s2["insight"].append("Last week vs the week before: " + ", ".join(
                f"{_t(s)} {_fmt(styles[s]['prev'])} → {_fmt(styles[s]['last'])}" for s in moved[:5]) + ".")
        # stock check: cleared (sold, none left) vs still in the shops (selling / not selling)
        cleared = [s for s in order if styles[s]["stock"] <= 0]
        idle = sorted((s for s in order if styles[s]["stock"] > 0 and styles[s]["month"] == 0), key=lambda s: -styles[s]["stock"])
        selling = [s for s in order if styles[s]["stock"] > 0 and styles[s]["month"] > 0]
        in_stock = idle + selling
        listed = lambda ss: ", ".join(_t(s) for s in ss[:6]) + (f" and {len(ss) - 6} more" if len(ss) > 6 else "")   # noqa: E731
        s2["insight"].append(f"Stock check: <b>{len(cleared)}</b> cleared (sold, none left), <b>{len(selling)}</b> still in the "
                             f"shops and selling, <b>{len(idle)}</b> in the shops and not selling this month "
                             f"({_fmt(sum(styles[s]['stock'] for s in in_stock))} bags left).")
        if cleared:
            s2["rec"].append(f"Cleared: {listed(cleared)}. Marketing and sales did a good job; decide whether to reorder them.")
        if in_stock:
            s2["rec"].append("Shoot at least a short video of each runway style still in stock and show it online in a regular "
                             "Runway segment, to reach the one buyer who wants it (in the shops now): "
                             + ", ".join(f"{_t(s)} {_fmt(styles[s]['stock'])}" for s in in_stock[:8])
                             + (f" and {len(in_stock) - 8} more" if len(in_stock) > 8 else "") + ".")
        if idle:
            s2["rec"].append(f"Start with the ones not selling: {listed(idle)}.")
        if unproven:
            s2["insight"].append(f"Not shown: {len(unproven)} other {p_start:%B} styles were created in Odoo but never stocked "
                                 f"or sold ({', '.join(_t(s) for s in unproven[:5])}{' and more' if len(unproven) > 5 else ''}).")
        s2["rec"] = s2["rec"][:3] or [f"Keep posting {p_start:%B}'s new styles: they are in the shops and selling."]
    else:
        s2["headline"] = f"No new bag styles were created in Odoo in {p_start:%B}."
    out.append(s2)

    # ── 3. Sales by Shop ──
    sh_m, sh_l, sh_p = units(m1, week_end, "shop"), units(week_start, week_end, "shop"), units(pw_s, pw_e, "shop")
    ss = NP.get("shopSales") or {}
    corp = lambda p: sum((r or {}).get("CORP", 0) or 0 for r in ((ss.get(p) or {}).get("rows") or {}).values())  # noqa: E731
    sh_m["CORP"] += corp("monthly")
    sh_l["CORP"] += corp("lastweek")
    shops = [s for s in sorted(set(sh_m) | set(sh_l) | set(sh_p), key=lambda s: -sh_m[s]) if sh_m[s] or sh_l[s] or sh_p[s]]
    s3 = {"id": "np-shops", "kicker": "New products: sales by shop, week to week and month to date", "tone": "neutral",
          "insight": [], "rec": [], "source": src + " CORP = Corporate app (week before not split by product, left blank).",
          "graph": {"ok": bool(shops), "kind": "npshops", "rows": [
              {"shop": s, "last": round(sh_l[s]), "prev": None if s == "CORP" else round(sh_p[s]), "month": round(sh_m[s])}
              for s in shops], "curLabel": f"{_d(week_start)} to {_d(week_end)}", "prevLabel": f"{_d(pw_s)} to {_d(pw_e)}",
              "total": {"label": "All shops", "month": round(sum(sh_m.values())), "last": round(sum(sh_l.values())),
                        "prev": round(sum(sh_p.values()))}}}
    if shops:
        top3 = shops[:3]
        s3["headline"] = (f"{top3[0]} sold the most new products this month ({_fmt(sh_m[top3[0]])})"
                          + (f", then {', '.join(f'{s} {_fmt(sh_m[s])}' for s in top3[1:])}" if len(top3) > 1 else "")
                          + f"; last week all shops sold {_fmt(sum(sh_l.values()))} ({_signed(_pct(sum(sh_l.values()), sum(sh_p.values())))}).")
        d = {s: sh_l[s] - sh_p[s] for s in shops if s != "CORP"}
        if d:
            u, w = max(d, key=d.get), min(d, key=d.get)
            s3["insight"].append(f"Biggest rise last week: {u} {_fmt(sh_p[u])} → {_fmt(sh_l[u])}; biggest fall: {w} {_fmt(sh_p[w])} → {_fmt(sh_l[w])}.")
        best_shop = {}
        for x in lines:
            if week_start <= x["d"] <= week_end and x["till"] not in SKIP_TILLS:
                best_shop.setdefault(x["bag"], collections.Counter())[SHOP_CODE.get(x["till"], "OTH")] += x["units"]
        tops = sorted(names, key=lambda n: -lw[n])[:4]
        s3["insight"].append("Best shop last week: " + ", ".join(
            f"{_t(n)} at {best_shop[n].most_common(1)[0][0]}" for n in tops if n in best_shop) + ".")
        zero = [c for c in SHOP_CODE.values() if not sh_l[c]]
        zero = list(dict.fromkeys(zero))
        if zero:
            s3["insight"].append("No new-product sale last week: " + ", ".join(zero) + ".")
            s3["rec"].append(f"Check stock and posts for the new products at {', '.join(zero[:6])}: no sale last week.")
        s3["rec"].append(f"Copy what {top3[0]} does with the new products (display, staff pitch) in the shops that sold none.")
    else:
        s3["headline"] = "No new-product sales by shop this month."
    out.append(s3)

    # ── 4. Sold vs Monthly Target ──
    rows4 = []
    for n in names:
        tg = (targets.get(n) or {}).get("target", 0)
        if not tg:
            continue
        rows4.append({"name": _t(n), "sold": round(mtd[n]), "target": tg, "expected": round(tg * gone),
                      "pct": round(mtd[n] / tg * 100), "stock": stock[n], "onPace": mtd[n] >= tg * gone})
    rows4.sort(key=lambda r: -r["pct"])
    on = [r for r in rows4 if r["onPace"]]
    s4 = {"id": "np-target", "kicker": f"New products: sold vs monthly target ({_d(m1)} to {_d(week_end)})",
          "tone": "good" if rows4 and len(on) == len(rows4) else "bad" if rows4 and not on else "neutral",
          "insight": [], "rec": [], "source": src,
          "graph": {"ok": bool(rows4), "kind": "nptarget", "rows": rows4, "gone": round(gone * 100)}}
    if rows4:
        s4["headline"] = (f"{len(on)} of {len(rows4)} new products are on pace for their monthly target "
                          f"({gone * 100:.0f}% of the month gone)" + (f": {', '.join(r['name'] for r in on)}." if on else "."))
        behind = sorted((r for r in rows4 if not r["onPace"]), key=lambda r: -(r["expected"] - r["sold"]))
        if behind:
            s4["insight"].append("Furthest behind where it should be by now: " + ", ".join(
                f"{r['name']} {_fmt(r['sold'])} vs {_fmt(r['expected'])}" for r in behind[:4]) + ".")
        if on:
            s4["insight"].append("Ahead: " + ", ".join(f"{r['name']} {r['pct']}%" for r in on) + ".")
        for r in behind[:3]:
            if r["stock"] <= 0:
                s4["rec"].append(f"Restock {r['name']} first: none in stock, {_fmt(r['target'] - r['sold'])} still needed.")
            elif r["stock"] < r["target"] - r["sold"]:
                s4["rec"].append(f"Restock {r['name']} while pushing it: {_fmt(r['stock'])} in stock, {_fmt(r['target'] - r['sold'])} still needed.")
            else:
                s4["rec"].append(f"Push and post {r['name']}: {_fmt(r['stock'])} in stock, {_fmt(r['expected'] - r['sold'])} behind pace.")
    else:
        s4["headline"] = "No new-product targets this month."
    out.append(s4)

    # ── 5. In stock: could move well vs least performers (colour level) ──
    col = []
    for r in colours:
        st = (r.get("sKenya") or 0) + (r.get("sOutside") or 0)
        if st < MIN_STOCK:
            continue
        sold = (r.get("kenyaSales") or 0) + (r.get("outsideKenya") or 0)
        col.append({"name": _t(r["productName"]), "bag": str(r["bagType"]).upper(), "stock": st, "sold": sold,
                    "last": lastwk.get(r["productName"], 0), "posts": (r.get("mpostKenya") or 0) + (r.get("mpostOutside") or 0)})
    movers = sorted((c for c in col if c["sold"] > 0 and c["stock"] >= COVER_OK * max(c["last"], 1)), key=lambda c: -c["sold"])[:5]
    least = sorted((c for c in col if c not in movers), key=lambda c: (-(c["stock"] / max(c["sold"], 1)), -c["stock"]))[:5]
    s5 = {"id": "np-stock", "kicker": "New products in stock: could move well vs least performers", "tone": "neutral",
          "insight": [], "rec": [], "source": "The New Products page: colour sales this month, last week, stock (Kenya shops + Sinza and Uganda) and posts.",
          "graph": {"ok": bool(movers or least), "kind": "npstock", "movers": movers, "least": least}}
    if movers or least:
        s5["headline"] = ((f"{movers[0]['name']} leads the new colours with stock to keep selling ({_fmt(movers[0]['sold'])} sold, "
                           f"{_fmt(movers[0]['stock'])} in stock)" if movers else "No new colour is selling with stock behind it")
                          + (f"; {least[0]['name']} is the slowest: {_fmt(least[0]['sold'])} sold with {_fmt(least[0]['stock'])} in stock." if least else "."))
        if movers:
            s5["insight"].append("Could move well: " + ", ".join(f"{c['name']} ({_fmt(c['sold'])} sold, {_fmt(c['stock'])} in stock)" for c in movers) + ".")
            s5["rec"].append("Push " + ", ".join(c["name"] for c in movers[:3]) + ": they sell and the stock is there; feature them in posts and the shop windows.")
        if least:
            s5["insight"].append("Least performers: " + ", ".join(f"{c['name']} ({_fmt(c['sold'])} sold, {_fmt(c['stock'])} in stock, "
                                                                 f"{_fmt(c['posts'])} posts)" for c in least) + ".")
            few = [c for c in least if c["posts"] < 3]
            if few:
                s5["rec"].append("Post " + ", ".join(c["name"] for c in few[:4]) + " first: fewer than 3 posts this month.")
            more = [c for c in least if c["posts"] >= 3]
            for c in more[:1]:
                best = max((x for x in col if x["bag"] == c["bag"]), key=lambda x: x["sold"], default=None)
                if not best or best["sold"] < 5 or best["name"] == c["name"]:
                    best = movers[0] if movers else None      # the partner must sell: else the top new-product seller
                pair = f" with {best['name']}" if best else ""
                s5["rec"].append(f"Put {c['name']} on an offer or in a combo{pair}: it is posted and still slow.")
        s5["rec"] = s5["rec"][:3]
    else:
        s5["headline"] = "No new-product colour holds 5 or more in stock."
    out.append(s5)
    return out
