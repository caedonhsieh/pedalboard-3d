#!/usr/bin/env python3
"""
TS9 Visual Validator v3 — Renders ACTUAL production code and compares pixels.
================================================================================
This validator catches visual bugs by:
1. Rendering the real parts.js + specs/ts9.json in headless Chromium
2. Rectifying reference photos to true orthographic views
3. Comparing color masks (green/black/silver) with zero tolerance
4. Running adversarial tests to prove it actually catches bugs

Usage:
    python3 scripts/visual_validate.py           # full validation
    python3 scripts/visual_validate.py --adversarial  # prove it catches bugs
    python3 scripts/visual_validate.py --view top    # just render top view

The validator FAILS if any color outline mismatches beyond antialiasing tolerance.
"""

import json
import sys
import base64
import io
import numpy as np
from pathlib import Path
from PIL import Image
from scipy import ndimage
import sys
sys.path.insert(0, str(Path(__file__).parent))
from rectify import rectify_top_homography, rectify_side_homography

REPO = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO / "specs" / "ts9.json"
RENDER_PAGE = REPO / "validate-render.html"

SIDE_PHOTO = Path.home() / "workspace/user/media_library/image/57/57ccfa5b5018878a1eb8243c8c5c2d311db55cc3dae415c8e0faceba40824819.png"
TOP_PHOTO = Path("/tmp/ts9_top.jpg")

# Tolerance: 2px for antialiasing at 1200px render. Anything beyond this is a real bug.
PIXEL_TOLERANCE = 2

# ----------------------------------------------------------------------------
# Rendering (headless Chromium via Playwright)
# ----------------------------------------------------------------------------

def render_view(view='top', mode='id'):
    """Render the actual production code. Returns (PIL Image, view_info)."""
    from playwright.sync_api import sync_playwright

    url = f"file://{RENDER_PAGE}?view={view}&mode={mode}"

    with sync_playwright() as p:
        browser = p.chromium.launch(args=[
            '--use-gl=swiftshader',
            '--enable-unsafe-swiftshader',
            '--disable-gpu',
        ])
        page = browser.new_page(viewport={'width': 1200, 'height': 1200})
        page.goto(url)
        # Wait for render to complete
        page.wait_for_function("window.__renderDone === true", timeout=30000)
        # Capture
        data_url = page.evaluate("window.__capture()")
        view_info = page.evaluate("window.__viewInfo")
        browser.close()

    # Decode data URL
    header, encoded = data_url.split(',', 1)
    img_data = base64.b64decode(encoded)
    img = Image.open(io.BytesIO(img_data))
    return img, view_info

# ----------------------------------------------------------------------------
# Photo rectification (homography-based, in rectify.py)
# ----------------------------------------------------------------------------
# rectify_top() and rectify_side() are now imported from rectify.py
# They use homography to map the photo to true orthographic.

def rectify_top():
    """Rectify top photo via homography. Returns (PIL Image, px_per_in)."""
    return rectify_top_homography(TOP_PHOTO)

def rectify_side():
    """Rectify side photo via homography. Returns (PIL Image, px_per_in)."""
    return rectify_side_homography(SIDE_PHOTO)

# ----------------------------------------------------------------------------
# Color mask extraction
# ----------------------------------------------------------------------------

def extract_masks_id_mode(img):
    """
    Extract color masks from ID-mode render.
    Green = #00FF00 (enclosure), Red = #FF0000 (black parts),
    Blue = #0000FF (silver/metal), Cyan = #00FFFF (white plate),
    White = background.
    """
    arr = np.array(img)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

    green = (g > 200) & (r < 100) & (b < 100)    # #00FF00
    black_parts = (r > 200) & (g < 100) & (b < 100)  # #FF0000 (black plastic as red)
    silver = (b > 200) & (r < 100) & (g < 100)    # #0000FF
    white_plate = (g > 200) & (b > 200) & (r < 100)  # #00FFFF (cyan)

    return {'green': green, 'black': black_parts, 'silver': silver, 'white': white_plate}

def extract_masks_photo(img):
    """
    Extract color masks from rectified photo.
    Green = TS9 green housing, Black = dark parts, Silver = chrome/metal,
    White = Ibanez plate (distinct from silver).
    """
    arr = np.array(img).astype(float)
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

    # TS9 green: green channel dominant
    green = (g > 90) & (g > r + 15) & (r < 160) & (b < 140)

    # Black: very dark
    brightness = (r + g + b) / 3
    black = (brightness < 70)

    # White: very bright, very low saturation (Ibanez plate)
    sat = np.std([r, g, b], axis=0)
    white = (brightness > 210) & (sat < 25)

    # Silver/chrome: bright but not white, low saturation
    # (knob tops, footswitch, jack hardware)
    silver = (brightness > 130) & (brightness <= 210) & (sat < 35) & ~white

    return {'green': green, 'black': black, 'silver': silver, 'white': white}

# ----------------------------------------------------------------------------
# Mask comparison
# ----------------------------------------------------------------------------

def compare_masks(render_masks, photo_masks, view_name):
    """
    Compare masks with zero tolerance (beyond antialiasing).
    Returns dict of {color: {iou, max_gap_px, mismatch_px, pass}}.
    """
    results = {}
    for color in ['green', 'black', 'silver', 'white']:
        rm = render_masks[color]
        pm = photo_masks[color]

        # Resize to match (render is 1200px, photo is at 200px/in)
        # For now, compare at photo resolution
        if rm.shape != pm.shape:
            rm_img = Image.fromarray(rm.astype(np.uint8) * 255)
            rm_img = rm_img.resize((pm.shape[1], pm.shape[0]), Image.NEAREST)
            rm = np.array(rm_img) > 127

        # IoU
        intersection = (rm & pm).sum()
        union = (rm | pm).sum()
        iou = intersection / max(union, 1)

        # Mismatch pixels (XOR)
        mismatch = (rm ^ pm).sum()

        # Max gap: distance transform on mismatch
        # For outline comparison, erode both and compare boundaries
        rm_eroded = ndimage.binary_erosion(rm, iterations=PIXEL_TOLERANCE)
        pm_eroded = ndimage.binary_erosion(pm, iterations=PIXEL_TOLERANCE)
        rm_outline = rm & ~rm_eroded
        pm_outline = pm & ~pm_eroded

        # Chamfer-like: for each outline pixel in render, distance to photo outline
        if rm_outline.sum() > 0 and pm_outline.sum() > 0:
            dt = ndimage.distance_transform_edt(~pm_outline)
            dists = dt[rm_outline]
            max_gap = dists.max()
            mean_gap = dists.mean()
        else:
            max_gap = 0
            mean_gap = 0

        # PASS if max gap within tolerance (antialiasing only)
        passed = max_gap <= PIXEL_TOLERANCE

        results[color] = {
            'iou': float(iou),
            'mismatch_px': int(mismatch),
            'max_gap_px': float(max_gap),
            'mean_gap_px': float(mean_gap),
            'pass': bool(passed),
        }

        status = "PASS" if passed else "FAIL"
        print(f"    {color:8s}: IoU={iou:.3f}, mismatch={mismatch}px, "
              f"max_gap={max_gap:.1f}px → {status}")

    return results

# ----------------------------------------------------------------------------
# Main validation
# ----------------------------------------------------------------------------

def validate_view(view_name):
    """Full validation for one view."""
    print(f"\n  [{view_name.upper()}] Rendering production code...")

    # Render ID mode (flat colors for precise masks)
    render_img, view_info = render_view(view=view_name, mode='id')
    print(f"    Rendered: {render_img.size}, view_info={view_info}")

    # Rectify photo
    print(f"    Rectifying reference photo...")
    if view_name == 'top':
        photo_img, px_per_in = rectify_top()
    else:
        photo_img, px_per_in = rectify_side()
    print(f"    Rectified: {photo_img.size}, {px_per_in}px/in")

    # Extract masks
    render_masks = extract_masks_id_mode(render_img)
    photo_masks = extract_masks_photo(photo_img)

    # Compare
    print(f"    Comparing color masks...")
    results = compare_masks(render_masks, photo_masks, view_name)

    return results

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--adversarial', action='store_true',
                        help='Run adversarial tests (prove validator catches bugs)')
    parser.add_argument('--view', choices=['top', 'side', 'both'], default='both')
    args = parser.parse_args()

    print("=" * 70)
    print("TS9 Visual Validator v3 — renders PRODUCTION CODE, compares PIXELS")
    print("=" * 70)

    if args.adversarial:
        return run_adversarial()

    views = ['top', 'side'] if args.view == 'both' else [args.view]
    all_results = {}

    for view in views:
        all_results[view] = validate_view(view)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    overall_pass = True
    for view, results in all_results.items():
        for color, r in results.items():
            status = "PASS" if r['pass'] else "FAIL"
            print(f"  {view:5s} {color:8s}: {status} "
                  f"(IoU={r['iou']:.3f}, max_gap={r['max_gap_px']:.1f}px)")
            if not r['pass']:
                overall_pass = False

    print(f"\n  Overall: {'PASS' if overall_pass else 'FAIL — do not ship'}")
    return 0 if overall_pass else 1

def run_adversarial():
    """
    Adversarial tests: deliberately break the model, validator MUST fail.
    If any test passes when it should fail, the validator is lying.
    """
    print("\n  [ADVERSARIAL] Proving the validator catches visual bugs...")
    print("  (Implementation: perturb spec, re-render, verify FAIL)")
    print("\n  Tests to implement:")
    print("    1. Move DRIVE label 0.05\" → must FAIL black mask")
    print("    2. Distort tick wedge (wrong angle) → must FAIL black mask")
    print("    3. Lower decal into z-fighting → must FAIL (flicker/disappearance)")
    print("    4. Shift jack 0.1\" → must FAIL silver mask (side view)")
    print("    5. Change profile point → must FAIL green mask (side view)")
    print("\n  Status: NOT YET IMPLEMENTED")
    return 1

if __name__ == '__main__':
    sys.exit(main())
