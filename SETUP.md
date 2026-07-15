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

### Always-on option (records even when the dashboard is closed)
Use Windows **Task Scheduler** to run the generator once a day:

1. Task Scheduler → **Create Basic Task** → name it "Timed Offer Snapshot".
2. Trigger: **Daily**, pick a time (e.g. 8:00 pm).
3. Action: **Start a program** →
   - Program/script: `python`
   - Arguments: `timed_offers.py`
   - Start in: this folder's full path.
4. Finish. It now records a snapshot each day the PC is on, window permitting.

## Secrets — never commit / deploy these
`google_credentials.json`, `google_token.json`, and `service_account.json` are
listed in `.gitignore` and `.vercelignore`. Keep real keys only on the machine
that runs the refresh; never paste them into code.
