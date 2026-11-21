"""Tests for lib/report_month.py and the product_targets empty-CSV fix. Run:
    python -m pytest tests/test_fixA_report_month.py -q
"""
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import paths, product_targets, report_month   # noqa: E402

D = datetime.date


def test_first_of_month_archive_is_last_month_but_live_is_this_month(monkeypatch):
    monkeypatch.delenv(report_month.ENV_VAR, raising=False)
    a = report_month.anchor(D(2026, 9, 1))
    assert (a.year, a.month) == (2026, 8)
    assert report_month.live_anchor(D(2026, 9, 1)) == D(2026, 9, 1)


def test_pin_wins_for_both_anchors(monkeypatch):
    monkeypatch.setenv(report_month.ENV_VAR, "2026-08")
    assert report_month.anchor(D(2026, 11, 20)) == D(2026, 8, 31)
    assert report_month.live_anchor(D(2026, 11, 20)) == D(2026, 8, 31)


def test_month_key_rolls_back_over_new_year(monkeypatch):
    monkeypatch.delenv(report_month.ENV_VAR, raising=False)
    assert report_month.month_key(D(2027, 1, 1)) == "2026-12"


def test_write_csv_writes_no_file_when_there_are_no_rows(monkeypatch, tmp_path):
    monkeypatch.setattr(paths, "data", lambda *p: os.path.join(str(tmp_path), *p))
    monkeypatch.setattr(product_targets, "build",
                        lambda month_start=None: ([], 0, D(2026, 8, 1), D(2026, 10, 31), ["2026-08"]))
    path, rows, total = product_targets.write_csv(D(2026, 11, 1))
    assert rows == [] and total == 0
    assert not os.path.exists(path)
    assert os.listdir(str(tmp_path)) == []