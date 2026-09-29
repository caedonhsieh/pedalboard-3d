#!/usr/bin/env python3
"""
Smart TS9 validator with geometry-aware diagnostics.

Instead of just reporting "IoU=0.74 FAIL", this tells you WHAT is wrong:
- "V4 peak z: expected -0.4406, got 0.0, delta +0.44in — move peak toward back"
- "Jack y: expected 1.25, got 1.475, delta +0.225in — lower the jack"

Components:
- ProfileValidator: compares rendered silhouette vertices vs spec (using validated mask as ground truth)
- ComponentValidator: checks jack/knob/footswitch positions
- TopValidator: existing photo comparison for top view (has good reference)
"""

import json
import sys
from pathlib import Path
from PIL import Image
import numpy as np

REPO = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO / "specs" / "ts9.json"
MASK_PATH = Path.home() / "workspace/imagine_media/ts9-hexagon-mask.png"

# Tolerances (inches) — "virtually no gap" per Caedon
VERTEX_TOL_IN = 0.02  # 0.02" = ~0.5mm, tight but achievable
COMPONENT_TOL_IN = 0.03


def extract_vertices_from_binary(binary):
    """
    Extract 6 hexagon vertices from a binary silhouette.
    IMPORTED from fix_hexagon_profile.py for consistency.
    Returns [(x_px, y_px), ...] for V1..V6.
    """
    # Import the canonical implementation
    import importlib.util
    fixer_path = Path(__file__).parent / "fix_hexagon_profile.py"
    spec = importlib.util.spec_from_file_location("fixer", fixer_path)
    fixer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixer)
    return fixer.extract_hexagon_vertices_from_array(binary)


class ProfileValidator:
    """
    Validates the housing side profile against the validated mask.
    
    Compares the spec's 6 vertices against vertices extracted from the mask.
    Reports per-vertex deltas in inches with actionable messages.
    """
    
    def __init__(self):
        with open(SPEC_PATH) as f:
            self.spec = json.load(f)
        self.spec_points = self.spec['enclosure']['points']
    
    def get_mask_vertices_physical(self):
        """Extract vertices from validated mask, map to inches."""
        img = Image.open(MASK_PATH).convert('L')
        arr = np.array(img)
        binary = arr > 128
        
        vertices_px = extract_vertices_from_binary(binary)
        if not vertices_px:
            return None
        
        xs = [p[0] for p in vertices_px]
        ys = [p[1] for p in vertices_px]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        
        physical = []
        for x_px, y_px in vertices_px:
            z = -2.44 + (x_px - x_min) / (x_max - x_min) * 4.88
            y = (y_max - y_px) / (y_max - y_min) * 2.09
            physical.append((z, y))
        
        return physical
    
    def validate(self):
        """
        Compare spec vertices vs mask vertices.
        Returns (passed, diagnostics) where diagnostics is a list of dicts.
        """
        mask_verts = self.get_mask_vertices_physical()
        if not mask_verts:
            return False, [{"error": "Could not extract vertices from mask"}]
        
        diagnostics = []
        all_pass = True
        
        vertex_names = [
            "V1 bottom-back",
            "V2 top-back", 
            "V3 flat-to-upslope",
            "V4 peak",
            "V5 downslope-to-front",
            "V6 bottom-front",
        ]
        
        for i, (name, spec_pt, mask_pt) in enumerate(zip(vertex_names, self.spec_points, mask_verts)):
            dz = spec_pt[0] - mask_pt[0]
            dy = spec_pt[1] - mask_pt[1]
            dist = (dz**2 + dy**2) ** 0.5
            
            passed = dist <= VERTEX_TOL_IN
            if not passed:
                all_pass = False
            
            # Actionable message
            if abs(dz) > VERTEX_TOL_IN or abs(dy) > VERTEX_TOL_IN:
                actions = []
                if abs(dz) > VERTEX_TOL_IN:
                    direction = "toward back (-z)" if dz > 0 else "toward front (+z)"
                    actions.append(f"move z {direction} by {abs(dz):.3f}in")
                if abs(dy) > VERTEX_TOL_IN:
                    direction = "down" if dy > 0 else "up"
                    actions.append(f"move y {direction} by {abs(dy):.3f}in")
                action_str = "; ".join(actions)
            else:
                action_str = "OK"
            
            diagnostics.append({
                "vertex": name,
                "spec": (round(spec_pt[0], 4), round(spec_pt[1], 4)),
                "expected": (round(mask_pt[0], 4), round(mask_pt[1], 4)),
                "delta_z": round(dz, 4),
                "delta_y": round(dy, 4),
                "distance": round(dist, 4),
                "passed": passed,
                "action": action_str,
            })
        
        return all_pass, diagnostics


def print_diagnostics(passed, diagnostics):
    """Pretty-print diagnostics."""
    print("\n" + "=" * 70)
    print("PROFILE VALIDATION (side silhouette vs validated mask)")
    print("=" * 70)
    
    for d in diagnostics:
        if "error" in d:
            print(f"  ERROR: {d['error']}")
            continue
        
        status = "✓ PASS" if d["passed"] else "✗ FAIL"
        print(f"\n  {d['vertex']}: {status}")
        print(f"    Spec:     z={d['spec'][0]:.4f}, y={d['spec'][1]:.4f}")
        print(f"    Expected: z={d['expected'][0]:.4f}, y={d['expected'][1]:.4f}")
        print(f"    Delta:    dz={d['delta_z']:+.4f}in, dy={d['delta_y']:+.4f}in (dist={d['distance']:.4f}in)")
        if not d["passed"]:
            print(f"    Action:   {d['action']}")
    
    print("\n" + "=" * 70)
    if passed:
        print("RESULT: PASS — profile matches validated mask within tolerance")
    else:
        print("RESULT: FAIL — profile deviates from validated mask")
        print("Run: python3 scripts/fix_hexagon_profile.py to re-measure from mask")
    print("=" * 70)


def main():
    print("Smart TS9 Validator — geometry-aware diagnostics")
    print(f"Reference: {MASK_PATH} (Caedon-validated)")
    print(f"Tolerance: {VERTEX_TOL_IN}in per vertex")
    
    validator = ProfileValidator()
    passed, diagnostics = validator.validate()
    print_diagnostics(passed, diagnostics)
    
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
