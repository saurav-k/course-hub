# Mission

The record of the interview in `.claude/skills/course-authoring/new-course.md`.
This file is canonical: when a later authoring decision is argued, it is settled by re-reading this, not by re-deciding.

## Why this course exists

**The learner** is a working software engineer with two to ten years in the job who uses an AI assistant every day and has never built, configured, secured or operated a coding agent on purpose.

**What may be assumed without teaching:** the shell, git, HTTP, one mainstream language, and surface familiarity with a ChatGPT- or Copilot-style tool.
Transformer internals, retrieval architecture and distributed systems are not assumed and are not taught. Each has a neighbour, and the neighbours are named below.

**The cold spot:** they treat the agent as a chat box.
They do not know what the loop does with their words, why a `CLAUDE.md` changes behaviour, what a hook can stop, why a repository is or is not agent-ready, where prompt injection enters, or how to run ten agents at once without chaos.
That is precise, and it is not "new to agents": they have thousands of hours of use and no model of the machine.
Getting this wrong in either direction makes every page slightly wrong. Written for a beginner, the course patronises someone who has shipped code with an agent every day for two years. Written for an architect, it skips the one thing they are actually missing.

## The source

The spine is the captain's ten-week syllabus.
**Its ten modules are the ceiling on topics and its ordering is the default.**
A module may become more lessons than it has bullets; no eleventh module is added.

A guest session in the syllabus becomes an **"in the field" lesson** built from that company's public primary material - documentation, engineering posts, open-source repositories, published talks.
A private lecture is never presented as if attended, and a person is named only as the author of public material.

## Success looks like

The learner can:

- **Read a tool-call trace** and say why the agent did what it did, without changing the prompt to find out.
- **Write a repository contract** - `AGENTS.md`, a hook, a skill - and predict which of its lines changes behaviour and what each costs per turn.
- **Score a repository for agent-readiness** and name the three changes worth making first.
- **Find where untrusted text enters** their own agent setup, and say what it is allowed to do once it is there.
- **Run several agents unattended** through an issue-to-pull-request pipeline with a spend ceiling and a way of telling which one is stuck.

**The failure that would still be a failure with every page accurate: the course becomes a tour of products.**
Every module names companies and every one of them ships fast. A page that is a feature list is out of date before it is merged and teaches nothing transferable.
The test each page must pass: **if the named product disappeared, would this page still be worth reading?**
If not, the mechanism is missing and the page is a review.

The second failure, close behind, is re-teaching `coding-harness-course`.
That course took fifteen harnesses apart at source level. This one is what the reader does at the keyboard.
Every page that explains how a harness is built rather than how to use one is a page in the wrong course.

## Structure

**Lesson pages, and lesson pages only.** Not chapters, not lectures split into parts.

Three reasons, and the third is decisive.
A chapter indexes many topics for a reader in review; this reader is learning a sequence for the first time, and each module bullet is a genuinely separate idea with its own figure and its own quiz.
A lecture-in-parts contract exists for a source lecture too big for one sitting, and there is no such source here - the syllabus is bullets, not transcripts.
And **the interactive shapes are per-idea**: a stepper that plays one trace, a scorecard for one question, a calculator with three sliders. Each belongs to one tight idea, and a chapter carrying six of them would blow the word ceiling and the reader's attention at once.

**Not routed.** There is one order and the syllabus states it.
A routed course costs a hand-written `routes.js`, a committed pager per lesson naming its owning route, and `gen_outline.py` refusing to run. `new-course.md` says answer no unless several orders were the reason for the course. They were not.

**Size: 86 pages.** Lesson `0000`, ten modules of seven or eight lessons, four capstone pages and three reference sheets.
Larger than `llm-evolution-course` (57) and `llm-papers-course` (46), and three times `coding-harness-course` (28).

**900 to 1,400 prose words per page, 1,800 the ceiling.** The house numbers, unchanged.
This course has a specific reason to sit at the low end: the captain's second guideline is low cognitive load and fewer words, and the fifth is more interactivity than theory.
A page here that reaches 1,600 words has probably written out what a stepper should be showing.

## The ladder

Three rungs, and the ladder is a claim about dependencies rather than about difficulty.

- **Foundation** (`pill easy`): lesson `0000` and all of modules 1 and 2. The reader arrives cold to the machine, and every term is defined here.
- **Working** (`pill med`): modules 3 to 8. The reader has the loop and the context model, and can be handed a mechanism and its trade-off directly.
- **Frontier** (`pill hard`): modules 9 and 10, all four capstone pages, and the "in the field" pages of modules 6 and 7. The reader can be handed an open question, a contested claim, or a company's own account of what it does.

## Constraints

Four that the house standard does not already carry.

1. **Every configuration file the course mentions is shown complete and runnable**, in a fenced block with a language tag, with its source, its licence and whether it may be reproduced verbatim.
   A fragment with an ellipsis in it teaches nobody to write the file. The licence rule is in `BUILDER-SPEC.md`.
2. **Evergreen and time-free.** No dates on pages, no schedule, no grading weights, no guest-lecture pages.
   A version-sensitive claim carries the version in the sentence, never a date on the page.
3. **A company is named only from its own public primary material.** A private lecture is never presented as if attended, and people are named only as authors of public material.
4. **Every page cites at least one primary source the author opened**, and separates KNOWN (documented or in source) from INFERRED (the author's reading) from MARKETING (a vendor claim with no mechanism shown). The third label goes in a `.callout.warn`.

## Out of scope

| Not taught here | Who owns it |
|---|---|
| How a harness is built inside, at source level | [`coding-harness-course`](../coding-harness-course/index.html) |
| Production agent systems: durable state, evals, cost kill-switches, retrieval, isolation | [`agent-engineering-course`](../agent-engineering-course/index.html) |
| The decision a staff engineer defends: should this be an AI system, what it costs, blast radius, model supply | [`staff-ai-course`](../staff-ai-course/index.html) |
| Whiteboard system design for AI interviews | [`ai-system-design-course`](../ai-system-design-course/index.html) |
| The terminal runtime agents live on, and its plugin system | [`herdr-course`](../herdr-course/index.html) |
| General production engineering at three scale tiers | [`production-systems-course`](../production-systems-course/index.html) |
| What a language model is, and the papers under it | [`llm-papers-course`](../llm-papers-course/index.html), [`llm-evolution-course`](../llm-evolution-course/index.html) |
| Inference economics and desk-hardware deployment | [`llm-inference-course`](../llm-inference-course/index.html), [`llm-efficiency-course`](../llm-efficiency-course/index.html) |

Every row has a destination. Nothing is abandoned.

## Siblings

`coding-harness-course` is the mechanism under modules 1 to 4 and is cited on nearly every page of them.
`staff-ai-course` owns prompt injection, cost and organisational adoption, which are the three places this course is most at risk of writing a second essay.
`agent-engineering-course` owns MCP-server design, durable async and isolation.
`herdr-course` owns everything about supervising a fleet from a terminal.

**Modules 5 and 6 - agent-ready codebases and agentic code review - have no coverage anywhere in this hub.** They are what this course adds that nothing else does.

One thing overlaps enough to have needed a decision, and it was taken before the build started.
**"Build a Claude-Code-like agent in about 200 lines" is `coding-harness-course/lessons/0270-build-a-harness.html` with a different framing.**
The decision is **split by purpose**: the harness capstone builds in order to compare against fifteen harnesses, and lesson `0160` here builds in order to read your own transcript afterwards.
Two pages, each linking the other in its first paragraph. Neither is a rewrite of the other, and an author who cannot say which purpose their page serves is writing the wrong one.

## Revisit when

**Module 4 is written**, because that is the first module whose "in the field" page tests whether the public-material-only rule produces a page worth reading.
If it does not, the rule needs the captain rather than the author.
