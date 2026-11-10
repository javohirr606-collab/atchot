// Dumps the page's SFX event list (clicks, keys, whooshes…) to build/events.json for tools/mix.py.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { chromium } = createRequire(join(execSync('npm root -g').toString().trim(), 'x.js'))('playwright');
const b = await chromium.launch(); const p = await b.newPage();
await p.goto(pathToFileURL(join(root, 'src', 'index.html')).href + '?render');
await p.waitForFunction(() => window.R);
const ev = await p.evaluate(() => window.R.events());
mkdirSync(join(root, 'build'), { recursive: true });
writeFileSync(join(root, 'build', 'events.json'), JSON.stringify(ev));
console.log(ev.length, 'events');
await b.close();
