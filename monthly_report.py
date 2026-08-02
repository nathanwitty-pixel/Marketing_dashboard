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
np_count   = int(num(gstr(np_, "productCount")))
np_target  = num(gstr(np_, "totalTarget"))
np_sales   = num(gstr(np_, "totalSales"))
np_pct     = (np_sales / np_target * 100) if np_target else 0
np_deficit = max(np_target - np_sales, 0)
np_kenya   = num(gstr(np_, "monthlyKenya"))
np_outside = num(gstr(np_, "monthlyOutside"))
np_posts   = num(gstr(np_, "mpostKenya")) + num(gstr(np_, "mpostOutside"))
np_names   = garr(np_, "productNames")

# Offer type analysis
combos    = int(num(gstr(oa, "comboCount")))
deals     = int(num(gstr(oa, "powerDealCount")))
ke_stock  = num(gstr(oa, "totalKenyaStock"))
sz_stock  = num(gstr(oa, "totalSinzaStock"))
ug_stock  = num(gstr(oa, "totalUgandaStock"))

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
mo_posts_made = num(gstr(pa, "monthlyPostsMade"))

# Per-bag "which bags were never posted" (in stock, no marketing posts).
unmarketed_bags = garr(pa, "instockNotPosted")
unm_sorted = sorted(unmarketed_bags, key=lambda b: num(b.get("stock")), reverse=True)[:10]

# Weakest region by monthly sales-achieved
regions = [("Kenya", ke_mo_mkt), ("Sinza", sz_mo_mkt), ("Uganda", ug_mo_mkt)]
weak_name, weak_val = min(regions, key=lambda r: r[1])

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
</style>
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
  </div>

  <div class="sec">
    <div class="sec-head"><div class="sec-num" style="background:#22d3ee">2</div><h2>New Products</h2></div>
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
    <div class="row"><div class="tag bottom">The Bottom Line</div>
      <p>Across <b>{combos} combos and {deals} power deals</b>, we are holding heavy inventory — <b>{fmt(ke_stock)} bags in Kenya</b> (plus {fmt(sz_stock)} Sinza, {fmt(ug_stock)} Uganda) — that is clearing too slowly to hit target.</p></div>
    <div class="row"><div class="tag insight">The Insight</div>
      <p>The offer mix isn't drawing down stock fast enough: the same <b>{fmt(ke_stock)}-bag Kenya position</b> here is the stock behind the marketing gap in Section 4. Inventory is concentrated in a handful of colours/combos rather than spread across movers.</p></div>
    <div class="row"><div class="tag rec">Recommendation</div>
      <div class="recs">
        <div class="rec-item"><span class="badge start">Start</span><span>Leading each week's offers with the <b>highest-stock combos</b> so pushes are aimed at what we most need to clear.</span></div>
        <div class="rec-item"><span class="badge stop">Stop</span><span>Restocking the <b>slowest-moving colours</b> until the current position draws down.</span></div>
      </div></div>
    <div class="row"><div class="tag impact">Business Impact</div>
      <div class="impact"><p>Clearing just <b>20% of the {fmt(ke_stock)}-bag Kenya position (~{fmt(offer_clear)} bags)</b> in the month is ~{pct(offer_clear_pct)} of target — and frees working capital tied up in slow stock.</p></div>
      <div class="assump">Assumes a 20% draw-down of the reported Kenya offer stock; excludes Sinza/Uganda upside.</div></div>
  </div>

  <div class="sec">
    <div class="sec-head"><div class="sec-num" style="background:#34d399">4</div><h2>Posting Yields (Sales from Accurate Posting)</h2></div>
    <div class="row"><div class="tag bottom">The Bottom Line</div>
      <p>Marketing posting is our most effective lever — Kenya posted bags hit <b>{pct(ke_mo_mkt)} of expected sales monthly</b> — but <b>{pct(unposted_pct)} of in-stock bags ({fmt(notposted)}) were never posted</b>. The target gap is sitting in unmarketed stock.</p></div>
    {unm_block}
    <div class="row"><div class="tag insight">The Insight</div>
      <p>Where we post, we sell: monthly sales on posted bags ({fmt(mo_sales_posting)}) ran <b>~{posting_mult:.1f}× the {fmt(mo_expect_posting)} expected</b>. Yet only <b>{fmt(posted)} bags were on offer/posted vs {fmt(notposted)} not</b>. Regionally the discipline collapses — Kenya {pct(ke_mo_mkt)}, <b>Sinza {pct(sz_mo_mkt)}, Uganda {pct(ug_mo_mkt)}</b> — so the biggest untapped demand is in <b>{weak_name}</b> and in unmarketed stock.</p></div>
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
</body>
</html>
"""

out = os.path.join(BASE, "monthly_report.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(head + body)

# Keep a dated archive so past months are never overwritten.
archive = os.path.join(BASE, f"report_{year}_{month.lower()}.html")
with open(archive, "w", encoding="utf-8") as f:
    f.write(head + body)

print(f"monthly_report.html built for {month} {year}.")
print(f"  Target achieved : {pct(achieved)}  ({fmt(total_sales)}/{fmt(total_target)})")
print(f"  Missed by       : {fmt(gap)} bags")
print(f"  Unposted stock  : {fmt(notposted)} ({pct(unposted_pct)})")
print(f"  Weakest region  : {weak_name} ({pct(weak_val)})")
print(f"  Archive         : report_{year}_{month.lower()}.html")
