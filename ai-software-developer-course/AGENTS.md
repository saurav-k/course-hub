# AGENTS.md - AI Software Developer

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

Eighty-six pages on what a working engineer does at the keyboard and in the repository to make coding agents useful, safe and many: the loop and the tools it dispatches, context as a budget, skills and repository contracts, what makes a codebase agent-ready and how to score one, AI review, where prompt injection enters, and running unattended agents with a ceiling.
Ten modules on the captain's syllabus, lesson grain, one linear order, plus a capstone the reader builds across the course and three reference sheets.

What it owns in this hub that no sibling owns: **agent-ready codebases and agentic code review**, which nothing else here covers, and the practitioner's framing of everything else.
[`MISSION.md`](MISSION.md) carries the full boundary table and the reasons.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - learner, cold spot, five capabilities, the two failure modes, the ladder, and the out-of-scope table. Canonical; do not rewrite it as a side effect of other work.
2. [`NOTES.md`](NOTES.md) - cadence, teaching preferences, and the gotchas that cost the last author an hour.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the course delta: the samples licence rule, the three claim labels, the mechanism axis, and cross-linking.
4. [`RESOURCES.md`](RESOURCES.md) - the canon, the per-module sources, and the `## Gaps` list. Add anything new there before citing it.
5. [`PLOT.md`](PLOT.md) - the true reading order, the numbering rule, and where the capstone pages are read rather than filed.
6. `lessons/0000-you-are-already-running-one.html` - the gold page. Match it.

## The rules that bite hardest here

- **Every sample carries its source, its licence and a may-reproduce verdict, in the `.code-cap`.** A sample whose licence cannot be established is paraphrased or omitted, never shown with a hedge. This is the one rule no other course in the hub has, and the samples gallery is why. Full statement in [`BUILDER-SPEC.md`](BUILDER-SPEC.md).
- **Nothing on a page is dated.** No dates, no schedule, no grading weights, no guest-lecture pages. A version-sensitive claim carries the version in the sentence. An "in the field" page uses that company's public primary material only, and names a person only as the author of something the reader can open.
- **A product is evidence for an axis, never the subject of a section.** The test, from [`MISSION.md`](MISSION.md): if the named product disappeared, would this page still be worth reading? If not, the mechanism is missing and the page is a review.
- **Where a sibling course owns a mechanism, link the page and move on.** Re-teaching `coding-harness-course` is the second-worst thing this course can do, and it is the easy mistake in modules 1 to 4.
- **Quote a Mermaid node label, always, and write a dash where you want a semicolon.** This course is full of parentheses, commas, shell syntax and file paths, and `A[claude -p "..." | jq]` does not parse bare.
- **Take the next free step of ten inside your module's block, and never renumber anything.** [`PLOT.md`](PLOT.md) has the rule and the reason.

## Out of scope here

Harness internals, production agent operation, the staff-level decision, interview system design, the terminal runtime, and what a language model is.
[`MISSION.md`](MISSION.md) owns the list and names the neighbour that owns each row.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this course.
Do not repeat what the other instruction files already carry; point at the authoritative file instead.
Prefer rewriting or pruning existing entries over appending new ones, and keep entries concise.
