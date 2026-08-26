/* The Audit Bench - Week 6 of Probability You Build.
   One script mounts every panel of the week's build, keyed by figure id:
     ab-baserate    lesson 0500 - accuracy against the always-no baseline
     ab-matrix      lesson 0501 - confusion matrix and its six rates
     ab-curves      lesson 0502 - PR and ROC panels, AUC, the degenerate case
     ab-reliability lesson 0503 - reliability diagram, ECE, binning fragility
     ab-temp        lesson 0504 - temperature scaling and the invariance proof
     ab-scores      lesson 0505 - Brier, Murphy decomposition, log loss
     ab-groups      lesson 0506 - group rates, fairness gaps, the collision
     ab-ci          lesson 0507 - bootstrap confidence intervals
     ab-card        lesson 0508 - the full bench feeding the printable audit card

   Computational core ported from data/pai-w56/prototypes/proto_audit.html
   (seeded LCG generator seed 7, grid temperature fit 0.05..6 step .01,
   accuracy-invariance check). Two deliberate departures from the prototype,
   both noted in the PR: (1) the reliability diagram and ECE use the standard
   observed positive frequency per bin (design report W6.2 concept 6-7;
   Guo et al. 2017 arXiv:1706.04599, Sec. 4 reliability form), not the
   prototype's "fraction correctly flagged", which is threshold-dependent;
   (2) every dataset gets its own seeded LCG so quoted numbers reproduce
   independently of call order. All quoted page numbers were verified against
   this exact code under node before publication. */
'use strict';

/*==CORE==*/
function AB_lcg(s){
  return {
    s: s >>> 0,
    next(){ this.s = (this.s * 1103515245 + 12345) % 2147483648; return this.s / 2147483648; },
    gauss(){ let u = 0, v = 0;
      while (!u) u = this.next();
      while (!v) v = this.next();
      return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
  };
}
const AB_sig   = z => 1 / (1 + Math.exp(-z));
const AB_logit = p => Math.log(p / (1 - p));

/* Datasets. Each is a fixed seeded population of rows {g, y, logit}. */
function AB_makePop(R, n){          // two groups, prevalences .30/.55, overconfident-compressed scorer
  const rows = [];
  for (let i = 0; i < n; i++){
    const g = R.next() < 0.7 ? 0 : 1;
    const y = R.next() < (g === 0 ? 0.30 : 0.55) ? 1 : 0;
    const q = y ? 0.9 + R.gauss() * 0.9 : -0.9 + R.gauss() * 0.9;
    rows.push({ g, y, logit: q * 1.4 + R.gauss() * 0.35 });
  }
  return rows;
}
function AB_makeControl(R, n){      // same signal, honest posterior from the generator's own densities
  const rows = [];
  for (let i = 0; i < n; i++){
    const g = R.next() < 0.7 ? 0 : 1;
    const prev = g === 0 ? 0.30 : 0.55;
    const y = R.next() < prev ? 1 : 0;
    const q = y ? 0.9 + R.gauss() * 0.9 : -0.9 + R.gauss() * 0.9;
    const l1 = Math.exp(-((q - 0.9) ** 2) / (2 * 0.81));
    const l0 = Math.exp(-((q + 0.9) ** 2) / (2 * 0.81));
    const post = (l1 * prev) / (l1 * prev + l0 * (1 - prev));
    rows.push({ g, y, logit: AB_logit(post) });
  }
  return rows;
}
function AB_makeRare(R, n){         // fraud-style, prevalence 0.02
  const rows = [];
  for (let i = 0; i < n; i++){
    const y = R.next() < 0.02 ? 1 : 0;
    const q = y ? 0.9 + R.gauss() * 0.9 : -0.9 + R.gauss() * 0.9;
    rows.push({ g: 0, y, logit: q * 1.4 + R.gauss() * 0.35 });
  }
  return rows;
}
function AB_makeDegenerate(R, n){   // perfect ranking squashed into [~.505, ~.515]: AUC 1, useless at t=.5
  const rows = [];
  for (let i = 0; i < n; i++){
    const y = R.next() < 0.5 ? 1 : 0;
    const q = y ? 1.0 : -1.0;
    const rank = AB_sig((q + R.gauss() * 0.15) * 3);
    const p = 0.505 + 0.010 * rank;
    rows.push({ g: i % 2, y, logit: AB_logit(p) });
  }
  return rows;
}
function AB_baseRateScorer(rows){   // knows NOTHING but each group's prevalence: perfectly calibrated within group
  return rows.map(r => {
    const p = r.g === 0 ? 0.30 : 0.55;
    return { g: r.g, y: r.y, logit: AB_logit(p) };
  });
}

const AB_DATA = {
  pop:   AB_makePop(AB_lcg(7), 2000),
  ctrl:  AB_makeControl(AB_lcg(17), 2000),
  rare:  AB_makeRare(AB_lcg(42), 2000),
  degen: AB_makeDegenerate(AB_lcg(43), 2000)
};

/* Everything measured at a temperature T and threshold thr.
   nb = number of equal-width probability bins for the reliability/ECE stats
   (ECE inherits binning arbitrariness; lesson 0503 makes that visible). */
function AB_metrics(rows, T, thr, nb){
  nb = nb || 10;
  let tp = 0, fp = 0, tn = 0, fn = 0, brier = 0, ll = 0;
  const bins = new Array(nb).fill(0).map(() => ({ n: 0, pos: 0, conf: 0 }));
  for (const r of rows){
    const p = AB_sig(r.logit / T);
    const d = p >= thr ? 1 : 0;
    if (d && r.y) tp++; else if (d && !r.y) fp++; else if (!d && !r.y) tn++; else fn++;
    const bi = Math.min(nb - 1, Math.floor(p * nb));
    bins[bi].n++; bins[bi].pos += r.y; bins[bi].conf += p;
    brier += (p - r.y) ** 2;
    ll    += -(r.y * Math.log(p + 1e-12) + (1 - r.y) * Math.log(1 - p + 1e-12));
  }
  const n = rows.length;
  let ece = 0;
  for (const b of bins) if (b.n) ece += b.n / n * Math.abs(b.pos / b.n - b.conf / b.n);
  return {
    n, tp, fp, tn, fn,
    acc: (tp + tn) / n, tpr: tp / (tp + fn), fpr: fp / (fp + tn),
    fnr: fn / (fn + tp), tnr: tn / (tn + fp),
    prec: tp + fp ? tp / (tp + fp) : NaN, npv: tn + fn ? tn / (tn + fn) : NaN,
    sel: (tp + fp) / n,
    ece, brier: brier / n, nll: ll / n, bins
  };
}

/* Murphy decomposition of the Brier score (Murphy 1973):
   Brier ~= uncertainty - resolution + reliability, binning-approximated. */
function AB_murphy(m){
  const pi = m.bins.reduce((a, b) => a + b.pos, 0) / m.n;
  let rel = 0, res = 0;
  for (const b of m.bins) if (b.n){
    const ob = b.pos / b.n;
    rel += b.n / m.n * (ob - b.conf / b.n) ** 2;
    res += b.n / m.n * (ob - pi) ** 2;
  }
  return { pi, unc: pi * (1 - pi), rel, res };
}

/* ROC and PR points at temperature T, AUC by trapezoid, AP by step integral. */
function AB_curves(rows, T){
  const pts = rows.map(r => ({ p: AB_sig(r.logit / T), y: r.y })).sort((a, b) => b.p - a.p);
  let P = 0, N = 0;
  for (const r of pts) r.y ? P++ : N++;
  const roc = [[0, 0]], pr = [[0, 1]];
  let tp = 0, fp = 0, i = 0, lastRec = 0, ap = 0;
  while (i < pts.length){
    const p0 = pts[i].p;
    while (i < pts.length && pts[i].p === p0){ pts[i].y ? tp++ : fp++; i++; }
    const rec = tp / P, prec = tp / (tp + fp);
    ap += (rec - lastRec) * prec; lastRec = rec;
    roc.push([fp / N, rec]);
    pr.push([rec, prec]);
  }
  let auc = 0;
  for (let k = 1; k < roc.length; k++)
    auc += (roc[k][0] - roc[k - 1][0]) * (roc[k][1] + roc[k - 1][1]) / 2;
  return { roc, pr, auc, ap };
}

/* Temperature fit: minimise mean log loss on a held-out split (grid, as prototyped). */
function AB_split(rows, frac){
  const rs = rows.slice();
  const R = AB_lcg(5);
  for (let i = rs.length - 1; i > 0; i--){
    const j = (R.next() * (i + 1)) | 0;
    [rs[i], rs[j]] = [rs[j], rs[i]];
  }
  const k = Math.round(rs.length * frac);
  return { fit: rs.slice(0, k), test: rs.slice(k) };
}
function AB_fitT(rows){
  let best = 1, bestNLL = Infinity;
  for (let T = 0.05; T < 6; T += 0.01){
    const m = AB_metrics(rows, T, 0.5);
    if (m.nll < bestNLL){ bestNLL = m.nll; best = T; }
  }
  return best;
}

/* Group-wise rates at ONE declared threshold. */
function AB_groupRates(rows, T, thr){
  const out = {};
  for (const g of [0, 1]){
    const rs = rows.filter(r => r.g === g);
    if (!rs.length){ out[g] = null; continue; }
    const m = AB_metrics(rs, T, thr);
    out[g] = { n: rs.length, prev: rs.reduce((a, r) => a + r.y, 0) / rs.length,
               sel: m.sel, tpr: m.tpr, fpr: m.fpr, ppv: m.prec };
  }
  return out;
}

/* Bootstrap CI with its own seeded stream so two readers print identical intervals. */
function AB_bootCI(rows, B, scoreFn, seedVal){
  const R = AB_lcg(seedVal == null ? 99 : seedVal);
  const n = rows.length, vals = [];
  for (let b = 0; b < B; b++){
    const sample = new Array(n);
    for (let i = 0; i < n; i++) sample[i] = rows[(R.next() * n) | 0];
    vals.push(scoreFn(sample));
  }
  vals.sort((a, b) => a - b);
  return [vals[Math.floor(0.025 * B)], vals[Math.floor(0.975 * B)]];
}
/*==CORE-END==*/

/* ---------- drawing helpers ---------- */
const AB_PRINT = false;                 // flipped true while printing
function AB_tok(name){
  if (AB_PRINT){                        // print-safe ink on white paper (NOTES.md gotcha fix)
    switch (name){
      case '--ink': case '--ink-soft': return '#1c1c1c';
      case '--ink-faint': return '#777';
      case '--line': return '#bbb'; case '--line-strong': return '#888';
      case '--surface': case '--bg': return '#ffffff';
      case '--accent': case '--stat': return '#0f6e73';
      case '--accent-2': return '#333';
      case '--ok': return '#136b2c';
      case '--warn': return '#b23c0a';
      case '--prob': return '#444';
      case '--gold': return '#7a5a0a';
      default: return '#444';
    }
  }
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || '#888';
}
function AB_font(mono, px){
  const fam = AB_tok(mono ? '--mono' : '--sans') || 'system-ui';
  return px + 'px ' + fam;
}
function AB_setup(canvas){
  const c = canvas.getContext('2d');
  c.clearRect(0, 0, canvas.width, canvas.height);
  c.fillStyle = AB_tok('--surface');
  c.fillRect(0, 0, canvas.width, canvas.height);
  c.lineWidth = 1;
  return c;
}
function AB_frame(c, w, h, pad, xlab, ylab){
  c.strokeStyle = AB_tok('--line');
  c.strokeRect(pad, pad, w - pad * 2, h - pad * 2);
  c.fillStyle = AB_tok('--ink-soft');
  c.font = AB_font(true, 11);
  if (xlab) c.fillText(xlab, w / 2 - c.measureText(xlab).width / 2, h - 8);
  if (ylab){
    c.save();
    c.translate(12, h / 2 + c.measureText(ylab).width / 2);
    c.rotate(-Math.PI / 2);
    c.fillText(ylab, 0, 0);
    c.restore();
  }
}
const AB_fmt = (v, d = 4) => (v == null || Number.isNaN(v)) ? '-' : (+v).toFixed(d);

/* ---------- registry ---------- */
const AB_FIGS = [];
function AB_reg(id, wire, render){
  const fig = document.getElementById(id);
  if (!fig || fig.dataset.abInit) return;
  fig.dataset.abInit = '1';
  const S = { fig, render };
  fig.querySelectorAll('[data-role]').forEach(el => {
    const role = el.dataset.role;
    if (el.tagName === 'BUTTON') el.addEventListener('click', () => wire.click(S, role));
    else el.addEventListener('input', () => wire.input(S, role));
  });
  AB_FIGS.push(S);
  if (wire.init) wire.init(S);
  render(S);
}
function AB_role(fig, name){ const el = fig.querySelector('[data-role="' + name + '"]'); return el; }
function AB_readout(fig){ return fig.querySelector('.build-readout'); }
function AB_setReadout(fig, pairs){
  const ro = AB_readout(fig);
  ro.innerHTML = pairs.map(([k, v]) => '<span>' + k + ' <b>' + v + '</b></span>').join('');
}
function AB_renderAll(){ for (const S of AB_FIGS) S.render(S); }

new MutationObserver(AB_renderAll)
  .observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
window.addEventListener('beforeprint', () => { AB_PRINT = true; AB_renderAll(); });
window.addEventListener('afterprint',  () => { AB_PRINT = false; AB_renderAll(); });

/*==FIGURES==*/
/* Lesson 0500 - accuracy against the always-no baseline. */
AB_reg('ab-baserate', {
  input(S, role){
    if (role === 'dataset') S.rows = AB_DATA[S.fig.querySelector('[data-role="dataset"]').value];
    if (role === 'thr'){ /* slider */ }
    S.render(S);
  },
  click(S){ S.render(S); },
  init(S){
    S.rows = AB_DATA[S.fig.querySelector('[data-role="dataset"]').value];
  }
}, function (S){
  const cv = S.fig.querySelector('canvas'), c = AB_setup(cv);
  const thr = +AB_role(S.fig, 'thr').value;
  const m = AB_metrics(S.rows, 1, thr);
  const alwaysNo = 1 - S.rows.reduce((a, r) => a + r.y, 0) / m.n;
  const w = cv.width, h = cv.height, pad = 46;
  const bw = w - pad * 2;
  const barY = [70, 130], barH = 34;
  // two horizontal bars scaled 0..1
  const bars = [
    ['always say no', alwaysNo, AB_tok('--ink-faint')],
    ['model @ t=' + thr.toFixed(2), m.acc, AB_tok('--accent')]
  ];
  c.font = AB_font(false, 12);
  bars.forEach(([lab, v, col], k) => {
    const y = barY[k];
    c.fillStyle = AB_tok('--ink');
    c.textAlign = 'left';
    c.fillText(lab, pad, y - 6);
    c.fillStyle = AB_tok('--surface-2') || AB_tok('--surface');
    c.fillRect(pad, y, bw, barH);
    c.fillStyle = col;
    c.fillRect(pad, y, bw * v, barH);
    c.strokeStyle = AB_tok('--line-strong');
    c.strokeRect(pad, y, bw, barH);
    c.fillStyle = AB_tok('--ink');
    c.font = AB_font(true, 13);
    c.fillText(v.toFixed(4), pad + bw * v + 6, y + barH / 2 + 4);
    c.font = AB_font(false, 12);
  });
  // flag composition bar: what the model's flags are made of
  const fy = 210, fw = bw * ((m.tp + m.fp) / m.n || 0);
  c.fillStyle = AB_tok('--ink');
  c.fillText('the flags themselves (' + (m.tp + m.fp) + ' of ' + m.n + ' rows)', pad, fy - 6);
  if (fw > 0){
    const tpw = fw * (m.tp / (m.tp + m.fp));
    c.fillStyle = AB_tok('--ok');    c.fillRect(pad, fy, tpw, barH);
    c.fillStyle = AB_tok('--warn');  c.fillRect(pad + tpw, fy, fw - tpw, barH);
    c.strokeStyle = AB_tok('--line-strong'); c.strokeRect(pad, fy, fw, barH);
    c.font = AB_font(true, 12);
    c.fillStyle = AB_tok('--ink');
    if (tpw > 60) c.fillText('true ' + m.tp, pad + 6, fy + barH / 2 + 4);
    if (fw - tpw > 90) c.fillText('false ' + m.fp, pad + tpw + 6, fy + barH / 2 + 4);
  } else {
    c.font = AB_font(true, 12);
    c.fillText('no flags at all: every row released', pad, fy + barH / 2 + 4);
  }
  AB_frame(c, w, h, pad, null, null);
  AB_setReadout(S.fig, [
    ['model accuracy', m.acc.toFixed(4)],
    ['always-no accuracy', alwaysNo.toFixed(4)],
    ['baseline wins by', Math.max(0, alwaysNo - m.acc).toFixed(4)],
    ['precision', AB_fmt(m.prec)],
    ['recall', m.tpr.toFixed(3)]
  ]);
});

/* Lesson 0501 - the confusion matrix and its six rates. */
AB_reg('ab-matrix', {
  input(S){
    S.rows = AB_DATA[AB_role(S.fig, 'dataset').value];
    S.render(S);
  },
  click(S){ S.render(S); },
  init(S){ S.rows = AB_DATA[AB_role(S.fig, 'dataset').value]; }
}, function (S){
  const cv = S.fig.querySelector('canvas'), c = AB_setup(cv);
  const thr = +AB_role(S.fig, 'thr').value;
  const m = AB_metrics(S.rows, 1, thr);
  const w = cv.width, h = cv.height;
  const gx = 40, gy = 52, cell = Math.min(120, (h - gy - 60) / 2), gap = 6;
  const cells = [
    ['TN', m.tn, gx, gy], ['FP', m.fp, gx + cell + gap, gy],
    ['FN', m.fn, gx, gy + cell + gap], ['TP', m.tp, gx + cell + gap, gy + cell + gap]
  ];
  const maxCell = Math.max(m.tp, m.fp, m.tn, m.fn) || 1;
  c.font = AB_font(true, 15);
  for (const [lab, v, x, y] of cells){
    c.globalAlpha = 0.18 + 0.62 * (v / maxCell);
    c.fillStyle = (lab === 'TP' || lab === 'TN') ? AB_tok('--ok') : AB_tok('--warn');
    c.fillRect(x, y, cell, cell);
    c.globalAlpha = 1;
    c.strokeStyle = AB_tok('--line-strong');
    c.strokeRect(x, y, cell, cell);
    c.fillStyle = AB_tok('--ink');
    c.fillText(lab + ' ' + v, x + 10, y + 22);
  }
  c.font = AB_font(false, 11);
  c.fillStyle = AB_tok('--ink-soft');
  c.fillText('predicted NO', gx, gy - 26); c.fillText('predicted YES', gx + cell + gap, gy - 26);
  c.save(); c.translate(gx - 14, gy + cell + 10); c.rotate(-Math.PI / 2);
  c.fillText('actually YES', 0, 0); c.restore();
  c.save(); c.translate(gx - 14, gy + cell - cell / 2 + 10); c.rotate(-Math.PI / 2);
  c.fillText('actually NO', 0, 0); c.restore();
  c.font = AB_font(false, 12);
  c.fillStyle = AB_tok('--ink');
  c.fillText('threshold t = ' + thr.toFixed(2), gx + cell * 2 + gap + 24, gy + 14);
  const rates = [
    ['sensitivity / TPR', m.tpr], ['specificity / TNR', m.tnr],
    ['FPR', m.fpr], ['FNR', m.fnr], ['PPV', m.prec], ['NPV', m.npv]
  ];
  c.font = AB_font(true, 12);
  rates.forEach(([lab, v], k) => {
    const y = gy + 40 + k * 24;
    c.fillStyle = AB_tok('--ink-soft'); c.textAlign = 'left';
    c.fillText(lab.padEnd(18), gx + cell * 2 + gap + 24, y);
    c.fillStyle = AB_tok('--accent-2');
    c.fillText(v.toFixed(3), gx + cell * 2 + gap + 168, y);
  });
  AB_frame(c, w, h, 20, null, null);
  AB_setReadout(S.fig, [
    ['accuracy', m.acc.toFixed(4)],
    ['prevalence', (m.tp + m.fn) / m.n > 0 ? ((m.tp + m.fn) / m.n).toFixed(3) : '-'],
    ['selection rate', m.sel.toFixed(3)],
    ['TP+FP+TN+FN', m.tp + m.fp + m.tn + m.fn],
    ['t', thr.toFixed(2)]
  ]);
});

/* Lesson 0502 - PR and ROC panels; the degenerate perfect AUC. */
AB_reg('ab-curves', {
  input(S){
    S.rows = AB_DATA[AB_role(S.fig, 'dataset').value];
    S.render(S);
  },
  click(S){ S.render(S); },
  init(S){ S.rows = AB_DATA[AB_role(S.fig, 'dataset').value]; }
}, function (S){
  const cv = S.fig.querySelector('canvas'), c = AB_setup(cv);
  const thr = +AB_role(S.fig, 'thr').value;
  const rows = S.rows;
  const cvx = AB_curves(rows, 1);
  const m = AB_metrics(rows, 1, thr);
  const w = cv.width, h = cv.height, pad = 42;
  const pw = (w - pad * 3) / 2, ph = h - pad * 2 - 14;
  function panel(x0, pts, diag){
    c.strokeStyle = AB_tok('--line');
    c.strokeRect(x0, pad, pw, ph);
    if (diag){
      c.save();
      c.strokeStyle = AB_tok('--ink-faint');
      c.setLineDash([4, 4]);
      c.beginPath(); c.moveTo(x0, pad + ph); c.lineTo(x0 + pw, pad); c.stroke();
      c.restore();
    }
    c.strokeStyle = AB_tok('--stat');
    c.lineWidth = 1.8;
    c.beginPath();
    pts.forEach(([u, v], k) => {
      const X = x0 + u * pw, Y = pad + ph - v * ph;
      k ? c.lineTo(X, Y) : c.moveTo(X, Y);
    });
    c.stroke();
    c.lineWidth = 1;
  }
  // left: precision-recall; right: ROC
  panel(pad, cvx.pr, false);
  panel(pad * 2 + pw, cvx.roc, true);
  // current threshold markers: the curve point at t
  const prec = m.prec, rec = m.tpr, fpr = m.fpr;
  c.fillStyle = AB_tok('--alarm') || AB_tok('--warn');
  c.beginPath();
  c.arc(pad + rec * pw, pad + ph - prec * ph, 4.5, 0, 7);
  c.fill();
  c.beginPath();
  c.arc(pad * 2 + pw + fpr * pw, pad + ph - rec * ph, 4.5, 0, 7);
  c.fill();
  c.font = AB_font(false, 12);
  c.fillStyle = AB_tok('--ink');
  c.fillText('precision-recall', pad + pw / 2 - 46, pad - 10);
  c.fillText('ROC', pad * 2 + pw + pw / 2 - 12, pad - 10);
  c.font = AB_font(true, 11);
  c.fillStyle = AB_tok('--ink-soft');
  c.fillText('t=' + thr.toFixed(2), pad + Math.min(pw - 40, rec * pw + 6), pad + ph - prec * ph - 8);
  AB_setReadout(S.fig, [
    ['AUC', cvx.auc.toFixed(4)],
    ['avg precision', cvx.ap.toFixed(4)],
    ['precision @ t', AB_fmt(prec)],
    ['recall @ t', rec.toFixed(3)],
    ['flags everyone?', (m.sel > 0.999 ? 'yes - every row is above t' : 'no')]
  ]);
});

/* Lesson 0503 - reliability diagram, ECE, and binning fragility. */
AB_reg('ab-reliability', {
  input(S){
    const v = AB_role(S.fig, 'dataset').value;
    S.rows = v === 'baserate' ? AB_baseRateScorer(AB_DATA.pop) : AB_DATA[v];
    S.nb = +AB_role(S.fig, 'bins').value || 10;
    S.render(S);
  },
  click(S){ S.render(S); },
  init(S){
    const v = AB_role(S.fig, 'dataset').value;
    S.rows = v === 'baserate' ? AB_baseRateScorer(AB_DATA.pop) : AB_DATA[v];
    S.nb = 10;
  }
}, function (S){
  const cv = S.fig.querySelector('canvas'), c = AB_setup(cv);
  if (S.nb == null) S.nb = 10;
  const m = AB_metrics(S.rows, 1, 0.5, S.nb);
  const w = cv.width, h = cv.height, pad = 46;
  const gw = w - pad * 2, gh = h - pad * 2;
  c.strokeStyle = AB_tok('--line');
  c.strokeRect(pad, pad, gw, gh);
  // perfect-calibration diagonal
  c.save();
  c.strokeStyle = AB_tok('--ink-faint');
  c.setLineDash([4, 4]);
  c.beginPath(); c.moveTo(pad, pad + gh); c.lineTo(pad + gw, pad); c.stroke();
  c.restore();
  // per-bin points with stems to the diagonal
  let worst = { gap: -1 };
  m.bins.forEach(b => {
    if (!b.n) return;
    const conf = b.conf / b.n, obs = b.pos / b.n;
    const gap = Math.abs(obs - conf);
    if (gap > worst.gap) worst = { gap, conf, obs, n: b.n };
    const X = pad + conf * gw, Y = pad + gh - obs * gh;
    c.strokeStyle = AB_tok('--gold');
    c.beginPath(); c.moveTo(X, pad + gh - conf * gh); c.lineTo(X, Y); c.stroke();
    c.fillStyle = AB_tok('--accent');
    c.beginPath(); c.arc(X, Y, 3 + Math.min(6, Math.sqrt(b.n)), 0, 7); c.fill();
  });
  c.font = AB_font(false, 11);
  c.fillStyle = AB_tok('--ink-soft');
  c.fillText('predicted probability', w / 2 - 52, h - 8);
  c.save();
  c.translate(12, h / 2 + 44); c.rotate(-Math.PI / 2);
  c.fillText('observed frequency', 0, 0);
  c.restore();
  c.font = AB_font(true, 12);
  c.fillStyle = AB_tok('--ink');
  c.fillText('ECE = ' + m.ece.toFixed(4), pad + 10, pad + 18);
  c.font = AB_font(true, 10);
  c.fillStyle = AB_tok('--ink-soft');
  c.fillText(m.nb + ' bins, counts ' + m.bins.filter(b => b.n).map(b => b.n).join('/'), pad + 10, pad + 34);
  AB_setReadout(S.fig, [
    ['ECE (' + m.nb + ' bins)', m.ece.toFixed(4)],
    ['worst bin gap', worst.gap >= 0 ? worst.gap.toFixed(3) : '-'],
    ['worst bin mean p / observed', worst.gap >= 0 ? worst.conf.toFixed(2) + ' / ' + worst.obs.toFixed(2) : '-'],
    ['rows', m.n]
  ]);
});

/* Lesson 0504 - temperature scaling on held-out data; the invariance proof. */
AB_reg('ab-temp', {
  input(S, role){
    if (role === 'split'){ S.fitted = null; }   // split moved: refit required
    S.render(S);
  },
  click(S, role){
    if (role === 'fit'){
      const frac = (+AB_role(S.fig, 'split').value) / 100;
      const sp = AB_split(S.rows || AB_DATA.pop, frac);
      S.T = AB_fitT(sp.fit);
      S.before = AB_metrics(sp.test, 1, 0.5);
      S.after = AB_metrics(sp.test, S.T, 0.5);
      S.nFit = sp.fit.length; S.nTest = sp.test.length;
    }
    if (role === 'reset'){ S.T = null; S.before = S.after = null; }
    S.render(S);
  },
  init(S){ S.rows = AB_DATA.pop; S.T = null; }
}, function (S){
  const cv = S.fig.querySelector('canvas'), c = AB_setup(cv);
  const w = cv.width, h = cv.height, pad = 46;
  const gw = w - pad * 2, gh = h - pad * 2;
  c.strokeStyle = AB_tok('--line');
  c.strokeRect(pad, pad, gw, gh);
  c.save();
  c.strokeStyle = AB_tok('--ink-faint');
  c.setLineDash([4, 4]);
  c.beginPath(); c.moveTo(pad, pad + gh); c.lineTo(pad + gw, pad); c.stroke();
  c.restore();
  function plotSeries(mm, col){
    mm.bins.forEach(b => {
      if (!b.n) return;
      const conf = b.conf / b.n, obs = b.pos / b.n;
      const X = pad + conf * gw, Y = pad + gh - obs * gh;
      c.strokeStyle = col;
      c.beginPath(); c.moveTo(X, pad + gh - conf * gh); c.lineTo(X, Y); c.stroke();
      c.fillStyle = col;
      c.beginPath(); c.arc(X, Y, 4, 0, 7); c.fill();
    });
  }
  if (S.before && S.after && S.T){
    plotSeries(S.before, AB_tok('--prob'));
    plotSeries(S.after, AB_tok('--ok'));
    c.font = AB_font(true, 12);
    c.fillStyle = AB_tok('--prob');
    c.fillText('before T=1', pad + gw - 150, pad + 20);
    c.fillStyle = AB_tok('--ok');
    c.fillText('after T*=' + S.T.toFixed(2), pad + gw - 150, pad + 38);
    const sameAcc = S.before.acc === S.after.acc &&
                    S.before.tp === S.after.tp && S.before.fp === S.after.fp;
    AB_setReadout(S.fig, [
      ['T* (fit on ' + S.nFit + ' held-out rows)', S.T.toFixed(2)],
      ['ECE on ' + S.nTest + ' test rows', S.before.ece.toFixed(4) + ' -> ' + S.after.ece.toFixed(4)],
      ['Brier', S.before.brier.toFixed(4) + ' -> ' + S.after.brier.toFixed(4)],
      ['log loss', S.before.nll.toFixed(4) + ' -> ' + S.after.nll.toFixed(4)],
      ['accuracy', S.before.acc.toFixed(4) + ' -> ' + S.after.acc.toFixed(4)],
      ['unchanged?', sameAcc ? 'true (bit-identical confusion matrix)' : 'FALSE']
    ]);
  } else {
    plotSeries(AB_metrics(S.rows, 1, 0.5), AB_tok('--prob'));
    c.font = AB_font(true, 12);
    c.fillStyle = AB_tok('--ink-soft');
    c.fillText('press Fit T - the fit uses only its half of the rows', pad + 12, pad + 20);
    AB_setReadout(S.fig, [['state', 'unscaled (T=1)']]);
  }
});
