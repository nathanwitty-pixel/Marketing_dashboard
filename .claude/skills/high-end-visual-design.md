---
name: high-end-visual-design
description: Premium agency-level UI/UX framework for producing $150k+ digital experiences. Glassmorphism, micro-interactions, GSAP animations, bento grids, double-bezel card architecture. Use when the goal is to make a UI feel dramatically more premium, animated, and visually striking.
---

# High-End Visual Design — Vanguard UI Architect

Engineer premium, agency-level digital experiences. Every output must feel like it came from a top-tier creative studio — not a template.

## Banned Defaults (Non-Negotiable)

Never use:
- Fonts: Inter, Roboto, Open Sans without explicit justification
- Generic 1px solid gray borders (#e5e7eb, #d1d5db)
- Standard `linear` or `ease-in-out` transitions — always use custom cubic-bezier
- Symmetrical Bootstrap-style equal-column grids
- Plain flat cards with no depth, shadow, or layering
- `box-shadow: 0 1px 3px rgba(0,0,0,0.1)` — this is the generic shadow

## Creative Variance Engine

Before designing, select from these archetypes:

**Vibe Archetypes** (pick one):
- **Ethereal Glass** — frosted glass layers, blur backdrops, translucent surfaces, soft luminous glows
- **Editorial Luxury** — high contrast, dramatic typography, editorial whitespace, precise grid discipline
- **Soft Structuralism** — structured bento grids, warm neutrals, deliberate asymmetry, tactile depth

**Layout Archetypes** (pick one):
- **Asymmetrical Bento** — irregular grid cells, varying aspect ratios, visual weight contrast
- **Z-Axis Cascade** — elements layered in 3D space, overlapping cards, depth stacking
- **Editorial Split** — strong vertical division, content and visual in deliberate tension

## Double-Bezel Card Architecture

All cards must use nested shell architecture:
```css
.card-outer {
  /* Outer shell: border, subtle gradient, padding */
  background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 16px;
  padding: 2px; /* Creates bezel gap */
}
.card-inner {
  /* Inner core: actual content surface */
  background: rgba(15, 17, 26, 0.85);
  border-radius: 14px;
  padding: 24px;
  backdrop-filter: blur(12px);
}
```

## Motion Requirements

**Custom cubic-bezier curves only:**
```css
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
--ease-in-out-circ: cubic-bezier(0.85, 0, 0.15, 1);
--spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* slight overshoot */
```

**GPU-safe animations only** — use exclusively `transform` and `opacity`:
```css
/* CORRECT */
transform: translateY(0) scale(1);
opacity: 1;

/* NEVER DO THIS — causes layout recalc */
/* top, left, width, height, margin, padding */
```

**Staggered scroll-reveal with IntersectionObserver:**
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      setTimeout(() => {
        entry.target.style.transform = 'translateY(0)';
        entry.target.style.opacity = '1';
      }, i * 80); // 80ms stagger between cards
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.card').forEach(el => {
  el.style.transform = 'translateY(24px)';
  el.style.opacity = '0';
  el.style.transition = 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.6s ease';
  observer.observe(el);
});
```

**Hover micro-interactions:**
```css
.card {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1),
              box-shadow 0.3s ease;
}
.card:hover {
  transform: translateY(-4px) scale(1.01);
  box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.08);
}
```

## Typography

Premium font pairings for dashboards:
- **Display values**: `Geist Mono`, `JetBrains Mono`, or `DM Mono` — numbers feel precise
- **Labels/headers**: `Geist`, `DM Sans`, or `Plus Jakarta Sans` — clean and modern
- **Never**: Times New Roman, Arial, Roboto as a design choice

Type scale must be intentional:
```css
--text-xs: 0.65rem;   /* subtle labels */
--text-sm: 0.75rem;   /* card labels, table headers */
--text-base: 0.875rem; /* body */
--text-lg: 1.125rem;  /* section titles */
--text-xl: 1.5rem;    /* card values */
--text-2xl: 2rem;     /* hero numbers */
--text-3xl: 2.75rem;  /* statement numbers */
```

## Spacing — Massive and Deliberate

Premium designs breathe. Don't compress:
- Card internal padding: `py-6 px-6` minimum (24px), ideally `py-8 px-8` (32px)
- Between card groups: `mt-8` to `mt-12` (32px–48px)
- Section gaps: `py-16` to `py-24` (64px–96px)

## Glassmorphism Recipe (for dark dashboards)

```css
.glass-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border-radius: 16px;
  box-shadow:
    0 4px 24px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.06);
}
```

## Gradient Accents

Use subtle gradients to add depth to card values and borders:
```css
/* Glowing number effect */
.value-glow {
  background: linear-gradient(135deg, #60a5fa, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 12px rgba(96, 165, 250, 0.4));
}

/* Accent border glow */
.card-accent {
  border-image: linear-gradient(135deg, rgba(96,165,250,0.6), transparent) 1;
}
```

## Mobile Collapse

Below 768px:
- All asymmetric bento grids collapse to single column
- Z-axis layering flattens (no overlapping elements)
- Font sizes drop one step on the scale
- Horizontal scroll allowed ONLY for data tables, never for cards

## Pre-Output Checklist

Before delivering, verify:
- [ ] No banned fonts used without explicit justification
- [ ] All cards use double-bezel or equivalent depth architecture
- [ ] All animations use only transform/opacity
- [ ] Custom cubic-bezier used (not linear or ease-in-out)
- [ ] Hover micro-interactions on all interactive cards
- [ ] Staggered reveal on card grids
- [ ] Minimum 4.5:1 contrast on all text (WCAG AA)
- [ ] Mobile collapse handled below 768px
- [ ] No symmetrical equal-column grid without intentional reason
- [ ] At least one signature visual moment the page is remembered by
