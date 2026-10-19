"""lib/runway_bags.py — RUNWAY BAGS: bag types first created in Odoo in the last 30 days.

Not part of the New Products (data/new_products.txt) — a separate metric on the New Products page
("Runway bags sold"). docs/new-products.md › Runway bags.

How a bag is identified:
  • every product template in a Bags / … category, active or archived, is folded to its BAG TYPE —
    the catalogue bag when the classifier knows it (product_targets.bag_key_fn), else the name with
    its trailing colour words dropped ("Noria Sky Blue" → NORIA, "Zela Creame" → ZELA);
  • the type's FIRST CREATED = the earliest create_date of any of its templates — so a new colour
    of an old bag (Code 3 Ankara Grey) is not a runway bag, only a brand-new type is;
  • runway = first created within the last RUNWAY_DAYS days, minus samples / custom / test items
    (EXCLUDE) and minus this month's New Products.
Sold = POS bags (same rules as the page's sold: incl. bags inside combos), folded the same way.
"""
import datetime
import re

RUNWAY_DAYS = 30

# Not real catalogue bags: samples, one-off custom orders, tests, sponsorship, packaging.
EXCLUDE = re.compile(r"^(SAMPLE|CUSTOM|CUSTOMISED|CUSTOMIZED|TEST|ZZ\b|SPONSORSHIP|PPM\b|-$)")

# Colour words dropped from the end of a name to get its bag type (on top of lib/colours' words).
_COLOUR_WORDS = {
    "BLACK", "BROWN", "GREY", "GRAY", "BLUE", "SKY", "NAVY", "RED", "PINK", "BEIGE", "TAN", "WHITE",
    "GREEN", "MAROON", "CREAM", "CREAME", "PURPLE", "YELLOW", "ORANGE", "GOLD", "SILVER", "KHAKI",
    "OLIVE", "WINE", "DARK", "LIGHT", "CHOCOLATE", "COFFEE", "MUSTARD", "TEAL", "PEACH", "NUDE",
    "MULTI", "MULTICOLOR", "MULTICOLOUR", "CAMEL", "LILAC", "MINT", "CRACKED", "SPICE", "OBSIDIAN",
}

_TEMPLATES_SQL = """
SELECT pt.create_date::date AS created, pt.name AS tmpl, COALESCE(pc.name, '') AS categ
FROM product_template pt
JOIN product_category pc ON pc.id = pt.categ_id
WHERE pc.complete_name ILIKE 'Bags%'
"""


def _strip(name):
    return re.sub(r"^\[[^\]]*\]\s*", "", str(name or "").upper().strip())


def type_fn():
    """Product name → bag type (see the module docstring)."""
    from lib import product_targets
    words = set(_COLOUR_WORDS)
    try:
        from lib import colours
        colours._load()
        words |= {str(w).upper() for w in (colours._WORDS or {})}
    except Exception:                                        # noqa: BLE001 — the built-in words still work
        pass
    key = product_targets.bag_key_fn()

    def typ(name):
        k = key(name)
        if k:
            return k
        t = _strip(name).replace("(", " (").split()
        while len(t) > 1 and t[-1].strip("()") in words:
            t.pop()
        return " ".join(t)
    return typ


def runway_bags(today=None, days=RUNWAY_DAYS, typ=None):
    """[{name, created, category}] newest first — the runway bag types as of today; [] if Odoo is down."""
    from lib import db, new_products_list
    today = today or datetime.date.today()
    typ = typ or type_fn()
    df = db.run_query(_TEMPLATES_SQL, {})
    if df is None:
        return []
    first = {}                                               # TYPE -> (created, category)
    for r in df.itertuples():
        t = typ(r.tmpl)
        if t and (t not in first or r.created < first[t][0]):
            first[t] = (r.created, r.categ)
    new = set(new_products_list.names())
    cutoff = today - datetime.timedelta(days=days)
    out = [{"name": t, "created": c.isoformat(), "category": cat}
           for t, (c, cat) in first.items()
           if c >= cutoff and t not in new and not EXCLUDE.match(t)
           and not any(t == n or t.startswith(n + " ") for n in new)]
    return sorted(out, key=lambda b: (b["created"], b["name"]), reverse=True)


def sold_by_type(names, start, end, typ):
    """{TYPE: bags sold} for the given runway types over [start, end] — POS bags, combo sub-lines included."""
    from lib import db, queries
    want = set(names)
    out = {n: 0 for n in names}
    params = {"start_date": start.isoformat(), "end_date": end.isoformat()}
    for sql in (queries.WEEKLY_BAGS_SOLD,
                queries.WEEKLY_BAGS_SOLD.replace("COALESCE(l.sub_product_line, false)   = false",
                                                 "COALESCE(l.sub_product_line, false)   = true")):
        df = db.run_query(sql, params)
        for r in (df.itertuples() if df is not None else []):
            t = typ(r.product)
            if t in want:
                out[t] += int(round(float(r.bags or 0)))
    return out


def shop_sales_by_type(names, start, end, typ):
    """{TYPE: {"kes", "shops": {SHOP: {"n", "kes"}}}} for the runway types over [start, end] — POS lines by till,
    the Sold rules (combo sub-lines included; they carry little or no KES — the combo line holds the money)."""
    from lib import db, queries
    want = set(names)
    out = {n: {"kes": 0, "shops": {}} for n in names}
    params = {"start_date": start.isoformat(), "end_date": end.isoformat()}
    base = ("SELECT upper(pc.\"name\") AS shop, l.full_product_name AS product, SUM(l.qty)::numeric AS bags, "
            "SUM(l.price_subtotal_incl)::numeric AS value FROM pos_order_line l JOIN pos_order o ON o.id = l.order_id "
            "JOIN pos_session ps ON ps.id = o.session_id JOIN pos_config pc ON pc.id = ps.config_id "
            "WHERE " + queries._BAGS_WHERE + " GROUP BY 1, 2")
    for sql in (base, base.replace("COALESCE(l.sub_product_line, false)   = false",
                                   "COALESCE(l.sub_product_line, false)   = true")):
        df = db.run_query(sql, params)
        for r in (df.itertuples() if df is not None else []):
            t = typ(r.product)
            if t not in want:
                continue
            shop = str(r.shop or "").strip().title() or "?"
            x = out[t]["shops"].setdefault(shop, {"n": 0, "kes": 0})
            x["n"] += int(round(float(r.bags or 0)))
            x["kes"] += int(round(float(r.value or 0)))
            out[t]["kes"] += int(round(float(r.value or 0)))
    for t in out:
        out[t]["shops"] = {k: v for k, v in out[t]["shops"].items() if v["n"] or v["kes"]}
    return out


def stock_by_type(names, typ):
    """({TYPE: Kenya shop on-hand}, {TYPE: Sinza + Uganda on-hand}) — live Odoo."""
    from lib import stock
    want = set(names)
    res = []
    for region in ("kenya", "outside"):
        acc = {n: 0 for n in names}
        for prod, q in (stock.odoo_stock_by_product(region) or {}).items():
            t = typ(prod)
            if t in want:
                acc[t] += int(q or 0)
        res.append(acc)
    return res[0], res[1]


def build(windows, today=None):
    """The NP.runway payload: {days, bags: [{name, created, category, stockKe, stockOut}],
    sold: {period: {TYPE: n}}}. windows = {period: (start, end)} (lifetime = since creation)."""
    today = today or datetime.date.today()
    typ = type_fn()
    bags = runway_bags(today, typ=typ)
    names = [b["name"] for b in bags]
    sold = {}
    if names:
        for per, (s, e) in windows.items():
            sold[per] = sold_by_type(names, s, min(e, today), typ)
        sold["lifetime"] = sold_by_type(names, min(datetime.date.fromisoformat(b["created"]) for b in bags), today, typ)
        first = min(datetime.date.fromisoformat(b["created"]) for b in bags)
        shops = {per: shop_sales_by_type(names, s, min(e, today), typ) for per, (s, e) in windows.items()}
        shops["lifetime"] = shop_sales_by_type(names, first, today, typ)
        ke, out = stock_by_type(names, typ)
        for b in bags:
            b["stockKe"], b["stockOut"] = ke.get(b["name"], 0), out.get(b["name"], 0)
    return {"days": RUNWAY_DAYS, "bags": bags, "sold": sold, "shops": shops if names else {}}
