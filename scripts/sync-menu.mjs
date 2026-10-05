import { readFileSync, writeFileSync } from 'node:fs';
import assert from 'node:assert/strict';

// Keep the accessible text menu and its reviewed source record together.
const data = JSON.parse(readFileSync('Docs/evidence/menu-transcription.json', 'utf8'));
const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const fragment = data.categories.map(category => {
  assert.match(category.id, /^[a-z-]+$/);
  const rows = category.items.map(([name, ...prices]) => {
    assert.equal(prices.length, category.columns.length, name);
    return `  <tr><th scope="row">${escape(name)}</th>${prices.map(price => `<td>${escape(price)}</td>`).join('')}</tr>`;
  }).join('\n');
  return `<section class="menu-category" id="${category.id}" aria-labelledby="${category.id}-heading">
 <p class="eyebrow">THE PHOTOGRAPHED MENU</p><h2 id="${category.id}-heading">${escape(category.title)}</h2>
 <p class="category-note">${escape(category.note)} <a href="#source-photos">See source photos</a>.</p>
 <table class="menu-table"><caption>${escape(category.title)} · prices as printed; confirm the current menu with the café.</caption><thead><tr><th scope="col">Item</th>${category.columns.map(column => `<th scope="col">${escape(column)}</th>`).join('')}</tr></thead><tbody>
${rows}
 </tbody></table>
 <a class="text-link" href="#menu-categories">Back to categories ↑</a>
</section>`;
}).join('\n');
const filename = 'dist/menu.html';
const html = readFileSync(filename, 'utf8');
const updated = html.replace(/<!-- MENU START -->[\s\S]*?<!-- MENU END -->/, `<!-- MENU START -->\n${fragment}\n<!-- MENU END -->`);
assert.notEqual(html.indexOf('<!-- MENU START -->'), -1, 'Menu markers missing');
if (process.argv.includes('--check')) assert.equal(html, updated, 'Run npm run sync:menu after editing the transcription');
else writeFileSync(filename, updated);
console.log(`${data.categories.reduce((sum, c) => sum + c.items.length, 0)} menu entries synchronized with reviewed photo transcription.`);
