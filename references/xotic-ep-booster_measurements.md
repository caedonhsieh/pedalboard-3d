# Xotic EP Booster — measurements

Slug: `xotic-ep-booster`. Exact model: Xotic EP Booster (standard black
mini boost, not the limited blue/purple/red editions). Single clear gain
knob, blue status LED, round true-bypass footswitch.

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| True top-down | `references/xotic-ep-booster_topdown.jpg` (350x681 PNG) | PedalPlayground catalog `xotic-ep.png` via `scripts/fetch_views.py` |
| Dead-on front (product render) | `references/xotic-ep-booster_front.jpg` (280x489 PNG) | Xotic official `img/ep-booster-280x489.png` |
| 3/4 hero | `references/xotic-ep-booster_hero.jpg` | Xotic official `img/ep-hero1.jpg` |
| Print close-up | `references/xotic-ep-booster_detail1.jpg` | Xotic official `img/EP_detail-1.jpg` |
| Front 3/4 (switch + jacks) | `references/xotic-ep-booster_detail2.jpg` | Xotic official `img/EP_detail-2.jpg` |
| IN jack close-up | `references/xotic-ep-booster_detail3.jpg` | Xotic official `img/EP_detail-3.jpg` |
| Clear knob close-up | `references/xotic-ep-booster_detail4.jpg` | Xotic official `img/EP_detail-4.jpg` |
| Footswitch close-up | `references/xotic-ep-booster_detail5.jpg` | Xotic official `img/EP_detail-5.jpg` |
| Interior / DC + DIP | `references/xotic-ep-booster_detail6.jpg` | Xotic official `img/EP_detail-6.jpg` |
| Annotated parts diagram | `references/xotic-ep-booster_parts.jpg` | Xotic official `img/ep-parts.jpg` |

Each `.jpg` has a matching `.META.txt` from `scripts/fetch_views.py`
(manual backend). Ten views of the exact pedal: satisfied (top-down,
front, hero 3/4, jack/knob/switch details, parts diagram). Image files
keep the `.jpg` extension from the fetch script; `topdown`/`front`
payloads are PNG (see file magic).

## Published dimensions (anchor) — staging entry verified

`data/spec_sheets_staging.json` EP Booster entry (verified, official
product page `https://xotic.us/effects/ep-booster/`):

> Dimensions (W/D/H): 3.5 x 1.5 x 1.5 in (89 x 38 x 38 mm)

The manufacturer's W/D labels are rotated relative to the physical
pedal: the 3.5 in side is the front-back length (knob at the back to
footswitch at the front), the 1.5 in side is left-right. Verified
against both top-down views: the footprint is a narrow 1:2.33
rectangle with the knob/footswitch on the long axis. Axis-remapped
physical convention used in the spec:

- `w` (x, left-right) = **1.50 in** (38.1 mm)
- `d` (z, back `-z` knob side to front `+z` switch side) = **3.50 in** (88.9 mm)
- `h` (y, bare enclosure) = **1.50 in** (38.1 mm), `height_includes_knobs: unknown`

Corroborated by Reverb/dealer spec tabs repeating 3.5 x 1.5 x 1.5 in.
Height note: the published 1.5 in is adopted as the bare-enclosure
height. The hero/detail photos show a deep mini box whose side wall
is comparable to its 1.5 in width, with the knob adding ~0.35 in and
the footswitch ~0.45 in above the deck, so treating 1.5 in as the
overall knob-inclusive height would make the box implausibly shallow.
Flagged provisional: if the 1.5 in proves knob-inclusive, lower `h`
by ~0.35 in and re-run validation (deck parts reseat automatically).

## Calibration

- `topdown.jpg` (PedalPlayground photo): body x 36–313 px (278 px)
  → 185 px/in across; full height 681 px → 195 px/in along depth.
  ~5% anamorphic difference; z positions use the depth scale, x
  positions the width scale, each normalised to its own body edge.
  Image top = back (`-z`). Side-jack protrusions extend beyond the
  body in x (rows y≈350/450) and are excluded from the body bbox.
- `front.jpg` (Xotic render): body x 17–262 px (246 px), y 13–476 px
  (464 px) → 164 px/in across, 133 px/in along depth. The render is
  vertically squashed (drawn ratio 1.89 vs true 2.33), so it
  corroborates ordering and the LED (below) but knob/footswitch z
  from this view alone would be biased; spec z averages both views
  weighted to the photo.

## Component positions (two views where possible)

All x/z in inches, origin at pedal centre, back `-z`. Knob/LED/switch
carry no `y` in the spec (they seat via `surfaceAt()` on the flat
deck, h = 1.50 in).

| Part | x | z | Source |
|---|---|---|---|
| Gain knob (clear) | 0.00 | -0.93 | topdown centre (174 px, ~170 px) → z -0.88; front centre (140 px, 115 px) → z -0.98; averaged -0.93 |
| Blue LED | 0.00 | -0.28 | topdown blue-core centroid (174, 285) → -0.283; front blue-core centroid (135, 207) → -0.283. Two-view agreement <0.01 in |
| Footswitch (round) | 0.00 | +1.20 | topdown chrome centre (~174, 585) → +1.26; front centre (140, 395) → +1.14; averaged +1.20 |
| INPUT jack (right wall, `+x`) | right | -0.30 | topdown protrusion y≈285 → -0.28; front jack y≈200 → -0.34. Detail2/3 confirm IN is the rear jack |
| OUTPUT jack (left wall, `-x`) | left | +0.35 | topdown protrusion y≈415 → +0.39; front jack y≈270 → +0.19 (squashed render, low weight); parts diagram + detail2 confirm OUT is forward of IN. Provisional ±0.10 in |
| DC jack (back wall, `-z` face) | 0.00 | back wall | `+ -C- -` polarity print centred on the back edge in both top views; parts diagram arrow to the back edge; detail6 shows the barrel at the back end. y 0.85 provisional single-view |

Jack wall height y = 0.75 in (mid-wall on the 1.50 in box; detail3
shows the IN barrel centred vertically on the side wall). Provisional.

Knob size: clear disc ≈ 140 px across in topdown → ~0.76 in diameter
(≈51% of the 1.50 in width). The library `mxr` Davies knob (0.92 in)
is scaled `diaScale 0.82` / height `scale 0.85` in the spec. Pointer
points to the back (12 o'clock, rot 0) in both top views.

Footswitch: chrome washer + hex nut + cylindrical plunger (detail5),
same construction as the library `round` switch; no scaling.

## Enclosure

Custom mini box (no `PRESETS` entry fits 38 x 89 mm). Spec uses
`enclosure.type: "box"` with per-model `dims` overriding any preset,
`edgeRadius 0.06`. Top face is gloss black with a thin silver pinstripe
border inset ~0.06 in from the edge (both top views; hero shows the
border catching light). Side walls are dark brushed metal (hero:
charcoal-grey, vertically brushed). The single-colour box builder
renders both as near-black `#141518`; the pinstripe is print (see
below) rather than geometry. No top screws; the four case screws are
on the bottom plate (parts diagram) and are not modelled.

## Colours

- Top face: black, lit non-specular patch ≈ `#0c0c0e` (topdown centre
  field). Spec enclosure `#141518` so the side walls read as the
  charcoal in the hero instead of pure void black.
- Print: white/silver-white (all lettering; detail1 shows matte white
  ink). Spec labels use `#f2f2f2`.
- LED: blue (both top views show a lit blue dot; parts diagram labels
  it "On/Off status led"). The library `led()` is red — the hero page
  retints the lens/glow blue locally; see the build report.
- Knob: clear transparent acrylic over a dark centre post (detail4).
  The library knob is opaque black — the hero page makes it
  transparent locally; see the build report.
- Hardware (footswitch, jack nuts/barrels): bright chrome/nickel
  (detail3/5).

## Print inventory (topdown + front + detail1; case as printed)

- Back edge, centred: `+ -C- -` DC polarity symbol (plus, centre-negative
  barrel glyph, minus). Modelled as the text `+ -C- -`.
- `EP` — very large script/brush lettering, centred, upper-middle
  (the E is drawn as a reversed/brush form; modelled as script `EP`).
- `-booster` — script, directly under `EP`, the dash leading.
- `BY xotic usa` — small sans capitals (`xotic` lower-case as printed),
  under `-booster`, right-aligned to the script block.
- `IN` — vertical (rotated 90°) on the right edge beside the INPUT
  jack, reading bottom-to-top.
- `OUT` — vertical on the left edge beside the OUTPUT jack.
- No other top print. No knob tick ring on the real pedal (the clear
  knob has a single black pointer line; no printed scale).

## Open / provisional

- OUTPUT jack z (±0.10 in): the two views disagree because the front
  render is squashed; the photo value dominates.
- DC jack y (0.85 in) and side-jack y (0.75 in) are single-view
  estimates; x/z of every deck part is two-view.
- Bare-vs-overall height (see above): 1.50 in adopted as bare.
