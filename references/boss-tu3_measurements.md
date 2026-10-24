# Boss TU-3 Chromatic Tuner — measurements

Slug: `boss-tu3`. Exact model: Boss TU-3 Chromatic Tuner (standard white
compact, not TU-3S/TU-3W). No knobs — controls are the pedal switch plus
MODE and STREAM/CENT buttons under a 21-segment LED meter.

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| True top-down | `references/boss-tu3_topdown.jpg` (350x621 PNG) | PedalPlayground catalog `boss-tu3.png` |
| Dead-on front | `references/boss-tu3_top-ortho.jpg` (980x700) | Boss official `tu-3_top.png` |
| Front elevation | `references/boss-tu3_top.jpg` (593x1050) | Boss official `tu-3_top_gal.jpg` |
| 3/4 top/front | `references/boss-tu3_hero34.jpg` (894x1050) | Boss official `tu-3_angle_gal.jpg` |
| Back wall | `references/boss-tu3_back.jpg` (1359x1050) | Boss official `tu-3_rear_gal.jpg` |
| Lifestyle 3/4 (left side) | `references/boss-tu3_hero.jpg` (1600x1067) | Boss official `tu-3_hero.jpg` |

Each `.jpg` has a matching `.META.txt` from `scripts/fetch_views.py`
(manual backend). Six views of the exact pedal: satisfied (top-down,
front, back, two 3/4s showing both side-jack arrangements).

## Published dimensions (anchor)

- Boss TU-3 manufacturer spec: **73 (W) x 129 (D) x 59 (H) mm**
  = 2.874 x 5.079 x 2.323 in. Corroborated by ManualsLib TU-3 owner's
  manual spec table and multiple retailer spec tabs (2-7/8 x 5-1/8 x
  2-3/8 in). Same Boss compact enclosure as DS-1/SD-1.
- Spec uses w 2.875 to match the measured DS-1 profile widths exactly
  (0.001 in rounding, below validator tolerance).

## Enclosure construction (reused from DS-1, legitimately)

TU-3 is a standard Boss compact: same die-cast body, pivoting treadle,
rubber pad, recess, base plate and toe thumbscrew as the DS-1 measured
in `references/ds1_measurements.md`. The DS-1 measured profiles
(`enclosure.points`, `treadleProfile`, `recessProfile`, `padProfile`,
`baseProfile` in `specs/ds1.json`, Caedon-approved v4, 2026-10-01) are
reused verbatim; only colours change (white). Side silhouette, heights
and hinge geometry therefore carry DS-1 provenance, not new guesses.
What is new on TU-3 is only what sits on the flat back deck (meter
panel instead of knobs) and the treadle print.

## Top-down calibration (boss-tu3_topdown.jpg)

- Alpha bbox 348x621 px for 2.874x5.079 in -> 121.1 px/in (x),
  122.3 px/in (z); 1% agreement. Image top = back (-z).
- Bbox includes side-jack protrusion and toe thumbscrew, so z values
  are provisional to ~±0.1 in. Single-view values flagged below.

| Part | x (in) | z (in) | Source |
|---|---|---|---|
| CHECK LED (red dot) | 0.00 | -2.31 | topdown + front |
| Meter panel extent | w 2.45, z -2.47..-0.86 | topdown (screws ±1.10) |
| Meter panel screws (x4) | ±1.10 | -2.19 / -0.98 | topdown |
| Note display (red "A") | 0.00 | -1.47 | topdown + front |
| STREAM/CENT button | -0.57 | -1.31 | topdown |
| MODE button | +0.58 | -1.31 | topdown |
| OUTPUT jack (left, rear) | left wall | -0.34 | topdown |
| BYPASS jack (left, front) | left wall | -0.04 | topdown |
| INPUT jack (right) | right wall | -0.34 | topdown |
| Toe thumbscrew | 0.00 | +2.45 (protrudes) | topdown; DS-1 hardware reused |

Side-jack height y 1.094 in reused from DS-1 (same wall, same jack
hardware; corroborated in hero34/back views). DC jacks on the back
wall (boss-tu3_back.jpg, viewed from behind so image-left = pedal
+x): DC IN at x +0.52, DC OUT at x -0.52, y ~0.85 (provisional,
single view). Back sticker text is above them (see print inventory).

Meter behaviour (owner's manual + photos): pedal switch toggles the
tuner. ON: CHECK lit, meter LEDs + note display lit, output muted.
OFF: display dark, signal passes (buffered bypass). Photos show the
ON state (centre green LED lit, note "A"). The hero reproduces this:
stomp release toggles CHECK + meter array + note display together.
MODE cycles tuning mode; STREAM/CENT selects Cent (single pip) vs
Stream (flowing) meter display. No audio is modelled.

## Colours

- Enclosure/treadle white: lit non-specular patch #f6f6f6 (front view);
  spec uses #f2f1ed (slightly warm, matches lifestyle hero).
- Print red (OUTPUT/Chromatic/TU-3): Boss TU-3 red-orange, ~#d93a2b
  (front-view letterforms; CHECK dot sampled #eb1d24).
- Meter panel near-black #101114; rubber pad #1a1a1c (as DS-1);
  recess shadow grey #5a5c60; meter LEDs red/yellow/green with green
  centre (in-tune) per front view.

## Print inventory (topdown + front; case as printed)

Meter panel (white unless noted): `CHECK`, `0`, `-50`, `+50`,
`3 2 b BASS 6 5 4 3 2 b GUITAR 2 b CHROMATIC` (b = flat sign),
`STREAM / CENT (PRESS & HOLD)` + brightness mark, `MODE`, `-#`
(sharp/flat by the note display), `PITCH` with down/up triangles.
Treadle (red, moves with treadle): `OUTPUT` (left arrow),
`INPUT` (right arrow), `BYPASS` (left arrow), `Chromatic`,
`Tuner`, `TU-3`. Pad: embossed `BOSS` (in pad geometry/decal path,
as DS-1). Back wall (red on light-grey sticker): `DC 9V Out jack:
Total of consumption current must not be exceeded the rating current
of PSA adaptor you use.` + `IN` / `OUT` under the DC jacks.

## Open / provisional

- Jack z and DC y from single views (±0.1 in); enclosure/treadle
  geometry is DS-1-measured, not re-measured for TU-3.
- Meter panel height 0.09 in above the flat deck (surfaceY 1.66)
  estimated from back/hero34 lens protrusion.
