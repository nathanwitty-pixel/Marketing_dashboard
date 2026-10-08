"""
bags_on_offer.py
─────────────────────────────────────────────────────────────────
Bags on offer vs bags not on offer vs others — Kenya, for three periods
(Monthly = live month to date, Weekly = current Sun–Sat week, Last week = previous
complete Sun–Sat week).

On offer     = combo products (running + self-made, name "A + B") and single sales of any
               bag that is a running-combo component, a Deal of the Week or a Power Deal.
Not on offer = every other catalogue bag sold, plus the month's new products (MONTHLY_TARGET
               col I) that are on no offer — even ones not in the price catalogue yet.
Others       = gift bags (POS) and corporate sales (customer invoices).

The on-offer bag set comes from self_made_combos.py (bags_offer_source.json), and bags are
resolved with the same self_made_combos.bag_classifier(), so the Monthly not-on-offer money
matches Menu 4's "Bags not on offer" panel (plus new products it can't resolve). Per shop,
till revenue is compared with its Odoo target (sales_pos_target, month or week) and ranked
within its region (docs/shop-regions.md); a shop behind its pro-rated target AND below its
region's pace (Kenya-wide pace for a one-shop region) is flagged red.

Spec: docs/bags-on-offer.md. Injects `BOO` into bags_on_offer.html between the
BOO_DATA markers.
─────────────────────────────────────────────────────────────────
"""

import os, re, sys, json, time, datetime, webbrowser, pathlib

from lib import db, report_month, oos_callbacks, colours, shop_birthdays
import self_made_combos as smc
import timed_offers as tof
import offer_picking as opk
import reject_sales as rsl

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "bags_on_offer.html")
SOURCE_JSON = os.path.join(BASE, "bags_offer_source.json")
TIERS_CSV = os.path.join(BASE, "bag_tiers.csv")
NEW_PRODUCTS_SHEET = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"   # same sheet as new_products.py

_KENYA_TILLS = "AND lower(COALESCE(pc.\"name\",'')) NOT IN ('sinza','dar-es-alam','uganda')"

# Every Kenya POS line by shop × product × day — same product filters as
# self_made_combos._bag_sales_sql, except combo products ("A + B") and gift bags are KEPT
# (combos are on offer; gift bags go to Others). Combo SUB-lines (the bags inside a combo,
# KES 0) are excluded — they're counted as combo prints, not single sales.
LINES_SQL = f"""
SELECT UPPER(COALESCE(pc."name",'?')) AS shop, UPPER(pt."name") AS name, p.date_order::date AS d,
       SUM(pl.qty)::int AS units, ROUND(SUM(pl.price_subtotal_incl))::int AS revenue
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
LEFT JOIN product_product pp ON pl.product_id=pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0 AND NOT COALESCE(pl.sub_product_line, false)
  {_KENYA_TILLS}
  AND pt."name" NOT ILIKE '%delivery%' AND pt."name" NOT ILIKE '%customi%'
  AND pt."name" NOT ILIKE '%strap%'
GROUP BY 1, 2, 3
"""

# Total till revenue per shop per day (every line) — what the Odoo target is set against.
TILL_SQL = f"""
SELECT UPPER(COALESCE(pc."name",'?')) AS shop, p.date_order::date AS d,
       ROUND(SUM(pl.price_subtotal_incl))::bigint AS revenue
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done', 'invoiced', 'paid')
  {_KENYA_TILLS}
GROUP BY 1, 2
"""

# Corporate sales per day — customer invoices, same qualifying rule as sql/corporate_bags.sql
# (posted out_invoice; paid / in payment, or at most 25% still outstanding).
CORPORATE_SQL = """
WITH qinv AS (
    SELECT am.id, am.invoice_date
    FROM account_move am
    WHERE am.move_type = 'out_invoice' AND am.state = 'posted'
      AND am.invoice_date BETWEEN :s AND :e
      AND ( am.payment_state IN ('paid', 'in_payment')
            OR (am.amount_total > 0 AND am.amount_residual / am.amount_total <= 0.25) )
)
SELECT qinv.invoice_date AS d, COALESCE(SUM(aml.quantity), 0)::int AS units,
       ROUND(COALESCE(SUM(aml.price_total), 0))::bigint AS revenue
FROM account_move_line aml JOIN qinv ON qinv.id = aml.move_id
WHERE aml.display_type IS NULL AND aml.product_id IS NOT NULL
GROUP BY 1
"""

# Odoo revenue targets (per till, plus the corporate row) overlapping the date range.
TARGET_SQL = """
SELECT COALESCE(UPPER(pc."name"), 'CORPORATE') AS shop, t.target_scope AS scope, t.period,
       t.start_date, t.end_date, t.target_amount::float AS target, t.write_date
FROM sales_pos_target t LEFT JOIN pos_config pc ON pc.id = t.config_id
WHERE t.period IN ('month', 'week') AND t.target_scope IN ('pos', 'corporate')
  AND t.start_date <= :e AND t.end_date >= :s
"""

# Bags printed inside combos, per day: Odoo's combo SUB-lines — one line per bag inside every
# combo, with the exact colour variant (Sep: 2,053 bags = every slot of all 946 combo orders).
COMBO_SUBLINES_SQL = f"""
SELECT p.date_order::date AS d, UPPER(pt."name") AS name, SUM(pl.qty)::int AS units
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
LEFT JOIN product_product pp ON pl.product_id=pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0
  AND COALESCE(pl.sub_product_line, false)
  {_KENYA_TILLS}
GROUP BY 1, 2
"""

# Combo RETURNS carry no sub-lines, so their bags come from the combo line's
# combo_product_attribute_values (the bag + colour chosen).
COMBO_PRINTS_SQL = f"""
SELECT p.date_order::date AS d, UPPER(pt."name") AS name, SUM(pl.qty)::int AS units,
       COALESCE(pl.combo_product_attribute_values, '') AS attrs
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
LEFT JOIN product_product pp ON pl.product_id=pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done', 'invoiced', 'paid') AND pl.qty < 0
  {_KENYA_TILLS}
  AND pt."name" LIKE '%+%' AND pt."name" NOT ILIKE '%delivery%' AND pt."name" NOT ILIKE '%customi%'
  AND NOT EXISTS (SELECT 1 FROM pos_order_line sl WHERE sl.order_id = p.id AND COALESCE(sl.sub_product_line, false))
GROUP BY 1, 2, 4
"""

# Single-bag lines inside a timed-offer campaign (timed_offers_config.json), one row per till
# line so overlapping campaigns can't count a sale twice. The campaign's own shop / hour /
# price / name filters (from timed_offers.py) are appended per offer.
TIMED_SQL = f"""
SELECT pl.id AS line_id, UPPER(COALESCE(pc."name",'?')) AS shop, UPPER(pt."name") AS name,
       p.date_order::date AS d, pl.qty::int AS units, ROUND(pl.price_subtotal_incl)::int AS revenue
FROM pos_order p JOIN pos_order_line pl ON pl.order_id=p.id
LEFT JOIN pos_session ps ON p.session_id=ps.id
LEFT JOIN pos_config pc ON ps.config_id=pc.id
LEFT JOIN product_product pp ON pl.product_id=pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id=pt.id
WHERE p.date_order::date BETWEEN :s AND :e AND p.state IN ('done', 'invoiced', 'paid') AND pl.qty <> 0 AND NOT COALESCE(pl.sub_product_line, false)
  {_KENYA_TILLS}
  AND pt."name" NOT LIKE '%+%'
"""

# Counted by how it was sold: a combo-button sale is a Combo sale; a SINGLE sale of a bag on
# several offers goes to the first of these — a timed-offer campaign is how the sale was
# actually priced; a Power Deal runs at every shop all month, so it wins over a Deal of the
# Week; a combo bag sold singly is the fallback.
# On offer (8 Oct 2026) = combo sales + Power Deal + Deal of the Week. A combo bag bought on its own and a
# timed-offer sale are NOT on offer (full-price single / a short sales boost) — docs/bags-on-offer.md.
_SOURCE_ORDER = ["Power Deal", "Deal of the Week"]
_TAG_ORDER = ["Timed offer", "Power Deal", "Deal of the Week", "Combo component"]   # which offers a bag is in
_NON_KENYA = ("SINZA", "DAR-ES-ALAM", "UGANDA", "?")

# Non-offer POS sales counted under "Others" (with corporate invoices): name prefix → group.
# (Laptop sleeves are bags since 27 Sep 2026 — see base(): any "…LAPTOP SLEEVE…" → the LAPTOP SLEEVE bag.)
_OTHER_GROUPS = (("GIFT BAG", "Gift bags"), ("SAMPLE", "Samples"))


# ── Offer type summary (matrix) ──
# Rows, in display order. Every sale lands in exactly one (see docs/bags-on-offer.md).
OFFER_ROWS = [("OFF", "Not on offer"), ("POWER", "Power deals"), ("COMBOS", "Combos (button)"),
              ("DOW", "Deal of wk"), ("MID", "Samples"), ("GIFT", "Gift bag"),
              ("CORP", "Corporate")]
# Combo bags sold singly are bags bought on their own, not combos — their own row (Oct 2026).
_ROW_OF_SOURCE = {"Combo sale": "COMBOS", "Power Deal": "POWER", "Deal of the Week": "DOW"}
_ROW_OF_OTHER = {"Gift bags": "GIFT", "Samples": "MID"}
# The 18 bag categories (offer sheet, bag_names tab) — "Top 5" + "Other 13".
CATEGORIES = ["BABY BAG", "BACKPACK", "BRIEFCASE", "CHEST BAG", "GIFT BAG", "HANDBAG", "HOOD",
              "LUNCH BAG", "MAKE UP", "MAN BAG", "MESSENGER", "SCHOOL BAG", "SLING", "SPORT",
              "THIGH BAG", "TRAVEL", "WAIST BAG", "WASHBAG"]
TIERS = ["Premium", "Core", "Entry"]


def _price_tier(price):
    """Tier of a bag from its price (KES): <= 2,000 Entry, 2,001-3,000 Core, > 3,000 Premium."""
    return "Entry" if price <= 2000 else ("Core" if price <= 3000 else "Premium")


def _bag_tiers():
    """{BAG: (category, tier)} from bag_tiers.csv (editable; '#' lines are comments). The tier
    follows PRICE when it is set, else the TIER column."""
    out = {}
    try:
        with open(TIERS_CSV, encoding="utf-8") as f:
            rows = [ln for ln in f if ln.strip() and not ln.lstrip().startswith("#")]
        import csv
        for r in csv.DictReader(rows):
            bag = str(r.get("BAG") or "").strip().upper()
            if not bag:
                continue
            tier = str(r.get("TIER") or "").strip().capitalize()
            try:   # the price decides: <= 2,000 Entry, 2,001-3,000 Core, > 3,000 Premium
                tier = _price_tier(float(str(r.get("PRICE") or "").replace(",", "")))
            except ValueError:
                pass
            out[bag] = (str(r.get("CATEGORY") or "").strip().upper(), tier if tier in TIERS else "")
    except OSError:
        print("  Tiers            : bag_tiers.csv not found — every bag Unassigned")
    return out


def _other_group(name):
    n = re.sub(r"^\[[^\]]*\]\s*", "", str(name)).strip().upper()
    return next((g for pre, g in _OTHER_GROUPS if n.startswith(pre)), None)


def _timed_offers():
    """Kenya timed-offer campaigns from timed_offers_config.json (normalised by timed_offers.py)."""
    try:
        return [o for o in tof.load_config().get("offers", [])
                if (o.get("market") or "Kenya").lower() == "kenya" and o.get("startDate") and o.get("endDate")]
    except Exception as ex:                                  # noqa: BLE001
        print(f"  Timed offers     : config unreadable ({ex}) — none counted")
        return []


def _has_deals(d):
    """True when the on-offer source carries any Power Deal / Deal of the Week — a source
    without them means the deals sheet failed to load, not that there were no deals."""
    tags = {t for v in (d.get("onOffer") or {}).values() for t in (v or [])}
    return bool(d.get("dowRuns")) or bool(tags & {"Power Deal", "Deal of the Week"})


def _load_source(month_label):
    """bags_offer_source.json if written in the last 15 min for this month (and it has its
    deals); else rebuild it live via self_made_combos.fetch() (which also refreshes the file)."""
    try:
        if os.path.exists(SOURCE_JSON) and (time.time() - os.path.getmtime(SOURCE_JSON)) < 900:
            with open(SOURCE_JSON, encoding="utf-8") as f:
                d = json.load(f)
            if d.get("onOffer") and d.get("month") == month_label and _has_deals(d):
                print("  On-offer source  : bags_offer_source.json (fresh, <15 min)")
                return d
    except (OSError, ValueError):
        pass
    print("  On-offer source  : rebuilding live via self_made_combos.fetch() …")
    payload = smc.fetch()
    if payload is None:
        return None
    smc.write_bags_offer_source(payload)
    try:
        with open(SOURCE_JSON, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _archived_source(month_start):
    """bags_offer_source_<YYYY-MM>.json — that month's archived on-offer list, or None."""
    fp = os.path.join(BASE, f"bags_offer_source_{month_start:%Y-%m}.json")
    try:
        with open(fp, encoding="utf-8") as f:
            d = json.load(f)
        return d if d.get("onOffer") else None
    except (OSError, ValueError):
        return None


def _previous_payload():
    try:
        with open(HTML, encoding="utf-8") as f:
            m = re.search(r"const BOO = (.*?);\n</script>", f.read(), re.S)
        return json.loads(m.group(1)) if m else None
    except (OSError, ValueError):
        return None


def _new_products():
    """This month's new products: new_products.txt when it lists any (lib/new_products_list),
    else MONTHLY_TARGET col A where col I is ticked. Falls back to the previous build's list
    if the sheet can't be read."""
    from lib import new_products_list
    listed = new_products_list.names()
    if listed:
        print(f"  New products     : {len(listed)} from new_products.txt")
        return listed

    def _ticked(v):
        v = str(v).strip()
        return any(c in v for c in "✅✔✓") or v.upper() in ("TRUE", "1", "YES")
    try:
        from google_auth import get_gspread_client
        rows = get_gspread_client().open_by_key(NEW_PRODUCTS_SHEET).worksheet("MONTHLY_TARGET").get_all_values()
        names = [r[0].strip().upper() for r in rows[1:] if len(r) > 8 and r[0].strip() and _ticked(r[8])]
        print(f"  New products     : {len(names)} from MONTHLY_TARGET")
        return names
    except Exception as e:                                   # noqa: BLE001
        prev = (_previous_payload() or {}).get("newProducts") or []
        print(f"  New products     : sheet unreadable ({type(e).__name__}); reusing {len(prev)} from last build")
        return prev


def _shop_label(till):
    return smc._SHOP_TO_LOC.get(till, till.title())


def _region_of(label):
    return smc._SHOP_REGION.get(label.upper(), "Other")


CUSTOM_JSON = os.path.join(BASE, "boo_custom_range.json")
CUSTOM_MAX_DAYS = 366


def _custom_range():
    """(from, to) dates from boo_custom_range.json — the Custom period — or None."""
    try:
        with open(CUSTOM_JSON, encoding="utf-8") as f:
            c = json.load(f)
        a, b = datetime.date.fromisoformat(c["from"]), datetime.date.fromisoformat(c["to"])
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if a > b:
        a, b = b, a
    return (max(a, b - datetime.timedelta(days=CUSTOM_MAX_DAYS - 1)), b)


def save_custom_range(a, b):
    """Write (or with a=None, delete) the Custom period's dates."""
    if a is None:
        try:
            os.remove(CUSTOM_JSON)
        except OSError:
            pass
        return
    with open(CUSTOM_JSON, "w", encoding="utf-8") as f:
        json.dump({"from": a.isoformat(), "to": b.isoformat()}, f)


def _windows(today, m_start, m_end):
    ws = today - datetime.timedelta(days=(today.weekday() + 1) % 7)       # Sunday of this week
    d = datetime.timedelta
    out = _base_windows(today, m_start, m_end, ws, d)
    c = _custom_range()
    if c:
        a, b = c
        days = (b - a).days + 1
        out["custom"] = {"label": f"Custom ({a:%d %b} – {b:%d %b})", "start": a, "end": b,
                         "upto": min(b, today), "period": "custom", "days": days,
                         "trend": "day" if days <= 31 else "week",
                         "anchor": a - d(days=(a.weekday() + 1) % 7)}       # Sunday on/before day 1
    return out


def _base_windows(today, m_start, m_end, ws, d):
    return {
        "monthly":  {"label": "Monthly", "start": m_start, "end": m_end, "upto": min(m_end, today),
                     "period": "month", "days": (m_end - m_start).days + 1, "trend": "week"},
        "weekly":   {"label": "Weekly", "start": ws, "end": ws + d(days=6), "upto": today,
                     "period": "week", "days": 7, "trend": "day"},
        "lastweek": {"label": "Last week", "start": ws - d(days=7), "end": ws - d(days=1),
                     "upto": ws - d(days=1), "period": "week", "days": 7, "trend": "day"},
    }


_MARKETS = (("sinza", "Sinza", "TSh"), ("uganda", "Uganda", "USh"))


def _market_periods(wins, today):
    """Sinza & Uganda on / not on offer per period, from till receipts (docs/bags-on-offer.md › Sinza & Uganda):
    on = every combo + single sales of a listed single; not on = every other single; others = bulk receipts."""
    from lib import receipt_combos as rc
    infer, _ = smc.bag_classifier(set())
    lo = min(w["start"] for w in wins.values())
    hi = min(max(w["end"] for w in wins.values()), today)
    as_date = lambda v: v if isinstance(v, datetime.date) and not isinstance(v, datetime.datetime) else datetime.date.fromisoformat(str(v)[:10])
    blank = lambda: {"units": 0, "revenue": 0}
    out = {}
    for key, label, cur in _MARKETS:
        lines = rc.market_lines(key, lo, hi)
        if lines is None:
            continue
        for ln in lines:
            ln["d"] = as_date(ln["d"])
        cur_offers = rc.load_offers(today.strftime("%B"), key)
        periods = {}
        for pk, w in wins.items():
            s, e = w["start"], w["end"]
            offers = rc.load_offers(s.strftime("%B"), key) or cur_offers
            sp = rc.offer_split([ln for ln in lines if s <= ln["d"] <= e], offers, infer)
            run, sm = sp["combos"]["running"], sp["combos"]["selfMade"]
            on_s = sp["onSingles"]
            on = {"units": run["bags"] + sm["bags"] + sum(v["units"] for v in on_s.values()),
                  "revenue": run["revenue"] + sm["revenue"] + sum(v["revenue"] for v in on_s.values())}
            off = {"units": sum(v["units"] for v in sp["offSingles"].values()),
                   "revenue": sum(v["revenue"] for v in sp["offSingles"].values())}
            oth = {"units": sp["bulk"]["bags"], "revenue": sp["bulk"]["revenue"]}
            periods[pk] = {
                "label": w["label"], "range": f"{s:%d %b} – {e:%d %b %Y}", "from": s.isoformat(), "to": e.isoformat(),
                "totals": {"on": on, "off": off, "oth": oth},
                "sources": [{"label": "Running combos", "units": run["count"], "bags": run["bags"], "revenue": run["revenue"]},
                            {"label": "Self-made combos", "units": sm["count"], "bags": sm["bags"], "revenue": sm["revenue"]},
                            {"label": "Listed singles", "units": sum(v["units"] for v in on_s.values()), "bags": sum(v["units"] for v in on_s.values()),
                             "revenue": sum(v["revenue"] for v in on_s.values())}],
                "onBags": sorted(({"bag": b, **v, "inSelfMade": sp["comboBags"].get(b, 0)} for b, v in on_s.items()),
                                 key=lambda x: (-x["revenue"], x["bag"])),
                "offBags": sorted(({"bag": b, **v, "inSelfMade": sp["comboBags"].get(b, 0)} for b, v in sp["offSingles"].items()),
                                  key=lambda x: (-x["revenue"], x["bag"])),
                "comboBags": sp["comboBags"], "bulk": sp["bulk"],
                "receiptBags": sp["bags"], "receiptRevenue": sp["revenue"],
                "offersListed": bool(offers),
            }
        out[key] = {"label": label, "currency": cur, "fx": smc.FX_PER_KSH.get(cur), "periods": periods}
        m = periods.get("monthly", {})
        if m:
            t = m["totals"]
            print(f"  {label:7} monthly: on {t['on']['units']} bags / {cur} {t['on']['revenue']:,} · "
                  f"not on {t['off']['units']} / {cur} {t['off']['revenue']:,} · bulk {t['oth']['units']}")
    return out


def _pick_target(rows, shop, period, start, end):
    """Latest target row for `shop` with this period that overlaps [start, end]. A custom range
    sums each overlapping month target × the share of that month's days inside the range."""
    if period == "custom":
        months, tot = {}, 0.0
        for r in rows:
            if r["shop"] == shop and r["period"] == "month" and r["start_date"] <= end and r["end_date"] >= start:
                months.setdefault(r["start_date"], []).append(r)
        for ms, lst in months.items():
            r = max(lst, key=lambda x: str(x["write_date"] or ""))
            span = (r["end_date"] - r["start_date"]).days + 1
            inside = (min(end, r["end_date"]) - max(start, r["start_date"])).days + 1
            tot += (r["target"] or 0) * inside / span
        return tot or None
    best = None
    for r in rows:
        if r["shop"] != shop or r["period"] != period:
            continue
        if not (r["start_date"] <= end and r["end_date"] >= start):
            continue
        key = (r["start_date"], str(r["write_date"] or ""))
        if best is None or key > best[0]:
            best = (key, r["target"])
    return best[1] if best and best[1] else None


def _build_period(w, lines, till, corp, target_rows, classify, extra_off, month_anchor, prints, cover, seg_of):
    s, e = w["start"], w["end"]
    elapsed = max(1, min((min(w["upto"], e) - s).days + 1, w["days"]))
    frac = elapsed / w["days"]

    def blank():
        return {"units": 0, "revenue": 0}

    tot = {"on": blank(), "off": blank(), "oth": blank(), "unc": blank()}
    others = {"Gift bags": blank(), "Samples": blank(), "Corporate": blank()}
    trend, by_source, on_bags, off_bags, unc_names, shops = {}, {}, {}, {}, set(), {}
    # Offer type × category and × tier: {row: {"cat": {CAT: [units, rev]}, "tier": {TIER: [units, rev]}}}
    mtx = {k: {"cat": {}, "tier": {}, "tree": {}} for k, _l in OFFER_ROWS}
    by_week = {}                                             # {week no: {row: [units, rev]}} (Monthly only)

    def add_mtx(row, parts, u, rev):
        for cat, tier, bg, wt in parts:
            node = (tier or "Unassigned") + "|" + (cat or "UNASSIGNED") + "|" + (bg or "")
            for dim, key in (("cat", cat or "UNASSIGNED"), ("tier", tier or "Unassigned"), ("tree", node)):
                c = mtx[row][dim].setdefault(key, [0.0, 0.0])
                c[0] += u * wt
                c[1] += rev * wt

    def tkey(d):
        if w["trend"] == "week":
            return (d - month_anchor).days // 7 + 1
        return d

    for r in lines:
        if not (s <= r["d"] <= e):
            continue
        side, bag, srcs, is_new, offers = classify(r["name"], r["shop"], r["d"], r.get("timed"))
        u, rev = r["units"], r["revenue"]
        tot[side]["units"] += u
        tot[side]["revenue"] += rev
        if side != "unc":
            trend.setdefault(tkey(r["d"]), {"on": 0, "off": 0, "oth": 0})[side] += rev
        if side == "on":
            src = by_source.setdefault(srcs[0], blank())
            src["units"] += u
            src["revenue"] += rev
            if srcs[0] != "Combo sale":
                b = on_bags.setdefault(bag, {"bag": bag, "sources": offers, "isNew": is_new,
                                             "bySource": {}, "revBySource": {}, "priceBySource": {}, **blank()})
                b["units"] += u
                b["revenue"] += rev
                b["bySource"][srcs[0]] = b["bySource"].get(srcs[0], 0) + u
                # money per source + the low–high till price (per shop-day line; refunds left out)
                b["revBySource"][srcs[0]] = b["revBySource"].get(srcs[0], 0) + rev
                if u > 0 and rev > 0:
                    p = round(rev / u)
                    lo_hi = b["priceBySource"].setdefault(srcs[0], [p, p])
                    lo_hi[0], lo_hi[1] = min(lo_hi[0], p), max(lo_hi[1], p)
        elif side == "off":
            # "dowElsewhere": a Deal-of-the-Week bag sold at a shop / in a week the deal wasn't running.
            b = off_bags.setdefault(bag, {"isNew": is_new, "dowElsewhere": "Deal of the Week" in offers,
                                          "comboBag": "Combo component" in offers, "timed": False, **blank()})
            b["timed"] = b["timed"] or bool(r.get("timed"))
            b["units"] += u
            b["revenue"] += rev
        elif side == "oth":
            others[srcs[0]]["units"] += u
            others[srcs[0]]["revenue"] += rev
        else:
            unc_names.add(r["name"])
        row = ("OFF" if side == "off" else _ROW_OF_SOURCE.get(srcs[0]) if side == "on"
               else _ROW_OF_OTHER.get(srcs[0]) if side == "oth" else None)
        if row:
            add_mtx(row, seg_of(r["name"], side, bag, srcs), u, rev)
            if w["trend"] == "week":                         # offer type per week of the month
                c = by_week.setdefault(tkey(r["d"]), {}).setdefault(row, [0, 0])
                c[0] += u
                c[1] += rev
        sh = shops.setdefault(r["shop"], {k: blank() for k in ("on", "off", "oth", "unc")})
        sh[side]["units"] += u
        sh[side]["revenue"] += rev

    in_combos = {}
    for r in prints:
        if s <= r["d"] <= e:
            in_combos[r["bag"]] = in_combos.get(r["bag"], 0) + r["units"]

    corp_rev = corp_units = 0
    for r in corp:
        if s <= r["d"] <= e:
            corp_rev += r["revenue"]
            corp_units += r["units"]
            trend.setdefault(tkey(r["d"]), {"on": 0, "off": 0, "oth": 0})["oth"] += r["revenue"]
            if w["trend"] == "week":
                c = by_week.setdefault(tkey(r["d"]), {}).setdefault("CORP", [0, 0])
                c[0] += r["units"]
                c[1] += r["revenue"]
    others["Corporate"] = {"units": corp_units, "revenue": corp_rev}
    add_mtx("CORP", [("", "", "", 1.0)], corp_units, corp_rev)       # invoices carry no bag → Unassigned
    tot["oth"]["units"] += corp_units
    tot["oth"]["revenue"] += corp_rev

    till_rev = {}
    for r in till:
        if s <= r["d"] <= e:
            till_rev[r["shop"]] = till_rev.get(r["shop"], 0) + r["revenue"]

    # ── Per-shop metrics vs the Odoo target ──
    shop_rows = []
    target_tills = {t["shop"] for t in target_rows if t["scope"] == "pos"}
    for tl in sorted(set(shops) | set(till_rev) | target_tills):
        if tl in _NON_KENYA:
            continue
        sh = shops.get(tl, {k: blank() for k in ("on", "off", "oth", "unc")})
        rev = till_rev.get(tl, 0)
        tgt = _pick_target(target_rows, tl, w["period"], s, e)
        if not rev and not tgt:
            continue
        label = _shop_label(tl)
        bag_rev = sh["on"]["revenue"] + sh["off"]["revenue"]
        shop_rows.append({
            "shop": label, "till": tl, "region": _region_of(label),
            "on": sh["on"], "off": sh["off"], "oth": sh["oth"],
            "onShare": round(sh["on"]["revenue"] / bag_rev * 100, 1) if bag_rev > 0 else None,
            "revenue": rev, "target": round(tgt) if tgt else None,
        })
    corp_tgt = _pick_target(target_rows, "CORPORATE", w["period"], s, e)
    if corp_rev or corp_tgt:
        shop_rows.append({
            "shop": "Corporate", "till": "CORPORATE", "region": "Corporate",
            "on": blank(), "off": blank(), "oth": {"units": corp_units, "revenue": corp_rev},
            "onShare": None, "revenue": corp_rev, "target": round(corp_tgt) if corp_tgt else None,
        })
    for x in shop_rows:
        t = x["target"]
        x["attain"] = round(x["revenue"] / t * 100, 1) if t else None
        x["pace"] = round(x["revenue"] / (t * frac) * 100, 1) if t else None
        x["behind"] = x["pace"] is not None and x["pace"] < 100

    def _pace_of(lst):
        tgt = sum(x["target"] for x in lst if x["target"])
        rev = sum(x["revenue"] for x in lst if x["target"])
        return round(rev / (tgt * frac) * 100, 1) if tgt else None

    kenya_pace = _pace_of([x for x in shop_rows if x["till"] != "CORPORATE"])
    regions = {}
    for x in shop_rows:
        regions.setdefault(x["region"], []).append(x)
    region_rows = []
    for reg, lst in regions.items():
        # Red = behind its pro-rated target AND below its benchmark — the region's pace (2+
        # targeted shops) or, for a one-shop region, the Kenya-wide POS pace.
        targeted = [x for x in lst if x["target"]]
        bench = _pace_of(lst) if len(targeted) >= 2 else kenya_pace
        kind = "region pace" if len(targeted) >= 2 else "Kenya pace"
        lst.sort(key=lambda x: (x["pace"] is None, -(x["pace"] or 0), -x["revenue"]))
        for i, x in enumerate(lst):
            x["benchmark"], x["benchmarkKind"] = bench, kind
            x["red"] = bool(x["behind"] and bench is not None and x["pace"] < bench)
            x["rank"] = i + 1
            x["leader"] = i == 0 and x["pace"] is not None and len(lst) > 1
        region_rows.append({
            "region": reg, "shops": [x["shop"] for x in lst],
            "revenue": sum(x["revenue"] for x in lst),
            "target": sum(x["target"] for x in lst if x["target"]) or None,
            "pace": _pace_of(lst), "redCount": sum(1 for x in lst if x["red"]),
        })
    region_rows.sort(key=lambda r: (r["region"] in ("Corporate", "Other"), -r["revenue"]))

    # Bags printed inside combos but never sold singly still belong in the bag tables.
    for bag, n in in_combos.items():
        if n <= 0 or bag in on_bags or bag in off_bags:
            continue
        side, bt, srcs, is_new, offers = classify(bag)
        if side == "on":
            on_bags[bag] = {"bag": bag, "sources": offers or srcs, "isNew": is_new, "bySource": {},
                            "revBySource": {}, "priceBySource": {}, **blank()}
        elif side == "off":
            off_bags[bag] = {"isNew": is_new, "dowElsewhere": False, "comboBag": "Combo component" in offers,
                             "timed": False, **blank()}

    off_list = []
    for bag, v in off_bags.items():
        if v["units"] <= 0 and in_combos.get(bag, 0) <= 0:
            continue
        x = cover.get(bag) or extra_off.get(bag, {})
        off_list.append({"bag": bag, "isNew": v["isNew"], "units": v["units"], "revenue": v["revenue"],
                         "dowElsewhere": v.get("dowElsewhere", False),
                         "comboBag": v.get("comboBag", False), "timed": v.get("timed", False),
                         # combo prints are shown once — on the on-offer row when the bag has one
                         "inCombos": 0 if bag in on_bags else in_combos.get(bag, 0),
                         "stock": x.get("stock"), "avgPerDay": x.get("avgPerDay"),
                         "daysCover": x.get("daysCover")})
    off_list.sort(key=lambda x: (-x["revenue"], -x["inCombos"]))
    for b in on_bags.values():
        b["inCombos"] = in_combos.get(b["bag"], 0)
    on_list = sorted((b for b in on_bags.values() if b["units"] > 0 or b["inCombos"] > 0),
                     key=lambda x: (-x["revenue"], -x["inCombos"]))

    order = ["Combo sale"] + _SOURCE_ORDER
    src_rows = sorted(({"label": k, **v} for k, v in by_source.items()),
                      key=lambda x: order.index(x["label"]) if x["label"] in order else 99)

    # Offer type per week (Wk 1 … current), with the days each week has had so far.
    week_rows = []
    if w["trend"] == "week":
        upto = min(w["upto"], e)
        for k in sorted(by_week):
            ws = month_anchor + datetime.timedelta(days=7 * (k - 1))
            lo, hi = max(ws, s), min(ws + datetime.timedelta(days=6), e)
            week_rows.append({"label": f"Wk {k}", "sub": f"{lo.strftime('%d %b')}–{hi.strftime('%d %b')}",
                              "days": max(0, (min(hi, upto) - lo).days + 1), "current": lo <= upto <= hi,
                              "rows": {r: {"units": v[0], "revenue": v[1]} for r, v in by_week[k].items()}})

    trend_rows = []
    for k in sorted(trend):
        if w["trend"] == "week":
            ws = month_anchor + datetime.timedelta(days=7 * (k - 1))
            lo, hi = max(ws, s), min(ws + datetime.timedelta(days=6), e)
            lbl, sub = f"Wk {k}", f"{lo.strftime('%d %b')}–{hi.strftime('%d %b')}"
        else:
            lbl, sub = k.strftime("%a"), k.strftime("%d %b")
        trend_rows.append({"label": lbl, "sub": sub, **trend[k]})

    return {
        "label": w["label"],
        "range": f"{s.strftime('%d %b')} – {e.strftime('%d %b %Y')}",
        "from": s.isoformat(), "to": e.isoformat(),
        "daysElapsed": elapsed, "daysInPeriod": w["days"],
        "complete": elapsed >= w["days"],
        "trendBy": w["trend"],
        "kenyaPace": kenya_pace,
        "totals": tot,
        "others": [{"label": k, **v} for k, v in others.items()],
        "comboPrints": sum(in_combos.values()),
        "inCombosByBag": in_combos,
        "unclassifiedNames": sorted(unc_names)[:40],
        "unclassifiedCount": len(unc_names),
        "trend": trend_rows,
        "sources": src_rows,
        "offerTypes": _offer_types(mtx),
        "offerTypesByWeek": week_rows,
        "onBags": on_list,
        "offBags": off_list,
        "shops": shop_rows,
        "regions": region_rows,
    }


def _offer_types(mtx):
    """Matrix payload: rows, per-row category / tier cells, and the period's Top-5 categories
    (by revenue across every row) vs the other 13."""
    rnd = lambda c: {"units": round(c[0], 2), "revenue": round(c[1])}
    cat_rev = {c: 0.0 for c in CATEGORIES}
    for v in mtx.values():
        for cat, c in v["cat"].items():
            if cat in cat_rev:
                cat_rev[cat] += c[1]
    top = sorted(CATEGORIES, key=lambda c: -cat_rev[c])[:5]
    return {
        "rows": [{"key": k, "label": lbl} for k, lbl in OFFER_ROWS],
        "cat": {k: {c: rnd(x) for c, x in v["cat"].items()} for k, v in mtx.items()},
        "tier": {k: {t: rnd(x) for t, x in v["tier"].items()} for k, v in mtx.items()},
        "tree": {k: {n: rnd(x) for n, x in v["tree"].items()} for k, v in mtx.items()},
        "top": top, "rest": [c for c in CATEGORIES if c not in top],
        "catRevenue": {c: round(v) for c, v in cat_rev.items()},
    }


def _as_date(v):
    return v if isinstance(v, datetime.date) else datetime.date.fromisoformat(str(v)[:10])


def fetch():
    m_start, m_end = report_month.live_month_window()
    today = datetime.date.today()
    month_label = m_start.strftime("%B %Y")
    month_anchor = m_start - datetime.timedelta(days=(m_start.weekday() + 1) % 7)  # Sunday on/before day 1
    wins = _windows(today, m_start, m_end)
    lo = min(w["start"] for w in wins.values())
    hi = max(w["end"] for w in wins.values())

    ok, msg = db.check_connection()
    if not ok:
        print(f"  DB unreachable — {msg}; bags_on_offer.html left unchanged.")
        return None
    src = _load_source(month_label)
    if not src:
        print("  No on-offer source — bags_on_offer.html left unchanged.")
        return None
    if not _has_deals(src) and os.environ.get("BOO_ALLOW_NO_DEALS") != "1":
        print("  On-offer source has no Power Deal / Deal of the Week bags (deals sheet not loaded?)"
              " — bags_on_offer.html left unchanged. Set BOO_ALLOW_NO_DEALS=1 if the month has none.")
        return None
    new_names = sorted(set(_new_products()), key=len, reverse=True)

    def new_of(name):
        n = re.sub(r"^\[[^\]]*\]\s*", "", name).strip()          # Odoo "[S_0] LAMORA …" codes
        for np in new_names:
            if n == np or n.startswith(np + " "):
                return np
        return None

    timed_bags = set()                  # bags listed on a timed offer that sold inside it

    def make_classifier(src_m, anchor_m):
        """(infer, base, classify) for one month's offer list — a sale is judged by the offers of
        its own month (docs/bags-on-offer.md › Period selector)."""
        on_offer = src_m.get("onOffer", {})
        infer, is_on_offer = smc.bag_classifier(set(on_offer))
        # Per on-offer name: its own matcher, so a sold bag picks up the right source tags.
        per_name = [(smc.bag_classifier({n})[1], srcs) for n, srcs in on_offer.items()]

        def sources_of(bt):
            tags = []
            for match, srcs in per_name:
                if match(bt):
                    tags += [x for x in srcs if x not in tags]
            return sorted(tags, key=lambda x: _TAG_ORDER.index(x) if x in _TAG_ORDER else 99)

        cache = {}

        # Where / when each Deal of the Week runs: (matcher, weeks, shop labels).
        dow_runs = [(smc.bag_classifier({r["product"]})[1], set(r.get("weeks") or []), set(r.get("locations") or []))
                    for r in src_m.get("dowRuns", []) if r.get("product")]

        def base(name):
            """Name-only part of the classification (cached): gift bag / combo / unresolved, or a bag
            with its all-month offers (Power Deal, combo component) and its Deal-of-the-Week runs."""
            if name in cache:
                return cache[name]
            other = _other_group(name)
            if other:
                res = ("oth", other, [], False, [])
            elif "+" in name:
                res = ("combo", name, [], False, [])
            else:
                npn = new_of(name)
                bt = ("LAPTOP SLEEVE" if "LAPTOP SLEEVE" in name.upper() else None) or infer(name) or npn
                if not bt:
                    res = ("unc", name, [], False, [])
                else:
                    static = [x for x in sources_of(bt) if x != "Deal of the Week"] if is_on_offer(bt) else []
                    runs = [(wk, locs) for match, wk, locs in dow_runs if match(bt)]
                    res = ("bag", bt, static, bool(npn) or (bt in new_names), runs)
            cache[name] = res
            return res

        def classify(name, shop=None, d=None, timed=None):
            """(side, bag, sources, isNew, allOffers) — side is on / off / oth / unc. A single sale is
            a Deal-of-the-Week sale only at a shop running that deal, in its tier's weeks (shop/d
            None = "anywhere", used for bags seen only inside combos). `timed` = the line was sold
            inside a timed-offer campaign. Sources are in counting order: Timed offer → Power Deal
            → Deal of the Week → Combo component."""
            kind, bt, static, is_new, runs = base(name)
            if kind == "oth":
                return ("oth", bt, [bt], False, [])
            if kind == "combo":
                return ("on", bt, ["Combo sale"], False, [])
            if kind == "unc":
                return ("unc", bt, [], False, [])
            if shop is None:
                dow_ok = bool(runs)
            else:
                wk, loc = (d - anchor_m).days // 7 + 1, _shop_label(shop)
                dow_ok = any(wk in weeks and loc in locs for weeks, locs in runs)
            # Counted on offer only through a Power Deal or a Deal of the Week (8 Oct 2026); a timed-offer
            # sale or a combo bag bought alone is not on offer (it still carries the tag in all_offers).
            srcs = [x for x in ("Power Deal",) if x in static]
            if dow_ok:
                srcs.append("Deal of the Week")
            all_offers = sorted(set(static) | ({"Deal of the Week"} if runs else set())
                                | ({"Timed offer"} if timed or bt in timed_bags else set()),
                                key=lambda x: _TAG_ORDER.index(x) if x in _TAG_ORDER else 99)
            return ("on" if srcs else "off", bt, srcs, is_new, all_offers)
        return infer, base, classify

    infer, base, classify_cur = make_classifier(src, month_anchor)
    # A window can reach into earlier months (Last week, Custom): their days use that month's
    # archived offer list (docs/bags-on-offer.md › Period selector), else this month's.
    by_month = {m_start: classify_cur}

    def classify_for(d):
        ms = d.replace(day=1)
        if ms not in by_month:
            src_m = _archived_source(ms) if ms < m_start else None
            by_month[ms] = (make_classifier(src_m, ms - datetime.timedelta(days=(ms.weekday() + 1) % 7))[2]
                            if src_m else classify_cur)
            print(f"  {ms:%B %Y} days   : " + ("its archived offer list" if src_m else "no archive — this month's list"))
        return by_month[ms]

    def classify(name, shop=None, d=None, timed=None):
        if d is not None and d < m_start:
            return classify_for(d)(name, shop, d, timed)
        return classify_cur(name, shop, d, timed)

    params = {"s": lo.isoformat(), "e": hi.isoformat()}

    def rows(sql):
        df = db.run_query(sql, params)
        out = [] if df is None else df.to_dict("records")
        for r in out:
            if "d" in r:
                r["d"] = _as_date(r["d"])
            for k in ("units", "revenue"):
                if k in r:
                    r[k] = int(r[k] or 0)
            for k in ("shop", "name"):
                if k in r:
                    r[k] = str(r[k])
        return out

    lines, till, corp, targets = rows(LINES_SQL), rows(TILL_SQL), rows(CORPORATE_SQL), rows(TARGET_SQL)

    # ── Timed offers: carve each campaign's single-bag lines out of `lines` ──
    timed_lines, timed_names = {}, []
    for o in _timed_offers():
        start = o.get("clearanceStart") or o["startDate"]
        try:
            os_, oe = max(lo, datetime.date.fromisoformat(start)), min(hi, datetime.date.fromisoformat(o["endDate"]))
        except ValueError:
            continue
        if os_ > oe:
            continue
        sql = (TIMED_SQL + tof._shop_sql(o.get("shops")) + tof._time_sql(o.get("startTime"), o.get("endTime"))
               + tof._price_sql(o.get("minPrice"), o.get("maxPrice")) + tof._name_sql(o.get("nameLike")))
        df = db.run_query(sql, {"s": os_.isoformat(), "e": oe.isoformat()})
        # nameLike offers (e.g. [REJECT]) take every matching bag; others only their listed bags.
        wanted = None if o.get("nameLike") else {infer(b) or new_of(b.upper()) or b.upper() for b in o.get("bags", [])}
        n = 0
        for r in ([] if df is None else df.to_dict("records")):
            kind, bt = base(str(r["name"]))[:2]
            if kind != "bag" or (wanted is not None and bt not in wanted) or r["line_id"] in timed_lines:
                continue
            timed_lines[r["line_id"]] = (str(r["shop"]), str(r["name"]), _as_date(r["d"]),
                                         int(r["units"] or 0), int(r["revenue"] or 0), o["name"])
            n += 1
        if n:
            timed_names.append(o["name"])
            if wanted:
                timed_bags.update(wanted)
    if timed_lines:
        # Split each (shop, product, day) line into its timed part and the rest.
        tsum = {}
        for shop, name, d, u, rev, _nm in timed_lines.values():
            t = tsum.setdefault((shop, name, d), [0, 0])
            t[0] += u
            t[1] += rev
        split = []
        for r in lines:
            t = tsum.pop((r["shop"], r["name"], r["d"]), None)
            if not t:
                split.append(r)
                continue
            split.append({**r, "units": t[0], "revenue": t[1], "timed": True})
            if r["units"] - t[0] or r["revenue"] - t[1]:
                split.append({**r, "units": r["units"] - t[0], "revenue": r["revenue"] - t[1]})
        lines = split
        print(f"  Timed offers     : {len(timed_lines)} till lines in {', '.join(timed_names)}")

    # ── Bags printed inside combos (per day) ──
    import ast

    def resolve(n):
        n = re.sub(r"\s+", " ", str(n).strip().upper())
        n = re.sub(r"\s+COMBO$", "", n)
        return infer(n) or new_of(n) or (n.split(" or ")[0].split(" OR ")[0].strip() or None)

    prints = []
    for r in rows(COMBO_SUBLINES_SQL):
        bag = resolve(r["name"])
        if bag:
            prints.append({"d": r["d"], "bag": bag, "units": r["units"]})
    for r in rows(COMBO_PRINTS_SQL):                              # returned combos (no sub-lines)
        slots = r["name"].count("+") + 1
        picked = []
        raw = str(r.get("attrs") or "").strip()
        if raw:
            try:
                parsed = ast.literal_eval(raw)
                for dct in (parsed if isinstance(parsed, list) else [parsed]):
                    if isinstance(dct, dict):
                        picked += [str(v["full_name_product"]) for v in dct.values()
                                   if isinstance(v, dict) and v.get("full_name_product")]
            except (ValueError, SyntaxError):
                picked = []
        if picked:
            # Two identical bags (Jumbo Brown + Jumbo Brown) are stored as ONE entry — pad to
            # the combo's bag count so the pair counts as 2.
            picked += [picked[-1]] * max(0, slots - len(picked))
        else:
            picked = r["name"].split("+")                         # no attribute data (some CBRs)
        for nm in picked:
            bag = resolve(nm)
            if bag:
                prints.append({"d": r["d"], "bag": bag, "units": r["units"]})
    # ── Category + tier of every sale, for the offer-type matrix ──
    tiers = _bag_tiers()
    try:
        offer_cats = opk._read_offers()[0]
    except Exception as ex:                                  # noqa: BLE001
        print(f"  Categories       : offer sheet unreadable ({ex}) — keyword fallback only")
        offer_cats = {}
    seg_cache = {}

    def cat_tier(bag):
        """(category, tier) of a resolved bag — bag_tiers.csv first, else the offer sheet's
        category (aliases + name keywords). Anything outside the 18 categories → ''."""
        if not bag:
            return ("", "")
        if bag not in seg_cache:
            c, t = tiers.get(bag, ("", ""))
            if not c:
                c = rsl._category_of(bag, offer_cats)
            seg_cache[bag] = (c if c in CATEGORIES else "", t)
        return seg_cache[bag]

    def seg_of(name, side, bag, srcs):
        """[(category, tier, bag, weight)] for one till line — a combo is split evenly over its slots
        (Jumbo + Jumbo = one combo sale: ½ + ½ to JUMBO)."""
        if side == "oth":
            return [cat_tier("GIFT BAG") + ("GIFT BAG", 1.0)] if srcs[0] == "Gift bags" else [("", "", "SAMPLES", 1.0)]
        if srcs and srcs[0] == "Combo sale":
            slots = [x for x in str(name).split("+") if x.strip()] or [name]
            out = []
            for x in slots:
                b = resolve(x)
                out.append(cat_tier(b) + (b or "", 1.0 / len(slots)))
            return out
        return [cat_tier(bag) + (bag or "", 1.0)]

    for t in targets:
        t["start_date"], t["end_date"] = _as_date(t["start_date"]), _as_date(t["end_date"])
        t["target"] = float(t["target"] or 0)

    nof = src.get("bagsNotOnOffer") or {}
    extra_off = {x["bag"]: x for x in nof.get("notOnOffer", [])}

    # Stock + days of cover for EVERY bag (point-in-time, same rule as Menu 4): today's Kenya
    # stock ÷ this month's pace on the days the bag actually sold (single sales + combo prints).
    stock_map = src.get("stockMap") or {}
    m_units, m_days = {}, {}
    for r in lines:
        if m_start <= r["d"] <= m_end:
            kind, bt = base(r["name"])[:2]
            if kind == "bag" and r["units"] > 0:
                m_units[bt] = m_units.get(bt, 0) + r["units"]
                m_days.setdefault(bt, set()).add(r["d"])
    for r in prints:
        if m_start <= r["d"] <= m_end and r["units"] > 0:
            m_units[r["bag"]] = m_units.get(r["bag"], 0) + r["units"]
            m_days.setdefault(r["bag"], set()).add(r["d"])
    cover = {}
    for bt in set(m_units) | set(stock_map):
        if bt not in stock_map:
            continue
        stk = stock_map[bt]
        avg = m_units.get(bt, 0) / len(m_days[bt]) if m_days.get(bt) else 0
        cover[bt] = {"stock": stk, "avgPerDay": round(avg, 1),
                     "daysCover": int(round(stk / avg)) if avg > 0 else None}

    periods = {k: _build_period(w, lines, till, corp, targets, classify, extra_off, w.get("anchor", month_anchor),
                                prints, cover, seg_of)
               for k, w in wins.items()}
    # Inside combos vs on its own, per running combo (docs/bags-on-offer.md › Inside combos vs on its own).
    combo_list = src.get("combos") or []
    for P in periods.values():
        singles = {}
        for lst in (P["onBags"], P["offBags"]):
            for b in lst:
                u, k = singles.get(b["bag"], (0, 0))
                singles[b["bag"]] = (u + (b.get("units") or 0), k + (b.get("revenue") or 0))
        prints = P.pop("inCombosByBag", {}) or {}
        out = []
        for c in combo_list:
            keys = []
            for n in c.get("bags") or []:
                bt = infer(n) if n else None
                if bt and bt not in keys:
                    keys.append(bt)
            rows = [{"bag": bt, "inCombos": prints.get(bt, 0), "alone": singles.get(bt, (0, 0))[0],
                     "aloneKes": singles.get(bt, (0, 0))[1]} for bt in keys]
            if any(r["inCombos"] or r["alone"] for r in rows):
                out.append({"combo": c.get("label", ""), "bags": rows})
        P["comboVsAlone"] = out
    # Tier + category on every bag row, for the bag tables' Tier tags / filter.
    for P in periods.values():
        for lst in (P["onBags"], P["offBags"]):
            for b in lst:
                b["category"], b["tier"] = cat_tier(b["bag"])
    # Out of stock — call back (WhatsApp Monitoring): distinct people per bag per shop, keyed by
    # this page's own classification (base()), Kenya only like the rest of the page — Sinza and
    # Uganda requests are left out; Website stays (it is a Kenya till).
    def oos_key(name):
        kind, bt = base(name)[:2]
        return bt if kind == "bag" else None
    oos_rows = oos_callbacks.load_rows()
    kenya = lambda r: r["kind"] != "region" and r["shop"].upper() != "SINZA"
    oos = oos_callbacks.aggregate(oos_rows, key_fn=oos_key, colour_fn=colours.family, shop_filter=kenya)
    # each shop's live on-hand + "call now" (still waiting, bag / colour in stock where they asked)
    oos_callbacks.attach_stock(oos, oos_key, colours.family, rows=oos_rows, shop_filter=kenya)
    shown = {b["bag"] for P in periods.values() for lst in (P["onBags"], P["offBags"]) for b in lst}
    print(f"  OOS call-backs: {len(oos.get('lifetime', {}))} bags asked for (lifetime), "
          f"{len(shown & set(oos.get('lifetime', {})))} of {len(shown)} table bags have asks")
    return {
        "month": month_label,
        "asOf": today.isoformat(),
        "oos": oos,
        "birthdays": shop_birthdays.by_shop(today),   # 🎂 shops within 30 days of their birthday
        "generated": datetime.datetime.now().strftime("%d %b %Y %H:%M"),
        "newProducts": new_names,
        "menu4NotOnOfferRevenue": nof.get("notOnOfferRevenue"),
        "periods": periods,
        # Sinza & Uganda, same on-offer rule, from till receipts (docs/bags-on-offer.md › Sinza & Uganda)
        "markets": _market_periods(wins, today),
    }


def inject(payload):
    with open(HTML, "r", encoding="utf-8") as f:
        html = f.read()
    block = ("<!-- BOO_DATA_START -->\n<script>\nconst BOO = "
             + json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str)
             + ";\n</script>\n<!-- BOO_DATA_END -->")
    html = re.sub(r"<!-- BOO_DATA_START -->.*?<!-- BOO_DATA_END -->", lambda _m: block, html,
                  flags=re.DOTALL)
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)


def fmt(n):
    return f"{int(round(n or 0)):,}"


def main():
    # python bags_on_offer.py 2026-09-15 2026-10-03  → set the Custom period; "clear" removes it.
    args = sys.argv[1:]
    if args and args[0].lower() == "clear":
        save_custom_range(None, None)
    elif len(args) >= 2:
        save_custom_range(datetime.date.fromisoformat(args[0]), datetime.date.fromisoformat(args[1]))
    payload = fetch()
    if payload is None:
        return
    inject(payload)
    print(f"bags_on_offer.html updated — {payload['month']} (Kenya).")
    for key, p in payload["periods"].items():
        t = p["totals"]
        print(f"  [{p['label']}] {p['range']} · day {p['daysElapsed']}/{p['daysInPeriod']}")
        print(f"    On offer     : {fmt(t['on']['units'])} units · KES {fmt(t['on']['revenue'])}")
        print(f"    Not on offer : {fmt(t['off']['units'])} units · KES {fmt(t['off']['revenue'])}"
              + (f"  (Menu 4 panel: KES {fmt(payload['menu4NotOnOfferRevenue'])})" if key == "monthly" else ""))
        print(f"    Others       : {fmt(t['oth']['units'])} units · KES {fmt(t['oth']['revenue'])}  ("
              + ", ".join(f"{o['label']} KES {fmt(o['revenue'])}" for o in p["others"]) + ")")
        print(f"    Unclassified : KES {fmt(t['unc']['revenue'])} · {p['unclassifiedCount']} products"
              f" · red shops {sum(1 for x in p['shops'] if x['red'])}/{sum(1 for x in p['shops'] if x['target'])}")
    if not os.environ.get("DENRI_LAUNCHER"):
        webbrowser.open(pathlib.Path(HTML).as_uri())


if __name__ == "__main__":
    main()
