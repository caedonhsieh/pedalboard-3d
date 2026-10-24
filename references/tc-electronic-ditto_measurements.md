# TC Electronic Ditto (original) — measurements

Variant: **original Ditto Looper** (single loop-level knob, one footswitch,
5-minute looper). NOT the Ditto X2 (two footswitches, larger box), NOT the
Ditto X4, NOT the Ditto+ (display + preset storage). All references below are
the original mini Ditto (Thomann product 304324).

## Published dims (anchor scale)

| Source | Value |
|---|---|
| TC Electronic Ditto Looper manual, Technical Specifications | Dimensions 48 × 48 × 93 mm |
| B&H / retailer spec (960801001) | 1.9 × 1.9 × 3.7 in (48 × 48 × 93 mm) |
| Sound House / Rubber Monkey corroboration | 48 × 48 × 93 mm (W × H × D) |

Interpretation: W = 48 mm = 1.890 in, D = 93 mm = 3.661 in, overall
H = 48 mm = 1.890 in **including knob/footswitch**. Bare enclosure height is
derived from the side views (below), not taken as 48 mm.

## Enclosure (side views: side-right, side-left, hero34)

- Flat-top mini box, rounded corners, dark charcoal sparkle powder coat.
  Sampled deck colour (topdown.jpg, lit non-specular patch at px 200,400):
  RGB (57,57,65) ≈ `#393941`. Spec colour `#33343a` (slightly darker so the
  studio key does not wash it to grey-blue).
- Side profile is a rectangle (no wedge): bare box height ≈ 0.66 × overall
  height in side-right.jpg (box wall ≈ 205 px vs knob-top-to-base ≈ 310 px,
  calibrated on published overall H 48 mm) → bare height ≈ 31–32 mm.
  Spec: `h = 1.26 in (32 mm)`, matching the MXR-class mini box height.
  Provisional ±1 mm — flagged in spec notes.
- Base seam: a thin darker base plate line runs around the bottom edge
  (visible in every side view); the shared `basePlate()` covers this.

## Component positions

Calibration (topdown.jpg, 600×600 px studio top view): enclosure spans
≈290 px across (W 1.890 in → 153 px/in) and ≈530 px deep (D 3.661 in →
145 px/in; the difference is mild perspective). Positions use
`z = (v − 0.5) × D`, `x = (u − 0.5) × W`, back = −z (knob end).

| Part | Top view (px, approx centre) | Second view | Spec x, z (in) |
|---|---|---|---|
| Loop level knob | (300, 110) of 600² | detail-knob, hero34 | 0, −1.31 |
| LED (red) | (300, 315) | main, hero34, detail-knob | 0, +0.10 |
| Footswitch (round chrome) | (300, 445) | detail-footswitch | 0, +1.00 |
| INPUT jack (right wall) | right edge, y≈285 | side-right ("input" wall print) | right, z −0.10, y 0.63 |
| OUTPUT jack (left wall) | left edge, y≈255 | side-left, hero34b | left, z −0.31, y 0.63 |
| 9V power + mini-USB | right wall, behind INPUT | side-right, hero34 (black recess) | see Shared needs |

Two-view rule: knob, LED and footswitch are each centred (x = 0) in the
top-down and in both 3/4 views. Jack z positions come from topdown (edge
onsets) cross-checked against side-right/side-left (single jack per wall,
mid-depth, hex nut + washer). Jack height y = 0.63 in is the wall mid-height
in both side views (explicit y is correct for wall parts).

## Knob / switch / LED details

- Knob: single black knob, ≈0.75 in dia (115 px at 153 px/in in topdown),
  white pointer line; pointer at ≈7–8 o'clock in topdown → `rot ≈ −0.6 rad`
  (photo state, provisional). TC mini knobs have a pointer notch, not a
  Davies skirt — closest shared style is `mxr` scaled down (see spec note).
- LED: red dome, lit in every studio view → hero page starts LED ON.
- Footswitch: round chrome plunger on a chrome washer/nut ring
  (detail-footswitch) → shared `footswitch style: round`.

## Print inventory (face, back → front)

| Text | Case/style | Spec z (in) |
|---|---|---|
| `loop level` | lowercase, small, light grey, at back edge above knob | −1.68 |
| `DITTO` | very large bold caps, light grey; the O carries a waveform glyph (vector text approximates it) | −0.55 |
| `LOOPER` | caps, under DITTO, left-aligned block | −0.18 |
| `true bypass` | lowercase small, above footswitch | +0.62 |
| `tc electronic` | lowercase bold brand line at front edge (® small) | +1.55 |

Wall print (not deck): `input` (right wall, below jack), `output` (left
wall), power/USB recess labels on the right wall. The shared library has no
side-wall text or side-wall power builders — see the hero page's local
staging note and Shared needs in the build report.

## Colour

- Enclosure: charcoal sparkle `#33343a` (sample above, darkened for studio).
- Print ink: light grey ≈ `#b9bbbe` (sampled print vs deck contrast in
  topdown.jpg).
- LED lens: red, lit.
