/* ============================================================
   The design system reference page - its live half.

   The page is complete and readable without this file. Every token row names
   its token, shows a specimen painted with that token by the stylesheet, and
   prints `var(--x)` where the value goes. What this adds is the value the
   browser actually resolved, which is the one thing a written page cannot hold
   without going stale.

   Three jobs, in order:

     1. fill every [data-token] with the resolved value of that property
     2. keep the fill correct across a mode, palette or design change, and
        across the two reading preferences, which is the second render state
        the whole framework has to be right in
     3. audit itself: count the custom properties `assets/hub.css` declares and
        say, on the page, which ones this page does not name

   Loaded with `defer`, after `assets/hub.js`, in the shape the build scripts in
   `probability-you-build-course/assets/builds/` already use. Zero dependencies,
   ES5, no build step, like everything else on this hub.
   ============================================================ */
(function () {
  'use strict';

  var root = document.documentElement;

  /* ---------- 1. the live values ----------
     A custom property's computed value is what is left after var() has been
     substituted, so `--measure` comes back as `72ch` rather than as a pixel
     count. That is the right answer for this page: `72ch` is what an author
     reads in the stylesheet and what a design would change.

     Four tokens are declared on a component rather than on <html> - the four
     `--sw-*` stripes of a palette swatch - so a row may name the element to
     read from with `data-token-in`. Everything else inherits down to the row
     itself, so the row is its own correct scope. */
  function valueOf(cell) {
    var selector = cell.getAttribute('data-token-in');
    var host = selector ? document.querySelector(selector) : cell;
    if (!host) return '';
    return getComputedStyle(host).getPropertyValue(cell.getAttribute('data-token')).trim();
  }

  function paint() {
    var cells = document.querySelectorAll('[data-token]');
    Array.prototype.forEach.call(cells, function (cell) {
      var value = valueOf(cell);
      // A token that resolves to nothing here is not a fault to hide. The
      // pre-production bar's height is set only where the hostname says
      // preprod, and saying so is more useful than an empty cell.
      cell.textContent = value || 'not set here';
    });
    paintState();
  }

  /* The five axes as the page's own readout: three the reader chooses, one the
     URL decides and one the hostname does. Reading them back off <html> is the
     same end-to-end check the computed-style harness makes. */
  var AXES = [
    { key: 'data-mode', fallback: 'system' },
    { key: 'data-palette', fallback: 'none' },
    { key: 'data-design', fallback: 'none' },
    { key: 'data-course', fallback: 'none' },
    { key: 'data-env', fallback: 'production' }
  ];

  function paintState() {
    AXES.forEach(function (axis) {
      var cell = document.querySelector('[data-axis="' + axis.key + '"]');
      if (cell) cell.textContent = root.getAttribute(axis.key) || axis.fallback;
    });
  }

  /* ---------- 2. the second render state ----------
     A mode, palette or design change rewrites an attribute on <html>; the two
     reading preferences write a `--*-user` property into its inline style. Both
     move values this page prints, and neither reloads the page, so the readout
     has to follow. This is the same MutationObserver the build contract in
     `references/widgets.md` prescribes for a canvas, and for the same reason:
     a value read once is a value that goes wrong the moment the reader moves an
     axis. */
  new MutationObserver(function () { paint(); drawRamp(); }).observe(root, {
    attributes: true,
    attributeFilter: ['data-mode', 'data-palette', 'data-design', 'data-env', 'style']
  });

  /* ---------- 3. the self-audit ----------
     The page names its tokens by hand, so it can fall behind a stylesheet that
     gains one. Rather than leave that to be noticed, the page counts: every
     custom property declared anywhere in `assets/hub.css`, against every name
     this page carries in a `data-token` or a `data-spec`.

     `cssRules` is readable because the sheet is same-origin. Opened straight
     off disk Chrome gives each file its own opaque origin and the read throws,
     so the audit says it could not run rather than reporting a false gap. */
  var DECLARATION = /(--[a-z0-9-]+)\s*:/g;

  function declaredTokens() {
    var found = {};
    var sheets = document.styleSheets;
    for (var s = 0; s < sheets.length; s += 1) {
      var href = sheets[s].href || '';
      if (href.indexOf('hub.css') === -1) continue;
      var rules;
      try { rules = sheets[s].cssRules; } catch (e) { return null; }
      if (!rules) return null;
      collect(rules, found);
    }
    return Object.keys(found).length ? found : null;
  }

  function collect(rules, found) {
    for (var r = 0; r < rules.length; r += 1) {
      var rule = rules[r];
      if (rule.cssRules) { collect(rule.cssRules, found); continue; }
      if (!rule.style) continue;
      var match;
      DECLARATION.lastIndex = 0;
      while ((match = DECLARATION.exec(rule.cssText)) !== null) found[match[1]] = true;
    }
  }

  function named() {
    var found = {};
    ['data-token', 'data-spec'].forEach(function (attribute) {
      var nodes = document.querySelectorAll('[' + attribute + ']');
      Array.prototype.forEach.call(nodes, function (node) {
        found[node.getAttribute(attribute)] = true;
      });
    });
    return found;
  }

  function audit() {
    var box = document.getElementById('ds-audit');
    if (!box) return;
    var declared = declaredTokens();
    if (declared === null) {
      box.textContent = 'The audit needs to read assets/hub.css, which a page opened '
        + 'straight off disk may not do. Serve the hub over http to run it.';
      return;
    }
    var here = named();
    var missing = Object.keys(declared).filter(function (name) { return !here[name]; }).sort();
    var total = Object.keys(declared).length;
    box.textContent = missing.length
      ? 'This page names ' + (total - missing.length) + ' of the ' + total
        + ' custom properties assets/hub.css declares. Not named here, so not documented: '
        + missing.join(', ') + '.'
      : 'This page names all ' + total
        + ' custom properties assets/hub.css declares. Nothing in the system is undocumented.';
  }


  /* ---------- the build demo's canvas ----------
     The widget gallery renders `figure.build` like every other widget, and a
     blank canvas would look like a fault rather than like a frame. So it draws
     something true: the eight steps of the space ramp, to scale.

     It follows the build contract in `references/widgets.md` exactly, because
     the page that documents the contract is a poor place to bend it. Colours
     are read from the tokens at draw time and never written as a literal - a
     canvas bakes colour into pixels, so unlike CSS it cannot follow a mode,
     palette or design change on its own. State lives outside the draw, and a
     MutationObserver repaints when an axis moves.

     The step lengths are measured off the specimens the stylesheet already
     drew, rather than converted from rem here. That keeps one source: if the
     ramp moves, the bars move, and no arithmetic in this file has to agree
     with the stylesheet about what a rem is. */
  var canvas = document.getElementById('ds-ramp-canvas');
  var stepsInput = document.getElementById('ds-ramp-steps');

  function tokenValue(name, fallback) {
    var value = getComputedStyle(root).getPropertyValue(name).trim();
    return value || fallback;
  }

  /* Print is the one render a canvas cannot follow, because the bitmap is
     painted before the print stylesheet applies. The paper twins of the ink and
     the surface are the raw light values, which are declared in both modes;
     each carries a fallback so a missing twin is loud rather than silent. */
  var forPaper = false;

  function ramp() {
    var lengths = [];
    for (var step = 1; step <= 8; step += 1) {
      var specimen = document.querySelector('.ds-spec[data-spec="--sp-' + step + '"]');
      lengths.push(specimen ? specimen.getBoundingClientRect().width : 0);
    }
    return lengths;
  }

  function drawRamp() {
    if (!canvas || !canvas.getContext) return;
    var context = canvas.getContext('2d');
    var shown = stepsInput ? Number(stepsInput.value) : 8;
    var ink = forPaper ? tokenValue('--l-ink', '#333') : tokenValue('--ink', '#333');
    var ground = forPaper ? tokenValue('--l-surface', '#fff') : tokenValue('--surface', '#fff');
    var mark = forPaper ? tokenValue('--l-accent', '#555') : tokenValue('--course-accent', '#555');

    context.setTransform(1, 0, 0, 1, 0, 0);
    context.fillStyle = ground;
    context.fillRect(0, 0, canvas.width, canvas.height);

    var lengths = ramp();
    var widest = Math.max.apply(null, lengths) || 1;
    var scale = (canvas.width - 150) / widest;
    var row = canvas.height / 9;

    context.font = '13px ' + tokenValue('--font-mono', 'monospace');
    context.textBaseline = 'middle';
    for (var index = 0; index < shown; index += 1) {
      var y = row * (index + 1);
      context.fillStyle = ink;
      context.fillText('--sp-' + (index + 1), 12, y);
      context.fillStyle = mark;
      context.fillRect(100, y - 5, Math.max(1, lengths[index] * scale), 10);
    }
    var count = document.getElementById('ds-ramp-count');
    var label = document.getElementById('ds-ramp-widest');
    if (count) count.textContent = String(shown);
    if (label) label.textContent = '--sp-' + shown;
  }

  if (stepsInput) stepsInput.addEventListener('input', drawRamp);
  window.addEventListener('beforeprint', function () { forPaper = true; drawRamp(); });
  window.addEventListener('afterprint', function () { forPaper = false; drawRamp(); });

  /* The palette swatch the `--sw-*` rows read from is built by `hub.js` at
     mount, and the fonts a size specimen is measured in arrive later still, so
     the first pass runs as soon as this file does and a second one runs at
     `load`, when both are certainly there. */
  paint();
  audit();
  drawRamp();
  window.addEventListener('load', function () { paint(); audit(); drawRamp(); });
  window.addEventListener('resize', drawRamp);
}());
