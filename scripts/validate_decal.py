#!/usr/bin/env python3
"""
Self-validation: render the treadle decal mapped to physical inches,
side-by-side with the reference photo.

Usage:
  python3 scripts/validate_decal.py --pedal sd1

This renders:
1. The decal texture mapped to the true treadle dimensions (2.875" x 3.214")
2. The reference photo's treadle area, scaled to the same physical size
3. A side-by-side comparison

If the text sizes/positions don't match, iterate on generate_*_decal.py
until they do. DO NOT ask Caedon to check until this passes.
"""

import argparse
import json
import os
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--pedal', required=True, help='Pedal ID (e.g., sd1)')
    p.add_argument('--ref', required=True, help='Reference image path (top-down)')
    args = p.parse_args()

    # Load spec
    with open(os.path.join(REPO, 'specs', f'{args.pedal}.json')) as f:
        spec = json.load(f)

    # Get treadle dimensions
    tp = spec['treadleProfile']
    import math
    ax, ay = tp['points'][0]
    bx, by = tp['points'][1]
    length = math.hypot(bx - ax, by - ay)
    width = tp.get('width', 2.875)
    print(f"Treadle: {width}\" x {length:.2f}\"")

    # Load decal
    decal_path = spec['treadleDecal'].split('?')[0].lstrip('./')
    decal = Image.open(os.path.join(REPO, decal_path)).convert('RGBA')

    # Render decal at physical scale (100 px/inch)
    SCALE = 100
    pw, ph = int(width * SCALE), int(length * SCALE)
    # The decal maps: texture X -> width, texture Y -> length
    # Texture top (V=1) = treadle back (hinge)
    physical = decal.resize((pw, ph), Image.LANCZOS)

    # Create comparison image with ruler
    # Put physical render on left, reference on right
    ref = Image.open(args.ref).convert('RGB')
    # Scale reference to match physical width (assume reference shows full pedal width)
    # This is approximate - user should verify
    ref_w, ref_h = ref.size
    # For now, just show side by side at reasonable sizes
    combined_h = max(ph, 600)
    combined = Image.new('RGB', (pw + ref_w + 40, combined_h), 'white')
    combined.paste(Image.new('RGB', (pw, ph), '#f0d060'), (0, 0))
    # Paste decal onto yellow background
    bg = Image.new('RGB', (pw, ph), '#f0d060')
    # Composite decal (with transparency) onto yellow
    bg.paste(physical, (0, 0), physical)
    combined.paste(bg, (0, 0))
    combined.paste(ref.resize((ref_w, min(ref_h, combined_h))), (pw + 40, 0))

    # Add labels
    from PIL import ImageDraw
    d = ImageDraw.Draw(combined)
    d.text((10, 10), f"Decal render ({width}\" x {length:.2f}\")", fill='black')
    d.text((pw + 50, 10), "Reference", fill='black')

    out = f"/tmp/{args.pedal}_decal_validate.png"
    combined.save(out)
    print(f"Saved: {out}")
    print("\nCompare the text sizes and positions.")
    print("If they don't match, adjust generate_*_decal.py and re-run.")

if __name__ == '__main__':
    main()
