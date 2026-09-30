"""lib/month_extras.py — the newer pages' figures, kept in each month's History snapshot.

monthly_report.py stores these under snapshot["extras"] when a month is archived (month_end.py);
supabase_migration.py writes them to denri_mkt_monthly.extras (jsonb); history.html renders them
inside the month's own sections:

  deals        → section 3 (Offer Type): Power Deals vs Deal of the Week — Kenya   (self_made_combos.html · SMC.deals)
  posting      → section 4 (Posting Yields): posting yield + dead stock clearance, per region (POSTING….html · PA)
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

POSTING_HTML = "POSTING (SALES YIELDS FROM ACCURATE POSTING).html"


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


def build_extras(base: str, month_name: str, year: int, warn=print) -> dict:
    """Everything above for `month_name year` (e.g. "September", 2026). Pages for another month are skipped."""
    label = f"{month_name} {year}"
    smc = _block(os.path.join(base, "self_made_combos.html"), "SMC") or {}
    boo = _block(os.path.join(base, "bags_on_offer.html"), "BOO") or {}
    pa = _posting_block(os.path.join(base, POSTING_HTML)) or {}

    out = {"deals": None, "selfMadeMore": None, "posting": None, "bagsOnOffer": None}
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
