// Renders the reel to MP4 (1080×1920, 30 fps): frames from the page + build/mix.wav.
// Usage: python3 tools/mix.py && node tools/render.mjs [--from 0] [--to 52.5]
// Shot frames are read from src/frames/sNN/ (extract with tools/frames.mjs).
import { createRequire } from 'node:module';
import { execSync, spawn } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { chromium } = createRequire(join(execSync('npm root -g').toString().trim(), 'x.js'))('playwright');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? +process.argv[i + 1] : d; };
const out = join(root, 'build', 'AIFU_Xitoy_malaka_oshirish_reels.mp4');
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
p.on('pageerror', e => console.error('PAGEERROR', e.message));
await p.goto(pathToFileURL(join(root, 'src', 'index.html')).href + '?render');
await p.waitForFunction(() => window.R && document.fonts.status === 'loaded');
const { DUR, FPS } = await p.evaluate(() => ({ DUR: window.R.DUR, FPS: window.R.FPS }));
const from = arg('from', 0), to = Math.min(arg('to', DUR), DUR), total = Math.round((to - from) * FPS);
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
  '-ss', String(from), '-t', String(to - from), '-i', join(root, 'build', 'mix.wav'),
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
  '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', '-shortest', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const t0 = Date.now();
for (let i = 0; i < total; i++) {
  const t = from + i / FPS;
  await p.evaluate(t => window.R.seek(t), t);
  const jpg = await p.screenshot({ type: 'jpeg', quality: 95 });
  if (!ff.stdin.write(jpg)) await new Promise(r => ff.stdin.once('drain', r));
  if (i % (FPS * 5) === 0) console.log(`frame ${i}/${total} t=${t.toFixed(1)} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
ff.stdin.end();
await new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));
await b.close();
console.log('wrote', out);
