# DS-1 Model Replication Notes

How the Boss DS-1 hero model was built (2026-09-29 → 2026-10-01). This is the
playbook for replicating the process on the next pedal.

## 0. Measurement Priority (in order)

1. **Manufacturer specs** — dims, heights, official diagrams (highest confidence)
2. **Automated photo measurement** — calibrated photos, Kasa circle fit for
   knob centers, edge detection for profiles (see PROCESS.md §1)
3. **Manual annotation by Caedon** — LAST RESORT ONLY, when 1+2 fail

Manual annotation is expensive (requires his time). Exhaust automated methods
first. The DS-1 side profile required manual annotation because the beveled
enclosure silhouette couldn't be reliably auto-extracted — this should be the
exception, not the rule.

## 1. Reference Collection

Gather at minimum:
- **Top-down**: knob/label/jack layout, x/z placement
- **True side profile** (left AND right): enclosure silhouette, heights, slopes
- **Front and back**: width profile, footswitch plate, power jack
- **3/4 angles** (2+): cross-check proportions, surface transitions

Sweetwater product pages are the first stop (6–10 studio views per pedal).
Also: manufacturer pages, Reverb used listings (wear angles reveal edges).

## 2. Manual Annotation Workflow (Last Resort)

When automated measurement fails, Caedon acts as ground-truth annotator.
His hand-painted boundaries and node placements are the spec, not suggestions.
Use sparingly — this is the most expensive step in the pipeline.

### Side Profile Annotation
1. He paints a boundary map: green=treadle, yellow=recess, orange=body
2. He places nodes (A, B, C, ...) at key vertices
3. Division = white-removal silhouette ∩ his L1/L2 line segments
   - L1 = treadle/recess boundary
   - L2 = recess/body boundary
4. Knobs and jack are excluded — handled afterward as separate 3D parts
5. Simplify: body → hexagon, treadle/recess → quadrilaterals
6. **Strictly inside his painted boundaries** — never extend any outer edge
7. **He must explicitly approve the 2D profile before it goes to 3D**

### Collinearity
Projected collinear points are computed from his nodes (see
`~/workspace/your_files/ds1-reference-tags/caedon_nodes_collinear.json`).
- DEFC is one continuous straight line
- NHGI is one continuous straight line

### Transform (pixels → inches)
```
sx = (129/25.4)/721
sy = sx * (59/60.5)
x0 = 365.5
y0 = 340
x_in = (x_px - x0) * sx
y_in = (y0 - y_px) * sy
```

## 3. Spec Construction (`specs/<id>.json`)

Per `spec-schema.md`. Key DS-1 learnings:

### Enclosure: Closed Measured Polygon
For the DS-1, the enclosure uses `enc.closed: true` with the IJKLMN polygon
(points in [z, y] profile plane). This is extruded directly via
`extrudeProfile()`.

```json
"enclosure": {
  "type": "profile",
  "closed": true,
  "points": [[2.5182, 0.8449], ...],
  "color": "#ff7a1a"
}
```

### The Bevel Problem
`extrudeProfile()` applies:
1. `roundPolygon(points, 0.08, 6)` — 2D corner rounding
2. Bevel compensation: insets polygon by `bevel` (0.02)
3. `ExtrudeGeometry` with `bevelThickness: 0.02, bevelSize: 0.02`

**The problem:** The bevel/rounding causes the real mesh surface to deviate
from the nominal spec geometry. Parts positioned via `surfaceAt()` (which uses
nominal spec math) end up buried inside the mesh.

**The solution:** Offline raycasting (see §5).

### Knobs
DS-1 knobs (measured 2026-10-01 from reference photo):
- Base flange OD: 20.0mm / 0.79"
- Upper body diameter: 13.8mm / 0.54"
- Total height: 12.0mm / 0.47"

TONE/DIST: fluted (8 visible peaks, NOT 10 — count from photo, never guess).
LEVEL: smooth, no fluting, no base ring.

Base rings: 0.1" wide black annulus, innerR=0.27", 3 dots at 12/5/7 o'clock.

## 4. Treadle Decal Generation

The treadle text (OUTPUT, INPUT, Distortion, DS-1) is a baked 2048×2048
transparent PNG, generated reproducibly by `generate_treadle_decal.py`.

### Fonts
- OUTPUT/INPUT/arrows: **DejaVu Sans Bold** (contains U+2B05 ⬅)
- Distortion, DS-1: **Liberation Sans Bold** (Caedon's pick)

### Layout
Positions are pixel coordinates in the 2048×2048 canvas. Caedon directs
spacing in inches; convert via the texture-to-model mapping (measure it,
don't guess).

Current (2026-10-01):
```python
POS_OUTPUT = (85, 100)
POS_INPUT = (1450, 100)
POS_DISTORTION = (100, 400)
POS_MODEL = (1627, 750)
```

### Deployment
Bump the `?v=` query param in the spec to force cache refresh:
```json
"treadleDecal": "./textures/ds1_treadle_decal.png?v=20261001f"
```

## 5. Offline Surface Raycasting (Critical)

**Problem:** Bevel + roundPolygon → real surface ≠ nominal spec → parts bury.

**Solution:** Compute true surface Y offline, bake into spec, no runtime cost.

### Procedure
1. Build the enclosure geometry in Node using the actual `roundPolygon` and
   `extrudeProfile` logic (copy functions; they don't need DOM)
2. For each label (x, z) and knob (x, z), raycast straight down from y=10
3. Record the hit Y as `surfaceY`
4. Write `surfaceY` into `specs/<id>.json` for each label/knob
5. In `parts.js`, when `surfaceY` exists, position directly in world space
   (bypass `surfaceAt()` and deck.group)

### Script
See `/tmp/compute_surface.mjs` (template — adapt per pedal).

### In parts.js
```js
// Labels
} else if (lb.surfaceY !== undefined) {
  const { pitch } = surfaceAt(decks, lb.z);
  group.add(part);
  part.position.set(lb.x ?? 0, lb.surfaceY + 0.015, lb.z ?? 0);
  part.rotation.x = pitch;
}

// Knobs: correct Y after seat()
if (k.surfaceY !== undefined) {
  const { y: nominalY } = surfaceAt(decks, k.z);
  part.position.y = k.surfaceY - nominalY;
}

// Rings: same pattern as labels
```

## 6. Label Layering (No Float, No Occlusion)

Goal: labels and dots look flush (not floating) but never cover each other.

### The Stack (Y offsets above surface)
- Labels: `surfaceY + 0.015"`
- Rings/dots: `surfaceY + 0.016"` (0.001" above labels)

The 0.001" (0.025mm) gap is invisible to the eye but enough for the depth
buffer to resolve ordering.

### Material Settings
Both `textLabel()` and `knobBaseRing()` use:
- `transparent: true`
- `alphaTest: 0.1` — **critical**: discards transparent background pixels so
  they don't write to depth buffer and can't occlude anything
- `polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4`
- `side: THREE.DoubleSide`
- `frustumCulled = false` on the mesh

`knobBaseRing` additionally uses `depthWrite: false` and `renderOrder = 1`.

### Why Not Just polygonOffset?
Tried giving rings stronger polygonOffset (-6 vs -4) with same Y — regressed.
The combination of `depthWrite: false` + `renderOrder` + aggressive offset
caused clipping through other geometry. Physical Y separation (even 0.001")
is more predictable.

## 7. Validation

### No Trustworthy IoU Yet
Prior 0.897–0.9379 claims were INVALID (white-background HSV leak).
Target: 0.99 per element/view. Do not report complete until reached.

### Required Review Images
- Straight side
- Straight top-down
- Front three-quarter
- Side-by-side reference/render
- Outline/diff overlay (outlines, NOT colored fills)

### Regression Testing
Shared `parts.js` changes affect all pedals. After any edit, verify:
- TS9 (accepted 2026-09-29 — preserve enclosure, 0.9-scale TONE, 10 wedges)
- `hero.html` (went blank after shared changes before)
- All `baseRing` users
- Multiline labels, decals, script/bold labels

## 8. Deployment

- Repo: https://github.com/caedonhsieh/pedalboard-3d
- Live: https://caedonhsieh.github.io/pedalboard-3d/boss-ds1.html
- Deploy from `main` branch
- **Caedon does final visual check himself** — be certain the site is updated
  before telling him to look. He checks via hard-refresh on iOS.

## 9. Key Principles

1. **Stop guessing and measure.** Every value traces to a measured source.
2. **Self-validate first, human review last.** Always make a strong autonomous
   attempt to validate and improve without a human in the loop. Iterate until
   no more progress can be made (≥20 no-improvement iterations before ending
   a branch). Only then bring in human review.
3. **Manual annotation is last resort.** See §0 — exhaust specs and automated
   measurement before asking for hand annotation.
4. **Never copy specs** — derive from reference photos.
5. **Fix only the named part** — don't let fixes propagate to siblings unasked.
6. **Counts from photos, never estimated** (he caught a guessed flute count).
7. **Disclose deviations honestly** up front.
