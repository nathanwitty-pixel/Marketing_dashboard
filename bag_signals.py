"""bag_signals.py — the Bag Signals page: drift, volatility, reliability, trend, beta, run-out risk and safe
stock per bag, with an action (spec: docs/bag-signals.md). Maths: lib/bag_quant.py.

    python bag_signals.py        # DENRI_LAUNCHER=1 to skip the browser tab
"""
import datetime
import json
import os
import re
import webbrowser

from lib import bag_quant as bq, product_targets

BASE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(BASE, "bag_signals.html")
HISTORY = os.path.join(BASE, "bag_posts_history.json")
SHEET_ID = "1Zb8Ly6vGrEHbxiYz0Dwd3aS8suUe86G66IDAWRdBKt0"


def _posts():
    """MONTHLY / WEEKLY_MARKETING_POST rows, or ([], []) if the sheet can't be read."""
    try:
        from google_auth import get_gspread_client
        sh = get_gspread_client().open_by_key(SHEET_ID)
        return sh.worksheet("MONTHLY_MARKETING_POST").get_all_values(), sh.worksheet("WEEKLY_MARKETING_POST").get_all_values()
    except Exception as e:                                   # noqa: BLE001
        print(f"  Posts unavailable ({e}) — posting columns empty.")
        return [], []


def _save_history(posts, daily, end):
    """Append last week's posts + sales per bag (one row per Sun–Sat week) — feeds the posting beta."""
    ws = end - datetime.timedelta(days=(end.weekday() + 1) % 7)            # Sunday of the week holding `end`
    last_sun = ws - datetime.timedelta(days=7) if end < ws + datetime.timedelta(days=6) else ws
    week = last_sun.isoformat()
    try:
        hist = json.load(open(HISTORY, encoding="utf-8"))
    except (OSError, ValueError):
        hist = []
    if any(h["week"] == week for h in hist):
        return hist
    start = end - datetime.timedelta(days=len(next(iter(daily.values()), [])) - 1) if daily else end
    lo = (last_sun - start).days
    rows = {}
    for b, (_, wk) in posts.items():
        series = daily.get(b) or []
        sold = sum(v for v in series[max(lo, 0):lo + 7] if v is not None) if 0 <= lo < len(series) else None
        if sold is not None:
            rows[b] = {"posts": wk, "sold": round(sold)}
    hist.append({"week": week, "bags": rows})
    json.dump(hist, open(HISTORY, "w", encoding="utf-8"), indent=1)
    return hist


def build():
    daily, total, stock, launch, start, end = bq.load()
    sig = bq.signals(daily, total, stock)
    key = product_targets.bag_key_fn()
    m_rows, w_rows = _posts()
    posts = bq.bag_posts(m_rows, w_rows, key) if (m_rows or w_rows) else {}
    hist = _save_history(posts, daily, end) if posts else []
    rows = []
    for b, s in sig.items():
        r = {"bag": b, **s, "launch": launch[b].isoformat() if launch.get(b) and launch[b] >= start else None}
        pm, pw = posts.get(b, (0, 0))
        r["postsMonth"], r["postsWeek"] = pm, pw
        r["postBeta"] = bq.posting_beta(hist, b)
        rows.append(r)
    rows.sort(key=lambda r: (r.get("tooFew", False), -(r.get("avg") or 0)))
    weeks = len(hist)
    return {"generated": datetime.datetime.now().strftime("%d %b %Y %H:%M"),
            "window": f"{start.strftime('%d %b')} – {end.strftime('%d %b %Y')}", "days": bq.DAYS,
            "horizon": bq.HORIZON, "kenyaPerDay": round(sum(total) / len(total)) if total else 0,
            "postWeeks": weeks, "rows": rows}


def inject(payload):
    with open(HTML, encoding="utf-8") as f:
        html = f.read()
    block = ("<!-- BAGQ_DATA_START -->\n<script>\nconst BQ = "
             + json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
             + ";\n</script>\n<!-- BAGQ_DATA_END -->")
    html = re.sub(r"<!-- BAGQ_DATA_START -->.*?<!-- BAGQ_DATA_END -->", lambda _m: block, html, flags=re.S)
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    p = build()
    judged = [r for r in p["rows"] if not r.get("tooFew")]
    print(f"  Bag Signals: {len(judged)} bags judged ({len(p['rows'])} listed), window {p['window']}, "
          f"posts history {p['postWeeks']} week(s)")
    inject(p)
    if os.environ.get("DENRI_LAUNCHER") != "1":
        webbrowser.open("file://" + HTML)
