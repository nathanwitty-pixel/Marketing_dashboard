# Sticky controls — the filter bar follows the reader

**Script:** `assets/sticky_controls.js` (CSS injected by the script). User's request, 19 Oct 2026: when the reader
reaches another chart they can change the period there, without scrolling back up.

## Use

```html
<script src="../assets/sticky_controls.js"></script>
<script>StickyControls.init({ selector: '.controls' });</script>
```

- `init({ selector, within, watch, background })` — once per bar (call it again for more bars).
  `selector` = CSS selector (every match becomes a bar) or an element. **`within`** = the section that bounds the bar
  (CSS selector of its closest ancestor, or an element): the bar follows the reader only while that section is on
  screen, then lets go at the section's end; no `within` = a **page-wide** bar that follows the whole page.
  **`watch: true`** = bars the page builds or rebuilds later (script-rendered filter bars, templates per offer) are
  pinned as they appear (MutationObserver). `background` = pinned background colour (default near-black).
- `initSections(['control-id', …], '.card')` — pins the **header row** of each card holding one of those controls
  (the card's direct child around the control), inside that card. `headerOf(el, '.card')` returns `[row, card]`.
- `update()` re-measures (it also runs on scroll, resize, clicks and any page size change).

## Behaviour

- **Pinned with a transform**, not CSS `position: sticky`: sticky only pins inside the bar's own parent box (most bars
  sit in a short header block), and in the Streamlit dashboard each page's iframe is stretched to its full height
  (`streamlit_app.py`), so the **parent** document scrolls and nothing inside the page sticks.
- **Standalone** (the page scrolls itself): the bar is lifted to the top of the window as soon as its own place
  scrolls past the top.
- **Embedded** (Streamlit): the same logic as `assets/page_sidebar.js` (`embedHost`) — measured against the parent's
  viewport and kept just **below the parent's top bar** (`.tn-bar`); listens to scrolls in the parent document.
- **Pinned look:** solid background (`--sc-bg`, default near-black), bottom shadow, slight blur, and a **compact** mode
  (smaller top / bottom padding). The bar keeps its own width inside the content column, so it never covers the page
  sidebar.
- **No layout jump:** a transform doesn't move anything else; the compact bar's lost height is reserved as bottom
  margin, so the content under it stays put.
- **Several bars at once stack** in page order, each just below the one above it — counting only the part of a bar
  actually in the top zone (a section bar being pushed out at its section's end frees its space).
- **Re-measured on any page size change** (ResizeObserver), so charts that render after load don't leave the bar out
  of place; bars are excluded from scroll anchoring (`overflow-anchor: none`) so the browser doesn't nudge the page.
- **Un-pins** by itself when the bar's own place scrolls back into view (transform 0), and never travels past the end
  of the page. Print: no transform, no shadow.

## Pages (19 Oct 2026)

Checked results per page: the table in `notes/STICKY_CONTROLS_PROGRESS.md`. Shop Stock Levels was taken off again (19 Oct 2026, user's call: its bar stays static).


| Page | What follows the reader | Bound |
|---|---|---|
| Product Performance | Market, Period, Share by (`.controls`) | page |
| Bags on offer | Period (`#boo-ctl`) | page |
| Self-made combos | 📞 call-back period bar (page) + Type switch | Type: the Kenya view |
| New Products | header rows of Sales by Shop, Sold vs Target, Runway, Top 10, Colour Movement | each card |
| Posting Yields | Segment, Period, Group, Sort rows (alignment, dead stock, region cards; KE, Sinza, Uganda) | each card |
| Shops Efficiency | Shop, Category, Bag type filters of every Stocks Remaining table (`watch`) | each table |
| Timed Offers | Sort and Group by of every offer's panels (`.to-ctl`, `watch`) | each panel |
| Offer Picking | Seasonality bag search (`.se-ctl`) | its card |
| Monthly Report | New Products Sort | its section |
| History | New Products Sort of the chosen month (`.sortbar`, `watch`) | its section |

## Checks

`notes/sticky_test/` — `run.py <page> <selector> [--at SEL] [--set SEL=VALUE] [--click SEL --read SEL]`, all pages: `run_all.py`: (i) **standalone** = a probe copy of the page scrolled to 3,000 px,
reports the bar's top (must be 0–8 px); (ii) **embedded** = a harness page with a fixed 56 px `.tn-bar` and the page in
a srcdoc iframe sized to its full height (local scripts inlined, like Streamlit), parent scrolled 3,000 px, reports
the bar's top in the parent's viewport (must be 56–72 px); plus JS errors (must be none).
