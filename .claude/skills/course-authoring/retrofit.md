# Re-evaluating and enhancing an existing course

The bar a course is measured against, in one sentence:
**a stranger with the stated prerequisites opens a page, understands where it sits, learns one idea, checks their understanding, practises it, and knows where to go next; every page looks like the same product; nothing is broken in either render state; and the learner would pay for the course.**

This file is the procedure that takes a published course to that bar without breaking a URL and without burying the change in noise.
It is one pull request per course, and it produces two artefacts: an enhanced course and a course report that a second worker on a second course can be compared against.
Ten workers on ten courses produce comparable audits only because they fill the same rubric, so the rubric is not a suggestion.

## What must never change

A published URL is a promise, and the promise reaches one level deeper than most authors expect.

- **A lesson filename.** Never renumbered, never renamed, even when the teaching order would prefer it. Teaching order lives in the module grouping in `index.html`.
- **An `<h3 id="...">` inside a chapter.** The glossary and sibling chapters link to it, and `validate_site.py` strips fragments before checking a link, so a renamed anchor breaks silently. Add anchors freely; change them never.
- **A course folder name.** It is the first path segment of every URL the course owns and the key `hub.js` reads to pick the course's accent.

Everything else is fair game.
The `.md` files were never public, so `BUILDER-SPEC.md` can be rewritten freely.
The design system was de-forked before this skill shipped; a course's `assets/course-extras.css`, where one remains, is not a fork and not a retrofit item.

## The procedure

Five steps, in this order, and the order is the point: the audit decides the work, the priorities decide the order of the work, and the report is what the next worker reads.

### 1. Audit every page

Run the three machines over the whole course before you read a single page as a reader.

```bash
python3 .claude/skills/course-authoring/scripts/check_pages.py <course>
python3 .claude/skills/course-authoring/scripts/check_pages.py <course> --links
python3 scripts/render_sweep.py <course> --narrow
```

The first is the house standard read off the markup; the second fetches every external link once; the third renders every page in both render states and at 360px.
Their output is the machine half of the rubric below, and every FAIL and WARN they print is a row already filled in.

Then open every page in a browser, served rather than from disk, and fill the judgement half of the rubric for each one.
Read as the learner `MISSION.md` names, not as the author.
The whole of what to look at is [`references/verify.md`](references/verify.md), layers two and three; the rubric names the rows a machine cannot fill.

Keep the filled rubrics.
They are the audit, and the pull request carries their totals.

### 2. Fix in priority order

Four priorities, worked to completion in this order across the whole course before the next one starts, because a course with every page half-fixed is worse to review and worse to read than a course fixed in layers.

1. **Broken.** Everything `render_sweep.py` reports, every FAIL from `check_pages.py`, every dead link, every quiz whose `data-answer` is wrong when you click it, every figure that contradicts itself. A page with one of these is not a page a learner pays for, whatever else it does well.
2. **Missing structure.** The rows of the rubric that are absent rather than weak: no learning contract, no orientation figure, no practice problem, no recap, no rung word on the pill, a pager that disagrees with the map, an h1 that is a name and not a claim. Add the block from [`references/widgets.md`](references/widgets.md), copied exactly.
3. **Reading load.** The word ceilings, the words-per-figure ceiling, paragraphs over 120 words, a formula before its picture or before a worked instance, a symbol used before it is named on this page, a term the glossary defines that the page does not link. Start with the paragraph a figure already says; a page still over the ceiling after that is two pages, and splitting is a map change with new numbers at the end.
4. **Consistency.** The eyebrow shape, the caption pair on every figure, the quiz shape and the answer-index spread across the course, a single `.callout.warn`, the topbar on one row at 1280px and at 720px, inline styles retired into classes, the legacy `.theme-btn` deleted.

One concern per commit, so a reviewer can read the mechanical commits at a glance and spend their attention on the judgement ones.
The mechanical passes - FAILs, inline styles, the dead button, the pills, the `BUILDER-SPEC.md` shrunk to its delta - come first in the history; the page-by-page authoring comes after, one page per commit.

Within priority 2, the orientation figure is the largest single item on any course that predates the bar and the one that changes how the course reads.
Draw it from the course map: the module the page sits in, the page before it, and what it unlocks.
The learning contract and the recap are the next largest, and both are written from the page rather than from the template: an outcome is what this page's reader can now be watched doing, and a recap point is something they can now say unprompted.

### 3. Verify in both render states

Every page you touched, and then the whole course once, exactly as [`references/verify.md`](references/verify.md) says.

```bash
python3 scripts/gen_outline.py <course>
python3 scripts/validate_site.py
python3 scripts/check_pages_gate.py
python3 .claude/skills/course-authoring/scripts/check_pages.py <course>
python3 scripts/render_sweep.py <course> --narrow
```

Then the browser, for the things no script sees: every figure read for what its roles claim, every quiz answered, every interactive figure operated by keyboard and once with the script blocked, print preview on one page carrying a diagram.
The pull request says in so many words that you looked at the diagrams in both render states.

### 4. Refresh the baseline

`scripts/check_pages_gate.py` gates on the difference from `scripts/check-pages-baseline.txt`, and it fails when a recorded failure no longer happens.
Fixing a course therefore turns the gate red on purpose, and the last commit of the pull request takes the fixed lines out:

```bash
python3 scripts/check_pages_gate.py --write
```

Refresh it as the last commit and expect to redo it after a rebase: ten course pull requests each shorten the same file, and the file is sorted by path so two courses' lines are adjacent.
Never add a line to it by hand and never leave a line in it that your course no longer produces.

### 5. Write the course report

The format is below.
It goes in the pull request body, in full, and a copy goes in `<course>/learning-records/NNNN-retrofit-report.md` so the next worker on this course starts from it.

## The per-page rubric

Fill one per page.
`M` rows are read off the three scripts and are not a judgement; `J` rows are a reading of the page in a browser.
Score each row `1` when it passes, `0` when it does not, and total the row count out of 30.
A page ships at 30; a page below 30 ships only when every missed row has a reason in the report, and "the neighbours miss it too" is not a reason.

```markdown
### <course>/lessons/NNNN-slug.html

| # | Row | M/J | Score | Note |
|---|---|---|---|---|
| **Broken** | | | | |
| 1 | render_sweep: 0 error boxes and 0 blank renders on first paint and after the mode toggle | M | | |
| 2 | render_sweep: no label text changed on repaint, body does not scroll sideways at 1280 or 360 | M | | |
| 3 | check_pages: 0 FAIL lines for this page | M | | |
| 4 | check_pages --links: 0 dead links, each dead one retried once; a 403, 406 or 429 is a robot block until a browser has opened it | M+J | | |
| 5 | every quiz answered by hand: the right option goes green, every wrong one reads its feedback | J | | |
| 6 | every hand-drawn figure read: no role contradicts another, no label cut at the frame edge at 360 or full width | J | | |
| **Structure** | | | | |
| 7 | .eyebrow states module, module name and position; h1 is a claim with a verb, not the card's name | M+J | | |
| 8 | .paper-meta: rung pill first with the rung word, then the reading-time pill | M | | |
| 9 | .card.outcomes under .paper-meta: 1 to 3 outcomes, each an action, and a .prereq line with links or "nothing" | M+J | | |
| 10 | .card.tldr: 3 to 5 claims, each bolding its key term | M+J | | |
| 11 | orientation figure: the page's first figure, before the first body section, drawing before / this / enables | M+J | | |
| 12 | a worked instance in an ol.worked before or beside the first general statement; first .math after the first figure | M | | |
| 13 | 3 or more figures of 2 or more kinds, each with .fig-cap, .fig-claim and a figcaption with a bolded takeaway | M | | |
| 14 | 2 or more quizzes, 4 options each within 12 characters, a .q-fb that explains every wrong option | M+J | | |
| 15 | 1 or more .practice under an h2 Practice, each with details.solution ending in a .p-check | M | | |
| 16 | .card.recap after the practice: 2 to 4 points, none a copy of a tldr bullet, and a .next-step link with its reason | M+J | | |
| 17 | .teacher-note, then Primary source to go deeper with a link opened this session | M+J | | |
| 18 | .pager points at the neighbours the course map gives the page; the last page points at the map | M | | |
| **Reading load** | | | | |
| 19 | 1,800 prose words or fewer, 400 or fewer per figure | M | | |
| 20 | no paragraph over 120 words | M | | |
| 21 | every new named thing defined in plain words on first use on this page; every .math has a .gloss | J+M | | |
| 22 | the course glossary is linked from the page and carries every term the page introduces | M+J | | |
| 23 | every technique carries its cost in the same section; at most one .callout.warn | J+M | | |
| **Consistency** | | | | |
| 24 | every technical claim links a source you opened this session; derived numbers show their arithmetic | J | | |
| 25 | every colour in a hand-drawn figure is a class or a var(--token); no inline style attribute in the page markup | M | | |
| 26 | the topbar sits on one row at 1280px and at 720px; nothing wraps inside a control | J | | |
| 27 | both modes and a second palette looked at: every figure legible, nothing invisible on the other ground | J | | |
| 28 | every interactive figure operated by keyboard, and read once with the script blocked | J | | |
| 29 | print preview: diagrams in ink on paper, solutions open, no raw graph source | J | | |
| 30 | the page reads as one idea, in the voice of its neighbours, and a stranger could say what it is about from the h1 and the orientation figure alone | J | | |
| | **Total** | | **/30** | |
```

Rows 7 to 18 are the page contract in [`references/page-contracts.md`](references/page-contracts.md), in order.
Rows 19 to 23 are [`references/pedagogy.md`](references/pedagogy.md), "Fewer words" and "Cognitive load".
Rows 1 to 6 and 24 to 30 are [`references/verify.md`](references/verify.md).
When a row and one of those files disagree, the file wins and the row is a bug to raise in the pull request.

## The course report

One per course, in the pull request body and in `learning-records/`.

```markdown
# Retrofit report: <course>

Worker: <agent or person>. Branch: <branch>. Date: YYYY-MM-DD.
Pages audited: N lessons, M reference sheets, 1 course map.

## Before and after

| Measure | Before | After |
|---|---|---|
| check_pages FAIL lines for this course | | |
| check_pages WARN lines for this course | | |
| render_sweep failures (1280, both states) | | |
| render_sweep failures (--narrow) | | |
| dead external links (--links) | | |
| pages scoring 30/30 on the rubric | | |
| lowest page score, and which page | | |
| pages with no orientation figure | | |
| pages with no .card.outcomes / no .card.recap | | |
| pages with no practice problem | | |
| pages over 1,800 prose words | | |
| rung pills not reading the rung word | | |
| pagers disagreeing with the course map | | |
| lesson cards on the map with no reading-time pill | | |

## What the course map now tells a learner

The hero's claim, what the learner will be able to do, the total time in hours, what one page costs, where to start, and which reference sheets exist. One line each.

## Warnings that stand, and why

One line per remaining check_pages WARN, grouped by kind: the count, the reason it stands, and what would clear it.

## Verified

- Looked at every diagram on every touched page in both render states, by hand, on <palette> and <palette>.
- render_sweep.py: N pages, 0 failures, with --narrow.
- Every quiz on every touched page answered; every interactive figure operated by keyboard and read with script blocked.
- Print preview on <page>.
- Baseline refreshed in the last commit: N lines removed, 0 added.

## Left for the next worker

What was out of reach in this pull request and why, one line each, with the page it belongs to.
```

## The ordering across courses

When one worker holds several courses, take them worst-gap-per-page first rather than largest first:

1. The course whose shape other courses copied, because fixing it stops the drift at the source.
2. The smallest courses, because a whole course at the bar is the worked example the rest are matched against.
3. The course missing its `MISSION.md`, `NOTES.md` or `RESOURCES.md`, because those cannot be reconstructed from the pages and memory has a half-life. `llm-inference-course` is the one with the gap.
4. The course already closest to the bar, which needs only the mechanical passes.
5. The largest course, last, when the passes are practised.

The routed course is its own case: every page in `llm-evolution-course` owes a committed pager naming its owning route and a `data-zone`/`data-asof` status block, `validate_site.py` checks both, and `check_pages.py` skips the pager-against-map row for it because the map is a route.
Read `llm-evolution-course/routes/README.md` before touching a page there.

A course is at the bar when `check_pages.py` reports zero failures for it, every remaining warning has its line in the report, `render_sweep.py --narrow` reports zero, and every page's rubric is filled.
Joining `EXTENDED_BAR_COURSES` in `check_pages.py`, which turns the practice and chart floors from WARN to FAIL for the course, is the last commit before the baseline refresh.
