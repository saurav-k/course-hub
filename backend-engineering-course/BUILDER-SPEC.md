# Builder spec - the delta for Backend Engineering

The house standard is `.claude/skills/course-authoring/`.
It carries the page contracts, the widget vocabulary, the teaching bar, and the verification gate,
and it governs this course as it governs every other.

This file carries **only what is true of this course and not of the hub**.
Keep it short. Every rule here is a rule an author must hold in addition to the standard, so a rule
that merely restates the standard costs attention and buys nothing.

Where this file and the skill disagree, the skill wins, and the disagreement is a bug to raise in the
pull request.

## The gold page

`lessons/0000-the-shape-of-a-request.html`. Read it in full before writing.
It is the page every other page in this course is matched against, so a divergence from it is a
decision to defend, not an accident to leave in.

## What this course does differently

- **This course is derived, never copied.** Prose and diagrams are re-authored from first principles
  from the canonical web sources the upstream field manual cites. Never transcribe the upstream text
  or lift its figures. The attribution contract is in `RESOURCES.md`.
- **A traced request is the through-line.** The orientation figure on a page shows where this
  mechanism sits in the single connected request→fleet route, so a reader can place any mechanism in a
  running system even before the later modules are written.
- **Two implementation voices.** Prefer Go and Python together where a page needs code, matching the
  upstream series; prefer whichever reads clearer when one implementation is enough.
- **Every mechanism is owned, never waved at.** A page that names a framework behaviour names the
  mechanism underneath; the framework is never the reason given.
- **Go and Python runtime behaviour claims carry sources** from `RESOURCES.md`, exactly as any other
  technical claim would.

## The lesson map

**The map lives in `index.html`, and only there.**

Do not restate it here.
`index.html` is the deployed artefact, the validator checks it, and `scripts/gen_outline.py` reads it
to build the sidebar, so it is the copy that cannot silently drift.

## Cross-linking

Which sibling courses this one links, and the rule for when a link is worth making.

- Cloud modules link the relevant cloud course only when a mechanism's deployment is the point
  (e.g. where a scaled fleet actually lands), not as decoration.
- `Production Systems` links serve the same reader wanting an index rather than a route.
- **Verify an anchor exists in the target file before you commit it**: the validator strips fragments
  and will not catch a dead one.