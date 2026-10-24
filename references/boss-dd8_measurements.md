# Boss DD-8 Digital Delay — measurements

Slug: `boss-dd8`. Exact model: Boss DD-8 Digital Delay (standard compact,
white/champagne finish, not DD-3/DD-7/DD-200). Four knobs
(E.LEVEL / FEEDBACK / TIME / MODE), CHECK LED, stereo I/O + TEMPO/EXP,
CARRYOVER switch on the back wall.

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| True top-down (orthographic render) | `references/boss-dd8_topdown.jpg` (350x621 PNG) | PedalPlayground catalog `boss-dd8.png` |
| Dead-on front (top face) | `references/boss-dd8_top.jpg` (980x700 PNG) | Boss official `dd-8_gal_top.png` |
| Front elevation (top face, tall) | `references/boss-dd8_front.jpg` (588x1050) | Boss official gallery `dd-8_top_gal.jpg` |
| 3/4 top/front | `references/boss-dd8_hero34.jpg` (855x1050) | Boss official gallery `dd-8_angle_gal.jpg` |
| Back wall | `references/boss-dd8_back.jpg` (1306x1050) | Boss official gallery `dd-8_back_gal.jpg` |
| Lifestyle 3/4 | `references/boss-dd8_hero.jpg` (1600x1067) | Boss official `dd-8_hero.jpg` |
| Main packshot | `references/boss-dd8_main.jpg` (185x330) | Boss official `dd-8_main.jpg` |
| Detail crops | `references/boss-dd8_detail1.jpg`, `boss-dd8_detail2.jpg` | Boss official `dd-8_gal_01/02.jpg` |

Each `.jpg` has a matching `.META.txt` from `scripts/fetch_views.py`
(manual backend). Seven views of the exact pedal: satisfied (top-down,
front, back, 3/4s showing both side-jack arrangements).
Note: `boss-dd8_top.jpg` is Boss's `dd-8_gal_top.png` (PNG bytes saved
with a `.jpg` name by the fetcher); dimensions/format recorded here.

## Published dimensions (anchor)

- Boss DD-8 manufacturer spec: **73 (W) x 129 (D) x 59 (H) mm**
  = 2.874 x 5.079 x 2.323 in. Corroborated by the DD-8 owner's-manual
  spec table via retailer spec tabs (73 x 129 x 59 mm; 2-7/8 x 5-1/8 x
  2-3/8 in; 440 g with battery) and the shared Boss compact preset
  `boss_compact` in `parts.js` (73 x 129 x 59 mm, high confidence).
- Spec uses w 2.875 to match the measured DS-1 Boss compact profile
  widths exactly (0.001 in rounding, below validator tolerance).
- Controls (manual): MODE, TIME, FEEDBACK, E.LEVEL knobs; CARRYOVER
  switch; pedal switch. Connectors: INPUT-A (MONO)/INPUT-B,
  OUTPUT-A (MONO)/OUTPUT-B, TEMPO/EXP (TRS), DC IN. CHECK indicator.

## Enclosure construction (reused from DS-1, legitimately)

DD-8 is a standard Boss compact: same die-cast body, pivoting treadle,
rubber pad, recess, base plate and toe thumbscrew as the DS-1 measured
in `references/ds1_measurements.md`. The DS-1 measured profiles
(`enclosure.points`, `treadleProfile`, `recessProfile`, `padProfile`,
`baseProfile` in `specs/ds1.json`, Caedon-approved v4, 2026-10-01) are
reused verbatim; only colours change (champagne white). Side
silhouette, heights and hinge geometry therefore carry DS-1
provenance, not new guesses. What is new on DD-8 is only what sits on
the flat back deck (four knobs + black control panel instead of the
DS-1's three knobs) and the treadle print.

## Top-down calibration (boss-dd8_topdown.jpg + boss-dd8_front.jpg)

Two independent views measured; positions agree to ~0.02 in.

- Topdown: body x 16..334 px (centre 175, width 319 px), body
  y 2..596 px (centre 299, depth 594 px). Image top = back (-z).
  Blue-cap segmentation (B>140, R<110, G>90) gives four knob clusters.
- Front (588x1050): body x 31..557 px at the knob row (centre 294),
  body y ~12..1012 px. Blue-cap segmentation gives the same four
  centres. Front is a perspective studio shot, so it cross-checks x/z
  but does not anchor absolute scale; the published W/D anchor scale.

| Part | x (in) | z (in) | Diameter | Source |
|---|---|---|---|---|
| E.LEVEL knob (leftmost) | -0.99 | -1.75 | blue cap 0.44, skirt ~0.55 | topdown (-0.979,-1.744) + front (-0.997,-1.763) |
| FEEDBACK knob | -0.31 | -1.75 | blue cap 0.44, skirt ~0.55 | topdown (-0.310,-1.743) + front (-0.315,-1.760) |
| TIME knob | +0.36 | -1.75 | blue cap 0.44, skirt ~0.55 | topdown (+0.353,-1.740) + front (+0.360,-1.753) |
| MODE knob (rightmost, detented) | +1.02 | -1.74 | blue cap 0.44, skirt ~0.55 | topdown (+1.013,-1.730) + front (+1.031,-1.742) |
| CHECK LED (red dot) | 0.00 | -2.26 | ~0.16 lens | topdown red cluster (173.9,35.7) + front (292.7,65.7) |
| Black control panel extent | w 2.45, z -2.47..-0.95 | — | topdown + front (panel corners) |
| OUTPUT B jack (left, rear) | left wall | -1.06 | — | topdown jack band y150-200 + front |
| OUTPUT A jack (left, front) | left wall | -0.42 | — | topdown jack band y220-280 + front |
| INPUT B jack (right, rear) | right wall | -1.06 | — | topdown jack band y150-200 + front |
| INPUT A jack (right, mid) | right wall | -0.42 | — | topdown jack band y220-280 + front |
| TEMPO/EXP jack (right, front) | right wall | +0.22 | — | topdown right-only band y300-350 + front |
| Toe thumbscrew | 0.00 | +2.45 (protrudes) | — | topdown; DS-1 hardware reused |

Knob spec positions use the two-view means rounded to 0.01 in
(E.LEVEL -0.99, FEEDBACK -0.31, TIME +0.36, MODE +1.02; all z -1.75).
Single-view jack z values are provisional to ~±0.1 in (flagged in the
spec). Side-jack height y 1.094 in reused from DS-1 (same wall, same
jack hardware; corroborated in hero34/back views).

Back wall (`boss-dd8_back.jpg`, viewed from behind so image-left =
pedal +x): DC IN square jack at pedal x ~-0.20, y ~0.85 (provisional,
single view); CARRYOVER slide switch below the PSA sticker at pedal
x ~+0.65. The hero models DC IN via `spec.powerJack`; the CARRYOVER
switch and back-wall print are page-built from spec fields (no
`parts.js` builder yet — see ship report).

## Colours (sampled)

- Enclosure/treadle champagne white: lit non-specular patch
  #d7ccba (front slope, 215,204,186) / #d8cebb (top); spec uses
  #e2d7bf (same hue, lifted for the studio's ACES tone mapping so the
  pedal does not render grey; hue matches the sample).
- Knob blue caps: #1faf e3 sampled (31,175,227) = #1fafe3; spec/page
  blue #1fb6e8. Print blue (OUTPUT/Digital Delay): deep Boss blue,
  ~#1e3fae from letterforms.
- Control panel near-black #0b0b0d; rubber pad #1a1a1c (as DS-1);
  recess shadow grey-brown for the champagne finish.

## Print inventory (topdown + front; case as printed)

Control panel (white on black, deck-fixed): `CHECK`,
`E.LEVEL`, `FEEDBACK`, `TIME`, MODE arc: `LOOP`, `ANALOG`,
`STANDARD`, `TAPE`, `WARM`, `REVERSE`, `+RV`, `SHIM`, `MOD`,
`WARP`, `GLT`, plus `STOP LOOP: PRESS TWICE` / `SET TEMPO: HOLD`.
Small silver dot markers sit below E.LEVEL/FEEDBACK/TIME/MODE.
Treadle/chassis (blue, moves with treadle): `OUTPUT B`,
`OUTPUT A (MONO)`, `INPUT B`, `INPUT A (MONO)`, `TEMPO/EXP`
(each with a jack-direction arrow), `Digital Delay`, `DD-8`.
Pad: embossed `BOSS`. Back wall (white on black sticker + direct
print): `USE BOSS PSA ADAPTOR ONLY (DC 9V)` with polarity diagram,
`CARRYOVER ON OFF`.

## Open / provisional

- Jack z and DC y from single views (±0.1 in); enclosure/treadle
  geometry is DS-1-measured, not re-measured for DD-8.
- MODE arc label positions are placed on the photographed arc
  (radius ~0.48 in about the MODE centre) from the front view;
  individual detent words are legibility-placed, not triangulated.
