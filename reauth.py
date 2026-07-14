"""
One-command Google re-authorization.

    python reauth.py

Deletes any stale google_token.json and opens a browser so you can sign in
again, saving a fresh token. Use this whenever the dashboards fail with:

    google.auth.exceptions.RefreshError: invalid_grant: Token has been expired or revoked.

Then run `python main.py` as usual.

NOTE: if you've set up a service account (service_account.json), you don't
need this at all — that auth never expires. See SETUP.md.
"""

import os
from google_auth import SERVICE_ACCOUNT_FILE, CREDS_FILE, TOKEN_FILE, get_gspread_client


def main():
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        print("service_account.json found — you're on a service account, which never expires.")
        print("No re-authorization needed. If reads still fail, make sure the spreadsheet is")
        print("shared (Viewer) with the service account's email.")
        return

    if not os.path.exists(CREDS_FILE):
        print("google_credentials.json is missing — can't re-authorize.")
        print("Add your OAuth desktop client as google_credentials.json (see SETUP.md),")
        print("or set up a service account for a permanent fix.")
        return

    if os.path.exists(TOKEN_FILE):
        try:
            os.remove(TOKEN_FILE)
            print("Removed stale google_token.json.")
        except OSError as e:
            print("Could not remove google_token.json:", e)
            return

    print("Opening your browser to sign in ...")
    try:
        get_gspread_client()   # no token present -> runs the interactive flow and saves a fresh one
    except Exception as e:
        print("Re-authorization failed:", e)
        return

    print("\nSuccess — a fresh google_token.json was saved.")
    print("You can now run:  python main.py")


if __name__ == "__main__":
    main()
