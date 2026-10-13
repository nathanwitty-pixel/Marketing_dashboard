"""
chronos_train.py
─────────────────────────────────────────────────────────────────
Experiment: can Chronos-2 forecast the month better if it (a) is told
about the calendar and (b) is fine-tuned on Denri's own shop sales?
Writes chronos_train_results.json, which chronos_preview.py shows as the
"Improved Chronos" section of chronos_preview.html.

Run with the Chronos venv (≈30 min on the laptop CPU):
    C:\\Users\\nate\\.venvs\\chronos\\Scripts\\python.exe chronos_train.py

Four ways of projecting the month, all tested on the same 12 finished
months on day 3/7/10/15/20/25, using only what was known that day:
  rr     straight line (today's method)
  base   Chronos-2 as downloaded, total sales only
  cal    + calendar inputs it knows in advance: Black Friday run-up,
           Christmas run-up, Kenyan public holidays, payday days
  tuned  + fine-tuned (LoRA) on every shop's daily sales and the total.
           Retrained each quarter on sales BEFORE that quarter only, so a
           test month never sees its own answers.
  shops  the tuned model forecasts each shop, and the shops are added up

Data: BAGS_SOLD_TOTAL grouped by day and till (pos_config) — the same
till-sales definition as chronos_preview.py. Corporate bags not included.
─────────────────────────────────────────────────────────────────
"""
import json
import os
import sys
import time
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
import torch
from chronos import Chronos2Pipeline

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root → lib/
from lib import db, queries

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "chronos_train_results.json" if not os.environ.get("CHRONOS_QUICK") else ".chronos_quick.json")
MODEL_DIR = os.path.join(os.path.expanduser("~"), "models", "chronos-denri")   # fine-tuned model, outside OneDrive
HISTORY_START = "2024-01-01"
CHECK_DAYS = [3, 7, 10, 15, 20, 25]
BACKTEST_MONTHS = 12
QUANTILES = [0.1, 0.5, 0.9]
MIN_SHOP_DAYS = 120          # a till needs this much history to be trained on / forecast on its own
FIT = dict(finetune_mode="lora", learning_rate=5e-5, num_steps=150, batch_size=8, context_length=512)
if os.environ.get("CHRONOS_QUICK"):      # smoke test: 1 month, 1 check day, 2 training steps
    BACKTEST_MONTHS, CHECK_DAYS, FIT["num_steps"] = 1, [7], 2
TMP_DIR = os.path.join(os.path.expanduser("~"), "models", "chronos-ft-tmp")

# ── Calendar inputs (known in advance) ─────────────────────────────
BLACK_FRIDAY = {2024: "2024-11-29", 2025: "2025-11-28", 2026: "2026-11-27", 2027: "2027-11-26"}
# Kenyan public holidays. Eid dates follow the moon and are the announced/expected dates.
HOLIDAYS = pd.to_datetime([
    "2024-01-01", "2024-03-29", "2024-04-01", "2024-04-10", "2024-05-01", "2024-06-01", "2024-06-17",
    "2024-10-10", "2024-10-20", "2024-12-12", "2024-12-25", "2024-12-26",
    "2025-01-01", "2025-03-31", "2025-04-18", "2025-04-21", "2025-05-01", "2025-06-01", "2025-06-06",
    "2025-10-10", "2025-10-20", "2025-12-12", "2025-12-25", "2025-12-26",
    "2026-01-01", "2026-03-20", "2026-04-03", "2026-04-06", "2026-05-01", "2026-05-27", "2026-06-01",
    "2026-10-10", "2026-10-20", "2026-12-12", "2026-12-25", "2026-12-26"])


def calendar_inputs(idx):
    idx = pd.DatetimeIndex(idx)
    to_bf = np.array([(d - pd.Timestamp(BLACK_FRIDAY[d.year])).days for d in idx])
    # 0 → 1 over the three weeks before Black Friday, held at 1 through Cyber Monday.
    black_friday = np.where((to_bf >= -21) & (to_bf <= 3), 1 - np.abs(np.minimum(to_bf, 0)) / 21, 0.0)
    xmas = np.where((idx.month == 12) & (idx.day <= 24), idx.day / 24, 0.0)
    return {"black_friday": black_friday.astype(float),
            "xmas": xmas.astype(float),
            "holiday": idx.isin(HOLIDAYS).astype(float),
            "payday": ((idx.day >= 25) | (idx.day <= 2)).astype(float)}


def daily_by_till(end):
    sql = queries.BAGS_SOLD_TOTAL.replace(
        "SELECT\n  COALESCE(SUM(pl.qty), 0)::numeric AS bags,",
        "SELECT p.date_order::date AS day, COALESCE(pc.\"name\", '?') AS shop,\n  COALESCE(SUM(pl.qty), 0)::numeric AS bags,")
    sql = sql.rstrip().rstrip(";") + "\nGROUP BY 1, 2 ORDER BY 1, 2"
    df = db.run_query(sql, {"start_date": HISTORY_START, "end_date": end.isoformat(),
                            "excluded": queries.excluded_products()})
    df["day"] = pd.to_datetime(df["day"])
    piv = df.pivot_table(index="day", columns="shop", values="bags", aggfunc="sum").astype(float)
    piv = piv.reindex(pd.date_range(HISTORY_START, end))
    return piv, piv.sum(axis=1).fillna(0.0)


def history(s, upto):
    """Series up to and including `upto`, from its first sale, gaps = 0."""
    s = s[s.index <= upto]
    first = s.first_valid_index()
    return s[first:].fillna(0.0) if first is not None else s.iloc[0:0]


def item(s, horizon=None, with_cal=True):
    d = {"target": s.values.astype(float)}
    if with_cal:
        d["past_covariates"] = calendar_inputs(s.index)
        if horizon:
            fut = pd.date_range(s.index[-1] + pd.Timedelta(days=1), periods=horizon)
            d["future_covariates"] = calendar_inputs(fut)
    return d


def quantiles(pipe, items, horizon):
    q, _ = pipe.predict_quantiles(items, prediction_length=horizon, quantile_levels=QUANTILES)
    return [x[0].numpy() for x in q]      # each (horizon, 3)


def active_tills(piv, upto):
    """Tills with enough history that also sold in the last 14 days."""
    recent = piv[(piv.index > upto - pd.Timedelta(days=14)) & (piv.index <= upto)]
    return [c for c in piv.columns
            if piv[c][piv.index <= upto].count() >= MIN_SHOP_DAYS and recent[c].fillna(0).sum() > 0]


def fine_tune(base, piv, total, before, out_dir=None):
    upto = before - pd.Timedelta(days=1)
    items = [item(history(total, upto))] + [item(history(piv[c], upto)) for c in active_tills(piv, upto)]
    t = time.time()
    ft = base.fit(items, prediction_length=31, output_dir=out_dir or TMP_DIR,
                  remove_printer_callback=True, report_to=[], save_strategy="no", logging_strategy="no",
                  disable_tqdm=True, **FIT)
    print(f"  fine-tuned on {len(items)} series to {upto.date()} in {time.time() - t:.0f}s", flush=True)
    return ft


def project(models, piv, total, upto, dim):
    """Month-end projection from each method, standing on `upto`."""
    start = upto.replace(day=1)
    got = float(total[(total.index >= start) & (total.index <= upto)].sum())
    h = dim - upto.day
    out = {"rr": got * dim / upto.day}
    hist = history(total, upto)
    (qb,) = quantiles(models["base"], [item(hist, with_cal=False)], h)
    (qc,) = quantiles(models["base"], [item(hist, h)], h)
    (qt,) = quantiles(models["tuned"], [item(hist, h)], h)
    for k, q in (("base", qb), ("cal", qc), ("tuned", qt)):
        out[k] = got + q[:, 1].sum()
        out[k + "_lo"], out[k + "_hi"] = got + q[:, 0].sum(), got + q[:, 2].sum()
    tills = active_tills(piv, upto)
    qs = quantiles(models["tuned"], [item(history(piv[c], upto), h) for c in tills], h)
    # Tills too new to forecast carry on at their pace so far this month.
    others = total - piv[tills].fillna(0).sum(axis=1)
    o_got = float(others[(others.index >= start) & (others.index <= upto)].sum())
    out["shops"] = got + sum(np.clip(q[:, 1], 0, None).sum() for q in qs) + o_got / upto.day * h
    return out, got, tills, qs


def main():
    t0 = time.time()
    torch.set_num_threads(os.cpu_count() or 4)
    yesterday = pd.Timestamp(date.today() - timedelta(days=1))
    piv, total = daily_by_till(yesterday.date())
    print(f"{len(total)} days, {piv.shape[1]} tills", flush=True)
    base = Chronos2Pipeline.from_pretrained("amazon/chronos-2", device_map="cpu")

    last = yesterday.to_period("M") - 1
    months = list(pd.period_range(last - (BACKTEST_MONTHS - 1), last, freq="M"))
    rows, tuned, tuned_for = [], None, None
    for m in months:
        q_start = pd.Period(year=m.year, quarter=m.quarter, freq="Q").start_time
        q_start = max(q_start, months[0].start_time)
        if tuned_for != q_start:
            print(f"training for {q_start.date()} onward", flush=True)
            tuned, tuned_for = fine_tune(base, piv, total, q_start), q_start
        models = {"base": base, "tuned": tuned}
        start, dim = m.start_time, m.days_in_month
        actual = float(total[(total.index >= start) & (total.index <= m.end_time)].sum())
        for dn in CHECK_DAYS:
            p, *_ = project(models, piv, total, start + pd.Timedelta(days=dn - 1), dim)
            rows.append({"month": start.strftime("%b %Y"), "day": dn, "actual": round(actual),
                         **{k: round(v) for k, v in p.items()}})
        print(f"{m} tested ({time.time() - t0:.0f}s)", flush=True)

    methods = ["rr", "base", "cal", "tuned", "shops"]
    summary = []
    for dn in CHECK_DAYS:
        r = [x for x in rows if x["day"] == dn]
        s = {"day": dn, "n": len(r)}
        for k in methods:
            s[k] = round(sum(abs(x[k] / x["actual"] - 1) for x in r) / len(r) * 100, 1)
        s["tuned_hit"] = sum(x["tuned_lo"] <= x["actual"] <= x["tuned_hi"] for x in r)
        summary.append(s)

    # ── This month, with a model trained on everything to yesterday ──
    print("training on all sales for this month's forecast", flush=True)
    final = fine_tune(base, piv, total, yesterday + pd.Timedelta(days=1), out_dir=MODEL_DIR)
    final.save_pretrained(MODEL_DIR)
    dim = yesterday.days_in_month
    p, got, tills, qs = project({"base": base, "tuned": final}, piv, total, yesterday, dim)
    start = yesterday.replace(day=1)
    prev = (start - pd.Timedelta(days=1)).to_period("M")
    shops = []
    for c, q in zip(tills, qs):
        sofar = float(piv[c][(piv.index >= start) & (piv.index <= yesterday)].fillna(0).sum())
        last_m = float(piv[c][(piv.index >= prev.start_time) & (piv.index <= prev.end_time)].fillna(0).sum())
        shops.append({"shop": c, "so_far": round(sofar), "last_month": round(last_m),
                      "med": round(sofar + np.clip(q[:, 1], 0, None).sum()),
                      "lo": round(sofar + np.clip(q[:, 0], 0, None).sum()),
                      "hi": round(sofar + np.clip(q[:, 2], 0, None).sum())})
    shops.sort(key=lambda x: -x["med"])

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"generated": datetime.now().strftime("%d %b %Y %H:%M"),
                   "data_to": yesterday.strftime("%d %b %Y"), "month_label": yesterday.strftime("%B %Y"),
                   "current": {k: round(v) for k, v in p.items()}, "so_far": round(got),
                   "summary": summary, "months": rows, "shops": shops,
                   "fit": FIT, "minutes": round((time.time() - t0) / 60, 1)}, f)
    print(f"written {OUT} in {(time.time() - t0) / 60:.1f} min")
    if not os.environ.get("CHRONOS_QUICK"):
        from chronos_preview import inject_train
        inject_train()
        print("chronos_preview.html updated")


if __name__ == "__main__":
    main()
