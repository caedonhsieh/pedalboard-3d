# Hero Pedal Process

How every hand-crafted hero model in this repo gets built. No shortcuts, no guessing.

## 0. Principle

**Stop guessing and measure.** Every geometric value in a hero spec must trace to a
measured source: a manufacturer dimension, a calibrated photo, or a triangulated
landmark. A value with no source is a guess, and guesses don't ship.

## 1. Collect all views

For the target pedal, gather **at minimum**:

| View | Purpose |
|---|---|
| Top-down (orthographic-ish) | Knob/label/jack layout, x/z placement |
| True side profile (left AND right) | Enclosure silhouette, heights, slopes, jack/thumb-screw placement |
| True front and back | Width profile, footswitch plate shape, power jack |
| 3/4 beauty angles (2+) | Cross-check proportions, surface transitions |

**Sweetwater is the first stop** — their product pages carry 6–10 studio views per
pedal (top, sides, back, 3/4s) shot under consistent lighting. Others: manufacturer
product pages, Reverb/Sweetwater used listings (often show wear angles that reveal
edges), retailer catalog shots (PedalPlayground, Thomann, session.de).

**API-driven fetching (preferred):** `scripts/fetch_views.py` pulls multi-view
galleries via product APIs instead of hand-scraping:

| Backend | Views | Auth |
|---|---|---|
| `ebay` | Up to 24/listing; used-gear listings show every angle | `EBAY_CLIENT_ID` + `EBAY_CLIENT_SECRET` env |
| `pedalplayground` | Single top-down, 8000+ pedals | None |
| `manual` | Whatever URLs you hand it | None |

eBay's Browse API is the workhorse: one `--query` returns the top listings, each
with its full photo gallery. One-time setup: create an app at
https://developer.ebay.com/my/keys and export the two keys. (Reverb's API is the
domain-perfect alternative if eBay access ever lapses.)

Save every reference under `references/<pedal>_<view>.jpg|png` with a matching
`<pedal>_<view>.META.txt` recording: source URL, retrieval date, image dimensions,
view description, and any known camera notes. **A reference without a META file
doesn't exist.**

Minimum bar: **4 distinct views** covering top, side, front/back, and one 3/4.
If you can't find 4, the pedal isn't ready to model — say so, don't proceed.

## 2. Research real measurements

Before touching geometry, record the published dimensions:

- Manufacturer spec sheet (W × D × H) — Boss, Ibanez, EHX all publish these.
- Retailer listings corroborate (Sweetwater specs tab, Thomann).
- Convert to inches, store in `specs/<pedal>.json` under `dims` with the source.

Published dims anchor the absolute scale. Everything else is derived relative to them.

## 3. Triangulate: sketch + measurement sheet

Build `references/<pedal>_measurements.md` — the single source of truth for every
number that goes into the model:

1. **Calibrate each photo.** Pick a known physical length visible in the frame
   (usually the published W or D) and compute px-per-unit. Note perspective caveats.
2. **Extract the enclosure profile** from the side view via edge detection or manual
   landmarking. Record the silhouette as a point list in physical units.
3. **Locate every component** (knobs, LED, jacks, screws, plates) in at least two
   views. A component positioned from a single view is provisional — flag it.
4. **Cross-check between views.** The knob x-position from the top view must agree
   with the knob position implied by the 3/4 view. Disagreements get resolved by a
   third view, not by averaging guesses.
5. **Sketch the profile.** A side-view line drawing (even ASCII) of the enclosure
   with labeled dimensions, committed next to the measurements file.

No geometry enters `parts.js` or the spec until its measurement row exists.

## 4. Build

- Implement the enclosure as **measured parametric geometry**, not a primitive with
  tweaked constants. If the side profile is a wedge with a sloped top, build the wedge.
- One reusable enclosure per product family (e.g. all Boss compacts share one
  enclosure builder parameterized by color).
- Components (knobs, footswitch plates, jacks, LEDs, labels) come from `parts.js`
  and are placed from the measurement sheet — never eyeballed in the renderer.

## 5. Validate (per view, independently)

For **each** reference view, render the model from a matched camera and compare:

- Silhouette IoU (rendered mask vs reference mask)
- Symmetric Chamfer distance on extracted contours
- Per-component checks: knob centers within tolerance, label legibility/placement,
  jack/screw positions
- A visual side-by-side, saved under `references/<pedal>_validation/`

A model that passes top view but fails side view **fails**. All views must pass.

## 6. Adversarial mutations

Before calling a model done, mutate it and confirm the validator catches each one:

- Shift a label, scale the enclosure, move a knob, drop the logo, sink a decal,
  perturb a profile point.
- Every mutation must flip its corresponding check from pass to fail.
- A validator that can't catch a deliberate break is decoration.

## 7. Loop until perfect

Fix → re-render → re-measure → re-validate. The loop is automated and doesn't stop
for check-ins. Manual inspection happens **once**, after:

1. Baseline passes on all views,
2. All adversarial mutations are caught,
3. The deployed site serves the exact pushed commit.

## 8. Ship

- Wire the pedal into its page (`<brand>-<model>.html`, generated via
  `scripts/gen_hero_pages.py`).
- Commit, push, and verify GitHub Pages serves the exact commit before asking for
  manual review.

---

*This process exists because the DS-1 shipped from a single top-down photo with a
guessed box enclosure. Never again.*
