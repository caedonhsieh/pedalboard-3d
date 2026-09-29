#!/usr/bin/env python3
"""Measure 2D landmarks in ds1_top.png (PedalPlayground top-down image).

Method: the image is a near-orthographic top view, 350x621 px, of a
73mm x 129mm pedal. We detect:
  - pedal outline corners (largest orange contour) -> image->mm affine
  - knob centers (dark circular blobs in the rear control area)
  - treadle pad corners (largest dark quad in the front treadle area)

All outputs go to references/ds1_landmarks.json with method + provenance.
No hand-picked pixel values: everything is detected, then verified visually
via an annotated overlay PNG.
"""
import json, os, math
import numpy as np
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REF = os.path.join(REPO, "references", "ds1_top.png")
OUT_JSON = os.path.join(REPO, "references", "ds1_landmarks.json")
OUT_OVERLAY = "/tmp/ds1_landmarks_overlay.png"

W_MM, D_MM = 73.0, 129.0  # manufacturer spec

import cv2
img = cv2.imread(REF)
H, W = img.shape[:2]
print(f"image {W}x{H}")

# --- 1. pedal outline: orange mask -> minAreaRect for mm/px scale ---
b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
orange = ((r > 150) & (r > b + 60) & (g < 170)).astype(np.uint8) * 255
n, lab, stats, cent = cv2.connectedComponentsWithStats(orange, 8)
big = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
pedal_mask = (lab == big).astype(np.uint8) * 255
rect = cv2.minAreaRect(cv2.findNonZero(pedal_mask))
(cx, cy), (rw, rh), ang = rect
# long side = depth (129mm), short side = width (73mm)
px_long, px_short = max(rw, rh), min(rw, rh)
mm_per_px_d = D_MM / px_long
mm_per_px_w = W_MM / px_short
print(f"pedal rect: {rw:.1f}x{rh:.1f}px angle={ang:.1f}")
print(f"mm/px: depth {mm_per_px_d:.4f}, width {mm_per_px_w:.4f}")
mm_per_px = (mm_per_px_d + mm_per_px_w) / 2

# pedal center in px -> maps to (0,0) in pedal coords (x right, z toward viewer-bottom/front)
# In the image, the pedal's rear (knobs) is at TOP, front (toe) at BOTTOM.
pcx, pcy = cx, cy

def px_to_pedal(px, py):
    """Image px -> pedal coords in mm: x (right+), z (front+)."""
    dx, dy = px - pcx, py - pcy
    # image y grows downward; pedal front is at image bottom -> z grows downward in image
    return (dx * mm_per_px, dy * mm_per_px)

# --- 2. knobs: dark blobs in rear third (image top), 3 largest circular ---
dark = ((r < 90) & (g < 90) & (b < 90)).astype(np.uint8) * 255
rear = dark[: int(H * 0.32), :]
n2, lab2, stats2, cent2 = cv2.connectedComponentsWithStats(rear, 8)
cands = []
for i in range(1, n2):
    area = stats2[i, cv2.CC_STAT_AREA]
    if 800 < area < 8000:
        x, y = cent2[i]
        cands.append((x, y, area))
cands.sort(key=lambda c: -c[2])
knobs = sorted(cands[:3], key=lambda c: c[0])  # left to right in image
print(f"knob blobs: {[(round(x,1), round(y,1), int(a)) for x, y, a in knobs]}")
# Reference (overlay-verified): left-to-right = TONE, LEVEL, DIST.
# (DS-1 knob order is TONE, LEVEL, DIST, not TONE, DIST, LEVEL.)
knob_names = ["tone", "level", "dist"]
knob_px = {}
for (x, y, a), name in zip(knobs[:3], knob_names):
    knob_px[name] = (x, y)

# --- 3. treadle pad: largest dark quad in front 2/3 ---
front = dark[int(H * 0.25):, :]
n3, lab3, stats3, cent3 = cv2.connectedComponentsWithStats(front, 8)
best, best_area = None, 0
for i in range(1, n3):
    area = stats3[i, cv2.CC_STAT_AREA]
    if area > best_area:
        best_area, best = area, i
ys, xs = np.where(lab3 == best)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min() + int(H * 0.25), ys.max() + int(H * 0.25)
pad_corners_px = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
pad_w_px, pad_d_px = x1 - x0, y1 - y0
print(f"pad rect px: x[{x0},{x1}] y[{y0},{y1}] -> {pad_w_px}x{pad_d_px}px")

landmarks = {
    "source": "references/ds1_top.png (PedalPlayground top-down, 350x621)",
    "method": "cv2 detection: orange minAreaRect for scale; dark-blob centroids for knobs; largest dark component bbox for pad. Verified via /tmp/ds1_landmarks_overlay.png.",
    "footprint_mm": {"w": W_MM, "d": D_MM},
    "mm_per_px": round(mm_per_px, 5),
    "coords": "pedal-mm: x right(+)/left(-) viewed from front(toe); z front(+)/rear(-); origin at pedal center",
    "knobs": {},
    "pad": {},
}
for name, (px, py) in knob_px.items():
    x_mm, z_mm = px_to_pedal(px, py)
    landmarks["knobs"][name] = {
        "px": [round(float(px), 1), round(float(py), 1)],
        "mm": [round(float(x_mm), 2), round(float(z_mm), 2)],
    }
cx_mm, cz_mm = px_to_pedal((x0 + x1) / 2, (y0 + y1) / 2)
landmarks["pad"] = {
    "corners_px": [[int(x), int(y)] for x, y in pad_corners_px],
    "center_mm": [round(float(cx_mm), 2), round(float(cz_mm), 2)],
    "size_mm": [round(float(pad_w_px * mm_per_px), 2), round(float(pad_d_px * mm_per_px), 2)],
}

with open(OUT_JSON, "w") as f:
    json.dump(landmarks, f, indent=2)
print(f"wrote {OUT_JSON}")

# overlay for visual verification
vis = Image.open(REF).convert("RGB")
d = ImageDraw.Draw(vis)
for name, (px, py) in knob_px.items():
    d.ellipse([px - 8, py - 8, px + 8, py + 8], outline="cyan", width=2)
    d.text((px + 10, py - 10), name, fill="cyan")
d.rectangle([x0, y0, x1, y1], outline="magenta", width=2)
d.text((x0, y0 - 12), "pad", fill="magenta")
box = cv2.boxPoints(rect)
d.polygon([tuple(map(int, p)) for p in box], outline="yellow")
vis.save(OUT_OVERLAY)
print(f"overlay -> {OUT_OVERLAY}")
print(json.dumps(landmarks, indent=1))
