# Notes

How this course teaches, and what the authoring cost.
Read `MISSION.md` first for why it exists, then `BUILDER-SPEC.md` for what differs from the house standard.

`MISSION.md` is the contract and changes rarely.
This file is the working memory and should change often.

## Learner profile

A Principal or Staff engineer, roughly twelve years, strong distributed systems.
Fluent in databases, caches, queues, sharding, replication, backpressure, circuit breakers and idempotency.
Has shipped at least one AI feature and been surprised by it.

What reads as friction to this reader, in the order they will close the tab:

1. **A number with no harness and no sample.** This is the strongest single signal in the research behind the course. Semgrep's own dismantling of its own headline reached 1,113 points on Hacker News; the audience rewarded the caveats and not the number.
2. **A recommendation with no refusal.** If a page cannot say when to *not* do the thing, the page does not understand the thing well enough to teach it.
3. **Being told what an embedding is.** Define nothing a person who has shipped a distributed system already knows. Where a term must appear, link out and keep going.
4. **Advice that has never met an incident.** Every capability is taught alongside the incident it produces when it is wrong, and the containment that bounds it.

## Cadence

One page is a chapter: five to six decisions, each an `<h3 id="...">`, each answered in the five fields from `MISSION.md`, in that fixed order.

- Prose: about 1,200 words, 1,800 the ceiling. The five-field grid is most of it, so the connective prose between decisions is nearly zero by design.
- Figures: four or more, at least two kinds, and **one hand-authored `svg.chart` on every chapter**. This course states magnitudes constantly and Mermaid cannot draw one.
- The orientation figure on a page of this course draws the same three things every time: the chapter before it, this chapter's decisions as a group, and the chapter that consumes them. A `mindmap` suits it when the chapter indexes many decisions; a `flowchart` suits the rest.
- Quizzes: two or more, after the decisions are worked, never as a gate in front of them. They test judgement, not recall - the stem gives a situation and the options are four defensible-sounding calls.
- Practice: one or more, under `<h2>Practice</h2>`, after the quizzes. A practice problem here is arithmetic a staff engineer would actually do at a whiteboard: a minimum detectable effect, a cache break-even, a compounding-error budget, a notice-period calendar.

## Teaching preferences

- **The five fields are the page.** Do not vary them, do not reorder them, do not merge two of them into one paragraph. A reader comparing the retrieval decision with the self-hosting decision must be able to read the fourth field of each side by side.
- **The fourth field is the one that earns the course.** "How you find out you were wrong" is the signal, its lag, and who sees it first. If it reduces to "the metric moves", it has not been written.
- **Attribute every judgement.** Whose judgement, published where. Where the judgement is this course's own, the page says so in those words so a reader can argue with it.
- **Every number carries its harness and its sample.** 39% against 32% F1 is meaningless; 39% against 32% F1 on one IDOR detection task, one dataset, one run, with the open-weight models given nothing but a prompt, is a fact a reader can use.
- **A derived number shows its arithmetic and names its assumptions**, in an `ol.worked` or a `.math` gloss, so a reader can tell this course's derivation from someone else's measurement.
- Plain dash, never an em dash.
- Quiz options must match in length so formatting never leaks the answer.

## Structure decisions

- **Chapters, not micro-lessons**, matching both siblings so the three read as one library. A reader who has `ai-system-design-course` open in one tab should recognise the shape in the next.
- **Nine chapters** rather than five or fifteen. Fifteen would produce a course of which nine chapters restate a neighbour; the captain's topic list is an inventory of what a staff engineer must know and was never a table of contents.
- **The chapter to cut if the course ever has to shrink is 0002**, which has the most overlap with `agent-engineering-course`. Do not lose 0000 or 0007: they are the two nothing else on the hub covers.
- **No vendor comparison table anywhere.** The strongest argument for that rule is inside the course: OpenAI retired its own Evals platform and Agent Builder within six months of shipping them. A table ranking eval platforms would already be wrong.

## Known gotchas

Symptom first, then cause, then fix. The next author arrives with the symptom.

- **A diagram renders correctly, then turns into joined-up nonsense after the reader touches the appearance control.** Cause: a literal `<br/>` inside a `<div class="mermaid">`. `hub.js` stashes the graph source as `textContent` to repaint it, and `textContent` drops the `BR`. Fix: write `&lt;br/&gt;`. This is invisible on first paint, which is why every page here is checked in both render states.
- **A diagram is a red error box on first paint and nothing reaches the console.** Cause: `<pre class="mermaid">` instead of `<div class="mermaid">`. `hub.js` appends a copy button to every `<pre>`, so the word `copy` becomes the last line of graph source.
- **A quiz whose options mention money fails the twelve-character spread check** almost every time, because "$0.17 per finding" and "the harness" are different lengths before you notice. Draft the four options to a target length rather than trimming afterwards.
- **A `.q-fb` that explains only the right answer fails the checker's intent even when it passes the regex.** The strongest distractor in this course is a true statement that answers a different question, and the feedback is where you tell the reader which question it answered.
- **The word ceiling is reached faster here than in a normal chapter.** Six decisions times five fields is thirty paragraphs before a single word of connective prose. Five decisions is the comfortable number; six needs the fields kept to about forty words each.

## Honesty notes

Where this course knowingly says less than a source claims, or leans on evidence thinner than the claim, the page carries a `.callout.warn` saying so. The live ones:

- **Chapter 0000** carries METR's July 2025 result together with its February 2026 redesign, in which METR states its own newer data is "only very weak evidence for the size of this increase". Quoting the 2025 number without the 2026 update is the exact failure this course exists to prevent.
- **Chapter 0003** carries the Ramp build case with the note that the page has no author name and publishes no absolute accuracy, and the Anthropic contextual-retrieval ladder with the note that it is a vendor publishing a technique that sells its own model.
- **Chapter 0006** carries the AgentDojo caution: one 2026 source reports near-zero attack success on the newest frontier models with no defence at all, which the research could not confirm against a primary source. A benchmark that stops discriminating is not evidence of safety.
- **Chapter 0007** carries the model-drift paper with the methodological criticism the research could not adjudicate, and leans the operational claim on the corroborating Voiceflow observation instead. It also states that the 61-day Opus 4.1 window is arithmetic on Anthropic's published table and not a figure Anthropic states.
- **Chapter 0008** carries the Solver-and-Architect argument labelled as one scout's own proposition rather than a published finding, and notes that Will Larson's archetypes page carries no date this course could read.

## Open threads

- **The vision and multimodal module landed in `llm-papers-course` while this course was being written.** Chapter 0003's multimodal decision and its GraphRAG routing decision now link straight into lessons 0038, 0039, 0042 and 0045 there. If that course renumbers, those four links are the ones to re-check.
- **Two sources in chapter 0007 change every few weeks.** Anthropic's model deprecation page and OpenAI's deprecations page are the only canon entries that must be re-fetched every time the course is touched, or that chapter will be the first page in the hub to state something provably false.
- **No learning record yet.** Add one once a reader takes a chapter into a real design review and reports what it got wrong.
- **`reference/decision-record.html` has not been used in anger.** It is the artefact the course claims is its practical output, and nobody has filled one in for a live decision. The first person who does should record what the template missed.
