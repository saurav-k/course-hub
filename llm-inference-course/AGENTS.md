# AGENTS.md - LLM Inference Optimization

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

The hands-on serving course: sixteen lab-based lessons that take a reader from the prefill/decode mental model to a load-tested, costed, honestly benchmarked inference stack.
It is the practice partner to [`../llm-papers-course/`](../llm-papers-course/index.html), which owns the theory.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - why this course exists, what success looks like, and what is out of scope. Canonical.
2. [`NOTES.md`](NOTES.md) - the lesson skeleton (which doubles as the contract for a new lesson), the cadence, and the authoring cautions.
3. [`PLOT.md`](PLOT.md) - the true reading order and everything planned but unwritten.
4. One or two existing lessons. `lessons/0000-inference-101.html` sets the mental model; `lessons/0004-continuous-batching-queueing.html` is a good example of the full skeleton in action.

There is no `BUILDER-SPEC.md` and no `RESOURCES.md` here; both absences are decisions recorded in `MISSION.md` and `NOTES.md`, not oversights to fix.

## The rules that bite hardest here

- **Every lesson carries a runnable lab** with commands, code, a benchmark, and a checklist. A lesson with nothing to measure does not belong in this course.
- **Mechanism before the lab, diagram before the command.**
- **Measured numbers are labelled as one run on one machine.** Never present hardware-specific results as expected values.
- **Version-sensitive commands name both versions** when a flag changes, rather than silently updating.
- **Quiz options match in length**, as everywhere in the hub.

## Out of scope here

Training and fine-tuning models, paper-level derivations, and procurement advice.
`MISSION.md` owns the list; `llm-papers-course` owns the derivations.
