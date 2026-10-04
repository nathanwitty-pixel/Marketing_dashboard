"""lib/receipt_combos.py — Sinza & Uganda combos counted from POS receipts.

Those tills ring every bag as its own line, so a combo is several bags on one receipt at ONE shared
unit price. Per receipt: bags grouped by unit price → a group of >= 2 bags is a combo, a bag alone at
its price is a single; receipts with >= BULK_MIN bags are bulk (wholesale) and never combos. A combo
whose bag types fill a listed combo's slots (offers_outside.csv; same count, any order, alternatives)
is RUNNING, otherwise SELF-MADE. Spec: docs/self-made-combos.md › Sinza & Uganda.
"""
import csv
import datetime
import itertools
import os

from . import db

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OFFERS_CSV = os.path.join(BASE, "offers_outside.csv")
BULK_MIN = 7
TILLS = {"sinza": ("sinza", "dar-es-alam"), "uganda": ("uganda",)}
_SKIP = ("DELIVERY", "GIFT BAG", "DISCOUNT", "CUSTOMI", "STRAP")

RECEIPT_LINES_SQL = """
SELECT o.id AS receipt, o.date_order::date AS d, pt."name" AS product, pl.qty AS qty,
       pl.price_subtotal_incl AS amount
FROM pos_order o
JOIN pos_order_line pl ON pl.order_id = o.id
JOIN pos_session ps ON ps.id = o.session_id
JOIN pos_config pc ON pc.id = ps.config_id
JOIN product_product pp ON pp.id = pl.product_id
JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE lower(pc."name") IN :tills
  AND o.state IN ('paid', 'done', 'invoiced')
  AND o.date_order::date BETWEEN :s AND :e
  AND pl.qty > 0
"""


def load_offers(month_name, market):
    """{'combos': [...], 'singles': [...]} for the month/market from offers_outside.csv, or None.
    Each offer: {name, slots: [set(bag types)], was, now, disc, currency, wasKsh, nowKsh}."""
    try:
        with open(OFFERS_CSV, encoding="utf-8", newline="") as f:
            rows = [r for r in csv.DictReader(f)
                    if r["Month"].strip().lower() == month_name.lower() and r["Market"].strip().lower() == market]
    except OSError:
        return None
    if not rows:
        return None

    def num(v):
        try:
            return int(float(str(v).replace(",", "") or 0))
        except ValueError:
            return 0
    out = {"combos": [], "singles": []}
    for r in rows:
        o = {"name": r["Name"].strip(), "slots": [{x.strip().upper() for x in s.split("/") if x.strip()}
                                                   for s in r["Bags"].split("+")],
             "was": num(r["Was"]), "now": num(r["Now"]), "disc": num(r["Disc"]), "currency": r["Currency"],
             "wasKsh": num(r["Was KSH"]), "nowKsh": num(r["Now KSH"])}
        out["combos" if r["Type"].strip().lower() == "combo" else "singles"].append(o)
    return out


def bag_key(name, infer):
    """Catalogue bag type of a POS product (None = not a bag). Any sleeve → '*SLEEVE'."""
    n = str(name).upper()
    if any(k in n for k in _SKIP):
        return None
    if "SLEEVE" in n:
        return "*SLEEVE"
    return infer(name)


def _fits(bags, slots):
    """Bag types fill the offer's slots one-to-one in some order (alternatives per slot)."""
    if len(bags) != len(slots):
        return False
    return any(all(b in slots[i] for b, i in zip(bags, perm)) for perm in itertools.permutations(range(len(slots))))


def classify(lines, offers, infer, month_start):
    """lines: [{receipt, d, product, qty, amount}] → per-market summary:
    {running: {offer: {count, revenue, weeks{wk: n}}}, selfMade: {label: {...}}, singles: {bag: {...}},
     singlesOffer: {offer: {...}}, bulk: {receipts, bags, revenue}, receipts, comboReceipts}."""
    anchor = month_start - datetime.timedelta(days=(month_start.weekday() + 1) % 7)   # Sunday on/before day 1
    by_r = {}
    for ln in lines:
        k = bag_key(ln["product"], infer)
        q = int(round(float(ln["qty"] or 0)))
        if not k or q <= 0:
            continue
        unit = round(float(ln["amount"] or 0) / q)
        rec = by_r.setdefault(ln["receipt"], {"d": ln["d"], "bags": []})
        rec["bags"] += [(k, unit)] * q
    out = {"running": {}, "selfMade": {}, "singles": {}, "singlesOffer": {},
           "bulk": {"receipts": 0, "bags": 0, "revenue": 0}, "receipts": len(by_r), "comboReceipts": 0}

    def bump(table, key, units, rev, wk):
        e = table.setdefault(key, {"count": 0, "revenue": 0, "weeks": {}})
        e["count"] += 1
        e["revenue"] += rev
        e["weeks"][wk] = e["weeks"].get(wk, 0) + 1
        if units is not None:
            e.setdefault("bags", units)

    for rec in by_r.values():
        d = rec["d"] if isinstance(rec["d"], datetime.date) else datetime.date.fromisoformat(str(rec["d"])[:10])
        wk = (d - anchor).days // 7 + 1
        if len(rec["bags"]) >= BULK_MIN:
            out["bulk"]["receipts"] += 1
            out["bulk"]["bags"] += len(rec["bags"])
            out["bulk"]["revenue"] += sum(u for _, u in rec["bags"])
            continue
        groups = {}
        for k, unit in rec["bags"]:
            groups.setdefault(unit, []).append(k)
        had_combo = False
        for unit, bags in groups.items():
            if len(bags) >= 2:
                had_combo = True
                offer = next((o["name"] for o in (offers or {}).get("combos", []) if _fits(bags, o["slots"])), None)
                if offer:
                    bump(out["running"], offer, None, unit * len(bags), wk)
                else:
                    label = " + ".join(sorted(b.lstrip("*") for b in bags))
                    bump(out["selfMade"], label, sorted(bags), unit * len(bags), wk)
            else:
                b = bags[0]
                bump(out["singles"], b.lstrip("*"), None, unit, wk)
                offer = next((o["name"] for o in (offers or {}).get("singles", []) if b in o["slots"][0]), None)
                if offer:
                    bump(out["singlesOffer"], offer, None, unit, wk)
        out["comboReceipts"] += had_combo
    return out


def market_summary(market, month_start, month_end, infer, month_name=None):
    """classify() for a market's tills over the month, with that month's offers; None if offline."""
    offers = load_offers(month_name or month_start.strftime("%B"), market)
    try:
        df = db.run_query(RECEIPT_LINES_SQL.replace(":tills", "(" + ", ".join("'" + t + "'" for t in TILLS[market]) + ")"),
                          {"s": month_start.isoformat(), "e": month_end.isoformat()})
    except Exception as e:                                   # noqa: BLE001
        print(f"  {market} receipts unavailable: {e}")
        return None
    if df is None:
        return None
    lines = [{"receipt": r.receipt, "d": r.d, "product": r.product, "qty": r.qty, "amount": r.amount}
             for r in df.itertuples(index=False)]
    return {"offers": offers, **classify(lines, offers, infer, month_start)}
