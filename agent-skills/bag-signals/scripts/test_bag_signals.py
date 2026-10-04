"""Tests for bag_signals.py — python -m pytest scripts -q"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bag_signals as bq   # noqa: E402

N = 91


def test_steady_seller_with_stock_is_post_more():
    daily = {"A": [10 + (1 if i % 2 else -1) for i in range(N)]}            # mean 10, tiny swing
    s = bq.signals(daily, [20.0 + (i % 3) for i in range(N)], {"A": 400})["A"]
    assert abs(s["avg"] - 10.0) < 0.02 and s["reliability"] > 5 and s["cover"] == 40 and s["action"] == "Post more"


def test_run_out_risk_and_safe_stock():
    daily = {"B": [5 + (2 if i % 2 else -2) for i in range(N)]}             # mean ≈ 5, swing ≈ 2
    s = bq.signals(daily, [10.0] * N, {"B": 20})["B"]                      # 14-day demand ≈ 70 ≫ 20
    assert s["runOut"] > 0.99 and s["action"] == "Restock first"
    assert s["safeStock"] == round(14 * s["avg"] + 1.645 * s["swing"] * 14 ** 0.5)
    assert s["restock"] == s["safeStock"] - 20


def test_real_decline_is_flagged_but_noise_is_not():
    falling = [8.0] * 63 + [2.0] * 28
    noisy = [5 + (3 if i % 2 else -3) for i in range(N)]
    out = bq.signals({"F": falling, "N": noisy}, [20.0] * N, {"F": 5000, "N": 5000})
    assert out["F"]["trendZ"] <= -2 and out["F"]["action"] == "Falling — act"
    assert abs(out["N"]["trendZ"]) < 2


def test_beta_scales_to_share():
    total = [100.0 + (40 if i % 7 in (5, 6) else 0) for i in range(N)]     # weekends busier
    prop = [t * 0.1 for t in total]                                         # moves in proportion → β ≈ 1
    flat = [10.0 + (1 if i % 2 else -1) for i in range(N)]                  # ignores the market → β ≈ 0
    out = bq.signals({"P": prop, "Q": flat}, total, {"P": 999, "Q": 999})
    assert abs(out["P"]["beta"] - 1) < 0.05 and abs(out["Q"]["beta"]) < 0.3


def test_days_before_launch_are_ignored_and_too_few_sales():
    late = [None] * 61 + [3.0] * 30
    out = bq.signals({"L": late, "T": [0.0] * 90 + [3.0]}, [10.0] * N, {"L": 300})
    assert out["L"]["days"] == 30 and out["L"]["avg"] == 3.0
    assert out["T"]["tooFew"] is True


def test_posting_beta_needs_history():
    hist = [{"week": i, "bags": {"X": {"posts": p, "sold": 10 + 2 * p}}} for i, p in enumerate([0, 1, 2, 3, 4, 5])]
    assert bq.posting_beta(hist, "X") == 2.0
    assert bq.posting_beta(hist[:5], "X") is None
