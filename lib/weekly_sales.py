"""lib/weekly_sales.py — the Weekly Report's Sales deck slides that the Marketing deck doesn't have:
Weekly Performance, Why Did We Move? (week on week vs month on month), What if…, Price per Bag, Corporate by Client.
All from the built Current Performance page (PERF / PROJ), so the figures match it; no Odoo query.
Spec: docs/weekly-report.md › Two reports in one page.

    slides(week_start, week_end) → [slide dicts] (the Weekly Report's shape; deck = sales)
"""
from __future__ import annotations

import collections
import datetime as dt
import json
import re

from lib import paths

EXTRA = (100, 200, 300, 500)        # What if: extra bags a day for the days left


def _fmt(x):
    return "—" if x is None else f"{round(x):,}"


def _pct(a, b):
    return (a - b) / b * 100 if b else None


def _signed(p):
    return "—" if p is None else f"{'+' if p >= 0 else ''}{p:.0f}%"


def _n(x):
    if x is None or x == "":
        return None
    try:
        return float(str(x).replace(",", "").replace("%", "").replace("KES", "").strip())
    except ValueError:
        return None


def _kes(x):
    return "—" if x is None else (f"KES {x / 1e6:.1f}M" if abs(x) >= 1e6 else f"KES {round(x):,}")


class _Page:
    def __init__(self):
        self.t = open(paths.html("current_performance.html"), encoding="utf-8").read()
        self.proj = self.t[self.t.index("<!-- PROJ_DATA_START -->"):] if "<!-- PROJ_DATA_START -->" in self.t else ""

    def get(self, name, proj=False):
        m = re.search(r"^\s*" + re.escape(name) + r":\s*(.+?),?\s*$", self.proj if proj else self.t, re.M)
        try:
            return json.loads(m.group(1)) if m else None
        except ValueError:
            return None


def _bags_between(s, e, tills_only=False):
    """Shop tills + Corporate-app bags between s and e (the Weekly Performance rules); None if Odoo is down.
    tills_only: shop tills alone (a one-off corporate payment mustn't drive a forecast)."""
    from lib import db, queries
    d = db.run_query(queries.BAGS_SOLD_DAILY, {"start_date": s.isoformat(), "end_date": e.isoformat(),
                                               "excluded": queries.excluded_products()})
    if d is None:
        return None
    if tills_only:
        return round(float(d["bags"].sum() if len(d) else 0))
    c = db.run_query(queries.CORPORATE_BAGS, {"start_date": s.isoformat(), "end_date": e.isoformat()})
    corp = float(c.iloc[0]["bags"] or 0) if c is not None and len(c) else 0
    return round(float(d["bags"].sum() if len(d) else 0) + corp)


def _same_days_last_month(s, e):
    """The same days of the month before (1–7 Nov → 1–7 Oct), clipped to that month."""
    p_end = s.replace(day=1) - dt.timedelta(days=1)
    a = min(s.day, p_end.day)
    b = min(e.day, p_end.day)
    return p_end.replace(day=a), p_end.replace(day=b)


def _weekly(pg, week_start, week_end):
    hist = pg.get("weeklyHistory", True) or []
    month = f"{week_end:%b}"
    weeks = [w for w in hist if w.get("month") == month and w.get("weekStart", "") <= week_start.isoformat()]
    floor = _n(pg.get("bareMinimum", True))
    prev = pg.get("cpPrevWeekly") or []
    beat = (pg.get("beats", True) or {}).get("weekly") or {}
    rows, labels = [], []
    for i, w in enumerate(weeks):
        wk_pct = (w.get("salesPct") or 0) - (w.get("prevSalesPct") or 0)
        pm = next((p for p in prev if p.get("label") == w["label"]), None)
        vs = (w.get("weeklySales") or 0) - floor if floor else None
        rows.append([w["label"], _fmt(w.get("weeklySales")), _fmt(w.get("corporateBags")), f"{wk_pct:.1f}%",
                     f"{w.get('salesPct', 0):.1f}%", (f"{'+' if vs >= 0 else ''}{_fmt(vs)}" if vs is not None else "—"),
                     f"{pm['pct']:.1f}%" if pm else "—"])
        labels.append(f"{w['label']} ({dt.date.fromisoformat(w['weekStart']).day} {dt.date.fromisoformat(w['weekStart']):%b})")
    # October beside November: the same days of the month before, and next week's forecast from how it moved then
    oct_vals, fc = [], None
    try:
        for w in weeks:
            ws = dt.date.fromisoformat(w["weekStart"])
            we = min(ws + dt.timedelta(days=6), week_end)
            a, b = _same_days_last_month(max(ws, week_end.replace(day=1)), we)
            oct_vals.append({"label": f"{a.day}–{b.day} {a:%b}", "bags": _bags_between(a, b)})
        if weeks:
            nxt_s = week_end + dt.timedelta(days=1)
            m_end = (week_end.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)
            nxt_e = min(nxt_s + dt.timedelta(days=6), m_end)
            if nxt_s <= m_end:
                pa, pb = _same_days_last_month(nxt_s, nxt_e)
                ca, cb = _same_days_last_month(week_start, week_end)
                prev_next, prev_cur = _bags_between(pa, pb, True), _bags_between(ca, cb, True)   # tills only
                last = weeks[-1].get("weeklySales") or 0
                nxt_hist = next((w for w in hist if w.get("weekStart") == nxt_s.isoformat()), None)
                if prev_next and prev_cur:
                    # a shorter next week (month end) is scaled by its days, so the forecast is for the days it has
                    ratio = prev_next / prev_cur
                    fc = {"label": f"Wk {len(weeks) + 1} forecast ({nxt_s.day}–{nxt_e.day} {nxt_e:%b})",
                          "bags": round(last * ratio), "ratio": round((ratio - 1) * 100, 1),
                          "octFrom": f"{ca.day}–{cb.day} {ca:%b}", "octTo": f"{pa.day}–{pb.day} {pa:%b}",
                          "octCur": prev_cur, "octNext": prev_next, "soFar": (nxt_hist or {}).get("weeklySales"),
                          "days": (nxt_e - nxt_s).days + 1}
    except Exception as e:                                       # noqa: BLE001
        print(f"  WARNING: October comparison skipped: {e}")
        oct_vals, fc = [], None
    for i, r in enumerate(rows):
        o = oct_vals[i]["bags"] if i < len(oct_vals) else None
        r.insert(6, f"{_fmt(o)} ({oct_vals[i]['label']})" if o is not None else "—")
    s = {"id": "weekly-perf", "kicker": "Weekly Performance, Week 1 to latest", "tone": beat.get("tone", "neutral"),
         "headline": beat.get("headline") or "Weekly sales this month.", "insight": [], "rec": [],
         "source": "The Current Performance page's Weekly Performance (Odoo tills + the Corporate app, Sun to Sat weeks).",
         "graph": {"ok": bool(weeks), "kind": "weekly", "labels": labels,
                   "pos": [round(w.get("posBags") or 0) for w in weeks], "corp": [round(w.get("corporateBags") or 0) for w in weeks],
                   "floor": round(floor) if floor else None,
                   "oct": [o["bags"] for o in oct_vals], "octLabels": [o["label"] for o in oct_vals], "forecast": fc,
                   "table": {"title": "Week by week (% of target = the week's bags against the month's bag target)",
                             "cols": ["Week", "Bags", "Corporate", "% of target", "Cumulative", "vs the floor", "Same days last month",
                                      "Last month same week (% of its target)"],
                             "rows": rows, "trend": [1, 1]}}}
    if weeks:
        best = max(weeks, key=lambda w: w.get("weeklySales") or 0)
        s["insight"].append(f"The best week was {best['label']} with <b>{_fmt(best['weeklySales'])}</b> bags; so far the month has reached "
                            f"<b>{weeks[-1].get('salesPct', 0):.1f}%</b> of the bag target ({_fmt(weeks[-1].get('salesBags'))} bags).")
        if floor:
            short = [w for w in weeks if (w.get("weeklySales") or 0) < floor]
            s["insight"].append(f"To reach the target each week needs {_fmt(floor)} bags (the target split over the month's weeks). "
                                + (f"{len(short)} of {len(weeks)} weeks fell short; last week was {_fmt(floor - (weeks[-1].get('weeklySales') or 0))} "
                                   f"bags under it." if short else "Every week cleared it."))
        if len(weeks) >= 2:
            a, b = weeks[-1], weeks[-2]
            s["insight"].append(f"Last week Denri sold {_fmt(a.get('weeklySales'))} bags, against {_fmt(b.get('weeklySales'))} the week before "
                                f"({_signed(_pct(a.get('weeklySales') or 0, b.get('weeklySales') or 0))}).")
        if fc:
            up = fc["ratio"] >= 0
            s["insight"].append(f"Next week should reach about <b>{_fmt(fc['bags'])}</b> bags ({'+' if up else ''}{fc['ratio']}% on last week), "
                                f"because last month the shop tills went from {_fmt(fc['octCur'])} to {_fmt(fc['octNext'])} between {fc['octFrom']} and "
                                f"{fc['octTo']} (corporate is left out, as one big payment would swing it)"
                                + (f"; {_fmt(fc['soFar'])} have sold so far." if fc.get("soFar") else "."))
            if floor:
                gap = floor * fc["days"] / 7 - fc["bags"]
                if gap > 0:
                    s["rec"].append(f"Push now: if next week moves as last month did, it ends near {_fmt(fc['bags'])} bags, "
                                    f"{_fmt(gap)} short of the floor.")
                elif up:
                    s["rec"].append(f"Hold the pace: last month gained at this point, so next week could reach {_fmt(fc['bags'])}.")
        if beat.get("rec"):
            s["rec"].append(beat["rec"])
        s["rec"] = s["rec"][:3]
    return s


def _why_moved(pg, week_start, week_end):
    wm = pg.get("whyMoved", True) or {}
    weeks = wm.get("weeks") or []
    cur = next((w for w in weeks if w.get("start") == week_start.isoformat()), None)
    i = weeks.index(cur) if cur in weeks else -1
    prev = weeks[i - 1] if i > 0 else None

    def regions(w):
        r, shops = collections.Counter(), {}
        for row in w.get("rows") or []:
            r[row[0]] += row[2]
            shops[row[1]] = (row[0], row[2])
        return r, shops
    wow, mom_rows, shop_moves, shop_region = [], [], [], {}
    head_w = head_m = None
    if cur and prev:
        rc, sc = regions(cur)
        rp, sp = regions(prev)
        tc, tp = sum(rc.values()), sum(rp.values())
        days_eff = round(tp / prev["days"] * (cur["days"] - prev["days"])) if prev["days"] and cur["days"] != prev["days"] else 0
        if days_eff:
            wow.append({"label": "Selling days", "delta": days_eff})
        for reg in sorted(set(rc) | set(rp), key=lambda r: -(rc[r] - rp[r])):
            wow.append({"label": reg, "delta": rc[reg] - rp[reg], "then": rp[reg], "now": rc[reg]})
        shop_moves = sorted(((sh, sc.get(sh, (None, 0))[1] - sp.get(sh, (None, 0))[1]) for sh in set(sc) | set(sp)), key=lambda t: t[1])
        shop_region = {sh: (sc.get(sh) or sp.get(sh))[0] for sh in set(sc) | set(sp)}
        head_w = (tp, tc, prev["label"], cur["label"])
    mom = (wm.get("mom") or {}).get("with") or {}
    if mom:
        if mom.get("daysEffect"):
            mom_rows.append({"label": "Selling days", "delta": mom["daysEffect"]})
        for r in sorted(mom.get("regions") or [], key=lambda r: -r["delta"]):
            mom_rows.append({"label": r["region"], "delta": r["delta"], "then": r["then"], "now": r["now"],
                             "shops": sorted(r.get("shops") or [], key=lambda x: -abs(x["delta"]))[:2]})
        head_m = (mom["then"]["bags"], mom["now"]["bags"], mom["then"]["range"], mom["now"]["range"])
    # every week of the month (and the week before Wk 1, for its growth): bags per region
    m_weeks = [w for w in weeks if w.get("start", "")[:7] == week_end.isoformat()[:7] and w.get("start", "") <= week_end.isoformat()]
    k0 = weeks.index(m_weeks[0]) if m_weeks else -1
    base_w = weeks[k0 - 1] if k0 > 0 else None
    series, all_regions = [], collections.Counter()
    for w in ([base_w] if base_w else []) + m_weeks:
        r, _ = regions(w)
        series.append({"label": w["label"].replace(f" {week_end:%b}", ""), "days": w.get("days"), "regions": dict(r),
                       "total": sum(r.values()), "base": w is base_w})
        if w is not base_w:
            all_regions.update(r)
    region_order = [r for r, _ in all_regions.most_common()]
    s = {"id": "why-moved", "kicker": "Why Did We Move? Week on week vs month on month", "tone": "neutral", "insight": [], "rec": [],
         "source": "The Current Performance page's Why Did We Move? (all shops, every market, with bulk orders; its own week rules and "
                   "date fixes, e.g. Nyeri's opening, so a week can differ from Weekly Performance).",
         "graph": {"ok": bool(wow or mom_rows), "kind": "whymoved", "wow": wow, "mom": mom_rows,
                   "weeks": series, "regionOrder": region_order,
                   "wowTitle": f"Week on week: {head_w[2]} → {head_w[3]}" if head_w else "Week on week",
                   "momTitle": f"Month on month: {head_m[2]} → {head_m[3]}" if head_m else "Month on month"}}
    parts = []
    if head_w:
        tp, tc = head_w[0], head_w[1]
        parts.append(f"week on week {_fmt(tp)} → {_fmt(tc)} bags ({_signed(_pct(tc, tp))})")
    if head_m:
        parts.append(f"month on month {_fmt(head_m[0])} → {_fmt(head_m[1])} ({_signed(_pct(head_m[1], head_m[0]))})")
    s["headline"] = ("Denri moved " + " and ".join(parts) + "." if parts else "No week-on-week or month-on-month figures yet.")
    wk_tot = [x for x in series if not x["base"]]
    if wk_tot:
        s["insight"].insert(0, "Denri sold " + ", ".join(f"{_fmt(x['total'])} bags in {x['label']}" for x in wk_tot)
                            + (f", after {_fmt(series[0]['total'])} in the week before Wk 1" if series and series[0]["base"] else "") + ".")
    regs_w = [r for r in wow if r["label"] != "Selling days"]
    if regs_w:
        up, dn = regs_w[0], regs_w[-1]
        s["insight"].append(f"On the week before, {up['label']} rose the most ({'+' if up['delta'] >= 0 else ''}{_fmt(up['delta'])} bags) "
                            f"and {dn['label']} fell the most ({'+' if dn['delta'] >= 0 else ''}{_fmt(dn['delta'])}).")
        if shop_moves:
            falls = [t for t in shop_moves if t[1] < 0][:2]
            rises = [t for t in reversed(shop_moves) if t[1] > 0][:2]
            if falls or rises:
                s["insight"].append("The shops behind those moves were " + ", ".join(f"{sh} ({'+' if d >= 0 else ''}{_fmt(d)})" for sh, d in rises + falls) + ".")
        if dn["delta"] < 0:                          # the falling region's own shops that fell most
            fall_shops = [sh for sh, d in shop_moves if d < 0 and shop_region.get(sh) == dn["label"]][:2]
            s["rec"].append(f"Check stock, staff and offers at {' and '.join(fall_shops) if fall_shops else dn['label']}: "
                            f"{dn['label']} fell most last week.")
        if up["delta"] > 0:
            rise_shops = [sh for sh, d in reversed(shop_moves) if d > 0 and shop_region.get(sh) == up["label"]][:2]
            s["rec"].append(f"Copy what {' and '.join(rise_shops) if rise_shops else up['label']} did: {up['label']} rose most.")
    regs_m = [r for r in mom_rows if r["label"] != "Selling days"]
    if regs_m:
        top = regs_m[0]
        sh = ", ".join(f"{x['shop']} {'+' if x['delta'] >= 0 else ''}{_fmt(x['delta'])}" for x in top.get("shops") or [])
        s["insight"].append(f"Against the same days last month, {top['label']} added the most ({'+' if top['delta'] >= 0 else ''}{_fmt(top['delta'])} bags"
                            + (f", from {sh}" if sh else "") + f"), and {regs_m[-1]['label']} changed the least "
                            f"({'+' if regs_m[-1]['delta'] >= 0 else ''}{_fmt(regs_m[-1]['delta'])}).")
    s["rec"] = s["rec"][:3]
    return s


def _why_shops(pg, week_start, week_end):
    """Why Did We Move? second segment: the shops inside each region (docs/weekly-report.md › Why Did We Move, shops):
    each Sun-Sat week of the month, week on week and month on month, so a region's rise or fall shows its shops."""
    wm = pg.get("whyMoved", True) or {}
    weeks = wm.get("weeks") or []
    m_weeks = [w for w in weeks if w.get("start", "")[:7] == week_end.isoformat()[:7] and w.get("start", "") <= week_end.isoformat()]
    if not m_weeks:
        raise ValueError("no weeks this month")
    k0 = weeks.index(m_weeks[0])
    prev_w = weeks[weeks.index(m_weeks[-1]) - 1] if weeks.index(m_weeks[-1]) > 0 else None
    def by_shop(w):
        return {row[1]: (row[0], row[2]) for row in (w.get("rows") or [])} if w else {}
    wk = [by_shop(w) for w in m_weeks]
    pv = by_shop(prev_w)
    b0 = by_shop(weeks[k0 - 1]) if k0 > 0 else {}          # the week before Wk 1: Wk 1's colour compares with it
    mom = {}
    for r in ((wm.get("mom") or {}).get("with") or {}).get("regions") or []:
        mom[r["region"]] = r
        for x in r.get("shops") or []:
            mom[("shop", x["shop"])] = x
    shop_reg = {}
    for d in wk + [pv]:
        for sh, (reg, _) in d.items():
            shop_reg.setdefault(sh, reg)
    regions = {}
    for sh, reg in shop_reg.items():
        if not sh:
            sh_name = reg
        else:
            sh_name = sh
        weeks_b = [d.get(sh, (reg, 0))[1] for d in wk]
        wow = weeks_b[-1] - pv.get(sh, (reg, 0))[1] if prev_w else None
        m = mom.get(("shop", sh))
        regions.setdefault(reg, []).append({"shop": sh_name, "weeks": weeks_b, "wow": wow,
                                            "base": b0.get(sh, (reg, 0))[1] if b0 else None,
                                            "mom": m["delta"] if m else None, "momThen": m["then"] if m else None,
                                            "momNow": m["now"] if m else None})
    out = []
    for reg, shops in regions.items():
        if len(shops) == 1 and (shops[0]["shop"] in (reg, "", None)):
            shops_list = []                                  # Online, Corporate: the region is its own single "shop"
        else:
            shops_list = sorted(shops, key=lambda x: -(x["wow"] or 0))
        tot = [sum(x["weeks"][i] for x in shops) for i in range(len(wk))]
        wow = sum((x["wow"] or 0) for x in shops) if prev_w else None
        mr = mom.get(reg)
        out.append({"region": reg, "weeks": tot, "wow": wow, "mom": mr["delta"] if mr else None,
                    "base": sum(x["base"] or 0 for x in shops) if b0 else None,
                    "momThen": mr["then"] if mr else None, "momNow": mr["now"] if mr else None, "shops": shops_list})
    out.sort(key=lambda r: -(r["wow"] or 0))
    labels = [w["label"].replace(f" {week_end:%b}", "") for w in m_weeks]
    s = {"id": "why-shops", "kicker": "Why Did We Move? Shops inside each region", "tone": "neutral", "insight": [], "rec": [],
         "source": "The Current Performance page's Why Did We Move? (shop rows per week, bulk orders in; month on month = "
                   "its same-days comparison).",
         "graph": {"ok": bool(out), "kind": "whyshops", "weekLabels": labels, "regions": out,
                   "momTitle": ((wm.get("mom") or {}).get("with") or {}).get("now", {}).get("range", "")}}
    up = [r for r in out if (r["wow"] or 0) > 0]
    dn = [r for r in out if (r["wow"] or 0) < 0]
    def drivers(r, sign):
        xs = [x for x in r["shops"] if x["wow"] and (x["wow"] > 0) == (sign > 0)]
        xs.sort(key=lambda x: -abs(x["wow"]))
        return ", ".join(f"{x['shop']} {'+' if x['wow'] >= 0 else ''}{_fmt(x['wow'])}" for x in xs[:3])
    if up:
        r = up[0]
        s["headline"] = (f"{r['region']} rose most last week ({'+' if r['wow'] >= 0 else ''}{_fmt(r['wow'])} bags)"
                         + (f", driven by {drivers(r, 1)}" if drivers(r, 1) else "")
                         + (f"; {dn[-1]['region']} fell most ({_fmt(dn[-1]['wow'])})" + (f", led by {drivers(dn[-1], -1)}" if drivers(dn[-1], -1) else "") if dn else "")
                         + ".")
    else:
        s["headline"] = "No region rose last week."
    for r in out:
        if r["shops"] and r["wow"]:
            mixed = [x for x in r["shops"] if x["wow"] and (x["wow"] > 0) != (r["wow"] > 0)]
            if mixed:
                s["insight"].append(f"<b>{r['region']}</b> {'rose' if r['wow'] >= 0 else 'fell'} {_fmt(abs(r['wow']))} bags in total, but its "
                                    f"shops went different ways: " + ", ".join(f"{x['shop']} {'+' if x['wow'] >= 0 else ''}{_fmt(x['wow'])}"
                                                                              for x in r["shops"] if x["wow"]) + ".")
    s["insight"] = s["insight"][:3]
    mom_up = sorted([x for r in out for x in r["shops"] if x["mom"] is not None], key=lambda x: -x["mom"])
    if mom_up:
        s["insight"].append("Against the same days last month, the shops that moved most were " + ", ".join(
            f"{x['shop']} {'+' if x['mom'] >= 0 else ''}{_fmt(x['mom'])}" for x in mom_up[:2] + mom_up[-2:]) + ".")
    falls = sorted([(x, r["region"]) for r in out for x in r["shops"] if (x["wow"] or 0) < 0], key=lambda t: t[0]["wow"])
    for x, reg in falls[:2]:
        s["rec"].append(f"{x['shop']} ({reg}) fell {_fmt(-x['wow'])} bags last week ({_fmt(x['weeks'][-2] if len(x['weeks']) > 1 else 0)}"
                        f" → {_fmt(x['weeks'][-1])}): check its stock, staff and offers this week.")
    rises = sorted([(x, r["region"]) for r in out for x in r["shops"] if (x["wow"] or 0) > 0], key=lambda t: -t[0]["wow"])
    if rises:
        x, reg = rises[0]
        s["rec"].append(f"Share what {x['shop']} ({reg}) did (+{_fmt(x['wow'])} last week) with the other {reg} shops.")
    s["rec"] = s["rec"][:3]
    return s


def _what_if(pg):
    pace = pg.get("pace", True) or {}
    target = _n(pg.get("totalTarget", True))
    fc_pct = _n(pg.get("forecastedProjection", True))
    rev_fc = _n(pg.get("forecastedRevenue", True))
    rev_t = _n(pg.get("revenueTarget", True))
    ppb = ((pg.get("priceMix", True) or {}).get("actualPpb")) or 0
    left = pace.get("left") or 0
    base = round(target * fc_pct / 100) if target and fc_pct else None
    s = {"id": "what-if", "kicker": "What if… the rest of the month", "tone": "neutral", "insight": [], "rec": [],
         "source": "The Current Performance page: Forecasted projection, the pace's days left and this month's price per bag.",
         "graph": {"ok": False}}
    if not (base and target and left):
        s["headline"] = "Not enough figures for the what-if yet."
        return s
    scen = [{"label": "At the current pace", "bags": base, "extra": 0}]
    for e in EXTRA:
        scen.append({"label": f"+{e} bags a day", "bags": base + e * left, "extra": e})
    for x in scen:
        x["pct"] = round(x["bags"] / target * 100, 1)
        x["rev"] = (rev_fc or 0) + x["extra"] * left * ppb
        x["revPct"] = round(x["rev"] / rev_t * 100, 1) if rev_t else None
    need = max(target - base, 0) / left
    so = pace.get("soFar") or {}
    sold = (so.get("bags") or 0) + (so.get("corpBags") or 0)
    done = pace.get("done") or 0
    rate_so_far = sold / done if done else None
    rate_rest = (base - sold) / left if left else None          # the forecast's own pace for the days left
    for x in scen:
        x["rate"] = round((rate_rest or 0) + x["extra"])
        x["label"] = (f"Current pace ({_fmt(rate_rest)} a day)" if not x["extra"] else
                      f"+{x['extra']} a day ({_fmt(rate_rest)} → {_fmt(rate_rest + x['extra'])})")
    s["graph"] = {"ok": True, "kind": "whatif", "rows": scen, "target": round(target), "need": round(need), "left": left,
                  "rateRest": round(rate_rest or 0), "rateSoFar": round(rate_so_far or 0)}
    s["headline"] = (f"At the current pace (about {_fmt(rate_rest)} bags a day) the month ends near {_fmt(base)} bags "
                     f"({scen[0]['pct']:.0f}% of {_fmt(target)}); reaching 100% takes {_fmt(need)} more a day, "
                     f"{_fmt(rate_rest + need)} a day for the {left} days left.")
    s["insight"].append(f"So far Denri sells {_fmt(rate_so_far)} bags a day ({_fmt(sold)} in {done} days), and the forecast expects "
                        f"about {_fmt(rate_rest)} a day for the last {left} days, following the weekday pattern; so \"+100 a day\" "
                        f"means {_fmt(rate_rest)} becomes {_fmt(rate_rest + 100)} a day.")
    s["insight"].append("Each extra 100 bags a day adds " + f"{_fmt(100 * left)} bags by month end ({100 * left / target * 100:.1f} points "
                        f"of the target) and {_kes(100 * left * ppb)} at KES {_fmt(ppb)} a bag.")
    reach = next((x for x in scen if x["pct"] >= 100), None)
    s["insight"].append(("A lift of " + reach["label"] + " would reach the target." if reach else
                         f"Even {EXTRA[-1]} more bags a day would end the month at {scen[-1]['pct']:.0f}%, so the target is out of reach this month."))
    s["insight"].append(f"At the current pace revenue reaches {_kes(scen[0]['rev'])}, {scen[0]['revPct']}% of the {_kes(rev_t)} target.")
    beat = (pg.get("beats", True) or {}).get("summary") or {}
    if beat.get("rec"):
        s["rec"].append(beat["rec"])
    s["rec"].append(f"Set a realistic lift with the shops: +200 a day ({scen[2]['pct']:.0f}%) is "
                    f"{_fmt(200 * left)} more bags by month end.")
    return s


def _price(pg):
    pm = pg.get("priceMix", True) or {}
    beat = (pg.get("beats", True) or {}).get("price") or {}
    tgt, act, gap = pm.get("targetPpb"), pm.get("actualPpb"), pm.get("gapPct")
    tot = pm.get("total") or {}
    rev_t = pm.get("revenueTarget")
    still = (rev_t - tot["kes"]) if rev_t and tot.get("kes") is not None else None
    bags_need = still / act if still and act else None
    rows = [r for r in ((pm.get("offerMix") or {}).get("rows") or [])     # bag sales only: gift bags and samples aren't
            if r.get("ppb") and r.get("key") not in ("GIFT", "SAMPLE")]     # sold at the target price
    OFFERS = ("POWER", "COMBOS", "DOW", "MID")          # the offer types the committee chooses and runs
    for r in rows:
        # Mid-month offers keep their bags under parts (timed offers, new products, listed singles): count those too
        src = (r.get("items") or []) + [x for pt in (r.get("parts") or []) for x in (pt.get("items") or [])]
        it = [x for x in src if x.get("gapPct") is not None]
        r["_n"], r["_ok"] = len(it), sum(1 for x in it if x["gapPct"] >= 0)
    offer_rows = [r for r in rows if r.get("key") in OFFERS]
    types_ok = [r for r in offer_rows if (r.get("ppb") or 0) >= (tgt or 0)]
    items_n = sum(r["_n"] for r in offer_rows)
    items_ok = sum(r["_ok"] for r in offer_rows)
    s = {"id": "price", "kicker": "Price per Bag: operating above the target price", "insight": [], "rec": [],
         "tone": "good" if (gap or 0) > 0 else "bad",
         "source": "The Current Performance page's Price per Bag (single bags and combos this month, after discounts).",
         "graph": {"ok": bool(rows), "kind": "price", "target": tgt, "actual": act, "gap": gap,
                   "rows": [{"label": r["label"], "ppb": r["ppb"], "gap": r.get("gapPct"), "bags": r.get("bags"),
                             "effect": r.get("effectKes"), "offer": r.get("key") in OFFERS,
                             "n": r["_n"], "ok": r["_ok"]} for r in rows],
                   "working": {"types": len(types_ok), "typesN": len(offer_rows), "items": items_ok, "itemsN": items_n},
                   "total": None}}
    s["headline"] = (f"Bags sell at KES {_fmt(act)} against the KES {_fmt(tgt)} target price ({'+' if (gap or 0) >= 0 else ''}{gap}%), "
                     f"so revenue runs {'ahead of' if (gap or 0) >= 0 else 'behind'} bags: {pm.get('revPct')}% of the revenue target "
                     f"vs {pm.get('bagsPct')}% of the bag target.") if tgt and act else "No price-per-bag figures yet."
    if tgt and act:
        s["insight"].append(f"The target price is KES {_fmt(tgt)} a bag (the {_kes(rev_t)} revenue target divided by the bag target); bags "
                            f"actually sell at KES {_fmt(act)}, KES {_fmt(abs(act - tgt))} {'more' if act >= tgt else 'less'} than the targets assume.")
    if offer_rows:
        ok_names = ", ".join(r["label"] for r in types_ok) or "none"
        s["insight"].insert(0, f"<b>Offers working, two ways.</b> By offer type: <b>{len(types_ok)} of {len(offer_rows)}</b> types "
                            f"({ok_names}) average at or above KES {_fmt(tgt)} a bag."
                            + (f" Bag by bag: those {len(offer_rows)} types held <b>{items_n}</b> bags and combos on offer this month; "
                               f"<b>{items_ok}</b> of them ({items_ok / items_n * 100:.0f}%) sold at or above KES {_fmt(tgt)} a bag, "
                               f"{items_n - items_ok} sold below. A type can pass on average while most of its bags sell below "
                               f"the target, because a few big sellers carry it." if items_n else ""))
        below = [r["label"] for r in offer_rows if r not in types_ok]
        if below:
            s["rec"].insert(0, f"Review {', '.join(below)}: below the KES {_fmt(tgt)} target price this month.")
    if bags_need:
        s["insight"].append(f"To bring in the {_kes(still)} still needed, Denri must sell <b>{_fmt(bags_need)}</b> more bags at KES {_fmt(act)} a bag.")
    eff = [r for r in rows if r.get("effectKes") is not None]
    if eff:
        lift = max(eff, key=lambda r: r["effectKes"])
        drag = min(eff, key=lambda r: r["effectKes"])
        s["insight"].append(f"{lift['label']} lifts revenue the most: it brings in {_kes(lift['effectKes'])} more by month end than the target "
                            f"price expects. {drag['label']} drags it the most: {_kes(abs(drag['effectKes']))} "
                            f"{'less' if drag['effectKes'] < 0 else 'more'} than the target price expects.")
    if beat.get("rec"):
        s["rec"].append(beat["rec"])
    if (gap or 0) > 0:
        s["rec"].append(f"Hold the prices that beat the target: {', '.join(r['label'] for r in rows if (r.get('gapPct') or 0) > 0) or 'the full-price bags'}.")
    return s


def _gone(pg):
    """Share of the month gone (the pace's days done ÷ days in the month), for 'on pace' colours."""
    pace = pg.get("pace", True) or {}
    d, left = pace.get("done") or 0, pace.get("left") or 0
    return round(d / (d + left) * 100) if d + left else None


def _corporate(pg):
    cc = pg.get("corporateClients") or []
    tgt = (pg.get("corporateTarget") or {}).get("kes")
    beat = pg.get("corporateBeat") or {}
    rows = []
    for c in cc:
        open_q = sum(int(_n(q.get("bags")) or 0) for q in c.get("quotes") or []
                     if not q.get("invoice") and str(q.get("status", "")).lower() not in ("cancel", "cancelled", "declined"))
        owed = max((c.get("agreedKes") or 0) - (c.get("receivedKes") or 0), 0)
        rows.append({"client": c.get("client"), "sold": c.get("sold") or 0, "open": open_q, "kes": c.get("receivedKes") or 0, "owed": owed})
    rows.sort(key=lambda r: (-(r["sold"] + r["open"]), -r["sold"]))       # sold + open quotes: the big quotes show too
    sold = sum(r["sold"] for r in rows)
    kes = sum(r["kes"] for r in rows)
    open_b = sum(r["open"] for r in rows)
    sc = pg.get("shopCorporate") or {}
    shop_rows = []
    for r in sc.get("rows") or []:
        shop_rows.append({"client": r.get("client"), "sold": r.get("bags") or 0,
                          "open": max((r.get("quotedBags") or 0) - (r.get("bags") or 0), 0),
                          "kes": r.get("paidKes") or 0, "owed": r.get("balance") or 0, "shop": r.get("hunted") or ""})
    shop_rows.sort(key=lambda r: (-(r["sold"] + r["open"]), -r["owed"]))
    s = {"id": "corporate", "kicker": "Corporate by Client: Corporate app and shops", "tone": beat.get("tone", "neutral"),
         "headline": beat.get("headline") or "Corporate sales this month.", "insight": [], "rec": [],
         "source": "The Current Performance page's Corporate by Client (the Corporate app: quotes, invoices, payments).",
         "graph": {"ok": bool(rows), "kind": "corporate",
                   "rows": [r for r in rows if r["sold"] or r["open"]][:12],
                   "strip": {"sold": sold, "kes": kes, "tgt": tgt, "open": open_b, "owed": sum(r["owed"] for r in rows),
                             "gone": _gone(pg)},
                   "shops": shop_rows[:10],
                   "shopStrip": {"sold": sum(r["sold"] for r in shop_rows), "kes": sum(r["kes"] for r in shop_rows),
                                 "owed": sum(r["owed"] for r in shop_rows), "clients": len(shop_rows)}}}
    # money first: what Denri has collected and what is still owed, Corporate app and shops
    app_owed = sum(r["owed"] for r in rows)
    shop_paid = sum(r["kes"] for r in shop_rows)
    shop_owed = sum(r["owed"] for r in shop_rows)
    s["insight"].append(f"Denri has <b>collected</b> {_kes(kes + shop_paid)} from corporate clients: {_kes(kes)} through the Corporate app"
                        + (f" and {_kes(shop_paid)} at the shops." if shop_rows else "."))
    owers = sorted([r for r in rows if r["owed"]] + [r for r in shop_rows if r["owed"]], key=lambda r: -r["owed"])[:4]
    if app_owed or shop_owed:
        s["insight"].append(f"Clients <b>still owe</b> {_kes(app_owed + shop_owed)} ({_kes(app_owed)} on the Corporate app"
                            + (f" and {_kes(shop_owed)} at the shops" if shop_rows else "") + "), mostly "
                            + ", ".join(f"{r['client']} ({_kes(r['owed'])})" for r in owers) + ".")
    top = sorted((r for r in rows if r["sold"]), key=lambda r: -r["sold"])[:3]
    if top:
        s["insight"].append("The biggest clients this month were " + ", ".join(f"{r['client']} ({_fmt(r['sold'])} bags)" for r in top) + ".")
    if tgt:
        s["insight"].append(f"The {_kes(kes)} collected through the Corporate app is {kes / tgt * 100:.0f}% of the {_kes(tgt)} corporate target.")
    opens = sorted((r for r in rows if r["open"]), key=lambda r: -r["open"])[:3]
    if opens:
        s["insight"].append(f"{_fmt(open_b)} bags are quoted but not invoiced yet, mostly for " + ", ".join(f"{r['client']} ({_fmt(r['open'])})" for r in opens) + ".")
    owes = []
    if shop_rows:
        s["headline"] = (s["headline"].rstrip(".") + f"; at the shops, {_fmt(sum(r['sold'] for r in shop_rows))} bags paid by "
                         f"Corporate-team clients and {_kes(sum(r['owed'] for r in shop_rows))} still owed.")
        by_shop = sc.get("shops") or []
        s["insight"].append(f"At the shops, {len(shop_rows)} Corporate-team clients paid for {_fmt(sum(r['sold'] for r in shop_rows))} bags"
                            + (" (" + ", ".join(f"{_fmt(x['bags'])} at {x['shop']}" for x in by_shop if x.get("bags")) + ")" if by_shop else "") + ".")
        owed_s = [x for x in by_shop if x.get("owed")]
        if owed_s:
            big = max(owed_s, key=lambda x: x["owed"])
            s["rec"].append(f"Collect the {_kes(big['owed'])} owed by corporate clients at {big['shop']}.")
    if beat.get("rec"):
        s["rec"].insert(0, beat["rec"])
    s["rec"] = s["rec"][:3]
    return s


def slides(week_start: dt.date, week_end: dt.date) -> list:
    pg = _Page()
    out = []
    for fn in (lambda: _weekly(pg, week_start, week_end), lambda: _why_moved(pg, week_start, week_end),
               lambda: _why_shops(pg, week_start, week_end),
               lambda: _what_if(pg), lambda: _price(pg), lambda: _corporate(pg)):
        try:
            sl = fn()
            sl["decks"] = ["sales"]
            out.append(sl)
        except Exception as e:                                  # noqa: BLE001
            print(f"  WARNING: a sales slide was skipped: {e}")
    return out
