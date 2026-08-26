# MISSION - Comparing the Four Clouds

## Why this course exists

Every vendor teaches its own platform in its own vocabulary, and every comparison
article online is a shallow table of service names that never says why two services
that look equivalent behave differently. A solution architect who works across more
than one cloud has nowhere to learn them side by side.

This course is that place. It takes one capability at a time - an object store, a
load balancer, an audit log - and asks all four major clouds to answer it, in one
shared vocabulary, on one page, with a link to each vendor's own documentation.

The course opens with the [capability matrix](index.html): every capability of the
shared taxonomy as a row, the four clouds as columns, filterable by area and
searchable by service name. The comparison lessons then take the rows a reader will
actually design against and explain the differences that names hide.

## Who it is for

An engineer or architect who already knows at least one cloud well enough to build
on it, and who wants the other three without reading four sets of documentation.
Ladder:

- **working** (`pill med`) - most pages: assumes cloud literacy, teaches the
  comparison directly.
- **foundation** (`pill easy`) - the orientation pages, including the matrix itself.

## What done looks like

After this course the learner can:

1. Take any capability from the taxonomy and name each cloud's answer to it, or say
   plainly which clouds have no equivalent (the matrix).
2. Explain why two nominally equivalent services differ, not just that they do
   (the lessons).
3. Choose a primary cloud for a workload with evidence rather than familiarity.

## What is out of scope

- **Deep single-cloud teaching.** Each per-cloud course in this category owns its
  own platform end to end. This course compares; it does not re-teach.
- **Unverified claims.** Every cell and every lesson is written only from verified,
  sourced research. Where research is still in flight, the page says so rather than
  guessing.
- **Pricing tables.** List prices rot fast and are each vendor's job to state. The
  course links vendor pricing pages and teaches cost *shape* instead.
- **Certification preparation as such.** The audience includes people studying for
  solution-architect exams, but no page carries exam drills, braindumps, study
  calendars, or anything time-bound.

## Shape and canon

The canon for every claim is the vendor's own documentation, linked from the very
cell or sentence that rests on it. The provenance discipline - what was read, when,
and what changed - lives in `RESOURCES.md`. The matrix data file (`matrix.js`) is
the single source of truth for the capability taxonomy; nothing else in the hub may
declare a capability key.
