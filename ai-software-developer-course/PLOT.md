# Plot - the reading order of AI Software Developer

This file records the true reading order of the course: where every lesson sits, and everything planned but unwritten.

The order rule, which holds for this course and every course in the hub: **a course's reading order is its true order**, and material that follows a lesson sits after that lesson in the course map, never in a separate list at the bottom.
When this file and `index.html` disagree, one of them is wrong, and it gets fixed before anything new is added.

Status marks:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held, nothing else may take it, nothing is written.

## Numbering

**Block numbering, stepping by ten.** Module `N` owns `0N00` to `0N99` and its lessons are `0N00`, `0N10`, `0N20` and so on.
Module 10 owns `10x0` and the capstone owns `1100` to `1130`.

`go-course` and `backend-engineering-course` establish the block; `coding-harness-course` establishes the step of ten.
All three write the full four digits in the eyebrow and on the card, so `Lesson 0100`, never `Lesson 100`.

The step of ten matters more here than usually. Nothing published is ever renumbered, this course will grow inside modules while writers work in parallel, and a gap of nine numbers between adjacent lessons means file order never has to disagree with teaching order.
**A lesson added inside a module takes the next free step of ten at the end of that module's block**, never a number between two existing ones.

## The capstone reads across the course, not after it

This is the one place where file order and reading order disagree, and this file is where that is allowed to be written down.

The capstone pages are numbered `1100` to `1130` because nothing published may be renumbered later, and because they reference every module.
**They are read at the end of the module that supplies each one**, not in a block at the end:

| Capstone page | Is read after |
|---|---|
| `1100-the-capstone-pick-your-repository.html` | Module 1 |
| `1110-the-capstone-write-the-contract.html` | Module 4 |
| `1120-the-capstone-close-the-gaps.html` | Module 6 |
| `1130-the-capstone-let-it-run.html` | Module 8 |

`index.html` places each capstone card at the foot of the module it follows, which is the course map carrying teaching order while the file numbers carry permanence.
The open-source contribution track rides on `1130` and gets no pages of its own: the reader's unattended pipeline runs against a repository that is not theirs, which is where module 7 stops being theoretical.
Lesson `0000` opens the capstone by naming it, so nobody meets it for the first time at `1100`.

## The sequence

| # | Position | Status | Notes |
|---|---|---|---|
| 0000 | You are already running one | **written** | The on-ramp. The ten-module map, what this course is not, the capstone opened, and the promise that everything here is done at a keyboard. |
| | **Module 01 - The internals of coding agents** | | Foundation. The machine, made visible. |
| 0100 | What the model actually receives | **written** | A request is a system prompt, a tool schema, a history and your words, concatenated by a program you can read. |
| 0110 | The loop in one picture | **written** | An agent is a while-loop around one API call, and every capability you notice is a tool the loop dispatched. |
| 0120 | The core four tools | **written** | Read, list, edit and bash are enough, because a filesystem plus a shell is a universal interface. |
| 0130 | Reading a tool-call trace | **written** | The trace answers "why did it do that" faster than any prompt change. |
| 0140 | How a system prompt is assembled | **written** | A production system prompt is assembled from parts at run time, and the parts have precedence. |
| 0150 | A tool definition is a contract | **written** | The description is behaviour, not documentation. |
| 0160 | Two hundred lines | **written** | The whole loop fits on one screen. **Split by purpose** from `coding-harness-course/lessons/0270-build-a-harness.html`; each page links the other in its first paragraph. |
| 0170 | What a shipped harness does that yours does not | **written** | Context assembly, permission and recovery, named so the reader knows what to go and read. |
| 1100 | The capstone: pick your repository | reserved | **Read here**, after module 1. A repository chosen, a baseline trace recorded, three tasks to measure. |
| | **Module 02 - Advanced context engineering** | | Foundation. The budget, and how to spend it. |
| 0200 | The window is a budget | **written** | Context is a budget with an eviction policy. |
| 0210 | Which prompting technique, when | **written** | Techniques are not a ranking; naming the failure picks the technique. |
| 0220 | RePPIT, the five moves | **written** | Research, Propose, Plan, Implement, Test puts the expensive decision before the expensive tokens. |
| 0230 | Spec-driven development | **written** | The spec becomes the unit of work rather than the diff. |
| 0240 | MCP in one page | **written** | A client, a server and a transport; the model only ever sees the tool schema. |
| 0250 | Write your first MCP server | **written** | One useful tool is about forty lines, and mounting it changes what the model plans. |
| 0260 | Tools are designed for a reader who cannot ask | **written** | A tool description is executed, not read. |
| 0270 | When not to add a tool | **written** | Every tool you mount is permanent context. Carries the per-turn tool-context arithmetic and the module assignment. It names `0900` and its measurement in prose but carries **no `href` yet**, because `0900` is unwritten and a link to a missing file fails the validator: the writer of `0900` adds both halves. |
| | **Module 03 - Agent skills and the CLI** | | Working. The smallest artefact you write for yourself. |
| 0300 | What a skill is | **written** | A folder the agent reads only when the task matches its description. Carries the measured metadata-against-bodies arithmetic over the nineteen published skills. |
| 0310 | Writing your first skill | **written** | The frontmatter is the whole contract. Carries `internal-comms` verbatim and the measured finding that one published description is 1,068 characters against the standard's 1,024. |
| 0320 | Progressive disclosure, and scripts | **written** | What the agent does not need every time belongs in `references/` or `scripts/`. Carries this repository's own `course-authoring` skill as the shape at scale. |
| 0330 | Where skills live | **written** | Four agents, four precedence rules, and Claude Code and Gemini CLI resolve the same clash in opposite directions. The portable answer is `.agents/skills/` plus a symlink. |
| 0340 | Web skills | **written** | A skill that reaches past the repository turns a context problem into a permission problem. Carries `webapp-testing` and its script complete. Home of the taint figure in this module. |
| 0350 | The agent in a pipeline | **written** | An ordinary unix filter: stdin in, chosen format out, exit code you can branch on. Carries the 10MB pipe cap against six real inputs measured in this repository. |
| 0360 | Session control from the CLI | **written** | A non-interactive run still leaves a session behind. Every flag verified at source, including that Codex has no `--full-auto` at the pinned commit. |
| 0370 | In the field: Cursor | **written** | Public primary material only. Cursor's four answers to the four questions, and the module assignment, which feeds the capstone's first committed agent configuration. |
| | **Module 04 - Customizing your agent and repository** | | Working. The file a team argues about. |
| 0400 | One file, two readers | **written** | Write `AGENTS.md`, then make Claude Code read it with one line. Module entry point. |
| 0410 | What belongs in the file | **written** | The instruction file is a context budget. Carries this repository's own root `AGENTS.md`, measured with `wc -l`, against the documented "under 200 lines". |
| 0420 | The loading hierarchy | **written** | Nothing overrides anything - the files are concatenated. |
| 0430 | Hooks are the enforcement layer | **written** | An instruction asks; a hook decides. |
| 0440 | Writing a blocking hook | **written** | Exit 2 with stderr, or exit 0 with decision JSON. One per hook, never both. |
| 0450 | The Stop hook closes the loop | **written** | The difference between a session you watch and one you walk away from. |
| 0460 | Planner, implementer, reviewer | **written** | A fresh context is the reviewer's entire advantage. |
| 0470 | In the field: Claude Code | **written** | Public primary material only. |
| 1110 | The capstone: write the contract | reserved | **Read here**, after module 4. `AGENTS.md`, one skill, one hook gate, committed and tested. |
| | **Module 05 - Agent-ready codebases** | | Working. Nothing in this hub covers it. |
| 0500 | What agent-ready means | **written** | The agent can close its own loop: set up, change, prove, without asking a human. |
| 0510 | The nine pillars and five levels | **written** | Readiness is a maturity ladder with named rungs. |
| 0520 | Tests are the agent's feedback loop | **written** | The suite is the agent's only sense organ, and its latency is the loop's clock speed. |
| 0530 | Reproducible environments | **written** | If the agent's environment differs from CI's, every failure it fixes is a guess. |
| 0540 | CI an agent can read | **written** | CI output is an API: addressable rather than scrollable. |
| 0550 | Scoring a repository | **written** | Every point must be evidence you can point at. Carries the warning that agent-readiness and AI-reviewability are different properties. |
| 0560 | The gaps that block agents | **written** | The gaps are boringly consistent and each has a named artefact that closes it. |
| 0570 | In the field: Factory | **written** | Public primary material only. |
| | **Module 06 - Agentic code review** | | Working, except `0670`, which is frontier. |
| 0600 | What review is actually for | **written** | Review has four jobs and an AI reviewer can do two. |
| 0610 | What AI review catches | **written** | The findings a machine can reach at all. **Adjacent pair with `0620`; neither may be merged back.** |
| 0620 | What AI review misses | **written** | No open reviewer found more than 62 of every 100 real bugs, recall did not rise with severity, and the benchmark's publisher competes in it. |
| 0630 | Review architectures | **written** | What a reviewer may look at is the ceiling; the prompt is only the ladder. |
| 0640 | Rules you write down | **written** | Write the standard once, in the repository. |
| 0650 | Wiring review into the pull request | **written** | Trigger, volume and authority are three separate settings. |
| 0660 | Measuring your reviewer | **written** | Acceptance rate is the only number that survives contact with your own codebase. |
| 0670 | In the field: Cognition | **written** | Public primary material only. |
| 1120 | The capstone: close the gaps | reserved | **Read here**, after module 6. A readiness score before and after, and review running on their pull requests. |
| | **Module 07 - Security** | | Working, except `0770`, which is frontier. |
| 0700 | The three scanners | **written** | Three scanners answer three different questions. |
| 0710 | Writing a rule | **written** | A scanner rule is a small program you can read. |
| 0720 | The agent attack surface | **written** | Every input the agent reads is a place instructions can enter. Home of the taint figure. |
| 0730 | Permissions are the defence | **written** | You do not defend an agent by prompting it better. |
| 0740 | Sandboxes and hooks | **written** | A rule the model can talk past is a suggestion. |
| 0750 | Scanners in CI | **written** | The gate is the pull request. |
| 0760 | Triage and auto-fix | **written** | The model's job is deciding whether a finding matters and drafting the fix. |
| 0770 | In the field: Semgrep | **written** | Public primary material only. |
| | **Module 08 - Background agents** | | Working. |
| 0800 | What a background agent is | **written** | Where it runs, what it can reach, and how you find out what it did. |
| 0810 | The six cloud agents | **written** | **Written on the mechanism axis** - where the sandbox is, what triggers it, what it may write - with the six as evidence. |
| 0820 | Triggers | **written** | A contract about who may start an agent, on what, with what permissions. |
| 0830 | Issue to pull request | **written** | The pipeline is the product; the agent is one stage in it. |
| 0840 | Running a fleet | **written** | Ten agents contend for one branch, one working tree and one merge target. |
| 0850 | What you owe a background agent | **written** | It cannot ask you a question, so everything it would have asked is in the repository first. |
| 0860 | In the field: Cloudflare | **written** | Public primary material only. |
| 1130 | The capstone: let it run | reserved | **Read here**, after module 8. One unattended pipeline with a ceiling, plus module 7's security pass, plus the open-source contribution track. |
| | **Module 09 - Building an AI-native team** | | Frontier. |
| 0900 | One door for every tool | reserved | Governance moves from the server to the endpoint in front of them. Links **both ways** with `0270`. |
| 0910 | Who is this token for? | reserved | Every token names exactly one MCP server, and no server passes a token onward. |
| 0920 | Granting and taking away | reserved | A policy file you can review, and a log of individual tool calls. |
| 0930 | One place the model bill is paid | reserved | A gateway moves the provider credential off developer machines. |
| 0940 | What a token actually costs | reserved | Arithmetic you can do in your head: which model, and how much of the context is a cache read. |
| 0950 | Making the good setup the default one | reserved | The good configuration arrives on the machine rather than being copied. |
| 0960 | Measuring adoption honestly | reserved | Every available metric measures activity; the number nobody can move is releases. |
| 0970 | In the field: Replit | reserved | Public primary material only. |
| | **Module 10 - The software factory and the future** | | Frontier. |
| 1000 | The loop that closes | reserved | The ordinary delivery loop with agents on some arcs and a human on exactly one gate. |
| 1010 | What starts an agent when nobody is there | reserved | Each trigger has a different trust story. |
| 1020 | Making a correction survive the session | reserved | A rule, a memory or a failing eval has to outlive the run. |
| 1030 | Give every agent one job and one key | reserved | An agent is a principal, and its own credential is what contains it. |
| 1040 | Watching the factory | reserved | Log everything, sample by risk, keep a switch that stops it all. |
| 1050 | Reading the trend lines | reserved | Three measurements point the same way on capability and the opposite way on delivery. Owes a chart with real data. |
| 1060 | What you do next | reserved | Four habits the reader can start this week. |

## Reference sheets

Read alongside, not positions in the sequence.

| Path | Status | Notes |
|---|---|---|
| `reference/glossary.html` | **written** | Every term the course introduces, one definition each. **Each module pull request adds its own terms**, alphabetically. |
| `reference/glossary.html` | **written**, 26 terms | Every term the course introduces, one definition each. **Each module pull request adds its own terms**, alphabetically. |
| `reference/samples.html` | reserved | The samples gallery: a complete, runnable, licensed example of each artefact the course teaches. Written last, because it collects from every module. |
| `reference/readiness.html` | reserved | The readiness scorecard as a standalone printable page, lifted from `0550`. Written last. |

## The one-way links that must not be lost

Two pairs are load-bearing in both directions and are recorded here so a later edit cannot silently drop one half.

- **`0270` and `0900`.** The measurement that four MCP servers and 52 tools cost roughly 9,400 tokens of definitions, collapsing to two tools and about 600 tokens under progressive disclosure, is module 9's strongest single argument and module 2's budget lesson is where the reader learned to care. Each page links the other. **State today:** `0270` is written and carries the measurement, Cloudflare's own source, and `0900`'s number and title in prose, with no `href`, because linking an unwritten page fails `validate_site.py`. Whoever writes `0900` adds the `href` in `0270` and the link back, in the same pull request.
- **`0160` and `coding-harness-course/lessons/0270-build-a-harness.html`.** The split by purpose. Each page states in its first paragraph what the other build is for.

The remaining out-of-course links are one-way and belong to the pages that carry them; `BUILDER-SPEC.md` names the rule for making one.

## Planned but unwritten

Everything above marked `reserved`. The position is held and nothing else may take it.
The full map - one row per page, with the report and lesson entry that carries its beats, figures and samples - is the frozen course map that this course was scaffolded from, and it is working material rather than a file in this repository.

## Adding a lesson to this course

1. Read `AGENTS.md`, `MISSION.md`, `NOTES.md`, `BUILDER-SPEC.md` and `RESOURCES.md` first, then the two pages either side of your slot.
2. Take the next free step of ten **inside your module's block**. Never renumber anything.
3. Insert the new material at its true position in this file and in `index.html`, never appended to the bottom because it arrived last, and flip its row here from `reserved` to `written`.
4. Re-run `python3 scripts/gen_outline.py ai-software-developer-course`, commit the regenerated `outline.js`, run `python3 scripts/validate_site.py` and `python3 .claude/skills/course-authoring/scripts/check_pages.py ai-software-developer-course`, and open the changed pages in both render states before opening the pull request.
5. Fix the pager on the previous last page of your module. Adding module `N` changes the "next" on the last page of module `N-1`, which is the edit nobody expects.
