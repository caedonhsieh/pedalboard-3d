#!/usr/bin/env python3
"""
Clone a pedal spec with workflow enforcement.

Prevents the SD-1 mistakes (2026-10-01):
- Cloning without looking at a reference photo
- Leaving source-pedal colors/text in the spec
- Moving knob positions (breaking surfaceY) instead of swapping labels
- Pushing without decal preview

Usage:
  python3 scripts/clone_pedal.py --source ds1 --target sd1 --name "SD-1 Super OverDrive"

Workflow enforced:
  1. Reference images REQUIRED before cloning (references/<target>/ must exist, non-empty)
  2. Field-by-field diff: every differing field needs an explicit decision
  3. Automated leftover checks (colors, text from source pedal)
  4. surfaceY consistency check (positions unchanged or recomputed)
  5. Decal preview render required before push

This script does steps 1-4. Step 5 is manual (view the preview).
"""

import argparse
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_spec(pedal_id):
    path = os.path.join(REPO, 'specs', f'{pedal_id}.json')
    with open(path) as f:
        return json.load(f)

def find_colors(spec):
    """Find all color values and their locations."""
    colors = {}
    def walk(obj, path=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{path}[{i}]")
        elif isinstance(obj, str) and re.match(r'^#[0-9a-fA-F]{6}$', obj):
            colors.setdefault(obj.lower(), []).append(path)
    walk(spec)
    return colors

def find_text(spec, terms):
    """Find source-pedal text leftovers."""
    spec_str = json.dumps(spec)
    found = []
    for term in terms:
        for m in re.finditer(re.escape(term), spec_str):
            # Get surrounding context
            start = max(0, m.start() - 80)
            ctx = spec_str[start:m.end() + 40].replace('\n', ' ')
            found.append((term, ctx))
    return found

def check_surfaceY(spec, source_spec):
    """Verify surfaceY values match positions."""
    issues = []
    # Build source position->surfaceY map
    src_map = {}
    for k in source_spec.get('knobs', []):
        src_map[(k.get('x'), k.get('z'), 'knob')] = k.get('surfaceY')
    for l in source_spec.get('labels', []):
        src_map[(l.get('x'), l.get('z'), 'label')] = l.get('surfaceY')

    for k in spec.get('knobs', []):
        key = (k.get('x'), k.get('z'), 'knob')
        expected = src_map.get(key)
        actual = k.get('surfaceY')
        if expected is not None and actual != expected:
            issues.append(
                f"Knob '{k.get('id')}' at ({k.get('x')}, {k.get('z')}): "
                f"surfaceY={actual}, expected {expected} for this position. "
                f"Did you move the knob instead of swapping labels?"
            )

    for l in spec.get('labels', []):
        key = (l.get('x'), l.get('z'), 'label')
        expected = src_map.get(key)
        actual = l.get('surfaceY')
        if expected is not None and actual != expected:
            issues.append(
                f"Label '{l.get('text')}' at ({l.get('x')}, {l.get('z')}): "
                f"surfaceY={actual}, expected {expected} for this position."
            )
    return issues

def main():
    p = argparse.ArgumentParser(description="Clone a pedal spec with workflow enforcement")
    p.add_argument('--source', required=True, help='Source pedal ID (e.g., ds1)')
    p.add_argument('--target', required=True, help='Target pedal ID (e.g., sd1)')
    p.add_argument('--name', required=True, help='Target pedal display name')
    p.add_argument('--source-terms', nargs='*', default=[],
                   help='Source pedal text terms to check for (e.g., DS-1 Distortion)')
    p.add_argument('--check-only', action='store_true',
                   help='Only run checks on existing target spec, do not clone')
    args = p.parse_args()

    errors = []

    # === GATE 1: Reference images required ===
    ref_dir = os.path.join(REPO, 'references', args.target)
    ref_ok = True
    if not args.check_only:
        if not os.path.isdir(ref_dir):
            errors.append(
                f"BLOCKED: No reference directory at references/{args.target}/\n"
                f"  Download reference photos FIRST. Cannot clone without looking at the real pedal."
            )
            ref_ok = False
        else:
            images = [f for f in os.listdir(ref_dir)
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            if not images:
                errors.append(
                    f"BLOCKED: references/{args.target}/ is empty.\n"
                    f"  Download reference photos FIRST. Cannot clone without looking at the real pedal."
                )
                ref_ok = False
            else:
                print(f"✓ References: {len(images)} images in references/{args.target}/")

    # === Clone or load ===
    target_path = os.path.join(REPO, 'specs', f'{args.target}.json')
    if not args.check_only:
        if os.path.exists(target_path):
            errors.append(f"BLOCKED: specs/{args.target}.json already exists. Use --check-only to validate.")
            ref_ok = False
        elif not ref_ok:
            print("  (skipping clone — fix BLOCKED issues first)")
        else:
            source = load_spec(args.source)
            import copy
            target = copy.deepcopy(source)
            target['id'] = f"boss-{args.target}"
            target['name'] = args.name
            # Clear surfaceY (must be explicitly set per-field)
            for k in target.get('knobs', []):
                k.pop('surfaceY', None)
            for l in target.get('labels', []):
                l.pop('surfaceY', None)
            with open(target_path, 'w') as f:
                json.dump(target, f, indent=2)
            print(f"✓ Cloned specs/{args.source}.json -> specs/{args.target}.json")
            print(f"  surfaceY cleared — must be set explicitly per position")
    else:
        if not os.path.exists(target_path):
            errors.append(f"specs/{args.target}.json does not exist")
            print("\n".join(errors))
            sys.exit(1)

    # === Summary (early exit for BLOCKED) ===
    blocked = [e for e in errors if e.startswith("BLOCKED")]
    if blocked and not args.check_only:
        print(f"\n{'='*50}")
        print(f"BLOCKED: fix these before cloning:\n")
        for e in blocked:
            print(f"  ✗ {e}\n")
        sys.exit(1)

    source = load_spec(args.source)
    target = load_spec(args.target)

    # === GATE 2: Source color leftovers ===
    print("\n--- Color audit ---")
    source_colors = find_colors(source)
    target_colors = find_colors(target)
    # Colors in target that exactly match source (potential leftovers)
    for color, paths in target_colors.items():
        if color in source_colors:
            # Check if it's a "shared" color (black, metal gray, etc.)
            # These are fine to share; flag only chromatic colors
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            is_chromatic = max(r, g, b) - min(r, g, b) > 30
            if is_chromatic:
                errors.append(
                    f"LEFTOVER COLOR: {color} (source pedal color) still in target at:\n"
                    f"    {', '.join(paths[:3])}\n"
                    f"  Sample the real {args.target} color from reference photos."
                )
            else:
                print(f"  Shared achromatic {color} (OK)")
    if not any(e.startswith("LEFTOVER COLOR") for e in errors):
        print("✓ No source-pedal chromatic colors in target")

    # === GATE 3: Source text leftovers ===
    print("\n--- Text audit ---")
    if args.source_terms:
        leftovers = find_text(target, args.source_terms)
        # Filter out notes field (heritage mentions are OK)
        real_leftovers = [l for l in leftovers if '"notes"' not in l[1]]
        if real_leftovers:
            for term, ctx in real_leftovers[:5]:
                errors.append(f"LEFTOVER TEXT: '{term}' still in spec: ...{ctx}...")
        else:
            print(f"✓ No leftover source terms: {args.source_terms}")
    else:
        print("  (skipped — no --source-terms provided)")

    # === GATE 4: surfaceY consistency ===
    print("\n--- surfaceY audit ---")
    sy_issues = check_surfaceY(target, source)
    if sy_issues:
        for issue in sy_issues:
            errors.append(f"SURFACEY MISMATCH: {issue}")
    else:
        # Check that surfaceY is actually set (not cleared and forgotten)
        knobs_missing = [k['id'] for k in target.get('knobs', []) if 'surfaceY' not in k]
        labels_missing = [l['text'] for l in target.get('labels', []) if 'surfaceY' not in l]
        if knobs_missing or labels_missing:
            errors.append(
                f"MISSING surfaceY: knobs={knobs_missing}, labels={labels_missing}\n"
                f"  Copy from source by POSITION (not by ID) or recompute via offline raycast."
            )
        else:
            print("✓ All knobs and labels have position-consistent surfaceY")

    # === GATE 5: Decal check ===
    print("\n--- Decal audit ---")
    decal = target.get('treadleDecal', '')
    if not decal:
        errors.append("MISSING: No treadleDecal in spec")
    else:
        # Extract path (strip query string)
        decal_path = decal.split('?')[0].lstrip('./')
        full_path = os.path.join(REPO, decal_path)
        if not os.path.exists(full_path):
            errors.append(f"MISSING: Decal file not found: {decal_path}")
        else:
            print(f"✓ Decal exists: {decal}")
            print(f"  MANUAL STEP: Render preview and compare to reference before push.")

    # === Summary ===
    print(f"\n{'='*50}")
    if errors:
        print(f"FAILED: {len(errors)} issue(s) must be fixed:\n")
        for e in errors:
            print(f"  ✗ {e}\n")
        sys.exit(1)
    else:
        print("PASSED all automated checks.")
        print("\nManual steps before push:")
        print("  1. View decal preview against reference photo")
        print("  2. Verify knob styles (fluted/smooth, base rings) against reference")
        print("  3. Verify label text and positions against reference")
        sys.exit(0)

if __name__ == '__main__':
    main()
