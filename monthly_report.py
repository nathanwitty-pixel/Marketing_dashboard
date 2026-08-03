#!/usr/bin/env python3
"""
monthly_report.py
─────────────────────────────────────────────────────────────────
Builds monthly_report.html — an executive monthly report that follows the
four-step framework for each area (Current Performance, New Products, Offer
Type Analysis, Posting Yields):

    1. Get attention  → lead with the conclusion
    2. Deliver the insight → the answer to a business question
    3. Recommendation → Stop / Start / Start-testing
    4. Business impact → quantified, with the assumptions stated

It reads the numbers already injected into the other dashboards (same approach
as generate_insights.py), so it must run AFTER them. The report month comes from
the projection month (the completed month during the first days of a new one),
so early-August runs correctly report July.

    python monthly_report.py

Change AVG_PRICE below if you want the revenue lines quantified with your real
average selling price.
"""
import os, re, json
import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

# ── MANUAL INPUT ──────────────────────────────────────────────
AVG_PRICE = 2500          # illustrative KES per bag — set to your real average


# ── READ HELPERS (mirror generate_insights.py) ────────────────
def read_block(fname, start, end):
    path = os.path.join(BASE, fname)
    if not os.path.exists(path):
        return ""
    txt = open(path, encoding="utf-8").read()
    m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), txt, re.DOTALL)
    return m.group(1) if m else ""

def gstr(block, key, default=""):
    m = re.search(rf'\b{key}"?\s*:\s*"([^"]*)"', block)
    return m.group(1) if m else default

def garr(block, key):
    m = re.search(rf'\b{key}"?\s*:\s*(\[.*?\]),?\s*\n', block)
    if not m:
        return []
    try:
        return json.loads(m.group(1))
    except (ValueError, TypeError):
        return []

def num(s, default=0.0):
    try:
        v = str(s).replace(",", "").replace("%", "").replace("x", "").strip()
        return float(v) if v else default
    except (ValueError, TypeError):
        return default

def gnum(block, key, default=0.0):
    """Numeric field reader that handles BOTH quoted ("1,211") and bare (7, 89.7)
    values — gstr only matches quoted strings, so counts like productCount fail it."""
    m = re.search(rf'\b{key}"?\s*:\s*"?\s*(-?[\d,\.]+)', block)
    return num(m.group(1)) if m else default

def fmt(n):   return f"{int(round(n)):,}"
def pct(n):   return f"{n:.1f}%"
def esc(s):   return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── READ THE DASHBOARDS ───────────────────────────────────────
perf = read_block("current_performance.html", "<!-- PERF_DATA_START -->", "<!-- PERF_DATA_END -->")
proj = read_block("current_performance.html", "<!-- PROJ_DATA_START -->", "<!-- PROJ_DATA_END -->")
np_  = read_block("new_products.html", "<!-- NEW_PROD_DATA_START -->", "<!-- NEW_PROD_DATA_END -->")
oa   = read_block("offer_type_analysis.html", "<!-- OFFER_DATA_START -->", "<!-- OFFER_DATA_END -->")
pa   = read_block("POSTING (SALES YIELDS FROM ACCURATE POSTING).html", "<!-- POST_DATA_START -->", "<!-- POST_DATA_END -->")

# Report month + year (projMonth is the completed month during a rollover)
month = gstr(proj, "projMonth") or datetime.date.today().strftime("%B")
year  = datetime.date.today().year

# Current performance
total_target = num(gstr(proj, "totalTarget"))
total_sales  = num(gstr(proj, "totalSales"))
achieved     = (total_sales / total_target * 100) if total_target else 0
gap          = max(total_target - total_sales, 0)
bare_min     = num(gstr(proj, "bareMinimum"))
corporate    = num(gstr(proj, "corporateBags"))
forecast     = gstr(proj, "forecastedProjection")

# Average weekly output for the report month (from weekly_history.json)
avg_weekly = 0
try:
    weeks = json.load(open(os.path.join(BASE, "weekly_history.json"))).get("weeks", [])
    m3 = month[:3]
    ws = [w.get("weeklySales", 0) for w in weeks if str(w.get("month", "")).startswith(m3)]
    if ws:
        avg_weekly = sum(ws) / len(ws)
except (ValueError, OSError):
    avg_weekly = 0
weekly_short = max(bare_min - avg_weekly, 0)

# New products
np_count   = int(gnum(np_, "productCount"))
np_target  = num(gstr(np_, "totalTarget"))
np_sales   = num(gstr(np_, "totalSales"))
np_pct     = (np_sales / np_target * 100) if np_target else 0
np_deficit = max(np_target - np_sales, 0)
np_kenya   = num(gstr(np_, "monthlyKenya"))
np_outside = num(gstr(np_, "monthlyOutside"))
np_posts   = num(gstr(np_, "mpostKenya")) + num(gstr(np_, "mpostOutside"))
np_names   = garr(np_, "productNames")
np_targets = garr(np_, "productTargets")   # [{name, target, sold, remaining}, ...]
# Per-new-product posts + current stock — colour rows aggregated up to bag type.
np_combined = garr(np_, "monthlyCombined")
_np_ps = {}
for _r in np_combined:
    _bt = str(_r.get("bagType") or "").strip().upper()
    if not _bt:
        continue
    _e = _np_ps.setdefault(_bt, {"posts": 0.0, "stock": 0.0})
    _e["posts"] += num(_r.get("mpostKenya")) + num(_r.get("mpostOutside"))
    _e["stock"] += num(_r.get("sKenya")) + num(_r.get("sOutside"))

# Offer type analysis
combos    = int(gnum(oa, "comboCount"))
deals     = int(gnum(oa, "powerDealCount"))
ke_stock  = num(gstr(oa, "totalKenyaStock"))
sz_stock  = num(gstr(oa, "totalSinzaStock"))
ug_stock  = num(gstr(oa, "totalUgandaStock"))

# Combos vs power deals movement (units moved, value = price x units, avg price).
def _garr_line(block, key):
    """Greedy single-line array extractor — handles nested [[...],[...]] arrays."""
    m = re.search(rf'\b{key}"?\s*:\s*(\[.*\]),?\s*\n', block)
    if not m:
        return []
    try:
        return json.loads(m.group(1))
    except (ValueError, TypeError):
        return []

def _parse_offers(headers, rows):
    headers = headers or []
    low = [str(h).lower().strip() for h in headers]
    iprice = next((i for i, h in enumerate(low) if "price" in h and "tsh" not in h), -1)
    if iprice < 0:
        iprice = next((i for i, h in enumerate(low) if "price" in h), -1)
    itotal = next((i for i, h in enumerate(low) if h == "total"), len(low) - 1)
    out = []
    for r in (rows or []):
        if not r:
            continue
        name = str(r[0]).strip()
        if not name or "total" in name.lower():
            continue
        price = num(r[iprice]) if 0 <= iprice < len(r) else 0
        units = num(r[itotal]) if 0 <= itotal < len(r) else 0
        out.append({"name": name, "units": units, "price": price})
    return out

def _agg_offers(offers):
    units = sum(o["units"] for o in offers)
    value = sum(o["units"] * o["price"] for o in offers)
    priced = [o["price"] for o in offers if o["price"] > 0]
    return units, value, (sum(priced) / len(priced) if priced else 0)

combo_offers = _parse_offers(_garr_line(oa, "juneComboHeaders"), _garr_line(oa, "juneCombos"))
deal_offers  = _parse_offers(_garr_line(oa, "powerDealHeaders"), _garr_line(oa, "powerDeals"))
combo_units, combo_value, combo_avg = _agg_offers(combo_offers)
deal_units, deal_value, deal_avg = _agg_offers(deal_offers)
offer_more_units = "combos" if combo_units >= deal_units else "power deals"
offer_more_value = "combos" if combo_value >= deal_value else "power deals"
offer_cheaper    = "power deals" if deal_avg <= combo_avg else "combos"
offer_pricier    = "combos" if offer_cheaper == "power deals" else "power deals"

# Posting yields
ke_wk_mkt = num(gstr(pa, "wkMktPct"))
ke_mo_mkt = num(gstr(pa, "moMktPct"))
sz_mo_mkt = num(gstr(pa, "szMoMktPct"))
ug_mo_mkt = num(gstr(pa, "ugMoMktPct"))
posted    = num(gstr(pa, "s3Posted"))
notposted = num(gstr(pa, "s3NotPosted"))
instock   = posted + notposted
unposted_pct = (notposted / instock * 100) if instock else 0
mo_sales_posting  = num(gstr(pa, "monthlySalesTotal"))
mo_expect_posting = num(gstr(pa, "monthlyExpected"))
posting_mult = (mo_sales_posting / mo_expect_posting) if mo_expect_posting else 0
mo_posts_made = gnum(pa, "monthlyPostsMade")

# Per-bag "which bags were never posted" (in stock, no marketing posts).
unmarketed_bags = garr(pa, "instockNotPosted")
unm_sorted = sorted(unmarketed_bags, key=lambda b: num(b.get("stock")), reverse=True)[:10]

# Weakest region by monthly sales-achieved
regions = [("Kenya", ke_mo_mkt), ("Sinza", sz_mo_mkt), ("Uganda", ug_mo_mkt)]
weak_name, weak_val = min(regions, key=lambda r: r[1])

# ── Outlook into the next month (weekly pace carried over) ────
import calendar as _cal
w_this   = gnum(perf, "weeklyThisMonth")
w_days   = gnum(perf, "weeklyThisMonthDays")
p_weekly = gnum(perf, "prevMonthWeekly")
p_days   = gnum(perf, "prevMonthDays")
p_label  = gstr(perf, "prevMonthLabel") or "last month"
_names   = list(_cal.month_name)
_mnum    = _names.index(month) if month in _names else datetime.date.today().month
next_month   = _cal.month_name[(_mnum % 12) + 1]
next_per_day = (w_this / w_days) if w_days else 0
proj_week    = next_per_day * 7
prev_per_day = (p_weekly / p_days) if p_days else 0
pace_ratio   = (next_per_day / prev_per_day) if prev_per_day else 0
show_outlook = w_days > 0 and w_this > 0 and prev_per_day > 0
w_total         = gnum(perf, "weeklySalesTotal")
carryover_month = gstr(perf, "carryoverMonth") or p_label
pct_of_week     = (w_this / w_total * 100) if w_total else 0
next_short      = next_month[:3]
growth_pct_txt  = gstr(perf, "weeklySalesPct")    or ""   # e.g. "19.73%"
prev_pct_txt    = gstr(perf, "previousSalesPct")  or ""   # e.g. "52.07%"
prev_bags_txt   = gstr(perf, "previousSalesBags") or ""   # e.g. "4,584"

# ── Sinza / Uganda offer movement (counts + units + value) ────
def _offers(hkey, rkey):
    return _parse_offers(_garr_line(oa, hkey), _garr_line(oa, rkey))
sz_combos_l  = _offers("sinzaComboHeaders",  "sinzaCombos")
sz_singles_l = _offers("sinzaSinglesHeaders", "sinzaSingles")
sz_special_l = _offers("sinzaSpecialHeaders", "sinzaSpecials")
sz_off_units, sz_off_value, sz_off_avg = _agg_offers(sz_combos_l + sz_singles_l + sz_special_l)
ug_combos_l  = _offers("ugComboHeaders",  "ugCombos")
ug_singles_l = _offers("ugSinglesHeaders", "ugSingles")
ug_off_units, ug_off_value, ug_off_avg = _agg_offers(ug_combos_l + ug_singles_l)

# Best-effort per-offer Uganda stock: sum STOCK_LEVELS Uganda stock by bag type / product name.
_ug_stock_by = {}
for _s in garr(oa, "ugStockData"):
    _q = num(_s.get("ugandaStock"))
    for _k in (str(_s.get("bagType") or ""), str(_s.get("productName") or "")):
        _k = _k.strip().upper()
        if _k:
            _ug_stock_by[_k] = _ug_stock_by.get(_k, 0) + _q
def _ug_stock_for(name):
    return _ug_stock_by.get(str(name).strip().upper(), 0)

# Judgment: was movement dead-stock clearance (offer/price) or marketing posting?
# posting_pct = the region's posting sales-achieved %; cleared = units moved / stock.
sz_cleared = (sz_off_units / sz_stock * 100) if sz_stock else 0
ug_cleared = (ug_off_units / ug_stock * 100) if ug_stock else 0
def _cause(region, units, cleared, posting_pct):
    lead = "marketing posting" if posting_pct >= cleared else "the offer/price clearing dead stock"
    tail = (" — but both are modest, so plenty of dead stock is still stuck."
            if (cleared < 40 and posting_pct < 60) else ".")
    return (f"<b>{region}</b> moved <b>{fmt(units)} bags</b> — <b>{cleared:.1f}% of its stock</b> cleared, "
            f"with posting sales-achieved at <b>{pct(posting_pct)}</b>. The bigger lever was "
            f"<b>{lead}</b>{tail}")
sz_judge = _cause("Sinza", sz_off_units, sz_cleared, sz_mo_mkt)
ug_judge = _cause("Uganda", ug_off_units, ug_cleared, ug_mo_mkt)

# Offer-type composition — share by count and by units moved (Kenya + Sinza).
def _share(parts):
    tot = sum(parts) or 1
    return [p / tot * 100 for p in parts]
ke_c_cnt, ke_d_cnt = len(combo_offers), len(deal_offers)
ke_cnt_pct  = _share([ke_c_cnt, ke_d_cnt])
ke_unit_pct = _share([combo_units, deal_units])
sz_c_cnt, sz_s_cnt, sz_sp_cnt = len(sz_combos_l), len(sz_singles_l), len(sz_special_l)
sz_cnt_pct  = _share([sz_c_cnt, sz_s_cnt, sz_sp_cnt])
sz_unit_pct = _share([_agg_offers(sz_combos_l)[0], _agg_offers(sz_singles_l)[0], _agg_offers(sz_special_l)[0]])

# ── Not-on-offer stock — the dead stock marketing must move ───
def _nested(block, key):
    m = re.search(rf'\b{key}"?\s*:\s*(\{{.*\}}),?\s*\n', block)
    return m.group(1) if m else ""
_sz_pa = _nested(pa, "sinza")
_ug_pa = _nested(pa, "uganda")
ke_notoffer_stock = notposted                                    # s3NotPosted = not-on-offer Kenya stock
sz_notoffer_stock = gnum(_sz_pa, "stockNotOnOffer")
ug_notoffer_stock = gnum(_ug_pa, "stockNotOnOffer")
ke_offer_stock    = posted                                       # s3Posted = on-offer Kenya stock
mo_sales_no_post  = gnum(pa, "monthlySalesNoPost")              # not-on-offer sales (still posted)

# ── IMPACTS (quantified, with assumptions) ────────────────────
weeks_n         = 4
cp_add          = (weekly_short / 2) * weeks_n
cp_new_pct      = achieved + (cp_add / total_target * 100 if total_target else 0)
cp_revenue      = cp_add * AVG_PRICE
np_recover      = np_deficit / 2
offer_clear     = ke_stock * 0.20
offer_clear_pct = (offer_clear / total_target * 100) if total_target else 0
post_convert    = notposted * 0.20
post_gap_share  = (post_convert / gap * 100) if gap else 0


# ── BUILD THE HTML ────────────────────────────────────────────
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>__TITLE__</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', system-ui, sans-serif; background: #0f1117; color: #e2e8f0; padding: 2rem; line-height: 1.55; }
  .wrap { width: 100%; max-width: 900px; margin: 0 auto; }
  .rpt-head { margin-bottom: 1.6rem; }
  .rpt-pill { display: inline-block; background: linear-gradient(135deg,#8b5cf6,#6366f1); color: #fff; font-size: 0.66rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; padding: 0.3rem 0.8rem; border-radius: 999px; margin-bottom: 0.7rem; }
  .rpt-head h1 { font-size: 1.9rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.01em; }
  .rpt-head .dek { font-size: 0.9rem; color: #94a3b8; margin-top: 0.35rem; }
  .exec { background: linear-gradient(160deg, #1b2333, #171a27); border: 1px solid #2d3148; border-left: 4px solid #34d399; border-radius: 16px; padding: 1.5rem 1.6rem; margin-bottom: 2rem; }
  .exec .lbl { font-size: 0.66rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; color: #6ee7b7; margin-bottom: 0.5rem; }
  .exec .headline { font-size: 1.2rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.9rem; }
  .exec .headline b { color: #facc15; }
  .exec ul { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
  .exec li { font-size: 0.9rem; color: #cbd5e1; padding-left: 1.2rem; position: relative; }
  .exec li::before { content: '\\25B8'; position: absolute; left: 0; color: #34d399; }
  .exec li b { color: #f8fafc; }
  .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr)); gap: 0.8rem; margin-bottom: 2rem; }
  .kpi { background: #1e2130; border: 1px solid #2d3148; border-radius: 12px; padding: 0.9rem 1rem; }
  .kpi .k-lbl { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #64748b; }
  .kpi .k-val { font-size: 1.6rem; font-weight: 800; color: #f8fafc; line-height: 1.1; margin-top: 0.2rem; font-variant-numeric: tabular-nums; }
  .kpi .k-sub { font-size: 0.72rem; color: #94a3b8; margin-top: 0.2rem; }
  .k-val.amber { color: #fbbf24; } .k-val.red { color: #f87171; } .k-val.green { color: #34d399; } .k-val.cyan { color: #22d3ee; }
  .sec { background: #1e2130; border: 1px solid #2d3148; border-radius: 16px; padding: 1.5rem 1.6rem; margin-bottom: 1.5rem; }
  .sec-head { display: flex; align-items: center; gap: 0.7rem; margin-bottom: 1rem; }
  .sec-num { width: 30px; height: 30px; flex-shrink: 0; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.9rem; color: #0b0d16; }
  .sec-head h2 { font-size: 1.15rem; font-weight: 700; color: #f8fafc; }
  .row { margin-bottom: 1rem; } .row:last-child { margin-bottom: 0; }
  .row .tag { font-size: 0.64rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; }
  .tag.bottom { color: #facc15; } .tag.insight { color: #22d3ee; } .tag.rec { color: #a78bfa; } .tag.impact { color: #34d399; }
  .row p { font-size: 0.9rem; color: #cbd5e1; } .row p b { color: #f8fafc; }
  .recs { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.4rem; }
  .rec-item { display: flex; align-items: baseline; gap: 0.6rem; font-size: 0.88rem; color: #cbd5e1; }
  .badge { flex-shrink: 0; font-size: 0.6rem; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase; padding: 0.18rem 0.5rem; border-radius: 5px; }
  .badge.stop  { background: rgba(248,113,113,0.16); color: #fca5a5; border: 1px solid rgba(248,113,113,0.35); }
  .badge.start { background: rgba(52,211,153,0.16); color: #6ee7b7; border: 1px solid rgba(52,211,153,0.35); }
  .badge.test  { background: rgba(34,211,238,0.16); color: #67e8f9; border: 1px solid rgba(34,211,238,0.35); }
  .impact { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.25); border-radius: 10px; padding: 0.7rem 0.9rem; margin-top: 0.4rem; }
  .impact p { font-size: 0.88rem; color: #d1fae5; } .impact b { color: #6ee7b7; }
  .assump { font-size: 0.72rem; color: #64748b; margin-top: 0.35rem; font-style: italic; }
  .foot { font-size: 0.72rem; color: #475569; text-align: center; margin-top: 1.5rem; }
  .chart-wrap { position: relative; height: 240px; margin: 0.2rem 0 1.2rem; }
  .chart-cap { font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.08em; color: #64748b; margin: 0 0 0.5rem; font-weight: 700; }
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
<div class="wrap">
"""

title = f"{month} {year} — Monthly Report"
head  = HEAD.replace("__TITLE__", title)

names_txt = ", ".join(esc(n) for n in np_names) if np_names else "the new products"

# Build the "which bags were never posted" list block (in stock, zero posts).
if unm_sorted:
    _unm_rows = "".join(
        '<div style="display:flex;justify-content:space-between;gap:.6rem;font-size:.82rem;padding:.28rem 0;border-top:1px solid rgba(148,163,184,.12)">'
        f'<span style="color:#e2e8f0"><b>{esc(b.get("colour",""))}</b> <span style="color:#64748b">{esc(b.get("productName", b.get("bagType","")))}</span></span>'
        f'<span style="color:#94a3b8;white-space:nowrap">{fmt(num(b.get("stock")))} in stock &middot; 0 posts</span></div>'
        for b in unm_sorted
    )
    unm_block = (
        '<div class="row"><div class="tag insight">Which bags were never posted</div>'
        '<p style="margin-bottom:.5rem">Against the month\'s posting, these in-stock bags carry <b>zero marketing posts</b> — the dead stock marketing moves first so the sales team can reach target:</p>'
        f'<div style="background:rgba(248,113,113,0.06);border:1px solid rgba(248,113,113,0.22);border-radius:10px;padding:.5rem .85rem">{_unm_rows}</div></div>'
    )
else:
    unm_block = ''

# Looking-into-next-month outlook (Section 1) — the two live weekly cards
if show_outlook:
    _pl = "" if int(w_days) == 1 else "s"
    outlook_block = (
        f'<div class="row"><div class="tag" style="color:#38bdf8">Momentum into {esc(next_month)}</div>'
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0.9rem">'
        # Weekly Sales card
        '<div style="position:relative;background:#171a27;border:1px solid #2d3148;border-radius:14px;padding:1.1rem 1.2rem;overflow:hidden">'
        '<div style="position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#8b5cf6,#6366f1)"></div>'
        '<div style="font-size:0.64rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#64748b">Weekly Sales</div>'
        f'<div style="font-size:2.1rem;font-weight:800;color:#f8fafc;line-height:1.15;margin:0.2rem 0 0.35rem">{fmt(w_total)}</div>'
        f'<div style="font-size:0.8rem;color:#93c5fd;line-height:1.5">{fmt(w_this)} this month ({pct_of_week:.1f}% of {fmt(w_total)}) &middot; {fmt(p_weekly)} from {esc(carryover_month)} &middot; {fmt(next_per_day)}/day &rarr; a full week at this pace &asymp; {fmt(proj_week)} bags</div>'
        '<div style="font-size:0.72rem;color:#64748b;margin-top:0.5rem">Total bags sold this week (Sun&ndash;Sat).</div>'
        '</div>'
        # Weekly vs Last Month card
        '<div style="position:relative;background:#171a27;border:1px solid #2d3148;border-radius:14px;padding:1.1rem 1.2rem;overflow:hidden">'
        '<div style="position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#8b5cf6,#22d3ee)"></div>'
        '<div style="font-size:0.64rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#64748b">Weekly vs Last Month</div>'
        f'<div style="font-size:2.1rem;font-weight:800;color:#34d399;line-height:1.15;margin:0.2rem 0 0.35rem">{pace_ratio:.2f}&times;</div>'
        f'<div style="font-size:0.8rem;color:#93c5fd;line-height:1.5">{esc(next_short)}: {fmt(w_this)} in {int(w_days)} day{_pl} ({fmt(next_per_day)}/day) vs {esc(p_label)}: {fmt(p_weekly)} in {int(p_days)} days ({fmt(prev_per_day)}/day)</div>'
        '<div style="font-size:0.72rem;color:#64748b;margin-top:0.5rem">This month&rsquo;s per-day pace vs last month&rsquo;s final-week pace. Above 1&times; means the new month is outrunning how last month closed.</div>'
        '</div>'
        '</div></div>'
    )
else:
    outlook_block = ''

# Sinza & Uganda offer movement (Section 3)
sz_ug_offer_block = (
    '<div class="row"><div class="tag insight">Sinza &amp; Uganda offers</div>'
    f'<p><b>Sinza</b> ran <b>{len(sz_combos_l)} combos</b>, {len(sz_singles_l)} singles and {len(sz_special_l)} specials, moving <b>{fmt(sz_off_units)} bags</b> (value {fmt(sz_off_value)}) against {fmt(sz_stock)} in stock. '
    f'<b>Uganda</b> ran <b>{len(ug_combos_l)} combos</b> and {len(ug_singles_l)} singles, moving <b>{fmt(ug_off_units)} bags</b> (value {fmt(ug_off_value)}) against {fmt(ug_stock)} in stock. '
    'Both are clearing only a thin slice of their offer stock — the same dead-stock problem as Kenya, at smaller scale.</p>'
    f'<p style="font-size:0.84rem;color:#cbd5e1;margin-top:0.5rem"><b style="color:#a78bfa">Dead stock or marketing?</b> {sz_judge} {ug_judge}</p></div>'
)

# Focus on moving the not-on-offer bags, across the three posting lenses (Section 4)
notoffer_block = (
    '<div class="row"><div class="tag rec">Focus — move the bags NOT on offer</div>'
    '<p style="margin-bottom:0.5rem">Marketing\'s real target is the stock sitting <b>not on offer</b>. Read across the three posting lenses:</p>'
    '<div class="recs">'
    f'<div class="rec-item"><span class="badge" style="background:rgba(148,163,184,0.16);color:#cbd5e1;border:1px solid rgba(148,163,184,0.35)">Combined</span><span><b>Sales vs Expected (Posted &amp; Unposted)</b> — of Kenya\'s in-stock bags, {fmt(ke_offer_stock)} are on offer but <b>{fmt(ke_notoffer_stock)} sit not on offer</b>: dead stock we aren\'t even putting in front of buyers.</span></div>'
    f'<div class="rec-item"><span class="badge start">With posting</span><span><b>Sales with Posting vs Expected</b> — where marketing posted, sales ran <b>~{posting_mult:.1f}× expected</b>. Posting demonstrably works, so aiming it at the not-on-offer pile is the lever.</span></div>'
    f'<div class="rec-item"><span class="badge test">No posting</span><span><b>Sales with no Posting vs Opportunity if Marketed</b> — the <b>sales team</b> already moved {fmt(mo_sales_no_post)} bags with <b>zero marketing</b>; the gap up to the opportunity is what marketing leaves on the table by not posting the not-on-offer stock.</span></div>'
    '</div>'
    f'<p style="font-size:0.82rem;color:#94a3b8;margin-top:0.55rem">Not-on-offer stock by region: <b>Kenya {fmt(ke_notoffer_stock)}</b>, <b>Sinza {fmt(sz_notoffer_stock)}</b>, <b>Uganda {fmt(ug_notoffer_stock)}</b> — and Sinza ({pct(sz_mo_mkt)}) and Uganda ({pct(ug_mo_mkt)}) move it far slower than Kenya ({pct(ke_mo_mkt)}). Same playbook, all three regions.</p></div>'
)

body = f"""
  <div class="rpt-head">
    <span class="rpt-pill">Monthly Report</span>
    <h1>{month} {year} — How the Month Went</h1>
    <div class="dek">Current Performance · New Products · Offer Type Analysis · Posting Yields</div>
  </div>

  <div class="exec">
    <div class="lbl">The Bottom Line</div>
    <div class="headline">
      {month} closed at <b>{pct(achieved)} of target</b> — {fmt(total_sales)} of {fmt(total_target)} bags,
      missing by <b>{fmt(gap)} bags</b>. The gap is not weak demand; it is <b>stock we never marketed</b>.
    </div>
    <ul>
      <li><b>{pct(unposted_pct)} of Kenya stock ({fmt(notposted)} bags) was never posted</b> — yet posted bags sold at {pct(ke_mo_mkt)} of expectation. Marketing is the lever, and much of it went unused.</li>
      <li><b>Weekly output (~{fmt(avg_weekly)} bags) ran below the {fmt(bare_min)}/week floor</b> needed to hit target — the problem is consistency, not a bad month.</li>
      <li><b>Regions are uneven:</b> Kenya posts at {pct(ke_mo_mkt)} sales-achieved, Sinza {pct(sz_mo_mkt)}, Uganda {pct(ug_mo_mkt)}. The Kenya playbook isn't being run elsewhere.</li>
    </ul>
  </div>

  <div class="kpis">
    <div class="kpi"><div class="k-lbl">Target Achieved</div><div class="k-val amber">{pct(achieved)}</div><div class="k-sub">{fmt(total_sales)} / {fmt(total_target)} bags</div></div>
    <div class="kpi"><div class="k-lbl">Missed By</div><div class="k-val red">{fmt(gap)}</div><div class="k-sub">bags short of target</div></div>
    <div class="kpi"><div class="k-lbl">Unmarketed Stock</div><div class="k-val red">{fmt(notposted)}</div><div class="k-sub">{pct(unposted_pct)} of Kenya stock not posted &middot; {fmt(mo_posts_made)} posts made this month</div></div>
    <div class="kpi"><div class="k-lbl">Posting Sales-Achieved</div><div class="k-val green">{pct(ke_mo_mkt)}</div><div class="k-sub">Kenya {pct(ke_mo_mkt)} &middot; Sinza {pct(sz_mo_mkt)} &middot; Uganda {pct(ug_mo_mkt)} (of expected)</div></div>
  </div>

  <div class="sec">
    <div class="sec-head"><div class="sec-num" style="background:#facc15">1</div><h2>Current Performance</h2></div>
    <div class="chart-cap">Sales vs monthly target</div>
    <div class="chart-wrap" style="height:250px"><canvas id="cp-chart"></canvas></div>
    <div style="display:flex;flex-wrap:wrap;gap:0.35rem 2rem;justify-content:center;font-size:0.8rem;color:#94a3b8;margin:-0.3rem 0 1.1rem">
      <span>Growth % towards achieved monthly sales: <b style="color:#fbbf24">{growth_pct_txt}</b></span>
      <span>Previous sales % achieved: <b style="color:#fbbf24">{prev_pct_txt} ({prev_bags_txt} bags)</b></span>
    </div>
    <div class="row"><div class="tag bottom">The Bottom Line</div>
      <p>We finished {month} at <b>{pct(achieved)} of target ({fmt(total_sales)} bags)</b>, <b>{fmt(gap)} bags short</b>. Weekly output averaged about <b>{fmt(avg_weekly)} bags</b> — under the <b>{fmt(bare_min)}-bag weekly floor</b> the target requires.</p></div>
    <div class="row"><div class="tag insight">The Insight</div>
      <p>Weekly output ran <b>below the bare minimum</b> needed to reach target most weeks. The shortfall is one of <b>throughput and consistency</b>, not demand — corporate orders ({fmt(corporate)} bags) only nudged the forecast to {forecast}.</p></div>
    <div class="row"><div class="tag rec">Recommendation</div>
      <div class="recs">
        <div class="rec-item"><span class="badge start">Start</span><span>Managing to a <b>hard {fmt(bare_min)}-bag weekly commit</b>, reviewed every Monday — not a single monthly number reconciled at month-end.</span></div>
        <div class="rec-item"><span class="badge stop">Stop</span><span>Treating the ~{fmt(weekly_short)}-bag weekly gap as normal. Each missed week is unrecoverable against a fixed monthly target.</span></div>
      </div></div>
    <div class="row"><div class="tag impact">Business Impact</div>
      <div class="impact"><p>Closing even <b>half the weekly gap (~{fmt(weekly_short/2)} bags/week)</b> across the month adds <b>~{fmt(cp_add)} bags</b> — lifting achievement from {pct(achieved)} to <b>~{pct(cp_new_pct)}</b>.</p></div>
      <div class="assump">Assumes ~{fmt(weekly_short/2)} bags/week recovered × {weeks_n} weeks; at ~KES {fmt(AVG_PRICE)}/bag that is ≈ KES {fmt(cp_revenue)} of recovered sales.</div></div>
    {outlook_block}
  </div>

  <div class="sec">
    <div class="sec-head"><div class="sec-num" style="background:#22d3ee">2</div><h2>New Products</h2></div>
    <div class="chart-cap">Each new product — sold vs remaining to target</div>
    <div class="chart-wrap"><canvas id="np-chart"></canvas></div>
    <div class="chart-cap">Each new product — posts done vs current stock (the dead-stock read)</div>
    <div class="chart-wrap"><canvas id="np-stock-chart"></canvas></div>
    <div class="row"><div class="tag bottom">The Bottom Line</div>
      <p>The {np_count} new products ({names_txt}) reached only <b>{pct(np_pct)} of their {fmt(np_target)}-bag target ({fmt(np_sales)} sold)</b> — a <b>{fmt(np_deficit)}-bag deficit</b>.</p></div>
    <div class="row"><div class="tag insight">The Insight</div>
      <p>New products received <b>{fmt(np_posts)} marketing posts</b> but converted just {fmt(np_sales)} bags, and <b>almost all of it ({fmt(np_kenya)} of {fmt(np_sales)}) was Kenya</b> — outside-Kenya is effectively <b>untested ({fmt(np_outside)} bags)</b>. Awareness is being created; conversion and distribution are the bottleneck.</p></div>
    <div class="row"><div class="tag rec">Recommendation</div>
      <div class="recs">
        <div class="rec-item"><span class="badge start">Start</span><span>A concentrated push on the <b>weakest launches</b> with price/offer support to clear the {fmt(np_deficit)}-bag deficit.</span></div>
        <div class="rec-item"><span class="badge test">Start testing</span><span><b>Outside-Kenya distribution</b> for the best-performing new lines — {fmt(np_outside)} bags sold there all month is an untested market, not a dead one.</span></div>
      </div></div>
    <div class="row"><div class="tag impact">Business Impact</div>
      <div class="impact"><p>Recovering <b>half the deficit (~{fmt(np_recover)} bags)</b> is realistic within one cycle; a working outside-Kenya channel would add a comparable second stream.</p></div>
      <div class="assump">Assumes weak-launch recovery of 50% of the {fmt(np_deficit)}-bag deficit; outside-Kenya upside sized off the {fmt(np_posts)}-post base.</div></div>
  </div>

  <div class="sec">
    <div class="sec-head"><div class="sec-num" style="background:#a78bfa">3</div><h2>Offer Type Analysis</h2></div>
    <div class="chart-cap">Kenya — each offer, units moved (amber = combo, violet = power deal)</div>
    <div class="chart-wrap" style="height:420px"><canvas id="offer-chart"></canvas></div>
    <div style="text-align:center;font-size:0.78rem;color:#94a3b8;margin:-0.3rem 0 1.1rem">
      <b>Offer mix</b> — by count: <b style="color:#fbbf24">Combos {ke_cnt_pct[0]:.0f}% ({ke_c_cnt})</b> vs <b style="color:#c4b5fd">Power Deals {ke_cnt_pct[1]:.0f}% ({ke_d_cnt})</b>
      &nbsp;·&nbsp; by units moved: <b style="color:#fbbf24">Combos {ke_unit_pct[0]:.0f}%</b> vs <b style="color:#c4b5fd">Power Deals {ke_unit_pct[1]:.0f}%</b>
    </div>
    <div class="chart-cap">Sinza — each offer, units moved (indigo = combo, cyan = single, pink = special)</div>
    <div class="chart-wrap" style="height:520px"><canvas id="offer-sinza-chart"></canvas></div>
    <div style="text-align:center;font-size:0.78rem;color:#94a3b8;margin:-0.3rem 0 1.1rem">
      <b>Offer mix</b> — by count: <b style="color:#818cf8">Combos {sz_cnt_pct[0]:.0f}% ({sz_c_cnt})</b> · <b style="color:#22d3ee">Singles {sz_cnt_pct[1]:.0f}% ({sz_s_cnt})</b> · <b style="color:#f472b6">Specials {sz_cnt_pct[2]:.0f}% ({sz_sp_cnt})</b>
      &nbsp;·&nbsp; by units: <b style="color:#818cf8">Combos {sz_unit_pct[0]:.0f}%</b> · <b style="color:#22d3ee">Singles {sz_unit_pct[1]:.0f}%</b> · <b style="color:#f472b6">Specials {sz_unit_pct[2]:.0f}%</b>
    </div>
    <div class="chart-cap">Uganda — top 5 &amp; bottom 5 movers, units moved vs stock available</div>
    <div class="chart-wrap" style="height:340px"><canvas id="offer-uganda-chart"></canvas></div>
    <div class="row"><div class="tag bottom">The Bottom Line</div>
      <p>Across <b>{combos} combos and {deals} power deals</b> (Kenya), the two offer types cleared stock very differently: <b>combos moved {fmt(combo_units)} bags</b> (KES {fmt(combo_value)}) while <b>power deals moved {fmt(deal_units)} bags</b> (KES {fmt(deal_value)}). <b>{offer_more_units.capitalize()}</b> shifted the most stock; <b>{offer_more_value}</b> made the most money.</p></div>
    <div class="row"><div class="tag insight">The Insight</div>
      <p>It's a price-point story: combos averaged <b>KES {fmt(combo_avg)}</b> per offer vs power deals <b>KES {fmt(deal_avg)}</b>. The cheaper <b>{offer_cheaper}</b> clear more volume, so <b>dead stock moves fastest through {offer_cheaper}</b> — yet <b>{fmt(ke_stock)} bags</b> remain in Kenya offer stock (plus {fmt(sz_stock)} Sinza, {fmt(ug_stock)} Uganda), so the mix still isn't drawing inventory down fast enough.</p></div>
    {sz_ug_offer_block}
    <div class="row"><div class="tag rec">Recommendation</div>
      <div class="recs">
        <div class="rec-item"><span class="badge start">Start</span><span>Routing the <b>slowest dead stock through {offer_cheaper}</b> (the higher-volume clearer) and keeping premium movers in <b>{offer_pricier}</b> for margin.</span></div>
        <div class="rec-item"><span class="badge stop">Stop</span><span>Restocking the <b>slowest-moving colours</b> until the {fmt(ke_stock)}-bag Kenya position draws down.</span></div>
      </div></div>
    <div class="row"><div class="tag impact">Business Impact</div>
      <div class="impact"><p>Clearing just <b>20% of the {fmt(ke_stock)}-bag Kenya position (~{fmt(offer_clear)} bags)</b> in the month is ~{pct(offer_clear_pct)} of target — and frees working capital tied up in slow stock.</p></div>
      <div class="assump">Assumes a 20% draw-down of the reported Kenya offer stock; excludes Sinza/Uganda upside.</div></div>
  </div>

  <div class="sec">
    <div class="sec-head"><div class="sec-num" style="background:#34d399">4</div><h2>Posting Yields (Sales from Accurate Posting)</h2></div>
    <div class="chart-cap">Posting sales-achieved % by region &amp; posted vs unposted stock</div>
    <div class="chart-wrap"><canvas id="posting-chart"></canvas></div>
    <div class="chart-wrap"><canvas id="stock-chart"></canvas></div>
    <div class="row"><div class="tag bottom">The Bottom Line</div>
      <p>Marketing posting is our most effective lever — Kenya posted bags hit <b>{pct(ke_mo_mkt)} of expected sales monthly</b> — but <b>{pct(unposted_pct)} of in-stock bags ({fmt(notposted)}) were never posted</b>. The target gap is sitting in unmarketed stock.</p></div>
    {unm_block}
    <div class="row"><div class="tag insight">The Insight</div>
      <p>Where we post, we sell: monthly sales on posted bags ({fmt(mo_sales_posting)}) ran <b>~{posting_mult:.1f}× the {fmt(mo_expect_posting)} expected</b>. Yet only <b>{fmt(posted)} bags were on offer/posted vs {fmt(notposted)} not</b>. Regionally the discipline collapses — Kenya {pct(ke_mo_mkt)}, <b>Sinza {pct(sz_mo_mkt)}, Uganda {pct(ug_mo_mkt)}</b> — so the biggest untapped demand is in <b>{weak_name}</b> and in unmarketed stock.</p></div>
    {notoffer_block}
    <div class="chart-cap">Bags NOT on offer, by region — the dead stock marketing must move</div>
    <div class="chart-wrap"><canvas id="notoffer-chart"></canvas></div>
    <div class="row"><div class="tag rec">Recommendation</div>
      <div class="recs">
        <div class="rec-item"><span class="badge start">Start</span><span>Systematically <b>posting the {fmt(notposted)} unmarketed in-stock bags</b> — the single largest, cheapest lever against the {fmt(gap)}-bag target gap.</span></div>
        <div class="rec-item"><span class="badge test">Start testing</span><span>The <b>Kenya posting playbook in {weak_name}</b>, where sales-achieved is {pct(weak_val)} vs Kenya's {pct(ke_mo_mkt)}.</span></div>
        <div class="rec-item"><span class="badge stop">Stop</span><span>Letting <b>in-stock bags sit unposted</b> — every unmarketed bag is a bag that reliably does not sell.</span></div>
      </div></div>
    <div class="row"><div class="tag impact">Business Impact</div>
      <div class="impact"><p>If the <b>{fmt(notposted)} unposted bags</b> converted at even a conservative <b>20%</b> once marketed, that is <b>~{fmt(post_convert)} bags</b> — enough to close <b>~{pct(post_gap_share)} of the entire target gap</b>. Bringing {weak_name} toward Kenya's rate compounds it further.</p></div>
      <div class="assump">Assumes a conservative 20% conversion on newly-posted stock (posted bags ran ~{posting_mult:.1f}× their expected rate, so this is deliberately cautious).</div></div>
  </div>

  <div class="foot">Denri Africa · Marketing Analytics — {month} {year} report. Figures from the live dashboards (Current Performance, New Products, Offer Type Analysis, Posting Yields).</div>

</div>
"""

# ── CHART DATA + SCRIPT ───────────────────────────────────────
_rpt = {
    "cp":   {"sold": total_sales, "gap": gap, "target": total_target, "achievedPct": achieved},
    "np":   {"targets": [{"name": t.get("name", ""), "sold": num(t.get("sold")),
                          "remaining": max(num(t.get("remaining")), 0),
                          "posts": _np_ps.get(str(t.get("name", "")).strip().upper(), {}).get("posts", 0),
                          "stock": _np_ps.get(str(t.get("name", "")).strip().upper(), {}).get("stock", 0)}
                         for t in np_targets]},
    "offer": {"items": [{"name": o["name"], "units": o["units"], "type": "combo"} for o in combo_offers]
                     + [{"name": o["name"], "units": o["units"], "type": "deal"} for o in deal_offers],
              "sinza": [{"name": o["name"], "units": o["units"], "type": "combo"} for o in sz_combos_l]
                     + [{"name": o["name"], "units": o["units"], "type": "single"} for o in sz_singles_l]
                     + [{"name": o["name"], "units": o["units"], "type": "special"} for o in sz_special_l],
              "uganda": [{"name": o["name"], "units": o["units"], "stock": _ug_stock_for(o["name"])} for o in (ug_combos_l + ug_singles_l)]},
    "post": {"ke": ke_mo_mkt, "sz": sz_mo_mkt, "ug": ug_mo_mkt,
             "posted": posted, "notposted": notposted,
             "keNotOffer": ke_notoffer_stock, "szNotOffer": sz_notoffer_stock, "ugNotOffer": ug_notoffer_stock},
}
chart_data = "<script>const RPT = " + json.dumps(_rpt) + ";</script>\n"

chart_js = r"""<script>
(function(){
  if (typeof Chart === 'undefined') return;
  var GRID = 'rgba(45,49,72,0.55)', INK = '#94a3b8';
  function money(n){ return Math.round(n).toLocaleString(); }
  Chart.defaults.font.family = "'Segoe UI', system-ui, sans-serif";
  Chart.defaults.color = INK;

  // Draws each bar's value on the bar (works for stacked segments and grouped bars).
  var VAL = { id:'valLabels', afterDatasetsDraw:function(ch){
    var c = ch.ctx; c.save();
    c.font='700 0.64rem "Segoe UI", system-ui, sans-serif';
    c.textAlign='center'; c.textBaseline='middle';
    c.shadowColor='rgba(0,0,0,0.85)'; c.shadowBlur=3; c.fillStyle='#f8fafc';
    ch.data.datasets.forEach(function(ds, di){
      var meta = ch.getDatasetMeta(di); if (meta.hidden) return;
      meta.data.forEach(function(bar, i){
        var v = ds.data[i]; if (v == null || v < 1) return;
        c.fillText(money(v), (bar.x + bar.base) / 2, bar.y);
      });
    });
    c.restore();
  }};

  // 1. Current Performance — sales vs monthly target (doughnut with centre %)
  (function(){
    var el = document.getElementById('cp-chart'); if (!el) return;
    var centre = { id:'cpCentre', afterDraw:function(ch){
      var a = ch.chartArea, c = ch.ctx;
      c.save(); c.textAlign='center'; c.textBaseline='middle';
      c.fillStyle='#f8fafc'; c.font='800 1.7rem "Segoe UI", system-ui, sans-serif';
      c.fillText((RPT.cp.achievedPct||0).toFixed(2)+'%', (a.left+a.right)/2, (a.top+a.bottom)/2);
      c.restore();
    }};
    new Chart(el, {
      type:'doughnut',
      data:{ labels:['Sold','Remaining'], datasets:[
        { data:[RPT.cp.sold, RPT.cp.gap], backgroundColor:['#34d399','rgba(148,163,184,0.28)'], borderWidth:0 } ] },
      options:{ responsive:true, maintainAspectRatio:false, cutout:'70%',
        plugins:{
          legend:{ position:'bottom', labels:{ boxWidth:12 } },
          tooltip:{ callbacks:{ label:function(c){ return c.label+': '+money(c.parsed)+' bags'; } } }
        }
      },
      plugins:[centre] });
  })();

  // 2. New Products — per product sold vs remaining (stacked)
  (function(){
    var el = document.getElementById('np-chart'); if (!el) return;
    var t = RPT.np.targets || []; if (!t.length){ el.parentNode.style.display='none'; return; }
    new Chart(el, { type:'bar', plugins:[VAL],
      data:{ labels:t.map(function(x){return x.name;}), datasets:[
        { label:'Sold', data:t.map(function(x){return x.sold;}), backgroundColor:'#22d3ee', borderRadius:3 },
        { label:'Remaining to target', data:t.map(function(x){return x.remaining;}), backgroundColor:'rgba(148,163,184,0.35)', borderRadius:3 } ] },
      options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{ position:'bottom', labels:{ boxWidth:12 } } },
        scales:{ x:{ stacked:true, grid:{color:GRID} }, y:{ stacked:true, grid:{display:false} } } } });
  })();

  // 2b. New Products — posts done vs current stock per product (grouped)
  (function(){
    var el = document.getElementById('np-stock-chart'); if (!el) return;
    var t = RPT.np.targets || []; if (!t.length){ el.parentNode.style.display='none'; return; }
    new Chart(el, { type:'bar', plugins:[VAL],
      data:{ labels:t.map(function(x){return x.name;}), datasets:[
        { label:'Stock available', data:t.map(function(x){return x.stock;}), backgroundColor:'#a78bfa', borderRadius:3 },
        { label:'Posts done', data:t.map(function(x){return x.posts;}), backgroundColor:'#22d3ee', borderRadius:3 } ] },
      options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{ position:'bottom', labels:{ boxWidth:12 } },
          tooltip:{ callbacks:{ label:function(c){ return c.dataset.label+': '+money(c.parsed.x); } } } },
        scales:{ x:{ grid:{color:GRID} }, y:{ grid:{display:false} } } } });
  })();

  // 3. Offer Type — each individual offer, units moved, coloured by type
  (function(){
    var el = document.getElementById('offer-chart'); if (!el) return;
    var items = (RPT.offer.items || []).slice().sort(function(a,b){ return b.units - a.units; });
    if (!items.length){ el.parentNode.style.display='none'; return; }
    new Chart(el, { type:'bar',
      data:{ labels:items.map(function(x){return x.name;}), datasets:[
        { label:'Units moved', data:items.map(function(x){return x.units;}),
          backgroundColor:items.map(function(x){ return x.type === 'combo' ? '#f59e0b' : '#a78bfa'; }), borderRadius:3 } ] },
      options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{display:false},
          tooltip:{ callbacks:{ label:function(c){ return money(c.parsed.x)+' units ('+(items[c.dataIndex].type === 'combo' ? 'combo' : 'power deal')+')'; } } } },
        scales:{ x:{ grid:{color:GRID}, ticks:{ callback:function(v){ return money(v); } } },
                 y:{ grid:{display:false}, ticks:{ font:{size:10} } } } } });
  })();

  // 3b. Offer Type — Sinza, EVERY offer coloured by type (all labels shown)
  (function(){
    var el = document.getElementById('offer-sinza-chart'); if (!el) return;
    var items = ((RPT.offer.sinza)||[]).slice().sort(function(a,b){ return b.units - a.units; });
    if (!items.length){ el.parentNode.style.display='none'; return; }
    var col = { combo:'#818cf8', single:'#22d3ee', special:'#f472b6' };
    new Chart(el, { type:'bar', plugins:[VAL],
      data:{ labels:items.map(function(x){return x.name;}), datasets:[
        { label:'Units moved', data:items.map(function(x){return x.units;}),
          backgroundColor:items.map(function(x){ return col[x.type] || '#818cf8'; }), borderRadius:3 } ] },
      options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{display:false},
          tooltip:{ callbacks:{ label:function(c){ return money(c.parsed.x)+' units ('+items[c.dataIndex].type+')'; } } } },
        scales:{ x:{ grid:{color:GRID} },
                 y:{ grid:{display:false}, ticks:{ autoSkip:false, font:{size:11}, color:'#cbd5e1' } } } } });
  })();

  // 3c. Offer Type — Uganda, top 5 + bottom 5 movers, units vs stock
  (function(){
    var el = document.getElementById('offer-uganda-chart'); if (!el) return;
    var all = ((RPT.offer.uganda)||[]).slice().sort(function(a,b){ return b.units - a.units; });
    if (!all.length){ el.parentNode.style.display='none'; return; }
    var rows;
    if (all.length <= 10) { rows = all; }
    else { rows = all.slice(0,5).concat(all.slice(-5)); }
    new Chart(el, { type:'bar', plugins:[VAL],
      data:{ labels:rows.map(function(x){return x.name;}), datasets:[
        { label:'Units moved', data:rows.map(function(x){return x.units;}), backgroundColor:'#34d399', borderRadius:3 },
        { label:'Stock available', data:rows.map(function(x){return x.stock;}), backgroundColor:'#a78bfa', borderRadius:3 } ] },
      options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{ position:'bottom', labels:{ boxWidth:12 } },
          tooltip:{ callbacks:{ label:function(c){ return c.dataset.label+': '+money(c.parsed.x); },
            afterLabel:function(c){ return (all.length > 10 && c.dataIndex < 5) ? 'Top mover' : (all.length > 10 ? 'Least mover' : ''); } } } },
        scales:{ x:{ grid:{color:GRID} },
                 y:{ grid:{display:false}, ticks:{ autoSkip:false, font:{size:11}, color:'#cbd5e1' } } } } });
  })();

  // 4a. Posting — sales-achieved % by region
  (function(){
    var el = document.getElementById('posting-chart'); if (!el) return;
    new Chart(el, { type:'bar',
      data:{ labels:['Kenya','Sinza','Uganda'], datasets:[
        { label:'Sales-achieved %', data:[RPT.post.ke, RPT.post.sz, RPT.post.ug],
          backgroundColor:['#34d399','#818cf8','#fb923c'], borderRadius:4 } ] },
      options:{ responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{display:false},
          tooltip:{ callbacks:{ label:function(c){ return c.parsed.y.toFixed(1)+'% of expected'; } } } },
        scales:{ y:{ beginAtZero:true, grid:{color:GRID}, ticks:{ callback:function(v){ return v+'%'; } } },
                 x:{ grid:{display:false} } } } });
  })();

  // 4b. Posting — posted vs unposted stock (doughnut)
  (function(){
    var el = document.getElementById('stock-chart'); if (!el) return;
    new Chart(el, {
      type:'doughnut',
      data:{ labels:['Posted stock','Unposted (dead) stock'], datasets:[
        { data:[RPT.post.posted, RPT.post.notposted], backgroundColor:['#34d399','#f87171'], borderWidth:0 } ] },
      options:{ responsive:true, maintainAspectRatio:false, cutout:'62%',
        plugins:{
          legend:{ position:'bottom', labels:{ boxWidth:12 } },
          tooltip:{ callbacks:{ label:function(c){ return c.label+': '+money(c.parsed)+' bags'; } } }
        }
      }
    });
  })();

  // 4c. Posting — bags NOT on offer, by region
  (function(){
    var el = document.getElementById('notoffer-chart'); if (!el) return;
    var d = [RPT.post.keNotOffer, RPT.post.szNotOffer, RPT.post.ugNotOffer];
    if (!(d[0] || d[1] || d[2])){ el.parentNode.style.display='none'; return; }
    new Chart(el, { type:'bar',
      data:{ labels:['Kenya','Sinza','Uganda'], datasets:[
        { label:'Not-on-offer stock', data:d, backgroundColor:['#f87171','#fb923c','#facc15'], borderRadius:4 } ] },
      options:{ responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{display:false},
          tooltip:{ callbacks:{ label:function(c){ return money(c.parsed.y)+' bags not on offer'; } } } },
        scales:{ y:{ beginAtZero:true, grid:{color:GRID}, ticks:{ callback:function(v){ return money(v); } } },
                 x:{ grid:{display:false} } } } });
  })();
})();
</script>
"""

_full = head + body + chart_data + chart_js + "\n</body>\n</html>\n"

out = os.path.join(BASE, "monthly_report.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(_full)

# Keep a dated archive so past months are never overwritten.
archive = os.path.join(BASE, f"report_{year}_{month.lower()}.html")
with open(archive, "w", encoding="utf-8") as f:
    f.write(_full)

print(f"monthly_report.html built for {month} {year}.")
print(f"  Target achieved : {pct(achieved)}  ({fmt(total_sales)}/{fmt(total_target)})")
print(f"  Missed by       : {fmt(gap)} bags")
print(f"  Unposted stock  : {fmt(notposted)} ({pct(unposted_pct)})")
print(f"  Weakest region  : {weak_name} ({pct(weak_val)})")
print(f"  Archive         : report_{year}_{month.lower()}.html")
