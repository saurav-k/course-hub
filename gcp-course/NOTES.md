# NOTES - Inside Google Cloud

How this course teaches, and gotchas specific to it. It is a shell: notes here are
the standing instructions every future author inherits.

## Voice

Big pictures, few words; diagrams carry the meaning. Every lesson opens with an
orientation figure placing the page's idea inside the platform, states its one idea
as a claim, and works mental model, then mechanism, then trade-off. Full prose
throughout - no fragments.

## Platform vocabulary is taught once, then used

Terms GCP gives its own names get defined at first use and reused exactly after;
synonyms are never invented for the same object. When a term differs from the other
three clouds' word for the same idea, say so once and move on - the comparison
course owns contrasts.

## Evergreen discipline

No dates, countdowns, study schedules or exam references on any page. Facts that rot
(service limits, preview status) carry their source link and point at the vendor's
page as the live authority. Dates belong only in `RESOURCES.md`, as provenance.

## Gotchas

- Every lesson registers as a card in `index.html` and in the generated
  `outline.js`; `python3 scripts/gen_outline.py gcp-course` after adding one.
- Quiz options match within twelve characters; Mermaid line breaks are written
  `&lt;br/&gt;` and labels never contain semicolons - the two silent traps in the
  root `AGENTS.md`.
- New lessons append at the end of `PLOT.md`'s sequence; published lessons are
  never renumbered or renamed.
