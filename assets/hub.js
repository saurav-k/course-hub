/* ============================================================
   Course Hub - the one shared runtime.

   Loaded from <head> without defer, so the persisted mode and palette
   are on <html> before the first paint and no page ever flashes the
   wrong colours.

   What it does, in order:
     1. head phase   - restore mode + palette from localStorage
     2. mount phase  - build the rail from window.COURSE_OUTLINE,
                       build the topbar controls and settings popover
     3. wire phase   - quiz, copy buttons, reading progress, Mermaid

   Every page links this one file. There is no per-course runtime.
   ============================================================ */
(function () {
  'use strict';

  var STORE = {
    mode:    'coursehub.mode',      // "light" | "dark" | "" (follow the system)
    palette: 'coursehub.palette',   // a palette key
    rail:    'coursehub.rail',      // "on" | "off"
    read:    'coursehub.read',      // { courseKey: [lesson file names] }
    legacy:  'llmcourse-theme'      // what the first design system wrote
  };

  var PALETTES = [
    { key: 'paper',     label: 'Paper',     note: 'Warm cream, rust links, deep teal. The house identity.' },
    { key: 'slate',     label: 'Slate',     note: 'Cool neutral greys with an indigo accent.' },
    { key: 'ink',       label: 'Ink',       note: 'Near-monochrome, maximum contrast.' },
    { key: 'sage',      label: 'Sage',      note: 'Soft green paper, pine accent, low glare.' },
    { key: 'harbor',    label: 'Harbor',    note: 'Blue-grey daylight with deep teal and coral.' },
    { key: 'aubergine', label: 'Aubergine', note: 'Violet-grey with plum and old gold.' }
  ];
  var PALETTE_KEYS = PALETTES.map(function (p) { return p.key; });

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

  /* ============================================================
     MERMAID - themed from the live tokens, re-rendered in place
     ============================================================ */
  function mermaidVars() {
    return {
      fontFamily: getComputedStyle(root).getPropertyValue('--sans').trim() || 'sans-serif',
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

  function renderMermaid() {
    if (!window.mermaid) return;
    var nodes = document.querySelectorAll('.mermaid');
    if (!nodes.length) return;
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
        node.textContent = node.dataset.mmd;
      }
      node.removeAttribute('data-processed');
    });
    var release = function () {
      Array.prototype.forEach.call(nodes, function (node) { node.style.minHeight = ''; });
      settleDiagrams();   // the SVGs exist only now, and their width is final
    };
    window.mermaid.initialize({
      startOnLoad: false,
      theme: isDark() ? 'dark' : 'neutral',
      themeVariables: mermaidVars(),
      flowchart: { curve: 'basis', htmlLabels: true, padding: 12, useMaxWidth: false },
      sequence: { useMaxWidth: false, wrap: true },
      state: { useMaxWidth: false }, class: { useMaxWidth: false }, er: { useMaxWidth: false },
      mindmap: { useMaxWidth: false }, timeline: { useMaxWidth: false }
    });
    try {
      var done = window.mermaid.run({ querySelector: '.mermaid' });
      if (done && done.then) done.then(release, release); else release();
    } catch (e) {
      if (window.mermaid.init) window.mermaid.init(undefined, nodes);
      release();
    }
  }

  /* ============================================================
     APPLYING A CHOICE
     One function for both axes: set the attribute, persist it, repaint the
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

    var prefGroup = el('div', 'set-group');
    prefGroup.appendChild(el('h3', null, 'Reading'));
    prefGroup.appendChild(toggleRow('Wider text column', 'coursehub.wide', function (on) {
      root.style.setProperty('--measure', on ? '52rem' : '');
    }));
    prefGroup.appendChild(toggleRow('Larger type', 'coursehub.big', function (on) {
      document.body.style.fontSize = on ? '1.3125rem' : '';
    }));
    var note = el('p', 'set-note',
      'Your choice is remembered in this browser and applies to every course in the hub.');
    prefGroup.appendChild(note);
    panel.appendChild(prefGroup);
    return panel;
  }

  function toggleRow(label, key, apply) {
    var row = el('label', 'set-row');
    var box = el('input');
    box.type = 'checkbox';
    box.checked = get(key) === '1';
    if (box.checked) apply(true);
    box.addEventListener('change', function () {
      set(key, box.checked ? '1' : '0');
      apply(box.checked);
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
    var currentPalette = root.getAttribute('data-palette');
    Array.prototype.forEach.call(settingsEl.querySelectorAll('.pal-card'), function (card) {
      card.setAttribute('aria-pressed', String(card.dataset.palette === currentPalette));
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
     back when the column grows and it no longer does. */
  function markScrollables() {
    Array.prototype.forEach.call(document.querySelectorAll('.diagram, pre, .math'), function (box) {
      if (box.scrollWidth > box.clientWidth + 1) box.setAttribute('tabindex', '0');
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
    wireQuizzes();
    wireCopyButtons();
    renderMermaid();
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
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
