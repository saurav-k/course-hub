---
name: course-authoring
description: Authoring in this course hub. Use when creating a course, writing or rewriting a lesson or chapter, or checking a page against the house standard before a pull request.
---

# Course authoring

The house standard for every page published from this repository, and the procedure that produces one.

`AGENTS.md` is the contract and it still binds: it says who may push, what may not be renamed, what the shared design system will do to a page that gets its markup slightly wrong, and what "done" looks like for a pull request.
Read it first.
This skill says what a page must contain to be one of these courses rather than a page that merely lives beside them.

Seven courses were built before this skill existed and each carries its own `BUILDER-SPEC.md`.
Those files have drifted from one another and from the pages they govern.
Where a course's `BUILDER-SPEC.md` contradicts this skill, this skill wins and the contradiction is a bug to raise in the pull request.
A course's `BUILDER-SPEC.md` is now only the **course delta**: what is true of that course and not of the hub.

## Pick the branch

| You were asked to | Read |
|---|---|
| build a whole new course from a topic and an audience | [`new-course.md`](new-course.md) |
| add or rewrite one lesson in a course that already exists | [`new-lesson.md`](new-lesson.md) |
| retrofit an existing course to this standard | [`new-lesson.md`](new-lesson.md), one page at a time, plus [`retrofit.md`](retrofit.md) |

Read the branch file before you open an editor.
Every branch ends at the same gate: [`references/verify.md`](references/verify.md).

## The closed vocabulary

Every visual element on a page comes from [`references/widgets.md`](references/widgets.md), copied character for character.

There is one design system and one copy of it, `assets/hub.css` plus `assets/hub.js`, and it only styles and animates the class names it already knows.
A hand-rolled `<div class="tip-box">` is invisible styling on the day it ships and dead weight forever after, and a hand-rolled quiz shape does not bind to the click handler at all.

When a lesson genuinely needs a shape the catalogue does not have, add the shape to `assets/hub.css`, document it in `references/widgets.md`, and use it, all in the one pull request.
Adding to the vocabulary is welcome; using a word that is not in it is not.
Before you touch any selector, grep **every** `*.css` in the repository for it: three courses still carry an `assets/course-extras.css` layered after the hub sheet, and they restyle shared elements.

## The five ways a page breaks silently

Every one of these ships green, renders wrong, and reaches no console.
`AGENTS.md` carries the full mechanism; this is what an author has to hold.

1. **A Mermaid diagram is `<div class="mermaid">`, never `<pre class="mermaid">`.** `hub.js` appends a copy button to every `<pre>`, and Mermaid renders from the element's `textContent`, so a `pre` picks up the word `copy` as a final line of graph source and the figure becomes an error box.
2. **A Mermaid line break is written `&lt;br/&gt;`, never `<br/>`.** A literal `<br/>` is parsed into a real `BR` element, which `textContent` drops, so the first paint looks right and every repaint after a mode or palette change joins the two halves with no space.
3. **A semicolon in Mermaid text is a statement separator.** Measured against the Mermaid 11 the hub loads: in a `sequenceDiagram` the free text after a colon, in a message or a `Note over`, is parsed as a statement, and a semicolon there is a red error box. A flowchart label survives one, quoted or not. The house form is a dash everywhere, because the safe positions are not worth remembering.
4. **Check a page in both render states.** Defects of kind 1 are wrong on first paint; defects of kind 2 are wrong only after a repaint. Toggling mode or palette is what moves a page from one state to the other, and one state alone catches neither reliably.
5. **Counting SVGs proves nothing.** A Mermaid error box is itself an `<svg>`. Look at the figures, and match `.error-icon` when you check by machine.

## The teaching bar

[`references/pedagogy.md`](references/pedagogy.md) carries the standard as numbers you can count rather than qualities you can assert.
It is the difference between "diagram-heavy" and "three diagrams, two kinds, one of them quantitative".
Read it on every branch.

## Facts

Every technical claim carries a link to a source you fetched and read during this session.

A course is a teaching artefact, so a confident wrong explanation costs more than a missing one.
Where a figure is not in a source you can link, describe the effect qualitatively and name what drives it.
Where you derive a number yourself, show the arithmetic and label the assumptions, so the reader can tell your derivation from someone else's measurement.
