"""Tests for share_targets.py — python -m pytest scripts -q"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import share_targets as pt   # noqa: E402

D = datetime.date
S, E = D(2026, 7, 1), D(2026, 9, 30)          # 92 days
M = ["2026-07", "2026-08", "2026-09"]


def test_new_bag_is_scaled_to_the_days_it_was_in_shops():
    sold = {"OLD": {"2026-07": 300, "2026-08": 300, "2026-09": 320},
            "NEW": {"2026-09": 300}}                       # launched 1 Sep: 30 days, same daily pace
    rows = pt.allocate(sold, {"OLD": D(2025, 1, 1), "NEW": D(2026, 9, 1)}, 1000, S, E, M)
    t = {r["bag"]: r for r in rows}
    assert t["NEW"]["days"] == 30 and t["NEW"]["equiv"] == 920      # 300 / 30 × 92
    assert t["OLD"]["equiv"] == 920 and t["NEW"]["target"] == t["OLD"]["target"] == 500


def test_min_days_stops_a_brand_new_bag_inflating():
    rows = pt.allocate({"A": {"2026-09": 920}, "B": {"2026-09": 10}}, {"A": D(2025, 1, 1), "B": D(2026, 9, 29)},
                       100, S, E, M)
    assert {r["bag"]: r["days"] for r in rows}["B"] == 14


def test_out_of_stock_days_do_not_count():
    days_in_stock = {S + datetime.timedelta(days=i) for i in range(46)}   # stocked only the first 46 days
    rows = pt.allocate({"X": {"2026-07": 230, "2026-08": 230}, "Y": {"2026-07": 300, "2026-08": 300, "2026-09": 320}},
                       {"X": D(2025, 1, 1), "Y": D(2025, 1, 1)}, 100, S, E, M,
                       avail={"X": days_in_stock, "Y": {S + datetime.timedelta(days=i) for i in range(92)}})
    t = {r["bag"]: r for r in rows}
    assert t["X"]["days"] == 46 and t["X"]["equiv"] == 920 and t["X"]["target"] == t["Y"]["target"] == 50


def test_no_zero_targets_and_exact_total():
    sold = {"BIG": {"2026-09": 10000}, "TINY": {"2026-09": 1}, "NONE": {"2026-09": 0}}
    rows = pt.allocate(sold, {}, 1000, S, E, M)
    assert [r["bag"] for r in rows] == ["BIG"] and sum(r["target"] for r in rows) == 1000


def test_available_days_rebuilt_backwards_from_today():
    today = D(2026, 10, 4)
    # 5 on hand now; 5 arrived on 2 Oct; nothing before — so out of stock all period except sale days.
    avail = pt.available_days({"K": 5}, {"K": {D(2026, 10, 2): 5}}, {"K": {D(2026, 9, 10)}}, S, E, today)
    assert avail["K"] == {D(2026, 9, 10)}
    # stock all along: 3 now, no moves → every day in the period
    assert len(pt.available_days({"J": 3}, {}, {}, S, E, today)["J"]) == 92
