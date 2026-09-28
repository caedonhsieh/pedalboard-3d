# Pedal spec schema (`specs/<id>.json`)

A spec is the single source of truth for a hero model. `hero.html` and
`validate.html` both assemble the pedal from the spec via
`assemblePedal()` in `parts.js` — there is no per-pedal modeling code.

## Units and coordinates

- **Inches** everywhere.
- **x**: across the width. Origin at the pedal's center.
- **z**: along the depth. **Back (knob side) = −z, front (switch side) = +z.**
  Origin at the pedal's center, so z ranges −d/2 … +d/2.
- **y**: up from the base. **y = 0 at the bottom of the pedal.**
  Part specs never carry y — every part seats by *sampling the enclosure
  profile at its z* (`surfaceAt()` in parts.js). A profile edit therefore
  reseats knobs / switch / LED automatically, with zero remodel work.

## Fields

| Field | Required | Description |
|---|---|---|
| `id` | yes | Slug, e.g. `ibanez-ts9`. |
| `brand`, `name` | yes | Display names. |
| `dims` | yes | `{w, d, h}` in inches. `h` = max enclosure height (bare enclosure). Add `source` when known. |
| `enclosure` | yes | See below. |
| `knobs` | no | `[{id, style, x, z, rot}]`. `style`: `ts9` \| `mxr`. `rot`: pointer rotation, radians. |
| `led` | no | `{x, z}` or null. |
| `footswitch` | no | `{style, x, z, w?, d?}` or null. `style`: `plate` (TS9 treadle) \| `round` (MXR button). `w`/`d` only for `plate`. |
| `jacks` | no | `[{side: 'left'\|'right', z, y}]`. y is the wall height — jacks don't sit on a deck, so y is explicit here. |
| `powerJack` | no | `{x, y}` on the back wall, or null. |
| `faceImage` | yes | Raw top-face photo URL (ground truth for CHECK B). |
| `decal` | no | Processed top-face texture actually applied to the model. |
| `notes` | no | Free text. **Mark photo-derived / soft values explicitly.** |

### `enclosure`

Box (MXR / EHX / Boss style):

```json
"enclosure": { "type": "box", "preset": "mxr_standard", "color": "#e8621a" }
```

- `preset` pulls w/d/h from `PRESETS` in parts.js (documented provenance there).
  Per-model `dims` always override the preset when measured.
- `edgeRadius` (default 0.06): corner rounding, inches.
- `color`: powder-coat color.

Custom profile (TS9 wedge and friends):

```json
"enclosure": {
  "type": "profile",
  "color": "#7fb75c",
  "points": [[-2.45, 2.09], [-0.99, 2.075], [-0.49, 2.03], [-0.09, 1.93],
             [0.51, 1.75], [1.31, 1.47], [2.45, 1.08]],
  "bevel": 0.07,
  "frontLean": 0.06
}
```

- `points`: `[[z, y], …]` from back (−d/2) to front (+d/2). This is the
  **nominal design intent** — the builder compensates for bevel internally.
- `bevel` (default 0.05): edge softening, inches. Larger values round
  corners more (e.g. the TS9's rounded rear-top corner).
- `frontLean` (default 0): inches the front-top edge leans forward —
  a slightly sloped front face instead of a perfectly vertical one.

## Minimal example — MXR Phase 90 style box

```json
{
  "id": "mxr-phase90",
  "brand": "MXR",
  "name": "Phase 90",
  "dims": { "w": 2.362, "d": 4.370, "h": 1.260, "source": "preset mxr_standard" },
  "enclosure": { "type": "box", "preset": "mxr_standard", "color": "#e8621a" },
  "knobs": [{ "id": "speed", "style": "mxr", "x": 0, "z": -1.0, "rot": 0.0 }],
  "led": { "x": 0.6, "z": -1.6 },
  "footswitch": { "style": "round", "x": 0, "z": 1.2 },
  "jacks": [
    { "side": "right", "z": -0.5, "y": 0.7 },
    { "side": "left", "z": -0.5, "y": 0.7 }
  ],
  "faceImage": "https://…/mxr-phase90.png",
  "notes": "Positions illustrative — measure before shipping."
}
```

A boxy pedal like this needs **no profile work at all**: preset dims, one
knob position, done. That is the whole point — the TS9's custom profile is
the exception, not the rule.
