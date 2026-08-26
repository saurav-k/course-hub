/* The Sampling Bench - Week 5 build for Probability You Build.
   Six draggable logits over one concrete completion ("The capital of France is ..."),
   softmax rendered as bars that always total 100%, optional temperature slider,
   sample button and token strip, and a naive-vs-stable overflow demonstration.
   Mounts into every figure.build[data-bench]; data-features gates the panels. */
(function () {
  'use strict';

  function lcg(seed) {
    let s = seed >>> 0;
    while (s === 0) s = 42;
    return function () { s = (s * 1103515245 + 12345) % 2147483648; return s / 2147483648; };
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
  function col(name) { probe.style.color = 'var(' + name + ')'; return getComputedStyle(probe).color; }
  function rgb(c) { const m = c.match(/\d+(\.\d+)?/g); return [+m[0], +m[1], +m[2]]; }
  function palette(printSafe) {
    const p = printSafe ? '--l-' : '--';
    return {
      bar: rgb(col(p + 'stat')), altBar: rgb(col(p + 'surface-2')),
      ink: col(p + 'ink'), faint: col(p + 'ink-faint')
    };
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
      const L = 56, R = 20, BOT = CH - 46, H = BOT - 34;
      const n = TOKENS.length, bw = (CW - L - R) / n;
      const ps = probs();
      /* uniform reference: if all six candidates were equally likely, each bar is exactly this high */
      const yU = BOT - (1 / n) * H;
      ctx.strokeStyle = P.faint; ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(L, yU); ctx.lineTo(CW - R, yU); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = P.faint; ctx.font = '11px ui-monospace, monospace'; ctx.textAlign = 'left';
      ctx.fillText((100 / n).toFixed(1) + '% = uniform', L + 4, yU - 4);
      for (let i = 0; i < n; i++) {
        const x = L + i * bw + bw * 0.18, w = bw * 0.64;
        const h = ps[i] * H;
        ctx.fillStyle = cssOf(i === 0 ? P.bar : P.altBar);
        ctx.globalAlpha = i === 0 ? 1 : 0.8;
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

    function sample() {
      if (!st.rnd) st.rnd = lcg(ui.seed ? +ui.seed.value : 42);
      const ps = probs();
      let u = st.rnd(), acc = 0, pick = n - 1;
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
