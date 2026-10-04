"""Tests for lib/oos_callbacks.py (WhatsApp "Out of stock — call back" demand). Run:
    python -m pytest tests/test_oos_callbacks.py -q
The reconciliation tests read live Odoo and are skipped when it is unreachable.
"""
import datetime
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import db, oos_callbacks as oc   # noqa: E402

TOP_BAG = "Mini Maya Wooven Black"


def _base_sql():
    with open(oc._SQL_PATH, encoding="utf-8") as f:
        return f.read().strip().rstrip(";")


@pytest.fixture(scope="module")
def live():
    if not db.check_connection()[0]:
        pytest.skip("Odoo unreachable")
    return oc.oos_by_bag_shop()


# ── reconciliation against raw SQL ───────────────────────────
def test_lifetime_total_matches_raw_sql(live):
    got = sum(n for shops in live["lifetime"].values() for n in shops.values())
    raw = db.run_query(f"SELECT COUNT(*) AS n FROM (SELECT DISTINCT person, product, shop FROM ({_base_sql()}) q) x")
    assert got == int(raw.n[0])


def test_top_bag_per_shop_matches_raw_sql(live):
    raw = db.run_query(f"SELECT shop, COUNT(DISTINCT person) AS n FROM ({_base_sql()}) q "
                       "WHERE product = :p GROUP BY shop", {"p": TOP_BAG})
    assert live["lifetime"][TOP_BAG] == {r.shop: int(r.n) for r in raw.itertuples()}


def test_current_and_periods_never_exceed_lifetime(live):
    for p in ("current", "monthly", "weekly", "lastweek"):
        for bag, shops in live[p].items():
            for shop, n in shops.items():
                assert n <= live["lifetime"][bag][shop], (p, bag, shop)


# ── pure logic ───────────────────────────────────────────────
D = datetime.date(2026, 9, 15)
ROWS = [
    {"date": D, "shop": "Hilton", "kind": "shop", "person": "a", "purchased": False, "product": "Kai Black"},
    {"date": D, "shop": "Hilton", "kind": "shop", "person": "a", "purchased": False, "product": "Kai Brown"},
    {"date": D, "shop": "Thika",  "kind": "shop", "person": "a", "purchased": True,  "product": "Kai Black"},
    {"date": D, "shop": "Thika",  "kind": "shop", "person": "b", "purchased": False, "product": "Kai Black"},
    {"date": D, "shop": "Uganda", "kind": "region", "person": "c", "purchased": False, "product": "Kai Black"},
    {"date": D, "shop": "Thika",  "kind": "shop", "person": "d", "purchased": False, "product": "DRAWER REPAIR"},
]


def _kai(name):
    return "KAI" if name.upper().startswith("KAI ") else None


def test_rekey_unions_people_not_counts():
    b = oc.aggregate(ROWS, key_fn=_kai, today=datetime.date(2026, 9, 20))["lifetime"]
    assert set(b) == {"KAI"}                                  # DRAWER REPAIR dropped
    assert dict(map(tuple, b["KAI"]["shops"])) == {"Hilton": 1, "Thika": 2, "Uganda": 1}
    assert b["KAI"]["total"] == 3                             # a counted once across shades + shops


def test_totals_never_exceed_sum_of_shops():
    blk = oc.aggregate(ROWS, key_fn=_kai, today=datetime.date(2026, 9, 20))
    for p, bags in blk.items():
        for k, v in bags.items():
            assert v["total"] <= sum(n for _, n in v["shops"])


def test_current_skips_purchased_and_shop_filter_scopes():
    b = oc.aggregate(ROWS, key_fn=_kai, shop_filter=lambda r: r["kind"] == "shop",
                     today=datetime.date(2026, 9, 20))["current"]
    assert dict(map(tuple, b["KAI"]["shops"])) == {"Hilton": 1, "Thika": 1}


def test_shops_sorted_high_to_low():
    shops = oc.aggregate(ROWS, key_fn=_kai, today=datetime.date(2026, 9, 20))["lifetime"]["KAI"]["shops"]
    assert [n for _, n in shops] == sorted((n for _, n in shops), reverse=True)


def test_colours_break_down_each_bag():
    col = lambda n: n.split()[-1]
    b = oc.aggregate(ROWS, key_fn=_kai, colour_fn=col, today=datetime.date(2026, 9, 20))["lifetime"]["KAI"]
    cols = {c: (n, dict(map(tuple, shops))) for c, n, shops in b["colours"]}
    assert cols == {"Black": (3, {"Hilton": 1, "Thika": 2, "Uganda": 1}), "Brown": (1, {"Hilton": 1})}
    assert b["total"] == 3 and dict(map(tuple, b["shops"]))["Hilton"] == 1   # shades merged per shop


def test_attach_stock_per_shop_and_colour():
    col = lambda n: n.split()[-1].title()
    blk = oc.aggregate(ROWS, key_fn=_kai, colour_fn=col, today=datetime.date(2026, 9, 20))
    stock = {"HTN": {"KAI BLACK": 4, "KAI BROWN": 0}, "THK": {"KAI BROWN": 2}}
    oc.attach_stock(blk, _kai, col, stock_by_code=stock)
    e = blk["lifetime"]["KAI"]
    assert {s: st for s, _, st in e["shops"]} == {"Hilton": 4, "Thika": 2, "Uganda": None}
    black = {s: st for s, _, st in next(c for c in e["colours"] if c[0] == "Black")[2]}
    assert black == {"Hilton": 4, "Thika": 0, "Uganda": None}     # Thika holds Brown only


# ── offline ──────────────────────────────────────────────────
@pytest.mark.parametrize("fail", ["raise", "none"])
def test_offline_returns_empty(monkeypatch, fail):
    def broken(*a, **k):
        if fail == "raise":
            raise RuntimeError("db down")
        return None
    monkeypatch.setattr(db, "run_query", broken)
    monkeypatch.setattr(db, "run_query_cached", broken)
    assert oc.oos_by_bag_shop() == {}
    assert oc.aggregate(oc.load_rows()) == {}
