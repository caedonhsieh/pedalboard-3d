#!/usr/bin/env python3
"""
TS9 AI Mesh Generator
=====================
Generates 3D meshes from the TS9 reference photos using TripoSR.

Usage:
    python3 scripts/generate_ts9_mesh.py

What it does:
    1. Checks Python, torch, and device (CUDA/MPS/CPU)
    2. Installs TripoSR + rembg if missing
    3. Downloads the side + top reference photos
    4. Removes backgrounds (TripoSR needs clean subject)
    5. Generates a mesh from each photo
    6. Saves as GLB in output/ts9_meshes/

Requirements:
    - Python 3.8+
    - ~2GB disk for models
    - GPU strongly recommended (CPU will work but slow)

The meshes are REFERENCE ONLY — they hallucinate unseen sides.
The parametric model (specs/ts9.json) stays the source of truth.
"""

import os
import sys
import subprocess
import urllib.request
from pathlib import Path

# ----------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "output" / "ts9_meshes"
REFS = {
    # Side view (Sweetwater-style product photo)
    "side": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWSFI3sh7EMHpJ2Ib_HzPLNQxrFtuvrHNgOwaY1whBsQ&s=10",
    # Top view (Sweetwater high-res)
    "top": "https://media.sweetwater.com/m/products/image/29a2414665T6pyenFpcASI7sBWwbVbS9ucJiSa6v.jpg?ha=29a2414665765b3773d22e551ff6429c8381ad32&quality=82",
}

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def run(cmd, **kw):
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True, **kw)

def pip_install(pkg):
    run([sys.executable, "-m", "pip", "install", pkg])

def ensure_import(name, pip_name=None):
    try:
        __import__(name)
        print(f"  [ok] {name}")
        return True
    except ImportError:
        print(f"  [missing] {name} — installing...")
        pip_install(pip_name or name)
        return False

# ----------------------------------------------------------------------------
# Step 1: Environment
# ----------------------------------------------------------------------------
print("=" * 60)
print("Step 1: Environment check")
print("=" * 60)
assert sys.version_info >= (3, 8), "Python 3.8+ required"
print(f"  Python {sys.version}")

ensure_import("torch")
ensure_import("PIL", "pillow")
ensure_import("numpy")
ensure_import("rembg")

import torch
if torch.cuda.is_available():
    device = "cuda"
elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"
    print("\n  ⚠ No GPU detected. CPU mesh generation will be SLOW (~10-20 min per image).")
    print("  Consider running on a machine with CUDA or Apple Silicon GPU.")
print(f"  Device: {device}")

# ----------------------------------------------------------------------------
# Step 2: TripoSR
# ----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Step 2: TripoSR")
print("=" * 60)
try:
    import tsr
    print("  [ok] tsr (TripoSR)")
except ImportError:
    print("  Installing TripoSR from GitHub...")
    # TripoSR needs to be installed from source
    run([sys.executable, "-m", "pip", "install", "git+https://github.com/VAST-AI-Research/TripoSR.git"])
    import tsr

# ----------------------------------------------------------------------------
# Step 3: Download references
# ----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Step 3: Download reference photos")
print("=" * 60)
OUT_DIR.mkdir(parents=True, exist_ok=True)
ref_paths = {}
for name, url in REFS.items():
    dest = OUT_DIR / f"ts9_{name}_ref.jpg"
    if not dest.exists():
        print(f"  Downloading {name}...")
        urllib.request.urlretrieve(url, dest)
        print(f"  Saved {dest} ({dest.stat().st_size // 1024}KB)")
    else:
        print(f"  [cached] {dest}")
    ref_paths[name] = dest

# ----------------------------------------------------------------------------
# Step 4: Background removal
# ----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Step 4: Background removal (rembg)")
print("=" * 60)
from rembg import remove
from PIL import Image

clean_paths = {}
for name, path in ref_paths.items():
    clean = OUT_DIR / f"ts9_{name}_clean.png"
    if not clean.exists():
        print(f"  Removing background from {name}...")
        img = Image.open(path).convert("RGB")
        # rembg expects PIL image, returns PIL with alpha
        out = remove(img)
        out.save(clean)
        print(f"  Saved {clean}")
    else:
        print(f"  [cached] {clean}")
    clean_paths[name] = clean

# ----------------------------------------------------------------------------
# Step 5: Mesh generation
# ----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Step 5: TripoSR mesh generation")
print("=" * 60)
print("  Loading TripoSR model (downloads ~500MB on first run)...")

from tsr.system import TSR
from tsr.utils import remove_background, resize_foreground, to_rgb

model = TSR.from_pretrained(
    "stabilityai/TripoSR",
    config_name="config.yaml",
    weight_name="model.ckpt",
)
model.renderer.set_chunk_size(8192)
model.to(device)

for name, clean_path in clean_paths.items():
    out_mesh = OUT_DIR / f"ts9_{name}_mesh.glb"
    if out_mesh.exists():
        print(f"  [cached] {out_mesh} — delete to regenerate")
        continue

    print(f"\n  Generating mesh from {name} view...")
    print(f"  (this takes ~30s on GPU, ~10-20 min on CPU)")

    image = Image.open(clean_path).convert("RGB")
    # TripoSR preprocessing
    image = remove_background(image)
    image = resize_foreground(image, 0.85)
    image = to_rgb(image)

    with torch.no_grad():
        scene_codes = model([image], device=device)
        meshes = model.extract_mesh(scene_codes)

    # Save (take first mesh)
    mesh = meshes[0] if isinstance(meshes, list) else meshes
    mesh.export(str(out_mesh))
    print(f"  ✓ Saved {out_mesh}")

# ----------------------------------------------------------------------------
# Done
# ----------------------------------------------------------------------------
print("\n" + "=" * 60)
print("Done!")
print("=" * 60)
print(f"\nMeshes in {OUT_DIR}/")
print("  - ts9_side_mesh.glb  (from side photo)")
print("  - ts9_top_mesh.glb   (from top photo)")
print("\nView them with:")
print("  - Blender (free, blender.org)")
print("  - Windows 3D Viewer (built-in)")
print("  - https://gltf-viewer.donmccurdy.com (drag & drop)")
print("\n⚠ These are REFERENCE ONLY. They hallucinate unseen sides.")
print("  The parametric model (specs/ts9.json) is the source of truth.")
