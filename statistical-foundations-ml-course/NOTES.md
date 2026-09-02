# Notes

Working notes on how this course teaches.
Read `MISSION.md` first for why it exists, then `BUILDER-SPEC.md` for the exact markup.

## Learner profile

- Software architect and tech lead. Strong engineer, comfortable with abstraction, comfortable with code.
- Did probability and statistics at university. It has gone cold. The notation is now friction.
- Explicit request: **as close to zero cognitive load as possible**, and **a lot of diagrams, of several different kinds**.
- Not a beginner in thinking. A beginner again in this notation. Those are different things, and the difference sets the whole tone.

## What "zero cognitive load" means here

It does not mean shallow, and it does not mean short.
It means the reader is never asked to hold more than one new thing at a time, and never asked to fill a gap the author skipped.

In practice:

- **Picture, then mechanism, then numbers.** Never numbers first. A formula the reader cannot picture is a formula the reader will re-read four times and still not own.
- **Name the symbol in words the first time it appears on a page.** Not once in the whole lecture. On every page where it appears. Repetition across pages is cheap; a reader stalling on an unexplained lambda is not.
- **Work every intermediate step.** If the deck writes `0.693 / 415 = 0.00167`, this course also says what 0.693 is, why it is there, and what the units of the answer are.
- **One idea per page.** If a page needs two headings that both feel like the point, it is two pages.
- **Every page ends by pointing at the next.** The reader should always know why they are about to turn the page.
- **A number the deck states gets quoted, not recomputed.** Use the `.keynum` span so a stated figure is visually distinct from a figure this course derived.

## Cadence

- A content page is one sitting: roughly 8 to 12 minutes of reading, three or four diagrams, two quizzes.
- A lecture hub page is a map, not a lesson. It states what the lecture delivers, carries the logistics, and links the parts.
- Quizzes come after the idea has been fully worked, never as a gate before it.

## Diagram policy

This is the part the learner asked for loudest, so it gets the most care.

- **At least three diagrams on every content page**, and use several distinct kinds across the lecture.
- **Mermaid draws structure.** `flowchart` for block and decision diagrams, `sequenceDiagram` for pipelines with actors, `mindmap` and `timeline` for maps and roadmaps, `quadrantChart` for two-axis placement.
- **Hand-authored inline SVG draws everything quantitative.** Mermaid cannot draw a distribution, a density, a confidence band, or a scatter plot. Write the SVG directly in the page. No chart library, no build step, no extra CDN.
- **Every figure gets a `<figcaption>` that explains it in plain English and bolds the one takeaway.** A caption that only labels the figure is a wasted caption. If you cannot state a takeaway, the figure is decoration and should be cut.
- **Colour is meaning, not decoration.** The palette in `../assets/hub.css` is fixed, and it is deliberately independent of the reader's chosen palette: teal is statistics, indigo is probability, green is signal, grey is noise, rust is the outlier or the risk tail, gold is the gold button. The same idea keeps the same colour on every page.
- **Never hard-code a hex value in an SVG.** Use the semantic `.chart` classes. A literal colour that looks right in light theme disappears in dark theme, and the learner reads in both.

## Known gotchas

- **Mermaid label text with parentheses, commas, or maths breaks the parser.** Wrap every node label in double quotes: `A["P(X > 2000)"]`. This bites on almost every diagram in a statistics course.
- **Mermaid repaints in place** whenever the reader changes theme or palette, because `hub.js` re-runs it rather than reloading the page. It reads the graph source out of `node.textContent`, so a line break inside a label must be written as the entity `&lt;br/&gt;`. A literal `<br/>` is parsed into a real element, `textContent` drops it, and the two halves of the label join with no break and no space: `P(Data | Model)PROBABILITY: forward`. Measured on this course, the join happens on the **first** paint, not only after a repaint, because `hub.js` reads the source before Mermaid ever draws. A semicolon inside a label breaks the diagram the same way; use a dash.
- **Charts shrink to illegibility on a phone.** `.chart` carries a `min-width` under 640px and scrolls inside its own `.diagram` box. The page itself must never scroll horizontally: check this at 360px before you ship.
- **A Mermaid `timeline` with more than about six columns is unreadable** in a 720px reading column, because `useMaxWidth` shrinks the whole diagram rather than wrapping it. Split a long timeline into two figures rather than letting it shrink. Lecture 1's twelve-lecture plan is two timelines for exactly this reason.
- **Mermaid's mindmap root node paints its own label near-black in every theme,** which disappears on a dark background. `assets/course-extras.css` overrides it under "Mermaid corrections", and the override needs `!important` because Mermaid injects an id-scoped style block inside the rendered SVG, later in the document than our stylesheet.
- **The Mermaid branch ramp comes from the hub runtime.** `hub.js` derives `cScale0` through `cScale7` from whichever palette the reader has chosen, so mindmaps and timelines follow the page. Do not re-add a course-local override; it would pin those diagrams to one palette while the rest of the page moved.
- **`th` is uppercased,** which flattens `x - x̄` into `X - X` and drops the macron. Wrap any header carrying real notation in `<span class="exact">`.
- **The browser caches `hub.css` hard.** When a style change appears not to take effect, add a query string to the page URL before concluding the CSS is wrong.
- **`.keynum` is `white-space: nowrap`, so a long one makes the whole page scroll sideways.** Measured on Lecture 5: a 45-character quoted expression rendered 408px wide against a 287px column at 360px, and nothing in the repository catches it - the validator passes and the page looks fine on a laptop. Keep `.keynum` for a stated figure or a short coefficient, roughly thirty characters at the most, and put a full expression in `<b>` or inside a `.math` block, which scrolls within itself. Lecture 4 already uses `<b>` this way; follow it.
  This trap was walked into twice, on Lecture 5 and again on TA Session 2, so check for it rather than remembering it:
  `python3 -c "import re,html,glob;[print(len(t),f,t) for f in glob.glob('statistical-foundations-ml-course/**/*.html',recursive=True) for m in re.finditer(r'<span class=\"keynum\">(.*?)</span>',open(f).read(),re.S) for t in [html.unescape(re.sub(r'<[^>]+>','',m.group(1)))] if len(t)>26]"`
- **A parenthesis inside a Mermaid `mindmap` node is parsed as node-shape syntax.** `C(n, k) p to the k` becomes node `C` with a shape, the diagram renders as an error box, and nothing reaches the console. Double quotes do not rescue a mindmap node the way they rescue a flowchart label, so write the words instead. Keep mindmap leaves to about fifteen characters as well: a wide mindmap overflows its `.diagram` box and the reader has to scroll a figure sideways to read it.
- **The validator only checks links, not correctness.** It will happily pass a page with a wrong exponent. Check the arithmetic yourself against the slide images.

## Honesty notes carried in the pages

The lecture is a first lecture, so it is deliberately loose in places.
Three of those places are called out in the pages rather than smoothed over, because hiding them would teach a wrong habit:

1. **Comparing two confidence intervals for overlap is a rougher test than a two-proportion test.** Non-overlapping intervals do imply a significant difference, but overlapping intervals do not imply the absence of one. Page 0005 says this plainly.
2. **The exponential model is an assumption the slide adopts, not a fact the ten data points establish.** Ten points cannot identify a distribution family. Page 0004 says this plainly.
3. **The correlation slide's normalising constants do not reproduce from its own table.** Page 0007 quotes the deck's stated results, then shows what the table itself gives, and notes that the qualitative conclusion survives either way. See `learning-records/0001-quoting-a-deck-that-does-not-recompute.md` for the full decision.

Lecture 4 carries two more of the same kind, both named on its hub page before the reader meets them:

4. **The lecture writes the reverse decomposition for `P(D | -)` and never evaluates it.** Page 0049 shows the identity as the notes leave it, then works the number out in a separate callout marked as this course's own derivation. See `learning-records/0002-finishing-an-arithmetic-the-lecture-leaves-open.md`.
5. **Conditional independence gets a definition and no example.** Page 0052 supplies one - two API replicas behind a shared database - and labels it as this course's construction rather than the lecture's.

Lecture 5 carries three more, all named on its hub page 0058:

6. **Almost nothing in Lecture 5 is evaluated to a decimal.** Both sources stop at an expression. Every decimal on pages 0059 to 0068 is this course's arithmetic on the lecture's own expressions, carried in a `.callout.key` marked as such, and none of it is marked `.keynum`.
7. **Two marks on the handwritten notes cannot be read.** A stray binomial coefficient beside the quality-check line, named on page 0061 with both readings and built on with neither, and the first letter of the sixth four-image configuration, which page 0065 derives from the count instead of guessing.
8. **Two threads were parked for the next session.** A pictorial view of the complement, carried as open on page 0061, and the direct route to "both classes represented", which page 0060 shows stalling and page 0068 closes under this course's own name once the binomial has arrived.

Lecture 6 carries five more, all named on its hub page 0077:

9. **The source's own lecture number is not this course's.** The notes are titled as the lecturer's Lecture 4 and are this course's Lecture 6, because the two numbering schemes have drifted by one topic. Nothing is renumbered; `PLOT.md` row 9 is the record.
10. **The notes state one worked set of figures in eight pages.** Only the two-coin example carries numbers. Every decimal and every curve on pages 0078 to 0091 is this course's own arithmetic on the notes' own formulas, carried in a `.callout.key` and never marked `.keynum`.
11. **Four results are asserted with no proof**: that the geometric is the only memoryless discrete shape, that the exponential is the only memoryless continuous one (the notes write "prove it" and move on), that a continuous variable gives any countable set probability zero, and that the Gaussian CDF has no closed form. All four are taught as stated and the absence is named on the page.
12. **The geometric's words and its formula disagree.** "Number of coin tosses before first heads" against `p(1-p)^(k-1)`, which counts the toss the first head lands on. Page 0086 follows the formula and leaves the sentence as written.
13. **The letter N means two different sets one paragraph apart.** The geometric needs it to start at 1 and the Poisson at 0. Page 0087 runs both sums and lets the arithmetic settle each reading.

## Open threads

- Page count per lecture has settled at whatever the lecture needs rather than a fixed nine: six for Lecture 2, eight for Lecture 3, twelve for Lecture 4, ten for Lecture 5, seven for TA Session 2, fourteen for Lecture 6. One idea per page is the constraint; the total falls out of it, and for a tutorial it falls out of the question count.
- No learning record on the learner's own recall yet. Add one after a lecture has actually been worked through, not merely read.
- A print-friendly formula sheet exists for Lectures 1, 2, 3, 4, 5 and 6. Keep one per lecture rather than growing a single sheet that nobody prints.
