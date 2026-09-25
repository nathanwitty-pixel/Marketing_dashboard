"""lib/odoo_tabs.py — the sales / stock / dispatch sheet tabs, rebuilt from live Odoo.

Replaces these Google-Sheet tabs with Postgres, row-for-row in the SAME layout
the page scripts already parse (same headers, same column letters, same
"SUM TOTAL" row), so a caller only swaps where the rows come from:

    WEEKLY_SALES      last complete Sun–Sat week   (matched the sheet within 11 bags)
    MONTHLY_SALES     the reporting month           (lib.report_month.month_window)
    STOCK_LEVELS      live on-hand                  (lib.stock)
    WEEKLY_DISPATCH   last complete Sun–Sat week   (sql/combined_distribution.sql)
    MONTHLY_DISPATCH  the reporting month

Where each column comes from:
  • COLOUR / CATEGORY / PRODUCT NAME / BAG TYPE — product_catalog.csv. These are
    the team's own labels (colour is a family: CROC BROWN → Brown; categories
    don't map 1:1 to Odoo's), and the posting tabs join on (colour, name), so
    they must match the sheet exactly. Odoo products missing from the catalogue
    are appended with a derived bag type / colour / category. Odoo renames are
    mapped back to the sheet name via product_aliases.csv (editable).
  • shop / total columns — Odoo, same bag-sale rules as sql/bags_sold_total.sql.
  • ✅ / x on-offer flags — MONTHLY_TARGET cols F/G/H (KENYA/SINZA/UGANDA) by bag
    type. That tab stays on the sheet; every product flag on the old tabs was
    exactly its bag type's MONTHLY_TARGET flag.

Use get_rows(sh, tab) in place of sh.worksheet(tab).get_all_values(). It falls
back to the sheet tab when Postgres is unreachable, so a DB outage never blanks
a page.

Refresh the catalogue from the sheet (e.g. after adding products there):
    python -m lib.odoo_tabs --refresh-catalog
"""
from __future__ import annotations

import csv
import datetime
import os
import re
from collections import Counter, defaultdict

from . import db, queries, report_month

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_FILE = os.path.join(BASE, "product_catalog.csv")
ALIASES_FILE = os.path.join(BASE, "product_aliases.csv")
SPREADSHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"

TABS = ("WEEKLY_SALES", "MONTHLY_SALES", "STOCK_LEVELS", "WEEKLY_DISPATCH", "MONTHLY_DISPATCH")

# The 19 shop columns, in sheet order (E..W on the weekly/stock/dispatch tabs, D..V on MONTHLY_SALES).
SHOPS = ["STARMALL", "MOMBASA", "NAKURU", "ELDORET", "KISUMU", "MERU", "THIKA", "HAZINA",
         "KITENGELA", "WEBSITE", "NANYUKI", "KAKAMEGA", "HILTON", "SINZA", "UGANDA",
         "KISII", "KTDA", "BUSIA", "RONGAI"]
OUTSIDE = ("SINZA", "UGANDA")

# Odoo stock-location top code → sheet shop column (see lib/stock.py for why an allow-list).
STOCK_CODE_TO_SHOP = {"STAR": "STARMALL", "MSA": "MOMBASA", "NAKS": "NAKURU", "ELD": "ELDORET",
                      "KSM": "KISUMU", "MERU": "MERU", "THK": "THIKA", "HAZ": "HAZINA",
                      "KITE": "KITENGELA", "NAN": "NANYUKI", "KAK": "KAKAMEGA", "HTN": "HILTON",
                      "KSI": "KISII", "KTDA": "KTDA", "BUSIA": "BUSIA", "RONG": "RONGAI",
                      "DAR": "SINZA", "UG": "UGANDA"}

TICK, CROSS = "✅️", "x"

# Per-product, per-shop bags sold. Filters are sql/bags_sold_total.sql's (the dashboard's
# headline "bags sold"); the shop mapping is sql/shop_bags_sold.sql's.
SALES_BY_PRODUCT_SHOP = """
SELECT UPPER(pt."name") AS product,
       CASE
         WHEN lower(pc."name") IN ('website sales','website','jumia') OR p.session_id IS NULL THEN 'WEBSITE'
         WHEN lower(pc."name") IN ('sinza','dar-es-alam')             THEN 'SINZA'
         WHEN lower(pc."name") IN ('ktda','ktda shop')                THEN 'KTDA'
         ELSE UPPER(pc."name")
       END AS shop,
       SUM(pl.qty)::numeric AS bags
FROM pos_order p
JOIN pos_order_line pl ON pl.order_id = p.id
LEFT JOIN pos_session ps ON p.session_id = ps.id
LEFT JOIN pos_config pc ON ps.config_id = pc.id
LEFT JOIN product_product pp ON pl.product_id = pp.id
LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
LEFT JOIN product_category pcat ON pcat.id = pt.categ_id
WHERE p.date_order::date BETWEEN CAST(:start_date AS DATE) AND CAST(:end_date AS DATE)
  AND p.state IN ('done', 'paid')
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


# ── windows ───────────────────────────────────────────────────

def last_complete_week(ref: datetime.date | None = None):
    """The most recent COMPLETE Sun–Sat week before `ref` (today) — what the sheet's
    weekly tabs held (verified 25 Sep 2026: Sun 13 → Sat 19 Sep)."""
    ref = ref or datetime.date.today()
    this_sunday = ref - datetime.timedelta(days=(ref.weekday() + 1) % 7)
    start = this_sunday - datetime.timedelta(days=7)
    return start, start + datetime.timedelta(days=6)


def default_window(tab):
    return last_complete_week() if tab.startswith("WEEKLY") else report_month.month_window()


# ── names & catalogue ─────────────────────────────────────────

def norm(s) -> str:
    """Name key shared by the catalogue and Odoo: upper-case, '.'→space, collapsed spaces."""
    return re.sub(r"\s+", " ", str(s).upper().replace(".", " ")).strip()


_ALIASES = None


def _aliases():
    """{NORM(odoo name): NORM(sheet name)} from product_aliases.csv — products Odoo renamed
    (CESS HB BLACK → CESS BLACK, STANDARD TRAVEL GREY → TRAVEL GREY, …)."""
    global _ALIASES
    if _ALIASES is None:
        _ALIASES = {}
        try:
            with open(ALIASES_FILE, encoding="utf-8", newline="") as f:
                for r in csv.DictReader(f):
                    if r.get("ODOO NAME") and r.get("SHEET NAME"):
                        _ALIASES[norm(r["ODOO NAME"])] = norm(r["SHEET NAME"])
        except OSError:
            pass
    return _ALIASES


def odoo_name(sheet_name) -> str:
    """Odoo's spelling of a catalogue name (the reverse of product_aliases.csv), for display:
    LAMORA SKYE BLUE → LAMORA SKY BLUE. Unaliased names come back norm()ed."""
    n = norm(sheet_name)
    return next((o for o, s in _aliases().items() if s == n), n)


def base_name(s) -> str:
    """The catalogue key for an Odoo product name: norm() without the "[REJECT]" tag (the
    sheet counted reject-clearance units under the product itself: ACE BEIGE [REJECT] →
    ACE BEIGE), then product_aliases.csv applied."""
    n = norm(re.sub(r"\[\s*REJECT\s*\]", " ", str(s), flags=re.I))
    return _aliases().get(n, n)


def load_catalog():
    """[{colour, category, name, bag}] in sheet order, from product_catalog.csv."""
    try:
        with open(CATALOG_FILE, encoding="utf-8", newline="") as f:
            return [{"colour": r["COLOUR"], "category": r["CATEGORY"],
                     "name": r["PRODUCT NAME"], "bag": r["BAG TYPE"]} for r in csv.DictReader(f)]
    except OSError:
        return []


class _Deriver:
    """Labels for an Odoo product the catalogue doesn't know yet, learnt from the catalogue:
    bag type = longest known bag type the name starts with; category = that bag type's usual
    category; colour = the family the catalogue most often gives the name's trailing words."""

    def __init__(self, catalog):
        self.bags = sorted({norm(c["bag"]) for c in catalog if c["bag"]}, key=len, reverse=True)
        cat_votes = defaultdict(Counter)
        colour_votes = defaultdict(Counter)
        for c in catalog:
            b, n = norm(c["bag"]), norm(c["name"])
            cat_votes[b][c["category"]] += 1
            rest = n[len(b):].strip() if n.startswith(b) else n
            if rest and c["colour"]:
                colour_votes[rest][c["colour"]] += 1
                colour_votes[rest.split()[-1]][c["colour"]] += 1
        self.category = {b: v.most_common(1)[0][0] for b, v in cat_votes.items()}
        self.colour = {k: v.most_common(1)[0][0] for k, v in colour_votes.items()}

    def __call__(self, name):
        n = norm(name)
        bag = next((b for b in self.bags if n == b or n.startswith(b + " ")), n.split(" ")[0])
        rest = n[len(bag):].strip()
        colour = self.colour.get(rest) or (self.colour.get(rest.split()[-1]) if rest else "") or ""
        return {"colour": colour, "category": self.category.get(bag, ""), "name": n, "bag": bag}


# ── Odoo fetches ──────────────────────────────────────────────

def _ok():
    try:
        return bool(db.check_connection()[0])
    except Exception:                                        # noqa: BLE001
        return False


def _num(v):
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def sales_by_product_shop(start, end):
    """{NORM(product): {SHOP: bags}} of POS bag sales in [start, end]; None if DB unreachable."""
    df = db.run_query_cached(SALES_BY_PRODUCT_SHOP,
                             {"start_date": str(start), "end_date": str(end),
                              "excluded": queries.excluded_products()}, ttl_min=30)
    if df is None:
        return None
    out = defaultdict(lambda: defaultdict(float))
    for _, r in df.iterrows():
        shop = str(r["shop"]).upper()
        if shop in SHOPS:                       # STAFF POS / MARKETING tills have no sheet column
            out[base_name(r["product"])][shop] += _num(r["bags"])
    return out


def dispatch_by_product_shop(start, end):
    """{NORM(product): {SHOP: bags distributed in}} from combined_distribution.sql's per-product rows."""
    with open(os.path.join(BASE, "sql", "combined_distribution.sql"), encoding="utf-8") as f:
        sql = f.read()
    df = db.run_query_cached(sql, {"start_date": str(start), "end_date": str(end)}, ttl_min=30)
    if df is None:
        return None
    out = defaultdict(lambda: defaultdict(float))
    for _, r in df[df["sort_order"] == 0].iterrows():
        for shop in SHOPS:
            if shop in df.columns and _num(r[shop]):
                out[base_name(r["Product"])][shop] += _num(r[shop])
    return out


def stock_by_product_shop():
    """{NORM(product): {SHOP: on-hand}} live, Kenya shops + Sinza (DAR) + Uganda (UG)."""
    from . import stock
    by_code = stock.odoo_stock_by_shop_code(codes=tuple(STOCK_CODE_TO_SHOP), positive_only=False)
    if not by_code:
        return None
    out = defaultdict(lambda: defaultdict(float))
    for code, prods in by_code.items():
        shop = STOCK_CODE_TO_SHOP.get(code)
        if shop:
            for name, qty in prods.items():
                out[base_name(name)][shop] += qty
    return out


_MT_CACHE = {}


def prime_offer_flags(mt_rows):
    """Seed offer_flags() from MONTHLY_TARGET rows the caller already read (saves a re-read)."""
    if mt_rows:
        _MT_CACHE["flags"] = {
            norm(r[0]): tuple(len(r) > c and "✅" in str(r[c]) for c in (5, 6, 7))
            for r in mt_rows[1:] if r and str(r[0]).strip()
        }


def offer_flags(sh=None):
    """{BAG TYPE: (kenya, sinza, uganda) on-offer bools} from MONTHLY_TARGET cols F/G/H."""
    if "flags" not in _MT_CACHE:
        if sh is None:
            from google_auth import get_gspread_client
            sh = get_gspread_client().open_by_key(SPREADSHEET_ID)
        prime_offer_flags(sh.worksheet("MONTHLY_TARGET").get_all_values())
    return _MT_CACHE.get("flags", {})


# ── row builders (exact sheet layouts) ────────────────────────

def _fmt(v):
    v = round(v, 2)
    return str(int(v)) if v == int(v) else str(v)


def _products(values, catalog):
    """Catalogue rows (sheet order, all of them — zeros included, like the sheet) followed by
    any Odoo product with non-zero figures that the catalogue lacks, with derived labels."""
    known = {norm(c["name"]) for c in catalog}
    extra = sorted(n for n, shops in values.items() if n not in known and any(shops.values()))
    derive = _Deriver(catalog)
    return catalog + [derive(n) for n in extra]


def _flag_cells(bag, flags):
    f = flags.get(norm(bag), (False, False, False))
    return [TICK if x else CROSS for x in f]


def build_rows(tab, values, catalog, flags):
    """Sheet-shaped rows for `tab` from {NORM(product): {SHOP: qty}}."""
    products = _products(values, catalog)
    body, totals = [], defaultdict(float)
    for p in products:
        shops = values.get(norm(p["name"]), {})
        q = [shops.get(s, 0.0) for s in SHOPS]
        by = dict(zip(SHOPS, q))
        total = sum(q)
        kenya = total - by["SINZA"] - by["UGANDA"]
        if tab == "WEEKLY_SALES":
            cells = ([p["colour"], p["category"], p["name"], p["bag"]] + [_fmt(x) for x in q]
                     + [_fmt(total)] + _flag_cells(p["bag"], flags) + [_fmt(kenya)])
        elif tab == "MONTHLY_SALES":
            cells = ([p["colour"], p["name"], p["bag"]] + [_fmt(x) for x in q]
                     + [_fmt(total), _fmt(kenya), _fmt(by["SINZA"]), _fmt(by["UGANDA"]),
                        _fmt(by["SINZA"] + by["UGANDA"])] + _flag_cells(p["bag"], flags))
        elif tab == "STOCK_LEVELS":
            kenya_shops = kenya - by["WEBSITE"]
            cells = ([p["colour"], p["category"], p["name"], p["bag"]] + [_fmt(x) for x in q]
                     + ["", _fmt(kenya_shops), _fmt(by["SINZA"] + by["UGANDA"]), ""]
                     + _flag_cells(p["bag"], flags))
        else:  # WEEKLY_DISPATCH / MONTHLY_DISPATCH — col X is "TOTAL ( KENYA )"
            cells = ([p["colour"], p["category"], p["name"], p["bag"]] + [_fmt(x) for x in q]
                     + [_fmt(kenya)])
        body.append(cells)
        for s, x in by.items():
            totals[s] += x
        totals["_total"] += total
        totals["_kenya"] += kenya

    header = HEADERS[tab]
    rows = [header] + body
    if tab != "MONTHLY_SALES":                   # the sheet's MONTHLY_SALES has no SUM TOTAL row
        t = ["", "", "SUM TOTAL", ""] + [_fmt(totals[s]) for s in SHOPS]
        if tab == "WEEKLY_SALES":
            t += [_fmt(totals["_total"]), "", "", "", _fmt(totals["_kenya"])]
        elif tab.endswith("DISPATCH"):
            t += [_fmt(totals["_kenya"])]
        rows.append(t)
    return rows


HEADERS = {
    "WEEKLY_SALES": ["COLOUR", "CATEGORY", "PRODUCT NAME", "BAG TYPE"] + SHOPS
                    + ["TOTAL", "KENYA", "SINZA", "UGANDA", "KENYA"],
    "MONTHLY_SALES": ["COLOUR", "PRODUCT NAME", "BAG TYPE"] + SHOPS
                     + ["TOTAL", "KENYA", "SINZA", "UGANDA", "OUTSIDE KENYA ", "KENYA", "SINZA", "UGANDA"],
    "STOCK_LEVELS": ["COLOUR", "CATEGORY", "PRODUCT NAME", "BAG TYPE"] + SHOPS
                    + ["KTDA MAIN STORE", "KENYA", "OUTSIDE KENYA", "SAFETY NET", "KENYA", "SINZA", "UGANDA"],
    "WEEKLY_DISPATCH": ["COLOUR", "CATEGORY", "PRODUCT NAME", "BAG TYPE"] + SHOPS + ["TOTAL ( KENYA )"],
    "MONTHLY_DISPATCH": ["COLOUR", "CATEGORY", "PRODUCT NAME", "BAG TYPE"] + SHOPS + ["TOTAL ( KENYA )"],
}


# ── public API ────────────────────────────────────────────────

_ROWS_MEMO = {}


def tab_rows(tab, sh=None, window=None):
    """Sheet-shaped rows for `tab` built from Odoo, or None when Postgres is unreachable.
    window=(start, end) overrides the tab's default period (see default_window)."""
    if tab not in TABS:
        raise ValueError(f"{tab} is not an Odoo-backed tab")
    key = (tab, tuple(str(d) for d in window) if window else None)
    if key not in _ROWS_MEMO:
        _ROWS_MEMO[key] = _build(tab, sh, window)
    return _ROWS_MEMO[key]


def _build(tab, sh, window):
    if not _ok():
        return None
    catalog = load_catalog()
    if tab == "STOCK_LEVELS":
        values = stock_by_product_shop()
    else:
        start, end = window or default_window(tab)
        fetch = sales_by_product_shop if tab.endswith("SALES") else dispatch_by_product_shop
        values = fetch(start, end)
    if values is None:
        return None
    flags = offer_flags(sh) if tab in ("WEEKLY_SALES", "MONTHLY_SALES", "STOCK_LEVELS") else {}
    return build_rows(tab, values, catalog, flags)


SOURCE = {}   # tab → "odoo" | "sheet": where get_rows() last got it (callers that persist state check this)


def get_rows(sh, tab, window=None):
    """Drop-in for sh.worksheet(tab).get_all_values(): Odoo first, the sheet tab as fallback."""
    try:
        rows = tab_rows(tab, sh=sh, window=window)
    except Exception as e:                                   # noqa: BLE001 — never fail a page on this
        print(f"  {tab}: Odoo build failed ({e}) — using the sheet tab.")
        rows = None
    if rows is None:
        print(f"  {tab}: Odoo unreachable — using the sheet tab.")
        SOURCE[tab] = "sheet"
        return sh.worksheet(tab).get_all_values()
    SOURCE[tab] = "odoo"
    period = "" if tab == "STOCK_LEVELS" else " %s → %s" % (window or default_window(tab))
    print(f"  {tab}: from Odoo{period} ({len(rows) - 1} rows)")
    return rows


def catalog_rows():
    """[header] + [[COLOUR, CATEGORY, PRODUCT NAME, BAG TYPE], …] — the label columns
    (A..D) shared by WEEKLY_SALES / STOCK_LEVELS / *_DISPATCH, straight from the catalogue.
    For callers that only need labels (e.g. category by bag type); needs no DB."""
    return [["COLOUR", "CATEGORY", "PRODUCT NAME", "BAG TYPE"]] + [
        [c["colour"], c["category"], c["name"], c["bag"]] for c in load_catalog()]


def refresh_catalog(sh=None):
    """Rewrite product_catalog.csv from the sheet's WEEKLY_SALES / MONTHLY_SALES product rows."""
    if sh is None:
        from google_auth import get_gspread_client
        sh = get_gspread_client().open_by_key(SPREADSHEET_ID)
    seen, out = set(), []
    for tab, (ci, ki, ni, bi) in (("WEEKLY_SALES", (0, 1, 2, 3)), ("MONTHLY_SALES", (0, None, 1, 2))):
        for r in sh.worksheet(tab).get_all_values()[1:]:
            if len(r) <= max(ni, bi):
                continue
            name = r[ni].strip()
            if not name or "TOTAL" in name.upper() or norm(name) in seen:
                continue
            seen.add(norm(name))
            out.append([r[ci].strip(), (r[ki].strip() if ki is not None else ""), name, r[bi].strip()])
    with open(CATALOG_FILE, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["COLOUR", "CATEGORY", "PRODUCT NAME", "BAG TYPE"])
        w.writerows(out)
    print(f"product_catalog.csv: {len(out)} products")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, BASE)
    if "--refresh-catalog" in sys.argv:
        refresh_catalog()
    else:
        print(__doc__)
