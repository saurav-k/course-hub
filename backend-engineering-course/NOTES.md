# Notes

How this course teaches, and what the authoring cost.
Read `MISSION.md` first for why it exists, then `BUILDER-SPEC.md` for what differs from the house
standard.

`MISSION.md` is the contract and changes rarely. This file is the working memory and should change
often.

## Learner profile

A working backend or platform engineer, two to eight years in the job. They ship services, but know
their framework faster than their fundamentals. They are fluent in writing code, not necessarily in
the vocabulary of why a system behaves as it does. They are not a beginner at thinking about systems,
so this course never talks down to them; it shows the mechanism underneath the framework.

A useful distinction: someone can be a beginner at *why a queue exists* while fluent at *writing a
task handler*. Those two take opposite tones - the first is taught, the second is assumed.

## Cadence

What one page is: 900-1,400 prose words, 3-5 diagrams across at least two kinds, 2+ active-recall
quizzes, one practice problem. The orientation figure on a page of this course draws where this
mechanism sits in the single connected request→fleet route, since that is the part every page shares.

A page ends when one mechanism is fully owned - mental model, mechanism, trade-off. The next page
develops the next mechanism in the sequence; the course never splits one idea across two pages.

Quizzes come after the idea is worked, which they should.

## Teaching preferences

The decisions that are this course's, not the house's.

- **A traced request is the through-line.** The orientation figure often shows the same request spine
  with this page's mechanism highlighted as a step in it.
- **Prefer sequence diagrams for order confusion and flowcharts for structure confusion**, per the
  house kind bar; skipped only when a genuinely quantitative claim needs a chart.
- **Both voices where it matters.** A concurrency page shows Go goroutines and Python asyncio; a
  serialization page shows Go struct tags and Python dataclasses.
- **What may be assumed:** the reader ships code and can read a status code. **What must be
  re-explained on every page:** the reason each tool exists, never the framework's flag list.

## Structure decisions

Why the page shape is what it is, and what was rejected.

The **lesson** shape was chosen over a chapter/reference shape because the source is a sequence (a
field manual read front to back) and the learner benefits from a connected route, not an index. A
reference-only version of this course was rejected: the reader can already look up tool flags; the
value is the connected why.

13 modules, first an on-ramp that traces one request before any mechanism is named. This was deliberate:
it gives the reader the whole map before module 02 starts unpacking individual mechanisms.

## Known gotchas

The things that cost an hour, so they cost the next author nothing.

- The source series' own diagrams are not to be reused; re-drawing from first principles means the
  illustration reflects this course's mental model, not a transcription.
- Concurrency examples in two languages balloon word count fast; keep each implementation to the lines
  that prove the mechanism, not a fuller app.
- Go and Python both need source links for behaviour claims about their runtimes; `RESOURCES.md` holds
  the canonical docs.
- A Mermaid `timeline` allocates a fixed width per event regardless of how short the label is, so it
  is the one kind whose overflow shortening does not fix. Measured while writing lesson 0800: four
  events rendered about 1,190px against an 856px figure, and cutting the label text moved it by 30px.
  Three events is what fits a reading column at desktop width. `hub.js` does give an overflowing
  figure a `tabindex`, so a wide one scrolls and is keyboard reachable rather than clipped.
- A `mindmap` and a `flowchart TB` both widen unboundedly across the reading column. Shortening the
  deepest labels is what pulls them back, and the number to check is the rendered `svg` width against
  the `figure` width rather than anything in the source.
- Codd's 1970 paper is paywalled on the ACM digital library and every mirror tried returned a 403, a
  404 or an unparsed PDF. Ground the relational model on the PostgreSQL documentation, which states
  the same properties in prose a lesson can quote, and leave the paper in `## Gaps`.

## Honesty notes

Where this course knowingly says less than the source claims, or more than the evidence supports.

- If a mechanism (e.g. cluster-consistent snapshots) is only waved at, say so in the page and point at
  the primary source rather than asserting a depth the course did not build.

## Open threads

- Whether a late module (fleet + scale) will want lab pages in the `llm-inference-course` lab-kit shape;
  the decision is deferred until that module is reached so it is not built on speculation.