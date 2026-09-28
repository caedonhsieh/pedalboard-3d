#!/usr/bin/env python3
"""Build base heights DB via enclosure inference (confidence=medium), null otherwise (low).
Output: heights_base.json with schema {key: {height_in, enclosure, source, confidence}}.
High-confidence entries from hand verification are merged in a later step.
"""
import json, collections, os

_HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(_HERE, 'pedals.json')
OUT = os.path.join(_HERE, 'heights_base.json')

# (name, footprint W in, footprint D in, height Z in, spec provenance)
# Footprints are the bare enclosure; pedals.json includes jacks/protrusions,
# so matching allows tolerance below.
ENCLOSURES = [
    ('hammond_1590A', 1.54, 3.66, 1.22,
     'Hammond 1590 series datasheet: 93x39x31mm, via Mouser'),
    ('hammond_1590B', 2.38, 4.41, 1.22,
     'Hammond 1590B spec: 112.4x60.5x31mm, via Farnell'),
    ('hammond_125B', 2.60, 4.78, 1.55,
     '125B/1590N1 Hammond standard: 121-122 x 66 x 39-39.5mm, via lovemyswitches.com / chinadaier.com'),
    ('hammond_1590BB', 3.70, 4.69, 1.34,
     '1590BB: 120x94.5x34mm, via chinadaier.com enclosure listing'),
    ('hammond_1590G', 1.97, 3.94, 1.02,
     '1590G: 100x50x26mm, via chinadaier.com enclosure listing'),
    ('boss_compact', 2.87, 5.08, 2.32,
     'Boss compact series spec: 73x129x59mm, Boss/Roland product manuals'),
    ('mxr_standard', 2.25, 4.25, 1.25,
     'Sweetwater Tech Specs, MXR M101 Phase 90: 2.25x4.25x1.25 in'),
    ('ehx_nano', 2.75, 4.50, 2.10,
     'EHX official spec (Nano Big Muff): 70x115x54mm'),
    ('mooer_micro', 1.65, 3.68, 2.05,
     'Mooer official micro-series spec: 93.5x42x52mm'),
    ('dunlop_crybaby', 4.00, 10.00, 2.50,
     'Dunlop official spec GCB95: 10x4x2.5 in'),
    ('strymon_small', 4.00, 4.50, 1.75,
     'Strymon blueSky user manual: 4.5 deep x 4 wide x 1.75 tall'),
    ('strymon_large', 6.75, 5.00, 1.87,
     'Strymon BigSky user manual: 5 deep x 6.75 wide x 1.87 tall'),
    ('tc_standard', 2.83, 4.80, 1.97,
     'TC Electronic official spec (Hall of Fame 2): 72x122x50mm, via Thomann'),
]

BRAND_PRIORITY = {
    'BOSS': ['boss_compact'],
    'MXR': ['mxr_standard'],
    'Electro-Harmonix': ['ehx_nano'],
    'Dunlop': ['dunlop_crybaby'],
    'Strymon': ['strymon_small', 'strymon_large'],
    'TC Electronic': ['tc_standard'],
    'Mooer': ['mooer_micro'],
    'Mosky': ['mooer_micro'],
    # Known 125B die-cast shops: their ~2.6x4.7 footprints are 125B (1.54"),
    # not the taller EHX nano (2.10") the generic matcher would prefer.
    'JHS': ['hammond_125B'],
    'Walrus Audio': ['hammond_125B'],
    'EarthQuaker': ['hammond_125B'],
    'Keeley': ['hammond_125B'],
    'Wampler': ['hammond_125B'],
    'Catalinbread': ['hammond_125B'],
    'OBNE': ['hammond_125B'],
}

TOL_W, TOL_D = 0.30, 0.45  # inches; allows for jacks/protrusions in pedals.json
# Wider tolerance for brand-priority form factors: pedals.json footprints include
# jacks/protrusions, so e.g. an MXR box records as 2.67x4.5 vs the bare 2.25x4.25.
TOL_W_PRIO, TOL_D_PRIO = 0.75, 0.90


def score(w, d, ew, ed, tw, td):
    if abs(w - ew) > tw or abs(d - ed) > td:
        return None
    return ((w - ew) / ew) ** 2 + ((d - ed) / ed) ** 2


def main():
    data = json.load(open(SRC))
    out, stats, dupes = {}, collections.Counter(), 0
    for p in data:
        key = f"{p['Brand']} | {p['Name']}"
        if key in out:
            dupes += 1
            continue
        w, d = p.get('Width'), p.get('Height')
        matched = None
        if isinstance(w, (int, float)) and isinstance(d, (int, float)):
            prio = BRAND_PRIORITY.get(p['Brand'], [])
            prio_encs = [e for e in ENCLOSURES if e[0] in prio]
            best = None
            for name, ew, ed, h, spec in prio_encs:
                s = score(w, d, ew, ed, TOL_W_PRIO, TOL_D_PRIO)
                if s is None:
                    continue
                if best is None or s < best[0]:
                    best = (s, name, ew, ed, h, spec)
            if best:
                matched = best
            elif prio:
                # Brand has known form factors but this pedal doesn't fit them
                # (BOSS 500-series, Dunlop Fuzz Face, EHX POG2, TC minis...):
                # don't generic-guess, leave for hand verification.
                matched = None
            else:
                best = None
                for name, ew, ed, h, spec in ENCLOSURES:
                    # Try both orientations: some pedals mount an enclosure
                    # sideways (e.g. wide 1590BB builds). Height is unaffected.
                    s1 = score(w, d, ew, ed, TOL_W, TOL_D)
                    s2 = score(w, d, ed, ew, TOL_W, TOL_D)
                    s = None if (s1 is None and s2 is None) else min(
                        x for x in (s1, s2) if x is not None)
                    if s is None:
                        continue
                    if best is None or s < best[0]:
                        best = (s, name, ew, ed, h, spec)
                matched = best
        if matched:
            _, name, ew, ed, h, spec = matched
            out[key] = {
                'height_in': round(h, 2),
                'enclosure': name,
                'source': (f'enclosure inference: pedalplayground footprint {w}x{d} in '
                           f'~ {name} ({ew}x{ed} in); height {h:.2f} in from {spec}'),
                'confidence': 'medium',
            }
            stats['medium'] += 1
        else:
            out[key] = {
                'height_in': None,
                'enclosure': None,
                'source': f'no enclosure match for pedalplayground footprint {w}x{d} in',
                'confidence': 'low',
            }
            stats['low'] += 1
    json.dump(out, open(OUT, 'w'), indent=1)
    print('unique keys:', len(out), '| dupes skipped:', dupes)
    print('confidence:', dict(stats))
    enc = collections.Counter(v['enclosure'] for v in out.values() if v['enclosure'])
    print('top enclosures:')
    for k, n in enc.most_common(15):
        print(f'  {k}: {n}')


main()
