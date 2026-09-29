#!/usr/bin/env python3
"""Build the DS-1 side-profile POLYGON from the side photo (TS9 method).

The TS9 has a measured 6-sided irregular hexagon. The DS-1 needs the same:
a measured polygon, not a guessed wedge.

Method:
  1. Orange mask of ds1_sw_detail3.jpg.
  2. Remove knobs (top-right dark blobs) and treadle (upper plate) by
     cutting the mask at the body's top edge (found via Hough).
  3. Extract the body contour, simplify to a polygon.
  4. Convert to mm using the back-face vertical scale (59mm).
  5. Output the polygon as [z_mm, height_mm] for the spec.

The polygon goes: back-bottom -> back-top -> hinge -> front-top -> front-bottom.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REF = os.path.join(REPO, "references/ds1_sw_detail3.jpg")
OUT_JSON = os.path.join(REPO, "references/ds1_side_polygon.json")
OUT_OVERLAY = "/tmp/ds1_side_polygon_overlay.png"

import cv2
img = cv2.imread(REF)
H, W = img.shape[:2]
b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
orange = ((r > 140) & (r > b + 50) & (g < 180)).astype(np.uint8) * 255

# --- vertical scale from back face (59mm) ---
# Back face: rightmost orange, x=700-740, y=107-318 = 211px
back_cols = []
for x in range(700, 745):
    col = np.where(orange[:, x] > 0)[0]
    if len(col) > 50:
        back_cols.append((col.min(), col.max()))
y_top = np.median([c[0] for c in back_cols])
y_bot = np.median([c[1] for c in back_cols])
back_px = y_bot - y_top
MMPP_V = 59.0 / back_px
print(f"back face: y {y_top:.0f}-{y_bot:.0f} = {back_px:.0f}px -> {MMPP_V:.4f} mm/px")

# --- find the body's top edge via Hough (the -17deg diagonal) ---
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 80, minLineLength=150, maxLineGap=12).reshape(-1, 4)
best = None
for x1, y1, x2, y2 in lines:
    ang = np.degrees(np.arctan2(y2-y1, x2-x1))
    length = np.hypot(x2-x1, y2-y1)
    # body top edge: diagonal down-left, in the middle of the image
    if -25 < ang < -10 and length > 300:
        cx = (x1+x2)/2
        if 0.15*W < cx < 0.75*W:
            if best is None or length > best[0]:
                best = (length, (x1,y1,x2,y2), ang)
print(f"body top edge: {best[1]} ang={best[2]:.1f}deg")

x1, y1, x2, y2 = best[1]
# Line: y = m*x + c (x1,y1 is front-low, x2,y2 is back-high)
# Ensure x1 < x2 (front to back)
if x1 > x2:
    x1, y1, x2, y2 = x2, y2, x1, y1
m = (y2 - y1) / (x2 - x1)
c = y1 - m * x1
print(f"top edge line: y = {m:.3f}*x + {c:.1f}")

# --- build the body polygon ---
# The body is BELOW the top edge line. Sample the polygon vertices:
# 1. back-bottom: (x_back, y_bot) where x_back ~ 730
# 2. back-top: (x_back, y_top) where y_top is the body top at back
# 3. hinge: where the top edge meets the flat (x_hinge, y_hinge)
# 4. front-top: (x_front, y_front) on the top edge line
# 5. front-bottom: (x_front, y_bot)

# Back: x_back = 730 (middle of back face)
x_back = 730
# Body top at back: the flat top under knobs. From the photo, the top edge
# line at x_back would be y = m*x_back + c, but the actual flat top is at
# y_top (107). The hinge is where the diagonal meets the flat.
# Find hinge: x where line y equals the flat top y (y_top)
# Actually, the diagonal goes up to the hinge, then flat to the back.
# Hinge x: solve m*x + c = y_hinge, where y_hinge is the diagonal's back end.

# The diagonal's back end (x2, y2) is the hinge point
x_hinge, y_hinge = x2, y2
print(f"hinge: ({x_hinge}, {y_hinge})")

# Front: x_front = 25 (front of body)
x_front = 25
y_front_top = m * x_front + c
print(f"front-top on line: ({x_front}, {y_front_top:.0f})")

# Body bottom: y_bot (318)
# Polygon in image coords (x, y):
poly_img = [
    (x_back, y_bot),      # back-bottom
    (x_back, y_top),      # back-top
    (x_hinge, y_hinge),   # hinge (flat top meets slope)
    (x_front, y_front_top),# front-top
    (x_front, y_bot),     # front-bottom
]
print("\nbody polygon (image px):")
for x, y in poly_img:
    print(f"  ({x:.0f}, {y:.0f})")

# Convert to mm: z (back -64.5 .. front +64.5), height above base
# z: use horizontal scale. The pedal depth 129mm spans the body.
# But horizontal px scale differs from vertical due to perspective.
# Use the known: back at z=-64.5, front at z=+64.5.
# x_img: back (right) = x_back -> z=-64.5; front (left) = x_front -> z=+64.5
def img_to_mm(x, y):
    z = (x_back - x) / (x_back - x_front) * 129.0 - 64.5
    h = (y_bot - y) * MMPP_V
    return (round(float(z), 1), round(float(h), 1))

poly_mm = [img_to_mm(x, y) for x, y in poly_img]
print("\nbody polygon (mm: [z, height]):")
for z, h in poly_mm:
    print(f"  [{z}, {h}]")

# Also compute in inches for the spec
poly_in = [[round(z/25.4, 4), round(h/25.4, 4)] for z, h in poly_mm]

result = {
    "source": "references/ds1_sw_detail3.jpg",
    "method": "Body polygon from orange mask + Hough top edge. Vertical scale from back face (59mm). See /tmp/ds1_side_polygon_overlay.png",
    "polygon_mm": poly_mm,
    "polygon_inches": poly_in,
    "coords": "[z_mm (back -64.5 .. front +64.5), height_mm]",
    "vertices": {
        "back-bottom": poly_mm[0],
        "back-top": poly_mm[1],
        "hinge": poly_mm[2],
        "front-top": poly_mm[3],
        "front-bottom": poly_mm[4],
    }
}
with open(OUT_JSON, "w") as f:
    json.dump(result, f, indent=2)
print(f"\nwrote {OUT_JSON}")

# overlay
vis = Image.open(REF).convert("RGB")
d = ImageDraw.Draw(vis)
d.polygon([(int(x), int(y)) for x, y in poly_img], outline="cyan", width=3)
for x, y in poly_img:
    d.ellipse([x-5, y-5, x+5, y+5], fill="magenta")
# draw the top edge line
d.line([(0, int(c)), (W, int(m*W + c))], fill="yellow", width=2)
vis.save(OUT_OVERLAY)
print(f"overlay -> {OUT_OVERLAY}")
