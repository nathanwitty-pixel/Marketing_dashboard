"""weekly_sales.py — the weekly-sales fix.

Computes the CURRENT Sun–Sat week's real bags sold from Postgres (the source of
truth) and writes it to weekly_sales_db.json. current_performance.py can then
read that instead of the flaky WEEKLY_SALES Google-Sheet tab, so the Weekly
Sales card stops showing the whole month / 494.5%.

Run:
    python weekly_sales.py

Needs: a .env with the DB connection (see .env.example) AND the sale-line
table/columns filled into lib/queries.py (it ships with {{placeholders}}).
"""
from __future__ import annotations

import datetime
import json
import os

from lib import db, queries

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(BASE, "weekly_sales_db.json")


def week_window(ref: datetime.date | None = None) -> tuple[datetime.date, datetime.date]:
    """The Sun–Sat week containing `ref` (defaults to today) — matches the
    dashboard's week_start_of()."""
    ref = ref or datetime.date.today()
    start = ref - datetime.timedelta(days=(ref.weekday() + 1) % 7)   # back to Sunday
    return start, start + datetime.timedelta(days=6)


def _query_ready(sql: str) -> bool:
    return "{{" not in sql


def main() -> None:
    ok, detail = db.check_connection()
    if not ok:
        print(f"Postgres not reachable — {detail}")
        return
    if not _query_ready(queries.BAGS_SOLD_TOTAL):
        print("lib/queries.py still has {{placeholders}}.")
        print("Fill in your sale-line table/columns (or paste your real BAGS_SOLD")
        print("SQL) and re-run — see the comments at the top of lib/queries.py.")
        return

    start, end = week_window()
    df = db.run_query(
        queries.BAGS_SOLD_TOTAL,   # same "bags sold" definition as the monthly total, so they reconcile
        {"start_date": start.isoformat(), "end_date": end.isoformat(),
         "excluded": queries.excluded_products()},
    )
    if df is None or df.empty:
        print(f"No sales rows for {start} → {end}.")
        return

    r = df.iloc[0]
    bags = float(r.get("bags") or 0)
    value = float(r.get("value") or 0)
    lines = int(r.get("lines") or 0)

    payload = {
        "weekStart":   start.isoformat(),
        "weekEnd":     end.isoformat(),
        "weeklyBags":  round(bags),
        "weeklyValue": round(value),
        "lines":       lines,
        "computedOn":  datetime.date.today().isoformat(),
    }
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Weekly bags sold {start} → {end}: {bags:,.0f} bags "
          f"(KES {value:,.0f} across {lines:,} lines)")
    print("Written to weekly_sales_db.json — current_performance.py can now read it.")


if __name__ == "__main__":
    main()
