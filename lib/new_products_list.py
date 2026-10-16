"""lib/new_products_list.py — which bag types count as this month's NEW PRODUCTS.

Source: new_products.txt at the project root (editable, one bag type per line).
It is the only source — the ✅ ticks in MONTHLY_TARGET col I are no longer read.
"""
import os as _os

from lib import paths as _paths

_FILE = _paths.data("new_products.txt")


def names():
    """Upper-cased bag types from new_products.txt in file order ([] = no new products)."""
    out = []
    try:
        with open(_FILE, encoding="utf-8") as f:
            for line in f:
                s = line.split("#", 1)[0].strip().upper()
                if s and s not in out:
                    out.append(s)
    except OSError:
        pass
    return out
