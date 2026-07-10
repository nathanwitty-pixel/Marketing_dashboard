---
name: design-taste-frontend
description: Anti-slop frontend skill. Enforces non-templated, production-grade UI. Sets DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY dials. Hard bans on AI design clichés. 90+ pre-flight checklist. Use when rebuilding or upgrading any frontend to avoid generic AI aesthetics.
---

# design-taste-frontend — Anti-Slop Frontend Skill

Build high-quality, non-templated frontend interfaces. Never default to AI clichés.

## Three Dials — Set These First

Before writing a single line of code, explicitly set and declare:

```
DESIGN_VARIANCE:   [low | medium | high]
  low    = conservative, enterprise, systematic
  medium = modern but approachable, slight personality
  high   = distinctive, risky, memorable

MOTION_INTENSITY:  [none | subtle | moderate | expressive]
  none       = purely static
  subtle     = hover states, opacity fades only
  moderate   = scroll reveals, staggered entrances, smooth transitions
  expressive = GSAP orchestration, physics springs, cinematic moments

VISUAL_DENSITY:    [sparse | balanced | dense]
  sparse   = massive whitespace, one idea per screen
  balanced = comfortable reading rhythm, moderate info density
  dense    = data-rich, every pixel earns its place (analytics dashboards)
```

For a marketing analytics dashboard: `DESIGN_VARIANCE: medium`, `MOTION_INTENSITY: moderate`, `VISUAL_DENSITY: dense`

## Hard Bans — Never Do These

**Typography bans:**
- No Fraunces, Instrument Serif, or Playfair Display as default display fonts
- No generic Inter/Roboto without a clear reason
- No mixed serif + sans combinations that look like Medium articles

**Color bans:**
- No beige + brass + oxblood "premium consumer" palette as default
- No AI-purple gradient (#7c3aed → #a855f7) mesh background as hero
- No generic blue (#3b82f6) as the only accent color

**Layout bans:**
- No centered 3-column equal feature cards (the "three pillars" layout)
- No fake div-based product screenshot mockups
- No hero with big headline + subtext + two CTA buttons + hero image — that exact pattern

**Code bans:**
- No `window.addEventListener('scroll', ...)` — use Motion `useScroll()`, GSAP ScrollTrigger, or CSS `@scroll-timeline`
- No hand-rolled SVG icons — use Phosphor, HugeIcons, Radix Icons, or Tabler
- No inline styles for anything that recurs (use CSS custom properties)
- No `transition: all 0.3s ease` — be specific about what transitions

**Content bans:**
- No em-dashes (—) on any visible page surface
- No "Revolutionize your workflow" headlines
- No "Trusted by 10,000+ teams" social proof without real numbers
- No Lorem Ipsum — always write real content appropriate to the brief

## Brief-First Process

1. **Read the context** — what is the actual product, audience, tone? Check memory for any prior design decisions.
2. **Identify the dominant emotional register** — is this a tool for power users (dense, efficient), a consumer product (warm, inviting), a data dashboard (precise, authoritative)?
3. **Set the three dials** explicitly
4. **Name the signature element** — the one thing this design will be remembered for
5. **Design token draft** — 5 colors, 2 fonts, 1 motion curve, 1 spacing unit
6. **Layout wireframe** — ASCII or prose, NOT code yet
7. **Anti-pattern audit** — does anything in the plan look like a banned pattern? Replace it.
8. **Build**

## Design System Choices

**For enterprise/SaaS/data tools** (this dashboard qualifies):
- Use an established system OR Tailwind with strict custom tokens
- Component libraries: Radix UI primitives, shadcn/ui, Headless UI
- Never mix two component libraries

**For animations** (when MOTION_INTENSITY ≥ moderate):
- GSAP for complex orchestration, timeline-based sequences
- Motion (Framer Motion) for React component animations
- CSS `@keyframes` for simple, repeatable micro-interactions
- CSS scroll-driven animations (`animation-timeline: scroll()`) for parallax

**For icons:**
- Phosphor Icons (most versatile, multiple weights)
- Tabler Icons (1600+ clean outline icons)
- Radix Icons (minimal, great for UI chrome)
- Never: Heroicons mixed with Font Awesome mixed with custom SVGs

## Pre-Flight Checklist (90+ items — key ones)

**Contrast & Accessibility:**
- [ ] All body text ≥ 4.5:1 contrast ratio (WCAG AA)
- [ ] All interactive element text ≥ 4.5:1
- [ ] Form field borders visible at 3:1 against background
- [ ] Focus indicators visible and styled (not browser default)
- [ ] `prefers-reduced-motion` respected for all animations

**Layout & Spacing:**
- [ ] No CTA button text wraps to two lines at any viewport
- [ ] Eyebrows (small labels above headings) used in ≤ ⅓ of sections
- [ ] Card grids have consistent gap rhythm
- [ ] Section spacing uses multiples of base unit (4px or 8px)
- [ ] Mobile layout tested at 375px width

**Typography:**
- [ ] Maximum 2 typefaces on the page
- [ ] Type scale is a real scale (not arbitrary sizes)
- [ ] Line height: body 1.5–1.7, headings 1.1–1.3, data 1.2
- [ ] Letter-spacing: labels +0.05em, data values normal or -0.01em

**Motion:**
- [ ] Every animation has a justification (not just "looks cool")
- [ ] No animation loops unless it carries meaning
- [ ] Hover transitions ≤ 300ms
- [ ] Page-load animations complete within 800ms
- [ ] All animations use GPU-composited properties only (transform, opacity)

**Content:**
- [ ] Zero em-dashes on any visible surface
- [ ] No Lorem Ipsum
- [ ] All numbers formatted consistently (commas, units)
- [ ] Error states designed (not just happy path)
- [ ] Empty states designed

**Code Quality:**
- [ ] No `!important` in CSS
- [ ] No inline styles except dynamic values
- [ ] No `window.addEventListener('scroll', ...)` for animations
- [ ] Custom properties defined at `:root` for all design tokens
- [ ] Dark mode via `prefers-color-scheme` or class toggle

## Redesign Protocol

When upgrading existing UI (like this dashboard):
1. Audit existing brand tokens — what colors, fonts, spacing units are already in use?
2. Audit IA and content structure — what must stay, what can move?
3. Preserve: SEO-relevant text, data IDs used by JS, accessibility wins
4. Propose changes in order of impact: color system → typography → spacing → motion → layout
5. Never remove a working feature while redesigning its appearance

## For Analytics Dashboards Specifically

Analytics dashboards are `VISUAL_DENSITY: dense` environments. Rules:
- KPI numbers are the hero — they must be the largest, most legible thing on each card
- Labels are secondary — smaller, muted, uppercase with tracking
- Color is semantic — green = good, amber = warning, red = bad, blue = neutral info. Never decorative.
- Tables must be readable — alternating row backgrounds or strong dividers, not both
- Charts must have axis labels and a legend — never make users guess what a color means
- Loading states matter — skeleton screens, not spinners for data cards
