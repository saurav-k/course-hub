# Plot - the reading order of this course

This file records the true reading order of the course: where every lesson sits, and everything planned but unwritten.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order, and a tutorial or lab session that follows a lecture sits after that lecture in the course map, never in a separate list at the bottom.**
When this file and the course `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The sequence

The course is linear: sixteen lessons in seven modules, read top to bottom.
The order is a dependency order for hands-on work - batching before eviction, engines before routing, routing before economics - so a lesson should only ever need what came before it.

| # | Position | Status | Notes |
|---|---|---|---|
| 1 | Module 00 - Inference Foundations: `0000` Inference 101, `0001` Local Testing | written | The mental model everything rests on, then models running locally behind one OpenAI-compatible gateway. |
| 2 | Module 01 - High-Throughput Serving Engines: `0002` vLLM and PagedAttention, `0003` SGLang and RadixAttention, `0004` Continuous Batching, `0005` KV Cache Eviction, `0006` Speculative Decoding | written | The core engine lessons. |
| 3 | Module 02 - Quantization: `0007` INT4/FP8/AWQ/GPTQ | written | The memory-quality-speed triangle. |
| 4 | Module 03 - Routing and Budgeting: `0008` Model Router, `0009` Token Budgeting | written | Cost, latency, quality forks, then per-request caps. |
| 5 | Module 04 - Edge and Deployment Targets: `0010` ONNX, TensorRT, WebLLM | written | Off the server. |
| 6 | Module 05 - Scale and Operations: `0011` Kubernetes, `0012` Observability, `0013` Load Testing | written | Running the stack like a system. |
| 7 | Module 06 - Economics and Craft: `0014` Unit Economics, `0015` Capstone | written | Where margins die, then build, benchmark, share. |

The glossary at `reference/glossary.html` reads alongside from Lesson 0 onwards; it is reference material, not a position in the sequence.

## Planned but unwritten

Nothing is currently planned beyond the capstone.
There are no reserved positions.
A seventeenth lesson would be a scope decision for `MISSION.md` first and a new row here second; it would take the next free number and the module position its dependency demands, which is not necessarily the end.

## Adding a session to this course

1. Read `NOTES.md` for the lesson skeleton, then an existing lesson or two.
2. Take the next free lesson number. Never renumber anything.
3. Insert it at its true position in this table and in `index.html`, inside the module whose material it depends on. If no module fits, that is a new-module decision, made deliberately rather than by appending.
4. Re-run `python3 scripts/gen_outline.py llm-inference-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py`, and open the changed pages in both themes before opening the pull request.
