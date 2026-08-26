/* Week 2 build - joints and marginals at the edges.
   Splats are a bivariate normal pair (X, Y) with independent sigmas on each
   axis and a correlation slider rho. The main plate shows the joint; the
   right edge histogram is the marginal of X, the top edge the marginal of
   Y. Moving rho tilts the ellipse and leaves both edge histograms
   unchanged: marginals do not determine dependence.
   Sampling with correlation: X = sx Z1, Y = sy (rho Z1 + sqrt(1-rho^2) Z2).
   Colours from CSS tokens at draw time; redraws on theme change. */
(function () {
  'use strict';
  pybGarden.mount('build-marginals', function (fig) {
    var canvas = fig.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');
    var seedInput = fig.querySelector('[data-role="seed"]');
    var regen = fig.querySelector('[data-role="regen"]');
    var sxInput = fig.querySelector('[data-role="sx"]');
    var syInput = fig.querySelector('[data-role="sy"]');
    var rhoInput = fig.querySelector('[data-role="rho"]');
    var nInput = fig.querySelector('[data-role="n"]');
    var outRho = fig.querySelector('[data-out="rho"]');
    var outCorr = fig.querySelector('[data-out="corr"]');

    var sprite = document.createElement('canvas');
    var SPR = 56;
    function paintSprite() {
      sprite.width = SPR; sprite.height = SPR;
      var sctx = sprite.getContext('2d');
      var g = sctx.createRadialGradient(SPR / 2, SPR / 2, 0, SPR / 2, SPR / 2, SPR / 2);
      g.addColorStop(0, pybGarden.alpha(pybGarden.tokenHex('--chart-plum'), 0.5));
      g.addColorStop(1, pybGarden.alpha(pybGarden.tokenHex('--chart-plum'), 0));
      sctx.fillStyle = g;
      sctx.fillRect(0, 0, SPR, SPR);
    }

    function render() {
      var seed = Math.max(0, Math.floor(+seedInput.value || 0)) >>> 0;
      var sx = Math.min(120, Math.max(10, +sxInput.value || 60));
      var sy = Math.min(120, Math.max(10, +syInput.value || 20));
      var rho = Math.min(0.95, Math.max(-0.95, +rhoInput.value || 0));
      var n = Math.min(2500, Math.max(100, Math.floor(+nInput.value || 900)));
      var rng = pybGarden.makeRng(seed);
      var W = canvas.width, H = canvas.height;
      var line = pybGarden.tokenHex('--line');
      var barCol = pybGarden.tokenHex('--accent-2');

      ctx.fillStyle = pybGarden.tokenHex('--surface');
      ctx.fillRect(0, 0, W, H);

      /* layout: square joint plate bottom-left, right strip for X, top strip for Y */
      var topH = 96, rightW = 116, gap = 10;
      var px0 = 14, py0 = topH + gap;
      var pw = W - rightW - gap - px0;
      var ph = H - py0 - 14;
      var RANGE = 300;

      var xs = new Array(n), ys = new Array(n);
      var sumx = 0, sumy = 0;
      for (var i = 0; i < n; i++) {
        var z1 = rng.normal(), z2 = rng.normal();
        var xv = sx * z1;
        var yv = sy * (rho * z1 + Math.sqrt(1 - rho * rho) * z2);
        xs[i] = xv; ys[i] = yv;
        sumx += xv; sumy += yv;
        var ux = px0 + pw / 2 + (xv / RANGE) * (pw / 2 - 6);
        var uy = py0 + ph / 2 - (yv / RANGE) * (ph / 2 - 6);
        if (ux < px0 - SPR || ux > px0 + pw + SPR || uy < py0 - SPR || uy > py0 + ph + SPR) continue;
        ctx.drawImage(sprite, ux - SPR / 2, uy - SPR / 2);
      }
      ctx.strokeStyle = pybGarden.alpha(line, 0.9);
      ctx.strokeRect(px0 + 0.5, py0 + 0.5, pw - 1, ph - 1);

      /* marginal histograms: x along the bottom-right strip, y along the top */
      var BW = 15;
      var nb = Math.ceil((2 * RANGE) / BW);
      var cx_ = new Array(nb).fill(0), cy_ = new Array(nb).fill(0);
      for (var j = 0; j < n; j++) {
        var bx = Math.floor((xs[j] + RANGE) / BW);
        var by = Math.floor((ys[j] + RANGE) / BW);
        if (bx >= 0 && bx < nb) cx_[bx]++;
        if (by >= 0 && by < nb) cy_[by]++;
      }
      var mx = Math.max.apply(null, cx_), my = Math.max.apply(null, cy_);
      var meanx = sumx / n, meany = sumy / n;
      var sxx = 0, syy = 0, sxy = 0;
      for (var k = 0; k < n; k++) {
        sxx += (xs[k] - meanx) * (xs[k] - meanx);
        syy += (ys[k] - meany) * (ys[k] - meany);
        sxy += (xs[k] - meanx) * (ys[k] - meany);
      }
      var sampleRho = sxy / Math.sqrt(sxx * syy);

      /* X marginal: vertical bars in the right strip */
      var hx0 = px0 + pw + gap, hw = W - hx0 - 8;
      ctx.fillStyle = pybGarden.alpha(barCol, 0.55);
      for (var b1 = 0; b1 < nb; b1++) {
        if (!cx_[b1]) continue;
        var bh = (cx_[b1] / mx) * (ph - 10);
        ctx.fillRect(hx0 + 4, py0 + ph - bh, hw - 8, bh);
      }
      ctx.strokeRect(hx0 + 3.5, py0 + 0.5, hw - 7, ph - 1);

      /* Y marginal: horizontal bars across the top strip */
      var hy1 = topH, hy0t = 12;
      ctx.fillStyle = pybGarden.alpha(barCol, 0.55);
      for (var b2 = 0; b2 < nb; b2++) {
        if (!cy_[b2]) continue;
        var bwid = (cy_[b2] / my) * (pw - 10);
        ctx.fillRect(px0 + 4, hy1 - (b2 + 1) * ((hy1 - hy0t) / nb),
                     bwid, Math.max(1, (hy1 - hy0t) / nb - 1));
      }

      outRho.textContent = pybGarden.fmt(rho, 2);
      outCorr.textContent = pybGarden.fmt(sampleRho, 2);
    }

    seedInput.addEventListener('change', render);
    regen.addEventListener('click', function () {
      seedInput.value = String(Math.floor(Math.random() * 90000) + 1);
      render();
    });
    [sxInput, syInput, rhoInput, nInput].forEach(function (el) {
      el.addEventListener('input', render);
    });

    paintSprite();
    render();
    var rerender = render;
    pybGarden.wireTheme(function () { paintSprite(); rerender(); });
  });
})();
