"""lib/product_targets.py — each month's units-to-sell target per bag, from Odoo (spec: docs/product-targets.md).

Total = the month's Odoo targets for every shop till + Corporate. Split by each bag's share of the last
three complete months' sales (all tills + Corporate invoices), with NEW bags scaled to the days they were
in the shops (launch = first sale on any till; at least MIN_DAYS). No row for a bag that didn't sell.

    python -m lib.product_targets            # writes product_targets_<YYYY-MM>.csv for the live month
"""
import calendar
import collections
import csv
import datetime
import math
import os
import re

from . import db, queries, report_month

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIN_DAYS = 14

POS_SALES_SQL = """
SELECT pt."name" AS product, date_trunc('month', p.date_order)::date AS m, SUM(pl.qty) AS bags
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0
  AND COALESCE(pt."name", '') NOT LIKE '%+%' AND COALESCE(pt."name", '') NOT ILIKE '%delivery%'
  AND COALESCE(pt."name", '') NOT ILIKE '%customization%' AND COALESCE(pt."name", '') NOT ILIKE '%strap%'
  AND COALESCE(pt."name", '') NOT ILIKE '%KES discount%' AND COALESCE(pt."name", '') NOT ILIKE '%sample%'
  AND COALESCE(pcat."name", '') NOT ILIKE '%Pos%' AND lower(COALESCE(pt."name", '')) <> ALL(:excluded)
  AND COALESCE(pt."name", '') NOT ILIKE '%gift bag%'
GROUP BY 1, 2
"""

CORPORATE_SALES_SQL = """
WITH qinv AS (
  SELECT am.id, am.invoice_date FROM account_move am
  WHERE am.move_type = 'out_invoice' AND am.state = 'posted' AND am.invoice_date BETWEEN :s AND :e
    AND (am.payment_state IN ('paid', 'in_payment') OR (am.amount_total > 0 AND am.amount_residual / am.amount_total <= 0.25)))
SELECT pt."name" AS product, date_trunc('month', qinv.invoice_date)::date AS m, SUM(aml.quantity) AS bags
FROM account_move_line aml JOIN qinv ON qinv.id = aml.move_id
JOIN product_product pp ON pp.id = aml.product_id JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE aml.display_type IS NULL AND aml.product_id IS NOT NULL
GROUP BY 1, 2
"""

FIRST_SALE_SQL = """
SELECT pt."name" AS product, MIN(p.date_order::date) AS first_sale
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
JOIN product_product pp ON pp.id = pl.product_id JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE p.state IN ('done', 'invoiced', 'paid') AND pl.qty > 0
GROUP BY 1
"""

# Shop stock locations (top-level codes) — the shops + Website, never warehouses (lib/stock.py rule).
SHOP_CODES = ("STAR", "MSA", "NAKS", "ELD", "KSM", "MERU", "THK", "HAZ", "KITE", "NAN", "KAK", "HTN", "KSI",
              "KTDA", "BUSIA", "RONG", "DAR", "UG", "WEB")
_IN_SHOPS = "(l.usage = 'internal' AND split_part(l.complete_name, '/', 1) IN (%s))" % ", ".join("'%s'" % c for c in SHOP_CODES)

ONHAND_SQL = """
SELECT pt."name" AS product, SUM(q.quantity) AS qty
FROM stock_quant q JOIN stock_location l ON l.id = q.location_id
JOIN product_product pp ON pp.id = q.product_id JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE """ + _IN_SHOPS + """
GROUP BY 1
"""

# Done moves into (+) / out of (−) the shops, per product per day, from :s to today (shop↔shop moves cancel).
MOVES_SQL = """
SELECT pt."name" AS product, m.date::date AS d,
       SUM(CASE WHEN """ + _IN_SHOPS.replace("l.", "ld.") + """ AND NOT """ + _IN_SHOPS.replace("l.", "ls.") + """ THEN m.product_qty
                WHEN """ + _IN_SHOPS.replace("l.", "ls.") + """ AND NOT """ + _IN_SHOPS.replace("l.", "ld.") + """ THEN -m.product_qty
                ELSE 0 END) AS net
FROM stock_move m JOIN stock_location ls ON ls.id = m.location_id JOIN stock_location ld ON ld.id = m.location_dest_id
JOIN product_product pp ON pp.id = m.product_id JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE m.state = 'done' AND m.date::date >= :s
GROUP BY 1, 2
"""

DAILY_SOLD_SQL = """
SELECT pt."name" AS product, p.date_order::date AS d, SUM(pl.qty) AS q
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
JOIN product_product pp ON pp.id = pl.product_id JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE p.state IN ('done', 'invoiced', 'paid') AND pl.qty > 0 AND p.date_order::date BETWEEN :s AND :e
GROUP BY 1, 2
"""

TOTAL_SQL = """
SELECT SUM(target_qty) AS qty, SUM(target_amount) AS amt FROM sales_pos_target
WHERE period = 'month' AND start_date = :m AND target_scope IN ('pos', 'corporate')
"""


def bag_key_fn():
    """Product name → catalogue bag (colours folded); sleeves and not-yet-catalogued new products by name."""
    import self_made_combos as smc
    infer, _ = smc.bag_classifier(set())
    try:
        from lib import new_products_list
        new = sorted({str(n).upper().strip() for n in new_products_list.names()}, key=len, reverse=True)
    except Exception:                                        # noqa: BLE001
        new = ["LAFEMME"]

    def key(name):
        u = re.sub(r"^\[[^\]]*\]\s*", "", str(name).upper().strip())
        if "LAPTOP SLEEVE" in u:
            return "LAPTOP SLEEVE"
        k = infer(name)
        if k:
            return k
        return next((n for n in new if u == n or u.startswith(n + " ")), None)
    return key


def base_period(month_start):
    """The three complete months before month_start → (start, end)."""
    end = month_start - datetime.timedelta(days=1)
    s = end.replace(day=1)
    for _ in range(2):
        s = (s - datetime.timedelta(days=1)).replace(day=1)
    return s, end


def available_days(onhand_now, net_moves, sold_days, start, end, today):
    """Pure. {bag: set(dates in [start, end] the bag had stock in a shop or sold)}.
    onhand_now = {bag: units now}; net_moves = {bag: {date: net into shops}}; sold_days = {bag: set(dates)}.
    End-of-day stock is rebuilt backwards from today: end(d-1) = end(d) - net(d)."""
    out = {}
    for b in set(onhand_now) | set(net_moves) | set(sold_days):
        moves = net_moves.get(b, {})
        level = onhand_now.get(b, 0)               # end of `today`
        d = today
        days = set()
        while d >= start:
            prev = level - moves.get(d, 0)          # end of the day before = start of d
            if d <= end and (level > 0 or prev > 0 or d in sold_days.get(b, ())):
                days.add(d)
            level, d = prev, d - datetime.timedelta(days=1)
        out[b] = days
    return out


def allocate(sold, launch, total, start, end, months, min_days=MIN_DAYS, avail=None):
    """Pure split. sold = {bag: {YYYY-MM: units}}, launch = {bag: date of first sale}, avail = {bag: set(dates
    with stock)} (optional). Returns rows sorted by target: {bag, launch, days, months{}, sold, equiv, share,
    target} — no row with target 0."""
    period_days = (end - start).days + 1
    eq = {}
    meta = {}
    for b, by_m in sold.items():
        units = sum(by_m.values())
        if units <= 0:
            continue
        first = max(launch.get(b) or start, start)
        if avail is not None and b in avail:
            raw_days = sum(1 for d in avail[b] if d >= first)      # stocked days since launch
        else:
            raw_days = (end - first).days + 1
        days = min(max(raw_days, min_days), period_days)
        eq[b] = units / days * period_days
        meta[b] = (first if (launch.get(b) or start) > start else None, days, units, raw_days)
    s = sum(eq.values())
    if not s:
        return []
    raw = {b: total * v / s for b, v in eq.items()}
    tgt = {b: math.floor(v) for b, v in raw.items()}
    for b in sorted(raw, key=lambda b: -(raw[b] - tgt[b]))[:total - sum(tgt.values())]:
        tgt[b] += 1
    rows = [{"bag": b, "launch": meta[b][0], "days": meta[b][1], "rawDays": meta[b][3], "months": {m: int(round(sold[b].get(m, 0))) for m in months},
             "sold": int(round(meta[b][2])), "equiv": round(eq[b]), "share": round(eq[b] / s * 100, 2), "target": tgt[b]}
            for b in eq if tgt[b] > 0]
    return sorted(rows, key=lambda r: (-r["target"], r["bag"]))


def build(month_start=None):
    """(rows, total, base start, base end) for the month, from Odoo."""
    month_start = month_start or report_month.live_month_window()[0]
    start, end = base_period(month_start)
    key = bag_key_fn()
    params = {"s": start.isoformat(), "e": end.isoformat()}
    sold = collections.defaultdict(collections.Counter)
    for df in (db.run_query(POS_SALES_SQL, {**params, "excluded": queries.excluded_products()}),
               db.run_query(CORPORATE_SALES_SQL, params)):
        for r in (df.itertuples() if df is not None else []):
            k = key(r.product)
            if k:
                sold[k][str(r.m)[:7]] += float(r.bags)
    launch = {}
    fs = db.run_query(FIRST_SALE_SQL)
    for r in (fs.itertuples() if fs is not None else []):
        k = key(r.product)
        d = r.first_sale if isinstance(r.first_sale, datetime.date) else datetime.date.fromisoformat(str(r.first_sale)[:10])
        if k and (k not in launch or d < launch[k]):
            launch[k] = d
    # Days each bag had stock in a shop (or sold) — rebuilt from today's on-hand and the stock moves.
    today = datetime.date.today()
    onhand, net, sold_d = collections.Counter(), collections.defaultdict(collections.Counter), collections.defaultdict(set)
    q = db.run_query(ONHAND_SQL)
    for r in (q.itertuples() if q is not None else []):
        k = key(r.product)
        if k:
            onhand[k] += float(r.qty or 0)
    q = db.run_query(MOVES_SQL, {"s": start.isoformat()})
    for r in (q.itertuples() if q is not None else []):
        k = key(r.product)
        if k and r.net:
            net[k][r.d if isinstance(r.d, datetime.date) else datetime.date.fromisoformat(str(r.d)[:10])] += float(r.net)
    q = db.run_query(DAILY_SOLD_SQL, params)
    for r in (q.itertuples() if q is not None else []):
        k = key(r.product)
        if k:
            sold_d[k].add(r.d if isinstance(r.d, datetime.date) else datetime.date.fromisoformat(str(r.d)[:10]))
    avail = available_days(onhand, net, sold_d, start, end, today) if (onhand or net) else None
    t = db.run_query(TOTAL_SQL, {"m": month_start.isoformat()})
    total = int(round(float(t.qty[0]))) if t is not None and len(t) and t.qty[0] is not None else 0
    months = []
    m = start
    while m <= end:
        months.append(m.strftime("%Y-%m"))
        m = (m.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    return allocate(sold, launch, total, start, end, months, avail=avail), total, start, end, months


def write_csv(month_start=None, sheet_targets=None):
    rows, total, start, end, months = build(month_start)
    month_start = month_start or report_month.live_month_window()[0]
    path = os.path.join(BASE, "product_targets_%s.csv" % month_start.strftime("%Y-%m"))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Bag", "Launch (first sale)", "Days available"]
                   + [calendar.month_abbr[int(x[5:])] + " sold" for x in months]
                   + ["Period sold", "Full-period equivalent", "Share %", "Target (units)", "Sheet target (col C)"])
        for r in rows:
            w.writerow([r["bag"], r["launch"].isoformat() if r["launch"] else "", r["days"]]
                       + [r["months"][x] for x in months]
                       + [r["sold"], r["equiv"], r["share"], r["target"], (sheet_targets or {}).get(r["bag"], "")])
    return path, rows, total


def load_targets(month_start=None, build_if_missing=True):
    """{BAG: target units} for the month from product_targets_<YYYY-MM>.csv (built from Odoo if missing),
    or {} when it can't be had."""
    month_start = month_start or report_month.live_month_window()[0]
    path = os.path.join(BASE, "product_targets_%s.csv" % month_start.strftime("%Y-%m"))
    if not os.path.exists(path) and build_if_missing:
        try:
            write_csv(month_start, sheet_targets=_sheet_targets())
        except Exception as e:                               # noqa: BLE001
            print(f"  Bag targets: could not build {os.path.basename(path)} ({e})")
    try:
        with open(path, encoding="utf-8", newline="") as f:
            rd = csv.DictReader(f)
            col = next(c for c in rd.fieldnames if c.startswith("Target"))
            return {r["Bag"].strip().upper(): int(float(r[col] or 0)) for r in rd if r.get("Bag")}
    except (OSError, StopIteration, ValueError):
        return {}


def monthly_target_rows(rows, month_start=None, targets=None, key=None):
    """MONTHLY_TARGET rows with column C = the bag's target from Odoo (docs/product-targets.md) and
    column E = max(C − D, 0); unmatched target bags appended; every other column kept. Sheet rows are
    returned unchanged (with a warning) if no targets can be had."""
    targets = load_targets(month_start) if targets is None else targets
    if not targets or not rows:
        if rows:
            print("  Bag targets unavailable — MONTHLY_TARGET column C used as is.")
        return rows
    key = key or bag_key_fn()

    def num(v):
        try:
            return int(float(str(v).replace(",", "") or 0))
        except (ValueError, TypeError):
            return 0
    out, used = [list(rows[0])], set()
    width = max(len(r) for r in rows)
    for r in rows[1:]:
        r = list(r) + [""] * (width - len(r))
        name = str(r[0]).strip()
        if name and "TOTAL" not in name.upper():
            k = (key(name) or name).upper()
            k = k if k in targets else name.upper()
            t = targets.get(k, 0) if k not in used else 0
            used.add(k)
            r[2] = t
            r[4] = max(t - num(r[3]), 0)
        out.append(r)
    for b, t in sorted(targets.items(), key=lambda kv: -kv[1]):
        if b not in used and t > 0:
            row = [b, "", t, 0, t] + [""] * max(width - 5, 0)
            out.append(row)
    print(f"  Bag targets: {sum(targets.values()):,} units over {len(targets)} bags (product_targets, not sheet col C)")
    return out


def _sheet_targets():
    """{BAG: col C} from MONTHLY_TARGET — for the comparison column only."""
    try:
        from google_auth import get_gspread_client
        mt = get_gspread_client().open_by_key("1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0").worksheet("MONTHLY_TARGET").get_all_values()
        return {re.sub(r"\s+", " ", r[0].strip().upper()): r[2] for r in mt[1:] if r and r[0].strip() and len(r) > 2}
    except Exception:                                        # noqa: BLE001
        return {}


if __name__ == "__main__":
    p, rows, total = write_csv(sheet_targets=_sheet_targets())
    print(f"{p}: {len(rows)} bags, {sum(r['target'] for r in rows)} of {total} units")
