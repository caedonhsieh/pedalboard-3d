# ProCo Rat 2 — measurements

Slug: `proco-rat2`. Exact model: current-production ProCo RAT 2 (black steel
case, three knobs DISTORTION / FILTER / VOLUME, LED inside the `A` of the RAT
wordmark, back-wall IN / 9V-DC / OUT). Not the vintage big-box RAT, Turbo RAT,
or RAT2 variants with side jacks.

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| Front / top elevation | `references/proco-rat2_front.jpg` (750x913) | Sweetwater product gallery main image (`Rat2`) |
| Back wall | `references/proco-rat2_back.jpg` (750x637) | Sweetwater closeup `750-Rat2_detail1.jpg` |
| Front-top (ProCo wall) | `references/proco-rat2_fronttop.jpg` (641x750) | Sweetwater closeup `750-Rat2_detail3.jpg` |
| Side A | `references/proco-rat2_side1.jpg` (750x556) | Sweetwater closeup `750-Rat2_detail5.jpg` |
| Side B | `references/proco-rat2_side2.jpg` (750x549) | Sweetwater closeup `750-Rat2_detail6.jpg` |
| 3/4 beauty | `references/proco-rat2_hero34.jpg` (750x737) | Sweetwater closeup `750-Rat2_detail2.jpg` |

Each `.jpg` has a matching `.META.txt` written by `scripts/fetch_views.py`
(manual backend, manufacturer/retailer CDN URLs above). Six views of the exact
pedal — top/front, back, front wall, both sides, 3/4: satisfied.

## Published dimensions (anchor)

- `data/spec_sheets_staging.json` (verified, secondary): 3.5 x 4.0 x 2.5 in
  (88.9 x 101.6 x 63.5 mm), retailer listing corroborated by the eBay product
  catalog. Axis mapping D x W x H in the listing read as W 3.5, D 4.0, H 2.5.
  ProCo publishes no dimensions (official manual carries none).
- `data/heights.json` "Pro Co | Rat 2": PedalPlayground footprint 3.5 x 4.13 in
  (the 4.13 includes back-jack protrusion; the case depth is the published 4.0).
- `height_includes_knobs` is "unknown" in staging, so the bare-enclosure
  heights were resolved from the side photos below. The side measurement
  (back 2.48 in) corroborates the published 2.5 in as the bare back height.

## Side profile (side1, 750x556; side2 agrees)

- Case depth in frame: x ~10 to ~745 px = 735 px for 4.0 in -> 184 px/in.
- Bottom edge y ~542 px. Back top y ~86 px -> bare back height
  (542-86)/184 = **2.48 in**. Mid top (x 350) y ~130 px -> 2.24 in.
  Front top y ~180 px -> bare front height (542-180)/184 = **1.97 in**.
- The top is a **single straight slope** from back to front (midpoint lies on
  the back-front line), like the EHX big box. Enclosure profile
  (back -z to front +z): `[[-2.0, 2.48], [2.0, 1.97]]`.
- Construction: folded black steel case; top face glossy black, side walls
  black crackle texture (lighting makes them read mid-grey in photos).
- Knob above deck (at knob x): deck y ~115 px, knob top y ~10 px ->
  ~0.57 in above the local deck. Footswitch top ~0.27 in above deck.
- Rubber feet below the base are visible in side/back views; the shared
  `basePlate` stands in for the base (feet not separately modelled, as on
  every other hero).

## Top layout (front view, planar homography)

Deck corners (32,36) (718,36) (730,850) (20,850) px mapped to
x -1.75..1.75 in, z -2.0 (back) .. +2.0 (front); 196 px/in across the back edge.

| Part | x (in) | z (in) | Notes |
|---|---|---|---|
| DISTORTION knob | -1.02 | -0.76 | homography (-1.01, -0.76), symmetrised |
| FILTER knob | 0.00 | -0.76 | centre knob (homography +0.02) |
| VOLUME knob | +1.02 | -0.76 | homography (+1.04, -0.76), symmetrised |
| Label strip centre | 0.00 | -1.40 | DISTORTION/FILTER/VOLUME boxes at the back edge |
| RAT box centre | 0.00 | +0.16 | box x -1.10..+1.14, z -0.19..+0.51 (2.24 x 0.70 in) |
| LED (red) | 0.00 | +0.16 | inside the counter of the `A` in RAT (lit in front view, grey triangle unlit in 3/4 views) |
| Footswitch (round) | 0.00 | +1.23 | centred chrome stomp (homography +0.01, +1.23) |

- Knob diameter 0.76 in (150 px), tick-arc diameter 0.96 in (r 0.48 in).
  Black ribbed knobs, flat tops, white pointer line at 12 o'clock in photos
  (`rot: 0`).
- Knob/LED/switch were read from the front elevation and corroborated in the
  two 3/4 views and fronttop view. No top screws are visible on the deck
  (folded-steel case) — none modelled.

## Back wall (back view, viewed from behind)

Viewed from behind, image-left is the pedal's right (+x). Calibration:
case width ~694 px for 3.5 in -> ~200 px/in; wall bottom y ~540 px.

| Part | x (in) | y (in) | Notes |
|---|---|---|---|
| IN jack | +0.88 | 0.72 | image-left bore centroid (207, 398) px, mirrored to +x; right in top view |
| OUT jack | -0.88 | 0.72 | image-right bore centroid (558, 400) px -> -x; left in top view |
| 9V-DC power | 0.00 | 0.72 | centre bore (379, 406) px; round black barrel |
| Back print row | as above | ~1.09 | `IN` / `9V-DC` (+ polarity mark) / `OUT` boxes above the jacks |

Single-view (back) positions: jack x/y are provisional to ~0.05 in; the
left/right assignment is confirmed by the print (`IN` image-left = +x).

## Front wall (fronttop view)

- `Pro Co` stacked white logo centred on the front (+z) wall, roughly
  mid-height (y ~1.0 in, provisional, single view). The shared library has
  no front-wall label, so the hero page stages this one print locally and
  the spec carries no front label (see spec notes).

## Print inventory (front + back + fronttop views)

- Back edge of deck, white-outlined boxes: `DISTORTION`, `FILTER`, `VOLUME`
  (white caps, one above each knob; dividers above the gaps between knobs).
- White tick arc (~300 deg, 5 radial ticks) around each knob, r 0.48 in.
- Centre: `RAT` in large white block letters inside a white outline box
  (2.24 x 0.70 in); the LED shines through the `A` counter.
- Front wall: `Pro Co` stacked logo, white.
- Back wall: `IN`, `9V-DC` with `+ -o- -` polarity diagram, `OUT`, white,
  in outlined boxes above the jacks.
- No other print. No deck screws.

## Colours

- Enclosure: black steel, top near-black glossy (~#1a1a1c sampled from the
  lit deck away from speculars); side crackle reads lighter only from
  texture lighting. Modelled as one black powder coat `#1a1a1c`.
- Print: white (~#f5f5f5). Knobs black; footswitch/jacks chrome;
  LED red (in the `A`).
