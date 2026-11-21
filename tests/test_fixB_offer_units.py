"""Tests for lib/offer_units.py Kenya combo units (20 Nov 2026 audit fix #19). Run:
    python -m pytest tests/test_fixB_offer_units.py -q
"""
import datetime
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import offer_units, receipt_combos   # noqa: E402

KE = {"combos": [{"name": "JUMBO + NIZANA", "slots": [{"JUMBO"}, {"NIZANA"}]}], "singles": []}


def _run(monkeypatch, rows):
    monkeypatch.setattr(offer_units, "_infer", lambda: (lambda n: n.upper().split(" ")[0] if " " in n else n.upper()))
    monkeypatch.setattr(offer_units, "_power_products", lambda m: [])
    monkeypatch.setattr(receipt_combos, "load_offers", lambda m, mk: KE if mk == "kenya" else None)
    monkeypatch.setattr(receipt_combos, "market_summary", lambda *a, **k: None)
    df = pd.DataFrame(rows, columns=["receipt", "combo", "combo_qty", "product", "qty"])
    monkeypatch.setattr(offer_units.db, "run_query", lambda sql, p=None: df)
    return offer_units.units(datetime.date(2026, 10, 1), datetime.date(2026, 10, 31))["kenya"]


def test_two_lines_of_one_combo_count_two(monkeypatch):
    # SQL sums the two combo lines (qty 2) and their sub-lines per bag: 2 Jumbo + 2 Nizana = 2 combos.
    assert _run(monkeypatch, [(1, 9, 2, "Jumbo Black", 2), (1, 9, 2, "Nizana Grey", 2)]) == {"JUMBO + NIZANA": 2}


def test_split_by_bag_not_by_list_order(monkeypatch):
    # qty 2 combo whose rows come back Jumbo, Jumbo, Nizana, Nizana: each combo is Jumbo + Nizana, not Jumbo + Jumbo.
    rows = [(1, 9, 2, "Jumbo Black", 1), (1, 9, 2, "Jumbo Grey", 1), (1, 9, 2, "Nizana Grey", 1), (1, 9, 2, "Nizana Red", 1)]
    assert _run(monkeypatch, rows) == {"JUMBO + NIZANA": 2}


def test_returned_combo_comes_off(monkeypatch):
    rows = [(1, 9, 1, "Jumbo Black", 1), (1, 9, 1, "Nizana Grey", 1),
            (2, 9, 1, "Jumbo Grey", 1), (2, 9, 1, "Nizana Red", 1),
            (3, 9, -1, "Jumbo Black", -1), (3, 9, -1, "Nizana Grey", -1)]   # order 3 = a return of order 1
    assert _run(monkeypatch, rows) == {"JUMBO + NIZANA": 1}
