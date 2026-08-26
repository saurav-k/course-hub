/* lrharness.js - Week 4 of Probability You Build: an adversarial predict-then-run
   test suite for hand-rolled logistic regression. Ported from the validated
   prototype data/pai-w34/prototypes/lrharness.html and extended per
   probability-you-build-course/BUILDER-SPEC.md: seeded randomness, token colours,
   re-render on theme change, frozen .build wrapper markup.

   Canonical trainer configuration (prototype-tuned, fixed for the whole suite):
   eta 0.05, 4000 batch gradient-ascent steps, mean-gradient updates, L2 lambda 0
   unless the reader moves the slider. Do not retune per case: the discipline is
   that every case runs the same trainer. */
(function () {
  "use strict";

  if (window.LRH && window.LRH.__mounted) return;

  // ---------- deterministic randomness ----------
  function makeRng(seed) {
    let s = seed >>> 0;
    return function () {
      s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
      return s / 4294967296;
    };
  }

  function makeGen(seed) {
    const rng = makeRng(seed);
    let spare = null;
    function gauss() {
      if (spare !== null) { const v = spare; spare = null; return v; }
      let u = 0, v = 0;
      while (u === 0) u = rng();
      while (v === 0) v = rng();
      const r = Math.sqrt(-2 * Math.log(u));
      const t = 2 * Math.PI * v;
      spare = r * Math.sin(t);
      return r * Math.cos(t);
    }
    function blob(cx, cy, n, y, sd) {
      sd = sd || 1;
      return Array.from({ length: n }, () => ({ x: [cx + gauss() * sd, cy + gauss() * sd], y: y }));
    }
    return { rng: rng, gauss: gauss, blob: blob };
  }

  // ---------- model ----------
  function sig(z) { return 1 / (1 + Math.exp(-z)); }

  function fit(data, opt) {
    opt = opt || {};
    const lr = opt.lr !== undefined ? opt.lr : 0.05;
    const steps = opt.steps !== undefined ? opt.steps : 4000;
    const l2 = opt.l2 || 0;
    let w = [0, 0, 0];
    let n400 = 0, n1600 = 0;
    for (let s = 0; s < steps; s++) {
      const g = [0, 0, 0];
      for (const p of data) {
        const z = w[0] + w[1] * p.x[0] + w[2] * p.x[1];
        const err = p.y - sig(z);
        g[0] += err; g[1] += err * p.x[0]; g[2] += err * p.x[1];
      }
      for (let j = 0; j < 3; j++) w[j] += lr * g[j] / data.length - l2 * w[j];
      if (s === 399) n400 = Math.hypot(w[1], w[2]);
      if (s === 1599) n1600 = Math.hypot(w[1], w[2]);
    }
    return { w: w, n400: n400, n1600: n1600 };
  }

  function score(w, x) { return w[0] + w[1] * x[0] + w[2] * x[1]; }
  function predict(w, x) { return sig(score(w, x)); }
  function accuracy(w, data) {
    return data.filter(p => (predict(w, p.x) > 0.5) === (p.y === 1)).length / data.length;
  }
  function corr(a, b) {
    const ma = a.reduce((x, y) => x + y, 0) / a.length;
    const mb = b.reduce((x, y) => x + y, 0) / b.length;
    let cab = 0, va = 0, vb = 0;
    for (let i = 0; i < a.length; i++) {
      cab += (a[i] - ma) * (b[i] - mb);
      va += (a[i] - ma) * (a[i] - ma);
      vb += (b[i] - mb) * (b[i] - mb);
    }
    return cab / Math.sqrt(va * vb);
  }

  // ---------- generators (per-case seeds; comments record why a seed is not 42) ----------
  const GENS = {
    separable: { seed: 42, label: "two tight clouds far apart, 40 v 40",
      make: g => [...g.blob(-4, -4, 40, 0, 0.7), ...g.blob(4, 4, 40, 1, 0.7)] },
    balanced: { seed: 42, label: "two overlapping clouds, 60 v 60",
      make: g => [...g.blob(-1, -1, 60, 0, 1.6), ...g.blob(1, 1, 60, 1, 1.6)] },
    imbalanced: { seed: 49,
      // seed chosen so the canonical failure shows on the default draw:
      // across seeds minority recall lands anywhere from 0.1 to 0.8.
      label: "190 negatives v 10 positives",
      make: g => [...g.blob(-1, -1, 190, 0, 1.5), ...g.blob(1.5, 1.5, 10, 1, 1.5)] },
    correlated: { seed: 47, label: "x2 is nearly a copy of x1 (120 points)",
      make: g => {
        const out = [];
        for (let i = 0; i < 120; i++) {
          const base = g.gauss();
          const y = base + g.gauss() * 0.8 > 0 ? 1 : 0;
          out.push({ x: [base, base + g.gauss() * 0.25], y: y });
        }
        return out;
      } },
    xorish: { seed: 42, label: "four clouds in the XOR corners, 30 each",
      make: g => [...g.blob(-2, -2, 30, 0), ...g.blob(2, 2, 30, 0),
                  ...g.blob(-2, 2, 30, 1), ...g.blob(2, -2, 30, 1)] },
    outlier: { seed: 42, label: "clean clouds, plus one confirmed positive planted at (10, -10)",
      make: g => [...g.blob(-2, -2, 60, 0), ...g.blob(2, 2, 59, 1), { x: [10, -10], y: 1 }],
      baseline: g => [...g.blob(-2, -2, 60, 0), ...g.blob(2, 2, 59, 1)] },
    labelnoise: { seed: 42, label: "two clouds, 15% of labels flipped at random",
      make: g => [...g.blob(-1.5, -1.5, 80, 0, 1.4)].map(p => g.rng() < 0.15 ? { x: p.x, y: 1 } : p)
        .concat([...g.blob(1.5, 1.5, 80, 1, 1.4)].map(p => g.rng() < 0.15 ? { x: p.x, y: 0 } : p)) },
    tiny: { seed: 42, label: "six points only, 3 v 3",
      make: g => [...g.blob(-2, -2, 3, 0, 1.2), ...g.blob(2, 2, 3, 1, 1.2)] }
  };

  // ---------- measurement ----------
  const CASES = {
    separable: {
      name: "perfect separation", gen: "separable",
      predict: "unbounded fit: train accuracy pins at 100% and confidence saturates past 0.999",
      check: r => r.acc === 1 && r.minConf > 0.99 },
    balanced: {
      name: "clean overlap", gen: "balanced",
      predict: "converges: the norm settles, accuracy lands between 70% and 95%, boundary between the clouds",
      check: r => r.normGrowth < 1.1 && r.acc > 0.7 && r.acc < 0.95 },
    imbalanced: {
      name: "class imbalance 19:1", gen: "imbalanced",
      predict: "accuracy looks great (>90%) but the model misses most positives",
      check: r => r.acc > 0.9 && r.minorityRecall < 0.5 },
    correlated: {
      name: "correlated features", gen: "correlated",
      predict: "predictions stay good, but each coefficient alone swings wildly across refits",
      check: r => r.coefCorr < -0.6 && r.acc > 0.7 },
    xorish: {
      name: "XOR shape", gen: "xorish",
      predict: "stuck near chance accuracy: no straight line separates these corners",
      check: r => r.acc < 0.7 },
    outlier: {
      name: "one far outlier", gen: "outlier",
      predict: "the boundary twists several degrees toward the outlier even though training accuracy never notices",
      check: r => r.tiltDeg !== null && Math.abs(r.tiltDeg) > 3 },
    labelnoise: {
      name: "15% label noise", gen: "labelnoise",
      predict: "probabilities near the boundary stay compressed (never 0.99); accuracy ceiling below 92%",
      check: r => r.maxProbNear < 0.97 && r.acc < 0.92 && r.acc > 0.7 },
    tiny: {
      name: "tiny sample n=6", gen: "tiny",
      predict: "refits disagree wildly: P(positive) at the origin swings across seeds",
      check: r => r.seedSpread > 0.35 }
  };

  function resolveCase(spec) {
    if (typeof spec === "string") return CASES[spec];
    return spec;
  }

  function resolveGen(cs) {
    if (typeof cs.gen === "string") {
      const entry = GENS[cs.gen];
      if (!entry) throw new Error("unknown generator: " + cs.gen);
      return entry;
    }
    return { seed: cs.seed !== undefined ? cs.seed : 42, make: cs.gen, baseline: cs.baseline };
  }

  function runCase(cs, l2) {
    const entry = resolveGen(cs);
    const seed = entry.seed;
    const data = entry.make(makeGen(seed));
    const main = fit(data, { lr: 0.05, steps: 4000, l2: l2 });
    const w = main.w;
    const normGrowth = main.n1600 / (main.n400 || 1);
    const acc = accuracy(w, data);
    const pos = data.filter(p => p.y === 1);
    const minorityRecall = pos.length ? pos.filter(p => predict(w, p.x) > 0.5).length / pos.length : 0;
    const near = data.filter(p => Math.abs(p.x[0]) < 1 && Math.abs(p.x[1]) < 1);
    const maxProbNear = near.length ? Math.max(...near.map(p => predict(w, p.x))) : 1;
    const K = 20;
    const ws = [];
    for (let s = 0; s < K; s++) ws.push(fit(entry.make(makeGen(seed + 1 + s)), { lr: 0.05, steps: 4000, l2: l2 }).w);
    const coefCorr = corr(ws.map(v => v[1]), ws.map(v => v[2]));
    const probs = ws.map(v => predict(v, [0, 0]));
    const seedSpread = Math.max(...probs) - Math.min(...probs);
    const minConf = Math.min(...data.map(p => p.y === 1 ? predict(w, p.x) : 1 - predict(w, p.x)));
    let tiltDeg = null;
    if (entry.baseline) {
      const wb = fit(entry.baseline(makeGen(seed)), { lr: 0.05, steps: 4000, l2: l2 }).w;
      tiltDeg = (Math.atan2(w[2], w[1]) - Math.atan2(wb[2], wb[1])) * 180 / Math.PI;
    }
    return {
      acc: acc, minorityRecall: minorityRecall, minConf: minConf,
      normGrowth: normGrowth, maxProbNear: maxProbNear, coefCorr: coefCorr,
      seedSpread: seedSpread, tiltDeg: tiltDeg,
      normFinal: Math.hypot(w[1], w[2]), w: w, data: data, ws: ws
    };
  }

  // ---------- token colours, read at draw time ----------
  let probeEl = null;
  function token(name) {
    if (!probeEl) {
      probeEl = document.createElement("div");
      probeEl.style.cssText = "position:absolute;width:0;height:0;overflow:hidden";
      document.body.appendChild(probeEl);
    }
    probeEl.style.color = "var(" + name + ")";
    return getComputedStyle(probeEl).color;
  }

  // ---------- drawing ----------
  const W = 640, H = 360;

  function drawSigma(canvas, state) {
    const c = canvas.getContext("2d");
    const ink = token("--ink"), inkSoft = token("--ink-faint"), accent = token("--prob"),
          line = token("--line"), surface = token("--surface");
    c.clearRect(0, 0, W, H);
    c.fillStyle = surface;
    c.fillRect(0, 0, W, H);
    const pad = 34, x0 = pad, x1 = W - pad, y0 = H - pad, y1 = pad + 14;
    const zx = z => x0 + (z + 6) / 12 * (x1 - x0);
    const py = p => y0 - p * (y0 - y1);
    c.strokeStyle = line;
    c.lineWidth = 1;
    c.beginPath(); c.moveTo(x0, py(0.5)); c.lineTo(x1, py(0.5)); c.stroke();
    c.strokeStyle = inkSoft;
    c.beginPath();
    c.moveTo(x0, y0); c.lineTo(x1, y0);
    c.moveTo(zx(0), y0); c.lineTo(zx(0), y1);
    c.stroke();
    c.fillStyle = inkSoft;
    c.font = "11px ui-monospace, monospace";
    c.fillText("p = 0.5", zx(0) + 6, py(0.5) - 5);
    c.fillText("z = 0", zx(0) + 5, y0 + 13);
    c.fillText("0", x0 - 10, y0 + 4);
    c.fillText("1", x0 - 10, y1 + 4);
    c.strokeStyle = accent;
    c.lineWidth = 2.5;
    c.beginPath();
    for (let i = 0; i <= 240; i++) {
      const z = -6 + i * 12 / 240;
      const X = zx(z), Y = py(sig(z));
      if (i === 0) c.moveTo(X, Y); else c.lineTo(X, Y);
    }
    c.stroke();
    const zv = state.z, pv = sig(zv);
    c.strokeStyle = inkSoft;
    c.setLineDash([3, 3]);
    c.beginPath(); c.moveTo(zx(zv), y0); c.lineTo(zx(zv), py(pv)); c.stroke();
    c.setLineDash([]);
    c.fillStyle = token("--signal");
    c.beginPath(); c.arc(zx(zv), py(pv), 5, 0, 7); c.fill();
    c.strokeStyle = ink;
    c.stroke();
    c.fillStyle = ink;
    c.font = "13px ui-monospace, monospace";
    const dec = pv > 0.5 ? 1 : 0;
    c.fillText("\u03c3(" + zv.toFixed(2) + ") = " + pv.toFixed(4) + "   decision: " + dec, zx(-5.8), y1 - 2);
  }

  function drawScatter(canvas, rec, title) {
    const c = canvas.getContext("2d");
    const ink = token("--ink"), inkSoft = token("--ink-faint"), line = token("--line"),
          signal = token("--signal"), alarm = token("--alarm"),
          prob = token("--prob"), surface = token("--surface");
    c.clearRect(0, 0, W, H);
    c.fillStyle = surface;
    c.fillRect(0, 0, W, H);
    const S = 340, ox = 14, oy = 10;
    let lim = 6;
    for (const p of rec.data) lim = Math.max(lim, Math.abs(p.x[0]) + 1, Math.abs(p.x[1]) + 1);
    const px = v => ox + (v + lim) / (2 * lim) * S;
    const py = v => oy + S - (v + lim) / (2 * lim) * S;
    c.strokeStyle = line;
    c.lineWidth = 1;
    c.strokeRect(ox, oy, S, S);
    c.beginPath();
    c.moveTo(px(-lim), py(0)); c.lineTo(px(lim), py(0));
    c.moveTo(px(0), py(-lim)); c.lineTo(px(0), py(lim));
    c.stroke();
    c.fillStyle = inkSoft;
    c.font = "10px ui-monospace, monospace";
    for (let t = -Math.floor(lim / 2) * 2; t <= lim; t += 2) {
      if (t === 0) continue;
      c.fillText(String(t), px(t) - 3, py(0) + 12);
      c.fillText(String(t), px(0) + 4, py(t) + 3);
    }
    for (const p of rec.data) {
      c.beginPath();
      c.arc(px(p.x[0]), py(p.x[1]), 3.2, 0, 7);
      c.fillStyle = p.y === 1 ? signal : alarm;
      c.globalAlpha = 0.9;
      c.fill();
      c.globalAlpha = 1;
    }
    const b = rec.w[0], w1 = rec.w[1], w2 = rec.w[2];
    const norm = Math.hypot(w1, w2);
    if (norm > 1e-6) {
      c.strokeStyle = prob;
      c.lineWidth = 2.5;
      c.beginPath();
      const f = x => -(b + w1 * x) / w2;
      c.moveTo(px(-lim), py(f(-lim)));
      c.lineTo(px(lim), py(f(lim)));
      c.stroke();
    }
    const tx = ox + S + 18;
    c.fillStyle = ink;
    c.font = "600 13px system-ui, sans-serif";
    c.fillText(title, tx, oy + 16);
    c.font = "11px ui-monospace, monospace";
    c.fillStyle = signal;
    c.fillRect(tx, oy + 30, 9, 9);
    c.fillStyle = ink;
    c.fillText("y = 1", tx + 14, oy + 38);
    c.fillStyle = alarm;
    c.fillRect(tx, oy + 46, 9, 9);
    c.fillStyle = ink;
    c.fillText("y = 0", tx + 14, oy + 54);
    c.fillStyle = prob;
    c.fillRect(tx, oy + 62, 9, 3);
    c.fillStyle = ink;
    c.fillText("\u03b8\u00b7x = 0", tx + 14, oy + 70);
    c.fillStyle = inkSoft;
    c.fillText("\u03b80 = " + b.toFixed(2), tx, oy + 94);
    c.fillText("\u03b81 = " + w1.toFixed(2), tx, oy + 110);
    c.fillText("\u03b82 = " + w2.toFixed(2), tx, oy + 126);
    c.fillText("||\u03b8|| = " + norm.toFixed(2), tx, oy + 142);
    c.fillText("train acc = " + rec.acc.toFixed(2), tx, oy + 158);
  }

  // ---------- suite rendering ----------
  function fmt(r) {
    return "acc=" + r.acc.toFixed(2) +
      "  minRecall=" + r.minorityRecall.toFixed(2) +
      "  ||w||final=" + r.normFinal.toFixed(1) +
      "  growth=" + r.normGrowth.toFixed(2) +
      "  maxP(near)=" + r.maxProbNear.toFixed(2) +
      "  minConf=" + (r.minConf >= 0.001 ? r.minConf.toFixed(4) : r.minConf.toExponential(1)) +
      "  coefCorr=" + r.coefCorr.toFixed(2) +
      "  seedSpread=" + r.seedSpread.toFixed(2) +
      (r.tiltDeg === null ? "" : "  tilt=" + r.tiltDeg.toFixed(1) + "\u00b0");
  }

  function chip(ok) {
    const bg = ok ? token("--ok-soft") : token("--warn-soft");
    const fg = ok ? token("--ok") : token("--warn");
    return '<span style="white-space:nowrap;padding:.1rem .55rem;border-radius:999px;' +
      'font-weight:700;font-size:.78em;background:' + bg + ";color:" + fg + '">' +
      (ok ? "MATCHES" : "CONTRADICTED") + "</span>";
  }

  const state = {};
  const stores = {};

  function predKey(figId, name) { return "pyb-w4-pred:" + figId + ":" + name; }

  function buildReport(st) {
    const rep = document.createElement("div");
    rep.style.cssText = "width:100%;margin-top:.6rem;font-size:.85em";
    let html = '<table style="border-collapse:collapse;width:100%">' +
      "<thead><tr>" +
      '<th scope="col" style="text-align:left;padding:.3rem .5rem;border-bottom:1px solid ' + token("--line") + '">case</th>' +
      '<th scope="col" style="text-align:left;padding:.3rem .5rem;border-bottom:1px solid ' + token("--line") + '">your claim</th>' +
      '<th scope="col" style="text-align:left;padding:.3rem .5rem;border-bottom:1px solid ' + token("--line") + '">verdict</th>' +
      "</tr></thead><tbody>";
    st.records.forEach((rec, i) => {
      const sel = i === st.selected;
      html += '<tr data-lrh-row="' + i + '" style="cursor:pointer;background:' +
        (sel ? token("--accent-wash") : "transparent") + '">' +
        '<td style="padding:.3rem .5rem;border-bottom:1px solid ' + token("--line") + ';white-space:nowrap">' + rec.name + "</td>" +
        '<td style="padding:.3rem .5rem;border-bottom:1px solid ' + token("--line") + '">' +
        (rec.claim ? escapeHtml(rec.claim) : '<span style="color:' + token("--ink-faint") + '">(nothing written)</span>') + "</td>" +
        '<td style="padding:.3rem .5rem;border-bottom:1px solid ' + token("--line") + '">' + chip(rec.ok) + "</td></tr>";
    });
    html += "</tbody></table>";
    html += '<div style="margin-top:.5rem;color:' + token("--ink-soft") + ';font-family:ui-monospace,monospace;font-size:.92em;line-height:1.7">';
    st.records.forEach((rec, i) => {
      html += "<div>" + (i === st.selected ? "\u25b8 " : "&nbsp;&nbsp;") + rec.name + ": " + fmt(rec.record) + "</div>";
    });
    html += "</div>";
    rep.innerHTML = html;
    return rep;
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function renderSuite(st) {
    drawScatter(st.canvas, st.records[st.selected].record, st.records[st.selected].name);
    const old = st.fig.querySelector(".lrh-report");
    if (old) old.remove();
    st.readout.appendChild(buildReport(st));
    st.fig.querySelectorAll("[data-lrh-row]").forEach(tr => {
      tr.addEventListener("click", () => {
        st.selected = Number(tr.getAttribute("data-lrh-row"));
        renderSuite(st);
      });
    });
  }

  function renderShellMessage(st) {
    const msg = document.createElement("div");
    msg.style.cssText = "width:100%;margin-top:.6rem;padding:.6rem .8rem;border:1px dashed " +
      token("--line-strong") + ";color:" + token("--ink-soft") + ";font-size:.88em";
    msg.textContent = "The suite frame is wired and empty: zero cases registered. " +
      "Cases arrive from lesson 0303 onward - each one is declared as data, with your written prediction graded against the measured record.";
    st.readout.appendChild(msg);
  }

  function render(st) {
    if (!st.fig.isConnected) return;
    if (st.mode === "sigma") { drawSigma(st.canvas, st); return; }
    if (st.mode === "trainer") { renderTrainer(st); return; }
    if (st.mode === "geometry") { renderGeometry(st); return; }
    if (st.mode === "suite") {
      if (st.records.length) renderSuite(st);
      else { drawEmptyPlot(st.canvas); renderShellMessage(st); }
    }
  }

  function drawEmptyPlot(canvas) {
    const c = canvas.getContext("2d");
    c.clearRect(0, 0, W, H);
    c.fillStyle = token("--surface");
    c.fillRect(0, 0, W, H);
    c.strokeStyle = token("--line");
    c.lineWidth = 1;
    const S = 340, ox = 14, oy = 10;
    c.strokeRect(ox, oy, S, S);
    c.fillStyle = token("--ink-faint");
    c.font = "12px system-ui, sans-serif";
    c.fillText("no cases registered yet", ox + 90, oy + S / 2);
  }

  // ---------- modes ----------
  function mountSigma(fig, cfg) {
    const canvas = fig.querySelector(".build-canvas");
    canvas.width = W; canvas.height = H;
    const st = { fig: fig, canvas: canvas, mode: "sigma", z: cfg.z !== undefined ? cfg.z : 1.0 };
    const controls = fig.querySelector(".build-controls");
    controls.innerHTML =
      '<label>score z <input type="range" min="-6" max="6" step="0.05" value="' + st.z + '" data-lrh="z"></label>';
    const readout = fig.querySelector(".build-readout");
    readout.innerHTML = "";
    const spanP = document.createElement("span");
    const spanD = document.createElement("span");
    readout.appendChild(spanP); readout.appendChild(spanD);
    st.spanP = spanP; st.spanD = spanD;
    controls.querySelector('[data-lrh="z"]').addEventListener("input", e => {
      st.z = Number(e.target.value);
      render(st);
    });
    updateSigmaReadout(st);
    return st;
  }

  function updateSigmaReadout(st) {
    const p = sig(st.z);
    st.spanP.innerHTML = "\u03c3(z) <b>" + p.toFixed(4) + "</b>";
    st.spanD.innerHTML = 'decision at 0.5 <b>' + (p > 0.5 ? 1 : 0) + "</b>";
  }

  function mountTrainer(fig, cfg) {
    const canvas = fig.querySelector(".build-canvas");
    canvas.width = W; canvas.height = H;
    const genName = cfg.gen || "balanced";
    const data = GENS[genName].make(makeGen(GENS[genName].seed));
    const st = {
      fig: fig, canvas: canvas, mode: "trainer",
      data: data, steps: cfg.steps !== undefined ? cfg.steps : 800, l2: 0,
      rec: null
    };
    measure(st);
    const controls = fig.querySelector(".build-controls");
    controls.innerHTML =
      '<label>training steps <input type="range" min="0" max="4000" step="50" value="' + st.steps + '" data-lrh="steps"></label>';
    const readout = fig.querySelector(".build-readout");
    readout.innerHTML = "";
    const sAcc = document.createElement("span"), sNorm = document.createElement("span"), sStep = document.createElement("span");
    readout.appendChild(sAcc); readout.appendChild(sNorm); readout.appendChild(sStep);
    st.sAcc = sAcc; st.sNorm = sNorm; st.sStep = sStep;
    controls.querySelector('[data-lrh="steps"]').addEventListener("input", e => {
      st.steps = Number(e.target.value);
      measure(st);
      render(st);
    });
    return st;
  }

  function measure(st) {
    const r = fit(st.data, { lr: 0.05, steps: Math.max(st.steps, 1), l2: st.l2 });
    st.rec = {
      w: r.w, data: st.data,
      acc: accuracy(r.w, st.data),
      minConf: Math.min(...st.data.map(p => p.y === 1 ? predict(r.w, p.x) : 1 - predict(r.w, p.x))),
      normFinal: Math.hypot(r.w[1], r.w[2])
    };
  }

  function renderTrainer(st) {
    drawScatter(st.canvas, st.rec, GENS.balanced.label.split(",")[0]);
    st.sAcc.innerHTML = "accuracy <b>" + st.rec.acc.toFixed(3) + "</b>";
    st.sNorm.innerHTML = "||\u03b8|| <b>" + st.rec.normFinal.toFixed(3) + "</b>";
    st.sStep.innerHTML = "steps <b>" + st.steps + "</b> of 4000";
  }

  function mountGeometry(fig, cfg) {
    const canvas = fig.querySelector(".build-canvas");
    canvas.width = W; canvas.height = H;
    const genName = cfg.gen || "balanced";
    const entry = GENS[genName];
    const data = entry.make(makeGen(entry.seed));
    const st = {
      fig: fig, canvas: canvas, mode: "geometry",
      data: data, genLabel: entry.label, th: [cfg.th0 || 0, cfg.th1 || 0, cfg.th2 || 0]
    };
    const controls = fig.querySelector(".build-controls");
    controls.innerHTML =
      '<label>bias \u03b80 <input type="range" min="-5" max="5" step="0.1" value="' + st.th[0] + '" data-lrh="t0"></label>' +
      '<label>weight \u03b81 <input type="range" min="-5" max="5" step="0.1" value="' + st.th[1] + '" data-lrh="t1"></label>' +
      '<label>weight \u03b82 <input type="range" min="-5" max="5" step="0.1" value="' + st.th[2] + '" data-lrh="t2"></label>';
    const readout = fig.querySelector(".build-readout");
    readout.innerHTML = "";
    const sAcc = document.createElement("span"), sOrg = document.createElement("span");
    readout.appendChild(sAcc); readout.appendChild(sOrg);
    st.sAcc = sAcc; st.sOrg = sOrg;
    ["t0", "t1", "t2"].forEach((k, i) => {
      controls.querySelector('[data-lrh="' + k + '"]').addEventListener("input", e => {
        st.th[i] = Number(e.target.value);
        render(st);
      });
    });
    return st;
  }

  function renderGeometry(st) {
    const w = [st.th[0], st.th[1], st.th[2]];
    const rec = { w: w, data: st.data, acc: accuracy(w, st.data) };
    drawScatter(st.canvas, rec, st.genLabel.split(",")[0] + " - your boundary");
    st.sAcc.innerHTML = "accuracy at your line <b>" + rec.acc.toFixed(2) + "</b>";
    st.sOrg.innerHTML = "\u03c3(origin) <b>" + predict(w, [0, 0]).toFixed(2) + "</b>";
  }

  function mountSuite(fig, cfg) {
    const canvas = fig.querySelector(".build-canvas");
    canvas.width = W; canvas.height = H;
    const caseList = (cfg.cases || []).map(resolveCase);
    const st = {
      fig: fig, canvas: canvas, mode: "suite",
      cases: caseList,
      includeMine: !!cfg.includeMine,
      l2: 0, selected: 0, records: [], running: false, stale: false
    };
    if (st.includeMine && Array.isArray(window.MY_CASES)) {
      window.MY_CASES.forEach(cs => st.cases.push(cs));
    }
    const controls = fig.querySelector(".build-controls");
    const lam = cfg.lambdaControl
      ? '<label>lambda (L2) <input type="range" min="0" max="0.02" step="0.001" value="0" data-lrh="lam"></label>'
      : "";
    controls.innerHTML =
      '<button type="button" data-lrh="run">Run suite</button>' + lam;
    const readout = fig.querySelector(".build-readout");
    readout.innerHTML = "";
    const sSum = document.createElement("span");
    sSum.setAttribute("aria-live", "polite");
    readout.appendChild(sSum);
    st.sSum = sSum;
    sSum.innerHTML = st.cases.length + " cases loaded - write each prediction, then run.";
    drawEmptyPlot(canvas);

    const lamInput = controls.querySelector('[data-lrh="lam"]');
    if (lamInput) {
      lamInput.addEventListener("input", () => {
        const v = Number(lamInput.value);
        if (v !== st.l2) {
          st.l2 = v;
          st.stale = true;
          sSum.innerHTML = "lambda now <b>" + v.toFixed(3) + "</b> - re-run to refresh the report.";
        }
      });
    }
    controls.querySelector('[data-lrh="run"]').addEventListener("click", () => run(st));

    // prediction boxes live between controls and stage output: one per case.
    const box = document.createElement("div");
    box.style.cssText = "width:100%;display:flex;flex-direction:column;gap:.45rem;margin-top:.6rem";
    st.cases.forEach((cs, i) => {
      const row = document.createElement("label");
      row.style.cssText = "display:block;font-size:.85em";
      const saved = localStorage.getItem(predKey(fig.id, cs.name)) || "";
      row.innerHTML = "<b>" + escapeHtml(cs.name) + "</b> <span style=\"color:" + token("--ink-faint") + "\">- " +
        escapeHtml(resolveGen(cs).label || "") + "</span><br>" +
        '<textarea rows="2" data-lrh-pred="' + i + '" style="width:min(100%,52ch);margin-top:.2rem" ' +
        'placeholder="Your prediction, written before you run - honour system.">' + escapeHtml(saved) + "</textarea>";
      box.appendChild(row);
    });
    if (st.cases.length) readout.appendChild(box);
    st.claims = st.cases.map((cs, i) => localStorage.getItem(predKey(fig.id, cs.name)) || "");
    readout.querySelectorAll("[data-lrh-pred]").forEach(ta => {
      ta.addEventListener("input", () => {
        st.claims[Number(ta.getAttribute("data-lrh-pred"))] = ta.value;
        try { localStorage.setItem(predKey(fig.id, st.cases[Number(ta.getAttribute("data-lrh-pred"))].name), ta.value); } catch (e) {}
      });
    });
    return st;
  }

  function run(st) {
    if (st.running) return;
    st.running = true;
    st.stale = false;
    st.records = [];
    st.selected = 0;
    let i = 0;
    st.sSum.innerHTML = "running case 1 of " + st.cases.length + "...";
    (function step() {
      if (i >= st.cases.length) {
        st.running = false;
        render(st);
        const m = st.records.filter(r => r.ok).length;
        st.sSum.innerHTML = "<b>" + m + " of " + st.records.length + " MATCH</b> - the rest contradict your claim. Lambda " + st.l2.toFixed(3) + ".";
        return;
      }
      const cs = st.cases[i];
      let record, ok;
      try {
        record = runCase(cs, st.l2);
        ok = !!cs.check(record);
      } catch (err) {
        record = { acc: NaN, minorityRecall: NaN, minConf: NaN, normGrowth: NaN, maxProbNear: NaN, coefCorr: NaN, seedSpread: NaN, tiltDeg: null, normFinal: NaN, w: [0, 0, 0], data: [] };
        ok = false;
      }
      st.records.push({ name: cs.name, claim: st.claims[i] || "", record: record, ok: ok });
      st.selected = i;
      render(st);
      i += 1;
      st.sSum.innerHTML = "running case " + (i + 1) + " of " + st.cases.length + "...";
      setTimeout(step, 30);
    })();
  }

  // ---------- entry ----------
  function mount(figId, cfg) {
    const fig = document.getElementById(figId);
    if (!fig) throw new Error("no figure #" + figId);
    if (state[figId]) return state[figId];
    cfg = cfg || {};
    let st;
    if (cfg.mode === "sigma") st = mountSigma(fig, cfg);
    else if (cfg.mode === "trainer") st = mountTrainer(fig, cfg);
    else if (cfg.mode === "geometry") st = mountGeometry(fig, cfg);
    else st = mountSuite(fig, cfg);
    state[figId] = st;
    render(st);
    return st;
  }

  new MutationObserver(() => {
    Object.keys(state).forEach(k => {
      try { render(state[k]); } catch (e) {}
    });
  }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-mode", "data-palette"] });

  window.LRH = {
    __mounted: true,
    mount: mount,
    makeGen: makeGen,
    sig: sig,
    fit: fit
  };
})();
