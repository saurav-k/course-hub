# Builder spec - the delta for Coding Harness Engineering

The house standard is `.claude/skills/course-authoring/`.
It carries the page contracts, the widget vocabulary, the teaching bar, and the verification gate, and it governs this course as it governs every other.

This file carries **only what is true of this course and not of the hub**.

## The gold page

`lessons/0000-what-is-a-coding-harness.html`. Read it in full before writing.
Every later page in this course is matched against it: its diagram density, its two-harness contrast pattern, and its evidence discipline are the course's voice.

## What this course does differently

- **Lesson numbers step in tens.** Files are `0000`, `0010`, `0020` ... `0270`, mirroring the epic's issue numbers (#123/#124 -> 0000, #125 -> 0010, ... #151 -> 0270). Inserting a page later costs nothing; never renumber.
- **The deep-dive skeleton is fixed.** Pages 0120 through 0260 run, in order: Identity - The loop - Context assembly - Trust posture - Extension surface - Model behavior - The distinctive mechanism. Same `<h2>` titles each time so fifteen pages stay side-by-side comparable. Mechanism modules (0010-0110) are exempt.
- **Two named harnesses per mechanism.** Any mechanism page explains each layer through at least two cast members answering differently, named with their real identifiers. One example alone does not close a section.
- **Evidence provenance on every deep dive.** The `.paper-meta` line names whether that harness was read from source (with the pinned commit in `RESOURCES.md`) or covered from official documentation because it is closed. Closed-source pages carry one `.callout.warn` stating the limit.
- **Diagram-led is enforced locally:** aim for four to six figures per content page where the house floor is three. A contrast another course writes as a paragraph of prose is drawn here as a two-path figure when a drawing exists for it.

## The lesson map

**The map lives in `index.html`, and only there.**

Do not restate it here.
`scripts/gen_outline.py` reads it to build the sidebar, `validate_site.py` fails the pull request when the outline and the lessons on disk disagree, and every pre-existing course that kept a second copy of its map watched that copy rot.

## Cross-linking

Mechanism pages forward-reference their deep dive by name and link (`the Claude Code deep dive`), and deep dives back-reference the mechanism pages that introduced their vocabulary.
Sibling-course links go to [`agent-engineering-course`](../agent-engineering-course/index.html) only where the boundary statement in `MISSION.md` says they touch - deployment questions belong there, internals here.
Verify an anchor exists before you commit a fragment link; the validator strips fragments and will not catch a dead one.
