import assert from 'node:assert/strict';
import { readFileSync, existsSync, statSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';

const root = path.resolve('dist');
const css = readFileSync(path.join(root, 'style.css'), 'utf8');
const pages = new Map(readdirSync(root).filter(file => file.endsWith('.html')).map(file => [file, readFileSync(path.join(root, file), 'utf8')]));
const idsFor = html => [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
const disclaimer = 'Concept design by Kelvin De Asis. This is an independent proposal created to showcase a potential web redesign for Ragsak Manila Café and is not an official site. All trademarks belong to their respective owners.';
let links = 0, images = 0;
const local = new Set();
for (const [filename, html] of pages) {
  const ids = idsFor(html);
  assert.equal(new Set(ids).size, ids.length, `${filename}: duplicate IDs`);
  assert.equal([...html.matchAll(/<h1\b/g)].length, 1, `${filename}: expected one main heading`);
  assert.match(html, /<html lang="en">/);
  assert.match(html, /<main id="main" tabindex="-1"/);
  assert.match(html, /<meta name="description" content="[^"]+"/);
  assert(html.includes(disclaimer), `${filename}: exact disclaimer missing`);
  assert.match(html, /href="\/?privacy\.html"/, `${filename}: privacy link missing`);
  assert(!/<(?:iframe|form)\b|>\s*Reserve\s*</i.test(html), `${filename}: unexpected embed/form/reservation action`);
  assert(!/ragsak-manila-cafe\.kelvindeasis2323\.chatgpt\.site/.test(html), 'Stale deployment metadata');
  assert(!/\b(?:API_KEY|SECRET_KEY|PRIVATE_KEY)\b/.test(html));
  for (const match of html.matchAll(/\b(href|src)="([^"]+)"/g)) {
    const [, attr, value] = match;
    if (attr === 'href') links++;
    assert(!/^(javascript:|http:|data:)/i.test(value), `Unsafe URL ${value}`);
    if (/^(https:|tel:)/.test(value)) continue;
    const [file, fragment] = value.split('#');
    const normalized = file ? file.replace(/^\//, '') || 'index.html' : filename;
    const target = file === '/' ? 'index.html' : normalized;
    local.add(target);
    if (fragment) assert(idsFor(pages.get(target) || '').includes(fragment), `${filename}: missing anchor ${value}`);
  }
  for (const match of html.matchAll(/\bsrcset="([^"]+)"/g)) {
    for (const candidate of match[1].split(',')) local.add(candidate.trim().split(/\s+/)[0]);
  }
  for (const match of html.matchAll(/<img\b[^>]*>/g)) {
    images++;
    assert.match(match[0], /\balt="[^"]*"/);
    assert.match(match[0], /\bwidth="\d+"/);
    assert.match(match[0], /\bheight="\d+"/);
  }
  const csp = html.match(/http-equiv="Content-Security-Policy" content="([^"]+)"/)?.[1];
  assert(csp?.includes("connect-src 'none'") && csp.includes("form-action 'none'"), `${filename}: CSP missing`);
  for (const match of html.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)) {
    JSON.parse(match[1]);
    const hash = createHash('sha256').update(match[1]).digest('base64');
    assert(csp.includes(`'sha256-${hash}'`), `${filename}: CSP structured data hash mismatch`);
  }
}
for (const match of css.matchAll(/url\('([^']+)'\)/g)) local.add(match[1]);
for (const file of local) {
  const resolved = path.resolve(root, file);
  assert(resolved.startsWith(root + path.sep), `Outside static directory: ${file}`);
  assert(existsSync(resolved) && statSync(resolved).size > 0, `Missing/empty asset: ${file}`);
}
const home = pages.get('index.html');
assert(home.includes('href="menu.html"'));
assert(pages.get('menu.html')?.includes('menu-photo-note'), 'Visible photo-price caution missing');
assert(pages.get('privacy.html')?.includes('Cloudflare’s privacy policy'));
const hero = home.match(/<img[^>]+fetchpriority="high"[^>]*>/)?.[0];
const preload = home.match(/<link[^>]+rel="preload"[^>]*>/)?.[0];
assert(hero && preload, 'Hero preload missing');
assert.equal(hero.match(/srcset="([^"]+)"/)[1], preload.match(/imagesrcset="([^"]+)"/)[1]);
assert.equal(hero.match(/sizes="([^"]+)"/)[1], preload.match(/imagesizes="([^"]+)"/)[1]);
assert.match(css, /\.reveal:focus-within\s*\{\s*opacity:1/);
assert.match(css, /@media\(prefers-reduced-motion:reduce\)/);
assert.match(css, /@media print/);
assert.match(readFileSync(path.join(root, 'robots.txt'), 'utf8'), /Disallow: \//);
assert.equal(JSON.parse(readFileSync('.openai/hosting.json', 'utf8')).static.directory, 'dist');
console.log(JSON.stringify({ result:'passed', pages:pages.size, links, images, localAssets:local.size, homepageBytes:Buffer.byteLength(home), audience:'Independent concept; search indexing disabled' }, null, 2));
