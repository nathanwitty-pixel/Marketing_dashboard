# -*- coding: utf-8 -*-
"""Reject Sale pricing (Kitengela)  →  reject_sales.html  (payload `RJ`).

A clearance-sale pricing board. Reads the reject stock (reject_stock.csv: BAG TYPE, COLOR,
UNITS) and the production **BOM cost** per bag, then puts every bag into one of two sale
price tiers — **KES 1,000 / 1,500** — chosen by cost so nothing is knowingly sold below cost:

    cost ≤ 900            → 1,000
    cost > 900            → 1,500   (flagged "below cost" if cost > 1,500)

Costlier bags land in 1,500, cheaper ones in 1,000. The mid-range bags are set one by one in
reject_overrides.json ({ "BAG": 1500 }) — a hand pin overrides the cost rule. Also writes an
Excel export (reject_sales_export.xlsx) of the whole pricing board — Bag, Category, Units,
Colours, BOM cost, Sale price, Margin/unit, Margin %, Revenue, Flag.

Sources
  • reject_stock.csv        — the physical reject stock for the sale (editable).
  • "Updated BOMs" sheet    — per-bag production cost (via offer_picking._read_bom_costs),
                              mirrored to bom_costs.json so the board still builds if the
                              sheet is unreachable.
  • reject_overrides.json   — optional manual price pins (editable).

Injects `RJ` into reject_sales.html between the RJ_DATA markers.
"""
import os
import csv
import json
import datetime as _dt

import offer_picking as _op   # reuse: _read_bom_costs, _resolve_bag, aliases (no DB at import)

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE, "reject_stock.csv")
HTML = os.path.join(BASE, "reject_sales.html")
BOM_CACHE = os.path.join(BASE, "bom_costs.json")
OVERRIDES = os.path.join(BASE, "reject_overrides.json")

LOCATION = "Kitengela"
TIERS = [1000, 1500]            # the two sale prices (no 1,200)
BAND = 900                      # cost ≤ BAND → 1,000 ; else 1,500 (unless pinned by hand)
THIN = 250                      # margin below this = "thin" (flagged)
DEFAULT_PRICE = 1000            # bag with no BOM cost → 1,000, flagged for review
EXPORT_XLSX = os.path.join(BASE, "reject_sales_export.xlsx")
EXPORT_CSV = os.path.join(BASE, "reject_sales_export.csv")


def _bom_costs():
    """{BAG (upper): cost} from the BOM sheet, mirrored to bom_costs.json. Falls back to the
    downloaded copy when the sheet is unreachable. Returns (costs, source)."""
    try:
        costs = _op._read_bom_costs()
    except Exception:                                        # noqa: BLE001
        costs = {}
    if costs:
        try:
            json.dump({"_note": "Local copy of BOM production costs, refreshed on every "
                                "successful run; used when the sheet is unreachable.",
                       "_updated": _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                       "costs": costs},
                      open(BOM_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=2, sort_keys=True)
        except Exception:                                    # noqa: BLE001
            pass
        return costs, "BOM sheet (live — downloaded copy refreshed)"
    try:
        raw = json.load(open(BOM_CACHE, encoding="utf-8"))
        return {str(k).upper(): float(v) for k, v in raw.get("costs", {}).items()}, \
            "downloaded copy bom_costs.json (sheet unreachable)"
    except Exception:                                        # noqa: BLE001
        return {}, "unavailable (no BOM sheet, no downloaded copy)"


# Category (col C of the offers sheet) — normalise a few synonyms; fallback keywords for
# bags not on the offers sheet so every bag still gets a bucket.
_CAT_ALIAS = {"SLING BAG": "SLING", "WAISTBAG": "WAIST BAG", "HAND BAG": "HANDBAG"}
_CAT_KEYWORDS = [("HANDBAG", "HANDBAG"), ("HAND BAG", "HANDBAG"), (" HB", "HANDBAG"),
                 ("MOON", "HANDBAG"), ("BAGPACK", "BACKPACK"), ("BACKPACK", "BACKPACK"),
                 (" BP", "BACKPACK"), ("PACK", "BACKPACK"), ("MAN BAG", "MAN BAG"),
                 ("MANBAG", "MAN BAG"), ("TRAVEL", "TRAVEL"), ("SLING", "SLING"),
                 ("SCHOOL", "SCHOOL BAG"), ("LUNCH", "LUNCH BAG"), ("WASH", "WASHBAG"),
                 ("BELT", "WAIST BAG"), ("WAIST", "WAIST BAG"), ("BABY", "BABY BAG"),
                 ("MESSENGER", "MESSENGER"), ("BRIEF", "BRIEFCASE")]


def _norm_cat(c):
    c = str(c or "").strip().upper()
    return _CAT_ALIAS.get(c, c) or "OTHER"


def _category_of(name, offers):
    """Category for a bag: the offers-sheet category (col C), else a keyword fallback."""
    up = str(name).upper().strip()
    for key in (up, _op._apply_alias(up)):
        v = offers.get(key)
        if v and v.get("category"):
            return _norm_cat(v["category"])
    for k, v in offers.items():                              # startswith match, word-boundary
        if v.get("category") and (up == k or up.startswith(k + " ") or k.startswith(up + " ")):
            return _norm_cat(v["category"])
    for sub, cat in _CAT_KEYWORDS:
        if sub in up:
            return cat
    return "OTHER"


def _read_overrides():
    try:
        raw = json.load(open(OVERRIDES, encoding="utf-8"))
    except Exception:                                        # noqa: BLE001
        return {}
    out = {}
    for k, v in (raw.items() if isinstance(raw, dict) else []):
        if str(k).startswith("_"):
            continue
        try:
            out[str(k).strip().upper()] = int(float(v))
        except (ValueError, TypeError):
            pass
    return out


def _read_stock():
    """reject_stock.csv → {BAG (upper): {units, colours:{COLOUR: units}}}."""
    agg = {}
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            bag = (row.get("BAG TYPE") or "").strip().upper()
            col = (row.get("COLOR") or row.get("COLOUR") or "").strip().upper()
            try:
                u = int(float(row.get("UNITS") or 0))
            except (ValueError, TypeError):
                u = 0
            if not bag or u <= 0:
                continue
            e = agg.setdefault(bag, {"units": 0, "colours": {}})
            e["units"] += u
            e["colours"][col] = e["colours"].get(col, 0) + u
    return agg


def _assign_price(cost):
    """(price, flag) from BOM cost — two tiers. flag ∈ {'', 'thin', 'below', 'nobom'}."""
    if cost is None:
        return DEFAULT_PRICE, "nobom"
    price = 1000 if cost <= BAND else 1500
    if price < cost:
        flag = "below"
    elif (price - cost) < THIN:
        flag = "thin"
    else:
        flag = ""
    return price, flag


def _write_export(bags):
    """Write an Excel (xlsx, or CSV fallback) of EVERYTHING on the pricing board — Bag,
    Category, Units, Colours, BOM cost, Sale price, Margin/unit, Margin %, Revenue, Flag.
    Sorted by category then bag, with a TOTAL row. Returns the path written."""
    ordered = sorted(bags, key=lambda b: (b["category"], b["bag"]))
    cols = ["Bag", "Category", "Units", "Colours", "BOM Cost (KES)", "Sale Price (KES)",
            "Margin/Unit (KES)", "Margin %", "Revenue (KES)", "Flag"]
    _FLAG = {"below": "below cost", "thin": "thin", "nobom": "no BOM", "pinned": "pinned", "": ""}
    rows = []
    for b in ordered:
        colours = ", ".join("%s: %d" % (c["c"], c["u"]) for c in b.get("colours", []))
        rows.append([
            b["bag"], b["category"].title(), b["units"], colours,
            b["cost"] if b["cost"] is not None else "",
            b["price"],
            b["marginUnit"] if b["marginUnit"] is not None else "",
            ("%.1f%%" % b["marginPct"]) if b.get("marginPct") is not None else "",
            b["revenue"], _FLAG.get(b.get("flag", ""), b.get("flag", "")),
        ])
    tot_u = sum(b["units"] for b in bags)
    tot_r = sum(b["revenue"] for b in bags)
    tot_m = sum(b.get("marginTotal") or 0 for b in bags)
    rows.append(["TOTAL · margin KES {:,}".format(tot_m), "", tot_u, "", "", "", "", "", tot_r, ""])
    try:
        import pandas as pd
        df = pd.DataFrame(rows, columns=cols)
        df.to_excel(EXPORT_XLSX, index=False, sheet_name="Reject Sale")
        if os.path.exists(EXPORT_CSV):
            try:
                os.remove(EXPORT_CSV)
            except OSError:
                pass
        return EXPORT_XLSX
    except Exception:                                        # noqa: BLE001
        import csv as _csv
        with open(EXPORT_CSV, "w", encoding="utf-8-sig", newline="") as f:
            w = _csv.writer(f)
            w.writerow(cols)
            w.writerows(rows)
        return EXPORT_CSV


def build():
    stock = _read_stock()
    cost, cost_source = _bom_costs()
    try:
        offers, _osrc = _op._read_offers()
    except Exception:                                        # noqa: BLE001
        offers = {}
    overrides = _read_overrides()
    bomkeys = sorted(cost.keys(), key=len, reverse=True)

    bags = []
    for name in sorted(stock):
        e = stock[name]
        canon, c, in_bom = _op._resolve_bag(name, cost, bomkeys)
        price, flag = _assign_price(c)
        pinned = name in overrides
        if pinned:
            price = overrides[name]
            flag = "pinned" if (c is None or price >= c) else "below"
        units = e["units"]
        margin_u = (price - c) if c is not None else None
        bags.append({
            "bag": name,
            "canon": None if canon == name else canon,
            "category": _category_of(name, offers),
            "units": units,
            "cost": round(c) if c is not None else None,
            "price": price,
            "tier": price,
            "pinned": pinned,
            "marginUnit": round(margin_u) if margin_u is not None else None,
            "marginPct": round(margin_u / price * 100, 1) if margin_u is not None and price else None,
            "revenue": price * units,
            "marginTotal": round(margin_u * units) if margin_u is not None else None,
            "flag": flag,
            "colours": [{"c": c2 or "—", "u": u2} for c2, u2 in
                        sorted(e["colours"].items(), key=lambda kv: -kv[1])],
        })

    # sort: most revenue first
    bags.sort(key=lambda b: -b["revenue"])

    def _tier_row(p):
        sel = [b for b in bags if b["price"] == p]
        return {
            "price": p,
            "bags": len(sel),
            "units": sum(b["units"] for b in sel),
            "revenue": sum(b["revenue"] for b in sel),
            "margin": sum(b["marginTotal"] or 0 for b in sel),
        }

    by_tier = [_tier_row(p) for p in TIERS]

    cats = {}
    for b in bags:
        r = cats.setdefault(b["category"], {"category": b["category"], "bags": 0, "units": 0,
                                            "revenue": 0, "margin": 0})
        r["bags"] += 1
        r["units"] += b["units"]
        r["revenue"] += b["revenue"]
        r["margin"] += b["marginTotal"] or 0
    by_category = sorted(cats.values(), key=lambda r: -r["revenue"])

    totals = {
        "bags": len(bags),
        "units": sum(b["units"] for b in bags),
        "revenue": sum(b["revenue"] for b in bags),
        "margin": sum(b["marginTotal"] or 0 for b in bags),
    }
    flags = {
        "below": sorted(b["bag"] for b in bags if b["flag"] == "below"),
        "nobom": sorted(b["bag"] for b in bags if b["flag"] == "nobom"),
        "thin": sorted(b["bag"] for b in bags if b["flag"] == "thin"),
    }

    payload = {
        "location": LOCATION,
        "generated": _dt.date.today().strftime("%d %b %Y"),
        "tiers": TIERS,
        "bands": {"band": BAND, "thin": THIN, "default": DEFAULT_PRICE},
        "costSource": cost_source,
        "bags": bags,
        "byTier": by_tier,
        "byCategory": by_category,
        "totals": totals,
        "flags": flags,
    }

    payload["exportFile"] = os.path.basename(_write_export(bags))

    with open(HTML, encoding="utf-8") as f:
        html = f.read()
    block = ("<!-- RJ_DATA_START -->\n<script>const RJ = "
             + json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
             + ";</script>\n<!-- RJ_DATA_END -->")
    import re
    html = re.sub(r"<!-- RJ_DATA_START -->.*?<!-- RJ_DATA_END -->", lambda _: block, html, flags=re.S)
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)
    return payload


if __name__ == "__main__":
    p = build()
    print("reject_sales.html updated.")
    print(f"  Cost source : {p['costSource']}")
    print(f"  Bag types   : {p['totals']['bags']}  ·  units {p['totals']['units']}")
    print(f"  Projected   : revenue KES {p['totals']['revenue']:,}  margin KES {p['totals']['margin']:,}")
    for t in p["byTier"]:
        print(f"    KES {t['price']:>4}: {t['bags']:>2} bags  {t['units']:>4} units  "
              f"revenue KES {t['revenue']:>7,}  margin KES {t['margin']:>7,}")
    print(f"  Categories  : {len(p['byCategory'])}")
    for crow in p["byCategory"]:
        print(f"    {crow['category']:<12} {crow['bags']:>2} bags  {crow['units']:>4} units  revenue KES {crow['revenue']:>7,}")
    if p["flags"]["below"]:
        print(f"  Below cost  : {', '.join(p['flags']['below'])}")
    if p["flags"]["nobom"]:
        print(f"  No BOM cost : {', '.join(p['flags']['nobom'])}")
    print(f"  Export      : {p.get('exportFile', '')}")
