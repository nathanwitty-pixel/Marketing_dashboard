/* chart_switcher.js — a chart-type menu on every Chart.js chart (spec: docs/chart-switcher.md).
   Load right after Chart.js, before the page creates its charts. It wraps the Chart class to keep
   each chart's original config, then redraws the SAME chart object in place when a type is
   picked, so the page's own references / destroy() / re-renders keep working. */
(function () {
  'use strict';
  var Base = window.Chart;
  if (!Base || Base.__chartSwitch) return;

  var TREEMAP_SRC = 'https://cdn.jsdelivr.net/npm/chartjs-chart-treemap@3/dist/chartjs-chart-treemap.min.js';
  var PALETTE = ['#06b6d4', '#f59e0b', '#8b5cf6', '#10b981', '#ec4899', '#3b82f6', '#ef4444', '#84cc16',
                 '#f97316', '#14b8a6', '#a78bfa', '#94a3b8'];
  var UP = '#10b981', DOWN = '#ef4444', TOTAL = '#3b82f6';

  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} }
  };

  // Deep clone of plain objects/arrays; functions, gradients etc. are kept by reference.
  function clone(v) {
    if (Array.isArray(v)) return v.map(clone);
    if (v && typeof v === 'object' && Object.getPrototypeOf(v) === Object.prototype) {
      var o = {};
      for (var k in v) if (Object.prototype.hasOwnProperty.call(v, k)) o[k] = clone(v[k]);
      return o;
    }
    return v;
  }
  var num = function (v) { var n = Number(v); return isFinite(n) ? n : 0; };
  var first = function (c) { return Array.isArray(c) ? c[0] : c; };
  function alpha(col, a) {
    if (typeof col !== 'string') return col;
    var m = col.match(/^#([0-9a-f]{6})$/i);
    if (m) { var n = parseInt(m[1], 16); return 'rgba(' + (n >> 16) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',' + a + ')'; }
    return col;
  }
  function seriesColor(ds, i) {
    return first(ds.backgroundColor) || first(ds.borderColor) || PALETTE[i % PALETTE.length];
  }

  // ── What the data looks like ──
  function shape(orig) {
    var ds = (orig.data && orig.data.datasets) || [];
    var labels = (orig.data && orig.data.labels) || [];
    var points = ds.some(function (d) { return (d.data || []).some(function (v) { return v && typeof v === 'object'; }); });
    var vals = ds.map(function (d) { return (d.data || []).map(num); });
    var neg = vals.some(function (a) { return a.some(function (v) { return v < 0; }); });
    return { ds: ds, labels: labels, points: points, n: ds.length, nl: labels.length, neg: neg, vals: vals };
  }

  // Slices for pie-like views: 1 series → label × value; 2+ → one slice per series total.
  function slices(s) {
    if (s.n === 1) {
      var bg = s.ds[0].backgroundColor;
      return s.labels.map(function (l, i) {
        return { label: Array.isArray(l) ? l.join(' ') : String(l), v: s.vals[0][i] || 0,
                 c: (Array.isArray(bg) && bg[i]) || PALETTE[i % PALETTE.length] };
      });
    }
    return s.ds.map(function (d, i) {
      return { label: d.label || ('Series ' + (i + 1)), v: s.vals[i].reduce(function (a, b) { return a + b; }, 0),
               c: seriesColor(d, i) };
    });
  }

  var TYPES = [
    { key: 'column',  label: 'Column',         ok: function () { return true; } },
    { key: 'bar',     label: 'Bar',            ok: function () { return true; } },
    { key: 'stacked', label: 'Stacked column', ok: function (s) { return s.n >= 2; } },
    { key: 'line',    label: 'Line',           ok: function () { return true; } },
    { key: 'area',    label: 'Area',           ok: function () { return true; } },
    { key: 'sarea',   label: 'Stacked area',   ok: function (s) { return s.n >= 2; } },
    { key: 'combo',   label: 'Combo',          ok: function (s) { return s.n >= 2; } },
    { key: 'pie',     label: 'Pie',            ok: function (s) { return !s.neg; } },
    { key: 'doughnut',label: 'Doughnut',       ok: function (s) { return !s.neg; } },
    { key: 'polar',   label: 'Polar area',     ok: function (s) { return !s.neg; } },
    { key: 'radar',   label: 'Radar',          ok: function (s) { return s.nl >= 3; } },
    { key: 'funnel',  label: 'Funnel',         ok: function (s) { return !s.neg && slices(s).length >= 2; } },
    { key: 'waterfall', label: 'Waterfall',    ok: function (s) { return s.nl >= 2; } },
    { key: 'treemap', label: 'Treemap',        ok: function (s) { return !s.neg; } }
  ];

  // Value formatter: the chart's own value-axis tick format when it has one.
  function valueFmt(orig) {
    var sc = (orig.options && orig.options.scales) || {};
    var horiz = orig.options && orig.options.indexAxis === 'y';
    var ax = (horiz ? sc.x : sc.y) || sc.y || sc.x || {};
    var cb = ax.ticks && ax.ticks.callback;
    return function (v) {
      if (cb) { try { var r = cb.call({ getLabelForValue: function (x) { return x; } }, v, 0, []); if (r != null && r !== '') return r; } catch (e) {} }
      return Math.round(v).toLocaleString('en-US');
    };
  }
  function genericTooltip(opts, fmtOf) {
    opts.plugins = opts.plugins || {};
    opts.plugins.tooltip = Object.assign({}, opts.plugins.tooltip || {});
    opts.plugins.tooltip.callbacks = { label: function (c) { return ' ' + (c.dataset.label ? c.dataset.label + ': ' : '') + fmtOf(c); } };
  }
  function dropScales(opts) { delete opts.scales; delete opts.indexAxis; }
  function axisOpts(opts) {
    opts.scales = opts.scales || {};
    opts.scales.x = opts.scales.x || {};
    opts.scales.y = opts.scales.y || {};
    return opts.scales;
  }

  // ── Build a config of the chosen type from the ORIGINAL config ──
  function build(key, orig) {
    var o = clone(orig), s = shape(orig), fmt = valueFmt(orig);
    var data = o.data, opts = o.options || (o.options = {});
    var wasHoriz = opts.indexAxis === 'y';
    var cartesian = !orig.type || ['bar', 'line'].indexOf(orig.type) >= 0;
    if (!cartesian) delete opts.scales;               // pie/doughnut/polar/radar → fresh axes
    delete opts.cutout; delete opts.circumference; delete opts.rotation;
    if (wasHoriz && key !== 'bar' && key !== 'funnel') {  // back to vertical: swap the axes back
      var sc0 = opts.scales || {}; opts.scales = Object.assign({}, sc0, { x: sc0.y || {}, y: sc0.x || {} }); delete opts.indexAxis;
    }
    var plain = function (ds, i, t) {                   // one series as a plain bar/line
      delete ds.type; delete ds.stack; delete ds.fill; delete ds.yAxisID; delete ds.xAxisID;
      var col = seriesColor(orig.data.datasets[i], i);
      if (t === 'line') {
        ds.borderColor = first(ds.borderColor) || col;
        ds.backgroundColor = alpha(col, 0.25);
        ds.pointRadius = ds.pointRadius == null ? 3 : ds.pointRadius;
        ds.tension = ds.tension == null ? 0.3 : ds.tension;
        ds.borderWidth = 2;
      } else if (orig.type === 'line' || ds.backgroundColor == null) {
        ds.backgroundColor = alpha(col, 0.85);
      }
      return ds;
    };
    var sc;
    switch (key) {
      case 'column': case 'stacked': case 'bar':
        data.datasets.forEach(function (d, i) { plain(d, i, 'bar'); d.borderRadius = d.borderRadius == null ? 4 : d.borderRadius; });
        sc = axisOpts(opts);
        sc.x.stacked = sc.y.stacked = key === 'stacked';
        if (key === 'bar') {
          if (!wasHoriz) { var t = sc.x; sc.x = sc.y; sc.y = t; }
          opts.indexAxis = 'y';
          sc.x.stacked = sc.y.stacked = false;
        }
        if (key === 'bar') genericTooltip(opts, function (c) { return fmt(c.parsed.x); });
        return { type: 'bar', data: data, options: opts };
      case 'line': case 'area': case 'sarea':
        data.datasets.forEach(function (d, i) {
          plain(d, i, 'line');
          d.fill = key === 'line' ? false : (key === 'sarea' && i > 0 ? '-1' : 'origin');
        });
        sc = axisOpts(opts);
        sc.x.stacked = false; sc.y.stacked = key === 'sarea';
        return { type: 'line', data: data, options: opts };
      case 'combo':
        data.datasets.forEach(function (d, i) {
          plain(d, i, i === 0 ? 'bar' : 'line');
          d.type = i === 0 ? 'bar' : 'line';
          d.order = i === 0 ? 2 : 1;
          if (i > 0) d.fill = false;
        });
        sc = axisOpts(opts); sc.x.stacked = sc.y.stacked = false;
        return { type: 'bar', data: data, options: opts };
      case 'pie': case 'doughnut': case 'polar':
        var sl = slices(s);
        dropScales(opts);
        opts.plugins = opts.plugins || {};
        opts.plugins.legend = Object.assign({ display: true, position: 'right' }, opts.plugins.legend || {}, { display: true });
        genericTooltip(opts, function (c) {
          var tot = sl.reduce(function (a, x) { return a + x.v; }, 0) || 1;
          return fmt(c.raw) + ' (' + Math.round(c.raw / tot * 100) + '%)';
        });
        if (key === 'polar') opts.scales = { r: { grid: { color: 'rgba(148,163,184,0.2)' }, ticks: { display: false } } };
        if (key === 'doughnut') opts.cutout = '58%';
        return { type: key === 'polar' ? 'polarArea' : key,
                 data: { labels: sl.map(function (x) { return x.label; }),
                         datasets: [{ data: sl.map(function (x) { return x.v; }),
                                      backgroundColor: sl.map(function (x) { return key === 'polar' ? alpha(x.c, 0.7) : x.c; }),
                                      borderColor: 'rgba(15,17,23,0.9)', borderWidth: 2 }] },
                 options: opts };
      case 'radar':
        data.datasets.forEach(function (d, i) {
          plain(d, i, 'line'); d.fill = true; d.backgroundColor = alpha(seriesColor(orig.data.datasets[i], i), 0.2);
        });
        dropScales(opts);
        opts.scales = { r: { grid: { color: 'rgba(148,163,184,0.2)' }, angleLines: { color: 'rgba(148,163,184,0.2)' },
                             ticks: { display: false }, pointLabels: { font: { size: 11 } } } };
        genericTooltip(opts, function (c) { return fmt(c.raw); });
        return { type: 'radar', data: data, options: opts };
      case 'funnel':
        var fs = slices(s).slice().sort(function (a, b) { return b.v - a.v; });
        dropScales(opts);
        opts.indexAxis = 'y';
        opts.scales = { x: { display: false, stacked: false }, y: { grid: { display: false } } };
        opts.plugins = opts.plugins || {}; opts.plugins.legend = { display: false };
        genericTooltip(opts, function (c) { return fmt(fs[c.dataIndex].v); });
        return { type: 'bar',
                 data: { labels: fs.map(function (x) { return x.label; }),
                         datasets: [{ label: '', data: fs.map(function (x) { return [-x.v / 2, x.v / 2]; }),
                                      backgroundColor: fs.map(function (x) { return x.c; }),
                                      borderRadius: 4, barPercentage: 0.95, categoryPercentage: 1 }] },
                 options: opts };
      case 'waterfall':
        var tot = s.labels.map(function (_, j) { return s.vals.reduce(function (a, v) { return a + (v[j] || 0); }, 0); });
        var run = 0, bars = [], cols = [], steps = [];
        tot.forEach(function (v) { bars.push([run, run + v]); cols.push(v >= 0 ? UP : DOWN); steps.push(v); run += v; });
        bars.push([0, run]); cols.push(TOTAL); steps.push(run);
        sc = axisOpts(opts); sc.x.stacked = sc.y.stacked = false;
        opts.plugins = opts.plugins || {}; opts.plugins.legend = { display: false };
        genericTooltip(opts, function (c) { return (c.dataIndex === steps.length - 1 ? 'Total ' : '') + fmt(steps[c.dataIndex]); });
        return { type: 'bar',
                 data: { labels: s.labels.concat(['Total']),
                         datasets: [{ label: '', data: bars, backgroundColor: cols, borderRadius: 3 }] },
                 options: opts };
      case 'treemap':
        var ts = slices(s).filter(function (x) { return x.v > 0; });
        dropScales(opts);
        opts.plugins = opts.plugins || {}; opts.plugins.legend = { display: false };
        genericTooltip(opts, function (c) { return fmt(c.raw && c.raw.v); });
        opts.plugins.tooltip.callbacks.title = function (items) { var r = items[0] && items[0].raw; return r && r._data ? r._data.label : ''; };
        return { type: 'treemap',
                 data: { datasets: [{ tree: ts.map(function (x) { return { label: x.label, v: x.v, c: x.c }; }), key: 'v',
                                      borderWidth: 1, borderColor: 'rgba(15,17,23,0.9)', spacing: 1,
                                      backgroundColor: function (ctx) { return ctx.type === 'data' && ctx.raw && ctx.raw._data ? ctx.raw._data.c : 'transparent'; },
                                      labels: { display: true, color: '#fff', font: { size: 11, weight: '600' },
                                                formatter: function (ctx) { var d = ctx.raw && ctx.raw._data; return d ? [d.label, fmt(d.v)] : ''; } } }] },
                 options: opts };
    }
    return null;
  }

  // ── Treemap plugin, loaded on first use ──
  var treemapReady = null;
  function needTreemap() {
    if (Base.registry && (function () { try { return Base.registry.getController('treemap'); } catch (e) { return null; } })()) return Promise.resolve();
    if (!treemapReady) treemapReady = new Promise(function (res, rej) {
      var sEl = document.createElement('script');
      sEl.src = TREEMAP_SRC; sEl.onload = res; sEl.onerror = function () { treemapReady = null; rej(); };
      document.head.appendChild(sEl);
    });
    return treemapReady;
  }

  // The original's shape — a remembered type is only re-applied when the page redraws the SAME
  // kind of chart (e.g. a period change), not after the page's own type toggle changed it.
  function sig(orig) {
    var o = orig.options || {}, d0 = ((orig.data && orig.data.datasets) || [])[0] || {};
    return [orig.type || 'bar', o.indexAxis || 'x', d0.fill ? 'fill' : '', d0.type || ''].join('/');
  }

  // ── Apply / restore ──
  // The page's own inline plugins (value labels, centre text…) assume its original data shape,
  // so they only run on views with the same shape: the original and the vertical cartesian ones.
  var SAME_SHAPE = ['column', 'stacked', 'line', 'area', 'sarea', 'combo'];
  function setConfig(chart, cfg, key) {
    var raw = chart.config._config, orig = chart.$csOrig;
    var keep = key === 'original' || (SAME_SHAPE.indexOf(key) >= 0 && (!orig.type || orig.type === 'bar' || orig.type === 'line'));
    if (chart.$csPlugins === undefined) chart.$csPlugins = raw.plugins || [];
    raw.plugins = keep ? chart.$csPlugins : [];
    chart.config.type = cfg.type;
    chart.config.data = cfg.data;
    chart.config.options = cfg.options;
    chart.update();
  }
  function apply(chart, key, remember) {
    var orig = chart.$csOrig;
    if (!orig) return;
    if (remember) store.set(chart.$csKey, key === 'original' ? null : key + '|' + sig(orig));
    if (key === 'original') { chart.$csType = 'original'; setConfig(chart, clone(orig), 'original'); return; }
    var go = function () {
      if (!chart.canvas) return;                       // destroyed meanwhile
      var cfg = build(key, orig);
      if (!cfg) return;
      chart.$csType = key;
      try { setConfig(chart, cfg, key); } catch (e) {
        if (window.console) console.warn('chart_switcher: ' + key + ' failed, restoring original', e);
        chart.$csType = 'original'; setConfig(chart, clone(orig), 'original');
      }
    };
    if (key === 'treemap') needTreemap().then(go, function () { if (window.console) console.warn('chart_switcher: treemap plugin could not load'); });
    else go();
  }

  function eligible(chart) {
    var cv = chart.canvas, o = chart.$csOrig;
    if (!cv || !o) return false;
    if (cv.getAttribute('data-chart-switch') === 'off') return false;
    if (o.options && o.options.plugins && o.options.plugins.chartSwitch === false) return false;
    if (['bar', 'line', 'pie', 'doughnut', 'polarArea', 'radar'].indexOf(o.type || 'bar') < 0) return false;
    if (shape(o).points) return false;
    var w = cv.clientWidth || cv.width, h = cv.clientHeight || cv.height;
    return w >= 200 && h >= 120;
  }

  // ── UI ──
  var ICON = {
    btn: '<path d="M3 13h2v4H3zM8 9h2v8H8zM13 5h2v12h-2z"/><path d="M17 7l2 2 2-2" fill="none" stroke="currentColor" stroke-width="1.6"/>',
    original: '<path d="M4 10a6 6 0 1 0 2-4.5M4 3v3h3" fill="none" stroke="currentColor" stroke-width="1.8"/>',
    column: '<path d="M3 11h3v6H3zM8.5 6h3v11h-3zM14 9h3v8h-3z"/>',
    bar: '<path d="M3 3h9v3H3zM3 8.5h13v3H3zM3 14h7v3H3z"/>',
    stacked: '<path d="M3 11h3v6H3zM8.5 6h3v11h-3zM14 9h3v8h-3z" opacity=".45"/><path d="M3 14h3v3H3zM8.5 11h3v6h-3zM14 13h3v4h-3z"/>',
    line: '<path d="M2 15l5-6 4 3 7-8" fill="none" stroke="currentColor" stroke-width="2"/>',
    area: '<path d="M2 17V13l5-5 4 3 7-7v13z" opacity=".8"/>',
    sarea: '<path d="M2 17v-6l5-4 4 2 7-5v13z" opacity=".4"/><path d="M2 17v-3l5-2 4 1 7-3v7z"/>',
    combo: '<path d="M3 11h3v6H3zM8.5 8h3v9h-3zM14 12h3v5h-3z" opacity=".6"/><path d="M2 8l6-4 5 3 6-4" fill="none" stroke="currentColor" stroke-width="1.8"/>',
    pie: '<path d="M10 2a8 8 0 1 0 8 8h-8z"/><path d="M12 0.5v7.5h7.5A7.5 7.5 0 0 0 12 .5z" opacity=".6"/>',
    doughnut: '<path d="M10 2a8 8 0 1 1-8 8h3.5a4.5 4.5 0 1 0 4.5-4.5z"/><path d="M9 2.1A8 8 0 0 0 2.1 9h3.5A4.5 4.5 0 0 1 9 5.6z" opacity=".55"/>',
    polar: '<path d="M10 10V1a9 9 0 0 1 8 5z"/><path d="M10 10l7 1a7 7 0 0 1-5 6z" opacity=".75"/><path d="M10 10l1 5a5 5 0 0 1-6-3z" opacity=".5"/><path d="M10 10L4 8a6 6 0 0 1 6-5z" opacity=".35"/>',
    radar: '<path d="M10 2l7.5 5.5-2.9 9H5.4l-2.9-9z" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M10 5l5 4-2 5H7.5L6 9.5z" opacity=".7"/>',
    funnel: '<path d="M2 3h16v3H2zM4.5 8.5h11v3h-11zM7 14h6v3H7z"/>',
    waterfall: '<path d="M2 12h3v5H2zM6 8h3v4H6zM10 5h3v3h-3z"/><path d="M14 5h3v12h-3z" opacity=".6"/>',
    treemap: '<path d="M2 2h9v10H2zM12 2h6v5h-6zM12 8h6v4h-6zM2 13h6v5H2zM9 13h9v5H9z"/>'
  };
  var svg = function (k) { return '<svg viewBox="0 0 20 20" width="15" height="15" fill="currentColor" aria-hidden="true">' + ICON[k] + '</svg>'; };

  var css = document.createElement('style');
  css.textContent =
    '.chartsw-btn{position:absolute;z-index:5;width:26px;height:24px;display:flex;align-items:center;justify-content:center;' +
    'background:rgba(30,33,48,.85);border:1px solid #2d3148;border-radius:6px;color:#94a3b8;cursor:pointer;opacity:.6;padding:0;' +
    'transition:opacity .15s,color .15s,border-color .15s}' +
    '.chartsw-btn:hover,.chartsw-btn:focus-visible,.chartsw-btn[aria-expanded="true"]{opacity:1;color:#e2e8f0;border-color:#6366f1;outline:none}' +
    '.chartsw-btn.chartsw-on{color:#a5b4fc;opacity:.95}' +
    '@media (hover:none){.chartsw-btn{opacity:.9}}' +
    '.chartsw-menu{position:fixed;z-index:9999;min-width:190px;max-height:70vh;overflow-y:auto;background:#1a1d2b;border:1px solid #2d3148;' +
    'border-radius:10px;padding:.35rem;box-shadow:0 12px 32px rgba(0,0,0,.45);font:13px "Segoe UI",system-ui,sans-serif}' +
    '.chartsw-menu .chartsw-h{font-size:10px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#64748b;padding:.35rem .55rem .25rem}' +
    '.chartsw-menu button{display:flex;width:100%;align-items:center;gap:.55rem;background:none;border:0;color:#cbd5e1;padding:.38rem .55rem;' +
    'border-radius:6px;cursor:pointer;text-align:left;font:inherit}' +
    '.chartsw-menu button:hover,.chartsw-menu button:focus-visible{background:#252840;color:#f8fafc;outline:none}' +
    '.chartsw-menu button.chartsw-cur{background:rgba(99,102,241,.18);color:#c7d2fe}' +
    '.chartsw-menu button svg{flex:0 0 auto;color:#22d3ee}' +
    '.chartsw-menu .chartsw-sep{height:1px;background:#2d3148;margin:.3rem .2rem}';
  (document.head || document.documentElement).appendChild(css);

  var openMenu = null;
  function closeMenu(focusBtn) {
    if (!openMenu) return;
    var m = openMenu; openMenu = null;
    m.btn.setAttribute('aria-expanded', 'false');
    m.el.remove();
    document.removeEventListener('mousedown', m.outside, true);
    window.removeEventListener('scroll', m.close, true);
    window.removeEventListener('resize', m.close);
    if (focusBtn) m.btn.focus({ preventScroll: true });
  }
  function showMenu(chart) {
    var btn = chart.$csBtn;
    if (openMenu && openMenu.btn === btn) { closeMenu(true); return; }
    closeMenu();
    var s = shape(chart.$csOrig), cur = chart.$csType || 'original';
    var el = document.createElement('div');
    el.className = 'chartsw-menu'; el.setAttribute('role', 'menu'); el.setAttribute('aria-label', 'Chart type');
    var items = [{ key: 'original', label: 'Original' }].concat(TYPES.filter(function (t) { return t.ok(s); }));
    el.innerHTML = '<div class="chartsw-h">Chart type</div>' + items.map(function (t, i) {
      return (i === 1 ? '<div class="chartsw-sep"></div>' : '') +
        '<button type="button" role="menuitemradio" aria-checked="' + (t.key === cur) + '" data-k="' + t.key + '" class="' +
        (t.key === cur ? 'chartsw-cur' : '') + '">' + svg(t.key) + '<span>' + t.label + '</span></button>';
    }).join('');
    document.body.appendChild(el);
    var r = btn.getBoundingClientRect(), mw = el.offsetWidth, mh = el.offsetHeight;
    var left = Math.max(8, Math.min(r.right - mw, window.innerWidth - mw - 8));
    var top = r.bottom + 6 + mh > window.innerHeight - 8 ? Math.max(8, r.top - mh - 6) : r.bottom + 6;
    el.style.left = left + 'px'; el.style.top = top + 'px';
    var m = {
      el: el, btn: btn,
      outside: function (e) { if (!el.contains(e.target) && e.target !== btn && !btn.contains(e.target)) closeMenu(); },
      close: function (e) { if (!(e && e.target && e.target.nodeType === 1 && el.contains(e.target))) closeMenu(); }
    };
    openMenu = m;
    btn.setAttribute('aria-expanded', 'true');
    document.addEventListener('mousedown', m.outside, true);
    window.addEventListener('scroll', m.close, true);
    window.addEventListener('resize', m.close);
    el.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-k]'); if (!b) return;
      closeMenu(true);
      apply(chart, b.getAttribute('data-k'), true);
      mark(chart);
    });
    el.addEventListener('keydown', function (e) {
      var bs = Array.prototype.slice.call(el.querySelectorAll('button')), i = bs.indexOf(document.activeElement);
      if (e.key === 'Escape') { e.preventDefault(); closeMenu(true); }
      else if (e.key === 'ArrowDown') { e.preventDefault(); bs[(i + 1) % bs.length].focus({ preventScroll: true }); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); bs[(i - 1 + bs.length) % bs.length].focus({ preventScroll: true }); }
      else if (e.key === 'Tab') closeMenu();
    });
    (el.querySelector('.chartsw-cur') || el.querySelector('button')).focus({ preventScroll: true });
  }
  function mark(chart) {
    if (!chart.$csBtn) return;
    var on = chart.$csType && chart.$csType !== 'original';
    chart.$csBtn.classList.toggle('chartsw-on', !!on);
    var t = TYPES.filter(function (x) { return x.key === chart.$csType; })[0];
    chart.$csBtn.title = 'Chart type' + (t ? ': ' + t.label : '');
  }
  function place(chart) {
    var b = chart.$csBtn, cv = chart.canvas;
    if (!b || !cv || !cv.parentNode) return;
    // A hidden chart (e.g. the other half of a Bars ⇄ Trend toggle) hides its button too.
    var shown = cv.offsetWidth > 0 && cv.offsetHeight > 0 && getComputedStyle(cv).display !== 'none';
    b.style.display = shown ? '' : 'none';
    if (!shown) return;
    b.style.top = (cv.offsetTop + 4) + 'px';
    b.style.left = Math.max(0, cv.offsetLeft + cv.offsetWidth - GUTTER + 4) + 'px';
  }
  function attach(chart) {
    if (chart.$csBtn || !eligible(chart)) return;
    var cv = chart.canvas, parent = cv.parentNode;
    if (getComputedStyle(parent).position === 'static') parent.style.position = 'relative';
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'chartsw-btn';
    b.setAttribute('aria-haspopup', 'menu'); b.setAttribute('aria-expanded', 'false');
    b.setAttribute('aria-label', 'Change chart type');
    if (cv.id) b.setAttribute('data-chart', cv.id);
    b.innerHTML = svg('btn');
    b.addEventListener('click', function (e) { e.stopPropagation(); showMenu(chart); });
    parent.appendChild(b);
    chart.$csBtn = b;
    if (window.ResizeObserver) {                      // follows the canvas being shown / hidden / resized
      chart.$csRO = new ResizeObserver(function () { place(chart); });
      chart.$csRO.observe(cv);
    }
    place(chart); mark(chart);
    chart.update('none');                             // re-lay out with the button's gutter
  }

  // An empty strip down the right edge of every chart with a button, so the button never covers
  // bars, lines, labels, the legend or the title. Added on top of the chart's own padding.
  var GUTTER = 34;
  function padOf(p) {
    if (typeof p === 'number') return { top: p, right: p, bottom: p, left: p };
    p = p || {};
    return { top: num(p.top != null ? p.top : p.y), right: num(p.right != null ? p.right : p.x),
             bottom: num(p.bottom != null ? p.bottom : p.y), left: num(p.left != null ? p.left : p.x) };
  }

  Base.register({
    id: 'chartSwitchUi',
    beforeLayout: function (chart) {
      if (!chart.$csBtn || !chart.options.layout) return;
      var base = padOf(((chart.config.options || {}).layout || {}).padding);
      base.right += GUTTER;
      chart.options.layout.padding = base;
    },
    afterInit: function (chart) { setTimeout(function () { attach(chart); }, 0); },
    resize: function (chart) { setTimeout(function () { if (chart.$csBtn) place(chart); else if (chart.$csOrig) attach(chart); }, 0); },
    afterDestroy: function (chart) {
      if (openMenu && openMenu.btn === chart.$csBtn) closeMenu();
      if (chart.$csRO) { chart.$csRO.disconnect(); chart.$csRO = null; }
      if (chart.$csBtn) { chart.$csBtn.remove(); chart.$csBtn = null; }
    }
  });

  // ── Wrap the Chart class: keep the pristine config, re-apply a remembered type ──
  var seq = 0;
  function Chart(item, config) {
    var orig = config ? clone({ type: config.type, data: config.data, options: config.options || {} }) : null;
    var chart = Reflect.construct(Base, [item, config], new.target || Chart);
    chart.$csOrig = orig;
    var cv = chart.canvas;
    if (cv) {
      var page = (location.pathname.split('/').pop() || 'page');
      chart.$csKey = 'cs:' + decodeURIComponent(page) + ':' + (cv.id || ('#' + (cv.$csIdx = cv.$csIdx || ++seq)));
      var parts = (store.get(chart.$csKey) || '').split('|'), saved = parts[0];
      if (saved && orig) {
        var t = TYPES.filter(function (x) { return x.key === saved; })[0];
        if (!t || parts.slice(1).join('|') !== sig(orig)) store.set(chart.$csKey, null);   // page changed the chart itself
        else if (eligible(chart) && t.ok(shape(orig))) setTimeout(function () { apply(chart, saved, false); mark(chart); }, 0);
      }
    }
    return chart;
  }
  Object.setPrototypeOf(Chart, Base);
  Chart.prototype = Base.prototype;
  Chart.__chartSwitch = true;
  window.Chart = Chart;
})();
