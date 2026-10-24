# Dunlop Cry Baby GCB95 (Original / Standard Wah) — measurements

Slug: `dunlop-crybaby-gcb95`. Exact model: GCB95 standard wah (red Fasel
inductor, die-cast shell, side jacks + side DC jack). Not CBJ95 Junior,
GCB95F Classic, or any signature variant: every reference below is the
plain black GCB95 with the `cry baby` toe badge and ribbed rubber treadle pad.

Orientation used everywhere below (spec-schema): toe (front, badge and toe
switch) = `+z`, heel (back, hinge end) = `-z`, left in top view
(AMPLIFIER/output side) = `-x`, right in top view (INSTRUMENT/input side)
= `+x`, `y` up from the base bottom (rubber feet excluded, as on the other
heroes).

## References (guide Step 1)

Fetched with `scripts/fetch_views.py --backend manual` from manufacturer /
retailer image URLs; each `.jpg` has a matching `.META.txt`.

| View | File (1280px unless noted) | Source |
|---|---|---|
| Top-down | `references/dunlop-crybaby-gcb95_top.jpg` | Dunlop (jimdunlop.com) product image `11095000001.TOPP` |
| Left side (AMPLIFIER) | `references/dunlop-crybaby-gcb95_left.jpg` | Dunlop product image `11095000001.LEFT` |
| Right side (INSTRUMENT + DC) | `references/dunlop-crybaby-gcb95_right.jpg` | Dunlop product image `11095000001.RGHT` |
| Toe / front | `references/dunlop-crybaby-gcb95_main34.jpg` | Dunlop product image `11095000001.MAIN` (straight toe view, not a 3/4 despite the file name) |
| Heel / back | `references/dunlop-crybaby-gcb95_back.jpg` | Dunlop product image `11095000001.BACK` (straight heel view) |
| Bottom | `references/dunlop-crybaby-gcb95_bottom.jpg` | Dunlop product image `11095000001.BOTT` |
| 3/4 beauty (INSTRUMENT side) | `references/dunlop-crybaby-gcb95_beauty34.jpg` (1500px) | Sweetwater product main image (media.sweetwater.com) |
| Toe detail (duplicate angle) | `references/dunlop-crybaby-gcb95_detail34.jpg` (750px) | Sweetwater closeup `750-Crybaby_detail4.jpg`; same toe view as Dunlop MAIN, used only to confirm the toe switch and bumpers |

Four-plus distinct views of the exact pedal: satisfied (top, both sides,
toe/front, heel/back, bottom, and a 3/4). The pedal in all Dunlop views is
photographed at rest with the toe raised (heel end of the treadle down);
that rest pose is what the profiles below trace.

## Published dimensions (anchor)

- Retailer/manufacturer listings agree on the footprint: 10 x 4 in.
  Thomann lists the GCB95 as (W x D x H) 102 x 254 x 64 mm, American
  Musical / Dunlop listings as 10" x 4" x 2-1/2", weight 3.7 lb (1.68 kg).
- Converted: W = 102/25.4 = **4.02 in**, D = 254/25.4 = **10.00 in**,
  published H = 64/25.4 = **2.52 in**.
- The published 2.52 in height does **not** match the toe-raised rest
  silhouette in the side photos (see calibration): it is the nominal
  treadle-level height, close to the treadle-top height over the heel/pivot
  (measured 2.50-2.56 in). Following the EHX big-box precedent in this repo
  (published overall height includes parts at an extreme, bare/rest height
  resolved from the side photos), `specs/dunlop-crybaby-gcb95.json` keeps
  the published W x D and sets `dims.h` to the measured rest height of the
  bare shell+treadle at the toe, **3.00 in**, with the discrepancy recorded
  in `dims.source`. The rubber pad adds ~0.11 in on top of that (3.11 in
  overall at the toe); the rubber feet add ~0.33 in below the base plate
  and are not modelled (as on the other heroes).

## Side-profile calibration (left + right, 1280x1280)

- Depth in frame: heel outer x ~122 px to toe outer x ~1168 px (left),
  122 to 1165 px (right) for 10.00 in -> **104.5 px/in** (104.6 left,
  104.4 right). Vertical scale assumed equal (studio product shots).
- `y = 0` at the bottom of the base plate, y_px ~768 (left). The rubber
  feet extend to y_px ~802, i.e. ~0.33 in below the plate: excluded.
- Toe is at image-right in `left.jpg` (AMPLIFIER side, heel/pivot at
  image-left) and at image-left in `right.jpg` (pivot pin at image-right);
  the two sides were mirrored into one z frame before averaging.
- Perspective caveat: these are studio shots, not orthographic renders.
  Landmarks near the frame centre are trusted to ~±0.05 in; end faces
  (foreshortened, rounded) to ~±0.10 in. Single-view values are flagged
  provisional in the table below.

### Base shell profile (spec `enclosure.points`, back -z to front +z)

Top edge of the black base casting, averaged over both sides:

| z (in) | y (in) | Landmark |
|---|---|---|
| -5.00 | 1.02 | heel top corner (both sides) |
| -3.00 | 1.20 | heel-mid wall top |
| 0.00 | 1.42 | wall top under the jack line |
| +3.00 | 1.70 | toe-mid wall top |
| +5.00 | 1.92 | toe top corner (corroborated by the toe view: base wall ~1.86 in at the badge face) |

So the base is a low wedge, taller at the toe (1.92 in) than at the heel
(1.02 in). ASCII side sketch (heel left, toe right, not to scale):

```
 treadle top  ____/‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾   <- pad on top of this line
             /   treadle casting  \
 base top       _/‾‾‾‾‾‾‾‾‾‾‾‾‾‾   <- gap (toe switch + gear) between
             __/   base casting    \
            |_______________________|  <- base plate (y=0)
 heel -5                         +5 toe
```

### Treadle profile (spec `treadleProfile.points`, [z, y] polygon)

Traced from the same two side views, rest pose (toe raised). The treadle
top rises from heel to toe at ~0.05 in/in; the casting is ~0.65 in thick
at the toe face (front view) and ~1.05 in through the pivot (side views),
with the side skirt's bottom edge rising heel-to-toe underneath it. The
polygon follows that skirt line (a recessed-underside variant was tried
in the first build and read as a thin floating slab in Side view, with
the pivot pin hanging in the gap — the skirt-line profile below is the
correction, checked against both side references):

| Point | z (in) | y (in) | Landmark |
|---|---|---|---|
| heel-top | -4.90 | 2.50 | treadle heel end, top (inset 0.10 from the heel face) |
| toe-top | +4.90 | 3.00 | treadle toe end, top (= `dims.h`) |
| toe-bottom | +4.90 | 2.35 | toe face bottom (0.65 face, front view) |
| underside mid | 0.00 | 1.95 | side skirt bottom edge at mid-depth (both sides) |
| heel-bottom | -4.90 | 1.50 | heel end bottom, just above the base heel (gap closing at the pivot) |

Widths (top view, see below): treadle casting ~3.3 in (spec width 3.30,
a mid-taper compromise — the real casting tapers with the shell).

### Rubber pad profile (spec `padProfile.points`)

The ribbed black rubber pad sits on the treadle top, inset ~0.35 in from
the toe/heel ends in z and ~0.18 in per side in x (width 2.95 in in spec):

| Point | z (in) | y (in) |
|---|---|---|
| heel-top | -4.55 | 2.65 |
| toe-top | +4.55 | 3.11 |
| toe-bottom | +4.55 | 2.98 |
| heel-bottom | -4.55 | 2.52 |

(Top line = treadle top line + ~0.13 in pad thickness.)

### Pivot (hero press axis)

Silver pivot pin visible on both treadle sides: centre at
z ~ **-2.1 in**, y ~ **1.70 in** (left: z -1.99, right: z -2.35 after
mirroring; average -2.17, rounded to -2.1; y from the pin centre against
the base-plate line, +/-0.1 in). The treadle rotates about this
axis; the heel overhang behind the pivot is ~2.9 in. Press travel in the
hero is 0.055 rad toe-down, which drops the toe ~0.39 in, just closing
the toe gap without striking the base.

## Top layout (top view, 1280x1280; image top = toe)

Calibration: pedal x 434-848 px (toe end) for the width, y 111-1168 px
for the 10.00 in depth -> ~104 px/in, consistent with the sides.

| Feature | Position | Notes |
|---|---|---|
| Footprint taper | toe width 3.96 in, heel width 3.18 in | The shell tapers toward the heel. Existing `parts.js` extrusions are constant-width, so the model uses the published max width 4.02 in for the base and mid-taper widths for treadle (3.30) and pad (2.95): a documented compromise, see the parent-builder proposal in the build report. Top/bottom views are where this shows. |
| Treadle frame inset | ~0.20-0.35 in per side | Treadle casting inset from the base edges, more at the heel. |
| Pad inset | ~0.18 in per side from the treadle | Ribbed pad covers most of the treadle top. |
| AMPLIFIER jack | left wall (-x), z +0.55, y 0.85 | 2 views: top (hole at image-left, ~43% from the toe) + left side (hex nut centred at z +0.55). |
| INSTRUMENT jack | right wall (+x), z +0.60, y 0.85 | 2 views: top + right side; z agrees with the left jack within 0.05 in, spec uses +0.58 for both (average). |
| DC 9V power jack | right wall (+x), z +0.22, y 0.85 | Right side + 3/4 only: small black round barrel just heel-ward of the INSTRUMENT jack, same height line. **Provisional (single straight view + 3/4).** `parts.js` has no side power jack (its `powerJack()` is back-wall only), so this is a proposed spec field, rendered by the hero page; see the build report. |
| CE / 9V sticker | right wall, z ~-0.9, y ~0.85 | Small white rectangle heel-ward of the DC jack (right side + 3/4). Page-rendered proposed field, same reason. Provisional size. |
| Pivot pins | both treadle sides, z -2.1, y 1.70 | Both side views; page-rendered with the treadle (they travel with it). |
| Toe switch | x 0, z +3.60, on the base deck | Chrome plunger under the treadle toe (toe views, Dunlop MAIN + Sweetwater detail): washer/nut/plunger stack ~0.32 in tall above the local deck. Modelled with the existing round `footswitch` builder seated on the base profile (deck parts carry no y). |
| Rubber bumpers | two, under the treadle toe, x ~±1.05 | Seen only in the toe views; not modelled (inside the gap, barely visible). Listed for the proposed wah builder. |
| Toe badge | toe face (+z), centred, y ~0.30-1.55 | Black plate with white `cry baby`; plate ~2.55 in wide x ~1.25 in tall (toe view, plate spans ~66% of the ~3.9 in toe face width, height from the toe-view ratio). Page-rendered proposed field (`parts.js` labels have no front-face orientation). |
| Bottom plate | underside | White `cry baby` / `MODEL GCB95` / battery-door print and 4 rubber feet on the bottom view; underside is never visible in the hero's orbit range (maxPolarAngle < floor), so it is inventoried but not modelled. |

Component heights: audio jack hex/washer stack is the shared `jack()`
builder (0.55 in nut, measured-consistent with the side views). No knobs,
no LED, no deck screws on this pedal: the GCB95 has **no indicator LED**
(checked in every view — no lens anywhere on the shell or treadle), so
the spec carries `led: null` and the hero press does not toggle anything.

## Colour and print inventory

Colour samples (median of a lit, non-specular patch, left side view):
base wall `#424247`, treadle side `#3d3c40`, pad top (top view) `#313030`
— all shaded readings of the same black powder-coat / rubber under studio
light. Spec colours are set a step darker so the studio key does not wash
them grey: enclosure and treadle `#26262a` (black powder-coat; first
build used `#1d1d20`, which read as a flat black silhouette in the dark
studio — corrected after the first hero screenshots), pad `#131315`
(rubber).

Print / marking inventory (every word on the pedal):

| Marking | Where | Treatment in the model |
|---|---|---|
| `cry baby` (white, lowercase rounded, long descenders on the `y`s) | black plate on the toe face | Hero-page front label (white on black, rounded/bold) from the proposed `toeBadge` spec field |
| `AMPLIFIER` | embossed vertically (reading toe-to-heel) in the pad's left groove | Pad decal texture (`textures/dunlop-crybaby-gcb95-decal.png`) |
| `INSTRUMENT` | embossed vertically in the pad's right groove | Pad decal texture |
| Ribs | ~24 longitudinal ribs across the pad | Pad decal texture (drawn ribs; the pad mesh itself is smooth) |
| `CE` + polarity marks | white sticker, right wall | Hero-page side label from the proposed `sideSticker` field (simplified `CE 9V` text) |
| `cry baby`, `MODEL GCB95`, battery text, `Dunlop` | bottom plate | Not modelled (underside out of view), inventoried here |
| (none) | no LED lens, no knob print, no top-face logo on the treadle frame | — |

## Provisional / single-view values (flagged per the guide)

- DC jack z (+0.22) and the CE sticker position/size: one straight side
  view plus the 3/4; no top-view confirmation (both are on the wall,
  hidden in the top view by the treadle overhang).
- Treadle underside mid point (z 0, y 1.95): the side skirt's bottom
  edge in both sides; the hollow above it (toe-view gap) is not profiled,
  because the extruded casting must read solid from the side.
- Base toe top corner (1.92 in): both sides agree, corroborated loosely
  by the toe view (~1.86 in); the shell taper means the side-wall top in
  the side photos is the wide toe-side edge, not the centre deck.
- Footprint taper (3.96 toe / 3.18 heel): top view only (it is a plan
  measurement, so one true top view suffices), but not expressible with
  the current constant-width builders.
