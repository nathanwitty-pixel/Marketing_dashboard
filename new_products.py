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


# ── ODOO SALES (source of truth for new-product sold) ─────────
def odoo_month_product_bags():
    """Reporting month's bags per product from Odoo (Postgres), or None if the DB
    isn't reachable. Product list still comes from MONTHLY_TARGET; only the SOLD
    figure is sourced here.

    The window comes from lib/report_month.py so this matches the month the
    report is labelled with — anchoring on today made the 1-Sep run report zero
    new-product sales for August."""
    try:
        from lib import db, queries, report_month
    except Exception:
        return None
    ok, _ = db.check_connection()
    if not ok:
        return None
    start, end = report_month.month_window()
    df = db.run_query(queries.WEEKLY_BAGS_SOLD,   # grouped by full_product_name
                      {"start_date": start.isoformat(), "end_date": end.isoformat()})
    if df is None:
        return None
    if df.empty:
        return []
    return [(str(r["product"]), int(round(float(r["bags"] or 0)))) for _, r in df.iterrows()]


def odoo_lifetime_product_bags():
    """All-time bags per product from Odoo (no month window) — the lifetime sales
    of each new product since it launched. Same query/scope as the monthly figure,
    just an open date range. None if Postgres isn't reachable."""
    try:
        from lib import db, queries
    except Exception:
        return None
    ok, _ = db.check_connection()
    if not ok:
        return None
    df = db.run_query(queries.WEEKLY_BAGS_SOLD,   # grouped by full_product_name
                      {"start_date": "2000-01-01", "end_date": date.today().isoformat()})
    if df is None:
        return None
    if df.empty:
        return []
    return [(str(r["product"]), int(round(float(r["bags"] or 0)))) for _, r in df.iterrows()]


def match_odoo_bags(bag_type, odoo_list):
    """Sum Odoo bags whose product name is the new product's — matched by name
    prefix so 'AMORA' picks up 'AMORA …' variants without catching 'LAMORA'.
    Returns (bags, [matched Odoo names])."""
    b = str(bag_type).upper().strip()
    total, hits = 0, []
    for name, bags in odoo_list:
        p = str(name).upper().strip()
        # Odoo prepends an internal-reference code to full_product_name for some
        # variants, e.g. "[S_0] Lamora Sky Blue" — drop it before prefix-matching
        # so the variant isn't silently missed.
        p = re.sub(r"^\[[^\]]*\]\s*", "", p)
        if p == b or p.startswith(b + " ") or p.startswith(b + "-"):
            total += bags
            hits.append(name)
    return total, hits


def odoo_sales_window(start, end):
    """{UPPER(product name): {'kenya': units, 'outside': units}} for a date window,
    live from Odoo. Kenya = Kenya POS tills; outside = Sinza / Dar-es-Salaam /
    Uganda. None if Postgres is unreachable — so callers fall back to the sheet."""
    if start is None or end is None:
        return None
    try:
        from lib import db
    except Exception:
        return None
    ok, _ = db.check_connection()
    if not ok:
        return None
    sql = """
    SELECT UPPER(pt."name") AS pname,
           COALESCE(SUM(pl.qty) FILTER (WHERE lower(COALESCE(pc."name", '')) NOT IN ('sinza','dar-es-alam','uganda')), 0)::int AS kenya,
           COALESCE(SUM(pl.qty) FILTER (WHERE lower(COALESCE(pc."name", '')) IN ('sinza','dar-es-alam','uganda')), 0)::int AS outside
    FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
    LEFT JOIN pos_session ps ON p.session_id = ps.id
    LEFT JOIN pos_config pc ON ps.config_id = pc.id
    LEFT JOIN product_product pp ON pl.product_id = pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
    WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done', 'paid') AND pl.qty <> 0
    GROUP BY UPPER(pt."name")
    """
    df = db.run_query(sql, {"s": start.isoformat(), "e": end.isoformat()})
    if df is None:
        return None
    return {str(r["pname"]): {"kenya": int(r["kenya"] or 0), "outside": int(r["outside"] or 0)}
            for _, r in df.iterrows()}


def odoo_stock_kenya_outside():
    """({UPPER name: kenya on-hand}, {UPPER name: outside on-hand}) — live Odoo stock.
    Kenya = Kenya shop locations; outside = Sinza (Dar) + Uganda. ({}, {}) when
    Postgres is unreachable — callers then show 0 (the sheet is not read for stock)."""
    try:
        from lib import stock as _stock
    except Exception:                                        # noqa: BLE001
        return {}, {}
    return (_stock.odoo_stock_by_product("kenya"),
            _stock.odoo_stock_by_product("outside"))


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

    # ── SALES from Odoo (source of truth) ─────────────────────
    # The product LIST + TARGET stay from MONTHLY_TARGET; the SOLD figure now
    # comes from Odoo (this month's bags for that product). Falls back to the
    # sheet's SALES column if Postgres isn't reachable.
    odoo_list = odoo_month_product_bags()
    if odoo_list is not None:
        total_sales = 0
        print("  Sales source          : Odoo (this month)")
        for p in product_targets:
            sold, hits = match_odoo_bags(p["name"], odoo_list)
            p["sold"]      = sold
            p["remaining"] = max(p["target"] - sold, 0)
            total_sales   += sold
            tag = ("← " + ", ".join(hits)) if hits else "(no Odoo match)"
            print(f"    - {p['name']:<16} {sold:>5} sold  {tag}")
        total_deficit = sum(p["remaining"] for p in product_targets)
    else:
        print("  Sales source          : sheet (Odoo unreachable)")

    # ── LIFETIME sales (all-time, per product) ────────────────
    odoo_life = odoo_lifetime_product_bags()
    if odoo_life is not None:
        for p in product_targets:
            life, _ = match_odoo_bags(p["name"], odoo_life)
            p["lifetime"] = life
        print(f"  Lifetime sales source : Odoo (all-time) — total {sum(p['lifetime'] for p in product_targets):,}")
    else:
        for p in product_targets:      # fall back to this month's figure
            p["lifetime"] = p["sold"]

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

    # ── STOCK: LIVE Odoo on-hand ONLY (the STOCK_LEVELS sheet is not read) ──
    # sKenya / sOutside are set from live Odoo stock further below (odoo_stock_kenya_outside).
    # sRestock is a sheet planning number with no Odoo on-hand equivalent, so it is 0.

    # Merge posts into each monthly colour-level row (stock is applied later, from Odoo)
    for r in ms_base:
        lk   = (r["bagType"].upper(), r["colour"].upper())
        post = mpost_lookup.get(lk, {"kenya": 0, "outsideKenya": 0})
        r["mpostKenya"]   = post["kenya"]
        r["mpostOutside"] = post["outsideKenya"]

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
        weekly_combined.append({
            "colour":       colour,
            "category":     str(row[1]).strip(),
            "productName":  product_name,
            "bagType":      bag_type,
            "weeklySales":  safe_int(row[23]) if len(row) > 23 else 0,
            "wpostKenya":   post["kenya"],
            "wpostOutside": post["outsideKenya"],
            "sKenya":       0,    # set from live Odoo stock below
            "sOutside":     0,    # set from live Odoo stock below
            "sRestock":     0     # no Odoo on-hand equivalent (sheet planning number)
        })

    # ── Sales from Odoo — the single source of truth for EVERY sales figure ──
    # Replace the sheet's colour-level sales with live Odoo POS sales, split
    # Kenya tills (Kenya) vs Sinza / Dar-es-Salaam / Uganda (outside). Matched to
    # each row by product name (exact upper, then alphanumeric-normalised). Falls
    # back to the sheet only if Postgres is unreachable.
    _norm = lambda s: re.sub(r"[^A-Z0-9]", "", str(s).upper())

    # ── STOCK from Odoo — LIVE on-hand ONLY (the STOCK_LEVELS sheet is not read) ──
    # sKenya = Kenya shop on-hand, sOutside = Sinza(Dar)+Uganda on-hand, matched to each
    # colour-level row by product name (exact upper, then alphanumeric-normalised — the
    # same matching the sales merge uses). A row Odoo has no on-hand for — or an
    # unreachable DB — shows 0; the sheet is never a fallback. sRestock has no Odoo
    # equivalent, so it is 0.
    _sk_odoo, _so_odoo = odoo_stock_kenya_outside()
    _skn = {_norm(k): v for k, v in _sk_odoo.items()}
    _son = {_norm(k): v for k, v in _so_odoo.items()}

    def _apply_stock(rows):
        for r in rows:
            k = str(r["productName"]).upper().strip()
            r["sKenya"]   = int(_sk_odoo.get(k, _skn.get(_norm(k), 0)))
            r["sOutside"] = int(_so_odoo.get(k, _son.get(_norm(k), 0)))
            r["sRestock"] = 0
    _apply_stock(ms_base)
    _apply_stock(weekly_combined)
    print("  Stock source          : Odoo (live on-hand only; sRestock=0, no sheet)"
          if (_sk_odoo or _so_odoo) else
          "  Stock source          : Odoo unreachable — stock shown as 0 (no sheet fallback)")

    try:
        from lib import report_month as _rm
        _m_start, _m_end = _rm.month_window()
    except Exception:
        _m_start = _m_end = None
    _odoo_m = odoo_sales_window(_m_start, _m_end)
    if _odoo_m is not None:
        _mn = {_norm(k): v for k, v in _odoo_m.items()}
        for r in ms_base:
            k = str(r["productName"]).upper().strip()
            s = _odoo_m.get(k) or _mn.get(_norm(k))
            r["kenyaSales"]   = s["kenya"]   if s else 0
            r["outsideKenya"] = s["outside"] if s else 0
        print("  Monthly sales source  : Odoo (Kenya tills vs outside)")

    # Weekly = the current Sun-Sat week, to date
    _today   = date.today()
    _wk_start = _today - timedelta(days=(_today.weekday() + 1) % 7)
    _odoo_w  = odoo_sales_window(_wk_start, _today)
    if _odoo_w is not None:
        _wn = {_norm(k): v for k, v in _odoo_w.items()}
        for r in weekly_combined:
            k = str(r["productName"]).upper().strip()
            s = _odoo_w.get(k) or _wn.get(_norm(k))
            r["weeklySales"] = (s["kenya"] if s else 0)   # WEEKLY_SALES col X is Kenya
        print("  Weekly sales source   : Odoo (Kenya, this week to date)")

    # Last COMPLETE Sun-Sat week — for the "last week's performance" hover, useful in
    # early-week (Mon-Wed) presentations when this week's numbers are still thin.
    _lw_end   = _wk_start - timedelta(days=1)          # Saturday before this week
    _lw_start = _lw_end - timedelta(days=6)            # that week's Sunday
    _odoo_lw  = odoo_sales_window(_lw_start, _lw_end)
    if _odoo_lw is not None:
        _lwn = {_norm(k): v for k, v in _odoo_lw.items()}
        for r in weekly_combined:
            k = str(r["productName"]).upper().strip()
            s = _odoo_lw.get(k) or _lwn.get(_norm(k))
            r["lastWeekKenya"]   = (s["kenya"] if s else 0)
            r["lastWeekOutside"] = (s["outside"] if s else 0)
        print("  Last-week sales source: Odoo (previous Sun-Sat week)")

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
total_lifetime   = sum(p.get("lifetime", 0) for p in product_targets)
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
last_week_kenya   = sum(r.get("lastWeekKenya", 0)   for r in weekly_combined)
last_week_outside = sum(r.get("lastWeekOutside", 0) for r in weekly_combined)
last_week_total   = last_week_kenya + last_week_outside
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
    f'  totalLifetime:   "{fmt_int(total_lifetime)}",\n'
    f'  totalDeficit:    "{fmt_int(total_deficit)}",\n'
    f'  salesPct:        "{fmt_pct(sales_pct)}",\n'
    f'  monthlyKenya:    "{fmt_int(monthly_kenya)}",\n'
    f'  monthlyOutside:  "{fmt_int(monthly_outside)}",\n'
    f'  mpostKenya:      "{fmt_int(mpost_kenya)}",\n'
    f'  mpostOutside:    "{fmt_int(mpost_outside)}",\n'
    f'  mSKenya:         "{fmt_int(m_skenya)}",\n'
    f'  mSOutside:       "{fmt_int(m_soutside)}",\n'
    f'  mSRestock:       "{fmt_int(m_srestock)}",\n'
    f'  productTargets:  {json.dumps(product_targets, ensure_ascii=False, separators=(",", ":"))},\n'
    f'  weeklyTotal:     "{fmt_int(weekly_total)}",\n'
    f'  weeklyTarget:    "{fmt_int(weekly_target)}",\n'
    f'  weeklySalesPct:  "{fmt_pct(weekly_sales_pct)}",\n'
    f'  lastWeekTotal:   "{fmt_int(last_week_total)}",\n'
    f'  lastWeekKenya:   "{fmt_int(last_week_kenya)}",\n'
    f'  lastWeekOutside: "{fmt_int(last_week_outside)}",\n'
    f'  lastWeekPct:     "{fmt_pct((last_week_total / weekly_target * 100) if weekly_target else 0)}",\n'
    f'  perfectWeeks:    {np_complete_weeks},\n'
    f'  wpostKenya:      "{fmt_int(wpost_kenya)}",\n'
    f'  wpostOutside:    "{fmt_int(wpost_outside)}",\n'
    f'  wSKenya:         "{fmt_int(w_skenya)}",\n'
    f'  wSOutside:       "{fmt_int(w_soutside)}",\n'
    f'  wSRestock:       "{fmt_int(w_srestock)}",\n'
    f'  productNames:    {json.dumps(new_product_names, ensure_ascii=False, separators=(",", ":"))},\n'
    f'  monthlyCombined: {json.dumps(monthly_combined, ensure_ascii=False, separators=(",", ":"))},\n'
    f'  weeklyCombined:  {json.dumps(weekly_combined, ensure_ascii=False, separators=(",", ":"))},\n'
    f'  allMonthlyCombined: {json.dumps(all_monthly_combined, ensure_ascii=False, separators=(",", ":"))},\n'
    f'  allWeeklyCombined:  {json.dumps(all_weekly_combined, ensure_ascii=False, separators=(",", ":"))},\n'
    f'  weeklyPostsHistory: {json.dumps(np_weekly_history, separators=(",", ":"))}\n'
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
