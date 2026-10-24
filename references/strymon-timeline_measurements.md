# Strymon TimeLine — measurements

Slug: `strymon-timeline`. Exact model: Strymon TimeLine Multidimensional
Delay (original big-box, graphite finish) — **not** TimeLine MX, **not**
Mobius/BigSky (same enclosure family, different print/controls).

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| Top-down (cropped, upper deck) | `references/strymon-timeline_topdown.jpg` (1600x714) | Strymon official `timeline_topdowncrop_1600.jpg` |
| Full top-down | `references/strymon-timeline_top.jpg` (800x579) | PedalPlayground catalog `strymon-timeline.png` |
| 3/4 front (knobs/switches) | `references/strymon-timeline_hero34.jpg` (1024x751) | Strymon official `TimeLine_knobs_1600-1024x751.jpg` |
| Rear 3/4 (back panel) | `references/strymon-timeline_rear.jpg` (1024x719) | Strymon official `TimeLine_Rear_knobs_1600-1024x719.jpg` |

Fetched via `scripts/fetch_views.py --backend manual` (see matching
`.META.txt` files). Identity check in every view: graphite wide box,
green LED display top-left, VALUE/TIME/REPEATS/MIX top row,
FILTER/GRIT/SPEED/DEPTH second row, TYPE encoder left with 12 machine
names around it, `strymon. TIMELINE` centre print, three chrome
footswitches (A / B / TAP) along the front edge.

## Published dimensions (anchor) — conflicts flagged

- **Adopted:** Strymon TimeLine manual (repo `verified_strymon_jhs_walrus.json`,
  hand-verified): **W 6.75 x D 5.00 x H 1.87 in**. H is the published
  overall height; knob inclusion unstated there.
- Strymon product page: 6.75 wide x 5.1 deep x 2.7 tall in. The 2.7 in
  is overall including knobs/switches and is **not** used as bare H;
  the 5.1 vs 5.0 deep delta (0.1 in) is flagged, manual value adopted.
- Product-intro sheet (Thomann PDF): "Height is 1.3 in (front) and
  1.9 in (rear)" — corroborates a sloped enclosure, rear ≈ adopted
  1.87 in. Spec profile therefore uses back 1.87 / front 1.30 in.

Coordinates: inches; x across (origin centre), back (knob side) = −z,
front (footswitch side) = +z, y up from base. Deck parts never carry
y — they seat via `surfaceAt()` (spec-schema).

## Top-view positions (two views)

Read from the full top view (`strymon-timeline_top.jpg`, pedal bounds
≈ full frame; `x=(u−0.5)·W`, `z=(v−0.5)·D`, v=0 at image top = back)
and cross-checked against the cropped official top-down
(`strymon-timeline_topdown.jpg`, same layout at higher resolution).
Agreement between the two views is within ~0.1 in on every knob.

| Part | x (in) | z (in) | Views |
|---|---|---|---|
| LED display (centre) | −2.03 | −1.80 | top + topdown |
| VALUE knob | −0.44 | −1.75 | top + topdown |
| TIME knob | 0.57 | −1.75 | top + topdown |
| REPEATS knob | 1.45 | −1.75 | top + topdown |
| MIX knob | 2.33 | −1.75 | top + topdown |
| TYPE encoder | −2.33 | −0.40 | top + topdown |
| FILTER knob | −0.17 | −0.30 | top + topdown |
| GRIT knob | 0.78 | −0.30 | top + topdown |
| SPEED knob | 1.72 | −0.30 | top + topdown |
| DEPTH knob | 2.60 | −0.30 | top + topdown |
| LED A (amber, lit in photo) | −2.94 | 0.80 | top only — provisional |
| Footswitch A | −2.90 | 1.60 | top + hero34 |
| Footswitch B | 0.24 | 1.60 | top + hero34 |
| Footswitch TAP | 2.87 | 1.60 | top + hero34 |

Enclosure colour sampled from a lit, non-specular mid-panel patch of
`hero34`: graphite ≈ `#3a3d42` (spec `enclosure.color`).

## Print inventory (from top + topdown)

Display `705mS`-style green readout; `VALUE push (param) hold (global)`;
`TIME REPEATS MIX FILTER GRIT` + `SPEED —MOD— DEPTH`; TYPE ring:
`REVERSE PATTERN DUAL DIGITAL dBUCKET dTAPE ICE DUCK SWELL TREM FILTER
LO-FI` (12 machines) + `TYPE push (bank/time) hold (save)`;
`strymon.` script + `TIMELINE` wordmark; switch print `A / B / TAP`,
`REC/DUB — BANK DOWN`, `PLAY — BANK UP`, `STOP hold (looper)`.
Spec `labels[]` carries the principal words; the 12 tiny TYPE-ring
names are inventoried here and rendered as labels where legible.

## Shared-library gaps (not edited — reported)

- `assemblePedal()` supports **one** `footswitch` and **one** `led`.
  Spec carries footswitch A + LED A; the hero page stages B/TAP
  switches and their LEDs locally from the shared `footswitch()` /
  `led()` builders. A multi-switch spec field is the shared fix.
- No LCD builder exists. The display is a spec `label` with a dark
  `bg` and green text (lit readout, no working UI), per brief.
- Back panel on the real pedal (stereo IN/OUT pairs, EXP, MIDI
  IN/OUT, 9V) exceeds the one-`powerJack` + side/back-jack model;
  spec carries one IN, one OUT, one 9V on the back wall.
- No smooth metal encoder knob style exists; `mxr` Davies knobs are
  the closest library approximation (noted in spec knob notes).
