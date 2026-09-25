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
import time
import subprocess
import datetime
from urllib.parse import quote

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

    # (1) SERVICE_ACCOUNT_B64 takes PRIORITY — the whole service_account.json,
    # base64-encoded. A single ASCII blob, immune to the newline/quote/smart-character
    # corruption that breaks a hand-pasted PEM key. It overrides any SERVICE_ACCOUNT_JSON
    # string, which can parse as JSON yet still hold a corrupted key.
    blob = ""
    try:
        if "SERVICE_ACCOUNT_B64" in secrets and secrets["SERVICE_ACCOUNT_B64"]:
            blob = str(secrets["SERVICE_ACCOUNT_B64"])
    except Exception:
        pass
    blob = blob or os.environ.get("SERVICE_ACCOUNT_B64", "")
    if blob:
        try:
            decoded = _b64.b64decode(blob).decode("utf-8")
            if _valid_json(decoded):
                os.environ["SERVICE_ACCOUNT_JSON"] = decoded
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
        ("Bags On vs Off Offer", "bags_on_offer.html", ["self_made_combos.py", "bags_on_offer.py"], "loyalty"),
        ("Offer Picking", "offer_picking.html", ["self_made_combos.py", "offer_picking.py"], "local_offer"),
        ("Reject Sale", "reject_sales.html", ["reject_sales.py"], "sell"),
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
                   # "auto": open on desktop, closed on phones — where an open sidebar
                   # covers the page (and the phone icon bar is the nav instead).
                   initial_sidebar_state="auto")

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
# ?page=<label> in the URL selects the page — that's how the phone icon bar (below) navigates.
_qp_page = st.query_params.get("page")
if _qp_page and any(it[0] == _qp_page for it in ALL_ITEMS):
    st.session_state.page = _qp_page
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
            st.query_params["page"] = label
            st.rerun()

# resolve the selected page
label, html_file, scripts, icon = next(it for it in ALL_ITEMS if it[0] == st.session_state.page)

# ── Phone icon bar ──
# On phones Streamlit's sidebar collapses away entirely, leaving no way to see where you
# are or jump pages without reopening it. This bar shows every page as an icon (active one
# lit, sections split by a thin rule) at the top of the content — phone widths only; the
# sidebar stays the nav on larger screens. Each icon is a ?page= link.
_mnav = []
for _i, (_sec, _items) in enumerate(NAV):
    if _i:
        _mnav.append("<span class='mnav-sep'></span>")
    for _lbl, _f, _s, _ic in _items:
        _on = " on" if _lbl == label else ""
        _mnav.append(f"<a class='mnav-i{_on}' href='?page={quote(_lbl)}' target='_self' "
                     f"title='{_lbl}' aria-label='{_lbl}'><span class='mnav-g'>{_ic}</span></a>")
st.markdown("""
<style>@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,500,0,0&display=block');</style>
<style>
  .mnav {display:none;}
  @media (max-width: 768px) {
    .mnav {display:flex; flex-wrap:wrap; justify-content:center; align-items:center; gap:0.3rem;
      padding:0.35rem; margin:0 0 0.4rem; border:1px solid #1e2233; border-radius:14px; background:#0b0d16;}
    .mnav-i {width:42px; height:42px; display:flex; align-items:center; justify-content:center;
      border-radius:11px; color:#94a3b8 !important; text-decoration:none !important;}
    .mnav-i:active {background:rgba(255,255,255,0.08);}
    .mnav-i.on {background:rgba(16,185,129,0.16); color:#34d399 !important;}
    .mnav-g {font-family:'Material Symbols Rounded'; font-size:22px; line-height:1; font-weight:normal;
      font-style:normal; letter-spacing:normal; text-transform:none; white-space:nowrap;
      -webkit-font-feature-settings:'liga'; font-feature-settings:'liga';}
    .mnav-sep {width:1px; height:24px; background:#1e2233; margin:0 0.1rem;}
    .mnav-cur {width:100%; text-align:center; font-size:0.7rem; font-weight:700; letter-spacing:0.06em;
      text-transform:uppercase; color:#34d399; padding-top:0.1rem;}
  }
</style>
<nav class="mnav">""" + "".join(_mnav) + f"<div class='mnav-cur'>{label}</div></nav>",
            unsafe_allow_html=True)
html_path = os.path.join(BASE, html_file)


# Per-generator subprocess budget. Odoo-heavy pages (e.g. timed_offers with many bags across
# all Kenya) can take a few minutes on a slow DB, so give them room rather than failing at 240s.
SCRIPT_TIMEOUT = 600


def run_scripts(script_list, force_fresh=False):
    # force_fresh (a manual Refresh) bypasses the Odoo TTL disk-cache and repopulates it;
    # auto-refresh / page-load leaves it unset so cached lookups are reused within their TTL.
    env = {**os.environ, "DENRI_LAUNCHER": "1", "PYTHONIOENCODING": "utf-8"}
    if force_fresh:
        env["DENRI_FORCE_FRESH"] = "1"
    logs = []
    for s in script_list:
        try:
            r = subprocess.run([sys.executable, os.path.join(BASE, s)], cwd=BASE, env=env,
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=SCRIPT_TIMEOUT)
            logs.append((s, r.returncode, (r.stderr or r.stdout or "").strip()[-600:]))
        except subprocess.TimeoutExpired:
            logs.append((s, -1, f"timed out after {SCRIPT_TIMEOUT}s"))
        except Exception as e:                                    # noqa: BLE001
            logs.append((s, -1, str(e)))
    return logs


# ── Auto-refresh every AUTO_REFRESH_MIN minutes ──────────────────────────────
# The current page regenerates itself from Odoo once its data goes stale. The
# generated HTML's mtime is the shared freshness clock (every viewer sees it), so
# the first session to notice a stale page rebuilds it and the rest get the fresh
# cache. A per-session guard makes each session attempt at most once per interval
# (so a failed build doesn't loop), and a JS timer in the header reloads an idle
# tab so the check keeps firing even with no clicks.
AUTO_REFRESH_MIN = 30
_AUTO_SECS = AUTO_REFRESH_MIN * 60


def _page_age_secs(path):
    try:
        return time.time() - os.path.getmtime(path)
    except OSError:
        return float("inf")


if (os.path.exists(html_path)
        and (time.time() - st.session_state.get("auto_last_check", 0)) >= _AUTO_SECS
        and _page_age_secs(html_path) >= _AUTO_SECS):
    st.session_state.auto_last_check = time.time()
    with st.spinner(f"Auto-refreshing {label} from Odoo…"):
        _logs = run_scripts(scripts)
    st.session_state.refresh_msg = {
        "when": datetime.datetime.now().strftime("%H:%M:%S"),
        "fails": [(s, out) for s, rc, out in _logs if rc != 0],
        "unreachable": any(("not reachable" in (out or "").lower())
                           or ("unreachable" in (out or "").lower())
                           for _, _, out in _logs),
        "auto": True,
    }
    st.rerun()


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

# Reload an idle tab every AUTO_REFRESH_MIN minutes so the auto-refresh check keeps
# firing with no clicks. The reload reruns the app → the stale page rebuilds from Odoo.
HEADER_HTML = HEADER_HTML.replace(
    "tick(); setInterval(tick,1000);",
    "tick(); setInterval(tick,1000);\n"
    "  setTimeout(function(){ try{ (window.top||window.parent||window).location.reload(); }"
    "catch(e){ location.reload(); } }, %d);" % (_AUTO_SECS * 1000))

components.html(HEADER_HTML, height=54)

# Small Refresh button, right-aligned just under the date / clock. The Reject Sale page also
# gets an Excel export button (bags · units · sale price) beside it.
_rj_export = os.path.join(BASE, "reject_sales_export.xlsx")
_rj_export_csv = os.path.join(BASE, "reject_sales_export.csv")
_show_export = (label == "Reject Sale") and (os.path.exists(_rj_export) or os.path.exists(_rj_export_csv))
if _show_export:
    _sp, _ex, _rc = st.columns([0.6, 0.2, 0.2])
    with _ex:
        if os.path.exists(_rj_export):
            with open(_rj_export, "rb") as _fh:
                st.download_button("⬇ Excel", _fh.read(), file_name="reject_sales.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True, key="rj_export_btn")
        else:
            with open(_rj_export_csv, "rb") as _fh:
                st.download_button("⬇ CSV", _fh.read(), file_name="reject_sales.csv",
                                   mime="text/csv", use_container_width=True, key="rj_export_btn")
else:
    _sp, _rc = st.columns([0.8, 0.2])
with _rc:
    _do_refresh = st.button("🔄 Refresh", use_container_width=True,
                            type="primary", key="refresh_btn")
if _do_refresh:
    with st.spinner(f"Refreshing {label} from Odoo…"):
        logs = run_scripts(scripts, force_fresh=True)   # manual: bypass cache, pull fresh + repopulate
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
        _how = "Auto-refreshed" if _rm.get("auto") else "Refreshed"
        st.success(f"✓ {_how} from Odoo at {_rm['when']}")

# Freshness caption: how long ago this page's data was regenerated + the auto cadence.
if os.path.exists(html_path):
    _age_min = int(_page_age_secs(html_path) // 60)
    _ago = "just now" if _age_min < 1 else (f"{_age_min} min ago" if _age_min < 60
            else f"{_age_min // 60}h {_age_min % 60}m ago")
    st.caption(f"Data updated {_ago} · auto-refreshes every {AUTO_REFRESH_MIN} min")

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
  var last = 0, pend = null;
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
  // Debounce: coalesce bursts of events into one measure, so we never re-fit on every
  // single mutation (chart animations fire hundreds) — that thrashed layout and made
  // the big pages feel sluggish, especially on phones.
  function schedule(){ if(pend) return; pend = setTimeout(function(){ pend=null; fit(); }, 120); }
  window.addEventListener('load', fit);
  window.addEventListener('resize', schedule);
  document.addEventListener('change', schedule, true);   // period dropdowns change chart heights
  document.addEventListener('click',  schedule, true);   // toggles / sort buttons
  [150, 500, 1200, 2500].forEach(function(t){ setTimeout(fit, t); });
  // Observe inserted/removed content only — NOT attribute mutations, which fire
  // constantly while charts animate and were the main source of the jank.
  try { new MutationObserver(schedule)
        .observe(document.documentElement, {subtree:true, childList:true}); } catch(e){}
})();
</script>
"""

if os.path.exists(html_path):
    with open(html_path, encoding="utf-8") as f:
        html = f.read()
    # Preconnect to the chart CDN in the <head> so Chart.js starts downloading a beat
    # sooner (saves the DNS/TLS handshake before the blocking <script> that loads it).
    _preconnect = ('<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>'
                   '<link rel="dns-prefetch" href="https://cdn.jsdelivr.net">')
    if "<head>" in html:
        html = html.replace("<head>", "<head>" + _preconnect, 1)
    else:
        html = _preconnect + html
    if "</body>" in html:
        html = html.replace("</body>", EMBED_FIX + "</body>", 1)
    else:
        html += EMBED_FIX
    # Cache token keyed to the file's last-modified time — NOT a fresh timestamp each run.
    # The embedded content string then only changes when the page is actually regenerated
    # (a Refresh rewrites the file → new mtime → the frame rebuilds and shows new data),
    # so plain navigation and reruns reuse the cached iframe instead of re-rendering the
    # whole ~600 KB page every time.
    try:
        _ver = int(os.path.getmtime(html_path))
    except OSError:
        _ver = 0
    html += "\n<!-- v:" + str(_ver) + " -->"
    # Initial height is a fallback only; the script sizes the frame to the EXACT content
    # height so the scroll ends at the last info, with no endless empty space.
    components.html(html, height=700, scrolling=True)
else:
    st.warning(f"“{html_file}” hasn't been generated yet. Click **Refresh this page** to build it.")
