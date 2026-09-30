/* welcome_screen.js — the dashboard's welcome / loading card (spec: docs/README.md › Where changes go).
   streamlit_app.py runs it inside a zero-height component (same origin) with window.DW_CONFIG set:
     { theme: 'light'|'dark', page: '<label>', pages: [{label}], jumps: ['Insights', …],
       owner: { name, title_short, email } }
   It draws into the PARENT (Streamlit) document:
     - <meta name="darkreader-lock"> — the dashboard has its own light/dark theme, so the Dark Reader
       extension must not re-darken it;
     - the welcome card, once per browser session, while the first page loads; it steps aside by itself
       ~1.5 s after the page's frame has rendered. "Show on start" (localStorage denri_welcome) turns it off. */
(function () {
  'use strict';
  var C = window.DW_CONFIG || {}, P, W;
  try { P = window.parent.document; W = window.parent; } catch (e) { return; }   // needs the same-origin parent
  if (!P || !P.head) return;

  // ── Dark Reader lock (every run — cheap and idempotent) ──
  if (!P.querySelector('meta[name="darkreader-lock"]')) {
    var lock = P.createElement('meta'); lock.name = 'darkreader-lock'; P.head.appendChild(lock);
  }

  function lsGet(k) { try { return W.localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { W.localStorage.setItem(k, v); } catch (e) {} }
  function ssGet(k) { try { return W.sessionStorage.getItem(k); } catch (e) { return null; } }
  function ssSet(k, v) { try { W.sessionStorage.setItem(k, v); } catch (e) {} }

  if (lsGet('denri_welcome') === 'off') return;         // viewer opted out
  if (ssGet('denri_welcome_seen')) return;             // once per browser session (Streamlit reruns a lot)
  if (P.getElementById('dw-splash')) return;
  ssSet('denri_welcome_seen', '1');

  var dark = C.theme === 'dark', owner = C.owner || {};
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function svg(body, size) {
    return '<svg width="' + (size || 18) + '" height="' + (size || 18) + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>';
  }
  var ICON = {
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    moon: '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
    page: '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    cal: '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    Insights: '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>',
    'Monthly Report': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h8"/>',
    History: '<path d="M3 3v5h5"/><path d="M3.05 13A9 9 0 1 0 6 5.3L3 8"/><path d="M12 7v5l4 2"/>'
  };
  var stars = [[22,30,.9,.8],[58,64,.6,.6],[95,22,.7,.7],[130,80,.5,.5],[170,40,.9,.8],[204,70,.6,.6],[240,28,.8,.7],
               [276,58,.6,.6],[40,110,.5,.5],[112,120,.6,.45],[226,112,.5,.5],[264,138,.7,.5]].map(function (s) {
    return '<circle cx="' + s[0] + '" cy="' + s[1] + '" r="' + s[2] + '" fill="#fff" opacity="' + s[3] + '"/>'; }).join('');
  var SCENE = '<svg class="dw-scene" viewBox="0 0 300 520" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><defs>' +
    '<linearGradient id="dwSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07121a"/><stop offset=".55" stop-color="#15303b"/><stop offset="1" stop-color="#1d3a44"/></linearGradient>' +
    '<linearGradient id="dwLake" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2b33"/><stop offset="1" stop-color="#070d11"/></linearGradient>' +
    '<linearGradient id="dwShade" x1="0" y1="0" x2="0" y2="1"><stop offset=".3" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></linearGradient></defs>' +
    '<rect width="300" height="520" fill="url(#dwSky)"/>' + stars +
    '<path d="M0 300 45 250 80 268 150 150 185 205 215 182 262 240 300 262V520H0Z" fill="#445c6c"/>' +
    '<path d="M150 150 185 205 215 182 300 262V330H170Z" fill="#2c404d" opacity=".85"/>' +
    '<path d="M150 150 128 196 142 190 150 212 163 194 175 200 185 205Z" fill="#e8f0f4"/>' +
    '<path d="M215 182 200 206 214 200 222 212 232 200Z" fill="#dbe6ec"/>' +
    '<path d="M0 348 50 318 100 334 160 308 222 330 300 314V520H0Z" fill="#0f1b22"/>' +
    '<rect y="372" width="300" height="148" fill="url(#dwLake)"/><rect width="300" height="520" fill="url(#dwShade)"/></svg>';

  var CSS = [
    '#dw-splash { --bg:' + (dark ? '#0b0d14' : '#e8ecf0') + '; --card:' + (dark ? '#151826' : '#ffffff') + '; --ink:' + (dark ? '#f1f5f9' : '#111827') + ';',
    '  --mid:' + (dark ? '#94a3b8' : '#6b7280') + '; --field:' + (dark ? '#1c2030' : '#f3f4f6') + '; --teal:' + (dark ? '#45b8d6' : '#2b9fbf') + ';',
    '  --btn:' + (dark ? '#f1f5f9' : '#17181c') + '; --btn-ink:' + (dark ? '#0f1117' : '#ffffff') + '; --ease:cubic-bezier(0.16,1,0.3,1);',
    '  position:fixed; inset:0; z-index:1000100; overflow-y:auto; display:flex; align-items:center; justify-content:center; padding:56px 16px;',
    '  background:var(--bg); font-family:Inter,"Segoe UI",system-ui,sans-serif; transition:opacity .5s var(--ease), visibility .5s; }',
    '#dw-splash * { box-sizing:border-box; margin:0; }',
    '#dw-splash.hide { opacity:0; visibility:hidden; }',
    '#dw-splash .dw-card { position:relative; display:grid; grid-template-columns:92px 1fr 1fr; width:min(780px,100%); min-height:420px; margin:auto;',
    '  background:var(--card); border-radius:18px; box-shadow:0 30px 70px rgba(16,24,40,.12); animation:dwIn .6s var(--ease) both; transition:transform .5s var(--ease); }',
    '#dw-splash.hide .dw-card { transform:scale(.97) translateY(10px); }',
    '@keyframes dwIn { from { opacity:0; transform:translateY(14px); } }',
    '#dw-splash .dw-rail { display:flex; flex-direction:column; align-items:center; padding:56px 0 28px; }',
    '#dw-splash .dw-logo { width:42px; height:42px; border-radius:12px; display:flex; align-items:center; justify-content:center; background:var(--ink); color:var(--card); font-weight:800; font-size:.82rem; }',
    '#dw-splash .dw-tabs { flex:1; display:flex; flex-direction:column; justify-content:center; gap:30px; align-self:stretch; }',
    '#dw-splash .dw-tab { position:relative; display:flex; flex-direction:column; align-items:center; gap:6px; padding:8px 0; border:0; background:none; color:var(--mid); font:500 .78rem inherit; font-family:inherit; cursor:pointer; }',
    '#dw-splash .dw-tab.on { color:var(--teal); }',
    '#dw-splash .dw-tab.on::before { content:""; position:absolute; left:0; top:4px; bottom:4px; width:4px; border-radius:0 4px 4px 0; background:var(--teal); }',
    '#dw-splash .dw-photo { position:relative; margin:-38px 0; border-radius:18px; overflow:hidden; display:flex; align-items:flex-end; justify-content:center; text-align:center; color:#fff; box-shadow:0 28px 50px rgba(0,0,0,.35); }',
    '#dw-splash .dw-scene { position:absolute; inset:0; width:100%; height:100%; }',
    '#dw-splash .dw-ptext { position:relative; padding:0 20px 64px; text-shadow:0 2px 12px rgba(0,0,0,.45); }',
    '#dw-splash .dw-ptext h2 { font-size:1.75rem; font-weight:600; color:#fff; }',
    '#dw-splash .dw-ptext p { font-size:.86rem; opacity:.85; margin-top:4px; }',
    '#dw-splash .dw-meta { display:block; margin-top:22px; font-size:.72rem; opacity:.6; }',
    '#dw-splash .dw-credit { display:block; margin-top:6px; font-size:.72rem; opacity:.9; }',
    '#dw-splash .dw-credit b { background:linear-gradient(90deg,#a5b4fc,#67e8f9,#6ee7b7); -webkit-background-clip:text; background-clip:text; color:transparent; }',
    '#dw-splash .dw-panel { min-width:0; display:flex; flex-direction:column; padding:30px 28px 28px; color:var(--ink); }',
    '#dw-splash .dw-help { align-self:flex-end; font-size:.76rem; color:var(--mid); margin-bottom:18px; }',
    '#dw-splash .dw-help a { color:var(--teal); font-weight:600; text-decoration:none; }',
    '#dw-splash .dw-label { font-size:.8rem; font-weight:500; margin:0 0 6px; }',
    '#dw-splash .dw-field { display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:14px; padding:.72rem .8rem; border-radius:10px; background:var(--field); border:1.5px solid transparent; font-size:.82rem; color:var(--mid); }',
    '#dw-splash .dw-focus { background:var(--card); border-color:var(--teal); color:var(--ink); }',
    '#dw-splash .dw-row { display:flex; align-items:center; justify-content:space-between; margin:4px 0 20px; font-size:.8rem; }',
    '#dw-splash .dw-check { display:inline-flex; align-items:center; gap:8px; cursor:pointer; }',
    '#dw-splash .dw-check input { width:16px; height:16px; accent-color:var(--teal); }',
    '#dw-splash .dw-link { background:none; border:0; font:600 .8rem inherit; font-family:inherit; color:var(--teal); cursor:pointer; }',
    '#dw-splash .dw-go { position:relative; overflow:hidden; width:100%; padding:.85rem; border:0; border-radius:10px; background:var(--btn); color:var(--btn-ink); font:600 .86rem inherit; font-family:inherit; cursor:pointer; }',
    '#dw-splash .dw-go:disabled { cursor:progress; }',
    '#dw-splash .dw-fill { position:absolute; inset:0 auto 0 0; width:0; background:color-mix(in srgb, var(--teal) 55%, transparent); transition:width 4s cubic-bezier(.1,.7,.3,1); }',
    '#dw-splash .dw-go:not(:disabled) .dw-fill { opacity:0; transition:opacity .4s; }',
    '#dw-splash .dw-go-text { position:relative; }',
    '#dw-splash .dw-or { text-align:center; font-size:.76rem; color:var(--mid); margin:18px 0 10px; }',
    '#dw-splash .dw-jumps { display:flex; justify-content:center; gap:10px; }',
    '#dw-splash .dw-jump { width:50px; height:42px; border-radius:10px; border:0; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; background:var(--field); color:var(--ink); }',
    '#dw-splash .dw-jump:hover { color:var(--teal); }',
    '#dw-splash button:focus-visible { outline:2px solid var(--teal); outline-offset:2px; }',
    '@media (max-width:720px) { #dw-splash { padding:16px; align-items:flex-start; } #dw-splash .dw-card { grid-template-columns:minmax(0,1fr); min-height:0; }',
    '  #dw-splash .dw-rail { display:none; } #dw-splash .dw-photo { margin:0; min-height:200px; border-radius:18px 18px 0 0; box-shadow:none; }',
    '  #dw-splash .dw-ptext { padding-bottom:28px; } #dw-splash .dw-panel { padding:20px 18px 22px; } }',
    '@media (prefers-reduced-motion: reduce) { #dw-splash, #dw-splash * { animation:none !important; transition:none !important; } }'
  ].join('\n');

  var st = P.createElement('style'); st.id = 'dw-css'; st.textContent = CSS; P.head.appendChild(st);

  var today = new Date().toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  var jumps = (C.jumps || []).map(function (l) {
    return '<button type="button" class="dw-jump" data-page="' + esc(l) + '" title="' + esc(l) + '" aria-label="Open ' + esc(l) + '">' + svg(ICON[l] || ICON.page) + '</button>';
  }).join('');
  var el = P.createElement('div');
  el.id = 'dw-splash'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-modal', 'true'); el.setAttribute('aria-labelledby', 'dw-title');
  el.innerHTML =
    '<div class="dw-card">' +
      '<div class="dw-rail"><div class="dw-logo">DA</div><div class="dw-tabs" role="group" aria-label="Colour theme">' +
        '<button type="button" class="dw-tab' + (dark ? '' : ' on') + '" data-theme="light">' + svg(ICON.sun, 22) + 'Light</button>' +
        '<button type="button" class="dw-tab' + (dark ? ' on' : '') + '" data-theme="dark">' + svg(ICON.moon, 22) + 'Dark</button>' +
      '</div></div>' +
      '<div class="dw-photo">' + SCENE + '<div class="dw-ptext"><h2 id="dw-title">Welcome back</h2><p>Your marketing dashboards are loading</p>' +
        '<span class="dw-meta">Denri Africa · Marketing Analytics</span>' +
        (owner.name ? '<span class="dw-credit">Dashboard by <b>' + esc(owner.name) + '</b> ✦ · ' + esc(owner.title_short || owner.title || '') + '</span>' : '') +
      '</div></div>' +
      '<div class="dw-panel">' +
        (owner.email ? '<div class="dw-help">Need help? <a href="mailto:' + esc(owner.email) + '" target="_blank">Contact</a></div>' : '') +
        '<div class="dw-label">Opening</div><div class="dw-field dw-focus"><span>' + esc(C.page || '') + '</span>' + svg(ICON.page) + '</div>' +
        '<div class="dw-label">Today</div><div class="dw-field"><span>' + esc(today) + '</span>' + svg(ICON.cal) + '</div>' +
        '<div class="dw-row"><label class="dw-check"><input type="checkbox" id="dw-remember" checked> Show on start</label>' +
          '<button type="button" class="dw-link" id="dw-skip">Skip intro</button></div>' +
        '<button type="button" class="dw-go" id="dw-go" disabled><span class="dw-fill" id="dw-fill"></span><span class="dw-go-text" id="dw-go-text">Loading data…</span></button>' +
        (jumps ? '<div class="dw-or">Or jump straight to</div><div class="dw-jumps">' + jumps + '</div>' : '') +
      '</div>' +
    '</div>';
  P.body.appendChild(el);

  var start = Date.now(), timer = null, closed = false;
  function close() {
    if (closed) return; closed = true; clearTimeout(timer);
    el.classList.add('hide');
    setTimeout(function () { el.remove(); var c = P.getElementById('dw-css'); if (c) c.remove(); }, 600);
  }
  function go(q) {   // Streamlit selects the page / theme from the URL
    var u = new W.URL(W.location.href);
    Object.keys(q).forEach(function (k) { u.searchParams.set(k, q[k]); });
    W.location.href = u.toString();
  }
  el.querySelector('#dw-skip').addEventListener('click', close);
  el.querySelector('#dw-go').addEventListener('click', close);
  el.querySelector('#dw-remember').addEventListener('change', function (e) { lsSet('denri_welcome', e.target.checked ? 'on' : 'off'); });
  el.querySelectorAll('.dw-jump').forEach(function (b) { b.addEventListener('click', function () { close(); go({ page: b.getAttribute('data-page') }); }); });
  el.querySelectorAll('.dw-tab').forEach(function (b) { b.addEventListener('click', function () { if (!b.classList.contains('on')) go({ theme: b.getAttribute('data-theme') }); }); });
  W.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  setTimeout(function () { var f = el.querySelector('#dw-fill'); if (f) f.style.width = '85%'; }, 60);

  // Ready = the dashboard page's frame has rendered (a visible iframe whose document holds the page).
  function pageReady() {
    return Array.prototype.some.call(P.querySelectorAll('iframe'), function (f) {
      try {
        var d = f.contentDocument;
        return f.offsetHeight > 50 && d && d.readyState === 'complete' && !!d.querySelector('.psb-layout, .section, .wrap, .container');
      } catch (e) { return false; }
    });
  }
  function markReady() {
    if (closed) return;
    var b = el.querySelector('#dw-go'); if (!b.disabled) return;
    el.querySelector('#dw-fill').style.width = '100%';
    b.disabled = false; el.querySelector('#dw-go-text').textContent = 'Open dashboard';
    try { b.focus({ preventScroll: true }); } catch (e) {}
    timer = setTimeout(close, Math.max(1500, 2800 - (Date.now() - start)));
  }
  var poll = setInterval(function () {
    if (closed) { clearInterval(poll); return; }
    if (pageReady()) { clearInterval(poll); markReady(); }
  }, 250);
  setTimeout(function () { clearInterval(poll); markReady(); }, 20000);   // never trap anyone behind a page that won't load
})();
