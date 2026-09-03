/* ============================================================
   Course Hub - the one shared runtime.

   Loaded from <head> without defer, so the persisted mode, palette and
   design are on <html> before the first paint and no page ever flashes
   the wrong colours or the wrong form.

   What it does, in order:
     1. head phase   - restore mode, palette, design and the two reading
                       preferences from localStorage
     2. mount phase  - build the rail and the fixed chapter bar from
                       window.COURSE_OUTLINE, build the in-page section rail
                       from the page's own headings, build the topbar controls
                       and settings popover, and the pre-production bar when
                       the host says so
     3. wire phase   - quiz, copy buttons, reading progress, Mermaid

   Every page links this one file. There is no per-course runtime.
   ============================================================ */
(function () {
  'use strict';

  var STORE = {
    mode:    'coursehub.mode',      // "light" | "dark" | "" (follow the system)
    palette: 'coursehub.palette',   // a palette key
    design:  'coursehub.design',    // a design key
    face:    'coursehub.bodyface',  // a reading-face key
    leading: 'coursehub.leading',   // a line-spacing key
    density: 'coursehub.density',   // a density key
    motion:  'coursehub.motion',    // "reduced" | "full" | "" (follow the system)
    panel:   'coursehub.panel',     // where the reader put the appearance panel
    notePanel: 'coursehub.notepanel', // where the reader put the notes panel
    noteScope: 'coursehub.notescope', // "page" | "course" | "hub"
    markPanel: 'coursehub.markpanel', // where the reader put the highlights panel
    rail:    'coursehub.rail',      // "on" | "off"
    read:    'coursehub.read',      // { courseKey: [lesson file names] }
    legacy:  'llmcourse-theme'      // what the first design system wrote
  };

  /* A reader's note is not a preference, and it does not live in STORE. It
     lives under `coursehub.note:` plus the tier and the identifier, one key per
     document, so nothing has to read or rewrite a map of every note in order to
     save one. See "THE STUDY NOTES PANEL" below for the key and why it is that
     one. */
  var NOTE_PREFIX = 'coursehub.note:';

  /* A page's highlights are not a preference either, and they live beside the
     notes rather than inventing a second scheme: `coursehub.mark:` plus the
     tier and the same course-key-and-file-name identifier `pageKey` derives.
     One key per page holding one array, because a page's marks are one
     document. See "THE TEXT HIGHLIGHTER" below. */
  var MARK_PREFIX = 'coursehub.mark:';

  /* ============================================================
     THE SIX READER CONTROLS

     Eleven reading axes were assessed and six earn a control: a control is
     worth its place when readers genuinely differ on it, the reader can
     perceive the difference and judge it, and a wrong setting is recoverable.
     Ground, body size, reading face, measure, line spacing and density pass.
     The display face, the mono face and the eyebrow treatment fail all three in
     the same way - a reader sets them once out of curiosity and never returns -
     and they are author tokens on the course contract instead. The accent is
     not a seventh control: it is carried by the palette and rotated per course,
     and a colour picker would put a contrast criterion in the reader's hands.

     Every registry below is DATA. Nothing in this file branches on a known key,
     so registering a face, a spacing step or a density adds an entry and no
     framework code, and the source of these lists can move without the code
     that consumes them changing. The same discipline the design registry
     already carries.

     Two shapes, and the difference is not cosmetic.

     A value that composes on its own is a `--*-user` custom property written
     inline on <html>, which is the only thing a reader may write; hub.css
     resolves the token every rule reads from it. Until 2026-08 the two
     preferences that existed were applied as an inline `--measure` and an
     inline `font-size` on <body>, which beat every stylesheet rule that was not
     !important and pinned a reader who had turned them on. Never write a
     resolved token from here.

     A value that cannot compose is a registered axis attribute. The reading
     face is one, because three measured constants - the prose advance, the
     x-height and the apparent-size factor - have to travel with the family and
     one property cannot carry them; motion is another, because what it selects
     is a block of rules rather than a value.
     ============================================================ */

  /* ---------- 3. the reading face ----------
     The strongest evidence behind any control here. Wallace et al. 2022, 352
     readers: a 35% per-individual spread in reading speed across faces at
     matched perceived size, three quarters of them showing a large effect, and
     a reader's preferred face is not their fastest one. The framework cannot
     pick for the reader and cannot claim the reader will pick right by feel
     either, so the honest response is to offer the control.

     A key here has a `:root[data-body-face="key"]` entry in hub.css declaring
     the family and its three constants together. The first entry is the
     registered default and is what a page with no attribute renders. */
  var FACES = [
    { key: 'serif', label: 'Serif', note: 'Source Serif 4. The hub as it reads today.' },
    { key: 'sans',  label: 'Sans',  note: 'Inter. A larger x-height at the same apparent size.' }
  ];

  /* ---------- 5. line spacing ----------
     Three steps and not a slider, because the range that matters is narrow and
     there is no modern screen evidence distinguishing points inside it; a
     continuous control would imply a precision the literature does not have.
     It reaches 1.5 because that is the figure both relevant success criteria
     name.

     Normal writes nothing. That is the whole of the difference between it and
     the other two: hub.css nudges the leading up above a wide measure, and an
     explicit reader value suppresses that nudge, so a reader on Normal keeps
     the design's leading with the nudge and a reader who has stated a number
     gets exactly that number. Reset therefore lands on Normal by removing a
     property rather than by writing one. */
  var LEADINGS = [
    { key: 'tight',  label: 'Tight',  value: '1.5' },
    { key: 'normal', label: 'Normal', value: null },
    { key: 'loose',  label: 'Loose',  value: '1.9' }
  ];
  var LEADING_DEFAULT = 'normal';

  /* ---------- 6. density ----------
     Density scales the reading column's vertical rhythm and reaches nothing
     else. That is a hard limit rather than a preference: one control in the
     chrome already fails WCAG 2.2 SC 2.5.8, seven more pass only on the spacing
     exception, and the smallest compliant control has two pixels of headroom,
     so a compact chrome turns near-misses into failures.

     The limit is structural and not a promise. Every name in RHYTHM below is
     one of the twenty prose-rhythm roles, the check in validate_site.py refuses
     any `--*-user` write hub.css does not resolve, and hub.css resolves exactly
     the twenty-four tokens a reader control can reach. A density that tried to
     tighten the topbar would have nothing to write to.

     The factor is applied to the stylesheet's own default rather than to a
     literal, so a design that restates a role is scaled rather than overruled. */
  var DENSITIES = [
    { key: 'comfortable', label: 'Comfortable', factor: 1 },
    { key: 'compact',     label: 'Compact',     factor: 0.75 }
  ];
  var DENSITY_DEFAULT = 'comfortable';

  /* The twenty prose-rhythm roles, each named by the `prop` field the check in
     validate_site.py reads, and each carrying what it spaces so the list can be
     compared against hub.css by eye. Six roles, four of them families, because
     the four heading levels do not share a value and reconciling them would be
     a design change. */
  var RHYTHM = [
    { prop: '--sp-para-user',              role: 'p' },
    { prop: '--sp-list-user',              role: 'ul, ol' },
    { prop: '--sp-list-item-user',         role: 'li' },
    { prop: '--sp-heading-before-1-user',  role: 'h1, above' },
    { prop: '--sp-heading-before-2-user',  role: 'h2, above' },
    { prop: '--sp-heading-before-3-user',  role: 'h3, above' },
    { prop: '--sp-heading-before-4-user',  role: 'h4, above' },
    { prop: '--sp-heading-after-1-user',   role: 'h1, below' },
    { prop: '--sp-heading-after-2-user',   role: 'h2, below' },
    { prop: '--sp-heading-after-3-user',   role: 'h3, below' },
    { prop: '--sp-heading-after-4-user',   role: 'h4, below' },
    { prop: '--sp-block-user',             role: '.card, table' },
    { prop: '--sp-block-note-user',        role: '.callout, .lab' },
    { prop: '--sp-block-code-user',        role: 'pre, .worked, .metric-grid' },
    { prop: '--sp-block-panel-user',       role: '.quiz, .practice, .cmatrix' },
    { prop: '--sp-block-aside-user',       role: '.teacher-note' },
    { prop: '--sp-block-inline-user',      role: '.math, .q' },
    { prop: '--sp-block-term-user',        role: '.term' },
    { prop: '--sp-figure-user',            role: 'figure, above' },
    { prop: '--sp-figure-after-user',      role: 'figure, below' }
  ];

  /* ---------- motion, which is a need rather than a taste ----------
     Present because it must be, and defaulting to the operating system because
     a reader who has already said this once should not have to say it again. */
  var MOTIONS = [
    { key: '',         label: 'System' },
    { key: 'reduced',  label: 'Reduced' },
    { key: 'full',     label: 'Full' }
  ];

  /* ---------- 2 and 4. the two ranges ----------
     Both are honest units. The body size is apparent px on the Source Serif 4
     reference scale, so "19" means the same apparent size whichever face is
     selected; the measure is real characters, because a `ch` is the advance of
     the digit zero and means a different character count for every face. Both
     are inputs to a derivation in hub.css and neither writes the width or the
     px size it implies: those are outputs.

     `token` is what the slider reads to find where it already is, and reading
     it rather than repeating a number here is what keeps the control honest.
     The default body size is not one number - the 720px block sets a smaller
     one, and a design may set another - so a hard-coded start would tell a
     reader on a phone they are at 19 while the page renders 17. */
  var RANGES = [
    {
      name:  'bodysize',
      store: 'coursehub.bodysize',
      prop:  '--fs-body-user',
      token: '--fs-body-ref',
      label: 'Text size',
      legend: function (value) { return value + 'px'; },
      min: 16, max: 28, step: 1,
      // The stylesheet states this size in rem and the reader's number is on
      // the same scale, so the write stays in rem: a reader who has raised the
      // browser's own default text size keeps it, which a px value would
      // silently take away from them.
      read:  function (raw) { return raw * 16; },
      write: function (value) { return (value / 16) + 'rem'; }
    },
    {
      name:  'measure',
      store: 'coursehub.measure',
      prop:  '--measure-chars-user',
      token: '--measure-chars',
      label: 'Line width',
      legend: function (value) { return value + ' characters'; },
      min: 55, max: 85, step: 5,
      read:  function (raw) { return raw; },
      write: function (value) { return String(value); }
    }
  ];

  var PALETTES = [
    { key: 'paper',     label: 'Paper',     note: 'Warm cream, rust links, deep teal. The house identity.' },
    { key: 'slate',     label: 'Slate',     note: 'Cool neutral greys with an indigo accent.' },
    { key: 'ink',       label: 'Ink',       note: 'Near-monochrome, maximum contrast.' },
    { key: 'sage',      label: 'Sage',      note: 'Soft green paper, pine accent, low glare.' },
    { key: 'harbor',    label: 'Harbor',    note: 'Blue-grey daylight with deep teal and coral.' },
    { key: 'aubergine', label: 'Aubergine', note: 'Violet-grey with plum and old gold.' },
    { key: 'press',     label: 'Press',     note: 'Unbleached paper, one rust in two steps, a dark code plate.' }
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

     Two designs are registered. `house` is what every reader had before the
     axis existed and is the fallback below; `press` is the form half of the
     reference look, whose colour half is the `press` palette above. The two
     halves are on two axes on purpose, so either can be worn without the
     other and neither multiplies the other's checks.

     This array is data and nothing in the framework branches on what is in it.
     Registering a design is one entry here plus one token block in hub.css;
     no function in this file, and no rule in that one, knows a design by name.

     Withdrawing a design is one line and needs no deploy: delete its entry.
     The picker stops offering it, and a reader who had chosen it falls through
     to the default below, which was measured to restore the original exactly.
     The default is the first entry rather than a literal, so withdrawing the
     default is the same one-line edit as withdrawing any other. */
  var DESIGNS = [
    { key: 'house', label: 'House', note: 'Serif prose, sans headings and chrome. The hub as it reads today.' },
    { key: 'press', label: 'Press', note: 'Serif display set tight, mono eyebrows, a 68-character column.' }
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

  /* ---------- storage that says whether it worked ----------
     The three helpers above swallow, which is right for a preference: a lost
     palette costs the reader one click and telling them about it would be
     noise. It is exactly wrong for a document the reader wrote. The reference
     site swallows in the same shape and then paints `Saved` from the caller,
     so a reader whose quota is full is told their work is safe on every
     keystroke and loses all of it on the next reload.

     So the notes panel writes through these two instead, and paints what they
     return rather than what it hoped. The read-back is not belt and braces: a
     `setItem` that raises is the loud failure and easy to catch, and a store
     that accepts the call and keeps nothing is the quiet one - which is what a
     private window and some extensions do - so the only honest answer is to
     ask the store what it now holds. */

  /* Why the last checked write did not take, so the sentence a panel shows is a
     diagnosis rather than a guess. A second probe cannot answer it: a store
     full to the last byte refuses the probe as well, and the reader is then
     told the browser is storing nothing when it is storing five megabytes of
     theirs. Measured, not reasoned - filling a store to refusal and then
     highlighting reported the wrong one of the two failures until this existed.

     Three outcomes and the middle one is the quiet failure the read-back is
     here for: the call was accepted, nothing raised, and the store kept
     nothing. */
  var writeRefusal = '';

  function isQuota(error) {
    return !!error && (error.name === 'QuotaExceededError'
      || error.name === 'NS_ERROR_DOM_QUOTA_REACHED'
      || error.code === 22 || error.code === 1014);
  }

  function setChecked(key, value) {
    writeRefusal = '';
    try {
      localStorage.setItem(key, value);
      if (localStorage.getItem(key) === value) return true;
      writeRefusal = 'kept nothing';
      return false;
    } catch (e) {
      writeRefusal = isQuota(e) ? 'full' : 'refused';
      return false;
    }
  }
  function dropChecked(key) {
    writeRefusal = '';
    try {
      localStorage.removeItem(key);
      if (localStorage.getItem(key) === null) return true;
      writeRefusal = 'kept nothing';
      return false;
    } catch (e) {
      writeRefusal = isQuota(e) ? 'full' : 'refused';
      return false;
    }
  }

  /* Whether this browser will keep anything here at all, asked with one byte.
     Chrome gives every file:// page its own opaque origin and every call
     raises; a reader with site data blocked is in the same position. Asking
     before the reader has written anything is what lets the panel say so on
     open, rather than after a page of typing. A byte also distinguishes the
     two failures the panel has to name apart: a store that refuses one byte is
     switched off, and a store that takes one byte and refuses the document is
     full. */
  function storageAccepts() {
    var probe = NOTE_PREFIX + 'probe';
    writeRefusal = '';
    try {
      localStorage.setItem(probe, '1');
      localStorage.removeItem(probe);
      return true;
    } catch (e) { writeRefusal = isQuota(e) ? 'full' : 'refused'; return false; }
  }

  /* ---------- the save state, which two panels now paint ----------
     A panel that holds something the reader wrote says what actually happened
     to it, and both of the panels that do say it in one shape. This is that
     shape: a `role="status"` line whose text is written only when it changed -
     the role speaks every write, and a reader on a screen reader does not need
     "Saved" announced at every pause - and the escape hatch beside it filled in
     `--warn` the moment a write fails, so nobody has to read a fourth sentence
     to find out what to do about it.

     It is a factory rather than a function because the "only when it changed"
     is per element: two panels sharing one `spoken` would silence each other. */
  function saveState(node, escape) {
    var spoken = '';
    return function (kind, text) {
      node.dataset.state = kind;
      if (text !== spoken) { node.textContent = text; spoken = text; }
      if (escape) escape.dataset.urgent = kind === 'failed' ? 'yes' : 'no';
    };
  }

  /* The two failures a store has, told apart by what the write itself raised
     rather than by a second probe. A store that refuses on quota is full; a
     store that refuses for any other reason, or that accepts the call and keeps
     nothing, is storing nothing here. Naming them apart is what makes the
     sentence actionable rather than an apology. */
  function saveFailure(what) {
    var reason = writeRefusal === 'full'
      ? 'browser storage is full'
      : 'this browser is storing nothing here';
    /* The way out is named only when there is something to take out of it.
       Telling a reader with nothing highlighted to export is an instruction
       with no object. */
    return 'Not saved: ' + reason + '.' + (what ? ' Export to keep ' + what + '.' : '');
  }

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

  /* The registered default is the first entry rather than a literal, as the
     design registry's already is, so withdrawing the default palette is the
     same one-line edit as withdrawing any other and no code names a palette.
     The panel's reset reads the same first entry, so the two can never
     disagree about what "the default" means. */
  var palette = get(STORE.palette);
  if (PALETTE_KEYS.indexOf(palette) === -1) palette = PALETTES[0].key;
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

  /* ---------- a registered choice ----------
     The reader's stored value if the registry still knows it, and the
     registry's own default if it does not. That guard is what makes a
     withdrawal survivable: a reader who chose a step that was later taken out
     lands on the default rather than on a page nobody else can see and nobody
     else can reproduce. Storage that raises returns null through `get`, which
     is not a registered key either, so a reader with storage blocked gets the
     same default and the same correct page.

     The default is named rather than taken from the first entry, because two of
     these registries are ordered for the eye - tight before normal before loose
     - and the step a reader lands on is not the one that happens to come
     first. */
  function registered(list, stored, fallback) {
    for (var i = 0; i < list.length; i += 1) {
      if (list[i].key === stored) return stored;
    }
    return fallback;
  }

  function entry(list, key) {
    for (var i = 0; i < list.length; i += 1) {
      if (list[i].key === key) return list[i];
    }
    return list[0];
  }

  /* ---------- the reading preferences, restored before the first paint ----------
     Here rather than when the appearance panel is built, so a reader who has
     set a face, a size, a column or a spacing gets it with the first paint
     instead of a step after it. */

  /* The two ranges. A stored value is a number on the control's own grid or it
     is nothing: anything else - a step that was withdrawn, a value from a range
     that has since narrowed, a hand-edited key - falls back to writing no
     property at all, which is exactly the stylesheet's own default.

     The two step names this used to store are migrated once and dropped, as the
     first design system's single theme key already is above. `big` reproduced
     1.3125rem, which is 21 on this scale and lands exactly. `wide` reproduced
     52rem, which is 97.8 characters at the house body size and does not land at
     all: it is past the 85 this framework calls a safe measure, so it migrates
     to 85 and that reader's column narrows slightly. The alternative was to
     keep a value the panel itself will not offer, which is the shape of a
     preference a reader can no longer find. */
  var LEGACY_STEPS = { measure: { wide: 85 }, bodysize: { big: 21 } };

  /* Two questions, deliberately not one function. `snap` asks where on the
     control's grid a number lands and always answers; `onGrid` asks whether a
     stored value is one this control could have written and answers null when
     it is not, which is what makes an unknown stored value fall back to the
     stylesheet's own default rather than to the nearest thing it could reach. */
  function snap(axis, value) {
    var stepped = Math.round((value - axis.min) / axis.step) * axis.step + axis.min;
    return Math.min(Math.max(stepped, axis.min), axis.max);
  }

  function onGrid(axis, value) {
    if (!isFinite(value) || value < axis.min || value > axis.max) return null;
    return snap(axis, value);
  }

  function readRange(axis) {
    var stored = get(axis.store);
    if (stored !== null && Object.prototype.hasOwnProperty.call(LEGACY_STEPS[axis.name], stored)) {
      stored = String(LEGACY_STEPS[axis.name][stored]);
      set(axis.store, stored);
    }
    return stored === null ? null : onGrid(axis, parseFloat(stored));
  }

  function applyRange(axis, value) {
    if (value === null) root.style.removeProperty(axis.prop);
    else root.style.setProperty(axis.prop, axis.write(value));
  }

  var reading = {};
  RANGES.forEach(function (axis) {
    reading[axis.name] = readRange(axis);
    applyRange(axis, reading[axis.name]);
  });

  /* The reading face. An attribute rather than a property, because three
     measured constants travel with the family; see the registry above. */
  var face = registered(FACES, get(STORE.face), FACES[0].key);
  if (face !== FACES[0].key) root.setAttribute('data-body-face', face);

  /* Line spacing, and the one step that writes nothing. */
  var leading = registered(LEADINGS, get(STORE.leading), LEADING_DEFAULT);
  function applyLeadingValue(value) {
    if (value) root.style.setProperty('--lh-body-user', value);
    else root.style.removeProperty('--lh-body-user');
  }
  applyLeadingValue(entry(LEADINGS, leading).value);

  /* Density, written onto the twenty prose-rhythm roles and nothing else. The
     factor multiplies each role's own `-default`, so a design that restates one
     is scaled rather than overruled, and a factor of 1 writes nothing so the
     comfortable page is byte-for-byte the page that had no control at all. */
  var density = registered(DENSITIES, get(STORE.density), DENSITY_DEFAULT);
  function applyDensityFactor(factor) {
    RHYTHM.forEach(function (role) {
      if (factor === 1) root.style.removeProperty(role.prop);
      else root.style.setProperty(role.prop, 'calc(var(' + role.prop.replace('-user', '-default') + ') * ' + factor + ')');
    });
  }
  /* Only when there is something to write. The head phase has written nothing
     yet, so a factor of 1 here would be twenty removeProperty calls against an
     inline style that is empty - twenty writes to <html> on every one of 796
     page loads, for every reader, to reach the state the page was already in.
     The panel's own path still removes, because by then something may be there. */
  var densityFactor = entry(DENSITIES, density).factor;
  if (densityFactor !== 1) applyDensityFactor(densityFactor);

  /* Motion. Absent means follow the operating system, which is the state every
     page was in before this control existed. */
  var motion = registered(MOTIONS, get(STORE.motion), '');
  if (motion) root.setAttribute('data-motion', motion);

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

  /* The printed sheet's identity, for the running foot `hub.css` sets in the
     `@page` margin. A margin box can reach nothing about the document except a
     custom property on the root element: `string()`, the standard way to run a
     heading into one, renders on the first page only in Chrome, which is the
     one sheet that never needed it. So the title becomes a CSS string here.

     `hub.css` declares a fallback, so a page with the script removed still
     prints a foot; this beats it because an inline property beats a rule. The
     stage is folded in on pre-production, which is what lets the print block
     drop the warning strip altogether rather than flowing it to the last page:
     every sheet now says where it came from instead of one of them.

     A CSS string, not a bare word - a backslash or a quotation mark in a
     lesson title would otherwise end the string early and take the whole
     declaration with it, and the foot would print empty with nothing said. */
  function cssString(text) {
    return '"' + String(text).replace(/\s+/g, ' ').trim().replace(/[\\"]/g, '\\$&') + '"';
  }
  var printId = document.title || 'Course Hub';
  if (root.getAttribute('data-env') === 'preprod') printId = 'PRE-PRODUCTION - ' + printId;
  root.style.setProperty('--print-id', cssString(printId));

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
    openFigures();
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
    closeFigures();
    if (!onPaper) return;
    onPaper.forEach(function (svg, node) { node.innerHTML = svg; });
    onPaper = null;
  }

  /* ============================================================
     APPLYING A CHOICE
     One function per axis: set the attribute, persist it, repaint the
     diagrams. Nothing here reloads the page.
     ============================================================ */
  /* Every axis repaints through here, and the request is coalesced onto one
     frame. Two reasons, and the second is the one that made it necessary.

     Mermaid cuts each label box to a measurement it takes at render time, so a
     repaint that starts before the new metrics are in place clips the last word
     of the label - the defect `whenFontsReady` was written for, on 380
     published flowcharts - and then looks correct on the next reload. The
     forced reflow first is what puts a newly needed face in flight, so the
     promise waited on is the new one rather than the settled old one. Mode and
     palette cannot move a text measurement and do not need any of that, but one
     path with no exceptions is cheaper to keep right than three.

     And "back to this course's defaults" moves eight axes in one gesture. Eight
     repaints of 2,159 diagram blocks is a button nobody can press; the last one
     is the only one that counts. */
  var repaintQueued = false;
  function repaint() {
    if (repaintQueued) return;
    repaintQueued = true;
    var run = function () {
      repaintQueued = false;
      void root.offsetWidth;
      whenFontsReady(renderMermaid);
    };
    if (window.requestAnimationFrame) window.requestAnimationFrame(run); else setTimeout(run, 0);
  }

  function applyMode(next) {
    if (next) { root.setAttribute('data-mode', next); set(STORE.mode, next); }
    else { root.removeAttribute('data-mode'); set(STORE.mode, ''); }
    repaint();
    syncSettings();
  }
  function applyPalette(next) {
    root.setAttribute('data-palette', next);
    set(STORE.palette, next);
    repaint();
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
    repaint();
    syncSettings();
  }

  /* Switching between the two registered faces costs no fetch. Both are on
     every page already - `--font-body` resolves to one of them and the chrome
     pulls Inter regardless - so the attribute is all this has to write.

     A THIRD face is the case that changes it, and the contract is not this
     function's to invent: `references/widgets.md`, "The faces, and what a page
     pays for them", states it and assigns the code here. A face nobody has
     picked should not be fetched, and a `@font-face` rule cannot say that,
     because the browser decides from the rendered content and for a registered
     face that is always. So the control loads it with the CSS Font Loading API
     and sets the attribute inside the callback - never before it - or the
     reader sees the fallback flash on a control they just used and a measure
     computed from one face while another is on screen. A `FontFace` built in
     script also carries its own `display`, so it is never subject to the
     descriptor on any rule and never silently dropped. */
  function applyFace(next) {
    face = next;
    set(STORE.face, next);
    // The first entry is what a page with no attribute renders, so the default
    // is expressed by removing the attribute rather than by writing it. That is
    // what makes the reset exact and what a page with no script already does.
    if (next === FACES[0].key) root.removeAttribute('data-body-face');
    else root.setAttribute('data-body-face', next);
    repaint();
    syncSettings();
  }

  function applyLeading(next) {
    leading = next;
    set(STORE.leading, next);
    applyLeadingValue(entry(LEADINGS, next).value);
    syncSettings();
  }

  function applyDensity(next) {
    density = next;
    set(STORE.density, next);
    applyDensityFactor(entry(DENSITIES, next).factor);
    repaint();
    syncSettings();
  }

  function applyMotion(next) {
    motion = next;
    set(STORE.motion, next);
    if (next) root.setAttribute('data-motion', next);
    else root.removeAttribute('data-motion');
    syncSettings();
  }

  /* A range moves twice on the way to a value. `input` fires on every step of a
     drag and writes the property, so the effect is live and the reader judges
     it rather than imagining it; `change` fires once when the drag ends and is
     where the diagrams repaint, because repainting 2,159 Mermaid blocks on
     every pixel of a slider is a page nobody can drag. */
  function applyRangeValue(axis, value, settled) {
    reading[axis.name] = value;
    if (value === null) drop(axis.store);
    else set(axis.store, String(value));
    applyRange(axis, value);
    if (settled) repaint();
  }

  /* ============================================================
     2. MOUNT PHASE - the rail, the topbar controls, the appearance panel
     ============================================================ */
  /* The one panel this file builds today, held so the sync pass and the reset
     button can reach it. It is a shell handle rather than an element: what the
     panel is made of belongs to the shell and nothing outside it may reach in. */
  var appearance = null;

  /* The second panel, on the same terms. Two handles rather than one list,
     because nothing in this file loops over panels: each is opened by its own
     button and each answers Escape for itself. */
  var studyNotes = null;

  /* The third, and the one that is not built on every browser: the highlighter
     is drawn with the CSS Custom Highlight API and there is no fallback, so on
     a browser without it this stays null and nothing is added to the topbar,
     the cluster or the page. See "THE TEXT HIGHLIGHTER" below. */
  var highlighter = null;

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

  /* ---------- the fixed chapter bar ----------
     Previous page, where you are, next page, held across the foot of the
     viewport for the whole of a lesson rather than only at its end. It reaches
     every page a course outline names because those pages link this file, and no
     page's markup mentions it. The stylesheet section of the same name carries
     where it sits and why; this is what it says.

     THE ORDER COMES FROM THE OUTLINE, NOT FROM THE PAGER. Two sources of page
     order were available and only one of them is generated: `outline.js` is
     written by `scripts/gen_outline.py` from the course map, `validate_site.py`
     check 3 fails the pull request when it and `lessons/` disagree, and check 7
     holds every title in it against the map and against every pager pointing at
     the page. The committed pager in a page's own markup is the other, and it
     is hand-written per page, which makes it a claim about two neighbours
     rather than a sequence: a bar built from it could not say how far through
     the course the reader is, could not tell a missing neighbour from a first
     page, and would go quietly wrong on exactly the page whose pager was the
     one nobody updated. The routed course is the same source by another route -
     its `outline.js` derives `window.COURSE_OUTLINE` from `routes.js` for the
     route in play, so this bar follows the route the reader is actually on with
     no code here that knows routes exist.

     The sequence is the outline's own reading order: every lesson of every
     section in order, then the reference pages the rail shows under `Reference`.
     A page the outline does not name gets no bar at all - the hub landing page,
     the design system and a course map have no place in that sequence, and a
     bar that could not say where you are would be answering two thirds of the
     question. */
  function chapterSequence(outline) {
    var pages = [];
    outline.sections.forEach(function (section) {
      section.lessons.forEach(function (lesson) { pages.push(lesson); });
    });
    (outline.extras || []).forEach(function (extra) { pages.push(extra); });
    return pages;
  }

  /* The visible text names the direction and the destination; the accessible
     name states both whatever is drawn. Below 720px the direction word is not
     rendered, and a hidden element is out of the accessibility tree as well as
     off the screen, so a link relying on it would be announced as a bare title
     on a phone. WCAG 2.2 SC 2.5.3 is satisfied at both widths because the
     visible label - the title, with or without the word in front of it - is
     contained in the accessible name. */
  function chapterLink(page, forward, base) {
    var link = el('a', 'chapbar-link ' + (forward ? 'chapbar-next' : 'chapbar-prev'));
    link.href = new URL(page.href, base).href;
    link.setAttribute('aria-label', (forward ? 'Next: ' : 'Previous: ') + page.title);

    var direction = el('span', 'chapbar-dir');
    var arrow = el('span', 'chapbar-arrow', forward ? '\u2192' : '\u2190');
    var word = el('span', 'chapbar-word', forward ? 'Next' : 'Previous');
    if (forward) { direction.appendChild(word); direction.appendChild(arrow); }
    else { direction.appendChild(arrow); direction.appendChild(word); }

    link.appendChild(direction);
    link.appendChild(el('span', 'chapbar-ttl', page.title));
    return link;
  }

  function mountChapterBar(outline) {
    var pages = chapterSequence(outline);
    var here = fileOf(location.pathname);
    var at = -1;
    for (var i = 0; i < pages.length; i += 1) {
      if (fileOf(pages[i].href) === here) { at = i; break; }
    }
    if (at === -1) return;

    var base = courseBase();
    var bar = el('nav', 'chapbar');
    /* A `nav` with a name of its own, because the page already has two: the
       rail is `Course outline` and the committed pager at the foot of the
       document is `Lesson navigation` on a routed course. Three landmarks with
       one name between them is three landmarks a screen-reader user cannot
       choose from. */
    bar.setAttribute('aria-label', 'Previous and next lesson');

    /* The first and the last page omit the control rather than disabling it. A
       disabled control is a promise the page cannot keep: it holds a tab stop,
       it reads as something that would work if the reader tried harder, and
       there is nowhere for it to go. The stylesheet places the two links by
       grid column, so the survivor stays on its own side of the bar. */
    if (at > 0) bar.appendChild(chapterLink(pages[at - 1], false, base));

    var where = el('span', 'chapbar-here');
    /* `of` rather than a slash: a screen reader says "3 of 68" and reads
       "3 / 68" as "3 slash 68". It is a position and not a progress reading -
       the rail already owns how much of a course has been read, and a second
       answer to that question in the same viewport would be two. */
    where.appendChild(el('span', 'chapbar-count', (at + 1) + ' of ' + pages.length));
    where.appendChild(el('span', 'chapbar-ttl', pages[at].title));
    bar.appendChild(where);

    if (at < pages.length - 1) bar.appendChild(chapterLink(pages[at + 1], true, base));

    /* Inserted straight after the topbar rather than appended to the body, for
       the reason the floating cluster gives above: a reader on a keyboard
       reaches it in the same breath as the rest of the chrome instead of after
       every paragraph, figure and footer link on the page. It goes in ahead of
       the cluster, which `start` has already inserted there, because a way on
       to the next page is wanted more often than a way into the settings.

       The attribute is what the stylesheet reserves room from, and it is
       written in the same breath as the element goes in so the two can never
       disagree. It is on `body` and not on `<html>`: check 11 in
       validate_site.py holds this file to the registered reader axes there. */
    var spine = document.querySelector('.spine');
    if (spine && spine.parentNode) spine.parentNode.insertBefore(bar, spine.nextSibling);
    else document.body.appendChild(bar);
    document.body.dataset.chapbar = 'on';
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
    button.appendChild(el('span', 'tb-icon', '◑'));
    button.appendChild(el('span', 'hide-sm', 'Appearance'));
    inner.appendChild(button);

    /* The topbar owns the button and nothing else about the panel. Opening,
       closing, moving, remembering a position and the focus contract all belong
       to the shell, so a second panel gets every one of them by asking for one.
       See "THE PANEL SHELL" below. */
    appearance = buildAppearancePanel();
    document.body.appendChild(appearance.el);
    appearance.attachOpener(button);

    /* The second opener, and the second panel. It is appended after the
       appearance button rather than before it because the topbar reads left to
       right as the page does: the control that changes how the page looks
       comes before the one that opens a workspace beside it. */
    var noteButton = el('button', 'tb-btn');
    noteButton.type = 'button';
    noteButton.appendChild(el('span', 'tb-icon', '\u270E'));
    noteButton.appendChild(el('span', 'hide-sm', 'Notes'));
    inner.appendChild(noteButton);

    studyNotes = buildNotesPanel();
    document.body.appendChild(studyNotes.el);
    studyNotes.attachOpener(noteButton);

    /* The third panel, and the only one with a condition on it. The
       highlighter is drawn with the CSS Custom Highlight API and deliberately
       has no DOM-splitting fallback, so on a browser without the API there is
       no button here at all rather than a control that does nothing. */
    if (markSupported()) {
      var markButton = el('button', 'tb-btn');
      markButton.type = 'button';
      markButton.appendChild(el('span', 'tb-icon', '\u25A4'));
      markButton.appendChild(el('span', 'hide-sm', 'Highlights'));
      inner.appendChild(markButton);

      highlighter = buildHighlighter();
      document.body.appendChild(highlighter.shell.el);
      /* The cue is inserted where the cluster is and for the same reason: a
         fixed control appended to the end of the body costs a keyboard reader
         every paragraph on the page before they reach it. */
      if (spine.parentNode) spine.parentNode.insertBefore(highlighter.cue, spine.nextSibling);
      else document.body.appendChild(highlighter.cue);
      highlighter.shell.attachOpener(markButton);
    }
  }

  /* ---------- the floating control cluster ----------
     Three controls, fixed to the bottom-right corner of every page, built here
     and present in no page's markup. The stylesheet section of the same name
     carries why it exists and where it sits; this is what it does.

     It is inserted straight after the topbar rather than appended to the body,
     so a reader on a keyboard reaches it in the same breath as the rest of the
     chrome instead of after every paragraph, figure and footer link on the
     page. That leaves a fixed overlay whose focus position is not its visual
     position, which is true of any fixed overlay and is the lesser of the two:
     a control cluster that costs eighty tab presses to reach is a control
     cluster keyboard readers do not have.

     It is a `role="group"` rather than a `role="toolbar"`, and that is a
     promise not made on purpose. A toolbar owes the reader arrow-key roving
     focus between its controls; three plain buttons in a labelled group owe
     nothing beyond Tab, which is what they implement. */
  var dockMode = null;
  var dockTop = null;

  /* The mode control names what it will do rather than what is on. The
     reference site's own button shows the current theme and reads as an
     instruction, so `Light` there means "you are in Light" and every reader
     who takes it for a button label presses it expecting the opposite. */
  function syncCluster() {
    if (!dockMode) return;
    var next = isDark() ? 'light' : 'dark';
    var say = 'Switch to ' + next + ' mode';
    dockMode.firstChild.textContent = next === 'dark' ? '\u263E' : '\u2600';
    dockMode.setAttribute('aria-label', say);
    dockMode.title = say;
  }

  function dockButton(glyph, label) {
    var control = el('button', 'dock-btn');
    control.type = 'button';
    control.title = label;
    control.setAttribute('aria-label', label);
    /* The glyph is its own element so the mode control can be relabelled
       without touching the button's attributes. It borrows no class from the
       topbar: `.dock-btn` sets the icon size itself, and one owner for a
       component's size is the rule the shared sheet is held to. */
    control.appendChild(el('span', null, glyph));
    return control;
  }

  function mountCluster() {
    var dock = el('div', 'dock');
    dock.setAttribute('role', 'group');
    dock.setAttribute('aria-label', 'Reader controls');

    /* Scroll to top, and it is the first child because the cluster hugs the
       right edge: a control that appears and disappears on the left grows the
       cluster away from the other two rather than pushing them under the
       reader's thumb. */
    dockTop = dockButton('\u2191', 'Back to the top of the page');
    dockTop.hidden = true;
    dockTop.addEventListener('click', function () {
      /* No `behavior` is named, so the browser reads `scroll-behavior` off the
         stylesheet: smooth by default and `auto` under either arm of the motion
         axis. Naming `smooth` here would animate a scroll for a reader who
         asked the whole system for no animation. */
      window.scrollTo({ top: 0 });
      /* Scrolling moves the page and leaves the keyboard where it was, so the
         next Tab would carry on from the foot of a document the reader has just
         left. Focus follows the scroll to the first thing at the top. It is
         `preventScroll` because the smooth scroll is already under way, and it
         is the wordmark because that is the page's first stop. A pointer
         activation sets the browser's modality to pointer, so this paints no
         ring for a reader using a mouse and paints one for a reader using
         Tab, which is what `:focus-visible` is for. */
      var first = document.querySelector('.spine .home');
      if (first) first.focus({ preventScroll: true });
    });
    dock.appendChild(dockTop);

    /* Nothing to launch on a page with no topbar, and no dead control either.
       The shell owns opening, closing and where focus goes; this is a second
       button asking it for the same contract the topbar's already has. */
    if (appearance) {
      var launch = dockButton('\u25D1', 'Appearance and reading settings');
      appearance.attachOpener(launch);
      dock.appendChild(launch);
    }

    /* The second panel's second way in, and it costs one call because the
       shell holds every opener rather than the last one. Escape returns the
       reader to whichever of the two buttons they actually used. */
    if (studyNotes) {
      var notesLaunch = dockButton('\u270E', 'Study notes for this page');
      studyNotes.attachOpener(notesLaunch);
      dock.appendChild(notesLaunch);
    }

    /* The third panel's second way in, on the same one call. It is absent on a
       browser with no Custom Highlight API, which is the same absence the
       topbar shows: a launcher for a panel that was never built is a dead
       control, and the cluster exists because dead controls are what it was
       built to replace. */
    if (highlighter) {
      var markLaunch = dockButton('\u25A4', 'Highlights on this page');
      highlighter.shell.attachOpener(markLaunch);
      dock.appendChild(markLaunch);
    }

    dockMode = dockButton('\u263E', 'Switch to dark mode');
    dockMode.addEventListener('click', function () { applyMode(isDark() ? 'light' : 'dark'); });
    dock.appendChild(dockMode);

    var spine = document.querySelector('.spine');
    if (spine && spine.parentNode) spine.parentNode.insertBefore(dock, spine.nextSibling);
    else document.body.appendChild(dock);

    /* A page the reader has not left yet has nowhere to go back to, so the
       control is not there. The threshold is one viewport rather than a
       literal, because "far enough to have lost the top" is a property of the
       screen in front of the reader and not of a number.

       It is never taken away while it holds focus. Hiding the element a
       keyboard reader is standing on drops focus to the body and loses their
       place in the tab order, and a reader can reach the top with the wheel
       while the control is focused. */
    var judge = function () {
      var far = (window.scrollY || document.documentElement.scrollTop || 0) > window.innerHeight;
      if (!far && dockTop.contains(document.activeElement)) return;
      // Only on a change. This runs on every frame of a scroll, and writing the
      // same state back each time is work the browser has to look at.
      var away = !far;
      if (dockTop.hidden !== away) dockTop.hidden = away;
    };
    window.addEventListener('scroll', judge, { passive: true });
    window.addEventListener('resize', judge);
    judge();
    syncCluster();
  }


  /* ============================================================
     THE IN-PAGE SECTION RAIL

     A reader half-way down a 3,000-word lesson has no idea where they are in
     it. The rail on the left names the pages of the course; nothing named the
     sections of the page in front of them. This does, on all 797 pages, and no
     page's markup mentions it: it is chrome, exactly as the topbar, the course
     rail and the floating cluster are, and it arrives because the page links
     the shared assets.

     It is DERIVED FROM THE PAGE'S OWN HEADINGS, at runtime, and from nothing
     else. That is the whole design. A model of the page's sections held
     anywhere but in the page is a second source that can disagree with it, and
     a lesson rewritten in the afternoon would leave it wrong by the evening.
     The headings are the one source that cannot drift from the page, because
     they are the page.

     Which headings, and why those. Measured from the corpus rather than
     guessed: inside `main`, the hub's 744 lesson pages carry 6,260 `h2`, 1,236
     `h3` and 10 `h4`, and 5,559 of the `h2` are direct children of the content
     region. So `h2` is this hub's section level, `h3` is an occasional
     subdivision inside one section rather than a section of its own, and `h4`
     barely exists. The rule is therefore one line - an `h2` that is a direct
     child of the content region and is not wearing a smaller face - and it is
     the same rule `.numbered` already applies when it draws the section
     badges, so the numbered squares down the page and the ticks down the rail
     can never name different sections.

     Direct children is also what keeps everything else out without naming any
     of it. The topbar, the course rail, both panels and the floating cluster
     are children of `body`; a figure's caption, a callout's heading and a
     card's title are grandchildren at best. None of them is a child of `main`,
     so none of them can appear in a list built this way, and a widget added
     next year cannot leak into it either.

     WHERE THE READER IS, in one sentence: the reader is in the last section
     whose heading has reached the reading line. The reading line is the
     stylesheet's `--secrail-line`, read back in pixels off the heading that
     has to land on it, so the distance that positions a jump and the distance
     that decides which section is current are the same number and can never
     drift apart. When two sections are on screen at once - the tail of one and
     the heading of the next - the reader is in the earlier of the two, because
     they have not reached the later heading yet. The reader is in exactly one
     section, or, above the first heading, in none: a page's opening is not a
     section and saying it is would be a small lie told on every page load.

     It is tracked with an IntersectionObserver rather than a scroll handler,
     and the observer's shape is what makes that honest. The root is the
     viewport from the reading line down; the thresholds are 0 and 1. A
     heading's top crossing the line is a crossing of threshold 1 - it stops
     being wholly inside the root - and a heading's bottom crossing the line is
     a crossing of threshold 0. Between them, every transition of "has this
     heading reached the line" raises a callback, which is what a single
     threshold could not promise: with 0 alone the highlight lagged by the
     height of the heading, and with a one-pixel band a fast scroll stepped
     over the band between two frames and the callback never came. The callback
     itself reads the headings' own rectangles rather than the entries, so what
     is painted is the geometry at the moment of painting and not a fact
     remembered from an earlier frame.

     It appears above a stated heading count and not before. It is not printed.
     It does not compete with the course rail, and the media query that holds
     it to wide viewports carries the reason.
     ============================================================ */

  /* Four sections, and below that no rail at all. A rail answers two questions
     - where am I, and how much is left - and on a page of three sections the
     scrollbar has already answered both, so a list of three is chrome that
     outweighs what it indexes. Fifty-seven of the hub's 789 content pages
     carry three sections or fewer and get nothing, which is the intended
     outcome rather than a gap. */
  var SECTION_MIN = 4;

  /* The sections of the page, in document order. The whole rule, and the
     reasoning behind every clause of it, is in the block above. */
  function pageSections(region) {
    var out = [];
    for (var node = region.firstElementChild; node; node = node.nextElementSibling) {
      if (node.tagName !== 'H2') continue;
      // `.h-label` and `.h-sub` are h2 tags wearing a smaller face - "The
      // one-minute version" is the common one - and neither is a section of
      // the argument. The tag sets the outline; the class sets the size.
      if (node.classList.contains('h-label') || node.classList.contains('h-sub')) continue;
      out.push(node);
    }
    return out;
  }

  /* A heading's text as a fragment identifier. Deterministic, so the same
     heading yields the same id on every load and in every build, which is what
     makes a link a reader shared last month still land in the right place
     today. Accents fold onto their letters, an apostrophe is dropped rather
     than turned into a word break, and every other run of non-alphanumeric
     characters becomes one dash. */
  function sectionSlug(text) {
    return text
      .normalize('NFKD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/['\u2018\u2019]/g, '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  /* The id a section is linked by. An author's own id is used exactly as
     written and is never replaced - it is the one a page may already be linked
     by from outside - and a heading without one is given `sec-` plus its slug.

     The collision rule. The candidate is taken only if nothing in the document
     already answers to it, which covers both halves of the problem at once: an
     id an author wrote elsewhere on the page, and a second heading whose words
     match an earlier one's. Otherwise the next free `-2`, `-3` and so on is
     taken, counting in document order, so the first heading with those words
     keeps the plain id and a later one can never take it away from it. A
     heading whose text yields no slug at all - punctuation alone - takes its
     own position in the sequence instead, which is unique by construction. */
  function anchorFor(head, ordinal) {
    if (head.id) return head.id;
    var slug = sectionSlug(head.textContent || '');
    var stem = 'sec-' + (slug || String(ordinal));
    var id = stem;
    var next = 1;
    while (document.getElementById(id)) { next += 1; id = stem + '-' + next; }
    head.id = id;
    return id;
  }

  function mountSectionRail() {
    var region = document.querySelector('main.wrap, main.wide');
    if (!region) return;
    var heads = pageSections(region);
    if (heads.length < SECTION_MIN) return;

    var nav = el('nav', 'secrail');
    /* A navigation region with no name is one a screen reader announces as
       "navigation" beside two others that say the same thing. This one says
       which page's sections it holds. */
    nav.setAttribute('aria-label', 'Sections on this page');
    var list = el('ol');
    var links = [];

    heads.forEach(function (head, index) {
      var link = el('a');
      link.href = '#' + anchorFor(head, index + 1);
      /* A plain anchor, and deliberately nothing else. The browser scrolls it,
         reads `scroll-behavior` off the stylesheet - so the motion axis governs
         whether the jump animates and no branch here has to - puts the address
         bar on the section the reader is now reading, and moves the sequential
         focus starting point to the heading, so the next Tab carries on from
         there rather than from the rail. Every one of those is a user story,
         and none of them is a line of script. */
      /* The label first and the tick second, so the tick is the element
         nearest the edge of the viewport. Opening the labels then grows the
         list leftwards and every tick stays exactly where it was, under
         whatever pointer was aiming at one. */
      link.appendChild(el('span', 'secrail-label', (head.textContent || '').trim()));
      link.appendChild(el('span', 'secrail-tick'));
      var row = el('li');
      row.appendChild(link);
      list.appendChild(row);
      links.push(link);
    });

    nav.appendChild(list);
    /* Immediately before the content it indexes, so a keyboard reader meets
       the sections of the page and then the page, in that order. */
    region.parentNode.insertBefore(nav, region);

    /* The reading line, in pixels, read off the stylesheet rather than stated
       twice. `--secrail-line` is the section headings' own `scroll-margin-top`,
       so a jump lands a heading exactly on the line and the same heading is at
       once the current one. A literal here would be that number's second home
       and the two would part company the first time a design moved one. */
    var line = parseFloat(getComputedStyle(heads[0]).scrollMarginTop) || 0;
    /* One pixel above the line, and it is the same number twice on purpose:
       the root's top edge and the test below. A heading is wholly inside the
       root while its top is at or below that edge and stops being wholly
       inside the moment its top rises past it, so the observation and the
       answer are one event rather than two that agree most of the time. The
       pixel is what makes a jump land right: `scroll-margin-top` puts the
       heading's top exactly on the line, which is inside the edge, so the
       section the reader jumped to is current the moment they arrive. */
    var edge = line + 1;
    var current = -1;

    function paint() {
      var found = -1;
      for (var index = 0; index < heads.length; index += 1) {
        // The headings are in document order, so their tops rise together and
        // the first one still below the edge ends the search.
        if (heads[index].getBoundingClientRect().top >= edge) break;
        found = index;
      }
      if (found === current) return;
      if (current >= 0) links[current].removeAttribute('aria-current');
      current = found;
      /* `location` rather than `page`: the course rail's `page` says which page
         of the course this is, and this says which place within the page the
         reader is at. Two different claims, and a screen reader announces the
         difference. */
      if (current >= 0) links[current].setAttribute('aria-current', 'location');
    }

    if (!window.IntersectionObserver) return;
    /* The root is the viewport from the reading line down, and both thresholds
       are watched. See the block above for why one of them is not enough. A
       resize or a reflow changes the geometry rather than the scroll position,
       and the observer recomputes on both, so nothing here listens for either. */
    var watch = new IntersectionObserver(paint, {
      rootMargin: (-edge) + 'px 0px 0px 0px',
      threshold: [0, 1]
    });
    heads.forEach(function (head) { watch.observe(head); });
  }

  /* ---------- the appearance panel ---------- */
  var MODES = [
    { key: '',      label: 'System', glyph: '◐' },
    { key: 'light', label: 'Light',  glyph: '☀' },
    { key: 'dark',  label: 'Dark',   glyph: '☾' }
  ];

  /* ---------- a segmented group of registered choices ----------
     Three of the six controls and the motion default are one shape: a short
     list of registered steps, one native button each, the chosen one carrying
     `aria-pressed`. It reuses the mode group's own classes rather than
     inventing a second pair the widget vocabulary would have to learn, exactly
     as the design group already does with the palette cards.

     `axis` is the attribute a sync pass reads the pressed state back from, so
     the panel and the page can never disagree about what is on: nothing here
     remembers what it drew. */
  function segmented(axis, list, choose) {
    var cards = el('div', 'mode-cards');
    cards.style.gridTemplateColumns = 'repeat(' + list.length + ', 1fr)';
    list.forEach(function (item) {
      var card = el('button', 'mode-card');
      card.type = 'button';
      card.dataset[axis] = item.key;
      card.appendChild(el('span', null, item.label));
      card.addEventListener('click', function () { choose(item.key); });
      cards.appendChild(card);
    });
    return cards;
  }

  /* ---------- a range, in a unit the reader can act on ----------
     The current value is read out of the stylesheet rather than remembered
     here, so a slider that has never been touched shows what the page actually
     renders - which is not one number, because the narrow-viewport block sets a
     smaller body size and a design may set another.

     The reading sits in an `output` inside the control's own `<label>`, so a
     screen reader announces it with the control's name and no live region has
     to speak on every step of a drag. */
  function rangeField(axis) {
    var field = el('div', 'set-field');
    var id = 'set-' + axis.name;
    var label = el('label', 'set-lbl');
    label.htmlFor = id;
    label.appendChild(el('span', null, axis.label));

    /* The readout is for the eye only. A range announces its own value, so the
       number in the label would be said twice; `aria-valuetext` carries the
       unit instead, which is what makes "80" into "80 characters" without a
       live region speaking on every step of a drag. */
    var readout = document.createElement('output');
    readout.setAttribute('aria-hidden', 'true');
    label.appendChild(readout);

    var input = el('input');
    input.type = 'range';
    input.id = id;
    input.min = String(axis.min);
    input.max = String(axis.max);
    input.step = String(axis.step);

    var show = function () {
      var legend = axis.legend(Number(input.value));
      readout.textContent = legend;
      input.setAttribute('aria-valuetext', legend);
    };
    input.addEventListener('input', function () {
      applyRangeValue(axis, Number(input.value), false);
      show();
    });
    input.addEventListener('change', function () {
      applyRangeValue(axis, Number(input.value), true);
      show();
    });

    field.appendChild(label);
    field.appendChild(input);
    field.rangeAxis = axis;
    return field;
  }

  /* A group of buttons is not a labelled control, so the name has to be tied on
     rather than assumed: the visible label gets an id and the container gets
     `role="group"` pointing at it, which is what makes a screen reader say
     "Line spacing" when focus enters the row instead of leaving "Tight" to
     stand on its own. */
  function choiceField(name, label, list, choose) {
    var field = el('div', 'set-field');
    var caption = el('span', 'set-lbl', label);
    caption.id = 'set-lbl-' + name;
    var cards = segmented(name, list, choose);
    cards.setAttribute('role', 'group');
    cards.setAttribute('aria-labelledby', caption.id);
    field.appendChild(caption);
    field.appendChild(cards);
    return field;
  }

  /* The panel is a shell plus a body. Everything the reader can do to the panel
     itself - open it, close it, pick it up, step it with the arrow keys, put it
     back, have it remembered - is the shell's, asked for by name and store key.
     What is left here is the six controls, which is all this function should
     ever have been about. */
  function buildAppearancePanel() {
    var shell = makePanel({
      name: 'appearance',
      className: 'settings',
      title: 'Appearance',
      closeLabel: 'Close appearance panel',
      storeKey: STORE.panel,
      onOpen: syncSettings
    });
    var body = shell.body;

    /* ---------- 1. ground ----------
       Mode and palette are the accessibility control the rest of the panel is
       often mistaken for. The success criterion that asks for selectable
       foreground and background is satisfied by a mechanism rather than by a
       good default, and this pair is that mechanism. There is nothing between
       the light band and the dark band, which is what keeps the forbidden
       ground - the lightness range where no ink reaches the standard - out of
       the reader's reach by construction rather than by a warning. */
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
    body.appendChild(modeGroup);

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
    body.appendChild(palGroup);

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
    body.appendChild(designGroup);

    /* ---------- 2 to 6. reading ----------
       In the order a reader is likely to reach for them, largest effect first.
       None of these is an independent setting: the measure is in real
       characters and the width follows the face, the body size is apparent size
       and the rendered px follows the face, the code size follows the face on
       its own, and the leading rises with a wide measure unless the reader has
       stated one. hub.css derives all four, so this panel offers the four
       inputs and never the outputs. */
    var readGroup = el('div', 'set-group');
    readGroup.appendChild(el('h3', null, 'Reading'));
    RANGES.forEach(function (axis) {
      if (axis.name === 'bodysize') readGroup.appendChild(rangeField(axis));
    });

    readGroup.appendChild(choiceField('face', 'Reading face', FACES, applyFace));

    RANGES.forEach(function (axis) {
      if (axis.name === 'measure') readGroup.appendChild(rangeField(axis));
    });

    readGroup.appendChild(choiceField('leading', 'Line spacing', LEADINGS, applyLeading));
    readGroup.appendChild(choiceField('density', 'Density', DENSITIES, applyDensity));

    readGroup.appendChild(el('p', 'set-note',
      'Your choices are remembered in this browser and apply to every course in the hub.'));
    body.appendChild(readGroup);

    /* ---------- accessibility: motion, and the way back ---------- */
    var accessGroup = el('div', 'set-group');
    accessGroup.appendChild(el('h3', null, 'Accessibility'));
    accessGroup.appendChild(choiceField('motion', 'Motion', MOTIONS, applyMotion));

    var reset = el('button', 'set-reset', "Back to this course's defaults");
    reset.type = 'button';
    reset.addEventListener('click', resetEverything);
    accessGroup.appendChild(reset);
    body.appendChild(accessGroup);

    return shell;
  }

  /* ---------- back to the defaults ----------
     Exact, because the reader's layer is an input to a token and never a
     competitor to one: removing a `--*-user` property leaves the stylesheet's
     own value with nothing to unwind, and removing a registered axis attribute
     leaves the arm a page with no script renders. The panel's own position goes
     too, so no setting a reader can reach is a setting they cannot get out of. */
  function resetEverything() {
    RANGES.forEach(function (axis) { applyRangeValue(axis, null, false); });
    applyLeading(LEADING_DEFAULT);
    applyDensity(DENSITY_DEFAULT);
    applyMotion('');
    applyFace(FACES[0].key);
    applyPalette(PALETTES[0].key);
    applyDesign(DESIGNS[0].key);
    applyMode('');
    if (appearance) appearance.goHome();
    /* Where a panel sits is a setting the reader can reach, so both panels come
       back. What the reader wrote is not a setting and this button does not go
       near it: a reset that quietly deleted a page of notes would be the worst
       defect in the hub, and it is one line away at all times. */
    if (studyNotes) studyNotes.goHome();
    syncSettings();
  }

  /* ============================================================
     THE PANEL SHELL

     One contract, and every panel wears it. A panel is a strip the reader can
     take hold of, a body, and a place the reader put it; `makePanel` owns all
     three and a caller supplies a name, a store key and what goes in the body.
     The reason the contract lives here rather than in the panel that first
     needed it is that a second panel written beside it would drift: one would
     trap focus, one would forget its position, one would close on an outside
     click, and the three would have to be corrected three times.

     ---------- opening, closing, and where focus goes ----------
     The specification's focus contract was written against a popover anchored
     to the button that opens it, and a panel the reader can pick up and park
     beside the paragraph they are judging is a different thing. So the contract
     is restated here, and every difference from the anchored one follows from
     the panel being movable.

     It is a NON-MODAL dialog: `role="dialog"` and `aria-labelledby`, and no
     `aria-modal`. A reader moves a panel in order to keep reading with it open,
     so the page behind it is not inert and saying that it is would be a lie a
     screen reader then acts on. For the same reason focus is not trapped: Tab
     walks out of the panel into the page and back round, which is what a reader
     who has parked it wants and what a trap would forbid.

     Focus moves into the panel when it opens, because the reader asked for it.
     On close it returns to the opening button only if it was inside the panel
     at the time - a reader who has tabbed back into the page and pressed Escape
     keeps their place instead of being thrown to the topbar.

     An outside click does not close a panel, and none of this is configurable.
     A parked panel that vanishes the moment the reader clicks the text beside
     it is a panel that cannot be parked, and a panel that dims the page behind
     it is a panel that hides the thing the reader opened it to work on. The
     ways out are the opening button, the close control in the title bar, and
     Escape - three, all of them visible or conventional.

     ---------- where a panel sits ----------
     The reader can pick a panel up with a pointer or with the keyboard, and the
     position is a preference like any other: it lives in the same store, under
     a key of that panel's own, and it is restored before the panel is shown.
     Two panels therefore remember two places and neither can overwrite the
     other's.

     What is stored is an INTENTION and what is rendered is that intention
     clamped into whatever viewport is in front of the reader now. A pair of
     coordinates that was right on a wide display is simply out of reach on a
     phone, so the clamp runs on every open and on every resize, and it does not
     write back: going from the phone to the display puts the panel where it was
     left rather than where the phone could fit it.

     The band the panel is held inside is measured rather than assumed. The
     topbar is sticky, and the pre-production strip and the chapter bar are both
     fixed to the foot of the viewport and both change height on a narrow
     screen, so all three are read off the elements themselves. A panel parked
     under any of them is a panel the reader cannot reach.
     ============================================================ */
  var PANEL_EDGE = 8;      // the gap a panel keeps from every edge
  var PANEL_STEP = 20;     // one arrow key
  var PANEL_FINE = 4;      // one arrow key with Shift held

  function makePanel(spec) {
    /* Every piece of state below belongs to this panel alone. A second panel
       gets its own, which is the whole reason the shell is a factory rather
       than a set of functions over one module-level element. */

    /* Where the panel was last put, which is not always where it is. A
       framework move glides, and `getBoundingClientRect` during a glide reports
       the frame the panel is passing through rather than the place it is going
       to. Reading that back is what made two arrow presses in quick succession
       add up to one: the second read a position still in flight and stepped
       from there. So the intended position is held here and the rendered one is
       never asked. */
    var placed = null;
    var dragging = null;
    var suppressClick = false;
    /* A panel can have more than one way in - the topbar button and the
       cluster's launcher both open the appearance panel - so the shell holds
       every attached opener and remembers which one was actually used. All of
       them wear the state; only the one that opened it gets focus back. A
       reader who opened the panel from the corner of the screen and was thrown
       to the topbar on Escape has lost their place, which is the thing the
       focus contract exists to prevent. */
    var openers = [];
    var opener = null;

    var panel = el('div', spec.className ? 'panel-shell ' + spec.className : 'panel-shell');
    panel.hidden = true;
    panel.setAttribute('role', 'dialog');
    /* The panel's own id, which is what `attachOpener` points `aria-controls`
       at. A button that says it opens a dialog and does not say which one
       leaves a screen reader to guess between two, and it leaves a harness the
       same problem: `scripts/focus_walk.py` walks both panels and reaches each
       by the button that names it. */
    panel.id = 'panel-' + spec.name;
    var titleId = 'panel-' + spec.name + '-title';
    var hintId = 'panel-' + spec.name + '-hint';
    panel.setAttribute('aria-labelledby', titleId);

    /* ---------- the title bar, which is the handle ----------
       The captain asked for a movable bar and meant it: the panel is picked up
       and put where the reader wants it, rather than hanging off the button
       that opened it. The whole strip is the pointer surface and the grip
       inside it is the keyboard one, because a panel only a mouse can move is a
       panel some readers cannot move at all. */
    var bar = el('div', 'panel-bar');
    var grip = el('button', 'panel-grip');
    grip.type = 'button';
    grip.setAttribute('aria-label', 'Move panel');
    grip.setAttribute('aria-describedby', hintId);
    grip.setAttribute('aria-keyshortcuts', 'ArrowUp ArrowDown ArrowLeft ArrowRight Home');
    grip.appendChild(el('span', 'tb-icon', '✥'));
    var title = el('h2', 'panel-title', spec.title);
    title.id = titleId;
    var shut = el('button', 'panel-close');
    shut.type = 'button';
    shut.setAttribute('aria-label', spec.closeLabel);
    shut.appendChild(el('span', 'tb-icon', '✕'));
    shut.addEventListener('click', function () { close(true); });
    bar.appendChild(grip);
    bar.appendChild(title);
    bar.appendChild(shut);
    panel.appendChild(bar);

    var hint = el('p', 'sr-only',
      'Drag this panel to move it, or press the arrow keys while this control has focus. '
      + 'Hold Shift for a smaller step. Press Enter or Home to return the panel to its usual place.');
    hint.id = hintId;
    panel.appendChild(hint);

    var body = el('div', 'panel-body');
    panel.appendChild(body);

    /* ---------- the foot, which is pinned rather than scrolled ----------
       Optional, because the appearance panel has nothing that belongs in one.
       A panel that holds a document has: the notes panel asked for it first,
       because a save state a reader has to scroll to is a save state a reader
       can miss, and the highlighter asks for exactly the same thing. It sits in
       the panel and outside `body`, which is the title bar's shape at the other
       end, and it belongs to the shell rather than to either panel so that the
       two cannot drift into two shapes. */
    var foot = spec.foot ? el('div', 'panel-foot') : null;
    if (foot) panel.appendChild(foot);

    function bounds() {
      var spine = document.querySelector('.spine');
      var box = panel.getBoundingClientRect();
      var ceiling = (spine ? spine.getBoundingClientRect().bottom : 0) + PANEL_EDGE;
      /* Everything fixed across the foot, measured rather than assumed: the
         pre-production strip and the chapter bar. Each is absent on some pages
         and the two are present together on a pre-production lesson, so the
         floor is their sum and not whichever one this code was written for.
         Measuring is what makes the strip's two-line phone height and the bar's
         one-line phone height correct here without either being restated. */
      var footHeight = 0;
      Array.prototype.forEach.call(document.querySelectorAll('.preprod-flag, .chapbar'), function (fixed) {
        footHeight += fixed.getBoundingClientRect().height;
      });
      var floor = window.innerHeight - footHeight - PANEL_EDGE;
      return {
        minX: PANEL_EDGE,
        maxX: Math.max(PANEL_EDGE, window.innerWidth - box.width - PANEL_EDGE),
        minY: ceiling,
        // A panel taller than the band it has to fit in is pinned to the top of
        // that band rather than pushed above it, and scrolls inside itself.
        maxY: Math.max(ceiling, floor - box.height)
      };
    }

    function place(x, y) {
      var limit = bounds();
      placed = {
        x: Math.min(Math.max(x, limit.minX), limit.maxX),
        y: Math.min(Math.max(y, limit.minY), limit.maxY)
      };
      panel.style.left = placed.x + 'px';
      panel.style.top = placed.y + 'px';
      panel.setAttribute('data-moved', '');
    }

    function at() {
      if (placed) return placed;
      var box = panel.getBoundingClientRect();
      return { x: box.left, y: box.top };
    }

    function storedPosition() {
      var raw = get(spec.storeKey);
      if (!raw) return null;
      try {
        var seen = JSON.parse(raw);
        if (seen && isFinite(seen.x) && isFinite(seen.y)) return { x: Number(seen.x), y: Number(seen.y) };
      } catch (e) { /* a key from another era, or a hand edit */ }
      return null;
    }

    function placeFromStore() {
      if (panel.hidden) return;
      var was = storedPosition();
      if (was) place(was.x, was.y);
      else goHome();
    }

    /* The viewport changed under a panel the reader placed. It glides back into
       reach rather than jumping, because a panel that teleports on a rotation
       reads as a bug and a panel that slides reads as the framework putting it
       somewhere it fits. `data-settling` is what carries the glide, and every
       direct move takes it off again: a step the reader is aiming must land
       where they aimed it, at once. Under either arm of the motion axis the
       glide is zeroed with everything else the framework animates, so reduced
       motion is answered by the stylesheet and not by a branch here. */
    function reseat() {
      if (panel.hidden) return;
      panel.setAttribute('data-settling', '');
      placeFromStore();
    }

    /* The way back. Removing the two lengths hands the panel to the
       stylesheet's own resting place, so "home" is one answer written in one
       file rather than a pair of numbers repeated here. */
    function goHome() {
      placed = null;
      panel.style.left = '';
      panel.style.top = '';
      panel.removeAttribute('data-moved');
      drop(spec.storeKey);
    }

    function rememberPosition() {
      if (placed) set(spec.storeKey, JSON.stringify({ x: Math.round(placed.x), y: Math.round(placed.y) }));
    }

    /* The pointer. One code path for mouse, touch and pen, and the capture is
       what keeps the panel following a finger that has left the strip. The grab
       offset is taken once, so the panel does not jump to centre itself under
       the pointer on the first move. */
    bar.addEventListener('pointerdown', function (event) {
      if (event.button !== 0 && event.pointerType === 'mouse') return;
      // The close control lives in the strip and is not part of the handle.
      if (shut.contains(event.target)) return;
      suppressClick = false;
      panel.removeAttribute('data-settling');
      var from = at();
      dragging = {
        id: event.pointerId,
        grabX: event.clientX - from.x,
        grabY: event.clientY - from.y,
        was: from,
        wasMoved: panel.hasAttribute('data-moved'),
        dragged: false
      };
      panel.setAttribute('data-dragging', '');
      bar.setPointerCapture(event.pointerId);
      // Without this a mouse drag selects the prose behind the panel as it
      // goes. `user-select` covers the strip's own text and not the page's.
      event.preventDefault();
    });

    bar.addEventListener('pointermove', function (event) {
      if (!dragging || event.pointerId !== dragging.id) return;
      dragging.dragged = true;
      place(event.clientX - dragging.grabX, event.clientY - dragging.grabY);
    });

    var release = function (event) {
      if (!dragging || event.pointerId !== dragging.id) return;
      panel.removeAttribute('data-dragging');
      if (dragging.dragged) {
        rememberPosition();
        // A drag that ends on the grip fires a click there too, and putting the
        // panel back the instant it was placed is the opposite of what the
        // reader asked for. The next press clears this whether a click came or
        // not, so it can never swallow a later genuine one.
        suppressClick = true;
      }
      dragging = null;
    };
    bar.addEventListener('pointerup', release);
    bar.addEventListener('pointercancel', release);

    /* The keyboard. Arrow keys move the panel while the grip has focus, with no
       mode to enter and none to be stranded in: a control whose whole purpose
       is the position takes the arrow keys the way a slider does. Enter and
       Space are the button's own activation and Home is the same action, so
       there is no keystroke here that does nothing. */
    grip.addEventListener('keydown', function (event) {
      var step = event.shiftKey ? PANEL_FINE : PANEL_STEP;
      var dx = 0;
      var dy = 0;
      if (event.key === 'ArrowLeft') dx = -step;
      else if (event.key === 'ArrowRight') dx = step;
      else if (event.key === 'ArrowUp') dy = -step;
      else if (event.key === 'ArrowDown') dy = step;
      else if (event.key === 'Home') { goHome(); event.preventDefault(); return; }
      else return;
      panel.removeAttribute('data-settling');
      var from = at();
      place(from.x + dx, from.y + dy);
      rememberPosition();
      // Arrow keys scroll the page by default, and a panel that moves while the
      // page slides under it is a control nobody can aim.
      event.preventDefault();
    });
    grip.addEventListener('click', function () {
      if (suppressClick) { suppressClick = false; return; }
      goHome();
    });

    /* Escape during a drag puts the panel back where it was picked up, which is
       the one undo a drag needs. It runs on the window in the capture phase so
       it settles before the handler that closes the panel sees the key: a
       cancelled drag must not also close the thing being dragged. */
    window.addEventListener('keydown', function (event) {
      if (!dragging || event.key !== 'Escape') return;
      var was = dragging.was;
      var wasMoved = dragging.wasMoved;
      panel.removeAttribute('data-dragging');
      if (bar.hasPointerCapture && bar.hasPointerCapture(dragging.id)) bar.releasePointerCapture(dragging.id);
      dragging = null;
      suppressClick = true;
      if (wasMoved) place(was.x, was.y); else goHome();
      event.stopPropagation();
      event.preventDefault();
    }, true);

    /* A stored position outlives the viewport it was chosen in. Re-seating it
       on every resize is what stops a reader who rotated a tablet, or came back
       on a smaller screen, finding the panel parked off the edge. */
    window.addEventListener('resize', reseat);

    function announce(shown) {
      openers.forEach(function (button) {
        button.setAttribute('aria-expanded', shown ? 'true' : 'false');
      });
    }

    /* `onClose` runs before the panel goes away and while its controls still
       hold whatever the reader last put in them. The notes panel is what asked
       for it: closing the panel is one of the four ways the reference site
       loses text, because it removes the drawer without flushing the write
       that was still in flight. A panel that has something to settle settles
       it here. */
    function close(restoreFocus) {
      if (panel.hidden) return;
      if (spec.onClose) spec.onClose();
      var inside = document.activeElement && panel.contains(document.activeElement);
      panel.hidden = true;
      announce(false);
      if (restoreFocus && inside && opener) opener.focus();
    }

    function open(from) {
      if (!panel.hidden) return;
      // Opened by script rather than by a control, the last button used is
      // still where focus should go back to.
      if (from) opener = from;
      panel.hidden = false;
      announce(true);
      if (spec.onOpen) spec.onOpen();
      // The panel has no size while it is hidden, so the constraint that keeps
      // it on screen can only be applied now. This is also what re-seats a
      // stored position that no longer fits the viewport in front of the reader.
      placeFromStore();
      var first = panel.querySelector('button, input, select, textarea, a[href]');
      if (first) first.focus();
    }

    /* Escape belongs to the panel the reader is in. With focus inside another
       panel this one stays open; with focus anywhere else every open panel
       closes, which is exactly what a lone panel has always done. */
    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape' || panel.hidden) return;
      var active = document.activeElement;
      if (active && active.closest && active.closest('.panel-shell') && !panel.contains(active)) return;
      close(true);
    });

    /* The button that opens the panel belongs to whatever built it - the topbar,
       a control cluster, a page. What the shell insists on is that the button
       and the panel never disagree about whether it is open, which is the defect
       the reference site ships: `aria-expanded` written once into the markup and
       never updated again. */
    function attachOpener(button) {
      openers.push(button);
      if (!opener) opener = button;
      button.setAttribute('aria-haspopup', 'dialog');
      button.setAttribute('aria-controls', panel.id);
      button.setAttribute('aria-expanded', String(!panel.hidden));
      button.addEventListener('click', function () {
        if (panel.hidden) open(button); else close(true);
      });
    }

    return {
      el: panel,
      body: body,
      foot: foot,
      open: open,
      close: close,
      goHome: goHome,
      attachOpener: attachOpener
    };
  }

  /* ============================================================
     THE STUDY NOTES PANEL

     A second panel on the shared shell, and the whole of it is chrome: no page
     in the hub names it, no page markup changes, and a page served with the
     script blocked has no button, no panel and no trace. Everything the reader
     can do to the panel itself belongs to the shell above and is not restated
     here; what follows is what this panel contains and what it promises.

     ---------- the promise, which is that the save state is true ----------
     The reference implementation this was read from paints a green `Saved` on
     every keystroke because `setItem` was called, never because it worked. Its
     write swallows the exception, the caller consults no return value, and a
     reader whose quota is full watches the panel confirm every save and loses
     every word on the next reload. That is the defect this panel exists not to
     copy, and it is why `setChecked` and `dropChecked` are separate helpers
     from `set` and `drop` rather than the same ones with a flag.

     Three states, and each is a fact rather than an intention:

       Saving                what the reader typed is not in storage yet
       Saved HH:MM           the store was written and read back equal
       Not saved: ...        the write failed, and Export is the way out

     Research counted four ways to lose text in the reference. Each is closed
     here and each fix is named where it lives:

       a  the silent quota failure         `setChecked`, and the state above
       b  nothing flushes on exit          `visibilitychange`, `pagehide`, blur
       c  closing the panel does not save  the shell's `onClose`
       d  a stale read overwrites the live editor
                                           `drafts`, below: what the reader can
                                           see is authoritative and storage is
                                           never read over the top of it

     ---------- where a note lives ----------
     Under `coursehub.note:` plus a tier and an identifier, one key per
     document. The identifier is the course key and the file name, which are
     the two things this repository has committed never to change: `AGENTS.md`
     forbids renumbering or renaming a lesson because its URL is public, and a
     course folder is in every cross-course link in the hub. A lesson's title
     is not among them and is rewritten often, which is exactly the mistake the
     reference makes - it keys on a slug built from a hand-maintained title
     array, so editing a chapter's title orphans every note under it, silently,
     with the old key left in storage unreachable.

     The course key comes from `COURSE_OUTLINE.key` where a course ships an
     outline and from the `data-course` folder otherwise, and the two are made
     to agree rather than being two identifiers. It is the same key the reading
     progress map already uses, so notes and progress cannot disagree about
     what a lesson is.

     ---------- what the scope control means ----------
     The reference site shows a badge reading `All Masterclass Lessons` beside
     its editor. It is a `div`. It has no handler, no role and no keyboard
     behaviour: it is a label that looks like a selector, and it says the same
     thing whatever page it is on. A control that appears to offer a choice and
     offers none is worse than no control, so this one is real. Three tiers,
     because the hub is eighteen courses and the reference was one:

       This page      the lesson, the course map or the reference page in front
                      of the reader
       This course    one running document for the whole course, reachable from
                      every page in it
       All courses    one document for the hub

     A page with no course - the hub landing page, the design system - offers
     the two tiers it actually has. The panel names the key it is editing under
     the control, so the answer to "where did that go" is on screen.
     ============================================================ */

  /* The pause that commits, and the longest a keystroke may go unwritten. The
     reference has the first and not the second, so a reader who types without
     pausing has nothing in storage however long they type. The ceiling is what
     bounds the loss to two seconds rather than to a paragraph. */
  var NOTE_SETTLE = 400;
  var NOTE_LATEST = 2000;

  var NOTE_VIEWS = [
    { key: 'write', label: 'Write' },
    { key: 'read',  label: 'Preview' }
  ];

  /* The toolbar, as data. Every entry is one splice of literal markdown
     characters around the selection and there is no model behind it, which is
     the part of the reference worth taking whole: a plain textarea and two
     primitives do all of the formatting, so there is nothing to vendor and
     nothing to keep in step with the text.

     `wrap` puts characters either side of the selection; `line` puts them in
     front of every line it covers. `heading` and `code` are the two that read
     what is already there, and each says why below. */
  var NOTE_TOOLS = [
    { key: 'bold',    glyph: 'B',  name: 'Bold',          wrap: ['**', '**'], sample: 'bold text',   keys: 'Ctrl+B' },
    { key: 'italic',  glyph: 'I',  name: 'Italic',        wrap: ['*', '*'],   sample: 'italic text', keys: 'Ctrl+I' },
    { key: 'heading', glyph: 'H',  name: 'Heading, one level deeper each press' },
    { key: 'mark',    glyph: '==', name: 'Highlight',    wrap: ['==', '=='], sample: 'highlighted' },
    { key: 'strike',  glyph: 'S',  name: 'Strikethrough', wrap: ['~~', '~~'], sample: 'struck out' },
    { key: 'code',    glyph: '‹›', name: 'Code', keys: 'Ctrl+Shift+C' },
    { key: 'list',    glyph: '•', name: 'Bulleted list', line: '- ',    sample: 'list item' },
    { key: 'task',    glyph: '☐', name: 'Task',          line: '- [ ] ', sample: 'something to review' },
    { key: 'callout', glyph: '!',  name: 'Callout',       line: '> ',
      sample: '[!tip] Key idea\nwhat the idea is' }
  ];

  /* ---------- which document this page is looking at ----------
     Two derivations of one identifier rather than two identifiers. A course
     that ships an outline states its own key; every other page falls back to
     the folder in the URL with the suffix taken off, which is the same string
     the generator would have written. */
  function courseKey() {
    var outline = window.COURSE_OUTLINE;
    if (outline && outline.key) return String(outline.key);
    var folder = root.getAttribute('data-course');
    return folder ? folder.replace(/-course$/, '') : '';
  }

  function pageKey() {
    return (courseKey() || 'hub') + '/' + (fileOf(location.pathname) || 'index.html');
  }

  function noteScopes() {
    var course = courseKey();
    var scopes = [{
      key: 'page',
      label: 'This page',
      store: NOTE_PREFIX + 'page:' + pageKey(),
      file: (course || 'hub') + '-' + (fileOf(location.pathname) || 'index.html').replace(/\.html?$/i, '')
    }];
    if (course) {
      scopes.push({
        key: 'course',
        label: 'This course',
        store: NOTE_PREFIX + 'course:' + course,
        file: course + '-course'
      });
    }
    scopes.push({
      key: 'hub',
      label: 'All courses',
      store: NOTE_PREFIX + 'hub',
      file: 'course-hub'
    });
    return scopes;
  }

  /* ---------- the two splice primitives ----------
     Both end by dispatching a real `input` event, so a toolbar press reaches
     the save machinery and the counter by the same path a keystroke does and
     neither has to know the toolbar exists. */
  function wrapSelection(field, before, after, sample) {
    var start = field.selectionStart;
    var end = field.selectionEnd;
    var body = field.value.slice(start, end) || sample;
    field.value = field.value.slice(0, start) + before + body + after + field.value.slice(end);
    field.focus();
    field.setSelectionRange(start + before.length, start + before.length + body.length);
    field.dispatchEvent(new Event('input', { bubbles: true }));
  }

  function prefixLines(field, prefix, sample) {
    var value = field.value;
    var from = value.lastIndexOf('\n', field.selectionStart - 1) + 1;
    var to = value.indexOf('\n', field.selectionEnd);
    if (to === -1) to = value.length;
    var block = value.slice(from, to) || sample;
    var written = block.split('\n').map(function (line) { return prefix + line; }).join('\n');
    field.value = value.slice(0, from) + written + value.slice(to);
    field.focus();
    field.setSelectionRange(from, from + written.length);
    field.dispatchEvent(new Event('input', { bubbles: true }));
  }

  /* The heading button cycles rather than pinning one level, which the
     reference does not: theirs is hard-wired to `###`, so an H1 or an H2 means
     typing the hashes by hand and the button is no help at the two levels a
     note most wants. Four presses walk `#`, `##`, `###` and back to plain, so
     there is no level the button cannot reach and none it cannot leave. */
  function cycleHeading(field) {
    var value = field.value;
    var from = value.lastIndexOf('\n', field.selectionStart - 1) + 1;
    var to = value.indexOf('\n', field.selectionStart);
    if (to === -1) to = value.length;
    var line = value.slice(from, to);
    var worn = line.match(/^(#{1,3})\s+/);
    var body = worn ? line.slice(worn[0].length) : line;
    var next = worn && worn[1].length >= 3 ? '' : new Array((worn ? worn[1].length : 0) + 2).join('#') + ' ';
    var written = next + (body || 'Heading');
    field.value = value.slice(0, from) + written + value.slice(to);
    field.focus();
    field.setSelectionRange(from + next.length, from + written.length);
    field.dispatchEvent(new Event('input', { bubbles: true }));
  }

  /* A selection spanning more than one line wants a fence and a selection
     inside one line wants a span, because a fence around three words puts them
     on a plate of their own and a span around a function body loses every line
     break. The reference reads the selection the same way and it is right. */
  function insertCode(field) {
    var body = field.value.slice(field.selectionStart, field.selectionEnd);
    if (body.indexOf('\n') === -1) wrapSelection(field, '`', '`', 'code');
    else wrapSelection(field, '```\n', '\n```', body);
  }

  /* ============================================================
     THE PREVIEW, AND THE SUBSET IT RENDERS

     A hand-written renderer over a closed subset, for the same reason the rest
     of the hub has no build step: a markdown library is a dependency this
     repository does not take, and the subset a study note needs is small.

     What it renders is the hub's own widgets and never a second vocabulary. A
     callout in a note is `.callout`, `.callout.warn` and `.callout.key` - the
     three the lessons already use, tokenised across seven palettes and both
     modes - so a note looks like the page it was written beside and costs no
     colour of its own.

     Three deliberate departures from the reference, and each closes a defect
     research measured on the live site.

     `_underscores_` are not italics. Their renderer turns `user_id_field` into
     `user<em>id</em>field`, on a hub whose courses are about `top_p`,
     `--max_tokens` and `attention_mask`. Only `*asterisks*` italicise here.

     Every placeholder restore is a function replacement rather than a string
     one, so a code span containing `$&` or `$1` survives being put back.

     A link's scheme is on an allowlist. The document is the reader's own, so
     this is not a trust boundary, but a note pasted from somewhere else is not
     the reader's own and `javascript:` in it should render as text. */
  var NOTE_SAFE_LINK = /^(https?:|mailto:|#|\/|\.{1,2}\/)/i;
  var NOTE_ITEM = /^(\s*)([-*+]|\d+[.)])\s+(.*)$/;
  var NOTE_CALLOUT = /^\[!([a-z]+)\]\s*(.*)$/i;
  /* The placeholder a pulled-out code span leaves behind. A NUL is not on any
     keyboard and nothing else in this renderer treats it as a character, so it
     cannot collide with anything the reader wrote. */
  var NOTE_HOLD = '\u0000';
  var NOTE_HOLD_BACK = /\u0000(\d+)\u0000/g;

  /* Nine names onto the three widgets the hub has. A name it does not know
     falls through to a plain blockquote rather than to a fourth appearance. */
  var NOTE_CALLOUTS = {
    note: '', info: '', example: '',
    warning: 'warn', danger: 'warn', caution: 'warn',
    tip: 'key', key: 'key', important: 'key'
  };

  function escapeText(text) {
    return String(text).replace(/[&<>"]/g, function (ch) {
      if (ch === '&') return '&amp;';
      if (ch === '<') return '&lt;';
      if (ch === '>') return '&gt;';
      return '&quot;';
    });
  }

  function renderInline(text) {
    var spans = [];
    /* Code comes out first and goes back last, so nothing in between rewrites
       what is inside a span. */
    var work = String(text).replace(/`([^`]+)`/g, function (whole, span) {
      spans.push(span);
      return NOTE_HOLD + (spans.length - 1) + NOTE_HOLD;
    });
    work = escapeText(work);
    work = work.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    work = work.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    work = work.replace(/==([^=]+)==/g, '<mark>$1</mark>');
    work = work.replace(/~~([^~]+)~~/g, '<del>$1</del>');
    work = work.replace(/\[([^\]]*)\]\(([^)\s]+)\)/g, function (whole, label, href) {
      if (!NOTE_SAFE_LINK.test(href)) return whole;
      return '<a href="' + href + '" rel="noreferrer">' + (label || href) + '</a>';
    });
    return work.replace(NOTE_HOLD_BACK, function (whole, index) {
      return '<code>' + escapeText(spans[Number(index)]) + '</code>';
    });
  }

  function noteIndent(space) { return space.replace(/\t/g, '  ').length; }

  /* One list, and every list nested under it. A deeper line belongs to the
     item above it rather than to a list of its own, which is the reference's
     most visible gap: theirs renders every item as an independent flat row, so
     a two-level outline arrives with no outline at all. */
  function renderList(lines, start, indent) {
    var opening = lines[start].match(NOTE_ITEM);
    var ordered = /\d/.test(opening[2]);
    var items = [];
    var at = start;
    while (at < lines.length) {
      var item = lines[at].match(NOTE_ITEM);
      if (!item) break;
      var width = noteIndent(item[1]);
      if (width < indent) break;
      if (width > indent) {
        if (!items.length) break;
        var deeper = renderList(lines, at, width);
        items[items.length - 1].html += deeper.html;
        at = deeper.next;
        continue;
      }
      if (/\d/.test(item[2]) !== ordered) break;
      var task = item[3].match(/^\[([ xX])\]\s*(.*)$/);
      if (task) {
        var done = task[1] !== ' ';
        items.push({
          cls: ' class="notes-task"',
          /* The box is a glyph and the state is a word, because the glyph
             carries the whole of the information and a screen reader cannot
             say it. It is not a checkbox: a preview that offered one would be
             offering to change a document it is not editing. */
          html: '<span class="notes-box" aria-hidden="true">' + (done ? '☑' : '☐') + '</span>'
            + '<span class="sr-only">' + (done ? 'Done: ' : 'To do: ') + '</span>'
            + renderInline(task[2])
        });
      } else {
        items.push({ cls: '', html: renderInline(item[3]) });
      }
      at += 1;
    }
    var tag = ordered ? 'ol' : 'ul';
    var body = items.map(function (item) { return '<li' + item.cls + '>' + item.html + '</li>'; }).join('');
    return { html: '<' + tag + ' class="notes-list">' + body + '</' + tag + '>', next: at };
  }

  function renderQuote(lines, start) {
    var body = [];
    var at = start;
    while (at < lines.length && /^\s*>/.test(lines[at])) {
      body.push(lines[at].replace(/^\s*>\s?/, ''));
      at += 1;
    }
    var head = body.length ? body[0].match(NOTE_CALLOUT) : null;
    var kind = head ? NOTE_CALLOUTS[head[1].toLowerCase()] : undefined;
    if (kind === undefined) {
      return { html: '<blockquote>' + renderBlocks(body) + '</blockquote>', next: at };
    }
    return {
      html: '<div class="' + (kind ? 'callout ' + kind : 'callout') + '">'
        + '<span class="tag">' + escapeText(head[2] || head[1]) + '</span>'
        + renderBlocks(body.slice(1)) + '</div>',
      next: at
    };
  }

  /* Headings start at `h3`. The panel's own title is the `h2` a dialog's name
     has to be, so a note's own `#` sits under it and the outline a screen
     reader walks stays in order. How big each one looks is the stylesheet's,
     which is the tag-and-size split the hub states everywhere else. */
  function renderBlocks(lines) {
    var out = [];
    var at = 0;
    while (at < lines.length) {
      var line = lines[at];
      if (/^\s*```/.test(line)) {
        var code = [];
        at += 1;
        while (at < lines.length && !/^\s*```/.test(lines[at])) { code.push(lines[at]); at += 1; }
        at += 1;   // the closing fence, or the end of the document
        out.push('<pre><code>' + escapeText(code.join('\n')) + '</code></pre>');
        continue;
      }
      if (/^\s*>/.test(line)) {
        var quote = renderQuote(lines, at);
        out.push(quote.html);
        at = quote.next;
        continue;
      }
      var head = line.match(/^(#{1,4})\s+(.*)$/);
      if (head) {
        var level = head[1].length + 2;
        out.push('<h' + level + '>' + renderInline(head[2]) + '</h' + level + '>');
        at += 1;
        continue;
      }
      if (/^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(line)) { out.push('<hr>'); at += 1; continue; }
      var item = line.match(NOTE_ITEM);
      if (item) {
        var list = renderList(lines, at, noteIndent(item[1]));
        out.push(list.html);
        at = list.next;
        continue;
      }
      if (!line.trim()) { at += 1; continue; }
      var para = [];
      while (at < lines.length && lines[at].trim()
        && !/^\s*(>|```|#{1,4}\s)/.test(lines[at]) && !NOTE_ITEM.test(lines[at])) {
        para.push(lines[at]);
        at += 1;
      }
      out.push('<p>' + renderInline(para.join('\n')).replace(/\n/g, '<br>') + '</p>');
    }
    return out.join('');
  }

  function renderNote(source) {
    return renderBlocks(String(source).replace(/\r\n?/g, '\n').split('\n'));
  }

  /* ---------- what the reader takes away ----------
     Front matter first, then the document as it stands in the editor rather
     than as it stands in storage: the whole point of the button on a failed
     write is that storage is exactly what cannot be trusted.

     The guard on an existing front-matter block is a real one. The reference
     tests `content.trim().indexOf('---') === 0`, so a note that opens with a
     horizontal rule is mistaken for a note that already carries front matter
     and is exported with none. A block is a fence, a body and a closing fence,
     and that is what this asks for. */
  var NOTE_FRONT = /^---\r?\n[\s\S]*?\r?\n---(\r?\n|$)/;

  function yamlString(text) { return '"' + String(text).replace(/"/g, '\\"') + '"'; }

  function exportBody(scope, text) {
    if (NOTE_FRONT.test(text)) return text;
    var today = new Date();
    var day = today.getFullYear()
      + '-' + ('0' + (today.getMonth() + 1)).slice(-2)
      + '-' + ('0' + today.getDate()).slice(-2);
    return [
      '---',
      'title: ' + yamlString(document.title),
      'scope: ' + yamlString(scope.label),
      (scope.keyName || 'notes-key') + ': ' + yamlString(scope.store),
      'source: ' + yamlString(location.href),
      'exported: ' + day,
      '---',
      '',
      text.replace(/\s*$/, ''),
      ''
    ].join('\n');
  }

  /* The anchor is put in the document before it is clicked and the object URL
     is revoked on the next turn of the loop. The reference does neither - it
     clicks a detached anchor and revokes on the very next line - and both are
     races a browser is entitled to lose on a large document. */
  function downloadMarkdown(name, body) {
    var url = URL.createObjectURL(new Blob([body], { type: 'text/markdown;charset=utf-8' }));
    var link = el('a');
    link.href = url;
    link.download = name;
    link.hidden = true;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 0);
  }

  /* Counted over the markdown the reader wrote rather than over the rendered
     prose, which is what the `title` on the readout says out loud: a count
     that silently meant one of the two would be wrong for whoever assumed the
     other. */
  function noteCount(text) {
    var words = text.trim() ? text.trim().split(/\s+/).length : 0;
    return words + (words === 1 ? ' word, ' : ' words, ')
      + text.length + (text.length === 1 ? ' character' : ' characters');
  }

  function clockStamp() {
    var now = new Date();
    return ('0' + now.getHours()).slice(-2) + ':' + ('0' + now.getMinutes()).slice(-2);
  }

  function buildNotesPanel() {
    var scopes = noteScopes();
    var scope = scopes[0];
    var chosen = get(STORE.noteScope);
    scopes.forEach(function (item) { if (item.key === chosen) scope = item; });

    var view = NOTE_VIEWS[0].key;
    var timer = null;
    var ceiling = 0;

    /* What the editor holds, per scope, for this page load. Storage is the
       durable copy and this is the live one, and the live one wins: a read
       that put storage over the top of the editor is loss path (d) in the
       reference, where saving a highlight rewrites the textarea from a
       document that predates whatever the reader has just typed. Nothing here
       reads storage over text the reader can still see, so a failed write
       leaves the words on screen for Export to take away. */
    var drafts = {};

    var shell = makePanel({
      name: 'notes',
      className: 'notes',
      title: 'Study notes',
      closeLabel: 'Close study notes',
      storeKey: STORE.notePanel,
      foot: true,
      onOpen: function () { load(scope); },
      onClose: function () { flush(); }
    });
    var body = shell.body;

    /* ---------- 1. which document ---------- */
    var scopeField = el('div', 'notes-field');
    var scopeLabel = el('span', 'notes-lbl', 'Notes for');
    scopeLabel.id = 'notes-scope-label';
    var scopeCards = segmented('scope', scopes, function (key) { switchScope(key); });
    scopeCards.setAttribute('role', 'group');
    scopeCards.setAttribute('aria-labelledby', scopeLabel.id);
    var where = el('p', 'notes-where');
    scopeField.appendChild(scopeLabel);
    scopeField.appendChild(scopeCards);
    scopeField.appendChild(where);
    body.appendChild(scopeField);

    /* ---------- 2. write or read ---------- */
    var viewField = el('div', 'notes-field');
    var viewLabel = el('span', 'sr-only', 'Editor view');
    viewLabel.id = 'notes-view-label';
    var viewCards = segmented('view', NOTE_VIEWS, function (key) { switchView(key); });
    viewCards.setAttribute('role', 'group');
    viewCards.setAttribute('aria-labelledby', viewLabel.id);
    viewField.appendChild(viewLabel);
    viewField.appendChild(viewCards);
    body.appendChild(viewField);

    /* ---------- 3. the toolbar ---------- */
    var tools = el('div', 'notes-tools');
    tools.setAttribute('role', 'toolbar');
    tools.setAttribute('aria-label', 'Formatting');
    NOTE_TOOLS.forEach(function (tool) {
      var button = el('button', 'notes-tool');
      button.type = 'button';
      button.dataset.tool = tool.key;
      button.setAttribute('aria-label', tool.name + (tool.keys ? ', ' + tool.keys : ''));
      button.title = tool.name + (tool.keys ? ' (' + tool.keys + ')' : '');
      var glyph = el('span', null, tool.glyph);
      glyph.setAttribute('aria-hidden', 'true');
      button.appendChild(glyph);
      button.addEventListener('click', function () { applyTool(tool); });
      tools.appendChild(button);
    });
    body.appendChild(tools);

    /* ---------- 4. the editor, and the preview in its place ---------- */
    var field = el('textarea', 'notes-edit');
    field.setAttribute('aria-label', 'Study notes, in Markdown');
    field.placeholder = 'Write here. Markdown: # heading, - list, **bold**, `code`, > [!tip] callout.';
    body.appendChild(field);

    var preview = el('div', 'notes-view');
    preview.hidden = true;
    body.appendChild(preview);

    /* ---------- 5. the truth, the count, and the way out ----------
       The foot is pinned to the panel rather than put in the scrolling body,
       which is the one place this panel departs from the appearance panel's
       shape and it is the save state that earns it: a reader whose write has
       just failed must not have to scroll to find that out, and the button
       that gets their words back out must not be the thing below the fold. It
       is the shell's `panel-foot` rather than this panel's own, because the
       highlighter needs the identical thing and two of them would drift. */
    var foot = shell.foot;
    foot.classList.add('notes-foot');
    var state = el('p', 'panel-state');
    state.setAttribute('role', 'status');
    var count = el('p', 'notes-count');
    count.title = 'Counted over the Markdown you wrote, not over the rendered preview.';
    var take = el('button', 'panel-export');
    take.type = 'button';
    take.textContent = 'Export Markdown';
    take.addEventListener('click', function () {
      downloadMarkdown(scope.file + '-notes.md', exportBody(scope, field.value));
    });
    foot.appendChild(state);
    foot.appendChild(count);
    foot.appendChild(take);

    /* The state is never more than what happened, and how it is painted is the
       shell's - see `saveState` above, which the highlighter reads too. */
    var say = saveState(state, take);

    function tally() {
      count.textContent = noteCount(field.value);
      take.disabled = !field.value.trim();
    }

    function commit() {
      window.clearTimeout(timer);
      timer = null;
      ceiling = 0;
      var text = field.value;
      drafts[scope.store] = text;
      var kept = text.trim() ? setChecked(scope.store, text) : dropChecked(scope.store);
      if (kept) say('saved', 'Saved ' + clockStamp());
      else say('failed', saveFailure('this'));
      return kept;
    }

    function flush() { if (timer) commit(); }

    function schedule() {
      var now = Date.now();
      if (!ceiling) ceiling = now + NOTE_LATEST;
      window.clearTimeout(timer);
      timer = window.setTimeout(commit, Math.max(0, Math.min(NOTE_SETTLE, ceiling - now)));
      say('saving', 'Saving');
    }

    /* ---------- loading, which never runs over the reader ---------- */
    function load(next) {
      scope = next;
      var draft = drafts[scope.store];
      field.value = draft === undefined ? (get(scope.store) || '') : draft;
      where.textContent = scope.store;
      pressGroup(shell.el, 'scope', scope.key);
      pressGroup(shell.el, 'view', view);
      tally();
      if (!storageAccepts()) {
        say('failed', saveFailure('this'));
      } else if (field.value) {
        say('saved', 'Saved earlier in this browser.');
      } else {
        say('idle', 'Nothing written for ' + scope.label.toLowerCase() + ' yet.');
      }
    }

    function switchScope(key) {
      if (key === scope.key) return;
      /* The document on screen is written before the other is read, so a
         scope change can never be the thing that loses a paragraph. If that
         write fails the draft is still held in memory, which is why `drafts`
         is keyed by store and never cleared. */
      flush();
      drafts[scope.store] = field.value;
      scopes.forEach(function (item) { if (item.key === key) load(item); });
      set(STORE.noteScope, scope.key);
      if (view === 'read') preview.innerHTML = renderNote(field.value);
    }

    function switchView(key) {
      view = key;
      var reading = key === 'read';
      if (reading) preview.innerHTML = renderNote(field.value);
      preview.hidden = !reading;
      field.hidden = reading;
      pressGroup(shell.el, 'view', view);
    }

    function applyTool(tool) {
      /* A formatting press in Preview means the reader wants to write, so the
         panel goes back to the editor rather than doing nothing visible. */
      if (view === 'read') switchView('write');
      if (tool.key === 'heading') cycleHeading(field);
      else if (tool.key === 'code') insertCode(field);
      else if (tool.wrap) wrapSelection(field, tool.wrap[0], tool.wrap[1], tool.sample);
      else prefixLines(field, tool.line, tool.sample);
    }

    field.addEventListener('input', function () { tally(); schedule(); });
    /* Leaving the field is a pause the reader can see, so it commits. Tab is
       bound to nothing here on purpose: the reference indents with it, which
       makes the editor a keyboard trap and fails WCAG 2.1.2, and this panel is
       walked with real Tab keys by `scripts/focus_walk.py`. */
    field.addEventListener('blur', flush);
    field.addEventListener('keydown', function (event) {
      if (!(event.metaKey || event.ctrlKey) || event.altKey) return;
      var key = event.key.toLowerCase();
      if (key === 's') { event.preventDefault(); commit(); return; }
      if (event.shiftKey) {
        if (key === 'c') { event.preventDefault(); insertCode(field); }
        return;
      }
      if (key === 'b') { event.preventDefault(); wrapSelection(field, '**', '**', 'bold text'); }
      else if (key === 'i') { event.preventDefault(); wrapSelection(field, '*', '*', 'italic text'); }
    });

    /* The two exits the reference has neither of. A keystroke followed inside
       the debounce by a link click, a tab close, a background switch or the
       browser's own back button is written rather than lost. */
    document.addEventListener('visibilitychange', function () {
      if (document.visibilityState === 'hidden') flush();
    });
    window.addEventListener('pagehide', flush);

    load(scope);
    return shell;
  }

  /* ============================================================
     THE TEXT HIGHLIGHTER

     A reader marks the sentence that mattered and finds it marked when they
     come back. It is chrome, exactly as the two panels above are: no page in
     the hub names it, no lesson markup changes, and a page served with the
     script blocked has no control, no panel and no trace.

     ---------- what a highlight is DRAWN with ----------
     The browser's own highlight mechanism - `CSS.highlights` and the
     `::highlight()` pseudo-element - and never a wrapper element around the
     words. The alternative is to split the text nodes a selection crosses and
     put a `<mark>` around each piece, which is how this feature is usually
     built and is why it usually breaks:

       a  It rewrites the prose. A sentence a screen reader read as one string
          becomes three, and a reader on VoiceOver or NVDA hears the sentence
          in fragments with a pause at each seam. That is the whole of user
          story 7 and it is the defect the specification asked to avoid.
       b  It is a live edit of a document other code holds references into: the
          section rail has put ids on the headings, Mermaid re-renders on every
          palette change, and the print pass copies the page. A splitter has to
          be right about all of them.
       c  It cannot be undone cleanly. Removing a mark means merging text nodes
          back, and a page marked and unmarked twenty times is a page whose DOM
          no longer matches its source.

     A range highlight has none of those properties. The DOM is byte-identical
     before and after, the paint is thrown away and rebuilt from the anchors
     whenever anything moves, and the worst failure available to it is a mark
     that does not appear.

     What it costs is that a `::highlight()` mark carries no semantics: there is
     no element, so there is nothing in the accessibility tree to announce and a
     screen reader is not told the words are marked. That trade is made on
     purpose and the panel below is the answer to it - it lists every mark on
     the page as text, in reading order, which is what a screen reader reads
     instead of a shredded sentence.

     Where the API is missing there is no button, no panel, no cue and no
     keyboard path: the feature is simply not on that browser. It does not fall
     back to splitting the DOM, because the fallback is the defect.

     ---------- THE ANCHORING CONTRACT ----------
     A highlight is a reference into text that can change under it, so where it
     lands on return is the whole design.

     THE DOMAIN. The page's own prose, flattened to one string: every text node
     under `main.wrap` or `main.wide`, in document order, with each run of
     whitespace collapsed to a single space. Five things are left out of it and
     each has a reason - `script` and `style` are not prose, `svg` and
     `.mermaid` are drawings whose text is replaced when they render, form
     controls and buttons are chrome inside the column, `.sr-only` is text no
     sighted reader can select, and anything `hidden` or `aria-hidden` is not on
     the page. Collapsing whitespace is what makes the domain the text the
     reader sees rather than the file's indentation, so re-wrapping the source
     of a lesson moves nothing.

     WHAT IS STORED. Four fields and no ids into the DOM: the exact quote, the
     offset it was taken from, and up to 48 characters of the text either side
     of it. That is a position selector and a quote selector with context, which
     is the shape the W3C Web Annotation model settled on for the same reason.

     HOW IT IS PLACED ON RETURN, in order, and every step is an EXACT match:

       1  The offset it was saved at. If the domain carries the quote at exactly
          that offset, that is the highlight. This is the whole of the cost on a
          page nobody has edited.
       2  The quote inside the context it was taken from. Otherwise the domain
          is searched for `before + quote + after`. If it occurs EXACTLY ONCE,
          that is the highlight. This is what survives an edit somewhere else on
          the page: a new paragraph above moves every offset below it and moves
          no words.
       3  The quote on its own. Otherwise the domain is searched for the quote.
          If it occurs EXACTLY ONCE, that is the highlight. This is what
          survives an edit to the sentences either side of the marked one.
       4  Nothing. The highlight is not painted. It stays in storage and it is
          listed in the panel, in full, under `Not placed`.

     WHAT MAKES IT FAIL, deliberately. Two or more occurrences at any step is an
     ambiguity, and an ambiguity is a failure rather than a guess: a mark placed
     on the wrong one of two identical sentences is a mark the reader will trust
     and should not. There is no fuzzy match, no nearest match and no edit
     distance anywhere in this file. A highlight that no longer fits FAILS
     VISIBLY rather than landing on the wrong words, because a silently
     misplaced highlight - marking the wrong sentence with complete confidence -
     is worse than one that openly did not come back. The panel says which
     highlights did not place, quotes the words they were made of so the reader
     can find them by eye, and offers to remove them; restoring the paragraph
     restores the mark, because nothing was thrown away.

     PLACEMENT NEVER WRITES. Re-anchoring through step 2 or 3 does not rewrite
     the stored offset. A load that quietly rewrote storage could report a write
     failure the reader did not cause, and the search it saves is a few
     milliseconds on a page the reader is already reading.

     ---------- a selection that crosses element boundaries ----------
     The domain is one string over the whole content region, so a selection that
     spans a paragraph break, a list, a code block or a figure caption is ONE
     highlight with one anchor, and the browser paints it across every element
     it crosses. Nothing in the DOM is touched, so there is no partial mark and
     no broken markup available here at all. The block boundary itself collapses
     to a single space in the domain, so the stored quote reads
     `...end of one. Start of the next...`.

     A selection is clipped to the content region: the part of it inside the
     region is marked and the part outside is dropped. A selection with no prose
     in it at all - one made entirely inside a diagram, or in the chrome - is
     refused, and the panel says so rather than storing a mark that can never
     paint.

     ---------- overlaps ----------
     A stroke over words that are already marked MERGES with them, so the reader
     ends with one highlight over the union rather than two stacked ones. That
     is what a marker pen does. Removing that highlight removes the whole of the
     merged run, which is the same rule read backwards.

     ---------- the two ways in, and the keyboard ----------
     A pointer reader gets a cue over the selection. A keyboard reader gets the
     panel: the last selection made inside the content region is held, so
     opening the panel and pressing its first button marks it whatever the
     selection did when focus moved. That is why there is no global shortcut
     key - a single-character one is an SC 2.1.4 problem, and every free
     modifier combination is taken by a browser on some platform - and it is
     why the button acts on a held anchor rather than on the live selection.
     ============================================================ */

  /* The characters of context stored either side of a quote. Long enough that
     `before + quote + after` is unique in a lesson-length page, short enough
     that a page's worth of highlights is a few kilobytes. */
  var MARK_CONTEXT = 48;
  /* The pause after the reader stops moving a selection. A drag fires
     `selectionchange` on every pixel and the cue must not follow the pointer. */
  var MARK_SETTLE = 120;
  /* How much of a quote a control's accessible name carries. A button whose
     name is a whole paragraph is a button nobody can listen to. */
  var MARK_LABEL = 60;
  var MARK_EDGE = 8;               // the gap the cue keeps from every edge
  var MARK_PAINT = 'coursehub-mark';
  var MARK_PAINT_ON = 'coursehub-mark-on';

  /* Not prose, and none of it is selectable text a reader means to mark.
     `.mermaid` is here rather than in the tag list because before it renders it
     is a div full of graph source, and after it renders it is an svg: a domain
     that included it would move under every palette change. */
  var MARK_SKIP_TAGS = /^(SCRIPT|STYLE|SVG|NOSCRIPT|TEXTAREA|INPUT|SELECT|BUTTON)$/;
  var MARK_SKIP_CLASS = /(^|\s)(sr-only|mermaid)(\s|$)/;

  function markSupported() {
    return !!(window.CSS && window.CSS.highlights && window.Highlight);
  }

  /* The same region the in-page section rail derives from, so the two chrome
     features cannot disagree about where a page's content begins. */
  function markRegion() { return document.querySelector('main.wrap, main.wide'); }

  function markSkipped(node, region) {
    var parent = node.parentElement;
    while (parent && parent !== region) {
      if (MARK_SKIP_TAGS.test(parent.tagName)) return true;
      if (parent.hidden || parent.getAttribute('aria-hidden') === 'true') return true;
      if (MARK_SKIP_CLASS.test(parent.className || '')) return true;
      parent = parent.parentElement;
    }
    return false;
  }

  /* ---------- the domain, and the map back into the DOM ----------
     `text` is what an anchor is stated in. `owner` and `at` say, for every
     character of it, which text node it came from and where in that node, which
     is what turns a pair of offsets back into a Range the browser can paint.
     `spans` is the same map the other way round, one entry per text node, which
     is what turns a Range the reader made into a pair of offsets. */
  function markIndex() {
    var region = markRegion();
    if (!region) return null;
    var walker = document.createTreeWalker(region, NodeFilter.SHOW_TEXT, null);
    var text = '';
    var owner = [];
    var at = [];
    var spans = [];
    var node;
    // True to start with, so leading whitespace never becomes character zero.
    var space = true;
    while ((node = walker.nextNode())) {
      var value = node.nodeValue;
      if (!value || markSkipped(node, region)) continue;
      var from = owner.length;
      for (var i = 0; i < value.length; i++) {
        var ch = value.charAt(i);
        var blank = ch === ' ' || ch === '\n' || ch === '\t' || ch === '\r' || ch === '\f';
        if (blank && space) continue;
        text += blank ? ' ' : ch;
        space = blank;
        owner.push(node);
        at.push(i);
      }
      if (owner.length > from) spans.push({ node: node, from: from, to: owner.length });
    }
    return { region: region, text: text, owner: owner, at: at, spans: spans };
  }

  function markRange(index, from, to) {
    if (!index || from < 0 || to <= from || to > index.owner.length) return null;
    var range = document.createRange();
    range.setStart(index.owner[from], index.at[from]);
    range.setEnd(index.owner[to - 1], index.at[to - 1] + 1);
    return range;
  }

  function markHeadOf(index, span, offset) {
    for (var i = span.from; i < span.to; i++) if (index.at[i] >= offset) return i;
    return span.to;
  }

  function markTailOf(index, span, offset) {
    for (var i = span.to - 1; i >= span.from; i--) if (index.at[i] < offset) return i + 1;
    return span.from;
  }

  /* A Range the reader made, in the domain's own offsets, clipped to the region.
     Every text node the range touches is asked for its own overlap, so a
     selection that starts in the chrome or ends inside a diagram contributes
     the part of itself that is prose and nothing else. */
  function markBounds(index, range) {
    var from = null;
    var to = null;
    index.spans.forEach(function (span) {
      if (!range.intersectsNode(span.node)) return;
      var head = range.startContainer === span.node ? range.startOffset : 0;
      var tail = range.endContainer === span.node ? range.endOffset : span.node.nodeValue.length;
      if (tail <= head) return;
      var a = markHeadOf(index, span, head);
      var b = markTailOf(index, span, tail);
      if (b <= a) return;
      if (from === null || a < from) from = a;
      if (to === null || b > to) to = b;
    });
    return from === null ? null : { from: from, to: to };
  }

  /* The four stored fields, taken from a pair of offsets. The edges are trimmed
     first: a reader who drags past the end of a sentence has selected the space
     after it, and a quote that begins or ends in whitespace is a quote whose
     context match is decided by trailing spaces. */
  function markAnchorAt(index, from, to) {
    var raw = index.text.slice(from, to);
    var body = raw.replace(/^\s+/, '');
    var head = from + (raw.length - body.length);
    body = body.replace(/\s+$/, '');
    if (!body) return null;
    return {
      text: body,
      start: head,
      before: index.text.slice(Math.max(0, head - MARK_CONTEXT), head),
      after: index.text.slice(head + body.length, head + body.length + MARK_CONTEXT)
    };
  }

  /* Exactly once, or nowhere. A second occurrence is what makes step 2 and step
     3 of the contract refuse rather than pick, and it is the whole of the
     promise that a highlight never lands on the wrong words. */
  function markOnly(haystack, needle) {
    if (!needle) return -1;
    var first = haystack.indexOf(needle);
    if (first < 0) return -1;
    return haystack.indexOf(needle, first + 1) < 0 ? first : -1;
  }

  /* The contract, in the order the block above states it. */
  function markPlace(index, anchor) {
    var quote = anchor.text;
    var length = quote.length;
    if (!length) return null;
    if (index.text.slice(anchor.start, anchor.start + length) === quote) {
      return { from: anchor.start, to: anchor.start + length, how: 'position' };
    }
    var context = anchor.before + quote + anchor.after;
    var found = markOnly(index.text, context);
    if (found >= 0) {
      var head = found + anchor.before.length;
      return { from: head, to: head + length, how: 'context' };
    }
    found = markOnly(index.text, quote);
    if (found >= 0) return { from: found, to: found + length, how: 'quote' };
    return null;
  }

  /* ---------- where a page's highlights live ----------
     Beside the notes panel's, and on the same identifier: `coursehub.mark:`
     plus the tier and the course key and file name that `pageKey` derives, so a
     note and a highlight on one page can never disagree about what a page is.
     One key per page holding one JSON array, which is the same "one key per
     document" the notes panel keeps - a page's marks are the document here, and
     nothing has to read or rewrite another page's key in order to save one. */
  function markStore() { return MARK_PREFIX + 'page:' + pageKey(); }

  function markRead() {
    var raw = get(markStore());
    if (!raw) return [];
    var parsed;
    try { parsed = JSON.parse(raw); } catch (e) { return []; }
    if (!Array.isArray(parsed)) return [];
    /* Storage is the reader's own and is not a trust boundary, but it is the
       one input this file does not write itself: a hand-edited key, or one left
       by a future version, must not be able to throw on the way in. */
    return parsed
      .filter(function (item) { return item && typeof item.text === 'string' && item.text; })
      .map(function (item) {
        return {
          text: item.text,
          start: typeof item.start === 'number' && item.start >= 0 ? item.start : 0,
          before: typeof item.before === 'string' ? item.before : '',
          after: typeof item.after === 'string' ? item.after : ''
        };
      });
  }

  function markShorten(text, limit) {
    return text.length > limit ? text.slice(0, limit - 1).replace(/\s+\S*$/, '') + '…' : text;
  }

  function buildHighlighter() {
    /* The anchors, in the order they were made, which is the order they are
       stored in. A row's identity is its position in this array: the array is
       only ever replaced whole, so there is no id to keep in step with it. */
    var anchors = markRead();
    /* One entry per anchor, in the same order, holding what placing it found.
       Rebuilt from the page whenever anything moves and never stored. */
    var placed = [];
    /* The last selection the reader made inside the content region, held as an
       anchor. This is what the panel's button marks, so the keyboard path does
       not depend on a selection surviving a change of focus. */
    var pending = null;
    /* Which row the panel is pointing at, or -1. Painted one step above the
       others so a reader who pressed Show on one of four marks in a paragraph
       can see which one answered. */
    var showing = -1;
    var watch = null;

    var shell = makePanel({
      name: 'marks',
      className: 'marks',
      title: 'Highlights',
      closeLabel: 'Close highlights',
      storeKey: STORE.markPanel,
      foot: true,
      onOpen: function () { replace(); render(); }
    });
    var body = shell.body;

    /* ---------- 1. the keyboard path, and the only control that acts ---------- */
    var make = el('button', 'panel-do');
    make.type = 'button';
    make.textContent = 'Highlight the selected text';
    make.addEventListener('click', function () { add(); });
    body.appendChild(make);

    /* The words the button will mark, said under it and pointed at from it, so
       a screen reader announces the button and what it is about to act on
       together rather than leaving the second sentence to be found. */
    var chosen = el('p', 'mark-chosen');
    chosen.id = 'marks-chosen';
    make.setAttribute('aria-describedby', chosen.id);
    body.appendChild(chosen);

    /* ---------- 2. what is on this page ---------- */
    var tally = el('p', 'mark-tally');
    tally.id = 'marks-tally';
    body.appendChild(tally);

    /* A list of quotations, named by the line that counts them, so a screen
       reader reaching it is told what it is a list of. */
    var list = el('ol', 'mark-list');
    list.setAttribute('aria-labelledby', tally.id);
    body.appendChild(list);

    /* ---------- 3. the truth, and the way out ---------- */
    var state = el('p', 'panel-state');
    state.setAttribute('role', 'status');
    var take = el('button', 'panel-export');
    take.type = 'button';
    take.textContent = 'Export Markdown';
    take.addEventListener('click', function () {
      downloadMarkdown(markFile() + '-highlights.md', markExport());
    });
    shell.foot.appendChild(state);
    shell.foot.appendChild(take);
    var say = saveState(state, take);

    /* ---------- the cue, which is the pointer path ----------
       Inserted straight after the topbar for the same reason the cluster is,
       and `mousedown` is prevented on it so that pressing it does not collapse
       the selection it is about to mark. */
    var cue = el('div', 'mark-cue');
    cue.hidden = true;
    var cueBtn = el('button', 'mark-cue-btn');
    cueBtn.type = 'button';
    cueBtn.textContent = 'Highlight';
    cueBtn.addEventListener('mousedown', function (event) { event.preventDefault(); });
    cueBtn.addEventListener('click', function () { add(); });
    cue.appendChild(cueBtn);

    function markFile() {
      return (courseKey() || 'hub') + '-'
        + (fileOf(location.pathname) || 'index.html').replace(/\.html?$/i, '');
    }

    /* ---------- placing, painting, and the order they are shown in ---------- */
    function replace() {
      var index = markIndex();
      placed = anchors.map(function (anchor) {
        var spot = index ? markPlace(index, anchor) : null;
        return {
          from: spot ? spot.from : -1,
          how: spot ? spot.how : '',
          range: spot ? markRange(index, spot.from, spot.to) : null
        };
      });
      if (!placed[showing] || !placed[showing].range) showing = -1;
      paint();
    }

    function paint() {
      var marks = new window.Highlight();
      placed.forEach(function (item) { if (item.range) marks.add(item.range); });
      if (marks.size) window.CSS.highlights.set(MARK_PAINT, marks);
      else window.CSS.highlights.delete(MARK_PAINT);

      var one = placed[showing];
      if (one && one.range) {
        var focus = new window.Highlight(one.range);
        focus.priority = 1;
        window.CSS.highlights.set(MARK_PAINT_ON, focus);
      } else {
        window.CSS.highlights.delete(MARK_PAINT_ON);
      }
    }

    /* Reading order, which is what makes the list a study aid rather than a
       log. A highlight that did not place has no position on the page, so it
       goes after the ones that did, in the order it was made. */
    function ordered() {
      return anchors
        .map(function (anchor, at) { return { anchor: anchor, at: at, spot: placed[at] }; })
        .sort(function (one, other) {
          var a = one.spot && one.spot.range ? one.spot.from : Infinity;
          var b = other.spot && other.spot.range ? other.spot.from : Infinity;
          if (a === b) return one.at - other.at;
          return a - b;
        });
    }

    /* ---------- the reader's three actions ---------- */
    function add() {
      if (!pending) return;
      var index = markIndex();
      /* The held selection is re-placed through the same contract a stored one
         is, against the page as it stands now. A reader who selected a sentence
         and then answered a quiz below it has moved every offset after the
         answer, and this is what makes the mark land anyway. */
      var spot = index ? markPlace(index, pending) : null;
      if (!spot) {
        say('failed', 'Nothing highlighted: those words are no longer on the page.');
        return;
      }
      var from = spot.from;
      var to = spot.to;
      var keep = [];
      /* Merged rather than stacked: a stroke that touches a mark becomes one
         mark over the union of the two, which is what a marker pen does and
         what makes Remove mean one thing. */
      placed.forEach(function (item, at) {
        if (item.range && item.from <= to && item.from + anchors[at].text.length >= from) {
          from = Math.min(from, item.from);
          to = Math.max(to, item.from + anchors[at].text.length);
        } else {
          keep.push(anchors[at]);
        }
      });
      var merged = markAnchorAt(index, from, to);
      if (!merged) {
        say('failed', 'Nothing highlighted: that selection holds no text.');
        return;
      }
      anchors = keep.concat([merged]);
      /* The new mark is not left in the pointed-at state. That state answers
         "which of these four is the one I pressed Show on", and a mark the
         reader has just made needs no answer to it: they are looking at it. */
      showing = -1;
      pending = null;
      hide();
      commit('Highlighted.');
    }

    function remove(at) {
      if (at < 0 || at >= anchors.length) return;
      var here = shell.el.contains(document.activeElement);
      anchors = anchors.slice(0, at).concat(anchors.slice(at + 1));
      showing = -1;
      commit('Removed.');
      /* The row the reader pressed is gone, so the focus that was on it has
         nowhere to return to. It goes to the panel's own first control rather
         than to <body>, which is where the browser would drop it. */
      if (here) make.focus();
    }

    /* Nothing here rebuilds the list. The reader has just pressed a button
       inside it, and replacing that button drops their focus to <body> and
       costs them their place in the tab order - which is the defect the quiz
       options were fixed for and is one line away in any panel built from
       data. Only the paint and the scroll position change. */
    function show(at) {
      var item = placed[at];
      if (!item || !item.range) return;
      showing = at;
      paint();
      var box = item.range.getBoundingClientRect();
      var spine = document.querySelector('.spine');
      var ceiling = (spine ? spine.getBoundingClientRect().height : 0) + MARK_EDGE * 2;
      window.scrollTo({ top: (window.scrollY || 0) + box.top - ceiling });
    }

    /* The write, and then the state that says what actually happened. The mark
       is painted either way: on a failed write the reader can still see it, and
       the sentence they are being told is that it will not survive the reload.
       That is the notes panel's rule, kept: never paint a save the store did not
       take. */
    function commit(did) {
      var kept = markWrite(anchors);
      replace();
      render();
      if (kept) say('saved', did + ' Saved ' + clockStamp() + '.');
      else say('failed', saveFailure('these'));
      return kept;
    }

    function markWrite(list) {
      var key = markStore();
      return list.length ? setChecked(key, JSON.stringify(list)) : dropChecked(key);
    }

    /* ---------- the list ---------- */
    function renderChosen() {
      make.disabled = !pending;
      chosen.textContent = pending
        ? 'Selected: “' + markShorten(pending.text, MARK_LABEL) + '”'
        : 'Select text in the page, then press the button above.';
    }

    function render() {
      renderChosen();
      var lost = placed.filter(function (item) { return !item.range; }).length;
      var total = anchors.length;
      if (!total) tally.textContent = 'Nothing highlighted on this page yet.';
      else {
        tally.textContent = total + (total === 1 ? ' highlight' : ' highlights') + ' on this page'
          + (lost ? ', ' + lost + ' not placed.' : '.');
      }

      list.textContent = '';
      list.hidden = !total;
      ordered().forEach(function (row) {
        var item = el('li', 'mark-row');
        var label = markShorten(row.anchor.text, MARK_LABEL);
        if (!row.spot || !row.spot.range) item.dataset.lost = 'yes';
        var quote = el('p', 'mark-quote', '“' + row.anchor.text + '”');
        item.appendChild(quote);
        if (!row.spot || !row.spot.range) {
          item.appendChild(el('p', 'mark-why',
            'Not placed: these words are no longer on the page, or the page now carries them twice.'));
        }
        var acts = el('div', 'mark-acts');
        if (row.spot && row.spot.range) {
          var find = el('button', 'mark-act');
          find.type = 'button';
          find.textContent = 'Show';
          find.setAttribute('aria-label', 'Show the highlight “' + label + '” in the page');
          find.addEventListener('click', function () { show(row.at); });
          acts.appendChild(find);
        }
        var drop = el('button', 'mark-act');
        drop.type = 'button';
        drop.textContent = 'Remove';
        drop.setAttribute('aria-label', 'Remove the highlight “' + label + '”');
        drop.addEventListener('click', function () { remove(row.at); });
        acts.appendChild(drop);
        item.appendChild(acts);
        list.appendChild(item);
      });

      take.disabled = !total;
    }

    /* ---------- export, which is what a failed write leaves the reader ----------
       Written from the anchors in memory rather than from storage, for the same
       reason the notes panel's is: a failed write is exactly the case where
       storage cannot be trusted. */
    function markExport() {
      var lines = [];
      ordered().forEach(function (row) {
        lines.push('> ' + row.anchor.text);
        if (!row.spot || !row.spot.range) {
          lines.push('>');
          lines.push('> *Not placed: these words are no longer on the page.*');
        }
        lines.push('');
      });
      return exportBody({
        label: 'This page',
        store: markStore(),
        keyName: 'highlights-key'
      }, lines.join('\n'));
    }

    /* ---------- the cue, and what the reader has selected ---------- */
    function hide() { cue.hidden = true; }

    function judge() {
      var selection = window.getSelection();
      if (!selection || !selection.rangeCount) { hide(); return; }
      if (selection.isCollapsed) {
        hide();
        /* A collapse inside the prose is the reader letting go of the words,
           and the held selection goes with it. A collapse anywhere else is not:
           moving focus to the topbar, opening the panel and pressing its button
           are the keyboard path, and clearing on any collapse would break it. */
        var region = markRegion();
        if (region && selection.anchorNode && region.contains(selection.anchorNode)) {
          pending = null;
          renderChosen();
        }
        return;
      }
      var range = selection.getRangeAt(0);
      var index = markIndex();
      var bounds = index ? markBounds(index, range) : null;
      var anchor = bounds ? markAnchorAt(index, bounds.from, bounds.to) : null;
      if (!anchor) { hide(); return; }
      pending = anchor;
      renderChosen();
      place(range);
    }

    /* Above the selection, clamped inside the band the reader can actually
       reach: under the sticky topbar, and above everything fixed across the
       foot, which `body`'s own padding already sums through `--foot-h`. A cue
       under the chapter bar is a cue the reader cannot press. */
    function place(range) {
      cue.hidden = false;
      var box = range.getBoundingClientRect();
      if (!box.width && !box.height) { hide(); return; }
      var spine = document.querySelector('.spine');
      var ceiling = (spine ? spine.getBoundingClientRect().bottom : 0) + MARK_EDGE;
      var floor = window.innerHeight - MARK_EDGE
        - parseFloat(getComputedStyle(document.body).paddingBottom || '0');
      var width = cue.offsetWidth;
      var height = cue.offsetHeight;
      var top = box.top - height - MARK_EDGE;
      if (top < ceiling) top = box.bottom + MARK_EDGE;
      top = Math.max(ceiling, Math.min(top, floor - height));
      var left = box.left + box.width / 2 - width / 2;
      left = Math.max(MARK_EDGE, Math.min(left, window.innerWidth - width - MARK_EDGE));
      cue.style.top = Math.round(top) + 'px';
      cue.style.left = Math.round(left) + 'px';
    }

    document.addEventListener('selectionchange', function () {
      window.clearTimeout(watch);
      watch = window.setTimeout(judge, MARK_SETTLE);
    });

    /* The cue is anchored to a rectangle in the viewport, so it follows the
       page rather than the document. Both are passive: this runs on every frame
       of a scroll. */
    function follow() {
      if (cue.hidden) return;
      var selection = window.getSelection();
      if (!selection || selection.isCollapsed || !selection.rangeCount) { hide(); return; }
      place(selection.getRangeAt(0));
    }
    window.addEventListener('scroll', follow, { passive: true });
    window.addEventListener('resize', follow);

    /* Web fonts, Mermaid and a quiz answer all change what the page holds, and
       a mark that could not be placed at parse time may place perfectly once
       the page has settled. Placing again is free and never writes. */
    window.addEventListener('load', function () { replace(); render(); });

    replace();
    render();
    if (!storageAccepts()) say('failed', saveFailure(''));
    else if (anchors.length) say('saved', 'Saved earlier in this browser.');
    else say('idle', 'Nothing highlighted on this page yet.');

    return { shell: shell, cue: cue };
  }

  /* ---------- the panel reads the page back, never its own memory ----------
     Every control's state is read off the attribute or the computed token that
     actually decides the page, so the panel and the page cannot disagree about
     what is on. A control that remembered what it drew would be right until the
     first time something else moved. */
  function pressGroup(scope, attribute, current) {
    var cards = scope.querySelectorAll('[data-' + attribute + ']');
    Array.prototype.forEach.call(cards, function (card) {
      if (card.tagName !== 'BUTTON') return;
      card.setAttribute('aria-pressed', String(card.dataset[attribute] === current));
    });
  }

  function syncGroup(attribute, current) {
    if (!appearance) return;
    pressGroup(appearance.el, attribute, current);
  }

  function syncSettings() {
    /* Before the early return, because the cluster is built whether or not the
       panel was and its mode control has to keep up with every path that moves
       the mode: the panel, the reset, and the cluster's own button. */
    syncCluster();
    if (!appearance) return;
    /* Four of these read an attribute straight off <html> and two read the
       chosen key, because a step whose value is "write nothing" leaves no trace
       on the element to read back. Two groups share the `.pal-card` shape, so
       each is asked for by the attribute that says which axis it selects: a
       bare `.pal-card` query would compare a design card's undefined palette
       against the live one and report every design as unpressed. */
    syncGroup('mode', root.getAttribute('data-mode') || '');
    syncGroup('palette', root.getAttribute('data-palette'));
    syncGroup('design', root.getAttribute('data-design'));
    syncGroup('face', root.getAttribute('data-body-face') || FACES[0].key);
    syncGroup('motion', root.getAttribute('data-motion') || '');
    syncGroup('leading', leading);
    syncGroup('density', density);

    /* A slider shows where the page actually is, computed, rather than what was
       last stored. A reader who has never touched it is told the design's own
       number, and on a narrow screen that is not the same number: the 720px
       block sets a smaller body size, so a hard-coded 19 here would be a
       confident wrong answer on every phone.

       The house measure is 81.15 characters and the control steps by five, so
       an untouched measure slider reads 80. It is the nearest position the
       control can express and it becomes exact the moment the reader moves it;
       an off-grid thumb that jumped on first touch would be worse. */
    Array.prototype.forEach.call(appearance.el.querySelectorAll('.set-field'), function (field) {
      var axis = field.rangeAxis;
      if (!axis) return;
      var computed = axis.read(parseFloat(getComputedStyle(root).getPropertyValue(axis.token)));
      var input = field.querySelector('input');
      input.value = String(isFinite(computed) ? snap(axis, computed) : axis.min);
      var legend = axis.legend(Number(input.value));
      field.querySelector('output').textContent = legend;
      input.setAttribute('aria-valuetext', legend);
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

  /* ============================================================
     THE PAGE'S ONE ARROWHEAD

     A hand-drawn diagram needs a connector with a head on it, and an SVG head
     is a `<marker>`, which is a definition referenced by id. That id has to be
     unique in the document, so a `<defs>` block copied into each figure
     collides the moment a page carries two diagrams: the second figure's
     `url(#hub-arrow)` resolves to the first figure's marker, which renders,
     validates, and reaches no console. One marker per page, owned here,
     removes the collision by removing the copies - and it means no page's
     markup mentions it, which is what lets the vocabulary reach all 797 pages
     without one of them being edited.

     `fill="context-stroke"` is the whole design. The head takes the colour of
     the line it sits on, so `class="d-flow s-alarm"` draws a red line with a
     red head and the author states no colour anywhere. An arrowhead that
     cannot disagree with what it points along is one less thing a figure can
     be quietly wrong about.

     This is the one part of the diagram vocabulary that needs this file. With
     the script blocked a connector still draws, in the right colour, and loses
     only its head, which is why the skill tells an author never to rest a
     figure's direction on the arrowhead alone.
     ============================================================ */
  function mountFigureDefs() {
    if (document.getElementById('hub-arrow')) return;
    var holder = document.createElement('div');
    holder.innerHTML =
      '<svg class="hub-defs" aria-hidden="true" focusable="false"><defs>' +
      '<marker id="hub-arrow" markerWidth="7" markerHeight="7" refX="6" refY="2.5"' +
      ' orient="auto" markerUnits="strokeWidth">' +
      '<path d="M0 0 L6 2.5 L0 5 Z" fill="context-stroke"/>' +
      '</marker></defs></svg>';
    document.body.appendChild(holder.firstChild);
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
     FIVE INTERACTIVE FIGURE SHAPES
     A stepper, an assembler, a calculator, a scorecard and a taint map:
     figures a reader operates rather than reads. Each wears `.diagram` for
     the frame and the caption pair plus its own class, reuses
     `.build-controls` for the control row and `.build-readout` for the
     numeric line, and is documented in
     .claude/skills/course-authoring/references/widgets.md.

     Five properties hold across all five and each is load-bearing.

     THE DATA IS MARKUP. A step, a part, a row and a block are elements the
     author wrote. Nothing here reads a JSON blob, so the figure prints, is
     searchable, is read by a screen reader before this file runs, and cannot
     fall out of step with a second file. `figure.cmatrix` above is the one
     widget that earned an external data file, and it took 191 rows.

     SCRIPT BLOCKED IS A COMPLETE PAGE. Every rule in `hub.css` that hides
     part of one of these is keyed on an attribute written only here -
     `[data-state]`, `[data-lit]`, `[data-can]` - so a page with no script
     shows every step, every fix and every block. The assembler goes further:
     its `<pre>` ships with every part already rendered into it and the first
     act of `mountAssemblers` is to render it again from the boxes.

     CONTROLS ARE NATIVE. Buttons, checkboxes, radios and ranges inside a
     `<label>`, so keyboard behaviour, focus rings and accessible names come
     from the platform. `scripts/focus_walk.py` presses real Tab keys.

     A CONTROL THAT CANNOT ACT SAYS SO WITH `aria-disabled`, NEVER `disabled`.
     A `disabled` button drops out of the tab order under the reader's finger:
     press Next onto the last step and focus falls to the document. Every
     no-op here stays focusable, announces its state, and does nothing.

     NOTHING PERSISTS. No `localStorage` in any of these, so no reader's
     answer outlives the page and none of them owes the save-state promise the
     notes and highlights panels make.

     None of the five paints into a canvas, so a mode or palette change needs
     no re-render: the DOM is painted by `hub.css` from tokens and follows the
     switch on its own.
     ============================================================ */

  // A figure's readout is the accessible status line for whatever moved, so
  // the count, the total and the band all arrive at a screen reader without
  // taking focus off the control the reader is still holding.
  function speakingReadout(figure) {
    var readout = figure.querySelector('.build-readout');
    if (readout) readout.setAttribute('aria-live', 'polite');
    return readout;
  }

  // The control row goes directly above the readout, because that is the order
  // the reader needs: act, then read what moved. A figure with no readout puts
  // it above the caption, and one with neither appends.
  function mountControlRow(figure, buttons) {
    var row = el('div', 'build-controls');
    buttons.forEach(function (button) { row.appendChild(button); });
    var before = figure.querySelector('.build-readout') || figure.querySelector('figcaption');
    if (before) figure.insertBefore(row, before);
    else figure.appendChild(row);
    return row;
  }

  function actionButton(label) {
    var button = el('button', null, label);
    button.type = 'button';
    return button;
  }

  function canAct(button, allowed) {
    button.setAttribute('aria-disabled', allowed ? 'false' : 'true');
  }

  // Grouping separators, always en-US, because the hub is written in English
  // and a figure's committed default value has to be the value the script
  // computes: a reader whose locale grouped differently would see the number
  // change on load for no reason they could name.
  function figureNumber(value, decimals) {
    if (!isFinite(value)) return '--';
    var places = isFinite(decimals) ? decimals : 0;
    return Number(value).toLocaleString('en-US', {
      minimumFractionDigits: places,
      maximumFractionDigits: places
    });
  }

  function figureOutputs(figure, attribute) {
    return Array.prototype.slice.call(figure.querySelectorAll('[' + attribute + ']'));
  }

  function writeOutputs(outputs, attribute, values) {
    outputs.forEach(function (node) {
      var role = node.getAttribute(attribute);
      if (Object.prototype.hasOwnProperty.call(values, role)) node.textContent = values[role];
    });
  }

  // `aria-controls` needs an id, and a figure that carries one can lend it.
  function nameRegion(figure, node, suffix) {
    if (!figure.id || node.id) return node.id || '';
    node.id = figure.id + '-' + suffix;
    return node.id;
  }

  /* ---------- the stepper ----------
     Plays an ordered list of turns. The step ahead of the reader keeps its
     row and loses its body, so the trace never jumps and the reader can see
     how much of it is left without seeing what is in it. `data-cost` is
     summed over everything played so far, which is what makes the figure
     about context growth rather than about clicking. */
  function stepCost(step) {
    var stated = parseFloat(step.getAttribute('data-cost'));
    return isFinite(stated) ? stated : 0;
  }

  function mountSteppers() {
    Array.prototype.forEach.call(document.querySelectorAll('figure.stepper'), function (figure) {
      var steps = Array.prototype.slice.call(figure.querySelectorAll('.step'));
      if (!steps.length) return;
      var outputs = figureOutputs(figure, 'data-step-out');
      speakingReadout(figure);

      var list = figure.querySelector('.step-list');
      var region = list ? nameRegion(figure, list, 'trace') : '';

      var back = actionButton('← Back');
      var next = actionButton('Next →');
      var restart = actionButton('Restart');
      [back, next, restart].forEach(function (button) {
        if (region) button.setAttribute('aria-controls', region);
      });
      mountControlRow(figure, [back, next, restart]);

      var at = 1;

      function render() {
        var carried = 0;
        steps.forEach(function (step, index) {
          var place = index + 1 < at ? 'done' : (index + 1 === at ? 'now' : 'ahead');
          step.setAttribute('data-state', place);
          if (index + 1 <= at) carried += stepCost(step);
        });
        writeOutputs(outputs, 'data-step-out', {
          index: figureNumber(at),
          total: figureNumber(steps.length),
          cost: figureNumber(carried),
          left: figureNumber(steps.length - at)
        });
        canAct(back, at > 1);
        canAct(next, at < steps.length);
        canAct(restart, at > 1);
      }

      function go(to) {
        var wanted = Math.min(steps.length, Math.max(1, to));
        if (wanted === at) return;
        at = wanted;
        render();
      }

      back.addEventListener('click', function () { go(at - 1); });
      next.addEventListener('click', function () { go(at + 1); });
      restart.addEventListener('click', function () { go(1); });
      render();
    });
  }

  /* ---------- the assembler ----------
     Concatenates the checked `<template>` parts into the figure's own
     `<pre><code>`, in the order the boxes are written. The copy button
     `wireCopyButtons` already put on that `<pre>` then works with no extra
     code at all.

     A template's body is indented to sit inside the page's markup, so the
     common indent comes off before it is written out: what the reader copies
     has to be the file, not the file plus four spaces a page needed. */
  function dedent(text) {
    var lines = String(text).replace(/\t/g, '  ').split('\n');
    while (lines.length && !lines[0].trim()) lines.shift();
    while (lines.length && !lines[lines.length - 1].trim()) lines.pop();
    var common = null;
    lines.forEach(function (line) {
      if (!line.trim()) return;
      var indent = line.match(/^ */)[0].length;
      if (common === null || indent < common) common = indent;
    });
    if (!common) return lines.join('\n');
    return lines.map(function (line) { return line.slice(common); }).join('\n');
  }

  // A token is about four characters of English prose. The widget says
  // "about" wherever it prints one, because this is an estimate and never a
  // measurement: no tokeniser ships in this file and none is going to.
  function tokenEstimate(text) {
    return Math.ceil(text.length / 4);
  }

  function mountAssemblers() {
    Array.prototype.forEach.call(document.querySelectorAll('figure.assembler'), function (figure) {
      /* Named through the `pre`, because `.asm-out code` is the first `code`
         in the block and a `.code-cap` is allowed to name its file in one.
         Written that way the assembled file was written into the caption, the
         `<pre>` never moved from what the page committed, and the readout
         updated correctly beside both - so every check passed and the figure
         was wrong on first paint. */
      var target = figure.querySelector('.asm-out pre code');
      if (!target) return;
      var boxes = Array.prototype.slice.call(
        figure.querySelectorAll('input[type="checkbox"][data-part]')
      );
      var templates = Array.prototype.slice.call(figure.querySelectorAll('template[data-part]'));
      if (!boxes.length || !templates.length) return;
      var outputs = figureOutputs(figure, 'data-asm-out');
      speakingReadout(figure);

      var region = nameRegion(figure, figure.querySelector('.asm-out'), 'file');

      // Matched in script rather than with an attribute selector: a part name
      // is author text and would need escaping before it could be a selector.
      function bodyOf(name) {
        for (var i = 0; i < templates.length; i++) {
          if (templates[i].getAttribute('data-part') === name) {
            return dedent(templates[i].content.textContent);
          }
        }
        return '';
      }

      function render() {
        var chosen = boxes.filter(function (box) { return box.checked; });
        var text = chosen
          .map(function (box) { return bodyOf(box.getAttribute('data-part')); })
          .filter(function (body) { return body; })
          .join('\n\n');
        target.textContent = text;
        writeOutputs(outputs, 'data-asm-out', {
          tokens: figureNumber(tokenEstimate(text)),
          chars: figureNumber(text.length),
          lines: figureNumber(text ? text.split('\n').length : 0),
          parts: figureNumber(chosen.length)
        });
      }

      boxes.forEach(function (box) {
        var label = box.closest('label');
        if (label) {
          label.appendChild(el(
            'span',
            'asm-cost',
            '+' + figureNumber(tokenEstimate(bodyOf(box.getAttribute('data-part')))) + ' tok'
          ));
        }
        if (region) box.setAttribute('aria-controls', region);
        box.addEventListener('change', render);
      });
      render();
    });
  }

  /* ---------- the calculator ----------
     Two operations and no more. `product` multiplies the named variables,
     `scale` multiplies that product by a constant the figure states. There is
     no expression language and no `eval` here, and there is not going to be:
     a formula parser in the shared runtime is a maintenance surface nobody
     asked for, and a page needing a third operation adds a named one to this
     closed set in the same three-part pull request every widget change takes.

     An unknown operation writes nothing, so the figure keeps the committed
     default it shipped with rather than showing the reader a NaN. */
  function calcValue(node, variables) {
    var names = (node.getAttribute('data-of') || '').split(/\s+/).filter(Boolean);
    var total = 1;
    for (var i = 0; i < names.length; i++) {
      if (!isFinite(variables[names[i]])) return NaN;
      total *= variables[names[i]];
    }
    if (node.getAttribute('data-calc') === 'scale') {
      var by = parseFloat(node.getAttribute('data-by'));
      if (!isFinite(by)) return NaN;
      total *= by;
    }
    return total;
  }

  function mountCalcs() {
    Array.prototype.forEach.call(document.querySelectorAll('figure.calc'), function (figure) {
      var fields = Array.prototype.slice.call(figure.querySelectorAll('[data-var]'));
      if (!fields.length) return;
      var outputs = figureOutputs(figure, 'data-calc').filter(function (node) {
        var operation = node.getAttribute('data-calc');
        return operation === 'product' || operation === 'scale';
      });
      speakingReadout(figure);

      // A range whose number the reader cannot see is a control they are
      // guessing at, so each one gets an `<output>` beside it. It is injected
      // rather than authored because it can only ever restate the input.
      // `aria-hidden` because a range control already announces its own value:
      // an `<output>` is a live region by default, so without it every drag
      // would be read out twice, and a third time by the readout below.
      var live = fields.map(function (field) {
        var value = el('output', 'calc-val');
        value.setAttribute('aria-hidden', 'true');
        if (field.id) value.setAttribute('for', field.id);
        if (field.parentNode) field.parentNode.insertBefore(value, field.nextSibling);
        return value;
      });

      function render() {
        var variables = {};
        fields.forEach(function (field, index) {
          var read = parseFloat(field.value);
          variables[field.getAttribute('data-var')] = read;
          live[index].textContent = figureNumber(read, parseInt(field.getAttribute('data-decimals'), 10));
        });
        outputs.forEach(function (node) {
          var value = calcValue(node, variables);
          if (!isFinite(value)) return;
          node.textContent =
            (node.getAttribute('data-prefix') || '') +
            figureNumber(value, parseInt(node.getAttribute('data-decimals'), 10)) +
            (node.getAttribute('data-suffix') || '');
        });
      }

      fields.forEach(function (field) {
        field.addEventListener('input', render);
        field.addEventListener('change', render);
      });
      render();
    });
  }

  /* ---------- the scorecard ----------
     Sums `value` times the row's `data-weight`, and picks a band from the two
     thresholds the figure states. `.score-fix` is the author's own words and
     is never hidden: it is the teaching, and revealing it only on a low score
     would make the widget a quiz. That is also what makes the printed figure a
     usable checklist. */
  var SCORE_BANDS = [0.5, 0.8];
  var SCORE_NAMES = ['not started', 'under way', 'ready'];

  function scoreThresholds(figure) {
    var stated = (figure.getAttribute('data-bands') || '').split(/\s+/).map(parseFloat)
      .filter(function (value) { return isFinite(value); });
    return stated.length === 2 ? stated : SCORE_BANDS;
  }

  function scoreNames(figure) {
    var stated = (figure.getAttribute('data-band-names') || '').split('|')
      .map(function (name) { return name.trim(); })
      .filter(function (name) { return name; });
    return stated.length === 3 ? stated : SCORE_NAMES;
  }

  function rowWeight(row) {
    var stated = parseFloat(row.getAttribute('data-weight'));
    return isFinite(stated) && stated > 0 ? stated : 1;
  }

  function rowCeiling(row) {
    var best = 0;
    Array.prototype.forEach.call(row.querySelectorAll('input[type="radio"]'), function (option) {
      var value = parseFloat(option.value);
      if (isFinite(value) && value > best) best = value;
    });
    return best;
  }

  function mountScorecards() {
    Array.prototype.forEach.call(document.querySelectorAll('figure.scorecard'), function (figure) {
      var rows = Array.prototype.slice.call(figure.querySelectorAll('.score-row'));
      if (!rows.length) return;
      var outputs = figureOutputs(figure, 'data-score-out');
      var thresholds = scoreThresholds(figure);
      var names = scoreNames(figure);
      speakingReadout(figure);

      // The weight is a scoring detail rather than teaching, so it is written
      // here and not into the page: a reader with no script gets every
      // question, every option and every fix, which is the document that
      // matters, and loses only the multiplier.
      rows.forEach(function (row) {
        var stem = row.querySelector('.score-q');
        if (!stem) return;
        // The glyph and the words, exactly as the quiz marks an option: a
        // multiplication sign is read as anything from "times" to nothing at
        // all, and the weight is the reason one question outranks another.
        var chip = el('span', 'score-weight', '×' + rowWeight(row));
        chip.setAttribute('aria-hidden', 'true');
        stem.appendChild(chip);
        stem.appendChild(el('span', 'sr-only', ' worth ' + rowWeight(row) + ' points.'));
      });

      var meter = el('div', 'score-meter');
      var fill = el('span', 'score-fill');
      meter.appendChild(fill);
      meter.setAttribute('role', 'progressbar');
      meter.setAttribute('aria-valuemin', '0');
      var before = figure.querySelector('.build-readout') || figure.querySelector('figcaption');
      if (before) figure.insertBefore(meter, before); else figure.appendChild(meter);

      function render() {
        var points = 0;
        var ceiling = 0;
        var answered = 0;
        rows.forEach(function (row) {
          var picked = row.querySelector('input[type="radio"]:checked');
          ceiling += rowCeiling(row) * rowWeight(row);
          if (picked) {
            points += (parseFloat(picked.value) || 0) * rowWeight(row);
            answered += 1;
          }
          row.setAttribute('data-answered', picked ? 'yes' : 'no');
        });
        var share = ceiling > 0 ? points / ceiling : 0;
        var band = share >= thresholds[1] ? 2 : (share >= thresholds[0] ? 1 : 0);
        fill.style.width = (share * 100).toFixed(1) + '%';
        fill.setAttribute('data-band', String(band));
        meter.setAttribute('aria-valuenow', String(points));
        meter.setAttribute('aria-valuemax', String(ceiling));
        meter.setAttribute('aria-valuetext', points + ' of ' + ceiling + ', ' + names[band]);
        writeOutputs(outputs, 'data-score-out', {
          points: figureNumber(points),
          max: figureNumber(ceiling),
          percent: figureNumber(share * 100),
          answered: figureNumber(answered),
          rows: figureNumber(rows.length),
          band: names[band]
        });
      }

      Array.prototype.forEach.call(figure.querySelectorAll('input[type="radio"]'), function (option) {
        option.addEventListener('change', render);
      });
      render();
    });
  }

  /* ---------- the taint map ----------
     One turn, split by who wrote each block. The state that teaches is the one
     with the origins turned OFF: five blocks that look identical, which is
     exactly what the model is handed. The default is on, because that is the
     more useful static document and it is what a page with no script shows.

     The capability line is the author's own `.taint-can`, hidden until the
     second box is ticked. Generating it was never an option: what an agent may
     do with a block is a claim about a real system and belongs in the page,
     where a reviewer can argue with it. */
  var TAINT_ORIGINS = ['you', 'repo', 'foreign'];

  function mountTaints() {
    Array.prototype.forEach.call(document.querySelectorAll('figure.taint'), function (figure) {
      var parts = Array.prototype.slice.call(figure.querySelectorAll('.taint-part'));
      if (!parts.length) return;
      var outputs = figureOutputs(figure, 'data-taint-out');
      var boxes = Array.prototype.slice.call(figure.querySelectorAll('input[type="checkbox"][data-taint]'));
      speakingReadout(figure);

      var turn = figure.querySelector('.taint-turn');
      var region = turn ? nameRegion(figure, turn, 'turn') : '';
      boxes.forEach(function (box) {
        if (region) box.setAttribute('aria-controls', region);
        box.addEventListener('change', render);
      });

      function boxFor(role) {
        for (var i = 0; i < boxes.length; i++) {
          if (boxes[i].getAttribute('data-taint') === role) return boxes[i];
        }
        return null;
      }

      function render() {
        var lit = boxFor('foreign');
        var can = boxFor('capability');
        figure.setAttribute('data-lit', !lit || lit.checked ? 'on' : 'off');
        figure.setAttribute('data-can', can && !can.checked ? 'off' : 'on');
        var tally = { total: parts.length };
        TAINT_ORIGINS.forEach(function (origin) { tally[origin] = 0; });
        parts.forEach(function (part) {
          var origin = part.getAttribute('data-origin');
          if (Object.prototype.hasOwnProperty.call(tally, origin)) tally[origin] += 1;
        });
        writeOutputs(outputs, 'data-taint-out', {
          you: figureNumber(tally.you),
          repo: figureNumber(tally.repo),
          foreign: figureNumber(tally.foreign),
          total: figureNumber(tally.total)
        });
      }

      render();
    });
  }

  function mountInteractiveFigures() {
    mountSteppers();
    mountAssemblers();
    mountCalcs();
    mountScorecards();
    mountTaints();
  }

  /* ---------- and what all five do on paper ----------
     Paper has no reader behind it, so a figure held at step two of nine would
     print seven blank rows and a taint map with the origins switched off would
     print five identical blocks and no claim. Every played state comes off
     before the sheet and goes back after, exactly as the practice disclosures
     do, and riding on `toPaper` / `offPaper` is what gets this the Safari
     media-query path as well.

     The controls themselves need nothing here: `.build-controls` is in the
     print block's hide list already. */
  var figuresOnPaper = null;

  function openFigures() {
    if (figuresOnPaper) return;
    figuresOnPaper = [];
    Array.prototype.forEach.call(document.querySelectorAll('.step[data-state]'), function (step) {
      figuresOnPaper.push([step, 'data-state', step.getAttribute('data-state')]);
      step.removeAttribute('data-state');
    });
    Array.prototype.forEach.call(document.querySelectorAll('figure.taint'), function (figure) {
      ['data-lit', 'data-can'].forEach(function (name) {
        if (!figure.hasAttribute(name)) return;
        figuresOnPaper.push([figure, name, figure.getAttribute(name)]);
        figure.setAttribute(name, 'on');
      });
    });
  }

  function closeFigures() {
    if (!figuresOnPaper) return;
    figuresOnPaper.forEach(function (held) { held[0].setAttribute(held[1], held[2]); });
    figuresOnPaper = null;
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
    /* First, because a hand-drawn connector is already on the page and paints
       its head the moment the marker exists. */
    mountFigureDefs();
    var outline = window.COURSE_OUTLINE;
    var hasRail = !!(outline && outline.sections && outline.sections.length);
    if (hasRail) {
      mountRail(outline);
      // The stored preference only applies where the rail is part of the layout.
      document.body.dataset.rail = isWide() ? (get(STORE.rail) || 'on') : 'off';
    }
    mountTopbar(hasRail);
    mountCluster();
    /* After the cluster, because both insert themselves straight after the
       topbar and this one has to land in front of it in the tab order. */
    if (hasRail) mountChapterBar(outline);
    mountSectionRail();
    mountStageFlag();
    wireQuizzes();
    wireCopyButtons();
    mountInteractiveFigures();
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
        if (root.getAttribute('data-mode')) return;
        // The cluster names the mode it will switch to, so a reader following
        // the system whose machine has just gone dark needs the label back the
        // other way round.
        syncCluster();
        renderMermaid();
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
