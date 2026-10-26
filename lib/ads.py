"""lib/ads.py — marketing's Weekly Ads Performance Report, as data (spec: docs/ads-impact.md).

data/ads_weekly.csv — one row per campaign per Sun–Sat week (transcribed from the report each week).
data/ads_notes.csv  — the report's takeaways / next steps, tagged by page group.
"""
from __future__ import annotations

import csv
import datetime as _dt

from lib import paths

USD_KES = 129.0          # assumed KES per USD for the USD channels (Google, X) — shown with ≈ on the pages
MARKETS = ("KENYA", "SINZA", "UGANDA")
CHAT_TYPES = ("messages", "conversions")   # Meta messaging conversations + TikTok conversions = "messages"


def _f(v) -> float:
    try:
        return float(str(v).replace(",", "") or 0)
    except ValueError:
        return 0.0


def campaigns() -> list[dict]:
    """Every campaign-week row, with spend_kes added (USD × USD_KES)."""
    try:
        with open(paths.data("ads_weekly.csv"), encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    except OSError:
        return []
    out = []
    for r in rows:
        spend = _f(r["spend"])
        out.append({**r, "week": _dt.date.fromisoformat(r["week_start"]), "spend": spend,
                    "spend_kes": spend * (USD_KES if r["currency"].upper() == "USD" else 1),
                    "results": _f(r["results"]), "impressions": _f(r["impressions"]), "clicks": _f(r["clicks"])})
    return out


def weeks() -> list[_dt.date]:
    """The report's Sun–Sat weeks (week starts), oldest first."""
    return sorted({r["week"] for r in campaigns()})


def notes(week: _dt.date | None = None) -> list[dict]:
    """The report's notes for one week (default: the latest week that has notes)."""
    try:
        with open(paths.data("ads_notes.csv"), encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    except OSError:
        return []
    if not rows:
        return []
    week = week or max(_dt.date.fromisoformat(r["week_start"]) for r in rows)
    return [{**r, "tags": [t.strip() for t in r["tags"].split(";") if t.strip()]}
            for r in rows if _dt.date.fromisoformat(r["week_start"]) == week]


def market_week(rows: list[dict], market: str, week: _dt.date) -> dict:
    """Spend (KES, all channels), chat messages and website results for one market and week."""
    sel = [r for r in rows if r["market"] == market and r["week"] == week]
    return {"spend": sum(r["spend_kes"] for r in sel),
            "usd_spend": sum(r["spend_kes"] for r in sel if r["currency"].upper() == "USD"),
            "messages": sum(r["results"] for r in sel if r["result_type"] in CHAT_TYPES),
            "chat_spend": sum(r["spend_kes"] for r in sel if r["result_type"] in CHAT_TYPES)}
