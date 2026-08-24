# AGENTS.md - How Language Models Happened

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

The hub's missing spine: the story of how language models happened, from the 1950s to 2026, written for a beginner who has heard of all of it and can explain none of it.
It is also the hub's only **routed** course: one pool of 57 pages read along four named routes, declared in `routes.js`.
[`routes/README.md`](routes/README.md) is the reference for that mechanism; read it before adding a lesson, a route, or any file under `lessons/`.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - why the course exists, what it owns versus `llm-papers-course`, and why it has four routes. Canonical.
2. [`NOTES.md`](NOTES.md) - the voice, the four-beat cadence every lesson follows, how to pay the self-containment tax, and the gotchas.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the full contract, including the two rules that stop this course re-converging with the papers course.
4. [`RESOURCES.md`](RESOURCES.md) - the sources behind every era. Add anything new there before citing it.
5. [`PLOT.md`](PLOT.md) - what "reading order" means for a routed course, and what is planned but unwritten.
6. Two neighbouring lessons, plus [`routes/README.md`](routes/README.md).

## The rules that bite hardest here

- **Numbers are identity; routes are order.** A lesson that belongs chronologically in the middle still takes the next free number at the end. Never renumber, never rename.
- **No runnable code and no derivation in this course.** At most one intuition-level formula per lesson, in prose. When a lesson wants to derive something, it links to `llm-papers-course` instead.
- **Every lesson names its own starting point** and links what it refers back to. There is no "the previous lesson" here: two readers reach the same lesson from different neighbours, depending on route.
- **Mermaid is a `div`, never a `pre`; line breaks are `&lt;br/&gt;`; semicolons in labels break diagrams.** This course carries the longest written record of those failures; see the gotchas section of `NOTES.md` before drawing anything.
- **Never hand-write a `?route=` link between lessons.** Write the plain filename; `outline.js` adds the parameter. A hand-written query pins the reader to a route they did not choose.

## Out of scope here

Mechanism, maths, and code (they live next door), tutorials, prediction, benchmark leaderboards, and any renaming or renumbering.
`MISSION.md` owns the list and the reasons.
