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
    s = {"id": "weekly-perf", "kicker": "Weekly Performance, Week 1 to latest", "tone": beat.get("tone", "neutral"),
         "headline": beat.get("headline") or "Weekly sales this month.", "insight": [], "rec": [],
         "source": "The Current Performance page's Weekly Performance (Odoo tills + the Corporate app, Sun to Sat weeks).",
         "graph": {"ok": bool(weeks), "kind": "weekly", "labels": labels,
                   "pos": [round(w.get("posBags") or 0) for w in weeks], "corp": [round(w.get("corporateBags") or 0) for w in weeks],
                   "floor": round(floor) if floor else None,
                   "table": {"title": "Week by week (% of target = the week's bags against the month's bag target)",
                             "cols": ["Week", "Bags", "Corporate", "% of target", "Cumulative", "vs the floor", "Last month same week"],
                             "rows": rows, "trend": [1, 1]}}}
    if weeks:
        best = max(weeks, key=lambda w: w.get("weeklySales") or 0)
        s["insight"].append(f"Best week: {best['label']} with <b>{_fmt(best['weeklySales'])}</b> bags; month so far "
                            f"<b>{weeks[-1].get('salesPct', 0):.1f}%</b> of the bag target ({_fmt(weeks[-1].get('salesBags'))} bags).")
        if floor:
            short = [w for w in weeks if (w.get("weeklySales") or 0) < floor]
            s["insight"].append(f"Weekly floor (target ÷ the month's weeks): {_fmt(floor)} bags. "
                                + (f"{len(short)} of {len(weeks)} weeks fell short, by {_fmt(floor - (weeks[-1].get('weeklySales') or 0))} "
                                   f"last week." if short else "Every week cleared it."))
        if len(weeks) >= 2:
            a, b = weeks[-1], weeks[-2]
            s["insight"].append(f"Last week {_fmt(a.get('weeklySales'))} bags vs {_fmt(b.get('weeklySales'))} the week before "
                                f"({_signed(_pct(a.get('weeklySales') or 0, b.get('weeklySales') or 0))}).")
        if beat.get("rec"):
            s["rec"].append(beat["rec"])
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
        s["insight"].insert(0, "Week by week: " + ", ".join(f"{x['label']} {_fmt(x['total'])}" for x in wk_tot)
                            + (f" (the week before Wk 1: {_fmt(series[0]['total'])})" if series and series[0]["base"] else "") + ".")
    regs_w = [r for r in wow if r["label"] != "Selling days"]
    if regs_w:
        up, dn = regs_w[0], regs_w[-1]
        s["insight"].append(f"Week on week: biggest rise {up['label']} {'+' if up['delta'] >= 0 else ''}{_fmt(up['delta'])}, "
                            f"biggest fall {dn['label']} {'+' if dn['delta'] >= 0 else ''}{_fmt(dn['delta'])}.")
        if shop_moves:
            falls = [t for t in shop_moves if t[1] < 0][:2]
            rises = [t for t in reversed(shop_moves) if t[1] > 0][:2]
            if falls or rises:
                s["insight"].append("Shops behind it: " + ", ".join(f"{sh} {'+' if d >= 0 else ''}{_fmt(d)}" for sh, d in rises + falls) + ".")
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
        s["insight"].append(f"Month on month: {top['label']} added the most ({'+' if top['delta'] >= 0 else ''}{_fmt(top['delta'])}"
                            + (f"; {sh}" if sh else "") + f"); {regs_m[-1]['label']} {'+' if regs_m[-1]['delta'] >= 0 else ''}"
                            f"{_fmt(regs_m[-1]['delta'])}.")
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
    s["insight"].append(f"What the extra is added to: so far {_fmt(rate_so_far)} bags a day ({_fmt(sold)} in {done} days); the "
                        f"forecast expects about {_fmt(rate_rest)} a day for the last {left} days (the weekday pattern). "
                        f"\"+100 a day\" = {_fmt(rate_rest)} → {_fmt(rate_rest + 100)} a day.")
    s["insight"].append("Each extra 100 bags a day adds " + f"{_fmt(100 * left)} bags ({100 * left / target * 100:.1f} points) and "
                        f"{_kes(100 * left * ppb)} at KES {_fmt(ppb)} a bag.")
    reach = next((x for x in scen if x["pct"] >= 100), None)
    s["insight"].append(("A lift of " + reach["label"] + " would reach the target." if reach else
                         f"Even +{EXTRA[-1]} a day ends at {scen[-1]['pct']:.0f}%: the target is out of reach this month."))
    s["insight"].append(f"Revenue at the current pace: {_kes(scen[0]['rev'])} ({scen[0]['revPct']}% of {_kes(rev_t)}).")
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
        it = [x for x in (r.get("items") or []) if x.get("gapPct") is not None]
        r["_n"], r["_ok"] = len(it), sum(1 for x in it if x["gapPct"] >= 0)
    offer_rows = [r for r in rows if r.get("key") in OFFERS]
    types_ok = [r for r in offer_rows if (r.get("ppb") or 0) >= (tgt or 0)]
    items_n = sum(r["_n"] for r in offer_rows)
    items_ok = sum(r["_ok"] for r in offer_rows)
    s = {"id": "price", "kicker": "Price per Bag: operating above the target price", "insight": [], "rec": [],
         "tone": "good" if (gap or 0) > 0 else "bad",
         "source": "The Current Performance page's Price per Bag (single bags and combos this month, after discounts).",
         "graph": {"ok": bool(rows), "kind": "price", "target": tgt,
                   "rows": [{"label": r["label"], "ppb": r["ppb"], "gap": r.get("gapPct"), "bags": r.get("bags"),
                             "effect": r.get("effectKes"), "offer": r.get("key") in OFFERS,
                             "n": r["_n"], "ok": r["_ok"]} for r in rows],
                   "working": {"types": len(types_ok), "typesN": len(offer_rows), "items": items_ok, "itemsN": items_n},
                   "total": None}}
    s["headline"] = (f"Bags sell at KES {_fmt(act)} against the KES {_fmt(tgt)} target price ({'+' if (gap or 0) >= 0 else ''}{gap}%), "
                     f"so revenue runs {'ahead of' if (gap or 0) >= 0 else 'behind'} bags: {pm.get('revPct')}% of the revenue target "
                     f"vs {pm.get('bagsPct')}% of the bag target.") if tgt and act else "No price-per-bag figures yet."
    if tgt and act:
        s["insight"].append(f"Target price KES {_fmt(tgt)} = {_kes(rev_t)} revenue target ÷ the bag target; actual KES {_fmt(act)}: "
                            f"KES {_fmt(act - tgt)} {'more' if act >= tgt else 'less'} a bag than the targets assume.")
    if offer_rows:
        s["insight"].insert(0, f"Offers working: <b>{len(types_ok)} of {len(offer_rows)}</b> offer types "
                            f"({len(types_ok) / len(offer_rows) * 100:.0f}%) sell at or above the target price"
                            + (f", and <b>{items_ok} of {items_n}</b> offers inside them ({items_ok / items_n * 100:.0f}%)" if items_n else "")
                            + ": the share of the committee's choices paying their way.")
        below = [r["label"] for r in offer_rows if r not in types_ok]
        if below:
            s["rec"].insert(0, f"Review {', '.join(below)}: below the KES {_fmt(tgt)} target price this month.")
    if bags_need:
        s["insight"].append(f"Bags still to sell for the revenue target: <b>{_fmt(bags_need)}</b> at KES {_fmt(act)} a bag, for the "
                            f"{_kes(still)} still to bring in.")
    eff = [r for r in rows if r.get("effectKes") is not None]
    if eff:
        lift = max(eff, key=lambda r: r["effectKes"])
        drag = min(eff, key=lambda r: r["effectKes"])
        s["insight"].append(f"Biggest lift: {lift['label']} ({_kes(lift['effectKes'])} above target by month end); biggest drag: "
                            f"{drag['label']} ({_kes(abs(drag['effectKes']))} {'below' if drag['effectKes'] < 0 else 'above'} target).")
    if beat.get("rec"):
        s["rec"].append(beat["rec"])
    if (gap or 0) > 0:
        s["rec"].append(f"Hold the prices that beat the target: {', '.join(r['label'] for r in rows if (r.get('gapPct') or 0) > 0) or 'the full-price bags'}.")
    return s


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
                   "strip": {"sold": sold, "kes": kes, "tgt": tgt, "open": open_b},
                   "shops": shop_rows[:10],
                   "shopStrip": {"sold": sum(r["sold"] for r in shop_rows), "kes": sum(r["kes"] for r in shop_rows),
                                 "owed": sum(r["owed"] for r in shop_rows), "clients": len(shop_rows)}}}
    top = sorted((r for r in rows if r["sold"]), key=lambda r: -r["sold"])[:3]
    if top:
        s["insight"].append("Biggest clients this month: " + ", ".join(f"{r['client']} {_fmt(r['sold'])} bags" for r in top) + ".")
    if tgt:
        s["insight"].append(f"Received {_kes(kes)} of the {_kes(tgt)} corporate target ({kes / tgt * 100:.0f}%).")
    opens = sorted((r for r in rows if r["open"]), key=lambda r: -r["open"])[:3]
    if opens:
        s["insight"].append(f"Quoted and not invoiced: {_fmt(open_b)} bags, " + ", ".join(f"{r['client']} {_fmt(r['open'])}" for r in opens) + ".")
    owes = sorted((r for r in rows if r["owed"]), key=lambda r: -r["owed"])[:2]
    if owes:
        s["insight"].append("Still owed: " + ", ".join(f"{r['client']} {_kes(r['owed'])}" for r in owes) + ".")
    if shop_rows:
        s["headline"] = (s["headline"].rstrip(".") + f"; at the shops, {_fmt(sum(r['sold'] for r in shop_rows))} bags paid by "
                         f"Corporate-team clients and {_kes(sum(r['owed'] for r in shop_rows))} still owed.")
        by_shop = sc.get("shops") or []
        s["insight"].append(f"Paid at the shops (Corporate-team clients): {len(shop_rows)} clients, "
                            f"{_fmt(sum(r['sold'] for r in shop_rows))} bags, {_kes(sum(r['kes'] for r in shop_rows))}"
                            + (": " + ", ".join(f"{x['shop']} {_fmt(x['bags'])} bags" for x in by_shop if x.get("bags")) if by_shop else "") + ".")
        owed_s = [x for x in by_shop if x.get("owed")]
        if owed_s:
            s["insight"].append("Owed at the shops: " + ", ".join(f"{x['shop']} {_kes(x['owed'])}" for x in owed_s) + ".")
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
               lambda: _what_if(pg), lambda: _price(pg), lambda: _corporate(pg)):
        try:
            sl = fn()
            sl["decks"] = ["sales"]
            out.append(sl)
        except Exception as e:                                  # noqa: BLE001
            print(f"  WARNING: a sales slide was skipped: {e}")
    return out
