"""Tests for stockout_demand.py — python -m pytest scripts -q"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import stockout_demand as sd   # noqa: E402

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
    b = sd.aggregate(ROWS, key_fn=_kai, today=datetime.date(2026, 9, 20))["lifetime"]
    assert set(b) == {"KAI"}                                  # DRAWER REPAIR dropped
    assert dict(map(tuple, b["KAI"]["shops"])) == {"Hilton": 1, "Thika": 2, "Uganda": 1}
    assert b["KAI"]["total"] == 3                             # a counted once across shades + shops


def test_totals_never_exceed_sum_of_shops():
    blk = sd.aggregate(ROWS, key_fn=_kai, today=datetime.date(2026, 9, 20))
    for p, bags in blk.items():
        for k, v in bags.items():
            assert v["total"] <= sum(n for _, n in v["shops"])


def test_current_skips_purchased_and_shop_filter_scopes():
    b = sd.aggregate(ROWS, key_fn=_kai, shop_filter=lambda r: r["kind"] == "shop",
                     today=datetime.date(2026, 9, 20))["current"]
    assert dict(map(tuple, b["KAI"]["shops"])) == {"Hilton": 1, "Thika": 1}


def test_shops_sorted_high_to_low():
    shops = sd.aggregate(ROWS, key_fn=_kai, today=datetime.date(2026, 9, 20))["lifetime"]["KAI"]["shops"]
    assert [n for _, n in shops] == sorted((n for _, n in shops), reverse=True)


def test_colours_break_down_each_bag():
    col = lambda n: n.split()[-1]
    b = sd.aggregate(ROWS, key_fn=_kai, colour_fn=col, today=datetime.date(2026, 9, 20))["lifetime"]["KAI"]
    cols = {c: (n, dict(map(tuple, shops))) for c, n, shops in b["colours"]}
    assert cols == {"Black": (3, {"Hilton": 1, "Thika": 2, "Uganda": 1}), "Brown": (1, {"Hilton": 1})}
    assert b["total"] == 3 and dict(map(tuple, b["shops"]))["Hilton"] == 1   # shades merged per shop


def test_attach_stock_per_shop_and_colour():
    col = lambda n: n.split()[-1].title()
    blk = sd.aggregate(ROWS, key_fn=_kai, colour_fn=col, today=datetime.date(2026, 9, 20))
    stock = {"HTN": {"KAI BLACK": 4, "KAI BROWN": 0}, "THK": {"KAI BROWN": 2}}
    sd.attach_stock(blk, _kai, col, {'Hilton': stock['HTN'], 'Thika': stock['THK']})
    e = blk["lifetime"]["KAI"]
    assert {s: st for s, _, st in e["shops"]} == {"Hilton": 4, "Thika": 2, "Uganda": None}
    black = {s: st for s, _, st in next(c for c in e["colours"] if c[0] == "Black")[2]}
    assert black == {"Hilton": 4, "Thika": 0, "Uganda": None}     # Thika holds Brown only


