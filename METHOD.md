# Z-axis database: method

This document describes how `heights.json` (vertical pedal heights for the
3D pedalboard visualizer) was built from the PedalPlayground catalog, which
publishes only 2D footprints (W x D). Nothing here is guessed: every entry is
either a published manufacturer/dealer spec, an inference from a verified
enclosure datasheet, or an explicit `null`.

## 1. Source dataset

- `pedals.json` — downloaded 2026-09-28 from
  `https://raw.githubusercontent.com/PedalPlayground/pedalplayground/master/public/data/pedals.json`
- 8,557 records; **8,550 unique `Brand | Name` keys**.
- Fields used: `Brand`, `Name`, `Width`, `Height`. Note: PedalPlayground's
  `Height` field is the **top-down depth** of the pedal, not its vertical
  height — the vertical (Z) dimension exists nowhere in their data.

### Duplicate keys (7)

`heights.json` is keyed by the exact string `"Brand | Name"`, so exact
duplicates collapse to one entry. Six of the seven duplicates are byte-identical
records (same footprint and image); the first occurrence is kept.

- `BOSS | BC-2 Combo Drive` — identical duplicates
- `Glou-Glou | Loupé (Blue)` — identical duplicates
- `Glou-Glou | Loupé (White)` — identical duplicates
- `JHS | AT+` — identical duplicates
- `MXR | Super Comp` — identical footprint, different images (`mxr-super-comp.png` vs `mxr-m132.png`)
- `Pedal Pawn | Gypsy Vibe` — identical duplicates
- `Kingtone | The Octaland` — **different footprints**: (4.7 x 3.7) vs (5.09 x 3.7), different images. First occurrence (4.7 x 3.7) is kept.

## 2. What "height" means here (important)

The database mixes two kinds of Z values, and `source` always says which:

- **Enclosure inference (confidence `medium`)**: the bare die-cast/folded
  enclosure height from a datasheet — footswitch, knobs, and jacks are
  *excluded*. These heights are systematic underestimates of the true maximum
  pedal height (typically by ~0.2–0.4").
- **Published pedal spec (confidence `high`)**: the manufacturer's or dealer's
  stated overall dimensions — usually *including* controls. Each `source`
  note records whether knobs/switches are included when the source says so;
  otherwise it reads "published overall height; inclusion of controls not
  explicitly stated".

The visualizer's practical goal is maximum pedal height (stomp clearance,
knob clearance, riser needs), so a published overall spec always overrides an
enclosure inference for the same pedal.

## 3. Verified enclosure reference table

All dimensions verified against the cited sources on 2026-09-28. Heights are
bare-enclosure (no knobs/switch).

| Enclosure key | Footprint W x D (in) | Height (in) | Spec source |
|---|---|---|---|
| `hammond_1590A` | 1.54 x 3.66 | 1.22 | Hammond 1590 datasheet: 93x39x31mm — https://www.mouser.com/datasheet/2/177/1590-1283706.pdf |
| `hammond_1590B` | 2.38 x 4.41 | 1.22 | Hammond 1590B: 112.4x60.5x31mm — https://www.farnell.com/datasheets/2297282.pdf |
| `hammond_125B` | 2.60 x 4.78 | 1.55 | 125B/1590N1 class: 121-122x66x39-39.5mm — https://lovemyswitches.com/125b-enclosure-bare-aluminum-powder-coat/ ; https://chinadaier.com/products/aluminum-enclosure-for-guitar-effects-pedal-1590n1/ |
| `hammond_1590BB` | 3.70 x 4.69 | 1.34 | 1590BB: 120x94.5x34mm — https://chinadaier.com/products/aluminum-enclosure-for-guitar-effects-pedal-1590bb/ |
| `hammond_1590G` | 1.97 x 3.94 | 1.02 | 1590G: 100x50x26mm — https://chinadaier.com/products/aluminum-enclosure-for-guitar-effects-pedal-1590g/ |
| `boss_compact` | 2.87 x 5.08 | 2.32 | Boss compact series: 73x129x59mm, Boss/Roland manuals — http://download.somanuals.com/pdf/view.php?id=7370564 |
| `mxr_standard` | 2.25 x 4.25 | 1.25 | Sweetwater Tech Specs, MXR M101 Phase 90 — https://www.sweetwater.com/store/detail/Phase90--mxr-m101-phase-90-phaser-pedal |
| `ehx_nano` | 2.75 x 4.50 | 2.10 | EHX official spec (Nano Big Muff): 70x115x54mm — https://www.ehx.com/products/nano-big-muff/ |
| `mooer_micro` | 1.65 x 3.68 | 2.05 | Mooer official micro-series spec: 93.5x42x52mm — https://www.worldwidemusic.co.uk/mooer-micro-series-hustle-drive-distortion-effects-pedal----brand-new-1304-p.asp |
| `dunlop_crybaby` | 4.00 x 10.00 | 2.50 | Dunlop official spec GCB95: 10x4x2.5 in — https://www.jimdunlop.com/gcb95-cry-baby-standard-wah/ |
| `strymon_small` | 4.00 x 4.50 | 1.75 | Strymon blueSky user manual: 4.5 deep x 4 wide x 1.75 tall — https://cf3.zzounds.com/media/Product_Manual-ec983f9fa2e6ee8110de70efb55b2ffd.pdf |
| `strymon_large` | 6.75 x 5.00 | 1.87 | Strymon BigSky user manual: 5 deep x 6.75 wide x 1.87 tall — https://knobsnob.app/api/catalog-public/strymon-bigsky/manual |
| `tc_standard` | 2.83 x 4.80 | 1.97 | TC Electronic official spec (Hall of Fame 2): 72x122x50mm — https://www.thomann.ie/tc_electronic_hall_of_fame_2.htm |

Notes on judgment calls:

- **125B**: Hammond's own catalog has no "125B" (it's a clone-market standard
  size). The 121x66x39mm clone dimension is used, sourced from pedal-parts
  vendors, and cross-checked against the 1590N1 (122x66x39.5mm), which is the
  nearest genuine Hammond size — they agree to 0.02", so they are treated as
  one class.
- **1590N1/G/BB**: verified via a third-party enclosure vendor's listings
  (Chinadaier), which reproduce Hammond's dimensional drawings. Not
  Hammond-authoritative, but mutually consistent; flagged here.
- **Dunlop Cry Baby**: Vintage King and Amazon list `10 x 4 x 2.5` in
  conflicting orders; Dunlop's official spec page confirms the 2.5" figure is
  the pedal's height. Treated as 2.50" maximum vertical height.
- **EHX Nano (2.10")**: this is the *overall* height from EHX's spec
  (70x115x54mm), likely including the footswitch — recorded as such in
  `source` notes, unlike the bare-enclosure Hammond rows.

## 4. Matching algorithm

Deterministic script: `build_db.py` → `heights_base.json`, then
high-confidence specs are merged on top (`heights.json`).

1. For each pedal, take its PedalPlayground footprint (W, D). Both
   orientations are tried in the generic pass, since some pedals mount an
   enclosure sideways (height is unaffected by orientation).
2. **Brand-priority pass**: brands with known house form factors are matched
   only against their enclosures, with a wide tolerance (|dW| <= 0.75",
   |dD| <= 0.90") because catalog footprints include jacks/protrusions
   (e.g. an MXR box records as 2.67x4.5 vs the bare 2.25x4.25):
   - BOSS → `boss_compact`; MXR → `mxr_standard`;
     Electro-Harmonix → `ehx_nano`; Dunlop → `dunlop_crybaby`;
     Strymon → `strymon_small`/`strymon_large`; TC Electronic → `tc_standard`;
     Mooer/Mosky → `mooer_micro`;
     JHS, Walrus Audio, EarthQuaker, Keeley, Wampler, Catalinbread,
     OBNE → `hammond_125B` (these are documented 125B shops; without this
     rule their ~2.9x5.0 catalog footprints mis-match to `boss_compact`).
   - If a priority-brand pedal fits none of its enclosures (BOSS 500-series,
     Dunlop Fuzz Face, EHX POG2, TC minis...), it is marked `low`/`null`
     rather than generic-guessed — those odd form factors are exactly where
     footprint matching goes wrong, and the popular ones are hand-verified.
3. **Generic pass** (other brands): nearest enclosure within |dW| <= 0.30",
   |dD| <= 0.45" by normalized squared distance. A clean unique match →
   `medium`. No match → `low` with `height_in: null`.
4. High-confidence hand-verified specs overwrite any inference for the same key.

## 5. Confidence levels

- `high` — published spec from the manufacturer, its manual, or a dealer
  quoting manufacturer specs (Sweetwater Tech Specs preferred). Hand-verified
  per pedal.
- `medium` — footprint cleanly matches a verified enclosure (bare-enclosure
  height; knobs/switch excluded). Correct enclosure family, approximate Z.
- `low` — no clean match; `height_in` is `null`. Never invented.

## 6. Coverage

Built 2026-09-28. 8,550 unique `Brand | Name` keys.

- `high`: **175** — hand-verified published specs (Sweetwater Tech Specs,
  manufacturer product pages/manuals, reputable dealers quoting manufacturer
  specs). ~168 pedals individually researched across BOSS, Dunlop, MXR,
  Electro-Harmonix, TC Electronic, Ibanez, Strymon, JHS, Walrus Audio,
  EarthQuaker, Keeley, Wampler, Catalinbread, and OBNE, plus 12 grouped
  family-spec additions (BOSS 200-series enclosure, Dunlop mini Fuzz Face
  family, Dunlop Echoplex Preamp). 122 override a medium inference, 41 fill
  a previous null. 2 requested pedals (Keeley Katana, Keeley Caverns V1)
  were honestly left unverified — conflicting/mismatched sources, no
  tie-breaker.
- `medium`: **6,060** — clean enclosure-footprint match (bare-enclosure
  height; knobs/switch excluded).
- `low`: **2,315** — no clean enclosure match; `height_in` is `null`.

## 7. Known limitations

- **Footprint-band ambiguity**: many builders' ~2.6–2.9 x 4.4–5.1 footprints
  sit between the 125B (1.55"), TC standard (1.97"), and EHX Nano (2.10")
  classes. The generic matcher picks the nearest, but a pedal recorded at
  2.75x4.5 could be any of the three — systematic uncertainty up to ~0.5"
  for `medium` entries in this band from non-priority brands.
- **Enclosure heights exclude hardware**: `medium` values are bare boxes.
  Real max height is higher by roughly the footswitch/knob stack (~0.2–0.4").
- **No orientation info**: a sideways-mounted enclosure gets the right
  height but the visualizer shouldn't infer orientation from `enclosure`.
- **Wah/volume pedals**: `dunlop_crybaby` (2.50") covers Dunlop treadle wahs;
  other brands' treadle pedals (Morley, etc.) mostly fall to `low` — treadle
  geometry varies too much to infer.
- **Power supplies, loopers, multi-FX**: generally `low`/`null`; their
  form factors don't map to stompbox enclosures.

## 8. Notable popular gaps (`low`/`null`, worth hand-verifying next)

These are compact, popular-format pedals whose form factors don't map to the
reference enclosures. The highest-value targets:

- **EHX wide-XO cluster** (~4.19x4.75): B9 Organ Machine, 720/1440 Stereo
  Looper, Big Muff w/ Tone Wicker, #1 Echo, Bass Mono Synth, 15Watt Howitzer.
  One authoritative EHX dimension would unlock the whole cluster (~2.25"?).
- **EQD large-enclosure pedals** (3.7–4.34 x 4.8–5.0): Astral Destiny,
  Pyramids, Life Pedal V2, Avalanche Run V2, Sea Machine, Disaster Transport,
  Gray Channel, Spires, Zap Machine V2. Likely ~2.25" but unverified.
- **Dunlop mini wahs** (3.1x5.24): Cry Baby Mini 535Q, Mini Bass Wah,
  Q Mini Auto-Return — same shell family as the verified CBM95 (3.75").
- **Dunlop Hendrix Shrine minis** (1.74x3.7): Fuzz Face, Octavio, Uni-Vibe,
  Band of Gypsys shrine series.
- **Catalinbread minis** (1.8x3.7): Epoch Boost Mini, Fuzzrite Mini,
  Little Secret.
- **Keeley Katana / Caverns V1**: researched, sources conflicted or belonged
  to a different hardware revision — deliberately left null.
- **Treadle pedals generally** (Morley, Ernie Ball VP, BOSS FV/EV series):
  treadle geometry varies too much to infer; all null.
- **Multi-FX / loop stations / switchers** (BOSS GT/ME/RC-300/600, Line 6,
  GigRig): null by design — not stompbox form factors.

## 9. Extending / correcting the database

- Re-run: `python3 build_db.py` regenerates `heights_base.json` from
  `pedals.json`; merge hand-verified entries with `merge_verified.py`.
- To correct one pedal: edit its entry in `heights.json` directly, set
  `confidence` to `high`, and put the spec URL plus what it includes in
  `source`.
- To add an enclosure: append a row to `ENCLOSURES` in `build_db.py` with a
  verifiable source URL, plus a brand-priority entry if a brand uses it
  house-wide.
- Never fill a `null` by guessing. A wrong number in a 3D visualizer is
  worse than a missing one.
