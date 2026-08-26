/* Week 2 build M5 - "Walks and the bell": sums of independent steps.
   Each walker takes N steps of +1/-1; its endpoint is the sum S_N. The
   main plate draws the trails with the sqrt(t) cone; the bottom strip is
   the endpoint histogram across many fresh walks with the independent-step
   normal prediction N(0, N) laid over it. The momentum toggle makes
   consecutive steps persistent (75 percent repeat), which inflates the
   variance by roughly (1+rho)/(1-rho) = 3 and visibly breaks the bell's
   fit: independence is what the formula was assuming.
   Colours from CSS tokens at draw time; redraws on theme change. */
(function () {
  'use strict';
  pybGarden.mount('build-walks', function (fig) {
    var canvas = fig.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');
    var seedInput = fig.querySelector('[data-role="seed"]');
    var regen = fig.querySelector('[data-role="regen"]');
    var nSteps = fig.querySelector('[data-role="steps"]');
    var walkersInput = fig.querySelector('[data-role="walkers"]');
    var mom = fig.querySelector('[data-role="momentum"]');
    var outN = fig.querySelector('[data-out="n"]');
    var outTheory = fig.querySelector('[data-out="theory"]');
    var outSample = fig.querySelector('[data-out="sample"]');

    function render() {
      var seed = Math.max(0, Math.floor(+seedInput.value || 0)) >>> 0;
      var N = Math.min(400, Math.max(10, Math.floor(+nSteps.value || 200)));
      var M = Math.min(120, Math.max(6, Math.floor(+walkersInput.value || 40)));
      var persist = mom.checked ? 0.75 : 0;
      var rng = pybGarden.makeRng(seed);
      var W = canvas.width, H = canvas.height;
      var ink = pybGarden.tokenHex('--ink');
      var faint = pybGarden.tokenHex('--ink-faint');
      var line = pybGarden.tokenHex('--line');
      var trail = pybGarden.tokenHex('--chart-plum');
      var bellCol = pybGarden.tokenHex('--gold');

      ctx.fillStyle = pybGarden.tokenHex('--surface');
      ctx.fillRect(0, 0, W, H);

      /* ---- main plate: M trails with the sqrt(t) cone ---- */
      var padL = 34, padR = 10, padT = 12;
      var plateH = Math.floor(H * 0.60);
      var yAmp = (plateH - padT * 2) / 2;
      var midY = padT + yAmp;
      var xStep = (W - padL - padR) / N;

      function toX(t) { return padL + t * xStep; }
      function toY(pos) { return midY - pos * (yAmp / Math.max(8, Math.sqrt(N) * 2.4)); }

      /* cone: position sd after t fair steps is sqrt(t) */
      ctx.strokeStyle = pybGarden.alpha(faint, 0.7);
      ctx.lineWidth = 1.4;
      [1, -1].forEach(function (sgn) {
        ctx.beginPath();
        for (var t = 0; t <= N; t += Math.max(1, N / 100)) {
          var yy = midY - sgn * Math.sqrt(t) * (yAmp / (Math.sqrt(N) * 2.4));
          if (t === 0) ctx.moveTo(toX(t), yy); else ctx.lineTo(toX(t), yy);
        }
        ctx.stroke();
      });

      ctx.strokeStyle = pybGarden.alpha(trail, 0.5);
      for (var w = 0; w < M; w++) {
        var pos = 0, lastSign = rng.bernoulli(0.5) === 1 ? 1 : -1;
        ctx.beginPath();
        ctx.moveTo(toX(0), toY(0));
        for (var s = 1; s <= N; s++) {
          var sign;
          if (rng.uniform() < persist) sign = lastSign;
          else { sign = rng.bernoulli(0.5) === 1 ? 1 : -1; lastSign = sign; }
          pos += sign;
          ctx.lineTo(toX(s), toY(pos));
        }
        ctx.stroke();
      }

      ctx.strokeStyle = pybGarden.alpha(line, 0.9);
      ctx.beginPath(); ctx.moveTo(padL, midY); ctx.lineTo(W - padR, midY); ctx.stroke();

      /* ---- endpoint histogram: fresh walks under the same seed ---- */
      var R = 600;
      var hy0 = H - 24, hy1 = plateH + 16;
      var hx0 = padL, hx1 = W - padR;
      var endpoints = new Array(R);
      for (var r = 0; r < R; r++) {
        var sum = 0, ls = rng.bernoulli(0.5) === 1 ? 1 : -1;
        for (var t2 = 0; t2 < N; t2++) {
          if (rng.uniform() < persist) sum += ls;
          else { ls = rng.bernoulli(0.5) === 1 ? 1 : -1; sum += ls; }
        }
        endpoints[r] = sum;
      }
      var meanE = 0;
      for (var e = 0; e < R; e++) meanE += endpoints[e];
      meanE /= R;
      var varE = 0;
      for (var e2 = 0; e2 < R; e2++) { var d = endpoints[e2] - meanE; varE += d * d; }
      varE /= (R - 1);
      var sdE = Math.sqrt(varE);

      var RANGE = Math.ceil(Math.max(2.2 * Math.sqrt(N), 2.4 * sdE));
      var BW = Math.max(2, Math.round(RANGE * 2 / 44));
      var nbins = Math.ceil((2 * RANGE + BW) / BW);
      var counts = new Array(nbins).fill(0);
      for (var e3 = 0; e3 < R; e3++) {
        var b = Math.floor((endpoints[e3] + RANGE) / BW);
        if (b >= 0 && b < nbins) counts[b]++;
      }
      /* theory: N(mean 0, sd sqrt(N)) in density units scaled to the bars */
      var densPeak = 1 / (Math.sqrt(N) * Math.sqrt(2 * Math.PI));
      var obsPeak = Math.max.apply(null, counts) / (R * BW);
      var yScale = (hy0 - hy1) / Math.max(densPeak * 1.06, obsPeak * 1.06);
      ctx.fillStyle = pybGarden.alpha(pybGarden.tokenHex('--prob'), 0.55);
      for (var k = 0; k < nbins; k++) {
        if (!counts[k]) continue;
        var bh = counts[k] / (R * BW) * yScale;
        var bx = hx0 + ((k * BW - RANGE) / (2 * RANGE)) * (hx1 - hx0);
        var bwid = (BW / (2 * RANGE)) * (hx1 - hx0);
        ctx.fillRect(bx + 0.5, hy0 - bh, Math.max(1, bwid - 1), bh);
      }
      ctx.strokeStyle = bellCol; ctx.lineWidth = 2;
      ctx.beginPath();
      for (var q = 0; q <= 240; q++) {
        var xv = -RANGE + (q / 240) * 2 * RANGE;
        var fv = Math.exp(-(xv * xv) / (2 * N)) / (Math.sqrt(N) * Math.sqrt(2 * Math.PI));
        var sx = hx0 + (q / 240) * (hx1 - hx0);
        var sy = hy0 - fv * yScale;
        if (q === 0) ctx.moveTo(sx, sy); else ctx.lineTo(sx, sy);
      }
      ctx.stroke();
      ctx.strokeStyle = pybGarden.alpha(ink, 0.5);
      ctx.beginPath(); ctx.moveTo(hx0, hy0); ctx.lineTo(hx1, hy0); ctx.stroke();
      [-2, -1, 0, 1, 2].forEach(function (m2) {
        var tx = hx0 + ((m2 * Math.sqrt(N) + RANGE) / (2 * RANGE)) * (hx1 - hx0);
        ctx.fillText(m2 === 0 ? '0' : m2 + '\u221a\u004e', tx - 8, H - 8);
      });
      void line;

      outN.textContent = N;
      outTheory.textContent = pybGarden.fmt(Math.sqrt(N), 1);
      outSample.textContent = pybGarden.fmt(sdE, 1);
    }

    seedInput.addEventListener('change', render);
    regen.addEventListener('click', function () {
      seedInput.value = String(Math.floor(Math.random() * 90000) + 1);
      render();
    });
    [nSteps, walkersInput].forEach(function (el) { el.addEventListener('input', render); });
    mom.addEventListener('change', render);

    render();
    pybGarden.wireTheme(render);
  });
})();
