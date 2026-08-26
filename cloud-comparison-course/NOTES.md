# NOTES - Comparing the Four Clouds

How this course teaches, and the gotchas specific to it.

## Voice

Big pictures, few words. A comparison lesson is a argument about a *difference*, not
a tour of four products: state the capability, show where the clouds diverge, explain
the reason for the divergence, and stop. Full prose throughout - no fragments.

## The matrix is the spine

`matrix.js` is the single source of truth for capability keys. Every lesson names
its rows from the taxonomy; no page may invent a capability name that is not a key
in `matrix.js`. When research mints a new key, it enters `matrix.js` first, with its
domain, and lessons follow.

## The four cell states are load-bearing

Unfilled ("not written yet"), absent (this cloud ships no equivalent, with the reason),
elsewhere (this cloud has the capability, inside a service listed on another row) and
filled (a service, linking vendor documentation) must never look alike or mean alike.
The widget styles them differently on purpose; an edit that makes two states look
similar is a bug even if it looks tidier.

Absent and elsewhere are the pair to guard. They both arrive as a `gaps` entry in the
same inventory and they make opposite claims, so a cell must never imply a cloud cannot
do something it demonstrably can: **NO EQUIVALENT is reserved for absent.** They are
told apart by the bar style, the hue and the tag word at once, because the hue alone
disappears in print and the tag alone is too quiet to read down a column of 191 rows.

## Evergreen discipline

No dates, countdowns, study schedules or exam references on any page - including
this course's map and the matrix itself. The one place dates belong is
`RESOURCES.md`, as provenance for sources.

## Gotchas

- The matrix renders only when three pieces agree: the `<figure class="cmatrix">`
  frame in `index.html`, this course's `matrix.js`, and the wiring in `assets/hub.js`.
  Changing any one without the others leaves an empty frame; check the page, not the
  console.
- Check the matrix in both render states - first paint and after a theme or palette
  change - and at phone width. It is the most dynamic thing on the hub.
- Vendor links rot between refreshes. Run `python3 scripts/validate_site.py
  --vendor-links` before opening a pull request that touches `matrix.js`.
- Quiz options match in length; Mermaid diagrams use `&lt;br/&gt;` entities and
  dashes - the two silent traps documented in the root `AGENTS.md`.
