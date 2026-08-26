/* The Glass Network - Week 5 build for Probability You Build.
   Ported from data/pai-w56/prototypes/proto-mlp.html (numerics already validated):
   seeded LCG datasets, flat-typed-array MLP, full-batch backprop, 80x80 boundary map.
   Mounts into every figure.build[data-glassnet]; which panels appear is decided by
   the figure's data-* attributes, so the same script grows across lessons 0400-0407. */
(function () {
  'use strict';

  /* ---- deterministic randomness (LCG, Box-Muller), exactly as prototyped ---- */
  function lcg(seed) {
    let s = (seed >>> 0) || 42;
    /* Numerical-Recipes constants through Math.imul, the hub's convention: imul keeps the
       product in exact 32-bit integer arithmetic, so the full 2^32 period survives and two
       readers on different engines see byte-identical data. Written with a plain float
       multiply the product passes 2^53, the low bits are rounded away, and the period
       collapses to about 16000 draws. */
    return function () { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
  }
  function gaussFactory(rnd) {
    return function () {
      let u = 0, v = 0;
      while (u === 0) u = rnd();
      while (v === 0) v = rnd();
      return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    };
  }

  /* ---- seeded datasets: n=200, labels alternate, input space roughly [-2,2]^2 ---- */
  const SIGMA = { 'moons': 0.09, 'moon-noisy': 0.25, 'spiral': 0.06, 'blobs': 0.35 };
  function makeData(kind, n) {
    const rnd = lcg(42), gauss = gaussFactory(rnd);
    const pts = [];
    for (let i = 0; i < n; i++) {
      const label = i % 2;
      let x, y;
      if (kind === 'moons' || kind === 'moon-noisy') {
        const sg = SIGMA[kind];
        const t = Math.PI * rnd();
        if (label === 0) { x = Math.cos(t) * 0.9 - 0.45; y = Math.sin(t) * 0.9 - 0.25; }
        else { x = -Math.cos(t) * 0.9 + 0.45; y = -Math.sin(t) * 0.9 + 0.25; }
        x += gauss() * sg; y += gauss() * sg;
      } else if (kind === 'spiral') {
        const t = 1.75 * i / n * 2 * Math.PI + (label ? Math.PI : 0);
        const r = 0.05 + 1.0 * i / n;
        x = r * Math.sin(t) + gauss() * SIGMA.spiral; y = r * Math.cos(t) + gauss() * SIGMA.spiral;
      } else { /* blobs */
        if (label === 0) { x = -0.5 + gauss() * SIGMA.blobs; y = -0.5 + gauss() * SIGMA.blobs; }
        else { x = 0.5 + gauss() * SIGMA.blobs; y = 0.5 + gauss() * SIGMA.blobs; }
      }
      pts.push({ x: [x, y], y: label });
    }
    return pts;
  }
  const DS_LABEL = { 'moons': 'two moons', 'moon-noisy': 'noisy moons', 'spiral': 'two spirals', 'blobs': 'linear-ish blobs' };

  /* ---- the network: layers as flat Float64Arrays, no matrix library ---- */
  function makeNet(sizes, act) {
    const rnd = lcg(42), gauss = gaussFactory(rnd);
    const W = [], b = [];
    for (let l = 0; l < sizes.length - 1; l++) {
      const nin = sizes[l], nout = sizes[l + 1];
      const w = new Float64Array(nin * nout);
      const scale = Math.sqrt(2 / (nin + nout)); /* Xavier-ish, as prototyped */
      for (let i = 0; i < w.length; i++) w[i] = gauss() * scale;
      W.push(w); b.push(new Float64Array(nout));
    }
    return { sizes: sizes.slice(), W: W, b: b, act: act || 'tanh' };
  }
  function hidAct(net, z) {
    if (net.act === 'sig') return 1 / (1 + Math.exp(-z));
    if (net.act === 'none') return z;
    return Math.tanh(z);
  }
  function hidDeriv(net, a) { /* derivative in terms of the activated value */
    if (net.act === 'sig') return a * (1 - a);
    if (net.act === 'none') return 1;
    return 1 - a * a;
  }
  /* forward one input; fills cache.zs (pre-activations) and cache.as (activations) */
  function forward(net, x, cache) {
    let a = x;
    const zs = [], as = [Float64Array.from(x)];
    for (let l = 0; l < net.W.length; l++) {
      const nin = net.sizes[l], nout = net.sizes[l + 1];
      const z = new Float64Array(nout);
      for (let j = 0; j < nout; j++) {
        let s = net.b[l][j];
        for (let i = 0; i < nin; i++) s += net.W[l][i * nout + j] * a[i];
        z[j] = s;
      }
      let out;
      if (l === net.W.length - 1) out = new Float64Array(nout).map((_, j) => 1 / (1 + Math.exp(-z[j])));
      else out = new Float64Array(nout).map((_, j) => hidAct(net, z[j]));
      zs.push(z); as.push(out); a = out;
    }
    if (cache) { cache.zs = zs; cache.as = as; }
    return a[0];
  }
  function lossOf(p, y) { return -(y * Math.log(p + 1e-12) + (1 - y) * Math.log(1 - p + 1e-12)); }

  /* analytic gradients over one full batch, plus mean |delta| per layer.
     delta at the output is p-y (sigmoid+BCE); hidden hops multiply by W and g'.
     THE backward pass the page ships; lesson 0404 walks it line by line. */
  function computeGrads(net, data) {
    const gW = net.W.map(w => new Float64Array(w.length)), gb = net.b.map(v => new Float64Array(v.length));
    const layerAbs = new Float64Array(net.W.length);
    let loss = 0;
    for (const d of data) {
      const cache = {};
      const p = forward(net, d.x, cache);
      loss += lossOf(p, d.y);
      let delta = new Float64Array([p - d.y]);
      for (let l = net.W.length - 1; l >= 0; l--) {
        const nin = net.sizes[l], nout = net.sizes[l + 1];
        const aprev = cache.as[l];
        let absSum = 0;
        for (let j = 0; j < nout; j++) {
          gb[l][j] += delta[j]; absSum += Math.abs(delta[j]);
          for (let i = 0; i < nin; i++) gW[l][i * nout + j] += delta[j] * aprev[i];
        }
        layerAbs[l] += absSum / nout;
        if (l > 0) {
          const nd = new Float64Array(nin);
          for (let i = 0; i < nin; i++) {
            let s = 0;
            for (let j = 0; j < nout; j++) s += net.W[l][i * nout + j] * delta[j];
            nd[i] = s * hidDeriv(net, aprev[i]);
          }
          delta = nd;
        }
      }
    }
    const n = data.length || 1;
    for (let l = 0; l < net.W.length; l++) {
      for (let i = 0; i < gW[l].length; i++) gW[l][i] /= n;
      for (let j = 0; j < gb[l].length; j++) gb[l][j] /= n;
      layerAbs[l] /= n;
    }
    return { gW: gW, gb: gb, loss: loss / n, layerAbs: layerAbs };
  }

  /* instructor-supplied trainer: gradient step using computeGrads */
  function trainEpochSupplied(net, data, lr) {
    const g = computeGrads(net, data);
    applyGrads(net, g, lr);
    return { loss: g.loss, layerAbs: g.layerAbs };
  }
  /* learner-owned trainer, milestone M3. In YOUR local copy of this file, delete the
     body below (everything between the HERE marks) and type the backward pass yourself,
     following lesson 0404. The finite-difference checker will tell you if you got it right. */
  function trainEpochMine(net, data, lr) {
    /* ===== STUDENT CODE HERE ===== */
    const g = computeGrads(net, data);
    applyGrads(net, g, lr);
    return { loss: g.loss, layerAbs: g.layerAbs };
    /* ===== END STUDENT CODE ===== */
  }
  function applyGrads(net, g, lr) {
    for (let l = 0; l < net.W.length; l++) {
      for (let i = 0; i < net.W[l].length; i++) net.W[l][i] -= lr * g.gW[l][i];
      for (let j = 0; j < net.b[l].length; j++) net.b[l][j] -= lr * g.gb[l][j];
    }
  }
  /* full-batch loss only (for the finite-difference checker) */
  function totalLoss(net, data) {
    let loss = 0;
    for (const d of data) loss += lossOf(forward(net, d.x, null), d.y);
    return loss / (data.length || 1);
  }
  /* finite-difference check: five random weights, central difference, eps = 1e-5 */
  function checkGradients(net, data) {
    const g = computeGrads(net, data);
    const flat = [], pick = [];
    for (let l = 0; l < net.W.length; l++) for (let i = 0; i < net.W[l].length; i++) flat.push([l, i]);
    const rnd = lcg(424242);
    while (pick.length < 5 && flat.length > pick.length) {
      const k = Math.floor(rnd() * flat.length);
      if (!pick.some(p => p[0] === flat[k][0] && p[1] === flat[k][1])) pick.push(flat[k]);
    }
    const eps = 1e-5;
    let worst = 0, rows = [];
    for (const where of pick) {
      const l = where[0], i = where[1], orig = net.W[l][i];
      net.W[l][i] = orig + eps; const lp = totalLoss(net, data);
      net.W[l][i] = orig - eps; const lm = totalLoss(net, data);
      net.W[l][i] = orig;
      const gn = (lp - lm) / (2 * eps), ga = g.gW[l][i];
      const rel = Math.abs(ga - gn) / Math.max(1, Math.abs(ga) + Math.abs(gn));
      worst = Math.max(worst, rel);
      rows.push('W' + l + '[' + i + '] analytical ' + ga.toFixed(6) + ', numerical ' + gn.toFixed(6));
    }
    return { worst: worst, rows: rows };
  }

  /* ---- colours: read from CSS tokens at draw time, never literal hex ---- */
  const probe = document.createElement('span');
  probe.style.display = 'none';
  document.body.appendChild(probe);
  /* A token that does not exist computes to `inherit` for `color`, which silently returns
     the surrounding text colour - every series then draws in the same hue and nothing warns
     you. The explicit fallback makes a missing token loud instead. */
  function col(name, fallback) {
    probe.style.color = 'var(' + name + ', ' + fallback + ')';
    return getComputedStyle(probe).color;
  }
  function rgb(c) { const m = c.match(/\d+(\.\d+)?/g); return [+m[0], +m[1], +m[2]]; }
  function css(c) { return 'rgb(' + Math.round(c[0]) + ',' + Math.round(c[1]) + ',' + Math.round(c[2]) + ')'; }
  function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }
  /* Screen tokens on the left, their paper twins on the right. The chart tokens --stat,
     --alarm and --prob have no --l- twin in hub.css, so print maps them onto tokens that
     do exist rather than onto names that resolve to nothing. */
  const TOKENS = {
    c1:    ['--stat',      '--l-accent-2'],
    c0:    ['--alarm',     '--l-warn'],
    surf:  ['--surface',   '--l-surface'],
    ink:   ['--ink',       '--l-ink'],
    faint: ['--ink-faint', '--l-ink-faint'],
    soft:  ['--ink-soft',  '--l-ink-soft'],
    train: ['--prob',      '--l-accent'],
    test:  ['--gold',      '--l-gold'],
    bar:   ['--accent',    '--l-accent']
  };
  function palette(printSafe) {
    const pick = k => col(TOKENS[k][printSafe ? 1 : 0], printSafe ? '#333' : 'currentColor');
    return {
      c1: rgb(pick('c1')), c0: rgb(pick('c0')),
      surf: rgb(pick('surf')), ink: pick('ink'), faint: pick('faint'),
      soft: rgb(pick('soft')), train: pick('train'), test: pick('test'),
      bar: pick('bar')
    };
  }

  /* ---- one cockpit canvas: boundary map left, loss curve right, bars below-right ---- */
  const CW = 880, MAP = { x: 18, y: 18, s: 360 }, RANGE = 2;
  function layout(feat) {
    const curvy = feat.has('gradbars');
    return {
      curve: { x: MAP.x + MAP.s + 34, y: 18, w: CW - MAP.x - MAP.s - 52, h: curvy ? 210 : 350 },
      bars: { x: MAP.x + MAP.s + 34, y: 252, w: CW - MAP.x - MAP.s - 52, h: 126 },
      h: 396
    };
  }
  function toPx(v) { return (v + RANGE) / (2 * RANGE); }

  function mount(fig) {
    if (fig.dataset.glassMounted) return;
    fig.dataset.glassMounted = '1';
    const feat = new Set((fig.dataset.features || '').split(',').filter(Boolean));
    const sizesAttr = (fig.dataset.sizes || '2,8,8,1').split(',').map(Number);
    const dsList = (fig.dataset.ds || 'moons').split(',');
    const canvas = fig.querySelector('.build-canvas');
    const lay = layout(feat);
    canvas.width = CW; canvas.height = lay.h;
    const ctx = canvas.getContext('2d');

    const role = r => fig.querySelector('[data-role="' + r + '"]');
    const ui = {};
    ['step', 'run', 'reset', 'lr', 'ds', 'h1size', 'h2size', 'shape', 'act', 'split', 'trainer',
      'check', 'ckout', 'epoch', 'losstr', 'losste', 'acctr', 'accte', 'insp'].forEach(k => { ui[k] = role(k); });

    const st = {};
    /* Two ways a page may expose architecture. The pair of h1/h2 pickers keeps the
       two-hidden-layer story of lesson 0402 concrete; a single `shape` select carries a
       comma-separated list of hidden widths, which is how a page reaches depths the pair
       cannot express - 2-4-4-4-4-1, for instance, where the gradient bars vanish. */
    function currentSizes() {
      if (ui.shape) {
        const mid = ui.shape.value.split(',').map(Number).filter(v => v > 0);
        return [2].concat(mid, [1]);
      }
      if (!ui.h1size) return sizesAttr.slice();
      const h1 = +ui.h1size.value, h2 = ui.h2size ? +ui.h2size.value : 8;
      const mid = h2 > 0 ? [h1, h2] : [h1];
      return [2].concat(mid, [1]);
    }
    function reset() {
      st.net = makeNet(currentSizes(), ui.act ? ui.act.value : 'tanh');
      st.kind = ui.ds ? ui.ds.value : dsList[0];
      const all = makeData(st.kind, 200);
      if (ui.split && ui.split.checked) {
        const idx = all.map((_, i) => i), rnd = lcg(7);
        for (let i = idx.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); const t = idx[i]; idx[i] = idx[j]; idx[j] = t; }
        const cut = Math.ceil(all.length * 0.7);
        st.train = idx.slice(0, cut).map(i => all[i]); st.test = idx.slice(cut).map(i => all[i]);
      } else { st.train = all; st.test = []; }
      st.lossT = []; st.lossE = []; st.epoch = 0; st.deltas = null; st.deltaMax = 0.001;
      st.running = false; if (ui.run) ui.run.textContent = 'run';
      st.hover = null; st.check = null;
      refresh(true);
    }
    function accuracy(set) {
      if (!set.length) return NaN;
      let c = 0;
      for (const d of set) if ((forward(st.net, d.x, null) > 0.5 ? 1 : 0) === d.y) c++;
      return c / set.length;
    }
    function doStep(k) {
      const lr = ui.lr ? +ui.lr.value : 2;
      const trainer = ui.trainer && ui.trainer.value === 'mine' ? trainEpochMine : trainEpochSupplied;
      for (let i = 0; i < k; i++) {
        const r = trainer(st.net, st.train, lr);
        st.lossT.push(r.loss); st.epoch++;
        if (st.test.length) {
          let lv = 0; for (const d of st.test) lv += lossOf(forward(st.net, d.x, null), d.y);
          st.lossE.push(lv / st.test.length);
        }
        if (r.layerAbs) {
          st.deltas = Array.from(r.layerAbs);
          st.deltaMax = Math.max(st.deltaMax * 0.999, ...st.deltas, 0.001);
        }
      }
      if (st.lossT.length > 6000) { st.lossT.splice(0, 3000); if (st.lossE.length) st.lossE.splice(0, 3000); }
      refresh(false);
    }

    /* rendering */
    const off = document.createElement('canvas'); off.width = 80; off.height = 80;
    function drawMap(P, printSafe) {
      const img = off.getContext('2d').createImageData(80, 80);
      const inp = new Float64Array(2);
      for (let py = 0; py < 80; py++) for (let px = 0; px < 80; px++) {
        inp[0] = (px / 80) * 2 * RANGE - RANGE; inp[1] = RANGE - (py / 80) * 2 * RANGE;
        const p = forward(st.net, inp, null);
        const conf = Math.abs(p - 0.5) * 2;                 /* 0 at the boundary, 1 far away */
        const base = mix(P.c0, P.c1, p);
        const k = (py * 80 + px) * 4, outc = mix(P.surf, base, 0.28 + 0.62 * conf);
        img.data[k] = outc[0]; img.data[k + 1] = outc[1]; img.data[k + 2] = outc[2]; img.data[k + 3] = 255;
      }
      off.getContext('2d').putImageData(img, 0, 0);
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(off, MAP.x, MAP.y, MAP.s, MAP.s);
      ctx.imageSmoothingEnabled = true;
      for (const d of st.train.concat(st.test)) {
        const px = MAP.x + toPx(d.x[0]) * MAP.s, py = MAP.y + (1 - toPx(d.x[1])) * MAP.s;
        ctx.beginPath(); ctx.arc(px, py, 3, 0, 7);
        ctx.fillStyle = css(d.y ? P.c1 : P.c0); ctx.fill();
        ctx.strokeStyle = P.ink; ctx.lineWidth = 0.6; ctx.stroke();
      }
      ctx.strokeStyle = P.faint; ctx.lineWidth = 1;
      ctx.strokeRect(MAP.x + 0.5, MAP.y + 0.5, MAP.s - 1, MAP.s - 1);
      ctx.fillStyle = P.faint; ctx.font = '11px ui-monospace, monospace'; ctx.textAlign = 'center';
      ctx.fillText(st.kind + '   x, y in [-2, 2]', MAP.x + MAP.s / 2, MAP.y + MAP.s + 14);
      if (st.hover) {
        const hx = MAP.x + toPx(st.hover.x) * MAP.s, hy = MAP.y + (1 - toPx(st.hover.y)) * MAP.s;
        ctx.beginPath(); ctx.arc(hx, hy, 6, 0, 7); ctx.strokeStyle = P.ink; ctx.lineWidth = 1.4; ctx.stroke();
      }
    }
    function drawCurves(P) {
      const c = layout(feat).curve;
      ctx.strokeStyle = P.faint; ctx.lineWidth = 1;
      ctx.strokeRect(c.x + 0.5, c.y + 0.5, c.w - 1, c.h - 1);
      ctx.fillStyle = P.faint; ctx.font = '11px ui-monospace, monospace'; ctx.textAlign = 'left';
      ctx.fillText('cross-entropy loss', c.x + 8, c.y + 16);
      if (st.lossT.length < 2) return;
      const T = st.lossT, E = st.lossE;
      let maxL = 0.1;
      for (let i = 0; i < T.length; i++) { if (T[i] > maxL) maxL = T[i]; }
      for (let i = 0; i < E.length; i++) { if (E[i] > maxL) maxL = E[i]; }
      maxL *= 1.05;
      const N = T.length;
      function plot(arr, color, dash) {
        ctx.beginPath();
        const M = arr.length, stride = Math.max(1, Math.floor(M / 1200));
        for (let i = 0; i < M; i += stride) {
          const x = c.x + 2 + (i / (N - 1)) * (c.w - 4);
          const y = c.y + c.h - 4 - (arr[i] / maxL) * (c.h - 26);
          if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = color; ctx.lineWidth = 1.6; ctx.setLineDash(dash || []); ctx.stroke(); ctx.setLineDash([]);
      }
      const yln = c.y + c.h - 4 - (Math.LN2 / maxL) * (c.h - 26);
      ctx.strokeStyle = P.faint; ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(c.x + 2, yln); ctx.lineTo(c.x + c.w - 2, yln); ctx.stroke(); ctx.setLineDash([]);
      plot(T, P.train, []); if (E.length) plot(E, P.test, [5, 4]);
      ctx.font = '11px ui-monospace, monospace';
      ctx.fillStyle = P.faint; ctx.textAlign = 'right';
      ctx.fillText(maxL.toFixed(2), c.x + c.w - 8, c.y + 16);
      ctx.fillStyle = P.train; ctx.fillText('train', c.x + c.w - 8, c.y + 30);
      if (E.length) { ctx.fillStyle = P.test; ctx.fillText('test', c.x + c.w - 8, c.y + 44); }
      ctx.textAlign = 'left';
      ctx.fillStyle = P.faint;
      ctx.fillText('ln 2 dashed - the uninformed guess', c.x + 8, c.y + c.h - 6);
      ctx.fillText('epoch ' + st.epoch, c.x + c.w - 78, c.y + c.h - 6);
    }
    function drawBars(P) {
      const c = layout(feat).bars;
      ctx.strokeStyle = P.faint; ctx.strokeRect(c.x + 0.5, c.y + 0.5, c.w - 1, c.h - 1);
      ctx.fillStyle = P.faint; ctx.font = '11px ui-monospace, monospace';
      ctx.fillText('mean |delta| per layer (backward signal)', c.x + 8, c.y + 15);
      if (!st.deltas) return;
      const n = st.deltas.length, bh = Math.min(18, (c.h - 44) / n);
      for (let l = 0; l < n; l++) {
        const y = c.y + 26 + l * (bh + 4);
        const w = (st.deltas[l] / st.deltaMax) * (c.w - 110);
        ctx.fillStyle = P.bar; ctx.fillRect(c.x + 56, y, Math.max(1, w), bh);
        ctx.fillStyle = P.faint; ctx.textAlign = 'right';
        ctx.fillText('layer ' + (l + 1), c.x + 50, y + bh - 5);
        ctx.textAlign = 'left';
        ctx.fillText(st.deltas[l].toFixed(3), c.x + 60 + Math.max(1, w), y + bh - 5);
      }
    }
    function render(printSafe) {
      const P = palette(printSafe);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawMap(P, printSafe);
      drawCurves(P);
      if (feat.has('gradbars')) drawBars(P);
    }

    /* readouts */
    function fmtArr(a) { return Array.from(a).map(v => (v >= 0 ? '+' : '') + v.toFixed(2)).join(' '); }
    function refresh(full) {
      if (ui.epoch) ui.epoch.textContent = String(st.epoch);
      const lt = st.lossT[st.lossT.length - 1];
      if (ui.losstr) ui.losstr.textContent = lt == null ? '-' : lt.toFixed(4);
      if (ui.losste) ui.losste.textContent = st.test.length && st.lossE.length ? st.lossE[st.lossE.length - 1].toFixed(4) : '-';
      if (ui.acctr) ui.acctr.textContent = isNaN(accuracy(st.train)) ? '-' : accuracy(st.train).toFixed(3);
      if (ui.accte) ui.accte.textContent = st.test.length ? accuracy(st.test).toFixed(3) : '-';
      if (full && ui.ckout && st.check) ui.ckout.textContent = '';
      render(false);
      if (st.hover && ui.insp) inspect(st.hover.x, st.hover.y);
    }
    const INSP_IDLE = 'hover the map to replay the forward pass at that point';
    function inspect(x, y) {
      const cache = {}; const p = forward(st.net, [x, y], cache);
      const last = st.net.sizes.length - 2;   /* index of the output layer's weights */
      const rows = [];
      for (let l = 0; l <= last; l++) {
        if (l === last) {
          /* The output layer's activation IS p-hat, so naming it twice would suggest two
             numbers where there is one. Label its pre-activation as the logit instead,
             which is the name lesson 0400 gave it. */
          rows.push('output logit z: ' + fmtArr(cache.zs[l]) + ', sigmoid of which is');
        } else {
          rows.push('layer ' + (l + 1) + ' pre-activation z: ' + fmtArr(cache.zs[l]));
          rows.push('layer ' + (l + 1) + ' activation   a: ' + fmtArr(cache.as[l + 1]));
        }
      }
      ui.insp.innerHTML = '';
      const mk = (txt, strong) => { const s = document.createElement('span'); s.textContent = txt; if (strong) { const b = document.createElement('b'); b.textContent = strong; s.appendChild(b); } ui.insp.appendChild(s); };
      mk('(' + x.toFixed(2) + ', ' + y.toFixed(2) + ')  ');
      rows.forEach(r => mk(r + '  '));
      mk('predicted p(class 1) = ', p.toFixed(3));
    }

    /* controls */
    if (ui.step) ui.step.addEventListener('click', () => doStep(100));
    if (ui.reset) ui.reset.addEventListener('click', reset);
    if (ui.run) ui.run.addEventListener('click', () => { st.running = !st.running; ui.run.textContent = st.running ? 'pause' : 'run'; });
    if (ui.ds) ui.ds.addEventListener('change', reset);
    if (ui.shape) ui.shape.addEventListener('change', reset);
    if (ui.h1size) ui.h1size.addEventListener('change', reset);
    if (ui.h2size) ui.h2size.addEventListener('change', reset);
    if (ui.act) ui.act.addEventListener('change', reset);
    if (ui.split) ui.split.addEventListener('change', reset);
    if (ui.check) ui.check.addEventListener('click', () => {
      const r = checkGradients(st.net, st.train);
      if (ui.ckout) ui.ckout.textContent = 'max relative error ' + r.worst.toExponential(2) + '  (' + r.rows.join('; ') + ')';
    });
    let hoverPending = false;
    canvas.addEventListener('pointermove', e => {
      if (!feat.has('inspector')) return;
      const r = canvas.getBoundingClientRect();
      const sx = (e.clientX - r.left) * (canvas.width / r.width);
      const sy = (e.clientY - r.top) * (canvas.height / r.height);
      if (sx < MAP.x || sx > MAP.x + MAP.s || sy < MAP.y || sy > MAP.y + MAP.s) { st.hover = null; }
      else {
        const x = ((sx - MAP.x) / MAP.s) * 2 * RANGE - RANGE;
        const y = RANGE - ((sy - MAP.y) / MAP.s) * 2 * RANGE;
        st.hover = { x: x, y: y };
      }
      if (!hoverPending) {
        hoverPending = true;
        requestAnimationFrame(() => {
          hoverPending = false; render(false);
          if (st.hover) inspect(st.hover.x, st.hover.y); else clearInspector();
        });
      }
    });
    /* Leaving the map must clear the readout too: a probe that is no longer on a point
       but still prints that point's activations is worse than printing nothing. */
    function clearInspector() { if (ui.insp) ui.insp.textContent = INSP_IDLE; }
    canvas.addEventListener('pointerleave', () => { st.hover = null; clearInspector(); render(false); });

    (function loop() { if (st.running) doStep(20); requestAnimationFrame(loop); })();

    new MutationObserver(() => render(false))
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
    window.addEventListener('beforeprint', () => render(true));
    window.addEventListener('afterprint', () => render(false));

    reset();
  }

  function initAll() {
    document.querySelectorAll('figure.build[data-glassnet]').forEach(mount);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initAll);
  else initAll();
})();
