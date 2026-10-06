"""Per-page Custom period: the From – To dates a page was last built for.

Each page keeps its own JSON file (`{"from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}`) in the project
root, written by the Streamlit page's Custom-range picker (Apply) and deleted by Clear. A generator
reads it with load(); `python <page>.py 2026-09-01 2026-09-30` / `python <page>.py clear` set it
from the command line via from_argv(). Spec: docs/README.md › Custom range.
"""
import calendar
import datetime
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_DAYS = 366

# page → its range file (bags_on_offer.py keeps its own boo_custom_range.json reader)
FILES = {
    "new_products":   "np_custom_range.json",
    "posting_yields": "py_custom_range.json",
}


def path(page):
    return os.path.join(BASE, FILES[page])


def load(page):
    """(from, to) dates for the page's Custom period, or None. Swapped if reversed; capped at
    MAX_DAYS (the latest days are kept); a To date in the future is pulled back to today."""
    try:
        with open(path(page), encoding="utf-8") as f:
            c = json.load(f)
        a, b = datetime.date.fromisoformat(c["from"]), datetime.date.fromisoformat(c["to"])
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if a > b:
        a, b = b, a
    b = min(b, datetime.date.today())
    a = max(a, b - datetime.timedelta(days=MAX_DAYS - 1))
    return (a, b) if a <= b else None


def save(page, a, b=None):
    """Write the range, or with a=None delete it (Clear)."""
    if a is None:
        try:
            os.remove(path(page))
        except OSError:
            pass
        return
    with open(path(page), "w", encoding="utf-8") as f:
        json.dump({"from": a.isoformat(), "to": b.isoformat()}, f)


def from_argv(page, argv=None):
    """`<script> FROM TO` saves a range, `<script> clear` deletes it; anything else is ignored."""
    args = (sys.argv if argv is None else argv)[1:]
    if args[:1] == ["clear"]:
        save(page, None)
    elif len(args) >= 2:
        try:
            save(page, datetime.date.fromisoformat(args[0]), datetime.date.fromisoformat(args[1]))
        except ValueError:
            pass


def label(a, b):
    """'01 Sep – 30 Sep' (years added when the range crosses one or isn't this year)."""
    yr = a.year != b.year or b.year != datetime.date.today().year
    f = "%d %b %Y" if yr else "%d %b"
    return f"{a.strftime(f)} – {b.strftime(f)}"


def month_share(a, b):
    """How many months the range covers — each day counts 1/(days in its month). A monthly target
    × this = the range's pro-rated target (01–30 Sep = 1.0; 15 Sep – 14 Oct ≈ 1.0)."""
    d, total = a, 0.0
    while d <= b:
        total += 1 / calendar.monthrange(d.year, d.month)[1]
        d += datetime.timedelta(days=1)
    return total


def block(page):
    """The page's NP/PA `custom` data block: None, or {from, to, label, days, months}."""
    r = load(page)
    if not r:
        return None
    a, b = r
    return {"from": a.isoformat(), "to": b.isoformat(), "label": label(a, b),
            "days": (b - a).days + 1, "months": round(month_share(a, b), 4)}
