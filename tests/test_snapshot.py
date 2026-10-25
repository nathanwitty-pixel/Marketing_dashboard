"""lib/snapshot.py must give the same answers as live Postgres (docs/README.md › DuckDB till snapshot).
Runs each query both ways over a fixed past window and compares. Needs Postgres; skipped when it's down. Run:
    python -m pytest tests/test_snapshot.py -q
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import db, queries, snapshot   # noqa: E402

S, E = "2026-09-01", "2026-09-30"        # a closed month inside the snapshot window

_FROM = """
FROM pos_order p
JOIN POS_LINES(p) pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
WHERE p.date_order::date BETWEEN CAST(:s AS date) AND CAST(:e AS date)
  AND p.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0
  AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
  AND COALESCE(pt."name",'') NOT LIKE '%+%'
  AND COALESCE(pt."name",'') NOT ILIKE '%delivery%'
  AND COALESCE(pcat."name",'') NOT ILIKE '%Pos%'
"""

# The shapes Timed offers uses: per product, per day for named bags, Nairobi time-of-day band, price band, bulk lines.
CASES = {
    "by_product": ('SELECT pt."name" AS product, SUM(pl.qty)::int AS bags, SUM(pl.price_subtotal_incl)::numeric AS val'
                   + _FROM + 'GROUP BY pt."name"', {"s": S, "e": E}),
    "daily_named": ("SELECT p.date_order::date AS d, SUM(pl.qty)::int AS bags" + _FROM
                    + ' AND (pt."name" ILIKE :bag0 OR pt."name" ILIKE :bag1) GROUP BY 1 ORDER BY 1',
                    {"s": S, "e": E, "bag0": "Jumbo%", "bag1": "Sarai%"}),
    "evening_band": ('SELECT pt."name" AS product, SUM(pl.qty)::int AS bags' + _FROM
                     + " AND (p.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::time >= TIME '16:00'"
                     + " AND (p.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::time < TIME '19:00'"
                     + ' GROUP BY pt."name"', {"s": S, "e": E}),
    "price_band": ('SELECT pt."name" AS product, SUM(pl.qty)::int AS bags' + _FROM
                   + " AND pl.price_unit <= 1600 GROUP BY pt.\"name\"", {"s": S, "e": E}),
    "bulk_lines": ('SELECT p.date_order::date AS d, p."name" AS ord, COALESCE(pc."name",\'\') AS till, pt."name" AS product, '
                   'SUM(pl.qty)::int AS qty' + _FROM + " AND pl.qty >= :bulk GROUP BY 1, 2, 3, 4",
                   {"s": S, "e": E, "bulk": 10}),
}


def _norm(df):
    df = df.copy()
    for c in df.columns:
        if c == "d":
            df[c] = df[c].astype(str)            # as pages use it (str(r["d"]) keys) — must read 2026-09-01, not a timestamp
        elif df[c].dtype == object and df[c].map(lambda v: hasattr(v, "as_tuple")).any():
            df[c] = df[c].astype(float)                      # Decimal (Postgres) vs float (DuckDB)
        elif pd.api.types.is_numeric_dtype(df[c]):
            df[c] = df[c].astype(float)
    return df.sort_values(list(df.columns)).reset_index(drop=True)


def _live_up():
    ok, _ = db.check_connection()
    return ok


def test_snapshot_matches_live():
    if not _live_up():
        print("Postgres unreachable — skipped")
        return
    for name, (sql, params) in CASES.items():
        live = db.run_query(sql, params)
        snap = snapshot.query(sql, params)
        assert snap is not None, f"{name}: snapshot couldn't answer"
        pd.testing.assert_frame_equal(_norm(live), _norm(snap), check_exact=False, atol=0.01, obj=name)


def test_falls_back_outside_window():
    meta = snapshot.fresh_meta()
    if meta is None:
        return
    assert snapshot.query(CASES["by_product"][0], {"s": "2020-01-01", "e": E}) is None   # before the window
    assert snapshot.query("SELECT 1 FROM stock_move m", {}) is None                       # a table it doesn't hold
