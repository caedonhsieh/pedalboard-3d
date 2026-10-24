# Boss SD-1 Super OverDrive — measurements

Slug: `boss-sd1`. Exact model: Boss SD-1 Super OverDrive (standard yellow
compact, silver-label era as in the Thomann gallery; not SD-1W Waza, not
the black 40th-anniversary edition). Three knobs — LEVEL / TONE / DRIVE —
over the Boss compact treadle. No other controls.

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| True top-down | `references/boss-sd1_top.jpg` (350x621, PNG bytes) | PedalPlayground catalog `boss-sd1.png` via `scripts/fetch_views.py` manual backend |
| Dead-on front | `references/boss-sd1_front.jpg` (600x600) | Thomann gallery `7536078_800.jpg` (Thomann UK Boss SD-1 page, art. 103975) |
| 3/4 hero (right side) | `references/boss-sd1_hero34.jpg` (600x600) | Thomann gallery `7536063_800.jpg` |
| Side profile (INPUT side) | `references/boss-sd1_side-right.jpg` (600x600) | Thomann gallery `7536083_800.jpg` |
| Side profile (OUTPUT side) | `references/boss-sd1_side-left.jpg` (600x600) | Thomann gallery `7536088_800.jpg` |
| Back / top-rear (inverted) | `references/boss-sd1_back.jpg` (600x600) | Thomann gallery `7536068_800.jpg` (pedal photographed upside-down; shows back-wall DC jack + sticker) |

Each `.jpg` has a matching `.META.txt` written by `scripts/fetch_views.py`.
Six views of the exact pedal: satisfied (top-down, front, two sides showing
both jack arrangements, back wall, 3/4). The two Thomann side views are
3/4 elevations, not true orthographic profiles — the enclosure silhouette
itself is therefore carried from the DS-1 measured profile (below), not
re-traced from these photos.

## Published dimensions (anchor)

- Boss SD-1 manufacturer/retailer spec: **73 (W) x 129 (D) x 59 (H) mm**
  = 2.874 x 5.079 x 2.323 in (Thomann, Gear4music, Scan spec tabs all
  agree). Same Boss compact enclosure as DS-1/TU-3.
- Spec `specs/sd1.json` uses w 2.875 to match the measured DS-1 profile
  widths exactly (0.001 in rounding, below validator tolerance). Controls
  corroboration (Thomann description): "Controls: Level, tone and drive".

## Enclosure construction (reused from DS-1, legitimately)

SD-1 is a standard Boss compact: same die-cast body, pivoting treadle,
rubber pad, recess, base plate and toe thumbscrew as the DS-1 measured in
`references/ds1_measurements.md`. The DS-1 measured profiles
(`enclosure.points`, `treadleProfile`, `recessProfile`, `padProfile`,
`baseProfile` in `specs/ds1.json`, Caedon-approved v4, 2026-10-01) are
reused verbatim; only colours change (yellow). Side silhouette, heights
and hinge geometry therefore carry DS-1 provenance, not new guesses.
What is new on SD-1 is only what sits on the flat back deck (LEVEL/TONE/
DRIVE instead of TONE/DIST/LEVEL) and the treadle print.

Pre-fix audit found the SD-1 clone had dropped one enclosure point
(`[-0.835, 1.695]`, the small step on the back deck) present in both
DS-1 and TU-3; restored 2026-10-24 so all three compacts share the
identical 7-point silhouette.

## Top-down calibration (boss-sd1_top.jpg)

- Body width 319 px (yellow extent, mid-body rows) for 2.875 in ->
  111.0 px/in (x). Depth scale 113.4 px/in (y) from the 576 px yellow
  extent; the 2% x/y disagreement is the front face + thumbscrew
  foreshortening in the catalog render, so z values below are
  provisional to ~±0.05 in. Image top = back (-z).
- Knob centres from the dark knob-body centroids (silver-cap centroids
  agree within 8 px):

| Part | x (in) | z (in) | In spec? |
|---|---|---|---|
| LEVEL knob (left, large) | -0.69 | -1.83 | spec (-0.678, -1.901) — agree < 2 mm, kept |
| DRIVE knob (right, large) | +0.68 | -1.84 | spec (+0.695, -1.894) — agree < 2 mm, kept |
| TONE knob (centre, small) | -0.02 | -1.35 | spec (0.000, -1.352) — agree, kept |
| CHECK LED (red dot) | +0.03 | -2.29* | spec (0.000, -2.100) — *absolute z shifted by the back-edge crop guess; the LED sits 0.20 in in front of the CHECK print in both photo and spec, kept |

Kept spec x/z are the DS-1 chassis drilling (same holes on every Boss
compact) and match this photo inside measurement noise; moving them to
single-photo values would trade a triangulated position for a noisier
one. What the photo *does* settle beyond doubt is identity and size:
LEVEL left / DRIVE right are the large fluted knobs, TONE centre is
the small smooth knob — the pre-fix spec had the large/small styles
swapped (see fix log).

- Knob outer diameter (dark bbox): ~88 px = 0.79 in = 20.1 mm for the
  two large knobs (spec `boss` builder ~19.6 mm + shadow — agree).
  Centre TONE cap is visibly narrower (spec `boss-smooth` with
  `diaScale` 0.85, as on the DS-1 centre knob).
- Side-jack height y 1.094 in reused from DS-1 (same wall, same jack
  hardware; corroborated in both Thomann side views). Jack z = 0.0
  (mid-wall) is consistent with the side views. Left = OUTPUT,
  right = INPUT, confirmed by the treadle print arrows.
- Back wall (`boss-sd1_back.jpg`): single centred DC 9V input jack,
  low on the back face (spec `powerJack` x 0, y 0.56, style round —
  style restored to match DS-1). Toe thumbscrew centred on the
  treadle toe (spec r 0.15 restored to DS-1 hardware size).

## Colours

- Enclosure/treadle yellow: lit non-specular deck patch of
  `boss-sd1_top.jpg` samples #e5cc4f (median RGB 229, 204, 79).
  Spec uses #f0d060 (240, 208, 96) — one step lighter so the powder
  texture (near-white multiply + bump) lands on the sampled yellow
  under studio light rather than going mustard-dark. Print ink black.
- Rubber pad #1a1a1c, base #8a8d92 (as DS-1). Recess (under-treadle
  shadow well) darkened 2026-10-24 from #907030 to #6b5518 so it reads
  as shadowed depth on yellow, mirroring the DS-1 recess fix.

## Print inventory (top + front; case as printed)

Deck (black, fixed): `CHECK` (above LED), `TONE` (centred, behind the
centre knob), `LEVEL` (forward of left knob), `DRIVE` (forward of
right knob). Each knob has a single index dot on the deck.
Treadle (black, moves with treadle): `<- OUTPUT` (left),
`INPUT <-` (right, arrow points left toward centre in top view),
`SUPER` (line 1), `Over Drive` (line 2, two words, capital O and D),
`SD-1` (below right). Pad: embossed `BOSS` (in pad decal, as DS-1).

Decal fix 2026-10-24: `textures/sd1_treadle_decal.png` previously set
`SUPER OverDrive` on one line; regenerated to the two-line
`SUPER` / `Over Drive` stack with `SD-1` below-right, matching both
the top-down and front references. `textures/sd1_pad_decal.png` added
(BOSS pad logo, same art geometry as DS-1) and wired as `padDecal`;
without it the pad rendered blank.

## Open / provisional

- Knob/LED z from a single top view (±0.05 in); enclosure/treadle
  geometry is DS-1-measured, not re-measured for SD-1.
- `surfaceY` values on knobs/labels are the baked DS-1 deck heights;
  valid because the deck profile is shared verbatim.
