/* gold_star.js — paints every ★ in a Chart.js hover box gold (#fbbf24).
   Chart.js draws a tooltip's lines in one colour, so a "★ Thika: +13" line would get a white star.
   This global plugin swaps ctx.fillText only while the tooltip is drawn: the text before the ★ and
   after it keep the tooltip's colour, the ★ itself is filled gold. Load right after Chart.js.
   Comparison tooltips use the ★ to mark what improved (docs/current-performance.md). */
(function () {
  'use strict';
  var Chart = window.Chart, GOLD = '#fbbf24', STAR = '★';
  if (!Chart || !Chart.register || window.__goldStar) return;
  window.__goldStar = true;
  Chart.register({
    id: 'goldStar',
    beforeTooltipDraw: function (ch) {
      var ctx = ch.ctx, orig = CanvasRenderingContext2D.prototype.fillText;
      ctx.fillText = function (t, x, y, mw) {
        var i = typeof t === 'string' ? t.indexOf(STAR) : -1;
        if (i < 0 || (ctx.textAlign !== 'left' && ctx.textAlign !== 'start')) return orig.apply(ctx, arguments);
        var col = ctx.fillStyle, pre = t.slice(0, i), sx = x + ctx.measureText(pre).width;
        if (pre) orig.call(ctx, pre, x, y);
        ctx.fillStyle = GOLD; orig.call(ctx, STAR, sx, y);
        ctx.fillStyle = col; orig.call(ctx, t.slice(i + 1), sx + ctx.measureText(STAR).width, y);
      };
    },
    afterTooltipDraw: function (ch) { delete ch.ctx.fillText; }   // back to the prototype's fillText
  });
})();
