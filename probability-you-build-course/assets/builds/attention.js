/* Attention-pattern explorer - Week 5 closing build for Probability You Build.
   A fixed six-token sentence and a frozen matrix of RAW attention scores.
   The reader applies their own sharpened softmax to one chosen row and watches
   the mixing weights redistribute. The pattern is ILLUSTRATIVE, hand-authored in
   the style of published single-head visualisations (cf. BertViz,
   https://bertviz.readthedocs.io/); no trained model's weights are loaded.
   Mounts into figure.build[data-attention]. */
(function () {
  'use strict';

  const SENTENCE = ['The', 'cat', 'sat', 'down', 'because', 'it'];

  /* Frozen data, hand-authored 2026-08-26 as a clearly-labelled illustration
     (BertViz-style single-head pattern). Rows are raw scores BEFORE softmax:
     row i = how strongly token i looks at each earlier-or-self token j. */
  const SCORES = [
    [3.0, 0.4, 0.2, 0.2, 0.1, 0.1],
    [0.8, 2.6, 1.0, 0.6, 0.3, 0.5],
    [0.5, 1.9, 2.4, 1.2, 0.4, 0.6],
    [0.3, 0.9, 1.7, 2.5, 0.5, 0.5],
    [0.4, 0.8, 1.8, 1.1, 2.2, 0.7],
    [0.6, 2.8, 0.7, 0.5, 0.9, 1.4]
  ];

  function col(name) {
    probe.style.color = 'var(' + name + ')';
    return getComputedStyle(probe).color;
  }
  const probe = document.createElement('span');
  probe.style.display = 'none';
  document.body.appendChild(probe);
  function rgb(c) { const m = c.match(/\d+(\.\d+)?/g); return [+m[0], +m[1], +m[2]]; }
  function cssOf(c) { return 'rgba(' + c.join(',') + ')'; }
  function palette(printSafe) {
    const p = printSafe ? '--l-' : '--';
    return { heat: rgb(col(p + 'stat')), ink: col(p + 'ink'), faint: col(p + 'ink-faint'), sel: col(p + 'alarm') };
  }

  const CW = 660, CH = 340;
  const PAD_L = 78, PAD_T = 46, CELL = 44;

  function mount(fig) {
    if (fig.dataset.attMounted) return;
    fig.dataset.attMounted = '1';
    const canvas = fig.querySelector('.build-canvas');
    canvas.width = CW; canvas.height = CH;
    const ctx = canvas.getContext('2d');
    const role = r => fig.querySelector('[data-role="' + r + '"]');
    const ui = {};
    ['beta', 'row', 'tout', 'weights', 'sum'].forEach(k => { ui[k] = role(k); });
    const st = { beta: ui.beta ? +ui.beta.value : 1, row: ui.row ? (+ui.row.value || 0) : 0 };

    /* the reader's own softmax, applied to one row of raw scores.
       Causal: only positions j <= i may receive weight, exactly as drawn. */
    function weights(rowIdx) {
      const visible = SCORES[rowIdx].slice(0, rowIdx + 1);
      const m = Math.max.apply(null, visible);
      const ex = visible.map(s => Math.exp((s - m) * st.beta));
      const tot = ex.reduce((a, b) => a + b, 0);
      return ex.map(e => e / tot);
    }

    function draw(printSafe) {
      const P = palette(printSafe);
      ctx.clearRect(0, 0, CW, CH);
      ctx.font = '12px ui-monospace, monospace';
      ctx.textAlign = 'center'; ctx.fillStyle = P.faint;
      for (let j = 0; j < 6; j++) ctx.fillText(SENTENCE[j], PAD_L + j * CELL + CELL / 2, PAD_T - 10);
      ctx.textAlign = 'right';
      for (let i = 0; i < 6; i++) {
        ctx.fillStyle = i === st.row ? P.sel : P.faint;
        ctx.fillText(SENTENCE[i], PAD_L - 8, PAD_T + i * CELL + CELL / 2 + 4);
      }
      const ws = weights(st.row);
      for (let i = 0; i < 6; i++) {
        const wi = weights(i);
        for (let j = 0; j <= i; j++) {
          const x = PAD_L + j * CELL, y = PAD_T + i * CELL;
          const a = wi[j];
          const selRow = i === st.row;
          ctx.fillStyle = cssOf(P.heat.concat((selRow ? a : a * 0.55).toFixed(3)));
          ctx.fillRect(x + 1, y + 1, CELL - 2, CELL - 2);
          ctx.strokeStyle = selRow ? P.sel : P.faint;
          ctx.lineWidth = selRow ? 1.6 : 0.75;
          ctx.strokeRect(x + 1.5, y + 1.5, CELL - 3, CELL - 3);
          if (a >= 0.08 && (selRow || a >= 0.2)) {
            ctx.fillStyle = a > 0.55 ? '#ffffff' : P.ink;
            ctx.textAlign = 'center';
            ctx.fillText((a * 100).toFixed(0) + '%', x + CELL / 2, y + CELL / 2 + 4);
          }
        }
        /* causal mask: later positions cannot be attended - drawn empty on purpose */
        for (let j = i + 1; j < 6; j++) {
          const x = PAD_L + j * CELL, y = PAD_T + i * CELL;
          ctx.strokeStyle = P.faint; ctx.setLineDash([3, 3]); ctx.lineWidth = 0.75;
          ctx.strokeRect(x + 1.5, y + 1.5, CELL - 3, CELL - 3); ctx.setLineDash([]);
        }
      }
      ctx.fillStyle = P.faint; ctx.textAlign = 'left';
      ctx.font = '11px ui-monospace, monospace';
      ctx.fillText('row = attending token, column = attended token; dashed cells are masked (a token never sees its future)', 8, CH - 8);
    }

    function refresh() {
      const ws = weights(st.row);
      if (ui.weights) ui.weights.textContent = SENTENCE.map((t, j) => t + ' ' + (ws[j] * 100).toFixed(1) + '%').join('   ');
      if (ui.sum) ui.sum.textContent = (ws.reduce((a, b) => a + b, 0) * 100).toFixed(1) + '%';
      if (ui.tout) ui.tout.textContent = String(st.beta);
      draw(false);
    }

    if (ui.beta) ui.beta.addEventListener('input', () => { st.beta = +ui.beta.value; refresh(); });
    if (ui.row) ui.row.addEventListener('change', () => { st.row = +ui.row.value; refresh(); });

    new MutationObserver(() => draw(false))
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
    window.addEventListener('beforeprint', () => draw(true));
    window.addEventListener('afterprint', () => draw(false));

    refresh();
  }

  function initAll() {
    document.querySelectorAll('figure.build[data-attention]').forEach(mount);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initAll);
  else initAll();
})();
