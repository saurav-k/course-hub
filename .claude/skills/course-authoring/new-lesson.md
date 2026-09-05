# Writing one page

One page, start to finish.
"Page" means whichever unit the course uses: a lesson, a chapter, or a part of a lecture.
[`references/page-contracts.md`](references/page-contracts.md) says which is which and what each one owes.

## 1. Orient

Read, in this order, and do not skip to writing when the topic feels familiar:

1. `<course>/MISSION.md`. The scope argument was already had; this file is its outcome.
2. `<course>/NOTES.md`. Cadence, learner profile, and the gotchas the last author paid for.
3. `<course>/BUILDER-SPEC.md`. Only the delta from this skill. Short by design.
4. `<course>/RESOURCES.md`. What this course already trusts, and its `## Gaps`.
5. The two pages either side of your slot, in full. Voice is caught, not specified.

Then settle three things before drafting:

- **The one idea.** State it in a single sentence with a verb in it. If it takes two sentences joined by "and", it is two pages.
- **The rung.** Which level does this page sit at, and what does it therefore assume? See the ladder in [`references/pedagogy.md`](references/pedagogy.md).
- **The sources.** Fetch and read them now. A citation added at the end is a citation nobody read.

## 2. Draft

Copy `templates/lesson.html.tmpl` and work top to bottom.
Order matters: the template's order is the teaching order.

**The contract before the idea.** Under `.paper-meta`, the `.card.outcomes` says in one to three actions what the reader can do after this page and links the pages they need first. Write it before the body, because a page whose outcome you cannot state in an action is a page whose idea you have not settled. The markup is in [`references/widgets.md`](references/widgets.md), "The learning contract".

**The big picture first.** Before the first body section, draw the orientation figure: what larger thing this idea is part of, what came before it, what it enables. Cover the rest of the page with your hand; the opening sentence and that figure alone must say what the page is about and why it exists. The bar is in [`references/pedagogy.md`](references/pedagogy.md) and the markup is in [`references/widgets.md`](references/widgets.md).

**Mental model, then mechanism, then trade-off.** The reader gets a picture they can hold before they get a thing they must follow, and they never get a technique without its cost. A section that introduces a technique and lists only benefits is unfinished.

**Two lines above every drawing, and neither does the other's job.** `.fig-cap` names the subject in two to five words and never argues; `.fig-claim` says in one sentence what the drawing proves and never describes the picture. Write them before you draw, not after: if you cannot say what the figure proves, you do not yet know what to draw. The markup is in [`references/widgets.md`](references/widgets.md), "What a figure is".

**Diagram before the paragraph it illustrates, not after.** A diagram that appears after the explanation is a summary; a diagram that appears before it is a scaffold, and scaffolds are what lower cognitive load.

**When a paragraph and a figure say the same thing, the paragraph goes.** Not both. A paragraph that walks the reader through a diagram node by node is the diagram typed out, and it is the first thing to cut when the page is over the word ceiling. 1,800 prose words is the ceiling and 400 words per figure is the density bar; both are counted by `check_pages.py`.

**One new named thing per paragraph.** Name it in plain words on first use on this page, not once per course. Repetition across pages is cheap; a reader stalling on an unexplained symbol is not.

**Every formula reads aloud.** Put it in `.math` with a `.gloss` that names every symbol in words. This rule is currently honoured on all 199 formulas in the hub, which is exactly why it is worth keeping.

**Work the steps a source compresses.** Where the source writes one line of algebra, write the three lines behind it in an `<ol class="worked">`. The reader must never have to reconstruct a step you skipped.

**Say where the ground is soft.** Where a source is loose, an assumption is doing real work, or the evidence is thinner than the claim, put it in a `.callout.warn` rather than smoothing it over. An honest limit teaches more than a seamless explanation that hides one. One per page: a page with three warnings has no warning.

**A problem after the quizzes, and a recap after the problem.** The `.practice` block gives the reader something to do with the idea at numbers the page has not shown, with a hint, a worked solution behind a disclosure and a sanity line. The `.card.recap` then says in two to four points what they can now say unprompted and links the next page with the reason to go there. Neither point in the recap repeats a bullet from the one-minute version: that was written before the idea and this is written after it.

Widget markup comes from [`references/widgets.md`](references/widgets.md), copied exactly.
Counts and kinds come from [`references/pedagogy.md`](references/pedagogy.md).

**Three things about a diagram are worth holding while you draft, because none of them reach the console.**
A Mermaid diagram is a `<div class="mermaid">` and never a `<pre>`; a line break in a label is `&lt;br/&gt;` and never a literal `<br/>`; and a semicolon inside a label is a statement separator.
The mechanism behind all three is in [`references/widgets.md`](references/widgets.md), and the reason you have to look at the page in both render states to catch them is in [`references/verify.md`](references/verify.md).

## 3. Register

A page nobody can reach is not published, and the validator will say so.

1. Add the lesson card to `<course>/index.html`, in its module, with its rung pill and reading-time pill, and correct that module's `.mcount`. The validator fails the pull request on an unregistered lesson.
2. Regenerate the outline: `python3 scripts/gen_outline.py <course>`, and commit `<course>/outline.js`. It is what the sidebar rail reads, and the validator fails the pull request when it and the lessons on disk disagree. A routed course has no generator: edit its `routes.js` by hand instead, following `llm-evolution-course/routes/README.md`.
3. Set the `.pager` on this page to its real neighbours, and fix the neighbours' pagers to point back at it. A new page inserted at the end changes the previous last page's "next", and its `.next-step` in the recap. The neighbours are the ones the course map gives the page: the fixed chapter bar is built from the map, and `check_pages.py` warns when a pager names anyone else. On a routed course the pager carries `data-pager-route` and the validator checks it against the owning route, so the neighbours are the route's, not the file order's.
4. Add every term you introduced to `<course>/reference/glossary.html`. The validator does not check this and never will, so it is on you.
5. Add every source you cited to `<course>/RESOURCES.md`. A claim you could not source goes in its `## Gaps`, not into the page.
6. Correct the course's page count on the **hub** landing page. Its card carries a count in `.ln`, like `Course &middot; 38 lessons`, and the subject section above it carries a `.mcount`. Nothing checks either, and a card claiming 38 beside a folder holding 39 is the cheapest kind of wrong.

## 4. Verify

Run the gate in [`references/verify.md`](references/verify.md).

It is not a formality.
Half of what this skill asks for is invisible to `scripts/validate_site.py`, which is why the six courses that predate this skill diverged while passing every check.
