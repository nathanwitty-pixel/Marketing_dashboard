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

# TTL disk-cache windows (minutes) for the slow Odoo lookups — a manual Refresh sets
# DENRI_FORCE_FRESH=1 to bypass and repopulate. Sales move intraday (short TTL); list/
# pricelist prices are near-static metadata (long TTL) and were the per-bag round-trip cost.
ODOO_CACHE_MIN = 30      # POS sales scans (window, daily, per-bag value, price averages)
META_CACHE_MIN = 720     # list_price / pricelist per-bag lookups (rarely change)

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

def _bags_from_file(fname):
    """Bag list from a repo CSV's 'BAG TYPE' column — unique, order-preserving. Lets an offer
    set "bagsFrom" (e.g. the Kitengela Rejects tracker → reject_stock.csv) so it stays in sync
    with that list instead of hand-listing bags."""
    path = os.path.join(BASE_DIR, str(fname).strip())
    try:
        import csv as _csv
        seen, out = set(), []
        with open(path, encoding="utf-8-sig") as f:
            for row in _csv.DictReader(f):
                b = (row.get("BAG TYPE") or row.get("Bag Type") or row.get("bag") or "").strip()
                if b and b.upper() not in seen:
                    seen.add(b.upper()); out.append(b)
        return out
    except (OSError, ValueError):
        return []


def _norm_offer(raw):
    """Normalise one offer dict into the canonical shape."""
    o = {"name": "", "market": "Kenya", "startDate": "", "endDate": "",
         "bags": list(_DEFAULT_BAGS), "prices": {}, "shops": [], "bagsFrom": ""}
    o["name"]      = str(raw.get("name", "") or "").strip()
    o["market"]    = str(raw.get("market", "Kenya") or "Kenya").strip()
    o["startDate"] = str(raw.get("startDate", "") or "").strip()
    o["endDate"]   = str(raw.get("endDate", "") or "").strip()
    # Optional: the day a clearance actually began, when it's partway through the window (the
    # window may span the whole month for counting). Splits the lift "before vs during" here.
    o["clearanceStart"] = str(raw.get("clearanceStart", "") or "").strip()
    # Optional: limit the offer to a time-of-day window (Nairobi wall time, HH:MM),
    # e.g. an evening 16:00–19:00 flash. Empty = the whole day.
    o["startTime"] = str(raw.get("startTime", "") or "").strip()
    o["endTime"]   = str(raw.get("endTime", "") or "").strip()
    # Optional: limit sales to specific POS tills (e.g. Nairobi CBD shops only).
    if isinstance(raw.get("shops"), list):
        o["shops"] = [str(s).strip() for s in raw["shops"] if str(s).strip()]
    if isinstance(raw.get("bags"), list) and raw["bags"]:
        o["bags"] = [str(b).strip() for b in raw["bags"] if str(b).strip()]
    # Optional: pull the bag list from a repo CSV (e.g. reject_stock.csv) so a tracker stays
    # in sync with that list. A non-empty bagsFrom overrides the inline bags[].
    o["bagsFrom"] = str(raw.get("bagsFrom", "") or "").strip()
    if o["bagsFrom"]:
        _fb = _bags_from_file(o["bagsFrom"])
        if _fb:
            o["bags"] = _fb
    # Optional unit-price band (isolates a clearance sold at set tiers from full-price sales
    # of the same bags at the same till). e.g. Kitengela rejects: maxPrice 1600.
    o["minPrice"] = safe_int(raw.get("minPrice")) if raw.get("minPrice") else 0
    o["maxPrice"] = safe_int(raw.get("maxPrice")) if raw.get("maxPrice") else 0
    # Optional product-name filter — the exact way to isolate a tagged range, e.g. the
    # Kitengela rejects are Odoo products with "[REJECT]" in the name.
    o["nameLike"] = str(raw.get("nameLike", "") or "").strip()
    # Optional: source the In-stock figure from a repo CSV's UNITS column (physical stock)
    # instead of live Odoo on-hand — e.g. Kitengela rejects → reject_stock.csv.
    o["stockFrom"] = str(raw.get("stockFrom", "") or "").strip()
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

# Optional unit-price band. Used to isolate the Kitengela reject clearance (sold at the
# 1,000/1,500 tiers) from the same shop's full-price sales of the same bag types: a
# maxPrice ≈ 1,600 keeps the clearance lines and drops normal-price ones (which start ~1,724).
def _price_sql(min_price, max_price):
    parts = []
    if isinstance(min_price, (int, float)) and min_price > 0:
        parts.append("pl.price_unit >= %g" % float(min_price))
    if isinstance(max_price, (int, float)) and max_price > 0:
        parts.append("pl.price_unit <= %g" % float(max_price))
    return ("  AND " + " AND ".join(parts) + " ") if parts else ""


# Optional product-name filter — the precise way to isolate a tagged range. The Kitengela
# rejects are distinct Odoo products with "[REJECT]" in the name, so nameLike "[REJECT]" counts
# exactly those (Postgres LIKE only treats % and _ as special, so [ ] are literal).
def _name_sql(pattern):
    pattern = (pattern or "").strip()
    if not pattern:
        return ""
    return "  AND COALESCE(pt.\"name\",'') ILIKE '%" + pattern.replace("'", "''") + "%' "

# Per-offer globals — the SQL helpers below read _BAGS_UP / _SHOP_SQL / _TIME_SQL / _PRICE_SQL,
# and the build block reads CFG / BAGS; build_offer() rebinds all of them before each offer.
CFG = {"name": "", "market": "Kenya", "startDate": "", "endDate": "",
       "bags": list(_DEFAULT_BAGS), "prices": {}, "shops": []}
BAGS = CFG["bags"]
_BAGS_UP = [b.upper() for b in BAGS]
_SHOP_SQL = ""
_TIME_SQL = ""
_PRICE_SQL = ""
_NAME_SQL = ""
# Quantity clause. Default counts sales only (qty > 0 = gross). A name-filtered clearance
# tracker (e.g. the Kitengela rejects) uses qty <> 0 so refunds/returns net out — matching
# the Monthly Sales / Current Performance reject figure (net), which its Sales total is too.
_QTY_SQL = " AND pl.qty > 0 "

# Catch-all bucket for name-filtered (e.g. [REJECT]) offers: units that match the name
# filter but whose product name doesn't map to a configured bag — colour/condition or
# plural/variant spellings (e.g. "Moon Bag …" vs the sheet's "Moon Bags", "Mega …" vs
# "Mega Bagpack", "Standard Travel …" vs "Travel"). Without this they were silently
# dropped, so the per-bag table under-counted the true reject total.
_OTHER_REJECTS = "Other rejects"


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
    # Fetch every bag product's sales in scope and bucket in Python (via _bucket) — far cheaper
    # than OR-ing 60-70+ ILIKE patterns in SQL (measured ~3× faster on a month of Kenya sales).
    params = {"s": start, "e": end}
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
      AND p.state IN ('done','paid'){_QTY_SQL}
      AND lower(COALESCE(pc."name",'')) NOT IN {non_kenya}
    {_SHOP_SQL}{_TIME_SQL}{_PRICE_SQL}{_NAME_SQL}
      AND COALESCE(pt."name",'') NOT LIKE '%+%'
      AND COALESCE(pt."name",'') NOT ILIKE '%delivery%'
      AND COALESCE(pt."name",'') NOT ILIKE '%customization%'
      AND COALESCE(pt."name",'') NOT ILIKE '%strap%'
      AND COALESCE(pt."name",'') NOT ILIKE '%sample%'
      AND COALESCE(pcat."name",'') NOT ILIKE '%Pos%'
    GROUP BY pt."name"
    """
    df = db.run_query_cached(q, params, ttl_min=ODOO_CACHE_MIN)
    if df is None or df.empty:
        return out, True
    for _, r in df.iterrows():
        b = _bucket(r["product"])
        if b:
            out[b] += int(r["bags"] or 0)
        elif _NAME_SQL:
            # Name-filtered offer (e.g. [REJECT]): keep unbucketed matches so the total is
            # honest — collect them under the catch-all bag instead of dropping them.
            k = _OTHER_REJECTS.upper()
            out[k] = out.get(k, 0) + int(r["bags"] or 0)
    return out, True


def odoo_daily_kenya(bags, start, end, name_sql=None):
    """{date_iso: bags} — daily Kenya bags for the offer bags across [start,end],
    used to measure the before-vs-during-offer lift. `name_sql` overrides the offer's name
    filter (e.g. pass a "NOT ILIKE '%[REJECT]%'" clause to get the NORMAL, full-price series of
    the same bags to compare against the reject clearance). {} if DB unreachable."""
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
    _nm = _NAME_SQL if name_sql is None else name_sql
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
      AND p.state IN ('done','paid'){_QTY_SQL}
      AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
    {_SHOP_SQL}{_TIME_SQL}{_PRICE_SQL}{_nm}
      AND COALESCE(pt."name",'') NOT LIKE '%+%'
      AND COALESCE(pt."name",'') NOT ILIKE '%delivery%'
      AND COALESCE(pt."name",'') NOT ILIKE '%customization%'
      AND COALESCE(pt."name",'') NOT ILIKE '%strap%'
      AND COALESCE(pt."name",'') NOT ILIKE '%sample%'
      AND COALESCE(pcat."name",'') NOT ILIKE '%Pos%'
      AND ({like_clauses})
    GROUP BY 1 ORDER BY 1
    """
    df = db.run_query_cached(q, params, ttl_min=ODOO_CACHE_MIN)
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
    params = {"s": start, "e": end}
    base = """
    FROM pos_order p
    JOIN pos_order_line pl ON pl.order_id = p.id
    LEFT JOIN pos_session ps ON p.session_id = ps.id
    LEFT JOIN pos_config pc ON ps.config_id = pc.id
    LEFT JOIN product_product pp ON pl.product_id = pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
    LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
    WHERE p.date_order::date BETWEEN CAST(:s AS date) AND CAST(:e AS date)
      AND p.state IN ('done','paid')
      AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
      AND COALESCE(pt."name",'') NOT LIKE '%+%'
      AND COALESCE(pt."name",'') NOT ILIKE '%delivery%'
      AND COALESCE(pt."name",'') NOT ILIKE '%customization%'
      AND COALESCE(pt."name",'') NOT ILIKE '%strap%'
      AND COALESCE(pt."name",'') NOT ILIKE '%sample%'
      AND COALESCE(pt."name",'') NOT ILIKE '%KES discount%'
      AND COALESCE(pcat."name",'') NOT ILIKE '%Pos%'
    """ + _QTY_SQL + _SHOP_SQL + _TIME_SQL + _PRICE_SQL + _NAME_SQL
    # per offer-bag — fetch all products, bucket in Python (only configured bags kept)
    df = db.run_query_cached(f'SELECT pt."name" AS product, SUM(pl.qty)::int AS qty, '
                             f'SUM(pl.price_subtotal_incl)::numeric AS val {base} '
                             f'GROUP BY pt."name"', params, ttl_min=ODOO_CACHE_MIN)
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            b = _bucket(r["product"])
            if b:
                prices[b]["qty"] += int(r["qty"] or 0)
                prices[b]["val"] += float(r["val"] or 0)
    # catalogue-wide avg
    dfc = db.run_query_cached(f'SELECT ROUND(SUM(pl.price_subtotal_incl)/NULLIF(SUM(pl.qty),0)) AS avg {base}',
                              {"s": start, "e": end}, ttl_min=ODOO_CACHE_MIN)
    if dfc is not None and not dfc.empty and dfc.iloc[0]["avg"] is not None:
        catalog = int(dfc.iloc[0]["avg"])
    return prices, catalog


def _sheet_category_by_bag(bags):
    """{BAG_UPPER: category} — the bag's category label only, from the product catalogue
    (product_catalog.csv, the old STOCK_LEVELS col B/D labels; lib/odoo_tabs). STOCK is
    never read from the sheet (see kenya_stock_by_bag)."""
    from lib import odoo_tabs
    out = {}
    rows = odoo_tabs.catalog_rows()
    if len(rows) <= 1:   # catalogue missing → the old sheet read
        rows = get_gspread_client().open_by_key(SPREADSHEET_ID).worksheet("STOCK_LEVELS").get_all_values()
    for row in rows[1:]:
        if len(row) < 4:
            continue
        b = _bucket(row[3])
        if not b or b in out:
            continue
        out[b] = str(row[1]).strip() if len(row) > 1 else ""
    return out


def _stock_from_file(fname):
    """{BAG_UPPER: units} — physical stock summed per BAG TYPE from a repo CSV's UNITS column.
    Lets an offer set "stockFrom" (e.g. Kitengela Rejects → reject_stock.csv) so the In-stock
    figure is the actual reject stock on the ground, not Odoo's live Kenya on-hand."""
    path = os.path.join(BASE_DIR, str(fname).strip())
    out = {}
    try:
        import csv as _csv
        with open(path, encoding="utf-8-sig") as f:
            for row in _csv.DictReader(f):
                b = (row.get("BAG TYPE") or row.get("Bag Type") or row.get("bag") or "").strip().upper()
                try:
                    u = int(float(row.get("UNITS") or row.get("Units") or 0))
                except (ValueError, TypeError):
                    u = 0
                if b:
                    out[b] = out.get(b, 0) + u
    except (OSError, ValueError):
        return {}
    return out


# ── Per-variant reject rows (Colour / Category / Product / Bag Type filterable) ──────
# Primary colour tokens used to reduce both Odoo product names ("Moon Bag Black [REJECT]")
# and reject_stock.csv COLOR values ("BLACK TT", "WOOVEN BLACK") to one comparable colour,
# so a sold variant and its stock line up. Multi-word first (longest-match wins).
_PRIMARY_COLOURS = ["DARK BROWN", "CHOCOLATE", "MUSTARD", "MAROON", "PURPLE", "CRACKED",
                    "BROWN", "BLACK", "GREEN", "BEIGE", "SPICE", "WOVEN", "WOOVEN",
                    "GREY", "GRAY", "NUDE", "CHOCO", "NAVY", "BLUE", "PINK", "RED"]

def _parse_colour(name):
    """First primary colour token found in a name (longest-first), Title-cased; '' if none."""
    up = " " + re.sub(r"[^A-Z0-9 ]+", " ", str(name).upper()) + " "
    for c in _PRIMARY_COLOURS:
        if (" " + c + " ") in up:
            return c.title()
    return ""

def _singular_tokens(s):
    """Word tokens, plural 's' trimmed, so 'MOON BAGS' and 'Moon Bag Black' share tokens."""
    toks = [w for w in re.split(r"[^A-Z0-9]+", str(s).upper()) if w]
    return [w[:-1] if (len(w) > 3 and w.endswith("S")) else w for w in toks]

def reject_variants(start, end):
    """Per-[REJECT]-product variant rows for a name-filtered offer, for the filterable table:
    {product, colour, bagType, category, sold, stock, priceWas, priceNow, discountKes,
    discountPct}. Sold/price come live from Odoo; stock is merged from the reject_stock.csv
    file per (bag, colour). Colour/bag matching is best-effort, but totals still sum to the
    true reject sold and stock. Returns [] when no nameLike filter or the DB is unreachable."""
    if not _NAME_SQL:
        return []
    try:
        from lib import db
        ok, _ = db.check_connection()
        if not ok:
            return []
    except Exception:
        return []
    cats = _sheet_category_by_bag(BAGS)

    # Stock variants from the CSV: (BAG_UP, COLOUR_UP) -> units, plus a bag-token index.
    stock_var, csv_bags, seen = {}, [], set()
    try:
        import csv as _csv
        src = os.path.join(BASE_DIR, str(CFG.get("stockFrom") or "reject_stock.csv").strip())
        with open(src, encoding="utf-8-sig") as f:
            for row in _csv.DictReader(f):
                bt = (row.get("BAG TYPE") or "").strip().upper()
                if not bt:
                    continue
                col = _parse_colour(row.get("COLOR") or row.get("COLOUR") or "") \
                      or (row.get("COLOR") or "").strip().title()
                stock_var[(bt, col.upper())] = stock_var.get((bt, col.upper()), 0) + safe_int(row.get("UNITS"))
                if bt not in seen:
                    seen.add(bt); csv_bags.append((bt, _singular_tokens(bt)))
    except OSError:
        pass
    csv_bags.sort(key=lambda x: -len(x[1]))     # match the most-specific bag first

    def _match_bag(clean_up):
        toks = set(_singular_tokens(clean_up))
        for bt, bt_toks in csv_bags:            # longest first
            if bt_toks and all(t in toks for t in bt_toks):
                return bt
        return None

    non_kenya = "('sinza','dar-es-alam','uganda')"
    q = f"""
    SELECT pt."name" AS product, SUM(pl.qty)::int AS qty,
           SUM(pl.price_subtotal_incl)::numeric AS val, MAX(pt.list_price)::numeric AS lp
    FROM pos_order p
    JOIN pos_order_line pl ON pl.order_id = p.id
    LEFT JOIN pos_session ps ON p.session_id = ps.id
    LEFT JOIN pos_config pc ON ps.config_id = pc.id
    LEFT JOIN product_product pp ON pl.product_id = pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
    LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
    WHERE p.date_order::date BETWEEN CAST(:s AS date) AND CAST(:e AS date)
      AND p.state IN ('done','paid'){_QTY_SQL}
      AND lower(COALESCE(pc."name",'')) NOT IN {non_kenya}
    {_SHOP_SQL}{_TIME_SQL}{_PRICE_SQL}{_NAME_SQL}
      AND COALESCE(pt."name",'') NOT LIKE '%+%'
      AND COALESCE(pt."name",'') NOT ILIKE '%delivery%'
      AND COALESCE(pt."name",'') NOT ILIKE '%customization%'
      AND COALESCE(pt."name",'') NOT ILIKE '%strap%'
      AND COALESCE(pt."name",'') NOT ILIKE '%sample%'
      AND COALESCE(pcat."name",'') NOT ILIKE '%Pos%'
    GROUP BY pt."name"
    """
    df = db.run_query_cached(q, {"s": start, "e": end}, ttl_min=ODOO_CACHE_MIN)
    rows = []
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            raw = str(r["product"])
            clean = re.sub(r"\s+", " ", re.sub(r"\[?REJECT\]?", "", raw, flags=re.I)).strip()
            bag = _match_bag(clean.upper()) or _bucket(clean) or _OTHER_REJECTS.upper()
            colour = _parse_colour(clean)
            qty = int(r["qty"] or 0)
            now = round(float(r["val"] or 0) / qty) if qty else None
            was = round(float(r["lp"]) * TAX_INCL) if r["lp"] else None
            if was and now and now > was:
                now = was
            # consume the matching stock line so it isn't double-listed below
            stk = stock_var.pop((bag, colour.upper()), 0)
            disc = (was - now) if (was and now) else None
            rows.append({
                "product": clean or raw, "colour": colour,
                "bagType": (_OTHER_REJECTS if bag == _OTHER_REJECTS.upper() else bag.title()),
                "category": ("Other / variant names" if bag == _OTHER_REJECTS.upper() else cats.get(bag, "")),
                "sold": qty, "stock": int(stk), "priceWas": was, "priceNow": now,
                "rev": round(float(r["val"] or 0)),   # actual realised revenue (incl-tax) for this variant
                "discountKes": (disc if (disc and disc > 0) else None),
                "discountPct": (round((now - was) / was * 100) if (was and now and was > 0) else None),
            })
    # Stock-only variants (in the reject pile but nothing sold in the window).
    for (bt, col), units in stock_var.items():
        if units <= 0:
            continue
        rows.append({
            "product": (bt.title() + ((" " + col.title()) if col else "")).strip(),
            "colour": col.title(), "bagType": bt.title(), "category": cats.get(bt, ""),
            "sold": 0, "stock": int(units), "priceWas": None, "priceNow": None,
            "rev": 0, "discountKes": None, "discountPct": None,
        })
    rows.sort(key=lambda x: (-x["sold"], -x["stock"]))
    return rows


def kenya_stock_by_bag(bags):
    """{BAG_UPPER: {stock, category}} for the configured bags.

    STOCK is LIVE Kenya Odoo on-hand ONLY (internal shop locations), bucketed to
    each configured bag via _bucket(); the sheet is never used for stock, so a bag
    Odoo has no on-hand for — or an unreachable DB — shows 0. CATEGORY is a
    non-stock label and still comes from STOCK_LEVELS col B.

    Exception: if the current offer sets "stockFrom" (a repo CSV), In-stock is that file's
    physical UNITS per bag — used by the Kitengela reject tracker so stock = the reject pile."""
    cats = _sheet_category_by_bag(bags)
    _src = CFG.get("stockFrom") if isinstance(CFG, dict) else ""
    if _src:
        fs = _stock_from_file(_src)
        print("  Stock source     : %s (physical reject stock units)" % _src)
        return {b: {"stock": fs.get(b, 0), "category": cats.get(b, "")} for b in _BAGS_UP}
    try:
        from lib import stock as _stock
        odoo = _stock.odoo_stock_by_product("kenya")
    except Exception:                                        # noqa: BLE001
        odoo = {}
    agg = {}
    for name, qty in odoo.items():
        b = _bucket(name)
        if b:
            agg[b] = agg.get(b, 0) + int(qty or 0)
    out = {}
    for b in _BAGS_UP:
        out[b] = {"stock": agg.get(b, 0), "category": cats.get(b, "")}
    print("  Stock source     : Odoo (live Kenya shop on-hand)" if odoo
          else "  Stock source     : Odoo unreachable — stock shown as 0 (no sheet fallback)")
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
        df = db.run_query_cached(
            'SELECT ROUND(pt.list_price * :tax) AS incl, COUNT(*) AS n '
            'FROM product_template pt '
            'WHERE pt."name" ILIKE :pat AND pt."name" NOT LIKE \'%+%\' '
            '  AND COALESCE(pt.active, true) = true AND pt.list_price > 0 '
            'GROUP BY 1 ORDER BY n DESC, incl ASC LIMIT 1',
            {"tax": TAX_INCL, "pat": b + "%"}, ttl_min=META_CACHE_MIN)
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
        df = db.run_query_cached(
            'SELECT ROUND(i.fixed_price * :tax) AS incl, COUNT(*) AS n '
            'FROM product_pricelist_item i JOIN product_template pt ON pt.id = i.product_tmpl_id '
            'WHERE pt."name" ILIKE :pat AND pt."name" NOT LIKE \'%+%\' '
            "  AND i.compute_price = 'fixed' AND i.fixed_price > 0 "
            '  AND (i.date_start IS NULL OR i.date_start::date <= CAST(:e AS date)) '
            '  AND (i.date_end   IS NULL OR i.date_end::date   >= CAST(:s AS date)) '
            'GROUP BY 1 ORDER BY n DESC, incl ASC LIMIT 1',
            {"tax": TAX_INCL, "pat": b + "%", "s": start, "e": end}, ttl_min=META_CACHE_MIN)
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
         "  AND p.state IN ('done','paid') "
         '  AND lower(COALESCE(pc."name",\'\')) NOT IN (\'sinza\',\'dar-es-alam\',\'uganda\') '
         + _QTY_SQL + _SHOP_SQL + _TIME_SQL + _PRICE_SQL + _NAME_SQL +
         '  AND COALESCE(pt."name",\'\') NOT LIKE \'%+%\' '
         '  AND COALESCE(pt."name",\'\') NOT ILIKE \'%delivery%\' '
         '  AND COALESCE(pt."name",\'\') NOT ILIKE \'%sample%\' '
         '  AND COALESCE(pcat."name",\'\') NOT ILIKE \'%Pos%\' '
         f'  AND ({like}) GROUP BY 1, 2')
    df = db.run_query_cached(q, params, ttl_min=ODOO_CACHE_MIN)
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
    global BAGS, _BAGS_UP, _SHOP_SQL, _TIME_SQL, _PRICE_SQL, _NAME_SQL, _QTY_SQL, CFG
    CFG = offer
    BAGS = offer["bags"]
    _BAGS_UP = [b.upper() for b in BAGS]
    _SHOP_SQL = _shop_sql(offer.get("shops"))
    _TIME_SQL = _time_sql(offer.get("startTime"), offer.get("endTime"))
    _PRICE_SQL = _price_sql(offer.get("minPrice"), offer.get("maxPrice"))
    _NAME_SQL = _name_sql(offer.get("nameLike"))
    # Net refunds for a clearance tracker so its total matches the Monthly/Current-Performance
    # reject figure; keep gross (qty > 0) for a normal campaign.
    _QTY_SQL = " AND pl.qty <> 0 " if offer.get("nameLike") else " AND pl.qty > 0 "

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
        # A clearance can begin partway through the offer window — e.g. the Kitengela rejects: the
        # window is the whole month (for counting every reject), but the clearance itself only
        # started on the 18th. `clearanceStart` splits "before" vs "during" at that day (comparing
        # the pre-clearance days from the 1st to the clearance days), so the weekly makes sense and
        # you can judge whether the Kitengela clearance was a good idea. Empty = split at the offer
        # start as usual.
        _split = _os
        if CFG.get("clearanceStart"):
            try:
                _split = date.fromisoformat(CFG["clearanceStart"])
            except (ValueError, TypeError):
                _split = _os
        # Only count clearance days that have actually ELAPSED — dividing a still-running window's
        # sales by its full length (e.g. 13 days to the 30th when only a few have passed) would
        # understate the daily pace. For a finished offer this is just its end date.
        _oe_eff = min(_oe, date.today())
        _dend = _oe_eff
        _daily = odoo_daily_kenya(BAGS, _mstart.isoformat(), _dend.isoformat())
        # For a name-filtered clearance (rejects), also pull the NORMAL (non-[REJECT]) daily for the
        # SAME bags/shops — so the panel can compare normal full-price sales vs the clearance sales.
        _normal_daily = odoo_daily_kenya(BAGS, _mstart.isoformat(), _dend.isoformat(),
                                         name_sql=" AND COALESCE(pt.\"name\",'') NOT ILIKE '%[REJECT]%' ") \
            if _NAME_SQL else {}
        if _daily:
            offer_days = (_oe_eff - _split).days + 1
            base_days  = (_split - _mstart).days          # days before the clearance/offer
            def _sum(a, b):
                return sum(v for k, v in _daily.items() if a <= k <= b)
            base_total  = _sum(_mstart.isoformat(), (_split - timedelta(days=1)).isoformat())
            offer_total = _sum(_split.isoformat(), _oe_eff.isoformat())
            base_per_day  = round(base_total / base_days, 1) if base_days else 0.0
            offer_per_day = round(offer_total / offer_days, 1) if offer_days else 0.0
            lift_pct = round((offer_per_day - base_per_day) / base_per_day * 100) if base_per_day else None
            # daily series for the chart (month start → elapsed end; clearance/offer days flagged)
            _series = []
            _d = _mstart
            while _d <= _oe_eff:
                k = _d.isoformat()
                _series.append({"date": k, "bags": _daily.get(k, 0),
                                "normal": _normal_daily.get(k, 0),
                                "off": _split.isoformat() <= k <= _oe_eff.isoformat()})
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
                if _split <= _d <= _oe_eff:
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
                "baseStart": _mstart.isoformat(), "baseEnd": (_split - timedelta(days=1)).isoformat(),
                "baseDays": base_days, "baseTotal": base_total, "basePerDay": base_per_day,
                "offerDays": offer_days, "offerTotal": offer_total, "offerPerDay": offer_per_day,
                "liftPct": lift_pct, "daily": _series, "weekly": weekly,
                "clearanceStart": (_split.isoformat() if CFG.get("clearanceStart") else ""),
            }
            # Normal (full-price) vs clearance (reject) over the whole month-to-date window
            # (e.g. 1st→21st), per day — the comparison the reject panel shows.
            if _NAME_SQL:
                _win_days = (_oe_eff - _mstart).days + 1
                _clr_total = _sum(_mstart.isoformat(), _oe_eff.isoformat())      # reject total
                _nrm_total = sum(v for k, v in _normal_daily.items()
                                 if _mstart.isoformat() <= k <= _oe_eff.isoformat())
                lift["cmpNormal"] = True
                lift["winStart"] = _mstart.isoformat(); lift["winEnd"] = _oe_eff.isoformat()
                lift["winDays"] = _win_days
                lift["normalTotal"] = _nrm_total
                lift["normalPerDay"] = round(_nrm_total / _win_days, 1) if _win_days else 0.0
                lift["clearanceTotal"] = _clr_total
                lift["clearancePerDay"] = round(_clr_total / _win_days, 1) if _win_days else 0.0
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
    # Catch-all row for name-filtered offers (units that matched [REJECT] but no configured
    # bag) so the table's total equals the real reject total, not the bucketed subset.
    _other_sold = int(sales_map.get(_OTHER_REJECTS.upper(), 0))
    if _other_sold:
        bag_rows.append({"name": _OTHER_REJECTS, "sold": _other_sold, "posts": 0,
                         "perPost": None, "isOther": True})
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
        # pricelist). Otherwise "now" = the REALISED avg sale price in the window (what the bag
        # actually left at — e.g. the reject clearance price), then the Odoo offer pricelist as a
        # last resort. A clearance "now" can't exceed the "was", so a stray pricelist value
        # (some products carry a wrong fixed_price) is clamped down instead of showing garbage.
        was = (pr.get("was") or None) or _list_prices.get(bu)
        now = (pr.get("now") or None) or off_p or _offer_prices.get(bu)
        if was and now and now > was:
            now = round(off_p) if (off_p and off_p <= was) else was
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
        _is_other = bool(r.get("isOther"))
        why_bags.append({
            "name": r["name"], "sold": r["sold"], "posts": r["posts"], "stock": sm["stock"],
            "priceWas": was, "priceNow": now, "discountKes": disc_kes,
            "discountPct": disc_pct, "discounted": discounted, "soldAt": sold_at,
            "prePerDay": pre_pd, "offerPerDay": off_pd, "bagLift": bag_lift,
            "category": ("Other / variant names" if _is_other else sm["category"]),
            "isOther": _is_other,
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
            f"Real inventory behind them — <b>{_total_stock:,} still in stock</b> "
            f"(led by {_topstock['name']} at {_topstock['stock']:,}). The offer draws down a genuine stock position, not a token one."})

    # 4) Season — only for the all-cut back-to-school campaign, not a plain clearance tracker.
    if _all_cut and _cats:
        _season_bag = (" and ".join(_zero_post[:2]) + " even sold on zero marketing posts (pure demand). ") if _zero_post else ""
        _insights.append({"tag": "Season", "text":
            f"All six sit in <b>{', '.join(c.title() for c in _cats)}</b> — school categories — and the step-up landed in the offer week as schools opened. "
            f"{_season_bag}The timing fits the sales pattern as much as the price cut does."})

    if _all_cut and _deepest:
        _verdict = (f"<b>Good move.</b> All six ran a real <b>{min(_pcts)}–{max(_pcts)}% cut</b> and daily sales rose <b>{_lift_txt}</b> during back-to-school. "
                    f"The catch: <b>discount depth didn't pick the winners</b> — the deepest cut ({_deepest['name']}, {_deepest['discountPct']}%) sold least, while the popular school lines led. "
                    f"Repeat the timing; you can likely <b>trim the deepest cuts</b> on the slow movers without losing volume.")
    else:
        _verdict = ("<b>Tracking live.</b> Per-bag sales over the window for the scoped tills — "
                    "use it to see which lines are clearing and which are stalling, and where to push or restock.")

    why = {"totalStock": _total_stock, "categories": _cats, "allCut": _all_cut,
           "bags": why_bags, "insights": _insights, "verdict": _verdict,
           # Per-variant rows (Colour/Category/Product/Bag Type filterable). Only populated
           # for a name-filtered offer (e.g. the Kitengela [REJECT] tracker); [] otherwise.
           "variants": reject_variants(CFG["startDate"], CFG["endDate"])}

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
        "scopeLabel": (
            ("Nairobi CBD &middot; " + ", ".join(CFG["shops"]))
            if set(s.lower() for s in (CFG.get("shops") or [])) == {"hazina", "hilton", "starmall", "ktda shop"}
            else (CFG["market"] + " &middot; " + ", ".join(CFG["shops"])) if CFG.get("shops")
            else CFG["market"]),
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
            _lp = lift.get('liftPct')
            _lpx = (('n/a (no pre-offer days)' if not lift.get('baseDays') else 'n/a (0 sold before)')
                    if _lp is None else (('+' if _lp >= 0 else '') + str(_lp) + '%'))
            print(f"    LIFT: offer {lift['offerPerDay']}/day vs pre-offer {lift['basePerDay']}/day -> {_lpx}")
        print(f"    TOTAL sold       : {fmt_int(TO['totalSold'])}   posts: {fmt_int(TO['totalPosts'])}")
    if not TO_LIST:
        print("  (no active offers — the list is free for the new month.)")
