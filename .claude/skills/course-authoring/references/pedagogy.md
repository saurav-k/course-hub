# The teaching bar

Counts, not qualities.
"Diagram-heavy" is an aspiration and every course claims it; "three diagrams, two kinds, one quantitative" is a bar a page either clears or does not.

Every row a script can count is counted by `.claude/skills/course-authoring/scripts/check_pages.py`, as a failure or as a warning, and the rows it cannot see say so where they stand: whether an outcome is an action, whether a worked instance is the right one, whether a source says what the page says it says.
The rubric in [`../retrofit.md`](../retrofit.md) marks each row `M` or `J` for the same reason.

The shape those counts add up to:

```
eyebrow -> h1 -> paper-meta -> LEARNING CONTRACT -> one-minute version -> ORIENTATION FIGURE -> the sections -> quizzes -> practice -> RECAP
                               what you can do                             where this sits        the detail                            what to carry,
                               afterwards, and                             in the whole                                                  and where next
                               what you need first
```

## The learning contract and the recap

A stranger opens a page and needs two answers before the idea and two after it: is this page mine and what do I need first; what do I now carry and where do I go.
Two cards answer them, and both are counted.

| Bar | Value |
|---|---|
| content pages without a `.card.outcomes` directly under `.paper-meta` | **0** |
| learning outcomes per page | **1 to 3**, each an action the reader could be watched doing |
| `.card.outcomes` without a `.prereq` line | **0**; "nothing needed" is stated, never implied |
| content pages without a `.card.recap` after the practice | **0** |
| recap points per page | **2 to 4**, none of them a copy of a one-minute-version bullet |
| recaps without a `.next-step` that links the next page and gives the reason | **0**, and the missing link is a FAIL |

One to three outcomes, because a page has one idea and an outcome is one thing the reader can do with it.
Two to four recap points, because a recap longer than the one-minute version is the page again.
The next step carries the one thing the pager cannot: why to go there.
The markup for both is in [`widgets.md`](widgets.md); a lecture hub page, named `*-start-here.html`, is a map rather than a lesson and owes neither.

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
| words in one paragraph | **120 maximum**; measured over 16,920 hub paragraphs, the median is 41 and the 99th percentile 141 |
| `.callout.warn` per page | **1 maximum**; a page with three warnings has no warning |
| pages in a course with a glossary that do not link it | **0**; a reader stalled on a term needs one click, not a search |

**When a paragraph and a figure say the same thing, the paragraph goes.**
Not both, and not the figure.

A paragraph over the ceiling is two ideas wearing one indent, and the fix is a split at the idea boundary rather than a cut.

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
| formula appearing before the page's first figure | **0**; the reader gets the picture before the symbols |
| pages that state a formula and work no instance of it in an `ol.worked` | **0**; a worked example comes before, or beside, the general statement |

The last two are what "a worked example before the abstract statement" comes to when a script counts it: the first `.math` on the page sits after the first `<figure>`, and a page with a formula on it has at least one `ol.worked`.
Whether the worked instance is the right one is a reading of the page.

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

Three rules keep it honest, and the first is a FAIL rather than a bar:

- **The rung pill's text is the rung word** - `foundation`, `working` or `frontier` - and nothing else. The class is not a colour: `pill easy` reading "labs" or `pill med` reading "first real arithmetic" tells the reader nothing about difficulty and burns the only signal the page has. `check_pages.py` fails any other text.
- **Every lesson card carries exactly one rung pill,** and the course map is counted against its lessons.
- **Every page carries its rung and its reading time** in `.paper-meta`, rung first, so a reader who arrived from a search result knows what they walked into.

| Bar | Value |
|---|---|
| rung pills whose text is not the rung word | **0**, a FAIL |
| pages with the reading-time pill before the rung pill | **0** |
| pages whose `<h1>` repeats the lesson's name from the course map | **0**; the h1 is the one idea as a claim with a verb in it, and the card is the name |

A course with no genuine progression is a reference work.
That is a fine thing to be, and `MISSION.md` should say so plainly rather than claim a ladder the pages do not have.

## Navigation

A reader knows where they are from three things the page did not write: the eyebrow, the fixed chapter bar, and the sidebar rail.
The rail and the bar are built from the generated outline, and the pager is written by hand, so the pager is the one that can disagree.

| Bar | Value |
|---|---|
| content pages without a `.pager` | **0**, a FAIL |
| pagers whose previous or next is not the neighbour the course map gives the page | **0**; the chapter bar follows the map, so a pager that does not shows two different "next" links at the foot of one page |
| pages with no link to `../index.html` | **0**; the spine carries it on every page today |

A course that deliberately reads a page out of map order - a solution page whose "next" is the matching practice set - states the reason in the pull request, and the warning stands until the map is changed to agree.

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
| problems without a `details.solution` | **0**, a FAIL on every course |
| problems without a `.p-check` sanity line | **0**, a FAIL on every course |
| inline `svg.chart` per content page | **1 minimum** |

The two floors are newer than the seven courses that predate this file, so a course **opts into them by name** in `EXTENDED_BAR_COURSES` at the top of `check_pages.py`: there a page with no problem or no chart is a FAIL, and everywhere else it is a WARN the retrofit rubric still counts.
The shape of a problem that is there is held on every course alike, because a problem with no solution fails the reader working alone wherever it sits.
Joining the set is the last step of a retrofit, not the first.

The chart floor is the one that decides whether a quantitative course is quantitative.
A page that states a distribution, a magnitude or a spread and draws only boxes and arrows has made a claim it did not show, and Mermaid cannot draw any of the three.

`.p-check` exists because a reader working alone has no marker.
One sentence saying what the answer should roughly be and why lets them catch their own arithmetic: "the trace is 4 and the eigenvalues sum to 4, so 3 and 1 is plausible and 3 and 2 is not."

## Sources

| Bar | Value |
|---|---|
| technical claims with no linked source | **0** |
| content pages with no external link anywhere in the reading column | **0**; the one proxy a script has for the row above |
| sources cited without being fetched this session | **0** |
| dead or redirected-to-nothing links, by `check_pages.py <course> --links` | **0** after a second try, and the try is stated in the pull request; a 403, 406 or 429 is a site refusing robots and is opened in a browser instead |
| numbers attributed to a source but not present in it | **0** |
| blog posts cited where the primary source exists | **0** |

A number you derived yourself is welcome, and it must show its arithmetic and name its assumptions, so the reader can tell your derivation from someone else's measurement.
A claim with no citable source goes in `RESOURCES.md` under `## Gaps`, not into the page with a hedge.
A page built entirely from a source the course itself owns - a homework solution whose source is the homework - links that page and says so; it is still a link.

## The course map, as a learner reads it

The map is what the learner buys before they open a page, and it is counted too.

| Bar | Value |
|---|---|
| lesson cards without a reading-time pill | **0**; a reader chooses a page by what it costs |
| lesson cards without a rung pill | **0** |
| course maps whose hero does not state the total time in hours and what one page costs | **0** |
| courses without a `reference/glossary.html` | **0** |
| hub cards whose page count differs from the folder | **0**, a FAIL |
| reference sheets the hero or a card promises that do not exist | **0**; `validate_site.py` fails the dead link, and a promise made in prose is yours to check |

What the hero says the learner will be able to do is a reading, not a count: it is phrased as actions, and it is the same list `MISSION.md` calls success.

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
