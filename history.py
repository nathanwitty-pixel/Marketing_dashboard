"""history.py — build the dashboard History page from Supabase.

Reads the four denri_mkt_* tables that push_to_supabase.py loaded (the frozen
monthly snapshots — Current Performance, Offer Type Analysis for all locations,
New Products, Posting Yields) and injects them into history.html so the
dashboard can showcase what is stored in Supabase.

This is the read side of the Supabase round-trip: supabase_migration.py /
push_to_supabase.py write the months; this reads them back for display.

Run:
    python history.py

Safe to run any time. If Supabase is unreachable it leaves the page's existing
data untouched (and prints why) so the launcher never fails on it.
"""
from __future__ import annotations

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
    finally:
        conn.close()

    by_key = {}
    for m in monthly:
        key = m["month_key"]
        by_key[key] = {
            "key": key,
            "month": m.get("month"),
            "year": _num(m.get("year")),
            "generatedOn": str(m["generated_on"]) if m.get("generated_on") else None,
            "monthly": {k: _num(v) for k, v in m.items()
                        if k not in ("month_key", "month", "generated_on")},
            "weekly": [],
            "newProducts": [],
            "offers": [],
        }

    def bucket(rows, field):
        for r in rows:
            key = r.pop("month_key")
            if key in by_key:
                by_key[key][field].append({k: _num(v) for k, v in r.items()})

    bucket(weekly, "weekly")
    bucket(newp, "newProducts")
    bucket(offers, "offers")

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


if __name__ == "__main__":
    main()
