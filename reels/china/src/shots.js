// Edit list shared by the page and tools/frames.mjs. Times in seconds; cuts sit on the percussion beat (0.4644 s) from the drop at 2.80 s.
// clip = source in assets/clips, vs = source in-point, z0→z1 = slow push, dark = overlay for text legibility.
window.EDIT = {
  DUR: 31.0,
  DROP: 2.80,
  BEAT: 0.4644,
  SHOTS: [
    { t0: 0.00,  t1: 2.80,  clip: 'c06', vs: 0.0,   z0: 1.00, z1: 1.10, dark: .25 },  // hook: dusk aerial
    { t0: 2.80,  t1: 3.26,  clip: 'c01', vs: 2.3,   z0: 1.08, z1: 1.00 },             // red towers
    { t0: 3.26,  t1: 3.73,  clip: 'c01', vs: 4.3,   z0: 1.08, z1: 1.00 },             // bridge
    { t0: 3.73,  t1: 4.19,  clip: 'c01', vs: 7.0,   z0: 1.08, z1: 1.00 },             // tower top
    { t0: 4.19,  t1: 4.66,  clip: 'c01', vs: 34.6,  z0: 1.08, z1: 1.00 },             // neon lattice
    { t0: 4.66,  t1: 5.12,  clip: 'c01', vs: 21.0,  z0: 1.08, z1: 1.00 },             // billboard street
    { t0: 5.12,  t1: 5.59,  clip: 'c02', vs: 1.0,   z0: 1.08, z1: 1.00 },             // sky garden
    { t0: 5.59,  t1: 6.98,  clip: 'c04', vs: 11.7,  z0: 1.00, z1: 1.06, dark: .5 }, // Hongyadong
    { t0: 6.98,  t1: 8.37,  clip: 'c01', vs: 0.2,   z0: 1.00, z1: 1.06, dark: .5 },
    { t0: 8.37,  t1: 9.30,  clip: 'c01', vs: 33.0,  z0: 1.00, z1: 1.05, dark: .5 }, // AI: neon streets
    { t0: 9.30,  t1: 10.23, clip: 'c01', vs: 21.45, z0: 1.00, z1: 1.05, dark: .5 },
    { t0: 10.23, t1: 11.16, clip: 'c01', vs: 9.6,   z0: 1.00, z1: 1.05, dark: .5 },
    { t0: 11.16, t1: 12.09, clip: 'c01', vs: 24.0,  z0: 1.00, z1: 1.05, dark: .5 }, // factories: motion, transport
    { t0: 12.09, t1: 13.02, clip: 'c05', vs: 1.0,   z0: 1.00, z1: 1.05, dark: .5 },
    { t0: 13.02, t1: 13.95, clip: 'c01', vs: 28.5,  z0: 1.00, z1: 1.05, dark: .5 },
    { t0: 13.95, t1: 14.88, clip: 'c01', vs: 29.9,  z0: 1.00, z1: 1.05, dark: .5 }, // seminar: people, bridges
    { t0: 14.88, t1: 15.81, clip: 'c01', vs: 37.5,  z0: 1.00, z1: 1.05, dark: .5 },
    { t0: 15.81, t1: 16.74, clip: 'c01', vs: 31.4,  z0: 1.00, z1: 1.05, dark: .5 },
    { t0: 16.74, t1: 19.52, clip: 'c02', vs: 4.0,   z0: 1.00, z1: 1.08, dark: .35 }, // certificate
    { t0: 19.52, t1: 19.99, clip: 'c03', vs: 1.0,   z0: 1.08, z1: 1.00, dark: .3 },  // dates burst
    { t0: 19.99, t1: 20.45, clip: 'c01', vs: 18.0,  z0: 1.08, z1: 1.00, dark: .3 },
    { t0: 20.45, t1: 20.92, clip: 'c03', vs: 6.5,   z0: 1.08, z1: 1.00, dark: .3 },
    { t0: 20.92, t1: 21.38, clip: 'c01', vs: 36.0,  z0: 1.08, z1: 1.00, dark: .3 },
    { t0: 21.38, t1: 25.10, clip: 'c04', vs: 21.62, z0: 1.00, z1: 1.08, dark: .55 }, // all inclusive
    { t0: 25.10, t1: 26.95, clip: 'c01', vs: 12.0,  z0: 1.00, z1: 1.06, dark: .5 },  // price
    { t0: 26.95, t1: 31.0,  clip: 'c06', vs: 2.8,   z0: 1.05, z1: 1.12, dark: .62 }, // CTA, back to the opening city
  ],
};
