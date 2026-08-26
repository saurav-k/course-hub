/* probability-you-build-course - Week 3 Build 3: the zero-failure paradox.
   A deliberately tiny instrument: n payments, k failures, the binomial
   likelihood over failure probability p, the maximum-likelihood estimate
   p-hat = k/n marked, and - on request - the likelihood interval: every p
   whose log-likelihood sits within 2 units of the peak.
   data-stage="curve"   - lesson 0204: the curve and its peak.
   data-stage="interval" - lesson 0207: the interval control, the boundary.

   The k = 0 case is the whole point: the curve then peaks hard against the
   boundary p = 0, and the honest reading of the data lives in the interval,
   not in the point estimate. */
(function () {
  'use strict';

  /* ============================================================
     CORE - pure functions, no DOM.
     ============================================================ */

  /* Binomial coefficient by the multiplicative loop: factorials overflow
     double precision past 171!, which this course must never hit. */
  function choose(n, k) {
    if (k < 0 || k > n) return 0;
    var r = 1;
    for (var i = 1; i <= k; i++) r = r * (n - k + i) / i;
    return r;
  }

  /* Log-likelihood of k failures in n orders under failure probability p,
     dropping the constant ln C(n,k): LL(p) = k ln p + (n-k) ln(1-p). */
  function logLik(n, k, p) {
    if (p <= 0) return k === 0 ? 0 : -Infinity;
    if (p >= 1) return k === n ? 0 : -Infinity;
    return k * Math.log(p) + (n - k) * Math.log(1 - p);
  }

  /* Every p whose log-likelihood is within `units` of the peak (2 is the
     course's working choice: within a factor e^-2 of the best explanation).
     At an interior peak this returns both ends; at a boundary peak the lower
     end is the boundary itself. Returns null when no p qualifies. */
  function interval(n, k, units) {
    var phat = k / n;
    var peak = logLik(n, k, phat === 0 ? 1e-12 : (phat === 1 ? 1 - 1e-12 : phat));
    var threshold = peak - units;
    var lo = null, hi = null;
    var N = 20000;
    for (var i = 0; i <= N; i++) {
      var p = i / N;
      if (logLik(n, k, p) >= threshold) {
        if (lo === null) lo = p;
        hi = p;
      }
    }
    return lo === null ? null : { lo: lo, hi: hi, peak: peak };
  }

  var PYBRate = { choose: choose, logLik: logLik, interval: interval };

  /* ============================================================
     MOUNTING - skipped entirely outside a browser.
     ============================================================ */
  if (typeof document === 'undefined') {
    if (typeof module !== 'undefined' && module.exports) module.exports = PYBRate;
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

  var PRINT = { bg: '#ffffff', ink: '#1a1a18', inkSoft: '#4a4a44', faint: '#63635b',
                line: '#cccccc', surface: '#ffffff', alarm: '#b23c0a',
                prob: '#4c3fbf', signal: '#136b2c' };

  function mount(figure) {
    if (figure.dataset.rateMounted) return;
    figure.dataset.rateMounted = 'yes';
    var stage = figure.dataset.stage;
    var canvas = figure.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');

    var state = { n: 40, k: 0, showInterval: stage === 'interval' };

    function el(role) { return figure.querySelector('[data-role="' + role + '"]'); }

    function colors(printSafe) {
      if (printSafe) return PRINT;
      return {
        bg: tok('--surface'), ink: tok('--ink'), inkSoft: tok('--ink-soft'),
        faint: tok('--ink-faint'), line: tok('--line'), surface: tok('--surface'),
        surface2: tok('--surface-2'), alarm: tok('--alarm'), prob: tok('--prob')
      };
    }

    var PLOT = { x: 64, y: 26, w: 540, h: 300 };

    function render(printSafe) {
      var C = colors(printSafe);
      ctx.fillStyle = C.bg;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      var n = state.n, k = state.k;
      var phat = n > 0 ? k / n : 0;
      var peakP = phat === 0 ? 1e-12 : (phat === 1 ? 1 - 1e-12 : phat);
      var peak = PYBRate.logLik(n, k, peakP);

      //relative likelihood curve, normalised so the peak is exactly 1
      var pts = [];
      var steps = 600;
      for (var i = 0; i <= steps; i++) {
        var p = i / steps;
        var rel = Math.exp(PYBRate.logLik(n, k, p) - peak);
        pts.push({ p: p, rel: rel });
      }

      //interval band first, so the curve draws over it
      var iv = state.showInterval ? PYBRate.interval(n, k, 2) : null;
      if (iv && iv.hi > iv.lo) {
        var x0 = PLOT.x + iv.lo * PLOT.w;
        var x1 = PLOT.x + iv.hi * PLOT.w;
        ctx.fillStyle = rgba(C.signal, 0.18);
        ctx.fillRect(x0, PLOT.y, x1 - x0, PLOT.h);
        ctx.strokeStyle = C.signal;
        ctx.setLineDash([4, 3]);
        ctx.beginPath();
        ctx.moveTo(x0, PLOT.y); ctx.lineTo(x0, PLOT.y + PLOT.h);
        ctx.moveTo(x1, PLOT.y); ctx.lineTo(x1, PLOT.y + PLOT.h);
        ctx.stroke();
        ctx.setLineDash([]);
      }

      //axes
      ctx.strokeStyle = C.line;
      ctx.beginPath();
      ctx.moveTo(PLOT.x, PLOT.y + PLOT.h); ctx.lineTo(PLOT.x + PLOT.w, PLOT.y + PLOT.h);
      ctx.moveTo(PLOT.x, PLOT.y); ctx.lineTo(PLOT.x, PLOT.y + PLOT.h);
      ctx.stroke();

      //the curve
      ctx.strokeStyle = C.prob;
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      pts.forEach(function (pt, idx) {
        var px = PLOT.x + pt.p * PLOT.w;
        var py = PLOT.y + PLOT.h * (1 - pt.rel);
        if (idx === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      });
      ctx.stroke();
      ctx.lineWidth = 1;

      //p-hat marker
      var hx = PLOT.x + phat * PLOT.w;
      ctx.strokeStyle = C.alarm;
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      ctx.moveTo(hx, PLOT.y + PLOT.h);
      ctx.lineTo(hx, PLOT.y + 14);
      ctx.stroke();
      ctx.lineWidth = 1;
      ctx.fillStyle = C.alarm;
      ctx.font = '12px sans-serif';
      ctx.textAlign = phat < 0.15 ? 'left' : 'center';
      ctx.fillText('MLE p-hat = ' + (Math.round(phat * 1000) / 1000), hx + (phat < 0.15 ? 6 : 0), PLOT.y + 10);

      //axis labels
      ctx.fillStyle = C.inkSoft;
      ctx.textAlign = 'center';
      [0, 0.25, 0.5, 0.75, 1].forEach(function (v) {
        var px = PLOT.x + v * PLOT.w;
        ctx.fillText(String(v), px, PLOT.y + PLOT.h + 18);
      });
      ctx.fillText('hypothesised failure probability p', PLOT.x + PLOT.w / 2, PLOT.y + PLOT.h + 38);
      ctx.textAlign = 'right';
      ctx.fillText('likelihood relative to the peak', PLOT.x - 8, PLOT.y + 4);
      ctx.fillText('1', PLOT.x - 8, PLOT.y + 10);
      ctx.textAlign = 'left';

      updateReadout(iv);
    }

    function updateReadout(iv) {
      var n = state.n, k = state.k;
      var mleEl = el('mle');
      if (mleEl) mleEl.textContent = String(Math.round((k / n) * 1000) / 1000);
      var llEl = el('llpeak');
      if (llEl) {
        var phat = k / n;
        var peak = PYBRate.logLik(n, k, phat === 0 ? 1e-12 : phat);
        llEl.textContent = peak.toFixed(2) + ' (constant terms dropped)';
      }
      var ivEl = el('interval');
      if (ivEl) {
        if (!state.showInterval) { ivEl.textContent = 'hidden'; }
        else if (!iv) { ivEl.textContent = 'empty'; }
        else {
          ivEl.textContent = 'every p from ' + (Math.round(iv.lo * 1000) / 1000) + ' up to ' +
            (Math.round(iv.hi * 1000) / 1000) + ' explains the data within a factor e^-2 of the best';
        }
      }
    }

    function wireRange(role, key, after) {
      var input = el(role);
      if (!input) return;
      input.value = String(state[key]);
      input.addEventListener('input', function () {
        state[key] = +input.value;
        if (key === 'n') {
          var kk = el('k');
          if (kk) {
            kk.max = String(state.n);
            if (state.k > state.n) { state.k = state.n; kk.value = String(state.k); }
          }
        }
        if (after) after();
        render(false);
      });
    }
    wireRange('n', 'n');
    wireRange('k', 'k');

    var cb = el('showiv');
    if (cb) {
      cb.checked = state.showInterval;
      cb.addEventListener('change', function () {
        state.showInterval = cb.checked;
        render(false);
      });
    }

    new MutationObserver(function () { render(false); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
    window.addEventListener('beforeprint', function () { render(true); });
    window.addEventListener('afterprint', function () { render(false); });

    render(false);
  }

  function init() {
    document.querySelectorAll('figure.build[data-build="rate"]').forEach(mount);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.PYBRate = PYBRate;
})();
