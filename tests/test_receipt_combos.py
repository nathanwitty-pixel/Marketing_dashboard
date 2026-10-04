"""Tests for lib/receipt_combos.py (Sinza & Uganda combos from receipts). Run:
    python -m pytest tests/test_receipt_combos.py -q
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import receipt_combos as rc   # noqa: E402

M = datetime.date(2026, 10, 1)          # Thu → Wk 1 = Sun 27 Sep – Sat 3 Oct
OFFERS = {"combos": [{"name": "GYMBAG + ARI SLING", "slots": [{"GYM BAG"}, {"ARIA SLING"}]},
                     {"name": "SAFIRI + CODE 3", "slots": [{"SAFIRI TRAVEL", "SAFIRI BP"}, {"CODE 3"}]}],
          "singles": [{"name": "BONITA", "slots": [{"BONITA"}]}, {"name": "SLEEVE", "slots": [{"*SLEEVE"}]}]}


def infer(name):
    n = name.upper()
    for k in ("GYM BAG", "ARIA SLING", "SAFIRI TRAVEL", "CODE 3", "BONITA", "ZELUS", "ELYSE", "REMI", "FABELA"):
        if n.startswith(k):
            return k
    return None


def L(receipt, product, amount, qty=1, d=datetime.date(2026, 10, 4)):
    return {"receipt": receipt, "d": d, "product": product, "qty": qty, "amount": amount}


def test_pair_at_one_price_is_a_running_combo_any_order():
    out = rc.classify([L(1, "Aria Sling Black", 41000), L(1, "Gym Bag Black", 41000), L(1, "Delivery Fee", 18000)],
                      OFFERS, infer, M)
    assert out["running"]["GYMBAG + ARI SLING"]["count"] == 1
    assert out["running"]["GYMBAG + ARI SLING"]["revenue"] == 82000
    assert out["running"]["GYMBAG + ARI SLING"]["weeks"] == {2: 1}       # 4 Oct = Wk 2
    assert not out["selfMade"] and not out["singles"]


def test_four_bags_at_two_prices_are_two_combos():
    out = rc.classify([L(2, "Gym Bag Grey", 42500), L(2, "Zelus Black", 42500),
                       L(2, "Elyse Black", 65000), L(2, "Bonita Black", 65000), L(2, "Gift Bag A3", 5000)], OFFERS, infer, M)
    assert set(out["selfMade"]) == {"GYM BAG + ZELUS", "BONITA + ELYSE"}
    assert out["comboReceipts"] == 1


def test_alternatives_and_singles():
    out = rc.classify([L(3, "Safiri Travel Black", 60000), L(3, "Code 3 Black", 60000),
                       L(4, "Bonita Black", 85000), L(5, "Handled Laptop Sleeve 018 Black", 20000)], OFFERS, infer, M)
    assert out["running"]["SAFIRI + CODE 3"]["count"] == 1
    assert out["singlesOffer"]["BONITA"]["count"] == 1 and out["singlesOffer"]["SLEEVE"]["count"] == 1
    assert out["singles"]["SLEEVE"]["count"] == 1


def test_two_identical_bags_on_one_line_are_a_combo():
    out = rc.classify([L(6, "Remi Black", 90000, qty=2)], OFFERS, infer, M)
    assert out["selfMade"]["REMI + REMI"]["count"] == 1


def test_bulk_receipts_are_not_combos():
    out = rc.classify([L(7, "Fabela Black", 280000, qty=7)], OFFERS, infer, M)
    assert out["bulk"] == {"receipts": 1, "bags": 7, "revenue": 280000}
    assert not out["selfMade"] and not out["running"]


def test_offers_csv_loads_october():
    sz = rc.load_offers("October", "sinza")
    assert len(sz["combos"]) == 10 and len(sz["singles"]) == 10
    lola = next(o for o in sz["combos"] if o["name"].startswith("LOLA"))
    assert lola["slots"] == [{"LOLA"}, {"AVANA HB"}, {"MINI UMBRA"}] and lola["now"] == 115000
    ug = rc.load_offers("October", "uganda")
    assert len(ug["combos"]) == 5 and ug["combos"][2]["slots"][1] == {"BELT BAG", "NIZANA"}
    assert rc.load_offers("March", "uganda") is None
