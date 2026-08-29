/* ============================================================
   Course Hub - the one shared runtime.

   Loaded from <head> without defer, so the persisted mode, palette and
   design are on <html> before the first paint and no page ever flashes
   the wrong colours or the wrong form.

   What it does, in order:
     1. head phase   - restore mode, palette, design and the two reading
                       preferences from localStorage
     2. mount phase  - build the rail from window.COURSE_OUTLINE,
                       build the topbar controls and settings popover,
                       and the pre-production bar when the host says so
     3. wire phase   - quiz, copy buttons, reading progress, Mermaid

   Every page links this one file. There is no per-course runtime.
   ============================================================ */
(function () {
  'use strict';

  var STORE = {
    mode:    'coursehub.mode',      // "light" | "dark" | "" (follow the system)
    palette: 'coursehub.palette',   // a palette key
    design:  'coursehub.design',    // a design key
    rail:    'coursehub.rail',      // "on" | "off"
    read:    'coursehub.read',      // { courseKey: [lesson file names] }
    legacy:  'llmcourse-theme'      // what the first design system wrote
  };

  /* ---------- the two reading preferences ----------
     Each one is a named step, not a raw length. Two properties follow from
     that and both matter.

     A stored step is validated against this table exactly as a palette key is,
     so a value from a step that was later withdrawn falls back to the default
     rather than leaving one reader with a page nobody else can see.

     And the value reaches the page as a `--*-user` custom property on <html>,
     which is the only thing a reader is allowed to write. hub.css resolves
     --measure and --fs-body from these; see the three-layer note there. Until
     2026-08 these were applied as an inline `--measure` on <html> and an inline
     `font-size` on <body>, which beat every stylesheet rule that was not
     !important and pinned a reader who had turned them on. Never write a
     resolved token from here.

     `legacy` and `on` carry the one-time migration from those two keys. A
     stored `wide=1` becomes the step that reproduces 52rem and a stored `big=1`
     the step that reproduces 1.3125rem, so a reader who had them on sees the
     same page after the migration as before it. */
  var READING = {
    measure: {
      store:  'coursehub.measure',
      prop:   '--measure-user',
      steps:  { normal: null, wide: '52rem' },
      legacy: 'coursehub.wide',
      on:     'wide'
    },
    bodysize: {
      store:  'coursehub.bodysize',
      prop:   '--fs-body-user',
      steps:  { normal: null, big: '1.3125rem' },
      legacy: 'coursehub.big',
      on:     'big'
    }
  };
  var READING_KEYS = Object.keys(READING);

  var PALETTES = [
    { key: 'paper',     label: 'Paper',     note: 'Warm cream, rust links, deep teal. The house identity.' },
    { key: 'slate',     label: 'Slate',     note: 'Cool neutral greys with an indigo accent.' },
    { key: 'ink',       label: 'Ink',       note: 'Near-monochrome, maximum contrast.' },
    { key: 'sage',      label: 'Sage',      note: 'Soft green paper, pine accent, low glare.' },
    { key: 'harbor',    label: 'Harbor',    note: 'Blue-grey daylight with deep teal and coral.' },
    { key: 'aubergine', label: 'Aubergine', note: 'Violet-grey with plum and old gold.' }
  ];
  var PALETTE_KEYS = PALETTES.map(function (p) { return p.key; });

  /* ---------- the design registry ----------
     A design is the form: the type scale, the leading, the weights, the
     tracking, the space ramp, the radii, the border weights, the shadow shape,
     the motion vocabulary and the eyebrow treatment. It carries no colour at
     all - that is the palette and mode axes - so registering a design costs no
     row in the contrast matrix.

     Each key here has a `:root[data-design="key"]` block in hub.css declaring
     the whole token set, and each such block is registered here. Neither half
     is trusted: `scripts/validate_site.py` fails the pull request on a key
     with no block, a block nobody can reach, and a block that declares only
     part of the set and would silently inherit the rest.

     The attribute is `data-design` rather than `data-theme` because "theme"
     already means two other things in this codebase - the dead `theme-btn`
     still in the source of 128 pages and removed at mount, and the
     `llmcourse-theme` key migrated once above - and a third meaning would be a
     maintenance trap.

     One design is registered on purpose. The axis and the second design are
     separate pieces of work, so the plumbing is debuggable before any design
     judgement is in play, and every reader keeps exactly the page they had.

     Withdrawing a design is one line and needs no deploy: delete its entry.
     The picker stops offering it, and a reader who had chosen it falls through
     to the default below, which was measured to restore the original exactly.
     The default is the first entry rather than a literal, so withdrawing the
     default is the same one-line edit as withdrawing any other. */
  var DESIGNS = [
    { key: 'house', label: 'House', note: 'Serif prose, sans headings and chrome. The hub as it reads today.' }
  ];
  var DESIGN_KEYS = DESIGNS.map(function (d) { return d.key; });

  var root = document.documentElement;

  /* ---------- storage that never throws ----------
     Chrome gives every file:// page its own opaque origin, so reading
     localStorage there can raise. A reader with storage blocked still gets a
     working page; they just get the default palette on every load. */
  function get(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
  function set(key, value) { try { localStorage.setItem(key, value); } catch (e) { /* read-only session */ } }
  function drop(key) { try { localStorage.removeItem(key); } catch (e) { /* read-only session */ } }

  /* ============================================================
     1. HEAD PHASE - runs before the body is parsed
     ============================================================ */
  var mode = get(STORE.mode);
  if (mode === null) {
    // one-time migration from the first design system's single theme key
    var legacy = get(STORE.legacy);
    if (legacy === 'dark' || legacy === 'light') { mode = legacy; set(STORE.mode, legacy); }
    drop(STORE.legacy);
  }
  if (mode === 'light' || mode === 'dark') root.setAttribute('data-mode', mode);

  var palette = get(STORE.palette);
  if (PALETTE_KEYS.indexOf(palette) === -1) palette = 'paper';
  root.setAttribute('data-palette', palette);

  /* The third reader axis: the form. Written here, in the head phase, for the
     same reason the palette is - the attribute has to be on <html> before the
     first paint or the page shows one design and settles into another.

     The stored value is validated against the registry and an unknown one
     falls back to the registered default, which is the guard that makes the
     kill switch work: a reader who chose a design that was later withdrawn
     lands on the default rather than on a page nobody else can see and nobody
     else can reproduce. Storage that raises returns null through `get`, which
     is not a registered key either, so a reader with storage blocked gets the
     same default and the same correct page. */
  var design = get(STORE.design);
  if (DESIGN_KEYS.indexOf(design) === -1) design = DESIGNS[0].key;
  root.setAttribute('data-design', design);

  /* The two reading preferences, restored here rather than when the appearance
     panel is built, so a reader who widened the column or asked for larger type
     gets it with the first paint instead of a step after it. */
  function readStep(axis) {
    var step = get(axis.store);
    if (step === null) {
      // one-time migration from the inline-style era; see READING above
      if (get(axis.legacy) === '1') { step = axis.on; set(axis.store, step); }
      drop(axis.legacy);
    }
    return Object.prototype.hasOwnProperty.call(axis.steps, step) ? step : 'normal';
  }

  function applyStep(axis, step) {
    var value = axis.steps[step];
    if (value) root.style.setProperty(axis.prop, value);
    else root.style.removeProperty(axis.prop);
  }

  var reading = {};
  READING_KEYS.forEach(function (name) {
    reading[name] = readStep(READING[name]);
    applyStep(READING[name], reading[name]);
  });

  /* The fourth axis: which course this page belongs to. Mode, palette and
     design are the reader's choices; this one is a property of the page, and it is what stops
     seven courses on one design system from looking interchangeable. The course
     is its folder, which is in the path on the live site, on a bucket prefix and
     on disk alike, so nothing has to be written into any page. The last match
     wins because a course folder is the deepest one that can carry the suffix.
     hub.css turns the name into a hue offset; a name it does not know, and the
     hub landing page which has no course folder at all, both fall through to the
     palette accent unrotated. */
  var courseHits = location.pathname.match(/[^/]+-course(?=\/)/g);
  if (courseHits) root.setAttribute('data-course', courseHits[courseHits.length - 1]);

  /* The fifth axis: which stage of the hub this page was served from. One
     repository publishes to two buckets, so the answer is a property of the
     host, not of anything a page could carry. Stamping it here, in the head
     phase, lets hub.css paint the warning bar with the first paint rather than
     after it. The live bucket has no "preprod" in its name, so on production
     the attribute is absent, the bar is never built, and every rule that keys
     off it is dead weight the browser never matches. Opened from disk,
     hostname is empty and the page looks exactly like the live one. */
  if (location.hostname.indexOf('preprod') !== -1) root.setAttribute('data-env', 'preprod');

  /* Mermaid renders itself on DOMContentLoaded unless told otherwise, and it
     would do so before the palette tokens have been read, producing a diagram
     in its own stock colours. Claim the render here, while the page is still
     parsing, so the only render that happens is the themed one below. */
  if (window.mermaid && window.mermaid.initialize) {
    window.mermaid.initialize({ startOnLoad: false });
  }

  /* ============================================================
     COLOUR TOKENS, READ BACK OUT OF CSS
     Custom properties compute to a token sequence, not to a colour, so a
     token holding color-mix() cannot be read with getPropertyValue. Painting
     it onto a probe element and reading the resolved colour works for every
     token, which is what lets Mermaid follow the palette with no JS palette
     table of its own.
     ============================================================ */
  var probe = null;
  var swatch = null;

  /* Chrome resolves a color-mix() token to a color(srgb ...) string, which
     Mermaid's colour library rejects, so every value is normalised to plain
     hex by painting one pixel and reading it back. */
  function asHex(value) {
    if (!swatch) {
      var canvas = document.createElement('canvas');
      canvas.width = 1;
      canvas.height = 1;
      swatch = canvas.getContext('2d', { willReadFrequently: true });
    }
    swatch.fillStyle = '#000000';
    swatch.fillStyle = value;
    swatch.fillRect(0, 0, 1, 1);
    var pixel = swatch.getImageData(0, 0, 1, 1).data;
    return '#' + [pixel[0], pixel[1], pixel[2]].map(function (channel) {
      return ('0' + channel.toString(16)).slice(-2);
    }).join('');
  }

  function token(name) {
    if (!probe) {
      probe = document.createElement('span');
      probe.style.cssText = 'position:absolute;width:0;height:0;visibility:hidden';
      document.body.appendChild(probe);
    }
    probe.style.color = '';
    probe.style.color = 'var(' + name + ')';
    return asHex(getComputedStyle(probe).color);
  }

  /* An undeclared custom property is invalid at computed-value time, and for
     `color` that means `inherit`, so the probe would hand back the surrounding
     text colour and report a confident wrong answer. Ask the cascade whether
     the name exists before trusting it. */
  function tokenExists(name) {
    return getComputedStyle(root).getPropertyValue(name).trim() !== '';
  }

  /* ---------- a token inside a Mermaid classDef ----------
     Mermaid's flowchart grammar rejects a parenthesis in a classDef value, so
     `classDef keep fill:var(--ok-soft)` never reaches the renderer: it is a
     parse error, and Mermaid draws a red error box rather than logging
     anything. A diagram that needs a colour of its own therefore had to write
     a hex literal, which is theme-blind by construction and wrong in one of the
     two modes - a near-white fill under near-white labels in dark, on the
     published site.

     The source keeps the honest spelling and the token is resolved on the way
     in, from the same probe that themes the rest of the diagram. So a classDef
     follows the palette, both modes and every repaint like everything else, and
     an author writes the token they already know.

     A name the stylesheet does not declare is left as it was written. That
     turns a typo into the red error box the author sees at once, instead of a
     colour quietly taken from whatever the probe inherited. */
  var TOKEN_DECL = /\b([a-z-]+)\s*:\s*var\(\s*(--[a-z0-9-]+)\s*\)/gi;

  function resolveTokens(source, forProperty) {
    return source.replace(TOKEN_DECL, function (whole, property, name) {
      if (!tokenExists(name)) return whole;
      return property + ':' + forProperty(property.toLowerCase(), name);
    });
  }

  /* ============================================================
     MERMAID - themed from the live tokens, re-rendered in place
     ============================================================ */
  /* Mermaid colours a mindmap's branches and a timeline's periods from a
     built-in twelve-step scale that it generates from its own theme rather than
     from the variables handed to it, and two of those steps land within 1.1:1 of
     the page - a near-black fill on a dark surface, a near-white one on a light
     surface - so the branch vanishes and its labels float unattached. Naming the
     scale explicitly is the whole fix. cScaleN is the branch fill and gets a
     soft tint of the step, cScaleLabelN is the text Mermaid paints on it and
     gets ordinary ink, and the rule that draws a branch's underline reads
     cScaleInvN, which Mermaid otherwise derives by inverting the fill and which
     therefore lands on a washed-out grey with none of the branch's hue in it.
     cScalePeerN is named as well because the mindmap renderer reaches for it.
     The eight steps come from --branch-0..7 in hub.css; 8 to 11 repeat the first
     four, because a diagram that deep is better served by a repeated hue than by
     a Mermaid default that may be invisible.

     Mermaid numbers a section's colour one step ahead of the section itself -
     the root is section -1 and takes step 0 - so twelve entries cover a diagram
     with eleven branches. */
  function branchScale() {
    var scale = {};
    for (var i = 0; i < 12; i += 1) {
      var step = i % 8;
      scale['cScale' + i] = token('--branch-' + step + '-soft');
      scale['cScaleLabel' + i] = token('--ink');
      scale['cScaleInv' + i] = token('--branch-' + step);
      scale['cScalePeer' + i] = token('--branch-' + step);
    }
    return scale;
  }

  /* `--font-ui` and not `--sans`: the role, not the registry. `hub.css` paints
     every diagram with `.mermaid { font-family: var(--font-ui) }`, so a design
     that moves the chrome face moves what the reader sees. Mermaid measures
     each label from this value instead, and the two must be the same face or
     every box is cut to the wrong width - which is the clipping defect one
     layer further back, latent until the first design moves that face. Today
     `--font-ui` is `var(--sans)` and the two spellings resolve identically; a
     custom property holding a var() is substituted at computed-value time, so
     `getPropertyValue` hands back the whole stack either way. */
  function mermaidVars() {
    var vars = {
      fontFamily: getComputedStyle(root).getPropertyValue('--font-ui').trim() || 'sans-serif',
      fontSize: '15px',
      background: token('--surface-3'),
      primaryColor: token('--accent2-soft'),
      primaryTextColor: token('--ink'),
      primaryBorderColor: token('--accent-2'),
      secondaryColor: token('--accent2-soft'),
      secondaryTextColor: token('--ink'),
      secondaryBorderColor: token('--accent-2'),
      tertiaryColor: token('--code-bg'),
      tertiaryTextColor: token('--ink'),
      tertiaryBorderColor: token('--line-strong'),
      lineColor: token('--ink-faint'),
      textColor: token('--ink'),
      mainBkg: token('--accent2-soft'),
      nodeBorder: token('--accent-2'),
      clusterBkg: token('--surface-2'),
      clusterBorder: token('--line-strong'),
      titleColor: token('--ink'),
      edgeLabelBackground: token('--surface-3'),
      noteBkgColor: token('--gold-soft'),
      noteTextColor: token('--ink'),
      noteBorderColor: token('--gold')
    };
    var scale = branchScale();
    for (var name in scale) { if (Object.prototype.hasOwnProperty.call(scale, name)) vars[name] = scale[name]; }
    return vars;
  }

  /* Above this width the rail is a column in the grid. Below it, the rail is a
     drawer over the content, and its state is transient. The number must match
     the breakpoint in hub.css. */
  function isWide() {
    return !window.matchMedia || window.matchMedia('(min-width: 1041px)').matches;
  }

  function isDark() {
    var explicit = root.getAttribute('data-mode');
    if (explicit) return explicit === 'dark';
    return !!(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
  }

  /* Mermaid sizes every node from a measurement it takes at render time, so a
     render that happens before the web font has been applied measures in the
     fallback face. Inter is wider than the system fallback at the same size, so
     the label then overflows the box that was cut for it and the last word or
     two is clipped - on the published site, on 380 flowcharts. It looks perfect
     on the next repaint, which is how it survived review. Waiting for the font
     is the whole fix; the timeout is there so a font that never arrives leaves
     a late diagram rather than none at all. */
  function whenFontsReady(run) {
    if (!document.fonts || !document.fonts.ready) { run(); return; }
    var done = false;
    var go = function () { if (!done) { done = true; run(); } };
    document.fonts.ready.then(go, go);
    setTimeout(go, 2000);
  }

  function renderMermaid() {
    if (!window.mermaid) return;
    var nodes = document.querySelectorAll('.mermaid');
    if (!nodes.length) return;
    repainting = true;
    Array.prototype.forEach.call(nodes, function (node) {
      // Rendering replaces the graph source with an <svg>, so the source is
      // stashed on the node the first time round and restored on every repaint.
      if (node.dataset.mmd === undefined) {
        node.dataset.mmd = node.textContent;
      } else {
        // Hold the rendered height while the SVG is briefly text again, or the
        // page collapses under the reader and the scroll position jumps.
        var box = node.getBoundingClientRect();
        if (box.height) node.style.minHeight = box.height + 'px';
      }
      // The stash keeps the token spelling, so every repaint resolves against
      // the mode and palette in force at that moment rather than the first one.
      node.textContent = resolveTokens(node.dataset.mmd, function (property, name) {
        return token(name);
      });
      node.removeAttribute('data-processed');
    });
    var release = function () {
      Array.prototype.forEach.call(nodes, function (node) { node.style.minHeight = ''; });
      settleDiagrams();   // the SVGs exist only now, and their width is final
      repainting = false;
      schedulePrintCopies();
    };
    window.mermaid.initialize(mermaidConfig(isDark(), mermaidVars()));
    try {
      var done = window.mermaid.run({ querySelector: '.mermaid' });
      if (done && done.then) done.then(release, release); else release();
    } catch (e) {
      if (window.mermaid.init) window.mermaid.init(undefined, nodes);
      release();
    }
  }

  /* ============================================================
     PRINTING A DIAGRAM
     Mermaid resolves every colour at render time and writes it into the SVG,
     so a diagram drawn while the reader was in dark mode carries dark fills and
     near-white labels into the printer. `hub.css` correctly forces the printed
     page white, which is exactly what makes the problem visible: the ground is
     paper and the labels are all but invisible on it.

     Re-rendering on `beforeprint` does not fix it. `mermaid.run()` is
     asynchronous and the browser takes its print snapshot long before the
     promise settles, and the first thing a repaint does is put the graph source
     back into the element - so the reader gets pages of raw Mermaid text, which
     is worse than a faint diagram. The ink-on-paper copy is therefore drawn
     ahead of time, while the browser is idle, and swapped in synchronously when
     the print begins.

     The print theme is fixed rather than read from the tokens, because the
     print block in `hub.css` already flattens the whole page to black ink on
     white paper and these are the same values. That also means the copy is
     correct whichever mode the reader is in when they press print.
     ============================================================ */
  var PRINT_FILL = ['#ffffff', '#eeeeee', '#f7f7f7', '#e4e4e4', '#fbfbfb', '#ebebeb', '#f2f2f2', '#e8e8e8'];
  var PRINT_EDGE = ['#000000', '#555555', '#222222', '#777777', '#333333', '#666666', '#111111', '#888888'];

  /* A token named in a classDef is resolved for paper by the role it is used
     for, not by a second colour table. hub.css's print block already flattens
     every semantic token to black ink on white paper, and the copy below is
     drawn in the screen medium where that block does not apply, so a table here
     would only be a duplicate of it that could go stale. A fill is the paper
     and everything else is the ink, which is the same answer the print block
     gives for --ok against --warn or --ok-soft against --warn-soft. */
  var PRINT_ROLE = { fill: '#ffffff' };

  function printToken(property) {
    return PRINT_ROLE[property] || '#000000';
  }

  function printVars() {
    var vars = {
      fontFamily: getComputedStyle(root).getPropertyValue('--font-ui').trim() || 'sans-serif',
      fontSize: '15px',
      background: '#ffffff',
      primaryColor: '#ffffff', primaryTextColor: '#000000', primaryBorderColor: '#000000',
      secondaryColor: '#ffffff', secondaryTextColor: '#000000', secondaryBorderColor: '#000000',
      tertiaryColor: '#f6f6f6', tertiaryTextColor: '#000000', tertiaryBorderColor: '#888888',
      lineColor: '#444444', textColor: '#000000',
      mainBkg: '#ffffff', nodeBorder: '#000000',
      clusterBkg: '#ffffff', clusterBorder: '#888888',
      titleColor: '#000000', edgeLabelBackground: '#ffffff',
      noteBkgColor: '#ffffff', noteTextColor: '#000000', noteBorderColor: '#333333'
    };
    for (var i = 0; i < 12; i += 1) {
      var step = i % 8;
      vars['cScale' + i] = PRINT_FILL[step];
      vars['cScaleLabel' + i] = '#000000';
      vars['cScaleInv' + i] = PRINT_EDGE[step];
      vars['cScalePeer' + i] = PRINT_EDGE[step];
    }
    return vars;
  }

  var repainting = false;      // a themed repaint is in flight
  var printCopies = null;      // node -> the SVG drawn for paper
  var printPass = 0;           // 0 idle, 1 running, 2 done
  var onPaper = null;          // node -> the SVG that was on screen before printing

  function mermaidConfig(dark, vars) {
    return {
      startOnLoad: false,
      theme: dark ? 'dark' : 'neutral',
      themeVariables: vars,
      flowchart: { curve: 'basis', htmlLabels: true, padding: 12, useMaxWidth: false },
      sequence: { useMaxWidth: false, wrap: true },
      state: { useMaxWidth: false }, class: { useMaxWidth: false }, er: { useMaxWidth: false },
      mindmap: { useMaxWidth: false }, timeline: { useMaxWidth: false }
    };
  }

  function schedulePrintCopies() {
    if (printPass !== 0 || !window.mermaid || !window.mermaid.render) return;
    var idle = window.requestIdleCallback || function (fn) { return setTimeout(fn, 400); };
    idle(function () { buildPrintCopies(); });
  }

  /* Renders every diagram a second time in the print theme and keeps the markup.
     A themed repaint starting mid-pass would leave half the copies drawn in the
     screen theme, so the pass abandons what it has and asks to be run again. */
  function buildPrintCopies() {
    if (printPass !== 0 || repainting) return;
    var nodes = Array.prototype.slice.call(document.querySelectorAll('.mermaid'));
    if (!nodes.length) { printPass = 2; return; }
    printPass = 1;
    var copies = new Map();
    /* Mermaid measures each label in whatever element it is handed, so the
       measuring element has to carry the same font as the finished diagram.
       Left to itself `render()` measures inside a bare container in the body
       serif, and every label comes out a shade too wide for the box that was
       cut for it. This is an off-screen `.mermaid`, so the `--font-ui` rule
       that governs the real diagrams governs the measurement too. */
    var stage = el('div', 'mermaid');
    stage.style.cssText = 'position:absolute;left:-99999px;top:0;visibility:hidden';
    document.body.appendChild(stage);
    window.mermaid.initialize(mermaidConfig(false, printVars()));

    var index = 0;
    var finish = function (complete) {
      printPass = complete ? 2 : 0;
      if (complete) printCopies = copies;
      if (stage.parentNode) stage.parentNode.removeChild(stage);
      window.mermaid.initialize(mermaidConfig(isDark(), mermaidVars()));
      if (!complete) schedulePrintCopies();
    };
    var step = function () {
      if (repainting) { finish(false); return; }
      if (index >= nodes.length) { finish(true); return; }
      var node = nodes[index];
      index += 1;
      var source = node.dataset.mmd;
      if (!source) { step(); return; }
      source = resolveTokens(source, printToken);
      var drawn;
      try {
        drawn = window.mermaid.render('mmd-print-' + index, source, stage);
      } catch (e) { finish(false); return; }
      if (!drawn || !drawn.then) { finish(false); return; }
      drawn.then(function (out) {
        copies.set(node, out.svg);
        step();
      }, function () { step(); });
    };
    step();
  }

  /* Chrome fires `beforeprint` and Safari changes the print media query, and a
     browser that does both would otherwise swap twice and stash the paper copy
     as the thing to restore afterwards. */
  /* A closed <details> does not print its contents, so a practice page would go
     to paper carrying its problems and none of its solutions. Open every one for
     the print and put each back exactly as the reader left it, so pressing print
     never silently spoils a problem they had not attempted yet.

     Unlike the Mermaid swap above there is nothing asynchronous here: setting
     `.open` reflows synchronously and the print snapshot sees it. Only the boxes
     that were shut are recorded, so a solution the reader had already opened
     stays open afterwards. This rides on toPaper and offPaper rather than on its
     own listeners, which is what gets it the Safari media-query path as well. */
  var reopened = null;

  function revealSolutions() {
    if (reopened) return;
    reopened = [];
    Array.prototype.forEach.call(document.querySelectorAll('.practice details'), function (box) {
      if (box.open) return;
      box.open = true;
      reopened.push(box);
    });
  }

  function restoreSolutions() {
    if (!reopened) return;
    reopened.forEach(function (box) { box.open = false; });
    reopened = null;
  }

  function toPaper() {
    revealSolutions();
    if (!printCopies || onPaper) return;
    onPaper = new Map();
    printCopies.forEach(function (svg, node) {
      if (!node.isConnected) return;
      onPaper.set(node, node.innerHTML);
      node.innerHTML = svg;
    });
  }

  function offPaper() {
    restoreSolutions();
    if (!onPaper) return;
    onPaper.forEach(function (svg, node) { node.innerHTML = svg; });
    onPaper = null;
  }

  /* ============================================================
     APPLYING A CHOICE
     One function per axis: set the attribute, persist it, repaint the
     diagrams. Nothing here reloads the page.
     ============================================================ */
  function applyMode(next) {
    if (next) { root.setAttribute('data-mode', next); set(STORE.mode, next); }
    else { root.removeAttribute('data-mode'); set(STORE.mode, ''); }
    renderMermaid();
    syncSettings();
  }
  function applyPalette(next) {
    root.setAttribute('data-palette', next);
    set(STORE.palette, next);
    renderMermaid();
    syncSettings();
  }

  /* The design repaints through `whenFontsReady`, which is the one thing that
     separates it from the two axes above. Mode and palette move colours, and a
     colour cannot change a text measurement. A design moves the faces, and
     Mermaid cuts every label box to a measurement it takes at render time: a
     repaint that starts before the new face is applied measures in the old one
     and clips the last word of 380 published flowcharts, which is the defect
     `whenFontsReady` was written for. It renders correctly on the next reload,
     so this has to be tested by switching rather than by loading. */
  function applyDesign(next) {
    root.setAttribute('data-design', next);
    set(STORE.design, next);
    /* `document.fonts.ready` answers for the fonts the document needs *now*,
       and a browser only discovers it needs a new face while it lays the page
       out. Read a layout property first, so the attribute above has been laid
       out and any face the new design asks for is already in flight when
       `whenFontsReady` asks. Without the flush the promise can be the settled
       one from the previous design and the wait is a no-op. One forced reflow,
       once per switch, against a whole page of clipped diagrams. */
    void root.offsetWidth;
    whenFontsReady(renderMermaid);
    syncSettings();
  }

  /* ============================================================
     2. MOUNT PHASE - the rail, the topbar controls, the settings panel
     ============================================================ */
  var settingsEl = null;

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  /* The manifest holds course-root-relative hrefs. The course root is the
     directory holding outline.js, which the script tag tells us, so the same
     manifest works from a lesson page, a reference page and the course map. */
  function courseBase() {
    var tag = document.querySelector('script[src$="outline.js"]');
    return tag ? new URL('.', tag.src).href : new URL('.', location.href).href;
  }

  function fileOf(href) { return href.split('#')[0].split('?')[0].split('/').pop(); }

  function readMap() {
    try { return JSON.parse(get(STORE.read) || '{}'); } catch (e) { return {}; }
  }
  function writeRead(map) { set(STORE.read, JSON.stringify(map)); }

  function mountRail(outline) {
    var base = courseBase();
    var here = fileOf(location.pathname);
    var read = readMap()[outline.key] || [];
    var total = 0, done = 0;

    var rail = el('aside', 'rail');
    rail.id = 'rail';
    rail.setAttribute('aria-label', 'Course outline');

    var head = el('div', 'rail-head');
    var up = el('a', 'up', '← All courses');
    up.href = new URL('../index.html', base).href;
    var title = el('h2');
    var titleLink = el('a', null, outline.title);
    titleLink.href = new URL('index.html', base).href;
    titleLink.style.color = 'inherit';
    titleLink.style.textDecoration = 'none';
    title.appendChild(titleLink);
    head.appendChild(up);
    head.appendChild(title);

    var prog = el('div', 'rail-prog');
    var bar = el('div', 'bar');
    var fill = el('i');
    bar.appendChild(fill);
    var pct = el('span', 'pct', '0%');
    var reset = el('button', 'reset', 'reset');
    reset.type = 'button';
    reset.title = 'Forget which lessons are marked read';
    prog.appendChild(bar); prog.appendChild(pct); prog.appendChild(reset);
    head.appendChild(prog);
    rail.appendChild(head);

    var search = el('div', 'rail-search');
    var input = el('input');
    input.type = 'search';
    input.id = 'rail-search';
    input.name = 'rail-search';
    input.placeholder = 'Search this course';
    input.setAttribute('aria-label', 'Search this course');
    search.appendChild(input);
    rail.appendChild(search);

    var list = el('div', 'rail-sections');
    outline.sections.forEach(function (section, index) {
      var box = el('details', 'rail-sec');
      var sum = el('summary');
      sum.appendChild(el('span', 'snum', section.n));
      sum.appendChild(el('span', null, section.title));
      sum.appendChild(el('span', 'caret', '›'));
      box.appendChild(sum);

      var items = el('ol');
      var hasCurrent = false;
      section.lessons.forEach(function (lesson) {
        total += 1;
        var file = fileOf(lesson.href);
        var isRead = read.indexOf(file) !== -1;
        if (isRead) done += 1;
        var link = el('a', 'rail-lesson');
        link.href = new URL(lesson.href, base).href;
        link.appendChild(el('span', 'dot'));
        link.appendChild(el('span', null, lesson.title));
        if (isRead) link.dataset.read = '1';
        if (file === here) { link.setAttribute('aria-current', 'page'); hasCurrent = true; }
        var row = el('li');
        row.appendChild(link);
        items.appendChild(row);
      });
      box.appendChild(items);
      // open the section the reader is in; on the course map open the first
      box.open = hasCurrent || (here === 'index.html' && index === 0);
      list.appendChild(box);
    });
    rail.appendChild(list);

    if (outline.extras && outline.extras.length) {
      var extraBox = el('details', 'rail-sec');
      extraBox.open = true;
      var extraSum = el('summary');
      extraSum.appendChild(el('span', 'snum', '·'));
      extraSum.appendChild(el('span', null, 'Reference'));
      extraSum.appendChild(el('span', 'caret', '›'));
      extraBox.appendChild(extraSum);
      var extraList = el('ol');
      outline.extras.forEach(function (extra) {
        var link = el('a', 'rail-lesson');
        link.href = new URL(extra.href, base).href;
        link.appendChild(el('span', 'dot'));
        link.appendChild(el('span', null, extra.title));
        if (fileOf(extra.href) === here) link.setAttribute('aria-current', 'page');
        var row = el('li');
        row.appendChild(link);
        extraList.appendChild(row);
      });
      extraBox.appendChild(extraList);
      rail.appendChild(extraBox);
    }

    document.body.insertBefore(rail, document.body.firstChild);

    function paintProgress() {
      var current = readMap()[outline.key] || [];
      var count = 0;
      Array.prototype.forEach.call(rail.querySelectorAll('.rail-lesson'), function (link) {
        var isRead = current.indexOf(fileOf(link.getAttribute('href'))) !== -1;
        if (isRead) { link.dataset.read = '1'; count += 1; } else { delete link.dataset.read; }
      });
      var share = total ? Math.round((count / total) * 100) : 0;
      fill.style.width = share + '%';
      pct.textContent = share + '%';
      prog.setAttribute('title', count + ' of ' + total + ' lessons marked read');
    }
    fill.style.width = (total ? Math.round((done / total) * 100) : 0) + '%';
    pct.textContent = (total ? Math.round((done / total) * 100) : 0) + '%';

    reset.addEventListener('click', function () {
      var map = readMap();
      delete map[outline.key];
      writeRead(map);
      paintProgress();
    });

    input.addEventListener('input', function () {
      var needle = input.value.trim().toLowerCase();
      Array.prototype.forEach.call(rail.querySelectorAll('.rail-sec'), function (section) {
        var matches = 0;
        Array.prototype.forEach.call(section.querySelectorAll('.rail-lesson'), function (link) {
          var hit = !needle || link.textContent.toLowerCase().indexOf(needle) !== -1;
          link.parentNode.hidden = !hit;
          if (hit) matches += 1;
        });
        section.hidden = needle && !matches;
        if (needle && matches) section.open = true;
      });
    });

    // mark the lesson read once the reader has actually got near the end
    if (here !== 'index.html' && outline.key) {
      var marked = false;
      var markIfDeep = function () {
        if (marked) return;
        var doc = document.documentElement;
        var scrolled = doc.scrollTop + window.innerHeight;
        if (scrolled < doc.scrollHeight - 400) return;
        marked = true;
        var map = readMap();
        var list2 = map[outline.key] || [];
        if (list2.indexOf(here) === -1) list2.push(here);
        map[outline.key] = list2;
        writeRead(map);
        paintProgress();
      };
      window.addEventListener('scroll', markIfDeep, { passive: true });
      markIfDeep();
    }

    // Only pull the rail to the current lesson when it is genuinely off-screen;
    // scrolling regardless would hide the course title on every short course.
    var current = rail.querySelector('[aria-current="page"]');
    if (current) {
      var seen = current.getBoundingClientRect();
      var frame = rail.getBoundingClientRect();
      if (seen.top < frame.top || seen.bottom > frame.bottom) {
        current.scrollIntoView({ block: 'center' });
      }
    }
  }

  /* ---------- the pre-production warning bar ----------
     A fixed strip along the foot of the viewport, so it stays in view at every
     scroll position on all 781 pages without touching the body grid, the
     sticky topbar or the rail's viewport arithmetic. */
  function mountStageFlag() {
    if (root.getAttribute('data-env') !== 'preprod') return;
    var flag = el('div', 'preprod-flag');
    flag.setAttribute('role', 'note');
    flag.appendChild(el('b', null, 'Pre-production'));
    flag.appendChild(el('span', null, 'This is the review site, not the live hub. Nothing here is published.'));
    document.body.appendChild(flag);
  }

  /* ---------- topbar controls ---------- */
  function mountTopbar(hasRail) {
    var spine = document.querySelector('.spine');
    if (!spine) return;
    var inner = spine.querySelector('.spine-inner') || spine;

    var progress = el('div', 'readbar');
    progress.appendChild(el('i'));
    spine.appendChild(progress);
    var fill = progress.firstChild;
    var paint = function () {
      var doc = document.documentElement;
      var span = doc.scrollHeight - window.innerHeight;
      fill.style.width = (span > 0 ? Math.min(100, (doc.scrollTop / span) * 100) : 0) + '%';
    };
    window.addEventListener('scroll', paint, { passive: true });
    window.addEventListener('resize', paint);
    paint();

    if (hasRail) {
      var toggle = el('button', 'tb-btn');
      toggle.type = 'button';
      toggle.title = 'Show or hide the course outline';
      toggle.setAttribute('aria-label', 'Toggle the course outline');
      toggle.appendChild(el('span', 'tb-icon', '☰'));
      toggle.addEventListener('click', function () {
        var next = document.body.dataset.rail === 'on' ? 'off' : 'on';
        document.body.dataset.rail = next;
        // Below the drawer breakpoint the rail is a transient overlay, not part
        // of the layout. Persisting it there would reopen the drawer on top of
        // the next lesson the reader navigates to.
        if (isWide()) set(STORE.rail, next);
      });
      inner.insertBefore(toggle, inner.firstChild);

      // In drawer mode, a click anywhere outside the rail dismisses it, which
      // covers the scrim without needing a real element behind the content.
      document.addEventListener('click', function (event) {
        if (isWide() || document.body.dataset.rail !== 'on') return;
        if (toggle.contains(event.target)) return;
        var rail = document.getElementById('rail');
        if (rail && rail.contains(event.target) && event.target.tagName !== 'A') return;
        document.body.dataset.rail = 'off';
      });
    }

    var legacy = inner.querySelector('.theme-btn');
    if (legacy) legacy.parentNode.removeChild(legacy);

    var button = el('button', 'tb-btn');
    button.type = 'button';
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-haspopup', 'dialog');
    button.appendChild(el('span', 'tb-icon', '◑'));
    button.appendChild(el('span', 'hide-sm', 'Appearance'));
    inner.appendChild(button);

    settingsEl = buildSettings();
    document.body.appendChild(settingsEl);

    function close() { settingsEl.hidden = true; button.setAttribute('aria-expanded', 'false'); }
    button.addEventListener('click', function (event) {
      event.stopPropagation();
      var open = settingsEl.hidden;
      settingsEl.hidden = !open;
      button.setAttribute('aria-expanded', String(open));
      if (open) syncSettings();
    });
    document.addEventListener('click', function (event) {
      if (settingsEl.hidden) return;
      if (settingsEl.contains(event.target) || button.contains(event.target)) return;
      close();
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') close();
    });
  }

  /* ---------- the appearance panel ---------- */
  var MODES = [
    { key: '',      label: 'System', glyph: '◐' },
    { key: 'light', label: 'Light',  glyph: '☀' },
    { key: 'dark',  label: 'Dark',   glyph: '☾' }
  ];

  function buildSettings() {
    var panel = el('div', 'settings');
    panel.hidden = true;
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Appearance');

    var modeGroup = el('div', 'set-group');
    modeGroup.appendChild(el('h3', null, 'Colour mode'));
    var modeCards = el('div', 'mode-cards');
    modeCards.style.gridTemplateColumns = 'repeat(3, 1fr)';
    MODES.forEach(function (item) {
      var card = el('button', 'mode-card');
      card.type = 'button';
      card.dataset.mode = item.key;
      card.appendChild(el('span', 'glyph', item.glyph));
      card.appendChild(el('span', null, item.label));
      card.addEventListener('click', function () { applyMode(item.key); });
      modeCards.appendChild(card);
    });
    modeGroup.appendChild(modeCards);
    panel.appendChild(modeGroup);

    var palGroup = el('div', 'set-group');
    palGroup.appendChild(el('h3', null, 'Colour palette'));
    var palCards = el('div', 'pal-cards');
    PALETTES.forEach(function (item) {
      var card = el('button', 'pal-card');
      card.type = 'button';
      card.dataset.palette = item.key;
      var swatch = el('span', 'pal-swatch');
      swatch.dataset.palette = item.key;
      for (var i = 0; i < 4; i += 1) swatch.appendChild(el('i'));
      card.appendChild(swatch);
      card.appendChild(el('span', 'pal-name', item.label));
      card.appendChild(el('span', 'pal-note', item.note));
      card.addEventListener('click', function () { applyPalette(item.key); });
      palCards.appendChild(card);
    });
    palGroup.appendChild(palCards);
    panel.appendChild(palGroup);

    /* The design group, in the shape of the palette group above and reusing
       its classes rather than inventing a pair the widget vocabulary does not
       know. It carries no swatch: a design has no colour to preview, which is
       the whole point of the split, and a swatch here would say otherwise.
       The column count follows the registry, as the mode group's already does,
       so one design reads as one full-width card rather than as half a row. */
    var designGroup = el('div', 'set-group');
    designGroup.appendChild(el('h3', null, 'Design'));
    var designCards = el('div', 'pal-cards');
    designCards.style.gridTemplateColumns = 'repeat(' + DESIGNS.length + ', 1fr)';
    DESIGNS.forEach(function (item) {
      var card = el('button', 'pal-card');
      card.type = 'button';
      card.dataset.design = item.key;
      card.appendChild(el('span', 'pal-name', item.label));
      card.appendChild(el('span', 'pal-note', item.note));
      card.addEventListener('click', function () { applyDesign(item.key); });
      designCards.appendChild(card);
    });
    designGroup.appendChild(designCards);
    designGroup.appendChild(el('p', 'set-note',
      'A design sets type, rhythm and shape. Colour is the palette above, so the two choose independently.'));
    panel.appendChild(designGroup);

    var prefGroup = el('div', 'set-group');
    prefGroup.appendChild(el('h3', null, 'Reading'));
    prefGroup.appendChild(readingRow('Wider text column', 'measure'));
    prefGroup.appendChild(readingRow('Larger type', 'bodysize'));
    var note = el('p', 'set-note',
      'Your choice is remembered in this browser and applies to every course in the hub.');
    prefGroup.appendChild(note);
    panel.appendChild(prefGroup);
    return panel;
  }

  /* Two steps today, a checkbox for each. The row reads the step the head phase
     already resolved rather than the store, so the panel and the page can never
     disagree about what is on. */
  function readingRow(label, name) {
    var axis = READING[name];
    var row = el('label', 'set-row');
    var box = el('input');
    box.type = 'checkbox';
    box.checked = reading[name] !== 'normal';
    box.addEventListener('change', function () {
      reading[name] = box.checked ? axis.on : 'normal';
      set(axis.store, reading[name]);
      applyStep(axis, reading[name]);
    });
    row.appendChild(box);
    row.appendChild(el('span', null, label));
    return row;
  }

  function syncSettings() {
    if (!settingsEl) return;
    var currentMode = root.getAttribute('data-mode') || '';
    Array.prototype.forEach.call(settingsEl.querySelectorAll('.mode-card'), function (card) {
      card.setAttribute('aria-pressed', String(card.dataset.mode === currentMode));
    });
    /* Two groups share the `.pal-card` shape, so each is asked for by the
       attribute that says which axis it selects. A bare `.pal-card` query
       would compare a design card's undefined palette against the live one and
       report every design as unpressed. */
    var currentPalette = root.getAttribute('data-palette');
    Array.prototype.forEach.call(settingsEl.querySelectorAll('.pal-card[data-palette]'), function (card) {
      card.setAttribute('aria-pressed', String(card.dataset.palette === currentPalette));
    });
    var currentDesign = root.getAttribute('data-design');
    Array.prototype.forEach.call(settingsEl.querySelectorAll('.pal-card[data-design]'), function (card) {
      card.setAttribute('aria-pressed', String(card.dataset.design === currentDesign));
    });
  }

  /* ---------- the widgets every lesson uses ---------- */
  /* Answering used to be reported by colour alone, and `disabled` removed the
     button the reader had just pressed from the tab order, which drops focus to
     <body> and costs a keyboard reader their place. Mark the outcome with a
     glyph and a spoken phrase, and keep every option exactly where the keyboard
     left it. Ported from the fix the live-site audit made in `course.js`. */
  function markOption(option, glyph, spokenLabel) {
    var mark = document.createElement('span');
    mark.className = 'q-mark';
    mark.setAttribute('aria-hidden', 'true');
    mark.textContent = glyph;
    var spoken = document.createElement('span');
    spoken.className = 'sr-only';
    spoken.textContent = spokenLabel + '. ';
    option.insertBefore(spoken, option.firstChild);
    option.insertBefore(mark, option.firstChild);
  }

  function wireQuizzes() {
    Array.prototype.forEach.call(document.querySelectorAll('.q'), function (question) {
      var answer = parseInt(question.getAttribute('data-answer'), 10);
      var options = question.querySelectorAll('.q-opt');
      var feedback = question.querySelector('.q-fb');
      if (feedback) feedback.setAttribute('aria-live', 'polite');
      Array.prototype.forEach.call(options, function (option, index) {
        option.addEventListener('click', function () {
          if (question.dataset.done) return;
          question.dataset.done = '1';
          Array.prototype.forEach.call(options, function (other, position) {
            if (position === answer) {
              other.classList.add('correct');
              markOption(other, '\u2713', 'Correct answer');
            } else if (position === index) {
              other.classList.add('wrong');
              markOption(other, '\u2717', 'Your answer, incorrect');
            }
            other.setAttribute('aria-disabled', 'true');
          });
          if (feedback) feedback.classList.add('show');
        });
      });
    });
  }

  /* ---------- diagrams: an accessible name, and keyboard reach ----------
     Mermaid returns an SVG with no accessible name, so a screen reader
     announces "flowchart" and nothing else, while the figcaption underneath
     already says in prose what the figure means. And a box that scrolls
     sideways is unreachable without a mouse until it can take focus. Both were
     fixed in `course.js` by the live-site audit; this is the same pair of
     passes for the new system. */
  function nameDiagrams() {
    Array.prototype.forEach.call(document.querySelectorAll('figure .mermaid svg'), function (svg) {
      if (svg.getAttribute('aria-label')) return;
      var figure = svg.closest('figure');
      var caption = figure && figure.querySelector('figcaption');
      if (!caption) return;
      svg.setAttribute('aria-label', caption.textContent.replace(/\s+/g, ' ').trim());
    });
  }

  /* Only a box that genuinely overflows gets a tab stop, and it gives the stop
     back when the column grows and it no longer does.

     Tables are here for the same reason the other three are. Below 720px
     `hub.css` gives a table `display: block; overflow-x: auto`, which turns a
     wide one into a scroll container with no way to reach its right-hand
     columns from the keyboard - `scrollable-region-focusable`, serious, WCAG
     2.1.1. Above that width the same table is an ordinary `display: table` that
     may still be wider than its column but scrolls nothing, so the computed
     overflow is checked as well: a box that cannot scroll never gets a tab stop
     it would have nothing to do with. */
  function scrolls(box) {
    if (box.scrollWidth <= box.clientWidth + 1) return false;
    var flow = getComputedStyle(box).overflowX;
    return flow === 'auto' || flow === 'scroll';
  }

  function markScrollables() {
    Array.prototype.forEach.call(document.querySelectorAll('.diagram, pre, .math, table'), function (box) {
      if (scrolls(box)) box.setAttribute('tabindex', '0');
      else if (box.getAttribute('tabindex') === '0') box.removeAttribute('tabindex');
    });
  }

  function settleDiagrams() {
    nameDiagrams();
    markScrollables();
  }

  function wireCopyButtons() {
    Array.prototype.forEach.call(document.querySelectorAll('pre'), function (block) {
      var button = el('button', 'copy-btn', 'copy');
      button.type = 'button';
      button.addEventListener('click', function () {
        var code = block.querySelector('code');
        var text = code ? code.innerText : block.innerText;
        if (navigator.clipboard) navigator.clipboard.writeText(text);
        button.textContent = 'copied';
        setTimeout(function () { button.textContent = 'copy'; }, 1200);
      });
      block.appendChild(button);
    });
  }

  /* ============================================================
     THE CAPABILITY MATRIX
     One row per capability key, one column per cloud, rendered from
     window.CLOUD_CAPABILITY_MATRIX (the data file beside the comparison
     course's index page). The author writes only the frame:

       <figure class="cmatrix"> ... <figcaption>...</figcaption></figure>

     and this builds the legend, the area filter, the search box and the
     rows inside it. Everything is plain DOM painted from CSS tokens, so a
     mode or palette change needs no re-render here - unlike Mermaid, whose
     colours are baked into the SVG at render time.

     Four cell states, which must never look alike (see widgets.md):
       unfilled  - nobody has written it yet; dashed and quiet
       absent    - this cloud ships no equivalent; a gold bar, and the only
                   state that says NO EQUIVALENT
       elsewhere - the cloud HAS the capability, delivered by a service that
                   holds a row under another key; a dotted green bar and a link
                   to that row
       service   - one or more services, each linking vendor documentation

     absent and elsewhere make opposite claims and both arrive as a gap entry in
     the inventories, so they are told apart on three signals at once, not one:
     the bar style (solid against dotted), the hue (--gold against --ok, which
     no palette aliases to each other), and the tag word. Print flattens both
     hues to the same grey, which is why the bar style and the tag carry the
     distinction on paper.

     A service that is not generally available carries a badge saying so. That
     is what tells a reader which of two services in one cell a new design
     should pick, because the pair is normally a current service beside the
     legacy one it replaces.
     ============================================================ */
  // What a non-GA badge means, spelled out for the reader who hovers it. A
  // status outside this list still badges, with no explanation to invent.
  var MATRIX_STATUS = {
    preview: 'Preview: announced but not generally available, so terms and behaviour can still change.',
    retiring: 'Retiring: still running, with a published end date. A new design should pick the current service beside it.',
    deprecated: 'Deprecated: closed to new use or already shut down. A new design should pick the current service beside it.'
  };

  function wireMatrix() {
    var frame = document.querySelector('figure.cmatrix');
    if (!frame) return;
    var caption = frame.querySelector('figcaption');
    var data = window.CLOUD_CAPABILITY_MATRIX;

    function fail(message) {
      var note = el('p', 'cmx-error', message);
      if (caption) frame.insertBefore(note, caption); else frame.appendChild(note);
    }

    if (!data || !Array.isArray(data.clouds) || !Array.isArray(data.domains) || !Array.isArray(data.rows)) {
      fail('The capability matrix data failed to load. This is a broken page, not an empty matrix.');
      return;
    }

    var clouds = data.clouds;
    var domainName = {};
    data.domains.forEach(function (d) { domainName[d.slug] = d.name; });

    /* ---------- legend ---------- */
    var legend = el('div', 'cmx-legend');
    [
      ['cmx-lg-service', 'Filled', 'a service answering the capability'],
      ['cmx-lg-elsewhere', 'Delivered elsewhere', 'the cloud has it, inside a service listed on another row'],
      ['cmx-lg-absent', 'No equivalent', 'the cloud ships nothing that answers it'],
      ['cmx-lg-unfilled', 'Not filled in yet', 'awaiting verified research']
    ].forEach(function (item) {
      var chip = el('span', 'cmx-lg');
      chip.appendChild(el('i', item[0]));
      chip.appendChild(el('span', null, item[1] + ' - ' + item[2]));
      legend.appendChild(chip);
    });
    frame.insertBefore(legend, caption);

    /* ---------- controls ---------- */
    var controls = el('div', 'cmx-controls');

    var areaLabel = el('label', 'cmx-control');
    areaLabel.appendChild(el('span', null, 'Area'));
    var select = el('select', 'cmx-area');
    select.name = 'cmx-area';
    select.setAttribute('aria-label', 'Filter the capability matrix by area');
    var allOpt = el('option', null, 'All areas (' + data.rows.length + ')');
    allOpt.value = 'all';
    select.appendChild(allOpt);
    data.domains.forEach(function (d) {
      var n = data.rows.filter(function (r) { return r.domain === d.slug; }).length;
      var opt = el('option', null, d.name + ' (' + n + ')');
      opt.value = d.slug;
      select.appendChild(opt);
    });
    areaLabel.appendChild(select);
    controls.appendChild(areaLabel);

    var searchLabel = el('label', 'cmx-control');
    searchLabel.appendChild(el('span', null, 'Search'));
    var search = el('input', 'cmx-search');
    search.type = 'search';
    search.name = 'cmx-search';
    search.placeholder = 'service or capability name';
    search.setAttribute('aria-label', 'Search the capability matrix by service or capability name');
    searchLabel.appendChild(search);
    controls.appendChild(searchLabel);

    var count = el('span', 'cmx-count');
    count.setAttribute('aria-live', 'polite');
    controls.appendChild(count);
    frame.insertBefore(controls, caption);

    /* ---------- rows ---------- */
    var table = el('div', 'cmx-table');
    table.setAttribute('role', 'table');
    table.setAttribute('aria-label', 'Cloud capability matrix');

    var headRow = el('div', 'cmx-row cmx-headrow');
    headRow.setAttribute('role', 'row');
    headRow.appendChild(el('div', 'cmx-cap', 'Capability'));
    clouds.forEach(function (c) {
      var h = el('div', 'cmx-colhead', c.short);
      h.setAttribute('role', 'columnheader');
      h.title = c.name;
      headRow.appendChild(h);
    });
    table.appendChild(headRow);

    // A cross-reference names the row a capability actually lives in, so the
    // reader needs the row's title rather than its key, and a way to get there.
    var rowTitle = {};
    data.rows.forEach(function (r) { rowTitle[r.key] = r.title || r.key; });
    var byKey = {};

    /* The jump a cross-reference offers. The target row can be filtered out -
       the reader is looking at one area and the capability lives in another -
       and an anchor into a hidden row silently goes nowhere, so the filter is
       cleared first whenever that would happen. */
    function crossLink(key) {
      var link = el('a', 'cmx-see');
      link.href = '#cmx-row-' + key;
      link.appendChild(el('span', 'cmx-see-arrow', '\u2192'));
      link.appendChild(document.createTextNode(' see ' + rowTitle[key]));
      link.title = 'Go to the ' + rowTitle[key] + ' row, where this cloud lists the service';
      link.addEventListener('click', function (ev) {
        var target = byKey[key];
        if (!target) return;
        ev.preventDefault();
        if (target.hidden) {
          select.value = 'all';
          search.value = '';
          state.area = 'all';
          state.q = '';
          apply();
        }
        target.scrollIntoView({ block: 'center' });
        target.setAttribute('tabindex', '-1');
        target.focus();
        target.classList.add('cmx-hit');
        setTimeout(function () { target.classList.remove('cmx-hit'); }, 2200);
      });
      return link;
    }

    var bodyRows = [];
    data.rows.forEach(function (row) {
      var tr = el('div', 'cmx-row');
      tr.setAttribute('role', 'row');
      tr.dataset.domain = row.domain;
      tr.id = 'cmx-row-' + row.key;
      byKey[row.key] = tr;

      var cap = el('div', 'cmx-cap');
      cap.setAttribute('role', 'rowheader');
      cap.appendChild(el('b', null, row.title || row.key));
      cap.appendChild(el('code', 'cmx-key', row.key));
      tr.appendChild(cap);

      var haystack = ((row.title || '') + ' ' + row.key + ' ' + (domainName[row.domain] || '')).toLowerCase();

      clouds.forEach(function (c) {
        var cellData = (row.cells || {})[c.key];
        var td = el('div', 'cmx-cell');
        td.setAttribute('role', 'cell');
        td.dataset.label = c.short;
        td.dataset.cloud = c.key;

        if (!cellData || typeof cellData !== 'object') {
          td.classList.add('cmx-unfilled');
          td.appendChild(el('span', 'cmx-unfilled-tag', 'Not filled in yet'));
          td.title = 'Nobody has filled this cell in yet.';
        } else if (cellData.state === 'unfilled') {
          td.classList.add('cmx-unfilled');
          td.appendChild(el('span', 'cmx-unfilled-tag', 'Not filled in yet'));
          td.title = 'Nobody has filled this cell in yet.';
        } else if (cellData.state === 'absent') {
          td.classList.add('cmx-absent');
          td.appendChild(el('span', 'cmx-absent-tag', 'No equivalent'));
          if (cellData.reason) td.appendChild(el('span', 'cmx-reason', cellData.reason));
          haystack += ' no equivalent';
        } else if (cellData.state === 'elsewhere') {
          // The cloud has the capability. Only the packaging differs, so this
          // must never wear the words the absence beside it wears.
          td.classList.add('cmx-elsewhere');
          td.appendChild(el('span', 'cmx-elsewhere-tag', 'Delivered elsewhere'));
          if (cellData.reason) td.appendChild(el('span', 'cmx-reason', cellData.reason));
          if (cellData.see && rowTitle[cellData.see]) td.appendChild(crossLink(cellData.see));
          // This is the one reason text worth indexing. A cross-reference names
          // the service that DOES answer the capability, which is what the
          // search box is for; an absence names what does not, and indexing
          // that would answer a service search with the rows lacking it.
          haystack += ' delivered elsewhere ' + (cellData.reason || '').toLowerCase();
        } else if (cellData.state === 'service' && Array.isArray(cellData.services)) {
          td.classList.add('cmx-service');
          cellData.services.forEach(function (s) {
            var svc = el('div', 'cmx-svc');
            if (s.doc_url) {
              var link = el('a', null, s.short_name || s.name || c.short);
              link.href = s.doc_url;
              link.title = (s.name || s.short_name || '') + ' - open in ' + c.name + ' documentation';
              svc.appendChild(link);
              if (s.name && s.short_name && s.name !== s.short_name) {
                svc.appendChild(el('span', 'cmx-fullname', s.name));
              }
            } else {
              svc.appendChild(el('b', null, s.short_name || s.name || ''));
            }
            if (s.status && s.status !== 'ga') {
              var badge = el('span', 'cmx-status', s.status);
              if (MATRIX_STATUS[s.status]) {
                badge.classList.add('cmx-st-' + s.status);
                badge.title = MATRIX_STATUS[s.status];
              }
              svc.appendChild(badge);
            }
            if (s.one_line) svc.appendChild(el('span', 'cmx-oneline', s.one_line));
            td.appendChild(svc);
            // 'ga' is every other service, so indexing it would match almost
            // every row; the statuses worth finding are the ones that badge.
            haystack += ' ' + ((s.name || '') + ' ' + (s.short_name || '') +
                               (s.status && s.status !== 'ga' ? ' ' + s.status : '')).toLowerCase();
          });
        } else {
          // An unknown shape is rendered as unfilled-looking but titled honestly,
          // and validate_site.py fails the pull request that produced it.
          td.classList.add('cmx-broken');
          td.appendChild(el('span', 'cmx-unfilled-tag', 'Broken cell'));
          td.title = 'This cell is none of the four states: a service, a capability delivered under another row, an absence with a reason, or unfilled.';
        }

        tr.dataset.haystack = haystack;
        tr.appendChild(td);
      });
      bodyRows.push(tr);
      table.appendChild(tr);
    });

    var emptyNote = el('div', 'cmx-empty', 'Nothing matches that filter.');
    emptyNote.hidden = true;
    table.appendChild(emptyNote);
    frame.insertBefore(table, caption);

    /* ---------- filtering ---------- */
    var state = { area: 'all', q: '' };
    function apply() {
      var shown = 0;
      bodyRows.forEach(function (tr) {
        var hit = (state.area === 'all' || tr.dataset.domain === state.area) &&
                  (!state.q || tr.dataset.haystack.indexOf(state.q) !== -1);
        tr.hidden = !hit;
        if (hit) shown += 1;
      });
      count.textContent = shown + ' of ' + bodyRows.length + ' capabilities';
      emptyNote.hidden = shown !== 0;
    }
    select.addEventListener('change', function () { state.area = select.value; apply(); });
    search.addEventListener('input', function () { state.q = search.value.trim().toLowerCase(); apply(); });
    apply();
  }

  /* ============================================================
     3. WIRE PHASE
     ============================================================ */
  function start() {
    var outline = window.COURSE_OUTLINE;
    var hasRail = !!(outline && outline.sections && outline.sections.length);
    if (hasRail) {
      mountRail(outline);
      // The stored preference only applies where the rail is part of the layout.
      document.body.dataset.rail = isWide() ? (get(STORE.rail) || 'on') : 'off';
    }
    mountTopbar(hasRail);
    mountStageFlag();
    wireQuizzes();
    wireCopyButtons();
    wireMatrix();
    whenFontsReady(renderMermaid);
    syncSettings();
    settleDiagrams();     // code blocks and formulas are ready before Mermaid is

    // Web fonts settle after DOMContentLoaded and can change what overflows, and
    // so does every column resize.
    window.addEventListener('load', settleDiagrams);
    var settleTimer = null;
    window.addEventListener('resize', function () {
      clearTimeout(settleTimer);
      settleTimer = setTimeout(settleDiagrams, 150);
    });

    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
        if (!root.getAttribute('data-mode')) renderMermaid();
      });
    }

    window.addEventListener('beforeprint', toPaper);
    window.addEventListener('afterprint', offPaper);
    if (window.matchMedia) {
      // Safari fires no print events; the print media query change is what it has.
      var paper = window.matchMedia('print');
      if (paper.addEventListener) {
        paper.addEventListener('change', function (event) {
          if (event.matches) toPaper(); else offPaper();
        });
      }
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
