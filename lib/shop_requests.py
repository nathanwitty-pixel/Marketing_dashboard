"""lib/shop_requests.py — what each shop REQUESTED in the Odoo dispatch module against what it RECEIVED, how well
it requests (effectiveness %), and how the shops' requests fared in the weekly production approved list.
Spec: docs/shop-stock-levels.md ("Shop requests" and "Production — requests vs approved list"). User, 18 Oct 2026.

Source = the dispatch module (denri_dispatch_*), which every shop orders through:
  • A REQUEST = an original shop order (`denri_dispatch_order`, request_type 'shop', not a backorder, not cancelled)
    from a retail shop. What isn't sent at once moves to backorders (backorder_root_id = the request); a request's
    sent / received / still-pending are summed over the request and all its backorders, per product.
    Cancelled orders are left out: most are "Cancelled from pending queue adjustment" — the shop re-ordered and
    the new order carries the quantity again.
  • Stock BEFORE ordering = the order line's own snapshot when the shop ordered: stock on hand, incoming, the
    shop's Min / Max (dispatch stock policy) and Odoo's alert (stockout / below_min / healthy).
  • Offers at the order date: Power Deal · Deal of the Week · timed offers · running combos (Kenya —
    generators/product_performance.Offers, the same source as Product Performance).

Effectiveness % per shop (user's choice, 18 Oct 2026 — "blend of 3 checks"), units-weighted:
  1. Right bag   — the bag was out of stock or at / below Min when asked, or on an offer that day while the shop
                   held under half of Max (Power Deal runs all month, so an offer alone isn't a reason).
  2. Right qty   — asked vs Odoo's SUGGESTED quantity (Max − on hand − incoming): min(asked, suggested) ÷ suggested
                   (lines with no suggestion are left out). Odoo already blocks ordering above Max, so the real
                   miss is under-ordering — Sep 2026: 14,858 asked against 43,683 suggested.
  3. Sold through — of what arrived, the share sold at that shop within 14 days of the first receipt
                   (only lines received at least 14 days ago).
  Score = the average of the three. Dispatch FILL (sent ÷ asked, capped per line) is shown beside it — that is the
  warehouse's score, not the shop's.

Production: the weekly "Approved list" (`denri_production_plan`, KE-…, UG-…, TZ-…) is the final submission to
production. Per plan, the shops' requests placed since the country's previous list (up to the plan date) are set
against what was approved (qty_demand) and what the tailors were given (`denri_tailor_plan_line`).
"""
from __future__ import annotations

import collections
import datetime

from lib import db, runway_bags

SELL_DAYS = 14

REQUESTS_SQL = """
WITH roots AS (
  SELECT o.id, o.name, (o.order_date AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date AS d, o.state,
         s.name AS shop, s.pos_config_id AS cfg, s.denri_country AS cty
  FROM denri_dispatch_order o JOIN denri_dispatch_shop s ON s.id = o.shop_id
  WHERE NOT COALESCE(o.is_backorder, false) AND o.request_type = 'shop' AND o.state <> 'cancel'
    AND s.shop_type = 'retail'
    AND (o.order_date AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date BETWEEN :s AND :e
), chain AS (
  SELECT r.id AS root, o.id AS oid, o.state
  FROM roots r JOIN denri_dispatch_order o ON o.id = r.id OR o.backorder_root_id = r.id
), asked AS (
  SELECT l.order_id AS root, l.product_id, SUM(l.qty_ordered) AS req,
         MAX(l.stock_current_qty) AS cur, MAX(l.stock_incoming_qty) AS inc,
         MAX(l.stock_min_qty) AS mn, MAX(l.stock_max_qty) AS mx, MAX(l.stock_suggested_qty) AS sug,
         MAX(l.stock_alert_status) AS alert
  FROM denri_dispatch_order_line l WHERE l.order_id IN (SELECT id FROM roots)
  GROUP BY 1, 2
), moved AS (
  SELECT c.root, l.product_id, SUM(l.qty_fulfilled) AS sent, SUM(l.qty_received) AS rec,
         SUM(CASE WHEN c.state NOT IN ('done', 'cancel', 'received') THEN l.qty_remaining ELSE 0 END) AS pend
  FROM chain c JOIN denri_dispatch_order_line l ON l.order_id = c.oid
  GROUP BY 1, 2
), arrived AS (
  SELECT c.root, tl.product_id,
         MIN((t.receive_date AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date) AS first_rcv
  FROM chain c JOIN denri_dispatch_transit t ON t.order_id = c.oid
  JOIN denri_dispatch_transit_line tl ON tl.transit_id = t.id
  WHERE tl.qty_received > 0 AND t.receive_date IS NOT NULL
  GROUP BY 1, 2
)
SELECT r.id AS root, r.name AS ref, r.d, r.state, r.shop, r.cfg, r.cty, a.product_id, pt."name" AS product,
       a.req, a.cur, a.inc, a.mn, a.mx, a.sug, a.alert,
       COALESCE(m.sent, 0) AS sent, COALESCE(m.rec, 0) AS rec, COALESCE(m.pend, 0) AS pend, ar.first_rcv
FROM roots r JOIN asked a ON a.root = r.id
JOIN product_product pp ON pp.id = a.product_id JOIN product_template pt ON pt.id = pp.product_tmpl_id
LEFT JOIN moved m ON m.root = r.id AND m.product_id = a.product_id
LEFT JOIN arrived ar ON ar.root = r.id AND ar.product_id = a.product_id
WHERE pt."name" NOT LIKE '%+%'
"""

SALES_SQL = """
SELECT ps.config_id AS cfg, pl.product_id, (o.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date AS d,
       SUM(pl.qty) AS qty
FROM pos_order o JOIN pos_order_line pl ON pl.order_id = o.id
JOIN pos_session ps ON ps.id = o.session_id
WHERE (o.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date BETWEEN :s AND :e
  AND o.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0
GROUP BY 1, 2, 3
"""

PLANS_SQL = """
SELECT p.id, p.name, p.country, p.plan_date AS d, p.state
FROM denri_production_plan p
WHERE p.state <> 'cancel' AND COALESCE(p.plan_type, '') <> 'newshop' AND COALESCE(p.is_corporate, false) = false
  AND p.country IS NOT NULL
ORDER BY p.plan_date
"""

PLAN_LINES_SQL = """
SELECT l.plan_id, l.bag_product_id AS product_id, pt."name" AS product, SUM(l.qty_demand) AS approved,
       MAX(l.priority) AS priority
FROM denri_production_plan_line l
JOIN product_product pp ON pp.id = l.bag_product_id JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE l.plan_id IN ({ids})
GROUP BY 1, 2, 3
"""

TAILOR_SQL = """
SELECT t.plan_id, tl.bag_product_id AS product_id, SUM(tl.qty) AS qty
FROM denri_tailor_plan_line tl JOIN denri_tailor_plan t ON t.id = tl.tailor_plan_id
WHERE t.plan_id IN ({ids})
GROUP BY 1, 2
"""


def _f(v):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return 0.0
    return x if x == x else 0.0


def _d(v):
    if v is None or v != v:
        return None
    return v if isinstance(v, datetime.date) and not isinstance(v, datetime.datetime) else getattr(v, "date", lambda: v)()


def _pct(a, b):
    return round(a / b * 100) if b else None


def _offers():
    """Offers lookup (Kenya) — or None when the offer data can't be loaded."""
    try:
        from generators.product_performance import Offers
        return Offers(runway_bags.type_fn())
    except Exception as e:                                   # noqa: BLE001
        print(f"  Shop requests: offers unavailable ({e})")
        return None


def _offer_label(o):
    if not o:
        return ""
    bits = (["Power Deal"] if o["power"] else []) + (["Deal of the Week"] if o["dow"] else []) \
        + (["Timed offer"] if o["timed"] else []) + (["In a combo"] if o["combo"] else [])
    return " · ".join(bits)


def requests(start, end, today, shop_name, typ, offers=None):
    """Per shop: requests in [start, end] — totals, the three checks, effectiveness %, dispatch fill and the bags.
    shop_name(dispatch shop name) → the page's shop name."""
    df = db.run_query(REQUESTS_SQL, {"s": start.isoformat(), "e": end.isoformat()})
    if df is None:
        raise RuntimeError("Odoo unreachable (dispatch requests)")
    lines = []
    for r in df.itertuples():
        shop = shop_name(r.shop)
        bag = typ(str(r.product))
        if not shop or not bag:
            continue
        req = _f(r.req)
        if req <= 0:
            continue
        lines.append({"root": int(r.root), "ref": r.ref, "d": _d(r.d), "shop": shop, "cfg": int(_f(r.cfg)) or None,
                      "cty": r.cty, "pid": int(r.product_id), "product": str(r.product), "bag": bag, "req": req,
                      "cur": _f(r.cur), "inc": _f(r.inc), "mn": _f(r.mn), "mx": _f(r.mx), "sug": _f(r.sug), "alert": r.alert or "",
                      "sent": _f(r.sent), "rec": _f(r.rec), "pend": _f(r.pend), "rcv": _d(r.first_rcv)})
    if not lines:
        return {}

    # Sales per till × product × day from the first receipt on — for the 14-day sell-through.
    rcvs = [x["rcv"] for x in lines if x["rcv"]]
    sold = collections.defaultdict(float)
    if rcvs:
        sd = db.run_query(SALES_SQL, {"s": min(rcvs).isoformat(), "e": today.isoformat()})
        for r in (sd.itertuples() if sd is not None else []):
            sold[(int(_f(r.cfg)), int(r.product_id), _d(r.d))] += _f(r.qty)

    cache = {}

    def offer(bag, d):
        if offers is None or d is None:
            return ""
        k = (bag, d)
        if k not in cache:
            try:
                cache[k] = _offer_label(offers.week(bag, d, d))
            except Exception:                                # noqa: BLE001
                cache[k] = ""
        return cache[k]

    acc = collections.defaultdict(lambda: {"orders": set(), "req": 0.0, "sent": 0.0, "rec": 0.0, "pend": 0.0, "fill": 0.0,
                                           "need_ok": 0.0, "qty_ok": 0.0, "qty_base": 0.0, "st_sold": 0.0, "st_base": 0.0,
                                           "low": 0.0, "offer": 0.0, "cur": 0.0, "mx": 0.0, "bags": {}})
    for x in lines:
        a = acc[x["shop"]]
        a["orders"].add(x["root"])
        req, sent = x["req"], min(x["sent"], x["req"])
        a["req"] += req
        a["sent"] += x["sent"]
        a["rec"] += x["rec"]
        a["pend"] += x["pend"]
        a["fill"] += sent
        low = x["cur"] <= 0 or x["alert"] in ("stockout", "below_min") or (x["mn"] > 0 and x["cur"] <= x["mn"])
        off = offer(x["bag"], x["d"])
        if low:
            a["low"] += req
        if off:
            a["offer"] += req
        # check 1 — right bag: low when asked, or on an offer while under half of Max (offers run all month on most
        # bags, so an offer alone doesn't make a full shelf need more)
        right = low or (off and x["mx"] > 0 and x["cur"] + x["inc"] < x["mx"] / 2)
        if right:
            a["need_ok"] += req
        fit = None
        if x["sug"] > 0:                                              # check 2 — right qty (vs Odoo's suggestion)
            fit = min(req, x["sug"])
            a["qty_ok"] += fit
            a["qty_base"] += x["sug"]
        st = None
        if x["rcv"] and x["rec"] > 0 and (today - x["rcv"]).days >= SELL_DAYS and x["cfg"]:   # check 3 — sold through
            s14 = sum(sold.get((x["cfg"], x["pid"], x["rcv"] + datetime.timedelta(days=i)), 0.0) for i in range(SELL_DAYS))
            st = min(max(s14, 0), x["rec"])
            a["st_sold"] += st
            a["st_base"] += x["rec"]
        a["cur"] += x["cur"]
        a["mx"] += x["mx"]
        b = a["bags"].setdefault(x["bag"], {"bag": x["bag"], "req": 0.0, "sent": 0.0, "rec": 0.0, "pend": 0.0, "cur": 0.0,
                                            "mx": 0.0, "sug": 0.0, "low": 0.0, "fit": 0.0, "fitBase": 0.0, "st": 0.0, "stBase": 0.0,
                                            "orders": 0, "offer": "", "last": None, "lines": []})
        b["req"] += req
        b["sent"] += x["sent"]
        b["rec"] += x["rec"]
        b["pend"] += x["pend"]
        b["cur"] += x["cur"]
        b["mx"] += x["mx"]
        b["orders"] += 1
        if low:
            b["low"] += req
        if fit is not None:
            b["fit"] += fit
            b["fitBase"] += x["sug"]
            b["sug"] += x["sug"]
        if st is not None:
            b["st"] += st
            b["stBase"] += x["rec"]
        if off and not b["offer"]:
            b["offer"] = off
        b["last"] = max(b["last"] or x["d"], x["d"])
        if len(b["lines"]) < 12:
            b["lines"].append({"ref": x["ref"], "d": x["d"].isoformat(), "product": x["product"], "req": int(req),
                               "sent": int(x["sent"]), "rec": int(x["rec"]), "pend": int(x["pend"]), "cur": int(x["cur"]),
                               "inc": int(x["inc"]), "mn": int(x["mn"]), "mx": int(x["mx"]), "sug": int(x["sug"]), "alert": x["alert"],
                               "offer": off, "rcv": x["rcv"].isoformat() if x["rcv"] else None,
                               "sold14": None if st is None else int(st)})

    out = {}
    for shop, a in acc.items():
        checks = {"need": _pct(a["need_ok"], a["req"]), "qty": _pct(a["qty_ok"], a["qty_base"]),
                  "sell": _pct(a["st_sold"], a["st_base"])}
        vals = [v for v in checks.values() if v is not None]
        bags = sorted(a["bags"].values(), key=lambda b: -b["req"])
        out[shop] = {
            "orders": len(a["orders"]), "req": int(a["req"]), "sent": int(a["sent"]), "rec": int(a["rec"]),
            "pend": int(a["pend"]), "fill": _pct(a["fill"], a["req"]), "recPct": _pct(a["rec"], a["sent"]),
            "lowPct": _pct(a["low"], a["req"]), "offerPct": _pct(a["offer"], a["req"]),
            "checks": checks, "score": round(sum(vals) / len(vals)) if vals else None,
            "sellBase": int(a["st_base"]), "sug": int(a["qty_base"]),
            "bags": [{"bag": b["bag"], "orders": b["orders"], "req": int(b["req"]), "sent": int(b["sent"]),
                      "rec": int(b["rec"]), "pend": int(b["pend"]), "cur": round(b["cur"] / b["orders"], 1),
                      "mx": round(b["mx"] / b["orders"], 1), "sug": int(b["sug"]), "lowPct": _pct(b["low"], b["req"]),
                      "fitPct": _pct(b["fit"], b["fitBase"]), "sellPct": _pct(b["st"], b["stBase"]),
                      "offer": b["offer"], "last": b["last"].isoformat() if b["last"] else None,
                      "lines": b["lines"]} for b in bags],
        }
    return out


def production(shop_name, typ, today, keep=6):
    """The last `keep` approved lists per country: shops' requests since the previous list vs approved vs tailors."""
    pl = db.run_query(PLANS_SQL, {})
    if pl is None or not len(pl):
        return []
    plans = [{"id": int(r.id), "name": r.name, "cty": str(r.country).lower(), "d": _d(r.d), "state": r.state}
             for r in pl.itertuples()]
    prev = {}
    for p in plans:                                           # window = day after the country's previous list → plan date
        p["from"] = (prev[p["cty"]] + datetime.timedelta(days=1)) if p["cty"] in prev else p["d"] - datetime.timedelta(days=6)
        prev[p["cty"]] = p["d"]
    by_cty = collections.defaultdict(list)
    for p in plans:
        by_cty[p["cty"]].append(p)
    plans = [p for ps in by_cty.values() for p in ps[-keep:]]
    if not plans:
        return []
    ids = ", ".join(str(int(p["id"])) for p in plans)          # integers from Odoo — safe to inline
    lines = db.run_query(PLAN_LINES_SQL.format(ids=ids), {})
    tail = db.run_query(TAILOR_SQL.format(ids=ids), {})
    tq = collections.defaultdict(float)
    for r in (tail.itertuples() if tail is not None else []):
        tq[(int(r.plan_id), int(r.product_id))] += _f(r.qty)
    appr = collections.defaultdict(dict)
    for r in (lines.itertuples() if lines is not None else []):
        appr[int(r.plan_id)][int(r.product_id)] = {"product": str(r.product), "approved": _f(r.approved),
                                                   "priority": r.priority or ""}

    lo = min(p["from"] for p in plans)
    hi = max(p["d"] for p in plans)
    df = db.run_query(REQUESTS_SQL, {"s": lo.isoformat(), "e": hi.isoformat()})
    reqs = [] if df is None else [r for r in df.itertuples()]

    out = []
    for p in sorted(plans, key=lambda p: (p["d"], p["name"]), reverse=True):
        asked = collections.defaultdict(lambda: {"req": 0.0, "pend": 0.0, "shops": collections.Counter(), "product": ""})
        for r in reqs:
            d = _d(r.d)
            if str(r.cty).lower() != p["cty"] or not (p["from"] <= d <= p["d"]):
                continue
            x = asked[int(r.product_id)]
            x["req"] += _f(r.req)
            x["product"] = str(r.product)
            x["shops"][shop_name(r.shop) or str(r.shop).title()] += _f(r.req)
        rows = []
        for pid in set(asked) | set(appr.get(p["id"], {})):
            a, ap = asked.get(pid), appr.get(p["id"], {}).get(pid)
            req = a["req"] if a else 0.0
            ok = ap["approved"] if ap else 0.0
            name = (ap or {}).get("product") or (a or {}).get("product") or ""
            if not typ(name) and not req and not ok:
                continue
            status = ("added" if not req else "full" if ok >= req else "cut" if ok > 0 else "not")
            rows.append({"product": name, "bag": typ(name) or name.upper(), "req": int(req), "approved": int(ok),
                         "tailor": int(tq.get((p["id"], pid), 0)), "priority": (ap or {}).get("priority", ""),
                         "status": status,
                         "shops": {s: int(v) for s, v in (a["shops"].most_common() if a else []) if v}})
        rows.sort(key=lambda r: -(max(r["req"], r["approved"])))
        req_t = sum(r["req"] for r in rows)
        ok_t = sum(r["approved"] for r in rows)
        allowed = sum(min(r["req"], r["approved"]) for r in rows)
        out.append({"id": p["id"], "name": p["name"], "cty": p["cty"].upper(), "date": p["d"].isoformat(),
                    "from": p["from"].isoformat(), "state": p["state"], "req": req_t, "approved": ok_t,
                    "tailor": sum(r["tailor"] for r in rows), "allowed": allowed,
                    "allowedPct": _pct(allowed, req_t), "fromShopsPct": _pct(allowed, ok_t),
                    "counts": dict(collections.Counter(r["status"] for r in rows)), "rows": rows})
    return out
