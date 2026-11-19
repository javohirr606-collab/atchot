// Renders one cut to MP4 at 30 fps: frames from the page + build/mix_<cut>.wav.
// Usage: python3 tools/mix.py reel && node tools/render.mjs reel [--from 0] [--to 10]   (reel = 1080×1920, wide = 1920×1080)
// Needs src/frames/ (tools/frames.sh).
import { createRequire } from 'node:module';
import { execSync, spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { chromium } = createRequire(join(execSync('npm root -g').toString().trim(), 'x.js'))('playwright');
const cut = process.argv[2] === 'wide' ? 'wide' : 'reel';
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? +process.argv[i + 1] : d; };
const out = join(root, 'build', cut === 'reel' ? 'AIFU_SIMO_1-kun_reels.mp4' : 'AIFU_SIMO_1-kun_16x9.mp4');
const size = cut === 'wide' ? { width: 1920, height: 1080 } : { width: 1080, height: 1920 };
const b = await chromium.launch(); const p = await b.newPage({ viewport: size });
p.on('pageerror', e => console.error('PAGEERROR', e.message));
await p.goto(pathToFileURL(join(root, 'src', cut + '.html')).href + '?render');
await p.waitForFunction(() => window.R && document.fonts.status === 'loaded');
const { DUR, FPS } = await p.evaluate(() => ({ DUR: window.R.DUR, FPS: window.R.FPS }));
const from = arg('from', 0), to = Math.min(arg('to', DUR), DUR), total = Math.round((to - from) * FPS);
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
  '-ss', String(from), '-t', String(to - from), '-i', join(root, 'build', `mix_${cut}.wav`),
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
  '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', '-shortest', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const t0 = Date.now();
for (let i = 0; i < total; i++) {
  const t = from + i / FPS;
  await p.evaluate(t => window.R.seek(t), t);
  const jpg = await p.screenshot({ type: 'jpeg', quality: 94 });
  if (!ff.stdin.write(jpg)) await new Promise(r => ff.stdin.once('drain', r));
  if (i % (FPS * 5) === 0) console.log(`${cut} frame ${i}/${total} t=${t.toFixed(1)} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
ff.stdin.end();
await new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));
await b.close();
console.log('wrote', out);
