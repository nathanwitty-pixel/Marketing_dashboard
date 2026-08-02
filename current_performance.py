"""
current_performance.py
─────────────────────────────────────────────────────────────────
Run:
    python current_performance.py

Reads live from Google Sheets:

  MONTHLY_TARGET sheet
    col C (TARGET)  → sum all rows below header  →  total_target
    col D (SALES)   → sum all rows below header  →  total_sales
    col E (DEFICIT) → sum all rows below header  →  total_deficit
─────────────────────────────────────────────────────────────────
"""

import re, os, json, datetime

# ── SPREADSHEET ───────────────────────────────────────────────

SPREADSHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"


# ── MANUAL INPUTS — fill these in yourself ────────────────────

bare_minimum = 0   # minimum bags target for the week (0 = not set)


# ── SNAPSHOT: auto-load previous period values ────────────────

SNAPSHOT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "previous_snapshot.json")

def load_snapshot():
    if os.path.exists(SNAPSHOT_FILE):
        with open(SNAPSHOT_FILE, "r") as f:
            data = json.load(f)
        current_iso_week = datetime.date.today().isocalendar()[1]
        saved_week       = data.get("saved_week")
        current_bags     = data.get("current_week_bags", 0)
        previous_bags    = data.get("previous_week_bags", 0)
        # New week: roll current → previous automatically
        if saved_week is not None and saved_week != current_iso_week:
            previous_bags = current_bags
        return current_bags, previous_bags
    return 0, 0

def save_snapshot(current_bags, previous_bags):
    current_iso_week = datetime.date.today().isocalendar()[1]
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump({
            "current_week_bags":  current_bags,
            "previous_week_bags": previous_bags,
            "saved_week":         current_iso_week
        }, f)

_, previous_sales_bags = load_snapshot()


# ── MONTH-BOUNDARY SNAPSHOT ───────────────────────────────────
# The WEEKLY_SALES sheet runs Sunday → Saturday, so the week that spans a
# month change mixes old-month and new-month bags (e.g. the first week of
# July had Sun 28 – Tue 30 June in it). Every run we record the weekly
# total with its week-start date; on the first run of a new month, the
# last value recorded in the old month becomes the "carryover" — the bags
# that belong to the previous month. While we're still inside that
# straddling week, weekly_this_month = sheet total − carryover.

MONTH_BOUNDARY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "month_boundary.json")

def week_start_of(d):
    """Sunday that starts the Sun–Sat sales week containing d."""
    return d - datetime.timedelta(days=(d.weekday() + 1) % 7)

def update_month_boundary(weekly_total):
    """Update the rolling snapshot.
    Returns (carryover_bags | None, captured_on, prev_month_record)."""
    today     = datetime.date.today()
    wk_start  = week_start_of(today).isoformat()
    month_key = today.strftime("%Y-%m")

    data = {}
    if os.path.exists(MONTH_BOUNDARY_FILE):
        try:
            with open(MONTH_BOUNDARY_FILE, "r") as f:
                data = json.load(f)
        except (ValueError, OSError):
            data = {}

    last  = data.get("last_run") or {}
    carry = data.get("carryover") or {}
    prev  = data.get("prev_month") or {}

    # Month changed since the last run → the old month's final weekly figure
    # is whatever the last run recorded. Keep it permanently for the
    # month-over-month weekly KPI.
    if last and last.get("date", "")[:7] != month_key:
        prev = {
            "month":              last.get("date", "")[:7],
            "final_weekly_sales": last.get("weekly_sales_total", 0),
            "recorded_on":        last.get("date", ""),
        }
        # Carryover only when the last run was in the SAME Sun–Sat week
        # (the week straddles the boundary)
        if last.get("week_start") == wk_start:
            carry = {
                "month":             month_key,
                "week_start":        wk_start,
                "bags_before_month": last.get("weekly_sales_total", 0),
                "captured_on":       last.get("date", ""),
            }
        else:
            carry = {}   # boundary fell between weeks — clean cut, no mixing

    # Carryover only applies while we're still inside the straddling week
    if carry and (carry.get("month") != month_key or carry.get("week_start") != wk_start):
        carry = {}

    data["last_run"] = {
        "date":               today.isoformat(),
        "week_start":         wk_start,
        "weekly_sales_total": weekly_total,
    }
    data["carryover"]  = carry
    data["prev_month"] = prev
    with open(MONTH_BOUNDARY_FILE, "w") as f:
        json.dump(data, f, indent=2)

    if carry:
        return carry.get("bags_before_month", 0), carry.get("captured_on", ""), prev
    return None, "", prev


# ── GOOGLE SHEETS AUTH ────────────────────────────────────────

# Shared auth: service account (permanent) or self-healing OAuth — see google_auth.py
from google_auth import get_gspread_client


# ── AUTO-READ: totals from MONTHLY_TARGET sheet ───────────────

def fetch_monthly_target():
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)

    # ── MONTHLY_TARGET ────────────────────────────────────────
    mt = sh.worksheet("MONTHLY_TARGET")

    col_c_raw = mt.col_values(3)   # column C — TARGET
    col_d_raw = mt.col_values(4)   # column D — SALES
    col_e_raw = mt.col_values(5)   # column E — DEFICIT

    def safe_sum(values):
        total = 0
        for v in values[1:]:
            try:
                total += int(float(str(v).replace(",", "")))
            except (ValueError, TypeError):
                pass
        return total

    target_total  = safe_sum(col_c_raw)
    sales_total   = safe_sum(col_d_raw)
    deficit_total = safe_sum(col_e_raw)

    # ── WEEKLY_SALES ──────────────────────────────────────────
    # Find the row where col C = "SUM TOTAL", read col X (24) = TOTAL
    ws       = sh.worksheet("WEEKLY_SALES")
    col_c_ws = ws.col_values(3)

    weekly_total = 0
    for i, cell in enumerate(col_c_ws):
        if str(cell).strip().upper() == "SUM TOTAL":
            val = ws.cell(i + 1, 24).value   # col X = 24
            weekly_total = int(float(val)) if val else 0
            break
    else:
        print("  Warning: 'SUM TOTAL' not found in WEEKLY_SALES column C.")

    return target_total, sales_total, deficit_total, weekly_total


print("Fetching data from Google Sheets...")
print(f"  Previous snapshot    : {previous_sales_bags:,} bags")
total_target, total_sales, total_deficit, weekly_sales_total = fetch_monthly_target()

# Month-boundary handling: split the straddling week's total by month.
carryover_bags, carryover_date, prev_month_rec = update_month_boundary(weekly_sales_total)
prev_month_weekly = prev_month_rec.get("final_weekly_sales", 0) if prev_month_rec else 0

# Are we still inside the Sun–Sat week that straddled the month boundary?
# Derive it from the persisted prev_month record (its final run's week) vs
# today's week — NOT from the fragile carryover dict, so a mistimed run in the
# following week can't wipe the split. While straddling, this month's slice =
# week total − last month's final weekly (e.g. Aug 1 alone vs Jul 27–31).
_today = datetime.date.today()
_data_date = _today - datetime.timedelta(days=1)   # sales data covers through yesterday
straddling = False
if prev_month_rec and prev_month_rec.get("recorded_on") and prev_month_weekly:
    try:
        straddling = (week_start_of(datetime.date.fromisoformat(prev_month_rec["recorded_on"]))
                      == week_start_of(_data_date))
    except ValueError:
        straddling = False

if straddling:
    carryover_bags    = prev_month_weekly                              # last month's part of this week
    carryover_date    = prev_month_rec.get("recorded_on", "")
    weekly_this_month = max(weekly_sales_total - prev_month_weekly, 0)  # this month's part (e.g. Aug 1 alone)
    _prev_month = datetime.datetime.strptime(prev_month_rec["month"] + "-01", "%Y-%m-%d").strftime("%B")
else:
    weekly_this_month = weekly_sales_total
    _prev_month = ""

prev_month_label  = ""
if prev_month_rec and prev_month_rec.get("month"):
    try:
        prev_month_label = datetime.datetime.strptime(
            prev_month_rec["month"] + "-01", "%Y-%m-%d").strftime("%B")
    except ValueError:
        prev_month_label = prev_month_rec["month"]

# Weekly vs Last Month: this month's weekly slice vs last month's final weekly.
mom_weekly_bags = weekly_this_month - prev_month_weekly
mom_weekly_pct  = ((weekly_this_month - prev_month_weekly) / prev_month_weekly * 100) if prev_month_weekly else 0


# ── CALCULATIONS ──────────────────────────────────────────────

# 1. Remaining Target
#    The number of bags still needed to reach the full target.
#    Taken directly from column E (DEFICIT) sum.
remaining_target = total_deficit

# 2. Sales % Achieved
#    How much of the target has been sold so far, as a percentage.
#    Formula: total_sales ÷ total_target × 100
sales_pct_achieved = (total_sales / total_target) * 100

# 3. Sales
#    The raw count of bags sold — straight from column D sum.
sales = total_sales

# 4. Previous Sales % Achieved
#    (Sales - Weekly Sales) / (Remaining Target + Sales) × 100
previous_sales_pct = ((total_sales - weekly_sales_total) / (remaining_target + total_sales)) * 100 if (remaining_target + total_sales) else 0

# 5. Week-over-Week Sales
#    Growth of this week vs last week: (this week - last week) / last week × 100.
#    Sign matches the bag change — up = positive (green), down = negative (red).
wow_sales_bags = weekly_sales_total - previous_sales_bags
wow_sales_pct  = (wow_sales_bags / previous_sales_bags * 100) if previous_sales_bags else 0

# 6. Growth % Towards Achieved Monthly Sales
#    How much Sales % Achieved grew this week: Sales % Achieved - Previous Sales % Achieved
weekly_sales_pct = sales_pct_achieved - previous_sales_pct

# 7. Declined By
declined_by = bare_minimum - weekly_sales_total if bare_minimum else 0


# ── GROWTH TREND HISTORY ──────────────────────────────────────
# Record the weekly growth % each run so the dashboard can draw a trend
# line over time. One point per day (latest run of the day wins).
GROWTH_HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "growth_history.json")

def update_growth_history(growth_pct):
    today = datetime.date.today().isoformat()
    points = []
    if os.path.exists(GROWTH_HISTORY_FILE):
        try:
            with open(GROWTH_HISTORY_FILE, "r") as f:
                points = json.load(f).get("points", [])
        except (ValueError, OSError):
            points = []
    points = [p for p in points if p.get("date") != today]
    points.append({"date": today, "growth": round(growth_pct, 2)})
    points.sort(key=lambda p: p.get("date", ""))
    points = points[-120:]
    with open(GROWTH_HISTORY_FILE, "w") as f:
        json.dump({"points": points}, f, indent=2)
    return points

growth_history = update_growth_history(weekly_sales_pct)


# ── FORMAT HELPERS ────────────────────────────────────────────

def fmt_int(n):
    return f"{n:,}"

def fmt_pct(p):
    return f"{p:.2f}%"

def fmt_signed(n):
    return f"+{n:,}" if n > 0 else f"{n:,}"   # negatives already carry "-"

def fmt_signed_pct(p):
    return f"+{p:.2f}%" if p > 0 else f"{p:.2f}%"


# ── INJECT INTO HTML ──────────────────────────────────────────

inline_script = (
    "<!-- PERF_DATA_START -->\n"
    "<script>\n"
    "const PERF = {\n"
    f'  remainingTarget:    "{fmt_int(remaining_target)}",\n'
    f'  salesPctAchieved:   "{fmt_pct(sales_pct_achieved)}",\n'
    f'  sales:              "{fmt_int(sales)}",\n'
    f'  previousSalesPct:   "{fmt_pct(previous_sales_pct)}",\n'
    f'  previousSalesBags:  "{fmt_int(previous_sales_bags)}",\n'
    f'  wowSalesPct:        "{fmt_signed_pct(wow_sales_pct)}",\n'
    f'  wowSalesBags:       "{fmt_signed(wow_sales_bags)}",\n'
    f'  weeklySalesTotal:   "{fmt_int(weekly_sales_total)}",\n'
    f'  weeklySalesPct:     "{fmt_pct(weekly_sales_pct)}",\n'
    f'  growthHistory:      {json.dumps(growth_history)},\n'
    f'  weeklyThisMonth:    "{fmt_int(weekly_this_month)}",\n'
    f'  weeklyCarryover:    "{fmt_int(carryover_bags) if carryover_bags is not None else ""}",\n'
    f'  carryoverMonth:     "{_prev_month}",\n'
    f'  carryoverDate:      "{carryover_date}",\n'
    f'  prevMonthWeekly:    "{fmt_int(prev_month_weekly) if prev_month_weekly else ""}",\n'
    f'  prevMonthLabel:     "{prev_month_label}",\n'
    f'  momWeeklyBags:      "{("+" if mom_weekly_bags > 0 else "") + fmt_int(mom_weekly_bags) if prev_month_weekly else ""}",\n'
    f'  momWeeklyPct:       "{("+" if mom_weekly_pct > 0 else "") + fmt_pct(mom_weekly_pct) if prev_month_weekly else ""}",\n'
    f'  bareMinimum:        "{fmt_int(bare_minimum) if bare_minimum else ""}",\n'
    f'  declinedBy:         "{("-" + fmt_int(abs(declined_by))) if bare_minimum else ""}"\n'
    "};\n"
    "</script>\n"
    "<!-- PERF_DATA_END -->"
)

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE_DIR, "current_performance.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

html = re.sub(
    r"<!-- PERF_DATA_START -->.*?<!-- PERF_DATA_END -->",
    inline_script,
    html,
    flags=re.DOTALL
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

save_snapshot(weekly_sales_total, previous_sales_bags)
print("current_performance.html updated.")
print(f"  Total Target (col C) : {fmt_int(total_target)}")
print(f"  Total Sales  (col D) : {fmt_int(total_sales)}")
print(f"  Total Deficit (col E): {fmt_int(total_deficit)}")
print(f"  Remaining Target     : {fmt_int(remaining_target)}")
print(f"  Sales % Achieved     : {fmt_pct(sales_pct_achieved)}")
print(f"  Sales                : {fmt_int(sales)}")
print(f"  Previous Sales %     : {fmt_pct(previous_sales_pct)}")
print(f"  Previous Sales bags  : {fmt_int(previous_sales_bags)}")
print(f"  WoW Sales %          : {fmt_pct(wow_sales_pct)}")
print(f"  WoW Sales bags       : {fmt_int(wow_sales_bags)}")
print(f"  Weekly Sales Total   : {fmt_int(weekly_sales_total)}")
print(f"  Weekly Sales %       : {fmt_pct(weekly_sales_pct)}")
if carryover_bags is not None:
    print(f"  Month carryover      : {fmt_int(carryover_bags)} bags belong to {_prev_month} (snapshot {carryover_date})")
    print(f"  Weekly (this month)  : {fmt_int(weekly_this_month)}")
if prev_month_weekly:
    print(f"  {prev_month_label} final weekly   : {fmt_int(prev_month_weekly)}")
    print(f"  MoM weekly           : {fmt_pct(mom_weekly_pct)} ({fmt_int(mom_weekly_bags)} bags)")
