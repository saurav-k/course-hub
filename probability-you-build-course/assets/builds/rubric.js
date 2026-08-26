/* probability-you-build-course - Capstone Build: the rubric self-scorer.
   Four axes scored 0-3 (correctness, communication, honesty about uncertainty,
   craft), the capstone pass bar applied live: total >= 8 with no axis at 0.
   The canvas draws one bar per axis so the shape of the score is visible -
   a project can total high and still fail on a single dead axis.

   Exposes PYBRubric.score(scores) as a pure function for lesson prose. */
(function () {
  'use strict';

  /* ============================================================
     CORE - pure functions, no DOM.
     ============================================================ */

  /* scores = { correctness, communication, honesty, craft }, each 0-3.
     Pass bar from the course rubric: total >= 8 AND every axis > 0. */
  function score(s) {
    var axes = ['correctness', 'communication', 'honesty', 'craft'];
    var total = 0;
    var zeros = [];
    for (var i = 0; i < axes.length; i++) {
      var v = Math.max(0, Math.min(3, Math.round(+s[axes[i]] || 0)));
      s[axes[i]] = v;
      total += v;
      if (v === 0) zeros.push(axes[i]);
    }
    return { total: total, zeros: zeros, passes: total >= 8 && zeros.length === 0 };
  }

  /* The rubric's own level names, shared by canvas and prose. */
  var AXES = [
    { key: 'correctness', label: 'Correctness' },
    { key: 'communication', label: 'Communication' },
    { key: 'honesty', label: 'Honesty about uncertainty' },
    { key: 'craft', label: 'Craft' }
  ];

  var PYBRubric = { score: score, AXES: AXES };

  /* ============================================================
     MOUNTING - skipped entirely outside a browser.
     ============================================================ */
  if (typeof document === 'undefined') {
    if (typeof module !== 'undefined' && module.exports) module.exports = PYBRubric;
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
    if (figure.dataset.rubricMounted) return;
    figure.dataset.rubricMounted = 'yes';
    var canvas = figure.querySelector('.build-canvas');
    var ctx = canvas.getContext('2d');

    var state = { correctness: 2, communication: 2, honesty: 1, craft: 2 };

    function el(role) { return figure.querySelector('[data-role="' + role + '"]'); }

    function colors(printSafe) {
      if (printSafe) return PRINT;
      return {
        bg: tok('--surface'), ink: tok('--ink'), inkSoft: tok('--ink-soft'),
        faint: tok('--ink-faint'), line: tok('--line'), surface: tok('--surface'),
        surface2: tok('--surface-2'), alarm: tok('--alarm'), prob: tok('--prob'),
        signal: tok('--signal')
      };
    }

    function render(printSafe) {
      var C = colors(printSafe);
      ctx.fillStyle = C.bg;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      var result = PYBRubric.score(state);

      //one horizontal track per axis, filled to its score out of 3
      var left = 250, top = 40, trackW = 300, barH = 34, gap = 26;
      for (var i = 0; i < PYBRubric.AXES.length; i++) {
        var ax = PYBRubric.AXES[i];
        var y = top + i * (barH + gap);
        var v = state[ax.key];

        ctx.fillStyle = C.inkSoft;
        ctx.font = '13px sans-serif';
        ctx.textAlign = 'left';
        ctx.fillText(ax.label, 30, y + barH / 2 + 4);

        //track
        ctx.fillStyle = C.surface2;
        ctx.fillRect(left, y, trackW, barH);

        //filled part - dead axes painted in alarm colour, alive ones in prob
        if (v > 0) {
          ctx.fillStyle = C.prob;
          ctx.fillRect(left, y, trackW * v / 3, barH);
        } else {
          ctx.strokeStyle = C.alarm;
          ctx.lineWidth = 2;
          ctx.strokeRect(left + 1, y + 1, trackW - 2, barH - 2);
          ctx.fillStyle = C.alarm;
          ctx.font = '12px sans-serif';
          ctx.fillText('zero - automatic fail', left + 10, y + barH / 2 + 4);
          ctx.lineWidth = 1;
        }

        //tick marks and numerals
        ctx.strokeStyle = C.line;
        for (var t = 1; t < 3; t++) {
          ctx.beginPath();
          ctx.moveTo(left + trackW * t / 3, y);
          ctx.lineTo(left + trackW * t / 3, y + barH);
          ctx.stroke();
        }
        ctx.fillStyle = C.faint;
        for (t = 0; t <= 3; t++) {
          ctx.fillText(String(t), left + trackW * t / 3 - 3, y + barH + 14);
        }
        ctx.fillStyle = C.ink;
        ctx.font = 'bold 14px sans-serif';
        ctx.fillText(String(v), left + (v > 0 ? trackW * v / 3 : 0) - (v === 3 ? 16 : -6), y + barH / 2 + 5);
        ctx.font = '13px sans-serif';
      }

      //the pass bar, drawn as a gate under the tracks
      var gy = top + 4 * (barH + gap) + 12;
      ctx.strokeStyle = result.passes ? C.signal : C.alarm;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(left, gy);
      ctx.lineTo(left + trackW, gy);
      ctx.stroke();
      ctx.lineWidth = 1;
      ctx.fillStyle = result.passes ? C.signal : C.alarm;
      ctx.textAlign = 'center';
      ctx.fillText(result.passes ? 'pass bar cleared: total >= 8, no axis at zero'
                                 : 'below the pass bar', left + trackW / 2, gy + 18);
      ctx.textAlign = 'left';

      updateReadout(result);
    }

    function updateReadout(result) {
      for (var i = 0; i < PYBRubric.AXES.length; i++) {
        var cell = el(PYBRubric.AXES[i].key);
        if (cell) cell.textContent = String(state[PYBRubric.AXES[i].key]) + ' / 3';
      }
      var tot = el('total');
      if (tot) tot.textContent = String(result.total) + ' / 12';
      var verd = el('verdict');
      if (verd) {
        verd.textContent = result.passes
          ? 'portfolio-ready bar met'
          : (result.total >= 8 && result.zeros.length > 0
            ? 'total is enough but ' + result.zeros.join(', ') + ' sits at zero - automatic fail'
            : 'not yet: raise the flagged axes');
      }
    }

    ['correctness', 'communication', 'honesty', 'craft'].forEach(function (key) {
      var input = el(key);
      if (!input) return;
      input.value = String(state[key]);
      input.addEventListener('input', function () {
        state[key] = +input.value;
        render(false);
      });
    });

    new MutationObserver(function () { render(false); })
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
    window.addEventListener('beforeprint', function () { render(true); });
    window.addEventListener('afterprint', function () { render(false); });

    render(false);
  }

  function init() {
    document.querySelectorAll('figure.build[data-build="rubric"]').forEach(mount);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  window.PYBRubric = PYBRubric;
})();
