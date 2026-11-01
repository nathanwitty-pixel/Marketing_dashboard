"""lib/month_extras.py — the newer pages' figures, kept in each month's History snapshot.

monthly_report.py stores these under snapshot["extras"] when a month is archived (month_end.py);
supabase_migration.py writes them to denri_mkt_monthly.extras (jsonb); history.html renders them
inside the month's own sections:

  deals        → section 3 (Offer Type): Power Deals vs Deal of the Week — Kenya   (self_made_combos.html · SMC.deals)
  posting      → section 4 (Posting Yields): posting yield + dead stock clearance, per region (posting_yields.html · PA)
  selfMadeMore → section 6 (Self-Made Combos): monetary implication, combos goal, combo button usage (SMC)
  bagsOnOffer  → section 7 (Bags On vs Off Offer)                                   (bags_on_offer.html · BOO)

Each page is read from its generated HTML data block and must be for the month being archived:
a page that wasn't rebuilt for it (e.g. Bags on offer's deals guard left it as it was) is skipped
(None) rather than storing another month's figures. Only summaries and short lists are kept.
"""
from __future__ import annotations

import json
import os
import re

POSTING_HTML = "posting_yields.html"


def _block(path: str, name: str):
    """The JSON object in `const NAME = {...};` of a generated page, or None."""
    try:
        with open(path, encoding="utf-8") as f:
            txt = f.read()
    except OSError:
        return None
    m = re.search(r"const %s = (\{.*?\});\s*</script>" % name, txt, re.S)
    try:
        return json.loads(m.group(1)) if m else None
    except ValueError:
        return None


def _posting_block(path: str):
    """PA is a JS object literal (unquoted keys, one field per line): read its JSON-valued fields."""
    try:
        with open(path, encoding="utf-8") as f:
            txt = f.read()
    except OSError:
        return None
    m = re.search(r"const PA = \{\n(.*?)\n\};", txt, re.S)
    if not m:
        return None
    out = {}
    for ln in m.group(1).split("\n"):
        f = re.match(r"\s*(\w+):\s*(.*?),?\s*$", ln)
        if f:
            try:
                out[f.group(1)] = json.loads(f.group(2))
            except ValueError:
                pass
    return out


def _pick(d: dict, keys) -> dict:
    return {k: d.get(k) for k in keys if k in d}


def _deals(smc: dict):
    d = smc.get("deals") or {}
    if not d:
        return None
    row = ("product", "tier", "orig", "now", "disc", "sold", "revenue", "stock")
    dow = sorted(d.get("dealOfWeek") or [], key=lambda r: -(r.get("sold") or 0))
    return {
        **_pick(d, ("powerCount", "powerSold", "powerRevenue", "powerDisc", "powerSoldExCombo",
                    "dowProducts", "dowRows", "dowLocations", "dowSold", "dowRevenue", "dowDisc",
                    "dowSoldExCombo", "dedupSold", "dedupRevenue", "dedupProducts", "overlapProducts",
                    "comboBagDeals")),
        "tiers": (d.get("tierCompare") or {}).get("tiers") or [],
        "power": [_pick(r, row) for r in sorted(d.get("powerDeals") or [], key=lambda r: -(r.get("sold") or 0))],
        "dow": [{**_pick(r, row), "shops": len(r.get("locations") or [])} for r in dow[:15]],
    }


def _self_made_more(smc: dict):
    mi, goal = smc.get("monetaryImplication") or {}, smc.get("combosGoal") or {}
    return {
        "monetary": {"running": mi.get("runTotals"), "selfMade": mi.get("smTotals")},
        "goal": {**_pick(goal, ("augLabel", "septLabel", "augTotal", "augAvg", "septSoFar", "weeklyToBeat", "beaten")),
                 "weeks": [_pick(w, ("wk", "cur", "prev")) for w in goal.get("weeklyDetail") or []]},
        "usage": [_pick(u, ("combo", "expected", "rung", "implied"))
                  for u in sorted(smc.get("comboUsage") or [], key=lambda u: -(u.get("implied") or 0))],
    }


def _posting(pa: dict):
    def region(r):
        py = ((r or {}).get("postYield") or {}).get("monthly") or {}
        dc = ((r or {}).get("deadClear") or {}).get("monthly") or {}
        if not py and not dc:
            return None
        return {"yield": {**_pick(py, ("spp", "posts", "bagsPosted", "expected", "soldPosted", "credited",
                                       "achievedPct", "bagsHit", "bagsZero", "soldNotPosted", "window")),
                          "on": py.get("on"), "off": py.get("off")},
                "dead": dc.get("seg") or {}}
    out = {"kenya": region(pa), "sinza": region(pa.get("sinza")), "uganda": region(pa.get("uganda"))}
    return out if any(out.values()) else None


def _bags_on_offer(boo: dict):
    p = (boo.get("periods") or {}).get("monthly") or {}
    if not p:
        return None
    # Units / money per offer type for the month (the page's "Offer type summary").
    types = {}
    for key, cats in ((p.get("offerTypes") or {}).get("cat") or {}).items():
        types[key] = {"units": round(sum((c or {}).get("units") or 0 for c in cats.values())),
                      "revenue": round(sum((c or {}).get("revenue") or 0 for c in cats.values()))}
    labels = {r["key"]: r["label"] for r in (p.get("offerTypes") or {}).get("rows") or []}
    return {
        **_pick(p, ("range", "kenyaPace", "totals", "others", "sources", "comboPrints")),
        "trend": [_pick(t, ("label", "sub", "on", "off", "oth")) for t in p.get("trend") or []],
        "types": [{"key": k, "label": labels.get(k, k), **v} for k, v in types.items()],
        "regions": [_pick(r, ("region", "revenue", "target", "pace", "redCount")) for r in p.get("regions") or []],
        "onTop": [_pick(b, ("bag", "units", "revenue", "sources", "category"))
                  for b in sorted(p.get("onBags") or [], key=lambda b: -(b.get("revenue") or 0))[:12]],
        "offTop": [_pick(b, ("bag", "units", "revenue", "stock", "daysCover", "category", "isNew"))
                   for b in sorted(p.get("offBags") or [], key=lambda b: -(b.get("revenue") or 0))[:12]],
        "offCount": len(p.get("offBags") or []),
        "onCount": len(p.get("onBags") or []),
    }


SHOP_CORP_BACKUP = "shop_corporate_history.json"


def shop_corporate_month(month_name: str, year: int, warn=print):
    """The month's Shop corporate tab, rebuilt from Odoo for that month (lib/shop_corporate), and saved to
    data/shop_corporate_history.json as a local backup. None when Odoo can't be read."""
    import calendar
    import datetime
    import json
    from lib import paths, shop_corporate
    m = list(calendar.month_name).index(month_name)
    last = datetime.date(year, m, calendar.monthrange(year, m)[1])
    try:
        data = shop_corporate.build(min(last, datetime.date.today()))
    except Exception as ex:                                  # noqa: BLE001
        warn(f"  extras: shop corporate skipped ({ex})")
        return None
    if data is None:
        warn("  extras: shop corporate skipped (Odoo unreachable)")
        return None
    path = paths.data(SHOP_CORP_BACKUP)
    try:
        hist = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        hist = {}
    hist[f"{year}-{m:02d}"] = dict(data, savedOn=datetime.date.today().isoformat())
    json.dump(hist, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
    return data


def _month_dates(month_name: str, year: int):
    import calendar
    import datetime
    m = list(calendar.month_name).index(month_name)
    return m, datetime.date(year, m, 1), datetime.date(year, m, calendar.monthrange(year, m)[1])


def cp_more_month(month_name: str, year: int, warn=print):
    """1 · Current Performance extras for History: revenue, month-on-month waterfall, Kenya followers & reach
    (docs/reporting-history.md). Each part None when its source can't be read."""
    from lib import db, queries, product_targets, why_moved, odoo_marketing
    m, first, last = _month_dates(month_name, year)
    out = {"revenue": None, "whyMoved": None, "followers": None}
    try:
        r = db.run_query(queries.BAG_REVENUE, {"start_date": first.isoformat(), "end_date": last.isoformat(),
                                               "excluded": queries.excluded_products()})
        c = db.run_query(queries.CORPORATE_BAGS, {"start_date": first.isoformat(), "end_date": last.isoformat()})
        t = db.run_query(product_targets.TOTAL_SQL, {"m": first.isoformat()})
        if r is not None and len(r):
            rev = {k: round(float(v or 0)) for k, v in r.iloc[0].items()}
            pos = rev["single_kes"] + rev["combo_kes"] + rev["gift_kes"] + rev["discount_kes"]
            corp = c.iloc[0] if c is not None and len(c) else {}
            out["revenue"] = dict(rev, posKes=pos, corporateKes=round(float(corp.get("kes") or 0)),
                                  corporateBags=round(float(corp.get("bags") or 0)),
                                  revenueTarget=round(float(t.amt[0])) if t is not None and len(t) and t.amt[0] else None,
                                  bagTarget=round(float(t.qty[0])) if t is not None and len(t) and t.qty[0] else None)
    except Exception as ex:                                  # noqa: BLE001
        warn(f"  extras: revenue skipped ({ex})")
    try:
        out["whyMoved"] = why_moved.build_month(year, m)
    except Exception as ex:                                  # noqa: BLE001
        warn(f"  extras: why-moved skipped ({ex})")
    try:
        days = [d for d in odoo_marketing.followers_daily() if first.isoformat() <= d["date"] <= last.isoformat()]
        if days:
            fol = {}
            for plat in ("instagram", "facebook"):
                ds = [d for d in days if d["platform"] == plat]
                counts = [d for d in ds if d["followers"] is not None]
                fol[plat] = {"followers": counts[-1]["followers"] if counts else None,
                             "newFollows": sum(d["newFollows"] or 0 for d in ds),
                             "reach": sum(d["reach"] or 0 for d in ds), "views": sum(d["views"] or 0 for d in ds),
                             "from": ds[0]["date"] if ds else None, "to": ds[-1]["date"] if ds else None}
            out["followers"] = fol
    except Exception as ex:                                  # noqa: BLE001
        warn(f"  extras: followers skipped ({ex})")
    return out


def product_performance_month(month_name: str, year: int, base: str | None = None, warn=print):
    """9 · Product Performance for History: the page's Last-month view for this month (vs the month before) —
    rows, bag of the month per market, why it moved, shop breakdown. Read from the built page when its Last month
    is this month, else built for the 1st of the next month. None on failure."""
    import datetime
    import sys
    from lib import paths
    m, first, last = _month_dates(month_name, year)
    pp = _block(os.path.join(base or paths.HTML, "product_performance.html"), "PP") or {}
    lm = (pp.get("periods") or {}).get("lastmonth") or {}
    if (lm.get("cur") or [None])[0] != first.isoformat():
        try:
            if paths.GENERATORS not in sys.path:
                sys.path.insert(0, paths.GENERATORS)
            import product_performance
            pp = product_performance.build(last + datetime.timedelta(days=1))
        except Exception as ex:                              # noqa: BLE001
            warn(f"  extras: product performance skipped ({ex})")
            return None
        lm = pp["periods"]["lastmonth"]
    return {"label": f"{month_name} {year}", "cur": lm.get("cur"), "prev": lm.get("prev"),
            "curLabel": lm.get("curLabel"), "prevLabel": lm.get("prevLabel"), "rows": lm.get("rows") or [],
            "botw": (pp.get("botw") or {}).get("lastmonth") or {}, "why": (pp.get("why") or {}).get("lastmonth") or {},
            "shops": (pp.get("shops") or {}).get("lastmonth") or {}, "topN": pp.get("topN", 15)}


def build_extras(base: str, month_name: str, year: int, warn=print) -> dict:
    """Everything above for `month_name year` (e.g. "September", 2026). Pages for another month are skipped.
    `base` is the folder holding the built pages (paths.HTML)."""
    label = f"{month_name} {year}"
    smc = _block(os.path.join(base, "self_made_combos.html"), "SMC") or {}
    boo = _block(os.path.join(base, "bags_on_offer.html"), "BOO") or {}
    pa = _posting_block(os.path.join(base, POSTING_HTML)) or {}

    out = {"deals": None, "selfMadeMore": None, "posting": None, "bagsOnOffer": None,
           "shopCorporate": shop_corporate_month(month_name, year, warn),
           "cpMore": cp_more_month(month_name, year, warn),
           "productPerformance": product_performance_month(month_name, year, base, warn)}
    if smc.get("month") == label:
        out["deals"], out["selfMadeMore"] = _deals(smc), _self_made_more(smc)
    else:
        warn(f"  extras: self_made_combos.html is for {smc.get('month') or '?'}, not {label} — deals / self-made extras skipped")
    if boo.get("month") == label:
        out["bagsOnOffer"] = _bags_on_offer(boo)
    else:
        warn(f"  extras: bags_on_offer.html is for {boo.get('month') or '?'}, not {label} — bags on/off offer skipped")
    win = (((pa.get("postYield") or {}).get("monthly") or {}).get("window") or "")
    if month_name[:3] in win and str(year) in win:
        out["posting"] = _posting(pa)
    else:
        warn(f"  extras: posting page window is '{win or '?'}', not {label} — posting yield extras skipped")
    return out
