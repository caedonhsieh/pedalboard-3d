#!/usr/bin/env python3
"""
TS9 Self-Validation v2 — True Image-Based
==========================================
Segments reference photos FRESH on every run. No hardcoded measurements.
The image is ground truth; the spec is what gets validated.

1. Loads specs/ts9.json
2. Segments side photo → extracts housing contour → compares to spec profile
3. Segments top photo → finds knobs, footswitch, LED, plate → compares to spec
4. Reports quantitative metrics. No circularity.

Usage:
    python3 scripts/validate_ts9.py
    python3 scripts/validate_ts9.py --fix
"""

import json
import sys
import numpy as np
from pathlib import Path
from PIL import Image
from scipy import ndimage

REPO = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO / "specs" / "ts9.json"

SIDE_PHOTO = Path.home() / "workspace/user/media_library/image/57/57ccfa5b5018878a1eb8243c8c5c2d311db55cc3dae415c8e0faceba40824819.png"
TOP_PHOTO = Path("/tmp/ts9_top.jpg")

PROFILE_THRESHOLD_MM = 2.5
PART_THRESHOLD_MM = 2.0

# ----------------------------------------------------------------------------

def load_spec():
    with open(SPEC_PATH) as f:
        return json.load(f)

def save_spec(spec):
    with open(SPEC_PATH, 'w') as f:
        json.dump(spec, f, indent=2)

# ----------------------------------------------------------------------------
# FRESH SEGMENTATION — Side
# ----------------------------------------------------------------------------

def segment_side():
    """Segment side photo fresh. Returns (contour_px, px_per_in)."""
    print("    Segmenting side photo...")
    img = Image.open(SIDE_PHOTO).convert('RGB')
    arr = np.array(img).astype(float)
    H, W = arr.shape[:2]
    print(f"      Image: {W}x{H}")

    # Green housing: green channel dominant, reasonably saturated
    # Sample the green: TS9 green is approx (60-100, 160-200, 60-100)
    g = arr[:,:,1]
    r = arr[:,:,0]
    b = arr[:,:,2]
    green_mask = (g > 100) & (g > r + 20) & (g > b - 10) & (r < 150)

    # Largest connected component = housing
    labeled, n = ndimage.label(green_mask)
    sizes = np.array([(labeled == i).sum() for i in range(1, n+1)])
    if len(sizes) == 0:
        return None, None
    housing = (labeled == (np.argmax(sizes) + 1))

    # Fill holes (knobs/jacks create holes in the mask)
    housing_filled = ndimage.binary_fill_holes(housing)

    ys, xs = np.where(housing_filled)
    x0, x1 = xs.min(), xs.max()
    y0, y1 = ys.min(), ys.max()
    print(f"      Housing bounds: x[{x0},{x1}] y[{y0},{y1}]")

    # Extract contour
    eroded = ndimage.binary_erosion(housing_filled, iterations=2)
    contour = housing_filled & ~eroded
    cy, cx = np.where(contour)

    # px_per_in: use known depth 4.88" for width
    # But the housing width in px includes perspective. Use it as estimate.
    px_per_in = (x1 - x0) / 4.88
    print(f"      Scale: ~{px_per_in:.1f} px/in, contour: {len(cx)} px")

    return np.stack([cx, cy], axis=1), px_per_in, (x0, x1, y0, y1)

def validate_side_fresh(spec):
    """Compare spec profile to freshly segmented side contour."""
    print("\n  [Side] Fresh segmentation vs spec...")
    result = segment_side()
    if result[0] is None:
        return {'error': 'segmentation failed', 'pass': False}
    contour_px, px_per_in, (x0, x1, y0, y1) = result

    d = spec['dims']['d']
    h = spec['dims']['h']

    # Map spec (z,y) to pixels using the housing bbox
    def spec_to_px(z, y):
        x_px = x0 + (z + d/2) / d * (x1 - x0)
        y_px = y1 - (y / h) * (y1 - y0)
        return x_px, y_px

    pts = spec['enclosure']['points']
    errors = []
    for z, y in pts:
        px, py = spec_to_px(z, y)
        dists = np.sqrt((contour_px[:,0] - px)**2 + (contour_px[:,1] - py)**2)
        err_in = dists.min() / px_per_in
        errors.append(err_in)
        print(f"      (z={z:6.3f}, y={y:5.3f}) err={err_in*25.4:5.2f}mm")

    max_err = max(errors)
    rms = np.sqrt(np.mean(np.array(errors)**2))
    passed = max_err * 25.4 <= PROFILE_THRESHOLD_MM
    print(f"      Max: {max_err*25.4:.2f}mm, RMS: {rms*25.4:.2f}mm → {'PASS' if passed else 'FAIL'}")
    return {'max_mm': max_err*25.4, 'rms_mm': rms*25.4, 'pass': passed, 'errors': errors}

# ----------------------------------------------------------------------------
# FRESH SEGMENTATION — Top
# ----------------------------------------------------------------------------

def segment_top():
    """Segment top photo fresh. Returns dict of measured part positions."""
    print("    Segmenting top photo...")
    img = Image.open(TOP_PHOTO).convert('RGB')
    arr = np.array(img).astype(float)
    H, W = arr.shape[:2]
    print(f"      Image: {W}x{H}")

    # Green body for calibration
    g, r, b = arr[:,:,1], arr[:,:,0], arr[:,:,2]
    green_mask = (g > 100) & (g > r + 10) & (r < 160)
    labeled, n = ndimage.label(green_mask)
    sizes = np.array([(labeled == i).sum() for i in range(1, n+1)])
    body = (labeled == (np.argmax(sizes) + 1))
    ys, xs = np.where(body)
    bx0, bx1 = xs.min(), xs.max()
    by0, by1 = ys.min(), ys.max()
    print(f"      Body: x[{bx0},{bx1}] y[{by0},{by1}]")

    # Calibration: body is 2.91" wide (x), 4.88" deep (y)
    px_per_in_x = (bx1 - bx0) / 2.91
    px_per_in_y = (by1 - by0) / 4.88
    cx_body = (bx0 + bx1) / 2

    def px_to_x(px): return (px - cx_body) / px_per_in_x
    def px_to_z(py): return -2.44 + (py - by0) / px_per_in_y

    measured = {}

    # Knobs: black circular regions in upper 45%
    black = (r < 60) & (g < 60) & (b < 60)
    upper = np.zeros_like(black)
    upper[:int(H*0.45)] = black[:int(H*0.45)]
    labeled_k, nk = ndimage.label(upper)
    knobs_found = []
    for i in range(1, nk+1):
        ys_k, xs_k = np.where(labeled_k == i)
        sz = len(xs_k)
        if sz > 5000:
            w, h = xs_k.max()-xs_k.min(), ys_k.max()-ys_k.min()
            # Circularity check: w/h close to 1
            if 0.7 < w/max(h,1) < 1.4:
                knobs_found.append((xs_k.mean(), ys_k.mean(), sz))
    # Sort by x: left=drive, middle=tone, right=level
    # But tone is lower (higher y). Sort: drive/level are upper row, tone is below.
    knobs_found.sort(key=lambda k: k[1])  # by y
    # First two by y are drive/level (upper), third is tone
    # Actually: drive (476,387), level (1302,390), tone (891,707)
    # Sort by y, then the two with smallest y are drive/level
    if len(knobs_found) >= 3:
        by_y = sorted(knobs_found, key=lambda k: k[1])
        upper_two = sorted(by_y[:2], key=lambda k: k[0])  # left to right
        drive_px, level_px = upper_two[0], upper_two[1]
        tone_px = by_y[2]
        measured['drive'] = {'x': px_to_x(drive_px[0]), 'z': px_to_z(drive_px[1])}
        measured['level'] = {'x': px_to_x(level_px[0]), 'z': px_to_z(level_px[1])}
        measured['tone'] = {'x': px_to_x(tone_px[0]), 'z': px_to_z(tone_px[1])}
        print(f"      Knobs: drive=({measured['drive']['x']:.3f},{measured['drive']['z']:.3f}), "
              f"tone=({measured['tone']['x']:.3f},{measured['tone']['z']:.3f}), "
              f"level=({measured['level']['x']:.3f},{measured['level']['z']:.3f})")

    # Footswitch: large bright rectangle in lower half
    bright = (r > 150) & (g > 150) & (b > 150)
    lower = np.zeros_like(bright)
    lower[int(H*0.55):] = bright[int(H*0.55):]
    labeled_f, nf = ndimage.label(lower)
    best = None
    for i in range(1, nf+1):
        ys_f, xs_f = np.where(labeled_f == i)
        sz = len(xs_f)
        if sz > 100000:  # large
            w, h = xs_f.max()-xs_f.min(), ys_f.max()-ys_f.min()
            # Footswitch is roughly 2:1 aspect (wider than tall)
            if 1.2 < w/max(h,1) < 3.0 and xs_f.mean() > W*0.3 and xs_f.mean() < W*0.7:
                if best is None or sz > best[0]:
                    best = (sz, xs_f.mean(), ys_f.mean(), w, h)
    if best:
        _, fx, fy, fw, fh = best
        measured['footswitch'] = {
            'x': px_to_x(fx), 'z': px_to_z(fy),
            'w': fw/px_per_in_x, 'd': fh/px_per_in_y,
        }
        print(f"      Footswitch: ({measured['footswitch']['x']:.3f},{measured['footswitch']['z']:.3f}) "
              f"{measured['footswitch']['w']:.3f}x{measured['footswitch']['d']:.3f}in")

    # LED: red dot in upper area
    red = (r > 150) & (g < 100) & (b < 100)
    upper_red = np.zeros_like(red)
    upper_red[:int(H*0.3)] = red[:int(H*0.3)]
    labeled_r, nr = ndimage.label(upper_red)
    for i in range(1, nr+1):
        ys_r, xs_r = np.where(labeled_r == i)
        if len(xs_r) > 100:
            measured['led'] = {'x': px_to_x(xs_r.mean()), 'z': px_to_z(ys_r.mean())}
            print(f"      LED: ({measured['led']['x']:.3f},{measured['led']['z']:.3f})")
            break

    # Ibanez plate: white rectangle in middle
    # Targeted: crop to plate region based on body bounds, then segment carefully.
    # Plate is at ~48-64% of body height, centered horizontally.
    px0 = int(cx_body - 650)
    px1 = int(cx_body + 650)
    py0 = int(by0 + (by1-by0)*0.48)
    py1 = int(by0 + (by1-by0)*0.66)
    crop = arr[py0:py1, px0:px1]
    # White pixels in crop
    cr, cg, cb = crop[:,:,0], crop[:,:,1], crop[:,:,2]
    white_c = (cr > 180) & (cg > 180) & (cb > 180)
    # The plate is the dominant white region. Find its bounds via
    # the largest connected component of white.
    labeled_c, nc = ndimage.label(white_c)
    sizes_c = np.array([(labeled_c == i).sum() for i in range(1, nc+1)])
    if len(sizes_c) > 0:
        # Take the largest, but the logo splits it. Instead, find the
        # bounding box that contains the top 2 largest (plate parts).
        idx_sorted = np.argsort(sizes_c)[::-1]
        # Combine top 2 if they're similar size (logo split)
        use_idx = [idx_sorted[0]]
        if len(idx_sorted) > 1 and sizes_c[idx_sorted[1]] > sizes_c[idx_sorted[0]] * 0.3:
            use_idx.append(idx_sorted[1])
        all_ys, all_xs = [], []
        for idx in use_idx:
            ys_c, xs_c = np.where(labeled_c == (idx+1))
            all_ys.extend(ys_c)
            all_xs.extend(xs_c)
        all_ys, all_xs = np.array(all_ys), np.array(all_xs)
        x0p, x1p = all_xs.min() + px0, all_xs.max() + px0
        y0p, y1p = all_ys.min() + py0, all_ys.max() + py0
        measured['ibanezPlate'] = {
            'x': px_to_x((x0p+x1p)/2), 'z': px_to_z((y0p+y1p)/2),
            'w': (x1p-x0p)/px_per_in_x, 'd': (y1p-y0p)/px_per_in_y,
        }
        print(f"      Ibanez plate: ({measured['ibanezPlate']['x']:.3f},{measured['ibanezPlate']['z']:.3f}) "
              f"{measured['ibanezPlate']['w']:.3f}x{measured['ibanezPlate']['d']:.3f}in")

    return measured

def validate_top_fresh(spec):
    """Compare spec to freshly segmented top measurements."""
    print("\n  [Top] Fresh segmentation vs spec...")
    measured = segment_top()

    errors = {}
    def check(name, spec_val, meas_val):
        if meas_val is None:
            print(f"      {name}: NOT FOUND in image")
            return
        err = np.sqrt((spec_val['x']-meas_val['x'])**2 + (spec_val['z']-meas_val['z'])**2)
        errors[name] = err * 25.4
        print(f"      {name}: spec=({spec_val['x']:.3f},{spec_val['z']:.3f}) "
              f"meas=({meas_val['x']:.3f},{meas_val['z']:.3f}) err={err*25.4:.2f}mm")

    for k in spec.get('knobs', []):
        if k['id'] in measured:
            check(f"knob-{k['id']}", k, measured[k['id']])

    if 'footswitch' in spec and 'footswitch' in measured:
        check('footswitch', spec['footswitch'], measured['footswitch'])

    if 'led' in spec and 'led' in measured:
        check('led', spec['led'], measured['led'])

    if 'ibanezPlate' in spec and 'ibanezPlate' in measured:
        check('ibanezPlate', spec['ibanezPlate'], measured['ibanezPlate'])

    max_err = max(errors.values()) if errors else 999
    passed = max_err <= PART_THRESHOLD_MM
    print(f"      Max: {max_err:.2f}mm → {'PASS' if passed else 'FAIL'}")
    return {'max_mm': max_err, 'pass': passed, 'errors': errors}

# ----------------------------------------------------------------------------
# Self-fixing
# ----------------------------------------------------------------------------

def fix_from_measurements(spec, measured):
    """Update spec from fresh measurements. Returns (spec, changed)."""
    changed = False

    # Knobs
    for k in spec.get('knobs', []):
        kid = k['id']
        if kid in measured:
            m = measured[kid]
            if abs(k['x'] - m['x']) > 0.001 or abs(k['z'] - m['z']) > 0.001:
                print(f"    Fix knob-{kid}: ({k['x']:.3f},{k['z']:.3f}) → ({m['x']:.3f},{m['z']:.3f})")
                k['x'], k['z'] = round(m['x'], 3), round(m['z'], 3)
                changed = True

    # Footswitch
    if 'footswitch' in spec and 'footswitch' in measured:
        fs, m = spec['footswitch'], measured['footswitch']
        for key in ['x', 'z', 'w', 'd']:
            if abs(fs.get(key, 0) - m.get(key, 0)) > 0.001:
                print(f"    Fix footswitch.{key}: {fs.get(key,0):.3f} → {m[key]:.3f}")
                fs[key] = round(m[key], 3)
                changed = True

    # LED
    if 'led' in spec and 'led' in measured:
        led, m = spec['led'], measured['led']
        if abs(led['x'] - m['x']) > 0.001 or abs(led['z'] - m['z']) > 0.001:
            print(f"    Fix led: ({led['x']:.3f},{led['z']:.3f}) → ({m['x']:.3f},{m['z']:.3f})")
            led['x'], led['z'] = round(m['x'], 3), round(m['z'], 3)
            changed = True

    # Ibanez plate
    if 'ibanezPlate' in spec and 'ibanezPlate' in measured:
        ip, m = spec['ibanezPlate'], measured['ibanezPlate']
        for key in ['x', 'z', 'w', 'd']:
            if abs(ip.get(key, 0) - m.get(key, 0)) > 0.001:
                print(f"    Fix ibanezPlate.{key}: {ip.get(key,0):.3f} → {m[key]:.3f}")
                ip[key] = round(m[key], 3)
                changed = True

    return spec, changed

# ----------------------------------------------------------------------------
# Spec consistency checks (must pass before image validation)
# ----------------------------------------------------------------------------

def check_spec_consistency(spec):
    """Check spec for known bugs. Returns (passed, issues, fixes)."""
    print("\n  [Consistency] Checking spec...")
    issues = []
    fixes = {}

    # 1. Duplicate z in profile (causes division by zero)
    pts = spec['enclosure']['points']
    zs = [p[0] for p in pts]
    dupes = [z for z in set(zs) if zs.count(z) > 1]
    if dupes:
        issues.append(f"Duplicate z in profile: {dupes} (causes NaN in interpolation)")
        # Fix: remove the duplicate (keep the one with higher y, the top edge)
        # Actually: the profile should go from back-bottom to front-bottom via top.
        # The duplicate z=-2.45 has y=0.0 and y=1.46. The y=0.0 is the bottom
        # which is already handled by profileEnclosure(). Remove it.
        fixes['remove_dupe_z'] = dupes[0]

    # 2. Dimensions must match published specs
    dims = spec['dims']
    expected = {'w': 2.91, 'd': 4.88, 'h': 2.09}
    for k, v in expected.items():
        if abs(dims[k] - v) > 0.001:
            issues.append(f"Dim {k}={dims[k]} != published {v}")
            fixes[f'dim_{k}'] = v

    # 3. No hardcoded y for jacks (must use surfaceAt)
    # Check if jacks have 'y' in spec (they shouldn't - should be derived)
    for jack in spec.get('jacks', []):
        if 'y' in jack:
            issues.append(f"Jack {jack.get('id')} has hardcoded y={jack['y']} (must use surfaceAt)")
            fixes[f"jack_{jack.get('id')}_y"] = True

    # 3b. No hardcoded y for powerJack
    if 'powerJack' in spec and 'y' in spec['powerJack']:
        issues.append(f"powerJack has hardcoded y={spec['powerJack']['y']} (must use surfaceAt)")
        fixes['powerJack_y'] = True

    # 4. Tick ring wedge count consistency
    # (Check parts.js for hardcoded values - done in code checks)

    passed = len(issues) == 0
    for issue in issues:
        print(f"      FAIL: {issue}")
    if passed:
        print(f"      All consistency checks passed.")
    return passed, issues, fixes

def apply_consistency_fixes(spec, fixes):
    """Apply automatic fixes. Returns (spec, changed)."""
    changed = False

    if 'remove_dupe_z' in fixes:
        dupe_z = fixes['remove_dupe_z']
        pts = spec['enclosure']['points']
        # Remove the point with dupe z and y=0 (the bottom, handled by enclosure)
        new_pts = [p for p in pts if not (p[0] == dupe_z and p[1] == 0.0)]
        if len(new_pts) < len(pts):
            print(f"    Fix: removed duplicate z={dupe_z} y=0 point")
            spec['enclosure']['points'] = new_pts
            changed = True

    for k in ['w', 'd', 'h']:
        fk = f'dim_{k}'
        if fk in fixes:
            old = spec['dims'][k]
            new = fixes[fk]
            print(f"    Fix: dim {k} {old} → {new}")
            # Rescale z-coordinates if depth changed
            if k == 'd':
                scale = new / old
                for p in spec['enclosure']['points']:
                    p[0] = round(p[0] * scale, 4)
                # Rescale part z positions too
                for kpart in spec.get('knobs', []):
                    kpart['z'] = round(kpart['z'] * scale, 3)
                for key in ['footswitch', 'led', 'ibanezPlate']:
                    if key in spec and 'z' in spec[key]:
                        spec[key]['z'] = round(spec[key]['z'] * scale, 3)
                for lbl in spec.get('labels', []):
                    lbl['z'] = round(lbl['z'] * scale, 3)
                print(f"    Fix: rescaled z-coords by {scale:.4f}")
            spec['dims'][k] = new
            changed = True

    for jack in spec.get('jacks', []):
        fk = f"jack_{jack.get('id')}_y"
        if fk in fixes and 'y' in jack:
            print(f"    Fix: removed hardcoded y from jack {jack.get('id')}")
            del jack['y']
            changed = True

    if 'powerJack_y' in fixes and 'y' in spec.get('powerJack', {}):
        print(f"    Fix: removed hardcoded y from powerJack")
        del spec['powerJack']['y']
        changed = True

    return spec, changed

# ----------------------------------------------------------------------------
# Code checks (parts.js)
# ----------------------------------------------------------------------------

def check_code():
    """Check parts.js for known issues. Returns (passed, issues)."""
    print("\n  [Code] Checking parts.js...")
    issues = []

    with open(REPO / "parts.js") as f:
        code = f.read()

    # 1. Hardcoded y for jacks
    # Look for jack positioning that doesn't use surfaceAt
    if 'y: 1.275' in code or 'y=1.275' in code:
        issues.append("parts.js has hardcoded jack y=1.275 (must use surfaceAt)")

    # 2. Tick ring wedge count consistency
    # Code uses 11 positions with 1 skipped = 10 rendered wedges (gap at bottom).
    # This matches the real pedal. Check that the comment is accurate.
    if 'wedges = 11' in code and '10 trapezoidal wedges' not in code:
        issues.append("Tick ring: comment should clarify 11 positions = 10 rendered wedges")

    passed = len(issues) == 0
    for issue in issues:
        print(f"      FAIL: {issue}")
    if passed:
        print(f"      All code checks passed.")
    return passed, issues

def main():
    fix = '--fix' in sys.argv

    print("=" * 60)
    print("TS9 Self-Validation v2 (fresh image segmentation)")
    print("=" * 60)

    spec = load_spec()
    print(f"Spec: {spec['id']}")

    # 0. Consistency + code checks (must pass first)
    consist_pass, consist_issues, consist_fixes = check_spec_consistency(spec)
    code_pass, code_issues = check_code()

    if fix and not consist_pass:
        print("\n  [Fix] Applying consistency fixes...")
        spec, changed = apply_consistency_fixes(spec, consist_fixes)
        if changed:
            save_spec(spec)
            print("  Spec updated. Re-run to verify.")
            return 1

    if not consist_pass or not code_pass:
        print("\n" + "=" * 60)
        print("SUMMARY: FAIL — fix consistency/code issues first (run with --fix)")
        print("=" * 60)
        return 1

    # 1. Image validation (only if consistency passes)
    print("\n  [Top] Segmenting...")
    measured_top = segment_top()

    side = validate_side_fresh(spec)

    # Validate top using the fresh measurements
    print("\n  [Top] Comparing to spec...")
    errors = {}
    def check(name, spec_val, meas_val):
        if meas_val is None:
            return
        err = np.sqrt((spec_val['x']-meas_val['x'])**2 + (spec_val['z']-meas_val['z'])**2)
        errors[name] = err * 25.4
    for k in spec.get('knobs', []):
        if k['id'] in measured_top:
            check(f"knob-{k['id']}", k, measured_top[k['id']])
    for key in ['footswitch', 'led', 'ibanezPlate']:
        if key in spec and key in measured_top:
            check(key, spec[key], measured_top[key])
    top_max = max(errors.values()) if errors else 999
    top_pass = top_max <= PART_THRESHOLD_MM
    print(f"      Max: {top_max:.2f}mm → {'PASS' if top_pass else 'FAIL'}")
    top = {'max_mm': top_max, 'pass': top_pass}

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    sp = side.get('pass', False)
    print(f"  Side: {'PASS' if sp else 'FAIL'} ({side.get('max_mm', 0):.2f}mm)")
    print(f"  Top:  {'PASS' if top_pass else 'FAIL'} ({top_max:.2f}mm)")
    overall = sp and top_pass
    print(f"  Overall: {'PASS' if overall else 'FAIL — do not ship'}")

    if fix and not overall:
        print("\n  [Fix] Updating spec from measurements...")
        spec, changed = fix_from_measurements(spec, measured_top)
        if changed:
            save_spec(spec)
            print("  Spec updated. Re-run to verify.")
        else:
            print("  No changes needed (within rounding).")

    return 0 if overall else 1

if __name__ == '__main__':
    sys.exit(main())
