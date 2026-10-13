#!/usr/bin/env python3
"""
build_all.py
────────────────────────────────────────────────────────────────
Regenerate EVERY dashboard once (Odoo + the Google Sheet), without
starting the web server or opening a browser:

    python scripts/build_all.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # project root → lib/

# Never pop open a browser tab (the generators check this flag).
os.environ.setdefault("DENRI_LAUNCHER", "1")

# Reuse main.py's ordered SCRIPTS list + quota handling, but not its server.
import main

main.run_scripts()
