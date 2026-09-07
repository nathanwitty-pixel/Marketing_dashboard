"""
month_end.py — the end-of-month archival routine.
─────────────────────────────────────────────────────────────────
Run this once at (or just after) the end of every month. It freezes the
just-completed month's numbers AND the report's written comments into Supabase,
where the History page reads them — so the live Monthly Report only ever shows
the newest month, and every past month lives in History.

What it does, in order:
  1. monthly_report.py    → rebuilds the report for the target month and writes
                            its snapshot (metrics + captured comments) into
                            monthly_report_history.json.
  2. push_to_supabase.py  → upserts every stored month (metrics + comments) into
                            the denri_mkt_* Supabase tables (idempotent).
  3. history.py           → re-reads Supabase into history.html so History shows
                            the freshly-archived month and its comments.

Target month = the month that just ended (the month containing yesterday), so a
1st-of-month run archives the month that just closed. Override with the env var
DENRI_REPORT_MONTH=YYYY-MM. The target month is PINNED for the run, which also
overrides monthly_report.py's FINALIZED_MONTHS guard so a finalized month can be
(re)built deliberately.

Run with the Python that has psycopg2 (the dashboard's Anaconda Python):
    & "C:\\ProgramData\\anaconda3\\python.exe" month_end.py
    # or a specific month:
    $env:DENRI_REPORT_MONTH="2026-08"; & "C:\\ProgramData\\anaconda3\\python.exe" month_end.py

Requires SUPABASE_DB_URL in .env (the Supabase SESSION POOLER connection string).
─────────────────────────────────────────────────────────────────
"""

import os
import sys
import subprocess
import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

# The current-month chain, regenerated PINNED to the month being archived so
# current_performance.html (which monthly_report.py reads) holds that month's
# figures — not the live month the dashboard is currently showing.
ARCHIVE_STEPS = ["monthly_sales.py", "weekly_sales.py", "current_performance.py",
                 "forward_projections.py", "monthly_report.py",
                 "push_to_supabase.py", "history.py"]

# After archiving, rebuild the live current-month view (unpinned) so the
# dashboard AND the monthly report return to the month we are actually in.
# (monthly_report.py run unpinned rebuilds the current-month HTML only; it does
# not touch history.json — that was just written for the archived month above.)
LIVE_RESTORE = ["monthly_sales.py", "weekly_sales.py", "current_performance.py",
                "forward_projections.py", "monthly_report.py"]


def target_month():
    """YYYY-MM to archive. Explicit DENRI_REPORT_MONTH wins; otherwise the month
    that just ended (the month containing yesterday)."""
    pinned = os.getenv("DENRI_REPORT_MONTH", "").strip()
    if pinned:
        return pinned
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return f"{yesterday.year}-{yesterday.month:02d}"


def run(script, env):
    path = os.path.join(BASE, script)
    print(f"\n\u25B6 {script}")
    print("-" * 60)
    result = subprocess.run([sys.executable, path], env=env)
    if result.returncode != 0:
        print(f"  \u2717 {script} exited with code {result.returncode}")
    return result.returncode


def main():
    tm = target_month()
    env_pin = dict(os.environ)
    env_pin["DENRI_REPORT_MONTH"] = tm    # pin the month (also overrides FINALIZED_MONTHS)
    env_pin["DENRI_LAUNCHER"] = "1"       # don't pop browser tabs
    env_live = dict(os.environ)
    env_live.pop("DENRI_REPORT_MONTH", None)   # unpinned = the month we are actually in
    env_live["DENRI_LAUNCHER"] = "1"

    print("=" * 60)
    print(f"  MONTH-END ARCHIVAL  \u2014  {tm}")
    print("=" * 60)

    failures = []
    for script in ARCHIVE_STEPS:              # rebuild + archive the target month (pinned)
        if run(script, env_pin) != 0:
            failures.append(script)

    print("\n\u2014 restoring the live current-month view \u2014")
    for script in LIVE_RESTORE:               # return the dashboard to today's month (unpinned)
        run(script, env_live)

    print("\n" + "=" * 60)
    if failures:
        print(f"  DONE WITH ERRORS \u2014 failed: {', '.join(failures)}")
        print("  Fix the cause and re-run; every step is idempotent (safe to repeat).")
        return 1
    print(f"  {tm} archived to Supabase \u2014 metrics + comments now in History.")
    print("  Live dashboards restored to the current month.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
