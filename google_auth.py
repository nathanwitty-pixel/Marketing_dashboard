"""
Shared Google Sheets authentication for every dashboard generator.

Two modes, tried in this order:

  1) SERVICE ACCOUNT  (recommended — permanent, no browser, never expires)
     Put the service-account key JSON next to this file as `service_account.json`
     and share the spreadsheet with the service account's email (Viewer).
     Refresh tokens / 7-day expiry no longer apply, so this never "expires or
     revokes" the way the OAuth desktop flow does.

  2) OAUTH DESKTOP FLOW  (fallback — interactive, for local/dev)
     Uses google_credentials.json + google_token.json. If the saved token is
     expired/revoked, it is discarded and a fresh browser login is triggered
     automatically instead of crashing.
"""

import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
_BASE = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(_BASE, "service_account.json")
CREDS_FILE = os.path.join(_BASE, "google_credentials.json")
TOKEN_FILE = os.path.join(_BASE, "google_token.json")


def get_gspread_client():
    import gspread

    # ── 1) Service account: permanent & non-interactive ───────────────────
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        from google.oauth2.service_account import Credentials as SACredentials
        creds = SACredentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return gspread.authorize(creds)

    # ── 2) OAuth desktop flow (self-healing) ──────────────────────────────
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.auth.exceptions import RefreshError

    if not os.path.exists(CREDS_FILE):
        raise FileNotFoundError(
            "No Google auth found. For a PERMANENT fix, add a service account key as "
            "'service_account.json' and share the sheet with its email. "
            "Otherwise add 'google_credentials.json' (OAuth desktop client)."
        )

    creds = None
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        got = False
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                got = True
            except RefreshError:
                # Expired or revoked → drop the dead token and re-consent.
                print("  google token expired/revoked — re-authorizing in the browser…")
                try:
                    os.remove(TOKEN_FILE)
                except OSError:
                    pass
                creds = None
        if not got:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return gspread.authorize(creds)
