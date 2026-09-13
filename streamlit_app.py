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

    # Robust Google service-account handling. A raw-JSON string in secrets is easy to
    # break (pasting with """ mangles the private key's \n). If SERVICE_ACCOUNT_JSON is
    # missing OR doesn't parse, fall back to a standard TOML table — [gcp_service_account]
    # or [service_account] — and rebuild valid JSON from it (this round-trips the key
    # newlines correctly regardless of quoting).
    import json as _json
    import base64 as _b64

    def _valid_json(s):
        try:
            _json.loads(s)
            return True
        except Exception:
            return False

    # (1) SERVICE_ACCOUNT_B64 — the whole service_account.json, base64-encoded. This is
    # the most robust: a single ASCII blob, immune to newline/quote/smart-character
    # corruption that breaks a hand-pasted PEM key.
    if not _valid_json(os.environ.get("SERVICE_ACCOUNT_JSON", "")):
        blob = ""
        try:
            if "SERVICE_ACCOUNT_B64" in secrets and secrets["SERVICE_ACCOUNT_B64"]:
                blob = str(secrets["SERVICE_ACCOUNT_B64"])
        except Exception:
            pass
        blob = blob or os.environ.get("SERVICE_ACCOUNT_B64", "")
        if blob:
            try:
                os.environ["SERVICE_ACCOUNT_JSON"] = _b64.b64decode(blob).decode("utf-8")
            except Exception:
                pass

    # (2) TOML table [gcp_service_account]/[service_account] → rebuild JSON.
    if not _valid_json(os.environ.get("SERVICE_ACCOUNT_JSON", "")):
        for tkey in ("gcp_service_account", "service_account"):
            try:
                if tkey in secrets:
                    os.environ["SERVICE_ACCOUNT_JSON"] = _json.dumps(dict(secrets[tkey]))
                    break
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
  /* Keep Streamlit's header (it holds the sidebar open/close arrow) — just hide the
     ⋮ menu + footer, and make the header transparent. Never hide the whole header,
     or the control that opens the side menu on narrow screens disappears. */
  #MainMenu, footer {visibility: hidden;}
  header[data-testid="stHeader"] {background: transparent;}
  /* Leave Streamlit's Deploy/toolbar alone in the top-right; just start the app's
     content lower so the header/date/refresh never sit under it. */
  .block-container {padding: 3.2rem 0.7rem 0 0.7rem; max-width: 100%;}
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

# ── Sidebar: grouped icon nav ──
# (Use Streamlit's built-in « chevron at the top of the sidebar to minimize/hide it —
#  a custom icon-rail fights Streamlit's sidebar width and can hide the whole menu.)
if "page" not in st.session_state:
    st.session_state.page = ALL_ITEMS[0][0]

st.sidebar.markdown(
    "<div class='brand'><div class='mark'>DA</div>"
    "<div><div class='nm'>Denri Africa</div><div class='sb'>Marketing Analytics</div></div></div>",
    unsafe_allow_html=True)

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


# ── Header: user card + live status dot + ticking clock (left) · refresh (right) ──
HEADER_HTML = """
<div style="display:flex;align-items:center;justify-content:space-between;font-family:'Segoe UI',system-ui,sans-serif">
  <div>
    <div style="font-weight:700;color:#f1f5f9;font-size:0.92rem;line-height:1.15">Jonathan Owiti</div>
    <div style="font-size:0.66rem;color:#64748b;letter-spacing:0.03em">Business Intelligence (BI) Analyst</div>
  </div>
  <div style="display:flex;align-items:center;gap:0.5rem">
    <span style="width:8px;height:8px;border-radius:50%;background:#10b981;display:inline-block;animation:pulse 1.8s ease-out infinite"></span>
    <span id="clk" style="font-size:0.84rem;color:#94a3b8;font-weight:600;font-variant-numeric:tabular-nums"></span>
  </div>
</div>
<style>
  body{margin:0;background:transparent}
  @keyframes pulse{0%{box-shadow:0 0 0 0 rgba(16,185,129,0.5)}70%{box-shadow:0 0 0 7px rgba(16,185,129,0)}100%{box-shadow:0 0 0 0 rgba(16,185,129,0)}}
  @media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>
<script>
  function tick(){
    var n=new Date();
    var d=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    var m=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var p=function(x){return String(x).padStart(2,'0')};
    document.getElementById('clk').textContent =
      d[n.getDay()]+', '+n.getDate()+' '+m[n.getMonth()]+' '+n.getFullYear()+
      ' \\u00b7 '+p(n.getHours())+':'+p(n.getMinutes())+':'+p(n.getSeconds());
  }
  tick(); setInterval(tick,1000);
</script>
"""

components.html(HEADER_HTML, height=54)

# Small Refresh button, right-aligned just under the date / clock.
_sp, _rc = st.columns([0.8, 0.2])
with _rc:
    _do_refresh = st.button("🔄 Refresh", use_container_width=True,
                            type="primary", key="refresh_btn")
if _do_refresh:
    with st.spinner(f"Refreshing {label} from Odoo…"):
        logs = run_scripts(scripts)          # current page's generators only
    fails = [(s, out) for s, rc, out in logs if rc != 0]
    unreachable = any(("not reachable" in (out or "").lower())
                      or ("unreachable" in (out or "").lower())
                      for _, _, out in logs)
    # Stash the result so it survives the rerun (a toast would vanish immediately).
    st.session_state.refresh_msg = {
        "when": datetime.datetime.now().strftime("%H:%M:%S"),
        "fails": fails, "unreachable": unreachable,
    }
    st.rerun()

# Persistent refresh feedback (shown after the rerun re-reads the regenerated page)
_rm = st.session_state.pop("refresh_msg", None)
if _rm:
    if _rm["fails"]:
        for s, out in _rm["fails"]:
            # Show the LAST line of the traceback — that's the actual exception,
            # e.g. "JSONDecodeError: ..." or "ValueError: Could not deserialize key".
            _lines = [ln for ln in (out or "").splitlines() if ln.strip()]
            _msg = _lines[-1] if _lines else "error"
            st.warning(f"⚠ {s}: {_msg[:300]}")
    elif _rm["unreachable"]:
        st.warning("⚠ Couldn’t reach Odoo / Google Sheets — showing the last data. "
                   "On the deployed app this means the DB secrets are missing or the "
                   "database is refusing the connection.")
    else:
        st.success(f"✓ Refreshed from Odoo at {_rm['when']}")

# ── Render the selected page ──
# Injected into each embedded page so it (a) doesn't force a full-viewport black
# body inside the iframe, and (b) auto-sizes the iframe to its real content height
# — which makes it fit correctly on both mobile and desktop with no dead space.
EMBED_FIX = """
<style id="st-embed-fix">
  /* Kill viewport-height rules inside the frame so the page is only as tall as its
     real content — otherwise min-height:100vh leaves empty scroll below the info. */
  html, body { min-height:0 !important; height:auto !important; overflow-y:visible !important;
               overflow-x:hidden !important; max-width:100% !important; }
  .wrap, .container, .app-body, main, [class*="-wrap"] { min-height:0 !important; }
  /* Mobile: fit the content to the phone width (no side cut-off), trim big padding. */
  @media (max-width: 640px){
    body { padding-left:0.6rem !important; padding-right:0.6rem !important; }
    .wrap, .container { max-width:100% !important; }
  }
</style>
<script>
(function(){
  var last = 0;
  function fit(){
    try{
      var h = document.body ? document.body.scrollHeight
                            : document.documentElement.scrollHeight;
      if (window.frameElement && h && Math.abs(h - last) > 2){
        last = h;
        window.frameElement.style.height = h + 'px';
        window.frameElement.style.minHeight = h + 'px';
      }
    }catch(e){}
  }
  window.addEventListener('load', fit);
  window.addEventListener('resize', fit);
  [150, 500, 1200, 2500].forEach(function(t){ setTimeout(fit, t); });
  try { new MutationObserver(function(){ setTimeout(fit, 50); })
        .observe(document.documentElement, {subtree:true, childList:true, attributes:true}); } catch(e){}
})();
</script>
"""

if os.path.exists(html_path):
    with open(html_path, encoding="utf-8") as f:
        html = f.read()
    if "</body>" in html:
        html = html.replace("</body>", EMBED_FIX + "</body>", 1)
    else:
        html += EMBED_FIX
    # Cache-buster: a unique marker each run forces components.html to rebuild the
    # iframe from the freshly-read file, so a refresh actually shows the new data
    # instead of a stale cached frame.
    html += "\n<!-- v:" + datetime.datetime.now().strftime("%H%M%S%f") + " -->"
    # Initial height is a fallback only; the script sizes the frame to the EXACT content
    # height so the scroll ends at the last info, with no endless empty space.
    components.html(html, height=700, scrolling=True)
else:
    st.warning(f"“{html_file}” hasn't been generated yet. Click **Refresh this page** to build it.")
