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
    color: 0xf4f4f6, roughness: 0.30, metalness: 1.0, envMapIntensity: 1.35,
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
 * internally so the outer surface matches the points.
 * frontLean: inches the front-top edge leans forward (slightly sloped front
 * face, e.g. 0.06 on the TS9). Larger `bevel` softens all corners.
 * Shape +x (tall end) maps to world -z (back) after rotation.y.
 */
export function profileEnclosure({ w, d, points, bevel = 0.05, frontLean = 0, material = FIN.green } = {}) {
  const b = bevel;
  const X = (z) => -z; // shape-x from board-z
  const n = points.length;
  const s = new THREE.Shape();
  s.moveTo(X(points[n - 1][0]) + b, b);
  s.lineTo(X(points[0][0]) - b, b);
  for (let i = 0; i < n; i++) {
    const [z, y] = points[i];
    let x = X(z);
    if (i === 0) x -= b;
    else if (i === n - 1) x += b - frontLean; // front face leans slightly forward
    s.lineTo(x, y - b);
  }
  s.closePath();
  const geo = new THREE.ExtrudeGeometry(s, {
    depth: w - 2 * b, bevelEnabled: true,
    bevelThickness: b, bevelSize: b, bevelSegments: 4, steps: 1,
  });
  geo.translate(0, 0, -(w - 2 * b) / 2);
  const g = new THREE.Group();
  const body = shadowed(new THREE.Mesh(geo, material));
  body.rotation.y = Math.PI / 2;
  g.add(body);
  g.userData.dims = { w, d, h: Math.max(...points.map((p) => p[1])) };
  return g;
}

/** Black base plate, slightly inset. */
export function basePlate({ w, d, h = 0.09 } = {}) {
  const m = shadowed(new THREE.Mesh(new THREE.BoxGeometry(w - 0.12, h, d - 0.12), FIN.blackPlastic));
  m.position.y = h / 2;
  const g = new THREE.Group(); g.add(m); return g;
}

/* ---------------- parts ---------------- */

/**
 * Control knob. Styles:
 *  - 'ts9': ribbed skirt + silver cap + pointer (Ibanez TS9)
 *  - 'mxr': Davies-style fluted black knob + pointer (MXR Phase 90 etc.)
 * pointerRot: rotation of the pointer, radians.
 * Origin at the knob base (sits on the deck at y=0).
 */
export function knob(style = 'ts9', pointerRot = 0) {
  const k = new THREE.Group();
  if (style === 'mxr') {
    const body = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.31, 0.42, 32), FIN.knobRib));
    body.position.y = 0.21;
    const top = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.27, 0.03, 32), FIN.blackPlastic);
    top.position.y = 0.425; top.castShadow = true;
    const pointer = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.014, 0.20), FIN.pointer);
    pointer.position.set(0, 0.44, -0.055);
    const pg = new THREE.Group(); pg.add(pointer); pg.rotation.y = pointerRot;
    k.add(body, top, pg);
  } else { // 'ts9'
    const skirt = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.295, 0.33, 0.40, 48), FIN.knobRib));
    skirt.position.y = 0.20;
    const cap = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.05, 48), FIN.silverCap));
    cap.position.y = 0.425;
    const pointer = new THREE.Mesh(new THREE.BoxGeometry(0.035, 0.014, 0.19), FIN.pointer);
    pointer.position.set(0, 0.452, -0.055);
    const pg = new THREE.Group(); pg.add(pointer); pg.rotation.y = pointerRot;
    k.add(skirt, cap, pg);
  }
  k.userData.knobStyle = style;
  return k;
}

/**
 * Footswitch. Styles:
 *  - 'plate': TS9-style rectangular chrome treadle plate + black bezel
 *  - 'round': MXR-style round chrome button + washer
 * {w, d} = plate size in inches (ignored for 'round'). Origin at deck (y=0).
 */
export function footswitch({ w = 2.046, d = 1.382, style = 'plate' } = {}) {
  const g = new THREE.Group();
  if (style === 'round') {
    const washer = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.30, 0.30, 0.04, 32), FIN.chrome));
    washer.position.y = 0.02;
    const btn = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.24, 0.22, 32), FIN.chrome));
    btn.position.y = 0.14;
    g.add(washer, btn);
  } else {
    const bezel = shadowed(new THREE.Mesh(new RoundedBoxGeometry(w + 0.26, 0.12, d + 0.26, 4, 0.06), FIN.blackPlastic));
    bezel.position.y = 0.05;
    const plate = shadowed(new THREE.Mesh(new RoundedBoxGeometry(w, 0.16, d, 4, 0.05), FIN.plateRib));
    plate.position.y = 0.13;
    g.add(bezel, plate);
  }
  g.userData.switchStyle = style;
  return g;
}

/** LED with chrome bezel + emissive dome + glow light. Origin at deck (y=0). */
export function led() {
  const g = new THREE.Group();
  const bezel = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.085, 0.098, 0.06, 32), FIN.chrome));
  bezel.position.y = 0.03;
  const dome = new THREE.Mesh(new THREE.SphereGeometry(0.062, 24, 16, 0, Math.PI * 2, 0, Math.PI / 2), FIN.led);
  dome.position.y = 0.055;
  const glow = new THREE.PointLight(0xff2a18, 0.9, 2.6, 2);
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
  const washerGeo = new THREE.CylinderGeometry(0.31, 0.31, 0.035, 32);
  washerGeo.rotateZ(Math.PI / 2);
  const washer = shadowed(new THREE.Mesh(washerGeo, FIN.jackChrome));
  washer.position.x = 0.018;
  const nutGeo = new THREE.CylinderGeometry(0.55 / Math.sqrt(3), 0.55 / Math.sqrt(3), 0.11, 6);
  nutGeo.rotateZ(Math.PI / 2);
  nutGeo.rotateX(Math.PI / 6); // flat faces up/down
  const nut = shadowed(new THREE.Mesh(nutGeo, FIN.jackChrome));
  nut.position.x = 0.035 + 0.055;
  const boreGeo = new THREE.CylinderGeometry(0.125, 0.125, 0.17, 24);
  boreGeo.rotateZ(Math.PI / 2);
  const bore = new THREE.Mesh(boreGeo,
    new THREE.MeshStandardMaterial({ color: 0x060606, roughness: 0.9, metalness: 0.2 }));
  bore.position.x = 0.055;
  const ringGeo = new THREE.CylinderGeometry(0.062, 0.062, 0.02, 16);
  ringGeo.rotateZ(Math.PI / 2);
  const contact = new THREE.Mesh(ringGeo, FIN.darkMetal);
  contact.position.x = 0.015;
  g.add(washer, nut, bore, contact);
  return g;
}

/** 9V barrel power jack on the back wall (faces -z). Origin at the wall plane. */
export function powerJack() {
  const g = new THREE.Group();
  const housing = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.088, 0.088, 0.09, 24), FIN.blackPlastic));
  housing.rotation.x = Math.PI / 2;
  const pin = new THREE.Mesh(new THREE.CylinderGeometry(0.028, 0.028, 0.10, 12), FIN.darkMetal);
  pin.rotation.x = Math.PI / 2;
  g.add(housing, pin);
  return g;
}

/* ---------------- studio scene (hero presentation) ---------------- */

/**
 * The shared studio: gradient backdrop, soft floor, 3-point-ish lighting,
 * environment reflections, orbit controls with gentle auto-rotate.
 */
export function studioScene(container, {
  cameraPos = [6.4, 4.8, 8.8], target = [0, 1.25, 0],
  autoRotate = true, exposure = 1.12,
} = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(container.clientWidth || window.innerWidth, container.clientHeight || window.innerHeight);
  renderer.shadowMap.enabled = true;
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
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  pmrem.dispose();

  const key = new THREE.DirectionalLight(0xffffff, 3.0);
  key.position.set(5, 8, 5); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.camera.left = -7; key.shadow.camera.right = 7;
  key.shadow.camera.top = 7; key.shadow.camera.bottom = -7;
  key.shadow.camera.near = 1; key.shadow.camera.far = 30;
  key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02;
  scene.add(key);
  const rim = new THREE.DirectionalLight(0x9db8ff, 2.0); rim.position.set(-6, 5, -7); scene.add(rim);
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

  for (const k of spec.knobs || []) {
    seat(knob(k.style || 'ts9', k.rot || 0), k.x, k.z, k.id || 'knob', 'knob');
  }
  if (spec.led) seat(led(), spec.led.x, spec.led.z, 'led', 'led');
  if (spec.footswitch) {
    const fs = spec.footswitch;
    seat(
      footswitch({ w: fs.w ?? 2.046, d: fs.d ?? 1.382, style: fs.style || 'plate' }),
      fs.x, fs.z, 'footswitch', 'footswitch'
    );
  }
  for (const j of spec.jacks || []) {
    const part = jack();
    const x = (j.side === 'left' ? -1 : 1) * (w / 2 - 0.06);
    if (j.side === 'left') part.rotation.y = Math.PI;
    part.position.set(x, j.y, j.z);
    group.add(part); parts.push(part);
    anchors.push({ id: j.id || `jack-${j.side}`, kind: 'jack', x, z: j.z, obj: part });
  }
  if (spec.powerJack) {
    const part = powerJack();
    const z = -(d / 2 - 0.02);
    part.position.set(spec.powerJack.x, spec.powerJack.y, z);
    group.add(part); parts.push(part);
    anchors.push({ id: 'power', kind: 'powerJack', x: spec.powerJack.x, z, obj: part });
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
