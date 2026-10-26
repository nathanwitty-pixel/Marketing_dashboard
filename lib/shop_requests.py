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
  2. Right qty   — asked vs Odoo's SUGGESTED quantity (Max − on hand − incoming), once per shop × product: all the
                   period's asks vs the largest suggestion at any of its requests, min(asked, suggested) ÷ suggested
                   (products with no suggestion are left out). Odoo already blocks ordering above Max, so the real
                   miss is under-ordering — Sep 2026: 13,467 asked against 20,716 suggested (once per product).
  3. Sold through — of what arrived, the share sold at that shop within 14 days of the first receipt
                   (only lines received at least 14 days ago).
  Score = the average of the three. Dispatch FILL (sent ÷ asked, capped per line) is shown beside it — that is the
  warehouse's score, not the shop's.
  GOT WHAT IT ASKED % covers both directions: matched (min(asked, sent) per line) ÷ (matched + ASKED, NOT GOT
  (asked − sent − still pending) + SENT WITHOUT A REQUEST). Not part of effectiveness either.

Production: the weekly "Approved list" (`denri_production_plan`, KE-…, UG-…, TZ-…) is the final submission to
production. Per plan, the shops' requests placed since the country's previous list (up to the plan date) are set
against what was approved (qty_demand) and what the tailors were given (`denri_tailor_plan_line`).
"""
from __future__ import annotations

import collections
import datetime
import math

from lib import db, runway_bags

SELL_DAYS = 14

REQUESTS_SQL = """
WITH roots AS MATERIALIZED (
  SELECT o.id, o.name, (o.order_date AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date AS d, o.state,
         s.name AS shop, s.pos_config_id AS cfg, s.denri_country AS cty
  FROM denri_dispatch_order o JOIN denri_dispatch_shop s ON s.id = o.shop_id
  WHERE NOT COALESCE(o.is_backorder, false) AND o.request_type = 'shop' AND o.state <> 'cancel'
    AND s.shop_type = 'retail'
    AND (o.order_date AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date BETWEEN :s AND :e
), chain AS MATERIALIZED (
  SELECT r.id AS root, r.id AS oid, r.state FROM roots r
  UNION ALL
  SELECT o.backorder_root_id, o.id, o.state FROM denri_dispatch_order o
  WHERE o.backorder_root_id IN (SELECT id FROM roots)
), asked AS MATERIALIZED (
  SELECT l.order_id AS root, l.product_id, SUM(l.qty_ordered) AS req,
         MAX(l.stock_current_qty) AS cur, MAX(l.stock_incoming_qty) AS inc,
         MAX(l.stock_min_qty) AS mn, MAX(l.stock_max_qty) AS mx, MAX(l.stock_suggested_qty) AS sug,
         MAX(l.stock_alert_status) AS alert
  FROM denri_dispatch_order_line l WHERE l.order_id IN (SELECT id FROM roots)
  GROUP BY 1, 2
), moved AS MATERIALIZED (
  SELECT c.root, l.product_id, SUM(l.qty_fulfilled) AS sent, SUM(l.qty_received) AS rec,
         SUM(CASE WHEN c.state NOT IN ('done', 'cancel', 'received') THEN l.qty_remaining ELSE 0 END) AS pend
  FROM chain c JOIN denri_dispatch_order_line l ON l.order_id = c.oid
  GROUP BY 1, 2
), arrived AS MATERIALIZED (
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
FROM pos_order o JOIN POS_LINES(o) pl ON pl.order_id = o.id
JOIN pos_session ps ON ps.id = o.session_id
WHERE (o.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date BETWEEN :s AND :e
  AND o.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0
GROUP BY 1, 2, 3
"""

# Warehouse sends INTO a shop's stock — the Shops menu's dispatch basis (sql/combined_distribution.sql):
# done stock moves from FINWH/Goods in Transit, CBD/Stock or FINWH/Stock into <CODE>/Stock. Stock counts
# (inventory adjustments), returns and shop-to-shop moves are left out.
SENT_SQL = """
SELECT split_part(d.complete_name, '/', 1) AS code, m.product_id, pt."name" AS product,
       MIN((m."date" AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date) AS first_in, SUM(m.product_qty) AS qty
FROM stock_move m
JOIN stock_location s ON s.id = m.location_id JOIN stock_location d ON d.id = m.location_dest_id
JOIN product_product pp ON pp.id = m.product_id JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE m.state = 'done' AND d.usage = 'internal' AND split_part(d.complete_name, '/', 2) = 'Stock'
  AND (s.complete_name LIKE 'FINWH/Goods in Transit%' OR s.complete_name LIKE 'CBD/Stock%' OR s.complete_name LIKE 'FINWH/Stock%')
  AND split_part(d.complete_name, '/', 1) NOT IN ('CBD', 'FINWH', 'VLD')
  AND (m."date" AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date BETWEEN :s AND :e
  AND pt."name" NOT LIKE '%+%'
GROUP BY 1, 2, 3
"""

# KTDA also asks through the older Shop Request module (SRQ, ic_shop_request) — those asks count as asked-for too.
SRQ_SQL = """
SELECT w.name AS shop, l.product_id, SUM(l.qty_requested) AS qty
FROM ic_shop_request r JOIN ic_shop_request_line l ON l.request_id = r.id
JOIN stock_warehouse w ON w.id = r.shop_warehouse_id
WHERE r.state NOT IN ('cancel', 'declined')
  AND (r.date_requested AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date BETWEEN :s AND :e
GROUP BY 1, 2
"""

NOT_CONVERTING_PCT = 25     # a requested bag that sold under this % of what arrived within 14 days isn't converting
ASK_LOOKBACK = 14           # a send counts as asked-for if the shop asked for that product up to 14 days before

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


def requests(start, end, today, shop_name, typ, offers=None, code_shop=None, have=None, no_shelf=(), target=None,
             prepaid_at=None):
    """Per shop: requests in [start, end] — totals, the three checks, effectiveness %, dispatch fill and the bags;
    plus bags SENT WITHOUT A REQUEST (warehouse sends beyond what the shop asked for) and requested bags NOT
    CONVERTING (received, but under NOT_CONVERTING_PCT % sold within 14 days).
    shop_name(dispatch shop name) → the page's shop name; code_shop(stock location code) → the same names;
    have = {SHOP: {BAG: units on the shelf now}}; no_shelf = online shops (never in "sent without a request").
    target = {"need": {SHOP: {BAG: monthly need}}, "days": days in that month, "minDays", "maxDays",
              "now": True when the period is this month (then "target needs it, not asked" uses the shelf now)}
    — since 26 Oct 2026 the weekly sales rate as a month's need (Min 1 week, Max 2.5 weeks), so the right-bag
    check and asked vs need are judged on what really sells (docs/shop-stock-levels.md › realistic performance).
    prepaid_at(shop, bag, date) = units customers had prepaid and were still waiting for (they count as out of stock)."""
    tneed = (target or {}).get("need") or {}
    tdays = (target or {}).get("days") or 30

    def tmax(shop, bag, days_key="maxDays"):
        nd = tneed.get(shop, {}).get(bag, 0.0)
        return math.ceil(nd / tdays * target[days_key]) if nd > 0 else 0
    look = start - datetime.timedelta(days=ASK_LOOKBACK)
    df = db.run_query(REQUESTS_SQL, {"s": look.isoformat(), "e": end.isoformat()})
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
    asked = collections.Counter()                         # (shop, product id) → asked from `look` to `end`
    cfg_of = {}
    for x in lines:
        asked[(x["shop"], x["pid"])] += x["req"]
        if x["cfg"]:
            cfg_of[x["shop"]] = x["cfg"]
    srq = db.run_query(SRQ_SQL, {"s": look.isoformat(), "e": end.isoformat()})
    for r in (srq.itertuples() if srq is not None else []):
        shop = shop_name(r.shop)
        if shop:
            asked[(shop, int(r.product_id))] += _f(r.qty)
    lines = [x for x in lines if x["d"] >= start]
    if not lines:
        return {}

    # Warehouse sends into each shop in the period (the Shops menu's dispatch basis).
    sent_in = collections.defaultdict(lambda: {"qty": 0.0, "first": None, "product": "", "bag": ""})
    if code_shop:
        sq = db.run_query(SENT_SQL, {"s": start.isoformat(), "e": end.isoformat()})
        for r in (sq.itertuples() if sq is not None else []):
            shop, bag = code_shop(r.code), typ(str(r.product))
            if not shop or not bag or shop in no_shelf:
                continue
            k = sent_in[(shop, int(r.product_id))]
            k["qty"] += _f(r.qty)
            k["first"] = min(k["first"] or _d(r.first_in), _d(r.first_in))
            k["product"], k["bag"] = str(r.product), bag

    # Sales per till × product × day from the period start / first receipt on — sell-through and sold-since.
    rcvs = [x["rcv"] for x in lines if x["rcv"]] + [start]
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
                                           "low": 0.0, "offer": 0.0, "cur": 0.0, "mx": 0.0, "short": 0.0,
                                           "t_ok": 0.0, "t_base": 0.0, "t_over": 0.0, "t_off": 0.0, "bags": {}})
    t_ask = collections.defaultdict(dict)                   # (shop, bag) → {request: {d, have (stock + incoming), req}}
    bag_have = collections.Counter()                        # (request, bag) → stock + incoming of its requested colours
    for x in lines:
        bag_have[(x["root"], x["bag"])] += x["cur"] + x["inc"]
    q_ask = {}                                              # (shop, product id) → {bag, sug (largest), req (total)}
    for x in lines:
        a = acc[x["shop"]]
        a["orders"].add(x["root"])
        req, sent = x["req"], min(x["sent"], x["req"])
        a["req"] += req
        a["sent"] += x["sent"]
        a["rec"] += x["rec"]
        a["pend"] += x["pend"]
        a["fill"] += sent
        short = max(req - x["sent"] - x["pend"], 0.0)                 # asked, closed without being sent
        a["short"] += short
        off = offer(x["bag"], x["d"])
        if target:
            # Realistic: the bag's stock when asked (requested colours, on hand + incoming) at or under 1 week of
            # sales, the colour out, or a prepaid customer still waiting for the bag (out of stock).
            bh = bag_have[(x["root"], x["bag"])]
            low = (x["cur"] <= 0 or bh <= tmax(x["shop"], x["bag"], "minDays")
                   or bool(prepaid_at and prepaid_at(x["shop"], x["bag"], x["d"]) > 0))
            half_max = tmax(x["shop"], x["bag"]) / 2
        else:
            bh = x["cur"] + x["inc"]
            low = x["cur"] <= 0 or x["alert"] in ("stockout", "below_min") or (x["mn"] > 0 and x["cur"] <= x["mn"])
            half_max = x["mx"] / 2
        if low:
            a["low"] += req
        if off:
            a["offer"] += req
        # check 1 — right bag: low when asked, or on an offer while under half of Max (offers run all month on most
        # bags, so an offer alone doesn't make a full shelf need more)
        right = low or (off and half_max > 0 and bh < half_max)
        if right:
            a["need_ok"] += req
        if x["sug"] > 0:                                              # check 2 — right qty, judged per product below
            q = q_ask.setdefault((x["shop"], x["pid"]), {"bag": x["bag"], "sug": 0.0, "req": 0.0})
            q["sug"] = max(q["sug"], x["sug"])
            q["req"] += req
        st = None
        if x["rcv"] and x["rec"] > 0 and (today - x["rcv"]).days >= SELL_DAYS and x["cfg"]:   # check 3 — sold through
            s14 = sum(sold.get((x["cfg"], x["pid"], x["rcv"] + datetime.timedelta(days=i)), 0.0) for i in range(SELL_DAYS))
            st = min(max(s14, 0), x["rec"])
            a["st_sold"] += st
            a["st_base"] += x["rec"]
        # vs target — collected per shop × bag × request (all colours), judged once per bag below
        if target:
            tg = t_ask[(x["shop"], x["bag"])].setdefault(x["root"], {"d": x["d"], "have": 0.0, "req": 0.0})
            tg["have"] += x["cur"] + x["inc"]
            tg["req"] += req
        a["cur"] += x["cur"]
        a["mx"] += x["mx"]
        b = a["bags"].setdefault(x["bag"], {"bag": x["bag"], "req": 0.0, "sent": 0.0, "rec": 0.0, "pend": 0.0, "cur": 0.0,
                                            "mx": 0.0, "sug": 0.0, "low": 0.0, "fit": 0.0, "fitBase": 0.0, "st": 0.0, "stBase": 0.0,
                                            "orders": 0, "offer": "", "last": None, "short": 0.0, "matched": 0.0,
                                            "tIn": 0.0, "tGap": 0.0, "tOver": 0.0, "tOff": 0.0, "lines": []})
        b["req"] += req
        b["sent"] += x["sent"]
        b["rec"] += x["rec"]
        b["pend"] += x["pend"]
        b["cur"] += x["cur"]
        b["mx"] += x["mx"]
        b["orders"] += 1
        b["short"] += short
        b["matched"] += sent
        if low:
            b["low"] += req
        if st is not None:
            b["st"] += st
            b["stBase"] += x["rec"]
        if off and not b["offer"]:
            b["offer"] = off
        b["last"] = max(b["last"] or x["d"], x["d"])
        if len(b["lines"]) < 12:
            b["lines"].append({"ref": x["ref"], "d": x["d"].isoformat(), "product": x["product"], "req": int(req),
                               "sent": int(x["sent"]), "rec": int(x["rec"]), "pend": int(x["pend"]), "short": int(short), "cur": int(x["cur"]),
                               "inc": int(x["inc"]), "mn": int(x["mn"]), "mx": int(x["mx"]), "sug": int(x["sug"]), "alert": x["alert"],
                               "offer": off, "rcv": x["rcv"].isoformat() if x["rcv"] else None,
                               "sold14": None if st is None else int(st)})

    # Right qty, once per shop × product: everything asked in the period vs the LARGEST suggestion Odoo made at any
    # of those requests (summing each request's suggestion counted the same shortfall again on every re-order).
    for (shop, pid), q in q_ask.items():
        a, b = acc[shop], acc[shop]["bags"][q["bag"]]
        fit = min(q["req"], q["sug"])
        a["qty_ok"] += fit
        a["qty_base"] += q["sug"]
        b["fit"] += fit
        b["fitBase"] += q["sug"]
        b["sug"] += q["sug"]

    # Asks vs target, once per shop × bag: target refill = (target Max − stock + incoming, all colours, at the first
    # request in the period) + the daily target need × days from that request to the period end (or today).
    end_eff = min(end, today)
    for (shop, bag), rq in t_ask.items():
        a, b = acc[shop], acc[shop]["bags"][bag]
        asked_t = sum(r["req"] for r in rq.values())
        nd = tneed.get(shop, {}).get(bag, 0.0)
        if nd <= 0:
            a["t_off"] += asked_t
            b["tOff"] += asked_t
            continue
        first = min(rq.values(), key=lambda r: r["d"])
        gap = max(tmax(shop, bag) - first["have"], 0.0) + nd / tdays * max((end_eff - first["d"]).days, 0)
        t_in = min(asked_t, gap)
        a["t_ok"] += t_in
        a["t_base"] += gap
        a["t_over"] += asked_t - t_in
        b["tIn"], b["tGap"], b["tOver"] = t_in, gap, asked_t - t_in

    by_sp = collections.defaultdict(list)                  # (till, product id) → [(date, qty)]
    for (c, p, d), v in sold.items():
        by_sp[(c, p)].append((d, v))

    def sold_since(shop, pid, d0):
        cfg = cfg_of.get(shop)
        if not cfg or not d0:
            return 0.0
        return sum(v for d, v in by_sp.get((cfg, pid), []) if d >= d0)

    # Sent without a request: per shop × product, warehouse sends beyond what the shop asked for (from 14 days
    # before the period to its end). "Never asked" = no ask for that product at all in that window.
    unasked = collections.defaultdict(dict)
    for (shop, pid), k in sent_in.items():
        a_q = asked.get((shop, pid), 0.0)
        extra = k["qty"] - a_q
        if extra <= 0:
            continue
        b = unasked[shop].setdefault(k["bag"], {"bag": k["bag"], "sent": 0.0, "asked": 0.0, "extra": 0.0, "sold": 0.0,
                                                "never": True, "first": k["first"], "products": []})
        b["sent"] += k["qty"]
        b["asked"] += a_q
        b["extra"] += extra
        b["never"] = b["never"] and a_q == 0
        b["first"] = min(b["first"], k["first"])
        sl = min(sold_since(shop, pid, k["first"]), k["qty"])
        b["sold"] += sl
        b["products"].append({"product": k["product"], "sent": int(k["qty"]), "asked": int(a_q), "extra": int(extra),
                              "first": k["first"].isoformat(), "sold": int(sl)})

    out = {}
    for shop in set(unasked) - set(acc):
        ua = sorted(unasked[shop].values(), key=lambda b: -b["extra"])
        out[shop] = {"orders": 0, "req": 0, "sent": 0, "rec": 0, "pend": 0, "fill": None, "recPct": None, "lowPct": None,
                     "offerPct": None, "checks": {"need": None, "qty": None, "sell": None}, "score": None,
                     "sellBase": 0, "sug": 0, "bags": [], "notConverting": [], "short": 0, "matched": 0, "notGot": [],
                     **_unasked_block(ua, have, shop)}
        out[shop]["match"] = _match(0, 0, out[shop]["unasked"])
        out[shop].update(_target_block(shop, None, [], have, target, tneed, tmax))
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
                      "tGap": int(b["tGap"]), "tIn": int(b["tIn"]), "tOver": int(b["tOver"] + b["tOff"]),
                      "offer": b["offer"], "last": b["last"].isoformat() if b["last"] else None,
                      "lines": b["lines"]} for b in bags],
            "notConverting": sorted([{"bag": b["bag"], "rec": int(b["stBase"]), "sold14": int(b["st"]),
                                      "pct": _pct(b["st"], b["stBase"]), "req": int(b["req"]), "offer": b["offer"],
                                      "have": int(((have or {}).get(shop) or {}).get(b["bag"], 0)),
                                      "lines": [l for l in b["lines"] if l["sold14"] is not None]}
                                     for b in bags if b["stBase"] > 0 and b["st"] / b["stBase"] * 100 < NOT_CONVERTING_PCT],
                                    key=lambda r: (r["pct"] or 0, -r["rec"])),
            "short": int(a["short"]), "matched": int(a["fill"]),
            **_target_block(shop, a, bags, have, target, tneed, tmax),
            "notGot": sorted([{"bag": b["bag"], "req": int(b["req"]), "sent": int(b["sent"]), "matched": int(b["matched"]),
                               "pend": int(b["pend"]), "short": int(b["short"]), "orders": b["orders"],
                               "have": int(((have or {}).get(shop) or {}).get(b["bag"], 0)),
                               "lines": [l for l in b["lines"] if l["short"] or l["pend"]]}
                              for b in bags if b["short"] >= 1 or b["pend"] >= 1],
                             key=lambda r: (-r["short"], -r["pend"])),
            **_unasked_block(sorted(unasked.get(shop, {}).values(), key=lambda b: -b["extra"]), have, shop),
        }
        out[shop]["match"] = _match(a["fill"], a["short"], out[shop]["unasked"])
    return out


def _target_block(shop, a, bags, have, target, tneed, tmax):
    """Asks vs the shop's target need: % of the target gap asked, units over / off target, and (this month) bags the
    target says need a refill that the shop hasn't asked for."""
    if not target:
        return {"vsTarget": None, "tOver": 0, "tOff": 0, "tMissed": 0, "targetBags": []}
    on_shelf = (have or {}).get(shop) or {}
    rows = [{"bag": b["bag"], "need": round(tneed.get(shop, {}).get(b["bag"], 0.0)), "tmax": tmax(shop, b["bag"]),
             "req": int(b["req"]), "gap": int(b["tGap"]), "in": int(b["tIn"]), "over": int(b["tOver"]),
             "off": int(b["tOff"]), "missed": 0, "have": int(on_shelf.get(b["bag"], 0))}
            for b in bags if b["tOver"] >= 1 or b["tOff"] >= 1 or b["tGap"] - b["tIn"] >= 1]
    missed = 0
    if target.get("now"):
        asked_bags = {b["bag"] for b in bags}
        for bag, nd in (tneed.get(shop) or {}).items():
            h = on_shelf.get(bag, 0)
            if nd <= 0 or bag in asked_bags or h > tmax(shop, bag, "minDays"):
                continue
            m = max(tmax(shop, bag) - h, 0)
            if m >= 1:
                missed += m
                rows.append({"bag": bag, "need": round(nd), "tmax": tmax(shop, bag), "req": 0, "gap": int(m), "in": 0,
                             "over": 0, "off": 0, "missed": int(m), "have": int(h)})
    rows.sort(key=lambda r: -(r["missed"] + r["off"] + r["over"] + r["gap"] - r["in"]))
    return {"vsTarget": _pct(a["t_ok"], a["t_base"]) if a else None,
            "tGap": int(a["t_base"]) if a else 0, "tIn": int(a["t_ok"]) if a else 0,
            "tOver": int(a["t_over"]) if a else 0, "tOff": int(a["t_off"]) if a else 0,
            "tMissed": int(missed), "targetBags": rows}


def _match(matched, short, unasked):
    """Got what it asked % — matched ÷ (matched + asked-not-got + sent-without-a-request); None with nothing to judge."""
    return _pct(matched, matched + short + unasked)


def _unasked_block(rows, have, shop):
    return {"unasked": int(sum(b["extra"] for b in rows)),
            "unaskedNever": int(sum(b["extra"] for b in rows if b["never"])),
            "unaskedSold": int(sum(min(b["sold"], b["extra"]) for b in rows)),
            "unaskedBags": [{"bag": b["bag"], "sent": int(b["sent"]), "asked": int(b["asked"]), "extra": int(b["extra"]),
                             "never": b["never"], "first": b["first"].isoformat(), "sold": int(min(b["sold"], b["extra"])),
                             "have": int(((have or {}).get(shop) or {}).get(b["bag"], 0)),
                             "products": b["products"][:12]} for b in rows]}


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
    if df is None:                                            # a cancelled query would show every ask as 0
        raise RuntimeError("Odoo unreachable (shop requests for the approved lists)")
    reqs = [r for r in df.itertuples()]

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
