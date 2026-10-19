"""lib/shop_regions.py — Shop → Region from docs/shop-regions.md (the source of truth; edit the table there)."""
from __future__ import annotations

from lib import paths


def load(default=None):
    """{SHOP (upper): region} parsed from the markdown table under the heading that mentions "shop" (first column =
    shop, second = region). Falls back to `default` (or {}) when the file is missing or has no rows."""
    try:
        lines = open(paths.doc("shop-regions.md"), encoding="utf-8").read().splitlines()
    except OSError:
        return dict(default or {})
    out, in_section = {}, False
    for ln in lines:
        s = ln.strip()
        if s.startswith("#"):                                    # heading → enter/leave the shops table
            in_section = "shop" in s.lower()
            continue
        if not (in_section and s.startswith("|")):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 2 or not cells[0] or not cells[1]:
            continue
        if cells[0].upper() == "SHOP" or set(cells[0]) <= set("-: "):   # header / separator row
            continue
        out[cells[0].upper()] = cells[1]
    return out or dict(default or {})
