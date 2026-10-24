# EHX Big Muff Pi (NYC reissue big box) — measurements

Slug: `ehx-big-muff-pi`. Exact model: current NYC/original reissue big box
(not Nano, Triangle, Op-Amp, or Sovtek variants).

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| 3/4 front (hero) | `references/ehx-big-muff-pi_front.jpg` (1500x1000) | EHX product page `usbm-f.jpg` |
| 3/4 top/front | `references/ehx-big-muff-pi_detail1.jpg` (1000x1000) | EHX product page `usbm-1.jpg` |
| Back wall | `references/ehx-big-muff-pi_detail2.jpg` (1000x1000) | EHX product page `usbm-2.jpg` |
| Side A | `references/ehx-big-muff-pi_side1.jpg` (1000x1000) | EHX product page `usbm-3.jpg` |
| Side B | `references/ehx-big-muff-pi_side2.jpg` (1000x1000) | EHX product page `usbm-4.jpg` |

Each `.jpg` has a matching `.META.txt` written by `scripts/fetch_views.py`.
Four-plus views of the exact pedal: satisfied (front, top/3-4, back, both sides).

## Published dimensions (anchor)

- `data/spec_sheets_staging.json` (verified, EHX product page): 5.5 x 6.88 x 2.95 in
  (139.7 x 174.8 x 74.9 mm). Axis mapping via labelled dealer W x D x H 140 x 175 x 75 mm:
  W (left-right) = 5.5, D (front-back) = 6.88, H = 2.95.
- Corroborated by `data/heights.json` "Electro-Harmonix | Big Muff Pi (Big Box)"
  height 2.95 in, confidence high.
- Conflicts rejected: B&H-derived 6.75 x 5.5 x 2.0 in and Thomann 140 x 173 x 76 mm
  (axis/order variants); Amazon axis labels and EHX shipping dims not used.
- `height_includes_knobs` is "unknown" in staging, so the bare-enclosure height
  was resolved from the side photos below instead of assuming 2.95 in is bare.

## Side-profile calibration (side1, 1000x1000)

- Enclosure depth in frame: x ~38 to ~970 px = 932 px for 6.88 in -> 135.5 px/in.
- Bottom edge y ~658 px. Back top y ~365 px -> bare back height
  (658-365)/135.5 = **2.16 in**.
- Front top y ~472 px -> bare front height (658-472)/135.5 = **1.37 in**.
- Knob top y ~262 px -> overall height (658-262)/135.5 = **2.92 in**, matching the
  published 2.95 in. Conclusion: **2.95 in is overall (knobs included)**; the bare
  sloped enclosure is 2.16 in (back) to 1.37 in (front), a single straight slope.
- Enclosure profile (back -z to front +z): `[[-3.44, 2.16], [3.44, 1.37]]`.
- Construction: brushed-silver top plate over a black sheet-metal lower box.
  Modelled as a black enclosure (sides read black) with the silver/art top
  supplied by the decal, so both colours land on the right faces.

## Top layout (detail1 homography)

Top-face corners mapped to pedal coords (W 5.5, D 6.88; back = -z) with a
planar homography, then symmetrised (the row is evenly spaced on the real pedal;
the ~0.2 in common offset is a corner-pick artefact):

| Part | x (in) | z (in) | Notes |
|---|---|---|---|
| VOLUME knob | -1.93 | -2.45 | 3 black hockey-puck knobs in a row near the back |
| TONE knob | 0.00 | -2.45 | centre knob |
| SUSTAIN knob | 1.93 | -2.45 | right knob |
| LED (red) | -0.90 | -1.82 | between VOLUME and TONE, forward of the knob row |
| Footswitch (round) | 0.00 | 1.97 | centred, in the black lower field |
| AMPLIFIER jack | -2.01 | back wall | back face, left in top view (see below) |
| INPUT jack | 1.88 | back wall | back face, right in top view |
| Power jack | -0.05 | back wall | back face, centred, between the audio jacks |

Knob diameter ~1.05 in, height ~0.75 in above the local deck (side view).
Single-view positions are provisional per the guide; knob/LED/switch were read
from the 3/4 top view and corroborated in the straight front view.

## Back wall (detail2, viewed from behind)

Audio jacks and power are on the **back face**, not the side walls (classic
big-box layout). Viewed from behind, image-left is the pedal's right (+x):
INPUT (+1.88) on image-left, power (-0.05) centre, AMPLIFIER/output (-2.01)
on image-right. Jack height from the calibrated face: y ~0.85 in.

## Print inventory (front + detail1, top view)

- Top edge, above knobs: `AMPLIFIER` (left), `INPUT` (right), black caps.
- Below knobs: `VOLUME`, `TONE`, `SUSTAIN`, black caps; red LED between
  VOLUME and TONE.
- Mid: `BIG MUFF` in large red block letters with white fill, red rules above
  and below, red pi symbol in a red semicircle under the wordmark.
- Lower field: solid black panel holding the footswitch.
- Front edge: `electro-harmonix` script (black) with `USA` beneath it.
- Four silver screws at the top-face corners.

Colours: top plate brushed silver (~#c9c9c7 sampled from a lit non-specular
patch), lower box and black field near-black (~#17181a), print red ~#d8232a,
knobs black.
