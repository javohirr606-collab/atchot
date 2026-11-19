// Shared helpers for reel.html and wide.html: easing, cached style setters, frame lookup, captions.
(() => {
  const FPS = 30, NFRAMES = 7721;
  const clamp01 = x => x < 0 ? 0 : x > 1 ? 1 : x;
  const H = {
    FPS,
    $: s => document.querySelector(s),
    clamp01,
    prog: (t, t0, d) => d <= 0 ? (t >= t0 ? 1 : 0) : clamp01((t - t0) / d),
    easeOut: x => 1 - Math.pow(1 - x, 3),
    easeIn: x => x * x * x,
    easeInOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    back: x => { const c1 = 1.7, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
    lerp: (a, b, k) => a + (b - a) * k,
    set(el, p, v) { const c = el.__c || (el.__c = {}); if (c[p] !== v) { c[p] = v; el.style[p] = v; } },
    pending: [],
    setSrc(img, src) { if (img.__src === src) return; img.__src = src; img.src = src; H.pending.push(img.decode().catch(() => {})); },
    frame(s) { const n = Math.min(NFRAMES, Math.max(1, Math.round(s * FPS) + 1)); return `frames/${String(n).padStart(5, '0')}.jpg`; },
    html(el, s) { if (el.__h !== s) { el.__h = s; el.innerHTML = s; } },
  };
  // envelope 0→1→0 for an element shown between t0 and t1 with in/out durations
  H.env = (t, t0, t1, di = .3, do_ = .25) => t < t0 || t > t1 ? 0 : Math.min(H.easeOut(H.prog(t, t0, di)), 1 - H.easeIn(H.prog(t, t1 - do_, do_)));

  // speech item active at t (with a small tail), and its source time
  H.speechAt = (items, t, tail = .45) => {
    for (const it of items) { const d = it.b - it.a; if (t >= it.t - .05 && t <= it.t + d + tail) return { it, src: it.a + (t - it.t) }; }
    return null;
  };
  // caption chunk for a speech item at source time src
  H.chunkAt = (chunks, it, src) => {
    const from = Math.max(it.a - .05, it.subFrom ?? -1), to = Math.min(it.b, it.subTo ?? 1e9);
    let best = null;
    for (const c of chunks) {
      if (c.s < from || c.s > to) continue;
      const words = c.words.filter(w => w.s >= it.a - .05 && w.s <= it.b);
      if (!words.length) continue;
      const lastW = words[words.length - 1].s;
      let end = Math.min(c.e, it.b + .25, to + .3);
      if (end - lastW > 1.1) end = lastW + .8;
      if (c.last || c.e > it.b) end = Math.min(it.b, c.e) + .35;
      if (src >= words[0].s - .08 && src < end) best = { c, words, s0: words[0].s };
    }
    return best;
  };
  // longer lines for the 16:9 transcript: merge consecutive chunks of one bite up to `max` characters
  H.lines = (chunks, it, max = 34) => {
    const out = [];
    for (const c of chunks) {
      const words = c.words.filter(w => w.s >= it.a - .05 && w.s <= it.b);
      if (!words.length) continue;
      const txt = words.map(w => w.w).join(' ');
      const prev = out[out.length - 1];
      if (prev && !/[.?!:]$/.test(prev.txt) && prev.txt.length + 1 + txt.length <= max && c.s - prev.end < .9) {
        prev.words.push(...words); prev.txt += ' ' + txt; prev.end = c.e;
      } else out.push({ s: words[0].s, end: c.e, words: [...words], txt });
    }
    return out;
  };
  H.wordsHTML = (words, src, opts = {}) => {
    let cur = -1; words.forEach((w, i) => { if (w.s <= src + .02) cur = i; });
    return words.map((w, i) => {
      const said = i <= cur, now = i === cur && opts.pill !== false;
      const cls = ['w', said ? 'said' : 'todo', now ? 'now' : '', w.hi && said ? 'hi' : ''].join(' ');
      return `<span class="${cls}">${w.w}</span>`;
    }).join(' ');
  };
  window.H = H;
})();
