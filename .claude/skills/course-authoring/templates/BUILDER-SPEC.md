# Builder spec - the delta for COURSE NAME

The house standard is `.claude/skills/course-authoring/`.
It carries the page contracts, the widget vocabulary, the teaching bar, and the verification gate, and it governs this course as it governs every other.

This file carries **only what is true of this course and not of the hub**.
Keep it short. Every rule here is a rule an author must hold in addition to the standard, so a rule that merely restates the standard costs attention and buys nothing.

Where this file and the skill disagree, the skill wins, and the disagreement is a bug to raise in the pull request.

## The gold page

`lessons/NNNN-slug.html`. Read it in full before writing.
It is the page every other page in this course is matched against, so a divergence from it is a decision to defend, not an accident to leave in.

## What this course does differently

The genuine deltas. Some examples of what belongs here, from courses that have them:

- A required section the house standard does not ask for, such as a per-topic scale ladder or a field drill.
- A rule about numbers, such as quoting a source deck's figure exactly rather than re-deriving it.
- A rule about what may be assumed, such as never re-teaching a concept the learner has twelve years of.
- A required section shape per topic, where a chapter indexes many topics rather than developing one.
- A fixed meaning for one of the shared chart colours, where this course's figures use `m-alarm` for one thing throughout.
- A rule that only holds because this course ships an `assets/course-extras.css`, naming what is in it and why it could not go in `assets/hub.css`.

Delete the ones that do not apply. An empty deltas list is a legitimate outcome and a good sign.

## The lesson map

**The map lives in `index.html`, and only there.**

Do not restate it here.
Every one of the seven pre-existing courses kept a second copy of its map in this file, and every one of those copies went out of date.
The map in `index.html` is also what `scripts/gen_outline.py` reads to build the sidebar, so it is the copy that cannot silently drift.
`index.html` is the deployed artefact and the validator checks it, so it is the one that cannot silently drift.

## Cross-linking

Which sibling courses this one links, and the rule for when a link is worth making.
Verify an anchor exists in the target file before you commit it: the validator strips fragments and will not catch a dead one.
