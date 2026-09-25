"""
shops_efficiency.py
─────────────────────────────────────────────────────────────────
Builds the Shops Efficiency dashboard (shops_efficiency.html) from
Google Sheets: how well each shop converts the bags it holds and
receives via dispatch.

    python shops_efficiency.py

Sheets (all COLOUR / [CATEGORY] / PRODUCT NAME / BAG TYPE, then one
column per location):
  WEEKLY_DISPATCH, MONTHLY_DISPATCH   bags dispatched to shops
  WEEKLY_SALES,    MONTHLY_SALES      bags sold / converted
  STOCK_LEVELS                        bags currently at each shop
(Dispatch and sales rows are now rebuilt from Odoo in these layouts by
lib/odoo_tabs.py; stock is live Odoo per-shop on-hand.)

Per-shop metrics (D = dispatched, C = sold):
  NO. OF BAGS AT THE SHOP            stock on hand
  TOTAL BAGS SOLD                   C
  NO. OF BAGS DISPATCHED            D
  BAGS SOLD FROM DISPATCH HELP      C where D>0
  STOCKS REMAINING AFTER DISPATCH   max(D-C,0) where D>0
  CLEARED BAGS WITHOUT DISPATCH     C where D=0  (shop's own buffer stock)
─────────────────────────────────────────────────────────────────
"""

import os, re, json
from datetime import date

SPREADSHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"


# ══════════════════════════════════════════════════════════════
# MANUAL INPUTS — edit these, then run (or hit Refresh)
# ══════════════════════════════════════════════════════════════

# Kenya shops only (WEBSITE / SINZA / UGANDA excluded on purpose).
# Any name here is matched to its column by the sheet header.
KENYA_SHOPS = [
    "STARMALL", "MOMBASA", "NAKURU", "ELDORET", "KISUMU", "MERU",
    "THIKA", "HAZINA", "KITENGELA", "NANYUKI", "KAKAMEGA", "HILTON",
    "KISII", "KTDA", "BUSIA", "RONGAI",
]

# Shop → Region grouping for the region-level view. Kenya only, so region
# totals match the Kenya-shop totals (Diaspora/Online/Rejects left out).
SHOP_REGION_MAP = {
    "Hazina":    "Nairobi CBD",
    "Hilton":    "Nairobi CBD",
    "Starmall":  "Nairobi CBD",
    "Ktda":      "Nairobi CBD",
    "Kitengela": "Nairobi Metropolitan",
    "Rongai":    "Nairobi Metropolitan",
    "Mombasa":   "Coastal Region",
    "Kakamega":  "Western & Nyanza",
    "Kisumu":    "Western & Nyanza",
    "Kisii":     "Western & Nyanza",
    "Busia":     "Western & Nyanza",
    "Meru":      "Central Region",
    "Nanyuki":   "Central Region",
    "Thika":     "Central Region",
    "Eldoret":   "Rift Valley",
    "Nakuru":    "Rift Valley",
}

REGION_MAP_UP = {k.upper(): v for k, v in SHOP_REGION_MAP.items()}
# Track every location the shop view or the region view needs (uppercased)
ALL_LOCATIONS = list(dict.fromkeys(KENYA_SHOPS + [k.upper() for k in SHOP_REGION_MAP]))

# Weekly targets
WK_BAGS_TARGET  = 5000      # total bags to sell this week (the 100% goal)
WK_BUFFER_STOCK = 5000      # last week's overstayed/buffer stock to clear

# Monthly targets
MO_BAGS_TARGET  = 20000     # total bags to sell this month
MO_BUFFER_STOCK = 20000     # month's buffer stock to clear

# Rates (used for both weekly and monthly)
DISPATCH_CONVERSION_TARGET_PCT = 90   # of dispatched bags, % expected to sell
STOCK_REMAINING_TARGET_PCT     = 10   # of dispatched bags, max % left over
BUFFER_CLEARANCE_TARGET_PCT    = 70   # of buffer stock, % cleared w/o dispatch


# ══════════════════════════════════════════════════════════════
# GOOGLE SHEETS AUTH
# ══════════════════════════════════════════════════════════════

# Shared auth: service account (permanent) or self-healing OAuth — see google_auth.py
from google_auth import get_gspread_client


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════

def safe_int(val):
    try:
        return int(float(str(val).replace(",", "").strip()))
    except (ValueError, TypeError):
        return 0

def fmt_int(n):
    return f"{int(round(n)):,}"

def fmt_pct(p):
    return f"{p:.2f}%"

def pct(numer, denom):
    return (numer / denom * 100) if denom else 0.0


def parse_sheet(rows):
    """Return (data, meta) for the Kenya shops, locating columns by header
    name (layouts differ per sheet).
      data : {(bag_upper, colour_upper): {shop: qty}}
      meta : {(bag_upper, colour_upper): {colour, product, category, bagType}}
    """
    if not rows:
        return {}, {}
    header = [str(h).strip() for h in rows[0]]
    header_up = [h.upper() for h in header]

    def col_of(name):
        try:
            return header_up.index(name)
        except ValueError:
            return None

    colour_c   = col_of("COLOUR")
    bag_c      = col_of("BAG TYPE")
    product_c  = col_of("PRODUCT NAME")
    category_c = col_of("CATEGORY")
    shop_cols = {}
    for shop in ALL_LOCATIONS:
        c = col_of(shop)
        if c is not None:
            shop_cols[shop] = c

    if bag_c is None or colour_c is None:
        return {}, {}

    def cell(row, c):
        return str(row[c]).strip() if (c is not None and len(row) > c) else ""

    data, meta = {}, {}
    for row in rows[1:]:
        bag    = cell(row, bag_c)
        colour = cell(row, colour_c)
        if not bag or bag.upper() in ("SUM TOTAL", "TOTAL", "GRAND TOTAL"):
            continue
        key = (bag.upper(), colour.upper())
        rec = data.setdefault(key, {s: 0 for s in shop_cols})
        for shop, c in shop_cols.items():
            if len(row) > c:
                rec[shop] += safe_int(row[c])
        if key not in meta:
            meta[key] = {
                "colour":   colour,
                "product":  cell(row, product_c),
                "category": cell(row, category_c),
                "bagType":  bag,
            }
    return data, meta


# Odoo stock-location top-code → the shop's uppercase name (the header parse_sheet
# keys shop columns by, and the names KENYA_SHOPS / SHOP_REGION_MAP use). Website /
# KTDA main store are online/warehouse, not retail shops, so they are left out.
STOCK_CODE_TO_SHOP = {
    "STAR": "STARMALL", "MSA": "MOMBASA", "NAKS": "NAKURU", "ELD": "ELDORET",
    "KSM": "KISUMU", "MERU": "MERU", "THK": "THIKA", "HAZ": "HAZINA",
    "KITE": "KITENGELA", "NAN": "NANYUKI", "KAK": "KAKAMEGA", "HTN": "HILTON",
    "KSI": "KISII", "KTDA": "KTDA", "BUSIA": "BUSIA", "RONG": "RONGAI",
}


def odoo_stock_levels():
    """Live per-shop Odoo on-hand in the SAME shape parse_sheet(STOCK_LEVELS) returns:
    {(PRODUCTNAME, ''): {SHOP_UPPER: qty}}. Only the per-shop totals are consumed
    downstream (via sum_by_shop / the region aggregation), so the colour key is left
    blank. Returns {} if Postgres is unreachable (the caller then shows 0 — the
    STOCK_LEVELS sheet is never read for stock)."""
    try:
        from lib import stock as _stock
        by_code = _stock.odoo_stock_by_shop_code(list(STOCK_CODE_TO_SHOP.keys()))
    except Exception:                                        # noqa: BLE001
        return {}
    if not by_code:
        return {}
    shops = list(STOCK_CODE_TO_SHOP.values())
    out = {}
    for code, names in by_code.items():
        shop = STOCK_CODE_TO_SHOP.get(str(code).strip().upper())
        if not shop:
            continue
        for name, qty in names.items():
            rec = out.setdefault((str(name).upper(), ""), {s: 0 for s in shops})
            rec[shop] += int(qty or 0)
    return out


def sum_by_shop(parsed, locations=None):
    """Total per location across all bag rows (Kenya shops by default)."""
    locs = locations if locations is not None else KENYA_SHOPS
    totals = {s: 0 for s in locs}
    for rec in parsed.values():
        for s in locs:
            totals[s] += rec.get(s, 0)
    return totals


def compute_period(dispatch, sales, stock, meta, bags_target, buffer_stock):
    """Build every per-shop metric + the summary rows for one period."""
    shops = [s for s in KENYA_SHOPS]

    at_shop     = sum_by_shop(stock)      # NO. OF BAGS AT THE SHOP
    sold_total  = sum_by_shop(sales)      # TOTAL BAGS SOLD
    dispatched  = sum_by_shop(dispatch)   # NO. OF BAGS DISPATCHED

    with_dispatch    = {s: 0 for s in shops}   # C where D>0
    remaining        = {s: 0 for s in shops}   # max(D-C,0) where D>0
    without_dispatch = {s: 0 for s in shops}   # C where D=0

    remaining_detail = []   # row-level leftover, for the filter table

    keys = set(dispatch) | set(sales)
    for key in keys:
        drec = dispatch.get(key, {})
        srec = sales.get(key, {})
        info = meta.get(key, {})
        for shop in shops:
            D = drec.get(shop, 0)
            C = srec.get(shop, 0)
            if D > 0:
                with_dispatch[shop] += C
                left = max(D - C, 0)
                remaining[shop] += left
                if left > 0:
                    remaining_detail.append({
                        "shop":       shop,
                        "colour":     info.get("colour", ""),
                        "category":   info.get("category", ""),
                        "product":    info.get("product", ""),
                        "bagType":    info.get("bagType", key[0]),
                        "dispatched": D,
                        "sold":       C,
                        "remaining":  left,
                    })
            else:
                without_dispatch[shop] += C

    remaining_detail.sort(key=lambda r: -r["remaining"])

    # Per-bag PUSH list per shop — the bags physically on hand at each shop, so the per-shop
    # panel can show "which bags to push". `stock` is live Odoo on-hand keyed by (PRODUCT, "")
    # (the product name already carries the colour), which doesn't share keys with the sheet
    # sales/meta — so we take the product name straight from the key and just report on-hand qty.
    def _pushable(name):
        name = (name or "").upper()
        if not name or "+" in name:
            return False                                     # drop combo/promo lines
        return not any(w in name for w in ("WIPE", " FREE", "FREE ", "BUY ", " GET "))

    # The sheet meta (dispatch/sales) carries bagType + category; use it to split each Odoo-stock
    # product name ("JUMBO BROWN") into bagType ("JUMBO") + colour ("BROWN") and tag its category,
    # so the push list is filterable by Colour / Category / Product / Bag Type.
    bt_cat, bt_list, _seen = {}, [], set()
    for info in meta.values():
        bt = str(info.get("bagType", "")).upper().strip()
        if not bt:
            continue
        if bt not in _seen:
            _seen.add(bt); bt_list.append(bt)
        if info.get("category") and bt not in bt_cat:
            bt_cat[bt] = info["category"]
    bt_list.sort(key=len, reverse=True)                      # longest bagType first (prefix match)

    def _split(name):
        up = str(name).upper().strip()
        for bt in bt_list:
            if up == bt or up.startswith(bt + " "):
                return bt.title(), up[len(bt):].strip().title(), bt_cat.get(bt, "")
        return "", "", ""

    push_detail = []
    for key, strec in stock.items():
        info = meta.get(key, {})
        name = info.get("product") or (key[0] if isinstance(key, tuple) else str(key))
        if not _pushable(name):
            continue
        bt, colour, cat = _split(name)
        for shop in shops:
            onhand = strec.get(shop, 0)
            if onhand > 0:
                push_detail.append({"shop": shop, "product": name, "stock": onhand,
                                    "bagType": bt or name, "colour": colour, "category": cat})
    push_detail.sort(key=lambda r: -r["stock"])

    def total(d):
        return sum(d.values())

    metrics = [
        {"metric": "NO. OF BAGS AT THE SHOP",          "byShop": at_shop},
        {"metric": "TOTAL BAGS SOLD",                  "byShop": sold_total},
        {"metric": "NO. OF BAGS DISPATCHED",           "byShop": dispatched},
        {"metric": "BAGS SOLD FROM DISPATCH HELP",     "byShop": with_dispatch},
        {"metric": "STOCKS REMAINING AFTER DISPATCH",  "byShop": remaining},
        {"metric": "CLEARED BAGS WITHOUT DISPATCH",    "byShop": without_dispatch},
    ]
    for m in metrics:
        m["total"] = total(m["byShop"])

    t_sold        = total(sold_total)
    t_dispatched  = total(dispatched)
    t_with        = total(with_dispatch)
    t_remaining   = total(remaining)
    t_without     = total(without_dispatch)

    dispatch_conv_target = round(t_dispatched * DISPATCH_CONVERSION_TARGET_PCT / 100)
    remaining_target     = round(t_dispatched * STOCK_REMAINING_TARGET_PCT / 100)
    clearance_target     = round(buffer_stock * BUFFER_CLEARANCE_TARGET_PCT / 100)

    summary = [
        {
            "metric": "TOTAL BAGS SOLD", "actual": t_sold, "target": bags_target,
            "targetPct": "100.00%", "actualPct": fmt_pct(pct(t_sold, bags_target)),
            "desc": "should reach 100%", "currentPct": fmt_pct(pct(t_sold, bags_target)),
            "tone": "sold",
        },
        {
            "metric": "NO. OF BAGS DISPATCHED", "actual": t_dispatched, "target": None,
            "targetPct": "—", "actualPct": "—",
            "desc": "bags sent out to the shops", "currentPct": "—",
            "tone": "info",
        },
        {
            "metric": "BAGS SOLD FROM DISPATCH HELP", "actual": t_with,
            "target": dispatch_conv_target,
            "targetPct": fmt_pct(DISPATCH_CONVERSION_TARGET_PCT),
            "actualPct": fmt_pct(pct(t_with, dispatch_conv_target)),
            "desc": "To help Sales to convert",
            "currentPct": fmt_pct(pct(t_with, t_sold)), "tone": "good",
        },
        {
            "metric": "STOCKS REMAINING AFTER DISPATCH", "actual": t_remaining,
            "target": remaining_target,
            "targetPct": fmt_pct(STOCK_REMAINING_TARGET_PCT),
            "actualPct": fmt_pct(pct(t_remaining, t_dispatched)),
            "desc": "To be reduced at the shop level",
            "currentPct": fmt_pct(pct(t_remaining, t_dispatched)), "tone": "warn",
        },
        {
            "metric": "CLEARED BAGS WITHOUT DISPATCH HELP", "actual": t_without,
            "target": clearance_target,
            "targetPct": fmt_pct(BUFFER_CLEARANCE_TARGET_PCT),
            "actualPct": fmt_pct(pct(t_without, clearance_target)),
            "desc": "Shops to convert bags that have overstayed",
            "currentPct": fmt_pct(pct(t_without, t_sold)), "tone": "good",
        },
    ]

    # ── PER-SHOP PERFORMANCE ──────────────────────────────────
    # Turn the raw counts into rates that say how each shop is doing:
    #   sellThrough   = sold / stock-at-shop           (higher = better)
    #   dispatchConv  = sold-from-dispatch / dispatched (higher = better; vs 90%)
    #   remainingRate = remaining / dispatched          (lower  = better; vs 10%)
    #   selfCleared   = bags cleared from own buffer    (hustle, higher = better)
    # Score (0-100, higher = better): sell-through, blended with dispatch
    # conversion where the shop actually received dispatches.
    performance = []
    for shop in shops:
        a  = at_shop[shop]
        c  = sold_total[shop]
        d  = dispatched[shop]
        wd = with_dispatch[shop]
        rm = remaining[shop]
        solo = without_dispatch[shop]

        sell_through = pct(c, a)
        disp_conv    = pct(wd, d) if d else None
        rem_rate     = pct(rm, d) if d else None

        # Cap both components at 100 so a shop that sold more than it held /
        # was sent (rate > 100%) doesn't distort the ranking.
        st_capped = min(sell_through, 100)
        if d:
            conv_capped = min(disp_conv or 0, 100)
            score = 0.6 * st_capped + 0.4 * conv_capped
        else:
            score = st_capped

        performance.append({
            "name": shop, "shop": shop, "atShop": a, "sold": c, "dispatched": d,
            "soldFromDispatch": wd, "remaining": rm, "selfCleared": solo,
            "sellThrough":   round(sell_through, 1),
            "dispatchConv":  (round(disp_conv, 1) if disp_conv is not None else None),
            "remainingRate": (round(rem_rate, 1)  if rem_rate  is not None else None),
            "score":         round(score, 1),
        })

    performance.sort(key=lambda p: -p["score"])
    for i, p in enumerate(performance):
        p["rank"] = i + 1

    return {
        "shops": shops, "metrics": metrics, "summary": summary,
        "remainingDetail": remaining_detail,
        "pushDetail": push_detail,
        "performance": performance,
        "totals": {
            "remaining": t_remaining,
            "cleared":   t_without,
        },
    }


def compute_regions(dispatch, sales, stock):
    """Aggregate every metric by region (using SHOP_REGION_MAP). Independent
    of the Kenya-shop view — includes any mapped location present in the
    sheets (so Diaspora / Online show up too)."""
    # Only locations that actually have a column somewhere
    present = set()
    for src in (dispatch, sales, stock):
        for rec in src.values():
            present.update(rec.keys())
    locs = [l for l in REGION_MAP_UP if l in present]
    if not locs:
        return {"names": [], "metrics": [], "performance": []}

    at   = {l: 0 for l in locs}
    sold = {l: 0 for l in locs}
    disp = {l: 0 for l in locs}
    wd   = {l: 0 for l in locs}
    rem  = {l: 0 for l in locs}
    solo = {l: 0 for l in locs}

    for rec in stock.values():
        for l in locs: at[l]   += rec.get(l, 0)
    for rec in sales.values():
        for l in locs: sold[l] += rec.get(l, 0)
    for rec in dispatch.values():
        for l in locs: disp[l] += rec.get(l, 0)
    for key in set(dispatch) | set(sales):
        drec = dispatch.get(key, {}); srec = sales.get(key, {})
        for l in locs:
            D = drec.get(l, 0); C = srec.get(l, 0)
            if D > 0:
                wd[l] += C
                rem[l] += max(D - C, 0)
            else:
                solo[l] += C

    region_order = list(dict.fromkeys(REGION_MAP_UP[l] for l in locs))

    def group(d):
        r = {reg: 0 for reg in region_order}
        for l, v in d.items():
            r[REGION_MAP_UP[l]] += v
        return r

    at_r, sold_r, disp_r = group(at), group(sold), group(disp)
    wd_r, rem_r, solo_r  = group(wd), group(rem), group(solo)

    regions = [r for r in region_order
               if any([at_r[r], sold_r[r], disp_r[r], wd_r[r], rem_r[r], solo_r[r]])]

    def by(d):  # restrict to displayed regions, preserving order
        return {r: d[r] for r in regions}

    metrics = [
        {"metric": "NO. OF BAGS AT THE SHOP",         "byRegion": by(at_r)},
        {"metric": "TOTAL BAGS SOLD",                 "byRegion": by(sold_r)},
        {"metric": "NO. OF BAGS DISPATCHED",          "byRegion": by(disp_r)},
        {"metric": "BAGS SOLD FROM DISPATCH HELP",    "byRegion": by(wd_r)},
        {"metric": "STOCKS REMAINING AFTER DISPATCH", "byRegion": by(rem_r)},
        {"metric": "CLEARED BAGS WITHOUT DISPATCH",   "byRegion": by(solo_r)},
    ]
    for m in metrics:
        m["total"] = sum(m["byRegion"].values())

    performance = []
    for r in regions:
        a, c, d = at_r[r], sold_r[r], disp_r[r]
        w, rm_, so = wd_r[r], rem_r[r], solo_r[r]
        sell_through = pct(c, a)
        disp_conv    = pct(w, d) if d else None
        rem_rate     = pct(rm_, d) if d else None
        st_capped = min(sell_through, 100)
        score = (0.6 * st_capped + 0.4 * min(disp_conv or 0, 100)) if d else st_capped
        performance.append({
            "name": r, "atShop": a, "sold": c, "dispatched": d,
            "soldFromDispatch": w, "remaining": rm_, "selfCleared": so,
            "sellThrough":   round(sell_through, 1),
            "dispatchConv":  (round(disp_conv, 1) if disp_conv is not None else None),
            "remainingRate": (round(rem_rate, 1)  if rem_rate  is not None else None),
            "score":         round(score, 1),
        })
    performance.sort(key=lambda p: -p["score"])
    for i, p in enumerate(performance):
        p["rank"] = i + 1

    return {
        "names": regions, "metrics": metrics, "performance": performance,
        "remainingByRegion": by(rem_r), "clearedByRegion": by(solo_r),
    }


# ══════════════════════════════════════════════════════════════
# FETCH + BUILD
# ══════════════════════════════════════════════════════════════

print("Fetching Shops Efficiency data...")
gc = get_gspread_client()
sh = gc.open_by_key(SPREADSHEET_ID)

# Dispatch + sales per bag per shop, rebuilt from Odoo in the sheet tabs' layout
# (lib/odoo_tabs; the sheet tab only if Postgres is down). Windows are shops_dispatch.py's
# — Wed→Tue week, calendar month — so the per-bag table reconciles with the shop totals
# apply_odoo() folds in from shops_dispatch_db.json.
from lib import odoo_tabs
import shops_dispatch
_wk_win, _mo_win = shops_dispatch.week_window(), shops_dispatch.month_window()

def load(tab):
    return odoo_tabs.get_rows(sh, tab, window=_wk_win if tab.startswith("WEEKLY") else _mo_win)

wk_dispatch, wk_d_meta = parse_sheet(load("WEEKLY_DISPATCH"))
mo_dispatch, mo_d_meta = parse_sheet(load("MONTHLY_DISPATCH"))
wk_sales,    wk_s_meta = parse_sheet(load("WEEKLY_SALES"))
mo_sales,    mo_s_meta = parse_sheet(load("MONTHLY_SALES"))

# STOCK (bags at each shop) is LIVE Odoo per-shop on-hand ONLY — the STOCK_LEVELS
# sheet is never read for stock. If Odoo is unreachable, shop stock shows 0.
stock = odoo_stock_levels()
print("  Stock source: Odoo (live per-shop on-hand)" if stock
      else "  Stock source: Odoo unreachable — shop stock shown as 0 (no sheet fallback)")

# Dispatch meta wins (it carries CATEGORY); sales meta fills any gaps
wk_meta = {**wk_s_meta, **wk_d_meta}
mo_meta = {**mo_s_meta, **mo_d_meta}

weekly  = compute_period(wk_dispatch, wk_sales, stock, wk_meta, WK_BAGS_TARGET, WK_BUFFER_STOCK)
monthly = compute_period(mo_dispatch, mo_sales, stock, mo_meta, MO_BAGS_TARGET, MO_BUFFER_STOCK)

weekly["regions"]  = compute_regions(wk_dispatch, wk_sales, stock)
monthly["regions"] = compute_regions(mo_dispatch, mo_sales, stock)


# ── HISTORY: snapshot today's remaining vs cleared for the trend graph ──
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "shops_efficiency_history.json")

def metric_byshop(period, name):
    for m in period["metrics"]:
        if m["metric"] == name:
            return m["byShop"]
    return {}

def update_history():
    today = date.today().isoformat()
    points = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                points = json.load(f).get("points", [])
        except (ValueError, OSError):
            points = []
    entry = {
        "date":        today,
        # grand totals (used for the "All shops" trend)
        "wkRemaining": weekly["totals"]["remaining"],
        "wkCleared":   weekly["totals"]["cleared"],
        "moRemaining": monthly["totals"]["remaining"],
        "moCleared":   monthly["totals"]["cleared"],
        # per-shop breakdown (used to draw each shop's own trend line)
        "wkRemainingByShop": metric_byshop(weekly,  "STOCKS REMAINING AFTER DISPATCH"),
        "wkClearedByShop":   metric_byshop(weekly,  "CLEARED BAGS WITHOUT DISPATCH"),
        "moRemainingByShop": metric_byshop(monthly, "STOCKS REMAINING AFTER DISPATCH"),
        "moClearedByShop":   metric_byshop(monthly, "CLEARED BAGS WITHOUT DISPATCH"),
        # per-region breakdown (region trend lines)
        "wkRemainingByRegion": weekly["regions"].get("remainingByRegion", {}),
        "wkClearedByRegion":   weekly["regions"].get("clearedByRegion", {}),
        "moRemainingByRegion": monthly["regions"].get("remainingByRegion", {}),
        "moClearedByRegion":   monthly["regions"].get("clearedByRegion", {}),
    }
    points = [p for p in points if p.get("date") != today]   # overwrite same day
    points.append(entry)
    points.sort(key=lambda p: p.get("date", ""))
    points = points[-120:]                                    # keep last ~4 months
    with open(HISTORY_FILE, "w") as f:
        json.dump({"points": points}, f, indent=2)
    return points

# ── LIVE dispatch & receiving from Odoo (shops_dispatch.py) ───
# Distributed-In per shop ("the in for the shops") and the receiving
# breakdown/score. Optional: if the file isn't there (DB unreachable when
# shops_dispatch.py ran), the page just hides those sections.
def load_dispatch():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shops_dispatch_db.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (ValueError, OSError):
        return None

dispatch = load_dispatch()


def _metric(period, name):
    for m in period["metrics"]:
        if m["metric"] == name:
            return m
    return None


def apply_odoo(period, disp_period, bags_target, buffer_stock):
    """Replace the dispatch-driven metrics with the live Odoo figures, at shop
    level: NO. OF BAGS DISPATCHED = distributed-in, TOTAL BAGS SOLD = Odoo POS,
    and STOCKS REMAINING AFTER DISPATCH = max(in - sold, 0). Sell-through still
    uses the sheet's NO. OF BAGS AT THE SHOP (stock on hand). Rebuilds the
    metrics, the summary Target-vs-Actual, and the per-shop performance."""
    if not disp_period:
        return
    di   = disp_period.get("distributedIn", {})
    sold = disp_period.get("sold", {})
    shops = period["shops"]
    at_shop = _metric(period, "NO. OF BAGS AT THE SHOP")["byShop"]   # keep from sheet (stock)

    dispatched = {s: int(di.get(s, 0)) for s in shops}
    sold_total = {s: int(sold.get(s, 0)) for s in shops}
    with_dispatch    = {s: min(sold_total[s], dispatched[s]) for s in shops}   # sold covered by dispatch
    remaining        = {s: max(dispatched[s] - sold_total[s], 0) for s in shops}
    without_dispatch = {s: max(sold_total[s] - dispatched[s], 0) for s in shops}  # sold beyond dispatch

    for name, by in (("TOTAL BAGS SOLD", sold_total),
                     ("NO. OF BAGS DISPATCHED", dispatched),
                     ("BAGS SOLD FROM DISPATCH HELP", with_dispatch),
                     ("STOCKS REMAINING AFTER DISPATCH", remaining),
                     ("CLEARED BAGS WITHOUT DISPATCH", without_dispatch)):
        m = _metric(period, name)
        if m:
            m["byShop"] = by
            m["total"] = sum(by.values())

    t_sold, t_dispatched = sum(sold_total.values()), sum(dispatched.values())
    t_with, t_remaining, t_without = (sum(with_dispatch.values()),
                                      sum(remaining.values()), sum(without_dispatch.values()))
    dispatch_conv_target = round(t_dispatched * DISPATCH_CONVERSION_TARGET_PCT / 100)
    remaining_target     = round(t_dispatched * STOCK_REMAINING_TARGET_PCT / 100)
    clearance_target     = round(buffer_stock * BUFFER_CLEARANCE_TARGET_PCT / 100)

    period["summary"] = [
        {"metric": "TOTAL BAGS SOLD", "actual": t_sold, "target": bags_target,
         "targetPct": "100.00%", "actualPct": fmt_pct(pct(t_sold, bags_target)),
         "desc": "should reach 100% — sold from Odoo POS", "currentPct": fmt_pct(pct(t_sold, bags_target)),
         "tone": "sold"},
        {"metric": "NO. OF BAGS DISPATCHED", "actual": t_dispatched, "target": None,
         "targetPct": "—", "actualPct": "—", "desc": "distributed in to shops (Odoo)",
         "currentPct": "—", "tone": "info"},
        {"metric": "BAGS SOLD FROM DISPATCH HELP", "actual": t_with, "target": dispatch_conv_target,
         "targetPct": fmt_pct(DISPATCH_CONVERSION_TARGET_PCT), "actualPct": fmt_pct(pct(t_with, dispatch_conv_target)),
         "desc": "sold that dispatch could cover", "currentPct": fmt_pct(pct(t_with, t_sold)), "tone": "good"},
        {"metric": "STOCKS REMAINING AFTER DISPATCH", "actual": t_remaining, "target": remaining_target,
         "targetPct": fmt_pct(STOCK_REMAINING_TARGET_PCT), "actualPct": fmt_pct(pct(t_remaining, t_dispatched)),
         "desc": "distributed-in not yet sold — to be reduced",
         "currentPct": fmt_pct(pct(t_remaining, t_dispatched)), "tone": "warn"},
        {"metric": "CLEARED BAGS WITHOUT DISPATCH HELP", "actual": t_without, "target": clearance_target,
         "targetPct": fmt_pct(BUFFER_CLEARANCE_TARGET_PCT), "actualPct": fmt_pct(pct(t_without, clearance_target)),
         "desc": "sold beyond what was distributed (own buffer)",
         "currentPct": fmt_pct(pct(t_without, t_sold)), "tone": "good"},
    ]

    performance = []
    for shop in shops:
        a, c, d = at_shop.get(shop, 0), sold_total[shop], dispatched[shop]
        wd, rm, solo = with_dispatch[shop], remaining[shop], without_dispatch[shop]
        sell_through = pct(c, a)
        disp_conv = pct(wd, d) if d else None
        rem_rate  = pct(rm, d) if d else None
        st_capped = min(sell_through, 100)
        score = (0.6 * st_capped + 0.4 * min(disp_conv or 0, 100)) if d else st_capped
        performance.append({
            "name": shop, "shop": shop, "atShop": a, "sold": c, "dispatched": d,
            "soldFromDispatch": wd, "remaining": rm, "selfCleared": solo,
            "sellThrough": round(sell_through, 1),
            "dispatchConv": (round(disp_conv, 1) if disp_conv is not None else None),
            "remainingRate": (round(rem_rate, 1) if rem_rate is not None else None),
            "score": round(score, 1),
        })
    performance.sort(key=lambda p: -p["score"])
    for i, p in enumerate(performance):
        p["rank"] = i + 1
    period["performance"] = performance
    period["totals"] = {"remaining": t_remaining, "cleared": t_without}

    # ── Region view: SAME groupings (SHOP_REGION_MAP), numbers from Odoo ──
    region_of = {s: REGION_MAP_UP.get(s) for s in shops}
    order = []
    for s in shops:
        r = region_of[s]
        if r and r not in order:
            order.append(r)
    z = lambda: {r: 0 for r in order}
    at_r, sold_r, disp_r, wd_r, rem_r, solo_r = z(), z(), z(), z(), z(), z()
    for s in shops:
        r = region_of[s]
        if not r:
            continue
        at_r[r]   += at_shop.get(s, 0)
        sold_r[r] += sold_total[s]
        disp_r[r] += dispatched[s]
        wd_r[r]   += with_dispatch[s]
        rem_r[r]  += remaining[s]
        solo_r[r] += without_dispatch[s]
    regions = [r for r in order
               if any([at_r[r], sold_r[r], disp_r[r], wd_r[r], rem_r[r], solo_r[r]])]

    def by(d):
        return {r: d[r] for r in regions}

    r_metrics = [
        {"metric": "NO. OF BAGS AT THE SHOP",         "byRegion": by(at_r)},
        {"metric": "TOTAL BAGS SOLD",                 "byRegion": by(sold_r)},
        {"metric": "NO. OF BAGS DISPATCHED",          "byRegion": by(disp_r)},
        {"metric": "BAGS SOLD FROM DISPATCH HELP",    "byRegion": by(wd_r)},
        {"metric": "STOCKS REMAINING AFTER DISPATCH", "byRegion": by(rem_r)},
        {"metric": "CLEARED BAGS WITHOUT DISPATCH",   "byRegion": by(solo_r)},
    ]
    for m in r_metrics:
        m["total"] = sum(m["byRegion"].values())

    r_perf = []
    for r in regions:
        a, c, d = at_r[r], sold_r[r], disp_r[r]
        w, rm_, so = wd_r[r], rem_r[r], solo_r[r]
        sell_through = pct(c, a)
        disp_conv = pct(w, d) if d else None
        rem_rate  = pct(rm_, d) if d else None
        st_capped = min(sell_through, 100)
        score = (0.6 * st_capped + 0.4 * min(disp_conv or 0, 100)) if d else st_capped
        r_perf.append({
            "name": r, "atShop": a, "sold": c, "dispatched": d,
            "soldFromDispatch": w, "remaining": rm_, "selfCleared": so,
            "sellThrough": round(sell_through, 1),
            "dispatchConv": (round(disp_conv, 1) if disp_conv is not None else None),
            "remainingRate": (round(rem_rate, 1) if rem_rate is not None else None),
            "score": round(score, 1),
        })
    r_perf.sort(key=lambda p: -p["score"])
    for i, p in enumerate(r_perf):
        p["rank"] = i + 1

    period["regions"] = {
        "names": regions, "metrics": r_metrics, "performance": r_perf,
        "remainingByRegion": by(rem_r), "clearedByRegion": by(solo_r),
    }


if dispatch:
    apply_odoo(weekly,  dispatch.get("weekly"),  WK_BAGS_TARGET, WK_BUFFER_STOCK)
    apply_odoo(monthly, dispatch.get("monthly"), MO_BAGS_TARGET, MO_BUFFER_STOCK)

# Snapshot the trend AFTER the Odoo override, so remaining/cleared history
# matches what the page now shows.
history = update_history()

def _load_combos_by_shop():
    """Per-shop combo / power-deal view for the panel — built **live from Odoo** via
    self_made_combos (the same POS data the combos page uses), so Shops Efficiency reads Odoo
    like the rest of the page: each shop's running combos (rung vs could-have, red under-ringing,
    Deal-of-the-Week overlap) and how its Power Deals are selling. To avoid rebuilding it twice
    when main.py runs the combos generator seconds earlier, a combos_by_shop.json written in the
    last 15 min is reused; anything older (or a standalone refresh) recomputes live. On a live
    rebuild the shared file is refreshed too. Keys re-cased UPPER to match KENYA_SHOPS."""
    import time
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "combos_by_shop.json")

    def _nonempty(by):
        # A usable view has at least one shop with combos or power deals — guards against an
        # empty rebuild clobbering good data (or a clobbered file being trusted downstream).
        return any((v or {}).get("combos") or (v or {}).get("powerDeals") for v in (by or {}).values())

    def _from_file():
        try:
            with open(p, encoding="utf-8") as f:
                d = json.load(f)
            by = {str(k).upper(): v for k, v in (d.get("byShop") or {}).items()}
            if not _nonempty(by):
                return None
            return {"month": d.get("month", ""), "byShop": by}
        except (OSError, ValueError):
            return None

    # Reuse a just-written file (self_made_combos.py ran seconds ago in the same cycle).
    try:
        if os.path.exists(p) and (time.time() - os.path.getmtime(p)) < 900:
            fresh = _from_file()
            if fresh:
                print("  Combos source    : combos_by_shop.json (fresh, <15 min)")
                return fresh
    except OSError:
        pass

    # Otherwise build it LIVE from Odoo.
    try:
        import self_made_combos as _smc
        ok, _ = _smc.db.check_connection()
        if ok:
            payload = _smc.fetch()
            cbs = (payload or {}).get("combosByShop") or {}
            if _nonempty(cbs):                          # only trust/write a real result
                try:                                    # keep the shared file in sync
                    with open(p, "w", encoding="utf-8") as f:
                        json.dump({"month": payload.get("month", ""), "byShop": cbs}, f, ensure_ascii=False)
                except OSError:
                    pass
                print("  Combos source    : Odoo (live via self_made_combos)")
                return {"month": payload.get("month", ""),
                        "byShop": {str(k).upper(): v for k, v in cbs.items()}}
            print("  Combos source    : live build returned no combos — keeping existing file")
    except Exception as e:                              # noqa: BLE001
        print("  Combos source    : live build failed (%s) — using file if present" % e)

    return _from_file() or {"month": "", "byShop": {}}

SE = {
    "generatedOn":  date.today().strftime("%d %b %Y"),
    "shops":        KENYA_SHOPS,
    "weekly":       weekly,
    "monthly":      monthly,
    "history":      history,
    "dispatch":     dispatch,   # {computedOn, shops, weekly:{distributedIn,receiving}, monthly:{...}}
    "combos":       _load_combos_by_shop(),   # per-shop combos + power deals (from self_made_combos.py)
}


# ══════════════════════════════════════════════════════════════
# INJECT INTO HTML
# ══════════════════════════════════════════════════════════════

inline = (
    "<!-- SHOPS_DATA_START -->\n"
    "<script>\n"
    "const SE = " + json.dumps(SE, ensure_ascii=False, separators=(",", ":")) + ";\n"
    "</script>\n"
    "<!-- SHOPS_DATA_END -->"
)

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE_DIR, "shops_efficiency.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()
html = re.sub(r"<!-- SHOPS_DATA_START -->.*?<!-- SHOPS_DATA_END -->",
              inline, html, flags=re.DOTALL)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

if not os.environ.get("DENRI_LAUNCHER"):
    import webbrowser, pathlib
    webbrowser.open_new_tab(pathlib.Path(html_path).as_uri())

print("shops_efficiency.html updated.")
for label, per in (("WEEKLY", weekly), ("MONTHLY", monthly)):
    s = {m["metric"]: m["total"] for m in per["metrics"]}
    print(f"  {label:8s} sold={s['TOTAL BAGS SOLD']:,}  dispatched={s['NO. OF BAGS DISPATCHED']:,}  "
          f"from-dispatch={s['BAGS SOLD FROM DISPATCH HELP']:,}  "
          f"remaining={s['STOCKS REMAINING AFTER DISPATCH']:,}  "
          f"cleared-solo={s['CLEARED BAGS WITHOUT DISPATCH']:,}")
