# 0001 - Parallel authoring against a shared spec

**Date:** 2026-08-21
**Status:** Accepted

## Context

111 topics, each requiring a mechanism explanation, a named real-world example, three worked scale tiers, arithmetic, and several diagrams. That is far more than one author can produce at consistent quality in one pass, and a sequential pass would have taken long enough that the early chapters would drift from the late ones as the format settled.

## Decision

Author the eleven chapters in parallel, by eleven separate authors, against a single binding `BUILDER-SPEC.md` written before any chapter started. Each author was given only its own chapter's topic list with pre-assigned anchor ids, and was forbidden from touching any shared file.

An integrator wrote the course-level files - `index.html`, `MISSION.md`, `NOTES.md`, this record - and assembled the glossary afterwards from per-chapter fragments each author produced alongside its chapter.

## Why it works

- **Anchor ids were assigned up front, not chosen by authors.** This is what makes the glossary and the cross-chapter links resolvable without negotiation between authors who cannot see each other.
- **No shared file has two writers.** Each author writes exactly two new files. The integrator owns everything with more than one stakeholder. There is no merge conflict to resolve because there is no contested file.
- **The spec carries the format, so the authors only carry the content.** Section skeleton, quiz markup, diagram minimums, citation format, and the four-question topic shape were all fixed in advance.
- **Glossary fragments parallelise the one genuinely shared artifact.** Each author writes the table rows for its own topics; the integrator concatenates them in chapter order.

## Cost of this decision

Authors cannot link to each other's anchors, because they cannot verify anchors that do not exist yet. Cross-chapter links are therefore thinner than they would be in a sequential pass, and adding them is deliberate follow-up work for the integrator.

Authors also see a failing site validator while their siblings are still writing, since pager targets and the glossary do not exist yet. Each was told to expect this. A validator run is only meaningful after all chapters land.

## Revisit when

A future course needs cross-chapter linking dense enough that writing blind is the dominant cost. At that point, run the parallel pass for content and a second, cheaper pass purely for cross-linking, once every anchor exists and can be verified.
