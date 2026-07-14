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

## Secrets — never commit / deploy these
`google_credentials.json`, `google_token.json`, and `service_account.json` are
listed in `.gitignore` and `.vercelignore`. Keep real keys only on the machine
that runs the refresh; never paste them into code.
