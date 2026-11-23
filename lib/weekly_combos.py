"""lib/weekly_combos.py — the Weekly Report's combos and offers slides:
one per market (Kenya, Sinza, Uganda): running combos vs self-made combos vs power deals (listed singles outside
Kenya), week on week and month to date; then the whole of Denri's offer types.
Spec: docs/weekly-report.md › Combos and offers slides.

    slides(week_start, week_end) → [slide dicts] (the Weekly Report's shape)
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import re
import sys

from lib import paths

FX = {"KE": 1, "TZ": 25, "UG": 29}                 # local currency per KES (sql/bags_sold_total.sql)
FALL = -15                                         # % week on week that counts as a fall
PROMOTE = {"KE": 5, "TZ": 3, "UG": 3}              # a self-made pairing sold this often → consider making it official
ROW_COLOUR = {"OFF": "#94a3b8", "POWER": "#7c3aed", "COMBOS": "#2563eb", "DOW": "#ea580c", "CORP": "#0891b2",
              "MID": "#db2777", "SAMPLE": "#64748b", "GIFT": "#059669"}


def _fmt(x):
    return "—" if x is None else f"{round(x):,}"


def _pct(a, b):
    return (a - b) / b * 100 if b else None


def _signed(p):
    return "—" if p is None else f"{'+' if p >= 0 else ''}{p:.0f}%"


def _d(d):
    return f"{d.day} {d:%b}"


def _t(s):
    return re.sub(r"\s+Combo$", "", str(s).strip(), flags=re.I).title()


def _page(html, var):
    t = open(paths.html(html), encoding="utf-8").read()
    m = re.search(r"const " + var + r"\s*=\s*(\{.*?\});\s*</script>", t, re.S)
    return json.loads(m.group(1)) if m else {}


def _gen():
    gen = paths.generator()
    if gen not in sys.path:
        sys.path.insert(0, gen)


def _weeks(m1, end):
    out, s, i = [], m1, 1
    while s <= end:
        e = min(s + dt.timedelta(days=(5 - s.weekday()) % 7), end)
        out.append((i, s, e))
        s, i = e + dt.timedelta(days=1), i + 1
    return out


def _kenya(m1, week_end, smc, boo, weeks):
    """{running, self, power: {wk: units}}, {..._kes: total}, tops — Kenya."""
    _gen()
    import product_performance as pp
    from lib import db, queries
    df = db.run_query(pp.LINES_SQL, {"s": m1.isoformat(), "e": week_end.isoformat(), "excluded": queries.excluded_products()})
    if df is None:
        raise RuntimeError("Odoo unreachable")
    from lib import runway_bags
    typ = runway_bags.type_fn()
    sm_names = {str(x["name"]).strip().upper() for x in smc.get("selfMade") or []}
    anchor = m1 - dt.timedelta(days=(m1.weekday() + 1) % 7)
    w = {"running": collections.Counter(), "self": collections.Counter(), "power": collections.Counter()}
    kes = collections.Counter()
    prod = {"running": collections.defaultdict(collections.Counter), "self": collections.Counter()}
    for r in df.itertuples():
        if not r.wrapper or not r.qty or pp._market(r.till) != "KE":
            continue
        wk = (r.d - anchor).days // 7 + 1
        side = "self" if str(r.product).strip().upper() in sm_names else "running"
        w[side][wk] += float(r.qty)
        kes[side] += float(r.amount or 0)
        if side == "running":
            prod["running"][wk][r.product] += float(r.qty)
        else:                                          # the pairing by bag style, colours dropped (Sarai + Antitheft)
            parts = re.sub(r"\s+combo$", "", str(r.product).strip(), flags=re.I).split("+")
            prod["self"][" + ".join(sorted((typ(p) or p.strip()).upper() for p in parts))] += float(r.qty)
    for x in (boo.get("periods") or {}).get("monthly", {}).get("offerTypesByWeek") or []:
        n = int(re.sub(r"\D", "", x["label"]) or 0)
        p = (x.get("rows") or {}).get("POWER") or {}
        w["power"][n] += p.get("units", 0)
        if n <= len(weeks):
            kes["power"] += p.get("revenue", 0)
    deals = (smc.get("deals") or {}).get("powerDeals") or []
    return w, kes, prod, deals


def _receipts(key, m1, week_end):
    """Sinza / Uganda from receipts (lib/receipt_combos): {running, self, power(listed singles): {wk: n}}, KES."""
    _gen()
    import self_made_combos as smc_gen
    from lib import receipt_combos
    infer, _ = smc_gen.bag_classifier(set())
    s = receipt_combos.market_summary(key, m1, week_end, infer)
    if not s:
        raise RuntimeError("Odoo unreachable")
    w = {"running": collections.Counter(), "self": collections.Counter(), "power": collections.Counter()}
    kes = collections.Counter()
    for tab, side in (("running", "running"), ("selfMade", "self"), ("singlesOffer", "power")):
        for name, e in (s.get(tab) or {}).items():
            for wk, n in (e.get("weeks") or {}).items():
                w[side][int(wk)] += n
            kes[side] += e.get("revenue", 0)
    return w, kes, s


def _market_slide(mkt, name, kname, w, kes, weeks, rw, extra):
    fx = FX[mkt]
    third = "Power deals" if mkt == "KE" else "Listed single offers"
    third_unit = "bags" if mkt == "KE" else "sold"
    wk_nums = [n for n, _, _ in weeks]
    prev = rw - 1 if rw - 1 in wk_nums else None
    mtd = {k: sum(w[k][n] for n in wk_nums) for k in w}
    last = {k: w[k][rw] for k in w}
    before = {k: (w[k][prev] if prev else None) for k in w}
    combos_l, combos_p = last["running"] + last["self"], (before["running"] or 0) + (before["self"] or 0)
    rows = []
    for k, label in (("running", "Running combos"), ("self", "Self-made combos"), ("power", third)):
        rows.append([label] + [_fmt(w[k][n]) for n in wk_nums] + [_fmt(mtd[k]), f"KES {_fmt(kes[k] / fx)}",
                     _signed(_pct(last[k], before[k])) if prev else "—"])
    rows.append(["All combos"] + [_fmt(w["running"][n] + w["self"][n]) for n in wk_nums]
                + [_fmt(mtd["running"] + mtd["self"]), f"KES {_fmt((kes['running'] + kes['self']) / fx)}",
                   _signed(_pct(combos_l, combos_p)) if prev else "—"])
    slide = {"id": f"combos-{mkt}", "kicker": f"Combos and offers, {kname}: running vs self-made vs {third.lower()}",
             "tone": "neutral", "insight": [], "rec": [],
             "source": ("Odoo combo lines on the Kenya tills (self-made = the Self-made Combos page's list); power deals = "
                        "the Bags On vs Off Offer page's Power deals row." if mkt == "KE" else
                        "Odoo receipts (lib/receipt_combos, the combos page's method); listed single offers from the month's "
                        "offer list. KES = local ÷ " + str(fx) + "."),
             "graph": {"ok": True, "kind": "combos", "labels": [f"Wk {n} ({s.day}–{e.day} {e:%b})" for n, s, e in weeks],
                       "running": [round(w["running"][n]) for n in wk_nums], "self": [round(w["self"][n]) for n in wk_nums],
                       "third": [round(w["power"][n]) for n in wk_nums], "thirdLabel": third,
                       "table": {"title": f"Week on week and month to date ({_d(weeks[0][1])} to {_d(weeks[-1][2])})",
                                 "cols": ["Measure"] + [f"Wk {n}" for n in wk_nums] + ["Month", "KES month", "Week on week"],
                                 "rows": rows, "trend": [1, len(wk_nums)]}}}
    ch = _signed(_pct(combos_l, combos_p)) if prev else None
    slide["headline"] = (f"{name} sold {_fmt(combos_l)} combos last week" + (f" ({ch} on the week before)" if ch else "")
                         + f": {_fmt(last['running'])} running, {_fmt(last['self'])} self-made; "
                         + f"{third.lower()} {_fmt(last['power'])} {third_unit}"
                         + (f" ({_signed(_pct(last['power'], before['power']))})." if prev and before["power"] else "."))
    tot_c = mtd["running"] + mtd["self"]
    if tot_c:
        slide["insight"].append(f"This month {_fmt(tot_c)} combos have sold, <b>{mtd['self'] / tot_c * 100:.0f}%</b> of them self-made; "
                                f"running combos brought in KES {_fmt(kes['running'] / fx)} and self-made ones KES {_fmt(kes['self'] / fx)}.")
    if extra.get("topRun"):
        slide["insight"].append("The best running combos last week were " + ", ".join(f"{_t(n)} ({_fmt(u)})" for n, u in extra["topRun"]) + ".")
    if extra.get("topSelf"):
        slide["insight"].append("Buyers' favourite self-made pairings this month were " + ", ".join(f"{_t(n)} ({_fmt(u)})" for n, u in extra["topSelf"]) + ".")
    if extra.get("topDeal"):
        slide["insight"].append(f"The top power deal last week was {extra['topDeal'][0]}, with {_fmt(extra['topDeal'][1])} bags sold.")
    # recommendations
    pr = _pct(last["running"], before["running"]) if prev else None
    if pr is not None and pr <= FALL:
        faller = extra.get("runFaller")
        slide["rec"].append(f"Push the running combos: down {abs(pr):.0f}% last week"
                            + (f", {_t(faller[0])} fell most ({_fmt(faller[1])} → {_fmt(faller[2])})." if faller else "."))
    promo = [(n, u) for n, u in (extra.get("topSelf") or []) if u >= PROMOTE[mkt]]
    if promo:
        slide["rec"].append(f"Consider making {_t(promo[0][0])} an official combo: sold {_fmt(promo[0][1])} times as a self-made "
                            f"pairing this month.")
    pp_ = _pct(last["power"], before["power"]) if prev and before["power"] else None
    if pp_ is not None and pp_ <= FALL:
        slide["rec"].append(f"Check {third.lower()}' stock and display: down {abs(pp_):.0f}% last week.")
    slide["rec"] = slide["rec"][:3] or ["Keep the combo list as it is: running combos held up last week."]
    return slide


def _offer_mix(boo, weeks, rw):
    pm = (boo.get("periods") or {}).get("monthly") or {}
    names = {r["key"]: r["label"] for r in (pm.get("offerTypes") or {}).get("rows") or []}
    byw = {int(re.sub(r"\D", "", x["label"]) or 0): x.get("rows") or {} for x in pm.get("offerTypesByWeek") or []}
    wk_nums = [n for n, _, _ in weeks if n in byw]
    keys = [k for k in names if any((byw[n].get(k) or {}).get("revenue") for n in wk_nums)]
    rev = lambda k, n: (byw[n].get(k) or {}).get("revenue", 0)                 # noqa: E731
    units = lambda k, n: (byw[n].get(k) or {}).get("units", 0)                 # noqa: E731
    tot = {n: sum(rev(k, n) for k in keys) for n in wk_nums}
    mtd_r = {k: sum(rev(k, n) for n in wk_nums) for k in keys}
    mtd_u = {k: sum(units(k, n) for n in wk_nums) for k in keys}
    all_r = sum(mtd_r.values()) or 1
    prev = rw - 1 if rw - 1 in wk_nums else None
    order = sorted(keys, key=lambda k: -mtd_r[k])
    rows = [[names[k], _fmt(mtd_u[k]), f"KES {_fmt(mtd_r[k])}", f"{mtd_r[k] / all_r * 100:.0f}%",
             _signed(_pct(rev(k, rw), rev(k, prev))) if prev else "—"] for k in order]
    rows.append(["Total", _fmt(sum(mtd_u.values())), f"KES {_fmt(all_r)}", "100%",
                 _signed(_pct(tot.get(rw, 0), tot.get(prev, 0))) if prev else "—"])
    slide = {"id": "offer-mix", "kicker": "Offer types, all of Denri (Kenya + Sinza + Uganda)", "tone": "neutral",
             "insight": [], "rec": [], "source": "The Bags On vs Off Offer page's offer type rows per week (all three countries, KES).",
             "graph": {"ok": bool(wk_nums), "kind": "offermix", "labels": [f"Wk {n} ({s.day}–{e.day} {e:%b})" for n, s, e in weeks if n in byw],
                       "series": [{"key": k, "label": names[k], "colour": ROW_COLOUR.get(k, "#94a3b8"),
                                   "data": [round(rev(k, n)) for n in wk_nums],
                                   "units": [round(units(k, n)) for n in wk_nums]} for k in order],
                       "weekNums": wk_nums,
                       "monthTable": {"cols": ["Offer type", "Bags month", "KES month", "Share", "Week on week"],
                                      "rows": rows}}}      # kept for reference; the charts carry the month totals
    if not wk_nums:
        slide["headline"] = "No offer-type figures for this month yet."
        return slide
    off = mtd_r.get("OFF", 0) / all_r * 100
    on_keys = [k for k in ("POWER", "COMBOS", "DOW", "MID") if k in keys]
    on = sum(mtd_r[k] for k in on_keys) / all_r * 100
    slide["headline"] = (f"Month to date, {on:.0f}% of Denri's revenue came on offer and {off:.0f}% not on offer "
                         f"(KES {all_r / 1e6:.1f}M in all); last week KES {tot.get(rw, 0) / 1e6:.1f}M"
                         + (f" ({_signed(_pct(tot.get(rw, 0), tot.get(prev, 0)))} on the week before)." if prev else "."))
    if prev:
        ch = {k: rev(k, rw) - rev(k, prev) for k in keys}
        up, dn = max(ch, key=ch.get), min(ch, key=ch.get)
        slide["insight"].append(f"Last week {names[up]} rose the most (+KES {_fmt(ch[up])} on the week before) and {names[dn]} "
                                f"{'fell the most' if ch[dn] < 0 else 'rose the least'} ({'-' if ch[dn] < 0 else '+'}KES {_fmt(abs(ch[dn]))}).")
        if ch[dn] < 0:
            slide["rec"].append(f"Check {names[dn].lower()}: KES {_fmt(abs(ch[dn]))} less than the week before.")
    shares = [sum(rev(k, n) for k in on_keys) / tot[n] * 100 for n in wk_nums if tot[n]]
    slide["insight"].append("The share of revenue that came from offers was " + ", ".join(
        f"{p:.0f}% in Wk {n}" for n, p in zip(wk_nums, shares)) + ".")
    top = order[0]
    slide["insight"].append(f"So far this month the biggest offer type is {names[top]}, with KES {_fmt(mtd_r[top])} "
                            f"({mtd_r[top] / all_r * 100:.0f}% of revenue) from {_fmt(mtd_u[top])} bags.")
    if off < 40:
        slide["rec"].append(f"Watch the discount cost: only {off:.0f}% of revenue came at full price (not on offer).")
    slide["rec"] = slide["rec"][:3] or ["Keep the offer mix: no offer type fell last week."]
    return slide


def slides(week_start: dt.date, week_end: dt.date) -> list:
    m1 = week_end.replace(day=1)
    weeks = _weeks(m1, week_end)
    rw = weeks[-1][0]
    smc, boo = _page("self_made_combos.html", "SMC"), _page("bags_on_offer.html", "BOO")
    out = []
    try:
        w, kes, prod, deals = _kenya(m1, week_end, smc, boo, weeks)
        top_run = prod["running"][rw].most_common(3)
        faller = None
        if rw - 1 in prod["running"]:
            diffs = {p: prod["running"][rw][p] - prod["running"][rw - 1][p] for p in set(prod["running"][rw]) | set(prod["running"][rw - 1])}
            p = min(diffs, key=diffs.get) if diffs else None
            if p and diffs[p] < 0:
                faller = (p, prod["running"][rw - 1][p], prod["running"][rw][p])
        top_deal = None
        for d in deals:
            wks = d.get("weeks") or []
            if len(wks) >= rw and (top_deal is None or wks[rw - 1]["sold"] > top_deal[1]):
                top_deal = (d["product"], wks[rw - 1]["sold"])
        out.append(_market_slide("KE", "Kenya", "Kenya", w, kes, weeks, rw,
                                 {"topRun": top_run, "topSelf": prod["self"].most_common(3), "topDeal": top_deal, "runFaller": faller}))
    except Exception as e:                                     # noqa: BLE001
        print(f"  WARNING: Kenya combos slide skipped: {e}")
    for key, mkt, name, kname in (("sinza", "TZ", "Sinza", "Tanzania (Sinza)"), ("uganda", "UG", "Uganda", "Uganda")):
        try:
            w, kes, s = _receipts(key, m1, week_end)
            run_last = sorted(((n, e.get("weeks", {}).get(rw, 0)) for n, e in (s.get("running") or {}).items()), key=lambda t: -t[1])
            top_self = sorted(((n, e.get("count", 0)) for n, e in (s.get("selfMade") or {}).items()), key=lambda t: -t[1])[:3]
            faller = None
            if rw > 1:
                ds = [(n, e.get("weeks", {}).get(rw - 1, 0), e.get("weeks", {}).get(rw, 0)) for n, e in (s.get("running") or {}).items()]
                ds = [t for t in ds if t[2] < t[1]]
                faller = min(ds, key=lambda t: t[2] - t[1]) if ds else None
            out.append(_market_slide(mkt, name, kname, w, kes, weeks, rw,
                                     {"topRun": [t for t in run_last if t[1]][:3], "topSelf": top_self, "runFaller": faller}))
        except Exception as e:                                 # noqa: BLE001
            print(f"  WARNING: {name} combos slide skipped: {e}")
    try:
        out.append(_offer_mix(boo, weeks, rw))
    except Exception as e:                                     # noqa: BLE001
        print(f"  WARNING: offer types slide skipped: {e}")
    return out
