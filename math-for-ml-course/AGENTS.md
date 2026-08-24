# AGENTS.md - Mathematics for Machine Learning

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

The hub's mathematics substrate: eleven modules from notation to a regression capstone, built so a working engineer who last did mathematics in 2009 can read any formula in a modern ML paper.
It owns the maths every other course uses and none of them teaches.
Its relationship with [`../statistical-foundations-ml-course/`](../statistical-foundations-ml-course/index.html) has a hard boundary, below.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - why the course exists, the union syllabus it follows, the six constraints, and the sibling boundary. Canonical; settled by interview.
2. [`NOTES.md`](NOTES.md) - the voice, the three sentences that shape a page, the order things get written in, and the gotchas the checker found.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the full page contract: layout, naming, dataset standard, quiz assignment.
4. [`RESOURCES.md`](RESOURCES.md) - primary sources. Add anything new there before citing it.
5. [`PLOT.md`](PLOT.md) - module order, what is written, and what is briefed but unwritten.
6. Two neighbouring lessons, plus the brief for your page in [`briefs/`](briefs/) if one exists.

## The rules that bite hardest here

- **Claim your lesson number through a brief before writing.** A brief in `briefs/NNNN-slug.md` is the register of who owns which number; two crews writing the same number is the one merge conflict this layout cannot absorb.
- **A stated proof for every named theorem, runnable NumPy/Pandas code for every named result**, on the same page, beside a picture before the formula and a problem after it. `MISSION.md` carries all six constraints; they are the bar.
- **Rows are samples, columns are features,** everywhere, for the whole course.
- **This course links to `statistical-foundations-ml-course` and never edits it.** Where the two overlap, pages here may point readers at the deck-faithful treatment there; nothing there points back, and neither re-derives the other. See the boundary paragraph in `MISSION.md`.
- **Regenerating a dataset must leave `git status` clean.** The generators in `code/` are seeded; a diff after regeneration is a bug in the generator, not a new dataset.
- **A planned page has no file.** It lives as a brief and as plain text in the `.roadmap`; linking a brief from any page fails the validator because the deploy excludes `.md`.

## Out of scope here

Machine learning itself, measure-theoretic probability, numerical analysis as a subject, statistical software tutorials, and deep-learning architectures.
`MISSION.md` owns the list and where each item is sent instead.
