#!/usr/bin/env python3
"""Self-fixing loop: automatically adjust spec params to pass validation.

The loop:
  1. Loads the spec and measured references.
  2. Computes the validation error (calibrated, mm-based).
  3. Uses coordinate descent to adjust params, minimizing error.
  4. Stops when all thresholds pass or max iterations reached.
  5. NEVER lowers thresholds; only changes the spec.

This is the "self-improving" loop: it measures, diagnoses, fixes, and
re-validates without human input.

Usage: self_fix.py [--perturb] [--max-iter N]
  --perturb: start from a perturbed spec (to demonstrate fixing)
"""
import json, os, sys, math, copy, argparse

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Params the loop is allowed to adjust: (json_path, step_inches, min, max)
# Each entry: (["knobs", idx, "x"], step, min, max)
PARAMS = []

def load_spec():
    with open(os.path.join(REPO, "specs/ds1.json")) as f:
        return json.load(f)

def load_refs():
    with open(os.path.join(REPO, "references/ds1_landmarks.json")) as f:
        lm = json.load(f)
    with open(os.path.join(REPO, "references/ds1_side_profile.json")) as f:
        prof = json.load(f)
    return lm, prof

def get_param(spec, path):
    obj = spec
    for p in path[:-1]:
        obj = obj[p]
    return obj[path[-1]]

def set_param(spec, path, val):
    obj = spec
    for p in path[:-1]:
        obj = obj[p]
    obj[path[-1]] = val

def validation_error(spec, lm, prof):
    """Total error in mm (lower is better). Also returns per-check errors."""
    errs = {}
    # knobs
    for k in spec["knobs"]:
        kid = k["id"]
        if kid in lm["knobs"]:
            sx, sz = k["x"] * 25.4, k["z"] * 25.4
            mx, mz = lm["knobs"][kid]["mm"]
            errs[f"knob_{kid}"] = math.hypot(sx - mx, sz - mz)
    # pad
    fs = spec["footswitch"]
    errs["pad_center"] = abs(fs["padCz"] * 25.4 - lm["pad"]["center_mm"][1])
    errs["pad_width"] = abs(fs["padW"] * 25.4 - lm["pad"]["size_mm"][0])
    errs["pad_depth"] = abs(fs["padD"] * 25.4 - lm["pad"]["size_mm"][1])
    # profile
    pts = spec["enclosure"]["points"]
    front_y = max(p[1] for p in pts if p[0] > 2.5) * 25.4
    back_y = max(p[1] for p in pts if p[0] < -2.5) * 25.4
    errs["front_height"] = abs(front_y - prof["front_height_mm"])
    errs["back_height"] = abs(back_y - prof["back_height_mm"])
    total = sum(errs.values())
    return total, errs

def build_params(spec):
    """Build the adjustable param list."""
    params = []
    for i, k in enumerate(spec["knobs"]):
        # x and z for each knob, step 0.5mm, bounds ±5mm from current
        for coord in ("x", "z"):
            cur = k[coord]
            params.append((["knobs", i, coord], 0.02, cur - 0.2, cur + 0.2))
    fs = spec["footswitch"]
    for key in ("padW", "padD", "padCz"):
        cur = fs[key]
        params.append((["footswitch", key], 0.02, cur - 0.2, cur + 0.2))
    # front height: adjust the front-top point's y
    # (points[3] is front-top: [2.5394, y])
    pts = spec["enclosure"]["points"]
    # find front-top point (max z)
    fi = max(range(len(pts)), key=lambda i: pts[i][0])
    cur = pts[fi][1]
    params.append((["enclosure", "points", fi, 1], 0.02, cur - 0.2, cur + 0.2))
    return params

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perturb", action="store_true")
    ap.add_argument("--max-iter", type=int, default=50)
    args = ap.parse_args()

    spec = load_spec()
    lm, prof = load_refs()

    if args.perturb:
        # Introduce errors to demonstrate fixing
        print("Perturbing spec to demonstrate self-fixing...")
        spec["knobs"][0]["x"] += 0.1  # tone 2.5mm off
        spec["knobs"][2]["z"] -= 0.08  # dist 2mm off
        spec["footswitch"]["padW"] -= 0.08
        spec["enclosure"]["points"][3][1] += 0.1  # front 2.5mm too tall

    params = build_params(spec)
    total, errs = validation_error(spec, lm, prof)
    print(f"Initial error: {total:.2f}mm")
    for k, v in errs.items():
        print(f"  {k}: {v:.2f}mm")

    # Coordinate descent
    for it in range(args.max_iter):
        improved = False
        for path, step, lo, hi in params:
            cur = get_param(spec, path)
            best_val, best_err = cur, total
            for delta in (-step, step):
                trial = max(lo, min(hi, cur + delta))
                set_param(spec, path, trial)
                t2, _ = validation_error(spec, lm, prof)
                if t2 < best_err - 1e-9:
                    best_err, best_val = t2, trial
            # restore the best (or original if no improvement)
            set_param(spec, path, best_val)
            if best_err < total - 1e-9:
                total = best_err
                improved = True
        print(f"Iter {it+1}: error={total:.3f}mm")
        if not improved:
            print("Converged (no improvement).")
            break

    total, errs = validation_error(spec, lm, prof)
    print(f"\nFinal error: {total:.2f}mm")
    all_pass = True
    thresholds = {"knob": 2.0, "pad": 3.0, "front_height": 2.0, "back_height": 1.0}
    for k, v in errs.items():
        th = thresholds.get(k.split("_")[0], 2.0)
        if "front" in k: th = 2.0
        if "back" in k: th = 1.0
        passed = v <= th
        all_pass &= passed
        print(f"  {k}: {v:.2f}mm (thresh {th}mm) {'PASS' if passed else 'FAIL'}")

    if all_pass:
        # Save the fixed spec
        with open(os.path.join(REPO, "specs/ds1.json"), "w") as f:
            json.dump(spec, f, indent=2)
        print("\nAll checks PASS. Spec saved.")
        return 0
    else:
        print("\nFAILURES remain after optimization.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
