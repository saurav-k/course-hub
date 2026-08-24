# Plot - the reading order of COURSE NAME

This file records the true reading order of the course: where every lecture, chapter, tutorial, or lab session sits, and everything planned but unwritten.
Fill it from the interview answer about order and the course map written in step 2 of [`../new-course.md`](../new-course.md), not from a guess.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order, and a tutorial or lab session that follows a lecture sits after that lecture in the course map, never in a separate list at the bottom.**
When this file and the course `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The sequence

| # | Position | Status | Notes |
|---|---|---|---|
| 1 | FIRST POSITION | reserved | What it is, where it sits, why it is there. |

One row per lecture, chapter, tutorial session, or lab session, in reading order.
A routed course states here what "reading order" means for it, names its default route as the canonical one, and points at its route manifest rather than duplicating every row; see `llm-evolution-course/PLOT.md` for that shape.
Reference sheets and glossaries read alongside and are recorded as such; they are not positions in the sequence.

## Planned but unwritten

Everything the course intends but nobody has written: reserve the position now, with a status of `reserved` and one line on when the position was claimed and by what plan.
A position reserved costs nothing; a position taken by accident is a renumbering.

## Adding a session to this course

1. Read the course's authoring contract files first.
2. Take the next free lesson number. Never renumber anything.
3. Insert the new material at its true position in this file and in `index.html`, never appended to the bottom because it arrived last.
4. Re-run `python3 scripts/gen_outline.py COURSE-NAME`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py`, and open the changed pages in both themes before opening the pull request.
