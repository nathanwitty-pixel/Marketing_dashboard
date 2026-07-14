"""
new_products.py
─────────────────────────────────────────────────────────────────
Reads live from Google Sheets (five sheets):

  MONTHLY_TARGET        → new product names + KPIs (target/sales/deficit)
                          col A=bag, col C=target, col D=sales, col E=deficit, col I=flag
  MONTHLY_MARKETING_POST→ col D=BAG TYPE, col E=KENYA posts, col H=OUTSIDE KENYA posts
  STOCK_LEVELS          → col D=BAG TYPE, col A=COLOUR
                          col Y=KENYA, col Z=OUTSIDE KENYA, col AA=RESTOCK
  WEEKLY_MARKETING_POST → col A=COLOUR, col D=BAG TYPE
                          col E=KENYA posts, col H=OUTSIDE KENYA posts
  WEEKLY_SALES          → col A=COLOUR, col B=CATEGORY, col C=PRODUCT NAME
                          col D=BAG TYPE, col X=weekly bags sold

  monthly_combined: bag-type level rows (target/sales/deficit + posts + stock)
  weekly_combined:  colour-level rows merging WEEKLY_SALES + posts + stock
─────────────────────────────────────────────────────────────────
"""

import re, webbrowser, os, pathlib, json
from datetime import date, timedelta

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

def fmt_pct(p):
    return f"{p:.2f}%"


# ── FETCH ─────────────────────────────────────────────────────

def fetch_new_products_data():
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)

    # ── MONTHLY_TARGET ────────────────────────────────────────
    # col A (idx 0) = bag type / name
    # col C (idx 2) = TARGET
    # col D (idx 3) = SALES
    # col E (idx 4) = DEFICIT
    # col I (idx 8) = NEW PRODUCTS flag

    mt      = sh.worksheet("MONTHLY_TARGET")
    mt_rows = mt.get_all_values()

    new_product_names = []
    total_target      = 0
    total_sales       = 0
    total_deficit     = 0
    category_lookup   = {}   # bag_upper -> CATEGORY (col B of MONTHLY_TARGET)
    product_targets   = []   # per-product {name, target, sold, remaining}

    for row in mt_rows[1:]:
        if len(row) < 1:
            continue
        bag = str(row[0]).strip()
        if bag and len(row) > 1:
            category_lookup[bag.upper()] = str(row[1]).strip()
        if len(row) < 9 or not is_checked(row[8]):
            continue
        t = safe_int(row[2]); s = safe_int(row[3]); dfc = safe_int(row[4])
        total_target  += t
        total_sales   += s
        total_deficit += dfc
        if bag:
            new_product_names.append(bag)
            product_targets.append({
                "name": bag, "target": t, "sold": s,
                "remaining": max(t - s, 0),
            })

    names_upper = {n.upper() for n in new_product_names}

    print(f"  New products found    : {len(new_product_names)}")
    for name in new_product_names:
        print(f"    - {name}")

    # ── MONTHLY_SALES ─────────────────────────────────────────
    # col A (idx  0) = COLOUR
    # col B (idx  1) = PRODUCT NAME
    # col C (idx  2) = BAG TYPE  ← matched against names_upper
    # col X (idx 23) = KENYA monthly sales
    # col AA (idx 26) = OUTSIDE KENYA monthly sales

    ms      = sh.worksheet("MONTHLY_SALES")
    ms_rows = ms.get_all_values()

    ms_base = []   # colour-level rows; posts + stock merged in later

    for row in ms_rows[1:]:
        if len(row) < 3:
            continue
        bag_type = str(row[2]).strip()   # col C
        if not bag_type or bag_type.upper() in ("SUM TOTAL", "TOTAL", "GRAND TOTAL"):
            continue
        # Build rows for EVERY product; the new-products subset is derived later.
        colour       = str(row[0]).strip()
        product_name = str(row[1]).strip()
        if "total" in product_name.lower():   # skip subtotal/grand-total rows
            continue
        ms_base.append({
            "colour":       colour,
            "category":     category_lookup.get(bag_type.upper(), ''),
            "productName":  product_name,
            "bagType":      bag_type,
            "kenyaSales":   safe_int(row[23]) if len(row) > 23 else 0,
            "outsideKenya": safe_int(row[26]) if len(row) > 26 else 0,
            "mpostKenya":   0,
            "mpostOutside": 0,
            "sKenya":       0,
            "sOutside":     0,
            "sRestock":     0
        })

    # ── MONTHLY_MARKETING_POST ────────────────────────────────
    # colour-level lookup to merge into monthly rows
    # col A (idx 0) = COLOUR, col D (idx 3) = BAG TYPE
    # col E (idx 4) = KENYA posts, col H (idx 7) = OUTSIDE KENYA posts

    mmp      = sh.worksheet("MONTHLY_MARKETING_POST")
    mmp_rows = mmp.get_all_values()

    mpost_lookup = {}   # (bag_upper, colour_upper) -> {kenya, outsideKenya}
    for row in mmp_rows[1:]:
        if len(row) < 4:
            continue
        bag_type = str(row[3]).strip()
        if not bag_type or bag_type.upper() in ("SUM TOTAL", "TOTAL", "GRAND TOTAL"):
            continue
        colour = str(row[0]).strip()
        key    = (bag_type.upper(), colour.upper())
        if key not in mpost_lookup:
            mpost_lookup[key] = {"kenya": 0, "outsideKenya": 0}
        mpost_lookup[key]["kenya"]        += safe_int(row[4]) if len(row) > 4 else 0
        mpost_lookup[key]["outsideKenya"] += safe_int(row[7]) if len(row) > 7 else 0

    # ── STOCK_LEVELS ──────────────────────────────────────────
    # per-colour lookup shared by both monthly and weekly merges
    # col D (idx  3) = BAG TYPE, col A (idx  0) = COLOUR
    # col Y (idx 24) = KENYA, col Z (idx 25) = OUTSIDE KENYA, col AA (idx 26) = RESTOCK

    sl      = sh.worksheet("STOCK_LEVELS")
    sl_rows = sl.get_all_values()

    stock_lookup = {}   # (bag_upper, colour_upper) -> {sKenya, sOutside, sRestock}

    for row in sl_rows[1:]:
        if len(row) < 4:
            continue
        bag_type = str(row[3]).strip()
        if not bag_type or bag_type.upper() in ("SUM TOTAL", "TOTAL", "GRAND TOTAL"):
            continue
        colour  = str(row[0]).strip()
        s_kenya = safe_int(row[24]) if len(row) > 24 else 0
        s_out   = safe_int(row[25]) if len(row) > 25 else 0
        s_rst   = safe_int(row[26]) if len(row) > 26 else 0
        key     = (bag_type.upper(), colour.upper())
        if key not in stock_lookup:
            stock_lookup[key] = {"sKenya": 0, "sOutside": 0, "sRestock": 0}
        stock_lookup[key]["sKenya"]   += s_kenya
        stock_lookup[key]["sOutside"] += s_out
        stock_lookup[key]["sRestock"] += s_rst

    # Merge posts + stock into each monthly colour-level row
    for r in ms_base:
        lk   = (r["bagType"].upper(), r["colour"].upper())
        post = mpost_lookup.get(lk, {"kenya": 0, "outsideKenya": 0})
        stk  = stock_lookup.get(lk, {"sKenya": 0, "sOutside": 0, "sRestock": 0})
        r["mpostKenya"]   = post["kenya"]
        r["mpostOutside"] = post["outsideKenya"]
        r["sKenya"]       = stk["sKenya"]
        r["sOutside"]     = stk["sOutside"]
        r["sRestock"]     = stk["sRestock"]

    monthly_combined = ms_base

    # ── WEEKLY_MARKETING_POST ─────────────────────────────────
    # col A (idx 0) = COLOUR, col D (idx 3) = BAG TYPE
    # col E (idx 4) = KENYA posts, col H (idx 7) = OUTSIDE KENYA posts

    wmp      = sh.worksheet("WEEKLY_MARKETING_POST")
    wmp_rows = wmp.get_all_values()

    wpost_lookup = {}   # (bag_upper, colour_upper) -> {kenya, outsideKenya}
    for row in wmp_rows[1:]:
        if len(row) < 4:
            continue
        bag_type = str(row[3]).strip()
        if not bag_type or bag_type.upper() in ("SUM TOTAL", "TOTAL", "GRAND TOTAL"):
            continue
        colour = str(row[0]).strip()
        key    = (bag_type.upper(), colour.upper())
        if key not in wpost_lookup:
            wpost_lookup[key] = {"kenya": 0, "outsideKenya": 0}
        wpost_lookup[key]["kenya"]        += safe_int(row[4]) if len(row) > 4 else 0
        wpost_lookup[key]["outsideKenya"] += safe_int(row[7]) if len(row) > 7 else 0

    # ── WEEKLY_SALES ──────────────────────────────────────────
    # col A (idx  0) = COLOUR
    # col B (idx  1) = CATEGORY
    # col C (idx  2) = PRODUCT NAME
    # col D (idx  3) = BAG TYPE
    # col X (idx 23) = TOTAL

    ws      = sh.worksheet("WEEKLY_SALES")
    ws_rows = ws.get_all_values()

    weekly_combined = []

    for row in ws_rows[1:]:
        if len(row) < 4:
            continue
        bag_type = str(row[3]).strip()
        if not bag_type or bag_type.upper() in ("SUM TOTAL", "TOTAL", "GRAND TOTAL"):
            continue
        product_name = str(row[2]).strip()
        if "total" in product_name.lower():
            continue
        colour  = str(row[0]).strip()
        lk      = (bag_type.upper(), colour.upper())
        post    = wpost_lookup.get(lk, {"kenya": 0, "outsideKenya": 0})
        stk     = stock_lookup.get(lk, {"sKenya": 0, "sOutside": 0, "sRestock": 0})
        weekly_combined.append({
            "colour":       colour,
            "category":     str(row[1]).strip(),
            "productName":  product_name,
            "bagType":      bag_type,
            "weeklySales":  safe_int(row[23]) if len(row) > 23 else 0,
            "wpostKenya":   post["kenya"],
            "wpostOutside": post["outsideKenya"],
            "sKenya":       stk["sKenya"],
            "sOutside":     stk["sOutside"],
            "sRestock":     stk["sRestock"]
        })

    # Full catalogue (every product) vs. the new-products subset used by cards/charts
    all_monthly_combined = ms_base
    all_weekly_combined  = weekly_combined
    monthly_combined = [r for r in ms_base         if r["bagType"].upper() in names_upper]
    weekly_combined  = [r for r in weekly_combined if r["bagType"].upper() in names_upper]

    return (new_product_names, total_target, total_sales, total_deficit,
            monthly_combined, weekly_combined, product_targets,
            all_monthly_combined, all_weekly_combined)


# ── RUN ───────────────────────────────────────────────────────

print("Fetching data from Google Sheets...")
(new_product_names, total_target, total_sales, total_deficit,
 monthly_combined, weekly_combined, product_targets,
 all_monthly_combined, all_weekly_combined) = fetch_new_products_data()

product_count    = len(new_product_names)
sales_pct        = (total_sales / total_target * 100) if total_target else 0
monthly_kenya    = sum(r["kenyaSales"]   for r in monthly_combined)
monthly_outside  = sum(r["outsideKenya"] for r in monthly_combined)
mpost_kenya      = sum(r["mpostKenya"]   for r in monthly_combined)
mpost_outside    = sum(r["mpostOutside"] for r in monthly_combined)
m_skenya         = sum(r["sKenya"]       for r in monthly_combined)
m_soutside       = sum(r["sOutside"]     for r in monthly_combined)
m_srestock       = sum(r["sRestock"]     for r in monthly_combined)
weekly_total     = sum(r["weeklySales"]  for r in weekly_combined)
wpost_kenya      = sum(r["wpostKenya"]   for r in weekly_combined)
wpost_outside    = sum(r["wpostOutside"] for r in weekly_combined)
w_skenya         = sum(r["sKenya"]       for r in weekly_combined)
w_soutside       = sum(r["sOutside"]     for r in weekly_combined)
w_srestock       = sum(r["sRestock"]     for r in weekly_combined)


# ── WEEKLY POSTS SNAPSHOT ─────────────────────────────────────
# Record each Sun–Sat week's Weekly Sales Total / Kenya Posts / Outside
# Posts so the dashboard can track Week 1 → the latest week.
WEEKLY_POSTS_HISTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "new_products_weekly_history.json")

def _np_week_start(d):
    return d - timedelta(days=(d.weekday() + 1) % 7)

def _np_complete_weeks_in_month(ref=None):
    """Total perfect weeks in the month (Sun–Sat weeks with >=5 days in it)."""
    d = ref or (date.today() - timedelta(days=1))
    year, month = d.year, d.month
    ms = date(year, month, 1)
    me = (date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)) - timedelta(days=1)
    ws = ms - timedelta(days=(ms.weekday() + 1) % 7)
    n = 0
    while ws <= me:
        days_in = sum(1 for i in range(7)
                      if (ws + timedelta(days=i)).year == year
                      and (ws + timedelta(days=i)).month == month)
        if days_in >= 5:
            n += 1
        ws += timedelta(days=7)
    return max(n, 1)

def _np_perfect_week_index(d):
    """Ordinal among the month's perfect weeks (>=5 days in month), so the first
    FULL week is Week 1 (the opening partial week is not counted here — posts
    tracking only begins on the first full week).
    (e.g. Jul 5–11 = Wk 1, Jul 12–18 = Wk 2, Jul 19–25 = Wk 3, ...)"""
    year, month = d.year, d.month
    ms = date(year, month, 1)
    me = (date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)) - timedelta(days=1)
    ws = ms - timedelta(days=(ms.weekday() + 1) % 7)
    target = _np_week_start(d)
    idx = 0
    while ws <= me:
        days_in = sum(1 for i in range(7)
                      if (ws + timedelta(days=i)).year == year
                      and (ws + timedelta(days=i)).month == month)
        if days_in >= 5:
            idx += 1
        if ws == target:
            return idx if days_in >= 5 else 0
        ws += timedelta(days=7)
    return idx

def update_np_weekly_history():
    ref = date.today() - timedelta(days=1)
    ws  = _np_week_start(ref)
    wk_idx = _np_perfect_week_index(ref)
    entry = {
        "weekStart":    ws.isoformat(),
        "label":        ("Wk " + str(wk_idx)) if wk_idx else "Partial",
        "month":        ref.strftime("%b"),
        "weeklyTotal":  weekly_total,
        "kenyaPosts":   wpost_kenya,
        "outsidePosts": wpost_outside,
    }
    weeks = []
    if os.path.exists(WEEKLY_POSTS_HISTORY):
        try:
            with open(WEEKLY_POSTS_HISTORY, "r") as f:
                weeks = json.load(f).get("weeks", [])
        except (ValueError, OSError):
            weeks = []
    weeks = [w for w in weeks if w.get("weekStart") != entry["weekStart"]]
    weeks.append(entry)
    weeks.sort(key=lambda w: w.get("weekStart", ""))
    weeks = weeks[-16:]
    # Re-label every stored week from its own weekStart, so the numbering stays
    # consistent (opening partial week = Wk 1) even for previously-frozen rows.
    for w in weeks:
        try:
            wi = _np_perfect_week_index(date.fromisoformat(w["weekStart"]))
            w["label"] = ("Wk " + str(wi)) if wi else "Partial"
        except Exception:
            pass
    with open(WEEKLY_POSTS_HISTORY, "w") as f:
        json.dump({"weeks": weeks}, f, indent=2)
    return weeks

np_weekly_history = update_np_weekly_history()

# Weekly target = new-product monthly target ÷ perfect weeks in the month
np_complete_weeks   = _np_complete_weeks_in_month()
weekly_target       = round(total_target / np_complete_weeks) if np_complete_weeks else 0
weekly_sales_pct    = (weekly_total / weekly_target * 100) if weekly_target else 0


# ── INJECT INTO HTML ──────────────────────────────────────────

inline_script = (
    "<!-- NEW_PROD_DATA_START -->\n"
    "<script>\n"
    "const NP = {\n"
    f'  productCount:    {product_count},\n'
    f'  totalTarget:     "{fmt_int(total_target)}",\n'
    f'  totalSales:      "{fmt_int(total_sales)}",\n'
    f'  totalDeficit:    "{fmt_int(total_deficit)}",\n'
    f'  salesPct:        "{fmt_pct(sales_pct)}",\n'
    f'  monthlyKenya:    "{fmt_int(monthly_kenya)}",\n'
    f'  monthlyOutside:  "{fmt_int(monthly_outside)}",\n'
    f'  mpostKenya:      "{fmt_int(mpost_kenya)}",\n'
    f'  mpostOutside:    "{fmt_int(mpost_outside)}",\n'
    f'  mSKenya:         "{fmt_int(m_skenya)}",\n'
    f'  mSOutside:       "{fmt_int(m_soutside)}",\n'
    f'  mSRestock:       "{fmt_int(m_srestock)}",\n'
    f'  productTargets:  {json.dumps(product_targets, ensure_ascii=False)},\n'
    f'  weeklyTotal:     "{fmt_int(weekly_total)}",\n'
    f'  weeklyTarget:    "{fmt_int(weekly_target)}",\n'
    f'  weeklySalesPct:  "{fmt_pct(weekly_sales_pct)}",\n'
    f'  perfectWeeks:    {np_complete_weeks},\n'
    f'  wpostKenya:      "{fmt_int(wpost_kenya)}",\n'
    f'  wpostOutside:    "{fmt_int(wpost_outside)}",\n'
    f'  wSKenya:         "{fmt_int(w_skenya)}",\n'
    f'  wSOutside:       "{fmt_int(w_soutside)}",\n'
    f'  wSRestock:       "{fmt_int(w_srestock)}",\n'
    f'  productNames:    {json.dumps(new_product_names, ensure_ascii=False)},\n'
    f'  monthlyCombined: {json.dumps(monthly_combined, ensure_ascii=False)},\n'
    f'  weeklyCombined:  {json.dumps(weekly_combined, ensure_ascii=False)},\n'
    f'  allMonthlyCombined: {json.dumps(all_monthly_combined, ensure_ascii=False)},\n'
    f'  allWeeklyCombined:  {json.dumps(all_weekly_combined, ensure_ascii=False)},\n'
    f'  weeklyPostsHistory: {json.dumps(np_weekly_history)}\n'
    "};\n"
    "</script>\n"
    "<!-- NEW_PROD_DATA_END -->"
)

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE_DIR, "new_products.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

html = re.sub(
    r"<!-- NEW_PROD_DATA_START -->.*?<!-- NEW_PROD_DATA_END -->",
    inline_script,
    html,
    flags=re.DOTALL
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

if not os.environ.get("DENRI_LAUNCHER"):
    webbrowser.open_new_tab(pathlib.Path(html_path).as_uri())

print("new_products.html updated.")
print(f"  Total Target           : {fmt_int(total_target)}")
print(f"  Total Sales            : {fmt_int(total_sales)}")
print(f"  Total Deficit          : {fmt_int(total_deficit)}")
print(f"  Sales % Achieved       : {fmt_pct(sales_pct)}")
print(f"  Monthly combined rows  : {len(monthly_combined)}")
print(f"  Monthly Kenya sales    : {fmt_int(monthly_kenya)}")
print(f"  Monthly Outside Kenya  : {fmt_int(monthly_outside)}")
print(f"  Monthly posts (Kenya)  : {fmt_int(mpost_kenya)}")
print(f"  Monthly posts (Out)    : {fmt_int(mpost_outside)}")
print(f"  Weekly combined rows   : {len(weekly_combined)}")
print(f"  Weekly sales total     : {fmt_int(weekly_total)}")
print(f"  Weekly posts (Kenya)   : {fmt_int(wpost_kenya)}")
print(f"  Weekly posts (Out)     : {fmt_int(wpost_outside)}")
