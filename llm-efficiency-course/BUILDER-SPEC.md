# Builder spec - llm-efficiency-course

The course delta only: what is true of this course and not of the hub. Where this file contradicts the house skill, the skill wins.

## Extended-bar opt-in

This course is **opted into `EXTENDED_BAR_COURSES`** in `.claude/skills/course-authoring/scripts/check_pages.py`. Every content page therefore owes at least one practice problem (with `details.solution` and a `.p-check` sanity line) and at least one inline `svg.chart`. This is deliberate: the course asserts magnitudes, and a page that states a footprint or a rate without drawing it has made a claim it did not show.

## Derived-numbers rule

Every number on a page is either linked to a canon source or derived on the page with arithmetic shown and labelled as a derivation. No figure is presented as a measurement of GLM-5.3-Flash on desk hardware; none exists yet (see `RESOURCES.md` Gaps).

## Charts

Charts use the hub's inline `svg.chart` shapes. Chart text keeps under the ninety-character per-line bound at 640 width; every chart class that sets no paint rides on an `s-*` colour class.

## The lesson map

The map lives in `index.html`, and only there. Do not restate it here.

## Cross-linking

Cross-links to `llm-inference-course` lessons 0006 and 0007 use relative sibling paths (`../../llm-inference-course/lessons/...`). Verify an anchor exists in the target file before committing it.
