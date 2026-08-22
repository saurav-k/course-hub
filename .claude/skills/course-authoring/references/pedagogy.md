# The teaching bar

Counts, not qualities.
"Diagram-heavy" is an aspiration and every course claims it; "three diagrams, two kinds, one quantitative" is a bar a page either clears or does not.

Everything here is checked by `.claude/skills/course-authoring/scripts/check_pages.py`, either as a failure or as a warning.

## Diagrams

| Bar | Value |
|---|---|
| diagrams per content page | **3 minimum**, 4 to 6 typical |
| distinct diagram kinds per page | **2 minimum** |
| distinct diagram kinds across the course | **4 minimum** |
| pages that are all flowchart | **0** |
| figures without a `<figcaption>` | **0** |
| figcaptions without a bolded takeaway | **0** |

The kind bar exists because a flowchart is the diagram you reach for when you have not asked what the reader is confused about.
A reader confused about *order* needs a `sequenceDiagram`.
A reader confused about *what state the thing is in* needs a `stateDiagram-v2`.
A reader confused about *how big* needs a chart, and Mermaid cannot draw one.

The kinds, and what each is for, are in [`widgets.md`](widgets.md).

**Quantitative claims need a quantitative figure.** A page that states a distribution, a trend over time, a spread, or a magnitude comparison owes the reader an inline `<svg class="chart">`, hand-authored. Prose saying "the tail is heavy" next to a flowchart is a claim without a picture.

**A figure with no takeaway is decoration.** If you cannot write the bolded sentence in the figcaption, cut the figure. Every figcaption explains the diagram in plain English and bolds the one thing to carry away.

## Cognitive load

The learner should never have to hold more than one new thing at a time, and never have to fill a gap you skipped.

| Bar | Value |
|---|---|
| new named concepts per paragraph | **1** |
| `.math` blocks without a `.gloss` | **0** |
| symbols used before being named in words *on this page* | **0** |
| reading minutes per page | **8 to 12** |
| formula appearing before its picture | **0** |

The reading-time bar is a grain rule, not a length limit.
A page at 25 minutes is two ideas wearing one title, and the fix is to split it rather than to cut it.

The number on the pill is prose words divided by 200, rounded to the nearest minute, plus one minute for each figure and each quiz.
It is an estimate and it only has to be honest; the point is that a reader arriving from a search result knows whether they have time for the page.

**A bar the neighbouring pages miss is still a bar.**
Most pages in this hub predate this file and carry no rung pill and no reading-time pill.
`new-lesson.md` tells you to match the neighbours for voice, depth and structure, and that is what it means: voice, depth and structure.
It does not mean inheriting a missing widget. Add the pills to the page you are writing and say in the pull request that its neighbours still lack them.

## Level progression

A course declares its ladder in `MISSION.md` and every page states its rung.
Three rungs, and the class names already exist in `assets/hub.css`:

| Rung | Class | The learner at this rung |
|---|---|---|
| foundation | `pill easy` | arrives cold; every term is defined here or in a named earlier page |
| working | `pill med` | has the foundation pages; can be given a mechanism and a trade-off directly |
| frontier | `pill hard` | has the working pages; can be handed an open question, a live disagreement, or a paper |

The ladder is a claim about *dependencies*, so it is checkable: read the map in order and confirm no page needs a page that comes later.

Two rules keep the ladder honest:

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

## Sources

| Bar | Value |
|---|---|
| technical claims with no linked source | **0** |
| sources cited without being fetched this session | **0** |
| numbers attributed to a source but not present in it | **0** |
| blog posts cited where the primary source exists | **0** |

A number you derived yourself is welcome, and it must show its arithmetic and name its assumptions, so the reader can tell your derivation from someone else's measurement.
A claim with no citable source goes in `RESOURCES.md` under `## Gaps`, not into the page with a hedge.
