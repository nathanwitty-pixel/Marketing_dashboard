/* shop_bday.js — 🎂 shop-birthday badges (spec: docs/shop-birthdays.md).
   Pages pass the generator's map {SHOP_KEY: {shop, date, days, age, label, dateLabel}} (from
   lib/shop_birthdays.by_shop — only shops within 30 days before / 1 day after their birthday).
     ShopBday.badge(map, shopName) → '<span class="bday">🎂 …</span>' or ''
     ShopBday.strip(map)           → a one-line "Shop birthdays coming up" note, or ''
   Colours use the page palette (dark); v5_theme.js remaps them for the light theme. */
(function () {
  if (window.ShopBday) return;
  var ALIAS = { 'NAIROBI': 'STARMALL', 'TANZANIA': 'SINZA', 'DAR-ES-ALAM': 'SINZA', 'KTDA SHOP': 'KTDA', 'WEBSITE SALES': 'WEBSITE' };
  function key(s) { var k = String(s == null ? '' : s).trim().toUpperCase().replace(/\s+/g, ' '); return ALIAS[k] || k; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  var css = document.createElement('style');
  css.textContent =
    '.bday{display:inline-flex;align-items:center;gap:0.2rem;margin-left:0.35rem;padding:0.05rem 0.4rem;border-radius:999px;' +
    'font-size:0.66rem;font-weight:700;white-space:nowrap;vertical-align:middle;cursor:help;' +
    'background:rgba(236,72,153,0.14);color:#f9a8d4;border:1px solid rgba(236,72,153,0.38)}' +
    '.bday.now{background:rgba(236,72,153,0.28);color:#fce7f3}' +
    '.bday-strip{display:flex;flex-wrap:wrap;align-items:center;gap:0.4rem 0.8rem;margin:0.4rem 0 0.9rem;padding:0.5rem 0.75rem;' +
    'border-radius:10px;background:rgba(236,72,153,0.08);border:1px solid rgba(236,72,153,0.28);font-size:0.78rem;color:#e2e8f0}' +
    '.bday-strip .t{font-size:0.66rem;font-weight:700;color:#f9a8d4;text-transform:uppercase;letter-spacing:0.08em}';
  (document.head || document.documentElement).appendChild(css);

  function short(e) {
    var d = e.days;
    var when = d === 0 ? 'today' : d === 1 ? 'tomorrow' : d < 0 ? 'yesterday' : 'in ' + d + 'd';
    return '🎂 ' + (e.age ? ordinal(e.age) + ' ' : '') + 'b’day ' + when;
  }
  function ordinal(n) { var s = ['th', 'st', 'nd', 'rd'], v = n % 100; return n + (s[(v - 20) % 10] || s[v] || s[0]); }

  function badge(map, name) {
    var e = (map || {})[key(name)];
    if (!e) return '';
    return '<span class="bday' + (Math.abs(e.days) <= 1 ? ' now' : '') + '" title="' +
      esc(e.shop + ' — ' + e.label.replace(/^🎂\s*/, '') + ' (' + e.dateLabel + '). Plan a birthday offer / posts for this shop.') +
      '">' + short(e) + '</span>';
  }

  function strip(map) {
    var list = Object.keys(map || {}).map(function (k) { return map[k]; }).sort(function (a, b) { return a.days - b.days; });
    if (!list.length) return '';
    return '<div class="bday-strip"><span class="t">Shop birthdays coming up</span>' + list.map(function (e) {
      return '<span><b>' + esc(e.shop) + '</b> ' + esc(e.label) + ' &middot; ' + esc(e.dateLabel) + '</span>';
    }).join('') + '</div>';
  }

  window.ShopBday = { badge: badge, strip: strip, key: key };
})();
