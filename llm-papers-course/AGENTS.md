# AGENTS.md - LLM Papers, In Order

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

Thirty-seven foundational LLM papers plus a primer, as 38 self-contained lessons ranked easiest to hardest, each with plain-English intuition, heavy diagrams, the maths explained in words, runnable implementation code, and a retrieval quiz.
It owns **mechanism** in this hub: what the thing actually is and how to implement it.
[`../llm-evolution-course/`](../llm-evolution-course/index.html) owns the story of how it happened; [`../llm-inference-course/`](../llm-inference-course/index.html) owns serving practice.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - the original brief: who this is for and what "understand" means here. Canonical.
2. [`NOTES.md`](NOTES.md) - the teaching preferences and, most importantly, the nine-part lesson template every lesson follows.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the markup contract.
4. [`RESOURCES.md`](RESOURCES.md) - paper links and sources. Add anything new there before citing it.
5. [`PLOT.md`](PLOT.md) - the reading order and what is planned but unwritten.
6. One or two existing lessons. `lessons/0000-primer-neural-nets-to-tokens.html` is the on-ramp everything else assumes.

## The rules that bite hardest here

- **Follow the nine-part lesson template** in `NOTES.md`: header with year and arXiv link, TL;DR, why this paper exists, mechanism diagram-first, maths explained line by line in words, runnable implementation, retrieval quiz, how it connects, primary source. A lesson missing a part is unfinished.
- **The glossary at `reference/glossary.html` is canonical for terms**, and lessons adhere to it everywhere rather than coining variants.
- **Difficulty pills are relative to this course**, not to the field, and "easy" still assumes the primer.
- **Quiz options match in length** so formatting never leaks the answer.
- **No em dashes anywhere**, including inside code comments.

## Out of scope here

Chronology, people, and the adoption story (`llm-evolution-course`), serving operations and cost engineering (`llm-inference-course`), and interview framing (`ai-system-design-course`).
A lesson that finds itself telling history should link there instead.
