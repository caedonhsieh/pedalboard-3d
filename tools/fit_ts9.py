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
    # Knobs: dark pixels in upper-left, find each knob's top and the deck below
    dark = (r < 60) & (g < 60) & (b < 60)
    knobs = []
    # Three knobs expected around x=100,150,200 — find dark clusters
    for xc in [100, 150, 200]:
        # search x window
        x0, x1 = xc-30, xc+30
        region = dark[:, x0:x1]
        cols = np.where(region.any(axis=0))[0]
        if len(cols) == 0:
            continue
        # knob top = min y of dark in this window (above deck)
        # deck y = tops at center
        sub = np.where(dark[:, x0:x1].any(axis=1))[0]
        # filter to y < deck (above the deck line)
        deck_y = tops[xc]
        above = sub[sub < deck_y - 5]
        if len(above) > 0:
            knobs.append({'x': xc, 'top_y': int(above.min()), 'deck_y': int(deck_y)})
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
    Model knob top = deck_y(at knob z) - recess + knob_visible_height.
    We measure the visible knob height from photo and solve for recess.
    Returns list of (measured_visible_px, model_visible_px) and error.
    """
    # Knob geometry from parts.js ts9Knob: skirt 0.40" tall, cap on top
    # Visible height above deck = 0.40 - recess + cap_height
    # For simplicity, measure total visible from photo and compare to model
    # Model: deck_y_px - recess_px ... knob top = deck - recess + knob_h
    # Photo: knob_top_y, deck_y → visible_px = deck_y - knob_top_y
    KNOB_H_IN = 0.55  # total knob height above base (skirt 0.40 + cap ~0.15)
    errs = []
    for i, km in enumerate(photo['knobs']):
        if i >= len(spec_knobs):
            break
        sk = spec_knobs[i]
        # deck height at knob z from profile
        z = sk['z']
        # interpolate profile y at z
        zs = [p[0] for p in points]
        ys = [p[1] for p in points]
        deck_y_in = np.interp(z, zs, ys)
        deck_py = y_to_py(deck_y_in)
        # model knob top
        model_top_py = deck_py - (KNOB_H_IN - recess) / IN_H * (PX_BOT - PX_TOP)
        # photo knob top
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
    kerr0, _ = knob_error(points, recess, photo, spec['knobs'])
    print(f"\nInitial silhouette RMS: {err0:.2f}px")
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
    # Solve for recess that minimizes knob error
    best_recess = recess
    kerr_best, _ = knob_error(best, best_recess, photo, spec['knobs'])
    for r_try in np.arange(0.0, 0.30, 0.005):
        ke, _ = knob_error(best, r_try, photo, spec['knobs'])
        if ke < kerr_best:
            kerr_best = ke
            best_recess = r_try
    print(f"\nKnob recess: {recess:.3f} -> {best_recess:.3f}")
    print(f"Knob RMS: {kerr0:.2f} -> {kerr_best:.2f}px")

    # --- Validate ---
    print(f"\n=== VALIDATION ===")
    print(f"Silhouette: {err0:.2f}px -> {best_err:.2f}px {'PASS' if best_err < 3.0 else 'FAIL'} (threshold 3px)")
    print(f"Knobs: {kerr0:.2f}px -> {kerr_best:.2f}px {'PASS' if kerr_best < 5.0 else 'FAIL'} (threshold 5px)")

    if args.write:
        spec['enclosure']['points'] = [[round(v, 4) for v in p] for p in best]
        for k in spec['knobs']:
            k['recess'] = round(float(best_recess), 4)
        spec['enclosure']['notes'] = (
            spec['enclosure'].get('notes', '') +
            f" [AUTO-FIT 2026-09-28: profile optimized against side-photo silhouette "
            f"(RMS {best_err:.1f}px), knob recess {best_recess:.3f}in from measured heights.]"
        )
        with open(SPEC, 'w') as f:
            json.dump(spec, f, indent=2)
        print(f"\nWrote updated {SPEC}")
    else:
        print("\nDry run — use --write to apply")

if __name__ == '__main__':
    main()
