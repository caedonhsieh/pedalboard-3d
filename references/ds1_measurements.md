# Boss DS-1 Measurements

Triangulated from multiple reference views. All values in mm unless noted.
Absolute scale anchored to published dims: **73 W × 129 D × 59 H mm**
(2.875 × 5.079 × 2.323 in).

## Reference views

| File | View | Source |
|---|---|---|
| `ds1_top.png` | Top-down | PedalPlayground catalog |
| `ds1_side_yahoo.jpg` | True side profile | Yahoo Auctions listing |
| `ds1_side_candidate1.jpg` | Close 3/4, footswitch detail | yayastation.com |
| `ds1_34_candidate1.jpg` | Full 3/4 | richtonemusic.co.uk |
| `boss_side_ch1.jpg` | Front (CH-1, same enclosure) | session.de |

## Enclosure side profile (from ds1_side_yahoo.jpg)

Side view: left = front of pedal, right = back. Pedal depth 129mm spans the frame.

| Landmark | Position | Value |
|---|---|---|
| Back face height | Full enclosure height | 59 mm (published) |
| Front face height | Measured ratio 0.79 × back | ~47 mm |
| Top edge | Slopes front→back, then flat | See profile below |
| Control panel flat | Back portion of top | ~40 mm deep, at 59 mm height |
| Slope | From front-top (47mm) to panel (59mm) | ~12 mm rise over ~89 mm run (~7.6°) |

Side profile points (x = mm from front, y = mm height):
- (0, 0) → (0, 47): front face
- (0, 47) → (89, 59): sloped top (under footswitch plate)
- (89, 59) → (129, 59): flat control panel
- (129, 59) → (129, 0): back face
- (129, 0) → (0, 0): bottom

Note: side photo has perspective caveats (camera slightly above). The wedge
character (tall back, sloping top, shorter front) is unambiguous; exact front
height ~47mm is provisional pending Sweetwater orthographic side view.

## Footswitch plate (from side + front views)

| Landmark | Value | Source |
|---|---|---|
| Plate length (front-back) | ~60 mm | Side view: 255px / 4.23 px/mm |
| Plate width | ~68 mm (93% of 73mm) | Front view: 500/540 px ratio |
| Plate thickness | ~5 mm | Side view + 3/4 detail |
| Hinge position | ~60 mm from front (plate back end) | Side view x≈310px |
| Plate tilt | ~4.5° (higher at back/hinge) | Side view |
| Gap under plate | ~9 mm at front, tapering to hinge | Side view |
| BOSS logo | Embossed, centered on plate | 3/4 detail view |

The plate is a separate hinged component, NOT flush with the body. There is a
visible shadow gap between plate underside and the sloped body top.

## Control panel (from top + 3/4 views)

Knob positions (from ds1_top.png, PedalPlayground, in inches from pedal center):

| Knob | x (in) | z (in) | x (mm) | z (mm) |
|---|---|---|---|---|
| TONE | -0.7418 | -1.8268 | -18.8 | -46.4 |
| LEVEL | +0.7250 | -1.8268 | +18.4 | -46.4 |
| DIST | -0.0042 | -1.2124 | -0.1 | -30.8 |

Cross-check vs side view: TONE/LEVEL 18mm from back ✓, DIST 34mm from back ✓.

| Component | Position | Notes |
|---|---|---|
| CHECK LED | Centered x, z ≈ -2.11" (18mm from back) | Red, between TONE/LEVEL and back edge |
| Knob diameter | ~15 mm | Boss standard |
| Knob height | ~18 mm | Side view ~45px |

## Jacks (from side view)

| Jack | Side | Position |
|---|---|---|
| INPUT | Right | ~55mm from front (43% of depth), ~35mm height |
| OUTPUT | Left | Mirror of INPUT |

Side view jack center: (335px, 232px) → 55mm from front, 26mm from bottom of
orange (bottom at y≈340). Height from base ≈ 26 + base thickness.

## Thumb screw (from side view)

| Position | Value |
|---|---|
| Center | ~74mm from front, ~48mm height |
| Diameter | ~6 mm |

Located on side panel, above body top edge, behind footswitch hinge.

## Labels (from top view ds1_top.png)

| Text | Position | Notes |
|---|---|---|
| CHECK | Above LED, near back edge | Small |
| TONE / LEVEL / DIST | Below respective knobs | — |
| OUTPUT ← / → INPUT | On slope between panel and plate | With arrows |
| Distortion | Large, center of slope area | — |
| DS-1 | Below "Distortion" | — |

Note: OUTPUT/INPUT labels sit on the SLOPED surface between control panel and
footswitch plate, not on a flat top. Label planes must follow the slope.

## Open questions

- [ ] Exact front face height (perspective in side photo). Sweetwater side view pending.
- [ ] Plate hinge mechanism detail (hidden — approximate is fine).
- [ ] Power jack on back face (visible in 3/4 view, low priority).
