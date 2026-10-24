# MXR Dyna Comp (M102) — measurements

Slug: `mxr-dyna-comp`. Exact model: MXR M102 Dyna Comp Compressor
(current block-logo version, red powder coat, OUTPUT + SENSITIVITY
knobs). Not the Script CSP102SL or Dyna Comp Deluxe M228.

## References (guide Step 1)

All Dunlop (jimdunlop.com, product 591) studio views of the exact
pedal, fetched via `scripts/fetch_views.py` (manual backend).
1280x1280 JPEG each (right/bottom re-encoded from WebP to JPEG).

| View | File | Dunlop view | Shows |
|---|---|---|---|
| Top-down | `references/mxr-dyna-comp_main.jpg` | MAIN | Knob/label/LED/switch x-z, side jacks |
| Back elevation | `references/mxr-dyna-comp_top.jpg` | TOPP | Knob height, back wall, switch behind |
| Left side | `references/mxr-dyna-comp_left.jpg` | LEFT | OUTPUT jack, profile, LED/switch |
| Right side | `references/mxr-dyna-comp_right.jpg` | RGHT | INPUT + side power jack, CE sticker |
| Front elevation | `references/mxr-dyna-comp_bottom.jpg` | BOTT | Front wall, switch foreground |
| Bottom | `references/mxr-dyna-comp_back.jpg` | BACK | Base plate, 4 screws (not modelled) |

Six views of the exact pedal: satisfied (top-down, both sides,
front, back, bottom). File suffixes keep the Dunlop view names;
this table is the mapping to pedal views.

## Published dimensions (anchor)

- Enclosure preset `mxr_standard` in `parts.js` PRESETS:
  **60 x 111 x 32 mm = 2.362 x 4.370 x 1.260 in** (W x D x H, bare
  enclosure, high confidence; Perfect Circuit / Session.de /
  Thomann Phase-90-class listings). Dyna Comp uses the same MXR
  standard die-cast box as the Phase 90 (M101).
- Spec `dims` therefore: w 2.362, d 4.370, h 1.260 in, source
  `preset mxr_standard`. Retail overall heights (~55 mm) include
  knobs/switch and are not used. Amazon package dims are the
  shipping box and are ignored.

## Enclosure

Plain box (`enclosure.type: "box"`, preset `mxr_standard`,
edgeRadius 0.06 as Phase 90). Side elevations (left/right) show a
flat deck at full height with a thin base-plate seam at the
bottom; no wedge or treadle. No profile points needed.

## Top-down calibration (mxr-dyna-comp_main.jpg)

- Red-mask enclosure bbox: x 351-928 px, y 110-1169 px for
  2.362 x 4.370 in -> 244 px/in (x), 242 px/in (z); 1% agreement.
  Image top = back (-z). Side-jack barrels protrude past the red
  bbox and are excluded from the width.
- Knob black-blob bboxes: left centre (519, 329) px, right
  (781, 329) px, diameter ~280 px (1.15 in incl. skirt flare and
  shadow; the `mxr` builder body is 0.92 in dia — see Open).

| Part | x (in) | z (in) | Source (2 views) |
|---|---|---|---|
| OUTPUT knob | -0.54 | -1.30 | main (centroid -0.49, symmetrised) + top elevation (left knob) |
| SENSITIVITY knob | +0.54 | -1.30 | main (centroid +0.60, symmetrised) + top elevation (right knob) |
| LED (red) | 0.00 | +0.40 | main (0.01, +0.40) + left side (between logo and switch) |
| Footswitch (round) | 0.00 | +0.94 | main (0.03, +0.94) + left/right sides |
| OUTPUT jack (left wall) | left | -0.20 | main (barrel at z ~-0.26) + left side (z ~-0.14) |
| INPUT jack (right wall) | right | -0.20 | main + right side (z ~-0.19) |
| Side power jack (right wall) | right | +0.42 | right side only (provisional, see below) |

Knob x symmetrised to ±0.54 in: raw centroids (-0.49 / +0.60)
differ by specular highlights eating the black masks; the two
knobs are mirror-placed about the centreline in main + top
elevation. Jack z averaged from top-down and side views
(agreement ~0.1 in). Jack wall height y 0.60 in from the side
views (jack centre at 44% of the 1.26 in wall height).

Side power jack: on the **right wall** (same wall as INPUT),
front of the INPUT jack — black 9V barrel with centre pin,
clearly in `mxr-dyna-comp_right.jpg`; the left wall carries the
OUTPUT jack alone. `parts.js` `powerJack()` only mounts on the
back wall, so the spec carries the proposed `sidePowerJack`
field (Dunlop GCB95 precedent) and the hero page renders it;
`powerJack` stays null. Single-view position: provisional
(±0.1 in).

Knob pointers: both at 12 o'clock (white line vertical) in
main; spec `rot: 0` for both. No tick rings on the real pedal
(`tickRing: false`).

## Colours

- Enclosure red: lit non-specular patches on main sampled
  #f12b3b (450,600) and #ef2335 (800,1000). Spec uses #e8262f
  (ACES tone mapping darkens ~10%; Phase 90 orange precedent).
- Print ink: black (all top print). Knobs: gloss black.
  LED lens: dark red, unlit in main (hero starts LED off).

## Print inventory (main, case as printed)

Deck (black): `OUTPUT` (under left knob), `SENSITIVITY` (under
right knob), `MXR` (block letters in rounded-rect border,
centre), vertical `OUTPUT` (left edge, by OUTPUT jack),
vertical `INPUT` (right edge, by INPUT jack), `dyna comp`
(lowercase rounded sans, front). The rounded-rect border and
`dyna comp` letterforms are baked into
`textures/mxr-dyna-comp-decal.png` (Phase 90 pattern); the
words above are vector `textLabel`s.
Right wall (not deck print): white CE sticker with `CE`,
crossed-bin mark and `9V` polarity marks, front half of the
wall — carried as spec `sideSticker`, rendered by the hero
page on the right wall. Bottom plate (back.jpg): embossed
`MXR` + 4 Phillips screws — never visible in the hero orbit
(maxPolarAngle 1.62), not modelled.

## Open / provisional

- Side power jack z/y and CE sticker placement: single view
  (right side), ±0.1 in.
- `mxr` knob body (0.92 in dia) reads slightly narrow vs the
  ~1.15 in skirted knobs in main; shared builder, not forked.
  Flagged as a shared-library note, not a per-pedal edit.
