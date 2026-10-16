"""scripts/estimated_targets.py — what the monthly bag target WOULD have been, by the dashboard's own method,
for every month back to the start of Odoo POS history — set against the Odoo target and what was sold.
(User, 16 Oct 2026: "estimated targets from the way I calculated my target … back date as far as possible
and factor in the growth rate". Spec: docs/product-targets.md › Estimated targets.)

Per month M:
  base     = lib/product_targets' base — each bag's sales over the 3 complete months before M (all tills +
             Corporate invoices), scaled to the days it was launched and in stock (≥ 14), summed ÷ 3
             → the availability-adjusted monthly rate going into M.
  growth   = monthly growth rate: (those 3 months' bags ÷ the 3 months before them) ^ (1/3) − 1.
  estimate = base × (1 + growth).
  odoo     = the month's Odoo target (shop tills + Corporate, `sales_pos_target`, period 'month'), if set.
  sold     = bags sold in M, same counting rules.

    python scripts/estimated_targets.py      # → data/estimated_targets.csv + a printed table
"""
import calendar
import collections
import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import db, paths, queries, product_targets as pt   # noqa: E402


def _d(v):
    return v if isinstance(v, datetime.date) else datetime.date.fromisoformat(str(v)[:10])


def _add_months(m, n):
    y, mo = divmod(m.year * 12 + m.month - 1 + n, 12)
    return datetime.date(y, mo + 1, 1)


def main():
    today = datetime.date.today()
    first = _d(db.run_query("SELECT MIN(date_order)::date AS d FROM pos_order "
                            "WHERE state IN ('done','invoiced','paid') AND date_order >= '2023-12-01'").d[0]).replace(day=1)
    live = today.replace(day=1)
    key = pt.bag_key_fn()
    p = {"s": first.isoformat(), "e": today.isoformat()}

    sold = collections.defaultdict(collections.Counter)            # bag -> {YYYY-MM: units}
    for df in (db.run_query(pt.POS_SALES_SQL, {**p, "excluded": queries.excluded_products()}),
               db.run_query(pt.CORPORATE_SALES_SQL, p)):
        for r in (df.itertuples() if df is not None else []):
            k = key(r.product)
            if k:
                sold[k][str(r.m)[:7]] += float(r.bags)
    launch = {}
    for r in db.run_query(pt.FIRST_SALE_SQL).itertuples():
        k = key(r.product)
        if k and (k not in launch or _d(r.first_sale) < launch[k]):
            launch[k] = _d(r.first_sale)
    onhand, net, sold_d = collections.Counter(), collections.defaultdict(collections.Counter), collections.defaultdict(set)
    for r in db.run_query(pt.ONHAND_SQL).itertuples():
        k = key(r.product)
        if k:
            onhand[k] += float(r.qty or 0)
    for r in db.run_query(pt.MOVES_SQL, {"s": first.isoformat()}).itertuples():
        k = key(r.product)
        if k and r.net:
            net[k][_d(r.d)] += float(r.net)
    for r in db.run_query(pt.DAILY_SOLD_SQL, p).itertuples():
        k = key(r.product)
        if k:
            sold_d[k].add(_d(r.d))
    odoo = {}
    for r in db.run_query("""SELECT start_date AS m, target_scope AS sc, SUM(target_qty) AS q, COUNT(*) AS n
                             FROM sales_pos_target WHERE period = 'month' GROUP BY 1, 2""").itertuples():
        o = odoo.setdefault(_d(r.m).strftime("%Y-%m"), {"pos": 0, "corporate": 0, "tills": 0})
        o[r.sc] = int(round(float(r.q or 0)))
        if r.sc == "pos":
            o["tills"] = int(r.n)

    month_sold = collections.Counter()
    for by in sold.values():
        for m, v in by.items():
            month_sold[m] += v

    out = []
    m = _add_months(first, 6)                                       # needs 3 base + 3 earlier months
    while m <= _add_months(live, 1):                                # through next month (a forecast)
        s, e = pt.base_period(m)
        months = [_add_months(s, i).strftime("%Y-%m") for i in range(3)]
        prev = [_add_months(s, i - 3).strftime("%Y-%m") for i in range(3)]
        base_sold = {b: collections.Counter({x: by.get(x, 0) for x in months}) for b, by in sold.items()}
        avail = pt.available_days(onhand, net, sold_d, s, e, today)
        rows = pt.allocate(base_sold, launch, 10 ** 7, s, e, months, avail=avail)   # big total: keep every bag
        base = sum(r["equiv"] for r in rows) / 3
        b3, p3 = sum(month_sold[x] for x in months), sum(month_sold[x] for x in prev)
        growth = (b3 / p3) ** (1 / 3) - 1 if p3 else 0.0
        est = round(base * (1 + growth))
        k = m.strftime("%Y-%m")
        o = odoo.get(k)
        o_tot = (o["pos"] + o["corporate"]) if o else None
        act = round(month_sold[k]) if m < live else None
        out.append({"month": k, "base": round(base), "growth_pct": round(growth * 100, 2), "estimate": est,
                    "odoo_target": o_tot, "odoo_tills": o["tills"] if o else None,
                    "est_vs_odoo_pct": round(est / o_tot * 100, 1) if o_tot else None,
                    "sold": act, "sold_vs_est_pct": round(act / est * 100, 1) if act and est else None,
                    "sold_vs_odoo_pct": round(act / o_tot * 100, 1) if act and o_tot else None,
                    "partial": m == live})
        m = _add_months(m, 1)

    path = paths.data("estimated_targets.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f"{'Month':8} {'Base':>7} {'Growth':>7} {'Estimate':>9} {'Odoo':>7} {'Est/Odoo':>9} {'Sold':>7} {'Sold/Est':>9} {'Sold/Odoo':>9}")
    for r in out:
        f = lambda v, sfx="": "" if v is None else f"{v:,}{sfx}"
        print(f"{r['month']:8} {r['base']:>7,} {r['growth_pct']:>6}% {r['estimate']:>9,} {f(r['odoo_target']):>7} "
              f"{f(r['est_vs_odoo_pct'], '%'):>9} {f(r['sold']):>7} {f(r['sold_vs_est_pct'], '%'):>9} {f(r['sold_vs_odoo_pct'], '%'):>9}"
              + ("  (month so far)" if r["partial"] else "") + (f"  ({r['odoo_tills']} tills)" if r["odoo_tills"] and r["odoo_tills"] < 15 else ""))
    print("→", path)


if __name__ == "__main__":
    main()
