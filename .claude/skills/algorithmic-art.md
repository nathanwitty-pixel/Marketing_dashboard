---
name: algorithmic-art
description: Create generative art using p5.js with seeded randomness, particle systems, flow fields, noise fields, and interactive parameter exploration. Use when creating animated backgrounds, generative visual effects, canvas art, or procedural dashboard visual elements.
---

# Algorithmic Art

Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use for generative art, animated backgrounds, particle systems, flow fields, and procedural canvas effects.

## Two-Step Process

### Step 1 — Algorithmic Philosophy (.md)

Create a computational aesthetic movement before writing code. Name the movement (1-2 words), then write 4-6 paragraphs articulating:
- How it manifests through computational processes and mathematical relationships
- Noise functions and randomness patterns
- Particle behaviors and field dynamics
- Temporal evolution and system states
- Parametric variation and emergent complexity

**Philosophy must emphasize craftsmanship** — the algorithm should appear as though it took countless hours to develop, refined with care, by someone at the top of their field. Phrases like "meticulously crafted algorithm," "painstaking optimization," "master-level implementation" set the quality bar.

**Example philosophies:**
- **"Organic Turbulence"**: Chaos constrained by natural law. Flow fields driven by layered Perlin noise. Thousands of particles following vector forces, trails accumulating into organic density maps. Color from velocity and density — fast particles burn bright, slow ones fade to shadow.
- **"Quantum Harmonics"**: Particles on a grid carrying phase values that evolve through sine waves. Constructive interference creates bright nodes, destructive creates voids. Simple harmonic motion generating complex emergent mandalas.
- **"Stochastic Crystallization"**: Random processes crystallizing into order. Voronoi tessellation evolving through relaxation algorithms. Cells push apart until equilibrium. Color based on cell size, neighbor count, distance from center.

### Step 2 — p5.js Implementation (.html)

Express the philosophy through a single self-contained HTML artifact.

## Technical Requirements

**Seeded Randomness (always):**
```javascript
let seed = 12345;
randomSeed(seed);
noiseSeed(seed);
// Same seed → identical output every time
```

**Parameter Structure:**
```javascript
let params = {
  seed: 12345,
  particleCount: 2000,
  noiseScale: 0.003,
  speed: 1.5,
  trailAlpha: 8,        // 0–255, controls trail decay
  colorShift: 0.0,      // hue rotation
};
```

**Canvas Setup:**
```javascript
function setup() {
  createCanvas(1200, 1200);
  colorMode(HSB, 360, 100, 100, 255);
  background(0);
}

function draw() {
  // algorithm here — can be static (noLoop()) or animated
}
```

## Core Algorithmic Patterns

**Flow Field (Organic Turbulence):**
```javascript
class Particle {
  constructor() {
    this.pos = createVector(random(width), random(height));
    this.vel = createVector(0, 0);
    this.acc = createVector(0, 0);
    this.col = color(random(200, 260), 80, 90, 40);
  }
  update() {
    let angle = noise(this.pos.x * params.noiseScale,
                      this.pos.y * params.noiseScale,
                      frameCount * 0.003) * TWO_PI * 4;
    this.acc = p5.Vector.fromAngle(angle).mult(params.speed);
    this.vel.add(this.acc).limit(4);
    this.pos.add(this.vel);
    if (this.pos.x < 0 || this.pos.x > width ||
        this.pos.y < 0 || this.pos.y > height) {
      this.pos = createVector(random(width), random(height));
      this.vel.set(0, 0);
    }
  }
  draw() {
    stroke(this.col);
    strokeWeight(1);
    point(this.pos.x, this.pos.y);
  }
}
```

**Fade Overlay (trail effect):**
```javascript
function draw() {
  // Instead of background() — creates trails
  fill(0, 0, 0, params.trailAlpha);
  noStroke();
  rect(0, 0, width, height);
  particles.forEach(p => { p.update(); p.draw(); });
}
```

**Voronoi / Crystallization:**
```javascript
// Relaxation-based point distribution
function relaxPoints(pts, iterations) {
  for (let i = 0; i < iterations; i++) {
    pts = pts.map(p => {
      let neighbors = pts.filter(q => dist(p.x,p.y,q.x,q.y) < 80);
      let fx = 0, fy = 0;
      neighbors.forEach(q => {
        let d = dist(p.x,p.y,q.x,q.y);
        fx += (p.x - q.x) / (d * d);
        fy += (p.y - q.y) / (d * d);
      });
      return { x: constrain(p.x + fx*0.5, 0, width),
               y: constrain(p.y + fy*0.5, 0, height) };
    });
  }
  return pts;
}
```

## Interactive Artifact Structure

Every output is a single self-contained HTML file with:

**Sidebar controls:**
1. **Seed section** (always): seed display, Prev/Next/Random buttons, jump-to-seed input
2. **Parameters section**: sliders for each `params` key with real-time update
3. **Colors section** (optional): color pickers if palette is adjustable
4. **Actions**: Regenerate, Reset, Download PNG

**Minimal sidebar template:**
```html
<div id="sidebar">
  <div class="section">
    <label>Seed: <span id="seed-display">12345</span></label>
    <button onclick="prevSeed()">Prev</button>
    <button onclick="nextSeed()">Next</button>
    <button onclick="randomSeed_()">Random</button>
  </div>
  <div class="section">
    <label>Particles: <span id="count-val">2000</span></label>
    <input type="range" min="100" max="5000" value="2000"
           oninput="params.particleCount=+this.value; document.getElementById('count-val').textContent=this.value; regenerate()">
  </div>
  <div class="section">
    <button onclick="regenerate()">Regenerate</button>
    <button onclick="saveCanvas('art','png')">Download PNG</button>
  </div>
</div>
```

## For Dashboard Use

When adding generative elements to a dark dashboard:
- Use `createGraphics()` for off-screen buffer so the art doesn't block UI
- Keep `frameRate(30)` — no need for 60fps in a dashboard context
- Use `colorMode(HSB)` for smooth color cycling through dashboard accent hues
- Set canvas opacity via CSS so underlying content shows through for ambient effects
- Particle counts: 500–1500 max for dashboards (performance matters)
- Prefer `noLoop()` + static render for backgrounds (draw once, no CPU drain)
- Animated elements: only use for focal points (a section hero, not every card)

## Seeded Variation System

```javascript
let currentSeed = 12345;
function nextSeed() { currentSeed++; applyNewSeed(); }
function prevSeed() { currentSeed--; applyNewSeed(); }
function randomSeed_() { currentSeed = Math.floor(Math.random() * 99999); applyNewSeed(); }
function applyNewSeed() {
  document.getElementById('seed-display').textContent = currentSeed;
  params.seed = currentSeed;
  regenerate();
}
function regenerate() {
  randomSeed(params.seed);
  noiseSeed(params.seed);
  clear();
  setup();
}
```
