# AGENTS.md - Inside OCI

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever
the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

The deep OCI course of the Cloud Architecture category: one platform walked end
to end as a connected design, from its account hierarchy (compartments in a tenancy) to the
services built on it. All fourteen modules of the plan in `PLOT.md` are written; that
file remains authoritative for the module numbering and the reading order.

## Read before you write

In this order: [`MISSION.md`](MISSION.md), [`NOTES.md`](NOTES.md),
[`BUILDER-SPEC.md`](BUILDER-SPEC.md), [`RESOURCES.md`](RESOURCES.md),
[`PLOT.md`](PLOT.md), then two neighbouring lessons once any exist.

## The rules that bite hardest here

- **No OCI facts without verified research behind them.** Pages are written only
  from sourced, verified material; until then a topic stays unwritten. See
  `MISSION.md`.
- **Capability names follow the shared taxonomy** in
  `../cloud-comparison-course/matrix.js`, so cross-cloud links stay exact. See
  `BUILDER-SPEC.md`.
- **Everything here is evergreen.** No dates, countdowns or study schedules on any
  page; dates live only in `RESOURCES.md`.
- **A lesson number names its module.** `lessons/MMxx-*.html`, `MM` from the module
  table in [`PLOT.md`](PLOT.md), which is authoritative. The four-digit number is
  carried unchanged into the eyebrow, the card `.ln` and the footer. `PLOT.md`
  carries the reasoning.

## Out of scope here

Cross-cloud comparison - [Comparing the Four Clouds](../cloud-comparison-course/index.html)
owns it. `MISSION.md` owns the full list and the reasons.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
