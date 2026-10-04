"""stockout_demand.py — distinct people who asked for each product while it was out of stock, per period, shop
and colour, with the shop's stock beside each count (skill: stockout-demand). Pure Python.

    rows  = [{date, shop, person, purchased, product}]   one per enquiry x product asked for
    block = aggregate(rows, key_fn=to_product, colour_fn=to_colour, today=date.today(), month_window=(first, last))
"""
import datetime

PERIODS = ("lifetime", "monthly", "weekly", "lastweek", "current")


def windows(today, month_window):
    """{period: (start, end)} for the dated periods. month_window = (first, last day) of the month to report."""
    ws = today - datetime.timedelta(days=(today.weekday() + 1) % 7)       # Sunday of this week
    return {"monthly": month_window, "weekly": (ws, today),
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


def collect(rows, key_fn=None, shop_filter=None, today=None, colour_fn=None, month_window=None):
    """{period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or None to
    drop the product; shop_filter(row) → False to leave a shop out (e.g. a market scope).
    With colour_fn(product) → colour, the shop level becomes {colour: {shop: set(person)}}."""
    today = today or datetime.date.today()
    wins = windows(today, month_window or (today.replace(day=1), today))
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


def aggregate(rows, key_fn=None, shop_filter=None, today=None, colour_fn=None, month_window=None):
    """The page block: {period: {key: {"total": people, "shops": [[shop, people], …]}}}, shops
    high → low. `total` is distinct people across shops (a person asking at two shops counts once).
    With colour_fn, each entry also carries "colours": [[colour, people, [[shop, people], …]], …]."""
    if not rows:
        return {}
    sets = collect(rows, key_fn, shop_filter, today, colour_fn, month_window)
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


def attach_stock(block, key_fn, colour_fn, stock_by_shop):
    """Add each shop's on-hand to an aggregate() block, in place: [shop, people] becomes [shop, people, stock]
    (product level, and per colour). stock_by_shop = {shop: {product name: qty}}; shops not in it get None
    (e.g. an online channel with no shelf)."""
    if not block:
        return block
    have = {str(s).upper() for s in stock_by_shop}
    bag, col = {}, {}
    for shop, names in stock_by_shop.items():
        s = str(shop).upper()
        for name, qty in names.items():
            k = _safe(key_fn, name)
            if not k:
                continue
            bag[(k, s)] = bag.get((k, s), 0) + qty
            if colour_fn:
                c = _safe(colour_fn, name) or "No colour"
                col[(k, c, s)] = col.get((k, c, s), 0) + qty

    def stk(table, key, shop):
        s = str(shop).upper()
        return table.get(key + (s,), 0) if s in have else None

    for bags in block.values():
        for k, e in bags.items():
            e["shops"] = [[s, n, stk(bag, (k,), s)] for s, n, *_ in e["shops"]]
            for c in e.get("colours", []):
                c[2] = [[s, n, stk(col, (k, c[0]), s)] for s, n, *_ in c[2]]
    return block
