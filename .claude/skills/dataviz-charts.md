---
name: dataviz-charts
description: Add Chart.js charts to the Denri Africa dark HTML dashboards. Bar, line, area, donut, and sparkline patterns pre-tuned for the existing dark theme (#0f1117 bg, emerald/amber/cyan accent palette). Use when the user asks to add graphs, charts, or visual data trends to any dashboard page.
---

# Dataviz — Charts for Denri Africa Dashboards

Add interactive charts to the existing dark HTML dashboards using Chart.js. Every chart must match the established design system.

## Library

Always use Chart.js loaded from CDN — already available since dashboards are served via http.server:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

Place the script tag in `<head>` or just before the chart's `<canvas>` element.

## Design System — Match Existing Dashboard

```javascript
const THEME = {
  bg:       '#0f1117',
  surface:  '#1e2130',
  border:   '#2d3148',
  text:     '#94a3b8',
  textHi:   '#f8fafc',
  green:    '#10b981',
  greenDim: 'rgba(16, 185, 129, 0.15)',
  amber:    '#f59e0b',
  amberDim: 'rgba(245, 158, 11, 0.15)',
  cyan:     '#06b6d4',
  cyanDim:  'rgba(6, 182, 212, 0.15)',
  red:      '#ef4444',
  purple:   '#a78bfa',
};
```

**Always apply these global Chart.js defaults before creating any chart:**

```javascript
Chart.defaults.color          = THEME.text;
Chart.defaults.borderColor    = THEME.border;
Chart.defaults.font.family    = "'Segoe UI', system-ui, sans-serif";
Chart.defaults.font.size      = 11;
```

## Chart Container Pattern

Every chart lives in a card matching the existing `.card` style:

```html
<div class="card" style="padding: 1.2rem 1.4rem;">
  <div style="font-size:0.72rem; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:#94a3b8; margin-bottom:0.75rem;">
    Chart Title
  </div>
  <div style="position:relative; height:220px;">
    <canvas id="my-chart"></canvas>
  </div>
</div>
```

Set a fixed pixel height on the wrapper div, not on the canvas itself — Chart.js handles canvas sizing automatically.

## Chart Recipes

### Bar Chart (weekly/monthly comparison)

```javascript
new Chart(document.getElementById('bar-chart'), {
  type: 'bar',
  data: {
    labels: ['W1', 'W2', 'W3', 'W4'],
    datasets: [{
      label: 'Sales',
      data: [1200, 1800, 1540, 2100],
      backgroundColor: THEME.greenDim,
      borderColor: THEME.green,
      borderWidth: 1.5,
      borderRadius: 4,
      borderSkipped: false,
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: '#1e2130',
        borderColor: '#2d3148',
        borderWidth: 1,
        titleColor: '#f8fafc',
        bodyColor: '#94a3b8',
        padding: 10,
      }
    },
    scales: {
      x: { grid: { color: 'rgba(45,49,72,0.5)' }, ticks: { color: THEME.text } },
      y: { grid: { color: 'rgba(45,49,72,0.5)' }, ticks: { color: THEME.text } }
    }
  }
});
```

### Line / Area Chart (trend over time)

```javascript
new Chart(document.getElementById('line-chart'), {
  type: 'line',
  data: {
    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    datasets: [{
      label: 'Sales',
      data: [800, 1200, 950, 1500],
      borderColor: THEME.cyan,
      backgroundColor: THEME.cyanDim,
      borderWidth: 2,
      fill: true,
      tension: 0.4,
      pointRadius: 3,
      pointBackgroundColor: THEME.cyan,
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false }, tooltip: { /* same as above */ } },
    scales: {
      x: { grid: { color: 'rgba(45,49,72,0.4)' }, ticks: { color: THEME.text } },
      y: { grid: { color: 'rgba(45,49,72,0.4)' }, ticks: { color: THEME.text } }
    }
  }
});
```

### Donut Chart (split / composition)

```javascript
new Chart(document.getElementById('donut-chart'), {
  type: 'doughnut',
  data: {
    labels: ['Posted', 'Not Posted'],
    datasets: [{
      data: [68, 32],
      backgroundColor: [THEME.greenDim, 'rgba(45,49,72,0.6)'],
      borderColor:     [THEME.green,    THEME.border],
      borderWidth: 1.5,
      hoverOffset: 4,
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '72%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: { color: THEME.text, padding: 16, boxWidth: 10, font: { size: 11 } }
      },
      tooltip: { backgroundColor: '#1e2130', borderColor: '#2d3148', borderWidth: 1 }
    }
  }
});
```

### Sparkline (tiny inline trend, no axes)

```javascript
new Chart(document.getElementById('spark'), {
  type: 'line',
  data: {
    labels: ['','','','','','',''],
    datasets: [{ data: [3,5,4,7,6,9,8], borderColor: THEME.green, borderWidth: 1.5,
                 pointRadius: 0, fill: false, tension: 0.4 }]
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: { display: false }, tooltip: { enabled: false } },
    scales: { x: { display: false }, y: { display: false } },
    animation: false,
  }
});
```

Sparkline container: `style="position:relative; height:36px; width:80px;"` — place inline next to a card value.

### Grouped Bar (compare Kenya / Sinza / Uganda)

```javascript
new Chart(document.getElementById('grouped-chart'), {
  type: 'bar',
  data: {
    labels: ['Week 1','Week 2','Week 3','Week 4'],
    datasets: [
      { label: 'Kenya',  data: [...], backgroundColor: THEME.greenDim, borderColor: THEME.green,  borderWidth:1.5, borderRadius:3 },
      { label: 'Sinza',  data: [...], backgroundColor: 'rgba(167,139,250,0.15)', borderColor: THEME.purple, borderWidth:1.5, borderRadius:3 },
      { label: 'Uganda', data: [...], backgroundColor: THEME.amberDim, borderColor: THEME.amber,  borderWidth:1.5, borderRadius:3 },
    ]
  },
  options: {
    responsive: true, maintainAspectRatio: false,
    plugins: { legend: { labels: { color: THEME.text, boxWidth: 10, font: { size: 11 } } }, tooltip: { backgroundColor: '#1e2130', borderColor: '#2d3148', borderWidth: 1 } },
    scales: {
      x: { grid: { display: false }, ticks: { color: THEME.text } },
      y: { grid: { color: 'rgba(45,49,72,0.5)' }, ticks: { color: THEME.text } }
    }
  }
});
```

## Connecting to Live Dashboard Data

The dashboards inject data via `<!-- DATA_START --> ... <!-- DATA_END -->` blocks. Charts should read from the same JS variables already set by `renderKPIs()` or equivalent functions — never duplicate the data fetch.

**Pattern:** add chart rendering at the end of the existing render function, after KPI values are set:

```javascript
// At the end of renderKPIs() or equivalent:
renderS1Chart(PA);   // pass the already-fetched data object

function renderS1Chart(PA) {
  var ctx = document.getElementById('s1-trend-chart');
  if (!ctx || !PA) return;
  new Chart(ctx, { /* ... using PA.weeklySales, PA.monthlySales etc */ });
}
```

## Chart Placement Rules

- **Full-width charts** (trend lines, grouped bars): `grid-column: 1 / -1` inside `.card-grid`
- **Half-width charts** (donut, single bar): normal card, `minmax(280px, 1fr)` grid cell
- **Sparklines**: inside existing KPI cards, beside the `.card-value`
- Always add the Chart.js `<script>` tag once per HTML file, in `<head>`
- Destroy existing chart instance before re-rendering: `if (window._myChart) window._myChart.destroy();`

## Tooltip Defaults (reuse everywhere)

```javascript
const TOOLTIP = {
  backgroundColor: '#1e2130',
  borderColor: '#2d3148',
  borderWidth: 1,
  titleColor: '#f8fafc',
  bodyColor: '#94a3b8',
  padding: 10,
  cornerRadius: 6,
};
```
