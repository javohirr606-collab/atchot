// Inlines fonts, logo and audio into one self-contained HTML file.
// Usage: node tools/build.mjs [v2]   (optional project folder; default is the first video)
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const sub = process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : '';
const root = join(dirname(fileURLToPath(import.meta.url)), '..', sub);
const src = join(root, 'src');
const dist = join(root, 'dist');
const NAME = 'AIFU_2026-2027_marketing_hisoboti' + (sub ? '_' + sub : '');
mkdirSync(dist, { recursive: true });

const b64 = rel => readFileSync(join(src, rel)).toString('base64');
const MIME = { woff2: 'font/woff2', png: 'image/png' };
const dataUri = rel => `data:${MIME[rel.split('.').pop()]};base64,${b64(rel)}`;

let html = readFileSync(join(src, 'index.html'), 'utf8');

const cache = new Map();
const inline = rel => { if (!cache.has(rel)) cache.set(rel, dataUri(rel)); return cache.get(rel); };
html = html.replace(/url\((assets\/fonts\/[^)]+\.woff2)\)/g, (_, rel) => `url(${inline(rel)})`);
html = html.replace(/src="(assets\/logo\.png)"/g, (_, rel) => `src="${inline(rel)}"`);
html = html.replace('/*@ASSETS@*/', `window.__AIFU_ASSETS__ = { vo: "${b64('assets/vo.mp3')}", music: "${b64('assets/music.mp3')}" };`);
if (/assets\//.test(html.replace(/fetch\('assets\/' \+ k \+ '\.mp3'\)/, ''))) throw new Error('Unresolved asset reference left in output');

const full = join(dist, NAME + '.html');
writeFileSync(full, html);

const mb = s => (Buffer.byteLength(s) / 1048576).toFixed(2) + ' MB';
console.log(`${full}  ${mb(html)}`);
