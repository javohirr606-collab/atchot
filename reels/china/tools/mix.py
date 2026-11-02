"""Soundtrack: metro announcement hook (announcer + doors + train), narration, ducked percussion bed, synthesized SFX.
Usage: python3 tools/mix.py   (needs ffmpeg and numpy; writes build/mix.wav)
"""
import os, subprocess, tempfile
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
A = os.path.join(ROOT, 'src', 'assets')
OUT = os.path.join(ROOT, 'build')
os.makedirs(OUT, exist_ok=True)
SR = 48000
DUR = 42.0
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



DROP = 5.6
NA = 7.45            # narration start
VO_CHAIN = ('highpass=f=85,equalizer=f=220:t=q:w=1.2:g=-2,equalizer=f=3200:t=q:w=1.0:g=3,'
            'equalizer=f=9000:t=h:w=0.7:g=2,acompressor=threshold=-24dB:ratio=3:attack=6:release=90:makeup=4,'
            'loudnorm=I=-15:TP=-2:LRA=7')
# station PA: narrower band, short slap from the platform walls
PA_CHAIN = ('highpass=f=230,lowpass=f=6500,equalizer=f=1800:t=q:w=1.0:g=3,'
            'acompressor=threshold=-22dB:ratio=4:attack=4:release=80:makeup=4,'
            'aecho=0.85:0.6:45|95:0.28|0.16,loudnorm=I=-16:TP=-2:LRA=6')

# ── voices ──
voice = np.zeros((N, 2))
ann = load(os.path.join(A, 'vo_announcer.mp3'), PA_CHAIN)
a_end = int(3.40 * SR); b_from = int(4.50 * SR)
place(voice, ann[int(1.0 * SR):a_end], 0.08)         # "Ehtiyot bo'ling, eshiklar yopiladi." (file starts with a throat clear, cut)
place(voice, ann[b_from:], 3.85 - 0.08)               # "Keyingi bekat — Xitoy."  (file 4.58 s → 3.85 s)
nar = load(os.path.join(A, 'vo_narrator.mp3'), VO_CHAIN)
place(voice, nar, NA)
SPEECH = [(0.08, 1.45), (1.68, 4.40), (4.68, 9.68), (9.95, 15.27), (15.50, 20.10), (20.31, 22.68), (22.91, 28.43), (28.60, 29.62), (29.80, 31.74)]
SPEECH = [(a + NA, b + NA) for a, b in SPEECH]
VO_END = SPEECH[-1][1]

# ── hook ambience: station hum, doors, train pulling away ──
bed = np.zeros((N, 2))
n = int(DROP * SR); tt = np.arange(n) / SR
hum = onepole_lp(noise(n), 300) * 5 + .2 * np.sin(2 * np.pi * 50 * tt)
hum *= np.minimum(1, tt / .3) * db(-30)
place(bed, np.stack([hum, hum], 1), 0)
# pneumatic hiss as the doors close, thud when they meet
hn = int(.6 * SR); hiss = sweep_bp(noise(hn), 5000, 1800) * np.exp(-np.arange(hn) / SR * 4.5)
hiss = hiss / np.abs(hiss).max() * db(-22)
place(bed, np.stack([hiss, hiss], 1), 1.47)
place(bed, boom(-16, 90, 45, .45), 2.08)
# train: rumble rising, rail-joint clicks speeding up
rn = int((DROP - 2.1) * SR); rt = np.arange(rn) / SR
rumble = onepole_lp(noise(rn), 140) * 7 * (rt / rt[-1]) ** 1.2 * db(-20)
place(bed, np.stack([rumble, rumble], 1), 2.1)
tclick = 2.35; gap = .5
while tclick < DROP - .15:
    for dt in (0, .11):
        place(bed, boom(-24, 160, 90, .12), tclick + dt)
    tclick += gap; gap = max(.17, gap * .8)
place(bed, whoosh(.45, 300, 2600, -16), 5.0)          # doors open
place(bed, riser(1.2, -17), DROP - 1.2)

def metro_chime(level=-13):
    """Three-tone station chime (bright, soft attack)."""
    out = np.zeros(int(2.2 * SR)); tt = np.arange(len(out)) / SR
    for f, dt in ((1046.5, 0), (830.6, .32), (659.3, .64)):
        k = tt >= dt; u = tt[k] - dt
        out[k] += (np.sin(2 * np.pi * f * u) + .3 * np.sin(4 * np.pi * f * u) + .08 * np.sin(6 * np.pi * f * u)) * np.exp(-u * 3.0) * np.minimum(1, u / .006)
    out /= np.abs(out).max(); out *= db(level)
    return np.stack([out, out * .97], 1)




# ── percussion bed from the drop (its strong downbeat at 3.76 s lands on DROP), ducked under the narrator ──
perc = load(os.path.join(A, 'music_percussion.mp3'))
perc = perc[int(3.76 * SR):]
bus_p = np.zeros((N, 2)); place(bus_p, perc, DROP)
pts = [(0, -80), (DROP - .01, -80), (DROP, -2)]
for a, b in SPEECH:
    pts += [(a - .12, pts[-1][1]), (a, -11), (b, -11), (b + .25, -7)]
pts += [(VO_END + .3, -7), (VO_END + .8, -2), (DUR - 1.2, -2), (DUR - .05, -45), (DUR, -60)]
bus_p *= envelope(sorted(pts, key=lambda p: p[0]))

# ── SFX ──
sfx = np.zeros((N, 2))
place(sfx, boom(-5), DROP)
for tt in (7.458, 12.102, 17.21, 22.783, 26.2, 27.70, 30.213, 33.928, 35.786):
    place(sfx, whoosh(.38, level=-17), tt - .2)
for tt in (14.45, 14.95, 15.55, 30.38, 31.05, 31.95, 32.4, 33.12, 36.05, 37.3):
    place(sfx, pop(-17, 900), tt)
place(sfx, boom(-13, 120, 50, .6), 9.85)              # 15 kunlik
place(sfx, boom(-13, 120, 50, .6), 17.42)             # BYD
place(sfx, boom(-12, 140, 55, .5), 26.75)             # seal stamp
place(sfx, boom(-7), 34.45)                           # $950
place(sfx, metro_chime(-19), 40.3)                    # bookend

mix = voice + bed + bus_p + sfx
raw = os.path.join(OUT, 'mix_raw.f32')
mix.astype(np.float32).tofile(raw)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', raw,
                '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9:linear=false,alimiter=limit=0.8,volume=-2dB',
                '-ar', str(SR), '-c:a', 'pcm_s16le', os.path.join(OUT, 'mix.wav')], check=True)
os.remove(raw)
print('wrote build/mix.wav')
