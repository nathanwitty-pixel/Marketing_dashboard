"""shop_stock_levels.py — the Shop Stock Levels page: min / max per shop × bag from the month's targets, the
stocks report (have · need · missing · month-end balance), next-month preparedness and the out-of-stock
call-backs per shop. Spec: docs/shop-stock-levels.md.

    python shop_stock_levels.py        # DENRI_LAUNCHER=1 to skip the browser tab
"""
import calendar
import collections
import csv
import datetime
import json
import math
import os
import re
import sys
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root → lib/
from lib import paths
from lib import db, queries, colours, oos_callbacks, product_targets, runway_bags, shop_requests
from lib import stock as stock_lib
from lib import shop_regions

HTML = paths.html("shop_stock_levels.html")
MIN_DAYS, MAX_DAYS = 7, 21          # min = 7 days of need, max = 21 days (user's choice, 16 Oct 2026)
NEXT_MONTH_FROM_DAY = 15            # next-month preparedness opens on the 15th
WAREHOUSE = stock_lib.RESTOCK_LOCATION   # CBD/Stock — restocks the Kenya shops

# Canonical shop names = the leads / WhatsApp names (lib/oos_callbacks).
TILL_SHOP = {"STARMALL": "Starmall", "MOMBASA": "Mombasa", "NAKURU": "Nakuru", "ELDORET": "Eldoret", "KISUMU": "Kisumu",
             "MERU": "Meru", "THIKA": "Thika", "HAZINA": "Hazina", "KITENGELA": "Kitengela", "NANYUKI": "Nanyuki",
             "KAKAMEGA": "Kakamega", "HILTON": "Hilton", "KISII": "Kisii", "KTDA SHOP": "Ktda", "KTDA": "Ktda",
             "BUSIA": "Busia", "RONGAI": "Rongai", "DAR-ES-ALAM": "Sinza", "SINZA": "Sinza", "UGANDA": "Uganda",
             "WEBSITE SALES": "Website", "WEBSITE": "Website", "WEBSITE STORE": "Website"}
CODE_SHOP = {"STAR": "Starmall", "MSA": "Mombasa", "NAKS": "Nakuru", "ELD": "Eldoret", "KSM": "Kisumu", "MERU": "Meru",
             "THK": "Thika", "HAZ": "Hazina", "KITE": "Kitengela", "NAN": "Nanyuki", "KAK": "Kakamega", "HTN": "Hilton",
             "KSI": "Kisii", "KTDA": "Ktda", "BUSIA": "Busia", "RONG": "Rongai", "DAR": "Sinza", "UG": "Uganda",
             "WEB": "Website"}
OUTSIDE = {"Sinza", "Uganda"}
ONLINE = {"Website"}                # no stock of its own — the page shows only who is waiting there
_CODES = ", ".join("'%s'" % c for c in CODE_SHOP)

SALES_SQL = """
SELECT upper(COALESCE(pc."name", '')) AS till, pt."name" AS product, SUM(pl.qty) AS qty
FROM pos_order o
JOIN pos_order_line pl ON pl.order_id = o.id
LEFT JOIN pos_session ps ON ps.id = o.session_id
LEFT JOIN pos_config pc ON pc.id = ps.config_id
JOIN product_product pp ON pp.id = pl.product_id
JOIN product_template pt ON pt.id = pp.product_tmpl_id
LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
WHERE (o.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date BETWEEN :s AND :e
  AND o.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0
  AND COALESCE(pl.is_program_reward, false) = false
  AND NOT (COALESCE(pl.is_combo_line, false) OR pt."name" LIKE '%+%')
  AND pt."name" NOT ILIKE '%delivery%' AND pt."name" NOT ILIKE '%customi%' AND pt."name" NOT ILIKE '%strap%'
  AND pt."name" NOT ILIKE '%KES discount%' AND pt."name" NOT ILIKE '%sample%' AND pt."name" NOT ILIKE 'gift bag%'
  AND COALESCE(pcat."name", '') NOT ILIKE '%Pos%'
  AND lower(pt."name") <> ALL(:excluded)
GROUP BY 1, 2
"""

SHOP_STOCK_SQL = """
SELECT split_part(l.complete_name, '/', 1) AS code, pt."name" AS product, SUM(q.quantity) AS qty
FROM stock_quant q JOIN stock_location l ON l.id = q.location_id
JOIN product_product pp ON pp.id = q.product_id JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE l.usage = 'internal' AND split_part(l.complete_name, '/', 1) IN (""" + _CODES + """)
  AND pt."name" NOT LIKE '%+%'
GROUP BY 1, 2
"""

SHOP_TARGETS_SQL = """
SELECT upper(pc."name") AS till, SUM(t.target_qty)::float AS qty
FROM sales_pos_target t JOIN pos_config pc ON pc.id = t.config_id
WHERE t.period = 'month' AND t.target_scope = 'pos' AND t.start_date = :m
GROUP BY 1
"""

TOTAL_SQL = """
SELECT SUM(target_qty)::float AS qty FROM sales_pos_target
WHERE period = 'month' AND start_date = :m AND target_scope IN ('pos', 'corporate')
"""


def _num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return 0.0
    return f if f == f else 0.0


def _shop(till):
    return TILL_SHOP.get(str(till or "").upper().strip())


def _next_month(d):
    return (d.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)


def sales(start, end, typ):
    """({SHOP: {BAG: units}}, {SHOP: {BAG: {colour: units}}}) over [start, end]."""
    df = db.run_query(SALES_SQL, {"s": start.isoformat(), "e": end.isoformat(), "excluded": queries.excluded_products()})
    if df is None:
        raise RuntimeError("Odoo unreachable")
    out = collections.defaultdict(collections.Counter)
    cols = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for r in df.itertuples():
        s, b = _shop(r.till), typ(r.product)
        if s and b:
            q = _num(r.qty)
            out[s][b] += q
            cols[s][b][colours.family(str(r.product), "") or "No colour"] += q
    return out, cols


def shop_targets(month_start):
    df = db.run_query(SHOP_TARGETS_SQL, {"m": month_start.isoformat()})
    out = collections.Counter()
    for r in (df.itertuples() if df is not None else []):
        s = _shop(r.till)
        if s:
            out[s] += _num(r.qty)
    return dict(out)


def grand_total(month_start):
    df = db.run_query(TOTAL_SQL, {"m": month_start.isoformat()})
    return _num(df.qty[0]) if df is not None and len(df) else 0.0


def new_bags(month_start):
    """Bags launched inside the base period (the bag-targets CSV's Launch column)."""
    path = paths.data("product_targets_%s.csv" % month_start.strftime("%Y-%m"))
    try:
        with open(path, encoding="utf-8", newline="") as f:
            return {r["Bag"].strip().upper() for r in csv.DictReader(f) if (r.get("Launch (first sale)") or "").strip()}
    except OSError:
        return set()


def fit(seed, row_tot, col_tot, iters=50):
    """Iterative proportional fitting: scale `seed` {shop: {bag: w}} so rows sum to row_tot and columns to
    col_tot (col_tot is first rescaled to the rows' grand total). Cells that start at 0 stay 0."""
    rt = sum(row_tot.values())
    ct = sum(col_tot.values()) or 1
    col = {b: v * rt / ct for b, v in col_tot.items()}
    m = {s: {b: w for b, w in bs.items() if w > 0 and b in col} for s, bs in seed.items() if s in row_tot}
    for _ in range(iters):
        for s, bs in m.items():
            tot = sum(bs.values())
            if tot:
                k = row_tot[s] / tot
                for b in bs:
                    bs[b] *= k
        csum = collections.Counter()
        for bs in m.values():
            for b, w in bs.items():
                csum[b] += w
        for bs in m.values():
            for b in bs:
                if csum[b]:
                    bs[b] *= col[b] / csum[b]
    return m


def needs(month_start, typ, base_sales, targets, shop_tgt):
    """{SHOP: {BAG: monthly need (float)}} for the month."""
    gt = grand_total(month_start) or sum(targets.values())
    shops_total = sum(shop_tgt.values())
    # Corporate's share comes out of each bag target pro rata.
    col = {b: t * (shops_total / gt if gt else 1) for b, t in targets.items() if t > 0}
    fresh = new_bags(month_start)
    share = {s: v / shops_total for s, v in shop_tgt.items()} if shops_total else {}
    seed = {}
    for s in shop_tgt:
        row = {b: max(_num(base_sales.get(s, {}).get(b, 0)), 0) for b in col}
        for b in fresh & set(col):            # new bags: every shop starts at its overall share
            row[b] = max(row.get(b, 0), share.get(s, 0) * col[b])
        seed[s] = row
    return fit(seed, shop_tgt, col)


def shop_stock(typ):
    """({SHOP: {BAG: units}}, {SHOP: {BAG: {colour: units}}}) — on hand in the shops now."""
    df = db.run_query(SHOP_STOCK_SQL, {})
    out = collections.defaultdict(collections.Counter)
    cols = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for r in (df.itertuples() if df is not None else []):
        s, b, q = CODE_SHOP.get(r.code), typ(r.product), _num(r.qty)
        if s and b and q:
            out[s][b] += q
            cols[s][b][colours.family(str(r.product), "") or "No colour"] += q
    return out, cols


def warehouse_stock(typ):
    """({BAG: units}, {BAG: {colour: units}}) at CBD/Stock."""
    out, cols = collections.Counter(), collections.defaultdict(collections.Counter)
    for name, q in (stock_lib.odoo_stock_at_location(WAREHOUSE) or {}).items():
        b = typ(name)
        if b and q:
            out[b] += q
            cols[b][colours.family(str(name), "") or "No colour"] += q
    return out, cols


BUFFER_LOCATIONS = ("CBD/Stock", "VLD/Stock")   # restock the Kenya shops — November preparedness "with" stock


def buffer_stock(typ):
    """{location: {BAG: units}} at CBD/Stock and VLD/Stock (exact locations)."""
    out = {}
    for loc in BUFFER_LOCATIONS:
        c = collections.Counter()
        for name, q in (stock_lib.odoo_stock_at_location(loc) or {}).items():
            b = typ(name)
            if b and q:
                c[b] += q
        out[loc] = c
    return out


PRODUCTION_LISTS = 16        # approved lists kept per country (~4 months) for the Production period / date range
CORE_CATEGORIES = ("BACKPACK", "TRAVEL", "HANDBAG", "MAN BAG", "SLING")   # ~75 % of bags sold (user, 18 Oct 2026)


def bag_categories():
    """{BAG: CATEGORY} from data/bag_tiers.csv (blank category left out)."""
    out = {}
    try:
        with open(paths.data("bag_tiers.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(ln for ln in f if not ln.startswith("#")):
                if r.get("BAG") and (r.get("CATEGORY") or "").strip():
                    out[r["BAG"].strip().upper()] = r["CATEGORY"].strip().upper()
    except OSError:
        pass
    return out


def leads(typ, today):
    """{period: {SHOP: {BAG: {"n", "online", "walkin", "colours": {c: n}}}}} — people still waiting, asked in the period."""
    rows = oos_callbacks.load_rows()
    wins = oos_callbacks.windows(today)
    out = {}
    for per in ("lastweek", "weekly", "monthly", "lifetime"):
        acc = collections.defaultdict(lambda: collections.defaultdict(lambda: {"all": set(), "online": set(), "walkin": set(),
                                                                            "colours": collections.defaultdict(set)}))
        for r in rows:
            if r["purchased"]:
                continue
            if per != "lifetime":
                s, e = wins[per]
                if not (s <= r["date"] <= e):
                    continue
            shop = r["shop"] if r["shop"] in CODE_SHOP.values() else _shop(r["shop"])
            b = typ(r["product"])
            if not shop or not b:
                continue
            x = acc[shop][b]
            x["all"].add(r["person"])
            x[r["channel"]].add(r["person"])
            x["colours"][colours.family(r["product"], "") or "Any colour"].add(r["person"])
        out[per] = {s: {b: {"n": len(x["all"]), "online": len(x["online"]), "walkin": len(x["walkin"]),
                            "colours": {c: len(p) for c, p in x["colours"].items()}}
                        for b, x in bs.items()} for s, bs in acc.items()}
    return out, {p: [w[0].isoformat(), w[1].isoformat()] for p, w in wins.items() if p in ("lastweek", "weekly", "monthly")}


def dispatch_shop(name):
    """Dispatch-module shop name (ELDORET, DAR-ES-ALAM, NYERI…) → the page's shop name."""
    return _shop(name) or str(name or "").strip().title() or None


def requests_block(today, typ, have=None, targets=None):
    """Shop requests vs received (this month · last month) and the production approved lists — or {} on failure."""
    m1 = today.replace(day=1)
    lm1 = (m1 - datetime.timedelta(days=1)).replace(day=1)
    try:
        offers = shop_requests._offers()
        per = {"monthly": (m1, today, m1.strftime("%B %Y")),
               "lastmonth": (lm1, m1 - datetime.timedelta(days=1), lm1.strftime("%B %Y"))}
        out = {"sellDays": shop_requests.SELL_DAYS, "notConvertingPct": shop_requests.NOT_CONVERTING_PCT,
               "askLookback": shop_requests.ASK_LOOKBACK, "periods": {}}
        for k, (s, e, label) in per.items():
            out["periods"][k] = {"label": label, "from": s.isoformat(), "to": e.isoformat(),
                                 "shops": shop_requests.requests(s, e, today, dispatch_shop, typ, offers,
                                                                  code_shop=CODE_SHOP.get, have=have, no_shelf=ONLINE,
                                                                  target=(targets or {}).get(k))}
        try:
            out["production"] = shop_requests.production(dispatch_shop, typ, today, keep=PRODUCTION_LISTS)
        except Exception as e:                               # noqa: BLE001
            print(f"  Production lists: skipped ({e})")
            out["production"] = []
        return out
    except Exception as e:                                   # noqa: BLE001
        print(f"  Shop requests: skipped ({e})")
        return {}


PUSH_MONTHS = 3                     # month-end lift: from the same days of the last 3 closed months
PUSH_CLAMP = (1.0, 1.5)             # kept between 1.0× (no lift) and 1.5×


def month_end_lift(today, typ):
    """How much faster the shops sell in the rest of the month than before it, from the last PUSH_MONTHS months:
    (units a day from today's day-of-month to month end) ÷ (units a day on days 1 … day before). Median, clamped.
    Returns (lift, [{"month", "lift"}]) — lift 1.0 when there is no history (e.g. on the 1st)."""
    day, per = today.day, []
    m = today.replace(day=1)
    for _ in range(PUSH_MONTHS):
        m = (m - datetime.timedelta(days=1)).replace(day=1)
        dim = calendar.monthrange(m.year, m.month)[1]
        if day < 2 or day > dim:
            continue
        try:
            early, _ = sales(m, m.replace(day=day - 1), typ)
            late, _ = sales(m.replace(day=day), m.replace(day=dim), typ)
        except Exception as e:                               # noqa: BLE001
            print(f"  Shop stock levels: month-end lift unavailable for {m:%b %Y} ({e})")
            continue
        tot = lambda d: sum(q for s, bs in d.items() if s not in ONLINE for q in bs.values())  # noqa: E731
        e_rate, l_rate = tot(early) / (day - 1), tot(late) / (dim - day + 1)
        if e_rate > 0:
            per.append({"month": m.strftime("%b %Y"), "lift": round(l_rate / e_rate, 3)})
    if not per:
        return 1.0, per
    lifts = sorted(p["lift"] for p in per)
    mid = len(lifts) // 2
    med = lifts[mid] if len(lifts) % 2 else (lifts[mid - 1] + lifts[mid]) / 2
    return round(min(max(med, PUSH_CLAMP[0]), PUSH_CLAMP[1]), 3), per


def last_month_need(m1, typ):
    """Last month's shop × bag target need (its own Odoo targets) for judging last month's requests — or None."""
    lm1 = (m1 - datetime.timedelta(days=1)).replace(day=1)
    try:
        tg, st = product_targets.load_targets(lm1, build_if_missing=False), shop_targets(lm1)
        if not tg or not st:
            return None
        b0, b1 = product_targets.base_period(lm1)
        base, _ = sales(b0, b1, typ)
        return {"need": needs(lm1, typ, base, tg, st), "days": calendar.monthrange(lm1.year, lm1.month)[1],
                "now": False, "minDays": MIN_DAYS, "maxDays": MAX_DAYS}
    except Exception as e:                                   # noqa: BLE001
        print(f"  Shop requests: last month's targets unavailable ({e})")
        return None


def build(today=None):
    today = today or datetime.date.today()
    m1 = today.replace(day=1)
    days_in = calendar.monthrange(today.year, today.month)[1]
    days_left = days_in - today.day + 1            # today counts as still to sell
    typ = runway_bags.type_fn()

    b0, b1 = product_targets.base_period(m1)
    base, _ = sales(b0, b1, typ)
    mtd, _ = sales(m1, today, typ)
    targets = product_targets.load_targets(m1)
    shop_tgt = shop_targets(m1)
    need = needs(m1, typ, base, targets, shop_tgt)

    # Next month — its own Odoo targets when they exist, else this month's need as the estimate.
    nm1 = _next_month(m1)
    nm_open = today.day >= NEXT_MONTH_FROM_DAY
    nm_rev = nm1.strftime("%Y-%m") in product_targets.REVENUE_TARGETS
    nm_targets = product_targets.load_targets(nm1, build_if_missing=nm_rev)
    nm_shop = shop_targets(nm1)
    nm_info = {"source": "odoo"}
    if nm_targets and not nm_shop and nm_rev:
        # Revenue-target month (docs/product-targets.md): shop targets = this month's Odoo shop targets scaled to the
        # month's total units, each shop keeping its share (Corporate's share left out as usual in needs()).
        nm_total, nm_info = product_targets.total_for(nm1)
        gt = grand_total(m1) or sum(shop_tgt.values())
        if nm_total and gt:
            nm_shop = collections.Counter({s: v * nm_total / gt for s, v in shop_tgt.items()})
    nm_estimated = not (nm_targets and nm_shop)
    if nm_open and not nm_estimated:
        nb0, nb1 = product_targets.base_period(nm1)          # the month's own base (Nov → Aug – Oct, to today)
        nm_base, _ = sales(nb0, min(nb1, today), typ)
        nm_need = needs(nm1, typ, nm_base, nm_targets, nm_shop)
    else:
        nm_need = need
    nm_days = calendar.monthrange(nm1.year, nm1.month)[1]
    # Sales pace scenarios for the rest of the month (Target / Optimistic / Push) — the page picks one.
    lift, lift_per = month_end_lift(today, typ) if nm_open else (1.0, [])

    stock, stock_cols = shop_stock(typ)
    wh, wh_cols = warehouse_stock(typ)
    buf = buffer_stock(typ)
    waiting, lead_wins = leads(typ, today)
    # Only leads for real bags (the leads module takes free text — repairs, spare parts…).
    known = set(targets) | {b for sb in stock.values() for b in sb} | {b for sb in base.values() for b in sb}
    waiting = {per: {sh: {b: v for b, v in bs.items() if b in known} for sh, bs in shops.items()}
               for per, shops in waiting.items()}

    rows = []
    shops = sorted(set(shop_tgt) | set(stock))
    for s in shops:
        if s in ONLINE:                            # online shop: no shelf — only its waiting customers are shown
            continue
        bags = set(need.get(s, {})) | {b for b, q in stock.get(s, {}).items() if q > 0} \
               | {b for per in waiting.values() for b in per.get(s, {})}
        for b in sorted(bags):
            nd = need.get(s, {}).get(b, 0.0)
            daily = nd / days_in
            have = stock.get(s, {}).get(b, 0)
            sold = mtd.get(s, {}).get(b, 0)
            mn = math.ceil(daily * MIN_DAYS) if nd > 0 else 0
            mx = math.ceil(daily * MAX_DAYS) if nd > 0 else 0
            if nd <= 0 and have <= 0:
                status = "none"
            elif nd <= 0:
                status = "idle"                    # stock on the shelf, no need this month
            elif have <= 0:
                status = "oos"
            elif have <= mn and have < mx:
                status = "low"
            elif have > mx:
                status = "over"
            else:
                status = "ok"
            send = max(mx - have, 0) if status in ("oos", "low") else 0
            bal = have - daily * days_left
            runs_out = (today + datetime.timedelta(days=int(have / daily))).isoformat() if daily > 0 and bal < 0 else None
            nmd = nm_need.get(s, {}).get(b, 0.0) * (nm_days / days_in if nm_estimated else 1)
            rows.append({"shop": s, "bag": b, "need": round(nd, 1), "daily": round(daily, 2), "have": int(have),
                         "sold": int(sold), "min": mn, "max": mx, "status": status, "send": int(send),
                         "bal": round(bal), "runsOut": runs_out, "nm": round(nmd),
                         "nmShort": round(max(nmd - max(bal, 0), 0)),
                         "colours": {c: int(q) for c, q in stock_cols.get(s, {}).get(b, {}).items() if q}})

    return {"generated": datetime.datetime.now().strftime("%d %b %Y %H:%M"),
            "month": m1.strftime("%B %Y"), "today": today.isoformat(), "daysIn": days_in, "daysLeft": days_left,
            "daysGone": today.day,                 # days whose sales are in "sold" (today's so far included)
            "pace": {"lift": lift, "liftMonths": lift_per, "clamp": list(PUSH_CLAMP)},
            "minDays": MIN_DAYS, "maxDays": MAX_DAYS, "warehouse": WAREHOUSE,
            "base": f"{b0.strftime('%d %b')} – {b1.strftime('%d %b %Y')}",
            "nextMonth": {"label": nm1.strftime("%B %Y"), "open": nm_open, "opensOn": m1.replace(day=NEXT_MONTH_FROM_DAY).isoformat(),
                          "estimated": nm_estimated, "source": "estimate" if nm_estimated else nm_info.get("source"),
                          "revenue": nm_info.get("revenue"), "kesPerBag": nm_info.get("kesPerBag"),
                          "kpbFrom": nm_info.get("from"), "totalUnits": int(sum((nm_targets or {}).values())),
                          "shopsUnits": round(sum(nm_shop.values())) if nm_shop else 0},
            "shopTargets": {s: round(v) for s, v in shop_tgt.items()}, "outside": sorted(OUTSIDE), "online": sorted(ONLINE),
            "rows": rows, "wh": {b: int(q) for b, q in wh.items() if q},
            "cats": bag_categories(), "core": list(CORE_CATEGORIES),
            "regions": shop_regions.load(),
            "buffer": {loc: {b: int(q) for b, q in bs.items() if q} for loc, bs in buf.items()},
            "whColours": {b: {c: int(q) for c, q in cs.items() if q} for b, cs in wh_cols.items()},
            "leads": waiting, "leadWindows": lead_wins, "requests": requests_block(today, typ, {sh: dict(bs) for sh, bs in stock.items()},
                                      {"monthly": {"need": need, "days": days_in, "now": True,
                                                   "minDays": MIN_DAYS, "maxDays": MAX_DAYS},
                                       "lastmonth": last_month_need(m1, typ)})}


def inject(payload):
    with open(HTML, encoding="utf-8") as f:
        html = f.read()
    block = ("<!-- SSL_DATA_START -->\n<script>\nconst SSL = "
             + json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
             + ";\n</script>\n<!-- SSL_DATA_END -->")
    html = re.sub(r"<!-- SSL_DATA_START -->.*?<!-- SSL_DATA_END -->", lambda _m: block, html, flags=re.S)
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    p = build()
    rs = p["rows"]
    cnt = collections.Counter(r["status"] for r in rs)
    print(f"  Shop Stock Levels: {len(rs)} shop × bag rows over {len(p['shopTargets'])} shops — "
          f"{cnt['oos']} out of stock, {cnt['low']} below min, {cnt['ok']} ok, {cnt['over']} over max; "
          f"send now {sum(r['send'] for r in rs):,} units; next month {p['nextMonth']['label']}"
          f"{' (estimated)' if p['nextMonth']['estimated'] else ''}")
    inject(p)
    if os.environ.get("DENRI_LAUNCHER") != "1":
        webbrowser.open("file://" + HTML)
