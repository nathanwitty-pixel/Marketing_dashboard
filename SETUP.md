# Marketing Dashboard — Google Sheets access & setup

The dashboard reads one Google Spreadsheet and bakes the numbers into the HTML
pages. All authentication lives in **`google_auth.py`** (shared by every
generator script). It supports two modes, tried in this order:

1. **Service account** (`service_account.json`) — *recommended, permanent.*
2. **OAuth desktop login** (`google_credentials.json` + `google_token.json`) — interactive fallback.

---

## Symptom: "invalid_grant: Token has been expired or revoked"

This means the OAuth token died. It happens on a schedule when the OAuth app is
in **Testing** mode (Google expires those tokens every ~7 days).

### Quick fix (re-login) — 30 seconds
```
python reauth.py        # opens a browser, sign in, saves a fresh token
python main.py          # dashboards refresh normally
```

### Stop it recurring
Google Cloud Console → **APIs & Services → OAuth consent screen → Publish app**
(move it from *Testing* to *In production*). That removes the 7-day expiry for
the login-based flow.

---

## Permanent, zero-maintenance fix — Service account (recommended)

A service account never expires and needs **no browser** — so it also makes the
in-dashboard **Refresh button** work (that runs the scripts server-side, where a
login flow can't open).

1. Google Cloud Console → your project → **APIs & Services → Credentials →
   Create credentials → Service account**. Name it (e.g. `dashboard-reader`) → Create → Done.
2. Open the service account → **Keys → Add key → Create new key → JSON** → download.
3. Save the downloaded file as **`service_account.json`** in this folder.
4. Copy the service account's **email** (e.g. `dashboard-reader@yourproject.iam.gserviceaccount.com`).
5. Open the Google Sheet → **Share** → paste that email → **Viewer** → Send.
6. Make sure **Google Sheets API** is enabled for the project.
7. Run `python main.py`. It auto-detects `service_account.json`. No login, no expiry.

No code changes are needed after adding the file.

---

## Running

```
python main.py          # refreshes every page, then serves the dashboard
```

---

## Timed Offers — snapshots over a window

Set the campaign on the **Timed Offers** page (the "Offer Window" card): pick
**All shops** or **Specific**, choose a **start / end date**, and hit
**Save & apply**. This writes `timed_offers_config.json` and records a snapshot
(sales + stock + posts, scoped to the chosen shops) for that day.

While `python main.py` is running, it **auto-records one snapshot per day** for
as long as the offer window is active — so the timeline fills itself in without
you refreshing. It only records on days the dashboard is left running.

## Auto-deploy the moment the sheet changes (event-driven)

Beyond the schedule, the spreadsheet can **ping GitHub the instant its data
changes**, so Vercel updates on its own with no clicking. The workflow already
listens for this (`repository_dispatch: sheet-updated`); you just wire up the
sheet once.

Full code + steps are in **`sheet_trigger.gs`**. In short:

1. **GitHub fine-grained token** (Settings → Developer settings → Fine-grained
   tokens): repository access = *Marketing_dashboard* only; permission
   *Contents: Read and write*. Copy it.
2. **Spreadsheet → Extensions → Apps Script.** Paste in `sheet_trigger.gs`.
3. **Project Settings → Script properties:** add `GH_TOKEN` = the token.
4. **Run `setup` once** (authorize when asked). It installs a trigger that
   checks every 5 minutes and pings GitHub *only when the sheet actually
   changed* — so CI runs only on real changes, not on a fixed clock.

The 2-hour schedule stays on as a safety net. Latency is up to ~5 min; lower the
`everyMinutes(5)` in `setup` to `everyMinutes(1)` if you want it snappier.

---

### Always-on option (records even when the dashboard is closed)
Use Windows **Task Scheduler** to run the generator once a day:

1. Task Scheduler → **Create Basic Task** → name it "Timed Offer Snapshot".
2. Trigger: **Daily**, pick a time (e.g. 8:00 pm).
3. Action: **Start a program** →
   - Program/script: `python`
   - Arguments: `timed_offers.py`
   - Start in: this folder's full path.
4. Finish. It now records a snapshot each day the PC is on, window permitting.

## Live data on Vercel — the build reads the sheet (git stays code)

The deployed site's data is **produced by Vercel's build**, not committed to the
repo. On each deploy Vercel runs the generators (`vercel.json` →
`python3 build_all.py`), reads the Google Sheet, and serves the rendered HTML
from `dist/`. So **git holds the code + a little trend-history state — not baked
data**, and the `.py`/JSON/secrets are never served (only `dist/*.html` is).

Two moving parts:

- **Vercel build** renders the live HTML from the sheet on every deploy.
- **GitHub Action** (`.github/workflows/refresh.yml`) runs on the sheet's event
  (+ a 2-hour safety net), advances the accumulating **trend history** (small
  JSON, committed — trends can't be re-derived from one read), then **pings the
  Vercel Deploy Hook** so the live render refreshes immediately.

### One-time setup
1. **Service-account key JSON** (Google Cloud → the service account →
   Keys → Add key → JSON). Share the spreadsheet (**Viewer**) with its email.
2. **GitHub secret:** repo → Settings → Secrets and variables → Actions →
   `SERVICE_ACCOUNT_JSON` = the entire key JSON.
3. **Vercel env var:** Vercel → Project → Settings → **Environment Variables** →
   add `SERVICE_ACCOUNT_JSON` = the **same** key JSON (Production + Preview). The
   build reads it straight from the env — no key file is ever written or served.
4. **Vercel build settings** (usually auto-applied from `vercel.json`): Framework
   preset **Other**, Build Command `python3 -m pip install -r requirements.txt &&
   python3 build_all.py && rm -rf dist && mkdir dist && cp *.html dist/`, Output
   Directory `dist`. Check the first deploy's build log shows Python running.
5. **Vercel Deploy Hook:** Vercel → Settings → Git → **Deploy Hooks** → create
   one on `main` → copy the URL → add as GitHub secret `VERCEL_DEPLOY_HOOK`.
   (Optional: turn OFF Vercel's automatic git deploys so the hook is the single
   trigger and you don't get double builds.)
6. **Push & test:** commit/push, then Actions → Run workflow → watch it green →
   the live site rebuilds from the sheet.

Run everything headlessly yourself any time with `python build_all.py`
(uses `service_account.json` locally, or your browser login).

---

## Secrets — never commit / deploy these
`google_credentials.json`, `google_token.json`, and `service_account.json` are
listed in `.gitignore` and `.vercelignore`. Keep real keys only on the machine
that runs the refresh; never paste them into code.
