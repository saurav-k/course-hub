# Mission

The record of the interview in `.claude/skills/course-authoring/new-course.md`.
This file is canonical: when a later authoring decision is argued, it is settled by re-reading this, not by re-deciding.

## Why this course exists

**The learner** is a working software engineer with three to fifteen years in the job who uses a coding agent every day and has never looked inside one.

**What may be assumed without teaching:** shell, git, HTTP APIs, what an LLM is, and what a tool call is at surface level.
Prompt engineering and transformer internals are not taught here and not needed.

**The cold spot:** they believe a coding harness is a thin wrapper around a model API - that the harness is a chat box plus a diff viewer, and all the capability lives in the model.
It is not, and every page erodes that belief with evidence: named files, named functions, measured token budgets, and the same model behaving differently under two harnesses.

## The source

The spine is the epic filed on this repository: issues #123 and #125 through #151, twenty-eight issues whose numbering IS the page numbering (`#124` names lesson 0000 and is folded into #123's scaffold).
Underneath the spine sits the canon of record: sixteen first-hand architecture reports, one per harness plus one on the model layer beneath all of them - ten read at a pinned commit in their own source, five covered from official documentation only because they are closed, and one catalog study.
Those reports are working material, not published pages, so a lesson cites the public source behind each claim (the repository at its pinned commit, or the official documentation) and never cites a report by path.

## Success looks like

The learner can:

- Trace any harness's turn cycle from source, naming where input becomes context becomes a model call becomes tool dispatch becomes a result.
- Predict what a given harness puts into the context window, and in what order, before reading its code.
- Choose a permission posture for an agent they deploy - ask, sandbox, classify, or nothing - and defend it against the failure modes of the other three.
- Read an unfamiliar harness codebase and find its loop, its tool surface, and its context assembly within an hour.
- Explain why a harness performs differently on a different model family, in terms of tool-call encoding and prompt-format fit rather than folklore.

And the failure that would still be a failure even if every page were accurate: **a feature comparison grid**.
A reader who finishes able to recite which tool has which feature, but unable to reason about a design they have not seen, has been given a table where a mechanism was owed.

## Structure

Lesson grain, twenty-eight pages, one module per concern, single linear order.
NOT a routed course: there is genuinely one order, and `gen_outline.py` runs against it normally.

Page length: 900 to 1,400 prose words typical, 1,800 ceiling.
This course leans harder on figures than any other in the hub - diagram-led is a design decision, not an aspiration - so most pages sit nearer the bottom of the word range with four to six figures doing the carrying.

| Module | Pages | Concern |
|---|---|---|
| Orientation | 2 | what a harness is; the design principles underneath |
| The loop | 3 | turn cycle, context engineering, the edit problem |
| Trust | 2 | permission postures; identity and supply chain |
| Extending | 3 | MCP; skills, subagents, hooks and modes; code mode |
| Models | 2 | per-family affinity; compatibility endpoints |
| Deep dives | 15 | one harness each, same skeleton, side-by-side comparable |
| Capstone | 1 | build a minimal harness |

Deep-dive pages share one fixed skeleton - identity, loop, context assembly, trust posture, extension surface, model behavior, distinctive mechanism - so page nineteen can be read against page thirteen without re-learning the shape.
That comparability is the point of the module; it is also why the skeleton is fixed and boring.

## The ladder

- **Foundation** (`pill easy`): Orientation and the first page of The loop. Every term defined on the page where it first appears.
- **Working** (`pill med`): the rest of The loop, Trust, Extending, Models, and all fifteen deep dives. Mechanisms and trade-offs taken directly, leaning on foundation vocabulary.
- **Frontier** (`pill hard`): the capstone, and the open questions surfaced inside deep dives (what the classifier-gated loop implies, what code mode does to tool surfaces).

Read the titles in order and the dependency holds: nothing before Orientation needs anything after it.

## Constraints

- **Erode the wrapper belief on every page.** Not by asserting the opposite but by showing a place where two harnesses, on the same model class, make structurally different choices - and where the difference is visible to the user.
- **Name the artifact.** A mechanism is taught with its real name attached: the file, the function, the config key, from a report pinned to a commit. No generic "some harnesses do X".
- **Two answers minimum.** A layer is explained through at least two harnesses answering it differently; one example is an anecdote, two are a design space.
- **Diagrams carry the comparisons.** Where another course would write a paragraph of contrast, this course draws the two paths side by side.

## Out of scope

- Model internals and training - how attention works, why RLHF shapes behavior. [`llm-evolution-course`](../llm-evolution-course/index.html) owns the lineage; the models report feeds this course's Models module only where it changes harness behavior.
- Building agents for non-coding domains, and operating agents in production - deployment patterns, evaluation gates, durable state. [`agent-engineering-course`](../agent-engineering-course/index.html) owns the build track.
- Inference serving - vLLM, quantization, KV cache economics. [`llm-inference-course`](../llm-inference-course/index.html) owns it.

## Siblings

[`agent-engineering-course`](../agent-engineering-course/index.html) is the closest neighbor, and the boundary is worth stating precisely: that course teaches you to **build and operate agents** - the systems you run - assuming the harness as a given component.
This course opens the component itself: the harnesses you **code with**, as software artifacts.
Where agent-engineering asks "what should your agent's trust boundary be", this course asks "how did Claude Code, Codex CLI, and Gemini CLI each build theirs, and what did each choice cost".
A reader finishing that course who wonders what is actually inside the thing it deploys is this course's target learner.

[`ai-system-design-course`](../ai-system-design-course/index.html) touches at token-budget and latency topics; [`herdr-course`](../herdr-course/index.html) covers the runtime those agents sit on, not the agents themselves.

## Revisit when

A harness ships a structural change to its loop or trust model (a new permission mode family, a rewrite of the edit pipeline), a new harness enters the cast and deserves deep-dive number sixteen, or the models report's protocol findings change (a new wire dialect displacing Anthropic Messages as the portability layer).
