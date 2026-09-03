# Notes

How this course teaches, and what the authoring cost.
Read `MISSION.md` first for why it exists, then `BUILDER-SPEC.md` for what differs from the house standard.

`MISSION.md` is the contract and changes rarely. This file is the working memory and should change often.

## Learner profile

Fluent: the shell, git, HTTP, one mainstream language, a pull-request workflow, and thousands of hours of driving an assistant.
Friction: anything that reads as a product announcement, anything that assumes they have never used an agent, and anything that asks them to accept a mechanism on trust.

**The useful distinction to hold: they are a beginner in the machine without being a beginner in software.**
Those two take opposite tones. Explain the loop from nothing, because they have never seen it. Do not explain what a pull request is, what CI does, or why a test suite matters.
A page that opens by defining "large language model" has lost them; a page that says "the harness assembles the request" without saying what a request contains has lost them too.

They also arrive with a specific kind of folklore, which is the most valuable thing to write against.
They believe prompt wording is the lever, because it is the only lever they have ever touched.
Nearly every module has a page whose job is to replace one lever with a better one: a file, a hook, a permission rule, a trigger, a scanner rule.

## Cadence

One page is 900 to 1,400 prose words, three to five figures, two quizzes, and one hand-drawn figure whenever the page states a quantity.
The word ceiling is 1,800 and this course should rarely be near it.

**The orientation figure on a page of this course draws where the reader's hands are.**
Not where the idea sits in an abstract taxonomy: what came before is the artefact the previous page had them write or read, this page is the next one, and what it enables is the thing they can then do.
That is the shared shape and it is what makes the course read as one sequence rather than as ten topic surveys.

A page ends when the reader could do the thing. If a page ends with them knowing about the thing, it is unfinished.

Quizzes come after the idea is fully worked, never as a gate in front of it.
Vary the answer index deliberately: the cap is 40% of a course's answers at any one index, and it is checked over the whole course rather than over one page.

## Teaching preferences

**Mechanism over product, every time.** The test in `MISSION.md` is the one to apply while drafting, not while reviewing: if the named product disappeared, would this page still be worth reading?
The house form is to teach the axis and cite the products as evidence for it. `0810` is the type case and the hardest one.

**Show the file.** Every configuration this course mentions appears complete in a fenced block with a language tag. A fragment with an ellipsis teaches nobody to write the file.
The licence rule that comes with that is in `BUILDER-SPEC.md` and it is not optional.

**Interactivity over theory.** Five interactive figure shapes ship with this course - a stepper, an assembler, a calculator, a scorecard and a taint tracer - and a page that could use one and writes three paragraphs instead has chosen the worse tool.
When a paragraph and a widget say the same thing, the paragraph goes.

**Callouts carry the non-prose.** Warnings, decisions, "why this matters" and field notes are visibly separated from prose, which is the captain's fourth guideline. A `.callout.warn` is also where an honest limit goes, and this course has several.

**Link out rather than re-derive.** Where a sibling course owns a mechanism, name the page and move on. `MISSION.md` has the table and `BUILDER-SPEC.md` has the rule for when a link is worth making.
Do not cross-link for completeness: a link that only says "this exists elsewhere too" costs the reader a click and returns nothing.

## Structure decisions

**Lesson pages, not chapters.** Argued in full in `MISSION.md`. The short version is that the interactive shapes are per-idea and a chapter carrying six of them would compete with itself.

**Block numbering stepping by ten**, so a lesson added later inside a module never forces file order to disagree with teaching order. `PLOT.md` states the rule and the reason.

**The capstone is a track, not a tail.** Four pages numbered `11xx` for permanence, read at the end of the modules that supply them. `PLOT.md` is where that disagreement is written down, because it is the one place the house standard allows it.

**Not routed.** Rejected explicitly: there is one order, the syllabus states it, and a routed course costs a hand-written manifest, a committed pager per page and a generator that refuses to run.

**No `assets/` folder and no course stylesheet.** A course owns the seven tokens of the course contract, and this one declares exactly one of them.

## Known gotchas

Symptom first, then cause, then fix, because the next author arrives with the symptom.

**A diagram is a red error box, or a label reads as two words run together after the reader changes theme.**
`hub.js` stashes Mermaid source as `textContent` so it can repaint on a mode or palette change.
A `<pre class="mermaid">` picks up the injected copy button as a final line of source and is wrong on first paint; a literal `<br/>` is parsed into a real `BR`, which `textContent` drops, and is wrong only *after* a repaint.
So: `<div class="mermaid">`, `&lt;br/&gt;`, and **look at every figure in both render states**. One state alone catches neither reliably.

**A Mermaid diagram fails to parse and this course will hit it more than most.**
Every node label is wrapped in double quotes, always. This subject is full of parentheses, commas, shell syntax and file paths, and `A[claude -p "..." | jq]` does not parse bare.
A semicolon inside diagram text is a statement separator - fatal in a `sequenceDiagram` message or `Note over` - so write a dash everywhere.

**A flowchart is missing a node at the right edge and nothing reported it.**
A `flowchart` grows unboundedly across its stated direction, so a `TB` graph with several roots lays out wider than the reading column and is clipped at the column edge.
Agent-loop diagrams are exactly this shape. Turn the direction, or cut the row to three or four nodes, and measure the rendered `svg` against its `figure`.

**A hand-drawn figure contradicts itself and passes every gate.**
The `d-*` classes make fill mean something, so a `d-ghost` box with a live `d-flow` into it says "removed" and "busy" at once.
Nothing in this repository can catch that. Read every drawing for what its roles claim, at 360px and at full width, and read the longest line of text in it: SVG text neither wraps nor is bounded by the `viewBox`.

**A roadmap entry that became a link fails the validator.**
Every unwritten lesson in `index.html` is plain text inside `.roadmap`. This course carries more unwritten pages than written ones for most of its life, so this will bite repeatedly.

**A Mermaid `timeline` overflows the reading column and hides its last period.**
Mermaid lays a timeline out at a fixed width per period regardless of how short the labels are, so five periods render about 1390px wide inside an 856px figure.
It scrolls rather than shrinking, which is correct behaviour and is also the trap: the reader arrives with the rightmost period off-screen, and on a revision history that period is the current one and the whole point of the drawing.
Shortening the event text does not help. Draw it by hand instead, where you control the width and can make the break structural - `0240` puts the four older MCP revisions inside a `d-bound` and the current one outside it, which says more than a timeline could.

**A 360px check cannot be done by resizing, in this environment.**
`chrome-devtools-axi resize` clamps the window to a 500px minimum, so the narrowest reachable viewport is 500px. That is still below the 720px breakpoint, so the small-screen arm is exercised and body overflow is genuinely testable.
The part 500px cannot reach is text clipped at a hand-drawn figure's `viewBox` edge - and that check does not need a narrow viewport at all, because `getBBox` returns user units.
Sweep every `<text>` in every `svg.chart` and flag any whose box starts below 0 or ends past the `viewBox` width. It found two clipped labels in this module that no checker and no screenshot would have caught.

**A lesson linked from below the last module appears in the rail under the wrong heading.**
`gen_outline.py` slices the course map at each `.module-h` and runs the last slice to the end of the file, so an `href="lessons/..."` in a footer is collected as an extra lesson of the final module.
Link a lesson from the hero or from a card, never from below the last module. It renders, every link resolves, and `validate_site.py` stays green.

## Honesty notes

Two limits are load-bearing and each has a page that must carry it in a `.callout.warn`.

- **`0550`.** Agent-readiness and AI-reviewability are different properties: in the one open sample available, the most agent-ready repository scored worst on reviewer recall. That is the honest limit that keeps the scorecard from over-claiming, and it is the strongest argument for the scorecard being a teaching widget rather than a verdict.
- **`0620`.** The recall ceiling in the only open head-to-head data is 61.7%, and the precision spread is four times wider than the recall spread. A vendor precision headline is not a contradiction of that; it is a different question. `0610` and `0620` are the adjacent pair that makes the difference legible.

Lesson `0000` carries the third, which is about the course rather than about a claim: the protocol under module 2 removed its own initialize handshake inside this course's lifetime, which is why nothing here is dated.

## Open threads

- The five interactive figure shapes have landed in the shared design system, ahead of any writer. Lesson `0000` deliberately depends on none of them, which is why the scaffold could land first; every module page after it should reach for one where it fits. `BUILDER-SPEC.md` carries the markup rule that bites first.
- Whether this course should join `EXTENDED_BAR_COURSES` in `check_pages.py` - one practice problem and one hand-drawn `svg.chart` per page. Not at the start; joining is the last step of a retrofit. Lesson `0000` already clears both, so it is worth re-asking once a module is written.
- Whether the "in the field" pages are worth reading under the public-material-only rule. `MISSION.md` says revisit after module 4, which is the first real test.
- The `go-course` / `gcp-course` hue collision at absolute 200, found while choosing this course's hue and recorded in `learning-records/0001-choosing-the-hue.md`. Not this course's to repair.
