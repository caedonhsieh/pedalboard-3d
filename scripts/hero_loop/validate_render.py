#!/usr/bin/env python3
"""Render-based validation: measure the RENDERED model, not the spec numbers.

Uses loop_harness.html mask modes with orthographic cameras of known scale.
Detects components in the render, converts to mm, compares to measured
landmarks. Catches bugs where parts.js renders differently from the spec.

Usage: validate_render.py [--port PORT]
Returns 0 if all pass, 1 otherwise. Prints errors in mm.
"""
import json, os, subprocess, sys, math, time
import http.server, threading, functools
import urllib.parse
import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHROME = "/home/hatch/workspace/chromium/chrome-linux64/chrome"

THRESHOLDS = {
    "knob_pos_mm": 2.5,
    "pad_center_mm": 3.5,
    "pad_size_mm": 3.5,
    "front_height_mm": 2.5,
    "back_height_mm": 1.5,
}

# Ortho view definitions: (name, cam_spec, mm_per_px)
# Top: looking down -Y. half-height 4in -> 800px = 8in = 203.2mm
TOP_CAM = {"type": "ortho", "scale": 4.0, "pos": [0, 20, 0], "look": [0, 0, 0]}
TOP_MMPP = 203.2 / 800
# Side: looking from +X (right side). half-height 4in.
SIDE_CAM = {"type": "ortho", "scale": 4.0, "pos": [20, 2, 0], "look": [0, 2, 0]}
SIDE_MMPP = 203.2 / 800

def render(mask_kind, cam, w=800, h=800, port=8796):
    os.chdir(REPO)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler)
    httpd = http.server.HTTPServer(('127.0.0.1', port), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.5)
    cam_q = urllib.parse.quote(json.dumps(cam))
    mode = f"mask:{mask_kind}" if mask_kind else "silhouette"
    url = (f"http://127.0.0.1:{port}/loop_harness.html?spec=./specs/ds1.json"
           f"&mode={mode}&cam={cam_q}&w={w}&h={h}")
    out = f"/tmp/rv_{mask_kind or 'sil'}_{int(time.time()*1000)%100000}.png"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
                    f"--window-size={w},{h}", "--hide-scrollbars",
                    "--virtual-time-budget=8000", f"--screenshot={out}", url],
                   capture_output=True, timeout=40)
    httpd.shutdown()
    for _ in range(30):
        if os.path.exists(out) and os.path.getsize(out) > 2000:
            break
        time.sleep(0.3)
    return np.array(Image.open(out).convert("RGB"))

def detect_centroids(mask, min_area=200):
    """Connected components -> list of (cx, cy, area)."""
    import cv2
    n, lab, stats, cent = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    out = []
    for i in range(1, n):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            out.append((cent[i][0], cent[i][1], stats[i, cv2.CC_STAT_AREA]))
    return out

def main():
    import cv2
    with open(os.path.join(REPO, "references/ds1_landmarks.json")) as f:
        lm = json.load(f)
    with open(os.path.join(REPO, "references/ds1_side_profile.json")) as f:
        prof = json.load(f)

    results = {}
    ok = True

    # --- knobs from top mask ---
    print("=== Render: knobs (top ortho mask) ===")
    img = render("knob", TOP_CAM)
    red = (img[:, :, 0] > 200) & (img[:, :, 1] < 100) & (img[:, :, 2] < 100)
    blobs = detect_centroids(red, min_area=300)
    print(f"  detected {len(blobs)} knob blobs")
    # ortho top: image center = pedal center (0,0). +x right, +z DOWN in image.
    # mm: dx_px * mmpp -> x_mm; dy_px * mmpp -> z_mm (image y down = +z front)
    blobs_sorted = sorted(blobs, key=lambda b: b[0])  # left to right
    names = ["tone", "level", "dist"]
    if len(blobs_sorted) >= 3:
        # match left-to-right; level is center
        for (cx, cy, a), name in zip(blobs_sorted, names):
            x_mm = (cx - 400) * TOP_MMPP
            z_mm = (cy - 400) * TOP_MMPP
            mx, mz = lm["knobs"][name]["mm"]
            err = math.hypot(x_mm - mx, z_mm - mz)
            passed = err <= THRESHOLDS["knob_pos_mm"]
            ok &= passed
            results[f"render_knob_{name}"] = round(err, 2)
            print(f"  {name}: render=({x_mm:.1f},{z_mm:.1f}) measured=({mx:.1f},{mz:.1f}) err={err:.2f}mm {'PASS' if passed else 'FAIL'}")
    else:
        print("  FAIL: expected 3 knob blobs")
        ok = False

    # --- pad from top mask ---
    print("=== Render: pad (top ortho mask) ===")
    img = render("treadle", TOP_CAM)
    green = (img[:, :, 1] > 200) & (img[:, :, 0] < 100) & (img[:, :, 2] < 100)
    blobs = detect_centroids(green, min_area=1000)
    if blobs:
        # largest = pad (or plate); take largest
        cx, cy, a = max(blobs, key=lambda b: b[2])
        # bbox for size
        ys, xs = np.where(green)
        w_mm = (xs.max() - xs.min()) * TOP_MMPP
        d_mm = (ys.max() - ys.min()) * TOP_MMPP
        cz_mm = (cy - 400) * TOP_MMPP
        mz = lm["pad"]["center_mm"][1]
        mw, md = lm["pad"]["size_mm"]
        for name, err, th in [("pad_center", abs(cz_mm - mz), THRESHOLDS["pad_center_mm"]),
                              ("pad_width", abs(w_mm - mw), THRESHOLDS["pad_size_mm"]),
                              ("pad_depth", abs(d_mm - md), THRESHOLDS["pad_size_mm"])]:
            passed = err <= th
            ok &= passed
            results[f"render_{name}"] = round(err, 2)
            print(f"  {name}: err={err:.2f}mm {'PASS' if passed else 'FAIL'}")
    else:
        print("  FAIL: no treadle mask found")
        ok = False

    print(f"\n{'ALL RENDER CHECKS PASS' if ok else 'RENDER FAILURES PRESENT'}")
    with open("/tmp/validate_render_results.json", "w") as f:
        json.dump(results, f, indent=2)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
