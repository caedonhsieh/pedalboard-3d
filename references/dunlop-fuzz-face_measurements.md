# Dunlop Fuzz Face (full-size, red) — measurements

Slug: `dunlop-fuzz-face`. Exact model: Dunlop Fuzz Face Distortion
**JDF2** — the standard full-size red Fuzz Face (germanium PNP,
vintage-spec round sand-cast shell, battery-only). **Not** a Fuzz Face
Mini (FFM1/FFM2/FFM3, ~3.5 in dia with LED + DC jack), not the JHF1
turquoise Hendrix full-size, and not any signature/MXR-housing variant:
every reference below is the plain red JDF2 with the white `FUZZFACE`
smile, black knobs, and black triangular rubber tread. The ledger entry
`dunlop-fuzz-face` ("Round enclosure — custom, not a box") is this pedal.

Orientation used everywhere below (spec-schema): back (knob/jack side)
= `-z`, front (footswitch/tread side) = `+z`, left in top view
(VOLUME/IN side) = `-x`, right in top view (FUZZ/OUT side) = `+x`, `y`
up from the base bottom (rubber feet excluded, as on the other heroes).
Top-view image top = back (`-z`).

## References (guide Step 1)

Fetched with `scripts/fetch_views.py --backend manual` from the Dunlop
(jimdunlop.com) JDF2 gallery (BigCommerce product 660, 1280x1280);
each `.jpg` has a matching `.META.txt`. Dunlop's gallery suffixes do
not match the guide's view names, so the files were renamed to the
true camera after visual check (META `Note:` records the suffix):

| View | File (1280x1280) | Dunlop suffix / image |
|---|---|---|
| Top-down | `references/dunlop-fuzz-face_top.jpg` | `11602052001.MAIN` (660/6598) — true top-down |
| Left side (VOLUME/IN) | `references/dunlop-fuzz-face_side-left.jpg` | `11602052001.LEFT` (660/6599) |
| Right side (FUZZ/OUT) | `references/dunlop-fuzz-face_side-right.jpg` | `11602052001.RGHT` (660/6600) |
| Back (jack wall) | `references/dunlop-fuzz-face_back.jpg` | `11602052001.TOPP` (660/6601) |
| Front (tread) | `references/dunlop-fuzz-face_front.jpg` | `11602052001.BOTT` (660/6602) |
| Bottom plate | `references/dunlop-fuzz-face_bottom.jpg` | `11602052001.BACK` (660/6603) |

Four-plus distinct views of the exact pedal: satisfied (top, both
sides, front, back, bottom — six). The side/front/back shots are
elevations shot slightly above horizontal, so each doubles as the
3/4 beauty check for its side; no separate Sweetwater 3/4 was needed.
All views show the same red JDF2 at rest; knob pointers sit near
12 o'clock in the top view.

## Published dimensions (anchor)

- `data/spec_sheets_staging.json` (verified, secondary, Sweetwater
  JDF2 listing): 7.25 x 7.25 x 3.25 in (184.2 x 184.2 x 82.6 mm),
  `height_includes_knobs: "unknown"`. Its note records the published
  rectangular bounding box as 7.25 in W x 8 in D x 3.25 in H and adopts
  the smaller horizontal dimension (7.25 in) as the round body
  diameter; the 8 in is treated as including jack/footswitch
  protrusion. Corroborated as published bounding box by Music Store
  JD-F2 (8 x 7-1/4 x 3-1/4 in), Equipboard JHF1 (W 7.25 / D 8 /
  H 3.25 in, 2.5 lb — same shell, turquoise), and eBay JDF2 catalog
  (D 8 / H 3.25 in). A vintage-size cross-check: Cornell Fuzz Face
  reissue 7 in (17.8 cm) diameter (Bonhams) — same shell family.
- Conflicts rejected: Amazon/shipping 8 x 7.6 x 3.3 in (box, not
  pedal); Mini listings (3.5 in dia) — wrong product.
- Adopted: **diameter (W = D) 7.25 in**. The top view corroborates a
  circle: red-mask bbox 1031 (x) x 1035 (y) px — equal within 0.4%.
- Published H 3.25 in is **overall**, not bare: the calibrated side
  elevations (below) put the bare dome peak at 2.45 in, with knob and
  footswitch tops at ~2.5–2.8 in and rubber feet (~0.15 in, bottom
  view) below the plate. Following the EHX big-box precedent in this
  repo, `specs/dunlop-fuzz-face.json` keeps the published diameter
  and sets `dims.h` to the measured bare peak, **2.45 in**, with the
  discrepancy recorded in `dims.source`. Do not "correct" 2.45 back
  to 3.25 — 3.25 includes parts the bare enclosure does not have.

## Top layout (top view, 1280x1280; image top = back)

Calibration: red-mask bbox x 125–1155, y 122–1156 (1033 px mean) for
7.25 in -> **142.5 px/in**. Centre (640, 639) px. Pedal coords:
`x = (px - 640)/142.5`, `z = (py - 639)/142.5` (image-down = front
= `+z`). Studio shot, near-orthographic from above; landmarks trusted
to ~±0.05 in. Dark-blob centroids (knobs/pad) and silver-blob
centroids (switch/jacks) were read by mask, then symmetrised where
the pedal is symmetric (differences < 0.05 in).

| Feature | Position (in) | Notes |
|---|---|---|
| Footprint | diameter 7.25 (r 3.625) | Circle; back jack plateau is a shallow stepped sector at the rim, not a diameter change (red top at centre y 122 vs circle y 181 at x ±240 px — the plateau + jack nuts reach the rim). |
| VOLUME knob | x **-1.94**, z **-1.96** | Left black knob (mask centroid -1.91/-1.95, bbox 1.10x1.07 in). 2 views: top centroid + side-left corroboration. |
| FUZZ knob | x **+1.95**, z **-1.97** | Right black knob (centroid +1.96/-1.97, bbox 1.06x1.06 in). Same row as VOLUME. Knob dia **~1.08 in** (mean of both). |
| Knob radius from centre | r 2.76 | `sqrt(1.94^2+1.96^2)`; sets the dome height under the knobs (profile below). |
| Footswitch | x **0.00**, z **+1.38** | Round chrome stomp through the rubber pad (silver centroid (640, 836) px -> 0.00/+1.38). 3 views: top + front + both sides. |
| Rubber tread pad | apex (0, **-0.25**), base corners (±**1.58**, **+3.38**) | Black ribbed triangle/trapezoid: apex y 603 px (z -0.25), base y 1143 px (z +3.54 at the rim centreline; corners inset to ±1.58 at z +3.38 by the circle). Base half-width at y 1100 px is ±1.39 and widening toward the front. Plan (single true top view suffices); thickness from the front/side elevations (~0.12 in over the local deck). |
| IN jack | back wall, x **-0.98**, y **0.65** | Silver nut centroid (504, 125) px -> x -0.96 (symmetrised -0.98). On the back curved wall under the `IN` plateau print. **IN is on the left in top view — the reverse of the modern right-input habit; confirmed by the top print, do not swap.** |
| OUT jack | back wall, x **+0.98**, y **0.65** | Centroid (782, 124) px -> x +0.99 (symmetrised +0.98), under the `OUT` print. |
| LED | **none** | No lens/bezel in any of the six views (checked top, front, back, both sides). Spec carries `led: null`; a footswitch press toggles nothing. The Minis have an LED — another reason they are the wrong reference. |
| Power jack | **none** (battery only) | No DC barrel in any view; Dunlop JDF2 copy: "can only be powered by one 9-volt battery". Spec carries `powerJack: null`. Battery access is the single centre screw on the bottom plate (bottom view). |
| Bottom plate | underside | Silver plate, 3 black rubber feet, centre screw, `Dunlop` / address / `CE` sticker + barcode sticker (bottom view). Underside is never visible in the hero orbit range; inventoried, not modelled. |

Component heights: knob ~0.55 in above the local deck (side
elevations; the library `mxr` Davies body is 0.49–0.55 in tall, so
only its diameter needs scaling, `diaScale` ~1.17 for 1.08 in).
Footswitch stack is the shared round `footswitch` builder (washer +
nut + plunger ~0.33 in above its seat). Audio jack hex/washer stack
is the shared `jack()` builder (0.55 in nut) — on this pedal the
barrels point straight back (`-z`) from the curved back wall, not
out the side walls.

## Round profile (side + front + back elevations)

The shell cannot be traced as a `[[z, y], …]` side profile for
`profileEnclosure` — it is a surface of revolution (plus the back
jack plateau). The reusable shape is a lathe profile
`[[r, y], …]`, r = radius from the centre axis, y up from the base
bottom (silver plate underside, feet excluded):

Calibration (side-left, 1028 px for 7.25 in -> 141.8 px/in; side-right
141.4, front 142.2, back 143.0 — averaged): red-silhouette top over
the base line gives rim (wall top) **~1.20 in** at the circle edge
and dome peak **2.44–2.50 in** at the centre (side-left 2.45,
side-right 2.44, back 2.50; front off-centre 2.27 under the pad
slope). Adopted bare peak **2.45 in** (= `dims.h`). Elevations are
perspective studio shots, not orthographic: centre heights trusted
to ~±0.08 in, rim heights to ~±0.10 in.

| r (in) | y (in) | Landmark |
|---|---|---|
| 0.00 | 2.45 | dome centre (= `dims.h`; under the pad apex region) |
| 1.00 | 2.43 | near-flat crown |
| 1.38 | 2.37 | footswitch radius (deck under the pad/switch) |
| 2.00 | 2.30 | mid-dome |
| 2.76 | 2.02 | knob radius (deck under VOLUME/FUZZ) |
| 3.20 | 1.62 | shoulder |
| 3.50 | 1.30 | shoulder-to-wall blend |
| 3.625 | 1.20 | rim (top of the vertical wall) |
| 3.625 | 0.00 | base (silver bottom plate line) |

ASCII plan (the "smiley face", back at top):

```
            IN (-0.98)   OUT (+0.98)     <- back wall jacks (-z)
         . - - - - - - - - - - - .
      /   VOLUME o       o FUZZ    \    <- knobs = eyes (z -1.96)
     |        \ FUZZFACE /         |      white smile arc
     |             /|\             |
     |            / | \   pad      |    <- black triangle (apex z -0.25)
      \          /  o  \          /     <- footswitch = nose (z +1.38)
       '-.__ DUNLOP banner __.-'        <- pad front banner (z +2.95)
            front (+z)
```

The vertical wall (y 0–1.20) is straight in every elevation; the
dome is a shallow cone/sphere blend, not a flat deck — deck parts
must seat on the dome at their radius (the round builder's
`surfaceAt` equivalent), never at `dims.h`. The back jack plateau
(a stepped flat sector spanning roughly x -1.6..+1.6 at the back
rim, carrying the `IN`/`OUT` print) breaks pure revolution symmetry;
it is called out as a builder option in the spec notes, not faked
in the lathe points.

## Colour and print inventory

Colour samples (median of a lit, non-specular patch): top field
`#d40f1e`, side wall `#fc2f3f` / front wall `#fc3344` (same red under
different light). Spec colour is set a step darker so the studio key
does not wash it pink: enclosure `#c1101c` (red powder coat). Rubber
pad near-black `#131315` (sampled median (19,16,15)); knobs black;
print white; bottom plate silver (not modelled).

Print / marking inventory (every word on the pedal):

| Marking | Where | Treatment in the model |
|---|---|---|
| `IN` (white caps) | back plateau, above the IN jack (x -0.98) | Vector label (spec `labels`) |
| `OUT` (white caps) | back plateau, above the OUT jack (x +0.98) | Vector label |
| `VOLUME` + teardrop dot (white, arced) | around the VOLUME knob, opening toward the knob | Vector label below the knob (arc flattened — see spec notes) |
| `FUZZ` + teardrop dot (white, arced) | around the FUZZ knob | Vector label below the knob |
| `FUZZFACE®` (large white hand-lettered, smile arc) | centre, between the knobs and the pad apex | Vector label, `script`-style hand lettering approximated bold/rounded (exact letterforms need the proposed round decal — see spec notes) |
| `DUNLOP MANUFACTURING INC.` (black on white curved banner) | front edge of the rubber pad (z ~+2.95) | Pad decal texture (`textures/dunlop-fuzz-face-decal.png`: ribs + banner) |
| Ribs (~longitudinal grooves) | rubber pad field | Pad decal texture (drawn ribs; the pad mesh itself is smooth) |
| `Dunlop`, address, `CE`, barcode | bottom plate stickers | Not modelled (underside out of view), inventoried here |
| (none) | no LED print, no power print, no top logo beyond the above | — |

Knob pointers in the top view both sit near 12 o'clock (pointing
back, `-z`): spec `rot` VOLUME -0.12, FUZZ +0.10 (photo-derived,
±0.1 rad — the white line reads within a few degrees of vertical).

## Provisional / single-view values (flagged per the guide)

- Jack height y 0.65: back + both side elevations agree the nuts sit
  mid-wall, but no straight back-wall close-up exists; ±0.10 in.
- Pad base corners (±1.58, +3.38): extrapolated 40 px from the last
  clean dark row (y 1100) to the rim; ±0.08 in. Apex, switch, knobs,
  and jacks are direct mask centroids (not provisional).
- Lathe mid points (r 1.00–3.20): interpolated between the measured
  centre peak, knob-radius deck, and rim on three elevations;
  ±0.08 in. Centre peak and rim are direct silhouette reads.
- Back plateau extent (x ±1.6): top view only (it is a plan feature,
  so one true top view suffices), but not expressible until the
  round builder lands.
