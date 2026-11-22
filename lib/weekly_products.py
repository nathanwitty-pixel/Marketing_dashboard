"""lib/weekly_products.py — the Weekly Report's Product Performance slides, per market (Kenya, Uganda, Tanzania):
A. Bag of the Month week by week vs the whole month, B. top 10 bags moving and the 5 stuck with stock,
C. top 5 categories with their best and weakest bags.
Spec: docs/weekly-report.md › Product Performance slides.

    slides(week_start, week_end) → [slide dicts] (the Weekly Report's shape: kicker, headline, graph, insight, rec)
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import os
import re
import sys

from lib import paths

MARKETS = [("KE", "Kenya"), ("UG", "Uganda"), ("TZ", "Tanzania")]
KICKER_NAME = {"TZ": "Tanzania (Sinza)"}       # the slide label; sentences say Tanzania
STOCK_I = {"KE": 0, "TZ": 1, "UG": 2}          # PP.info[bag].stock = [Kenya, Sinza, Uganda]
POSTS_I = {"KE": 0, "TZ": 1, "UG": 1}          # PP.info[bag].postsM = [Kenya, outside Kenya]
BULK = 10              # a POS line of 10+ units = a bulk order (product_performance.BULK_LINE_QTY)
MOVER_MIN_WEEK = {"KE": 10, "TZ": 3, "UG": 3}   # the mover sells at least this many a week (Kenya = the page's MOVER_MIN)
COVER_WEEKS = 2        # stock under this many weeks of last week's pace = restock
SLOWING = 20           # last week this % under the month average a week = slowing
STUCK_MIN = {"KE": 30, "UG": 10, "TZ": 10}     # shop stock a stuck bag must have
SMALL_WEEK = 100       # under this many bags in the week = a small market, say so
WEAK_MIN, WEAK_MAX = 3, 5   # weakest bags listed per category
WEAK_COVER = 6              # a weak bag's shop stock lasts at least this many weeks at last week's pace


def _fmt(x):
    return "—" if x is None else f"{round(x):,}"


def _pct(a, b):
    return (a - b) / b * 100 if b else None


def _signed(p, dp=0):
    return "new" if p is None else f"{'+' if p >= 0 else ''}{p:.{dp}f}%"


def _d(d):
    return f"{d.day} {d:%b}"


def _title(bag):
    return str(bag).title()


def _pp_page():
    t = open(paths.html("product_performance.html"), encoding="utf-8").read()
    m = re.search(r"const PP = (.*?);\s*</script>", t, re.S)
    return json.loads(m.group(1)) if m else {}


def _load_lines(s, e):
    gen = paths.generator()
    if gen not in sys.path:
        sys.path.insert(0, gen)
    import product_performance as pp                       # main-guarded: importing doesn't rebuild the page
    from lib import runway_bags
    return pp.load_lines(s, e, runway_bags.type_fn())


def _units(lines, mkt, s, e, nobulk=False):
    u, r = collections.Counter(), collections.Counter()
    for x in lines:
        if x["mkt"] == mkt and s <= x["d"] <= e:
            if nobulk and not x["sub"] and x["units"] >= BULK:
                continue
            u[x["bag"]] += x["units"]
            r[x["bag"]] += x["rev"]
    return u, r


def _weeks(m1, end):
    """The Sun–Sat weeks from the 1st to `end`; the first can be short."""
    out, s, i = [], m1, 1
    while s <= end:
        e = min(s + dt.timedelta(days=(5 - s.weekday()) % 7), end)
        out.append((f"Wk {i}", s, e))
        s, i = e + dt.timedelta(days=1), i + 1
    return out


def _stuck_rec(bag, mkt, info, cat_top):
    """The page's bottom-bag rule (docs/product-performance.md › Top 5 categories — suggestions)."""
    i = info.get(bag) or {}
    posts = (i.get("postsM") or [0, 0])[POSTS_I[mkt]] or 0
    on_offer = bool(i.get("tags")) if mkt == "KE" else False
    if not posts:
        return "post", f"Post {_title(bag)} first: it wasn't posted this month."
    if not on_offer:
        pair = f" with {_title(cat_top)}" if cat_top and cat_top != bag else ""
        return "offer", f"Put {_title(bag)} on an offer or in a combo{pair}."
    return "check", f"Check {_title(bag)}'s price or design, or clear it: it is on offer and still slow."


def _market_slides(mkt, name, lines, info, why, week_start, week_end):
    kname = KICKER_NAME.get(mkt, name)
    si = STOCK_I[mkt]
    stock = lambda b: ((info.get(b) or {}).get("stock") or [0, 0, 0])[si] or 0       # noqa: E731
    cat = lambda b: ((info.get(b) or {}).get("cat") or "OTHER").upper()                # noqa: E731
    lw, lr = _units(lines, mkt, week_start, week_end)
    pw, _ = _units(lines, mkt, week_start - dt.timedelta(days=7), week_end - dt.timedelta(days=7))
    lw_total, pw_total = sum(lw.values()), sum(pw.values())
    small = (f"{name} sold {_fmt(lw_total)} bags last week, so one sale moves a bag's share a lot."
             if lw_total < SMALL_WEEK else None)
    cover = lambda b: stock(b) / lw[b] if lw[b] > 0 else None                          # noqa: E731
    out = []

    # ── A. Bag of the Month ──
    m1 = week_end.replace(day=1)
    p1 = (m1 - dt.timedelta(days=1)).replace(day=1)
    pend = min(p1 + (week_end - m1), m1 - dt.timedelta(days=1))
    mu, mr = _units(lines, mkt, m1, week_end)
    pu, _ = _units(lines, mkt, p1, pend)
    mnb, _ = _units(lines, mkt, m1, week_end, nobulk=True)
    pnb, _ = _units(lines, mkt, p1, pend, nobulk=True)
    days = (week_end - m1).days + 1
    weeks = _weeks(m1, week_end)
    month_total = sum(mu.values())
    slide = {"id": f"botm-{mkt}", "kicker": f"Bag of the Month, {kname} ({_d(m1)} to {_d(week_end)})",
             "tone": "neutral", "insight": [], "rec": [],
             "source": "Odoo tills (bags in combos included, refunds netted), the Product Performance page's stock and why-it-moved."}
    if mu:
        top = max(mu, key=lambda b: mu[b])
        floor = MOVER_MIN_WEEK[mkt] * days / 7
        movers = [b for b in mnb if b != top and mnb[b] >= floor]
        mover = max(movers, key=lambda b: mnb[b] - pnb.get(b, 0)) if movers else None
        if mover is not None and mnb[mover] - pnb.get(mover, 0) <= 0:
            mover = None
        bags = [b for b in (top, mover) if b]
        # each week's own leaders: top seller, and the biggest rise vs the 7 days before (bulk orders aside)
        leaders = []
        for k, s, e in weeks:
            wu, _ = _units(lines, mkt, s, e)
            wn, _ = _units(lines, mkt, s, e, nobulk=True)
            pn, _ = _units(lines, mkt, s - dt.timedelta(days=7), e - dt.timedelta(days=7), nobulk=True)
            wt = max(wu, key=lambda b: wu[b]) if wu else None
            fl = MOVER_MIN_WEEK[mkt] * ((e - s).days + 1) / 7
            cand = [b for b in wn if b != wt and wn[b] >= fl and wn[b] - pn.get(b, 0) > 0]
            wm = max(cand, key=lambda b: wn[b] - pn.get(b, 0)) if cand else None
            leaders.append({"week": f"{k} ({s.day}–{e.day} {e:%b})",
                            "top": _title(wt) if wt else "—", "topUnits": round(wu[wt]) if wt else 0, "topIsMonth": wt == top,
                            "mover": _title(wm) if wm else "—", "moverFrom": round(pn.get(wm, 0)) if wm else None,
                            "moverTo": round(wn[wm]) if wm else None, "moverIsMonth": wm is not None and wm == mover})
        leaders.append({"week": "Whole month", "top": _title(top), "topUnits": round(mu[top]), "topIsMonth": True,
                        "mover": _title(mover) if mover else "—", "moverFrom": round(pnb.get(mover, 0)) if mover else None,
                        "moverTo": round(mnb[mover]) if mover else None, "moverIsMonth": True, "month": True})
        wk_units = {b: [round(_units(lines, mkt, s, e)[0][b]) for _, s, e in weeks] for b in bags}
        avg = {b: mu[b] / days * 7 for b in bags}
        slide["graph"] = {"ok": True, "kind": "botm",
                          "labels": [f"{k} ({s.day}–{e.day} {e:%b})" for k, s, e in weeks],
                          "series": [{"label": _title(b) + (" (top seller)" if b == top else " (biggest mover)"),
                                      "data": wk_units[b], "avg": round(avg[b])} for b in bags],
                          "leaders": leaders}
        share = mu[top] / month_total * 100 if month_total else 0
        chg = _pct(mu[top], pu.get(top, 0))
        slide["headline"] = (f"{_title(top)} is {name}'s Bag of the Month: {_fmt(mu[top])} bags from {_d(m1)} to "
                             f"{_d(week_end)} ({share:.1f}% of units), {_signed(chg)} on the same days of {p1:%B}.")
        wk_txt = ", ".join(f"{k} <b>{_fmt(u)}</b>" for (k, _, _), u in zip(weeks, wk_units[top]))
        slide["insight"].append(f"{_title(top)} week by week: {wk_txt}, against a month average of {_fmt(avg[top])} a week.")
        other_tops = [(l["week"].split(" (")[0], l["top"]) for l in leaders[:-1] if not l["topIsMonth"]]
        if other_tops:
            rest = (f"; {_title(top)} led the other weeks." if len(other_tops) < len(weeks)
                    else f"; {_title(top)} led no single week but sold the most over the month.")
            slide["insight"].append("The lead changed hands: " + ", ".join(f"{w} was led by <b>{b}</b>" for w, b in other_tops) + rest)
        else:
            slide["insight"].append(f"{_title(top)} was the top seller in every week.")
        slide["insight"].append(f"Whole month: <b>{_fmt(mu[top])}</b> bags, {share:.1f}% of {name}'s {_fmt(month_total)}, "
                                f"KES {_fmt(mr[top])}; {_fmt(pu.get(top, 0))} the same days of {p1:%B}.")
        w = (why.get(mkt) or {}).get(top) or {}
        if w.get("head"):
            sc = (w.get("score") or {})
            slide["insight"].append(f"Why: {w['head']}." + (f" Support {sc['total']}/100, {sc['verdict']}." if sc.get("verdict") else ""))
        c = cover(top)
        slide["insight"].append(f"{_fmt(stock(top))} in {name}'s shops now"
                                + (f": about {c:.1f} weeks at last week's pace." if c is not None else "."))
        for b in bags:
            c = cover(b)
            if c is not None and c < COVER_WEEKS:
                slide["rec"].append(f"Restock {_title(b)}: {_fmt(stock(b))} in the shops is about {c:.1f} weeks at last week's pace.")
            last = wk_units[b][-1] * (7 / ((weeks[-1][2] - weeks[-1][1]).days + 1))
            if avg[b] and last < avg[b] * (1 - SLOWING / 100):
                slide["rec"].append(f"{_title(b)} is slowing ({_fmt(wk_units[b][-1])} last week vs {_fmt(avg[b])} a week "
                                    f"for the month): check its stock by shop and its posts.")
        verdict = ((why.get(mkt) or {}).get(top) or {}).get("score", {}).get("verdict", "")
        vrec = {"Demand": f"Check {_title(top)}'s price and design: it had support and still sold less.",
                "Support": f"Put {_title(top)}'s offer and posts back: support was pulled.",
                "Working": f"Keep {_title(top)}'s offer and posts running: they are working.",
                "Selling": f"Give {_title(top)} more posts: it is selling on its own."}
        for k, v in vrec.items():
            if verdict.startswith(k):
                slide["rec"].append(v)
        slide["rec"] = slide["rec"][:3] or [f"Keep {_title(top)} in stock and posted: it carries the month."]
    else:
        slide.update({"headline": f"No {name} sales this month yet.", "graph": {"ok": False}})
    if small:
        slide["insight"].append(small)
    out.append(slide)

    # ── B. Top 10 moving, 5 stuck ──
    top10 = sorted((b for b in lw if lw[b] > 0), key=lambda b: -lw[b])[:10]
    sh = lambda u, b, t: (u[b] / t * 100) if t else 0                                  # noqa: E731
    rows = [{"bag": _title(b), "units": round(lw[b]), "share": round(sh(lw, b, lw_total), 1),
             "pp": round(sh(lw, b, lw_total) - sh(pw, b, pw_total), 1), "stock": stock(b)} for b in top10]
    stuck = [b for b in info if stock(b) >= STUCK_MIN[mkt] and b not in top10
             and not str(b).startswith(("SAMPLE", "GIFT"))]
    stuck.sort(key=lambda b: (-(stock(b) / max(lw[b], 1)), -stock(b)))
    stuck = stuck[:5]
    srows = [{"bag": _title(b), "stock": stock(b), "units": round(max(lw[b], 0)),
              "cover": round(stock(b) / max(lw[b], 1), 1)} for b in stuck]
    t10 = sum(lw[b] for b in top10)
    t10p = sum(pw[b] for b in sorted((b for b in pw if pw[b] > 0), key=lambda b: -pw[b])[:10])
    slide = {"id": f"top-{mkt}", "kicker": f"Top-selling bags, {kname} (last week, {_d(week_start)} to {_d(week_end)})",
             "tone": "neutral", "insight": [], "rec": [],
             "source": "Odoo tills last week vs the week before; shop stock now from the Product Performance page.",
             "graph": {"ok": bool(rows), "kind": "top10", "top": rows, "stuck": srows}}
    if rows:
        lead = rows[0]
        slide["headline"] = (f"The top 10 bags carried {t10 / lw_total * 100:.0f}% of {name}'s units last week, led by "
                             f"{lead['bag']} ({_fmt(lead['units'])}, {lead['share']:.1f}%)"
                             + (f"; {len(srows)} bags hold {_fmt(sum(r['stock'] for r in srows))} in the shops but sold "
                                f"only {_fmt(sum(r['units'] for r in srows))}." if srows else "."))
        slide["insight"].append(f"Top 10 = <b>{t10 / lw_total * 100:.0f}%</b> of {_fmt(lw_total)} bags "
                                f"(the week before: {t10p / pw_total * 100:.0f}% of {_fmt(pw_total)})." if pw_total else
                                f"Top 10 = <b>{t10 / lw_total * 100:.0f}%</b> of {_fmt(lw_total)} bags.")
        up = max(rows, key=lambda r: r["pp"])
        dn = min(rows, key=lambda r: r["pp"])
        if up["pp"] > 0:
            slide["insight"].append(f"Biggest gain in share: {up['bag']} ({'+' if up['pp'] >= 0 else ''}{up['pp']:.1f} pp)"
                                    + (f"; biggest loss: {dn['bag']} ({dn['pp']:.1f} pp)." if dn["pp"] < 0 else "."))
        short = [b for b in top10 if cover(b) is not None and cover(b) < COVER_WEEKS]
        if short:
            slide["insight"].append("Under 2 weeks of stock: " + ", ".join(f"{_title(b)} ({_fmt(stock(b))} left)" for b in short) + ".")
            slide["rec"].append("Restock " + ", ".join(_title(b) for b in short[:4]) + ": under 2 weeks of stock at last week's pace.")
        if srows:
            slide["insight"].append("Stuck with stock: " + ", ".join(
                f"{r['bag']} ({_fmt(r['stock'])} in shops, sold {_fmt(r['units'])})" for r in srows) + ".")
            cat_top = {}
            for b in sorted(lw, key=lambda b: -lw[b]):
                cat_top.setdefault(cat(b), b)
            groups = collections.OrderedDict()
            for b in stuck:
                kind, text = _stuck_rec(b, mkt, info, cat_top.get(cat(b)))
                groups.setdefault(kind, []).append((b, text))
            for kind, items in groups.items():
                if kind == "post":
                    slide["rec"].append("Post " + ", ".join(_title(b) for b, _ in items) + " first: not posted this month.")
                else:
                    slide["rec"].extend(t for _, t in items[:2])
        slide["rec"] = slide["rec"][:3]
    else:
        slide["headline"] = f"No {name} sales last week."
    if small:
        slide["insight"].append(small)
    out.append(slide)

    # ── C. Top 5 categories ──
    cw, cp = collections.Counter(), collections.Counter()
    for b, u in lw.items():
        cw[cat(b)] += u
    for b, u in pw.items():
        cp[cat(b)] += u
    cats = [c for c, u in cw.most_common() if u > 0][:5]
    slide = {"id": f"cats-{mkt}", "kicker": f"Top 5 categories, {kname} (last week)", "tone": "neutral",
             "insight": [], "rec": [],
             "source": "Odoo tills last week vs the week before; category and stock from the Product Performance page.",
             "graph": {"ok": bool(cats), "kind": "cats", "labels": [c.title() for c in cats],
                       "cur": [round(cw[c]) for c in cats], "prev": [round(cp[c]) for c in cats],
                       "share": [round(cw[c] / lw_total * 100, 1) if lw_total else 0 for c in cats],
                       "curLabel": f"{_d(week_start)} to {_d(week_end)}",
                       "prevLabel": f"{_d(week_start - dt.timedelta(days=7))} to {_d(week_end - dt.timedelta(days=7))}"}}
    weak_all, table = [], []
    for c in cats:
        in_c = sorted((b for b in lw if cat(b) == c and lw[b] >= 1), key=lambda b: -lw[b])
        if not in_c:
            continue
        best = in_c[0]
        # weakest 3 to 5: high stock, not selling (most weeks of cover first); lowest sellers fill it to 3
        stocked = [b for b in info if cat(b) == c and b != best and stock(b) >= STUCK_MIN[mkt]
                   and stock(b) >= WEAK_COVER * max(lw[b], 1) and not str(b).startswith(("SAMPLE", "GIFT"))]
        stocked.sort(key=lambda b: (-(stock(b) / max(lw[b], 1)), -stock(b)))
        weak = stocked[:WEAK_MAX]
        for b in reversed(in_c[1:]):
            if len(weak) >= WEAK_MIN:
                break
            if b not in weak:
                weak.append(b)
        held, sold = sum(stock(b) for b in weak), sum(max(lw[b], 0) for b in weak)
        line = (f"<b>{c.title()}</b> {cw[c] / lw_total * 100:.0f}% of units ({_signed(_pct(cw[c], cp[c]))}): best "
                f"{_title(best)} {_fmt(lw[best])} sold")
        if weak:
            line += f"; its {len(weak)} weakest hold {_fmt(held)} in the shops and sold {_fmt(sold)}"
            weak_all += [(c, w, best) for w in weak]
        slide["insight"].append(line + ".")
        table.append([c.title(), f"{_title(best)} {_fmt(lw[best])} / {_fmt(stock(best))}",
                      ", ".join(f"{_title(w)} {_fmt(max(lw[w], 0))}/{_fmt(stock(w))}" for w in weak) or "—"])
        if stock(best) < lw[best]:
            slide["rec"].append(f"Restock {_title(best)} ({c.title()}): {_fmt(stock(best))} in the shops, it sold {_fmt(lw[best])} last week.")
    if table:
        slide["graph"]["table"] = {"title": "Best and weakest bags per category (sold last week / in the shops now)",
                                   "cols": ["Category", "Best bag", "Weakest bags"], "rows": table, "wrap": True}
    if cats:
        c0 = cats[0]
        weak0 = next((w for c, w, _ in weak_all if c == c0), None)
        slide["headline"] = (f"{c0.title()} is {name}'s biggest category last week ({cw[c0] / lw_total * 100:.0f}% of units)"
                             + (f"; its weakest bag, {_title(weak0)}, sold {_fmt(max(lw[weak0], 0))} with {_fmt(stock(weak0))} in the shops."
                                if weak0 else "."))
        weak_all.sort(key=lambda t: -stock(t[1]))
        seen = set()
        for c, w, best in weak_all:
            if c in seen or len(seen) >= 2:
                continue
            seen.add(c)
            if stock(w) > 2:
                slide["rec"].append(_stuck_rec(w, mkt, info, best)[1])
            else:
                slide["rec"].append(f"Let {_title(w)} run out ({c.title()}): {_fmt(stock(w))} left, don't reorder.")
        slide["rec"] = slide["rec"][:3]
    else:
        slide["headline"] = f"No {name} sales last week."
    if small:
        slide["insight"].append(small)
    out.append(slide)

    # ── D. Male vs female bags ──
    from lib import bag_gender
    sides = ("Male", "Female", "Unisex")
    g_of = lambda b: bag_gender.gender(b, cat(b))                                     # noqa: E731

    def by_side(u):
        c = collections.Counter()
        for b, v in u.items():
            g = g_of(b)
            if g:
                c[g] += v
        return c
    g1, g0, gm = by_side(lw), by_side(pw), by_side(mu)
    t1, t0 = sum(g1.values()), sum(g0.values())
    wk_side = []
    for k, s, e in weeks:
        c = by_side(_units(lines, mkt, s, e)[0])
        tot = sum(c.values())
        wk_side.append({"label": f"{k} ({s.day}–{e.day} {e:%b})", **{x: round(c[x]) for x in sides},
                        **{x + "Pct": round(c[x] / tot * 100) if tot else 0 for x in sides}})
    sh1 = {x: g1[x] / t1 * 100 if t1 else 0 for x in sides}
    sh0 = {x: g0[x] / t0 * 100 if t0 else 0 for x in sides}
    slide = {"id": f"gender-{mkt}", "kicker": f"Male vs female bags, {kname}", "tone": "neutral", "insight": [], "rec": [],
             "source": "Odoo tills; who a bag is for from data/bag_gender.csv (by category, bags can override). Gift bags left out.",
             "graph": {"ok": bool(t1), "kind": "gender", "weeks": wk_side}}
    if t1:
        lead, other = ("Female", "Male") if g1["Female"] >= g1["Male"] else ("Male", "Female")
        slide["headline"] = (f"{lead} bags outsold {other.lower()} bags in {name} last week: {_fmt(g1[lead])} vs "
                             f"{_fmt(g1[other])} ({sh1[lead]:.0f}% vs {sh1[other]:.0f}% of units, the rest unisex).")
        for x in sides:
            tops = sorted((b for b in lw if g_of(b) == x and lw[b] > 0), key=lambda b: -lw[b])[:3]
            d = sh1[x] - sh0[x]
            slide["insight"].append(
                f"<b>{x}</b>: {_fmt(g1[x])} bags, {sh1[x]:.0f}% of units ({'+' if d >= 0 else ''}{d:.1f} pts on the week before)"
                + (f"; top: " + ", ".join(f"{_title(b)} {_fmt(lw[b])}" for b in tops) if tops else "") + ".")
            if x != "Unisex" and t0 and d <= -2 and tops:
                slide["rec"].append(f"Push the {x.lower()} range: its share fell {abs(d):.1f} points last week; "
                                    f"feature {_title(tops[0])} in posts and offers.")
            if x != "Unisex" and tops:
                c = cover(tops[0])
                if c is not None and c < COVER_WEEKS:
                    slide["rec"].append(f"Restock {_title(tops[0])}, the top {x.lower()} bag: about {c:.1f} weeks of stock left.")
        tm = sum(gm.values())
        if tm:
            slide["insight"].append(f"Month so far ({_d(m1)} to {_d(week_end)}): male {gm['Male'] / tm * 100:.0f}%, "
                                    f"female {gm['Female'] / tm * 100:.0f}%, unisex {gm['Unisex'] / tm * 100:.0f}%.")
        slide["rec"] = slide["rec"][:3] or ["Keep the mix: neither the male nor the female range lost share last week."]
    else:
        slide["headline"] = f"No {name} sales last week."
    if small:
        slide["insight"].append(small)
    out.append(slide)
    return out


def _buyer_lines(s, e):
    """[{d, mkt, bag, units, g}] — the Product Performance sales lines with the order's customer gender
    (res_partner.gender: female / male; corporate and blank left out). Only counts leave Odoo, never names."""
    gen = paths.generator()
    if gen not in sys.path:
        sys.path.insert(0, gen)
    import product_performance as pp
    from lib import db, queries, runway_bags
    sql = (pp.LINES_SQL.replace("SELECT pl.id,", "SELECT COALESCE(rp.gender, '') AS gender, pl.id,", 1)
           .replace("FROM pos_order o\n", "FROM pos_order o\nLEFT JOIN res_partner rp ON rp.id = o.partner_id\n", 1))
    df = db.run_query(sql, {"s": s.isoformat(), "e": e.isoformat(), "excluded": queries.excluded_products()})
    if df is None:
        return []
    typ = runway_bags.type_fn()
    out = []
    for r in df.itertuples():
        g = str(r.gender or "").lower()
        if g not in ("female", "male") or r.wrapper:
            continue
        bag = typ(r.product)
        if not bag:
            continue
        d = r.d if isinstance(r.d, dt.date) else dt.date.fromisoformat(str(r.d)[:10])
        out.append({"d": d, "mkt": pp._market(r.till), "bag": bag, "units": float(r.qty or 0), "g": g})
    return out


def _buyer_slide(mkt, name, kname, blines, info, week_start, week_end):
    """E. Who buys: women vs men — Odoo's customer gender on each till order."""
    from lib import bag_gender
    m1 = week_end.replace(day=1)
    weeks = _weeks(m1, week_end)
    cat = lambda b: ((info.get(b) or {}).get("cat") or "OTHER").upper()               # noqa: E731
    by = {"female": collections.Counter(), "male": collections.Counter()}
    for x in blines:
        if x["mkt"] == mkt and m1 <= x["d"] <= week_end:
            by[x["g"]][x["bag"]] += x["units"]
    f, m = by["female"], by["male"]
    tf, tm = sum(f.values()), sum(m.values())
    slide = {"id": f"buyers-{mkt}", "kicker": f"Who buys: women vs men, {kname} ({_d(m1)} to {_d(week_end)})",
             "tone": "neutral", "insight": [], "rec": [],
             "source": "Odoo: the customer on each till order and the customer's gender (female / male; corporate left out). "
                       "Counts only, no names.", "graph": {"ok": False}}
    if not (tf or tm):
        slide["headline"] = f"No {name} sales with a customer's gender this month."
        return slide
    share_f = lambda b: f[b] / (f[b] + m[b]) * 100 if f[b] + m[b] else 0               # noqa: E731
    vol = 30 if mkt == "KE" else 4                       # a bag needs this many bags with a buyer's gender to be judged
    judged = [b for b in set(f) | set(m) if f[b] + m[b] >= vol]
    top_f = sorted((b for b in judged if f[b] > 0), key=lambda b: (-share_f(b), -f[b]))[:10]     # bags women lean to
    top_m = sorted((b for b in judged if m[b] > 0), key=lambda b: (share_f(b), -m[b]))[:10]      # bags men lean to
    both = [b for b, _ in (f + m).most_common(3)]
    row = lambda b, side: {"bag": _title(b), "units": round((f if side == "f" else m)[b]),            # noqa: E731
                           "pct": round(share_f(b) if side == "f" else 100 - share_f(b))}
    slide["graph"] = {"ok": True, "kind": "buyers", "women": [row(b, "f") for b in top_f], "men": [row(b, "m") for b in top_m]}
    wf = tf / (tf + tm) * 100
    slide["headline"] = (f"Women bought {wf:.0f}% of {name}'s bags this month ({_fmt(tf)} vs {_fmt(tm)} by men)"
                         + (f"; women lean most to {_title(top_f[0])} ({share_f(top_f[0]):.0f}% women)" if top_f else "")
                         + (f", men to {_title(top_m[0])} ({100 - share_f(top_m[0]):.0f}% men)." if top_m else "."))
    slide["insight"].append("Best sellers with both: " + ", ".join(
        f"{_title(b)} ({share_f(b):.0f}% women)" for b in both) + f"; women are {wf:.0f}% of all buyers, so a bag above "
        f"that leans to women, below it to men.")
    # the women's share week by week
    wk = []
    for k, s, e in weeks:
        a = sum(x["units"] for x in blines if x["mkt"] == mkt and s <= x["d"] <= e and x["g"] == "female")
        b = sum(x["units"] for x in blines if x["mkt"] == mkt and s <= x["d"] <= e and x["g"] == "male")
        wk.append((k, a / (a + b) * 100 if a + b else None))
    slide["insight"].append("Women's share of bags week by week: " + ", ".join(
        f"{k} {p:.0f}%" for k, p in wk if p is not None) + ".")
    # crossovers: the bag list's side vs who actually buys it (bags with 10+ buyers' bags)
    cross = []
    for b in set(f) | set(m):
        n = f[b] + m[b]
        if n < (10 if mkt == "KE" else 4):
            continue
        side = bag_gender.gender(b, cat(b))
        if side == "Male" and share_f(b) >= 50:
            cross.append((b, "women", share_f(b), n))
        elif side == "Female" and share_f(b) <= 50:
            cross.append((b, "men", 100 - share_f(b), n))
    cross.sort(key=lambda t: -t[3])
    if cross:
        slide["insight"].append("Crossovers (a bag for one side bought mostly by the other): " + ", ".join(
            f"{_title(b)} {p:.0f}% {who}" for b, who, p, _ in cross[:5]) + ".")
    even = sorted((b for b in set(f) | set(m) if f[b] + m[b] >= (20 if mkt == "KE" else 5)),
                  key=lambda b: abs(share_f(b) - 50))[:3]
    if even:
        slide["insight"].append("Closest to 50/50: " + ", ".join(f"{_title(b)} ({share_f(b):.0f}% women)" for b in even) + ".")
    if top_f:
        slide["rec"].append("Aim " + ", ".join(_title(b) for b in top_f[:3]) + " posts and ads at women: women buy "
                            + f"{share_f(top_f[0]):.0f}% or so of them.")
    if top_m:
        slide["rec"].append("Aim " + ", ".join(_title(b) for b in top_m[:3]) + " posts and ads at men: they lean most "
                            + f"to men ({100 - share_f(top_m[0]):.0f}% men for {_title(top_m[0])}).")
    if cross:
        b, who, p, _ = cross[0]
        slide["rec"].append(f"Show {_title(b)} to {who} too ({p:.0f}% of its buyers), e.g. as a gift.")
    pts = [p for _, p in wk if p is not None]
    if len(pts) >= 2 and abs(pts[-1] - pts[-2]) >= 3:
        slide["insight"].append(f"Women's share moved {pts[-2]:.0f}% → {pts[-1]:.0f}% last week.")
    slide["rec"] = slide["rec"][:3]
    if tf + tm < 100:
        slide["insight"].append(f"Only {_fmt(tf + tm)} bags with a buyer's gender this month: read the shares with care.")
    return slide


def slides(week_start: dt.date, week_end: dt.date) -> list:
    m1 = week_end.replace(day=1)
    p1 = (m1 - dt.timedelta(days=1)).replace(day=1)
    lines = _load_lines(min(p1, week_start - dt.timedelta(days=7)), week_end)
    page = _pp_page()
    info = page.get("info") or {}
    why = (page.get("why") or {}).get("monthly") or {}
    try:
        blines = _buyer_lines(m1, week_end)
    except Exception as e:                                    # noqa: BLE001
        print(f"  WARNING: buyer gender skipped: {e}")
        blines = []
    out = []
    for mkt, name in MARKETS:
        try:
            out += _market_slides(mkt, name, lines, info, why, week_start, week_end)
            if blines:
                out.append(_buyer_slide(mkt, name, KICKER_NAME.get(mkt, name), blines, info, week_start, week_end))
        except Exception as e:                                # noqa: BLE001
            print(f"  WARNING: {name} product slides skipped: {e}")
    return out
