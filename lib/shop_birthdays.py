"""lib/shop_birthdays.py — shop opening anniversaries ("birthdays"), a sales hook.

Source of truth: the table in docs/shop-birthdays.md (edit it there — no code change). A
birthday is flagged from WINDOW_BEFORE days ahead to WINDOW_AFTER days after, so an offer /
posts can be planned for that shop. Used by Shops Efficiency, Bags on vs off Offer, the Push
Planner and the Monthly Report.

    upcoming(today)          → [{shop, date, days, age, label, dayKnown}], soonest first
    for_shop(name, today)    → that shop's entry if it's in the window, else None
    in_month(year, month)    → every shop whose birthday falls in that month
    next_up(today, n)        → the next n birthdays after the window (whatever the distance)
"""
import calendar
import datetime
import os
import re

DOC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "shop-birthdays.md")
WINDOW_BEFORE, WINDOW_AFTER = 30, 1
# Names the sheet / tills use for a dashboard shop.
_ALIASES = {"NAIROBI": "STARMALL", "TANZANIA": "SINZA", "DAR-ES-ALAM": "SINZA", "KTDA SHOP": "KTDA",
            "WEBSITE SALES": "WEBSITE"}
_MONTHS = {m.upper(): i for i, m in enumerate(calendar.month_name) if m}
_MONTHS.update({m.upper(): i for i, m in enumerate(calendar.month_abbr) if m})
_MONTHS.update({"SEPT": 9, "OCTOMBER": 10})

_ROWS = None


def _key(name):
    k = re.sub(r"\s+", " ", str(name or "").strip().upper())
    return _ALIASES.get(k, k)


def load():
    """[{shop, month, day, year, dayKnown, note}] for every shop with a known month."""
    global _ROWS
    if _ROWS is not None:
        return _ROWS
    rows = []
    try:
        with open(DOC, encoding="utf-8") as f:
            text = f.read()
        body = text.split("## Shop → opening date", 1)[1].split("\n## ", 1)[0]
        for line in body.splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4 or cells[0] in ("Shop", "") or set(cells[0]) <= set("-"):
                continue
            month = _MONTHS.get(cells[1].upper())
            if not month:
                continue                                     # month unknown → no birthday yet
            day = int(cells[2]) if cells[2].isdigit() else None
            year = int(cells[3]) if cells[3].isdigit() else None
            rows.append({"shop": cells[0], "month": month, "day": day or 1, "dayKnown": day is not None,
                         "year": year, "note": cells[4] if len(cells) > 4 else ""})
    except (OSError, IndexError, ValueError) as e:
        print(f"  Shop birthdays unavailable ({e}) — none shown.")
    _ROWS = rows
    return rows


def _ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def _on(r, year):
    """The birthday in a given year (29 Feb → 28 Feb in a common year)."""
    return datetime.date(year, r["month"], min(r["day"], calendar.monthrange(year, r["month"])[1]))


def _entry(r, date, today):
    days = (date - today).days
    age = date.year - r["year"] if r["year"] else None
    what = (_ordinal(age) + " birthday") if age and age > 0 else ("opening anniversary" if age == 0 else "birthday")
    when = ("today" if days == 0 else "tomorrow" if days == 1 else "was yesterday" if days == -1
            else f"in {days} days" if days > 0 else f"was {-days} days ago")
    return {"shop": r["shop"], "date": date.isoformat(), "days": days, "age": age, "dayKnown": r["dayKnown"],
            "what": what,
            "label": f"🎂 {what} {when}" + ("" if r["dayKnown"] else " (day not set)"),
            "dateLabel": date.strftime("%d %b").lstrip("0") if r["dayKnown"] else date.strftime("%B")}


def upcoming(today=None, before=WINDOW_BEFORE, after=WINDOW_AFTER):
    """Shops whose birthday is within [today - after, today + before], soonest first."""
    today = today or datetime.date.today()
    out = []
    for r in load():
        for y in (today.year - 1, today.year, today.year + 1):
            d = _on(r, y)
            if -after <= (d - today).days <= before:
                out.append(_entry(r, d, today))
                break
    return sorted(out, key=lambda e: e["days"])


def for_shop(name, today=None):
    """The shop's birthday entry when it's inside the window, else None (name matched loosely)."""
    k = _key(name)
    return next((e for e in upcoming(today) if _key(e["shop"]) == k), None)


def by_shop(today=None):
    """{SHOP_KEY: entry} for every shop in the window — for pages that badge many shops."""
    return {_key(e["shop"]): e for e in upcoming(today)}


def in_month(year, month, today=None):
    """Every shop whose birthday falls in that month (for the Monthly Report), by date."""
    ref = today or datetime.date(year, month, 1)
    return sorted((_entry(r, _on(r, year), ref) for r in load() if r["month"] == month),
                  key=lambda e: e["date"])


def next_up(today=None, n=3):
    """The next n birthdays strictly after today, soonest first (for "none soon — next: …")."""
    today = today or datetime.date.today()
    out = []
    for r in load():
        d = _on(r, today.year)
        if d <= today:
            d = _on(r, today.year + 1)
        out.append(_entry(r, d, today))
    return sorted(out, key=lambda e: e["days"])[:n]
