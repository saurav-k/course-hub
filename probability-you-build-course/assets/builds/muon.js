/* probability-you-build-course - Week 3 Build 1: find the hidden chamber.
   Muon tomography by maximum likelihood, taught in four staged figures:
   data-stage="compare" (sky, stone, observed bars, two hypotheses by eye),
   "slide" (hypothesis sliders with live Poisson log-likelihood),
   "search" (the log-likelihood heatmap over (x, w) and the learner's grid search),
   "repeat" (resample-and-refit history: estimation variance made visible),
   "api" (headless: exposes the core for the problems page).

   Every number the simulation shows is generated in this file from teaching
   constants. Nothing here is ScanPyramids measurement data: the geometry
   follows the published description of the 2017 discovery (Morishima et al.,
   Nature 552, 386-390, 2017, https://www.nature.com/articles/nature24647),
   and every flux, absorption and exposure constant is a teaching choice,
   labelled as such on the lesson pages. */
(function () {
  'use strict';

  /* ============================================================
     CORE - pure functions, no DOM. Exported for the problems page
     and for mechanical verification of everything the pages claim.
     ============================================================ */

  /* Seeded PRNG (mulberry32), course convention seed 42: two readers see
     byte-identical counts and screenshots match the prose. Chosen over a
     classic multiplicative LCG because LCG outputs sit on lattice lines that
     correlate Box-Muller pairs; this generator does not (verified while
     building: Park-Miller produced a 3.9-sigma shadowing draw in its first
     eight outputs). */
  function makeRng(seed) {
    var a = (seed >>> 0) || 1;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  /* World geometry, in canvas pixels used as length units throughout.
     Teaching constants except the qualitative facts they encode: muons arrive
     near-vertically (a cos-squared angular law, the standard sea-level
     approximation), rock absorbs a fraction of them, and a void shortens the
     stone a crossing ray traverses. */
  var WORLD = {
    H: 220,            //pyramid height
    BASEW: 380,        //base width
    apexX: 210,        //apex position on the canvas
    apexY: 40,
    trueVoid: { x: 40, w: 25 }, //centre offset from the axis, half-width - nature's void
    voidTop: 95,       //void band, depths below the apex
    voidBottom: 145,
    gallery: { x: -70, top: 170, w: 26, h: 34 }, //known chamber (Grand Gallery stand-in)
    LAMBDA: 260,       //absorption length of stone, px (teaching constant)
    NBIN: 24,          //angular bins the detector counts
    TANMAX: 0.9,       //tan of the widest accepted angle
    EXPOSURE: 250,     //open-sky count scale per bin (teaching constant; kept well
                       //below the Poisson-sampler underflow regime)
    XD: 60,            //detector centre offset from the axis
    SEED: 42
  };

  function tanLo(i) { return -WORLD.TANMAX + 2 * WORLD.TANMAX * i / WORLD.NBIN; }

  /* Stone thickness crossed by the ray that reaches the detector at tangent
     t, traced upward through a pyramid that contains a hypothesised void
     centred at hx with half-width hw. Backward tracing from one known
     detector position is what buys spatial resolution (see lesson 0200). */
  function rockLength(t, hx, hw) {
    var xd = WORLD.apexX + WORLD.XD;
    var steps = 120;
    var dd = WORLD.H / steps;
    var len = 0;
    for (var i = 0; i < steps; i++) {
      var d = i * dd + dd / 2;
      var x = xd - t * (WORLD.H - d);
      var y = WORLD.apexY + d;
      var halfw = (y - WORLD.apexY) * WORLD.BASEW / (2 * WORLD.H);
      if (Math.abs(x - WORLD.apexX) <= halfw) {
        var inVoid = hw > 0 &&
          Math.abs(x - (WORLD.apexX + hx)) <= hw &&
          y > WORLD.apexY + WORLD.voidTop &&
          y < WORLD.apexY + WORLD.voidBottom;
        if (!inVoid) len += dd;
      }
    }
    return len;
  }

  /* Expected count per angular bin under a hypothesis: open-sky flux with the
     standard cos-squared angular law, attenuated by exp(-L/LAMBDA) along the
     traced ray. */
  function expectedCounts(hx, hw) {
    var m = [];
    for (var i = 0; i < WORLD.NBIN; i++) {
      var tMid = (tanLo(i) + tanLo(i + 1)) / 2;
      var sky = Math.cos(Math.atan(tMid)) * Math.cos(Math.atan(tMid));
      var L = rockLength(tMid, hx, hw);
      m.push(WORLD.EXPOSURE * sky * Math.exp(-L / WORLD.LAMBDA));
    }
    return m;
  }

  /* One Poisson draw with mean lam (Knuth's method; every lambda this world
     produces stays far below the exp-underflow regime, by construction). */
  function poissonSample(rnd, lam) {
    var L = Math.exp(-lam);
    var k = 0, p = 1;
    do { k++; p *= rnd(); } while (p > L);
    return k - 1;
  }

  /* Generate one exposure worth of observed counts under nature's void. */
  function generateObserved(seed) {
    var rnd = makeRng(seed === undefined ? WORLD.SEED : seed);
    var truth = expectedCounts(WORLD.trueVoid.x, WORLD.trueVoid.w);
    return truth.map(function (lam) { return poissonSample(rnd, lam); });
  }

  /* Poisson log-likelihood of the observed counts under hypothesis (hx, hw),
     dropping the constant ln(k!) terms: sum over bins of k*ln(m) - m. */
  function poissonLogLik(obs, hx, hw) {
    var m = expectedCounts(hx, hw);
    var ll = 0;
    for (var i = 0; i < obs.length; i++) ll += obs[i] * Math.log(m[i]) - m[i];
    return ll;
  }

  /* The learner's grid search itself lives on the page; this helper runs the
     same scan so the pages and solutions can quote reproducible numbers:
     x in [-120, 120] step 5, w in [0, 80] step 5, first max wins. */
  function gridScan(obs) {
    var best = null;
    var rows = [];
    for (var w = 0; w <= 80; w += 5) {
      var row = [];
      for (var x = -120; x <= 120; x += 5) {
        var v = poissonLogLik(obs, x, w);
        row.push(v);
        if (best === null || v > best.ll) best = { x: x, w: w, ll: v };
      }
      rows.push(row);
    }
    return { xs: 49, ws: 17, x0: -120, w0: 0, step: 5, grid: rows, best: best };
  }

  var PYBMuon = {
    WORLD: WORLD,
    makeRng: makeRng,
    tanLo: tanLo,
    rockLength: rockLength,
    expectedCounts: expectedCounts,
    poissonSample: poissonSample,
    generateObserved: generateObserved,
    poissonLogLik: poissonLogLik,
    gridScan: gridScan
  };

  /* ============================================================
     MOUNTING - DOM wiring for the lesson figures. Skipped entirely
     when loaded outside a browser (node verification imports the
     core directly).
     ============================================================ */
  if (typeof document === 'undefined') {
    if (typeof module !== 'undefined' && module.exports) module.exports = PYBMuon;
    return;
  }

  function tok(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim() || '#888';
  }
  function hexParts(c) {
    c = c.replace('#', '');
    if (c.length === 3) c = c[0] + c[0] + c[1] + c[1] + c[2] + c[2];
    var n = parseInt(c, 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function rgba(hex, a) { var p = hexParts(hex); return 'rgba(' + p[0] + ',' + p[1] + ',' + p[2] + ',' + a + ')'; }
  function mix(h1, h2, t) {
    var a = hexParts(h1), b = hexParts(h2);
    var r = Math.round(a[0] + (b[0] - a[0]) * t);
    var g = Math.round(a[1] + (b[1] - a[1]) * t);
    var bl = Math.round(a[2] + (b[2] - a[2]) * t);
    return 'rgb(' + r + ',' + g + ',' + bl + ')';
  }

  /* Print keeps the stage and readout but the canvas keeps whatever colours it
     drew last, so a dark-mode canvas would print dark-on-white. Redraw the
     whole instrument in ink-on-paper before the snapshot, restore after. */
  var PRINT = { bg: '#ffffff', ink: '#1a1a18', inkSoft: '#4a4a44', faint: '#63635b',
                line: '#cccccc', surface: '#ffffff', alarm: '#b23c0a', prob: '#4c3fbf',
                signal: '#136b2c', noise: '#5c5c55', gold: '#7a5a0a' };

  function mount(figure) {
    if (figure.dataset.muonMounted) return;
    figure.dataset.muonMounted = 'yes';
    var stage = figure.dataset.stage;
    var canvas = figure.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');
    var controls = figure.querySelector('.build-controls');
    var readout = figure.querySelector('.build-readout');

    var state = {
      obs: null,
      hx: 40, hw: 25,          //slider positions
      showRock: false, showVoid: false,
      fit: null,               //grid-search result, once run
      history: [],             //resample-refit markers (stage "repeat")
      seed: 43
    };
    var scanCache = null;      //heatmap grid for the current dataset

    function el(role) { return figure.querySelector('[data-role="' + role + '"]'); }

    function regenerate(seed) {
      state.obs = PYBMuon.generateObserved(seed);
      scanCache = null;
    }

    function scan() {
      if (!scanCache) scanCache = PYBMuon.gridScan(state.obs);
      return scanCache;
    }

    /* ---------- drawing ---------- */

    var LAYOUT = {
      pyr: { x: 18, y: 14, w: 424, h: 306 },
      bars: { x: 462, y: 14, w: 458, h: 306 },
      heat: { x: 60, y: 386, w: 812, h: 250 }
    };

    function colors(printSafe) {
      if (printSafe) return PRINT;
      return {
        bg: tok('--surface'), ink: tok('--ink'), inkSoft: tok('--ink-soft'),
        faint: tok('--ink-faint'), line: tok('--line'), surface: tok('--surface'),
        surface2: tok('--surface-2'), alarm: tok('--alarm'), prob: tok('--prob'),
        signal: tok('--signal'), noise: tok('--noise'), gold: tok('--chart-gold')
      };
    }

    function drawPyramid(c, C, ox, oy) {
      var ax = ox + 192, ay = oy + 26;             //apex inside the panel
      var baseY = ay + WORLD.H;
      //stone
      c.beginPath();
      c.moveTo(ax, ay);
      c.lineTo(ax - WORLD.BASEW / 2, baseY);
      c.lineTo(ax + WORLD.BASEW / 2, baseY);
      c.closePath();
      c.fillStyle = rgba(C.gold, 0.16);
      c.fill();
      c.strokeStyle = C.gold;
      c.stroke();
      //known gallery
      c.fillStyle = C.surface;
      c.strokeStyle = C.faint;
      c.fillRect(ax + WORLD.gallery.x, ay + WORLD.gallery.top, WORLD.gallery.w, WORLD.gallery.h);
      c.strokeRect(ax + WORLD.gallery.x, ay + WORLD.gallery.top, WORLD.gallery.w, WORLD.gallery.h);
      c.fillStyle = C.faint;
      c.font = '11px sans-serif';
      c.textAlign = 'center';
      c.fillText('known gallery', ax + WORLD.gallery.x + 13, ay + WORLD.gallery.top + WORLD.gallery.h + 13);
      //nature's void - dashed, never movable
      var tvx = ax + WORLD.trueVoid.x;
      c.setLineDash([5, 3]);
      c.strokeStyle = C.alarm;
      c.lineWidth = 1.6;
      c.strokeRect(tvx - WORLD.trueVoid.w, ay + WORLD.voidTop, 2 * WORLD.trueVoid.w, WORLD.voidBottom - WORLD.voidTop);
      c.setLineDash([]);
      c.lineWidth = 1;
      c.fillStyle = C.alarm;
      c.fillText('hidden void (nature)', tvx, ay + WORLD.voidTop - 6);
      //hypothesised void
      if ((state.showVoid || stage === 'slide' || stage === 'search' || stage === 'repeat') && state.hw > 0) {
        var hvx = ax + state.hx;
        c.strokeStyle = C.prob;
        c.lineWidth = 2;
        c.strokeRect(hvx - state.hw, ay + WORLD.voidTop + 5, 2 * state.hw, WORLD.voidBottom - WORLD.voidTop - 10);
        c.lineWidth = 1;
        c.fillStyle = C.prob;
        c.fillText('your hypothesis', hvx, ay + WORLD.voidBottom + 14);
      }
      //fitted void from the grid search, once run
      if (state.fit) {
        var fx = ax + state.fit.best.x;
        c.strokeStyle = C.signal;
        c.lineWidth = 2;
        c.strokeRect(fx - state.fit.best.w, ay + WORLD.voidTop + 10, 2 * state.fit.best.w, WORLD.voidBottom - WORLD.voidTop - 20);
        c.lineWidth = 1;
        c.fillStyle = C.signal;
        c.fillText('grid argmax', fx, ay + WORLD.voidTop + 2);
      }
      //detector
      c.fillStyle = C.inkSoft;
      c.fillRect(ax - WORLD.BASEW / 2, baseY, WORLD.BASEW, 8);
      c.fillStyle = C.inkSoft;
      c.fillText('muon detector (counts arrivals in 24 angular bins)', ax + WORLD.XD - 40, baseY + 22);
      //a few sample rays
      c.strokeStyle = rgba(C.faint, 0.55);
      for (var ri = -2; ri <= 2; ri++) {
        var t = ri * 0.35;
        c.beginPath();
        c.moveTo(ax + WORLD.XD, baseY);
        c.lineTo(ax + WORLD.XD - t * WORLD.H, ay);
        c.stroke();
      }
      c.textAlign = 'left';
    }

    function drawBars(c, C, oxb, oyb) {
      var m = PYBMuon.expectedCounts(state.hx, state.hw);
      var baseY = oyb + 262, topY = oyb + 26;
      var bw = LAYOUT.bars.w / WORLD.NBIN;
      var mx = Math.max.apply(null, state.obs.concat(m));
      var scale = (baseY - topY) / mx;
      c.strokeStyle = C.line;
      c.beginPath(); c.moveTo(oxb, baseY); c.lineTo(oxb + LAYOUT.bars.w, baseY); c.stroke();
      for (var i = 0; i < WORLD.NBIN; i++) {
        var x0 = oxb + i * bw;
        //observed: filled grey
        c.fillStyle = rgba(C.noise, 0.75);
        c.fillRect(x0 + 3, baseY - state.obs[i] * scale, bw - 6, state.obs[i] * scale);
        //no-void prediction: dashed outline
        if (state.showRock) {
          var m0 = PYBMuon.expectedCounts(0, 0)[i];
          c.setLineDash([3, 3]);
          c.strokeStyle = C.faint;
          c.strokeRect(x0 + 3, baseY - m0 * scale, bw - 6, m0 * scale);
          c.setLineDash([]);
        }
        //void prediction (live hypothesis): solid indigo outline
        if (state.showVoid || stage === 'slide' || stage === 'search' || stage === 'repeat') {
          c.strokeStyle = C.prob;
          c.lineWidth = 1.8;
          c.strokeRect(x0 + 3, baseY - m[i] * scale, bw - 6, m[i] * scale);
          c.lineWidth = 1;
        }
      }
      c.fillStyle = C.inkSoft;
      c.font = '12px sans-serif';
      c.textAlign = 'center';
      c.fillText('muons counted per angular bin (left = steep, right = steep, middle = through the peak)',
        oxb + LAYOUT.bars.w / 2, baseY + 18);
      c.fillText('grey: observed   indigo: your hypothesis predicts' +
        (state.showRock ? '   dashed grey: solid-rock prediction' : ''), oxb + LAYOUT.bars.w / 2, baseY + 34);
      c.textAlign = 'left';
    }

    function drawHeatmap(c, C) {
      var sc = scan();
      var R = LAYOUT.heat;
      var cw = R.w / sc.xs, ch = R.h / sc.ws;
      var lo = Infinity, hi = -Infinity;
      for (var r = 0; r < sc.ws; r++) for (var q = 0; q < sc.xs; q++) {
        var v = sc.grid[r][q];
        if (v < lo) lo = v;
        if (v > hi) hi = v;
      }
      var off = document.createElement('canvas');
      off.width = sc.xs; off.height = sc.ws;
      var octx = off.getContext('2d');
      for (r = 0; r < sc.ws; r++) for (q = 0; q < sc.xs; q++) {
        var t = (sc.grid[r][q] - lo) / (hi - lo);
        octx.fillStyle = mix(C.surface2, C.signal, Math.pow(t, 1.6));
        octx.fillRect(q, sc.ws - 1 - r, 1, 1);
      }
      c.imageSmoothingEnabled = false;
      c.drawImage(off, R.x, R.y, R.w, R.h);
      c.imageSmoothingEnabled = true;
      c.strokeStyle = C.line;
      c.strokeRect(R.x, R.y, R.w, R.h);
      //axes
      c.fillStyle = C.inkSoft;
      c.font = '12px sans-serif';
      c.textAlign = 'center';
      c.fillText('hypothesised void centre x (px)', R.x + R.w / 2, R.y + R.h + 20);
      c.save();
      c.translate(R.x - 34, R.y + R.h / 2);
      c.rotate(-Math.PI / 2);
      c.fillText('hypothesised half-width w (px)', 0, 0);
      c.restore();
      c.textAlign = 'center';
      [-120, -60, 0, 60, 120].forEach(function (xv) {
        var px = R.x + (xv + 120) / 240 * R.w;
        c.strokeStyle = C.line;
        c.beginPath(); c.moveTo(px, R.y + R.h); c.lineTo(px, R.y + R.h + 5); c.stroke();
        c.fillText(String(xv), px, R.y + R.h + 15);
      });
      [0, 20, 40, 60, 80].forEach(function (wv) {
        var py = R.y + R.h - wv / 80 * R.h;
        c.strokeStyle = C.line;
        c.beginPath(); c.moveTo(R.x - 5, py); c.lineTo(R.x, py); c.stroke();
        c.fillText(String(wv), R.x - 12, py + 4);
      });
      //nature's void, for reference
      var tx = R.x + (WORLD.trueVoid.x + 120) / 240 * R.w;
      var ty = R.y + R.h - WORLD.trueVoid.w / 80 * R.h;
      c.setLineDash([4, 3]);
      c.strokeStyle = C.alarm;
      c.beginPath();
      c.moveTo(tx, R.y); c.lineTo(tx, R.y + R.h);
      c.moveTo(R.x, ty); c.lineTo(R.x + R.w, ty);
      c.stroke();
      c.setLineDash([]);
      c.fillStyle = C.alarm;
      c.fillText("nature's void", tx, R.y - 6);
      //resample-refit history
      c.fillStyle = C.prob;
      state.history.forEach(function (hfit) {
        var hx2 = R.x + (hfit.x + 120) / 240 * R.w;
        var hy2 = R.y + R.h - hfit.w / 80 * R.h;
        c.beginPath();
        c.arc(hx2, hy2, 4, 0, 7);
        c.fill();
      });
      //the grid-search argmax
      if (state.fit) {
        var bx = R.x + (state.fit.best.x + 120) / 240 * R.w;
        var by = R.y + R.h - state.fit.best.w / 80 * R.h;
        c.strokeStyle = C.ink;
        c.lineWidth = 2;
        c.beginPath();
        c.moveTo(bx - 7, by - 7); c.lineTo(bx + 7, by + 7);
        c.moveTo(bx + 7, by - 7); c.lineTo(bx - 7, by + 7);
        c.stroke();
        c.lineWidth = 1;
        c.fillStyle = C.ink;
        c.fillText('grid argmax', bx, by - 12);
      }
      c.textAlign = 'left';
    }

    function render(printSafe) {
      var C = colors(printSafe);
      ctx.fillStyle = C.bg;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = C.line;
      ctx.strokeRect(LAYOUT.pyr.x, LAYOUT.pyr.y, LAYOUT.pyr.w, LAYOUT.pyr.h);
      ctx.strokeRect(LAYOUT.bars.x, LAYOUT.bars.y, LAYOUT.bars.w, LAYOUT.bars.h);
      drawPyramid(ctx, C, LAYOUT.pyr.x, LAYOUT.pyr.y);
      drawBars(ctx, C, LAYOUT.bars.x, LAYOUT.bars.y);
      if (stage === 'search' || stage === 'repeat') drawHeatmap(ctx, C);
      updateReadout();
    }

    function updateReadout() {
      var totEl = el('total');
      if (totEl && state.obs) {
        totEl.textContent = String(state.obs.reduce(function (a, b) { return a + b; }, 0));
      }
      var llEl = el('ll');
      if (llEl && state.obs) {
        llEl.textContent = PYBMuon.poissonLogLik(state.obs, state.hx, state.hw).toFixed(1);
      }
      var gridEl = el('grid');
      if (gridEl && state.fit) {
        gridEl.textContent = 'grid argmax: x=' + state.fit.best.x + ', w=' + state.fit.best.w +
          ', LL=' + state.fit.best.ll.toFixed(1);
      }
      var histEl = el('history');
      if (histEl) {
        if (!state.history.length) { histEl.textContent = 'no refits yet'; }
        else {
          var last = state.history.slice(-5);
          var xs = state.history.map(function (f) { return f.x; });
          var ws = state.history.map(function (f) { return f.w; });
          histEl.textContent = last.length + ' of ' + state.history.length + ' latest: ' +
            last.map(function (f) { return '(x=' + f.x + ', w=' + f.w + ')'; }).join(' ') +
            ' - x range ' + Math.min.apply(null, xs) + '..' + Math.max.apply(null, xs) +
            ', w range ' + Math.min.apply(null, ws) + '..' + Math.max.apply(null, ws);
        }
      }
    }

    /* ---------- controls ---------- */

    function bindRange(role, key) {
      var input = el(role);
      if (!input) return;
      input.value = state[key];
      input.addEventListener('input', function () {
        state[key] = +input.value;
        render(false);
      });
    }
    bindRange('vx', 'hx');
    bindRange('vw', 'hw');

    var bRock = el('rock');
    if (bRock) bRock.addEventListener('change', function () { state.showRock = bRock.checked; render(false); });
    var bVoid = el('void');
    if (bVoid) bVoid.addEventListener('change', function () { state.showVoid = bVoid.checked; render(false); });

    var bSearch = el('search');
    if (bSearch) bSearch.addEventListener('click', function () {
      state.fit = scan();
      render(false);
    });

    var bRefit = el('refit');
    if (bRefit) bRefit.addEventListener('click', function () {
      var seedInput = el('seed');
      var seed = seedInput ? (+seedInput.value || 43) : 43;
      regenerate(seed);
      el('seed') && (el('seed').value = seed + 1);
      state.seed = seed + 1;
      var sc = scan();
      state.history.push({ x: sc.best.x, w: sc.best.w });
      state.fit = sc;
      render(false);
    });

    /* theme and palette changes repaint every Mermaid diagram but know nothing
       of canvases, which bake colour into pixels at draw time. Observe and
       redraw losslessly from state. */
    new MutationObserver(function () { render(false); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
    window.addEventListener('beforeprint', function () { render(true); });
    window.addEventListener('afterprint', function () { render(false); });

    regenerate(PYBMuon.WORLD.SEED);
    render(false);
  }

  function init() {
    document.querySelectorAll('figure.build[data-build="muon"]').forEach(mount);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.PYBMuon = PYBMuon; //exposed for the problems page and its solutions
})();
