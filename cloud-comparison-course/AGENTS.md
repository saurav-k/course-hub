# AGENTS.md - Comparing the Four Clouds

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever
the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

The cross-cloud comparison course of the Cloud Architecture category: one capability
at a time, four clouds answering side by side, every answer linked to its vendor's
own documentation. It opens with the interactive capability matrix rendered from
`matrix.js` in this folder.

## Read before you write

In this order: [`MISSION.md`](MISSION.md), [`NOTES.md`](NOTES.md),
[`BUILDER-SPEC.md`](BUILDER-SPEC.md), [`RESOURCES.md`](RESOURCES.md),
[`PLOT.md`](PLOT.md), then the matrix section of
`../.claude/skills/course-authoring/references/widgets.md`.

## The rules that bite hardest here

- **No cloud facts without verified research behind them.** The cells in
  `matrix.js` ship unfilled on purpose; filling one is a later slice's job and it
  cites its inventory. See `MISSION.md`.
- **`matrix.js` is the only home of capability keys**, and the validator gates it:
  row set, domains, cell states and link shape all fail the pull request when they
  drift. See `BUILDER-SPEC.md`.
- **Unfilled and absent are different states.** Never merge them, in data or in
  styling. See `NOTES.md`.
- **Everything here is evergreen.** No dates, countdowns or study schedules on any
  page; dates live only in `RESOURCES.md`.

## Out of scope here

Deep single-cloud teaching - each sibling per-cloud course owns that. `MISSION.md`
owns the full list and the reasons.
