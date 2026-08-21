# Notes

## Learner profile

- Principal engineer, twelve years, strong distributed-systems background.
- Knows the vocabulary. Needs the trade-offs, the arithmetic, and the scale boundaries.
- Do not slow-walk fundamentals; do not skip the maths.

## Teaching preferences

- Mental model, then mechanism, then real example, then the three scale tiers, then the failure mode.
- Every technical claim carries a citation. Parametric memory is not a source.
- Plain dash, never an em dash.
- Quiz options must match in length so formatting never leaks the answer.
- Diagrams are not decoration. Aim for six or more per chapter.

## Structure decisions

- Eleven chapters grouped by the layer of the system they belong to, not alphabetically, so a chapter reads as one argument.
- The three-tier spine (100 / 1,000 / 10,000 requests per second) is mandatory per topic. It is what makes the course different from a glossary.
- Chapters were authored in parallel by separate authors against a shared `BUILDER-SPEC.md`. That spec is the reason they read as one course; keep editing it rather than letting chapters drift.

## Open threads

- Chapter sizes are uneven by design (8 to 13 topics), following the natural layer boundary rather than a quota.
- No learning records for the learner yet. Add one when a chapter has been worked through and recall demonstrated, not on exposure.
- A single-page "scale cheat sheet" pulling the three-tier verdict from every topic into one printable table would be the highest-value addition once the chapters settle.
