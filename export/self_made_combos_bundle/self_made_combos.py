"""
self_made_combos.py
─────────────────────────────────────────────────────────────────
Self-Made Combos vs Running Combos — for the current month (live).

Staff create ad-hoc combos on the POS via a Combo Request (Odoo model
pos.combo.request → the CBR/2026/NNNN references). Each request carries a
`combo_product_id` that points at the product_template created for that combo,
so when it sells it lands in POS sales (pos_order_line) linked back to the CBR.

We now read the real request table (SELECT access granted), so every combo sold
this month is split by the *actual* CBR link, not a name heuristic:
  • Self-made  — the sold product's template IS a CBR combo_product_id
  • Running    — everything else (the official offer-sheet combos)

We also surface the request log itself — CBR ref · combo · shop · requested by ·
approved-by-Lloyd · state · date — including rejected/pending requests that never
reached the tills.

Scoped to the Kenya tills (the combos run there). Injects `SMC` into
self_made_combos.html between the SMC_DATA markers.
─────────────────────────────────────────────────────────────────
"""

import re, os, json, webbrowser, pathlib, datetime

import pandas as pd

from lib import db, report_month

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "self_made_combos.html")


def fmt(n):
    return f"{int(round(n)):,}"


# Combos sold this month, split by the real CBR link (combo_product_id).
COMBO_SQL = """
WITH cbr AS (
    SELECT DISTINCT combo_product_id
    FROM pos_combo_request
    WHERE combo_product_id IS NOT NULL
)
SELECT pt."name" AS product,
       pt.id      AS tmpl_id,
       SUM(pl.qty)::int AS qty,
       ROUND(SUM(pl.price_subtotal_incl))::numeric AS value,
       (pt.id IN (SELECT combo_product_id FROM cbr)) AS is_cbr,
       -- include_all = the POS combo picker offers the FULL range of a category
       -- (e.g. "Select any 2" across every Lola/Mini Zuri/Trecento colour). That
       -- is the defining mark of an official running combo; a self-made CBR combo
       -- is a fixed, specific pairing (include_all is false).
       COALESCE((SELECT BOOL_OR(pcx.include_all) FROM product_combo pcx
                 WHERE pcx.product_template_id = pt.id), FALSE) AS include_all,
       -- Colour range: total picker options across the combo's categories. A
       -- running/official combo offers a wide range (the shop attendant chooses
       -- the colour); a self-made CBR combo is locked to one specific pairing.
       (SELECT COUNT(*) FROM product_combo pcx
          JOIN product_combo_product_product_rel r ON r.product_combo_id = pcx.id
        WHERE pcx.product_template_id = pt.id) AS colour_options
FROM pos_order p
JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
  AND p.state IN ('done', 'paid')
  AND pl.qty <> 0
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
  -- A combo follows the naming convention "A + B" — every real running and
  -- self-made combo does. We do NOT treat "has a product_combo definition" as
  -- sufficient: single bags occasionally carry a stray combo/include_all flag
  -- (e.g. "Big Man Bag Grey", a KES 1,810 single bag), which must not be counted.
  AND pt."name" LIKE '%+%'
  AND pt."name" NOT ILIKE '%delivery%'
  AND pt."name" NOT ILIKE '%customi%'
GROUP BY pt."name", pt.id
ORDER BY qty DESC, value DESC
"""

# Per combo SALE, the bags actually printed — Odoo stores the chosen components in
# pos_order_line.combo_product_attribute_values (e.g. "Mini Umbra Grey", "Mega Black").
# This lets us attribute a combo like "Mega + Man Bag or Mini Umbra or Neo Man Bag"
# to the specific bag the customer picked, instead of the bundle as a whole.
COMBO_COMPONENTS_SQL = """
SELECT pt.id AS tmpl_id, pl.qty::int AS qty,
       COALESCE(pl.combo_product_attribute_values, '') AS attrs
FROM pos_order p
JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
  AND p.state IN ('done', 'paid') AND pl.qty <> 0
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
  AND pt."name" LIKE '%+%'
"""

# Odoo location codes for live-stock fallback (excludes the WIP/production
# placeholder locations that hold a bogus ~44k/variant).
_KENYA_SHOP_CODES = ('STAR', 'MSA', 'NAKS', 'ELD', 'KSM', 'MERU', 'THK', 'HAZ',
                     'KITE', 'NAN', 'KAK', 'HTN', 'KSI', 'KTDA', 'BUSIA', 'RONG')
_SINZA_CODES  = ('DAR',)   # Dar-es-Salaam warehouse serves the Sinza region
_UGANDA_CODES = ('UG',)

# Deal sheet location label ← Odoo POS-config (till) name. Used to break each Deal
# of the Week's Odoo sales down by the shop that actually ran it, so a per-shop card
# shows that shop's own sales — not the bag's Kenya-wide total.
_SHOP_TO_LOC = {
    "STARMALL": "Starmall", "MOMBASA": "Mombasa", "NAKURU": "Nakuru",
    "ELDORET": "Eldoret", "KISUMU": "Kisumu", "MERU": "Meru", "THIKA": "Thika",
    "HAZINA": "Hazina", "KITENGELA": "Kitengela", "NANYUKI": "Nanyuki",
    "KAKAMEGA": "Kakamega", "HILTON": "Hilton", "KISII": "Kisii",
    "KTDA SHOP": "KTDA", "BUSIA": "Busia", "RONGAI": "Rongai",
    "WEBSITE SALES": "Website",
}
# Shop → sales region, for the per-shop combo-button chips: a shop is flagged red when
# it rings less than half of the best-performing shop in its own region. The mapping is
# maintained in docs/shop-regions.md (edit the table there — no code change needed); this
# dict is the fallback if that file is missing or unparseable.
_SHOP_REGION_DEFAULT = {
    "HAZINA": "Nairobi CBD", "HILTON": "Nairobi CBD", "STARMALL": "Nairobi CBD",
    "KTDA": "Nairobi CBD",
    "KITENGELA": "Nairobi Metropolitan", "RONGAI": "Nairobi Metropolitan",
    "MOMBASA": "Coastal Region",
    "KAKAMEGA": "Western & Nyanza", "KISUMU": "Western & Nyanza",
    "KISII": "Western & Nyanza", "BUSIA": "Western & Nyanza",
    "MERU": "Central Region", "NANYUKI": "Central Region", "THIKA": "Central Region",
    "ELDORET": "Rift Valley", "NAKURU": "Rift Valley",
    "WEBSITE": "Online",
}


def _load_shop_regions():
    """Read the Shop → Region table from docs/shop-regions.md so the mapping can be
    maintained there. Parses the markdown table under the heading that mentions "shop"
    (first column = shop, second = region). Falls back to the built-in default."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "shop-regions.md")
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError:
        return dict(_SHOP_REGION_DEFAULT)
    out, in_section = {}, False
    for ln in lines:
        s = ln.strip()
        if s.startswith("#"):                                    # heading → enter/leave the shops table
            in_section = "shop" in s.lower()
            continue
        if not (in_section and s.startswith("|")):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 2:
            continue
        shop, region = cells[0], cells[1]
        if not shop or not region:
            continue
        if shop.upper() == "SHOP" or set(shop) <= set("-: "):    # header / separator row
            continue
        out[shop.upper()] = region
    return out or dict(_SHOP_REGION_DEFAULT)


_SHOP_REGION = _load_shop_regions()

# Deal sheet location label ← Odoo stock-location code (for per-shop live stock).
# Website is online-only (no physical shelf), so it has no stock code here.
_STOCK_CODE_TO_LOC = {
    "STAR": "Starmall", "MSA": "Mombasa", "NAKS": "Nakuru", "ELD": "Eldoret",
    "KSM": "Kisumu", "MERU": "Meru", "THK": "Thika", "HAZ": "Hazina",
    "KITE": "Kitengela", "NAN": "Nanyuki", "KAK": "Kakamega", "HTN": "Hilton",
    "KSI": "Kisii", "KTDA": "KTDA", "BUSIA": "Busia", "RONG": "Rongai",
}


def _odoo_stock_for(codes):
    """{UPPER(product name): on-hand units} for standalone bags in the given Odoo
    shop-location codes. Live fallback for stock the offer sheet reports as 0."""
    if not codes:
        return {}
    inlist = ", ".join("'" + c + "'" for c in codes)
    sql = f"""
    SELECT UPPER(pt."name") AS name, SUM(q.quantity)::int AS qty
    FROM stock_quant q
    JOIN stock_location l ON l.id = q.location_id AND l.usage = 'internal'
    JOIN product_product pp ON pp.id = q.product_id
    JOIN product_template pt ON pt.id = pp.product_tmpl_id
    WHERE split_part(l.complete_name, '/', 1) IN ({inlist})
      AND pt."name" NOT LIKE '%+%'
    GROUP BY UPPER(pt."name")
    HAVING SUM(q.quantity) > 0
    """
    try:
        df = db.run_query(sql, {})
    except Exception:
        return {}
    if df is None or df.empty:
        return {}
    return {str(r["name"]).upper(): int(r["qty"] or 0) for _, r in df.iterrows()}


def _odoo_stock_by_shop(code_to_loc):
    """{sheet-loc label: {UPPER(product name): on-hand units}} — live per-shop stock,
    one shop at a time, so a Deal of the Week card can show that shop's own stock."""
    codes = list(code_to_loc.keys())
    if not codes:
        return {}
    inlist = ", ".join("'" + c + "'" for c in codes)
    sql = f"""
    SELECT split_part(l.complete_name, '/', 1) AS code,
           UPPER(pt."name") AS name, SUM(q.quantity)::int AS qty
    FROM stock_quant q
    JOIN stock_location l ON l.id = q.location_id AND l.usage = 'internal'
    JOIN product_product pp ON pp.id = q.product_id
    JOIN product_template pt ON pt.id = pp.product_tmpl_id
    WHERE split_part(l.complete_name, '/', 1) IN ({inlist})
      AND pt."name" NOT LIKE '%+%'
    GROUP BY code, UPPER(pt."name")
    HAVING SUM(q.quantity) > 0
    """
    out = {}
    try:
        df = db.run_query(sql, {})
    except Exception:
        return {}
    if df is None or df.empty:
        return {}
    for _, r in df.iterrows():
        loc = code_to_loc.get(str(r["code"]).strip().upper())
        if loc:
            out.setdefault(loc, {})[str(r["name"]).upper()] = int(r["qty"] or 0)
    return out


_AUGMENTED_STOCK = {}   # Kenya bag stock (sheet + Odoo fallback), shared with _enrich_deals

# The combo-request log for the month (all states).
REQUEST_SQL = """
SELECT r.name        AS cbr,
       r.combo_name  AS combo,
       r.state       AS state,
       r.approved_by_lloyd AS lloyd,
       COALESCE(r.price_incl, 0)::numeric AS price,
       pc."name"     AS shop,
       rp."name"     AS requested_by,
       r.create_date AS requested_on,
       r.decision_date AS decided_on,
       r.reject_reason AS reject_reason,
       r.combo_product_id AS tmpl_id
FROM pos_combo_request r
LEFT JOIN pos_config  pc ON pc.id = r.config_id
LEFT JOIN res_users   ru ON ru.id = r.user_id
LEFT JOIN res_partner rp ON rp.id = ru.partner_id
WHERE r.create_date::date BETWEEN :start_date AND :end_date
ORDER BY r.create_date DESC, r.id DESC
"""

# Per-combo units sold per Sun-Sat week. WK index = weeks since the Sunday on/before
# the month's first day (:anchor, precomputed in Python), so WK1 = the week
# containing day 1, then each Sunday starts a new week — the offer sheet's structure.
_WK_EXPR = ("(((p.date_order::date - (EXTRACT(DOW FROM p.date_order::date)::int)) "
            "- :anchor) / 7 + 1)")
_COMBO_WHERE = """
  AND p.state IN ('done', 'paid') AND pl.qty <> 0
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
  AND pt."name" LIKE '%+%'
  AND pt."name" NOT ILIKE '%delivery%'
  AND pt."name" NOT ILIKE '%customi%'
"""
COMBO_WEEKLY_SQL = f"""
SELECT pt.id AS tmpl_id, pt."name" AS product, {_WK_EXPR} AS wk, SUM(pl.qty)::int AS units
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
{_COMBO_WHERE}
GROUP BY pt.id, pt."name", wk
"""
# A whole month's combo sales (all combos) per Sun-Sat week — used for the August
# baseline and the September-so-far tally.
MONTH_WEEKLY_SQL = f"""
SELECT {_WK_EXPR} AS wk, SUM(pl.qty)::int AS units
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
{_COMBO_WHERE}
GROUP BY wk ORDER BY wk
"""


def _dstr(v):
    if v is None:
        return ""
    try:
        return v.strftime("%d %b")
    except Exception:
        s = str(v)
        return s[:10] if s and s.lower() != "nat" else ""


def _read_offer_analysis():
    """Pull the Kenya offer-sheet combos + bag targets + Kenya stock from the
    Offer Type Analysis page, so the Running combos can be rendered as the same
    target cards (price · weekly sold · stock ★ · monthly/weekly target · verdict).
    We aggregate stock to a {bagType: kenyaStock} map to keep the payload small."""
    try:
        import offer_data
        oa = offer_data.build()[0]
    except Exception:
        return None
    stock_map = {}
    for s in oa.get("stockData", []):
        k = str(s.get("bagType") or "").strip().upper()
        if k:
            stock_map[k] = stock_map.get(k, 0) + (s.get("kenyaStock") or 0)

    def _region_stock(rows, key):
        m = {}
        for s in rows or []:
            k = str(s.get("bagType") or "").strip().upper()
            if k:
                m[k] = m.get(k, 0) + (s.get(key) or 0)
        return m

    return {
        "combos":          oa.get("juneCombos", []),
        "comboHeaders":    oa.get("juneComboHeaders", []),
        "bagTargets":      oa.get("bagTargets", {}),
        "stockMap":        stock_map,
        "weeksRemaining":  oa.get("weeksRemaining", 1),
        "monthName":       oa.get("monthName", ""),
        "comboCount":      oa.get("comboCount"),
        "powerDealCount":  oa.get("powerDealCount"),
        "totalKenyaStock": oa.get("totalKenyaStock"),
        # Sinza & Uganda combos (from the COMBOS sheet) + their regional stock,
        # for the region-selector guidance cards on this page.
        "sinzaCombos":        oa.get("sinzaCombos", []),
        "sinzaComboHeaders":  oa.get("sinzaComboHeaders", []),
        "sinzaSingles":       oa.get("sinzaSingles", []),
        "sinzaSinglesHeaders":oa.get("sinzaSinglesHeaders", []),
        "sinzaSpecials":      oa.get("sinzaSpecials", []),
        "sinzaSpecialHeaders":oa.get("sinzaSpecialHeaders", []),
        "ugCombos":           oa.get("ugCombos", []),
        "ugComboHeaders":     oa.get("ugComboHeaders", []),
        "ugSingles":          oa.get("ugSingles", []),
        "ugSinglesHeaders":   oa.get("ugSinglesHeaders", []),
        "sinzaStock":         _region_stock(oa.get("sinzaStockData"), "sinzaStock"),
        "ugStock":            _region_stock(oa.get("ugStockData"), "ugandaStock"),
        "totalSinzaStock":    oa.get("totalSinzaStock"),
        "totalUgandaStock":   oa.get("totalUgandaStock"),
        "ugComboTitle":       oa.get("ugComboTitle", ""),
        "sinzaComboTitle":    oa.get("sinzaComboTitle", ""),
    }


DEALS_SHEET_ID = "1TAGv9bGnE88nEjn2d0QvBkRhKiK3E42VI2GfU-MmJEY"

# All Kenya bag sales this month by product template — to attach real sold/revenue
# to each deal product (matched by name prefix, like the new-products page).
DEAL_SALES_SQL = """
SELECT UPPER(pt."name") AS name, SUM(pl.qty)::int AS units,
       ROUND(SUM(pl.price_subtotal_incl))::int AS val
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
  AND p.state IN ('done', 'paid') AND pl.qty <> 0
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
  AND pt."name" NOT LIKE '%+%'   -- combo products belong to the combos view, not deals
GROUP BY UPPER(pt."name")
"""

# Same, split by Sun-Sat week — for the per-deal weekly line (like the combo cards).
DEAL_WEEKLY_SQL = f"""
SELECT UPPER(pt."name") AS name, {_WK_EXPR} AS wk, SUM(pl.qty)::int AS units
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
  AND p.state IN ('done', 'paid') AND pl.qty <> 0
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
  AND pt."name" NOT LIKE '%+%'   -- combo products belong to the combos view, not deals
GROUP BY UPPER(pt."name"), wk
"""

# Same deal sales, but broken down by the POS till (shop) — so each Deal of the Week
# can carry its per-shop sold figure, not just the Kenya-wide total.
DEAL_SALES_BY_SHOP_SQL = """
SELECT UPPER(pc."name") AS shop, UPPER(pt."name") AS name, SUM(pl.qty)::int AS units
FROM pos_order p JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE p.date_order::date BETWEEN :start_date AND :end_date
  AND p.state IN ('done', 'paid') AND pl.qty <> 0
  AND lower(COALESCE(pc."name", '')) NOT IN ('sinza', 'dar-es-alam', 'uganda')
  AND pt."name" NOT LIKE '%+%'   -- combo products belong to the combos view, not deals
GROUP BY UPPER(pc."name"), UPPER(pt."name")
"""


def _enrich_deals(deals, m_start, m_end, stock_map, combo_bags=None):
    """Attach real Odoo sales (units + revenue), per-week sales, and Kenya stock to
    each deal product, matched by product-name prefix."""
    sales = []
    df = db.run_query(DEAL_SALES_SQL, {"start_date": m_start.isoformat(),
                                       "end_date": m_end.isoformat()})
    if df is not None and not df.empty:
        sales = [(str(r["name"]), int(r["units"] or 0), int(r["val"] or 0)) for _, r in df.iterrows()]

    # weekly: name -> {wk: units}
    name_wk, max_wk = {}, 1
    _anchor = m_start - datetime.timedelta(days=(m_start.weekday() + 1) % 7)   # Sunday on/before month start
    wf = db.run_query(DEAL_WEEKLY_SQL, {"start_date": m_start.isoformat(),
                                        "end_date": m_end.isoformat(), "anchor": _anchor})
    if wf is not None and not wf.empty:
        for _, r in wf.iterrows():
            nm, w, u = str(r["name"]), int(r["wk"]), int(r["units"] or 0)
            name_wk.setdefault(nm, {})[w] = u
            max_wk = max(max_wk, w)
    deals["curWeek"] = max_wk
    stock_items = list(stock_map.items())

    # Per-shop sold (this month) and per-shop live stock, so a Deal of the Week card
    # shows the SELLING shop's own numbers rather than the bag's Kenya-wide total.
    sales_by_loc = {}   # sheet-loc label -> {UPPER(name): units}
    sf = db.run_query(DEAL_SALES_BY_SHOP_SQL, {"start_date": m_start.isoformat(),
                                               "end_date": m_end.isoformat()})
    if sf is not None and not sf.empty:
        for _, r in sf.iterrows():
            loc = _SHOP_TO_LOC.get(str(r["shop"]).strip().upper())
            if loc:
                sales_by_loc.setdefault(loc, {})[str(r["name"]).upper()] = int(r["units"] or 0)
    stock_by_loc = _odoo_stock_by_shop(_STOCK_CODE_TO_LOC)   # sheet-loc label -> {UPPER(name): qty}

    # Deal label → bag-type key, where the promo wording differs from the catalogue
    # (e.g. "Standard Travel" is the TRAVEL bag, "Cairo Backpack" is CAIRO BP).
    DEAL_ALIASES = {
        "STANDARD TRAVEL": "TRAVEL", "STANDARD": "TRAVEL",
        "CAIRO BACKPACK": "CAIRO BP", "LAPTOP BACKPACK": "CODE 3",
        "NEO MAN BAG": "NEO MAN",
        "BRIEFCASE": "BRIEF CASE",   # sheet writes it one word; Odoo stores "BRIEF CASE …"
    }

    # Odoo product names are colour-only for many bags ("JAMELA BLACK", "KAI BLACK",
    # "LIAM BLACK") while the deal label carries a category word ("Jamela handbag",
    # "Kai backpack", "Liam travel"). So if the full label matches nothing, retry on
    # the label with its trailing category word stripped ("JAMELA", "KAI", "LIAM").
    _CATEGORY_WORDS = {"HANDBAG", "BACKPACK", "TRAVEL", "SLING", "SLINGBAG",
                       "MESSENGER", "BAG", "LUNCHBAG", "LUNCHSET", "HB", "BP"}

    def _match(prod):
        p = str(prod).strip().upper()
        pa = DEAL_ALIASES.get(p, p)          # aliased bag-type key
        _parts = p.split(" ")
        root = " ".join(_parts[:-1]) if (len(_parts) >= 2 and _parts[-1] in _CATEGORY_WORDS) else None
        # Full-label match against the sheet label AND its alias, so a spelling
        # variant is caught too (sheet "Briefcase" vs Odoo "BRIEF CASE …",
        # "Laptop Backpack" vs "CODE 3 …").
        def _full_of(key, nm): return nm == key or nm.startswith(key + " ") or key.startswith(nm + " ")
        def _full(nm):   return _full_of(p, nm) or (pa != p and _full_of(pa, nm))
        def _rooted(nm): return root is not None and (nm == root or nm.startswith(root + " "))
        def _stock_match(bt):
            return (bt == p or bt == pa or bt.startswith(p + " ") or bt.startswith(pa + " ")
                    or p.startswith(bt + " ") or bt == p.split(" ")[0])
        # Choose ONE selector for this deal — full label (incl. alias) if anything
        # matches, else the category-stripped root — and use it for the total,
        # the weekly series and the per-shop split so they always agree.
        _has_full = (any(_full(nm) for nm, _u, _v in sales)
                     or any(_full(nm) for nm in name_wk))
        _sel = _full if (_has_full or root is None) else _rooted

        u = v = st = 0
        wk = {}
        for nm, un, val in sales:
            if _sel(nm):
                u += un
                v += val
        for nm, wm in name_wk.items():
            if _sel(nm):
                for w, un in wm.items():
                    wk[w] = wk.get(w, 0) + un
        for bt, s in stock_items:
            if _sel(bt) or _stock_match(bt):
                st += s
        weeks = [{"label": "Wk %d" % i, "sold": wk.get(i, 0)} for i in range(1, max_wk + 1)]

        # Per-shop sold — same selector, so a shop's figure is a true subset of the total.
        sold_by_loc = {}
        for loc, names in sales_by_loc.items():
            tot = sum(un for nm, un in names.items() if _sel(nm))
            if tot:
                sold_by_loc[loc] = tot
        # Per-shop live stock. The per-shop map holds colour-level Odoo names
        # ("KAI BLACK", "BRIEF CASE GREY"), so match them the same way plus the
        # bag-type/alias stock rule.
        stock_by_loc_out = {}
        for loc, smap in stock_by_loc.items():
            tot = sum(s for nm, s in smap.items() if _sel(nm) or _stock_match(nm))
            if tot:
                stock_by_loc_out[loc] = tot
        return u, v, st, weeks, sold_by_loc, stock_by_loc_out

    for grp in ("powerDeals", "dealOfWeek"):
        for it in deals.get(grp, []):
            (it["sold"], it["revenue"], it["stock"], it["weeks"],
             it["soldByLoc"], it["stockByLoc"]) = _match(it["product"])
    deals["powerSold"] = sum(x["sold"] for x in deals.get("powerDeals", []))
    deals["powerRevenue"] = sum(x["revenue"] for x in deals.get("powerDeals", []))
    deals["dowSold"] = sum(x["sold"] for x in deals.get("dealOfWeek", []))
    deals["dowRevenue"] = sum(x["revenue"] for x in deals.get("dealOfWeek", []))

    # Deduped totals — a bag that runs as BOTH a Power Deal and a Deal of the Week
    # (same Odoo product) is one bag's sales, so count it once for the combined
    # "Deal units sold" / revenue headline instead of on both sides.
    def _dn(s):
        return re.sub(r"\s+", " ", str(s).strip().upper())
    _seen = {}
    for _x in deals.get("powerDeals", []) + deals.get("dealOfWeek", []):
        _seen.setdefault(_dn(_x["product"]), _x)   # first wins; sold/revenue identical per product
    deals["dedupSold"] = sum(v.get("sold", 0) for v in _seen.values())
    deals["dedupRevenue"] = sum(v.get("revenue", 0) for v in _seen.values())
    deals["dedupProducts"] = len(_seen)
    deals["overlapProducts"] = (len(deals.get("powerDeals", [])) + len(deals.get("dealOfWeek", []))) - len(_seen)

    # "Deal units sold" headline excluding deal bags that are ALSO running-combo
    # components (they're already represented under the combos), so the cumulative
    # total doesn't mix deal bags with combo bags. Standalone deal cards still render.
    _cbags = {re.sub(r"\s+", " ", str(b).strip().upper()) for b in (combo_bags or set())}

    def _is_combo_bag(prod):
        p = re.sub(r"\s+", " ", str(prod).strip().upper())
        return any(b == p or b.startswith(p + " ") or p.startswith(b) for b in _cbags)

    _ex = [v for v in _seen.values() if not _is_combo_bag(v["product"])]
    deals["dedupSoldExCombo"] = sum(v.get("sold", 0) for v in _ex)
    deals["dedupRevenueExCombo"] = sum(v.get("revenue", 0) for v in _ex)
    deals["dedupProductsExCombo"] = len(_ex)
    deals["comboBagDeals"] = len(_seen) - len(_ex)   # deal bags excluded (in the combos)
    # Same combo-bag exclusion applied to each side's own "· N sold" sub-total.
    deals["powerSoldExCombo"] = sum(x.get("sold", 0) for x in deals.get("powerDeals", []) if not _is_combo_bag(x["product"]))
    deals["dowSoldExCombo"] = sum(x.get("sold", 0) for x in deals.get("dealOfWeek", []) if not _is_combo_bag(x["product"]))

    # Cross-sell: which Power Deals are ALSO run as a Deal of the Week (same bag).
    # Matched by product name, so each card can show the same bag's rival pricing —
    # all-month Power price vs the Tier-1 weekly deal — like the running↔self-made hover.
    def _norm(s):
        return re.sub(r"\s+", " ", str(s).strip().upper())
    dow_by_name = {}
    for d in deals.get("dealOfWeek", []):
        dow_by_name.setdefault(_norm(d["product"]), []).append(d)
    for p in deals.get("powerDeals", []):
        conns = dow_by_name.get(_norm(p["product"]), [])
        p["dowConns"] = [{"product": m["product"], "tier": m["tier"],
                          "orig": m["orig"], "now": m["now"], "disc": m["disc"],
                          "sold": m["sold"], "revenue": m["revenue"], "stock": m["stock"],
                          "locations": m.get("locations", [])}
                         for m in conns]
        p["dowConnCount"] = len(conns)


def _read_deals(month_name):
    """Power Deals & Deal of the Week for the given month (Kenya sheet). Columns:
    A Tier · B Month · C Product · D Location · E Type · F Original · G Current · H Discount.
    Type = 'Power Deals' (Tier 'All', run all month) or 'Deal of the Week' (Tier 1/2, per
    location, phased). Deal-of-week rows are deduped by product across locations."""
    try:
        from google_auth import get_gspread_client
        gc = get_gspread_client()
        rows = gc.open_by_key(DEALS_SHEET_ID).worksheet("Kenya").get_all_values()
    except Exception:                                            # noqa: BLE001
        return None

    def _pn(v):
        try:
            return int(round(float(str(v).replace(",", "").strip() or 0)))
        except (ValueError, TypeError):
            return 0

    # Sheet location labels → the shop name we use elsewhere.
    LOC_ALIASES = {"nairobi town": "Starmall"}

    # Shops that run the SAME Deal of the Week as another shop but aren't listed
    # separately in the sheet. Each mirror shop inherits every DoW product its
    # parent runs, and still gets its own per-shop card (its own sold + stock).
    DOW_MIRROR = {"Starmall": ["Hazina", "Hilton", "KTDA"]}

    power, dow = [], {}
    dow_rows = 0
    for r in rows[1:]:
        if len(r) < 8:
            continue
        tier, mon, prod, loc, typ = (str(r[0]).strip(), str(r[1]).strip(), str(r[2]).strip(),
                                     str(r[3]).strip(), str(r[4]).strip())
        loc = LOC_ALIASES.get(loc.lower(), loc)
        if not prod or mon.lower() != month_name.lower():
            continue
        item = {"tier": tier, "product": prod, "location": loc,
                "orig": _pn(r[5]), "now": _pn(r[6]), "disc": _pn(r[7])}
        if typ.lower().startswith("power"):
            power.append(item)
        elif typ.lower().startswith("deal"):
            dow_rows += 1
            k = (prod.upper(), tier.upper())
            e = dow.setdefault(k, {"product": prod, "tier": tier, "orig": item["orig"],
                                   "now": item["now"], "disc": item["disc"], "locations": []})
            if loc and loc not in e["locations"]:
                e["locations"].append(loc)

    # A mirror shop inherits every DoW product its parent runs.
    for parent, shops in DOW_MIRROR.items():
        for e in dow.values():
            if parent in e["locations"]:
                for s in shops:
                    if s not in e["locations"]:
                        e["locations"].append(s)

    dow_list = sorted(dow.values(), key=lambda x: (-x["disc"], x["product"]))
    locs = sorted({l for d in dow_list for l in d["locations"]})
    return {
        "month": month_name,
        "powerDeals": sorted(power, key=lambda x: (-x["disc"], x["product"])),
        "dealOfWeek": dow_list,
        "powerCount": len(power),
        "dowProducts": len(dow_list),
        "dowRows": dow_rows,
        "dowLocations": len(locs),
        "locations": locs,
        "powerDisc": sum(p["disc"] for p in power),
        "dowDisc": sum(d["disc"] for d in dow_list),
    }


# ── Running-combo classification against the authoritative monthly sheet ──
# The offer sheet's SEPT COMBOS list (oa["combos"]) is the source of truth for which
# combos are "running" this month. We match each Odoo combo product to that list
# slot-by-slot; a combo that matches AND is not a CBR is a running combo, everything
# else (a CBR, or an Odoo combo not on the sheet) is self-made. This replaces the old
# include_all flag heuristic, which wrongly promoted stray include_all combos (e.g.
# "Amaya + Avana", not on the sheet) into the running set.
_COMBO_CATEGORY = {"HANDBAG", "TRAVEL", "BACKPACK", "BAG", "SLING", "SLINGBAG",
                   "MESSENGER", "LUNCH", "LUNCHSET", "LUNCHBAG", "CHEST", "BP", "HB", "COMBO"}
_COMBO_COLOURS = {"BLACK", "GREY", "GREEN", "BROWN", "NUDE", "RED", "BLUE", "MAROON",
                  "SPICE", "BEIGE", "CHOCOLATE", "YELLOW", "DOTTED", "CRACKED", "DARK",
                  "TT", "PURPLE", "PINK", "ORANGE", "WHITE", "GOLD", "SILVER", "NAVY"}
# Promo wording on the sheet ↔ catalogue wording in Odoo.
_COMBO_PHRASE_ALIAS = {"LAPTOP BACKPACK": "CODE 3", "STANDARD TRAVEL": "STANDARD",
                       "NEO MAN BAG": "NEO MAN", "CAIRO BACKPACK": "CAIRO BP"}


def _combo_norm_option(opt):
    """One combo slot-option → its distinctive bag token(s), colours/category words
    and promo aliases stripped so the sheet and Odoo names line up."""
    s = " " + str(opt).upper().strip() + " "
    for a, b in _COMBO_PHRASE_ALIAS.items():
        s = s.replace(" " + a + " ", " " + b + " ")
    words = [w for w in re.split(r"[^A-Z0-9]+", s) if w]
    words = [w for w in words if w not in _COMBO_CATEGORY and w not in _COMBO_COLOURS]
    return " ".join(words).strip()


def _combo_sheet_slots(label):
    """Sheet label "AMAYA/ELYSE+MOON/NIZANA" → [ {AMAYA,ELYSE}, {MOON,NIZANA} ]."""
    return [set(filter(None, (_combo_norm_option(o) for o in slot.split("/"))))
            for slot in str(label).split("+")]


def _combo_odoo_slots(name):
    """Odoo name "Amaya Handbag or Elyse Handbag + Moon Bag or Nizana" → the same shape."""
    return [set(filter(None, (_combo_norm_option(o) for o in re.split(r"\bor\b", slot, flags=re.I))))
            for slot in str(name).split("+")]


def _build_sheet_slots(offer):
    """[(label, slots)] for each running combo on the offer sheet (skips the TOTAL row)."""
    out = []
    for row in (offer or {}).get("combos", []):
        label = str(row[0]).strip() if isinstance(row, (list, tuple)) else str(row).strip()
        if not label or label.upper() in ("TOTAL", "SEPT COMBOS"):
            continue
        out.append((label, _combo_sheet_slots(label)))
    return out


def _matches_sheet(name, sheet_slots):
    """The sheet label this Odoo combo maps to (same slot count, every slot overlaps),
    or None if it isn't on the sheet."""
    o = _combo_odoo_slots(name)
    for label, s in sheet_slots:
        if len(s) == len(o) and all((o[i] & s[i]) for i in range(len(s))):
            return label
    return None


_BAG_PRICES = None


def _load_bag_prices():
    """{BAG_UPPER: original full price} from bag_original_prices.json — the baseline the
    combo monetary-implication measures the bundling discount against. Editable there."""
    global _BAG_PRICES
    if _BAG_PRICES is not None:
        return _BAG_PRICES
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bag_original_prices.json")
    out = {}
    try:
        for k, v in json.load(open(path, encoding="utf-8")).items():
            if str(k).startswith("_"):
                continue
            try:
                out[str(k).strip().upper()] = int(v)
            except (ValueError, TypeError):
                pass
    except Exception:                                        # noqa: BLE001
        out = {}
    _BAG_PRICES = out
    return out


# Standalone bag sales this month (any single bag, not a combo) — to find which bags
# are NOT on any offer (running combo, Deal of the Week, or Power Deal).
BAG_SALES_SQL = """
SELECT UPPER(pt."name") AS name, SUM(pl.qty)::int AS units,
       ROUND(SUM(pl.price_subtotal_incl))::int AS revenue
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
LEFT JOIN product_product pp ON pl.product_id=pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done','paid') AND pl.qty <> 0
  AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
  AND pt."name" NOT LIKE '%+%'
  AND pt."name" NOT ILIKE '%delivery%' AND pt."name" NOT ILIKE '%customi%'
  AND pt."name" NOT ILIKE '%strap%' AND pt."name" NOT ILIKE 'gift bag%'
GROUP BY UPPER(pt."name")
"""


def _bags_not_on_offer(m_start, m_end, combo_bags, deals):
    """Bags with sales this month that are on NO offer — i.e. not a running-combo
    component, a Deal of the Week, or a Power Deal. Each Odoo product is resolved to
    its bag type via the price-list catalogue (longest-prefix match)."""
    keys = sorted(_load_bag_prices().keys(), key=len, reverse=True)
    # Promo wording ↔ catalogue bag (e.g. a "Cairo backpack" deal is the CAIRO BP bag).
    _ALIAS = {"CAIRO BACKPACK": "CAIRO BP", "LAPTOP BACKPACK": "CODE 3",
              "STANDARD TRAVEL": "TRAVEL", "STANDARD": "TRAVEL", "NEO MAN BAG": "NEO MAN",
              "BRIEFCASE": "BRIEF CASE"}

    def _norm(name):
        p = re.sub(r"\s+", " ", str(name).strip().upper())
        for a, b in _ALIAS.items():
            if p == a or p.startswith(a + " "):
                return (b + p[len(a):]).strip()
        return p

    def _infer(name):
        p = _norm(name)
        for k in keys:
            if p == k or p.startswith(k + " "):
                return k
        return None

    # On-offer names: running-combo components + Deal-of-Week + Power-Deal products,
    # normalised (aliases applied). Matched to a sold bag by either being equal or one
    # being a word-prefix of the other (so a "AVANA" deal covers the "AVANA HB" bag).
    on_offer_names = {_norm(b) for b in (combo_bags or set())}
    for grp in ("dealOfWeek", "powerDeals"):
        for x in (deals or {}).get(grp, []):
            on_offer_names.add(_norm(x.get("product", "")))

    def _is_on_offer(bt):
        return any(d == bt or bt.startswith(d + " ") or d.startswith(bt + " ")
                   for d in on_offer_names)

    sold = {}
    df = db.run_query(BAG_SALES_SQL, {"s": m_start.isoformat(), "e": m_end.isoformat()})
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            bt = _infer(r["name"])
            if not bt:
                continue                                      # not in the catalogue — skip
            e = sold.setdefault(bt, {"units": 0, "revenue": 0})
            e["units"] += int(r["units"] or 0)
            e["revenue"] += int(r["revenue"] or 0)

    not_on = [{"bag": bt, "units": v["units"], "revenue": v["revenue"]}
              for bt, v in sold.items() if not _is_on_offer(bt) and v["units"] > 0]
    not_on.sort(key=lambda x: -x["units"])
    on_sold = [bt for bt in sold if _is_on_offer(bt) and sold[bt]["units"] > 0]
    return {
        "notOnOffer": not_on,
        "notOnOfferCount": len(not_on),
        "notOnOfferUnits": sum(x["units"] for x in not_on),
        "notOnOfferRevenue": sum(x["revenue"] for x in not_on),
        "onOfferCount": len(on_sold),
        "onOfferUnits": sum(sold[bt]["units"] for bt in on_sold),
    }


# Per-shop combo-button usage: how many of each running combo were actually rung
# THROUGH the combo button (Odoo combo product), vs the component bags sold as
# singles at that shop — surfaces tills that sell a combo as separate bags (the
# Jumbo+Jumbo problem) instead of using the combo button.
COMBO_BY_SHOP_SQL = """
SELECT UPPER(COALESCE(pc."name",'?')) AS shop, pt."name" AS combo, SUM(pl.qty)::int AS qty
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
LEFT JOIN product_product pp ON pl.product_id=pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done','paid') AND pl.qty <> 0
  AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
  AND pt."name" LIKE '%+%' AND pt."name" NOT ILIKE '%delivery%' AND pt."name" NOT ILIKE '%customi%'
GROUP BY shop, pt."name"
"""
SINGLES_BY_SHOP_SQL = """
SELECT UPPER(COALESCE(pc."name",'?')) AS shop, UPPER(pt."name") AS name, SUM(pl.qty)::int AS qty
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
LEFT JOIN product_product pp ON pl.product_id=pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done','paid') AND pl.qty <> 0
  AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
  AND pt."name" NOT LIKE '%+%'
GROUP BY shop, UPPER(pt."name")
"""


def _combo_button_usage(m_start, m_end, offer, sheet_slots, running):
    """Per running combo: units rung through the combo button (Odoo) vs the sheet's
    expected figure, with a per-shop breakdown of combos rung and the combo's
    component bags sold as singles at that shop."""
    if not sheet_slots:
        return []
    # sheet's expected COMBO figure per label (col C of the SEPT COMBOS list)
    expected = {}
    for row in (offer or {}).get("combos", []):
        if isinstance(row, (list, tuple)) and len(row) >= 3:
            lbl = str(row[0]).strip()
            try:
                expected[lbl] = int(str(row[2]).replace(",", "").strip() or 0)
            except ValueError:
                expected[lbl] = 0
    # Each combo's slots as token-sets, with how many times an identical slot repeats
    # (Jumbo+Jumbo = the {JUMBO} slot twice → a pair needs 2 Jumbos).
    slot_sets = {}   # lbl -> list of (frozenset(tokens), multiplicity)
    for lbl, slots in sheet_slots:
        counts = {}
        for s in slots:
            fs = frozenset(s)
            counts[fs] = counts.get(fs, 0) + 1
        slot_sets[lbl] = list(counts.items())
    name_to_label = {r["name"]: _matches_sheet(r["name"], sheet_slots) for r in running}
    name_to_label = {n: l for n, l in name_to_label.items() if l}

    def _shop(s):
        s = str(s).strip().upper()
        return _SHOP_TO_LOC.get(s, s.title())

    rung = {lbl: {} for lbl, _ in sheet_slots}
    cf = db.run_query(COMBO_BY_SHOP_SQL, {"s": m_start.isoformat(), "e": m_end.isoformat()})
    if cf is not None and not cf.empty:
        for _, r in cf.iterrows():
            lbl = name_to_label.get(str(r["combo"]).strip())
            if lbl:
                sh = _shop(r["shop"])
                rung[lbl][sh] = rung[lbl].get(sh, 0) + int(r["qty"] or 0)

    # Single-bag sales by shop & token, to estimate combos the singles could have formed.
    shop_tok = {}    # shop -> {token: units}
    sf = db.run_query(SINGLES_BY_SHOP_SQL, {"s": m_start.isoformat(), "e": m_end.isoformat()})
    if sf is not None and not sf.empty:
        for _, r in sf.iterrows():
            tok = _combo_norm_option(r["name"])
            if not tok:
                continue
            sh = _shop(r["shop"])
            shop_tok.setdefault(sh, {})[tok] = shop_tok.setdefault(sh, {}).get(tok, 0) + int(r["qty"] or 0)

    def _implied(lbl, sh):
        # Combos the shop's single-bag sales could have made = the tightest slot:
        # min over distinct slots of (component singles in that slot ÷ how many that
        # slot needs). This is the honest "could-have-been-combos" figure — it does
        # NOT over-count popular bags the way a raw component-singles sum does.
        toks = shop_tok.get(sh, {})
        best = None
        for fs, k in slot_sets[lbl]:
            pool = sum(toks.get(t, 0) for t in fs)
            limited = pool // k
            best = limited if best is None else min(best, limited)
        return best or 0

    out = []
    for lbl, _ in sheet_slots:
        shops = sorted(set(list(rung[lbl]) + list(shop_tok)))
        shoprows = []
        for s in shops:
            rn = rung[lbl].get(s, 0)
            im = _implied(lbl, s)
            if rn or im:
                shoprows.append({"shop": s, "rung": rn, "implied": im})
        # Red flag: a shop ringing less than half the best-performing shop in its region.
        region_best = {}
        for x in shoprows:
            reg = _SHOP_REGION.get(x["shop"].upper(), x["shop"])
            region_best[reg] = max(region_best.get(reg, 0), x["rung"])
        for x in shoprows:
            reg = _SHOP_REGION.get(x["shop"].upper(), x["shop"])
            best = region_best.get(reg, 0)
            x["region"] = reg
            x["red"] = best > 0 and x["rung"] < 0.5 * best
        # Arrange from the highest green (rung) number down.
        shoprows.sort(key=lambda x: (-x["rung"], -x["implied"], x["shop"]))
        out.append({"combo": lbl, "expected": expected.get(lbl, 0),
                    "rung": sum(rung[lbl].values()),
                    "implied": sum(r["implied"] for r in shoprows), "shops": shoprows})
    # Worst combo-button adherence first (rung ÷ sheet-expected); combos with no
    # sheet target fall to the end.
    out.sort(key=lambda x: (x["rung"] / x["expected"]) if x["expected"] else 9e9)
    return out


def build_payload(m_start, m_end):
    """Query + shape the self-made/running split and the combo-request log for the
    given month window (Kenya tills). Assumes the DB connection is already up — the
    caller checks. Shared by fetch() (live month) and monthly_report.py (report
    month, possibly pinned to a past month), so both stay in sync."""
    month = m_start.strftime("%B %Y")
    # The authoritative running-combo list for the month comes from the offer sheet.
    offer = _read_offer_analysis() or {}
    sheet_slots = _build_sheet_slots(offer)
    df = db.run_query(COMBO_SQL, {"start_date": m_start.isoformat(),
                                  "end_date": m_end.isoformat()})
    self_made, running = [], []
    sold_units = {}          # tmpl_id -> units sold this month (self-made only)
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            row = {"name": str(r["product"]).strip(),
                   "qty": int(r["qty"] or 0),
                   "value": int(r["value"] or 0),
                   "colourOptions": int(r["colour_options"] or 0)}
            is_cbr = bool(r["is_cbr"])
            # Running = the combo's BAG COMPOSITION matches an offer-sheet combo,
            # however it was rung. A combo is JUMBO+JUMBO if both bags are Jumbo (any
            # colours) — the official "Jumbo + Jumbo" AND the CBR pairings like "Jumbo
            # Grey + Jumbo Black Combo" all count. A Jumbo + a *different* bag matches no
            # sheet combo, so it stays self-made. Fall back to the old heuristic only if
            # the sheet is missing.
            if sheet_slots:
                is_running = _matches_sheet(row["name"], sheet_slots) is not None
            else:
                is_running = bool(r["include_all"]) and not is_cbr
            if is_running:
                row["tmpl"] = int(r["tmpl_id"]) if pd.notna(r["tmpl_id"]) else None
                running.append(row)
            else:
                self_made.append(row)
                if pd.notna(r["tmpl_id"]):
                    tid = int(r["tmpl_id"])
                    sold_units[tid] = sold_units.get(tid, 0) + row["qty"]

    # Keep the per-product running list (for the combo-button usage, which needs every
    # Odoo product name), then collapse products that map to the same sheet combo into
    # one card — so JUMBO+JUMBO (the official "Jumbo + Jumbo" plus the older "Jumbo green
    # + Jumbo black") shows as a single running combo, not two.
    running_products = list(running)
    if sheet_slots and running:
        _merged = {}
        for _row in running:
            _lbl = _matches_sheet(_row["name"], sheet_slots) or _row["name"]
            _g = _merged.get(_lbl)
            if _g is None:
                _g = {"name": _row["name"], "qty": 0, "value": 0, "colourOptions": 0,
                      "tmpls": [], "_topqty": -1}
                _merged[_lbl] = _g
            if _row["qty"] > _g["_topqty"]:            # representative name = top seller
                _g["name"], _g["_topqty"] = _row["name"], _row["qty"]
            _g["qty"] += _row["qty"]
            _g["value"] += _row["value"]
            _g["colourOptions"] = max(_g["colourOptions"], _row.get("colourOptions", 0))
            if _row.get("tmpl") is not None:
                _g["tmpls"].append(_row["tmpl"])
        for _g in _merged.values():
            _g.pop("_topqty", None)
            _g["tmpl"] = _g["tmpls"][0] if _g["tmpls"] else None
        running = list(_merged.values())

    # Combo-request log
    rq = db.run_query(REQUEST_SQL, {"start_date": m_start.isoformat(),
                                    "end_date": m_end.isoformat()})
    requests = []
    st_counts = {"approved": 0, "rejected": 0, "pending": 0, "other": 0}
    if rq is not None and not rq.empty:
        for _, r in rq.iterrows():
            state = str(r["state"] or "").strip().lower()
            tid = int(r["tmpl_id"]) if pd.notna(r["tmpl_id"]) else None
            requests.append({
                "cbr": str(r["cbr"] or "").strip(),
                "combo": str(r["combo"] or "").strip(),
                "shop": str(r["shop"] or "—").strip(),
                "by": str(r["requested_by"] or "—").strip(),
                "state": state,
                "lloyd": bool(r["lloyd"]),
                "price": int(round(float(r["price"] or 0))),
                "on": _dstr(r["requested_on"]),
                "decided": _dstr(r["decided_on"]),
                "reject": str(r["reject_reason"] or "").strip(),
                "soldUnits": sold_units.get(tid, 0) if tid is not None else 0,
            })
            if state in ("approved",):
                st_counts["approved"] += 1
            elif state in ("rejected", "reject"):
                st_counts["rejected"] += 1
            elif state in ("draft", "pending", "requested", "to approve", "submitted"):
                st_counts["pending"] += 1
            else:
                st_counts["other"] += 1

    def agg(rows):
        _co = [x["colourOptions"] for x in rows]
        return {"count": len(rows),
                "units": sum(x["qty"] for x in rows),
                "value": sum(x["value"] for x in rows),
                "avgColours": round(sum(_co) / len(_co), 1) if _co else 0}

    # ── Weekly sales (Sun-Sat) + beat-August goal + running-combo cards ──
    offer = _read_offer_analysis() or {}
    stock_map = offer.get("stockMap", {})
    bag_targets = offer.get("bagTargets", {})
    # Recognise any bag that has stock OR a target, so 0-stock bags (e.g. NEO MAN,
    # GYM BAG — which live in targets, not the stock sheet) still resolve.
    known = set(stock_map.keys()) | set(bag_targets.keys())
    # Stocked bags first, then target-only bags (NEO MAN, GYM BAG, SAFIRI BP…), so a
    # fuzzy prefix like "SAFIRI" resolves to the stocked SAFIRI TRAVEL, not SAFIRI BP.
    bag_types = list(stock_map.keys()) + [k for k in bag_targets if k not in stock_map]
    # Combo-sheet wording → actual bag type (the attendant's names differ from the
    # catalogue): Laptop Backpack = CODE 3, Neo Man Bag = NEO MAN, Standard Travel
    # = TRAVEL (also bare "Standard"), Gym Bag = GYM BAG.
    BAG_ALIASES = {
        "STANDARD": "TRAVEL", "STANDARD TRAVEL": "TRAVEL",
        "LAPTOP BACKPACK": "CODE 3", "NEO MAN BAG": "NEO MAN", "NEO MAN": "NEO MAN",
        "GYM BAG": "GYM BAG",
    }

    def _match_bag(tok):
        tok = tok.strip().upper()
        if len(tok) < 2:
            return None
        if tok in BAG_ALIASES:
            tok = BAG_ALIASES[tok]
        else:
            # An alias may be keyed on the leading word(s) with a colour/suffix
            # after it — e.g. "STANDARD TRAVEL BLACK" → "STANDARD"/"STANDARD TRAVEL"
            # → TRAVEL. Without this the printed component (with colour) is orphaned
            # under "STANDARD" while the card shows the bag as TRAVEL, so the per-bag
            # "sold" chips don't sum to the combo total.
            _p = tok.split(" ")
            for _n in (min(3, len(_p)), 2, 1):
                _k = " ".join(_p[:_n])
                if _k in BAG_ALIASES:
                    tok = BAG_ALIASES[_k]
                    break
        if tok in known:
            return tok
        ns = tok.replace(" ", "")
        for bt in bag_types:
            if (bt == tok or bt.replace(" ", "") == ns or tok in bt.split(" ")
                    or bt.startswith(tok + " ") or tok.startswith(bt)):
                return bt
        return None

    def _combo_bags(name):
        """Component bags of a POS combo name → (all bags, picks). Groups split on
        '+' (Kenya) or ' x '/'×' (Sinza & Uganda write combos as 'A x B'),
        alternatives on '/' or ' or '; the pick is the highest-Kenya-stock
        alternative in each group (the ★)."""
        all_b, picks = [], []
        for g in re.split(r"\s*\+\s*|\s+[x×]\s+", str(name), flags=re.I):
            best, best_s = None, -1
            for a in re.split(r"\s+or\s+|/", g, flags=re.I):
                b = _match_bag(a)
                if b:
                    if b not in all_b:
                        all_b.append(b)
                    s = stock_map.get(b, 0)
                    if s > best_s:
                        best, best_s = b, s
            if best and best not in picks:
                picks.append(best)
        return all_b, picks

    # ── Odoo live-stock fallback ──────────────────────────────────
    # The offer sheet is the primary stock source; where it reports 0 (or doesn't
    # list a bag), fall back to live Odoo on-hand for that region's shops. Each
    # product variant is resolved to its bag type.
    def _fill_from_odoo(bag_stock, codes, label):
        agg = {}
        for _n, _q in _odoo_stock_for(codes).items():
            _b = _match_bag(_n)
            if _b:
                agg[_b] = agg.get(_b, 0) + _q
        _f = 0
        for _b, _q in agg.items():
            if not bag_stock.get(_b):        # sheet stock is 0 or missing → use Odoo
                bag_stock[_b] = _q
                _f += 1
        if _f:
            print(f"  Stock fallback ({label}): filled {_f} bag(s) the sheet had at 0")
        return bag_stock

    _fill_from_odoo(stock_map, _KENYA_SHOP_CODES, "Kenya shops")
    global _AUGMENTED_STOCK
    _AUGMENTED_STOCK = stock_map           # Power Deals / DoW read this (via _enrich_deals)

    def _anchor_sunday(d):
        # Sunday on/before d (Postgres DOW: Sunday=0). Python weekday(): Mon=0..Sun=6.
        return d - datetime.timedelta(days=(d.weekday() + 1) % 7)

    def _month_weekly(s, e):
        d = db.run_query(MONTH_WEEKLY_SQL, {"start_date": s.isoformat(),
                                            "end_date": e.isoformat(), "anchor": _anchor_sunday(s)})
        wk = {}
        if d is not None and not d.empty:
            for _, x in d.iterrows():
                wk[int(x["wk"])] = int(x["units"] or 0)
        return wk

    # Per-combo weekly (this month) → {tmpl: {wk: units}}
    pw = db.run_query(COMBO_WEEKLY_SQL, {"start_date": m_start.isoformat(),
                                         "end_date": m_end.isoformat(), "anchor": _anchor_sunday(m_start)})
    per_combo, max_wk = {}, 1
    week_combos = {}   # wk -> {combo name: units} (all combos, for the weekly breakdown)
    if pw is not None and not pw.empty:
        for _, x in pw.iterrows():
            t, w, u = int(x["tmpl_id"]), int(x["wk"]), int(x["units"] or 0)
            per_combo.setdefault(t, {})[w] = u
            max_wk = max(max_wk, w)
            _nm = str(x["product"]).strip()
            _wc = week_combos.setdefault(w, {})
            _wc[_nm] = _wc.get(_nm, 0) + u

    # September-so-far combos (all combos) + August baseline
    sept_wk = _month_weekly(m_start, m_end)
    max_wk = max([max_wk] + list(sept_wk.keys()))
    sept_total = sum(sept_wk.values())

    prev_end = m_start - datetime.timedelta(days=1)
    prev_start = prev_end.replace(day=1)
    aug_wk = _month_weekly(prev_start, prev_end)
    aug_span = max(list(aug_wk.keys()) + [1])
    aug_weekly = [aug_wk.get(i, 0) for i in range(1, aug_span + 1)]
    aug_total = sum(aug_weekly)
    aug_active = len([w for w in aug_weekly if w > 0]) or 1

    weeks_left = int(offer.get("weeksRemaining") or 4) or 4
    remaining = max(aug_total + 1 - sept_total, 0)
    weekly_to_beat = -(-remaining // weeks_left) if weeks_left else remaining
    # Weekly detail: this-month vs last-month per Sun-Sat week, with each week's
    # target = last month's same week, and the combos that sold that week — so a
    # week that misses its target shows which combos did (and didn't) carry it.
    _span = max(max_wk, len(aug_weekly))
    weekly_detail = []
    for _i in range(1, _span + 1):
        _cs = sorted(week_combos.get(_i, {}).items(), key=lambda kv: -kv[1])
        weekly_detail.append({
            "wk": _i,
            "cur": (sept_wk.get(_i, 0) if _i <= max_wk else None),   # None = week not reached yet
            "prev": (aug_weekly[_i - 1] if _i - 1 < len(aug_weekly) else 0),
            "combos": [{"name": _n, "units": _u} for _n, _u in _cs[:8]],
        })

    combos_goal = {
        "augLabel": prev_start.strftime("%B"), "septLabel": m_start.strftime("%B"),
        "augTotal": aug_total, "augWeekly": aug_weekly, "augAvg": round(aug_total / aug_active),
        "septSoFar": sept_total, "weeksLeft": weeks_left, "weeklyToBeat": weekly_to_beat,
        "beaten": sept_total > aug_total, "curWeek": max_wk, "weeklyDetail": weekly_detail,
    }

    # ── Offer Sales vs Stock Guidance (borrowed from Offer Type Analysis) ──
    # Per offer-sheet combo: stock, weekly gain, remaining-to-target (highest-stock
    # bag per group ★, halved) + a verdict — the data behind the guidance chart.
    def _num2(v):
        try:
            return float(str(v).replace(",", "").replace("%", "").strip() or 0)
        except (ValueError, TypeError):
            return 0.0

    def _offer_trend():
        combos = offer.get("combos", [])
        headers = offer.get("comboHeaders", [])
        norm = [str(h).upper().replace(" ", "") for h in headers]
        price_i, weeks_i = 1, []
        for i, h in enumerate(norm):
            if h == "PRICE" and price_i == 1:
                price_i = i
            mm = re.match(r"^WK(\d+)$", h)
            if mm:
                weeks_i.append(i)
        if not weeks_i:
            weeks_i = [2, 3]
        out = []
        for r in combos:
            name = str(r[0]).strip()
            if not name or "TOTAL" in name.upper():
                continue
            wk_vals = [_num2(r[i]) if i < len(r) else 0 for i in weeks_i]
            sales = int(sum(wk_vals))                       # total sales across the weekly columns
            gain = int(wk_vals[-1] - wk_vals[-2]) if len(wk_vals) > 1 else 0
            all_b, picks = _combo_bags(name)
            stock = int(sum(stock_map.get(b, 0) for b in all_b))
            is_single = len(all_b) == 1 and all_b[0] == name.upper()
            raw_t = sum(bag_targets.get(b, {}).get("target", 0) for b in picks)
            raw_r = sum(bag_targets.get(b, {}).get("remaining", 0) for b in picks)
            tgt = int(raw_t if is_single else round(raw_t / 2))
            rem = int(raw_r if is_single else round(raw_r / 2))
            wk_tgt = int(-(-rem // weeks_left)) if weeks_left else rem
            price = int(_num2(r[price_i])) if price_i < len(r) else 0
            _lead = "%d sold so far. " % sales
            if stock == 0:
                advice = _lead + "Out of stock — pause the push until restocked."
            elif gain > 0:
                advice = _lead + "Sales rising — keep the momentum, %d/wk is the goal." % wk_tgt
            elif gain < 0:
                advice = _lead + "Sales slowing — push harder to hit %d/wk with %d in stock." % (wk_tgt, stock)
            else:
                advice = _lead + "Sales steady — hold the effort to keep %d/wk." % wk_tgt
            out.append({"name": name, "stock": stock, "gain": gain, "rem": rem, "sales": sales,
                        "target": tgt, "weekTgt": wk_tgt, "price": price, "advice": advice})
        return out

    offer_trend = _offer_trend()
    offer_kpis = {
        "combos": offer.get("comboCount"), "powerDeals": offer.get("powerDealCount"),
        "kenyaStock": offer.get("totalKenyaStock"), "kenyaTotal": 10192,
    }

    # ── Top bags clients keep pairing in self-made combos ─────────
    # Which bag types recur most across the CBR combos (weighted by units sold),
    # and whether each is already offered in an official/running combo — a bag that
    # clients keep self-combining but that we never put in an official combo is a
    # gap worth closing. Stock shown so a low-stock favourite is flagged.
    sm_freq, sm_in = {}, {}
    for _r in self_made:
        _bags, _ = _combo_bags(_r["name"])
        for _b in _bags:
            sm_freq[_b] = sm_freq.get(_b, 0) + _r["qty"]
            sm_in.setdefault(_b, set()).add(_r["name"])
    official_bags = set()
    for _oc in offer.get("combos", []):
        _nm = str(_oc[0]).strip()
        if _nm and "TOTAL" not in _nm.upper():
            _ob, _ = _combo_bags(_nm)
            official_bags.update(_ob)
    running_bags = set()
    for _r in running:
        _rb, _ = _combo_bags(_r["name"])
        running_bags.update(_rb)
    top_bags = []
    for _b, _freq in sorted(sm_freq.items(), key=lambda kv: (-kv[1], kv[0]))[:6]:
        top_bags.append({
            "bag": _b, "times": _freq, "combos": len(sm_in.get(_b, [])),
            "inOfficial": _b in official_bags, "inRunning": _b in running_bags,
            "stock": int(stock_map.get(_b, 0)),
        })
    top6_set = {tb["bag"] for tb in top_bags}
    # bag → the self-made combos built on it (for the running-combo cross-sell hover)
    sm_by_bag = {}
    for _r in self_made:
        _bags, _ = _combo_bags(_r["name"])
        for _b in set(_bags):
            sm_by_bag.setdefault(_b, []).append(
                {"name": _r["name"], "qty": _r["qty"], "value": _r["value"]})

    # Actual bags PRINTED inside each combo sale (per template) — Odoo records the
    # chosen components in combo_product_attribute_values, so a bundle like
    # "Mega + Man Bag or Mini Umbra or Neo Man Bag" is attributed to the exact bag
    # the customer picked, not just the bundle.
    import ast as _ast
    comp_by_tmpl, comp_by_bag = {}, {}
    _cc = db.run_query(COMBO_COMPONENTS_SQL, {"start_date": m_start.isoformat(),
                                              "end_date": m_end.isoformat()})
    if _cc is not None and not _cc.empty:
        for _, _cr in _cc.iterrows():
            _tid = int(_cr["tmpl_id"]) if pd.notna(_cr["tmpl_id"]) else None
            _q = int(_cr["qty"] or 0)
            _raw = str(_cr["attrs"] or "").strip()
            _names = []
            if _raw:
                try:
                    _parsed = _ast.literal_eval(_raw)
                    for _d in (_parsed if isinstance(_parsed, list) else [_parsed]):
                        if isinstance(_d, dict):
                            for _v in _d.values():
                                if isinstance(_v, dict) and _v.get("full_name_product"):
                                    _names.append(str(_v["full_name_product"]))
                except (ValueError, SyntaxError):
                    _names = []
            for _nm in _names:
                _bag = _match_bag(_nm) or _nm.strip().upper().split(" ")[0]
                _d = comp_by_tmpl.setdefault(_tid, {})
                _d[_bag] = _d.get(_bag, 0) + _q
                comp_by_bag[_bag] = comp_by_bag.get(_bag, 0) + _q

    # Combo-button usage per combo (rung vs sheet-expected + per-shop split), attached
    # to each running card so it renders inside the card rather than a separate panel.
    combo_usage = _combo_button_usage(m_start, m_end, offer, sheet_slots, running_products)
    usage_by_label = {u["combo"]: u for u in combo_usage}

    running_cards = []
    for row in running:
        tmpls = row.get("tmpls") or ([row["tmpl"]] if row.get("tmpl") is not None else [])
        pcw = {}
        for _t in tmpls:
            for _w, _q in per_combo.get(_t, {}).items():
                pcw[_w] = pcw.get(_w, 0) + _q
        weeks = [{"label": "Wk %d" % i, "sold": pcw.get(i, 0)} for i in range(1, max_wk + 1)]
        total = row["qty"]
        all_b, picks = _combo_bags(row["name"])
        _comp = {}
        for _t in tmpls:
            for _b, _q in comp_by_tmpl.get(_t, {}).items():
                _comp[_b] = _comp.get(_b, 0) + _q
        bags = [{"name": b, "stock": stock_map.get(b, 0), "star": b in picks, "sold": _comp.get(b, 0)} for b in all_b]
        last = weeks[-1]["sold"] if weeks else 0
        prev = weeks[-2]["sold"] if len(weeks) > 1 else last
        # Guidance (same rule as Offer Sales vs Stock Guidance): remaining-to-target
        # from the highest-stock bag per group (★), halved, and a weekly target.
        is_single = len(all_b) == 1 and all_b[0] == row["name"].strip().upper()
        raw_t = sum(bag_targets.get(b, {}).get("target", 0) for b in picks)
        raw_r = sum(bag_targets.get(b, {}).get("remaining", 0) for b in picks)
        target = int(raw_t if is_single else round(raw_t / 2))
        remaining = int(raw_r if is_single else round(raw_r / 2))
        week_tgt = int(-(-remaining // weeks_left)) if weeks_left else remaining
        # Cross-sell: which top-6 bag(s) this running combo shares, and the self-made
        # (CBR) combos built on the same bag — so the money the official combo made
        # can be read against the money "shifted" into self-made combos.
        conns, seen_sm = [], {}
        for b in all_b:
            if b in top6_set:
                sm = sm_by_bag.get(b, [])
                conns.append({"bag": b, "selfMade": sm,
                              "smUnits": sum(x["qty"] for x in sm),
                              "smValue": sum(x["value"] for x in sm)})
                for x in sm:
                    seen_sm[x["name"]] = x          # dedup a combo shared across bags
        _sheet_lbl = _matches_sheet(row["name"], sheet_slots)   # the sheet's combo name
        running_cards.append({
            "name": row["name"], "price": round(row["value"] / row["qty"]) if row["qty"] else 0,
            "value": row["value"], "colourOptions": row.get("colourOptions", 0),
            "weeks": weeks, "total": total, "avg": round(total / max_wk) if max_wk else 0,
            "bags": bags, "totalStock": sum(b["stock"] for b in bags),
            "target": target, "remaining": remaining, "weekTgt": week_tgt,
            "diff": last - prev,
            "connections": conns,
            "connUnits": sum(x["qty"] for x in seen_sm.values()),
            "connValue": sum(x["value"] for x in seen_sm.values()),
            "connCombos": len(seen_sm),
            "lastLabel": weeks[-1]["label"] if weeks else "Wk 1",
            "prevLabel": weeks[-2]["label"] if len(weeks) > 1 else (weeks[-1]["label"] if weeks else "Wk 1"),
            "usage": usage_by_label.get(_sheet_lbl),
            "sheetLabel": _sheet_lbl,
        })

    for row in running:            # tmpl(s) were only needed to build the cards
        row.pop("tmpl", None)
        row.pop("tmpls", None)

    # ── Sinza & Uganda region guidance cards (combos from the COMBOS sheet) ──
    # Each combo → price (col B), per-week sales, total, component-bag stock in that
    # region, and a sales-vs-stock verdict — rendered like the Kenya running cards.
    def _rnum(x):
        try:
            return int(round(float(str(x).replace(",", "").strip() or 0)))
        except (ValueError, TypeError):
            return 0

    def _region_cards(combos, headers, region_stock):
        norm = [str(h).upper().replace(" ", "") for h in (headers or [])]
        price_i, wk_i, wk_l = 1, [], []
        for i, h in enumerate(norm):
            if h == "PRICE" and price_i == 1:
                price_i = i
            mo = re.match(r"^WK(\d+)$", h)
            if mo:
                wk_i.append(i)
                wk_l.append("Wk " + mo.group(1))
        cards = []
        for row in combos or []:
            name = str(row[0]).strip() if row else ""
            if not name or name.upper().startswith("TOTAL"):
                continue
            price = _rnum(row[price_i]) if price_i < len(row) else 0
            weeks = [{"label": wk_l[j], "sold": _rnum(row[wk_i[j]]) if wk_i[j] < len(row) else 0}
                     for j in range(len(wk_i))]
            total = sum(w["sold"] for w in weeks)
            all_b, picks = _combo_bags(name)
            bags = [{"name": b, "stock": int(region_stock.get(b, 0)), "star": b in picks} for b in all_b]
            stock = int(sum(region_stock.get(b, 0) for b in (picks or all_b)))
            last = weeks[-1]["sold"] if weeks else 0
            prev = weeks[-2]["sold"] if len(weeks) > 1 else last
            cards.append({
                "name": name, "price": price, "weeks": weeks, "total": total,
                "avg": round(total / len(weeks)) if weeks else 0,
                "bags": bags, "stock": stock, "diff": last - prev,
                "lastLabel": weeks[-1]["label"] if weeks else "Wk 1",
            })
        return cards

    def _groups(specs, stock):
        out = []
        for key, label, cards_k, hdr_k in specs:
            cards = _region_cards(offer.get(cards_k), offer.get(hdr_k), stock)
            if cards:
                out.append({"key": key, "label": label, "cards": cards})
        return out

    _sz_stock, _ug_stock = offer.get("sinzaStock", {}), offer.get("ugStock", {})
    _fill_from_odoo(_sz_stock, _SINZA_CODES, "Sinza/Dar")
    _fill_from_odoo(_ug_stock, _UGANDA_CODES, "Uganda")
    regions = {
        "sinza": {
            "label": "Sinza", "currency": "TSh",
            "totalStock": offer.get("totalSinzaStock"),
            "groups": _groups([
                ("combos",   "Combos",   "sinzaCombos",   "sinzaComboHeaders"),
                ("singles",  "Singles",  "sinzaSingles",  "sinzaSinglesHeaders"),
                ("specials", "Specials", "sinzaSpecials", "sinzaSpecialHeaders"),
            ], _sz_stock),
        },
        "uganda": {
            "label": "Uganda", "currency": "USh",
            "totalStock": offer.get("totalUgandaStock"),
            "groups": _groups([
                ("combos",  "Combos",  "ugCombos",  "ugComboHeaders"),
                ("singles", "Singles", "ugSingles", "ugSinglesHeaders"),
            ], _ug_stock),
        },
    }

    # ── Monetary implication: the full-price value of the bags a combo contains vs the
    #    combo's actual revenue = the money given away by bundling. Split self-made vs
    #    running. Baseline prices from bag_original_prices.json. ──
    _prices = _load_bag_prices()

    def _bag_price(b):
        return _prices.get(str(b).strip().upper(), 0)

    def _mi_row(name, units, actual, expected, missing):
        impl = expected - actual
        return {"combo": name, "units": int(units), "expected": int(round(expected)),
                "actual": int(round(actual)), "implication": int(round(impl)),
                "original": int(round(expected / units)) if units else 0,
                "discPct": round(impl / expected * 100, 1) if expected else 0.0,
                "missingPrice": missing}

    mi_running = []
    for rc in running_cards:
        exp = sum((b.get("sold", 0) or 0) * _bag_price(b["name"]) for b in rc.get("bags", []))
        miss = [b["name"] for b in rc.get("bags", []) if _bag_price(b["name"]) == 0]
        mi_running.append(_mi_row(rc.get("sheetLabel") or rc["name"], rc["total"], rc["value"], exp, miss))
    mi_self = []
    for r in self_made:
        _bags, _ = _combo_bags(r["name"])
        unit_full = sum(_bag_price(b) for b in _bags)
        miss = [b for b in _bags if _bag_price(b) == 0]
        mi_self.append(_mi_row(r["name"], r["qty"], r["value"], unit_full * r["qty"], miss))

    def _mi_tot(rows):
        e = sum(x["expected"] for x in rows)
        a = sum(x["actual"] for x in rows)
        return {"expected": e, "actual": a, "implication": e - a,
                "discPct": round((e - a) / e * 100, 1) if e else 0.0,
                "units": sum(x["units"] for x in rows), "combos": len(rows)}

    monetary_implication = {
        "running": sorted(mi_running, key=lambda x: -x["implication"]),
        "selfMade": sorted(mi_self, key=lambda x: -x["implication"]),
        "runTotals": _mi_tot(mi_running), "smTotals": _mi_tot(mi_self),
    }

    return {
        "month": month,
        "monthStart": m_start.isoformat(), "monthEnd": m_end.isoformat(),
        "selfMade": self_made, "running": running,
        "monetaryImplication": monetary_implication,
        "smTotals": agg(self_made), "runTotals": agg(running),
        "requests": requests, "reqCounts": st_counts,
        "reqTotal": len(requests),
        "runningCards": running_cards, "combosGoal": combos_goal,
        "offerTrend": offer_trend, "offerKpis": offer_kpis,
        "topBags": top_bags,
        "regions": regions,
        "comboUsage": combo_usage,
        # Component bags across the running combos — deal bags matching these are excluded
        # from the "Deal units sold" headline (already counted under the combos).
        "comboBags": sorted({str(b["name"]).upper() for rc in running_cards for b in rc.get("bags", [])}),
    }


def fetch():
    m_start, m_end = report_month.live_month_window()
    ok, _ = db.check_connection()
    if not ok:
        print("  Postgres not reachable — self_made_combos not updated.")
        return None
    payload = build_payload(m_start, m_end)
    deals = _read_deals(m_start.strftime("%B"))               # Power Deals / Deal of the Week
    if deals:
        # Reuse the sheet+Odoo-augmented Kenya stock built in build_payload, so deal
        # products the sheet had at 0 pick up live Odoo shop stock too.
        _stock = _AUGMENTED_STOCK or (_read_offer_analysis() or {}).get("stockMap", {})
        _enrich_deals(deals, m_start, m_end, _stock, set(payload.get("comboBags", [])))
    payload["deals"] = deals
    payload["bagsNotOnOffer"] = _bags_not_on_offer(
        m_start, m_end, set(payload.get("comboBags", [])), deals)
    return payload


def inject(payload):
    with open(HTML, "r", encoding="utf-8") as f:
        html = f.read()
    block = ("<!-- SMC_DATA_START -->\n<script>\nconst SMC = "
             + json.dumps(payload, ensure_ascii=False) + ";\n</script>\n<!-- SMC_DATA_END -->")
    html = re.sub(r"<!-- SMC_DATA_START -->.*?<!-- SMC_DATA_END -->", block, html, flags=re.DOTALL)
    # Embed the offer/combo data block here too, so the Monthly Report reads it from
    # this page (Offer Type Analysis has been retired). Function replacement avoids
    # re.sub treating backslashes in the block as backreferences.
    try:
        import offer_data
        oa_block = offer_data.build()[1]
        html = re.sub(r"<!-- OFFER_DATA_START -->.*?<!-- OFFER_DATA_END -->",
                      lambda _m: oa_block, html, flags=re.DOTALL)
    except Exception:
        pass
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    payload = fetch()
    if payload is None:
        return
    inject(payload)
    sm, run = payload["smTotals"], payload["runTotals"]
    rc = payload["reqCounts"]
    print(f"self_made_combos.html updated — {payload['month']} (Kenya).")
    print(f"  Self-made combos : {sm['count']} combos · {fmt(sm['units'])} units · KES {fmt(sm['value'])}")
    print(f"  Running combos   : {run['count']} combos · {fmt(run['units'])} units · KES {fmt(run['value'])}")
    print(f"  Combo requests   : {payload['reqTotal']} logged "
          f"({rc['approved']} approved · {rc['rejected']} rejected · {rc['pending']} pending)")
    if not os.environ.get("DENRI_LAUNCHER"):
        webbrowser.open_new_tab(pathlib.Path(HTML).as_uri())


if __name__ == "__main__":
    main()
