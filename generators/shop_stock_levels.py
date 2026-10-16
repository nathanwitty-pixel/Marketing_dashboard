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
from lib import db, queries, colours, oos_callbacks, product_targets, runway_bags
from lib import stock as stock_lib

HTML = paths.html("shop_stock_levels.html")
MIN_DAYS, MAX_DAYS = 7, 21          # min = 7 days of need, max = 21 days (user's choice, 16 Oct 2026)
NEXT_MONTH_FROM_DAY = 15            # next-month preparedness opens on the 15th
WAREHOUSE = stock_lib.RESTOCK_LOCATION   # CBD/Stock — restocks the Kenya shops

# Canonical shop names = the leads / WhatsApp names (lib/oos_callbacks).
TILL_SHOP = {"STARMALL": "Starmall", "MOMBASA": "Mombasa", "NAKURU": "Nakuru", "ELDORET": "Eldoret", "KISUMU": "Kisumu",
             "MERU": "Meru", "THIKA": "Thika", "HAZINA": "Hazina", "KITENGELA": "Kitengela", "NANYUKI": "Nanyuki",
             "KAKAMEGA": "Kakamega", "HILTON": "Hilton", "KISII": "Kisii", "KTDA SHOP": "Ktda", "KTDA": "Ktda",
             "BUSIA": "Busia", "RONGAI": "Rongai", "DAR-ES-ALAM": "Sinza", "SINZA": "Sinza", "UGANDA": "Uganda",
             "WEBSITE SALES": "Website", "WEBSITE": "Website"}
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
  AND o."name" <> ALL(:corp_refs)   -- Corporate-team till orders are Corporate's, not the shop's history
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
    try:
        from lib import shop_corporate
        corp = sorted(shop_corporate.corporate_team_receipts(start, end))
    except Exception as e:                                   # noqa: BLE001
        print(f"  Corporate-team till orders: skipped ({e})")
        corp = []
    df = db.run_query(SALES_SQL, {"s": start.isoformat(), "e": end.isoformat(), "excluded": queries.excluded_products(),
                                  "corp_refs": corp or ["~none~"]})
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
    nm_targets = product_targets.load_targets(nm1, build_if_missing=False)
    nm_shop = shop_targets(nm1)
    nm_estimated = not (nm_targets and nm_shop)
    if nm_open and not nm_estimated:
        nm_need = needs(nm1, typ, base, nm_targets, nm_shop)
    else:
        nm_need = need
    nm_days = calendar.monthrange(nm1.year, nm1.month)[1]

    stock, stock_cols = shop_stock(typ)
    wh, wh_cols = warehouse_stock(typ)
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
            "minDays": MIN_DAYS, "maxDays": MAX_DAYS, "warehouse": WAREHOUSE,
            "base": f"{b0.strftime('%d %b')} – {b1.strftime('%d %b %Y')}",
            "nextMonth": {"label": nm1.strftime("%B %Y"), "open": nm_open, "opensOn": m1.replace(day=NEXT_MONTH_FROM_DAY).isoformat(),
                          "estimated": nm_estimated},
            "shopTargets": {s: round(v) for s, v in shop_tgt.items()}, "outside": sorted(OUTSIDE), "online": sorted(ONLINE),
            "rows": rows, "wh": {b: int(q) for b, q in wh.items() if q},
            "whColours": {b: {c: int(q) for c, q in cs.items() if q} for b, cs in wh_cols.items()},
            "leads": waiting, "leadWindows": lead_wins}


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
