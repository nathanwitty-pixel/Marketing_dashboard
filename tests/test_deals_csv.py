"""Tests for the poster-sourced deals (deals_kenya.csv → self_made_combos._read_deals). Run:
    python -m pytest tests/test_deals_csv.py -q
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import self_made_combos as smc   # noqa: E402


def test_october_comes_from_the_csv():
    d = smc._read_deals("October")
    assert d["powerCount"] == 10
    pw = {p["product"]: (p["orig"], p["now"], p["disc"]) for p in d["powerDeals"]}
    assert pw["Bonita"] == (3900, 3000, 900) and pw["Standard Travel"] == (2600, 2200, 400)
    dow = {(x["product"], x["tier"]): x for x in d["dealOfWeek"]}
    big = dow[("Big Man Bag", "Tier 1")]
    assert {"Kisii", "Busia", "Starmall", "Hazina", "Hilton", "KTDA", "Kakamega", "Eldoret",
            "Mombasa", "Thika", "Meru", "Nanyuki"} <= set(big["locations"])
    assert (big["orig"], big["now"], big["disc"]) == (2100, 1700, 400)
    assert d["dowLocations"] == 17


def test_month_not_in_csv_uses_the_sheet_path(monkeypatch):
    called = {}

    class Boom(Exception):
        pass

    def fake_client():
        called["sheet"] = True
        raise Boom()
    import google_auth
    monkeypatch.setattr(google_auth, "get_gspread_client", fake_client)
    assert smc._local_deal_rows("March") is None
    assert smc._read_deals("March") is None and called.get("sheet")
