# AGENTS.md - Production Systems

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

The substrate course: eleven chapters covering 111 topics an engineer reaches for when designing or operating a production system.
Its organising idea is the three-tier spine - every topic answered at 100, 1,000, and 10,000 requests per second - because naming the load at which a decision flips is more useful than the technique itself.
It sits under [`../ai-system-design-course/`](../ai-system-design-course/index.html), the interview track, and [`../agent-engineering-course/`](../agent-engineering-course/index.html), the agent build track; both assume what this course teaches.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - why the three-tier spine exists and what is out of scope. Canonical.
2. [`NOTES.md`](NOTES.md) - the learner profile, the per-topic teaching order, and the parallel-authoring history.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the markup contract the chapters were written against. It is the reason eleven separately authored chapters read as one course: edit it rather than letting any chapter drift.
4. [`RESOURCES.md`](RESOURCES.md) - primary sources: RFCs, specifications, papers, first-party docs. Add anything new there before citing it.
5. [`PLOT.md`](PLOT.md) - the chapter order and what is planned but unwritten.
6. One existing chapter, to match its voice and its three-tier rhythm.

## The rules that bite hardest here

- **The three-tier spine is mandatory for every topic**: 100 / 1,000 / 10,000 requests per second, every time. A topic without its tiers is a glossary entry, not part of this course.
- **Arithmetic is shown, not asserted.** Derived numbers are welcome; borrowed numbers must be in the source you link.
- **Every proposal names its failure mode**, not only its benefit.
- **Diagrams over paragraphs**: a block or sequence diagram beats three paragraphs of prose.
- **Quiz options match in length** so formatting never leaks the answer.

## Out of scope here

Language-specific implementation, framework APIs, vendor comparison, procurement advice, and front-end concerns beyond the transport and security boundary.
`MISSION.md` owns the list and the reasons.
