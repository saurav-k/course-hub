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

### The part eyebrow, `.part-eyebrow`

Optional, and it sits directly above `.eyebrow`.
Where a page also carries a breadcrumb it goes below that, because navigation comes before the page's own labels.
It names the division of the course this page belongs to, which is the one piece of bearing the rest of the head block does not carry: `.eyebrow` says which module and which lesson, and this says which part of the whole.

```html
<div class="part-eyebrow"><span>Part II / Methods and semantics</span><span>Where the argument turns</span></div>
```

One span or two.
The first is the part itself and is the only one that matters.
A second span is the part's own subtitle, and it prints faint at the far end of the row.
It needs no class of its own: the row can tell one span from two without being told.
Each span is a cell of the row, so keep a cell's own markup inside its span; bare text beside a span reads as a second cell and is pushed to the far end.
Write both in sentence case and let the stylesheet decide about capitals, exactly as `.eyebrow` is written: the row takes the course's own eyebrow face, tracking and case from the design in force.

It is a row rather than a label, and the hairline under it is what makes it read as a divider of the course rather than as a second caption.
The rule's style is `--part-rule-style`, so the House design draws it solid and Press draws it dashed.

Do not put one on every page of a course that has no parts.
The widget answers "where am I in the whole", and a course whose whole is one sequence has already answered it in the eyebrow.

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

### The numbered section badge, `.numbered`

Optional, and one class on the container does the whole job.

```html
<main class="wrap numbered">
  <h2>What routing is</h2>
  <h2>The keeper and the viewer</h2>
</main>
```

Every `h2` that is a direct child of the container gets a filled square in front of it carrying its number: `01`, `02`, `03`.
Nothing is written on the headings, and nothing may be.
The numbers come from a CSS counter, so they cannot drift from the headings the way a typed number does, and adding a section in the middle renumbers the rest with no edit anywhere.

Four things to know before you use it.

**It is opt-in, and that is the point.**
A course map and a reference sheet are lists rather than arguments, and neither is a numbered sequence.
Put `.numbered` on the pages that really do proceed in sections.

**`.h-label` and `.h-sub` are stepped over.**
Both are `h2` tags wearing a smaller face - "The one-minute version" is the common one - and neither is a section of the argument, so neither takes a number and neither advances the count.

**The number is not part of the heading's accessible name.**
The badge is drawn with empty alternative text, so a screen reader announces "The keeper and the viewer" rather than "02 The keeper and the viewer".
It is decoration beside a heading, and the heading's own name is what a reader navigates by.

**One rule above the heading, never two.**
An `h2` already carries a hairline above it.
Do not add a second rule under the heading to go with the badge; the sheet ships one and one is what the page should have.

Inline markup inside a numbered heading behaves exactly as it does in any other heading: the badge hangs in a gutter beside the block rather than turning the heading into a row of boxes, so `Practice <span class="note-sm">about 15 minutes</span>` still reads as one line and still wraps.

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

### What a figure is

Four parts, in this order, and the order is the point.

```html
<figure class="diagram">
  <div class="fig-cap">How the two summaries move</div>
  <div class="fig-claim">The mean is dragged past nine of the ten days. The median is not.</div>
  <div class="mermaid">
flowchart LR
  A["Observed data"] --> B["Estimate"]
  </div>
  <figcaption>Plain English reading of the figure, with <b>the one takeaway in bold</b>.</figcaption>
</figure>
```

| Part | What it is | Length |
|---|---|---|
| `.fig-cap` | the **subject**. What the drawing is of. | 2 to 5 words, and 5 is a gate |
| `.fig-claim` | the **claim**. What the drawing proves. | one sentence, under 15 words |
| the drawing | `div.mermaid` or `svg.chart` | - |
| `<figcaption>` | the reading, with the bolded takeaway | as short as it can be and still teach |

The reader meets the label, then the claim, then the picture.
The picture answers a question that has already been asked, which is why the two lines go above and the reading stays below.

**`.fig-cap` names and never argues. `.fig-claim` argues and never describes the picture.**
Neither is ever a question.
Measured across the 94 figures the anatomy comes from: zero question marks in either line, median 3 words in the label and 11 in the claim.
An author who is choosing what kind of sentence to write has already put the wrong thing in one of them.

Write `.fig-cap` in sentence case.
The stylesheet upper-cases it, and it takes the eyebrow family, tracking and case from the design in force, so it is mono under Press and Inter under House with the page naming no face.
Both lines cost no colour: the label is `--accent-2` and the claim `--ink`, which the contrast matrix already holds over the diagram card in every palette, both modes and every course hue.

**Five words is the ceiling, and it is the eyebrow's rather than a second number.**
`.fig-cap` wears the eyebrow treatment, so `validate_site.py` holds it to exactly the limit a page's own `.eyebrow` already answers to: no more than five words in a segment while the case is uppercase, because capitals read 9.53% to 19.01% slower than lowercase.
The house target is two to four.
A label that needs more than five words has stopped naming a subject and started making the claim, which is the line below it.

A figure may carry neither line.
It may not carry only the claim.
**A `.fig-claim` with no `.fig-cap` above it is a proposition with no subject, and it reads as a stray sentence that lost its paragraph.**
Check 19 in `scripts/validate_site.py` fails that, and three other shapes with it.

The pair is not required on an existing figure and never will be by machine.
A label cannot be generated: the measured pass over the hub's own 2,934 captions produces 434 figures all labelled WHERE THIS SITS and 173 labelled FIGURE 1, FIGURE 2, FIGURE 3, which is worse than no label.
The bar for a page you are writing now is in [`pedagogy.md`](pedagogy.md).

### Two ways the caption pair breaks silently

- **`.fig-cap` and `.fig-claim` are direct children of `figure.diagram`, in that order, before the drawing.** The stylesheet selects them as `figure.diagram > .fig-cap`, so one wrapped in a `<div>` for spacing takes no styling at all and renders as unstyled body text at figure width. Nothing reaches the console and the page still validates against every other check.
- **Write the label in sentence case, never in capitals of your own.** The stylesheet upper-cases it, so `WHERE THIS SITS` and `Where this sits` are the same pixels under the default treatment and the mistake is invisible on the page you wrote it on. A course that sets `--eyebrow-case: none`, which the course contract allows, then renders your capitals as capitals, on a page nobody is going to look at again. The treatment is the stylesheet's decision, and a page that takes it back has taken a reading-speed penalty nobody asked for.

The rule mark is not one of them, and it used to be.
It rides the first line by a half-line offset rather than by centring on the box, so a label that wraps keeps its anchor and its second line stays indented under its first.
That was worth fixing rather than documenting: measured at 320px, a five-word label wraps under Press and a six-word one under House, both inside the bar above, so the wrap is reachable by an author who did nothing wrong.

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

### Compose the figure the idea needs

There is no catalogue of approved pictures and there is not going to be one.
A figure nobody has drawn before is the **expected** outcome of a page with a new idea in it, not an exception you have to justify.
If the drawing in your head is not in this file, draw it.

Six things must hold, whatever you compose.
They are the whole list.

1. **Colour comes from a token.** A class, or `var(--token)`. Never a value, in any spelling. This is what lets a figure follow seven palettes, two modes and paper without you thinking about it.
2. **It has an accessible name.** `role="img"` and an `aria-label` that says what the drawing shows, not what it is called.
3. **It scales.** A `viewBox`, never a `width`/`height` pair.
4. **No new dependency.** No chart library, no build step, no CDN, no network at render time.
5. **It works offline**, from a file, with script blocked.
6. **It prints.** Which the first rule already gives you.

Everything else in this section is guidance from figures that worked.
Guidance tells you what has usually been true; it does not tell you what you may draw.
Where a rule below names an instrument - chart or diagram - it applies to that instrument and not to the other.

The one thing on that list with a footnote is the arrowhead.
`#hub-arrow` is injected by `hub.js`, so with the script blocked a `d-flow` connector still draws, in the right colour, and loses only its head.
Never rest a figure's direction on the arrowhead alone: let the layout, the labels or a verb carry it too, and the head becomes confirmation rather than the whole claim.

### Which of the three to draw

Three instruments, and most technical pages need at least two of them.

| Instrument | The question it answers | Reach for it when |
|---|---|---|
| a **chart** (`svg.chart`, `m-*` `s-*` `f-*`) | *how much* | a quantity, a distribution, a density, a band, a comparison of sizes |
| a **diagram** (`svg.chart`, `d-*`) | *what is where* | boxes, boundaries, a labelled connector, state, an addressed row, anything positioned on purpose |
| **Mermaid** (`div.mermaid`) | *what connects to what* | a graph whose layout you do not care about: any sane arrangement will do |

**Mermaid's strength is that it lays the graph out for you, and that is also when to stop using it.**
The moment position carries meaning - an offset axis under a row of cells, two panels aligned row by row, a thing that sits *inside* a boundary - Mermaid has no way to express it, because a Mermaid node has no position you chose.
Draw it by hand instead.

A page whose figures are all the same instrument has probably not asked what the reader is actually confused about.

**Those three instruments draw. Five more are figures the reader operates.**
A drawing answers a question the reader has already asked; an interactive figure answers one they have not, because they have to move something before the answer appears.
Reach for one when the claim is a *consequence* rather than a fact: the thing that changes when you change something else.

| Shape | The question it answers | Reach for it when |
|---|---|---|
| a **stepper** (`figure.stepper`) | *what happens next, and what it cost* | a trace, a protocol exchange, a loop, a pipeline: anything with a real order and a running total |
| an **assembler** (`figure.assembler`) | *what goes in the file* | a config, a memory file, a prompt, a manifest, where the lesson is which parts belong and what each one costs |
| a **calculator** (`figure.calc`) | *how much, at your numbers* | a cost, a budget, a rate, a fleet: an arithmetic claim the reader should test against their own scale |
| a **scorecard** (`figure.scorecard`) | *where do I stand* | a readiness check, an audit, a maturity question, where the teaching is the list of fixes rather than the number |
| a **taint map** (`figure.taint`) | *who wrote this* | a trust boundary: which parts of one turn, one request or one document came from somebody who is not the reader |

The five sections at the end of this file carry the markup for each, character for character.
**A figure a reader can operate is not a substitute for a drawing.**
A page whose only figure is a slider has not shown the reader the shape of the thing; the interactive shapes sit beside the three instruments above rather than in place of them.

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
A `flowchart` grows along its stated direction and *unboundedly* across it, so a `TB` graph with several independent roots, or one whose subgraphs sit side by side, lays out wider than the reading column and is clipped at the column edge. Nothing reports it: `validate_site.py` and `check_pages.py` both pass, no console message appears, and the figure looks complete until you notice a node missing at the right. Turn the direction so the many-node axis runs down the page, or cut the row to three or four nodes, and measure the rendered `svg` against its `figure` rather than trusting the source.

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

### A chart, when the claim is a quantity

Mermaid cannot draw a distribution, a density, a confidence band, or a scatter plot, and it cannot put one saturated mark in a neutral field so that the colour is the argument.
That last one is a real reason to draw by hand: a figure whose whole point is *this one thing, among these others* is clearer when nine tenths of it is unpainted.
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

- Always a `viewBox`, never a `width`/`height` pair. Around `640 x 300` keeps 13px text readable. This one holds for both instruments.
- Always `role="img"` and an `aria-label` saying what the chart shows. This one holds for both instruments too.
- **Colour comes only from the semantic classes**, or from a `var(--token)` naming one of them. A literal hex looks right in one theme and vanishes in the other, and it cannot follow the print stylesheet either.
- **In a chart, colour marks the subject and the field stays neutral.** The field is `panel`, `grid`, `axis` and `ink`; roughly a tenth of the canvas carries the saturated mark. If every series is saturated the chart has no subject, and the reader has to be *told* which one matters instead of seeing it. **This is a charting rule and it stops here.** In a diagram a filled box is a state, so fill as much as the idea needs - see the section below.
- **A figure is usually wider than it is tall**, because a tall one interrupts the column. The hub's own median is 2.13:1 and a `640 x 300` viewBox is a good default. There is no ratio to hit.

> **Two rules were deleted from this list in 2026-08, and it is worth knowing why.**
> A "house shape" of 3.43:1 and a hard 10% paint ceiling were both measured on the reference site's corpus and then applied to ours without anybody checking them against our own work.
> Measured: **755 of our 763 hand-drawn figures - 99% - sit below 3.43:1**, and **44% exceed the paint ceiling**, including figures the captain singled out as the ones he wanted more of.
> A rule the whole corpus breaks is not a standard, it is a trap for the next author, and it was the mechanism keeping the box shut.
> If you find yourself about to write a rule in this file from a number you measured somewhere else, measure it here first.

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

`fill="var(--token)"` and `style="fill:var(--token)"` are both legitimate and both already in use across the hub.
Reach for one when no class says what you mean and the colour is genuinely a one-off; name a **semantic** token - `--ok`, `--warn`, `--gold`, `--accent-2`, `--surface-2`, `--line-strong`, `--ink-faint` and their `-soft` partners - and never a raw `--l-*` or `--d-*`, which belong to the terminal transcript and to nothing else.

### A diagram, when the claim is a structure

A chart says how much. A diagram says what is where.
Both are `svg.chart`, so a diagram inherits the frame, the text sizing, the tabular figures and the print behaviour; what it adds is the shapes a chart has no use for.

Until 2026-08 there were none of those shapes.
The 45-class set was a statistics-plot set, `<marker>` appeared **once in 763 figures**, and there was no box, no connector, no state and no way to set machine text inside a drawing.
So every directed arrow in the hub was a Mermaid arrow, and an author who wanted an architecture drawing had nowhere to go.
These eleven classes are that gap closed.

| Class | What it draws | What it means |
|---|---|---|
| `d-box` | a filled box with a strong edge | a thing: a component, a cell, a participant |
| `d-bound` | an unfilled box with a heavier edge | a boundary: a process, a host, a trust zone, drawn *around* things |
| `d-focus` | an accent fill and an accent edge | **the one under discussion** - at most one or two per figure |
| `d-keep` | an `--ok` fill and edge | kept, written, retained, passing |
| `d-drop` | a `--warn` fill and edge | dropped, evicted, rejected, failing |
| `d-absent` | no fill, a dashed faint edge | not yet: unwritten, unallocated, the next one |
| `d-ghost` | a faint box at 45% opacity | no longer, or "and so on" |
| `d-flow` | a connector with an arrowhead | a direction: a call, a write, a read, a move |
| `d-flow ref` | the same, dashed | a weaker link: optional, asynchronous, implied |
| `d-mono` | text in the mono face, small and soft | machine text: an offset, a key, a wire value, a file name |
| `read` | italic text in full ink | the sentence the figure says out loud |

Four things about them, and each is the reason a rule is written the way it is.

- **Fill is a state, not decoration.** A row of `d-keep` cells with one `d-absent` at the end is a claim about the row. That is why the charting paint rule is scoped to charts and does not reach here.
- **A connector takes its colour from a paired `s-*` class, and the arrowhead follows.** `class="d-flow s-alarm"` is a red line with a red head; `class="d-flow"` alone is a neutral one. The head fills with `context-stroke`, so it can never disagree with the line it sits on, and you never state a colour to get one.
- **`d-mono` is what makes a drawing read as a machine.** The reference corpus uses a mono face inside a figure 504 times; before this we had no way to.
- **Text inside a `d-*` box is `lbl-b`, never `lbl-on`.** `lbl-on` is `fill: var(--surface)`, the page's own ground, and it is meant for a saturated `m-*` mark. Every `d-*` fill is a `-soft` tint of that same ground, so a label written `lbl-on` inside one is near-invisible in both modes, at every palette, and nothing reports it: the element is in the DOM and the contrast matrix only measures the tokens, not which label was put on which fill.

#### The worked example

An append-only log, addressed by offset.
Mermaid cannot draw this, and the reason is exactly the one in the table above: **position on the line is the address**, and a Mermaid node has no position you chose.

```html
<figure class="diagram">
  <div class="fig-cap">Append-only, offset-addressed</div>
  <div class="fig-claim">Writes go to the tail; the offset is a permanent address.</div>
  <svg class="chart" viewBox="0 0 640 240" role="img" aria-label="An append-only log of four
       written events and one not-yet-written cell at the tail, with producers appending at the
       tail, an offset axis beneath the written cells, and three consumers each sitting under the
       offset it holds">

    <rect class="d-box" x="20" y="20" width="100" height="30" rx="5"/>
    <text class="lbl-b" x="70" y="40" text-anchor="middle">producers</text>
    <path class="d-flow s-alarm" d="M122 36 C240 20 380 20 504 66"/>
    <text class="d-mono" x="180" y="46">append</text>

    <rect class="d-keep"   x="150" y="70" width="72" height="36" rx="4"/>
    <text class="d-mono"   x="186" y="92" text-anchor="middle">e0</text>
    <rect class="d-keep"   x="230" y="70" width="72" height="36" rx="4"/>
    <text class="d-mono"   x="266" y="92" text-anchor="middle">e1</text>
    <rect class="d-keep"   x="310" y="70" width="72" height="36" rx="4"/>
    <text class="d-mono"   x="346" y="92" text-anchor="middle">e2</text>
    <rect class="d-focus"  x="390" y="70" width="72" height="36" rx="4"/>
    <text class="d-mono"   x="426" y="92" text-anchor="middle">e3</text>
    <rect class="d-absent" x="470" y="70" width="72" height="36" rx="4"/>
    <text class="d-mono"   x="506" y="92" text-anchor="middle">...</text>
    <text class="d-mono"   x="552" y="92">tail</text>

    <text class="d-mono" x="186" y="124" text-anchor="middle">0</text>
    <text class="d-mono" x="266" y="124" text-anchor="middle">1</text>
    <text class="d-mono" x="346" y="124" text-anchor="middle">2</text>
    <text class="d-mono" x="426" y="124" text-anchor="middle">3</text>
    <line class="axis" x1="150" y1="136" x2="462" y2="136"/>
    <line class="tick" x1="186" y1="136" x2="186" y2="142"/>
    <line class="tick" x1="266" y1="136" x2="266" y2="142"/>
    <line class="tick" x1="346" y1="136" x2="346" y2="142"/>
    <line class="tick" x1="426" y1="136" x2="426" y2="142"/>
    <text class="d-mono" x="140" y="140" text-anchor="end">offset</text>

    <path class="d-flow s-signal" d="M186 146 L186 172"/>
    <rect class="d-box" x="152" y="176" width="68" height="28" rx="4"/>
    <text class="lbl-sm" x="186" y="194" text-anchor="middle">C @ 0</text>
    <path class="d-flow s-signal" d="M266 146 L266 172"/>
    <rect class="d-box" x="232" y="176" width="68" height="28" rx="4"/>
    <text class="lbl-sm" x="266" y="194" text-anchor="middle">B @ 1</text>
    <path class="d-flow s-signal" d="M426 146 L426 172"/>
    <rect class="d-box" x="392" y="176" width="68" height="28" rx="4"/>
    <text class="lbl-sm" x="426" y="194" text-anchor="middle">A @ 3</text>

    <text class="read" x="320" y="228" text-anchor="middle">Each consumer keeps its own
      position, so reading one event never removes it.</text>
  </svg>
  <figcaption>Every mark takes its colour from a token, so this follows seven palettes and both
    modes. <b>A log is addressed by position, which is why one reader cannot consume another's
    event.</b></figcaption>
</figure>
```

It paints far more than a tenth of its canvas and it runs at 2.7:1, so under the two deleted rules it was twice wrong.
It is the figure the captain asked for.

Read the geometry as carefully as the classes, because that half is nobody's job but yours.
Each consumer sits directly under the offset it holds, so no connector crosses a cell, a label or another connector; the append arc travels over the row and lands on the tail, because the claim is that writes go to the tail and an arrow pointing anywhere else would contradict it; and the axis stops at `e3`, because the unwritten cell has no offset yet.
An earlier draft of this same figure crossed the offset labels with two connectors and pointed the append arrow at `e0`, and it validated.

#### The states, side by side

The remaining structural classes, which the worked example above has no use for:

```html
<svg class="chart" viewBox="0 0 640 150" role="img" aria-label="The structural states">
  <rect class="d-bound" x="12"  y="26" width="120" height="58" rx="6"/>
  <rect class="d-box"   x="24"  y="40" width="96"  height="30" rx="4"/>
  <rect class="d-drop"  x="360" y="40" width="88"  height="30" rx="4"/>
  <rect class="d-ghost" x="552" y="40" width="72"  height="30" rx="4"/>
  <path class="d-flow ref" d="M540 55 L548 55"/>
</svg>
```

`d-bound` is drawn *around* the things it contains rather than beside them, which is the whole difference between a boundary and a box.
All eleven are rendered together, live and in both modes, at `design-system/index.html`.

### What the checks catch, and what rests on your judgement

The licence to compose is real, and so is the cost: more freedom is more ways to be wrong.
Building the prototype for this vocabulary produced **five defects that no check in this repository catches**, and one of them was semantic - a box drawn `d-ghost`, meaning removed, while being drawn a live connector, meaning reading. Every check passed.

**Caught by machine, on the pull request:**

| What | By |
|---|---|
| a colour written as a value, in any of the four spellings - `fill="#hex"`, `style="fill:#hex"`, `rgb()`/`hsl()`/a named colour, a Mermaid `classDef` | `check_pages.py`, FAIL, and it names the offending value |
| a misspelled `d-*`, `m-*`, `s-*`, `f-*`, `t-*` or `sw-*` class | `check_pages.py`, FAIL |
| an `svg.chart` with no `viewBox` or no `aria-label` | `check_pages.py`, FAIL |
| the caption pair's shape, order and length | `validate_site.py` check 19, `check_pages.py` |
| every token the vocabulary uses, over seven palettes and two modes | `contrast_matrix.py` |

**Not caught by anything. These are yours:**

- **Roles that contradict each other.** A `d-ghost` box with a live `d-flow` into it. The colour says gone, the arrow says busy, and the figure teaches the wrong thing while passing every gate. This is the worst of them and it is new with the licence.
- **Text that runs past the frame.** SVG text does not wrap and is clipped at the `viewBox` edge with nothing reported. Read the longest line in every figure, at 360px and at full width.
- **Connectors that cross labels, axes or each other.** Geometric nonsense renders perfectly.
- **A figure that is illegible at 360px.**

So: **open the page in a browser and look at the figure.** Not at the markup, and not at the console, which stays clean through all four.

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

## Five figures a reader operates

A stepper, an assembler, a calculator, a scorecard and a taint map.
Each one is a figure the reader operates rather than reads, each is built into `assets/hub.css` and `assets/hub.js`, and no course writes a line of JavaScript to use one.
`design-system/index.html` renders all five live, under "Five figures a reader operates", with the markup beneath each.

Five properties hold across all five, and each one is a rule rather than a habit.

1. **The data is markup.** A step, a part, a row and a block is an element you wrote. Nothing here reads a data file, so the figure prints, is searchable, is read by a screen reader before `hub.js` runs, and cannot fall out of step with a second file. The capability matrix below is the one widget that earned an external data file, and it took 191 rows to earn it.
2. **Script blocked is a complete page.** Every rule that hides part of one of these is keyed on an attribute only `hub.js` writes, so a page with no script shows every step, every fix and every block. The assembler goes furthest: you commit the assembled file into its `<pre>`, and the script's first act is to render it again from the boxes.
3. **Controls are native elements inside a `<label>`.** Buttons, checkboxes, radios and ranges, exactly as `.build-controls` already requires. Keyboard behaviour, focus rings and accessible names come from the platform; do not rebuild them.
4. **The frame is `.diagram` and the two service rows are `.build-controls` and `.build-readout`.** A figure wears `.diagram` plus its own class - `class="diagram stepper"` - so the frame, the shadow and the caption pair keep one owner, and `figure.diagram > .fig-cap` still selects the label. Never give one of these a frame of its own.
5. **Nothing persists.** No reader's answer outlives the page. If one of these ever needs to remember something it goes through `setChecked` / `dropChecked`, never `set` / `drop`, for the reason the study notes panel carries.

The caption pair and the `figcaption` are not optional here.
A figure a reader can operate still has to say what it is, what it proves, and what they should have noticed.

**Give the figure an `id`.**
`hub.js` names the region a control acts on by borrowing the figure's own id - `agents-md-builder` becomes `agents-md-builder-file` - and writes `aria-controls` on every checkbox and every button pointing at it.
A figure with no `id` gets no `aria-controls` at all, silently: it looks identical, it validates, and a screen reader is left with a checkbox that changes something unnamed.
Every markup block below carries one for that reason and not for the link.

**The accessible state is the runtime's, and there are two ways to break it from a page.**
`hub.js` marks the `.build-readout` `aria-live="polite"`, so whatever the reader moved is announced without taking focus off the control they are still holding: write the readout as words around the number - `step 1 of 3`, not a bare `1` - because the announcement is the whole row.
And **never write `disabled` on a control in one of these**. A disabled button drops out of the tab order under the reader's finger; the runtime marks a control that cannot act `aria-disabled` and leaves it focusable, and a `disabled` attribute in the page would undo that on the one control the reader was about to press.

**Every one of these is operated by keyboard before it is done.**
The controls are native, so the behaviour is the platform's and there is nothing to build - which is exactly why it goes unchecked.
Tab to each control, drive it from the keyboard, and confirm the ring: `scripts/focus_walk.py` proves the ring exists and nothing proves the figure responds.
[`verify.md`](verify.md) carries the pass, one page per shape.

**What `scripts/check_pages.py` makes of one.**
An interactive figure is a `<figure>`, so it counts toward the page's diagram floor and toward the
words-per-figure ceiling, and it is held to the same caption bar: a `figcaption` with a bolded
takeaway, and a well-formed caption pair above it.
It contributes **no diagram kind**, because it draws nothing.
A page whose only figures are these will pass the count and warn on the kind floor, which is the
right answer: the interactive shapes sit beside a chart, a hand-drawn diagram or a Mermaid graph
rather than in place of one.

### The stepper, for a trace with an order and a cost

Plays an ordered list of turns one at a time.
Reach for it when the claim is a *sequence*: a tool-call loop, a protocol exchange, a pipeline, a review that goes round twice.

```html
<figure class="diagram stepper" id="loop-trace">
  <div class="fig-cap">One task through the loop</div>
  <div class="fig-claim">Two model calls and one tool result answer one sentence.</div>

  <ol class="step-list">
    <li class="step" data-actor="user" data-cost="34">
      <span class="step-role">prompt</span>
      <span class="step-body">Rename <code>parse()</code> to <code>parseHeader()</code> everywhere.</span>
    </li>
    <li class="step" data-actor="model" data-cost="1842">
      <span class="step-role">model call</span>
      <span class="step-body">Emits a <code>tool_use</code> block: grep the tree for <code>parse(</code>.</span>
    </li>
    <li class="step" data-actor="tool" data-cost="410">
      <span class="step-role">tool result</span>
      <span class="step-body">Seven hits across four files, handed back as text nobody has read yet.</span>
    </li>
  </ol>

  <div class="build-readout">
    <span>step <b data-step-out="index">1</b> of <b data-step-out="total">3</b></span>
    <span>context <b data-step-out="cost">34</b> tokens</span>
  </div>
  <figcaption>Play it once through and watch the token count rather than the prose.
  <b>Every capability you notice is a tool the loop dispatched, not a thing the model did.</b></figcaption>
</figure>
```

- **`data-actor`** is the only styling hook and it takes four values: `user` is `--accent-2`, `model` is `--accent`, `tool` is `--ok`, `error` is `--warn`. The colour rides the left rule and the role chip together, never the colour alone.
- **`data-cost`** is optional and is summed over everything played so far. A step with none counts zero.
- **`.step-role`** is two or three words, lower case; the stylesheet upper-cases it. **`.step-body`** is one sentence.
- **The step number is a CSS counter**, so inserting a turn in the middle renumbers the rest for free. Never type one.
- **`hub.js` injects Back, Next and Restart** into a `.build-controls` row above the readout. You write no controls.
- **`[data-step-out]`** takes `index`, `total`, `cost` and `left`. Commit the value each one has at step one, because that is what a page with no script shows.
- The step ahead of the reader keeps its row and loses its body, so the figure never jumps and the reader can see how much trace is left.

### The assembler, for a file built out of choices

Concatenates the ticked parts into a real file.
Reach for it when the lesson is *what belongs in something* and what each part costs: a memory file, a config, a system prompt, a manifest.

```html
<figure class="diagram assembler" id="agents-md-builder">
  <div class="fig-cap">What belongs in the file</div>
  <div class="fig-claim">Every line you add is prepended to every request you ever send.</div>

  <div class="build-controls">
    <label><input type="checkbox" data-part="build" checked> build and test commands</label>
    <label><input type="checkbox" data-part="layout"> where things go</label>
  </div>

  <div class="asm-out">
    <div class="code-cap">AGENTS.md &middot; assembled from the boxes above</div>
    <pre><code># Commands

npm test        # the whole suite, about 40 seconds

# Layout

src/      one module per directory, no index barrels
</code></pre>
  </div>

  <template data-part="build"># Commands

npm test        # the whole suite, about 40 seconds</template>
  <template data-part="layout"># Layout

src/      one module per directory, no index barrels</template>

  <div class="build-readout">
    <span>about <b data-asm-out="tokens">28</b> tokens, on every turn</span>
    <span><b data-asm-out="parts">2</b> of 2 sections</span>
  </div>
  <figcaption>Tick only what the repository cannot show the agent itself.
  <b>A memory file is a per-turn cost, not a wiki.</b></figcaption>
</figure>
```

- **One `<template data-part="...">` per part**, and one checkbox carrying the same `data-part`. The parts assemble in the order the *checkboxes* are written, not the order the templates are.
- **The `<pre><code>` ships assembled**, holding every part joined by a blank line. That is what a page with no script shows and what prints, so it has to be right by hand: it is the one place in these five where a committed default can drift. The templates are the source of truth; make the `<pre>` match them.
- **A template's body is dedented** before it is written out, so you may indent it to sit in the page.
- **`[data-asm-out]`** takes `tokens`, `chars`, `lines` and `parts`. The token count is characters divided by four and is an estimate: say "about" wherever you print one, because no tokeniser ships in `hub.js` and none is going to.
- **`hub.js` appends a `.asm-cost` chip to each label** showing what that part costs. You write no chip.
- The copy button on the `<pre>` is the one `hub.js` puts on every `<pre>`, so it needs no code here.
- **The assembled file is written into `.asm-out pre code`, named through the `pre`.** So a `.code-cap` above it is free to name its file in `<code>`, which is how a caption should name a file. It was not always: the runtime took `.asm-out code`, the first `code` in the block, and on the one page whose caption used one the 773-character file was written into the caption line while the `<pre>` never moved from what the page committed. The readout beside both updated correctly, so every check passed and the figure was wrong on first paint. The rule is now the runtime's rather than the author's, and it is written here because the shape of the defect is the lesson: an interactive figure can be inert and still report the right numbers.

### The calculator, for an arithmetic claim at the reader's own numbers

Sliders in, two derived numbers out.
Reach for it when a claim is *linear in something the reader can name*: a bill, a budget, a rate, a fleet.

```html
<figure class="diagram calc" id="fleet-bill">
  <div class="fig-cap">What the fleet costs</div>
  <div class="fig-claim">Cost is linear in agents and in turns.</div>

  <div class="build-controls">
    <label>agents <input type="range" data-var="a" min="1" max="20" step="1" value="4"></label>
    <label>turns per task <input type="range" data-var="t" min="4" max="60" step="2" value="18"></label>
    <label>tokens per turn <input type="range" data-var="k" min="2000" max="60000" step="1000" value="14000"></label>
  </div>

  <div class="build-readout">
    <span>tokens per hour <b data-calc="product" data-of="a t k">1,008,000</b></span>
    <span>at $3 per Mtok <b data-calc="scale" data-of="a t k" data-by="0.000003" data-decimals="2" data-prefix="$">$3.02</b></span>
  </div>
  <figcaption>Move the middle slider first and watch which number moves with it.
  <b>Turns per task is the only term you can actually change.</b></figcaption>
</figure>
```

- **Two operations, and there is no third.** `product` multiplies the variables `data-of` names; `scale` multiplies that product by the constant in `data-by`. **There is no expression language and no `eval`**, and a page that needs a third operation adds a named one to the closed set in the same three-part pull request every widget change takes.
- **`data-var`** names a variable; `data-of` is a space-separated list of those names. An unknown name writes nothing at all, so the figure keeps its committed default rather than showing a reader `NaN`.
- **`data-decimals`, `data-prefix` and `data-suffix`** are optional and format the output. Thousands are grouped for you.
- **Commit the correct value** for the defaults you shipped. A page with no script shows exactly those numbers, so a wrong one is a wrong lesson on paper.
- **`hub.js` injects a `.calc-val` output beside each range**, because a slider whose number the reader cannot see is a control they are guessing at. You write no output.
- A `data-decimals` on a range formats that slider's own readout.

### The scorecard, for a weighted readiness check

Radios in, a weighted total, a meter and a band out.
Reach for it when the teaching is the *list of fixes* rather than the number: an audit, a readiness check, a maturity question.

```html
<figure class="diagram scorecard" id="agent-ready-score" data-bands="0.5 0.8" data-band-names="not started|under way|agent-ready">
  <div class="fig-cap">Is this repository agent-ready</div>
  <div class="fig-claim">Every point maps to one change you could make this week.</div>

  <ol class="score-rows">
    <li class="score-row" data-weight="3">
      <span class="score-q">One documented command runs the whole test suite.</span>
      <span class="score-opts">
        <label><input type="radio" name="ar-1" value="0"> no</label>
        <label><input type="radio" name="ar-1" value="1"> partly</label>
        <label><input type="radio" name="ar-1" value="2"> yes</label>
      </span>
      <span class="score-fix">Put it in <code>AGENTS.md</code> and make it the only one.</span>
    </li>
  </ol>

  <div class="build-readout">
    <span>score <b data-score-out="points">0</b> of <b data-score-out="max">6</b></span>
    <span><b data-score-out="band">not started</b></span>
  </div>
  <figcaption>Answer for a repository you actually own, not for the one you wish you had.
  <b>The blockers are boring, repeatable, and none of them is the model.</b></figcaption>
</figure>
```

- **The score is each radio's `value` times its row's `data-weight`**, and the maximum is the highest option on each row times the same weight. A row with no `data-weight` counts once.
- **Every row needs its own `name`.** Two rows sharing one is one question with six options, and nothing warns you.
- **`data-bands`** is two fractions of the maximum and **`data-band-names`** is three names separated by `|`. Both are optional and default to `0.5 0.8` and `not started|under way|ready`.
- **`[data-score-out]`** takes `points`, `max`, `percent`, `answered`, `rows` and `band`.
- **`.score-fix` is always visible and is always your own words.** It is the teaching, and revealing it only on a low score would make the widget a quiz. It is also what makes the printed figure a usable checklist, which is why the fix text is never generated.
- **`hub.js` injects the `.score-meter`, its `.score-fill` and a `.score-weight` chip** on each question. You write none of them.

### The taint map, for a trust boundary inside one turn

Splits one turn by who wrote each block.
Reach for it when the confusion is *provenance*: which parts of a request, a document or a context window came from somebody who is not the reader.

```html
<figure class="diagram taint" id="where-injection-enters">
  <div class="fig-cap">One turn, by origin</div>
  <div class="fig-claim">Three of these five blocks were written by somebody who is not you.</div>

  <div class="taint-turn">
    <p class="taint-part" data-origin="you">Fix the failing test in <code>parser_test.go</code>.
      <span class="taint-can">The only block in the turn you actually authored.</span></p>
    <p class="taint-part" data-origin="repo">AGENTS.md: run <code>go test ./...</code> before any commit.
      <span class="taint-can">Read as an instruction, which is what it is, and reviewed like code.</span></p>
    <p class="taint-part" data-origin="foreign">Issue body, opened this morning by an outside contributor.
      <span class="taint-can">Reaches every tool this turn holds, the shell included.</span></p>
  </div>

  <div class="build-controls">
    <label><input type="checkbox" data-taint="foreign" checked> show what you did not write</label>
    <label><input type="checkbox" data-taint="capability"> show what the agent may do with it</label>
  </div>
  <div class="build-readout">
    <span><b data-taint-out="foreign">1</b> of <b data-taint-out="total">3</b> blocks are foreign</span>
  </div>
  <figcaption>Untick the first box: all three arrive as one flat prompt, and that is the model's view of the turn.
  <b>The model has no way to tell them apart, so the boundary has to be a permission.</b></figcaption>
</figure>
```

- **`data-origin`** takes three values and three existing tokens: `you` is `--accent-2`, `repo` is `--ink-faint`, `foreign` is `--warn`. There is no fourth, and adding one is a change to the shared sheet rather than to a page.
- **The origin word is generated from the attribute**, so a block can never be labelled one thing and coloured another, and no page can misspell it. Write no chip.
- **`.taint-can` is optional, one per block, and is yours to write.** What an agent may do with a block is a claim about a real system and belongs where a reviewer can argue with it.
- **`data-taint="foreign"`** toggles the origin colouring and **`data-taint="capability"`** toggles the `.taint-can` lines. Ship the first checked and the second unchecked, which is what the committed page shows.
- **`[data-taint-out]`** takes `you`, `repo`, `foreign` and `total`.
- **The state that teaches is the one with the first box unticked**, where every block looks identical. That is the model's view of the turn, and the figcaption should say so.

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
| Type scale | 64 | `--fs-1` to `--fs-4` are the four heading sizes, `--fs-body`, `--fs-lead`, `--fs-ui`, `--fs-sm`, `--fs-xs`, `--fs-foot` and `--fs-mono` the named roles, and the rest are component sizes named for the component. `--fs-body` and `--fs-mono` are derived, not set; see the derived axes below. |
| Leading | 15 | `--lh-tight` for headings, `--lh-body` for prose, then one per component role. `--lh-body` carries the measure nudge; see the derived axes below. |
| Weight | 6 | `--fw-normal` 400, `--fw-medium` 600, `--fw-strong` 650, `--fw-bold` 700, `--fw-metric` 750, `--fw-heavy` 800. |
| Tracking | 14 | Negative on display type, positive on anything set in capitals. |
| Space | 184 | Two layers, five of them the printed page's; see below. |
| Reading frame | 3 | `--measure-chars-default`, the column width in real characters, and `--wide-left` / `--wide-right`, unitless shares summing to 1 that say how the breakout band sits around it. `.5` and `.5` centres the prose; `0` and `1` grows figures from its left edge. The rule does the arithmetic, because `--measure-wide` differs by element. |
| Shape | 22 | The seven radii, the four border widths, the two that are the figure label's rule mark, and the six that are the shadow *shape* - its colour stays on the mode layer. Three more are one widget's shape each: `--part-rule-style`, `--sec-badge-size` and `--sec-badge-radius`. |
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

## The panel shell

`hub.js` builds every panel from one shell, `makePanel(spec)`, and a panel supplies nothing but its own name, its store key, its title and what goes in its body.
The contract below belongs to the shell, so a second panel gets all of it by asking for one, and a correction to any of it is made once.
Nothing here is in any page's markup, and a page served with the script blocked has no panel and no dead control in its place.

**Ten classes, and the shape is fixed.** The last four arrive only when a panel asks for a foot.

| Class | What it is |
|---|---|
| `.panel-shell` | The dialog. Every panel wears it, plus one class of its own - the appearance panel's is `.settings` - which is where that panel states its width and the height above which its body scrolls. |
| `.panel-bar` | The title bar, which is also the whole pointer surface for a drag. |
| `.panel-grip` | The keyboard handle inside the bar. Arrow keys move the panel, Shift is the finer step, Home or Enter puts it back. |
| `.panel-title` | An `h2`, because a dialog's name is a heading. The tag decides the outline a screen reader navigates by and the class decides how it looks. |
| `.panel-close` | The close control. It lives in the bar and is deliberately not part of the handle. |
| `.panel-body` | The part that scrolls. The bar stays in view at every scroll position, because a handle that scrolls out of reach is a panel the reader cannot put back. |
| `.panel-foot` | Optional, asked for with `foot: true`. Pinned below the body and outside it, which is the title bar's shape at the other end. |
| `.panel-state` | The save state, in `--ok` on a good write and `--warn` on a failed one, written by the shell's `saveState` helper and never by a caller's own copy of it. |
| `.panel-export` | The escape hatch, filled in `--warn` the moment a write fails. |
| `.panel-do` | The one action a panel body leads with, when it has one. |

**A panel that holds something the reader made takes a foot, and the foot is the shell's.**
The two that do are the study notes panel and the highlights panel, and both of them make the same promise - that the save state is a fact rather than an intention - so both paint it with the same three classes and the same two helpers, `saveState` and `saveFailure`.
The state is a `role="status"` line whose text is written only when it changed, because the role speaks every write and nobody needs `Saved` announced at every pause.
A second copy of that would drift, which is the reason the shell exists at all.

The root is `.panel-shell` rather than `.panel` because `panel` is already taken by chart furniture, and a bare `.panel` rule would have matched every `<rect class="panel">` in the hub's inline drawings.

**A panel is non-modal, it has no backdrop, and an outside click does not close it. This is not configurable.**
It carries `role="dialog"` and `aria-labelledby` and it does not carry `aria-modal`, because a reader parks a panel in order to keep reading with it open and telling a screen reader the page behind it is inert would be a lie.
For the same reason focus is not trapped: Tab walks out of the panel into the page and back round.
A parked panel that vanishes the moment the reader clicks the text beside it is a panel that cannot be parked, and a panel that dims or blurs the page behind it hides the thing the reader opened it to work on.
The ways out are the opening button, the close control and Escape - three, all of them visible or conventional.

**Focus moves into a panel when it opens, and returns to the opening button only if it was inside.**
A reader who has tabbed back into the page and pressed Escape keeps their place instead of being thrown to the topbar.
Escape belongs to the panel the reader is in: with focus inside another panel this one stays open, and with focus anywhere else every open panel closes.

**The panel and the button that opens it can never disagree about whether it is open.**
`attachOpener` is what ties them together, and it is the shell that writes `aria-expanded` on every open and every close.
A button whose markup states `aria-expanded="false"` once and is never updated tells a screen reader the panel is closed while it is open; that is the defect the reference site ships and the reason this is the shell's job rather than a caller's.

**A panel moves, by pointer and by keyboard, and its position is an intention.**
What is rendered is that intention clamped into whatever viewport is in front of the reader now, so a coordinate chosen on a wide display comes back when the wide display does and on a phone the panel is re-seated rather than stranded.
The clamp runs on every open and every resize and it never writes back.
The band the panel is held inside is measured off the sticky topbar and the pre-production strip rather than assumed, so a panel can never be parked under either.
Only the re-seat glides - it carries `[data-settling]` - and every move the reader aims takes that attribute off first, because a step that animates is a step nobody can aim.
`[data-motion="reduced"]` zeroes the glide with every other transition, so reduced motion is answered by the stylesheet and never by a branch in the script.

**Each panel remembers its own position under its own key**, so two panels remember two places and neither can overwrite the other's.
The appearance panel's key is `coursehub.panel`.

**A panel is `hidden` while it is closed, and that is a requirement rather than a detail.**
The element is in the DOM of all 797 pages; without `hidden`, `scripts/focus_walk.py` would tab through every control in it on every page and so would every reader.

**Three tokens belong to the shell and are read by every panel**: `--panel-target`, the square the grip and the close control take, at the WCAG 2.2 SC 2.5.8 floor; `--sp-inset-panel-bar`; and `--sp-inset-panel-body`.
`--set-w` and `--set-h` are the appearance panel's own width and height and are not the shell's, and neither are `--notes-*` or `--marks-*`.

**Adding a panel is a call and a class, and nothing else.**
Ask `makePanel` for a shell, fill `shell.body`, optionally ask for a foot and fill `shell.foot`, hand it the button that opens it, and give it a class of its own for the two lengths it states.
It may not reintroduce a backdrop, make the close-on-outside-click behaviour configurable, trap focus, share another panel's store key, or write its own drag.
Every colour it uses is a token, and every control in it must show the hub's focus ring, because `focus_walk.py` presses real Tab keys through the open panel.

## The reader control panel

`hub.js` builds one panel from the shell above and it reaches every page, because every page already links the shared assets.
It is the shell plus six controls: everything a reader can do to the panel itself - open it, close it, pick it up, step it with the arrow keys, put it back, have it remembered - is stated in "The panel shell" and is not restated here.
What follows is what this panel *contains*, and why.

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

**The panel passes the floors it enforces.**
Its labels are `--ink` or `--ink-soft` and never faint ink on a recessed surface at a small size - the comment on the copy button in `hub.css` records that this codebase has already failed that once.
Every control clears 24 by 24 CSS pixels, which is why the range thumb is drawn rather than inherited: the browser's own is about 16px square.
`scripts/focus_walk.py` opens the panel and presses Tab through all of it in both modes.
The panel's own chrome - the grip, the title and the close control - is the shell's and clears the same floor through `--panel-target`.

**"Back to this course's defaults" is exact.**
It removes every `--*-user` property, every reader axis attribute and the panel's own position, which leaves the stylesheet's own values with nothing to unwind.
That is a property of the three-layer rule rather than a feature of the button: a reader value that competed with a token instead of feeding one would have to be unwound rather than removed.

## The floating control cluster

`hub.js` builds a five-control cluster in the bottom-right corner of every page, and no page's markup mentions it.
The fifth, the highlights launcher, is the only one that is conditional: it is absent on a browser with no CSS Custom Highlight API, because the panel it would open was never built there.
It is chrome you never author, exactly as the topbar and the rail are: it arrives on a page because that page links the shared assets.

**It exists because the panel above was invisible.**
Every reader control sat behind one unlabelled glyph at the right of the topbar, and the person who commissioned the framework could not find it.
A reader who never opens that glyph never learns that the palettes, the designs, the text size or the reading face exist, so the framework was shipped and not delivered.

**The light and dark control is what teaches, and that is why it is in the cluster rather than only in the panel.**
One click repaints the whole page, which is a demonstration rather than a label; a reader who has watched it happen reads the launcher beside it as an offer.
It names the mode it will switch to rather than the mode that is on, in its glyph and in its `aria-label`, and it follows the operating system's preference while the reader has stated none.
The reference site's own button shows the current theme and reads as an instruction, so `Light` there means "you are in Light" and every reader who takes it for a label presses it expecting the opposite.

**Each panel has two openers and no owner, and the shell is where that lives.**
`attachOpener` registers a button rather than replacing the last one, so both the topbar button and the cluster's launcher wear `aria-expanded`, and Escape or the close control returns focus to whichever one was actually used.
The study notes panel and the highlights panel each take their second way in the same way, which is one call apiece in `mountCluster`.
A reader who opened the panel from the corner and was thrown to the topbar has lost their place, which is the thing the panel's focus contract exists to prevent.
A third way in, or a second panel with two of its own, is one call and no new code.

**Scroll-to-top is absent until there is somewhere to go back to**, which is one viewport of scrolling rather than a literal distance.
It is the first control in the row, because the cluster hugs the right edge and a control that comes and goes on the left never moves the other two under the reader's thumb.
It is never taken away while it holds focus, because hiding the element a keyboard reader is standing on drops focus to the body.
Activating it scrolls with no `behavior` named, so the browser reads `scroll-behavior` off the stylesheet and the motion axis governs it, and then moves focus to the wordmark: a page that scrolls to the top and leaves the keyboard at the foot of it has moved only half the reader.

**Three positioning decisions, and each is read rather than assumed.**
The bottom edge is `--dock-offset` plus everything already fixed across the foot, read through `--foot-h`, so the live site, the review site and a page carrying the chapter bar are one declaration.
`z-index: 64` puts the cluster under the rail's drawer scrim below 1040px and under every panel shell, so a click on it while the drawer is open dismisses the drawer, which is what the reader meant.
It is a `role="group"` and not a `role="toolbar"`, because a toolbar owes the reader arrow-key roving focus and three plain buttons owe nothing beyond Tab.

**It is chrome, so it is out of the density control's reach and it is not on the paper.**
The print block hides it with the topbar, the rail, the panel and the pager.

Three tokens are its own: `--dock-target`, the square each control takes, at 36px because it is aimed at with a thumb while the reader is reading rather than with a pointer while they are looking at it; `--dock-offset`, the distance from the two viewport edges it hugs; and `--sp-inset-dock`, the padding around the row.
All three are design-axis tokens, so a design may raise the target and may never lower it below the 24px WCAG 2.2 SC 2.5.8 asks for.
## The fixed chapter bar

`hub.js` builds a band across the foot of the viewport carrying the previous page, where you are and the next page, and no page's markup mentions it.
It is chrome you never author, exactly as the topbar, the rail and the floating cluster are: it arrives on a page because that page links the shared assets.

**It exists because the end-of-page pager is at the end of the page.**
A reader who has decided to move on is almost never at the foot of the document when they decide it, so the pager costs a scroll to the bottom before it can be used at all.
The pager stays and is not restyled: it is the page's own last word, it is what a reader with scripting switched off has, and it is the half of this that prints.
The bar is the same two destinations held in view the whole way down.

**The order comes from the generated outline, never from the pager's own markup.**
`outline.js` is written by `scripts/gen_outline.py` from the course map, check 3 in `validate_site.py` fails the pull request when it and `lessons/` disagree, and check 7 holds every title in it against the map and against every pager pointing at the page.
A page's committed pager is hand-written per page, which makes it a claim about two neighbours rather than a sequence: a bar built from it could not say how far through the course the reader is, could not tell a missing neighbour from a first page, and would go quietly wrong on exactly the page whose pager was the one nobody updated.
A routed course is the same source by another route.
Its `outline.js` derives `window.COURSE_OUTLINE` from `routes.js` for the route in play, so the bar follows the route the reader is actually on, carries `?route=` on both links because the outline already does, and no code in `hub.js` knows routes exist.

**The sequence is the outline's own reading order**: every lesson of every section in order, then the reference pages the rail shows under `Reference`.
A page the outline does not name gets no bar at all - a course map, the hub landing page and the design system reference have no place in that sequence, and a bar that could not say where you are would be answering two thirds of the question.
On a routed course that also covers a page the active route does not contain, which is the same answer the rail gives it.

**The first and the last page omit the dead control rather than disabling it.**
A disabled control is a promise the page cannot keep: it holds a tab stop, it reads as something that would work if the reader tried harder, and there is nowhere for it to go.
The three parts are placed by grid column rather than by source order, so the survivor stays on its own side of the bar and the centre stays centred.

**The centre names the position and the page, and it is text rather than a link.**
The topbar already carries the way back to the course map, and a third destination in a bar whose whole job is two destinations is a third thing to read past.
It reads `3 of 68` rather than `3 / 68` because a screen reader says the second one as "3 slash 68", and it is a position rather than a progress reading: the rail owns how much of a course has been read, and a second answer to that question in the same viewport would be two answers.

**Everything fixed across the foot of the viewport is summed once, in `--foot-h`.**
Three things can occupy it and any two can be there at once: the pre-production strip, this bar, and the device's own bottom inset.
Every rule that has to give that space back - the body's padding, the rail's scroll foot, the floating cluster's offset, both panels' heights - reads that one token rather than restating the sum, so a fourth occupant is one term and no edit anywhere else.
`--preprod-h` and `--chapbar-h` are each declared only where the thing they measure exists, so the fallback in each `var()` is the answer for every page that does not carry it.
`--foot-h` is declared on `body` rather than on `:root` because `--chapbar-h` is: `hub.js` may write no attribute on `<html>` but a registered reader axis, so the flag that says a bar was built is `body[data-chapbar]`, and a custom property resolves against the element that declares it.

**The bar's height is the token, not the other way round.**
`height` is `--chapbar-h` and the reserve reads the same token, so the two cannot disagree.
That is why both lines inside it are pinned to one line each and clipped with an ellipsis rather than wrapped: a wrapped title would make the bar taller than the space given back for it and hide the last line of the page behind it.

**`z-index: 63` is one below the floating cluster**, so the two can never contend for a pixel, and it inherits the cluster's reasoning for everything above it: under the rail's drawer scrim at 65 and under every panel shell at 90.
The panels go further than the stacking order.
`bounds()` in the panel shell measures this bar along with the pre-production strip, so a parked panel cannot be dropped over it, and measuring is what makes the strip's two-line phone height and the bar's one-line phone height both correct there without either being restated.

**It is full-bleed rather than inset to the reading column.**
The topbar is, the pre-production strip is, and a band that started at the rail's right edge would have to track `--rail-w` through the drawer arm below 1040px, where that token still holds a width the layout is no longer using.

**Below 720px it is one line, and the title is what survives.**
A phone reader still needs the name of the page they are moving to, which is the whole reason the bar carries titles rather than two arrows, so the direction word goes and the arrow and the title stay; the centre gives up its title the same way and keeps the position.
The link's accessible name states the direction in full at both widths - `Previous: <title>` - because a hidden element is out of the accessibility tree as well as off the screen, and WCAG 2.2 SC 2.5.3 is satisfied at both because the visible label is contained in that name.
The arrow carries `flex: none`: `* { min-width: 0 }` at the head of the sheet takes the flex automatic minimum off every element, and measured at 320px the arrow was laid out 5.2px wide against a 15px glyph and rendered as a stub.
The title is the item that may give up width, because an ellipsis still reads.

**It is a `nav` with a name of its own**, `Previous and next lesson`, because the page already has two: the rail is `Course outline` and a routed course's committed pager is `Lesson navigation`.
Three landmarks with one name between them is three landmarks a screen-reader user cannot choose from.

**It is chrome, so it is out of the density control's reach and it is not on the paper.**
The print block hides it with the topbar, the rail, the panel, the pager and the cluster, and zeroes the reserve with it.

Three tokens are its own: `--chapbar-h`, its height, declared only under `body[data-chapbar="on"]` and again in the narrow arm where the bar is one line; `--sp-inset-chapbar`; and `--sp-inset-chapbar-sm`.
The two insets are design-axis tokens; the height is not, for the same reason `--topbar-h` and `--preprod-h` are not.

## The study notes panel

`hub.js` builds a second panel from the shell above and it reaches every page, from a topbar button beside `Appearance` and from a launcher in the floating cluster.
It is chrome and only chrome: no page names it, no page markup changes, and a page served with the script blocked has no button, no panel and no trace.
Everything a reader can do to the panel itself - open it, close it, pick it up, step it with the arrow keys, put it back, have it remembered - is stated in "The panel shell" and is not restated here.
What follows is what this panel *contains*, and what it promises.

**The save state is a fact, never an intention. That is the whole point of the panel.**
Three states, and each one says what actually happened:

| State | What it means |
|---|---|
| `Saving` | what the reader typed is not in storage yet |
| `Saved HH:MM` | the store was written and read back equal |
| `Not saved: ...` | the write failed; the words are still on screen and Export is the way out |

The panel writes through `setChecked` and `dropChecked`, which return whether the store now holds what was asked for, and never through `set` and `drop`, which swallow.
Swallowing is right for a preference - a lost palette costs one click, and saying so would be noise - and it is the defect itself for a document.
The reference site this was replicated from paints a green `Saved` on every keystroke because `setItem` was *called*, so a reader whose quota is full is told their work is safe on every keystroke and loses all of it on the next reload.
The read-back is not belt and braces: a `setItem` that raises is the loud failure, and a store that accepts the call and keeps nothing is the quiet one, so the only honest answer is to ask the store what it now holds.

**Four ways to lose text, all closed, and each one is a rule rather than a fix.**

- *Nothing is written until you stop typing.* The debounce carries a **ceiling** as well as a pause: a keystroke waits 400ms for the next one, and no keystroke waits longer than 2s whatever the reader does. A trailing debounce alone means a reader who types without pausing has nothing in storage however long they type.
- *Nothing flushes on the way out.* `visibilitychange`, `pagehide` and the editor's own `blur` all commit, so a keystroke followed inside the debounce by a link click, a tab close or a background switch is written rather than lost.
- *Closing the panel throws the last keystroke away.* The shell's `onClose` commits before the panel goes; that hook exists because this panel asked for it.
- *A read runs over the live editor.* It cannot here. What the reader can still see is authoritative and storage is never read over the top of it, which is also what leaves the words on screen for Export to take away after a failed write.

**A note is keyed on the two things this repository has committed never to change.**
The key is `coursehub.note:` plus a tier and an identifier, one key per document, and the identifier is the course key and the file name: `AGENTS.md` forbids renumbering or renaming a lesson because its URL is public, and a course folder is in every cross-course link in the hub.
A lesson's *title* is none of those things and is rewritten often, which is the mistake the reference makes - it keys on a slug built from a hand-maintained title array, so editing a chapter's title orphans every note under it, silently, with the old key left in storage unreachable.
The course key is `COURSE_OUTLINE.key` where a course ships an outline and the `data-course` folder without its suffix otherwise, which are two derivations of one identifier rather than two identifiers, and it is the same key the reading progress map already uses.

**Three scopes, and the control is real.**
`This page`, `This course` and `All courses`, each its own document.
A page with no course - the hub landing page, the design system - offers the two tiers it actually has, and the panel names the key it is editing underneath, so the answer to "where did that go" is on screen.
The reference shows a badge in this position reading `All Masterclass Lessons`; it is a `div` with no handler, no role and no keyboard behaviour, and it says the same thing on every page.
A control that appears to offer a choice and offers none is worse than no control.

**The editor is a plain `textarea` and the formatting is nine splices.**
No library, no `contenteditable`, no model: each toolbar button puts literal markdown characters around the selection or in front of the lines it covers, and then dispatches a real `input` event, so a toolbar press reaches the save machinery by the same path a keystroke does.
`Ctrl/Cmd+B`, `Ctrl/Cmd+I`, `Ctrl/Cmd+S` and `Ctrl/Cmd+Shift+C` do the same four things from the keyboard.
The heading button *cycles* `#`, `##`, `###` and back to plain, so no level is out of reach and none is a trap.

**Tab is bound to nothing in the editor, and that is deliberate.**
The reference indents with it, which makes the editor a keyboard trap and fails WCAG 2.1.2.
`scripts/focus_walk.py` presses real Tab keys through this panel in both modes, on three pages, and every one of its stops has to wear the hub's ring.

**The preview renders the hub's own widgets and never a second vocabulary.**
Headings, paragraphs, rules, nested bullet and numbered lists, tasks, fenced code, inline code, `**bold**`, `*italic*`, `==highlight==`, `~~strike~~`, links, blockquotes, and `> [!note]` / `[!warning]` / `[!tip]` mapped onto `.callout`, `.callout.warn` and `.callout.key`.
So a note looks like the page it was written beside, in all seven palettes and both modes, and costs the contrast matrix no row of its own.
A note's `#` renders as an `h3`, because the panel's own title is the `h2` a dialog's name has to be and the outline a screen reader walks has to stay in order; how big each level looks is the stylesheet's, which is the tag-and-size split stated everywhere else in this file.

Three departures from the reference renderer, and each closes a measured defect:

- **`_underscores_` are not italics.** Theirs turns `user_id_field` into `user<em>id</em>field`, on a hub whose courses are about `top_p`, `--max_tokens` and `attention_mask`. Only `*asterisks*` italicise.
- **Every placeholder restore is a function replacement**, so a code span containing `$&` or `$1` survives being put back.
- **A link's scheme is on an allowlist.** The document is the reader's own, so this is not a trust boundary, but a note pasted from somewhere else is not, and `javascript:` in it renders as text.

**Export is the escape hatch, and it exports what is on screen.**
Front matter - title, scope, the storage key, the source URL and the date - then the document as the editor holds it, never as storage holds it, because a failed write is exactly the case where storage cannot be trusted.
The button is filled in `--warn` when the last write failed, so a reader who has just been told their words are not saved does not have to read a fourth sentence to find out what to do about it.
The front-matter guard is a real one: a block is a fence, a body and a closing fence, so a note that opens with a horizontal rule still gets its own front matter.

**The foot is pinned to the panel and the body scrolls above it.**
It is the one place this panel departs from the appearance panel's shape, and the save state is what earns it: a state that can be below the fold is a state a reader can miss.
The foot itself, the state line and the export button are the shell's `.panel-foot`, `.panel-state` and `.panel-export`: this panel asked for them first and the highlights panel needs the identical three, so they belong to the shell rather than to either.

**What this panel deliberately does not have.**
No images and no attachment store - theirs is what fills the quota that then causes the silent data loss.
No `Clear` - theirs wipes every chapter's highlights from the landing page while deleting only one document, and a reader who wants an empty note selects all and deletes, which saves as an empty note and drops the key.
No page-text highlighter: that is its own feature, its own panel and its own anchoring contract, stated below.

**Seven tokens belong to this panel and are read by nothing else**: `--notes-w`, `--notes-h` and `--notes-edit-h` for the two lengths it states and the editor's floor, and `--sp-notes-rows`, `--sp-notes-block`, `--sp-notes-indent` and `--sp-inset-notes-edit` for its rhythm.
The highlights panel states its own four and reads none of these.
The preview's block rhythm is a chrome distance rather than one of the twenty reading roles on purpose: a `.callout` inside a panel that took a reading role would put the density control into the chrome, which is the split the space ramp exists to prevent.

## The text highlighter

A reader selects a sentence, marks it, and finds it marked when they come back.
`hub.js` builds all of it and no page's markup mentions it: it is chrome you never author, exactly as the topbar, the rail, the cluster and the two panels are, and it reaches all 797 pages because those pages link the shared assets.
A page served with the script blocked has no control, no panel and no trace.

**It is painted with the browser's own highlight mechanism and never with a `<mark>` element.**
`CSS.highlights` takes a set of `Range` objects and `::highlight()` styles them, so nothing in the page is wrapped, split or rewritten and the DOM a screen reader walks is byte for byte the one the author wrote.
The alternative is to split the text nodes a selection crosses and wrap each piece, which is how this feature is usually built and is why it usually breaks: a sentence a screen reader read as one string becomes three, and it is read out in fragments with a pause at each seam.
It is also a live edit of a document the section rail, Mermaid and the print pass all hold references into, and it cannot be undone cleanly - removing a mark means merging text nodes back.
A range highlight has none of those properties, and the worst failure available to it is a mark that does not appear.

**What that costs is semantics, and the panel is the answer to it.**
There is no element, so there is nothing in the accessibility tree to announce and a screen reader is not told the words are marked.
That trade is made on purpose: the panel lists every mark on the page as text, in reading order, which is what a screen reader reads instead of a shredded sentence.

**Where the API is missing there is no button, no panel and no cue.**
The feature is simply not on that browser, and it does not fall back to splitting the DOM, because the fallback is the defect.

### The anchoring contract

A highlight is a reference into text that can change under it, so where it lands on return is the whole design.

**The domain** is the page's own prose flattened to one string: every text node under `main.wrap` or `main.wide`, in document order, with each run of whitespace collapsed to a single space.
Five things are left out and each has a reason - `script` and `style` are not prose, `svg` and `.mermaid` are drawings whose text is replaced when they render, form controls and buttons are chrome inside the column, `.sr-only` is text no sighted reader can select, and anything `hidden` or `aria-hidden` is not on the page.
Collapsing whitespace is what makes the domain the text the reader sees rather than the file's indentation, so re-wrapping a lesson's source moves nothing.

**What is stored** is four fields and no ids into the DOM: the exact quote, the offset it was taken from, and up to 48 characters of the text either side.
That is a position selector plus a quote selector with context, which is the shape the W3C Web Annotation model settled on for the same reason.

**How it is placed on return**, in order, and every step is an exact match:

| Step | What is asked | What answers it |
|---|---|---|
| 1 | Is the quote at the offset it was saved at? | The whole of the cost on a page nobody has edited. |
| 2 | Does `before + quote + after` occur **exactly once**? | A new paragraph above moves every offset below it and moves no words. |
| 3 | Does the quote occur **exactly once**? | An edit to the sentences either side of the marked one. |
| 4 | Nothing else. | The highlight is not painted, and the panel says so. |

**Two or more occurrences at any step is a failure rather than a guess.**
There is no fuzzy match, no nearest match and no edit distance anywhere in the file.
A highlight that no longer fits **fails visibly** rather than landing on the wrong words, because a silently misplaced highlight - marking the wrong sentence with complete confidence - is worse than one that openly did not come back.
The panel names the ones that did not place, quotes the words they were made of so the reader can find them by eye, and offers to remove them; nothing is thrown away, so restoring the paragraph restores the mark.

**Placing never writes.**
Re-anchoring through step 2 or step 3 does not rewrite the stored offset: a load that quietly rewrote storage could report a write failure the reader did not cause.

**A selection that crosses element boundaries is one highlight.**
The domain is one string over the whole content region, so a selection spanning a paragraph break, a list, a code block or a figure caption has one anchor and the browser paints it across every element it crosses.
Nothing in the DOM is touched, so there is no partial mark and no broken markup available here at all.
A selection is clipped to the content region - the part inside is marked and the part outside is dropped - and a selection with no prose in it, one made entirely inside a diagram or in the chrome, is refused and said to be refused.

**A stroke over words already marked merges with them**, so the reader ends with one highlight over the union rather than two stacked ones, which is what a marker pen does and what makes Remove mean one thing.

### Where a page's highlights live

Beside the notes, and on the same identifier: `coursehub.mark:` plus the tier and the course-key-and-file-name `pageKey` derives, so a note and a highlight on one page can never disagree about what a page is.
One key per page holding one array, because a page's marks are one document.
The storage discipline is the notes panel's and is not negotiable: writes go through `setChecked` and `dropChecked`, the state is painted from what they returned, and a mark whose write failed is still on screen with the export button filled and the sentence saying it will not survive the reload.
The panel tells the two failures apart by what the write itself raised rather than by a second probe - a store full to the last byte refuses a probe as well, and the reader would then be told the browser is storing nothing when it is storing five megabytes of theirs.

### The two ways in

**A pointer reader gets the cue**, a floating `Highlight` offer over the selection, which borrows the cluster's `--dock-target` and `--sp-inset-dock` because it is the same kind of control - a floating one aimed at with a thumb while the reader is reading.
It prevents the default on `mousedown` so pressing it does not collapse the selection it is about to mark, and it is positioned into the band between the sticky topbar and everything fixed across the foot, so it never opens where it cannot be pressed.

**A keyboard reader gets the panel.**
The last selection made inside the content region is held as an anchor, so opening the panel and pressing its first button marks it whatever the selection did when focus moved, and the panel names the words it is about to mark underneath.
There is no global shortcut key: a single-character one is an SC 2.1.4 problem and every free modifier combination is taken by a browser on some platform.
The held selection is re-placed through the same contract a stored one is, so a reader who selected a sentence and then answered a quiz below it still marks the right words.

### On paper

**The control comes off and the mark stays, as an underline.**
The cue is hidden with the rest of the interactive chrome, `--mark-soft` is white in the print block, and `::highlight()` carries a grey rule instead - so a marked page prints the reader's own annotation without printing a grey block behind every marked paragraph.
Verified in Chrome at A4: the fill is gone and the underline is there.

### What it costs the design system

**One colour, and it comes from the palette.**
`--mark-soft` is `color-mix(in srgb, var(--gold) 26%, var(--surface))`, so it is the palette's own gold in every one of the seven and never a hard-coded yellow.
26% is the strongest tint that still clears the 7:1 body floor on every palette in both modes, which is arithmetic rather than taste: `scripts/contrast_matrix.py` measures `--ink` and `--ink-soft` on it over all 266 combinations, and the worst is 8.08:1 against a 7:1 floor.
The highlight the panel is pointing at, after `Show`, adds an `--accent-2` underline, which is the only shape `::highlight()` can carry - it takes colour, background, text-decoration, text-shadow and the stroke, and nothing else - and that pair is measured too, at 4.14:1 against a 3:1 floor.

**Four tokens belong to this feature and are read by nothing else**: `--marks-w` and `--marks-h`, the two lengths its panel states, and `--sp-marks-rows` and `--sp-inset-mark` for its rhythm.

**What CI proves.**
`scripts/focus_walk.py` makes three highlights through the cue, on three pages, in both modes, before it walks the panel - so every run proves the highlighter works end to end in a browser and not only that its panel opens.

## The in-page section rail

`hub.js` builds a strip of ticks down the right-hand margin of every page, one per section of that page, and no page's markup mentions it.
It is chrome you never author, exactly as the topbar, the course rail and the floating cluster are: it arrives on a page because that page links the shared assets.

**It is derived from the page's own headings, at runtime, and from nothing else.**
That is the whole design and it is the reason there is no authoring step here at all.
A model of a page's sections held anywhere but in the page is a second source that can disagree with it, and a lesson rewritten in the afternoon would leave that model wrong by the evening.
The headings cannot drift from the page, because they are the page.

**Which headings is one rule, and it was read off the corpus rather than guessed.**
An `h2` that is a direct child of the content region and is not wearing a smaller face.
Inside `main`, the hub's 744 lesson pages carry 6,260 `h2`, 1,236 `h3` and 10 `h4`, and 5,559 of those `h2` are direct children, so `h2` is this hub's section level, `h3` is an occasional subdivision inside a section rather than a section of its own, and `h4` barely exists.
It is the same rule [`.numbered`](#the-numbered-section-badge-numbered) already applies when it draws the section badges, so the squares down the page and the ticks down the margin can never name different sections.
Direct children is also what keeps everything else out without naming any of it: the topbar, the course rail, both panels and the cluster are children of `body`, and a figure's caption, a callout's heading and a card's title are deeper than one level, so none of them can appear in the list and a widget added next year cannot leak into it either.

**Four sections, or no rail.**
A rail answers two questions - where am I, and how much is left - and on a page of three sections the scrollbar has already answered both, so a list of three is chrome that outweighs what it indexes.
Fifty-seven of the hub's 789 content pages carry three sections or fewer and get nothing at all, which is the intended outcome and not a gap.
A course map gets none either, and for the same reason rather than by an exception: its headings sit inside `.module` blocks and are not direct children of anything.

**A heading keeps its own id and is given one only if it has none.**
The generated id is `sec-` plus the heading's text, lowercased, with accents folded onto their letters, apostrophes dropped so a possessive stays one word, and every other run of non-alphanumeric characters folded to a single dash.
It is deterministic, so a link a reader shared last month still lands in the right place today.
The collision rule: a candidate is taken only if nothing in the document already answers to it, which covers an id an author wrote elsewhere on the page and a second heading whose words match an earlier one's in the same test.
Otherwise the next free `-2`, `-3` and so on is taken, counting in document order, so the first heading with those words keeps the plain id and a later one can never take it away.
A heading whose text yields no slug at all takes its own position in the sequence instead.

**The reader is in the last section whose heading has reached the reading line, and in exactly one.**
The reading line is `--secrail-line`, which is also every direct-child `h2`'s `scroll-margin-top`, so a jump lands a heading on the line and the section jumped to is current the moment the reader arrives.
`hub.js` reads that value back in pixels off the heading itself rather than restating it, so the distance that positions a jump and the distance that decides which section is current are one number with one home.
When two sections are on screen at once - the tail of one and the heading of the next - the reader is in the earlier of the two, because they have not reached the later heading yet.
Above the first heading no section is current, and nothing is highlighted: a page's opening is not a section, and saying it is would be a small lie told on every page load.

**It is tracked with an `IntersectionObserver`, and the observer's shape is what makes that honest.**
The root is the viewport from one pixel above the reading line down; the thresholds are 0 and 1.
A heading's top crossing that edge is a crossing of threshold 1 - it stops being wholly inside the root - and its bottom crossing is a crossing of threshold 0, so every transition of "has this heading reached the line" raises a callback.
Neither threshold alone would do: with 0 the highlight lagged by the height of the heading, and a one-pixel band was stepped over between two frames by any fast scroll and never fired at all.
The callback reads the headings' own rectangles rather than the entries it was handed, so what is painted is the geometry at the moment of painting and never a fact remembered from an earlier frame.

**Ticks always, labels on hover and on focus.**
Collapsed, the strip is about 35px wide and stands in the content gutter beside the breakout band rather than over it; the reader's own section is drawn on a longer tick in the course accent, so "where am I" is answered with no label showing and without asking anyone to tell two colours apart.
Hovering the strip, or tabbing into it, opens the labels leftwards over the page for as long as the reader is there.
That is the trade the widget exists to make: a permanently labelled list would sit on every figure and every table on the page, and a list of ticks nobody can read is not a list.
Opening changes colours and the labels' own width, never anything under the pointer - the ticks are the elements nearest the edge and they do not move.

**Every row is a plain anchor and deliberately nothing else.**
The browser scrolls it, reads `scroll-behavior` off the stylesheet so the motion axis governs whether the jump animates, puts the address bar on the section the reader is now reading, and moves the sequential focus starting point to the heading so the next Tab carries on from the page rather than from the rail.
Four user stories, and not one line of script.
The strip is a `nav` with an accessible name, the rows are an ordered list, and the current row carries `aria-current="location"` - `location` rather than `page`, because the course rail's `page` says which page of the course this is and this says which place within the page the reader is at.
A label is clipped rather than hidden, so it stays in the link's accessible name whether the labels are open or shut.

**Its band stops where the foot begins.**
The strip spans the viewport from the foot of the topbar to the top of the floating cluster, and what is fixed across the foot below the cluster is [`--foot-h`](#the-fixed-chapter-bar), which this reads as one token exactly as the cluster does.
So the pre-production strip, the chapter bar and the device inset are already summed and a fourth occupant reaches this rail with no edit to it.
It carries `z-index: 63`, the chapter bar's layer, and the two never contend for a pixel because the strip ends above where the bar begins.

**It runs at 1281px and up, and it is absent below that.**
The strip stands in the content gutter, which is `--pad`: 3rem above 1280px, where there is room for it beside the widest figure on the page, and 2rem or less below, where the same strip would stand on the edge of every breakout element instead.
That threshold is above the course rail's own by construction, so the two never compete.
Below 1041px the course rail leaves the grid and becomes a drawer over the content, the reading column takes the whole viewport, and there is no gutter at all; a second navigation floating over the same prose would be a second thing between the reader and the page, and a phone reader's whole width is the reading width.
So the section rail is simply not there, and the page keeps the navigation it has always had.
It is not printed either, with the rest of the chrome.

**Seven tokens belong to it and are read by nothing else**: `--secrail-w`, the width the labels open to; `--secrail-tick` and `--secrail-tick-on`, one section's tick and the reader's own; `--secrail-target`, the height of a row; `--secrail-offset`, from the right edge of the viewport; `--secrail-line`, the reading line; and `--sp-inset-secrail`, around the ticks.
A row is `--secrail-target` tall and no wider than its own tick, so it meets WCAG 2.2 SC 2.5.8 on the spacing exception rather than outright: the nearest other target is the row above or below and nothing else on the page comes within the strip's own width.
Widening a row to clear the criterion outright would put the strip on the breakout band at the width the rail starts at, which is the one thing it may not do, and closing the gap between rows would take the exception away, so nothing here may be tightened.

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
