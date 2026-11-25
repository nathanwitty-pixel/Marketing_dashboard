"""
weekly_report.py — the weekly marketing report as slides (Headline / Graph / Insight / Biz Rec).
Spec: docs/weekly-report.md

Reads the built current_performance.html (PERF / PROJ) so the month figures match that page, and Odoo for the
daily till bags, Kenya's Meta account sync, WhatsApp chats and footfall. Writes WR into weekly_report.html.
"""
import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root → lib/
import pandas as pd  # noqa: E402

from lib import paths  # noqa: E402

LINK = 0.3            # match score at or above this = follows and sales move together
CHECK_WEEKS = 12      # history needed before the follows answer is trusted
NOT_KENYA = ("sinza", "dar-es-alam", "uganda")

today = dt.date.today()
from lib import report_period  # noqa: E402
report_period.from_argv()
P = report_period.load(today)          # the Period dropdown's choice (default Last Week); docs › Period picker
report_period.set_active(P)
week_start, week_end = P.start, P.end  # the report's days (named week_* from when it was weekly only)
cmp_start, cmp_end = P.cs, P.ce        # the days they are compared with


def n(x):
    """'13,251' / '39.78%' / 13251 → float, None if blank."""
    if x is None or x == "":
        return None
    try:
        return float(str(x).replace(",", "").replace("%", "").replace("KES", "").strip())
    except ValueError:
        return None


def fmt(x):
    return f"{round(x):,}" if x is not None else "—"


def pct(a, b):
    return (a - b) / b * 100 if b else None


def signed(p, dp=0):
    return "—" if p is None else f"{'+' if p >= 0 else ''}{p:.{dp}f}%"


def day_label(d):
    return f"{d:%a} {d.day} {d:%b}"


# ── the Current Performance page's figures ────────────────────────────────────
cp_html = open(paths.html("current_performance.html"), encoding="utf-8").read()


def field(name):
    """A one-line value from PERF / PROJ (`  name:   <json>,`); the first match (PERF before PROJ)."""
    m = re.search(r"^\s*" + re.escape(name) + r":\s*(.+?),?\s*$", cp_html, re.M)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def proj_field(name):
    """Same as field() but from the PROJ block only."""
    i = cp_html.find("<!-- PROJ_DATA_START -->")
    m = re.search(r"^\s*" + re.escape(name) + r":\s*(.+?),?\s*$", cp_html[i:], re.M)
    try:
        return json.loads(m.group(1)) if m else None
    except ValueError:
        return None


beats = proj_field("beats") or {}
corp_beat = field("corporateBeat") or {}
history = proj_field("weeklyHistory") or []
days_in_month = proj_field("daysInMonth") or 30
current_day = proj_field("currentDay") or today.day
target = n(proj_field("totalTarget"))
sales = n(field("sales"))
sales_pos = n(field("salesPos"))
corp_bags = n(field("corporateBags"))
sales_pct = n(field("salesPctAchieved"))
month_name = proj_field("projMonth") or f"{today:%B}"
rev_fc = n(proj_field("forecastedRevenue"))
rev_fc_pct = n(proj_field("forecastedRevenuePct"))
rev_target = n(proj_field("revenueTarget"))
pace = proj_field("pace") or {}


def kes_m(x):
    """KES 36,769,357 → 'KES 36.8M'."""
    return "—" if x is None else (f"KES {x / 1e6:.1f}M" if x >= 1e6 else f"KES {round(x):,}")


# headline: bags and revenue together (docs/weekly-report.md › Slide 1)
summary = beats.get("summary") or {}
proj_bags = n(proj_field("forecastedProjection"))
headline1 = summary.get("headline", "")
m = re.match(r"(.*?on course for about [\d,]+ bags), ([\d.]+% of the [\d,]+ target)\.?$", headline1)
if m and rev_fc is not None and rev_target:
    headline1 = (f"{m.group(1)} ({m.group(2)}) and {kes_m(rev_fc)} "
                 f"({rev_fc_pct:.0f}% of the {kes_m(rev_target)} revenue target).")
tone1 = "bad" if (proj_bags is not None and proj_bags < 90) or (rev_fc_pct is not None and rev_fc_pct < 90) \
    else summary.get("tone", "neutral")

# ── Odoo ──────────────────────────────────────────────────────────────────────
db_ok = True
try:
    from lib import db, queries, footfall, odoo_marketing, foot_traffic
except Exception as e:                                       # noqa: BLE001
    print(f"  WARNING: Odoo helpers unavailable: {e}")
    db_ok = False


def daily_bags(s, e):
    """{date: {'all': bags, 'ke': Kenya bags}} from bags_sold_daily.sql split by shop."""
    sql = (queries.BAGS_SOLD_DAILY
           .replace("p.date_order::date AS day,", "p.date_order::date AS day, lower(pc.\"name\") AS shop,", 1)
           .replace("GROUP BY 1\n", "GROUP BY 1, 2\n", 1))
    df = db.run_query(sql, {"start_date": s.isoformat(), "end_date": e.isoformat(),
                            "excluded": queries.excluded_products()})
    if df is None:
        return None
    out = {}
    for _, r in df.iterrows():
        d = out.setdefault(r["day"], {"all": 0.0, "ke": 0.0, "tz": 0.0, "ug": 0.0})
        b = float(r["bags"] or 0)
        shop = r["shop"] or ""
        d["all"] += b
        d["ug" if shop == "uganda" else "tz" if shop in NOT_KENYA else "ke"] += b
    return out


# ── WhatsApp buyers by source (docs/weekly-report.md › WhatsApp buyers by source) ──
SRC_LABEL = {"Existing Direct": "Returning customers", "New Direct": "New customers",
             "Social DMs": "Social pages (follower path)", "Direct IG": "Social pages (follower path)",
             "Meta Ad - Facebook": "Facebook ads", "Meta Ad - Instagram": "Instagram ads", "Meta Ad - Twitter": "X ads",
             "Status Ads": "WhatsApp Status ads", "Web Check Out": "Website checkout", "Walk-in": "Walk-in",
             "Shop Transfer": "Shop transfer"}
FOLLOWER_PATH = "Social pages (follower path)"
SRC_REC = {
    "Returning customers": "Re-contact returning customers: {n} fewer bought through direct chats. Send last month's buyers "
                           "a broadcast with new arrivals and the current offers.",
    "New customers": "Check how first-time chats are answered and followed up: {n} fewer new customers bought.",
    FOLLOWER_PATH: "Answer Instagram and Facebook page DMs faster and point posts to WhatsApp: {n} fewer bought from the pages.",
}


def wa_sources(market, s, e):
    """{label: [chats, bought]} for one market's shops (KE = all but Sinza and Uganda) between s and e."""
    where = {"KE": "lower(sh.name) NOT IN ('sinza', 'uganda')", "TZ": "lower(sh.name) = 'sinza'",
             "UG": "lower(sh.name) = 'uganda'"}[market]
    df = db.run_query(f"""
        SELECT src.name AS src, COUNT(*) AS chats, SUM(CASE WHEN i.is_purchased THEN 1 ELSE 0 END) AS bought
        FROM denri_monitor_interaction i
        JOIN denri_monitor_source src ON src.id = i.source_id
        JOIN denri_monitor_shop sh ON sh.id = i.shop_id
        WHERE i.date BETWEEN :s AND :e AND {where}
        GROUP BY 1""", {"s": s.isoformat(), "e": e.isoformat()})
    out = {}
    for _, r in (df.iterrows() if df is not None else []):
        k = SRC_LABEL.get(r["src"], r["src"])
        v = out.setdefault(k, [0, 0])
        v[0] += int(r["chats"] or 0)
        v[1] += int(r["bought"] or 0)
    return out


def src_words(market_name, label):
    """'Sinza's returning customers' / 'Sinza's buyers from Instagram ads' — a source said as words."""
    lab = label.split(" (")[0]
    keep = lab.split(" ")[0] in ("Instagram", "Facebook", "Website", "TikTok")
    lab = lab if keep else lab[0].lower() + lab[1:]
    return f"{market_name}'s {lab}" if lab.endswith("customers") else f"{market_name}'s buyers from {lab}"


def month_weeks():
    """Sun-to-Sat weeks of the month, Week 1 from the 1st, the last one ending on the report week's Saturday."""
    s_, out = week_end.replace(day=1), []
    while s_ <= week_end:
        e_ = min(s_ + dt.timedelta(days=(5 - s_.weekday()) % 7), week_end)
        out.append((s_, e_))
        s_ = e_ + dt.timedelta(days=1)
    return out


def source_weeks(market):
    """(week labels, {source: [bought per week]}, {source: [chats, bought] last week}) for one market."""
    wks = month_weeks()
    per = [wa_sources(market, a_, b_) for a_, b_ in wks]
    labels = [f"Wk {i + 1} ({a_.day}–{b_.day} {b_:%b})" for i, (a_, b_) in enumerate(wks)]
    srcs = {}
    for i, d in enumerate(per):
        for k, (c, bt) in d.items():
            srcs.setdefault(k, [0] * len(per))[i] = bt
    return labels, srcs, per[-1] if per else {}


def source_change(market):
    """(rows [[label, chats, bought, bought before, change]], insight line, rec line or None) for the period."""
    cur = wa_sources(market, week_start, week_end)
    prev = wa_sources(market, cmp_start, cmp_end)
    labels = sorted(set(cur) | set(prev), key=lambda k: (-cur.get(k, [0, 0])[1], -cur.get(k, [0, 0])[0]))
    rows = [[k, cur.get(k, [0, 0])[0], cur.get(k, [0, 0])[1], prev.get(k, [0, 0])[1],
             cur.get(k, [0, 0])[1] - prev.get(k, [0, 0])[1]] for k in labels if cur.get(k) or prev.get(k)]
    total = sum(r[2] for r in rows)
    fp = next((r for r in rows if r[0] == FOLLOWER_PATH), None)
    big = max(rows, key=lambda r: abs(r[4])) if rows else None
    if fp:
        line = (f"Follower path: <b>{fmt(fp[2])}</b> buyers from page chats ({fp[2] / total * 100:.0f}% of WhatsApp buyers, "
                f"{'+' if fp[4] >= 0 else ''}{fp[4]}).")
    else:
        line = "Follower path: <b>0</b> buyers from page chats."
    if big and big[4]:
        line += (" " if line else "") + (f"Biggest change: {big[0].split(' (')[0].lower()} "
                                         f"{fmt(big[3])} → {fmt(big[2])}.")
    worst = min(rows, key=lambda r: r[4]) if rows else None
    rec = None
    if worst and worst[4] <= -5:
        tmpl = SRC_REC.get(worst[0])
        rec = (tmpl.format(n=fmt(-worst[4])) if tmpl else
               f"Check the {worst[0]} budget and creatives: {fmt(-worst[4])} fewer buyers came from them {P.when} than {P.prev}."
               if "ads" in worst[0] else f"Check {worst[0].lower()}: {fmt(-worst[4])} fewer buyers {P.when} than {P.prev}.")
    return rows, line, rec


# ── Slide 1: Sales this month ─────────────────────────────────────────────────
month_start = today.replace(day=1) if today.day > 1 else (today - dt.timedelta(days=1)).replace(day=1)
prev_end = month_start - dt.timedelta(days=1)
prev_start = prev_end.replace(day=1)
last_done = min(today - dt.timedelta(days=1), month_start + dt.timedelta(days=days_in_month - 1))

slide1 = {"ok": False}
if db_ok:
    try:
        cur = daily_bags(month_start, last_done) or {}
        prv = daily_bags(prev_start, prev_end) or {}
        cum, run = [], 0.0
        for i in range(days_in_month):
            d = month_start + dt.timedelta(days=i)
            if d <= last_done:
                run += cur.get(d, {}).get("all", 0.0)
                cum.append(round(run))
            else:
                cum.append(None)
        pcum, run = [], 0.0
        for i in range((prev_end - prev_start).days + 1):
            run += prv.get(prev_start + dt.timedelta(days=i), {}).get("all", 0.0)
            pcum.append(round(run))
        done = (last_done - month_start).days + 1
        same_day_prev = pcum[min(done, len(pcum)) - 1] if pcum else None
        till_to_date = cum[done - 1] if done else 0
        # projection: last actual day → month end, Forward Projections' rest of month spread by weekday pattern
        proj = [None] * days_in_month
        rest, wd = pace.get("restBags"), pace.get("weekdays")
        if rest is not None and done and done < days_in_month:
            left = [month_start + dt.timedelta(days=i) for i in range(done, days_in_month)]
            w = [(wd[d.weekday()] if wd and len(wd) == 7 else 1) or 0 for d in left]
            tot = sum(w) or len(w)
            run = cum[done - 1]
            proj[done - 1] = run
            for i, x in enumerate(w):
                run += rest * x / tot
                proj[done + i] = round(run)
        slide1 = {"ok": True, "days": list(range(1, days_in_month + 1)), "cur": cum, "prev": pcum, "proj": proj,
                  "target": target, "done": done, "tillToDate": till_to_date, "samePrev": same_day_prev,
                  "prevLabel": f"{prev_start:%B}", "curLabel": month_name}
    except Exception as e:                                   # noqa: BLE001
        print(f"  WARNING: slide 1 graph skipped: {e}")

insight1 = []
if sales is not None and target:
    gone = round(current_day / days_in_month * 100)
    insight1.append(f"Denri has sold <b>{fmt(sales)}</b> bags so far ({fmt(sales_pos)} at the shop tills and {fmt(corp_bags)} corporate), "
                    f"<b>{field('salesPctAchieved')}</b> of the {fmt(target)} target, with {gone}% of the month gone.")
wk = next((w for w in history if w.get("weekStart") == week_start.isoformat()), None) if P.key == "last_week" else None
if wk:
    add = (wk.get("salesPct") or 0) - (wk.get("prevSalesPct") or 0)
    insight1.append(f"Last week ({day_label(week_start)} to {day_label(week_end)}) Denri sold <b>{fmt(wk.get('weeklySales'))}</b> bags "
                    f"and took the month from {wk.get('prevSalesPct'):.1f}% to {wk.get('salesPct'):.1f}% of target (+{add:.1f} points).")
elif db_ok:
    try:                                                     # any other period: the tills for the period vs the one before
        _pb = daily_bags(min(week_start, cmp_start), week_end) or {}
        _b1 = sum(v["all"] for d_, v in _pb.items() if week_start <= d_ <= week_end)
        _b0 = sum(v["all"] for d_, v in _pb.items() if cmp_start <= d_ <= cmp_end)
        _p = pct(_b1, _b0)
        insight1.append(f"{P.When} ({P.dates}) the shop tills sold <b>{fmt(_b1)}</b> bags, "
                        + ("the same as" if not _p else f"{abs(_p):.0f}% {'more' if _p > 0 else 'fewer'} than")
                        + f" {P.prev} ({P.prev_dates}: {fmt(_b0)}).")
    except Exception as e:                                   # noqa: BLE001
        print(f"  WARNING: period sales line skipped: {e}")
if slide1.get("ok") and slide1.get("samePrev"):
    d = pct(slide1["tillToDate"], slide1["samePrev"])
    same_day = (f"At the tills, {fmt(slide1['tillToDate'])} bags by day {slide1['done']} vs {fmt(slide1['samePrev'])} by the same day of "
                f"{slide1['prevLabel']} (<b>{signed(d)}</b>).")
    # better than last month, but the target rose more: say both so the team sees the improvement and the gap
    try:
        from lib import product_targets
        prev_t, _ = product_targets.total_for(prev_start)
    except Exception:                                        # noqa: BLE001
        prev_t = 0
    if not (prev_t and target and slide1.get("prev")):
        insight1.append(same_day)
    else:
        t_up = pct(target, prev_t)
        prev_full = next((v for v in reversed(slide1["prev"]) if v is not None), None)
        now_pct, then_pct = slide1["tillToDate"] / target * 100, slide1["samePrev"] / prev_t * 100
        slide1["prevTarget"] = prev_t
        insight1.append(f"<b>We improved, but the target rose more:</b> this month's target of {fmt(target)} is <b>{signed(t_up)}</b> on "
                        f"{slide1['prevLabel']}'s {fmt(prev_t)}, while the tills are up only <b>{signed(d)}</b> ({fmt(slide1['tillToDate'])} "
                        f"against {fmt(slide1['samePrev'])} by day {slide1['done']}). So we are at {now_pct:.0f}% of target, against "
                        f"{slide1['prevLabel']}'s {then_pct:.0f}% at this point; on {slide1['prevLabel']}'s target we would be at "
                        f"{slide1['tillToDate'] / prev_t * 100:.0f}%."
                        + (f" {slide1['prevLabel']} finished at {fmt(prev_full)} bags ({prev_full / prev_t * 100:.0f}% of its target)." if prev_full else ""))
so_far = pace.get("soFar") or {}
if so_far.get("kes") is not None and rev_target:
    rev_now = (so_far.get("kes") or 0) + (so_far.get("corpKes") or 0)
    price = (beats.get("price") or {}).get("headline", "")
    insight1.append(f"Revenue so far is <b>{kes_m(rev_now)}</b> ({rev_now / rev_target * 100:.1f}% of {kes_m(rev_target)}), "
                    f"heading for {kes_m(rev_fc)} by month end. {price}")
_cc = field("corporateClients") or []
_coll = sum(c.get("receivedKes") or 0 for c in _cc)
_owed = sum(max((c.get("agreedKes") or 0) - (c.get("receivedKes") or 0), 0) for c in _cc)
_sc = field("shopCorporate") or {}
_coll += sum(r.get("paidKes") or 0 for r in _sc.get("rows") or [])
_owed += sum(r.get("balance") or 0 for r in _sc.get("rows") or [])
if corp_beat.get("headline"):
    _ch = corp_beat["headline"].rstrip(".")
    _ch = ("On the corporate side, " + _ch[len("Corporate: "):]) if _ch.startswith("Corporate: ") else _ch
    insight1.append(_ch + (f"; Denri has collected {kes_m(_coll)} and is still owed <b>{kes_m(_owed)}</b>"
                           " (Corporate app and shops)." if _cc or _sc else "."))
rec1 = [r for r in (summary.get("rec"), (beats.get("projections") or {}).get("rec"), corp_beat.get("rec")) if r]

# ── Slide 2: Did new followers sell bags? (Kenya) ─────────────────────────────
slide2 = {"ok": False}
ft_daily = {}      # market → daily follows / chats / bags for the follower test
headline2, insight2, rec2 = "", [], []
if db_ok:
    try:
        fol = pd.DataFrame(odoo_marketing.followers_daily("KE"))
        fol["date"] = pd.to_datetime(fol["date"]).dt.date
        fol = fol[fol.platform.isin(["instagram", "facebook"])]
        piv = lambda k: fol.groupby(["date", "platform"])[k].sum(min_count=1).unstack()   # noqa: E731 — blank stays blank
        nf = piv("newFollows")
        both = nf.dropna()
        first = min(both.index)                              # first day both platforms report new follows
        s, e = min(first, cmp_start), week_end
        reach, views = piv("reach"), piv("views")
        bags = daily_bags(s, e) or {}
        wa = db.run_query("""
            SELECT i.date::date AS day, COUNT(*) AS chats
            FROM denri_monitor_interaction i JOIN denri_monitor_shop sh ON sh.id = i.shop_id
            WHERE i.date BETWEEN :s AND :e AND lower(sh.name) NOT IN ('sinza', 'uganda')
            GROUP BY 1""", {"s": s.isoformat(), "e": e.isoformat()})
        wa = {r["day"]: float(r["chats"]) for _, r in wa.iterrows()} if wa is not None else {}
        ff = footfall.daily(s, e)
        if not ff.empty:
            ff = ff[(ff.shop.map(footfall.MARKET) == "KENYA") & (ff.shop != footfall.HILTON)]
            vis = ff.groupby("day")["visitors"].sum(min_count=1).to_dict()
        else:
            vis = {}
        rows = []
        d = s
        while d <= e:
            rows.append({"day": d, "follows": nf.loc[d].sum() if d in nf.index else None,
                         "ig": nf.loc[d].get("instagram") if d in nf.index else None,
                         "fb": nf.loc[d].get("facebook") if d in nf.index else None,
                         "reach": reach.loc[d].get("instagram") if d in reach.index else None,
                         "views": views.loc[d].sum() if d in views.index else None,
                         "bags": bags.get(d, {}).get("ke", 0.0), "chats": wa.get(d), "visitors": vis.get(d)})
            d += dt.timedelta(days=1)
        df = pd.DataFrame(rows).set_index("day")
        df.index = pd.to_datetime(df.index)
        df = df.astype(float)
        ft_daily["KE"] = df[df.index >= pd.Timestamp(first)][["follows", "chats", "bags"]].copy()   # Meta days only

        # weekday-adjusted, same day, rank correlation
        adj = df.div(df.groupby(df.index.dayofweek).transform("mean"))
        def score(col):
            x = adj[[col, "bags"]].dropna()
            return round(float(x[col].corr(x["bags"], method="spearman")), 2) if len(x) >= 10 else None
        scores = {"follows": score("follows"), "chats": score("chats"), "visitors": score("visitors")}
        q = adj["follows"].quantile(0.75)
        top = adj["follows"] >= q
        top_same = (adj["bags"][top].mean() - 1) * 100
        top_next = (adj["bags"].shift(-1)[top].dropna().mean() - 1) * 100

        # Sun–Sat weeks with all 7 days on both platforms
        df["week"] = [ix.date() - dt.timedelta(days=(ix.weekday() + 1) % 7) for ix in df.index]
        weeks = []
        for w, g in df.groupby("week"):
            if len(g) == 7 and g["ig"].notna().all() and g["fb"].notna().all():
                weeks.append({"start": w.isoformat(), "label": f"{w.day} {w:%b}", "bags": round(g.bags.sum()),
                              "follows": round(g.follows.sum()), "ig": round(g.ig.sum()), "fb": round(g.fb.sum()),
                              "chats": round(g.chats.sum()) if g.chats.notna().any() else None,
                              "visitors": round(g.visitors.sum()) if g.visitors.notna().any() else None,
                              "reach": round(g.reach.sum()) if g.reach.notna().any() else None,
                              "views": round(g.views.sum()) if g.views.notna().any() else None})
        for w in weeks:                                      # chats as the band counts them (Foot Traffic's WhatsApp Monitor)
            try:
                ws_ = dt.date.fromisoformat(w["start"])
                w["chats"] = foot_traffic.summary(ws_, ws_ + dt.timedelta(days=6))["KE"]["whatsapp"]["chats"]
            except Exception:                                # noqa: BLE001
                pass
        n_days = len(df)
        slide2 = {"ok": len(weeks) >= 2, "weeks": weeks, "scores": scores, "days": n_days,
                  "from": s.isoformat(), "to": e.isoformat(),
                  "topSame": round(top_same, 1), "topNext": round(top_next, 1)}

        def per_(lo, hi):                                    # the period's (or comparison's) totals, like a week row
            g = df[(df.index.date >= lo) & (df.index.date <= hi)]
            sm = lambda c: round(g[c].sum()) if g[c].notna().any() else 0     # noqa: E731
            return {"bags": sm("bags"), "follows": sm("follows"), "ig": sm("ig"), "fb": sm("fb"), "chats": sm("chats")}
        if len(weeks) >= 2:
            a, b = per_(week_start, week_end), per_(cmp_start, cmp_end)
            pf, pb = pct(a["follows"], b["follows"]) or 0, pct(a["bags"], b["bags"])
            pig, pfb = pct(a["ig"], b["ig"]), pct(a["fb"], b["fb"])
            pc = pct(a["chats"], b["chats"]) if a["chats"] and b["chats"] else None
            up = lambda p: "rose" if p >= 0 else "fell"     # noqa: E731
            sf = scores["follows"]
            words = lambda v: ("no link" if v is None or v < 0.2 else "a weak link" if v < LINK      # noqa: E731
                               else "a clear link" if v < 0.6 else "a strong link")
            ready = first + dt.timedelta(weeks=CHECK_WEEKS)          # 12 weeks of follower history
            later = (f" Check again from {day_label(ready)} {ready.year} ({CHECK_WEEKS} weeks of history)."
                     if ready > week_end else "")
            # the band (Foot Traffic figures) for the period and the one before: one path from a follow to a sale
            try:
                ft1 = foot_traffic.summary(week_start, week_end)["KE"]
                ft0 = foot_traffic.summary(cmp_start, cmp_end)["KE"]
            except Exception as fe:                          # noqa: BLE001
                print(f"  WARNING: foot traffic for the insight skipped: {fe}")
                ft1 = ft0 = None
            if ft1 and ft0:
                w1, w0, c1, c0 = ft1["walkins"], ft0["walkins"], ft1["whatsapp"], ft0["whatsapp"]
                d_walk = w1["purchased"] - w0["purchased"]
                d_wa = c1["purchased"] - c0["purchased"]
                p1_ = lambda v: "—" if v is None else f"{v:.1f}%"     # noqa: E731 — no chats / walk-ins yet = blank
                gain = lambda dn, who: f"{who} {'gained' if dn >= 0 else 'lost'} {fmt(abs(dn))}"     # noqa: E731
                parts = [(abs(d_walk), gain(d_walk, "the shops") + " walk-in buyers"),
                         (abs(d_wa), gain(d_wa, "WhatsApp") + " buyers")]
                parts.sort(key=lambda t: -t[0])
                linked = sf is not None and sf >= LINK
                headline2 = (f"Kenya sold {fmt(a['bags'])} bags {P.when} ({signed(pb)}): {parts[0][1]} while {parts[1][1]}; "
                             + (f"new follows {up(pf or 0)} {abs(pf or 0):.0f}% on {P.prev}" if cmp_start >= first else
                                f"new follows reached {fmt(a['follows'])} (no fair comparison: follower data only starts on {day_label(first)})")
                             + (" and moved with sales." if linked else " and didn't move sales."))
                insight2.append(
                    f"<b>Online path</b>: {fmt(a['follows'])} new follows ({signed(pf)}) → {fmt(c1['chats'])} WhatsApp chats "
                    f"({signed(pct(c1['chats'], c0['chats']))}), {fmt(c1['ads'])} of them from ads → <b>{fmt(c1['purchased'])}</b> bought "
                    f"({p1_(c1['performance'])}, was {p1_(c0['performance'])}).")
                insight2.append(
                    f"<b>Shop path</b>: {fmt(w1['counted'])} walk-ins counted ({signed(pct(w1['counted'], w0['counted']))}) → "
                    f"<b>{fmt(w1['purchased'])}</b> bought ({p1_(w1['conversion'])}, was {p1_(w0['conversion'])}); "
                    f"{fmt(w1['didntBuy'])} left without buying.")
                sale = (w1["revPerWalkin"] or 0) * w1["counted"] / w1["purchased"] if w1["purchased"] else 0
                extra = round(w1["counted"] * 0.05)
                try:
                    src_rows, src_line, src_rec = source_change("KE")
                except Exception as se:                      # noqa: BLE001
                    print(f"  WARNING: WhatsApp sources skipped: {se}")
                    src_rows, src_line, src_rec = [], "", None
                if src_line:
                    insight2.append(src_line)
                if src_rows:
                    keep = src_rows[:4] + [r for r in src_rows[4:] if r[0] == FOLLOWER_PATH]
                    rest = [r for r in src_rows if r not in keep]
                    if rest:
                        keep.append(["Other"] + [sum(r[i] for r in rest) for i in (1, 2, 3, 4)])
                    try:
                        wl, sw, last = source_weeks("KE")
                        names = [r[0] for r in keep if r[0] != "Other"]
                        other = [k for k in sw if k not in names]
                        rows_k = []
                        for k in names + (["Other"] if other else []):
                            ks = [k] if k != "Other" else other
                            wk_b = [sum(sw.get(x, [0] * len(wl))[i] for x in ks) for i in range(len(wl))]
                            ch = sum(last.get(x, [0, 0])[0] for x in ks)
                            bt = sum(last.get(x, [0, 0])[1] for x in ks)
                            d_ = wk_b[-1] - wk_b[-2] if len(wk_b) > 1 else 0
                            rows_k.append([k] + [fmt(v) for v in wk_b] + [fmt(ch), f"{bt / ch * 100:.0f}%" if ch else "—",
                                                                          f"{'+' if d_ > 0 else ''}{d_}"])
                        slide2["table"] = {"title": "WhatsApp buyers by source, Kenya, week by week (green = more than the week before, red = fewer)",
                                           "cols": ["Source"] + [w.split(" (")[0] for w in wl] + [f"Chats {wl[-1].split(' (')[0]}", "Bought %", "Change"],
                                           "rows": rows_k, "mark": FOLLOWER_PATH, "trend": [1, len(wl)]}
                        # the month's story per source: which ones are climbing or sliding week after week
                        story = []
                        moved = sorted((k for k in names if len(sw.get(k) or []) >= 3),        # the two that moved most
                                       key=lambda k: -(max(sw[k]) - min(sw[k])))[:2]
                        for k in moved:
                            story.append(f"{k.split(' (')[0].lower()} {' → '.join(fmt(x) for x in sw[k])}")
                        if story:
                            # one bullet: the follower path, then the month's biggest runs (the old "biggest change" repeats it)
                            fp_i = next((i for i, ln in enumerate(insight2) if ln.startswith("Follower path")), None)
                            run = "Month so far: " + "; ".join(story) + "."
                            if fp_i is not None:
                                head_ = insight2[fp_i].split(" Biggest change:")[0].replace(" of WhatsApp buyers", "")
                                insight2[fp_i] = head_ + " " + run
                            else:
                                insight2.append(run)
                    except Exception as e_:                      # noqa: BLE001
                        print(f"  WARNING: week-by-week source table skipped: {e_}")
                        slide2["table"] = {"title": "WhatsApp buyers by source, Kenya",
                                           "cols": ["Source", "Chats", "Bought", "Before", "Change"],
                                           "rows": [[r[0], fmt(r[1]), fmt(r[2]), fmt(r[3]), f"{'+' if r[4] > 0 else ''}{r[4]}"]
                                                    for r in keep], "mark": FOLLOWER_PATH}
                # the full explanation (user's call, 23 Nov 2026): each path with its cause, then the net, written from
                # the week's figures so it holds every week (docs/weekly-report.md › Kenya Insight explained)
                if src_rows:
                    R_ = {r[0]: r for r in src_rows}
                    sg = lambda v: f"{'+' if v > 0 else ''}{fmt(v)}"                       # noqa: E731
                    pc_ = lambda x, y: f"{x / y * 100:.0f}%" if y else "—"                 # noqa: E731
                    ret, fba, fp_ = R_.get("Returning customers"), R_.get("Facebook ads"), R_.get(FOLLOWER_PATH)
                    wa_b = sum(r[2] for r in src_rows)
                    def vs_(p_, more="more", less="fewer"):      # "55% fewer than the week before"
                        return f"the same as {P.prev}" if not p_ else f"{abs(p_):.0f}% {more if p_ > 0 else less} than {P.prev}"
                    def n_(v, unit=""):                        # "148 fewer" / "52 more buyers"
                        return "no change" if not v else f"{fmt(abs(v))} {'more' if v > 0 else 'fewer'}" + (f" {unit}" if unit else "")
                    dc_ = pct(c1['chats'], c0['chats'])
                    lines = [f"<b>Online path</b>: {fmt(a['follows'])} new follows {P.when}"
                             + (f", {vs_(pf)} ({fmt(b['follows'])}): " if cmp_start >= first else
                                f" (follower data only starts on {day_label(first)}, so {P.prev} is incomplete: {fmt(b['follows'])}): ")
                             + f""
                             f"Facebook {fmt(b['fb'])} to {fmt(a['fb'])}, Instagram {fmt(b['ig'])} to {fmt(a['ig'])}. "
                             f"WhatsApp had {fmt(c1['chats'])} chats ({abs(dc_ or 0):.0f}% {'fewer' if (dc_ or 0) < 0 else 'more'}) and "
                             f"<b>{fmt(c1['purchased'])}</b> bought, {p1_(c1['performance'])} of chats against {p1_(c0['performance'])}: "
                             f"<b>{n_(d_wa, 'WhatsApp buyers')}</b>."]
                    why = [f"{fmt(ret[2])} returning customers bought, against {fmt(ret[3])} {P.prev} ({n_(ret[4])})"
                           for _ in [0] if ret]
                    why += [f"Facebook ads brought {fmt(fba[2])} buyers against {fmt(fba[3])} ({n_(fba[4])})" for _ in [0] if fba]
                    if why:
                        lines.append(f"<b>Why WhatsApp {'fell' if d_wa < 0 else 'moved'}</b>: " + ", and ".join(why) + ". "
                                     + (f"Ads started {pc_(c1['ads'], c1['chats'])} of chats, but only "
                                        f"{pc_(fba[2], fba[1])} of Facebook-ad chatters bought." if fba else ""))
                    lines.append(f"<b>Shop path</b>: {fmt(w1['counted'])} walk-ins, {vs_(pct(w1['counted'], w0['counted']))}; "
                                 f"<b>{fmt(w1['purchased'])}</b> bought, {p1_(w1['conversion'])} of walk-ins against "
                                 f"{p1_(w0['conversion'])}: <b>{n_(d_walk, 'shop buyers')}</b>. {fmt(w1['didntBuy'])} left without "
                                 f"buying.")
                    if fp_:
                        lines.append(f"<b>Follower path</b>: {fmt(fp_[1])} chats came from people who found our pages and "
                                     f"{fmt(fp_[2])} bought (<b>{pc_(fp_[2], fp_[1])}</b>"
                                     + (", the best rate" if fp_[1] and all(fp_[2] / fp_[1] >= r[2] / r[1] for r in src_rows
                                                                            if r[1] >= 5) and fp_[2] else "")
                                     + (f"; ad chats {pc_(fba[2], fba[1])}" if fba else "")
                                     + f"), but that is only {pc_(fp_[2], wa_b)} of WhatsApp buyers, {n_(fp_[4])} than {P.prev}.")
                    falls_ = sorted([r for r in src_rows if r[4] < 0], key=lambda r: r[4])[:2]
                    lines.append(f"<b>Net</b>: WhatsApp had {n_(d_wa, 'buyers')} and the shops {n_(d_walk)}: "
                                 f"{n_(d_wa + d_walk)} in all than {P.prev}. Bags sold went from {fmt(b['bags'])} to "
                                 f"{fmt(a['bags'])} ({abs(pb or 0):.0f}% {'fewer' if (pb or 0) < 0 else 'more'}), as some buy more than one. "
                                 + ("The drop comes from " + " and ".join(f"{(lambda t: t if t.startswith('Facebook') else t.lower())(r[0].split(' (')[0])} ({n_(r[4])})" for r in falls_)
                                    + (f", not follows: chats {'fell' if (dc_ or 0) < 0 else 'rose'} {abs(dc_ or 0):.0f}% while "
                                       f"follows {'fell' if pf < 0 else 'rose'} {abs(pf):.0f}%." if cmp_start >= first else ".")
                                    if falls_ and d_wa < 0 else ""))
                    insight2[:] = lines
                    slide2["wideSide"] = True
                if src_rec:
                    rec2.append(src_rec)
                elif d_wa < 0 and (pct(c1["purchased"], c0["purchased"]) or 0) <= -10:
                    rec2.append(f"Win back WhatsApp buyers: {fmt(c1['purchased'])} of {fmt(c1['chats'])} chats bought "
                                f"({p1_(c1['performance'])} vs {p1_(c0['performance'])}). Follow up the chats that didn't buy.")
                if w1["didntBuy"]:
                    rec2.append(f"Work on the {fmt(w1['didntBuy'])} walk-ins who left without buying, shop by shop (Footfall and "
                                f"Marketing ranks them): 5 points of conversion is worth about KES {fmt(extra * sale)} "
                                f"{'a week' if P.key == 'last_week' else 'over ' + P.noun}.")
                rec2.append(("Judge posts and ads by the WhatsApp chats and buyers they bring, not follows." if not linked else
                             "Repeat what went out on the top follow days, and track the WhatsApp buyers they bring.") + later)
                rec2[:] = rec2[:3]
            else:
                headline2 = (f"New follows {up(pf or 0)} {abs(pf or 0):.0f}% {P.when} while Kenya shop sales {up(pb or 0)} {abs(pb or 0):.0f}%: "
                             f"follows are building awareness, not this period's sales.")
                insight2.append(f"Day by day, sales had {words(scores['visitors'])} with shop visitors ({scores['visitors']}), "
                                f"{words(scores['chats'])} with WhatsApp chats ({scores['chats']}) and {words(sf)} with new follows ({sf}).")
                rec2.append("Judge posts and ads by WhatsApp chats and cost per chat, not follows." + later)
    except Exception as e:                                   # noqa: BLE001
        print(f"  WARNING: slide 2 skipped: {e}")

# ── Slide 2b: Followers vs sales, Sinza and Uganda (docs/weekly-report.md › Slide 2b) ──
EARLY_DAYS = 28
slide2b = {"ok": False}
headline2b, insight2b, rec2b = "", [], []
if db_ok:
    try:
        panels, lines_hl, ready_dates = [], [], []
        for code, key, name, shop, ff_shop in (("TZ", "tz", "Sinza", "sinza", "DAR-ES-ALAM"),
                                               ("UG", "ug", "Uganda", "uganda", "UGANDA")):
            fol = pd.DataFrame(odoo_marketing.followers_daily(code))
            if fol.empty:
                insight2b.append(f"<b>{name}</b>: no follower data in Odoo yet.")
                continue
            fol["date"] = pd.to_datetime(fol["date"]).dt.date
            fol = fol[fol.platform.isin(["instagram", "facebook"])]
            piv = lambda k: fol.groupby(["date", "platform"])[k].sum(min_count=1).unstack()   # noqa: E731
            nf, rc, vw = piv("newFollows"), piv("reach"), piv("views")
            both = nf.dropna()
            if both.empty:
                continue
            s = min(both.index)
            bags = daily_bags(min(s, cmp_start), week_end) or {}   # the comparison period in full
            wa = db.run_query("""
                SELECT i.date::date AS day, COUNT(*) AS chats
                FROM denri_monitor_interaction i JOIN denri_monitor_shop sh ON sh.id = i.shop_id
                WHERE i.date BETWEEN :s AND :e AND lower(sh.name) = :shop GROUP BY 1""",
                {"s": s.isoformat(), "e": week_end.isoformat(), "shop": shop})
            wa = {r["day"]: float(r["chats"]) for _, r in wa.iterrows()} if wa is not None else {}
            days_, d = [], s
            while d <= week_end:
                days_.append(d)
                d += dt.timedelta(days=1)
            follows = [float(nf.loc[d].sum()) if d in nf.index else None for d in days_]
            sold = [bags.get(d, {}).get(key, 0.0) for d in days_]
            dfm = pd.DataFrame({"f": follows, "b": sold}).dropna()
            sc = round(float(dfm["f"].corr(dfm["b"], method="spearman")), 2) if len(dfm) >= 7 else None
            # Shop visitors (footfall), same rules as Kenya's: None = the shop did not count that day.
            ff = footfall.daily(s, week_end)
            ff = ff[ff.shop == ff_shop] if not ff.empty else ff
            vis_by_day = ff.set_index("day")["visitors"].to_dict() if not ff.empty else {}
            visitors = [None if pd.isna(vis_by_day.get(d)) else float(vis_by_day[d]) for d in days_]
            dfv = pd.DataFrame({"v": visitors, "b": sold}).dropna()
            sc_v = round(float(dfv["v"].corr(dfv["b"], method="spearman")), 2) if len(dfv) >= 7 else None
            wk_vis = [v for d, v in zip(days_, visitors) if week_start <= d <= week_end and v is not None]
            n_days = len(days_)

            def wk(vals, a, b):
                return sum(v or 0 for d, v in zip(days_, vals) if a <= d <= b)
            pw_s, pw_e = cmp_start, cmp_end
            full_prev = s <= pw_s
            f1, f0 = wk(follows, week_start, week_end), wk(follows, pw_s, pw_e)
            b1 = wk(sold, week_start, week_end)
            b0 = sum(bags.get(pw_s + dt.timedelta(days=i), {}).get(key, 0.0) for i in range((pw_e - pw_s).days + 1))
            ig_reach = sum(float(rc.loc[d].get("instagram") or 0) for d in days_ if week_start <= d <= week_end and d in rc.index)
            views = sum(float(vw.loc[d].sum()) for d in days_ if week_start <= d <= week_end and d in vw.index)
            chats = sum(v for d, v in wa.items() if week_start <= d <= week_end)
            latest = lambda p: (fol[(fol.platform == p) & fol.followers.notna()].sort_values("date").followers.iloc[-1]   # noqa: E731
                                if ((fol.platform == p) & fol.followers.notna()).any() else None)
            ig_n, fb_n = latest("instagram"), latest("facebook")
            panels.append({"name": name, "labels": [f"{d.day} {d:%b}" for d in days_],
                           "follows": [round(v) if v is not None else None for v in follows], "bags": [round(v) for v in sold],
                           "visitors": [round(v) if v is not None else None for v in visitors]})
            insight2b.append(
                f"{P.When} <b>{name}</b> gained <b>{fmt(f1)}</b> new follows"
                + (f" ({signed(pct(f1, f0))} on {P.prev})" if full_prev and f0 else "")
                + f", sold <b>{fmt(b1)}</b> bags at the till" + (f" ({signed(pct(b1, b0))} on {P.prev})" if b0 else "")
                + f" and had {fmt(chats)} WhatsApp chat{'' if round(chats) == 1 else 's'}"
                + (f" and {fmt(sum(wk_vis))} shop visitors ({len(wk_vis)} of {P.days} day{'' if P.days == 1 else 's'} counted)."
                   if wk_vis else "."))
            lines_hl.append((name, f1, b1, sc, n_days))
            ft_daily[code] = pd.DataFrame({"follows": follows, "chats": [wa.get(d, 0.0) for d in days_], "bags": sold},
                                          index=pd.to_datetime(days_))
            ready_dates.append((name, s + dt.timedelta(weeks=CHECK_WEEKS)))
        if lines_hl:
            short = min(x[4] for x in lines_hl)
            parts = " and ".join(f"{n} +{fmt(f)} new follows ({fmt(b)} bag{'' if round(b) == 1 else 's'} sold)"
                                 for n, f, b, _, _ in lines_hl)
            if short < EARLY_DAYS:
                headline2b = f"{P.When} {parts}: with only {short} days of follower history, it is too early to link follows to sales."
            elif all((x[3] or 0) < LINK for x in lines_hl):
                headline2b = f"{P.When} {parts}: follows aren't moving with sales yet, so they are building awareness."
            else:
                headline2b = f"{P.When} {parts}: on some days follows and sales moved together; watch which posts did it."
            # WhatsApp buyers by source, both markets in one table
            try:
                srcs = {nm: source_change(cd) for cd, nm in (("TZ", "Sinza"), ("UG", "Uganda"))}
                labels = []
                for rows_, _, _ in srcs.values():
                    labels += [r[0] for r in rows_ if r[0] not in labels]
                cell = lambda rows_, k: next(((f"{fmt(r[2])} ({'+' if r[4] > 0 else ''}{r[4]})") for r in rows_ if r[0] == k), "0")  # noqa: E731
                tot_b = lambda k: sum(next((r[2] for r in v[0] if r[0] == k), 0) for v in srcs.values())   # noqa: E731
                labels.sort(key=lambda k: -tot_b(k))
                keep = labels[:4] + [k for k in labels[4:] if k == FOLLOWER_PATH]
                rest = [k for k in labels if k not in keep]
                rows_t = [[k] + [cell(v[0], k) for v in srcs.values()] for k in keep]
                if rest:
                    def other(v):
                        b_ = sum(r[2] for r in v[0] if r[0] in rest)
                        c_ = sum(r[4] for r in v[0] if r[0] in rest)
                        return f"{fmt(b_)} ({'+' if c_ > 0 else ''}{c_})"
                    rows_t.append(["Other"] + [other(v) for v in srcs.values()])
                slide2b_table = {"title": f"WhatsApp buyers by source {P.when} (change on {P.prev})",
                                 "cols": ["Source"] + list(srcs), "mark": FOLLOWER_PATH, "rows": rows_t}
                try:
                    wk2 = {nm: source_weeks(cd) for cd, nm in (("TZ", "Sinza"), ("UG", "Uganda"))}
                    nw = len(next(iter(wk2.values()))[0])
                    rows_w = []
                    for k in keep + (["Other"] if rest else []):
                        ks = [k] if k != "Other" else rest
                        row = [k]
                        for nm, (wl_, sw_, _) in wk2.items():
                            row += [fmt(sum(sw_.get(x, [0] * nw)[i] for x in ks)) for i in range(nw)]
                        if any(c != "0" for c in row[1:]):            # a source with no buyers all month adds nothing
                            rows_w.append(row)
                    short = [w.split(" (")[0] for w in next(iter(wk2.values()))[0]]
                    # each market's biggest run over the month, Wk 1 to last week
                    runs = []
                    for nm, (wl_, sw_, _) in wk2.items():
                        mv = max(sw_.items(), key=lambda kv: abs(kv[1][-1] - kv[1][0]), default=None)
                        if mv and mv[1][-1] != mv[1][0]:
                            runs.append(f"{src_words(nm, mv[0])} ({' → '.join(fmt(x) for x in mv[1])})")
                    if runs:
                        insight2b.append("Since Wk 1 the biggest shifts in WhatsApp buyers were " + " and ".join(runs) + ".")
                    slide2b_table = {"title": "WhatsApp buyers by source, week by week (green = more than the week before, red = fewer)",
                                     "cols": ["Source"] + [f"{nm} {w}" for nm in wk2 for w in short],
                                     "mark": FOLLOWER_PATH, "rows": rows_w,
                                     "trend": [[1 + j * nw, nw + j * nw] for j in range(len(wk2))]}
                except Exception as e_:                          # noqa: BLE001
                    print(f"  WARNING: Sinza/Uganda week-by-week source table skipped: {e_}")
                fpb = ", ".join(f"{nm} {fmt(next((r[2] for r in v[0] if r[0] == FOLLOWER_PATH), 0))}" for nm, v in srcs.items())
                big = []
                for nm, v in srcs.items():
                    if v[0]:
                        r = max(v[0], key=lambda r: abs(r[4]))
                        if r[4]:
                            big.append(f"{src_words(nm, r[0])} ({'+' if r[4] > 0 else ''}{r[4]})")
                insight2b.append(f"Buyers who came through the pages (the follower path): {fpb}."
                                 + (f" The biggest change on {P.prev} was {' and '.join(big)}." if big else ""))
                for nm, (_, _, rc_) in srcs.items():
                    if rc_:
                        rec2b.append(f"{nm}: {rc_}")
            except Exception as se:                          # noqa: BLE001
                print(f"  WARNING: Sinza / Uganda WhatsApp sources skipped: {se}")
                slide2b_table = None
            rec2b.append("Judge Sinza and Uganda's posts and ads by WhatsApp chats and bags sold at the shop, not by follows.")
            uniq = sorted({d for _, d in ready_dates})
            when = (f"{day_label(uniq[0])} {uniq[0].year}" if len(uniq) == 1
                    else " and ".join(f"{day_label(d)} {d.year} ({n})" for n, d in ready_dates))
            rec2b.append(f"Check this again from {when}, with {CHECK_WEEKS} weeks of history.")
            rec2b[:] = rec2b[:3] if len(rec2b) <= 3 else rec2b[:2] + rec2b[-1:]
            slide2b = {"ok": True, "kind": "folmk", "panels": panels}
            if slide2b_table:
                slide2b["table"] = slide2b_table
    except Exception as e:                                   # noqa: BLE001
        print(f"  WARNING: slide 2b skipped: {e}")

# ── Foot Traffic page figures for last week, per market (docs/weekly-report.md › Foot traffic band) ──
def _ft_band(name: str, f: dict) -> dict:
    """One market's three rows, labelled as on the Denri dashboard's Foot Traffic page."""
    w, n, a = f["walkins"], f["not_walkins"], f["whatsapp"]
    p = lambda v: "—" if v is None else f"{v:.1f}%"                       # noqa: E731
    return {"name": name, "groups": [
        {"label": "Walk-ins", "note": "the people who came into the shops", "items": [
            ["Walk-ins counted", fmt(w["counted"]), f"{w['shopDays']} shop-days counted"],
            ["Purchased walk-ins", fmt(w["purchased"]), "walk-in orders on the POS"],
            ["Didn't buy", fmt(w["didntBuy"]), "counted, no purchase"],
            ["Walk-in conversion", p(w["conversion"]), "purchased ÷ counted"],
            ["Revenue per walk-in", "—" if w["revPerWalkin"] is None else f"KES {w['revPerWalkin']:,}", "walk-in revenue ÷ counted"]]},
        {"label": "Not walk-ins", "note": "orders that are not part of the conversion", "items": [
            ["Online orders", fmt(n["online"]), "ordered online"],
            ["Activation & employee", fmt(n["other"]), "other order types"],
            ["Refunds", fmt(n["refunds"]), "refund orders"],
            ["Days not counted", fmt(n["daysNotCounted"]), "walk-ins bought, no count"],
            ["Undercounted days", fmt(n["undercounted"]), "more purchases than counted"]]},
        {"label": "WhatsApp", "note": f"chats handled by every {name} shop, from the WhatsApp Monitor", "items": [
            # the 4th field is printed on the tile: the people behind each figure (user's call, 23 Nov 2026)
            ["Performance", p(a["performance"]), "chats that bought ÷ all chats",
             f"{fmt(a['purchased'])} of {fmt(a['chats'])} bought"],
            ["Ads", fmt(a["ads"]), "chats that came from ads",
             f"{fmt(a.get('adPurchased', 0))} bought" if a["ads"] else "none"],
            ["Avg response", "—" if a["avgResponse"] is None else f"{a['avgResponse']:.1f} min",
             "average time to answer a chat, over the chats with a timed reply",
             f"{fmt(a['sampled'])} of {fmt(a['chats'])} timed"]]},
    ]}


# ── Follower test: follows → chats → bags, per market (docs/weekly-report.md › Follower test) ──
ftest_slide = {"id": "follower-test", "kicker": "Follower test: does a new follower become a sale?", "tone": "neutral",
               "headline": "", "insight": [], "rec": [], "graph": {"ok": False},
               "source": "Odoo Meta sync (new follows), WhatsApp Monitoring (chats, every source), the market's tills (bags); "
                         "weekday-adjusted daily figures, rank correlation with a 2,000-shuffle chance test."}
try:
    from lib import follower_test
    results = []
    for code, name in (("KE", "Kenya"), ("TZ", "Sinza"), ("UG", "Uganda")):
        if code in ft_daily:
            r = follower_test.run(ft_daily[code])
            r["name"] = name
            results.append(r)
    if results:
        ftest_slide["graph"] = {"ok": True, "kind": "ftest", "markets": results,
                                "names": {k: v[3] for k, v in follower_test.LINKS.items()}}
        ke = results[0]
        lag = ((ke.get("links") or {}).get("f2b") or {}).get("lag") or 0
        ftest_slide["headline"] = {
            "none": f"In {ke['name']}, new follows didn't lead to more WhatsApp chats or bags over {ke['days']} days: "
                    "they are brand growth only, for now.",
            "chats": f"In {ke['name']}, new follows turn into WhatsApp chats that buy.",
            "awareness": f"In {ke['name']}, new follows lift sales {lag} day{'s' if lag != 1 else ''} later, but not through WhatsApp chats.",
            "leak": f"In {ke['name']}, new follows bring WhatsApp chats, but those chats don't buy.",
        }.get(ke["code"], f"{ke['name']}: {ke['verdict']}")
        for r in results:
            if r["code"] == "early":
                ftest_slide["insight"].append(f"<b>{r['name']}</b> is {r['verdict'][0].lower() + r['verdict'][1:]}")
                continue
            L = r["links"]
            short = lambda k, nm: (f"{nm} {L[k]['score']:.2f} ({'passed' if L[k]['passed'] else f'chance {L[k][chr(112)] * 100:.0f}%'})"  # noqa: E731
                                   if L[k].get("score") is not None else f"{nm} n/a")
            ftest_slide["insight"].append(f"Over {r['days']} days in <b>{r['name']}</b>, the link scores were: " + ", ".join(
                short(k, nm) for k, nm in (("f2c", "follows to chats"), ("c2b", "chats to bags"), ("f2b", "follows to bags"))) + ".")
        ftest_slide["insight"].append("A score of 0 means no link and 1 means the two always move together. The chance is how "
                                      "often shuffled days score as high, so a high chance means the link could be luck. A link "
                                      "passes at a score of 0.3 or more with a chance under 5%.")
        recs = {"chats": "Grow follows on purpose: they turn into WhatsApp buyers. Point every post to WhatsApp.",
                "awareness": "Keep growing follows for awareness, and judge them by sales a week later, not by chats.",
                "leak": "Follows bring chats that don't buy: follow up page chats within the hour and send prices and pictures.",
                "none": "Don't buy follows for sales: judge Meta posts and ads by WhatsApp chats and buyers.",
                "early": None}
        for r in results:
            t = recs.get(r["code"])
            if t and t not in ftest_slide["rec"]:
                ftest_slide["rec"].append(t if r is ke else f"{r['name']}: {t}")
        early = [r for r in results if r["code"] == "early"]
        if early:
            ftest_slide["rec"].append("Run the test for " + " and ".join(r["name"] for r in early)
                                      + " once they have 28 days: it updates itself every week.")
        ftest_slide["rec"] = ftest_slide["rec"][:3]
except Exception as e:                                       # noqa: BLE001
    print(f"  WARNING: follower test skipped: {e}")

ft_bands = {}
if db_ok:
    try:
        ft = foot_traffic.summary(week_start, week_end)
        ft_bands = {"KE": [_ft_band("Kenya", ft["KE"])],
                    "TZUG": [_ft_band("Sinza", ft["TZ"]), _ft_band("Uganda", ft["UG"])]}
    except Exception as e:                                   # noqa: BLE001
        print(f"  WARNING: foot traffic band skipped: {e}")

owner = {}
try:
    owner = json.load(open(paths.root("dashboard_pages.json"), encoding="utf-8")).get("owner", {})
except Exception:                                            # noqa: BLE001
    pass

WR = {
    "built": dt.datetime.now().strftime("%a %d %b %Y, %H:%M"),
    "weekStart": week_start.isoformat(), "weekEnd": week_end.isoformat(),
    "weekLabel": P.dates, "period": P.to_json(),
    "asOf": day_label(today),
    "owner": {"name": owner.get("name", ""), "title": owner.get("title", "")},
    "slides": [
        {"id": "sales", "kicker": f"Sales, {month_name} to date (as of {day_label(today)})",
         "headline": headline1, "tone": tone1,
         "graph": slide1, "insight": insight1, "rec": rec1,
         "source": "Odoo tills and the Corporate app, the Current Performance page's Sales card and its hover."},
        {"id": "followers", "kicker": "Followers vs sales, Kenya",
         "headline": headline2, "tone": "neutral",
         "graph": slide2, "insight": insight2, "rec": rec2, "band": ft_bands.get("KE", []),
         "source": "Odoo Meta sync (Kenya page and account), Kenya shop tills, WhatsApp Monitoring and footfall. "
                   f"Band: {P.noun} ({P.dates}), the Denri dashboard's Foot Traffic page (Hilton left out: mall traffic)."},
        {"id": "followers-tzug", "kicker": "Followers vs sales, Sinza and Uganda",
         "headline": headline2b, "tone": "neutral",
         "graph": slide2b, "insight": insight2b, "rec": rec2b, "band": ft_bands.get("TZUG", []),
         "source": "Odoo Meta sync (Sinza and Uganda pages and accounts, from 10 to 11 Nov 2026), the Sinza and Uganda tills, "
                   f"WhatsApp Monitoring and footfall. Band: {P.noun} ({P.dates}), the Denri dashboard's Foot Traffic page."},
        ftest_slide,
    ],
}
# Walk-ins and WhatsApp, Week 1 to latest and month to date (docs/weekly-report.md), both decks
if db_ok:
    try:
        from lib import weekly_foot
        WR["slides"].append(weekly_foot.slide(week_start, week_end))
    except Exception as e:                                   # noqa: BLE001
        print(f"  WARNING: walk-ins and WhatsApp week-by-week slide skipped: {e}")

# Product Performance slides, Kenya then Uganda then Tanzania (docs/weekly-report.md › Product Performance slides)
if db_ok:
    try:
        from lib import weekly_products
        WR["slides"] += weekly_products.slides(week_start, week_end)
    except Exception as e:                                   # noqa: BLE001
        print(f"  WARNING: product slides skipped: {e}")
    # New Products slides (docs/weekly-report.md › New Products slides)
    try:
        from lib import weekly_newproducts
        WR["slides"] += weekly_newproducts.slides(week_start, week_end)
    except Exception as e:                                   # noqa: BLE001
        print(f"  WARNING: new products slides skipped: {e}")
    # Combos and offers slides (docs/weekly-report.md › Combos and offers slides)
    try:
        from lib import weekly_combos
        WR["slides"] += weekly_combos.slides(week_start, week_end)
    except Exception as e:                                   # noqa: BLE001
        print(f"  WARNING: combos slides skipped: {e}")

# Sales deck (docs/weekly-report.md › Two reports in one page): its own slides from Current Performance, then the
# shared ones. The Marketing deck keeps everything but the sales-only slides.
try:
    from lib import weekly_sales
    WR["slides"] += weekly_sales.slides(week_start, week_end)
except Exception as e:                                       # noqa: BLE001
    print(f"  WARNING: sales slides skipped: {e}")
MARKETING_ONLY = {"followers", "followers-tzug", "follower-test"}
SALES_FIRST = ["sales", "weekly-perf", "why-moved", "why-shops", "what-if", "price", "corporate"]
# A slide whose Odoo query failed this run (a blip on the read replica) keeps the last good build of the same
# week instead of going blank (docs/weekly-report.md › Keep the last good slide).
try:
    with open(paths.html("weekly_report.html"), encoding="utf-8") as f:
        _m = re.search(r"const WR = (\{.*?\});\s*</script>\s*<!-- WR_DATA_END -->", f.read(), flags=re.DOTALL)
    _old = json.loads(_m.group(1)) if _m else {}
except Exception:                                            # noqa: BLE001
    _old = {}
if _old.get("weekStart") == str(WR.get("weekStart")) and _old.get("weekEnd") == str(WR.get("weekEnd")):
    _good = {sl.get("id"): sl for sl in _old.get("slides") or [] if (sl.get("graph") or {}).get("ok") and sl.get("headline")}
    for _i, _sl in enumerate(WR["slides"]):
        if not ((_sl.get("graph") or {}).get("ok") and _sl.get("headline")) and _sl.get("id") in _good:
            WR["slides"][_i] = {**_good[_sl["id"]], "carried": _old.get("built")}
            print(f"  NOTE: slide {_sl['id']} had no data this run; kept the build from {_old.get('built')}")
    _have = {sl["id"] for sl in WR["slides"]}
    _prev_id = None
    for _sl in _old.get("slides") or []:
        if _sl.get("id") in _good and _sl["id"] not in _have:        # put it back after the slide it followed
            _at = next((k + 1 for k, x in enumerate(WR["slides"]) if x["id"] == _prev_id), 0)
            WR["slides"].insert(_at, {**_sl, "carried": _old.get("built")})
            _have.add(_sl["id"])
            print(f"  NOTE: slide {_sl['id']} missing this run; kept the build from {_old.get('built')}")
        _prev_id = _sl.get("id")

ids = [sl["id"] for sl in WR["slides"]]
sales_only ={sl["id"] for sl in WR["slides"] if sl.get("decks") == ["sales"]}
WR["decks"] = {
    "marketing": [i for i in ids if i not in sales_only],
    "sales": [i for i in SALES_FIRST if i in ids] + [i for i in ids if i not in MARKETING_ONLY and i not in SALES_FIRST],
}

block =("<!-- WR_DATA_START -->\n<script>\nconst WR = " + json.dumps(WR, ensure_ascii=False, default=str)
         + ";\n</script>\n<!-- WR_DATA_END -->")
html_path = paths.html("weekly_report.html")
with open(html_path, encoding="utf-8") as f:
    page = f.read()
page = re.sub(r"<!-- WR_DATA_START -->.*?<!-- WR_DATA_END -->", lambda _m: block, page, flags=re.DOTALL)
paths.write_atomic(html_path, page)
print(f"  Weekly report: week {WR['weekLabel']}, {len(WR['slides'])} slides"
      + ("" if slide2.get("ok") else " (followers slide has no data)"))

if not os.environ.get("DENRI_LAUNCHER"):
    import webbrowser
    webbrowser.open("file:///" + os.path.abspath(html_path).replace("\\", "/"))
