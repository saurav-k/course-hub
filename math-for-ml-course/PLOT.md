# Plot - the reading order of this course

This file records the true reading order of the course: where every module and page sits, and everything planned but unwritten.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order, and a tutorial or lab session that follows a lecture sits after that lecture in the course map, never in a separate list at the bottom.**
When this file and the course `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The sequence

The eleven modules run in the order their file numbers do, so **reading `lessons/` in ascending number order is always a legal reading order**: no page needs a page that comes after it.
Two positions are deliberate and non-obvious: Module 04 (eigenvalues, SVD, PCA) precedes calculus because everything in it is calculus-free once PCA is derived through the SVD, and Module 02 sits second so a reader meets a histogram long before the Central Limit Theorem.

| # | Module | Lessons | Status |
|---|---|---|---|
| 0 | Start here: one dataset, eleven modules, how to read this course | `0000` | written |
| 1 | M01 Foundations: notation, sets, functions, logs, counting, limits | `0001`-`0009` | written |
| 2 | M02 Data and summaries | `0020`-`0027` | written |
| 3 | M03 Vectors, matrices, and linear maps | `0040`-`0052` | written |
| 4 | M04 Eigenvalues, SVD, and PCA | `0060`-`0069` | written |
| 5 | M05 Calculus for machine learning | `0080`-`0091` | written |
| 6 | M06 Optimization | `0100`-`0111` | written |
| 7 | M07 Probability | `0120`-`0134` | written |
| 8 | M08 Expectation, limits, and simulation | `0140`-`0155` | written |
| 9 | M09 Estimation, testing, and inference | `0160`-`0172` | written; one page briefed but unwritten (below) |
| 10 | M10 Information, similarity, and dimension | `0180`-`0190` | written |
| 11 | M11 Capstone: regression, end to end | `0200`-`0202` | written |

That is 123 written pages: the start-here page plus the eleven modules.

Two orders besides the main line exist as link indexes rather than routes, which keeps the single-route property intact:

- The **fast path through probability and statistics**: M01, then M02, then M07 to M09, taking M05's two pages on integrals first. It is a reading list over existing pages, not a reordering.
- The **`core`/`depth` partition**: every page is labelled one or the other in its brief, where `core` is the roughly thirty-page path a reader needs for a modern paper. The partition is recorded from day one so a fast-track route can be added later without renumbering.

The reference sheets - notation, formula sheet, glossary, datasets, self-test, by-subject and interview indexes under [`reference/`](reference/) - read alongside; they are not positions in the sequence.

## Planned but unwritten

- **Lesson `0173`, "Bayesian against frequentist"**, the last page of M09. Its brief exists at `briefs/0173-bayesian-against-frequentist.md`; it takes its place between `0172` and M10 when written.
- **A few pages of headroom.** `MISSION.md` budgets roughly 133 content pages against the 123 now written, because pages carrying named proofs sometimes split rather than stretch past the word ceiling. No further numbers are claimed; a new page starts with a brief claiming its number.
- Nothing else is reserved.

## Adding a session to this course

1. Write the brief first, in `briefs/NNNN-slug.md`, claiming the next free number. The brief is complete enough that the writer needs no further briefing; see `NOTES.md` for what it must carry.
2. Take nothing for granted about position: the number places the page inside its module, and the module order above *is* the reading order. A page never moves to make room.
3. Follow the writing order in `NOTES.md`: brief, dataset, code, figures, prose, quizzes, card, outline, checkers, browser.
4. Run `python3 scripts/gen_outline.py math-for-ml-course`, commit the regenerated `outline.js`, run both `scripts/validate_site.py` and `.claude/skills/course-authoring/scripts/check_pages.py math-for-ml-course`, and open the page in both render states before opening the pull request.
