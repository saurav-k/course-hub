/* Week 2 build M3 - "Variance you can see": normal splats by Box-Muller.
   Each splat's centre offset is (Z1, Z2) sigma for two independent standard
   normals Z; the cloud IS the variance. Below the plate, a histogram of the
   x-offsets is drawn in density units with the theoretical N(0, sigma^2)
   curve over it - bars and curve move together when the slider moves, which
   is the whole point. Readout compares sample mean and sample variance
   against 0 and sigma^2 within the tolerance stated in the figcaption.
   Colours from CSS tokens at draw time; redraws on theme change. */
(function () {
  'use strict';
  pybGarden.mount('build-splats', function (fig) {
    var canvas = fig.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');
    var seedInput = fig.querySelector('[data-role="seed"]');
    var regen = fig.querySelector('[data-role="regen"]');
    var sigInput = fig.querySelector('[data-role="sigma"]');
    var nInput = fig.querySelector('[data-role="n"]');
    var outSig = fig.querySelector('[data-out="sigma"]');
    var outMean = fig.querySelector('[data-out="mean"]');
    var outVar = fig.querySelector('[data-out="var"]');
    var outDrift = fig.querySelector('[data-out="drift"]');

    /* one soft splat sprite, re-rendered per theme so its colour follows */
    var sprite = document.createElement('canvas');
    var SPR = 64;
    function paintSprite() {
      sprite.width = SPR; sprite.height = SPR;
      var sctx = sprite.getContext('2d');
      var g = sctx.createRadialGradient(SPR / 2, SPR / 2, 0, SPR / 2, SPR / 2, SPR / 2);
      g.addColorStop(0, pybGarden.alpha(pybGarden.tokenHex('--accent-2'), 0.5));
      g.addColorStop(1, pybGarden.alpha(pybGarden.tokenHex('--accent-2'), 0));
      sctx.fillStyle = g;
      sctx.fillRect(0, 0, SPR, SPR);
    }

    function render() {
      var seed = Math.max(0, Math.floor(+seedInput.value || 0)) >>> 0;
      var sig = Math.min(120, Math.max(5, +sigInput.value || 40));
      var n = Math.min(4000, Math.max(50, Math.floor(+nInput.value || 600)));
      var rng = pybGarden.makeRng(seed);
      var W = canvas.width, H = canvas.height;
      var ink = pybGarden.tokenHex('--ink');
      var faint = pybGarden.tokenHex('--ink-faint');
      var line = pybGarden.tokenHex('--line');
      var curveCol = pybGarden.tokenHex('--gold');
      var cx = W / 2, plateH = Math.floor(H * 0.62), cy = plateH / 2;

      ctx.fillStyle = pybGarden.tokenHex('--surface');
      ctx.fillRect(0, 0, W, H);

      /* the splat cloud: offsets ARE sigma pixels on screen */
      var xs = new Array(n);
      for (var i = 0; i < n; i++) {
        var zx = rng.normal(), zy = rng.normal();
        xs[i] = zx * sig;
        var px = cx + zx * sig;
        var py = cy + zy * sig;
        if (px < -SPR || px > W + SPR || py < -SPR || py > plateH + SPR) continue;
        ctx.drawImage(sprite, px - SPR / 2, py - SPR / 2);
      }

      /* histogram strip: x-offsets in density units, theory curve on top */
      var hx0 = 20, hx1 = W - 20, hy0 = H - 26, hy1 = plateH + 18;
      var RANGE = 300;                              /* pixels each side */
      var BW = 12;                                  /* bin width in pixels */
      var nbins = Math.ceil((2 * RANGE) / BW);
      var counts = new Array(nbins).fill(0);
      var mean = 0;
      for (var j = 0; j < n; j++) {
        mean += xs[j];
        var b = Math.floor((xs[j] + RANGE) / BW);
        if (b >= 0 && b < nbins) counts[b]++;
      }
      mean /= n;
      var vari = 0;
      for (var j2 = 0; j2 < n; j2++) { var d = xs[j2] - mean; vari += d * d; }
      vari /= (n - 1);

      /* density scaling: bar height proportional to count/(n*bw) */
      var densMax = 1 / (sig * Math.sqrt(2 * Math.PI));  /* peak of N(0,sig^2) */
      var yScale = (hy0 - hy1) / (densMax * 1.08);
      ctx.fillStyle = pybGarden.alpha(pybGarden.tokenHex('--prob'), 0.55);
      for (var k = 0; k < nbins; k++) {
        if (!counts[k]) continue;
        var dens = counts[k] / (n * BW);
        var bh = dens * yScale;
        ctx.fillRect(hx0 + (k * BW + RANGE) * ((hx1 - hx0) / (2 * RANGE)),
                     hy0 - bh,
                     Math.max(1, (BW - 1) * ((hx1 - hx0) / (2 * RANGE))),
                     bh);
      }
      /* theory curve N(0, sigma^2) in the same units */
      ctx.strokeStyle = curveCol; ctx.lineWidth = 2.2;
      ctx.beginPath();
      for (var s = 0; s <= 300; s++) {
        var xv = -RANGE + (s / 300) * 2 * RANGE;
        var fv = Math.exp(-(xv * xv) / (2 * sig * sig)) / (sig * Math.sqrt(2 * Math.PI));
        var sx = hx0 + (s / 300) * (hx1 - hx0);
        var sy = hy0 - fv * yScale;
        if (s === 0) ctx.moveTo(sx, sy); else ctx.lineTo(sx, sy);
      }
      ctx.stroke();

      /* axes, sigma marks that slide apart with the slider */
      ctx.strokeStyle = pybGarden.alpha(line, 0.9);
      ctx.beginPath(); ctx.moveTo(hx0, hy0); ctx.lineTo(hx1, hy0); ctx.stroke();
      var toPx = (hx1 - hx0) / (2 * RANGE);
      [-1, 1].forEach(function (m) {
        var mx = cx + m * sig * toPx;
        ctx.strokeStyle = pybGarden.alpha(faint, 0.9);
        ctx.setLineDash([3, 3]);
        ctx.beginPath(); ctx.moveTo(mx, hy1 - 4); ctx.lineTo(mx, hy0); ctx.stroke();
        ctx.setLineDash([]);
      });
      ctx.strokeStyle = pybGarden.alpha(ink, 0.35);
      ctx.beginPath(); ctx.moveTo(hx0, plateH); ctx.lineTo(hx1, plateH); ctx.stroke();
      ctx.fillStyle = pybGarden.alpha(faint, 1);
      ctx.font = '11px ui-monospace, monospace';
      ctx.fillText('-' + sig, hx0 + (RANGE - sig) * toPx - 8, hy0 + 14);
      ctx.fillText('+' + sig, hx0 + (RANGE + sig) * toPx - 6, hy0 + 14);

      outSig.textContent = sig;
      outMean.textContent = pybGarden.fmt(mean, 1);
      outVar.textContent = pybGarden.fmt(vari, 0) + ' vs ' + (sig * sig);
      var drift = Math.abs(vari - sig * sig) / (sig * sig) * 100;
      outDrift.textContent = pybGarden.fmt(drift, 1) + '%';
    }

    seedInput.addEventListener('change', render);
    regen.addEventListener('click', function () {
      seedInput.value = String(Math.floor(Math.random() * 90000) + 1);
      render();
    });
    sigInput.addEventListener('input', render);
    nInput.addEventListener('input', render);

    paintSprite();
    render();
    /* both run again on a mode or palette change: sprite colour first */
    var rerender = render;
    pybGarden.wireTheme(function () { paintSprite(); rerender(); });
  });
})();
