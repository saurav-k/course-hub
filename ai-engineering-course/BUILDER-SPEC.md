# Builder spec - the delta for End-to-End AI Engineering

The house standard is `.claude/skills/course-authoring/`.
It carries the page contracts, the widget vocabulary, the teaching bar and the verification gate, and it governs this course as it governs every other.

This file carries **only what is true of this course and not of the hub**.
Where this file and the skill disagree, the skill wins, and the disagreement is a bug to raise in the pull request.

## The gold page

`lessons/0000-your-demo-works-and-you-cannot-prove-it.html`. Read it in full before writing anything else here.
It is the page every other page in this course is matched against, so a divergence from it is a decision to defend rather than an accident to leave in.

Four things about it are the course's shape rather than that page's own choices, and every page repeats them:

- **The orientation figure draws where the reader's hands are on the pipeline**, hand-drawn rather than Mermaid, because its job is to say what is *where*.
- **Every page ends with a number or an artefact** in the reader's own repository, and the practice problem is that page's increment to the capstone.
- **Every quantity gets a hand-drawn `svg.chart`.** This course is on the extended bar, so that is a floor rather than a preference.
- **Every figure with a state, a budget, a file, a score or a boundary in it gets one of the five interactive shapes.** The reader moves something on nearly every page.

## What this course does differently

### The measurement rule

**Every technique in modules 2 and 4 is introduced with a number the reader can move, and the lesson says what moved.**

The house standard asks that every technique carry its cost. This course asks for one thing more: the page names the metric, on the reader's own golden set, that the technique is supposed to change, and the hands-on act is the measurement rather than the implementation.
A module 2 lesson whose hands-on act ends at "and now you have hybrid search" has not finished; it finishes at "and recall@10 went from 0.61 to 0.68, or it did not, and here is what to check next".

The strong form of the rule lives in [`NOTES.md`](NOTES.md) under **The number moved**, and the module 2 capstone page owes at least one row with a zero or negative delta.

### The provenance rule for a number

**Every quantity on a page is one of three things and the sentence says which.**

| Kind | What it is | How it is written |
|---|---|---|
| **Measured here** | the reader's own run, or arithmetic this page performs | show the arithmetic, label the assumptions |
| **Published, on somebody else's corpus** | a vendor's or a paper's measurement | name the measurer and the corpus in the same sentence; it is evidence that an effect is real, never a target |
| **Derived** | this course's arithmetic over somebody else's inputs | state both inputs and the operation |

A vendor number printed bare, without its measurer, becomes a target the first time a reader quotes it back.
The three lists a reader would expect and this course does not assert are in `RESOURCES.md` under `## Gaps`.

### A version is a name, and a date is not

No dates on pages, no schedule, no grading weights, no cohort.
A version-sensitive claim carries **the version in the sentence**: "revision `2026-07-28` removes the handshake", never "as of September this is true".
A protocol revision, a model id, a pinned commit and a package version are all names, and all four are welcome.

This course carries more version-sensitive claims than any of its siblings, and one of them is unusual enough to be a rule of its own: **an OpenTelemetry GenAI attribute is quoted with the convention's Development status and the specification revision it instruments, in the same paragraph.** [`NOTES.md`](NOTES.md) has the mechanism.

### The provider swaps in one place

Reference code is Claude API first and Gemini second, and every sample is written so that changing provider is one edit.
Where the two vendors' mechanisms genuinely differ - a `strict: true` tool `input_schema` against a documented subset of JSON Schema - show both and teach the shape they agree on.

Reference code stays framework-light: the provider SDK, Pydantic, one vector database, LangGraph for agent graphs, and the official MCP and A2A SDKs.
Everything else is evidence for a concept, pinned to a version in the sentence, and never the subject of a lesson.

### Cross-linking

Where a sibling course owns a mechanism, name the page and move on.
This is a defining constraint rather than a courtesy: `MISSION.md`'s out-of-scope table is what keeps this course from becoming a second copy of four others.

| What the reader is missing | Where to send them |
|---|---|
| The whiteboard framing of retrieval, cost, evaluation and trust | `../../ai-system-design-course/lessons/0001-rag-and-retrieval.html` and its siblings |
| MCP as a protocol, and writing a server | `../../ai-software-developer-course/lessons/0240-mcp-in-one-page.html`, `0250-write-your-first-mcp-server.html` |
| The agent loop in twelve lines | `../../ai-software-developer-course/lessons/0110-the-loop-in-one-picture.html` |
| Context engineering across the turns of a loop; durable state and resumption | `../../agent-engineering-course/lessons/0000-context-and-protocol.html`, `0002-state-async-and-degradation.html` |
| Trajectory evals and shadow testing, concept-first | `../../agent-engineering-course/lessons/0001-evaluation-and-the-data-flywheel.html` |
| Prefix caching inside the serving engine, quantization, serving economics | `../../llm-inference-course/` |
| Retries, circuit breakers, queues and general scaling | `../../production-systems-course/`, `../../backend-engineering-course/` |
| Whether to build it at all, and who owns the gate | `../../staff-ai-course/` |

Two rules on top of that.
**Do not cross-link for completeness**: a link that only says "this exists elsewhere too" costs the reader a click and returns nothing.
**Verify an anchor before you commit it**: `validate_site.py` strips fragments and will not catch a dead one.

### The five interactive shapes

The stepper, assembler, calculator, scorecard and taint map are in the **shared** design system and this course writes no JavaScript to use one.
The reference is `.claude/skills/course-authoring/references/widgets.md`, "Five figures a reader operates", and `design-system/index.html` renders all five live with the markup beneath each.

Each wears `.diagram` plus its own class - `class="diagram stepper"`, never `class="stepper"` alone.

One constraint this course meets more often than its siblings: **the calculator has exactly two operations, `product` and `scale`, and no exponentiation.** Anything that needs a power - `pass^k` is the case that came up - is drawn as an `svg.chart` from the source's own figures. Adding an operation is a three-part pull request against the shared system, never a page-level workaround.

**Do not invent a sixth shape.** A hand-rolled widget here will look like one of the five and behave like none of them.

## Numbering

Block numbering stepping by ten, with the full four digits written in the eyebrow, on the card and in the footer: `Lesson 0100`, never `Lesson 100`.
[`PLOT.md`](PLOT.md) states the rule, the reason, the eight registration blocks and where a new lesson's number comes from.

## The lesson map

**The map lives in `index.html`, and only there.**

Do not restate it here. `index.html` is the deployed artefact, `validate_site.py` checks it, and `scripts/gen_outline.py` reads it to build the sidebar, so it is the copy that cannot silently drift.
[`PLOT.md`](PLOT.md) carries the reading order, which is a different thing: it is where the capstone track's disagreement between file order and reading order is written down.

## This course declares one token

`--course-hue: 136`, and nothing else, in the course-contract block of `assets/hub.css`.
The measurement behind the number is `learning-records/0001-choosing-the-hue.md`.
**This course ships no stylesheet of its own**, and no course gets a fourth `course-extras.css`.
