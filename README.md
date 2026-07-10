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

Requires `google_credentials.json` (OAuth desktop client) in this folder;
a `google_token.json` is created on first sign-in. **Neither file is committed.**

## Hosted version (Vercel)
The deployed site is a **static snapshot** of the last locally-generated data.
Python does not run on Vercel, so the Refresh buttons are inactive there.
To update the hosted numbers: run `python main.py` locally, then commit &
push the regenerated HTML.
