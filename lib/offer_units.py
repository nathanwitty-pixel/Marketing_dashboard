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

# One row per (receipt, combo product, bag): the combo lines summed per order + product (two lines of one combo =
# qty 2; a return is its own order with negative qty, POS_LINES gives it bags), the sub-lines summed per order +
# parent + bag — as generators/bags_on_offer.py COMBO_LINES_SQL (20 Nov 2026: the old line × sub-line join
# cross-joined two lines of one combo and counted refunded combos).
COMBO_LINES_SQL = """
WITH c AS (
    SELECT pl.order_id, pl.product_id, SUM(pl.qty) AS combo_qty
    FROM pos_order p JOIN POS_LINES(p) pl ON pl.order_id = p.id
    JOIN pos_session ps ON ps.id = p.session_id
    JOIN pos_config pc ON pc.id = ps.config_id
    JOIN product_product wp ON wp.id = pl.product_id
    JOIN product_template wt ON wt.id = wp.product_tmpl_id
    WHERE p.date_order::date BETWEEN :s AND :e
      AND p.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0
      AND NOT COALESCE(pl.sub_product_line, false) AND wt."name" LIKE '%%+%%'
      AND lower(pc."name") NOT IN ('sinza', 'dar-es-alam', 'uganda')
    GROUP BY 1, 2
), s AS (
    SELECT sl.order_id, sl.parent_id, pt."name" AS product, SUM(sl.qty) AS qty
    FROM (SELECT DISTINCT order_id FROM c) co JOIN pos_order po ON po.id = co.order_id
    JOIN POS_LINES(po) sl ON sl.order_id = po.id
    JOIN c ON c.order_id = sl.order_id AND c.product_id = sl.parent_id
    JOIN product_product pp ON pp.id = sl.product_id
    JOIN product_template pt ON pt.id = pp.product_tmpl_id
    WHERE COALESCE(sl.sub_product_line, false)
    GROUP BY 1, 2, 3
)
SELECT c.order_id AS receipt, c.product_id AS combo, c.combo_qty, s.product, s.qty
FROM c JOIN s ON s.order_id = c.order_id AND s.parent_id = c.product_id
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
        groups = collections.defaultdict(lambda: {"qty": 0, "bags": collections.Counter()})
        for r in (df.itertuples(index=False) if df is not None else []):
            g = groups[(r.receipt, r.combo)]
            g["qty"] = int(round(float(r.combo_qty or 0)))
            b = key(r.product)
            if b:
                g["bags"][b] += int(round(float(r.qty or 0)))
        for g in groups.values():
            n = g["qty"]                                     # < 0 = a return: its bags are negative too
            if n == 0:
                continue
            if all(c % n == 0 and c // n >= 0 for c in g["bags"].values()):
                per = [b for b, c in g["bags"].items() for _ in range(c // n)]       # one combo's bags
            else:
                per = [b for b, c in g["bags"].items() for _ in range(abs(c))]
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
