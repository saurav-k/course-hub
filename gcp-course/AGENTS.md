# AGENTS.md - Inside Google Cloud

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever
the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

The deep Google Cloud course of the Cloud Architecture category: one platform walked end
to end as a connected design, from its account hierarchy (projects under folders under an organisation) to the
services built on it. Modules 01 to 04 are written; `PLOT.md` holds the fourteen-module
plan and the written sequence, and it is authoritative for both.

## Read before you write

In this order: [`MISSION.md`](MISSION.md), [`NOTES.md`](NOTES.md),
[`BUILDER-SPEC.md`](BUILDER-SPEC.md), [`RESOURCES.md`](RESOURCES.md),
[`PLOT.md`](PLOT.md), then two neighbouring lessons once any exist.

## The rules that bite hardest here

- **No Google Cloud facts without verified research behind them.** Pages are written only
  from sourced, verified material; until then a topic stays unwritten. See
  `MISSION.md`.
- **Capability names follow the shared taxonomy** in
  `../cloud-comparison-course/matrix.js`, so cross-cloud links stay exact. See
  `BUILDER-SPEC.md`.
- **Everything here is evergreen.** No dates, countdowns or study schedules on any
  page; dates live only in `RESOURCES.md`. A certification's weights may be cited as
  what the exam tests, never as a plan.
- **A lesson number names its module.** `lessons/MMxx-*.html`, where `MM` is the module
  number in [`PLOT.md`](PLOT.md): module 01 owns 0100 to 0199, module 02 owns 0200 to
  0299, and so on. Modules are commissioned separately and written in parallel, so a
  single running sequence collides the moment two contributors add a lesson. The eyebrow,
  the card `.ln` and the footer carry the four-digit number unchanged, because dropping
  the padding as the house `widgets.md` describes would render 0200 as "Lesson 200".
- **An absence is a finding and has to be stated exactly.** Where the verified inventory
  records that Google Cloud ships nothing for a capability, say so plainly. Where it
  records the capability as delivered inside another service, name that service. Never
  write that this cloud cannot do something without the inventory recording a real,
  reasoned absence: that error was the most common serious defect found across this
  programme, and `RESOURCES.md` lists the flags the inventory itself raised.

## Out of scope here

Cross-cloud comparison - [Comparing the Four Clouds](../cloud-comparison-course/index.html)
owns it. `MISSION.md` owns the full list and the reasons.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this course.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
