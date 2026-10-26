/* ads_panel.js — the "Ads impact" panel on every page (spec: docs/ads-impact.md).
   Data: window.ADS_IMPACT = this page's section of data/ads_impact.json (injected by streamlit_app.py):
     { week, lead, tiles:[{k,v,n,tone}], tables:[{title, head:[], rows:[[cell|{t,c}]], note}], actions:[{kind, market, text}], foot }
   Draws a card at the end of the page (22 Oct 2026, user's call — the last thing on every menu): headline tiles always visible; "Details" opens the tables and every action.
   Colours use the page palette (dark); v5_theme.js remaps the <style> for the light theme. */
(function () {
  var S = window.ADS_IMPACT;
  if (!S || window.__adsPanel) return;
  window.__adsPanel = true;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  var KIND = { event: ['Event', 'ev'], watch: ['Watch', 'wa'], 'do': ['Do', 'do'], win: ['Working', 'wi'] };

  var css = document.createElement('style');
  css.textContent =
    '.ads-panel{position:relative;background:#1a1d2b;border:1px solid #2d3148;border-radius:14px;padding:1.1rem 1.25rem 1rem;margin:1.6rem 0 1.6rem;color:#cbd5e1;overflow:hidden}' +
    '.ads-panel::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#f59e0b,#ec4899,#8b5cf6)}' +
    '.ads-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:0.4rem 0.8rem;margin-bottom:0.2rem}' +
    '.ads-pill{font-size:0.62rem;font-weight:800;letter-spacing:0.08em;text-transform:uppercase;color:#fbbf24;border:1px solid rgba(251,191,36,0.45);border-radius:999px;padding:0.1rem 0.55rem}' +
    '.ads-title{font-size:1.02rem;font-weight:800;color:#f1f5f9}' +
    '.ads-week{font-size:0.78rem;color:#94a3b8}' +
    '.ads-lead{font-size:0.8rem;color:#94a3b8;margin:0 0 0.8rem}' +
    '.ads-tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:0.7rem;margin-bottom:0.8rem}' +
    '.ads-tile{background:rgba(148,163,184,0.06);border:1px solid rgba(148,163,184,0.12);border-radius:10px;padding:0.6rem 0.75rem}' +
    '.ads-tile .k{font-size:0.63rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#64748b}' +
    '.ads-tile .v{font-size:1.25rem;font-weight:800;color:#e2e8f0;margin-top:0.15rem;font-variant-numeric:tabular-nums}' +
    '.ads-tile .n{font-size:0.72rem;color:#94a3b8;margin-top:0.1rem;line-height:1.4}' +
    '.ads-up{color:#34d399!important}.ads-down{color:#fb7185!important}' +
    '.ads-acts{list-style:none;margin:0;padding:0;display:grid;gap:0.4rem}' +
    '.ads-acts li{display:grid;grid-template-columns:auto 1fr;gap:0.6rem;align-items:start;font-size:0.8rem;line-height:1.5;color:#cbd5e1}' +
    '.ads-tag{font-size:0.6rem;font-weight:800;letter-spacing:0.06em;text-transform:uppercase;border-radius:6px;padding:0.12rem 0.45rem;margin-top:0.12rem;white-space:nowrap;min-width:64px;text-align:center}' +
    '.ads-tag.ev{background:rgba(239,68,68,0.15);color:#fca5a5}.ads-tag.wa{background:rgba(245,158,11,0.15);color:#fcd34d}' +
    '.ads-tag.do{background:rgba(59,130,246,0.15);color:#93c5fd}.ads-tag.wi{background:rgba(16,185,129,0.15);color:#6ee7b7}' +
    '.ads-mk{color:#64748b;font-size:0.72rem;margin-right:0.35rem}' +
    '.ads-more{margin-top:0.7rem;background:none;border:1px solid rgba(148,163,184,0.25);color:#cbd5e1;border-radius:999px;padding:0.3rem 0.85rem;font-size:0.74rem;font-weight:600;cursor:pointer}' +
    '.ads-more:hover{border-color:#f59e0b;color:#fbbf24}' +
    '.ads-detail{margin-top:0.9rem}' +
    '.ads-sub{font-size:0.66rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#64748b;margin:0.9rem 0 0.4rem}' +
    '.ads-tw{overflow-x:auto}' +
    '.ads-t{width:100%;border-collapse:collapse;font-size:0.76rem;min-width:620px}' +
    '.ads-t th{text-align:right;font-size:0.62rem;letter-spacing:0.05em;text-transform:uppercase;color:#64748b;font-weight:700;padding:0.35rem 0.45rem;border-bottom:1px solid rgba(148,163,184,0.18);white-space:nowrap}' +
    '.ads-t td{text-align:right;padding:0.38rem 0.45rem;color:#cbd5e1;border-bottom:1px solid rgba(148,163,184,0.08);white-space:nowrap;font-variant-numeric:tabular-nums}' +
    '.ads-t th:first-child,.ads-t td:first-child,.ads-t th:nth-child(2),.ads-t td:nth-child(2){text-align:left}' +
    '.ads-note,.ads-foot{font-size:0.7rem;color:#64748b;margin-top:0.4rem;line-height:1.45}' +
    '.ads-foot{margin-top:0.8rem}' +
    '.ads-charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:0.8rem;margin-bottom:0.9rem}' +
    '.ads-chart{background:rgba(148,163,184,0.04);border:1px solid rgba(148,163,184,0.12);border-radius:10px;padding:0.7rem 0.8rem 0.6rem;min-width:0}' +
    '.ads-ch-head{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0.4rem 0.6rem;margin-bottom:0.45rem}' +
    '.ads-ch-t{font-size:0.66rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#94a3b8}' +
    '.ads-seg{display:inline-flex;flex-wrap:wrap;gap:2px;background:rgba(148,163,184,0.08);border-radius:14px;padding:2px}' +
    '.ads-seg button{background:none;border:0;color:#94a3b8;font-size:0.68rem;font-weight:600;padding:0.22rem 0.6rem;border-radius:999px;cursor:pointer}' +
    '.ads-seg button.on{background:#f59e0b;color:#111827}' +
    '.ads-cv{position:relative;height:230px}' +
    '.ads-leg{display:flex;flex-wrap:wrap;gap:0.3rem 0.9rem;font-size:0.7rem;color:#94a3b8;margin-top:0.4rem}' +
    '.ads-leg i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:0.3rem;vertical-align:-1px}' +
    '.ads-ch-n{font-size:0.68rem;color:#64748b;margin-top:0.3rem;line-height:1.4}';
  document.head.appendChild(css);

  function cell(c) {
    if (c && typeof c === 'object') return '<td class="' + (c.c ? 'ads-' + c.c : '') + '">' + esc(c.t) + '</td>';
    return '<td>' + esc(c) + '</td>';
  }
  function act(a) {
    var k = KIND[a.kind] || [a.kind, 'do'];
    return '<li><span class="ads-tag ' + k[1] + '">' + esc(k[0]) + '</span><span>' +
      (a.market ? '<span class="ads-mk">' + esc(a.market) + '</span>' : '') + esc(a.text) + '</span></li>';
  }

  var top = (S.actions || []).slice(0, 3), rest = (S.actions || []).slice(3);
  var h = '<div class="ads-head"><span class="ads-pill">Ads</span><span class="ads-title">Ads impact</span>' +
    '<span class="ads-week">week of ' + esc(S.week) + '</span></div>' +
    (S.lead ? '<p class="ads-lead">' + esc(S.lead) + '</p>' : '') +
    '<div class="ads-tiles">' + (S.tiles || []).map(function (t) {
      return '<div class="ads-tile"><div class="k">' + esc(t.k) + '</div><div class="v' + (t.tone ? ' ads-' + t.tone : '') + '">' +
        esc(t.v) + '</div><div class="n">' + esc(t.n) + '</div></div>';
    }).join('') + '</div>' +
    (S.chart ? '<div class="ads-charts">' +
      '<div class="ads-chart"><div class="ads-ch-head"><span class="ads-ch-t">Week on week</span><div class="ads-seg" id="ads-seg-wow"></div></div>' +
        '<div class="ads-cv"><canvas id="ads-cv-wow" role="img" aria-label="Ads week on week by market"></canvas></div><div class="ads-leg" id="ads-leg-wow"></div><div class="ads-ch-n" id="ads-n-wow"></div></div>' +
      '<div class="ads-chart"><div class="ads-ch-head"><span class="ads-ch-t">Week of ' + esc(S.week) + ', by campaign</span><div class="ads-seg" id="ads-seg-cmp"></div></div>' +
        '<div class="ads-cv"><canvas id="ads-cv-cmp" role="img" aria-label="Last week by campaign"></canvas></div><div class="ads-leg" id="ads-leg-cmp"></div><div class="ads-ch-n" id="ads-n-cmp"></div></div>' +
    '</div>' : '') +
    (top.length ? '<div class="ads-sub" style="margin-top:0">What we can do</div><ul class="ads-acts">' + top.map(act).join('') + '</ul>' : '') +
    '<div class="ads-detail" hidden>' +
      (rest.length ? '<ul class="ads-acts">' + rest.map(act).join('') + '</ul>' : '') +
      (S.tables || []).map(function (t) {
        return '<div class="ads-sub">' + esc(t.title) + '</div><div class="ads-tw"><table class="ads-t"><thead><tr>' +
          t.head.map(function (x) { return '<th>' + esc(x) + '</th>'; }).join('') + '</tr></thead><tbody>' +
          t.rows.map(function (r) { return '<tr>' + r.map(cell).join('') + '</tr>'; }).join('') + '</tbody></table></div>' +
          (t.note ? '<div class="ads-note">' + esc(t.note) + '</div>' : '');
      }).join('') +
      '<div class="ads-foot">' + esc(S.foot) + '</div>' +
    '</div>' +
    '<button type="button" class="ads-more">Details' + (rest.length ? ' and ' + rest.length + ' more actions' : '') + '</button>';

  function mount() {
    if (document.getElementById('ads-panel')) return;
    var box = document.createElement('section');
    box.className = 'ads-panel'; box.id = 'ads-panel'; box.innerHTML = h;
    var btn = box.querySelector('.ads-more'), det = box.querySelector('.ads-detail'), label = btn.textContent;
    btn.addEventListener('click', function () {
      det.hidden = !det.hidden;
      btn.textContent = det.hidden ? label : 'Hide details';
    });
    // The last thing on the page (22 Oct 2026). Find the page's top-level block that holds the first
    // section (a child of the page column / body). Pages that are a list of sections side by side at
    // that level get the panel after the last one; pages with one wrapper (.wrap, .container, main)
    // get it at the end of that wrapper, so it always spans the page width.
    var root = document.querySelector('.psb-main') || document.body;
    var top = document.querySelector('.section, section:not(#ads-panel), main, .container');
    while (top && top.parentNode && top.parentNode !== root && top.parentNode !== document.body) top = top.parentNode;
    if (!top || !top.parentNode) root.appendChild(box);
    else {
      var par = top.parentNode, cs = getComputedStyle(par);
      var secs = [].filter.call(par.children, function (c) { return c !== box && c.matches('.section, section, main'); });
      if (secs.length > 1) {
        var stacked = !/flex|grid/.test(cs.display) || (/flex/.test(cs.display) && /^column/.test(cs.flexDirection));
        if (stacked) par.appendChild(box); else secs[secs.length - 1].appendChild(box);
      } else top.appendChild(box);
    }
    if (S.chart) withChart(charts);
    // page_sidebar.js turns the page into a grid (sidebar | page column) — possibly after this ran,
    // and it may pick the panel up as a grid item. Keep the panel at the end of the page column, and
    // move it back to the end if the page adds more content after it (late-built sections).
    function lastShown(el) {
      var c = el.lastElementChild;
      while (c && (c.tagName === 'SCRIPT' || c.tagName === 'STYLE' || c.tagName === 'TEMPLATE')) c = c.previousElementSibling;
      return c;
    }
    function settle() {
      var main = document.querySelector('.psb-main') || box.parentNode;
      if (main && (box.parentNode !== main || lastShown(main) !== box)) main.appendChild(box);
    }
    settle();
    window.addEventListener('load', settle);
    [200, 800, 2000].forEach(function (t) { setTimeout(settle, t); });
    try {
      var mo = new MutationObserver(settle);
      mo.observe(document.body, { childList: true });
      setTimeout(function () { mo.disconnect(); }, 5000);
    } catch (e) {}
  }

  /* ── charts ─────────────────────────────────────────────── */
  // Markets = categorical slots 1–3 (blue, orange, aqua: validated together, dark steps).
  var MC = { Kenya: '#3987e5', Tanzania: '#d95926', Uganda: '#199e70' };
  var INK = '#94a3b8', GRID = 'rgba(148,163,184,0.10)', SURF = '#1a1d2b';
  function withChart(cb) {
    if (window.Chart) return cb();
    var sc = document.createElement('script');
    sc.src = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
    sc.onload = cb; document.head.appendChild(sc);
  }
  function fmt(v, unit) {
    if (v == null || isNaN(v)) return '';
    if (unit === 'kes') return 'KES ' + Math.round(v).toLocaleString('en-US');
    if (unit === 'pct') return v.toFixed(1) + '%';
    return Math.round(v).toLocaleString('en-US');
  }
  function short(v, unit) {
    var a = Math.abs(v), s = a >= 1e6 ? (v / 1e6).toFixed(1) + 'M' : a >= 1e3 ? Math.round(v / 1e3) + 'k' : Math.round(v) + '';
    return unit === 'pct' ? v.toFixed(1) + '%' : (unit === 'kes' ? 'KES ' + s : s);
  }
  function seg(id, opts, cur, fn) {
    var el = document.getElementById(id);
    el.innerHTML = opts.map(function (o) {
      return '<button type="button" data-k="' + o[0] + '"' + (o[0] === cur ? ' class="on"' : '') + '>' + esc(o[1]) + '</button>';
    }).join('');
    el.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      [].forEach.call(el.children, function (x) { x.classList.toggle('on', x === b); });
      fn(b.getAttribute('data-k'));
    });
  }
  function legend(id, names) {
    document.getElementById(id).innerHTML = names.map(function (n) {
      return '<span><i style="background:' + MC[n] + '"></i>' + esc(n) + '</span>';
    }).join('');
  }
  function axes(unit, stacked, horizontal) {
    var val = { stacked: stacked, beginAtZero: true, grid: { color: GRID }, border: { display: false },
                ticks: { color: INK, font: { size: 10 }, maxTicksLimit: 5, maxRotation: 0, callback: function (v) { return short(v, unit); } } };
    var cat = { stacked: stacked, grid: { display: false }, border: { display: false }, ticks: { color: INK, font: { size: 10 }, maxRotation: 0, autoSkip: false } };
    return horizontal ? { x: val, y: cat } : { x: cat, y: val };
  }

  function charts() {
    var C = S.chart, se = C.series, mk = C.markets;
    var focus = C.scope !== 'All ads';
    // [key, label, unit, sum = stacked bars by market | ratio = one line per market]
    var M = [['spend', 'Ad spend', 'kes', 'sum'], ['messages', 'Messages', 'n', 'sum'], ['cpm', 'Cost per message', 'kes', 'ratio'],
             ['bags', 'Bags sold', 'n', 'sum'], ['cpb', 'Ad cost per bag', 'kes', 'ratio'], ['share', 'Ads % of revenue', 'pct', 'ratio'],
             ['posts', 'Posts', 'n', 'sum']].filter(function (m) {
      var need = { cpm: 'messages', cpb: 'bags', share: 'revenue' }[m[0]] || m[0];
      return se[need] && !(focus && (m[0] === 'cpb' || m[0] === 'share'));
    });
    function values(key, m) {
      var w = C.weeks.map(function (_, i) { return i; });
      function r(n, d) { return w.map(function (i) { return se[d][m][i] ? se[n][m][i] / se[d][m][i] : null; }); }
      if (key === 'cpm') return r('chatSpend', 'messages');
      if (key === 'cpb') return r('spend', 'bags');
      if (key === 'share') return w.map(function (i) { return se.revenue[m][i] ? se.spend[m][i] / se.revenue[m][i] * 100 : null; });
      return se[key][m];
    }
    var wow = null;
    function drawWow(key) {
      var def = M.filter(function (m) { return m[0] === key; })[0], unit = def[2], sum = def[3] === 'sum';
      if (wow) wow.destroy();
      wow = new Chart(document.getElementById('ads-cv-wow'), {
        type: sum ? 'bar' : 'line',
        data: { labels: C.weeks, datasets: mk.map(function (m) {
          return sum
            ? { label: m, data: values(key, m), backgroundColor: MC[m], borderColor: SURF, borderWidth: { top: 2 },
                borderRadius: 4, borderSkipped: 'bottom', maxBarThickness: 46 }
            : { label: m, data: values(key, m), borderColor: MC[m], backgroundColor: MC[m], borderWidth: 2, pointRadius: 4,
                pointHoverRadius: 6, pointBorderColor: SURF, pointBorderWidth: 2, tension: 0.25, spanGaps: true };
        }) },
        options: { responsive: true, maintainAspectRatio: false, animation: { duration: 350 }, layout: { padding: { left: 4, right: 10 } },
          interaction: { mode: 'index', intersect: false },
          plugins: { legend: { display: false }, chartSwitch: false, weekChange: false,
            tooltip: { callbacks: {
              label: function (c) { return ' ' + c.dataset.label + ': ' + fmt(c.parsed.y, unit); },
              footer: sum ? function (items) {
                var t = items.reduce(function (s, i) { return s + (i.parsed.y || 0); }, 0); return 'All markets: ' + fmt(t, unit);
              } : undefined } } },
          scales: axes(unit, sum, false) }
      });
      document.getElementById('ads-n-wow').textContent =
        (focus && (key === 'spend' || key === 'messages' || key === 'cpm') ? C.scope + ' only. ' : '') +
        (key === 'spend' || key === 'cpb' || key === 'share' ? 'Google and X converted at the assumed USD rate. ' : '') +
        (key === 'messages' || key === 'cpm' ? 'Meta messages plus TikTok conversions. ' : '') +
        (key === 'bags' || key === 'cpb' || key === 'share' ? 'Bags and revenue are all POS sales in the market.' : '') +
        (key === 'posts' ? 'Posts from the marketing posting sheets.' : '');
    }
    legend('ads-leg-wow', mk);
    seg('ads-seg-wow', M.map(function (m) { return [m[0], m[1]]; }), M[0][0], drawWow);
    drawWow(M[0][0]);

    var cmp = null, camps = C.campaigns;
    var K = [['spend', 'Spend', 'kes'], ['messages', 'Messages', 'n'], ['cpm', 'Cost per message', 'kes']];
    function drawCmp(key) {
      var unit = K.filter(function (k) { return k[0] === key; })[0][2];
      var list = camps.filter(function (c) { return key === 'spend' || c.chat; }).map(function (c) {
        return { c: c, v: key === 'spend' ? c.spend : key === 'messages' ? c.results : c.cpr };
      }).filter(function (x) { return x.v != null; }).sort(function (a, b) { return b.v - a.v; });
      if (cmp) cmp.destroy();
      document.getElementById('ads-cv-cmp').parentNode.style.height = Math.max(150, list.length * 30 + 40) + 'px';
      cmp = new Chart(document.getElementById('ads-cv-cmp'), {
        type: 'bar',
        data: { labels: list.map(function (x) { return x.c.name; }),
                datasets: [{ data: list.map(function (x) { return x.v; }),
                             backgroundColor: list.map(function (x) { return MC[x.c.market]; }),
                             borderRadius: 4, borderSkipped: 'start', maxBarThickness: 18 }] },
        options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, animation: { duration: 350 },
          layout: { padding: { left: 10, right: 64 } },
          plugins: { legend: { display: false }, chartSwitch: false, weekChange: false,
            tooltip: { callbacks: {
              label: function (c) {
                var x = list[c.dataIndex].c;
                var out = [' ' + x.market + ': ' + fmt(c.parsed.x, unit) + (x.usd && key === 'spend' ? ' (≈, paid in USD)' : '')];
                if (key !== 'cpm') out.push(' ' + Math.round(x.results).toLocaleString('en-US') + ' ' + x.type);
                if (x.cpr != null) {
                  var ch = x.avg3 ? (x.cpr / x.avg3 - 1) * 100 : null;
                  out.push(' ' + fmt(x.cpr, 'kes') + ' per message' + (x.avg3
                    ? ', 3-week average ' + fmt(x.avg3, 'kes') + ' (' + (ch >= 0 ? '+' : '') + ch.toFixed(0) + '%)'
                    : ', new this week'));
                }
                return out;
              } } } },
          scales: axes(unit, false, true) },
        plugins: [{ id: 'adsEndLabels', afterDatasetsDraw: function (ch) {
          var ctx = ch.ctx, meta = ch.getDatasetMeta(0);
          ctx.save(); ctx.font = '600 10px system-ui, sans-serif'; ctx.fillStyle = '#cbd5e1'; ctx.textBaseline = 'middle';
          meta.data.forEach(function (b, i) { ctx.fillText(short(list[i].v, unit), b.x + 6, b.y); });
          ctx.restore();
        } }]
      });
      document.getElementById('ads-n-cmp').textContent = key === 'spend'
        ? 'Every campaign, KES and USD (≈) together. Colour = market.'
        : 'Chat campaigns only (Meta messages, TikTok conversions). Hover for the 3-week average.';
    }
    legend('ads-leg-cmp', mk.filter(function (m) { return camps.some(function (c) { return c.market === m; }); }));
    seg('ads-seg-cmp', K.map(function (k) { return [k[0], k[1]]; }), 'spend', drawCmp);
    drawCmp('spend');
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
