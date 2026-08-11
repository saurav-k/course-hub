# 0001 - Chapters over micro-lessons

**Date:** 2026-08-11
**Status:** Accepted

## Context

The teaching default in this workspace is a short, tightly-scoped lesson: one idea, completable in a few minutes, sized to working memory. The other courses in the hub follow that shape.

This course was commissioned differently. The learner supplied a fixed syllabus of 111 topics across six pillars and asked for chapters covering all of them, with a reference link per topic.

## Decision

Organise as six chapters, one per pillar, each covering every topic in that pillar as its own anchored subsection.

## Why

- The stated mission is interview preparation, not first-time learning. The learner is a Principal engineer with twelve years of distributed-systems experience, so the binding constraint is coverage and recall, not cognitive load on unfamiliar material.
- A pillar is how the material is actually recalled under interview pressure. "Tell me about retrieval" is one question, not nineteen.
- Anchored subsections give the granularity a micro-lesson would have provided, without fragmenting the pillar into pieces that lose their relationship to each other.
- The glossary links to those anchors, so the course works in both directions: read a chapter to learn, jump from a term to revise.

## Cost of this decision

Chapters are longer than the workspace's usual lesson and exceed a single sitting. That is the accepted trade. Mitigations in place: a one-minute summary at the top of each chapter, and a print-friendly glossary that carries the whole syllabus in compressed form.

## Revisit when

The learner works through a chapter and reports that the length gets in the way of recall. At that point split the largest pillars into two chapters each, keeping every anchor id unchanged so the glossary links survive.
