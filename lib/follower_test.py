"""lib/follower_test.py — does a new follower become a sale? Pins new follows, WhatsApp chats and bags together.
Spec: docs/weekly-report.md › Follower test.

    run(daily) → {"days", "ok", "links": {"f2c", "c2b", "f2b"}, "verdict", "code", "from"}
      daily: DataFrame indexed by date with columns follows, chats, bags (NaN = not known that day)
"""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

LINK = 0.3        # score a link needs
P_MAX = 0.05      # chance test: at most this share of shuffles may score as high
MIN_DAYS = 28     # days of history before the test runs
SHUFFLES = 2000
LINKS = {"f2c": ("follows", "chats", 3, "Follows → Chats"),
         "c2b": ("chats", "bags", 2, "Chats → Bags"),
         "f2b": ("follows", "bags", 7, "Follows → Bags (awareness)")}


def _rank(a):
    return pd.Series(a).rank().to_numpy()


def _best(x, y, max_lag):
    """Best Spearman score of x[t] vs y[t+lag] over lags 0..max_lag → (score, lag)."""
    best, at = -2.0, 0
    for lag in range(max_lag + 1):
        a, b = (x[:-lag], y[lag:]) if lag else (x, y)
        m = ~(np.isnan(a) | np.isnan(b))
        if m.sum() < 10:
            continue
        r = np.corrcoef(_rank(a[m]), _rank(b[m]))[0, 1]
        if not np.isnan(r) and r > best:
            best, at = float(r), lag
    return (None, None) if best == -2.0 else (best, at)


def _link(x, y, max_lag, rng):
    r, lag = _best(x, y, max_lag)
    if r is None:
        return {"score": None, "lag": None, "p": None, "passed": False}
    hits = 0
    for _ in range(SHUFFLES):
        rs, _ = _best(rng.permutation(x), y, max_lag)
        if rs is not None and rs >= r:
            hits += 1
    p = (hits + 1) / (SHUFFLES + 1)
    return {"score": round(r, 2), "lag": lag, "p": round(p, 3), "passed": r >= LINK and p < P_MAX}


def run(daily: pd.DataFrame, seed: int = 7) -> dict:
    d = daily.sort_index().astype(float)
    d.index = pd.to_datetime(d.index)
    days = len(d)
    start = d.index.min().date() if days else None
    out = {"days": days, "from": start.isoformat() if start else None, "ok": days >= MIN_DAYS, "links": {}}
    if not out["ok"]:
        ready = start + dt.timedelta(days=MIN_DAYS - 1) if start else None
        out.update(code="early", ready=ready.isoformat() if ready else None,
                   verdict=f"Too early: {days} days of history; the test runs from {ready:%a} {ready.day} {ready:%b}." if ready
                   else "No follower data yet.")
        return out
    adj = d / d.groupby(d.index.dayofweek).transform("mean")         # weekday-adjusted
    rng = np.random.default_rng(seed)
    for k, (a, b, lag, _) in LINKS.items():
        out["links"][k] = _link(adj[a].to_numpy(), adj[b].to_numpy(), lag, rng)
    L = out["links"]
    if L["f2c"]["passed"] and L["c2b"]["passed"]:
        code, v = "chats", "Followers buy through WhatsApp: follows bring chats and the chats sell."
    elif L["f2b"]["passed"]:
        n = L["f2b"]["lag"]
        code, v = "awareness", (f"Awareness: follows lift sales {n} day{'s' if n != 1 else ''} later, but not through WhatsApp chats."
                                if n else "Awareness: follows and sales rise on the same days, but not through WhatsApp chats.")
    elif L["f2c"]["passed"]:
        code, v = "leak", "Follows bring chats that don't buy: fix the chat follow-up."
    else:
        code, v = "none", "Not yet: follows are brand growth only; judge Meta by chats and buyers."
    out.update(code=code, verdict=v)
    return out


def words(link: dict, name: str) -> str:
    """One link in plain words for the slide."""
    if link.get("score") is None:
        return f"{name}: not enough days."
    lag = link["lag"]
    when = "the same day" if lag == 0 else f"{lag} day{'s' if lag != 1 else ''} later"
    return (f"{name}: {'passed' if link['passed'] else 'not passed'} (score {link['score']:.2f}, best {when}, "
            f"chance {link['p'] * 100:.1f}%).")
