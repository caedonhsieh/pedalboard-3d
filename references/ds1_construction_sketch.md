# DS-1 3D Construction Sketch — from multi-view interpolation

**Date:** 2026-09-29
**Sources:** 5 Sweetwater closeups (both sides, back, 3/4, front), Sweetwater front, GC back, Yahoo side, Session.de 3/4, Yayastation treadle detail, Rich Tone 3/4, PedalPlayground top.

## Coordinate system
- x: left(-) to right(+) when viewed from FRONT (toe). 73mm wide → x ∈ [-1.437", +1.437"]
- z: front(toe, +) to back(-). 129mm deep → z ∈ [-2.539", +2.539"]
- y: up from base. 0 at bottom.

## 1. Enclosure (orange wedge)
Profile in the y-z plane (side view), extruded across x:
- Front face: vertical, 47mm (1.850") tall. z = +2.539".
- Back face: vertical, 59mm (2.323") tall. z = -2.539".
- Top: slopes from (z=+2.539", y=1.850") up to (z=-0.965", y=2.323"), then FLAT at y=2.323" for the rear 40mm (control panel, z=-0.965" to -2.539").
- Bottom: flat at y=0.

In spec profile coords (z, y):
```
[+2.539, 0.000] → [+2.539, 1.850] → [-0.965, 2.323] → [-2.539, 2.323] → [-2.539, 0.000]
```

**Correction needed:** Current spec has the slope going to z=-0.9646 which is correct, but verify the 40mm control panel depth against detail1/detail3.

## 2. Treadle assembly (the footswitch)
The treadle is TWO parts, not one:

### 2a. Treadle plate (orange metal)
- A flat orange metal plate, hinged at the BACK.
- Spans from the front (z=+2.539") back to the hinge line (z≈-0.965", where the slope meets the control panel).
- Depth: ~89mm (3.504"). Centered at z ≈ +0.787".
- Width: ~66mm (2.6"), centered on x=0. Slightly narrower than the enclosure (73mm).
- Thickness: ~2mm.
- At rest, the FRONT is lifted ~8mm (0.315"), pivoting at the back hinge. The plate angles down toward the back.
- The plate has an orange border visible around the black pad on all four sides.

### 2b. Rubber pad (black)
- Black rubber pad, inset into the top of the orange plate.
- Smaller than the plate: ~60mm deep × ~62mm wide.
- Positioned toward the FRONT of the plate (not centered). From detail4, there's more orange visible behind the pad (near hinge) than in front.
- Pad front edge: near the plate front (z≈+2.4").
- Pad back edge: z≈+0.0" (leaving ~25mm of orange plate visible behind it).
- BOSS logo embossed in the center of the pad (raised black-on-black, subtle).
- Thickness: ~3mm above the plate surface.

**Correction needed:** Current model has plate and pad as the same size (2.362" deep, centered at z=+1.36"). Must separate:
- Plate: 3.504" deep, center z=+0.787", hinge at back (z=-0.965")
- Pad: 2.362" deep, center z=+1.30" (toward front), on top of plate

### 2c. Hinge
- Pivot axis at z=-0.965", y≈2.30" (just below the control panel surface).
- The black circular thing visible in detail1/detail3 side views at the top is the hinge pivot cap.
- Hinge axis runs along x (left-right).

**Correction needed:** Current model pivots at the back edge of the treadle (z=+0.18"). Must move pivot to z=-0.965".

## 3. Thumb screw (front)
- Black knurled knob on the FRONT (toe) face, centered horizontally (x=0).
- Position: y≈0.6" (15mm up from base), z=+2.539" (front face plane).
- Diameter ~18mm, protrudes ~10mm from the front face.
- This secures the treadle for battery access. Unscrew to lift treadle from front.

**Status:** Added to spec (2026-09-29). Verify y position against detail5.

## 4. Knobs (3x)
On the control panel (flat rear 40mm, y=2.323"):
- TONE: x=-0.742", z=-1.827" (left, back row)
- LEVEL: x=+0.725", z=-1.827" (right, back row)  
- DIST: x=-0.004", z=-1.212" (center, front row — closer to treadle)
- Black plastic, ~16mm diameter, ~15mm tall.
- Silver/white indicator line on top.
- Knurled sides.

**From detail2 (back view):** Knobs extend ~15mm above the control panel surface. They are clearly visible from behind.

## 5. Jacks
### 5a. Side jacks (2x, chrome)
- Left (OUTPUT): x=-1.437" (side wall), z=+0.374" (55mm from front), y=1.024" (26mm up)
- Right (INPUT): x=+1.437", z=+0.374", y=1.024"
- Chrome/silver, standard 1/4" barrel.
- From detail1/detail3: the jack is positioned on the sloped part of the side, vertically centered.

### 5b. DC power jack (back)
- x=0 (centered), z=-2.539" (back face), y=0.75" (19mm up from base).
- Black square bezel (~15mm) with round barrel connector in center.
- From detail2: positioned in lower half of back face, centered horizontally.

**Status:** Added to spec (2026-09-29). y=0.75" verified against detail2.

## 6. Labels
### On the sloped top surface (facing up-forward):
- "← OUTPUT" (left side, near back of slope)
- "INPUT ←" (right side, near back of slope) — BOTH arrows point left (signal flow)
- "Distortion" (center, large script)
- "DS-1" (center-right, below Distortion)

### On the control panel (flat, facing up):
- "CHECK" (center, above LED)
- "TONE" (below left knob)
- "LEVEL" (below right knob)  
- "DIST" (below center knob)

### On the back face:
- "USE BOSS PSA ADAPTOR ONLY (9V DC)" + polarity symbol. White sticker with red text, to the RIGHT of the DC jack (when viewed from back).
- **Missing from model** — label system doesn't support vertical back-face labels yet.

### On the treadle pad:
- "BOSS" embossed (raised, black-on-black, subtle). Centered on the pad.

## 7. LED
- Red LED, center of control panel, between the knobs.
- Position: x=0, z≈-1.55", on the control panel surface.
- Small dome, ~3mm diameter.

## 8. Construction order (for the builder)
1. Enclosure wedge (extruded profile)
2. Control panel (flat rear section — part of enclosure)
3. Treadle plate (orange, hinged at z=-0.965")
4. Rubber pad (black, on plate, toward front)
5. BOSS logo (embossed on pad)
6. Knobs (3x, on control panel)
7. LED (on control panel)
8. Side jacks (2x, chrome)
9. DC jack (back)
10. Thumb screw (front)
11. Labels (top slope, control panel)
12. PSA sticker (back) — needs vertical label support

## 9. Critical corrections from this sketch
1. **Treadle plate vs pad:** Separate them. Plate is 89mm deep (hinge to front), pad is 60mm deep (front-biased on plate).
2. **Hinge position:** Move from z=+0.18" to z=-0.965" (at the slope/control-panel junction).
3. **PSA label:** Add vertical back-face label support for the "USE BOSS PSA ADAPTOR ONLY" sticker.
4. **Pad position:** Front-biased on the plate, not centered.
5. **Verify:** Control panel depth (40mm?), knob z-positions, thumb screw y.

## 10. View coverage (complete)
- [x] Top-down: Sweetwater front, PedalPlayground top
- [x] Right side: Sweetwater detail1, Yahoo side
- [x] Left side: Sweetwater detail3
- [x] Front/toe: Sweetwater detail5
- [x] Back/rear: Sweetwater detail2, GC back
- [x] 3/4: Sweetwater detail4, Session.de, Rich Tone
- [x] Treadle detail: Yayastation, Sweetwater closeups
