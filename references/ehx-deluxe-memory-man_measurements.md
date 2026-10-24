# EHX Deluxe Memory Man — measurements

Slug: `ehx-deluxe-memory-man`. Form built: **current XO / reissue
Deluxe Memory Man** (EHX product page `deluxe-memory-man`, UPC
683274010724, released 2008, still listed). This is the silver
die-cast box with six knobs in one row. It is **not** the vintage
1970s–2008 big-box sheet-metal Memory Man, not the Nano Deluxe
Memory Man (70×115 mm nano box), and not the 550-TT / 1100-TT tap-tempo
variants (same 5.75×4.75 in chassis family but extra tap switch,
subdivision and expression controls that this base model does not have).

## References (guide Step 1)

All five views are the exact XO pedal from the manufacturer gallery
(`ehx.com/products/deluxe-memory-man`), fetched with
`scripts/fetch_views.py --backend manual`. Each `.jpg` has a matching
`.META.txt` (source URL, retrieved via that script).

| View | File (px) | What it shows |
|---|---|---|
| Beauty / hero (cabled, lit bypass LED) | `references/ehx-deluxe-memory-man_hero34.jpg` (1500×1000) | Straight-on face with cables in the side jacks; confirms jack sides and LED colours under power |
| Top-down face (primary layout) | `references/ehx-deluxe-memory-man_front.jpg` (1000×1000) | Orthographic face on white: 6-knob row, both red LEDs, footswitch, all print, silver/black wedge. Primary homography source. Note: EHX names this file `DMM_Front.jpg`; geometrically it is the top-down view (back/knob edge at image top) |
| Left wall | `references/ehx-deluxe-memory-man_side-left.jpg` (1000×1000) | Left side wall: two 1/4 in jacks, one back knob (left) and footswitch (right) silhouetted above the deck, two red LED domes between them |
| Right wall | `references/ehx-deluxe-memory-man_side-right.jpg` (1000×1000) | Right side wall: single INPUT jack, footswitch (left) and back knob (right) — mirror orientation of the left view |
| Back / knob edge | `references/ehx-deluxe-memory-man_top.jpg` (1000×1000) | Back wall head-on: six knob backs in a row, chrome footswitch post between knobs 3–4, square 24 V power socket centred in the wall. EHX names this `DMM_Top.jpg`; geometrically it is the back edge |

≥4 exact views of the chosen form: satisfied (5). No sibling-model
photos were used for geometry.

## Published dimensions (anchor) — with conflicts flagged

- **Adopted W×D: 5.75 × 4.75 in.** EHX official spec (product page and
  `data/spec_sheets_staging.json`, verified): "Dimensions (in)
  5.75 x 4.75 x 2.5", UPC 683274010724. Retailer corroboration:
  Reverb/D​rumSetSupply/ProMusic listings repeat 5.75 x 4.75 x 2.5.
- **Axis conflict — resolved by photo aspect.** `spec_sheets_staging`
  maps the EHX sequence to w=4.75, d=5.75 (portrait). The orthographic
  face photo disproves that mapping: pedal bounding box
  866×714 px, ratio 1.213, matches 5.75/4.75 = 1.211, not
  4.75/5.75 = 0.826. The first EHX number is therefore the left–right
  width. Spec uses `w=5.75, d=4.75`. The staging W/D labels are
  transposed for this pedal (its mm pair 120.7×146.1 inherits the
  same transposition; 146.1 mm = 5.75 in is the width).
  A Specialty Traders listing prints "4.75 (w) x 5.75 (l)" beside
  "146 (w) x 121 (l) mm" — internally inconsistent (146 mm ≠ 4.75 in)
  and rejected on the same photo evidence.
- **Height conflict — bare vs overall.** Published 2.5 in is the
  overall height. Calibrated side/back photos (below) give bare
  enclosure **1.68 in**, knob top 0.65 in above the deck, rubber feet
  ≈0.10 in: 1.68+0.65+0.10 ≈ 2.43 in, within photo tolerance of
  2.5 in. Spec `h` is the bare enclosure (1.68 in) per schema;
  2.5 in is recorded here as overall, not used as `h`.
- **Rejected heights.** `data/heights.json` "Deluxe Memory Man
  (Big Box)" 1.97 in cites the 90s big-box version (different form,
  not this XO). Its "Deluxe Memory Man XO" entry has no height
  (PedalPlayground footprint 6.07×4.75 in includes jack protrusion
  and is not used). Nano 2.1 in belongs to the Nano model.
- Conversions: all spec values in inches (mm÷25.4 where needed).

## Enclosure profile

**Flat box, not sloped.** Both side views and the back view show a
constant-height deck: silver top edge horizontal, no back-to-front
slope (contrast the Big Muff Pi's measured 2.16→1.37 in single slope
— that pattern does not transfer to this form despite the shared
multi-knob row). Spec therefore uses `enclosure.type: "box"` with
the published footprint and measured bare height; there is no
profile polyline. Check C compares the side silhouette against the
flat spec height `h`.

Calibration (per-photo scale from the known footprint):

| Photo | Scale reference | px/in | Enclosure height |
|---|---|---|---|
| side-left | depth 722 px = 4.75 in | 150.3 (width 714 px at deck mid-height) | silver rows 403–656 = 254 px → **1.69 in** |
| top (back) | width 870 px = 5.75 in | 151.3 | silver rows 377–630 = 254 px → **1.68 in** |
| side-right | depth 711 px = 4.75 in | 149.7 | corroborates flat top; silver-row count truncated by foot shadow, not used for H |

Adopted bare `h = 1.68 in` (mean of the two clean views). Knob top:
dark-silhouette top y=306 (side-left) vs deck top 403 → 97 px =
**0.65 in above deck**; back view gives 0.65 in identically.
Footswitch post height above deck in side views ≈0.55 in (chrome
post + nut, corroborative only; the library `round` footswitch is
0.325 in to the plunger top and is not rescaled).

Construction: one silver-grey painted die-cast box; the black field
is print, not a separate plate. Modelled as a silver `box`
enclosure with the black wedge and large wordmarks in the top decal
(`textures/ehx-deluxe-memory-man-decal.png`), so side walls stay
silver as photographed.

## Top layout — two views per position where possible

Coordinates: inches, origin at footprint centre, back (knob edge)
= −z, front (footswitch edge) = +z. Face-photo homography is a
direct px→inch map (orthographic on white, no perspective fit
needed): bbox x 69–935 px = 5.75 in (150.6 px/in), y 146–860 px =
4.75 in (150.3 px/in); `x=(px−502)/150.6`, `z=(py−503)/150.3`.

### Knobs (6, one row, measured in face + back views)

Face view: the three right knobs sit on silver and segment cleanly
(dark-blob centroids, 100×100 px ≈ 0.66 in dia). The three left
knobs merge with the black wedge in a threshold mask, so their
centres come from the even-spacing fit corroborated by the back
view (six knob silhouettes across the width, outer centres at
pedal x ≈ −2.30 / +2.15 before perspective allowance). The row is
evenly spaced and symmetric (measured right-half spacings
0.896/0.912 in, mean 0.904 in; fitted centres are symmetric about 0
within 0.01 in):

| Knob (left→right in top view) | x (in) | z (in) | Source views |
|---|---|---|---|
| BLEND | −2.26 | −1.41 | Face (fit) + back silhouette |
| LEVEL | −1.36 | −1.41 | Face (fit) + back silhouette |
| FEEDBACK | −0.45 | −1.41 | Face (fit) + back silhouette |
| CHRS/VIBR | +0.46 | −1.41 | Face centroid (570.7, 289.2 px) + back |
| DEPTH | +1.37 | −1.41 | Face centroid (708.1, 291.3 px) + back |
| DELAY | +2.26 | −1.41 | Face centroid (842.9, 291.2 px) + back |

- Knob diameter **0.66 in** (100 px / 150.6), height **0.65 in**
  above deck (side views, above). Nearest library knob is `ehx`
  (hockey puck, 1.00 in bottom dia, 0.62 in tall): spec uses
  `diaScale 0.68, scale 1.05` (≈0.68 in dia, 0.65 in tall). No tick
  ring on the real pedal (`tickRing: false`).
- Pointer angles (`rot`, from the face photo): five pointers point
  to the back (−z, `rot 0`). CHRS/VIBR points front-left
  (≈7–8 o'clock): `rot 2.35` (135° from −z, at the hero drag clamp;
  photo-derived, ±0.15 rad).

### LEDs (2 — read this before the spec)

The real pedal has **two** red domes. The shared spec schema and
`assemblePedal()` support exactly one `led`, so the spec's `led`
is the bypass LED (the one the footswitch toggles); the overload
LED is staged by the hero page as an extra `led()` part (see the
build report's shared-changes list — library support for a second
spec LED is the clean fix).

| LED | x (in) | z (in) | Source views |
|---|---|---|---|
| OVERLOAD (red, under LEVEL) | −1.35 | −0.54 | Face red-blob centroid (298.6, 420.1 px), 235 px; side views: rear red dome between knob and footswitch |
| Bypass/status (red, in the MAN wordmark) | −0.01 | +0.79 | Face red-blob centroid (500.8, 620.0 px), 271 px; side views: front red dome; lit orange in the cabled beauty view |

Both domes are 3 mm-class red lenses on black bezels (`led()`),
≈0.14 in above deck including bezel (side silhouette, provisional).

### Footswitch

Round chrome stomp, centred: face bright-chrome centroid
(501.1, 743.4 px) → **x −0.01, z +1.62**; bbox 448–546 × 690–784 px
(hex nut ≈0.65 in across, library washer/nut/plunger stack is the
same construction at 0.54/0.44/0.40 in — not rescaled). Side views
corroborate: post silhouetted at the front end of the depth,
opposite the knob row. Spec `footswitch {style round, x 0, z 1.62}`
(x centred to 0.00; −0.01 is inside photo tolerance).

### Jacks and power (side walls + back wall, two views each)

Jack height (wall): side-view hole centroid y=523 px, deck bottom
656 px, scale 150.3 → **y 0.89 in** above the base (all three audio
jacks and the power socket share this height within 0.02 in; power
centroid in the back view: (630−495)/151.3 = 0.89 in).

| Jack | Wall | z (in) or x (in) | View 1 (side) | View 2 (face edge tabs / back) |
|---|---|---|---|---|
| DIRECT OUT | left | z 0.00 | side-left dark-hole centre x 489 px, enclosure 128–841 px → z +0.03 | Face left-edge chrome tab y 499.5 px → z −0.02 |
| EFFECT OUT | left | z +0.79 | side-left centre x 605.5 px → z +0.81 | Face left tab y 620.0 px → z +0.78 |
| INPUT | right | z +0.80 | side-right centre x 391 px (mirrored view) → z +0.83 | Face right tab y 620.5 px → z +0.78 |
| 24 V power | back | x +0.01 | back-view square socket centroid (500.5, 495.1 px) → x +0.01, y 0.89 | Face top edge "24V" print centred above the socket; beauty view cable exits the back centre |

Two-view agreement ≤0.05 in (≈1.2 mm) on every jack; spec rounds to
0.00 / 0.79 / 0.80. Left = outputs, right = input, confirmed by the
edge print (DIRECT OUT / EFFECT OUT left, INPUT right), not habit.
Power is a square black bezel with round barrel (`boss-square`
library style matches the photographed square plate; the barrel is
24 V on this model — print only, no geometry change).

### Screws

No deck screws are visible on the face (the box is screwed from
below). Spec has no `screws` — adding face screws would invent
hardware.

## Colours (sampled, lit non-specular patches)

- Silver enclosure: `#d3d2d0` (211,210,208) top centre of the face
  photo; side wall in shadow `#a5a6a0`. Spec/decal ground `#cbcbc9`
  (between the two; the powder-coat material darkens it under
  studio light to match the side reading).
- Black print field: `#191919`–`#1c1c1c` (face photo wedge patches).
- Print red (DELUXE / Echo): ≈`#d8232a` class (same EHX red as the
  Big Muff wordmark; sampled hue from the DELUXE block, value
  compressed by JPEG — decal uses `#e30613` with white outline as
  photographed).
- Knobs: black puck, white pointer line. LEDs: red domes.

## Print inventory (every word on the pedal, face photo)

Top face, back→front:

- Back edge centre: `24V` + centre-negative polarity symbol (black,
  small, above the power socket). Vector label in spec.
- Knob row labels (directly in front of each knob, z −0.86):
  `BLEND`, `LEVEL`, `FEEDBACK` — white caps (they sit on the black
  wedge); `CHRS/VIBR`, `DEPTH`, `DELAY` — black caps (on silver).
  All bold sans, untracked (`spaced: false`, width sized to avoid
  clipping). Vector labels in spec with per-label colour.
- `OVERLOAD` (white caps) right of the overload LED, z −0.54.
  Vector label in spec.
- Diagonal red italic: `Echo/Chorus/Vibrato` along the wedge edge,
  sloping down left→right (≈23° in face view), on the silver just
  above the black. In the decal (a rotated text label cannot follow
  the edge cleanly at this length).
- Centre wordmarks (in the decal; display letterforms the vector
  label font cannot reproduce): `DELUXE` red block with white
  outline; `MEMORY` large white stencil-style caps; `MAN` same
  style below it. Bypass LED sits in the counter space right of
  `MAN`.
- Left edge, vertical (reading bottom→top in face view):
  `DIRECT OUT` (back half, z 0.00) and `EFFECT OUT` (front half,
  z +0.79), white caps. Vector labels in spec, `rot 1.5708`.
- Right edge, vertical: `INPUT` (z +0.80), black caps. Vector
  label in spec, `rot 1.5708`.
- Front-right of the black field: `electro-harmonix` white script
  with `NEW YORK CITY, USA` white caps beneath it. In the decal
  (script lettering).

Orientation note: image top = pedal back (−z) in every face
measurement above; the decal canvas follows the same convention
(v=1 at the back edge in `applyDecal`).

## Provisional / single-view flags

- Left-three knob x positions: spacing-fit from the measured right
  three plus back-view silhouettes (two views, but indirect on the
  left) — provisional to ≈±0.05 in.
- CHRS/VIBR pointer angle: single face view, ±0.15 rad.
- Jack z positions: two views each, ≤1.2 mm cross-view spread —
  not provisional beyond that rounding.
- LED dome height and footswitch post height: side-silhouette
  estimates, corroborative only (library parts unscaled).
