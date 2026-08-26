/* probability-you-build-course - Week 3 Build 2: the cell-phone tracker.
   Position recovered from four noisy signal strengths by maximum likelihood:
   a log-likelihood heatmap over the map, the distance-implied circles,
   and the learner's own hand-coded gradient ascent walking to the peak.
   data-stage="climb"   - lesson 0205: heatmap, circles, ascent, learning rate.
   data-stage="degrade" - lesson 0206: tower removal, error table, bad geometry.

   Sensor model: the log-distance path-loss model with Gaussian shadowing -
   received power P_r(dBm) = P_ref - 10*gamma*log10(d/d_ref) + X_g, X_g ~
   Normal(0, sigma dB). Standard form; see the log-distance path loss model
   article and Rappaport, Wireless Communications: Principles and Practice.
   All constants are teaching constants chosen so four towers land the
   estimate within tens of metres, which is honest for RSSI positioning. */
(function () {
  'use strict';

  /* ============================================================
     CORE - pure functions, no DOM.
     ============================================================ */

  var WORLD = {
    S: 360,
    PREF: -30,
    GAMMA: 3.4,
    SIGMA: 2.0,        //dB shadowing sigma (teaching constant, tuned so four
                       //towers give a compact likelihood blob and honest
                       //tens-of-metres errors)
    DEFAULT_TOWERS: [
      { x: 40,  y: 40,  name: 'A' },
      { x: 320, y: 50,  name: 'B' },
      { x: 60,  y: 310, name: 'C' },
      { x: 300, y: 300, name: 'D' }
    ],
    BAD_TOWERS: [
      { x: 30,  y: 235, name: 'A' },
      { x: 180, y: 265, name: 'B' },
      { x: 330, y: 290, name: 'C' },
      { x: 300, y: 80,  name: 'D' }
    ],
    PHONE: { x: 110, y: 250 },
    SEED: 42,
    LR_DEFAULT: 40,
    LR_BIG: 1800,
    LR_SMALL: 0.5,
    STEPS: 60,
    /* The learning-rate slider is logarithmic so both pathologies are within a
       drag's reach: position u in [0,100] maps to eta = 10^(-0.301 + u/100 * 3.556),
       i.e. u=0 -> eta 0.5 (crawl), u=54 -> eta 40 (default), u=100 -> eta ~1800
       (overshoots and diverges on this surface - measured, lesson 0205). */
    LOG_MIN: -0.301,
    LOG_SPAN: 3.556,
    U_DEFAULT: 54
  };

  /* Seeded PRNG (mulberry32), course convention seed 42. Chosen over a
     classic multiplicative LCG because LCG outputs sit on lattice lines that
     correlate the Box-Muller pairs used below; this generator does not. */
  function makeRng(seed) {
    var a = (seed >>> 0) || 1;
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function makeGauss(rnd) {
    return function () {
      var u = 0, v = 0;
      while (u === 0) u = rnd();
      while (v === 0) v = rnd();
      return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    };
  }

  function rssiPredicted(tower, q) {
    var d = Math.max(1, Math.hypot(tower.x - q.x, tower.y - q.y));
    return WORLD.PREF - 10 * WORLD.GAMMA * Math.log10(d);
  }

  /* One phone broadcast heard by every tower: true signal plus Gaussian
     shadowing noise per tower. */
  function measure(towers, phone, seed) {
    var rnd = makeRng(seed === undefined ? WORLD.SEED : seed);
    var gauss = makeGauss(rnd);
    return towers.map(function (t) {
      var d = Math.max(1, Math.hypot(t.x - phone.x, t.y - phone.y));
      return {
        tower: t.name,
        x: t.x, y: t.y,
        rssi: WORLD.PREF - 10 * WORLD.GAMMA * Math.log10(d) + gauss() * WORLD.SIGMA
      };
    });
  }

  /* Inverts the path-loss equation: the distance one reading implies alone. */
  function impliedDistance(rssi) {
    return Math.pow(10, (WORLD.PREF - rssi) / (10 * WORLD.GAMMA));
  }

  /* LL(q) = -sum (r_i - pred_i)^2 / (2 sigma^2), constants dropped. */
  function logLik(meas, q) {
    var ll = 0;
    for (var i = 0; i < meas.length; i++) {
      var err = meas[i].rssi - rssiPredicted(meas[i], q);
      ll += -(err * err) / (2 * WORLD.SIGMA * WORLD.SIGMA);
    }
    return ll;
  }

  /* The analytic gradient derived on lesson 0205's page:
     dLL/dq = sum_i (r_i - pred_i) * (-10 gamma / ln 10) / (sigma^2 d_i^2) * (q - t_i).
     Divided by the number of measurements: the mean gradient keeps one
     learning rate working across different tower counts (lesson 0206). */
  function gradLL(meas, q) {
    var gx = 0, gy = 0;
    var k = -10 * WORLD.GAMMA / Math.LN10 / (WORLD.SIGMA * WORLD.SIGMA);
    for (var i = 0; i < meas.length; i++) {
      var t = meas[i];
      var d = Math.max(1, Math.hypot(t.x - q.x, t.y - q.y));
      var e = t.rssi - rssiPredicted(t, q);
      gx += e * k * (q.x - t.x) / (d * d);
      gy += e * k * (q.y - t.y) / (d * d);
    }
    return meas.length ? { x: gx / meas.length, y: gy / meas.length }
                       : { x: 0, y: 0 };
  }

  /* The learner's optimiser: evaluate the slope, step uphill, repeat.
     Returns the whole path so the page can draw the walk. */
  function ascend(meas, q0, lr, steps) {
    var q = { x: q0.x, y: q0.y };
    var path = [{ x: q.x, y: q.y }];
    for (var s = 0; s < steps; s++) {
      var g = gradLL(meas, q);
      q = { x: q.x + lr * g.x, y: q.y + lr * g.y };
      if (!isFinite(q.x) || Math.abs(q.x) > 1e6 || Math.abs(q.y) > 1e6) {
        path.push({ x: NaN, y: NaN });
        break;
      }
      path.push({ x: q.x, y: q.y });
    }
    return path;
  }

  var PYBTracker = {
    WORLD: WORLD,
    makeRng: makeRng,
    makeGauss: makeGauss,
    rssiPredicted: rssiPredicted,
    measure: measure,
    impliedDistance: impliedDistance,
    logLik: logLik,
    gradLL: gradLL,
    ascend: ascend
  };

  /* ============================================================
     MOUNTING - skipped entirely outside a browser.
     ============================================================ */
  if (typeof document === 'undefined') {
    if (typeof module !== 'undefined' && module.exports) module.exports = PYBTracker;
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
    return 'rgb(' + Math.round(a[0] + (b[0] - a[0]) * t) + ',' +
      Math.round(a[1] + (b[1] - a[1]) * t) + ',' +
      Math.round(a[2] + (b[2] - a[2]) * t) + ')';
  }

  var PRINT = { bg: '#ffffff', ink: '#1a1a18', inkSoft: '#4a4a44', faint: '#63635b',
                line: '#cccccc', surface: '#ffffff', surface2: '#f2f2ee',
                alarm: '#b23c0a', prob: '#4c3fbf' };

  function mount(figure) {
    if (figure.dataset.trackerMounted) return;
    figure.dataset.trackerMounted = 'yes';
    var canvas = figure.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');

    var MAP = { x: 38, y: 16, w: WORLD.S, h: WORLD.S };

    var state = {
      towers: WORLD.DEFAULT_TOWERS.map(function (t) { return { x: t.x, y: t.y, name: t.name }; }),
      active: [true, true, true, true],
      all: [],
      seed: WORLD.SEED,
      path: null,
      eta: WORLD.LR_DEFAULT,
      history: [],
      timer: null
    };

    function el(role) { return figure.querySelector('[data-role="' + role + '"]'); }
    function activeMeas() {
      return state.all.filter(function (m) {
        var idx = state.towers.findIndex(function (t) { return t.name === m.tower; });
        return idx !== -1 && state.active[idx];
      });
    }
    function remeasure(seedOverride) {
      var seed = seedOverride === undefined ? (+el('seed') && +el('seed').value) || state.seed : seedOverride;
      state.all = PYBTracker.measure(state.towers, WORLD.PHONE, seed);
      state.seed = seed + 1;
      var box = el('seed');
      if (box) box.value = String(state.seed);
    }

    function colors(printSafe) {
      if (printSafe) return PRINT;
      return {
        bg: tok('--surface'), ink: tok('--ink'), inkSoft: tok('--ink-soft'),
        faint: tok('--ink-faint'), line: tok('--line'), surface: tok('--surface'),
        surface2: tok('--surface-2'), alarm: tok('--alarm'), prob: tok('--prob')
      };
    }

    function drawHeat(C, meas) {
      var cell = 5;
      var n = WORLD.S / cell;
      var lo = Infinity, hi = -Infinity;
      var vals = new Float64Array(n * n);
      for (var j = 0; j < n; j++) {
        for (var i = 0; i < n; i++) {
          var v = PYBTracker.logLik(meas, { x: i * cell + cell / 2, y: j * cell + cell / 2 });
          vals[j * n + i] = v;
          if (v < lo) lo = v;
          if (v > hi) hi = v;
        }
      }
      var off = document.createElement('canvas');
      off.width = n; off.height = n;
      var octx = off.getContext('2d');
      for (j = 0; j < n; j++) {
        for (i = 0; i < n; i++) {
          var t = hi > lo ? Math.max(0, (vals[j * n + i] - lo) / (hi - lo)) : 1;
          octx.fillStyle = mix(C.surface2, C.prob, Math.pow(t, 1.4));
          octx.fillRect(i, n - 1 - j, 1, 1);
        }
      }
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(off, MAP.x, MAP.y, MAP.w, MAP.h);
      ctx.imageSmoothingEnabled = true;
      ctx.strokeStyle = C.line;
      ctx.strokeRect(MAP.x, MAP.y, MAP.w, MAP.h);
    }

    function render(printSafe) {
      var C = colors(printSafe);
      var meas = activeMeas();
      ctx.fillStyle = C.bg;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      if (!meas.length) {
        ctx.strokeStyle = C.line;
        ctx.strokeRect(MAP.x, MAP.y, MAP.w, MAP.h);
        ctx.fillStyle = C.faint;
        ctx.font = '13px sans-serif';
        ctx.fillText('tick at least one tower, then re-run the climb.', MAP.x + 24, MAP.y + 44);
        updateReadout(meas);
        return;
      }

      drawHeat(C, meas);

      //distance-implied circles: what each surviving reading says on its own
      ctx.setLineDash([4, 3]);
      ctx.strokeStyle = rgba(C.alarm, 0.65);
      meas.forEach(function (m) {
        ctx.beginPath();
        ctx.arc(MAP.x + m.x, MAP.y + m.y, PYBTracker.impliedDistance(m.rssi), 0, 7);
        ctx.stroke();
      });
      ctx.setLineDash([]);

      //towers
      ctx.font = '12px sans-serif';
      state.towers.forEach(function (t, i) {
        var px = MAP.x + t.x, py = MAP.y + t.y;
        ctx.fillStyle = state.active[i] ? C.ink : C.faint;
        ctx.fillRect(px - 5, py - 5, 10, 10);
        ctx.fillStyle = C.inkSoft;
        ctx.fillText(t.name, px + 8, py - 6);
      });

      //true phone
      ctx.fillStyle = C.alarm;
      ctx.beginPath();
      ctx.arc(MAP.x + WORLD.PHONE.x, MAP.y + WORLD.PHONE.y, 5, 0, 7);
      ctx.fill();
      ctx.fillText('true', MAP.x + WORLD.PHONE.x + 9, MAP.y + WORLD.PHONE.y + 4);

      //the ascent walk
      if (state.path && state.path.length) {
        ctx.strokeStyle = rgba(C.prob, 0.9);
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        var started = false;
        state.path.forEach(function (p) {
          if (!isFinite(p.x)) return;
          var px = MAP.x + p.x, py = MAP.y + p.y;
          if (!started) { ctx.moveTo(px, py); started = true; }
          else ctx.lineTo(px, py);
        });
        ctx.stroke();
        ctx.lineWidth = 1;
        ctx.fillStyle = C.prob;
        for (var s = 0; s < state.path.length; s += 6) {
          var p = state.path[s];
          if (!isFinite(p.x)) break;
          ctx.beginPath();
          ctx.arc(MAP.x + p.x, MAP.y + p.y, 2, 0, 7);
          ctx.fill();
        }
        var est = state.path[state.path.length - 1];
        if (isFinite(est.x)) {
          ctx.strokeStyle = C.ink;
          ctx.lineWidth = 2;
          var ex = MAP.x + est.x, ey = MAP.y + est.y;
          ctx.beginPath();
          ctx.moveTo(ex - 7, ey); ctx.lineTo(ex + 7, ey);
          ctx.moveTo(ex, ey - 7); ctx.lineTo(ex, ey + 7);
          ctx.stroke();
          ctx.lineWidth = 1;
        }
      }

      ctx.fillStyle = C.inkSoft;
      ctx.font = '12px sans-serif';
      ctx.fillText('bright = higher log-likelihood   dashed circle = distance one reading implies', MAP.x, MAP.y + MAP.h + 22);

      updateReadout(meas);
    }

    function updateReadout(meas) {
      var measEl = el('measurements');
      if (measEl) {
        measEl.textContent = meas && meas.length
          ? meas.map(function (m) { return m.tower + '=' + m.rssi.toFixed(1); }).join('  ')
          : '-';
      }
      var errEl = el('error');
      if (errEl) {
        if (state.path && state.path.length && isFinite(state.path[state.path.length - 1].x)) {
          var est = state.path[state.path.length - 1];
          errEl.textContent = '(' + est.x.toFixed(0) + ', ' + est.y.toFixed(0) + '), ' +
            Math.hypot(est.x - WORLD.PHONE.x, est.y - WORLD.PHONE.y).toFixed(1) + ' m from truth';
        } else if (state.path) {
          errEl.textContent = 'diverged off the map';
        } else {
          errEl.textContent = 'not run yet';
        }
      }
      var table = el('etable');
      if (table) {
        var rows = state.history.slice(-8).map(function (h) {
          var errTxt = h.err === Infinity ? 'diverged' : h.err.toFixed(1) + ' m';
          return '<tr><td>' + h.towers + '</td><td>' + errTxt + '</td></tr>';
        }).join('');
        table.innerHTML = '<thead><tr><th>towers used</th><th>final error</th></tr></thead><tbody>' +
          (rows || '<tr><td colspan="2">no runs yet</td></tr>') + '</tbody>';
      }
    }

    function finalError(full) {
      var last = full[full.length - 1];
      return isFinite(last.x)
        ? Math.hypot(last.x - WORLD.PHONE.x, last.y - WORLD.PHONE.y)
        : Infinity;
    }

    /* Animate the walk over roughly a second; theme repaints skip ahead. */
    function animate(full, record) {
      window.clearInterval(state.timer);
      var i = 1;
      state.path = full.slice(0, 1);
      state.timer = window.setInterval(function () {
        i++;
        state.path = full.slice(0, i);
        render(false);
        if (i >= full.length) {
          window.clearInterval(state.timer);
          if (record) state.history.push({ towers: activeMeas().length, err: finalError(full) });
        }
      }, 22);
    }

    function runAscent(record) {
      var meas = activeMeas();
      if (!meas.length) { state.path = null; render(false); return; }
      animate(PYBTracker.ascend(meas, { x: WORLD.S / 2, y: WORLD.S / 2 }, state.eta, WORLD.STEPS), record);
    }

    function wireCheckboxes() {
      figure.querySelectorAll('[data-role="tw"]').forEach(function (box) {
        box.addEventListener('change', function () {
          state.active[+box.value] = box.checked;
          runAscent(true);
        });
      });
    }
    wireCheckboxes();

    var bMeasure = el('remeasure');
    if (bMeasure) bMeasure.addEventListener('click', function () {
      remeasure();
      runAscent(true);
    });
    var bRun = el('run');
    if (bRun) bRun.addEventListener('click', function () { runAscent(false); });

    var eta = el('eta');
    if (eta) {
      eta.value = String(WORLD.U_DEFAULT);
      eta.addEventListener('input', function () {
        state.eta = Math.pow(10, WORLD.LOG_MIN + (+eta.value) / 100 * WORLD.LOG_SPAN);
        var lbl = el('etaval');
        if (lbl) lbl.textContent = state.eta < 10 ? state.eta.toFixed(1) : String(Math.round(state.eta));
      });
      state.eta = Math.pow(10, WORLD.LOG_MIN + WORLD.U_DEFAULT / 100 * WORLD.LOG_SPAN);
      var lbl0 = el('etaval');
      if (lbl0) lbl0.textContent = String(Math.round(state.eta));
    }

    function resetTo(towers) {
      state.towers = towers.map(function (t) { return { x: t.x, y: t.y, name: t.name }; });
      figure.querySelectorAll('[data-role="tw"]').forEach(function (box) { box.checked = true; });
      state.active = [true, true, true, true];
      remeasure();
      runAscent(true);
    }
    var bBad = el('badgeo');
    if (bBad) bBad.addEventListener('click', function () { resetTo(WORLD.BAD_TOWERS); });
    var bGood = el('goodgeo');
    if (bGood) bGood.addEventListener('click', function () { resetTo(WORLD.DEFAULT_TOWERS); });

    new MutationObserver(function () { render(false); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
    window.addEventListener('beforeprint', function () {
      window.clearInterval(state.timer);
      render(true);
    });
    window.addEventListener('afterprint', function () { render(false); });

    remeasure(WORLD.SEED);
    runAscent(true);
  }

  function init() {
    document.querySelectorAll('figure.build[data-build="tracker"]').forEach(mount);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.PYBTracker = PYBTracker;
})();
