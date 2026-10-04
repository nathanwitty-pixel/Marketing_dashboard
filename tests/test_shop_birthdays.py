"""Tests for lib/shop_birthdays.py (opening anniversaries from docs/shop-birthdays.md). Run:
    python -m pytest tests/test_shop_birthdays.py -q
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import shop_birthdays as sb   # noqa: E402

D = datetime.date


def test_table_parses_known_months_only():
    shops = {r["shop"] for r in sb.load()}
    assert {"Hilton", "Nanyuki", "Sinza", "Rongai"} <= shops
    assert "Meru" not in shops and "Starmall" not in shops          # month not given yet


def test_window_30_days_before_to_1_after():
    e = sb.for_shop("Nanyuki", D(2026, 9, 2))                       # 2 Oct 2023 → 30 days ahead
    assert e and e["days"] == 30 and e["age"] == 3 and "3rd birthday in 30 days" in e["label"]
    assert sb.for_shop("Nanyuki", D(2026, 9, 1)) is None            # 31 days ahead → not yet
    assert "was yesterday" in sb.for_shop("Nanyuki", D(2026, 10, 3))["label"]
    assert sb.for_shop("Nanyuki", D(2026, 10, 4)) is None


def test_aliases_and_year_wrap():
    assert sb.for_shop("TANZANIA", D(2026, 9, 1))["shop"] == "Sinza"
    assert sb.for_shop("KTDA SHOP", D(2026, 12, 31))["date"] == "2027-01-30"


def test_unknown_day_uses_first_and_says_so():
    e = sb.for_shop("Kisumu", D(2026, 9, 25))
    assert e["date"] == "2026-10-01" and "day not set" in e["label"]


def test_in_month():
    assert [e["shop"] for e in sb.in_month(2026, 10)] == ["Kisumu", "Nanyuki"]
