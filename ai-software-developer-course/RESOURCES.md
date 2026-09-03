# AI Software Developer - Resources

The sources this course trusts.
A page cites from here; anything new goes in here first, in the same pull request.

Every entry below was fetched by a research scout or by an author of this course, and the entries are grouped by what rests on them rather than by publisher.
**A page may not cite an entry the author did not open.** That is the house rule and this course leans on it hard, because half its subject matter changes between one release and the next.

## The canon

The small set this course keeps returning to. Primary only.

- [Anthropic - How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works) - the agentic loop stated as a `while` on `stop_reason`, where each kind of tool executes, and the sentence the whole course rests on: "The model never executes anything on its own." Cited by `0000`, `0110`, `0120`, `0130`.
- [Anthropic - Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) - the request fields, the `tool_use` / `tool_result` round trip, and the per-model tool-use system-prompt token table. Cited by `0000`, `0100`, `0150`, `0270`.
- [Anthropic - Define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) - the tool-definition fields, the description rule, `input_examples`, the four `tool_choice` values. Cited by `0150`, `0260`.
- [Anthropic - Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) - window sizes, what counts toward the window, overflow behaviour. Cited by `0100`, `0200`.
- [Anthropic - Pricing](https://platform.claude.com/docs/en/about-claude/pricing) - model prices, cache multipliers, tool-use overheads. Cited by `0940` and by every cost calculator in the course.
- [Model Context Protocol - the current specification](https://modelcontextprotocol.io/specification/2026-07-28) - hosts, clients, servers, the three server primitives. Cited by `0240`, `0250`, `0910`.
- [Model Context Protocol - versioning](https://modelcontextprotocol.io/specification/versioning) - which revision is current, and how a client and a server agree on one. **Read this before writing any MCP claim**; the revision under a page can move.
- [Model Context Protocol - key changes in the current revision](https://modelcontextprotocol.io/specification/2026-07-28/changelog) - the removal of protocol-level sessions and of the `initialize` / `notifications/initialized` handshake. Cited by `0000` and `0240`.
- [Anthropic - Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) - the agent-versus-workflow definition, the five workflow patterns, the agent-computer-interface appendix. Cited by `0110`, `0260`, `0460`.
- [Anthropic - Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) - the tool-design principles, namespacing, response formats, and the prototype-evaluate-collaborate method. Cited by `0260`, `0270`.
- [Claude Code documentation](https://code.claude.com/docs/en/) - the reference for memory files, hooks, skills, permissions, permission modes, sandboxing, settings precedence, headless mode and GitHub Actions. This is the single most-cited host in the course; the specific page goes in the module section below rather than here.
- [agents.md - the AGENTS.md open format](https://agents.md/) - what the file is, how it nests, and closest-wins precedence. Cited by `0400`, `0410`, `0420`, `0500`.
- [agentskills.io - the Agent Skills specification](https://agentskills.io/specification) - the frontmatter contract, the directory layout, and the three progressive-disclosure stages with their token budgets. Cited by `0300`, `0310`, `0320`.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) - the entry IDs and titles this course names, and the prompt-injection entry that `0720` is built on.
- [Simon Willison - the lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) - private data, untrusted content, external communication. **`staff-ai-course` owns this argument**; this course names it and links out rather than re-deriving it.

## Supporting sources

Cited once or twice, by module.

### Module 01 - The internals of coding agents

- [Thorsten Ball - How to build an agent](https://ampcode.com/how-to-build-an-agent) - the staging `0160`'s build ladder follows. No licence statement on the post, so it is quoted rather than copied.
- [Claude Code - permissions](https://code.claude.com/docs/en/permissions) and [permission modes](https://code.claude.com/docs/en/permission-modes) - the six modes, cited by `0170`.
- Open-source harnesses at pinned commits, for real system prompts and tool definitions: [`sst/opencode`](https://github.com/sst/opencode) (MIT), [`cline/cline`](https://github.com/cline/cline) (Apache-2.0), [`block/goose`](https://github.com/block/goose) (Apache-2.0), [`google-gemini/gemini-cli`](https://github.com/google-gemini/gemini-cli) (Apache-2.0), [`openai/codex`](https://github.com/openai/codex) (Apache-2.0). Cited by `0140` and `0150`. **Pin the commit in the page**, as `coding-harness-course` does.
- [Anthropic - Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls) - the `tool_use` and `tool_result` field lists, the formatting rules, `is_error`, and the instruction to write error messages that name the next move. Cited by `0110`, `0120`, `0130`.
- [Anthropic - Parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use) - one assistant turn may carry several calls, and every result goes back together in the next user message. Cited by `0110`, `0130`.
- The five pinned commits module 1 quotes, all read from clones and checked against each repository's own `LICENSE`: opencode `b578b7261fc9ec4917fe272df5cc4bd8a056cd5d` (MIT), Cline `5de79a75d083776552100f21645188badb7bd5aa` (Apache-2.0), goose `9eb6ef099f20b6b3fb5093d7ebb39a3c2d16a35f` (Apache-2.0), Gemini CLI `55b495d6db1794bf5b7f37a9bc03ebcab5103673` (Apache-2.0), Codex CLI `36984da4424cb91b6bc88c6af8d73207930ac729` (Apache-2.0). The three prompt line counts on `0140` were measured with `wc -l` on those clones.

### Module 02 - Advanced context engineering

- [Anthropic - prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) - example counts, XML tagging, the prefill migration table. Cited by `0210`.
- [Anthropic - structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) - the replacement for prefill. Cited by `0210`.
- [Wei et al. - Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) and [Wang et al. - Self-Consistency](https://arxiv.org/abs/2203.11171) - the two results `0210`'s chart is drawn from.
- [MCP - Streamable HTTP transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http) and [server tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) - cited by `0240` and `0260`.
- [MCP - build a server](https://modelcontextprotocol.io/docs/develop/build-server) - the current TypeScript and Python quickstarts, and the correct package names. Cited by `0250`.
- [github/spec-kit](https://github.com/github/spec-kit) (MIT) and [Kiro - specs](https://kiro.dev/docs/specs/) - the two spec-driven toolchains `0230` compares.
- [Mihail Eric - RePPIT](https://mlops.community/blog/reppit-a-framework-to-ship-production-code-2-3x-faster) - the only substantive public source for RePPIT, and the source of an unevidenced speed claim. `0220` must label that claim MARKETING.
- [Anthropic - context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) - the accounting rule, context rot, the overflow stop reasons, and the statement that a cached prefix still occupies the window. Cited by `0200`.
- [Anthropic - pricing](https://platform.claude.com/docs/en/about-claude/pricing) - the per-model tool-use system prompt table, the bash and text-editor definition costs, the base input rates and the cache multipliers. Every number in `0200`'s bar chart and both calculators.
- [Anthropic - define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) - the three-to-four-sentence description floor, the matched good and poor `get_stock_price` descriptions, `input_examples` token costs, and the consolidation guidance. Cited by `0260` and `0270`.
- [Anthropic - writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) - the five principles, the 25,000-token Claude Code response cap, and "More tools don't always lead to better outcomes." Cited by `0260` and `0270`.
- [Anthropic - tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) - the 55k five-server measurement, the over-85% reduction, the 30-to-50-tool accuracy cliff, and the stated conditions for deferring. `0270`'s chart and its escape-hatch table.
- [Anthropic - manage tool context](https://platform.claude.com/docs/en/agents-and-tools/tool-use/manage-tool-context) - the four approaches to context pressure and which source each one addresses. Cited by `0270`.
- [Anthropic - building effective agents](https://www.anthropic.com/engineering/building-effective-agents) - the prompt-chaining definition and the "add complexity only when it demonstrably improves outcomes" counterweight. Cited by `0210` and `0220`.
- [MCP - specification index, revision 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28) - the three roles, the LSP analogy, and "Stateless, self-contained requests". Cited by `0240`.
- [MCP - versioning](https://modelcontextprotocol.io/specification/versioning) - which revision is current, how revisions are named, and the twelve-month deprecation window with its ninety-day exception. `0240`'s timeline and its deprecation chart.
- [MCP - stdio transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/stdio) - the newline framing and the rule that nothing but a valid message may reach standard output. Cited by `0240` and `0250`.
- [MCP - server concepts](https://modelcontextprotocol.io/docs/learn/server-concepts) - the who-controls-what table for tools, resources and prompts. Cited by `0240`.
- [modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol), `schema/2026-07-28/schema.ts` at commit `1dc2c72` (Apache-2.0 or MIT) - the `ToolAnnotations` comment saying every property is a hint. Quoted in `0260`.
- [modelcontextprotocol/typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) at commit `dcc0102` (MIT) and [python-sdk](https://github.com/modelcontextprotocol/python-sdk) at commit `d060b36` (MIT) - the `registerResource`, `registerPrompt`, `@mcp.resource` and `@mcp.prompt` signatures `0250`'s two servers are written against.
- [Anthropic - Claude Code MCP](https://code.claude.com/docs/en/mcp) - the three scopes, the explicit `type` rule on a `url` entry, variable expansion, and the project-scope approval gate. Cited by `0250`.
- [Cursor - MCP](https://cursor.com/docs/context/mcp) - the `.cursor/mcp.json` shape and Cursor's own interpolation syntax. Cited by `0250`, documented rather than run.
- [Anthropic - configure permissions](https://code.claude.com/docs/en/permissions) - the six permission modes, quoted for the `plan` row. Cited by `0220`.
- [Cloudflare - enterprise MCP reference architecture](https://blog.cloudflare.com/enterprise-mcp/) - the internal portal measurement: 52 tools at about 9,400 tokens collapsing to 2 tools at roughly 600. `0270`'s chart, and the forward reference to module 9.

### Module 03 - Agent skills and the CLI

- [agentskills.io](https://agentskills.io/) and [the specification](https://agentskills.io/specification) - the frontmatter contract, the `name` and `description` constraints, the three conventional folders, and the three progressive-disclosure stages with their token budgets. Cited by `0300`, `0310` and `0320`. **The site publishes no licence for its own text**, so it is quoted short and attributed, never reproduced.
- [Anthropic - Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - progressive disclosure as the design principle, the "effectively unbounded" claim, and the argument for code over token generation. Cited by `0300` and `0320`.
- [Claude Code - skills](https://code.claude.com/docs/en/skills) - the discovery levels and their precedence, the nested and synced cases, the full frontmatter table, the six fields that travel outside Claude Code, the skill-content lifecycle, and the listing budget. Cited by `0300`, `0310`, `0320` and `0330`.
- [Claude Code - headless](https://code.claude.com/docs/en/headless) - `-p`, `--bare`, the three output formats, `--json-schema`, the 10MB stdin cap, the SIGTERM exit code, and `--continue` / `--resume`. Cited by `0350` and `0360`.
- [Claude Code - permission modes](https://code.claude.com/docs/en/permission-modes) - the six modes, and the fact that a `-p` session starts in Manual on every plan. Cited by `0360`.
- [Claude Code - best practices](https://code.claude.com/docs/en/best-practices) - the fan-out loop, the advice to refine on two or three files first, and `/batch` at 5 to 30 subagents. Cited by `0350`.
- [Claude Code - sub-agents](https://code.claude.com/docs/en/sub-agents) - the `mcpServers` frontmatter field, and that a subagent gets the tools while the parent conversation does not pay for the schemas. Cited by `0340`.
- [anthropics/skills](https://github.com/anthropics/skills) - nineteen real skills, measured in this session for the charts in `0300`, `0310` and `0320`. `internal-comms` and `webapp-testing` each bundle an **Apache-2.0** `LICENSE.txt` and are reproduced verbatim with attribution. **Individual skills carry their own licence**; the document skills are described as source-available and must not be reproduced.
- [Cursor - rules](https://cursor.com/docs/rules), [skills](https://cursor.com/docs/skills), [hooks](https://cursor.com/docs/hooks), [cloud agents](https://cursor.com/docs/cloud-agent), [Bugbot](https://cursor.com/docs/bugbot), [CLI overview](https://cursor.com/docs/cli/overview) and [CLI parameters](https://cursor.com/docs/cli/reference/parameters) - the whole of `0370`, and the Cursor column of `0330` and `0360`. **Cursor's documentation states no licence**, so its tables are paraphrased and only short individual descriptions are quoted; the hook script on `0370` is written for this course rather than reproduced.
- [Codex - build skills](https://learn.chatgpt.com/docs/build-skills) - the five discovery scopes, the 2%-or-8,000-character listing budget, and the rule that two skills of the same name both stay available. Cited by `0330`.
- [openai/codex](https://github.com/openai/codex) (**Apache-2.0**) - `codex-rs/utils/cli/src/shared_options.rs`, `codex-rs/exec/src/cli.rs`, `codex-rs/tui/src/cli.rs`, `codex-rs/utils/cli/src/sandbox_mode_cli_arg.rs` and `codex-rs/utils/cli/src/approval_mode_cli_arg.rs`, read at commit `728cb12`. Every Codex flag in `0360` comes from source, because the published documentation would not yield a verbatim flag table. **Pin the commit in the page.**
- [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) (**Apache-2.0**) - `docs/cli/cli-reference.md`, `docs/cli/headless.md` and `docs/cli/skills.md` at commit `55b495d`: the flag table, the four exit codes, and the four discovery tiers with the `.agents/` alias rule. Cited by `0330` and `0360`.

### Module 04 - Customizing your agent and repository

- [Claude Code - memory](https://code.claude.com/docs/en/memory) - the scopes, the concatenation order, imports, and the fact that `AGENTS.md` is not read directly. The whole of `0400` and `0420`.
- [Claude Code - hooks](https://code.claude.com/docs/en/hooks) and [the hooks guide](https://code.claude.com/docs/en/hooks-guide) - the event list, the exit-code and JSON protocols. `0430` to `0450`.
- [Claude Code - subagents](https://code.claude.com/docs/en/sub-agents) and [best practices](https://code.claude.com/docs/en/best-practices) - `0460`.
- [Cursor - hooks](https://cursor.com/docs/agent/hooks) - the second hook contract `0440` compares against.
- [Anthropic - multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) - the orchestrator-worker architecture and its published numbers. `0460`.
- Real `AGENTS.md` files: [`cloudflare/agents`](https://github.com/cloudflare/agents) (MIT), [`sst/opencode`](https://github.com/sst/opencode) (MIT), [`openai/codex`](https://github.com/openai/codex) (Apache-2.0), and this repository's own, which is CC BY 4.0 content and MIT code and may be quoted in full.

### Module 05 - Agent-ready codebases

- [Factory - agent readiness](https://docs.factory.ai/agent-readiness/overview.md), [the readiness report](https://docs.factory.ai/agent-readiness/readiness-report.md), [the dashboard](https://docs.factory.ai/agent-readiness/dashboard.md) - the five levels and nine pillars behind `0510`, and the whole of `0570`.
- [Claude Code - best practices](https://code.claude.com/docs/en/best-practices) - the verification-loop material `0500` and `0520` are built on.
- [`getsentry/sentry` AGENTS.md](https://raw.githubusercontent.com/getsentry/sentry/master/AGENTS.md) - the agent-perception-gap paragraph. The repository's licence is `NOASSERTION`, so **short quoted excerpts only**.
- [`discourse/discourse` devcontainer.json](https://raw.githubusercontent.com/discourse/discourse/main/.devcontainer/devcontainer.json) - GPL-2.0, reproducible with attribution. `0530`.
- [containers.dev - the devcontainer reference](https://containers.dev/implementors/json_reference/) - `0530`.
- [GitHub - workflow commands](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-commands) - annotations and job summaries with their limits. The whole of `0540`.
- [GitHub Copilot - customize the agent environment](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/customize-the-agent-environment) - `0530`.
- [Cognition - how Cognition uses Devin to build Devin](https://cognition.com/blog/how-cognition-uses-devin-to-build-devin) - the best published statement of the agent-perception gap `0500` teaches. Not cited on the page, which builds the gap from a shipped instruction file instead.
- [Factory - AGENTS.md, as one harness reads it](https://docs.factory.ai/harness/agents-md.md) - the search order, the compatible filenames, the nesting rule, the root template, and the 80,000 and 40,000 character context budgets. `0560`.
- [Factory - Droid Shield](https://docs.factory.ai/autonomy-and-safety/droid-shield.md) - secret detection shipped as a product feature, which is the evidence that "secrets in the environment" is a real blocker rather than a hypothetical. `0560`.
- [Factory - the software factory](https://factory.ai/news/software-factory) - the company's own argument that autonomy is gated on organisational readiness, which is the claim `0570` is built on.
- [GitHub - about code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) - what CODEOWNERS matches, last-pattern-wins, and the 3 MB limit past which the file is not loaded at all. `0540`, `0550`.
- [`getsentry/sentry` CODEOWNERS coverage baseline](https://raw.githubusercontent.com/getsentry/sentry/master/.github/codeowners-coverage-baseline.txt) - 2,481 lines carrying 2,470 uncovered paths, under the header "Goal: Reduce this list to zero". The ratchet, as a shipped artefact. `0540`.
- [`discourse/discourse`](https://github.com/discourse/discourse) - GPL-2.0. The worked scoring example in `0550`: `AI-AGENTS.md` with `AGENTS.md` and `CLAUDE.md` as 12-byte symlinks to it, 15 scripts in `bin/`, 17 skills in `.skills/`, a 574-byte root `CODEOWNERS`, 19 workflows, and the devcontainer quoted in `0530`.
- [`keycloak/keycloak`](https://github.com/keycloak/keycloak) - the contrast case in `0550`: no root `AGENTS.md`, no `CLAUDE.md`, no container definition, and a vendor-specific `.github/copilot-instructions.md` instead.

### Module 06 - Agentic code review

- [Factory - review benchmark](https://docs.factory.ai/benchmarks/review-benchmark) and [`droid-code-review-evals/review-droid-benchmark`](https://github.com/droid-code-review-evals/review-droid-benchmark) - the open head-to-head data behind `0610` and `0620`. **The benchmark repository carries no LICENSE file**, so the numbers may be cited and the method described, and nothing may be reproduced verbatim.
- [Google Research - resolving code review comments with ML](https://research.google/blog/resolving-code-review-comments-with-ml/) and [AutoCommenter](https://arxiv.org/abs/2405.13565) - published production results rather than vendor benchmarks. `0660`.
- [MetaMateCR](https://arxiv.org/abs/2507.13499) - the production numbers and the safety trial. `0660`.
- [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) (MIT) and its [solutions](https://raw.githubusercontent.com/anthropics/claude-code-action/main/docs/solutions.md) - reproducible verbatim. `0650`.
- [Cursor - Bugbot](https://cursor.com/docs/bugbot) and [CodeRabbit - the YAML reference](https://docs.coderabbit.ai/reference/yaml-template) - the two rules-file formats `0640` compares.
- [GitHub - available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) and [about CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) - the authority beat in `0650`.
- [Cognition - Devin Review](https://docs.devin.ai/work-with-devin/devin-review) and [the announcement](https://cognition.com/blog/devin-review) - `0670`.
- [Semgrep - rule syntax](https://docs.semgrep.dev/writing-rules/rule-syntax) - the required rule fields, the four severity values and the `paths` section. The rule `0640` shows is written for this course, so the course owns it; rule *syntax* is not licensable. Anyone copying a registry rule instead must read that repository's own licence rather than assume it.
- [Factory - automated code review in CI](https://docs.factory.ai/software-factory/code-review-ci.md) - the trigger events, the draft-skipping default, and `deep` against `shallow` as one dial. Cited by `0630` and `0650`. [Factory - the local `/review` command](https://docs.factory.ai/software-factory/code-review.md) carries the P0 to P3 severities `0670` compares.
- [Claude Code - subagents](https://code.claude.com/docs/en/sub-agents) - the `.claude/agents/` location and the frontmatter fields, including the `tools` line that is the architecture decision. The reviewer subagent in `0640` uses these fields with a body written for this course.
- [GitHub Copilot - configure coding guidelines](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/configure-coding-guidelines) - `.github/copilot-instructions.md` and the path-specific instruction files, for the rules-file comparison in `0640`. GitHub Docs are CC BY 4.0.
- [Greptile - v4](https://www.greptile.com/blog/greptile-v4) - acceptance rising 30% to 43% and addressed comments per pull request rising 0.92 to 1.60, with "addressed" determined by an LLM. **Vendor-stated**; `0660` labels it MARKETING and says what would make it evidence.
- [Cognition - how Cognition uses Devin to build Devin](https://cognition.com/blog/how-cognition-uses-devin-to-build-devin), [Devin's 2025 performance review](https://cognition.com/blog/devin-annual-performance-review-2025), [DeepWiki](https://docs.devin.ai/work-with-devin/deepwiki) and [Windsurf Codemaps](https://cognition.com/blog/codemaps) - the rest of `0670`'s public material. Every quantitative claim in the first two is self-reported with no method and no comparison group, and the page says so. The `.devin/wiki.json` field names come from the DeepWiki page; the contents shown are the course's own.
- [Google - AutoCommenter, full text](https://arxiv.org/html/2405.13565v1) - the readable form of the paper already listed above, and the one `0600`, `0610` and `0640` quote from.

### Module 07 - Security

- [OWASP - LLM01 prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) - the definition, direct against indirect, the prevention strategies. `0720`.
- [Semgrep - rule syntax](https://docs.semgrep.dev/writing-rules/rule-syntax) and [taint mode](https://docs.semgrep.dev/writing-rules/data-flow/taint-mode) - the whole of `0710`. **The rules repository carries "Semgrep Rules License v1.0", not an OSI licence**; the engine is LGPL-2.1. Check before reproducing a rule.
- [Semgrep - supply chain](https://docs.semgrep.dev/semgrep-supply-chain/overview), [secrets](https://docs.semgrep.dev/semgrep-secrets/conceptual-overview), [Assistant](https://docs.semgrep.dev/semgrep-assistant/overview), [CI configs](https://docs.semgrep.dev/semgrep-ci/sample-ci-configs) - `0700`, `0750`, `0760`, `0770`.
- [OSV-Scanner](https://google.github.io/osv-scanner/), [gitleaks](https://github.com/gitleaks/gitleaks) (MIT), [TruffleHog](https://github.com/trufflesecurity/trufflehog) (AGPL-3.0) - the other two scanners in `0700` and `0750`.
- [CodeQL - the SQL injection query](https://raw.githubusercontent.com/github/codeql/main/javascript/ql/src/Security/CWE-089/SqlInjection.ql) - `0710`.
- [Claude Code - sandboxing](https://code.claude.com/docs/en/sandboxing), [security](https://code.claude.com/docs/en/security), [permissions](https://code.claude.com/docs/en/permissions) - `0730` and `0740`.
- [MCP - security best practices](https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices), [Invariant Labs - tool poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks), [Trail of Bits - line jumping](https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/) - the named attack classes in `0720`.
- [Design patterns for securing LLM agents against prompt injection](https://arxiv.org/abs/2506.08837) - `0730`.
- [Semgrep - introduction](https://docs.semgrep.dev/introduction) - the product family in Semgrep's own words, and the "over 30 programming languages" figure. `0700`, `0770`.
- [Semgrep - the MCP server](https://github.com/semgrep/mcp) (MIT) - seven tools, one prompt and two resources, and the turn from scanning in CI to scanning inside the loop. `0770`.
- [Semgrep - a security engineer's guide to MCP](https://semgrep.dev/blog/2025/a-security-engineers-guide-to-mcp/) - their own MCP threat model, and the path traversal they found in their own server. `0720`, `0770`.
- [Semgrep - Cursor hooks and the MCP server](https://semgrep.dev/blog/2025/cursor-hooks-mcp-server/) - the `afterFileEdit` plus `stop` hook pattern, quoted. `0770`.
- [Semgrep Rules License v1.0](https://semgrep.dev/legal/rules-license) - why `semgrep/semgrep-rules` is linked rather than reproduced. `0710`.
- [GitHub - responsible use of Copilot Autofix](https://docs.github.com/en/code-security/code-scanning/managing-code-scanning-alerts/responsible-use-autofix-code-scanning) - the documented inputs, the non-determinism sentence, the 2,300-alert test corpus, and five named failure modes. `0760`.
- [GitHub - about push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection) - what it blocks, and its bypass. `0750`.
- [GitHub - Dependabot configuration options](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file) - the five-pull-request default and grouping. GitHub Docs code samples are MIT ([`LICENSE-CODE`](https://github.com/github/docs/blob/main/LICENSE-CODE)). `0750`.
- [OSV-Scanner - the GitHub Action](https://google.github.io/osv-scanner/github-action/) - the reusable workflow and the `security-events: write` scope SARIF upload needs. `0750`.
- [Claude Code - permission modes](https://code.claude.com/docs/en/permission-modes) - the six modes, and the two rules about `bypassPermissions`. `0730`.
- [Claude Code - hooks](https://code.claude.com/docs/en/hooks) - the `PreToolUse` input schema, the exit-code contract and `permissionDecision`. `0740`.
- [bubblewrap](https://github.com/containers/bubblewrap) and [gitignore pattern syntax](https://git-scm.com/docs/gitignore) - the two external mechanisms the sandbox and the file rules rest on. `0730`, `0740`.

### Module 08 - Background agents

- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web), [cloud environments](https://code.claude.com/docs/en/cloud-environments), [GitHub Actions](https://code.claude.com/docs/en/github-actions), [Slack](https://code.claude.com/docs/en/slack) - `0800` to `0830`.
- [GitHub Copilot coding agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent), [Cursor background agent](https://cursor.com/docs/background-agent), [Devin](https://docs.devin.ai/get-started/devin-intro), [Jules](https://jules.google/docs) and [its usage limits](https://jules.google/docs/usage-limits/), [Codex cloud](https://learn.chatgpt.com/docs/cloud) - the six in `0810`. **Only one of them publishes concurrency numbers**, which is the evidence that `0810` is written on the mechanism axis rather than the product axis.
- [Linear - agents](https://linear.app/developers/agents) - the delegation model in `0820`.
- [git-worktree](https://git-scm.com/docs/git-worktree) and [GitHub merge queues](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue) - the contention mechanics in `0840`.
- [Cloudflare - Agents SDK](https://developers.cloudflare.com/agents/), [the API reference](https://developers.cloudflare.com/agents/api-reference/agents-api/), [remote MCP](https://developers.cloudflare.com/agents/guides/remote-mcp-server/), [AI Gateway](https://developers.cloudflare.com/ai-gateway/) - `0860`.

### Module 09 - Building an AI-native team

- [MCP - authorization, current revision](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) and [the superseded one](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - the whole of `0910` and its comparison table.
- [Cloudflare - enterprise MCP](https://blog.cloudflare.com/enterprise-mcp/) and [MCP portals](https://developers.cloudflare.com/cloudflare-one/access-controls/ai-controls/mcp-portals/) - the tool-count measurement `0900` carries, and the link back to `0270`.
- [Docker - MCP gateway](https://docs.docker.com/ai/mcp-gateway/) and [the MCP registry](https://github.com/modelcontextprotocol/registry) - the three things people call one word in `0900`.
- [Claude Code - managed settings](https://code.claude.com/docs/en/managed-settings), [settings](https://code.claude.com/docs/en/settings), [LLM gateway](https://code.claude.com/docs/en/llm-gateway), [costs](https://code.claude.com/docs/en/costs), [monitoring usage](https://code.claude.com/docs/en/monitoring-usage), [analytics](https://code.claude.com/docs/en/analytics) - `0920` to `0960`.
- [LiteLLM routing](https://docs.litellm.ai/docs/routing), [Portkey](https://portkey.ai/docs/product/ai-gateway), [OpenRouter provider routing](https://openrouter.ai/docs/features/provider-routing) - the three gateway configurations in `0930`.
- [Replit - automated self-testing](https://replit.com/blog/automated-self-testing) and [the agent docs](https://docs.replit.com/replitai/agent) - `0970`.
- [Stack Overflow developer survey, AI section](https://survey.stackoverflow.co/2025/ai) and [the DORA report](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report) - the adoption-against-trust gap in `0960`.

### Module 10 - The software factory and the future

- [Claude Code - routines](https://code.claude.com/docs/en/routines) and [scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks) - `1010`.
- [Anthropic - how Anthropic secures its AI-native SDLC](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle) and [how we contain Claude](https://www.anthropic.com/engineering/how-we-contain-claude) - agent identity, audit, egress control. `1030` and `1040`.
- [NBER working paper 35275, Demirer, Musolff and Yang](https://www.nber.org/papers/w35275) - the commit-to-project-to-release attenuation. **The single most important number in module 10**, and the chart `1050` owes the reader.
- [METR - measuring task horizons](https://arxiv.org/abs/2503.14499) and [SWE-bench](https://arxiv.org/abs/2310.06770) - the capability half of `1050`.
- [QEMU code provenance](https://www.qemu.org/docs/master/devel/code-provenance.html), [the LLVM AI tool policy](https://llvm.org/docs/AIToolPolicy.html), [curl's contributing guide](https://github.com/curl/curl/blob/master/docs/CONTRIBUTE.md), [Fedora's proposed policy](https://communityblog.fedoraproject.org/council-policy-proposal-policy-on-ai-assisted-contributions/) - the four open-source positions the contribution track on `1130` must respect.

## Wisdom

Where the practitioners argue, for a reader who wants to test their understanding against people who do this.

- [Simon Willison's blog](https://simonwillison.net/) - the running commentary on prompt injection and agent security, and the place a new attack class usually gets named first.
- [The Model Context Protocol SEP discussions](https://github.com/modelcontextprotocol/modelcontextprotocol/pulls) - where a protocol change is argued before it is a specification, which is the honest way to see how fast this field moves.
- [The AGENTS.md discussion threads](https://github.com/openai/agents.md) - what teams actually put in the file, and what they regret putting in it.

## Not used, and why

- **`openai.com`.** Unreachable to agent tooling behind a bot challenge, and this course never bypasses one. OpenAI claims are routed through arXiv, GitHub or `learn.chatgpt.com` instead, and a blog-only claim is labelled as third-party sourced.
- **`web.archive.org`.** Also blocked. A source that is only reachable through an archive is a source this course does not cite.
- **Third-party "best AI code reviewer" comparisons.** Every one found was an aggregator without a published method. `0620`'s numbers come from an open benchmark whose method can be read, or from published production research, and from nothing else.
- **Vendor benchmark pages with no method.** Cited only as MARKETING inside a `.callout.warn`, never as evidence.
- **The research reports behind this course.** They are working material and are never cited by path. Find the public source underneath the claim, exactly as `coding-harness-course` requires.

## Gaps

Claims this course would like to make and cannot source.
**A gap recorded here is a gap the course does not assert on a page.**

- **RePPIT's speed claim.** The only public source for the framework states a speed-up with no method behind it. `0220` teaches the five moves and labels the number MARKETING.
- **Cursor, Devin and Factory review accuracy.** None of the three publishes precision or recall against a method a reader can inspect. `0620` uses the one open benchmark and says so.
- **Concurrency and rate limits for five of the six cloud agents.** Only one publishes them. `0810` is written on the mechanism axis for this reason, and the absence is itself worth stating on the page.
- **Whether agent-readiness scores predict anything.** The rubric in `0550` is a teaching instrument. No published study relates a readiness score to an outcome, and the page must not imply one.
- **A licence for the open review benchmark.** The repository ships no LICENSE file. Numbers may be cited, method may be described, nothing may be reproduced.
- **What model-assisted triage is worth on your own repository.** Semgrep publishes "over 95% accurate" for categorising false positives with no method, corpus or evaluation set; GitHub publishes the size of its auto-fix test corpus and no aggregate fix rate. `0760` states both as published and neither as evidence, and its calculator asks the reader for the number instead.
- **Adoption figures that measure delivery rather than activity.** Every available metric measures activity. `0960` says so rather than substituting a proxy.
- **EARS notation as a Kiro convention.** Third-party writing attributes "WHEN [condition] THE SYSTEM SHALL [behaviour]" to Kiro's `requirements.md`. It is not on `kiro.dev/docs/specs/`, which describes the file as capturing stories and acceptance criteria "in structured notation" without naming one. `0230` quotes Kiro's own wording for its three files and does not name EARS.
- **Any cap on the number of tools Cursor will mount.** Older third-party writing cites a forty-tool limit. Cursor's own MCP documentation states none, and no Cursor-owned page could be found either way, so `0250` and `0270` say nothing about a cap.
- **Cursor's `.cursor/mcp.json` behaviour, run rather than read.** Cursor is not installed in the authoring environment, so `0250`'s Cursor configuration is quoted from Cursor's documentation and its caption says "documented rather than run". The Claude Code half was written into a scratch repository and the two MCP servers were built and driven with raw JSON-RPC.
- **Any published token cost for the tool-search reduction on a named setup.** The "over 85 percent" figure is stated as a typical reduction rather than measured on the five-server example it accompanies, so `0270`'s second bar in that pair is a derived floor and its caption says so.
- **A version number for the Agent Skills standard.** `agentskills.io/specification` carries no version string and no revision name. Module 3 therefore never writes "Agent Skills v1.x"; it names the field constraints and where they were read.
- **Whether Gemini CLI can resume a session by its id.** Its `cli-reference.md` documents `-r` as `"latest"` or an index number and names no id form. `0360`'s matrix records that cell as undocumented rather than asserting it either way.
- **A licence for Cursor's documentation.** The site states none, so `0330`, `0360` and `0370` paraphrase its tables, quote only short individual descriptions, and ship a hook script written for this course instead of the one Cursor publishes.

