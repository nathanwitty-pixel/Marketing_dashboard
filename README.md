# Denri Africa · Marketing Dashboard

Internal marketing analytics dashboard. Reads live data from Google Sheets,
injects it into HTML dashboards, and serves them through a unified shell.

## Dashboards
- **Current Performance** + Forward Projections
- **New Products** Analytics
- **Offer Type Analysis**
- **Posting** — Sales Yields from Accurate Posting
- **Shops Efficiency** Tracking (per-shop + per-region)
- **Insights** — auto-generated summary

## Where things live
```
streamlit_app.py      the dashboard (Streamlit Cloud runs this)
main.py               local fallback: runs every generator, serves html/shell.html
dashboard_pages.json  the ONE page list (menu, page → html file + generator scripts)
publish.bat           double-click to check + publish (runs scripts/publish.py)
generators/           one script per page: pulls Odoo / Sheets data, writes it into html/ and data/
html/                 the dashboard pages (+ shell.html, the local frame)
assets/               shared JS/CSS the pages load (theme, chart switcher, sidebar, …)
data/                 inputs, configs, snapshots and history (.json / .csv / .txt / .xlsx)
lib/                  shared Python (DB, queries, Google auth, paths.py, …)
sql/  migrations/     queries and the Supabase migration
scripts/              tools: build_all, publish, month_end, reauth, product_targets_workbook
tests/                pytest suite  (python -m pytest tests -q)
docs/                 one spec per page + docs/README.md
notes/                working notes (Ralph tasks, progress logs, month-end runbook)
archive/              old reports, previews and one-off scripts, kept for reference
```
In Python, build file paths with `lib/paths.py` (`paths.data("x.json")`, `paths.html("x.html")`, …),
never from `__file__`. Pages load shared scripts as `../assets/<name>.js`.

## Which version is real
The dashboard is the **Streamlit app**: run `streamlit_app.py` locally (VS Code ▶ or double-click — it starts `streamlit run` itself); Streamlit
Cloud runs the same `streamlit_app.py` from GitHub `main`. To put local changes online,
double-click `publish.bat` (checks → shows changes → asks → commits + pushes). Pages are listed
once, in `dashboard_pages.json`. Details: [docs/README.md › Where changes go](docs/README.md#where-changes-go).

## Run locally (full, live data) — fallback shell
```
python main.py
```
Runs all data scripts (fetching from Google Sheets), starts a local server,
and opens the shell at http://127.0.0.1:8765/html/shell.html. The in-app Refresh
buttons re-run the relevant script on demand.

Requires, in the project root (none of them are committed):
- `.env` — the Odoo/Postgres connection (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`,
  `DB_PASSWORD`) and `SUPABASE_DB_URL`;
- `service_account.json` — Google Sheets access (see SETUP.md). The older OAuth
  login (`google_credentials.json` + `google_token.json`) still works as a fallback.

## Hosted version (Streamlit Cloud)
`streamlit_app.py` is the deployed app; its credentials live in Streamlit Cloud →
Settings → Secrets (see `.streamlit/secrets.toml.example`).
