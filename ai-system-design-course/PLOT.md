# Plot - the reading order of this course

This file records the true reading order of the course: where every chapter sits, and everything planned but unwritten.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order, and a tutorial or lab session that follows a lecture sits after that lecture in the course map, never in a separate list at the bottom.**
When this file and the course `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The sequence

The course is linear: six chapters, read in number order.
The chapters are grouped by pillar and sized by the pillar's honest boundary; the topic counts are uneven on purpose.

| # | Position | Status | Notes |
|---|---|---|---|
| 1 | **Chapter 1 - LLM Basics** (`lessons/0000`) | written | 19 topics. Tokens, context windows, sampling, tool calling, agents, hallucinations, routing, the fine-tuning decision. The start-here chapter. |
| 2 | **Chapter 2 - RAG and Retrieval** (`lessons/0001`) | written | 19 topics. Most rounds are won here. |
| 3 | **Chapter 3 - AI System Architecture** (`lessons/0002`) | written | 19 topics. The reference whiteboard diagram. |
| 4 | **Chapter 4 - Cost and Performance** (`lessons/0003`) | written | 18 topics. Token budgeting, the three caches, latency budgets, behaviour under overload. |
| 5 | **Chapter 5 - Evaluation and Quality** (`lessons/0004`) | written | 18 topics. Golden datasets, LLM-as-judge and its biases, drift, escalation. |
| 6 | **Chapter 6 - Reliability and Security** (`lessons/0005`) | written | 18 topics. Degradation ladders, error budgets, prompt injection, compliance. |

The glossary at `reference/glossary.html` holds all 111 terms and reads alongside from Chapter 1 onwards; it is reference material, not a position in the sequence.

## Planned but unwritten

- **A whiteboard-checklist reference sheet**, worth adding once the chapters have been used in a mock round rather than merely read. Reference sheets sit beside the sequence like the glossary does.
- **Learning records**, added once the learner works through a chapter and demonstrates recall, not exposure.

There are no reserved positions. A seventh chapter would be a scope decision for `MISSION.md` first and a new row here second.

## Adding a session to this course

1. Read `BUILDER-SPEC.md`, `NOTES.md`, and an existing chapter first.
2. Take the next free lesson number. Never renumber anything.
3. A new chapter takes its place in this table and in `index.html` in pillar order, which is the reading order. A new topic inside a chapter joins that chapter's list in place.
4. Re-run `python3 scripts/gen_outline.py ai-system-design-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py`, and check every cross-link anchor by hand before opening the pull request.
