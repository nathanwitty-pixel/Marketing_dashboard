#!/usr/bin/env python3
"""
Denri Africa — Marketing Dashboard Launcher
============================================
Run this file to refresh all dashboards and open them in your browser.

    python main.py

Press Ctrl+C to stop the server.
"""
import os
import sys
import json
import subprocess
import threading
import time
import webbrowser
import http.server
import socketserver
from datetime import date
from urllib.parse import urlparse, parse_qs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT     = 8765

SCRIPTS = [
    ("Current Performance",    "current_performance.py"),
    ("Forward Projections",    "forward_projections.py"),
    ("New Products Analytics", "new_products.py"),
    ("Timed Offers Analytics", "timed_offers.py"),
    ("Bags Selection Analytics", "bags_selection.py"),
    ("Offer Type Analysis",    "offer_type_analysis.py"),
    ("Posting Yields",         "POSTING (SALES YIELDS FROM ACCURATE POSTING).py"),
    ("Shops Efficiency",       "shops_efficiency.py"),
    # Must run LAST — reads the data the scripts above injected
    ("Dashboard Insights",     "generate_insights.py"),
]


# Seconds to pause between scripts so we stay under the Google Sheets
# read-request quota (60 reads/min/user). A short gap spreads the calls out.
SCRIPT_GAP = 8
# When a 429 quota error hits, wait this long for the per-minute window to
# reset, then retry the script once.
QUOTA_WAIT = 65


def _run_one(path):
    return subprocess.run(
        [sys.executable, path],
        cwd=BASE_DIR,
        timeout=120,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        env={**os.environ, "PYTHONIOENCODING": "utf-8", "DENRI_LAUNCHER": "1"},
    )


def _is_quota_error(result):
    blob = (result.stderr or "") + (result.stdout or "")
    return "429" in blob or "Quota exceeded" in blob or "RATE_LIMIT" in blob


def run_scripts():
    print("\n  Refreshing dashboards... (each can take up to 2 minutes — please wait)\n", flush=True)
    for i, (label, script) in enumerate(SCRIPTS):
        path = os.path.join(BASE_DIR, script)
        if not os.path.exists(path):
            print(f"    - {label:32s} (script not found, skipped)")
            continue
        print(f"    > {label:32s}", end=" ", flush=True)
        try:
            result = _run_one(path)

            # Retry once if we hit the Sheets read quota
            if result.returncode != 0 and _is_quota_error(result):
                print(f"quota hit, waiting {QUOTA_WAIT}s to retry...", end=" ", flush=True)
                time.sleep(QUOTA_WAIT)
                result = _run_one(path)

            if result.returncode == 0:
                print("OK", flush=True)
            else:
                err = result.stderr.strip().splitlines()
                short = err[-1][:100] if err else "unknown error"
                print(f"FAIL  {short}", flush=True)
        except subprocess.TimeoutExpired:
            print("FAIL  timed out after 120 s", flush=True)
        except Exception as exc:
            print(f"FAIL  {exc}", flush=True)

        # Space out API calls to avoid tripping the per-minute quota
        if i < len(SCRIPTS) - 1:
            time.sleep(SCRIPT_GAP)
    print()


def _offer_active_today():
    """True if a timed-offer window is set and today falls inside it."""
    cfg_path = os.path.join(BASE_DIR, "timed_offers_config.json")
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        start, end = raw.get("startDate", ""), raw.get("endDate", "")
        if start and end:
            return date.fromisoformat(start) <= date.today() <= date.fromisoformat(end)
    except (ValueError, OSError):
        pass
    return False


def start_daily_snapshot():
    """Once per calendar day, while an offer window is active, re-run
    timed_offers.py so it records that day's shop-scoped snapshot. Runs in the
    background for as long as the dashboard server is up (records only on days
    the dashboard is left running — see SETUP.md for the always-on option)."""
    to_py = os.path.join(BASE_DIR, "timed_offers.py")
    last_date = date.today()   # startup run_scripts() already recorded today
    while True:
        time.sleep(1800)       # check twice an hour so a day-rollover is caught promptly
        today = date.today()
        if today != last_date and os.path.exists(to_py) and _offer_active_today():
            try:
                subprocess.run(
                    [sys.executable, to_py], cwd=BASE_DIR, timeout=120,
                    capture_output=True, text=True, encoding='utf-8', errors='replace',
                    env={**os.environ, "PYTHONIOENCODING": "utf-8", "DENRI_LAUNCHER": "1"},
                )
                print(f"  (timed-offer snapshot recorded for {today.isoformat()})", flush=True)
            except Exception:
                pass
        last_date = today


# Scripts to run when the Refresh button is used on each page.
# current_performance.html holds BOTH the PERF and PROJ data blocks, so its
# refresh also re-runs forward_projections.py — this picks up manual edits
# to corporate_bags / bare_minimum at the top of that script.
SCRIPT_MAP = {
    "current_performance.html":                             ["current_performance.py",
                                                             "forward_projections.py"],
    "forward_projections.html":                             ["forward_projections.py"],
    "new_products.html":                                    ["new_products.py"],
    "timed_offers.html":                                    ["timed_offers.py"],
    "bags_selection.html":                                  ["bags_selection.py"],
    "offer_type_analysis.html":                             ["offer_type_analysis.py"],
    "POSTING (SALES YIELDS FROM ACCURATE POSTING).html":   ["POSTING (SALES YIELDS FROM ACCURATE POSTING).py"],
    "shops_efficiency.html":                                ["shops_efficiency.py"],
    "insights.html":                                        ["generate_insights.py"],
}


def start_server():
    os.chdir(BASE_DIR)

    class DashHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def end_headers(self):
            # Never let the browser cache dashboard HTML — always serve fresh data
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
            super().end_headers()

        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path == "/api/refresh":
                self._handle_refresh(parse_qs(parsed.query))
            elif parsed.path == "/api/timed-offers-config":
                self._handle_to_config(parse_qs(parsed.query))
            else:
                super().do_GET()

        def _handle_to_config(self, params):
            """GET (no params) → return the current timed-offer config.
            GET with save=1&shops=..&start=..&end=.. → write it + re-run the
            generator so the page reflects the new shops/window immediately."""
            cfg_path = os.path.join(BASE_DIR, "timed_offers_config.json")
            if params.get("save"):
                shops_raw = params.get("shops", ["ALL"])[0].strip()
                start = params.get("start", [""])[0].strip()
                end   = params.get("end", [""])[0].strip()
                shops = "ALL" if (not shops_raw or shops_raw.upper() == "ALL") \
                    else [s.strip() for s in shops_raw.split(",") if s.strip()]
                cfg = {
                    "_help": ("shops: \"ALL\" or a list of shop names exactly as in the "
                              "sheet headers. startDate/endDate: YYYY-MM-DD; snapshots "
                              "record only while today is inside this window."),
                    "shops": shops, "startDate": start, "endDate": end,
                }
                try:
                    with open(cfg_path, "w", encoding="utf-8") as f:
                        json.dump(cfg, f, indent=2)
                except OSError as exc:
                    self._json(500, {"ok": False, "error": str(exc)})
                    return
                # Re-run the generator so the injected data + snapshot update now.
                to_py = os.path.join(BASE_DIR, "timed_offers.py")
                try:
                    result = subprocess.run(
                        [sys.executable, to_py], cwd=BASE_DIR, timeout=90,
                        capture_output=True, text=True, encoding='utf-8', errors='replace',
                        env={**os.environ, "PYTHONIOENCODING": "utf-8", "DENRI_LAUNCHER": "1"},
                    )
                    if result.returncode != 0:
                        lines = result.stderr.strip().splitlines()
                        msg = lines[-1][:200] if lines else "unknown error"
                        self._json(500, {"ok": False, "error": f"timed_offers.py: {msg}"})
                        return
                except subprocess.TimeoutExpired:
                    self._json(500, {"ok": False, "error": "timed_offers.py timed out after 90s"})
                    return
                except Exception as exc:
                    self._json(500, {"ok": False, "error": str(exc)})
                    return
                self._json(200, {"ok": True})
                return
            # No save → return current config
            cfg = {"shops": "ALL", "startDate": "", "endDate": ""}
            if os.path.exists(cfg_path):
                try:
                    with open(cfg_path, "r", encoding="utf-8") as f:
                        raw = json.load(f)
                    cfg = {"shops": raw.get("shops", "ALL"),
                           "startDate": raw.get("startDate", ""),
                           "endDate": raw.get("endDate", "")}
                except (ValueError, OSError):
                    pass
            self._json(200, {"ok": True, "config": cfg})

        def _handle_refresh(self, params):
            html_file = params.get("dashboard", [None])[0]
            scripts = SCRIPT_MAP.get(html_file) if html_file else None

            if not scripts:
                self._json(400, {"ok": False, "error": "Unknown dashboard"})
                return

            for script in scripts:
                script_path = os.path.join(BASE_DIR, script)
                if not os.path.exists(script_path):
                    self._json(404, {"ok": False, "error": f"Script not found: {script}"})
                    return
                try:
                    result = subprocess.run(
                        [sys.executable, script_path],
                        cwd=BASE_DIR,
                        timeout=90,
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        errors='replace',
                        env={**os.environ, "PYTHONIOENCODING": "utf-8", "DENRI_LAUNCHER": "1"},
                    )
                    if result.returncode != 0:
                        lines = result.stderr.strip().splitlines()
                        msg = lines[-1][:200] if lines else "unknown error"
                        self._json(500, {"ok": False, "error": f"{script}: {msg}"})
                        return
                except subprocess.TimeoutExpired:
                    self._json(500, {"ok": False, "error": f"{script} timed out after 90s"})
                    return
                except Exception as exc:
                    self._json(500, {"ok": False, "error": str(exc)})
                    return

            self._json(200, {"ok": True})

        def _json(self, code, data):
            body = json.dumps(data).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    socketserver.TCPServer.allow_reuse_address = True
    # Bind to all interfaces so colleagues on the same network can open
    # the dashboard from their own machines
    with socketserver.TCPServer(("0.0.0.0", PORT), DashHandler) as httpd:
        httpd.serve_forever()


def get_lan_ip():
    """This machine's address on the local network (for the share URL)."""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))   # no traffic sent — just picks the route
            return s.getsockname()[0]
    except Exception:
        return None


FIREWALL_RULE = "Denri Marketing Dashboard 8765"

def ensure_firewall_rule():
    """Allow inbound connections to the dashboard port. Needs admin the
    first time; if that fails, Windows will show its own allow prompt or
    the rule can be added manually."""
    try:
        show = subprocess.run(
            ["netsh", "advfirewall", "firewall", "show", "rule", f"name={FIREWALL_RULE}"],
            capture_output=True, text=True, timeout=10,
        )
        if show.returncode == 0:
            return True   # rule already exists
        add = subprocess.run(
            ["netsh", "advfirewall", "firewall", "add", "rule",
             f"name={FIREWALL_RULE}", "dir=in", "action=allow",
             "protocol=TCP", f"localport={PORT}"],
            capture_output=True, text=True, timeout=10,
        )
        return add.returncode == 0
    except Exception:
        return False


def free_port(port):
    """Stop any previous dashboard server still holding the port, so the
    fresh server (with no-cache headers and /api/refresh) can bind."""
    import socket
    try:
        with socket.socket() as s:
            s.settimeout(0.3)
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return  # port already free
    except Exception:
        return

    try:
        out = subprocess.run(
            ["netstat", "-ano", "-p", "TCP"],
            capture_output=True, text=True, timeout=10,
        ).stdout
        me = str(os.getpid())
        for line in out.splitlines():
            parts = line.split()
            if (len(parts) >= 5 and parts[1].endswith(f":{port}")
                    and parts[3] == "LISTENING" and parts[4] != me):
                subprocess.run(["taskkill", "/PID", parts[4], "/F"],
                               capture_output=True, text=True)
                print(f"  (stopped previous dashboard server, pid {parts[4]})")
        time.sleep(0.5)
    except Exception:
        pass


if __name__ == "__main__":
    print("\n" + "=" * 52)
    print("  Denri Africa · Marketing Dashboard")
    print("=" * 52)

    try:
        # Make sure no stale server from a previous run is holding the port
        free_port(PORT)

        # Start server in background while scripts run
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        time.sleep(0.5)  # give server a moment to bind

        # Refresh all dashboard data before opening browser
        run_scripts()

        # Record a timed-offer snapshot once a day while the server is running
        threading.Thread(target=start_daily_snapshot, daemon=True).start()

        url = f"http://127.0.0.1:{PORT}/shell.html"
        print(f"  Server running at {url}")

        # Network sharing: show the URL colleagues on the same LAN can open
        lan_ip = get_lan_ip()
        if lan_ip:
            fw_ok = ensure_firewall_rule()
            print(f"  Share on your network: http://{lan_ip}:{PORT}/shell.html")
            if not fw_ok:
                print("    (if others can't connect, allow Python through the")
                print("     Windows Firewall prompt, or run this once as admin:")
                print(f'     netsh advfirewall firewall add rule name="{FIREWALL_RULE}"'
                      f' dir=in action=allow protocol=TCP localport={PORT})')

        print("  Press Ctrl+C to stop.\n", flush=True)
        webbrowser.open(url)

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  Stopped.")
