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

# ── Auto-launch ───────────────────────────────────────────────
# Run this file directly — `python streamlit_app.py`, VS Code's Run button or a double-click —
# and it re-launches itself via `streamlit run`. If the Python that opened it has no Streamlit
# (e.g. the Windows Store python), it hands over to the Anaconda Python the .bat used.
_FALLBACK_PYTHON = r"C:\ProgramData\anaconda3\python.exe"
try:
    import streamlit as st
    import streamlit.components.v1 as components
except ImportError:
    if os.path.exists(_FALLBACK_PYTHON) and os.path.normcase(sys.executable) != os.path.normcase(_FALLBACK_PYTHON):
        sys.exit(subprocess.run([_FALLBACK_PYTHON, "-m", "streamlit", "run",
                                 os.path.abspath(__file__), *sys.argv[1:]]).returncode)
    print("Streamlit isn't installed for " + sys.executable + " — run: pip install -r requirements.txt")
    input("Press Enter to close...")
    sys.exit(1)

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
# Built from dashboard_pages.json — the ONE page list (shell.html reads the same file).
# Add / rename / reorder pages there, not here.
import json as _json
with open(os.path.join(BASE, "dashboard_pages.json"), encoding="utf-8") as _mf:
    MANIFEST = _json.load(_mf)
OWNER = MANIFEST.get("owner", {})

# ── Password-locked pages ("password_secret": "<SECRET NAME>" in dashboard_pages.json) ──
# Everyone sees the tab (with a lock); opening it asks for that page's own password, read from the
# named Streamlit secret. A correct password opens the page at once and is remembered in the
# browser's localStorage for 30 days: on a later visit the locked page hands the saved token back
# once (?unlock=, removed straight away), so reloads and tab clicks don't ask again — until the
# password is changed in Secrets. Running locally never asks.
import hashlib as _hashlib


def _secret(name):
    """A Streamlit secret by name — top level, or pasted by mistake under a [table] (TOML puts it there)."""
    try:
        secrets = st.secrets
        if name in secrets and str(secrets[name]).strip():
            return str(secrets[name]).strip()
        for _v in secrets.values():
            if hasattr(_v, "get") and str(_v.get(name) or "").strip():
                return str(_v[name]).strip()
    except Exception:
        pass
    return os.environ.get(name, "").strip()


def _pw_key(lbl):
    return "dw_pw_" + re.sub(r"[^a-z0-9]+", "_", lbl.lower()).strip("_")


def _pw_token(lbl, pw):
    return _hashlib.sha256(("dw-page:" + lbl + ":" + pw).encode()).hexdigest()


try:
    _host = (st.context.headers.get("Host") or "").split(":")[0]
except Exception:
    _host = ""
IS_LOCAL = _host in ("localhost", "127.0.0.1")
_unlocked = st.session_state.setdefault("pw_unlocked", {})   # label → token unlocked in this session
_qp_unlock = st.query_params.get("unlock")
if _qp_unlock is not None:
    del st.query_params["unlock"]        # don't leave the token in the address bar
PW_TOKEN_TRIED = _qp_unlock is not None   # this load came from a saved token (no auto-retry → no loop)
PAGE_PASSWORD = {}   # label → password ("" = page locked but no password set up yet)
LOCKED = set()       # labels this browser hasn't unlocked
for _p in MANIFEST["pages"]:
    if _p.get("password_secret"):
        _lbl = _p["label"]
        _pw = _secret(_p["password_secret"])
        PAGE_PASSWORD[_lbl] = _pw
        _tok = _pw_token(_lbl, _pw) if _pw else None
        if _tok and _qp_unlock == _tok:
            _unlocked[_lbl] = _tok
        if not IS_LOCAL and not (_tok and _unlocked.get(_lbl) == _tok):
            LOCKED.add(_lbl)

NAV = []
for _p in sorted(MANIFEST["pages"], key=lambda p: p["order"]):
    if not NAV or NAV[-1][0] != _p["section"]:
        NAV.append((_p["section"], []))
    NAV[-1][1].append((_p["label"], _p["html"], _p["scripts"], _p["icon"]))
ALL_ITEMS = [it for _, items in NAV for it in items]

st.set_page_config(page_title="Denri · Marketing Dashboard",
                   page_icon="📊", layout="wide",
                   # "auto": open on desktop, closed on phones — where an open sidebar
                   # covers the page (and the phone icon bar is the nav instead).
                   initial_sidebar_state="collapsed")

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
    "light": dict(bg="#e9ebf0", bar="#f9fafb", raised="#f9fafb", border="#d9dde5",
                  hi="#0f172a", mid="#334155", lo="#475569", track="#14161f"),
    "dark":  dict(bg="#0b0d14", bar="#11131c", raised="#1a1d2b", border="#232738",
                  hi="#f1f5f9", mid="#aab4c3", lo="#8a97a8", track="#1c1f2d"),
}[THEME]

# One-line purpose under the page title (from dashboard_pages.json).
PURPOSE = {_p["label"]: _p.get("purpose", "") for _p in MANIFEST["pages"]}

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
  /* Title row = one compact strip under the top bar */
  [data-testid="stHorizontalBlock"]:has(.v5-title) {{background: var(--v5-bar); border: 1px solid var(--v5-border);
    border-radius: 14px; padding: 0.45rem 0.6rem 0.45rem 1rem; margin: 0.15rem 0 0.1rem; gap: 0.6rem;
    box-shadow: 0 4px 14px rgba(16,24,40,0.05);}}
  [data-testid="stHorizontalBlock"]:has(.v5-title) .v5-title h1 {{font-size: 1.08rem !important;}}
  .st-key-refresh_btn button {{min-height: 36px !important; padding: 0 0.9rem !important;}}
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

# ── Top bar look (like shell.html's header) + owner credit ─────────────────────────────
# There is no sidebar: one sticky bar holds the brand, every page as a pill tab (the track scrolls
# left ↔ right — top_nav.js), the theme switch, contact and the owner. Colours follow the V5 tokens.
_look_css = """<style>
  @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,500,0,0&display=block');
  section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"],
  [data-testid="stSidebarCollapseButton"], header[data-testid="stHeader"] {display:none !important;}
  .block-container {padding-top:0.6rem !important;}
  /* Invisible helpers (style-only blocks, zero-height components) must not add the 16px row gap each */
  [data-testid="stElementContainer"][height="0px"],
  [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] > style:only-child) {display:none !important;}
  /* Narrow screens: Refresh becomes an icon button instead of wrapping its label */
  @media (max-width: 900px) {.st-key-refresh_btn button p {display:none !important;} .st-key-refresh_btn button {min-width:44px;}}
  [data-testid="stElementContainer"]:has(.tn-bar), .element-container:has(.tn-bar) {position:sticky; top:0; z-index:999;}
  /* Let the page frame's holder grow with the frame (EMBED_FIX stretches it), so the column is as tall as
     the page and the sticky bar stays pinned all the way down */
  [data-testid="stElementContainer"]:has(> iframe[data-dash-page]) {height:auto !important;}
  .tn-bar {display:flex; align-items:center; gap:1rem; padding:0.6rem 0.9rem; margin:0 0 0.2rem; min-width:0;
    background:var(--v5-bar); border:1px solid var(--v5-border); border-radius:16px; box-shadow:0 6px 18px rgba(16,24,40,0.06);}
  .tn-brand {display:flex; align-items:center; gap:0.6rem; flex-shrink:0;}
  .tn-mark {width:36px; height:36px; border-radius:11px; flex-shrink:0; display:flex; align-items:center; justify-content:center;
    background:linear-gradient(135deg,#4f46e5,#06b6d4); color:#fff; font-weight:800; font-size:0.78rem; box-shadow:0 4px 12px rgba(79,70,229,0.35);}
  .tn-nm {font-weight:800; font-size:0.92rem; color:var(--v5-hi); line-height:1.15;}
  .tn-sb {font-size:0.64rem; color:var(--v5-lo);}
  .tn-scroller {flex:1; min-width:0; display:flex; justify-content:center;}
  .tn-frame {display:flex; min-width:0; max-width:100%; border-radius:999px;}   /* hugs the pill; carries the glow + arrows */
  .tn-track {display:flex; align-items:center; gap:2px; max-width:100%; padding:4px; border-radius:999px; overflow-x:auto;
    background:var(--v5-track); box-shadow:0 6px 18px rgba(16,24,40,0.12);}
  .tn-item {display:inline-flex; align-items:center; gap:0.4rem; padding:0.46rem 0.85rem; border-radius:999px; flex-shrink:0;
    font-size:0.74rem; font-weight:600; white-space:nowrap; color:#a1a7bb !important; text-decoration:none !important;
    transition:background .2s, color .2s;}
  .tn-item:hover {color:#fff !important; background:rgba(255,255,255,0.07);}
  .tn-item.on {background:var(--v5-indigo); color:#fff !important; box-shadow:0 4px 14px rgba(79,70,229,0.5);}
  .tn-ic {font-family:'Material Symbols Rounded' !important; font-size:16px; line-height:1; font-weight:normal; font-style:normal;
    letter-spacing:normal; text-transform:none; white-space:nowrap; -webkit-font-feature-settings:'liga'; font-feature-settings:'liga';}
  .tn-sep {width:1px; height:16px; margin:0 3px; flex-shrink:0; background:rgba(255,255,255,0.12);}
  .tn-right {display:flex; align-items:center; gap:0.6rem; flex-shrink:0;}
  .tn-theme {display:inline-flex; padding:3px; border-radius:999px; background:var(--v5-track);}
  .tn-th {display:inline-flex; align-items:center; gap:0.3rem; padding:0.36rem 0.7rem; border-radius:999px;
    font-size:0.7rem; font-weight:600; color:#a1a7bb !important; text-decoration:none !important;}
  .tn-th:hover {color:#fff !important;}
  .tn-th.on {background:var(--v5-indigo); color:#fff !important;}
  .tn-icon {width:36px; height:36px; border-radius:11px; display:inline-flex; align-items:center; justify-content:center;
    background:var(--v5-raised); border:1px solid var(--v5-border); color:var(--v5-mid) !important; text-decoration:none !important;}
  .tn-icon:hover {border-color:var(--v5-indigo); color:var(--v5-indigo) !important;}
  .tn-bar .v5-user {margin:0; justify-content:flex-start;}
  .tn-item:focus-visible, .tn-th:focus-visible, .tn-icon:focus-visible {outline:2px solid #818cf8; outline-offset:2px;}
  /* Narrower screens: the tabs drop to their own full-width row (still scrolling sideways) */
  @media (max-width: 1340px) {.tn-bar {flex-wrap:wrap; row-gap:0.55rem;} .tn-scroller {order:3; flex-basis:100%;}
    .tn-right {margin-left:auto;}}
  @media (max-width: 640px) {.tn-sb, .tn-th .lbl, .tn-bar .v5-user .rl {display:none;} .tn-bar {padding:0.5rem 0.6rem; gap:0.6rem;}
    .tn-item {min-height:40px;}}

  /* Owner credit — Jonathan Owiti, the person behind the dashboard */
  @property --own-spin {syntax:'<angle>'; initial-value:0deg; inherits:false;}
  .v5-user {--own-a:__own_a__; --own-b:__own_b__; --own-c:__own_c__;}
  .v5-user .av.owner-avatar {position:relative; isolation:isolate; box-shadow:0 0 0 2px __ring_gap__, 0 0 16px __glow__;}
  .v5-user .av.owner-avatar::before {content:''; position:absolute; inset:-4px; border-radius:50%; z-index:-1;
    background:conic-gradient(from var(--own-spin), var(--own-a), var(--own-b), var(--own-c), var(--own-a));
    animation:ownSpin 6s linear infinite;}
  .v5-user .nm.owner-name {font-weight:800; background:linear-gradient(90deg,var(--own-a),var(--own-b),var(--own-c),var(--own-b),var(--own-a));
    background-size:200% auto; -webkit-background-clip:text; background-clip:text; color:transparent !important;
    animation:ownShimmer 6s linear infinite;}
  .v5-user .owner-spark {display:inline-block; margin-left:0.3rem; font-size:0.9em; color:#f59e0b; -webkit-text-fill-color:#f59e0b;
    animation:ownTwinkle 2.4s ease-in-out infinite;}
  .v5-user .rl.owner-role {display:inline-block; margin-top:3px; padding:0.12rem 0.5rem; border-radius:999px; font-weight:700;
    color:var(--v5-mid) !important; border:1px solid transparent;
    background:linear-gradient(var(--v5-raised),var(--v5-raised)) padding-box, linear-gradient(90deg,var(--own-a),var(--own-b),var(--own-c)) border-box;}
  @keyframes ownSpin {to {--own-spin:360deg;}}
  @keyframes ownShimmer {to {background-position:200% center;}}
  @keyframes ownTwinkle {0%,100% {opacity:0.6; transform:scale(0.85) rotate(0deg);}
    50% {opacity:1; transform:scale(1.15) rotate(20deg); text-shadow:0 0 8px rgba(245,158,11,0.75);}}
  @media (prefers-reduced-motion: reduce) {.v5-user .av.owner-avatar::before, .v5-user .nm.owner-name, .v5-user .owner-spark {animation:none !important;}}
</style>"""
_OWN = {"light": dict(own_a="#4f46e5", own_b="#0e7490", own_c="#047857", glow="rgba(79,70,229,0.28)", ring_gap="#ffffff"),
        "dark": dict(own_a="#818cf8", own_b="#22d3ee", own_c="#34d399", glow="rgba(99,102,241,0.45)", ring_gap="#11131c")}[THEME]
for _k, _v in _OWN.items():
    _look_css = _look_css.replace("__" + _k + "__", _v)
st.markdown(_look_css, unsafe_allow_html=True)


# resolve the selected page
label, html_file, scripts, icon = next(it for it in ALL_ITEMS if it[0] == st.session_state.page)

# ── Welcome / loading card + Dark Reader lock (welcome_screen.js) ──
# A zero-height component: the script draws into the Streamlit page itself (same origin). It locks
# out the Dark Reader extension every run and shows the welcome card once per browser session.
try:
    with open(os.path.join(BASE, "welcome_screen.js"), encoding="utf-8") as _fh:
        _welcome_js = _fh.read().replace("</script", "<\\/script")
    _dw_cfg = {"theme": THEME, "page": label, "owner": OWNER,
               "jumps": [l for l in ("Insights", "Monthly Report", "History") if any(it[0] == l for it in ALL_ITEMS)]}
    st.markdown("<style>[data-testid='stElementContainer']:has(iframe[height='0']),"
                ".element-container:has(iframe[height='0']) {display:none !important;}</style>",
                unsafe_allow_html=True)
    components.html("<script>window.DW_CONFIG = " + _json.dumps(_dw_cfg).replace("</", "<\\/") + ";</script>"
                    "<script>" + _welcome_js + "</script>", height=0)
except OSError:
    pass

# ── Top bar: brand · pill tabs (scroll left ↔ right) · theme · contact · owner ──
# Every page from dashboard_pages.json as a pill; each is a ?page= link (the theme rides along),
# so a reload / shared link opens the same page. top_nav.js adds wheel / drag / arrow scrolling
# and keeps the current tab in view.
from html import escape as _esc
_pmeta = {p["label"]: p for p in MANIFEST["pages"]}
_tabs = []
for _i, (_sec, _items) in enumerate(NAV):
    if _i:
        _tabs.append("<span class='tn-sep' aria-hidden='true'></span>")
    for _lbl, _f, _s, _ic in _items:
        _pm, _on = _pmeta.get(_lbl, {}), _lbl == label
        if _lbl in LOCKED:
            _ic = "lock"
        _tabs.append(f"<a class='tn-item{' on' if _on else ''}' href='?page={quote(_lbl)}&amp;theme={THEME}' target='_self'"
                     f"{' aria-current=\"page\"' if _on else ''} title='{_esc(_pm.get('purpose', ''), quote=True)}'>"
                     f"<span class='tn-ic' aria-hidden='true'>{_ic}</span>{_esc(_pm.get('short') or _lbl)}</a>")
_themes = "".join(
    f"<a class='tn-th{' on' if THEME == _m else ''}' href='?page={quote(label)}&amp;theme={_m}' target='_self' "
    f"aria-label='{_l} theme'><span class='tn-ic' aria-hidden='true'>{_ic}</span><span class='lbl'>{_l}</span></a>"
    for _m, _l, _ic in (("light", "Light", "light_mode"), ("dark", "Dark", "dark_mode")))
_owner_html = ("<div class='v5-user' title='Built and maintained by " + _esc(OWNER.get("name", ""), quote=True) + ", "
               + _esc(OWNER.get("title", ""), quote=True) + "'>"
               "<div class='av owner-avatar'>" + _esc(OWNER.get("initials", "JO")) + "</div><div>"
               "<div class='nm owner-name'>" + _esc(OWNER.get("name", "")) + "<span class='owner-spark' aria-hidden='true'>✦</span></div>"
               "<div class='rl owner-role'>" + _esc(OWNER.get("title", "")) + "</div></div></div>")
_mail = (f"<a class='tn-icon' href='mailto:{_esc(OWNER.get('email', ''), quote=True)}' title='Contact &amp; help' "
         "aria-label='Contact the dashboard owner by email'><span class='tn-ic' aria-hidden='true'>mail</span></a>"
         if OWNER.get("email") else "")
st.markdown(
    "<div class='tn-bar'>"
    "<div class='tn-brand'><div class='tn-mark'>DA</div><div><div class='tn-nm'>Denri Africa</div>"
    "<div class='tn-sb'>Marketing Analytics</div></div></div>"
    "<div class='tn-scroller'><div class='tn-frame tn-glow'><nav class='tn-track' aria-label='Dashboards'>" + "".join(_tabs) + "</nav></div></div>"
    "<div class='tn-right'><div class='tn-theme' role='group' aria-label='Colour theme'>" + _themes + "</div>"
    + _mail + _owner_html + "</div></div>",
    unsafe_allow_html=True)
# Sideways scrolling for the tab track: load top_nav.js into the Streamlit page (once) and attach it.
try:
    with open(os.path.join(BASE, "top_nav.js"), encoding="utf-8") as _fh:
        _topnav_js = _fh.read()
    components.html(
        "<script>(function(){var P=window.parent,D;try{D=P.document;}catch(e){return;}"
        "if(!P.TopNav){var s=D.createElement('script');s.textContent=" + _json.dumps(_topnav_js).replace("</", "<\\/") +
        ";D.head.appendChild(s);}"
        "if(P.TopNav&&P.TopNav.injectCss){P.TopNav.injectCss(D);}"
        "var n=0;(function go(){var t=D.querySelector('.tn-track');"
        "if(t&&P.TopNav){P.TopNav.attach(t);}else if(n++<100){setTimeout(go,100);}})();})();</script>", height=0)
except OSError:
    pass

html_path = os.path.join(BASE, html_file)

# Just unlocked: save the token in this browser so later visits open without asking.
_pw_save = st.session_state.pop("pw_save", None)
if _pw_save:
    components.html("<script>try{window.parent.localStorage.setItem(" + _json.dumps(_pw_key(_pw_save[0])) + ","
                    + _json.dumps(_json.dumps({"tok": _pw_save[1], "exp": int(time.time() + 30 * 86400) * 1000}))
                    + ");}catch(e){}</script>", height=0)

# ── Password gate for locked pages — nothing of the page is built or shown until it's unlocked ──
if label in LOCKED:
    _pw_need = PAGE_PASSWORD.get(label, "")
    _k = _json.dumps(_pw_key(label))
    if _pw_need and not PW_TOKEN_TRIED:
        # A token saved on this browser? Hand it back once (the server checks it), else show the form.
        components.html("<script>try{var P=window.parent,v=JSON.parse(P.localStorage.getItem(" + _k + ")||'null');"
                        "if(v&&v.tok&&v.exp>Date.now()){var u=new URL(P.location.href);"
                        "u.searchParams.set('page'," + _json.dumps(label) + ");u.searchParams.set('unlock',v.tok);"
                        "P.location.replace(u.toString());}}catch(e){}</script>", height=0)
    elif PW_TOKEN_TRIED:
        # The saved token no longer matches (password changed) — forget it.
        components.html("<script>try{window.parent.localStorage.removeItem(" + _k + ");}catch(e){}</script>", height=0)
    st.markdown("<div class='v5-title'><h1>" + _esc(label) + "</h1>"
                "<div class='pp'>" + _esc(PURPOSE.get(label, "")) + "</div></div>", unsafe_allow_html=True)
    _, _gate, _ = st.columns([1, 1.2, 1])
    with _gate:
        if not _pw_need:
            st.warning("This page is locked and has no password set up yet. Add "
                       f"`{_pmeta[label]['password_secret']}` in the app's Secrets.", icon=":material/lock:")
        else:
            with st.form("pw_gate_" + _pw_key(label), border=True):
                st.markdown(f"**:material/lock: {_esc(label)} is password protected**")
                _pw_try = st.text_input("Password", type="password", placeholder="Enter the password for this page")
                _pw_ok = st.form_submit_button("Unlock", type="primary", icon=":material/lock_open:",
                                               use_container_width=True)
            if _pw_ok:
                if _pw_try.strip() == _pw_need:
                    _unlocked[label] = _pw_token(label, _pw_need)
                    st.session_state.pw_save = (label, _unlocked[label])
                    st.rerun()
                else:
                    st.error("Wrong password.", icon=":material/error:")
    st.stop()


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
# DASH_NO_AUTOREFRESH=1 (testing / previews): never rebuild pages from Odoo on a page view and
# never reload idle tabs. The manual "Refresh this page" button still works.
NO_AUTOREFRESH = os.environ.get("DASH_NO_AUTOREFRESH") == "1"


def _page_age_secs(path):
    try:
        return time.time() - os.path.getmtime(path)
    except OSError:
        return float("inf")


if (not NO_AUTOREFRESH
        and os.path.exists(html_path)
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


# ── Month-end catch-up: archive last month to Supabase (History) automatically ──
# month_end.py freezes a finished month (numbers + report comments) into Supabase. It used to
# rely on being run by hand, so a month could be missed. Now the first page view of a new month
# checks Supabase and, if last month isn't there, starts month_end.py in the background, pinned
# to last month. A lock file stops other viewers / reruns starting it twice. Spec: MONTH_END.md.
MONTH_END_LOCK = os.path.join(BASE, ".month_end.lock")
MONTH_END_LOG = os.path.join(BASE, "month_end.log")


def _prev_month_key():
    last = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)
    return f"{last.year}-{last.month:02d}"


@st.cache_data(ttl=1800, show_spinner=False)
def _month_archived(key):
    """True when `key` is in Supabase (falls back to monthly_report_history.json). If neither
    can be read, say True — never start a heavy archive run blind."""
    url = os.environ.get("SUPABASE_DB_URL")
    if url:
        try:
            import psycopg2
            conn = psycopg2.connect(url, connect_timeout=10)
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1 FROM denri_mkt_monthly WHERE month_key = %s", (key,))
                    return cur.fetchone() is not None
            finally:
                conn.close()
        except Exception:                                        # noqa: BLE001
            pass
    try:
        with open(os.path.join(BASE, "monthly_report_history.json"), encoding="utf-8") as _fh:
            return key in _json.load(_fh)
    except (OSError, ValueError):
        return True


def _month_end_running(key):
    """A month_end run for `key` started in the last 3 hours (the lock holds 'key|epoch')."""
    try:
        with open(MONTH_END_LOCK, encoding="utf-8") as _fh:
            k, t = _fh.read().strip().split("|")
        return k == key and time.time() - float(t) < 3 * 3600
    except (OSError, ValueError):
        return False


if not NO_AUTOREFRESH:
    _pm = _prev_month_key()
    if _month_end_running(_pm):
        st.info(f"Archiving {datetime.datetime.strptime(_pm, '%Y-%m'):%B %Y} to History in the background — "
                "the pages refresh themselves when it finishes.", icon=":material/inventory:")
    elif not _month_archived(_pm):
        with open(MONTH_END_LOCK, "w", encoding="utf-8") as _fh:
            _fh.write(f"{_pm}|{time.time()}")
        _env = {**os.environ, "DENRI_REPORT_MONTH": _pm, "DENRI_MONTH_END_AUTO": "1",
                "DENRI_LAUNCHER": "1", "PYTHONIOENCODING": "utf-8"}
        with open(MONTH_END_LOG, "a", encoding="utf-8") as _log:
            subprocess.Popen([sys.executable, os.path.join(BASE, "month_end.py")], cwd=BASE, env=_env,
                             stdout=_log, stderr=subprocess.STDOUT)
        _month_archived.clear()                                  # re-check once it has had time to finish
        st.info(f"{datetime.datetime.strptime(_pm, '%Y-%m'):%B %Y} wasn't in History yet — archiving it "
                "to Supabase now, in the background.", icon=":material/inventory:")


# ── Title row: page title + purpose (left) · live clock pill · Refresh (right) ──
# The clock is a tiny component (it needs JS to tick); it also reloads an idle tab every
# AUTO_REFRESH_MIN minutes so the auto-refresh check keeps firing with no clicks.
CLOCK_HTML = """
<div class="pill" title="Live clock · when this page's data was last rebuilt from Odoo"><span class="dot"></span><span id="clk"></span><span class="sep"></span><span class="upd">__AGO__</span></div>
<style>
  body{margin:0;background:transparent;font-family:'Inter','Segoe UI',system-ui,sans-serif;
       display:flex;justify-content:flex-end;align-items:center;height:100vh}
  .pill{position:relative;display:inline-flex;align-items:center;gap:0.45rem;padding:0.5rem 0.85rem;border-radius:999px;
        background:__RAISED__;border:1px solid __BORDER__;white-space:nowrap}
  /* the date pill's travelling purple → pink light (same as the KPI tiles and the nav bar) */
  @property --g{syntax:'<angle>';initial-value:0deg;inherits:false}
  .pill::after{content:'';position:absolute;inset:-1px;border-radius:inherit;padding:1.5px;pointer-events:none;
    background:conic-gradient(from var(--g),transparent 0deg 30deg,#a855f7 60deg,#ec4899 80deg,transparent 100deg 210deg,#a855f7 240deg,#ec4899 260deg,transparent 280deg);
    -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;
    mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);mask-composite:exclude;animation:gspin 5s linear infinite}
  @keyframes gspin{to{--g:360deg}}
  .dot{width:8px;height:8px;border-radius:50%;background:#10b981;display:inline-block;animation:pulse 1.8s ease-out infinite}
  #clk{font-size:0.74rem;color:__MID__;font-weight:600;font-variant-numeric:tabular-nums}
  .sep{width:1px;height:14px;background:__BORDER__}
  .upd{font-size:0.7rem;color:__LO__;font-weight:500}
  @media (max-width:330px){.sep,.upd{display:none}}
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
      d[n.getDay()]+' '+n.getDate()+' '+m[n.getMonth()]+
      ' \u00b7 '+p(n.getHours())+':'+p(n.getMinutes())+':'+p(n.getSeconds());
  }
  tick(); setInterval(tick,1000);
  setTimeout(function(){ try{ (window.top||window.parent||window).location.reload(); }catch(e){ location.reload(); } }, __RELOAD_MS__);
</script>
"""
CLOCK_HTML = (CLOCK_HTML.replace("__RAISED__", _V5["raised"]).replace("__BORDER__", _V5["border"])
              .replace("__MID__", _V5["mid"]).replace("__LO__", _V5["lo"])
              .replace("__RELOAD_MS__", str(_AUTO_SECS * 1000)))
if NO_AUTOREFRESH:   # no idle-tab reload either
    CLOCK_HTML = re.sub(r"\n  setTimeout\(function\(\)\{ try\{ \(window\.top.*?\n", "\n", CLOCK_HTML)

# The Reject Sale page also gets an Excel export button (bags · units · sale price).
_rj_export = os.path.join(BASE, "reject_sales_export.xlsx")
_rj_export_csv = os.path.join(BASE, "reject_sales_export.csv")
_show_export = (label == "Reject Sale") and (os.path.exists(_rj_export) or os.path.exists(_rj_export_csv))
# How long ago this page's data was rebuilt — shown inside the clock chip (no separate caption line).
if os.path.exists(html_path):
    _age_min = int(_page_age_secs(html_path) // 60)
    _ago = "just now" if _age_min < 1 else (f"{_age_min} min ago" if _age_min < 60
            else f"{_age_min // 60}h {_age_min % 60}m ago")
    _fresh = f"Updated {_ago} · auto {AUTO_REFRESH_MIN} min"
else:
    _fresh = "Not built yet"
CLOCK_HTML = CLOCK_HTML.replace("__AGO__", _fresh)
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
    _tt, _ck, _rc = st.columns([0.55, 0.34, 0.11], vertical_alignment="center")
with _tt:
    st.markdown(_title_html, unsafe_allow_html=True)
with _ck:
    components.html(CLOCK_HTML, height=44)
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
        window.frameElement.setAttribute('data-dash-page', '');   // lets the holder grow (CSS below)
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
