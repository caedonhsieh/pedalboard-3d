# Klon Centaur (original gold, "horsey") — measurements

Slug: `klon-centaur`. Exact model: original Klon Centaur in the gold
finish with the centaur ("horsey") graphic — Bill Finnegan-built
production Centaur (c. 1994–2009), custom cast enclosure, oxblood knobs.
This is **not** the silver Centaur, **not** the Klon KTR (different,
smaller enclosure and layout), and **not** any klone (Warm Audio Centavo,
RYRA, etc. — used below only as dimensional corroboration, never as a
visual reference).

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| Top-down | `references/klon-centaur_top.jpg` (350x271, PNG bytes in .jpg) | PedalPlayground catalog, `klon-centaur-gold.png` (gold top-down ground truth) |
| 3/4 hero | `references/klon-centaur_hero.jpg` (1500x2250) | Walt Grace Vintage, 1999 Klon Centaur Gold #2533, `IMG_8317.jpg` |
| Detail, GAIN/LED/centaur left | `references/klon-centaur_detail-gain.jpg` (1500x2250) | Walt Grace Vintage #2533, `IMG_8332...jpg` |
| Detail, OUTPUT/footswitch/CENTAUR | `references/klon-centaur_detail-output.jpg` (1500x2250) | Walt Grace Vintage #2533, `IMG_8333...jpg` |
| Back wall (IN / OUT / 9V) | `references/klon-centaur_back.jpg` (1500x2250) | Walt Grace Vintage #2533, `IMG_8322.jpg` |
| Front wall (footswitch side) | `references/klon-centaur_front.jpg` (1500x2250) | Walt Grace Vintage #2533, `IMG_8324...jpg` |
| Underside label | `references/klon-centaur_bottom.jpg` (1500x2250) | Walt Grace Vintage #2533, `IMG_8356...jpg` |

Fetched 2026 via `scripts/fetch_views.py --backend manual` (see the
matching `.META.txt` files). Four-plus views of the exact pedal:
satisfied (top, 3/4 hero, both knob details, back, front, bottom).
Identity check in every view: champagne-gold cast box, three oxblood
knobs in a back row, red LED, centaur line graphic front-left,
`CENTAUR™` front-right of the footswitch, back-wall IN/OUT/9V. The
silver PedalPlayground variants (`klon-centaur`, `klon-centaur-horsey`
in silver) were inspected and **rejected** — wrong finish.

## Published dimensions (anchor) — CONFLICTING SOURCES, flagged

Klon published no spec sheet (company closed 2008), so there is no
manufacturer W×D×H. The sources disagree; they are flagged here
instead of being silently averaged:

- **Adopted anchor — dealer measurement, verified in repo staging**
  (`data/spec_sheets_staging.json`, Reverb listing 90989796, opened and
  verified): "Length is 5 in., 6 5/8 in. width, and 2 in. in depth at
  deepest point." Mapped as **W 6.63 x D 5.00 x H 2.00 in**
  (168.3 x 127.0 x 50.8 mm). Caveat recorded in staging: "Length"
  mapped to depth; "depth at deepest point" mapped to height is
  interpretive; knob inclusion unstated. Secondary source.
- **Footprint corroboration** (`data/heights.json`, PedalPlayground):
  footprint **6.50 x 5.03 in**, consistent with the adopted 6.63 x 5.00
  within cropping/measurement tolerance (~2%). Its height 1.87 in is
  an enclosure inference from a Strymon enclosure, **not a Klon
  measurement — rejected for height.**
- **Clone corroboration only** (Warm Audio Centavo, a faithful
  reproduction of this pedal): **6.75 x 5.00 x 2.25 in** (Perfect
  Circuit / retailer listings). Corroborates the footprint (W within
  0.12 in). Its 2.25 in is overall height including knobs, so it must
  not be used as the bare-enclosure height.
- **Conflict summary:** W spans 6.50–6.75 in across sources; H spans
  1.87 (inferred, rejected) / 2.00 (dealer, adopted) / 2.25 (clone
  overall, knob-inclusive). The spec adopts W 6.63, D 5.00 from the
  verified dealer listing, and resolves the **bare** enclosure height
  from the calibrated back photo below (1.98 in max), which is
  consistent with the dealer's 2.00 in as a bare/deepest figure and
  with the clone's 2.25 in overall once the ~0.3–0.45 in knob height
  above the deck is added. `specs/klon-centaur.json` `dims.source`
  carries this provenance.

Coordinates: inches; x across (origin centre), back (knob side) = −z,
front (footswitch side) = +z, y up from base. Deck parts never carry
y — they seat via `surfaceAt()` (spec-schema).

## Top-view calibration (klon-centaur_top.jpg, 350x271)

The PedalPlayground frame is cropped essentially to the footprint:
full frame ≈ W × D. Calibration: 350 px / 6.63 in = **52.8 px/in**
across; 271 px / 5.00 in = **54.2 px/in** along depth. The ~2.5%
anisotropy is the photo crop/perspective — positions below are read
with `x = (u−0.5)·W`, `z = (v−0.5)·D` (v=0 at image top = back),
then symmetrised where the hardware is visibly symmetric. Dark-blob
centroids were measured programmatically on the image (oxblood knobs
are near-black against the gold), not eyeballed:

| Part | blob cx, cy (px) | x (in) | z (in) | Notes |
|---|---|---|---|---|
| GAIN knob | 64.4, 63.1 (bbox 31–87 x 31–91) | −2.10 | −1.33 | left knob |
| TREBLE knob | 177.4, 64.0 (bbox 146–201) | +0.05 | −1.32 | centre knob |
| OUTPUT knob | 291.4, 64.9 (bbox 263–317) | +2.20 | −1.31 | right knob |
| LED (red) | 24.7, 105.4 (red mask) | −2.85 | −0.55 | left of GAIN label, forward of knob row |
| Footswitch | ~226, ~210 (silver highlight cluster) | +0.95 | +1.35 | provisional — highlight centroid, corroborated in hero/detail views |

Symmetrised for the spec (outer knobs are equidistant from TREBLE on
the real pedal): GAIN −2.10, TREBLE +0.05, OUTPUT +2.20, all at
z = −1.32. Knob blob diameter 55–57 px ≈ **1.05–1.10 in** (oxblood
tapered knob, glossy domed top, fine-knurled skirt, small pointer
notch at the rim — see detail views). Knob height above deck
~0.4–0.5 in (detail/back views; provisional, single-scale estimate).
LED/footswitch positions were cross-checked in the Walt Grace hero
and detail views (LED left of GAIN, footswitch front-right of the
centaur graphic) — same layout, second view satisfied for the knobs,
LED and footswitch; exact sub-0.1 in values rest on the top view.

## Side profile (back + front + hero/detail views)

There is no true lateral (side-on) studio view in the set; the
profile is triangulated from the back view, the front view, and the
two 3/4 details, and is **flagged provisional where single-view**:

- **Back view (klon-centaur_back.jpg, 1500x2250):** pedal width in
  frame ≈1190 px for 6.63 in → ~179 px/in. Gold back-wall height
  ≈355 px → **bare back height ≈1.98 in**, matching the dealer 2.00 in.
  The back wall is near-vertical with a bevelled top edge; IN, OUT
  and the 9V jack sit on this wall (below).
- **Front view (klon-centaur_front.jpg):** front wall is shorter
  than the back wall; the deck falls gently toward the footswitch.
  Combined with the hero/detail views (front lip visibly lower than
  the back deck), the top is modelled as a **single gentle straight
  slope: 1.98 in at the back (−2.50) to 1.70 in at the front (+2.50)**
  — a 0.28 in fall over 5.00 in, far shallower than the Big Muff's
  wedge. Adopted enclosure points (back to front):
  `[[-2.50, 1.98], [2.50, 1.70]]`. The cast box also has a stepped
  perimeter flange (visible in hero/detail: a narrower upper deck
  over a wider base with a shadow groove); `profileEnclosure`
  extrudes a constant width, so the flange step is **not** modelled
  in silhouette — noted as a known simplification, invisible to
  validator check C (which compares the z–y silhouette only).
- Enclosure construction: one-piece gold cast box, fine metallic
  flake, rounded corners (bevel 0.06 in), black base plate beneath.

## Back wall (klon-centaur_back.jpg, viewed from behind)

Audio and power are on the **back face**, not the side walls.
Viewed from behind, image-left is the pedal's right (+x). Reading the
jacks left-to-right in the photo and flipping to pedal coords:

| Jack | pedal x (in) | y (in) | Notes |
|---|---|---|---|
| IN (input) | +1.05 | 0.95 | image-left; pedal right, as conventional |
| OUT (output) | −0.80 | 0.95 | centre-right in image |
| 9V power | −1.90 | 0.95 | small round barrel, image-far-right |

Labels `IN`, `OUT`, `9V` are printed in dark serif caps directly
above each jack on the back wall. Jack row height y ≈0.95 in
(mid-wall on the 1.98 in back face; single-view, provisional).
In the spec, IN/OUT use `face: 'back'` jacks and the 9V barrel uses
`powerJack` (also back-wall in `parts.js`), so all three sit on the
same wall as photographed.

## Colours (sampled)

- **Enclosure gold:** sampled from lit, non-specular patches —
  PedalPlayground top mid-deck `#c07804` (shaded albedo) and Walt
  hero `#dea452` / highlight `#f0bd6e` (lit). Adopted spec colour
  **`#c9972f`** (mid-albedo champagne gold between the shaded and
  lit samples; the studio ACES tone mapping lifts it toward the lit
  sample at the hero angle). Fine metallic speckle in the photos is
  represented by the shared powder-coat grain.
- **Knobs:** oxblood / dark maroon-brown, glossy — sampled dark
  maroon (near `#3d1210` in shadow, deep red-brown highlight).
  Modelled with the closest `parts.js` knob (see spec notes; the
  library knob is black — a reusable oxblood tapered knob builder
  is listed as a follow-up, not edited here).
- **Print ink:** dark brown-black serif (labels/centaur), red LED
  lens, chrome footswitch and jack hardware, silver/nickel jack nuts.

## Print inventory (top + back + underside)

Top face (all in the decal — serif lettering + line art that vector
labels cannot reproduce):

- `GAIN` — serif caps, under the left knob (front of it), dark ink.
- `TREBLE` — serif caps, under the centre knob.
- `OUTPUT` — serif caps, under the right knob.
- Centaur line graphic — outlined centaur (man's torso/head/beard,
  horse body/legs/tail, sword in raised right hand, left arm
  extended) front-left of centre, approx x −2.9…−0.3, z −0.1…+1.6,
  thin dark outline, no fill.
- `CENTAUR™` — serif caps to the right of the footswitch.
- Red LED left of `GAIN`. No `KLON` wordmark on the top of the gold
  horsey version (the silver version's `KLON` top print does not
  apply here).

Back wall: `IN`, `OUT`, `9V` serif caps above the jacks. Inventoried
here; omitted from `specs/klon-centaur.json` `labels[]` because
`validate.html` `expectedPos()` has no `face: 'back'` label case
(any back label fails check A with a deck-height/NaN expectation
even though `parts.js` positions it correctly) — see the spec
`notes` and the build report's shared-file list.

Underside (photographed, **not modelled** — it is the pedal's bottom
and never visible in the hero views): gold foil label reading
`CENTAUR™ / PROFESSIONAL / OVERDRIVE / KLON / PHONE: (617) 666-1551 /
WWW.KLON-SIBERIA.COM` in red serif on the black base plate.

Knob pointers: each oxblood knob has a small moulded pointer notch
at its rim (visible at approx 12 o'clock in the top view); spec `rot`
values reproduce that orientation (approx 0 rad = pointing back).
