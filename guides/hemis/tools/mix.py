"""Soundtrack for the HEMIS guide: narration (with a 3 s pause for the OneID hint), ducked percussion bed, UI sound effects.
Usage: node tools/events.mjs && python3 tools/mix.py   (needs ffmpeg and numpy; writes build/mix.wav)
"""
import os, json, subprocess, tempfile
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
A = os.path.join(ROOT, 'src', 'assets')
OUT = os.path.join(ROOT, 'build')
SR = 48000
DUR = 98.0
VO_AT, GAP, GAP_AT = 0.3, 3.0, 34.42   # narration offset; OneID pause inserted at this file time
N = int(DUR * SR)
t_axis = np.arange(N) / SR
rng = np.random.default_rng(11)


def load(path, af=None):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, 'x.f32')
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', path] + (['-af', af] if af else []) + ['-ac', '2', '-ar', str(SR), '-f', 'f32le', f]
        subprocess.run(cmd, check=True)
        return np.fromfile(f, dtype=np.float32).reshape(-1, 2).astype(np.float64)


def db(x): return 10 ** (x / 20)


def place(bus, sig, at, gain=1.0):
    i = int(round(at * SR)); n = min(len(sig), N - i)
    if n > 0: bus[i:i + n] += sig[:n] * gain


def envelope(points):
    ts = np.array([p[0] for p in points]); gs = np.array([p[1] for p in points])
    return db(np.interp(t_axis, ts, gs))[:, None]


def ft(f): return f + VO_AT + (GAP if f >= GAP_AT else 0)


# ── narration ──
VO_CHAIN = ('highpass=f=85,equalizer=f=220:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1.0:g=3,'
            'equalizer=f=9000:t=h:w=0.7:g=2,acompressor=threshold=-24dB:ratio=3:attack=6:release=90:makeup=4,'
            'loudnorm=I=-15:TP=-2:LRA=7')
vo = load(os.path.join(A, 'vo.mp3'), VO_CHAIN)
voice = np.zeros((N, 2)); k = int(GAP_AT * SR)
place(voice, vo[:k], VO_AT); place(voice, vo[k:], VO_AT + GAP_AT + GAP)
SPEECH = [(0.0, 3.61), (4.06, 9.37), (9.81, 19.31), (19.74, 24.98), (25.39, 34.25), (34.58, 48.81), (49.25, 62.42),
          (62.75, 78.39), (78.70, 85.49), (85.82, 91.99)]
SPEECH = [(ft(a), ft(b)) for a, b in SPEECH]
VO_END = SPEECH[-1][1]

# ── music: percussion bed ducked under the narrator ──
mus = load(os.path.join(A, 'music_percussion.mp3'))[int(0.9 * SR):]
bus = np.zeros((N, 2)); place(bus, mus, 0)
pts = [(0, -4)]
for a, b in SPEECH:
    pts += [(a - .15, pts[-1][1]), (a, -15), (b, -15), (b + .3, -9)]
pts += [(ft(34.25) + .3, -6), (ft(34.58) - .2, -6)]         # OneID pause: music up
pts += [(VO_END + .3, -9), (VO_END + .9, -3), (DUR - 1.4, -3), (DUR - .05, -45), (DUR, -60)]
pts.sort(key=lambda p: p[0])
bus *= envelope(pts)

# ── SFX ──
def noise(n): return rng.standard_normal(n)


def lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); acc = 0.0
    for i in range(len(x)): acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y


def st(y): return np.stack([y, y], 1)


def click(level=-14):
    n = int(.03 * SR); tt = np.arange(n) / SR
    x = noise(n); x = x - lp(x, 1800)
    y = x * np.exp(-tt * 260) + .5 * np.sin(2 * np.pi * 1300 * tt) * np.exp(-tt * 180)
    return st(y / np.abs(y).max() * db(level))


def key(level=-22):
    n = int(.025 * SR); tt = np.arange(n) / SR
    x = noise(n); x = x - lp(x, 1200 + rng.uniform(-300, 300))
    y = x * np.exp(-tt * 300)
    return st(y / np.abs(y).max() * db(level + rng.uniform(-2, 1)))


def tone(freqs, dur=.18, level=-18, decay=14, gap=.07):
    n = int((dur + gap * len(freqs)) * SR); y = np.zeros(n); tt = np.arange(n) / SR
    for i, f in enumerate(freqs):
        k = tt >= i * gap; u = tt[k] - i * gap
        y[k] += (np.sin(2 * np.pi * f * u) + .25 * np.sin(4 * np.pi * f * u)) * np.exp(-u * decay) * np.minimum(1, u / .004)
    return st(y / np.abs(y).max() * db(level))


def whoosh(d=.4, f0=400, f1=3500, level=-17):
    n = int(d * SR); x = noise(n)
    f = np.geomspace(f0, f1, n); y = np.empty(n); a1 = a2 = 0.0
    for i in range(n):
        c1 = np.exp(-2 * np.pi * f[i] * 1.6 / SR); c2 = np.exp(-2 * np.pi * f[i] / 1.6 / SR)
        a1 = (1 - c1) * x[i] + c1 * a1; a2 = (1 - c2) * x[i] + c2 * a2; y[i] = a1 - a2
    y *= np.sin(np.linspace(0, np.pi, n)) ** 1.6
    return st(y / np.abs(y).max() * db(level))


def hit(level=-9):
    n = int(.9 * SR); tt = np.arange(n) / SR
    f = 42 + 70 * np.exp(-tt * 9); y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 3.5)
    return st(y / np.abs(y).max() * db(level))


GEN = {
    'click': lambda: click(-13), 'key': lambda: key(-21), 'enter': lambda: click(-11),
    'whoosh': lambda: whoosh(.38, level=-18), 'swish': lambda: whoosh(.6, 300, 3000, -14),
    'pop': lambda: tone([880], .12, -19, 30), 'tick': lambda: tone([1760], .06, -24, 60),
    'success': lambda: tone([1046.5, 1568], .5, -15, 7, .1), 'alert': lambda: tone([659.3, 523.3], .35, -17, 9, .14),
    'hit': lambda: hit(-10),
}
OFFS = {'whoosh': -.2, 'swish': -.3}
sfx = np.zeros((N, 2))
for e in json.load(open(os.path.join(OUT, 'events.json'))):
    place(sfx, GEN[e['type']](), e['t'] + OFFS.get(e['type'], 0))

mix = voice + bus + sfx
raw = os.path.join(OUT, 'mix_raw.f32'); mix.astype(np.float32).tofile(raw)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', raw,
                '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.8,volume=-1.5dB', '-ar', str(SR), '-c:a', 'pcm_s16le',
                os.path.join(OUT, 'mix.wav')], check=True)
os.remove(raw)
print('wrote build/mix.wav')
