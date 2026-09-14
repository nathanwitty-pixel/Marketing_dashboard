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
oa   = read_block("self_made_combos.html", "<!-- OFFER_DATA_START -->", "<!-- OFFER_DATA_END -->")
pa   = read_block("POSTING (SALES YIELDS FROM ACCURATE POSTING).html", "<!-- POST_DATA_START -->", "<!-- POST_DATA_END -->")

# Report month + year. The live report always shows the CURRENT month
# (live_anchor), matching the live dashboards — on 1 Sep it is September (day 1),
# not the closed August. A pin (DENRI_REPORT_MONTH, set by month_end.py) points
# it at the exact month being archived instead.
from lib import report_month
_anchor = report_month.live_anchor()
month = gstr(proj, "projMonth") or _anchor.strftime("%B")
year  = _anchor.year

# ── FINALIZED (FROZEN) MONTHS ─────────────────────────────────
# A finalized month's report is STATIC — never regenerated. Its report HTML,
# dated archive and history entry stay exactly as saved, so a later run (or a
# change in the live dashboards) can't overwrite it. Once the reporting month
# rolls forward, the next run generates that new month as a fresh report.
# July and August 2026 are frozen with their final figures.
#
# A DELIBERATE rebuild overrides the freeze: pin the month with
# DENRI_REPORT_MONTH=YYYY-MM and the report regenerates for exactly that month.
# That is the supported way to correct a frozen month (August 2026 was rebuilt
# this way after the report-month anchor bug filled it with September's day-1
# numbers) — an unpinned run can still never touch it.
FINALIZED_MONTHS = {"2026-07", "2026-08"}
import calendar as _cal_fin
_fin_num = (list(_cal_fin.month_name).index(month)
            if month in list(_cal_fin.month_name) else _anchor.month)
_this_key = f"{year}-{_fin_num:02d}"
if _this_key in FINALIZED_MONTHS and not report_month.is_pinned():
    print(f"Monthly report: {month} {year} is finalized (static) — left unchanged.")
    print("  The next reporting month (e.g. September) will generate as a new report.")
    print(f"  To rebuild it deliberately, set {report_month.ENV_VAR}={_this_key} and re-run.")
    raise SystemExit(0)
if _this_key in FINALIZED_MONTHS:
    print(f"Monthly report: REBUILDING finalized month {month} {year} "
          f"({report_month.ENV_VAR} is set) — the frozen figures will be replaced.")

# Previous month's weekly climb, for the History-style comparison overlay on the
# Current Performance chart (this month solid, last month dashed).
_prev_weekly, _prev_label = [], ""
try:
    _pm_num = _fin_num - 1 if _fin_num > 1 else 12
    _pm_year = year if _fin_num > 1 else year - 1
    _pm_key = f"{_pm_year}-{_pm_num:02d}"
    _hist_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "monthly_report_history.json")
    with open(_hist_path, encoding="utf-8") as _pf:
        _pm_snap = json.load(_pf).get(_pm_key)
    if _pm_snap:
        _prev_weekly = [{"label": w.get("label", ""), "pct": num(w.get("pct"))}
                        for w in _pm_snap.get("currentPerformance", {}).get("weekly", [])]
        _prev_label = f"{_pm_snap.get('month', '')} {_pm_snap.get('year', '')}".strip()
except (ValueError, OSError):
    pass

# Net bags sold for master-catalogue products only (KPI), live from Odoo.
_master_bags = None
try:
    from lib import db as _mdb, queries as _mq
    _mw_start = datetime.date(year, _fin_num, 1)
    _mw_end = datetime.date(year, _fin_num, _cal_fin.monthrange(year, _fin_num)[1])
    _mdf = _mdb.run_query(_mq.MASTER_BAGS_SOLD,
                          {"start_date": _mw_start.isoformat(), "end_date": _mw_end.isoformat(),
                           "master": _mq.master_products()})
    if _mdf is not None and not _mdf.empty:
        _master_bags = int(round(float(_mdf.iloc[0]["bags"] or 0)))
except Exception:                                             # noqa: BLE001 — KPI is optional
    _master_bags = None

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

# ── In-progress vs completed month → tense/phrasing ───────────
# When the report is the CURRENT calendar month and today isn't the last day, the
# month is still running, so the report reads "so far" / "is going" instead of the
# past-tense "closed" / "went" used for a completed (archived) month.
_today_rpt = datetime.date.today()
_in_progress = (year == _today_rpt.year and _fin_num == _today_rpt.month
                and _today_rpt.day < _cal_fin.monthrange(year, _fin_num)[1])
_headline_verb = "How the Month Is Going So Far" if _in_progress else "How the Month Went"
if _in_progress:
    _exec_lead = (f"{month} is at <b>{pct(achieved)} of target</b> so far — {fmt(total_sales)} of "
                  f"{fmt(total_target)} bags, <b>{fmt(gap)} bags</b> still to go. The gap so far is not "
                  f"weak demand; it is <b>stock we haven't marketed yet</b>.")
    _cp_lead = (f"So far in {month} we're at <b>{pct(achieved)} of target ({fmt(total_sales)} bags)</b>, "
                f"<b>{fmt(gap)} bags</b> still to go. Weekly output has averaged about <b>{fmt(avg_weekly)} bags</b> "
                f"— under the <b>{fmt(bare_min)}-bag weekly floor</b> the target requires.")
else:
    _exec_lead = (f"{month} closed at <b>{pct(achieved)} of target</b> — {fmt(total_sales)} of "
                  f"{fmt(total_target)} bags, missing by <b>{fmt(gap)} bags</b>. The gap is not weak demand; "
                  f"it is <b>stock we never marketed</b>.")
    _cp_lead = (f"We finished {month} at <b>{pct(achieved)} of target ({fmt(total_sales)} bags)</b>, "
                f"<b>{fmt(gap)} bags short</b>. Weekly output averaged about <b>{fmt(avg_weekly)} bags</b> — "
                f"under the <b>{fmt(bare_min)}-bag weekly floor</b> the target requires.")

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

# ── Timed offers (rendered as their own section after New Products) ──
# Read the campaign payload the Timed Offers page injects (const TO = {...}).
# Kept as a LIST so "every timed offer" can be shown; only campaigns whose
# window falls in THIS report month are included.
def _read_timed_offers():
    blk = read_block("timed_offers.html", "<!-- TIMED_DATA_START -->", "<!-- TIMED_DATA_END -->")
    camps = []
    # New multi-offer payload: const TO_DATA = {"month": ..., "offers": [...]};
    m = re.search(r"const\s+TO_DATA\s*=\s*(\{.*?\})\s*;\s*\r?\n\s*const\s+TO_LIST", blk, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group(1))
            camps = data.get("offers", []) if isinstance(data, dict) else []
        except (ValueError, TypeError):
            camps = []
    else:
        # Back-compat: legacy single payload const TO = {...} (or a bare list).
        m = re.search(r"const\s+TO\s*=\s*(\{.*\}|\[.*\])\s*;", blk, re.DOTALL)
        if not m:
            return []
        try:
            data = json.loads(m.group(1))
        except (ValueError, TypeError):
            return []
        camps = data if isinstance(data, list) else [data]
    month_key = f"{year}-{_fin_num:02d}"
    out = []
    for c in camps:
        if not isinstance(c, dict) or not c.get("bags"):
            continue
        if str(c.get("startDate", ""))[:7] != month_key:   # only this month's campaigns
            continue
        out.append(c)
    return out

timed_offers = _read_timed_offers()

# ── Self-Made Combos (CBR requests) vs running combos ─────────
# Staff-created combos (Odoo pos_combo_request → the CBR/2026 refs) vs the
# official running combos, for the REPORT month, Kenya tills. Queried directly
# (like the master-bags KPI) via self_made_combos.build_payload so it is correct
# whether the report is live or pinned to a past month, and stays in sync with
# the Self-Made Combos page.
def _self_made_combos():
    try:
        from lib import db as _sdb
        from self_made_combos import build_payload as _smc_build
    except Exception:                                            # noqa: BLE001
        return None
    try:
        _s = datetime.date(year, _fin_num, 1)
        _e = datetime.date(year, _fin_num, _cal_fin.monthrange(year, _fin_num)[1])
        ok, _ = _sdb.check_connection()
        if not ok:
            return None
        return _smc_build(_s, _e)
    except Exception:                                            # noqa: BLE001 — section is optional
        return None

self_made = _self_made_combos()

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
    """Parse an offer table (Kenya combos/deals, Sinza, Uganda) → [{name, units, price}].

    Robust to the offer sheet's shifting column order (the reason August's units
    came out as prices). The units-moved figure is the sum of the weekly 'Wk N'
    columns (bags moved), never a price column:
      • price  = a header containing 'price' (the non-TSH one first);
      • units  = Σ of the 'Wk N' / week columns; falling back to a
                 'total'/'units'/'moved'/'sold' column, then to the last
                 non-name, non-price column — but a price column is NEVER read
                 as units."""
    headers = headers or []
    low = [str(h).lower().strip() for h in headers]
    iprice = next((i for i, h in enumerate(low) if "price" in h and "tsh" not in h), -1)
    if iprice < 0:
        iprice = next((i for i, h in enumerate(low) if "price" in h), -1)
    price_cols = {i for i, h in enumerate(low) if "price" in h}          # every price column (incl. TSH)
    wk_cols    = [i for i, h in enumerate(low) if i != 0 and i not in price_cols and ("wk" in h or "week" in h)]
    tot_cols   = [i for i, h in enumerate(low) if i != 0 and i not in price_cols
                  and any(k in h for k in ("total", "unit", "moved", "sold"))]
    other_cols = [i for i in range(len(low)) if i != 0 and i not in price_cols]

    def _units(r):
        cols = wk_cols or tot_cols[:1] or other_cols[-1:]
        return sum(num(r[i]) for i in cols if 0 <= i < len(r))

    out = []
    for r in (rows or []):
        if not r:
            continue
        name = str(r[0]).strip()
        if not name or "total" in name.lower():
            continue
        price = num(r[iprice]) if 0 <= iprice < len(r) else 0
        out.append({"name": name, "units": _units(r), "price": price})
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
# The momentum card compares THIS month's pace vs last month's. For a live,
# in-progress month that's "Momentum in September (so far)" labelled "Sep:", not
# "into October"/"Oct:" — that framing only fits an already-completed month.
_mom_title = (f"{month} momentum so far" if _in_progress else f"Momentum into {next_month}")
_mom_short = (month[:3] if _in_progress else next_short)
growth_pct_txt  = gstr(perf, "weeklySalesPct")    or ""   # e.g. "19.73%"
prev_pct_txt    = gstr(perf, "previousSalesPct")  or ""   # e.g. "52.07%"
prev_bags_txt   = gstr(perf, "previousSalesBags") or ""   # e.g. "4,584"
# Weekly performance line: each week's OWN % of target = cumulative − previous cumulative.
wk_series = []
_prevc = 0.0
for _w in garr(proj, "weeklyHistory"):
    _cum = num(_w.get("salesPct"))
    wk_series.append({"label": str(_w.get("label") or ""),
                      "pct":  round(_cum - _prevc, 2),        # this week's own contribution
                      "cum":  round(_cum, 2),                 # cumulative to date
                      "bags": num(_w.get("weeklySales"))})    # weekly sales (bags)
    _prevc = _cum

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

  /* ── Consistency with the other pages: reduced-motion, flat accent, glass, aura ── */
  @media (prefers-reduced-motion: reduce){
    *,*::before,*::after{ transition-duration:.12s!important; transition-property:opacity!important;
      animation-duration:.01ms!important; animation-iteration-count:1!important; scroll-behavior:auto!important; }
  }
  .rpt-pill{ background:#8b5cf6 !important; }              /* flat accent (was a gradient) */
  .exec, .kpi, .sec{ border-radius:10px !important; }
  /* Frosted-glass card surfaces — the aura shows through */
  .exec, .kpi, .sec, .mini{
    background-color:rgba(24,27,40,0.52) !important; background-image:none !important;
    backdrop-filter:blur(14px) saturate(1.08); -webkit-backdrop-filter:blur(14px) saturate(1.08); }
  @media (prefers-reduced-transparency: reduce){
    .exec, .kpi, .sec, .mini{ background-color:#141824 !important; backdrop-filter:none; -webkit-backdrop-filter:none; } }
  /* Spectral Edge aura backdrop (decorative, fixed, behind all content) */
  body{ background-color:#100e0b; }
  .aura-layer-1,.aura-layer-2,.aura-layer-3{ position:fixed; inset:0; z-index:-1; pointer-events:none; transform:translateZ(0); will-change:transform; }
  .aura-layer-1{ mix-blend-mode:screen; filter:blur(108px); background:linear-gradient(90deg, transparent 0%, rgba(59,130,246,0.04) 32%, rgba(6,182,212,0.12) 45%, rgba(34,197,94,0.13) 51%, rgba(250,204,21,0.12) 57%, rgba(244,63,94,0.11) 64%, transparent 82%); }
  .aura-layer-2{ mix-blend-mode:screen; filter:blur(58px); opacity:0.24; background:linear-gradient(102deg, transparent 38%, rgba(255,255,255,0.08) 46%, rgba(125,211,252,0.06) 51%, transparent 60%); }
  .aura-layer-3{ mix-blend-mode:screen; filter:blur(126px); opacity:0.55; background:radial-gradient(ellipse 25% 65% at 92% 50%, rgba(139,92,246,0.16) 0%, transparent 78%); }
  @media (max-width:640px){ .aura-layer-1{ filter:blur(75px);} .aura-layer-2{ filter:blur(40px);} .aura-layer-3{ filter:blur(88px);} }
</style>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
<div class="aura-layer-1" aria-hidden="true"></div>
<div class="aura-layer-2" aria-hidden="true"></div>
<div class="aura-layer-3" aria-hidden="true"></div>
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
        f'<div class="row"><div class="tag" style="color:#38bdf8">{esc(_mom_title)}</div>'
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
        f'<div style="font-size:0.8rem;color:#93c5fd;line-height:1.5">{esc(_mom_short)}: {fmt(w_this)} in {int(w_days)} day{_pl} ({fmt(next_per_day)}/day) vs {esc(p_label)}: {fmt(p_weekly)} in {int(p_days)} days ({fmt(prev_per_day)}/day)</div>'
        '<div style="font-size:0.72rem;color:#64748b;margin-top:0.5rem">This month&rsquo;s per-day pace vs last month&rsquo;s final-week pace. Above 1&times; means this month is outrunning how last month closed.</div>'
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

# ── Timed Offers section (inserted after New Products) ────────
def _pp_txt(v):
    return f"{v:.1f}" if isinstance(v, (int, float)) else "—"

timed_offers_section = ""
if timed_offers:
    _to_parts = []
    for _i, _c in enumerate(timed_offers):
        _bags   = _c.get("bags", [])
        _sold   = int(num(_c.get("totalSold")))
        _posts  = int(num(_c.get("totalPosts")))
        _pp     = _pp_txt(_c.get("perPost"))
        _win    = esc(_c.get("windowLabel", ""))
        _mkt    = esc(_c.get("market", "Kenya"))
        _best   = esc(_c.get("bestName", ""))
        _bsold  = int(num(_c.get("bestSold")))
        _name   = esc(_c.get("name", "")) or "Timed Offer"
        _lift   = _c.get("lift") or {}
        _lpct   = _lift.get("liftPct")
        _lup    = isinstance(_lpct, (int, float)) and _lpct >= 0
        _lift_kpi = (
            f'<span><b style="color:{"#34d399" if _lup else "#f87171"};font-size:1.15rem">'
            f'{"+" if _lup else ""}{_lpct}%</b> sales lift</span>'
            if _lpct is not None else '')
        _lift_block = ""
        if _lift.get("daily"):
            _lift_block = (
                f'<div class="chart-cap" style="margin-top:1rem">Did it lift sales? Daily bags — pre-offer (grey) vs offer window (green), '
                f'{_lift.get("basePerDay")}/day → {_lift.get("offerPerDay")}/day</div>'
                f'<div class="chart-wrap" style="height:230px"><canvas id="to-lift-{_i}"></canvas></div>')
        _week_block = ""
        if _lift.get("weekly"):
            _week_block = (
                '<div class="chart-cap" style="margin-top:1rem">Week by week — bags/day for the 6 bags (offer week in green)</div>'
                f'<div class="chart-wrap" style="height:220px"><canvas id="to-week-{_i}"></canvas></div>')
        _why    = _c.get("why") or {}
        _wins   = _why.get("insights", [])
        _verdict = _why.get("verdict", "")
        _why_rows = "".join(
            f'<div class="row"><div class="tag insight">{esc(x.get("tag",""))}</div><p>{x.get("text","")}</p></div>'
            for x in _wins)
        _verdict_box = (
            '<div style="margin-top:0.6rem;padding:0.85rem 1rem;background:rgba(245,158,11,0.08);'
            'border:1px solid rgba(245,158,11,0.28);border-radius:10px;color:#e2e8f0;font-size:0.9rem;line-height:1.55">'
            f'{_verdict}</div>' if _verdict else '')
        _zeros  = [esc(b.get("name", "")) for b in _bags
                   if not b.get("posts") and num(b.get("sold")) > 0]
        _rows = "".join(
            f'<tr><td style="padding:0.45rem 0.7rem;border-top:1px solid #262a3d;color:#f1f5f9;font-weight:600">{esc(b.get("name",""))}</td>'
            f'<td style="padding:0.45rem 0.7rem;border-top:1px solid #262a3d;text-align:right;color:#e2e8f0">{fmt(num(b.get("sold")))}</td>'
            f'<td style="padding:0.45rem 0.7rem;border-top:1px solid #262a3d;text-align:right;color:{"#f87171" if not b.get("posts") else "#e2e8f0"};font-weight:{"700" if not b.get("posts") else "400"}">{fmt(num(b.get("posts")))}</td>'
            f'<td style="padding:0.45rem 0.7rem;border-top:1px solid #262a3d;text-align:right;color:#94a3b8">{_pp_txt(b.get("perPost"))}</td></tr>'
            for b in _bags)
        _insight = (f'<b>{" and ".join(_zeros)}</b> sold with <b>0 recorded posts</b> — moving without marketing. '
                    if _zeros else '')

        # ── "Why these bags" table (price from Odoo incl-tax · discount · lift · stock) ──
        _wb = _why.get("bags", [])
        _th = ('style="text-align:{a};padding:0.45rem 0.7rem;font-size:0.66rem;'
               'text-transform:uppercase;letter-spacing:0.06em;color:#64748b;border-bottom:1px solid #2d3148"')
        def _cell(txt, extra=""):
            return f'<td style="padding:0.45rem 0.7rem;border-top:1px solid #262a3d;{extra}">{txt}</td>'
        _why_table = ""
        if _wb:
            _wh = ("<tr>"
                   + f'<th {_th.format(a="left")}>Bag</th>'
                   + f'<th {_th.format(a="right")}>Sold</th>'
                   + f'<th {_th.format(a="right")}>In stock</th>'
                   + f'<th {_th.format(a="right")}>Price was</th>'
                   + f'<th {_th.format(a="right")}>Price now</th>'
                   + f'<th {_th.format(a="right")}>Discount</th>'
                   + f'<th {_th.format(a="right")}>Sales lift</th>'
                   + f'<th {_th.format(a="left")}>Category</th></tr>')
            _wbody = ""
            for b in _wb:
                _dk = num(b.get("discountKes"))
                _disc = (f'<span style="color:#34d399;font-weight:700">&minus;{fmt(_dk)}</span> '
                         f'<span style="color:#94a3b8;font-size:0.72rem">({b.get("discountPct")}%)</span>'
                         if _dk else '<span style="color:#64748b">&mdash;</span>')
                _bl = b.get("bagLift")
                _lift = ('<span style="color:#64748b">&mdash;</span>' if _bl is None
                         else f'<span style="color:{"#34d399" if _bl >= 0 else "#f87171"};font-weight:700">'
                              f'{"+" if _bl >= 0 else ""}{_bl}%</span>')
                _was = f'KES {fmt(num(b.get("priceWas")))}' if b.get("priceWas") is not None else '&mdash;'
                _now = f'KES {fmt(num(b.get("priceNow")))}' if b.get("priceNow") is not None else '&mdash;'
                _wbody += ("<tr>"
                    + _cell(esc(b.get("name", "")), "color:#f1f5f9;font-weight:600")
                    + _cell(fmt(num(b.get("sold"))), "text-align:right;color:#e2e8f0")
                    + _cell(fmt(num(b.get("stock"))), "text-align:right;color:#94a3b8")
                    + _cell(_was, "text-align:right;color:#94a3b8")
                    + _cell(_now, "text-align:right;color:#34d399")
                    + _cell(_disc, "text-align:right")
                    + _cell(_lift, "text-align:right")
                    + _cell(esc(b.get("category", "")), "color:#94a3b8") + "</tr>")
            _why_table = (
                '<div class="chart-cap" style="margin-top:1rem">Why these bags — price (Odoo, incl-tax), discount &amp; each bag\'s own sales lift</div>'
                '<table style="width:100%;border-collapse:collapse;font-size:0.82rem;margin-top:0.4rem">'
                '<thead>' + _wh + '</thead><tbody>' + _wbody + '</tbody></table>')

        # ── "Price week by week" matrix (realised avg vs list/offer) ──
        _pw = _why.get("priceWeeks") or {}
        _pw_wks = _pw.get("weeks", [])
        _pw_table = ""
        if _pw.get("bags") and _pw_wks:
            _offbg = "background:rgba(16,185,129,0.10);"
            _pth = 'text-align:right;padding:0.4rem 0.6rem;font-size:0.64rem;text-transform:uppercase;color:#64748b;border-bottom:1px solid #2d3148'
            _ph = ('<tr><th style="text-align:left;padding:0.4rem 0.6rem;font-size:0.64rem;text-transform:uppercase;'
                   'color:#64748b;border-bottom:1px solid #2d3148">Bag</th>')
            for _w in _pw_wks:
                _st = _pth + (";" + _offbg + "color:#34d399" if _w.get("off") else "")
                _ph += f'<th style="{_st}" title="{esc(_w.get("start",""))} &rarr; {esc(_w.get("end",""))}">{esc(_w.get("label",""))}{" &middot;offer" if _w.get("off") else ""}</th>'
            _ph += f'<th style="{_pth}">Was</th><th style="{_pth}">Now</th></tr>'
            _pbody = ""
            for b in _pw["bags"]:
                _wv, _nv = num(b.get("was")), num(b.get("now"))
                _prow = ('<td style="padding:0.4rem 0.6rem;border-top:1px solid #262a3d;color:#f1f5f9;font-weight:600">'
                         + esc(b.get("name", "")) + '</td>')
                for _i2, _c in enumerate(b.get("cells", [])):
                    _off = _pw_wks[_i2].get("off") if _i2 < len(_pw_wks) else False
                    _bg = _offbg if _off else ""
                    _avg = _c.get("avg")
                    if _avg is None:
                        _prow += f'<td style="padding:0.4rem 0.6rem;border-top:1px solid #262a3d;text-align:right;color:#475569;{_bg}">&mdash;</td>'
                    else:
                        _col = "#94a3b8"
                        if _nv and _avg <= _nv * 1.03:
                            _col = "#34d399"
                        elif _wv and _avg < _wv * 0.97:
                            _col = "#fbbf24"
                        _prow += (f'<td style="padding:0.4rem 0.6rem;border-top:1px solid #262a3d;text-align:right;{_bg}">'
                                  f'<span style="color:{_col};font-weight:700">{fmt(_avg)}</span> '
                                  f'<span style="color:#64748b;font-size:0.68rem">({fmt(num(_c.get("qty")))})</span></td>')
                _prow += f'<td style="padding:0.4rem 0.6rem;border-top:1px solid #262a3d;text-align:right;color:#94a3b8">{fmt(_wv) if _wv else "&mdash;"}</td>'
                _prow += f'<td style="padding:0.4rem 0.6rem;border-top:1px solid #262a3d;text-align:right;color:#34d399">{fmt(_nv) if _nv else "&mdash;"}</td>'
                _pbody += "<tr>" + _prow + "</tr>"
            _pw_table = (
                '<div class="chart-cap" style="margin-top:1.1rem">Price week by week &mdash; realised avg price per bag '
                '(incl-tax; units in parens). <span style="color:#34d399">green</span> = at/below offer, '
                '<span style="color:#94a3b8">grey</span> &asymp; full, <span style="color:#fbbf24">amber</span> = part-way. Offer week highlighted.</div>'
                '<table style="width:100%;border-collapse:collapse;font-size:0.8rem;margin-top:0.4rem">'
                '<thead>' + _ph + '</thead><tbody>' + _pbody + '</tbody></table>')

        _to_parts.append(f"""
    <div style="font-size:1.05rem;font-weight:700;color:#fbbf24;margin:0.2rem 0 0.15rem">{_name}</div>
    <div class="chart-cap">{_win} · {_mkt} · sales from Odoo (exact window) · posting = last week (Kenya)</div>
    <div style="display:flex;gap:1.6rem;flex-wrap:wrap;margin:0 0 0.9rem;font-size:0.9rem;color:#cbd5e1">
      <span><b style="color:#34d399;font-size:1.15rem">{fmt(_sold)}</b> bags sold</span>
      <span><b style="color:#22d3ee;font-size:1.15rem">{fmt(_posts)}</b> Kenya posts</span>
      <span><b style="color:#a78bfa;font-size:1.15rem">{_pp}</b> bags/post</span>
      {_lift_kpi}
      <span>Top seller: <b>{_best}</b> ({fmt(_bsold)})</span>
    </div>
    {_lift_block}
    {_week_block}
    <div class="chart-cap">Each bag — bags sold (Odoo, {_win})</div>
    <div class="chart-wrap" style="height:300px"><canvas id="to-chart-{_i}"></canvas></div>
    <table style="width:100%;border-collapse:collapse;font-size:0.84rem;margin-top:0.6rem">
      <thead><tr>
        <th style="text-align:left;padding:0.45rem 0.7rem;font-size:0.66rem;text-transform:uppercase;letter-spacing:0.06em;color:#64748b;border-bottom:1px solid #2d3148">Bag</th>
        <th style="text-align:right;padding:0.45rem 0.7rem;font-size:0.66rem;text-transform:uppercase;letter-spacing:0.06em;color:#64748b;border-bottom:1px solid #2d3148">Bags sold</th>
        <th style="text-align:right;padding:0.45rem 0.7rem;font-size:0.66rem;text-transform:uppercase;letter-spacing:0.06em;color:#64748b;border-bottom:1px solid #2d3148">Posts</th>
        <th style="text-align:right;padding:0.45rem 0.7rem;font-size:0.66rem;text-transform:uppercase;letter-spacing:0.06em;color:#64748b;border-bottom:1px solid #2d3148">Sold/post</th>
      </tr></thead>
      <tbody>{_rows}</tbody>
    </table>
    {_why_table}
    {_pw_table}
    <div style="margin-top:0.9rem"></div>
    {_why_rows}
    {_verdict_box}""")
    timed_offers_section = (
        '\n  <div class="sec">\n'
        '    <div class="sec-head"><div class="sec-num" style="background:#f59e0b">★</div><h2>Timed Offers</h2></div>'
        + "".join(_to_parts) +
        '\n  </div>'
    )

# ── Self-Made Combos section (staff CBR combos vs running combos) ──
self_made_section = ""
if self_made and (self_made.get("smTotals", {}).get("count") or self_made.get("reqTotal")):
    _sm = self_made["smTotals"]; _run = self_made["runTotals"]
    _rc = self_made.get("reqCounts", {})
    _tot_units = _sm["units"] + _run["units"]
    _sm_share = (_sm["units"] / _tot_units * 100) if _tot_units else 0
    _sm_avg = (_sm["value"] / _sm["units"]) if _sm["units"] else 0
    _run_avg = (_run["value"] / _run["units"]) if _run["units"] else 0
    _reqs = self_made.get("requests", [])
    _rej = [r for r in _reqs if r["state"] in ("rejected", "reject")]

    # KPI chips
    _smc_kpis = (
        '<div style="display:flex;gap:1.6rem;flex-wrap:wrap;margin:0 0 1rem;font-size:0.9rem;color:#cbd5e1">'
        f'<span><b style="color:#fbbf24;font-size:1.15rem">{fmt(_sm["units"])}</b> self-made units ({fmt(_sm["count"])} combos)</span>'
        f'<span><b style="color:#22d3ee;font-size:1.15rem">{fmt(_run["units"])}</b> running units ({fmt(_run["count"])} combos)</span>'
        f'<span><b style="color:#a78bfa;font-size:1.15rem">{_sm_share:.0f}%</b> self-made share</span>'
        f'<span><b style="color:#e2e8f0;font-size:1.15rem">{fmt(self_made.get("reqTotal", 0))}</b> requests '
        f'({fmt(_rc.get("approved",0))} approved · {fmt(_rc.get("rejected",0))} rejected'
        + (f' · {fmt(_rc.get("pending",0))} pending' if _rc.get("pending") else '') + ')</span>'
        '</div>'
    )

    # Self-made vs running summary table
    def _smc_srow(lbl, colour, d, avg):
        return (f'<tr><td style="padding:0.45rem 0.7rem;border-top:1px solid #262a3d;color:{colour};font-weight:700">{lbl}</td>'
                f'<td style="padding:0.45rem 0.7rem;border-top:1px solid #262a3d;text-align:right;color:#e2e8f0">{fmt(d["count"])}</td>'
                f'<td style="padding:0.45rem 0.7rem;border-top:1px solid #262a3d;text-align:right;color:#e2e8f0">{fmt(d["units"])}</td>'
                f'<td style="padding:0.45rem 0.7rem;border-top:1px solid #262a3d;text-align:right;color:#e2e8f0">{fmt(d["value"])}</td>'
                f'<td style="padding:0.45rem 0.7rem;border-top:1px solid #262a3d;text-align:right;color:#94a3b8">{fmt(avg)}</td>'
                f'<td style="padding:0.45rem 0.7rem;border-top:1px solid #262a3d;text-align:right;color:#94a3b8">{d.get("avgColours", 0):g}</td></tr>')
    _th_smc = ('style="text-align:{a};padding:0.45rem 0.7rem;font-size:0.66rem;text-transform:uppercase;'
               'letter-spacing:0.06em;color:#64748b;border-bottom:1px solid #2d3148"')
    _smc_summary = (
        '<div class="chart-cap">Self-made vs running — combos, units, revenue, avg price &amp; colour range</div>'
        '<table style="width:100%;border-collapse:collapse;font-size:0.84rem;margin-bottom:0.4rem">'
        '<thead><tr>'
        f'<th {_th_smc.format(a="left")}>Type</th>'
        f'<th {_th_smc.format(a="right")}>Combos</th>'
        f'<th {_th_smc.format(a="right")}>Units</th>'
        f'<th {_th_smc.format(a="right")}>Revenue (KES)</th>'
        f'<th {_th_smc.format(a="right")}>Avg price</th>'
        f'<th {_th_smc.format(a="right")}>Avg colours</th>'
        '</tr></thead><tbody>'
        + _smc_srow('Self-made (CBR)', '#fbbf24', _sm, _sm_avg)
        + _smc_srow('Running (official)', '#22d3ee', _run, _run_avg)
        + '</tbody></table>'
    )

    _cheaper = "self-made" if _sm_avg <= _run_avg else "running"
    _rej_note = (f' {len(_rej)} request(s) were rejected'
                 + (f' (e.g. {esc(_rej[0]["cbr"])} — {esc(_rej[0]["reject"])})' if _rej and _rej[0].get("reject") else '')
                 + '.') if _rej else ''
    self_made_section = f"""
  <div class="sec">
    <div class="sec-head"><div class="sec-num" style="background:#fbbf24">◆</div><h2>Self-Made Combos</h2></div>
    <p style="font-size:0.86rem;color:#94a3b8;margin-bottom:0.9rem">Staff often build their own combos on the POS (a <b>Combo Request</b> &mdash; the CBR/2026 refs) instead of pushing the month&rsquo;s official running combos. Each self-made combo is matched to its real CBR request via <code style="color:#94a3b8">combo_product_id</code>. Kenya tills.</p>
    {_smc_kpis}
    {_smc_summary}
    <div class="row" style="margin-top:1rem"><div class="tag bottom">The Bottom Line</div>
      <p>Staff-made combos were <b>{fmt(_sm["count"])} combos moving {fmt(_sm["units"])} units</b> (KES {fmt(_sm["value"])}) — <b>{_sm_share:.0f}% of all combo volume</b> — vs <b>{fmt(_run["count"])} official running combos moving {fmt(_run["units"])} units</b> (KES {fmt(_run["value"])}). {fmt(self_made.get("reqTotal",0))} combo requests were logged this month.{_rej_note}</p></div>
    <div class="row"><div class="tag insight">The Insight</div>
      <p>Self-made combos average <b>KES {fmt(_sm_avg)}</b> vs running combos <b>KES {fmt(_run_avg)}</b>, so the <b>{_cheaper}</b> combos are the cheaper ticket. Every self-made combo needs an approved CBR, so the request table behind them is the audit trail — who requested what, from which shop, and whether it actually sold.</p>
      <p style="margin-top:0.5rem">The split also shows up at the till: an <b>official running combo offers a wide colour range</b> for the attendant to pick from (avg <b>{_run.get("avgColours",0):g} colour options</b>), while a <b>self-made combo is locked to one specific pairing</b> (avg <b>{_sm.get("avgColours",0):g}</b>) — the same divide the CBR link draws, from the shop floor’s point of view.</p></div>
  </div>"""

body = f"""
  <div class="rpt-head">
    <span class="rpt-pill">Monthly Report</span>
    <h1>{month} {year} — {_headline_verb}</h1>
    <div class="dek">Current Performance · New Products · Offer Type Analysis · Self-Made Combos · Posting Yields</div>
  </div>

  <div class="exec">
    <div class="lbl">The Bottom Line</div>
    <div class="headline">
      {_exec_lead}
    </div>
    <ul>
      <li><b>{pct(unposted_pct)} of Kenya stock ({fmt(notposted)} bags) was never posted</b> — yet posted bags sold at {pct(ke_mo_mkt)} of expectation. Marketing is the lever, and much of it went unused.</li>
      <li><b>Weekly output (~{fmt(avg_weekly)} bags) ran below the {fmt(bare_min)}/week floor</b> needed to hit target — the problem is consistency, not a bad month.</li>
      <li><b>Regions are uneven:</b> Kenya posts at {pct(ke_mo_mkt)} sales-achieved, Sinza {pct(sz_mo_mkt)}, Uganda {pct(ug_mo_mkt)}. The Kenya playbook isn't being run elsewhere.</li>
    </ul>
  </div>

  <div class="kpis">
    <div class="kpi" style="align-items:stretch"><div class="k-lbl">Sales vs Monthly Target</div><div style="position:relative;height:150px;margin-top:0.35rem"><canvas id="kpi-target-donut"></canvas></div><div class="k-sub" style="text-align:center">{fmt(total_sales)} / {fmt(total_target)} bags</div></div>
    <div class="kpi"><div class="k-lbl">Missed By</div><div class="k-val red">{fmt(gap)}</div><div class="k-sub">bags short of target</div></div>
    <div class="kpi"><div class="k-lbl">Unmarketed Stock</div><div class="k-val red">{fmt(notposted)}</div><div class="k-sub">{pct(unposted_pct)} of Kenya stock not posted &middot; {fmt(mo_posts_made)} posts made this month</div></div>
    <div class="kpi"><div class="k-lbl">Posting Sales-Achieved</div><div class="k-val green">{pct(ke_mo_mkt)}</div><div class="k-sub">Kenya {pct(ke_mo_mkt)} &middot; Sinza {pct(sz_mo_mkt)} &middot; Uganda {pct(ug_mo_mkt)} (of expected)</div></div>
    <div class="kpi"><div class="k-lbl">Net Bags Sold &middot; Catalogue</div><div class="k-val cyan">{fmt(_master_bags) if _master_bags is not None else '&mdash;'}</div><div class="k-sub">net of refunds &middot; master-list products only</div></div>
  </div>

  <div class="sec">
    <div class="sec-head"><div class="sec-num" style="background:#facc15">1</div><h2>Current Performance</h2></div>
    <div class="chart-cap">Weekly performance — Week 1 to latest (each week's % of target)</div>
    <div class="chart-wrap" style="height:240px"><canvas id="cp-chart"></canvas></div>
    <div style="display:flex;flex-wrap:wrap;gap:0.35rem 2rem;justify-content:center;font-size:0.8rem;color:#94a3b8;margin:0 0 1.1rem">
      <span>Growth % towards achieved monthly sales: <b style="color:#fbbf24">{growth_pct_txt}</b></span>
      <span>Previous sales % achieved: <b style="color:#fbbf24">{prev_pct_txt} ({prev_bags_txt} bags)</b></span>
    </div>
    <div class="row"><div class="tag bottom">The Bottom Line</div>
      <p>{_cp_lead}</p></div>
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
    <div style="display:flex;justify-content:flex-end;align-items:center;gap:0.45rem;margin:0 0 0.5rem;font-size:0.72rem;color:#64748b">
      <span style="text-transform:uppercase;letter-spacing:0.06em">Sort</span>
      <select id="np-sort" style="background:#1e2130;border:1px solid #2d3148;color:#e2e8f0;padding:0.28rem 0.55rem;border-radius:6px;font-size:0.75rem;cursor:pointer;outline:none">
        <option value="sold-desc">Sold — high to low</option>
        <option value="sold-asc">Sold — low to high</option>
        <option value="remaining-desc">Still needed — high to low</option>
        <option value="stock-desc">Stock — high to low</option>
        <option value="posts-desc">Posts — high to low</option>
      </select>
    </div>
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
{timed_offers_section}
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
{self_made_section}
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

# ── Per-bag stock lookup (for the combo hover — which components hold most stock) ──
_ke_stock_by_bag = {}
for _s in garr(oa, "stockData"):
    _bt = str(_s.get("bagType", "")).strip().upper()
    if _bt:
        _ke_stock_by_bag[_bt] = _ke_stock_by_bag.get(_bt, 0) + num(_s.get("kenyaStock"))
_sz_stock_by_bag = {}
for _s in garr(oa, "sinzaStockData"):
    _bt = str(_s.get("bagType", "")).strip().upper()
    if _bt:
        _sz_stock_by_bag[_bt] = _sz_stock_by_bag.get(_bt, 0) + num(_s.get("sinzaStock"))


def _norm_bag(s):
    """Space/punctuation-insensitive key so 'MINIZURI' matches 'MINI ZURI'."""
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def _bag_stock(part, smap):
    pu = str(part).strip().upper()
    if pu in smap:
        return smap[pu]
    pn = _norm_bag(part)
    if not pn:
        return None
    for _k, _v in smap.items():                 # match ignoring spacing/punctuation,
        kn = _norm_bag(_k)                       # then prefix (e.g. "STANDARD" ~ "STANDARD TRAVEL")
        if kn == pn or kn.startswith(pn) or pn.startswith(kn):
            return _v
    return None


def _combo_bags(name, smap):
    """Component bags of an offer, each with its stock, sorted most-stock first."""
    seen, out = set(), []
    for p in [x.strip() for x in re.split(r"[/+&]", str(name)) if x.strip()]:
        if p.upper() in seen:
            continue
        seen.add(p.upper())
        out.append({"name": p, "stock": _bag_stock(p, smap)})
    out.sort(key=lambda x: (x["stock"] is None, -(x["stock"] or 0)))
    return out


# ── CHART DATA + SCRIPT ───────────────────────────────────────
_rpt = {
    "cp":   {"sold": total_sales, "gap": gap, "target": total_target, "achievedPct": achieved,
             "weekly": wk_series, "prevWeekly": _prev_weekly, "prevLabel": _prev_label,
             "curLabel": f"{month} {year}"},
    "np":   {"targets": [{"name": t.get("name", ""), "sold": num(t.get("sold")),
                          "remaining": max(num(t.get("remaining")), 0),
                          "posts": _np_ps.get(str(t.get("name", "")).strip().upper(), {}).get("posts", 0),
                          "stock": _np_ps.get(str(t.get("name", "")).strip().upper(), {}).get("stock", 0)}
                         for t in np_targets]},
    "offer": {"items": [{"name": o["name"], "units": o["units"], "type": "combo", "bags": _combo_bags(o["name"], _ke_stock_by_bag)} for o in combo_offers]
                     + [{"name": o["name"], "units": o["units"], "type": "deal", "bags": _combo_bags(o["name"], _ke_stock_by_bag)} for o in deal_offers],
              "sinza": [{"name": o["name"], "units": o["units"], "type": "combo", "bags": _combo_bags(o["name"], _sz_stock_by_bag)} for o in sz_combos_l]
                     + [{"name": o["name"], "units": o["units"], "type": "single", "bags": _combo_bags(o["name"], _sz_stock_by_bag)} for o in sz_singles_l]
                     + [{"name": o["name"], "units": o["units"], "type": "special", "bags": _combo_bags(o["name"], _sz_stock_by_bag)} for o in sz_special_l],
              "uganda": [{"name": o["name"], "units": o["units"], "stock": _ug_stock_for(o["name"])} for o in (ug_combos_l + ug_singles_l)]},
    "post": {"ke": ke_mo_mkt, "sz": sz_mo_mkt, "ug": ug_mo_mkt,
             "posted": posted, "notposted": notposted,
             "keNotOffer": ke_notoffer_stock, "szNotOffer": sz_notoffer_stock, "ugNotOffer": ug_notoffer_stock},
    "timed": timed_offers,
}
chart_data = "<script>const RPT = " + json.dumps(_rpt, separators=(",", ":")) + ";</script>\n"

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

  // Doughnut centre-% plugin, reused by the KPI target tile.
  function donutCentre(sizeRem){
    return { id:'donutCentre', afterDraw:function(ch){
      var a = ch.chartArea, c = ch.ctx;
      c.save(); c.textAlign='center'; c.textBaseline='middle';
      c.fillStyle='#f8fafc'; c.font='800 '+sizeRem+'rem "Segoe UI", system-ui, sans-serif';
      c.fillText((RPT.cp.achievedPct||0).toFixed(2)+'%', (a.left+a.right)/2, (a.top+a.bottom)/2);
      c.restore();
    }};
  }
  // Draws the % above each line point.
  var LINEVAL = { id:'lineVals', afterDatasetsDraw:function(ch){
    var c = ch.ctx, ds = ch.data.datasets[0]; if (!ds) return;
    c.save(); c.font='700 0.66rem "Segoe UI", system-ui, sans-serif';
    c.textAlign='center'; c.textBaseline='bottom'; c.fillStyle='#fde68a';
    c.shadowColor='rgba(0,0,0,0.75)'; c.shadowBlur=3;
    ch.getDatasetMeta(0).data.forEach(function(pt,i){ c.fillText((ds.data[i]).toFixed(1)+'%', pt.x, pt.y-7); });
    c.restore();
  }};
  // Week-on-week growth badge (last two weeks) — like the dashboard.
  var WOW = { id:'wowBadge', afterDraw:function(ch){
    var w = RPT.cp.weekly || []; if (w.length < 2) return;
    var n = w.length, g = w[n-1].pct - w[n-2].pct, up = g >= 0;
    var c = ch.ctx, ca = ch.chartArea;
    var txt = 'Week-on-week growth: ' + (up ? '+' : '') + g.toFixed(2) + ' pts';
    var sub = w[n-2].label + ' → ' + w[n-1].label;
    c.save();
    c.font = '700 0.72rem "Segoe UI", system-ui, sans-serif';
    var bw = Math.max(c.measureText(txt).width, c.measureText(sub).width) + 24, bh = 38;
    var x = ca.left + 6, y = ca.top + 4;
    c.fillStyle = up ? 'rgba(16,185,129,0.16)' : 'rgba(239,68,68,0.16)';
    c.strokeStyle = up ? '#34d399' : '#f87171'; c.lineWidth = 1;
    c.beginPath();
    if (c.roundRect) c.roundRect(x, y, bw, bh, 8); else c.rect(x, y, bw, bh);
    c.fill(); c.stroke();
    c.textAlign = 'left'; c.textBaseline = 'top';
    c.fillStyle = up ? '#34d399' : '#f87171';
    c.fillText((up ? '▲ ' : '▼ ') + txt, x + 10, y + 7);
    c.fillStyle = '#94a3b8'; c.font = '600 0.6rem "Segoe UI", system-ui, sans-serif';
    c.fillText(sub, x + 10, y + 23);
    c.restore();
  }};

  // KPI tile — Sales vs Monthly Target doughnut (was the CP chart)
  (function(){
    var el = document.getElementById('kpi-target-donut'); if (!el) return;
    new Chart(el, {
      type:'doughnut',
      data:{ labels:['Sold','Remaining'], datasets:[
        { data:[RPT.cp.sold, RPT.cp.gap], backgroundColor:['#34d399','rgba(148,163,184,0.28)'], borderWidth:0 } ] },
      options:{ responsive:true, maintainAspectRatio:false, cutout:'66%',
        plugins:{
          legend:{ display:false },
          tooltip:{ callbacks:{ label:function(c){ return c.label+': '+money(c.parsed)+' bags'; } } }
        }
      },
      plugins:[donutCentre(1.15)] });
  })();

  // 1. Current Performance — weekly performance line (each week's % of target)
  (function(){
    var el = document.getElementById('cp-chart'); if (!el) return;
    var w = RPT.cp.weekly || []; if (!w.length){ el.parentNode.style.display='none'; return; }
    var series = w.map(function(x){return x.pct;});
    var pw = RPT.cp.prevWeekly || [];
    var hasPrev = pw.length > 0;
    var labels = w.map(function(x){return x.label;});
    if (pw.length > labels.length) labels = pw.map(function(x){return x.label;});
    var dsets = [
      { label: RPT.cp.curLabel || '% of target', data: series,
        borderColor:'#f59e0b', backgroundColor:'rgba(245,158,11,0.15)', borderWidth:2, fill:true, tension:0.35,
        pointRadius:4, pointBackgroundColor:'#f59e0b', pointBorderColor:'#0b0d16', pointBorderWidth:1, order:1 } ];
    if (hasPrev) dsets.push(
      { label: RPT.cp.prevLabel, data: pw.map(function(x){return x.pct;}),
        borderColor:'rgba(148,163,184,0.9)', backgroundColor:'transparent', borderWidth:2, borderDash:[5,4],
        fill:false, tension:0.35, pointRadius:3, pointBackgroundColor:'#94a3b8', pointBorderColor:'#0b0d16', pointBorderWidth:1, order:2 });
    new Chart(el, {
      type:'line',
      data:{ labels:labels, datasets:dsets },
      options:{ responsive:true, maintainAspectRatio:false, layout:{ padding:{ top:16 } },
        plugins:{ legend:{ display:hasPrev, labels:{ usePointStyle:true, boxWidth:8, color:'#94a3b8' } },
          tooltip:{ callbacks:{
            label:function(c){ return c.dataset.label + ': ' + Number(c.parsed.y).toFixed(2) + '% of target'; },
            afterBody:function(items){ if(!items.length || items[0].datasetIndex!==0) return '';
              var x = w[items[0].dataIndex]; if(!x) return '';
              return ['Weekly sales: ' + money(x.bags) + ' bags',
                      'Cumulative to date: ' + x.cum.toFixed(1) + '% of target']; },
            footer:function(){ if(w.length<2) return '';
              var n=w.length, g=w[n-1].pct-w[n-2].pct;
              return (g>=0?'▲ +':'▼ ')+g.toFixed(2)+' pts week-on-week ('+w[n-2].label+' → '+w[n-1].label+')'; } } } },
        scales:{ y:{ beginAtZero:true, grid:{color:GRID}, ticks:{ callback:function(v){ return v+'%'; } } },
                 x:{ grid:{display:false} } } },
      plugins:[LINEVAL] });
  })();

  // 2 + 2b. New Products — sold/remaining and posts/stock, sortable high↔low
  (function(){
    var el1 = document.getElementById('np-chart'), el2 = document.getElementById('np-stock-chart');
    var base = RPT.np.targets || [];
    if (!base.length){
      if (el1) el1.parentNode.style.display='none';
      if (el2) el2.parentNode.style.display='none';
      return;
    }
    var sel = document.getElementById('np-sort');
    function sorted(){
      var v = sel ? sel.value : 'sold-desc', parts = v.split('-');
      var key = parts[0], dir = (parts[1] === 'asc') ? 1 : -1;
      var get = { sold:function(x){return x.sold;}, remaining:function(x){return x.remaining;},
                  stock:function(x){return x.stock;}, posts:function(x){return x.posts;} }[key] || function(x){return x.sold;};
      return base.slice().sort(function(a,b){ return (get(a) - get(b)) * dir; });
    }
    var c1 = null, c2 = null;
    if (el1) c1 = new Chart(el1, {
      type:'bar', plugins:[VAL],
      data:{ labels:[], datasets:[
        { label:'Sold', data:[], backgroundColor:'#22d3ee', borderRadius:3 },
        { label:'Remaining to target', data:[], backgroundColor:'rgba(148,163,184,0.35)', borderRadius:3 } ] },
      options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{ position:'bottom', labels:{ boxWidth:12 } } },
        scales:{ x:{ stacked:true, grid:{color:GRID} }, y:{ stacked:true, grid:{display:false} } } }
    });
    if (el2) c2 = new Chart(el2, {
      type:'bar', plugins:[VAL],
      data:{ labels:[], datasets:[
        { label:'Stock available', data:[], backgroundColor:'#a78bfa', borderRadius:3 },
        { label:'Posts done', data:[], backgroundColor:'#22d3ee', borderRadius:3 } ] },
      options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{ position:'bottom', labels:{ boxWidth:12 } },
          tooltip:{ callbacks:{ label:function(c){ return c.dataset.label+': '+money(c.parsed.x); } } } },
        scales:{ x:{ grid:{color:GRID} }, y:{ grid:{display:false} } } }
    });
    function draw(){
      var t = sorted(), labels = t.map(function(x){return x.name;});
      if (c1){ c1.data.labels=labels; c1.data.datasets[0].data=t.map(function(x){return x.sold;}); c1.data.datasets[1].data=t.map(function(x){return x.remaining;}); c1.update(); }
      if (c2){ c2.data.labels=labels; c2.data.datasets[0].data=t.map(function(x){return x.stock;}); c2.data.datasets[1].data=t.map(function(x){return x.posts;}); c2.update(); }
    }
    if (sel) sel.addEventListener('change', draw);
    draw();
  })();

  // 2c. Timed Offers — daily lift trend + bags sold per bag (per campaign)
  (RPT.timed || []).forEach(function(camp, ci){
    // Lift trend: daily bags, offer window highlighted, dashed pre-offer average
    var L = camp.lift;
    var lel = document.getElementById('to-lift-' + ci);
    if (lel && L && (L.daily || []).length){
      var dd = L.daily;
      var BASE = { id:'tobase'+ci, afterDatasetsDraw:function(ch){
        var y = ch.scales.y.getPixelForValue(L.basePerDay); if(!isFinite(y)) return;
        var c = ch.ctx, a = ch.chartArea; c.save();
        c.strokeStyle='#f59e0b'; c.setLineDash([5,4]); c.lineWidth=1.5;
        c.beginPath(); c.moveTo(a.left,y); c.lineTo(a.right,y); c.stroke(); c.setLineDash([]);
        c.fillStyle='#fbbf24'; c.font='700 0.6rem "Segoe UI",system-ui,sans-serif'; c.textAlign='right';
        c.fillText('pre-offer avg ' + Math.round(L.basePerDay) + '/day', a.right-4, y-6); c.restore();
      }};
      new Chart(lel, { type:'bar', plugins:[BASE],
        data:{ labels: dd.map(function(x){ return x.date.slice(8); }),
          datasets:[{ label:'Bags', data: dd.map(function(x){ return x.bags; }),
            backgroundColor: dd.map(function(x){ return x.off ? '#10b981' : '#3b4256'; }), borderRadius:3 }] },
        options:{ responsive:true, maintainAspectRatio:false,
          plugins:{ legend:{display:false},
            tooltip:{ callbacks:{ title:function(t){ return dd[t[0].dataIndex].date; },
              label:function(c){ var x=dd[c.dataIndex]; return x.bags + ' bags' + (x.off?' · OFFER':' · pre-offer'); } } } },
          scales:{ x:{ grid:{display:false}, ticks:{ color:INK, font:{size:9} } },
                   y:{ beginAtZero:true, grid:{color:GRID}, ticks:{ color:INK } } } } });
    }
    // Weekly view: bags/day per week, offer week highlighted
    var wel = document.getElementById('to-week-' + ci);
    if (wel && L && (L.weekly || []).length){
      var wk = L.weekly;
      new Chart(wel, { type:'bar',
        data:{ labels: wk.map(function(w){ return w.label; }),
          datasets:[{ label:'Bags/day', data: wk.map(function(w){ return w.perDay; }),
            backgroundColor: wk.map(function(w){ return w.off ? '#10b981' : '#3b4256'; }), borderRadius:4 }] },
        options:{ responsive:true, maintainAspectRatio:false,
          plugins:{ legend:{display:false},
            tooltip:{ callbacks:{ title:function(t){ var w=wk[t[0].dataIndex]; return w.label+' ('+w.start+' → '+w.end+')'; },
              label:function(c){ var w=wk[c.dataIndex]; return [w.perDay+' bags/day', w.total+' over '+w.days+' days'+(w.off?' · OFFER':'')]; } } } },
          scales:{ x:{ grid:{display:false}, ticks:{ color:INK } },
                   y:{ beginAtZero:true, grid:{color:GRID}, ticks:{ color:INK }, title:{display:true,text:'bags/day',color:'#64748b',font:{size:10}} } } } });
    }
    var el = document.getElementById('to-chart-' + ci); if (!el) return;
    var rows = (camp.bags || []).slice();
    if (!rows.length){ el.parentNode.style.display='none'; return; }
    var VAL = { id:'toval'+ci, afterDatasetsDraw:function(ch){
      var c = ch.ctx, m = ch.getDatasetMeta(0); c.save();
      c.font='700 0.64rem "Segoe UI", system-ui, sans-serif'; c.fillStyle='#f8fafc';
      c.textAlign='left'; c.textBaseline='middle';
      m.data.forEach(function(bar,i){ var v = rows[i].sold; if (v==null) return; c.fillText(money(v), bar.x + 6, bar.y); });
      c.restore();
    }};
    new Chart(el, { type:'bar', plugins:[VAL],
      data:{ labels: rows.map(function(r){ return r.name; }),
        datasets:[{ label:'Bags sold', data: rows.map(function(r){ return r.sold; }),
          backgroundColor:'#10b981', borderRadius:4, maxBarThickness:30 }] },
      options:{ indexAxis:'y', responsive:true, maintainAspectRatio:false,
        layout:{ padding:{ right:42 } },
        interaction:{ mode:'index', axis:'y', intersect:false },
        plugins:{ legend:{ display:false },
          tooltip:{ callbacks:{ label:function(c){ var r = rows[c.dataIndex];
            return [ money(r.sold) + ' bags sold',
                     (r.posts>0 ? r.posts + ' posts · ' + (r.perPost!=null?r.perPost.toFixed(1):'—') + ' sold/post'
                                : '0 posts — sold without marketing') ]; } } } },
        scales:{ x:{ beginAtZero:true, grid:{ color:GRID }, ticks:{ color:INK } },
                 y:{ grid:{ display:false }, ticks:{ color:'#cbd5e1', font:{ size:12 } } } } } });
  });

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
          tooltip:{ callbacks:{
            label:function(c){ var o=items[c.dataIndex]; return money(c.parsed.x)+' units moved · '+(o.type==='combo'?'combo':'power deal'); },
            afterBody:function(t){ var o=items[t[0].dataIndex], b=o.bags||[]; if(!b.length) return [];
              return [(o.type==='combo'?'Bags — most stock first:':'Stock:')].concat(
                b.map(function(x){ return '  ' + x.name + (x.stock!=null ? ' — ' + money(x.stock) + ' in stock' : ' — stock n/a'); })); } } } },
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
        // axis:'y' + intersect:false makes the WHOLE row hoverable, so zero-length
        // (non-selling) offers still pop their tooltip showing the stock sitting.
        interaction:{ mode:'index', axis:'y', intersect:false },
        plugins:{ legend:{display:false},
          tooltip:{ callbacks:{
            label:function(c){ var o=items[c.dataIndex]; return money(c.parsed.x)+' units moved · '+o.type; },
            afterBody:function(t){ var o=items[t[0].dataIndex], b=o.bags||[]; if(!b.length) return [];
              var head = (Number(o.units)||0)===0
                ? 'Dead stock — 0 moved, ' + money(b.reduce(function(a,x){return a+(Number(x.stock)||0);},0)) + ' in stock:'
                : (o.type==='combo'?'Bags — most stock first:':'Stock:');
              return [head].concat(
                b.map(function(x){ return '  ' + x.name + (x.stock!=null ? ' — ' + money(x.stock) + ' in stock' : ' — stock n/a'); })); } } } },
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

# The live monthly_report.html always shows only the latest month. Past months
# are preserved in the History page (backed by Supabase) — including the comments
# collected below — so no dated per-month HTML archive is written any more.

# ── COLLECT THE REPORT'S COMMENTS (for Supabase / History) ────
# Pull the narrative blocks straight out of the rendered report, so History can
# show the same Bottom Line / Insight / Recommendation prose per month without a
# second copy of the text drifting out of sync.
def _html_text(s):
    s = re.sub(r"<[^>]+>", "", s)
    for _a, _b in (("&amp;", "&"), ("&mdash;", "—"), ("&minus;", "−"), ("&middot;", "·"),
                   ("&rarr;", "→"), ("&asymp;", "≈"), ("&nbsp;", " "), ("&lt;", "<"),
                   ("&gt;", ">"), ("&times;", "×")):
        s = s.replace(_a, _b)
    return re.sub(r"\s+", " ", s).strip()

def _collect_comments(html):
    items = []
    m = re.search(r'<div class="headline">(.*?)</div>', html, re.S)
    if m:
        items.append({"section": "Executive Summary", "label": "The Bottom Line",
                      "type": "bottom", "text": _html_text(m.group(1))})
    for li in re.findall(r'<div class="exec">.*?<ul>(.*?)</ul>', html, re.S)[:1]:
        for one in re.findall(r'<li>(.*?)</li>', li, re.S):
            items.append({"section": "Executive Summary", "label": "Key point",
                          "type": "bullet", "text": _html_text(one)})
    heads = [(mm.start(), _html_text(mm.group(1)))
             for mm in re.finditer(r'<div class="sec-head">.*?<h2>(.*?)</h2>', html, re.S)]
    def _section_for(pos):
        name = "Report"
        for hpos, hname in heads:
            if hpos <= pos:
                name = hname
            else:
                break
        return name
    # Bottom Line / Insight / Business Impact — each carries a <p>
    for mm in re.finditer(
            r'<div class="tag (bottom|insight|impact)">(.*?)</div>'
            r'(?:\s*<div class="impact">)?\s*<p>(.*?)</p>', html, re.S):
        text = _html_text(mm.group(3))
        if text:
            items.append({"section": _section_for(mm.start()),
                          "label": _html_text(mm.group(2)), "type": mm.group(1), "text": text})
    # Recommendations (Start/Stop/Test list items — no <p>)
    for mm in re.finditer(r'<div class="tag rec">(.*?)</div>\s*<div class="recs">(.*?)</div>\s*</div>', html, re.S):
        label = _html_text(mm.group(1))
        for span in re.findall(r'<span[^>]*>(.*?)</span>', mm.group(2), re.S):
            t = _html_text(span)
            if t and t.lower() not in ("start", "stop", "start testing"):
                items.append({"section": _section_for(mm.start()), "label": label, "type": "rec", "text": t})
    return items

_comments = _collect_comments(body)
print(f"  Report comments : {len(_comments)} blocks captured")

# ── HISTORICAL SNAPSHOT (JSON) ────────────────────────────────
# Freeze this month's report figures, keyed by YYYY-MM, so past months (e.g.
# the July report) are preserved even after the live dashboards roll into the
# next month. Accumulates all months in monthly_report_history.json.
_month_num = list(_cal.month_name).index(month) if month in list(_cal.month_name) else datetime.date.today().month
_key = f"{year}-{_month_num:02d}"


def _timed_offer_snapshots():
    """This month's timed-offer campaigns, flattened for storage.

    The live TO payload carries each bag twice — the headline list (sold, posts,
    sold/post) and the richer `why.bags` list (stock, prices, discount, the bag's
    own lift). They are merged by name here so one stored row per bag holds the
    whole picture. The daily series comes along too: it is what makes the lift
    ("77.5/day before → 139.0/day during") readable in History instead of a bare
    percentage."""
    out = []
    for c in timed_offers:
        lift = c.get("lift") or {}
        why = c.get("why") or {}
        rich = {str(b.get("name", "")).strip().lower(): b for b in (why.get("bags") or [])}
        bags = []
        for b in (c.get("bags") or []):
            r = rich.get(str(b.get("name", "")).strip().lower(), {})
            bags.append({
                "name":        b.get("name"),
                "sold":        num(b.get("sold")),
                "posts":       num(b.get("posts")),
                "perPost":     b.get("perPost"),
                "stock":       r.get("stock"),
                "category":    r.get("category"),
                "priceWas":    r.get("priceWas"),
                "priceNow":    r.get("priceNow"),
                "discountKes": r.get("discountKes"),
                "discountPct": r.get("discountPct"),
                "bagLift":     r.get("bagLift"),
            })
        out.append({
            "name":        c.get("name"),
            "market":      c.get("market"),
            "startDate":   c.get("startDate"),
            "endDate":     c.get("endDate"),
            "windowLabel": c.get("windowLabel"),
            "totalSold":   num(c.get("totalSold")),
            "totalPosts":  num(c.get("totalPosts")),
            "perPost":     c.get("perPost"),
            "bestName":    c.get("bestName"),
            "bestSold":    num(c.get("bestSold")),
            "totalStock":  why.get("totalStock"),
            "verdict":     why.get("verdict"),
            "liftPct":     lift.get("liftPct"),
            "baseStart":   lift.get("baseStart"),
            "baseEnd":     lift.get("baseEnd"),
            "baseDays":    lift.get("baseDays"),
            "baseTotal":   lift.get("baseTotal"),
            "basePerDay":  lift.get("basePerDay"),
            "offerDays":   lift.get("offerDays"),
            "offerTotal":  lift.get("offerTotal"),
            "offerPerDay": lift.get("offerPerDay"),
            "bags":        bags,
            "daily":       lift.get("daily") or [],
            "weekly":      lift.get("weekly") or [],
        })
    return out
_snapshot = {
    "month": month, "year": year, "key": _key,
    "generatedOn": datetime.date.today().isoformat(),
    "currentPerformance": {
        "achievedPct": round(achieved, 2), "totalSales": total_sales, "totalTarget": total_target,
        "gap": gap, "bareMinimum": bare_min, "avgWeekly": avg_weekly, "corporate": corporate,
        "forecast": forecast, "weekly": wk_series,
    },
    "newProducts": {
        "count": np_count, "target": np_target, "sales": np_sales, "deficit": np_deficit,
        "kenya": np_kenya, "outside": np_outside, "posts": np_posts,
        "names": np_names, "products": _rpt["np"]["targets"],
    },
    "offerType": {
        "combos": combos, "powerDeals": deals,
        "kenya": {"comboUnits": combo_units, "comboValue": combo_value, "comboAvg": round(combo_avg, 1),
                  "dealUnits": deal_units, "dealValue": deal_value, "dealAvg": round(deal_avg, 1),
                  "offers": _rpt["offer"]["items"]},   # individual Kenya offers (combo/deal), stored like Sinza/Uganda
        "sinza": {"units": sz_off_units, "value": sz_off_value, "cleared": round(sz_cleared, 1),
                  "offers": _rpt["offer"]["sinza"]},
        "uganda": {"units": ug_off_units, "value": ug_off_value, "cleared": round(ug_cleared, 1),
                   "offers": _rpt["offer"]["uganda"]},
    },
    "postingYields": {
        "kenyaPct": ke_mo_mkt, "sinzaPct": sz_mo_mkt, "ugandaPct": ug_mo_mkt,
        "postedStock": posted, "unpostedStock": notposted, "postsMade": mo_posts_made,
        "notOnOffer": {"kenya": ke_notoffer_stock, "sinza": sz_notoffer_stock, "uganda": ug_notoffer_stock},
        "salesFromPosting": mo_sales_posting, "expectedFromPosting": mo_expect_posting,
    },
    "timedOffers": _timed_offer_snapshots(),
    "selfMadeCombos": ({
        "smTotals": self_made["smTotals"], "runTotals": self_made["runTotals"],
        "selfMade": self_made["selfMade"], "running": self_made["running"],
        "requests": self_made["requests"], "reqCounts": self_made["reqCounts"],
        "reqTotal": self_made["reqTotal"],
    } if self_made else None),
    "comments": _comments,
}
HISTORY_FILE = os.path.join(BASE, "monthly_report_history.json")
# History (→ Supabase) is written ONLY when archiving a completed month — i.e.
# when month_end.py PINS the month. A normal live run just rebuilds the current-
# month report HTML and leaves the archive untouched, so History holds finished
# months only; the current month lands there at month-end.
_archived = report_month.is_pinned()
_hist = {}
if _archived:
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, encoding="utf-8") as f:
                _hist = json.load(f)
        except (ValueError, OSError):
            _hist = {}
    if not isinstance(_hist, dict):
        _hist = {}
    _hist[_key] = _snapshot
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(_hist, f, indent=2, ensure_ascii=False)

print(f"monthly_report.html built for {month} {year}.")
print(f"  Target achieved : {pct(achieved)}  ({fmt(total_sales)}/{fmt(total_target)})")
print(f"  Missed by       : {fmt(gap)} bags")
print(f"  Unposted stock  : {fmt(notposted)} ({pct(unposted_pct)})")
print(f"  Weakest region  : {weak_name} ({pct(weak_val)})")
print(f"  Timed offers    : {len(_snapshot['timedOffers'])} campaign(s) stored "
      f"({sum(len(c['bags']) for c in _snapshot['timedOffers'])} bag rows)")
if _archived:
    print(f"  Archived [{_key}] to history.json  ({len(_hist)} month(s) stored) — will push to Supabase.")
else:
    print(f"  Live {month} report — history.json unchanged (a month is archived at month-end via month_end.py).")
