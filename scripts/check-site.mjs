import assert from 'node:assert/strict';
import { readFileSync, existsSync, statSync } from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';

const root = path.resolve('dist');
const html = readFileSync(path.join(root, 'index.html'), 'utf8');
const css = readFileSync(path.join(root, 'style.css'), 'utf8');
const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
assert.equal(new Set(ids).size, ids.length, 'Duplicate IDs');
assert.equal([...html.matchAll(/<h1\b/g)].length, 1, 'Expected one main heading');
assert.match(html, /<html lang="en">/);
assert.match(html, /<main id="main" tabindex="-1">/);
assert.match(html, /<meta name="description" content="[^"]+"/);
assert.match(html, /menu-photo-note/, 'Historical menu needs a visible caution');

let links = 0;
const local = new Set();
for (const match of html.matchAll(/\b(href|src)="([^"]+)"/g)) {
  const [, attr, value] = match;
  if (attr === 'href') links++;
  assert(!/^(javascript:|http:|data:)/i.test(value), `Unsafe URL ${value}`);
  if (value.startsWith('#')) assert(ids.includes(value.slice(1)), `Missing anchor ${value}`);
  else if (!/^(https:|tel:)/.test(value)) local.add(value);
}
for (const match of html.matchAll(/\bsrcset="([^"]+)"/g)) {
  for (const candidate of match[1].split(',')) local.add(candidate.trim().split(/\s+/)[0]);
}
for (const match of css.matchAll(/url\('([^']+)'\)/g)) local.add(match[1]);
for (const file of local) {
  const resolved = path.resolve(root, file);
  assert(resolved.startsWith(root + path.sep), `Outside static directory: ${file}`);
  assert(existsSync(resolved), `Missing asset: ${file}`);
  assert(statSync(resolved).size > 0, `Empty asset: ${file}`);
}
const images = [...html.matchAll(/<img\b[^>]*>/g)];
for (const [index, match] of images.entries()) {
  assert.match(match[0], /\balt="[^"]*"/, `Image ${index} needs alt text`);
  assert.match(match[0], /\bwidth="\d+"/);
  assert.match(match[0], /\bheight="\d+"/);
}
const hero = html.match(/<img[^>]+fetchpriority="high"[^>]*>/)[0];
const preload = html.match(/<link[^>]+rel="preload"[^>]*>/)[0];
assert.equal(hero.match(/srcset="([^"]+)"/)[1], preload.match(/imagesrcset="([^"]+)"/)[1]);
assert.equal(hero.match(/sizes="([^"]+)"/)[1], preload.match(/imagesizes="([^"]+)"/)[1]);
const ldText = html.match(/<script type="application\/ld\+json">(.*?)<\/script>/s)[1];
const ld = JSON.parse(ldText);
assert.equal(ld['@type'], 'CafeOrCoffeeShop');
assert.equal(ld.telephone, '+639171571488');
assert.equal(ld.url, html.match(/rel="canonical" href="([^"]+)"/)[1]);
const hash = createHash('sha256').update(ldText).digest('base64');
assert(html.includes(`'sha256-${hash}'`), 'CSP does not match structured data');
assert.match(css, /\.reveal:focus-within\s*\{\s*opacity:1/);
assert.match(css, /@media\(prefers-reduced-motion:reduce\)/);
assert.match(css, /@media print/);
const robots = readFileSync(path.join(root, 'robots.txt'), 'utf8');
if (html.includes('content="noindex, nofollow"')) assert.match(robots, /Disallow: \//);
else assert.match(robots, /Sitemap: https:\/\//);
assert(existsSync(path.join(root, '404.html')));
assert(!/\b(?:API_KEY|SECRET_KEY|PRIVATE_KEY)\b/.test(html));
const manifest = JSON.parse(readFileSync('.openai/hosting.json', 'utf8'));
assert.equal(manifest.static.directory, 'dist');
console.log(JSON.stringify({ result: 'passed', links, images: images.length, localAssets: local.size, initialHtmlBytes: Buffer.byteLength(html), structuredData: 'valid', audience: html.includes('noindex, nofollow') ? 'private' : 'public' }, null, 2));
