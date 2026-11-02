"""Soundtrack: metro-chime hook, percussion bed from the drop, synthesized whooshes and hits.
Usage: python3 tools/mix.py   (needs ffmpeg and numpy; writes build/mix.wav)
"""
import os, subprocess, tempfile
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
A = os.path.join(ROOT, 'src', 'assets')
OUT = os.path.join(ROOT, 'build')
os.makedirs(OUT, exist_ok=True)
SR = 48000
DUR = 31.0
rng = np.random.default_rng(7)


def load(path, af=None):
    with tempfile.TemporaryDirectory() as d:
        wav = os.path.join(d, 'x.f32')
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', path]
        if af:
            cmd += ['-af', af]
        cmd += ['-ac', '2', '-ar', str(SR), '-f', 'f32le', wav]
        subprocess.run(cmd, check=True)
        return np.fromfile(wav, dtype=np.float32).reshape(-1, 2).astype(np.float64)


def db(x):
    return 10 ** (x / 20)


N = int(DUR * SR)
t_axis = np.arange(N) / SR


def place(bus, sig, at, gain=1.0):
    i = int(round(at * SR))
    if i < 0:
        sig = sig[-i:]
        i = 0
    n = min(len(sig), N - i)
    if n > 0:
        bus[i:i + n] += sig[:n] * gain


def envelope(points):
    """Piecewise-linear gain curve in dB: [(t, dB), ...]."""
    ts = np.array([p[0] for p in points]); gs = np.array([p[1] for p in points])
    return db(np.interp(t_axis, ts, gs))[:, None]


# ── SFX (synthesized) ──
sfx = np.zeros((N, 2))


def noise(n):
    return rng.standard_normal(n)


def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y


def sweep_bp(x, f0, f1):
    """Crude time-varying band-pass: high-pass by subtracting a moving low-pass, both swept."""
    n = len(x); f = np.geomspace(f0, f1, n)
    lo = np.empty(n); hi = np.empty(n); a1 = a2 = 0.0
    for i in range(n):
        c1 = np.exp(-2 * np.pi * f[i] * 1.6 / SR); c2 = np.exp(-2 * np.pi * f[i] / 1.6 / SR)
        a1 = (1 - c1) * x[i] + c1 * a1; a2 = (1 - c2) * x[i] + c2 * a2
        lo[i] = a1; hi[i] = a2
    return lo - hi


def whoosh(d=.42, f0=350, f1=3200, level=-14, pan=True):
    n = int(d * SR); x = noise(n)
    y = sweep_bp(x, f0, f1)
    env = np.sin(np.linspace(0, np.pi, n)) ** 1.6
    y = y * env; y /= np.abs(y).max() + 1e-9; y *= db(level)
    if pan:
        p = np.linspace(-.6, .6, n)
        return np.stack([y * np.sqrt((1 - p) / 2) * 1.41, y * np.sqrt((1 + p) / 2) * 1.41], 1)
    return np.stack([y, y], 1)


def boom(level=-6, f0=110, f1=38, d=1.2):
    n = int(d * SR); tt = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-tt * 9); ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-tt * 3.2)
    click = onepole_lp(noise(int(.03 * SR)), 1800) * np.exp(-np.arange(int(.03 * SR)) / SR * 140) * 3
    y[:len(click)] += click
    y /= np.abs(y).max(); y *= db(level)
    return np.stack([y, y], 1)


def pop(level=-12, f=880):
    n = int(.12 * SR); tt = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * tt * (1 + 0.6 * np.exp(-tt * 40))) * np.exp(-tt * 38)
    y *= db(level)
    return np.stack([y, y], 1)


def riser(d, level=-16):
    n = int(d * SR); x = noise(n)
    y = sweep_bp(x, 300, 7000)
    env = np.linspace(0, 1, n) ** 2.4
    y = y / (np.abs(y).max() + 1e-9) * env * db(level)
    tt = np.arange(n) / SR
    tone = np.sin(2 * np.pi * np.cumsum(np.geomspace(180, 720, n)) / SR) * env * db(level - 8)
    y = y + tone
    return np.stack([y, y], 1)


def chime(level=-16):
    n = int(2.6 * SR); tt = np.arange(n) / SR; y = np.zeros(n)
    for f, dt in ((784, 0), (1174.66, .09), (1568, .18)):
        k = tt >= dt; u = tt[k] - dt
        y[k] += (np.sin(2 * np.pi * f * u) * .8 + np.sin(4 * np.pi * f * u) * .15) * np.exp(-u * 2.2)
    y /= np.abs(y).max(); y *= db(level)
    return np.stack([y, y * .96], 1)



DROP = 2.80

# ── hook: low city drone, metro chime, riser into the drop ──
bed = np.zeros((N, 2))
n = int(DROP * SR)
drone = onepole_lp(noise(n), 260) * 6
tt = np.arange(n) / SR
drone += .25 * np.sin(2 * np.pi * 55 * tt) + .12 * np.sin(2 * np.pi * 82.4 * tt)
drone *= np.minimum(1, tt / .4) * db(-24)
place(bed, np.stack([drone, drone], 1), 0)


def metro_chime(level=-13):
    """Three-tone station chime (bright, soft attack)."""
    out = np.zeros(int(2.2 * SR)); tt = np.arange(len(out)) / SR
    for f, dt in ((1046.5, 0), (830.6, .32), (659.3, .64)):
        k = tt >= dt; u = tt[k] - dt
        out[k] += (np.sin(2 * np.pi * f * u) + .3 * np.sin(4 * np.pi * f * u) + .08 * np.sin(6 * np.pi * f * u)) * np.exp(-u * 3.0) * np.minimum(1, u / .006)
    out /= np.abs(out).max(); out *= db(level)
    return np.stack([out, out * .97], 1)



# ── percussion bed from the drop (its strong downbeat at 3.76 s lands on 2.80 s) ──
perc = load(os.path.join(A, 'music_percussion.mp3'))
perc = perc[int(3.76 * SR):]
bus_p = np.zeros((N, 2)); place(bus_p, perc, DROP)
bus_p *= envelope([(0, -80), (DROP - .01, -80), (DROP, 0), (29.9, 0), (30.95, -40), (DUR, -60)])

# ── SFX ──
sfx = np.zeros((N, 2))

place(sfx, metro_chime(-12), 0.12)
place(sfx, whoosh(.35, 500, 3500, -20), 0.3)       # KEYINGI BEKAT
place(sfx, whoosh(.3, 400, 3000, -17), 1.42)       # XITOY
place(sfx, riser(1.3, -15), DROP - 1.3)
place(sfx, boom(-5), DROP)
for tt in (5.59, 8.37, 11.16, 13.95, 16.74, 19.52, 21.38, 25.10, 26.95):
    place(sfx, whoosh(.38, level=-15), tt - .2)
for tt in (9.30, 9.77, 10.23, 21.85, 22.31, 22.78, 23.24, 23.71, 27.0):
    place(sfx, pop(-15, 900), tt)
place(sfx, boom(-12, 120, 50, .6), 5.9)            # 15 kunlik
place(sfx, boom(-12, 120, 50, .6), 11.32)          # BYD
place(sfx, boom(-10, 140, 55, .5), 17.65)          # seal stamp
place(sfx, boom(-6), 25.32)                        # $950
place(sfx, metro_chime(-16), 29.75)                # bookend

mix = bed + bus_p + sfx
raw = os.path.join(OUT, 'mix_raw.f32')
mix.astype(np.float32).tofile(raw)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', raw,
                '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9:linear=false,alimiter=limit=0.8,volume=-2dB',
                '-ar', str(SR), '-c:a', 'pcm_s16le', os.path.join(OUT, 'mix.wav')], check=True)
os.remove(raw)
print('wrote build/mix.wav')
