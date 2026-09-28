#!/usr/bin/env python3
"""
Self-validating, self-fixing loop for TS9 hero model.

Measures the side-profile photo, compares against the spec's profile,
optimizes the spec parameters to minimize silhouette error, and fixes
knob recess from measured knob heights — no human eyeballing.

Usage: python3 fit_ts9.py [--iterations N] [--write]
  --write: actually update specs/ts9.json (default: dry run, report only)

The loop:
  1. MEASURE: extract photo silhouette (top edge) + knob heights
  2. PREDICT: compute model's silhouette from spec profile points
  3. COMPARE: RMS pixel error between model and photo edges
  4. FIX: coordinate-descent on profile y/z + knob recess
  5. VALIDATE: re-compute error; loop until converged or stalled
"""

import json, argparse, copy
import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes, binary_opening, binary_closing

PHOTO = '/home/hatch/workspace/user/media_library/image/57/57ccfa5b5018878a1eb8243c8c5c2d311db55cc3dae415c8e0faceba40824819.png'
SPEC = '/home/hatch/workspace/pedalboard-3d/repo/specs/ts9.json'

# Photo geometry (measured)
PX_W = 744.0   # body x=2..746
PX_X0 = 2.0
PX_TOP = 17.0    # peak pixel y
PX_BOT = 306.0   # bottom pixel y
IN_D = 4.9       # depth inches (z: -2.45..2.45)
IN_H = 2.09      # peak height inches (53mm mfr spec)

def z_to_x(z):
    return PX_X0 + (z + IN_D/2) / IN_D * PX_W

def y_to_py(y):
    return PX_BOT - (y / IN_H) * (PX_BOT - PX_TOP)

def x_to_z(x):
    return (x - PX_X0) / PX_W * IN_D - IN_D/2

def py_to_y(py):
    return (PX_BOT - py) / (PX_BOT - PX_TOP) * IN_H

def extract_photo():
    """Returns dict with top edge array, knob measurements."""
    img = Image.open(PHOTO).convert('RGB')
    a = np.array(img)
    H, W = a.shape[:2]
    r, g, b = a[:,:,0].astype(int), a[:,:,1].astype(int), a[:,:,2].astype(int)
    gm = (g > 90) & (g > r + 25) & (g > b + 25) & (r < 150)
    gm = binary_closing(binary_opening(gm, structure=np.ones((3,3))), structure=np.ones((5,5)))
    filled = binary_fill_holes(gm)
    tops = np.full(W, -1)
    for x in range(W):
        col = np.where(filled[:, x])[0]
        if len(col) > 10:
            tops[x] = col.min()
    # Knobs: find the top edge where background (light) transitions to knob (dark)
    # The knob top is the first row going down where pixels become dark,
    # not the first dark pixel (which might be a gray transition).
    knobs = []
    for xc in [100, 150, 200]:
        # Scan down from y=0 to find the transition
        top_y = None
        for y in range(0, 60):
            r_v, g_v, b_v = a[y, xc].astype(int)
            # Background is light (r>200), knob is dark (r<100)
            # Find first y where it's clearly knob (not transition)
            if r_v < 80 and g_v < 80 and b_v < 80:
                # Verify it's actually the knob by checking a few more rows are also dark
                if all(a[y+i, xc, 0] < 100 for i in range(3)):
                    top_y = y
                    break
        if top_y is not None:
            deck_y = int(tops[xc])
            # Only accept if top_y is well below image top (not cropped)
            # and above the deck
            if top_y > 2 and top_y < deck_y - 10:
                knobs.append({'x': xc, 'top_y': top_y, 'deck_y': deck_y})
    return {'tops': tops, 'knobs': knobs, 'W': W}

def model_top_edge(points, xs):
    """
    Given profile points [(z,y)...] (top edge, rear to front),
    return interpolated model top y (in pixels) at each x in xs.
    """
    # Convert points to pixel space
    px_pts = [(z_to_x(z), y_to_py(y)) for z, y in points]
    px_pts.sort(key=lambda p: p[0])
    px_xs = [p[0] for p in px_pts]
    px_ys = [p[1] for p in px_pts]
    # Linear interpolate (sharp hexagon, no smoothing)
    return np.interp(xs, px_xs, px_ys, left=px_ys[0], right=px_ys[-1])

def silhouette_error(points, photo):
    """RMS pixel error between model top edge and photo top edge."""
    tops = photo['tops']
    # Use clean x ranges:
    # - exclude x<7 (slanted rear face, not top edge)
    # - exclude 250..390 (knob/jack contamination)
    # - exclude x>738 (rounded front corner)
    xs_clean = [x for x in range(7, 739)
                if tops[x] > 0 and not (250 <= x <= 390)]
    xs = np.array(xs_clean)
    model_ys = model_top_edge(points, xs)
    photo_ys = tops[xs].astype(float)
    err = model_ys - photo_ys
    return float(np.sqrt(np.mean(err**2))), xs, err

def knob_error(points, recess, photo, spec_knobs):
    """
    Compare model knob top height vs photo.
    Returns (rms_error, details). If knobs are cropped in the photo
    (top_y < 15px from image top), returns (None, 'cropped') to signal
    that validation is impossible from this photo.
    """
    # Check for cropping: if any knob top is within 2px of image top,
    # the photo is cropped and we cannot measure true height.
    for km in photo['knobs']:
        if km['top_y'] <= 2:
            return None, 'cropped'
    KNOB_H_IN = 0.65  # total knob height (skirt 0.60 + cap 0.05)
    errs = []
    for i, km in enumerate(photo['knobs']):
        if i >= len(spec_knobs):
            break
        sk = spec_knobs[i]
        z = sk['z']
        zs = [p[0] for p in points]
        ys = [p[1] for p in points]
        deck_y_in = np.interp(z, zs, ys)
        deck_py = y_to_py(deck_y_in)
        model_top_py = deck_py - (KNOB_H_IN - recess) / IN_H * (PX_BOT - PX_TOP)
        photo_top_py = km['top_y']
        errs.append(model_top_py - photo_top_py)
    if not errs:
        return 0.0, []
    return float(np.sqrt(np.mean(np.array(errs)**2))), errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--iterations', type=int, default=50)
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()

    with open(SPEC) as f:
        spec = json.load(f)

    photo = extract_photo()
    print(f"Photo: {len(photo['knobs'])} knobs measured")
    for k in photo['knobs']:
        print(f"  x={k['x']}: top_y={k['top_y']}, deck_y={k['deck_y']}, visible={k['deck_y']-k['top_y']}px")

    points = [list(p) for p in spec['enclosure']['points']]
    recess = spec['knobs'][0].get('recess', 0.05)

    print(f"\nStarting profile: {points}")
    print(f"Starting recess: {recess}")

    err0, _, _ = silhouette_error(points, photo)
    kerr0, k_detail0 = knob_error(points, recess, photo, spec['knobs'])
    print(f"\nInitial silhouette RMS: {err0:.2f}px")
    if k_detail0 == 'cropped':
        print(f"Initial knob RMS: SKIPPED (cropped photo)")
    else:
        print(f"Initial knob RMS: {kerr0:.2f}px")

    # --- Coordinate descent on profile ---
    # Params: y of points[0], y of points[1], z of points[1], z of points[2],
    #         y of points[3], z of points[3]
    # (peak y fixed at 2.09 = mfr spec; rear/front z fixed by depth; front bottom y=0)
    best = [list(p) for p in points]
    best_err, _, _ = silhouette_error(best, photo)

    # param: (point_idx, coord) where coord 0=z, 1=y
    params = [(0,1), (1,0), (1,1), (2,0), (3,0), (3,1)]
    steps = {(0,1): 0.02, (1,0): 0.02, (1,1): 0.02, (2,0): 0.02, (3,0): 0.02, (3,1): 0.02}

    for it in range(args.iterations):
        improved = False
        for pi, ci in params:
            for direction in (+1, -1):
                trial = [list(p) for p in best]
                trial[pi][ci] += direction * steps[(pi,ci)]
                # Constraints
                if ci == 1:  # y must be 0..2.2
                    if not (0 <= trial[pi][ci] <= 2.2):
                        continue
                if (pi,ci) == (2,0):  # peak z in [-0.5, 0.5]
                    if not (-0.5 <= trial[pi][ci] <= 0.5):
                        continue
                # z must stay ordered
                zs = [trial[i][0] for i in range(len(trial))]
                if any(zs[i] >= zs[i+1] for i in range(len(zs)-1)):
                    continue
                e, _, _ = silhouette_error(trial, photo)
                if e < best_err - 1e-6:
                    best_err = e
                    best = trial
                    improved = True
        if not improved:
            # shrink steps
            for k in steps:
                steps[k] *= 0.5
            if max(steps.values()) < 1e-4:
                print(f"Converged at iteration {it}")
                break

    print(f"\nOptimized profile: {[[round(v,3) for v in p] for p in best]}")
    print(f"Silhouette RMS: {err0:.2f} -> {best_err:.2f}px")

    # --- Fix knob recess from measured heights ---
    # Skip if photo is cropped (cannot measure true knob height)
    kerr_best, k_detail = knob_error(best, recess, photo, spec['knobs'])
    if k_detail == 'cropped':
        print(f"\nKnob validation: SKIPPED (photo crops knobs at image top, cannot measure true height)")
        print(f"Knob recess kept at: {recess:.3f}")
        best_recess = recess
        kerr0 = kerr_best = 0.0  # don't report invalid numbers
    else:
        # Solve for recess that minimizes knob error
        best_recess = recess
        for r_try in np.arange(0.0, 0.30, 0.005):
            ke, _ = knob_error(best, r_try, photo, spec['knobs'])
            if ke is not None and ke < kerr_best:
                kerr_best = ke
                best_recess = r_try
        print(f"\nKnob recess: {recess:.3f} -> {best_recess:.3f}")
        print(f"Knob RMS: {kerr0:.2f} -> {kerr_best:.2f}px")

    # --- Validate ---
    print(f"\n=== VALIDATION ===")
    print(f"Silhouette: {err0:.2f}px -> {best_err:.2f}px {'PASS' if best_err < 3.0 else 'FAIL'} (threshold 3px)")
    if k_detail == 'cropped':
        print(f"Knobs: SKIPPED (cropped photo — need uncropped side view for validation)")
    else:
        print(f"Knobs: {kerr0:.2f}px -> {kerr_best:.2f}px {'PASS' if kerr_best < 5.0 else 'FAIL'} (threshold 5px)")

    if args.write:
        spec['enclosure']['points'] = [[round(v, 4) for v in p] for p in best]
        if k_detail != 'cropped':
            for k in spec['knobs']:
                k['recess'] = round(float(best_recess), 4)
            knob_note = f"knob recess {best_recess:.3f}in from measured heights."
        else:
            knob_note = "knob recess NOT auto-fit (photo crops knobs)."
        spec['enclosure']['notes'] = (
            spec['enclosure'].get('notes', '') +
            f" [AUTO-FIT 2026-09-28: profile optimized against side-photo silhouette "
            f"(RMS {best_err:.1f}px). {knob_note}]"
        )
        with open(SPEC, 'w') as f:
            json.dump(spec, f, indent=2)
        print(f"\nWrote updated {SPEC}")
    else:
        print("\nDry run — use --write to apply")

if __name__ == '__main__':
    main()
