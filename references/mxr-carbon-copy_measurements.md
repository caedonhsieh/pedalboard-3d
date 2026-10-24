# MXR Carbon Copy (M169) — measurements

Slug: `mxr-carbon-copy`. Exact model: MXR M169 Carbon Copy Analog Delay
(standard dark-green model, not Carbon Copy Mini M299, not Bright, not
10th Anniversary silver). Controls on the real pedal, and only those:
three knobs (REGEN, MIX, DELAY), one top-mounted MOD push-switch with
its own small indicator LED, one effect LED, one round footswitch.
Two internal trim pots exist inside the case; they are not deck
controls and are not modelled.

## References (guide Step 1)

All six views are Dunlop (jimdunlop.com) studio photos of the M169,
fetched with `scripts/fetch_views.py --backend manual` on 2026-10-24.
Each `.jpg` has a matching `.META.txt` with the source CDN URL.

| View | File | Dunlop suffix | What it shows |
|---|---|---|---|
| Top-down (dead-on) | `references/mxr-carbon-copy_hero.jpg` (1280x1280) | 6299 MAIN | Full top face: knob/MOD/LED/print layout |
| Left side | `references/mxr-carbon-copy_left.jpg` (1280x1280) | 6300 LEFT | OUTPUT jack wall, enclosure height |
| Right side | `references/mxr-carbon-copy_right.jpg` (1280x1280) | 6301 RGHT | INPUT jack + 9 V socket wall, CE/9 V sticker |
| Back elevation | `references/mxr-carbon-copy_top.jpg` (1280x1280) | 6302 TOPP | Plain back wall, knob row from behind |
| Front elevation | `references/mxr-carbon-copy_bottom.jpg` (1280x1280) | 6303 BOTT | Front wall, footswitch centred |
| Bottom | `references/mxr-carbon-copy_back.jpg` (1280x1280) | 6304 BACK | Base plate, 4 screws, 4 rubber feet |

File names keep the fetch order; the Dunlop suffix in each `.META.txt`
is the ground truth for which elevation is which. Six views of the
exact pedal: satisfied (top-down, both sides, front, back, bottom).

## Published dimensions (anchor)

- Enclosure preset `mxr_standard` in `parts.js` PRESETS:
  60 x 111 x 32 mm = **2.362 (W) x 4.370 (D) x 1.260 (H) in**, bare
  enclosure, high confidence (Phase 90-class listings). The Carbon
  Copy is repeatedly described as "no bigger than a Phase 90"
  (Dunlop copy) and `verified_mxr_ehx.json` lists
  `MXR | Carbon Copy` at 1.25 in height ("Repeated dealer specs"),
  corroborating the preset height (1.260 vs 1.25 = 0.25 mm).
- Spec `dims` therefore uses the preset verbatim:
  w 2.362, d 4.370, h 1.260, with that source string. Retailer
  footprints such as 2.75 x 4.75 in include jack protrusion and are
  not used, same as the Phase 90 spec.

## Top-down calibration (mxr-carbon-copy_hero.jpg)

- Green-enclosure bbox by colour mask: x 324..928, y 109..1173 px
  (604 x 1064 px). For 2.362 x 4.370 in that is 256 px/in across and
  244 px/in along depth (5% spread: the stencil is a near-ortho
  elevation with mild perspective, not a metrology scan). Mean
  ~250 px/in; 0.04 in is ~10 px. Positions below are quoted to
  0.02 in and flagged where a second view does not corroborate them.
- Mapping: image top = pedal back (-z), image bottom = front (+z),
  image right = pedal right (+x). `x = (u - 0.5) * W`,
  `z = (v - 0.5) * D` with u, v as fractions of the enclosure bbox.
- Knob diameter in frame ~0.88 in (Davies knob, same as Phase 90).

## Component positions (pedal inches; back = -z)

| Part | x | z | Source views |
|---|---|---|---|
| MIX knob | +0.08 | -1.58 | hero (top centre) + back elevation (centre knob highest) |
| REGEN knob | -0.74 | -1.02 | hero (left) + front elevation (left knob) |
| DELAY knob | +0.74 | -1.02 | hero (right) + front elevation (right knob) |
| MOD push-switch (white cap) | -0.50 | -1.82 | hero (pale cap top-left) + left side (cap at back-left of deck) |
| MOD LED (small, clear/blue) | -0.36 | -1.58 | hero (tiny dome below-right of MOD cap); single-view, provisional +-0.06 |
| Effect LED (below MXR logo) | 0.00 | +0.18 | hero + both side views (small dome ahead of footswitch) |
| Footswitch (round chrome) | 0.00 | +0.78 | hero + front elevation (centred) + side views |
| OUTPUT jack (left wall) | left | z -0.30, y 0.65 | hero protrusion + left side (jack centred on wall) |
| INPUT jack (right wall) | right | z -0.30, y 0.65 | hero protrusion + right side |
| 9 V DC socket (right wall) | right | z +0.55, y 0.65 | right side only (black socket forward of INPUT); provisional +-0.1 |

Second-view notes: the back elevation
(`mxr-carbon-copy_top.jpg`, filename keeps fetch order) shows the
three knob caps in a shallow arc with MIX centred and highest,
matching the hero z split (MIX behind REGEN/DELAY). The front
elevation (`mxr-carbon-copy_bottom.jpg`) shows REGEN and DELAY
flanking the footswitch, matching their x split. Side views put both
audio jacks at mid wall height (y ~0.65 of the 1.26 wall) and show
the 9 V socket only on the right wall — there is no back-wall power
jack on this pedal (the back elevation and bottom views show plain
walls/plate). `parts.js` `powerJack()` only builds a back-wall jack,
so the side DC socket is carried as `spec.powerSide` and built by
`mxr-carbon-copy.html`; see the build report's shared-needs list.

Knob pointers in the hero photo all sit at ~12 o'clock
(toward the back), so `rot` is 0.00 / +0.05 / -0.05 for
MIX / REGEN / DELAY (photo read, +-0.1 rad).

## Colours

- Enclosure: dark metallic green powder coat with fine sparkle.
  Colour-mask stats on the hero top face: median #263c15, lit-patch
  mean (G 70..120) #3c5828. Spec uses **#1c5a2c** (dark green;
  `powderCoat()` multiplies a near-white grain map, so the spec hex
  is the rendered base). Sparkle itself is the shared powder grain.
- Print: white throughout (sampled #eef2ee on front lettering).
- Knobs: glossy black Davies-style (shared `mxr` knob). MOD cap:
  translucent pale mint/white (photo ~#cfe8d8, unlit). LEDs: blue on
  the real pedal (Sweetwater: "stage-worthy blue LEDs"); both domes
  photograph clear because the pedal is off. The hero tints the
  shared red LED material to blue in-page (no parts.js edit).

## Print inventory (hero top-down; case as printed)

Top face, all white: `MOD` (left of the MOD cap), `MIX` (below the
MIX knob), `REGEN` (below the REGEN knob), `DELAY` (below the DELAY
knob), boxed `MXR` logo (centre), vertical `OUTPUT` (left edge, by
the OUTPUT jack), vertical `INPUT` (right edge, by the INPUT jack),
`carbon copy` (lowercase rounded sans, front), `analog delay`
(smaller, under it). Right wall: white `CE` / crossed-bin / `9V`
polarity sticker (photographed, not modelled as deck print — it is a
wall sticker, inventoried here so the omission is explicit).
Bottom: embossed MXR mark between the rear feet (not modelled).

## Open / provisional

- MOD LED x/z and the 9 V socket z rest on one clear view each
  (+-0.06 / +-0.1 in). Everything else is in two views.
- Enclosure is the `mxr_standard` preset box; the photos show the
  same shallow rounded box as the Phase 90, so no profile trace is
  needed (guide Step 3, preset first).
