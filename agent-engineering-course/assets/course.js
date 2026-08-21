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
        tertiaryColor: currentDark() ? '#1b1913' : '#f4f1e8'
      },
      flowchart: { curve: 'basis', htmlLabels: true, padding: 12 },
      sequence: { useMaxWidth: true, wrap: true }
    });
  }
  initMermaid();

  // ---- quiz ----
  // Markup:
  // <div class="q" data-answer="2">
  //   <div class="q-stem">Question?</div>
  //   <button class="q-opt">A</button> ... <button class="q-opt">D</button>
  //   <div class="q-fb">Explanation shown after answering.</div>
  // </div>
  document.querySelectorAll('.q').forEach(function (q) {
    var ans = parseInt(q.getAttribute('data-answer'), 10);
    var opts = q.querySelectorAll('.q-opt');
    var fb = q.querySelector('.q-fb');
    opts.forEach(function (opt, i) {
      opt.addEventListener('click', function () {
        if (q.dataset.done) return;
        q.dataset.done = '1';
        opts.forEach(function (o, j) {
          if (j === ans) o.classList.add('correct');
          else if (j === i) o.classList.add('wrong');
          o.disabled = true;
        });
        if (fb) fb.classList.add('show');
      });
    });
  });

  // ---- copy buttons ----
  document.querySelectorAll('pre').forEach(function (pre) {
    var btn = document.createElement('button');
    btn.className = 'copy-btn'; btn.textContent = 'copy';
    btn.addEventListener('click', function () {
      var code = pre.querySelector('code');
      navigator.clipboard.writeText(code ? code.innerText : pre.innerText);
      btn.textContent = 'copied'; setTimeout(function(){ btn.textContent = 'copy'; }, 1200);
    });
    pre.appendChild(btn);
  });
})();
