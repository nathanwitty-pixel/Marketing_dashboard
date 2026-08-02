"""
forward_projections.py
─────────────────────────────────────────────────────────────────
Edit the values in MANUAL INPUTS, then run:
    python forward_projections.py

First run: a browser window will open asking you to sign in to
Google. After that, credentials are saved locally and every
subsequent run is fully automatic.
─────────────────────────────────────────────────────────────────
Reads live from Google Sheets (one connection, two sheets):

  MONTHLY_TARGET sheet
    col C (TARGET) → sum all rows below header  →  total_target
    col D (SALES)  → sum all rows below header  →  total_sales

  WEEKLY_SALES sheet
    col C = "SUM TOTAL" row, col X (TOTAL)      →  weekly_sales_total
"""

import re, webbrowser, os, pathlib, calendar, subprocess, sys, json
from datetime import date, timedelta

# ── SPREADSHEET ───────────────────────────────────────────────

SPREADSHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"


# ── MANUAL INPUTS — fill these in yourself ────────────────────

corporate_bags = 138+131+43   # 138 prior + 131 new corporate bags in week 4 (Forecasted Projection)
# bare_minimum is computed below = monthly target ÷ perfect weeks in month.


# ── PERFECT (COMPLETE) WEEKS IN THE MONTH ─────────────────────
# A "perfect week" = a week with >=5 of its days falling inside the month
# (the project's count_complete_weeks_in_month definition). Sales run
# Sun–Sat, so weeks are counted from Sunday.

def count_complete_weeks_in_month(ref=None):
    today = ref or date.today()
    year, month = today.year, today.month
    month_start = date(year, month, 1)
    if month == 12:
        month_end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = date(year, month + 1, 1) - timedelta(days=1)
    # align to the Sunday that starts the week containing the 1st
    week_start = month_start - timedelta(days=(month_start.weekday() + 1) % 7)
    complete = 0
    while week_start <= month_end:
        days_in = sum(
            1 for i in range(7)
            if (week_start + timedelta(days=i)).year  == year
            and (week_start + timedelta(days=i)).month == month
        )
        if days_in >= 5:
            complete += 1
        week_start += timedelta(days=7)
    return max(complete, 1)


# ── GOOGLE SHEETS AUTH ────────────────────────────────────────

# Shared auth: service account (permanent) or self-healing OAuth — see google_auth.py
from google_auth import get_gspread_client


# ── AUTO-READ: all figures from Google Sheets ─────────────────

def fetch_sheet_data():
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)

    # ── MONTHLY_TARGET ────────────────────────────────────────
    # Row 1 = header: COLOUR | CATEGORY | PRODUCT NAME | BAG TYPE | TARGET | SALES | DEFICIT | ...
    # Wait — actual header: BAG TYPE | CATEGORY | TARGET(C) | SALES(D) | DEFICIT(E)
    # col C = TARGET, col D = SALES  (rows 2 onwards, skip header row 1)

    mt = sh.worksheet("MONTHLY_TARGET")

    col_c_raw = mt.col_values(3)   # column C — TARGET
    col_d_raw = mt.col_values(4)   # column D — SALES

    # Skip header (row 1); sum all numeric values
    def safe_sum(values):
        total = 0
        for v in values[1:]:            # [1:] skips the header row
            try:
                total += int(float(str(v).replace(",", "")))
            except (ValueError, TypeError):
                pass
        return total

    target_total = safe_sum(col_c_raw)   # sum of column C (TARGET)
    sales_total  = safe_sum(col_d_raw)   # sum of column D (SALES)

    # ── WEEKLY_SALES ──────────────────────────────────────────
    # Find the row where column C = "SUM TOTAL", read column X (24) = TOTAL

    ws = sh.worksheet("WEEKLY_SALES")
    col_c_ws = ws.col_values(3)          # column C

    weekly_total = 0
    for i, cell in enumerate(col_c_ws):
        if str(cell).strip().upper() == "SUM TOTAL":
            val = ws.cell(i + 1, 24).value   # column X = 24
            weekly_total = int(float(val)) if val else 0
            break
    else:
        print("  Warning: 'SUM TOTAL' not found in WEEKLY_SALES column C.")

    return target_total, sales_total, weekly_total


print("Fetching data from Google Sheets...")
total_target, total_sales, weekly_sales_total = fetch_sheet_data()


# ── DATE (auto-calculated) ────────────────────────────────────
# Sales are entered in the sheet the same evening, so by today the data
# covers every complete day through YESTERDAY. Complete days = yesterday's
# day-of-month.

yesterday       = date.today() - timedelta(days=1)
current_day     = max(yesterday.day, 1)
days_in_month   = calendar.monthrange(yesterday.year, yesterday.month)[1]
proj_ref        = yesterday

# Start-of-month rollover guard: in the first days of a new calendar month the
# sheet often still holds LAST month's full total (it hasn't been reset yet).
# Multiplying that by days_in_month ÷ current_day (e.g. ×31 on day 1) produces a
# nonsense projection (2225%). If the projection would be wildly over target this
# early, the data is still last month's — so project the PREVIOUS, completed
# month at 1× pace until the new month's data actually starts coming in.
if (current_day <= 6 and days_in_month and total_target
        and (total_sales * days_in_month / current_day) > total_target * 1.5):
    proj_ref      = yesterday.replace(day=1) - timedelta(days=1)   # last day of previous month
    current_day   = calendar.monthrange(proj_ref.year, proj_ref.month)[1]
    days_in_month = current_day

velocity_factor = days_in_month / current_day
proj_month      = proj_ref.strftime("%B")

# Perfect (complete) weeks in the month — used for the bare minimum
perfect_weeks = count_complete_weeks_in_month()


# ── CALCULATIONS ──────────────────────────────────────────────

# 1. Standard Projection
#    Step 1: total_sales × (days_in_month ÷ current_day)  → projected end-of-month bags
#    Step 2: ÷ total_target × 100                         → as % of target
standard_projection_pct = (total_sales * velocity_factor) / total_target * 100

# 2. Forecasted Projection
#    Step 1: (total_sales + corporate_bags) × (days_in_month ÷ current_day)
#    Step 2: ÷ total_target × 100                         → as % of target
forecasted_projection_pct = ((total_sales + corporate_bags) * velocity_factor) / total_target * 100

# 3. Bare Minimum = monthly target ÷ perfect weeks in the month
bare_minimum       = round(total_target / perfect_weeks) if perfect_weeks else 0
bare_minimum_value = bare_minimum

# 3b. Bare Minimum Growth %
bare_minimum_growth_pct = (bare_minimum / total_target) * 100 if total_target else 0

# 4. Declined By
declined_by = bare_minimum_value - weekly_sales_total if bare_minimum_value else 0


# ── WEEKLY PERFORMANCE SNAPSHOT ───────────────────────────────
# Record each Sun–Sat week's Sales / Weekly Sales / Declined By so the
# dashboard can show Week 1 → the latest week. One entry per week; the
# current week's row is refreshed each run until the week rolls over.
WEEKLY_HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "weekly_history.json")

def _week_start(d):                       # Sunday that starts d's week
    return d - timedelta(days=(d.weekday() + 1) % 7)

def _perfect_week_index(d):
    """Ordinal of d's Sun–Sat week within the month, counting EVERY week that has
    at least one day in the month — so the opening partial week is Week 1.
    (e.g. Jul 1–4 = Wk 1, Jul 5–11 = Wk 2, Jul 12–18 = Wk 3, ...)"""
    year, month = d.year, d.month
    ms = date(year, month, 1)
    me = (date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)) - timedelta(days=1)
    ws = ms - timedelta(days=(ms.weekday() + 1) % 7)
    target = _week_start(d)
    idx = 0
    while ws <= me:
        days_in = sum(1 for i in range(7)
                      if (ws + timedelta(days=i)).year == year
                      and (ws + timedelta(days=i)).month == month)
        if days_in >= 1:
            idx += 1
        if ws == target:
            return idx if days_in >= 1 else 0
        ws += timedelta(days=7)
    return idx

def update_weekly_history():
    ref = date.today() - timedelta(days=1)       # data covers through yesterday
    ws  = _week_start(ref)
    wk_idx = _perfect_week_index(ref)
    sales_pct = (total_sales / total_target * 100) if total_target else 0
    # Previous-period bags come from the snapshot current_performance keeps
    prev_bags = 0
    snap = os.path.join(os.path.dirname(os.path.abspath(__file__)), "previous_snapshot.json")
    if os.path.exists(snap):
        try:
            with open(snap, "r") as f:
                prev_bags = json.load(f).get("previous_week_bags", 0)
        except (ValueError, OSError):
            prev_bags = 0
    # Previous Sales % = the previous-sales bags as a share of the SAME target,
    # so the % column stays consistent with the bags column and trends week to week.
    prev_pct  = (prev_bags / total_target * 100) if total_target else 0
    entry = {
        "weekStart":    ws.isoformat(),
        "label":        ("Wk " + str(wk_idx)) if wk_idx else "Partial",
        "month":        ref.strftime("%b"),
        "salesPct":     round(sales_pct, 2),      # Sales % Achieved
        "salesBags":    total_sales,              # bags behind that %
        "prevSalesPct": round(prev_pct, 2),       # Previous Sales % Achieved
        "prevSalesBags": prev_bags,               # bags behind that %
        "weeklySales":  weekly_sales_total,       # bags sold this week (reference)
        "declinedBy":   weekly_sales_total - bare_minimum,  # +over / -under minimum
    }
    weeks = []
    if os.path.exists(WEEKLY_HISTORY_FILE):
        try:
            with open(WEEKLY_HISTORY_FILE, "r") as f:
                weeks = json.load(f).get("weeks", [])
        except (ValueError, OSError):
            # Corrupt/unparseable (e.g. a git merge conflict left markers in it).
            # Do NOT overwrite — that would wipe the whole trend history. Leave
            # the file for manual repair and skip this run's history update.
            print("  WARNING: weekly_history.json is unreadable (merge conflict?)."
                  " Leaving it untouched — fix the file, then re-run.")
            return []
    weeks = [w for w in weeks if w.get("weekStart") != entry["weekStart"]]
    weeks.append(entry)
    weeks.sort(key=lambda w: w.get("weekStart", ""))
    weeks = weeks[-16:]
    # Number the weeks 1..N within each month, in date order, so the opening
    # (partial) week is Wk 1 — even when it starts in the previous calendar month
    # (e.g. Jun 28 → "Jul" Wk 1). Keyed off each row's own "month" field.
    _month_counts = {}
    for w in weeks:
        m = w.get("month", "")
        _month_counts[m] = _month_counts.get(m, 0) + 1
        w["label"] = "Wk " + str(_month_counts[m])
    with open(WEEKLY_HISTORY_FILE, "w") as f:
        json.dump({"weeks": weeks}, f, indent=2)
    return weeks

weekly_history = update_weekly_history()


# ── FORMAT HELPERS ────────────────────────────────────────────

def fmt_int(n):
    return f"{n:,}"

def fmt_pct(p):
    return f"{p:.2f}%"

def fmt_signed(n):
    return f"+{n:,}" if n > 0 else f"{n:,}"


# ── INJECT INTO HTML ──────────────────────────────────────────

inline_script = (
    "<!-- PROJ_DATA_START -->\n"
    "<script>\n"
    "const PROJ = {\n"
    f'  currentDay:               {current_day},\n'
    f'  daysInMonth:              {days_in_month},\n'
    f'  projMonth:                "{proj_month}",\n'
    f'  velocityFactor:           "{velocity_factor:.2f}x",\n'
    f'  totalTarget:              "{fmt_int(total_target)}",\n'
    f'  totalSales:               "{fmt_int(total_sales)}",\n'
    f'  standardProjection:       "{fmt_pct(standard_projection_pct)}",\n'
    f'  forecastedProjection:     "{fmt_pct(forecasted_projection_pct)}",\n'
    f'  corporateBags:            "{fmt_int(corporate_bags)}",\n'
    f'  bareMinimum:              "{fmt_int(bare_minimum_value) if bare_minimum_value else ""}",\n'
    f'  bareMinimumGrowthPct:     "{fmt_pct(bare_minimum_growth_pct)}",\n'
    f'  declinedBy:               "{("-" + fmt_int(abs(declined_by))) if bare_minimum_value else ""}",\n'
    f'  weeklySalesTotal:         "{fmt_int(weekly_sales_total)}",\n'
    f'  weeklyHistory:            {json.dumps(weekly_history)}\n'
    "};\n"
    "</script>\n"
    "<!-- PROJ_DATA_END -->"
)

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
proj_html_path  = os.path.join(BASE_DIR, "forward_projections.html")
combined_path   = os.path.join(BASE_DIR, "current_performance.html")

def _inject(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(
        r"<!-- PROJ_DATA_START -->.*?<!-- PROJ_DATA_END -->",
        inline_script,
        content,
        flags=re.DOTALL
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

_inject(proj_html_path)   # keep standalone file up to date
_inject(combined_path)    # inject into the combined dashboard

# Refresh PERF data so both blocks are up to date before the browser opens.
# Skip when launched from main.py — it already runs current_performance.py
# right before this, so re-running here just wastes Google Sheets read quota.
if not os.environ.get("DENRI_LAUNCHER"):
    subprocess.run([sys.executable, os.path.join(BASE_DIR, "current_performance.py")], check=True)

if not os.environ.get("DENRI_LAUNCHER"):
    webbrowser.open_new_tab(pathlib.Path(combined_path).as_uri())

print("forward_projections data injected; dashboard updated.")
print(f"  Data through          : {yesterday.strftime('%d %b %Y')}  (day {current_day} of {days_in_month})")
print(f"  Velocity factor       : {velocity_factor:.2f}x")
print(f"  Total Target (col C)  : {fmt_int(total_target)}")
print(f"  Total Sales  (col D)  : {fmt_int(total_sales)}")
print(f"  Standard Proj.        : {fmt_pct(standard_projection_pct)}")
print(f"  Forecasted Proj.      : {fmt_pct(forecasted_projection_pct)}  (incl. {fmt_int(corporate_bags)} corporate)")
print(f"  Perfect weeks / month : {perfect_weeks}")
print(f"  Bare Minimum          : {fmt_int(bare_minimum_value)}  (= {fmt_int(total_target)} / {perfect_weeks})")
print(f"  Bare Min Growth %     : {fmt_pct(bare_minimum_growth_pct)}")
print(f"  Weekly Sales (col X)  : {fmt_int(weekly_sales_total)}")
print(f"  Declined By           : {'-' + fmt_int(abs(declined_by)) if bare_minimum_value else '(bare minimum not set)'}")
