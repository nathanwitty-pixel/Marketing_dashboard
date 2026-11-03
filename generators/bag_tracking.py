"""
generators/bag_tracking.py — Bag Tracking: the chosen bags' Kenya shop stock at the start (2 Nov 2026, 8 am) vs now,
what sold / came in since, and price was → now.            Spec: docs/bag-tracking.md
─────────────────────────────────────────────────────────────────
  • Bags + start time + price overrides: data/bag_tracking.json
  • Stock now: live Kenya shop stock (lib/stock), folded to bag names exactly as Offer Picking does
  • Since the start: done Odoo stock moves in / out of the Kenya shops (till sales move stock as they're rung)
  • Stock was: stock now worked back over those moves — once, then frozen in data/bag_tracking_baseline.json
  • Prices: Offer Picking's offers-sheet WAS / NOW (config `now` overrides)

Injects `BT` into bag_tracking.html between the BT_DATA markers.
─────────────────────────────────────────────────────────────────
"""
import os
import re
import sys
import json
import datetime as dt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root → lib/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))                   # generators/ → offer_picking
from lib import db, paths, stock
import offer_picking as op

CONFIG = paths.data("bag_tracking.json")
BASELINE = paths.data("bag_tracking_baseline.json")
HTML = paths.html("bag_tracking.html")

# Moves since the start that touch a Kenya shop, per product. A shop-to-shop move inside Kenya is in neither column.
MOVES_SQL = """
SELECT UPPER(pt."name") AS name,
  SUM(CASE WHEN d_in AND NOT s_in AND src.usage <> 'customer' THEN m.product_qty ELSE 0 END) AS received,
  SUM(CASE WHEN d_in AND src.usage = 'customer' THEN m.product_qty ELSE 0 END) AS returned,
  SUM(CASE WHEN s_in AND dest.usage = 'customer' THEN m.product_qty ELSE 0 END) AS sold,
  SUM(CASE WHEN s_in AND NOT d_in AND dest.usage <> 'customer' THEN m.product_qty ELSE 0 END) AS sent_out
FROM (SELECT m.*, (split_part(src.complete_name, '/', 1) IN ({codes}) AND src.usage = 'internal') AS s_in,
             (split_part(dest.complete_name, '/', 1) IN ({codes}) AND dest.usage = 'internal') AS d_in
      FROM stock_move m
      JOIN stock_location src ON src.id = m.location_id
      JOIN stock_location dest ON dest.id = m.location_dest_id
      WHERE m.state = 'done' AND m."date" >= :since) m
JOIN stock_location src ON src.id = m.location_id
JOIN stock_location dest ON dest.id = m.location_dest_id
JOIN product_product pp ON pp.id = m.product_id
JOIN product_template pt ON pt.id = pp.product_tmpl_id
WHERE (m.s_in OR m.d_in) AND position('+' in pt."name") = 0
GROUP BY 1
"""


def _cfg():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def _folder(cost, offers):
    """Odoo product name → the dashboard's bag name (Offer Picking's _build_catalog folding)."""
    bomkeys = sorted(cost.keys(), key=len, reverse=True)
    offer_keys = sorted(offers.keys(), key=len, reverse=True)

    def canon(nm):
        c, _, in_bom = op._resolve_bag(nm, cost, bomkeys)
        if not in_bom:
            c = next((k for k in offer_keys if c == k or c.startswith(k + " ")), c)
        return c
    return canon


def _moves(since_utc):
    codes = stock._inlist(stock.KENYA_SHOP_CODES)
    df = db.run_query(MOVES_SQL.format(codes=codes), {"since": since_utc.strftime("%Y-%m-%d %H:%M:%S")})
    out = {}
    for r in (df.itertuples(index=False) if df is not None else []):
        out[str(r.name).upper()] = {k: float(getattr(r, k) or 0) for k in ("received", "returned", "sold", "sent_out")}
    return out


def _colour(product, bag):
    return product[len(bag):].strip() if product.startswith(bag + " ") else product


def build():
    cfg = _cfg()
    start = dt.datetime.strptime(cfg["start"], "%Y-%m-%d %H:%M")          # Nairobi time
    since_utc = start - dt.timedelta(hours=3)                              # stock_move.date is UTC
    want = [str(b["bag"]).upper() for b in cfg["bags"]]
    over = {str(b["bag"]).upper(): b["now"] for b in cfg["bags"] if b.get("now")}

    cost = op._read_bom_costs()
    offers, offers_source = op._read_offers()
    canon = _folder(cost, offers)
    now_stock = stock.odoo_stock_by_product("kenya", positive_only=False)   # a bag sold out since 8 am still shows 0
    moves = _moves(since_utc)

    # per bag → per product (colour)
    prods = {}
    for nm in set(now_stock) | set(moves):
        b = canon(nm)
        if b in want:
            mv = moves.get(nm, {})
            prods.setdefault(b, {})[nm] = {"now": int(now_stock.get(nm, 0)), **{k: round(mv.get(k, 0)) for k in
                                                                                  ("received", "returned", "sold", "sent_out")}}

    # Stock was: frozen once per (start, product); a product not in the file yet is worked back from now
    try:
        base = json.load(open(BASELINE, encoding="utf-8"))
        if base.get("start") != cfg["start"]:
            base = None
    except (OSError, ValueError):
        base = None
    base = base or {"start": cfg["start"], "computedAt": None, "was": {}}
    changed = False
    for b, ps in prods.items():
        for nm, p in ps.items():
            if nm not in base["was"]:
                base["was"][nm] = p["now"] - p["received"] - p["returned"] + p["sold"] + p["sent_out"]
                changed = True
    if changed:
        base["computedAt"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(BASELINE, "w", encoding="utf-8") as f:
            json.dump(base, f, indent=1, ensure_ascii=False, sort_keys=True)

    catalog = {}
    try:
        catalog = {c["name"]: c for c in op._build_catalog(cost, {}, sorted(cost.keys(), key=len, reverse=True), offers)[0]}
    except Exception as ex:                                                 # noqa: BLE001
        print(f"  Prices unavailable: {ex}")

    rows = []
    for b in want:
        ps = prods.get(b, {})
        c = catalog.get(b, {})
        was_p, now_p = c.get("valueWas"), over.get(b) or c.get("valueNow")
        cols = []
        for nm, p in sorted(ps.items()):
            w = int(base["was"].get(nm, 0))
            if w or p["now"] or p["sold"] or p["received"] or p["sent_out"]:
                cols.append({"colour": _colour(nm, b), "was": w, "now": p["now"], "sold": p["sold"] - p["returned"],
                             "received": p["received"], "sentOut": p["sent_out"]})
        t = lambda k: sum(x[k] for x in cols)                               # noqa: E731
        rows.append({"bag": b, "category": c.get("category", ""), "was": t("was"), "now": t("now"), "sold": t("sold"),
                     "received": t("received"), "sentOut": t("sentOut"), "priceWas": was_p, "priceNow": now_p,
                     "colours": cols})

    payload = {"start": cfg["start"], "startLabel": start.strftime("%a %d %b %Y, %I:%M %p").replace(" 0", " "),
               "baselineAt": base.get("computedAt"), "built": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
               "priceSource": offers_source, "bags": rows}
    with open(HTML, encoding="utf-8") as f:
        html = f.read()
    block = ("<!-- BT_DATA_START -->\n<script>const BT = "
             + json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
             + ";</script>\n<!-- BT_DATA_END -->")
    html = re.sub(r"<!-- BT_DATA_START -->.*?<!-- BT_DATA_END -->", lambda _: block, html, flags=re.S)
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)
    return payload


if __name__ == "__main__":
    p = build()
    tot = lambda k: sum(r[k] for r in p["bags"])                            # noqa: E731
    print(f"bag_tracking.html updated: {len(p['bags'])} bags since {p['startLabel']}; "
          f"stock was {tot('was'):,} → now {tot('now'):,}, sold {tot('sold'):,}, received {tot('received'):,}")
    for r in p["bags"]:
        if not r["colours"]:
            print(f"  ⚠ no Odoo stock or moves for {r['bag']}")
