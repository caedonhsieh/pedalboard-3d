# DS-1 Build Spec — From Cross-View Component Alignment

Derived 2026-09-29 from ds1_component_decomposition.md.
All dimensions in mm unless noted. Published envelope: 73 × 129 × 59.

## Critical correction

The previous body heights (39.4 back / 16.7 front) were measured from a side
photo showing BODY+TREADLE merged (both orange). They are invalid as body-only
heights. The 59mm published is the TOTAL max height (body + treadle + knobs).

## Body (C1) — lower enclosure

The body is the lower orange box. Its top has two zones:
- Rear flat deck (knob deck): behind the treadle hinge, holds the 3 knobs + LED.
- Sloped section: from the hinge forward, sloping down toward the front.

Dimensions:
- Width: 73 (published)
- Depth: 129 (published)
- Back height (body only, excl. treadle/knobs): 30
- Front height (body only): 14
- The slope runs from z=-25 (back of slope) to z=+64.5 (front).
  Slope drop: 30 → 14 = 16mm over 89.5mm ≈ 10.1°.
- Rear flat deck: from z=-64.5 to z=-25, at height 30 (flat).
- Base plate (C11): black, 2mm thick, at the bottom (y=0 to 2).
  Body orange starts at y=2.

Rationale: Total height check — body back 30 + gap 1 + plate 5.5 + pad 3 = 39.5
at the treadle. Knobs on the rear deck: knob height ~15mm → 30 + 15 = 45.
The 59mm published max likely includes the knob + packaging tolerance, or the
body is slightly taller. We stay within the envelope; the visual proportions
from V3/V5 drive the slope, not the 59mm.

## Treadle plate (C2) — the "large button"

Separate orange plate, hinged at the back, NOT merged with the body.

- Width: 68 (5mm narrower than body; 2.5mm inset each side)
- Length: 64 (from hinge forward; front lip stops ~15mm short of pedal front)
- Thickness: 5.5
- Hinge z: -5 (just in front of the knob deck; the knobs are at z≈-48)
- Hinge y (plate center): body_top_at_hinge + 1 (gap) + 2.75 (half thickness)
  body_top_at_hinge (z=-5): 30 - (20 * 16/89.5) ≈ 30 - 3.6 = 26.4
  hinge_y = 26.4 + 1 + 2.75 = 30.15
- The plate is HORIZONTAL (not tilted). The wedge gap forms because the body
  slopes down beneath it.
  - Gap at hinge: 1mm
  - Gap at front (z=59): body top = 30 - (84 * 16/89.5) ≈ 30 - 15 = 15
    plate bottom = 30.15 - 2.75 = 27.4
    gap = 27.4 - 15 = 12.4mm
  This matches V3/V5: thin at back, ~12mm at front.

- Front lip: the plate's front edge has a small downward curl (V6/V7). Model as
  a 3mm radius fillet on the front bottom edge. (Detail; can be a simple bevel.)

## Rubber pad (C3)

- Width: 62, Depth: 37, Thickness: 3
- Centered left-right on the plate (x=0).
- Positioned toward the FRONT of the plate: pad center z = hinge_z + 40 = 35.
  (Pad spans z=16.5 to 53.5; plate spans z=-5 to 59. Front orange lip: 5.5mm.
  Hmm, decomposition says front lip ~15-20mm. Adjust: pad center z=30,
  spans 11.5 to 48.5, front lip = 59-48.5 = 10.5mm. Closer.)
- Sits on top of the plate: pad bottom = plate top.
- Embossed BOSS logo on top (C13).

## Hinge (C4)

- Axis along X at (z=-5, y=29). The plate rotates about this axis.
- Hinge screws: black cylinders, Ø8mm, on both sides at (±36.5, 29, -5),
  axis along X. Visible in V3/V5/V9.

## Knobs (C5)

On the rear flat deck (z from -64.5 to -25, y=30):
- TONE: x=-16.5, z=-48, large (Ø20)
- LEVEL: x=0, z=-44, small (Ø14)
- DIST: x=+16.5, z=-48, large (Ø20)
- Each: black skirt + silver center + white indicator line.
- Silver nut/washer under each (visible in V4).
- Tick dots on the deck around each knob (V1/V8).

(Positions from the earlier ds1_top.png measurement; kept.)

## CHECK LED (C6)

- x=0, z=-56, on the rear deck. Small red dome, Ø5mm.
- Label "CHECK" above it (V1/V8).

## Jacks (C7/C8)

- Input (right, +x): at (36.5, 15, +10), axis along X. Chrome ring Ø14, black center.
- Output (left, -x): at (-36.5, 15, +10), same.
- On the body side walls, mid-height, slightly forward of center.
  (V3 shows input jack centered; V5 shows output jack.)

## DC jack (C9) + PSA label (C10)

On the back face (z=-64.5):
- DC jack: black square 13×13mm, centered x=0, y=15. Circular socket.
- PSA label: white sticker 28×18mm, at x=+20, y=15.
  Red text: "USE BOSS PSA ADAPTOR ONLY (9V DC)".

## Thumbscrew (C12)

- Front face (z=+64.5), centered x=0, y=8. Black knurled, Ø12mm.
- (V7 shows it centered on the front bottom.)

## Text / artwork (C13)

On the treadle plate top (y = plate top), in the strip between hinge and pad:
- "← OUTPUT": left side, at x=-22, z=+2, black.
- "INPUT ←": right side, at x=+22, z=+2, black. (Arrow points left in both? V1 shows
  "← OUTPUT" and "INPUT ←" — both arrows point left. Follow the photo.)
- "Distortion": centered, x=0, z=+10, large black.
- "DS-1": right, x=+18, z=+10, black.
On the body rear deck:
- "TONE" below TONE knob, "LEVEL" above LEVEL knob, "DIST" below DIST knob.
- "CHECK" above LED.
- Tick dots around knobs.

## What changed vs the old spec

1. Body back 39.4 → 30; front 16.7 → 14. (Old values included the treadle.)
2. Body slope 14.2° → 10.1°. (Less steep.)
3. Treadle length 59 → 64. (Measured from top view.)
4. Hinge z -2.4 → -5. (Just in front of knob deck.)
5. Hinge y derived from body top + gap + half thickness (not a magic 0.13").
6. The plate is HORIZONTAL; the old code applied a 6° lift on top of the deck
   slope, which double-tilted it. The wedge gap comes from the BODY sloping,
   not the plate tilting.
