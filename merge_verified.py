#!/usr/bin/env python3
"""Merge hand-verified high-confidence entries into heights.json.
Resolves batch keys against pedals.json; reports unresolved/ambiguous keys.
Manual overrides for flagged entries live in OVERRIDES (key -> action).
"""
import json, re, unicodedata, os

BASE = os.path.dirname(os.path.abspath(__file__)) + '/'
pedals = json.load(open(BASE + 'pedals.json'))
exact_keys = {f"{p['Brand']} | {p['Name']}": (p['Width'], p['Height']) for p in pedals}

def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]', '', s.lower())

norm_index = {}
for k in exact_keys:
    norm_index.setdefault(norm(k), []).append(k)

def resolve(key):
    if key in exact_keys:
        return ('exact', key)
    cands = norm_index.get(norm(key), [])
    if len(cands) == 1:
        return ('fuzzy', cands[0])
    return ('unresolved', cands)

# key -> 'drop' (keep base inference) ; checked manually
OVERRIDES = {
    'MXR | Analog Chorus': 'drop',  # worker flagged 2.5" as possibly package dims
}

batches = ['verified_tc_ibanez.json', 'verified_strymon_jhs_walrus.json',
           'verified_boss_dunlop.json', 'verified_boutique.json',
           'verified_mxr_ehx.json']

base = json.load(open(BASE + 'heights_base.json'))
high = {}
unresolved, ambiguous, dropped = [], [], []
for b in batches:
    data = json.load(open(BASE + b))
    for v in data['verified']:
        key = v.get('key') or f"{v['brand']} | {v['name']}"
        note = v.get('note') or v.get('notes') or ''
        status, target = resolve(key)
        fp = exact_keys.get(target, ('?', '?')) if status != 'unresolved' else ('?', '?')
        if key in OVERRIDES and OVERRIDES[key] == 'drop':
            dropped.append((key, target, fp))
            continue
        if status == 'unresolved':
            unresolved.append((b, key, target))
            continue
        if status == 'fuzzy':
            ambiguous.append((b, key, target, fp))
        h = round(float(v['height_in']), 2)
        prov = v.get('source') or v.get('note') or 'source not recorded'
        src = f"hand-verified spec: {prov}"
        if note and note != prov:
            src += f" [{note}]"
        high[target] = {'key': target, 'height_in': h, 'source': src,
                        'note': note, 'fp': fp, 'via': status}

print(f'== resolved high entries: {len(high)}')
print(f'== dropped by override: {len(dropped)}')
for k, t, fp in dropped:
    print('  DROP', k, '->', t, fp)
print(f'== UNRESOLVED ({len(unresolved)}):')
for b, k, c in unresolved:
    print('  ', b, '|', k, '| candidates:', c[:6])
print(f'== FUZZY-RESOLVED ({len(ambiguous)}), review:')
for b, k, t, fp in ambiguous:
    print('  ', b, '|', k, '->', t, fp)

json.dump(high, open(BASE + 'high_staging.json', 'w'), indent=1)
print('staged', len(high), '-> high_staging.json')
