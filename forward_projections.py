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

import re, webbrowser, os, pathlib, calendar, subprocess, sys
from datetime import date, timedelta

# ── SPREADSHEET ───────────────────────────────────────────────

SPREADSHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"


# ── MANUAL INPUTS — fill these in yourself ────────────────────

corporate_bags = 118+230     # Bags from corporate orders (Forecasted Projection)
bare_minimum   = 6400     # Minimum bags you need to sell this week


# ── GOOGLE SHEETS AUTH ────────────────────────────────────────

def get_gspread_client():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import gspread

    SCOPES     = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    CREDS_FILE = os.path.join(os.path.dirname(__file__), "google_credentials.json")
    TOKEN_FILE = os.path.join(os.path.dirname(__file__), "google_token.json")

    if not os.path.exists(CREDS_FILE):
        print()
        print("  !! google_credentials.json not found.")
        print("  Follow these steps once to set up access:")
        print("  1. Go to https://console.cloud.google.com/")
        print("  2. Create a project > APIs & Services > Enable 'Google Sheets API'")
        print("  3. APIs & Services > Credentials > Create OAuth client (Desktop app)")
        print("  4. Download the JSON and save it as:")
        print(f"     {CREDS_FILE}")
        print()
        raise FileNotFoundError("google_credentials.json missing.")

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return gspread.authorize(creds)


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
velocity_factor = days_in_month / current_day


# ── CALCULATIONS ──────────────────────────────────────────────

# 1. Standard Projection
#    Step 1: total_sales × (days_in_month ÷ current_day)  → projected end-of-month bags
#    Step 2: ÷ total_target × 100                         → as % of target
standard_projection_pct = (total_sales * velocity_factor) / total_target * 100

# 2. Forecasted Projection
#    Step 1: (total_sales + corporate_bags) × (days_in_month ÷ current_day)
#    Step 2: ÷ total_target × 100                         → as % of target
forecasted_projection_pct = ((total_sales + corporate_bags) * velocity_factor) / total_target * 100

# 3. Bare Minimum (entered manually above)
bare_minimum_value = bare_minimum

# 3b. Bare Minimum Growth %
bare_minimum_growth_pct = (bare_minimum / total_target) * 100 if total_target else 0

# 4. Declined By
declined_by = bare_minimum_value - weekly_sales_total if bare_minimum_value else 0


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
    f'  velocityFactor:           "{velocity_factor:.2f}x",\n'
    f'  totalTarget:              "{fmt_int(total_target)}",\n'
    f'  totalSales:               "{fmt_int(total_sales)}",\n'
    f'  standardProjection:       "{fmt_pct(standard_projection_pct)}",\n'
    f'  forecastedProjection:     "{fmt_pct(forecasted_projection_pct)}",\n'
    f'  corporateBags:            "{fmt_int(corporate_bags)}",\n'
    f'  bareMinimum:              "{fmt_int(bare_minimum_value) if bare_minimum_value else ""}",\n'
    f'  bareMinimumGrowthPct:     "{fmt_pct(bare_minimum_growth_pct)}",\n'
    f'  declinedBy:               "{("-" + fmt_int(abs(declined_by))) if bare_minimum_value else ""}",\n'
    f'  weeklySalesTotal:         "{fmt_int(weekly_sales_total)}"\n'
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
print(f"  Bare Minimum          : {fmt_int(bare_minimum_value) if bare_minimum_value else '(not set)'}")
print(f"  Bare Min Growth %     : {fmt_pct(bare_minimum_growth_pct)}")
print(f"  Weekly Sales (col X)  : {fmt_int(weekly_sales_total)}")
print(f"  Declined By           : {'-' + fmt_int(abs(declined_by)) if bare_minimum_value else '(bare minimum not set)'}")
