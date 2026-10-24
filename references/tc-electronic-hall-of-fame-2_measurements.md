# TC Electronic Hall of Fame 2 — measurements

Slug: `tc-electronic-hall-of-fame-2`. Exact model: TC Electronic
Hall of Fame 2 Reverb (full-size TonePrint pedal with MASH footswitch,
not the Mini, not the X4). Custom compact box, stereo in/out.

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| Dead-on front (layout) | `references/tc-electronic-hall-of-fame-2_front.jpg` (371x600) | Thomann gallery `12228542_800.jpg` via `scripts/fetch_views.py` manual |
| 3/4 hero | `references/tc-electronic-hall-of-fame-2_hero34.jpg` (530x600) | Thomann gallery `12228587_800.jpg` |
| Close-up 3/4 (switch/LED) | `references/tc-electronic-hall-of-fame-2_detail.jpg` (580x600) | Thomann gallery `12228552_800.jpg` |
| Right wall (STEREO IN) | `references/tc-electronic-hall-of-fame-2_side_in.jpg` (774x600) | Thomann gallery `12228557_800.jpg` |
| Left wall (STEREO OUT) | `references/tc-electronic-hall-of-fame-2_side_out.jpg` (800x594) | Thomann gallery `12228567_800.jpg` |
| Back edge / DC (180-rotated top) | `references/tc-electronic-hall-of-fame-2_back.jpg` (426x600) | Thomann gallery `12228607_800.jpg` |

Each `.jpg` has a matching `.META.txt` written by
`scripts/fetch_views.py`. Six views of the exact pedal: satisfied
(front layout, two 3/4s, both side walls, back edge). No true
orthographic side elevation exists in the Thomann set; enclosure
height is anchored on the published dims below, not on a side
silhouette (box enclosure, so no profile trace is needed).

## Published dimensions (anchor)

- TC Electronic Hall of Fame (identical enclosure) manual via
  `data/spec_sheets_staging.json` (verified): **72 x 122 x 50 mm**
  = **2.835 x 4.803 x 1.969 in** (W x D x H). Thomann labels the same
  72 x 122 x 50 mm. The HOF2 manual misprints the Mini dims
  (93 x 48 x 48 mm) — rejected, as is the Mini/X4.
- Spec uses w 2.835, d 4.803, h 1.969. `height_includes_knobs` is
  "unknown" in staging; the 50 mm is adopted as the bare-enclosure
  height, following the Boss/MXR convention in this repo that the
  published H is the enclosure (knob tops exceed it by ~0.45 in).
  Corroborated by `verified_tc_ibanez.json`: Sweetwater H 2 in,
  manufacturer 72x122x50 mm (1.97 in).
- Enclosure: single flat-top box (`type: "box"`), no preset matches
  (closest is Boss compact at 73x129x59 mm — HOF2 is 7 mm shorter
  and 9 mm lower), so per-model dims override with no preset key.
  Edge radius 0.10 in from the front-view corner rounding.

## Front-view calibration (front, 371x600)

- Red-body bbox 307x548 px (x 32..338, y 28..575); the 371-px frame
  width includes the side-jack protrusions, so the enclosure edges
  are read per-row from the red mask: width 290 px at the back
  (y=60, x 48..338) tapering to 273 px at the front (y=500,
  x 54..326) — ~6% perspective taper, camera near-orthographic.
- Scale: 290 px / 2.835 in = **102 px/in (x)** at the knob rows;
  548 px / 4.803 in = **114 px/in (z)**. The x/z mismatch is the
  perspective taper; knob mapping below interpolates the left/right
  edges linearly with y and maps y linearly back (-2.4015) to front
  (+2.4015). Residual position error ~±0.08 in, flagged provisional
  where single-view.
- Dark-blob centroids (threshold <45, components >2000 px are the
  four knobs, verbatim from the measurement script):

| Part | px centre | pedal x (in) | pedal z (in) | spec (symmetrised) |
|---|---|---|---|---|
| DECAY knob | (131.8, 104.9) | -0.61 | -1.73 | **-0.66, -1.72** |
| TONE knob | (264.8, 106.4) | +0.71 | -1.71 | **+0.66, -1.72** |
| LEVEL knob | (131.7, 224.0) | -0.61 | -0.68 | **-0.66, -0.69** |
| Mode selector | (263.7, 222.9) | +0.71 | -0.69 | **+0.66, -0.69** |
| PRE-DELAY toggle | (193.3, 119.2) | +0.00 | -1.60 | **0.00, -1.60** |
| LED (red lens) | ~(197, 298) | +0.05 | -0.03 | **+0.05, -0.03** |
| MASH footswitch | (187.7, 442.7)* | -0.03 | +1.24 | **0.00, +1.24** |

*Bright-chrome mean; the washer/plunger centroid, centred to x=0.
The ±0.05 in left/right asymmetry (DECAY -0.61 vs TONE +0.71) is a
perspective/centre-pick artefact; the real 2x2 grid is symmetric
(hero34 confirms equal spacing), so the spec symmetrises to
±0.66 in. Knob diameter from blob width 70 px / 102 px/in =
**0.69 in** (z extent 74 px / 114 px/in = 0.65 in) — spec uses the
`mxr` Davies body scaled dia 0.72 / height 0.88 (~0.66 in across,
~0.43 in tall above the deck; side views corroborate a chunky
black knob roughly 1.6x the 0.40 in jack-nut width).

## Second view (hero34, 530x600, perspective 3/4)

Hero34 looks at the same grid diagonally (back edge top-right,
front edge bottom-left). Reading fractions along the pedal's long
axis (back 0% to front 100%) and across (left 0% to right 100%):

| Part | across | along | implied z (in) | vs front |
|---|---|---|---|---|
| DECAY | ~22% left | ~12% | -1.83* | grid agrees |
| TONE | ~78% right | ~14% | -1.73 | agrees |
| LEVEL | ~24% left | ~33% | -0.82* | agrees |
| Mode | ~76% right | ~35% | -0.73 | agrees |
| LED | ~52% | ~48% | -0.10 | agrees |
| Footswitch | ~50% | ~72% | +1.05* | agrees |

*Perspective foreshortening compresses the far (back) end, so
hero34 along-fractions are biased ~0.1 in toward the front at the
back row; the front-view ortho numbers govern. Both views agree
on: 2x2 symmetric grid, top row at the back, LED centred just
forward of the mode row, footswitch centred in the front third.
DECAY/TONE/LEVEL + mode positions are therefore two-view
confirmed (front ortho + hero34 fractions), not single-view.

## Side walls, jacks, power (front + side_in + side_out + back)

- Four side jacks (stereo pairs). Non-white pixel clusters in the
  front view give two jack rows per side: rear cluster centre
  y=307 px, front cluster y=382 px (left; right 306/380 px).
  Mapped: **z +0.05 (rear)** and **z +0.71 (front)** on both walls.
  Label adjacency in the enlarged front view puts `MONO` beside
  the rear jack and `STEREO` beside the front jack, with `OUT`
  (left) / `IN` (right) between them: rear = MONO, front = STEREO.
  Jack height y **0.98 in** (wall centre, side_in/side_out: the
  jack axis sits at mid-wall; provisional ±0.1 in, single-height
  view). Left = OUTPUT, right = INPUT (print-confirmed).
- Power: 9V DC barrel centred on the back wall (back view, viewed
  from behind: the jack sits at the image-bottom centre, which is
  pedal x=0 on the back edge): **powerJack x 0.00, y 0.98**,
  `style: "round"`. The mini-USB port for TonePrint sits on the
  same back wall (hero34/detail show the cable plugged in at the
  back edge, right of the DC jack): spec field `usb` at
  x +0.70, y 0.98, built by the hero page (no parts.js builder —
  see the build report's shared-needs list).
- PRE-DELAY toggle: miniature bat toggle between DECAY and TONE,
  spec field `toggle` at (0.00, -1.60), built by the hero page
  from that field (same no-builder situation). Its tiny MASH
  indicator LED beside it is print + a dark dot in the photos;
  only the print is modelled (decal), the dot is below hero
  viewing distance.

## Colours

- Enclosure red: median of red-mask pixels in front view
  **#A9152A** (169,21,42); lit non-specular patch (80,300)
  #A70222, (280,470) #AE1B2E. Spec colour **#A11624** (between the
  median and lit patch; the brighter #B31B2E first tried washed to
  pink at the hero grazing angle, the median value holds red).
- Print silver #D9DEE6 (HALL OF FAME 2 / tc electronic / knob
  labels), accent orange #D96C2C (MASH / IN / OUT), LED red.
- Knobs black gloss, footswitch chrome, jacks chrome.

## Print inventory (front + hero34; case as printed)

Back-to-front, silver unless noted: `DECAY` over the DECAY knob;
`PRE-DELAY` with `SHORT` / `LONG` stacked over the toggle;
`TONE` over the TONE knob; `MASH` (orange, with `)))` ) under the
toggle; `LEVEL` over the LEVEL knob; around the mode selector,
clockwise from top: `SHIM`, `MOD`, `LOFI`, boxed `1`, `2`, `3`
(TonePrint slots), `ROOM`, `HALL`, `SPRING`, `PLATE`, `CHURCH`;
red LED; `HALL OF FAME 2` (large silver, distressed block) with
`REVERB` at its left; vertical side print, left wall bottom-to-top
`STEREO` / `OUT` (orange) / `MONO`, right wall `STEREO` / `IN`
(orange) / `MONO`; `MASH` (orange, with `)))`) right of the
footswitch; `TRUE BYPASS` arced under the footswitch;
`tc electronic` with the tc logo at the front edge. Mode-arc,
big-logo, MASH/TRUE BYPASS and tc wordmarks are in
`textures/tc-electronic-hall-of-fame-2-decal.png`; DECAY/TONE/
LEVEL/PRE-DELAY/SHORT/LONG and the vertical side words are vector
`textLabel`s above it.

## MASH footswitch behaviour

The MASH switch is pressure-sensitive (expression-style) as well
as a bypass switch. No reference shows a distinct pressure state
at hero viewing distance, so the hero follows the other heroes:
press-and-hold dips the plunger, release springs it back and
toggles the LED on release. The pressure dimension is noted here
and in the HUD hint; it is not separately modelled.

## Open / provisional

- Knob x symmetrised (±0.66) from a ±0.05 in asymmetric read;
  knob z, LED, footswitch, toggle from the front ortho (±0.08 in).
- Jack z from the front view (±0.1 in); jack/power y from side
  views (±0.1 in). USB x from the plugged-cable hero views.
- Bare height adopted from the published 50 mm (see above).
