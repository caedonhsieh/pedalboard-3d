# New pedal guide — building a standalone hero, step by step

The repeatable recipe used for the MXR Phase 90, Boss DS-1, and Ibanez TS9
heroes. Follow it in order; do not skip the gates. Deeper background lives in
[PROCESS.md](../PROCESS.md) (strategy and the validator),
[spec-schema.md](../spec-schema.md) (every spec field), and
[hero-process.md](hero-process.md) (measurement discipline). This guide is the
checklist that ties them together.

**The one-sentence version:** measure a real pedal, write it as data in
`specs/<id>.json`, assemble it with the shared part library (`parts.js`),
prove it with `validate.html`, then make it *feel* real (studio page,
working knobs and footswitch) and keep fixing what a fresh viewer can still
notice until there is nothing left to notice.

**The stop rule (do not soften it):** stop when there are no realistic gaps
left. If you *know* the footswitch, in/out jacks, font, or hardware is wrong,
fix it. If nobody can notice a gap at normal viewing distance, you may stop.

---

## Step 0 — Pick the pedal and set up

1. Pick from `specs/ledger.json` (`status: "planned"`, lowest `priority`
   number first) or add a new entry there.
2. Decide the slug now and never change it: `<brand>-<model>` in lowercase,
   e.g. `mxr-phase90`, `boss-ds1`, `ibanez-ts9`. It names the spec file, the
   page file, and the ledger entry.
3. Serve the repo locally (every later step needs it):

   ```bash
   cd /data/repos/AAI/caedon-pedalboard-3d   # or your clone
   python3 -m http.server 8765
   ```

4. Open the current gold standard once so you know the target:
   `http://localhost:8765/mxr-phase90.html`. A finished hero looks and behaves
   like that page.

## Step 1 — Collect references (no references, no model)

Gather at least four views of the *exact* pedal (not a sibling model):

| View | What you will measure from it |
|---|---|
| Top-down | Knob/LED/label x–z positions, footprint |
| Side (both, if they differ) | Enclosure profile, heights, jack and screw positions |
| Front and back | Footswitch/treadle shape, power jack, thumbscrew |
| 3/4 beauty (1–2) | Colour, print, proportion sanity check |

- First stops: Sweetwater product galleries, the manufacturer's page,
  PedalPlayground (top-down), then used listings for wear angles.
- `python3 scripts/fetch_views.py --pedal <id> --query "<Brand Model>"` can
  pull galleries; see its header for backends.
- Save every image as `references/<id>_<view>.jpg|png` **plus** a matching
  `.META.txt` (source URL, date, dimensions, view description). A reference
  without a META file does not exist.
- If you cannot find four views, stop and say so. Do not proceed on one photo.

## Step 2 — Measure, and write the numbers down

Create `references/<id>_measurements.md` before touching any geometry. Every
number that later enters the spec must have a row here.

1. **Published dims first.** Manufacturer W × D × H (retailers corroborate).
   Convert mm to inches by dividing by 25.4; keep all spec values in inches.
   These anchor the absolute scale.
2. **Calibrate each photo.** px-per-inch from a known length in frame
   (usually the published W or D). Note perspective caveats.
3. **Side profile.** If the enclosure is not a plain box, trace the side
   silhouette into a `[[z, y], …]` point list, back (−z) to front (+z),
   grounded against the published height.
4. **Every component, in two views where possible.** Knobs, LED, footswitch,
   side jacks, power jack, screws, plates: record centre x/z, diameter or
   size, and the source view(s). Single-view positions are provisional —
   flag them in the file.
5. **Colour.** Sample the enclosure colour from a lit, non-specular patch of
   a photo (record the hex and where you sampled it). Do the same for any
   printed ink that matters (logo blue, label black).
6. **Print and fonts.** Note every word on the pedal, its case, weight,
   spacing, and orientation (some labels are vertical). Fonts are matched by
   eye from the reference at the end, but the *text inventory* is made now.

## Step 3 — Choose the enclosure strategy

Exactly one of these, in this order of preference:

1. **Preset box** (most pedals): `PRESETS` in `parts.js` —
   `mxr_standard` 60×111×32 mm, `boss_compact` 73×129×59 mm,
   `ehx_nano` 70×115×54 mm, `ehx_xo` 102×121×57 mm. Per-model `dims` always
   override the preset when measured.
2. **Measured profile** (wedges, treadles, wah shells): `enclosure.type:
   "profile"` with the traced points from Step 2. This is the exception,
   not the rule.
3. **Profile-built family parts** (Boss compact and similar): measured
   `treadleProfile` / `padProfile` / `recessProfile` / `baseProfile`
   extrusions, as in `specs/ds1.json`. Only when the pedal's moving cover
   *is* the product's identity.

Never hand-model geometry per pedal. If a shape cannot be expressed as spec
data plus existing `parts.js` builders, add a *reusable* builder to
`parts.js` (parameterised, with provenance in a comment), never a one-off.

## Step 4 — Write the spec (`specs/<id>.json`)

Full field list: [spec-schema.md](../spec-schema.md). The rules that bite:

- **Coordinates:** inches; x across, origin at centre; **back (knob side) =
  −z, front (switch side) = +z**; y up from the base, and **part specs never
  carry y**. Every deck part seats by sampling the enclosure profile at its
  z (`surfaceAt()` in `parts.js`), so a profile edit reseats everything for
  free. If you are typing a y for a knob/LED/switch, stop — the spec is
  wrong. (Exceptions that do carry explicit y: side `jacks`, `powerJack`,
  `thumbscrew`, and baked `surfaceY` on measured Boss-style specs.)
- **`dims` always carries its `source`** (manufacturer spec, preset name, or
  the measurement file). No source, no ship.
- **Knobs:** `{id, style, x, z, rot}`. Styles in `parts.js`: `mxr`, `ts9`,
  `boss`, `boss-smooth`. Set `tickRing`/`baseRing`/`tickRingScale` only when
  the real pedal has them. `rot` is the pointer angle in the reference photo.
- **Labels:** one entry per printed word from Step 2, with `w`/`h` sized so
  the text cannot clip (set `spaced: false` and widen `w` before shrinking
  the font — clipped first/last letters are the classic failure). Mark any
  label printed on a *moving* part with `"onTreadle": true` (Step 7 needs
  it). Script/brand words get `script: true` or `bold: true` to match the
  reference lettering.
- **Jacks:** one per side with explicit `y` (wall height) and `z`. Left =
  OUTPUT, right = INPUT on almost every pedal — confirm from the print,
  not habit.
- **`faceImage`:** the top-down ground-truth photo URL. **`decal`:** only
  when you apply processed top-face art (Step 6); otherwise `null`.
- **`notes`:** mark every photo-derived or provisional value as such.

## Step 5 — Assemble and look at it

There is no per-pedal modelling code. `assemblePedal(spec)` in `parts.js`
builds the pedal; the page (Step 7) only stages it. To see your spec before
writing the page, open the validator (Step 6), which assembles it too.

Part library you will actually use (`parts.js`):

| Need | Builder |
|---|---|
| Box / profile enclosure | `boxEnclosure`, `profileEnclosure`, `extrudeProfile` |
| Knobs | `knob(style, …)`, `flutedKnobBody`, `tickRing`, `dotRing`, `knobBaseRing` |
| Footswitch | `footswitch({style: 'round' \| 'plate', …})` |
| Name plate | `ibanezPlate` (pattern for printed metal plates) |
| LED / jack / power | `led()`, `jack()`, `powerJack({style})` |
| Text | `textLabel({text, w, h, spaced, script, bold, …})` |
| Finishes | `FIN.*`, `powderCoat(color)`, `hardwareChrome()` |

Material starting points: paint/plastic roughness ~0.4–0.6, metalness 0;
steel/chrome roughness ~0.3, metalness 0.4–1.0 (prefer ~0.45 where the part
must read on a software renderer with no environment map — full metal goes
flat black at grazing angles); rubber ~0.9. Emissive is for the LED only.

## Step 6 — Decals and print art (only when vector labels are not enough)

- Prefer clean vector text (`textLabel`) and canvas-drawn plate art (see
  `ibanezPlate`) over photo pastes. They stay sharp at every angle.
- Full top-face art (MXR style): process the face photo into
  `textures/<id>-decal.png`, set `spec.decal`, and let `applyDecal()` split
  it across deck segments.
- Treadle/pad art (Boss style): `applyTreadleDecal()` for the sloped treadle
  face, `applyPadDecal()` for the rubber pad (its profile is a traced
  outline; the helper spans the upper edge to the farthest-x point). Any new
  decal helper must tag its mesh `userData.kind` and return it, so the page
  can move it with its panel (Step 7).
- Check orientation in Top view: image top = pedal back (−z). A mirrored or
  rotated decal ships mirrored text — look, do not assume.

## Step 7 — Build the hero page (`<brand>-<model>.html`)

Copy `mxr-phase90.html` (the gold standard) and adapt it. The finished page
must have all of this:

1. **Studio:** `studioScene()` on a dark set — key/fill lights, tone mapping,
   soft contact shadow under the base (a radial-gradient plane works where
   shadow maps are weak), fog matched to the background. The pedal must
   never float and never wash out at the hero angle.
2. **Views:** five buttons — 3/4 view, Top, Front, Side, Back — with
   aspect-aware fit distances. On portrait phones the hero must fit the
   pedal's *projected diagonal* (footprint diagonal plus knobs/jacks), and
   `controls.maxDistance` must be at least that fit distance or the orbit
   clamp will silently crop the phone hero.
3. **Orbit clamps:** `minPolarAngle ≈ 0.12`, `maxPolarAngle ≈ 1.62` (never
   under the floor), `minDistance` large enough that zooming in stops
   outside the enclosure, `maxDistance` ≈ 1.5× the hero distance so the
   pedal cannot shrink to a lost stamp.
4. **Interactions (all of them, through the page's own controls):**
   - Drag to orbit, scroll/pinch to zoom.
   - Draggable knobs: raycast the knob anchors; rotate on a horizontal
     *and* vertical drag (`delta = dx − dy` — players try vertical first).
     Clamp rotation to ±2.35 rad.
   - Clickable footswitch: the LED starts in the state the reference photo
     shows (usually ON). Press-and-hold must move the switch, release must
     spring it back, LED toggles on release.
5. **The moving-set rule (the DS-1 lesson):** everything printed on or
   screwed into a moving panel moves with it — panel mesh, pad, decals,
   labels flagged `onTreadle`, and the toe thumbscrew on Boss pedals.
   Rotate the whole set about the *same pivot* the panel geometry uses
   (store each part's base position/rotation, rotate its position about
   that pivot, add the same tilt). Rotating each label in place, or
   forgetting the decals that load asynchronously *after* the set was
   collected, leaves text floating while the panel dips — the exact bug
   this rule exists to prevent.
6. **HUD:** title, one-line hint naming every interaction, spec card, view
   pills. On narrow screens the subtitle must wrap inside the viewport
   (e.g. `max-width: 58vw` under 600 px) and nothing may overlap the pedal.
7. **Errors:** an `onerror`/`unhandledrejection` overlay (see the MXR page)
   instead of a black page. No test hooks (`window.__*`) in the shipped
   file, no external URLs beyond the spec's own `faceImage` reference.

For treadle pedals, sink only the treadle plate on a press — its bezel well
and any enclosure-fixed name plate stay put (TS9 pattern). For round-button
pedals, dip the plunger only (MXR pattern).

## Step 8 — Validate the spec (hard gate)

```
http://localhost:8765/validate.html?spec=specs/<id>.json
```

Three independent checks, fixed canonical cameras (details in
[PROCESS.md](../PROCESS.md)):

- **A — placement:** every part anchor read back from the object graph vs an
  independent interpolation of the spec. **Fails above 2 mm.**
- **B — render vs photo:** top render vs the spec's nominal W×D footprint,
  IoU **≥ 0.90** (explicitly skipped when the spec has no full-top decal).
- **C — profile:** side silhouette vs the spec polyline. **Fails above
  2.5 mm.**

**No model ships without validate.html passing. Not “passing except” —
passing.** When a check fails, first suspect the validator's assumptions,
then the spec, then the builder — in that order — and fix at the root. Never
weaken a threshold to get green.

Also run the pedal both ways in the ledger sense: a profile edit must reseat
parts (Step 4's rule), so re-run A after *any* enclosure change.

## Step 9 — Look at it, from every side, at both sizes

Numbers do not replace looking. With the page open (headless screenshots are
fine; never install a browser, use the one already on the machine):

1. Screenshot the 3/4 hero, Top, Front, Side, Back on desktop (1366×768)
   and the hero + Top on a phone portrait viewport (393×852).
2. For each, ask: could a stranger name this pedal without the page title?
   Is every printed word legible and unclipped? Does every material read as
   its real material (powder coat, chrome, rubber, printed ink) at *this*
   angle — chrome that goes black from the front and text that washes out
   at grazing angles are failures, fixable in the material, not the light.
3. Exercise every interaction and screenshot the held state, not just the
   settled one: knob mid-drag (both drag directions), footswitch held down
   (does the whole panel, print included, travel?), LED off and on, zoom at
   both stops, free orbit to low angles and behind.
4. Compare Top and Side directly against the reference photos from Step 1.
   Proportions, knob layout, and silhouette must agree at normal viewing
   distance — not just under measurement.

## Step 10 — Fresh-eyes critique, and loop

A clean run says the page works, not that it is finished.

1. Hand the page to a fresh reviewer (a subagent or another person) who has
   **not** seen your code or notes. Give them only: the brief (“a standalone
   detailed 3D hero of a real <pedal>; stop when no realistic gap is left”),
   the page URL, and your Step 9 screenshots. Ask for a written critique
   file with a `ready` / `not ready` verdict and, for every shortfall, the
   screenshot, what a player sees, and the change they would make.
2. Work the list top-down. For each item, mark it in the critique file as
   `fixed:` with the screenshot that proves it, or `answered:` with the
   evidence (usually: the measured spec value and the validator result —
   e.g. “enclosure height is the published 53 mm; lowering it would falsify
   the spec”). Do not argue a visible defect away without evidence.
3. Re-screenshot the affected views, re-run Step 8, and send a **new** fresh
   reviewer. Repeat until the verdict is `ready`, or until the only
   remaining items are answered with measurement evidence. Critics
   contradict each other on taste (silver caps vs black knobs happened);
   measurements and the reference photos break ties, in that order.
4. If the same shortfall survives two fix rounds, change technique (rebuild
   the part's geometry or material), do not tune numbers a third time.

## Step 11 — Ship

1. Final gate on the exact bytes you will commit: load the page fresh at
   desktop and phone sizes with nothing injected; zero console errors, zero
   failed requests, screenshots opened and checked once more.
2. Flip the ledger entry in `specs/ledger.json` to `status: "hero"` with a
   notes line recording the validator numbers (A/C in mm, B if applicable).
3. Commit the spec, page, any `parts.js`/texture changes, the measurement
   file, and the ledger together. Message style from this repo's history,
   e.g.:

   ```
   Add <Brand> <Model> standalone hero

   Spec validation: A <x>mm / C <y>mm. Fresh-critic verdict: ready.
   ```

4. Push to `main` **only when the user asks**. Then verify the pushed commit
   is what is served (`git log -1`, pages return HTTP 200).
5. Do not touch `index.html` or the board app in a modeling pass — hero to
   board integration is separate future work (see PROCESS.md).

---

## Failure museum — every one of these shipped once

| Symptom | Root cause | Fix (guide step) |
|---|---|---|
| Text stays floating while the treadle dips | Decals/labels never joined the moving set; decals load after the set was collected | Moving-set rule, rotate about one pivot (7.5) |
| Phone hero crops the pedal | Portrait fit used width, and `maxDistance` clamped the pull-back | Fit the projected diagonal; size the clamp from the fit (7.2–7.3) |
| Pedal turns black on phone | Farther portrait camera inside the scene fog | Push fog out past the farthest camera (7.1) |
| Chrome treadle black from the front | Full-metal material, no environment map on software renderers | Metalness ~0.45, brighter base colour (5) |
| Label loses its first/last letters | Letter-spaced text wider than its plane | `spaced: false`, widen `w` (4) |
| Line strikes through plate wording | Decorative rules drawn at the text's y, text wider than the gap | Shorten rules to flank the measured text width (6) |
| Tick marks read as gear teeth | Wedges too wide and too radial | Wedge ≈ 0.20 of step, ring hugging the skirt (5) |
| Knob only turns sideways | Drag mapped to dx only | `delta = dx − dy` (7.4) |
| LED toggle but no switch travel | Dip fired on release for 150 ms | Sink on pointer-down, spring back + toggle on release (7.4) |
| Print washes out at hero angle | Print layer too metallic/smooth | Matte print material (metalness 0, roughness ~0.6), deeper ink (5–6) |

## Worked examples already in the repo

- **MXR Phase 90** — preset box, one knob, full-top decal. The simplest
  complete pass: `specs/mxr-phase90.json`, `mxr-phase90.html`.
- **Boss DS-1** — measured Boss compact profiles (treadle/pad/recess/base),
  pad decal, `onTreadle` labels. The hard case for moving print:
  `specs/ds1.json`, `boss-ds1.html`, `references/ds1_*`.
- **Ibanez TS9** — custom wedge profile, vector labels, canvas name plate,
  plate-only stomp dip: `specs/ts9.json`, `ibanez-ts9.html`.

When in doubt, diff your work against the closest of these three.
