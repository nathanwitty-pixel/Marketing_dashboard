/* kpi_anim.js — KPI tiles fade up and their numbers count up, with Anime.js 4 (assets/vendor/anime.umd.min.js,
   MIT, https://github.com/juliangarnier/anime). streamlit_app.py inlines both into every dashboard page.

   - A tile's value appears for the first time on this page → the tile fades up (staggered) and the number
     counts from 0.
   - The value changes later (Period dropdown, custom range) → it counts from the old number to the new one.
   - Same value again → nothing.   prefers-reduced-motion → no motion at all.
   - Only a value holding exactly one number is counted ("KES 1,234,567", "8,421", "45.3%", "-6,839");
     dates, names and "Week 3 of 52" just appear.
   - The page's own scripts own the DOM: we only change the existing text node's nodeValue, always finish on
     the exact original text, animate opacity / transform only and clear them afterwards. */
(function () {
  if (window.__kpiAnim || !window.anime) return;
  window.__kpiAnim = 1;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var A = window.anime;
  var VAL = '.k-val, .card-value, .m-val, .kpi-value';
  var TILE = '.card, .kpi, .mini, .exec';
  var NUM = /[-−]?\d[\d,]*(?:\.\d+)?/g;
  var seen = {};      // key → last number shown
  var active = {};    // key → {node, anim} while counting
  var shown = new WeakSet();   // tiles that already faded in

  function key(el) {
    if (el.id) return '#' + el.id;
    var t = el.closest(TILE) || el.parentElement;
    var l = t && t.querySelector('[class*="lbl"], [class*="label"], [class*="title"]');
    return (l && l !== el ? l.textContent.trim() : '') + '|' + el.className;
  }

  // The one text node holding the number, split into prefix / number / suffix — or null.
  function parse(el) {
    var txt = el.textContent || '';
    var all = txt.match(NUM);
    if (!all || all.length !== 1) return null;
    if (/[A-Za-z]{2,}/.test(txt.replace(all[0], '').replace(/KES|bags?|units?|pcs/gi, ''))) return null;
    var w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), node;
    while ((node = w.nextNode())) {
      var m = node.nodeValue.match(NUM);
      if (m && m.length === 1) {
        var raw = m[0], i = node.nodeValue.indexOf(raw);
        var n = parseFloat(raw.replace(/,/g, '').replace('−', '-'));
        if (!isFinite(n)) return null;
        return { node: node, orig: node.nodeValue, pre: node.nodeValue.slice(0, i),
                 post: node.nodeValue.slice(i + raw.length), n: n,
                 dec: (raw.split('.')[1] || '').length, comma: raw.indexOf(',') >= 0,
                 minus: raw.charAt(0) === '−' ? '−' : '-' };
      }
    }
    return null;
  }

  function fmt(v, p) {
    var s = Math.abs(v).toFixed(p.dec);
    if (p.comma) {
      var parts = s.split('.');
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      s = parts.join('.');
    }
    return (v < 0 && Math.abs(v) >= Math.pow(10, -p.dec) / 2 ? p.minus : '') + s;
  }

  function count(k, p, from) {
    var o = { v: from };
    active[k] = { node: p.node, anim: A.animate(o, {
      v: p.n, duration: 900, ease: 'outExpo',
      onUpdate: function () { p.node.nodeValue = p.pre + fmt(o.v, p) + p.post; },
      onComplete: function () { p.node.nodeValue = p.orig; delete active[k]; }
    }) };
    p.node.nodeValue = p.pre + fmt(from, p) + p.post;   // start state now, before paint
  }

  function scan() {
    var tiles = [];
    document.querySelectorAll(VAL).forEach(function (el) {
      var k = key(el), a = active[k];
      if (a && el.contains(a.node)) return;              // our own count-up is running here
      var p = parse(el);
      if (!p) return;
      if (a) { a.anim.pause(); delete active[k]; }       // the page redrew it mid-count
      var t = el.closest(TILE);
      if (!(k in seen)) {
        if (t && !shown.has(t)) { shown.add(t); tiles.push(t); }
        count(k, p, 0);
      } else if (seen[k] !== p.n) {
        count(k, p, seen[k]);
      }
      seen[k] = p.n;
    });
    if (tiles.length) {
      tiles.forEach(function (t) { t.style.opacity = '0'; });
      A.animate(tiles, {
        opacity: [0, 1], translateY: [12, 0], duration: 600, ease: 'outExpo', delay: A.stagger(45),
        onComplete: function () {
          tiles.forEach(function (t) { t.style.removeProperty('opacity'); t.style.removeProperty('transform'); });
        }
      });
    }
  }

  new MutationObserver(scan).observe(document.documentElement, { childList: true, subtree: true });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', scan); else scan();
})();
