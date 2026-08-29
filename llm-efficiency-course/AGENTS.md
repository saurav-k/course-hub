# AGENTS.md - llm-efficiency-course

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.

## What this course is

Eleven lesson pages teaching the mechanisms that put a 320B/18B-active MoE (GLM-5.3-Flash) on desk hardware: the memory-bandwidth wall, quantization, LoRA/QLoRA post-training, the wider PEFT family, and speculative decoding, landing in two worked deployment case studies (two DGX Sparks; one 256 GB Mac Studio). It owns desk-scale deployment arithmetic in this hub; serving infrastructure lives in `llm-inference-course`.

## Read before you write

1. [`MISSION.md`](MISSION.md) - why the course exists and what is out of scope. Canonical; do not rewrite it as a side effect.
2. [`NOTES.md`](NOTES.md) - cadence, the doorway analogy policy, known gotchas.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the extended-bar opt-in and the derived-numbers rule.
4. [`RESOURCES.md`](RESOURCES.md) - the canon. Add anything new there before citing it.
5. [`PLOT.md`](PLOT.md) - the reading order and the two reserved positions (0011, 0012).
6. Two neighbouring lessons, to match voice, depth, and structure.

## The rules that bite hardest here

- Every number is sourced or derived on the page, labelled; never present a derivation as a measurement (`BUILDER-SPEC.md`).
- Every content page owes a chart and a practice problem with `.p-check`; this course opts into the extended bar (`BUILDER-SPEC.md`).
- Never renumber lessons; 0011 and 0012 are reserved positions (`PLOT.md`).
- Quiz markup is bound by `hub.js`; copy `widgets.md` character for character.

## Out of scope here

Serving infrastructure, transformer mathematics, cloud economics, distributed training - see `MISSION.md` for the neighbour that owns each.
