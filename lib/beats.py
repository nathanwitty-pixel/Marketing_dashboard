"""Three beats for each Current Performance card (docs/current-performance.md › Three beats).

Beat 1 = the headline (the takeaway, with its number), Beat 2 = the chart already on the card,
Beat 3 = the recommendation (one line that starts with a verb). The generators call these with
figures they already have; the page only renders the strings. Pure functions: no DB, no files.

Each function returns {"headline", "rec", "tone"} (tone = good / warn / bad / neutral), or None
when there isn't enough data to say anything true. Words and commas only, no dot separators.
"""
from datetime import date, timedelta
import calendar

# Projected month end as % of target: below OUT_OF_REACH = out of reach, below ON_TRACK = within reach.
OUT_OF_REACH = 90
ON_TRACK = 100


def _n(x):
    return f"{round(x):,}"


def _tone_for(pct):
    return "good" if pct >= ON_TRACK else ("warn" if pct >= OUT_OF_REACH else "bad")


def summary(month, sales, target, proj_bags, done, days_in_month):
    """The strip at the top of the page: where the month will land and what it takes to close the gap.
    sales = the Sales card (tills + corporate paid); proj_bags = the Forecasted projection in bags;
    done = complete days so far."""
    if not target or not days_in_month:
        return None
    proj_pct = proj_bags / target * 100
    left = max(days_in_month - done, 0)
    remaining = max(target - sales, 0)
    rate = sales / done if done else 0
    need = remaining / left if left else 0
    headline = (f"{month} is on course for about {_n(round(proj_bags, -2))} bags, "
                f"{proj_pct:.0f}% of the {_n(target)} target.")
    evidence = (f"{_n(sales)} sold so far ({sales / target * 100:.0f}%) with {done / days_in_month * 100:.0f}% "
                f"of the month gone ({done} of {days_in_month} days). "
                + (f"{_n(remaining)} bags still to sell in {left} days." if remaining else "The target is already met."))
    if not remaining:
        rec = "Keep selling: every bag from here is above target. Protect stock on the top sellers."
    elif proj_pct >= ON_TRACK:
        rec = f"Hold the pace: {_n(rate)} bags a day lands the target. Protect stock on the top sellers."
    elif proj_pct >= OUT_OF_REACH:
        rec = (f"Push to close it: the target needs {_n(need)} bags a day from here, "
               f"{_n(need - rate)} a day more than so far.")
    else:
        rec = (f"Decide on a push now or reset the month's expectation: the target needs {_n(need)} bags a day "
               f"against {_n(rate)} a day so far.")
    return {"headline": headline, "evidence": evidence, "rec": rec, "tone": _tone_for(proj_pct)}


def _week_days(w, month_end):
    s = date.fromisoformat(w["weekStart"])
    e = min(s + timedelta(days=(5 - s.weekday()) % 7), month_end)      # that week's Saturday, cut at month end
    return s, e, (e - s).days + 1


def weekly(history, today, target, sales, bare_minimum):
    """Weekly Performance card: the last complete week against the one before (per day, since the
    month's first and last weeks are short), and what each week from here has to do."""
    if not history:
        return None
    s0 = date.fromisoformat(history[0]["weekStart"])
    month_end = s0.replace(day=calendar.monthrange(s0.year, s0.month)[1])
    full, current = [], None
    for w in history:
        s, e, d = _week_days(w, month_end)
        if e < today:
            full.append((w, d))
        elif s <= today:
            current = (w, (today - s).days)                # complete days so far this week
    if not full:
        return None
    b, db_ = full[-1]
    rb = b["weeklySales"] / db_
    if len(full) >= 2:
        a, da = full[-2]
        ra = a["weeklySales"] / da
        ch = (rb / ra - 1) * 100 if ra else 0
        headline = (f"{b['label']} sold {_n(b['weeklySales'])} bags ({_n(rb)} a day), "
                    f"{abs(ch):.0f}% {'more' if ch >= 0 else 'less'} a day than {a['label']}.")
        tone = "good" if ch >= 0 else "bad"
    else:
        headline = f"{b['label']} sold {_n(b['weeklySales'])} bags ({_n(rb)} a day) over {db_} days."
        tone = "neutral"
    left_days = (month_end - today).days + 1
    remaining = max(target - sales, 0)
    need = remaining / left_days if left_days else 0
    if not remaining:
        rec = "Keep it going: the month's target is met."
    elif rb >= need:
        rec = f"Hold this rate: {_n(rb)} a day is enough, the target needs {_n(need)} a day from here."
    else:
        rec = (f"Lift the daily rate from {_n(rb)} to {_n(need)} bags to reach target; "
               f"use Why Did We Move? below to find the shops that fell.")
    if current and bare_minimum:
        w, d = current
        short = bare_minimum - w["weeklySales"]
        if short > 0:
            rec += (f" This week has {_n(w['weeklySales'])} so far against the weekly floor of {_n(bare_minimum)}: "
                    f"{_n(short)} more by Saturday.")
    return {"headline": headline, "rec": rec, "tone": tone}


def projections(proj_bags, target, rev_pct):
    """Forward Projections cards: bags and revenue together, and what the gap between them means."""
    if not target:
        return None
    bags_pct = proj_bags / target * 100
    headline = (f"Month end: about {_n(round(proj_bags, -2))} bags, {bags_pct:.0f}% of target"
                + (f", and {rev_pct:.0f}% of the revenue target." if rev_pct is not None else "."))
    if rev_pct is None:
        rec = "Watch the bag count: there is no live revenue figure to compare yet."
    elif rev_pct - bags_pct > 2:
        rec = ("Push the bag count, not discounts: revenue runs ahead of bags, so the price per bag is "
               "holding and the gap is volume.")
    elif rev_pct - bags_pct < -2:
        rec = ("Check discounts and the offer mix below: revenue trails bags, so bags are selling under "
               "the target price.")
    else:
        rec = "Push the bag count: revenue and bags move together, so the gap is volume."
    return {"headline": headline, "rec": rec, "tone": _tone_for(bags_pct)}


def price(price_mix):
    """Price per Bag card: the price gap, and the group that drags revenue most."""
    if not price_mix:
        return None
    a, t, g = price_mix["actualPpb"], price_mix["targetPpb"], price_mix["gapPct"]
    headline = (f"Bags sell at KES {_n(a)} against the KES {_n(t)} target price ({g:+.1f}%), so revenue "
                f"{'runs ahead of' if g > 0 else 'trails' if g < 0 else 'keeps pace with'} bags.")
    rows = (price_mix.get("offerMix") or {}).get("rows") or price_mix.get("rows") or []
    cands = []
    for r in rows:
        cands += r.get("parts") or [r]
    cands = [r for r in cands if r.get("key") not in ("UNC",) and r.get("effectKes", 0) < 0]
    if cands:
        worst = min(cands, key=lambda r: r["effectKes"])
        rec = (f"Review {worst['label']}: it brings in KES {_n(-worst['effectKes'])} less by month end "
               f"than its target price expects.")
    else:
        rec = "Keep the mix: no group sells below its target price."
    return {"headline": headline, "rec": rec, "tone": "good" if g >= 0 else "bad"}


def corporate(sold, target, clients, month_gone_pct):
    """Corporate by Client: sold against the corporate target, the open pipeline, and who to chase."""
    open_q = []
    for c in clients or []:
        for q in c.get("quotes") or []:
            try:
                bags = int(float(q.get("bags") or 0))
            except ValueError:
                bags = 0
            if not q.get("invoice") and bags:
                open_q.append((bags, c["client"], q))
    pipe = sum(b for b, _, _ in open_q)
    tb = (target or {}).get("bags")
    if tb:
        pct = sold / tb * 100
        headline = f"Corporate: {_n(sold)} bags sold, {pct:.0f}% of the {_n(tb)} target"
        tone = "good" if pct >= month_gone_pct else "bad"
    else:
        headline = f"Corporate: {_n(sold)} bags sold this month"
        tone = "neutral"
    headline += (f", with {_n(pipe)} bags quoted and not invoiced yet." if pipe else ".")
    recs = []
    if open_q:
        bags, client, q = max(open_q, key=lambda x: x[0])
        kes = q.get("kes")
        recs.append(f"Chase {client} on {q.get('no', 'their quote')} ({bags} bags"
                    + (f", KES {_n(float(kes))}" if kes else "")
                    + (f", valid until {q['until']}" if q.get("until") else "") + ").")
    owed = [(c.get("agreedKes", 0) - c.get("paidKes", 0), c["client"]) for c in clients or []]
    owed = [o for o in owed if o[0] > 0]
    if owed:
        kes, client = max(owed)
        recs.append(f"Collect KES {_n(kes)} still owed by {client}.")
    rec = " ".join(recs) or "Find the next order: nothing is quoted or owed right now."
    return {"headline": headline, "rec": rec, "tone": tone}
