# AGENTS.md - Coding Harness Engineering

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

Twenty-eight pages on the software artifact every engineer uses daily and almost nobody has read: the coding harness.
Ten harnesses are covered from their own source at a pinned commit, five from official documentation only (closed source), plus one report on the model layer beneath all of them.
Lesson grain, single linear order, diagram-led by design.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - learner, cold spot, five capabilities, failure mode. Canonical.
2. [`NOTES.md`](NOTES.md) - cadence, teaching preferences, known gotchas.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the course delta only: numbering, the deep-dive skeleton, the evidence rules.
4. [`RESOURCES.md`](RESOURCES.md) - the canon and its provenance. Add anything new before citing it.
5. [`PLOT.md`](PLOT.md) - the true reading order: what is written, what is planned, where each issue number lands.
6. `lessons/0000-what-is-a-coding-harness.html` - the gold page. Match it.

## The rules that bite hardest here

- **Every mechanism gets two named harnesses minimum**, answering it differently. One example is an anecdote; the design space needs the second answer.
- **Cite what the reader can open**: the repository at its pinned commit, or official documentation you fetched this session.
  The sixteen research reports behind this course are working material and are never cited by path - find the public source underneath the claim.
- **Deep dives keep the skeleton** (identity, loop, context, trust, extensions, models, distinctive). The module's value is side-by-side comparability; a creative restructure breaks nineteen pages against each other.
- **Numbers come from a pinned source or show their arithmetic.** Token budgets, thresholds, and tool counts differ per harness and per version; a number without either is invented.

## Out of scope here

Model internals and training (`../../llm-evolution-course/`), production agent operation (`../../agent-engineering-course/`), inference serving (`../../llm-inference-course/`).
`MISSION.md` owns the list and the boundary with the build track.
