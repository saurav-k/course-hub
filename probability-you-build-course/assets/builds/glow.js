/* Week 2 build M2 - "Make it glow": rejection sampling under the radial
   density f(r) = exp(-k r). Proposals are uniform over the canvas square;
   a proposal at radius r is kept with probability f(r). The kept points
   render as a nebula whose brightness is relative density - the PDF made
   visible. The acceptance rate is derived on the lesson page as
   A(k) = (pi/2) (1 - (1+k) e^-k) / k^2 for the unit disc, and the readout
   shows simulated acceptance beside it: derive, code, simulate.
   Colours from CSS tokens at draw time; redraws on theme change. */
(function () {
  'use strict';
  pybGarden.mount('build-glow', function (fig) {
    var canvas = fig.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');
    var seedInput = fig.querySelector('[data-role="seed"]');
    var regen = fig.querySelector('[data-role="regen"]');
    var kInput = fig.querySelector('[data-role="k"]');
    var nInput = fig.querySelector('[data-role="n"]');
    var outK = fig.querySelector('[data-out="k"]');
    var outAcc = fig.querySelector('[data-out="acc"]');
    var outTheory = fig.querySelector('[data-out="theory"]');
    var outTries = fig.querySelector('[data-out="tries"]');

    /* analytic acceptance for unit disc in a 2x2 square, see lesson page */
    function theoryRate(k) {
      return (Math.PI / 2) * (1 - (1 + k) * Math.exp(-k)) / (k * k);
    }

    function render() {
      var seed = Math.max(0, Math.floor(+seedInput.value || 0)) >>> 0;
      var k = Math.min(12, Math.max(0.5, +kInput.value || 3));
      var target = Math.min(8000, Math.max(200, Math.floor(+nInput.value || 4000)));
      var rng = pybGarden.makeRng(seed);
      var W = canvas.width, H = canvas.height;
      var cx = W / 2, cy = H / 2;
      var R = Math.min(W, H) / 2 - 8;          /* screen radius of the unit disc */
      var gold = pybGarden.tokenHex('--gold');

      ctx.fillStyle = pybGarden.tokenHex('--surface');
      ctx.fillRect(0, 0, W, H);

      var kept = 0, tries = 0;
      var MAX_TRIES = 2000000;
      while (kept < target && tries < MAX_TRIES) {
        tries++;
        var x = (rng.uniform() * 2 - 1);
        var y = (rng.uniform() * 2 - 1);       /* uniform in the 2x2 square */
        var r = Math.sqrt(x * x + y * y);
        if (r > 1) continue;                    /* outside the disc: reject */
        if (rng.uniform() < Math.exp(-k * r)) { /* keep with probability f(r) */
          kept++;
          ctx.fillStyle = pybGarden.alpha(gold, 0.75);
          ctx.fillRect(cx + x * R, cy + y * R, 1.4, 1.4);
        }
      }

      outK.textContent = pybGarden.fmt(k, 1);
      var acc = kept / tries;
      outAcc.textContent = pybGarden.fmt(100 * acc, 1) + '%';
      outTheory.textContent = pybGarden.fmt(100 * theoryRate(k), 1) + '%';
      outTries.textContent = tries.toLocaleString();
    }

    seedInput.addEventListener('change', render);
    regen.addEventListener('click', function () {
      seedInput.value = String(Math.floor(Math.random() * 90000) + 1);
      render();
    });
    kInput.addEventListener('input', render);
    nInput.addEventListener('input', render);

    render();
    pybGarden.wireTheme(render);
  });
})();
