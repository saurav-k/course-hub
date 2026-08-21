# Mission

## Why this course exists

Build and operate agents that survive production, rather than agents that demo well.

The learner is a Principal engineer with twelve years of distributed-systems experience.
The gap is not architecture and it is not model knowledge.
It is that the agent ecosystem's default patterns quietly omit properties this engineer would never ship without: durable state, a deploy gate, a cost ceiling, a tested degradation path, and a trust boundary around anything the model reads.

This is the **build track**.
Its sibling, [`ai-system-design-course`](../ai-system-design-course/index.html), is the **interview track** over overlapping material.
Where the interview track asks what you would say at a whiteboard, this course asks what you would put in a repository, what you would measure the week after, and what pages you at 03:00 when you get it wrong.

## Success looks like

In a design review for a system you are actually going to run, you can:

- Account for every token in the tenth turn of an agent loop, by slot, and say which slot you evict from first.
- Write an MCP server and defend what it refuses to do, not only what it exposes.
- Show the evaluation gate a prompt change must pass, including how the agent's trajectory is graded and not only its answer.
- Point at the recorded state that lets a crashed agent resume without repeating a paid call or a side effect.
- Name your time to first token and your inter-token latency separately, at the tail, and say which one users complained about.
- Show the enforcement point that stops a runaway bill without a human being awake.
- Explain why one agent's output is untrusted input to the next, and what bounds the damage when it is.

## Constraints

- Concept-first. The learner does not need code walkthroughs to understand a mechanism.
- Every topic carries a link to a primary source: a paper, a specification, or vendor documentation.
- No invented numbers. Where a figure is not in a source that can be linked, the effect is described qualitatively and the reader is told what determines it.
- Field framing throughout. Each chapter ends with the questions a Staff+ reviewer actually asks and the trap inside each one.

## Out of scope

- Training or fine-tuning models. This is a build, serve, and operate course.
- Framework tutorials. Frameworks change; the failure modes do not.
- Agent product design, prompt-writing craft, and model selection as a shopping exercise.
- Interview technique, which is the sibling course's job.

## Structure

Five chapters, one per pillar, covering eighteen topics.
Every topic appears as its own anchored subsection with a linked source, so a chapter doubles as a reference index during a design review.

1. Context and Protocol
2. Evaluation and the Data Flywheel
3. State, Async and Degradation
4. Latency, Cost and Local-First
5. Retrieval and Isolation
