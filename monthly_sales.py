"""monthly_sales.py — the current month's real bags sold, from Postgres.

The monthly mirror of weekly_sales.py: same Odoo POS rules (net of refunds,
combos/rewards/gift-bag/delivery/strap excluded, Nairobi-local dates), but over
the whole calendar month instead of a Sun–Sat week. Writes monthly_sales_db.json
so current_performance.py can use the source-of-truth total for the CURRENT
month's Sales / target-achievement instead of the MONTHLY_TARGET sheet.

Run:
    python monthly_sales.py

Needs a .env with the DB connection (see .env.example) and lib/queries.py
filled in (ships resolved).
"""
from __future__ import annotations

import datetime
import json
import os

from lib import db, queries, report_month

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(BASE, "monthly_sales_db.json")


def month_window(ref: datetime.date | None = None) -> tuple[datetime.date, datetime.date]:
    """First → last calendar day of the LIVE month (today's month; see
    lib/report_month.py `live_month_window`).

    This feeds the LIVE Current Performance cards, which must always show the
    month we are actually in — on 1 Sep that is September (day 1), not the closed
    August. The archived monthly report is kept correct separately: the just-
    finished month is frozen via FINALIZED_MONTHS, and month_end.py PINS the month
    it archives (which makes this window resolve to that pinned month), so the 1-Sep
    'August report filled with September's day-1 bags' bug cannot recur."""
    return report_month.live_month_window(ref)


def _query_ready(sql: str) -> bool:
    return "{{" not in sql


def main() -> None:
    ok, detail = db.check_connection()
    if not ok:
        print(f"Postgres not reachable — {detail}")
        return
    if not _query_ready(queries.BAGS_SOLD_TOTAL):
        print("lib/queries.py still has {{placeholders}} — fill them in and re-run.")
        return

    start, end = month_window()
    df = db.run_query(
        queries.BAGS_SOLD_TOTAL,   # Product Sales GRAND TOTAL definition (bags incl. combo contents)
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

    # Net bags sold for master-catalogue products only (KPI on both pages).
    master_bags = None
    mdf = db.run_query(queries.MASTER_BAGS_SOLD,
                       {"start_date": start.isoformat(), "end_date": end.isoformat(),
                        "master": queries.master_products()})
    if mdf is not None and not mdf.empty:
        master_bags = int(round(float(mdf.iloc[0].get("bags") or 0)))

    payload = {
        "monthKey":     start.strftime("%Y-%m"),
        "monthLabel":   start.strftime("%B %Y"),
        "monthStart":   start.isoformat(),
        "monthEnd":     end.isoformat(),
        "monthlyBags":  round(bags),
        "monthlyValue": round(value),
        "masterBags":   master_bags,
        "lines":        lines,
        "computedOn":   datetime.date.today().isoformat(),
    }
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Monthly bags sold {start} → {end}: {bags:,.0f} bags "
          f"(KES {value:,.0f} across {lines:,} lines)")
    print("Written to monthly_sales_db.json — current_performance.py can now read it.")


if __name__ == "__main__":
    main()
