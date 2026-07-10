---
name: dashboard-design
description: Denri Africa Marketing Dashboard design system. Exact design tokens, component patterns (cards, KPI tiles, badges, tables, section headers), correct animation approach, and copy-paste templates for building or upgrading dashboard sections. Use when adding a new section, new dashboard page, or upgrading the visual treatment of an existing one.
---

# Denri Africa Dashboard Design System

This skill captures the exact design language used across all Denri Africa marketing dashboards. Use it to build new sections or pages that feel native to the existing shell — same tokens, same rhythm, same component vocabulary.

---

## Design Tokens

These values are used across every dashboard. Never guess — always pull from here.

### Colors

```css
:root {
  /* Surfaces */
  --bg-page:    #0f1117;   /* page background */
  --bg-card:    #1e2130;   /* card surface */
  --border:     #2d3148;   /* card/divider borders */
  --border-lo:  #1a1e2e;   /* subtle row dividers */

  /* Text */
  --text-hi:    #f8fafc;   /* headlines, card values */
  --text-mid:   #cbd5e1;   /* body copy */
  --text-lo:    #94a3b8;   /* labels, secondary */
  --text-muted: #64748b;   /* tertiary, timestamps */
  --text-dim:   #475569;   /* section headers, disabled */

  /* Brand accents */
  --green:      #10b981;   /* good / on-target */
  --green-hi:   #34d399;   /* high-contrast green text */
  --green-dim:  rgba(16, 185, 129, 0.15);
  --amber:      #f59e0b;   /* warning / at risk */
  --amber-hi:   #fbbf24;   /* high-contrast amber text */
  --amber-dim:  rgba(245, 158, 11, 0.15);
  --red:        #ef4444;   /* critical / bad */
  --red-hi:     #f87171;   /* high-contrast red text */
  --red-dim:    rgba(239, 68, 68, 0.15);
  --cyan:       #06b6d4;   /* neutral info / new */
  --cyan-hi:    #22d3ee;
  --cyan-dim:   rgba(6, 182, 212, 0.15);
  --purple:     #a78bfa;   /* Sinza region / secondary */
  --purple-dim: rgba(167, 139, 250, 0.15);
}
```

### Semantic color rules
| Meaning | Color |
|---|---|
| On target / good | `--green` / `--green-hi` |
| At risk / monitor | `--amber` / `--amber-hi` |
| Critical / bad | `--red` / `--red-hi` |
| Neutral / info | `--cyan` / `--cyan-hi` |
| Kenya region | `--green` |
| Sinza region | `--purple` |
| Uganda region | `--amber` |

**Never use color decoratively.** Every color choice must carry semantic meaning.

### Typography scale

```css
--text-section: 0.56rem;  /* section headers — UPPERCASE + tracking */
--text-label:   0.62rem;  /* card labels — UPPERCASE + tracking */
--text-xs:      0.68rem;  /* timestamps, footnotes */
--text-sm:      0.72rem;  /* sub-values, chart labels */
--text-body:    0.78rem;  /* body copy, table rows */
--text-md:      0.84rem;  /* card titles, insight headers */
--text-lg:      1rem;     /* small card values */
--text-xl:      1.4rem;   /* standard KPI values */
--text-2xl:     1.7rem;   /* hero KPI values */
--text-3xl:     2.2rem;   /* statement numbers */
```

Label pattern (always):
```css
font-size: 0.62rem;
font-weight: 700;
letter-spacing: 0.1em;
text-transform: uppercase;
color: var(--text-muted);
```

### Spacing / Border-radius

```css
--radius-card: 10px;   /* all cards */
--radius-tag:  4px;    /* badges/tags */
--radius-btn:  6px;    /* buttons */

--gap-card: 0.75rem;   /* gap between cards in a grid */
--pad-card: 1.1rem 1.25rem;  /* card internal padding */
```

---

## Components

### Card

The base building block. Every section uses this.

```html
<div class="card">
  <!-- content -->
</div>
```

```css
.card {
  background: #1e2130;
  border: 1px solid #2d3148;
  border-radius: 10px;
  padding: 1.1rem 1.25rem;
}
```

Hover state (for interactive/clickable cards):
```css
.card:hover {
  border-color: rgba(16, 185, 129, 0.35);
  transform: translateY(-2px);
  transition: border-color 0.2s, transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### KPI Tile

Standard metric card: value + label + sub-text.

```html
<div class="card kpi-card">
  <div class="kpi-label">Weekly Sales</div>
  <div class="kpi-value" style="color: var(--green-hi)">2,427</div>
  <div class="kpi-sub">vs 3,388 prior week (−961)</div>
</div>
```

```css
.kpi-label {
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #64748b;
  margin-bottom: 0.4rem;
}
.kpi-value {
  font-size: 1.7rem;
  font-weight: 800;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}
.kpi-sub {
  font-size: 0.72rem;
  color: #64748b;
  margin-top: 0.3rem;
}
```

KPI grid:
```html
<div class="card-grid">
  <!-- 4–6 kpi cards -->
</div>
```

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 0.75rem;
}
```

### Section Header (divider label)

```html
<div class="section-header">Weekly Breakdown</div>
```

```css
.section-header {
  font-size: 0.56rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #475569;
  margin: 2rem 0 0.75rem;
}
```

### Status Badge / Tag

```html
<span class="tag tag-green">Strong</span>
<span class="tag tag-red">Critical</span>
<span class="tag tag-amber">Watch</span>
<span class="tag tag-blue">Info</span>
```

```css
.tag {
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
}
.tag-green { background: rgba(16,185,129,0.2);  color: #6ee7b7; }
.tag-red   { background: rgba(239,68,68,0.2);   color: #fca5a5; }
.tag-amber { background: rgba(245,158,11,0.2);  color: #fcd34d; }
.tag-blue  { background: rgba(6,182,212,0.2);   color: #67e8f9; }
```

### Progress Bar

```html
<div class="bar-track">
  <div class="bar-fill" style="width: 66.7%; background: #10b981;"></div>
</div>
```

```css
.bar-track {
  height: 5px;
  background: #2d3148;
  border-radius: 3px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
```

### Alert / Banner Card

```html
<div class="alert alert-red">
  <div class="alert-icon">⚠</div>
  <div>
    <strong>Title here</strong>
    <p>Body copy here.</p>
  </div>
</div>
```

```css
.alert {
  border-radius: 10px;
  padding: 0.9rem 1.1rem;
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.82rem;
}
.alert-red   { background: rgba(239,68,68,0.1);  border: 1px solid rgba(239,68,68,0.3);  color: #fca5a5; }
.alert-amber { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.35); color: #fcd34d; }
.alert-green { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); color: #6ee7b7; }
.alert-blue  { background: rgba(6,182,212,0.1);  border: 1px solid rgba(6,182,212,0.3);  color: #67e8f9; }
```

### Table

```html
<table class="data-table">
  <thead>
    <tr>
      <th>#</th><th>Product</th><th>Sales</th>
    </tr>
  </thead>
  <tbody>
    <tr><td class="rank">1</td><td>Mini Umbra</td><td class="green">109</td></tr>
  </tbody>
</table>
```

```css
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.78rem;
}
.data-table th {
  text-align: left;
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #475569;
  padding: 0.4rem 0.5rem;
  border-bottom: 1px solid #2d3148;
}
.data-table td {
  padding: 0.5rem 0.5rem;
  border-bottom: 1px solid #1a1e2e;
  color: #cbd5e1;
}
.data-table tr:last-child td { border-bottom: none; }
.rank { color: #475569; font-weight: 700; }
```

### Signature Element — Flowing Border (Achievement/Pct cards)

Use on cards that show a percentage or achievement to make them stand out:

```css
.card.s1-pct { position: relative; overflow: hidden; }
.card.s1-pct::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, #10b981, #34d399, #06b6d4, #10b981);
  background-size: 200% 100%;
  animation: flow-border 3s linear infinite;
}
@keyframes flow-border {
  0%   { background-position: 0% 0%; }
  100% { background-position: 200% 0%; }
}
```

---

## Animation

### Card entrance — CORRECT approach

**Always use CSS `@keyframes` with `animation-fill-mode: both`.** Never use IntersectionObserver with `opacity: 0` as the initial state — it causes invisible content when the observer fires late or not at all (this burned us before).

```css
.s1-reveal {
  animation: card-in 0.55s cubic-bezier(0.16, 1, 0.3, 1) both;
  animation-delay: var(--s1-delay, 0ms);
}
@keyframes card-in {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

Stagger the delay via JS (after DOM is ready):
```javascript
document.querySelectorAll('.s1-reveal').forEach(function(el, i) {
  el.style.setProperty('--s1-delay', (i * 55) + 'ms');
});
```

The `animation-fill-mode: both` (abbreviated as the `both` keyword in the shorthand) guarantees the card is **always visible** — it holds the final state even before the animation starts.

### Hover spring

```css
.card {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1),
              border-color 0.2s ease;
}
.card:hover {
  transform: translateY(-2px);
  border-color: rgba(16, 185, 129, 0.35);
}
```

### Ease curves reference

```css
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);   /* entrances */
--ease-spring:   cubic-bezier(0.34, 1.56, 0.64, 1); /* hover, spring overshoot */
--ease-smooth:   cubic-bezier(0.4, 0, 0.2, 1);      /* general transitions */
```

---

## Page Structure Template

Use this as the starting point for any new dashboard page:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Dashboard Name — Denri Africa</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      line-height: 1.5;
      padding: 1.5rem 2rem 3rem;
    }

    /* ── Paste your card/grid/label/tag CSS from above ── */

    .page-header { margin-bottom: 2rem; }
    .page-header h1 { font-size: 1.2rem; font-weight: 800; color: #f8fafc; }
    .page-header p  { font-size: 0.72rem; color: #64748b; margin-top: 0.25rem; }
  </style>
</head>
<body>

  <div class="page-header">
    <h1>Dashboard Name</h1>
    <p>Subtitle or date range</p>
  </div>

  <!-- DATA INJECTION BLOCK -->
  <!-- SECTION_DATA_START -->
  <script>
    var DATA = { /* injected by Python */ };
  </script>
  <!-- SECTION_DATA_END -->

  <!-- KPI Grid -->
  <div class="section-header">Headline Numbers</div>
  <div class="card-grid" id="kpi-grid">
    <!-- JS-rendered cards go here -->
  </div>

  <!-- Charts (add Chart.js CDN in <head> if needed) -->

  <script>
    function render(DATA) {
      // populate cards, charts etc.
    }
    render(DATA);
  </script>

</body>
</html>
```

---

## Section Design Patterns

### 3-group card layout (On Offer / Not Offer / Pct)

Use when cards need to be separated by category with a label divider:

```html
<div class="s1-group-label"><span>Bags On Offer</span></div>
<div class="card-grid">
  <!-- cards with class="card s1-reveal s1-on-offer" -->
</div>

<div class="s1-group-label"><span>Not On Offer</span></div>
<div class="card-grid">
  <!-- cards with class="card s1-reveal s1-not-offer" -->
</div>

<div class="s1-group-label"><span>Achievement</span></div>
<div class="card-grid">
  <!-- cards with class="card s1-reveal s1-pct" -->
</div>
```

```css
.s1-group-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 1.25rem 0 0.6rem;
}
.s1-group-label::before,
.s1-group-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #2d3148;
}
.s1-group-label span {
  font-size: 0.58rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #475569;
  white-space: nowrap;
}

.card.s1-on-offer  { border-color: rgba(16,185,129,0.25); }
.card.s1-not-offer { border-color: rgba(239,68,68,0.2); }
.card.s1-pct       { border-color: rgba(6,182,212,0.2); }
```

### Regional comparison (Kenya / Sinza / Uganda)

3-column grid with a bar chart per region:
```html
<div style="display:grid; grid-template-columns: repeat(3,1fr); gap:0.75rem;">
  <!-- Kenya card with green, Sinza with purple, Uganda with amber -->
</div>
```

---

## Do / Don't

| Do | Don't |
|---|---|
| Use `animation-fill-mode: both` for card entrances | Use IntersectionObserver with `opacity: 0` as base |
| Semantic colors (green = good, red = bad) | Decorative color choices |
| `.card` container for everything | Bare `<div>` with inline background |
| `font-variant-numeric: tabular-nums` on KPI values | Numbers that jump widths when they change |
| `letter-spacing: 0.1em` on labels | Normal-spaced uppercase labels |
| `cubic-bezier(0.16, 1, 0.3, 1)` for eases | `ease`, `ease-in-out`, `linear` |
| Section headers at `0.56rem` uppercase | Full-size headings between card groups |
| Chart.js from CDN in `<head>` | Inline `<script src>` before chart canvas |
| One `Chart.defaults` setup block at top | Repeating chart default settings per chart |
| Destroy old chart before re-render | Creating duplicate chart on same canvas |

---

## Related skills

- **dataviz-charts** — Chart.js patterns for bar, donut, line, sparkline charts in this theme
- **dashboard-insights** — Extract live data from dashboard HTML files and generate an insights report
- **design-taste-frontend** — General anti-slop frontend design rules and pre-flight checklist
- **high-end-visual-design** — Premium glassmorphism and animation patterns (use selectively — some patterns like IntersectionObserver opacity:0 must be adapted using the correct approach above)
