"""history.py — build the dashboard History page from Supabase.

Reads the denri_mkt_* tables that push_to_supabase.py loaded (the frozen monthly
snapshots — Current Performance, New Products, Offer Type Analysis for all
locations, Posting Yields, and each month's Timed Offer campaigns with their
bags and daily sales series) and injects them into history.html so the dashboard
can showcase what is stored in Supabase.

This is the read side of the Supabase round-trip: supabase_migration.py /
push_to_supabase.py write the months; this reads them back for display.

Run:
    python history.py

Safe to run any time. If Supabase is unreachable it leaves the page's existing
data untouched (and prints why) so the launcher never fails on it.
"""
from __future__ import annotations

import datetime
import json
import os
import re
from datetime import date

try:
    import psycopg2
except ModuleNotFoundError:   # dashboard launched under a Python without the driver
    psycopg2 = None
from dotenv import load_dotenv

load_dotenv()

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "history.html")
START = "<!-- HISTORY_DATA_START -->"
END = "<!-- HISTORY_DATA_END -->"


def _num(v):
    """psycopg2 numerics come back as Decimal — make them JSON-friendly.
    Whole numbers print as ints; keep None as None."""
    if v is None:
        return None
    try:
        f = float(v)
        return int(f) if f == int(f) else round(f, 2)
    except (TypeError, ValueError):
        return v


def _val(v):
    """Like _num, but leaves booleans alone and renders dates as ISO strings —
    the timed-offer tables carry both, and json.dumps chokes on a date object."""
    if isinstance(v, bool) or v is None:
        return v
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    return _num(v)


def _rows(cur, sql, params=None):
    cur.execute(sql, params or ())
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def fetch_months(url):
    conn = psycopg2.connect(url, connect_timeout=15)
    try:
        with conn.cursor() as cur:
            monthly = _rows(cur, "select * from denri_mkt_monthly order by month_key")
            weekly = _rows(cur, "select * from denri_mkt_weekly order by month_key, seq")
            newp = _rows(cur, "select * from denri_mkt_new_products order by month_key, sold desc")
            offers = _rows(cur, "select * from denri_mkt_offers order by month_key, region, units desc nulls last")
            timed = _rows(cur, "select * from denri_mkt_timed_offers order by month_key, seq")
            timed_bags = _rows(cur, "select * from denri_mkt_timed_offer_bags "
                                    "order by month_key, offer_seq, sold desc nulls last")
            timed_days = _rows(cur, "select * from denri_mkt_timed_offer_days "
                                    "order by month_key, offer_seq, day")
            timed_weeks = _rows(cur, "select * from denri_mkt_timed_offer_weeks "
                                     "order by month_key, offer_seq, seq")
            smc_summary = _rows(cur, "select * from denri_mkt_self_made_summary order by month_key")
            combo_sales = _rows(cur, "select * from denri_mkt_combo_sales "
                                     "order by month_key, self_made desc, units desc")
            combo_reqs = _rows(cur, "select * from denri_mkt_combo_requests "
                                    "order by month_key, cbr desc")
    finally:
        conn.close()

    by_key = {}
    for m in monthly:
        key = m["month_key"]
        # comments is a jsonb list of {section,label,type,text}; psycopg2 usually
        # decodes it already, but guard the string case for older drivers.
        _cmts = m.get("comments")
        if isinstance(_cmts, str):
            try:
                _cmts = json.loads(_cmts)
            except (ValueError, TypeError):
                _cmts = []
        by_key[key] = {
            "key": key,
            "month": m.get("month"),
            "year": _num(m.get("year")),
            "generatedOn": str(m["generated_on"]) if m.get("generated_on") else None,
            "comments": _cmts or [],
            "monthly": {k: _num(v) for k, v in m.items()
                        if k not in ("month_key", "month", "generated_on", "comments")},
            "weekly": [],
            "newProducts": [],
            "offers": [],
            "timedOffers": [],
            "selfMade": {"summary": None, "sales": [], "requests": []},
        }

    def bucket(rows, field):
        for r in rows:
            key = r.pop("month_key")
            if key in by_key:
                by_key[key][field].append({k: _num(v) for k, v in r.items()})

    bucket(weekly, "weekly")
    bucket(newp, "newProducts")
    bucket(offers, "offers")

    # Timed offers arrive as three flat tables; nest the bags and the daily
    # series back under their campaign so the page can render one block per
    # campaign. Keyed on (month_key, seq/offer_seq).
    campaigns = {}
    for r in timed:
        key, seq = r["month_key"], r.get("seq")
        if key not in by_key:
            continue
        camp = {k: _val(v) for k, v in r.items() if k != "month_key"}
        camp["bags"], camp["daily"], camp["weekly"] = [], [], []
        by_key[key]["timedOffers"].append(camp)
        campaigns[(key, seq)] = camp

    for rows, field in ((timed_bags, "bags"), (timed_days, "daily"), (timed_weeks, "weekly")):
        for r in rows:
            camp = campaigns.get((r["month_key"], r.get("offer_seq")))
            if camp is not None:
                camp[field].append({k: _val(v) for k, v in r.items()
                                    if k not in ("month_key", "offer_seq")})

    # Self-made combos: one summary row per month, plus the sold-combo lines and
    # the CBR request log.
    for r in smc_summary:
        key = r.get("month_key")
        if key in by_key:
            by_key[key]["selfMade"]["summary"] = {k: _num(v) for k, v in r.items() if k != "month_key"}
    for r in combo_sales:
        key = r.get("month_key")
        if key in by_key:
            by_key[key]["selfMade"]["sales"].append({k: _val(v) for k, v in r.items() if k != "month_key"})
    for r in combo_reqs:
        key = r.get("month_key")
        if key in by_key:
            by_key[key]["selfMade"]["requests"].append({k: _val(v) for k, v in r.items() if k != "month_key"})

    # newest month first so the page defaults to the latest
    return [by_key[k] for k in sorted(by_key, reverse=True)]


def inject(payload):
    with open(HTML, "r", encoding="utf-8") as f:
        html = f.read()

    block = (f"{START}\n"
             f'<script id="history-data" type="application/json">\n'
             f"{json.dumps(payload, ensure_ascii=False, indent=0)}\n"
             f"</script>\n{END}")

    if START in html and END in html:
        html = re.sub(re.escape(START) + r".*?" + re.escape(END), block, html, flags=re.DOTALL)
    else:
        # First run before the markers exist — nothing to do; the template ships
        # with the markers, so this only guards a hand-edited file.
        print("  history.html is missing the data markers — not modified.")
        return
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    if psycopg2 is None:
        print("psycopg2 not installed in this Python — history.html left unchanged. "
              "Install it with:  python -m pip install psycopg2-binary")
        return
    url = os.getenv("SUPABASE_DB_URL")
    if not url:
        print("SUPABASE_DB_URL not set (add it to .env) — history.html left as-is.")
        return
    try:
        months = fetch_months(url)
    except Exception as e:                                    # noqa: BLE001
        print(f"Could not read from Supabase: {e}")
        print("history.html left unchanged.")
        return

    payload = {
        "source": "Supabase",
        "generatedOn": date.today().isoformat(),
        "months": months,
    }
    inject(payload)
    names = ", ".join(f"{m['month']} {m['year']}" for m in months) or "none"
    print(f"history.html updated — {len(months)} month(s) from Supabase: {names}")
    for m in months:
        for c in m.get("timedOffers", []):
            print(f"  timed offer · {m['month']} {m['year']}: {c.get('name')} "
                  f"({c.get('window_label')}) — {c.get('total_sold')} bags, "
                  f"{len(c.get('bags', []))} bag rows, {len(c.get('daily', []))} daily rows")


if __name__ == "__main__":
    main()
