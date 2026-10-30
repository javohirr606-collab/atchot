"""Soundtrack for the reel: processed narration, two music beds with ducking, synthesized SFX.
Usage: python3 tools/mix.py   (needs ffmpeg and numpy; writes build/mix.wav)
"""
import os, subprocess, tempfile
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
A = os.path.join(ROOT, 'src', 'assets', 'audio')
OUT = os.path.join(ROOT, 'build')
os.makedirs(OUT, exist_ok=True)
SR = 48000
DUR = 52.5
VO_AT = 0.3
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


# ── narration: clean, present, loud (ElevenLabs file is −23 LUFS) ──
vo_chain = ('highpass=f=85,equalizer=f=220:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1.0:g=3,'
            'equalizer=f=9000:t=h:w=0.7:g=2,acompressor=threshold=-24dB:ratio=3:attack=6:release=90:makeup=4,'
            'loudnorm=I=-15:TP=-2:LRA=7')
vo = load(os.path.join(A, 'vo.mp3'), vo_chain)
voice = np.zeros((N, 2)); place(voice, vo, VO_AT)

# speech spans (narration time) for ducking
SPEECH = [(0.07, 1.98), (2.47, 8.02), (8.51, 12.94), (13.40, 21.52), (21.86, 30.42), (30.76, 36.88),
          (37.19, 38.38), (38.58, 40.05), (40.40, 43.02), (43.35, 45.72), (46.13, 48.42)]
SPEECH = [(a + VO_AT, b + VO_AT) for a, b in SPEECH]


def duck_points(t_from, t_to, under, gap, start_level):
    pts = [(t_from, start_level)]
    for a, b in SPEECH:
        if b < t_from or a > t_to:
            continue
        pts += [(max(t_from, a - .08), gap if pts[-1][1] == gap else pts[-1][1]), (max(t_from, a), under), (min(t_to, b), under), (min(t_to, b + .18), gap)]
    pts.append((t_to, pts[-1][1]))
    pts.sort(key=lambda p: p[0])
    return pts


# ── bed 1: percussion, 0 → 37.5 s ──
perc = load(os.path.join(A, 'music_percussion.mp3'))
perc = perc[int(0.9 * SR):]
bus_p = np.zeros((N, 2)); place(bus_p, perc, 0.0)
pts = duck_points(0.0, 37.0, -13, -8, -4)
pts = [p for p in pts if p[0] < 37.0] + [(37.0, -13), (37.55, -60), (DUR, -60)]
bus_p *= envelope(pts)
bus_p[: int(.03 * SR)] *= np.linspace(0, 1, int(.03 * SR))[:, None]

# ── bed 2: Evergreen. Its first band entry (16.10 s in the file) lands on "Bu — talabalarimizning…" (43.65 s) ──
DROP = 43.65
eg = load(os.path.join(A, 'music_evergreen.mp3'))
bus_e = np.zeros((N, 2)); place(bus_e, eg, DROP - 16.10)
pre = [(0, -80), (36.95, -80), (37.6, 3), (DROP - .02, 3)]
post = duck_points(DROP, 48.8, -12, -8, -12)
end = [(49.4, -5), (51.2, -5), (52.45, -40)]
bus_e *= envelope(pre + post + end)

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


SHOT_IN = [(2.55, 'whip'), (5.0, 'zoom'), (8.6, 'flash'), (10.7, 'whip'), (13.55, 'zoom'), (16.75, 'whip'),
           (22.1, 'zoom'), (26.38, 'whip'), (30.85, 'whip'), (37.3, 'slide'), (40.5, 'zoom'), (48.9, 'slide')]
for tt, kind in SHOT_IN:
    w = whoosh(.38 if kind != 'slide' else .55, level=-15 if kind != 'flash' else -19)
    place(sfx, w, tt - .22)
place(sfx, boom(-9), 0.04)                       # hook
place(sfx, pop(-17, 1200), 3.15)                 # location tag
place(sfx, whoosh(.3, 600, 4000, -20), 11.95)    # name tag
place(sfx, boom(-12, 90, 40, .8), 32.6)          # 1+2+1 card
for tt in (32.78, 33.28, 33.82):
    place(sfx, pop(-13, 660), tt); place(sfx, boom(-17, 130, 60, .35), tt)
place(sfx, boom(-14, 100, 45, .8), 37.3)
place(sfx, riser(1.75, -17), DROP - 1.75)        # into the drop
place(sfx, boom(-6), DROP)
place(sfx, whoosh(.5, 300, 2500, -14), 46.08)    # logo
place(sfx, boom(-10, 100, 42, 1.0), 46.3)
place(sfx, chime(-19), 46.5)

mix = voice + bus_p + bus_e + sfx
raw = os.path.join(OUT, 'mix_raw.f32')
mix.astype(np.float32).tofile(raw)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', raw,
                '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9:linear=false,alimiter=limit=0.8,volume=-2dB',
                '-ar', str(SR), '-c:a', 'pcm_s16le', os.path.join(OUT, 'mix.wav')], check=True)
os.remove(raw)
print('wrote build/mix.wav')
