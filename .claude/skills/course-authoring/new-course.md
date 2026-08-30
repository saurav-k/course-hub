# Building a new course

A course is scaffolded once and authored many times.
This file covers the once.
When the scaffold stands and the first lesson is the next thing to write, switch to [`new-lesson.md`](new-lesson.md).

Work the four steps in order.
Step 1 produces answers, step 2 turns them into a shape, step 3 writes files, step 4 proves the shape holds before any real content goes into it.

## 1. Interview

Do not write a file until every question below has an answer written down.
A course whose audience was never pinned down teaches three different people badly.

Ask the questions in one message as a numbered list, offer your own answer to each as a starting point, and let the human correct rather than compose.
Where an answer is genuinely derivable from the existing hub, derive it and say you did.

**Who and where they start.**

1. Who is the learner, in one sentence naming their job and their years in it?
2. What do they already know that this course may assume without teaching?
3. What is the specific cold spot: the thing they once knew, never knew, or know as folklore?

**What done means.**

4. What can the learner do at the end that they cannot do now? Five capabilities, each phrased as an action, not a topic.
5. What would make this course a failure even if every page were accurate?

**Shape.**

6. How many pages, and what is a page? A lesson, a chapter that indexes many topics, or a lecture split into parts. The three shapes are described in [`references/page-contracts.md`](references/page-contracts.md); pick one and stay in it.
6b. Is there genuinely more than one order in which this course should be read? If yes, and only if yes, it is a **routed** course: one pool of lessons declared once in a `routes.js` manifest and travelled several ways. `llm-evolution-course` is the only one, `llm-evolution-course/routes/README.md` is the reference, and the cost is real: `gen_outline.py` refuses to run against a routed course, every lesson owes a committed pager naming its owning route, and `validate_site.py` checks all of it. Answer no unless the several orders were the reason for the course.
7. What is the level ladder, rung by rung? See the level ladder in [`references/pedagogy.md`](references/pedagogy.md). A course with no ladder is a reference, and a reference should say so rather than pretend to be a progression.
8. How long is one page in prose words? This sets the grain. 900 to 1,400 is one sitting and 1,800 is the ceiling; a page that wants 4,000 is three pages wearing one title. The count excludes the figures, the code and the quizzes, because prose is what the reader has to hold. See [`references/pedagogy.md`](references/pedagogy.md).

**Order.**

9. Walk the course in reading order: what comes first, what follows what, and why that order and no other?
   Which sessions sit directly after which lectures, so a tutorial or lab lands beside the material it supports rather than in a list at the bottom of the map?
   Name everything planned but unwritten and reserve its position now.
   A position reserved costs nothing; a position taken by accident is a renumbering.

**Boundaries.**

10. What is out of scope, and for each, which neighbour owns it? "Out of scope" with nowhere to send the reader is an abandonment.
11. Which existing courses in this hub does it touch, and at which pages? Read their `MISSION.md` files before answering.
12. Does anything here overlap an existing course enough that the honest answer is a chapter there rather than a course here?

**Sources.**

13. What is the canon: the small set of primary sources this course will keep returning to? A course with no canon cites whatever a search returns.
14. Is there a spine document, deck, or syllabus this course follows? If yes, its numbers are the ceiling and its ordering is the default.

Write the answers into `MISSION.md` before anything else.
That file is the record of this interview, and every later authoring decision is settled by re-reading it.
The answer to question 9 becomes `PLOT.md` in step 3; it is the one answer that gets a file of its own.

## 2. Architecture

Turn the interview into a lesson map before writing a lesson.

Write the map as the course `index.html` directly, not as a list in a markdown file.
`index.html` is the deployed artefact, the validator checks it, and a second copy of the map in `BUILDER-SPEC.md` is the duplication that put the six existing specs out of step with their own courses.

The map states, for every page: its number, its slug, its title, its module, its level rung, and its reading time.
Pages that are planned but unwritten sit in a `.roadmap` list as plain text.
**A roadmap entry must never be a link**, because a link to a file that does not exist fails the validator.

Record the same map as reading order in `PLOT.md`: one row per position, with the unwritten ones marked reserved rather than left out.
The course map and the plot are two views of one order, and they have to agree; when they disagree, one of them is wrong and it gets fixed before anything new is added.

Check the map against the ladder before you accept it: read the titles in order and confirm each one only needs what came before it.
A page that needs a later page is a map bug, and it is far cheaper to fix here than after eight pages are written.

## 3. Scaffold

Copy from [`templates/`](templates/), then fill:

| File | Template | What it is |
|---|---|---|
| `<course>/AGENTS.md` | `AGENTS.md` | the course contract for agents: what the course is, what to read in which order, and the rules an agent violates first here |
| `<course>/CLAUDE.md` | `CLAUDE.md` | a symlink to `AGENTS.md`, exactly as at the repository root, so either filename resolves to the same contract |
| `<course>/MISSION.md` | `MISSION.md` | the interview answers; canonical, settles every later argument |
| `<course>/PLOT.md` | `PLOT.md` | the reading order: every position, written or reserved, and everything planned but unwritten |
| `<course>/NOTES.md` | `NOTES.md` | how this course teaches, and the gotchas found while authoring it |
| `<course>/RESOURCES.md` | `RESOURCES.md` | the canon, plus a `## Gaps` list of claims with no citable source |
| `<course>/BUILDER-SPEC.md` | `BUILDER-SPEC.md` | the course delta only: what differs from this skill |
| `<course>/index.html` | `course-index.html.tmpl` | the course map from step 2 |
| `<course>/lessons/` | | empty until step 4 |
| `<course>/reference/glossary.html` | `glossary.html.tmpl` | grows as terms are introduced |
| `<course>/learning-records/` | | notes on the authoring itself; never published |

Five of these are instruction files and a new course is never born without them: `AGENTS.md`, `CLAUDE.md`, `MISSION.md`, `PLOT.md`, `NOTES.md`.
Fill each one from this interview and from what the course actually is; a template with only the name swapped produces files nobody reads.
If your tooling flattened the `CLAUDE.md` symlink into a text file while copying, recreate it with `ln -s AGENTS.md CLAUDE.md`.

A course needs **no `assets/` folder at all**, and a new course may not have one.
It links `assets/hub.css` and `assets/hub.js` like every other page in the hub, and there is nothing else to link.
Three courses carry a grandfathered `assets/course-extras.css` from before the course contract; they stay because their pages link them, and no course gets a fourth.
A rule two courses would both want belongs in `assets/hub.css`, and so does a rule only one course wants: one owner is the whole point.
A course's identity is the seven tokens below, not a stylesheet.

Then three registrations, none of which the course can do for itself:

1. **Register the course.** Add one block to the course-contract section of `assets/hub.css`.
   Seven tokens are available, one of them required, and that is the entire author surface:

   ```css
   :root[data-course="<course>-course"] { --course-hue: 0; }
   ```

   Most courses stop there.
   A course that also wants its own heading voice, its own code face or its own eyebrow writes them into the same block:

   ```css
   :root[data-course="<course>-course"] {
     --course-hue: 0;
     --font-display: var(--serif);       /* a face in the registry, never a stack of your own */
     --font-mono: var(--mono);
     --eyebrow-family: var(--font-mono);
     --eyebrow-tracking: .18em;          /* 0em to .34em */
     --eyebrow-case: uppercase;          /* or none; uppercase only on about five words or fewer */
     --eyebrow-size: var(--fs-xs);       /* inside the --fs-xs band */
   }
   ```

   [`references/widgets.md`](references/widgets.md), "The course contract", is the reference: what each token constrains, what you may rely on, and what is forbidden.
   `python3 scripts/validate_site.py` fails the pull request on a hue with a unit, a token that is not one of the seven, a value out of range, a face that is not in the registry, and a hue another course already holds.

   **Choosing the hue is the one part no script can do for you.**
   `hub.js` reads the course folder out of the URL and writes it onto `<html>`, and `hub.css` rotates whichever palette the reader chose by that offset in OKLCH.
   Read the list as absolute hue and the 25-degree grid is already full: 0 to +200 in steps of 25, then +225 through +335 written as negatives.
   So a new course splits a gap rather than extending outwards, and which gap is decided by whose pages your reader actually holds open beside yours.
   `staff-ai-course/learning-records/0001-choosing-the-hue.md` carries the method and a measured comparison table for four shipped hues; compare a candidate against that table.
   A course with no line at all silently wears the plain palette accent, which is dull rather than broken.

   Check the candidate against every palette in both modes before you ship it: seven palettes times two modes is what "verified" means here.
   Looking is the check, and there is a cheaper one worth doing first, because hue rotation preserves lightness and chroma while the OKLCH gamut is not a cylinder: at some hues the rotated colour falls outside sRGB and the browser clips it, which quietly changes what the reader sees.
   Render the candidate against all twelve combinations, read the painted pixel back through a canvas, and compare its chroma with the unrotated accent's.
   The seven original hues lose between 0 and 8 percent of their chroma on average, and up to 55 percent in their worst cell, so a candidate inside that range is no worse than what is already published.

2. **Generate the outline.** `python3 scripts/gen_outline.py <course>` reads the map you wrote in step 2 and writes `<course>/outline.js`, which is what the sidebar rail renders from. Commit it. Re-run it after every change to `index.html`; `validate_site.py` fails the pull request when the outline and the lessons on disk disagree.

3. **Add the course card to the hub `index.html`,** inside the `<section class="module">` for its subject, using the card shape in [`references/page-contracts.md`](references/page-contracts.md), and correct that section's `.mcount`.

Do not fork `assets/hub.js` or `assets/hub.css`.
The hub carried six byte-identical copies of an earlier design system, one of which had a rendering fix the other five never received, and de-forking them is why there is one copy now.

## 4. Prove the scaffold

Write `lessons/0000-*.html` from `templates/lesson.html.tmpl` and take it all the way to done under [`references/verify.md`](references/verify.md) before writing a second page.

Lesson zero is load-bearing twice over.
It is the on-ramp the learner meets first, and it is the page every later lesson in this course is matched against.
A shortcut taken here is taken forty more times.

Then run the gate over the whole scaffold:

```bash
python3 scripts/gen_outline.py <course>
python3 scripts/validate_site.py
python3 .claude/skills/course-authoring/scripts/check_pages.py <course>
```

Both checkers green before the pull request, and the page itself opened in a browser in both render states.
