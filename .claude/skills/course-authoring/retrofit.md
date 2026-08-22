# Bringing an existing course to the standard

Seven courses were published before this skill existed.
This file is how one of them is brought up, without breaking a URL and without burying the change in noise.

Run the baseline first, and work from what it says rather than from what a page looks like:

```bash
python3 .claude/skills/course-authoring/scripts/check_pages.py <course>
```

## What must never change

A published URL is a promise, and the promise reaches one level deeper than most authors expect.

- **A lesson filename.** Never renumbered, never renamed, even when the teaching order would prefer it. Teaching order lives in the module grouping in `index.html`, and it is free to disagree with file order.
- **An `<h3 id="...">` inside a chapter.** The glossary links to it and sibling chapters link to it, and `validate_site.py` strips fragments before checking a link, so a renamed anchor breaks silently. Add anchors freely; change them never.
- **A course folder name.** It is the first path segment of every URL that course owns, and it is also the key `hub.js` reads out of the URL to decide the course's accent hue. Renaming it changes the site's colours as well as its links.

Everything else is fair game.
The `.md` files are excluded from the S3 sync and were never public at all, so `BUILDER-SPEC.md` can be rewritten freely.

## What is already done, and is not a retrofit item

The design system was de-forked before this skill shipped.
Every page in the hub now links `assets/hub.css` and loads `assets/hub.js` plus its course `outline.js`, and the six byte-identical copies of the old `course.css` / `course.js` pair are gone.
Do not go looking for them, and do not treat a course's `assets/course-extras.css` as a fork: the three that remain carry rules genuinely unique to their course and are layered after the hub sheet on purpose.

What that leaves is content work, which is the part no migration could do.

## One course per pull request, one concern per commit

A retrofit touches every page in a course, so it is exactly the change that buries a real edit in reformatting.
Keep the mechanical passes separate from the judgement passes, so a reviewer can read the mechanical ones quickly and spend their attention on the ones that need it.

Mechanical, reviewable at a glance:

1. **Fix whatever `check_pages.py` reports as FAIL.** These are small and unambiguous, and the Mermaid ones are the highest-value: a `<pre class="mermaid">`, a literal `<br/>` in a label, or a semicolon in one is a figure that is broken or about to be, and no reader has reported it because nothing reaches the console.
2. **Retire the inline styles.** Every repeated inline style is a class the design system is missing; add the class to `assets/hub.css`, then delete the attribute.
3. **Delete the dead `<button class="theme-btn">`.** `hub.js` removes it at mount and replaces it with the real appearance control, so it is markup that has done nothing since the migration.
4. **Add the rung pill and the reading-time pill** to every lesson `.paper-meta` and every card in `index.html`, then re-run `scripts/gen_outline.py <course>` and commit the outline.
5. **Shrink `BUILDER-SPEC.md` to its delta.** Delete the lesson map from it: `index.html` already carries one, the validator checks that one, and the two copies have already disagreed.

Judgement, one page per commit:

6. **Raise the diagrams to the floor.** A page at one flowchart needs a second kind, chosen by what the reader is confused about rather than by what is quick to draw. This is authoring, not formatting, so treat each page as a small `new-lesson.md` job.
7. **Draw the quantitative claims.** A course that states magnitudes and draws none needs hand-authored `svg.chart` figures. Usually one or two pages carry most of the numbers; start there.
8. **Rebalance the answer indices** across the course, not within a page.

## The ordering

Take the courses in this order, which is worst-gap-per-page first rather than largest first:

1. **The course whose shape other courses copied.** Its shape propagates, so fixing it stops the drift at the source.
2. **The smallest courses**, because a whole course brought to the standard is a worked example the later ones can be matched against, and a small one gets there in an afternoon.
3. **The course missing its `MISSION.md`, `NOTES.md`, or `RESOURCES.md`.** Those files cannot be reconstructed from the pages; they have to be written from what the author remembers, and that memory has a half-life. `llm-inference-course` is the one with the gap.
4. **The course that is already closest to the standard**, which needs only the mechanical passes.
5. **The largest course, last.** Its backlog is the biggest but it is almost entirely mechanical, and by then the mechanical passes are practised.

The routed course is its own case and should not be batched with the others: every page in it owes a committed pager naming its owning route and a `data-zone`/`data-asof` status block, and `validate_site.py` checks both.
Read `llm-evolution-course/routes/README.md` before touching a page there.

Re-run the baseline after each course.
A course is retrofitted when `check_pages.py` reports zero failures for it and every remaining warning has a reason written in the pull request.
