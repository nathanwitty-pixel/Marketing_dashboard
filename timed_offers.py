"""
timed_offers.py
─────────────────────────────────────────────────────────────────
Timed-offer campaign report (Kenya).

  • Sales  : LIVE from Odoo POS for the EXACT window (startDate..endDate,
             end-of-day inclusive), scoped to the market (Kenya = every till
             except the Sinza/Dar/Uganda ones), per bag type.
             Combo wrappers / delivery / customisation / straps / samples /
             POS-category lines are excluded (same rules as Total Sales).
  • Posting: last week's Kenya marketing posting (WEEKLY_MARKETING_POST col E),
             per bag type — "borrowed" alongside the sales.
  • Config : timed_offers_config.json (market, startDate, endDate, bags[]).

Injects the campaign payload (const TO) into timed_offers.html between the
<!-- TIMED_DATA_START --> / <!-- TIMED_DATA_END --> markers.
─────────────────────────────────────────────────────────────────
"""

import re, os, json, webbrowser, pathlib
from datetime import date, timedelta

SPREADSHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from google_auth import get_gspread_client


# ── HELPERS ───────────────────────────────────────────────────

def safe_int(val):
    try:
        return int(float(str(val).replace(",", "")))
    except (ValueError, TypeError):
        return 0

def fmt_int(n):
    return f"{n:,}"


# ── CONFIG ────────────────────────────────────────────────────

CONFIG_FILE = os.path.join(BASE_DIR, "timed_offers_config.json")

_DEFAULT_BAGS = ["Kai", "Pioneer", "Double Press", "Antitheft", "Code 3", "School bag"]

def _norm_offer(raw):
    """Normalise one offer dict into the canonical shape."""
    o = {"name": "", "market": "Kenya", "startDate": "", "endDate": "",
         "bags": list(_DEFAULT_BAGS), "prices": {}, "shops": []}
    o["name"]      = str(raw.get("name", "") or "").strip()
    o["market"]    = str(raw.get("market", "Kenya") or "Kenya").strip()
    o["startDate"] = str(raw.get("startDate", "") or "").strip()
    o["endDate"]   = str(raw.get("endDate", "") or "").strip()
    # Optional: limit the offer to a time-of-day window (Nairobi wall time, HH:MM),
    # e.g. an evening 16:00–19:00 flash. Empty = the whole day.
    o["startTime"] = str(raw.get("startTime", "") or "").strip()
    o["endTime"]   = str(raw.get("endTime", "") or "").strip()
    # Optional: limit sales to specific POS tills (e.g. Nairobi CBD shops only).
    if isinstance(raw.get("shops"), list):
        o["shops"] = [str(s).strip() for s in raw["shops"] if str(s).strip()]
    if isinstance(raw.get("bags"), list) and raw["bags"]:
        o["bags"] = [str(b).strip() for b in raw["bags"] if str(b).strip()]
    # Actual offer pricing per bag {was, now} — the authoritative discount.
    if isinstance(raw.get("prices"), dict):
        for k, v in raw["prices"].items():
            if isinstance(v, dict):
                o["prices"][str(k).strip().upper()] = {
                    "was": safe_int(v.get("was")), "now": safe_int(v.get("now"))}
    return o

def _derive_month(offers):
    for o in offers:
        s = o.get("startDate") or ""
        if len(s) >= 7:
            return s[:7]
    return date.today().strftime("%Y-%m")

def load_config():
    """Multi-offer config: {"month": "YYYY-MM", "offers": [offer, ...]}.
    Back-compat: an old single-offer dict (top-level name/bags/startDate) is
    wrapped into a one-item offers list."""
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            raw = json.load(f)
    except (ValueError, OSError):
        raw = {}
    if isinstance(raw, dict) and isinstance(raw.get("offers"), list):
        offers = [_norm_offer(o) for o in raw["offers"] if isinstance(o, dict)]
        month = str(raw.get("month", "") or "").strip() or _derive_month(offers)
    elif isinstance(raw, dict) and (raw.get("name") or raw.get("bags") or raw.get("startDate")):
        offers = [_norm_offer(raw)]                     # legacy single-offer file
        month = _derive_month(offers)
    else:
        offers, month = [], date.today().strftime("%Y-%m")
    return {"month": month, "offers": offers}

# Optional shop scoping: when an offer's "shops" is set, campaign sales are limited
# to those tills (e.g. Nairobi CBD = Hazina/Hilton/Starmall/KTDA Shop). Empty = whole market.
def _shop_sql(shops):
    shops = shops or []
    if not shops:
        return ""
    inlist = ", ".join("'" + s.strip().lower().replace("'", "''") + "'" for s in shops)
    return '  AND lower(COALESCE(pc."name",\'\')) IN (' + inlist + ') '

# Optional time-of-day scoping. Odoo stores date_order as UTC; convert to Nairobi wall
# time so an evening "4pm–7pm" window counts the right sales. Applied to both the offer
# window AND the pre-offer baseline, so the daily/lift comparison is like-for-like.
_TIME_RE = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")
def _time_sql(start_time, end_time):
    if not (_TIME_RE.match(start_time or "") and _TIME_RE.match(end_time or "")):
        return ""
    local = "(p.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'Africa/Nairobi')::time"
    return f"  AND {local} >= TIME '{start_time}' AND {local} < TIME '{end_time}' "

# Per-offer globals — the SQL helpers below read _BAGS_UP / _SHOP_SQL / _TIME_SQL, and the
# build block reads CFG / BAGS; build_offer() rebinds all of them before each offer is computed.
CFG = {"name": "", "market": "Kenya", "startDate": "", "endDate": "",
       "bags": list(_DEFAULT_BAGS), "prices": {}, "shops": []}
BAGS = CFG["bags"]
_BAGS_UP = [b.upper() for b in BAGS]
_SHOP_SQL = ""
_TIME_SQL = ""


def _bucket(name):
    """Which configured bag (if any) an Odoo/​sheet product name belongs to,
    by longest-prefix match so 'Double Press' wins over a shorter overlap."""
    n = str(name).strip().upper()
    best = None
    for b in sorted(_BAGS_UP, key=len, reverse=True):
        if n == b or n.startswith(b):
            best = b
            break
    return best


# ── SALES: live from Odoo POS, exact window, Kenya market ─────

def odoo_window_sales(bags, start, end, market):
    """{BAG_UPPER: bags_sold} for the window, Kenya market (excludes Sinza/Dar/
    Uganda tills). Returns ({}, False) if Postgres isn't reachable."""
    out = {b: 0 for b in _BAGS_UP}
    try:
        from lib import db
        ok, _ = db.check_connection()
        if not ok:
            return out, False
    except Exception:
        return out, False

    # Kenya = every till except the non-Kenya markets.
    non_kenya = "('sinza','dar-es-alam','uganda')"
    like_clauses = " OR ".join(
        [f'pt."name" ILIKE :bag{i}' for i in range(len(bags))])
    params = {"s": start, "e": end}
    for i, b in enumerate(bags):
        params[f"bag{i}"] = b + "%"

    q = f"""
    SELECT pt."name" AS product, SUM(pl.qty)::int AS bags
    FROM pos_order p
    JOIN pos_order_line pl ON pl.order_id = p.id
    LEFT JOIN pos_session ps ON p.session_id = ps.id
    LEFT JOIN pos_config pc ON ps.config_id = pc.id
    LEFT JOIN product_product pp ON pl.product_id = pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
    LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
    WHERE p.date_order::date BETWEEN CAST(:s AS date) AND CAST(:e AS date)
      AND p.state IN ('done','paid') AND pl.qty > 0
      AND lower(COALESCE(pc."name",'')) NOT IN {non_kenya}
    {_SHOP_SQL}{_TIME_SQL}
      AND COALESCE(pt."name",'') NOT LIKE '%+%'
      AND COALESCE(pt."name",'') NOT ILIKE '%delivery%'
      AND COALESCE(pt."name",'') NOT ILIKE '%customization%'
      AND COALESCE(pt."name",'') NOT ILIKE '%strap%'
      AND COALESCE(pt."name",'') NOT ILIKE '%sample%'
      AND COALESCE(pcat."name",'') NOT ILIKE '%Pos%'
      AND ({like_clauses})
    GROUP BY pt."name"
    """
    df = db.run_query(q, params)
    if df is None or df.empty:
        return out, True
    for _, r in df.iterrows():
        b = _bucket(r["product"])
        if b:
            out[b] += int(r["bags"] or 0)
    return out, True


def odoo_daily_kenya(bags, start, end):
    """{date_iso: bags} — daily Kenya bags for the offer bags across [start,end],
    used to measure the before-vs-during-offer lift. {} if DB unreachable."""
    out = {}
    try:
        from lib import db
        ok, _ = db.check_connection()
        if not ok:
            return out
    except Exception:
        return out
    like_clauses = " OR ".join([f'pt."name" ILIKE :bag{i}' for i in range(len(bags))])
    params = {"s": start, "e": end}
    for i, b in enumerate(bags):
        params[f"bag{i}"] = b + "%"
    q = f"""
    SELECT p.date_order::date AS d, SUM(pl.qty)::int AS bags
    FROM pos_order p
    JOIN pos_order_line pl ON pl.order_id = p.id
    LEFT JOIN pos_session ps ON p.session_id = ps.id
    LEFT JOIN pos_config pc ON ps.config_id = pc.id
    LEFT JOIN product_product pp ON pl.product_id = pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
    LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
    WHERE p.date_order::date BETWEEN CAST(:s AS date) AND CAST(:e AS date)
      AND p.state IN ('done','paid') AND pl.qty > 0
      AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
    {_SHOP_SQL}{_TIME_SQL}
      AND COALESCE(pt."name",'') NOT LIKE '%+%'
      AND COALESCE(pt."name",'') NOT ILIKE '%delivery%'
      AND COALESCE(pt."name",'') NOT ILIKE '%customization%'
      AND COALESCE(pt."name",'') NOT ILIKE '%strap%'
      AND COALESCE(pt."name",'') NOT ILIKE '%sample%'
      AND COALESCE(pcat."name",'') NOT ILIKE '%Pos%'
      AND ({like_clauses})
    GROUP BY 1 ORDER BY 1
    """
    df = db.run_query(q, params)
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            out[str(r["d"])] = int(r["bags"] or 0)
    return out


def odoo_bag_prices(bags, start, end):
    """Per-bag avg unit price (Kenya, window) + the catalogue-wide Kenya avg,
    so we can tell whether the offer bags are cheap/premium. ({}, 0) if no DB."""
    prices, catalog = {b.upper(): {"qty": 0, "val": 0.0} for b in bags}, 0
    try:
        from lib import db
        ok, _ = db.check_connection()
        if not ok:
            return prices, catalog
    except Exception:
        return prices, catalog
    like_clauses = " OR ".join([f'pt."name" ILIKE :bag{i}' for i in range(len(bags))])
    params = {"s": start, "e": end}
    for i, b in enumerate(bags):
        params[f"bag{i}"] = b + "%"
    base = """
    FROM pos_order p
    JOIN pos_order_line pl ON pl.order_id = p.id
    LEFT JOIN pos_session ps ON p.session_id = ps.id
    LEFT JOIN pos_config pc ON ps.config_id = pc.id
    LEFT JOIN product_product pp ON pl.product_id = pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
    LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
    WHERE p.date_order::date BETWEEN CAST(:s AS date) AND CAST(:e AS date)
      AND p.state IN ('done','paid') AND pl.qty > 0
      AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
      AND COALESCE(pt."name",'') NOT LIKE '%+%'
      AND COALESCE(pt."name",'') NOT ILIKE '%delivery%'
      AND COALESCE(pt."name",'') NOT ILIKE '%customization%'
      AND COALESCE(pt."name",'') NOT ILIKE '%strap%'
      AND COALESCE(pt."name",'') NOT ILIKE '%sample%'
      AND COALESCE(pt."name",'') NOT ILIKE '%KES discount%'
      AND COALESCE(pcat."name",'') NOT ILIKE '%Pos%'
    """
    # per offer-bag
    df = db.run_query(f'SELECT pt."name" AS product, SUM(pl.qty)::int AS qty, '
                      f'SUM(pl.price_subtotal_incl)::numeric AS val {base} AND ({like_clauses}) '
                      f'GROUP BY pt."name"', params)
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            b = _bucket(r["product"])
            if b:
                prices[b]["qty"] += int(r["qty"] or 0)
                prices[b]["val"] += float(r["val"] or 0)
    # catalogue-wide avg
    dfc = db.run_query(f'SELECT ROUND(SUM(pl.price_subtotal_incl)/NULLIF(SUM(pl.qty),0)) AS avg {base}',
                       {"s": start, "e": end})
    if dfc is not None and not dfc.empty and dfc.iloc[0]["avg"] is not None:
        catalog = int(dfc.iloc[0]["avg"])
    return prices, catalog


def kenya_stock_by_bag(bags):
    """{BAG_UPPER: {stock, category}} from STOCK_LEVELS (col Y=24 Kenya, col B=category)."""
    out = {}
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)
    rows = sh.worksheet("STOCK_LEVELS").get_all_values()
    for row in rows[1:]:
        if len(row) < 4:
            continue
        b = _bucket(row[3])
        if not b:
            continue
        e = out.setdefault(b, {"stock": 0, "category": ""})
        e["stock"] += safe_int(row[24]) if len(row) > 24 else 0
        if not e["category"] and len(row) > 1:
            e["category"] = str(row[1]).strip()
    return out


# ── OFFER PRICING: pulled from Odoo, tax-INCLUSIVE (matches the "Incl. Taxes"
#    figure on the product) — NOT the ex-tax Sales Price, and NOT an average. ──
TAX_INCL = 1.16   # Kenya VAT: list_price / fixed_price are ex-tax; ×1.16 = incl-tax.

def odoo_list_price(bags):
    """{BAG_UP: incl-tax Sales Price} — the product's normal price ("was"),
    the dominant list_price among each bag's plain (non-combo) variants, grossed
    up to tax-inclusive. {} if the DB isn't reachable."""
    out = {}
    try:
        from lib import db
        ok, _ = db.check_connection()
        if not ok:
            return out
    except Exception:
        return out
    for b in bags:
        df = db.run_query(
            'SELECT ROUND(pt.list_price * :tax) AS incl, COUNT(*) AS n '
            'FROM product_template pt '
            'WHERE pt."name" ILIKE :pat AND pt."name" NOT LIKE \'%+%\' '
            '  AND COALESCE(pt.active, true) = true AND pt.list_price > 0 '
            'GROUP BY 1 ORDER BY n DESC, incl ASC LIMIT 1',
            {"tax": TAX_INCL, "pat": b + "%"})
        if df is not None and not df.empty:
            out[b.upper()] = int(df.iloc[0]["incl"])
    return out

def odoo_offer_price(bags, start, end):
    """{BAG_UP: incl-tax offer price} — the offer's "now" price, the dominant
    fixed price from pricelist items overlapping the offer window, grossed up to
    incl-tax. {} if none (bag not on a dated pricelist)."""
    out = {}
    try:
        from lib import db
        ok, _ = db.check_connection()
        if not ok:
            return out
    except Exception:
        return out
    for b in bags:
        df = db.run_query(
            'SELECT ROUND(i.fixed_price * :tax) AS incl, COUNT(*) AS n '
            'FROM product_pricelist_item i JOIN product_template pt ON pt.id = i.product_tmpl_id '
            'WHERE pt."name" ILIKE :pat AND pt."name" NOT LIKE \'%+%\' '
            "  AND i.compute_price = 'fixed' AND i.fixed_price > 0 "
            '  AND (i.date_start IS NULL OR i.date_start::date <= CAST(:e AS date)) '
            '  AND (i.date_end   IS NULL OR i.date_end::date   >= CAST(:s AS date)) '
            'GROUP BY 1 ORDER BY n DESC, incl ASC LIMIT 1',
            {"tax": TAX_INCL, "pat": b + "%", "s": start, "e": end})
        if df is not None and not df.empty:
            out[b.upper()] = int(df.iloc[0]["incl"])
    return out

def odoo_bag_daily_value(bags, start, end):
    """{(BAG_UP, 'YYYY-MM-DD'): {'qty', 'val'}} — per-bag daily units and incl-tax
    value (Kenya), so we can build the realised price per bag per week. {} if no DB."""
    out = {}
    try:
        from lib import db
        ok, _ = db.check_connection()
        if not ok:
            return out
    except Exception:
        return out
    like = " OR ".join([f'pt."name" ILIKE :bag{i}' for i in range(len(bags))])
    params = {"s": start, "e": end}
    for i, b in enumerate(bags):
        params[f"bag{i}"] = b + "%"
    q = ('SELECT p.date_order::date AS d, pt."name" AS product, '
         'SUM(pl.qty)::int AS qty, SUM(pl.price_subtotal_incl)::numeric AS val '
         'FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id '
         'LEFT JOIN pos_session ps ON p.session_id = ps.id '
         'LEFT JOIN pos_config pc ON ps.config_id = pc.id '
         'LEFT JOIN product_product pp ON pl.product_id = pp.id '
         'LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id '
         'LEFT JOIN product_category pcat ON pcat.id = pt.categ_id '
         'WHERE p.date_order::date BETWEEN CAST(:s AS date) AND CAST(:e AS date) '
         "  AND p.state IN ('done','paid') AND pl.qty > 0 "
         '  AND lower(COALESCE(pc."name",\'\')) NOT IN (\'sinza\',\'dar-es-alam\',\'uganda\') '
         + _SHOP_SQL + _TIME_SQL +
         '  AND COALESCE(pt."name",\'\') NOT LIKE \'%+%\' '
         '  AND COALESCE(pt."name",\'\') NOT ILIKE \'%delivery%\' '
         '  AND COALESCE(pt."name",\'\') NOT ILIKE \'%sample%\' '
         '  AND COALESCE(pcat."name",\'\') NOT ILIKE \'%Pos%\' '
         f'  AND ({like}) GROUP BY 1, 2')
    df = db.run_query(q, params)
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            b = _bucket(r["product"])
            if not b:
                continue
            e = out.setdefault((b.upper(), str(r["d"])), {"qty": 0, "val": 0.0})
            e["qty"] += int(r["qty"] or 0)
            e["val"] += float(r["val"] or 0)
    return out


# ── POSTING: last week's Kenya posts (WEEKLY_MARKETING_POST col E) ─

def weekly_kenya_posts(bags):
    """{BAG_UPPER: kenya_posts} from WEEKLY_MARKETING_POST col D=bag type,
    col E (idx 4) = Kenya posts."""
    out = {b: 0 for b in _BAGS_UP}
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)
    rows = sh.worksheet("WEEKLY_MARKETING_POST").get_all_values()
    for row in rows[1:]:
        if len(row) < 5:
            continue
        b = _bucket(row[3])          # col D = BAG TYPE
        if b:
            out[b] += safe_int(row[4])   # col E = KENYA posts
    return out


# ── BUILD ─────────────────────────────────────────────────────

def build_offer(offer):
    """Compute the full TO payload for a single offer dict. Rebinds the
    per-offer module globals the SQL helpers and build logic read."""
    global BAGS, _BAGS_UP, _SHOP_SQL, _TIME_SQL, CFG
    CFG = offer
    BAGS = offer["bags"]
    _BAGS_UP = [b.upper() for b in BAGS]
    _SHOP_SQL = _shop_sql(offer.get("shops"))
    _TIME_SQL = _time_sql(offer.get("startTime"), offer.get("endTime"))

    print("Fetching timed-offer data (Odoo sales + weekly posting)...")
    sales_map, sales_live = odoo_window_sales(BAGS, CFG["startDate"], CFG["endDate"], CFG["market"])
    posts_map = weekly_kenya_posts(BAGS)

    # ── LIFT: offer-window bags/day vs the pre-offer month-to-date bags/day ──
    # Baseline = 1st of the offer's month → the day before the offer started
    # ("first week … up to when the offer ran"). Daily series feeds the trend chart.
    lift = None
    try:
        _os = date.fromisoformat(CFG["startDate"])
        _oe = date.fromisoformat(CFG["endDate"])
        _mstart = _os.replace(day=1)
        _dend = max(_oe, date.today())               # fetch through today for the weekly view
        _daily = odoo_daily_kenya(BAGS, _mstart.isoformat(), _dend.isoformat())
        if _daily:
            offer_days = (_oe - _os).days + 1
            base_days  = (_os - _mstart).days            # days before the offer
            def _sum(a, b):
                return sum(v for k, v in _daily.items() if a <= k <= b)
            base_total  = _sum(_mstart.isoformat(), (_os - timedelta(days=1)).isoformat())
            offer_total = _sum(_os.isoformat(), _oe.isoformat())
            base_per_day  = round(base_total / base_days, 1) if base_days else 0.0
            offer_per_day = round(offer_total / offer_days, 1) if offer_days else 0.0
            lift_pct = round((offer_per_day - base_per_day) / base_per_day * 100) if base_per_day else None
            # daily series for the chart (month start → offer end; offer days flagged)
            _series = []
            _d = _mstart
            while _d <= _oe:
                k = _d.isoformat()
                _series.append({"date": k, "bags": _daily.get(k, 0),
                                "off": _os.isoformat() <= k <= _oe.isoformat()})
                _d += timedelta(days=1)
            # weekly buckets (Sun–Sat) across the whole month-to-date — the "week 1,
            # week 2, week 3, offer week" view; the week holding the offer is flagged.
            def _wk_start(d):
                return d - timedelta(days=(d.weekday() + 1) % 7)
            _wk = {}
            _d = _mstart
            while _d <= _dend:
                k = _d.isoformat()
                ws = _wk_start(_d)
                e = _wk.setdefault(ws, {"total": 0, "days": 0, "off": False})
                e["total"] += _daily.get(k, 0)
                e["days"] += 1
                if _os <= _d <= _oe:
                    e["off"] = True
                _d += timedelta(days=1)
            weekly = []
            for _n, ws in enumerate(sorted(_wk), start=1):
                e = _wk[ws]
                # Clamp the week's shown range to within the month (Aug only) — the
                # opening Sun–Sat week starts in July, but we only count/label August.
                _ws_show = max(ws, _mstart)
                _we_show = min(ws + timedelta(days=6), _dend)
                weekly.append({
                    "label": "Wk " + str(_n),
                    "start": _ws_show.isoformat(), "end": _we_show.isoformat(),
                    "total": e["total"], "days": e["days"],
                    "perDay": round(e["total"] / e["days"], 1) if e["days"] else 0.0,
                    "off": e["off"],
                })
            lift = {
                "baseStart": _mstart.isoformat(), "baseEnd": (_os - timedelta(days=1)).isoformat(),
                "baseDays": base_days, "baseTotal": base_total, "basePerDay": base_per_day,
                "offerDays": offer_days, "offerTotal": offer_total, "offerPerDay": offer_per_day,
                "liftPct": lift_pct, "daily": _series, "weekly": weekly,
            }
    except (ValueError, TypeError):
        lift = None

    bag_rows = []
    for b in BAGS:
        bu = b.upper()
        sold  = int(sales_map.get(bu, 0))
        posts = int(posts_map.get(bu, 0))
        bag_rows.append({
            "name":  b,
            "sold":  sold,
            "posts": posts,
            "perPost": round(sold / posts, 1) if posts else None,   # bags sold per post
        })

    bag_rows.sort(key=lambda r: -r["sold"])
    total_sold  = sum(r["sold"]  for r in bag_rows)
    total_posts = sum(r["posts"] for r in bag_rows)

    # Nice window label, e.g. "17–21 Aug 2026"
    def _win_label(s, e):
        try:
            ds, de = date.fromisoformat(s), date.fromisoformat(e)
            if ds.month == de.month and ds.year == de.year:
                return f"{ds.day}–{de.day} {de:%b %Y}"
            return f"{ds:%d %b} – {de:%d %b %Y}"
        except ValueError:
            return f"{s} – {e}"

    # "16:00" -> "4pm", "16:30" -> "4:30pm"
    def _fmt_time(hm):
        try:
            h, m = (int(x) for x in hm.split(":"))
            ap = "am" if h < 12 else "pm"
            h12 = h % 12 or 12
            return f"{h12}:{m:02d}{ap}" if m else f"{h12}{ap}"
        except (ValueError, AttributeError):
            return hm or ""

    _time_label = (_fmt_time(CFG.get("startTime")) + "–" + _fmt_time(CFG.get("endTime"))) \
        if (CFG.get("startTime") and CFG.get("endTime")) else ""

    best  = max(bag_rows, key=lambda r: r["sold"]) if bag_rows else None
    mostp = max(bag_rows, key=lambda r: r["posts"]) if bag_rows else None

    # ── WHY these bags? stock (clearance) · price · season — a repeatable read ──
    try:
        _pstart = date.fromisoformat(CFG["startDate"]).replace(day=1).isoformat()
    except ValueError:
        _pstart = CFG["startDate"]
    _pend = max(date.fromisoformat(CFG["endDate"]), date.today()).isoformat() \
            if CFG["endDate"] else CFG["endDate"]
    _, _catalog_avg = odoo_bag_prices(BAGS, _pstart, _pend)      # catalogue-wide avg (cheap/premium read)
    # Discount attribution: avg selling price BEFORE vs DURING the offer per bag.
    # A real markdown shows the price dropping; a flat/higher price means the bag
    # was effectively already at that price, so its sales aren't down to the discount.
    try:
        _os_d = date.fromisoformat(CFG["startDate"])
        _oe_d = date.fromisoformat(CFG["endDate"])
        _ms_d = _os_d.replace(day=1)
        _pre_prices, _ = odoo_bag_prices(BAGS, _ms_d.isoformat(), (_os_d - timedelta(days=1)).isoformat())
        _off_prices, _ = odoo_bag_prices(BAGS, _os_d.isoformat(), _oe_d.isoformat())
    except ValueError:
        _pre_prices, _off_prices = {}, {}
    _stock_map = kenya_stock_by_bag(BAGS)

    def _avg(m, bu):
        e = m.get(bu, {"qty": 0, "val": 0})
        return round(e["val"] / e["qty"]) if e["qty"] else None

    # Days in each window, so we can compare each bag's DAILY pace before vs during.
    _bd = lift.get("baseDays") if lift else None
    _od = lift.get("offerDays") if lift else None

    _cfg_prices  = CFG.get("prices", {})
    _list_prices = odoo_list_price(BAGS)                            # "was" — Odoo Sales Price incl-tax
    _offer_prices = odoo_offer_price(BAGS, CFG["startDate"], CFG["endDate"])   # "now" — offer pricelist incl-tax

    why_bags = []
    for r in bag_rows:
        bu = r["name"].upper()
        off_p = _avg(_off_prices, bu)
        pre_p = _avg(_pre_prices, bu)
        sold_at = off_p or pre_p                     # realised avg (what it actually left at)
        # AUTHORITATIVE prices come from ODOO, tax-INCLUSIVE:
        #   was = product Sales Price (list_price ×1.16); now = offer pricelist (fixed ×1.16).
        # Manual config is only a fallback if Odoo has no price; averages are a last resort.
        pr = _cfg_prices.get(bu) or {}
        # Config prices win when present (a manual offer like "300 off" isn't in Odoo's
        # pricelist); otherwise fall back to Odoo's list / offer price.
        was = (pr.get("was") or None) or _list_prices.get(bu)
        now = (pr.get("now") or None) or _offer_prices.get(bu)
        if was and now and was > 0:
            disc_kes = was - now
            disc_pct = round((now - was) / was * 100)          # negative = a cut
            discounted = disc_kes > 0
        else:
            was = now = disc_kes = None
            disc_pct = round((off_p - pre_p) / pre_p * 100) if (pre_p and off_p) else None
            discounted = bool(disc_pct is not None and disc_pct <= -3)
        # each bag's own sales pace: units/day before vs during the offer
        pre_q = int(_pre_prices.get(bu, {}).get("qty", 0))
        off_q = int(_off_prices.get(bu, {}).get("qty", 0))
        pre_pd = round(pre_q / _bd, 1) if _bd else None
        off_pd = round(off_q / _od, 1) if _od else None
        bag_lift = round((off_pd - pre_pd) / pre_pd * 100) if (pre_pd and off_pd is not None) else None
        sm = _stock_map.get(bu, {"stock": 0, "category": ""})
        why_bags.append({
            "name": r["name"], "sold": r["sold"], "posts": r["posts"], "stock": sm["stock"],
            "priceWas": was, "priceNow": now, "discountKes": disc_kes,
            "discountPct": disc_pct, "discounted": discounted, "soldAt": sold_at,
            "prePerDay": pre_pd, "offerPerDay": off_pd, "bagLift": bag_lift,
            "category": sm["category"],
        })

    _total_stock = sum(w["stock"] for w in why_bags)
    _cats = sorted({w["category"] for w in why_bags if w["category"]})
    _topstock = max(why_bags, key=lambda w: w["stock"]) if why_bags else None
    _zero_post = [w["name"] for w in why_bags if not w["posts"] and w["sold"] > 0]
    _lift_txt = (f"+{lift['liftPct']}%" if lift and lift.get("liftPct") is not None else "higher")

    # Discount reality — from the real offer pricelist (config), not inferred averages.
    _priced = [w for w in why_bags if w.get("discountKes") is not None]
    _disc   = [w for w in why_bags if w["discounted"]]
    _all_cut = bool(_priced) and all(w["discounted"] for w in _priced)
    _kes  = [w["discountKes"] for w in _priced if w["discountKes"]]
    _pcts = [abs(w["discountPct"]) for w in _priced if w["discountPct"] is not None]
    _deepest = min(_priced, key=lambda w: w["discountPct"]) if _priced else None    # most negative
    _bestseller  = bag_rows[0]  if bag_rows else None
    _best_disc = next((w["discountPct"] for w in why_bags
                       if _bestseller and w["name"] == _bestseller["name"]), None)

    _insights = []
    # 1) On offer? — the real cuts
    if _all_cut:
        _list = ", ".join(f"{w['name']} −{w['discountKes']:,} ({w['discountPct']}%)" for w in _priced)
        _insights.append({"tag": "On offer?", "text":
            f"<b>All six were genuinely on offer</b> — real list-price cuts of KES {min(_kes):,}–{max(_kes):,} "
            f"({min(_pcts)}–{max(_pcts)}% off): {_list}."})
    elif _disc:
        _insights.append({"tag": "On offer?", "text":
            "On offer (real cut): " + ", ".join(f"{w['name']} ({w['discountPct']}%)" for w in _disc) + "."})
    else:
        _insights.append({"tag": "On offer?", "text":
            "No configured offer prices — showing realised averages only."})

    # 2) Did the discount drive it? — depth vs sales
    if _all_cut and _deepest and _bestseller:
        _insights.append({"tag": "Discount vs demand", "text":
            f"Because <b>every bag was cut</b>, the discount and back-to-school timing can't be fully separated — both applied at once. "
            f"But <b>discount depth didn't decide the winners</b>: the deepest cut, {_deepest['name']} ({_deepest['discountPct']}%), sold only {_deepest['sold']:,}, "
            f"while {_bestseller['name']} led with {_bestseller['sold']:,} on a shallower {_best_disc}% cut. "
            f"The cut opened the door, but <b>demand — which bags people wanted for school — chose what actually moved</b>."})

    # 3) Stock
    if _topstock and _total_stock:
        _insights.append({"tag": "Stock", "text":
            f"Mostly backpacks with real inventory behind them — <b>{_total_stock:,} still in Kenya stock</b> even after the push "
            f"(led by {_topstock['name']} at {_topstock['stock']:,}). The offer draws down a genuine stock position, not a token one."})

    # 4) Season
    if _cats:
        _season_bag = (" and ".join(_zero_post[:2]) + " even sold on zero marketing posts (pure demand). ") if _zero_post else ""
        _insights.append({"tag": "Season", "text":
            f"All six sit in <b>{', '.join(c.title() for c in _cats)}</b> — school categories — and the step-up landed in the offer week as schools opened. "
            f"{_season_bag}The timing fits the sales pattern as much as the price cut does."})

    if _all_cut and _deepest:
        _verdict = (f"<b>Good move.</b> All six ran a real <b>{min(_pcts)}–{max(_pcts)}% cut</b> and daily sales rose <b>{_lift_txt}</b> during back-to-school. "
                    f"The catch: <b>discount depth didn't pick the winners</b> — the deepest cut ({_deepest['name']}, {_deepest['discountPct']}%) sold least, while the popular school lines led. "
                    f"Repeat the timing; you can likely <b>trim the deepest cuts</b> on the slow movers without losing volume.")
    else:
        _verdict = (f"<b>Good move.</b> Sales rose <b>{_lift_txt}</b> per day during back-to-school. Match the cut depth to demand — the popular school lines carried the volume.")

    why = {"totalStock": _total_stock, "categories": _cats, "allCut": _all_cut,
           "bags": why_bags, "insights": _insights, "verdict": _verdict}

    # ── Price week-by-week: realised avg price per bag per week vs list/offer ──
    # Shows whether each bag was ALREADY selling at/below the offer price before the
    # window (→ timing drove it) or only got cut in the offer week (→ the discount did).
    if lift and lift.get("weekly"):
        _dv = odoo_bag_daily_value(BAGS, lift["baseStart"], date.today().isoformat())
        _pw_bags = []
        for w in why_bags:
            bu = w["name"].upper()
            cells = []
            for wk in lift["weekly"]:
                q = v = 0.0
                dd, de = date.fromisoformat(wk["start"]), date.fromisoformat(wk["end"])
                while dd <= de:
                    c = _dv.get((bu, dd.isoformat()))
                    if c:
                        q += c["qty"]; v += c["val"]
                    dd += timedelta(days=1)
                cells.append({"avg": (round(v / q) if q else None), "qty": int(q)})
            _pw_bags.append({"name": w["name"], "was": w["priceWas"], "now": w["priceNow"], "cells": cells})
        why["priceWeeks"] = {
            "weeks": [{"label": wk["label"], "start": wk["start"], "end": wk["end"], "off": wk["off"]}
                      for wk in lift["weekly"]],
            "bags": _pw_bags,
        }

    TO = {
        "name":       CFG["name"],
        "market":     CFG["market"],
        "shops":      CFG.get("shops") or [],
        "scopeLabel": ("Nairobi CBD &middot; " + ", ".join(CFG["shops"])) if CFG.get("shops") else CFG["market"],
        "startDate":  CFG["startDate"],
        "endDate":    CFG["endDate"],
        "timeLabel":  _time_label,
        "windowLabel": _win_label(CFG["startDate"], CFG["endDate"])
                       + (" &middot; " + _time_label + " daily" if _time_label else ""),
        "lift":       lift,
        "why":        why,
        "salesLive":  sales_live,
        "bags":       bag_rows,
        "totalSold":  total_sold,
        "totalPosts": total_posts,
        "perPost":    round(total_sold / total_posts, 1) if total_posts else None,
        "bestName":   best["name"]  if best  else "",
        "bestSold":   best["sold"]  if best  else 0,
        "mostPName":  mostp["name"] if mostp else "",
        "mostPosts":  mostp["posts"] if mostp else 0,
    }

    return TO


# ── DRIVER: build all of the month's offers, stacked on one page ──
# The month-rollover archive + config-clear is handled by month_end.py (it pins
# the closing month, archives its offers to Supabase via monthly_report.py →
# push_to_supabase.py, then clears this config), NOT here — this generator runs
# on every refresh/snapshot and must never race the archive or wipe live data.

if __name__ == "__main__":
    cfg = load_config()

    # Build every live offer for the current month (stacked on the page).
    TO_LIST = [build_offer(off) for off in cfg["offers"]]
    payload = {"month": cfg["month"], "offers": TO_LIST}

    # ── INJECT ────────────────────────────────────────────────
    inline_script = (
        "<!-- TIMED_DATA_START -->\n"
        "<script>\n"
        "const TO_DATA = " + json.dumps(payload, ensure_ascii=False) + ";\n"
        "const TO_LIST = TO_DATA.offers;\n"
        "const TO = TO_LIST[0] || null;\n"      # back-compat: first offer
        "</script>\n"
        "<!-- TIMED_DATA_END -->"
    )

    html_path = os.path.join(BASE_DIR, "timed_offers.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    html = re.sub(r"<!-- TIMED_DATA_START -->.*?<!-- TIMED_DATA_END -->",
                  inline_script, html, flags=re.DOTALL)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    if not os.environ.get("DENRI_LAUNCHER"):
        webbrowser.open_new_tab(pathlib.Path(html_path).as_uri())

    print(f"timed_offers.html updated  ({cfg['month']}, {len(TO_LIST)} offer(s)).")
    for TO in TO_LIST:
        lift = TO.get("lift")
        print(f'  "{TO["name"] or "Timed Offer"}"  ({TO["windowLabel"]}, {TO["scopeLabel"]})')
        print(f"    Sales source     : {'Odoo (live)' if TO['salesLive'] else 'DB UNREACHABLE — zeros'}")
        if lift:
            print(f"    LIFT: offer {lift['offerPerDay']}/day vs pre-offer {lift['basePerDay']}/day "
                  f"-> {('+' if (lift['liftPct'] or 0) >= 0 else '')}{lift['liftPct']}%")
        print(f"    TOTAL sold       : {fmt_int(TO['totalSold'])}   posts: {fmt_int(TO['totalPosts'])}")
    if not TO_LIST:
        print("  (no active offers — the list is free for the new month.)")
