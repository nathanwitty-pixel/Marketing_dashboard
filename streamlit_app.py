"""
streamlit_app.py — Denri Marketing Dashboard on Streamlit.

Serves the existing dashboard HTML pages inside a Streamlit shell (sidebar nav),
and — because Streamlit is a live Python server — the Refresh button re-runs that
page's generators against Odoo/Sheets and re-renders instantly. No GitHub Actions,
no redeploys, and nothing generated has to be committed (so no merge conflicts).

Deploy: Streamlit Community Cloud → point it at this repo, main file = streamlit_app.py.
Secrets (Cloud → Settings → Secrets), TOML — see .streamlit/secrets.toml.example:
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
    SUPABASE_DB_URL
    SERVICE_ACCOUNT_JSON   (the whole Google service-account key, as one string)
"""
import os
import sys
import subprocess
import datetime

import streamlit as st
import streamlit.components.v1 as components

BASE = os.path.dirname(os.path.abspath(__file__))


# ── Secrets → environment, so lib/db.py and google_auth.py work unchanged ──
def _load_secrets_into_env():
    try:
        secrets = st.secrets
    except Exception:
        secrets = {}
    for key in ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD",
                "DATABASE_URL", "SUPABASE_DB_URL", "SERVICE_ACCOUNT_JSON"):
        try:
            if key in secrets and secrets[key] not in (None, ""):
                os.environ[key] = str(secrets[key])
        except Exception:
            pass
    os.environ.setdefault("DENRI_LAUNCHER", "1")     # never try to open a browser
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

_load_secrets_into_env()


# ── Pages: label → HTML file → the generators that build it (mirrors SCRIPT_MAP) ──
PAGES = [
    ("Current Performance",           "current_performance.html",
        ["weekly_sales.py", "monthly_sales.py", "current_performance.py", "forward_projections.py"]),
    ("Forward Projections",           "forward_projections.html",
        ["forward_projections.py"]),
    ("New Products",                  "new_products.html",
        ["new_products.py"]),
    ("Timed Offers",                  "timed_offers.html",
        ["timed_offers.py"]),
    ("Self-made vs Running Combos",   "self_made_combos.html",
        ["self_made_combos.py"]),
    ("Posting Yields",                "POSTING (SALES YIELDS FROM ACCURATE POSTING).html",
        ["POSTING (SALES YIELDS FROM ACCURATE POSTING).py"]),
    ("Shops Efficiency",              "shops_efficiency.html",
        ["shops_dispatch.py", "shops_efficiency.py"]),
    ("Insights",                      "insights.html",
        ["generate_insights.py"]),
    ("Monthly Report",                "monthly_report.html",
        ["monthly_report.py"]),
    ("History",                       "history.html",
        ["history.py"]),
]

st.set_page_config(page_title="Denri · Marketing Dashboard",
                   page_icon="📊", layout="wide",
                   initial_sidebar_state="expanded")

# Trim Streamlit chrome so the embedded dashboard fills the width.
st.markdown("""
<style>
  #MainMenu, footer, header {visibility: hidden;}
  .block-container {padding: 0.4rem 0.6rem 0 0.6rem; max-width: 100%;}
  section[data-testid="stSidebar"] {background: #0b0d16;}
</style>
""", unsafe_allow_html=True)


def run_scripts(scripts):
    """Run a page's generators as subprocesses (same as main.py). Returns a list
    of (script, returncode, tail-of-output)."""
    env = {**os.environ, "DENRI_LAUNCHER": "1", "PYTHONIOENCODING": "utf-8"}
    logs = []
    for s in scripts:
        try:
            r = subprocess.run(
                [sys.executable, os.path.join(BASE, s)],
                cwd=BASE, env=env, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=240,
            )
            logs.append((s, r.returncode, (r.stderr or r.stdout or "").strip()[-600:]))
        except subprocess.TimeoutExpired:
            logs.append((s, -1, "timed out after 240s"))
        except Exception as e:                                    # noqa: BLE001
            logs.append((s, -1, str(e)))
    return logs


# ── Sidebar: brand + nav + refresh ──
st.sidebar.markdown("### Denri Africa")
st.sidebar.caption("Marketing Analytics")

labels = [p[0] for p in PAGES]
choice = st.sidebar.radio("Dashboard", labels, label_visibility="collapsed")
label, html_file, scripts = next(p for p in PAGES if p[0] == choice)
html_path = os.path.join(BASE, html_file)

if st.sidebar.button("🔄 Refresh this page from Odoo", use_container_width=True, type="primary"):
    with st.spinner(f"Refreshing {label} from Odoo… (a few seconds)"):
        logs = run_scripts(scripts)
    if all(rc == 0 for _, rc, _ in logs):
        st.sidebar.success("Refreshed with live data.")
    else:
        st.sidebar.error("Some steps failed:")
        for s, rc, out in logs:
            if rc != 0:
                st.sidebar.caption(f"⚠ {s}: {out[:200] or 'error'}")

with st.sidebar.expander("Refresh everything (slower)"):
    if st.button("Rebuild all pages", use_container_width=True):
        all_scripts = []
        for _, _, sc in PAGES:
            for s in sc:
                if s not in all_scripts:
                    all_scripts.append(s)
        with st.spinner("Rebuilding every dashboard from Odoo…"):
            logs = run_scripts(all_scripts)
        bad = [s for s, rc, _ in logs if rc != 0]
        st.success("All pages rebuilt." if not bad else f"Done, with issues: {', '.join(bad)}")

# ── Render the selected page ──
if os.path.exists(html_path):
    with open(html_path, encoding="utf-8") as f:
        html = f.read()
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(html_path))
    st.sidebar.caption(f"Data as of {mtime:%d %b %Y · %H:%M}")
    # Tall iframe; the page scrolls inside it. Bump height if a page gets cut off.
    components.html(html, height=3200, scrolling=True)
else:
    st.warning(f"“{html_file}” hasn't been generated yet. Click **Refresh this page from Odoo** to build it.")
