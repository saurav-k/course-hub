/* Week 2 build M4 - "The u-machine": the CDF and inverse-transform
   sampling, made physical. Left: the exponential CDF F(x) = 1 - e^(-lambda x)
   with a draggable u level; its intersection drops onto the x-axis at
   x = F^-1(u) = -ln(1-u)/lambda. Right: exponential rings sampled by exactly
   that transform, with the inspector's ghost ring highlighted.
   The readout shows u, the machine's output x, the theoretical mean 1/lambda,
   and the sample mean of the drawn radii beside it.
   Colours from CSS tokens at draw time; redraws on theme change. */
(function () {
  'use strict';
  pybGarden.mount('build-umachine', function (fig) {
    var canvas = fig.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');
    var seedInput = fig.querySelector('[data-role="seed"]');
    var regen = fig.querySelector('[data-role="regen"]');
    var uInput = fig.querySelector('[data-role="u"]');
    var lamInput = fig.querySelector('[data-role="lam"]');
    var nInput = fig.querySelector('[data-role="n"]');
    var outU = fig.querySelector('[data-out="u"]');
    var outX = fig.querySelector('[data-out="x"]');
    var outMean = fig.querySelector('[data-out="mean"]');
    var outLam = fig.querySelector('[data-out="lam"]');
    var outEMean = fig.querySelector('[data-out="emean"]');

    function render() {
      var seed = Math.max(0, Math.floor(+seedInput.value || 0)) >>> 0;
      var u = (+uInput.value) / 1000;
      var lam = Math.min(30, Math.max(1, +lamInput.value || 8));
      var nRings = Math.min(400, Math.max(10, Math.floor(+nInput.value || 120)));
      var rng = pybGarden.makeRng(seed);
      var W = canvas.width, H = canvas.height;
      var ink = pybGarden.tokenHex('--ink');
      var faint = pybGarden.tokenHex('--ink-faint');
      var line = pybGarden.tokenHex('--line');
      var curve = pybGarden.tokenHex('--accent-2');
      var mark = pybGarden.tokenHex('--gold');
      var ring = pybGarden.tokenHex('--chart-sky');

      ctx.fillStyle = pybGarden.tokenHex('--surface');
      ctx.fillRect(0, 0, W, H);

      /* ---- left panel: CDF with the u rail ---- */
      var padL = 40, padB = 30, padT = 16;
      var plotW = Math.floor(W * 0.46);
      var xmax = 5 / lam;
      function X(x) { return padL + (x / xmax) * (plotW - padL - 12); }
      function Y(p) { return H - padB - p * (H - padB - padT); }

      ctx.strokeStyle = pybGarden.alpha(line, 0.9);
      ctx.lineWidth = 1;
      [0.25, 0.5, 0.75].forEach(function (p) {
        ctx.beginPath(); ctx.moveTo(X(0), Y(p)); ctx.lineTo(plotW - 12, Y(p)); ctx.stroke();
      });
      ctx.strokeStyle = pybGarden.alpha(ink, 0.6);
      ctx.beginPath();
      ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(xmax), Y(0));
      ctx.moveTo(X(0), Y(0)); ctx.lineTo(X(0), Y(1.02));
      ctx.stroke();

      ctx.strokeStyle = curve; ctx.lineWidth = 2.4;
      ctx.beginPath();
      for (var i = 0; i <= 220; i++) {
        var xx = (i / 220) * xmax;
        var yy = 1 - Math.exp(-lam * xx);
        if (i === 0) ctx.moveTo(X(xx), Y(yy)); else ctx.lineTo(X(xx), Y(yy));
      }
      ctx.stroke();

      /* the u level and its inverse image */
      var xq = -Math.log(1 - u) / lam;
      ctx.strokeStyle = mark; ctx.lineWidth = 1.6;
      ctx.setLineDash([5, 4]);
      ctx.beginPath();
      ctx.moveTo(X(0), Y(u)); ctx.lineTo(X(xq), Y(u));
      ctx.lineTo(X(xq), Y(0));
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = mark;
      ctx.beginPath(); ctx.arc(X(xq), Y(0), 4.5, 0, pybGarden.TAU); ctx.fill();

      ctx.fillStyle = pybGarden.alpha(faint, 1);
      ctx.font = '11px ui-monospace, monospace';
      ctx.fillText('u', X(0) - 22, Y(u) + 4);
      ctx.fillText('F(x)', X(0) + 6, Y(1) - 6);
      ctx.fillText('x', X(xmax) - 4, H - padB + 16);
      ctx.fillText(pybGarden.fmt(xmax, 2), X(xmax) - 20, H - padB + 16);

      /* ---- right panel: rings drawn by the same machine ---- */
      var rcx = plotW + (W - plotW) / 2, rcy = H / 2;
      var Rmax = Math.min(W - plotW, H) / 2 - 14;
      var sum = 0;
      for (var r = 0; r < nRings; r++) {
        var rad = rng.exponential(lam);
        var ang = rng.uniform() * pybGarden.TAU;
        sum += rad;
        var px = rad / xmax * Rmax;
        if (px > Rmax) continue;               /* rare far tail off the plate */
        var ghost = Math.abs(rad - xq) < (xmax / 300);
        ctx.strokeStyle = ghost ? mark : pybGarden.alpha(ring, 0.55);
        ctx.lineWidth = ghost ? 2 : 1;
        ctx.beginPath();
        ctx.arc(rcx, rcy, Math.max(px, 0.7), 0, pybGarden.TAU);
        ctx.stroke();
      }
      ctx.strokeStyle = pybGarden.alpha(ink, 0.35);
      ctx.beginPath(); ctx.arc(rcx, rcy, Rmax, 0, pybGarden.TAU); ctx.stroke();

      outLam.textContent = lam;
      outU.textContent = pybGarden.fmt(u, 3);
      outX.textContent = pybGarden.fmt(xq, 3);
      if (outEMean) outEMean.textContent = pybGarden.fmt(1 / lam, 3);
      outMean.textContent = pybGarden.fmt(sum / nRings, 3);
    }

    seedInput.addEventListener('change', render);
    regen.addEventListener('click', function () {
      seedInput.value = String(Math.floor(Math.random() * 90000) + 1);
      render();
    });
    uInput.addEventListener('input', render);
    lamInput.addEventListener('input', render);
    nInput.addEventListener('input', render);

    render();
    pybGarden.wireTheme(render);
  });
})();
