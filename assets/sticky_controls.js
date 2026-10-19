/* assets/sticky_controls.js — keep a page's filter / controls bar (Market, Period, Share by, Sort…) at the top of the
 * view while the reader scrolls, so it can be changed beside any chart. Spec: docs/sticky-controls.md.
 *
 * Usage (after the bar exists), once per bar:
 *   StickyControls.init({ selector: '.controls' });                       // page-wide bar: follows the whole page
 *   StickyControls.init({ selector: el, within: '.panel' });              // a section's own bar: follows only while
 *                                                                          //   that section (closest .panel) is on screen
 * selector = CSS selector (every match becomes a bar) or an element. within = CSS selector of the ancestor that bounds
 * the bar (closest match), or an element; default = the whole page.
 *
 * How it pins: with a transform, never CSS sticky. Sticky only pins inside the bar's own parent box (most bars sit in
 * a short header block), and in the Streamlit dashboard the page's iframe is stretched to its full height, so the
 * PARENT document scrolls and nothing inside the page ever sticks. Like assets/page_sidebar.js (embedHost): standalone
 * → measured against this window; embedded → against the parent's viewport, below the parent's top bar (.tn-bar).
 * A transform leaves the bar in the layout, so nothing jumps; the compact look is height-compensated with a bottom
 * margin (the reserved space acts as the placeholder).
 */
(function (root) {
  'use strict';
  var bars = [], watchers = [], frame = null, bound = false, mo = null;
  var GAP = 0;   // px below the top edge / the host's top bar

  function injectCss() {
    if (document.getElementById('sc-css')) return;
    var s = document.createElement('style');
    s.id = 'sc-css';
    s.textContent = [
      '.sc-bar { position: relative; z-index: 80; will-change: transform; overflow-anchor: none; }',
      '.sc-bar.sc-pinned { background-color: var(--sc-bg, rgba(17, 19, 28, 0.97)) !important; border-radius: 8px;',
      '  box-shadow: 0 10px 22px -10px rgba(0, 0, 0, 0.75), 0 1px 0 rgba(148, 163, 184, 0.12);',
      '  backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }',
      '.sc-bar.sc-pinned.sc-compact { padding-top: 0.35rem !important; padding-bottom: 0.35rem !important; }',
      '@media print { .sc-bar { transform: none !important; box-shadow: none !important; } }'
    ].join('\n');
    document.head.appendChild(s);
  }

  // Embedded (Streamlit): the iframe is as tall as the page, so the parent scrolls. Null when the page scrolls itself.
  function embedHost() {
    if (!frame) return null;
    // streamlit_app.py marks the frame it stretches (data-dash-page): trust that. The height test alone flipped
    // for a moment when pinning added the bar's margin before the frame re-fitted → pin / unpin every scroll step.
    if (!frame.hasAttribute('data-dash-page') && document.documentElement.scrollHeight > window.innerHeight + 2) return null;
    try {
      var tb = window.parent.document.querySelector('.tn-bar'), inset = tb ? Math.max(0, tb.getBoundingClientRect().bottom) : 0;
      return { frameTop: frame.getBoundingClientRect().top, inset: inset };
    } catch (e) { return null; }
  }

  function setPinned(x, on) {
    if (on === x.pinned) return;
    var b = x.el;
    if (on) x.h0 = b.offsetHeight;                                  // full height before going compact
    x.pinned = on;
    b.classList.toggle('sc-pinned', on);
    b.classList.toggle('sc-compact', on);
    b.style.marginBottom = on ? (x.baseMB + Math.max(0, x.h0 - b.offsetHeight)) + 'px' : '';   // layout stays put
  }

  function place(x, host, off) {
    var b = x.el;
    if (!b.isConnected || b.offsetParent === null) {                 // hidden (another tab / region): reset
      if (x.t) { x.t = 0; b.style.transform = ''; }
      setPinned(x, false);
      return;
    }
    var rectTop = b.getBoundingClientRect().top - x.t;              // where the bar sits without the transform
    var want = host ? host.inset + GAP + off - (host.frameTop + rectTop) : GAP + off - rectTop;
    var limit;                                                       // the lowest the bar may travel (its bottom stays inside)
    if (x.box) limit = x.box.getBoundingClientRect().bottom - rectTop - b.offsetHeight - 8;
    else limit = document.documentElement.scrollHeight - (rectTop + (host ? 0 : window.scrollY)) - b.offsetHeight - 8;
    var t = Math.max(0, Math.min(Math.floor(limit), Math.ceil(want)));   // ceil: never a fraction above the edge
    setPinned(x, t > 0);
    if (t !== x.t) { x.t = t; b.style.transform = t ? 'translateY(' + t + 'px)' : ''; }
  }

  function update() {
    for (var i = bars.length - 1; i >= 0; i--) if (!bars[i].el.isConnected) bars.splice(i, 1);   // re-rendered away
    if (!bars.length) return;
    var host = embedHost(), off = 0;
    // bars pinned at the same time stack in page order, each below the one above it
    bars.slice().sort(function (a, b) { return a.el.compareDocumentPosition(b.el) & 4 ? -1 : 1; }).forEach(function (x) {
      place(x, host, off);
      if (x.pinned) {                                               // stack only by the part actually in the top zone
        var line = host ? host.inset - host.frameTop + GAP : GAP;   // the pin line, in this document's viewport
        var used = x.el.getBoundingClientRect().bottom - line;      // a bar being pushed out by its section's end uses less
        if (used + 4 > off) off = used + 4;
      }
    });
  }

  function bind() {
    if (bound) return;
    bound = true;
    try { if (window.frameElement && window.parent !== window) frame = window.frameElement; } catch (e) {}
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    if (frame) {
      try {
        window.parent.document.addEventListener('scroll', update, { capture: true, passive: true });
        window.parent.addEventListener('resize', update);
      } catch (e) {}
    }
    document.addEventListener('click', function () { setTimeout(update, 0); }, true);   // tabs / toggles change layout
    // charts / tables that render after load move the bar's place without any scroll: re-measure on size changes
    // (deferred, and only on a real height change: re-measuring inside the callback changes the bar's margin and
    //  would trip the browser's ResizeObserver loop warning)
    var lastH = -1;
    if (window.ResizeObserver) {
      try {
        new ResizeObserver(function () {
          var h = document.body.offsetHeight;
          if (h !== lastH) { lastH = h; setTimeout(update, 0); }
        }).observe(document.body);
      } catch (e) {}
    }
  }

  function init(opts) {
    opts = opts || {};
    var els = typeof opts.selector === 'string' ? Array.prototype.slice.call(document.querySelectorAll(opts.selector))
                                                : (opts.selector ? [opts.selector] : []);
    if (opts.watch && typeof opts.selector === 'string') watch(opts);
    if (!els.length) return [];
    injectCss();
    bind();
    var added = [];
    els.forEach(function (b) {
      if (!b || b.hasAttribute('data-sticky-controls')) return;
      b.classList.add('sc-bar');
      b.setAttribute('data-sticky-controls', '');
      if (opts.background) b.style.setProperty('--sc-bg', opts.background);
      var box = typeof opts.within === 'string' ? b.parentElement && b.parentElement.closest(opts.within) : (opts.within || null);
      var x = { el: b, box: box, t: 0, pinned: false, h0: b.offsetHeight, baseMB: parseFloat(getComputedStyle(b).marginBottom) || 0 };
      bars.push(x);
      added.push(b);
    });
    update();
    return added;
  }

  // watch: true — bars the page builds or rebuilds later (filter bars rendered by script) are pinned as they appear.
  function watch(opts) {
    if (watchers.indexOf(opts) < 0) watchers.push(opts);
    if (mo || !window.MutationObserver) return;
    var pending = false;
    mo = new MutationObserver(function () {
      if (pending) return;
      pending = true;
      setTimeout(function () {
        pending = false;
        watchers.forEach(function (w) { init({ selector: w.selector, within: w.within, background: w.background }); });
        update();
      }, 50);
    });
    mo.observe(document.body, { childList: true, subtree: true });
  }

  // The direct child of the closest `container` (CSS selector) that holds `el` — e.g. a card's header row around its
  // Period select. Returns [row, container] or null.
  function headerOf(el, container) {
    if (typeof el === 'string') el = document.querySelector(el);
    var c = el && el.closest(container);
    if (!c) return null;
    var n = el;
    while (n.parentElement && n.parentElement !== c) n = n.parentElement;
    return [n, c];
  }
  // Pin the header row of every card / section holding one of `ids` (control ids) inside that card.
  function initSections(ids, container) {
    ids.forEach(function (id) {
      var h = headerOf(document.getElementById(id), container);
      if (h) init({ selector: h[0], within: h[1] });
    });
  }

  root.StickyControls = { init: init, update: update, headerOf: headerOf, initSections: initSections, _bars: bars };
})(window);
