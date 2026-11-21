"""Fix batch C (Nov 2026): SQL rules run on fake rows in DuckDB (no Odoo needed) plus small source checks.
    python -m pytest tests/test_fixC_sql.py -q
"""
import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

duckdb = pytest.importorskip("duckdb")


def _read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8-sig") as f:
        return f.read()


def _bind(sql, s, e):
    return sql.replace(":start_date", "DATE '%s'" % s).replace(":end_date", "DATE '%s'" % e)


def _corp_db():
    con = duckdb.connect()
    con.execute("CREATE TABLE denri_corporate_invoice(id INT, date_invoice DATE, amount_total DOUBLE, "
                "wht_amount DOUBLE, status VARCHAR, company VARCHAR)")
    con.execute("CREATE TABLE denri_corporate_invoice_line(invoice_id INT, qty DOUBLE, product VARCHAR)")
    con.execute("CREATE TABLE denri_corporate_payment(invoice_id INT, date DATE, amount DOUBLE)")
    con.execute("INSERT INTO denri_corporate_invoice VALUES (1, '2026-10-01', 11000, 0, 'paid', 'Acme')")
    con.execute("INSERT INTO denri_corporate_invoice_line VALUES (1, 11, 'Bag A')")
    con.execute("INSERT INTO denri_corporate_payment VALUES (1, '2026-10-05', 5500), (1, '2026-11-05', 5500)")
    return con


OCT, NOV = ("2026-10-01", "2026-10-31"), ("2026-11-01", "2026-11-30")


def test_corporate_bags_instalments_add_up_to_whole_invoice():
    con, sql = _corp_db(), _read("sql", "corporate_bags.sql")
    octo = con.execute(_bind(sql, *OCT)).fetchone()
    nov = con.execute(_bind(sql, *NOV)).fetchone()
    assert (octo[0], octo[1], octo[3]) == (1, 5, 5500)     # invoices, bags, kes
    assert (nov[0], nov[1], nov[3]) == (1, 6, 5500)        # 5 + 6 = 11, not 5 + 5


def test_corporate_clients_sold_matches_corporate_bags():
    con, sql = _corp_db(), _read("sql", "corporate_clients.sql")
    head = sql.split(",\nquote_rows AS (")[0]               # inv / inv_pay / inv_rows only (the rest is Postgres regex)
    assert head != sql
    q = head + "\nSELECT SUM(sold) FROM inv_rows"
    assert con.execute(_bind(q, *OCT)).fetchone()[0] == 5
    assert con.execute(_bind(q, *NOV)).fetchone()[0] == 6


def _dist_db():
    con = duckdb.connect()
    for ddl in ("CREATE TABLE stock_move(id INT, state VARCHAR, product_qty DOUBLE, date TIMESTAMP, "
                "location_id INT, location_dest_id INT, product_id INT)",
                "CREATE TABLE stock_location(id INT, complete_name VARCHAR, name VARCHAR, usage VARCHAR)",
                "CREATE TABLE product_product(id INT, product_tmpl_id INT)",
                "CREATE TABLE product_template(id INT, name VARCHAR)",
                "CREATE TABLE denri_dispatch_transit_line(id INT, transit_id INT, product_id INT, qty_dispatched DOUBLE)",
                "CREATE TABLE denri_dispatch_transit(id INT, dispatch_date TIMESTAMP, shop_id INT)",
                "CREATE TABLE denri_dispatch_shop(id INT, name VARCHAR)"):
        con.execute(ddl)
    con.execute("INSERT INTO stock_location VALUES (1,'FINWH/Stock','Stock','internal'),"
                "(2,'FINWH/Goods in Transit/MOMBASA','MOMBASA','transit'),(3,'MSA/Stock','Stock','internal'),"
                "(4,'FINWH/Goods in Transit/STARMALL','STARMALL','transit')")
    con.execute("INSERT INTO product_product VALUES (10, 10)")
    con.execute("INSERT INTO product_template VALUES (10, 'ALPHA Tote')")
    # Mombasa: two real identical receipts the same day. Starmall: 4, 4 and 7 sent, each seen in BOTH
    # stock_move and the dispatch app.
    con.execute("INSERT INTO stock_move VALUES (1,'done',5,'2026-11-18 08:00',2,3,10),(2,'done',5,'2026-11-18 09:00',2,3,10),"
                "(3,'done',4,'2026-11-18 08:00',1,4,10),(4,'done',4,'2026-11-18 09:00',1,4,10),"
                "(5,'done',7,'2026-11-18 10:00',1,4,10)")
    con.execute("INSERT INTO denri_dispatch_shop VALUES (1, 'STARMALL')")
    con.execute("INSERT INTO denri_dispatch_transit VALUES (1, '2026-11-18 08:00', 1)")
    con.execute("INSERT INTO denri_dispatch_transit_line VALUES (1,1,10,4),(2,1,10,4),(3,1,10,7)")
    return con


def test_combined_distribution_keeps_identical_moves_but_collapses_two_sources():
    con = _dist_db()
    sql = _read("sql", "combined_distribution.sql").replace(":start_date", "'2026-11-16'").replace(":end_date", "'2026-11-22'")
    df = con.execute(sql).df()
    gt = df[df["sort_order"] == 2].iloc[0]
    assert gt["MOMBASA"] == 10      # 5 + 5, was 5
    assert gt["STARMALL"] == 15     # 4 + 4 + 7 once each (stock_move and dispatch app are one dispatch), was 11


def test_shop_bags_sold_nets_refunds_on_nairobi_days():
    sql = _read("sql", "shop_bags_sold.sql")
    assert re.search(r"AND pl\.qty <> 0", sql) and "pl.qty > 0" not in sql
    assert "(p.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::date BETWEEN" in sql


def test_nyeri_is_a_kenya_shop_code():
    from lib import odoo_tabs, stock
    assert "NYERI" in stock.KENYA_SHOP_CODES
    assert odoo_tabs.STOCK_CODE_TO_SHOP["NYERI"] == "NYERI"
    assert '"RONG", "NYERI", "DAR"' in _read("generators", "product_performance.py")


def test_new_products_injection_is_literal_and_escaped():
    src = _read("generators", "new_products.py")
    assert "lambda _m: inline_script" in src
    assert '.replace("</", "<\\\\/")' in src
    # what the lambda form protects against: a plain replacement string turns \\n into a real newline
    js = 'const NP = {"a":"x\\ny"};'
    assert re.sub("X", js, "X") != js
    assert re.sub("X", lambda _m: js, "X") == js
