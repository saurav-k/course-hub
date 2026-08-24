# AGENTS.md - AI System Design for Staff+ Interviews

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

The **interview track**: six chapters covering 111 topics for Senior, Staff, and Principal AI/ML system design rounds.
It assumes the reader can already reason about sharding, replication, consistency, and backpressure, and spends its budget on the new bottleneck set - tokens, context windows, retrieval quality, inference cost, hallucinations, model latency, evaluation, and user trust.
Its sibling [`../agent-engineering-course/`](../agent-engineering-course/index.html) is the build track over overlapping material; where that course asks what you would ship, this one asks what you would say at a whiteboard.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - why the interview track exists and what is out of scope. Canonical.
2. [`NOTES.md`](NOTES.md) - the learner profile, the chapter shape, and the open threads.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the markup contract for a chapter page.
4. [`RESOURCES.md`](RESOURCES.md) - the primary sources this course cites. Add anything new there before citing it.
5. [`PLOT.md`](PLOT.md) - the true reading order and what is planned but unwritten.
6. One existing chapter, to match its voice. Chapter 1 is the entry point.

## The rules that bite hardest here

- **Every topic gets its own subsection with a linked primary source**, so a chapter doubles as a revision index the night before an interview. That shape is the product; do not flatten topics into running prose.
- **Every chapter ends with an interview drill**: the questions actually asked, and the trap in each. A chapter without its drill is unfinished.
- **Interview framing beats mechanism depth.** When a topic wants more depth than the round requires, link to the course that owns it rather than growing this chapter; `llm-papers-course` owns mechanisms, `agent-engineering-course` owns production practice.
- **Quiz options must match in length** so formatting never leaks the answer, as everywhere in the hub.

## Out of scope here

Training large models from scratch, framework tutorials, coding rounds, behavioural rounds, and compensation strategy.
`MISSION.md` owns the list and the reasons.
