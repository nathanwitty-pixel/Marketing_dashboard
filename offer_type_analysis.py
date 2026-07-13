"""
offer_type_analysis.py
─────────────────────────────────────────────────────────────────
Reads live from Google Sheets (three sheets) — KENYA focus:

  COMBOS         → B3:K12 = JUNE COMBOS
                   col B (range idx 0) = combo name
                   col K (range idx 9) = price

  MONTHLY_TARGET → col F (idx 5) = offer flag ✅
                   if flagged: return col A (idx 0), col B (idx 1)

  STOCK_LEVELS   → filtered where col D (idx 3) = BAG TYPE matches
                   MONTHLY_TARGET col A offer products
                   return col A=COLOUR, col B=CATEGORY,
                          col C=PRODUCT NAME, col Y(idx 24)=KENYA stock
─────────────────────────────────────────────────────────────────
"""

import re, webbrowser, os, pathlib, json

# ── SPREADSHEET ───────────────────────────────────────────────

SPREADSHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"


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


# ── HELPERS ───────────────────────────────────────────────────

def safe_int(val):
    try:
        return int(float(str(val).replace(",", "")))
    except (ValueError, TypeError):
        return 0

def is_checked(val):
    v = str(val).strip()
    return (
        '✅' in v or   # ✅
        '✔' in v or   # ✔
        '✓' in v or   # ✓
        v.upper() in ('TRUE', '1', 'YES')
    )

def fmt_int(n):
    return f"{n:,}"

def fmt_price(raw):
    try:
        return f"{float(str(raw).replace(',', '')):,.0f}"
    except (ValueError, TypeError):
        return str(raw).strip()


# ── FETCH ─────────────────────────────────────────────────────

def fetch_offer_data():
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)

    # ── COMBOS ────────────────────────────────────────────────
    # The sheet layout shifts every month (JUNE COMBOS → JULY COMBOS, rows
    # move around), so instead of fixed cell ranges we fetch the live area
    # once and locate each section by its marker text, reading each table
    # from its header row down to its TOTAL row.
    combos_ws = sh.worksheet("COMBOS")
    grid = combos_ws.get("A1:M150")   # cols A..M — June archive lives in N..P

    def cell(r, c):
        row = grid[r] if 0 <= r < len(grid) else []
        return str(row[c]).strip() if c < len(row) else ''

    def find_row(col_idx, needle, start=0, contains=False):
        """0-based row index whose cell in col_idx matches needle."""
        n = needle.upper()
        for r in range(start, len(grid)):
            v = cell(r, col_idx).upper()
            if (contains and n in v) or v == n:
                return r
        return None

    def find_row_any(needle, start=0, contains=False, max_col=13):
        """Like find_row but scans every column — section titles move
        around (e.g. POWER DEALS moved from col B to col D)."""
        n = needle.upper()
        for r in range(start, len(grid)):
            for c in range(max_col):
                v = cell(r, c).upper()
                if (contains and n in v) or v == n:
                    return r
        return None

    SECTION_KEYWORDS = ('COMBO', 'POWER', 'SINGLE', 'SALE', 'SPECIAL', 'OFFER')

    def section_name_col(header_r):
        """Column holding the section title / product names. Price columns
        may now sit BEFORE it (B=PRICE, C=TSH, D=name)."""
        if header_r is None:
            return None
        for c in range(1, 13):
            v = cell(header_r, c).upper()
            if v and any(k in v for k in SECTION_KEYWORDS):
                return c
        for c in range(1, 13):
            v = cell(header_r, c).upper()
            if v and v != 'PRICE':
                return c
        return None

    def section_title(header_r):
        c = section_name_col(header_r)
        return cell(header_r, c) if c is not None else ''

    def section_raw(header_r, first_col=1, last_col=12):
        """Rows from the header row down to (and incl.) the TOTAL row.
        Columns are reordered to: name, price column(s), then the week /
        total columns — so tables render name-first even though the sheet
        now puts PRICE in front (cols B/C)."""
        if header_r is None:
            return []
        name_c = section_name_col(header_r)
        if name_c is None:
            return []
        price_cols = list(range(first_col, name_c))
        cols = [name_c] + price_cols + list(range(name_c + 1, last_col + 1))
        out = []
        for r in range(header_r, min(header_r + 40, len(grid))):
            vals = [cell(r, c) for c in cols]
            out.append(vals)
            if r > header_r and vals and 'TOTAL' in vals[0].upper():
                break
        # Name blank price-column headers so process_table doesn't
        # auto-label them as week columns
        for i in range(1, 1 + len(price_cols)):
            if i < len(out[0]) and not out[0][i]:
                out[0][i] = 'PRICE (TSH)' if i > 1 else 'PRICE'
        return out

    def process_table(raw):
        """Return (headers, rows).
        Keeps every column; blank-header columns between name and price are
        auto-named Wk 1, Wk 2, … so week data is never lost.
        Drops columns (except col 0) with no data — hides future empty weeks."""
        if not raw:
            return [], []
        all_headers = [str(c).strip() for c in raw[0]]
        ncols = len(all_headers)

        # Split data rows from the TOTAL row
        data_raw  = []
        total_raw = None
        for row in raw[1:]:
            padded = [str(row[i]).strip() if i < len(row) else '' for i in range(ncols)]
            if any(padded):
                if 'TOTAL' in padded[0].upper():
                    total_raw = padded
                else:
                    data_raw.append(padded)

        def col_has_data(col_idx):
            for padded in data_raw:
                val = padded[col_idx] if col_idx < len(padded) else ''
                try:
                    if float(str(val).replace(',', '')) != 0:
                        return True
                except (ValueError, TypeError):
                    if val:
                        return True
            return False

        # Always keep col 0 (name); drop any other column with no data
        keep = [i for i in range(ncols) if i == 0 or col_has_data(i)]

        # Build headers: blank cols get auto-names (Wk 1, Wk 2, …)
        wk = 0
        headers = []
        for i in keep:
            h = all_headers[i]
            if not h:
                if i == 0:
                    h = "Name"
                else:
                    wk += 1
                    h = f"Wk {wk}"
            headers.append(h)

        rows = []
        for padded in data_raw:
            filtered = [padded[i] if i < len(padded) else '' for i in keep]
            if any(filtered):
                rows.append(filtered)
        if total_raw is not None:
            rows.append([total_raw[i] if i < len(total_raw) else '' for i in keep])

        return headers, rows

    # ── Locate section markers (row positions shift every month) ──
    kenya_r  = find_row(0, "KENYA")                            # col A
    pd_r     = find_row_any("POWER DEALS", contains=True)      # any col
    sinza_r  = find_row(0, "SINZA")                            # col A
    ug_r     = find_row(0, "UGANDA")                           # col A

    # Month label comes from the sheet itself, e.g. "JULY COMBOS" → "July"
    kenya_title = section_title(kenya_r)
    month_name  = kenya_title.split()[0].capitalize() if kenya_title else ""

    # Kenya Combos: header row + data until TOTAL
    june_combo_headers, june_combos = process_table(section_raw(kenya_r))

    # Power Deals: header row + data until TOTAL
    power_deal_headers, power_deals = process_table(section_raw(pd_r))

    print(f"  Month detected    : {month_name or '(not found)'}")
    print(f"  {month_name} Combos found : {len(june_combos)}")
    print(f"  Power Deals found : {len(power_deals)}")

    # ── MONTHLY_TARGET: col F offer flag ──────────────────────
    # col A (idx 0) = BAG TYPE
    # col B (idx 1) = CATEGORY
    # col F (idx 5) = OFFER flag ✅

    mt      = sh.worksheet("MONTHLY_TARGET")
    mt_rows = mt.get_all_values()

    offer_products = []   # [{bagType, category}]
    offer_set      = set()   # bag_upper keys for STOCK_LEVELS filter
    bag_targets    = {}   # BAG_UPPER -> {target, sold, remaining}  (from cols C/D/E)

    for row in mt_rows[1:]:
        if len(row) < 6:
            continue
        bag = str(row[0]).strip()
        # Capture the monthly target for EVERY bag (needed for combo/power targets)
        if bag:
            t   = safe_int(row[2]) if len(row) > 2 else 0   # col C = TARGET
            s   = safe_int(row[3]) if len(row) > 3 else 0   # col D = SALES
            dfc = safe_int(row[4]) if len(row) > 4 else 0   # col E = DEFICIT
            bag_targets[bag.upper()] = {
                "target": t, "sold": s,
                "remaining": dfc if dfc else max(t - s, 0),
            }
        if is_checked(row[5]):   # col F
            category = str(row[1]).strip()
            if bag:
                offer_products.append({"bagType": bag, "category": category})
                offer_set.add(bag.upper())

    print(f"  Offer products    : {len(offer_products)}")
    for p in offer_products:
        print(f"    - {p['bagType']}  ({p['category']})")

    # ── STOCK_LEVELS ──────────────────────────────────────────
    # Filter where col D (idx 3) = BAG TYPE is in offer_set
    # col A (idx  0) = COLOUR
    # col B (idx  1) = CATEGORY
    # col C (idx  2) = PRODUCT NAME
    # col D (idx  3) = BAG TYPE  ← filter key
    # col Y (idx 24) = KENYA stock

    sl      = sh.worksheet("STOCK_LEVELS")
    sl_rows = sl.get_all_values()

    stock_data       = []
    total_kenya_stock = 0

    for row in sl_rows[1:]:
        if len(row) < 4:
            continue
        bag_type = str(row[3]).strip()   # col D
        if not bag_type or bag_type.upper() not in offer_set:
            continue
        colour       = str(row[0]).strip()   # col A
        category     = str(row[1]).strip()   # col B
        product_name = str(row[2]).strip()   # col C
        kenya_stock  = safe_int(row[24]) if len(row) > 24 else 0   # col Y

        stock_data.append({
            "colour":      colour,
            "category":    category,
            "productName": product_name,
            "bagType":     bag_type,
            "kenyaStock":  kenya_stock
        })
        total_kenya_stock += kenya_stock

    print(f"  Stock rows        : {len(stock_data)}")
    print(f"  Total Kenya stock : {fmt_int(total_kenya_stock)}")

    # ── UGANDA ────────────────────────────────────────────────
    # One live table now (e.g. "JULY SALE" at the UGANDA marker); the old
    # June combos/singles layout is archived in cols N..P which we ignore.
    ug_title = section_title(ug_r).title()   # e.g. "July Sale"
    ug_combo_headers, ug_combos = process_table(section_raw(ug_r))

    # No separate Uganda singles table in the current layout
    ug_singles_headers, ug_singles = [], []

    print(f"  Uganda '{ug_title}' rows : {len(ug_combos)}")

    # Uganda Stock: col A (colour), B (category), C (product name), D (bag type), S idx 18
    ug_stock_data = []
    total_uganda_stock = 0

    for row in sl_rows[1:]:
        if len(row) < 19:
            continue
        colour       = str(row[0]).strip()
        category     = str(row[1]).strip()
        product_name = str(row[2]).strip()
        bag_type     = str(row[3]).strip()
        uganda_stock = safe_int(row[18])   # col S = UGANDA
        if not bag_type and not product_name:
            continue
        ug_stock_data.append({
            "colour":      colour,
            "category":    category,
            "productName": product_name,
            "bagType":     bag_type,
            "ugandaStock": uganda_stock
        })
        total_uganda_stock += uganda_stock

    print(f"  Uganda Stock rows    : {len(ug_stock_data)}")
    print(f"  Total Uganda stock   : {fmt_int(total_uganda_stock)}")

    # ── SINZA ─────────────────────────────────────────────────
    # Combos at the SINZA marker; SINGLES and SPECIAL tables (if present)
    # are located below it by their own title cells (any column).
    sinza_combo_headers, sinza_combos = process_table(section_raw(sinza_r))

    # Sinza combo NAMES are maintained in a separate column (AK372:AK381);
    # override the parsed names with those, matched positionally to the data rows.
    try:
        ak_vals  = combos_ws.get("AK372:AK381")
        ak_names = [str(row[0]).strip() if row else '' for row in ak_vals]
        di = 0
        for row in sinza_combos:
            if row and str(row[0]).strip().upper().startswith("TOTAL"):
                continue
            if di < len(ak_names) and ak_names[di]:
                row[0] = ak_names[di]
            di += 1
        print(f"  Sinza combo names from AK: {len([n for n in ak_names if n])}")
    except Exception as e:
        print(f"  (Sinza AK names skipped: {e})")

    singles_r = find_row_any("SINGLES", start=(sinza_r or 0) + 1) if sinza_r is not None else None
    sinza_singles_headers, sinza_singles = process_table(section_raw(singles_r))

    specials_r = (find_row_any("SPECIAL", start=(sinza_r or 0) + 1, contains=True)
                  if sinza_r is not None else None)
    sinza_special_headers, sinza_specials = process_table(section_raw(specials_r))

    print(f"  Sinza Combos found   : {len(sinza_combos)}")
    print(f"  Sinza Singles found  : {len(sinza_singles)}")
    print(f"  Sinza Specials found : {len(sinza_specials)}")

    # Sinza Stock: col A–D + col R (idx 17)
    sinza_stock_data = []
    total_sinza_stock = 0

    for row in sl_rows[1:]:
        if len(row) < 18:
            continue
        colour       = str(row[0]).strip()
        category     = str(row[1]).strip()
        product_name = str(row[2]).strip()
        bag_type     = str(row[3]).strip()
        sinza_stock  = safe_int(row[17])   # col R = SINZA
        if not bag_type and not product_name:
            continue
        sinza_stock_data.append({
            "colour":      colour,
            "category":    category,
            "productName": product_name,
            "bagType":     bag_type,
            "sinzaStock":  sinza_stock
        })
        total_sinza_stock += sinza_stock

    print(f"  Sinza Stock rows     : {len(sinza_stock_data)}")
    print(f"  Total Sinza stock    : {fmt_int(total_sinza_stock)}")

    return (month_name, ug_title,
            june_combo_headers, june_combos,
            power_deal_headers, power_deals,
            offer_products, stock_data, total_kenya_stock,
            ug_combo_headers, ug_combos,
            ug_singles_headers, ug_singles,
            ug_stock_data, total_uganda_stock,
            sinza_combo_headers, sinza_combos,
            sinza_singles_headers, sinza_singles,
            sinza_special_headers, sinza_specials,
            sinza_stock_data, total_sinza_stock,
            bag_targets)


# ── RUN ───────────────────────────────────────────────────────

print("Fetching Offer Type Analysis data...")
(month_name, ug_title,
 june_combo_headers, june_combos,
 power_deal_headers, power_deals,
 offer_products, stock_data, total_kenya_stock,
 ug_combo_headers, ug_combos,
 ug_singles_headers, ug_singles,
 ug_stock_data, total_uganda_stock,
 sinza_combo_headers, sinza_combos,
 sinza_singles_headers, sinza_singles,
 sinza_special_headers, sinza_specials,
 sinza_stock_data, total_sinza_stock,
 bag_targets) = fetch_offer_data()

# ── Complete (perfect) weeks REMAINING in the current month ───
# A "perfect week" is a Sun–Sat week with >=5 of its days in the month;
# "remaining" counts this week (if it still has days left) plus later ones.
def complete_weeks_remaining(ref=None):
    from datetime import date, timedelta
    today = ref or date.today()
    year, month = today.year, today.month
    me = (date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)) - timedelta(days=1)
    ws = today - timedelta(days=(today.weekday() + 1) % 7)   # Sunday of current week
    n = 0
    while ws <= me:
        days_in = sum(1 for i in range(7)
                      if (ws + timedelta(days=i)).year == year
                      and (ws + timedelta(days=i)).month == month)
        we = ws + timedelta(days=6)
        if days_in >= 5 and we >= today:   # perfect week not yet finished
            n += 1
        ws += timedelta(days=7)
    return max(n, 1)

weeks_remaining = complete_weeks_remaining()

def data_rows_count(rows):
    """Count product rows, excluding the appended TOTAL row."""
    return sum(1 for r in rows
               if not (r and str(r[0]).strip().upper().startswith("TOTAL")))

combo_count      = data_rows_count(june_combos)
power_deal_count = data_rows_count(power_deals)
offer_count      = len(offer_products)      # no total row in this list
stock_row_cnt    = len(stock_data)          # no total row in this list

# Uganda counts
ug_combo_count   = data_rows_count(ug_combos)
ug_singles_count = data_rows_count(ug_singles)
ug_stock_row_cnt = len(ug_stock_data)

# Sinza counts
sinza_combo_count    = data_rows_count(sinza_combos)
sinza_singles_count  = data_rows_count(sinza_singles)
sinza_specials_count = data_rows_count(sinza_specials)
sinza_stock_row_cnt  = len(sinza_stock_data)


# ── INJECT INTO HTML ──────────────────────────────────────────

inline_script = (
    "<!-- OFFER_DATA_START -->\n"
    "<script>\n"
    "const OA = {\n"
    f'  monthName:           {json.dumps(month_name)},\n'
    f'  ugComboTitle:        {json.dumps(ug_title)},\n'
    f'  comboCount:          {combo_count},\n'
    f'  powerDealCount:      {power_deal_count},\n'
    f'  offerCount:          {offer_count},\n'
    f'  stockRowCount:       {stock_row_cnt},\n'
    f'  totalKenyaStock:     "{fmt_int(total_kenya_stock)}",\n'
    f'  juneComboHeaders:    {json.dumps(june_combo_headers,  ensure_ascii=False)},\n'
    f'  juneCombos:          {json.dumps(june_combos,         ensure_ascii=False)},\n'
    f'  powerDealHeaders:    {json.dumps(power_deal_headers,  ensure_ascii=False)},\n'
    f'  powerDeals:          {json.dumps(power_deals,         ensure_ascii=False)},\n'
    f'  bagTargets:          {json.dumps(bag_targets,         ensure_ascii=False)},\n'
    f'  weeksRemaining:      {weeks_remaining},\n'
    f'  offerProducts:       {json.dumps(offer_products,      ensure_ascii=False)},\n'
    f'  stockData:           {json.dumps(stock_data,          ensure_ascii=False)},\n'
    f'  ugComboHeaders:      {json.dumps(ug_combo_headers,    ensure_ascii=False)},\n'
    f'  ugCombos:            {json.dumps(ug_combos,           ensure_ascii=False)},\n'
    f'  ugSinglesHeaders:    {json.dumps(ug_singles_headers,  ensure_ascii=False)},\n'
    f'  ugSingles:           {json.dumps(ug_singles,          ensure_ascii=False)},\n'
    f'  ugComboCount:        {ug_combo_count},\n'
    f'  ugSinglesCount:      {ug_singles_count},\n'
    f'  ugStockRowCount:     {ug_stock_row_cnt},\n'
    f'  totalUgandaStock:    "{fmt_int(total_uganda_stock)}",\n'
    f'  ugStockData:         {json.dumps(ug_stock_data,       ensure_ascii=False)},\n'
    f'  sinzaComboHeaders:   {json.dumps(sinza_combo_headers,   ensure_ascii=False)},\n'
    f'  sinzaCombos:         {json.dumps(sinza_combos,          ensure_ascii=False)},\n'
    f'  sinzaSinglesHeaders: {json.dumps(sinza_singles_headers, ensure_ascii=False)},\n'
    f'  sinzaSingles:        {json.dumps(sinza_singles,         ensure_ascii=False)},\n'
    f'  sinzaSpecialHeaders: {json.dumps(sinza_special_headers, ensure_ascii=False)},\n'
    f'  sinzaSpecials:       {json.dumps(sinza_specials,        ensure_ascii=False)},\n'
    f'  sinzaComboCount:     {sinza_combo_count},\n'
    f'  sinzaSinglesCount:   {sinza_singles_count},\n'
    f'  sinzaSpecialsCount:  {sinza_specials_count},\n'
    f'  sinzaStockRowCount:  {sinza_stock_row_cnt},\n'
    f'  totalSinzaStock:     "{fmt_int(total_sinza_stock)}",\n'
    f'  sinzaStockData:      {json.dumps(sinza_stock_data,      ensure_ascii=False)}\n'
    "};\n"
    "</script>\n"
    "<!-- OFFER_DATA_END -->"
)

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE_DIR, "offer_type_analysis.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

html = re.sub(
    r"<!-- OFFER_DATA_START -->.*?<!-- OFFER_DATA_END -->",
    inline_script,
    html,
    flags=re.DOTALL
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

if not os.environ.get("DENRI_LAUNCHER"):
    webbrowser.open_new_tab(pathlib.Path(html_path).as_uri())

print("offer_type_analysis.html updated.")
