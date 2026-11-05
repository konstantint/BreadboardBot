import * as THREE from 'three';
    import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
    import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
    import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

    // =========================================================================
    // 1. SCENE, RENDERER & LIGHTING (1 Three.js unit = 1 millimeter)
    // =========================================================================
    const canvas = document.getElementById('viewport');
    const renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      powerPreference: 'high-performance'
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 0.98;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFShadowMap;

    const scene = new THREE.Scene();
    const bgHex = 0xece8df;
    scene.background = new THREE.Color(bgHex);
    scene.fog = new THREE.Fog(bgHex, 950, 2400);

    const pmrem = new THREE.PMREMGenerator(renderer);
    const envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
    scene.environment = envTex;
    scene.environmentIntensity = 0.65;

    const camera = new THREE.PerspectiveCamera(
      40,
      window.innerWidth / window.innerHeight,
      2,
      4000
    );
    camera.position.set(145, 125, 195);

    const controls = new OrbitControls(camera, canvas);
    controls.enableDamping = true;
    controls.dampingFactor = 0.07;
    controls.minDistance = 55;
    controls.maxDistance = 1100;
    controls.maxPolarAngle = Math.PI * 0.488;
    controls.target.set(0, 26, 10);

    const hemiLight = new THREE.HemisphereLight(0xfffcf5, 0xd8cfc0, 0.55);
    scene.add(hemiLight);

    const keyLight = new THREE.DirectionalLight(0xfff9ee, 1.55);
    keyLight.position.set(220, 420, 260);
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.set(2048, 2048);
    keyLight.shadow.camera.near = 80;
    keyLight.shadow.camera.far = 1200;
    const shadowExtent = 460;
    keyLight.shadow.camera.left = -shadowExtent;
    keyLight.shadow.camera.right = shadowExtent;
    keyLight.shadow.camera.top = shadowExtent;
    keyLight.shadow.camera.bottom = -shadowExtent;
    keyLight.shadow.bias = -0.0004;
    keyLight.shadow.normalBias = 0.25;
    scene.add(keyLight);

    const rimLight = new THREE.DirectionalLight(0xeef4ff, 0.45);
    rimLight.position.set(-240, 190, -210);
    scene.add(rimLight);

    // =========================================================================
    // 2. PROCEDURAL TEXTURES (XIAO SHIELD, FS90R STICKER, HW-006 PCB, TABLETOP)
    // =========================================================================
    function makeXiaoShieldTexture() {
      const c = document.createElement('canvas');
      c.width = 256;
      c.height = 256;
      const ctx = c.getContext('2d');

      // Crisp white top label with subtle silver shield rim (matching 5c5ksqrg1522o.png)
      ctx.fillStyle = '#c8cdd6';
      ctx.fillRect(0, 0, 256, 256);
      ctx.fillStyle = '#f6f7f9';
      ctx.fillRect(8, 8, 240, 240);

      // Rotate text to match XIAO mounted with USB-C facing +X (viewer's right):
      ctx.save();
      ctx.translate(128, 128);
      ctx.rotate(Math.PI / 2);
      ctx.textAlign = 'center';
      ctx.fillStyle = '#182032';
      ctx.font = 'bold 31px sans-serif';
      ctx.fillText('seeed studio', 0, -52);
      ctx.fillStyle = '#333b4d';
      ctx.font = '500 18px sans-serif';
      ctx.fillText('Model: XIAO-RP2040', 0, -20);
      ctx.fillStyle = '#182032';
      ctx.font = 'bold 58px sans-serif';
      ctx.fillText('FC  CE', 0, 56);
      ctx.restore();

      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.anisotropy = 8;
      return tex;
    }

    function makeXiaoTopOverlayTexture() {
      // 20.96 mm (X: 512px) × 17.78 mm (Y: 434px) top PCB overlay with 2.0mm rounded corners,
      // gold castellated stadium pads right at the ±Y outer edges, and crisp 'R', 'B', 'P', 'U' silkscreen
      const W = 512;
      const H = 434;
      const pxPerMmX = W / 20.96;
      const pxPerMmY = H / 17.78;
      const c = document.createElement('canvas');
      c.width = W;
      c.height = H;
      const ctx = c.getContext('2d');

      const rPx = 2.0 * pxPerMmX;
      ctx.beginPath();
      ctx.roundRect(0, 0, W, H, rPx);
      ctx.clip();

      // Matte black solder-mask FR4
      ctx.fillStyle = '#14161a';
      ctx.fillRect(0, 0, W, H);

      // White silkscreen outline around central shield keepout
      ctx.strokeStyle = 'rgba(236, 240, 246, 0.7)';
      ctx.lineWidth = 2.5;
      const shX = (10.48 - 1.55 - 5.3) * pxPerMmX;
      const shY = (8.89 - 5.3) * pxPerMmY;
      ctx.strokeRect(shX, shY, 10.6 * pxPerMmX, 10.6 * pxPerMmY);

      // 14 gold stadium/pill-shaped castellated edge pads (7 along top edge y=0, 7 along bottom edge y=H)
      ctx.fillStyle = '#d8ae48';
      const padW = 1.82 * pxPerMmX;
      const padLenY = 2.58 * pxPerMmY; // extends from outer edge (0 / H) inward 2.58 mm (pin center is at 1.27 mm!)
      for (let i = -3; i <= 3; i++) {
        const cx = (10.48 + i * 2.54) * pxPerMmX;
        // Top row (row 3, +Y in 3D = y=0 in canvas)
        ctx.beginPath();
        ctx.roundRect(cx - padW * 0.5, -6, padW, padLenY + 6, padW * 0.48);
        ctx.fill();
        // Bottom row (row 7, -Y in 3D = y=H in canvas)
        ctx.beginPath();
        ctx.roundRect(cx - padW * 0.5, H - padLenY, padW, padLenY + 6, padW * 0.48);
        ctx.fill();
      }

      // Crisp white silkscreen markings ('R' & 'B' near -X corners, 'P' & 'U' LED labels near +X USB-C)
      ctx.fillStyle = '#eef2f7';
      ctx.font = 'bold 28px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      // Rotated 90 deg CW to match board orientation in 5c5ksqrg1522o.png when USB-C faces +X
      const drawRotText = (txt, mmX, mmY, fontStr) => {
        ctx.save();
        ctx.font = fontStr;
        ctx.translate((10.48 + mmX) * pxPerMmX, (8.89 - mmY) * pxPerMmY);
        ctx.rotate(Math.PI / 2);
        ctx.fillText(txt, 0, 0);
        ctx.restore();
      };
      drawRotText('R', -8.95, 6.25, 'bold 26px sans-serif');
      drawRotText('B', -8.95, -6.25, 'bold 26px sans-serif');
      drawRotText('P', 5.05, -5.15, 'bold 20px sans-serif');
      drawRotText('U', 5.05, -6.55, 'bold 20px sans-serif');

      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.anisotropy = 8;
      return tex;
    }

    function makeLineSensorTexture(pcbW = 10.2, pcbLen = 31.5, chamfer = 2.75, holeZOff = 16.5, holeR = 1.55) {
      const c = document.createElement('canvas');
      c.width = 256;
      c.height = 768;
      const ctx = c.getContext('2d');
      ctx.clearRect(0, 0, c.width, c.height);

      const hw = pcbW * 0.5;
      ctx.save();
      // Work directly in 1:1 millimeter coordinates: x in [-hw..+hw], z in [0..pcbLen] (header -> front tip)
      ctx.scale(c.width / pcbW, c.height / pcbLen);
      ctx.translate(hw, 0);

      // Clip to exact HW-006 v1.3 cut-corner polygon (square rear at z=0, 45° chamfered front nose at z=pcbLen)
      ctx.beginPath();
      ctx.moveTo(-hw, 0);
      ctx.lineTo(hw, 0);
      ctx.lineTo(hw, pcbLen - chamfer);
      ctx.lineTo(hw - chamfer, pcbLen);
      ctx.lineTo(-hw + chamfer, pcbLen);
      ctx.lineTo(-hw, pcbLen - chamfer);
      ctx.closePath();
      ctx.clip();

      // Glossy dark black solder-mask FR4
      ctx.fillStyle = '#15171a';
      ctx.fillRect(-hw, 0, pcbW, pcbLen);

      // Subtle copper traces under black solder mask
      ctx.strokeStyle = '#20242a';
      ctx.lineWidth = 0.24;
      for (const tx of [-2.2, 0, 2.2]) {
        ctx.beginPath();
        ctx.moveTo(tx, 1.8);
        ctx.lineTo(tx, pcbLen - 3.2);
        ctx.stroke();
      }

      // Crisp white silkscreen outline around 3-pin header footprint & along front chamfered edges (per 6509g25e8u0ho.png)
      ctx.strokeStyle = 'rgba(232, 236, 242, 0.85)';
      ctx.lineWidth = 0.16;
      ctx.strokeRect(-4.05, 0.35, 8.1, 2.55);

      ctx.beginPath();
      ctx.moveTo(hw - 0.22, pcbLen - chamfer - 0.3);
      ctx.lineTo(hw - 0.22, pcbLen - chamfer);
      ctx.lineTo(hw - chamfer, pcbLen - 0.22);
      ctx.lineTo(-hw + chamfer, pcbLen - 0.22);
      ctx.lineTo(-hw + 0.22, pcbLen - chamfer);
      ctx.lineTo(-hw + 0.22, pcbLen - chamfer - 0.3);
      ctx.stroke();

      // White silkscreen pin labels near breadboard header end (-X to +X: GND, VCC, OUT)
      ctx.fillStyle = '#edf1f7';
      ctx.font = 'bold 1.35px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      for (const [lx, label] of [[-2.54, 'GND'], [0, 'VCC'], [2.54, 'OUT']]) {
        ctx.save();
        ctx.translate(lx, 5.15);
        ctx.rotate(Math.PI / 2);
        ctx.fillText(label, 0, 0);
        ctx.restore();
      }

      // Side silkscreen: 'HW-006 V1.3' along +X edge & 'Tracker Sensor' along -X edge
      ctx.font = 'bold 1.18px sans-serif';
      ctx.save();
      ctx.translate(3.85, 16.0);
      ctx.rotate(Math.PI / 2);
      ctx.fillText('HW-006 V1.3', 0, 0);
      ctx.restore();

      ctx.font = '600 1.14px sans-serif';
      ctx.save();
      ctx.translate(-3.65, 19.2);
      ctx.rotate(Math.PI / 2);
      ctx.fillText('Tracker   Sensor', 0, 0);
      ctx.restore();

      // Silver-tinned M3 mounting ring + diagonal silkscreen tick mark
      ctx.strokeStyle = 'rgba(232, 236, 242, 0.85)';
      ctx.lineWidth = 0.18;
      ctx.beginPath();
      ctx.moveTo(1.75, holeZOff - 2.45);
      ctx.lineTo(2.55, holeZOff - 1.65);
      ctx.stroke();

      ctx.fillStyle = '#d4dbe4';
      ctx.beginPath();
      ctx.arc(0, holeZOff, holeR + 0.72, 0, Math.PI * 2);
      ctx.fill();

      // Tinned annular rings under the 4 TCRT5000 through-hole leads near front tip
      const tcrtZOff = pcbLen - 5.6;
      for (const lx of [-1.35, 1.35]) {
        for (const lz of [-2.45, 2.45]) {
          ctx.beginPath();
          ctx.arc(lx, tcrtZOff + lz, 0.72, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      ctx.restore();

      // Punch out the M3 through-hole so the overlay plane is genuinely open over the 3D hole
      ctx.save();
      ctx.globalCompositeOperation = 'destination-out';
      ctx.scale(c.width / pcbW, c.height / pcbLen);
      ctx.translate(hw, 0);
      ctx.beginPath();
      ctx.arc(0, holeZOff, holeR, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();

      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.anisotropy = 8;
      return tex;
    }

    function makeServoLabelTexture() {
      const c = document.createElement('canvas');
      c.width = 256;
      c.height = 128;
      const ctx = c.getContext('2d');
      ctx.fillStyle = '#181a1f';
      ctx.fillRect(0, 0, 256, 128);
      ctx.strokeStyle = '#d4d8df';
      ctx.lineWidth = 6;
      ctx.strokeRect(6, 6, 244, 116);
      ctx.fillStyle = '#e11d48';
      ctx.font = 'italic bold 30px sans-serif';
      ctx.fillText('FITEC', 18, 42);
      ctx.fillStyle = '#f1f5f9';
      ctx.font = '600 20px sans-serif';
      ctx.fillText('Continuous servo', 18, 74);
      ctx.font = 'bold 26px monospace';
      ctx.fillText('FS90R', 18, 106);

      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }

    function makeWorkbenchTexture() {
      const c = document.createElement('canvas');
      c.width = 512;
      c.height = 512;
      const ctx = c.getContext('2d');

      ctx.fillStyle = '#e7e1d5';
      ctx.fillRect(0, 0, 512, 512);

      // Subtle warm birch/melamine tabletop grain + cutting-mat micro-speckle
      let seed = 42;
      const rand = () => {
        seed = (seed * 1664525 + 1013904223) >>> 0;
        return seed / 4294967296;
      };

      for (let y = 0; y < 512; y += 2) {
        const v = Math.floor(227 + (rand() - 0.5) * 7);
        ctx.fillStyle = `rgb(${v + 4}, ${v}, ${v - 8})`;
        ctx.fillRect(0, y, 512, 2);
      }
      for (let i = 0; i < 2500; i++) {
        const x = rand() * 512;
        const y = rand() * 512;
        const a = rand() * 0.035;
        ctx.fillStyle = `rgba(60, 50, 35, ${a.toFixed(3)})`;
        ctx.fillRect(x, y, 2, 2);
      }

      // Subtle 50mm workbench dot matrix so forward motion across the tabletop reads effortlessly
      ctx.fillStyle = 'rgba(75, 68, 56, 0.14)';
      for (let gx = 32; gx < 512; gx += 64) {
        for (let gy = 32; gy < 512; gy += 64) {
          ctx.beginPath();
          ctx.arc(gx, gy, 1.6, 0, Math.PI * 2);
          ctx.fill();
        }
      }

      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(12, 12);
      tex.anisotropy = 8;
      return tex;
    }

    // =========================================================================
    // 3. FLOOR & BLACK ELECTRICAL-TAPE TRACKS
    // =========================================================================
    const floorGeo = new THREE.PlaneGeometry(4200, 4200);
    floorGeo.rotateX(-Math.PI / 2);
    const floorMat = new THREE.MeshStandardMaterial({
      map: makeWorkbenchTexture(),
      roughness: 0.78,
      metalness: 0.0
    });
    const floorMesh = new THREE.Mesh(floorGeo, floorMat);
    floorMesh.receiveShadow = true;
    scene.add(floorMesh);

    const TAPE_WIDTH = 15.0; // mm (standard 15mm black isolation tape fitting cleanly between 20.32mm sensor centers)
    const TAPE_HALF = TAPE_WIDTH * 0.5;
    const TRACK_SAMPLES = 960;

    // Squashed oval ("peanut" / pinched-waist loop: like a figure-8 without crossing)
    const SQUASHED_OVAL_POINTS = (() => {
      const pts = [];
      const N = 64;
      for (let i = 0; i < N; i++) {
        const t = (i / N) * Math.PI * 2;
        const ct = Math.cos(t);
        const st = Math.sin(t);
        const x = 360 * ct;
        const z = -st * (58 + 260 * ct * ct);
        pts.push(new THREE.Vector3(x, 0, z));
      }
      return pts;
    })();

    const tapeMaterial = new THREE.MeshStandardMaterial({
      color: 0x141518,
      roughness: 0.36,
      metalness: 0.05,
      side: THREE.DoubleSide,
      polygonOffset: true,
      polygonOffsetFactor: -2,
      polygonOffsetUnits: -2
    });

    let trackCurve = null;
    let trackPolyline = []; // sampled 2D points {x, z} for fast exact distance query
    let trackMesh = null;

    function buildTrackRibbon(curve, width, segments) {
      const halfW = width * 0.5;
      const tapeY = 0.28;
      const frames = curve.computeFrenetFrames(segments, true);
      const pts = curve.getSpacedPoints(segments);

      const positions = new Float32Array((segments + 1) * 2 * 3);
      const normals = new Float32Array((segments + 1) * 2 * 3);
      const uvs = new Float32Array((segments + 1) * 2 * 2);
      const indices = [];

      const up = new THREE.Vector3(0, 1, 0);
      const side = new THREE.Vector3();

      for (let i = 0; i <= segments; i++) {
        const p = pts[i];
        const tangent = frames.tangents[i];
        side.crossVectors(up, tangent).normalize();

        const vi = i * 6;
        positions[vi + 0] = p.x + side.x * halfW;
        positions[vi + 1] = tapeY;
        positions[vi + 2] = p.z + side.z * halfW;

        positions[vi + 3] = p.x - side.x * halfW;
        positions[vi + 4] = tapeY;
        positions[vi + 5] = p.z - side.z * halfW;

        normals[vi + 0] = 0; normals[vi + 1] = 1; normals[vi + 2] = 0;
        normals[vi + 3] = 0; normals[vi + 4] = 1; normals[vi + 5] = 0;

        const ui = i * 4;
        uvs[ui + 0] = 0; uvs[ui + 1] = i / 20;
        uvs[ui + 2] = 1; uvs[ui + 3] = i / 20;

        if (i < segments) {
          const a = i * 2;
          const b = a + 1;
          const c = a + 2;
          const d = a + 3;
          indices.push(a, b, c, b, d, c);
        }
      }

      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      geo.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
      geo.setAttribute('uv', new THREE.BufferAttribute(uvs, 2));
      geo.setIndex(indices);
      return geo;
    }

    function distanceSqToTrack(x, z) {
      let minD2 = Infinity;
      const n = trackPolyline.length;
      for (let i = 0; i < n; i++) {
        const a = trackPolyline[i];
        const b = trackPolyline[(i + 1) % n];
        const abx = b.x - a.x;
        const abz = b.z - a.z;
        const apx = x - a.x;
        const apz = z - a.z;
        const len2 = abx * abx + abz * abz;
        let t = len2 > 1e-6 ? (apx * abx + apz * abz) / len2 : 0;
        if (t < 0) t = 0;
        else if (t > 1) t = 1;
        const dx = apx - abx * t;
        const dz = apz - abz * t;
        const d2 = dx * dx + dz * dz;
        if (d2 < minD2) minD2 = d2;
      }
      return minD2;
    }

    function isPointOnBlackTape(x, z) {
      return distanceSqToTrack(x, z) <= TAPE_HALF * TAPE_HALF;
    }

    // =========================================================================
    // 4. ASSEMBLED BREADBOARDBOT MODEL (EXACT REAL-WORLD MILLIMETER GEOMETRY)
    // =========================================================================
    // Coordinate conventions in botRoot:
    //   y = 0      : floor plane
    //   +Z         : forward driving direction (line sensors point +Z)
    //   +Y         : up
    //   +X         : robot's LEFT side (= viewer's RIGHT when looking at front face from +Z)
    //   -X         : robot's RIGHT side (= viewer's LEFT when looking at front face from +Z)
    const WHEEL_RADIUS = 32.5;     // Adafruit #4205: 65.0 mm diameter
    const WHEEL_WIDTH = 9.8;       // Adafruit #4205: ~9.8 mm rubber tire width (~14 mm overall incl. inner hub boss)
    const WHEEL_TRACK_HALF = 30.8; // axle tire center at X = ±30.8 mm
    const CHASSIS_TILT = 0.205;    // ~11.7 deg forward slant so front TCRT5000 tips hover ~2.6mm above floor

    const botRoot = new THREE.Group();
    scene.add(botRoot);

    // Explodable sub-assemblies anchored in chassis frame
    const chassisPivot = new THREE.Group();
    chassisPivot.position.set(0, WHEEL_RADIUS, 0);
    chassisPivot.rotation.x = CHASSIS_TILT;
    botRoot.add(chassisPivot);

    const grpBreadboard = new THREE.Group();
    const grpXiao = new THREE.Group();
    const grpWires = new THREE.Group();
    const grpSensors = new THREE.Group();
    const grpServos = new THREE.Group();
    const grpBattery = new THREE.Group();
    chassisPivot.add(grpBreadboard, grpXiao, grpWires, grpSensors, grpServos, grpBattery);

    // Wheels stay aligned to axle in botRoot (so spin around X is pure rolling)
    const grpWheelLeft = new THREE.Group();   // +X side (robot's left)
    const grpWheelRight = new THREE.Group();  // -X side (robot's right)
    grpWheelLeft.position.set(WHEEL_TRACK_HALF, WHEEL_RADIUS, 0);
    grpWheelRight.position.set(-WHEEL_TRACK_HALF, WHEEL_RADIUS, 0);
    botRoot.add(grpWheelLeft, grpWheelRight);

    // Shared materials
    const matWhiteABS = new THREE.MeshStandardMaterial({
      color: 0xf0f1f3,
      roughness: 0.42,
      metalness: 0.02
    });
    const matHoleInterior = new THREE.MeshStandardMaterial({
      color: 0x22252a,
      roughness: 0.85,
      metalness: 0.1
    });
    const matBlackPlastic = new THREE.MeshStandardMaterial({
      color: 0x1b1d21,
      roughness: 0.52,
      metalness: 0.05
    });
    const matGreenHeader = new THREE.MeshStandardMaterial({
      color: 0x4d7c3f,
      roughness: 0.5,
      metalness: 0.05
    });
    const matBrightMetal = new THREE.MeshStandardMaterial({
      color: 0xd8dde6,
      roughness: 0.22,
      metalness: 0.88
    });
    const matChrome = new THREE.MeshStandardMaterial({
      color: 0xf2f5fa,
      roughness: 0.08,
      metalness: 0.96
    });
    const matGoldPin = new THREE.MeshStandardMaterial({
      color: 0xd9ad4a,
      roughness: 0.26,
      metalness: 0.86
    });
    const matServoBlue = new THREE.MeshPhysicalMaterial({
      color: 0x0b4fd6,
      roughness: 0.2,
      metalness: 0.02,
      transmission: 0.42,
      thickness: 4.5,
      ior: 1.49,
      attenuationColor: new THREE.Color(0x0838a8),
      attenuationDistance: 8.0
    });
    const matHotGlue = new THREE.MeshPhysicalMaterial({
      color: 0xe8edf2,
      roughness: 0.35,
      transmission: 0.55,
      thickness: 2.0,
      ior: 1.46
    });

    // Breadboard coordinate frame inside chassisPivot:
    // Servo bodies sit centered near z = 0 (axle), breadboard back face at z = +6.2, front face at z = +14.7
    const BB_WIDTH = 46.6;
    const BB_HEIGHT = 35.0;
    const BB_DEPTH = 8.5;
    const BB_BACK_Z = 6.2;
    const BB_FRONT_Z = BB_BACK_Z + BB_DEPTH; // 14.7 mm
    const BB_CENTER_Y = 0.8;                 // center of breadboard near axle height
    const PITCH = 2.54;

    // Exact SYB-170 hole helper: col = 1..17 (-X viewer's left to +X viewer's right), row = 1..10 (top to bottom)
    function holePos(col, row, zOffset = 0) {
      const x = (col - 9) * PITCH;
      const yRel = row <= 5 ? (6.5 - row) * PITCH : (4.5 - row) * PITCH;
      return new THREE.Vector3(x, BB_CENTER_Y + yRel, BB_FRONT_Z + zOffset);
    }

    // --- 4A. SYB-170 Mini-Breadboard ---
    {
      // Top and bottom halves separated by the central horizontal ravine
      const halfH = 14.9;
      const ravineH = BB_HEIGHT - halfH * 2; // 5.2 mm ravine
      const topHalf = new THREE.Mesh(
        new RoundedBoxGeometry(BB_WIDTH, halfH, BB_DEPTH, 3, 0.7),
        matWhiteABS
      );
      topHalf.position.set(0, BB_CENTER_Y + (ravineH + halfH) * 0.5, BB_BACK_Z + BB_DEPTH * 0.5);
      topHalf.castShadow = true;
      topHalf.receiveShadow = true;
      grpBreadboard.add(topHalf);

      const botHalf = new THREE.Mesh(
        new RoundedBoxGeometry(BB_WIDTH, halfH, BB_DEPTH, 3, 0.7),
        matWhiteABS
      );
      botHalf.position.set(0, BB_CENTER_Y - (ravineH + halfH) * 0.5, BB_BACK_Z + BB_DEPTH * 0.5);
      botHalf.castShadow = true;
      botHalf.receiveShadow = true;
      grpBreadboard.add(botHalf);

      // Base bridge behind the central ravine
      const ravineFloor = new THREE.Mesh(
        new RoundedBoxGeometry(BB_WIDTH, ravineH + 1.4, BB_DEPTH - 1.8, 2, 0.4),
        matWhiteABS
      );
      ravineFloor.position.set(0, BB_CENTER_Y, BB_BACK_Z + (BB_DEPTH - 1.8) * 0.5);
      ravineFloor.castShadow = true;
      ravineFloor.receiveShadow = true;
      grpBreadboard.add(ravineFloor);

      // End walls of central ravine around the two M2 screw bosses
      for (const sx of [-1, 1]) {
        const boss = new THREE.Mesh(
          new THREE.BoxGeometry(8.2, ravineH + 0.4, BB_DEPTH - 0.3),
          matWhiteABS
        );
        boss.position.set(sx * (BB_WIDTH * 0.5 - 4.1), BB_CENTER_Y, BB_BACK_Z + (BB_DEPTH - 0.3) * 0.5);
        grpBreadboard.add(boss);

        // Countersunk recess + M2 bolt head securing the servo on the back
        const recess = new THREE.Mesh(
          new THREE.CylinderGeometry(2.1, 2.1, 1.2, 18),
          matHoleInterior
        );
        recess.rotation.x = Math.PI / 2;
        recess.position.set(sx * 16.5, BB_CENTER_Y, BB_FRONT_Z - 0.45);
        grpBreadboard.add(recess);

        const m2Head = new THREE.Mesh(
          new THREE.CylinderGeometry(1.75, 1.75, 1.3, 18),
          matBrightMetal
        );
        m2Head.rotation.x = Math.PI / 2;
        m2Head.position.set(sx * 16.5, BB_CENTER_Y, BB_FRONT_Z - 0.3);
        grpBreadboard.add(m2Head);

        // Phillips cross slot on M2 screw head
        for (const rotZ of [0, Math.PI / 2]) {
          const slot = new THREE.Mesh(
            new THREE.BoxGeometry(2.1, 0.35, 0.35),
            matHoleInterior
          );
          slot.rotation.z = rotZ;
          slot.position.set(sx * 16.5, BB_CENTER_Y, BB_FRONT_Z + 0.32);
          grpBreadboard.add(slot);
        }
      }

      // Characteristic SYB-170 dovetail tabs on top & right edges
      const topTab = new THREE.Mesh(
        new RoundedBoxGeometry(4.4, 1.3, 3.6, 2, 0.25),
        matWhiteABS
      );
      topTab.position.set(0, BB_CENTER_Y + BB_HEIGHT * 0.5 + 0.55, BB_BACK_Z + 4.2);
      grpBreadboard.add(topTab);

      const sideTab = new THREE.Mesh(
        new RoundedBoxGeometry(1.3, 4.4, 3.6, 2, 0.25),
        matWhiteABS
      );
      sideTab.position.set(BB_WIDTH * 0.5 + 0.55, BB_CENTER_Y, BB_BACK_Z + 4.2);
      grpBreadboard.add(sideTab);

      // 170 square socket holes (InstancedMesh for crisp close-up detail at 1 draw call)
      const socketGeo = new THREE.BoxGeometry(1.18, 1.18, 0.9);
      const socketInst = new THREE.InstancedMesh(socketGeo, matHoleInterior, 170);
      const dummy = new THREE.Object3D();
      let idx = 0;
      for (let col = 1; col <= 17; col++) {
        for (let row = 1; row <= 10; row++) {
          const p = holePos(col, row, -0.32);
          dummy.position.copy(p);
          dummy.updateMatrix();
          socketInst.setMatrixAt(idx++, dummy.matrix);
        }
      }
      socketInst.instanceMatrix.needsUpdate = true;
      grpBreadboard.add(socketInst);

      // Double-sided foam adhesive pad on back of breadboard
      const foamPad = new THREE.Mesh(
        new THREE.BoxGeometry(BB_WIDTH - 1.5, BB_HEIGHT - 1.5, 0.8),
        new THREE.MeshStandardMaterial({ color: 0xd9d6ce, roughness: 0.85 })
      );
      foamPad.position.set(0, BB_CENTER_Y, BB_BACK_Z - 0.4);
      grpBreadboard.add(foamPad);
    }

    // --- 4B. Seeed Studio XIAO RP2040 (Cols 7..13, Rows 3 & 7 — Exact 0.600" / 15.24mm Row Spacing!) ---
    let neoPixelMesh = null;
    {
      // On SYB-170 (3-pitch central ravine), row 3 (+3.5*PITCH) and row 7 (-2.5*PITCH) are separated by
      // 6.0 * 2.54 = 15.24 mm (0.600"), matching XIAO's castellated edge headers to 0.01 mm (5c5ksqrg1522o.png)!
      const xiaoCenterX = holePos(10, 3).x; // centered at col 10 (+2.54 mm), spanning cols 7..13
      const xiaoCenterY = 0.5 * (holePos(10, 3).y + holePos(10, 7).y); // BB_CENTER_Y + 1.27 mm (+2.07 mm)
      const pcbW = 20.96;  // KiCad verified 20.96 mm length along X
      const pcbH = 17.78;  // KiCad verified 17.78 mm width along Y (pins at ±7.62 mm -> 1.27 mm from outer edge!)
      const pcbT = 1.50;
      const cornerR = 2.00; // KiCad verified 2.0 mm corner rounding
      const pcbBackZ = BB_FRONT_Z + 2.55; // rests atop the 2.5mm black pin-header spacers
      const pcbTopZ = pcbBackZ + pcbT;

      // Extruded 2D rounded-rectangle PCB substrate with true 2.0 mm XY corner arcs
      const hw = pcbW * 0.5;
      const hh = pcbH * 0.5;
      const pcbShape = new THREE.Shape();
      pcbShape.moveTo(-hw + cornerR, -hh);
      pcbShape.lineTo(hw - cornerR, -hh);
      pcbShape.absarc(hw - cornerR, -hh + cornerR, cornerR, -Math.PI / 2, 0, false);
      pcbShape.lineTo(hw, hh - cornerR);
      pcbShape.absarc(hw - cornerR, hh - cornerR, cornerR, 0, Math.PI / 2, false);
      pcbShape.lineTo(-hw + cornerR, hh);
      pcbShape.absarc(-hw + cornerR, hh - cornerR, cornerR, Math.PI / 2, Math.PI, false);
      pcbShape.lineTo(-hw, -hh + cornerR);
      pcbShape.absarc(-hw + cornerR, -hh + cornerR, cornerR, Math.PI, Math.PI * 1.5, false);

      const pcbGeo = new THREE.ExtrudeGeometry(pcbShape, {
        depth: pcbT,
        bevelEnabled: true,
        bevelThickness: 0.06,
        bevelSize: 0.06,
        bevelSegments: 2,
        curveSegments: 16
      });
      const xiaoPcb = new THREE.Mesh(
        pcbGeo,
        new THREE.MeshStandardMaterial({ color: 0x14161a, roughness: 0.42, metalness: 0.06 })
      );
      xiaoPcb.position.set(xiaoCenterX, xiaoCenterY, pcbBackZ);
      xiaoPcb.castShadow = true;
      grpXiao.add(xiaoPcb);

      // Crisp top overlay plane carrying gold stadium edge pads + 'R', 'B', 'P', 'U' silkscreen
      const topOverlay = new THREE.Mesh(
        new THREE.PlaneGeometry(pcbW, pcbH),
        new THREE.MeshStandardMaterial({
          map: makeXiaoTopOverlayTexture(),
          alphaTest: 0.5,
          roughness: 0.36,
          metalness: 0.18
        })
      );
      topOverlay.position.set(xiaoCenterX, xiaoCenterY, pcbTopZ + 0.07);
      grpXiao.add(topOverlay);

      // Two 7-pin black header insulators + flush castellated edge plating + domed silver solder fillets (rows 3 & 7)
      for (const row of [3, 7]) {
        const edgeSignY = row === 3 ? 1 : -1;
        const hdrStrip = new THREE.Mesh(
          new THREE.BoxGeometry(7 * PITCH, 2.0, 2.5),
          matBlackPlastic
        );
        const pMid = holePos(10, row, 1.28);
        hdrStrip.position.copy(pMid);
        grpXiao.add(hdrStrip);

        for (let col = 7; col <= 13; col++) {
          const p = holePos(col, row, 0);

          // Square gold header pin entering breadboard socket & protruding slightly through solder dome
          const pin = new THREE.Mesh(
            new THREE.BoxGeometry(0.60, 0.60, 5.20),
            matGoldPin
          );
          pin.position.set(p.x, p.y, BB_FRONT_Z + 2.12);
          grpXiao.add(pin);

          // Flush gold castellated edge plating right along the outer ±Y wall of the PCB (never protruding past ±hh)
          const castellation = new THREE.Mesh(
            new THREE.BoxGeometry(1.18, 0.24, pcbT + 0.06),
            matGoldPin
          );
          castellation.position.set(p.x, xiaoCenterY + edgeSignY * (hh - 0.08), pcbBackZ + pcbT * 0.5);
          grpXiao.add(castellation);

          // Shiny domed silver solder meniscus fillet around each pin near the outer PCB edge (as in 5c5ksqrg1522o.png)
          const solderDome = new THREE.Mesh(
            new THREE.SphereGeometry(0.86, 14, 10, 0, Math.PI * 2, 0, Math.PI * 0.55),
            matChrome
          );
          solderDome.rotation.x = Math.PI / 2;
          solderDome.scale.set(0.90, 0.82, 1.12);
          solderDome.position.set(p.x, p.y - edgeSignY * 0.14, pcbTopZ + 0.06);
          grpXiao.add(solderDome);
        }
      }

      // Metallic Seeed Studio RF Shield Can with crisp white top label
      const shieldMat = [
        matBrightMetal,
        matBrightMetal,
        matBrightMetal,
        matBrightMetal,
        new THREE.MeshStandardMaterial({
          map: makeXiaoShieldTexture(),
          roughness: 0.48,
          metalness: 0.06
        }),
        matBrightMetal
      ];
      const shield = new THREE.Mesh(
        new THREE.BoxGeometry(10.3, 10.2, 1.95),
        shieldMat
      );
      shield.position.set(xiaoCenterX - 1.55, xiaoCenterY, pcbTopZ + 1.02);
      shield.castShadow = true;
      grpXiao.add(shield);

      // USB-C Receptacle on +X (7.50 × 8.94 × 3.26 mm, overhanging +X PCB edge by 1.35 mm per KiCad DXF)
      const usbcGroup = new THREE.Group();
      usbcGroup.position.set(xiaoCenterX + hw + 1.35 - 3.75, xiaoCenterY, pcbTopZ + 1.65);
      const usbcShell = new THREE.Mesh(
        new RoundedBoxGeometry(7.5, 8.94, 3.22, 3, 1.05),
        matBrightMetal
      );
      usbcShell.castShadow = true;
      usbcGroup.add(usbcShell);

      const usbcCavity = new THREE.Mesh(
        new RoundedBoxGeometry(2.0, 7.6, 2.1, 2, 0.6),
        matHoleInterior
      );
      usbcCavity.position.set(2.9, 0, 0);
      usbcGroup.add(usbcCavity);

      const usbcTongue = new THREE.Mesh(
        new THREE.BoxGeometry(3.2, 5.8, 0.6),
        matBlackPlastic
      );
      usbcTongue.position.set(2.2, 0, 0);
      usbcGroup.add(usbcTongue);
      grpXiao.add(usbcGroup);

      // Tiny SMD 'P' (amber power) and 'U' (user) LEDs next to USB-C on -Y side (visible in 5c5ksqrg1522o.png)
      for (const [lyOff, ledCol] of [[-5.15, 0xd97706], [-6.55, 0x3b3f46]]) {
        const tinyLed = new THREE.Mesh(
          new THREE.BoxGeometry(1.15, 0.8, 0.55),
          new THREE.MeshStandardMaterial({ color: ledCol, roughness: 0.35 })
        );
        tinyLed.position.set(xiaoCenterX + 6.35, xiaoCenterY + lyOff, pcbTopZ + 0.32);
        grpXiao.add(tinyLed);
      }

      // RESET ('R' at +Y) and BOOT ('B' at -Y) SMD micro-tactile buttons + white WS2812 NeoPixel on -X edge
      for (const byOff of [3.85, -3.85]) {
        const btnBase = new THREE.Mesh(
          new THREE.BoxGeometry(2.5, 3.2, 0.85),
          matBrightMetal
        );
        btnBase.position.set(xiaoCenterX - 8.65, xiaoCenterY + byOff, pcbTopZ + 0.45);
        grpXiao.add(btnBase);

        const btnCap = new THREE.Mesh(
          new THREE.CylinderGeometry(0.82, 0.82, 0.55, 14),
          matBlackPlastic
        );
        btnCap.rotation.x = Math.PI / 2;
        btnCap.position.set(xiaoCenterX - 8.65, xiaoCenterY + byOff, pcbTopZ + 0.98);
        grpXiao.add(btnCap);
      }

      // White 2.2×2.2mm WS2812 RGB LED package centered between R and B buttons right at -X edge
      const neoPkg = new THREE.Mesh(
        new THREE.BoxGeometry(2.25, 2.25, 0.8),
        matWhiteABS
      );
      neoPkg.position.set(xiaoCenterX - 8.75, xiaoCenterY, pcbTopZ + 0.42);
      grpXiao.add(neoPkg);

      neoPixelMesh = new THREE.Mesh(
        new THREE.CylinderGeometry(0.72, 0.72, 0.28, 16),
        new THREE.MeshStandardMaterial({
          color: 0x22c55e,
          emissive: 0x22c55e,
          emissiveIntensity: 1.4,
          roughness: 0.3
        })
      );
      neoPixelMesh.rotation.x = Math.PI / 2;
      neoPixelMesh.position.set(xiaoCenterX - 8.75, xiaoCenterY, pcbTopZ + 0.85);
      grpXiao.add(neoPixelMesh);
    }

    // --- 4C. Breadboard Solid-Core Jumper Wires + Top Servo Header Jumpers ---
    function addBreadboardJumper(col1, row1, col2, row2, hexColor, archHeight = 1.5, midOffsetY = 0.0, radius = 0.60) {
      const p1 = holePos(col1, row1, 0);
      const p2 = holePos(col2, row2, 0);

      // Bare tinned copper wire legs entering sockets
      for (const p of [p1, p2]) {
        const leg = new THREE.Mesh(
          new THREE.CylinderGeometry(0.30, 0.30, archHeight + 1.5, 8),
          matBrightMetal
        );
        leg.rotation.x = Math.PI / 2;
        leg.position.set(p.x, p.y, BB_FRONT_Z + archHeight * 0.5 - 0.3);
        grpWires.add(leg);
      }

      // Insulated PVC jacket spanning between holes
      const start = new THREE.Vector3(p1.x, p1.y, BB_FRONT_Z + archHeight);
      const end = new THREE.Vector3(p2.x, p2.y, BB_FRONT_Z + archHeight);
      const mid = start.clone().lerp(end, 0.5);
      mid.y += midOffsetY;
      mid.z += 0.25;

      const curve = new THREE.CatmullRomCurve3([start, mid, end]);
      const tubeGeo = new THREE.TubeGeometry(curve, 16, radius, 10, false);
      const tubeMat = new THREE.MeshStandardMaterial({
        color: hexColor,
        roughness: 0.38,
        metalness: 0.04
      });
      const mesh = new THREE.Mesh(tubeGeo, tubeMat);
      mesh.castShadow = true;
      grpWires.add(mesh);
    }

    {
      // Exact breadboard jumpers from reference wiring photo (0fu1htingcm08.png), including under-MCU routing:
      // 1. Under-MCU power & ground jumpers (cols 4..15 across rows 4..6):
      addBreadboardJumper(5, 5, 14, 4, 0xf97316, 1.15);         // Long orange 5V bus under XIAO (col 5 -> col 14)
      addBreadboardJumper(4, 5, 4, 6, 0xeab308, 1.35);         // Short yellow GND ravine bridge (col 4)
      addBreadboardJumper(15, 5, 12, 6, 0x1d63dc, 1.20);       // Diagonal blue servo GND -> XIAO GND (col 15 -> col 12)
      addBreadboardJumper(14, 5, 13, 6, 0xeab308, 1.92);       // Diagonal yellow 5V -> XIAO 5V & left sensor VCC (over blue)

      // 2. Right & left line-sensor jumpers (rows 8..9):
      addBreadboardJumper(6, 8, 7, 8, 0x181a1e, 1.25);         // Tiny 1-pitch black: Right sensor OUT (col 6) -> D7 (col 7)
      addBreadboardJumper(5, 9, 11, 8, 0x181a1e, 1.50);        // Medium black: Right sensor VCC (col 5) -> 3V3 (col 11)
      addBreadboardJumper(4, 9, 12, 8, 0xeab308, 2.05);        // Long yellow: Right sensor GND (col 4) -> XIAO GND (col 12)
      addBreadboardJumper(10, 9, 14, 9, 0x10b981, 1.60);       // Medium green: Left sensor OUT (col 14) -> D10 (col 10)

      // Two hot-glued 3-pin black female servo connectors on the TOP edge of the breadboard:
      // - Right motor (viewer-left, cols 4,5,6): 3 black jumpers -> (4,1), (5,1), (7,1 [D6])
      // - Left motor  (viewer-right, cols 13,14,15): yellow -> (13,2 [D0]), green -> (14,3 [5V]), green -> (15,3 [GND])
      const topConnectors = [
        {
          centerCol: 5,
          wires: [
            { pinCol: 4, targetCol: 4, targetRow: 1, color: 0x181a1e },
            { pinCol: 5, targetCol: 5, targetRow: 1, color: 0x181a1e },
            { pinCol: 6, targetCol: 7, targetRow: 1, color: 0x181a1e }
          ]
        },
        {
          centerCol: 14,
          wires: [
            { pinCol: 13, targetCol: 13, targetRow: 2, color: 0xeab308 },
            { pinCol: 14, targetCol: 14, targetRow: 3, color: 0x10b981 },
            { pinCol: 15, targetCol: 15, targetRow: 3, color: 0x10b981 }
          ]
        }
      ];

      for (const tc of topConnectors) {
        const cx = (tc.centerCol - 9) * PITCH;
        const topEdgeY = BB_CENTER_Y + BB_HEIGHT * 0.5;

        // Milky translucent hot-glue bead underneath connector
        const glue = new THREE.Mesh(
          new THREE.SphereGeometry(3.4, 14, 10),
          matHotGlue
        );
        glue.scale.set(1.35, 0.32, 1.1);
        glue.position.set(cx, topEdgeY + 0.3, BB_BACK_Z + 5.2);
        grpWires.add(glue);

        // Black 3-pin DuPont female servo plug housing
        const housing = new THREE.Mesh(
          new RoundedBoxGeometry(8.0, 2.8, 14.0, 2, 0.3),
          matBlackPlastic
        );
        housing.position.set(cx, topEdgeY + 1.55, BB_BACK_Z + 5.6);
        housing.castShadow = true;
        grpWires.add(housing);

        // 3 jumper bridges curving from front of top connector down into target holes
        for (const wSpec of tc.wires) {
          const startX = (wSpec.pinCol - 9) * PITCH;
          const targetHole = holePos(wSpec.targetCol, wSpec.targetRow, 0);

          const pA = new THREE.Vector3(startX, topEdgeY + 1.45, BB_BACK_Z + 12.2);
          const pB = new THREE.Vector3(
            (startX + targetHole.x) * 0.5,
            topEdgeY + 0.55,
            BB_FRONT_Z + 2.15
          );
          const pC = new THREE.Vector3(targetHole.x, targetHole.y, BB_FRONT_Z + 1.7);
          const pD = new THREE.Vector3(targetHole.x, targetHole.y, BB_FRONT_Z - 0.2);

          const jCurve = new THREE.CatmullRomCurve3([pA, pB, pC]);
          const jMesh = new THREE.Mesh(
            new THREE.TubeGeometry(jCurve, 14, 0.60, 8, false),
            new THREE.MeshStandardMaterial({ color: wSpec.color, roughness: 0.38 })
          );
          jMesh.castShadow = true;
          grpWires.add(jMesh);

          const pinLeg = new THREE.Mesh(
            new THREE.CylinderGeometry(0.30, 0.30, 2.3, 8),
            matBrightMetal
          );
          pinLeg.rotation.x = Math.PI / 2;
          pinLeg.position.copy(pD.lerp(pC, 0.45));
          grpWires.add(pinLeg);
        }
      }

      // Foolproof 3-pin battery header spanning cols 3, 4, 5 at row 3 + black 3-pin female plug
      const batHdrPos = holePos(4, 3, 1.6);
      const greenHdr = new THREE.Mesh(
        new THREE.BoxGeometry(3 * PITCH, 2.5, 3.2),
        matGreenHeader
      );
      greenHdr.position.copy(batHdrPos);
      grpWires.add(greenHdr);

      const batPlug = new THREE.Mesh(
        new RoundedBoxGeometry(3 * PITCH + 0.4, 2.7, 11.5, 2, 0.3),
        matBlackPlastic
      );
      batPlug.position.set(batHdrPos.x, batHdrPos.y, BB_FRONT_Z + 7.2);
      batPlug.castShadow = true;
      grpWires.add(batPlug);
    }

    // --- 4D. Two HW-006 v1.3 IR Line-Tracker Sensors (Row 10, Cols 4..6 & Cols 12..14) ---
    const SENSOR_PCB_W = 10.2;
    const SENSOR_PCB_LEN = 31.5;
    const SENSOR_CHAMFER = 2.75;
    const SENSOR_HOLE_Z_OFF = 16.5;
    const SENSOR_HOLE_R = 1.55;

    const sensorTexture = makeLineSensorTexture(
      SENSOR_PCB_W,
      SENSOR_PCB_LEN,
      SENSOR_CHAMFER,
      SENSOR_HOLE_Z_OFF,
      SENSOR_HOLE_R
    );
    const sensorMatTop = new THREE.MeshStandardMaterial({
      map: sensorTexture,
      alphaTest: 0.5,
      roughness: 0.32,
      metalness: 0.12
    });
    const sensorPcbBodyMat = new THREE.MeshStandardMaterial({
      color: 0x16191d,
      roughness: 0.48,
      metalness: 0.06
    });
    const sensorHoleBarrelMat = new THREE.MeshStandardMaterial({
      color: 0xd4dbe4,
      roughness: 0.25,
      metalness: 0.85,
      side: THREE.DoubleSide
    });

    // Shared extruded cut-corner PCB geometry (square at -Z header end, 45° chamfered corners at +Z sensor tip)
    const sensorPcbGeo = (() => {
      const hw = SENSOR_PCB_W * 0.5;
      const hl = SENSOR_PCB_LEN * 0.5;
      const ch = SENSOR_CHAMFER;
      // After rotation.x = -Math.PI / 2 around pcbCenterZ:
      //   shapeY = +hl -> Z = pcbStartZ (rear header end, square corners)
      //   shapeY = -hl -> Z = pcbStartZ + pcbLen (front nose tip, 45° cut corners)
      const shape = new THREE.Shape();
      shape.moveTo(-hw, hl);
      shape.lineTo(hw, hl);
      shape.lineTo(hw, -hl + ch);
      shape.lineTo(hw - ch, -hl);
      shape.lineTo(-hw + ch, -hl);
      shape.lineTo(-hw, -hl + ch);
      shape.closePath();

      const m3Hole = new THREE.Path();
      m3Hole.absarc(0, hl - SENSOR_HOLE_Z_OFF, SENSOR_HOLE_R, 0, Math.PI * 2, true);
      shape.holes.push(m3Hole);

      return new THREE.ExtrudeGeometry(shape, {
        depth: 1.42,
        bevelEnabled: true,
        bevelThickness: 0.04,
        bevelSize: 0.04,
        bevelSegments: 2,
        curveSegments: 20
      });
    })();

    // World-space optical sample points attached directly to the TCRT5000 lenses!
    const sensorTipRight = new THREE.Object3D(); // Robot's right = viewer's left (col 5, X = -10.16mm)
    const sensorTipLeft = new THREE.Object3D();  // Robot's left  = viewer's right (col 13, X = +10.16mm)
    let sensorLedRightMat = null;
    let sensorLedLeftMat = null;

    function buildLineSensor(centerCol, isLeftSensor) {
      const sGroup = new THREE.Group();
      const rootHole = holePos(centerCol, 10, 0);
      sGroup.position.copy(rootHole);

      // 3 header pins + black plastic collar plugging into row 10 (cols centerCol-1 .. centerCol+1)
      const collar = new THREE.Mesh(
        new THREE.BoxGeometry(3 * PITCH, 2.5, 2.5),
        matBlackPlastic
      );
      collar.position.set(0, 0, 1.3);
      sGroup.add(collar);

      for (const dc of [-1, 0, 1]) {
        const pin = new THREE.Mesh(
          new THREE.BoxGeometry(0.64, 0.64, 7.0),
          matBrightMetal
        );
        pin.position.set(dc * PITCH, 0, 2.4);
        sGroup.add(pin);
      }

      // Main HW-006 v1.3 cut-corner PCB extending forward (+Z): 10.2mm wide x 1.5mm thick x 31.5mm long
      const pcbLen = SENSOR_PCB_LEN;
      const pcbW = SENSOR_PCB_W;
      const pcbStartZ = 4.2;
      const pcbCenterZ = pcbStartZ + pcbLen * 0.5;

      const pcb = new THREE.Mesh(sensorPcbGeo, sensorPcbBodyMat);
      pcb.rotation.x = -Math.PI / 2;
      pcb.position.set(0, -0.71, pcbCenterZ); // spans y = -0.75 .. +0.75
      pcb.castShadow = true;
      pcb.receiveShadow = true;
      sGroup.add(pcb);

      // Clipped top silkscreen & pad overlay aligned 1:1 with the cut-corner PCB
      const pcbTopOverlay = new THREE.Mesh(
        new THREE.PlaneGeometry(pcbW, pcbLen),
        sensorMatTop
      );
      pcbTopOverlay.rotation.x = -Math.PI / 2;
      pcbTopOverlay.position.set(0, 0.76, pcbCenterZ);
      pcbTopOverlay.receiveShadow = true;
      sGroup.add(pcbTopOverlay);

      // Plated open-ended M3 barrel lining the see-through mounting hole
      const mountHoleBarrel = new THREE.Mesh(
        new THREE.CylinderGeometry(SENSOR_HOLE_R, SENSOR_HOLE_R, 1.50, 24, 1, true),
        sensorHoleBarrelMat
      );
      mountHoleBarrel.position.set(0, 0, pcbStartZ + SENSOR_HOLE_Z_OFF);
      sGroup.add(mountHoleBarrel);

      // 74HC14D 14-pin SOIC IC chip mounted on the underside (-Y) of the PCB (per part-linesensor.jpg)
      const icChip = new THREE.Mesh(
        new RoundedBoxGeometry(6.2, 1.2, 4.0, 2, 0.15),
        matBlackPlastic
      );
      icChip.position.set(0, -1.2, pcbStartZ + 9.5);
      sGroup.add(icChip);

      // Tiny SMD passives on underside + reactive Red status LED on top (+Y)
      for (const sx of [-2.6, 2.6]) {
        const smd = new THREE.Mesh(
          new THREE.BoxGeometry(1.6, 0.65, 1.0),
          new THREE.MeshStandardMaterial({ color: 0x2b2d30, roughness: 0.4 })
        );
        smd.position.set(sx, -0.95, pcbStartZ + 21.5);
        sGroup.add(smd);
      }

      const ledMat = new THREE.MeshStandardMaterial({
        color: 0xef4444,
        emissive: 0xdc2626,
        emissiveIntensity: 0.2,
        roughness: 0.3
      });
      const smdLed = new THREE.Mesh(
        new THREE.BoxGeometry(1.5, 0.75, 1.1),
        ledMat
      );
      smdLed.position.set(0, 1.0, pcbStartZ + 22.0);
      sGroup.add(smdLed);

      if (isLeftSensor) sensorLedLeftMat = ledMat;
      else sensorLedRightMat = ledMat;

      // Front TCRT5000 Reflective Optical Sensor Shroud hanging underneath (+Z tip, -Y underside),
      // oriented lengthwise ("front and back" along Z: 5.5mm wide x 10.2mm long, per part-linesensor.jpg):
      //   - Rear (-Z) dome : dark black IR phototransistor receiver
      //   - Center barrier : thin black anti-crosstalk divider rib
      //   - Front (+Z) dome: blue-tinted IR emitter LED
      const tcrtZ = pcbStartZ + pcbLen - 5.6;
      const tcrtHousing = new THREE.Mesh(
        new RoundedBoxGeometry(5.5, 5.6, 10.2, 2, 0.55),
        matBlackPlastic
      );
      tcrtHousing.position.set(0, -3.1, tcrtZ);
      tcrtHousing.castShadow = true;
      sGroup.add(tcrtHousing);

      const tcrtDivider = new THREE.Mesh(
        new THREE.BoxGeometry(4.4, 1.3, 0.8),
        matBlackPlastic
      );
      tcrtDivider.position.set(0, -6.1, tcrtZ);
      sGroup.add(tcrtDivider);

      // Dark IR phototransistor receiver in back (-Z) & blue-tinted IR emitter LED in front (+Z)
      const irDetector = new THREE.Mesh(
        new THREE.SphereGeometry(1.55, 14, 12),
        new THREE.MeshStandardMaterial({ color: 0x0c0d10, roughness: 0.12, metalness: 0.2 })
      );
      irDetector.position.set(0, -5.7, tcrtZ - 2.35);
      sGroup.add(irDetector);

      const irEmitter = new THREE.Mesh(
        new THREE.SphereGeometry(1.55, 14, 12),
        new THREE.MeshPhysicalMaterial({
          color: 0x3b82f6,
          roughness: 0.12,
          transmission: 0.65,
          thickness: 2.0
        })
      );
      irEmitter.position.set(0, -5.7, tcrtZ + 2.35);
      sGroup.add(irEmitter);

      // 4 silver through-hole solder cones on top (+Y) of the PCB tip matching lengthwise TCRT5000 lead spacing
      for (const lx of [-1.35, 1.35]) {
        for (const lz of [-2.45, 2.45]) {
          const lead = new THREE.Mesh(
            new THREE.ConeGeometry(0.50, 1.35, 10),
            matBrightMetal
          );
          lead.position.set(lx, 1.35, tcrtZ + lz);
          sGroup.add(lead);
        }
      }

      // Optical measurement point right between the emitter & receiver under the TCRT5000 shroud
      const tipAnchor = isLeftSensor ? sensorTipLeft : sensorTipRight;
      tipAnchor.position.set(0, -6.5, tcrtZ);
      sGroup.add(tipAnchor);

      grpSensors.add(sGroup);
    }

    buildLineSensor(5, false);  // Right sensor (cols 4,5,6 -> leaves 3 empty strips 1,2,3)
    buildLineSensor(13, true);  // Left sensor  (cols 12,13,14 -> leaves 3 empty strips 15,16,17)

    // --- 4E. Two Translucent Blue FS90R Servos + Folded Ribbon Cables ---
    const servoStickerTex = makeServoLabelTexture();
    {
      for (const sideSign of [-1, 1]) {
        const sv = new THREE.Group();
        // Aligned symmetrically with outer edges of breadboard, output shaft on axle (y=0, z=0 in chassisPivot)
        const bodyCenterX = sideSign * 17.2;
        sv.position.set(bodyCenterX, 1.8, 0.0);

        // Translucent royal-blue FS90R servo housing mounted sideways with output shaft along ±X
        const caseLenX = 19.5;
        const caseHeightY = 23.0;
        const caseThickZ = 12.4;

        // Inner brass/white nylon gear silhouettes visible through translucent blue case
        const innerMotor = new THREE.Mesh(
          new THREE.CylinderGeometry(4.6, 4.6, 13.5, 16),
          new THREE.MeshStandardMaterial({ color: 0xb8bec8, roughness: 0.4, metalness: 0.7 })
        );
        innerMotor.rotation.z = Math.PI / 2;
        innerMotor.position.set(0, -3.5, 0);
        sv.add(innerMotor);

        const innerGear = new THREE.Mesh(
          new THREE.CylinderGeometry(4.8, 4.8, 4.0, 16),
          matWhiteABS
        );
        innerGear.rotation.z = Math.PI / 2;
        innerGear.position.set(sideSign * 5.2, 4.0, 0);
        sv.add(innerGear);

        const servoBody = new THREE.Mesh(
          new RoundedBoxGeometry(caseLenX, caseHeightY, caseThickZ, 3, 0.8),
          matServoBlue
        );
        servoBody.position.set(0, 2.2, 0);
        servoBody.castShadow = true;
        sv.add(servoBody);

        // Mounting ears (sticking up & down in Y along the outer face of the servo)
        const flange = new THREE.Mesh(
          new RoundedBoxGeometry(2.4, 32.2, caseThickZ, 2, 0.4),
          matServoBlue
        );
        flange.position.set(sideSign * 4.8, 2.2, 0);
        sv.add(flange);

        // Stepped cylindrical output gear dome + secondary boss pointing outward (±X) at axle (y = -1.8 -> chassis y = 0!)
        const gearDome = new THREE.Mesh(
          new THREE.CylinderGeometry(5.8, 5.8, 4.8, 24),
          matServoBlue
        );
        gearDome.rotation.z = Math.PI / 2;
        gearDome.position.set(sideSign * (caseLenX * 0.5 + 2.0), -1.8, 0);
        sv.add(gearDome);

        const secDome = new THREE.Mesh(
          new THREE.CylinderGeometry(2.8, 2.8, 4.4, 18),
          matServoBlue
        );
        secDome.rotation.z = Math.PI / 2;
        secDome.position.set(sideSign * (caseLenX * 0.5 + 1.8), 3.6, 0);
        sv.add(secDome);

        // White nylon output spline bridging cleanly into the rear wheel hub collar (staying well behind the outer '+' slot)
        const whiteSpline = new THREE.Mesh(
          new THREE.CylinderGeometry(2.4, 2.4, 2.8, 16),
          matWhiteABS
        );
        whiteSpline.rotation.z = Math.PI / 2;
        whiteSpline.position.set(sideSign * (caseLenX * 0.5 + 2.5), -1.8, 0);
        sv.add(whiteSpline);

        // FITEC FS90R label on top/rear of one servo
        const sticker = new THREE.Mesh(
          new THREE.PlaneGeometry(14.5, 7.5),
          new THREE.MeshStandardMaterial({ map: servoStickerTex, roughness: 0.45 })
        );
        sticker.position.set(-sideSign * 1.0, 2.5, -caseThickZ * 0.5 - 0.08);
        sticker.rotation.y = Math.PI;
        sv.add(sticker);

        grpServos.add(sv);
      }

      // Neatly folded orange/red/brown servo ribbon wire loops tucked between the two servos
      // (peeking out at the top between the breadboard and AAA battery box, as seen in example-linefollower.jpg!)
      const wireColors = [0x78350f, 0xdc2626, 0xf97316]; // Brown, Red, Orange
      for (let loopIdx = 0; loopIdx < 3; loopIdx++) {
        for (let cIdx = 0; cIdx < 3; cIdx++) {
          const xOff = -4.2 + loopIdx * 3.6 + (cIdx - 1) * 1.05;
          const topPeak = BB_CENTER_Y + BB_HEIGHT * 0.5 + 3.2 - loopIdx * 1.1;
          const ribbonCurve = new THREE.CatmullRomCurve3([
            new THREE.Vector3(xOff, BB_CENTER_Y + 2.0, -2.5),
            new THREE.Vector3(xOff + 0.8, BB_CENTER_Y + 12.0, 0.8),
            new THREE.Vector3(xOff, topPeak, 2.4),
            new THREE.Vector3(xOff - 0.7, BB_CENTER_Y + 11.0, 4.2),
            new THREE.Vector3(xOff, BB_CENTER_Y - 2.0, 2.5)
          ]);
          const ribMesh = new THREE.Mesh(
            new THREE.TubeGeometry(ribbonCurve, 20, 0.58, 8, false),
            new THREE.MeshStandardMaterial({ color: wireColors[cIdx], roughness: 0.42 })
          );
          ribMesh.castShadow = true;
          grpServos.add(ribMesh);
        }
      }
    }

    // --- 4F. Two Adafruit #4205 65 mm Multi-Hub Wheels (Sleek ~9.8 mm Rubber Tire + Rear Hub Collar) ---
    function buildLegoServoWheel(isLeftWheel) {
      const wheelGrp = new THREE.Group();
      const rimMat = new THREE.MeshStandardMaterial({
        color: 0xc2c6cc,
        roughness: 0.42,
        metalness: 0.05
      });
      const tireMat = new THREE.MeshStandardMaterial({
        color: 0x1c1e22,
        roughness: 0.82,
        metalness: 0.02
      });

      const outerSign = isLeftWheel ? 1 : -1;
      const hw = WHEEL_WIDTH * 0.5; // 4.9 mm tire half-width (9.8 mm sleek rubber tire)
      const rimOuterR = 24.8;       // ~49.6 mm grey rim OD, leaving 7.7 mm rubber sidewall

      // Rounded-crown narrow rubber tire body with continuous 2.6 mm smooth center spine at R = 32.5 mm
      // and recessed shoulder valleys into which the 32 fine ribs sit cleanly within the 9.8 mm width
      const profile = [
        new THREE.Vector2(rimOuterR - 0.5, -hw + 0.55),
        new THREE.Vector2(rimOuterR + 0.9, -hw),
        new THREE.Vector2(29.5, -hw),
        new THREE.Vector2(31.0, -hw + 0.65),
        new THREE.Vector2(31.55, -3.2),
        new THREE.Vector2(31.65, -1.35),
        new THREE.Vector2(WHEEL_RADIUS, -1.2),
        new THREE.Vector2(WHEEL_RADIUS, 1.2),
        new THREE.Vector2(31.65, 1.35),
        new THREE.Vector2(31.55, 3.2),
        new THREE.Vector2(31.0, hw - 0.65),
        new THREE.Vector2(29.5, hw),
        new THREE.Vector2(rimOuterR + 0.9, hw),
        new THREE.Vector2(rimOuterR - 0.5, hw - 0.55),
        new THREE.Vector2(rimOuterR - 0.5, -hw + 0.55)
      ];
      const carcassGeo = new THREE.LatheGeometry(profile, 64);
      carcassGeo.rotateZ(Math.PI / 2);
      const carcass = new THREE.Mesh(carcassGeo, tireMat);
      carcass.castShadow = true;
      carcass.receiveShadow = true;
      wheelGrp.add(carcass);

      // 32 sleek closely-spaced shoulder ribs on each side of the smooth center spine (matching wheel-4205-00.jpg)
      const numLugs = 32;
      const lugSpanX = 3.1;
      const lugGeo = new THREE.BoxGeometry(lugSpanX, 0.95, 2.35);
      const lugInst = new THREE.InstancedMesh(lugGeo, tireMat, numLugs * 2);
      lugInst.castShadow = true;
      const dummy = new THREE.Object3D();
      let li = 0;
      for (let i = 0; i < numLugs; i++) {
        const a = (i / numLugs) * Math.PI * 2;
        for (const side of [-1, 1]) {
          dummy.position.set(
            side * 2.75,
            Math.cos(a) * (WHEEL_RADIUS - 0.52),
            Math.sin(a) * (WHEEL_RADIUS - 0.52)
          );
          dummy.rotation.set(a, 0, 0);
          dummy.rotateZ(-side * 0.14);
          dummy.updateMatrix();
          lugInst.setMatrixAt(li++, dummy.matrix);
        }
      }
      lugInst.instanceMatrix.needsUpdate = true;
      wheelGrp.add(lugInst);

      // Dished light-grey plastic rim barrel (8.8 mm wide inside the 9.8 mm tire)
      const rimHalfW = 4.4;
      const rimProfile = [
        new THREE.Vector2(22.6, -rimHalfW),
        new THREE.Vector2(rimOuterR, -rimHalfW),
        new THREE.Vector2(rimOuterR, rimHalfW),
        new THREE.Vector2(22.6, rimHalfW),
        new THREE.Vector2(22.6, -rimHalfW)
      ];
      const rimRingGeo = new THREE.LatheGeometry(rimProfile, 48);
      rimRingGeo.rotateZ(Math.PI / 2);
      const rimRing = new THREE.Mesh(rimRingGeo, rimMat);
      rimRing.castShadow = true;
      wheelGrp.add(rimRing);

      // Recessed central hub disc (3.8 mm thick inside the 8.8 mm rim barrel)
      const webCenterX = -outerSign * 0.4;
      const hub = new THREE.Mesh(
        new THREE.CylinderGeometry(8.2, 8.2, 3.8, 28),
        rimMat
      );
      hub.rotation.z = Math.PI / 2;
      hub.position.x = webCenterX;
      wheelGrp.add(hub);

      // LEGO Technic '+' cross-axle slot in the center of the hub
      for (const rotX of [0, Math.PI / 2]) {
        const crossSlot = new THREE.Mesh(
          new THREE.BoxGeometry(4.1, 4.8, 1.8),
          matHoleInterior
        );
        crossSlot.rotation.x = rotX;
        crossSlot.position.x = webCenterX;
        wheelGrp.add(crossSlot);
      }

      // 4 diagonal H-beam spokes (thin central web + twin raised edge flanges, matching wheel-4205-00.jpg)
      for (let s = 0; s < 4; s++) {
        const ang = (s * Math.PI) / 2 + Math.PI / 4;
        const spokeGroup = new THREE.Group();
        spokeGroup.position.x = webCenterX;
        spokeGroup.rotation.x = ang;

        const spokeWeb = new THREE.Mesh(
          new THREE.BoxGeometry(1.6, 4.2, 17.2),
          rimMat
        );
        spokeWeb.position.set(0, 0, 15.5);
        spokeGroup.add(spokeWeb);

        for (const ribSide of [-1.75, 1.75]) {
          const spokeRib = new THREE.Mesh(
            new THREE.BoxGeometry(3.6, 0.85, 17.2),
            rimMat
          );
          spokeRib.position.set(0, ribSide, 15.5);
          spokeGroup.add(spokeRib);
        }
        wheelGrp.add(spokeGroup);

        // 4 LEGO Technic pin bosses + open holes around center hub
        const pAng = (s * Math.PI) / 2;
        const py = Math.cos(pAng) * 5.4;
        const pz = Math.sin(pAng) * 5.4;

        const pinRing = new THREE.Mesh(
          new THREE.CylinderGeometry(2.35, 2.35, 4.0, 16),
          rimMat
        );
        pinRing.rotation.z = Math.PI / 2;
        pinRing.position.set(webCenterX, py, pz);
        wheelGrp.add(pinRing);

        const pinHole = new THREE.Mesh(
          new THREE.CylinderGeometry(1.45, 1.45, 4.3, 14),
          matHoleInterior
        );
        pinHole.rotation.z = Math.PI / 2;
        pinHole.position.set(webCenterX, py, pz);
        wheelGrp.add(pinHole);
      }

      // Inner snap-in multi-hub adapter boss extending ~4.2 mm out the back (giving ~14 mm total envelope)
      const innerCollar = new THREE.Mesh(
        new THREE.CylinderGeometry(4.6, 4.6, 6.2, 20),
        rimMat
      );
      innerCollar.rotation.z = Math.PI / 2;
      innerCollar.position.set(-outerSign * 6.0, 0, 0);
      wheelGrp.add(innerCollar);

      return wheelGrp;
    }

    const wheelMeshLeft = buildLegoServoWheel(true);
    const wheelMeshRight = buildLegoServoWheel(false);
    grpWheelLeft.add(wheelMeshLeft);
    grpWheelRight.add(wheelMeshRight);

    // --- 4G. 3×AAA Black Battery Box + Rear Steel Caster Ball + Overarching Power Loop ---
    let casterBallMesh = null;
    {
      // Battery box sits vertically behind the servos (z ≈ -13mm in chassisPivot),
      // sticking ~17mm above the breadboard top just like example-linefollower.jpg!
      const batW = 37.5;
      const batH = 52.5;
      const batD = 13.2;
      const batCenterY = 4.2;
      const batCenterZ = -13.2;

      const batBox = new THREE.Mesh(
        new RoundedBoxGeometry(batW, batH, batD, 3, 1.4),
        new THREE.MeshStandardMaterial({ color: 0x18191d, roughness: 0.48, metalness: 0.05 })
      );
      batBox.position.set(0, batCenterY, batCenterZ);
      batBox.castShadow = true;
      batBox.receiveShadow = true;
      grpBattery.add(batBox);

      // Front-facing slide switch + recessed cover screw hole (visible in example-linefollower.jpg & assembly-battery-stick-1.jpg)
      const topLatch = new THREE.Mesh(
        new THREE.BoxGeometry(6.5, 1.4, 4.2),
        matBlackPlastic
      );
      topLatch.position.set(0, batCenterY + batH * 0.5 + 0.3, batCenterZ);
      grpBattery.add(topLatch);

      const screwWell = new THREE.Mesh(
        new THREE.CylinderGeometry(2.3, 2.3, 1.2, 16),
        matHoleInterior
      );
      screwWell.rotation.x = Math.PI / 2;
      screwWell.position.set(6.5, batCenterY + 13.5, batCenterZ + batD * 0.5 - 0.3);
      grpBattery.add(screwWell);

      const onOffSwitch = new THREE.Mesh(
        new THREE.BoxGeometry(3.2, 6.2, 1.8),
        new THREE.MeshStandardMaterial({ color: 0x272a30, roughness: 0.4 })
      );
      onOffSwitch.position.set(-10.5, batCenterY + 13.5, batCenterZ + batD * 0.5 + 0.4);
      grpBattery.add(onOffSwitch);

      // Self-adhesive rear caster ball mounted under the battery box so steel ball grazes y = 0 in world!
      // Compute exact local Y at z = batCenterZ so world Y of steel ball bottom = 0.2mm:
      // In chassisPivot (origin at world y = WHEEL_RADIUS = 28, rotated around X by +CHASSIS_TILT):
      //   worldY = 28 + localY * cos(tilt) - localZ * sin(tilt)
      // Setting worldY_bottom = 0.2 at localZ = batCenterZ (-13.2):
      //   localY_bottom = (-27.8 + batCenterZ * sin(tilt)) / cos(tilt) ≈ -29.85 mm!
      const ballRadius = 4.6;
      const casterBottomLocalY = (-WHEEL_RADIUS + 0.2 + batCenterZ * Math.sin(CHASSIS_TILT)) / Math.cos(CHASSIS_TILT);
      const casterPlateY = casterBottomLocalY + 12.4;

      // Pill-shaped self-adhesive base flange (per part-casterball.jpg) with two side mounting holes
      const flangeHalfSpanX = 9.5;
      const flangeRadZ = 9.2;
      const flangeThickY = 2.2;
      const flangeCenter = new THREE.Mesh(
        new THREE.BoxGeometry(flangeHalfSpanX * 2, flangeThickY, flangeRadZ * 2),
        matBlackPlastic
      );
      flangeCenter.position.set(0, casterPlateY, batCenterZ);
      flangeCenter.castShadow = true;
      grpBattery.add(flangeCenter);

      for (const sx of [-1, 1]) {
        const flangeEnd = new THREE.Mesh(
          new THREE.CylinderGeometry(flangeRadZ, flangeRadZ, flangeThickY, 24),
          matBlackPlastic
        );
        flangeEnd.position.set(sx * flangeHalfSpanX, casterPlateY, batCenterZ);
        flangeEnd.castShadow = true;
        grpBattery.add(flangeEnd);

        const flangeHole = new THREE.Mesh(
          new THREE.CylinderGeometry(1.6, 1.6, flangeThickY + 0.2, 14),
          matHoleInterior
        );
        flangeHole.position.set(sx * (flangeHalfSpanX + 2.2), casterPlateY, batCenterZ);
        grpBattery.add(flangeHole);
      }

      // Tapered cone: WIDE at the top against the base flange, NARROW collar at the bottom hugging the steel ball!
      const coneHeight = 8.4;
      const casterDome = new THREE.Mesh(
        new THREE.CylinderGeometry(9.0, 5.2, coneHeight, 28),
        matBlackPlastic
      );
      casterDome.position.set(0, casterPlateY - flangeThickY * 0.5 - coneHeight * 0.5 + 0.2, batCenterZ);
      casterDome.castShadow = true;
      grpBattery.add(casterDome);

      casterBallMesh = new THREE.Mesh(
        new THREE.SphereGeometry(ballRadius, 24, 20),
        matChrome
      );
      casterBallMesh.position.set(0, casterBottomLocalY + ballRadius, batCenterZ);
      casterBallMesh.castShadow = true;
      grpBattery.add(casterBallMesh);

      // Iconic overarching Red & Black battery wires:
      // Exit top-+X corner of battery box (viewer's right in example-linefollower.jpg),
      // arc gracefully up & across to the black 3-pin battery connector on viewer's left (cols 4 & 5, row 3)!
      const batPlugPos = holePos(4.5, 3, 12.6);
      const wireSpecs = [
        {
          color: 0xdc2626, // Red (+5V to col 5)
          pts: [
            new THREE.Vector3(12.0, batCenterY + batH * 0.5 - 1.0, batCenterZ + 1.5),
            new THREE.Vector3(8.5, batCenterY + batH * 0.5 + 18.0, -4.0),
            new THREE.Vector3(-10.5, batCenterY + batH * 0.5 + 12.0, 12.0),
            new THREE.Vector3(-23.5, BB_CENTER_Y + 11.0, 24.5),
            new THREE.Vector3(-19.5, batPlugPos.y - 2.2, 29.0),
            new THREE.Vector3(holePos(5, 3).x, batPlugPos.y, batPlugPos.z)
          ]
        },
        {
          color: 0x17191c, // Black (GND to col 4)
          pts: [
            new THREE.Vector3(13.8, batCenterY + batH * 0.5 - 1.0, batCenterZ + 0.5),
            new THREE.Vector3(11.0, batCenterY + batH * 0.5 + 22.5, -2.5),
            new THREE.Vector3(-9.0, batCenterY + batH * 0.5 + 15.0, 13.5),
            new THREE.Vector3(-22.2, BB_CENTER_Y + 13.5, 25.8),
            new THREE.Vector3(-20.8, batPlugPos.y + 0.5, 29.8),
            new THREE.Vector3(holePos(4, 3).x, batPlugPos.y, batPlugPos.z)
          ]
        }
      ];

      for (const ws of wireSpecs) {
        const c = new THREE.CatmullRomCurve3(ws.pts);
        const m = new THREE.Mesh(
          new THREE.TubeGeometry(c, 44, 0.92, 10, false),
          new THREE.MeshStandardMaterial({ color: ws.color, roughness: 0.36 })
        );
        m.castShadow = true;
        grpBattery.add(m);
      }
    }

    // =========================================================================
    // 5. EXPLODED-VIEW INTERACTION (CLEAN AXIS OFFSETS)
    // =========================================================================
    let explodeAmount = 0;
    function applyExplode(amount) {
      explodeAmount = amount;
      const e = amount;
      grpBreadboard.position.set(0, 0, e * 10);
      grpXiao.position.set(0, 0, e * 34);
      grpWires.position.set(0, e * 14, e * 22);
      grpSensors.position.set(0, e * 4, e * 38);
      grpServos.position.set(0, 0, -e * 14);
      grpBattery.position.set(0, e * 8, -e * 38);
      grpWheelLeft.position.x = WHEEL_TRACK_HALF + e * 26;
      grpWheelRight.position.x = -WHEEL_TRACK_HALF - e * 26;
    }

    // =========================================================================
    // 6. DIFFERENTIAL-DRIVE KINEMATICS + LINE-FOLLOWER CONTROL LAW
    // =========================================================================
    // Sensor outputs: true (1) over reflective floor, false (0) over black isolation tape.
    // Control law:
    //   left_motor_speed  = bool(left_sensor)  * max_speed
    //   right_motor_speed = bool(right_sensor) * (-max_speed)
    // where max_speed is in [0, 1]. Because the two FS90R servos are mounted back-to-back
    // facing opposite sides (+X left shaft, -X right shaft), +max_speed on the left motor
    // and -max_speed on the right motor both roll their respective wheels forward.
    const FULL_THROTTLE_MM_PER_SEC = 195.0; // linear wheel speed at |motor_speed| = 1.0 (~57 RPM on 65mm wheel)
    const AXLE_TRACK = WHEEL_TRACK_HALF * 2.0;

    let maxSpeed = 0.60;

    const botState = {
      x: 0,
      z: 0,
      heading: 0,
      leftSensor: true,
      rightSensor: true,
      leftMotorSpeed: maxSpeed,
      rightMotorSpeed: -maxSpeed,
      wheelAngleL: 0,
      wheelAngleR: 0,
      simTime: 0
    };

    const tmpWorldL = new THREE.Vector3();
    const tmpWorldR = new THREE.Vector3();

    function syncBotTransform() {
      botRoot.position.set(botState.x, 0, botState.z);
      botRoot.rotation.y = botState.heading;
      wheelMeshLeft.rotation.x = botState.wheelAngleL;
      wheelMeshRight.rotation.x = botState.wheelAngleR;
      botRoot.updateMatrixWorld(true);
    }

    function placeBotOnTrackStart() {
      const u0 = 0.25; // start at top of squashed waist heading smoothly into the left lobe
      const p0 = trackCurve.getPointAt(u0);
      const p1 = trackCurve.getPointAt(u0 + 0.004);
      const dx = p1.x - p0.x;
      const dz = p1.z - p0.z;
      const heading = Math.atan2(dx, dz);

      // Sensor pair sits at cols 5 & 12 (midpoint local X = -1.27mm); back-compute chassis position
      // so the black tape begins centered directly between the two TCRT5000 optical heads
      botState.x = p0.x;
      botState.z = p0.z;
      botState.heading = heading;
      botState.leftSensor = true;
      botState.rightSensor = true;
      botState.leftMotorSpeed = maxSpeed;
      botState.rightMotorSpeed = -maxSpeed;
      syncBotTransform();

      sensorTipLeft.getWorldPosition(tmpWorldL);
      sensorTipRight.getWorldPosition(tmpWorldR);
      const midX = 0.5 * (tmpWorldL.x + tmpWorldR.x);
      const midZ = 0.5 * (tmpWorldL.z + tmpWorldR.z);
      const nearPt = trackCurve.getPointAt(u0 + 0.02);
      // Shift slightly along normal so midpoint of sensors starts right on the track centerline
      const nrmX = Math.cos(heading);
      const nrmZ = -Math.sin(heading);
      const latErr = (midX - nearPt.x) * nrmX + (midZ - nearPt.z) * nrmZ;
      botState.x -= nrmX * latErr;
      botState.z -= nrmZ * latErr;
      syncBotTransform();
    }

    function buildSquashedOvalTrack() {
      trackCurve = new THREE.CatmullRomCurve3(SQUASHED_OVAL_POINTS, true, 'centripetal', 0.5);

      trackPolyline = [];
      const spaced = trackCurve.getSpacedPoints(TRACK_SAMPLES);
      for (let i = 0; i < TRACK_SAMPLES; i++) {
        trackPolyline.push({ x: spaced[i].x, z: spaced[i].z });
      }

      if (trackMesh) {
        scene.remove(trackMesh);
        trackMesh.geometry.dispose();
      }
      trackMesh = new THREE.Mesh(buildTrackRibbon(trackCurve, TAPE_WIDTH, TRACK_SAMPLES), tapeMaterial);
      trackMesh.receiveShadow = true;
      scene.add(trackMesh);

      placeBotOnTrackStart();
    }

    buildSquashedOvalTrack();

    const elLedLeft = document.getElementById('led-left');
    const elLedRight = document.getElementById('led-right');
    const elValLeft = document.getElementById('val-left');
    const elValRight = document.getElementById('val-right');
    const elSpdLeft = document.getElementById('spd-left');
    const elSpdRight = document.getElementById('spd-right');

    function formatSigned(v) {
      if (Math.abs(v) < 1e-4) return '0.00';
      return (v > 0 ? '+' : '') + v.toFixed(2);
    }

    function stepSimulation(dt) {
      // Sub-step at <= 2ms so sensor transitions across the 13.6mm tape are crisp even at max_speed = 1.0
      const subSteps = Math.max(1, Math.ceil(dt / 0.002));
      const h = dt / subSteps;

      for (let s = 0; s < subSteps; s++) {
        botState.simTime += h;

        // 1. Sample floor reflectivity under each TCRT5000 optical tip:
        //    true (1) over reflective floor, false (0) over black isolation tape
        sensorTipLeft.getWorldPosition(tmpWorldL);
        sensorTipRight.getWorldPosition(tmpWorldR);

        const left_sensor = !isPointOnBlackTape(tmpWorldL.x, tmpWorldL.z);
        const right_sensor = !isPointOnBlackTape(tmpWorldR.x, tmpWorldR.z);

        // 2. Exact line-follower algorithm:
        const left_motor_speed = (left_sensor ? 1 : 0) * maxSpeed;
        const right_motor_speed = (right_sensor ? 1 : 0) * (-maxSpeed);

        botState.leftSensor = left_sensor;
        botState.rightSensor = right_sensor;
        botState.leftMotorSpeed = left_motor_speed;
        botState.rightMotorSpeed = right_motor_speed;

        // Convert signed servo throttle [-1, 1] to linear wheel velocity along robot +Z:
        // Left servo shaft faces +X (+throttle = forward); right servo shaft faces -X (-throttle = forward)
        const vLeft = left_motor_speed * FULL_THROTTLE_MM_PER_SEC;
        const vRight = (-right_motor_speed) * FULL_THROTTLE_MM_PER_SEC;

        const vLinear = 0.5 * (vLeft + vRight);
        const omega = (vRight - vLeft) / AXLE_TRACK;

        const midHeading = botState.heading + 0.5 * omega * h;
        botState.x += Math.sin(midHeading) * vLinear * h;
        botState.z += Math.cos(midHeading) * vLinear * h;
        botState.heading += omega * h;

        // 3. No-slip wheel & rear caster rotation
        botState.wheelAngleL += (vLeft * h) / WHEEL_RADIUS;
        botState.wheelAngleR += (vRight * h) / WHEEL_RADIUS;
        if (casterBallMesh) {
          casterBallMesh.rotation.x += (vLinear * h) / 4.6;
        }

        syncBotTransform();
      }

      const leftOnLine = !botState.leftSensor;
      const rightOnLine = !botState.rightSensor;

      if (sensorLedLeftMat) {
        sensorLedLeftMat.emissiveIntensity = leftOnLine ? 2.2 : 0.12;
        sensorLedLeftMat.color.setHex(leftOnLine ? 0xff3b3b : 0x551818);
      }
      if (sensorLedRightMat) {
        sensorLedRightMat.emissiveIntensity = rightOnLine ? 2.2 : 0.12;
        sensorLedRightMat.color.setHex(rightOnLine ? 0xff3b3b : 0x551818);
      }

      if (neoPixelMesh) {
        const hue = (botState.simTime * 0.35) % 1.0;
        neoPixelMesh.material.color.setHSL(hue, 0.9, 0.55);
        neoPixelMesh.material.emissive.setHSL(hue, 0.9, 0.45);
      }

      elLedLeft.classList.toggle('on-line', leftOnLine);
      elLedRight.classList.toggle('on-line', rightOnLine);
      elValLeft.textContent = botState.leftSensor ? '1' : '0';
      elValRight.textContent = botState.rightSensor ? '1' : '0';
      elSpdLeft.textContent = formatSigned(botState.leftMotorSpeed);
      elSpdRight.textContent = formatSigned(botState.rightMotorSpeed);
    }

    // =========================================================================
    // 7. CAMERA MODES & UI WIRING
    // =========================================================================
    let camMode = 'follow'; // 'follow' | 'front' | 'rear' | 'overview'
    let isPlaying = true;

    // Relative offset preserved while OrbitControls orbits in follow mode
    const followOffset = new THREE.Vector3(135, 118, 168);
    let userDraggingOrbit = false;
    controls.addEventListener('start', () => { userDraggingOrbit = true; });
    controls.addEventListener('end', () => {
      userDraggingOrbit = false;
      if (camMode === 'follow') {
        const worldDelta = camera.position.clone().sub(controls.target);
        followOffset.copy(worldDelta).applyAxisAngle(new THREE.Vector3(0, 1, 0), -botState.heading);
      }
    });

    function setCameraMode(mode) {
      camMode = mode;
      for (const id of ['cam-follow', 'cam-front', 'cam-rear', 'cam-overview']) {
        document.getElementById(id).classList.toggle('active', id === `cam-${mode}`);
      }
      if (mode === 'follow') {
        followOffset.set(135, 118, 168);
      } else if (mode === 'overview') {
        controls.target.set(0, 15, 0);
        camera.position.set(0, 560, 480);
      }
    }

    const desiredCamPos = new THREE.Vector3();
    const desiredTarget = new THREE.Vector3();
    const upAxis = new THREE.Vector3(0, 1, 0);

    function updateCamera(dt) {
      if (camMode === 'overview') {
        controls.update();
        return;
      }

      const botCenter = new THREE.Vector3(botState.x, 30, botState.z);
      if (camMode === 'follow') {
        if (!userDraggingOrbit) {
          const rotatedOff = followOffset.clone().applyAxisAngle(upAxis, botState.heading);
          desiredCamPos.copy(botCenter).add(rotatedOff);
          const smooth = 1 - Math.exp(-dt * 5.5);
          camera.position.lerp(desiredCamPos, smooth);
          controls.target.lerp(botCenter, smooth * 1.4);
        } else {
          controls.target.copy(botCenter);
        }
      } else if (camMode === 'front') {
        const localOff = new THREE.Vector3(12, 52, 166).applyAxisAngle(upAxis, botState.heading);
        const lookOff = new THREE.Vector3(0, 26, 12).applyAxisAngle(upAxis, botState.heading);
        desiredCamPos.set(botState.x, 0, botState.z).add(localOff);
        desiredTarget.set(botState.x, 0, botState.z).add(lookOff);
        const smooth = 1 - Math.exp(-dt * 8.0);
        camera.position.lerp(desiredCamPos, smooth);
        controls.target.lerp(desiredTarget, smooth);
      } else if (camMode === 'rear') {
        const localOff = new THREE.Vector3(-52, 78, -156).applyAxisAngle(upAxis, botState.heading);
        const lookOff = new THREE.Vector3(0, 30, -4).applyAxisAngle(upAxis, botState.heading);
        desiredCamPos.set(botState.x, 0, botState.z).add(localOff);
        desiredTarget.set(botState.x, 0, botState.z).add(lookOff);
        const smooth = 1 - Math.exp(-dt * 8.0);
        camera.position.lerp(desiredCamPos, smooth);
        controls.target.lerp(desiredTarget, smooth);
      }

      controls.update();
    }

    // Bind UI controls
    document.getElementById('cam-follow').addEventListener('click', () => setCameraMode('follow'));
    document.getElementById('cam-front').addEventListener('click', () => setCameraMode('front'));
    document.getElementById('cam-rear').addEventListener('click', () => setCameraMode('rear'));
    document.getElementById('cam-overview').addEventListener('click', () => setCameraMode('overview'));

    const btnPlay = document.getElementById('btn-play');
    btnPlay.addEventListener('click', () => {
      isPlaying = !isPlaying;
      btnPlay.textContent = isPlaying ? 'Pause' : 'Play';
      btnPlay.classList.toggle('active', isPlaying);
    });

    const sliderSpeed = document.getElementById('slider-speed');
    const labelSpeed = document.getElementById('label-speed');
    function setMaxSpeed(val) {
      maxSpeed = Math.max(0, Math.min(1, val));
      sliderSpeed.value = String(Math.round(maxSpeed * 100));
      labelSpeed.textContent = maxSpeed.toFixed(2);
      botState.leftMotorSpeed = (botState.leftSensor ? 1 : 0) * maxSpeed;
      botState.rightMotorSpeed = (botState.rightSensor ? 1 : 0) * (-maxSpeed);
      elSpdLeft.textContent = formatSigned(botState.leftMotorSpeed);
      elSpdRight.textContent = formatSigned(botState.rightMotorSpeed);
    }
    sliderSpeed.addEventListener('input', (e) => {
      setMaxSpeed(Number(e.target.value) / 100);
    });

    const sliderExplode = document.getElementById('slider-explode');
    sliderExplode.addEventListener('input', (e) => {
      applyExplode(Number(e.target.value) / 100);
    });

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Snap initial camera cleanly onto the robot without initial lerp lag
    {
      const initCenter = new THREE.Vector3(botState.x, 30, botState.z);
      const initOff = followOffset.clone().applyAxisAngle(upAxis, botState.heading);
      camera.position.copy(initCenter).add(initOff);
      controls.target.copy(initCenter);
      controls.update();
    }

    // =========================================================================
    // 8. RENDER LOOP & TEST / INSPECTION HOOK
    // =========================================================================
    let lastTime = performance.now();
    function animate(now) {
      requestAnimationFrame(animate);
      const rawDt = Math.min(0.05, Math.max(0.001, (now - lastTime) / 1000));
      lastTime = now;

      if (isPlaying) {
        stepSimulation(rawDt);
      }
      updateCamera(rawDt);

      // Keep shadow frustum centered near the robot for ultra-crisp contact shadows everywhere
      keyLight.target.position.set(botState.x, 0, botState.z);
      keyLight.target.updateMatrixWorld();
      keyLight.position.set(botState.x + 220, 420, botState.z + 260);

      renderer.render(scene, camera);
    }
    requestAnimationFrame(animate);

    // Deterministic inspection hook for automated verification
    window.__BREADBOARDBOT__ = {
      botState,
      reset: placeBotOnTrackStart,
      setMaxSpeed,
      step: (seconds, doRender = false) => {
        const chunks = Math.ceil(seconds / 0.02);
        for (let i = 0; i < chunks; i++) stepSimulation(seconds / chunks);
        if (doRender) {
          keyLight.target.position.set(botState.x, 0, botState.z);
          keyLight.target.updateMatrixWorld();
          keyLight.position.set(botState.x + 220, 420, botState.z + 260);
          renderer.render(scene, camera);
        }
      },
      setPaused: (paused) => {
        isPlaying = !paused;
        btnPlay.textContent = isPlaying ? 'Pause' : 'Play';
        btnPlay.classList.toggle('active', isPlaying);
      },
      setCameraMode,
      setXiaoVisible: (v) => {
        grpXiao.visible = v;
        renderer.render(scene, camera);
      },
      setExplode: (v) => {
        sliderExplode.value = String(Math.round(v * 100));
        applyExplode(v);
        renderer.render(scene, camera);
      },
      setCustomCamera: (pos, target) => {
        camMode = 'custom';
        camera.position.set(pos[0], pos[1], pos[2]);
        controls.target.set(target[0], target[1], target[2]);
        controls.update();
        renderer.render(scene, camera);
      },
      getSensorMidpointTrackError: () => {
        sensorTipLeft.getWorldPosition(tmpWorldL);
        sensorTipRight.getWorldPosition(tmpWorldR);
        const mx = 0.5 * (tmpWorldL.x + tmpWorldR.x);
        const mz = 0.5 * (tmpWorldL.z + tmpWorldR.z);
        return Math.sqrt(distanceSqToTrack(mx, mz));
      }
    };
