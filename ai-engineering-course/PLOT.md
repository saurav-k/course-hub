# Plot - the reading order of End-to-End AI Engineering

This file records the true reading order of the course: where every lesson and every capstone stop sits, and everything planned but unwritten.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order**, and a lab that follows a lesson sits after that lesson in the course map, never in a separate list at the bottom.
When this file and `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

Status marks:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held, nothing else may take it, nothing is written.

## Numbering

**Block numbering, stepping by ten.** Module `N` owns `0N00` to `0N99` and its lessons are `0N00`, `0N10`, `0N20` and so on.
The capstone track owns `1000` to `1090`.

Write the full four digits everywhere: `Lesson 0100`, never `Lesson 100`.

Nothing published is ever renumbered, and eight writers work inside this course in parallel, so **a lesson added inside a module takes the next free step of ten at the end of that module's block**, never a number between two existing ones.
The free tail of every block is reserved below for exactly that.

## Eight writers, eight blocks

This course is written by eight module writers working at the same time, so `index.html` and this file both carry one delimited registration block per module, created empty in the scaffold pull request:

```html
<!-- module-05:start -->
<!-- module-05:end -->
```

**A writer fills its own block and touches no other.** That is what keeps eight branches off the same lines of the same four files, which is the failure `.claude/skills/course-authoring/new-course.md` section 3b was written from.

Three things are the integrator's rather than a writer's:

- **`reference/glossary.html` and `RESOURCES.md`** are one final pass after the modules land. Every module would otherwise add terms and sources alphabetically into one list, which is a guaranteed conflict with every sibling.
- **`outline.js` is generated and never merged.** Re-run `python3 scripts/gen_outline.py ai-engineering-course` after every rebase and commit the result. Hand-resolving it is resolving a build artefact against itself.
- **The previous slice's last page.** Adding module `N` changes the "next" pager on the last page of module `N-1`. Two slices are not independent even when their lesson blocks are disjoint, so that edit belongs to the integrator, or it is the first act of the later slice's branch.

The whole capstone track is the integrator's too, for the same reason: every capstone page reads across several modules.

## The within-module constraint that is load-bearing

**In module 1, observability (`0150`) precedes evaluation (`0160` and `0170`), and all three precede module 2.**

A reader who reaches module 2 without a baseline cannot tell whether any of module 2 worked, and that is module 2's entire promise.
This is the one ordering constraint inside a module that a writer may not rearrange for narrative convenience.

## The capstone reads across the course, not after it

This is the one place where file order and reading order disagree, and this file is where that is allowed to be written down.

The capstone pages are numbered `1000` upward because nothing published may be renumbered later, and because each one references several modules.
**They are read at the foot of the module that supplies each one**, not in a block at the end:

| Capstone page | Is read after |
|---|---|
| `1000` - The baseline you will argue with | Module 1 |
| `1010` - The same thirty questions, six changes later | Module 2 |
| `1020` - The agent that knows when to stop | Module 3 |
| `1030` - The retriever other people can call | Module 4 |
| `1040` - The second agent you decided against | Module 5 |
| `1050` - Ship it | Module 6 |
| `1060` - Deliver it | Module 8 |

While nothing in the track is written, the seven entries are grouped in one `Capstone track` section of the course map so the integrator has a single registration block.
**When a capstone page is written, its card moves to the foot of the module it is read after**, and the grouped roadmap entry goes with it.
The pagers carry the same order, which is where the pager chain and the file numbers deliberately disagree.

## The sequence

One table per module, wrapped in that module's registration markers.

### The on-ramp

| # | Position | Status | Notes |
|---|---|---|---|
| 0000 | Your demo works and you cannot prove it | **written** | The gold page. The pipeline in one picture, the same request as a trace, the first number, and the eight modules read as edits to that picture. |

### Module 01 - Foundations

Foundation rung. A pipeline you can run, and then a number you can argue with. The observability and evaluation thread starts here at 0150 and every later module in the course re-runs the golden set built at 0160.

<!-- module-01:start -->

| # | Position | Status | Notes |
|---|---|---|---|
| 0100 | The lifecycle is a loop with a measurement in it | reserved | An AI product has no training step, so what you version is the corpus, the prompt and the eval set. |
| 0110 | The environment is a lockfile, a key and a trace | reserved | A reproducible AI project is three files, and the tooling landscape only matters where it changes one of them. |
| 0120 | RAG is a search problem wearing a generation costume | reserved | Retrieval decides the answer and the prompt only decides the wording. |
| 0130 | An embedding is a lossy address, not a meaning | reserved | Similar addresses are a hypothesis about similar meaning, and the hypothesis is model-specific. |
| 0140 | A vector index trades recall for latency, and a filter breaks it | reserved | An approximate index is a deliberate loss of recall, and a WHERE clause spends the budget again without saying so. |
| 0150 | A RAG trace has a retrieval span, and that is where you look first | reserved | Instrument with names somebody else already agreed on, so why was this answer wrong is a query rather than an argument. |
| 0160 | Measure the retrieval before the model is involved | reserved | Retrieval is measurable with no generation at all, and that measurement tells you where to spend. |
| 0170 | A generation metric is a judge, and a judge needs its own eval | reserved | Reference-free scoring works, and the scorer is a model with named biases you evaluate too. |
| 0180 | Free position | reserved | Held for a lesson a module 1 writer discovers they need. Nothing may take it by accident. |

<!-- module-01:end -->

| # | Position | Status | Notes |
|---|---|---|---|
| 1000 | The capstone: the baseline you will argue with | reserved | **Read here**, at the foot of module 1. The charter, the corpus, the golden set, the two numbers and the trace. The page that makes every later module falsifiable. The integrator writes it, not a module writer. |

### Module 02 - Retrieval quality and context engineering

Working rung, and the module whose whole promise is a number that moved. No lesson here ships without stating what it changed on the reader's own golden set, and the module's capstone page must carry at least one row with a zero or a negative delta.

<!-- module-02:start -->

| # | Position | Status | Notes |
|---|---|---|---|
| 0200 | Ingestion is a pipeline, and every chunk needs an identity | reserved | A chunk that cannot name its source, its offset and its checksum cannot be re-ingested or cited. |
| 0210 | A schema is a contract the model has to satisfy | reserved | One object in three forms: a Python class, a JSON Schema, and a wire payload you can validate at the boundary. |
| 0220 | Chunking is a boundary decision, and the boundary is where meaning is lost | reserved | Retrieval precision and generation sufficiency pull in opposite directions, and the sweep settles it. |
| 0230 | A chunk that cannot say where it came from cannot be found | reserved | Two repairs for the orphan chunk, with their bills: context written in, against embed then split. |
| 0240 | The window is an attention budget, not a container | reserved | More retrieved passages raise the chance the answer is present and lower the chance it is attended to. |
| 0250 | A prompt is a versioned artefact with a name | reserved | A prompt with no name and no version makes a regression unattributable, which is the Tuesday nobody enjoys. |
| 0260 | Two rankings beat one, and RRF is the cheapest way to add them | reserved | Reciprocal rank fusion needs no scores, no tuning and no training, and its k barely matters. |
| 0270 | A reranker is a second, more expensive opinion on twenty documents | reserved | A cross-encoder buys ranking quality with latency, linearly, and the funnel is where you choose how much. |
| 0280 | The document you retrieved is untrusted input | reserved | The retrieved passage is somebody else's text inside your prompt, and the model cannot see the seam. |
| 0290 | Free position | reserved | Held for a lesson a module 2 writer discovers they need. |

<!-- module-02:end -->

| # | Position | Status | Notes |
|---|---|---|---|
| 1010 | The capstone: the same thirty questions, six changes later | reserved | **Read here**, at the foot of module 2. One row per change and the delta it produced. A row with a zero or a negative delta is required. The integrator writes it, not a module writer. |

### Module 03 - Agents and agentic systems

Working rung. What an agent loop is, what bounds it, what a tool call actually carries, and how to grade a trajectory rather than an answer. No page in this module uses a coding-agent example.

<!-- module-03:start -->

| # | Position | Status | Notes |
|---|---|---|---|
| 0300 | Five shapes, and the one that loops | reserved | Most systems people call agents are workflows with predefined code paths; only one shape hands the model the path. |
| 0310 | A loop you did not write is still a loop you must stop | reserved | A framework's agent loop has exactly one exit you control, and choosing it is a product decision. |
| 0320 | A tool call is the only verb an agent has | reserved | The model emits a name and a JSON object and executes nothing; everything happens in your code. |
| 0330 | A failed tool call is a result, not an exception | reserved | An error the model cannot see is an error the model cannot correct. |
| 0340 | Memory is four stores with four lifetimes | reserved | The context window is one of four, and the other three are the ones nobody in this hub has drawn. |
| 0350 | Give the agent a memory it maintains, and a path it cannot escape | reserved | A file-backed memory is a store you own, which makes path validation part of the design. |
| 0360 | Reflection works when the feedback comes from outside | reserved | Two peer-reviewed results disagree, and the difference between them is where the signal came from. |
| 0370 | Grade the path, not only the answer | reserved | A right answer reached by four redundant calls is a bill you will pay every day. |
| 0380 | Free position | reserved | Held for a lesson a module 3 writer discovers they need. |

<!-- module-03:end -->

| # | Position | Status | Notes |
|---|---|---|---|
| 1020 | The capstone: the agent that knows when to stop | reserved | **Read here**, at the foot of module 3. A turn ceiling, a token ceiling, retrieval bound as a tool, a file-backed memory with a traversal test, and an eval set with expected trajectories. The integrator writes it, not a module writer. |

### Module 04 - From basic to agentic RAG

Working rung, and the join. Module 2's pipeline and module 3's loop become one system: retrieval the model decides to call, a grader with a refusal path, a pause the reader can resume, and a feedback loop that grows the golden set.

<!-- module-04:start -->

| # | Position | Status | Notes |
|---|---|---|---|
| 0400 | Retrieval becomes a tool the model decides to call | reserved | Always retrieve becomes retrieve if needed, and the tool description is what decides. |
| 0410 | A retrieval you do not trust is one you can correct | reserved | A lightweight grader between retrieval and generation buys a refusal path, which is a designed exit rather than a failure. |
| 0420 | A pause is a state you saved, not a thread you blocked | reserved | Human-in-the-loop is a checkpoint on disk, and the node restarts from its first line rather than resuming mid-function. |
| 0430 | A thumb down is a row in the golden set | reserved | A feedback record with no trace id is unusable, and the loop closes on the set module 1 built. |
| 0440 | Your RAG app is a host, and its best source is one you did not write | reserved | Mounting a server you do not run changes what reaches the window without changing top-k, and the annotation defaults are the trap. |
| 0450 | A deep research agent is a retrieval loop with a citation contract | reserved | The loop is cheap to describe and expensive to run, and the citation contract is what makes it checkable. |
| 0460 | Free position | reserved | Held for a lesson a module 4 writer discovers they need. |

<!-- module-04:end -->

| # | Position | Status | Notes |
|---|---|---|---|
| 1030 | The capstone: the retriever other people can call | reserved | **Read here**, at the foot of module 4. The refusal path, the resumable approval, the feedback endpoint, and a golden set bigger than the reader wrote by hand. The integrator writes it, not a module writer. |

### Module 05 - Multi-agent systems

Working rung, and the module a reader may correctly finish by deciding against. The arithmetic comes before the architecture: a recorded decision to refuse the second agent, with the numbers, is a complete capstone.

<!-- module-05:start -->

| # | Position | Status | Notes |
|---|---|---|---|
| 0500 | The second agent is a cost before it is a capability | reserved | The token multiplier is measured and published, so the decision can be arithmetic rather than taste. |
| 0510 | Delegation is a tool call | reserved | A handoff is an ordinary tool call with a history filter on it, and the filter is the design. |
| 0520 | Planning is a ledger the orchestrator rewrites | reserved | An outer loop that rewrites a durable plan is what survives a stall; a plan held in the window does not. |
| 0530 | Shared state is what they actually disagree about | reserved | Three sharing mechanisms, and only one of them is still there after a restart. |
| 0540 | An agent that is not a tool | reserved | MCP goes down to tools and A2A goes across to peers, and the Agent Card is a list of promises. |
| 0550 | Read the trace before you touch a prompt | reserved | A multi-agent failure has a category, and the category names the design change. |
| 0560 | Reserved: in the field, the orchestrator-worker research system | reserved | Held, not written. The strongest available page here rests on an evaluation set that is not published, so it would have to be written as what the company says it measured. Module 7 uses the same post as one of two priced case studies instead. |
| 0570 | Free position | reserved | Held for a lesson a module 5 writer discovers they need. |

<!-- module-05:end -->

| # | Position | Status | Notes |
|---|---|---|---|
| 1040 | The capstone: the second agent you decided against | reserved | **Read here**, at the foot of module 5. The measured single-agent cost, the projected multi-agent cost, and the go or no-go. Deciding against it correctly is a pass. The integrator writes it, not a module writer. |

### Module 06 - Deployment, optimization and reliability

Working rung, and the heaviest module in the course. Six syllabus bullets that are each a separate mechanism with its own hands-on act: request shapes, health, latency, four caches, injection, the CI gate, and monitoring a system that fails without an error.

<!-- module-06:start -->

| # | Position | Status | Notes |
|---|---|---|---|
| 0600 | Four shapes for a request that takes thirty seconds | written | Synchronous, streamed, queued with a handle, offline batch; picking the wrong one is what makes a demo unshippable. |
| 0610 | The provider is a dependency you do not own | written | A liveness probe that calls the model turns a provider outage into a restart storm you inflicted on yourself. |
| 0620 | Where the seconds go | written | Latency is time to first token plus tokens times inter-token latency, and only one of the three terms is yours. |
| 0630 | Four caches, and only two of them are yours | written | Caching names four mechanisms at four layers, and confusing them is why a team pays for a cache it is not using. |
| 0640 | Semantic caching, and the false hit you have to measure | written | A semantic cache answers a question nobody asked, at a rate you can measure and must measure. |
| 0650 | What a prompt injection is allowed to do | written | You cannot make a general-purpose agent injection-proof, so the design decision is what it may do after it reads untrusted text. |
| 0660 | CI when the unit test is a distribution | written | A prompt change is a code change with no compiler, so the gate is a threshold on a measured score. |
| 0670 | Monitoring a system whose failures are quiet | written | The signals worth alerting on are token counts, finish reasons and eval scores rather than 500s. |
| 0680 | Free position | reserved | Held for a lesson a module 6 writer discovers they need. |

<!-- module-06:end -->

| # | Position | Status | Notes |
|---|---|---|---|
| 1050 | The capstone: Ship it | reserved | **Read here**, at the foot of module 6. A deployed service with three probes, a written cost budget, one security pattern applied, and an evaluation threshold in CI. The integrator writes it, not a module writer. |

### Module 07 - Agentic AI system design

Frontier rung. Two case studies built from those organisations' own public material, the arithmetic that prices a system before it exists, and a six-question review the reader runs on their own capstone. Interview preparation is out of scope and belongs to AI System Design for Staff+ Interviews.

<!-- module-07:start -->

| # | Position | Status | Notes |
|---|---|---|---|
| 0700 | In the field: an orchestrator and its workers | reserved | A fan-out research system buys quality with tokens at a rate the organisation published, and the multiplier is the design decision. |
| 0710 | In the field: a text-to-SQL agent people actually use | reserved | Two independent teams arrived at the same three-stage decomposition, and every stage exists to shrink the search space. |
| 0720 | Sizing a system you have not built | reserved | Five numbers price an agentic system before it is written, and the sensitivity says which of the five actually moves the answer. |
| 0730 | The design review: six questions, on your own system | reserved | The transferable skill is a review you can run on any agentic system, including one you did not build. |
| 0740 | Free position | reserved | Held for a lesson a module 7 writer discovers they need. |

<!-- module-07:end -->

### Module 08 - Final delivery

Frontier rung. Three tiers of test for a system that answers differently every time, a repository a stranger can run, and the artefact that replaces demo day.

<!-- module-08:start -->

| # | Position | Status | Notes |
|---|---|---|---|
| 0800 | Three tiers of test for a system that answers differently every time | reserved | Non-determinism does not excuse a system from testing; it decides which tier each assertion belongs in. |
| 0810 | The repository a stranger can run | reserved | Four artefacts carry the promise that somebody else can reproduce your result. |
| 0820 | The delivery: what replaces demo day | reserved | The demo is an artefact rather than an event, and the rehearsal is of the failure rather than the happy path. |
| 0830 | Free position | reserved | Held for a lesson a module 8 writer discovers they need. |

<!-- module-08:end -->

| # | Position | Status | Notes |
|---|---|---|---|
| 1060 | The capstone: Deliver it | reserved | **Read here**, at the foot of module 8. A public repository, three test tiers, the six-question design record, and a recorded five-minute walkthrough. The integrator writes it, not a module writer. |


## Reference sheets

Read alongside, not positions in the sequence. All four are the integrator's final pass.

| Path | Status | Notes |
|---|---|---|
| `reference/glossary.html` | **written** | Glossary. Every term this course introduces, one definition each, linked to the page that develops it. Seeded from the three research reports; the integrator completes it after the modules land. |
| `reference/eval-harness.html` | **reserved** | The eval harness. The golden-set format, every metric definition with its source, and the reporting rule: a number with no k, no set and no corpus version is not a number. |
| `reference/troubleshooting.html` | **reserved** | The number did not move. What to check, in order, when a change that should have helped did not. The self-paced conversion of the syllabus's office hours. |
| `reference/figures.html` | **reserved** | The two figures the course reuses. The four request shapes from 0600 and the six-question design review from 0730, drawn once so later lessons and both capstone pages point at them rather than redrawing them. |

## Planned but unwritten

Everything above marked `reserved`: fifty-two lessons, nine free positions at the tail of the eight module blocks, the held module 5 in-the-field position `0560`, seven capstone pages and three reference sheets.

`0560` deserves its own line, because it is held rather than free.
The strongest available page there is the orchestrator-worker research system, and its evaluation set is not published, so the page would have to be written as *what the company says it measured* rather than as a result.
That is a harder page than it looks, and module 7 already uses the same public post as one of two priced case studies.
**Do not write `0560` without the captain.**

## Adding a lesson to this course

1. Read `AGENTS.md`, `MISSION.md`, `NOTES.md`, `BUILDER-SPEC.md` and `RESOURCES.md` first, then `lessons/0000-your-demo-works-and-you-cannot-prove-it.html`, which is the gold page every other page here is matched against.
2. Take the next free step of ten **inside your own module's block**. Never renumber anything.
3. Put the card inside your own `<!-- module-NN:start -->` block in `index.html`, flip the row here from `reserved` to `written`, and touch no other module's block.
4. Re-run `python3 scripts/gen_outline.py ai-engineering-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py` and `python3 .claude/skills/course-authoring/scripts/check_pages.py ai-engineering-course`, and open the changed pages in both render states before opening the pull request.
5. The "next" pager on the last page of the previous module is the integrator's edit, not yours - unless you make it the first act of your own branch and say so in the pull request.
