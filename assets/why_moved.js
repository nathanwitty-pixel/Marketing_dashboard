/* "Why did we move?" waterfall — shared by Current Performance (every bag) and New Products
   (new-product bags only). The data is lib/why_moved.py's build(): {weeks, mom}.
   Bars: last period's bags → selling-days effect → one bar per region → this period.
   The bars add up exactly (the generator puts rounding leftovers on the biggest mover).
   The page carries the markup (#wm-grid, #wm-mode, #wm-period, #wm-weeks, #wm-a, #wm-b, #wm-best,
   #wm-best-note, #wm-head, #wm-sub, #chart-why-moved, #wm-reason) and calls
     WhyMoved.init(data, { C: colours, tt: tooltip defaults, store: 'localStorage key prefix' }). */
window.WhyMoved = {
  init: function (WM, opts) {
    var C = opts.C, ttDefaults = opts.tt, STORE = opts.store || 'wm';
    var cv = document.getElementById('chart-why-moved');
    var WEEKS = (WM && WM.weeks) || [];
    if (!cv || !WM || (WEEKS.length < 2 && !WM.mom)) return;
    document.getElementById('wm-grid').style.display = '';
    var chart = null;
    var fmt = function (n) { return Math.abs(n).toLocaleString(); };
    var sgn = function (n) { return (n > 0 ? '+' : n < 0 ? '−' : '') + fmt(n); };
    var TOTAL_THEN = 'rgba(96,165,250,0.55)', TOTAL_NOW = '#3b82f6', DAYS = '#f59e0b';

    var MODE_WORD = { with: 'With bulk orders', without: 'Without bulk orders' };

    // Week on week: the generator sends every week's till rows [region, shop, bags, bulk];
    // view() and waterfall() are _view() / _waterfall() in forward_projections.py, so any two weeks compare.
    var selA = WEEKS.length - 2, selB = WEEKS.length - 1;
    function view(wk, mode) {
      var regs = {}, total = 0;
      wk.rows.forEach(function (r) {
        var v = mode === 'with' ? r[2] : r[2] - r[3];
        var o = regs[r[0]] || (regs[r[0]] = { bags: 0, bulk: 0, shops: {} });
        o.bags += v;
        if (mode !== 'without') o.bulk += r[3];
        if (r[1]) o.shops[r[1]] = (o.shops[r[1]] || 0) + v;
      });
      Object.keys(regs).forEach(function (k) {
        if (!Math.round(regs[k].bags) && !Object.keys(regs[k].shops).length) delete regs[k];
        else total += regs[k].bags;
      });
      return { label: wk.label, range: wk.range, days: wk.days, total: total, regions: regs };
    }
    function waterfall(a, b) {
      var scale = a.days ? b.days / a.days : 1;
      var daysEff = Math.round(a.total * scale) - Math.round(a.total);
      var names = Object.keys(a.regions).concat(Object.keys(b.regions))
        .filter(function (n, i, all) { return all.indexOf(n) === i; }).sort();
      var get = function (p, n) { return p.regions[n] || { bags: 0, bulk: 0, shops: {} }; };
      var raw = {}, bars = {}, sum = 0;
      names.forEach(function (n) {
        raw[n] = get(b, n).bags - get(a, n).bags * scale;
        bars[n] = Math.round(raw[n]); sum += bars[n];
      });
      // Rounding leftovers go on the biggest mover so the bars land exactly on b.
      var left = Math.round(b.total) - Math.round(a.total) - daysEff - sum;
      if (left && names.length) {
        var big = names.reduce(function (m, n) { return Math.abs(raw[n]) > Math.abs(raw[m]) ? n : m; });
        bars[big] += left;
      }
      var end = function (p) { return { label: p.label, range: p.range, days: p.days, bags: Math.round(p.total) }; };
      return {
        then: end(a), now: end(b), daysEffect: daysEff,
        regions: names.map(function (n) {
          var ra = get(a, n), rb = get(b, n);
          var shops = Object.keys(ra.shops).concat(Object.keys(rb.shops))
            .filter(function (s, i, all) { return all.indexOf(s) === i; }).sort();
          return {
            region: n, delta: bars[n], then: Math.round(ra.bags), now: Math.round(rb.bags),
            bulkThen: Math.round(ra.bulk), bulkNow: Math.round(rb.bulk),
            shops: shops.map(function (s) {
              var st = ra.shops[s] || 0, sn = rb.shops[s] || 0;
              return { shop: s, then: Math.round(st), now: Math.round(sn), delta: Math.round(sn - st * scale) };
            })
          };
        })
      };
    }
    function hasKey(key) { return key === 'wow' ? WEEKS.length >= 2 : !!WM[key]; }
    function getW(key, mode) {
      if (key === 'wow') return WEEKS.length >= 2 ? waterfall(view(WEEKS[selA], mode), view(WEEKS[selB], mode)) : null;
      return WM[key] && WM[key][mode];
    }
    // Best week = the most bags among LAST MONTH's full 7-day weeks (a week cut at a month end can't
    // win on size). The list starts on the 1st of last month, so WEEKS[0] names that month.
    var LAST_MONTH = WEEKS.length ? WEEKS[0].start.slice(0, 7) : '';
    var MONTH_NAME = LAST_MONTH ? new Date(LAST_MONTH + '-01T00:00:00').toLocaleString('en-GB', { month: 'long' }) : '';
    // This month's best week is marked too (cyan), from the weeks after last month's.
    var THIS_MONTH = (WEEKS.filter(function (wk) { return wk.start.slice(0, 7) > LAST_MONTH; })[0] || {}).start;
    THIS_MONTH = THIS_MONTH ? THIS_MONTH.slice(0, 7) : '';
    var THIS_MONTH_NAME = THIS_MONTH ? new Date(THIS_MONTH + '-01T00:00:00').toLocaleString('en-GB', { month: 'long' }) : '';
    var BEST_COL = { last: '#fbbf24', 'this': '#22d3ee' };
    function shortMonth(name) { return name.slice(0, 3); }
    function bestWeek(mode, month) {
      month = month || LAST_MONTH;
      var best = -1, bags = -Infinity;
      WEEKS.forEach(function (wk, i) {
        var t = Math.round(view(wk, mode).total);
        if (wk.days === 7 && !wk.current && wk.start.slice(0, 7) === month && t > bags) { best = i; bags = t; }
      });
      return best < 0 ? null : { i: best, wk: WEEKS[best], bags: bags };
    }
    // Both reference weeks: [{best, name, col}] — last month's first, then this month's.
    function bestWeeks(mode) {
      var out = [];
      var a = bestWeek(mode, LAST_MONTH), b = THIS_MONTH ? bestWeek(mode, THIS_MONTH) : null;
      if (a) out.push({ i: a.i, wk: a.wk, bags: a.bags, name: MONTH_NAME, col: BEST_COL.last });
      if (b) out.push({ i: b.i, wk: b.wk, bags: b.bags, name: THIS_MONTH_NAME, col: BEST_COL['this'] });
      return out;
    }

    function build(key, mode) {
      var w = getW(key, mode);
      if (!w) return;
      var wNorm = mode !== 'without' ? getW(key, 'without') : null;   // the "without bulk orders" figure beside the title
      var bests = key === 'wow' ? bestWeeks(mode) : [];               // the reference lines (last month, this month)
      var bestNote = document.getElementById('wm-best-note');
      bestNote.innerHTML = bests.map(function (best) {
        return '<div><span style="color:' + best.col + ';font-weight:700">★ Best week in ' + best.name + ':</span> ' +
          best.wk.label + ' (' + best.wk.range + ') ' +
          '<strong style="color:#e2e8f0">' + fmt(best.bags) + ' bags</strong>' + (function () {
            var gap = w.now.bags - best.bags;
            if (best.i === selB) return ', and that is ' + w.now.label + '.';
            return '. ' + w.now.label + ' is <strong style="color:' + (gap < 0 ? '#f87171' : '#34d399') + '">' +
              sgn(gap) + ' bags (' + (gap >= 0 ? '+' : '−') + Math.abs(gap / best.bags * 100).toFixed(1) + '%)</strong> from it.';
          })() + '</div>';
      }).join('');
      var then = w.then, now = w.now, delta = now.bags - then.bags;
      var pct = then.bags ? delta / then.bags * 100 : 0;
      var down = delta < 0;

      // Steps between the two totals: days first, then regions — rises before falls (like the reel).
      var steps = [];
      if (w.daysEffect) steps.push({ label: 'Selling days', delta: w.daysEffect, days: true });
      w.regions.filter(function (r) { return r.delta; })
        .sort(function (a, b) { return b.delta - a.delta; })
        .forEach(function (r) { steps.push({ label: r.region, delta: r.delta, row: r }); });

      // The reason = the biggest step in the direction of the total move.
      var reason = null;
      steps.forEach(function (s) {
        if ((down ? s.delta < 0 : s.delta > 0) && (!reason || Math.abs(s.delta) > Math.abs(reason.delta))) reason = s;
      });

      var bars = [{ label: then.label, lo: 0, hi: then.bags, total: true, color: TOTAL_THEN, delta: then.bags }];
      var level = then.bags;
      steps.forEach(function (s) {
        var nx = level + s.delta;
        bars.push({ label: s.label, lo: Math.min(level, nx), hi: Math.max(level, nx), from: level, to: nx,
                    delta: s.delta, step: s, color: s.days ? DAYS : (s.delta > 0 ? C.green : C.red) });
        level = nx;
      });
      bars.push({ label: now.label, lo: 0, hi: now.bags, total: true, color: TOTAL_NOW, delta: now.bags });

      // Start the axis below the lowest level so a 20-bag move is still visible next to 3,000-bag totals.
      var lows = bars.filter(function (b) { return !b.total; }).map(function (b) { return b.lo; }).concat([then.bags, now.bags]);
      var highs = bars.map(function (b) { return b.hi; });
      bests.forEach(function (best) { lows.push(best.bags); highs.push(best.bags); });
      var lo = Math.min.apply(null, lows), hi = Math.max.apply(null, highs), span = Math.max(hi - lo, 1);
      var mag = Math.pow(10, Math.floor(Math.log10(span)));
      var yMin = Math.max(0, Math.floor((lo - span * 0.6) / mag) * mag);
      bars.forEach(function (b) { if (b.total) b.lo = yMin; });

      var pctTxt = function (d, base) {
        return (d >= 0 ? '+' : '−') + Math.abs(base ? d / base * 100 : 0).toFixed(1) + '%';
      };
      document.getElementById('wm-head').innerHTML =
        (mode === 'with' ? '' : '<span style="color:#94a3b8;font-weight:700">' + MODE_WORD[mode] + ' · </span>') +
        then.label + ' → ' + now.label + ': <span style="color:' + (down ? '#f87171' : '#34d399') + '">'
        + sgn(delta) + ' bags (' + pctTxt(delta, then.bags) + ')</span>' +
        (wNorm ? (function () {
          var nd = wNorm.now.bags - wNorm.then.bags;
          return '<span style="color:#94a3b8;font-weight:600;font-size:0.82rem"> · without bulk orders:</span>' +
            '<span style="color:' + (nd < 0 ? '#f87171' : '#34d399') + ';font-size:0.82rem">' + sgn(nd) + ' (' + pctTxt(nd, wNorm.then.bags) + ')</span>';
        })() : '');
      document.getElementById('wm-sub').textContent =
        then.range + ' (' + then.days + ' days, ' + fmt(then.bags) + ' bags)  vs  ' +
        now.range + ' (' + now.days + ' days, ' + fmt(now.bags) + ' bags)' +
        (then.days === now.days ? ' · same number of days' : '') +
        (yMin ? ' · axis starts at ' + fmt(yMin) : '');
      // "⚠ bulk 600 → 50" on a region in the All view, when bulk orders are part of its move.
      var bulkNote = function (r) {
        return (mode !== 'without' && r && r.region !== 'Corporate' && (r.bulkThen || r.bulkNow))
          ? '⚠ bulk orders ' + fmt(r.bulkThen) + ' → ' + fmt(r.bulkNow) : '';
      };

      var rEl = document.getElementById('wm-reason');
      if (!reason) {
        rEl.textContent = delta ? '' : 'No change.';
      } else if (reason.days) {
        rEl.innerHTML = '<strong style="color:#fbbf24">The reason:</strong> fewer selling days — ' + now.days + ' vs ' + then.days +
          ' (' + sgn(reason.delta) + ' bags at the old pace).';
      } else {
        var shops = (reason.row.shops || []).filter(function (s) { return s.delta; })
          .sort(function (a, b) { return down ? a.delta - b.delta : b.delta - a.delta; }).slice(0, 4);
        rEl.innerHTML = '<strong style="color:#fbbf24">The reason:</strong> ' + reason.label + ' ' +
          '<strong style="color:' + (reason.delta < 0 ? '#f87171' : '#34d399') + '">' + sgn(reason.delta) + ' bags</strong>' +
          ' (' + fmt(reason.row.then) + ' → ' + fmt(reason.row.now) + ')' +
          (shops.length ? ' — ' + shops.map(function (s) {
            return s.shop + ' <span style="color:' + (s.delta < 0 ? '#f87171' : '#34d399') + '">' + sgn(s.delta) + '</span>';
          }).join(', ') : '') + '.' +
          (bulkNote(reason.row) ? ' <span style="color:#fbbf24">' + bulkNote(reason.row) + '</span> — check <em>Without bulk orders</em>.' : '');
      }
      // Late-keyed sales moved back to their real day (lib/sales_date_fix, docs/shop-launch.md): say so when the
      // day they were moved to is in either period shown (the month view: in either month).
      var inPeriod = function (iso) {
        if (key === 'wow') {
          return [WEEKS[selA], WEEKS[selB]].some(function (wk) {
            if (!wk) return false;
            var s = new Date(wk.start + 'T00:00:00'), e = new Date(s); e.setDate(e.getDate() + wk.days - 1);
            var d = new Date(iso + 'T00:00:00'); return d >= s && d <= e;
          });
        }
        return true;
      };
      var fixDay = function (s, long) {
        return new Date(s.replace(' ', 'T')).toLocaleDateString('en-GB', long ? { weekday: 'long', day: 'numeric', month: 'short' } : { weekday: 'short', day: 'numeric', month: 'short' });
      };
      var fixes = ((WM && WM.dateFixes) || []).filter(function (f) { return inPeriod(f.asDate); });
      if (fixes.length) {
        rEl.innerHTML += fixes.map(function (f) {
          return '<div style="margin-top:0.35rem;color:#94a3b8;font-size:0.82rem"><strong style="color:#fbbf24">Printed sales:</strong> '
            + f.shop + '’s <strong style="color:#e2e8f0">' + fmt(f.bags) + ' bags</strong> from ' + fixDay(f.from) + ' morning to '
            + fixDay(f.to) + ' morning (' + f.days + ' days, keyed in late) are counted on <strong style="color:#e2e8f0">'
            + fixDay(f.asDate + ' 00:00', true) + '</strong>.</div>';
        }).join('');
      }

      // Value labels, connector lines and the "the reason" box.
      var deco = {
        id: 'wmDeco',
        afterDatasetsDraw: function (ch) {
          var x = ch.ctx, meta = ch.getDatasetMeta(0), ys = ch.scales.y;
          x.save();
          x.strokeStyle = 'rgba(148,163,184,0.55)'; x.lineWidth = 1;
          for (var i = 0; i < bars.length - 1; i++) {      // connector at each bar's closing level
            var a = meta.data[i], b = meta.data[i + 1];
            var lvl = bars[i].total ? bars[i].hi : bars[i].to, y = ys.getPixelForValue(lvl);
            x.beginPath(); x.moveTo(a.x + a.width / 2, y); x.lineTo(b.x - b.width / 2, y); x.stroke();
          }
          bests.forEach(function (best, n) {                // ★ best weeks: a dashed line each across the chart
            var by = ys.getPixelForValue(best.bags), ca = ch.chartArea;
            x.save();
            x.strokeStyle = best.col; x.globalAlpha = 0.8; x.lineWidth = 1.5; x.setLineDash([6, 4]);
            x.beginPath(); x.moveTo(ca.left, by); x.lineTo(ca.right, by); x.stroke();
            x.globalAlpha = 1; x.setLineDash([]); x.fillStyle = best.col; x.font = 'bold 11px "Segoe UI", system-ui, sans-serif';
            x.textAlign = 'center'; x.textBaseline = 'bottom';
            // Label over a bar slot whose bar, value label and reason box stay clear of the line —
            // last month's searched from the right, this month's from the left, so the two never meet.
            var slot = null, k;
            for (var s = 0; s < bars.length && !slot; s++) {
              k = n === 0 ? bars.length - 1 - s : s;
              var bt = ys.getPixelForValue(bars[k].hi), bb = ys.getPixelForValue(bars[k].lo);
              if (by - 16 > bb + 42 || by < bt - 24) slot = meta.data[k];
            }
            // Keep the whole label inside the chart (it was clipped at the right edge) on a dark backing.
            var txt = '★ Best ' + shortMonth(best.name) + ' ' + fmt(best.bags);
            x.font = 'bold 12px "Segoe UI", system-ui, sans-serif';
            var tw = x.measureText(txt).width, pad = 5;
            var tx = slot ? slot.x : (n === 0 ? ca.right : ca.left);
            tx = Math.min(Math.max(tx, ca.left + tw / 2 + pad + 2), ca.right - tw / 2 - pad - 2);
            var ty = Math.max(by - 4, ca.top + 18);
            x.fillStyle = 'rgba(15,23,42,0.92)';
            x.fillRect(tx - tw / 2 - pad, ty - 16, tw + pad * 2, 18);
            x.strokeStyle = best.col; x.lineWidth = 1;
            x.strokeRect(tx - tw / 2 - pad, ty - 16, tw + pad * 2, 18);
            x.fillStyle = best.col;
            x.fillText(txt, tx, ty);
            x.restore();
          });
          x.textAlign = 'center'; x.font = 'bold 12px "Segoe UI", system-ui, sans-serif';
          bars.forEach(function (bar, i) {
            var el = meta.data[i];
            var top = ys.getPixelForValue(bar.hi), bot = ys.getPixelForValue(bar.lo);
            var neg = !bar.total && bar.delta < 0;
            x.fillStyle = bar.total ? '#e2e8f0' : (bar.step.days ? '#fbbf24' : (neg ? '#f87171' : '#34d399'));
            x.textBaseline = neg ? 'top' : 'bottom';
            x.fillText(bar.total ? fmt(bar.hi) : sgn(bar.delta), el.x, neg ? bot + 4 : top - 4);
            if (bar.step && bar.step === reason) {
              var pad = 6, bw = el.width + pad * 2;
              x.strokeStyle = '#f59e0b'; x.lineWidth = 2.5;
              x.beginPath(); x.roundRect(el.x - bw / 2, top - 20, bw, bot - top + 40, 6); x.stroke();
              x.fillStyle = '#fbbf24'; x.textBaseline = 'top'; x.font = 'bold 12px "Segoe UI", system-ui, sans-serif';
              x.fillText('the reason', el.x, bot + 24);
            }
          });
          x.restore();
        }
      };

      if (chart) chart.destroy();
      chart = new Chart(cv, {
        type: 'bar',
        data: {
          labels: bars.map(function (b) { return b.label; }),
          datasets: [{
            data: bars.map(function (b) { return [b.lo, b.hi]; }),
            backgroundColor: bars.map(function (b) { return b.color; }),
            borderRadius: 3, borderSkipped: false, maxBarThickness: 64, categoryPercentage: 0.8,
          }]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          layout: { padding: { top: 22, bottom: 4 } },
          plugins: {
            legend: { display: false },
            tooltip: Object.assign({}, ttDefaults, {
              callbacks: {
                label: function (c) {
                  var b = bars[c.dataIndex];
                  if (b.total) return ' ' + fmt(b.hi) + ' bags';
                  if (b.step.days) return [' ' + sgn(b.delta) + ' bags',
                    ' ' + now.days + ' days vs ' + then.days + ' at ' + Math.round(then.bags / then.days).toLocaleString() + ' bags/day'];
                  var r = b.step.row, out = [' ' + sgn(b.delta) + ' bags', ' ' + fmt(r.then) + ' → ' + fmt(r.now) + ' bags'];
                  // Different week lengths: the earlier week is scaled to the later week's days before
                  // subtracting, so show that step (the rest of the raw gap is in the Selling days bar).
                  var sc = then.days && then.days !== now.days ? now.days / then.days : 1;
                  if (sc !== 1) out.push(' ' + fmt(r.then) + ' in ' + then.days + ' days = ' + fmt(Math.round(r.then * sc)) +
                    ' for ' + now.days + ' days, so ' + fmt(r.now) + ' is ' + sgn(b.delta),
                    ' (the rest of the gap is in the Selling days bar)');
                  if (bulkNote(r)) out.push(' ' + bulkNote(r));
                  if (sc !== 1) out.push(' Shops, earlier week scaled to ' + now.days + ' days:');
                  (r.shops || []).filter(function (s) { return s.delta; })
                    .sort(function (a, z) { return Math.abs(z.delta) - Math.abs(a.delta); }).slice(0, 6)
                    .forEach(function (s) { out.push('   ' + s.shop + ': ' + sgn(s.delta) + '  (' + fmt(Math.round(s.then * sc)) + ' → ' + fmt(s.now) + ')'); });
                  return out;
                }
              }
            })
          },
          scales: {
            x: { grid: { display: false }, ticks: { color: C.text, autoSkip: false, maxRotation: 40, font: { size: 11 } } },
            // suggestedMax: a best week above every bar still gets its line on the chart (it sat off the top).
            y: { min: yMin, suggestedMax: hi + span * 0.08, grid: { color: 'rgba(45,49,72,0.5)' }, ticks: { color: C.text, includeBounds: false } }
          }
        },
        plugins: [deco]
      });
    }

    // Two toggles: period (wow / mom) and bulk orders (with / without). Both remembered.
    var segP = document.getElementById('wm-period'), segM = document.getElementById('wm-mode');
    var pick = 'wow', mode = 'with';
    try { pick = localStorage.getItem(STORE + '-period') || 'wow'; mode = localStorage.getItem(STORE + '-mode') || 'with'; } catch (e) {}
    if (!hasKey(pick)) pick = hasKey('wow') ? 'wow' : 'mom';
    if (!getW(pick, mode)) mode = 'with';
    var selElA = document.getElementById('wm-a'), selElB = document.getElementById('wm-b');
    function fillWeeks() {                              // option text carries the bags for the current filter
      var bests = bestWeeks(mode);
      [selElA, selElB].forEach(function (el, j) {
        el.innerHTML = WEEKS.map(function (wk, i) {
          var star = bests.filter(function (b) { return b.i === i; })[0];
          return '<option value="' + i + '">' + wk.label + ' (' + wk.range + ') ' +
            fmt(Math.round(view(wk, mode).total)) + ' bags' + (star ? '  ★ best ' + shortMonth(star.name) : '') + '</option>';
        }).slice().reverse().join('');                   // latest week first
        el.value = String(j ? selB : selA);
      });
      document.getElementById('wm-weeks').style.display = pick === 'wow' ? 'flex' : 'none';
    }
    selElA.addEventListener('change', function () { selA = +selElA.value; redraw(); });
    selElB.addEventListener('change', function () { selB = +selElB.value; redraw(); });
    document.getElementById('wm-best').addEventListener('click', function () {
      var best = bestWeek(mode);
      if (!best) return;
      selA = best.i;
      if (selB === best.i) selB = best.i === WEEKS.length - 1 ? WEEKS.length - 2 : WEEKS.length - 1;
      redraw();
    });
    function mark(seg, attr, val, has) {
      Array.prototype.forEach.call(seg.querySelectorAll('.cp-seg'), function (b) {
        var on = b.getAttribute(attr) === val;
        b.classList.toggle('active', on); b.setAttribute('aria-pressed', on ? 'true' : 'false');
        b.disabled = !has(b.getAttribute(attr));
      });
    }
    function redraw() {
      mark(segP, 'data-p', pick, hasKey);
      mark(segM, 'data-m', mode, function (m) { return !!getW(pick, m); });
      if (WEEKS.length >= 2) fillWeeks();
      build(pick, mode);
    }
    function onClick(seg, attr, store, set) {
      seg.addEventListener('click', function (ev) {
        var b = ev.target.closest && ev.target.closest('.cp-seg');
        if (!b || b.disabled) return;
        var v = b.getAttribute(attr);
        try { localStorage.setItem(store, v); } catch (e) {}
        set(v); redraw();
      });
    }
    onClick(segP, 'data-p', STORE + '-period', function (v) { pick = v; });
    onClick(segM, 'data-m', STORE + '-mode',   function (v) { mode = v; });
    redraw();
  }
};
