"""The Weekly Report's period: which days the report covers, which days it is compared with, and the words the
slides use for both (docs/weekly-report.md › Period picker).

The page's Period dropdown (Today … Month to Date, Custom) saves data/wr_period.json as
{"key": "<preset>", "from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}; presets are worked out again from today on every
build, so "Yesterday" always means yesterday. No file (the default, and after the hourly rebuild) = Last Week.
`python generators/weekly_report.py yesterday` / `… custom 2026-11-01 2026-11-10` / `… clear` set it by hand.

Every slide reads the active period through active(): P.start / P.end (the report's days), P.cs / P.ce (the
days it is compared with), and the words: P.when ("last week", "yesterday", "in the last 30 days"), P.noun
("last week", "the last 30 days"), P.prev ("the week before", "the day before", "the same days last month").
"""
from __future__ import annotations

import calendar
import datetime as dt
import json
import os
import sys
from dataclasses import dataclass

from lib import paths

FILE = "wr_period.json"
PRESETS = [("today", "Today"), ("yesterday", "Yesterday"), ("this_week", "This Week"), ("last_week", "Last Week"),
           ("last_7", "Last 7 Days"), ("last_30", "Last 30 Days"), ("mtd", "Month to Date"), ("custom", "Custom")]
NAMES = dict(PRESETS)
DEFAULT = "last_week"
MAX_DAYS = 92


def _d(d: dt.date) -> str:
    return f"{d:%a} {d.day} {d:%b}"


@dataclass
class Period:
    key: str
    start: dt.date
    end: dt.date
    cs: dt.date            # comparison start
    ce: dt.date            # comparison end
    when: str              # "last week" — fits "Kenya sold 4,196 bags ___"
    noun: str              # "last week" — fits "___ brought 641 new follows"
    prev: str              # "the week before" — fits "55% fewer than ___"

    @property
    def name(self) -> str:
        return NAMES.get(self.key, "Custom")

    @property
    def days(self) -> int:
        return (self.end - self.start).days + 1

    @property
    def When(self) -> str:
        return self.when[:1].upper() + self.when[1:]

    @property
    def Noun(self) -> str:
        return self.noun[:1].upper() + self.noun[1:]

    @property
    def dates(self) -> str:
        """'Sun 15 Nov to Sat 21 Nov 2026' / 'Mon 23 Nov 2026'."""
        return (f"{_d(self.start)} {self.end.year}" if self.start == self.end
                else f"{_d(self.start)} to {_d(self.end)} {self.end.year}")

    @property
    def prev_dates(self) -> str:
        return _d(self.cs) if self.cs == self.ce else f"{_d(self.cs)} to {_d(self.ce)}"

    @property
    def is_week(self) -> bool:
        """A full Sun–Sat week (Last Week, or a custom range that is one)."""
        return self.days == 7 and self.start.weekday() == 6

    @property
    def short(self) -> str:
        """Table-header size: 'Last wk', 'Yesterday', 'Last 30d'."""
        return {"today": "Today", "yesterday": "Yesterday", "this_week": "This wk", "last_week": "Last wk",
                "last_7": "Last 7d", "last_30": "Last 30d", "mtd": "Month so far"}.get(self.key, "Period")

    @property
    def prev_short(self) -> str:
        return {"today": "Yesterday", "yesterday": "Day before", "this_week": "Same days last wk", "last_week": "Wk before",
                "last_7": "7d before", "last_30": "30d before", "mtd": f"Same days {self.cs:%b}"}.get(self.key, "Before")

    def to_json(self) -> dict:
        return {"key": self.key, "name": self.name, "short": self.short, "prevShort": self.prev_short,
                "from": self.start.isoformat(), "to": self.end.isoformat(),
                "cmpFrom": self.cs.isoformat(), "cmpTo": self.ce.isoformat(), "when": self.when, "noun": self.noun,
                "prev": self.prev, "dates": self.dates, "prevDates": self.prev_dates, "days": self.days}


def _same_days_last_month(a: dt.date, b: dt.date) -> tuple[dt.date, dt.date]:
    pm_end = a.replace(day=1) - dt.timedelta(days=1)
    last = calendar.monthrange(pm_end.year, pm_end.month)[1]
    return pm_end.replace(day=min(a.day, last)), pm_end.replace(day=min(b.day, last))


def make(key: str, today: dt.date | None = None, a: dt.date | None = None, b: dt.date | None = None) -> Period:
    t = today or dt.date.today()
    y = t - dt.timedelta(days=1)
    one = dt.timedelta(days=1)
    if key == "today":
        return Period(key, t, t, y, y, "so far today", "today so far", "the whole of yesterday")
    if key == "yesterday":
        return Period(key, y, y, y - one, y - one, "yesterday", "yesterday", "the day before")
    if key == "this_week":
        s = t - dt.timedelta(days=(t.weekday() + 1) % 7)          # this Sunday
        return Period(key, s, t, s - dt.timedelta(days=7), t - dt.timedelta(days=7), "this week so far",
                      "this week so far", "the same days last week")
    if key == "last_7":
        return Period(key, t - dt.timedelta(days=7), y, t - dt.timedelta(days=14), t - dt.timedelta(days=8),
                      "in the last 7 days", "the last 7 days", "the 7 days before")
    if key == "last_30":
        return Period(key, t - dt.timedelta(days=30), y, t - dt.timedelta(days=60), t - dt.timedelta(days=31),
                      "in the last 30 days", "the last 30 days", "the 30 days before")
    if key == "mtd":
        e = y if t.day > 1 else t
        s = e.replace(day=1)
        cs, ce = _same_days_last_month(s, e)
        return Period(key, s, e, cs, ce, "this month so far", "this month so far", f"the same days of {cs:%B}")
    if key == "custom" and a and b:
        a, b = sorted((a, b))
        b = min(b, t)
        a = max(a, b - dt.timedelta(days=MAX_DAYS - 1))
        n = (b - a).days + 1
        lab = _d(a) if a == b else f"{_d(a)} to {_d(b)}"
        nb = dt.timedelta(days=n)
        prev = ("the day before" if n == 1 else "the week before" if n == 7 else f"the {n} days before")
        return Period(key, a, b, a - nb, b - nb, f"on {lab}" if n == 1 else f"from {lab}", lab, prev)
    # last_week (the default): the last full Sun–Sat week before today
    e = t - dt.timedelta(days=(t.weekday() + 2) % 7 or 7)
    s = e - dt.timedelta(days=6)
    return Period("last_week", s, e, s - dt.timedelta(days=7), e - dt.timedelta(days=7), "last week", "last week",
                  "the week before")


def load(today: dt.date | None = None) -> Period:
    try:
        with open(paths.data(FILE), encoding="utf-8") as f:
            c = json.load(f)
        key = c.get("key") or "custom"
        a = dt.date.fromisoformat(c["from"]) if c.get("from") else None
        b = dt.date.fromisoformat(c["to"]) if c.get("to") else None
        return make(key if key in NAMES else "custom", today, a, b)
    except (OSError, ValueError, KeyError, TypeError):
        return make(DEFAULT, today)


def save(key: str | None, a: dt.date | None = None, b: dt.date | None = None) -> None:
    """Write the choice, or with key None / 'last_week' delete it (back to the default)."""
    p = paths.data(FILE)
    if not key or key == DEFAULT:
        try:
            os.remove(p)
        except OSError:
            pass
        return
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"key": key, "from": a.isoformat() if a else None, "to": b.isoformat() if b else None}, f)


def from_argv(argv=None) -> None:
    """`weekly_report.py yesterday` / `… custom FROM TO` / `… clear`; anything else leaves the file alone."""
    args = (sys.argv if argv is None else argv)[1:]
    if not args:
        return
    if args[0] == "clear":
        save(None)
    elif args[0] == "custom" and len(args) >= 3:
        try:
            save("custom", dt.date.fromisoformat(args[1]), dt.date.fromisoformat(args[2]))
        except ValueError:
            pass
    elif args[0] in NAMES:
        save(args[0])


def full_week(p: Period, today: dt.date | None = None) -> Period:
    """For the slides built from whole Sun–Sat weeks (Weekly Performance, Why Did We Move?, Why shops): the last
    full week that ends on or before the period's last day. It is Last Week itself (worded "last week") when
    that is the week; otherwise a dated week ("from Sun 8 Nov to Sat 14 Nov")."""
    t = today or dt.date.today()
    e = p.end if p.end.weekday() == 5 else p.end - dt.timedelta(days=(p.end.weekday() + 2) % 7 or 7)
    lw = make("last_week", t)
    if e >= lw.end:
        return lw
    return make("custom", t, e - dt.timedelta(days=6), e)


_ACTIVE: Period | None = None


def active() -> Period:
    """The period this build is for (set once by the generator; read by every slide module)."""
    global _ACTIVE
    if _ACTIVE is None:
        _ACTIVE = load()
    return _ACTIVE


def set_active(p: Period) -> None:
    global _ACTIVE
    _ACTIVE = p
