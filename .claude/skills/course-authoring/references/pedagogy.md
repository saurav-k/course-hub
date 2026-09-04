# The teaching bar

Counts, not qualities.
"Diagram-heavy" is an aspiration and every course claims it; "three diagrams, two kinds, one quantitative" is a bar a page either clears or does not.

Everything here is checked by `.claude/skills/course-authoring/scripts/check_pages.py`, either as a failure or as a warning.

The shape those counts add up to:

```
eyebrow -> h1 -> paper-meta -> one-minute version -> ORIENTATION FIGURE -> the sections -> quizzes
                                                     where this sits        the detail
                                                      in the whole
```

## The orientation figure

**The big picture comes first.**
Every content page opens with a figure that shows where this idea sits in the whole: what larger thing it is part of, what came before it, what it enables.

| Bar | Value |
|---|---|
| position | the page's **first** `<figure>` |
| body sections opened before it | **0**; it stands between the one-minute version and the first section |
| prose words before it | **250 maximum** |
| things it draws | **3 minimum**: what came before, this, what it enables |
| content pages without one | **0** |

The test it has to pass: a reader who reads the opening sentence, looks at this figure, and reads nothing else can say what the page is about and why it exists.

It is not a decorative header and it is not the mechanism drawn early.
The mechanism figure belongs beside the mechanism.
This one is the map the reader keeps in the corner of their eye for the rest of the page.

It counts towards the diagram floor below.

## Fewer words

The page carries its meaning in figures and short prose, not in paragraphs the reader must hold in their head.

| Bar | Value |
|---|---|
| prose words per content page | **1,800 maximum**, 900 to 1,400 typical |
| prose words per figure | **400 maximum** |

**When a paragraph and a figure say the same thing, the paragraph goes.**
Not both, and not the figure.

Prose is what is left of the reading column once the figures, the code, the quizzes and the page chrome are taken out.
It is the quantity the reader has to hold, which is why it is the quantity the bars are stated in.

Both numbers are measured rather than chosen.
Every one of the 54 pages in `llm-papers-course` and `llm-inference-course`, the two courses that read best, clears both: their longest page is 1,716 words and their densest is 394 words per figure.
A ceiling that fails a good page is a wish, not a bar.

A page over the ceiling is usually two pages, and splitting it beats cutting it.
A page over the density ceiling is usually one figure short, and the missing one is the picture some paragraph is describing in words.

The reading-time pill is prose words divided by 200, plus half a minute for each figure and each quiz, rounded.
It is an estimate and it only has to be honest; the point is that a reader arriving from a search result knows whether they have time for the page.

## Diagrams

| Bar | Value |
|---|---|
| diagrams per content page | **3 minimum**, 4 to 6 typical |
| distinct diagram kinds per page | **2 minimum** |
| distinct diagram kinds across the course | **4 minimum** |
| pages that are all flowchart | **0** |
| figures without a `<figcaption>` | **0** |
| figcaptions without a bolded takeaway | **0** |
| figures on a new page without a `.fig-cap` label | **0** |
| `.fig-cap` labels over 5 words | **0** |
| `.fig-claim` sentences over 15 words | **0** |

The kind bar exists because a flowchart is the diagram you reach for when you have not asked what the reader is confused about.
A reader confused about *order* needs a `sequenceDiagram`.
A reader confused about *what state the thing is in* needs a `stateDiagram-v2`.
A reader confused about *how big* needs a chart, and Mermaid cannot draw one.
A reader confused about *what is where* needs a diagram drawn by hand, because the moment position carries meaning Mermaid has no way to express it.

**A page whose figures are all the same instrument has probably not asked the question at all.**
A chart answers *how much*. A diagram answers *what is where*. Mermaid answers *what connects to what*, when any sane layout will do.
Most technical pages need at least two of the three, and the checker counts them that way: a hand-drawn diagram, a hand-drawn plot and a hand-drawn chart are three kinds, not one.

The kinds, and what each is for, are in [`widgets.md`](widgets.md).

**Quantitative claims need a quantitative figure.** A page that states a distribution, a trend over time, a spread, or a magnitude comparison owes the reader an inline `<svg class="chart">`, hand-authored. Prose saying "the tail is heavy" next to a flowchart is a claim without a picture.

**A figure with no takeaway is decoration.** If you cannot write the bolded sentence in the figcaption, cut the figure. Every figcaption explains the diagram in plain English and bolds the one thing to carry away.

**The figure's text budget is fifteen words above the drawing and a short reading below.**
The label is the subject, the claim is what the drawing proves, and the caption is the reading a learner checks their own understanding against.
The shape of the two lines above is in [`widgets.md`](widgets.md); the numbers are here, because they are what a page is measured on.

Figure text is not counted by the word ceiling - `check_pages.py` strips the whole `<figure>` block before it counts prose - so it is the one place on a page where length is nobody's problem, and it has become the place where length goes.
Measured across the hub: 2,934 captions, a median of 57 words, 165,597 words in total.
That is 219 words a lesson page, 12% of the prose ceiling, none of it counted.
When a caption runs past about 40 words, the sentence it is really trying to write belongs in the `.fig-claim` and the rest belongs in the body or nowhere.

The first of the three new rows is a bar and not a gate, and the difference matters.
The other two are gates: `validate_site.py` fails a label over five words, on the same rule that already holds a page's own `.eyebrow` to five, and `check_pages.py` fails a label or a claim written as a question and warns on a claim past fifteen words.
Nothing fails a figure with no label at all, and nothing must: requiring one would fail every figure written before the widget existed, and a generated label is worse than none.
A page you are writing now is held to the bar; a page you are not touching is not.

## Interaction

A diagram is read and a quiz is answered.
An interactive figure is **operated**, which is a third thing, and it is the one the counts above miss.

| Bar | Value |
|---|---|
| interactive figures on a page with something to manipulate | **1 minimum** |
| interactive figures on a page with nothing to manipulate | **0**; a widget with no state to move is decoration with a control on it |
| distinct interactive shapes across the course | **3 minimum** of the five, on a course of ten pages or more |
| interactive figures whose committed default values are wrong | **0** |
| interactive figures that break when the script is blocked | **0** |
| interactive figures with no `figcaption` telling the reader what to move first | **0** |

**"Something to manipulate" is a state, a budget, a file, a score, or a boundary**, and the test is whether the page already argues about one.
A lesson that walks a trace has a state.
A lesson that says a cost is linear in two numbers has a budget.
A lesson that tells the reader what belongs in a file has a file.
A lesson that judges a thing on several dimensions at once has a score.
A lesson about who wrote which part of a request has a boundary.
A lesson with none of the five owes no interactive figure, and adding one anyway produces a control that does nothing a paragraph did not.

**Which interaction answers which confusion**, read the same way as the diagram-kind table above:

| The reader is confused about | Reach for |
|---|---|
| a trace, a loop, an exchange that goes round twice | the **stepper** |
| a file they are about to write, and what each part of it costs | the **assembler** |
| a number they will argue with, at their own inputs | the **calculator** |
| a judgement that has several dimensions and one answer | the **scorecard** |
| where the trust boundary is inside one thing | the **taint map** |
| whether the idea landed | a **quiz**, which is the reveal they already know |
| whether they can use it | a **practice problem**, whose `details.solution` is the other reveal |

The markup for the five is in [`widgets.md`](widgets.md), "Five figures a reader operates", and the shapes are shared: no course writes a line of JavaScript to use one and no course invents a sixth.

**None of this bar is machine-checked, and none of it can be.**
`check_pages.py` counts an interactive figure as a `<figure>` and holds it to the caption bar, which is the whole of what a script can say: whether a lesson has a budget in it is a reading of the lesson.
The one number a machine could report is the one that would be gamed.
Measured on the course this bar comes from: 83 lessons carrying 80 interactive figures - 25 steppers, 22 calculators, 15 assemblers, 15 scorecards and 3 taint maps - which is about one a page and five kinds across the course, and it is the shape to match rather than the total.

## Cognitive load

The learner should never have to hold more than one new thing at a time, and never have to fill a gap you skipped.

| Bar | Value |
|---|---|
| new named concepts per paragraph | **1** |
| `.math` blocks without a `.gloss` | **0** |
| symbols used before being named in words *on this page* | **0** |
| formula appearing before its picture | **0** |

**A bar the neighbouring pages miss is still a bar.**
Most pages in this hub predate this file and carry no rung pill, no reading-time pill, and no orientation figure.
`new-lesson.md` tells you to match the neighbours for voice, depth and structure, and that is what it means: voice, depth and structure.
It does not mean inheriting a missing widget.
Write the page to the bar and say in the pull request that its neighbours still miss it.

## Level progression

A course declares its ladder in `MISSION.md` and every page states its rung.
Three rungs, and the class names already exist in `assets/hub.css`:

| Rung | Class | The learner at this rung |
|---|---|---|
| foundation | `pill easy` | arrives cold; every term is defined here or in a named earlier page |
| working | `pill med` | has the foundation pages; can be given a mechanism and a trade-off directly |
| frontier | `pill hard` | has the working pages; can be handed an open question, a live disagreement, or a paper |

The ladder is a claim about *dependencies*, so it is checkable: read the map in order and confirm no page needs a page that comes later.

Two rules keep it honest:

- **Every lesson card carries exactly one rung pill,** and the pill text is the rung word. The class is not a colour: `pill easy` reading "labs" tells the reader nothing about difficulty and burns the only signal the card has.
- **Every page carries its rung and its reading time** in `.paper-meta`, so a reader who arrived from a search result knows what they walked into.

A course with no genuine progression is a reference work.
That is a fine thing to be, and `MISSION.md` should say so plainly rather than claim a ladder the pages do not have.

## Active recall

| Bar | Value |
|---|---|
| quizzes per content page | **2 minimum** |
| options per quiz | **exactly 4** |
| character spread across the four options | **12 maximum** |
| quizzes without a `.q-fb` | **0** |
| share of a course's answers at any single index | **40% maximum** |

The index bar is the one that is easy to miss and easy to exploit.
Options matched to the character are worthless if the answer is the first option nine times out of ten: the reader learns the pattern, not the material.
Vary the index deliberately and check the distribution over the whole course, never over one page.

`.q-fb` explains **why each wrong option is wrong**, not merely why the right one is right.
The strongest distractor is a true statement that answers a different question, and the feedback is where you tell the reader which question it answered.

Quizzes come after the idea has been fully worked, never as a gate in front of it.

## Practice problems

A quiz checks that the idea landed. A problem checks that the reader can use it.

| Bar | Value |
|---|---|
| practice problems per content page | **1 minimum** |
| problems without a `details.solution` | **0** |
| problems without a `.p-check` sanity line | **0** |
| inline `svg.chart` per content page | **1 minimum** |

These four are newer than the seven courses that predate this file, so a course **opts into them by name** in `EXTENDED_BAR_COURSES` at the top of `check_pages.py` rather than inheriting them and turning every legacy page red.
Joining that set is the last step of a retrofit, not the first.

The chart floor is the one that decides whether a quantitative course is quantitative.
A page that states a distribution, a magnitude or a spread and draws only boxes and arrows has made a claim it did not show, and Mermaid cannot draw any of the three.

`.p-check` exists because a reader working alone has no marker.
One sentence saying what the answer should roughly be and why lets them catch their own arithmetic: "the trace is 4 and the eigenvalues sum to 4, so 3 and 1 is plausible and 3 and 2 is not."

## Sources

| Bar | Value |
|---|---|
| technical claims with no linked source | **0** |
| sources cited without being fetched this session | **0** |
| numbers attributed to a source but not present in it | **0** |
| blog posts cited where the primary source exists | **0** |

A number you derived yourself is welcome, and it must show its arithmetic and name its assumptions, so the reader can tell your derivation from someone else's measurement.
A claim with no citable source goes in `RESOURCES.md` under `## Gaps`, not into the page with a hedge.

### A quoted file states where it came from and whether it may be here

A citation says where a claim came from.
**A sample is different, because the page is not citing the file, it is redistributing it**, and a hub page is published on the open web.

| Bar | Value |
|---|---|
| quoted config, file or code samples with no source, licence and verdict above the block | **0** |
| samples whose licence could not be established | **0** on the page; paraphrased, or left out |
| samples shown with an ellipsis where the reader needs the whole file | **0** |

The four facts go in the `.code-cap` directly above the block, in this order, because that is a line that travels with the sample when it is collected onto a gallery page:

```html
<div class="code-cap">AGENTS.md &middot; cloudflare/agents &middot; MIT &middot; reproduced verbatim</div>
```

1. **What it is**, including the filename it belongs at.
2. **Where it came from**, as a source the reader can open.
3. **Its licence**, named. Not "open source": the licence.
4. **The verdict**: `reproduced verbatim`, or `paraphrased`.

**A sample whose licence cannot be established is paraphrased or omitted**, never shown with the licence field left vague.
"No LICENSE file in the repository" is an answer and the answer is paraphrase.
Where a licence permits reproduction with attribution, the caption *is* the attribution and it is not optional.

**This repository is the exception that costs nothing.** Its content is CC BY 4.0 and its code MIT, so a course may quote its own hub in full.

**A course that quotes real files enough to lose track of them owes a gallery**, which is one reference page collecting each artefact complete, with the same four facts unchanged, and a table of what is there against where each one is developed.
`ai-software-developer-course/reference/samples.html` is the pattern.
The gallery is why the four facts live in the caption rather than in prose beside the block: prose does not survive being collected.
