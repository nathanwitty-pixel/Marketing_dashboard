# Chart type switcher (every chart, every menu)

- **File:** `chart_switcher.js` (repo root) — one shared script.
- **Loaded by:** every page that draws Chart.js charts, via
  `<script src="chart_switcher.js"></script>` placed **right after** the Chart.js `<script>` tag
  (it must run before the page creates its charts). `monthly_report.py` writes the tag into
  `monthly_report.html` and the month archives (`report_YYYY_month.html`).
- **Streamlit (`streamlit_app.py`, port 8501):** `components.html()` renders each page in a frame
  with no URL, so a local `<script src>` can't load there. The app **inlines every local `.js`**
  a page references before rendering it, and folds the script's mtime into the frame's cache
  token so editing `chart_switcher.js` refreshes every page. (`main.py`'s static server loads
  the file normally.)

## What it does

Every chart gets a small **chart-type button** in its top-right corner. It opens a menu of the
chart types that suit that chart's data; picking one redraws the **same chart object in
place** (so the page's own code — re-renders, period switches, `chart.destroy()` — keeps
working). **Original** restores the page's own design. The choice is remembered per chart in
this browser (`localStorage`, key `cs:<page>:<canvas id>`, value `<type>|<original shape>`), and
re-applied when the page redraws the **same kind** of chart (e.g. after a period change). If the
page redraws it as a different kind — a page's own type toggle, like Current Performance's
Area / Line / Bar / Radar — the remembered choice is dropped, so the page's toggle wins.

The page's own inline Chart.js plugins (value labels, centre text…) run only on the Original,
Column, Stacked, Line, Area, Stacked-area and Combo views; they assume the original data shape
and would break on the reshaped views.

## Types offered (only when the data suits them)

| Type | Built from | Offered when |
|---|---|---|
| Column / Bar (horizontal) | the chart's labels × series | always |
| Stacked column | series stacked | 2+ series |
| Line / Area | series as lines (area = filled) | always |
| Stacked area | filled lines, stacked | 2+ series |
| Combo | first series as columns, the rest as lines | 2+ series |
| Pie / Doughnut / Polar area | 1 series: one slice per label · 2+ series: one slice per **series total** | no negative values |
| Radar | labels as spokes, series as shapes | 3+ labels |
| Funnel | same slices as Pie, largest first, centred bars | no negative values, 2+ slices |
| Waterfall | per-label totals as running steps + a Total bar (green up / red down) | 2+ labels |
| Treemap | same slices as Pie, as nested rectangles (`chartjs-chart-treemap`, loaded from jsDelivr on first use) | no negative values |

**Not offered:** Map, Stock (candlestick), Box & whisker, Histogram, XY scatter and Sunburst —
they need data the dashboard's charts don't hold (coordinates, open/high/low/close,
per-observation distributions, x/y pairs, a hierarchy).

Tooltips: the page's own tooltip text is kept for the column / stacked / line / area / combo
views (same data shape); the other views use a generic tooltip that formats the value with
the chart's own axis format when it has one.

## Skipped charts

A chart gets **no** button when: its canvas is smaller than 200 × 120 px (progress rings,
sparklines), its data is x/y points (scatter/bubble), or it opts out with
`<canvas data-chart-switch="off">` or `options.plugins.chartSwitch = false`.

## Layout rules

- The button sits in a **34 px strip reserved down the right edge** of the chart (added to the
  chart's own `layout.padding.right` on every layout), so it never covers bars, lines, labels,
  the legend or the title.
- A chart that is hidden (e.g. the other half of a Bars ⇄ Trend toggle) hides its button too —
  a `ResizeObserver` on the canvas shows / hides / re-places it.
- All CSS classes are prefixed **`chartsw-`**. (The first version used `cs-btn`, which New Products
  and Posting already use for their own drop-down buttons — it restyled and squashed them.)
