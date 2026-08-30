# AGENTS.md - Statistical Foundations of Machine Learning

Instructions for AI coding agents working inside this course folder.
The repository root [`../AGENTS.md`](../AGENTS.md) still binds, and it wins wherever the two disagree.
This file adds only what is true of this course and nowhere else.

## What this course is

A deck-faithful expansion of the IIT Bombay lecture series *Statistical Foundations of Machine Learning* (Nikhil Karamchandani and D. Manjunath), written for one learner: a tech lead whose university probability has gone cold and who asked for near-zero cognitive load and many diagrams.
The course nests three levels deep: course map, lecture hub, one-idea page.
Lectures 1 to 5, TA Sessions 1 and 2, and Homework 1 are on the site, occupying lessons `0000` to `0076`; see [`PLOT.md`](PLOT.md) for the exact state and the true reading order.

## Read before you write

In this order:

1. [`MISSION.md`](MISSION.md) - why the course exists, for whom, and what is out of scope. It is canonical and was settled in a real interview; do not rewrite it as a side effect of other work.
2. [`NOTES.md`](NOTES.md) - how this course teaches: what "zero cognitive load" means here, the diagram policy, the colour meanings, and the gotchas.
3. [`BUILDER-SPEC.md`](BUILDER-SPEC.md) - the exact markup contract, including the required section skeleton for every content page.
4. [`RESOURCES.md`](RESOURCES.md) - the sources this course trusts. Add anything new there before citing it.
5. [`PLOT.md`](PLOT.md) - the true reading order and everything planned but unwritten. Place any new session by it.
6. Two neighbouring lessons. `lessons/0002-robust-summaries-mean-vs-median.html` is the gold template for a content page; `lessons/0000-lecture-1-start-here.html` shows the lecture-hub shape.

## The rules that bite hardest here

- **Deck numbers are quoted, never recomputed or improved.** A stated figure goes on the page inside `<span class="keynum">` exactly as the slide gives it. Where the deck is loose or does not recompute from its own table, say so in a `.callout.warn` rather than fixing it silently; `learning-records/0001-quoting-a-deck-that-does-not-recompute.md` records one full worked example of that decision, and `learning-records/0002-finishing-an-arithmetic-the-lecture-leaves-open.md` records the companion case, where the deck states no figure at all and this course derives one under its own name.
- **Never renumber anything.** Lecture 1 occupies lessons `0000` to `0008`, and every session since has taken the next free numbers in one continuous sequence. URLs are public.
- **A tutorial or TA session sits after the lecture it supports**, in both `index.html` and `PLOT.md`, never in a separate list at the bottom of the map.
- **Mermaid labels carrying maths need double quotes** (`A["P(X > 2000)"]`), line breaks are the entity `&lt;br/&gt;`, and a semicolon in a label breaks the diagram. This subject is full of parentheses; read the gotchas section of `NOTES.md` before drawing anything.
- **SVG charts use the semantic `.chart` classes, never hex values.** Teal is statistics, indigo is probability, green is signal, grey is noise, rust is the outlier or risk tail, on every page, in both themes.

## Out of scope here

Machine learning itself, measure-theoretic probability, proofs as ritual, and programming exercises.
The full list and the reasons live in `MISSION.md`.
Do not add model or training content because the title contains "machine learning"; that word names what this material is foundations *for*, and the other courses in the hub own the rest.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.
