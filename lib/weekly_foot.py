"""Weekly report: walk-ins and WhatsApp week by week, Week 1 of the month to the report week, plus month to date
(docs/weekly-report.md › Walk-ins and WhatsApp, week by week). Same figures as the Foot Traffic page
(lib/foot_traffic.summary), one call per week."""
from __future__ import annotations

import datetime as dt

from lib import foot_traffic

MARKETS = (("KE", "Kenya"), ("TZ", "Sinza"), ("UG", "Uganda"))


def _fmt(v) -> str:
    return f"{round(v):,}" if v is not None else "—"


def _weeks(week_end: dt.date) -> list[tuple[dt.date, dt.date]]:
    """Sun-to-Sat weeks of the month, Week 1 starting on the 1st, the last one ending on the report week's Saturday."""
    s, out = week_end.replace(day=1), []
    while s <= week_end:
        e = min(s + dt.timedelta(days=(5 - s.weekday()) % 7), week_end)    # next Saturday (weekday 5)
        out.append((s, e))
        s = e + dt.timedelta(days=1)
    return out


def _row(label: str, f: dict) -> dict:
    w, a = f["walkins"], f["whatsapp"]
    return {"label": label,
            "counted": w["counted"], "bought": w["purchased"], "conv": w["conversion"], "days": w["shopDays"],
            "chats": a["chats"], "waBought": a["purchased"], "perf": a["performance"],
            "resp": a["avgResponse"], "sampled": a["sampled"]}


def slide(week_start: dt.date, week_end: dt.date) -> dict:
    weeks = _weeks(week_end)
    per_week = [foot_traffic.summary(s, e) for s, e in weeks]
    mtd = foot_traffic.summary(weeks[0][0], week_end)
    mon = week_end.strftime("%b")
    labels = [f"Wk {i + 1} ({s.day}–{e.day} {mon})" for i, (s, e) in enumerate(weeks)]
    markets = []
    for code, name in MARKETS:
        rows = [_row(lb, f[code]) for lb, f in zip(labels, per_week)] + [_row("Month to date", mtd[code])]
        markets.append({"code": code, "name": name, "rows": rows})
    s = {"id": "foot-weeks", "kicker": f"Walk-ins and WhatsApp, Week 1 to latest and {week_end.strftime('%B')} to date",
         "tone": "neutral", "insight": [], "rec": [],
         "source": "The Denri dashboard's Foot Traffic page figures (footfall counts, POS walk-in orders, WhatsApp Monitor), "
                   "one Sun-to-Sat week at a time; Hilton left out (mall traffic).",
         "graph": {"ok": True, "kind": "footwk", "markets": markets}}

    def ch(a, b):
        return None if a is None or b is None else round(a - b, 1)

    lines, worst = [], None
    for m in markets:
        last, prev, md = m["rows"][-2], (m["rows"][-3] if len(m["rows"]) > 2 else None), m["rows"][-1]
        dc, dp = ch(last["conv"], prev and prev["conv"]), ch(last["perf"], prev and prev["perf"])
        part = (f"In <b>{m['name']}</b>, {last['conv'] if last['conv'] is not None else '—'}% of walk-ins bought last week"
                + (f" ({'+' if dc >= 0 else ''}{dc} points)" if dc is not None else "")
                + f" and {md['conv'] if md['conv'] is not None else '—'}% this month ({_fmt(md['bought'])} of {_fmt(md['counted'])}); "
                f"on WhatsApp {last['perf'] if last['perf'] is not None else '—'}% of chats bought"
                + (f" ({'+' if dp >= 0 else ''}{dp} points)" if dp is not None else "")
                + f" and {md['perf'] if md['perf'] is not None else '—'}% this month ({_fmt(md['waBought'])} of {_fmt(md['chats'])})"
                + (f", with replies in {last['resp']} minutes on average" if last["resp"] is not None else "") + ".")
        lines.append(part)
        if last["perf"] is not None and (worst is None or last["perf"] < worst[1]["perf"]):
            worst = (m, last, prev)
    s["insight"] = lines
    best_c = max(markets, key=lambda m: m["rows"][-1]["conv"] or 0)
    s["headline"] = (f"Month to date, {best_c['name']} converts the most walk-ins "
                     f"({best_c['rows'][-1]['conv']}%), and WhatsApp turns "
                     + ", ".join(f"{m['rows'][-1]['perf']}% of {m['name']}'s chats" for m in markets) + " into sales.")
    for m in markets:
        last, prev = m["rows"][-2], (m["rows"][-3] if len(m["rows"]) > 2 else None)
        if prev and last["conv"] is not None and prev["conv"] is not None and last["conv"] < prev["conv"] - 5:
            s["rec"].append(f"{m['name']}: walk-in conversion fell {prev['conv']}% → {last['conv']}% last week; "
                            f"check the shop floor (stock on display, staff on the door) with the shop leads.")
        if prev and last["resp"] is not None and prev["resp"] is not None and last["resp"] > prev["resp"] * 1.5 and last["resp"] > 3:
            s["rec"].append(f"{m['name']}: WhatsApp replies slowed to {last['resp']} min (from {prev['resp']}); "
                            f"get first replies under 2 minutes.")
    if worst and not any(worst[0]["name"] in r for r in s["rec"]):
        s["rec"].append(f"{worst[0]['name']}: WhatsApp sells to {worst[1]['perf']}% of chats, the lowest; review how chats "
                        f"are followed up (price sent, photos, a call back).")
    s["rec"] = s["rec"][:3]
    return s
