/* custom_range.js — pick a Custom From – To range for the page.
   Shared by New Products, Posting Yields and Bags On vs Off Offer (spec: docs/README.md › Custom range).

     CustomRange.attach({ key: 'np', page: 'New Products', selects: ['pc-period', …], current: NP.custom })

   Two ways in, one form:
   • a **Custom range** panel under the page sidebar's "Back to top" (page_sidebar.js) — always there on
     wide screens, showing the range in use;
   • every listed Period <select> gets "Custom range…" (or "Change range…") — choosing it keeps the
     dropdown where it was and opens the same form under it (phones, where the sidebar is a top strip).
   Apply / Clear reload the Streamlit app with ?page=<page>&crange=<key>:<from>:<to> (or <key>:clear); the app
   saves the page's range file, rebuilds the page from Odoo and opens it again — its dropdowns then carry
   "Custom (dd Mon – dd Mon)". current = the page's built range ({from, to, label} or null). Opened as a plain
   file (no Streamlit around it) the form shows the command to run instead. */
(function () {
  if (window.CustomRange) return;
  var PICK = '__pick_range';
  var css = document.createElement('style');
  css.textContent =
    '.crp{position:fixed;z-index:10000;width:min(300px,calc(100vw - 24px));padding:0.75rem 0.85rem;border-radius:10px;' +
    'background:#1e2130;border:1px solid #4f46e5;color:#e2e8f0;font:0.76rem "Segoe UI",system-ui,sans-serif;' +
    'box-shadow:0 12px 30px rgba(0,0,0,0.45)}' +
    '.crf .t{font-weight:800;letter-spacing:0.06em;text-transform:uppercase;font-size:0.66rem;color:#a5b4fc;margin-bottom:0.5rem}' +
    '.crf .r{display:grid;grid-template-columns:1fr 1fr;gap:0.5rem}' +
    '.crf label{display:flex;flex-direction:column;gap:0.2rem;color:#94a3b8;font-size:0.68rem;min-width:0}' +
    '.crf input{background:#0f1117;border:1px solid #2d3148;color:#e2e8f0;border-radius:6px;padding:0.3rem 0.3rem;font:inherit;' +
    'font-size:0.72rem;color-scheme:dark;min-width:0;width:100%;box-sizing:border-box}' +
    '.crf .q{display:flex;flex-wrap:wrap;gap:0.3rem;margin-top:0.5rem}' +
    '.crf .q button{all:unset;cursor:pointer;font-size:0.66rem;padding:0.12rem 0.45rem;border-radius:999px;background:#252840;color:#cbd5e1}' +
    '.crf .q button:hover{background:#312e81}' +
    '.crf .b{display:flex;gap:0.4rem;justify-content:flex-end;margin-top:0.65rem}' +
    '.crf .b button{all:unset;cursor:pointer;padding:0.3rem 0.7rem;border-radius:6px;font-weight:700;font-size:0.72rem;border:1px solid #2d3148;color:#cbd5e1;text-align:center}' +
    '.crf .b button.go{background:#4f46e5;border-color:#4f46e5;color:#fff}' +
    '.crf .b button:disabled{opacity:0.4;cursor:default}' +
    '.crf .e{color:#fca5a5;font-size:0.68rem;margin-top:0.4rem}' +
    '.crf .e:empty{display:none}' +
    '.crf .n{color:#64748b;font-size:0.66rem;margin-top:0.35rem}' +
    /* sidebar panel (under "Back to top") */
    '.hsb-cr{margin-top:0.9rem;padding:0.7rem 0.55rem 0.2rem;border-top:1px solid #2d3148}' +
    '.hsb-cr .t{padding:0;margin:0 0 0.45rem;color:#64748b;letter-spacing:0.12em;font-size:0.62rem}' +
    '.hsb-cr .cur{display:flex;align-items:center;gap:0.4rem;margin-bottom:0.55rem;font-size:0.72rem;color:#94a3b8}' +
    '.hsb-cr .cur b{color:#a5b4fc;font-weight:700}' +
    '.hsb-cr .cur i{width:7px;height:7px;border-radius:50%;background:#475569;flex-shrink:0}' +
    '.hsb-cr .cur.on i{background:#818cf8;box-shadow:0 0 6px #818cf8}' +
    '.hsb-cr .b{justify-content:stretch}.hsb-cr .b button{flex:1}' +
    '.hsb-cr .r{grid-template-columns:1fr;gap:0.4rem}.hsb-cr label{flex-direction:row;align-items:center;gap:0.4rem}' +
    '.hsb-cr label input{flex:1}.hsb-cr .q button{font-size:0.62rem}' +
    '@media (max-width:980px){.hsb-cr{display:none}}';
  (document.head || document.documentElement).appendChild(css);

  var pop = null, opts = null;
  function iso(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function close() { if (pop) pop.style.display = 'none'; }

  function topWin() {
    try { if (window.top !== window && window.top.location.href) return window.top; } catch (e) {}
    return null;
  }

  function go(value) {
    var t = topWin();
    if (!t) return false;
    var u = new URL(t.location.href);
    u.searchParams.set('page', opts.page);
    u.searchParams.set('crange', opts.key + ':' + value);
    // The page frame's sandbox has no allow-top-navigation, so the frame itself can't move the app.
    // It is same-origin, though: schedule the navigation on the app window, so the app navigates itself.
    try { t.setTimeout(new t.Function('u', 'window.location.href = u;'), 0, u.toString()); }
    catch (e) { t.location.href = u.toString(); }
    return true;
  }

  // Fill `box` with the From / To form. inPanel = the sidebar version (no Cancel, Clear always shown when set).
  function form(box, inPanel) {
    var today = new Date(), cur = opts.current || null;
    var first = new Date(today.getFullYear(), today.getMonth(), 1);
    box.classList.add('crf');
    box.innerHTML = '<div class="t">Custom range</div>' +
      (inPanel ? '<div class="cur' + (cur ? ' on' : '') + '"><i></i>' + (cur ? 'In use: <b>' + esc(cur.label) + '</b>' : 'Not set — pick dates') + '</div>' : '') +
      '<div class="r"><label>From<input type="date" class="f"></label><label>To<input type="date" class="to"></label></div>' +
      '<div class="q"><button type="button" data-q="7">Last 7 days</button><button type="button" data-q="30">Last 30 days</button>' +
      '<button type="button" data-q="lm">Last month</button><button type="button" data-q="tm">This month</button></div>' +
      '<div class="e"></div>' +
      '<div class="b">' + (cur ? '<button type="button" class="clr">Clear</button>' : '') +
      (inPanel ? '' : '<button type="button" class="cn">Cancel</button>') + '<button type="button" class="go">Apply</button></div>' +
      (inPanel ? '' : '<div class="n">' + (cur ? 'Now: ' + esc(cur.label) + ' · ' : '') + 'rebuilds the page from Odoo for these dates</div>');
    var f = box.querySelector('.f'), to = box.querySelector('.to'), err = box.querySelector('.e');
    f.max = to.max = iso(today);
    f.value = cur ? cur.from : iso(first);
    to.value = cur ? cur.to : iso(today);
    box.querySelectorAll('[data-q]').forEach(function (b) {
      b.addEventListener('click', function () {
        var q = b.getAttribute('data-q'), a, z = new Date(today);
        if (q === 'lm') { a = new Date(today.getFullYear(), today.getMonth() - 1, 1); z = new Date(today.getFullYear(), today.getMonth(), 0); }
        else if (q === 'tm') a = first;
        else { a = new Date(today); a.setDate(a.getDate() - (+q - 1)); }
        f.value = iso(a); to.value = iso(z); err.textContent = '';
      });
    });
    var cn = box.querySelector('.cn'); if (cn) cn.addEventListener('click', close);
    var clr = box.querySelector('.clr');
    if (clr) clr.addEventListener('click', function () {
      this.disabled = true; this.textContent = 'Clearing…';
      if (!go('clear')) { this.disabled = false; this.textContent = 'Clear';
        err.textContent = 'Open this page in the dashboard, or run: python <page script> clear'; }
    });
    box.querySelector('.go').addEventListener('click', function () {
      var a = f.value, b = to.value;
      if (!a || !b) { err.textContent = 'Pick both a From and a To date.'; return; }
      if (a > b) { var x = a; a = b; b = x; }
      if ((new Date(b) - new Date(a)) / 864e5 > 365) { err.textContent = 'Keep it to a year or less.'; return; }
      this.disabled = true; this.textContent = 'Building…';
      if (!go(a + ':' + b)) { this.disabled = false; this.textContent = 'Apply';
        err.textContent = 'Open this page in the dashboard to apply — or run: python <page script> ' + a + ' ' + b; }
    });
    return f;
  }

  function open(anchor) {
    if (!pop) { pop = document.createElement('div'); pop.className = 'crp'; pop.setAttribute('role', 'dialog'); document.body.appendChild(pop); }
    var f = form(pop, false);
    pop.style.display = 'block'; pop.style.left = '0px'; pop.style.top = '0px';
    var r = anchor.getBoundingClientRect(), pw = pop.offsetWidth, ph = pop.offsetHeight;
    var vw = document.documentElement.clientWidth, vh = document.documentElement.clientHeight;
    pop.style.left = Math.max(12, Math.min(r.right - pw, vw - pw - 12)) + 'px';
    pop.style.top = ((r.bottom + 6 + ph > vh && r.top - 6 - ph > 0) ? r.top - 6 - ph : r.bottom + 6) + 'px';
    f.focus();
  }

  // The sidebar panel: placed right after the sidebar's "Back to top" once page_sidebar.js has built it.
  function mountPanel(tries) {
    var aside = document.getElementById('hsb'), topBtn = aside && aside.querySelector('.hsb-top');
    if (!topBtn) { if (tries < 40) setTimeout(function () { mountPanel(tries + 1); }, 150); return; }
    if (aside.querySelector('.hsb-cr')) return;
    var box = document.createElement('div');
    box.className = 'hsb-cr';
    topBtn.parentNode.insertBefore(box, topBtn.nextSibling);
    form(box, true);
  }

  function attach(o) {
    opts = o;
    var ids = o.selects || [];
    ids.forEach(function (id) {
      var el = document.getElementById(id); if (!el) return;
      if (o.current && !el.querySelector('option[value="custom"]')) {
        var c = document.createElement('option'); c.value = 'custom'; c.textContent = 'Custom (' + o.current.label + ')';
        el.appendChild(c);
        if (o.selectCurrent !== false) el.value = 'custom';
      }
      var p = document.createElement('option'); p.value = PICK;
      p.textContent = o.current ? 'Change range…' : 'Custom range…';
      el.appendChild(p);
      el.__crPrev = el.value;
      el.addEventListener('focus', function () { el.__crPrev = el.value; });
    });
    // Capture phase on the document runs before the page's own change handlers, so they never see PICK.
    document.addEventListener('change', function (ev) {
      var el = ev.target;
      if (!el || ids.indexOf(el.id) < 0) return;
      if (el.value === PICK) {
        ev.stopImmediatePropagation(); ev.stopPropagation();
        el.value = el.__crPrev && el.__crPrev !== PICK ? el.__crPrev : el.options[0].value;
        open(el);
      } else {
        el.__crPrev = el.value;
      }
    }, true);
    document.addEventListener('mousedown', function (ev) { if (pop && pop.style.display === 'block' && !pop.contains(ev.target)) close(); }, true);
    document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') close(); });
    mountPanel(0);
  }

  window.CustomRange = { attach: attach, close: close };
})();
