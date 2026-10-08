"""shop_launch.py — the Shop Launch page: a new shop from its first sale (spec: docs/shop-launch.md).

Opening stock from the workplan sheet (or its saved CSV), sales live from the shop's Odoo till, a day-by-day
race against the benchmark launch, and the Kenya marketing posts on the bags it stocks.

    python shop_launch.py        # DENRI_LAUNCHER=1 to skip the browser tab
"""
import csv
import datetime
import json
import os
import re
import webbrowser

from lib import db, queries, stock as lstock

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "shop_launch.html")
CONFIG = os.path.join(BASE, "shop_launch_config.json")
CATALOG = os.path.join(BASE, "product_catalog.csv")
POSTS_SHEET = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"     # MONTHLY / WEEKLY_MARKETING_POST

# The headline "bags sold" rules (sql/bags_sold_total.sql), per day × product, for one till.
SALES_SQL = """
SELECT p.date_order::date AS d, UPPER(pt."name") AS name,
       SUM(pl.qty)::numeric AS bags, ROUND(SUM(pl.price_subtotal_incl))::numeric AS kes
FROM pos_order p
JOIN pos_order_line pl ON pl.order_id = p.id
JOIN pos_session ps ON p.session_id = ps.id
JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
WHERE UPPER(pc."name") = :till
  AND p.date_order::date BETWEEN :s AND :e
  AND p.state IN ('done', 'invoiced', 'paid')
  AND pl.qty <> 0
  AND COALESCE(pt."name", '') NOT LIKE '%+%'
  AND COALESCE(pt."name", '') NOT ILIKE '%delivery%'
  AND COALESCE(pt."name", '') NOT ILIKE '%customization%'
  AND COALESCE(pt."name", '') NOT ILIKE '%strap%'
  AND COALESCE(pt."name", '') NOT ILIKE '%KES discount%'
  AND COALESCE(pt."name", '') NOT ILIKE '%sample%'
  AND COALESCE(pcat."name", '') NOT ILIKE '%Pos%'
  AND lower(COALESCE(pt."name", '')) <> ALL(:excluded)
GROUP BY 1, 2
"""


def _cfg():
    with open(CONFIG, encoding="utf-8") as fh:
        return json.load(fh)


# ── Opening stock (the workplan) ──
def _parse_workplan(rows):
    """[[bag, colour, qty], …] → {BAG: {COLOUR: qty}} (TOTAL and blank rows skipped, zero quantities dropped)."""
    out = {}
    for r in rows:
        if len(r) < 3:
            continue
        bag, col = str(r[0]).strip().upper(), str(r[1]).strip().upper()
        if not bag or bag == "BAG TYPE" or col == "TOTAL":
            continue
        try:
            q = int(float(str(r[2]).replace(",", "") or 0))
        except ValueError:
            continue
        if q > 0:
            out.setdefault(bag, {})
            out[bag][col] = out[bag].get(col, 0) + q
    return out


def load_workplan(cfg):
    """(opening stock, source) — the live sheet, else the saved CSV."""
    try:
        from google_auth import get_gspread_client
        rows = get_gspread_client().open_by_key(cfg["workplanSheet"]).sheet1.get_all_values()
        wp = _parse_workplan(rows)
        if wp:
            return wp, "live sheet"
    except Exception as e:                                   # noqa: BLE001 — fall back to the saved copy
        print(f"  Workplan sheet unavailable ({type(e).__name__}) — using {cfg['workplanCsv']}")
    with open(os.path.join(BASE, cfg["workplanCsv"]), encoding="utf-8") as fh:
        return _parse_workplan(list(csv.reader(fh))), "saved copy"


# ── Product name → workplan bag type / colour ──
def make_matcher(bag_types):
    catalog = {}
    try:
        with open(CATALOG, encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                catalog[str(r.get("PRODUCT NAME", "")).strip().upper()] = str(r.get("BAG TYPE", "")).strip().upper()
    except OSError:
        pass
    by_len = sorted(set(bag_types) | {b for b in catalog.values() if b}, key=len, reverse=True)

    def match(name):
        n = str(name).strip().upper()
        n = re.sub(r"^STANDARD TRAVEL(?= |$)", "TRAVEL", n)   # Odoo "Standard Travel Grey" = workplan / catalogue TRAVEL
        bag = catalog.get(n) or next((b for b in by_len if n == b or n.startswith(b + " ")), None)
        if not bag:
            return None, None
        col = n[len(bag):].strip() if n.startswith(bag) else ""
        return bag, (col or "—")
    return match


def till_sales(till, s, e):
    try:
        df = db.run_query(SALES_SQL, {"till": till.upper(), "s": s.isoformat(), "e": e.isoformat(),
                                      "excluded": queries.excluded_products()})
    except Exception as ex:                                  # noqa: BLE001
        print(f"  Sales unavailable for {till} ({ex})")
        return []
    if df is None:
        return []
    return [{"d": r["d"], "name": r["name"], "bags": float(r["bags"] or 0), "kes": float(r["kes"] or 0)}
            for _, r in df.iterrows()]


def first_sale(till):
    """Launch day 1 = the first day the till sold a bag (by the same rules), or None."""
    days = [r["d"] for r in till_sales(till, datetime.date(2024, 1, 1), datetime.date.today()) if r["bags"] > 0]
    return min(days) if days else None


def kenya_posts():
    """({BAG: posts this month}, {BAG: posts last week}) from col D / col E (Kenya), or (None, None)."""
    try:
        from google_auth import get_gspread_client
        sh = get_gspread_client().open_by_key(POSTS_SHEET)
        out = []
        for tab in ("MONTHLY_MARKETING_POST", "WEEKLY_MARKETING_POST"):
            per = {}
            for r in sh.worksheet(tab).get_all_values()[1:]:
                if len(r) < 5 or not str(r[3]).strip():
                    continue
                try:
                    n = int(float(str(r[4]).replace(",", "") or 0))
                except ValueError:
                    continue
                b = str(r[3]).strip().upper()
                per[b] = per.get(b, 0) + n
            out.append(per)
        return out[0], out[1]
    except Exception as e:                                   # noqa: BLE001
        print(f"  Posts unavailable ({e}) — posting columns empty.")
        return None, None


def build():
    cfg = _cfg()
    today = datetime.date.today()
    days = int(cfg.get("days", 28))
    wp, wp_source = load_workplan(cfg)
    match = make_matcher(wp)
    opened = first_sale(cfg["till"])

    # Sales since launch, per bag and colour, and per launch day.
    bags, daily, other = {}, {}, {"bags": 0, "kes": 0, "names": {}}
    if opened:
        for r in till_sales(cfg["till"], opened, today):
            bag, col = match(r["name"])
            day = (r["d"] - opened).days + 1
            daily.setdefault(day, [0, 0])
            daily[day][0] += r["bags"]
            daily[day][1] += r["kes"]
            if not bag:
                other["bags"] += r["bags"]
                other["kes"] += r["kes"]
                other["names"][r["name"]] = other["names"].get(r["name"], 0) + r["bags"]
                continue
            b = bags.setdefault(bag, {"sold": 0, "kes": 0, "cols": {}})
            b["sold"] += r["bags"]
            b["kes"] += r["kes"]
            b["cols"][col] = b["cols"].get(col, 0) + r["bags"]

    # Live on-hand at the shop (0 until stock is transferred there).
    on_hand = {}
    for names in lstock.odoo_stock_by_shop_code((cfg["stockCode"],), positive_only=False).values():
        for name, q in names.items():
            bag, col = match(name)
            if bag:
                c = on_hand.setdefault(bag, {})
                c[col] = c.get(col, 0) + q
    stock_live = any(q for c in on_hand.values() for q in c.values())

    month_posts, week_posts = kenya_posts()
    rows = []
    for bag in sorted(set(wp) | set(bags)):
        opening = sum(wp.get(bag, {}).values())
        s = bags.get(bag, {"sold": 0, "kes": 0, "cols": {}})
        left = sum(on_hand.get(bag, {}).values()) if stock_live else max(opening - s["sold"], 0)
        cols = []
        for col in sorted(set(wp.get(bag, {})) | set(s["cols"]), key=lambda c: -wp.get(bag, {}).get(c, 0)):
            o, sd = wp.get(bag, {}).get(col, 0), s["cols"].get(col, 0)
            cols.append([col, o, round(sd), on_hand.get(bag, {}).get(col, 0) if stock_live else max(o - sd, 0)])
        rows.append({"bag": bag, "opening": opening, "sold": round(s["sold"]), "kes": round(s["kes"]), "left": left,
                     "inWorkplan": bag in wp, "postsMonth": None if month_posts is None else month_posts.get(bag, 0),
                     "postsWeek": None if week_posts is None else week_posts.get(bag, 0), "colours": cols})
    rows.sort(key=lambda r: (-r["sold"], -r["opening"], r["bag"]))

    # Benchmark: the earlier launch's first `days` days.
    bm = cfg.get("benchmark") or {}
    bm_daily = {}
    bm_open = first_sale(bm["till"]) if bm.get("till") else None
    if bm_open:
        for r in till_sales(bm["till"], bm_open, bm_open + datetime.timedelta(days=days - 1)):
            day = (r["d"] - bm_open).days + 1
            bm_daily.setdefault(day, [0, 0])
            bm_daily[day][0] += r["bags"]
            bm_daily[day][1] += r["kes"]

    day_n = (today - opened).days + 1 if opened else 0
    return {
        "shop": cfg["shop"], "till": cfg["till"], "generated": datetime.datetime.now().strftime("%d %b %Y %H:%M"),
        "opened": opened.isoformat() if opened else None, "day": day_n, "days": days,
        "workplanSource": wp_source, "stockLive": stock_live, "postsKnown": month_posts is not None,
        "openingTotal": sum(sum(c.values()) for c in wp.values()),
        "daily": [[d, round(v[0]), round(v[1])] for d, v in sorted(daily.items())],
        "benchmark": {"shop": bm.get("shop"), "opened": bm_open.isoformat() if bm_open else None,
                      "daily": [[d, round(v[0]), round(v[1])] for d, v in sorted(bm_daily.items())]},
        "rows": rows,
        "other": {"bags": round(other["bags"]), "kes": round(other["kes"]),
                  "names": sorted(([n, round(q)] for n, q in other["names"].items()), key=lambda x: -x[1])[:15]},
    }


def inject(payload):
    with open(HTML, encoding="utf-8") as fh:
        html = fh.read()
    block = ("<!-- LAUNCH_DATA_START -->\n<script>\nconst SL = "
             + json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
             + ";\n</script>\n<!-- LAUNCH_DATA_END -->")
    html = re.sub(r"<!-- LAUNCH_DATA_START -->.*?<!-- LAUNCH_DATA_END -->", lambda _m: block, html, flags=re.S)
    with open(HTML, "w", encoding="utf-8") as fh:
        fh.write(html)


if __name__ == "__main__":
    data = build()
    inject(data)
    sold = sum(r["sold"] for r in data["rows"])
    print(f"{HTML} updated — {data['shop']}: "
          + (f"day {data['day']} since {data['opened']}, {sold} bags sold" if data["opened"] else "not open yet")
          + f"; opening stock {data['openingTotal']} ({data['workplanSource']}); "
          + f"benchmark {data['benchmark']['shop']} from {data['benchmark']['opened']}")
    if os.environ.get("DENRI_LAUNCHER") != "1":
        webbrowser.open("file://" + HTML)
