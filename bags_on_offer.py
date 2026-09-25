"""
bags_on_offer.py
─────────────────────────────────────────────────────────────────
Bags on offer vs bags not on offer vs others — Kenya, for three periods
(Monthly = live month to date, Weekly = current Sun–Sat week, Last week = previous
complete Sun–Sat week).

On offer     = combo products (running + self-made, name "A + B") and single sales of any
               bag that is a running-combo component, a Deal of the Week or a Power Deal.
Not on offer = every other catalogue bag sold, plus the month's new products (MONTHLY_TARGET
               col I) that are on no offer — even ones not in the price catalogue yet.
Others       = gift bags (POS) and corporate sales (customer invoices).

The on-offer bag set comes from self_made_combos.py (bags_offer_source.json), and bags are
resolved with the same self_made_combos.bag_classifier(), so the Monthly not-on-offer money
matches Menu 4's "Bags not on offer" panel (plus new products it can't resolve). Per shop,
till revenue is compared with its Odoo target (sales_pos_target, month or week) and ranked
within its region (docs/shop-regions.md); a shop behind its pro-rated target AND below its
region's pace (Kenya-wide pace for a one-shop region) is flagged red.

Spec: docs/bags-on-offer.md. Injects `BOO` into bags_on_offer.html between the
BOO_DATA markers.
─────────────────────────────────────────────────────────────────
"""

import os, re, json, time, datetime, webbrowser, pathlib

from lib import db, report_month
import self_made_combos as smc

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "bags_on_offer.html")
SOURCE_JSON = os.path.join(BASE, "bags_offer_source.json")
NEW_PRODUCTS_SHEET = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"   # same sheet as new_products.py

_KENYA_TILLS = "AND lower(COALESCE(pc.\"name\",'')) NOT IN ('sinza','dar-es-alam','uganda')"

# Every Kenya POS line by shop × product × day — same product filters as
# self_made_combos._bag_sales_sql, except combo products ("A + B") and gift bags are KEPT
# (combos are on offer; gift bags go to Others).
LINES_SQL = f"""
SELECT UPPER(COALESCE(pc."name",'?')) AS shop, UPPER(pt."name") AS name, p.date_order::date AS d,
       SUM(pl.qty)::int AS units, ROUND(SUM(pl.price_subtotal_incl))::int AS revenue
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
LEFT JOIN product_product pp ON pl.product_id=pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done','paid') AND pl.qty <> 0
  {_KENYA_TILLS}
  AND pt."name" NOT ILIKE '%delivery%' AND pt."name" NOT ILIKE '%customi%'
  AND pt."name" NOT ILIKE '%strap%'
GROUP BY 1, 2, 3
"""

# Total till revenue per shop per day (every line) — what the Odoo target is set against.
TILL_SQL = f"""
SELECT UPPER(COALESCE(pc."name",'?')) AS shop, p.date_order::date AS d,
       ROUND(SUM(pl.price_subtotal_incl))::bigint AS revenue
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done','paid')
  {_KENYA_TILLS}
GROUP BY 1, 2
"""

# Corporate sales per day — customer invoices, same qualifying rule as sql/corporate_bags.sql
# (posted out_invoice; paid / in payment, or at most 25% still outstanding).
CORPORATE_SQL = """
WITH qinv AS (
    SELECT am.id, am.invoice_date
    FROM account_move am
    WHERE am.move_type = 'out_invoice' AND am.state = 'posted'
      AND am.invoice_date BETWEEN :s AND :e
      AND ( am.payment_state IN ('paid', 'in_payment')
            OR (am.amount_total > 0 AND am.amount_residual / am.amount_total <= 0.25) )
)
SELECT qinv.invoice_date AS d, COALESCE(SUM(aml.quantity), 0)::int AS units,
       ROUND(COALESCE(SUM(aml.price_total), 0))::bigint AS revenue
FROM account_move_line aml JOIN qinv ON qinv.id = aml.move_id
WHERE aml.display_type IS NULL AND aml.product_id IS NOT NULL
GROUP BY 1
"""

# Odoo revenue targets (per till, plus the corporate row) overlapping the date range.
TARGET_SQL = """
SELECT COALESCE(UPPER(pc."name"), 'CORPORATE') AS shop, t.target_scope AS scope, t.period,
       t.start_date, t.end_date, t.target_amount::float AS target, t.write_date
FROM sales_pos_target t LEFT JOIN pos_config pc ON pc.id = t.config_id
WHERE t.period IN ('month', 'week') AND t.target_scope IN ('pos', 'corporate')
  AND t.start_date <= :e AND t.end_date >= :s
"""

# Bags printed inside combos, per day: the exact bag + colour chosen on each combo line
# (combo_product_attribute_values — same source as Menu 4's component attribution).
COMBO_PRINTS_SQL = f"""
SELECT p.date_order::date AS d, UPPER(pt."name") AS name, SUM(pl.qty)::int AS units,
       COALESCE(pl.combo_product_attribute_values, '') AS attrs
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
LEFT JOIN product_product pp ON pl.product_id=pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done','paid') AND pl.qty <> 0
  {_KENYA_TILLS}
  AND pt."name" LIKE '%+%' AND pt."name" NOT ILIKE '%delivery%' AND pt."name" NOT ILIKE '%customi%'
GROUP BY 1, 2, 4
"""

# Counted by how it was sold: a combo-button sale is a Combo sale; a SINGLE sale of a bag on
# several offers goes to the first of these — a Power Deal runs at every shop all month, so it
# wins over a Deal of the Week; a combo bag sold singly is the fallback.
_SOURCE_ORDER = ["Power Deal", "Deal of the Week", "Combo component"]
_NON_KENYA = ("SINZA", "DAR-ES-ALAM", "UGANDA", "?")


def _load_source(month_label):
    """bags_offer_source.json if written in the last 15 min for this month; else rebuild it
    live via self_made_combos.fetch() (which also refreshes the file)."""
    try:
        if os.path.exists(SOURCE_JSON) and (time.time() - os.path.getmtime(SOURCE_JSON)) < 900:
            with open(SOURCE_JSON, encoding="utf-8") as f:
                d = json.load(f)
            if d.get("onOffer") and d.get("month") == month_label:
                print("  On-offer source  : bags_offer_source.json (fresh, <15 min)")
                return d
    except (OSError, ValueError):
        pass
    print("  On-offer source  : rebuilding live via self_made_combos.fetch() …")
    payload = smc.fetch()
    if payload is None:
        return None
    smc.write_bags_offer_source(payload)
    try:
        with open(SOURCE_JSON, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _previous_payload():
    try:
        with open(HTML, encoding="utf-8") as f:
            m = re.search(r"const BOO = (.*?);\n</script>", f.read(), re.S)
        return json.loads(m.group(1)) if m else None
    except (OSError, ValueError):
        return None


def _new_products():
    """This month's new products: new_products.txt when it lists any (lib/new_products_list),
    else MONTHLY_TARGET col A where col I is ticked. Falls back to the previous build's list
    if the sheet can't be read."""
    from lib import new_products_list
    listed = new_products_list.names()
    if listed:
        print(f"  New products     : {len(listed)} from new_products.txt")
        return listed

    def _ticked(v):
        v = str(v).strip()
        return any(c in v for c in "✅✔✓") or v.upper() in ("TRUE", "1", "YES")
    try:
        from google_auth import get_gspread_client
        rows = get_gspread_client().open_by_key(NEW_PRODUCTS_SHEET).worksheet("MONTHLY_TARGET").get_all_values()
        names = [r[0].strip().upper() for r in rows[1:] if len(r) > 8 and r[0].strip() and _ticked(r[8])]
        print(f"  New products     : {len(names)} from MONTHLY_TARGET")
        return names
    except Exception as e:                                   # noqa: BLE001
        prev = (_previous_payload() or {}).get("newProducts") or []
        print(f"  New products     : sheet unreadable ({type(e).__name__}); reusing {len(prev)} from last build")
        return prev


def _shop_label(till):
    return smc._SHOP_TO_LOC.get(till, till.title())


def _region_of(label):
    return smc._SHOP_REGION.get(label.upper(), "Other")


def _windows(today, m_start, m_end):
    ws = today - datetime.timedelta(days=(today.weekday() + 1) % 7)       # Sunday of this week
    d = datetime.timedelta
    return {
        "monthly":  {"label": "Monthly", "start": m_start, "end": m_end, "upto": min(m_end, today),
                     "period": "month", "days": (m_end - m_start).days + 1, "trend": "week"},
        "weekly":   {"label": "Weekly", "start": ws, "end": ws + d(days=6), "upto": today,
                     "period": "week", "days": 7, "trend": "day"},
        "lastweek": {"label": "Last week", "start": ws - d(days=7), "end": ws - d(days=1),
                     "upto": ws - d(days=1), "period": "week", "days": 7, "trend": "day"},
    }


def _pick_target(rows, shop, period, start, end):
    """Latest target row for `shop` with this period that overlaps [start, end]."""
    best = None
    for r in rows:
        if r["shop"] != shop or r["period"] != period:
            continue
        if not (r["start_date"] <= end and r["end_date"] >= start):
            continue
        key = (r["start_date"], str(r["write_date"] or ""))
        if best is None or key > best[0]:
            best = (key, r["target"])
    return best[1] if best and best[1] else None


def _build_period(w, lines, till, corp, target_rows, classify, extra_off, month_anchor, prints, cover):
    s, e = w["start"], w["end"]
    elapsed = max(1, min((min(w["upto"], e) - s).days + 1, w["days"]))
    frac = elapsed / w["days"]

    def blank():
        return {"units": 0, "revenue": 0}

    tot = {"on": blank(), "off": blank(), "oth": blank(), "unc": blank()}
    others = {"Gift bags": blank(), "Corporate": blank()}
    trend, by_source, on_bags, off_bags, unc_names, shops = {}, {}, {}, {}, set(), {}

    def tkey(d):
        if w["trend"] == "week":
            return (d - month_anchor).days // 7 + 1
        return d

    for r in lines:
        if not (s <= r["d"] <= e):
            continue
        side, bag, srcs, is_new, offers = classify(r["name"], r["shop"], r["d"])
        u, rev = r["units"], r["revenue"]
        tot[side]["units"] += u
        tot[side]["revenue"] += rev
        if side != "unc":
            trend.setdefault(tkey(r["d"]), {"on": 0, "off": 0, "oth": 0})[side] += rev
        if side == "on":
            src = by_source.setdefault(srcs[0], blank())
            src["units"] += u
            src["revenue"] += rev
            if srcs[0] != "Combo sale":
                b = on_bags.setdefault(bag, {"bag": bag, "sources": offers, "isNew": is_new,
                                             "bySource": {}, **blank()})
                b["units"] += u
                b["revenue"] += rev
                b["bySource"][srcs[0]] = b["bySource"].get(srcs[0], 0) + u
        elif side == "off":
            # "dowElsewhere": a Deal-of-the-Week bag sold at a shop / in a week the deal wasn't running.
            b = off_bags.setdefault(bag, {"isNew": is_new, "dowElsewhere": "Deal of the Week" in offers, **blank()})
            b["units"] += u
            b["revenue"] += rev
        elif side == "oth":
            others["Gift bags"]["units"] += u
            others["Gift bags"]["revenue"] += rev
        else:
            unc_names.add(r["name"])
        sh = shops.setdefault(r["shop"], {k: blank() for k in ("on", "off", "oth", "unc")})
        sh[side]["units"] += u
        sh[side]["revenue"] += rev

    in_combos = {}
    for r in prints:
        if s <= r["d"] <= e:
            in_combos[r["bag"]] = in_combos.get(r["bag"], 0) + r["units"]

    corp_rev = corp_units = 0
    for r in corp:
        if s <= r["d"] <= e:
            corp_rev += r["revenue"]
            corp_units += r["units"]
            trend.setdefault(tkey(r["d"]), {"on": 0, "off": 0, "oth": 0})["oth"] += r["revenue"]
    others["Corporate"] = {"units": corp_units, "revenue": corp_rev}
    tot["oth"]["units"] += corp_units
    tot["oth"]["revenue"] += corp_rev

    till_rev = {}
    for r in till:
        if s <= r["d"] <= e:
            till_rev[r["shop"]] = till_rev.get(r["shop"], 0) + r["revenue"]

    # ── Per-shop metrics vs the Odoo target ──
    shop_rows = []
    target_tills = {t["shop"] for t in target_rows if t["scope"] == "pos"}
    for tl in sorted(set(shops) | set(till_rev) | target_tills):
        if tl in _NON_KENYA:
            continue
        sh = shops.get(tl, {k: blank() for k in ("on", "off", "oth", "unc")})
        rev = till_rev.get(tl, 0)
        tgt = _pick_target(target_rows, tl, w["period"], s, e)
        if not rev and not tgt:
            continue
        label = _shop_label(tl)
        bag_rev = sh["on"]["revenue"] + sh["off"]["revenue"]
        shop_rows.append({
            "shop": label, "till": tl, "region": _region_of(label),
            "on": sh["on"], "off": sh["off"], "oth": sh["oth"],
            "onShare": round(sh["on"]["revenue"] / bag_rev * 100, 1) if bag_rev > 0 else None,
            "revenue": rev, "target": round(tgt) if tgt else None,
        })
    corp_tgt = _pick_target(target_rows, "CORPORATE", w["period"], s, e)
    if corp_rev or corp_tgt:
        shop_rows.append({
            "shop": "Corporate", "till": "CORPORATE", "region": "Corporate",
            "on": blank(), "off": blank(), "oth": {"units": corp_units, "revenue": corp_rev},
            "onShare": None, "revenue": corp_rev, "target": round(corp_tgt) if corp_tgt else None,
        })
    for x in shop_rows:
        t = x["target"]
        x["attain"] = round(x["revenue"] / t * 100, 1) if t else None
        x["pace"] = round(x["revenue"] / (t * frac) * 100, 1) if t else None
        x["behind"] = x["pace"] is not None and x["pace"] < 100

    def _pace_of(lst):
        tgt = sum(x["target"] for x in lst if x["target"])
        rev = sum(x["revenue"] for x in lst if x["target"])
        return round(rev / (tgt * frac) * 100, 1) if tgt else None

    kenya_pace = _pace_of([x for x in shop_rows if x["till"] != "CORPORATE"])
    regions = {}
    for x in shop_rows:
        regions.setdefault(x["region"], []).append(x)
    region_rows = []
    for reg, lst in regions.items():
        # Red = behind its pro-rated target AND below its benchmark — the region's pace (2+
        # targeted shops) or, for a one-shop region, the Kenya-wide POS pace.
        targeted = [x for x in lst if x["target"]]
        bench = _pace_of(lst) if len(targeted) >= 2 else kenya_pace
        kind = "region pace" if len(targeted) >= 2 else "Kenya pace"
        lst.sort(key=lambda x: (x["pace"] is None, -(x["pace"] or 0), -x["revenue"]))
        for i, x in enumerate(lst):
            x["benchmark"], x["benchmarkKind"] = bench, kind
            x["red"] = bool(x["behind"] and bench is not None and x["pace"] < bench)
            x["rank"] = i + 1
            x["leader"] = i == 0 and x["pace"] is not None and len(lst) > 1
        region_rows.append({
            "region": reg, "shops": [x["shop"] for x in lst],
            "revenue": sum(x["revenue"] for x in lst),
            "target": sum(x["target"] for x in lst if x["target"]) or None,
            "pace": _pace_of(lst), "redCount": sum(1 for x in lst if x["red"]),
        })
    region_rows.sort(key=lambda r: (r["region"] in ("Corporate", "Other"), -r["revenue"]))

    # Bags printed inside combos but never sold singly still belong in the bag tables.
    for bag, n in in_combos.items():
        if n <= 0 or bag in on_bags or bag in off_bags:
            continue
        side, bt, srcs, is_new, offers = classify(bag)
        if side == "on":
            on_bags[bag] = {"bag": bag, "sources": offers or srcs, "isNew": is_new, "bySource": {}, **blank()}
        elif side == "off":
            off_bags[bag] = {"isNew": is_new, "dowElsewhere": False, **blank()}

    off_list = []
    for bag, v in off_bags.items():
        if v["units"] <= 0 and in_combos.get(bag, 0) <= 0:
            continue
        x = cover.get(bag) or extra_off.get(bag, {})
        off_list.append({"bag": bag, "isNew": v["isNew"], "units": v["units"], "revenue": v["revenue"],
                         "dowElsewhere": v.get("dowElsewhere", False),
                         # combo prints are shown once — on the on-offer row when the bag has one
                         "inCombos": 0 if bag in on_bags else in_combos.get(bag, 0),
                         "stock": x.get("stock"), "avgPerDay": x.get("avgPerDay"),
                         "daysCover": x.get("daysCover")})
    off_list.sort(key=lambda x: (-x["revenue"], -x["inCombos"]))
    for b in on_bags.values():
        b["inCombos"] = in_combos.get(b["bag"], 0)
    on_list = sorted((b for b in on_bags.values() if b["units"] > 0 or b["inCombos"] > 0),
                     key=lambda x: (-x["revenue"], -x["inCombos"]))

    order = ["Combo sale"] + _SOURCE_ORDER
    src_rows = sorted(({"label": k, **v} for k, v in by_source.items()),
                      key=lambda x: order.index(x["label"]) if x["label"] in order else 99)

    trend_rows = []
    for k in sorted(trend):
        if w["trend"] == "week":
            ws = month_anchor + datetime.timedelta(days=7 * (k - 1))
            lo, hi = max(ws, s), min(ws + datetime.timedelta(days=6), e)
            lbl, sub = f"Wk {k}", f"{lo.strftime('%d %b')}–{hi.strftime('%d %b')}"
        else:
            lbl, sub = k.strftime("%a"), k.strftime("%d %b")
        trend_rows.append({"label": lbl, "sub": sub, **trend[k]})

    return {
        "label": w["label"],
        "range": f"{s.strftime('%d %b')} – {e.strftime('%d %b %Y')}",
        "daysElapsed": elapsed, "daysInPeriod": w["days"],
        "complete": elapsed >= w["days"],
        "trendBy": w["trend"],
        "kenyaPace": kenya_pace,
        "totals": tot,
        "others": [{"label": k, **v} for k, v in others.items()],
        "comboPrints": sum(in_combos.values()),
        "unclassifiedNames": sorted(unc_names)[:40],
        "unclassifiedCount": len(unc_names),
        "trend": trend_rows,
        "sources": src_rows,
        "onBags": on_list,
        "offBags": off_list,
        "shops": shop_rows,
        "regions": region_rows,
    }


def _as_date(v):
    return v if isinstance(v, datetime.date) else datetime.date.fromisoformat(str(v)[:10])


def fetch():
    m_start, m_end = report_month.live_month_window()
    today = datetime.date.today()
    month_label = m_start.strftime("%B %Y")
    month_anchor = m_start - datetime.timedelta(days=(m_start.weekday() + 1) % 7)  # Sunday on/before day 1
    wins = _windows(today, m_start, m_end)
    lo = min(w["start"] for w in wins.values())
    hi = max(w["end"] for w in wins.values())

    ok, msg = db.check_connection()
    if not ok:
        print(f"  DB unreachable — {msg}; bags_on_offer.html left unchanged.")
        return None
    src = _load_source(month_label)
    if not src:
        print("  No on-offer source — bags_on_offer.html left unchanged.")
        return None
    new_names = sorted(set(_new_products()), key=len, reverse=True)

    on_offer = src.get("onOffer", {})
    infer, is_on_offer = smc.bag_classifier(set(on_offer))
    # Per on-offer name: its own matcher, so a sold bag picks up the right source tags.
    per_name = [(smc.bag_classifier({n})[1], srcs) for n, srcs in on_offer.items()]

    def sources_of(bt):
        tags = []
        for match, srcs in per_name:
            if match(bt):
                tags += [x for x in srcs if x not in tags]
        return sorted(tags, key=lambda x: _SOURCE_ORDER.index(x) if x in _SOURCE_ORDER else 99)

    def new_of(name):
        n = re.sub(r"^\[[^\]]*\]\s*", "", name).strip()          # Odoo "[S_0] LAMORA …" codes
        for np in new_names:
            if n == np or n.startswith(np + " "):
                return np
        return None

    cache = {}

    # Where / when each Deal of the Week runs: (matcher, weeks, shop labels).
    dow_runs = [(smc.bag_classifier({r["product"]})[1], set(r.get("weeks") or []), set(r.get("locations") or []))
                for r in src.get("dowRuns", []) if r.get("product")]

    def base(name):
        """Name-only part of the classification (cached): gift bag / combo / unresolved, or a bag
        with its all-month offers (Power Deal, combo component) and its Deal-of-the-Week runs."""
        if name in cache:
            return cache[name]
        if name.startswith("GIFT BAG"):
            res = ("oth", "GIFT BAGS", [], False, [])
        elif "+" in name:
            res = ("combo", name, [], False, [])
        else:
            npn = new_of(name)
            bt = infer(name) or npn
            if not bt:
                res = ("unc", name, [], False, [])
            else:
                static = [x for x in sources_of(bt) if x != "Deal of the Week"] if is_on_offer(bt) else []
                runs = [(wk, locs) for match, wk, locs in dow_runs if match(bt)]
                res = ("bag", bt, static, bool(npn) or (bt in new_names), runs)
        cache[name] = res
        return res

    def classify(name, shop=None, d=None):
        """(side, bag, sources, isNew, allOffers) — side is on / off / oth / unc. A single sale is
        a Deal-of-the-Week sale only at a shop running that deal, in its tier's weeks (shop/d
        None = "anywhere", used for bags seen only inside combos). Sources are in counting
        order: Power Deal → Deal of the Week → Combo component."""
        kind, bt, static, is_new, runs = base(name)
        if kind == "oth":
            return ("oth", bt, ["Gift bags"], False, [])
        if kind == "combo":
            return ("on", bt, ["Combo sale"], False, [])
        if kind == "unc":
            return ("unc", bt, [], False, [])
        if shop is None:
            dow_ok = bool(runs)
        else:
            wk, loc = (d - month_anchor).days // 7 + 1, _shop_label(shop)
            dow_ok = any(wk in weeks and loc in locs for weeks, locs in runs)
        srcs = [x for x in ("Power Deal",) if x in static]
        if dow_ok:
            srcs.append("Deal of the Week")
        srcs += [x for x in ("Combo component",) if x in static]
        all_offers = sorted(set(static) | ({"Deal of the Week"} if runs else set()),
                            key=lambda x: _SOURCE_ORDER.index(x) if x in _SOURCE_ORDER else 99)
        return ("on" if srcs else "off", bt, srcs, is_new, all_offers)

    params = {"s": lo.isoformat(), "e": hi.isoformat()}

    def rows(sql):
        df = db.run_query(sql, params)
        out = [] if df is None else df.to_dict("records")
        for r in out:
            if "d" in r:
                r["d"] = _as_date(r["d"])
            for k in ("units", "revenue"):
                if k in r:
                    r[k] = int(r[k] or 0)
            for k in ("shop", "name"):
                if k in r:
                    r[k] = str(r[k])
        return out

    lines, till, corp, targets = rows(LINES_SQL), rows(TILL_SQL), rows(CORPORATE_SQL), rows(TARGET_SQL)

    # ── Bags printed inside combos (per day) ──
    import ast

    def resolve(n):
        n = re.sub(r"\s+", " ", str(n).strip().upper())
        n = re.sub(r"\s+COMBO$", "", n)
        return infer(n) or new_of(n) or (n.split(" or ")[0].split(" OR ")[0].strip() or None)

    prints = []
    for r in rows(COMBO_PRINTS_SQL):
        slots = r["name"].count("+") + 1
        picked = []
        raw = str(r.get("attrs") or "").strip()
        if raw:
            try:
                parsed = ast.literal_eval(raw)
                for dct in (parsed if isinstance(parsed, list) else [parsed]):
                    if isinstance(dct, dict):
                        picked += [str(v["full_name_product"]) for v in dct.values()
                                   if isinstance(v, dict) and v.get("full_name_product")]
            except (ValueError, SyntaxError):
                picked = []
        if picked:
            # Two identical bags (Jumbo Brown + Jumbo Brown) are stored as ONE entry — pad to
            # the combo's bag count so the pair counts as 2.
            picked += [picked[-1]] * max(0, slots - len(picked))
        else:
            picked = r["name"].split("+")                         # no attribute data (some CBRs)
        for nm in picked:
            bag = resolve(nm)
            if bag:
                prints.append({"d": r["d"], "bag": bag, "units": r["units"]})
    for t in targets:
        t["start_date"], t["end_date"] = _as_date(t["start_date"]), _as_date(t["end_date"])
        t["target"] = float(t["target"] or 0)

    nof = src.get("bagsNotOnOffer") or {}
    extra_off = {x["bag"]: x for x in nof.get("notOnOffer", [])}

    # Stock + days of cover for EVERY bag (point-in-time, same rule as Menu 4): today's Kenya
    # stock ÷ this month's pace on the days the bag actually sold (single sales + combo prints).
    stock_map = src.get("stockMap") or {}
    m_units, m_days = {}, {}
    for r in lines:
        if m_start <= r["d"] <= m_end:
            kind, bt = base(r["name"])[:2]
            if kind == "bag" and r["units"] > 0:
                m_units[bt] = m_units.get(bt, 0) + r["units"]
                m_days.setdefault(bt, set()).add(r["d"])
    for r in prints:
        if m_start <= r["d"] <= m_end and r["units"] > 0:
            m_units[r["bag"]] = m_units.get(r["bag"], 0) + r["units"]
            m_days.setdefault(r["bag"], set()).add(r["d"])
    cover = {}
    for bt in set(m_units) | set(stock_map):
        if bt not in stock_map:
            continue
        stk = stock_map[bt]
        avg = m_units.get(bt, 0) / len(m_days[bt]) if m_days.get(bt) else 0
        cover[bt] = {"stock": stk, "avgPerDay": round(avg, 1),
                     "daysCover": int(round(stk / avg)) if avg > 0 else None}

    periods = {k: _build_period(w, lines, till, corp, targets, classify, extra_off, month_anchor, prints, cover)
               for k, w in wins.items()}
    return {
        "month": month_label,
        "asOf": today.isoformat(),
        "generated": datetime.datetime.now().strftime("%d %b %Y %H:%M"),
        "newProducts": new_names,
        "menu4NotOnOfferRevenue": nof.get("notOnOfferRevenue"),
        "periods": periods,
    }


def inject(payload):
    with open(HTML, "r", encoding="utf-8") as f:
        html = f.read()
    block = ("<!-- BOO_DATA_START -->\n<script>\nconst BOO = "
             + json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str)
             + ";\n</script>\n<!-- BOO_DATA_END -->")
    html = re.sub(r"<!-- BOO_DATA_START -->.*?<!-- BOO_DATA_END -->", lambda _m: block, html,
                  flags=re.DOTALL)
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)


def fmt(n):
    return f"{int(round(n or 0)):,}"


def main():
    payload = fetch()
    if payload is None:
        return
    inject(payload)
    print(f"bags_on_offer.html updated — {payload['month']} (Kenya).")
    for key, p in payload["periods"].items():
        t = p["totals"]
        print(f"  [{p['label']}] {p['range']} · day {p['daysElapsed']}/{p['daysInPeriod']}")
        print(f"    On offer     : {fmt(t['on']['units'])} units · KES {fmt(t['on']['revenue'])}")
        print(f"    Not on offer : {fmt(t['off']['units'])} units · KES {fmt(t['off']['revenue'])}"
              + (f"  (Menu 4 panel: KES {fmt(payload['menu4NotOnOfferRevenue'])})" if key == "monthly" else ""))
        print(f"    Others       : {fmt(t['oth']['units'])} units · KES {fmt(t['oth']['revenue'])}  ("
              + ", ".join(f"{o['label']} KES {fmt(o['revenue'])}" for o in p["others"]) + ")")
        print(f"    Unclassified : KES {fmt(t['unc']['revenue'])} · {p['unclassifiedCount']} products"
              f" · red shops {sum(1 for x in p['shops'] if x['red'])}/{sum(1 for x in p['shops'] if x['target'])}")
    if not os.environ.get("DENRI_LAUNCHER"):
        webbrowser.open(pathlib.Path(HTML).as_uri())


if __name__ == "__main__":
    main()
