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
| 2 | **Lecture 2: The probability space** | written | Lessons `0009` to `0015`: a hub plus six parts, plus the Lecture 2 formula sheet in `reference/`. Dated Aug 18, 2026. |
| 3 | **Lecture 3: From the axioms to Bayes** | written | Lessons `0016` to `0024`: a hub plus eight parts, plus the Lecture 3 formula sheet in `reference/`. Dated Aug 22, 2026. |
| 4 | **TA Session 1** (tutorial) | written | Lessons `0025` to `0033`: a hub plus eight parts, the twelve tutorial problems worked in full from the Week 1 question sheet and tutorial notes, dated August 22, 2026. It follows Lecture 3 and sits there in the map, not in a list at the bottom. Its twelve problems are its own; they are not duplicated by the problem sets below. |
| 5 | **Homework 1: Practice Set 1, explained not solved** | written | Lessons `0034` to `0044`: a hub plus ten parts. The four graded problems get one page each and the thirty practice problems are grouped by concept. Nothing on those pages is solved, on purpose. Due Sunday 6 September. |
| 6 | **Lecture 4: the applied pass** | written | Lessons `0045` to `0057`: a hub plus twelve parts, plus the Lecture 4 formula sheet in `reference/`. Dated Aug 25, 2026, six handwritten pages. The worked medical-test example, independence as a check on a table, and the counting and sampling machinery. It sits after Homework 1 by the captain's own placement, which is also the true chronological order. |
| 7 | **Lecture 5: counting and sampling, applied** | written | Lessons `0058` to `0068`: a hub plus ten parts, plus the Lecture 5 formula sheet in `reference/`. Dated Aug 29, 2026, five handwritten pages of class notes alongside the lecturer's typeset examples handout for the same three problems. Three machine-learning problems worked end to end, the page on where the equally-likely formula stops being legal, and the road to the binomial. It follows Lecture 4 directly, which is both its true position and the chronological one. |
| 8 | **TA Session 2 (Week 2)** (tutorial) | written | Lessons `0069` to `0076`: a hub plus seven parts. Seven questions worked in full from two sets of scribe notes, Saturday 29 and Sunday 30 August 2026. It follows Lecture 5, which is the material it drills, and sits there in the map rather than in a list at the bottom. The source's own question numbers (3, 10, 25, 30) are kept; two of its questions carry no number and that is recorded rather than repaired. |
| 9 | **Lecture 6: the random variable** | written | Lessons `0077` to `0091`: a hub plus fourteen parts, plus the Lecture 6 formula sheet in `reference/`. Eight pages of the lecturer's handwritten pre-class notes: the random variable as a function from the sample space to the real line, the PMF, the CDF with its four properties proved, five named discrete shapes, the density, the uniform and exponential, the Gaussian, and light against heavy tails. It follows TA Session 2, which is where this course's own sequence had reached. **Numbering drift, recorded here so the next person is not caught by it: the source document for this lecture is titled as the lecturer's Lecture 4, and it is not this course's Lecture 4, which is lessons `0045` to `0057` and covers conditional probability, independence and counting; the lecturer's own lecture numbering and this course's session numbering have drifted apart by one topic, and nothing has been renumbered to make them agree.** The source's first page carries a handwritten date reading 11/8/25, which is a preparation date on a pre-class document and does not fit the 2026 session timeline the rows above record, so no delivery date is claimed for this lecture. |
| 10 | **Third tutorial session** | reserved | No source deck exists yet, so nothing is named or anchored. The position after the current material is held, and the exact anchor is pinned in this file and in `index.html` on the day its deck arrives. |

After the positions above sit the remaining lectures of the source series, planned but unwritten and listed as roadmap entries in `index.html`: the joint and conditional halves of random variables, PMFs and PDFs, expectation, variance and covariance, moment generating functions, tail inequalities, the law of large numbers and CLT, and conditional expectation with MMSE.
Row 9 above has now delivered the single-variable half of slide 20's Lectures 4, 5 and 6; joint CDFs, joint and conditional PMFs and PDFs, and independence of random variables are all still unwritten.

Note the divergence between plan and delivery, because the roadmap numbering in `index.html` does not match the sessions that actually happened.
Slide 20 of Lecture 1 plans Lecture 4 as random variables and the CDF.
The session delivered as Lecture 4, on 25 August 2026, is the applied conditional-probability pass plus counting and sampling, which slide 20 had placed earlier.
Delivery therefore runs one lecture behind the slide-20 plan, and the roadmap list is kept as the deck wrote it rather than renumbered.
The same divergence holds for Lecture 5: slide 20 plans it as discrete random variables and the PMF, while the session delivered on 29 August 2026 is the applied counting and sampling pass that ends at the binomial.
A second, independent divergence is recorded in row 9: the lecturer's own numbering of his handwritten notes has drifted from this course's session numbering by one topic, so the notes titled Lecture 4 are this course's Lecture 6.
The two divergences have the same cause and are not the same fact; check both before assigning a number to new material.
Each entry takes its true place in this table when its deck arrives; a tutorial deck that lands among them slots in after the lecture it supports rather than at the end.

## Planned but unwritten, off the main line

- **Problem sets**, tracked in hub issues #102 and #103: nine concept sets for Lectures 1 and 2, then six sets for Lecture 3 plus three of extra tutorial practice, landing in a `problems/` folder with its own index.
  Problem sets attach to lectures concept by concept rather than holding a position in the read, so they are recorded here but not as sequence rows.
- **A closing pass** that wires lessons to their problem sets and back, reconciles the glossary, and reads the whole map against this file.
- **One formula sheet per lecture.** The policy in `NOTES.md` is to keep one per lecture rather than grow a single sheet nobody prints. Lectures 1, 2, 3, 4, 5 and 6 each have one in `reference/`; the Lecture 2 sheet is linked from its own lessons but not yet from the course map.

## Adding a session to this course

1. Read `BUILDER-SPEC.md` and two neighbouring pages first.
2. Take the next free lesson number. Never renumber anything.
3. Insert the new material at its true position in this file and in `index.html`. A tutorial goes directly after the lecture it supports.
4. Re-run `python3 scripts/gen_outline.py statistical-foundations-ml-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py`, and open the changed pages in both themes before opening the pull request.
