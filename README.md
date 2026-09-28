# Pedalboard 3D

A 3D pedalboard visualizer. Import a board from [PedalPlayground](https://pedalplayground.com) and see it in true 3D — rotate, zoom, pan — to catch the practical problems 2D planners hide: a drive pedal too short to stomp behind a tall delay, knob clearance between rows, whether that back row actually needs a riser.

**Live demo:** enable GitHub Pages (Settings → Pages → Deploy from branch → `main`, root) and open the published URL. No build step — `index.html` is the whole app (Three.js via CDN).

## Import format

Paste a JSON array (or `{"pedals": [...]}`) into the import box. Each pedal needs any of `image` / `brand`+`name`, plus `x`/`y` in inches, board-centered (`+y` = back of board, away from the player). Pedals are matched by image filename first, then brand+name (case-insensitive, with a lenient substring fallback). Unrecognized entries are skipped with a console warning.

```json
[
  {"brand": "BOSS", "name": "TU-3 Chromatic Tuner", "x": -9.3, "y": -3.5},
  {"image": "ibanez-ts9.png", "x": -5.9, "y": -3.5}
]
```

Click a pedal for its dimensions and height provenance. **Player view** puts the camera at standing eye height for the stomp test; **Top-down** gives the 2D comparison.

## Data

- **Pedal catalog & images** (`W × D` footprints, top-down PNGs): fetched live from the open-source [PedalPlayground repo](https://github.com/PedalPlayground/pedalplayground) (`pedals.json`, `public/images/pedals/`), with a small bundled fallback if the fetch fails. Note their `Height` field is the top-down *depth* — vertical height exists nowhere in their data.
- **Vertical heights** (`data/heights.json`, 8,550 pedals): built for this project because no such dataset existed. See [METHOD.md](METHOD.md) for the full method. Confidence scheme:
  - `high` (175) — hand-verified published spec (manufacturer manual, Sweetwater Tech Specs, etc.). Usually the **overall** height *including* knobs/footswitch.
  - `medium` (6,060) — footprint matched to a verified enclosure datasheet (Hammond 1590A/B/BB, 125B, Boss compact, …). **Bare-enclosure** height — knobs and footswitch excluded, so true max height is ~0.2–0.4″ higher.
  - `low` (2,315) — no clean match; `height_in` is `null`. Never guessed — the visualizer shows an honest 2.0″ default labeled *unknown*.
- **Board geometry**: Pedaltrain Classic 2, 24″ × 12.5″, rendered with its real front-to-back incline. Back rail 3.5″ is the published spec (Sweetwater Tech Specs, MPN PT-CL2-F); front rail 1.75″ is estimated from product side-profile photography (≈ 8° incline). See the `BOARD` comment in `index.html`.

## Regenerating the height database

```bash
# 1. drop pedals.json from PedalPlayground next to the scripts:
#    https://raw.githubusercontent.com/PedalPlayground/pedalplayground/master/public/data/pedals.json
python3 build_db.py        # enclosure inference -> heights_base.json
python3 merge_verified.py  # merge verified_*.json hand specs -> data/heights.json
```

To correct one pedal, edit its entry in `data/heights.json` directly, set `confidence` to `high`, and record the spec URL plus what it includes in `source`. To add an enclosure, append a row to `ENCLOSURES` in `build_db.py` with a verifiable source URL. Never fill a `null` by guessing.

## Roadmap

- More boards (Nano+, Metro 16, Classic 1 — needs verified rail heights) + board picker
- Knob/footswitch geometry instead of plain boxes (taller max-height rendering for `medium` entries)
- Pedal-to-pedal collision / knob-clearance warnings on import
- Cable + jack clearance visualization
- "Stompability" score per pedal from player view
- Save/share board links
