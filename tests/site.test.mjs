import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const source = readFileSync(new URL('../dist/site.js', import.meta.url), 'utf8');
function run(options = {}) {
  const elements = Array.from({ length: 3 }, () => {
    const classes = new Set();
    const events = {};
    return { classes, events, classList: { add: x => classes.add(x), remove: x => classes.delete(x) }, addEventListener: (name, fn) => { events[name] = fn; } };
  });
  const state = { year: { textContent: '2026' }, disconnected: false, unobserved: [], observed: [], motionChange: undefined };
  const mobile = { matches: !!options.mobile, addEventListener: (_, fn) => { state.mobileChange = fn; } };
  const links = ['https://www.instagram.com/ragsak.mnl.cafe/', 'https://www.google.com/maps/dir/?api=1', 'https://ragsak.test/menu.html'].map(href => ({
    href, attributes: {}, setAttribute(key, value) { this.attributes[key] = value; }, removeAttribute(key) { delete this.attributes[key]; }
  }));
  const motion = { matches: !!options.reduce, addEventListener: (_, fn) => { state.motionChange = fn; } };
  class Observer {
    constructor(callback) {
      if (options.constructorFails) throw new Error('Observation unavailable');
      state.callback = callback;
    }
    observe(element) {
      if (options.observeFails && state.observed.length === 1) throw new Error('Observe failed');
      state.observed.push(element);
    }
    unobserve(element) { state.unobserved.push(element); }
    disconnect() { state.disconnected = true; }
  }
  const window = options.noObserver ? {} : { IntersectionObserver: Observer };
  window.location = { origin: 'https://ragsak.test' };
  if (!options.noMatchMedia) window.matchMedia = query => query.includes('prefers-reduced-motion') ? motion : mobile;
  const document = { querySelectorAll: selector => selector === '.reveal' ? elements : links, querySelector: () => state.year };
  vm.runInNewContext(source, { window, document, URL, IntersectionObserver: Observer });
  return Object.assign(state, { elements, links, mobile, hidden: () => elements.filter(e => e.classes.has('reveal-pending')).length });
}

test('Entering the viewport reveals a card and stops observing it', () => {
  const state = run();
  assert.equal(state.hidden(), 3);
  state.callback([{ isIntersecting: false, target: state.elements[0] }]);
  assert.equal(state.hidden(), 3);
  state.callback([{ isIntersecting: true, target: state.elements[0] }]);
  assert.equal(state.hidden(), 2);
  assert.equal(state.unobserved.length, 1);
});
test('Keyboard focus reveals an off-screen card', () => {
  const state = run();
  state.elements[1].events.focusin();
  assert.equal(state.hidden(), 2);
  assert.equal(state.unobserved[0], state.elements[1]);
});
test('Changing reduced-motion preference restores all content', () => {
  const state = run();
  state.motionChange({ matches: true });
  assert.equal(state.hidden(), 0);
  assert.equal(state.disconnected, true);
});
for (const options of [{ reduce: true }, { noObserver: true }, { noMatchMedia: true }, { constructorFails: true }, { observeFails: true }]) {
  test(`Content is readable with ${Object.keys(options)[0]}`, () => {
    const state = run(options);
    assert.equal(state.hidden(), 0);
    assert.equal(state.year.textContent, new Date().getFullYear());
  });
}
test('Desktop external social and map links open safely in a new tab; same-origin links remain unchanged', () => {
  const state = run();
  for (const link of state.links.slice(0, 2)) {
    assert.equal(link.attributes.target, '_blank');
    assert.equal(link.attributes.rel, 'noopener noreferrer');
    assert.equal(link.attributes.title, 'Opens in a new tab');
  }
  assert.deepEqual(state.links[2].attributes, {});
});
test('Mobile links stay in the same tab even with reduced motion', () => {
  const state = run({ mobile:true, reduce:true });
  assert.equal(state.links[0].attributes.target, '_self');
  assert.equal(state.links[1].attributes.target, '_self');
  assert.equal(state.links[0].attributes.title, undefined);
  assert.equal(state.hidden(), 0);
});
test('Targets follow changes in device media queries without intercepting link clicks', () => {
  const state = run();
  state.mobile.matches = true;
  state.mobileChange();
  assert.equal(state.links[0].attributes.target, '_self');
  state.mobile.matches = false;
  state.mobileChange();
  assert.equal(state.links[0].attributes.target, '_blank');
});
