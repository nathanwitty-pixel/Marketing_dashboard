"""
forward_projections.py
─────────────────────────────────────────────────────────────────
Edit the values in MANUAL INPUTS, then run:
    python forward_projections.py

First run: a browser window will open asking you to sign in to
Google. After that, credentials are saved locally and every
subsequent run is fully automatic.
─────────────────────────────────────────────────────────────────
Reads live from Google Sheets (one connection, two sheets):

  MONTHLY_TARGET sheet
    col C (TARGET) → sum all rows below header  →  total_target
    col D (SALES)  → sum all rows below header  →  total_sales

  WEEKLY_SALES sheet
    col C = "SUM TOTAL" row, col X (TOTAL)      →  weekly_sales_total
"""

import re, webbrowser, os, pathlib, calendar, subprocess, sys, json
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root → lib/
from lib import paths
from lib import report_month   # which month these figures belong to

# ── SPREADSHEET ───────────────────────────────────────────────

SPREADSHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"


# ── CORPORATE BAGS (dynamic) ──────────────────────────────────
# No longer a manual entry. Pulled live from Odoo customer invoices
# (account_move) for the projected month — see _corporate_bags() below and
# sql/corporate_bags.sql. Used ONLY by the Forecasted Projection and added on
# top of POS in the Sales card; Total/Weekly Sales stay POS-only, so
# corporate is never double-counted.
# bare_minimum is computed below = monthly target ÷ perfect weeks in month.


def _corporate_bags(year, month):
    """(corporate bags, corporate KES received) in the given month, live from
    Odoo invoices. Returns (0, 0) when Postgres isn't reachable (projection falls
    back to POS-only rather than a stale hardcoded figure)."""
    try:
        from lib import db, queries
        ok, _ = db.check_connection()
        if not ok:
            return 0, 0
        m_start = date(year, month, 1)
        m_end   = date(year, month, calendar.monthrange(year, month)[1])
        df = db.run_query(queries.CORPORATE_BAGS,
                          {"start_date": m_start.isoformat(),
                           "end_date":   m_end.isoformat()})
        if df is not None and not df.empty:
            return int(df.iloc[0]["bags"] or 0), round(float(df.iloc[0]["kes"] or 0))
    except Exception:
        pass
    return 0, 0


def _corporate_lines(year, month):
    """The corporate app bags behind _corporate_bags(), one row per product with its clients
    (sql/corporate_bag_lines.sql). [] when Postgres isn't reachable."""
    try:
        from lib import db, queries
        df = db.run_query(queries.CORPORATE_BAG_LINES,
                          {"start_date": date(year, month, 1).isoformat(),
                           "end_date":   date(year, month, calendar.monthrange(year, month)[1]).isoformat()})
        if df is not None and not df.empty:
            return [{"product": r["product"], "bags": float(r["bags"] or 0), "kes": float(r["kes"] or 0),
                     "clients": r["clients"] or ""} for _, r in df.iterrows()]
    except Exception:
        pass
    return []


def _bag_revenue(year, month):
    return _bag_revenue_range(date(year, month, 1), date(year, month, calendar.monthrange(year, month)[1]))


def _bag_revenue_range(start, end):
    """POS bag revenue for the month, split by how the bags were sold (sql/bag_revenue.sql —
    combo money taken from the '+' wrapper line). Same month window as monthly_sales.py, so it
    sits on the same bags as Total Sales. None when Postgres isn't reachable."""
    try:
        from lib import db, queries
        ok, _ = db.check_connection()
        if not ok:
            return None
        df = db.run_query(queries.BAG_REVENUE,
                          {"start_date": start.isoformat(),
                           "end_date":   end.isoformat(),
                           "excluded":   queries.excluded_products()})
        if df is not None and not df.empty:
            return {k: round(float(v or 0)) for k, v in df.iloc[0].items()}
    except Exception:
        pass
    return None


def _revenue_target(year, month):
    """The month's revenue target (KES): Odoo sales_pos_target amount (pos +
    corporate), else REVENUE_TARGETS in lib/product_targets. 0 = none / no DB."""
    try:
        from lib import db, product_targets
        ok, _ = db.check_connection()
        if ok:
            t = db.run_query(product_targets.TOTAL_SQL, {"m": date(year, month, 1).isoformat()})
            if t is not None and len(t) and t.amt[0] is not None and float(t.amt[0]) > 0:
                return round(float(t.amt[0]))
        return product_targets.REVENUE_TARGETS.get(f"{year}-{month:02d}", 0)
    except Exception:
        return 0


# ── PERFECT (COMPLETE) WEEKS IN THE MONTH ─────────────────────
# A "perfect week" = a week with >=5 of its days falling inside the month
# (the project's count_complete_weeks_in_month definition). Sales run
# Sun–Sat, so weeks are counted from Sunday.

def count_complete_weeks_in_month(ref=None):
    today = ref or date.today()
    year, month = today.year, today.month
    month_start = date(year, month, 1)
    if month == 12:
        month_end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = date(year, month + 1, 1) - timedelta(days=1)
    # align to the Sunday that starts the week containing the 1st
    week_start = month_start - timedelta(days=(month_start.weekday() + 1) % 7)
    complete = 0
    while week_start <= month_end:
        days_in = sum(
            1 for i in range(7)
            if (week_start + timedelta(days=i)).year  == year
            and (week_start + timedelta(days=i)).month == month
        )
        if days_in >= 5:
            complete += 1
        week_start += timedelta(days=7)
    return max(complete, 1)


# ── GOOGLE SHEETS AUTH ────────────────────────────────────────

# Shared auth: service account (permanent) or self-healing OAuth — see google_auth.py
from lib.google_auth import get_gspread_client


# ── AUTO-READ: all figures from Google Sheets ─────────────────

def fetch_sheet_data():
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)

    # ── MONTHLY_TARGET ────────────────────────────────────────
    # Row 1 = header: COLOUR | CATEGORY | PRODUCT NAME | BAG TYPE | TARGET | SALES | DEFICIT | ...
    # Wait — actual header: BAG TYPE | CATEGORY | TARGET(C) | SALES(D) | DEFICIT(E)
    # col C = TARGET, col D = SALES  (rows 2 onwards, skip header row 1)

    # Column C = the month's bag targets from Odoo (lib/product_targets — docs/product-targets.md).
    from lib import product_targets
    mt_rows = product_targets.monthly_target_rows(sh.worksheet("MONTHLY_TARGET").get_all_values())
    col_c_raw = [r[2] if len(r) > 2 else "" for r in mt_rows]   # column C — TARGET
    col_d_raw = [r[3] if len(r) > 3 else "" for r in mt_rows]   # column D — SALES

    # Skip header (row 1); sum all numeric values
    def safe_sum(values):
        total = 0
        for v in values[1:]:            # [1:] skips the header row
            try:
                total += int(float(str(v).replace(",", "")))
            except (ValueError, TypeError):
                pass
        return total

    target_total = safe_sum(col_c_raw)   # sum of column C (TARGET)
    sales_total  = safe_sum(col_d_raw)   # sum of column D (SALES)

    # ── WEEKLY_SALES ──────────────────────────────────────────
    # The row where column C = "SUM TOTAL", column X = TOTAL. Built from Odoo for
    # the CURRENT Sun–Sat week (lib/odoo_tabs; the sheet tab only if Postgres is down).
    from lib import odoo_tabs
    from weekly_sales import week_window
    ws_rows = odoo_tabs.get_rows(sh, "WEEKLY_SALES", window=week_window())

    weekly_total = 0
    for row in ws_rows:
        if len(row) > 23 and str(row[2]).strip().upper() == "SUM TOTAL":
            val = str(row[23]).replace(",", "").strip()   # column X
            weekly_total = int(float(val)) if val else 0
            break
    else:
        print("  Warning: 'SUM TOTAL' not found in WEEKLY_SALES column C.")

    return target_total, sales_total, weekly_total


print("Fetching data from Google Sheets...")
total_target, total_sales, weekly_sales_total = fetch_sheet_data()


# ── Prefer LIVE Odoo figures over the sheet (same as current_performance.py) ──
# Target is the Odoo target (lib/product_targets — past sales + stock days). Sales & weekly come from
# Postgres when available, so the projections match the Current Performance
# cards instead of the sheet's SALES / WEEKLY_SALES columns.
def _live_bags(filename, key_field, key_value, bags_field):
    path = paths.data(filename)
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
        if d.get(key_field, "") == key_value:
            return int(round(float(d.get(bags_field))))
    except (ValueError, OSError, KeyError, TypeError):
        pass
    return None

_today  = date.today()
_sunday = _today - timedelta(days=(_today.weekday() + 1) % 7)
# Match the monthly file against the LIVE month (today's month, unless pinned),
# so the live dashboard projects the month we are actually in. The archived
# report stays correct because month_end.py PINS the month it archives.
_live_month = _live_bags("monthly_sales_db.json", "monthKey",  report_month.live_month_key(), "monthlyBags")
_live_week  = _live_bags("weekly_sales_db.json",  "weekStart", _sunday.isoformat(),      "weeklyBags")
sales_is_live = _live_month is not None
if sales_is_live:
    total_sales = _live_month
if _live_week is not None:
    weekly_sales_total = _live_week


# ── DATE (auto-calculated) ────────────────────────────────────
# Sales are entered in the sheet the same evening, so by today the data
# covers every complete day through YESTERDAY. Complete days = yesterday's
# day-of-month.

# Projection reference for the LIVE month. Pinned (archive) → the month's last
# day (a complete month, velocity ×1). Live → complete days so far (data through
# yesterday), floored to day 1 so the 1st of a new month reads day 1, not the
# previous month's day 31.
if report_month.is_pinned():
    yesterday = report_month.live_anchor()
else:
    _la = report_month.live_anchor()
    yesterday = max(_la - timedelta(days=1), _la.replace(day=1))
current_day     = max(yesterday.day, 1)
days_in_month   = calendar.monthrange(yesterday.year, yesterday.month)[1]
proj_ref        = yesterday

# Start-of-month rollover guard: in the first days of a new calendar month the
# sheet often still holds LAST month's full total (it hasn't been reset yet).
# Multiplying that by days_in_month ÷ current_day (e.g. ×31 on day 1) produces a
# nonsense projection (2225%). If the projection would be wildly over target this
# early, the data is still last month's — so project the PREVIOUS, completed
# month at 1× pace until the new month's data actually starts coming in.
if (not sales_is_live and current_day <= 6 and days_in_month and total_target
        and (total_sales * days_in_month / current_day) > total_target * 1.5):
    proj_ref      = yesterday.replace(day=1) - timedelta(days=1)   # last day of previous month
    current_day   = calendar.monthrange(proj_ref.year, proj_ref.month)[1]
    days_in_month = current_day

velocity_factor = days_in_month / current_day
proj_month      = proj_ref.strftime("%B")

# Corporate bags for the projected month (dynamic — from Odoo invoices).
corporate_bags, corporate_kes = _corporate_bags(proj_ref.year, proj_ref.month)
revenue_target = _revenue_target(proj_ref.year, proj_ref.month)
# POS bag revenue month-to-date — live month only (the sheet has no money column).
bag_rev     = _bag_revenue(proj_ref.year, proj_ref.month) if sales_is_live else None
total_value = (bag_rev["single_kes"] + bag_rev["combo_kes"] + bag_rev["gift_kes"]
               + bag_rev["discount_kes"]) if bag_rev else None

# Perfect (complete) weeks in the month — used for the bare minimum
perfect_weeks = count_complete_weeks_in_month()


# ── CALCULATIONS ──────────────────────────────────────────────

# 1. Standard Projection
#    Step 1: total_sales × (days_in_month ÷ current_day)  → projected end-of-month bags
#    Step 2: ÷ total_target × 100                         → as % of target
standard_projection_pct = (total_sales * velocity_factor) / total_target * 100

# 2. Forecasted Projection
#    Step 1: (total_sales + corporate_bags) × (days_in_month ÷ current_day)
#    Step 2: ÷ total_target × 100                         → as % of target
forecasted_projection_pct = ((total_sales + corporate_bags) * velocity_factor) / total_target * 100

# 2b. Projected revenue (KES) — same pace as the bags projections, so the two read together.
#     Standard = POS revenue × velocity; Forecasted = (POS revenue + corporate KES) × velocity.
#     None when there's no live month figure (the cards then leave the revenue line off).
if total_value is not None:
    standard_revenue   = total_value * velocity_factor
    forecasted_revenue = (total_value + corporate_kes) * velocity_factor
else:
    standard_revenue = forecasted_revenue = None
standard_revenue_pct   = (standard_revenue   / revenue_target * 100) if standard_revenue   is not None and revenue_target else None
forecasted_revenue_pct = (forecasted_revenue / revenue_target * 100) if forecasted_revenue is not None and revenue_target else None

# 2c. Price per bag — why the revenue % and the bags % differ. The targets assume each bag brings
#     in revenue_target ÷ total_target; this month's bags actually bring in total_value ÷ bags.
#     revenue % ≈ bags % × (actual ÷ target price). Split by how bags were sold so the reader can
#     see what lifts or drags the average.
price_mix = None
if bag_rev and bag_rev["bags"] and revenue_target and total_target:
    vel        = velocity_factor
    target_ppb = revenue_target / total_target          # the bag target has no gift bags in it
    main_bags  = bag_rev["single_bags"] + bag_rev["combo_bags"]
    main_kes   = bag_rev["single_kes"] + bag_rev["combo_kes"] + bag_rev["discount_kes"]
    actual_ppb = main_kes / main_bags if main_bags else 0

    # Gift bags have no Odoo target, so they get their own: the average month of the three complete
    # months before (product_targets.base_period, the same base as the bag targets), at their own
    # price then. Judged against that, not the KES ~2,000 a bag that targeted bags carry.
    from lib import product_targets as _pt
    _bs, _be = _pt.base_period(date(proj_ref.year, proj_ref.month, 1))
    _base = _bag_revenue_range(_bs, _be)
    gift_target_bags = round(_base["gift_bags"] / 3) if _base else 0
    gift_target_ppb  = (_base["gift_kes"] / _base["gift_bags"]) if _base and _base["gift_bags"] else 0

    def _row(label, bags, kes, tppb, target_bags=None):
        """One table row, month-end projected. expected = what the targets expect from this group
        by month end: projected bags × target price, or (gift bags) their own target × own price."""
        pb, pk = bags * vel, kes * vel
        expected = ((target_bags if target_bags is not None else pb) * tppb) if tppb else 0
        ppb = (kes / bags) if bags else None
        return {"label": label, "bags": bags, "kes": kes, "projBags": round(pb), "projKes": round(pk),
                "ppb": round(ppb) if ppb is not None else None,
                "targetPpb": round(tppb) if tppb else None,
                "targetBags": target_bags,
                "gapPct": round((ppb / tppb - 1) * 100, 1) if ppb is not None and tppb else None,
                "share": round(bags / bag_rev["bags"] * 100, 1) if bags else None,
                "expectedKes": round(expected),
                "effectKes": round(pk - expected),
                "effectPts": round((pk - expected) / revenue_target * 100, 2)}
    rows = [
        _row("Single bags", bag_rev["single_bags"], bag_rev["single_kes"], target_ppb),
        _row("Combos",      bag_rev["combo_bags"],  bag_rev["combo_kes"],  target_ppb),
        _row("Gift bags",   bag_rev["gift_bags"],   bag_rev["gift_kes"],   gift_target_ppb,
             gift_target_bags if gift_target_bags else None),
        _row("Discounts",   0,                      bag_rev["discount_kes"], 0),
    ]
    total = {"label": "All bags", "bags": bag_rev["bags"], "kes": total_value,
             "projBags": sum(r["projBags"] for r in rows), "projKes": sum(r["projKes"] for r in rows),
             "ppb": round(total_value / bag_rev["bags"]), "share": 100.0,
             "expectedKes": sum(r["expectedKes"] for r in rows),
             "effectKes": sum(r["effectKes"] for r in rows),
             "effectPts": round(sum(r["effectKes"] for r in rows) / revenue_target * 100, 2)}
    price_mix = {
        "targetPpb": round(target_ppb),
        "actualPpb": round(actual_ppb),                  # single bags + combos (after discounts) — like for like with the target
        "gapPct":    round((actual_ppb / target_ppb - 1) * 100, 1),
        "mainBags":  main_bags,
        "bagsPct":   round(total_sales / total_target * 100, 2),
        "revPct":    round(total_value / revenue_target * 100, 2),
        "velocity":  round(vel, 4),
        "revenueTarget": revenue_target,
        "giftBase":  {"from": _bs.strftime("%b"), "to": _be.strftime("%b"), "bags": gift_target_bags,
                      "ppb": round(gift_target_ppb)},
        "rows": rows,
        "total": total,
    }

    # On offer vs not on offer — the Bags On vs Off Offer page's sorting of the same month's bags
    # (data/offer_mix.json, written by bags_on_offer.py), judged on the same prices: KES ~2,000 a bag,
    # gift bags on their own target, samples expect nothing (not in the bag target). Each offer row
    # carries the bags inside it.
    try:
        with open(paths.data("offer_mix.json"), encoding="utf-8") as _f:
            _om = json.load(_f)
    except (OSError, ValueError):
        _om = None
    if _om and _om.get("month") == proj_ref.strftime("%B %Y"):
        # Corporate app bags (paid invoices, not POS) — the same bags and KES the Forecasted card adds.
        _capp = _corporate_lines(proj_ref.year, proj_ref.month)
        _capp_bags = sum(c["bags"] for c in _capp)
        # The till's KES 300 discount line has qty 1 but isn't a bag: keep its money, drop its count.
        _disc_units = sum(u["units"] for u in _om.get("unclassifiedBags", []) if "DISCOUNT" in u["name"].upper())
        _unc = dict(_om["unclassified"], units=_om["unclassified"]["units"] - _disc_units)
        _all = (sum(r["units"] for r in _om["rows"] if r["key"] != "CORP")       # CORP = the Corporate app, added once below
                + _unc["units"] + _capp_bags)                                    # _unc = the non-discount lines

        def _orow(label, units, kes, key=None, on=None, bags=None):
            if key == "GIFT":
                tppb, tb = gift_target_ppb, (gift_target_bags or None)
            elif key == "SAMPLE":
                tppb, tb = 0, None
            else:
                tppb, tb = target_ppb, None
            r = _row(label, units, kes, tppb, tb)
            r["bags"] = round(units)
            r["projBags"] = round(units * vel)
            r["share"] = round(units / _all * 100, 1) if units and _all else None
            r["key"], r["on"] = key, on
            if key == "UNC":            # the till discount: no bags, nothing expected, so its effect = the money off
                r.update(gapPct=None, targetPpb=None, ppb=None, share=None)
            if bags is not None and key in ("CAPP", "UNC", "PART"):
                r["items"] = bags            # already shaped (bag, sub, bags, kes, ppb, gapPct)
            elif bags is not None:
                r["items"] = [{"bag": b["bag"], "category": b["category"], "tier": b["tier"],
                               "bags": round(b["units"], 1), "kes": b["revenue"],
                               "ppb": round(b["revenue"] / b["units"]) if b["units"] else None,
                               "gapPct": round((b["revenue"] / b["units"] / tppb - 1) * 100, 1)
                                         if b["units"] and tppb else None}
                              for b in bags]
            return r

        _on = [r for r in _om["rows"] if r["on"]]
        # bag → (category, tier) from the offer page's tree, so the Mid-month parts' bags group by category too
        _cat_of = {b["bag"]: (b["category"], b["tier"]) for r in _om["rows"] for b in r["bags"]
                   if b["category"] and b["category"] != "UNASSIGNED"}
        groups = []
        for r in _om["rows"]:
            # The offer page's Corporate row is the Corporate app too (26 Oct 2026), so only the per-bag
            # "Corporate app" row below is shown — never both.
            if r["key"] != "CORP":
                groups.append(_orow(r["label"], r["units"], r["revenue"], r["key"], r["on"], r["bags"]))
            if r["key"] == "MID":
                # What the Mid-month offers are made of: new products, runway bags, timed offers (Kenya),
                # the month's listed singles (Tanzania / Uganda). Rows sit under Mid-month offers.
                _part_lbl = {mp["part"]: f'{mp["part"]} ({", ".join(mp.get("countries") or ["Kenya"])})'
                             for mp in _om.get("midParts", [])}
                groups[-1]["parts"] = [
                    _orow(_part_lbl.get(mp["part"], mp["part"]), mp["units"], mp["revenue"], "PART", True,
                          [{"bag": b["bag"], "category": _cat_of.get(b["bag"], ("", ""))[0],
                            "tier": _cat_of.get(b["bag"], ("", ""))[1],
                            "bags": round(b["units"], 1), "kes": b["revenue"],
                            "ppb": round(b["revenue"] / b["units"]) if b["units"] else None,
                            "gapPct": round((b["revenue"] / b["units"] / target_ppb - 1) * 100, 1) if b["units"] else None}
                           for b in mp["bags"]])
                    for mp in _om.get("midParts", [])]
                if groups[-1]["parts"]:
                    groups[-1].pop("items", None)        # its bags are listed under each part instead
            if r["key"] == "CORP" and _capp:
                items = [{"bag": c["product"].title() if c["product"] != "Fees and other" else c["product"],
                          "sub": c["clients"], "bags": round(c["bags"], 1), "kes": round(c["kes"]),
                          "ppb": round(c["kes"] / c["bags"]) if c["bags"] else None,
                          "gapPct": round((c["kes"] / c["bags"] / target_ppb - 1) * 100, 1) if c["bags"] else None}
                         for c in _capp]
                groups.append(_orow("Corporate app", _capp_bags, sum(c["kes"] for c in _capp),
                                    "CAPP", None, items))
        # "Not yet sorted" is only the KES 300 till discount line (money off the bill, not bags). The few
        # other unsorted lines are items the offer lists don't know (PPM, Passport Holder…) sold at full
        # price, so they're added to Not on offer, each listed with why.
        _ub = _om.get("unclassifiedBags", [])
        _disc = [u for u in _ub if "DISCOUNT" in u["name"].upper()]
        _rest = [u for u in _ub if "DISCOUNT" not in u["name"].upper()]
        _off = next((g for g in groups if g["key"] == "OFF"), None)
        if _off is not None and _rest:
            _orig = next(r for r in _om["rows"] if r["key"] == "OFF")
            _extra = [{"bag": u["name"], "category": "NOT IN THE BAG LIST YET", "tier": "full price",
                       "units": u["units"], "revenue": u["revenue"]} for u in _rest]
            groups[groups.index(_off)] = _orow(_off["label"], _orig["units"] + sum(u["units"] for u in _rest),
                                               _orig["revenue"] + sum(u["revenue"] for u in _rest),
                                               "OFF", False, _orig["bags"] + _extra)
        if _disc:
            _dk = sum(u["revenue"] for u in _disc)
            _dn = round(sum(u["units"] for u in _disc))
            groups.append(_orow("KES 300 till discount", 0, _dk, "UNC", None,
                                [{"bag": "KES 300 discount on total amount", "bags": 0, "kes": _dk, "ppb": None,
                                  "gapPct": None, "sub": f"given {_dn} times this month"}]))
        _where = {r["key"]: r.get("where") for r in _om["rows"]}
        for g in groups:
            if g["key"] == "CAPP":
                g["where"] = "Kenya (Corporate app)"
            elif _where.get(g["key"]):
                g["where"] = _where[g["key"]]
            for pt in g.get("parts") or []:
                pt["where"] = None              # the label says where
        on_total = _orow("On offer", sum(r["units"] for r in _on), sum(r["revenue"] for r in _on), "ON", True)
        off = next((g for g in groups if g["key"] == "OFF"), None)
        price_mix["offerMix"] = {
            "generated": _om["generated"],
            "range":     _om["range"],
            "on":        on_total,
            "rows":      groups,
            # corporate counted as the Sales card counts it (whole bags), so the two totals agree
            "total":     {"label": "All bags", "bags": round(_all - _capp_bags) + corporate_bags,
                          "kes": sum(g["kes"] for g in groups),
                          "projBags": sum(g["projBags"] for g in groups),
                          "projKes": sum(g["projKes"] for g in groups),
                          "ppb": round(sum(g["kes"] for g in groups) / _all) if _all else None,
                          "share": 100.0,
                          "effectKes": sum(g["effectKes"] for g in groups),
                          "effectPts": round(sum(g["effectKes"] for g in groups) / revenue_target * 100, 2)},
            "offPpb":    off["ppb"] if off else None,
        }

# 3. Bare Minimum = monthly target ÷ perfect weeks in the month
bare_minimum       = round(total_target / perfect_weeks) if perfect_weeks else 0
bare_minimum_value = bare_minimum

# 3b. Bare Minimum Growth %
bare_minimum_growth_pct = (bare_minimum / total_target) * 100 if total_target else 0

# 4. Declined By
declined_by = bare_minimum_value - weekly_sales_total if bare_minimum_value else 0


# ── WEEKLY PERFORMANCE SNAPSHOT ───────────────────────────────
# Record each Sun–Sat week's Sales / Weekly Sales / Declined By so the
# dashboard can show Week 1 → the latest week. One entry per week; the
# current week's row is refreshed each run until the week rolls over.
WEEKLY_HISTORY_FILE = paths.data("weekly_history.json")

def _week_start(d):                       # Sunday that starts d's week
    return d - timedelta(days=(d.weekday() + 1) % 7)

def _perfect_week_index(d):
    """Ordinal of d's Sun–Sat week within the month, counting EVERY week that has
    at least one day in the month — so the opening partial week is Week 1.
    (e.g. Jul 1–4 = Wk 1, Jul 5–11 = Wk 2, Jul 12–18 = Wk 3, ...)"""
    year, month = d.year, d.month
    ms = date(year, month, 1)
    me = (date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)) - timedelta(days=1)
    ws = ms - timedelta(days=(ms.weekday() + 1) % 7)
    target = _week_start(d)
    idx = 0
    while ws <= me:
        days_in = sum(1 for i in range(7)
                      if (ws + timedelta(days=i)).year == year
                      and (ws + timedelta(days=i)).month == month)
        if days_in >= 1:
            idx += 1
        if ws == target:
            return idx if days_in >= 1 else 0
        ws += timedelta(days=7)
    return idx

def odoo_weekly_breakdown():
    """Current month's Weekly Performance, live from Odoo.

    Cuts the month into Sun–Sat weeks (the opening partial week — e.g. Aug 1
    alone — is Wk 1, the first full Sun–Sat is Wk 2, …, matching how weeks are
    counted here) and asks Postgres for each week's bags. Cumulative bags drive
    the % climb; each week's own bags drive Weekly Sales / Declined By.

    Returns the weekly_history entries (current month only) or None if the DB
    isn't reachable, in which case the caller keeps the sheet-based fallback."""
    try:
        from lib import db, queries
    except Exception:
        return None
    ok, _ = db.check_connection()
    if not ok:
        return None

    # Anchored on the REPORTING month, not today — on the 1st those differ, and
    # using today's rebuilt weekly_history.json as a single "Sep Wk 1" row,
    # wiping August's whole weekly climb out of the August report.
    today   = report_month.live_anchor()
    m_start, m_end = report_month.live_month_window()
    ws      = m_start - timedelta(days=(m_start.weekday() + 1) % 7)   # Sunday of the week holding the 1st

    weeks = []                                            # (seg_start, label, till bags, corporate bags)
    idx = 0
    while ws <= m_end:
        we        = ws + timedelta(days=6)                # Saturday
        seg_start = max(ws, m_start)
        seg_end   = min(we, m_end)
        if seg_start <= seg_end:                          # this Sun–Sat week has in-month days
            idx += 1
            if seg_start <= today:                        # …and it has already started
                win = {"start_date": seg_start.isoformat(), "end_date": seg_end.isoformat()}
                df = db.run_query(queries.BAGS_SOLD_TOTAL,   # same total definition as monthly Sales
                                  {**win, "excluded": queries.excluded_products()})
                pos = int(round(float(df.iloc[0]["bags"]))) if df is not None and not df.empty else 0
                # Corporate bags paid this week — the Sales card's corporate rule over the week's dates
                cdf = db.run_query(queries.CORPORATE_BAGS, win)
                corp = int(cdf.iloc[0]["bags"] or 0) if cdf is not None and not cdf.empty else 0
                weeks.append([seg_start, "Wk " + str(idx), pos, corp])
        ws += timedelta(days=7)
    # Part-paid invoices round down per window, so the weeks' corporate can fall a bag short of the month's;
    # the remainder goes on the latest week so the rows add up to the Sales card.
    if weeks and corporate_bags:
        weeks[-1][3] += corporate_bags - sum(w[3] for w in weeks)

    entries, cum = [], 0
    for seg_start, label, pos, corp in weeks:
        bags = pos + corp
        prev_cum = cum
        cum += bags
        entries.append({
            "weekStart":    seg_start.isoformat(),
            "label":        label,
            "month":        today.strftime("%b"),
            "salesPct":     round((cum / total_target * 100) if total_target else 0, 2),
            "salesBags":    cum,
            "prevSalesPct": round((prev_cum / total_target * 100) if total_target else 0, 2),
            "prevSalesBags": prev_cum,
            "weeklySales":  bags,
            "posBags":      pos,
            "corporateBags": corp,
            "declinedBy":   bags - bare_minimum,
        })
    return entries or None


def update_weekly_history():
    # Prefer the live Odoo per-week breakdown for the CURRENT month (starts fresh
    # at Wk 1 each month). Falls back to the incremental sheet-based history below
    # when Postgres isn't reachable.
    live = odoo_weekly_breakdown()
    if live is not None:
        with open(WEEKLY_HISTORY_FILE, "w") as f:
            json.dump({"weeks": live}, f, indent=2)
        return live

    ref = date.today() - timedelta(days=1)       # data covers through yesterday
    ws  = _week_start(ref)
    wk_idx = _perfect_week_index(ref)
    sales_pct = (total_sales / total_target * 100) if total_target else 0
    # Previous-period bags come from the snapshot current_performance keeps
    prev_bags = 0
    snap = paths.data("previous_snapshot.json")
    if os.path.exists(snap):
        try:
            with open(snap, "r") as f:
                prev_bags = json.load(f).get("previous_week_bags", 0)
        except (ValueError, OSError):
            prev_bags = 0
    # Previous Sales % = the previous-sales bags as a share of the SAME target,
    # so the % column stays consistent with the bags column and trends week to week.
    prev_pct  = (prev_bags / total_target * 100) if total_target else 0
    entry = {
        "weekStart":    ws.isoformat(),
        "label":        ("Wk " + str(wk_idx)) if wk_idx else "Partial",
        "month":        ref.strftime("%b"),
        "salesPct":     round(sales_pct, 2),      # Sales % Achieved
        "salesBags":    total_sales,              # bags behind that %
        "prevSalesPct": round(prev_pct, 2),       # Previous Sales % Achieved
        "prevSalesBags": prev_bags,               # bags behind that %
        "weeklySales":  weekly_sales_total,       # bags sold this week (reference)
        "declinedBy":   weekly_sales_total - bare_minimum,  # +over / -under minimum
    }
    weeks = []
    if os.path.exists(WEEKLY_HISTORY_FILE):
        try:
            with open(WEEKLY_HISTORY_FILE, "r") as f:
                weeks = json.load(f).get("weeks", [])
        except (ValueError, OSError):
            # Corrupt/unparseable (e.g. a git merge conflict left markers in it).
            # Do NOT overwrite — that would wipe the whole trend history. Leave
            # the file for manual repair and skip this run's history update.
            print("  WARNING: weekly_history.json is unreadable (merge conflict?)."
                  " Leaving it untouched — fix the file, then re-run.")
            return []
    weeks = [w for w in weeks if w.get("weekStart") != entry["weekStart"]]
    weeks.append(entry)
    weeks.sort(key=lambda w: w.get("weekStart", ""))
    # Drop hollow weeks: a later week whose cumulative salesBags did not advance
    # past the previous week carries no new data (a new calendar week ran on a
    # stale sheet, e.g. "Wk 2 Aug" duplicating Wk 1's total). Keep only weeks that
    # actually moved the cumulative forward; the week reappears once real data lands.
    _clean = []
    for w in weeks:
        if _clean and w.get("salesBags", 0) <= _clean[-1].get("salesBags", 0):
            continue
        _clean.append(w)
    weeks = _clean
    weeks = weeks[-16:]
    # Number the weeks 1..N within each month, in date order, so the opening
    # (partial) week is Wk 1 — even when it starts in the previous calendar month
    # (e.g. Jun 28 → "Jul" Wk 1). Keyed off each row's own "month" field.
    _month_counts = {}
    for w in weeks:
        m = w.get("month", "")
        _month_counts[m] = _month_counts.get(m, 0) + 1
        w["label"] = "Wk " + str(_month_counts[m])
    with open(WEEKLY_HISTORY_FILE, "w") as f:
        json.dump({"weeks": weeks}, f, indent=2)
    return weeks

weekly_history = update_weekly_history()


# ── FORMAT HELPERS ────────────────────────────────────────────

def fmt_int(n):
    return f"{n:,}"

def fmt_pct(p):
    return f"{p:.2f}%"

def fmt_signed(n):
    return f"+{n:,}" if n > 0 else f"{n:,}"

def fmt_kes(n):
    return f"KES {round(n):,}" if n is not None else ""

def fmt_opt_pct(p):
    return fmt_pct(p) if p is not None else ""


# ── INJECT INTO HTML ──────────────────────────────────────────

inline_script = (
    "<!-- PROJ_DATA_START -->\n"
    "<script>\n"
    "const PROJ = {\n"
    f'  currentDay:               {current_day},\n'
    f'  daysInMonth:              {days_in_month},\n'
    f'  projMonth:                "{proj_month}",\n'
    f'  velocityFactor:           "{velocity_factor:.2f}x",\n'
    f'  totalTarget:              "{fmt_int(total_target)}",\n'
    f'  totalSales:               "{fmt_int(total_sales)}",\n'
    f'  standardProjection:       "{fmt_pct(standard_projection_pct)}",\n'
    f'  forecastedProjection:     "{fmt_pct(forecasted_projection_pct)}",\n'
    f'  corporateBags:            "{fmt_int(corporate_bags)}",\n'
    f'  corporateKes:             "{fmt_kes(corporate_kes) if corporate_kes else ""}",\n'
    f'  standardRevenue:          "{fmt_kes(standard_revenue)}",\n'
    f'  forecastedRevenue:        "{fmt_kes(forecasted_revenue)}",\n'
    f'  revenueTarget:            "{fmt_kes(revenue_target) if revenue_target else ""}",\n'
    f'  standardRevenuePct:       "{fmt_opt_pct(standard_revenue_pct)}",\n'
    f'  forecastedRevenuePct:     "{fmt_opt_pct(forecasted_revenue_pct)}",\n'
    f'  priceMix:                 {json.dumps(price_mix)},\n'
    f'  bareMinimum:              "{fmt_int(bare_minimum_value) if bare_minimum_value else ""}",\n'
    f'  bareMinimumGrowthPct:     "{fmt_pct(bare_minimum_growth_pct)}",\n'
    f'  declinedBy:               "{("-" + fmt_int(abs(declined_by))) if bare_minimum_value else ""}",\n'
    f'  weeklySalesTotal:         "{fmt_int(weekly_sales_total)}",\n'
    f'  weeklyHistory:            {json.dumps(weekly_history)}\n'
    "};\n"
    "</script>\n"
    "<!-- PROJ_DATA_END -->"
)

proj_html_path  = paths.html("forward_projections.html")
combined_path   = paths.html("current_performance.html")

def _inject(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(
        r"<!-- PROJ_DATA_START -->.*?<!-- PROJ_DATA_END -->",
        lambda _m: inline_script,     # a function, so backslashes in the JSON (–) stay literal
        content,
        flags=re.DOTALL
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

_inject(proj_html_path)   # keep standalone file up to date
_inject(combined_path)    # inject into the combined dashboard

# Refresh PERF data so both blocks are up to date before the browser opens.
# Skip when launched from main.py — it already runs current_performance.py
# right before this, so re-running here just wastes Google Sheets read quota.
if not os.environ.get("DENRI_LAUNCHER"):
    subprocess.run([sys.executable, paths.generator("current_performance.py")], check=True)

if not os.environ.get("DENRI_LAUNCHER"):
    webbrowser.open_new_tab(pathlib.Path(combined_path).as_uri())

print("forward_projections data injected; dashboard updated.")
print(f"  Data through          : {yesterday.strftime('%d %b %Y')}  (day {current_day} of {days_in_month})")
print(f"  Velocity factor       : {velocity_factor:.2f}x")
print(f"  Total Target (bags)   : {fmt_int(total_target)}")
print(f"  Total Sales  ({'Odoo' if sales_is_live else 'sheet'})  : {fmt_int(total_sales)}")
print(f"  Standard Proj.        : {fmt_pct(standard_projection_pct)}")
print(f"  Forecasted Proj.      : {fmt_pct(forecasted_projection_pct)}  (incl. {fmt_int(corporate_bags)} corporate)")
print(f"  Standard revenue      : {fmt_kes(standard_revenue) or '(no live month value)'}  {fmt_opt_pct(standard_revenue_pct)}")
print(f"  Forecasted revenue    : {fmt_kes(forecasted_revenue) or '(no live month value)'}  {fmt_opt_pct(forecasted_revenue_pct)}  (incl. {fmt_kes(corporate_kes)} corporate)")
print(f"  Revenue target        : {fmt_kes(revenue_target) if revenue_target else '(none)'}")
if price_mix:
    print(f"  Price per bag         : {fmt_kes(price_mix['actualPpb'])} actual vs {fmt_kes(price_mix['targetPpb'])} target ({price_mix['gapPct']:+.1f}%)")
print(f"  Perfect weeks / month : {perfect_weeks}")
print(f"  Bare Minimum          : {fmt_int(bare_minimum_value)}  (= {fmt_int(total_target)} / {perfect_weeks})")
print(f"  Bare Min Growth %     : {fmt_pct(bare_minimum_growth_pct)}")
print(f"  Weekly Sales (col X)  : {fmt_int(weekly_sales_total)}")
print(f"  Declined By           : {'-' + fmt_int(abs(declined_by)) if bare_minimum_value else '(bare minimum not set)'}")
