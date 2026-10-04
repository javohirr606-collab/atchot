// Renders the built HTML frame by frame into an MP4 backup copy (1920×1080, 30 fps, AAC).
// Requires: ffmpeg in PATH and Playwright with Chromium (npm i -D playwright, or a global install).
// Usage: node tools/build.mjs && node tools/render-video.mjs [--fps 30] [--from 0] [--to 145]
import { spawn, execSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { writeFileSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const html = join(root, 'dist', 'AIFU_2026-2027_marketing_hisoboti.html');
const out = join(root, 'dist', 'AIFU_2026-2027_marketing_hisoboti.mp4');
const wav = join(root, 'dist', '.mix.wav');
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? +process.argv[i + 1] : d; };
const FPS = arg('fps', 30);

function loadPlaywright() {
  const req = createRequire(join(root, 'package.json'));
  try { return req('playwright'); } catch {}
  const globalRoot = execSync('npm root -g').toString().trim();
  return createRequire(join(globalRoot, 'noop.js'))('playwright');
}
const { chromium } = loadPlaywright();

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.error('page error:', e.message));
await page.goto(pathToFileURL(html).href + '?render');
await page.waitForFunction(() => window.AIFU && window.AIFU.audio().vo > 0 && window.AIFU.audio().music > 0, null, { timeout: 60000 });
const DUR = await page.evaluate(() => window.AIFU.DUR);
const from = arg('from', 0), to = Math.min(arg('to', DUR), DUR);

// 1) soundtrack: narration + ducked music + synthesized effects, mixed offline in the page
const { bytes, sampleRate } = await page.evaluate(() => window.AIFU.renderMix(48000));
const parts = [];
for (let off = 0; off < bytes; off += 4 << 20) parts.push(Buffer.from(await page.evaluate(([o, n]) => window.AIFU.mixChunk(o, n), [off, 4 << 20]), 'base64'));
const pcm = Buffer.concat(parts);
const hdr = Buffer.alloc(44);
hdr.write('RIFF', 0); hdr.writeUInt32LE(36 + pcm.length, 4); hdr.write('WAVE', 8); hdr.write('fmt ', 12);
hdr.writeUInt32LE(16, 16); hdr.writeUInt16LE(1, 20); hdr.writeUInt16LE(2, 22); hdr.writeUInt32LE(sampleRate, 24);
hdr.writeUInt32LE(sampleRate * 4, 28); hdr.writeUInt16LE(4, 32); hdr.writeUInt16LE(16, 34); hdr.write('data', 36); hdr.writeUInt32LE(pcm.length, 40);
writeFileSync(wav, Buffer.concat([hdr, pcm]));
console.log(`soundtrack: ${(pcm.length / 1048576).toFixed(1)} MB PCM`);

// 2) frames piped straight into ffmpeg
const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error',
  '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
  '-ss', String(from), '-t', String(to - from), '-i', wav,
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-tune', 'animation',
  '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-shortest', out], { stdio: ['pipe', 'inherit', 'inherit'] });
const total = Math.round((to - from) * FPS);
const t0 = Date.now();
for (let i = 0; i < total; i++) {
  const t = from + i / FPS;
  await page.evaluate(t => window.AIFU.seek(t), t);
  const png = await page.screenshot({ type: 'png' });
  if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r));
  if (i % (FPS * 10) === 0) console.log(`frame ${i}/${total}  t=${t.toFixed(1)}s  ${((Date.now() - t0) / 1000).toFixed(0)}s elapsed`);
}
ff.stdin.end();
await new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg exited ' + c))));
await browser.close();
rmSync(wav, { force: true });
console.log('wrote', out);
