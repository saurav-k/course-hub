/* Week 2 build M1 - "Function, not picture": a uniform starfield driven by
   a seed. Same seed reproduces the identical canvas; a different seed draws
   a different sample from the same uniform distribution. Every star is one
   evaluation of X(omega): the seed plays omega, the function is fixed.
   Colours come from CSS tokens at draw time; redraws on theme change. */
(function () {
  'use strict';
  pybGarden.mount('build-starfield', function (fig) {
    var canvas = fig.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');
    var seedInput = fig.querySelector('[data-role="seed"]');
    var regen = fig.querySelector('[data-role="regen"]');
    var nInput = fig.querySelector('[data-role="n"]');
    var outSeed = fig.querySelector('[data-out="seed"]');
    var outN = fig.querySelector('[data-out="n"]');
    var outFirst = fig.querySelector('[data-out="first"]');
    var outPrint = fig.querySelector('[data-out="print"]');

    function params() {
      return {
        seed: Math.max(0, Math.floor(+seedInput.value || 0)) >>> 0,
        n: Math.max(1, Math.floor(+nInput.value || 1))
      };
    }

    function render() {
      var p = params();
      var rng = pybGarden.makeRng(p.seed);
      var W = canvas.width, H = canvas.height;
      var ink = pybGarden.tokenHex('--ink');
      var faint = pybGarden.tokenHex('--ink-faint');
      var accent = pybGarden.tokenHex('--accent-2');

      ctx.fillStyle = pybGarden.tokenHex('--surface');
      ctx.fillRect(0, 0, W, H);

      var h = 0, first = '', x, y, xi, yi;
      for (var i = 0; i < p.n; i++) {
        x = rng.uniform() * W;
        y = rng.uniform() * H;
        xi = Math.round(x * 10); yi = Math.round(y * 10);
        h = ((h * 31) + xi + yi) | 0;
        if (i < 3) first += '(' + pybGarden.fmt(x, 0) + ', ' + pybGarden.fmt(y, 0) + ') ';
        ctx.fillStyle = pybGarden.alpha(faint, 0.9);
        ctx.fillRect(x, y, 1.6, 1.6);
      }

      outSeed.textContent = p.seed;
      outN.textContent = p.n;
      outFirst.textContent = first;
      /* The print: a checksum of every drawn position. Identical under the
         same seed and settings, different otherwise - X as a function,
         physically verifiable without trusting your eyes. */
      outPrint.textContent = (h >>> 0).toString(16).toUpperCase();
      ctx.strokeStyle = pybGarden.alpha(ink, 0.25);
      ctx.strokeRect(0.5, 0.5, W - 1, H - 1);
      void accent;
    }

    seedInput.addEventListener('change', render);
    regen.addEventListener('click', function () {
      seedInput.value = (Math.floor(Math.random() * 90000) + 1);
      render();
    });
    nInput.addEventListener('input', render);

    render();
    pybGarden.wireTheme(render);
  });
})();
