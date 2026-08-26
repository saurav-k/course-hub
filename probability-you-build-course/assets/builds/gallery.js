/* Week 2 build M6 - the Distribution Garden, composed.
   One canvas, five independently toggleable layers, each a named random
   variable with its own sampler and its own seeded stream (layer k is fed
   by mulberry32(seed*7919 + k)), so toggling a layer never disturbs the
   samples of another - the piece stays reproducible under inspection.
   Layers: uniform starfield; glow by rejection sampling under exp(-k r);
   normal splats by Box-Muller; walks as sums of steps; exponential rings
   by inverse transform. Gallery variant adds parameter sliders, PNG export
   and a parameter permalink; the live caption names every distribution in
   play - the caption IS the specification.
   Colours from CSS tokens at draw time; redraws on theme change. */
(function () {
  'use strict';
  pybGarden.mount('build-gallery', function (fig) {
    var variant = fig.dataset.garden === 'hub' ? 'hub' : 'gallery';
    var canvas = fig.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');
    var seedInput = fig.querySelector('[data-role="seed"]');
    var regen = fig.querySelector('[data-role="regen"]');
    var tStars = fig.querySelector('[data-layer="stars"]');
    var tGlow = fig.querySelector('[data-layer="glow"]');
    var tSplats = fig.querySelector('[data-layer="splats"]');
    var tWalks = fig.querySelector('[data-layer="walks"]');
    var tRings = fig.querySelector('[data-layer="rings"]');
    var sigInput = fig.querySelector('[data-role="sigma"]');
    var kInput = fig.querySelector('[data-role="k"]');
    var lamInput = fig.querySelector('[data-role="lam"]');
    var exportBtn = fig.querySelector('[data-role="export"]');
    var outSeed = fig.querySelector('[data-out="seed"]');
    var outAcc = fig.querySelector('[data-out="acc"]');
    var outSpec = fig.querySelector('[data-out="spec"]');

    var sprites = {};
    function paintSprites() {
      /* the splat sprite wears --accent-2 so it never reads as glow */
      var c = document.createElement('canvas');
      c.width = 48; c.height = 48;
      var g = c.getContext('2d').createRadialGradient(24, 24, 0, 24, 24, 24);
      g.addColorStop(0, pybGarden.alpha(pybGarden.tokenHex('--accent-2'), 0.5));
      g.addColorStop(1, pybGarden.alpha(pybGarden.tokenHex('--accent-2'), 0));
      c.getContext('2d').fillStyle = g;
      c.getContext('2d').fillRect(0, 0, 48, 48);
      sprites.splat = c;
    }

    function params() {
      return {
        seed: Math.max(0, Math.floor(+seedInput.value || 0)) >>> 0,
        sig: sigInput ? Math.min(90, Math.max(10, +sigInput.value || 35)) : 35,
        k: kInput ? Math.min(8, Math.max(1, +kInput.value || 3)) : 3,
        lam: lamInput ? Math.min(16, Math.max(2, +lamInput.value || 8)) : 8,
        layers: {
          stars: !tStars || tStars.checked,
          glow: !tGlow || tGlow.checked,
          splats: !tSplats || tSplats.checked,
          walks: !tWalks || tWalks.checked,
          rings: !tRings || tRings.checked
        }
      };
    }

    /* restore state from the permalink hash before first render */
    function readHash() {
      if (!location.hash || location.hash.length < 2) return;
      var m;
      if ((m = location.hash.match(/s=(\d+)/))) seedInput.value = m[1];
      if (sigInput && (m = location.hash.match(/sig=(\d+(?:\.\d+)?)/))) sigInput.value = m[1];
      if (kInput && (m = location.hash.match(/k=(\d+(?:\.\d+)?)/))) kInput.value = m[1];
      if (lamInput && (m = location.hash.match(/lam=(\d+(?:\.\d+)?)/))) lamInput.value = m[1];
      if ((m = location.hash.match(/L=([a-z]*)/))) {
        if (tStars) tStars.checked = m[1].indexOf('t') >= 0;
        if (tGlow) tGlow.checked = m[1].indexOf('g') >= 0;
        if (tSplats) tSplats.checked = m[1].indexOf('p') >= 0;
        if (tWalks) tWalks.checked = m[1].indexOf('w') >= 0;
        if (tRings) tRings.checked = m[1].indexOf('r') >= 0;
      }
    }
    var writeTimer = null;
    function writeHash() {
      var p = params();
      var L = (p.layers.stars ? 't' : '') + (p.layers.glow ? 'g' : '') +
              (p.layers.splats ? 'p' : '') + (p.layers.walks ? 'w' : '') +
              (p.layers.rings ? 'r' : '');
      var h = '#s=' + p.seed +
        (sigInput ? '&sig=' + p.sig : '') +
        (kInput ? '&k=' + p.k : '') +
        (lamInput ? '&lam=' + p.lam : '') +
        '&L=' + L;
      if (writeTimer) clearTimeout(writeTimer);
      writeTimer = setTimeout(function () {
        try { history.replaceState(null, '', h); } catch (e) { /* sandboxed */ }
      }, 200);
    }

    function render() {
      var p = params();
      var W = canvas.width, H = canvas.height;

      ctx.fillStyle = pybGarden.tokenHex('--surface');
      ctx.fillRect(0, 0, W, H);

      /* ---- stars: X ~ Uniform over the canvas ---- */
      if (p.layers.stars) {
        var rs = pybGarden.makeRng(p.seed ^ 1);
        for (var i = 0; i < 3000; i++) {
          ctx.fillStyle = pybGarden.alpha(pybGarden.tokenHex('--ink-faint'), 0.75);
          ctx.fillRect(rs.uniform() * W, rs.uniform() * H, 1.5, 1.5);
        }
      }

      /* ---- glow: rejection sampling under f(r) = exp(-k r) ---- */
      var accPct = 0;
      if (p.layers.glow) {
        var rg = pybGarden.makeRng(p.seed ^ 2);
        var gcx = W * 0.30, gcy = H * 0.46, R = Math.min(W, H) * 0.26;
        var kept = 0, tries = 0;
        while (kept < 2600 && tries < 400000) {
          tries++;
          var gx = rg.uniform() * 2 - 1, gy = rg.uniform() * 2 - 1;
          var gr = Math.sqrt(gx * gx + gy * gy);
          if (gr > 1) continue;
          if (rg.uniform() < Math.exp(-p.k * gr)) {
            kept++;
            ctx.fillStyle = pybGarden.alpha(pybGarden.tokenHex('--gold'), 0.7);
            ctx.fillRect(gcx + gx * R, gcy + gy * R, 1.6, 1.6);
          }
        }
        accPct = 100 * kept / tries;
      }

      /* ---- splats: bivariate normal by Box-Muller ---- */
      if (p.layers.splats) {
        var rn = pybGarden.makeRng(p.seed ^ 3);
        var scx = W * 0.67, scy = H * 0.33;
        for (var s = 0; s < 320; s++) {
          var zx = rn.normal() * p.sig, zy = rn.normal() * p.sig;
          ctx.drawImage(sprites.splat, scx + zx * 1.15 - 24, scy + zy * 1.15 - 24);
        }
      }

      /* ---- walks: sums of independent steps ---- */
      if (p.layers.walks) {
        var rw = pybGarden.makeRng(p.seed ^ 4);
        var wx0 = W * 0.05, wx1 = W * 0.56, wy = H * 0.80;
        var amp = H * 0.085, steps = 140;
        ctx.strokeStyle = pybGarden.alpha(pybGarden.tokenHex('--chart-plum'), 0.55);
        ctx.lineWidth = 1;
        for (var w = 0; w < 22; w++) {
          ctx.beginPath();
          ctx.moveTo(wx0, wy);
          var pos = 0;
          for (var t = 1; t <= steps; t++) {
            pos += rw.bernoulli(0.5) === 1 ? 1 : -1;
            ctx.lineTo(wx0 + (wx1 - wx0) * t / steps, wy - pos * (amp / 12));
          }
          ctx.stroke();
        }
      }

      /* ---- rings: exponential radii by inverse transform ---- */
      if (p.layers.rings) {
        var rr = pybGarden.makeRng(p.seed ^ 5);
        var rcx = W * 0.67, rcy = H * 0.71;
        var Rmax = Math.min(W, H) * 0.21;
        var xmax = 4 / p.lam;
        ctx.strokeStyle = pybGarden.alpha(pybGarden.tokenHex('--chart-sky'), 0.5);
        for (var q = 0; q < 80; q++) {
          var rad = rr.exponential(p.lam);
          if (rad > xmax) continue;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.arc(rcx, rcy, Math.max(0.8, rad / xmax * Rmax), 0, pybGarden.TAU);
          ctx.stroke();
        }
      }

      /* ---- readout and the living caption ---- */
      if (outSeed) outSeed.textContent = p.seed;
      if (outAcc) outAcc.textContent = p.layers.glow ? pybGarden.fmt(accPct, 1) + '%' : '-';
      var bits = [];
      if (p.layers.stars) bits.push('3,000 uniform stars');
      if (p.layers.glow) bits.push('keeps 2,600 proposals under exp(-' + p.k + 'r) (acceptance ' + pybGarden.fmt(accPct, 1) + '%)');
      if (p.layers.splats) bits.push('splats 320 normals, sigma ' + p.sig);
      if (p.layers.walks) bits.push('walks 22 agents of 140 steps');
      if (p.layers.rings) bits.push('rings r = -ln(1-u)/' + p.lam);
      if (outSpec) outSpec.textContent = 'This piece draws ' + bits.join(', ') + '. Seed ' + p.seed + '.';
    }

    function refresh() { render(); writeHash(); }

    seedInput.addEventListener('change', refresh);
    regen.addEventListener('click', function () {
      seedInput.value = String(Math.floor(Math.random() * 90000) + 1);
      refresh();
    });
    [tStars, tGlow, tSplats, tWalks, tRings].forEach(function (el) {
      if (el) el.addEventListener('change', refresh);
    });
    [sigInput, kInput, lamInput].forEach(function (el) {
      if (el) el.addEventListener('input', refresh);
    });

    if (exportBtn) {
      exportBtn.addEventListener('click', function () {
        var a = document.createElement('a');
        a.download = 'distribution-garden-seed-' + String(params().seed) + '.png';
        a.href = canvas.toDataURL('image/png');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      });
    }

    /* wire the theme observer BEFORE the first render so a failure later in
       init can never leave the canvas deaf to mode or palette changes */
    paintSprites();
    readHash();
    var rerender = render;
    pybGarden.wireTheme(function () { paintSprites(); rerender(); });
    render();
    writeHash();
  });
})();
