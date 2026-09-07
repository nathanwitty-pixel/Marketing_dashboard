# Month-End Routine

At the end of every month, one command freezes that month's **numbers and the
report's written comments** into Supabase. The History page reads them back, so
the live **Monthly Report always shows only the newest month**, and every past
month — with its analysis — lives in **History**.

---

## Run it

Use the Python that has `psycopg2` (the dashboard's Anaconda Python):

```powershell
& "C:\ProgramData\anaconda3\python.exe" month_end.py
```

- Run it on (or just after) the **1st of the month** — it automatically targets
  the month that just ended (the month containing *yesterday*).
- To (re)archive a specific month, pin it:
  ```powershell
  $env:DENRI_REPORT_MONTH="2026-08"; & "C:\ProgramData\anaconda3\python.exe" month_end.py
  ```

Requires `SUPABASE_DB_URL` in `.env` — the Supabase **Session Pooler** connection
string (the direct host is IPv6-only and fails here).

---

## What it does

`month_end.py` runs in two phases (every step is **idempotent** — safe to re-run):

**Phase 1 — archive the target month (all pinned to that month):**

| # | Script | What it does |
|---|--------|--------------|
| 1 | `monthly_sales.py` · `weekly_sales.py` · `current_performance.py` · `forward_projections.py` | Rebuild the current-month view **pinned to the target month**, so `current_performance.html` holds *that* month's figures (the report reads from it). |
| 2 | `monthly_report.py` | Rebuilds the report and writes its snapshot — **metrics + comments** — into `monthly_report_history.json`. |
| 3 | `push_to_supabase.py` | Upserts every stored month into the `denri_mkt_*` tables (metrics **and comments**). |
| 4 | `history.py` | Re-reads Supabase into `history.html`. |

**Phase 2 — restore the live view (unpinned):** re-runs the current-month chain
so the dashboards return to **the month we are actually in** (e.g. September),
while the report stays on the archived month (August).

Pinning the target month also overrides `monthly_report.py`'s `FINALIZED_MONTHS`
freeze so a finalized month can be deliberately (re)built.

### Live vs. archive — how the current month and past months split
- **Live view — always the current month.** The dashboards *and* the monthly
  report show the month we are actually in (`lib/report_month.py` `live_*`), so a
  normal refresh on 1 Sep shows September (day 1) with live metrics. A live run
  rebuilds only the HTML — it does **not** write `monthly_report_history.json`.
- **Archive — completed months, at month-end.** `monthly_report.py` writes a
  month's snapshot to history.json **only when pinned** (`DENRI_REPORT_MONTH`),
  which is what `month_end.py` does. So History/Supabase holds finished months
  only; the current month lands there when you run `month_end.py` at month-end.
- After archiving, `month_end.py` restores the live current-month view (it re-runs
  the current-month chain **and** the report unpinned).

---

## The comments

The report's narrative — **The Bottom Line**, **The Insight**,
**Recommendations**, **Business Impact** across every section, plus the
executive summary and each timed-offer verdict — is captured automatically.

- `monthly_report.py` pulls the prose straight out of the rendered report
  (`_collect_comments`) into the snapshot's `comments` field, so the wording can
  never drift from what the report actually said.
- It is stored in Supabase as `denri_mkt_monthly.comments` (a `jsonb` list of
  `{section, label, type, text}` — the `section` is what places each note).
- On the **History page**, each comment is shown **directly under the charts of
  the section it belongs to** — Current Performance notes under the weekly chart,
  Offer Type notes under the offer charts, and so on (mirroring the monthly
  report's own layout), not in one separate block. The executive summary notes
  sit under the KPI tiles.

---

## Where the data lives

- **Supabase** (`denri_mkt_*` tables) — the durable store; the History page's
  only source.
- **History page** (`history.html`) — every archived month: numbers, charts,
  timed offers, and the per-section comments.
- **Timed offers** — each campaign stores its per-bag rows, the daily lift
  series, **and the week-by-week bags/day view** (`denri_mkt_timed_offer_weeks`,
  offer week flagged) — all rendered per campaign in History.
- **Self-made combos** — the staff CBR combos vs running combos split, stored as
  a summary row (`denri_mkt_self_made_summary`), the sold-combo lines
  (`denri_mkt_combo_sales`) and the full combo-request log
  (`denri_mkt_combo_requests` — CBR ref, shop, requester, state, Lloyd approval,
  price, sold units). Classified by the real CBR link (`combo_product_id`),
  rendered as Section 6 in both the Monthly Report and History. Requires SELECT on
  Odoo `pos_combo_request` (granted 2026-09-02).
- **Monthly Report** (`monthly_report.html`) — **only the latest month.** No
  dated `report_YYYY_month.html` archives are written any more (past months are
  in History). Old archive files that already exist can be deleted safely.

---

## Notes & gotchas

- **`FINALIZED_MONTHS`** (in `monthly_report.py`) marks months whose report is
  frozen. `month_end.py` pins the target month, which overrides the freeze for
  that run. After archiving a month for good, add its `YYYY-MM` to that set so
  routine dashboard refreshes don't rewrite it.
- **Session Pooler only.** If the push errors with a host/IPv6 message, confirm
  `SUPABASE_DB_URL` uses the Session/Pooler string.
- **Always pushed.** `push_to_supabase.py` now runs inside `main.py` (right after
  `monthly_report.py`, before `history.py`) and on the report/History page
  refreshes, so Supabase — and therefore History — is never behind the local
  snapshot. It no-ops safely when Supabase is unreachable. `month_end.py` still
  does its own pinned push as part of archiving.
- **Idempotent.** Every step upserts — re-running a month overwrites its row
  cleanly and never duplicates.

---

## Optional: schedule it

To run automatically, add a **Windows Task Scheduler** task:

- **Trigger:** Monthly, day **1**, ~06:00.
- **Action:** Start a program
  - Program: `C:\ProgramData\anaconda3\python.exe`
  - Arguments: `month_end.py`
  - Start in: `C:\Users\jonat\Desktop\Marketing_dashboard`

It will archive the month that just closed each time it fires.
