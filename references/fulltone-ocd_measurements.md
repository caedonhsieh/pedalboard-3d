# Fulltone OCD — measurements

Slug: `fulltone-ocd`. Exact model: **Fulltone OCD V2** ("final" version,
2017–present). Not V1.7 or earlier — see version evidence below. Three
knobs (Volume / Drive / Tone), HP/LP mini-toggle, blue LED, round 3PDT
stomp, side audio jacks, side DC jack. Cream/off-white custom box.

## Version: V2 (state this everywhere)

V1.7 vs V2 differ in ways that are visible in the references, so the
version is decidable from the photos, not a guess:

| Trait | V1.7 (pre-2017) | V2 (2017– ) | These refs |
|---|---|---|---|
| Under-footswitch print | `Fulltone` only | `Fulltone` + `Built in the USA` | **V2** (front, topdown, fronttop) |
| Side jack position | toward the bottom (front) of the sides | exactly halfway along the sides | **V2** (jacks at z ≈ 0, both side views) |
| OCD wordmark | larger | slightly smaller | consistent with V2 |
| Construction | hand-wired, jacks off-board | board-mounted, output buffer + internal true/Enhanced Bypass switch | not visible externally |

Sources: Legendary Tones V1.7-vs-V2 comparison (2017-07-21),
Fulltone V2 dealer copy (Reverb/Loopersparadise listings quoting
Fulltone), and the Sweetwater OCD page, whose version selector labels
the current pedal "v2 Standard" (item `OCD`). All eight views below are
that V2 pedal. Circuit differences (buffer, bypass) have no geometry;
the geometry differences (jack z, print) are modelled as V2.

## References (guide Step 1)

All fetched 2026-10-24 with `scripts/fetch_views.py` (manual backend);
each `.jpg` has a matching `.META.txt` with its source URL.

| View | File | Source |
|---|---|---|
| Front elevation (top face head-on) | `fulltone-ocd_front.jpg` (750x1222) | Sweetwater main image, item OCD (v2) |
| True top-down | `fulltone-ocd_topdown.jpg` (350x567, PNG data) | PedalPlayground `fulltone-ocd-v2.png` |
| Right wall (Input) | `fulltone-ocd_side-input.jpg` (750x353) | Sweetwater `750-OCD_detail1.jpg` |
| Left wall (Output + DC) | `fulltone-ocd_side-output.jpg` (750x349) | Sweetwater `750-OCD_detail2.jpg` |
| 3/4 left-front | `fulltone-ocd_hero34-left.jpg` (750x689) | Sweetwater `750-OCD_detail3.jpg` |
| Front-top elevation | `fulltone-ocd_fronttop.jpg` (514x750) | Sweetwater `750-OCD_detail4.jpg` |
| 3/4 right-front | `fulltone-ocd_hero34-right.jpg` (750x671) | Sweetwater `750-OCD_detail5.jpg` |
| Back wall | `fulltone-ocd_back.jpg` (750x576) | Sweetwater `750-OCD_detail6.jpg` |

Eight views of the exact pedal (top-down, front, both sides, back, two
3/4s): satisfied. Watermarks on the Sweetwater closeups sit over the
lower wall; no measurement is taken from a watermarked patch.

## Published dimensions (anchor) — and the height trap

- Sweetwater-style retailer spec (corroborated by Reverb spec tables):
  **2.5 (W) x 4.5 (D) x 2.1 (H) in**. Staging
  (`data/spec_sheets_staging.json`, Star's Music): 60 x 115 x 55 mm
  = 2.36 x 4.53 x 2.17 in. Fulltone publishes no dims (manual is
  electrical only).
- The 2.1–2.17 in height is **overall, knobs included** — the same trap
  the MXR preset notes flag. Photo calibration below resolves the bare
  enclosure at **1.39 in**; knob tops add ~0.61 in, giving ~2.0 in
  overall, which corroborates the published 2.1 in as an overall figure.
  Spec `dims.h` is the bare enclosure (schema definition), so it uses
  the measured 1.39 in, not 2.1 in.

## Photo calibration

- `topdown` is orthographic: enclosure cream spans x 23..325 px
  (W = 302 px), y 0..563 px (D = 563 px). With D = 4.53 in (115 mm
  staging, corroborated by the 4.5 in retailer figure): 124 px/in,
  so W = 302/124 = **2.43 in**. D/W ratio 1.864.
- `front` (mild perspective, ~264 px/in at the face): enclosure
  653 px wide, 1208 px tall (depth). D/W = 1.850 — agrees with the
  top-down ratio within perspective error.
- Side views: wall spans 743 px for D = 4.53 in → 164 px/in. Deck top
  edge y ≈ 115, base y ≈ 343 → bare wall height 228 px = **1.39 in**.
  Back view agrees (W/H ≈ 1.85 at W 2.43 → H ≈ 1.31–1.39; its top
  edge is blown out, so the side value is adopted).
- Adopted spec dims: **W 2.43 x D 4.53 x H 1.39 in** (bare enclosure).
  Published W 2.5 in is within 0.07 in (likely rounded/overall); the
  measured 2.43 in is used and flagged here.

## Enclosure

Flat-top cream box, vertical walls, small corner radius; the top face
is one flat deck (no slope), so `type: "box"` with measured dims —
no profile. Colour: lit non-specular cream sampled at front
(500..650, 1100..1200) `#e0d8c3` and topdown `#d8d2b1`; spec uses
`#e8dec4` (warm off-white between the two lightings). Print is black.
Front wall carries `OCD` / `Fulltone` print; back wall is blank
(`back` view). Four knurled side thumbscrews (two per side wall, low,
near the front/back ends) hold the base — see Open/provisional.

## Top layout (two views each: topdown + front; back = -z)

Scale 124 px/in (topdown) / ~264 px/in (front); knob centres from dark-
blob centroids, symmetrised where the pair disagrees (white pointer
line splits each blob asymmetrically by up to 0.07 in).

| Part | x (in) | z (in) | Source |
|---|---|---|---|
| VOLUME knob | -0.65 | -1.48 | topdown (-0.58,-1.44) + front (-0.66,-1.54) |
| DRIVE knob | +0.65 | -1.48 | topdown (+0.71,-1.45) + front (+0.66,-1.52) |
| TONE knob | 0.00 | -0.63 | topdown (+0.07,-0.60) + front (0.00,-0.67) |
| HP/LP toggle | 0.00 | -1.70 | topdown toggle centroid (174,70)px + front |
| LED (blue) | 0.00 | -1.47 | blue-mask centroid: topdown (173,99)px, front (372,212)px |
| Footswitch | 0.00 | +1.15 | front washer centre + topdown chrome circle (±0.05) |
| OCD wordmark | 0.00 | +0.24 | letter blobs y 264..357px (1.85 wide x 0.76 tall) |

- Knob diameter 92 px (topdown) / 204 px (front) → **0.75 in** black
  fluted Davies-style knobs, white pointer line. Pointers at 12 o'clock
  in `front` (`rot: 0`); the topdown unit happens to sit at ~7:30.
  Knob height above deck ~0.61 in (side views, knob top vs deck edge);
  `parts.js` mxr knob (0.545 in) at diaScale 0.82 is the closest shared
  part (0.75/0.92).
- HP/LP positions in both views: toggle bat leans toward the back
  (HP) in `front`, `topdown`, and `back` (bat visible above the deck
  between the knobs). HP label above the toggle (z ≈ -2.02), LP below
  it (z ≈ -1.60, left of the LED). The toggle is a separate control —
  its positions are recorded here and in the hero page; `parts.js` has
  no toggle builder (shared need, see spec notes).
- LED is **blue** when on (both lit photos). `parts.js` `led()` is red;
  the hero page re-colours the lens/emissive locally (shared need:
  LED colour parameter).
- No deck screws visible; none modelled.

## Side / back walls

| Part | Position | Source |
|---|---|---|
| INPUT jack (right wall) | z 0.00, y 0.45 | bore centroid (377,269)px, side-input |
| OUTPUT jack (left wall) | z 0.00, y 0.45 | bore centroid (376,269)px, side-output |
| 9-18V DC jack (left wall) | z +0.85, y 0.44 | black bore centroid (512,271)px, side-output; corroborated in hero34-left |
| Side thumbscrews (x4) | z ≈ ±1.74, y ≈ 0.26, both walls | knurled discs in both side views (provisional ±0.06, watermark-adjacent) |

Jack y: bore 74 px above the base at 164 px/in = 0.45 in (below mid-
wall — V2 jacks are centred along z, not raised in y). DC is on the
**left (Output) side wall**, forward of the Output jack — not on the
back wall. `parts.js` `powerJack` only mounts on the back wall, so the
spec carries `powerJack: null` and the hero page stages the DC barrel
locally on the left wall (shared need: side-wall power support).
Right = INPUT, left = OUTPUT, confirmed by the wall print, not habit.

## Print inventory (case as printed)

Top face (back→front): `Volume`, `HP`, `Drive` (labels above the back
row); `LP` below the toggle; curved rotation arrows around all three
knobs (arc + arrowhead, lower-right); `Tone` right of the Tone knob;
`OCD` wordmark with `®`; `Fulltone` script with `®`; `Built in the
USA` beneath it. Front wall: `OCD`, `Fulltone`. Right wall: `Input`
above the jack. Left wall: `Output` above the jack, `9-18VDC` with
`+ —(•— -` polarity diagram by the DC jack (text oriented to read
from the back edge). Back wall: blank. Side print is wall-mounted;
the shared library has no side-wall labels, so the hero page stages
wall print locally (shared need, with the ProCo front/back precedent).

Fonts: knob/HP/LP labels are a casual hand-style sans (vector
`textLabel` bold approximates); `OCD` and `Fulltone` are custom
letterforms — drawn into `textures/fulltone-ocd-decal.png` with the
knob arrows, as on the Klon/Rat heroes. `Volume`/`Drive`/`Tone`/`HP`/
`LP` stay vector labels so they stay crisp.

## Open / provisional

- Thumbscrew z (±1.74) is single-view-per-side to ±0.06 in; the discs
  are partly watermark-adjacent in the closeups. They are staged in
  the hero page only (no spec field exists for side hardware).
- W 2.43 in is photo-measured (published 2.36–2.5 in bracket it);
  bare H 1.39 in is photo-measured (published heights are overall).
- Footswitch z +1.15 is ±0.05 (chrome highlights centroid differently
  per view); knob x ±0.65 is symmetrised from ±0.58..0.71 readings.
