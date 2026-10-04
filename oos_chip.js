/* oos_chip.js — "Out of stock — call back" chips, shared by New Products, Self-made vs Running
   Combos and Bags on vs off Offer (spec: docs/*.md "Out of stock — call back").

   Data per bag (from lib/oos_callbacks.py): { total: distinct people, shops: [[shop, people], …],
   colours: [[colour, people, [[shop, people], …]], …] } — the popover lists shops, then each colour.
     OOS.chip(entry, waiting)   → HTML for "📞 N asked" / "📞 N waiting", '' when 0 / missing
     OOS.seg(id, value, opts)   → HTML for a small segmented toggle; OOS.onSeg(id, fn) wires it
   Hover OR tap a chip opens one popover listing shops high → low; an outside tap / Esc closes it.
   Colours use the page palette (dark); v5_theme.js remaps them for the light theme. */
(function () {
  if (window.OOS) return;
  var reg = [], pop = null, openFor = null;
  var NOTE = 'Bag recorded from June 2026';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  var css = document.createElement('style');
  css.textContent =
    '.oos-chip{display:inline-flex;align-items:center;gap:0.25rem;padding:0.08rem 0.45rem;border-radius:999px;' +
    'font-size:0.68rem;font-weight:600;line-height:1.5;white-space:nowrap;cursor:pointer;user-select:none;' +
    'background:rgba(245,158,11,0.14);color:#fcd34d;border:1px solid rgba(245,158,11,0.35);vertical-align:middle}' +
    '.oos-chip.wait{background:rgba(239,68,68,0.14);color:#fca5a5;border-color:rgba(239,68,68,0.38)}' +
    '.oos-chip:hover,.oos-chip:focus-visible,.oos-chip.on{border-color:#f59e0b;outline:none}' +
    '.oos-pop{position:fixed;z-index:9999;max-width:min(300px,calc(100vw - 24px));padding:0.6rem 0.75rem;' +
    'border-radius:10px;background:#1e2130;border:1px solid #3d4a5c;color:#e2e8f0;font-size:0.74rem;line-height:1.55;' +
    'box-shadow:0 10px 28px rgba(0,0,0,0.35)}' +
    '.oos-pop .h{font-weight:700;margin-bottom:0.25rem}' +
    '.oos-pop .h .bg{color:#fcd34d;text-transform:uppercase;letter-spacing:0.03em}' +
    '.oos-pop .row{display:flex;justify-content:space-between;gap:1rem}' +
    '.oos-pop .row b{font-variant-numeric:tabular-nums;color:#fcd34d}' +
    '.oos-pop .n{margin-top:0.35rem;color:#64748b;font-size:0.66rem}' +
    '.oos-pop{max-height:min(420px,calc(100vh - 24px));overflow:auto}' +
    '.oos-pop .sec{margin-top:0.45rem;padding-top:0.4rem;border-top:1px solid #2d3148;color:#94a3b8;font-size:0.64rem;text-transform:uppercase;letter-spacing:0.06em}' +
    '.oos-pop .col{margin-top:0.3rem}' +
    '.oos-pop .col .row span{font-weight:600}' +
    '.oos-pop .sh{color:#94a3b8;font-size:0.68rem;line-height:1.45}' +
    '.oos-pop .sh b{color:#fcd34d;font-weight:600}' +
    '.oos-pop .si{white-space:nowrap}' +
    '.oos-pop .stk{font-style:normal;font-size:0.62rem;font-weight:700;padding:0 0.3rem;border-radius:4px;margin-left:0.1rem}' +
    '.oos-pop .stk.ok{color:#6ee7b7;background:rgba(16,185,129,0.14)}' +
    '.oos-pop .stk.z{color:#fca5a5;background:rgba(239,68,68,0.16)}' +
    '.oos-pop .stk.on{color:#94a3b8;background:rgba(148,163,184,0.14)}' +
    '.oos-seg{display:inline-flex;flex-wrap:wrap;gap:0.2rem;padding:0.15rem;border-radius:8px;background:#161824;border:1px solid #2d3148}' +
    '.oos-seg button{all:unset;cursor:pointer;padding:0.18rem 0.55rem;border-radius:6px;font-size:0.7rem;color:#94a3b8;white-space:nowrap}' +
    '.oos-seg button.on{background:#252840;color:#e2e8f0;font-weight:600}' +
    '.oos-seg button:focus-visible{outline:1px solid #f59e0b}';
  (document.head || document.documentElement).appendChild(css);

  // bag = the bag's name, shown in the popover header and read out by screen readers.
  function chip(entry, waiting, bag) {
    if (!entry || !entry.total) return '';
    var id = reg.push({ e: entry, w: !!waiting, b: bag || '' }) - 1;
    return '<span class="oos-chip' + (waiting ? ' wait' : '') + '" tabindex="0" role="button" data-oos="' + id + '"' +
      ' aria-label="' + esc(bag ? bag + ': ' : '') + entry.total + (waiting ? ' people waiting' : ' people asked') + ' while out of stock — show shops">' +
      '📞 ' + entry.total + (waiting ? ' waiting' : ' asked') + '</span>';
  }

  function close() {
    if (pop) pop.style.display = 'none';
    if (openFor) openFor.classList.remove('on');
    openFor = null;
  }

  // "Mombasa 2 · 0 stk" — [shop, people, stock]; stock null = no shelf (Website → online).
  function shopItem(s) {
    var st = s.length > 2 ? s[2] : undefined, tag = '';
    if (st === null) tag = /^website$/i.test(s[0]) ? ' <i class="stk on">online</i>' : '';
    else if (st !== undefined) tag = ' <i class="stk ' + (st > 0 ? 'ok' : 'z') + '">' + st + ' stk</i>';
    return '<span class="si">' + esc(s[0]) + ' <b>' + s[1] + '</b>' + tag + '</span>';
  }

  function open(el) {
    var it = reg[+el.getAttribute('data-oos')];
    if (!it) return;
    if (openFor === el) return;
    close();
    if (!pop) { pop = document.createElement('div'); pop.className = 'oos-pop'; pop.setAttribute('role', 'tooltip'); document.body.appendChild(pop); }
    pop.innerHTML = '<div class="h">' + (it.b ? '<span class="bg">' + esc(it.b) + '</span> — ' : '') +
      it.e.total + (it.w ? ' still waiting' : ' asked') + ' while out of stock</div>' +
      '<div class="sec">By shop · in stock now</div><div class="sh">' + (it.e.shops || []).map(shopItem).join(' · ') + '</div>' +
      // Colours asked for, each with its own shops ("Black 63 — Ktda 23 · Eldoret 6").
      ((it.e.colours || []).length ? '<div class="sec">By colour</div>' + it.e.colours.map(function (c) {
        return '<div class="col"><div class="row"><span>' + esc(c[0]) + '</span><b>' + c[1] + '</b></div>' +
          '<div class="sh">' + (c[2] || []).map(shopItem).join(' · ') + '</div></div>';
      }).join('') : '') +
      '<div class="n">People, not requests · ' + NOTE + '</div>';
    pop.style.display = 'block';
    pop.style.left = '0px'; pop.style.top = '0px';
    var r = el.getBoundingClientRect(), pw = pop.offsetWidth, ph = pop.offsetHeight;
    var vw = document.documentElement.clientWidth, vh = document.documentElement.clientHeight;
    var left = Math.max(12, Math.min(r.left, vw - pw - 12));
    var top = (r.bottom + 6 + ph > vh && r.top - 6 - ph > 0) ? r.top - 6 - ph : r.bottom + 6;
    pop.style.left = left + 'px'; pop.style.top = top + 'px';
    el.classList.add('on');
    openFor = el;
  }

  function chipOf(t) { return t && t.closest ? t.closest('.oos-chip') : null; }
  document.addEventListener('mouseover', function (ev) { var c = chipOf(ev.target); if (c) open(c); });
  document.addEventListener('mouseout', function (ev) {
    var c = chipOf(ev.target);
    if (c && c === openFor && !(ev.relatedTarget && c.contains(ev.relatedTarget)) && !c.__tapped) close();
  });
  document.addEventListener('click', function (ev) {
    var c = chipOf(ev.target);
    if (c) {
      ev.stopPropagation();
      if (openFor === c && c.__tapped) { c.__tapped = false; close(); return; }
      open(c); c.__tapped = true;
      return;
    }
    if (openFor) { openFor.__tapped = false; close(); }
  }, true);
  document.addEventListener('keydown', function (ev) {
    var c = chipOf(ev.target);
    if (ev.key === 'Escape') close();
    else if (c && (ev.key === 'Enter' || ev.key === ' ')) { ev.preventDefault(); openFor === c ? close() : open(c); }
  });
  window.addEventListener('scroll', close, true);
  window.addEventListener('resize', close);

  // Segmented toggle. opts = [[value, label], …]
  function seg(id, value, opts) {
    return '<span class="oos-seg" id="' + esc(id) + '" role="group" aria-label="Call-back period">' +
      opts.map(function (o) {
        return '<button type="button" data-v="' + esc(o[0]) + '" class="' + (o[0] === value ? 'on' : '') + '"' +
          ' aria-pressed="' + (o[0] === value) + '">' + esc(o[1]) + '</button>';
      }).join('') + '</span>';
  }
  function onSeg(id, fn) {
    document.addEventListener('click', function (ev) {
      var b = ev.target && ev.target.closest ? ev.target.closest('#' + id + ' button[data-v]') : null;
      if (!b) return;
      var wrap = b.parentNode;
      Array.prototype.forEach.call(wrap.querySelectorAll('button'), function (x) {
        x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b);
      });
      fn(b.getAttribute('data-v'));
    });
  }
  function remember(key, val) {
    try { if (val === undefined) return window.localStorage.getItem(key); window.localStorage.setItem(key, val); }
    catch (e) { return null; }
  }

  window.OOS = { chip: chip, seg: seg, onSeg: onSeg, remember: remember, close: close, NOTE: NOTE };
})();
