#!/usr/bin/env python3
"""
build_all.py
────────────────────────────────────────────────────────────────
Regenerate EVERY dashboard from Google Sheets once, without starting
the web server or opening a browser.

Used by CI (.github/workflows/refresh.yml): the workflow authenticates
with the service account, runs this, and commits the freshly-baked HTML —
which Vercel then auto-deploys.

You can also run it locally to refresh all pages headlessly:

    python build_all.py
"""
import os

# Never pop open a browser tab (the generators check this flag).
os.environ.setdefault("DENRI_LAUNCHER", "1")

# Reuse main.py's ordered SCRIPTS list + quota handling, but not its server.
import main

main.run_scripts()
