# AGENTS.md - Production Agent Engineering

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

The **build track** for agents that survive production: five chapters covering eighteen topics across context and protocol, evaluation, durable state, latency and cost, and retrieval isolation.
Its sibling [`../ai-system-design-course/`](../ai-system-design-course/index.html) is the interview track over overlapping material; the two are written to read as one library, with chapters rather than micro-lessons.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - why the build track exists, what success looks like in a design review, and what is out of scope. Canonical.
2. [`NOTES.md`](NOTES.md) - the learner profile, the chapter shape, the cross-linking policy with the interview track, and known gotchas.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the markup contract for a chapter page.
4. [`RESOURCES.md`](RESOURCES.md) - the primary sources this course cites. Add anything new there before citing it.
5. [`PLOT.md`](PLOT.md) - the true reading order and what is planned but unwritten.
6. One existing chapter, to match its voice. Chapter 1 is the entry point.

## The rules that bite hardest here

- **Name the distributed-systems concept the agent problem is isomorphic to**, then say precisely where the isomorphism breaks. That is this course's core teaching move; see `NOTES.md`.
- **Every chapter ends with a field drill**: the questions a Staff+ reviewer actually asks about a system you are going to run, and the trap inside each one. A chapter without one is unfinished.
- **Cross-links go to the interview track only where the two genuinely touch** and the other page adds something. A link that only says "this exists elsewhere too" costs a click and returns nothing. Cross-links land on real anchors: the validator strips fragments before checking, so a missing anchor passes validation and breaks silently - check `id` attributes by hand.
- **No invented numbers.** The 30 percent semantic-caching saving circulating in agent-engineering source lists has no primary source behind it; frame savings as hit rate times avoided call cost instead. See `NOTES.md`.

## Out of scope here

Training or fine-tuning models, framework tutorials, prompt-writing craft, agent product design, and interview technique.
`MISSION.md` owns the list and the reasons; the interview track owns interview technique.
