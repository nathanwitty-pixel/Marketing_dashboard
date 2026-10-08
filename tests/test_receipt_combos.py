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
    assert out["selfMade"]["BONITA + ELYSE"]["days"] == {"2026-10-04": 1}
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


def test_uneven_prices_on_one_receipt_are_one_combo():
    # Uganda splits a combo's price unevenly: Jumbo 115,000 + Big Man Bag 70,000 = one combo, not 2 singles.
    out = rc.classify([L(10, "Jumbo Grey", 115000), L(10, "Big Man Bag Grey", 70000)], OFFERS,
                      lambda n: n.upper().rsplit(" ", 1)[0], M)
    assert out["selfMade"] == {"BIG MAN BAG + JUMBO": {"count": 1, "revenue": 185000, "weeks": {2: 1},
                                                        "days": {"2026-10-04": 1}, "bags": ["BIG MAN BAG", "JUMBO"]}}
    assert not out["singles"]


def test_shilling_rounding_still_one_price():
    out = rc.classify([L(11, "Gym Bag Black", 40000), L(11, "Aria Sling Black", 40001)], OFFERS, infer, M)
    assert out["running"]["GYMBAG + ARI SLING"]["count"] == 1


def test_refunded_receipt_is_dropped():
    lines = [dict(L(12, "Bonita Black", 85000), ref="UGANDA/0784"),
             dict(L(13, "Bonita Black", -85000, qty=-1), ref="UGANDA/0784 REFUND"),
             dict(L(14, "Bonita Black", 85000), ref="UGANDA/0785")]
    out = rc.classify(lines, OFFERS, infer, M)
    assert out["singles"]["BONITA"]["count"] == 1 and out["refunded"] == 1


def test_pair_plus_one_at_other_price_is_combo_plus_single():
    out = rc.classify([L(15, "Elyse Black", 75000), L(15, "Elyse Grey", 75001), L(15, "Bonita Black", 110000)],
                      OFFERS, infer, M)
    assert out["selfMade"]["ELYSE + ELYSE"]["count"] == 1 and out["singles"]["BONITA"]["count"] == 1


def test_six_identical_bags_are_bulk():
    out = rc.classify([L(16, "Remi Black", 65000)] * 6, OFFERS, infer, M)
    assert out["bulk"]["receipts"] == 1 and not out["selfMade"]


# ── offer_split (Bags on Offer › Sinza & Uganda) ──
def test_offer_split_listed_single_on_combo_bag_alone_off():
    lines = [L(10, "Bonita Black", 60000),                       # listed single → on offer
             L(11, "Gym Bag Grey", 45000),                       # listed-combo bag bought alone → not on offer
             L(12, "Remi Black", 30000)]                         # not listed at all → not on offer
    out = rc.offer_split(lines, OFFERS, infer)
    assert out["onSingles"] == {"BONITA": {"units": 1, "revenue": 60000}}
    assert out["offSingles"]["GYM BAG"] == {"units": 1, "revenue": 45000, "comboBag": True}
    assert out["offSingles"]["REMI"]["comboBag"] is False


def test_offer_split_combos_are_on_and_self_made_bags_counted():
    lines = [L(20, "Gym Bag Black", 41000), L(20, "Aria Sling Black", 41000),     # running combo
             L(21, "Remi Black", 40000), L(21, "Fabela Grey", 40000)]             # self-made combo
    out = rc.offer_split(lines, OFFERS, infer)
    assert out["combos"]["running"] == {"count": 1, "bags": 2, "revenue": 82000}
    assert out["combos"]["selfMade"] == {"count": 1, "bags": 2, "revenue": 80000}
    assert out["comboBags"] == {"REMI": 1, "FABELA": 1}
    assert not out["onSingles"] and not out["offSingles"]


def test_offer_split_bulk_is_others_and_refund_dropped():
    bulk = [L(30, "Remi Black", 150000, qty=5)]                  # amount = the line total (5 × 30,000)
    refunded = [dict(L(31, "Bonita Black", 60000), ref="SINZA/001"), dict(L(32, "Bonita Black", -60000, qty=-1), ref="SINZA/001 REFUND")]
    out = rc.offer_split(bulk + refunded, OFFERS, infer)
    assert out["bulk"] == {"receipts": 1, "bags": 5, "revenue": 150000}
    assert not out["onSingles"]                                   # the refunded single is gone
    assert out["bags"] == 5 and out["revenue"] == 150000           # every bag = on + off + bulk
