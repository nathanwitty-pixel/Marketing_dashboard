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

## Run locally (full, live data)
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
