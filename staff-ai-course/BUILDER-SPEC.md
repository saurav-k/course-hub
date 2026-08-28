# Builder spec - the delta for The Staff AI Engineer

The house standard is `.claude/skills/course-authoring/`.
It carries the page contracts, the widget vocabulary, the teaching bar and the verification gate, and it governs this course as it governs every other.

This file carries **only what is true of this course and not of the hub**.
Where this file and the skill disagree, the skill wins, and the disagreement is a bug to raise in the pull request.

## The gold page

`lessons/0000-reading-the-claim.html`. Read it in full before writing anything else here.
It is the page every other chapter is matched against, so a divergence from it is a decision to defend rather than an accident to leave in.

## What this course does differently

### The five-field grid is the required section shape

A chapter indexes decisions. Every decision is an `<h3 id="kebab-case">` stating the decision, followed by exactly five paragraphs, in this order and with these bolded openers, verbatim:

```html
<h3 id="model-or-harness">Is this number about the model, or about the harness?</h3>
<p><b>The call.</b> ...</p>
<p><b>What you must know first.</b> ...</p>
<p><b>The bill.</b> ...</p>
<p><b>How you find out you were wrong.</b> ...</p>
<p><b>The reversal.</b> ...</p>
```

No new CSS: this is ordinary prose markup, so it survives every mode, every palette and print without a single rule of its own.

Four rules about the grid:

- **Order is fixed.** A reader comparing two decisions reads the fourth field of each side by side, and that only works if the fourth field is always fourth.
- **Nothing is merged.** Two fields in one paragraph is a decision that was not thought through.
- **The fourth field carries the signal, the lag, and who sees it first.** All three. "The metric moves" is not a fourth field.
- **A topic that cannot fill all five is cut**, and the reason it could not is worth a line in `RESOURCES.md` under `## Gaps`.

Source links sit inside the field that rests on them, in the house form `<em>Source: <a href="...">Publisher, "Title"</a>.</em>`, not collected at the end of the decision.

### Numbers

Every number on a page carries its harness, its sample and its date in the same sentence or the sentence beside it.
The house form is `<span class="keynum">` for a figure quoted from a source and plain text for a figure derived here, and this course leans on that distinction harder than any other, because half its argument is that readers do not check which is which.

A derived number shows its arithmetic in an `ol.worked` or a `.math` gloss and names its assumptions.

### Judgements

A judgement is attributed on the page: whose, and where they published it.
A judgement that is this course's own says so in those words - "this course's own reading" or "the course's own proposition" - so a reader can argue with it rather than absorb it.

### One chart per chapter

Every chapter carries at least one hand-authored inline `svg.chart`.
This course states magnitudes constantly - error bars, price spreads, notice periods, attack success rates - and Mermaid can draw none of them.
The chart classes are the hub's closed semantic set; never a literal hex.

Two fixed meanings hold across the whole course, so a reader can read a figure before reading its caption:

- `m-alarm` and `s-alarm` mark **the number that is worse than it looks**: the noise floor, the undefended baseline, the cost you did not budget for.
- `m-stat` and `s-stat` mark **the measured value being reported**.

### The chapter close

Every chapter ends with a **decision drill** before the teacher note: five questions a reviewer will put to a design, each with the trap inside it, phrased as `<b>"The question."</b> The trap is ... Answer with ...`.
`agent-engineering-course` calls its version a field drill and asks what a reviewer asks about a system you are going to run. This one asks what a reviewer asks about a decision you are going to sign.

## The lesson map

**The map lives in `index.html`, and only there.**
Do not restate it here. `scripts/gen_outline.py` reads it to build the sidebar and `scripts/validate_site.py` checks it, so it is the copy that cannot silently drift.

## Cross-linking

Every mechanism question links out. That is the course's defining constraint, not a courtesy.

| What the reader is missing | Where to send them |
|---|---|
| How a mechanism works | `../../llm-papers-course/`, the specific lesson |
| How to build the shape | `../../agent-engineering-course/lessons/NNNN-*.html#anchor` |
| What to say about it at a whiteboard | `../../ai-system-design-course/lessons/NNNN-*.html#anchor` |
| How to serve it, and what a rented GPU costs | `../../llm-inference-course/lessons/NNNN-*.html` |
| The substrate under all of it | `../../production-systems-course/lessons/NNNN-*.html#anchor` |
| The statistics chapter 0004 refuses to re-teach | `../../statistical-foundations-ml-course/`, `../../probability-you-build-course/` |

Inherit `agent-engineering-course/NOTES.md`'s rule verbatim: **do not cross-link for completeness.** A link that only says "this exists elsewhere too" costs the reader a click and returns nothing.

Verify an anchor exists in the target file before you commit it: `validate_site.py` strips fragments and will not catch a dead one.
