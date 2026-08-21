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
      tertiaryColor: dark ? '#1b1913' : '#f4f1e8'
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
