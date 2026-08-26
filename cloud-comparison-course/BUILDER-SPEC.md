# BUILDER-SPEC - Comparing the Four Clouds

The course delta only. The house standard is
[`.claude/skills/course-authoring/SKILL.md`](../.claude/skills/course-authoring/SKILL.md)
and it wins wherever this file is silent or behind.

## What differs from the house standard

- **The capability matrix is a first-class widget.** Its markup is documented in
  `references/widgets.md` under "The capability matrix" and its data lives in
  `matrix.js` beside this file. An author never hand-writes matrix rows in HTML;
  the widget renders them from the data file, and `scripts/validate_site.py` gates
  the data.
- **No lesson may cite a capability that is not a key in `matrix.js`.** If research
  needs a new key, add it to the taxonomy in `matrix.js` (with its domain) in the
  same pull request as the lesson.
- **Every filled cell carries its vendor link.** A service cell without a working
  link to that vendor's own documentation fails validation; do not ship one.
- **Comparison pages carry a provenance line.** Each lesson names which sources it
  rests on, with the read date, and links `RESOURCES.md`.

## Conventions specific to this course

- Course name in chrome: **FOUR CLOUDS COMPARED**; footer prefix "Comparing the
  Four Clouds".
- Cloud order everywhere is AWS, Azure, Google Cloud, OCI - column order in
  `matrix.js`, and the order every table and diagram follows.
  **Mermaid places sibling subgraphs in reverse**, so a figure that puts one cloud
  per subgraph has to be declared backwards to render in that order, with a `%%`
  comment saying why. Read the rendered figure rather than the source: the source
  reads OCI-first and the page reads AWS-first, and that is correct.
- The four per-cloud sibling courses own their platforms' depths; link out to them
  rather than re-teaching.
