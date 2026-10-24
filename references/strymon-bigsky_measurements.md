# Strymon BigSky — measurements

Slug: `strymon-bigsky`. Exact model: Strymon BigSky Multidimensional
Reverb (original big-box, sky-blue finish; not BigSky MX, not BlueSky).

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| Full top (studio, dead-on) | `references/strymon-bigsky_front.jpg` (1024x754) | Strymon `BigSky_knobs_1600-1024x754.jpg` |
| Top detail (cropped) | `references/strymon-bigsky_topdown.jpg` (1600x834) | Strymon `bigsky_topdowncrop_1600.jpg` |
| Orthographic top | `references/strymon-bigsky_top-ortho.jpg` (800x579, PNG bytes) | PedalPlayground catalog `strymon-bigsky.png` |
| 3/4 hero | `references/strymon-bigsky_hero34.jpg` (1400x1198, PNG bytes) | Strymon `BigSky_Pedal_Site_Trans.png` |
| Back wall + side height | `references/strymon-bigsky_rear.jpg` (1024x723) | Strymon `BigSky_Rear_knobs_1600-1024x723.jpg` |

Each `.jpg` has a matching `.META.txt` from `scripts/fetch_views.py`
(manual backend). Five views of the exact pedal: satisfied (full top,
ortho top, cropped detail, 3/4, back). The back view also shows the
side-wall height and knob/stomp heights; no dead-on side photo was
published by Strymon, so side heights below are corroborated from the
back + 3/4 views and flagged provisional where single-view.
Note: the two files fetched from PNG sources hold PNG bytes under a
`.jpg` name (the fetch script sniffs magic and accepts PNG); they open
as images and their `.META.txt` records the true source URL.

## Published dimensions (anchor)

- Strymon BigSky User Manual (Rev B, specs page): **5" deep x 6.75"
  wide x 1.87" tall**. Corroborated in-repo by
  `verified_strymon_jhs_walrus.json` ("Manufacturer spec: 5 deep x
  6.75 wide x 1.87 tall") and `data/heights.json`
  (`strymon_large` 6.75x5.0 in, height 1.87 in from the manual).
- Current Strymon product page lists 6.75" x 5.1" x 2.7" — read as
  overall (knobs/switches included, depth including rear-jack
  protrusion): 1.87 + knob height (~0.65) + switch travel accounts
  for the 2.7" overall. Spec therefore uses the manual footprint
  **W 6.75 x D 5.00** with bare-enclosure **H 1.87**; the 5.1"/2.7"
  figures are recorded here as the rejected overall reading.
- Spec dims: `w 6.75, d 5.00, h 1.87` (inches).

## Enclosure

Flat-top wide box, vertical walls, small edge radius; brushed
sky-blue aluminium. No slope: top is level in the front, back and
3/4 views, so `enclosure.type: "box"` (no profile points). Height
1.87" is the bare box; knobs and footswitches sit on top of it.
Colour samples (lit, non-specular top patches): front view
`#248cb1` (500,180), `#217fa3` (350,420), `#1f7da1` (850,420);
hero 3/4 highlight up to `#00b3df`. Spec uses `#1a8ab4`, the mid lit
value; the powder-coat grain in `parts.js` supplies the brushed
variation. Print ink is white throughout.

## Top calibration (strymon-bigsky_front.jpg)

- Blue-mask bbox 21..998 px (x) by 30..729 px (y) for 6.75 x 5.00 in
  -> 144.7 px/in (x), 139.8 px/in (z); ~3% anisotropy from the
  near-orthographic studio tilt. Centres below are pixel picks
  converted with that bbox (x = (u-0.5)*W, z = (v-0.5)*D, image top
  = back = -z), then symmetrised where the design is visibly
  symmetric (footswitch row). Two-view corroboration: front +
  top-ortho agree on row order and spacing; hero34 confirms heights.

| Part | x (in) | z (in) | Size / note |
|---|---|---|---|
| LCD display centre | -2.00 | -1.85 | 2.18 x 0.50 in window (315x70 px) |
| VALUE encoder | -0.58 | -1.82 | back row, knob dia ~0.59 in |
| DECAY | +0.42 | -1.82 | back row (1.00 in grid) |
| PRE-DELAY | +1.42 | -1.82 | back row |
| MIX | +2.42 | -1.82 | back row |
| TYPE encoder | -2.17 | -0.46 | front knob row, left |
| TONE | -0.45 | -0.46 | front knob row |
| PARAM 1 | +0.69 | -0.46 | front knob row |
| PARAM 2 | +1.73 | -0.46 | front knob row |
| MOD | +2.77 | -0.46 | front knob row |
| Footswitch A | -2.65 | +1.75 | round chrome, dia ~0.66 in washer |
| Footswitch B | 0.00 | +1.75 | symmetrised (photo B reads -0.13, perspective) |
| Footswitch C | +2.65 | +1.75 | round chrome |
| LED A (green, lit) | -2.65 | +0.83 | above switch A |
| LED B (unlit) | 0.00 | +0.83 | above switch B (print hidden by wordmark) |
| LED C (unlit) | +2.65 | +0.83 | above switch C |

Knob diameter ~85 px = 0.59 in; knob height above deck ~0.6 in
(rear view, provisional). All nine knobs share one black fluted
design with a white pointer line (all pointers at 12 o'clock in the
references, so spec `rot: 0`). TYPE is ringed by 12 small LEDs
(radius ~0.55 in) for the machine names; ROOM (bottom-left LED) is
lit green in every reference.

## Back wall (strymon-bigsky_rear.jpg, viewed from behind)

Viewed from behind, image-left is pedal +x. Left-to-right in the
photo: `LEFT IN, RIGHT IN, LEFT OUT, RIGHT OUT, EXP`, CAB FILTER
mini toggle, `MIDI IN, MIDI OUT`, `9VDC` square socket. Converted
(pedal coords, 0.98 in grid, provisional single-view):

| Jack | x (in) | Note |
|---|---|---|
| LEFT IN | +2.63 | 1/4" (mono in on pedal-right, as cabled) |
| RIGHT IN | +1.65 | 1/4" |
| LEFT OUT | +0.68 | 1/4" |
| RIGHT OUT | -0.30 | 1/4" |
| EXP | -1.25 | 1/4" expression |
| MIDI IN | -2.06 | 5-pin DIN (no `parts.js` builder — see spec notes) |
| MIDI OUT | -2.70 | 5-pin DIN (same) |
| 9VDC | -3.11 | square socket -> `powerJack` |

Jack centre height y ~0.90 in (mid back wall; provisional). Audio/EXP
use the `parts.js` `jack()` barrel via `face: "back"`; MIDI DINs and
the CAB FILTER toggle have no library builder and are built by the
hero page from `spec.midi` / `spec.cabFilter` (proposal in the build
report, same pattern as the TU-3 meter).

## Print inventory (front + top-ortho; case as printed)

- Back row: `VALUE` + `push (param)` / `hold (global)`; `DECAY`;
  `PRE-DELAY`; `MIX`.
- Front knob row: `TYPE` + `push (bank/time)` / `hold (save)`;
  `TONE`; `PARAM 1`; `PARAM 2`; `MOD`.
- Around TYPE (clockwise from bottom): `ROOM, HALL, PLATE, SPRING,
  SWELL, BLOOM, CLOUD, CHORALE, SHIMMER, MAGNETO, NONLINEAR,
  REFLECTIONS` with a dot LED per name.
- Centre: `strymon.` (small sans) over `BigSky` (large script).
- Switch row: `A, B, C` by the LEDs; `BANK DOWN` (between A-B) and
  `BANK UP` (between B-C) with horizontal rules.
- LCD shows decay time `9.30 mS` in green 7-segment style (front
  views; hero34 shows `BIGSKY`). Lit display only — no editing UI.
- Back wall (white caps): `LEFT IN, RIGHT IN, LEFT OUT, RIGHT OUT,
  EXP, CAB FILTER OFF/ON, MIDI IN, MIDI OUT, 9VDC + -C- -`.

## Open / provisional

- Rear-jack x/y and knob/stomp heights are single-view (back photo)
  to ~±0.1 in; top x/z are two-view. Enclosure is a box, so check C
  compares the flat silhouette only.
- The spec's single `footswitch`/`led` fields carry switch B / LED A
  for the validator; all three switches/LEDs are listed in
  `spec.footswitches`/`spec.leds` for the hero page (shared-library
  gap reported, not patched here).
