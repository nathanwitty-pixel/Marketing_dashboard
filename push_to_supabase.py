"""push_to_supabase.py — run the marketing migration against Supabase.

Regenerates migrations/marketing_dashboard.sql from the latest
monthly_report_history.json, then executes it on the Supabase Postgres given by
SUPABASE_DB_URL (in .env), and prints the resulting row counts.

Run:
    python push_to_supabase.py
"""
from __future__ import annotations

import os

import psycopg2
from dotenv import load_dotenv

import supabase_migration

load_dotenv()

BASE = os.path.dirname(os.path.abspath(__file__))
SQL_FILE = os.path.join(BASE, "migrations", "marketing_dashboard.sql")
TABLES = ("denri_mkt_monthly", "denri_mkt_weekly", "denri_mkt_new_products", "denri_mkt_offers",
          "denri_mkt_timed_offers", "denri_mkt_timed_offer_bags", "denri_mkt_timed_offer_days",
          "denri_mkt_timed_offer_weeks", "denri_mkt_self_made_summary", "denri_mkt_combo_sales",
          "denri_mkt_combo_requests")


def main() -> None:
    url = os.getenv("SUPABASE_DB_URL")
    if not url:
        print("SUPABASE_DB_URL not set (add it to .env).")
        return

    # Always rebuild the SQL from the current history first.
    supabase_migration.main()
    sql = open(SQL_FILE, encoding="utf-8").read()

    try:
        conn = psycopg2.connect(url, connect_timeout=15)
    except Exception as e:                                    # noqa: BLE001
        print(f"Could not connect to Supabase: {e}")
        print("If this is a host/IPv6 error, use the Session/Pooler connection "
              "string from Supabase → Database → Connection string instead.")
        return

    try:
        conn.autocommit = False
        with conn.cursor() as cur:
            cur.execute(sql)                                  # DDL + all inserts, one transaction
        conn.commit()
        print("Migration applied.")
        with conn.cursor() as cur:
            for t in TABLES:
                cur.execute(f"SELECT count(*) FROM {t}")
                print(f"  {t:<26} {cur.fetchone()[0]:>4} rows")
            cur.execute("SELECT month_key, month, year, achieved_pct, total_sales "
                        "FROM denri_mkt_monthly ORDER BY month_key")
            print("  months:", "; ".join(
                f"{m} {int(y)} — {a}% ({int(s):,} bags)" for (_, m, y, a, s) in cur.fetchall()))
    except Exception as e:                                    # noqa: BLE001
        conn.rollback()
        print(f"Migration failed (rolled back): {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
