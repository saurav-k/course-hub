/* Probability You Build - Week 2, the Distribution Garden.
   Shared library for every Week 2 build. Loaded from the lesson head with
   defer, before the build script that uses it. Exposes exactly one global,
   window.pybGarden; nothing else leaks.

   Rules this file implements (see BUILDER-SPEC.md):
   - Randomness is seeded: mulberry32 LCG, seed 42 by convention, never
     Math.random(), so two readers see byte-identical canvases.
   - Canvas colours are read from CSS tokens at draw time through a probe
     element and a 1x1 canvas normalisation, never baked in as literals.
   - Every build re-renders when the reader changes mode or palette, via a
     MutationObserver on <html> data-mode / data-palette, and redraws on
     beforeprint / afterprint so paper gets ink-appropriate pixels. */
(function () {
  'use strict';
  if (window.pybGarden) return;

  var TAU = Math.PI * 2;

  /* mulberry32 - a tiny seeded LCG. Same seed, same sequence, forever. */
  function mulberry32(seed) {
    var a = seed >>> 0;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* A seeded generator with the named samplers the garden layers need.
     normal() is Box-Muller with a cached second value and a log(0) guard:
     uniform() can return 0, and ln(0) is -Infinity, so u===0 is rejected. */
  function makeRng(seed) {
    var next = mulberry32(seed);
    var spare = null;
    return {
      next: next,
      uniform: function () { return next(); },
      normal: function () {
        if (spare !== null) { var s = spare; spare = null; return s; }
        var u = next(), v = next();
        while (u === 0) u = next();
        var mag = Math.sqrt(-2 * Math.log(u));
        spare = mag * Math.sin(TAU * v);
        return mag * Math.cos(TAU * v);
      },
      exponential: function (lambda) {
        var u = next();
        while (u === 0) u = next();
        return -Math.log(1 - u) / lambda;
      },
      bernoulli: function (p) { return next() < p ? 1 : 0; }
    };
  }

  /* Colour probe: resolves a CSS custom property to a hex string at draw
     time. The 1x1 canvas round-trip normalises whatever serialization the
     browser hands back (rgb(), oklch(), ...) to #rrggbb. */
  var probe = null;
  var probeCtx = null;
  function tokenHex(name) {
    if (!document.body) return '#888888';
    if (!probe) {
      probe = document.createElement('span');
      probe.style.cssText = 'position:absolute;width:0;height:0;overflow:hidden;';
      document.body.appendChild(probe);
      probeCtx = document.createElement('canvas').getContext('2d');
    }
    probe.style.color = 'var(' + name + ')';
    probeCtx.fillStyle = '#000000';
    probeCtx.fillStyle = getComputedStyle(probe).color;
    return probeCtx.fillStyle;
  }

  /* #rrggbb -> rgba() with the given alpha, for soft splats and fills. */
  function alpha(hex, a) {
    if (hex.charAt(0) !== '#') return hex;
    var h = hex.slice(1);
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    var n = parseInt(h, 16);
    return 'rgba(' + ((n >> 16) & 255) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',' + a + ')';
  }

  /* Wire one render function to every appearance change there is: explicit
     mode/palette writes on <html>, print (where hub.css remaps the tokens),
     and the return trip from print. */
  function wireTheme(render) {
    try {
      new MutationObserver(render).observe(document.documentElement,
        { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
    } catch (e) { /* very old engine: the page still renders once */ }
    window.addEventListener('beforeprint', render);
    window.addEventListener('afterprint', render);
  }

  /* Mount helper: finds the figure, refuses double initialisation, and runs
     init(fig) once. Returns null when the figure is absent or already live. */
  function mount(figureId, init) {
    var fig = document.getElementById(figureId);
    if (!fig || fig.dataset.pybMounted) return null;
    fig.dataset.pybMounted = '1';
    init(fig);
    return fig;
  }

  window.pybGarden = {
    TAU: TAU,
    mulberry32: mulberry32,
    makeRng: makeRng,
    tokenHex: tokenHex,
    alpha: alpha,
    wireTheme: wireTheme,
    mount: mount,
    fmt: function (x, d) { return Number(x).toFixed(d === undefined ? 1 : d); }
  };
})();
