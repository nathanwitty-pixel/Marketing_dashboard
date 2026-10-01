#!/usr/bin/env python3
"""push_planner.py — Push Planner: what to push this week, where, and why bags aren't moving.
Spec: docs/push-planner.md. Writes push_planner.html (data block <!-- PP_DATA_START/END -->).

    python push_planner.py              # build the page
    python push_planner.py --dry-run    # load + compute, print a summary, write nothing
"""
from __future__ import annotations

import datetime
import json
import os
import sys
import time
from collections import defaultdict

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from lib import db, report_month                     # noqa: E402
from lib import stock as lstock                       # noqa: E402
from lib.odoo_tabs import STOCK_CODE_TO_SHOP          # noqa: E402
import self_made_combos as smc                        # noqa: E402  (shared bag SQL + bag_classifier)

MARKETS = ("kenya", "sinza", "uganda")
DAILY_SQL = {"kenya": smc.BAG_SALES_DAILY_SQL, "sinza": smc.BAG_SALES_DAILY_SINZA_SQL,
             "uganda": smc.BAG_SALES_DAILY_UGANDA_SQL}
WINDOW_DAYS = 28        # sales history per bag
SHOP_DAYS = 14          # Kenya per-shop sales window

# Kenya per-shop sales: the same product filters as the per-day bag query, by till.
SHOP_SALES_SQL = """
SELECT UPPER(COALESCE(pc."name", 'WEBSITE')) AS till, UPPER(pt."name") AS name, SUM(pl.qty)::int AS units
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
LEFT JOIN product_product pp ON pl.product_id=pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0
  AND NOT COALESCE(pl.sub_product_line, false)
  AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
  AND pt."name" NOT LIKE '%+%'
  AND pt."name" NOT ILIKE '%delivery%' AND pt."name" NOT ILIKE '%customi%'
  AND pt."name" NOT ILIKE '%strap%' AND pt."name" NOT ILIKE 'gift bag%'
GROUP BY 1, 2
"""


def _till_to_shop(till):
    """POS till name → the shop name used by STOCK_CODE_TO_SHOP ('KTDA SHOP' → 'KTDA')."""
    t = (till or "").upper().strip()
    if t.endswith(" SHOP"):
        t = t[:-5].strip()
    return {"WEBSITE SALES": "WEBSITE", "JUMIA": "WEBSITE"}.get(t, t)


def _prices():
    try:
        with open(os.path.join(BASE, "bag_original_prices.json"), encoding="utf-8") as f:
            return {k: v for k, v in json.load(f).items() if not k.startswith("_")}
    except (OSError, ValueError):
        return {}


def load_data(today=None):
    """Raw inputs rolled up to bag type. Returns a dict (see keys below) or None if Odoo is down."""
    ok, msg = db.check_connection()
    if not ok:
        print(f"  DB unreachable — {msg}")
        return None
    today = today or datetime.date.today()
    end = today - datetime.timedelta(days=1)                  # last full day
    start = end - datetime.timedelta(days=WINDOW_DAYS - 1)
    infer, _ = smc.bag_classifier(set())
    prices = _prices()
    m_start, m_end = report_month.live_month_window()

    daily = {}            # market -> bag -> {date iso: units}
    stock = {}            # market -> bag -> units
    unmatched = {}        # market -> units sold that didn't resolve to a bag type
    for mk in MARKETS:
        df = db.run_query_cached(DAILY_SQL[mk], {"s": start, "e": end}, ttl_min=30)
        per = defaultdict(lambda: defaultdict(int))
        miss = 0
        for r in ([] if df is None else df.itertuples(index=False)):
            bag = infer(r.name)
            if bag is None:
                miss += int(r.units or 0)
                continue
            per[bag][str(r.d)[:10]] += int(r.units or 0)
        daily[mk] = {b: dict(v) for b, v in per.items()}
        unmatched[mk] = miss
        st = defaultdict(int)
        for name, qty in (lstock.odoo_stock_by_product(market=mk) or {}).items():
            bag = infer(name)
            if bag:
                st[bag] += int(qty or 0)
        stock[mk] = dict(st)

    # Kenya per shop: stock (by location code) + 14-day sales (by till).
    shop_stock = defaultdict(lambda: defaultdict(int))
    for code, items in (lstock.odoo_stock_by_shop_code() or {}).items():
        shop = STOCK_CODE_TO_SHOP.get(code, code)
        for name, qty in items.items():
            bag = infer(name)
            if bag:
                shop_stock[shop][bag] += int(qty or 0)
    s14 = end - datetime.timedelta(days=SHOP_DAYS - 1)
    shop_sales = defaultdict(lambda: defaultdict(int))
    df = db.run_query_cached(SHOP_SALES_SQL, {"s": s14, "e": end}, ttl_min=30)
    for r in ([] if df is None else df.itertuples(index=False)):
        bag = infer(r.name)
        if bag:
            shop_sales[_till_to_shop(r.till)][bag] += int(r.units or 0)

    return {
        "start": start.isoformat(), "end": end.isoformat(), "today": today.isoformat(),
        "monthStart": m_start.isoformat(), "monthEnd": m_end.isoformat(),
        "daily": daily, "stock": stock, "unmatched": unmatched, "prices": prices,
        "shopStock": {s: dict(v) for s, v in shop_stock.items()},
        "shopSales": {s: dict(v) for s, v in shop_sales.items()},
    }


def load_pages(infer):
    """Posting (PA) + Self-made combos (SMC) + new products, per market and bag type.

    Returns {"posting": {market: {bag: {...}}}, "onOffer": {market: set}, "isNew": set,
             "postingWindow": str, "smcMonth": str}. Posting rows carry the region's own on-offer
    flag (docs/posting-yields.md › "On offer" definition), so that is the on-offer source for all
    three markets; SMC's on-offer names (combos, Power Deals, Deal of the Week) are added for Kenya.
    """
    from lib.month_extras import _block, _posting_block, POSTING_HTML
    pa = _posting_block(os.path.join(BASE, POSTING_HTML)) or {}
    smc_page = _block(os.path.join(BASE, "self_made_combos.html"), "SMC") or {}

    def bag_of(row):
        return infer(row.get("bagType") or "") or infer(row.get("productName") or "")

    posting, on_offer = {}, {}
    for mk in MARKETS:
        reg = pa if mk == "kenya" else (pa.get(mk) or {})
        py = reg.get("postYield") or {}
        dc = ((reg.get("deadClear") or {}).get("monthly") or {}).get("bags") or []
        per = defaultdict(lambda: {"postsMonth": 0, "postsLastWeek": 0, "expected": 0.0, "credited": 0.0,
                                   "soldMonth": 0, "available": 0, "deadVariants": 0, "variants": 0})
        offer = set()
        for r in (py.get("monthly") or {}).get("bags") or []:
            b = bag_of(r)
            if not b:
                continue
            x = per[b]
            x["postsMonth"] += int(r.get("posts") or 0)
            x["expected"] += float(r.get("expected") or 0)
            x["credited"] += float(r.get("credited") or 0)
            if r.get("onOffer"):
                offer.add(b)
        for r in (py.get("lastweek") or {}).get("bags") or []:
            b = bag_of(r)
            if b:
                per[b]["postsLastWeek"] += int(r.get("posts") or 0)
        for r in dc:
            b = bag_of(r)
            if not b:
                continue
            x = per[b]
            x["soldMonth"] += int(r.get("sold") or 0)
            x["available"] += int(r.get("available") or 0)
            x["variants"] += 1
            x["deadVariants"] += 1 if r.get("dead") else 0
            if r.get("onOffer"):
                offer.add(b)
        for x in per.values():
            x["yieldPct"] = round(100 * x["credited"] / x["expected"], 1) if x["expected"] else None
            x["clearPct"] = round(100 * x["soldMonth"] / x["available"], 1) if x["available"] else None
        posting[mk], on_offer[mk] = {b: dict(v) for b, v in per.items()}, offer

    for name in (smc_page.get("onOfferSources") or {}):
        b = infer(name)
        if b:
            on_offer["kenya"].add(b)
    try:
        from lib.new_products_list import names as _np_names
        is_new = {b for b in (infer(n) for n in (_np_names() or [])) if b}
    except Exception:                                             # noqa: BLE001 — sheet may be unreachable
        is_new = set()
    return {"posting": posting, "onOffer": on_offer, "isNew": is_new,
            "postingWindow": ((pa.get("postYield") or {}).get("monthly") or {}).get("window") or "",
            "smcMonth": smc_page.get("month") or ""}


def _categories():
    """{BAG: CATEGORY} from bag_tiers.csv (the Bags on offer menu's editable table)."""
    import csv
    out = {}
    try:
        with open(os.path.join(BASE, "bag_tiers.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(ln for ln in f if not ln.startswith("#")):
                if r.get("BAG"):
                    out[r["BAG"].strip().upper()] = (r.get("CATEGORY") or "").strip().upper()
    except OSError:
        pass
    return out


def build_facts(data, pages):
    """Facts for every bag × market that has stock or sold in the window (lib/push_rules)."""
    from lib import push_rules as pr
    cats = _categories()
    rows = []
    for mk in MARKETS:
        bags = set(data["stock"][mk]) | set(data["daily"][mk])
        for b in sorted(bags):
            if b.startswith("GIFT") or cats.get(b, "").startswith("GIFT"):
                continue                       # gift bags are given away, not sold — nothing to push
            rows.append(pr.facts(b, mk, data["daily"][mk].get(b, {}), data["stock"][mk].get(b, 0), data["end"],
                                 posting=pages["posting"][mk].get(b), on_offer=b in pages["onOffer"][mk],
                                 is_new=b in pages["isNew"], price=data["prices"].get(b),
                                 category=cats.get(b, ""), window=WINDOW_DAYS))
    return pr.add_peers(rows)


def build_actions(rows, data, today=None):
    """Adds action / says / units / confidence / score to each facts row; returns (rows, moves, top)."""
    from lib import push_rules as pr
    today = today or datetime.date.today()
    m_start = datetime.date.fromisoformat(data["monthStart"])
    m_end = datetime.date.fromisoformat(data["monthEnd"])
    urg = pr.urgency((today - m_start).days, (m_end - m_start).days + 1)
    med = pr.posting_median(rows)
    for r in rows:
        code, says, units, conf = pr.action(r, post_median=med.get(r["market"], 0))
        r.update(action=code, says=says, units=round(units, 1), confidence=round(conf, 2),
                 score=pr.score(units, r["price"], urg, conf))
    mv = pr.moves(data["shopStock"], data["shopSales"], days=SHOP_DAYS)
    price = data["prices"]
    move_rows = [{"bag": m["bag"], "market": "kenya", "action": "MOVE_STOCK", "says": m["says"], "units": m["qty"],
                  "confidence": 0.8, "score": pr.score(m["qty"], price.get(m["bag"]), urg, 0.8), "move": m}
                 for m in mv]
    allr = rows + move_rows
    top = pr.rank(allr, n=15, per_action=5)
    # Kenya's volumes are ~10x the others', so Sinza and Uganda get their own ranked lists too.
    top_by = {mk: pr.rank([r for r in allr if r["market"] == mk], n=8, per_action=3) for mk in MARKETS}
    return rows, mv, top, top_by


def build_reasons(rows, data):
    """Adds notMoving + reasons to every row (lib/push_rules.reasons). Returns the not-moving rows,
    most stock-value first."""
    from lib import push_rules as pr
    ctx = pr.context(rows, data["shopStock"], data["shopSales"])
    stuck = []
    for r in rows:
        r["notMoving"] = pr.not_moving(r)
        r["reasons"] = pr.reasons(r, ctx) if r["notMoving"] else []
        if r["notMoving"]:
            stuck.append(r)
    stuck.sort(key=lambda r: -(r["stock"] * (r["price"] or 2500)))
    return stuck


HISTORY_FILE = os.path.join(BASE, "push_planner_history.json")


def weekly(top, data, today=None, write=True):
    """Last week's calls checked against what happened (lib/push_rules.followup), then this week's
    top actions stored (replacing this week's entry if the planner already ran this week)."""
    from lib import push_rules as pr
    today = today or datetime.date.today()
    try:
        with open(HISTORY_FILE, encoding="utf-8") as f:
            hist = json.load(f)
    except (OSError, ValueError):
        hist = {}
    wk, rows = pr.followup(hist, data["daily"], data["stock"], today)
    if write:
        hist = pr.record_week(hist, pr.week_start(today), top)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(hist, f, indent=1, ensure_ascii=False, default=str)
    return {"week": wk, "rows": rows, "thisWeek": str(pr.week_start(today)), "weeksStored": len(hist)}


HTML_FILE = os.path.join(BASE, "push_planner.html")
START, END = "<!-- PP_DATA_START -->", "<!-- PP_DATA_END -->"
_KEEP = ("bag", "market", "category", "price", "stock", "sold7", "soldPrev7", "sold28", "perDay", "daysCover",
         "momentum", "postsMonth", "postsLastWeek", "yieldPct", "clearPct", "onOffer", "isNew", "peerPrice",
         "peerPerDay", "action", "says", "score", "confidence", "reasons", "laya", "move")


def _slim(r):
    return {k: r[k] for k in _KEEP if k in r and r[k] not in (None, [], {})}


def _kenya_target():
    """Kenya's month target from current_performance.html (PERF.totalTarget), or None."""
    import re
    try:
        with open(os.path.join(BASE, "current_performance.html"), encoding="utf-8") as f:
            m = re.search(r'totalTarget:\s*"([\d,]+)"', f.read())
        return int(m.group(1).replace(",", "")) if m else None
    except OSError:
        return None


def month_progress(data, today=None):
    """Per market: sold this month so far (from the daily sales), days elapsed / left, pace, and for
    Kenya the bags a day still needed to reach the target."""
    today = today or datetime.date.today()
    ms, me = datetime.date.fromisoformat(data["monthStart"]), datetime.date.fromisoformat(data["monthEnd"])
    elapsed = max(0, (min(today, me + datetime.timedelta(days=1)) - ms).days)   # full days before today
    left = max(0, (me - today).days + 1)
    out = {}
    for mk in MARKETS:
        sold = sum(u for b in data["daily"][mk].values() for d, u in b.items() if data["monthStart"] <= d < today.isoformat())
        row = {"sold": sold, "daysElapsed": elapsed, "daysLeft": left, "daysInMonth": (me - ms).days + 1,
               "pacePerDay": round(sold / elapsed, 1) if elapsed else None,
               "last28PerDay": round(sum(u for b in data["daily"][mk].values() for u in b.values()) / WINDOW_DAYS, 1)}
        if mk == "kenya":
            tgt = _kenya_target()
            if tgt:
                row.update(target=tgt, neededPerDay=round(max(0, tgt - sold) / left, 1) if left else None)
        out[mk] = row
    return out


def payload(data, pages, rows, mv, top, top_by, stuck, lay, wkly):
    by_mk = {mk: [_slim(r) for r in stuck if r["market"] == mk][:40] for mk in MARKETS}
    return {
        "generated": datetime.datetime.now().strftime("%d %b %Y %H:%M"),
        "salesWindow": f"{data['start']} → {data['end']}", "postingWindow": pages["postingWindow"],
        "month": month_progress(data),
        "top": [_slim(r) for r in top], "topBy": {mk: [_slim(r) for r in v] for mk, v in top_by.items()},
        "notMoving": by_mk,
        "notMovingCount": {mk: sum(1 for r in stuck if r["market"] == mk) for mk in MARKETS},
        "reasonCounts": {mk: {x["code"]: sum(1 for r in stuck if r["market"] == mk for y in r["reasons"] if y["code"] == x["code"])
                              for r in stuck if r["market"] == mk for x in r["reasons"]} for mk in MARKETS},
        "moves": mv[:30],
        "weekly": wkly,
        "laya": {k: v for k, v in lay.items() if k != "label"},
        "counts": {"bags": len(rows), "actions": {a: sum(1 for r in rows if r.get("action") == a) for a in
                   ("RESTOCK", "STOP_POSTS", "PUT_ON_OFFER", "POST_MORE", "WATCH")}, "moves": len(mv)},
    }


def inject(pp):
    import re
    with open(HTML_FILE, encoding="utf-8") as f:
        html = f.read()
    block = START + "\n<script>\nconst PP = " + json.dumps(pp, ensure_ascii=False, default=str).replace("</", "<\\/") + ";\n</script>\n" + END
    new, n = re.subn(re.escape(START) + r".*?" + re.escape(END), lambda _m: block, html, flags=re.DOTALL)
    if n != 1:
        raise SystemExit(f"expected one {START}…{END} pair in push_planner.html, found {n}")
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(new)


LAYA_BUDGET = 80   # model calls per run (~1.2 s each); answers are cached, so repeat runs are faster


def add_laya(rows, top, enabled=True):
    """Laya's second opinion (lib/push_laya) when the model is on this PC; else a reason why not."""
    from lib import laya, push_laya
    if not enabled:
        return {"available": False, "why": "switched off (--no-laya)"}
    t = time.time()
    if not laya.available():
        return {"available": False, "why": laya.why_unavailable()}
    laya.set_budget(LAYA_BUDGET)
    out = push_laya.second_opinion(rows, top, laya.ask_choice, laya.ask_yes_no,
                                   budget_left=lambda: laya.stats["budget_left"])
    laya.save_cache()
    out.update(available=True, modelCalls=laya.stats["asked"], cached=laya.stats["cached"],
               seconds=round(time.time() - t, 1))
    return out


def main(argv):
    dry = "--dry-run" in argv
    t0 = time.time()
    data = load_data()
    if data is None:
        print("push_planner: Odoo unreachable — push_planner.html left unchanged.")
        return 0
    print(f"Push Planner · sales {data['start']} → {data['end']} · month {data['monthStart']} → {data['monthEnd']}")
    for mk in MARKETS:
        st, dl = data["stock"][mk], data["daily"][mk]
        sold = {b: sum(v.values()) for b, v in dl.items()}
        print(f"  {mk:<7} bags with stock {sum(1 for v in st.values() if v > 0):>4} ({sum(st.values()):,} units) · "
              f"bags sold {sum(1 for v in sold.values() if v > 0):>4} ({sum(sold.values()):,} units in {WINDOW_DAYS} d) · "
              f"unmatched {data['unmatched'][mk]:,} units")
    shops = sorted(set(data["shopStock"]) | set(data["shopSales"]))
    print(f"  kenya shops: {len(shops)} — " + ", ".join(
        f"{s} {sum(data['shopStock'].get(s, {}).values())}/{sum(data['shopSales'].get(s, {}).values())}" for s in shops)
        + "  (stock / sold 14 d)")
    print(f"  prices for {len(data['prices'])} bag types · loaded in {time.time() - t0:.1f}s")
    infer, _ = smc.bag_classifier(set())
    pages = load_pages(infer)
    print(f"  pages: posting window '{pages['postingWindow']}' · self-made combos '{pages['smcMonth']}' · "
          f"{len(pages['isNew'])} new products")
    for mk in MARKETS:
        p = pages["posting"][mk]
        print(f"  {mk:<7} posting rows for {len(p):>3} bags · posted this month {sum(1 for x in p.values() if x['postsMonth']):>3} · "
              f"posted last week {sum(1 for x in p.values() if x['postsLastWeek']):>3} · on offer {len(pages['onOffer'][mk]):>3}")
    rows = build_facts(data, pages)
    print(f"  facts: {len(rows)} bag × market rows · with category {sum(1 for r in rows if r['category'])} · "
          f"with selling peers {sum(1 for r in rows if r['peerCount'])}")
    rows, mv, top, top_by = build_actions(rows, data)
    from collections import Counter
    print("  actions:", dict(Counter(r["action"] for r in rows)), f"· {len(mv)} shop moves")
    print("  TOP 15 this week:")
    for i, r in enumerate(top, 1):
        print(f"   {i:>2}. [{r['action']:<12}] {r['bag']:<18} {r['market']:<6} score {r['score']:>9,}  {r['says']}")
    stuck = build_reasons(rows, data)
    from collections import Counter as _C
    for mk in MARKETS:
        st = [r for r in stuck if r["market"] == mk]
        print(f"  NOT MOVING {mk}: {len(st)} bags · reasons " + str(dict(_C(x['code'] for r in st for x in r['reasons']))))
    for mk, n in (("kenya", 5), ("sinza", 3), ("uganda", 2)):
        for r in [r for r in stuck if r["market"] == mk][:n]:
            print(f"    {mk:<6} {r['bag']:<16} stock {r['stock']:>4} · {r['perDay']:g}/day · " +
                  " | ".join(x["text"] for x in r["reasons"]) if r["reasons"] else f"    {mk:<6} {r['bag']:<16} (no reason found)")
    lay = add_laya(rows, top, enabled="--no-laya" not in argv)
    if lay.get("available"):
        from collections import Counter as _C2
        offv = _C2(r["laya"]["offer"]["verdict"] for r in rows if (r.get("laya") or {}).get("offer"))
        resv = _C2(r["laya"]["reason"]["verdict"] for r in rows if (r.get("laya") or {}).get("reason"))
        print(f"  LAYA: {lay['asked']} bags checked · {lay['modelCalls']} model calls + {lay['cached']} cached · "
              f"{lay['seconds']}s · baselines offer {lay['offerBaseline']} / reason {lay['reasonBaseline']}")
        print(f"        offer verdicts {dict(offv)} · main-reason verdicts {dict(resv)}")
        if lay.get("offerNote"):
            print(f"        {lay['offerNote']}")
        for r in [r for r in rows if (r.get("laya") or {}).get("reason")][:4]:
            m = r["laya"]["reason"]
            print(f"        {r['market']:<6} {r['bag']:<14} rules: {', '.join(x['code'] for x in r['reasons'])} → Laya: {m['code']} ({m['confidence']:.0%}, {m['verdict']})")
    else:
        print(f"  LAYA: not used — {lay.get('why')}")
    for mk in ("sinza", "uganda"):
        print(f"  TOP for {mk}:")
        for i, r in enumerate(top_by[mk], 1):
            print(f"   {i:>2}. [{r['action']:<12}] {r['bag']:<18} score {r['score']:>8,}  {r['says']}")
    wkly = weekly(top, data, write=not dry)
    print(f"  WEEKLY: this week {wkly['thisWeek']} · weeks stored {wkly['weeksStored']} · "
          f"last week's calls: {wkly['week'] or 'none yet'} ({len(wkly['rows'])})" + ("" if not dry else " · dry run: not saved"))
    if dry:
        return 0
    pp = payload(data, pages, rows, mv, top, top_by, stuck, lay, wkly)
    inject(pp)
    print(f"push_planner.html updated · {len(pp['top'])} top actions · "
          f"{sum(pp['notMovingCount'].values())} not-moving bags · {time.time() - t0:.0f}s")
    if os.environ.get("DENRI_LAUNCHER") != "1":
        import webbrowser
        webbrowser.open("file://" + HTML_FILE)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
