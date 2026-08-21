/* ============================================================
   Statistical Foundations of Machine Learning - shared runtime
   Started from the AI System Design Course runtime; the Mermaid
   palette is retuned to this course's indigo/teal accent pair.

   - Mermaid init (theme-aware)
   - Quiz widget (data-answer index; immediate feedback)
   - Code copy buttons
   - Light/dark toggle (persisted, shared with the rest of the hub)

   Loaded by every lesson, every reference page, and the course map.

   Quiz markup, verbatim - copy this shape, do not invent another:

     <div class="q" data-answer="2">
       <div class="q-stem">Question?</div>
       <button class="q-opt">Option zero</button>
       <button class="q-opt">Option one</button>
       <button class="q-opt">Option two</button>
       <button class="q-opt">Option three</button>
       <div class="q-fb">Why each wrong option is wrong.</div>
     </div>

   data-answer is a ZERO-BASED index into the .q-opt buttons.
   Every option must match in word count and sit as close as
   possible in character count, or the layout leaks the answer.

   Mermaid markup, verbatim:

     <figure class="diagram"><div class="mermaid">
     flowchart LR
       A["Data"] --> B["Model"]
     </div><figcaption>Plain English, with <b>the takeaway in bold</b>.</figcaption></figure>

   Hand-authored SVG charts use <svg class="chart" viewBox="..."> and
   take their colours from the semantic classes in course.css. Never
   hard-code a hex value in an SVG: it will vanish in one theme.
   ============================================================ */
(function () {
  // ---- theme ----
  var saved = localStorage.getItem('llmcourse-theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
  function currentDark() {
    var t = document.documentElement.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  window.toggleTheme = function () {
    var next = currentDark() ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('llmcourse-theme', next);
    location.reload(); // re-render mermaid in new theme
  };

  // ---- mermaid ----
  function initMermaid() {
    if (!window.mermaid) return;
    var dark = currentDark();

    // Mindmap and timeline pick their branch colours from the cScale ramp,
    // and Mermaid's stock ramp is a set of pinks and magentas that fight this
    // course's indigo and teal. Override the first eight steps so a branch is
    // tinted from the course palette, and pin the matching label colour so the
    // text stays legible on the tint in both themes.
    // The first rendered branch reads cScale1, not cScale0, so teal is repeated
    // at both ends of the ramp to keep "statistics is teal" on the first branch.
    var scale = dark
      ? ['#123c3e', '#123c3e', '#241f42', '#1b3524', '#3c2517', '#2f2a12', '#152c3c', '#31203a']
      : ['#dceeef', '#dceeef', '#e6e3f8', '#e1f2e6', '#fbe6da', '#f7f0d8', '#dfeaf5', '#efe4f5'];
    var scaleLabel = dark
      ? '#e8e4d8'
      : '#1a1a1a';
    var vars = {
      fontFamily: 'Inter, system-ui, sans-serif',
      fontSize: '15px',
      primaryColor: dark ? '#1e1c14' : '#fbf9f2',
      primaryTextColor: dark ? '#e8e4d8' : '#1a1a1a',
      primaryBorderColor: dark ? '#4fb0b6' : '#0f6e73',
      lineColor: dark ? '#938d80' : '#6b6b63',
      secondaryColor: dark ? '#221d3a' : '#eeecfa',
      tertiaryColor: dark ? '#1b1913' : '#f4f1e8',
      edgeLabelBackground: dark ? '#1e1c14' : '#fbf9f2'
    };
    scale.forEach(function (colour, i) {
      vars['cScale' + i] = colour;
      vars['cScaleLabel' + i] = scaleLabel;
      vars['cScaleInv' + i] = scaleLabel;
    });

    window.mermaid.initialize({
      startOnLoad: true,
      theme: dark ? 'dark' : 'neutral',
      themeVariables: vars,
      flowchart: { curve: 'basis', htmlLabels: true, padding: 12, useMaxWidth: false },
      sequence: { useMaxWidth: false, wrap: true },
      state: { useMaxWidth: false },
      class: { useMaxWidth: false },
      er: { useMaxWidth: false },
      mindmap: { useMaxWidth: false },
      timeline: { useMaxWidth: false },
      quadrantChart: { useMaxWidth: false }
    });
  }
  initMermaid();

  // ---- diagrams: accessible name and keyboard reach ----
  // Mermaid returns an SVG with no accessible name, so a screen reader announces
  // "flowchart" and nothing else. The figcaption below each figure already says in
  // prose what the figure means, so it becomes the name.
  // A figure wider than the text column scrolls inside its own box. Until that box
  // can take focus, a reader with no mouse never reaches the part that is off-screen.
  function nameDiagrams() {
    document.querySelectorAll('figure .mermaid svg').forEach(function (svg) {
      if (svg.getAttribute('aria-label')) return;
      var figure = svg.closest('figure');
      var caption = figure && figure.querySelector('figcaption');
      if (!caption) return;
      svg.setAttribute('aria-label', caption.textContent.replace(/\s+/g, ' ').trim());
    });
  }

  function markScrollables() {
    document.querySelectorAll('.diagram, pre, .math').forEach(function (box) {
      if (box.scrollWidth > box.clientWidth + 1) box.setAttribute('tabindex', '0');
      else if (box.getAttribute('tabindex') === '0') box.removeAttribute('tabindex');
    });
  }

  function allDiagramsRendered() {
    var pending = 0;
    document.querySelectorAll('.mermaid').forEach(function (m) {
      if (!m.querySelector('svg')) pending++;
    });
    return pending === 0;
  }

  // Mermaid draws asynchronously and offers no completion hook when it starts on
  // load, so repeat the pass until every diagram has an SVG, once more when web
  // fonts have settled, and again whenever the column width changes.
  var diagramTries = 0;
  (function untilDiagramsSettle() {
    nameDiagrams();
    markScrollables();
    if (allDiagramsRendered() || ++diagramTries > 40) return;
    setTimeout(untilDiagramsSettle, 150);
  })();
  window.addEventListener('load', function () { nameDiagrams(); markScrollables(); });
  var resizeTimer = null;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(markScrollables, 150);
  });

  // ---- theme button ----
  // The visible label stays the accessible name, so pressing state is the only
  // thing missing for a reader who cannot see which way the toggle is set.
  document.querySelectorAll('.theme-btn').forEach(function (btn) {
    btn.type = 'button';
    btn.setAttribute('aria-pressed', currentDark() ? 'true' : 'false');
  });

  // ---- quiz ----
  // Markup:
  // <div class="q" data-answer="2">
  //   <div class="q-stem">Question?</div>
  //   <button class="q-opt">A</button> ... <button class="q-opt">D</button>
  //   <div class="q-fb">Explanation shown after answering.</div>
  // </div>
  // Answering used to be reported by colour alone, and disabling the button the
  // reader had just pressed threw focus back to <body>. Mark the outcome with a
  // glyph and a spoken phrase, and keep every option where the keyboard left it.
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

  document.querySelectorAll('.q').forEach(function (q) {
    var ans = parseInt(q.getAttribute('data-answer'), 10);
    var opts = q.querySelectorAll('.q-opt');
    var fb = q.querySelector('.q-fb');
    // The feedback has to be a live region before it is revealed, or a screen
    // reader never learns that answering changed anything on the page.
    if (fb) fb.setAttribute('aria-live', 'polite');
    opts.forEach(function (opt, i) {
      opt.type = 'button';
      opt.addEventListener('click', function () {
        if (q.dataset.done) return;
        q.dataset.done = '1';
        opts.forEach(function (o, j) {
          if (j === ans) { o.classList.add('correct'); markOption(o, '\u2713', 'Correct answer'); }
          else if (j === i) { o.classList.add('wrong'); markOption(o, '\u2717', 'Your answer, incorrect'); }
          o.setAttribute('aria-disabled', 'true');
        });
        if (fb) fb.classList.add('show');
      });
    });
  });

  // ---- copy buttons ----
  document.querySelectorAll('pre').forEach(function (pre) {
    var btn = document.createElement('button');
    btn.className = 'copy-btn'; btn.type = 'button'; btn.textContent = 'copy';
    btn.addEventListener('click', function () {
      var code = pre.querySelector('code');
      navigator.clipboard.writeText(code ? code.innerText : pre.innerText);
      btn.textContent = 'copied'; setTimeout(function(){ btn.textContent = 'copy'; }, 1200);
    });
    pre.appendChild(btn);
  });
})();
