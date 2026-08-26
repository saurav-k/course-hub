# BUILDER-SPEC - Inside AWS

The course delta only. The house standard is
[`.claude/skills/course-authoring/SKILL.md`](../.claude/skills/course-authoring/SKILL.md)
and it wins wherever this file is silent or behind.

## What differs from the house standard

- **Capability keys come from the shared taxonomy.** When a page names a capability
  (an object store, an L4 balancer), it uses the key defined in the comparison
  course's `matrix.js`, so cross-links between this course and
  [Comparing the Four Clouds](../cloud-comparison-course/index.html) stay exact.
- **Limits and status quo carry sources.** Quotas, previews and regional
  availability are stated only with a link to the vendor page that currently says
  so, phrased so the page survives the fact changing.
- **Diagrams over tables for structure.** The platform's own shapes - hierarchy,
  trust, flow - are drawn; reserve tables for genuinely tabular facts.

## Conventions specific to this course

- Course name in chrome: **INSIDE AWS**; footer prefix "Inside AWS".
- Canon is https://docs.aws.amazon.com/; anything else is labelled third-party at the point of use.
