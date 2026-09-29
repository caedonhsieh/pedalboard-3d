// parts.js — parametric part library for pedalboard-3d hero models.
//
// Every hero model is data (specs/<id>.json) + these shared parts.
// Coordinate convention (inches): x = width, z = depth (back = -z,
// front = +z), y up from the base (y=0 at the bottom of the pedal).
// Spec positions (knobs, switch, LED, jacks) are given in pedal-space
// x/z with the origin at the pedal's center.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

export const IN = 25.4; // mm per inch

/* ---------------- procedural micro-textures ---------------- */
export function stripeTexture({ horizontal = true, stripes = 24, size = 256 } = {}) {
  const c = document.createElement('canvas'); c.width = c.height = size;
  const g = c.getContext('2d');
  g.fillStyle = '#808080'; g.fillRect(0, 0, size, size);
  const step = size / stripes;
  for (let i = 0; i < stripes; i++) {
    g.fillStyle = i % 2 ? '#5a5a5a' : '#a6a6a6';
    if (horizontal) g.fillRect(0, Math.round(i * step), size, Math.max(1, Math.round(step / 2)));
    else g.fillRect(Math.round(i * step), 0, Math.max(1, Math.round(step / 2)), size);
  }
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}

/* ---------------- shared finishes (the part library's materials) ---------------- */
export const FIN = {
  green: new THREE.MeshPhysicalMaterial({
    color: 0x7fb75c, roughness: 0.38, metalness: 0.0,
    clearcoat: 0.55, clearcoatRoughness: 0.28, envMapIntensity: 0.85,
  }),
  blackPlastic: new THREE.MeshStandardMaterial({
    color: 0x121215, roughness: 0.55, metalness: 0.0, envMapIntensity: 0.6,
  }),
  knobRib: new THREE.MeshStandardMaterial({
    color: 0x141416, roughness: 0.5, metalness: 0.05, envMapIntensity: 0.7,
    bumpMap: stripeTexture({ horizontal: false, stripes: 26 }), bumpScale: 0.6,
  }),
  chrome: new THREE.MeshStandardMaterial({
    color: 0xf4f4f6, roughness: 0.22, metalness: 1.0, envMapIntensity: 1.35,
  }),
  plateRib: new THREE.MeshStandardMaterial({
    color: 0xf4f4f6, roughness: 0.26, metalness: 1.0, envMapIntensity: 1.35,
    bumpMap: stripeTexture({ horizontal: true, stripes: 30 }), bumpScale: 0.35,
  }),
  silverCap: new THREE.MeshStandardMaterial({
    color: 0xd9d9de, roughness: 0.32, metalness: 0.9, envMapIntensity: 1.1,
  }),
  pointer: new THREE.MeshStandardMaterial({
    color: 0xf2f2f2, roughness: 0.4, metalness: 0.0,
    emissive: 0xffffff, emissiveIntensity: 0.25,
  }),
  led: new THREE.MeshPhysicalMaterial({
    color: 0x2a0505, roughness: 0.25, metalness: 0.0,
    emissive: 0xff2015, emissiveIntensity: 2.4, clearcoat: 1.0, envMapIntensity: 0.8,
  }),
  jackChrome: new THREE.MeshStandardMaterial({
    color: 0xe8e8ec, roughness: 0.35, metalness: 0.6, envMapIntensity: 1.0,
  }),
  darkMetal: new THREE.MeshStandardMaterial({
    color: 0x2a2a2e, roughness: 0.45, metalness: 0.85, envMapIntensity: 0.8,
  }),
};
FIN.knobRib.bumpMap.repeat.set(3, 1);

/** Powder-coat enclosure finish in any color (same PBR recipe as the TS9 green). */
export function powderCoat(color) {
  return new THREE.MeshPhysicalMaterial({
    color: new THREE.Color(color), roughness: 0.38, metalness: 0.0,
    clearcoat: 0.55, clearcoatRoughness: 0.28, envMapIntensity: 0.85,
  });
}

export function shadowed(m) { m.castShadow = true; m.receiveShadow = true; return m; }

/* ---------------- enclosures ---------------- */

/**
 * Boxy enclosure for MXR / EHX / Boss-style pedals.
 * {w, d, h} in inches, y=0 at the base.
 */
export function boxEnclosure({ w, d, h, edgeRadius = 0.06, material = FIN.green } = {}) {
  const g = new THREE.Group();
  g.userData.kind = 'enclosure';
  const body = shadowed(new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 4, edgeRadius), material));
  body.position.y = h / 2;
  g.add(body);
  g.userData.dims = { w, d, h };
  return g;
}

/**
 * Extruded custom side profile for unorthodox shapes (TS9 wedge, etc.).
 * points: [[z, y], ...] from back (-d/2) to front (+d/2), y up from base.
 * The profile is the NOMINAL design intent; bevel compensation is applied
 * internally so the outer surface matches the points. The bevel expands the
 * outline outward by exactly `bevel`, so every pre-bevel outline point is
 * inset by `bevel` along the outline — the outer surface then lands on the
 * nominal points (up to normal bevel-arc rounding at corners).
 * frontLean: inches the front face leans forward at the top (slightly sloped
 * front face, e.g. 0.06 on the TS9). Implemented by setting the front-BOTTOM
 * corner back by frontLean; the front-TOP corner keeps full bevel
 * compensation and lands exactly on the nominal spec point. (Subtracting the
 * lean from the top corner instead would let the bevel push the outer surface
 * `frontLean` past nominal — a real bug we shipped once: +0.06" silhouette
 * overshoot on the TS9.)
 * Shape +x (tall end) maps to world -z (back) after rotation.y.
 */
export function profileEnclosure({ w, d, points, bevel = 0.05, frontLean = 0, material = FIN.green, smooth = true } = {}) {
  const b = bevel;
  const X = (z) => -z; // shape-x from board-z
  // Densify the spec polyline through a centripetal Catmull-Rom so the deck
  // renders as one smooth surface. The spec points stay the source of truth;
  // without this the 7 straight facets show visible crease lines under studio
  // lighting even though the silhouette is correct.
  // For sharp polygons (e.g. TS9 irregular hexagon), set smooth=false to use
  // the raw polyline with crisp corners.
  let dense;
  if (smooth) {
    const curve = new THREE.CatmullRomCurve3(
      points.map(([z, y]) => new THREE.Vector3(X(z), y, 0)), false, 'centripetal');
    dense = curve.getPoints(72);
  } else {
    dense = points.map(([z, y]) => new THREE.Vector3(X(z), y, 0));
  }
  const n = dense.length;
  const s = new THREE.Shape();
  s.moveTo(dense[n - 1].x + b + frontLean, b);
  s.lineTo(dense[0].x - b, b);
  for (let i = 0; i < n; i++) {
    let x = dense[i].x;
    if (i === 0) x -= b;
    else if (i === n - 1) x += b;
    s.lineTo(x, dense[i].y - b);
  }
  s.closePath();
  const geo = new THREE.ExtrudeGeometry(s, {
    depth: w - 2 * b, bevelEnabled: true,
    bevelThickness: b, bevelSize: b, bevelSegments: 4, steps: 1,
  });
  geo.translate(0, 0, -(w - 2 * b) / 2);
  const g = new THREE.Group();
  const body = shadowed(new THREE.Mesh(geo, material));
  g.userData.kind = 'enclosure';
  body.rotation.y = Math.PI / 2;
  g.add(body);
  g.userData.dims = { w, d, h: Math.max(...points.map((p) => p[1])) };
  return g;
}

/** Black base plate, slightly inset. */
export function basePlate({ w, d, h = 0.09 } = {}) {
  const m = shadowed(new THREE.Mesh(new THREE.BoxGeometry(w - 0.12, h, d - 0.12), FIN.blackPlastic));
  m.position.y = h / 2;
  const g = new THREE.Group(); g.add(m);
  g.userData.kind = 'base';
  return g;
}

/* ---------------- parts ---------------- */

/**
 * Control knob. Styles:
 *  - 'ts9': ribbed skirt + silver cap + pointer (Ibanez TS9)
 *  - 'mxr': Davies-style fluted black knob + pointer (MXR Phase 90 etc.)
 * pointerRot: rotation of the pointer, radians.
 * Origin at the knob base (sits on the deck at y=0).
 */
export function knob(style = 'ts9', pointerRot = 0, scale = 1) {
  // tagged below
  const k = new THREE.Group();
  k.userData.kind = 'knob';
  if (style === 'mxr') {
    const body = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.31, 0.42, 32), FIN.knobRib));
    body.position.y = 0.21;
    const top = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.27, 0.03, 32), FIN.blackPlastic);
    top.position.y = 0.425; top.castShadow = true;
    const pointer = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.014, 0.20), FIN.pointer);
    pointer.position.set(0, 0.44, -0.055);
    const pg = new THREE.Group(); pg.add(pointer); pg.rotation.y = pointerRot;
    k.add(body, top, pg);
  } else if (style === 'boss') {
    // Boss compact knobs: black body with silver aluminum cap, white indicator.
    // Large: 0.54" dia, Small (DIST): 0.42" dia. Scale via the scale param.
    const skirt = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.27, 0.45, 32), FIN.knobRib));
    skirt.position.y = 0.225;
    const cap = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.19, 0.19, 0.04, 32), FIN.silverCap));
    cap.position.y = 0.47;
    const pointer = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.012, 0.16), FIN.pointer);
    pointer.position.set(0, 0.495, -0.045);
    const pg = new THREE.Group(); pg.add(pointer); pg.rotation.y = pointerRot;
    k.add(skirt, cap, pg);
  } else { // 'ts9'
    // Davies-style TS9 knobs. Overlay vs Sweetwater photo shows the original
    // 0.66" diameter is correct (the 0.34" "fix" was based on a bad measurement).
    // Tick rings in decal are sized to sit OUTSIDE the knob (0.70" dia).
    const skirt = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.295, 0.33, 0.60, 48), FIN.knobRib));
    skirt.position.y = 0.30;
    const cap = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.05, 48), FIN.silverCap));
    cap.position.y = 0.625;
    const pointer = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.014, 0.19), FIN.pointer);
    pointer.position.set(0, 0.652, -0.055);
    const pg = new THREE.Group(); pg.add(pointer); pg.rotation.y = pointerRot;
    k.add(skirt, cap, pg);
  }
  k.userData.knobStyle = style;
  if (scale !== 1) k.scale.setScalar(scale);
  return k;
}

/**
 * Footswitch. Styles:
 *  - 'plate': TS9-style rectangular chrome treadle plate + black bezel
 *  - 'round': MXR-style round chrome button + washer
 * {w, d} = plate size in inches (ignored for 'round'). Origin at deck (y=0).
 */
export function footswitch({ w = 2.046, d = 1.382, style = 'plate', frameColor = null,
  plateW: specPlateW = null, plateD: specPlateD = null,
  padW: specPadW = null, padD: specPadD = null, padCz: specPadCz = null,
  deckPitch = 0 } = {}) {
  const g = new THREE.Group();
  if (style === 'round') {
  g.userData.kind = 'treadle';
    const washer = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.30, 0.30, 0.04, 32), FIN.chrome));
    washer.position.y = 0.02;
    const btn = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.24, 0.22, 32), FIN.chrome));
    btn.position.y = 0.14;
    g.add(washer, btn);
  } else if (style === 'boss-pedal') {
    // Boss compact footswitch: SOLID orange plate, hinged at back,
    // with black rubber pad on top.
    // MEASURED from ds1_top.png (2026-09-29 pixel analysis):
    //   Pad: 61.6mm wide (2.425"), 40.5mm deep (1.594"), center z=+1.333".
    //   Plate: 68mm wide (2.677"), 55mm deep (2.165"). Hinge at z=+0.413".
    // Origin at hinge (spec footswitch.z).
    const plateD = specPlateD ?? 2.322;
    const plateW = specPlateW ?? 2.677;
    const plateT = 0.217; // 5.5mm — measured from ds1_sw_detail3.jpg (was 2mm, too thin)
    const padD = specPadD ?? 1.594;
    const padW = specPadW ?? 2.425;
    const padT = 0.12;
    // padCz is passed hinge-relative (spec padCz minus spec footswitch.z)
    // Default: pad center z=+1.333", hinge at +0.217" → relative 1.116"
    const padRelZ = specPadCz ?? 1.116;
    // REBUILT 2026-09-29 from component alignment:
    // The treadle plate is HORIZONTAL. The wedge gap comes from the body sloping
    // down beneath it (10.1 deg), not from tilting the plate.

    // Treadle plate gets its own material (not global powderCoat): the plate is a
    // large horizontal surface that catches the key light directly. The shared
    // powderCoat's clearcoat blows it out to white; a flatter standard material
    // in the same base color renders as the same orange the eye sees on the body.
    // TS9's global powderCoat is untouched.
    const fmat = frameColor
      ? new THREE.MeshStandardMaterial({ color: new THREE.Color(frameColor), roughness: 0.62, metalness: 0.0, envMapIntensity: 0.35 })
      : FIN.green;

    // Hinge group at the part origin (which is the hinge point in pedal coords,
    // set by the spec's footswitch.z).
    // Treadle extends FORWARD (+z) from the hinge.
    const hinge = new THREE.Group();
    hinge.position.y = 0.148; // plate center 3.75mm above deck: 1mm gap + 2.75mm half-thickness
    // hinge at origin; treadle children positioned forward

    // Treadle subgroup (plate + pad)
    const treadle = new THREE.Group();
    // Plate: solid orange box, extends from hinge (z=0) forward to z=plateD
    const plate = shadowed(new THREE.Mesh(
      new RoundedBoxGeometry(plateW, plateT, plateD, 2, 0.02), fmat
    ));
    plate.position.set(0, 0, plateD / 2);
    treadle.add(plate);

    // Pad: black rubber, on top of plate. padRelZ is hinge-relative (from spec).
    const pad = shadowed(new THREE.Mesh(
      new RoundedBoxGeometry(padW, padT, padD, 4, 0.06), FIN.blackPlastic
    ));
    pad.position.set(0, plateT/2 + padT/2, padRelZ);
    treadle.add(pad);

    // BOSS logo embossed on the pad (raised, subtle black-on-black)
    const logoCanvas = document.createElement('canvas');
    logoCanvas.width = 512; logoCanvas.height = 128;
    const lctx = logoCanvas.getContext('2d');
    lctx.clearRect(0, 0, 512, 128);
    lctx.fillStyle = '#1a1a1c';  // slightly darker than pad
    lctx.font = '700 72px Arial, sans-serif';
    lctx.textAlign = 'center'; lctx.textBaseline = 'middle';
    lctx.fillText('BOSS', 256, 64);
    const logoTex = new THREE.CanvasTexture(logoCanvas);
    logoTex.colorSpace = THREE.SRGBColorSpace;
    const logo = new THREE.Mesh(
      new THREE.PlaneGeometry(padW * 0.6, padW * 0.15),
      new THREE.MeshStandardMaterial({ map: logoTex, transparent: true, roughness: 0.8 })
    );
    logo.rotation.x = -Math.PI / 2;
    logo.position.set(0, plateT/2 + padT + 0.001, padRelZ);
    treadle.add(logo);

    // Hinge rotation: the footswitch is a child of the sloped deck group.
    // REBUILT 2026-09-29: the treadle plate is HORIZONTAL in world space.
    // Cancel the deck pitch exactly so the plate does not inherit the body slope.
    // The wedge gap forms because the BODY slopes down beneath the level plate.
    hinge.rotation.x = -deckPitch;
    hinge.add(treadle);
    g.add(hinge);
  } else {
    // TS9-style: black bezel RECESSED into the deck (sunk so only a thin lip
    // shows; the deck occludes the rest), chrome treadle sitting down inside it.
    const bezel = shadowed(new THREE.Mesh(new RoundedBoxGeometry(w + 0.26, 0.12, d + 0.26, 4, 0.06), FIN.blackPlastic));
    bezel.position.y = -0.04;
    const plate = shadowed(new THREE.Mesh(new RoundedBoxGeometry(w, 0.16, d, 4, 0.05), FIN.plateRib));
    plate.position.y = 0.06;
    g.add(bezel, plate);
  }
  g.userData.switchStyle = style;
  return g;
}

/** Ibanez logo plate: black border + white plate + blue "Ibanez" text.
 *  Physical 3D element on the downslope deck. Origin at deck (y=0). */
export function ibanezPlate({ w = 2.145, d = 0.733, border = 0.06 } = {}) {
  const g = new THREE.Group();
  // Black border (slightly larger, thin)
  g.userData.kind = 'plate';
  const borderMesh = shadowed(new THREE.Mesh(
    new RoundedBoxGeometry(w + border*2, 0.04, d + border*2, 2, 0.02),
    FIN.blackPlastic
  ));
  borderMesh.position.y = 0.02;
  // White plate on top
  const plateMesh = shadowed(new THREE.Mesh(
    new RoundedBoxGeometry(w, 0.04, d, 2, 0.02),
    new THREE.MeshStandardMaterial({ color: 0xf5f5f5, roughness: 0.35, metalness: 0.0 })
  ));
  plateMesh.position.y = 0.05;
  g.add(borderMesh, plateMesh);
  // "Ibanez" text via canvas texture — bright cyan-blue, bold rounded italic
  const canvas = document.createElement('canvas');
  canvas.width = 1024; canvas.height = 256;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#f5f5f5';
  ctx.fillRect(0, 0, 1024, 256);
  ctx.fillStyle = '#31B4F7';  // sampled from reference photo 2026-09-28
  ctx.font = 'italic 900 175px "Arial Rounded MT Bold", Arial, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  // Real Ibanez logo is bold and elongated — stretch horizontally
  ctx.save();
  ctx.translate(512, 140);
  ctx.scale(1.45, 1);
  ctx.fillText('Ibanez', 0, 0);
  ctx.restore();
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  const textMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(w * 0.85, d * 0.55),
    new THREE.MeshStandardMaterial({ map: tex, transparent: true, roughness: 0.35 })
  );
  textMesh.rotation.x = -Math.PI / 2;
  textMesh.position.y = 0.071;
  g.add(textMesh);
  return g;
}

/** Dot ring: small black dots around a Boss knob. Flat on deck.
 *  Real Boss: dots at knob positions, not wedges. Clean vector. */
export function dotRing({ r = 0.42, dots = 11, dotR = 0.035 } = {}) {
  const size = 512;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, size, size);
  ctx.fillStyle = '#111';
  const c = size / 2;
  const px = (rr) => rr / r * (size / 2) * 0.95;
  for (let i = 0; i < dots; i++) {
    const a = (i / dots) * Math.PI * 2 - Math.PI / 2;
    const x = c + Math.cos(a) * px(r);
    const y = c + Math.sin(a) * px(r);
    ctx.beginPath();
    ctx.arc(x, y, px(dotR), 0, Math.PI * 2);
    ctx.fill();
  }
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  const m = new THREE.Mesh(
    new THREE.CircleGeometry(r, 48),
    new THREE.MeshStandardMaterial({ map: tex, transparent: true, roughness: 0.6, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 })
  );
  m.rotation.x = -Math.PI / 2;
  const g = new THREE.Group();
  g.add(m);
  g.userData.kind = 'ring';
  return g;
}

/** Tick ring: black wedge segments around a knob. Flat on deck.
 *  Real TS9: 12 positions around circle, 10 trapezoidal wedges rendered
 *  (2-trapezoid gap centered at bottom). Wedges tuck slightly under the knob
 *  base (inner r=0.32" vs knob base 0.33") so they're flush with no gap.
 *  Outer r=0.485". Clean vector — no photo paste. */
export function tickRing({ innerR = 0.32, outerR = 0.485, wedges = 12 } = {}) {
  const size = 512;
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, size, size);
  ctx.fillStyle = '#111';
  const c = size / 2;
  const px = (r) => r / outerR * (size / 2);
  // 12 positions, 10 wedges rendered (2-trapezoid gap centered at bottom)
  // Canvas angle: -π/2=top, π/2=bottom. Skip the 2 wedges straddling the bottom.
  const step = (Math.PI * 2) / wedges;
  const wedgeAngular = step * 0.8;  // wedge covers 80% of step, gap 20%
  for (let i = 0; i < wedges; i++) {
    // Half-step offset so the 2-wedge gap lands symmetric around the bottom
    const centerA = (i / wedges) * Math.PI * 2 - Math.PI / 2 + step / 2;
    // Skip the 2 wedges centered around the bottom (angle ≈ π/2)
    let normA = centerA;
    while (normA > Math.PI) normA -= Math.PI * 2;
    while (normA < -Math.PI) normA += Math.PI * 2;
    if (Math.abs(normA - Math.PI / 2) < step) continue;  // 2-wedge gap at bottom
    const a0 = centerA - wedgeAngular / 2;
    const a1 = centerA + wedgeAngular / 2;
    // Trapezoid: inner arc to outer arc
    ctx.beginPath();
    ctx.moveTo(c + Math.cos(a0) * px(innerR), c + Math.sin(a0) * px(innerR));
    ctx.lineTo(c + Math.cos(a0) * px(outerR), c + Math.sin(a0) * px(outerR));
    ctx.arc(c, c, px(outerR), a0, a1);
    ctx.lineTo(c + Math.cos(a1) * px(innerR), c + Math.sin(a1) * px(innerR));
    ctx.arc(c, c, px(innerR), a1, a0, true);
    ctx.closePath();
    ctx.fill();
  }
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  const m = new THREE.Mesh(
    new THREE.CircleGeometry(outerR, 48),
    new THREE.MeshStandardMaterial({ map: tex, transparent: true, roughness: 0.6, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 })
  );
  m.rotation.x = -Math.PI / 2;
  const g = new THREE.Group();
  g.add(m);
  g.userData.kind = 'ring';
  return g;
}

/** Flat text label on the deck. Clean vector text via canvas. */
export function textLabel({ text, w = 0.3, h = 0.12, color = '#1a1a1a', bg = null, font = null, spaced = true, arrow = null, script = false, bold = false } = {}) {
  const canvas = document.createElement('canvas');
  canvas.width = 512; canvas.height = 256;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, 512, 256);
  // Optional solid background (e.g. white PSA label)
  if (bg) { ctx.fillStyle = bg; ctx.fillRect(0, 0, 512, 256); }
  ctx.fillStyle = color;
  // Font selection: script (italic serif), bold, or standard
  if (!font) {
    if (script) font = 'italic 700 130px Georgia, serif';
    else if (bold) font = '800 140px Arial, sans-serif';
    else font = '600 115px Arial, sans-serif';
  }
  ctx.font = font;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  // Letter-spacing for the TS9 label style (wide-tracked caps); disable for script words
  let render = spaced && !script ? text.split('').join('\u2009') : text;
  // Add arrow symbol if specified
  if (arrow === 'left') render = '\u2190 ' + render;
  else if (arrow === 'right') render = render + ' \u2192';
  // Multi-line support: split on \n and stack vertically
  const lines = render.split('\n');
  const lineH = 256 / (lines.length + 0.5);
  lines.forEach((ln, i) => {
    ctx.fillText(ln, 256, lineH * (i + 0.75));
  });
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = 8;
  const m = new THREE.Mesh(
    new THREE.PlaneGeometry(w, h),
    new THREE.MeshStandardMaterial({ map: tex, transparent: true, roughness: 0.6, polygonOffset: true, polygonOffsetFactor: -4, polygonOffsetUnits: -4 })
  );
  m.rotation.x = -Math.PI / 2;
  const g = new THREE.Group();
  g.add(m);
  g.userData.kind = 'label';
  return g;
}

/** LED with chrome bezel + emissive dome + glow light. Origin at deck (y=0). */
export function led() {
  const g = new THREE.Group();
  const bezel = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.098, 0.06, 32), FIN.chrome));
  g.userData.kind = 'led';
  bezel.position.y = 0.03;
  const dome = new THREE.Mesh(new THREE.SphereGeometry(0.062, 24, 16, 0, Math.PI * 2, 0, Math.PI / 2), FIN.led);
  dome.position.y = 0.055;
  const glow = new THREE.PointLight(0xff2a18, 0.9, 0.8, 2);
  glow.position.y = 0.35;
  g.add(bezel, dome, glow);
  return g;
}

/**
 * 1/4" side jack, built along +X (mounts on the right wall as-is;
 * rotate y by PI for the left wall). Origin at the wall plane.
 * Washer -> hex nut (0.55" across flats) -> dark socket bore.
 */
export function jack() {
  const g = new THREE.Group();
  // Washer: outer circle, against the enclosure wall
  g.userData.kind = 'jack';
  const washerGeo = new THREE.CylinderGeometry(0.31, 0.31, 0.035, 32);
  washerGeo.rotateZ(Math.PI / 2);
  const washer = shadowed(new THREE.Mesh(washerGeo, FIN.jackChrome));
  washer.position.x = 0.018;
  // Nut: smaller hex, in front of washer. Reduced from 0.55" to 0.48" so washer rim shows.
  const nutGeo = new THREE.CylinderGeometry(0.48 / Math.sqrt(3), 0.48 / Math.sqrt(3), 0.09, 6);
  nutGeo.rotateZ(Math.PI / 2);
  nutGeo.rotateX(Math.PI / 6); // flat faces up/down
  const nut = shadowed(new THREE.Mesh(nutGeo, FIN.jackChrome));
  nut.position.x = 0.035 + 0.045;
  // Bore: dark hole, extends in front of nut face so it's visible
  const boreGeo = new THREE.CylinderGeometry(0.125, 0.125, 0.20, 24);
  boreGeo.rotateZ(Math.PI / 2);
  const bore = new THREE.Mesh(boreGeo,
    new THREE.MeshStandardMaterial({ color: 0x060606, roughness: 0.9, metalness: 0.2 }));
  bore.position.x = 0.08; // front face at x=0.18, in front of nut (0.125)
  const ringGeo = new THREE.CylinderGeometry(0.062, 0.062, 0.02, 16);
  ringGeo.rotateZ(Math.PI / 2);
  const contact = new THREE.Mesh(ringGeo, FIN.darkMetal);
  contact.position.x = 0.015;
  g.add(washer, nut, bore, contact);
  return g;
}

/** 9V barrel power jack on the back wall (faces -z). Origin at the wall plane.
 * Boss compact: black SQUARE bezel (~15mm) with round barrel in center. */
export function powerJack() {
  const g = new THREE.Group();
  // Square bezel
  const bezel = shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.59, 0.59, 0.06), FIN.blackPlastic));
  bezel.position.z = -0.03;
  // Round barrel housing
  const housing = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.088, 0.088, 0.09, 24), FIN.blackPlastic));
  housing.rotation.x = Math.PI / 2;
  housing.position.z = -0.06;
  const pin = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.028, 0.10, 12), FIN.darkMetal);
  pin.rotation.x = Math.PI / 2;
  pin.position.z = -0.06;
  g.add(bezel, housing, pin);
  return g;
}

/* ---------------- studio scene (hero presentation) ---------------- */

/**
 * True when the WebGL context is a software rasterizer (SwiftShader,
 * llvmpipe, …) rather than real GPU hardware. Typical in headless / CI
 * browsers. The studio's heavy synchronous GPU work (PMREM environment
 * convolution, large PCFSoft shadow maps, MSAA + clearcoat materials) is
 * fine on hardware GL but can block the main thread for tens of seconds
 * under software GL — long enough for the browser to kill the page as
 * "unresponsive". Callers degrade gracefully instead.
 */
export function isSoftwareGL(renderer) {
  try {
    const gl = renderer.getContext();
    const ext = gl.getExtension('WEBGL_debug_renderer_info');
    const name = ext ? String(gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) || '') : '';
    return /swiftshader|llvmpipe|softpipe|software rasterizer|basic render/i.test(name);
  } catch {
    return false;
  }
}

/**
 * The shared studio: gradient backdrop, soft floor, 3-point-ish lighting,
 * environment reflections, orbit controls with gentle auto-rotate.
 *
 * On software WebGL (headless/test browsers) the expensive bits are scaled
 * back — pixel ratio 1, 1024px shadows, no PMREM environment convolution —
 * so the page stays interactive. Visuals on hardware GL are untouched.
 */
export function studioScene(container, {
  cameraPos = [6.4, 4.8, 8.8], target = [0, 1.25, 0],
  autoRotate = true, exposure = 1.12,
} = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  const softwareGL = isSoftwareGL(renderer);
  renderer.setPixelRatio(softwareGL ? 1 : Math.min(window.devicePixelRatio, 2));
  renderer.setSize(container.clientWidth || window.innerWidth, container.clientHeight || window.innerHeight);
  // Shadow maps are the biggest per-frame cost after env lighting — disable
  // entirely under software GL (headless/test browsers) where they can hang
  // the renderer. On hardware GL they stay on.
  renderer.shadowMap.enabled = !softwareGL;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = exposure;
  container.appendChild(renderer.domElement);

  const scene = new THREE.Scene();

  // dark studio backdrop: soft radial gradient, near-black edges
  const bgC = document.createElement('canvas'); bgC.width = bgC.height = 512;
  const bg = bgC.getContext('2d');
  const grd = bg.createRadialGradient(256, 200, 40, 256, 256, 380);
  grd.addColorStop(0, '#2b2d33'); grd.addColorStop(0.55, '#141518'); grd.addColorStop(1, '#060607');
  bg.fillStyle = grd; bg.fillRect(0, 0, 512, 512);
  const bgT = new THREE.CanvasTexture(bgC); bgT.colorSpace = THREE.SRGBColorSpace;
  scene.background = bgT;

  const camera = new THREE.PerspectiveCamera(34, container.clientWidth / container.clientHeight, 0.1, 120);
  camera.position.set(...cameraPos);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.set(...target);
  controls.enableDamping = true; controls.dampingFactor = 0.06;
  controls.minDistance = 4; controls.maxDistance = 22;
  controls.maxPolarAngle = 1.52;
  controls.autoRotate = autoRotate; controls.autoRotateSpeed = 0.9;
  let resumeT = null;
  controls.addEventListener('start', () => { controls.autoRotate = false; clearTimeout(resumeT); });
  controls.addEventListener('end', () => {
    clearTimeout(resumeT);
    resumeT = setTimeout(() => { if (autoRotate) controls.autoRotate = true; }, 2500);
  });

  const pmrem = new THREE.PMREMGenerator(renderer);
  // PMREM RoomEnvironment convolution is the single biggest synchronous GPU
  // cost on this page — skipped under software GL (see isSoftwareGL).
  // Metals render flatter without an env map, but the page stays alive.
  if (!softwareGL) scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  pmrem.dispose();

  const key = new THREE.DirectionalLight(0xffffff, 3.0);
  key.position.set(5, 8, 5); key.castShadow = true;
  const shadowRes = softwareGL ? 1024 : 2048;
  key.shadow.mapSize.set(shadowRes, shadowRes);
  key.shadow.camera.left = -7; key.shadow.camera.right = 7;
  key.shadow.camera.top = 7; key.shadow.camera.bottom = -7;
  key.shadow.camera.near = 1; key.shadow.camera.far = 30;
  key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0xffffff, 0.7); rim.position.set(-6, 5, -7); scene.add(rim);
  scene.add(new THREE.HemisphereLight(0x8a93a8, 0x050505, 0.55));

  const floor = new THREE.Mesh(
    new THREE.CircleGeometry(30, 64),
    new THREE.MeshStandardMaterial({ color: 0x0c0c0e, roughness: 0.42, metalness: 0.15, envMapIntensity: 0.5 })
  );
  floor.rotation.x = -Math.PI / 2;
  floor.receiveShadow = true;
  scene.add(floor);

  function start() {
    renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });
  }
  function onResize() {
    const wpx = container.clientWidth || window.innerWidth;
    const hpx = container.clientHeight || window.innerHeight;
    camera.aspect = wpx / hpx; camera.updateProjectionMatrix();
    renderer.setSize(wpx, hpx);
  }
  window.addEventListener('resize', onResize);

  return { renderer, scene, camera, controls, start, onResize };
}

/* ---------------- decks + the surface-sampling rule ---------------- */

/**
 * Build one deck group per profile segment (or a single flat deck for a
 * box enclosure). A deck is the sloped mounting plane of a top segment:
 * {group, z0, z1, zc, yc, pitch}.
 */
export function buildDecks(parent, spec) {
  const { w, d, h } = spec.dims;
  const decks = [];
  const enc = spec.enclosure || {};
  if (enc.type === 'box' || !enc.points) {
    decks.push({ group: null, z0: -d / 2, z1: d / 2, zc: 0, yc: h, pitch: 0 });
  } else {
    const pts = enc.points;
    for (let i = 0; i < pts.length - 1; i++) {
      const [z0, y0] = pts[i], [z1, y1] = pts[i + 1];
      const deck = new THREE.Group();
      const zc = (z0 + z1) / 2, yc = (y0 + y1) / 2;
      const pitch = Math.atan2(y0 - y1, z1 - z0);
      deck.position.set(0, yc, zc);
      deck.rotation.x = pitch;
      parent.add(deck);
      decks.push({ group: deck, z0, z1, zc, yc, pitch });
    }
  }
  return decks;
}

/**
 * THE PROCESS RULE: parts seat by SAMPLING the enclosure profile at their
 * z-position — never hardcoded y values. A profile spec-edit automatically
 * reseats knobs / switch / LED, because their height is always derived here.
 *
 * Returns {y, pitch, deck} for pedal-space z.
 */
export function surfaceAt(decks, z) {
  const EPS = 1e-6;
  let dk = decks.find((d) => z >= d.z0 - EPS && z <= d.z1 + EPS);
  if (!dk) dk = z < decks[0].z0 ? decks[0] : decks[decks.length - 1];
  return { y: dk.yc - (z - dk.zc) * Math.tan(dk.pitch), pitch: dk.pitch, deck: dk };
}

/* ---------------- the assembler (hero.html and validate.html share this) ---------------- */

/**
 * Assemble a complete pedal from a spec object. Returns
 * {group, spec, decks, anchors, parts, enclosureMesh}.
 *
 * anchors: [{id, kind, x, z, obj}] — x/z are the SPEC positions; obj is the
 * placed part group. Validation derives the placed position from the object
 * graph (pedalSpacePos) and compares it against an INDEPENDENT interpolation
 * of the spec — never against this assembler's own math.
 */
export function assemblePedal(spec) {
  const { w, d, h } = spec.dims;
  const enc = spec.enclosure || {};
  const group = new THREE.Group();
  const anchors = [];
  const parts = []; // everything except enclosure + base plate (toggleable for silhouette checks)

  const material = enc.color ? powderCoat(enc.color) : FIN.green;
  const enclosureMesh = enc.type === 'box' || !enc.points
    ? boxEnclosure({ w, d, h, edgeRadius: enc.edgeRadius ?? 0.06, material })
    : profileEnclosure({
        w, d, points: enc.points,
        bevel: enc.bevel ?? 0.05, frontLean: enc.frontLean ?? 0, material,
        smooth: enc.smooth ?? true,
      });
  group.add(enclosureMesh);
  group.add(basePlate({ w, d }));

  const decks = buildDecks(group, spec);

  function seat(part, x, z, id, kind) {
    const { y, pitch, deck } = surfaceAt(decks, z);
    if (deck.group) {
      deck.group.add(part);
      // deck-local z chosen so the WORLD z equals the spec z exactly
      part.position.set(x, 0, (z - deck.zc) / Math.cos(pitch));
    } else {
      group.add(part);
      part.position.set(x, y, z);
    }
    anchors.push({ id, kind, x, z, obj: part });
    parts.push(part);
    return part;
  }

  for (let ki = 0; ki < (spec.knobs || []).length; ki++) {
    const k = spec.knobs[ki];
    const part = seat(knob(k.style || 'ts9', k.rot || 0, k.scale || 1), k.x, k.z, k.id || 'knob', 'knob');
    // Recessed knobs (e.g. TS9): sink the skirt into the deck so the knob
    // emerges from the surface instead of perching on top of it.
    const recess = k.recess ?? 0;
    if (recess) part.position.y -= recess;
    // Tick ring (or dot ring for Boss) flat on the deck around the knob
    if (k.tickRing !== false) {
      const trScale = k.tickRingScale || 1;
      const ring = k.style === 'boss'
        ? dotRing({ r: 0.42 * trScale, dots: 11, dotR: 0.035 * trScale })
        : tickRing({ innerR: 0.32 * trScale, outerR: 0.485 * trScale, wedges: 12 });
      const { y, pitch, deck } = surfaceAt(decks, k.z);
      // Stagger Y by knob index (0.001" steps) so overlapping tick rings
      // don't z-fight — later knobs render on top. Invisible to the eye.
      const ringY = 0.012 + ki * 0.001;
      ring.position.y = ringY;
      if (deck.group) {
        deck.group.add(ring);
        ring.position.set(k.x, ringY, (k.z - deck.zc) / Math.cos(pitch));
      } else {
        group.add(ring);
        ring.position.set(k.x, y + ringY, k.z);
      }
      parts.push(ring);
    }
  }
  if (spec.led) seat(led(), spec.led.x, spec.led.z, 'led', 'led');
  if (spec.footswitch) {
    const fs = spec.footswitch;
    // Get the deck pitch so the treadle can cancel it (stay horizontal)
    const { pitch: fsPitch } = surfaceAt(decks, fs.z);
    seat(
      footswitch({ w: fs.w ?? 2.046, d: fs.d ?? 1.382, style: fs.style || 'plate',
                   frameColor: fs.frameColor || enc.color || null,
                   plateW: fs.plateW, plateD: fs.plateD,
                   padW: fs.padW, padD: fs.padD, padCz: fs.padCz != null ? fs.padCz - fs.z : null,
                   deckPitch: fsPitch }),
      fs.x, fs.z, 'footswitch', 'footswitch'
    );
  }
  for (const j of spec.jacks || []) {
    const part = jack();
    // Position jack so washer sits flush on the wall surface.
    // Wall at x=±w/2. Washer center at +0.018 relative, so origin at w/2 - 0.018.
    const x = (j.side === 'left' ? -1 : 1) * (w / 2 - 0.018);
    if (j.side === 'left') part.rotation.y = Math.PI;
    // y: use explicit spec value when measured; otherwise fall back to the
    // legacy surface-offset (TS9-derived, 0.706" below deck surface).
    let y;
    if (j.y != null) {
      y = j.y;
    } else {
      const { y: surfY } = surfaceAt(decks, j.z);
      y = surfY - 0.706;
    }
    part.position.set(x, y, j.z);
    group.add(part); parts.push(part);
    anchors.push({ id: j.id || `jack-${j.side}`, kind: 'jack', x, z: j.z, obj: part });
  }
  if (spec.powerJack) {
    const part = powerJack();
    const z = -(d / 2 - 0.02);
    // y: use explicit spec value when measured; otherwise derive from surfaceAt
    // (legacy 0.474" offset below top surface at back wall).
    let y;
    if (spec.powerJack.y != null) {
      y = spec.powerJack.y;
    } else {
      const { y: surfY } = surfaceAt(decks, z);
      y = surfY - 0.474;
    }
    part.position.set(spec.powerJack.x, y, z);
    group.add(part); parts.push(part);
    anchors.push({ id: 'power', kind: 'powerJack', x: spec.powerJack.x, z, obj: part });
  }
  if (spec.ibanezPlate) {
    const ip = spec.ibanezPlate;
    seat(
      ibanezPlate({ w: ip.w ?? 2.145, d: ip.d ?? 0.733, border: ip.border ?? 0.06 }),
      ip.x ?? 0, ip.z ?? 0.345, 'ibanez-plate', 'plate'
    );
  }
  if (spec.thumbscrew) {
    // Battery-compartment thumb screw on the front (toe) face. Black knurled knob.
    const ts = spec.thumbscrew;
    const screw = new THREE.Group();
    const r = ts.r ?? 0.20, h = 0.16;
    const knob = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, 24), FIN.blackPlastic));
    knob.rotation.x = Math.PI / 2;
    // Knurling: small boxes around the rim, subtle
    for (let i = 0; i < 16; i++) {
      const k = new THREE.Mesh(new THREE.BoxGeometry(0.025, 0.025, h + 0.01), FIN.blackPlastic);
      const a = (i / 16) * Math.PI * 2;
      k.position.set(Math.cos(a) * r, Math.sin(a) * r, 0);
      screw.add(k);
    }
    screw.add(knob);
    screw.position.set(ts.x, ts.y, ts.z);
    group.add(screw); parts.push(screw);
    anchors.push({ id: 'thumbscrew', kind: 'thumbscrew', x: ts.x, z: ts.z, obj: screw });
  }
  // Knob labels (DRIVE/TONE/LEVEL) — flat text on deck; face:"back" labels go on rear wall
  for (const lb of spec.labels || []) {
    const part = textLabel({ text: lb.text, w: lb.w ?? 0.3, h: lb.h ?? 0.12, spaced: lb.spaced ?? true,
                             arrow: lb.arrow ?? null, script: lb.script ?? false, bold: lb.bold ?? false,
                             color: lb.color ?? '#1a1a1a', bg: lb.bg ?? null });
    if (lb.face === 'back') {
      // Rear wall: the textLabel mesh is pre-rotated -90° x for deck use;
      // reset it to face -z (out the back).
      part.children[0].rotation.set(0, Math.PI, 0);
      group.add(part);
      const backZ = -(spec.dims?.d ?? 5.079) / 2 - 0.005;
      part.position.set(lb.x ?? 0, lb.y ?? 0.75, backZ);
    } else {
      const { y, pitch, deck } = surfaceAt(decks, lb.z);
      if (deck.group) {
        deck.group.add(part);
        part.position.set(lb.x, 0.012, (lb.z - deck.zc) / Math.cos(pitch));
      } else {
        group.add(part);
        part.position.set(lb.x, y + 0.012, lb.z);
      }
    }
    parts.push(part);
    anchors.push({ id: `label-${(lb.id || lb.text).toLowerCase()}`, kind: 'label', x: lb.x, z: lb.z, obj: part });
  }

  return { group, spec, decks, anchors, parts, enclosureMesh };
}

/** Pedal-space position of a part, derived from the OBJECT GRAPH (world matrices). */
export function pedalSpacePos(assembly, obj) {
  assembly.group.updateMatrixWorld(true);
  const v = new THREE.Vector3();
  obj.getWorldPosition(v);
  assembly.group.worldToLocal(v);
  return v;
}

export function setPartsVisible(assembly, visible) {
  for (const p of assembly.parts) p.visible = visible;
}

/**
 * Apply the top-face decal art, split across deck segments so it follows the
 * profile. texture: THREE.Texture (v=1 at the back edge of the pedal).
 */
export function applyDecal(assembly, texture, { anisotropy = 8 } = {}) {
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.anisotropy = anisotropy;
  const { spec, decks } = assembly;
  const D = spec.dims.d, W = spec.dims.w;
  const mat = new THREE.MeshStandardMaterial({
    map: texture, transparent: true, roughness: 0.42, metalness: 0.05,
    envMapIntensity: 0.7, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2,
  });
  for (const dk of decks) {
    const len = dk.z1 - dk.z0;
    const g = new THREE.PlaneGeometry(W, len);
    const uv = g.attributes.uv;
    // texture v: 1 = back edge (image top), 0 = front edge
    const vFront = 0.5 - dk.z1 / D, vBack = 0.5 - dk.z0 / D;
    for (let i = 0; i < uv.count; i++) uv.setY(i, vFront + uv.getY(i) * (vBack - vFront));
    const m = new THREE.Mesh(g, mat);
    m.rotation.x = -Math.PI / 2;
    m.receiveShadow = true;
    if (dk.group) { m.position.y = 0.008; dk.group.add(m); }
    else { m.position.y = spec.dims.h + 0.008; assembly.group.add(m); }
  }
}

/* ---------------- enclosure presets (boxy pedals) ----------------
 * Provenance + uncertainty documented per preset. Dimensions are the bare
 * enclosure (before knobs/switch); individual models vary, so per-model
 * dims override the preset when measured.
 */
export const PRESETS = {
  mxr_standard: {
    w: 2.362, d: 4.370, h: 1.260, // 60 x 111 x 32 mm
    source: 'Perfect Circuit / Session.de / Thomann listings for Phase 90-class pedals (60W x 111D x 32H mm). Some retailers list ~55mm height — that includes knobs; 32mm is the bare enclosure.',
    confidence: 'high',
  },
  ehx_nano: {
    w: 2.756, d: 4.528, h: 2.126, // 70 x 115 x 54 mm
    source: 'Nano Big Muff / Nano 360 listings (70W x 115D x 54H mm, 2.75 x 4.5 x 2.1 in). Nano Pulsar listed at 114 x 70 x 53 mm.',
    confidence: 'medium',
    note: 'Individual Nano models vary by several mm — override per model when measured.',
  },
  ehx_xo: {
    w: 4.016, d: 4.764, h: 2.25, // 102 x 121 x 57 mm (Micro POG die-cast chassis, ehx.com: 4.75 x 4 x 2.25 in)
    source: 'EHX Micro POG manufacturer spec (4.75 x 4 x 2.25 in). "XO" is not one universal enclosure — treat as a starting point, not gospel.',
    confidence: 'medium',
  },
  boss_compact: {
    w: 2.874, d: 5.079, h: 2.323, // 73 x 129 x 59 mm
    source: 'DS-1 listings across retailers (73W x 129D x 59H mm). Well corroborated.',
    confidence: 'high',
  },
};
