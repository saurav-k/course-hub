/* ============================================================
   LLM Papers Course - shared runtime
   - Mermaid init (theme-aware)
   - Quiz widget (data-answer index; immediate feedback)
   - Code copy buttons
   - Light/dark toggle (persisted)
   Loaded by every lesson + index.
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
    window.mermaid.initialize({
      startOnLoad: true,
      theme: currentDark() ? 'dark' : 'neutral',
      themeVariables: {
        fontFamily: 'Inter, system-ui, sans-serif',
        fontSize: '15px',
        primaryColor: currentDark() ? '#1e1c14' : '#fbf9f2',
        primaryTextColor: currentDark() ? '#e8e4d8' : '#1a1a1a',
        primaryBorderColor: currentDark() ? '#4fb0b6' : '#1c6b70',
        lineColor: currentDark() ? '#938d80' : '#6b6b63',
        secondaryColor: currentDark() ? '#2a2110' : '#f5f2ea',
        tertiaryColor: currentDark() ? '#1b1913' : '#f4f1e8',
        edgeLabelBackground: currentDark() ? '#1e1c14' : '#fbf9f2'
      },
      flowchart: { curve: 'basis', htmlLabels: true, padding: 12, useMaxWidth: false },
      sequence: { useMaxWidth: false, wrap: true },
      state: { useMaxWidth: false },
      class: { useMaxWidth: false },
      er: { useMaxWidth: false }
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
