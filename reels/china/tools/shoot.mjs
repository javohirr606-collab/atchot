// Screenshots of single frames: node tools/shoot.mjs outdir t1 t2 ...
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { chromium } = createRequire(join(execSync('npm root -g').toString().trim(), 'x.js'))('playwright');
const [out, ...ts] = process.argv.slice(2);
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
p.on('pageerror', e => console.error('PAGEERROR', e.message));
await p.goto(pathToFileURL(join(root, 'src', 'index.html')).href + '?render');
await p.waitForFunction(() => window.R && document.fonts.status === 'loaded');
for (const t of ts.map(Number)) { await p.evaluate(t => window.R.seek(t), t); await p.screenshot({ path: `${out}/f${t.toFixed(2).padStart(6, '0')}.jpg`, quality: 80 }); }
await b.close();
