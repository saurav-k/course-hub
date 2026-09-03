# Mission

The record of the interview in `.claude/skills/course-authoring/new-course.md`.
This file is canonical: when a later authoring decision is argued, it is settled by re-reading this, not by re-deciding.

## Why this course exists

**The learner** is a data scientist, ML engineer or backend engineer with two to eight years in the job, who has called an LLM API and built a demo, and has never shipped an AI system to production.

**What may be assumed without teaching:** intermediate Python, basic machine learning, HTTP and APIs, git and the shell.
Docker and Kubernetes are taught only as far as deployment needs them.
Transformer internals, serving engines and classic backend scaling are not assumed and are not taught. Each has a neighbour, and the neighbours are named below.

**The cold spot:** they can make a demo work and cannot make it measurably better, reliable, or cheap.
They believe prompt wording is the lever, and they treat evaluation as a final step instead of the first one.

That is precise, and it is not "new to LLMs".
Written for a beginner, this course patronises somebody who has shipped Python for six years. Written for an architect, it skips the one thing they are actually missing, which is a number they can move.

## The source

The spine is the captain's eight-module syllabus, `data/aie/syllabus.html` in the firstmate home.
**Its eight modules are the ceiling on topics and its ordering is the default.**
A module may become more lessons than it has bullets; no ninth module is added.

Three scout reports ground the syllabus in primary sources and set the exact lesson count per module.
Where a report grounds a sharper version of an answer here - a page number, a source, a rung - the sharper version wins as long as it does not change the decision.

## Success looks like

The learner can:

- **Build a retrieval pipeline** with evaluation and observability wired in from day one, and read one request as a trace rather than as a guess.
- **Improve retrieval** with hybrid search and re-ranking, and prove the gain with a number on their own golden set.
- **Build an agent** with tools, memory and reflection, and grade its trajectory rather than only its answer.
- **Orchestrate multi-agent workflows** over MCP and A2A, and debug one from its trace.
- **Deploy** with CI/CD, caching, security and a cost and latency budget, and monitor it in production.

**The failure that would still be a failure with every page accurate: a page that explains a mechanism a sibling course already explains better, with a code block bolted on.**
This course has almost no territory that is not already covered at concept level somewhere in this hub. Its whole claim is the word hands-on, and a page that is a second essay on somebody else's subject has forfeited that claim.

Two more failures, close behind, each named by the captain:

- **A framework tutorial.** The syllabus names five frameworks and every one of them ships fast. The test each page must pass: if the named package disappeared, would this page still be worth reading?
- **A concept course with no running capstone.** If a module's increment does not leave the reader's own application runnable, the module is a lecture.

## Structure

**Lesson pages, and lesson pages only.** Not chapters, not lectures split into parts.
Each syllabus bullet is a separate mechanism with its own figure, its own quiz and its own hands-on act, and the five interactive figure shapes are per-idea rather than per-topic.

**Not routed.** There is one order and the syllabus states it.

**Size: 53 lessons, seven capstone pages and four reference sheets.**
Lesson `0000`, then eight modules of three to nine lessons each.

**900 to 1,400 prose words per page, 1,800 the ceiling.** Three to five figures, two quizzes, one practice problem, and one interactive figure wherever there is a state, a budget, a file, a score or a boundary to manipulate.

**This course is on the extended bar.** `ai-engineering-course` is in `EXTENDED_BAR_COURSES` in `.claude/skills/course-authoring/scripts/check_pages.py`, opted in at scaffold time rather than retrofitted later.
Every page therefore owes a practice problem with a `details.solution` and a `.p-check`, and at least one inline `svg.chart`.
The decision was taken because two scouts reached it independently from different evidence, because a course about token bills and retrieval scores that draws no chart has made claims it did not show, and because joining the set later is a retrofit across every page.

## The ladder

Six rungs of capability, mapped onto the three pills the hub paints:

1. Run a pipeline.
2. Measure it.
3. Change it and prove the improvement.
4. Compose systems from agents.
5. Operate it in production.
6. Design and defend the architecture.

- **Foundation** (`pill easy`): lesson `0000` and module 1. The reader arrives cold to the pipeline, and every term is defined here.
- **Working** (`pill med`): modules 2 to 6. The reader has a baseline and can be handed a mechanism and its trade-off directly.
- **Frontier** (`pill hard`): modules 7 and 8, the two "in the field" pages, and every capstone page. The reader can be handed an open question, a contested claim, or a company's own account of what it does.

## The spine that is not a module

**Observability and evaluation is a thread, not a module 1 topic.**
It starts at `0150` with one trace and one retrieval span, becomes a gate by `0250`, and closes at `0430` when the reader's own users start writing rows into the golden set.
**Modules 5 to 8 re-run the same golden set.** They do not build a second one.
If a later module introduces its own eval harness, the course has two harnesses and the reader will maintain neither, and the thread has become decoration.

The consequence for a writer: whatever module 1 establishes as the evaluation vocabulary is the vocabulary `0640`, `0660` and `0800` use. Module 1 has to land before those three are written.

## The capstone

**One application, built as an increment per module, measured every time on the same golden set.**
A question-answering service over a document corpus the reader chooses, served behind an HTTP API, traced with OpenTelemetry, and gated by an evaluation set the reader wrote in module 1.

Three decisions about it are settled and are recorded here so nobody re-proposes them.

**Bring-your-own corpus is the default, and the course ships a fallback.**
A reader who cares about their corpus will actually look at the failures, and the cost - that no number in the course can be a target - is correct anyway, since every number the course cites is somebody else's measurement on somebody else's data.
The fallback corpus for a reader with nothing to hand is **this repository's own course content**, which is CC BY 4.0 for prose and MIT for code and is therefore the one corpus this hub can redistribute with no licence question.
It is real technical prose with real structure, and a reader can check a retrieval result by opening the page it came from.
The module 1 writer builds the loader.

**A single-agent capstone is complete.**
Lesson `0500` teaches refusing the second agent with arithmetic, and a reader who correctly decides against multi-agent, with the arithmetic written down, has learned the module.
The recorded decision - the measured single-agent token cost, the projected multi-agent cost, and the go or no-go - satisfies the capstone. **No delegation edge is required.**
Without this stated, every reader builds a supervisor in order to finish the course, which is the exact behaviour `0500` teaches against.

**Demo day is an artefact, not an event.**
Lesson `0820` converts it: a recorded five-minute walkthrough, a written design record and a live URL, with the failure rehearsed rather than the happy path. No dates, no schedule, no grading, no attendees.

## Constraints

Five that the house standard does not already carry.

1. **The protocol is the subject; the framework is the fixture.**
   Reference code stays framework-light: the provider SDK, Pydantic, one vector database, LangGraph for agent graphs, and the official MCP and A2A SDKs.
   LangChain, the OpenAI Agents SDK and Google ADK appear as evidence for a concept and never as the subject of a lesson.
   A framework may be named when it is the shortest honest way to show a mechanism, and it is then pinned to a version in the same sentence.
2. **Claude API first, Gemini second, and the provider swaps in one place.**
   Every sample is written so that changing provider is one edit, and the two vendors' structured-output mechanisms are shown as two spellings of one shape.
3. **No page in modules 3 or 5 uses a coding-agent example, and no page in modules 1, 2 or 4 uses a code corpus as its worked example.**
   Both exist for one reason: `ai-software-developer-course` is 86 pages about agents at the keyboard, and without these two rules the tool-use pages and the retrieval pages read as a second copy of it.
   The reader's instinct will be to index their own repository. Do not let a lesson do it.
4. **Nothing on a page is dated.** A version-sensitive claim carries the version in the sentence.
   A protocol revision (`2026-07-28`), a model id, a pinned commit and a package version are names rather than dates, and all four are welcome.
5. **Every number carries whose measurement it is.**
   A vendor's figure measured on the vendor's own corpus is evidence that an effect is real and is never a target for the reader's corpus. The page says which it is, in the same sentence.

## Out of scope

| Not taught here | Who owns it |
|---|---|
| Model internals, attention, and the papers under them | [`llm-papers-course`](../llm-papers-course/index.html), [`math-for-ml-course`](../math-for-ml-course/index.html) |
| Serving engines, quantization, paged attention, inference economics | [`llm-inference-course`](../llm-inference-course/index.html) |
| Whiteboard system design and AI interview practice | [`ai-system-design-course`](../ai-system-design-course/index.html) |
| Coding agents, agent-ready repositories, AI code review | [`ai-software-developer-course`](../ai-software-developer-course/index.html) |
| Organisational adoption, model retirement, the staff-level decision | [`staff-ai-course`](../staff-ai-course/index.html) |
| Classic scaling, queues, caches and backend fundamentals | [`production-systems-course`](../production-systems-course/index.html), [`backend-engineering-course`](../backend-engineering-course/index.html) |
| Desk hardware and local models | [`llm-efficiency-course`](../llm-efficiency-course/index.html) |

Every row has a destination. Nothing is abandoned.

**Syllabus bullet 7.3, interview preparation, is dropped.**
It is `ai-system-design-course`'s stated purpose and re-writing it here would be the duplication this mission is written to prevent.
The module 7 card carries a plain-text pointer to that course rather than a lesson. The decision is recorded here so it is not re-proposed.

## Siblings

Five courses this one touches, and what each adds that this one does not.

- **`agent-engineering-course`** owns context engineering **across the turns of an agent loop**, MCP server design, durable async and inter-agent security.
  **This course's context engineering is one turn's retrieval payload**: what goes into the window for a single request, and what it displaces.
  That split is written down here because two writers will otherwise each write the general essay.
- **`ai-system-design-course`** frames retrieval, evaluation, cost and trust at the whiteboard.
  Nineteen of module 1 and module 2's topics appear there as concept entries. **Every foundations and retrieval-quality lesson links its counterpart section** in `ai-system-design-course/lessons/0001-rag-and-retrieval.html`, which is what makes "we teach it hands-on, they frame it" true rather than asserted.
- **`ai-software-developer-course`** owns MCP as a subject: `lessons/0240-mcp-in-one-page.html` is already written against revision `2026-07-28` and `0250-write-your-first-mcp-server.html` walks a reader through a server in two languages.
  **Do not write an "MCP in one page" here.** This course's MCP lesson is the host side, which is the framing none of those pages takes.
- **`llm-inference-course`** owns the serving engine, so prefix caching inside the server links out from `0630` rather than being explained.
- **`production-systems-course`** owns retries, circuit breakers and queues, so `0610` links out for the general mechanism and owns only what is different when the dependency is a model provider.

**A2A appears nowhere else in this hub, and neither does the host side of MCP, agent memory outside the context window, or the arithmetic of refusing a second agent.** Those are what this course adds that nothing else does.

## Revisit when

**Module 2 is finished**, because module 2 is the module whose whole promise is that the number moved.
If its capstone page cannot produce a table with at least one zero or negative delta in it, the promise is decoration and the `NOTES.md` rule that carries it needs the captain rather than the author.
