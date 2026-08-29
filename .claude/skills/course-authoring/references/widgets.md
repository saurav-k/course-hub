# The widget vocabulary

Every visual element available to a page, and the exact markup for each.
Copy the markup character for character.
Nothing here is a suggestion about shape: `assets/hub.css` styles these class names and `assets/hub.js` binds behaviour to these class names, so a near-miss is unstyled, inert, or both.

There is **one** design system and one copy of it.
The old `assets/course.css` / `course.js` pair and its per-course forks are gone.
Three courses still layer an `assets/course-extras.css` after the hub sheet, and those files restyle shared elements, so grep every `*.css` in the repository before you change any selector.
Those three are grandfathered and no course gets a fourth: see "The course contract" at the foot of this file.

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

- **One stylesheet, `assets/hub.css`.** Add `<link rel="stylesheet" href="../assets/course-extras.css">` immediately after it only when that course already has one; three do, they are grandfathered, and no course gets a fourth. A course owns the seven tokens of the course contract, never the design system.
- **`hub.js` loads in the head, without `defer`.** It writes `data-mode`, `data-palette` and `data-course` onto `<html>` before the first paint, so a deferred copy means every page flashes the wrong colours.
- **`../outline.js` after it.** That is what the sidebar rail reads, and it is generated: `python3 scripts/gen_outline.py <course>`. A routed course loads `../routes.js` first and then its hand-written `../outline.js`; `gen_outline.py` refuses to run against one.
- **The Mermaid script tag goes on a page if and only if that page contains a `.mermaid` block.** It must come before `hub.js`, which claims the render from it in its head phase.
- **No `<button class="theme-btn">`.** `hub.js` deletes a legacy one and mounts the real appearance control, which offers three modes, seven palettes and two designs. Writing one is dead markup.

**The spine is one row that never wraps, and it changes shape twice on the way down.**
Below 1040px nothing in it may be squeezed except the wordmark, which clips to an ellipsis rather than running out over the next link.
Below 720px the row keeps the wordmark, the **last** of the page's own links, and the two controls, and hides the rest.
So write the link a reader on a phone must keep last, which on this hub is `Course Hub`: it is the one destination the wordmark does not already reach.
`hide-sm` still marks a link as droppable at 720px and is still worth writing, but it is no longer what holds the row together - 493 of the 796 pages carry no such class, so the rules that keep the row legible read the structure every spine shares instead.

`main.wrap` is the reading column and it is the default for a lesson and for a reference sheet.
`main.wide wrap` is the full width and it is for a course map and the hub landing page only.

Inside `main.wrap` a page has three widths, and they are the only three:

| Width | How to reach it | For |
|---|---|---|
| the prose column | the default for every child | prose, and anything read as prose |
| the breakout | a figure, table, `pre`, `.diagram`, `.module`, `.lgrid`, `.hero` or `.roadmap`, which the sheet widens on its own; `class="wide"` on anything else | a figure or a table that does not fit the prose column |
| edge to edge | `class="bleed"` | reserved, see below |

**`.bleed` is a reserved escape hatch and it has no uses today.**
It is kept on purpose rather than retired: it is the only route from `main.wrap` to the full grid column, the gutters included, and without it the first page that wants a full-bleed figure would reach for an inline style or invent a class, and the vocabulary is closed.
It stays one declaration, it stays documented, and reaching for it means the figure genuinely wants the whole page.
Widening the whole page instead is `main.wide`, which is a decision about the page and not about one element.

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

### The breadcrumb, `.crumbs`

Optional, and above the eyebrow when it is there.
The hub sheet styles it; no script is needed to make it work.

```html
<nav class="crumbs" aria-label="Breadcrumb"><a href="../../index.html">Course Hub</a><span class="sep">/</span><a href="../index.html">Course Name</a><span class="sep">/</span><span>Module name</span></nav>
```

`.sep` is the divider between the rungs and is a `<span>` holding a single `/`.
The last rung is the page's own place and is plain text, never a link.
`aria-label="Breadcrumb"` is what tells a screen reader which navigation this is; the class alone says nothing.

Only `llm-evolution-course` writes one today, on all 60 of its pages, because a routed course is the case where a reader can arrive from four different orders and needs telling which one they are in.
That course adds `data-crumb-section` to the last rung and its own `outline.js` rewrites the text to the active route's section name; the attribute means nothing outside it, so do not copy it into another course.
An ordinary course whose spine already names the hub and the course map does not need a breadcrumb as well.

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

#### A colour of its own, in a `classDef`

Most diagrams need none: every node already carries the palette.
Where one node genuinely means something different from another - kept against dropped, a constant against a term you can shrink - write a `classDef` and give it a **token**, never a hex literal.

```
  classDef keep fill:var(--ok-soft),stroke:var(--ok)
  classDef drop fill:var(--warn-soft),stroke:var(--warn)
```

Mermaid's own grammar rejects a parenthesis in a `classDef` value, so `hub.js` resolves the token on the way in, from the same probe that themes the rest of the diagram.
The result follows the palette, both modes and every repaint, and the printed copy comes out black on white with the rest of the page.
**A hex literal cannot do any of that**: it is one mode's answer written down, and the mode it is wrong in is the one nobody checked. Two published diagrams carried a near-white fill under near-white labels in dark mode, at 1.1:1, until this existed.

Three rules.

- **Name a semantic token, not a raw one.** `--ok`, `--warn`, `--gold`, `--accent-2`, `--surface-2`, `--line-strong` and their `-soft` partners. The raw `--l-*` and `--d-*` layer belongs to the terminal transcript and to nothing else.
- **Do not set `color`.** The label already takes `--ink` from the theme, in both modes. Setting it is how a fill and its label drift apart later.
- **Spell the token correctly.** A name the stylesheet does not declare is left exactly as written, so Mermaid fails to parse it and draws a red error box. That is deliberate: a visible failure beats a colour quietly taken from somewhere else.

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
  <b>A cell marked NO EQUIVALENT means the cloud genuinely ships nothing for that capability. A cell marked DELIVERED ELSEWHERE means it has the capability inside a service this table lists on another row, and links you there.</b></figcaption>
</figure>
```

The page also loads the data file in the head, before `hub.js`, exactly as
`outline.js` is loaded:

```html
<script src="matrix.js"></script>
```

Word the figcaption by the tag a cell wears, not by its colour. The page prints,
and the print block flattens both `--gold` and `--ok` to the same grey, so a
caption that says "the gold cell" describes nothing on paper and nothing to a
reader who cannot separate the two hues.

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
exactly four states:

| State | Markup | Reads as |
|---|---|---|
| unfilled | `{ "state": "unfilled" }` | dashed, quiet - *nobody has written this yet* |
| absent | `{ "state": "absent", "reason": "..." }` | solid gold bar + NO EQUIVALENT - the cloud genuinely ships no equivalent, and why |
| elsewhere | `{ "state": "elsewhere", "reason": "...", "see": "<capability key>" }` | dotted green bar + DELIVERED ELSEWHERE - the cloud **has** the capability, inside a service that holds a row under another key, with a link to that row |
| service | `{ "state": "service", "services": [{ "name": "...", "short_name": "...", "doc_url": "https://...", "one_line": "...", "status": "ga" }] }` | linked service names into that vendor's own documentation |

`see` is optional on an `elsewhere` cell, for the case where the capability is
spread across several rows rather than living in one. When it is present the
validator resolves it: the target must be a real row, must not be the cell's own
row, and must be a `service` cell for that same cloud. A cross-reference into
another absence would render as a confident sentence and be a lie.

`status` is optional and is one of `ga`, `preview`, `retiring` or `deprecated`.
Everything that is not `ga` renders as a badge on the service name; `ga` renders nothing, so the badge stays rare enough to notice.
That badge is what tells a reader which of two services in one cell a new design should pick, because such a pair is normally a current service beside the legacy one it replaces.

**No two of the four states may look alike.** They mean different things -
missing data, a finding, a difference in packaging, an answer - and the reader
must be able to tell them apart at a glance, in every mode, every palette and on
paper. Any edit that moves two states closer together is a defect even if it
looks tidier.

`absent` and `elsewhere` are the pair that matters most, because they make
opposite claims and both arrive as a `gaps` entry in the same inventory. A cell
must never imply a cloud cannot do something it demonstrably can, so
**NO EQUIVALENT is reserved for `absent`.** The widget separates the two on three
signals at once, and each one covers a case the others miss:

- the bar style, solid against dotted, which is the only signal that survives
  print, where `--gold` and `--ok` both flatten to `#333`;
- the hue, `--gold` against `--ok`, which no palette aliases to one another -
  unlike `--accent-2`, which *equals* `--gold` in Sage and Aubergine and would
  have made the two boxes identical for those readers;
- the tag word, which is what a screen reader gets.

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

**The plate and the chip are two token pairs.**
A `<pre>` reads `--code-bg` and `--code-ink`; an inline `<code>` reads `--code-inline-bg` and `--code-inline-ink`.
Six palettes state the same values twice, so the two look identical on them.
Press states them apart: a dark plate for a block of code, deep rust on warm paper for a word of it inside a sentence, which is what the reference site does and what one shared pair could not express.
Both pairs carry body text, so `scripts/contrast.py` holds both to 7:1.
Neither is yours to write in a page - `hub.css` owns both rules - and neither is a design-axis token, because both are colour.

**Both sizes are one token, `--fs-mono`, and it is written in `em`.**
So block and inline code track the prose around them, and a change to the reader's body size or reading face moves both together.

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

`.roadmap` is in `assets/hub.css`, because a second course needed it and an unstyled roadmap is invisible markup.
The hub sheet is its only home; the duplicate that used to sit in `statistical-foundations-ml-course/assets/course-extras.css` is gone.
`.parts` and `.pn` are still only in that extras sheet, so a new course that uses them gets unstyled markup and must promote them the same way rather than copying the file.

On the hub landing page a category may carry an emblem, `<img class="cat-art">`, between the `.module-h` heading and its `.mcount`:

```html
<div class="module-h"><span class="mnum">CLOUD</span><h2 class="h-sub">Cloud Architecture</h2><img class="cat-art" src="assets/category-cloud.svg" alt="" width="34" height="34"><span class="mcount">5 courses</span></div>
```

The image is decorative, so `alt` is empty: the heading beside it already names the category, and a second reading of the same words is noise on a screen reader.
`width` and `height` are the intrinsic size of the file and hold the space before it loads; the sheet sets the drawn height to `1.7rem` and lets the width follow, so the emblem tracks the heading rather than a pixel figure.
Only Cloud Architecture has one today.
An emblem is a hub-landing-page shape, not a course-map one.

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

**The whole kit lives in `assets/hub.css`, under "the lab kit", and every course may use it.**
`llm-inference-course` invented it and `llm-efficiency-course` was the second course to need it, which is what promoted it; the originating extras file keeps no copy, and the responsive and print rules for `.lab` and `.metric-grid` and the tabular-numerals entry for `.metric` sit in the hub sheet beside the base rules rather than in two files.
One owner, one place to change it.

One rule in that block reads the raw palette layer on purpose.
`.term` is drawn from the `--d-*` values in **both** modes, because a terminal reads as a terminal only while it is dark, and the `--d-*` set is declared whichever mode the reader is in.
That is the one sanctioned use of the raw layer: everything else in the kit reads the semantic tokens.
The print block restates the six `--term-*` tokens with `!important`, because the hub's own print block flattens the semantic tokens and cannot reach these.

## The design tokens

Type, rhythm and shape are tokens, in one block near the head of `assets/hub.css` marked "the design axis".
A page never names one: the sheet does, and a page gets the whole system by linking the sheet.
The block matters to you in three cases - you are adding a widget, you are changing an existing rule, or you are writing a course sheet.

**Adding a widget or changing a rule: read a token, never a literal.**
The whole point of the block is that a second design is a list of values rather than a second copy of the sheet, and one hard-coded `1.05rem` is a rule that a design cannot reach.
If nothing in the block fits, add a token beside the ones it belongs with, give it a call-site comment, and say so in the pull request.

The groups, and what each is for.

| Group | Count | What a rule reads |
|---|---|---|
| Faces | 4 | `--font-body` for reading prose, `--font-display` for `h1` to `h4`, `--font-ui` for chrome and captions, `--font-mono` for code. The three `--sans` / `--serif` / `--mono` tokens above them are the registry of what is loaded; do not name those. `--font-body` is set by the face registry rather than in this block; see the derived axes below. |
| Type scale | 62 | `--fs-1` to `--fs-4` are the four heading sizes, `--fs-body`, `--fs-lead`, `--fs-ui`, `--fs-sm`, `--fs-xs`, `--fs-foot` and `--fs-mono` the named roles, and the rest are component sizes named for the component. `--fs-body` and `--fs-mono` are derived, not set; see the derived axes below. |
| Leading | 15 | `--lh-tight` for headings, `--lh-body` for prose, then one per component role. `--lh-body` carries the measure nudge; see the derived axes below. |
| Weight | 6 | `--fw-normal` 400, `--fw-medium` 600, `--fw-strong` 650, `--fw-bold` 700, `--fw-metric` 750, `--fw-heavy` 800. |
| Tracking | 14 | Negative on display type, positive on anything set in capitals. |
| Space | 176 | Two layers; see below. |
| Reading frame | 3 | `--measure-chars-default`, the column width in real characters, and `--wide-left` / `--wide-right`, unitless shares summing to 1 that say how the breakout band sits around it. `.5` and `.5` centres the prose; `0` and `1` grows figures from its left edge. The rule does the arithmetic, because `--measure-wide` differs by element. |
| Shape | 17 | The seven radii, the four border widths, and the six that are the shadow *shape* - its colour stays on the mode layer. |
| Focus ring | 5 | `--focus-ring-color`, `--focus-ring-width`, `--focus-ring-style` and the two offsets; see below. |
| Motion | 11 | Six durations, two easings, two lift distances and one slide distance. `--motion-slide` is `0px` in House; a design whose signature gesture is horizontal sets it and every lesson card follows. |
| Eyebrow | 5 | Family, case, tracking, size and weight, as one author-level treatment. |

**Six of those tokens carry two names.**
`--font-display`, `--font-mono` and the four eyebrow tokens a course may set are written by a design as `--x-default` and by a course as `--x`, so the two writers never contend; every rule still reads `--x`.
See "The course contract" at the foot of this file.

**Space has two layers and a rule only ever reads the second.**
Layer one is `--sp-1` to `--sp-8`, a ramp of ratio about 1.41 anchored on `.5rem`, which is the modal spacing value in the sheet; every step is a local maximum of the measured distribution.
Layer two is the roles: the reading column's rhythm, the component insets, the gap ladder and the offset ladder.
**Never write `padding: var(--sp-3)`.** A ramp step in a rule is a value with no name, and it puts a reading-rhythm distance and a chrome distance on the same token, which is exactly what the split exists to prevent.

Six of the role tokens are the reading column's vertical rhythm - `--sp-para`, `--sp-list`, `--sp-heading-before-*`, `--sp-heading-after-*`, `--sp-block*` and `--sp-figure*` - and a later reader density control may scale those and nothing else.
Everything else, component insets and page chrome included, is permanently out of its reach.
That is a hard limit rather than a note: seven pointer targets in the chrome pass WCAG 2.2 SC 2.5.8 only on the spacing exception and the smallest compliant control has two pixels of margin, so a compact chrome would turn near-misses into failures.

**A reader-settable value has three layers; nothing else does.**
`hub.css` declares a `-default`, `hub.js` writes only a `--*-user` property inline on `<html>`, and one resolved token `--x: var(--x-user, var(--x-default))` is what every rule reads.
Only that resolution line may read a `--*-user` property, and only as the head of its own fallback: what follows the comma is a `-default` for a token a control sets directly and the derivation itself for a derived axis.
Twenty-four tokens carry the form today, and they are the ones a reader control can reach: `--measure-chars`, `--measure`, `--fs-body`, `--lh-body` and the twenty prose-rhythm roles.
**A resolution line never sits inside a design block.** A design block is `(0,2,0)`, so a resolution line written in one would be a second resolution line for the same reader value and source order between two designs would decide which answered.
The twenty rhythm roles resolve at a bare `:root` just after the design blocks, in the shape of the course layer, and the design writes only the `-default`.
The `var()` still picks up the design's value, because substitution reads the computed value of the `-default` on the element rather than the declaration beside it.
The rest are one-layer design tokens.
The reading face is the one reader choice that is not a `--*-user` property, because three measured constants have to travel with the family; it is the registered axis attribute `data-body-face` instead.
The consequence for a media query: a token with a `-user` layer must be restated as its `-default` inside the query, never as the token, or the query out-argues the reader.
`--fs-body-default` in the 720px block is the worked example.

**The focus ring is one ring, and every focusable element gets it.**
`--focus-ring-color` is `--accent-2`, deliberately not `--accent`: the ring is never the link colour, and never the fill of the control it surrounds - the appearance panel's pressed mode card is painted in `--accent` and its ring used to be the same colour as itself.
`--focus-ring-offset` is 2px and `--focus-ring-offset-box` is the 3px a scroll container takes, one pixel further out so the ring clears the box's own edge.
Neither may be 0: a ring on the border box of a scroll container is clipped by that container and disappears.
Write the rule against `:focus-visible`, never `:focus`, so a mouse click paints nothing.
You should not need to write one at all - `hub.css` already covers `a`, `button`, `input`, `select`, `summary`, `textarea` and anything carrying a `tabindex` - and if you find an element that needs its own, it is a sign the element is doing something the closed vocabulary does not know about.
`scripts/focus_walk.py` presses Tab through three pages, the appearance panel and a narrow viewport and fails if any stop is missing the ring, wearing the browser's own, or sitting flat on the border box.

**Contrast is measured, not asserted.**
`scripts/contrast.py` checks the colours the palette layer states outright - every registered ground is inside its lightness band, every ink clears 7:1 and sits on the right side of the L\* 48.9 crossover, every other palette colour clears the floor its role carries - and it runs inside `validate_site.py`, so it gates every pull request.
`scripts/contrast_matrix.py` measures what needs a browser: the nine `color-mix()` tints and the per-course accent, over every registered palette, two modes and every registered course hue.
Both print every number, pass or fail: `python3 scripts/contrast.py --report` is the command to run while choosing a colour, and both carry a `--self-test` or a recorded-breach list so a gate that stops biting says so.
The floors are WCAG 2.2: 7:1 body text, 4.5:1 every other text, 3:1 borders, focus rings and chart marks.

## The derived axes

Four of the reading axes are not independent, and each coupling is measured.
A framework that offered the four as free settings would let a reader move one control and silently move a second, and then build a page that no single setting explains.
So the block after the design axis derives all four, in CSS, with nothing left to the script.

**The measure names real characters, and the width is computed.**
`ch` is the advance of the digit zero rather than of a character, and the two part company by face: one `ch` of Source Serif 4 is `.5049em` against an average prose character of `.4479em`, so the `72ch` this sheet used to carry was 81 characters and not 72.
A reader who set "72" and then changed the reading face would have moved their line length without touching the measure control.
`--measure-chars` is the number a control sets and `--measure` is the width that follows from it.

**The body size names apparent size, not nominal size.**
Holding `font-size` at 19px and swapping Source Serif 4 for Inter makes the page about 21% larger to the eye, because the x-heights are `.4520` and `.5459` em.
So `--fs-body-ref` is the reader's number on the Source Serif 4 reference scale and `--fs-body` is what the page renders.

**The code size follows the reading face.**
JetBrains Mono at x-height parity is `.822em` against a Source Serif 4 body and `.993em` against an Inter body, so one hard-coded mono size is wrong for one of the two faces.
`--fs-mono` is derived from `--xh-body`, and it stays a ratio of `1em` so block and inline code keep tracking the prose that surrounds them.

**The leading rises with the measure, as a nudge and never as a lock.**
Above 80 characters, or above the design's own default measure if that is wider, `--lh-body` gains `.05` per 10 characters.
A reader who has chosen a line spacing suppresses the nudge entirely, and nothing may move a control's visible position because another control moved.

**A face is a name plus three measured constants.**
The family, the average prose advance, the x-height per em and the apparent-size factor are declared together in one `:root[data-body-face="..."]` entry, because the three derivations cannot compute without all three numbers.
Never set `--font-body` on its own, and never copy a constant out of a report: `scripts/type_invariants.py` refuses an entry that names a family without the other three, measures the advance from a committed corpus of real hub prose, and holds two invariants for every registered face.
M1 requires a `--measure-chars` of N to realise N plus or minus one characters, at 55, 68, 80 and 85.
M2 requires the code size to stay inside `.85` to `.90` of the prose under a serif reading face, at every body size the panel will offer.
The registry must stay after any design block, for the same reason the mode layer sits after the palettes: an explicit reader choice and a design block have the same specificity, so source order decides.

**Four tokens are outputs and nothing may write them.**
`--measure`, `--fs-body`, `--fs-mono` and the per-face constants are computed from the controls above them.
A control that wrote one would put back exactly the coupling this block removes.

**A course sheet restates tokens; it never restates rules.**
The three `course-extras.css` files are layered after the hub sheet, so a copy of a hub rule in one of them wins on source order and every later change to the hub sheet stops at that course's pages.
Setting `--radius` or `--fs-note` under a course's own selector reaches the same pixels and keeps one owner.
Write that selector as `:root[data-course="your-course"]`, which is the spelling `hub.css` already uses for `--course-hue`.
A bare `[data-course="..."]` is `(0,1,0)` and loses to a design block, so the course's own value would go silently dead.
The spelling is necessary and not sufficient: a course block and a design block are both `(0,2,0)`, so for the six tokens both of them want, the design writes a `-default` and the course writes the token.
See "The course contract" below.
A new course has no sheet to do either in: it declares the seven tokens of the course contract and nothing else.

## The faces, and what a page pays for them

Three families are self-hosted as woff2 beside the stylesheet, declared at the head of `assets/hub.css` and served from nowhere else.
That is what lets a page opened straight off disk look like the published one, and it is why no reader is ever visible to a font service.
`assets/fonts/README.md` carries the per-file table, the sizes and the refresh procedure.

**Eight files, 459.3K on disk, and no page fetches more than four of them.**
The `-ext` cuts are gated by `unicode-range` and only 34 of the 796 pages carry a character that needs one.
A page with no italic in its prose fetches 152.8K; a page with `<em>` in its prose fetches 241.0K, and that is 559 of the 796 pages, so it is the number to plan against.
`scripts/validate_site.py` holds both a total ceiling and a latin-cut ceiling, so a fourth face is added against a known figure rather than against a guess.

**`font-display` is `swap` on every face, and it is the only value this hub may use.**
The validator refuses `optional`, and the reason is measured rather than argued.
`optional` does remove the swap, and there is little left to remove: the font-attributable layout shift on a throttled first load measures 0.00002 on the hub landing page, 0.0011 on the worst lesson and 0.027 on a course map, because the derived apparent-size layer leaves the fallback and the webfont occupying nearly the same space.
It was 0.29 on that lesson before the derived layer landed, so the swap is cheap because of a fix rather than by nature.
The reason `optional` is refused is separate: a face that misses the first-paint deadline is dropped for the life of that page load.
Chrome will not apply it afterwards and `document.fonts.load()` does not bring it back: after the drop, a probe set in `"Source Serif 4"` measures exactly as wide as one set in a family that does not exist.
A reader control that switches the body face would therefore do nothing at all until the next navigation.
`block` and `fallback` only add invisible text, because the faces arrive 1.4s to 1.9s after first paint on a Slow 4G connection, which is inside the swap period both of them end with anyway.

**Loading a face on demand is a different mechanism, and it is not governed by that descriptor.**
Both registry faces are on every page already - `--font-body` resolves to Source Serif 4 or to Inter, and the chrome pulls Inter regardless - so switching between the two today costs no fetch at all.
A *third* face is the case that needs this note.
It should not be fetched before the reader picks it, and a `@font-face` rule cannot express that: the browser decides from the rendered content when to fetch, which for a registered face is always.
The control that offers the face therefore loads it itself, with the CSS Font Loading API, and selects it only once the load has settled:

```js
var face = new FontFace('Some Face', "url('../../assets/fonts/some-face.woff2') format('woff2')", { display: 'swap', weight: '400 700' });
face.load().then(function (loaded) {
  document.fonts.add(loaded);
  root.setAttribute('data-body-face', 'someface');   // the registry entry, with its three constants
});
```

Two properties follow, and both are the point.
A `FontFace` built in script carries its own `display`, so it is never subject to the descriptor on any `@font-face` rule and never silently dropped.
And setting the attribute only inside the callback means the reader never sees the fallback flash on a control they just used, and never sees a measure computed from one face while another is on screen.
The control panel owns that code; this note owns the contract it has to keep.

## The palette axis

A palette is the colour half of the system, and it is the only place in `hub.css` that states a literal colour.
Seven are registered - Paper, Slate, Ink, Sage, Harbor, Aubergine and Press - and each states **18 raw values twice**, once as `--l-*` for light and once as `--d-*` for dark.
The mode layer maps one of the two sets onto the semantic tokens every rule reads, and it is written once for the whole system, so adding a palette is a block of values plus one entry in the `PALETTES` array in `hub.js`.

Sixteen of the eighteen are colours. The other two are the ground treatment and the reading pane, and they work together.

`--*-wash` is a `background-image` value painted on the canvas, `none` on six of the seven palettes and two faint radial gradients on Press.
A ground that is a flat fill reads as a screen colour; a ground with a wash reads as paper.

`--*-pane` is what the reading column paints behind the prose.
Six palettes state their own `--surface`, which is what that column has always been.
Press states `transparent`, so the prose sits directly on the washed paper and cards and callouts read as lighter veils over it - the reference site's own arrangement, which has no separate reading pane at all.
Text on a Press page therefore sits on `--bg` rather than on `--surface`, and both grounds are checked.

Both are a palette's rather than a design's because both are colour, and both are stated by every palette rather than by the one that uses them, because a palette is data the framework consumes and never a name the framework knows.

**Do not name a raw value.** `--l-*` and `--d-*` exist for the mode layer and for the appearance panel's own swatches. Everything else reads a semantic token.

**Every colour is measured before it is registered.**
`scripts/contrast.py` runs inside `validate_site.py` and holds every registered ground inside its lightness band, every ink to 7:1 on the right side of the L\* 48.9 crossover, and every other stated colour to the floor its role carries.
`scripts/contrast_matrix.py` runs in the browser job and measures the nine `color-mix()` tints and the per-course accent over every palette, both modes and every registered course hue.
A palette that fails is a palette to fix. The band is arithmetic, not taste.

## The design axis

The block above is a *design*, and `house` is its name.
`hub.js` writes `data-design` on `<html>` in its head phase, beside `data-mode` and `data-palette`, before the first paint.
The token block is written once under two selectors, `:root, :root[data-design="house"]`, exactly as the Paper palette is: the bare arm is what a page gets with no script at all, and the attribute arm is what the axis selects.

**Two designs are registered.**
`house` is what every reader had before the axis existed, and it is the fallback a withdrawn design falls through to.
`press` is the form half of the reference look: a display serif set at or below 1.0 leading with tracking graded by size, prose set loose against it, monospace on every eyebrow, capitals always tracked, a 68-character column, figures growing from the prose's left edge, softer radii, a shadow that pools rather than drops, and one signature gesture that is horizontal.
Sixty of its 317 tokens differ from House; the rest are House's, restated in full.
Its colour half is the `press` *palette*, not part of it, so a reader may wear either without the other.

**A design carries no colour.**
Type, rhythm, shape, motion and the eyebrow treatment are the design's; the 16 raw colours and the ground treatment are the palette's, and the light-or-dark mapping is the mode's.
That split is why a second design costs no row in the contrast matrix, and it is why the reference look's warm paper ships as a seventh palette rather than as part of a design.

**A design is data, and nothing branches on its name.**
No function in `hub.js` and no rule in `hub.css` knows a design by name; the registry is a plain array and the blocks are keyed on the attribute.
The same is true of a palette.
That is what keeps the door open to designs, palettes and course templates arriving from somewhere other than these two files.

**Adding a design is a block of the same tokens under a new attribute value, plus one entry in the `DESIGNS` registry in `hub.js`.**
Three checks in `scripts/validate_site.py` hold the two halves together, so none of this is left to review:

- every registered design has a block and every block is registered, so the picker can offer nothing that resolves to nothing;
- every design declares the *whole* token set, compared against the default design's, in both directions - a design that declares half of it inherits the other half and looks nearly right;
- a design-axis token is declared in a design block and nowhere else, because a design block is `(0,2,0)` against a bare `:root` and would out-argue a media-query override in every viewport.

**What a design may not reach, and why.**
The body size is resolved outside every design block, because the 720px arm has to be able to move it and a design block would out-argue that arm.
The reading face is a registry entry carrying three measured constants, and a design has no way to supply them, so the face registry sits *after* the design blocks and has the last word.
Colour is the palette's.
Everything else - the whole type scale, the leading set, the weights, the tracking, the space ramp and its roles, the reading frame, the shape, the motion vocabulary and the eyebrow treatment - is the design's, on paper as well as on screen.

**Withdrawing a design is deleting its registry entry.**
The picker stops offering it and a reader who had chosen it falls through to the registered default, because the head phase validates a stored key against the registry exactly as it does a palette key.
No deploy, no page edit, and the fallback was measured to restore the original exactly.

**A design moves faces, so anything measured at render time is repainted through `whenFontsReady`.**
Mermaid cuts every label box to a measurement it takes at render time, and it takes that measurement in the face `hub.js` hands it - `--font-ui`, the chrome role, which is also what `hub.css` paints diagrams with.
Test a design change by *switching*, never by loading: a diagram with stale metrics renders correctly on the next reload, which is how the defect survives review.

## The reader control panel

`hub.js` builds one panel and it reaches every page, because every page already links the shared assets.
Nothing about it is in any page's markup, and a page served with the script blocked has no panel and no dead control in its place.

**Six controls, and three axes that are deliberately not among them.**
The six are the ground (mode and palette), the body size, the reading face, the measure, the line spacing and the density.
A control earns its place when readers genuinely differ on it, when the reader can perceive the difference and judge it, and when a wrong setting is recoverable.
The display face, the mono face and the eyebrow treatment fail all three in the same way: a reader sets one once out of curiosity and never returns to it, and they are exactly the axes a *course* has every reason to differ on, so they are author tokens on the course contract instead.
The accent is not a seventh control either.
It is carried by the palette the reader already chooses and rotated per course, and expanding it into a colour picker would put a contrast criterion in the reader's hands.

**A control is an input to a derivation, never a setting of its own.**
The four couplings in "The derived axes" above are why: a reader who set a measure of 72 and then changed the face would move their line length without touching the measure control.
So the measure names real characters, the body size names apparent size on the Source Serif 4 reference scale, the code size follows the reading face on its own, and the leading nudges above a wide measure unless the reader has stated one.
`--measure`, `--fs-body`, `--fs-mono` and the per-face constants are outputs and no control writes one.

**Every control writes a `--*-user` property or a registered axis attribute, and nothing else.**
Two of the reader's choices are attributes rather than properties, because what they carry does not compose into a single value: `data-body-face` selects a family together with the three measured constants that have to travel with it, and `data-motion` selects a block of rules.
Check 11 in `scripts/validate_site.py` gates both halves - hub.js may write no other attribute on `<html>` and no property that is not a `--*-user` one hub.css resolves.

**Density scales the reading column's rhythm and reaches nothing else, and that is structural rather than promised.**
It writes the twenty prose-rhythm roles as `calc(var(--x-default) * 0.75)`, so a design that restates a role is scaled rather than overruled, and the only names it *can* write are ones hub.css resolves.
There is no headroom in the chrome for a compact mode: one control already fails WCAG 2.2 SC 2.5.8, seven more pass on the spacing exception alone, and the smallest compliant control has two pixels of margin.

**The panel moves, by pointer and by keyboard.**
The title bar is the drag surface and the grip inside it takes the arrow keys, with Shift for a finer step and Home or Enter to put the panel back where it started.
A panel only a mouse can move is a panel some readers cannot move at all.

**Its position is an intention, and what is rendered is that intention clamped into the viewport in front of the reader.**
The band it is held inside is measured off the sticky topbar and the pre-production strip rather than assumed, so it can never be parked under either.
The clamp does not write back, so a coordinate chosen on a wide display comes back when the wide display does, and on a phone the panel is re-seated rather than stranded.
Only the re-seat glides; a move the reader is aiming lands at once, and `[data-motion="reduced"]` zeroes the glide with every other transition.

**The panel is a non-modal dialog, and that follows from it being movable.**
It carries `role="dialog"` and `aria-labelledby` and it does not carry `aria-modal`, because a reader parks it in order to keep reading with it open and telling a screen reader the page behind it is inert would be a lie.
For the same reason focus is not trapped and a click on the page does not close it.
Focus moves into the panel when it opens; Escape and the close control both shut it, and both return focus to the opening button only when focus was inside the panel, so a reader who has tabbed back into the page keeps their place.

**The panel passes the floors it enforces.**
Its labels are `--ink` or `--ink-soft` and never faint ink on a recessed surface at a small size - the comment on the copy button in `hub.css` records that this codebase has already failed that once.
Every control clears 24 by 24 CSS pixels, which is why the range thumb is drawn rather than inherited: the browser's own is about 16px square.
`scripts/focus_walk.py` opens the panel and presses Tab through all of it in both modes.

**"Back to this course's defaults" is exact.**
It removes every `--*-user` property, every reader axis attribute and the panel's own position, which leaves the stylesheet's own values with nothing to unwind.
That is a property of the three-layer rule rather than a feature of the button: a reader value that competed with a token instead of feeding one would have to be unwound rather than removed.

## The course contract

A course declares its identity through **seven tokens, in one block, and through nothing else**.
The block is keyed on the `data-course` attribute `hub.js` writes onto `<html>` from the URL path, and it sits in `assets/hub.css` with the other registrations under "the course contract".
Adding a course adds no framework code, and every control the framework offers works on the new course automatically, because every control operates on tokens the new course inherits.

```css
:root[data-course="statistical-foundations-ml-course"] {
  --course-hue: -50;                  /* required */
  --font-display: var(--serif);       /* optional */
  --font-mono: var(--mono);           /* optional */
  --eyebrow-family: var(--font-mono); /* optional */
  --eyebrow-tracking: .18em;          /* optional */
  --eyebrow-case: uppercase;          /* optional */
  --eyebrow-size: var(--fs-xs);       /* optional */
}
```

| Token | Required | Constraint |
|---|---|---|
| `--course-hue` | yes | A unitless number. Never a `deg` value: inside a relative colour `h` is a number and not an angle, so `calc(h + 25deg)` is a type error that drops the whole declaration in silence. |
| `--font-display` | no | A face in the registry, named as `var(--serif)` or `var(--font-mono)`, never a font stack of your own. |
| `--font-mono` | no | A face in the registry. |
| `--eyebrow-family` | no | A face in the registry. |
| `--eyebrow-tracking` | no | `0em` to `.34em`, or `var(--tracking-eyebrow)`. |
| `--eyebrow-case` | no | `uppercase` or `none`, and `uppercase` only on a label of about five words or fewer. |
| `--eyebrow-size` | no | Inside the `--fs-xs` band, `.625rem` to `.78125rem`, or `var(--fs-xs)`. |

Three of the seven are deliberately absent from the reader's panel.
The display face, the mono face and the eyebrow treatment decide a heading voice and a two to four word label, so a reader has no basis on which to choose them and would set them once and forget them, while a course has every reason to differ on them.
They are author-level for that reason, and for no other.

**Six of the seven carry two names, and a course writes the shorter one.**
A design block and a course block are both `(0,2,0)`, so if they wrote the same property the cascade would settle the contest silently on source order.
The design therefore writes `--x-default`, a course writes `--x`, and every rule reads `--x`.
The resolution line at bare `:root` is `(0,1,0)`, so a course block wins it wherever either one appears in the file.
`--course-hue` needs no such layer, because a design carries no colour and nothing else may write it.

`validate_site.py` checks every constraint in that table except one, and the exception is the hue itself.
Rotation preserves OKLCH lightness and chroma, but the gamut is not a cylinder, so at some hues the browser clips the result and quietly changes what the reader sees.
Choosing a hue and proving it is therefore yours, and the pull request says how you did it: [`new-course.md`](../new-course.md) carries the canvas readback that measures it.
The eyebrow rule is checked, but only once a page exists, so keep it while you write rather than finding out afterwards: two to four words is the target and about five is the limit.

### What you may rely on

Every line here is measured on published pages, and it is a promise rather than a description.

| Guarantee | Where it lives |
|---|---|
| Every colour on a page comes from a semantic token. There is not one literal hex colour in any published page. | The theme blocks in `assets/hub.css` |
| The three grid zones. `main.wrap` is one grid with the named lines `text`, `wide` and `full`: prose sits at the measure, figures and tables and code break out. | "Page chrome", above |
| The closed widget vocabulary, styled by the hub sheet and documented in this file. Nothing outside it is authored by hand. | This file |
| Type, rhythm and shape are tokens, so a rule reads a token rather than a literal. | "The design tokens", above |
| The six legacy aliases `--paper`, `--paper-2`, `--card-bg`, `--rule`, `--maxw` and `--readw` keep resolving. | `assets/hub.css` |
| The eight-colour chart ramp stays palette-independent, so a course that teaches "statistics is teal" keeps that whichever palette the reader picked. | "Inline SVG, for anything quantitative", above |
| `--gold` and `--ok` are never aliased to each other in any palette or either mode, because the capability matrix uses them for two states that make opposite claims. The print block flattens both to one ink, which is why the `absent` cell also carries the words *No equivalent*. | "The capability matrix", above |
| `.h-sub` and `.h-label` hold visual rank separately from outline rank, so a heading can be retagged for outline order without being redesigned. | "Headings", above |
| Mermaid follows the tokens for free: a new palette needs no colour table. | "Mermaid, for structure", above |
| Diagrams print as ink on paper, from a copy drawn ahead of time during browser idle. | `assets/hub.js` |
| A page renders fully styled and readable with no script at all. Anything the script adds is an enhancement, never a requirement. | Measured, and protected by every issue in this series |
| A lesson URL never changes. | `AGENTS.md`, hard rule 6 |

### What is forbidden

| Forbidden | Why |
|---|---|
| A course shipping its own colour, type, spacing or component shape in CSS. | If a course can ship a design, seventeen courses ship seventeen designs and the hub is back to the six byte-identical `course.css` forks it already paid to remove. |
| A course sheet at all, beyond the three that already exist. | A widget a second course could want has one owner, and that owner is `assets/hub.css`. `validate_site.py` fails a fourth sheet. |
| A course-local rule that restates type or spacing the design axis owns. | Measured: a course sheet sets `.metric .v` to 24px, a design rule at `:root[data-design=...] .metric .v` computes 48px and wins at `(0,2,2)` against `(0,1,1)`, and the course's considered typography is gone with nothing to warn. |
| A literal colour in a page or in an SVG. | Zero exist today. It reads in one mode, vanishes in the other, and cannot follow the print stylesheet. |
| New markup for a new design. | A design expressible as CSS over the existing markup costs three files. The same design plus one required wrapper `<div>` costs 796 pages and a migration no validator can check. This is the line to hold in every design review. |
| Uppercase body text, or a heading that runs to a full line in capitals. | Capitals read 9.53% to 19.01% slower than lowercase, and 90% of readers prefer lowercase. An eyebrow is looked at rather than read, which is why it is the one exception. |
| A token invented under a course's own selector. | The author surface is these seven. Anything else in a course block is a fork with a shorter name, and `validate_site.py` fails it. |

### The three course sheets are grandfathered, not a precedent

`llm-evolution-course`, `llm-inference-course` and `statistical-foundations-ml-course` each ship an `assets/course-extras.css`, layered after the hub sheet.
They predate this contract and they stay, because their pages link them.
No course gets a fourth.

Two of them carry a hazard worth knowing before you change a shared rule.
`llm-evolution-course` still restyles shared elements - `.stub-note h4`, `.routecard` and `.route-map .module` among them - so grep every `*.css` in the repository for a selector before you touch it, never just `hub.css`.
`statistical-foundations-ml-course` sets `.parts` and `.pn` in literal `rem` sizes and spacings, and names `--sans` and `--mono` from the registry rather than a role token, which is exactly the restatement the table above forbids: a design that moves the type scale or the face roles will not move those two rules, and the course's cards will drift out of step with everything around them.
Neither is repaired here.
They are recorded so the next change to either is made with its eyes open.

### What CI checks

`check_course_contract()` in `scripts/validate_site.py` reads the registrations straight out of `assets/hub.css` and fails on a hue with a unit, a token that is not one of the seven, a face that is not in the registry, a value outside its range, two courses on one hue, a course folder with no registration, a fourth course sheet, a design block writing a course token, and an eyebrow set in capitals that runs past five words in a segment.
Assertion A3 in `scripts/style_snapshot.py` proves the other half in a browser: it registers two throwaway courses, wears each in turn, and checks that a hue alone moves the accent and nothing else, that all seven move the two faces and the eyebrow and still nothing else, that an unregistered name is dull rather than broken, that the reader's controls keep working underneath, and that removing the block restores the page exactly.

## Printing

A lesson prints. Readers do print them, the paper is the third render state, and a rule that fixes one of the three can break another.
`hub.css` carries one `PAPER` block near the end, and everything below is what an author has to know about it.

**Paper is a set of token overrides, not a second stylesheet.**
The block redefines the semantic colour tokens - one ground, one ink - and every existing rule follows.
So a widget that reads tokens prints correctly with no work, and a widget that hard-codes a colour prints wrong with no warning.
That is the whole reason the sheet forbids a literal: a literal is unreachable from the print block by construction.

**A width media query names its medium.**
Write `@media screen and (max-width: 720px)`, never `@media (max-width: 720px)`.
A width feature is answered by the *page box* in print, and the page box is narrow: A4 inside the browser's own margins is about 717px and US Letter about 739px.
An unqualified query therefore straddles the hub's own breakpoint, so the same lesson lays out as a phone on one paper and as a laptop on the other.
This is not theoretical. It is how the rail's drawer arm reached paper, and with it a `position: fixed` scrim carrying a literal `rgb(0 0 0 / .35)` that repeated on every single printed sheet: a 35% black rectangle over all 37 pages of a lesson, in a hub whose readers print.
Check 15 in `validate_site.py` fails an unqualified width query in `hub.css` or in any course sheet.

**Every sheet says what it is.**
`@page` margin boxes carry the identity on the left and `counter(page) " / " counter(pages)` on the right.
The identity is `--print-id`, a custom property `hub.js` writes from `document.title` and `hub.css` declares a fallback for, so a page with the script removed still prints an identified sheet.
It is the one property `hub.js` may write on `<html>` that is not a reader's, and check 14 holds the two halves together.
`string-set` with `string()` is the standard way to run a heading into a margin box and was measured first: Chrome renders it on the first page and then stops, which is the one sheet that never needed it.

**Eight print tokens sit in the design block** with the rest of the type and space scale, so a second design sets its own paper: `--fs-print-body`, `--fs-print-foot`, `--fs-print-url`, `--sp-print-page`, `--sp-print-foot`, `--sp-print-figure`, `--sp-print-row` and `--sp-print-cell`.
Colour is not among them. A design carries no colour on paper any more than on screen.

**What the block does to each widget, and why.**

| Widget | On paper | Why |
|---|---|---|
| Chrome: topbar, rail, appearance panel, pager, copy buttons, reading bar, pre-production strip | Gone | Nothing on paper can be clicked. The running foot carries what the pre-production strip was there to say, on every sheet rather than one. |
| `pre`, `.term`, `.math`, `.diagram`, `table` | Wrap or fit; never scroll | A box that scrolls sideways on screen is cut at the sheet edge on paper, and the rest of the line is not merely unreachable, it is gone. |
| A Mermaid diagram | Scaled to fit the page box, both dimensions | `hub.js` draws its ink-on-paper copy off-screen with no column to fit, so it arrives at its natural size: the widest on the sample was 884px against a 587px column and the tallest 1270px against a page box near 1017px. `--sp-print-figure` is in `vh`, which is the page box in print, so one cap fits both papers. |
| An absolute link | Prints its destination after the text | Paper cannot be clicked. Relative links do not, because `../index.html` tells a reader nothing the link text does not, and the capability matrix is exempt, because 700 vendor URLs would bury the table it is trying to be. |
| A quiz | Question and options, no answer | A printed lesson has to still be answerable. `.q-fb` is hidden until the reader answers, and paper leaves that alone: a question already answered prints its feedback, one not yet answered prints as a question. |
| A practice problem | Solution open | The opposite of the quiz, deliberately. A solution sits behind a disclosure the reader chose, and printing is a request for the whole document; `hub.js` opens each one and restores it afterwards. |
| The capability matrix | Five columns, service names and cell states, no prose | The stacked phone layout printed as 105 pages. It is now 23, at the width of the page box rather than the reading measure, and the four cell states still read as shapes once colour is gone. |

**Verify a print change by printing.**
Neither CI check can see paper: `validate_site.py` does not render, and `style_snapshot.py` holds the viewport at 1280px, where the narrow arms match in no medium at all.
Produce a PDF at A4 *and* at US Letter, look at it, and check that no ink reaches the edge of a sheet.
## The design system reference page

Everything above is also *rendered*, live, at [`design-system/index.html`](../../../../design-system/index.html): every token with the value the browser resolved for it and a specimen painted by that token itself, every widget beside its markup, every reader control working, and the accessibility floor as numbers.
Open it when you are unsure what a token does, and copy the markup from it rather than from here.
It cannot go stale in the way a written list can: nothing on it restates a value, and it counts the custom properties `assets/hub.css` declares against the names it carries and says on the page which ones it misses.

**Two attributes name a token, and `validate_site.py` checks both.**
`data-token` marks the cell the page fills with the resolved value; `data-spec` marks a specimen the page's own sheet paints with that same token.
A name in either that `assets/hub.css` does not declare fails the pull request, so a rename cannot leave the reference describing something that is gone.
Any page may use them; the reference page is simply the one that does.

**Two classes belong to that page and to no lesson.**
They are furniture for showing the system, not vocabulary for teaching with, and they live in `design-system/assets/course-extras.css` rather than in the hub sheet for exactly that reason.

```html
<span class="ds-spec" data-kind="colour" data-spec="--accent"></span>
<span class="ds-spec" data-kind="size" data-spec="--fs-1">Handgloves</span>
<code data-token="--fs-1">var(--fs-1)</code>

<div class="ds-demo wide">
  <div class="card tldr">...the widget, rendered...</div>
  <div class="code-cap">the markup &middot; copy it, do not approximate it</div>
  <pre><code>...the same markup, escaped...</code></pre>
</div>
```

`.ds-spec` is one specimen and `data-kind` says which property it sets - one kind, one property, so a reader sees the token doing its own job rather than a picture of it.
`.ds-demo` pairs a rendered widget with the markup that made it; the markup goes in an ordinary `pre`, so `hub.js` gives it the copy button every code block has.

**Adding a token means adding a row there**, in the same pull request as the declaration and the first rule that reads it.
Nothing forces it - a check that failed every sibling pull request adding a token would be a check people route around - but the page says out loud when a token is missing from it, and that line is the reason to go back.

**Quotes inside a shown code block are written `&quot;`.**
A reader sees the same characters and a copy takes the same text, because `textContent` decodes the entity.
Written as plain quotes, `validate_site.py`'s link check reads a sample `href` as a link the page makes and fails on a file that was never meant to exist.
