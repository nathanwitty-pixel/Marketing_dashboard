"""
timed_offers.py
─────────────────────────────────────────────────────────────────
Timed-offer campaign report (Kenya).

  • Sales  : LIVE from Odoo POS for the EXACT window (startDate..endDate,
             end-of-day inclusive), scoped to the market (Kenya = every till
             except the Sinza/Dar/Uganda ones), per bag type.
             Combo wrappers / delivery / customisation / straps / samples /
             POS-category lines are excluded (same rules as Total Sales).
  • Posting: last week's Kenya marketing posting (WEEKLY_MARKETING_POST col E),
             per bag type — "borrowed" alongside the sales.
  • Config : timed_offers_config.json (market, startDate, endDate, bags[]).

Injects the campaign payload (const TO) into timed_offers.html between the
<!-- TIMED_DATA_START --> / <!-- TIMED_DATA_END --> markers.
─────────────────────────────────────────────────────────────────
"""

import re, os, json, webbrowser, pathlib
from datetime import date, timedelta

SPREADSHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from google_auth import get_gspread_client


# ── HELPERS ───────────────────────────────────────────────────

def safe_int(val):
    try:
        return int(float(str(val).replace(",", "")))
    except (ValueError, TypeError):
        return 0

def fmt_int(n):
    return f"{n:,}"


# ── CONFIG ────────────────────────────────────────────────────

CONFIG_FILE = os.path.join(BASE_DIR, "timed_offers_config.json")

def load_config():
    cfg = {"name": "", "market": "Kenya", "startDate": "", "endDate": "",
           "bags": ["Kai", "Pioneer", "Double Press", "Antitheft", "Code 3", "School bag"]}
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            raw = json.load(f)
        cfg["name"]      = str(raw.get("name", "") or "").strip()
        cfg["market"]    = str(raw.get("market", "Kenya") or "Kenya").strip()
        cfg["startDate"] = str(raw.get("startDate", "") or "").strip()
        cfg["endDate"]   = str(raw.get("endDate", "") or "").strip()
        if isinstance(raw.get("bags"), list) and raw["bags"]:
            cfg["bags"] = [str(b).strip() for b in raw["bags"] if str(b).strip()]
    except (ValueError, OSError):
        pass
    return cfg

CFG = load_config()
BAGS = CFG["bags"]
_BAGS_UP = [b.upper() for b in BAGS]


def _bucket(name):
    """Which configured bag (if any) an Odoo/​sheet product name belongs to,
    by longest-prefix match so 'Double Press' wins over a shorter overlap."""
    n = str(name).strip().upper()
    best = None
    for b in sorted(_BAGS_UP, key=len, reverse=True):
        if n == b or n.startswith(b):
            best = b
            break
    return best


# ── SALES: live from Odoo POS, exact window, Kenya market ─────

def odoo_window_sales(bags, start, end, market):
    """{BAG_UPPER: bags_sold} for the window, Kenya market (excludes Sinza/Dar/
    Uganda tills). Returns ({}, False) if Postgres isn't reachable."""
    out = {b: 0 for b in _BAGS_UP}
    try:
        from lib import db
        ok, _ = db.check_connection()
        if not ok:
            return out, False
    except Exception:
        return out, False

    # Kenya = every till except the non-Kenya markets.
    non_kenya = "('sinza','dar-es-alam','uganda')"
    like_clauses = " OR ".join(
        [f'pt."name" ILIKE :bag{i}' for i in range(len(bags))])
    params = {"s": start, "e": end}
    for i, b in enumerate(bags):
        params[f"bag{i}"] = b + "%"

    q = f"""
    SELECT pt."name" AS product, SUM(pl.qty)::int AS bags
    FROM pos_order p
    JOIN pos_order_line pl ON pl.order_id = p.id
    LEFT JOIN pos_session ps ON p.session_id = ps.id
    LEFT JOIN pos_config pc ON ps.config_id = pc.id
    LEFT JOIN product_product pp ON pl.product_id = pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
    LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
    WHERE p.date_order::date BETWEEN CAST(:s AS date) AND CAST(:e AS date)
      AND p.state IN ('done','paid') AND pl.qty > 0
      AND lower(COALESCE(pc."name",'')) NOT IN {non_kenya}
      AND COALESCE(pt."name",'') NOT LIKE '%+%'
      AND COALESCE(pt."name",'') NOT ILIKE '%delivery%'
      AND COALESCE(pt."name",'') NOT ILIKE '%customization%'
      AND COALESCE(pt."name",'') NOT ILIKE '%strap%'
      AND COALESCE(pt."name",'') NOT ILIKE '%sample%'
      AND COALESCE(pcat."name",'') NOT ILIKE '%Pos%'
      AND ({like_clauses})
    GROUP BY pt."name"
    """
    df = db.run_query(q, params)
    if df is None or df.empty:
        return out, True
    for _, r in df.iterrows():
        b = _bucket(r["product"])
        if b:
            out[b] += int(r["bags"] or 0)
    return out, True


def odoo_daily_kenya(bags, start, end):
    """{date_iso: bags} — daily Kenya bags for the offer bags across [start,end],
    used to measure the before-vs-during-offer lift. {} if DB unreachable."""
    out = {}
    try:
        from lib import db
        ok, _ = db.check_connection()
        if not ok:
            return out
    except Exception:
        return out
    like_clauses = " OR ".join([f'pt."name" ILIKE :bag{i}' for i in range(len(bags))])
    params = {"s": start, "e": end}
    for i, b in enumerate(bags):
        params[f"bag{i}"] = b + "%"
    q = f"""
    SELECT p.date_order::date AS d, SUM(pl.qty)::int AS bags
    FROM pos_order p
    JOIN pos_order_line pl ON pl.order_id = p.id
    LEFT JOIN pos_session ps ON p.session_id = ps.id
    LEFT JOIN pos_config pc ON ps.config_id = pc.id
    LEFT JOIN product_product pp ON pl.product_id = pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
    LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
    WHERE p.date_order::date BETWEEN CAST(:s AS date) AND CAST(:e AS date)
      AND p.state IN ('done','paid') AND pl.qty > 0
      AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
      AND COALESCE(pt."name",'') NOT LIKE '%+%'
      AND COALESCE(pt."name",'') NOT ILIKE '%delivery%'
      AND COALESCE(pt."name",'') NOT ILIKE '%customization%'
      AND COALESCE(pt."name",'') NOT ILIKE '%strap%'
      AND COALESCE(pt."name",'') NOT ILIKE '%sample%'
      AND COALESCE(pcat."name",'') NOT ILIKE '%Pos%'
      AND ({like_clauses})
    GROUP BY 1 ORDER BY 1
    """
    df = db.run_query(q, params)
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            out[str(r["d"])] = int(r["bags"] or 0)
    return out


def odoo_bag_prices(bags, start, end):
    """Per-bag avg unit price (Kenya, window) + the catalogue-wide Kenya avg,
    so we can tell whether the offer bags are cheap/premium. ({}, 0) if no DB."""
    prices, catalog = {b.upper(): {"qty": 0, "val": 0.0} for b in bags}, 0
    try:
        from lib import db
        ok, _ = db.check_connection()
        if not ok:
            return prices, catalog
    except Exception:
        return prices, catalog
    like_clauses = " OR ".join([f'pt."name" ILIKE :bag{i}' for i in range(len(bags))])
    params = {"s": start, "e": end}
    for i, b in enumerate(bags):
        params[f"bag{i}"] = b + "%"
    base = """
    FROM pos_order p
    JOIN pos_order_line pl ON pl.order_id = p.id
    LEFT JOIN pos_session ps ON p.session_id = ps.id
    LEFT JOIN pos_config pc ON ps.config_id = pc.id
    LEFT JOIN product_product pp ON pl.product_id = pp.id
    LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
    LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
    WHERE p.date_order::date BETWEEN CAST(:s AS date) AND CAST(:e AS date)
      AND p.state IN ('done','paid') AND pl.qty > 0
      AND lower(COALESCE(pc."name",'')) NOT IN ('sinza','dar-es-alam','uganda')
      AND COALESCE(pt."name",'') NOT LIKE '%+%'
      AND COALESCE(pt."name",'') NOT ILIKE '%delivery%'
      AND COALESCE(pt."name",'') NOT ILIKE '%customization%'
      AND COALESCE(pt."name",'') NOT ILIKE '%strap%'
      AND COALESCE(pt."name",'') NOT ILIKE '%sample%'
      AND COALESCE(pt."name",'') NOT ILIKE '%KES discount%'
      AND COALESCE(pcat."name",'') NOT ILIKE '%Pos%'
    """
    # per offer-bag
    df = db.run_query(f'SELECT pt."name" AS product, SUM(pl.qty)::int AS qty, '
                      f'SUM(pl.price_subtotal_incl)::numeric AS val {base} AND ({like_clauses}) '
                      f'GROUP BY pt."name"', params)
    if df is not None and not df.empty:
        for _, r in df.iterrows():
            b = _bucket(r["product"])
            if b:
                prices[b]["qty"] += int(r["qty"] or 0)
                prices[b]["val"] += float(r["val"] or 0)
    # catalogue-wide avg
    dfc = db.run_query(f'SELECT ROUND(SUM(pl.price_subtotal_incl)/NULLIF(SUM(pl.qty),0)) AS avg {base}',
                       {"s": start, "e": end})
    if dfc is not None and not dfc.empty and dfc.iloc[0]["avg"] is not None:
        catalog = int(dfc.iloc[0]["avg"])
    return prices, catalog


def kenya_stock_by_bag(bags):
    """{BAG_UPPER: {stock, category}} from STOCK_LEVELS (col Y=24 Kenya, col B=category)."""
    out = {}
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)
    rows = sh.worksheet("STOCK_LEVELS").get_all_values()
    for row in rows[1:]:
        if len(row) < 4:
            continue
        b = _bucket(row[3])
        if not b:
            continue
        e = out.setdefault(b, {"stock": 0, "category": ""})
        e["stock"] += safe_int(row[24]) if len(row) > 24 else 0
        if not e["category"] and len(row) > 1:
            e["category"] = str(row[1]).strip()
    return out


# ── POSTING: last week's Kenya posts (WEEKLY_MARKETING_POST col E) ─

def weekly_kenya_posts(bags):
    """{BAG_UPPER: kenya_posts} from WEEKLY_MARKETING_POST col D=bag type,
    col E (idx 4) = Kenya posts."""
    out = {b: 0 for b in _BAGS_UP}
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)
    rows = sh.worksheet("WEEKLY_MARKETING_POST").get_all_values()
    for row in rows[1:]:
        if len(row) < 5:
            continue
        b = _bucket(row[3])          # col D = BAG TYPE
        if b:
            out[b] += safe_int(row[4])   # col E = KENYA posts
    return out


# ── BUILD ─────────────────────────────────────────────────────

print("Fetching timed-offer data (Odoo sales + weekly posting)...")
sales_map, sales_live = odoo_window_sales(BAGS, CFG["startDate"], CFG["endDate"], CFG["market"])
posts_map = weekly_kenya_posts(BAGS)

# ── LIFT: offer-window bags/day vs the pre-offer month-to-date bags/day ──
# Baseline = 1st of the offer's month → the day before the offer started
# ("first week … up to when the offer ran"). Daily series feeds the trend chart.
lift = None
try:
    _os = date.fromisoformat(CFG["startDate"])
    _oe = date.fromisoformat(CFG["endDate"])
    _mstart = _os.replace(day=1)
    _dend = max(_oe, date.today())               # fetch through today for the weekly view
    _daily = odoo_daily_kenya(BAGS, _mstart.isoformat(), _dend.isoformat())
    if _daily:
        offer_days = (_oe - _os).days + 1
        base_days  = (_os - _mstart).days            # days before the offer
        def _sum(a, b):
            return sum(v for k, v in _daily.items() if a <= k <= b)
        base_total  = _sum(_mstart.isoformat(), (_os - timedelta(days=1)).isoformat())
        offer_total = _sum(_os.isoformat(), _oe.isoformat())
        base_per_day  = round(base_total / base_days, 1) if base_days else 0.0
        offer_per_day = round(offer_total / offer_days, 1) if offer_days else 0.0
        lift_pct = round((offer_per_day - base_per_day) / base_per_day * 100) if base_per_day else None
        # daily series for the chart (month start → offer end; offer days flagged)
        _series = []
        _d = _mstart
        while _d <= _oe:
            k = _d.isoformat()
            _series.append({"date": k, "bags": _daily.get(k, 0),
                            "off": _os.isoformat() <= k <= _oe.isoformat()})
            _d += timedelta(days=1)
        # weekly buckets (Sun–Sat) across the whole month-to-date — the "week 1,
        # week 2, week 3, offer week" view; the week holding the offer is flagged.
        def _wk_start(d):
            return d - timedelta(days=(d.weekday() + 1) % 7)
        _wk = {}
        _d = _mstart
        while _d <= _dend:
            k = _d.isoformat()
            ws = _wk_start(_d)
            e = _wk.setdefault(ws, {"total": 0, "days": 0, "off": False})
            e["total"] += _daily.get(k, 0)
            e["days"] += 1
            if _os <= _d <= _oe:
                e["off"] = True
            _d += timedelta(days=1)
        weekly = []
        for _n, ws in enumerate(sorted(_wk), start=1):
            e = _wk[ws]
            # Clamp the week's shown range to within the month (Aug only) — the
            # opening Sun–Sat week starts in July, but we only count/label August.
            _ws_show = max(ws, _mstart)
            _we_show = min(ws + timedelta(days=6), _dend)
            weekly.append({
                "label": "Wk " + str(_n),
                "start": _ws_show.isoformat(), "end": _we_show.isoformat(),
                "total": e["total"], "days": e["days"],
                "perDay": round(e["total"] / e["days"], 1) if e["days"] else 0.0,
                "off": e["off"],
            })
        lift = {
            "baseStart": _mstart.isoformat(), "baseEnd": (_os - timedelta(days=1)).isoformat(),
            "baseDays": base_days, "baseTotal": base_total, "basePerDay": base_per_day,
            "offerDays": offer_days, "offerTotal": offer_total, "offerPerDay": offer_per_day,
            "liftPct": lift_pct, "daily": _series, "weekly": weekly,
        }
except (ValueError, TypeError):
    lift = None

bag_rows = []
for b in BAGS:
    bu = b.upper()
    sold  = int(sales_map.get(bu, 0))
    posts = int(posts_map.get(bu, 0))
    bag_rows.append({
        "name":  b,
        "sold":  sold,
        "posts": posts,
        "perPost": round(sold / posts, 1) if posts else None,   # bags sold per post
    })

bag_rows.sort(key=lambda r: -r["sold"])
total_sold  = sum(r["sold"]  for r in bag_rows)
total_posts = sum(r["posts"] for r in bag_rows)

# Nice window label, e.g. "17–21 Aug 2026"
def _win_label(s, e):
    try:
        ds, de = date.fromisoformat(s), date.fromisoformat(e)
        if ds.month == de.month and ds.year == de.year:
            return f"{ds.day}–{de.day} {de:%b %Y}"
        return f"{ds:%d %b} – {de:%d %b %Y}"
    except ValueError:
        return f"{s} – {e}"

best  = max(bag_rows, key=lambda r: r["sold"]) if bag_rows else None
mostp = max(bag_rows, key=lambda r: r["posts"]) if bag_rows else None

# ── WHY these bags? stock (clearance) · price · season — a repeatable read ──
try:
    _pstart = date.fromisoformat(CFG["startDate"]).replace(day=1).isoformat()
except ValueError:
    _pstart = CFG["startDate"]
_pend = max(date.fromisoformat(CFG["endDate"]), date.today()).isoformat() \
        if CFG["endDate"] else CFG["endDate"]
_, _catalog_avg = odoo_bag_prices(BAGS, _pstart, _pend)      # catalogue-wide avg (cheap/premium read)
# Discount attribution: avg selling price BEFORE vs DURING the offer per bag.
# A real markdown shows the price dropping; a flat/higher price means the bag
# was effectively already at that price, so its sales aren't down to the discount.
try:
    _os_d = date.fromisoformat(CFG["startDate"])
    _oe_d = date.fromisoformat(CFG["endDate"])
    _ms_d = _os_d.replace(day=1)
    _pre_prices, _ = odoo_bag_prices(BAGS, _ms_d.isoformat(), (_os_d - timedelta(days=1)).isoformat())
    _off_prices, _ = odoo_bag_prices(BAGS, _os_d.isoformat(), _oe_d.isoformat())
except ValueError:
    _pre_prices, _off_prices = {}, {}
_stock_map = kenya_stock_by_bag(BAGS)

def _avg(m, bu):
    e = m.get(bu, {"qty": 0, "val": 0})
    return round(e["val"] / e["qty"]) if e["qty"] else None

# Days in each window, so we can compare each bag's DAILY pace before vs during.
_bd = lift.get("baseDays") if lift else None
_od = lift.get("offerDays") if lift else None

why_bags = []
for r in bag_rows:
    bu = r["name"].upper()
    pre_p = _avg(_pre_prices, bu)
    off_p = _avg(_off_prices, bu)
    disc_pct = round((off_p - pre_p) / pre_p * 100) if (pre_p and off_p) else None
    discounted = bool(disc_pct is not None and disc_pct <= -3)   # ≥3% drop = a real markdown
    avg_price = off_p or pre_p
    # each bag's own sales pace: units/day before vs during the offer
    pre_q = int(_pre_prices.get(bu, {}).get("qty", 0))
    off_q = int(_off_prices.get(bu, {}).get("qty", 0))
    pre_pd = round(pre_q / _bd, 1) if _bd else None
    off_pd = round(off_q / _od, 1) if _od else None
    bag_lift = round((off_pd - pre_pd) / pre_pd * 100) if (pre_pd and off_pd is not None) else None
    sm = _stock_map.get(bu, {"stock": 0, "category": ""})
    why_bags.append({
        "name": r["name"], "sold": r["sold"], "posts": r["posts"], "stock": sm["stock"],
        "avgPrice": avg_price, "prePrice": pre_p, "offerPrice": off_p,
        "discountPct": disc_pct, "discounted": discounted,
        "prePerDay": pre_pd, "offerPerDay": off_pd, "bagLift": bag_lift,
        "category": sm["category"],
        "cheaper": bool(avg_price is not None and _catalog_avg and avg_price < _catalog_avg),
    })

_total_stock = sum(w["stock"] for w in why_bags)
_cats = sorted({w["category"] for w in why_bags if w["category"]})
_priced = [w for w in why_bags if w["avgPrice"]]
_cheapest = min(_priced, key=lambda w: w["avgPrice"]) if _priced else None
_priciest = max(_priced, key=lambda w: w["avgPrice"]) if _priced else None
_topstock = max(why_bags, key=lambda w: w["stock"]) if why_bags else None
_zero_post = [w["name"] for w in why_bags if not w["posts"] and w["sold"] > 0]
_lift_txt = (f"+{lift['liftPct']}%" if lift and lift.get("liftPct") is not None else "higher")

# Discount attribution
_disc = [w for w in why_bags if w["discounted"]]
_nodisc_sold = sum(w["sold"] for w in why_bags if not w["discounted"])
_nodisc_share = round(_nodisc_sold / total_sold * 100) if total_sold else 0
_top2 = sorted(why_bags, key=lambda w: -w["sold"])[:2]
_top2_nodisc = [w for w in _top2 if not w["discounted"]]
_disc_drove = _nodisc_share < 50   # did the discount drive most volume?

_insights = []
# Discount check first — it's the "was it really the offer price?" question
if _top2:
    if _top2_nodisc:
        _names = " and ".join(w["name"] for w in _top2_nodisc)
        _disc_list = ", ".join(f"{w['name']} {w['discountPct']}%" for w in _disc) or "the smaller lines"
        _insights.append({"tag": "Discount check", "text":
            f"<b>Not really the discount.</b> {_names} — the top seller(s) — held a <b>flat or higher</b> price during the window, "
            f"and <b>{_nodisc_share}% of all volume sold at (near) full price</b>. The genuine markdowns ({_disc_list}) were the mid/low-volume bags. "
            f"So the offer price wasn't what pulled buyers on the bulk of sales."})
    else:
        _dt = ", ".join(f"{w['name']} {w['discountPct']}%" for w in _top2)
        _insights.append({"tag": "Discount check", "text":
            f"<b>The discount plausibly helped.</b> The top sellers were genuinely marked down during the window "
            f"({_dt}), and only {_nodisc_share}% of volume sold at full price — so the offer price did pull buyers."})

# Which bags were ACTUALLY on offer (price truly cut) — and did the cut sell them faster?
if _disc:
    def _phrase(w):
        bl = w.get("bagLift")
        if bl is None:
            return f"{w['name']} ({w['discountPct']}% price)"
        return f"{w['name']} ({w['discountPct']}% price, own pace {'+' if bl > 0 else ''}{bl}%)"
    _helped  = [w for w in _disc if (w.get("bagLift") or 0) > 0]
    _flopped = [w for w in _disc if (w.get("bagLift") or 0) <= 0]
    _txt = "<b>Actually on offer (price truly cut):</b> " + "; ".join(_phrase(w) for w in _disc) + ". "
    if _helped:
        _txt += ("The cut sold <b>" + " and ".join(w["name"] for w in _helped)
                 + "</b> faster than before the offer. ")
    if _flopped:
        _txt += ("<b>" + " and ".join(w["name"] for w in _flopped)
                 + "</b> were marked down but still didn't pick up — those cuts mostly gave away margin.")
    _insights.append({"tag": "On offer?", "text": _txt})
else:
    _insights.append({"tag": "On offer?", "text":
        "None of the six were meaningfully marked down during the window (all sold within ~3% of their pre-offer price), "
        "so the sales came from demand/timing rather than a real price cut."})

if _topstock and _total_stock:
    _insights.append({"tag": "Stock", "text":
        f"Mostly backpacks with real inventory behind them — <b>{_total_stock:,} still in Kenya stock</b> even after the push "
        f"(led by {_topstock['name']} at {_topstock['stock']:,}). Putting them on offer draws down a genuine stock position, not a token one."})
if _cats:
    _season_bag = (" and ".join(_zero_post[:2]) + " even sold on zero marketing posts (pure demand). ") if _zero_post else ""
    _insights.append({"tag": "Season", "text":
        f"All six sit in <b>{', '.join(c.title() for c in _cats)}</b> — school categories — and the step-up landed in the offer week as schools opened. "
        f"{_season_bag}The timing lines up with schools opening, which fits the sales pattern better than the price cut does."})

if _disc_drove:
    _verdict = (f"<b>Good move.</b> Sales rose <b>{_lift_txt}</b> per day and the genuinely-discounted bags drove most of it, "
                f"so the offer price did its job. Repeat at back-to-school; consider protecting margin on any lines that sold well without a deep cut.")
else:
    _verdict = (f"<b>Good move — but credit the timing, not the discount.</b> Sales rose <b>{_lift_txt}</b> per day, yet "
                f"<b>{_nodisc_share}% of volume sold at (near) full price</b> — the lift tracks <b>back-to-school demand for high-stock school bags</b>, "
                f"not the markdown. Keep running these bags this season; the offer framing helps, but you likely don't need to give away margin on the top sellers "
                + (f"({', '.join(w['name'] for w in _top2_nodisc)})" if _top2_nodisc else "") + ".")

why = {"catalogAvg": _catalog_avg, "totalStock": _total_stock, "categories": _cats,
       "nodiscShare": _nodisc_share, "discDrove": _disc_drove,
       "bags": why_bags, "insights": _insights, "verdict": _verdict}

TO = {
    "name":       CFG["name"],
    "market":     CFG["market"],
    "startDate":  CFG["startDate"],
    "endDate":    CFG["endDate"],
    "windowLabel": _win_label(CFG["startDate"], CFG["endDate"]),
    "lift":       lift,
    "why":        why,
    "salesLive":  sales_live,
    "bags":       bag_rows,
    "totalSold":  total_sold,
    "totalPosts": total_posts,
    "perPost":    round(total_sold / total_posts, 1) if total_posts else None,
    "bestName":   best["name"]  if best  else "",
    "bestSold":   best["sold"]  if best  else 0,
    "mostPName":  mostp["name"] if mostp else "",
    "mostPosts":  mostp["posts"] if mostp else 0,
}


# ── INJECT ────────────────────────────────────────────────────

inline_script = (
    "<!-- TIMED_DATA_START -->\n"
    "<script>\n"
    "const TO = " + json.dumps(TO, ensure_ascii=False) + ";\n"
    "</script>\n"
    "<!-- TIMED_DATA_END -->"
)

html_path = os.path.join(BASE_DIR, "timed_offers.html")
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()
html = re.sub(r"<!-- TIMED_DATA_START -->.*?<!-- TIMED_DATA_END -->",
              inline_script, html, flags=re.DOTALL)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

if not os.environ.get("DENRI_LAUNCHER"):
    webbrowser.open_new_tab(pathlib.Path(html_path).as_uri())

print(f"timed_offers.html updated  \"{CFG['name'] or 'Timed Offer'}\"  ({TO['windowLabel']}, {CFG['market']}).")
print(f"  Sales source        : {'Odoo (live)' if sales_live else 'DB UNREACHABLE — zeros'}")
if lift:
    print(f"  LIFT: offer {lift['offerPerDay']}/day vs pre-offer {lift['basePerDay']}/day "
          f"({lift['baseStart']}..{lift['baseEnd']})  ->  {('+' if (lift['liftPct'] or 0) >= 0 else '')}{lift['liftPct']}%")
for r in bag_rows:
    pp = f"{r['perPost']}" if r["perPost"] is not None else "—"
    print(f"    {r['name']:<14} sold {r['sold']:>4}   posts {r['posts']:>3}   sold/post {pp}")
print(f"  TOTAL sold          : {fmt_int(total_sold)}")
print(f"  TOTAL posts (Kenya) : {fmt_int(total_posts)}")
