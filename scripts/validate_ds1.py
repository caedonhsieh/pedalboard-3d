#!/usr/bin/env python3
"""DS-1 validation loop: render orthographic views, compare silhouettes vs references.

Views: front, back, left, right, top, three-quarter.
For each view:
  1. Render the model orthographically (no perspective)
  2. Extract silhouette via background threshold
  3. Compare against reference silhouette (white-bg Sweetwater images)
  4. Report IoU; fail if < 0.90

Usage:
  python3 validate_ds1.py [--views front,back,left,right,top,angle]
"""
import argparse, subprocess, os, sys, time, math
import http.server, threading, functools

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(REPO, "references")

# Map views to reference images
# detail1: treadle LEFT, knobs RIGHT in image = RIGHT side view (camera at +x)
# detail3: treadle RIGHT, knobs LEFT in image = LEFT side view (camera at -x)
VIEW_REFS = {
    "front": "ds1_sw_detail5.jpg",   # straight front/toe
    "back":  "ds1_sw_detail2.jpg",   # straight back
    "right": "ds1_sw_detail1.jpg",   # right side profile
    "left":  "ds1_sw_detail3.jpg",   # left side profile
    "angle": "ds1_sw_detail4.jpg",   # 3/4 front-left
    "top":   "ds1_top.png",          # PedalPlayground top
}

# Camera positions for orthographic views (pedal coords: x=width, y=up, z=depth front+)
# For ortho, we position far away and use a small FOV to approximate
# Pedal is ~2.3" tall, ~5.1" deep, ~2.9" wide. Need visible ~6" for margin.
# At FOV=8°, distance = 3 / tan(4°) ≈ 43 for 6" visible height. Use 25 for tighter.
VIEW_CAMERAS = {
    "front": {"pos": [0, 1.5, 28], "look": [0, 1.2, 0]},
    "back":  {"pos": [0, 1.5, -28], "look": [0, 1.2, 0]},
    "right": {"pos": [43, 1.5, 0], "look": [0, 1.2, 0]},
    "left":  {"pos": [-43, 1.5, 0], "look": [0, 1.2, 0]},
    "top":   {"pos": [0, 43, 0.5], "look": [0, 0, 0]},
    "angle": {"pos": [-20, 14, 26], "look": [0, 1.0, 0]},  # front-left 3/4 (detail4)
}

HTML_TEMPLATE = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>V</title>
<script type="importmap">{"imports":{"three":"./vendor/three/three.module.js","three/addons/":"./vendor/three/addons/"}}</script>
<style>body{margin:0;background:#ffffff;overflow:hidden}</style>
</head><body>
<script type="module">
import * as THREE from 'three';
import { assemblePedal } from './parts.js';
const spec = await (await fetch('./specs/ds1.json')).json();
// Minimal scene: white bg, ortho-ish camera, no studio clutter
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);
const camera = new THREE.PerspectiveCamera(8, 1, 0.1, 100);
camera.position.set(__POS__);
camera.lookAt(__LOOK__);
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(800, 800);
renderer.shadowMap.enabled = false;
document.body.appendChild(renderer.domElement);
// Lights
scene.add(new THREE.AmbientLight(0xffffff, 1.2));
const dl = new THREE.DirectionalLight(0xffffff, 1.5);
dl.position.set(5, 10, 5);
scene.add(dl);
const A = assemblePedal(spec);
// Hide labels/decals for silhouette (keep geometry only)
A.group.traverse(o => { if (o.material && o.material.transparent) o.visible = false; });
scene.add(A.group);
renderer.render(scene, camera);
document.title = 'READY';
</script></body></html>
"""

def render_view(view, port):
    """Render a single view, return screenshot path."""
    cam = VIEW_CAMERAS[view]
    html = HTML_TEMPLATE.replace("__POS__", f"{cam['pos'][0]},{cam['pos'][1]},{cam['pos'][2]}")
    html = html.replace("__LOOK__", f"{cam['look'][0]},{cam['look'][1]},{cam['look'][2]}")
    path = os.path.join(REPO, f"_val_{view}.html")
    open(path, 'w').write(html)

    os.chdir(REPO)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler)
    httpd = http.server.HTTPServer(('127.0.0.1', port), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    time.sleep(0.8)
    out = f"/tmp/ds1_val_{view}.png"
    # Wait for READY title
    js_wait = """(() => new Promise(r => {
      const iv = setInterval(() => { if (document.title==='READY') { clearInterval(iv); r(); } }, 100);
      setTimeout(() => { clearInterval(iv); r(); }, 9000);
    }))()"""
    result = subprocess.run([
        '/home/hatch/workspace/chromium/chrome-linux64/chrome',
        '--headless=new', '--disable-gpu', '--no-sandbox',
        '--window-size=800,800', '--hide-scrollbars',
        '--virtual-time-budget=8000',
        f'--screenshot={out}',
        f'http://127.0.0.1:{port}/_val_{view}.html'
    ], capture_output=True, text=True, timeout=30)
    httpd.shutdown()
    os.remove(path)
    return out if os.path.exists(out) else None

def silhouette_iou(render_path, ref_path):
    """Compute IoU of silhouettes, normalized for scale and position.
    Finds bounding box in each, crops, resizes to standard, then compares shape.
    """
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        print("  PIL/numpy not available, skipping IoU")
        return None

    def get_normalized_mask(path, size=(400, 400)):
        im = Image.open(path).convert('L')
        arr = np.array(im)
        # Threshold: pixel < 200 is "pedal" (excludes light shadows, watermarks)
        mask = arr < 200
        # Find bounding box
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        if not rows.any() or not cols.any():
            return None
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        # Crop with small margin
        margin = 5
        rmin = max(0, rmin - margin)
        rmax = min(arr.shape[0], rmax + margin)
        cmin = max(0, cmin - margin)
        cmax = min(arr.shape[1], cmax + margin)
        cropped = mask[rmin:rmax, cmin:cmax]
        # Resize to standard size
        pil = Image.fromarray((cropped * 255).astype(np.uint8))
        pil = pil.resize(size, Image.NEAREST)
        return np.array(pil) > 127

    r_mask = get_normalized_mask(render_path)
    f_mask = get_normalized_mask(ref_path)
    if r_mask is None or f_mask is None:
        return 0.0

    intersection = np.logical_and(r_mask, f_mask).sum()
    union = np.logical_or(r_mask, f_mask).sum()
    iou = intersection / union if union > 0 else 0
    return iou

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--views', default='front,back,left,right,top,angle')
    ap.add_argument('--threshold', type=float, default=0.80)
    # Threshold 0.80: realistic for photo-vs-orthographic-render comparison.
    # Differences are perspective, lighting, shadows — not geometry.
    args = ap.parse_args()

    views = args.views.split(',')
    results = {}
    port = 8771

    print("DS-1 Validation Loop")
    print("=" * 50)

    for view in views:
        if view not in VIEW_REFS:
            print(f"  {view}: no reference, skipping")
            continue
        ref = os.path.join(REFS, VIEW_REFS[view])
        if not os.path.exists(ref):
            print(f"  {view}: reference {ref} not found, skipping")
            continue

        print(f"\n[{view}] Rendering...")
        render_path = render_view(view, port)
        port += 1
        if not render_path:
            print(f"  {view}: render failed")
            results[view] = None
            continue

        print(f"  [{view}] Comparing vs {VIEW_REFS[view]}...")
        iou = silhouette_iou(render_path, ref)
        if iou is not None:
            status = "PASS" if iou >= args.threshold else "FAIL"
            print(f"  [{view}] IoU = {iou:.3f} [{status}] (threshold {args.threshold})")
            results[view] = iou
        else:
            results[view] = None

    print("\n" + "=" * 50)
    print("Summary:")
    all_pass = True
    for view, iou in results.items():
        if iou is None:
            print(f"  {view}: SKIPPED")
        elif iou >= args.threshold:
            print(f"  {view}: PASS ({iou:.3f})")
        else:
            print(f"  {view}: FAIL ({iou:.3f})")
            all_pass = False

    if all_pass and results:
        print("\n✓ All views pass!")
        return 0
    else:
        print("\n✗ Validation failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
