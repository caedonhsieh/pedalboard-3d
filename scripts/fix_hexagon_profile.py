#!/usr/bin/env python3
"""
Self-fixing loop for TS9 irregular hexagon profile.

Measures the 6 hexagon vertices from the validated reference mask
(workspace/imagine_media/ts9-hexagon-mask.png, approved by Caedon 2026-09-28
as "the right housing shape") and updates specs/ts9.json.

This is MEASUREMENT, not guessing. The mask is the ground truth.
Run: python3 scripts/fix_hexagon_profile.py
"""

import json
import sys
from pathlib import Path
from PIL import Image
import numpy as np

# Paths
REPO = Path(__file__).parent.parent
MASK_PATH = Path.home() / "workspace/imagine_media/ts9-hexagon-mask.png"
SPEC_PATH = REPO / "specs/ts9.json"

# Physical dimensions (inches)
DEPTH_IN = 4.88  # z: -2.44 to +2.44
HEIGHT_IN = 2.09  # y: 0 to 2.09

def extract_hexagon_vertices(mask_path):
    """
    Extract 6 hexagon vertices from the validated mask by pixel scanning.
    
    Uses robust scanning: finds top edge, left/right edges, then identifies
    the 6 vertices by analyzing the shape. Returns list of (x_px, y_px).
    """
    img = Image.open(mask_path).convert('L')
    arr = np.array(img)
    binary = arr > 128
    
    h, w = binary.shape
    
    # Top edge: for each x, first white y
    top_ys = {}
    for x in range(w):
        col = binary[:, x]
        ys = np.where(col)[0]
        if len(ys) > 0:
            top_ys[x] = ys[0]
    
    # For each y, first and last white x
    row_xs = {}
    for y in range(h):
        row = binary[y, :]
        xs = np.where(row)[0]
        if len(xs) > 0:
            row_xs[y] = (xs[0], xs[-1])
    
    # V4: Peak = minimum y in top edge
    peak_x = min(top_ys, key=lambda x: top_ys[x])
    peak_y = top_ys[peak_x]
    
    # V1: bottom-left = at max y, leftmost x
    max_y = max(row_xs.keys())
    v1_x, _ = row_xs[max_y]
    # Use a y slightly above bottom to avoid noise, find leftmost
    for y in range(max_y, max_y-10, -1):
        if y in row_xs:
            v1_x = min(v1_x, row_xs[y][0])
    
    # V6: bottom-right = at max y, rightmost x
    v6_x = row_xs[max_y][1]
    for y in range(max_y, max_y-10, -1):
        if y in row_xs:
            v6_x = max(v6_x, row_xs[y][1])
    
    # V2: back-top = leftmost x where top edge is at flat level
    # Flat level = y at x where the top is stable on the left
    # Find by scanning from left: first x where top_y < 150 (above the noise)
    sorted_x = sorted(top_ys.keys())
    # The flat top is around y=93-96. Find leftmost x with y in [85, 110]
    v2_candidates = [x for x in sorted_x if 85 <= top_ys[x] <= 110]
    v2_x = min(v2_candidates)
    v2_y = top_ys[v2_x]
    
    # V3: end of flat = where y starts dropping significantly
    # Find the x where top_y goes below 85 (leaving the flat)
    # Search from v2_x rightward
    v3_x = next(x for x in sorted_x if x > v2_x and top_ys[x] < 85)
    # Back up to find the last x still on the flat (y >= 85)
    for x in range(v3_x, v2_x, -1):
        if x in top_ys and top_ys[x] >= 85:
            v3_x = x
            break
    v3_y = top_ys[v3_x]
    
    # V5: end of downslope = where y returns to ~100-110 on the right
    # Search from right: first x where y <= 110
    right_sorted = sorted(top_ys.keys(), reverse=True)
    v5_x = next(x for x in right_sorted if top_ys[x] <= 110)
    # Refine: find the x where the slope flattens (y stops increasing rapidly)
    # Look for the point where y is minimal in the right region before rising
    v5_y = top_ys[v5_x]
    
    vertices_px = [
        (v1_x, max_y),  # V1: bottom-back
        (v2_x, v2_y),   # V2: top-back
        (v3_x, v3_y),   # V3: flat-to-upslope
        (peak_x, peak_y),  # V4: peak
        (v5_x, v5_y),   # V5: downslope-to-front
        (v6_x, max_y),  # V6: bottom-front
    ]
    
    return vertices_px

def pixels_to_physical(vertices_px):
    """
    Map pixel coordinates to physical (z, y) in inches.
    
    x_px: left->right maps to z: -2.44 (back) -> +2.44 (front)
    y_px: top->bottom maps to y: 2.09 (top) -> 0 (bottom)
    """
    xs = [p[0] for p in vertices_px]
    ys = [p[1] for p in vertices_px]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)  # y_min is top (smaller pixel y)
    
    physical = []
    for x_px, y_px in vertices_px:
        z = -2.44 + (x_px - x_min) / (x_max - x_min) * DEPTH_IN
        y = (y_max - y_px) / (y_max - y_min) * HEIGHT_IN
        physical.append([round(z, 4), round(y, 4)])
    
    return physical

def main():
    print("=" * 60)
    print("TS9 Hexagon Profile Self-Fixing Loop")
    print("=" * 60)
    print(f"\nReference mask: {MASK_PATH}")
    print("Status: Validated by Caedon 2026-09-28 as 'the right housing shape'")
    
    if not MASK_PATH.exists():
        print(f"ERROR: Mask not found at {MASK_PATH}")
        sys.exit(1)
    
    print("\n[1/3] Extracting vertices from mask...")
    vertices_px = extract_hexagon_vertices(MASK_PATH)
    for i, (x, y) in enumerate(vertices_px):
        print(f"  V{i+1}: pixel ({x}, {y})")
    
    print("\n[2/3] Mapping to physical coordinates...")
    vertices_phys = pixels_to_physical(vertices_px)
    for i, (z, y) in enumerate(vertices_phys):
        print(f"  V{i+1}: ({z:.4f}, {y:.4f}) inches")
    
    print("\n[3/3] Updating spec...")
    with open(SPEC_PATH) as f:
        spec = json.load(f)
    
    old_points = spec['enclosure']['points']
    spec['enclosure']['points'] = vertices_phys
    spec['enclosure']['notes'] = (
        "MEASURED by scripts/fix_hexagon_profile.py from validated mask "
        "(workspace/imagine_media/ts9-hexagon-mask.png, Caedon 2026-09-28: "
        "'the right housing shape'). Vertices extracted by pixel scan, mapped to "
        "4.88x2.09in. This is measurement from validated reference, not estimation."
    )
    
    with open(SPEC_PATH, 'w') as f:
        json.dump(spec, f, indent=2)
    
    print(f"  Updated {SPEC_PATH}")
    print("\nChanges:")
    for i, (new, old) in enumerate(zip(vertices_phys, old_points)):
        dz = new[0] - old[0]
        dy = new[1] - old[1]
        if abs(dz) > 0.001 or abs(dy) > 0.001:
            print(f"  V{i+1}: [{old[0]:.4f}, {old[1]:.4f}] -> [{new[0]:.4f}, {new[1]:.4f}] (d: {dz:+.4f}, {dy:+.4f})")
    
    print("\n" + "=" * 60)
    print("DONE. Profile measured from validated reference.")
    print("=" * 60)

if __name__ == "__main__":
    main()
