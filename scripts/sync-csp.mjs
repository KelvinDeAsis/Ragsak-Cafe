import { readFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const filename = 'dist/index.html';
const html = readFileSync(filename, 'utf8');
const ld = html.match(/<script type="application\/ld\+json">(.*?)<\/script>/s)?.[1];
if (!ld) throw new Error('Missing local business structured data');
JSON.parse(ld);
const hash = createHash('sha256').update(ld).digest('base64');
const updated = html.replace(/'sha256-[A-Za-z0-9+/=]+'/, `'sha256-${hash}'`);
if (updated === html && !html.includes(`'sha256-${hash}'`)) throw new Error('Missing CSP hash');
if (updated !== html) writeFileSync(filename, updated);
console.log('Structured data CSP hash is up to date.');
