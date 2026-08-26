/* Week 2 build - PMF, Bernoulli atoms and binomial counts.
   n dots land uniformly on a grid of m equal cells. "Dot i landed in this
   cell" is a Bernoulli(p) indicator with p = 1/m, so the number of dots in
   one cell is Binomial(n, p). The histogram over cells (how many cells hold
   k dots) is overlaid with the expected-count curve m * P(X=k), computed
   with the multiplicative loop for C(n,k) - never factorials, which
   overflow past 171!. The readout reports total variation distance between
   the observed cell-count distribution and the binomial law.
   Colours from CSS tokens at draw time; redraws on theme change. */
(function () {
  'use strict';
  pybGarden.mount('build-pmf', function (fig) {
    var canvas = fig.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');
    var seedInput = fig.querySelector('[data-role="seed"]');
    var regen = fig.querySelector('[data-role="regen"]');
    var nInput = fig.querySelector('[data-role="n"]');
    var gridInput = fig.querySelector('[data-role="grid"]');
    var outN = fig.querySelector('[data-out="n"]');
    var outP = fig.querySelector('[data-out="p"]');
    var outMean = fig.querySelector('[data-out="mean"]');
    var outTV = fig.querySelector('[data-out="tv"]');

    function choose(n, k) {
      /* multiplicative loop: C(n,k) without factorials */
      if (k < 0 || k > n) return 0;
      var r = 1;
      for (var i = 1; i <= k; i++) r = r * (n - k + i) / i;
      return r;
    }

    function binomialPmf(n, p, k) {
      return choose(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k);
    }

    function render() {
      var seed = Math.max(0, Math.floor(+seedInput.value || 0)) >>> 0;
      var n = Math.min(20000, Math.max(10, Math.floor(+nInput.value || 100)));
      var g = Math.floor(+gridInput.value || 8);
      var rng = pybGarden.makeRng(seed);
      var W = canvas.width, H = canvas.height;
      var ink = pybGarden.tokenHex('--ink');
      var line = pybGarden.tokenHex('--line');
      var dotCol = pybGarden.tokenHex('--accent-2');
      var barCol = pybGarden.tokenHex('--prob');
      var stickCol = pybGarden.tokenHex('--gold');

      /* left panel: the placement itself, gridded */
      var plotW = Math.floor(W * 0.52), pad = 8;
      var cellW = (plotW - pad * 2) / g, cellH = (H - pad * 2) / g;
      ctx.fillStyle = pybGarden.tokenHex('--surface');
      ctx.fillRect(0, 0, W, H);
      ctx.strokeStyle = pybGarden.alpha(line, 0.9);
      ctx.lineWidth = 1;
      for (var gi = 0; gi <= g; gi++) {
        ctx.beginPath();
        ctx.moveTo(pad + gi * cellW, pad); ctx.lineTo(pad + gi * cellW, H - pad);
        ctx.moveTo(pad, pad + gi * cellH); ctx.lineTo(plotW - pad, pad + gi * cellH);
        ctx.stroke();
      }
      var counts = new Array(g * g).fill(0);
      var pCell = 1 / (g * g);
      for (var d = 0; d < n; d++) {
        var x = rng.uniform() * (plotW - pad * 2);
        var y = rng.uniform() * (H - pad * 2);
        var cx = Math.min(g - 1, Math.floor(x / cellW));
        var cy = Math.min(g - 1, Math.floor(y / cellH));
        counts[cy * g + cx]++;
        ctx.fillStyle = pybGarden.alpha(dotCol, 0.85);
        ctx.fillRect(pad + x - 1, pad + y - 1, 2, 2);
      }

      /* right panel: histogram of "dots per cell" across the m=g*g cells,
         with binomial sticks behind the bars */
      var hx0 = plotW + 14, hx1 = W - 12, hy0 = H - 30, hy1 = 26;
      var maxK = 0;
      for (var c = 0; c < counts.length; c++) if (counts[c] > maxK) maxK = counts[c];
      var kMax = Math.min(n, Math.ceil(Math.max(maxK, n * pCell) + 4 * Math.sqrt(n * pCell)));
      var nbins = kMax + 1;
      var bw = (hx1 - hx0) / nbins;
      var cellCounts = {};
      for (var c2 = 0; c2 < counts.length; c2++) {
        cellCounts[counts[c2]] = (cellCounts[counts[c2]] || 0) + 1;
      }
      var m = counts.length;
      var peak = Math.max.apply(null, [1].concat(
        Object.keys(cellCounts).map(function (k) { return cellCounts[k]; }),
        [m * binomialPmf(n, pCell, Math.round(n * pCell))]
      ));
      var yScale = (hy0 - hy1) / peak;

      /* sticks first (behind), then bars */
      ctx.strokeStyle = pybGarden.alpha(stickCol, 0.95);
      ctx.lineWidth = 2;
      for (var k2 = 0; k2 <= kMax; k2++) {
        var pk = binomialPmf(n, pCell, k2) * m;
        var xx = hx0 + (k2 + 0.5) * bw;
        ctx.beginPath();
        ctx.moveTo(xx, hy0); ctx.lineTo(xx, hy0 - pk * yScale);
        ctx.stroke();
      }
      ctx.fillStyle = pybGarden.alpha(barCol, 0.55);
      for (var k3 = 0; k3 <= kMax; k3++) {
        var obs = cellCounts[k3] || 0;
        if (!obs) continue;
        var bh = obs * yScale;
        ctx.fillRect(hx0 + k3 * bw + 1, hy0 - bh, Math.max(1, bw - 2), bh);
      }

      /* axes and labels */
      ctx.strokeStyle = pybGarden.alpha(ink, 0.5);
      ctx.beginPath(); ctx.moveTo(hx0, hy0); ctx.lineTo(hx1, hy0); ctx.stroke();
      ctx.fillStyle = pybGarden.alpha(ink, 0.85);
      ctx.font = '11px ui-monospace, monospace';
      for (var t = 0; t <= kMax; t += Math.max(1, Math.round(kMax / 6))) {
        ctx.fillText(String(t), hx0 + (t + 0.5) * bw - 4, hy0 + 14);
      }
      ctx.fillText('dots in a cell (k)', hx0, H - 4);

      /* readout: empirical mean count vs theory n*p, TV distance of the
         cell-count distribution from the binomial */
      var sum = 0;
      for (var c3 = 0; c3 < counts.length; c3++) sum += counts[c3];
      var empMean = sum / m;
      var tv = 0;
      for (var k4 = 0; k4 <= kMax; k4++) {
        tv += Math.abs((cellCounts[k4] || 0) / m - binomialPmf(n, pCell, k4));
      }
      tv /= 2;

      outN.textContent = n + ' dots, ' + m + ' cells';
      outP.textContent = pybGarden.fmt(pCell, 4);
      outMean.textContent = pybGarden.fmt(empMean, 2) + ' vs ' + pybGarden.fmt(n * pCell, 2);
      outTV.textContent = pybGarden.fmt(tv, 3);
    }

    seedInput.addEventListener('change', render);
    regen.addEventListener('click', function () {
      seedInput.value = String(Math.floor(Math.random() * 90000) + 1);
      render();
    });
    nInput.addEventListener('input', render);
    gridInput.addEventListener('change', render);

    render();
    pybGarden.wireTheme(render);
  });
})();
