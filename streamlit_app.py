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
import re
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

# ── Theme: "Dashboard V5" — light by default, dark on request ──
# Kept in session state and mirrored to ?theme= so a reload / shared link keeps it.
_qp_theme = st.query_params.get("theme")
if _qp_theme in ("light", "dark"):
    st.session_state.theme = _qp_theme
if "theme" not in st.session_state:
    st.session_state.theme = "light"
THEME = st.session_state.theme

# Palette for the Streamlit chrome (the embedded pages are themed by v5_theme.js).
_V5 = {
    "light": dict(bg="#f4f5fa", bar="#ffffff", raised="#ffffff", border="#e4e7ef",
                  hi="#0f172a", mid="#475569", lo="#64748b", track="#14161f"),
    "dark":  dict(bg="#0b0d14", bar="#11131c", raised="#1a1d2b", border="#232738",
                  hi="#f1f5f9", mid="#aab4c3", lo="#8a97a8", track="#1c1f2d"),
}[THEME]

# One-line purpose under the page title.
PURPOSE = {
    "Current Performance": "Month-to-date sales vs target — live from Odoo POS & Sheets",
    "New Products": "How this month’s new bags are selling",
    "Timed Offers": "Live timed-offer campaigns and the sales lift they drive",
    "Self-made vs Running Combos": "Running vs self-made combos, per market",
    "Bags On vs Off Offer": "Offer vs non-offer bag revenue, and shops vs their Odoo target",
    "Offer Picking": "Which bags to put on offer next",
    "Reject Sale": "Reject-stock sales and pricing",
    "Posting Yields": "Sales yield earned from accurate marketing posting",
    "Shops Efficiency": "Per-shop dispatch, stock and sell-through",
    "Insights": "Automated read-outs across the dashboards",
    "Monthly Report": "The month’s report, targets and commentary",
    "History": "Archived monthly reports from Supabase",
}

# ── Styling: hide Streamlit chrome, V5 header, pill nav, pill buttons ──
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  :root {{ --v5-bg:{_V5['bg']}; --v5-bar:{_V5['bar']}; --v5-raised:{_V5['raised']}; --v5-border:{_V5['border']};
           --v5-hi:{_V5['hi']}; --v5-mid:{_V5['mid']}; --v5-lo:{_V5['lo']}; --v5-track:{_V5['track']};
           --v5-indigo:#4f46e5; --v5-indigo-hi:#6366f1; }}

  /* Keep Streamlit's header (it holds the sidebar open/close arrow) — just hide the ⋮ menu +
     footer, and make it transparent. Never hide the whole header, or the control that opens the
     side menu on narrow screens disappears. */
  #MainMenu, footer {{visibility: hidden;}}
  header[data-testid="stHeader"] {{background: transparent;}}
  .block-container {{padding: 3.2rem 1.25rem 0 1.25rem; max-width: 100%;}}

  .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{background: var(--v5-bg) !important;}}
  /* Inter everywhere except Streamlit's Material icon glyphs (they're ligatures in their own font) */
  .stApp, .stApp p, .stApp label, .stApp span:not([data-testid="stIconMaterial"]) {{
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;}}
  .st-key-themepill [data-testid="stIconMaterial"], .st-key-refresh_btn [data-testid="stIconMaterial"],
  .st-key-rj_export_btn [data-testid="stIconMaterial"] {{font-size: 1rem !important;}}
  .stApp .stMarkdown, .stApp .stMarkdown p {{color: var(--v5-hi);}}
  [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {{color: var(--v5-lo) !important;}}
  [data-testid="stSpinner"], [data-testid="stSpinner"] * {{color: var(--v5-mid) !important;}}
  [data-testid="stAlert"] p, [data-testid="stAlertContentSuccess"] p, [data-testid="stAlertContentWarning"] p
      {{color: var(--v5-hi) !important;}}

  /* ── Sidebar: brand · theme switch · grouped nav · user ── */
  section[data-testid="stSidebar"] {{background: var(--v5-bar); border-right: 1px solid var(--v5-border);}}
  section[data-testid="stSidebar"] > div {{padding-top: 0.6rem;}}
  .v5-brand {{display:flex; align-items:center; gap:0.6rem; padding:0.2rem 0.4rem 0.8rem;}}
  .v5-brand .mark {{width:40px; height:40px; border-radius:12px; flex-shrink:0;
    background:linear-gradient(135deg,#4f46e5,#06b6d4); color:#fff; font-weight:800; font-size:0.82rem;
    display:flex; align-items:center; justify-content:center; letter-spacing:0.04em;
    box-shadow:0 4px 12px rgba(79,70,229,0.35);}}
  .v5-brand .nm {{font-weight:800; color:var(--v5-hi); line-height:1.15; font-size:0.95rem;}}
  .v5-brand .sb {{font-size:0.62rem; color:var(--v5-lo); letter-spacing:0.03em;}}
  .nav-sec {{font-size:0.64rem; font-weight:700; letter-spacing:0.13em; text-transform:uppercase;
    color:var(--v5-lo); margin:0.9rem 0 0.15rem 0.35rem;}}

  /* nav buttons: tight, left-aligned, ghost; active = V5 indigo pill */
  section[data-testid="stSidebar"] .stButton {{margin-bottom:-0.55rem;}}
  /* a button with a tooltip (help=) sits inside a hover-target wrapper — let it fill the row */
  section[data-testid="stSidebar"] .stButton [data-testid="stTooltipHoverTarget"] {{width:100%; display:block;}}
  section[data-testid="stSidebar"] .st-key-themepill .stButton [data-testid="stTooltipHoverTarget"],
  section[data-testid="stSidebar"] .st-key-nav_toggle .stButton [data-testid="stTooltipHoverTarget"] {{width:auto;}}
  section[data-testid="stSidebar"] .stButton button {{
    width:100%; justify-content:flex-start; text-align:left; gap:0.6rem;
    background:transparent; border:none; box-shadow:none; color:var(--v5-mid); font-weight:600;
    padding:0.42rem 0.7rem; border-radius:12px;
    transition: background .2s cubic-bezier(.16,1,.3,1), color .2s cubic-bezier(.16,1,.3,1);}}
  section[data-testid="stSidebar"] .stButton button p {{font-size:0.84rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}}
  section[data-testid="stSidebar"] .stButton button:hover {{background:rgba(79,70,229,0.08); color:var(--v5-hi);}}
  section[data-testid="stSidebar"] .stButton button[kind="primary"],
  section[data-testid="stSidebar"] .stButton button[data-testid="stBaseButton-primary"],
  section[data-testid="stSidebar"] .stButton button[data-testid="baseButton-primary"] {{
    background:var(--v5-indigo); color:#ffffff; font-weight:700; box-shadow:0 4px 14px rgba(79,70,229,0.35);}}
  section[data-testid="stSidebar"] .stButton button[kind="primary"] p {{color:#ffffff;}}

  /* Theme switch — a small dark pill (V5), under the brand */
  .st-key-themepill {{background: var(--v5-track); border-radius: 999px; padding: 3px !important; gap: 2px !important;
    width: fit-content !important; margin: 0 0 0.3rem 0.35rem; flex-wrap: nowrap !important;}}
  section[data-testid="stSidebar"] .st-key-themepill .stButton {{margin-bottom: 0;}}
  section[data-testid="stSidebar"] .st-key-themepill .stButton button {{
    width:auto; background: transparent; color: #a1a7bb; border-radius: 999px; padding: 0.3rem 0.7rem;
    min-height: 0; box-shadow: none;}}
  section[data-testid="stSidebar"] .st-key-themepill .stButton button p {{font-size: 0.72rem; color: inherit;}}
  section[data-testid="stSidebar"] .st-key-themepill .stButton button:hover {{color:#fff; background: rgba(255,255,255,0.07);}}
  section[data-testid="stSidebar"] .st-key-themepill .stButton button[kind="primary"] {{background: var(--v5-indigo); color: #fff;}}

  /* User card — title row, right-aligned, directly above the clock pill */
  .v5-user {{display:flex; align-items:center; justify-content:flex-end; gap:0.55rem; margin:0 0 -0.35rem;
    text-align:left;}}
  @media (max-width: 640px) {{ .v5-user .rl {{display:none;}} }}
  .v5-user .av {{width:32px; height:32px; border-radius:50%; flex-shrink:0;
    background:linear-gradient(135deg,#1e1b4b,#4f46e5); color:#fff; font-size:0.68rem; font-weight:700;
    display:flex; align-items:center; justify-content:center;}}
  .v5-user .nm {{font-size:0.78rem; font-weight:700; color:var(--v5-hi); line-height:1.2;}}
  .v5-user .rl {{font-size:0.62rem; color:var(--v5-lo);}}

  /* ── Title row ── */
  .v5-title h1 {{font-size: 1.3rem !important; font-weight: 800 !important; letter-spacing: -0.02em;
    color: var(--v5-hi) !important; margin: 0 !important; padding: 0 !important; line-height: 1.25;}}
  .v5-title .pp {{font-size: 0.76rem; color: var(--v5-lo); margin-top: 2px;}}
  /* Primary action: solid indigo pill; secondary (Excel): ghost pill */
  .st-key-refresh_btn button, .st-key-rj_export_btn button {{
    border-radius: 999px !important; font-weight: 600 !important; min-height: 38px;
    transition: transform .16s cubic-bezier(.16,1,.3,1), background .16s;}}
  .st-key-refresh_btn button {{background: var(--v5-indigo) !important; border: 1px solid var(--v5-indigo) !important;
    color: #fff !important; box-shadow: 0 6px 16px rgba(79,70,229,0.35);}}
  .st-key-refresh_btn button:hover {{background: var(--v5-indigo-hi) !important; transform: translateY(-1px);}}
  .st-key-refresh_btn button p {{color: #fff !important; font-size: 0.8rem !important; font-weight: 600 !important;}}
  .st-key-rj_export_btn button {{background: var(--v5-raised) !important; border: 1px solid var(--v5-border) !important;
    color: var(--v5-mid) !important;}}
  .st-key-rj_export_btn button:hover {{border-color: var(--v5-indigo) !important; color: var(--v5-indigo) !important;}}
  .st-key-rj_export_btn button p {{color: inherit !important;}}
</style>
""", unsafe_allow_html=True)

# ?page=<label> in the URL selects the page, so a reload / shared link opens the same page.
_qp_page = st.query_params.get("page")
if _qp_page and any(it[0] == _qp_page for it in ALL_ITEMS):
    st.session_state.page = _qp_page
if "page" not in st.session_state:
    st.session_state.page = ALL_ITEMS[0][0]

# ── Sidebar: collapse toggle · brand · theme switch · grouped icon nav ──
# « / » at the top folds the sidebar to an ICON RAIL (desktop/tablet): icons stay, the labels pop
# out on hover (button tooltips), and the page widens into the freed space. Remembered in
# session + ?nav=mini so a reload / shared link keeps it. Phones keep Streamlit's own slide-away
# sidebar (the phone icon bar is the nav there), so the rail styles only apply ≥ 769px.
if st.query_params.get("nav") in ("mini", "full"):
    st.session_state.nav_mini = st.query_params.get("nav") == "mini"
MINI = st.session_state.setdefault("nav_mini", False)
if st.sidebar.button("Toggle menu", key="nav_toggle",
                     icon=(":material/keyboard_double_arrow_right:" if MINI else ":material/keyboard_double_arrow_left:"),
                     help=("Expand menu" if MINI else "Collapse to icons")):
    st.session_state.nav_mini = not MINI
    st.query_params["nav"] = "mini" if not MINI else "full"
    st.rerun()

st.markdown("""
<style>
  /* Our « replaces Streamlit's hide-the-sidebar chevron on larger screens */
  @media (min-width: 769px) {
    [data-testid="stSidebarCollapseButton"] {display: none !important;}
  }
  .st-key-nav_toggle {display: flex; justify-content: flex-end; margin: -0.4rem 0 0.2rem;}
  section[data-testid="stSidebar"] .st-key-nav_toggle .stButton button {
    width: auto !important; padding: 0.3rem 0.45rem !important; color: var(--v5-lo) !important;
    background: transparent !important; box-shadow: none !important; justify-content: center !important;}
  section[data-testid="stSidebar"] .st-key-nav_toggle .stButton button p {display: none;}
  section[data-testid="stSidebar"] .st-key-nav_toggle .stButton button:hover {color: var(--v5-indigo) !important;
    background: rgba(79,70,229,0.08) !important;}
</style>""", unsafe_allow_html=True)

if MINI:
    st.markdown("""
<style>
  @media (min-width: 769px) {
    /* the rail: fixed narrow width (drop Streamlit's drag-to-resize) — the page widens to fill */
    section[data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
      width: 84px !important; min-width: 84px !important; max-width: 84px !important;}
    section[data-testid="stSidebar"] [data-testid="stSidebarResizeHandle"],
    section[data-testid="stSidebar"] div[style*="cursor: col-resize"] {display: none !important;}
    [data-testid="stSidebarUserContent"] {padding-left: 0.55rem !important; padding-right: 0.55rem !important;}
    .st-key-nav_toggle {justify-content: center;}
    /* brand → just the DA mark */
    .v5-brand {justify-content: center; padding: 0.2rem 0 0.6rem;}
    .v5-brand > div:not(.mark) {display: none;}
    /* theme pill → a compact pill of two icon buttons, centred in the rail */
    .st-key-themepill {margin: 0 auto 0.3rem !important; padding: 2px !important; gap: 0 !important;}
    .st-key-themepill > div {width: auto !important; min-width: 0 !important; flex: 0 0 auto !important;}
    section[data-testid="stSidebar"] .st-key-themepill .stButton button {
      padding: 0.28rem 0.38rem !important; gap: 0 !important; min-width: 0 !important;}
    section[data-testid="stSidebar"] .st-key-themepill .stButton button p {display: none;}
    section[data-testid="stSidebar"] .st-key-themepill [data-testid="stIconMaterial"] {font-size: 0.95rem !important;}
    /* section headings → a thin rule */
    .nav-sec {font-size: 0 !important; height: 1px; margin: 0.7rem 0.6rem 0.45rem !important;
      background: var(--v5-border);}
    /* nav → centred icons; the label pops out on hover (tooltip) */
    section[data-testid="stSidebar"] .stButton button {justify-content: center !important;
      padding: 0.55rem 0 !important; gap: 0 !important;}
    section[data-testid="stSidebar"] .stButton button p {display: none;}
    section[data-testid="stSidebar"] .stButton button [data-testid="stIconMaterial"] {font-size: 1.25rem !important;}
    section[data-testid="stSidebar"] .stButton {margin-bottom: -0.35rem;}
  }
</style>""", unsafe_allow_html=True)

st.sidebar.markdown(
    "<div class='v5-brand'><div class='mark'>DA</div>"
    "<div><div class='nm'>Denri Africa</div><div class='sb'>Marketing Analytics</div></div></div>",
    unsafe_allow_html=True)
with st.sidebar.container(horizontal=True, key="themepill", gap=None):
    for _mode, _lbl, _ic in (("light", "Light", "light_mode"), ("dark", "Dark", "dark_mode")):
        if st.button(_lbl, key=f"theme_{_mode}", icon=f":material/{_ic}:",
                     help=(f"{_lbl} theme" if MINI else None),
                     type=("primary" if THEME == _mode else "secondary")):
            st.session_state.theme = _mode
            st.query_params["theme"] = _mode
            st.rerun()

for section, items in NAV:
    st.sidebar.markdown(f"<div class='nav-sec'>{section}</div>", unsafe_allow_html=True)
    for _lbl, _f, _s, _ic in items:
        if st.sidebar.button(_lbl, icon=f":material/{_ic}:", key=f"nav_{_lbl}",
                             use_container_width=True,
                             help=(_lbl if MINI else None),          # the label pops out on the rail
                             type=("primary" if st.session_state.page == _lbl else "secondary")):
            st.session_state.page = _lbl
            st.query_params["page"] = _lbl
            st.rerun()

# (The user card now sits in the title row, above the live clock — see below.)

# resolve the selected page
label, html_file, scripts, icon = next(it for it in ALL_ITEMS if it[0] == st.session_state.page)

# ── Phone icon bar ──
# On phones Streamlit's sidebar collapses away entirely, leaving no way to see where you
# are or jump pages without reopening it. This bar shows every page as an icon (active one
# lit, sections split by a thin rule) at the top of the content — phone widths only; the
# sidebar stays the nav on larger screens. Each icon is a ?page= link (the theme rides along).
_mnav = []
for _i, (_sec, _items) in enumerate(NAV):
    if _i:
        _mnav.append("<span class='mnav-sep'></span>")
    for _lbl, _f, _s, _ic in _items:
        _on = " on" if _lbl == label else ""
        _mnav.append(f"<a class='mnav-i{_on}' href='?page={quote(_lbl)}&theme={THEME}' target='_self' "
                     f"title='{_lbl}' aria-label='{_lbl}'><span class='mnav-g'>{_ic}</span></a>")
st.markdown("""
<style>@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,500,0,0&display=block');</style>
<style>
  .mnav {display:none;}
  @media (max-width: 768px) {
    .mnav {display:flex; flex-wrap:wrap; justify-content:center; align-items:center; gap:0.3rem;
      padding:0.35rem; margin:0 0 0.4rem; border-radius:18px; background:var(--v5-track);}
    .mnav-i {width:42px; height:42px; display:flex; align-items:center; justify-content:center;
      border-radius:999px; color:#a1a7bb !important; text-decoration:none !important;}
    .mnav-i:active {background:rgba(255,255,255,0.08);}
    .mnav-i.on {background:var(--v5-indigo); color:#ffffff !important;}
    .mnav-g {font-family:'Material Symbols Rounded' !important; font-size:22px; line-height:1; font-weight:normal;
      font-style:normal; letter-spacing:normal; text-transform:none; white-space:nowrap;
      -webkit-font-feature-settings:'liga'; font-feature-settings:'liga';}
    .mnav-sep {width:1px; height:24px; background:rgba(255,255,255,0.14); margin:0 0.1rem;}
    .mnav-cur {width:100%; text-align:center; font-size:0.7rem; font-weight:700; letter-spacing:0.06em;
      text-transform:uppercase; color:#c7d2fe; padding-top:0.1rem;}
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


# ── Title row: page title + purpose (left) · live clock pill · Refresh (right) ──
# The clock is a tiny component (it needs JS to tick); it also reloads an idle tab every
# AUTO_REFRESH_MIN minutes so the auto-refresh check keeps firing with no clicks.
CLOCK_HTML = """
<div class="pill"><span class="dot"></span><span id="clk"></span></div>
<style>
  body{margin:0;background:transparent;font-family:'Inter','Segoe UI',system-ui,sans-serif;
       display:flex;justify-content:flex-end;align-items:center;height:100vh}
  .pill{display:inline-flex;align-items:center;gap:0.45rem;padding:0.5rem 0.85rem;border-radius:999px;
        background:__RAISED__;border:1px solid __BORDER__;white-space:nowrap}
  .dot{width:8px;height:8px;border-radius:50%;background:#10b981;display:inline-block;animation:pulse 1.8s ease-out infinite}
  #clk{font-size:0.74rem;color:__MID__;font-weight:600;font-variant-numeric:tabular-nums}
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
      ' \u00b7 '+p(n.getHours())+':'+p(n.getMinutes())+':'+p(n.getSeconds());
  }
  tick(); setInterval(tick,1000);
  setTimeout(function(){ try{ (window.top||window.parent||window).location.reload(); }catch(e){ location.reload(); } }, __RELOAD_MS__);
</script>
"""
CLOCK_HTML = (CLOCK_HTML.replace("__RAISED__", _V5["raised"]).replace("__BORDER__", _V5["border"])
              .replace("__MID__", _V5["mid"]).replace("__RELOAD_MS__", str(_AUTO_SECS * 1000)))

# The Reject Sale page also gets an Excel export button (bags · units · sale price).
_rj_export = os.path.join(BASE, "reject_sales_export.xlsx")
_rj_export_csv = os.path.join(BASE, "reject_sales_export.csv")
_show_export = (label == "Reject Sale") and (os.path.exists(_rj_export) or os.path.exists(_rj_export_csv))
_title_html = ("<div class='v5-title'><h1>" + label + "</h1>"
               "<div class='pp'>" + PURPOSE.get(label, "") + "</div></div>")
if _show_export:
    _tt, _ck, _ex, _rc = st.columns([0.5, 0.24, 0.13, 0.13], vertical_alignment="center")
    with _ex:
        if os.path.exists(_rj_export):
            with open(_rj_export, "rb") as _fh:
                st.download_button("Excel", _fh.read(), file_name="reject_sales.xlsx", icon=":material/download:",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True, key="rj_export_btn")
        else:
            with open(_rj_export_csv, "rb") as _fh:
                st.download_button("CSV", _fh.read(), file_name="reject_sales.csv", icon=":material/download:",
                                   mime="text/csv", use_container_width=True, key="rj_export_btn")
else:
    _tt, _ck, _rc = st.columns([0.6, 0.26, 0.14], vertical_alignment="center")
with _tt:
    st.markdown(_title_html, unsafe_allow_html=True)
with _ck:
    # User card above the live clock pill (both right-aligned in the title row)
    st.markdown(
        "<div class='v5-user'><div class='av'>JO</div><div>"
        "<div class='nm'>Jonathan Owiti</div><div class='rl'>Business Intelligence (BI) Analyst</div>"
        "</div></div>", unsafe_allow_html=True)
    components.html(CLOCK_HTML, height=48)
with _rc:
    _do_refresh = st.button("Refresh", icon=":material/refresh:", use_container_width=True,
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
    # Dashboard V5 theme: inline v5_theme.css + v5_theme.js (local files can't be fetched from
    # inside the component frame) and apply the chosen theme once the page has built its charts.
    _v5_block, _v5_mtimes = "", []
    try:
        with open(os.path.join(BASE, "v5_theme.css"), encoding="utf-8") as _fh:
            _v5_css = _fh.read()
        with open(os.path.join(BASE, "v5_theme.js"), encoding="utf-8") as _fh:
            _v5_js = _fh.read().replace("</script", "<\\/script")
        _v5_mtimes = [int(os.path.getmtime(os.path.join(BASE, f))) for f in ("v5_theme.css", "v5_theme.js")]
        _v5_block = ('<style id="v5-css" data-v5>' + _v5_css + '</style>'
                     '<script>/* v5_theme.js */\n' + _v5_js + '\n</script>'
                     '<script>(function(){var m="' + THEME + '";'
                     'function go(){try{window.V5Theme&&V5Theme.apply(document,m);}catch(e){console.error("V5 theme",e);}}'
                     'if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",go);else go();'
                     'window.addEventListener("load",go);})();</script>')
    except OSError:
        pass
    if "</body>" in html:
        html = html.replace("</body>", _v5_block + EMBED_FIX + "</body>", 1)
    else:
        html += _v5_block + EMBED_FIX
    # components.html() renders the page in a frame with no URL, so a LOCAL
    # <script src="chart_switcher.js"> has nothing to resolve against (Streamlit answers
    # it with its own index page). Inline every local script file instead.
    _inlined_mtimes = []

    def _inline_local_script(m):
        src = m.group(1)
        path = os.path.join(os.path.dirname(os.path.abspath(html_path)), src)
        if "://" in src or src.startswith("//") or not os.path.isfile(path):
            return m.group(0)
        try:
            with open(path, encoding="utf-8") as _js:
                code = _js.read().replace("</script", "<\\/script")
            _inlined_mtimes.append(int(os.path.getmtime(path)))
        except OSError:
            return m.group(0)
        return "<script>/* " + src + " */\n" + code + "\n</script>"

    html = re.sub(r'<script\s+src="([^"]+\.js)"\s*>\s*</script>', _inline_local_script, html)
    # Cache token keyed to the file's last-modified time — NOT a fresh timestamp each run.
    # The embedded content string then only changes when the page is actually regenerated
    # (a Refresh rewrites the file → new mtime → the frame rebuilds and shows new data),
    # so plain navigation and reruns reuse the cached iframe instead of re-rendering the
    # whole ~600 KB page every time.
    try:
        _ver = int(os.path.getmtime(html_path))
    except OSError:
        _ver = 0
    _ver = max([_ver] + _inlined_mtimes + _v5_mtimes)   # an edited shared script also refreshes the frame
    html += "\n<!-- v:" + str(_ver) + " theme:" + THEME + " -->"   # switching theme rebuilds the frame
    # Initial height is a fallback only; the script sizes the frame to the EXACT content
    # height so the scroll ends at the last info, with no endless empty space.
    components.html(html, height=700, scrolling=True)
else:
    st.warning(f"“{html_file}” hasn't been generated yet. Click **Refresh this page** to build it.")
