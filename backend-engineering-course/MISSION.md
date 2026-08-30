# Mission

The record of the interview in `.claude/skills/course-authoring/new-course.md`.
This file is canonical: when a later authoring decision is argued, it is settled by re-reading this, not by re-deciding.

## Why this course exists

**The learner** is a working backend or platform engineer with two to eight years in the job.
They write working services every week, and they know their framework quicker than their fundamentals:
the request/response shape, the database, the queue and the deploy pipeline all "just work" and are
understood as folklore rather than as a connected design.

**What it may assume:** how to write and ship code in at least one language (the course teaches Go and
Python patterns when a mechanism needs an implementation), basic HTTP enough to have read a status code,
and the patience to trace a request across services on paper.

**The cold spot** is specific: a capable engineer who has never been shown why a REST API, a relational
store, a message queue and a horizontally scaled fleet are four answers to *four different questions*.
They know each tool as a catalogue entry and reach for whichever someone else recommended, not for the
one the load pattern actually demands.

So the on-ramp is genuinely from first principles: this course defines its own shape for a request, its
own account of statelessness, its own definition of a cache hit, and assumes no symbol the reader has
not been shown. Every module builds the connected picture that a framework hides.

## The source

The spine this course follows is the open field-manual series
[Backend from First Principles](https://github.com/DsThakurRawat/Backend-from-first-Principle) by
@DsThakurRawat, a 24-chapter reference on backend engineering (HTTP, routing, serialization, auth,
databases, caching, queues, search, error handling, gRPC, config, observability, graceful shutdown,
security, scaling, concurrency, containerization, testing, Kafka, and WebSockets).

This course is **derived** from that series: same subjects, same arc, same commitment to mechanism over
memorisation. The prose and every diagram are re-authored here from first principles and from the
canonical web sources those chapters cite; nothing is a transcription of the source text. The
attribution contract is in `RESOURCES.md`: the source is credited, and each page links the primary
source for its subject.

The source's numbers are a ceiling and its ordering is the default; where this course diverges it says
so under `PLOT.md`.

## Success looks like

The learner can:

- Trace what happens to a single request from socket to response, naming which layer owns what,
  for any framework they happen to be using.
- Choose between a relational store, a cache and a queue for a given load pattern, and say the
  trade-off that forced the choice.
- Explain why statelessness is what makes horizontal scale possible, and what breaks it.
- Design a resilient service: retries with backoff, timeouts, graceful shutdown, structured logs,
  and a blast-radius-reducing failure mode.
- Read a production incident and say which of these first principles was violated.

And the failure that would still be a failure even if every page were accurate: a learner who
finishes every page and still reaches for tools as a catalogue someone else curated, with no
ability to defend the choice to an engineer who asks why.

## Structure

The **lesson** shape: one idea per page, one claim per heading, held for the whole course.
One page is 900-1,400 prose words; figures, code and quizzes excluded.
13 modules, the first a single on-ramp page that reasons a request end to end before any
mechanism is named. Later modules develop each mechanism in teaching order.

## The ladder

The rungs, and what a learner arriving at each one already has.

- **Foundation** (`pill easy`): arrives cold. Every term is defined here or in a named earlier page.
- **Working** (`pill med`): has the foundation pages. Can be given a mechanism and a trade-off directly.
- **Frontier** (`pill hard`): has the working pages. Can be handed an open design question or a
  live disagreement (polyglot persistence, sharding, event sourcing).

Module 01 is foundation. Modules 02-09 work up from it. Modules 10-13 (scale, concurrency,
fleet, shipping) sit at working, with frontier questions at the end of the scale and flight modules.

## Constraints

The rules specific to this course that the house standard does not already carry.

- **Never let a framework become a black box.** When a page names a framework behaviour (an ORM, a
  DI container, a middleware chain), it names who owns the underlying mechanism, and never lets the
  framework stand in for the reason.
- **Go and Python are the two implementation voices**, matching the source series; a mechanism is
  only proven when it appears in both a typed and an untyped language. Keep both where a page needs
  an implementation; prefer whichever reads clearer when it does not.
- **Certainty is earned.** A claim about how a database, a queue or a browser behaves links the
  primary source that states it; an unsourceable claim goes to `RESOURCES.md` under `## Gaps`.

## Out of scope

What this course does not cover, and for each, the neighbour that owns it.

- **Any single framework or language's product docs** - neighbours: the framework's own
  documentation, linked at the point of use.
- **Cloud-provider specifics** - neighbours: [Inside AWS](../aws-course/index.html),
  [Inside Azure](../azure-course/index.html), [Inside GCP](../gcp-course/index.html),
  [Inside OCI](../oci-course/index.html). Those own platforms; this owns service design.
- **A full protocol catalogue** (every HTTP header, every status code) - that is reference, not
  sequence; this course teaches the ones that shape a design.
- **LLM/AI backend patterns** - neighbour: [Production Agent Engineering](../agent-engineering-course/index.html).

## Siblings

- [Inside AWS](../aws-course/index.html), [Inside Azure](../azure-course/index.html),
  [Inside GCP](../gcp-course/index.html), [Inside OCI](../oci-course/index.html) - the platforms a
  service this course teaches will run on. Linked when a mechanism's deployment is the point.
- [Production Systems](../production-systems-course/index.html) - a different shape for the same
  reader: topics at three scales. This course builds a connected route; that one indexes the territory.
- [Backend from First Principles](https://github.com/DsThakurRawat/Backend-from-first-Principle) -
  the upstream source, credited, not owned.

## Revisit when

A module is finished, the source series ships a chapter this course treats as a gap, or a learner
report says the ladder's assumption (foundation → working → frontier) stopped holding.

