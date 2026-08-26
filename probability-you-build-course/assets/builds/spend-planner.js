/* Spend Planner - the Week 1 interactive build of Probability You Build.
   One file serves every Week 1 lesson: each page mounts the panels its
   figure ids name, and unused panels cost nothing.
   Contract: probability-you-build-course/BUILDER-SPEC.md.
   - Colours are read from CSS tokens at draw time (never literal hex) and
     every mounted panel re-renders when <html> data-mode/data-palette move,
     plus beforeprint (paper-safe ink) and afterprint.
   - Randomness is seeded (LCG, seed 42 by convention) so two readers see
     identical numbers and screenshots match the prose.
   - Prices are a frozen snapshot dated 2026-08-26; see the block below.
   - Exposes nothing global. */
(function () {
  'use strict';

  /* ---------- frozen catalogue ------------------------------------------
     Dated snapshot fetched 2026-08-26. Per-1M-token USD prices.
     Sources read that day:
       - OpenAI pricing page, https://platform.openai.com/docs/pricing
         (gpt-5.6-luna $0.20 in / $1.20 out)
       - Anthropic pricing page,
         https://platform.claude.com/docs/en/about-claude/pricing
         (Claude Sonnet 5 $2/$10, Claude Opus 5 $5/$25)
     Tier names are deliberately neutral; the anchors above are recorded so
     the snapshot's provenance survives vendor rebrands. These numbers are
     historical: they were true on 2026-08-26 and the maths does not care
     when they stop being true. Nothing here fetches anything at runtime. */
  var REQUEST_TOKENS = { inp: 900, out: 300 }; // the standard request shape used all week
  var TIERS = [
    { key: 'nano',     label: 'nano',     inPrice: 0.20, outPrice: 1.20 },  // anchor: gpt-5.6-luna, 2026-08-26
    { key: 'standard', label: 'standard', inPrice: 2.00, outPrice: 10.00 }, // anchor: Claude Sonnet 5, 2026-08-26
    { key: 'frontier', label: 'frontier', inPrice: 5.00, outPrice: 25.00 }  // anchor: Claude Opus 5, 2026-08-26
  ];
  TIERS.forEach(function (t) {
    t.cost = (REQUEST_TOKENS.inp * t.inPrice + REQUEST_TOKENS.out * t.outPrice) / 1e6;
  });
  var NANO_COST = TIERS[0].cost;      // $0.00054 per request
  var FRONTIER_COST = TIERS[2].cost;  // $0.01200 per request

  /* ---------- print-safe ink -------------------------------------------
     The print stylesheet recolours CSS, not canvas pixels, so while a print
     job is pending every panel draws dark ink for white paper instead of
     reading the (possibly dark-mode) tokens. */
  var printMode = false;
  var PRINT_INK = {
    ink: '#1a1a18', soft: '#4a4a44', faint: '#63635b',
    accent: '#a63a24', accent2: '#15585c', ok: '#1a6e35',
    warn: '#a63a24', gold: '#7a5a0a', fill: 'rgba(0,0,0,0.06)', grid: 'rgba(0,0,0,0.14)'
  };

  function token(name) {
    var probe = token._probe;
    if (!probe) {
      probe = token._probe = document.createElement('span');
      probe.style.display = 'none';
      document.body.appendChild(probe);
    }
    probe.style.color = '';
    probe.style.color = 'var(' + name + ')';
    return getComputedStyle(probe).color;
  }

  function rgba(color, alpha) {
    var m = color.match(/rgba?\(([^)]+)\)/);
    if (!m) { return color; }
    var parts = m[1].split(',').map(parseFloat);
    return 'rgba(' + parts[0] + ',' + parts[1] + ',' + parts[2] + ',' + alpha + ')';
  }

  function colors() {
    if (printMode || !document.body) { return PRINT_INK; }
    return {
      ink: token('--ink'),
      soft: token('--ink-soft'),
      faint: token('--ink-faint'),
      accent: token('--accent'),
      accent2: token('--accent-2'),
      ok: token('--ok'),
      warn: token('--warn'),
      gold: token('--gold'),
      fill: rgba(token('--ink'), 0.07),
      grid: rgba(token('--ink'), 0.18)
    };
  }

  /* ---------- seeded randomness ---------------------------------------- */
  function lcg(seed) {
    var s = (seed >>> 0) || 42;
    return function () {
      s = (Math.imul(s, 1664525) + 1013904223) >>> 0;
      return s / 4294967296;
    };
  }

  /* ---------- the week's mathematics ----------------------------------- */
  function choose(n, k) { // multiplicative loop; never factorials (171! overflows)
    var r = 1;
    for (var i = 0; i < k; i++) { r = r * (n - i) / (i + 1); }
    return r;
  }
  function pAnyCorrect(n, p) { return 1 - Math.pow(1 - p, n); }
  function pMajority(n, p) { // n odd
    var s = 0, maj = (n + 1) / 2;
    for (var k = maj; k <= n; k++) { s += choose(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k); }
    return s;
  }
  // Cascade events: C = the nano answer is actually right; S = the check ships it.
  // P(S|C) = a (sensitivity), P(S|W) = b (false-alarm rate). Escalation happens
  // on refusal REGARDLESS of whether the nano answer was right - the classic error
  // is conditioning escalation on being wrong.
  function cascadeParts(ps, pf, a, b) {
    var pShip = ps * a + (1 - ps) * b;            // law of total probability
    var pCorrect = ps * a + (1 - pShip) * pf;     // ship-and-right OR refuse-and-frontier-right
    var eCost = NANO_COST + (1 - pShip) * FRONTIER_COST; // frontier paid only on refusal
    return { pShip: pShip, pCorrect: pCorrect, eCost: eCost };
  }
  // World simulator with optional clumping: with probability c an entire batch of
  // samples fails together (correlated failure on hard prompts); otherwise the
  // samples are independent Bernoulli(p). Single-sample policies cannot clump.
  function drawBatch(rng, n, p, clump) {
    if (clump > 0 && rng() < clump) { return 0; } // the whole batch goes down together
    var hits = 0;
    for (var i = 0; i < n; i++) { if (rng() < p) { hits++; } }
    return hits;
  }
  function simulate(trials, seed, drawTrial) {
    var rng = lcg(seed);
    var ok = 0, cost = 0;
    for (var t = 0; t < trials; t++) {
      var r = drawTrial(rng);
      ok += r.correct;
      cost += r.cost;
    }
    return { p: ok / trials, cost: cost / trials };
  }
  var TRIALS = 40000;

  /* ---------- canvas helpers ------------------------------------------- */
  function ctx2d(canvas, w, h) {
    var dpr = window.devicePixelRatio || 1;
    if (canvas.width !== Math.round(w * dpr)) {
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.width = w + 'px';
      canvas.style.height = h + 'px';
    }
    var ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    ctx.font = '13px Inter, system-ui, sans-serif';
    return ctx;
  }
  function fmt(x, dp) { return Number(x).toFixed(dp === undefined ? 4 : dp); }
  function money(x) { return '$' + Number(x).toFixed(5); }
  function role(fig, name) { return fig.querySelector('[data-role="' + name + '"]'); }
  function out(fig, name) { return fig.querySelector('[data-out="' + name + '"]'); }
  function say(fig, name, text) { var el = out(fig, name); if (el) { el.textContent = text; } }
  function num(fig, name) { var el = role(fig, name); return el ? parseFloat(el.value) : NaN; }

  /* ======================================================================
     Panel: coin-world (lesson 0001)
     One request to one model is one biased coin. Run N requests, watch the
     running frequency settle toward p.
     ====================================================================== */
  function coinWorld(fig) {
    var W = 640, H = 300;

    function render() {
      var p = num(fig, 'p') / 100;
      var seed = num(fig, 'seed') || 42;
      var nTrials = 10000;
      var rng = lcg(seed);
      var hits = 0;
      var path = []; // running frequency sampled for drawing
      for (var t = 1; t <= nTrials; t++) {
        if (rng() < p) { hits++; }
        if (t <= 100 || t % 100 === 0) { path.push([t, hits / t]); }
      }
      var freq = hits / nTrials;
      say(fig, 'freq', fmt(freq));
      say(fig, 'gap', fmt(Math.abs(freq - p)));
      say(fig, 'hits', hits.toLocaleString('en-US') + ' of ' + nTrials.toLocaleString('en-US'));

      var c = colors();
      var ctx = ctx2d(fig.querySelector('canvas'), W, H);
      var padL = 52, padR = 16, padT = 18, padB = 34;
      var xMax = nTrials;
      function X(t) { return padL + (Math.log(t + 1) / Math.log(xMax + 1)) * (W - padL - padR); }
      function Y(f) { return padT + (1 - f) * (H - padT - padB); }

      ctx.strokeStyle = c.grid;
      ctx.lineWidth = 1;
      ctx.fillStyle = c.faint;
      ctx.textAlign = 'right';
      [0, 0.25, 0.5, 0.75, 1].forEach(function (f) {
        ctx.beginPath();
        ctx.moveTo(padL, Y(f)); ctx.lineTo(W - padR, Y(f));
        ctx.stroke();
        ctx.fillText(f.toFixed(2), padL - 8, Y(f) + 4);
      });

      // the true p the world uses
      ctx.strokeStyle = c.accent2;
      ctx.setLineDash([6, 4]);
      ctx.beginPath(); ctx.moveTo(padL, Y(p)); ctx.lineTo(W - padR, Y(p)); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = c.accent2;
      ctx.textAlign = 'left';
      ctx.fillText('true p = ' + fmt(p, 2), padL + 6, Y(p) - 6);

      // the running frequency
      ctx.strokeStyle = c.accent;
      ctx.lineWidth = 2;
      ctx.beginPath();
      path.forEach(function (pt, i) {
        var x = X(pt[0]), y = Y(Math.min(1, pt[1]));
        if (i === 0) { ctx.moveTo(x, y); } else { ctx.lineTo(x, y); }
      });
      ctx.stroke();
      ctx.fillStyle = c.soft;
      ctx.textAlign = 'center';
      ctx.fillText('requests, log scale', padL + (W - padL - padR) / 2, H - 6);
    }

    var runBtn = role(fig, 'rerun');
    if (runBtn) { runBtn.addEventListener('click', render); }
    ['p', 'seed'].forEach(function (r) {
      var el = role(fig, r);
      if (el) { el.addEventListener('input', render); }
    });
    return { render: render };
  }

  /* ======================================================================
     Panel: complement-lab (lesson 0002)
     P(at least one hit in n) = 1 - P(all miss). Bars show the complement
     identity holding for every n, analytic beside simulated.
     ====================================================================== */
  function complementLab(fig) {
    var W = 640, H = 300;

    function render() {
      var p = num(fig, 'p') / 100;
      var nMax = Math.round(num(fig, 'nmax'));
      var seed = num(fig, 'seed') || 42;
      var c = colors();
      var ctx = ctx2d(fig.querySelector('canvas'), W, H);
      var padL = 52, padR = 12, padT = 18, padB = 46;
      var plotW = W - padL - padR, plotH = H - padT - padB;
      var trials = 20000;
      var rng = lcg(seed);

      function Y(f) { return padT + (1 - f) * plotH; }
      ctx.strokeStyle = c.grid;
      ctx.fillStyle = c.faint;
      ctx.textAlign = 'right';
      [0, 0.5, 1].forEach(function (f) {
        ctx.beginPath(); ctx.moveTo(padL, Y(f)); ctx.lineTo(W - padR, Y(f)); ctx.stroke();
        ctx.fillText(f.toFixed(1), padL - 8, Y(f) + 4);
      });

      var slot = plotW / nMax;
      var bw = Math.min(30, slot * 0.32);
      var simMiss = 0, simN = 0;
      for (var k = 1; k <= nMax; k++) {
        var analytic = 1 - Math.pow(1 - p, k);
        var xMid = padL + slot * (k - 0.5);
        // analytic bar (accent) and simulated bar (accent2) side by side
        ctx.fillStyle = c.accent;
        ctx.fillRect(xMid - bw - 2, Y(analytic), bw, Y(0) - Y(analytic));
        var hits = 0;
        for (var t = 0; t < trials; t++) {
          if (drawBatch(rng, k, p, 0) > 0) { hits++; }
        }
        var simf = hits / trials;
        if (k === nMax) { simMiss = 1 - simf; simN = k; }
        ctx.fillStyle = c.accent2;
        ctx.fillRect(xMid + 2, Y(simf), bw, Y(0) - Y(simf));
        ctx.fillStyle = c.faint;
        ctx.textAlign = 'center';
        ctx.fillText(String(k), xMid, Y(0) + 14);
      }
      ctx.fillStyle = c.accent;
      ctx.fillRect(padL + 4, 6, 10, 10);
      ctx.fillStyle = c.soft;
      ctx.textAlign = 'left';
      ctx.fillText('analytic 1-(1-p)^k', padL + 18, 15);
      ctx.fillStyle = c.accent2;
      ctx.fillRect(padL + 150, 6, 10, 10);
      ctx.fillStyle = c.soft;
      ctx.fillText('simulated, 20k batches', padL + 164, 15);

      say(fig, 'allmiss', fmt(Math.pow(1 - p, nMax)));
      say(fig, 'anyhit', fmt(1 - Math.pow(1 - p, nMax)));
      say(fig, 'simmiss', fmt(simMiss));
      say(fig, 'identity', fmt(Math.pow(1 - p, nMax) + (1 - Math.pow(1 - p, nMax))) + ' = 1');
    }

    ['p', 'nmax', 'seed'].forEach(function (r) {
      var el = role(fig, r);
      if (el) { el.addEventListener('input', render); }
    });
    var btn = role(fig, 'rerun');
    if (btn) { btn.addEventListener('click', render); }
    return { render: render };
  }

  /* ======================================================================
     Panel: check-grid (lesson 0003)
     Conditional probability as re-scaling the world. A mosaic of the four
     joint outcomes: columns are the hidden truth (correct / wrong), rows
     are the check's verdict (ship / refuse), cell areas proportional to
     their joint probability.
     ====================================================================== */
  function checkGrid(fig) {
    var W = 640, H = 300;

    function render() {
      var ps = num(fig, 'ps') / 100;
      var a = num(fig, 'a') / 100;
      var b = num(fig, 'b') / 100;
      var c = colors();
      var ctx = ctx2d(fig.querySelector('canvas'), W, H);
      var padT = 14, padB = 30, x0 = 120, x1 = 520;
      var colW = (x1 - x0);

      var wC = colW * ps, wW = colW * (1 - ps);
      var hShipC = 180 * a, hRefC = 180 * (1 - a);
      var hShipW = 180 * b, hRefW = 180 * (1 - b);

      function cell(x, y, w, h, fill, stroke, label, sub) {
        if (h > 12 && w > 12) {
          ctx.fillStyle = fill;
          ctx.fillRect(x, y, w, h);
          ctx.strokeStyle = stroke;
          ctx.strokeRect(x + 0.5, y + 0.5, w - 1, h - 1);
          if (sub && h > 34) {
            ctx.fillStyle = c.ink;
            ctx.textAlign = 'center';
            ctx.fillText(label, x + w / 2, y + h / 2 - 4);
            ctx.fillStyle = c.soft;
            ctx.fillText(sub, x + w / 2, y + h / 2 + 13);
          } else if (h > 16) {
            ctx.fillStyle = c.ink;
            ctx.textAlign = 'center';
            ctx.fillText(label, x + w / 2, y + h / 2 + 4);
          }
        }
      }

      // correct column
      cell(x0, padT, wC, hShipC, rgba(c.ok, 0.55), c.grid, 'ship', fmt(ps * a, 4));
      cell(x0, padT + hShipC, wC, hRefC, rgba(c.gold, 0.35), c.grid, 'refuse', fmt(ps * (1 - a), 4));
      // wrong column
      cell(x0 + wC, padT, wW, hShipW, rgba(c.warn, 0.45), c.grid, 'ship', fmt((1 - ps) * b, 4));
      cell(x0 + wW, padT + hShipW, wW, hRefW, rgba(c.ok, 0.28), c.grid, 'refuse', fmt((1 - ps) * (1 - b), 4));

      ctx.fillStyle = c.soft;
      ctx.textAlign = 'center';
      ctx.fillText('answer actually right (P = ' + fmt(ps, 2) + ')', x0 + wC / 2, H - 14);
      ctx.fillText('actually wrong (P = ' + fmt(1 - ps, 2) + ')', x0 + wC + wW / 2, H - 14);
      ctx.save();
      ctx.translate(70, padT + 130);
      ctx.rotate(-Math.PI / 2);
      ctx.fillText('check verdicts within each truth', 0, 0);
      ctx.restore();

      var pShip = ps * a + (1 - ps) * b;
      say(fig, 'jointCR', fmt(ps * a));
      say(fig, 'jointWR', fmt((1 - ps) * b));
      say(fig, 'pship', fmt(pShip));
      say(fig, 'pship-gloss', fmt(ps * a, 4) + ' + ' + fmt((1 - ps) * b, 4) + ' = ' + fmt(pShip, 4));
    }

    ['ps', 'a', 'b'].forEach(function (r) {
      var el = role(fig, r);
      if (el) { el.addEventListener('input', render); }
    });
    return { render: render };
  }

  /* ======================================================================
     Panel: path-products (lesson 0004)
     The cascade drawn as paths. Each final outcome is a product along its
     path; the two highlighted paths are the ones where the customer ends
     up with a correct answer.
     ====================================================================== */
  function pathProducts(fig) {
    var W = 640, H = 340;

    function render() {
      var ps = num(fig, 'ps') / 100;
      var pf = num(fig, 'pf') / 100;
      var a = num(fig, 'a') / 100;
      var b = num(fig, 'b') / 100;
      var pShip = ps * a + (1 - ps) * b;
      var c = colors();
      var ctx = ctx2d(fig.querySelector('canvas'), W, H);

      function edge(x1, y1, x2, y2, label, good) {
        ctx.strokeStyle = good ? c.ok : c.faint;
        ctx.lineWidth = good ? 2 : 1;
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
        if (label) {
          ctx.fillStyle = c.soft;
          ctx.textAlign = 'left';
          ctx.fillText(label, (x1 + x2) / 2 - 20, (y1 + y2) / 2 - 4);
        }
      }
      function nodeBox(x, y, w, headline, sub, tone) {
        var h = 34;
        ctx.fillStyle = tone === 'ok' ? rgba(c.ok, 0.5) : tone === 'warn' ? rgba(c.warn, 0.45) : rgba(c.gold, 0.22);
        ctx.fillRect(x - w / 2, y - h / 2, w, h);
        ctx.strokeStyle = c.grid;
        ctx.strokeRect(x - w / 2 + 0.5, y - h / 2 + 0.5, w - 1, h - 1);
        ctx.fillStyle = c.ink;
        ctx.textAlign = 'center';
        ctx.font = '12px Inter, system-ui, sans-serif';
        ctx.fillText(headline, x, y - 3);
        ctx.fillStyle = c.soft;
        ctx.fillText(sub, x, y + 11);
        ctx.font = '13px Inter, system-ui, sans-serif';
      }

      // level 0: the request
      ctx.fillStyle = c.ink;
      ctx.textAlign = 'center';
      ctx.fillText('one request', 55, 172);
      // level 1: hidden truth
      edge(105, 165, 165, 85, fmt(ps, 2), false);
      edge(105, 175, 165, 255, fmt(1 - ps, 2), false);
      nodeBox(235, 78, 130, 'answer right', 'P = ' + fmt(ps, 2));
      nodeBox(235, 262, 130, 'answer wrong', 'P = ' + fmt(1 - ps, 2));
      // level 2: the check verdicts
      edge(300, 70, 360, 42, '', false);
      edge(300, 86, 360, 122, fmt(a, 2) + ' ships', false);
      edge(300, 254, 360, 222, fmt(b, 2) + ' ships', false);
      edge(300, 270, 360, 298, fmt(1 - b, 2), false);
      nodeBox(455, 38, 168, 'shipped anyway - CORRECT', fmt(ps, 2) + ' x ' + fmt(a, 2) + ' = ' + fmt(ps * a, 4), 'ok');
      nodeBox(455, 128, 150, 'refused', fmt(ps, 2) + ' x ' + fmt(1 - a, 2) + ' = ' + fmt(ps * (1 - a), 4));
      nodeBox(455, 218, 168, 'shipped anyway - WRONG', fmt(1 - ps, 2) + ' x ' + fmt(b, 2) + ' = ' + fmt((1 - ps) * b, 4), 'warn');
      nodeBox(455, 302, 150, 'refused', fmt(1 - ps, 2) + ' x ' + fmt(1 - b, 2) + ' = ' + fmt((1 - ps) * (1 - b), 4));

      // both refused branches merge into one escalation event with probability 1 - P(ship)
      ctx.strokeStyle = c.faint;
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(530, 145); ctx.lineTo(585, 185); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(530, 295); ctx.lineTo(585, 205); ctx.stroke();
      ctx.save();
      ctx.translate(596, 195);
      ctx.rotate(Math.PI / 2);
      ctx.fillStyle = c.soft;
      ctx.textAlign = 'center';
      ctx.fillText('escalate, P = ' + fmt(1 - pShip, 4), 0, -4);
      ctx.restore();

      say(fig, 'path1', fmt(ps * a));
      say(fig, 'path2', fmt((1 - pShip) * pf));
      say(fig, 'sumpaths', fmt(ps * a + (1 - pShip) * pf));
      say(fig, 'pfinal', fmt(ps * a + (1 - pShip) * pf));
    }

    ['ps', 'pf', 'a', 'b'].forEach(function (r) {
      var el = role(fig, r);
      if (el) { el.addEventListener('input', render); }
    });
    return { render: render };
  }

  /* ======================================================================
     Panel: cascade-lab (lesson 0005)
     The M2 milestone: derive P(final correct) and E[cost] for the cascade,
     then let 40,000 simulated requests check the derivation. If the
     analytic bar sits visibly BELOW the simulated one, the derivation
     forgot to pay the frontier on refusals of correct answers.
     ====================================================================== */
  function cascadeLab(fig) {
    var W = 640, H = 320;

    function render() {
      var ps = num(fig, 'ps') / 100;
      var pf = num(fig, 'pf') / 100;
      var a = num(fig, 'a') / 100;
      var b = num(fig, 'b') / 100;
      var seed = num(fig, 'seed') || 42;
      var parts = cascadeParts(ps, pf, a, b);
      var sim = simulate(TRIALS, seed, function (rng) {
        var right = rng() < ps;                 // was the nano answer actually right?
        var ship = rng() < (right ? a : b);     // does the check ship it?
        if (ship) { return { correct: right ? 1 : 0, cost: NANO_COST }; }
        return { correct: rng() < pf ? 1 : 0, cost: NANO_COST + FRONTIER_COST };
      });

      say(fig, 'pship', fmt(parts.pShip));
      say(fig, 'pc-a', fmt(parts.pCorrect));
      say(fig, 'pc-s', fmt(sim.p));
      say(fig, 'ec-a', money(parts.eCost));
      say(fig, 'ec-s', money(sim.cost));
      say(fig, 'agree', fmt(Math.abs(parts.pCorrect - sim.p)) + ' (tolerance 0.02)');

      var c = colors();
      var ctx = ctx2d(fig.querySelector('canvas'), W, H);
      var padL = 56, padB = 30, padT = 20;
      // P bars live on 0..1; cost bars are anchored to one frontier call,
      // so the reader sees the escalation premium against a known quantity.
      var groups = [
        { label: 'P(final correct)', av: parts.pCorrect, sv: sim.p, fa: fmt(parts.pCorrect), fs: fmt(sim.p) },
        { label: 'E[cost], one frontier call = full width', av: parts.eCost / FRONTIER_COST, sv: sim.cost / FRONTIER_COST, fa: money(parts.eCost), fs: money(sim.cost) }
      ];
      var slot = (W - padL - 16) / 2;
      var bw = 52;
      function Y0() { return H - padB; }
      function Yh(f) { return f * (H - padT - padB); }

      groups.forEach(function (g, gi) {
        var x0 = padL + slot * gi + slot / 2;
        ctx.fillStyle = c.accent;
        ctx.fillRect(x0 - bw - 3, Y0() - Yh(g.av), bw, Yh(g.av));
        ctx.fillStyle = c.accent2;
        ctx.fillRect(x0 + 3, Y0() - Yh(g.sv), bw, Yh(g.sv));
        ctx.fillStyle = c.accent;
        ctx.textAlign = 'center';
        ctx.fillText(g.fa, x0 - bw / 2 - 3, Y0() - Yh(g.av) - 6);
        ctx.fillStyle = c.accent2;
        ctx.fillText(g.fs, x0 + bw / 2 + 3, Y0() - Yh(g.sv) - 6);
        ctx.fillStyle = c.soft;
        ctx.fillText('analytic', x0 - bw / 2 - 3, Y0() + 12);
        ctx.fillText('simulated', x0 + bw / 2 + 3, Y0() + 12);
        ctx.fillText(g.label, x0, H - 10);
      });
      ctx.strokeStyle = c.grid;
      ctx.beginPath(); ctx.moveTo(padL, Y0()); ctx.lineTo(W - 12, Y0()); ctx.stroke();
    }

    ['ps', 'pf', 'a', 'b', 'seed'].forEach(function (r) {
      var el = role(fig, r);
      if (el) { el.addEventListener('input', render); }
    });
    var btn = role(fig, 'rerun');
    if (btn) { btn.addEventListener('click', render); }
    return { render: render };
  }

  /* ======================================================================
     Panel: bayes-grid (lesson 0006)
     Belief about ps as a discrete grid of hypotheses with a uniform prior.
     Every recorded trial multiplies each hypothesis by its likelihood and
     re-normalises; the bars are the posterior.
     ====================================================================== */
  function bayesGrid(fig) {
    var W = 640, H = 300;
    var GRID = [];
    for (var v = 0.60; v <= 0.951; v += 0.05) { GRID.push(Math.round(v * 100) / 100); }
    var weights = GRID.map(function () { return 1; }); // uniform prior
    var obs = [];

    function posterior() {
      var z = weights.reduce(function (s, w) { return s + w; }, 0);
      return weights.map(function (w) { return w / z; });
    }
    function meanPs() {
      var post = posterior();
      return post.reduce(function (s, pr, i) { return s + pr * GRID[i]; }, 0);
    }

    function record(correct) {
      obs.push(correct ? 1 : 0);
      weights = weights.map(function (w, i) { return w * (correct ? GRID[i] : 1 - GRID[i]); });
      render();
    }
    function reset() {
      obs = [];
      weights = GRID.map(function () { return 1; });
      render();
    }

    function render() {
      var post = posterior();
      var c = colors();
      var ctx = ctx2d(fig.querySelector('canvas'), W, H);
      var padL = 48, padB = 42, padT = 16;
      var plotW = W - padL - 14, base = H - padB;

      ctx.strokeStyle = c.grid;
      ctx.beginPath(); ctx.moveTo(padL, base); ctx.lineTo(W - 12, base); ctx.stroke();

      var slot = plotW / GRID.length;
      var bw = Math.min(46, slot * 0.62);
      GRID.forEach(function (h, i) {
        var xMid = padL + slot * (i + 0.5);
        ctx.fillStyle = c.accent;
        ctx.fillRect(xMid - bw / 2, base - post[i] * (base - padT), bw, post[i] * (base - padT));
        ctx.fillStyle = c.faint;
        ctx.textAlign = 'center';
        ctx.fillText(fmt(h, 2), xMid, base + 15);
        if (post[i] > 0.04) {
          ctx.fillStyle = c.ink;
          ctx.fillText(post[i].toFixed(2), xMid, base - post[i] * (base - padT) - 5);
        }
      });
      ctx.fillStyle = c.soft;
      ctx.fillText('hypothesis h for P(nano correct)', padL + plotW / 2, H - 4);

      var trials = obs.length;
      var hits = obs.reduce(function (s, o) { return s + o; }, 0);
      say(fig, 'ntrials', String(trials));
      say(fig, 'record', hits + ' correct of ' + trials);
      say(fig, 'emean', fmt(meanPs()));
      say(fig, 'obsrate', trials ? fmt(hits / trials) : '-');
    }

    if (role(fig, 'yes')) { role(fig, 'yes').addEventListener('click', function () { record(true); }); }
    if (role(fig, 'no')) { role(fig, 'no').addEventListener('click', function () { record(false); }); }
    if (role(fig, 'reset')) { role(fig, 'reset').addEventListener('click', reset); }
    return { render: render };
  }

  /* ======================================================================
     Panel: clump-lab (lesson 0007)
     Independence is an assumption, not a law. With clump probability c a
     whole batch of samples fails together; the promised (independence)
     bars stay fixed while the simulated bars sink toward their ceiling
     1 - c. Majority's promised gain evaporates first.
     ====================================================================== */
  function clumpLab(fig) {
    var W = 640, H = 320;
    var N = 5; // fixed batch size so the two bars stay comparable across the slider

    function render() {
      var p = num(fig, 'ps') / 100;
      var clump = num(fig, 'clump') / 100;
      var seed = num(fig, 'seed') || 42;

      var anyPromised = pAnyCorrect(N, p);
      var majPromised = pMajority(N, p);
      var simAny = simulate(TRIALS, seed, function (rng) {
        return { correct: drawBatch(rng, N, p, clump) > 0 ? 1 : 0, cost: N * NANO_COST };
      });
      var simMaj = simulate(TRIALS, seed + 1, function (rng) {
        return { correct: drawBatch(rng, N, p, clump) >= (N + 1) / 2 ? 1 : 0, cost: N * NANO_COST };
      });

      say(fig, 'any-p', fmt(anyPromised));
      say(fig, 'any-s', fmt(simAny.p));
      say(fig, 'maj-p', fmt(majPromised));
      say(fig, 'maj-s', fmt(simMaj.p));
      say(fig, 'ceiling', clump > 0 ? fmt(1 - clump) : '1');
      say(fig, 'gap-maj', fmt(majPromised - simMaj.p));

      var c = colors();
      var ctx = ctx2d(fig.querySelector('canvas'), W, H);
      var padL = 48, padB = 34, padT = 22, base = H - padB;
      var groups = [
        { label: 'nano x' + N + ' any-correct', prom: anyPromised, simv: simAny.p },
        { label: 'nano x' + N + ' majority', prom: majPromised, simv: simMaj.p }
      ];
      var slot = (W - padL - 16) / 2;
      var bw = 56;
      ctx.strokeStyle = c.grid;
      ctx.beginPath(); ctx.moveTo(padL, base); ctx.lineTo(W - 12, base); ctx.stroke();
      groups.forEach(function (g, gi) {
        var x0 = padL + slot * gi + slot / 2;
        ctx.fillStyle = rgba(c.accent, 0.45);
        ctx.fillRect(x0 - bw - 3, base - g.prom * (base - padT), bw, g.prom * (base - padT));
        ctx.fillStyle = c.warn;
        ctx.fillRect(x0 + 3, base - g.simv * (base - padT), bw, g.simv * (base - padT));
        ctx.fillStyle = c.soft;
        ctx.textAlign = 'center';
        ctx.fillText(g.label, x0, H - 10);
        ctx.fillStyle = c.accent;
        ctx.fillText('promised ' + fmt(g.prom), x0 - bw / 2 - 3, base - g.prom * (base - padT) - 6);
        ctx.fillStyle = c.warn;
        ctx.fillText('with clumping ' + fmt(g.simv), x0 + bw / 2 + 3, base - g.simv * (base - padT) - 6);
      });
      // the hard-prompt ceiling 1 - c
      if (clump > 0) {
        ctx.strokeStyle = c.gold;
        ctx.setLineDash([6, 4]);
        ctx.beginPath();
        ctx.moveTo(padL, base - (1 - clump) * (base - padT));
        ctx.lineTo(W - 12, base - (1 - clump) * (base - padT));
        ctx.stroke();
        ctx.setLineDash([]);
        ctx.fillStyle = c.gold;
        ctx.textAlign = 'left';
        ctx.fillText('ceiling 1 - c = ' + fmt(1 - clump, 2) + ': no n fixes this', padL + 6, base - (1 - clump) * (base - padT) - 6);
      }
    }

    ['ps', 'clump', 'seed'].forEach(function (r) {
      var el = role(fig, r);
      if (el) { el.addEventListener('input', render); }
    });
    var btn = role(fig, 'rerun');
    if (btn) { btn.addEventListener('click', render); }
    return { render: render };
  }

  /* ======================================================================
     Panel: vote-counting (lesson 0008)
     C(n,k) counting earns its keep: P(majority) is a sum over sequences,
     computed multiplicatively, checked against simulation.
     ====================================================================== */
  function voteCounting(fig) {
    var W = 640, H = 300;

    function render() {
      var n = Math.round(num(fig, 'n'));
      if (n % 2 === 0) { n += 1; }
      var p = num(fig, 'ps') / 100;
      var seed = num(fig, 'seed') || 42;

      var anyA = pAnyCorrect(n, p);
      var majA = pMajority(n, p);
      var simAny = simulate(20000, seed, function (rng) {
        return { correct: drawBatch(rng, n, p, 0) > 0 ? 1 : 0, cost: n * NANO_COST };
      });
      var simMaj = simulate(20000, seed + 7, function (rng) {
        return { correct: drawBatch(rng, n, p, 0) >= (n + 1) / 2 ? 1 : 0, cost: n * NANO_COST };
      });

      var maj = (n + 1) / 2;
      var terms = [];
      for (var k = maj; k <= n; k++) {
        terms.push('C(' + n + ',' + k + ')=' + choose(n, k).toLocaleString('en-US') +
          ': ' + (choose(n, k) * Math.pow(p, k) * Math.pow(1 - p, n - k)).toFixed(4));
      }
      say(fig, 'terms', terms.join('   '));
      say(fig, 'maj-n', String(n));
      say(fig, 'any-p', fmt(anyA));
      say(fig, 'any-s', fmt(simAny.p));
      say(fig, 'maj-p', fmt(majA));
      say(fig, 'maj-s', fmt(simMaj.p));

      var c = colors();
      var ctx = ctx2d(fig.querySelector('canvas'), W, H);
      var padL = 48, padB = 32, padT = 24, base = H - padB;
      var groups = [
        { label: 'P(at least one right)', prom: anyA, simv: simAny.p },
        { label: 'P(majority right)', prom: majA, simv: simMaj.p }
      ];
      var slot = (W - padL - 16) / 2;
      var bw = 58;
      ctx.strokeStyle = c.grid;
      ctx.beginPath(); ctx.moveTo(padL, base); ctx.lineTo(W - 12, base); ctx.stroke();
      groups.forEach(function (g, gi) {
        var x0 = padL + slot * gi + slot / 2;
        ctx.fillStyle = c.accent;
        ctx.fillRect(x0 - bw - 3, base - g.prom * (base - padT), bw, g.prom * (base - padT));
        ctx.fillStyle = c.accent2;
        ctx.fillRect(x0 + 3, base - g.simv * (base - padT), bw, g.simv * (base - padT));
        ctx.fillStyle = c.soft;
        ctx.textAlign = 'center';
        ctx.fillText(g.label, x0, H - 8);
        ctx.fillStyle = c.accent;
        ctx.textAlign = 'left';
        ctx.fillText('analytic ' + fmt(g.prom), x0 - bw - 3, base - g.prom * (base - padT) - 6);
        ctx.fillStyle = c.accent2;
        ctx.textAlign = 'right';
        ctx.fillText('simulated ' + fmt(g.simv), x0 + bw + 3, base - g.simv * (base - padT) - 6);
        ctx.textAlign = 'center';
      });
    }

    ['n', 'ps', 'seed'].forEach(function (r) {
      var el = role(fig, r);
      if (el) { el.addEventListener('input', render); }
    });
    var btn = role(fig, 'rerun');
    if (btn) { btn.addEventListener('click', render); }
    return { render: render };
  }

  /* ======================================================================
     Panel: planner-board (lesson 0009)
     The assembled Spend Planner: catalogue in, quality bar and priors as
     sliders, one row per policy with analytic and Monte-Carlo columns, a
     decision line that names the cheapest feasible policy or says plainly
     that none clears the bar, Bayes feedback from recorded validation
     outcomes, and a permalink that serialises the whole state.
     ====================================================================== */
  function plannerBoard(fig) {
    var W = 640, H = 260;
    var POLICIES = ['nano x1', 'frontier x1', 'any-correct', 'majority vote', 'cascade'];

    function readState() {
      var n = Math.round(num(fig, 'n'));
      if (n % 2 === 0) { n += 1; }
      return {
        q: num(fig, 'q') / 100,
        ps: num(fig, 'ps') / 100,
        pf: num(fig, 'pf') / 100,
        a: num(fig, 'a') / 100,
        b: num(fig, 'b') / 100,
        n: n,
        clump: num(fig, 'clump') / 100,
        seed: num(fig, 'seed') || 42
      };
    }

    function rows(s, sims) {
      var cas = cascadeParts(s.ps, s.pf, s.a, s.b);
      var list = [
        { name: 'single nano call', pa: s.ps, ca: NANO_COST },
        { name: 'single frontier call', pa: s.pf, ca: FRONTIER_COST },
        { name: 'nano x' + s.n + ' any-correct', pa: pAnyCorrect(s.n, s.ps), ca: s.n * NANO_COST },
        { name: 'nano x' + s.n + ' majority', pa: pMajority(s.n, s.ps), ca: s.n * NANO_COST },
        { name: 'cascade nano to frontier', pa: cas.pCorrect, ca: cas.eCost }
      ];
      if (sims) {
        list.forEach(function (r, i) { r.ps_ = sims[i].p; r.cs = sims[i].cost; });
      }
      return list;
    }

    function simulateAll(s) {
      var cf = FRONTIER_COST;
      return [
        simulate(TRIALS, s.seed, function (rng) { return { correct: rng() < s.ps ? 1 : 0, cost: NANO_COST }; }),
        simulate(TRIALS, s.seed + 11, function (rng) { return { correct: rng() < s.pf ? 1 : 0, cost: cf }; }),
        simulate(TRIALS, s.seed + 23, function (rng) {
          return { correct: drawBatch(rng, s.n, s.ps, s.clump) > 0 ? 1 : 0, cost: s.n * NANO_COST };
        }),
        simulate(TRIALS, s.seed + 37, function (rng) {
          return { correct: drawBatch(rng, s.n, s.ps, s.clump) >= (s.n + 1) / 2 ? 1 : 0, cost: s.n * NANO_COST };
        }),
        simulate(TRIALS, s.seed + 51, function (rng) {
          var right = rng() < s.ps;
          var ship = rng() < (right ? s.a : s.b);
          if (ship) { return { correct: right ? 1 : 0, cost: NANO_COST }; }
          return { correct: rng() < s.pf ? 1 : 0, cost: NANO_COST + cf };
        })
      ];
    }

    function decide(rowsList, useSimulated, q) {
      var best = null;
      rowsList.forEach(function (r) {
        var p = useSimulated ? r.ps_ : r.pa;
        var cost = useSimulated ? r.cs : r.ca;
        if (p >= q && (best === null || cost < best.cost)) { best = { name: r.name, p: p, cost: cost }; }
      });
      return best;
    }

    function writeTable(rowsList, haveSims) {
      var tbody = fig.querySelector('[data-out="policy-rows"]');
      if (!tbody) { return; }
      tbody.innerHTML = rowsList.map(function (r) {
        var simP = haveSims ? fmt(r.ps_) : '<span class="dim">not run</span>';
        var simC = haveSims ? money(r.cs) : '<span class="dim">not run</span>';
        return '<tr><td>' + r.name + '</td><td><b>' + fmt(r.pa) + '</b></td><td>' + simP +
          '</td><td><b>' + money(r.ca) + '</b></td><td>' + simC + '</td></tr>';
      }).join('');
    }

    function writeDecision(best, q) {
      var line = out(fig, 'decision');
      if (!line) { return; }
      if (best) {
        line.innerHTML = 'Cheapest policy clearing the bar: <b>' + best.name + '</b> at <b>' +
          money(best.cost) + '</b> per request, P(correct) ' + fmt(best.p) + ' &ge; target ' + fmt(q, 3) + '.';
      } else {
        line.innerHTML = '<b>No policy on this board clears a ' + fmt(q, 3) +
          ' bar.</b> The honest answer is that the plan is infeasible: raise reliability estimates, add a better check, or change the policy family.';
      }
    }

    function writeHash(s, obs) {
      try {
        window.history.replaceState(null, '', '#' + [
          'q=' + (s.q * 100).toFixed(1), 'ps=' + (s.ps * 100).toFixed(0),
          'pf=' + (s.pf * 100).toFixed(1), 'a=' + (s.a * 100).toFixed(0),
          'b=' + (s.b * 100).toFixed(0), 'n=' + s.n, 'c=' + (s.clump * 100).toFixed(0),
          'obs=' + obs.join('')
        ].join('&'));
      } catch (e) { /* sandboxed contexts may refuse; the button still works */ }
    }

    var obs = [];

    function bayesMean() {
      if (!obs.length) { return num(fig, 'ps') / 100; }
      var h0 = 0.60, step = 0.05, count = 8;
      var wts = [], i;
      for (i = 0; i < count; i++) { wts.push(1); }
      for (var t = 0; t < obs.length; t++) {
        for (i = 0; i < count; i++) {
          var h = h0 + step * i;
          wts[i] *= obs[t] ? h : 1 - h;
        }
      }
      var z = wts.reduce(function (s2, w) { return s2 + w; }, 0);
      var mean = 0;
      for (i = 0; i < count; i++) { mean += (wts[i] / z) * (h0 + step * i); }
      return mean;
    }

    var lastSims = null;

    function render() {
      var s = readState();
      var listRows = rows(s, lastSims);
      writeTable(listRows, !!lastSims);
      writeDecision(decide(listRows, !!lastSims, s.q), s.q);
      say(fig, 'bayes-n', String(obs.length));
      say(fig, 'bayes-mean', fmt(bayesMean()));
      say(fig, 'costs', 'per request: nano ' + money(NANO_COST) + ', frontier ' + money(FRONTIER_COST));
      writeHash(s, obs);

      // canvas: P(correct) per policy against the target line
      var c = colors();
      var ctx = ctx2d(fig.querySelector('canvas'), W, H);
      var padL = 150, padR = 60, padT = 18, base = H - 26;
      var plotW = W - padL - padR;
      ctx.strokeStyle = c.grid;
      ctx.beginPath(); ctx.moveTo(padL, base); ctx.lineTo(W - padR, base); ctx.stroke();
      listRows.forEach(function (r, i) {
        var p = lastSims ? r.ps_ : r.pa;
        var y = padT + (base - padT) * (i + 0.5) / listRows.length;
        var wBar = Math.max(0, Math.min(1, p)) * plotW;
        ctx.fillStyle = p >= s.q ? c.ok : c.warn;
        ctx.globalAlpha = 0.75;
        ctx.fillRect(padL, y - 11, wBar, 20);
        ctx.globalAlpha = 1;
        ctx.fillStyle = c.soft;
        ctx.textAlign = 'right';
        ctx.font = '12px Inter, system-ui, sans-serif';
        ctx.fillText(r.name, padL - 6, y + 4);
        ctx.textAlign = 'left';
        ctx.fillStyle = c.faint;
        ctx.fillText(money(lastSims ? r.cs : r.ca), padL + wBar + 6, y + 4);
      });
      ctx.font = '13px Inter, system-ui, sans-serif';
      var qx = padL + s.q * plotW;
      ctx.strokeStyle = c.accent;
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(qx, padT - 6); ctx.lineTo(qx, base); ctx.stroke();
      ctx.fillStyle = c.accent;
      ctx.textAlign = 'left';
      ctx.fillText('bar ' + fmt(s.q, 2), qx + 4, padT + 2);
    }

    function runSims() {
      lastSims = simulateAll(readState());
      render();
    }

    // wire controls
    ['q', 'ps', 'pf', 'a', 'b', 'n', 'clump'].forEach(function (r) {
      var el = role(fig, r);
      if (el) { el.addEventListener('input', function () { lastSims = null; render(); }); }
    });
    if (role(fig, 'rerun')) { role(fig, 'rerun').addEventListener('click', runSims); }
    if (role(fig, 'bayes-yes')) {
      role(fig, 'bayes-yes').addEventListener('click', function () {
        obs.push(1);
        var m = bayesMean();
        role(fig, 'ps').value = Math.round(m * 100);
        lastSims = null;
        render();
      });
    }
    if (role(fig, 'bayes-no')) {
      role(fig, 'bayes-no').addEventListener('click', function () {
        obs.push(0);
        var m = bayesMean();
        role(fig, 'ps').value = Math.round(m * 100);
        lastSims = null;
        render();
      });
    }
    if (role(fig, 'bayes-reset')) {
      role(fig, 'bayes-reset').addEventListener('click', function () {
        obs = [];
        lastSims = null;
        render();
      });
    }
    if (role(fig, 'permalink')) {
      role(fig, 'permalink').addEventListener('click', function () {
        var url = window.location.href;
        var done = function () {
          var note = out(fig, 'link-note');
          if (note) { note.textContent = 'Copied. Anyone opening it sees this exact board.'; }
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(done, done);
        } else {
          done();
        }
      });
    }

    // restore from the hash on load
    (function restore() {
      if (!window.location.hash || window.location.hash.length < 2) { return; }
      var params = {};
      window.location.hash.slice(1).split('&').forEach(function (kv) {
        var pair = kv.split('=');
        params[pair[0]] = pair[1];
      });
      function set(name, val) { var el = role(fig, name); if (el && isFinite(val)) { el.value = val; } }
      set('q', parseFloat(params.q)); set('ps', parseFloat(params.ps));
      set('pf', parseFloat(params.pf)); set('a', parseFloat(params.a));
      set('b', parseFloat(params.b)); set('n', parseInt(params.n, 10));
      set('clump', parseFloat(params.c));
      if (params.obs) {
        params.obs.split('').forEach(function (ch) { if (ch === '0' || ch === '1') { obs.push(+ch); } });
        if (obs.length) { set('ps', Math.round(bayesMean() * 100)); }
      }
    })();

    return { render: render };
  }

  /* ---------- registry, theme repaint, print --------------------------- */

  var panels = [];
  function mount(figId, factory) {
    var fig = document.getElementById(figId);
    if (!fig || fig.dataset.buildMounted) { return; }
    fig.dataset.buildMounted = '1';
    try {
      panels.push(factory(fig));
    } catch (err) {
      if (window.console) { console.warn('spend-planner: panel ' + figId + ' failed', err); }
    }
  }

  function renderAll() {
    for (var i = 0; i < panels.length; i++) {
      try { panels[i].render(); } catch (err) { if (window.console) { console.warn(err); } }
    }
  }

  new MutationObserver(function () { if (!printMode) { renderAll(); } })
    .observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
  window.addEventListener('beforeprint', function () { printMode = true; renderAll(); });
  window.addEventListener('afterprint', function () { printMode = false; renderAll(); });

  function init() {
    mount('coin-world', coinWorld);
    mount('complement-lab', complementLab);
    mount('check-grid', checkGrid);
    mount('path-products', pathProducts);
    mount('cascade-lab', cascadeLab);
    mount('bayes-grid', bayesGrid);
    mount('clump-lab', clumpLab);
    mount('vote-counting', voteCounting);
    mount('planner-board', plannerBoard);
    renderAll();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
