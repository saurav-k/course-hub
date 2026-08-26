/* The Sampling Bench - Week 5 build for Probability You Build.
   Six draggable logits over one concrete completion ("The capital of France is ..."),
   softmax rendered as bars that always total 100%, optional temperature slider,
   sample button and token strip, and a naive-vs-stable overflow demonstration.
   Mounts into every figure.build[data-bench]; data-features gates the panels. */
(function () {
  'use strict';

  /* The hub's seeded generator: Math.imul keeps the product in exact 32-bit integer
     arithmetic, so the full 2^32 period survives and every reader draws the same tokens
     from the same seed. */
  function lcg(seed) {
    let s = (seed >>> 0) || 42;
    return function () { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
  }

  /* The concrete completion the bench completes. Fixed vocabulary of six candidates. */
  const PROMPT = 'The capital of France is';
  const TOKENS = [' Paris', ' London', ' Berlin', ' Rome', ' Madrid', ' cheese'];
  const DEFAULT_LOGITS = [3.2, 1.4, 1.1, 0.8, 0.6, -0.5];

  /* softmax with the max-subtraction trick: shift by the max before exponentiating */
  function softmaxStable(logits, T) {
    const m = Math.max.apply(null, logits);
    const ex = logits.map(l => Math.exp((l - m) / T));
    const s = ex.reduce((a, b) => a + b, 0);
    return ex.map(e => e / s);
  }
  /* the same call without the shift - what you would naively write first */
  function softmaxNaive(logits) {
    const ex = logits.map(l => Math.exp(l));
    const s = ex.reduce((a, b) => a + b, 0);
    return ex.map(e => e / s);
  }

  /* colours from CSS tokens at draw time; --l- variants give print-safe ink on paper */
  const probe = document.createElement('span');
  probe.style.display = 'none';
  document.body.appendChild(probe);
  /* An undefined custom property computes to `inherit` for `color`, so a probe reading a
     token that does not exist quietly returns the body text colour and every bar draws the
     same. The fallback makes that loud instead. */
  function col(name, fallback) { probe.style.color = 'var(' + name + ', ' + fallback + ')'; return getComputedStyle(probe).color; }
  function rgb(c) { const m = c.match(/\d+(\.\d+)?/g); return [+m[0], +m[1], +m[2]]; }
  /* --stat has no --l- twin in hub.css, so paper uses --l-accent-2, which does exist. */
  const PAINT = {
    bar:    ['--stat',      '--l-accent-2'],
    altBar: ['--noise',     '--l-ink-soft'],
    ink:    ['--ink',       '--l-ink'],
    faint:  ['--ink-faint', '--l-ink-faint']
  };
  function palette(printSafe) {
    const pick = k => col(PAINT[k][printSafe ? 1 : 0], printSafe ? '#333' : 'currentColor');
    return { bar: rgb(pick('bar')), altBar: rgb(pick('altBar')), ink: pick('ink'), faint: pick('faint') };
  }
  function cssOf(c) { return 'rgb(' + c.map(Math.round).join(',') + ')'; }

  const CW = 680;

  function mount(fig) {
    if (fig.dataset.benchMounted) return;
    fig.dataset.benchMounted = '1';
    const feat = new Set((fig.dataset.features || '').split(',').filter(Boolean));
    const canvas = fig.querySelector('.build-canvas');
    const CH = 300;
    canvas.width = CW; canvas.height = CH;
    const ctx = canvas.getContext('2d');

    const role = r => fig.querySelector('[data-role="' + r + '"]');
    const sliders = Array.from(fig.querySelectorAll('input[type="range"][data-logit]'))
      .sort((a, b) => +a.dataset.logit - +b.dataset.logit);
    const ui = {};
    ['temp', 'sample', 'seed', 'overflow', 'sum', 'tout', 'drawn', 'strip', 'note'].forEach(k => { ui[k] = role(k); });

    const st = { T: ui.temp ? +ui.temp.value : 1.0, rnd: null, drawn: 0 };

    function logits() { return sliders.map(s => +s.value); }
    function probs() { return softmaxStable(logits(), st.T); }

    function draw(printSafe) {
      const P = palette(printSafe);
      ctx.clearRect(0, 0, CW, CH);
      const L = 62, R = 60, BOT = CH - 46, H = BOT - 34;
      const n = TOKENS.length, bw = (CW - L - R) / n;
      const ps = probs();
      /* the leading candidate is whichever logit is currently highest, not whichever
         token happens to sit first: the reader can drag any slider to the top */
      let top = 0;
      for (let i = 1; i < n; i++) if (ps[i] > ps[top]) top = i;
      /* uniform reference: if all six candidates were equally likely, each bar is exactly this high */
      const yU = BOT - (1 / n) * H;
      ctx.font = '11px ui-monospace, monospace';
      /* The axis runs from 0 to the whole of the probability mass, so mark the top: the
         empty space above the tallest bar is headroom, not missing data. */
      ctx.strokeStyle = P.faint; ctx.fillStyle = P.faint;
      ctx.beginPath(); ctx.moveTo(L, BOT - H); ctx.lineTo(L, BOT); ctx.stroke();
      ctx.textAlign = 'right';
      ctx.fillText('100%', L - 6, BOT - H + 10);
      ctx.fillText('0%', L - 6, BOT);
      /* The uniform reference sat at the left margin, directly under the leading bar, so
         its label was unreadable whenever that bar was tall. Put it in the margin instead. */
      ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(L, yU); ctx.lineTo(CW - R, yU); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillText((100 / n).toFixed(1) + '%', L - 6, yU + 4);
      ctx.textAlign = 'left';
      ctx.fillText('uniform', CW - R + 2, yU + 4);
      for (let i = 0; i < n; i++) {
        const x = L + i * bw + bw * 0.18, w = bw * 0.64;
        const h = ps[i] * H;
        ctx.fillStyle = cssOf(i === top ? P.bar : P.altBar);
        ctx.globalAlpha = i === top ? 1 : 0.7;
        ctx.fillRect(x, BOT - h, w, h);
        ctx.globalAlpha = 1;
        ctx.strokeStyle = P.ink; ctx.lineWidth = 0.8; ctx.strokeRect(x + 0.5, BOT - h + 0.5, w - 1, Math.max(h - 1, 1));
        ctx.fillStyle = P.ink; ctx.textAlign = 'center';
        ctx.fillText((ps[i] * 100).toFixed(1) + '%', x + w / 2, BOT - h - 6);
        ctx.fillText(TOKENS[i].trim(), x + w / 2, BOT + 16);
        ctx.fillText('logit ' + (+sliders[i].value).toFixed(1), x + w / 2, BOT + 30);
      }
      ctx.strokeStyle = P.faint;
      ctx.beginPath(); ctx.moveTo(L, BOT + 0.5); ctx.lineTo(CW - R, BOT + 0.5); ctx.stroke();
    }

    function refresh() {
      const ps = probs();
      const total = ps.reduce((a, b) => a + b, 0) * 100;
      if (ui.sum) ui.sum.textContent = total.toFixed(1) + '%';
      if (ui.tout) ui.tout.textContent = String(st.T);
      draw();
    }

    /* inverse-CDF sampling: walk the bars left to right, accumulating probability, and
       stop at the first one whose running total passes the uniform draw. The final index
       is the fallback for the rounding case where the totals stop a hair below u. */
    function sample() {
      if (!st.rnd) st.rnd = lcg(ui.seed ? +ui.seed.value : 42);
      const ps = probs(), n = TOKENS.length;
      const u = st.rnd();
      let acc = 0, pick = n - 1;
      for (let i = 0; i < n; i++) { acc += ps[i]; if (u < acc) { pick = i; break; } }
      st.drawn++;
      if (ui.drawn) ui.drawn.textContent = String(st.drawn);
      if (ui.strip) addChip(TOKENS[pick]);
    }
    function addChip(tok) {
      const d = document.createElement('span');
      d.textContent = tok;
      d.setAttribute('style', [
        'display:inline-block', 'padding:1px 9px', 'margin:2px 3px 2px 0',
        'border-radius:999px', 'font-size:.86em',
        'background:var(--surface-2)', 'color:var(--ink)', 'border:1px solid var(--ink-faint)',
        'opacity:0', 'transform:scale(.85)',
        'transition:opacity .28s ease, transform .28s ease'
      ].join(';'));
      ui.strip.prepend(d);
      while (ui.strip.children.length > 36) ui.strip.removeChild(ui.strip.lastChild);
      requestAnimationFrame(() => requestAnimationFrame(() => { d.style.opacity = '1'; d.style.transform = 'scale(1)'; }));
    }

    sliders.forEach(s => s.addEventListener('input', refresh));
    if (ui.temp) ui.temp.addEventListener('input', () => { st.T = +ui.temp.value; refresh(); });
    if (ui.sample) ui.sample.addEventListener('click', sample);
    if (ui.seed) ui.seed.addEventListener('change', () => { st.rnd = lcg(+ui.seed.value || 42); });
    if (ui.overflow) ui.overflow.addEventListener('click', () => {
      if (!ui.note) return;
      const pushed = logits(); pushed[0] = 1000;
      const naive = softmaxNaive(pushed).map(v => v === 0 ? '0%' : (isFinite(v) ? (v * 100).toFixed(1) + '%' : 'NaN')).join(' ');
      const stable = softmaxStable(pushed, 1).map(v => (v * 100).toFixed(1) + '%').join(' ');
      ui.note.textContent = 'with one logit pushed to 1000 - naive: ' + naive +
        '   max-subtracted: ' + stable;
    });

    new MutationObserver(() => draw(false))
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
    window.addEventListener('beforeprint', () => draw(true));
    window.addEventListener('afterprint', () => draw(false));

    /* prompt caption inside readout so the story is visible without scrolling */
    if (ui.note && !feat.has('overflow')) ui.note.textContent = 'completing: "' + PROMPT + ' ..."';

    refresh();
  }

  function initAll() {
    document.querySelectorAll('figure.build[data-bench]').forEach(mount);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initAll);
  else initAll();
})();
