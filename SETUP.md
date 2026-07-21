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

## Auto-refresh the deployed (Vercel) site from the sheet

The Vercel site is **static** — it shows whatever numbers were baked in the last
time the generators ran. To keep the deployed site fresh **without running
anything locally**, a GitHub Action (`.github/workflows/refresh.yml`) re-reads
the sheet, regenerates the HTML, and commits it — and Vercel auto-deploys the
commit.

- **Automatic:** runs on a schedule (default every 2 hours; edit the `cron` line).
- **On demand:** GitHub repo → **Actions** tab → *Refresh dashboard from Google
  Sheets* → **Run workflow**. ~2–3 min later the live site is updated.

### One-time setup
1. **Service account key.** In Google Cloud Console open the service account you
   already use (e.g. `marketing-and-predictive-sales@…`) → **Keys → Add key →
   Create new key → JSON** → download. (CI can't use the browser login.)
2. **Share the sheet with it.** The dashboard spreadsheet must be shared
   (**Viewer**) with that service account's email.
3. **Push the code.** Commit & push this repo (including `requirements.txt`,
   `build_all.py`, and `.github/workflows/refresh.yml`).
4. **Add the secret.** Repo → **Settings → Secrets and variables → Actions → New
   repository secret** → name `SERVICE_ACCOUNT_JSON`, value = the **entire**
   contents of the downloaded key file.
5. **Vercel deploy trigger.** If your Vercel project is linked to this GitHub
   repo (Vercel → Project → Settings → Git), the push auto-deploys — done. If it
   is **not** linked, create a Vercel **Deploy Hook** and add its URL as a second
   secret named `VERCEL_DEPLOY_HOOK`.
6. **Test it.** Actions tab → Run workflow → watch it go green → check the site.

Run all generators headlessly yourself any time with `python build_all.py`.

---

## Secrets — never commit / deploy these
`google_credentials.json`, `google_token.json`, and `service_account.json` are
listed in `.gitignore` and `.vercelignore`. Keep real keys only on the machine
that runs the refresh; never paste them into code.
