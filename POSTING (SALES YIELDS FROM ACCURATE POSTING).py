"""
POSTING (SALES YIELDS FROM ACCURATE POSTING).py
─────────────────────────────────────────────────────────────────
Kenya & Sinza – Posting Yield Analysis

Column mapping per region:
  MONTHLY_SALES          Kenya → col X (idx 23)   Sinza → col R (idx 17)
  MONTHLY_MARKETING_POST Kenya → col E (idx  4)   Sinza → col F (idx  5)
  STOCK_LEVELS           Kenya → col Y (idx 24)   Sinza → col Y (idx 24)

Social funnel:
  Kenya :  225,000 × 5% × 1% × 2% = 2.25  expected sales per post
  Sinza :    2,160 × 5% × 1% × 2% = 0.0216 expected sales per post

Three analytical sections per region:
  1. Sales Achieved from Marketing Posting
       bags where expected_pct > 0  AND expected_sales > 0
  2. Sales Without Being Posted
       MONTHLY_SALES (sales > 0) with no match in MONTHLY_MARKETING_POST
  3. Accuracy of Marketing Posting
       STOCK_LEVELS (stock > 0) ∩ MONTHLY_MARKETING_POST (posts > 0)
─────────────────────────────────────────────────────────────────
"""

import re, webbrowser, os, pathlib, json, datetime

SPREADSHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"

# ── WEEK COUNTER ─────────────────────────────────────────────

def count_complete_weeks_in_month():
    """Count Mon–Sun weeks in the current month that have ≥5 days falling within that month."""
    today = datetime.date.today()
    year, month = today.year, today.month
    month_start = datetime.date(year, month, 1)
    if month == 12:
        month_end = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        month_end = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
    week_start = month_start - datetime.timedelta(days=month_start.weekday())
    complete = 0
    while week_start <= month_end:
        days_in_month = sum(
            1 for i in range(7)
            if (week_start + datetime.timedelta(days=i)).year  == year
            and (week_start + datetime.timedelta(days=i)).month == month
        )
        if days_in_month >= 5:
            complete += 1
        week_start += datetime.timedelta(days=7)
    return max(complete, 1)


# ── FUNNEL CONSTANTS ──────────────────────────────────────────
KENYA_SPP = 225_000 * 0.05 * 0.01 * 0.02   # 2.25  expected sales per post
SINZA_SPP  =  140000 * 0.05 * 0.01 * 0.02   # expected sales per post
UGANDA_SPP =   2_160 * 0.05 * 0.01 * 0.02   # 0.0216 expected sales per post


# ── GOOGLE SHEETS AUTH ────────────────────────────────────────

# Shared auth: service account (permanent) or self-healing OAuth — see google_auth.py
from google_auth import get_gspread_client


# ── HELPERS ───────────────────────────────────────────────────

def safe_int(val):
    try:
        return int(float(str(val).replace(",", "")))
    except (ValueError, TypeError):
        return 0

def fmt_int(n):
    return f"{n:,}"

def _is_checked(row, col_idx):
    """Return True if the cell at col_idx holds a checkmark/truthy value, or if no filter is set."""
    if col_idx is None:
        return True
    if len(row) <= col_idx:
        return False
    cell = str(row[col_idx]).strip()
    # Any checkmark character present (✅ U+2705, ✔ U+2714, ✓ U+2713, ☑ U+2611, heavy check)
    if any(c in cell for c in ("✅", "✔", "✓", "☑", "🗸", "🗹")):
        return True
    return cell.upper() in ("TRUE", "1", "YES")

def _is_x(row, col_idx):
    """Return True if the cell at col_idx holds an 'x' / cross mark (marks 'not posted')."""
    if col_idx is None or len(row) <= col_idx:
        return False
    cell = str(row[col_idx]).strip()
    if any(c in cell for c in ("❌", "✗", "✘", "🗙", "☒")):
        return True
    return cell.upper() == "X"

# Key functions: same column structure for both regions
def _ms_key(row):
    """MONTHLY_SALES: colour=A(0), product_name=B(1)"""
    return (str(row[0]).lower().strip(), str(row[1]).lower().strip())

def _mmp_key(row):
    """MONTHLY_MARKETING_POST: colour=A(0), product_name=C(2)"""
    return (str(row[0]).lower().strip(), str(row[2]).lower().strip())

def _sl_key(row):
    """STOCK_LEVELS: colour=A(0), product_name=C(2)"""
    return (str(row[0]).lower().strip(), str(row[2]).lower().strip())


# ── REGIONAL ANALYSIS ─────────────────────────────────────────

def _analyze_region(ms_rows, mmp_rows, sl_rows,
                    sales_col, post_col, stock_col, spp, region,
                    ms_check_col=None, mmp_check_col=None, sl_check_col=None):
    """
    Runs all three posting sections for one region.

    sales_col  – column index in MONTHLY_SALES for the region's sales total
    post_col   – column index in MONTHLY_MARKETING_POST for the region's post count
    stock_col  – column index in STOCK_LEVELS for the region's stock level
    spp        – expected sales per post  (followers × reach × click × conversion)
    """

    # ── Build sales_map from MONTHLY_SALES ────────────────────
    sales_map = {}
    for row in ms_rows[1:]:
        if len(row) < 2:
            continue
        if not _is_checked(row, ms_check_col):
            continue
        colour       = str(row[0]).strip()
        product_name = str(row[1]).strip()
        sales_total  = safe_int(row[sales_col]) if len(row) > sales_col else 0
        if not product_name:
            continue
        k = _ms_key(row)
        if k not in sales_map:
            sales_map[k] = {"colour": colour, "productName": product_name, "salesTotal": 0}
        sales_map[k]["salesTotal"] += sales_total

    # ── Build post_map from MONTHLY_MARKETING_POST ────────────
    post_map = {}
    for row in mmp_rows[1:]:
        if len(row) < 3:
            continue
        if not _is_checked(row, mmp_check_col):
            continue
        colour       = str(row[0]).strip()
        bag_type_mmp = str(row[1]).strip()
        product_name = str(row[2]).strip()
        post_count   = safe_int(row[post_col]) if len(row) > post_col else 0
        if not product_name or post_count == 0:
            continue
        k = _mmp_key(row)
        if k not in post_map:
            post_map[k] = {"colour": colour, "category": bag_type_mmp,
                           "productName": product_name, "postingTotal": 0}
        post_map[k]["postingTotal"] += post_count

    # ── Build stock_map from STOCK_LEVELS ─────────────────────
    stock_map = {}
    for row in sl_rows[1:]:
        if len(row) < 4:
            continue
        if not _is_checked(row, sl_check_col):
            continue
        product_name = str(row[2]).strip()
        bag_type     = str(row[3]).strip()
        stock_val    = safe_int(row[stock_col]) if len(row) > stock_col else 0
        if not product_name and not bag_type:
            continue
        k = _sl_key(row)
        if k not in stock_map:
            stock_map[k] = {"bagType": bag_type, "stock": 0}
        stock_map[k]["stock"] += stock_val

    # ── Check-column diagnostics ───────────────────────────────
    for label, rows, col in [("MONTHLY_SALES col AB", ms_rows, ms_check_col),
                              ("MONTHLY_MARKETING_POST col I", mmp_rows, mmp_check_col),
                              ("STOCK_LEVELS col AB", sl_rows, sl_check_col)]:
        if col is None:
            continue
        samples = []
        for r in rows[1:6]:       # first 5 data rows
            val = r[col] if len(r) > col else "<row too short>"
            samples.append(repr(val))
        print(f"  [{region}] {label} sample values: {samples}")

    # ── Diagnostics ────────────────────────────────────────────
    overlap             = set(sales_map.keys()) & set(post_map.keys())
    overlap_with_sales  = overlap & {k for k, v in sales_map.items() if v["salesTotal"] > 0}
    print(f"\n  ── {region}  (sales_col={sales_col}  post_col={post_col}) ────────────────────")
    print(f"  Sales entries       : {len(sales_map)}")
    print(f"  Unique bags posted  : {len(post_map)}")
    print(f"  Stock entries       : {len(stock_map)}")
    print(f"  Keys in BOTH maps   : {len(overlap)}")
    print(f"  Keys w/ sales > 0   : {len(overlap_with_sales)}  ← drives Section 1")

    # ── Sections 1 & 2: iterate MONTHLY_SALES ─────────────────
    sales_from_posting = []
    sales_no_post      = []

    for k, sale in sales_map.items():
        sales_total   = sale["salesTotal"]
        post_entry    = post_map.get(k)
        posting_count = post_entry["postingTotal"] if post_entry else 0
        stock_info    = stock_map.get(k, {"bagType": "", "stock": 0})

        expected_sales = round(posting_count * spp, 4)
        expected_pct   = (
            round(min(sales_total / expected_sales, 1.0) * 100, 1)
            if expected_sales > 0 else 0.0
        )

        enriched = {
            "colour":        sale["colour"],
            "category":      post_entry["category"] if post_entry else "",
            "productName":   sale["productName"],
            "bagType":       stock_info["bagType"],
            "stock":         stock_info["stock"],
            "postingTotal":  posting_count,
            "salesTotal":    sales_total,
            "expectedSales": expected_sales,
            "expectedPct":   expected_pct,
        }

        # Section 1: expected_pct > 0 AND expected_sales > 0
        # Section 1: expected_pct > 0 AND expected_sales > 0
        if expected_pct > 0 and expected_sales > 0:
            sales_from_posting.append(enriched)
        # Section 2: sold but never posted
        elif sales_total > 0 and posting_count == 0:
            sales_no_post.append(enriched)

    # ── Section 3: STOCK_LEVELS (stock>0) ∩ MONTHLY_MARKETING_POST ──
    accuracy_bags = []
    for k, stock_info in stock_map.items():
        if stock_info["stock"] <= 0:
            continue
        post_entry = post_map.get(k)
        if not post_entry:
            continue
        posting_count  = post_entry["postingTotal"]
        sale           = sales_map.get(k)
        sales_total    = sale["salesTotal"] if sale else 0
        expected_sales = round(posting_count * spp, 4)
        expected_pct   = (
            round(min(sales_total / expected_sales, 1.0) * 100, 1)
            if expected_sales > 0 else 0.0
        )

        accuracy_bags.append({
            "colour":        post_entry["colour"],
            "category":      post_entry["category"],
            "productName":   post_entry["productName"],
            "bagType":       stock_info["bagType"],
            "stock":         stock_info["stock"],
            "postingTotal":  posting_count,
            "salesTotal":    sales_total,
            "expectedSales": expected_sales,
            "expectedPct":   expected_pct,
        })

    sales_from_posting.sort(key=lambda x: -x["expectedPct"])
    sales_no_post.sort(key=lambda x:      -x["salesTotal"])
    accuracy_bags.sort(key=lambda x:      (-x["stock"], -x["postingTotal"]))

    s1_count            = len(sales_from_posting)
    s2_count            = len(sales_no_post)
    s3_count            = len(accuracy_bags)
    s3_not_posted_count = sum(1 for k, si in stock_map.items() if si["stock"] > 0 and k not in post_map)
    s1_sales            = sum(b["salesTotal"]    for b in sales_from_posting)
    s2_sales            = sum(b["salesTotal"]    for b in sales_no_post)
    s1_posts            = sum(b["postingTotal"]  for b in sales_from_posting)
    s1_expected         = round(sum(b["expectedSales"] for b in sales_from_posting), 2)

    print(f"  1. Bags sold via posting : {s1_count}  (sales: {fmt_int(s1_sales)}, posts: {fmt_int(s1_posts)})")
    print(f"  2. Sold w/o posting      : {s2_count}  (sales: {fmt_int(s2_sales)})")
    print(f"  3. Accuracy bags         : {s3_count}  (not posted: {s3_not_posted_count})")

    return {
        "salesFromPosting":  sales_from_posting,
        "salesNoPost":       sales_no_post,
        "accuracyBags":      accuracy_bags,
        "s1Count":           s1_count,
        "s2Count":           s2_count,
        "s3Count":           s3_count,
        "s3NotPostedCount":  s3_not_posted_count,
        "s1Sales":           fmt_int(s1_sales),
        "s2Sales":           fmt_int(s2_sales),
        "s1Posts":           s1_posts,
        "s1Expected":        fmt_int(round(s1_expected)),
    }


# ── NO-CONVERT HELPER ─────────────────────────────────────────

def _build_no_convert(post_rows, sales_rows, sales_col_indices,
                      check_col, count_col, sl_rows, stock_col, spp,
                      sales_check_col=None):
    """
    Bags that were posted (check_col has x or ✅) but have zero sales.
    Returns list of {colour, category, productName, bagType, stock, postingTotal, expectedSale}.
    """
    # stock_map: (colour, product_C) → {bagType, stock}
    stock_map = {}
    for row in sl_rows[1:]:
        if len(row) < 4:
            continue
        k = (str(row[0]).lower().strip(), str(row[2]).lower().strip())
        if k not in stock_map:
            stock_map[k] = {"bagType": str(row[3]).strip(), "stock": 0}
        if len(row) > stock_col:
            stock_map[k]["stock"] += safe_int(row[stock_col])

    # sales_map: (colour, product_B) → total across given columns
    sales_map = {}
    for row in sales_rows[1:]:
        if len(row) < 2:
            continue
        if sales_check_col is not None and not (_is_checked(row, sales_check_col) or _is_x(row, sales_check_col)):
            continue
        k = (str(row[0]).lower().strip(), str(row[1]).lower().strip())
        total = sum(safe_int(row[c]) for c in sales_col_indices if len(row) > c)
        sales_map[k] = sales_map.get(k, 0) + total

    result = []
    seen = set()
    for row in post_rows[1:]:
        if len(row) < 3:
            continue
        if not (_is_checked(row, check_col) or _is_x(row, check_col)):
            continue
        colour       = str(row[0]).strip()
        category     = str(row[1]).strip()
        product_name = str(row[2]).strip()
        if not product_name:
            continue
        k = (colour.lower(), product_name.lower())
        if k in seen:
            continue
        seen.add(k)
        if sales_map.get(k, 0) > 0:
            continue          # has sales — not a no-convert
        post_count = safe_int(row[count_col]) if len(row) > count_col else 0
        if post_count <= 0:
            continue          # not actually posted this week — exclude
        stock_info = stock_map.get(k, {"bagType": "", "stock": 0})
        result.append({
            "colour":       colour,
            "category":     category,
            "productName":  product_name,
            "bagType":      stock_info["bagType"],
            "stock":        stock_info["stock"],
            "postingTotal": post_count,
            "expectedSale": round(post_count * spp, 4),
            "onOffer":      _is_checked(row, check_col),   # ✅ = on offer, x = not on offer
        })

    result.sort(key=lambda x: -x["expectedSale"])
    return result


def _posted_stock(wmp_rows, sl_rows, post_col, check_col, stock_col):
    """Current stock for bags marketing POSTED (col post_col > 0, flagged ✅/x).
    Returns { 'colour|name': {colour, productName, category, bagType, stock} }."""
    posted = {}
    for row in wmp_rows[1:]:
        if len(row) > post_col and safe_int(row[post_col]) > 0 and (_is_checked(row, check_col) or _is_x(row, check_col)):
            name = str(row[2]).strip()
            if not name:
                continue
            key = str(row[0]).lower().strip() + '|' + name.lower()
            if key not in posted:
                posted[key] = {"colour": str(row[0]).strip(), "productName": name,
                               "category": str(row[1]).strip(), "bagType": "", "stock": 0}
    for row in sl_rows[1:]:
        if len(row) < 4:
            continue
        key = str(row[0]).lower().strip() + '|' + str(row[2]).lower().strip()
        if key in posted:
            posted[key]["bagType"] = str(row[3]).strip()
            posted[key]["stock"] += safe_int(row[stock_col]) if len(row) > stock_col else 0
    return posted


# ── WEEKLY REGION (generic for Sinza / Uganda) ────────────────

def _fetch_weekly_region(wmp_rows, ws_rows, post_col, check_col, sales_col, offer_col, spp):
    """
    Generic weekly fetch for Sinza / Uganda.
    WMP: posts in post_col where check_col = ✅
    WS:  sales in sales_col where offer_col = ✅ (posted/on-offer)
         unposted in sales_col where offer_col = x
    WS SUM TOTAL row: sales_col
    """
    wk_posts = sum(
        safe_int(row[post_col])
        for row in wmp_rows[1:]
        if len(row) > check_col and _is_checked(row, check_col)
    )
    wk_expected = round(wk_posts * spp, 2)
    wk_sales = sum(
        safe_int(row[sales_col])
        for row in ws_rows[1:]
        if len(row) > offer_col and _is_checked(row, offer_col)
    )
    wk_unposted = sum(
        safe_int(row[sales_col])
        for row in ws_rows[1:]
        if len(row) > offer_col and _is_x(row, offer_col)
    )
    wk_sum_total = 0
    for row in ws_rows:
        if str(row[2]).strip().upper() == "SUM TOTAL":
            wk_sum_total = safe_int(row[sales_col]) if len(row) > sales_col else 0
            break
    return {
        'wkPosts':      wk_posts,
        'wkSales':      wk_sales,
        'wkExpected':   round(wk_expected, 2),
        'wkUnposted':   wk_unposted,
        'wkSumTotal':   wk_sum_total,
        'wkOnOffer':    wk_sales,
        'wkNotOnOffer': wk_unposted,
    }


# ── WEEKLY KENYA ──────────────────────────────────────────────

def _fetch_weekly_kenya(sh, sl_rows):
    """
    Weekly Kenya figures for the S1 KPI card.
    WEEKLY_MARKETING_POST: sum col E (idx 4) where col I (idx 8) is checked
    WEEKLY_SALES: sum cols E–Q (4–16) + T–W (19–22) where col Y (idx 24) is checked
    """
    wmp_rows = sh.worksheet("WEEKLY_MARKETING_POST").get_all_values()
    ws_rows  = sh.worksheet("WEEKLY_SALES").get_all_values()

    weekly_posts = sum(
        safe_int(row[4])
        for row in wmp_rows[1:]
        if len(row) > 4 and _is_checked(row, 8)
    )

    # Bags Not On Offer: col I = x
    weekly_posts_x = sum(
        safe_int(row[4])
        for row in wmp_rows[1:]
        if len(row) > 4 and _is_x(row, 8)
    )

    # Expected sales = each row's posts (col E) × KENYA_SPP, summed (checked rows only)
    weekly_expected = sum(
        safe_int(row[4]) * KENYA_SPP
        for row in wmp_rows[1:]
        if len(row) > 4 and _is_checked(row, 8)
    )

    # Sales without posting: WMP col I = x AND col E > 0 → names → WS col AB sum
    _wmp_not_posted = {
        str(row[2]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > 8 and _is_x(row, 8) and safe_int(row[4]) > 0
    }
    weekly_sales_no_post = sum(
        safe_int(row[27])
        for row in ws_rows[1:]
        if len(row) > 27
        and not any(str(cell).strip().upper() == "SUM TOTAL" for cell in row[:5])
        and str(row[2]).lower().strip() in _wmp_not_posted
    )

    # WMP lookup: (colour, product_name) → (col_I_checked, col_E_gt0)
    # Check 1: col I = ✅  |  Check 2: col E > 0
    wmp_info_wk = {}
    for row in wmp_rows[1:]:
        if len(row) < 3:
            continue
        key = str(row[2]).lower().strip()   # match on product name (col C) only
        wmp_info_wk[key] = (
            _is_checked(row, 8) if len(row) > 8 else False,  # col I
            safe_int(row[4]) > 0 if len(row) > 4 else False,  # col E > 0
        )

    # WEEKLY_SALES shop-sales columns: E→Q (idx 4-16) + T→W (idx 19-22)
    _WS_SHOP_COLS = list(range(4, 17)) + list(range(19, 23))

    # 4-way split of WEEKLY_SALES
    # Posted   = WMP col I = ✅ (check 1) AND WMP col E > 0 (check 2)
    # On Offer = WS  col Y = ✅ (check 1) AND WS  sum(E:Q,T:W) > 0 (check 2)
    # offer_posted_wk   → shop-cols sum (E:Q+T:W) for "Bags Posted & On Offer" card
    # offer_posted_wk_x → col X total for "Total Sales with Posting (Weekly)" card
    weekly_sales          = 0
    offer_posted_wk       = 0
    offer_posted_wk_x     = 0
    offer_posted_wk_count = 0   # count of WS rows where posted & on offer
    not_offer_posted_wk     = 0
    offer_not_posted_wk     = 0
    not_offer_not_posted_wk = 0

    for row in ws_rows[1:]:
        if len(row) < 3:
            continue
        if any(str(cell).strip().upper() == "SUM TOTAL" for cell in row[:5]):
            continue
        row_total = safe_int(row[23]) if len(row) > 23 else 0

        key = str(row[2]).lower().strip()   # match on product name (col C) only
        wmp_col_i, wmp_col_e = wmp_info_wk.get(key, (False, False))
        ws_col_y  = _is_checked(row, 24)
        ws_ab     = safe_int(row[27]) if len(row) > 27 else 0
        ws_sum    = sum(safe_int(row[c]) for c in _WS_SHOP_COLS if len(row) > c)

        # weekly posted totals (driven by WS col Y)
        if ws_col_y:
            weekly_sales += row_total

        is_posted   = wmp_col_i and wmp_col_e   # WMP col I ✅ AND col E > 0
        is_on_offer = ws_col_y                  # WS  col Y ✅

        # Total Posts Made + Total Sales with Posting: WMP name match only, no WS Y filter
        if is_posted:
            offer_posted_wk_count += ws_ab      # sum WS col AB → "Total Posts Made" = 261
            offer_posted_wk_x     += row_total  # sum WS col X  → "Total Sales with Posting" = 415

        # four-way split for Bags Posted/On Offer cards
        if is_posted and is_on_offer:
            offer_posted_wk += ws_sum
        elif is_posted and not is_on_offer:
            offer_not_posted_wk += ws_sum
        elif not is_posted and is_on_offer:
            not_offer_posted_wk += ws_sum
        else:
            not_offer_not_posted_wk += ws_sum

    # Total Sales w/o Posting: WMP col E = 0 → names → WS col AB sum
    _wmp_zero_post_names = {
        str(row[2]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > 4 and safe_int(row[4]) == 0
    }
    weekly_unposted = sum(
        safe_int(row[27])
        for row in ws_rows[1:]
        if len(row) > 27
        and not any(str(cell).strip().upper() == "SUM TOTAL" for cell in row[:5])
        and str(row[2]).lower().strip() in _wmp_zero_post_names
    )

    # S3: total posts done (col E) where col I has x OR ✅
    s3_wk_posts = sum(
        safe_int(row[4])
        for row in wmp_rows[1:]
        if len(row) > 4 and (_is_checked(row, 8) or _is_x(row, 8))
    )

    # No-convert weekly: posted (col I checked) but zero WEEKLY_SALES
    nc_wk = _build_no_convert(
        post_rows=wmp_rows,
        sales_rows=ws_rows,
        sales_col_indices=list(range(4, 17)) + list(range(19, 23)),
        check_col=8, count_col=4,
        sl_rows=sl_rows, stock_col=24,
        spp=KENYA_SPP,
        sales_check_col=24,   # only count sales where col Y is checked
    )

    # Kenya total bags sold this week = SUM TOTAL row, WEEKLY_SALES col AB (idx 27)
    # (col AB is the Kenya sales column; all posting splits below also read col AB).
    proj_weekly_sales = 0
    for row in ws_rows:
        if any(str(cell).strip().upper() == "SUM TOTAL" for cell in row[:5]):
            proj_weekly_sales = safe_int(row[27]) if len(row) > 27 else 0
            break

    # S3 weekly accuracy: in-stock bags posted vs not posted in WMP
    sl_stock_keys = set()
    for row in sl_rows[1:]:
        if len(row) > 24 and safe_int(row[24]) > 20:
            sl_stock_keys.add((str(row[0]).lower().strip(), str(row[2]).lower().strip()))
    wmp_posted_keys = set()
    for row in wmp_rows[1:]:
        if len(row) > 4 and safe_int(row[4]) > 0:
            wmp_posted_keys.add((str(row[0]).lower().strip(), str(row[2]).lower().strip()))
    wk_instock_posted     = len(sl_stock_keys & wmp_posted_keys)
    not_posted_keys       = sl_stock_keys - wmp_posted_keys
    wk_instock_not_posted = len(not_posted_keys)

    # Detail rows for the in-stock & not posted table
    instock_not_posted_list = []
    for row in sl_rows[1:]:
        if len(row) > 24 and safe_int(row[24]) > 20:
            key = (str(row[0]).lower().strip(), str(row[2]).lower().strip())
            if key in not_posted_keys:
                instock_not_posted_list.append({
                    "colour":        str(row[0]).strip(),
                    "category":      str(row[1]).strip() if len(row) > 1 else "",
                    "productName":   str(row[2]).strip(),
                    "bagType":       str(row[3]).strip() if len(row) > 3 else "",
                    "stock":         safe_int(row[24]),
                    "expectedSales": KENYA_SPP,
                })
    instock_not_posted_list.sort(key=lambda x: -x["stock"])

    print(f"\n  ── Kenya Weekly ──────────────────────────────────────────")
    print(f"  Weekly posts (WEEKLY_MARKETING_POST col E, check I): {weekly_posts}")
    print(f"  Weekly sales (WEEKLY_SALES cols E–Q+T–W, check Y)  : {fmt_int(weekly_sales)}")
    print(f"  Weekly expected (posts × {KENYA_SPP})                : {fmt_int(round(weekly_expected))}")
    print(f"  Weekly unposted (WEEKLY_SALES E–Q+T–W, x in Y)     : {fmt_int(weekly_unposted)}")
    print(f"  S3 weekly posts (WEEKLY_MARKETING_POST col E, x or ✅ in I): {s3_wk_posts}")
    print(f"  No-convert weekly bags                              : {len(nc_wk)}")
    print(f"  Posted & On Offer wk      (WMP✅ + WS✅): {offer_posted_wk}")
    print(f"  Posted & Not on Offer wk  (WMP✅ + WSx): {offer_not_posted_wk}")
    print(f"  Not Posted & On Offer wk  (WMPx + WS✅): {not_offer_posted_wk}")
    print(f"  Not Posted & Not on Offer wk(WMPx + WSx): {not_offer_not_posted_wk}")
    print(f"  In-Stock & Posted (distinct bags, wk)     : {wk_instock_posted}")
    print(f"  In-Stock & Not Posted (distinct bags, wk) : {wk_instock_not_posted}")

    # Sales Achieved % (weekly): per-bag yield/posts ratio, then average
    # WMP: col I (✅ or x) AND col E > 0 → {name: sum col E}
    wmp_posts_map = {}
    for row in wmp_rows[1:]:
        if len(row) < 3:
            continue
        if not (_is_checked(row, 8) or _is_x(row, 8)):
            continue
        col_e = safe_int(row[4]) if len(row) > 4 else 0
        if col_e <= 0:
            continue
        name = str(row[2]).lower().strip()
        wmp_posts_map[name] = wmp_posts_map.get(name, 0) + col_e

    # WS: col Y (✅ or x) AND col AB > 0 → {name: sum col AB}
    ws_yield_map = {}
    for row in ws_rows[1:]:
        if len(row) < 3:
            continue
        if any(str(cell).strip().upper() == "SUM TOTAL" for cell in row[:5]):
            continue
        if not (_is_checked(row, 24) or _is_x(row, 24)):
            continue
        col_ab = safe_int(row[27]) if len(row) > 27 else 0
        if col_ab <= 0:
            continue
        name = str(row[2]).lower().strip()
        ws_yield_map[name] = ws_yield_map.get(name, 0) + col_ab

    # Per-bag %: min((yield / posts) × 100, 100) — 0% if posted but no yield
    bag_pcts = []
    for name, posts in wmp_posts_map.items():
        yield_val = ws_yield_map.get(name, 0)
        bag_pcts.append(min((yield_val / posts) * 100, 100.0) if posts > 0 else 0.0)

    wk_mkt_pct = round(sum(bag_pcts) / len(bag_pcts), 1) if bag_pcts else 0.0
    print(f"  Mkt % wk  : {len(bag_pcts)} bags, avg {wk_mkt_pct}%")

    # Sales Achieved from Marketing Posting (Weekly)(Bags Not on Offer %): per-bag avg
    # WMP col I=x, col E>0 → posts per bag; WS col Y=x, col AB>0 → yield per bag
    wmp_x_posts_map = {}
    for row in wmp_rows[1:]:
        if len(row) < 3 or not _is_x(row, 8):
            continue
        col_e = safe_int(row[4]) if len(row) > 4 else 0
        if col_e <= 0:
            continue
        name = str(row[2]).lower().strip()
        wmp_x_posts_map[name] = wmp_x_posts_map.get(name, 0) + col_e

    ws_x_yield_map = {}
    for row in ws_rows[1:]:
        if len(row) < 3:
            continue
        if any(str(cell).strip().upper() == "SUM TOTAL" for cell in row[:5]):
            continue
        if not _is_x(row, 24):
            continue
        col_ab = safe_int(row[27]) if len(row) > 27 else 0
        if col_ab <= 0:
            continue
        name = str(row[2]).lower().strip()
        ws_x_yield_map[name] = ws_x_yield_map.get(name, 0) + col_ab

    bag_pcts_x = []
    for name, posts in wmp_x_posts_map.items():
        yield_val = ws_x_yield_map.get(name, 0)
        bag_pcts_x.append(min((yield_val / posts) * 100, 100.0) if posts > 0 else 0.0)

    wk_not_offer_mkt_pct = round(sum(bag_pcts_x) / len(bag_pcts_x), 1) if bag_pcts_x else 0.0
    print(f"  Mkt % wk (not-offer): {len(bag_pcts_x)} bags, avg {wk_not_offer_mkt_pct}%")

    # Bags Not Posted & On Offer (Weekly): WMP col I=✅, col E=0 → names col C → WS col C match → sum col AB
    _wmp_chk_zero_wk = {
        str(row[2]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > 8 and _is_checked(row, 8) and safe_int(row[4]) == 0 and str(row[2]).strip()
    }
    offer_not_posted_wk_sales = sum(
        safe_int(row[27])
        for row in ws_rows[1:]
        if len(row) > 27
        and not any(str(cell).strip().upper() == "SUM TOTAL" for cell in row[:5])
        and str(row[2]).lower().strip() in _wmp_chk_zero_wk
    )

    # Bags Not Posted & Not on Offer (Weekly): WMP col I=x, col E=0 → names col C → WS col C match → sum col AB
    _wmp_x_zero_wk = {
        str(row[2]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > 8 and _is_x(row, 8) and safe_int(row[4]) == 0 and str(row[2]).strip()
    }
    not_offer_not_posted_wk_sales = sum(
        safe_int(row[27])
        for row in ws_rows[1:]
        if len(row) > 27
        and not any(str(cell).strip().upper() == "SUM TOTAL" for cell in row[:5])
        and str(row[2]).lower().strip() in _wmp_x_zero_wk
    )

    return (weekly_posts, weekly_sales, weekly_expected, weekly_unposted, s3_wk_posts, nc_wk,
            not_offer_posted_wk, offer_not_posted_wk, offer_posted_wk, not_offer_not_posted_wk,
            wk_instock_posted, wk_instock_not_posted, proj_weekly_sales, instock_not_posted_list,
            offer_posted_wk_x, offer_posted_wk_count,
            weekly_posts_x, weekly_sales_no_post, wk_mkt_pct,
            not_offer_not_posted_wk_sales, wk_not_offer_mkt_pct,
            offer_not_posted_wk_sales)


def _fetch_monthly_kenya(ms_rows, mmp_rows):
    """
    Monthly Kenya figures for the S1 KPI cards.
    MONTHLY_MARKETING_POST: sum col E (idx 4) where col I (idx 8) is checked
    MONTHLY_SALES: sum col X (idx 23) where col AB (idx 27) is checked
    """
    monthly_posts = sum(
        safe_int(row[4])
        for row in mmp_rows[1:]
        if len(row) > 4 and _is_checked(row, 8)
    )

    # posted names from MMP: col I ✅ AND col E > 0 → col C (idx 2)
    _mmp_posted = {
        str(row[2]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > 8 and _is_checked(row, 8) and safe_int(row[4]) > 0
    }
    # sum MONTHLY_SALES col X (idx 23) where col B (idx 1) matches a posted name
    monthly_sales = sum(
        safe_int(row[23])
        for row in ms_rows[1:]
        if len(row) > 23 and str(row[1]).lower().strip() in _mmp_posted
    )

    # Bags Not On Offer monthly: col I = x
    monthly_posts_x = sum(
        safe_int(row[4])
        for row in mmp_rows[1:]
        if len(row) > 4 and _is_x(row, 8)
    )

    # Sales without posting monthly: MMP col I = x AND col E > 0 → names → MS col B match → col X sum
    _mmp_not_posted = {
        str(row[2]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > 8 and _is_x(row, 8) and safe_int(row[4]) > 0
    }
    monthly_sales_no_post = sum(
        safe_int(row[23])
        for row in ms_rows[1:]
        if len(row) > 23 and str(row[1]).lower().strip() in _mmp_not_posted
    )

    # S2 monthly unposted: col X (idx 23) where col AB (idx 27) has an "x"
    # Total Sales w/o Posting (Monthly): MMP col E = 0 → names (col C) → MS col B match → sum col AF
    _mmp_any_posted = {
        str(row[2]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > 4 and safe_int(row[4]) > 0 and str(row[2]).strip()
    }
    _mmp_zero_post_names = {
        str(row[2]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > 4
        and str(row[2]).strip()                          # non-empty name
        and str(row[4]).strip() == '0'                   # explicitly zero, not blank
        and str(row[2]).lower().strip() not in _mmp_any_posted  # never posted elsewhere
    }
    monthly_unposted = sum(
        safe_int(row[23])   # MS col X = monthly Kenya sales (col AF/31 was empty → wrong total)
        for row in ms_rows[1:]
        if len(row) > 23 and str(row[1]).lower().strip() in _mmp_zero_post_names
    )

    # S2 monthly total: col X (idx 23) where col AB has x OR ✅
    monthly_total = sum(
        safe_int(row[23])
        for row in ms_rows[1:]
        if len(row) > 23 and (_is_x(row, 27) or _is_checked(row, 27))
    )

    # Offer / not-offer breakdown (col I = x → not on offer, col I = ✅ → on offer)
    not_offer_posted_mo     = sum(safe_int(row[4]) for row in mmp_rows[1:] if len(row) > 4 and _is_x(row, 8))
    not_offer_not_posted_mo = sum(1 for row in mmp_rows[1:] if len(row) > 4 and _is_x(row, 8)      and safe_int(row[4]) == 0)
    offer_posted_mo         = sum(safe_int(row[4]) for row in mmp_rows[1:] if len(row) > 4 and _is_checked(row, 8))
    offer_not_posted_mo     = sum(1 for row in mmp_rows[1:] if len(row) > 4 and _is_checked(row, 8) and safe_int(row[4]) == 0)

    monthly_expected = round(sum(
        safe_int(row[4]) * KENYA_SPP
        for row in mmp_rows[1:]
        if len(row) > 4 and _is_checked(row, 8)
    ))

    print(f"\n  ── Kenya Monthly ─────────────────────────────────────────")
    print(f"  Monthly posts (MONTHLY_MARKETING_POST col E, check I): {monthly_posts}")
    print(f"  Monthly expected (posts × {KENYA_SPP})               : {fmt_int(monthly_expected)}")
    print(f"  Monthly sales (MONTHLY_SALES col X, check AB)        : {fmt_int(monthly_sales)}")
    print(f"  Monthly unposted (MONTHLY_SALES col X, x in AB)      : {fmt_int(monthly_unposted)}")
    print(f"  Monthly total (MONTHLY_SALES col X, x or ✅ in AB)   : {fmt_int(monthly_total)}")
    print(f"  Posted & Not on Offer mo  (x + E>0)  : {not_offer_posted_mo}")
    print(f"  On Offer & Not Posted mo  (✅ + E=0) : {offer_not_posted_mo}")
    print(f"  Posted & On Offer mo      (✅ + E>0) : {offer_posted_mo}")
    print(f"  Not Posted & Not on Offer mo (x + E=0): {not_offer_not_posted_mo}")

    # Sales Achieved % (monthly): per-bag yield/posts ratio, then average
    # MMP: col I (✅ or x) AND col E > 0 → {name col C: sum col E}
    mmp_posts_map = {}
    for row in mmp_rows[1:]:
        if len(row) < 3:
            continue
        if not (_is_checked(row, 8) or _is_x(row, 8)):
            continue
        col_e = safe_int(row[4]) if len(row) > 4 else 0
        if col_e <= 0:
            continue
        name = str(row[2]).lower().strip()
        mmp_posts_map[name] = mmp_posts_map.get(name, 0) + col_e

    # MS: col AB (✅ or x) AND col X > 0 → {name col B: sum col X}
    ms_yield_map = {}
    for row in ms_rows[1:]:
        if len(row) < 2:
            continue
        if not (_is_checked(row, 27) or _is_x(row, 27)):
            continue
        col_x = safe_int(row[23]) if len(row) > 23 else 0
        if col_x <= 0:
            continue
        name = str(row[1]).lower().strip()
        ms_yield_map[name] = ms_yield_map.get(name, 0) + col_x

    # Per-bag % → average
    bag_pcts_mo = []
    for name, posts in mmp_posts_map.items():
        yield_val = ms_yield_map.get(name, 0)
        bag_pcts_mo.append(min((yield_val / posts) * 100, 100.0) if posts > 0 else 0.0)

    mo_mkt_pct = round(sum(bag_pcts_mo) / len(bag_pcts_mo), 1) if bag_pcts_mo else 0.0
    print(f"  Mkt % mo  : {len(bag_pcts_mo)} bags, avg {mo_mkt_pct}%")

    # Sales Achieved from Marketing Posting (Monthly)(Bags Not on Offer %): per-bag avg
    # MMP col I=x, col E>0 → posts per bag; MS col AB=x, col AF>0 → yield per bag
    mmp_x_posts_map = {}
    for row in mmp_rows[1:]:
        if len(row) < 3 or not _is_x(row, 8):
            continue
        col_e = safe_int(row[4]) if len(row) > 4 else 0
        if col_e <= 0:
            continue
        name = str(row[2]).lower().strip()
        mmp_x_posts_map[name] = mmp_x_posts_map.get(name, 0) + col_e

    ms_x_yield_map = {}
    for row in ms_rows[1:]:
        if len(row) < 2 or not _is_x(row, 27):
            continue
        col_af = safe_int(row[31]) if len(row) > 31 else 0
        if col_af <= 0:
            continue
        name = str(row[1]).lower().strip()
        ms_x_yield_map[name] = ms_x_yield_map.get(name, 0) + col_af

    bag_pcts_x_mo = []
    for name, posts in mmp_x_posts_map.items():
        yield_val = ms_x_yield_map.get(name, 0)
        bag_pcts_x_mo.append(min((yield_val / posts) * 100, 100.0) if posts > 0 else 0.0)

    mo_not_offer_mkt_pct = round(sum(bag_pcts_x_mo) / len(bag_pcts_x_mo), 1) if bag_pcts_x_mo else 0.0
    print(f"  Mkt % mo (not-offer): {len(bag_pcts_x_mo)} bags, avg {mo_not_offer_mkt_pct}%")

    # Bags Not Posted & On Offer (Monthly): MMP col I=✅, col E=0 → names col C → MS col B (col AB=✅, AF>0) → sum col AF
    _mmp_chk_zero_mo = {
        str(row[2]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > 8 and _is_checked(row, 8) and safe_int(row[4]) == 0 and str(row[2]).strip()
    }
    offer_not_posted_mo_sales = sum(
        safe_int(row[23])   # MS col X = monthly Kenya sales (col AF/31 was empty → 0)
        for row in ms_rows[1:]
        if len(row) > 23
        and not any(str(cell).strip().upper() == "SUM TOTAL" for cell in row[:5])
        and str(row[1]).lower().strip() in _mmp_chk_zero_mo
    )

    # Bags Not Posted & Not on Offer (Monthly): MMP col I=x, col E=0 → names col C → MS col B match → sum col AF
    _mmp_x_zero_mo = {
        str(row[2]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > 8 and _is_x(row, 8) and safe_int(row[4]) == 0 and str(row[2]).strip()
    }
    not_offer_not_posted_mo_sales = sum(
        safe_int(row[23])   # MS col X = monthly Kenya sales (col AF/31 was empty → 0)
        for row in ms_rows[1:]
        if len(row) > 23
        and not any(str(cell).strip().upper() == "SUM TOTAL" for cell in row[:5])
        and str(row[1]).lower().strip() in _mmp_x_zero_mo
    )

    return (monthly_posts, monthly_sales, monthly_unposted, monthly_total,
            not_offer_posted_mo, offer_not_posted_mo, offer_posted_mo, not_offer_not_posted_mo,
            monthly_expected, monthly_posts_x, monthly_sales_no_post, mo_mkt_pct,
            not_offer_not_posted_mo_sales, mo_not_offer_mkt_pct,
            offer_not_posted_mo_sales)


def _fetch_sinza_weekly(wmp_rows, ws_rows):
    """Sinza weekly KPIs — mirrors _fetch_weekly_kenya column offsets for Sinza."""
    WMP_POST, WMP_CHK, WMP_NAME = 5, 9, 2
    WS_OFFER, WS_SALES, WS_NAME = 25, 17, 2

    sz_wk_posts = sum(
        safe_int(row[WMP_POST]) for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_checked(row, WMP_CHK)
    )
    sz_wk_posts_x = sum(
        safe_int(row[WMP_POST]) for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_x(row, WMP_CHK)
    )
    sz_wk_expected = round(sum(
        safe_int(row[WMP_POST]) * SINZA_SPP for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_checked(row, WMP_CHK)
    ))

    sz_proj_weekly_sales = 0
    for row in ws_rows:
        if any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5]):
            sz_proj_weekly_sales = safe_int(row[WS_SALES]) if len(row) > WS_SALES else 0
            break

    _sz_posted = {
        str(row[WMP_NAME]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_checked(row, WMP_CHK) and safe_int(row[WMP_POST]) > 0
    }
    sz_wk_sales_posted = sum(
        safe_int(row[WS_SALES]) for row in ws_rows[1:]
        if len(row) > WS_SALES
        and not any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5])
        and str(row[WS_NAME]).lower().strip() in _sz_posted
    )

    _sz_x_posted = {
        str(row[WMP_NAME]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_x(row, WMP_CHK) and safe_int(row[WMP_POST]) > 0
    }
    sz_wk_sales_no_offer = sum(
        safe_int(row[WS_SALES]) for row in ws_rows[1:]
        if len(row) > WS_SALES
        and not any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5])
        and str(row[WS_NAME]).lower().strip() in _sz_x_posted
    )

    _sz_zero_post = {
        str(row[WMP_NAME]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > WMP_POST and safe_int(row[WMP_POST]) == 0 and str(row[WMP_NAME]).strip()
    }
    sz_wk_unposted = sum(
        safe_int(row[WS_SALES]) for row in ws_rows[1:]
        if len(row) > WS_SALES
        and not any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5])
        and str(row[WS_NAME]).lower().strip() in _sz_zero_post
    )

    # Per-bag avg % for all posted bags (S1 weekly % + On Offer %)
    sz_posts_map = {}
    for row in wmp_rows[1:]:
        if len(row) < WMP_NAME + 1: continue
        if not (_is_checked(row, WMP_CHK) or _is_x(row, WMP_CHK)): continue
        col_f = safe_int(row[WMP_POST]) if len(row) > WMP_POST else 0
        if col_f <= 0: continue
        name = str(row[WMP_NAME]).lower().strip()
        sz_posts_map[name] = sz_posts_map.get(name, 0) + col_f

    sz_yield_map = {}
    for row in ws_rows[1:]:
        if len(row) < WS_NAME + 1: continue
        if any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5]): continue
        if not (_is_checked(row, WS_OFFER) or _is_x(row, WS_OFFER)): continue
        col_r = safe_int(row[WS_SALES]) if len(row) > WS_SALES else 0
        if col_r <= 0: continue
        name = str(row[WS_NAME]).lower().strip()
        sz_yield_map[name] = sz_yield_map.get(name, 0) + col_r

    sz_bag_pcts = [
        min((sz_yield_map.get(n, 0) / p) * 100, 100.0) if p > 0 else 0.0
        for n, p in sz_posts_map.items()
    ]
    sz_wk_mkt_pct = round(sum(sz_bag_pcts) / len(sz_bag_pcts), 1) if sz_bag_pcts else 0.0

    # Per-bag avg % for x-only (Not on Offer %)
    sz_x_posts_map = {}
    for row in wmp_rows[1:]:
        if len(row) < WMP_NAME + 1 or not _is_x(row, WMP_CHK): continue
        col_f = safe_int(row[WMP_POST]) if len(row) > WMP_POST else 0
        if col_f <= 0: continue
        name = str(row[WMP_NAME]).lower().strip()
        sz_x_posts_map[name] = sz_x_posts_map.get(name, 0) + col_f

    sz_x_yield_map = {}
    for row in ws_rows[1:]:
        if len(row) < WS_NAME + 1: continue
        if any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5]): continue
        if not _is_x(row, WS_OFFER): continue
        col_r = safe_int(row[WS_SALES]) if len(row) > WS_SALES else 0
        if col_r <= 0: continue
        name = str(row[WS_NAME]).lower().strip()
        sz_x_yield_map[name] = sz_x_yield_map.get(name, 0) + col_r

    sz_x_pcts = [
        min((sz_x_yield_map.get(n, 0) / p) * 100, 100.0) if p > 0 else 0.0
        for n, p in sz_x_posts_map.items()
    ]
    sz_wk_not_offer_mkt_pct = round(sum(sz_x_pcts) / len(sz_x_pcts), 1) if sz_x_pcts else 0.0

    # Bags Not Posted & Not on Offer (Weekly)
    _sz_x_zero = {
        str(row[WMP_NAME]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_x(row, WMP_CHK)
        and safe_int(row[WMP_POST]) == 0 and str(row[WMP_NAME]).strip()
    }
    sz_not_offer_not_posted_wk = sum(
        safe_int(row[WS_SALES]) for row in ws_rows[1:]
        if len(row) > WS_SALES
        and not any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5])
        and str(row[WS_NAME]).lower().strip() in _sz_x_zero
    )

    # Bags Not Posted & On Offer (Weekly)
    _sz_chk_zero = {
        str(row[WMP_NAME]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_checked(row, WMP_CHK)
        and safe_int(row[WMP_POST]) == 0 and str(row[WMP_NAME]).strip()
    }
    sz_offer_not_posted_wk = sum(
        safe_int(row[WS_SALES]) for row in ws_rows[1:]
        if len(row) > WS_SALES
        and not any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5])
        and str(row[WS_NAME]).lower().strip() in _sz_chk_zero
    )

    return {
        'szWkPosts':                  sz_wk_posts,
        'szWkPostsX':                 sz_wk_posts_x,
        'szWkExpected':               sz_wk_expected,
        'szWkSalesPosted':            fmt_int(sz_wk_sales_posted),
        'szWkSalesNoOffer':           fmt_int(sz_wk_sales_no_offer),
        'szProjWeeklySales':          fmt_int(sz_proj_weekly_sales),
        'szWkUnposted':               fmt_int(sz_wk_unposted),
        'szWkMktPct':                 f"{sz_wk_mkt_pct}%",
        'szWkNotOfferMktPct':         f"{sz_wk_not_offer_mkt_pct}%",
        'szNotOfferNotPostedWkSales': fmt_int(sz_not_offer_not_posted_wk),
        'szOfferNotPostedWkSales':    fmt_int(sz_offer_not_posted_wk),
        'szWkNonMktPct':              f"{round(min(sz_wk_unposted / sz_proj_weekly_sales, 1.0) * 100, 1) if sz_proj_weekly_sales > 0 else 0.0}%",
    }


def _fetch_sinza_monthly(ms_rows, mmp_rows):
    """Sinza monthly KPIs — mirrors _fetch_monthly_kenya column offsets for Sinza."""
    MMP_POST, MMP_CHK, MMP_NAME = 5, 9, 2
    MS_CHK, MS_VAL, MS_NAME = 28, 24, 1

    sz_mo_posts = sum(
        safe_int(row[MMP_POST]) for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_checked(row, MMP_CHK)
    )
    sz_mo_posts_x = sum(
        safe_int(row[MMP_POST]) for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_x(row, MMP_CHK)
    )
    sz_mo_expected = round(sum(
        safe_int(row[MMP_POST]) * SINZA_SPP for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_checked(row, MMP_CHK)
    ))

    _sz_mo_posted = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_checked(row, MMP_CHK) and safe_int(row[MMP_POST]) > 0
    }
    sz_mo_sales_posted = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL
        and str(row[MS_NAME]).lower().strip() in _sz_mo_posted
    )

    _sz_mo_x_posted = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_x(row, MMP_CHK) and safe_int(row[MMP_POST]) > 0
    }
    sz_mo_sales_no_offer = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL
        and str(row[MS_NAME]).lower().strip() in _sz_mo_x_posted
    )

    sz_mo_total = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL and (_is_x(row, MS_CHK) or _is_checked(row, MS_CHK))
    )

    _sz_any_posted_mo = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_POST and safe_int(row[MMP_POST]) > 0 and str(row[MMP_NAME]).strip()
    }
    _sz_zero_post_mo = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_POST and str(row[MMP_NAME]).strip()
        and str(row[MMP_POST]).strip() == '0'
        and str(row[MMP_NAME]).lower().strip() not in _sz_any_posted_mo
    }
    sz_mo_unposted = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL
        and str(row[MS_NAME]).lower().strip() in _sz_zero_post_mo
    )

    # Per-bag avg % for all posted bags (S1 monthly % + On Offer monthly %)
    sz_mo_posts_map = {}
    for row in mmp_rows[1:]:
        if len(row) < MMP_NAME + 1: continue
        if not (_is_checked(row, MMP_CHK) or _is_x(row, MMP_CHK)): continue
        col_f = safe_int(row[MMP_POST]) if len(row) > MMP_POST else 0
        if col_f <= 0: continue
        name = str(row[MMP_NAME]).lower().strip()
        sz_mo_posts_map[name] = sz_mo_posts_map.get(name, 0) + col_f

    sz_mo_yield_map = {}
    for row in ms_rows[1:]:
        if len(row) < MS_NAME + 1: continue
        if not (_is_checked(row, MS_CHK) or _is_x(row, MS_CHK)): continue
        col_y = safe_int(row[MS_VAL]) if len(row) > MS_VAL else 0
        if col_y <= 0: continue
        name = str(row[MS_NAME]).lower().strip()
        sz_mo_yield_map[name] = sz_mo_yield_map.get(name, 0) + col_y

    sz_mo_pcts = [
        min((sz_mo_yield_map.get(n, 0) / p) * 100, 100.0) if p > 0 else 0.0
        for n, p in sz_mo_posts_map.items()
    ]
    sz_mo_mkt_pct = round(sum(sz_mo_pcts) / len(sz_mo_pcts), 1) if sz_mo_pcts else 0.0

    # Per-bag avg % for x-only (Not on Offer monthly %)
    sz_mo_x_posts_map = {}
    for row in mmp_rows[1:]:
        if len(row) < MMP_NAME + 1 or not _is_x(row, MMP_CHK): continue
        col_f = safe_int(row[MMP_POST]) if len(row) > MMP_POST else 0
        if col_f <= 0: continue
        name = str(row[MMP_NAME]).lower().strip()
        sz_mo_x_posts_map[name] = sz_mo_x_posts_map.get(name, 0) + col_f

    sz_mo_x_yield_map = {}
    for row in ms_rows[1:]:
        if len(row) < MS_NAME + 1 or not _is_x(row, MS_CHK): continue
        col_y = safe_int(row[MS_VAL]) if len(row) > MS_VAL else 0
        if col_y <= 0: continue
        name = str(row[MS_NAME]).lower().strip()
        sz_mo_x_yield_map[name] = sz_mo_x_yield_map.get(name, 0) + col_y

    sz_mo_x_pcts = [
        min((sz_mo_x_yield_map.get(n, 0) / p) * 100, 100.0) if p > 0 else 0.0
        for n, p in sz_mo_x_posts_map.items()
    ]
    sz_mo_not_offer_mkt_pct = round(sum(sz_mo_x_pcts) / len(sz_mo_x_pcts), 1) if sz_mo_x_pcts else 0.0

    # Bags Not Posted & Not on Offer (Monthly)
    _sz_x_zero_mo = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_x(row, MMP_CHK)
        and safe_int(row[MMP_POST]) == 0 and str(row[MMP_NAME]).strip()
    }
    sz_not_offer_not_posted_mo = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL
        and str(row[MS_NAME]).lower().strip() in _sz_x_zero_mo
    )

    # Bags Not Posted & On Offer (Monthly): MMP col J=✅ & col F=0 → MS col B (col AC=✅, Y>0) → sum col Y
    _sz_chk_zero_mo = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_checked(row, MMP_CHK)
        and safe_int(row[MMP_POST]) == 0 and str(row[MMP_NAME]).strip()
    }
    sz_offer_not_posted_mo = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL
        and _is_checked(row, MS_CHK)
        and safe_int(row[MS_VAL]) > 0
        and str(row[MS_NAME]).lower().strip() in _sz_chk_zero_mo
    )

    sz_mo_grand_total = sum(safe_int(row[MS_VAL]) for row in ms_rows[1:] if len(row) > MS_VAL)
    sz_mo_non_mkt_pct = round(min(sz_mo_unposted / sz_mo_grand_total, 1.0) * 100, 1) if sz_mo_grand_total > 0 else 0.0

    return {
        'szMoPosts':                  sz_mo_posts,
        'szMoPostsX':                 sz_mo_posts_x,
        'szMoExpected':               sz_mo_expected,
        'szMoSalesPosted':            fmt_int(sz_mo_sales_posted),
        'szMoSalesNoOffer':           fmt_int(sz_mo_sales_no_offer),
        'szMoTotal':                  fmt_int(sz_mo_total),
        'szMoUnposted':               fmt_int(sz_mo_unposted),
        'szMoMktPct':                 f"{sz_mo_mkt_pct}%",
        'szMoNotOfferMktPct':         f"{sz_mo_not_offer_mkt_pct}%",
        'szNotOfferNotPostedMoSales': fmt_int(sz_not_offer_not_posted_mo),
        'szOfferNotPostedMoSales':    fmt_int(sz_offer_not_posted_mo),
        'szMoNonMktPct':              f"{sz_mo_non_mkt_pct}%",
    }


def _fetch_uganda_weekly(wmp_rows, ws_rows):
    """Uganda weekly KPIs — mirrors _fetch_sinza_weekly with Uganda column offsets."""
    WMP_POST, WMP_CHK, WMP_NAME = 6, 10, 2
    WS_OFFER, WS_SALES, WS_NAME = 26, 18, 2

    ug_wk_posts = sum(
        safe_int(row[WMP_POST]) for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_checked(row, WMP_CHK)
    )
    ug_wk_posts_x = sum(
        safe_int(row[WMP_POST]) for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_x(row, WMP_CHK)
    )
    ug_wk_expected = round(sum(
        safe_int(row[WMP_POST]) * UGANDA_SPP for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_checked(row, WMP_CHK)
    ))

    ug_proj_weekly_sales = 0
    for row in ws_rows:
        if any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5]):
            ug_proj_weekly_sales = safe_int(row[WS_SALES]) if len(row) > WS_SALES else 0
            break

    _ug_posted = {
        str(row[WMP_NAME]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_checked(row, WMP_CHK) and safe_int(row[WMP_POST]) > 0
    }
    ug_wk_sales_posted = sum(
        safe_int(row[WS_SALES]) for row in ws_rows[1:]
        if len(row) > WS_SALES
        and not any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5])
        and str(row[WS_NAME]).lower().strip() in _ug_posted
    )

    _ug_x_posted = {
        str(row[WMP_NAME]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_x(row, WMP_CHK) and safe_int(row[WMP_POST]) > 0
    }
    ug_wk_sales_no_offer = sum(
        safe_int(row[WS_SALES]) for row in ws_rows[1:]
        if len(row) > WS_SALES
        and not any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5])
        and str(row[WS_NAME]).lower().strip() in _ug_x_posted
    )

    _ug_zero_post = {
        str(row[WMP_NAME]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > WMP_POST and safe_int(row[WMP_POST]) == 0 and str(row[WMP_NAME]).strip()
    }
    ug_wk_unposted = sum(
        safe_int(row[WS_SALES]) for row in ws_rows[1:]
        if len(row) > WS_SALES
        and not any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5])
        and str(row[WS_NAME]).lower().strip() in _ug_zero_post
    )

    # Per-bag avg % for all posted bags (S1 weekly % + On Offer %)
    ug_posts_map = {}
    for row in wmp_rows[1:]:
        if len(row) < WMP_NAME + 1: continue
        if not (_is_checked(row, WMP_CHK) or _is_x(row, WMP_CHK)): continue
        col_f = safe_int(row[WMP_POST]) if len(row) > WMP_POST else 0
        if col_f <= 0: continue
        name = str(row[WMP_NAME]).lower().strip()
        ug_posts_map[name] = ug_posts_map.get(name, 0) + col_f

    ug_yield_map = {}
    for row in ws_rows[1:]:
        if len(row) < WS_NAME + 1: continue
        if any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5]): continue
        if not (_is_checked(row, WS_OFFER) or _is_x(row, WS_OFFER)): continue
        col_r = safe_int(row[WS_SALES]) if len(row) > WS_SALES else 0
        if col_r <= 0: continue
        name = str(row[WS_NAME]).lower().strip()
        ug_yield_map[name] = ug_yield_map.get(name, 0) + col_r

    ug_bag_pcts = [
        min((ug_yield_map.get(n, 0) / p) * 100, 100.0) if p > 0 else 0.0
        for n, p in ug_posts_map.items()
    ]
    ug_wk_mkt_pct = round(sum(ug_bag_pcts) / len(ug_bag_pcts), 1) if ug_bag_pcts else 0.0

    # Per-bag avg % for x-only (Not on Offer %)
    ug_x_posts_map = {}
    for row in wmp_rows[1:]:
        if len(row) < WMP_NAME + 1 or not _is_x(row, WMP_CHK): continue
        col_f = safe_int(row[WMP_POST]) if len(row) > WMP_POST else 0
        if col_f <= 0: continue
        name = str(row[WMP_NAME]).lower().strip()
        ug_x_posts_map[name] = ug_x_posts_map.get(name, 0) + col_f

    ug_x_yield_map = {}
    for row in ws_rows[1:]:
        if len(row) < WS_NAME + 1: continue
        if any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5]): continue
        if not _is_x(row, WS_OFFER): continue
        col_r = safe_int(row[WS_SALES]) if len(row) > WS_SALES else 0
        if col_r <= 0: continue
        name = str(row[WS_NAME]).lower().strip()
        ug_x_yield_map[name] = ug_x_yield_map.get(name, 0) + col_r

    ug_x_pcts = [
        min((ug_x_yield_map.get(n, 0) / p) * 100, 100.0) if p > 0 else 0.0
        for n, p in ug_x_posts_map.items()
    ]
    ug_wk_not_offer_mkt_pct = round(sum(ug_x_pcts) / len(ug_x_pcts), 1) if ug_x_pcts else 0.0

    # Bags Not Posted & Not on Offer (Weekly)
    _ug_x_zero = {
        str(row[WMP_NAME]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_x(row, WMP_CHK)
        and safe_int(row[WMP_POST]) == 0 and str(row[WMP_NAME]).strip()
    }
    ug_not_offer_not_posted_wk = sum(
        safe_int(row[WS_SALES]) for row in ws_rows[1:]
        if len(row) > WS_SALES
        and not any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5])
        and str(row[WS_NAME]).lower().strip() in _ug_x_zero
    )

    # Bags Not Posted & On Offer (Weekly)
    _ug_chk_zero = {
        str(row[WMP_NAME]).lower().strip()
        for row in wmp_rows[1:]
        if len(row) > WMP_CHK and _is_checked(row, WMP_CHK)
        and safe_int(row[WMP_POST]) == 0 and str(row[WMP_NAME]).strip()
    }
    ug_offer_not_posted_wk = sum(
        safe_int(row[WS_SALES]) for row in ws_rows[1:]
        if len(row) > WS_SALES
        and not any(str(c).strip().upper() == "SUM TOTAL" for c in row[:5])
        and str(row[WS_NAME]).lower().strip() in _ug_chk_zero
    )

    return {
        'ugWkPosts':                  ug_wk_posts,
        'ugWkPostsX':                 ug_wk_posts_x,
        'ugWkExpected':               ug_wk_expected,
        'ugWkSalesPosted':            fmt_int(ug_wk_sales_posted),
        'ugWkSalesNoOffer':           fmt_int(ug_wk_sales_no_offer),
        'ugProjWeeklySales':          fmt_int(ug_proj_weekly_sales),
        'ugWkUnposted':               fmt_int(ug_wk_unposted),
        'ugWkMktPct':                 f"{ug_wk_mkt_pct}%",
        'ugWkNotOfferMktPct':         f"{ug_wk_not_offer_mkt_pct}%",
        'ugNotOfferNotPostedWkSales': fmt_int(ug_not_offer_not_posted_wk),
        'ugOfferNotPostedWkSales':    fmt_int(ug_offer_not_posted_wk),
        'ugWkNonMktPct':              f"{round(min(ug_wk_unposted / ug_proj_weekly_sales, 1.0) * 100, 1) if ug_proj_weekly_sales > 0 else 0.0}%",
    }


def _fetch_uganda_monthly(ms_rows, mmp_rows):
    """Uganda monthly KPIs — mirrors _fetch_sinza_monthly with Uganda column offsets."""
    MMP_POST, MMP_CHK, MMP_NAME = 6, 10, 2
    MS_CHK, MS_VAL, MS_NAME = 29, 25, 1

    ug_mo_posts = sum(
        safe_int(row[MMP_POST]) for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_checked(row, MMP_CHK)
    )
    ug_mo_posts_x = sum(
        safe_int(row[MMP_POST]) for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_x(row, MMP_CHK)
    )
    ug_mo_expected = round(sum(
        safe_int(row[MMP_POST]) * UGANDA_SPP for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_checked(row, MMP_CHK)
    ))

    _ug_mo_posted = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_checked(row, MMP_CHK) and safe_int(row[MMP_POST]) > 0
    }
    ug_mo_sales_posted = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL
        and str(row[MS_NAME]).lower().strip() in _ug_mo_posted
    )

    _ug_mo_x_posted = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_x(row, MMP_CHK) and safe_int(row[MMP_POST]) > 0
    }
    ug_mo_sales_no_offer = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL
        and str(row[MS_NAME]).lower().strip() in _ug_mo_x_posted
    )

    ug_mo_total = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL and (_is_x(row, MS_CHK) or _is_checked(row, MS_CHK))
    )

    _ug_any_posted_mo = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_POST and safe_int(row[MMP_POST]) > 0 and str(row[MMP_NAME]).strip()
    }
    _ug_zero_post_mo = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_POST and str(row[MMP_NAME]).strip()
        and str(row[MMP_POST]).strip() == '0'
        and str(row[MMP_NAME]).lower().strip() not in _ug_any_posted_mo
    }
    ug_mo_unposted = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL
        and str(row[MS_NAME]).lower().strip() in _ug_zero_post_mo
    )

    # Per-bag avg % for all posted bags (S1 monthly % + On Offer monthly %)
    ug_mo_posts_map = {}
    for row in mmp_rows[1:]:
        if len(row) < MMP_NAME + 1: continue
        if not (_is_checked(row, MMP_CHK) or _is_x(row, MMP_CHK)): continue
        col_f = safe_int(row[MMP_POST]) if len(row) > MMP_POST else 0
        if col_f <= 0: continue
        name = str(row[MMP_NAME]).lower().strip()
        ug_mo_posts_map[name] = ug_mo_posts_map.get(name, 0) + col_f

    ug_mo_yield_map = {}
    for row in ms_rows[1:]:
        if len(row) < MS_NAME + 1: continue
        if not (_is_checked(row, MS_CHK) or _is_x(row, MS_CHK)): continue
        col_y = safe_int(row[MS_VAL]) if len(row) > MS_VAL else 0
        if col_y <= 0: continue
        name = str(row[MS_NAME]).lower().strip()
        ug_mo_yield_map[name] = ug_mo_yield_map.get(name, 0) + col_y

    ug_mo_pcts = [
        min((ug_mo_yield_map.get(n, 0) / p) * 100, 100.0) if p > 0 else 0.0
        for n, p in ug_mo_posts_map.items()
    ]
    ug_mo_mkt_pct = round(sum(ug_mo_pcts) / len(ug_mo_pcts), 1) if ug_mo_pcts else 0.0

    # Per-bag avg % for x-only (Not on Offer monthly %)
    ug_mo_x_posts_map = {}
    for row in mmp_rows[1:]:
        if len(row) < MMP_NAME + 1 or not _is_x(row, MMP_CHK): continue
        col_f = safe_int(row[MMP_POST]) if len(row) > MMP_POST else 0
        if col_f <= 0: continue
        name = str(row[MMP_NAME]).lower().strip()
        ug_mo_x_posts_map[name] = ug_mo_x_posts_map.get(name, 0) + col_f

    ug_mo_x_yield_map = {}
    for row in ms_rows[1:]:
        if len(row) < MS_NAME + 1 or not _is_x(row, MS_CHK): continue
        col_y = safe_int(row[MS_VAL]) if len(row) > MS_VAL else 0
        if col_y <= 0: continue
        name = str(row[MS_NAME]).lower().strip()
        ug_mo_x_yield_map[name] = ug_mo_x_yield_map.get(name, 0) + col_y

    ug_mo_x_pcts = [
        min((ug_mo_x_yield_map.get(n, 0) / p) * 100, 100.0) if p > 0 else 0.0
        for n, p in ug_mo_x_posts_map.items()
    ]
    ug_mo_not_offer_mkt_pct = round(sum(ug_mo_x_pcts) / len(ug_mo_x_pcts), 1) if ug_mo_x_pcts else 0.0

    # Bags Not Posted & Not on Offer (Monthly)
    _ug_x_zero_mo = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_x(row, MMP_CHK)
        and safe_int(row[MMP_POST]) == 0 and str(row[MMP_NAME]).strip()
    }
    ug_not_offer_not_posted_mo = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL
        and str(row[MS_NAME]).lower().strip() in _ug_x_zero_mo
    )

    # Bags Not Posted & On Offer (Monthly)
    _ug_chk_zero_mo = {
        str(row[MMP_NAME]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > MMP_CHK and _is_checked(row, MMP_CHK)
        and safe_int(row[MMP_POST]) == 0 and str(row[MMP_NAME]).strip()
    }
    ug_offer_not_posted_mo = sum(
        safe_int(row[MS_VAL]) for row in ms_rows[1:]
        if len(row) > MS_VAL
        and _is_checked(row, MS_CHK)
        and safe_int(row[MS_VAL]) > 0
        and str(row[MS_NAME]).lower().strip() in _ug_chk_zero_mo
    )

    ug_mo_grand_total = sum(safe_int(row[MS_VAL]) for row in ms_rows[1:] if len(row) > MS_VAL)
    ug_mo_non_mkt_pct = round(min(ug_mo_unposted / ug_mo_grand_total, 1.0) * 100, 1) if ug_mo_grand_total > 0 else 0.0

    return {
        'ugMoPosts':                  ug_mo_posts,
        'ugMoPostsX':                 ug_mo_posts_x,
        'ugMoExpected':               ug_mo_expected,
        'ugMoSalesPosted':            fmt_int(ug_mo_sales_posted),
        'ugMoSalesNoOffer':           fmt_int(ug_mo_sales_no_offer),
        'ugMoTotal':                  fmt_int(ug_mo_total),
        'ugMoUnposted':               fmt_int(ug_mo_unposted),
        'ugMoMktPct':                 f"{ug_mo_mkt_pct}%",
        'ugMoNotOfferMktPct':         f"{ug_mo_not_offer_mkt_pct}%",
        'ugNotOfferNotPostedMoSales': fmt_int(ug_not_offer_not_posted_mo),
        'ugOfferNotPostedMoSales':    fmt_int(ug_offer_not_posted_mo),
        'ugMoNonMktPct':              f"{ug_mo_non_mkt_pct}%",
    }


# ── FETCH ─────────────────────────────────────────────────────

def fetch_posting_data():
    gc = get_gspread_client()
    sh = gc.open_by_key(SPREADSHEET_ID)

    print("  Reading sheets (one connection)...")
    ms_rows  = sh.worksheet("MONTHLY_SALES").get_all_values()
    mmp_rows = sh.worksheet("MONTHLY_MARKETING_POST").get_all_values()
    sl_rows  = sh.worksheet("STOCK_LEVELS").get_all_values()
    mt_rows  = sh.worksheet("MONTHLY_TARGET").get_all_values()
    print(f"  MONTHLY_SALES rows         : {len(ms_rows) - 1}")
    print(f"  MONTHLY_MARKETING_POST rows: {len(mmp_rows) - 1}")
    print(f"  STOCK_LEVELS rows          : {len(sl_rows) - 1}")
    print(f"  MONTHLY_TARGET rows        : {len(mt_rows) - 1}")

    kenya = _analyze_region(ms_rows, mmp_rows, sl_rows,
                            sales_col=23, post_col=4, stock_col=24,
                            spp=KENYA_SPP, region="Kenya")

    sinza = _analyze_region(ms_rows, mmp_rows, sl_rows,
                            sales_col=17, post_col=5, stock_col=24,
                            spp=SINZA_SPP, region="Sinza")

    uganda = _analyze_region(ms_rows, mmp_rows, sl_rows,
                             sales_col=17, post_col=6, stock_col=18,
                             spp=UGANDA_SPP, region="Uganda")

    (wk_posts, wk_sales, wk_expected, wk_unposted, s3_wk_posts, nc_wk,
     not_offer_posted_wk, offer_not_posted_wk, offer_posted_wk, not_offer_not_posted_wk,
     wk_instock_posted, wk_instock_not_posted, proj_weekly_sales,
     instock_not_posted_list, offer_posted_wk_x,
     offer_posted_wk_count, wk_posts_x, wk_sales_no_post,
     wk_mkt_pct, not_offer_not_posted_wk_sales,
     wk_not_offer_mkt_pct, offer_not_posted_wk_sales) = _fetch_weekly_kenya(sh, sl_rows)

    # Kenya S3 monthly not-posted: STOCK_LEVELS col Y (idx 24) > 20 − MONTHLY_MARKETING_POST col E (idx 4) > 0
    kenya_sl_keys  = set(
        (str(row[0]).lower().strip(), str(row[2]).lower().strip())
        for row in sl_rows[1:] if len(row) > 24 and safe_int(row[24]) > 20)
    kenya_mmp_keys = set(
        (str(row[0]).lower().strip(), str(row[2]).lower().strip())
        for row in mmp_rows[1:] if len(row) > 4 and safe_int(row[4]) > 0)
    mo_instock_not_posted = len(kenya_sl_keys - kenya_mmp_keys)

    wmp_rows_wk = sh.worksheet("WEEKLY_MARKETING_POST").get_all_values()
    ws_rows_wk  = sh.worksheet("WEEKLY_SALES").get_all_values()
    sz_wk = _fetch_weekly_region(wmp_rows_wk, ws_rows_wk, 5, 9, 17, 25, SINZA_SPP)
    ug_wk = _fetch_weekly_region(wmp_rows_wk, ws_rows_wk, 6, 10, 18, 26, UGANDA_SPP)
    sinza['weekly']  = sz_wk
    uganda['weekly'] = ug_wk

    # Posted-but-didn't-sell bags (weekly), tagged on/not-on-offer, for the guidance panel
    sinza['noConvertWk']  = _build_no_convert(wmp_rows_wk, ws_rows_wk, [17],  9, 5, sl_rows, 17, SINZA_SPP,  sales_check_col=25)
    uganda['noConvertWk'] = _build_no_convert(wmp_rows_wk, ws_rows_wk, [18], 10, 6, sl_rows, 18, UGANDA_SPP, sales_check_col=26)

    # Current stock of bags marketing POSTED (for the clearance tracker)
    kenya['postedStock']  = _posted_stock(wmp_rows_wk, sl_rows, 4,  8, 24)
    sinza['postedStock']  = _posted_stock(wmp_rows_wk, sl_rows, 5,  9, 17)
    uganda['postedStock'] = _posted_stock(wmp_rows_wk, sl_rows, 6, 10, 18)

    # Sinza accuracy: STOCK_LEVELS col R (idx 17) > 0, col AC (idx 28) = ✅ or x → Sinza-specific rows
    # Match against WMP/MMP using col C (idx 2) name only
    sz_sl_keys = set()
    for row in sl_rows[1:]:
        if len(row) > 28 and safe_int(row[17]) > 0 and (_is_checked(row, 28) or _is_x(row, 28)):
            sz_sl_keys.add(str(row[2]).lower().strip())

    sz_wmp_keys = set()
    for row in wmp_rows_wk[1:]:
        if len(row) > 5 and safe_int(row[5]) > 0:
            sz_wmp_keys.add(str(row[2]).lower().strip())

    sz_mmp_keys = set()
    for row in mmp_rows[1:]:
        if len(row) > 5 and safe_int(row[5]) > 0:
            sz_mmp_keys.add(str(row[2]).lower().strip())

    sinza['weekly']['wkInstockPosted']    = len(sz_sl_keys & sz_wmp_keys)
    sinza['weekly']['wkInstockNotPosted'] = len(sz_sl_keys - sz_wmp_keys)
    sinza['weekly']['moInstockPosted']    = len(sz_sl_keys & sz_mmp_keys)
    sinza['weekly']['moInstockNotPosted'] = len(sz_sl_keys - sz_mmp_keys)
    sinza['weekly']['wkPostsAcc'] = sum(
        safe_int(row[5]) for row in wmp_rows_wk[1:]
        if len(row) > 5 and str(row[2]).lower().strip() in sz_sl_keys)
    sinza['weekly']['moPostsAcc'] = sum(
        safe_int(row[5]) for row in mmp_rows[1:]
        if len(row) > 5 and str(row[2]).lower().strip() in sz_sl_keys)
    # Stock sums for description text (col R = idx 17)
    sinza['weekly']['wkInstockPostedSum']    = sum(safe_int(row[17]) for row in sl_rows[1:] if len(row) > 28 and safe_int(row[17]) > 0 and (_is_checked(row, 28) or _is_x(row, 28)) and str(row[2]).lower().strip() in sz_wmp_keys)
    sinza['weekly']['wkInstockNotPostedSum'] = sum(safe_int(row[17]) for row in sl_rows[1:] if len(row) > 28 and safe_int(row[17]) > 0 and (_is_checked(row, 28) or _is_x(row, 28)) and str(row[2]).lower().strip() not in sz_wmp_keys)
    sinza['weekly']['moInstockPostedSum']    = sum(safe_int(row[17]) for row in sl_rows[1:] if len(row) > 28 and safe_int(row[17]) > 0 and (_is_checked(row, 28) or _is_x(row, 28)) and str(row[2]).lower().strip() in sz_mmp_keys)
    sinza['weekly']['moInstockNotPostedSum'] = sum(safe_int(row[17]) for row in sl_rows[1:] if len(row) > 28 and safe_int(row[17]) > 0 and (_is_checked(row, 28) or _is_x(row, 28)) and str(row[2]).lower().strip() not in sz_mmp_keys)

    # Sinza monthly unposted: MONTHLY_SALES col Y (idx 24) for bags NOT in MMP (col F>0, col J=✅)
    sz_mmp_chk_keys = set()
    for row in mmp_rows[1:]:
        if len(row) > 9 and safe_int(row[5]) > 0 and _is_checked(row, 9):
            sz_mmp_chk_keys.add((str(row[0]).lower().strip(), str(row[2]).lower().strip()))
    sinza['weekly']['moUnposted'] = sum(
        safe_int(row[24]) for row in ms_rows[1:]
        if len(row) > 24 and (str(row[0]).lower().strip(), str(row[1]).lower().strip()) not in sz_mmp_chk_keys)

    sinza.update(_fetch_sinza_weekly(wmp_rows_wk, ws_rows_wk))
    sinza.update(_fetch_sinza_monthly(ms_rows, mmp_rows))

    # Uganda accuracy: STOCK_LEVELS col S (idx 18) > 0, col AD (idx 29) = ✅ or x → Uganda-specific rows
    ug_sl_keys = set()
    for row in sl_rows[1:]:
        if len(row) > 29 and safe_int(row[18]) > 0 and (_is_checked(row, 29) or _is_x(row, 29)):
            ug_sl_keys.add(str(row[2]).lower().strip())

    ug_wmp_keys = set()
    for row in wmp_rows_wk[1:]:
        if len(row) > 6 and safe_int(row[6]) > 0:
            ug_wmp_keys.add(str(row[2]).lower().strip())

    ug_mmp_keys = set()
    for row in mmp_rows[1:]:
        if len(row) > 6 and safe_int(row[6]) > 0:
            ug_mmp_keys.add(str(row[2]).lower().strip())

    uganda['weekly']['wkInstockPosted']    = len(ug_sl_keys & ug_wmp_keys)
    uganda['weekly']['wkInstockNotPosted'] = len(ug_sl_keys - ug_wmp_keys)
    uganda['weekly']['moInstockPosted']    = len(ug_sl_keys & ug_mmp_keys)
    uganda['weekly']['moInstockNotPosted'] = len(ug_sl_keys - ug_mmp_keys)
    uganda['weekly']['wkPostsAcc'] = sum(
        safe_int(row[6]) for row in wmp_rows_wk[1:]
        if len(row) > 6 and str(row[2]).lower().strip() in ug_sl_keys)
    uganda['weekly']['moPostsAcc'] = sum(
        safe_int(row[6]) for row in mmp_rows[1:]
        if len(row) > 6 and str(row[2]).lower().strip() in ug_sl_keys)
    # Stock sums for description text (col S = idx 18)
    uganda['weekly']['wkInstockPostedSum']    = sum(safe_int(row[18]) for row in sl_rows[1:] if len(row) > 29 and safe_int(row[18]) > 0 and (_is_checked(row, 29) or _is_x(row, 29)) and str(row[2]).lower().strip() in ug_wmp_keys)
    uganda['weekly']['wkInstockNotPostedSum'] = sum(safe_int(row[18]) for row in sl_rows[1:] if len(row) > 29 and safe_int(row[18]) > 0 and (_is_checked(row, 29) or _is_x(row, 29)) and str(row[2]).lower().strip() not in ug_wmp_keys)
    uganda['weekly']['moInstockPostedSum']    = sum(safe_int(row[18]) for row in sl_rows[1:] if len(row) > 29 and safe_int(row[18]) > 0 and (_is_checked(row, 29) or _is_x(row, 29)) and str(row[2]).lower().strip() in ug_mmp_keys)
    uganda['weekly']['moInstockNotPostedSum'] = sum(safe_int(row[18]) for row in sl_rows[1:] if len(row) > 29 and safe_int(row[18]) > 0 and (_is_checked(row, 29) or _is_x(row, 29)) and str(row[2]).lower().strip() not in ug_mmp_keys)

    uganda.update(_fetch_uganda_weekly(wmp_rows_wk, ws_rows_wk))
    uganda.update(_fetch_uganda_monthly(ms_rows, mmp_rows))

    (mo_posts, mo_sales, mo_unposted, mo_total,
     not_offer_posted_mo, offer_not_posted_mo, offer_posted_mo, not_offer_not_posted_mo,
     mo_expected, mo_posts_x, mo_sales_no_post,
     mo_mkt_pct, not_offer_not_posted_mo_sales,
     mo_not_offer_mkt_pct,
     offer_not_posted_mo_sales) = _fetch_monthly_kenya(ms_rows, mmp_rows)

    # Bags On Offer % — MONTHLY_TARGET col C where col F = ✅, split by complete weeks
    total_target = sum(
        safe_int(row[2])
        for row in mt_rows[1:]
        if len(row) > 2
    )
    mt_offer_target = sum(
        safe_int(row[2])
        for row in mt_rows[1:]
        if len(row) > 5 and _is_checked(row, 5)
    )
    complete_weeks = count_complete_weeks_in_month()
    offer_adjusted      = mt_offer_target - offer_not_posted_mo
    offer_weekly_target = offer_adjusted / complete_weeks if offer_adjusted > 0 else 0
    offer_sales_pct_wk  = (
        round(min(wk_sales / offer_weekly_target, 1.0) * 100, 1)
        if offer_weekly_target > 0 else 0.0
    )
    offer_sales_pct_mo = (
        round(min(mo_sales / offer_adjusted, 1.0) * 100, 1)
        if offer_adjusted > 0 else 0.0
    )
    # Bags Not on Offer % — MONTHLY_TARGET col C where col F = x, split by complete weeks
    mt_not_offer_target = sum(
        safe_int(row[2])
        for row in mt_rows[1:]
        if len(row) > 5 and _is_x(row, 5)
    )
    not_offer_adjusted     = mt_not_offer_target - not_offer_posted_mo
    not_offer_weekly_target = not_offer_adjusted / complete_weeks if not_offer_adjusted > 0 else 0
    not_offer_sales_pct_wk = (
        round(min(not_offer_not_posted_wk / not_offer_weekly_target, 1.0) * 100, 1)
        if not_offer_weekly_target > 0 else 0.0
    )
    not_offer_sales_pct_mo = (
        round(min(not_offer_not_posted_mo / mt_not_offer_target, 1.0) * 100, 1)
        if mt_not_offer_target > 0 else 0.0
    )

    print(f"\n  ── Bags On Offer % ───────────────────────────────────────")
    print(f"  MONTHLY_TARGET col C (col F=✅): {fmt_int(mt_offer_target)}")
    print(f"  Complete weeks this month      : {complete_weeks}")
    print(f"  Offer weekly target            : {fmt_int(round(offer_weekly_target))}")
    print(f"  Offer sales % (wk)             : {offer_sales_pct_wk}%")
    print(f"  Bags Not Posted & On Offer (mo): {offer_not_posted_mo}")
    print(f"  Adjusted offer target (mo)     : {fmt_int(offer_adjusted)}")
    print(f"  Offer sales % (mo)             : {offer_sales_pct_mo}%")
    print(f"\n  ── Bags Not on Offer % ───────────────────────────────────")
    print(f"  MONTHLY_TARGET col C (col F=x) : {fmt_int(mt_not_offer_target)}")
    print(f"  Bags Posted & Not on Offer (mo): {fmt_int(not_offer_posted_mo)}")
    print(f"  Adjusted target (target - mo)  : {fmt_int(not_offer_adjusted)}")
    print(f"  Not-offer weekly target        : {fmt_int(round(not_offer_weekly_target))}")
    print(f"  Not-offer not-posted wk        : {not_offer_not_posted_wk}")
    print(f"  Not-offer sales % (wk)         : {not_offer_sales_pct_wk}%")

    # S3: STOCK_LEVELS col Y (idx 24) filtered by col AB (idx 27)
    s3_posted = sum(
        safe_int(row[24])
        for row in sl_rows[1:]
        if len(row) > 24 and _is_checked(row, 27)
    )
    s3_not_posted = sum(
        safe_int(row[24])
        for row in sl_rows[1:]
        if len(row) > 24 and _is_x(row, 27)
    )
    # S3: total posts done monthly (col E) where col I has x OR ✅
    s3_mo_posts = sum(
        safe_int(row[4])
        for row in mmp_rows[1:]
        if len(row) > 4 and (_is_checked(row, 8) or _is_x(row, 8))
    )
    # S3: count of distinct bags with posts in WMP / MMP (for COUNT display)
    s3_wk_posts_count = len({
        str(row[2]).lower().strip()
        for row in wmp_rows_wk[1:]
        if len(row) > 4 and safe_int(row[4]) > 0 and (_is_checked(row, 8) or _is_x(row, 8))
    })
    s3_mo_posts_count = len({
        str(row[2]).lower().strip()
        for row in mmp_rows[1:]
        if len(row) > 4 and safe_int(row[4]) > 0 and (_is_checked(row, 8) or _is_x(row, 8))
    })
    # S3: stock sum for monthly not-posted bags (description value)
    mo_instock_not_posted_sum = sum(
        safe_int(row[24])
        for row in sl_rows[1:]
        if len(row) > 24 and safe_int(row[24]) > 20
        and (str(row[0]).lower().strip(), str(row[2]).lower().strip()) not in kenya_mmp_keys
    )

    # No-convert monthly: posted (col I checked) but zero MONTHLY_SALES col X
    nc_mo = _build_no_convert(
        post_rows=mmp_rows,
        sales_rows=ms_rows,
        sales_col_indices=[23],           # col X only
        check_col=8, count_col=4,
        sl_rows=sl_rows, stock_col=24,
        spp=KENYA_SPP,
    )

    print(f"\n  ── Kenya S3 Stock ────────────────────────────────────────")
    print(f"  In-stock & posted     (STOCK_LEVELS col Y, ✅ in AB): {fmt_int(s3_posted)}")
    print(f"  In-stock & not posted (STOCK_LEVELS col Y, x  in AB): {fmt_int(s3_not_posted)}")
    print(f"  S3 weekly posts  (WEEKLY_MARKETING_POST col E, x or ✅ in I): {s3_wk_posts}")
    print(f"  S3 monthly posts (MONTHLY_MARKETING_POST col E, x or ✅ in I): {fmt_int(s3_mo_posts)}")
    print(f"  No-convert monthly bags                                     : {len(nc_mo)}")

    return (kenya, sinza, uganda,
            wk_posts, wk_sales, wk_expected, wk_unposted,
            mo_posts, mo_sales, mo_unposted, mo_total, mo_expected, mo_posts_x, mo_sales_no_post,
            s3_posted, s3_not_posted, s3_wk_posts, s3_mo_posts,
            s3_wk_posts_count, s3_mo_posts_count, mo_instock_not_posted_sum,
            nc_wk, nc_mo,
            not_offer_posted_wk, offer_not_posted_wk, offer_posted_wk, not_offer_not_posted_wk,
            wk_instock_posted, wk_instock_not_posted, mo_instock_not_posted,
            not_offer_posted_mo, offer_not_posted_mo, offer_posted_mo, not_offer_not_posted_mo,
            offer_sales_pct_wk, offer_sales_pct_mo,
            not_offer_sales_pct_wk, not_offer_sales_pct_mo,
            total_target, complete_weeks,
            proj_weekly_sales, instock_not_posted_list, offer_posted_wk_x,
            offer_posted_wk_count,
            wk_posts_x, wk_sales_no_post, wk_mkt_pct,
            mo_posts_x, mo_sales_no_post, mo_mkt_pct,
            not_offer_not_posted_wk_sales, not_offer_not_posted_mo_sales,
            wk_not_offer_mkt_pct, mo_not_offer_mkt_pct,
            offer_not_posted_wk_sales, offer_not_posted_mo_sales)


# ── RUN ───────────────────────────────────────────────────────

print("Fetching Posting Analysis data...")
(kenya, sinza, uganda,
 wk_posts, wk_sales, wk_expected, wk_unposted,
 mo_posts, mo_sales, mo_unposted, mo_total, mo_expected, mo_posts_x, mo_sales_no_post,
 s3_posted, s3_not_posted, s3_wk_posts, s3_mo_posts,
 s3_wk_posts_count, s3_mo_posts_count, mo_instock_not_posted_sum,
 nc_wk, nc_mo,
 not_offer_posted_wk, offer_not_posted_wk, offer_posted_wk, not_offer_not_posted_wk,
 wk_instock_posted, wk_instock_not_posted, mo_instock_not_posted,
 not_offer_posted_mo, offer_not_posted_mo, offer_posted_mo, not_offer_not_posted_mo,
 offer_sales_pct_wk, offer_sales_pct_mo,
 not_offer_sales_pct_wk, not_offer_sales_pct_mo,
 total_target, complete_weeks,
 proj_weekly_sales, instock_not_posted_list, offer_posted_wk_x,
 offer_posted_wk_count,
 wk_posts_x, wk_sales_no_post, wk_mkt_pct,
 mo_posts_x, mo_sales_no_post, mo_mkt_pct,
 not_offer_not_posted_wk_sales, not_offer_not_posted_mo_sales,
 wk_not_offer_mkt_pct, mo_not_offer_mkt_pct,
 offer_not_posted_wk_sales, offer_not_posted_mo_sales) = fetch_posting_data()

# ── Sales-Achieved % snapshot: one row per CALENDAR week ──
# Weeks are numbered so the opening partial week of the month is Wk 1
# (e.g. Jul 1–4 = Wk 1, Jul 5–11 = Wk 2, Jul 12–18 = Wk 3, ...). Each time the
# posts-made signature changes within a week its % is refreshed in place; the
# row only rolls over to the next number when a new calendar week begins.
from datetime import date, timedelta

def _mkt_perfect_week_index(d):
    """Ordinal of d's Sun–Sat week within the month, counting every week that has
    at least one day in the month — so the opening partial week is Week 1."""
    year, month = d.year, d.month
    ms = date(year, month, 1)
    me = (date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)) - timedelta(days=1)
    ws = ms - timedelta(days=(ms.weekday() + 1) % 7)
    target = d - timedelta(days=(d.weekday() + 1) % 7)
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

def _mkt_week_label(d=None):
    wi = _mkt_perfect_week_index(d or date.today())
    return ("Wk " + str(wi)) if wi else "Partial"

MKT_HISTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posting_mkt_history.json")

def _pct_num(v):
    try:
        return round(float(str(v).replace('%', '').strip()), 1)
    except (ValueError, TypeError):
        return 0.0

def update_mkt_history(vals, sig):
    """vals = {kenya,sinza,uganda} %; sig = [kenya_posts, sinza_posts, uganda_posts]."""
    weeks = []
    if os.path.exists(MKT_HISTORY):
        try:
            with open(MKT_HISTORY, "r") as f:
                weeks = json.load(f).get("weeks", [])
        except (ValueError, OSError):
            weeks = []

    month = date.today().strftime("%b")
    wk_label = _mkt_week_label()
    if weeks and weeks[-1].get("label") == wk_label:
        # Same calendar week → refresh its % (and signature) to the latest read
        weeks[-1].update({"kenya": vals["kenya"], "sinza": vals["sinza"],
                          "uganda": vals["uganda"], "month": month, "_sig": sig})
    else:
        # A new calendar week has begun → new row
        weeks.append({
            "label": wk_label,
            "month": month,
            "kenya": vals["kenya"], "sinza": vals["sinza"], "uganda": vals["uganda"],
            "_sig":  sig,
        })
        weeks = weeks[-12:]

    with open(MKT_HISTORY, "w") as f:
        json.dump({"weeks": weeks}, f, indent=2)
    return weeks

mkt_pct_history = update_mkt_history(
    {"kenya":  _pct_num(wk_mkt_pct),
     "sinza":  _pct_num(sinza.get('szWkMktPct')),
     "uganda": _pct_num(uganda.get('ugWkMktPct'))},
    [wk_posts, sinza.get('szWkPosts', 0), uganda.get('ugWkPosts', 0)],
)

# ── Bags cleared by marketing: stock drop on posted bags since the week's baseline ──
STOCK_HISTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posting_stock_history.json")

def update_clearance(current, sig):
    """current = {region: {key: {productName,colour,category,bagType,stock}}}.
    A new week's baseline is captured whenever the posting signature changes;
    'cleared' = baseline stock − current stock (per posted bag)."""
    state = {}
    if os.path.exists(STOCK_HISTORY):
        try:
            with open(STOCK_HISTORY, "r") as f:
                state = json.load(f)
        except (ValueError, OSError):
            state = {}
    baseline = state.get("baseline") or {}
    history  = state.get("history") or []
    month    = date.today().strftime("%b")

    if (state.get("sig") is None) or (state.get("sig") != sig):
        baseline = current   # posting changed → re-baseline stock
        wk_label = _mkt_week_label()
        if not history or history[-1].get("label") != wk_label:
            history.append({"label": wk_label, "month": month,
                            "kenya": 0, "sinza": 0, "uganda": 0})
            history = history[-12:]

    lists, totals = {}, {}
    for region in ("kenya", "sinza", "uganda"):
        base, cur = baseline.get(region, {}), current.get(region, {})
        lst, tot = [], 0
        for key, b in base.items():
            cur_stock = (cur.get(key) or {}).get("stock", 0)
            drop = b.get("stock", 0) - cur_stock
            if drop > 0:
                lst.append({"productName": b.get("productName"), "colour": b.get("colour"),
                            "category": b.get("category"), "bagType": b.get("bagType"),
                            "prevStock": b.get("stock", 0), "curStock": cur_stock, "cleared": drop})
                tot += drop
        lst.sort(key=lambda x: -x["cleared"])
        lists[region], totals[region] = lst, tot
    if history:
        history[-1].update({"kenya": totals["kenya"], "sinza": totals["sinza"], "uganda": totals["uganda"]})

    with open(STOCK_HISTORY, "w") as f:
        json.dump({"sig": sig, "baseline": baseline, "history": history}, f, indent=2)
    return lists, totals, history

cleared_lists, cleared_totals, cleared_history = update_clearance(
    {"kenya": kenya.get('postedStock', {}), "sinza": sinza.get('postedStock', {}), "uganda": uganda.get('postedStock', {})},
    [wk_posts, sinza.get('szWkPosts', 0), uganda.get('ugWkPosts', 0)],
)

# Flatten Kenya into top-level PA keys (keeps HTML backward-compatible)
# Sinza goes under PA.sinza
inline_script = (
    "<!-- POST_DATA_START -->\n"
    "<script>\n"
    "const PA = {\n"
    # ── Kenya top-level ──
    f'  weeklyPostsMade:  {wk_posts},\n'
    f'  weeklySalesTotal: "{fmt_int(offer_posted_wk_count)}",\n'   # WS col AB for ✅-posted (on-offer) names — Kenya
    f'  weeklyExpected:   "{fmt_int(round(wk_expected))}",\n'
    f'  monthlyPostsMade: {mo_posts},\n'
    f'  monthlySalesTotal:"{fmt_int(mo_sales)}",\n'
    f'  monthlyExpected:  "{fmt_int(mo_expected)}",\n'
    f'  weeklyPostsNotOnOffer:  {wk_posts_x},\n'
    f'  weeklySalesNoPost:     "{fmt_int(wk_sales_no_post)}",\n'
    f'  wkMktPct:              "{wk_mkt_pct}%",\n'
    f'  monthlyPostsNotOnOffer: {mo_posts_x},\n'
    f'  monthlySalesNoPost:    "{fmt_int(mo_sales_no_post)}",\n'
    f'  moMktPct:              "{mo_mkt_pct}%",\n'
    f'  totalBagsSoldWeek:"{fmt_int(proj_weekly_sales)}",\n'
    f'  weeklyUnposted:   "{fmt_int(wk_unposted)}",\n'
    f'  monthlyUnposted:  "{fmt_int(mo_unposted)}",\n'
    f'  monthlyTotal:     "{fmt_int(mo_total)}",\n'
    f'  s3Posted:             "{fmt_int(s3_posted)}",\n'
    f'  s3NotPosted:          "{fmt_int(s3_not_posted)}",\n'
    f'  s3WkPosts:            {s3_wk_posts},\n'
    f'  s3MoPosts:            {s3_mo_posts},\n'
    f'  s3WkPostsCount:       {s3_wk_posts_count},\n'
    f'  s3MoPostsCount:       {s3_mo_posts_count},\n'
    f'  moInstockNotPostedSum:"{fmt_int(mo_instock_not_posted_sum)}",\n'
    f'  noConvertWk:         {json.dumps(nc_wk, ensure_ascii=False)},\n'
    f'  noConvertMo:         {json.dumps(nc_mo, ensure_ascii=False)},\n'
    f'  mktPctHistory:       {json.dumps(mkt_pct_history)},\n'
    f'  clearedKenya:        {json.dumps(cleared_lists["kenya"],  ensure_ascii=False)},\n'
    f'  clearedSinza:        {json.dumps(cleared_lists["sinza"],  ensure_ascii=False)},\n'
    f'  clearedUganda:       {json.dumps(cleared_lists["uganda"], ensure_ascii=False)},\n'
    f'  clearedTotals:       {json.dumps(cleared_totals)},\n'
    f'  clearedHistory:      {json.dumps(cleared_history)},\n'
    f'  notOfferPostedWk:    {not_offer_posted_wk},\n'
    f'  offerNotPostedWkSales: "{fmt_int(offer_not_posted_wk_sales)}",\n'
    f'  offerNotPostedMoSales: "{fmt_int(offer_not_posted_mo_sales)}",\n'
    f'  wkInstockPosted:     {wk_instock_posted},\n'
    f'  wkInstockNotPosted:  {wk_instock_not_posted},\n'
    f'  moInstockNotPosted:  {mo_instock_not_posted},\n'
    f'  offerNotPostedWk:    {offer_not_posted_wk},\n'
    f'  offerPostedWk:       {offer_posted_wk},\n'
    f'  notOfferNotPostedWk: {not_offer_not_posted_wk},\n'
    f'  notOfferNotPostedWkSales: "{fmt_int(not_offer_not_posted_wk_sales)}",\n'
    f'  notOfferPostedMo:    {not_offer_posted_mo},\n'
    f'  offerNotPostedMo:    {offer_not_posted_mo},\n'
    f'  offerPostedMo:       {offer_posted_mo},\n'
    f'  notOfferNotPostedMo: {not_offer_not_posted_mo},\n'
    f'  notOfferNotPostedMoSales: "{fmt_int(not_offer_not_posted_mo_sales)}",\n'
    f'  offerSalesPctWk:     {wk_mkt_pct},\n'
    f'  offerSalesPctMo:     {mo_mkt_pct},\n'
    f'  notOfferSalesPctWk:  {wk_not_offer_mkt_pct},\n'
    f'  notOfferSalesPctMo:  {mo_not_offer_mkt_pct},\n'
    f'  totalTarget:         {total_target},\n'
    f'  completeWeeks:       {complete_weeks},\n'
    f'  wkSumTotal:          {proj_weekly_sales},\n'
    f'  instockNotPosted: {json.dumps(instock_not_posted_list)},\n'
    f'  s1Count:          {kenya["s1Count"]},\n'
    f'  s2Count:          {kenya["s2Count"]},\n'
    f'  s3Count:          {kenya["s3Count"]},\n'
    f'  s3NotPostedCount: {kenya["s3NotPostedCount"]},\n'
    f'  s1Sales:          "{kenya["s1Sales"]}",\n'
    f'  s2Sales:          "{kenya["s2Sales"]}",\n'
    f'  s1Posts:          {kenya["s1Posts"]},\n'
    f'  s1Expected:       "{kenya["s1Expected"]}",\n'
    f'  salesFromPosting: {json.dumps(kenya["salesFromPosting"], ensure_ascii=False)},\n'
    f'  salesNoPost:      {json.dumps(kenya["salesNoPost"],      ensure_ascii=False)},\n'
    f'  accuracyBags:     {json.dumps(kenya["accuracyBags"],     ensure_ascii=False)},\n'
    # ── Sinza nested ──
    f'  sinza:            {json.dumps(sinza,   ensure_ascii=False)},\n'
    # ── Uganda nested ──
    f'  uganda:           {json.dumps(uganda,  ensure_ascii=False)}\n'
    "};\n"
    "</script>\n"
    "<!-- POST_DATA_END -->"
)

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(BASE_DIR, "POSTING (SALES YIELDS FROM ACCURATE POSTING).html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

html = re.sub(
    r"<!-- POST_DATA_START -->.*?<!-- POST_DATA_END -->",
    inline_script,
    html,
    flags=re.DOTALL
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

if not os.environ.get("DENRI_LAUNCHER"):
    webbrowser.open_new_tab(pathlib.Path(html_path).as_uri())
print("\nPOSTING (SALES YIELDS FROM ACCURATE POSTING).html updated.")
