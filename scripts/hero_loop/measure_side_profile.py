#!/usr/bin/env python3
"""Measure the DS-1 side profile from the side photo using edge detection.

TS9 lesson: the side profile is a measured polygon, never a guessed wedge.

Method (references/ds1_sw_detail3.jpg, 750x357):
  1. Vertical calibration: the back face is a vertical edge of KNOWN 59mm
     (manufacturer spec). Measure its px length -> mm/px_vertical.
     Vertical edges are robust to the photo's slight perspective.
  2. Canny + HoughLinesP to find the body's sloped top edge and the front
     (toe) vertical face.
  3. Front height = (front face px length) * mm/px_vertical.
  4. Also report the treadle hinge position and treadle angle for the loop.

Output: references/ds1_side_profile.json + overlay PNG.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REF = os.path.join(REPO, "references", "ds1_sw_detail3.jpg")
OUT_JSON = os.path.join(REPO, "references", "ds1_side_profile.json")
OUT_OVERLAY = "/tmp/ds1_side_profile_overlay.png"

import cv2
img = cv2.imread(REF)
H, W = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# --- edges ---
edges = cv2.Canny(gray, 50, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80,
                        minLineLength=120, maxLineGap=12).reshape(-1, 4)
segs = []
for x1, y1, x2, y2 in lines:
    length = np.hypot(x2 - x1, y2 - y1)
    ang = np.degrees(np.arctan2(y2 - y1, x2 - x1))
    segs.append({"p1": (int(x1), int(y1)), "p2": (int(x2), int(y2)),
                 "len": round(float(length), 1), "ang": round(float(ang), 1)})
segs.sort(key=lambda s: -s["len"])
print("long segments (len, ang, p1->p2):")
for s in segs[:12]:
    print(f"  {s['len']:6.1f}px ang={s['ang']:6.1f} {s['p1']}->{s['p2']}")

# --- vertical calibration from the back face ---
# Back face: near-vertical (|ang| ~ 90), at the right side (x > 0.85W)
verts = [s for s in segs if abs(abs(s["ang"]) - 90) < 12 and min(s["p1"][0], s["p2"][0]) > 0.80 * W]
print("\nback-face vertical candidates:")
for s in verts[:5]:
    print(f"  {s['len']:.1f}px {s['p1']}->{s['p2']}")
BACK_MM = 59.0
if verts:
    bv = max(verts, key=lambda s: s["len"])
    y_top = min(bv["p1"][1], bv["p2"][1])
    y_bot = max(bv["p1"][1], bv["p2"][1])
    back_px = y_bot - y_top
    mm_per_px_v = BACK_MM / back_px
    print(f"\nback face: y {y_top}-{y_bot} = {back_px}px = {BACK_MM}mm -> {mm_per_px_v:.4f} mm/px vertical")
else:
    raise SystemExit("no back-face vertical found")

# --- front (toe) face: near-vertical at the left side (x < 0.20W) ---
fronts = [s for s in segs if abs(abs(s["ang"]) - 90) < 14 and max(s["p1"][0], s["p2"][0]) < 0.22 * W]
print("\nfront-face vertical candidates:")
for s in fronts[:5]:
    print(f"  {s['len']:.1f}px {s['p1']}->{s['p2']}")
front_h_mm = None
if fronts:
    fv = max(fronts, key=lambda s: s["len"])
    front_h_mm = (max(fv["p1"][1], fv["p2"][1]) - min(fv["p1"][1], fv["p2"][1])) * mm_per_px_v
    print(f"front face height: {front_h_mm:.1f}mm")

# --- body sloped top edge: diagonal from back-top going down-left ---
# angle roughly -20..-35 deg (down-left), in the middle band of the image
diags = [s for s in segs if -40 < s["ang"] < -12 and 0.1 * W < (s["p1"][0] + s["p2"][0]) / 2 < 0.9 * W]
print("\nsloped top-edge candidates:")
for s in diags[:6]:
    print(f"  {s['len']:.1f}px ang={s['ang']:.1f} {s['p1']}->{s['p2']}")

profile = {
    "source": "references/ds1_sw_detail3.jpg (Sweetwater side, 750x357)",
    "method": "Canny+Hough edges; vertical scale calibrated from back face = 59mm (mfr spec). Overlay: /tmp/ds1_side_profile_overlay.png",
    "mm_per_px_vertical": round(float(mm_per_px_v), 4),
    "back_height_mm": BACK_MM,
    "back_height_source": "manufacturer spec (Boss compact enclosure)",
    "front_height_mm": round(float(front_h_mm), 1) if front_h_mm else None,
    "front_height_source": "measured from front vertical face in photo" if front_h_mm else "NOT FOUND",
    "segments": segs[:12],
}
with open(OUT_JSON, "w") as f:
    json.dump(profile, f, indent=2)
print(f"\nwrote {OUT_JSON}")

vis = Image.open(REF).convert("RGB")
d = ImageDraw.Draw(vis)
import random
random.seed(1)
for s in segs[:12]:
    c = (random.randint(80, 255), random.randint(80, 255), random.randint(80, 255))
    d.line([s["p1"], s["p2"]], fill=c, width=3)
vis.save(OUT_OVERLAY)
print(f"overlay -> {OUT_OVERLAY}")
