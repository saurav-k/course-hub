# AGENTS.md - Probability You Build

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

The hub's build-first probability course, modelled on Stanford's Probability for AI (PAI1):
six weeks plus a capstone, each week existing so the learner ships a running browser
artifact - the Spend Planner, the Distribution Garden, the pyramid chamber and phone
tracker, an adversarial test suite, the Glass Network, the Audit Bench - with theory
arriving only when the build needs it. It is deliberately complementary to
`statistical-foundations-ml-course`, which owns the formal lecture treatment; this course
cross-links rather than re-derives. Every interactive build runs as zero-dependency vanilla
JavaScript in the lesson page. Nothing is written yet; see [`PLOT.md`](PLOT.md).

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - why the course exists, who it is for, what is out of scope.
   Canonical; do not rewrite it as a side effect of other work.
2. [`NOTES.md`](NOTES.md) - how this course teaches: the derive-code-simulate triple,
   predict-then-run, frozen data, seeded randomness, and the gotchas.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the markup contract for builds and the course deltas.
4. [`RESOURCES.md`](RESOURCES.md) - the sources this course trusts. Add anything new there before citing it.
5. [`PLOT.md`](PLOT.md) - the true reading order and the reserved numbering blocks. Place any new page by it, never at the bottom.
6. `.claude/skills/course-authoring/references/widgets.md`, section "Interactive builds" -
   the exact `.build` wrapper markup every build uses.

## The rules that bite hardest here

- **The `.build` wrapper markup is frozen.** Canvas, controls, readout, caption, exactly as
  documented in `widgets.md`; six parallel workers are writing against those class names.
  Never rename them, never fork the shape.
- **Build scripts live at `assets/builds/<name>.js`**, loaded from the head with `defer`.
  They draw colours only from CSS tokens and re-render on mode or palette change (the
  MutationObserver pattern in `BUILDER-SPEC.md`), or they will silently show stale colours
  after a theme toggle.
- **Never renumber anything, never cross a block.** Weeks own reserved blocks of one hundred
  numbers (`0000`-`0099` and so on); take free numbers inside your own block only.
- **Frozen data over live data.** Prices and benchmarks enter as dated, cited snapshot
  constants; no runtime fetches, no keys. Prefer neutral tier names over brand names.
- **Cross-link the derivations.** Bayes, confidence intervals, gradient descent mechanics:
  link to `statistical-foundations-ml-course` or `math-for-ml-course`; verify the anchor
  exists before committing.

## Out of scope here

Measure-theoretic probability, proofs as ritual, live API calls, frameworks and chart
libraries, and re-deriving what the sibling courses already teach.
The full list and the reasons live in `MISSION.md`.
