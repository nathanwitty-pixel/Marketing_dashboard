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
and opens the shell at http://127.0.0.1:8765/shell.html. The in-app Refresh
buttons re-run the relevant script on demand.

Requires, in this folder (none of them are committed):
- `.env` — the Odoo/Postgres connection (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`,
  `DB_PASSWORD`) and `SUPABASE_DB_URL`;
- `service_account.json` — Google Sheets access (see SETUP.md). The older OAuth
  login (`google_credentials.json` + `google_token.json`) still works as a fallback.

## Hosted version (Streamlit Cloud)
`streamlit_app.py` is the deployed app; its credentials live in Streamlit Cloud →
Settings → Secrets (see `.streamlit/secrets.toml.example`).
