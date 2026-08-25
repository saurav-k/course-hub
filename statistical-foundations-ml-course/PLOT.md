# Plot - the reading order of this course

This file records the true reading order of the course: where every lecture and tutorial session sits, and everything planned but unwritten.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order, and a tutorial or lab session that follows a lecture sits after that lecture in the course map, never in a separate list at the bottom.**
When this file and the course `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.
New material takes its real position here and in `index.html`; it is never appended to the end just because it arrived last.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The sequence

| # | Position | Status | Notes |
|---|---|---|---|
| 1 | **Lecture 1: Introduction** | written | Lessons `0000` to `0008`: a hub plus eight parts, plus the Lecture 1 formula sheet in `reference/`. Dated Aug 11, 2026 in the source deck. |
| 2 | **Lecture 2: probability axioms, conditional probability and independence** | written | Lessons `0009` to `0015`: a hub plus six parts, plus the Lecture 2 formula sheet in `reference/`. |
| 3 | **Lecture 3: counting and sampling** | written | Lessons `0016` to `0024`: a hub plus eight parts, plus the Lecture 3 formula sheet in `reference/`. |
| 4 | **TA Session 1** (tutorial) | written | Lessons `0025` to `0033`: a hub plus eight parts, the twelve tutorial problems worked in full from the Week 1 question sheet and tutorial notes, dated August 22, 2026. It follows Lecture 3 and sits there in the map, not in a list at the bottom. Its twelve problems are its own; they are not duplicated by the problem sets below. |
| 5 | **Homework 1 chapter** (Practice Set 1) | in progress | Lessons `0034` to `0044`: a hub, one page per graded problem (`0035` to `0038`, covering the sheet's four submitted questions worth 15 marks, due Sunday 6 September), and six pages grouping the thirty practice problems by concept (`0039` to `0044`). It sits after TA Session 1 in the map, because the homework tests exactly what Lectures 2, 3 and TA Session 1 built. Nothing on any of its pages solves a problem: the chapter explains, names traps, and stops before the arithmetic. The hub and the graded four are written; the six practice-grouping pages follow. |
| 6 | **Second tutorial session** | reserved | No source deck exists yet, so nothing is named or anchored. The position after the current material is held, and the exact anchor is pinned in this file and in `index.html` on the day its deck arrives. |
| 7 | **Third tutorial session** | reserved | As above. |

After the positions above sit Lectures 4 through 12 of the source series, planned but unwritten and listed as roadmap entries in `index.html`: random variables and CDFs, discrete PMFs, continuous PDFs, expectation, variance and covariance, moment generating functions, tail inequalities, the law of large numbers and CLT, and conditional expectation with MMSE.
Each takes its true place in this table when its deck arrives; a tutorial deck that lands among them slots in after the lecture it supports rather than at the end.

## Planned but unwritten, off the main line

- **Problem sets**, tracked in hub issues #102 and #103: nine concept sets for Lectures 1 and 2, then six sets for Lecture 3 plus three of extra tutorial practice, landing in a `problems/` folder with its own index.
  Problem sets attach to lectures concept by concept rather than holding a position in the read, so they are recorded here but not as sequence rows.
- **A closing pass** that wires lessons to their problem sets and back, reconciles the glossary, and reads the whole map against this file.
- **One formula sheet per lecture.** The policy in `NOTES.md` is to keep one per lecture rather than grow a single sheet nobody prints. Only Lecture 1's exists.

## Adding a session to this course

1. Read `BUILDER-SPEC.md` and two neighbouring pages first.
2. Take the next free lesson number. Never renumber anything.
3. Insert the new material at its true position in this file and in `index.html`. A tutorial goes directly after the lecture it supports.
4. Re-run `python3 scripts/gen_outline.py statistical-foundations-ml-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py`, and open the changed pages in both themes before opening the pull request.
