"""
self_made_combos.py
─────────────────────────────────────────────────────────────────
Self-Made Combos vs Running Combos — for the current month (live).

Staff create ad-hoc combos on the POS via a Combo Request (Odoo model
pos.combo.request → the CBR/2026/NNNN references). Each request carries a
`combo_product_id` that points at the product_template created for that combo,
so when it sells it lands in POS sales (pos_order_line) linked back to the CBR.

We now read the real request table (SELECT access granted), so every combo sold
this month is split by the *actual* CBR link, not a name heuristic:
  • Self-made  — the sold product's template IS a CBR combo_product_id
  • Running    — everything else (the official offer-sheet combos)

We also surface the request log itself — CBR ref · combo · shop · requested by ·
approved-by-Lloyd · state · date — including rejected/pending requests that never
reached the tills.

Scoped to the Kenya tills (the combos run there). Injects `SMC` into
self_made_combos.html between the SMC_DATA markers.
─────────────────────────────────────────────────────────────────
"""

import re, os, json, webbrowser, pathlib, datetime

import pandas as pd

from lib import db, report_month

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "self_made_combos.html")


def fmt(n):
    return f"{int(round(n)):,}"


# Combos sold this month, split by the real CBR link (combo_product_id).
COMBO_SQL = """
WITH cbr AS (
    SELECT DISTINCT combo_product_id
    FROM pos_combo_request
    WHERE combo_product_id IS NOT NULL
)
SELECT pt."name" AS product,
       pt.id      AS tmpl_id,
       SUM(pl.qty)::int AS qty,
       ROUND(SUM(pl.price_subtotal_incl))::numeric AS value,
       (pt.id IN (SELECT combo_product_id FROM cbr)) AS is_cbr,
       -- include_all = the POS combo picker offers the FULL range of a category
       -- (e.g. "Select any 2" across every Lola/Mini Zuri/Trecento colour). That
       -- is the defining mark of an official running combo; a self-made CBR combo
       -- is a fixed, specific pairing (include_all is false).
       COALESCE((SELECT BOOL_OR(pcx.include_all) FROM product_combo pcx
                 WHERE pcx.product_template_id = pt.id), FALSE) AS include_all,
       -- Colour range: total picker options across the combo's categories. A
       -- running/official combo offers a wide range (the shop attendant chooses
       -- the colour); a self-made CBR combo is locked to one specific pairing.
       (SELECT COUNT(*) FROM product_combo pcx
          JOIN product_combo_product_product_rel r ON r.product_combo_id = pcx.id
        WHERE pcx.product_template_id = pt.id) AS colour_options
FROM pos_order p
JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
  AND p.state IN ('done', 'paid')
  AND pl.qty > 0
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
  -- A combo follows the naming convention "A + B" — every real running and
  -- self-made combo does. We do NOT treat "has a product_combo definition" as
  -- sufficient: single bags occasionally carry a stray combo/include_all flag
  -- (e.g. "Big Man Bag Grey", a KES 1,810 single bag), which must not be counted.
  AND pt."name" LIKE '%+%'
  AND pt."name" NOT ILIKE '%delivery%'
  AND pt."name" NOT ILIKE '%customi%'
GROUP BY pt."name", pt.id
ORDER BY qty DESC, value DESC
"""

# Per combo SALE, the bags actually printed — Odoo stores the chosen components in
# pos_order_line.combo_product_attribute_values (e.g. "Mini Umbra Grey", "Mega Black").
# This lets us attribute a combo like "Mega + Man Bag or Mini Umbra or Neo Man Bag"
# to the specific bag the customer picked, instead of the bundle as a whole.
COMBO_COMPONENTS_SQL = """
SELECT pt.id AS tmpl_id, pl.qty::int AS qty,
       COALESCE(pl.combo_product_attribute_values, '') AS attrs
FROM pos_order p
JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
  AND p.state IN ('done', 'paid') AND pl.qty > 0
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
  AND pt."name" LIKE '%+%'
"""

# The combo-request log for the month (all states).
REQUEST_SQL = """
SELECT r.name        AS cbr,
       r.combo_name  AS combo,
       r.state       AS state,
       r.approved_by_lloyd AS lloyd,
       COALESCE(r.price_incl, 0)::numeric AS price,
       pc."name"     AS shop,
       rp."name"     AS requested_by,
       r.create_date AS requested_on,
       r.decision_date AS decided_on,
       r.reject_reason AS reject_reason,
       r.combo_product_id AS tmpl_id
FROM pos_combo_request r
LEFT JOIN pos_config  pc ON pc.id = r.config_id
LEFT JOIN res_users   ru ON ru.id = r.user_id
LEFT JOIN res_partner rp ON rp.id = ru.partner_id
WHERE r.create_date::date BETWEEN :start_date AND :end_date
ORDER BY r.create_date DESC, r.id DESC
"""

# Per-combo units sold per Sun-Sat week. WK index = weeks since the Sunday on/before
# the month's first day (:anchor, precomputed in Python), so WK1 = the week
# containing day 1, then each Sunday starts a new week — the offer sheet's structure.
_WK_EXPR = ("(((p.date_order::date - (EXTRACT(DOW FROM p.date_order::date)::int)) "
            "- :anchor) / 7 + 1)")
_COMBO_WHERE = """
  AND p.state IN ('done', 'paid') AND pl.qty > 0
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
  AND pt."name" LIKE '%+%'
  AND pt."name" NOT ILIKE '%delivery%'
  AND pt."name" NOT ILIKE '%customi%'
"""
COMBO_WEEKLY_SQL = f"""
SELECT pt.id AS tmpl_id, pt."name" AS product, {_WK_EXPR} AS wk, SUM(pl.qty)::int AS units
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
{_COMBO_WHERE}
GROUP BY pt.id, pt."name", wk
"""
# A whole month's combo sales (all combos) per Sun-Sat week — used for the August
# baseline and the September-so-far tally.
MONTH_WEEKLY_SQL = f"""
SELECT {_WK_EXPR} AS wk, SUM(pl.qty)::int AS units
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
{_COMBO_WHERE}
GROUP BY wk ORDER BY wk
"""


def _dstr(v):
    if v is None:
        return ""
    try:
        return v.strftime("%d %b")
    except Exception:
        s = str(v)
        return s[:10] if s and s.lower() != "nat" else ""


def _read_offer_analysis():
    """Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the
    Offer Type Analysis page, so the Running combos can be rendered as the same
    target cards (price · weekly sold · stock ★ · monthly/weekly target · verdict).
    We aggregate stock to a {bagType: kenyaStock} map to keep the payload small."""
    try:
        import offer_data
        oa = offer_data.build()[0]
    except Exception:
        return None
    stock_map = {}
    for s in oa.get("stockData", []):
        k = str(s.get("bagType") or "").strip().upper()
        if k:
            stock_map[k] = stock_map.get(k, 0) + (s.get("kenyaStock") or 0)

    def _region_stock(rows, key):
        m = {}
        for s in rows or []:
            k = str(s.get("bagType") or "").strip().upper()
            if k:
                m[k] = m.get(k, 0) + (s.get(key) or 0)
        return m

    return {
        "combos":          oa.get("juneCombos", []),
        "comboHeaders":    oa.get("juneComboHeaders", []),
        "bagTargets":      oa.get("bagTargets", {}),
        "stockMap":        stock_map,
        "weeksRemaining":  oa.get("weeksRemaining", 1),
        "monthName":       oa.get("monthName", ""),
        "comboCount":      oa.get("comboCount"),
        "powerDealCount":  oa.get("powerDealCount"),
        "totalKenyaStock": oa.get("totalKenyaStock"),
        # Sinza & Uganda combos (from the COMBOS sheet) + their regional stock,
        # for the region-selector guidance cards on this page.
        "sinzaCombos":        oa.get("sinzaCombos", []),
        "sinzaComboHeaders":  oa.get("sinzaComboHeaders", []),
        "sinzaSingles":       oa.get("sinzaSingles", []),
        "sinzaSinglesHeaders":oa.get("sinzaSinglesHeaders", []),
        "sinzaSpecials":      oa.get("sinzaSpecials", []),
        "sinzaSpecialHeaders":oa.get("sinzaSpecialHeaders", []),
        "ugCombos":           oa.get("ugCombos", []),
        "ugComboHeaders":     oa.get("ugComboHeaders", []),
        "ugSingles":          oa.get("ugSingles", []),
        "ugSinglesHeaders":   oa.get("ugSinglesHeaders", []),
        "sinzaStock":         _region_stock(oa.get("sinzaStockData"), "sinzaStock"),
        "ugStock":            _region_stock(oa.get("ugStockData"), "ugandaStock"),
        "totalSinzaStock":    oa.get("totalSinzaStock"),
        "totalUgandaStock":   oa.get("totalUgandaStock"),
        "ugComboTitle":       oa.get("ugComboTitle", ""),
        "sinzaComboTitle":    oa.get("sinzaComboTitle", ""),
    }


DEALS_SHEET_ID = "1TAGv9bGnE88nEjn2d0QvBkRhKiK3E42VI2GfU-MmJEY"

# All Kenya bag sales this month by product template — to attach real sold/revenue
# to each deal product (matched by name prefix, like the new-products page).
DEAL_SALES_SQL = """
SELECT UPPER(pt."name") AS name, SUM(pl.qty)::int AS units,
       ROUND(SUM(pl.price_subtotal_incl))::int AS val
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
  AND p.state IN ('done', 'paid') AND pl.qty > 0
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
  AND pt."name" NOT LIKE '%+%'   -- combo products belong to the combos view, not deals
GROUP BY UPPER(pt."name")
"""

# Same, split by Sun-Sat week — for the per-deal weekly line (like the combo cards).
DEAL_WEEKLY_SQL = f"""
SELECT UPPER(pt."name") AS name, {_WK_EXPR} AS wk, SUM(pl.qty)::int AS units
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
  AND p.state IN ('done', 'paid') AND pl.qty > 0
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
  AND pt."name" NOT LIKE '%+%'   -- combo products belong to the combos view, not deals
GROUP BY UPPER(pt."name"), wk
"""


def _enrich_deals(deals, m_start, m_end, stock_map):
    """Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to
    each deal product, matched by product-name prefix."""
    sales = []
    df = db.run_query(DEAL_SALES_SQL, {"start_date": m_start.isoformat(),
                                       "end_date": m_end.isoformat()})
    if df is not None and not df.empty:
        sales = [(str(r["name"]), int(r["units"] or 0), int(r["val"] or 0)) for _, r in df.iterrows()]

    # weekly: name -> {wk: units}
    name_wk, max_wk = {}, 1
    _anchor = m_start - datetime.timedelta(days=(m_start.weekday() + 1) % 7)   # Sunday on/before month start
    wf = db.run_query(DEAL_WEEKLY_SQL, {"start_date": m_start.isoformat(),
                                        "end_date": m_end.isoformat(), "anchor": _anchor})
    if wf is not None and not wf.empty:
        for _, r in wf.iterrows():
            nm, w, u = str(r["name"]), int(r["wk"]), int(r["units"] or 0)
            name_wk.setdefault(nm, {})[w] = u
            max_wk = max(max_wk, w)
    deals["curWeek"] = max_wk
    stock_items = list(stock_map.items())

    def _match(prod):
        p = str(prod).strip().upper()
        u = v = st = 0
        wk = {}
        for nm, un, val in sales:
            if nm == p or nm.startswith(p + " ") or p.startswith(nm + " "):
                u += un
                v += val
        for nm, wkmap in name_wk.items():
            if nm == p or nm.startswith(p + " ") or p.startswith(nm + " "):
                for w, un in wkmap.items():
                    wk[w] = wk.get(w, 0) + un
        for bt, s in stock_items:
            if bt == p or bt.startswith(p + " ") or p.startswith(bt + " ") or bt == p.split(" ")[0]:
                st += s
        weeks = [{"label": "Wk %d" % i, "sold": wk.get(i, 0)} for i in range(1, max_wk + 1)]
        return u, v, st, weeks

    for grp in ("powerDeals", "dealOfWeek"):
        for it in deals.get(grp, []):
            it["sold"], it["revenue"], it["stock"], it["weeks"] = _match(it["product"])
    deals["powerSold"] = sum(x["sold"] for x in deals.get("powerDeals", []))
    deals["powerRevenue"] = sum(x["revenue"] for x in deals.get("powerDeals", []))
    deals["dowSold"] = sum(x["sold"] for x in deals.get("dealOfWeek", []))
    deals["dowRevenue"] = sum(x["revenue"] for x in deals.get("dealOfWeek", []))

    # Deduped totals — a bag that runs as BOTH a Power Deal and a Deal of the Week
    # (same Odoo product) is one bag's sales, so count it once for the combined
    # "Deal units sold" / revenue headline instead of on both sides.
    def _dn(s):
        return re.sub(r"\s+", " ", str(s).strip().upper())
    _seen = {}
    for _x in deals.get("powerDeals", []) + deals.get("dealOfWeek", []):
        _seen.setdefault(_dn(_x["product"]), _x)   # first wins; sold/revenue identical per product
    deals["dedupSold"] = sum(v.get("sold", 0) for v in _seen.values())
    deals["dedupRevenue"] = sum(v.get("revenue", 0) for v in _seen.values())
    deals["dedupProducts"] = len(_seen)
    deals["overlapProducts"] = (len(deals.get("powerDeals", [])) + len(deals.get("dealOfWeek", []))) - len(_seen)

    # Cross-sell: which Power Deals are ALSO run as a Deal of the Week (same bag).
    # Matched by product name, so each card can show the same bag's rival pricing —
    # all-month Power price vs the Tier-1 weekly deal — like the running↔self-made hover.
    def _norm(s):
        return re.sub(r"\s+", " ", str(s).strip().upper())
    dow_by_name = {}
    for d in deals.get("dealOfWeek", []):
        dow_by_name.setdefault(_norm(d["product"]), []).append(d)
    for p in deals.get("powerDeals", []):
        conns = dow_by_name.get(_norm(p["product"]), [])
        p["dowConns"] = [{"product": m["product"], "tier": m["tier"],
                          "orig": m["orig"], "now": m["now"], "disc": m["disc"],
                          "sold": m["sold"], "revenue": m["revenue"], "stock": m["stock"],
                          "locations": m.get("locations", [])}
                         for m in conns]
        p["dowConnCount"] = len(conns)


def _read_deals(month_name):
    """Power Deals & Deal of the Week for the given month (Kenya sheet). Columns:
    A Tier · B Month · C Product · D Location · E Type · F Original · G Current · H Discount.
    Type = 'Power Deals' (Tier 'All', run all month) or 'Deal of the Week' (Tier 1/2, per
    location, phased). Deal-of-week rows are deduped by product across locations."""
    try:
        from google_auth import get_gspread_client
        gc = get_gspread_client()
        rows = gc.open_by_key(DEALS_SHEET_ID).worksheet("Kenya").get_all_values()
    except Exception:                                            # noqa: BLE001
        return None

    def _pn(v):
        try:
            return int(round(float(str(v).replace(",", "").strip() or 0)))
        except (ValueError, TypeError):
            return 0

    # Sheet location labels → the shop name we use elsewhere.
    LOC_ALIASES = {"nairobi town": "Starmall"}

    power, dow = [], {}
    dow_rows = 0
    for r in rows[1:]:
        if len(r) < 8:
            continue
        tier, mon, prod, loc, typ = (str(r[0]).strip(), str(r[1]).strip(), str(r[2]).strip(),
                                     str(r[3]).strip(), str(r[4]).strip())
        loc = LOC_ALIASES.get(loc.lower(), loc)
        if not prod or mon.lower() != month_name.lower():
            continue
        item = {"tier": tier, "product": prod, "location": loc,
                "orig": _pn(r[5]), "now": _pn(r[6]), "disc": _pn(r[7])}
        if typ.lower().startswith("power"):
            power.append(item)
        elif typ.lower().startswith("deal"):
            dow_rows += 1
            k = (prod.upper(), tier.upper())
            e = dow.setdefault(k, {"product": prod, "tier": tier, "orig": item["orig"],
                                   "now": item["now"], "disc": item["disc"], "locations": []})
            if loc and loc not in e["locations"]:
                e["locations"].append(loc)

    dow_list = sorted(dow.values(), key=lambda x: (-x["disc"], x["product"]))
    locs = sorted({l for d in dow_list for l in d["locations"]})
    return {
        "month": month_name,
        "powerDeals": sorted(power, key=lambda x: (-x["disc"], x["product"])),
        "dealOfWeek": dow_list,
        "powerCount": len(power),
        "dowProducts": len(dow_list),
        "dowRows": dow_rows,
        "dowLocations": len(locs),
        "locations": locs,
        "powerDisc": sum(p["disc"] for p in power),
        "dowDisc": sum(d["disc"] for d in dow_list),
    }


def build_payload(m_start, m_end):
    """Query + shape the self-made/running split and the combo-request log for the
    given month window (Kenya tills). Assumes the DB connection is already up — the
    caller checks. Shared by fetch() (live month) and monthly_report.py (report
    month, possibly pinned to a past month), so both stay in sync."""
    month = m_start.strftime("%B %Y")
    df = db.run_query(COMBO_SQL, {"start_date": m_start.isoformat(),
                                  "end_date": m_end.isoformat()})
    self_made, running = [], []
    sold_units = {}          # tmpl_id -> units sold this month (self-made only)
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            row = {"name": str(r["product"]).strip(),
                   "qty": int(r["qty"] or 0),
                   "value": int(r["value"] or 0),
                   "colourOptions": int(r["colour_options"] or 0)}
            is_cbr = bool(r["is_cbr"])
            # Running = an official combo offering the full POS range (include_all);
            # self-made = a CBR request (a fixed pairing). A fixed non-CBR combo
            # (no include_all) is not a running combo, so it groups with self-made.
            is_running = bool(r["include_all"]) and not is_cbr
            if is_running:
                row["tmpl"] = int(r["tmpl_id"]) if pd.notna(r["tmpl_id"]) else None
                running.append(row)
            else:
                self_made.append(row)
                if pd.notna(r["tmpl_id"]):
                    tid = int(r["tmpl_id"])
                    sold_units[tid] = sold_units.get(tid, 0) + row["qty"]

    # Combo-request log
    rq = db.run_query(REQUEST_SQL, {"start_date": m_start.isoformat(),
                                    "end_date": m_end.isoformat()})
    requests = []
    st_counts = {"approved": 0, "rejected": 0, "pending": 0, "other": 0}
    if rq is not None and not rq.empty:
        for _, r in rq.iterrows():
            state = str(r["state"] or "").strip().lower()
            tid = int(r["tmpl_id"]) if pd.notna(r["tmpl_id"]) else None
            requests.append({
                "cbr": str(r["cbr"] or "").strip(),
                "combo": str(r["combo"] or "").strip(),
                "shop": str(r["shop"] or "—").strip(),
                "by": str(r["requested_by"] or "—").strip(),
                "state": state,
                "lloyd": bool(r["lloyd"]),
                "price": int(round(float(r["price"] or 0))),
                "on": _dstr(r["requested_on"]),
                "decided": _dstr(r["decided_on"]),
                "reject": str(r["reject_reason"] or "").strip(),
                "soldUnits": sold_units.get(tid, 0) if tid is not None else 0,
            })
            if state in ("approved",):
                st_counts["approved"] += 1
            elif state in ("rejected", "reject"):
                st_counts["rejected"] += 1
            elif state in ("draft", "pending", "requested", "to approve", "submitted"):
                st_counts["pending"] += 1
            else:
                st_counts["other"] += 1

    def agg(rows):
        _co = [x["colourOptions"] for x in rows]
        return {"count": len(rows),
                "units": sum(x["qty"] for x in rows),
                "value": sum(x["value"] for x in rows),
                "avgColours": round(sum(_co) / len(_co), 1) if _co else 0}

    # ── Weekly sales (Sun-Sat) + beat-August goal + running-combo cards ──
    offer = _read_offer_analysis() or {}
    stock_map = offer.get("stockMap", {})
    bag_targets = offer.get("bagTargets", {})
    # Recognise any bag that has stock OR a target, so 0-stock bags (e.g. NEO MAN,
    # GYM BAG — which live in targets, not the stock sheet) still resolve.
    known = set(stock_map.keys()) | set(bag_targets.keys())
    # Stocked bags first, then target-only bags (NEO MAN, GYM BAG, SAFIRI BP…), so a
    # fuzzy prefix like "SAFIRI" resolves to the stocked SAFIRI TRAVEL, not SAFIRI BP.
    bag_types = list(stock_map.keys()) + [k for k in bag_targets if k not in stock_map]
    # Combo-sheet wording → actual bag type (the attendant's names differ from the
    # catalogue): Laptop Backpack = CODE 3, Neo Man Bag = NEO MAN, Standard Travel
    # = TRAVEL (also bare "Standard"), Gym Bag = GYM BAG.
    BAG_ALIASES = {
        "STANDARD": "TRAVEL", "STANDARD TRAVEL": "TRAVEL",
        "LAPTOP BACKPACK": "CODE 3", "NEO MAN BAG": "NEO MAN", "NEO MAN": "NEO MAN",
        "GYM BAG": "GYM BAG",
    }

    def _match_bag(tok):
        tok = tok.strip().upper()
        if len(tok) < 2:
            return None
        tok = BAG_ALIASES.get(tok, tok)
        if tok in known:
            return tok
        ns = tok.replace(" ", "")
        for bt in bag_types:
            if (bt == tok or bt.replace(" ", "") == ns or tok in bt.split(" ")
                    or bt.startswith(tok + " ") or tok.startswith(bt)):
                return bt
        return None

    def _combo_bags(name):
        """Component bags of a POS combo name → (all bags, picks). Groups split on
        '+' (Kenya) or ' x '/'×' (Sinza & Uganda write combos as 'A x B'),
        alternatives on '/' or ' or '; the pick is the highest-Kenya-stock
        alternative in each group (the ★)."""
        all_b, picks = [], []
        for g in re.split(r"\s*\+\s*|\s+[x×]\s+", str(name), flags=re.I):
            best, best_s = None, -1
            for a in re.split(r"\s+or\s+|/", g, flags=re.I):
                b = _match_bag(a)
                if b:
                    if b not in all_b:
                        all_b.append(b)
                    s = stock_map.get(b, 0)
                    if s > best_s:
                        best, best_s = b, s
            if best and best not in picks:
                picks.append(best)
        return all_b, picks

    def _anchor_sunday(d):
        # Sunday on/before d (Postgres DOW: Sunday=0). Python weekday(): Mon=0..Sun=6.
        return d - datetime.timedelta(days=(d.weekday() + 1) % 7)

    def _month_weekly(s, e):
        d = db.run_query(MONTH_WEEKLY_SQL, {"start_date": s.isoformat(),
                                            "end_date": e.isoformat(), "anchor": _anchor_sunday(s)})
        wk = {}
        if d is not None and not d.empty:
            for _, x in d.iterrows():
                wk[int(x["wk"])] = int(x["units"] or 0)
        return wk

    # Per-combo weekly (this month) → {tmpl: {wk: units}}
    pw = db.run_query(COMBO_WEEKLY_SQL, {"start_date": m_start.isoformat(),
                                         "end_date": m_end.isoformat(), "anchor": _anchor_sunday(m_start)})
    per_combo, max_wk = {}, 1
    week_combos = {}   # wk -> {combo name: units} (all combos, for the weekly breakdown)
    if pw is not None and not pw.empty:
        for _, x in pw.iterrows():
            t, w, u = int(x["tmpl_id"]), int(x["wk"]), int(x["units"] or 0)
            per_combo.setdefault(t, {})[w] = u
            max_wk = max(max_wk, w)
            _nm = str(x["product"]).strip()
            _wc = week_combos.setdefault(w, {})
            _wc[_nm] = _wc.get(_nm, 0) + u

    # September-so-far combos (all combos) + August baseline
    sept_wk = _month_weekly(m_start, m_end)
    max_wk = max([max_wk] + list(sept_wk.keys()))
    sept_total = sum(sept_wk.values())

    prev_end = m_start - datetime.timedelta(days=1)
    prev_start = prev_end.replace(day=1)
    aug_wk = _month_weekly(prev_start, prev_end)
    aug_span = max(list(aug_wk.keys()) + [1])
    aug_weekly = [aug_wk.get(i, 0) for i in range(1, aug_span + 1)]
    aug_total = sum(aug_weekly)
    aug_active = len([w for w in aug_weekly if w > 0]) or 1

    weeks_left = int(offer.get("weeksRemaining") or 4) or 4
    remaining = max(aug_total + 1 - sept_total, 0)
    weekly_to_beat = -(-remaining // weeks_left) if weeks_left else remaining
    # Weekly detail: this-month vs last-month per Sun-Sat week, with each week's
    # target = last month's same week, and the combos that sold that week — so a
    # week that misses its target shows which combos did (and didn't) carry it.
    _span = max(max_wk, len(aug_weekly))
    weekly_detail = []
    for _i in range(1, _span + 1):
        _cs = sorted(week_combos.get(_i, {}).items(), key=lambda kv: -kv[1])
        weekly_detail.append({
            "wk": _i,
            "cur": (sept_wk.get(_i, 0) if _i <= max_wk else None),   # None = week not reached yet
            "prev": (aug_weekly[_i - 1] if _i - 1 < len(aug_weekly) else 0),
            "combos": [{"name": _n, "units": _u} for _n, _u in _cs[:8]],
        })

    combos_goal = {
        "augLabel": prev_start.strftime("%B"), "septLabel": m_start.strftime("%B"),
        "augTotal": aug_total, "augWeekly": aug_weekly, "augAvg": round(aug_total / aug_active),
        "septSoFar": sept_total, "weeksLeft": weeks_left, "weeklyToBeat": weekly_to_beat,
        "beaten": sept_total > aug_total, "curWeek": max_wk, "weeklyDetail": weekly_detail,
    }

    # ── Offer Sales vs Stock Guidance (borrowed from Offer Type Analysis) ──
    # Per offer-sheet combo: stock, weekly gain, remaining-to-target (highest-stock
    # bag per group ★, halved) + a verdict — the data behind the guidance chart.
    def _num2(v):
        try:
            return float(str(v).replace(",", "").replace("%", "").strip() or 0)
        except (ValueError, TypeError):
            return 0.0

    def _offer_trend():
        combos = offer.get("combos", [])
        headers = offer.get("comboHeaders", [])
        norm = [str(h).upper().replace(" ", "") for h in headers]
        price_i, weeks_i = 1, []
        for i, h in enumerate(norm):
            if h == "PRICE" and price_i == 1:
                price_i = i
            mm = re.match(r"^WK(\d+)$", h)
            if mm:
                weeks_i.append(i)
        if not weeks_i:
            weeks_i = [2, 3]
        out = []
        for r in combos:
            name = str(r[0]).strip()
            if not name or "TOTAL" in name.upper():
                continue
            wk_vals = [_num2(r[i]) if i < len(r) else 0 for i in weeks_i]
            sales = int(sum(wk_vals))                       # total sales across the weekly columns
            gain = int(wk_vals[-1] - wk_vals[-2]) if len(wk_vals) > 1 else 0
            all_b, picks = _combo_bags(name)
            stock = int(sum(stock_map.get(b, 0) for b in all_b))
            is_single = len(all_b) == 1 and all_b[0] == name.upper()
            raw_t = sum(bag_targets.get(b, {}).get("target", 0) for b in picks)
            raw_r = sum(bag_targets.get(b, {}).get("remaining", 0) for b in picks)
            tgt = int(raw_t if is_single else round(raw_t / 2))
            rem = int(raw_r if is_single else round(raw_r / 2))
            wk_tgt = int(-(-rem // weeks_left)) if weeks_left else rem
            price = int(_num2(r[price_i])) if price_i < len(r) else 0
            _lead = "%d sold so far. " % sales
            if stock == 0:
                advice = _lead + "Out of stock — pause the push until restocked."
            elif gain > 0:
                advice = _lead + "Sales rising — keep the momentum, %d/wk is the goal." % wk_tgt
            elif gain < 0:
                advice = _lead + "Sales slowing — push harder to hit %d/wk with %d in stock." % (wk_tgt, stock)
            else:
                advice = _lead + "Sales steady — hold the effort to keep %d/wk." % wk_tgt
            out.append({"name": name, "stock": stock, "gain": gain, "rem": rem, "sales": sales,
                        "target": tgt, "weekTgt": wk_tgt, "price": price, "advice": advice})
        return out

    offer_trend = _offer_trend()
    offer_kpis = {
        "combos": offer.get("comboCount"), "powerDeals": offer.get("powerDealCount"),
        "kenyaStock": offer.get("totalKenyaStock"), "kenyaTotal": 10192,
    }

    # ── Top bags clients keep pairing in self-made combos ─────────
    # Which bag types recur most across the CBR combos (weighted by units sold),
    # and whether each is already offered in an official/running combo — a bag that
    # clients keep self-combining but that we never put in an official combo is a
    # gap worth closing. Stock shown so a low-stock favourite is flagged.
    sm_freq, sm_in = {}, {}
    for _r in self_made:
        _bags, _ = _combo_bags(_r["name"])
        for _b in _bags:
            sm_freq[_b] = sm_freq.get(_b, 0) + _r["qty"]
            sm_in.setdefault(_b, set()).add(_r["name"])
    official_bags = set()
    for _oc in offer.get("combos", []):
        _nm = str(_oc[0]).strip()
        if _nm and "TOTAL" not in _nm.upper():
            _ob, _ = _combo_bags(_nm)
            official_bags.update(_ob)
    running_bags = set()
    for _r in running:
        _rb, _ = _combo_bags(_r["name"])
        running_bags.update(_rb)
    top_bags = []
    for _b, _freq in sorted(sm_freq.items(), key=lambda kv: (-kv[1], kv[0]))[:6]:
        top_bags.append({
            "bag": _b, "times": _freq, "combos": len(sm_in.get(_b, [])),
            "inOfficial": _b in official_bags, "inRunning": _b in running_bags,
            "stock": int(stock_map.get(_b, 0)),
        })
    top6_set = {tb["bag"] for tb in top_bags}
    # bag → the self-made combos built on it (for the running-combo cross-sell hover)
    sm_by_bag = {}
    for _r in self_made:
        _bags, _ = _combo_bags(_r["name"])
        for _b in set(_bags):
            sm_by_bag.setdefault(_b, []).append(
                {"name": _r["name"], "qty": _r["qty"], "value": _r["value"]})

    # Actual bags PRINTED inside each combo sale (per template) — Odoo records the
    # chosen components in combo_product_attribute_values, so a bundle like
    # "Mega + Man Bag or Mini Umbra or Neo Man Bag" is attributed to the exact bag
    # the customer picked, not just the bundle.
    import ast as _ast
    comp_by_tmpl, comp_by_bag = {}, {}
    _cc = db.run_query(COMBO_COMPONENTS_SQL, {"start_date": m_start.isoformat(),
                                              "end_date": m_end.isoformat()})
    if _cc is not None and not _cc.empty:
        for _, _cr in _cc.iterrows():
            _tid = int(_cr["tmpl_id"]) if pd.notna(_cr["tmpl_id"]) else None
            _q = int(_cr["qty"] or 0)
            _raw = str(_cr["attrs"] or "").strip()
            _names = []
            if _raw:
                try:
                    _parsed = _ast.literal_eval(_raw)
                    for _d in (_parsed if isinstance(_parsed, list) else [_parsed]):
                        if isinstance(_d, dict):
                            for _v in _d.values():
                                if isinstance(_v, dict) and _v.get("full_name_product"):
                                    _names.append(str(_v["full_name_product"]))
                except (ValueError, SyntaxError):
                    _names = []
            for _nm in _names:
                _bag = _match_bag(_nm) or _nm.strip().upper().split(" ")[0]
                _d = comp_by_tmpl.setdefault(_tid, {})
                _d[_bag] = _d.get(_bag, 0) + _q
                comp_by_bag[_bag] = comp_by_bag.get(_bag, 0) + _q

    running_cards = []
    for row in running:
        t = row.get("tmpl")
        pcw = per_combo.get(t, {})
        weeks = [{"label": "Wk %d" % i, "sold": pcw.get(i, 0)} for i in range(1, max_wk + 1)]
        total = row["qty"]
        all_b, picks = _combo_bags(row["name"])
        _comp = comp_by_tmpl.get(t, {})
        bags = [{"name": b, "stock": stock_map.get(b, 0), "star": b in picks, "sold": _comp.get(b, 0)} for b in all_b]
        last = weeks[-1]["sold"] if weeks else 0
        prev = weeks[-2]["sold"] if len(weeks) > 1 else last
        # Guidance (same rule as Offer Sales vs Stock Guidance): remaining-to-target
        # from the highest-stock bag per group (★), halved, and a weekly target.
        is_single = len(all_b) == 1 and all_b[0] == row["name"].strip().upper()
        raw_t = sum(bag_targets.get(b, {}).get("target", 0) for b in picks)
        raw_r = sum(bag_targets.get(b, {}).get("remaining", 0) for b in picks)
        target = int(raw_t if is_single else round(raw_t / 2))
        remaining = int(raw_r if is_single else round(raw_r / 2))
        week_tgt = int(-(-remaining // weeks_left)) if weeks_left else remaining
        # Cross-sell: which top-6 bag(s) this running combo shares, and the self-made
        # (CBR) combos built on the same bag — so the money the official combo made
        # can be read against the money "shifted" into self-made combos.
        conns, seen_sm = [], {}
        for b in all_b:
            if b in top6_set:
                sm = sm_by_bag.get(b, [])
                conns.append({"bag": b, "selfMade": sm,
                              "smUnits": sum(x["qty"] for x in sm),
                              "smValue": sum(x["value"] for x in sm)})
                for x in sm:
                    seen_sm[x["name"]] = x          # dedup a combo shared across bags
        running_cards.append({
            "name": row["name"], "price": round(row["value"] / row["qty"]) if row["qty"] else 0,
            "value": row["value"], "colourOptions": row.get("colourOptions", 0),
            "weeks": weeks, "total": total, "avg": round(total / max_wk) if max_wk else 0,
            "bags": bags, "totalStock": sum(b["stock"] for b in bags),
            "target": target, "remaining": remaining, "weekTgt": week_tgt,
            "diff": last - prev,
            "connections": conns,
            "connUnits": sum(x["qty"] for x in seen_sm.values()),
            "connValue": sum(x["value"] for x in seen_sm.values()),
            "connCombos": len(seen_sm),
            "lastLabel": weeks[-1]["label"] if weeks else "Wk 1",
            "prevLabel": weeks[-2]["label"] if len(weeks) > 1 else (weeks[-1]["label"] if weeks else "Wk 1"),
        })

    for row in running:            # tmpl was only needed to build the cards
        row.pop("tmpl", None)

    # ── Sinza & Uganda region guidance cards (combos from the COMBOS sheet) ──
    # Each combo → price (col B), per-week sales, total, component-bag stock in that
    # region, and a sales-vs-stock verdict — rendered like the Kenya running cards.
    def _rnum(x):
        try:
            return int(round(float(str(x).replace(",", "").strip() or 0)))
        except (ValueError, TypeError):
            return 0

    def _region_cards(combos, headers, region_stock):
        norm = [str(h).upper().replace(" ", "") for h in (headers or [])]
        price_i, wk_i, wk_l = 1, [], []
        for i, h in enumerate(norm):
            if h == "PRICE" and price_i == 1:
                price_i = i
            mo = re.match(r"^WK(\d+)$", h)
            if mo:
                wk_i.append(i)
                wk_l.append("Wk " + mo.group(1))
        cards = []
        for row in combos or []:
            name = str(row[0]).strip() if row else ""
            if not name or name.upper().startswith("TOTAL"):
                continue
            price = _rnum(row[price_i]) if price_i < len(row) else 0
            weeks = [{"label": wk_l[j], "sold": _rnum(row[wk_i[j]]) if wk_i[j] < len(row) else 0}
                     for j in range(len(wk_i))]
            total = sum(w["sold"] for w in weeks)
            all_b, picks = _combo_bags(name)
            bags = [{"name": b, "stock": int(region_stock.get(b, 0)), "star": b in picks} for b in all_b]
            stock = int(sum(region_stock.get(b, 0) for b in (picks or all_b)))
            last = weeks[-1]["sold"] if weeks else 0
            prev = weeks[-2]["sold"] if len(weeks) > 1 else last
            cards.append({
                "name": name, "price": price, "weeks": weeks, "total": total,
                "avg": round(total / len(weeks)) if weeks else 0,
                "bags": bags, "stock": stock, "diff": last - prev,
                "lastLabel": weeks[-1]["label"] if weeks else "Wk 1",
            })
        return cards

    def _groups(specs, stock):
        out = []
        for key, label, cards_k, hdr_k in specs:
            cards = _region_cards(offer.get(cards_k), offer.get(hdr_k), stock)
            if cards:
                out.append({"key": key, "label": label, "cards": cards})
        return out

    _sz_stock, _ug_stock = offer.get("sinzaStock", {}), offer.get("ugStock", {})
    regions = {
        "sinza": {
            "label": "Sinza", "currency": "TSh",
            "totalStock": offer.get("totalSinzaStock"),
            "groups": _groups([
                ("combos",   "Combos",   "sinzaCombos",   "sinzaComboHeaders"),
                ("singles",  "Singles",  "sinzaSingles",  "sinzaSinglesHeaders"),
                ("specials", "Specials", "sinzaSpecials", "sinzaSpecialHeaders"),
            ], _sz_stock),
        },
        "uganda": {
            "label": "Uganda", "currency": "USh",
            "totalStock": offer.get("totalUgandaStock"),
            "groups": _groups([
                ("combos",  "Combos",  "ugCombos",  "ugComboHeaders"),
                ("singles", "Singles", "ugSingles", "ugSinglesHeaders"),
            ], _ug_stock),
        },
    }

    return {
        "month": month,
        "monthStart": m_start.isoformat(), "monthEnd": m_end.isoformat(),
        "selfMade": self_made, "running": running,
        "smTotals": agg(self_made), "runTotals": agg(running),
        "requests": requests, "reqCounts": st_counts,
        "reqTotal": len(requests),
        "runningCards": running_cards, "combosGoal": combos_goal,
        "offerTrend": offer_trend, "offerKpis": offer_kpis,
        "topBags": top_bags,
        "regions": regions,
    }


def fetch():
    m_start, m_end = report_month.live_month_window()
    ok, _ = db.check_connection()
    if not ok:
        print("  Postgres not reachable — self_made_combos not updated.")
        return None
    payload = build_payload(m_start, m_end)
    deals = _read_deals(m_start.strftime("%B"))               # Power Deals / Deal of the Week
    if deals:
        _stock = (_read_offer_analysis() or {}).get("stockMap", {})
        _enrich_deals(deals, m_start, m_end, _stock)
    payload["deals"] = deals
    return payload


def inject(payload):
    with open(HTML, "r", encoding="utf-8") as f:
        html = f.read()
    block = ("<!-- SMC_DATA_START -->\n<script>\nconst SMC = "
             + json.dumps(payload, ensure_ascii=False) + ";\n</script>\n<!-- SMC_DATA_END -->")
    html = re.sub(r"<!-- SMC_DATA_START -->.*?<!-- SMC_DATA_END -->", block, html, flags=re.DOTALL)
    # Embed the offer/combo data block here too, so the Monthly Report reads it from
    # this page (Offer Type Analysis has been retired). Function replacement avoids
    # re.sub treating backslashes in the block as backreferences.
    try:
        import offer_data
        oa_block = offer_data.build()[1]
        html = re.sub(r"<!-- OFFER_DATA_START -->.*?<!-- OFFER_DATA_END -->",
                      lambda _m: oa_block, html, flags=re.DOTALL)
    except Exception:
        pass
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    payload = fetch()
    if payload is None:
        return
    inject(payload)
    sm, run = payload["smTotals"], payload["runTotals"]
    rc = payload["reqCounts"]
    print(f"self_made_combos.html updated — {payload['month']} (Kenya).")
    print(f"  Self-made combos : {sm['count']} combos · {fmt(sm['units'])} units · KES {fmt(sm['value'])}")
    print(f"  Running combos   : {run['count']} combos · {fmt(run['units'])} units · KES {fmt(run['value'])}")
    print(f"  Combo requests   : {payload['reqTotal']} logged "
          f"({rc['approved']} approved · {rc['rejected']} rejected · {rc['pending']} pending)")
    if not os.environ.get("DENRI_LAUNCHER"):
        webbrowser.open_new_tab(pathlib.Path(HTML).as_uri())


if __name__ == "__main__":
    main()
