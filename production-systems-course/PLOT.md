# Plot - the reading order of this course

This file records the true reading order of the course: where every chapter sits, and everything planned but unwritten.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order, and a tutorial or lab session that follows a lecture sits after that lecture in the course map, never in a separate list at the bottom.**
When this file and the course `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The sequence

The course is linear: eleven chapters, read in number order.
The chapters are grouped by the layer of the system they belong to - not alphabetically - so each one reads as a single argument.

| # | Position | Status | Notes |
|---|---|---|---|
| 1 | **Chapter 1 - Edge and Traffic Management** (`lessons/0000`) | written | |
| 2 | **Chapter 2 - Resilience Patterns** (`lessons/0001`) | written | |
| 3 | **Chapter 3 - Asynchronous and Event-Driven Systems** (`lessons/0002`) | written | |
| 4 | **Chapter 4 - Protocols and Real-Time Transport** (`lessons/0003`) | written | |
| 5 | **Chapter 5 - Database Performance** (`lessons/0004`) | written | |
| 6 | **Chapter 6 - Distributing Data** (`lessons/0005`) | written | |
| 7 | **Chapter 7 - Concurrency and Runtime** (`lessons/0006`) | written | |
| 8 | **Chapter 8 - Scale, Latency and Cost** (`lessons/0007`) | written | |
| 9 | **Chapter 9 - Delivery and Deployment** (`lessons/0008`) | written | |
| 10 | **Chapter 10 - Observability and Operations** (`lessons/0009`) | written | |
| 11 | **Chapter 11 - Security** (`lessons/0010`) | written | |

All 111 topics across the eleven chapters are written; chapter sizes are uneven by design, following the natural layer boundary rather than a quota.
There are no reserved positions.

## Planned but unwritten

- **A single-page scale cheat sheet**, pulling the three-tier verdict from every topic into one printable table. It is recorded in `NOTES.md` as the highest-value addition once the chapters settle. Reference sheets sit beside the sequence like the glossary does.
- **Learning records for the learner**, added when a chapter has been worked through and recall demonstrated, not on exposure.

A twelfth chapter would be a scope decision for `MISSION.md` first and a new row here second.

## Adding a session to this course

1. Read `BUILDER-SPEC.md`, `NOTES.md`, and an existing chapter first.
2. Take the next free lesson number. Never renumber anything.
3. A new chapter takes its place in this table and in `index.html` by layer order, which is the reading order. A new topic inside a chapter joins that chapter's list in place.
4. Re-run `python3 scripts/gen_outline.py production-systems-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py`, and open the changed pages in both themes before opening the pull request.
