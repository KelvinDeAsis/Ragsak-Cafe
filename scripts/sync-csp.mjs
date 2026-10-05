import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';

for (const file of readdirSync('dist').filter(file => file.endsWith('.html'))) {
  const filename = `dist/${file}`;
  const html = readFileSync(filename, 'utf8');
  const hashes = [...html.matchAll(/<script type="application\/ld\+json">(.*?)<\/script>/gs)].map(match => {
    JSON.parse(match[1]);
    return `'sha256-${createHash('sha256').update(match[1]).digest('base64')}'`;
  });
  const updated = html.replace(/script-src 'self'(?: 'sha256-[A-Za-z0-9+/=]+')*/, `script-src 'self'${hashes.length ? ' ' + hashes.join(' ') : ''}`);
  if (updated !== html) writeFileSync(filename, updated);
}
console.log('All HTML content security policies synchronized. No business schema is asserted for this independent concept.');
