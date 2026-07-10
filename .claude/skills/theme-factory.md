---
name: theme-factory
description: Toolkit for styling artifacts with a theme. 10 pre-set themes with colors/fonts that can be applied to any artifact, or generate a custom theme on-the-fly. Use for slides, docs, HTML dashboards, landing pages.
---

# Theme Factory Skill

This skill provides a curated collection of professional font and color themes, each with carefully selected color palettes and font pairings. Once a theme is chosen, it can be applied to any artifact.

## Purpose

To apply consistent, professional styling to any artifact. Each theme includes:
- A cohesive color palette with hex codes
- Complementary font pairings for headers and body text
- A distinct visual identity suitable for different contexts and audiences

## Usage Instructions

1. **Show theme options**: Present the 10 available themes with brief descriptions
2. **Ask for their choice**: Ask which theme to apply
3. **Wait for selection**: Get explicit confirmation about the chosen theme
4. **Apply the theme**: Apply the selected theme's colors and fonts consistently throughout

## Themes Available

1. **Ocean Depths** — Professional and calming maritime theme; deep navy, teal accents, clean whites
2. **Sunset Boulevard** — Warm and vibrant sunset colors; coral, amber, deep purple
3. **Forest Canopy** — Natural and grounded earth tones; deep greens, warm browns, cream
4. **Modern Minimalist** — Clean and contemporary grayscale; stark whites, charcoal, single accent
5. **Golden Hour** — Rich and warm autumnal palette; golds, burnt orange, warm shadow
6. **Arctic Frost** — Cool and crisp winter-inspired theme; ice blue, silver, pure white
7. **Desert Rose** — Soft and sophisticated dusty tones; rose, sand, muted sage
8. **Tech Innovation** — Bold and modern tech aesthetic; electric blue, dark background, sharp contrast
9. **Botanical Garden** — Fresh and organic garden colors; leafy greens, soft yellows, natural white
10. **Midnight Galaxy** — Dramatic and cosmic deep tones; deep purple, starlight silver, void black

## Application Process

After a preferred theme is selected:
1. Apply the specified colors and fonts consistently throughout the artifact
2. Ensure proper contrast and readability (WCAG AA minimum)
3. Maintain the theme's visual identity across all sections
4. Use CSS custom properties (variables) so the theme is easy to swap later

## Create a Custom Theme

When none of the existing themes fit, generate a custom theme:
- Based on provided inputs (brand colors, mood, audience), choose appropriate colors and fonts
- Give the theme a descriptive name
- Define: primary, secondary, accent, background, surface, text, and muted hex values
- Define: display font (headers), body font, and mono font (if needed)
- Show the theme for review before applying it

## For Dark Dashboards

When applying to a dark analytics dashboard like this one:
- Use the artifact's existing card colors (green/amber/blue) as the accent system
- Generate a dark surface palette: background ~#0f1117, card surface ~#1e2235, border ~#2d3148
- Ensure all card values pass 4.5:1 contrast against their card background
- Typography: a clean sans-serif (Inter, DM Sans, or Geist) for data readability
