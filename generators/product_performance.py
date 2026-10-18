"""product_performance.py — the Product Performance page: % share of the top-selling bags, categories and
colours, and the Bag of the Week (top seller + biggest mover) with why it moved — stock, offer or posting.
Spec: docs/product-performance.md.

    python product_performance.py        # DENRI_LAUNCHER=1 to skip the browser tab
"""
import collections
import datetime
import json
import math
import os
import re
import sys
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root → lib/
from lib import paths
from lib import marketing_posts
from lib import db, queries, colours, odoo_tabs, runway_bags, receipt_combos

HTML = paths.html("product_performance.html")
SHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"
POSTS_HISTORY = paths.data("bag_posts_history.json")
PRICES = paths.data("bag_original_prices.json")
TIMED = paths.data("timed_offers_config.json")

BULK_LINE_QTY = 10       # a POS line of 10+ units = corporate / bulk order (memory: bulk-orders-flag-lift)
MOVER_MIN = 10           # the biggest mover must have sold at least this many last week
TOP_N = 15               # bags listed before "Other bags"
FX = {"TZ": 25, "UG": 29}  # local currency per KES (sql/bags_sold_total.sql)
MARKETS = ("KE", "TZ", "UG")

# Every bag line on the tills (combo contents included; the '+' combo wrapper kept only to split its money).
LINES_SQL = """
SELECT pl.id, o.id AS receipt, o."name" AS ref,
       (o.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date AS d,
       lower(COALESCE(pc."name", '')) AS till, pt."name" AS product, pl.qty AS qty,
       pl.price_subtotal_incl AS amount,
       (COALESCE(pl.is_combo_line, false) OR pt."name" LIKE '%+%') AS wrapper,
       COALESCE(pl.sub_product_line, false) AS sub,
       COALESCE(pcat."name", '') AS categ
FROM pos_order o
JOIN pos_order_line pl ON pl.order_id = o.id
LEFT JOIN pos_session ps ON ps.id = o.session_id
LEFT JOIN pos_config pc ON pc.id = ps.config_id
JOIN product_product pp ON pp.id = pl.product_id
JOIN product_template pt ON pt.id = pp.product_tmpl_id
LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
WHERE (o.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date BETWEEN :s AND :e
  AND o.state IN ('done', 'invoiced', 'paid')
  AND pl.qty <> 0
  AND COALESCE(pl.is_program_reward, false) = false
  AND pt."name" NOT ILIKE '%delivery%'
  AND pt."name" NOT ILIKE '%customi%'
  AND pt."name" NOT ILIKE '%strap%'
  AND pt."name" NOT ILIKE '%discount%'      -- KES and % discount lines aren't bags
  AND pt."name" NOT ILIKE '%sample%'
  AND pt."name" NOT ILIKE 'gift bag%'
  AND COALESCE(pcat."name", '') NOT ILIKE '%Pos%'
  AND lower(pt."name") <> ALL(:excluded)
ORDER BY o.id, pl.id
"""

# Shop stock locations by top-level code — the lib/product_targets list (shops + Website, never warehouses).
SHOP_CODES = ("STAR", "MSA", "NAKS", "ELD", "KSM", "MERU", "THK", "HAZ", "KITE", "NAN", "KAK", "HTN", "KSI",
              "KTDA", "BUSIA", "RONG", "DAR", "UG", "WEB")
CODE_MKT = {c: ("TZ" if c == "DAR" else "UG" if c == "UG" else "KE") for c in SHOP_CODES}
_CODES = ", ".join("'%s'" % c for c in SHOP_CODES)

ONHAND_SQL = """
SELECT pt."name" AS product, split_part(l.complete_name, '/', 1) AS code, SUM(q.quantity) AS qty
FROM stock_quant q JOIN stock_location l ON l.id = q.location_id
JOIN product_product pp ON pp.id = q.product_id JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE l.usage = 'internal' AND split_part(l.complete_name, '/', 1) IN (""" + _CODES + """)
  AND pt."name" NOT LIKE '%+%'   -- combo products carry their own stock; their bags are counted on their own
GROUP BY 1, 2
"""

# Done moves touching a shop since :s — source / destination shop code (NULL = not a shop).
MOVES_SQL = """
SELECT pt."name" AS product, m.date::date AS d,
       CASE WHEN ls.usage = 'internal' AND split_part(ls.complete_name, '/', 1) IN (""" + _CODES + """)
            THEN split_part(ls.complete_name, '/', 1) END AS src,
       CASE WHEN ld.usage = 'internal' AND split_part(ld.complete_name, '/', 1) IN (""" + _CODES + """)
            THEN split_part(ld.complete_name, '/', 1) END AS dst,
       SUM(m.product_qty) AS qty
FROM stock_move m JOIN stock_location ls ON ls.id = m.location_id JOIN stock_location ld ON ld.id = m.location_dest_id
JOIN product_product pp ON pp.id = m.product_id JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE m.state = 'done' AND m.date::date >= :s AND pt."name" NOT LIKE '%+%'
  AND ((ls.usage = 'internal' AND split_part(ls.complete_name, '/', 1) IN (""" + _CODES + """))
    OR (ld.usage = 'internal' AND split_part(ld.complete_name, '/', 1) IN (""" + _CODES + """)))
GROUP BY 1, 2, 3, 4
"""


# ── small helpers ─────────────────────────────────────────────
def _d(v):
    return v if isinstance(v, datetime.date) else datetime.date.fromisoformat(str(v)[:10])


def _num(v):
    """float, with None / NaN as 0."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return 0.0
    return f if f == f else 0.0


def _sunday(d):
    return d - datetime.timedelta(days=(d.weekday() + 1) % 7)


def _month_start(d):
    return d.replace(day=1)


def _month_end(d):
    return (d.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)


def _market(till):
    t = str(till or "").lower()
    return "TZ" if t in ("sinza", "dar-es-alam") else "UG" if t == "uganda" else "KE"


def _fmt_d(d):
    return d.strftime("%d %b").lstrip("0")


def _load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def periods(today):
    """{period: (cur start, cur end, prev start, prev end, label)} — each compared with the period before it."""
    ws = _sunday(today)
    m1 = _month_start(today)
    pm1 = _month_start(m1 - datetime.timedelta(days=1))
    ppm1 = _month_start(pm1 - datetime.timedelta(days=1))
    same = min(pm1 + (today - m1), _month_end(pm1))
    return {
        "lastweek":  (ws - datetime.timedelta(days=7), ws - datetime.timedelta(days=1),
                      ws - datetime.timedelta(days=14), ws - datetime.timedelta(days=8), "Last week"),
        "weekly":    (ws, today, ws - datetime.timedelta(days=7), today - datetime.timedelta(days=7), "This week"),
        "monthly":   (m1, today, pm1, same, "This month"),
        "lastmonth": (pm1, _month_end(pm1), ppm1, _month_end(ppm1), "Last month"),
    }


# ── sales lines → bag records (combo money split across its bags) ──
def load_lines(start, end, typ):
    df = db.run_query(LINES_SQL, {"s": start.isoformat(), "e": end.isoformat(),
                                  "excluded": queries.excluded_products()})
    if df is None:
        raise RuntimeError("Odoo unreachable")
    prices = {k.upper(): v for k, v in _load_json(PRICES, {}).items() if isinstance(v, (int, float))}
    out = []
    pending = []   # [(rec, weight)] of the bag lines under the current combo wrapper
    wrap = {"amount": 0.0, "receipt": None}

    def flush():
        if pending:
            tot = sum(w for _, w in pending) or len(pending)
            for rec, w in pending:
                rec["rev"] += wrap["amount"] * ((w or 1) / tot if tot else 1 / len(pending))
        pending.clear()
        wrap["amount"] = 0.0

    for r in df.itertuples():
        if r.receipt != wrap["receipt"]:
            flush()
            wrap["receipt"] = r.receipt
        mkt = _market(r.till)
        amt = _num(r.amount) / FX.get(mkt, 1)
        if r.wrapper:
            flush()
            wrap["amount"] = amt
            continue
        bag = typ(r.product)
        if not bag:
            continue
        rec = {"d": _d(r.d), "mkt": mkt, "bag": bag, "product": str(r.product),
               "colour": colours.family(str(r.product), "") or "No colour",
               "categ": re.sub(r"^.*/\s*", "", str(r.categ or "")), "units": _num(r.qty),
               "rev": 0.0 if r.sub else amt, "sub": bool(r.sub), "ref": str(r.ref), "till": str(r.till)}
        out.append(rec)
        if r.sub:
            pending.append((rec, prices.get(bag, 0) * (1 if rec["units"] >= 0 else -1)))
        else:
            flush()
    flush()
    return out


# Shade = the product name after its bag type ("Mini Umbra Cracked" → Cracked), for the Colours list's
# expandable shades. Edition / material words (counted as the base colour) and [REJECT] are dropped.
_EDITION = {"WOOVEN", "WOVEN", "HB", "CN", "TT", "018", "ANKARA", "CUSTOM", "CROC"}
_SHADE_ALIAS = {"CHOCO": "CHOCOLATE", "CHOCOLATE BROWN": "CHOCOLATE", "D.BROWN": "DARK BROWN", "D BROWN": "DARK BROWN",
                "GRAY": "GREY", "CREAME": "CREAM"}


def shade(product, bag, family):
    n = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", " ", str(product).upper())).strip()
    b = str(bag).upper()
    i = n.find(b + " ") if b else -1
    s = n[i + len(b) + 1:] if i >= 0 else n
    s = " ".join(w for w in s.split() if w.strip("()") not in _EDITION and not w.isdigit())
    s = _SHADE_ALIAS.get(s, s)
    return s.title() if s else family


def categories(lines):
    """{BAG: category} — the bag type's usual catalogue category, else its Odoo category."""
    votes = collections.defaultdict(collections.Counter)
    for c in odoo_tabs.load_catalog():
        if c["bag"] and c["category"]:
            votes[c["bag"].strip().upper()][c["category"].strip().upper()] += 1
    odoo = collections.defaultdict(collections.Counter)
    for x in lines:
        if x["categ"]:
            odoo[x["bag"]][x["categ"].upper()] += 1
    known = {c for v in votes.values() for c in v}

    def norm(c):
        """Odoo's plural category names → the catalogue's (Handbags → HANDBAG, Briefcase Bags → BRIEFCASE)."""
        c = c.upper().strip()
        if c in known or not c:
            return c or "OTHER"
        if c in ("ALL", "SALEABLE", "BAGS"):
            return "OTHER"
        for cand in (re.sub(r"S$", "", c), re.sub(r"\s+BAGS?$", "", c), re.sub(r"S\b", "", c)):
            if cand in known:
                return cand
        return re.sub(r"S$", "", c)
    out = {}
    for b in {x["bag"] for x in lines}:
        v = votes.get(b) or odoo.get(b)
        out[b] = norm(v.most_common(1)[0][0]) if v else "OTHER"
    return out


# ── stock: daily shop on-hand per market, rebuilt from today's on-hand and the moves ──
def stock_facts(typ, since, today):
    """({mkt: {BAG: now}}, {mkt: {BAG: {date: end-of-day level}}}, {mkt: {BAG: {date: units dispatched in}}})
    for mkt in ALL / KE / TZ / UG."""
    mk = ("ALL",) + MARKETS
    onhand = {m: collections.Counter() for m in mk}
    q = db.run_query(ONHAND_SQL, {})
    for r in (q.itertuples() if q is not None else []):
        b, qty = typ(r.product), _num(r.qty)
        if b and qty:
            onhand["ALL"][b] += qty
            onhand[CODE_MKT.get(r.code, "KE")][b] += qty
    net = {m: collections.defaultdict(collections.Counter) for m in mk}
    disp = {m: collections.defaultdict(collections.Counter) for m in mk}
    q = db.run_query(MOVES_SQL, {"s": since.isoformat()})
    for r in (q.itertuples() if q is not None else []):
        b, qty = typ(r.product), _num(r.qty)
        if not b or not qty:
            continue
        d = _d(r.d)
        sm = CODE_MKT.get(r.src) if r.src else None
        dm = CODE_MKT.get(r.dst) if r.dst else None
        for m in mk:
            in_s = sm is not None and (m == "ALL" or sm == m)
            in_d = dm is not None and (m == "ALL" or dm == m)
            if in_d and not in_s:
                net[m][b][d] += qty
                if sm is None:                     # from a warehouse (not another shop) = a dispatch
                    disp[m][b][d] += qty
            elif in_s and not in_d:
                net[m][b][d] -= qty
    levels = {m: {} for m in mk}
    for m in mk:
        for b in set(onhand[m]) | set(net[m]):
            lv, d, series = onhand[m].get(b, 0), today, {}
            while d >= since - datetime.timedelta(days=1):
                series[d] = lv
                lv -= net[m][b].get(d, 0)
                d -= datetime.timedelta(days=1)
            levels[m][b] = series
    return ({m: {b: int(round(v)) for b, v in onhand[m].items()} for m in mk}, levels, disp)


def week_stock(levels, disp, sold_days, b, s, e):
    """Start-of-week stock, units dispatched in, biggest delivery, days in stock for one bag/market/week."""
    lv = levels.get(b, {})
    start = lv.get(s - datetime.timedelta(days=1), 0)
    days = 0
    d = s
    while d <= e:
        if lv.get(d - datetime.timedelta(days=1), 0) > 0 or lv.get(d, 0) > 0 or d in sold_days:
            days += 1
        d += datetime.timedelta(days=1)
    dd = {d: q for d, q in disp.get(b, {}).items() if s <= d <= e and q > 0}
    big = max(dd.items(), key=lambda kv: kv[1]) if dd else None
    return {"start": int(round(start)), "disp": int(round(sum(dd.values()))), "days": days,
            "big": [int(round(big[1])), _fmt_d(big[0])] if big else None}


# ── offers ────────────────────────────────────────────────────
class Offers:
    """Kenya offers per day (each day reads its own month's bags_offer_source file) + timed offers;
    Sinza / Uganda listings from offers_monthly.csv."""

    def __init__(self, typ):
        self.typ = typ
        self.src = {}
        self.timed = []
        for o in (_load_json(TIMED, {}) or {}).get("offers", []):
            if str(o.get("market", "Kenya")).lower() != "kenya":
                continue
            try:
                s, e = _d(o["startDate"]), _d(o["endDate"])
            except (KeyError, ValueError):
                continue
            prices = {self.typ(k) or k.upper(): v for k, v in (o.get("prices") or {}).items()}
            self.timed.append({"name": o.get("name", "Timed offer"), "s": s, "e": e,
                               "bags": {self.typ(b) or str(b).upper() for b in o.get("bags", [])}, "prices": prices})

    def month(self, d):
        key = d.strftime("%Y-%m")
        if key not in self.src:
            data = _load_json(paths.data(f"bags_offer_source_{key}.json"), None)
            if data is None:
                cur = _load_json(paths.data("bags_offer_source.json"), {})
                try:
                    data = cur if datetime.datetime.strptime(cur.get("month", ""), "%B %Y").strftime("%Y-%m") == key else {}
                except ValueError:
                    data = {}
            tags = collections.defaultdict(set)
            for name, ts in (data.get("onOffer") or {}).items():
                tags[self.typ(name) or name.upper()] |= set(ts)
            runs = collections.defaultdict(list)
            for r in data.get("dowRuns") or []:
                runs[self.typ(r.get("product", "")) or str(r.get("product", "")).upper()].append(r)
            combos = collections.defaultdict(list)
            for c in data.get("combos") or []:
                for b in c.get("bags", []):
                    combos[self.typ(b) or b].append(c.get("label", ""))
            self.src[key] = {"tags": tags, "runs": runs, "combos": combos}
        return self.src[key]

    def week(self, b, s, e):
        """{power, combo:[labels], dow:[{tier, shops}], timed:[{name, s, e, was, now}]} for bag b over [s, e]."""
        out = {"power": False, "combo": [], "dow": [], "timed": []}
        d = s
        while d <= e:
            m = self.month(d)
            t = m["tags"].get(b, set())
            out["power"] |= "Power Deal" in t
            for lbl in m["combos"].get(b, []):
                if lbl not in out["combo"]:
                    out["combo"].append(lbl)
            wn = 1 + (d - _sunday(_month_start(d))).days // 7
            for r in m["runs"].get(b, []):
                if wn in (r.get("weeks") or []):
                    k = {"tier": r.get("tier", ""), "shops": len(r.get("locations") or [])}
                    if k not in out["dow"]:
                        out["dow"].append(k)
            d += datetime.timedelta(days=1)
        for o in self.timed:
            if b in o["bags"] and o["s"] <= e and o["e"] >= s:
                p = o["prices"].get(b) or {}
                out["timed"].append({"name": o["name"], "s": _fmt_d(o["s"]), "e": _fmt_d(o["e"]),
                                     "was": p.get("was"), "now": p.get("now")})
        return out

    def tags_now(self, b, today):
        m = self.month(today)
        t = sorted(m["tags"].get(b, set()))
        return t

    @staticmethod
    def listings(month_name, typ):
        """{mkt: {BAG: [text]}} for Sinza / Uganda from offers_monthly.csv."""
        out = {}
        for mkt, key, cur in (("TZ", "sinza", "TSh"), ("UG", "uganda", "USh")):
            o = receipt_combos.load_offers(month_name, key) or {}
            per = collections.defaultdict(list)
            for c in o.get("combos", []):
                for slot in c["slots"]:
                    for b in slot:
                        per[typ(b) or b].append(f"In the {c['name']} combo" + (f" ({cur} {c['now']:,})" if c.get("now") else ""))
            for c in o.get("singles", []):
                for slot in c["slots"]:
                    for b in slot:
                        per[typ(b) or b].append(f"Listed single offer {cur} {c['now']:,}" if c.get("now") else "Listed single offer")
            out[mkt] = per
        return out


# ── posts ─────────────────────────────────────────────────────
def load_posts(typ):
    """({BAG: [kenya, outside]} last week, {BAG: [kenya, outside]} this month) from the two MARKETING_POST tabs."""
    try:
        from lib.google_auth import get_gspread_client
        sh = get_gspread_client().open_by_key(SHEET_ID)
        rows_m = marketing_posts.read(sh, "MONTHLY_MARKETING_POST")
        rows_w = marketing_posts.read(sh, "WEEKLY_MARKETING_POST")
    except Exception as e:                                   # noqa: BLE001
        print(f"  Posts unavailable ({e}) — marketing reasons left out.")
        return None, None

    def num(v):
        try:
            return float(str(v).replace(",", "") or 0)
        except ValueError:
            return 0.0

    def tally(rows):
        out = collections.defaultdict(lambda: [0, 0])
        for r in (rows or [])[1:]:
            if len(r) < 5:
                continue
            name, bag_type = str(r[2]).strip(), str(r[3]).strip()
            if not name or not bag_type or bag_type.upper() in ("SUM TOTAL", "TOTAL", "GRAND TOTAL"):
                continue
            b = typ(name) or typ(bag_type)
            if b:
                out[b][0] += num(r[4])
                out[b][1] += num(r[7]) if len(r) > 7 else 0
        return {b: [int(v[0]), int(v[1])] for b, v in out.items()}
    return tally(rows_w), tally(rows_m)


def posts_between(typ):
    """fn(start, end) → {BAG: {"KE", "TZ", "UG": posts}} from marketing's daily posting sheets, so any past
    window (last month, the month before) can be counted; None when the sheets can't be read."""
    try:
        marketing_posts.daily()
    except Exception as e:                                   # noqa: BLE001
        print(f"  Daily posting sheets unavailable ({e}) — past-period posting comparisons left out.")
        return None
    cache = {}

    def fn(s, e):
        if (s, e) not in cache:
            out = collections.defaultdict(lambda: {"KE": 0, "TZ": 0, "UG": 0})
            for (bt, col), by in marketing_posts.posts(s, e).items():
                b = typ(f"{bt} {col}".strip()) or typ(bt)
                if b:
                    for m, k in (("KENYA", "KE"), ("SINZA", "TZ"), ("UGANDA", "UG")):
                        out[b][k] += int(by.get(m, 0))
            cache[(s, e)] = dict(out)
        return cache[(s, e)]
    return fn


# ── why it moved ──────────────────────────────────────────────
def explain(b, mkt, w, ctx):
    """{lw, pw, lwNb, pwNb, head, lines:[[group, dir, text]]} for bag b in market mkt — the period w["cur"]
    vs the period before it w["prev"] (w: s1, e1, s0, e0, cur, prev, key; ctx["by_bag"] holds both windows)."""
    s1, e1, s0, e0 = w["s1"], w["e1"], w["s0"], w["e0"]
    C, P = w["cur"], w["prev"]
    n1, n0 = (e1 - s1).days + 1, (e0 - s0).days + 1
    rows = [x for x in ctx["by_bag"].get(b, ()) if mkt == "ALL" or x["mkt"] == mkt]
    lw = sum(x["units"] for x in rows if s1 <= x["d"] <= e1)
    pw = sum(x["units"] for x in rows if s0 <= x["d"] <= e0)
    bulk = [x for x in rows if not x["sub"] and (x["units"] >= BULK_LINE_QTY or x.get("corp"))]
    lw_nb = lw - sum(x["units"] for x in bulk if s1 <= x["d"] <= e1)
    pw_nb = pw - sum(x["units"] for x in bulk if s0 <= x["d"] <= e0)
    lines = []

    # Stock
    sold_days = {x["d"] for x in rows if x["units"] > 0}
    lv, dp = ctx["levels"].get(mkt, {}), ctx["disp"].get(mkt, {})
    st1, st0 = week_stock(lv, dp, sold_days, b, s1, e1), week_stock(lv, dp, sold_days, b, s0, e0)
    r1, r0 = st1["days"] / n1, st0["days"] / n0
    if r1 > r0 + 0.01:
        lines.append(["Stock", "up", f"Back in stock — in stock {st1['days']}/{n1} days {C} vs {st0['days']}/{n0} {P}"])
    elif r1 < r0 - 0.01:
        lines.append(["Stock", "down", f"Ran short — in stock only {st1['days']}/{n1} days {C} (vs {st0['days']}/{n0} {P})"])
    if st1["disp"] >= 10 and st1["disp"] >= 0.3 * max(lw, 1):
        big = f" — biggest delivery {st1['big'][0]:,} on {st1['big'][1]}" if st1["big"] else ""
        if st1["start"] < lw_nb:   # the shops couldn't have covered the period (bulk orders aside) from what they started with
            lines.append(["Stock", "up", f"Restocked — {st1['disp']:,} dispatched into the shops {C}{big}; "
                                         f"they started with {st1['start']:,} against {int(lw_nb):,} sold"
                                         + (" (bulk orders aside)" if lw_nb != lw else "")])
        else:
            lines.append(["Stock", "info", f"{st1['disp']:,} dispatched into the shops {C}{big} — "
                                           f"stock was already enough ({st1['start']:,} at the start)"])
    now = ctx["stock_now"].get(mkt, {}).get(b, 0)
    lines.append(["Stock", "info", f"Shop stock {st0['start']:,} at the start of {P} → {st1['start']:,} at the start of {C} → {now:,} now"])

    # Offer
    if mkt in ("ALL", "KE"):
        o1, o0 = ctx["offers"].week(b, s1, e1), ctx["offers"].week(b, s0, e0)
        any_offer = False
        if o1["power"] or o0["power"]:
            any_offer = True
            d = "info" if (o1["power"] and o0["power"]) else ("up" if o1["power"] else "down")
            lines.append(["Offer", d, {"info": "On Power Deal in both (runs all month at every shop)",
                                       "up": f"Power Deal started — on it {C}, not {P}",
                                       "down": f"Power Deal ended — on it {P}, not {C}"}[d]])
        if o1["dow"] or o0["dow"]:
            any_offer = True
            dsc = lambda ds: ", ".join(f"{x['tier']} at {x['shops']} shop{'s' if x['shops'] != 1 else ''}" for x in ds)
            if o1["dow"] and not o0["dow"]:
                lines.append(["Offer", "up", f"Deal of the Week started {C} ({dsc(o1['dow'])})"])
            elif o0["dow"] and not o1["dow"]:
                lines.append(["Offer", "down", f"Deal of the Week ended — ran {P} ({dsc(o0['dow'])}), not {C}"])
            else:
                lines.append(["Offer", "info", f"Deal of the Week in both ({dsc(o1['dow'])})"])
        t1 = {t["name"] for t in o1["timed"]}
        t0 = {t["name"] for t in o0["timed"]}
        for t in o1["timed"]:
            any_offer = True
            price = f", KES {t['was']:,} → {t['now']:,}" if t.get("was") and t.get("now") else ""
            lines.append(["Offer", "info" if t["name"] in t0 else "up", f"Timed offer {t['s']}–{t['e']}{price}"])
        for t in o0["timed"]:
            if t["name"] not in t1:
                any_offer = True
                lines.append(["Offer", "down", f"Timed offer {t['s']}–{t['e']} ended — ran {P} only"])
        c1 = sum(x["units"] for x in rows if x["sub"] and s1 <= x["d"] <= e1 and x["mkt"] == "KE")
        c0 = sum(x["units"] for x in rows if x["sub"] and s0 <= x["d"] <= e0 and x["mkt"] == "KE")
        if o1["combo"] or c1 or c0:
            any_offer = True
            names = f" ({', '.join(o1['combo'][:3])})" if o1["combo"] else ""
            diff, gate = c1 - c0, max(5, 0.2 * max(abs(lw - pw), 1))
            d = "up" if diff >= gate else "down" if -diff >= gate else "info"
            lines.append(["Offer", d, f"{int(c1):,} sold inside running combos {C} vs {int(c0):,} {P}{names}"])
        if not any_offer:
            lines.append(["Offer", "info", "Not on any Kenya offer in either — full-price sales"])
    if mkt in ("ALL", "TZ", "UG"):
        for m in ("TZ", "UG") if mkt == "ALL" else (mkt,):
            for t in ctx["listings"].get(m, {}).get(b, [])[:2]:
                lines.append(["Offer", "info", f"{'Sinza' if m == 'TZ' else 'Uganda'}: {t}"])

    # Marketing — posts are counted a week in arrears. Last week / last month: compared with the period before
    # from marketing's daily posting sheets; the saved weekly history is only the fallback.
    pm = ctx["posts_m"].get(b, [0, 0])
    pb = ctx.get("posts_between")
    if pb is not None and w["key"] in ("lastweek", "lastmonth"):
        def cnt(s, e):
            v = pb(s, e).get(b, {})
            return sum(v.values()) if mkt == "ALL" else v.get(mkt, 0)
        p1v, p0v = cnt(w["s1"], w["e1"]), cnt(w["s0"], w["e0"])
        where = "" if mkt in ("ALL", "KE") else " (outside Kenya)"
        if p1v > p0v:
            lines.append(["Marketing", "up", f"Posted more{where} — {p1v} posts {C} vs {p0v} {P}"])
        elif p1v < p0v:
            lines.append(["Marketing", "down", f"Posted less{where} — {p1v} posts {C} vs {p0v} {P}"])
        else:
            lines.append(["Marketing", "info", f"Same posting in both ({p1v} posts)" if p1v else f"Not posted{where} in either"])
    elif ctx["posts_w"] is not None and w["key"] == "lastweek":
        col = 1 if mkt in ("TZ", "UG") else 0
        p1 = ctx["posts_w"].get(b, [0, 0])
        p1v = p1[0] + p1[1] if mkt == "ALL" else p1[col]
        pw_hist = ctx["posts_prev"]
        p0v = pw_hist.get(b) if (pw_hist is not None and mkt in ("ALL", "KE")) else None
        if mkt == "ALL" and p0v is not None:
            p1v = p1[0]                                      # history is Kenya posts only — compare like with like
        where = "" if mkt in ("ALL", "KE") else " (outside Kenya)"
        if p0v is None:
            lines.append(["Marketing", "info", f"Posted {p1v} time{'s' if p1v != 1 else ''}{where} {C} ({P} isn't recorded)"
                          if p1v else f"Not posted{where} {C}"])
        elif p1v > p0v:
            lines.append(["Marketing", "up", f"Posted more — {p1v} posts {C} vs {p0v} {P}"])
        elif p1v < p0v:
            lines.append(["Marketing", "down", f"Posted less — {p1v} posts {C} vs {p0v} {P}"])
        else:
            lines.append(["Marketing", "info", f"Same posting in both ({p1v} posts)" if p1v else "Not posted in either"])
    elif ctx["posts_w"] is not None and w["key"] == "weekly":
        p1 = ctx["posts_w"].get(b, [0, 0])
        lines.append(["Marketing", "info", f"This week's posts are counted next week — last week: {p1[0] + p1[1]} posts"])
    if ctx["posts_w"] is not None and w["key"] != "lastmonth":
        lines.append(["Marketing", "info", f"{pm[0] + pm[1]} posts this month ({pm[0]} Kenya · {pm[1]} outside)"])
    elif w["key"] == "lastmonth" and pb is None:
        lines.append(["Marketing", "info", "Posting sheets couldn't be read — no posting comparison"])

    # Bulk
    for x in sorted(bulk, key=lambda x: -x["units"]):
        if s1 <= x["d"] <= e1 or s0 <= x["d"] <= e0:
            lines.append(["Bulk", "warn", f"{int(x['units']):,} × {x['product']} — {x['ref']}, {x['till'].title()}, {_fmt_d(x['d'])}"
                          + (f" ({C})" if s1 <= x["d"] <= e1 else f" ({P})")
                          + (f" — Corporate lead ({x['corp']}), credited to {x['till'].title()}" if x.get("corp") else "")])

    delta = lw_nb - pw_nb
    want = "up" if delta > 0 else "down" if delta < 0 else None
    head = None
    if bulk and abs(delta) < 0.5 * abs(lw - pw):          # the bulk order, not demand, made the change
        big = max(bulk, key=lambda x: x["units"])
        head = (f"Bulk order — {int(big['units']):,} × {big['product']} ({big['ref']}); without bulk orders "
                f"sales were {int(lw_nb):,} vs {int(pw_nb):,} {P}")
        want = None
    if want:
        for g in ("Stock", "Offer", "Marketing"):
            hit = next((l for l in lines if l[0] == g and l[1] == want), None)
            if hit:
                head = hit[2]
                break
    return {"lw": int(lw), "pw": int(pw), "lwNb": int(lw_nb), "pwNb": int(pw_nb), "bulk": bool(bulk),
            "head": head or ("No single driver — steady demand" if delta >= 0 else "No single driver found — demand eased"),
            "lines": lines}


# ── build ─────────────────────────────────────────────────────
def build(today=None):
    today = today or datetime.date.today()
    P = periods(today)
    start = min(p[2] for p in P.values())
    typ = runway_bags.type_fn()
    lines = load_lines(start, today, typ)
    try:                                                  # Corporate-lead till orders — noted on the bulk-order flag
        from lib import shop_corporate
        corp_team = shop_corporate.corporate_team_receipts(start, today)
    except Exception as e:                                # noqa: BLE001
        print(f"  Corporate-team till orders: skipped ({e})")
        corp_team = {}
    for x in lines:
        if x["ref"] in corp_team:
            x["corp"] = corp_team[x["ref"]]["client"]
    cats = categories(lines)

    out_periods = {}
    for key, (s1, e1, s0, e0, label) in P.items():
        agg = collections.defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
        for x in lines:
            cur, prev = s1 <= x["d"] <= e1, s0 <= x["d"] <= e0
            if cur or prev:
                a = agg[(x["bag"], x["colour"], x["mkt"], shade(x["product"], x["bag"], x["colour"]))]
                i = 0 if cur else 2
                a[i] += x["units"]
                a[i + 1] += x["rev"]
        rows = [[b, c, m, round(v[0]), round(v[1]), round(v[2]), round(v[3]), s] for (b, c, m, s), v in agg.items()
                if any(round(z) for z in v)]
        out_periods[key] = {"label": label, "cur": [s1.isoformat(), e1.isoformat()], "prev": [s0.isoformat(), e0.isoformat()],
                            "curLabel": f"{_fmt_d(s1)} – {_fmt_d(e1)}", "prevLabel": f"{_fmt_d(s0)} – {_fmt_d(e0)}", "rows": rows}

    s1, e1, s0, e0, _ = P["lastweek"]
    stock_now, levels, disp = stock_facts(typ, start, today)
    posts_w, posts_m = load_posts(typ)
    hist = _load_json(POSTS_HISTORY, [])
    prev_wk = next((h for h in hist if h.get("week") == s0.isoformat()), None)
    posts_prev = {b: int(v.get("posts", 0)) for b, v in prev_wk["bags"].items()} if prev_wk else None
    offers = Offers(typ)
    base_ctx = {"levels": levels, "disp": disp, "stock_now": stock_now, "offers": offers,
                "posts_w": posts_w, "posts_m": posts_m or {}, "posts_prev": posts_prev,
                "posts_between": posts_between(typ),
                "listings": Offers.listings(today.strftime("%B"), typ)}
    words = {"lastweek": ("last week", "the week before"),
             "weekly": ("this week", "the same days last week"),
             "monthly": ("this month", "the same days last month"),
             "lastmonth": ("last month", "the month before")}

    # Bag of the period (top seller + biggest mover) and why it moved — for every period and market.
    why, botw = {}, {}
    for per, (p1, q1, p0, q0, _lbl) in P.items():
        w = {"key": per, "s1": p1, "e1": q1, "s0": p0, "e0": q0, "cur": words[per][0], "prev": words[per][1]}
        by_bag = collections.defaultdict(list)
        for x in lines:
            if (p1 <= x["d"] <= q1) or (p0 <= x["d"] <= q0):
                by_bag[x["bag"]].append(x)
        ctx = dict(base_ctx, by_bag=by_bag)
        mover_min = math.ceil(MOVER_MIN * ((q1 - p1).days + 1) / 7)
        why[per], botw[per] = {}, {}
        for mkt in ("ALL",) + MARKETS:
            u1, r1 = collections.Counter(), collections.Counter()
            for x in lines:
                if (mkt == "ALL" or x["mkt"] == mkt) and p1 <= x["d"] <= q1:
                    u1[x["bag"]] += x["units"]
                    r1[x["bag"]] += x["rev"]
            if not u1:
                continue
            pick = {b for b, _ in u1.most_common(TOP_N + 5)} | {b for b, _ in r1.most_common(TOP_N + 5)}
            top = u1.most_common(1)[0][0]
            pick.add(top)
            cands = [b for b, v in u1.items() if v >= mover_min]
            expl = {b: explain(b, mkt, w, ctx) for b in pick | set(cands)}
            mover = max(cands, key=lambda b: (expl[b]["lwNb"] - expl[b]["pwNb"], u1[b]), default=None)
            if mover is not None and expl[mover]["lwNb"] - expl[mover]["pwNb"] <= 0:
                mover = None
            keep = pick | ({mover} if mover else set())
            why[per][mkt] = {b: expl[b] for b in keep}
            botw[per][mkt] = {"top": top, "mover": mover, "total": int(sum(u1.values())), "rev": int(sum(r1.values())),
                              "moverMin": mover_min, "cur": words[per][0], "prev": words[per][1]}

    bags = {x["bag"] for x in lines}
    info = {}
    for b in bags:
        pw_, pm_ = (posts_w or {}).get(b, [0, 0]), (posts_m or {}).get(b, [0, 0])
        info[b] = {"cat": cats.get(b, "OTHER"), "stock": [stock_now[m].get(b, 0) for m in MARKETS],
                   "tags": offers.tags_now(b, today), "postsW": pw_, "postsM": pm_}

    return {"generated": datetime.datetime.now().strftime("%d %b %Y %H:%M"), "topN": TOP_N,
            "bulkQty": BULK_LINE_QTY, "moverMin": MOVER_MIN,
            "week": {"cur": f"{_fmt_d(s1)} – {_fmt_d(e1)}", "prev": f"{_fmt_d(s0)} – {_fmt_d(e0)}"},
            "periods": out_periods, "botw": botw, "why": why, "info": info}


def inject(payload):
    with open(HTML, encoding="utf-8") as f:
        html = f.read()
    block = ("<!-- PP_DATA_START -->\n<script>\nconst PP = "
             + json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
             + ";\n</script>\n<!-- PP_DATA_END -->")
    html = re.sub(r"<!-- PP_DATA_START -->.*?<!-- PP_DATA_END -->", lambda _m: block, html, flags=re.S)
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    p = build()
    b = p["botw"].get("lastweek", {}).get("ALL", {})
    print(f"  Product Performance: last week {p['week']['cur']} — {b.get('total', 0):,} bags; "
          f"top seller {b.get('top')}, biggest mover {b.get('mover')}")
    for k, v in p["periods"].items():
        print(f"    {v['label']:<11} {v['curLabel']:>15} vs {v['prevLabel']:<15} {len(v['rows'])} rows")
    inject(p)
    if os.environ.get("DENRI_LAUNCHER") != "1":
        webbrowser.open("file://" + HTML)
