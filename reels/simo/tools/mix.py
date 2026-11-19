"""Soundtrack for both cuts: speech from the separated vocal stem, two music beds with ducking, synthesized SFX.
Usage: python3 tools/mix.py reel|wide   (needs node, ffmpeg and numpy; writes build/mix_<cut>.wav)
Edit data (speech placements, scenes) comes from src/edit.js.
"""
import json, os, subprocess, sys, tempfile
import numpy as np

CUT = sys.argv[1] if len(sys.argv) > 1 else 'reel'
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
A = os.path.join(ROOT, 'src', 'assets', 'audio')
OUT = os.path.join(ROOT, 'build')
os.makedirs(OUT, exist_ok=True)
EDIT = json.loads(subprocess.run(['node', '-e', "global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.EDIT))",
                                  os.path.join(ROOT, 'src', 'edit.js')], check=True, capture_output=True, text=True).stdout)
E = EDIT[CUT]
BEAT = EDIT['BEAT']
SR = 48000
DUR = E['DUR']; DROP = E['DROP']; EG_BAND = E['EG_BAND']
N = int(DUR * SR)
t_axis = np.arange(N) / SR
rng = np.random.default_rng(11)


def load(path, af=None, ch=2):
    with tempfile.TemporaryDirectory() as d:
        raw = os.path.join(d, 'x.f32')
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', path]
        if af:
            cmd += ['-af', af]
        cmd += ['-ac', str(ch), '-ar', str(SR), '-f', 'f32le', raw]
        subprocess.run(cmd, check=True)
        return np.fromfile(raw, dtype=np.float32).reshape(-1, ch).astype(np.float64)


def db(x):
    return 10 ** (x / 20)


def place(bus, sig, at, gain=1.0):
    i = int(round(at * SR))
    if i < 0:
        sig = sig[-i:]; i = 0
    n = min(len(sig), N - i)
    if n > 0:
        bus[i:i + n] += sig[:n] * gain


def envelope(points):
    pts = sorted(points, key=lambda p: p[0])
    return db(np.interp(t_axis, [p[0] for p in pts], [p[1] for p in pts]))[:, None]


# ── speech: one processing chain for the whole stem, then each placement levelled to the same loudness ──
chain = ('highpass=f=90,lowpass=f=12500,equalizer=f=240:t=q:w=1.2:g=-2.5,equalizer=f=3200:t=q:w=1.0:g=2.5,'
         'equalizer=f=8500:t=h:w=0.7:g=1.5,acompressor=threshold=-22dB:ratio=2.6:attack=8:release=120:makeup=2')
stem = load(os.path.join(A, 'speech.m4a'), chain, ch=1)[:, 0]
voice = np.zeros((N, 2))
SPEECH = []
for it in E['speech']:
    a, b = it['a'], it['b']
    seg = stem[int(a * SR):int(b * SR)].copy()
    fi, fo = int(.012 * SR), int(.03 * SR)
    seg[:fi] *= np.linspace(0, 1, fi); seg[-fo:] *= np.linspace(1, 0, fo)
    fr = seg[:len(seg) // 960 * 960].reshape(-1, 960)
    rms = np.sqrt((fr ** 2).mean(1)); act = rms[rms > db(-45)]
    level = 20 * np.log10(np.sqrt((act ** 2).mean()) + 1e-9) if len(act) else -30
    g = db(-19 - level)
    place(voice, np.stack([seg, seg], 1) * g, it['t'])
    SPEECH.append((it['t'], it['t'] + (b - a)))
    print(f"{it['id']:6s} t={it['t']:6.2f} {a:7.2f}-{b:7.2f} level {level:6.1f} dB → gain {20*np.log10(g):+5.1f}")


def duck(points_base, under, gap, t_from, t_to):
    """Add ducking breakpoints between t_from and t_to: `under` dB inside speech, `gap` dB elsewhere."""
    pts = [(t_from, gap)]
    for s0, s1 in SPEECH:
        if s1 < t_from or s0 > t_to:
            continue
        pts += [(max(t_from, s0 - .12), gap), (max(t_from, s0), under), (min(t_to, s1), under), (min(t_to, s1 + .3), gap)]
    pts.append((t_to, gap))
    return points_base + pts


# ── bed 1: percussion; its first big hit (3.76 s in the file) lands on the title ──
EG_IN = 36.0 if CUT == 'reel' else 64.6
perc = load(os.path.join(A, 'music_percussion.mp3'))
bus_p = np.zeros((N, 2)); place(bus_p, perc, DROP - 3.76)
pts = duck([], -17, -7, 0.0, EG_IN)
pts = [p for p in pts if p[0] < EG_IN] + [(EG_IN, -17), (EG_IN + .8, -60), (DUR, -60)]
pts = [(t, g - 3 if t < DROP else g) for t, g in pts]
bus_p *= envelope(pts)
bus_p[:int(.02 * SR)] *= np.linspace(0, 1, int(.02 * SR))[:, None]

# ── bed 2: Evergreen for the closing thought; its band entry (16.10 s in the file) lands on EG_BAND ──
eg = load(os.path.join(A, 'music_evergreen.mp3'))
bus_e = np.zeros((N, 2)); place(bus_e, eg, EG_BAND - 16.10)
last_speech = max(s1 for _, s1 in SPEECH)
pts = [(0, -80), (EG_IN - .4, -80)]
pts = duck(pts, -15, -9, EG_IN, EG_BAND)
pts = duck(pts, -12, -6, EG_BAND, last_speech + .1)
pts += [(last_speech + .6, -2), (DUR - 1.6, -2), (DUR - .05, -45), (DUR, -60)]
bus_e *= envelope(pts)

# keep the music at least 13 dB under the speech inside every speech span (the beds are not evenly loud)
def rms_db(x, a, b):
    return 20 * np.log10(np.sqrt((x[int(a * SR):int(b * SR)] ** 2).mean()) + 1e-9)


extra = [(0.0, 0.0)]
for s0, s1 in SPEECH:
    music = bus_p + bus_e
    over = rms_db(music, s0, s1) - (rms_db(voice, s0, s1) - 13)
    if over > 0:
        extra += [(max(0, s0 - .15), 0.0), (s0, -over), (s1, -over), (s1 + .2, 0.0)]
extra.append((DUR, 0.0))
ext = envelope(extra)
bus_p *= ext; bus_e *= ext

# ── SFX ──
sfx = np.zeros((N, 2))


def noise(n):
    return rng.standard_normal(n)


def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y


def sweep_bp(x, f0, f1):
    n = len(x); f = np.geomspace(f0, f1, n)
    lo = np.empty(n); hi = np.empty(n); a1 = a2 = 0.0
    for i in range(n):
        c1 = np.exp(-2 * np.pi * f[i] * 1.6 / SR); c2 = np.exp(-2 * np.pi * f[i] / 1.6 / SR)
        a1 = (1 - c1) * x[i] + c1 * a1; a2 = (1 - c2) * x[i] + c2 * a2
        lo[i] = a1; hi[i] = a2
    return lo - hi


def whoosh(d=.4, f0=350, f1=3200, level=-15):
    n = int(d * SR); y = sweep_bp(noise(n), f0, f1)
    y *= np.sin(np.linspace(0, np.pi, n)) ** 1.6; y /= np.abs(y).max() + 1e-9; y *= db(level)
    p = np.linspace(-.6, .6, n)
    return np.stack([y * np.sqrt((1 - p) / 2) * 1.41, y * np.sqrt((1 + p) / 2) * 1.41], 1)


def boom(level=-6, f0=110, f1=38, d=1.2):
    n = int(d * SR); tt = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-tt * 9); y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 3.2)
    m = int(.03 * SR); y[:m] += onepole_lp(noise(m), 1800) * np.exp(-np.arange(m) / SR * 140) * 3
    y /= np.abs(y).max(); y *= db(level)
    return np.stack([y, y], 1)


def pop(level=-14, f=880):
    n = int(.12 * SR); tt = np.arange(n) / SR
    y = np.sin(2 * np.pi * f * tt * (1 + .6 * np.exp(-tt * 40))) * np.exp(-tt * 38) * db(level)
    return np.stack([y, y], 1)


def tick(level=-20, f=2600, pan=0.0):
    n = int(.05 * SR); tt = np.arange(n) / SR
    y = (np.sin(2 * np.pi * f * tt) * .6 + noise(n) * .4) * np.exp(-tt * 220) * db(level)
    return np.stack([y * (1 - pan), y * (1 + pan)], 1)


def riser(d, level=-17):
    n = int(d * SR); env = np.linspace(0, 1, n) ** 2.4
    y = sweep_bp(noise(n), 300, 7000); y = y / (np.abs(y).max() + 1e-9) * env * db(level)
    y += np.sin(2 * np.pi * np.cumsum(np.geomspace(180, 720, n)) / SR) * env * db(level - 8)
    return np.stack([y, y], 1)


def chime(level=-18):
    n = int(2.6 * SR); tt = np.arange(n) / SR; y = np.zeros(n)
    for f, dt in ((784, 0), (1174.66, .09), (1568, .18)):
        k = tt >= dt; u = tt[k] - dt
        y[k] += (np.sin(2 * np.pi * f * u) * .8 + np.sin(4 * np.pi * f * u) * .15) * np.exp(-u * 2.2)
    y /= np.abs(y).max(); y *= db(level)
    return np.stack([y, y * .96], 1)


W = lambda t, lvl=-16, d=.38: place(sfx, whoosh(d, level=lvl), t - d * .55)

# hook: clock ticks on half beats, light whooshes on the cuts, riser into the title hit
k = 0; tt = .1
while tt < DROP - .15:
    place(sfx, tick(-21 if k % 2 == 0 else -25, 2600 if k % 2 == 0 else 2000, .2 if k % 2 else -.2), tt); k += 1; tt += BEAT / 2
for c in (DROP - 4 * BEAT, DROP - 3 * BEAT, DROP - 2 * BEAT, DROP - BEAT):
    W(c, -22, .3)
place(sfx, riser(1.7, -18), DROP - 1.7)
place(sfx, boom(-6), DROP)
place(sfx, pop(-16, 1200), DROP + .7)

if CUT == 'reel':
    sp = {s['id']: s for s in E['speech']}
    W(4.42, -15, .4)                                           # title out
    for l in E['lower']:
        place(sfx, pop(-19, 990), l['t0'] + .05)
    for c in (12.13, 16.10, 20.65, 21.30, 21.95, 22.65, 23.35, 24.05):
        W(c, -18)
    c540 = 16.10 + (21.28 - 19.20) - .08
    place(sfx, boom(-11, 100, 42, .9), c540)
    for i in range(12):
        place(sfx, tick(-24, 3200), c540 + i * .045)
    place(sfx, pop(-15, 700), c540 + .8)
    t45 = sp['t45']
    for s in (232.26, 233.26):
        ts = t45['t'] + s - t45['a'] - .05
        place(sfx, boom(-13, 120, 50, .5), ts); place(sfx, whoosh(.3, 500, 3500, -18), ts - .15)
    W(25.25, -16)
    for c in (25.45, 26.90, 29.22):
        W(c, -15, .35); place(sfx, boom(-15, 120, 55, .4), c + .05)
    W(36.25, -15, .5)
    for c in (37.75, 38.60, 39.85, 41.25, 41.70, 42.75, 44.05):
        W(c, -24, .45)
    END = 45.30
else:
    scenes = E['scenes']
    W(scenes[1]['t1'] - .05, -15, .4)
    kinds = [s['kind'] for s in scenes]
    for i, s in enumerate(scenes[2:], start=2):
        if s['kind'] != kinds[i - 1] or s['kind'] == 'end':
            place(sfx, whoosh(.55, 250, 2600, -13), s['t0'] - .3)
        if s['kind'] == 'tri' and s.get('chapter'):
            place(sfx, boom(-12, 100, 45, .8), s['t0'] + .08); place(sfx, pop(-16, 760), s['t0'] + .1)
        if s['kind'] == 'tri':
            for c in s['cuts'][1:]:
                W(c, -20, .35)
        if s['kind'] == 'th':
            for w in s['who']:
                place(sfx, pop(-19, 990), w[0] + .18)
            if s['t0'] == 40.40 or kinds[i - 1] == 'th':
                W(s['t0'], -17)
    for x in (44.95, 52.1):
        W(x + .05, -17)
    sp = {s['id']: s for s in E['speech']}
    c540 = sp['n540']['t'] + (21.28 - 19.20) - .08
    place(sfx, boom(-11, 100, 42, .9), c540)
    for i in range(12):
        place(sfx, tick(-24, 3200), c540 + i * .045)
    place(sfx, pop(-15, 700), c540 + .8)
    t45 = sp['t45']
    for s in (232.26, 233.26):
        ts = t45['t'] + s - t45['a'] - .05
        place(sfx, boom(-13, 120, 50, .5), ts)
    END = [s for s in scenes if s['kind'] == 'end'][0]['t0']

place(sfx, riser(1.3, -22), EG_BAND - 1.3)
place(sfx, boom(-15, 90, 40, 1.0), EG_BAND)
place(sfx, boom(-10, 100, 42, 1.0), END + .3)
place(sfx, chime(-19), END + .5)
place(sfx, pop(-16, 760), END + .98)

mix = voice + bus_p + bus_e + sfx
if os.environ.get('DEBUG'):
    for a, b in [(0.2, 2.4), (4.6, 6.4), (16.2, 18.0), (22.0, 25.0), (29.3, 36.0), (37.0, 41.4), (41.7, 45.0), (46, 49)]:
        r = lambda x: 20 * np.log10(np.sqrt((x[int(a * SR):int(b * SR)] ** 2).mean()) + 1e-9)
        print(f'{a:5.1f}-{b:5.1f} voice {r(voice):6.1f} perc {r(bus_p):6.1f} eg {r(bus_e):6.1f} sfx {r(sfx):6.1f}')
raw = os.path.join(OUT, f'mix_{CUT}_raw.f32')
mix.astype(np.float32).tofile(raw)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', raw,
                '-af', 'loudnorm=I=-14:TP=-1.5:LRA=9:linear=false,alimiter=limit=0.84,volume=-1.5dB',
                '-ar', str(SR), '-c:a', 'pcm_s16le', os.path.join(OUT, f'mix_{CUT}.wav')], check=True)
os.remove(raw)
print(f'wrote build/mix_{CUT}.wav')
