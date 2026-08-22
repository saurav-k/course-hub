# Notes

How this course teaches, and the gotchas found while building it.
`MISSION.md` says what the course is. `BUILDER-SPEC.md` says what a page must contain. This file is the craft between them.

## The voice

The reader ships distributed systems for a living and has not done an integral since 2009.
Both halves of that sentence are load-bearing.

- **Never explain what a variable is.** They program. They understand naming, scope and composition better than most mathematicians.
- **Always explain what a symbol means.** &Sigma;, &Pi;, &part;, &nabla; and &sim; are not notation they carry any more.
- **Reach for the systems analogy when it is genuinely the same shape**, and never when it is merely nearby. The gradient is not "like a load balancer". The dot product genuinely is the same operation a single neuron performs, and saying so lands.
- Full prose, complete sentences, plain dash, never an em dash.

## The three sentences that shape a page

Written in this order while planning, before any HTML:

1. **What is the one idea?** If it takes two sentences, it is two pages.
2. **What picture makes it obvious?** If there isn't one, the idea is not understood well enough to teach yet.
3. **What can the reader now compute that they could not before?** That is the practice problem.

## What the checker taught us, from the one maths course that came first

`statistical-foundations-ml-course` is a live sibling course and this table is not a complaint about it. It was the hub's first maths course and the teaching bar postdates it by a long way, so running today's checker over yesterday's pages says nothing about the author and a great deal about which bars are easy to miss. That makes it the cheapest available list of traps, and every row below is a trap this course walks into just as easily.

| The trap | What this course does about it |
|---|---|
| Quiz answers drifting to one index, arrived at one page at a time rather than in one decision. | The module owner assigns `data-answer` at integration and keeps the running count. `BUILDER-SPEC.md` section 7. |
| Opening a content page with prose, so the first figure arrives two or three sections in. | The orientation figure is the page's first figure, and it is that page's slice of the prerequisite graph. |
| Prose outgrowing the figures, past 400 words per figure. | The `svg.chart` floor. The missing figure is usually the picture some paragraph is describing in words. |
| A roadmap that promises more than anyone has planned. | Nothing goes in a `.roadmap` without a written brief in `briefs/` behind it. |
| A page promising a technique that arrives later, where "later" is never scheduled. | A forward promise names the module that keeps it, and that module's brief carries the promise as a beat. |

## Gotchas found while building the scaffold

- **A practice problem breaks the word ceiling unless the checker excludes it.** Measured: one 600-word practice section added to a clean page took it to 2,139 prose words against an 1,800 ceiling, and 535 words per figure against 400. `check_pages.py` now excludes `.practice` exactly as it excludes `.quiz`. If a page ever reports an impossible word count, check that the practice block is well formed - the exclusion is anchored on `<div class="practice">` and a typo in that opening tag silently turns the whole solution into prose.
- **A planned page cannot be a file.** `validate_site.py` requires every `lessons/*.html` to be a card in `index.html` and to appear in `outline.js`. So a page that is planned but unwritten has **no file at all**: its brief lives in `briefs/NNNN-slug.md`, which the deploy excludes, and the course map lists it in a `.roadmap` as plain text. Never link a brief from a page; the validator fails the pull request for a local `.md` link.
- **The number is claimed when the brief is written, not when the page is.** `briefs/` is the register of who owns which number. Two crews writing `0034` is the one merge conflict this layout cannot absorb, because the number is in the file name, the eyebrow, the footer and the pager.
- **Regenerating a dataset must leave `git status` clean.** Both generators are seeded and write byte-identical output. If a regeneration produces a diff, the generator has picked up an unseeded source of randomness and that is a bug, not a new dataset.
- **`hub.js` opens every `<details>` for printing.** A reader who prints a page gets the solutions. That is deliberate and it matches `.q-fb`, which the print block also forces open, but it means a printed page is a worked answer key rather than a problem sheet.

## The order things get written

1. The brief in `briefs/`, complete enough that the writer needs no further briefing.
2. The dataset, if the lesson needs one that does not exist.
3. The program in `code/`, run and its output captured.
4. The figures, because the page is built around them.
5. The prose, which is what is left once the figures carry what they carry.
6. The quizzes and the practice problem.
7. The card in `index.html`, then `gen_outline.py`, then both checkers, then the browser in both render states.

Step 5 coming fifth is the whole method. Prose written first always says what a figure would have said better, and then nobody deletes it.
