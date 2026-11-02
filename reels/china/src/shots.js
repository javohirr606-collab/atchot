// Edit list shared by the page and tools/frames.mjs. Times in seconds on the timeline.
// 0–5.6 s: metro-door hook (graphic + Nodira's announcement); from DROP the cuts sit on the percussion beat (0.4644 s);
// narration (Davronbek) starts at NA. clip = source in assets/clips, vs = source in-point, z0→z1 = slow push, dark = overlay.
(() => {
  const DROP = 5.6, BEAT = 0.4644, B = k => +(DROP + k * BEAT).toFixed(3);
  window.EDIT = {
    DUR: 42.0, DROP, BEAT, NA: 7.45, HOOK_AT: 0.15, HOOK_B_AT: 3.85,
    SHOTS: [
      { t0: 5.08,  t1: B(1),  clip: 'c06', vs: 0.0,   z0: 1.12, z1: 1.04, dark: .2 },  // doors open onto Chongqing
      { t0: B(1),  t1: B(2),  clip: 'c01', vs: 2.3,   z0: 1.08, z1: 1.00 },            // red towers
      { t0: B(2),  t1: B(3),  clip: 'c01', vs: 4.3,   z0: 1.08, z1: 1.00 },            // bridge
      { t0: B(3),  t1: B(4),  clip: 'c01', vs: 34.6,  z0: 1.08, z1: 1.00 },            // neon lattice
      { t0: B(4),  t1: B(8),  clip: 'c04', vs: 11.7,  z0: 1.00, z1: 1.06, dark: .5 },  // 15 kunlik: Hongyadong
      { t0: B(8),  t1: B(11), clip: 'c01', vs: 7.0,   z0: 1.00, z1: 1.06, dark: .5 },
      { t0: B(11), t1: B(14), clip: 'c01', vs: 0.2,   z0: 1.00, z1: 1.06, dark: .5 },
      { t0: B(14), t1: B(17), clip: 'c01', vs: 33.0,  z0: 1.00, z1: 1.05, dark: .5 },  // AI: neon
      { t0: B(17), t1: B(20), clip: 'c01', vs: 21.0,  z0: 1.00, z1: 1.05, dark: .5 },
      { t0: B(20), t1: B(25), clip: 'c01', vs: 12.85, z0: 1.00, z1: 1.06, dark: .5 },
      { t0: B(25), t1: B(28), clip: 'c01', vs: 23.95, z0: 1.00, z1: 1.05, dark: .5 },  // factories: motion
      { t0: B(28), t1: B(32), clip: 'c05', vs: 0.5,   z0: 1.00, z1: 1.05, dark: .5 },
      { t0: B(32), t1: B(35), clip: 'c01', vs: 28.4,  z0: 1.00, z1: 1.05, dark: .5 },
      { t0: B(35), t1: B(37), clip: 'c01', vs: 27.0,  z0: 1.00, z1: 1.05, dark: .5 },
      { t0: B(37), t1: B(40), clip: 'c01', vs: 29.85, z0: 1.00, z1: 1.05, dark: .5 },  // seminar
      { t0: B(40), t1: B(43), clip: 'c01', vs: 31.35, z0: 1.00, z1: 1.05, dark: .5 },
      { t0: B(43), t1: B(47), clip: 'c02', vs: 4.0,   z0: 1.00, z1: 1.08, dark: .4 },  // certificate
      { t0: B(47), t1: B(48), clip: 'c03', vs: 1.0,   z0: 1.08, z1: 1.00, dark: .35 }, // dates burst
      { t0: B(48), t1: B(49), clip: 'c01', vs: 18.0,  z0: 1.08, z1: 1.00, dark: .35 },
      { t0: B(49), t1: B(50), clip: 'c03', vs: 6.5,   z0: 1.08, z1: 1.00, dark: .35 },
      { t0: B(50), t1: B(51), clip: 'c01', vs: 36.0,  z0: 1.08, z1: 1.00, dark: .35 },
      { t0: B(51), t1: B(52), clip: 'c01', vs: 37.5,  z0: 1.08, z1: 1.00, dark: .35 },
      { t0: B(52), t1: B(53), clip: 'c04', vs: 15.5,  z0: 1.08, z1: 1.00, dark: .35 },
      { t0: B(53), t1: B(57), clip: 'c04', vs: 21.63, z0: 1.00, z1: 1.05, dark: .58 }, // all inclusive (c04 fades out after ~24 s)
      { t0: B(57), t1: B(61), clip: 'c05', vs: 3.6,   z0: 1.00, z1: 1.05, dark: .58 },
      { t0: B(61), t1: B(65), clip: 'c01', vs: 15.5,  z0: 1.00, z1: 1.06, dark: .5 },  // price
      { t0: B(65), t1: 42.0,  clip: 'c06', vs: 0.75,  z0: 1.04, z1: 1.12, dark: .62 }, // CTA, back to the opening city
    ],
  };
})();
