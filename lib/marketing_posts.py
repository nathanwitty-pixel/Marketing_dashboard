"""lib/marketing_posts.py — marketing POSTS per bag, from marketing's own daily posting sheets (16 Oct 2026).

Replaces the main spreadsheet's WEEKLY_MARKETING_POST / MONTHLY_MARKETING_POST tabs (user, 16 Oct 2026):
  • Kenya  — "MARKETING POSTS KENYA"        (1Os81Lhn…), tab "2026"
  • Sinza  — " STOCKS & POSTING RECORDS"    (1DGrRYrv…), tab "MARKETING POSTS_SINZA"
  • Uganda — same spreadsheet,                            tab "MARKETING POSTS_UGANDA"
Both spreadsheets must be shared (Viewer) with the dashboard's service account.

Layout (all three): the header row (row 2 — found as the row whose col A is "BAG TYPE") is
BAG TYPE · COLOUR · one column per DAY (M/D/YYYY) with a weekly TOTAL / TOTL column after each Saturday.
Each row is one bag × colour; a cell is that day's posts. Read here: only the dated columns — the TOTAL
columns and the sheet's own "TOTAL SUM" / "SUM TOTAL" rows are ignored (formulas; the totals rows don't
line up with the date columns). Each bag type's TOTAL row (COLOUR "TOTAL"): up to Aug 2026 it's the sum of
its colour rows; from Sep 2026 marketing types the posts there with the colours blank. So per day, what the
TOTAL row has beyond its colour rows counts as that bag's posts with NO colour — row (BAG TYPE, "") with
PRODUCT NAME = the bag type. A non-number in a day cell ("o", "\\") counts 0.

tab_rows(tab) gives the old tabs' exact layout, summed over that tab's period, so callers didn't change:
    COLOUR · CATEGORY · PRODUCT NAME · BAG TYPE · KENYA · SINZA · UGANDA · OUTSIDE KENYA · on-offer ✅/x KE · SZ · UG
  (the ✅/x ticks are MONTHLY_TARGET cols F/G/H by bag type — lib/odoo_tabs.offer_flags, as on the Odoo-built tabs)
  WEEKLY_MARKETING_POST  = the last complete Sun–Sat week (posts are "last week's posting work")
  MONTHLY_MARKETING_POST = the live month, 1st → today
PRODUCT NAME = BAG TYPE + COLOUR ("ACE" + "CROC BROWN"); COLOUR = the colour family and CATEGORY the bag
category, both from bag_names.csv (lib/colours) — the same values the old tabs carried.
"""
from __future__ import annotations

import csv
import datetime as _dt
import re

from lib import paths

KENYA_SHEET = "1Os81LhnsbTLrLScv4_M1tq_xb6Das2SDABR7Tlg0eYU"
OUTSIDE_SHEET = "1DGrRYrvAKRD5t1X1jxcAB7Abp8TkcXmpPjc8FGJutiM"
SOURCES = (("KENYA", KENYA_SHEET, "2026"),
           ("SINZA", OUTSIDE_SHEET, "MARKETING POSTS_SINZA"),
           ("UGANDA", OUTSIDE_SHEET, "MARKETING POSTS_UGANDA"))
MARKETS = ("KENYA", "SINZA", "UGANDA")
HEADER = ["COLOUR", "", "PRODUCT NAME", "BAG TYPE", "KENYA", "SINZA", "UGANDA", "OUTSIDE KENYA", "KENYA", "SINZA", "UGANDA"]

_DAILY = None        # {(BAG TYPE, COLOUR): {market: {date: posts}}} — read once per run
_ORDER = []          # keys in sheet order (Kenya first)
_FAIL = None         # the error, if the sheets couldn't be read this run


def _num(v) -> float:
    s = str(v or "").strip().replace(",", "")
    return float(s) if re.fullmatch(r"-?\d+(\.\d+)?", s) else 0.0


def _date(v):
    try:
        return _dt.datetime.strptime(str(v).strip(), "%m/%d/%Y").date()
    except ValueError:
        return None


def parse(rows) -> dict:
    """One tab's rows → {(BAG TYPE, COLOUR): {date: posts}}."""
    h = next((i for i, r in enumerate(rows[:10]) if r and str(r[0]).strip().upper() == "BAG TYPE"), None)
    if h is None:
        raise ValueError("no BAG TYPE header row")
    cols = [(j, d) for j, d in ((j, _date(c)) for j, c in enumerate(rows[h])) if d]
    out, total = {}, {}
    for r in rows[h + 1:]:
        bt = re.sub(r"\s+", " ", str(r[0]).strip().upper()) if r else ""
        col = re.sub(r"\s+", " ", str(r[1] if len(r) > 1 else "").strip().upper())
        if not bt or "TOTAL" in bt:                   # the sheet's TOTAL SUM / SUM TOTAL rows
            continue
        day = total.setdefault(bt, {}) if col == "TOTAL" else out.setdefault((bt, col), {})
        for j, d in cols:
            v = _num(r[j]) if j < len(r) else 0
            if v:
                day[d] = day.get(d, 0) + v          # a bag × colour listed twice (… WHITE) adds up
    # From Sep 2026 marketing types posts straight onto the bag type's TOTAL row (colours left blank).
    # Per day: whatever the TOTAL row has beyond its colour rows is posts with no colour → (BAG TYPE, "").
    by_bt = {}
    for (b, _), days in out.items():
        acc = by_bt.setdefault(b, {})
        for d, v in days.items():
            acc[d] = acc.get(d, 0) + v
    for bt, days in total.items():
        for d, t in days.items():
            c = by_bt.get(bt, {}).get(d, 0)
            if t > c:
                k = out.setdefault((bt, ""), {})
                k[d] = k.get(d, 0) + (t - c)
    return out


def daily() -> dict:
    """{(BAG TYPE, COLOUR): {market: {date: posts}}} from the three sheets (cached for the run).
    Raises if a sheet can't be read — callers already treat a failed posting read as "no posts"."""
    global _DAILY, _FAIL
    if _FAIL is not None:
        raise _FAIL                                         # tried once this run already
    if _DAILY is None:
        try:
            from lib.google_auth import get_gspread_client
            gc, books, out, order = get_gspread_client(), {}, {}, []
            for mkt, sid, tab in SOURCES:
                if sid not in books:
                    books[sid] = gc.open_by_key(sid)
                for key, days in parse(books[sid].worksheet(tab).get_all_values()).items():
                    if key not in out:
                        out[key] = {}
                        order.append(key)
                    out[key][mkt] = days
        except Exception as ex:                              # noqa: BLE001
            _FAIL = ex
            raise
        _DAILY, _ORDER[:] = out, order
    return _DAILY


def window(tab: str, today: _dt.date | None = None) -> tuple[_dt.date, _dt.date]:
    today = today or _dt.date.today()
    if tab == "WEEKLY_MARKETING_POST":                     # last complete Sun–Sat week
        sun = today - _dt.timedelta(days=(today.weekday() + 1) % 7)
        return sun - _dt.timedelta(days=7), sun - _dt.timedelta(days=1)
    if tab == "MONTHLY_MARKETING_POST":                    # the live month to date
        from lib import report_month
        s, e = report_month.live_month_window(today)
        return s, min(e, today)
    raise ValueError(f"unknown posting tab {tab!r}")


def posts(start: _dt.date, end: _dt.date) -> dict:
    """{(BAG TYPE, COLOUR): {market: posts}} over [start, end]."""
    return {k: {m: sum(v for d, v in by.get(m, {}).items() if start <= d <= end) for m in MARKETS}
            for k, by in daily().items()}


_CAT = None


def _category(name: str) -> str:
    global _CAT
    if _CAT is None:
        _CAT = {}
        try:
            with open(paths.data("bag_names.csv"), encoding="utf-8-sig") as f:
                for r in csv.DictReader(f):
                    _CAT.setdefault(re.sub(r"\s+", " ", (r.get("PRODUCT NAME") or "").strip().upper()),
                                    (r.get("CATEGORY") or "").strip().upper())
        except OSError:
            pass
    return _CAT.get(name, "")


def tab_rows(tab: str, start: _dt.date | None = None, end: _dt.date | None = None, sh=None) -> list[list]:
    """The old WEEKLY_ / MONTHLY_MARKETING_POST tab — same header and columns A–H — over the tab's period
    (or [start, end]). Posts are numbers as strings, like a sheet read."""
    from lib import colours, odoo_tabs
    flags = odoo_tabs.offer_flags(sh)
    if start is None or end is None:
        start, end = window(tab)
    p = posts(start, end)
    rows = [list(HEADER)]
    for key in _ORDER:
        bt, col = key
        n = p.get(key, {})
        name = f"{bt} {col}".strip()
        ke, sz, ug = (int(round(n.get(m, 0))) for m in MARKETS)
        fam = (colours.family(name, "") or col.title()) if col else ""     # bag-level row: no colour
        rows.append([fam, _category(name) or _bag_category(bt), name, bt, str(ke), str(sz), str(ug), str(sz + ug)]
                    + odoo_tabs._flag_cells(bt, flags))
    return rows


def is_bag_level(row) -> bool:
    """A tab_rows() row of posts with no colour (from the bag type's TOTAL row): COLOUR blank, NAME = BAG TYPE."""
    return len(row) > 3 and not str(row[0]).strip() and str(row[2]).strip().upper() == str(row[3]).strip().upper()


def _bag_category(bt: str) -> str:
    _category("")                                           # loads _CAT
    cats = [c for n, c in _CAT.items() if c and (n == bt or n.startswith(bt + " "))]
    return max(set(cats), key=cats.count) if cats else ""


def read(sh, tab: str) -> list[list]:
    """The posting tab's rows: from marketing's daily sheets (tab_rows); if they can't be read (not shared with
    the service account yet, Google down) the old tab of the main spreadsheet `sh`, with a warning."""
    try:
        rows = tab_rows(tab, sh=sh)
        s, e = window(tab)
        print(f"  {tab}: from the marketing posting sheets {s} → {e} ({len(rows) - 1} rows)")
        return rows
    except Exception as ex:                                  # noqa: BLE001
        print(f"  {tab}: marketing posting sheets unreadable ({type(ex).__name__}: {ex}) — using the old tab.")
        return sh.worksheet(tab).get_all_values()


if __name__ == "__main__":                                  # quick check: python -m lib.marketing_posts
    for t in ("WEEKLY_MARKETING_POST", "MONTHLY_MARKETING_POST"):
        s, e = window(t)
        r = tab_rows(t)[1:]
        print(t, s, "→", e, {m: sum(int(x[4 + i]) for x in r) for i, m in enumerate(MARKETS)})
