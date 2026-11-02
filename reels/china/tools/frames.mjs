// Extracts each shot's source segment as 1080×1920 JPEG frames at 30 fps into src/frames/sNN/.
// Also writes src/frames/counts.js (frames per shot) for the page.
// Usage: node tools/frames.mjs
import { readFileSync, mkdirSync, rmSync, readdirSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const ctx = { window: {} }; vm.runInNewContext(readFileSync(join(root, 'src', 'shots.js'), 'utf8'), ctx);
const { SHOTS } = ctx.window.EDIT;
const counts = {};
SHOTS.forEach((s, i) => {
  const dir = join(root, 'src', 'frames', 's' + String(i).padStart(2, '0'));
  rmSync(dir, { recursive: true, force: true }); mkdirSync(dir, { recursive: true });
  execFileSync('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y', '-ss', String(s.vs), '-i', join(root, 'src', 'assets', 'clips', s.clip + '.mp4'),
    '-t', String(s.t1 - s.t0 + .15), '-vf', 'fps=30,scale=1080:1920:flags=lanczos,setsar=1', '-q:v', '2', join(dir, '%04d.jpg')]);
  counts[i] = readdirSync(dir).length;
  console.log(i, s.clip, s.vs, counts[i]);
});
writeFileSync(join(root, 'src', 'frames', 'counts.js'), 'window.FRAMECOUNT = ' + JSON.stringify(counts) + ';\n');
