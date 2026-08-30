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
| `.fig-cap` labels over 6 words | **0** |
| `.fig-claim` sentences over 15 words | **0** |

The kind bar exists because a flowchart is the diagram you reach for when you have not asked what the reader is confused about.
A reader confused about *order* needs a `sequenceDiagram`.
A reader confused about *what state the thing is in* needs a `stateDiagram-v2`.
A reader confused about *how big* needs a chart, and Mermaid cannot draw one.

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
`check_pages.py` fails a label over six words and a label that is a question, because both are defects in what an author wrote.
It does not fail a figure with no label at all, and it must not: requiring one would fail every figure written before the widget existed, and a generated label is worse than none.
A page you are writing now is held to the bar; a page you are not touching is not.

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
