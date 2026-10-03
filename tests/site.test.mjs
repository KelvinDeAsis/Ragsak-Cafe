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
  if (!options.noMatchMedia) window.matchMedia = () => motion;
  const document = { querySelectorAll: () => elements, querySelector: () => state.year };
  vm.runInNewContext(source, { window, document, IntersectionObserver: Observer });
  return Object.assign(state, { elements, hidden: () => elements.filter(e => e.classes.has('reveal-pending')).length });
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
