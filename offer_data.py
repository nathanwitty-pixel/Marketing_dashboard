"""
offer_data.py
─────────────────────────────────────────────────────────────────
Shared offer dataset (formerly the COMBOS-sheet reader, offer_type_analysis.py).
Oct 2026: the offer lists come from the monthly uploads (offers_monthly.csv, deals_kenya.csv);
only MONTHLY_TARGET is read from the sheet. Builds the offer /
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
                   (rows now built from live Odoo on-hand by lib/odoo_tabs.py in the
                   same layout; the sheet tab is only a fallback when Postgres is down)
─────────────────────────────────────────────────────────────────
"""

import json

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

def _offer_tables(month_name):
    """The month's offer tables in the old COMBOS-sheet shape ([headers], [rows…, TOTAL]) from the
    monthly uploads — offers_monthly.csv (Kenya / Sinza / Uganda combos + singles) and
    deals_kenya.csv (Power Deals). No sheet is read (docs/README.md › Where the data comes from)."""
    import csv, os
    base = os.path.dirname(os.path.abspath(__file__))

    def rows_of(fname):
        try:
            with open(os.path.join(base, fname), encoding="utf-8", newline="") as f:
                return [r for r in csv.DictReader(f) if r.get("Month", "").strip().lower() == month_name.lower()]
        except OSError:
            return []
    offers, deals = rows_of("offers_monthly.csv"), rows_of("deals_kenya.csv")

    def table(title, picked, price_key):
        if not picked:
            return [], []
        body = [[r[price_key[0]].strip(), r.get(price_key[1], "").strip()] for r in picked]
        return [title, "PRICE"], body + [["TOTAL", ""]]
    mon = month_name.upper()
    pick = lambda m, t: [r for r in offers if r["Market"].strip().lower() == m and r["Type"].strip().lower() == t]
    return {
        "kenya":         table(f"{mon} COMBOS", pick("kenya", "combo"), ("Name", "Now")),
        "power":         table("POWER DEALS", [r for r in deals if r["Type"].lower().startswith("power")], ("Product", "Current")),
        "sinzaCombos":   table(f"{mon} COMBOS", pick("sinza", "combo"), ("Name", "Now")),
        "sinzaSingles":  table("SINGLES", pick("sinza", "single"), ("Name", "Now")),
        "ugCombos":      table(f"{mon} OFFERS", pick("uganda", "combo"), ("Name", "Now")),
        "ugSingles":     table("SINGLES", pick("uganda", "single"), ("Name", "Now")),
    }


def fetch_offer_data():
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)

    # Only MONTHLY_TARGET comes from the sheet; the offer lists come from the monthly uploads.
    # Column C = the month's bag targets from Odoo (lib/product_targets — docs/product-targets.md).
    from lib import product_targets
    mt_rows = product_targets.monthly_target_rows(sh.worksheet("MONTHLY_TARGET").get_all_values())
    # STOCK_LEVELS: live Odoo on-hand in the sheet's layout (lib/odoo_tabs; never the sheet).
    # Its ✅/x flags come from the MONTHLY_TARGET just read.
    from lib import odoo_tabs, report_month
    odoo_tabs.prime_offer_flags(mt_rows)
    sl_rows = odoo_tabs.get_rows(None, "STOCK_LEVELS")

    month_name = report_month.live_month_window()[0].strftime("%B")
    T = _offer_tables(month_name)
    june_combo_headers, june_combos = T["kenya"]
    power_deal_headers, power_deals = T["power"]
    ug_title = (month_name + " Offers") if T["ugCombos"][1] else ""

    print(f"  Month             : {month_name} (offers_monthly.csv / deals_kenya.csv)")
    print(f"  {month_name} Combos found : {data_rows_count(june_combos)}")
    print(f"  Power Deals found : {data_rows_count(power_deals)}")

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
    ug_combo_headers, ug_combos = T["ugCombos"]
    ug_singles_headers, ug_singles = T["ugSingles"]

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
    sinza_combo_headers, sinza_combos = T["sinzaCombos"]
    sinza_singles_headers, sinza_singles = T["sinzaSingles"]
    sinza_special_headers, sinza_specials = [], []          # no specials list is uploaded

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
