"""lib/oos_callbacks.py — "Out of stock — call back" demand from the WhatsApp Monitoring module.

Who asked for a bag on WhatsApp while it was out of stock, per shop. One source for the
New Products, Self-made vs Running Combos and Bags on vs off Offer menus (each page keys the
Odoo product names its own way, through `key_fn`).

Every number is DISTINCT PEOPLE: one person = phone_key, else WhatsApp username, else the
interaction itself (see sql/oos_callbacks.sql). Re-keying several Odoo names onto one page bag
unions the person sets — counts are never added, so a customer who asked for two shades of the
same bag still counts once.

Periods: lifetime / monthly (live report month) / weekly (this Sun–Sat week to date) /
lastweek (previous complete Sun–Sat week) / current (still waiting = not purchased since).
The bag is only recorded from June 2026, so lifetime effectively starts there.

Never raises: an unreachable DB (and no cached copy) gives [] rows → {} blocks → no chips.
"""
import os
import datetime

from . import db, report_month

_SQL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql", "oos_callbacks.sql")
PERIODS = ("lifetime", "monthly", "weekly", "lastweek", "current")


def load_rows():
    """[{date, shop, kind, person, purchased, product}] — one per OOS request × bag asked for."""
    try:
        with open(_SQL_PATH, encoding="utf-8") as f:
            df = db.run_query_cached(f.read(), ttl_min=20)
        if df is None:
            return []
        return [{"date": r.req_date if isinstance(r.req_date, datetime.date) else datetime.date.fromisoformat(str(r.req_date)[:10]),
                 "shop": str(r.shop), "kind": str(r.shop_kind or ""), "person": str(r.person),
                 "purchased": bool(r.is_purchased), "product": str(r.product)}
                for r in df.itertuples(index=False)]
    except Exception as e:                                   # noqa: BLE001 — never break a page build
        print(f"  OOS call-backs unavailable: {e}")
        return []


def windows(today=None):
    """{period: (start, end)} for the dated periods (lifetime / current are undated)."""
    today = today or datetime.date.today()
    m_start, m_end = report_month.live_month_window()
    ws = today - datetime.timedelta(days=(today.weekday() + 1) % 7)       # Sunday of this week
    return {"monthly": (m_start, m_end), "weekly": (ws, today),
            "lastweek": (ws - datetime.timedelta(days=7), ws - datetime.timedelta(days=1))}


def _in(period, r, wins):
    if period == "lifetime":
        return True
    if period == "current":
        return not r["purchased"]
    s, e = wins[period]
    return s <= r["date"] <= e


def _safe(fn, arg):
    try:
        return fn(arg)
    except Exception:                                        # noqa: BLE001 — an odd name just doesn't match
        return None


def collect(rows, key_fn=None, shop_filter=None, today=None, colour_fn=None):
    """{period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or None to
    drop the product; shop_filter(row) → False to leave a shop out (e.g. a market scope).
    With colour_fn(product) → colour, the shop level becomes {colour: {shop: set(person)}}."""
    wins = windows(today)
    out = {p: {} for p in PERIODS}
    keys, cols = {}, {}
    for r in rows:
        if shop_filter and not shop_filter(r):
            continue
        if r["product"] not in keys:
            keys[r["product"]] = _safe(key_fn, r["product"]) if key_fn else r["product"]
            if colour_fn:
                cols[r["product"]] = _safe(colour_fn, r["product"]) or "No colour"
        k = keys[r["product"]]
        if not k:
            continue
        for p in PERIODS:
            if _in(p, r, wins):
                node = out[p].setdefault(k, {})
                if colour_fn:
                    node = node.setdefault(cols[r["product"]], {})
                node.setdefault(r["shop"], set()).add(r["person"])
    return out


def _shops(shops):
    """{shop: set(person)} → (distinct people, [[shop, people], …] high → low)."""
    return (len(set().union(*shops.values())) if shops else 0,
            sorted(([s, len(v)] for s, v in shops.items()), key=lambda x: (-x[1], x[0])))


def aggregate(rows, key_fn=None, shop_filter=None, today=None, colour_fn=None):
    """The page block: {period: {key: {"total": people, "shops": [[shop, people], …]}}}, shops
    high → low. `total` is distinct people across shops (a person asking at two shops counts once).
    With colour_fn, each entry also carries "colours": [[colour, people, [[shop, people], …]], …]."""
    if not rows:
        return {}
    sets = collect(rows, key_fn, shop_filter, today, colour_fn)
    out = {}
    for p, bags in sets.items():
        out[p] = {}
        for k, node in bags.items():
            if colour_fn:
                merged = {}
                for shops in node.values():
                    for s, v in shops.items():
                        merged.setdefault(s, set()).update(v)
                total, shop_list = _shops(merged)
                cl = [[c] + list(_shops(shops)) for c, shops in node.items()]
                cl.sort(key=lambda x: (-x[1], x[0]))
                out[p][k] = {"total": total, "shops": shop_list, "colours": cl}
            else:
                total, shop_list = _shops(node)
                out[p][k] = {"total": total, "shops": shop_list}
    return out


def totals(block):
    """{period: {key: people}} from an aggregate() block."""
    return {p: {k: v["total"] for k, v in bags.items()} for p, bags in (block or {}).items()}


def oos_by_bag_shop(today=None):
    """{period: {product name: {shop: people}}} straight from Odoo names, or {} if unavailable."""
    sets = collect(load_rows(), today=today)
    if not any(sets.values()):
        return {}
    return {p: {k: {s: len(v) for s, v in shops.items()} for k, shops in bags.items()}
            for p, bags in sets.items()}


def attach_stock(block, key_fn, colour_fn=None, stock_by_code=None):
    """Add each shop's live on-hand to an aggregate() block, in place: every [shop, people]
    (bag level and under each colour) becomes [shop, people, stock], stock = that shop's units of
    the bag (or of that colour), matched with the page's own key_fn / colour_fn. stock is None for
    a shop with no stock location (Website — online). stock_by_code = {CODE: {NAME: qty}} (tests)."""
    if not block:
        return block
    if stock_by_code is None:
        from . import stock as lstock
        from .odoo_tabs import STOCK_CODE_TO_SHOP as code_to_shop
        try:
            stock_by_code = lstock.odoo_stock_by_shop_code(tuple(code_to_shop))
        except Exception as e:                               # noqa: BLE001 — counts still show
            print(f"  OOS call-backs: shop stock unavailable ({e})")
            stock_by_code = {}
    else:
        from .odoo_tabs import STOCK_CODE_TO_SHOP as code_to_shop
    shops_with_stock = {code_to_shop.get(c, c).upper() for c in stock_by_code}
    bag, col = {}, {}
    for code, names in (stock_by_code or {}).items():
        shop = code_to_shop.get(code, code).upper()
        for name, qty in names.items():
            k = _safe(key_fn, name)
            if not k:
                continue
            bag[(k, shop)] = bag.get((k, shop), 0) + qty
            if colour_fn:
                c = _safe(colour_fn, name) or "No colour"
                col[(k, c, shop)] = col.get((k, c, shop), 0) + qty

    def stk(table, key, shop):
        s = str(shop).upper()
        return table.get(key + (s,), 0) if s in shops_with_stock else None

    for bags in block.values():
        for k, e in bags.items():
            e["shops"] = [[s, n, stk(bag, (k,), s)] for s, n, *_ in e["shops"]]
            for c in e.get("colours", []):
                c[2] = [[s, n, stk(col, (k, c[0]), s)] for s, n, *_ in c[2]]
    return block
