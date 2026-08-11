# Builder Spec - read this before writing Lecture 2

This is the authoring contract for *Statistical Foundations of Machine Learning*.
Read `MISSION.md` and `NOTES.md` first.
Then read `lessons/0002-robust-summaries-mean-vs-median.html` in full: it is the gold template for a content page.
Read `lessons/0000-lecture-1-start-here.html` for the shape of a lecture hub page.

The repository-wide rules in `../AGENTS.md` and `../CONTRIBUTING.md` still apply and win where they conflict with anything here.

## The structure this course uses

Three levels of nesting, because a lecture is too much for one sitting and a slide is too little for one page:

```
hub index.html  ->  course index.html  ->  lecture hub page  ->  content page
```

A lecture becomes one hub page plus N content pages, numbered as a single continuous sequence in `lessons/`.
Lecture 1 occupies `0000` through `0008`.
**Lecture 2 starts at `0009`.** Do not renumber anything: the URLs are public.

The lecture hub page states what the lecture delivers, carries the logistics, and links its content pages in order.
The course `index.html` groups the lecture as one `<section class="module">` with the hub card first and the parts listed beneath it.

## Hard rules

1. **No em dashes anywhere.** Plain `-` only.
2. **Every number matches the source deck exactly.** Quote the deck's figure with `<span class="keynum">`. Do not round it differently, do not re-derive it into a nicer value, do not extrapolate past what the slide claims.
3. **Work every intermediate step the slides compress.** The reader must never have to reconstruct a missing step. If the slide writes one line of algebra, this course writes the three lines behind it, inside a `<ol class="worked">`.
4. **Name every symbol in words on every page where it appears,** not once per lecture.
5. **At least three diagrams per content page,** using several distinct kinds across the lecture.
6. **At least two quizzes per content page,** using the exact markup in `assets/course.js`.
7. **Never hard-code a colour in an SVG.** Use the semantic `.chart` classes so the figure survives both themes.
8. **Cite a primary source.** The canon is in `RESOURCES.md`. Anything new goes there first.
9. **Where the lecture is loose, say so** in a `.callout.warn`, rather than smoothing it over.
10. Self-contained HTML with the same `<head>`, spine nav, and `../assets/course.js` at the end of `<body>`.

## Required section skeleton for a content page

1. `.eyebrow` = `Lecture N &middot; Part K of M &middot; <Slide range>`
2. `<h1>` = the page's one idea, phrased as a claim rather than a topic.
3. `.paper-meta` = a `<span class="pill">` reading time, plus a one-line framing.
4. `.card.tldr` = "The one-minute version", three or four bullets.
5. The mental model, with the first diagram, before any formula.
6. The mechanism, with every symbol named.
7. The numbers, worked in full in an `<ol class="worked">`.
8. Two or more diagrams, each in `<figure class="diagram">` with a `<figcaption>` that bolds the takeaway.
9. Two or more quizzes.
10. An honesty note in a `.callout.warn` if the lecture was loose here.
11. `.teacher-note`, then `Where this came from` with the linked source, then `.pager`, then `<footer>`.

The `.pager` on a content page goes back to the previous part and forward to the next.
The first part goes back to the lecture hub; the last part goes forward to the next lecture hub, or to the course map if there is no next lecture yet.

## Diagrams

Two tools, and the split between them is not negotiable.

### Mermaid, for structure

Loaded from the CDN in every page's `<head>`. Wrap it exactly like this:

```html
<figure class="diagram"><div class="mermaid">
flowchart LR
  A["Observed data"] --> B["Estimate"]
</div><figcaption>Plain English, with <b>the one takeaway in bold</b>.</figcaption></figure>
```

Kinds already in use, so reuse rather than reinvent: `flowchart`, `sequenceDiagram`, `mindmap`, `timeline`, `quadrantChart`.

**Always wrap node labels in double quotes.** A statistics course is full of parentheses, commas, and maths, and every one of them breaks the Mermaid parser unquoted. `A["P(X > 2000)"]` is safe; `A[P(X > 2000)]` is not.

### Inline SVG, for anything quantitative

Mermaid cannot draw a distribution, a density, a confidence band, or a scatter plot.
Write the SVG by hand, in the page. No chart library, no build step, no extra CDN.

```html
<figure class="diagram">
  <svg class="chart" viewBox="0 0 640 300" role="img" aria-label="...">
    <line class="axis" x1="60" y1="250" x2="610" y2="250"/>
    <rect class="m-stat" x="70" y="180" width="30" height="70"/>
    <rect class="m-alarm" x="110" y="40" width="30" height="210"/>
  </svg>
  <div class="chart-legend"><span><i class="sw-stat"></i>typical day</span></div>
  <figcaption>...<b>takeaway</b>.</figcaption>
</figure>
```

Rules for an SVG figure:

- Always set a `viewBox`, never a fixed `width`/`height` attribute pair.
- Always set `role="img"` and an `aria-label` that says what the chart shows.
- Colour comes from the semantic classes only: `m-*` filled mark, `s-*` stroked line, `f-*` translucent fill, `t-*` coloured text, `sw-*` legend swatch.
- Keep the viewBox around `640 x 300`. Text at 13px in that box stays readable, and `.chart` has a `min-width` under 640px so a phone scrolls the figure rather than shrinking the labels.
- Check both themes. A colour that reads well on cream can vanish on near-black.

### The palette

Fixed for the whole course. The same idea keeps the same colour on every page.

| Variable | Colour | Means |
|---|---|---|
| `--stat` | teal | statistics, the backward engine, the robust summary |
| `--prob` | indigo | probability, the forward engine, the model |
| `--signal` | green | the real effect we are trying to find |
| `--noise` | grey | randomness, and the grey control group |
| `--alarm` | rust | the outlier, the risk tail, the thing that bites |
| `--gold` | gold | the gold button in the A/B test |

## Quizzes

Use the widget documented in the header of `assets/course.js`. `data-answer` is a zero-based index.

**Every option must match in word count and sit as close as possible in character count.**
A visibly longer correct answer leaks the answer and destroys the retrieval practice, which is the entire point of the widget.
Count the words before you commit.

`.q-fb` must explain **why each wrong option is wrong**, not merely restate the right one.

## Adding Lecture 2

1. Write the lecture hub page as `lessons/0009-lecture-2-start-here.html`, following `0000`.
2. Write the content pages as `0010` onward, one tight idea each.
3. Add a `<section class="module">` for Lecture 2 in `index.html`, with the hub card and a `<ul class="parts">` beneath it linking every content page. **The validator fails the pull request if any file in `lessons/` is not linked from `index.html`.**
4. Move Lecture 2 from the `.roadmap` list into the module, and mark its roadmap entry `class="written"` if you keep it listed.
5. Add a formula sheet at `reference/lecture-2-formula-sheet.html` and link it from the course map. Keep one sheet per lecture rather than growing a single sheet nobody prints.
6. Add every new term to `reference/glossary.html`. The validator will not catch a missing glossary row, so this is on you.
7. Run `python3 ../scripts/validate_site.py` from the repository root and open the pages in a browser, in both themes, at 360px and at full width.

## What the validator does and does not check

It checks three things: every course is linked from the hub, every `lessons/*.html` is linked from its course `index.html`, and every relative link resolves to a file on disk.

It does not check arithmetic, quiz answers, Mermaid syntax, colour contrast, or whether a figure renders at all.
Those are yours. Open the page.

**A roadmap entry for an unwritten lecture must be plain text, never a link.** A link to a file that does not exist fails the validator.
