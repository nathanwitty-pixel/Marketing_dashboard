/* assets/growth_tracking.js — "Growth Rate — Monthly & Annual" and "Month-on-Month Tracking" sections for the Monthly
   Report (docs/monthly-report.md › Growth rate & month-on-month tracking). Same look as History's sections 10 / 11.

   GrowthTracking.render(el, GT, opts) — GT = data/growth_tracking.json (+ the live month, see below);
   opts = {month: 'November', year: 2026, num1: '10', num2: '11'}.
   GT.live (optional) = {month, year, soFar, projected, day, days, row: {…tracking row…}} — the month in progress:
   shown in the tables as "so far" (growth with the projected total), left off the waterfalls (a part month isn't a fair bar). */
(function () {
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var GRID = 'rgba(45,49,72,0.55)';
  var nf = function (n) { return Math.round(Number(n) || 0).toLocaleString('en-US'); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var ttl = function (t) { return String(t || '').toLowerCase().replace(/\b\w/g, function (c) { return c.toUpperCase(); }); };
  var sg = function (v, note) { return v == null ? '<span style="color:#475569">—</span>' : '<b style="color:' + (v >= 0 ? '#34d399' : '#f87171') + '">' + (v >= 0 ? '+' : '') + v.toFixed(2) + '%</b>' + (note || ''); };
  var TD = 'padding:0.4rem 0.7rem;border-top:1px solid #262a3d;font-variant-numeric:tabular-nums';
  var TH = 'text-align:left;padding:0.45rem 0.7rem;font-size:0.64rem;text-transform:uppercase;letter-spacing:0.06em;color:#64748b;border-bottom:1px solid #2d3148';
  function table(cols, rows) {
    return '<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:0.8rem"><thead><tr>'
      + cols.map(function (c) { return '<th style="' + TH + (c.r ? ';text-align:right' : '') + '">' + c.h + '</th>'; }).join('') + '</tr></thead><tbody>'
      + rows.map(function (r) { return '<tr>' + r.map(function (v, i) { return '<td style="' + TD + (cols[i].r ? ';text-align:right' : '') + (i === 0 ? ';color:#f1f5f9;font-weight:600' : ';color:#cbd5e1') + '">' + v + '</td>'; }).join('') + '</tr>'; }).join('')
      + '</tbody></table></div>';
  }
  var charts = {};
  function wf(id, headId, cfg) {
    var el = document.getElementById(id); if (!el || !window.Chart || !cfg.items.length) return;
    if (charts[id]) { try { charts[id].destroy(); } catch (e) {} }
    var items = cfg.items, run = cfg.start, bars = [[0, cfg.start]], levels = [cfg.start];
    items.forEach(function (x) { bars.push([run, run + x.delta]); run += x.delta; levels.push(run); });
    var end = run; bars.push([0, end]); levels.push(end);
    var up = end >= cfg.start, mark = -1;
    items.forEach(function (x, i) { if ((up ? x.delta > 0 : x.delta < 0) && (mark < 0 || Math.abs(x.delta) > Math.abs(items[mark].delta))) mark = i; });
    var lo = Math.min.apply(null, levels), hi = Math.max.apply(null, levels), span = Math.max(hi - lo, 1);
    var stepR = Math.pow(10, Math.floor(Math.log10(span))), yMin = lo > 0.5 * hi ? Math.max(0, Math.floor((lo - span * 0.6) / stepR) * stepR) : 0;
    var hd = document.getElementById(headId);
    if (hd) hd.innerHTML = cfg.head + '<div style="font-size:0.72rem;font-weight:400;color:#94a3b8;margin-top:0.1rem">' + nf(cfg.start) + ' → ' + nf(end) + ' bags'
      + (yMin ? '. Axis starts at ' + nf(yMin) : '') + (cfg.extra ? '<br>' + cfg.extra : '') + '</div>';
    var lbl = { id: 'gtLabels', afterDatasetsDraw: function (ch) {
      var ctx = ch.ctx, meta = ch.getDatasetMeta(0);
      ctx.save(); ctx.textAlign = 'center';
      meta.data.forEach(function (e, i) {
        var top = Math.min(e.y, e.base), bottom = Math.max(e.y, e.base), isEnd = i === 0 || i === bars.length - 1;
        var v = isEnd ? bars[i][1] : items[i - 1].delta;
        ctx.font = '700 10px Segoe UI, system-ui, sans-serif'; ctx.textBaseline = 'bottom';
        ctx.fillStyle = isEnd ? '#f8fafc' : (v >= 0 ? '#34d399' : '#f87171');
        ctx.fillText(isEnd ? nf(v) : (v >= 0 ? '+' : '') + nf(v), e.x, top - 4);
        if (mark >= 0 && i === mark + 1) {
          var bw = e.width + 8; ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 2;
          ctx.strokeRect(e.x - bw / 2, top - 18, bw, bottom - top + 22);
          ctx.fillStyle = '#f59e0b'; ctx.fillText('the reason', e.x, top - 21);
        }
      });
      ctx.restore();
    } };
    charts[id] = new Chart(el, {
      type: 'bar',
      data: { labels: [cfg.startLabel].concat(items.map(function (x) { return x.label; }), [cfg.endLabel]),
              datasets: [{ data: bars, backgroundColor: bars.map(function (b, i) { return i === 0 ? '#3b5b8a' : i === bars.length - 1 ? '#3b82f6' : (items[i - 1].delta >= 0 ? '#10b981' : '#ef4444'); }),
                           borderRadius: 3, barPercentage: 0.75, categoryPercentage: 0.9 }] },
      options: { responsive: true, maintainAspectRatio: false, layout: { padding: { top: 30 } },
        plugins: { weekChange: false, legend: { display: false },
          tooltip: { callbacks: { label: function (c) { var i = c.dataIndex;
            if (i === 0 || i === bars.length - 1) return nf(bars[i][1]) + ' bags';
            var x = items[i - 1]; return [(x.delta >= 0 ? '+' : '') + nf(x.delta) + ' bags'].concat(x.tip || []); } } } },
        scales: { x: { grid: { display: false }, ticks: { color: '#94a3b8', maxRotation: 30, minRotation: 0, autoSkip: false, font: { size: 10 } } },
                  y: { min: yMin, grid: { color: GRID }, ticks: { color: '#64748b', callback: function (v) { return nf(v); } } } } },
      plugins: [lbl]
    });
  }

  function growthData(GT) {
    var g = GT.growth || {}, years = Object.keys(g).sort(), ly = years[years.length - 1], py = years[years.length - 2];
    var live = GT.live && String(GT.live.year) === ly ? GT.live : null, li = live ? MONTHS.indexOf(live.month) : -1;
    var val = function (y, i) { return y === ly && i === li ? (live.projected || live.soFar) : g[y][i]; };   // live month: projected
    var mom = [], yoy = [];
    for (var i = 0; i < 12; i++) {
      var v = val(ly, i), before = i ? val(ly, i - 1) : (py ? g[py][11] : null), last = py ? g[py][i] : null;
      mom.push(v != null && before ? (v - before) / before * 100 : null);
      yoy.push(v != null && last ? (v - last) / last * 100 : null);
    }
    return { g: g, years: years, ly: ly, py: py, mom: mom, yoy: yoy, live: live, li: li };
  }

  function render(el, GT, opts) {
    if (!el || !GT || !GT.growth) return;
    var G = growthData(GT), sel = String(opts.year) === G.ly ? MONTHS.indexOf(opts.month) : -1, L = G.live;
    var liveNote = L ? '<div style="text-align:center;font-size:0.8rem;color:#cbd5e1;margin:0.2rem 0 0.6rem"><b style="color:#fbbf24">' + esc(L.month) + ' so far</b> (day '
      + L.day + ' of ' + L.days + '): <b>' + nf(L.soFar) + ' bags</b>' + (L.projected ? ', on pace for <b>~' + nf(L.projected) + '</b>' : '')
      + (G.py && G.g[G.py][G.li] != null ? ' vs ' + nf(G.g[G.py][G.li]) + ' in ' + esc(L.month) + ' ' + G.py : '') + '. It joins the charts when the month closes.</div>' : '';
    // growth table — the live month shows so far + its growth on the projected total
    var tot = function (y) { return G.g[y].reduce(function (t, v) { return t + (v || 0); }, 0); };
    var gRows = MONTHS.map(function (nm, i) {
      var isLive = L && i === G.li;
      return [(i === sel ? '<b style="color:#fbbf24">▶ ' : '') + nm.slice(0, 3).toUpperCase() + (i === sel ? '</b>' : '')]
        .concat(G.years.map(function (y) {
          if (y === G.ly && isLive) return nf(L.soFar) + ' <span style="font-size:0.68rem;color:#fbbf24">so far</span>';
          return G.g[y][i] == null ? '<span style="color:#475569">—</span>' : nf(G.g[y][i]);
        }), [sg(G.mom[i], isLive ? ' <span style="font-size:0.66rem;color:#94a3b8">projected</span>' : ''), sg(G.yoy[i], isLive ? ' <span style="font-size:0.66rem;color:#94a3b8">projected</span>' : '')]);
    });
    gRows.push(['<b>TOTALS</b>'].concat(G.years.map(function (y) { return '<b>' + nf(tot(y) + (y === G.ly && L && G.g[y][G.li] == null ? L.soFar : 0)) + '</b>'; }), ['', '']));
    // tracking rows (+ the live month)
    var T = GT.tracking || { months: [] }, TL = (T.months || []).slice(), liveRow = L && L.row && String(L.year) === String(T.year) ? L.row : null;
    if (liveRow && !TL.some(function (r) { return r.month === liveRow.month; })) TL.push(liveRow);
    var ch = function (r, i, k) { return i && TL[i - 1][k] !== r[k] ? ' <span title="Changed from ' + esc(ttl(TL[i - 1][k])) + '" style="color:#fbbf24;font-size:0.7rem">●</span>' : ''; };
    var tRows = TL.map(function (r, i) {
      var on = r.month === opts.month && String(opts.year) === String(T.year), isLive = liveRow && r === liveRow, d = i && !isLive ? r.total - TL[i - 1].total : null;
      return [(on ? '<b style="color:#fbbf24">▶ ' : '') + esc(r.month) + (on ? '</b>' : '') + (isLive ? ' <span style="font-size:0.66rem;color:#fbbf24">so far</span>' : ''),
              nf(r.total) + (d != null ? ' <span style="font-size:0.7rem;color:' + (d >= 0 ? '#34d399' : '#f87171') + '">' + (d >= 0 ? '+' : '') + nf(d) + '</span>' : ''),
              esc(ttl(r.shop)) + ch(r, i, 'shop'), nf(r.shopSales), esc(ttl(r.colour)) + ch(r, i, 'colour'), esc(ttl(r.category)) + ch(r, i, 'category'),
              esc(ttl(r.bagType)) + ch(r, i, 'bagType'), nf(r.bagTypeSales), esc(ttl(r.product)) + ch(r, i, 'product')];
    });
    var btn = function (k, t) { return '<button type="button" data-g="' + k + '" style="font:inherit;font-size:0.7rem;font-weight:700;padding:0.25rem 0.7rem;border-radius:7px;cursor:pointer;border:1px solid #2d3148;background:transparent;color:#94a3b8">' + t + '</button>'; };
    el.innerHTML =
      '<div class="sec"><div class="sec-head"><div class="sec-num" style="background:#22c55e">' + (opts.num1 || '10') + '</div><h2>Growth Rate — Monthly &amp; Annual</h2></div>'
      + '<div style="font-size:0.8rem;color:#94a3b8;margin-bottom:0.4rem">Bags sold each month, ' + G.years.join(' / ') + '. <b>Monthly growth</b> = the month vs the month before; <b>annual growth</b> = the month vs the same month last year (' + G.ly + ' vs ' + G.py + ').</div>'
      + liveNote
      + '<div id="gt-mode" style="display:flex;justify-content:flex-end;gap:0.3rem;margin-bottom:0.3rem">' + btn('annual', 'Annual') + btn('monthly', 'Monthly') + '</div>'
      + '<div id="gt-growth-head" style="text-align:center;font-size:0.92rem;font-weight:800;color:#f8fafc"></div>'
      + '<div class="chart-wrap" style="height:300px"><canvas id="gt-growth"></canvas></div>'
      + table([{ h: 'Month' }].concat(G.years.map(function (y) { return { h: y, r: 1 }; }), [{ h: 'Monthly growth', r: 1 }, { h: 'Annual growth', r: 1 }]), gRows)
      + '</div>'
      + '<div class="sec"><div class="sec-head"><div class="sec-num" style="background:#0ea5e9">' + (opts.num2 || '11') + '</div><h2>Month-on-Month Tracking — ' + esc(T.year) + '</h2></div>'
      + '<div style="font-size:0.8rem;color:#94a3b8;margin-bottom:0.4rem">Each month’s total sales and its best shop, colour, category, bag type and product. <span style="color:#fbbf24">●</span> = changed from the month before.'
      + (liveRow ? ' <b style="color:#fbbf24">' + esc(liveRow.month) + '</b> is live from Odoo (tills + corporate) and fills in as the month runs.' : '') + '</div>'
      + '<div id="gt-track-head" style="text-align:center;font-size:0.92rem;font-weight:800;color:#f8fafc"></div>'
      + '<div class="chart-wrap" style="height:300px"><canvas id="gt-track"></canvas></div>'
      + table([{ h: 'Month' }, { h: 'Total sales', r: 1 }, { h: 'Best shop' }, { h: 'Shop sales', r: 1 }, { h: 'Best colour' }, { h: 'Best category' }, { h: 'Best bag type' }, { h: 'Bag type sales', r: 1 }, { h: 'Best product' }], tRows)
      + '</div>';

    function drawGrowth() {
      var mode = 'annual'; try { mode = localStorage.getItem('gt-growth-mode') || 'annual'; } catch (e) {}
      [].forEach.call(el.querySelectorAll('#gt-mode button'), function (b) { var on = b.getAttribute('data-g') === mode;
        b.style.borderColor = on ? '#6366f1' : '#2d3148'; b.style.background = on ? 'rgba(99,102,241,0.2)' : 'transparent'; b.style.color = on ? '#e2e8f0' : '#94a3b8'; });
      var ys = G.g[G.ly], done = []; for (var j = 0; j < 12; j++) if (ys[j] != null && j !== G.li) done.push(j);   // complete months only
      if (!done.length) return;
      var span = MONTHS[done[0]].slice(0, 3) + '–' + MONTHS[done[done.length - 1]].slice(0, 3);
      if (mode === 'monthly' || !G.py) {
        var startV = G.py ? G.g[G.py][11] : ys[done[0]], startL = G.py ? 'Dec ' + G.py : MONTHS[done[0]].slice(0, 3), months = G.py ? done : done.slice(1);
        var pv = startV, pl = startL;
        var steps = months.map(function (j) { var v = ys[j], st = { label: MONTHS[j].slice(0, 3), delta: v - pv, tip: [nf(pv) + ' (' + pl + ') → ' + nf(v) + (G.mom[j] != null ? ', ' + (G.mom[j] >= 0 ? '+' : '') + G.mom[j].toFixed(2) + '%' : '')] }; pv = v; pl = MONTHS[j].slice(0, 3); return st; });
        var d = pv - startV, lm = MONTHS[months[months.length - 1]];
        wf('gt-growth', 'gt-growth-head', { startLabel: startL, start: startV, items: steps, endLabel: lm.slice(0, 3) + ' ' + G.ly,
          head: 'Monthly growth, ' + startL + ' → ' + lm + ' ' + G.ly + ': <span style="color:' + (d >= 0 ? '#34d399' : '#f87171') + '">' + (d >= 0 ? '+' : '') + nf(d) + ' bags (' + (d >= 0 ? '+' : '') + (startV ? (d / startV * 100).toFixed(1) : 0) + '%)</span>' });
      } else {
        var both = done.filter(function (j) { return G.g[G.py][j] != null; });
        var items = both.map(function (j) { var a = G.g[G.py][j], b = ys[j]; return { label: MONTHS[j].slice(0, 3), delta: b - a, tip: [nf(a) + ' (' + G.py + ') → ' + nf(b) + ' (' + G.ly + '), ' + (G.yoy[j] >= 0 ? '+' : '') + G.yoy[j].toFixed(2) + '%'] }; })
          .sort(function (p, q) { return q.delta - p.delta; });
        var a0 = both.reduce(function (t, j) { return t + G.g[G.py][j]; }, 0), a1 = both.reduce(function (t, j) { return t + ys[j]; }, 0), dd = a1 - a0;
        wf('gt-growth', 'gt-growth-head', { startLabel: span + ' ' + G.py, start: a0, items: items, endLabel: span + ' ' + G.ly,
          head: 'Annual growth, ' + span + ' ' + G.py + ' → ' + G.ly + ': <span style="color:' + (dd >= 0 ? '#34d399' : '#f87171') + '">' + (dd >= 0 ? '+' : '') + nf(dd) + ' bags (' + (dd >= 0 ? '+' : '') + (a0 ? (dd / a0 * 100).toFixed(1) : 0) + '%)</span>' });
      }
    }
    el.querySelector('#gt-mode').addEventListener('click', function (ev) { var b = ev.target.closest('button'); if (!b) return;
      try { localStorage.setItem('gt-growth-mode', b.getAttribute('data-g')); } catch (e) {} drawGrowth(); });
    drawGrowth();
    // tracking waterfall: complete months only
    var TC = TL.filter(function (r) { return r !== liveRow; });
    if (TC.length >= 2) {
      var steps = TC.slice(1).map(function (r, i) { var p = TC[i]; return { label: r.month.slice(0, 3), delta: r.total - p.total,
        tip: [nf(p.total) + ' (' + p.month.slice(0, 3) + ') → ' + nf(r.total), 'Best shop: ' + r.shop + ' (' + nf(r.shopSales) + ')', 'Best bag type: ' + r.bagType + ' (' + nf(r.bagTypeSales) + ')', 'Best product: ' + r.product] }; });
      var f = TC[0], l = TC[TC.length - 1], dt = l.total - f.total;
      wf('gt-track', 'gt-track-head', { startLabel: f.month.slice(0, 3), start: f.total, items: steps, endLabel: l.month.slice(0, 3) + ' total',
        head: f.month + ' → ' + l.month + ' ' + T.year + ': <span style="color:' + (dt >= 0 ? '#34d399' : '#f87171') + '">' + (dt >= 0 ? '+' : '') + nf(dt) + ' bags (' + (dt >= 0 ? '+' : '') + (f.total ? (dt / f.total * 100).toFixed(1) : 0) + '%)</span>',
        extra: liveRow ? esc(liveRow.month) + ' so far: ' + nf(liveRow.total) + ' bags, best shop ' + esc(ttl(liveRow.shop)) + ', best bag ' + esc(ttl(liveRow.bagType)) : '' });
    }
  }
  window.GrowthTracking = { render: render };
})();
