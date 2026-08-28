# Mission

The record of the interview in `.claude/skills/course-authoring/new-course.md`.
This file is canonical: when a later authoring decision is argued, it is settled by re-reading this, not by re-deciding.

## Why this course exists

The learner is a Principal or Staff engineer with roughly twelve years in distributed systems who is now accountable for AI systems they did not train and cannot fully predict.
It is the same person the two sibling courses address, one role further along.

They may be assumed to have everything in `production-systems-course`, the mechanism level of `llm-papers-course`, and the build patterns of `agent-engineering-course`.
Assume also that they have shipped at least one AI feature and been surprised by it.

The cold spot is precise.
They can build the system and cannot yet defend the decision.
Specifically: they accept published numbers without reconstructing the harness that produced them, they hold no retirement calendar for the models running in production, and they have never written down what would make them stop.

The hub already answers everything else.
Lay it out by what a page answers rather than by its subject and the hole is one row wide.

| The reader's question | Who owns it |
|---|---|
| How does the mechanism work? | `llm-papers-course`, `math-for-ml-course` |
| How did we get here? | `llm-evolution-course` |
| How do I run it? | `llm-inference-course`, the five cloud courses |
| How do I build it? | `agent-engineering-course`, `coding-harness-course` |
| What do I say about it at a whiteboard? | `ai-system-design-course` |
| What does the substrate cost at each scale? | `production-systems-course` |
| **Should we do this, what will it cost us, how will we know we were wrong, and who has to agree?** | **this course** |

That last row is not a missing topic. It is a missing kind of page, and that is why it cannot be a chapter inside an existing course.

## The spine

**Every topic in this course is a decision, and every decision is answered in the same five fields.**

| Field | What it must contain | Why it is in the spine |
|---|---|---|
| **The call** | The decision in one sentence, phrased so that a reasonable person could choose either way | Stops a topic drifting back into being a mechanism explainer |
| **What you must know first** | The evidence required before the call can be made, and what that evidence costs to get, with links out to the course that teaches it | No number without its conditions |
| **The bill** | Money, latency, and team attention, including the recurring part | A recommendation with no price is not a recommendation |
| **How you find out you were wrong** | The signal, the lag before it appears, and who sees it first | The field nothing else in the discipline teaches |
| **The reversal** | What undoing it costs, and the point after which you cannot | Makes a two-way door and a one-way door visibly different objects |

The spine is structural, not a template to vary.
A topic that cannot be written with all five fields is the wrong topic and is cut.
The fourth field is the one that makes the course worth a staff engineer's time, and it never shrinks to a sentence.

## Success looks like

The learner can:

- Audit any published AI number back to its harness, its sample and its selection effects, and say what it does not show.
- Choose among a single call, a workflow and an agent with the bill for each written down before the choice is made.
- Name the signal that will tell them a choice was wrong, say how long it takes to arrive, and say who sees it first.
- Produce a model supply plan carrying retirement dates, a migration test and a named owner for the calendar.
- Write a decision record a successor can act on in eighteen months.

The failure that would still be a failure even if every page were accurate: **if it reads as a survey.**
The failure mode of this subject is a beautifully sourced page that leaves the reader with no way to decide anything on Monday.

## Structure

Chapter shape, matching both siblings so the three read as one library.
Nine chapters, one module each, plus three reference sheets.
Every topic is its own `<h3 id="...">` decision answered in the five fields, so a chapter doubles as a reference index during a design review.

Roughly 1,200 prose words per page, 1,800 the ceiling.
Five to six decisions per chapter.
Not routed: there is one reading order.

## The ladder

- **Foundation** (`pill easy`): chapters 0000 and 0001. Reading evidence, and whether to build at all.
- **Working** (`pill med`): chapters 0002 to 0006. Shape, knowledge, proof, cost, blast radius.
- **Frontier** (`pill hard`): chapters 0007 and 0008. Model supply as a dependency, and carrying an organisation through a decision.

Every chapter states the chapter it depends on, so the ladder is checkable by reading the map in order.

## Constraints

- **No mechanism, anywhere.** A page may name a mechanism in one sentence and must then link rather than explain. Zero paragraphs on attention, RoPE, MoE, LoRA, DPO, chain of thought or ReAct.
- **Every number arrives with its harness, its sample and its date.** A number without those is cut, not hedged.
- **Where a claim is a judgement it is attributed**: whose judgement, published where. Where it is this course's own, it says so on the page.
- **No vendor comparison tables.** They are stale on publication and never carry the case where the recommendation is wrong. The course teaches the criteria a reader applies to whatever exists when they read it.
- **No role or salary data.** No reliable 2026 source was found, so the course carries none.
- **Evergreen pages.** No study calendars and no countdowns. The only dates on a page are the dates a source carries, and provenance dates live in `RESOURCES.md`.

## Out of scope

| Excluded | Owner |
|---|---|
| Transformer, attention, RoPE, MoE, LoRA, RLHF, chain of thought, ReAct mechanism | `llm-papers-course` |
| Vision, generative and multimodal papers | `llm-papers-course`, as its own module |
| Serving engines, batching, quantization, KV eviction, load testing | `llm-inference-course` |
| Sharding, replication, queues, backpressure, circuit breakers, idempotency | `production-systems-course` |
| Classical web security: injection, identity, crypto, the browser boundary | `production-systems-course`, chapter 11 |
| MCP server authoring, permission postures, subagents, harness internals | `coding-harness-course`, `agent-engineering-course` |
| Trajectory evals, shadow testing, golden datasets, the data flywheel | `agent-engineering-course`, chapter 2 |
| Databases as a subject, cloud and DevOps as subjects | `production-systems-course`, the five cloud courses |
| Probability, estimators, confidence intervals | `statistical-foundations-ml-course`, `probability-you-build-course` |
| Interview technique | `ai-system-design-course` |
| Prompt-writing craft, framework tutorials, training and finetuning procedure | Nowhere, deliberately. Frameworks change; the decisions do not |
| The EU AI Act's substance | Nobody yet. Only its timeline has been researched; the substance needs its own round |

## Siblings

`agent-engineering-course/MISSION.md` already frames itself and `ai-system-design-course` as a pair: the build track and the interview track over overlapping material.
This course is the third member of that set.

- **Interview track**: what you would say at a whiteboard.
- **Build track**: what you would put in the repository.
- **Decision track**: what you put your name on.

Beyond those two it touches `llm-inference-course` for the sell side of inference cost, `production-systems-course` for the substrate, `llm-papers-course` for every mechanism, and `statistical-foundations-ml-course` for the statistics chapter 0004 leans on and refuses to re-teach.

## Revisit when

Two of this course's sources are vendor deprecation pages that change every few weeks, and chapter 0007 is built on them.
Reopen this file when that chapter is next touched, and re-fetch both pages before editing a word of it.
Reopen it also when the vision and multimodal module lands in `llm-papers-course`, because chapter 0003's multimodal decision should then link to a specific lesson rather than to that course's map.
