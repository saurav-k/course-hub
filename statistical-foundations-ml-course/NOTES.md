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

Lecture 6 has two sources now - the lecturer's pre-class notes and the delivered session of Tuesday 1 September 2026 - and carries nine notes, all named on its hub page 0077:

9. **The numbering question is closed by the delivered session.** The class board is headed "Lecture 6" in the lecturer's own hand and dated 1 September 2026, which agrees with this course. Only the **pre-class** document carries a stale title, and that document is what created the appearance of a drift in the first place.
10. **Numbers now come from both sources.** The pre-class notes work only the two-coin example; the delivered session works the CDF from minus five thousand, three die intervals, the four Bin(3, 1/2) masses and a biased-coin PMF. Everything else on pages 0078 to 0091 is still this course's own arithmetic, carried in a `.callout.key` and never marked `.keynum`.
11. **Pages 0088 to 0091 were never delivered in this session.** The room stopped after the Poisson and the lecturer named the continuous case as the next class's work, which is where it was delivered, as Lecture 7. Those four pages rest on the pre-class notes alone and each one says so in a callout linking its Lecture 7 counterpart.
12. **The geometric's index was settled live.** The pre-class notes' words and formula disagreed; in the room the lecturer settled k as the toss the first head lands on, which is also Ross 4.8.1's definition. Page 0086 follows that and records where the wording came from.
13. **Three smaller partings, each named on its page.** Memorylessness is proved in the notes and only asserted in the room; a spoken "1 in 100" contradicts the board's written 0.1 for the same email example; and the discrete uniform has one source only, because the room named four shapes rather than five. The letter N still means two different index sets one paragraph apart in the notes, and page 0087 lets the arithmetic settle each reading.

Lecture 7 rests on the class notes and the full session transcript, and carries seven notes, all named on its hub page 0096:

14. **Two of the three error probabilities the session quotes belong to a neighbouring sample size, and the transcript says why.** The lecture opened those two cases at n = 20 and n = 100. A student objected that an even split is a tie, so the board moved to 21 and 101 - and the prepared figures never followed the repair. Recomputed, the binomial gives 0.1744 and 0.0209 against the quoted .25 and .03, which are the n = 20 and n = 100 values. A student computed 0.17 live and challenged it. Page 0098 carries the repair and the recomputation; the n = 5 figure is sound.
15. **One identity was written wrong on the board and corrected live.** `P(X > 4) = 1 - F_X(3)` became `1 - F_X(4)` after a student caught it, and the class notes carry the corrected form. Page 0101 names the slip rather than quietly printing the right version, because that off-by-one is the mistake a reader is about to make alone.
16. **Three results are asserted, and one of them is only sketched**: that a continuous CDF is differentiable almost everywhere, that the Gaussian CDF has no closed form, and that every exact value carries probability zero, the last argued from a shrinking band rather than proved. All three are taught as stated.
17. **Memorylessness is proved in one direction only in this course.** The session proves the exponential is memoryless and never proves it is the only such law. That uniqueness is not unproved everywhere: Ross proves it in Section 5.5, and page 0107 now says how rather than leaving the claim standing on assertion.
18. **The Gaussian is offered for a quantity it does not fit.** A student objected that heights are never negative while a Gaussian puts weight across the whole real line. The lecturer agreed, said practitioners use it anyway when the negative tail carries almost nothing, and offered the repair - model the deviation from the sample mean. Page 0108 carries the objection and the repair together.

A sixth thing about Lecture 7 is not an honesty note but is worth recording: **mu, sigma and lambda arrive with no definition on purpose**. The lecturer said, when asked directly, that mu is the expected value, sigma squared the variance and the exponential's mean 1/lambda, then said the course has not reached those ideas and moved on. These pages do the same, and page 0096 says so under its own heading rather than letting a reader think it was overlooked.

Lecture 8 was delivered on Tuesday 8 September 2026 and covers expectation only. It carries five notes, all named on its hub page 0110:

19. **The delivered session is dated and numbered; the pre-class notes are not.** The class notes are headed Lecture 8 and dated 8 September 2026. The nine-page pre-class document carries neither, and it is the pre-class document alone that the earlier version of this note described.
20. **Three means are handed over as exercises.** The exponential, the geometric and the binomial means are stated and left to the reader in the room. This course works them and labels each as its own derivation rather than the lecture's.
21. **The second-derivative test was omitted on the board and supplied from the floor.** In the inventory example the lecturer set the first derivative to zero and stopped; a student asked for the second-derivative check and the lecturer conceded it should be done. Page 0160 carries both. The pre-class notes' own two unanswered margin questions - the general definition of expectation, and whether the balls-and-bins indicators are independent - belong to that document rather than to the delivered session.
22. **The Cauchy was called infinite aloud and undefined in the notes.** Page 0113 keeps the two apart and says why undefined is the stronger verdict. Outside the inventory example the session states almost no numbers at all, so every decimal on pages 0111 to 0117 is this course's own arithmetic and none of it is marked `.keynum`.

TA Session Week 3 carries four, all named on its hub page 0120:

23. **The word "support" was used before the class had met it.** The tutor used it in the revision block, noticed it had not been defined in any lecture, and withdrew it mid-session. Page 0121 defines it and records that it arrived early.
24. **The exponential series is asserted in both sittings and proved in neither.** It is what forces the normalising constant in Problem 5, and page 0126 says the identity is taken as given.
25. **The fast sitting's working is headed "probability mass function" over a cumulative one.** A student caught it and the tutor agreed to correct it. Page 0125 carries the heading as written and the correction beside it.
26. **The sheet has eleven problems and the week reached seven.** One more was set as homework and appears as a practice block; three were never touched in any sitting and are named on the hub without pages, rather than solved under a source that never solved them.

## When pre-class notes overrun the delivered session

This has now happened twice, so it is a policy rather than an incident.
Lecture 6's pages were written from pre-class notes and the room stopped four pages short of them; Lecture 8's pages were written the same way and the room stopped at expectation, three pages short of the variance and covariance material.

**Keep the numbers, relabel the page, and reconcile in place when the session lands.**
Nothing is renamed or renumbered, because the URLs are public.
A page the class has not reached carries a callout saying so at the top and an eyebrow naming it as the next session's pre-read; a page the class reached by a different route keeps its number and gains a section carrying what the room added.
The course map groups the not-yet-delivered pages separately from the delivered parts so a reader never mistakes one for the other.

## Deliberate repetition, which this course had not had before

Lecture 7 is the first session in this course that covers ground an earlier lecture already covered.
Lecture 6 came from the lecturer's pre-class notes and defined the density, the uniform, the exponential and the Gaussian; Lecture 7 is the same material delivered live.
The policy settled on, and the one to follow if it happens again: **keep both, at their true positions, and make every overlapping page link to its counterpart and say what is new here.**
Nothing was merged and nothing was renumbered.
What the delivered session adds is what a pre-class note cannot carry - two examples worked from a sentence about the world down to a number, the room's own objections, a proof left earlier as an exercise, and the modelling judgement at the end - and the hub page 0096 states that argument once so no individual page has to defend itself.

## Open threads

- Page count per lecture has settled at whatever the lecture needs rather than a fixed nine: six for Lecture 2, eight for Lecture 3, twelve for Lecture 4, ten for Lecture 5, seven for TA Session 2, fifteen for Lecture 6, thirteen for Lecture 7, ten for TA Session 3, seven for Lecture 8 plus three pages of the next session's pre-read. One idea per page is the constraint; the total falls out of it, and for a tutorial it falls out of the question count.
- No learning record on the learner's own recall yet. Add one after a lecture has actually been worked through, not merely read.
- A print-friendly formula sheet exists for Lectures 1 to 8. **TA Session 3 has none yet** and its pages point at the Lecture 7 sheet; one sheet per session is the policy, so that gap is open work. Keep one per lecture rather than growing a single sheet that nobody prints.
