"""receipt_combos.py — find combos in till receipts that ring every item as its own line, and classify them
as running (on the offer list) or self-made (skill: receipt-combo-detection). Pure Python.

    out = classify(lines, offers, infer, month_start)
    lines  = [{receipt, ref, d, product, qty, amount}]     one per receipt line (amount = line total incl. tax)
    offers = {"combos": [{name, slots: [set(types)]}], "singles": [{name, slots: [set(types)]}]}
    infer  = function(product name) -> catalogue type or None
"""
import datetime
import itertools

BULK_MIN = 5                     # >= this many items on one receipt = wholesale, never a combo
_SKIP = ("DELIVERY", "GIFT BAG", "DISCOUNT", "CUSTOMI", "STRAP")   # lines that are not products


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
    by_r, refunded = {}, set()
    for ln in lines:
        k = bag_key(ln["product"], infer)
        ref = str(ln.get("ref") or "")
        if ref.upper().endswith(" REFUND"):
            refunded.add(ref[:-len(" REFUND")].strip())          # cancels its original receipt
            continue
        q = int(round(float(ln["qty"] or 0)))
        if not k or q <= 0:
            continue
        unit = int(round(float(ln["amount"] or 0) / q, -1))     # to the nearest 10: 40,000 = 40,001
        rec = by_r.setdefault(ln["receipt"], {"d": ln["d"], "bags": [], "ref": ref})
        rec["bags"] += [(k, unit)] * q
    by_r = {k: v for k, v in by_r.items() if not v["ref"] or v["ref"] not in refunded}
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
        groups = {}
        for k, unit in rec["bags"]:
            groups.setdefault(unit, []).append(k)
        combos, left = [], []                     # [(bags, revenue)], [(bag, price)]
        for unit, bags in groups.items():
            if len(bags) >= 2:
                combos.append((bags, unit * len(bags)))
            else:
                left.append((bags[0], unit))
        if len(left) >= 2:                        # sold together at different prices = one combo
            combos.append(([b for b, _ in left], sum(u for _, u in left)))
            left = []
        for bags, rev in combos:
            offer = next((o["name"] for o in (offers or {}).get("combos", []) if _fits(bags, o["slots"])), None)
            if offer:
                bump(out["running"], offer, None, rev, wk, d.isoformat())
            else:
                label = " + ".join(sorted(b.lstrip("*") for b in bags))
                bump(out["selfMade"], label, sorted(bags), rev, wk, d.isoformat())
        for b, unit in left:
            bump(out["singles"], b.lstrip("*"), None, unit, wk)
            offer = next((o["name"] for o in (offers or {}).get("singles", []) if b in o["slots"][0]), None)
            if offer:
                bump(out["singlesOffer"], offer, None, unit, wk)
        out["comboReceipts"] += bool(combos)
    return out
