"""
generate_insights.py
─────────────────────────────────────────────────────────────────
Regenerates insights.html from the data already injected into the
dashboard HTML files. No Google Sheets calls — run it AFTER the other
dashboard scripts (main.py does this automatically).

    python generate_insights.py
"""
import os, re, json
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── PARSE HELPERS ─────────────────────────────────────────────

def read_block(filename, start, end):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    m = re.search(re.escape(start) + r"(.*?)" + re.escape(end), txt, re.DOTALL)
    return m.group(1) if m else ""

# The injected blocks mix two styles: top-level keys are plain JS identifiers
# (wkMktPct: "65.8%"), while nested objects come from json.dumps and are quoted
# ("szWkMktPct": "15.0%"). The optional `"?` after the key matches both — without
# it every nested lookup (Sinza / Uganda) silently fell back to the default.
def gstr(block, key, default=""):
    m = re.search(rf'\b{key}"?\s*:\s*"([^"]*)"', block)
    return m.group(1) if m else default

def graw(block, key, default=0.0):
    m = re.search(rf'\b{key}"?\s*:\s*(-?[\d.]+)', block)
    return float(m.group(1)) if m else default

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

def fmt(n):
    return f"{int(round(n)):,}"

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

# ── READ ALL DASHBOARD DATA ───────────────────────────────────

print("Generating insights from dashboard data...")

perf = read_block("current_performance.html", "<!-- PERF_DATA_START -->", "<!-- PERF_DATA_END -->")
proj = read_block("current_performance.html", "<!-- PROJ_DATA_START -->", "<!-- PROJ_DATA_END -->")
np_  = read_block("new_products.html", "<!-- NEW_PROD_DATA_START -->", "<!-- NEW_PROD_DATA_END -->")
oa   = read_block("offer_type_analysis.html", "<!-- OFFER_DATA_START -->", "<!-- OFFER_DATA_END -->")
pa   = read_block("POSTING (SALES YIELDS FROM ACCURATE POSTING).html", "<!-- POST_DATA_START -->", "<!-- POST_DATA_END -->")

missing = [n for n, b in [("current_performance", perf), ("projections", proj),
                          ("new_products", np_), ("offer_type", oa), ("posting", pa)] if not b]
if missing:
    print(f"  Warning: missing data blocks: {', '.join(missing)} — run those dashboards first.")

# Current performance
sales        = num(gstr(perf, "sales"))
sales_pct    = num(gstr(perf, "salesPctAchieved"))
remaining    = num(gstr(perf, "remainingTarget"))
wow_pct      = num(gstr(perf, "wowSalesPct"))
wow_bags     = num(gstr(perf, "wowSalesBags"))
weekly_sales = num(gstr(perf, "weeklySalesTotal"))
prev_bags    = num(gstr(perf, "previousSalesBags"))

# Projections
cur_day      = int(graw(proj, "currentDay", 1))
days_in_mo   = int(graw(proj, "daysInMonth", 30))
velocity     = num(gstr(proj, "velocityFactor"))
total_target = num(gstr(proj, "totalTarget"))
bare_min     = num(gstr(proj, "bareMinimum"))
declined_by  = num(gstr(proj, "declinedBy"))
std_proj     = gstr(proj, "standardProjection")
fc_proj      = gstr(proj, "forecastedProjection")

# New products
np_count   = int(graw(np_, "productCount"))
np_target  = num(gstr(np_, "totalTarget"))
np_sales   = num(gstr(np_, "totalSales"))
np_pct     = num(gstr(np_, "salesPct"))
np_deficit = num(gstr(np_, "totalDeficit"))
np_rows    = garr(np_, "monthlyCombined")

# Offer types
month_name  = gstr(oa, "monthName", "Current")
combo_count = int(graw(oa, "comboCount"))
pd_count    = int(graw(oa, "powerDealCount"))
ke_stock    = num(gstr(oa, "totalKenyaStock"))
ug_stock    = num(gstr(oa, "totalUgandaStock"))
sz_stock    = num(gstr(oa, "totalSinzaStock"))

# Posting
ke_wk_mkt   = num(gstr(pa, "wkMktPct"))
ke_mo_mkt   = num(gstr(pa, "moMktPct"))
ke_wk_posts = int(graw(pa, "s3WkPosts"))
posted      = num(gstr(pa, "s3Posted"))
not_posted  = num(gstr(pa, "s3NotPosted"))
sz_wk_mkt   = num(gstr(pa, "szWkMktPct"))
sz_mo_mkt   = num(gstr(pa, "szMoMktPct"))
sz_wk_posts = int(graw(pa, "szWkPosts"))
ug_wk_mkt   = num(gstr(pa, "ugWkMktPct"))
ug_mo_mkt   = num(gstr(pa, "ugMoMktPct"))
ug_wk_posts = int(graw(pa, "ugWkPosts"))

# ── DERIVED METRICS ───────────────────────────────────────────

pace_pct     = (cur_day / days_in_mo * 100) if days_in_mo else 0
distorted    = velocity > 10
stock_total  = posted + not_posted
invisible_pct = (not_posted / stock_total * 100) if stock_total else 0
recoverable  = not_posted * ke_wk_mkt / 100          # daydream metric
gap          = abs(declined_by)

top_products = []
if np_rows:
    agg = {}
    for r in np_rows:
        bt = r.get("bagType", "?")
        a = agg.setdefault(bt, {"kenya": 0, "outside": 0, "stock": 0})
        a["kenya"]   += r.get("kenyaSales", 0)
        a["outside"] += r.get("outsideKenya", 0)
        a["stock"]   += r.get("sKenya", 0)
    top_products = sorted(
        ({"name": k, "total": v["kenya"] + v["outside"], **v} for k, v in agg.items()),
        key=lambda x: -x["total"])[:5]

# ── BUILD INSIGHT CARDS ───────────────────────────────────────

good, attention, actions = [], [], []

def card(title, body, tag, tag_cls):
    return (f'<div class="insight-card"><h3><span class="tag {tag_cls}">{tag}</span> '
            f'{esc(title)}</h3><p>{body}</p></div>')

# Sales pace
if sales_pct >= pace_pct:
    good.append(card("Sales Ahead of Calendar Pace",
        f'<span class="number">{sales_pct:.2f}%</span> of target achieved by day '
        f'<span class="number">{cur_day}</span> of {days_in_mo} '
        f'(calendar pace: {pace_pct:.1f}%). <span class="number">{fmt(sales)}</span> bags sold, '
        f'<span class="number">{fmt(remaining)}</span> to go.', "On Pace", "tag-green"))
else:
    attention.append(card(f"Sales Behind Pace — {sales_pct:.2f}% vs {pace_pct:.1f}% Expected",
        f'<span class="number">{fmt(sales)}</span> bags sold; the calendar says '
        f'{pace_pct:.1f}% of target should be done by day {cur_day}. '
        f'<span class="number">{fmt(remaining)}</span> bags still needed.', "Behind", "tag-amber"))
    actions.append(f"<strong>Close the pace gap.</strong> Sales are at {sales_pct:.2f}% vs a "
                   f"calendar pace of {pace_pct:.1f}%. The remaining {fmt(remaining)} bags require "
                   f"~{fmt(remaining / max(days_in_mo - cur_day, 1))} bags/day for the rest of the month.")

# WoW
if wow_pct < 0:
    sev = ("tag-red", "Critical") if wow_pct < -20 else ("tag-amber", "Watch")
    attention.append(card(f"Weekly Sales Declined {abs(wow_pct):.1f}% Week-over-Week",
        f'Last week: <span class="number">{fmt(weekly_sales)}</span> bags vs '
        f'<span class="number">{fmt(prev_bags)}</span> prior — a drop of '
        f'<span class="number">{fmt(abs(wow_bags))}</span> bags.', sev[1], sev[0]))
    actions.append(f"<strong>Reverse the {abs(wow_pct):.0f}% WoW decline.</strong> Identify whether "
                   f"the drop came from posting volume, stock availability, or offer activity.")
else:
    good.append(card(f"Weekly Sales Growing +{wow_pct:.1f}% WoW",
        f'<span class="number">{fmt(weekly_sales)}</span> bags last week vs '
        f'<span class="number">{fmt(prev_bags)}</span> prior.', "Growing", "tag-green"))

# Bare minimum
if bare_min and declined_by < 0:
    attention.append(card(f"Weekly Bare Minimum Missed by {fmt(gap)} Bags",
        f'Weekly sales <span class="number">{fmt(weekly_sales)}</span> vs bare minimum '
        f'<span class="number">{fmt(bare_min)}</span>. '
        f'Recoverable via posting: <span class="number">{fmt(recoverable)}</span> bags '
        f'(unposted stock × Kenya {ke_wk_mkt:.1f}% conversion) — '
        f'{"<strong>enough to close the gap</strong>" if recoverable >= gap else "not enough alone"}.',
        "Critical", "tag-red"))
    actions.append(f"<strong>Post unposted stock to close the bare-minimum gap.</strong> "
                   f"{fmt(not_posted)} unposted bags × {ke_wk_mkt:.1f}% conversion ≈ "
                   f"{fmt(recoverable)} recoverable bags vs the {fmt(gap)}-bag shortfall.")

# Unposted stock
if not_posted > posted:
    attention.append(card(f"{fmt(not_posted)} Bags In Stock Are Not Posted — "
                          f"{invisible_pct:.0f}% of Stock Invisible",
        f'Only <span class="number">{fmt(posted)}</span> bags are posted and visible to buyers. '
        f'At Kenya\'s {ke_wk_mkt:.1f}% weekly conversion, posting the rest is worth roughly '
        f'<span class="number">{fmt(recoverable)}</span> additional sales.', "Critical", "tag-red"))

# Regional posting rates
for region, wk, mo, posts in [("Kenya", ke_wk_mkt, ke_mo_mkt, ke_wk_posts),
                              ("Sinza", sz_wk_mkt, sz_mo_mkt, sz_wk_posts),
                              ("Uganda", ug_wk_mkt, ug_mo_mkt, ug_wk_posts)]:
    if wk >= 40:
        good.append(card(f"{region} Marketing Conversion Above Target",
            f'<span class="number">{wk:.1f}%</span> of weekly {region} sales came from posted bags '
            f'(monthly: <span class="number">{mo:.1f}%</span>) — above the 40% benchmark. '
            f'Posts last week: <span class="number">{posts}</span>.', "Strong", "tag-green"))
    elif wk < 25:
        attention.append(card(f"{region} Marketing Conversion at {wk:.1f}% — Below Critical Threshold",
            f'Only <span class="number">{wk:.1f}%</span> of weekly {region} sales came from posts '
            f'(benchmark: 40%). Posts made: <span class="number">{posts}</span>. '
            f'Monthly rate: <span class="number">{mo:.1f}%</span>.', "Critical", "tag-red"))
        actions.append(f"<strong>{region} needs a posting intervention.</strong> Weekly conversion "
                       f"is {wk:.1f}% vs the 40% benchmark with only {posts} posts made.")
    else:
        attention.append(card(f"{region} Posting Rate Below Benchmark",
            f'Weekly marketing rate <span class="number">{wk:.1f}%</span> vs 40% target; '
            f'monthly <span class="number">{mo:.1f}%</span>. Posts: <span class="number">{posts}</span>.',
            "Watch", "tag-amber"))

# New products
if np_pct >= 50:
    good.append(card(f"New Products at {np_pct:.1f}% of Target",
        f'<span class="number">{fmt(np_sales)}</span> of <span class="number">{fmt(np_target)}</span> '
        f'bags across <span class="number">{np_count}</span> new products.', "Strong", "tag-green"))
else:
    attention.append(card(f"New Products at {np_pct:.1f}% of Target",
        f'<span class="number">{fmt(np_sales)}</span> of <span class="number">{fmt(np_target)}</span> '
        f'target — deficit of <span class="number">{fmt(np_deficit)}</span> bags across '
        f'{np_count} products.', "Watch", "tag-amber"))
    if top_products:
        leaders = ", ".join(esc(p["name"]) for p in top_products[:3])
        actions.append(f"<strong>Push the new-product leaders.</strong> {leaders} are the top sellers — "
                       f"concentrate posts on them to close the {fmt(np_deficit)}-bag deficit.")

if distorted:
    actions.append(f"<strong>Ignore projection percentages until day 5+.</strong> The "
                   f"{velocity:.1f}x velocity factor makes Standard ({std_proj}) and Forecasted "
                   f"({fc_proj}) projections unreliable this early in the month.")

# ── RENDER HTML ───────────────────────────────────────────────

def region_card(name, colour, wk, mo, posts, stock, bar_colour):
    return f'''
    <div class="region-card">
      <div class="region-name" style="color:{colour}">{name}</div>
      <div class="region-metric"><span>Weekly posts</span><strong style="color:{colour}">{posts}</strong></div>
      <div class="region-metric"><span>Weekly mkt %</span><strong style="color:{colour}">{wk:.1f}%</strong></div>
      <div class="region-metric"><span>Monthly mkt %</span><strong style="color:{colour}">{mo:.1f}%</strong></div>
      <div class="region-metric"><span>Stock</span><strong class="muted">{fmt(stock)}</strong></div>
      <div class="bar-wrap"><div class="bar-track"><div class="bar-fill" style="width:{min(wk,100):.1f}%;background:{bar_colour}"></div></div></div>
    </div>'''

distortion_html = ""
if distorted:
    distortion_html = f'''
  <div class="distortion-banner">
    <div class="icon">&#9888;&#65039;</div>
    <div>
      <h3>Projection Data Unreliable (Early-Month Artifact)</h3>
      <p>Day {cur_day} of {days_in_mo} &mdash; the velocity factor is <strong style="color:#fbbf24">{velocity:.2f}x</strong>,
      so Standard ({esc(std_proj)}) and Forecasted ({esc(fc_proj)}) projections are early-month artifacts.
      Disregard until at least day 5&ndash;7.</p>
    </div>
  </div>'''

top_rows = "".join(
    f'<tr><td class="rank">{i+1}</td><td>{esc(p["name"].title())}</td>'
    f'<td>{p["kenya"]}</td><td>{p["outside"]}</td><td>{p["stock"]}</td>'
    f'<td><strong class="green">{p["total"]}</strong></td></tr>'
    for i, p in enumerate(top_products))

top_table_html = f'''
  <div class="section-title">Top {len(top_products)} New Products by Monthly Sales</div>
  <div class="insight-card" style="padding:0.75rem 0;">
    <table class="top-products">
      <thead><tr><th>#</th><th>Product</th><th>Kenya</th><th>Outside</th><th>Stock</th><th>Total</th></tr></thead>
      <tbody>{top_rows}</tbody>
    </table>
  </div>''' if top_products else ""

actions_html = "".join(f"<li><div>{a}</div></li>" for a in actions)
today = date.today()

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Marketing Dashboard Insights &mdash; {month_name} {today.year}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ overflow-y: scroll; }}
    ::-webkit-scrollbar {{ width: 12px; height: 12px; }}
    ::-webkit-scrollbar-track {{ background: #0f1117; }}
    ::-webkit-scrollbar-thumb {{ background: #2d3148; border-radius: 6px; border: 3px solid #0f1117; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #3d4a5c; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; line-height: 1.6; padding: 2rem; }}
    .container {{ max-width: 900px; margin: 0 auto; }}
    .page-header {{ margin-bottom: 2rem; }}
    .page-header h1 {{ font-size: 1.6rem; font-weight: 800; color: #f8fafc; }}
    .page-header p {{ font-size: 0.8rem; color: #64748b; margin-top: 0.3rem; }}
    .section-title {{ font-size: 0.62rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #475569; margin: 2rem 0 0.75rem; }}
    .kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 0.75rem; margin-bottom: 0.5rem; }}
    .kpi {{ background: #1e2130; border: 1px solid #2d3148; border-radius: 10px; padding: 1rem 1.1rem; }}
    .kpi-label {{ font-size: 0.62rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #64748b; margin-bottom: 0.4rem; }}
    .kpi-value {{ font-size: 1.7rem; font-weight: 800; line-height: 1; font-variant-numeric: tabular-nums; }}
    .kpi-sub {{ font-size: 0.72rem; color: #64748b; margin-top: 0.3rem; }}
    .green {{ color: #34d399; }} .amber {{ color: #fbbf24; }} .red {{ color: #f87171; }}
    .cyan {{ color: #22d3ee; }} .muted {{ color: #94a3b8; }}
    .insight-card {{ background: #1e2130; border: 1px solid #2d3148; border-radius: 10px; padding: 1.1rem 1.25rem; margin-bottom: 0.75rem; }}
    .insight-card h3 {{ font-size: 0.84rem; font-weight: 700; color: #f8fafc; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; }}
    .insight-card p {{ font-size: 0.8rem; color: #94a3b8; line-height: 1.6; }}
    .insight-card .number {{ color: #f8fafc; font-weight: 700; }}
    .tag {{ font-size: 0.58rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; padding: 0.15rem 0.5rem; border-radius: 4px; }}
    .tag-red {{ background: rgba(239,68,68,0.2); color: #fca5a5; }}
    .tag-green {{ background: rgba(16,185,129,0.2); color: #6ee7b7; }}
    .tag-amber {{ background: rgba(245,158,11,0.2); color: #fcd34d; }}
    .region-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 0.75rem; }}
    .region-card {{ background: #1e2130; border: 1px solid #2d3148; border-radius: 10px; padding: 1rem; }}
    .region-name {{ font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.5rem; }}
    .region-metric {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem; }}
    .region-metric span {{ font-size: 0.75rem; color: #64748b; }}
    .region-metric strong {{ font-size: 0.82rem; font-weight: 700; }}
    .bar-wrap {{ margin: 0.4rem 0 0.2rem; }}
    .bar-track {{ height: 5px; background: #2d3148; border-radius: 3px; overflow: hidden; }}
    .bar-fill {{ height: 100%; border-radius: 3px; }}
    .actions-list {{ list-style: none; counter-reset: act; }}
    .actions-list li {{ counter-increment: act; display: flex; gap: 0.75rem; align-items: flex-start; padding: 0.7rem 0; border-bottom: 1px solid #2d3148; font-size: 0.8rem; color: #94a3b8; }}
    .actions-list li:last-child {{ border-bottom: none; }}
    .actions-list li::before {{ content: counter(act); background: #10b981; color: #022c22; font-size: 0.65rem; font-weight: 800; width: 18px; height: 18px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px; }}
    .actions-list li strong {{ color: #f8fafc; }}
    .top-products {{ width: 100%; border-collapse: collapse; font-size: 0.78rem; }}
    .top-products th {{ text-align: left; font-size: 0.6rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #475569; padding: 0.4rem 0.75rem; border-bottom: 1px solid #2d3148; }}
    .top-products td {{ padding: 0.5rem 0.75rem; border-bottom: 1px solid #1a1e2e; color: #cbd5e1; }}
    .top-products tr:last-child td {{ border-bottom: none; }}
    .rank {{ color: #475569; font-weight: 700; }}
    .distortion-banner {{ background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.3); border-radius: 10px; padding: 0.9rem 1.1rem; margin-bottom: 1.5rem; display: flex; gap: 0.75rem; align-items: flex-start; }}
    .distortion-banner .icon {{ font-size: 1.2rem; flex-shrink: 0; }}
    .distortion-banner h3 {{ font-size: 0.84rem; font-weight: 700; color: #fbbf24; margin-bottom: 0.3rem; }}
    .distortion-banner p {{ font-size: 0.78rem; color: #b45309; }}
  </style>
</head>
<body>
<div class="container">

  <div class="page-header">
    <h1>Marketing Dashboard Insights</h1>
    <p>Auto-generated from live dashboard data &bull; Day {cur_day} of {month_name} {today.year} &bull; Generated {today.strftime("%d %b %Y")} &bull; Denri Africa</p>
  </div>
{distortion_html}
  <div class="section-title">Headline Numbers</div>
  <div class="kpi-grid">
    <div class="kpi"><div class="kpi-label">Monthly Sales</div>
      <div class="kpi-value {'green' if sales_pct >= pace_pct else 'amber'}">{fmt(sales)}</div>
      <div class="kpi-sub">{sales_pct:.2f}% of {fmt(total_target)} target</div></div>
    <div class="kpi"><div class="kpi-label">Bags Still Needed</div>
      <div class="kpi-value red">{fmt(remaining)}</div>
      <div class="kpi-sub">to hit monthly target</div></div>
    <div class="kpi"><div class="kpi-label">Last Week Sales</div>
      <div class="kpi-value muted">{fmt(weekly_sales)}</div>
      <div class="kpi-sub">WoW {wow_pct:+.1f}%</div></div>
    <div class="kpi"><div class="kpi-label">Bare Minimum</div>
      <div class="kpi-value amber">{fmt(bare_min)}</div>
      <div class="kpi-sub">weekly floor{f" &bull; missed by {fmt(gap)}" if declined_by < 0 else ""}</div></div>
    <div class="kpi"><div class="kpi-label">Kenya Post Rate</div>
      <div class="kpi-value {'green' if ke_wk_mkt >= 40 else 'red'}">{ke_wk_mkt:.1f}%</div>
      <div class="kpi-sub">weekly sales from posts</div></div>
    <div class="kpi"><div class="kpi-label">New Products</div>
      <div class="kpi-value cyan">{np_pct:.1f}%</div>
      <div class="kpi-sub">{fmt(np_sales)} of {fmt(np_target)} target</div></div>
  </div>

  <div class="section-title">What&rsquo;s Going Well</div>
  {"".join(good) if good else '<div class="insight-card"><p>No green signals this period.</p></div>'}

  <div class="section-title">What Needs Attention</div>
  {"".join(attention) if attention else '<div class="insight-card"><p>Nothing critical detected.</p></div>'}

  <div class="section-title">Regional Posting Comparison</div>
  <div class="region-grid">
    {region_card("Kenya",  "#34d399", ke_wk_mkt, ke_mo_mkt, ke_wk_posts, ke_stock, "#10b981")}
    {region_card("Sinza",  "#a78bfa", sz_wk_mkt, sz_mo_mkt, sz_wk_posts, sz_stock, "#a78bfa")}
    {region_card("Uganda", "#fbbf24", ug_wk_mkt, ug_mo_mkt, ug_wk_posts, ug_stock, "#f59e0b")}
  </div>
{top_table_html}
  <div class="section-title">Recommended Actions &mdash; This Week</div>
  <div class="insight-card">
    <ul class="actions-list">{actions_html if actions_html else "<li><div>No actions triggered — all metrics within thresholds.</div></li>"}</ul>
  </div>

</div>
</body>
</html>
'''

out_path = os.path.join(BASE_DIR, "insights.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"  Sales           : {fmt(sales)} ({sales_pct:.2f}% of target, pace {pace_pct:.1f}%)")
print(f"  Weekly          : {fmt(weekly_sales)} (WoW {wow_pct:+.1f}%)")
print(f"  Unposted stock  : {fmt(not_posted)} ({invisible_pct:.0f}% invisible)")
print(f"  Good signals    : {len(good)}   Attention: {len(attention)}   Actions: {len(actions)}")
print("insights.html updated.")
