# AGENTS.md - End-to-End AI Engineering

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

Fifty-three lessons on turning one working LLM script into a system you can measure, improve, defend and operate: a retrieval pipeline with evaluation and observability wired in on day one, retrieval quality proved with numbers, agents with tools and memory graded on their trajectory, multi-agent orchestration over MCP and A2A priced before it is built, and a deployment with three probes, four caches and a threshold in CI.
Eight modules on the captain's syllabus, lesson grain, one linear order, plus a capstone the reader builds across the course and four reference sheets.

What it owns in this hub that no sibling owns: **A2A**, **the host side of MCP**, **agent memory outside the context window**, and **the arithmetic of refusing a second agent**.
[`MISSION.md`](MISSION.md) carries the full boundary table and the reasons.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - learner, cold spot, five capabilities, the three failure modes, the ladder, the capstone decisions and the out-of-scope table. Canonical; do not rewrite it as a side effect of other work.
2. [`NOTES.md`](NOTES.md) - cadence, teaching preferences, the six rules that came out of the research, and the gotchas that cost the last author an hour.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the course delta: the measurement rule, the provenance rule and the cross-linking table.
4. [`RESOURCES.md`](RESOURCES.md) - the canon, the per-module sources, and the `## Gaps` list. Add anything new there before citing it.
5. [`PLOT.md`](PLOT.md) - the true reading order, the numbering rule, the eight registration blocks, and where the capstone pages are read rather than filed.
6. `lessons/0000-your-demo-works-and-you-cannot-prove-it.html` - the gold page. Match it.

## The rules that bite hardest here

- **Fill your own `<!-- module-NN:start -->` block and touch no other.** Eight writers work in this course at the same time. `index.html`, `PLOT.md`, `RESOURCES.md` and `reference/glossary.html` are where eight branches collide, and the blocks plus the integrator's ownership of the last two are what prevent it. `PLOT.md` has the full statement.
- **Every page ends with a number or an artefact in the reader's own repository.** This course's whole claim over its concept-first siblings is the word hands-on. A page that explains a mechanism a sibling explains better, with a code block bolted on, is the failure `MISSION.md` names first.
- **Every number carries whose measurement it is, in the same sentence.** A vendor's figure on the vendor's own corpus is evidence that an effect is real and is never a target for the reader's corpus.
- **An OpenTelemetry attribute carries the convention's Development status and the specification revision it instruments.** Both are in the same paragraph, always. The convention has no releases and no tags, and it and the MCP specification already disagree. [`NOTES.md`](NOTES.md) has the mechanism.
- **The protocol is the subject; the framework is the fixture.** A framework may be named when it is the shortest honest way to show a mechanism, pinned to a version in the sentence. It is never the subject of a lesson. The test: if the named package disappeared, would this page still be worth reading?
- **No coding-agent example in modules 3 or 5, and no code corpus as the worked example in modules 1, 2 or 4.** Both exist to keep this course from reading as a second copy of `../ai-software-developer-course/`.
- **Modules 5 to 8 re-run module 1's golden set.** Do not build a second eval harness. A course with two harnesses has none.

## Out of scope here

Model internals, serving engines and quantization, whiteboard interview practice, coding agents and agent-ready repositories, organisational decisions and model retirement, and classic backend scaling.
[`MISSION.md`](MISSION.md) owns the list and names the neighbour that owns each row.
Syllabus bullet 7.3, interview preparation, is dropped by a recorded decision; do not re-propose it.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this course.
Do not repeat what the other instruction files already carry; point at the authoritative file instead.
Prefer rewriting or pruning existing entries over appending new ones, and keep entries concise.
