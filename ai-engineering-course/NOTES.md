# Notes

How this course teaches, and what the authoring cost.
Read [`MISSION.md`](MISSION.md) first for why it exists, then [`BUILDER-SPEC.md`](BUILDER-SPEC.md) for what differs from the house standard.

`MISSION.md` is the contract and changes rarely.
This file is the working memory and should change often.

## Learner profile

They write Python competently and have shipped services. They are not beginners at thinking, and they are beginners at nothing in this course except measurement.

What reads as friction: being told what RAG stands for, being walked through `pip install`, being handed a framework tour.
What lands: an arithmetic they can do on their own numbers, a trace they can read, a defect they can reproduce and then fix.

The sentence to keep in mind while writing: **they already believe the lever is the prompt wording.** Every module 1 and module 2 page is, underneath, an argument that the lever is somewhere else and here is the number that shows it.

## Cadence

One page is 900 to 1,400 prose words, 1,800 the ceiling. Three to five figures, two quizzes, one practice problem with a `details.solution` and a `.p-check`, and at least one inline `svg.chart`.
One interactive figure wherever there is a state, a budget, a file, a score or a boundary to manipulate, which is nearly every page here.

**The orientation figure on a page of this course draws where the reader's hands are on the pipeline.** What came before is the artefact the previous page had them build or measure; what it enables is the next thing their own system can do. It is hand-drawn, never Mermaid: its job is to say what is *where*.

Quizzes come after the idea is worked, never before. The practice problem is the module's increment to the capstone, so the reader who does every practice problem has built the application.

## Teaching preferences

- **Every page ends with a number or an artefact in the reader's own repository.** A page that leaves them knowing about a thing is unfinished. This is the course's whole claim over its concept-first siblings.
- **State the arithmetic, then draw it.** Mermaid cannot draw a distribution, a spread or a magnitude comparison, and this course states all three constantly.
- **A tension is presented as a tension.** Where two primary sources disagree - semantic chunking against contextual embeddings, top-20 against the middle of a long context, reflection with and without an external signal - the page states both with their bills and tells the reader to run both on their own thirty questions. Do not rank them.

## The rules that came out of the research, and are rules rather than habits

### The number moved

**No lesson in module 2 ships without stating what it changed on the reader's own golden set**, and the module's capstone page must carry at least one row with a zero or a negative delta.

This is the single strongest defence against the failure `MISSION.md` names: the course becoming a tour of techniques. A capstone in which every idea worked is a capstone the reader faked.

### Link the counterpart, do not re-frame it

**Every foundations and retrieval-quality lesson links its counterpart section in `../ai-system-design-course/lessons/0001-rag-and-retrieval.html`.**

Nineteen of module 1 and module 2's topics appear there as concept entries. The link is what makes "we teach it hands-on, they frame it" true rather than asserted, and it is the same discipline `ai-software-developer-course` keeps with `coding-harness-course`.
Verify the anchor exists before committing it: `validate_site.py` strips fragments and will not catch a dead one.

### A semantic-convention attribute carries its status and its revision

**Every page that quotes an OpenTelemetry GenAI attribute names the convention's Development status in the same paragraph.**

The GenAI semantic conventions live in `open-telemetry/semantic-conventions-genai`, which has **no releases and no tags**, and every document in it is marked *Status: Development*. They also moved: the old page under `opentelemetry.io` is now a redirect notice.
What the course commits to is the *shape* - one span per stage, the query and the document scores recorded - and a rename is a rename of attribute constants in one file.

The same rule has a second half, and it is why it is one rule rather than two: **a page also names the specification revision it is instrumenting**, because the convention and the specification can disagree and now do. The OTel MCP convention's own examples still show `initialize` and `mcp.session.id`, both of which MCP `2026-07-28` removed.

### Open the artefact, do not fetch a summary of it

**Any lesson citing a paper's named list, table or section headings is written with the PDF open.**

Two of the fifteen lessons in the `aie-ops` slice rest on numbers read out of a PDF *after* an automated summary of the same PDF returned invented content. A summary that fabricates a table is indistinguishable from one that does not until you open the artefact.

### Two lessons are narrowed, and the narrowing is the brief

- **`0440`, the MCP lesson, is the host side and nothing else.** `../ai-software-developer-course/lessons/0240-mcp-in-one-page.html` is already written against revision `2026-07-28` and is correct on the stateless redesign, and `0250-write-your-first-mcp-server.html` walks a reader through writing a server in two languages. A third MCP explainer here is the duplication `MISSION.md` exists to prevent.
  The brief is: *your RAG application as a host, what a mounted retrieval tool promises, what its annotation defaults claim, and the `mcp.*` spans across the boundary*. The protocol itself is out of scope and linked in the first paragraph.
- **`0280`, the prompt-injection lesson, is the retrieved document as untrusted input and nothing else.** Agent permissions, capability containment and multi-tenant isolation belong to `0650` and to `staff-ai-course`. This page owns the seam the model cannot see: retrieved text arriving inside a prompt the reader wrote.

### The pager the writer of the previous module cannot fix

**The "next" link on the last page of module `N-1` is the integrator's edit.**

Adding module `N` changes it, so two slices are not independent even when their lesson blocks are disjoint. Either leave it to the integrator or make it the first act of your own branch and say so in the pull request. Do not both do it.

## Structure decisions

- **Module 2 is nine lessons against six syllabus bullets**, because two of its bullets each carry two independent mechanisms with different evidence and opposite cost profiles: chunk boundaries against injected context, and rank fusion against second-pass scoring. Four pages at 2,000 words was the alternative.
- **Module 1 spends three lessons on the observability and evaluation thread** rather than two, because every later module re-runs that harness and a thread the reader half-learned is a thread nobody uses.
- **Module 6 is eight lessons and is the heaviest module.** If it ever has to shrink, the cut is `0640` folded into `0630` as a fifth beat, and that trades away the best-evidenced lesson in the slice.
- **Module 8 is deliberately small**, three lessons for three bullets, because two of its bullets are checklists rather than mechanisms and one is the conversion of a cohort event.
- **`0360` needs the captain's eye before it is written.** It is the one page that hands the reader two peer-reviewed papers that disagree, and the reconciliation is the author's reading rather than either paper's claim. It is also the page most likely to be quietly wrong in a way no validator catches.

## Known gotchas

Written symptom first, because that is how the next author arrives.

- **A figure looks right on first paint and joins two words after the reader changes the palette.** A literal `<br/>` inside a `<div class="mermaid">` is parsed into a real `BR` element, which `hub.js` drops when it stashes the graph source as `textContent` to repaint. Write `&lt;br/&gt;`. This course's diagrams are full of two-line labels, so it will happen here.
- **A Mermaid figure is a red error box and the source looks fine.** A semicolon in free text is a statement separator. Every span attribute this course quotes is fine, but `top_k; k=10` is not. Use a dash.
- **A hand-drawn label's tail is simply gone.** SVG text neither wraps nor is bounded by the `viewBox`, and the browser clips at the frame edge. At the `640` width these charts use, a `.lbl-sm` line runs out of room past about ninety characters. This course writes long attribute names into figures, so split them across two `<text>` elements.
- **`.ref` alone draws nothing.** It sets a dash pattern and a width, not a stroke. Write `class="s-signal ref"` when you draw a reference line, which this course does constantly for a threshold or a baseline.
- **The figure label and claim render as body text.** `.fig-cap` and `.fig-claim` must be direct children of `figure.diagram`. One wrapped in a `div` for spacing takes no styling and validates green.

## Honesty notes

Where the course knowingly says less than a source claims, each one belongs in a `.callout.warn` on the page that carries it.

- **Every vendor figure is that organisation's measurement on its own corpus.** The contextual-retrieval failure-rate ladder, the multi-agent token multipliers, the internal research-eval win rate, and the text-to-SQL adoption numbers are all evidence that an effect is real and none is a target. Say so in the sentence that quotes them.
- **Three claims could not be verified in research and must not be asserted until somebody opens the artefact**: the "only a small fraction of a real ML system is ML code" figure, the three confidence labels of corrective RAG, and the nine stage names of the ML workflow. `RESOURCES.md` carries the full `## Gaps` list.
- **The judge's agreement with hand-scoring is the confidence interval on every automated number in the course**, and `0170` says so. No later page may quote a judge score as if it were a measurement.

## Open threads

- `RESOURCES.md` and `reference/glossary.html` are seeded, not written. The integrator completes both after the eight modules land.
- Three reference sheets are reserved and unwritten: `eval-harness.html`, `troubleshooting.html`, `figures.html`.
- `0560` is held rather than free. See `PLOT.md`.
- Nobody has yet checked whether the fallback corpus - this repository's own content - actually produces interesting retrieval failures at the size a reader will ingest. The module 1 writer finds out first.
