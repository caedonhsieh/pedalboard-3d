# EHX Small Clone (EH 4600 Full-Chorus) — measurements

Slug: `ehx-small-clone`. Exact model: current Small Clone reissue (not Nano Clone / Neo Clone).

## References (guide Step 1)

| View | File | Source |
|---|---|---|
| 3/4 front (hero) | `references/ehx-small-clone_front.jpg` (1500x1000) | EHX product page `clone-f-1.jpg` |
| 3/4 top/front | `references/ehx-small-clone_detail1.jpg` (1000x1000) | EHX product page `clone-1.jpg` |
| Back wall | `references/ehx-small-clone_detail2.jpg` (1000x1000) | EHX product page `clone-2.jpg` |
| Side A | `references/ehx-small-clone_side1.jpg` (1000x1000) | EHX product page `clone-3.jpg` |
| Side B | `references/ehx-small-clone_side2.jpg` (1000x1000) | EHX product page `clone-4.jpg` |

Each `.jpg` has a matching `.META.txt` from `scripts/fetch_views.py`. Five views: satisfied.

## Published dimensions (anchor)

- `data/spec_sheets_staging.json` (verified, EHX spec block via dealers): 3.38 x 5.25 x 2.75 in
  (85.9 x 133.4 x 69.9 mm). EHX orders L x W x H; mapped w=3.38 (L-R), d=5.25 (F-B), h=2.75.
- Conflict: `verified_mxr_ehx.json` lists height 1.6 in (Rubber Monkey) — rejected as
  enclosure-only/package confusion; side-photo calibration below gives bare back 2.09 in
  and overall-with-knob ~2.63 in, corroborating 2.75 in as overall (knobs included).
- Spec `dims.h` = bare back height 2.09 in (measured), not the 2.75 in overall.

## Side-profile calibration (side1, 1000x1000)

- Enclosure depth in frame: x ~88 to ~905 px = 817 px for 5.25 in -> 155.6 px/in.
- Bottom edge y ~660 px. Back top y ~335 px -> bare back (660-335)/155.6 = **2.09 in**.
- Front top y ~455 px -> bare front (660-455)/155.6 = **1.32 in**.
- Knob top y ~250 px -> overall (660-250)/155.6 = **2.63 in** ≈ published 2.75 in.
- Profile (back -z to front +z): `[[-2.625, 2.09], [2.625, 1.32]]` — single straight slope.
- Construction: brushed-silver top plate over black sheet-metal box (black sides,
  silver back panel where jacks/power mount — see detail2). Same construction as
  Big Muff Pi; modelled black enclosure + silver `backColor` + top decal.

## Top layout (detail1 + front, symmetrised; provisional, single-family views)

| Part | x (in) | z (in) | Notes |
|---|---|---|---|
| RATE knob | +0.15 | -1.65 | Black hockey-puck ~1.05 in dia; tick arc around it |
| DEPTH toggle | -0.85 | -1.65 | Small black slide toggle left of RATE (no parts.js builder — see spec notes) |
| STATUS LED (red) | +0.95 | -1.65 | Right of RATE, same row |
| Footswitch (round) | 0.00 | +1.25 | Centred in purple panel |
| OUTPUT jack | -1.02 | back wall | Back face, left in top view |
| INPUT jack | +1.02 | back wall | Back face, right in top view |
| Power jack | 0.00 | back wall | Centred, round barrel (detail2) |

Back wall (detail2, viewed from behind; image-left = pedal right/+x):
INPUT (+1.02) image-left, power (0) centre, OUTPUT (-1.02) image-right. Jack y ~0.95 in.

## Print inventory (front + detail1)

- Back edge: `OUTPUT` (left), `9V` (centre), `INPUT` (right), white caps on black.
- `DEPTH` under toggle, `RATE` under knob, `STATUS` under LED; tick marks around RATE.
- Purple panel: `SMALL` / `CLONE` large white block, `EH 4600 FULL-CHORUS` beneath.
- Front strip: `ELECTRO HARMONIX` (with EH block logo) white on black, `USA` beneath.
- Screws: black top panel corners + purple panel lower corners (6 total).

Colours: top/back plate brushed silver ~#c9c9c7, sides near-black ~#17181a,
purple panel ~#4b1fa6, print white, knobs black, LED red.
