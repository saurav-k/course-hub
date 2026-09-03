# Builder spec - the delta for AI Software Developer

The house standard is `.claude/skills/course-authoring/`.
It carries the page contracts, the widget vocabulary, the teaching bar and the verification gate, and it governs this course as it governs every other.

This file carries **only what is true of this course and not of the hub**.
Where this file and the skill disagree, the skill wins, and the disagreement is a bug to raise in the pull request.

## The gold page

`lessons/0000-you-are-already-running-one.html`. Read it in full before writing anything else here.
It is the page every other page in this course is matched against, so a divergence from it is a decision to defend rather than an accident to leave in.

Four things about it are the course's shape rather than that page's own choices, and every page repeats them:

- **The orientation figure draws where the reader's hands are**, not where an idea sits in a taxonomy. What came before is the artefact the previous page had them write or read; what it enables is the next thing they can do.
- **Every page has a keyboard verb.** By the end, the reader has read something, written something, or run something. A page that leaves them knowing about a thing is unfinished.
- **Every quantity gets a hand-drawn `svg.chart`.** Mermaid cannot draw a distribution, a spread or a magnitude comparison, and this course states all three constantly.
- **A product is evidence for an axis, never the subject of a section.**

## What this course does differently

### Every configuration file is shown complete, and every sample carries a licence verdict

**This is the rule this course has that no other course in the hub has**, and it exists because the samples gallery redistributes other people's files.

Every artefact the course shows - `AGENTS.md`, `CLAUDE.md`, a hooks configuration, a `SKILL.md` and its script, an MCP server, a CI workflow, a scanner rule - appears **complete and runnable**, in a fenced block with a language tag.
A fragment with an ellipsis in it teaches nobody to write the file.

Every one of them is preceded by four facts, in this order, in the `.code-cap`:

```html
<div class="code-cap">AGENTS.md &middot; cloudflare/agents &middot; MIT &middot; reproduced verbatim</div>
```

1. **What it is**, including the filename it belongs at.
2. **Where it came from**, as a source the reader can open.
3. **Its licence**, named. Not "open source": the licence.
4. **The verdict**: `reproduced verbatim`, `paraphrased`, or the sample is not shown.

**A sample whose licence cannot be established is paraphrased or omitted.** Not shown with a hedge, and not shown with the licence field left vague.
"No LICENSE file in the repository" is an answer, and the answer is paraphrase.
Where a licence permits reproduction with attribution, the attribution is the `.code-cap` and it is not optional.

**This repository is the exception that costs nothing.** Its content is CC BY 4.0 and its code is MIT, so the course may quote its own repository in full - and `0410` does exactly that, against the vendor guidance it breaks.

The same four facts follow a sample into `reference/samples.html` unchanged, which is why they live in the caption rather than in prose beside it.

### Three labels, and the third one has a home

Every technical claim is one of three things and the page says which:

| Label | What it is | Where it goes |
|---|---|---|
| **KNOWN** | documented, or read in source at a pinned commit | ordinary prose, with the link |
| **INFERRED** | the author's reading of what the source implies | ordinary prose, saying whose reading it is |
| **MARKETING** | a vendor claim with no mechanism and no method shown | a `.callout.warn`, never anywhere else |

A number in a vendor's own announcement with no published method is MARKETING even when it is probably true.
The course quotes it, attributes it, and says what would have to be published for it to be evidence.

### Nothing on a page is dated

No dates, no schedule, no grading weights, no guest-lecture pages, and no "as of" hedges.

A version-sensitive claim carries **the version in the sentence**: "the `2026-07-28` revision removes the handshake", never "as of September this is true".
A protocol revision, a model id, a specification date used as a *name* and a pinned commit are all versions rather than dates, and all four are welcome.

A guest session in the syllabus is an **"in the field" lesson** built from that company's public primary material only.
A private lecture is never presented as if attended, and a person is named only as the author of public material the reader can open.

### The mechanism axis, and the test that enforces it

Every module names companies and every one of them ships fast.
**The test each page must pass: if the named product disappeared, would this page still be worth reading?**

The house form is to state the axis, then use the products as evidence for positions on it.
`0810-the-six-cloud-agents` is the type case: it is written on where the sandbox is, what triggers it and what it may write, with six products as the evidence, rather than as six product sections.
A section whose heading is a company name is almost always the wrong shape. The exceptions are the "in the field" pages, which are about that company on purpose.

### Cross-linking

Where a sibling course owns a mechanism, name the page and move on.
This is a defining constraint rather than a courtesy: `MISSION.md`'s out-of-scope table is what keeps this course from becoming a second copy of four others.

| What the reader is missing | Where to send them |
|---|---|
| How a harness is built inside | `../../coding-harness-course/lessons/NNNN-*.html` |
| How to run an agent system in production | `../../agent-engineering-course/lessons/NNNN-*.html` |
| Whether to build it at all, and what it costs | `../../staff-ai-course/lessons/NNNN-*.html` |
| Supervising a fleet from a terminal | `../../herdr-course/lessons/NNNN-*.html` |
| What a language model is | `../../llm-papers-course/`, `../../llm-evolution-course/` |

Two rules on top of that.
**Do not cross-link for completeness**: a link that only says "this exists elsewhere too" costs the reader a click and returns nothing.
**Verify an anchor before you commit it**: `validate_site.py` strips fragments and will not catch a dead one.

`PLOT.md` records the two links that are load-bearing in both directions - `0270` with `0900`, and `0160` with `coding-harness-course/lessons/0270-build-a-harness.html` - and neither half may be dropped by a later edit.

### The five interactive shapes

Five figure shapes a reader operates live are in the **shared** design system, available to every course with no course script: a stepper, an assembler, a calculator, a scorecard and a taint map.
They arrived for this course's sake, and this course does not own them. The reference is `.claude/skills/course-authoring/references/widgets.md`, "Five figures a reader operates", and `design-system/index.html` renders all five live with the markup beneath each.

**Each wears `.diagram` plus its own class** - `class="diagram stepper"`, never `class="stepper"` alone. A shape class on its own is a figure with no frame and an unstyled label, and `validate_site.py` check 19 fails it. The audit-era shorthand `figure.stepper` names the shape, not the markup.

Their data is markup: a step, a part, a row and a block is an element you wrote, so each one prints, is searchable, and is read by a screen reader before `hub.js` runs. Nothing persists.

They are the reason this course is lesson pages rather than chapters, so use them where they fit and **do not invent a sixth**.
A shape the vocabulary does not have is added to `assets/hub.css`, documented in `references/widgets.md`, and used, all in one pull request - which is the house rule, and it applies here with the extra weight that a hand-rolled widget in this course will look like one of the five and behave like none of them.

A technique picker is a `<details>` per failure and needs no widget at all. Reach for plain markup first.

## Numbering

Block numbering stepping by ten, with the full four digits written in the eyebrow, on the card and in the footer: `Lesson 0100`, never `Lesson 100`.
`PLOT.md` states the rule, the reason, and where a new lesson's number comes from.

## The lesson map

**The map lives in `index.html`, and only there.**

Do not restate it here. `index.html` is the deployed artefact, `validate_site.py` checks it, and `scripts/gen_outline.py` reads it to build the sidebar, so it is the copy that cannot silently drift.
`PLOT.md` carries the reading order, which is a different thing: it is where the capstone track's disagreement between file order and reading order is written down.
