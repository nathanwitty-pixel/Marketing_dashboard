"""
chronos_preview.py
─────────────────────────────────────────────────────────────────
Preview of an Amazon Chronos-2 month-end forecast for till (POS) bag
sales, next to the straight-line run rate the dashboard uses today.
Not in dashboard_pages.json yet — open chronos_preview.html directly.

Run with the Chronos venv (PyTorch lives there, not in Anaconda):
    C:\\Users\\nate\\.venvs\\chronos\\Scripts\\python.exe chronos_preview.py

Steps:
  1. daily bags = BAGS_SOLD_TOTAL grouped by day (same filters as Sales,
     till sales only — corporate bags are NOT included)
  2. this month: Chronos forecasts the remaining days (10% / 50% / 90%)
  3. track record: for each of the last 12 finished months, project the
     month on day 3/7/10/15/20/25 both ways and compare with the actual
  4. inject the result as JSON between the CHRONOS_DATA markers, plus
     chronos_train_results.json (if chronos_train.py has been run)
     between the CHRONOS_TRAIN markers
─────────────────────────────────────────────────────────────────
"""
import calendar
import json
import os
import re
import time
from datetime import date, datetime, timedelta

import pandas as pd
import torch
from chronos import Chronos2Pipeline

from lib import db, queries

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "chronos_preview.html")
HISTORY_START = "2024-01-01"          # daily data is continuous from mid-Dec 2023
CHECK_DAYS = [3, 7, 10, 15, 20, 25]
BACKTEST_MONTHS = 12
QUANTILES = [0.1, 0.5, 0.9]


TRAIN_RESULTS = os.path.join(HERE, "chronos_train_results.json")


def inject(marker, name, data):
    """Put `data` into the page as `const <name>` between the <marker>_START/END comments."""
    with open(HTML, encoding="utf-8") as f:
        html = f.read()
    html = re.sub(rf"(<!-- {marker}_START -->).*?(<!-- {marker}_END -->)",
                  lambda mm: f"{mm.group(1)}\n<script>const {name} = {json.dumps(data)};</script>\n{mm.group(2)}",
                  html, flags=re.S)
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(html)


def inject_train():
    """The latest chronos_train.py results, if it has been run."""
    if os.path.exists(TRAIN_RESULTS):
        with open(TRAIN_RESULTS, encoding="utf-8") as f:
            inject("CHRONOS_TRAIN", "CHRONOS_TRAIN", json.load(f))


def daily_bags(end):
    sql = queries.BAGS_SOLD_TOTAL.replace(
        "SELECT\n  COALESCE(SUM(pl.qty), 0)::numeric AS bags,",
        "SELECT p.date_order::date AS day,\n  COALESCE(SUM(pl.qty), 0)::numeric AS bags,")
    sql = sql.rstrip().rstrip(";") + "\nGROUP BY 1 ORDER BY 1"
    df = db.run_query(sql, {"start_date": HISTORY_START, "end_date": end.isoformat(),
                            "excluded": queries.excluded_products()})
    s = pd.Series(df["bags"].astype(float).values, index=pd.to_datetime(df["day"]))
    # Days with no till sales at all (Christmas, New Year) count as zero.
    return s.reindex(pd.date_range(HISTORY_START, end), fill_value=0.0)


def main():
    t0 = time.time()
    yesterday = date.today() - timedelta(days=1)
    s = daily_bags(yesterday)
    print(f"{len(s)} days of sales loaded")

    torch.set_num_threads(os.cpu_count() or 4)
    pipe = Chronos2Pipeline.from_pretrained("amazon/chronos-2", device_map="cpu")

    def forecast(upto, days):
        q, _ = pipe.predict_quantiles([torch.tensor(s[s.index <= upto].values)],
                                      prediction_length=days, quantile_levels=QUANTILES)
        return q[0][0].numpy()        # (days, 3) → lo, med, hi per day

    # ── This month ────────────────────────────────────────────────
    upto = pd.Timestamp(yesterday)
    dim = calendar.monthrange(upto.year, upto.month)[1]
    month = s[s.index >= upto.replace(day=1)]
    so_far = float(month.sum())
    q = forecast(upto, dim - upto.day)
    current = {
        "month_label": upto.strftime("%B %Y"),
        "data_to": upto.strftime("%d %b %Y"),
        "dim": dim, "day": upto.day, "so_far": round(so_far),
        "runrate": round(so_far * dim / upto.day),
        "lo": round(so_far + q[:, 0].sum()),
        "med": round(so_far + q[:, 1].sum()),
        "hi": round(so_far + q[:, 2].sum()),
        "actual_daily": [round(v) for v in month.values],
        "fc_daily": {k: [round(float(v)) for v in q[:, i]] for i, k in enumerate(["lo", "med", "hi"])},
    }

    # ── Track record ──────────────────────────────────────────────
    rows = []
    last = upto.to_period("M") - 1
    for m in pd.period_range(last - (BACKTEST_MONTHS - 1), last, freq="M"):
        start, mdim = m.start_time, m.days_in_month
        actual = float(s[(s.index >= start) & (s.index <= m.end_time)].sum())
        for dn in CHECK_DAYS:
            cut = start + pd.Timedelta(days=dn - 1)
            got = float(s[(s.index >= start) & (s.index <= cut)].sum())
            fq = forecast(cut, mdim - dn)
            rows.append({"month": start.strftime("%b %Y"), "day": dn, "actual": round(actual),
                         "rr": round(got * mdim / dn),
                         "ch": round(got + fq[:, 1].sum()),
                         "lo": round(got + fq[:, 0].sum()),
                         "hi": round(got + fq[:, 2].sum())})
        print(m, "tested")

    summary = []
    for dn in CHECK_DAYS:
        r = [x for x in rows if x["day"] == dn]
        err = lambda k: sum(abs(x[k] / x["actual"] - 1) for x in r) / len(r) * 100
        summary.append({"day": dn, "rr": round(err("rr"), 1), "ch": round(err("ch"), 1),
                        "wins": sum(abs(x["ch"] - x["actual"]) < abs(x["rr"] - x["actual"]) for x in r),
                        "hit": sum(x["lo"] <= x["actual"] <= x["hi"] for x in r),
                        "n": len(r)})

    data = {"generated": datetime.now().strftime("%d %b %Y %H:%M"),
            "current": current, "summary": summary, "months": rows}
    inject("CHRONOS_DATA", "CHRONOS", data)
    inject_train()
    print(f"chronos_preview.html written in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
