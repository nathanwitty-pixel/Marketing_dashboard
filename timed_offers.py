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
from datetime import date

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
    cfg = {"market": "Kenya", "startDate": "", "endDate": "",
           "bags": ["Kai", "Pioneer", "Double Press", "Antitheft", "Code 3", "School bag"]}
    try:
        with open(CONFIG_FILE, encoding="utf-8") as f:
            raw = json.load(f)
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

TO = {
    "market":     CFG["market"],
    "startDate":  CFG["startDate"],
    "endDate":    CFG["endDate"],
    "windowLabel": _win_label(CFG["startDate"], CFG["endDate"]),
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

print(f"timed_offers.html updated  ({TO['windowLabel']}, {CFG['market']}).")
print(f"  Sales source        : {'Odoo (live)' if sales_live else 'DB UNREACHABLE — zeros'}")
for r in bag_rows:
    pp = f"{r['perPost']}" if r["perPost"] is not None else "—"
    print(f"    {r['name']:<14} sold {r['sold']:>4}   posts {r['posts']:>3}   sold/post {pp}")
print(f"  TOTAL sold          : {fmt_int(total_sold)}")
print(f"  TOTAL posts (Kenya) : {fmt_int(total_posts)}")
