"""lib/receipt_combos.py — Sinza & Uganda combos counted from POS receipts.

Those tills ring every bag as its own line; a client printed out with more than one bag bought a combo.
Per receipt (refunded receipts dropped; >= BULK_MIN bags = bulk, never a combo): bags at one shared unit
price (rounded to 10) = a combo per price; the bags left over = one more combo if two or more (Uganda
splits a combo's price unevenly), a single if one. A combo
whose bag types fill a listed combo's slots (offers_monthly.csv; same count, any order, alternatives)
is RUNNING, otherwise SELF-MADE. Spec: docs/self-made-combos.md › Sinza & Uganda.
A listed SINGLE whose name carries colours ("Jumbo blue", "Elyse black/red") counts only bags of those colours
(16 Nov 2026); a name with no colour ("Nizana", "MINIZURI") counts every colour of the bag.
"""
import collections
import csv
import datetime
import itertools
import os
import re

from . import db

from lib import paths

OFFERS_CSV = paths.data("offers_monthly.csv")
BULK_MIN = 5
TILLS = {"sinza": ("sinza", "dar-es-alam"), "uganda": ("uganda",)}
_SKIP = ("DELIVERY", "GIFT BAG", "DISCOUNT", "CUSTOMIZATION", "STRAP")

RECEIPT_LINES_SQL = """
SELECT o.id AS receipt, o."name" AS ref, o.date_order::date AS d, pt."name" AS product, pl.qty AS qty,
       pl.price_subtotal_incl AS amount, pl.product_id AS product_id, pl.parent_id AS parent
FROM pos_order o
JOIN pos_order_line pl ON pl.order_id = o.id
JOIN pos_session ps ON ps.id = o.session_id
JOIN pos_config pc ON pc.id = ps.config_id
JOIN product_product pp ON pp.id = pl.product_id
JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE lower(pc."name") IN :tills
  AND o.state IN ('paid', 'done', 'invoiced')
  AND o.date_order::date BETWEEN :s AND :e
"""


def load_offers(month_name, market):
    """{'combos': [...], 'singles': [...]} for the month/market from offers_monthly.csv, or None.
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
        o["colours"] = _name_colours(o["name"], o["slots"])
        out["combos" if r["Type"].strip().lower() == "combo" else "singles"].append(o)
    return out


def _words(s):
    return {w for w in re.split(r"[^A-Z0-9]+", str(s).upper()) if w}


def _name_colours(name, slots):
    """Colour words in an offer's name beyond its bag types: "Elyse black/red" → {BLACK, RED}; "Nizana" → set()
    (= every colour). Only words lib/colours knows as colours (bag_names.csv), so "MINIZURI" / "man" never count."""
    from . import colours
    colours._load()
    bag_words = set().union(*[_words(b) for slot in slots for b in slot]) if slots else set()
    return {w for w in _words(name) - bag_words if w in (colours._WORDS or {})}


def single_offer(bag, rec, singles):
    """The listed single offer a receipt's single `bag` belongs to, or None. A coloured offer takes a bag of its
    colour (the product names on the receipt, rec["names"][bag], each used once); a colourless one takes any."""
    cands = [o for o in singles if bag in o["slots"][0]]
    if not cands:
        return None
    pool = rec.get("names", {}).get(bag, [])
    for i, nm in enumerate(pool):
        w = _words(nm)
        o = next((o for o in cands if o.get("colours") and o["colours"] & w), None)
        if o:
            pool.pop(i)
            return o
    o = next((o for o in cands if not o.get("colours")), None)
    if o and pool:
        pool.pop(0)
    return o


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


def _id(v):
    """A nullable id column (NaN / None → None)."""
    try:
        return None if v is None or v != v else int(v)
    except (TypeError, ValueError):
        return None


def _receipts(lines, infer):
    """Receipt lines → {receipt: {d, bags: [(bag, unit)], ref}} with refunds netted off; also the refunded refs.
    A combo product line ('A + B') isn't a bag: its bags are its KES 0 sub-lines on the same receipt, which share
    its price evenly (25 Oct 2026 — it was counted as one extra bag). With no KES 0 bags it counts as before.
    Sub-lines whose parent_id is a combo line's product on the receipt belong to that combo only, one combo per
    unit of its qty (rec["fixed"]: [[(bag, unit)]], each a combo of its own — 20 Nov 2026, two combos on one
    receipt were one 4-bag combo). A "<ref> REFUND" receipt takes its bags off the original receipt, which is
    dropped only when nothing is left (a refund with a combo line still drops the whole receipt)."""
    by_r, refunds, wraps = {}, {}, {}
    for ln in lines:
        k = bag_key(ln["product"], infer)
        ref = str(ln.get("ref") or "")
        if ref.upper().endswith(" REFUND"):
            refunds.setdefault(ref[:-len(" REFUND")].strip(), []).append((k, ln))   # netted off its receipt below
            continue
        q = int(round(float(ln["qty"] or 0)))
        pid = _id(ln.get("product_id"))
        if q <= 0 or not (k or ("+" in str(ln["product"]) and pid is not None)):
            continue                                             # a '+' line with no bag name may still own sub-lines
        rec = by_r.setdefault(ln["receipt"], {"d": ln["d"], "bags": [], "ref": ref})
        if "+" in str(ln["product"]):
            wraps.setdefault(ln["receipt"], []).append((k, q, float(ln["amount"] or 0), pid))
            continue
        unit = int(round(float(ln["amount"] or 0) / q, -1))     # to the nearest 10: 40,000 = 40,001
        rec.setdefault("names", {}).setdefault(k, []).extend([str(ln["product"])] * q)
        par = _id(ln.get("parent"))
        if unit == 0 and par is not None:                        # a combo's sub-line: placed with its combo below
            rec.setdefault("kids", {}).setdefault(par, collections.Counter())[k] += q
            continue
        rec["bags"] += [(k, unit)] * q
    for r, rec in by_r.items():
        kids, ws = rec.pop("kids", {}), wraps.get(r, [])
        own = {}                                                 # combo product → [qty, amount]
        for k, q, a, pid in ws:
            if pid is not None and pid in kids:
                e = own.setdefault(pid, [0, 0.0])
                e[0] += q
                e[1] += a
        for pid, (n, a) in own.items():
            cnt = kids.pop(pid)
            split = n > 1 and all(c % n == 0 for c in cnt.values())
            per = {b: c // n for b, c in cnt.items()} if split else dict(cnt)
            groups = n if split else 1
            unit = int(round(a / groups / max(sum(per.values()), 1), -1))
            for _ in range(groups):
                g = [(b, unit) for b, c in per.items() for _ in range(c)]
                rec["bags"] += g
                if len(g) >= 2:                                  # one bag alone is judged by price, as before
                    rec.setdefault("fixed", []).append(g)
        for cnt in kids.values():                                # parent matched no combo line: plain KES 0 bags
            for b, c in cnt.items():
                rec["bags"] += [(b, 0)] * c
        ws = [w for w in ws if w[3] not in own and w[0]]
        if not ws:
            continue
        bags = rec["bags"]
        fixed = {id(t) for g in rec.get("fixed", []) for t in g}
        zeros = [i for i, t in enumerate(bags) if t[1] == 0 and id(t) not in fixed]
        if zeros:
            unit = int(round(sum(a for _k, _q, a, _p in ws) / len(zeros), -1))
            for i in zeros:
                bags[i] = (bags[i][0], unit)
        else:
            for k, q, a, _p in ws:
                bags += [(k, int(round(a / q, -1)))] * q
    for ref, rls in refunds.items():
        for rec in (v for v in by_r.values() if v["ref"] == ref):
            if any("+" in str(ln["product"]) for _k, ln in rls):
                rec["bags"] = []                                 # a combo came back: drop the receipt as before
                continue
            for k, ln in rls:
                q = -int(round(float(ln["qty"] or 0)))
                if not k or q <= 0:
                    continue
                unit = int(round(-float(ln["amount"] or 0) / q, -1))
                for _ in range(q):
                    bags = rec["bags"]
                    i = next((i for i, t in enumerate(bags) if t == (k, unit)), None)
                    if i is None:
                        i = next((i for i, t in enumerate(bags) if t[0] == k), None)
                    if i is None:
                        break
                    t = bags.pop(i)
                    pool = rec.get("names", {}).get(k, [])
                    if str(ln["product"]) in pool:
                        pool.remove(str(ln["product"]))
                    elif pool:
                        pool.pop()
                    for g in rec.get("fixed", []):
                        if t in g:                               # its combo is broken: the rest judged by price
                            rec["fixed"].remove(g)
                            break
    return {k: v for k, v in by_r.items() if v["bags"]}, set(refunds)


def _groups(bags, fixed=None):
    """One receipt's [(bag, unit)] → ([(bags, revenue)] combos, [(bag, unit)] singles): each fixed group (a combo
    line's own bags, rec["fixed"]) = one combo; of the rest, same unit price = a combo per price; two or more
    leftover bags at different prices = one more combo; one leftover = a single."""
    bags, combos = list(bags), []
    for g in fixed or ():
        for t in g:
            bags.remove(t)
        combos.append(([b for b, _ in g], sum(u for _, u in g)))
    groups = {}
    for k, unit in bags:
        groups.setdefault(unit, []).append(k)
    left = []
    for unit, bs in groups.items():
        if len(bs) >= 2:
            combos.append((bs, unit * len(bs)))
        else:
            left.append((bs[0], unit))
    if len(left) >= 2:                        # sold together at different prices = one combo
        combos.append(([b for b, _ in left], sum(u for _, u in left)))
        left = []
    return combos, left


def offer_split(lines, offers, infer):
    """On / not on offer for Sinza / Uganda (docs/bags-on-offer.md › Sinza & Uganda): every combo (running or
    self-made) and single sales of a bag on the market's listed singles are ON offer; every other single is NOT
    on offer; 5+ bag receipts are bulk (others). Returns {combos: {running: {count, bags, revenue}, selfMade:
    {…}}, onSingles: {bag: {units, revenue}}, offSingles: {bag: {units, revenue, comboBag}}, bulk: {receipts,
    bags, revenue}, comboBags: {bag: units in self-made combos}, bags, revenue}."""
    recs, _ = _receipts(lines, infer)
    singles = (offers or {}).get("singles", [])
    listed_combo_bags = {b for o in (offers or {}).get("combos", []) for slot in o["slots"] for b in slot}
    out = {"combos": {"running": {"count": 0, "bags": 0, "revenue": 0}, "selfMade": {"count": 0, "bags": 0, "revenue": 0}},
           "onSingles": {}, "offSingles": {}, "bulk": {"receipts": 0, "bags": 0, "revenue": 0}, "comboBags": {},
           "bags": sum(len(v["bags"]) for v in recs.values()),
           "revenue": sum(u for v in recs.values() for _, u in v["bags"])}
    for rec in recs.values():
        if len(rec["bags"]) >= BULK_MIN:
            out["bulk"]["receipts"] += 1
            out["bulk"]["bags"] += len(rec["bags"])
            out["bulk"]["revenue"] += sum(u for _, u in rec["bags"])
            continue
        combos, left = _groups(rec["bags"], rec.get("fixed"))
        for bags, rev in combos:
            running = any(_fits(bags, o["slots"]) for o in (offers or {}).get("combos", []))
            c = out["combos"]["running" if running else "selfMade"]
            c["count"] += 1
            c["bags"] += len(bags)
            c["revenue"] += rev
            if not running:
                for b in bags:
                    out["comboBags"][b.lstrip("*")] = out["comboBags"].get(b.lstrip("*"), 0) + 1
        for b, unit in left:
            side = out["onSingles"] if single_offer(b, rec, singles) else out["offSingles"]
            e = side.setdefault(b.lstrip("*"), {"units": 0, "revenue": 0})
            e["units"] += 1
            e["revenue"] += unit
            if side is out["offSingles"]:
                e["comboBag"] = b in listed_combo_bags
    return out


def classify(lines, offers, infer, month_start):
    """lines: [{receipt, d, product, qty, amount}] → per-market summary:
    {running: {offer: {count, revenue, weeks{wk: n}}}, selfMade: {label: {...}}, singles: {bag: {...}},
     singlesOffer: {offer: {...}}, bulk: {receipts, bags, revenue}, receipts, comboReceipts}."""
    anchor = month_start - datetime.timedelta(days=(month_start.weekday() + 1) % 7)   # Sunday on/before day 1
    by_r, refunded = _receipts(lines, infer)
    out = {"running": {}, "selfMade": {}, "singles": {}, "singlesOffer": {},
           "bulk": {"receipts": 0, "bags": 0, "revenue": 0}, "receipts": len(by_r), "comboReceipts": 0,
           "refunded": len(refunded),
           "bags": sum(len(v["bags"]) for v in by_r.values()),               # every bag the till sold
           "revenue": sum(u for v in by_r.values() for _, u in v["bags"])}

    def bump(table, key, units, rev, wk, day=None):
        e = table.setdefault(key, {"count": 0, "revenue": 0, "weeks": {}, "days": {}})
        e["count"] += 1
        e["revenue"] += rev
        e["weeks"][wk] = e["weeks"].get(wk, 0) + 1
        if day:
            e["days"][day] = e["days"].get(day, 0) + 1          # the receipt date, for "sold on"
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
        combos, left = _groups(rec["bags"], rec.get("fixed"))     # [(bags, revenue)], [(bag, price)]
        for bags, rev in combos:
            offer = next((o["name"] for o in (offers or {}).get("combos", []) if _fits(bags, o["slots"])), None)
            if offer:
                bump(out["running"], offer, None, rev, wk, d.isoformat())
            else:
                label = " + ".join(sorted(b.lstrip("*") for b in bags))
                bump(out["selfMade"], label, sorted(bags), rev, wk, d.isoformat())
        for b, unit in left:
            bump(out["singles"], b.lstrip("*"), None, unit, wk)
            o = single_offer(b, rec, (offers or {}).get("singles", []))
            if o:
                bump(out["singlesOffer"], o["name"], None, unit, wk)
        out["comboReceipts"] += bool(combos)
    return out


def market_lines(market, start, end):
    """Receipt lines for a market's tills between start and end (inclusive), or None if offline."""
    try:
        df = db.run_query(RECEIPT_LINES_SQL.replace(":tills", "(" + ", ".join("'" + t + "'" for t in TILLS[market]) + ")"),
                          {"s": start.isoformat(), "e": end.isoformat()})
    except Exception as e:                                   # noqa: BLE001
        print(f"  {market} receipts unavailable: {e}")
        return None
    if df is None:
        return None
    return [{"receipt": r.receipt, "ref": r.ref, "d": r.d, "product": r.product, "qty": r.qty, "amount": r.amount,
             "product_id": r.product_id, "parent": r.parent} for r in df.itertuples(index=False)]


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
    lines = [{"receipt": r.receipt, "ref": r.ref, "d": r.d, "product": r.product, "qty": r.qty, "amount": r.amount,
              "product_id": r.product_id, "parent": r.parent} for r in df.itertuples(index=False)]
    return {"offers": offers, **classify(lines, offers, infer, month_start)}
