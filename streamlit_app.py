"""
streamlit_app.py — Denri Marketing Dashboard on Streamlit.

Serves the existing dashboard HTML pages inside a Streamlit shell (grouped icon
nav, like the old shell), and — because Streamlit is a live Python server — the
Refresh button re-runs that page's generators against Odoo/Sheets and re-renders
instantly. No GitHub Actions, no redeploys, nothing generated has to be committed.

Deploy: Streamlit Community Cloud → repo, main file = streamlit_app.py.
Secrets (Cloud → Settings → Secrets), TOML — see .streamlit/secrets.toml.example.
"""
import os
import sys
import subprocess
import datetime

import streamlit as st
import streamlit.components.v1 as components

# ── Auto-launch under Streamlit ───────────────────────────────
# If this file is run with plain `python streamlit_app.py` (or double-clicked),
# re-launch it properly via `streamlit run` instead of just printing the
# "missing ScriptRunContext" warnings. Under `streamlit run` (and on Streamlit
# Community Cloud) the runtime already exists, so this block is skipped.
def _under_streamlit():
    try:
        from streamlit.runtime import exists
        return exists()
    except Exception:
        try:
            from streamlit.runtime.scriptrunner import get_script_run_ctx
            return get_script_run_ctx() is not None
        except Exception:
            return False

if not _under_streamlit():
    subprocess.run([sys.executable, "-m", "streamlit", "run",
                    os.path.abspath(__file__), *sys.argv[1:]])
    sys.exit(0)

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
    os.environ.setdefault("DENRI_LAUNCHER", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

_load_secrets_into_env()


# ── Nav: section → [(label, html_file, generator_scripts, material_icon)] ──
NAV = [
    ("Performance", [
        ("Current Performance", "current_performance.html",
            ["weekly_sales.py", "monthly_sales.py", "current_performance.py", "forward_projections.py"], "monitoring"),
    ]),
    ("Products", [
        ("New Products", "new_products.html", ["new_products.py"], "inventory_2"),
        ("Timed Offers", "timed_offers.html", ["timed_offers.py"], "schedule"),
        ("Self-made vs Running Combos", "self_made_combos.html", ["self_made_combos.py"], "shopping_bag"),
    ]),
    ("Marketing", [
        ("Posting Yields", "POSTING (SALES YIELDS FROM ACCURATE POSTING).html",
            ["POSTING (SALES YIELDS FROM ACCURATE POSTING).py"], "campaign"),
        ("Shops Efficiency", "shops_efficiency.html", ["shops_dispatch.py", "shops_efficiency.py"], "storefront"),
    ]),
    ("Intelligence", [
        ("Insights", "insights.html", ["generate_insights.py"], "lightbulb"),
        ("Monthly Report", "monthly_report.html", ["monthly_report.py"], "description"),
        ("History", "history.html", ["history.py"], "history"),
    ]),
]
ALL_ITEMS = [it for _, items in NAV for it in items]

st.set_page_config(page_title="Denri · Marketing Dashboard",
                   page_icon="📊", layout="wide",
                   initial_sidebar_state="expanded")

# ── Styling: hide Streamlit chrome + make the sidebar buttons read as nav items ──
st.markdown("""
<style>
  #MainMenu, footer, header {visibility: hidden;}
  .block-container {padding: 0.5rem 0.7rem 0 0.7rem; max-width: 100%;}
  section[data-testid="stSidebar"] {background:#0b0d16;}
  section[data-testid="stSidebar"] > div {padding-top: 0.6rem;}

  /* brand block */
  .brand {display:flex; align-items:center; gap:0.6rem; padding:0.2rem 0.4rem 0.9rem;}
  .brand .mark {width:40px; height:40px; border-radius:12px; flex-shrink:0;
    background:linear-gradient(135deg,#10b981,#06b6d4); color:#fff; font-weight:800;
    display:flex; align-items:center; justify-content:center; letter-spacing:0.04em;}
  .brand .nm {font-weight:700; color:#f1f5f9; line-height:1.15; font-size:0.95rem;}
  .brand .sb {font-size:0.62rem; color:#64748b; letter-spacing:0.05em;}

  /* section labels */
  .nav-sec {font-size:0.64rem; font-weight:700; letter-spacing:0.13em; text-transform:uppercase;
    color:#475569; margin:0.9rem 0 0.15rem 0.35rem;}

  /* nav buttons: tight, left-aligned, ghost; active = subtle green tint */
  section[data-testid="stSidebar"] .stButton {margin-bottom:-0.55rem;}
  section[data-testid="stSidebar"] .stButton > button {
    width:100%; justify-content:flex-start; text-align:left; gap:0.6rem;
    background:transparent; border:none; box-shadow:none; color:#94a3b8; font-weight:600;
    padding:0.42rem 0.7rem; border-radius:10px;}
  section[data-testid="stSidebar"] .stButton > button:hover {background:rgba(255,255,255,0.06); color:#f1f5f9;}
  section[data-testid="stSidebar"] .stButton > button[kind="primary"],
  section[data-testid="stSidebar"] .stButton > button[data-testid="baseButton-primary"] {
    background:rgba(16,185,129,0.14); color:#34d399; font-weight:700;}
</style>
""", unsafe_allow_html=True)

# ── Sidebar: brand + grouped icon nav ──
st.sidebar.markdown(
    "<div class='brand'><div class='mark'>DA</div>"
    "<div><div class='nm'>Denri Africa</div><div class='sb'>Marketing Analytics</div></div></div>",
    unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = ALL_ITEMS[0][0]

for section, items in NAV:
    st.sidebar.markdown(f"<div class='nav-sec'>{section}</div>", unsafe_allow_html=True)
    for label, html_file, scripts, icon in items:
        active = (st.session_state.page == label)
        if st.sidebar.button(label, icon=f":material/{icon}:", key=f"nav_{label}",
                             use_container_width=True,
                             type=("primary" if active else "secondary")):
            st.session_state.page = label
            st.rerun()

# resolve the selected page
label, html_file, scripts, icon = next(it for it in ALL_ITEMS if it[0] == st.session_state.page)
html_path = os.path.join(BASE, html_file)


def run_scripts(script_list):
    env = {**os.environ, "DENRI_LAUNCHER": "1", "PYTHONIOENCODING": "utf-8"}
    logs = []
    for s in script_list:
        try:
            r = subprocess.run([sys.executable, os.path.join(BASE, s)], cwd=BASE, env=env,
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=240)
            logs.append((s, r.returncode, (r.stderr or r.stdout or "").strip()[-600:]))
        except subprocess.TimeoutExpired:
            logs.append((s, -1, "timed out after 240s"))
        except Exception as e:                                    # noqa: BLE001
            logs.append((s, -1, str(e)))
    return logs


# ── Header row: page title + refresh ──
h_left, h_right = st.columns([0.7, 0.3])
with h_left:
    st.markdown(f"#### {label}")
    if os.path.exists(html_path):
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(html_path))
        st.caption(f"Data as of {mtime:%d %b %Y · %H:%M}")
with h_right:
    if st.button("🔄 Refresh from Odoo", use_container_width=True, type="primary"):
        with st.spinner(f"Refreshing {label} from Odoo…"):
            logs = run_scripts(scripts)
        if all(rc == 0 for _, rc, _ in logs):
            st.success("Refreshed with live data.")
            st.rerun()
        else:
            st.error("Some steps failed:")
            for s, rc, out in logs:
                if rc != 0:
                    st.caption(f"⚠ {s}: {out[:200] or 'error'}")

# ── Render the selected page ──
if os.path.exists(html_path):
    with open(html_path, encoding="utf-8") as f:
        html = f.read()
    components.html(html, height=3200, scrolling=True)
else:
    st.warning(f"“{html_file}” hasn't been generated yet. Click **Refresh from Odoo** to build it.")
