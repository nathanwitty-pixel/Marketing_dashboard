"""lib/bag_gender.py — who a bag is for (Male / Female / Unisex), from data/bag_gender.csv.
Spec: docs/weekly-report.md › D. Male vs female bags.

    gender(bag, category) → "Male" | "Female" | "Unisex" | None (None = gift bag, left out)
"""
from __future__ import annotations

import csv
import functools

from lib import paths

KINDS = ("Male", "Female", "Unisex")


@functools.lru_cache(maxsize=1)
def _table():
    cats, bags = {}, {}
    try:
        with open(paths.data("bag_gender.csv"), encoding="utf-8") as f:
            rows = [r for r in f if r.strip() and not r.lstrip().startswith("#")]
        for r in csv.DictReader(rows):
            g = (r.get("GENDER") or "").strip().title()
            if g not in KINDS:
                continue
            name = (r.get("NAME") or "").strip().upper()
            (bags if (r.get("KIND") or "").strip().lower() == "bag" else cats)[name] = g
    except FileNotFoundError:
        pass
    return cats, bags


def gender(bag: str, category: str | None) -> str | None:
    b, c = str(bag or "").strip().upper(), str(category or "").strip().upper()
    if c == "GIFT BAG" or b.startswith("GIFT BAG"):
        return None
    cats, bags = _table()
    return bags.get(b) or cats.get(c) or "Unisex"
