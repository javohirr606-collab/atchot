// Stills for review: node tools/shoot.mjs reel 1.2 5 9.5 …  → build/shots/reel_<t>.jpg
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { mkdirSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { chromium } = createRequire(join(execSync('npm root -g').toString().trim(), 'x.js'))('playwright');
const [page, ...times] = process.argv.slice(2);
const size = page === 'wide' ? { width: 1920, height: 1080 } : { width: 1080, height: 1920 };
mkdirSync(join(root, 'build', 'shots'), { recursive: true });
const b = await chromium.launch(); const p = await b.newPage({ viewport: size });
p.on('pageerror', e => console.error('PAGEERROR', e.message)); p.on('console', m => { if (m.type() === 'error') console.error('CONSOLE', m.text()); });
await p.goto(pathToFileURL(join(root, 'src', page + '.html')).href + '?render');
await p.waitForFunction(() => window.R && document.fonts.status === 'loaded');
for (const t of times) {
  await p.evaluate(t => window.R.seek(t), +t);
  await p.screenshot({ path: join(root, 'build', 'shots', `${page}_${t}.jpg`), type: 'jpeg', quality: 85 });
}
await b.close();
