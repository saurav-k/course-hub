# The widget vocabulary

Every visual element available to a page, and the exact markup for each.
Copy the markup character for character.
Nothing here is a suggestion about shape: `assets/hub.css` styles these class names and `assets/hub.js` binds behaviour to these class names, so a near-miss is unstyled, inert, or both.

There is **one** design system and one copy of it.
The old `assets/course.css` / `course.js` pair and its per-course forks are gone.
Three courses still layer an `assets/course-extras.css` after the hub sheet for rules genuinely unique to them, and those files restyle shared elements, so grep every `*.css` in the repository before you change any selector.

Adding a widget is a three-part pull request: the CSS in `assets/hub.css`, the entry here, and the first use.

## Page chrome

### A lesson or a reference sheet

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page title - Course Name</title>
<meta name="description" content="One sentence: the one idea, for a search result.">
<link rel="stylesheet" href="../../assets/hub.css">
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script src="../../assets/hub.js"></script>
<script src="../outline.js"></script>
</head>
<body>
<nav class="spine"><div class="spine-inner">
  <a class="home" href="../index.html">COURSE NAME</a>
  <a href="../index.html">Course map</a>
  <a href="../reference/glossary.html">Glossary</a>
  <a href="../../index.html">Course Hub</a>
  <span class="sp"></span>
</div></nav>

<main class="wrap">
  ...
</main>
</body>
</html>
```

Five rules, all of them load-bearing.

- **One stylesheet, `assets/hub.css`.** Add `<link rel="stylesheet" href="../assets/course-extras.css">` immediately after it, and only if that course already has one or the rule you need is genuinely unique to that course. A course owns its palette hue and its extras, never the design system.
- **`hub.js` loads in the head, without `defer`.** It writes `data-mode`, `data-palette` and `data-course` onto `<html>` before the first paint, so a deferred copy means every page flashes the wrong colours.
- **`../outline.js` after it.** That is what the sidebar rail reads, and it is generated: `python3 scripts/gen_outline.py <course>`. A routed course loads `../routes.js` first and then its hand-written `../outline.js`; `gen_outline.py` refuses to run against one.
- **The Mermaid script tag goes on a page if and only if that page contains a `.mermaid` block.** It must come before `hub.js`, which claims the render from it in its head phase.
- **No `<button class="theme-btn">`.** `hub.js` deletes a legacy one and mounts the real appearance control, which offers three modes and six palettes. Writing one is dead markup.

`main.wrap` is the reading column and it is the default for a lesson and for a reference sheet.
`main.wide wrap` is the full width and it is for a course map and the hub landing page only.

### A course map

Same head, one level shallower, and no Mermaid unless the map itself carries a diagram:

```html
<link rel="stylesheet" href="../assets/hub.css">
<script src="../assets/hub.js"></script>
<script src="outline.js"></script>
```

## Lesson head

```html
<div class="eyebrow">Module 01 &middot; The Transformer Core &middot; Lesson 01</div>
<h1>Attention Is All You Need</h1>
<p class="paper-meta">
  <span class="pill med">working</span>
  <span class="pill">11 min</span>
  Vaswani et al. (Google Brain, 2017).
  &middot; <a href="https://arxiv.org/abs/1706.03762">arXiv:1706.03762</a>
</p>
```

The rung pill comes first and its text is the rung word: `easy`/foundation, `med`/working, `hard`/frontier.
The reading-time pill comes second.

The number in the eyebrow is the lesson's file number with the padding dropped: `lessons/0007-*.html` is `Lesson 07`.
The `<footer>` at the bottom of the page repeats that same number.
The module number in the eyebrow is the module the card sits under in `index.html`, and the two must agree.
Both are mandatory on every lesson page. See the ladder in [`pedagogy.md`](pedagogy.md).

A one-sentence framing line may use `<p class="lead">` instead, above `.paper-meta`, where the page has no attribution to carry.

## Headings: the tag and the size are separate decisions

`h1` to `h4` set the outline a screen reader navigates by.
`.h-sub` is the h3 face and `.h-label` is the small uppercase h4 face.
Fix a broken heading order by retagging the heading and adding the matching class, never by leaving the tag wrong because the right one looks wrong.

That is why the house forms below read `<h2 class="h-label">` rather than `<h4>`: they sit directly under the page `<h1>` and a bare `<h4>` there skips two levels.

## The one-minute version

Opens every page. Three to five bullets, each a claim, each bolding its own key term.

```html
<div class="card tldr">
  <h2 class="h-label">The one-minute version</h2>
  <ul>
    <li>Before this paper, sequence models read text <b>one step at a time</b>.</li>
  </ul>
</div>
```

## Callouts

Three, and the difference is not decoration.

```html
<div class="card callout key"><span class="tag">The reframing</span>
  The sentence you want the reader to still have next month.</div>

<div class="callout warn">
  The failure that is silent, expensive, or both. At most one per page.</div>

<div class="callout">
  An aside that is worth setting apart but is neither the key idea nor a warning.</div>
```

`.callout.warn` is also where an honest limit goes: a source that is loose, an assumption doing real work, evidence thinner than the claim.
Reserve it. A page with three warnings has no warning.

## Diagrams

### The orientation figure, which opens every content page

Ordinary `figure.diagram` markup in a load-bearing position: the page's first figure, directly after the one-minute version and before the first body section.
Position is what makes it the orientation figure, so there is no class to remember and nothing to add to the stylesheet.

```html
<figure class="diagram">
  <div class="mermaid">
flowchart LR
  P["What came before&lt;br/&gt;the reader already has this"] --> T["THIS PAGE&lt;br/&gt;the one idea"]
  T --> N["What it enables&lt;br/&gt;named, not hinted"]
  W["The larger thing&lt;br/&gt;this is a part of"] -.- T
  </div>
  <figcaption>Where this sits: it takes X from the previous page and is what makes Y possible.
  <b>The one sentence a reader should leave with even if they read nothing else.</b></figcaption>
</figure>
```

Three things it must draw, which is why the floor is three nodes: what came before, this, what it enables.
On a routed course it names what the idea enables rather than the next file, because the neighbour changes with the route and the place in the whole does not.
Any kind may carry it.
A `timeline` suits a history, a `mindmap` suits a chapter that indexes topics, a `flowchart` suits everything else.

The bar, and the test the figure has to pass, are in [`pedagogy.md`](pedagogy.md).

### Mermaid, for structure

```html
<figure class="diagram">
  <div class="mermaid">
flowchart LR
  A["Observed data"] --> B["Estimate"]
  </div>
  <figcaption>Plain English reading of the figure, with <b>the one takeaway in bold</b>.</figcaption>
</figure>
```

Four rules that are the difference between a diagram and an error box.
`hub.js` stashes the graph source as `node.textContent` so it can repaint the diagram when the reader changes mode or palette, and every one of these is a way that stash goes wrong.

- **`<div class="mermaid">`, never `<pre class="mermaid">`.** `hub.js` appends a copy button to every `<pre>`, so a `pre` diagram gains the word `copy` as a final line of graph source and renders as a syntax error. Nothing reaches the console.
- **A line break inside a label is `&lt;br/&gt;`, never `<br/>`.** A literal `<br/>` is parsed by the browser into a real `BR` element, which `textContent` drops. The first render survives; every repaint after that joins the two halves with no break and no space, so the diagram is correct until the reader touches the appearance controls and mangled from then on. In a sequence diagram the join can merge two statements and the figure becomes a red error box.
- **No semicolon in diagram text.** Use a dash. Where it is fatal was measured against the Mermaid 11 the hub loads, rather than assumed: in a `sequenceDiagram`, the free text after a colon in a message or a `Note over` is parsed as a statement, so a semicolon there renders the whole figure as a red error box. A flowchart label survives one, quoted or not, as do a timeline title and a `stateDiagram-v2` transition label. Write the dash anyway; the safe positions are not worth carrying, and a Mermaid upgrade is free to narrow them.
- **Always wrap node labels in double quotes.** `A["P(X > 2000)"]` parses; `A[P(X > 2000)]` does not. Parentheses, commas and mathematics all break the parser bare, and every technical course is full of them.

Pick the kind by what the reader is confused about:

| Kind | The reader's confusion | Use it for |
|---|---|---|
| `flowchart` | what connects to what | components, decisions, before-and-after |
| `sequenceDiagram` | what happens in what order | requests, retries, handshakes, failure paths |
| `stateDiagram-v2` | what state the thing is in | lifecycles, protocols, connection state |
| `mindmap` | how a field is organised | a chapter's own map, a taxonomy |
| `timeline` | when things happened | history, a roadmap, a release sequence |
| `quadrantChart` | how options compare on two axes | trade-off placement |

`timeline` shrinks rather than wraps, so keep it to about six columns and split a longer one into two figures.
`quadrantChart` centres a label under its point and neither clips nor wraps it, so keep point labels under about 26 characters and away from the axes.

A `mindmap` and a `timeline` take their branch colours from Mermaid's own twelve-step scale rather than from the theme it is handed.
`hub.js` supplies that scale from the `--branch-0..7` tokens and `hub.css` pins the mindmap root disc, so both follow the palette.
A diagram type that appears in a colour following neither the palette nor those tokens is that bug resurfacing.

### Inline SVG, for anything quantitative

Mermaid cannot draw a distribution, a density, a confidence band, or a scatter plot.
Write the SVG by hand, in the page. No chart library, no build step, no extra CDN.

```html
<figure class="diagram">
  <svg class="chart" viewBox="0 0 640 300" role="img" aria-label="What this chart shows">
    <line class="axis" x1="60" y1="250" x2="610" y2="250"/>
    <rect class="m-stat"  x="70"  y="180" width="30" height="70"/>
    <rect class="m-alarm" x="110" y="40"  width="30" height="210"/>
    <text class="lbl-sm" x="85" y="268" text-anchor="middle">typical</text>
  </svg>
  <div class="chart-legend"><span><i class="sw-stat"></i>typical day</span></div>
  <figcaption>Plain English, with <b>the takeaway in bold</b>.</figcaption>
</figure>
```

- Always a `viewBox`, never a `width`/`height` pair. Around `640 x 300` keeps 13px text readable.
- Always `role="img"` and an `aria-label` saying what the chart shows.
- **Colour comes only from the semantic classes.** A literal hex looks right in one theme and vanishes in the other, and it cannot follow the print stylesheet either.

The colour names are a **closed set, shared by the whole hub** and declared in `assets/hub.css`: `stat`, `prob`, `signal`, `noise`, `alarm`, `gold`, `plum`, `sky`, and `ink` for marks and strokes.
They are not a per-course palette any more; a course's identity comes from its accent hue, not from its charts.

| Prefix | Applies to | Example |
|---|---|---|
| `m-*` | a filled mark: bar, dot, area | `m-stat`, `m-alarm` |
| `s-*` | a stroked line or curve | `s-signal`, `s-noise` |
| `f-*` | a translucent fill: a band, a region | `f-prob` |
| `t-*` | coloured text | `t-alarm` |
| `sw-*` | a legend swatch inside `.chart-legend` | `sw-gold` |
| `axis`, `grid`, `tick`, `panel`, `ref`, `thick` | chart furniture | |
| `lbl-sm`, `lbl-b`, `lbl-on`, `ttl` | chart text faces | |

One idea keeps one colour on every page of a course.

## Interactive builds

The wrapper every running artifact mounts inside: canvas, controls, readout, caption, one figure. `probability-you-build-course` uses it for every weekly build; any course whose pages carry a live widget uses the same shape.

```html
<figure class="build" id="<build-id>">
  <div class="build-stage"><canvas class="build-canvas" width="640" height="360"></canvas></div>
  <div class="build-controls">
    <label>quality bar <input type="range" min="0.5" max="0.99" step="0.01" value="0.95" data-role="bar"></label>
    <button type="button" data-role="simulate">Simulate</button>
  </div>
  <div class="build-readout">
    <span>P(correct) analytic <b>0.95</b></span>
    <span>simulated <b>0.9497</b></span>
  </div>
  <figcaption>What the reader should see when they move the control, and <b>why that is the lesson</b>.</figcaption>
</figure>
```

Five parts, each with a job:

- **`figure.build` with an `id`.** The frame: surface, border, shadow, like a diagram box. The `id` lets a quiz or a sentence link straight at the build (`#planner-build`). Required.
- **`.build-stage` holds `.build-canvas`.** The stage is the drawing's plate. Give the canvas real pixel dimensions in its `width`/`height` attributes - it scales down responsively and stays centred, so pick a size (around 640 wide) whose drawn type survives scaling on a phone.
- **`.build-controls` holds labelled native inputs.** `<label>` wrapping the control text, native `input`, `select`, `button` elements. Keyboard behaviour, focus rings and screen-reader names come from the platform; do not rebuild them in script.
- **`.build-readout` holds live numeric output** as inline spans. It renders mono with tabular numerals; bold marks the moving numbers. This is where an analytic result sits beside its Monte Carlo twin.
- **`figcaption` states what the reader should see and why**, per the house caption bar. A build without a stated takeaway is decoration.

Build script rules (the full contract lives in that course's `BUILDER-SPEC.md`):

- Shared scripts live at `probability-you-build-course/assets/builds/<name>.js` and load from the head with `defer`.
- Draw colours only from CSS tokens, read at draw time, never literal hex: a canvas bakes colours into pixels, so unlike CSS it cannot follow a mode or palette change on its own. Keep state outside closures and re-render when the theme moves:

  ```js
  new MutationObserver(render)
    .observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
  ```

- Print hides the controls (inert on paper) and keeps stage, readout and caption. A build whose dark rendering would be unusable on white paper adds a `beforeprint` listener that redraws print-safe ink, restoring on `afterprint`; at minimum say in the caption what the printed figure shows.

## The capability matrix

A four-way comparison table: one row per capability key of the shared taxonomy,
one column per cloud. `cloud-comparison-course` owns it; its course map opens
with one. Unlike every widget above, an author does not write the rows - the
widget renders itself from a data file, because 191 rows hand-written in HTML is
a maintenance hole.

The author writes only the frame, and the figcaption is theirs to word:

```html
<figure class="cmatrix" id="capability-matrix">
  <figcaption>The capability matrix: one row per capability, one column per cloud.
  Filter by area, search by service name, and follow any cell to that vendor's own documentation.
  <b>A dashed cell means nobody has written it yet; a marked cell means the cloud genuinely has no equivalent.</b></figcaption>
</figure>
```

The page also loads the data file in the head, before `hub.js`, exactly as
`outline.js` is loaded:

```html
<script src="matrix.js"></script>
```

`hub.js` finds every `figure.cmatrix` and builds the legend, the area filter,
the search box, the sticky column headers and the rows from
`window.CLOUD_CAPABILITY_MATRIX`. Everything is DOM painted from semantic
tokens, so a mode or palette change needs no re-render; the narrow-screen and
print restacking is in `hub.css`. If the data file is missing or unreadable the
frame shows a visible broken-page note rather than an empty box.

### The data contract

The data file is the single source of truth for the taxonomy, and
`scripts/validate_site.py` gates all of this:

```js
window.CLOUD_CAPABILITY_MATRIX = {
  snapshot: "2026-08-26",                                // when the four inventories were verified
  clouds:  [ { key: "aws", short: "AWS", ... }, ... ],   // exactly aws, azure, gcp, oci; column order
  domains: [ { slug: "compute-iaas", name: ..., covers: ..., keys: ["vm-instances", ...] }, ... ],  // 24 areas
  rows:    [ { key: "vm-instances", domain: "compute-iaas", title: "VM instances",
               cells: { aws: {...}, azure: {...}, gcp: {...}, oci: {...} } }, ... ]
};
```

`snapshot` is optional and is data, not page text: it records when the cells were verified so a refresh knows what it is refreshing.
The widget does not paint it, because a course may forbid dates on its pages; `cloud-comparison-course` does, and keeps that date in its `RESOURCES.md` instead.

One row per capability key; each key appears under exactly one area and as
exactly one row; every row carries a cell for all four clouds. A cell is one of
exactly three states:

| State | Markup | Reads as |
|---|---|---|
| unfilled | `{ "state": "unfilled" }` | dashed, quiet - *nobody has written this yet* |
| absent | `{ "state": "absent", "reason": "..." }` | marked bar + tag - the cloud genuinely ships no equivalent, and why |
| service | `{ "state": "service", "services": [{ "name": "...", "short_name": "...", "doc_url": "https://...", "one_line": "...", "status": "ga" }] }` | linked service names into that vendor's own documentation |

`status` is optional and is one of `ga`, `preview`, `retiring` or `deprecated`.
Everything that is not `ga` renders as a badge on the service name; `ga` renders nothing, so the badge stays rare enough to notice.
That badge is what tells a reader which of two services in one cell a new design should pick, because such a pair is normally a current service beside the legacy one it replaces.

**An unfilled cell and a declared absence must never look alike.** They mean
different things - missing data versus a finding - and the reader must be able
to tell them apart at a glance, in every mode, palette and on paper. Any edit
that moves the two states closer together is a defect even if it looks tidier.

Every `doc_url` must be a well-formed https link; the validator fetches nothing
by default, so before opening a pull request that touches the data file run:

```bash
python3 scripts/validate_site.py --vendor-links
```

which chases dead links over the network and fails on any HTTP error status or
unreachable host.

## Formulas

```html
<div class="math">
  admitted(T) = B + (r &times; T)
  <span class="gloss">Read as: over a window of <i>T</i> seconds a client gets the whole
  bucket <i>B</i> once, plus whatever the bucket refills at rate <i>r</i> during the window.</span>
</div>
```

The `.gloss` names **every** symbol in words.
No formula ships without one.
A `<br/>` inside `.math` is an ordinary line break and is correct there; the entity rule applies only inside `.mermaid`.

## Worked arithmetic

```html
<ol class="worked">
  <li><b>Add the ten numbers.</b> Running the total in order: 400, then 750 ... and finally <b>12,250</b>.</li>
  <li><b>Divide by the count.</b> 12,250 &divide; 10 = <span class="keynum">1,225</span>.</li>
</ol>
```

`<span class="keynum">` marks a number quoted from a source, so a reader can tell a stated figure from one this page derived.
`<span class="exact">` wraps notation inside a `<th>`, because table headers are uppercased and that flattens `x - x̄` into `X - X`.

## Code

```html
<div class="code-cap">pile_mix.py &middot; runnable Python, standard library only</div>
<pre><code>import hashlib
</code></pre>
```

The copy button is injected by `hub.js` into every `<pre>`. Do not add one.
The caption names the file and says what it is, so a reader knows whether to run it or read it.

## Retrieval practice

```html
<h2>Check yourself</h2>
<div class="quiz">
  <h3 class="h-label">Retrieval practice</h3>
  <p class="note-sm">Answer from memory before revealing.</p>

  <div class="q" data-answer="2">
    <div class="q-stem">In attention, what do Query and Key produce together?</div>
    <button class="q-opt">The final blended output vector for each of the tokens</button>
    <button class="q-opt">The positional encoding added onto each input token</button>
    <button class="q-opt">Relevance scores saying how much each token attends</button>
    <button class="q-opt">The feed-forward network weights used inside the block</button>
    <div class="q-fb">Query dot Key gives the raw relevance score. The first option is the
      output after the blend, the second is added before attention runs, and the fourth
      belongs to a different sublayer entirely.</div>
  </div>
</div>
```

`data-answer` is a **zero-based** index into the `.q-opt` buttons.
Exactly four options, matched to within 12 characters. The counts and the answer-index rule are in [`pedagogy.md`](pedagogy.md).
`hub.js` writes the tick, the cross and their screen-reader labels itself; the page supplies nothing but the four buttons and the feedback.

## Practice problems

A quiz is a quick check the reader answers in their head.
A practice problem needs paper and several minutes, so it is a different widget and it sits **after** the quizzes, under its own `<h2>Practice</h2>`.

```html
<h2>Practice <span class="note-sm">about 15 minutes, with paper</span></h2>

<div class="practice">
  <div class="p-head"><span class="tag">Practice 1</span><span class="pill med">working</span></div>

  <div class="p-stem">
    <p>A dataset has two features whose covariance matrix is:</p>
    <div class="math">
      S = [[2, 1], [1, 2]]
      <span class="gloss">Read as: a 2 by 2 covariance matrix. Each feature has variance
      <i>2</i>, and the covariance between the two is <i>1</i>.</span>
    </div>
    <p><b>Find</b> the two principal directions and the share of variance the first one carries.</p>
  </div>

  <details class="hint"><summary>Hint</summary>
    <p>A principal direction is an eigenvector of the covariance matrix.
    Start from det(S - &lambda;I) = 0.</p></details>

  <details class="solution"><summary>Show the worked solution</summary>
    <ol class="worked">
      <li><b>Write the characteristic equation.</b> det(S - &lambda;I) = (2 - &lambda;)<sup>2</sup> - 1 = 0.</li>
      <li><b>Solve it.</b> (2 - &lambda;)<sup>2</sup> = 1, so &lambda; = 3 or &lambda; = 1.</li>
      <li><b>Take the variance share.</b> 3 &divide; (3 + 1) = 0.75.</li>
    </ol>
    <p class="p-check"><b>Sanity check.</b> The trace is 4 and the eigenvalues sum to 4, as they must.
    Both are positive, as they must be for a covariance matrix.</p>
  </details>
</div>
```

Six rules.

- **Reveal-only.** There is no answer box and no checker. The reader attempts the problem, then opens the solution. `<details>` carries the disclosure, the keyboard behaviour and the expanded state a screen reader announces, so no JavaScript is involved and nothing breaks with scripting off.
- **`details.hint` before `details.solution`.** Zero or more hints, exactly one solution. A hint names the next move without making it, so a reader who is stuck can unstick themselves without being shown the answer.
- **Every problem ends in `.p-check`,** one sentence saying what the answer should roughly be and why. It is what lets a reader catch their own arithmetic, and `check_pages.py` fails a problem without one.
- **The solution is an `ol.worked`,** one arithmetic step per `<li>`, each opening with a bolded imperative. `.keynum` marks a number quoted from a source; a number derived here is plain.
- **Practice text is not prose.** `check_pages.py` excludes the block from the word ceiling and from the words-per-figure ceiling, exactly as it excludes the quiz. Without that exclusion a single problem takes a clean page over both.
- **`hub.js` opens every disclosure for printing** and closes again afterwards, so a printed page carries its solutions and the reader's own open/closed state survives. Nothing on the page needs to arrange that.

The floors, and which courses are held to them, are in [`pedagogy.md`](pedagogy.md).

## Course map

The course `index.html`, and the same card shape on the hub landing page.

```html
<section class="module">
  <div class="module-h"><span class="mnum">01</span><h2 class="h-sub">The Transformer Core</h2><span class="mcount">4 lessons</span></div>
  <div class="lgrid">
    <a class="lcard" href="lessons/0001-attention-is-all-you-need.html">
      <div class="ln">Lesson 01</div>
      <div class="lt">Attention Is All You Need</div>
      <div class="ld">One or two sentences saying what the reader will be able to do after it.</div>
      <div class="lmeta"><span class="pill med">working</span><span class="pill">11 min</span></div>
    </a>
  </div>
</section>
```

`scripts/gen_outline.py` parses exactly this shape: it splits the page at each `.module-h`, reads `.mnum` and the heading, and takes each card's `.lt` as the lesson title.
A heading written any other way empties that section of the generated outline, and `validate_site.py` then fails the pull request for a stale outline.
Match either `<h2 class="h-sub">` or `<h3>`; new work uses the first.

A page planned but unwritten goes in a `.roadmap` list as plain text.
**Never as a link**: a link to a file that does not exist fails the validator.
A roadmap entry that has since been written is marked `class="written"`.

Where a course nests a level deeper, a lecture hub card is followed by `<ul class="parts">` listing its parts, each numbered with `<span class="pn">`.

`.roadmap` is now in `assets/hub.css`, because a second course needed it and an unstyled roadmap is invisible markup.
**It is currently declared twice**: the copy in `statistical-foundations-ml-course/assets/course-extras.css` is still there, and on that course's own pages it wins on cascade order. The two declarations are equivalent, so nothing renders differently, but the duplication is real and the extras copy should be deleted the next time that course is touched for another reason.
`.parts` and `.pn` are still only in that extras sheet, so a new course that uses them gets unstyled markup and must promote them the same way rather than copying the file.

Two more small shapes live in the hub sheet and are worth knowing, because both were being written as inline styles before they existed:

- **`.note-sm`** is the quiet line under a heading: the instruction above a quiz, the time estimate beside a `Practice` heading, an aside under a module title.
- **`.module-note`** is a paragraph of prose under a `.module-h` on a course map, where a `.sub` would be unstyled because `.sub` is only styled inside a `.hero`.

## Page foot

In this order, every page:

```html
<div class="teacher-note"><b>Your teacher.</b> What to ask an agent next if a step did not land.</div>

<h2 class="h-label">Primary source to go deeper</h2>
<p>The single best onward source, with a real working link.</p>

<div class="pager">
  <a href="0000-previous.html"><span class="dir">&larr; Previous</span><span class="ttl">Previous title</span></a>
  <a class="nxt" href="0002-next.html"><span class="dir">Next &rarr;</span><span class="ttl">Next title</span></a>
</div>

<footer><p>Course Name &middot; Lesson 01 &middot; <a href="../reference/glossary.html">Glossary</a></p></footer>
```

The last page's "next" points at `../index.html`, titled "Course map".
The spine already carries a link back to the course map, which is the `← Course map` route `AGENTS.md` asks for; a page whose spine omits it owes an explicit one in the foot.

A routed course writes `<nav class="pager" data-pager-route="ROUTE-ID" aria-label="Lesson navigation">` instead, and `validate_site.py` checks that its two links are the neighbours the owning route declares.
See `llm-evolution-course/routes/README.md`.

## The lab kit

For courses whose pages are exercises rather than readings.

```html
<div class="lab">
  <div class="goal">Goal</div>
  <h3 class="h-label">Stand up vLLM, then measure tokens per second under concurrency</h3>
  <p>What the learner will have done by the end, in one sentence.</p>

  <div class="metric-grid">
    <div class="metric"><div class="k">Endpoint</div><div class="v">:8000</div><div class="u">OpenAI-compatible /v1</div></div>
  </div>

  <div class="term">
<span class="p">$</span> vllm serve meta-llama/Meta-Llama-3-8B-Instruct \
    --gpu-memory-utilization 0.90 \  <span class="c"># fraction of VRAM for weights and KV cache</span>
<span class="o">INFO: Started server process</span>
  </div>
</div>

<ul class="checklist">
  <li>I can launch vLLM with <code>vllm serve</code> and hit its :8000 endpoint</li>
</ul>
```

`.p` is the prompt, `.c` a comment, `.o` output.
`.metric` is key, value, unit.
The `ul.checklist` closes a lab page: each item is something the learner can now do, phrased in the first person.

These classes live in `llm-inference-course/assets/course-extras.css`, not in the hub sheet, so today they only work in that course.
A second course that wants the lab kit promotes the rules into `assets/hub.css` and deletes them from the extras file, in one pull request. It does not fork them.
