# Boss CE-2W Chorus (Waza Craft) — measurements

Slug: `boss-ce2w`. Exact model: Boss CE-2W Chorus Waza Craft Special
Edition (light-blue compact, Made in Japan). Not the mono CE-2 (no mode
switch, mono out) and not the CE-5/CE-3. Controls: RATE + DEPTH knobs,
3-position Standard/CE-1 mode switch (S / CE-1 Chorus / CE-1 Vibrato),
CHECK LED, stereo outputs.

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| True top-down | `references/boss-ce2w_topdown.jpg` (350x621 PNG) | PedalPlayground catalog `boss-ce2w.png` |
| Dead-on front | `references/boss-ce2w_front.jpg` (598x1050) | Boss official `CE-2W_F_gal.jpg` |
| Front 3/4 (OUTPUT side) | `references/boss-ce2w_hero34.jpg` (1540x1027) | Boss official `CE-2W_image1_gal.jpg` |
| Back 3/4 (back wall + DC) | `references/boss-ce2w_rear.jpg` (1540x1027) | Boss official `CE-2W_image_R_gal.jpg` |
| Side 3/4 (INPUT side) | `references/boss-ce2w_angle.jpg` (1540x1027) | Boss official `CE-2W_image2_gal.jpg` |
| Detail 3/4 | `references/boss-ce2w_detail.jpg` (936x1050) | Boss official `CE-2W_D_gal.jpg` |
| Small front | `references/boss-ce2w_main.jpg` (189x330) | Boss official `CE-2W_main.jpg` |

Each `.jpg` has a matching `.META.txt` from `scripts/fetch_views.py`
(manual backend). Seven views of the exact pedal: satisfied (top-down,
front, back, both side-jack arrangements in the two 3/4s).

## Published dimensions (anchor)

- Boss CE-2W manufacturer spec (boss.info CE-2W specifications page,
  retrieved 2026-10-24): **73 (W) x 129 (D) x 59 (H) mm**
  = 2-7/8 x 5-1/8 x 2-3/8 in, weight 450 g incl. battery.
  Corroborated by Thomann spec tab (73 x 59 x 129 mm, 450 g).
- In inches: 2.874 x 5.079 x 2.323. Spec uses w 2.875 to match the
  measured DS-1 Boss-compact profile widths exactly (0.001 in rounding,
  below validator tolerance), as `specs/boss-tu3.json` does.
- Modes (Boss spec): 3 modes — Standard, CE-1 Chorus, CE-1 Vibrato.
  Controls: pedal switch, Standard/CE-1 Mode switch, RATE knob,
  DEPTH knob. Indicator: CHECK. Bypass: buffered. Stereo output
  (OUTPUT A (MONO) / OUTPUT B) — the CE-2W delta over the mono CE-2.

## Enclosure construction (reused from DS-1, legitimately)

CE-2W is a standard Boss compact: same die-cast body, pivoting
treadle, rubber pad, recess, base plate and toe thumbscrew as the DS-1
measured in `references/ds1_measurements.md`. The DS-1 measured
profiles (`enclosure.points`, `treadleProfile`, `recessProfile`,
`padProfile`, `baseProfile` in `specs/ds1.json`, Caedon-approved v4,
2026-10-01) are reused verbatim; only colours change (blue). Side
silhouette, heights and hinge geometry therefore carry DS-1
provenance, not new guesses. What is new on CE-2W is only what sits
on the flat back deck (2 knobs + mode switch instead of 3 knobs),
the stereo jack set, and the treadle print.

## Top-down calibration (boss-ce2w_topdown.jpg)

- Image 350x621 px is a tight crop of the footprint: 110.9 px/in (x,
  319 px blue width incl. jack protrusion / 2.875 in), 122.3 px/in
  (z, 621 px / 5.079 in). Image top = back (-z). Origin at pedal
  centre (x px 175.5, z = -2.5395 + y_px/122.27).
- Knob dark-ring bboxes: RATE x 51-159, DEPTH x 191-301, both
  y 41-139 -> centres (105, 90) and (246, 90).
- Front view cross-check (`boss-ce2w_front.jpg`, blue bbox
  x 29-566 = 187.1 px/in): knob dark-mass centres x 178.3 / 417.3
  about centre 297.5 -> +/-0.64 in. Two views agree.

| Part | x (in) | z (in) | Source |
|---|---|---|---|
| RATE knob (large Boss) | -0.64 | -1.80 | topdown + front |
| DEPTH knob (large Boss) | +0.64 | -1.80 | topdown + front |
| CHECK LED (red) | 0.00 | -2.24 | topdown (red px 176.5, 36.8) + front |
| Mode switch slot | +0.02 | -1.41 | topdown slot px (178, 138) |
| OUTPUT A jack (left, rear) | left wall | -0.63 | topdown jack bore y~233 |
| OUTPUT B jack (left, front) | left wall | +0.24 | topdown jack bore y~340 |
| INPUT jack (right) | right wall | -0.45 | topdown jack bore y~255 |
| Toe thumbscrew | 0.00 | +2.45 (protrudes) | topdown; DS-1 hardware reused |

Knob diameter/height: Boss large knob as DS-1 (19.6 mm dia class,
`parts.js` `boss` style). Pointers point up (12 o'clock) in both
front and topdown references -> `rot: 0`.

Side-jack height y 1.094 in reused from DS-1 (same wall, same jack
hardware; corroborated in hero34/angle views). DC jack on the back
wall (`boss-ce2w_rear.jpg`, viewed from behind): single square
Boss DC IN centred x 0.00, y ~0.72 (provisional, single view,
+/-0.1 in). No DC OUT (unlike TU-3). Back sticker above it (see
print inventory).

Mode switch behaviour (owner's manual + Boss spec): left = S
(Standard, CE-2 sound), middle = CE-1 Chorus, right = CE-1 Vibrato.
RATE/DEPTH act in all modes. Photos show the lever at the left (S)
detent. The hero reproduces this: click the switch to cycle
S -> CE-1 Chorus -> CE-1 Vibrato, lever stepping across the slot.
No audio is modelled.

## Colours

- Enclosure/treadle blue: lit non-specular patches in
  `boss-ce2w_front.jpg` sampled (53,168,197) `#35a8c5` (upper deck)
  and (13,165,189) `#0da5bd` (treadle). Spec uses `#27a8c7`
  (midpoint; powder-coat speckle lightens it a few percent in
  render). PedalPlayground topdown reads paler (`#7ec6dc` class)
  under flat catalog light — front/hero photos break the tie.
- Print ink: near-black `#1a1a1a` (all deck/treadle lettering is
  black on the blue, unlike TU-3's red/white). Rubber pad `#1a1a1c`
  (as DS-1); recess shadow blue `#14657d`; WAZA CRAFT badge white
  on black (in pad decal).

## Print inventory (topdown + front; case as printed)

Deck (black, fixed): `CHECK` (above LED), `RATE` (under left knob),
`DEPTH` (under right knob), `S` (above-left of switch), `CE-1`
(below switch, with 2 dots for the CE-1 positions).
Treadle (black, moves with treadle): `OUTPUT A` + `(MONO)` +
`OUTPUT B` (left, left-arrows, A boxed), `INPUT` (right,
left-arrow), `Chorus` (large), `CE-2w` (below-right of Chorus).
Pad: embossed `BOSS` + `WAZA CRAFT` badge with kanji (in pad
decal, as DS-1). Back wall (black on silver sticker): `CE-2w`,
`SER No. 00001`, `MADE IN JAPAN`, `USE BOSS PSA ADAPTOR ONLY
(9V DC)` (hero page back-wall art, from `boss-ce2w_rear.jpg`).

## Open / provisional

- Jack z and DC y from single views (+/-0.1 in); enclosure/treadle
  geometry is DS-1-measured, not re-measured for CE-2W.
- Treadle-label `surfaceY` values are interpolated on the DS-1
  treadle slope (`1.608 - 0.297*z`, fit to DS-1's three baked
  treadle labels, residual <0.002 in), not independently raycast.
