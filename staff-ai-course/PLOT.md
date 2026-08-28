# Plot - the reading order of The Staff AI Engineer

This file records the true reading order of the course: where every chapter sits, and everything planned but unwritten.
It is filled from the interview answer about order in `MISSION.md` and from the course map in `index.html`.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order, and a session that follows a chapter sits after that chapter in the course map, never in a separate list at the bottom.**
When this file and `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

The ordering principle here is **one system's life**, from "should this exist" to "who has to agree", with one prerequisite chapter in front of it.
Each row states what it depends on, so the ladder is checkable by reading the table top to bottom.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The sequence

| # | Position | Rung | Status | Depends on | Why it sits here |
|---|---|---|---|---|---|
| 1 | `lessons/0000-reading-the-claim.html` - Reading the Claim | foundation | written | nothing | Every later chapter consumes evidence. A reader who cannot audit a number cannot make a single decision in chapters 1 to 8. |
| 2 | `lessons/0001-should-this-be-an-ai-system.html` - Should This Be an AI System at All | foundation | written | 0000 | "Should we" is answered with evidence, so it needs chapter 0 first. It is also the chapter that stops you spending the money every later chapter costs. |
| 3 | `lessons/0002-the-shape-of-the-system.html` - The Shape of the System | working | written | 0001 | Shape is only decidable once the problem is. Prompt, workflow or agent, and the price of each step up the ladder. |
| 4 | `lessons/0003-where-the-knowledge-comes-from.html` - Where the Knowledge Comes From | working | written | 0002 | The shape determines what knowledge the system needs and when it needs it. |
| 5 | `lessons/0004-proving-it-works.html` - Proving It Works | working | written | 0003 | You cannot evaluate a system whose knowledge path is undecided. Ownership, statistics and organisational cost, not eval mechanics. |
| 6 | `lessons/0005-what-it-costs.html` - What It Costs | working | written | 0004 | Every cost lever changes behaviour, so none of them is safe to pull before the previous chapter's gate exists. This edge is the important one. |
| 7 | `lessons/0006-the-blast-radius.html` - The Blast Radius | working | written | 0002 and 0005 | Authority and cost ceilings are the two limits on the same thing. |
| 8 | `lessons/0007-model-supply-is-a-dependency.html` - Model Supply Is a Dependency | frontier | written | 0000 and 0004 | A supply change is detected by evidence and defended by evals, so it needs both. |
| 9 | `lessons/0008-carrying-the-organisation.html` - Carrying the Organisation | frontier | written | all of the above | This chapter is about those decisions being carried by people. You cannot argue for an eval budget until you can quantify what its absence costs. |

## Reference sheets

Read alongside, not positions in the sequence.

| Sheet | Status | What it is |
|---|---|---|
| `reference/decision-record.html` | written | The five-field template as a print-friendly page. The artefact a reader takes into a review rather than only into a reading. |
| `reference/claim-audit.html` | written | Chapter 0000's checklist as a one-page audit for reading someone else's number. |
| `reference/glossary.html` | written | Every term this course introduces, linked to the decision that develops it. |

## Planned but unwritten

Nothing is reserved.
Three candidates have been considered and deliberately not reserved, because a position reserved for a chapter nobody can source is a promise the course cannot keep:

- **A compliance chapter.** The EU AI Act was researched only for its timeline, not its substance. It needs its own research round before a position is claimed for it.
- **A chapter on retiring an AI feature you built.** The research found no published account of a named company removing an LLM from production and replacing it with a classical model or rules. The absence is taught in chapter 0001 as a finding; it is not enough to build a chapter on.
- **A tenth chapter splitting 0006.** Security and observability are one chapter today. If the security material outgrows it, the split is into "what it may do" and "what you recorded", not into "attacks" and "defences".

## Adding a chapter to this course

1. Read `AGENTS.md`, `MISSION.md` and `NOTES.md` first, in that order.
2. Take the next free lesson number. Never renumber anything.
3. Insert the new material at its true position in this file and in `index.html`, never appended to the bottom because it arrived last.
4. Re-run `python3 scripts/gen_outline.py staff-ai-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py`, and open the changed pages in both render states before opening the pull request.
