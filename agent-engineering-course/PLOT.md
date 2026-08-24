# Plot - the reading order of this course

This file records the true reading order of the course: where every chapter sits, and everything planned but unwritten.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order, and a tutorial or lab session that follows a lecture sits after that lecture in the course map, never in a separate list at the bottom.**
When this file and the course `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The sequence

The course is linear: five chapters, read in number order.
The pillar boundary is the honest one, so the chapters are deliberately uneven in topic count; nothing is padded to make the counts match.

| # | Position | Status | Notes |
|---|---|---|---|
| 1 | **Chapter 1 - Context and Protocol** (`lessons/0000`) | written | Context as admission and eviction, MCP servers and what they refuse, typed handoffs, guardrails in version control. The start-here chapter. |
| 2 | **Chapter 2 - Evaluation and the Data Flywheel** (`lessons/0001`) | written | Trajectory evals, shadow testing, the thumbs-down pipeline, the teardown. |
| 3 | **Chapter 3 - State, Async and Degradation** (`lessons/0002`) | written | Durable execution, parking long-running tools, webhook resumption, the measured degradation ladder. |
| 4 | **Chapter 4 - Latency, Cost and Local-First** (`lessons/0003`) | written | TTFT against TPOT, semantic caching and the confidently wrong hit, kill-switches that refuse, inference on the user's own hardware. |
| 5 | **Chapter 5 - Retrieval and Isolation** (`lessons/0004`) | written | Indexing tables and layout, tenant filtering inside the search, bounding what an agent may do with hostile text. |

The glossary at `reference/glossary.html` reads alongside from Chapter 1 onwards; it is reference material, not a position in the sequence.

## Planned but unwritten

- **A fourth topic in Chapter 3**: human-in-the-loop approval as a first-class workflow state. It currently lives as a paragraph inside inter-agent security and a sentence inside degradation, which is one topic pretending to be two footnotes. When written, it joins Chapter 3's topic list in place; it does not become a new chapter.
- **A worked cost model** as a print-friendly reference sheet pairing with Chapter 4, once someone has run the arithmetic on a real workload. Reference sheets sit beside the sequence like the glossary does.
- **Learning records beyond the first**, added when the learner builds against a chapter and reports what the chapter got wrong, not on exposure.

## Adding a session to this course

1. Read `BUILDER-SPEC.md`, `NOTES.md`, and an existing chapter first.
2. Take the next free lesson number. Never renumber anything.
3. A new chapter takes its place in this table and in `index.html` by pillar order, which is the reading order. A new topic inside a chapter joins that chapter's list in place.
4. Re-run `python3 scripts/gen_outline.py agent-engineering-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py`, and check every cross-link anchor by hand before opening the pull request.
