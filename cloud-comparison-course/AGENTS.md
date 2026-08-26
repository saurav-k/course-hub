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

- **No cloud facts without verified research behind them.** Every cell in
  `matrix.js` comes from a verified per-cloud inventory. See `MISSION.md`.
- **`matrix.js` is generated, not hand-written.** It is joined from the four
  verified inventories onto the canonical vocabulary, and both live outside this
  repository. Correcting a cell here is lost at the next refresh: correct the
  inventory it came from and regenerate. `RESOURCES.md` records the read dates and
  the refresh procedure.
- **`matrix.js` is the only home of capability keys**, and the validator gates it:
  row set, domains, cell states and link shape all fail the pull request when they
  drift. See `BUILDER-SPEC.md`.
- **Four cell states, none of them interchangeable.** Never merge two, in data or
  in styling. The pair that bites is `absent` against `elsewhere`: both arrive as
  a `gaps` entry in the same inventory, and only `absent` lets a reader conclude
  the cloud cannot do the thing, so **NO EQUIVALENT belongs to `absent` alone**.
  Which gaps are which is a list the research directory holds; the gap prose does
  not separate them. See `NOTES.md`.
- **Everything here is evergreen.** No dates, countdowns or study schedules on any
  page; dates live only in `RESOURCES.md`.
- **A lesson number names its module.** `lessons/MMxx-*.html`, where `MM` is the
  module number in the table in [`PLOT.md`](PLOT.md), which is authoritative: module
  02 owns 0200 to 0299. Modules are written in parallel by different contributors, so
  a single running sequence collides the moment two of them add a lesson. The eyebrow,
  the card `.ln` and the footer carry the four-digit number unchanged, because dropping
  the padding as `widgets.md` describes would render 0200 as "Lesson 200".

## Out of scope here

Deep single-cloud teaching - each sibling per-cloud course owns that. `MISSION.md`
owns the full list and the reasons.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
