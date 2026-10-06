"""lib/oos_callbacks.py — "Out of stock — call back" demand, ONLINE and WALK-IN.

Who asked for a bag while it was out of stock, per shop, from two Odoo modules:
  • online  — WhatsApp Monitoring (denri_monitor_*; sql/oos_callbacks.sql);
  • walkin  — the leads module (denri_lead; sql/oos_walkin.sql): leads whose status is, or ever was,
              "Awaiting stock", captured at the shops. Branches map onto the WhatsApp shop names.
One source for the New Products, Self-made vs Running Combos and Bags on vs off Offer menus (each
page keys the Odoo product names its own way, through `key_fn`). Every row carries "channel".

Every number is DISTINCT PEOPLE: one person = phone_key, else WhatsApp username, else the
interaction itself (see sql/oos_callbacks.sql). Re-keying several Odoo names onto one page bag
unions the person sets — counts are never added, so a customer who asked for two shades of the
same bag still counts once.

Periods: lifetime / monthly (live report month) / weekly (this Sun–Sat week to date) /
lastweek (previous complete Sun–Sat week) / current (still waiting, any date — same as lifetime now).

NET (Oct 2026): every count is people who asked in the period AND are still waiting — a request that was
bought since (WhatsApp is_purchased, or a lead no longer "Awaiting stock") drops out, so the chip, the
"to remind" figure and every list agree. Each entry also carries "asked" = gross people who asked in the
period, so the popover can say "12 still waiting · 15 asked, 3 already bought".
WhatsApp records the bag from June 2026; walk-in leads go back to January 2026.
Each bag's entry also carries the split: "online" / "walkin" (distinct people per channel — a
person who asked in both counts once in "total"), "shopCh" {shop: [online, walkin]} and, on each
colour, a 4th item {shop: [online, walkin]}.

Never raises: an unreachable DB (and no cached copy) gives [] rows → {} blocks → no chips.
"""
import os
import re
import datetime

from . import db, report_month

_SQL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql")
_SQL_PATH = os.path.join(_SQL_DIR, "oos_callbacks.sql")
_WALKIN_SQL_PATH = os.path.join(_SQL_DIR, "oos_walkin.sql")
PERIODS = ("lifetime", "monthly", "weekly", "lastweek", "current")
CHANNELS = ("online", "walkin")

# Leads-module branch → the WhatsApp Monitoring shop name (and its kind), so both channels share
# one shop list. Branches that aren't shops (marketing, shoot, staff, rejects) are left out.
_BRANCH_SHOP = {"KTDA SHOP": "Ktda", "DAR-ES-ALAM": "Sinza", "WEBSITE SALES": "Website", "JUMIA": "Website",
                "FLASH SALE HILTON": "Hilton", "FLASH SALE MOMBASA": "Mombasa"}
_BRANCH_SKIP = {"MARKETING", "SHOOT", "STAFF POS", "REJECTS"}
_SHOP_KIND = {"Website": "online", "Uganda": "region"}


def _date(v):
    return v if isinstance(v, datetime.date) else datetime.date.fromisoformat(str(v)[:10])


def _txt(v):
    """Odoo translatable names can come back as {'en_US': …}."""
    if isinstance(v, dict):
        v = v.get("en_US") or next(iter(v.values()), "")
    return "" if v is None or str(v) in ("nan", "None") else str(v).strip()


def _online_rows():
    with open(_SQL_PATH, encoding="utf-8") as f:
        df = db.run_query_cached(f.read(), ttl_min=20)
    if df is None:
        return []
    return [{"date": _date(r.req_date), "shop": str(r.shop), "kind": str(r.shop_kind or ""), "person": str(r.person),
             "purchased": bool(r.is_purchased), "product": _txt(r.product), "channel": "online"}
            for r in df.itertuples(index=False)]


def _walkin_rows():
    with open(_WALKIN_SQL_PATH, encoding="utf-8") as f:
        df = db.run_query_cached(f.read(), ttl_min=20)
    if df is None:
        return []
    out = []
    for r in df.itertuples(index=False):
        branch = _txt(r.branch).upper()
        if not branch or branch in _BRANCH_SKIP:
            continue
        shop = _BRANCH_SHOP.get(branch, branch.title())
        product = _txt(r.product)
        if not product:                       # free-text bag: add the colour when it is a single one
            product, colour = _txt(r.product_text), _txt(r.colour_text)
            if colour and not re.search(r"[,/&]|\bany\b|\band\b", colour, re.I):
                product = f"{product} {colour}"
        if not product:
            continue
        digits = re.sub(r"\D", "", _txt(r.phone))
        name = _txt(r.customer_name).lower()
        person = digits[-9:] if len(digits) >= 9 else (f"n:{name}@{shop}" if name else f"L{r.lead_id}")
        out.append({"date": _date(r.req_date), "shop": shop, "kind": _SHOP_KIND.get(shop, "shop"), "person": person,
                    # still waiting = still "Awaiting stock"; anything else has been dealt with
                    "purchased": r.state != "awaiting_stock", "product": product, "channel": "walkin"})
    return out


def load_rows():
    """[{date, shop, kind, person, purchased, product, channel}] — one per OOS request × bag asked for,
    online (WhatsApp) and walk-in (leads). Either side failing just leaves it out."""
    rows = []
    for name, fn in (("online (WhatsApp)", _online_rows), ("walk-in (leads)", _walkin_rows)):
        try:
            rows += fn()
        except Exception as e:                               # noqa: BLE001 — never break a page build
            print(f"  OOS call-backs {name} unavailable: {e}")
    return rows


def windows(today=None, custom=None):
    """{period: (start, end)} for the dated periods (lifetime / current are undated).
    custom = (from, to) adds a "custom" period (a page's Custom range — lib/custom_range.py)."""
    today = today or datetime.date.today()
    m_start, m_end = report_month.live_month_window()
    ws = today - datetime.timedelta(days=(today.weekday() + 1) % 7)       # Sunday of this week
    out = {"monthly": (m_start, m_end), "weekly": (ws, today),
           "lastweek": (ws - datetime.timedelta(days=7), ws - datetime.timedelta(days=1))}
    if custom:
        out["custom"] = tuple(custom)
    return out


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


def collect(rows, key_fn=None, shop_filter=None, today=None, colour_fn=None, custom=None):
    """{period: {key: {shop: set(person)}}}. key_fn(product) → the page's bag key, or None to
    drop the product; shop_filter(row) → False to leave a shop out (e.g. a market scope).
    With colour_fn(product) → colour, the shop level becomes {colour: {shop: set(person)}}."""
    wins = windows(today, custom)
    periods = PERIODS + (("custom",) if custom else ())
    out = {p: {} for p in periods}
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
        for p in periods:
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


def aggregate(rows, key_fn=None, shop_filter=None, today=None, colour_fn=None, custom=None):
    """The page block: {period: {key: {"total": people, "shops": [[shop, people], …]}}}, shops
    high → low. `total` is distinct people across shops (a person asking at two shops counts once).
    With colour_fn, each entry also carries "colours": [[colour, people, [[shop, people], …]], …]."""
    if not rows:
        return {}
    # Gross (everyone who asked) only for the "N asked, M already bought" line; every shown count is NET.
    gross = collect(rows, key_fn, shop_filter, today, colour_fn, custom)
    rows = [r for r in rows if not r["purchased"]]
    sets = collect(rows, key_fn, shop_filter, today, colour_fn, custom)
    # The same, per channel — for the online / walk-in split on every bag, shop and colour.
    by_ch = {ch: collect([r for r in rows if r.get("channel", "online") == ch], key_fn, shop_filter, today, colour_fn, custom)
             for ch in CHANNELS}

    def flat(node):                                   # {colour: {shop: set}} → {shop: set}
        merged = {}
        for shops in node.values():
            for s, v in shops.items():
                merged.setdefault(s, set()).update(v)
        return merged

    def split(p, k, colour=None):
        """({shop: [online, walkin]}, online people, walk-in people) for a bag (or one of its colours)."""
        per, tot = {}, []
        for i, ch in enumerate(CHANNELS):
            node = by_ch[ch].get(p, {}).get(k, {})
            shops = (node.get(colour, {}) if colour is not None else flat(node)) if colour_fn else node
            for s, v in shops.items():
                per.setdefault(s, [0, 0])[i] = len(v)
            tot.append(len(set().union(*shops.values())) if shops else 0)
        return per, tot[0], tot[1]

    out = {}
    for p, bags in sets.items():
        out[p] = {}
        for k, node in bags.items():
            if colour_fn:
                total, shop_list = _shops(flat(node))
                cl = [[c] + list(_shops(shops)) + [split(p, k, c)[0]] for c, shops in node.items()]
                cl.sort(key=lambda x: (-x[1], x[0]))
                e = {"total": total, "shops": shop_list, "colours": cl}
            else:
                total, shop_list = _shops(node)
                e = {"total": total, "shops": shop_list}
            e["shopCh"], e["online"], e["walkin"] = split(p, k)
            g = gross.get(p, {}).get(k, {})
            g = flat(g) if colour_fn else g
            e["asked"] = len(set().union(*g.values())) if g else total
            out[p][k] = e
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
