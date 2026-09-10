"""
offer_data.py
─────────────────────────────────────────────────────────────────
Shared COMBOS-sheet reader (formerly offer_type_analysis.py). Builds the offer /
combo dataset (Kenya + Sinza + Uganda) once and hands it to the Self-Made-Combos
page and the Monthly Report — call build() for the (dict, OFFER_DATA-block) pair.

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

import re, os, json

# ── SPREADSHEET ───────────────────────────────────────────────

SPREADSHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"


# ── GOOGLE SHEETS AUTH ────────────────────────────────────────

# Shared auth: service account (permanent) or self-healing OAuth — see google_auth.py
from google_auth import get_gspread_client


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
    # One batched read of every range this function needs — a single network
    # round-trip instead of ~6 (a worksheet() metadata lookup + a values read per
    # sheet), which dominated the Google-Sheets portion of a refresh. Open-ended row
    # ranges (A:J, A:AB) return all populated rows, matching get_all_values().
    _batched = sh.values_batch_get([
        "COMBOS!A1:M150",           # cols A..M — June archive lives in N..P
        "MONTHLY_TARGET!A:J",       # bag list + target/sales/deficit/offer flag
        "STOCK_LEVELS!A:AB",        # colour/category/name/bagType + region stock cols
    ])
    _vr = _batched.get("valueRanges", [])
    _rng = lambda i: ((_vr[i].get("values") if i < len(_vr) else None) or [])
    grid    = _rng(0)   # COMBOS A1:M150
    mt_rows = _rng(1)   # MONTHLY_TARGET
    sl_rows = _rng(2)   # STOCK_LEVELS

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

    # mt_rows already fetched in the batched read above.
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

    # sl_rows already fetched in the batched read above.
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
        ak_vals  = sh.values_get("COMBOS!AK372:AK381").get("values", [])
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


# ── DERIVED HELPERS ───────────────────────────────────────────

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

def data_rows_count(rows):
    """Count product rows, excluding the appended TOTAL row."""
    return sum(1 for r in rows
               if not (r and str(r[0]).strip().upper().startswith("TOTAL")))


_CACHE = None


def build():
    """Fetch + shape the COMBOS-sheet dataset once (cached per process).

    Returns (oa_dict, offer_data_block). `oa_dict` is consumed directly by
    self_made_combos.py; `offer_data_block` is the
    <!-- OFFER_DATA_START -->…<!-- OFFER_DATA_END --> markup that
    self_made_combos.html embeds so the Monthly Report can read it there."""
    global _CACHE
    if _CACHE is not None:
        return _CACHE

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

    oa = {
        "monthName":           month_name,
        "ugComboTitle":        ug_title,
        "comboCount":          data_rows_count(june_combos),
        "powerDealCount":      data_rows_count(power_deals),
        "offerCount":          len(offer_products),
        "stockRowCount":       len(stock_data),
        "totalKenyaStock":     fmt_int(total_kenya_stock),
        "juneComboHeaders":    june_combo_headers,
        "juneCombos":          june_combos,
        "powerDealHeaders":    power_deal_headers,
        "powerDeals":          power_deals,
        "bagTargets":          bag_targets,
        "weeksRemaining":      complete_weeks_remaining(),
        "offerProducts":       offer_products,
        "stockData":           stock_data,
        "ugComboHeaders":      ug_combo_headers,
        "ugCombos":            ug_combos,
        "ugSinglesHeaders":    ug_singles_headers,
        "ugSingles":           ug_singles,
        "ugComboCount":        data_rows_count(ug_combos),
        "ugSinglesCount":      data_rows_count(ug_singles),
        "ugStockRowCount":     len(ug_stock_data),
        "totalUgandaStock":    fmt_int(total_uganda_stock),
        "ugStockData":         ug_stock_data,
        "sinzaComboHeaders":   sinza_combo_headers,
        "sinzaCombos":         sinza_combos,
        "sinzaSinglesHeaders": sinza_singles_headers,
        "sinzaSingles":        sinza_singles,
        "sinzaSpecialHeaders": sinza_special_headers,
        "sinzaSpecials":       sinza_specials,
        "sinzaComboCount":     data_rows_count(sinza_combos),
        "sinzaSinglesCount":   data_rows_count(sinza_singles),
        "sinzaSpecialsCount":  data_rows_count(sinza_specials),
        "sinzaStockRowCount":  len(sinza_stock_data),
        "totalSinzaStock":     fmt_int(total_sinza_stock),
        "sinzaStockData":      sinza_stock_data,
    }

    # One field per line, arrays inline — the format the Monthly Report's
    # line-based readers (gstr / gnum / garr) expect.
    lines = "".join(f'  {k}: {json.dumps(v, ensure_ascii=False)},\n' for k, v in oa.items())
    block = ("<!-- OFFER_DATA_START -->\n<script>\nconst OA = {\n"
             + lines + "};\n</script>\n<!-- OFFER_DATA_END -->")

    _CACHE = (oa, block)
    return _CACHE


if __name__ == "__main__":
    _oa, _block = build()
    print(f"offer_data: {_oa['comboCount']} Kenya combos · "
          f"{_oa['sinzaComboCount']} Sinza combos · {_oa['ugComboCount']} Uganda combos")
