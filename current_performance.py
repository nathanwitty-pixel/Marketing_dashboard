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

from lib import report_month   # which month these figures belong to

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

def weekly_from_db(sheet_value):
    """Prefer the real current-week bags from Postgres (weekly_sales_db.json,
    written by weekly_sales.py) over the WEEKLY_SALES sheet tab, which has been
    unreliable (whole-month totals). Falls back to the sheet if the file is
    missing/unreadable or is for a different week."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weekly_sales_db.json")
    if not os.path.exists(path):
        return sheet_value
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("weekStart", "") == week_start_of(datetime.date.today()).isoformat():
            return int(round(float(data.get("weeklyBags", sheet_value))))
    except (ValueError, OSError, KeyError, TypeError):
        pass
    return sheet_value

def monthly_from_db(sheet_value):
    """Prefer the REPORTING month's real bags from Postgres (monthly_sales_db.json,
    written by monthly_sales.py) over the MONTHLY_TARGET sheet's SALES column.
    Applies only when the file is for the reporting month; otherwise (a past/frozen
    month, or the DB unreachable) falls back to the sheet value unchanged.

    The key is matched against the REPORTING month (lib/report_month.py), not
    today's — on the 1st those differ, and matching on today's is what let
    September's 8 bags land in the August report."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monthly_sales_db.json")
    if not os.path.exists(path):
        return sheet_value
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("monthKey", "") == report_month.live_month_key():
            return int(round(float(data.get("monthlyBags", sheet_value))))
    except (ValueError, OSError, KeyError, TypeError):
        pass
    return sheet_value

def master_from_db():
    """Reporting month's NET catalogue bags from Postgres (monthly_sales_db.json,
    written by monthly_sales.py). None if unavailable or not the reporting month."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monthly_sales_db.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("monthKey", "") == report_month.live_month_key():
            mb = data.get("masterBags")
            return int(mb) if mb is not None else None
    except (ValueError, OSError, KeyError, TypeError):
        pass
    return None

def reject_from_db():
    """Reporting month's reject-clearance bags ([REJECT] tag) from monthly_sales_db.json —
    the subset of Sales that were rejects. 0 if unavailable / not the reporting month."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "monthly_sales_db.json")
    if not os.path.exists(path):
        return 0
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("monthKey", "") == report_month.live_month_key():
            return int(data.get("rejectBags") or 0)
    except (ValueError, OSError, KeyError, TypeError):
        pass
    return 0

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
# Real current-week bags from Postgres when available (see weekly_sales.py);
# falls back to the WEEKLY_SALES sheet tab otherwise.
weekly_sales_total = weekly_from_db(weekly_sales_total)

# Real current-MONTH bags from Postgres when available (see monthly_sales.py);
# this is the total sales we've done in the month. Falls back to the sheet's
# SALES column for past months or when the DB/file isn't there.
total_sales = monthly_from_db(total_sales)

# Net catalogue bags (master-list products only) for the KPI card.
master_bags = master_from_db()

# Corporate bags (dynamic, from Odoo customer invoices — NOT the POS tills, so
# they're absent from Weekly Sales and Net Bags Sold, which stay POS-only).
# Added on top of POS in the Sales card only.
def corporate_from_db():
    """Current month's corporate bags, live from Odoo invoices. 0 when the DB
    isn't reachable so the Sales card gracefully shows POS-only."""
    try:
        from lib import db, queries
        ok, _ = db.check_connection()
        if not ok:
            return 0
        today   = datetime.date.today()
        m_start = today.replace(day=1)
        import calendar as _cal
        m_end   = today.replace(day=_cal.monthrange(today.year, today.month)[1])
        df = db.run_query(queries.CORPORATE_BAGS,
                          {"start_date": m_start.isoformat(),
                           "end_date":   m_end.isoformat()})
        if df is not None and not df.empty:
            return int(df.iloc[0]["bags"] or 0)
    except Exception:
        pass
    return 0

corporate_bags = corporate_from_db()
sales_pos      = total_sales                    # POS-only (Weekly / Net Bags basis)
total_sales    = total_sales + corporate_bags   # Sales card = POS + corporate

# Reject-clearance bags ([REJECT] tag) — a subset of the POS bags, so the Sales card can
# split "of N sold, R were rejects". % is of the POS total (rejects are POS, not corporate).
reject_bags = reject_from_db()
reject_pct  = (reject_bags / sales_pos * 100) if sales_pos else 0

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

# Stale-sheet guard: keep the straddle split alive when the calendar has moved
# past the straddle week but the sheet's weekly total is UNCHANGED — i.e. no new
# week's data has arrived yet, so all we still have is the straddle week (e.g.
# data through Aug 1 while the clock already says Aug 3). Anchored in the boundary
# file so the Weekly-vs-Last-Month split and per-day framing don't collapse.
_boundary = {}
try:
    with open(MONTH_BOUNDARY_FILE) as _bf:
        _boundary = json.load(_bf)
except (ValueError, OSError):
    _boundary = {}
_anchor = _boundary.get("straddle_anchor") or {}

if straddling:
    _anchor = {"week_total": weekly_sales_total,
               "data_date":  _data_date.isoformat(),
               "prev_month_weekly": prev_month_weekly}
elif (_anchor and prev_month_weekly
      and _anchor.get("week_total") == weekly_sales_total
      and weekly_sales_total > prev_month_weekly):
    straddling = True
    try:
        _data_date = datetime.date.fromisoformat(_anchor["data_date"])
    except (ValueError, KeyError):
        pass
else:
    _anchor = {}   # a new week's data has replaced the straddle week → drop the anchor

_boundary["straddle_anchor"] = _anchor
try:
    with open(MONTH_BOUNDARY_FILE, "w") as _bf:
        json.dump(_boundary, _bf, indent=2)
except OSError:
    pass

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

# Day-count split so the dashboard can compare PACE, not just totals — e.g.
# "Aug 1 alone (1 day) did 1,211" vs "July's final 6 days did 3,373". This turns
# a misleading 1-day-vs-many-days comparison into a fair per-day / weekly-potential read.
this_month_days = 0   # days of THIS month that have data inside the current week
prev_month_days = 0   # days the previous month contributed to the straddling week
if straddling and prev_month_rec and prev_month_rec.get("recorded_on"):
    try:
        _wk_start = week_start_of(_data_date)
        _prev_end = _data_date.replace(day=1) - datetime.timedelta(days=1)  # last day of prev month
        this_month_days = _data_date.day                                    # e.g. Aug 1 → 1
        prev_month_days = max((_prev_end - _wk_start).days + 1, 0)          # e.g. Jul 26–31 → 6
    except ValueError:
        this_month_days = prev_month_days = 0


# ── CALCULATIONS ──────────────────────────────────────────────

# 1. Remaining Target
#    The number of bags still needed to reach the full target.
#    Target comes from the sheet (col C); sales is the Odoo month total, so
#    remaining = sheet target − Odoo sales (floored at 0). This replaces the
#    sheet's col-E deficit, which was computed off the sheet's own sales and
#    would ignore the Postgres figure.
remaining_target = max(total_target - total_sales, 0)

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


# ── Previous month's weekly climb (for the Sept-vs-Aug comparison line) ──
# Same per-week "% of target" series the monthly report overlays: this month
# solid, last month dashed. Read from monthly_report_history.json.
_cp_prev_weekly, _cp_prev_label, _cp_cur_label = [], "", "This month"
try:
    _lk = report_month.live_month_key()          # e.g. "2026-09"
    _ly, _lm = int(_lk[:4]), int(_lk[5:7])
    _pm_num  = _lm - 1 if _lm > 1 else 12
    _pm_year = _ly if _lm > 1 else _ly - 1
    _pm_key  = f"{_pm_year}-{_pm_num:02d}"
    _hist_p  = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "monthly_report_history.json")
    import calendar as _cpcal
    _cp_cur_label = f"{_cpcal.month_name[_lm]} {_ly}"
    with open(_hist_p, encoding="utf-8") as _pf:
        _pm_snap = json.load(_pf).get(_pm_key)
    if _pm_snap:
        _cp_prev_weekly = [{"label": w.get("label", ""),
                            "pct": round(float(w.get("pct") or 0), 2)}
                           for w in _pm_snap.get("currentPerformance", {}).get("weekly", [])]
        _cp_prev_label = f"{_pm_snap.get('month', '')} {_pm_snap.get('year', '')}".strip()
except (ValueError, OSError, KeyError, TypeError):
    pass


# ── INJECT INTO HTML ──────────────────────────────────────────

inline_script = (
    "<!-- PERF_DATA_START -->\n"
    "<script>\n"
    "const PERF = {\n"
    f'  cpPrevWeekly:       {json.dumps(_cp_prev_weekly)},\n'
    f'  cpPrevLabel:        "{_cp_prev_label}",\n'
    f'  cpCurLabel:         "{_cp_cur_label}",\n'
    f'  remainingTarget:    "{fmt_int(remaining_target)}",\n'
    f'  salesPctAchieved:   "{fmt_pct(sales_pct_achieved)}",\n'
    f'  sales:              "{fmt_int(sales)}",\n'
    f'  salesPos:           "{fmt_int(sales_pos)}",\n'
    f'  corporateBags:      "{fmt_int(corporate_bags)}",\n'
    f'  rejectBags:         "{fmt_int(reject_bags)}",\n'
    f'  rejectPct:          "{fmt_pct(reject_pct)}",\n'
    f'  masterBags:         "{fmt_int(master_bags) if master_bags is not None else "—"}",\n'
    f'  previousSalesPct:   "{fmt_pct(previous_sales_pct)}",\n'
    f'  previousSalesBags:  "{fmt_int(previous_sales_bags)}",\n'
    f'  wowSalesPct:        "{fmt_signed_pct(wow_sales_pct)}",\n'
    f'  wowSalesBags:       "{fmt_signed(wow_sales_bags)}",\n'
    f'  weeklySalesTotal:   "{fmt_int(weekly_sales_total)}",\n'
    f'  weeklySalesPct:     "{fmt_pct(weekly_sales_pct)}",\n'
    f'  growthHistory:      {json.dumps(growth_history)},\n'
    f'  weeklyThisMonth:    "{fmt_int(weekly_this_month)}",\n'
    f'  weeklyThisMonthDays: {this_month_days},\n'
    f'  prevMonthDays:      {prev_month_days},\n'
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
print(f"  Total Target (sheet) : {fmt_int(total_target)}")
print(f"  POS Sales    (Odoo)  : {fmt_int(sales_pos)}")
print(f"  Corporate    (invoices): {fmt_int(corporate_bags)}")
print(f"  Sales (POS+corp)     : {fmt_int(total_sales)}")
print(f"  Sheet Deficit (col E): {fmt_int(total_deficit)}")
print(f"  Remaining (tgt-sales): {fmt_int(remaining_target)}")
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
