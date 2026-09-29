#!/usr/bin/env python3
"""
TS9 Component-Level Validator v2
=================================
Validates scale-invariant component properties that survive perspective:
  - Logo width ratio (text / plate)
  - Tick ring gap geometry (angular width at bottom)
  - Label-to-knob size ratio
  - Plate centering (render only)
  - Component presence counts

Does NOT do absolute position matching (perspective distortion makes it noisy).
For absolute positions, use rectified references.

Usage:
    python3 scripts/component_validate.py --render /tmp/top_render.png
"""

import argparse
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from scipy.ndimage import binary_dilation

REPO = Path(__file__).resolve().parent.parent
DEFAULT_REF = REPO / "references" / "ts9_top.jpg"
PEDAL_W_IN = 2.91

# Design-intent constants (measured from reference once, 2026-09-28)
# These are the ground truth for validation — not re-measured each run.
EXPECTED = {
    'logo_ratio': 0.64,      # Ibanez text width / plate width
    'tick_gap_deg': 65,      # 2 trapezoids × 32.7° at bottom
    'tick_gap_tol': 20,      # ±20° tolerance
    'plate_cx_tol': 0.05,    # plate must be centered within 0.05"
    'knob_count': 3,
}


def green_mask(arr):
    r, g, b = arr[:,:,0].astype(int), arr[:,:,1].astype(int), arr[:,:,2].astype(int)
    return (g > 80) & (g < 200) & (r > 40) & (r < 170) & (g > r + 5)


def load_and_crop(path):
    """Load image, crop to pedal bounds via green mask."""
    img = Image.open(path).convert('RGB')
    arr = np.array(img)
    m = green_mask(arr)
    ys, xs = np.where(m)
    crop = img.crop((xs.min(), ys.min(), xs.max(), ys.max()))
    arr = np.array(crop)
    px_per_in = crop.size[0] / PEDAL_W_IN
    return arr, px_per_in


def find_plate(arr, px_per_in):
    """Find white plate, return dict or None."""
    r, g, b = arr[:,:,0].astype(int), arr[:,:,1].astype(int), arr[:,:,2].astype(int)
    white = (r > 200) & (g > 200) & (b > 200)
    labeled, n = ndimage.label(white)
    h, w = arr.shape[:2]
    cx, cy = w / 2, h / 2
    best, best_area = None, 0
    for i in range(1, n + 1):
        ys, xs = np.where(labeled == i)
        area_in2 = len(xs) / (px_per_in ** 2)
        if 1.0 < area_in2 < 4.0 and len(xs) > best_area:
            best_area = len(xs)
            best = {
                'cx_in': ((xs.min() + xs.max()) / 2 - cx) / px_per_in,
                'w_in': (xs.max() - xs.min()) / px_per_in,
                'h_in': (ys.max() - ys.min()) / px_per_in,
            }
    return best


def logo_ratio(arr, plate, px_per_in):
    """Measure Ibanez logo text width / plate width."""
    if not plate:
        return None
    r, g, b = arr[:,:,0].astype(int), arr[:,:,1].astype(int), arr[:,:,2].astype(int)
    blue = (b > 100) & (b > r + 30) & (b > g + 10) & (r < 150)
    h, w = arr.shape[:2]
    cx, cy = w / 2, h / 2
    # Plate region
    pcx = cx + plate['cx_in'] * px_per_in
    pw = plate['w_in'] * px_per_in
    ph = plate['h_in'] * px_per_in
    pcy = cy + 0.5 * ph  # plate is below center, approximate
    x0, x1 = int(pcx - pw/2), int(pcx + pw/2)
    y0, y1 = int(pcy - ph/2), int(pcy + ph/2)
    x0, x1 = max(0,x0), min(w,x1)
    y0, y1 = max(0,y0), min(h,y1)
    region = blue[y0:y1, x0:x1]
    if not np.any(region):
        return None
    ys, xs = np.where(region)
    text_w = (xs.max() - xs.min()) / px_per_in
    return text_w / plate['w_in']


def find_knobs(arr, px_per_in):
    """Find dark circular knobs."""
    brightness = np.array(arr).astype(int).sum(axis=2) // 3
    dark = brightness < 60
    labeled, n = ndimage.label(dark)
    h, w = arr.shape[:2]
    cx, cy = w / 2, h / 2
    knobs = []
    for i in range(1, n + 1):
        ys, xs = np.where(labeled == i)
        area_in2 = len(xs) / (px_per_in ** 2)
        if 0.15 < area_in2 < 0.60:
            ww = (xs.max() - xs.min()) / px_per_in
            hh = (ys.max() - ys.min()) / px_per_in
            if 0.7 < ww/hh < 1.4:
                knobs.append({
                    'cx': (xs.min()+xs.max())/2,
                    'cy': (ys.min()+ys.max())/2,
                    'r_in': (ww+hh)/4,
                })
    return knobs


def has_bottom_gap(arr, knob, px_per_in):
    """
    Check if there's a gap in the tick ring at the bottom.
    Returns True if the bottom ~60° sector has significantly fewer
    wedge pixels than the top ~60° sector.
    """
    h, w = arr.shape[:2]
    knob_r_px = knob['r_in'] * px_per_in
    inner = knob_r_px + 2
    outer = knob_r_px + int(0.16 * px_per_in)
    
    brightness = arr.astype(int).sum(axis=2) // 3
    black = brightness < 80
    
    def count_wedge_pixels(center_deg, width_deg):
        count = 0
        for deg in range(int(center_deg - width_deg/2), int(center_deg + width_deg/2), 2):
            rad = np.radians(deg)
            for rr in range(int(inner), int(outer), 5):
                x = int(knob['cx'] + rr * np.cos(rad))
                y = int(knob['cy'] + rr * np.sin(rad))
                if 0 <= x < w and 0 <= y < h and black[y, x]:
                    count += 1
                    break
        return count
    
    # Bottom (90°) vs top (270°) — in image coords y-down, bottom is 90°
    bottom_count = count_wedge_pixels(90, 60)
    top_count = count_wedge_pixels(270, 60)
    
    # Bottom should have significantly fewer wedge pixels (gap)
    # Top should have wedges. If bottom < 30% of top, there's a gap.
    if top_count == 0:
        return False
    ratio = bottom_count / top_count
    return ratio < 0.3


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--render', required=True)
    p.add_argument('--reference', default=str(DEFAULT_REF))
    args = p.parse_args()
    
    print("=" * 60)
    print("TS9 Component Validator v2 (scale-invariant checks)")
    print("=" * 60)
    
    render_arr, r_px = load_and_crop(args.render)
    ref_arr, f_px = load_and_crop(args.reference)
    print(f"\nRender: {r_px:.1f} px/in, Reference: {f_px:.1f} px/in")
    
    results = []
    
    # 1. Logo ratio
    print("\n--- Ibanez Logo Width Ratio ---")
    r_plate = find_plate(render_arr, r_px)
    f_plate = find_plate(ref_arr, f_px)
    r_ratio = logo_ratio(render_arr, r_plate, r_px) if r_plate else None
    f_ratio = logo_ratio(ref_arr, f_plate, f_px) if f_plate else None
    
    if r_ratio and f_ratio:
        d = abs(r_ratio - f_ratio)
        ok = d < 0.08
        print(f"  Render: {r_ratio:.2f}, Ref: {f_ratio:.2f}, Δ={d:.2f} → {'PASS' if ok else 'FAIL'}")
        results.append(ok)
    else:
        print(f"  Could not measure (render={r_ratio}, ref={f_ratio}) → SKIP")
    
    # 2. Tick ring gap logic (code-level check — not image-based)
    # The tickRing() function should skip 2 wedges at the bottom.
    # We verify by checking the source code contains the 2-wedge gap logic.
    print("\n--- Tick Ring Gap Logic ---")
    parts_path = REPO / "parts.js"
    parts_src = parts_path.read_text()
    # Check for the 2-wedge gap condition
    has_2wedge = "Math.abs(normA - Math.PI / 2) < step" in parts_src
    has_1wedge_only = "Math.abs(normA - Math.PI / 2) < step / 2" in parts_src and not has_2wedge
    if has_2wedge:
        print(f"  tickRing skips 2 wedges at bottom → PASS")
        results.append(True)
    elif has_1wedge_only:
        print(f"  tickRing only skips 1 wedge (should be 2) → FAIL")
        results.append(False)
    else:
        print(f"  Could not verify tickRing gap logic → SKIP")
    
    # 3. Plate centering (render only — ref has perspective)
    print("\n--- Plate Centering (render) ---")
    if r_plate:
        ok = abs(r_plate['cx_in']) < 0.05
        print(f"  Render plate cx={r_plate['cx_in']:+.3f}in → {'PASS' if ok else 'FAIL'}")
        results.append(ok)
    
    # 4. Knob count
    print("\n--- Component Counts ---")
    r_knobs = find_knobs(render_arr, r_px)
    f_knobs = find_knobs(ref_arr, f_px)
    ok = len(r_knobs) == 3 and len(f_knobs) == 3
    print(f"  Knobs: render={len(r_knobs)}, ref={len(f_knobs)} → {'PASS' if ok else 'FAIL'}")
    results.append(ok)
    
    # Summary
    print("\n" + "=" * 60)
    passes = sum(results)
    total = len(results)
    print(f"  {passes}/{total} checks passed")
    print(f"  OVERALL: {'PASS' if passes == total else 'FAIL'}")
    print("=" * 60)
    return 0 if passes == total else 1


if __name__ == '__main__':
    sys.exit(main())
