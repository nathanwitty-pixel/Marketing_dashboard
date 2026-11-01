"""lib/offer_units.py — units moved per listed offer for a month, from Odoo (docs/monthly-report.md › Offer units).

From Oct 2026 the offer lists come from the monthly uploads (offers_monthly.csv, deals_kenya.csv), which carry
names and prices but no units — the old COMBOS sheet's weekly columns are gone. This counts them from the tills:

  Kenya combos   combo sales (a '+' product with its bag sub-lines) whose bags fill a listed combo's slots
                 (same count, any order, alternatives — receipt_combos._fits); 1 combo = 1 unit.
  Power Deals    single bags of the deal's bag type sold at the Kenya tills (combo sub-lines left out).
  Sinza / Uganda receipt_combos.market_summary: listed combos found on receipts and listed singles sold.

units(month_start, month_end) → {"kenya": {offer name: units}, "power": {product: units},
                                 "sinza": {offer name: units}, "uganda": {offer name: units}}
"""
from __future__ import annotations

import collections
import csv

from lib import db, paths, receipt_combos

COMBO_LINES_SQL = """
SELECT p.id AS receipt, w.product_id AS combo, w.qty AS combo_qty, pt."name" AS product, s.qty AS qty
FROM pos_order p
JOIN pos_session ps ON ps.id = p.session_id
JOIN pos_config pc ON pc.id = ps.config_id
JOIN pos_order_line w ON w.order_id = p.id
JOIN product_product wp ON wp.id = w.product_id
JOIN product_template wt ON wt.id = wp.product_tmpl_id
JOIN pos_order_line s ON s.order_id = p.id AND s.parent_id = w.product_id AND COALESCE(s.sub_product_line, false)
JOIN product_product pp ON pp.id = s.product_id
JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE p.date_order::date BETWEEN :s AND :e
  AND p.state IN ('done', 'invoiced', 'paid')
  AND w.qty > 0 AND wt."name" LIKE '%%+%%'
  AND lower(pc."name") NOT IN ('sinza', 'dar-es-alam', 'uganda')
"""

SINGLES_SQL = """
SELECT pt."name" AS product, SUM(pl.qty) AS units
FROM pos_order p JOIN POS_LINES(p) pl ON pl.order_id = p.id
JOIN pos_session ps ON ps.id = p.session_id
JOIN pos_config pc ON pc.id = ps.config_id
JOIN product_product pp ON pp.id = pl.product_id
JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE p.date_order::date BETWEEN :s AND :e
  AND p.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0
  AND NOT COALESCE(pl.sub_product_line, false) AND pt."name" NOT LIKE '%%+%%'
  AND lower(pc."name") NOT IN ('sinza', 'dar-es-alam', 'uganda')
GROUP BY 1
"""


def _infer():
    import sys
    if paths.GENERATORS not in sys.path:
        sys.path.insert(0, paths.GENERATORS)
    import self_made_combos as smc
    return smc.bag_classifier(set())[0]


def _power_products(month_name):
    try:
        with open(paths.data("deals_kenya.csv"), encoding="utf-8", newline="") as f:
            return [r["Product"].strip() for r in csv.DictReader(f)
                    if r["Month"].strip().lower() == month_name.lower() and r["Type"].strip().lower().startswith("power")]
    except OSError:
        return []


def units(month_start, month_end):
    month = month_start.strftime("%B")
    infer = _infer()
    key = lambda n: receipt_combos.bag_key(n, infer)       # noqa: E731
    p = {"s": month_start.isoformat(), "e": month_end.isoformat()}
    out = {"kenya": {}, "power": {}, "sinza": {}, "uganda": {}}

    # Kenya combos: each combo sale's bags against the listed combos
    ke = (receipt_combos.load_offers(month, "kenya") or {}).get("combos", [])
    if ke:
        df = db.run_query(COMBO_LINES_SQL, p)
        groups = collections.defaultdict(lambda: {"qty": 1, "bags": []})
        for r in (df.itertuples(index=False) if df is not None else []):
            g = groups[(r.receipt, r.combo)]
            g["qty"] = max(int(r.combo_qty or 1), 1)
            b = key(r.product)
            if b:
                g["bags"] += [b] * max(int(round(float(r.qty or 0))), 0)
        for g in groups.values():
            n = g["qty"]
            per = g["bags"][:len(g["bags"]) // n] if n > 1 and len(g["bags"]) % n == 0 else g["bags"]
            hit = next((o["name"] for o in ke if receipt_combos._fits(per, o["slots"])), None)
            if hit:
                out["kenya"][hit] = out["kenya"].get(hit, 0) + n

    # Power Deals: single bags of the deal's type
    deals = _power_products(month)
    if deals:
        df = db.run_query(SINGLES_SQL, p)
        by_bag = collections.Counter()
        for r in (df.itertuples(index=False) if df is not None else []):
            b = key(r.product)
            if b:
                by_bag[b] += float(r.units or 0)
        for d in deals:
            k = key(d)
            out["power"][d] = int(round(by_bag.get(k, 0))) if k else 0

    # Sinza / Uganda: receipts
    for mkt in ("sinza", "uganda"):
        s = receipt_combos.market_summary(mkt, month_start, month_end, infer, month_name=month) or {}
        for tbl in ("running", "singlesOffer"):
            for name, v in (s.get(tbl) or {}).items():
                out[mkt][name] = out[mkt].get(name, 0) + int(v.get("count", 0))
    return out
