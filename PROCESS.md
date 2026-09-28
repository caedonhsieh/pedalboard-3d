# Modeling process — hero pedals for pedalboard-3d

Strategy (2026-09-28): exceptional art on the most popular pedals, procedural
boxes for the long tail. A hero model is never hand-modeled per pedal — it is
a **spec** (`specs/<id>.json`) assembled by the shared part library
(`parts.js`). Correcting a model means editing data, not geometry code.

## The pipeline: measure → spec → validate → ship

### 1. Measure

- **Dims**: manufacturer spec preferred; else `heights.json` / `pedals.json`.
  Mark the provenance in the spec. The height DB's enclosure estimates
  understate true max height by ~0.2–0.4" — note it when you use one.
- **Face photo**: PedalPlayground image, top-down. Knob centers via Kasa
  circle fit, converted through the decal UV mapping
  (`x = (u−0.5)·W`, `z = (0.5−v)·D`, v=1 at image top = back).
- **Side photo** (profile enclosures only, e.g. TS9): Wikimedia or dealer
  listing. Ground keypoints against a known dimension (usually the back-wall
  height from the manufacturer spec).
- **Boxy pedals skip all of this**: pick the enclosure preset, measure one
  knob position, done.

### 2. Spec

Write `specs/<id>.json` per `spec-schema.md`.

**The surface-sampling rule (hard requirement):** parts seat by *sampling the
enclosure profile at their z-position* — never hardcoded y values. In
`parts.js` this is `surfaceAt(decks, z)`, and `assemblePedal()` places every
knob / LED / footswitch through it. Consequence: a profile spec-edit
automatically reseats every part at the correct height. If you ever find
yourself writing a y for a deck-mounted part, stop — the spec is wrong.

Enclosure presets (`PRESETS` in parts.js, provenance documented there):

| Preset | W×D×H (mm) | Confidence |
|---|---|---|
| `mxr_standard` | 60 × 111 × 32 | high |
| `ehx_nano` | 70 × 115 × 54 | medium — individual Nano models vary, override per model |
| `ehx_xo` | 102 × 121 × 57 | medium — "XO" is not one universal enclosure |
| `boss_compact` | 73 × 129 × 59 | high |

Custom profiles are the exception (TS9 wedge), not the rule. Most pedals
on the ledger are boxes — the preset table is what makes the queue tractable.

### 3. Validate

```
open validate.html?spec=specs/<id>.json
```

All client-side. Three independent checks, fixed canonical cameras, no
auto-rotation:

- **CHECK A — spec→render placement.** Every part anchor's placed position is
  derived from the object graph (`pedalSpacePos`, world matrices) and
  compared against an *independent* interpolation of the spec done inside
  validate.html — never against the assembler's own math. **> 2 mm fails.**
- **CHECK B — render→photo.** Top render next to the spec's face art, blink
  toggle, footprint IoU. The IoU compares the render's top-down silhouette
  against the spec's nominal W×D rect — deliberately **not** against the decal
  PNG's alpha channel. Decal art legitimately contains transparency (the TS9
  decal is ~87% opaque), which capped IoU at ~87% no matter how perfect the
  model — comparing against alpha conflates art coverage with geometry, so
  the check measured the wrong thing. The bbox center/size readouts verify the
  decal art is drawn at the right scale and position; the blink test covers
  art alignment qualitatively. **IoU < 0.90 fails** (with bbox center/size
  ≤ 2 mm). The threshold itself was not weakened — the comparison was fixed
  to measure geometry instead of art transparency.
- **CHECK C — profile.** Side render with the spec profile polyline
  overlaid; max deviation of the rendered silhouette from the polyline.
  This is what would have caught the TS9's exaggerated single-slope wedge.
  **> 2.5 mm fails** (slightly looser than A: bevel rounding eats ~1 mm at
  the silhouette edge).

**The rule: no model ships without validate.html passing.** Not "passing
except" — passing.

### 4. Ship

Commit, push to `main`, wait for GitHub Pages, verify HTTP 200 on
`hero.html`, `validate.html`, `parts.js`, and the spec. Flip the ledger
entry to `hero` (below).

## Worked example: the TS9 profile correction (2026-09-28)

The first real spec-edit-not-remodel fix. Side-by-side comparison showed the
model exaggerated the wedge: sharp elbow at ~33% depth + steep straight ramp,
back only ~1.7× front height. The real pedal: rear deck ~flat for the rear
40% of depth, then a subtle smooth bend easing into a gentle straight slope,
no hard kink, back ~1.94× front.

The fix was a data edit in `specs/ts9.json` — seven profile points replacing
three, `bevel` 0.05→0.07 (rounder rear-top corner), `frontLean` 0.06 (slightly
sloped front face). Knob/switch/LED z-positions were untouched; their heights
reseated automatically via the surface-sampling rule. Then re-run
validate.html. No geometry code changed. This is the process working as
designed.

A follow-up fix (same day) corrected `profileEnclosure`'s bevel compensation:
`frontLean` had been subtracted from the front-*top* corner's pre-bevel
position, so the bevel expanded the outer surface `frontLean` (0.06") past the
nominal spec point — the rendered silhouette overshot the spec footprint and
check B's bbox size readout caught it (Δ 1.54 mm). The lean is now applied to
the front-*bottom* corner instead, so the front-top corner lands exactly on the
nominal point. Lesson: the profile is the design intent, and the builder must
be held to it — that's what check B's footprint IoU is for.

## Hero page robustness

`studioScene()` (parts.js) detects software WebGL (SwiftShader / llvmpipe —
typical in headless/test browsers) via `WEBGL_debug_renderer_info` and scales
back: pixel ratio 1, 1024px shadow maps, no PMREM environment convolution
(the biggest synchronous GPU cost on the page). Without this, the page can
block the main thread long enough for the browser to kill it as
"unresponsive" under software GL. Hardware-GL visuals are untouched. This is a
fallback path, not a quality reduction.

## Model ledger (`specs/ledger.json`)

The ledger tracks hero candidates explicitly. Statuses:

- `planned` — queued for hero modeling.
- `hero` — fully modeled: spec written **and** validate.html passing.
- `placeholder` — implicit, never listed: the other ~8,550 catalog pedals,
  rendered as procedural boxes in the main app.

Lifecycle: `planned` → (spec written per this doc → validate.html passes all
three checks) → flip to `hero` in the same ship commit.

### Priority rubric

Priority is **iconicness = cultural ubiquity + board frequency**, not sales
rank alone. A pedal every guitarist recognizes and half the boards on the
internet carry outranks a niche bestseller. Priority 1 = model first.
The current queue is a **draft for Caedon's cuts/additions** — seeded
2026-09-28, not final.

### Standing rule — board integration (future work)

The main board app will eventually read this ledger and swap hero models in
for placeholders where `status == "hero"`. That integration is **future
work — do not touch `index.html` in modeling passes.** The ledger is the
contract the future integration will read; keep it current on every ship.
