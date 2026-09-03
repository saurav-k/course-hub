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

### Module 02 - Advanced context engineering

- [Anthropic - prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) - example counts, XML tagging, the prefill migration table. Cited by `0210`.
- [Anthropic - structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) - the replacement for prefill. Cited by `0210`.
- [Wei et al. - Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) and [Wang et al. - Self-Consistency](https://arxiv.org/abs/2203.11171) - the two results `0210`'s chart is drawn from.
- [MCP - Streamable HTTP transport](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http) and [server tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools) - cited by `0240` and `0260`.
- [MCP - build a server](https://modelcontextprotocol.io/docs/develop/build-server) - the current TypeScript and Python quickstarts, and the correct package names. Cited by `0250`.
- [github/spec-kit](https://github.com/github/spec-kit) (MIT) and [Kiro - specs](https://kiro.dev/docs/specs/) - the two spec-driven toolchains `0230` compares.
- [Mihail Eric - RePPIT](https://mlops.community/blog/reppit-a-framework-to-ship-production-code-2-3x-faster) - the only substantive public source for RePPIT, and the source of an unevidenced speed claim. `0220` must label that claim MARKETING.

### Module 03 - Agent skills and the CLI

- [agentskills.io](https://agentskills.io/) - what a skill is, and which clients read the format.
- [Claude Code - skills](https://code.claude.com/docs/en/skills), [headless](https://code.claude.com/docs/en/headless), [CLI reference](https://code.claude.com/docs/en/cli-reference) - cited by `0300` to `0360`.
- [anthropics/skills](https://github.com/anthropics/skills) - real skills to read. **Individual skills carry their own licence**; the document skills are described as source-available and must not be reproduced.
- [Cursor - rules](https://cursor.com/docs/context/rules), [skills](https://cursor.com/docs/context/skills), [CLI parameters](https://cursor.com/docs/cli/reference/parameters) - cited by `0330` and `0370`.
- [Codex - build skills](https://learn.chatgpt.com/docs/build-skills) and [Gemini CLI](https://github.com/google-gemini/gemini-cli) - the other two precedence models in `0330`.

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
- [Cognition - how Cognition uses Devin to build Devin](https://cognition.com/blog/how-cognition-uses-devin-to-build-devin) - the best published statement of the agent-perception gap. `0500`.

### Module 06 - Agentic code review

- [Factory - review benchmark](https://docs.factory.ai/benchmarks/review-benchmark) and [`droid-code-review-evals/review-droid-benchmark`](https://github.com/droid-code-review-evals/review-droid-benchmark) - the open head-to-head data behind `0610` and `0620`. **The benchmark repository carries no LICENSE file**, so the numbers may be cited and the method described, and nothing may be reproduced verbatim.
- [Google Research - resolving code review comments with ML](https://research.google/blog/resolving-code-review-comments-with-ml/) and [AutoCommenter](https://arxiv.org/abs/2405.13565) - published production results rather than vendor benchmarks. `0660`.
- [MetaMateCR](https://arxiv.org/abs/2507.13499) - the production numbers and the safety trial. `0660`.
- [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) (MIT) and its [solutions](https://raw.githubusercontent.com/anthropics/claude-code-action/main/docs/solutions.md) - reproducible verbatim. `0650`.
- [Cursor - Bugbot](https://cursor.com/docs/bugbot) and [CodeRabbit - the YAML reference](https://docs.coderabbit.ai/reference/yaml-template) - the two rules-file formats `0640` compares.
- [GitHub - available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets) and [about CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) - the authority beat in `0650`.
- [Cognition - Devin Review](https://docs.devin.ai/work-with-devin/devin-review) and [the announcement](https://cognition.com/blog/devin-review) - `0670`.

### Module 07 - Security

- [OWASP - LLM01 prompt injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) - the definition, direct against indirect, the prevention strategies. `0720`.
- [Semgrep - rule syntax](https://docs.semgrep.dev/writing-rules/rule-syntax) and [taint mode](https://docs.semgrep.dev/writing-rules/data-flow/taint-mode) - the whole of `0710`. **The rules repository carries "Semgrep Rules License v1.0", not an OSI licence**; the engine is LGPL-2.1. Check before reproducing a rule.
- [Semgrep - supply chain](https://docs.semgrep.dev/semgrep-supply-chain/overview), [secrets](https://docs.semgrep.dev/semgrep-secrets/conceptual-overview), [Assistant](https://docs.semgrep.dev/semgrep-assistant/overview), [CI configs](https://docs.semgrep.dev/semgrep-ci/sample-ci-configs) - `0700`, `0750`, `0760`, `0770`.
- [OSV-Scanner](https://google.github.io/osv-scanner/), [gitleaks](https://github.com/gitleaks/gitleaks) (MIT), [TruffleHog](https://github.com/trufflesecurity/trufflehog) (AGPL-3.0) - the other two scanners in `0700` and `0750`.
- [CodeQL - the SQL injection query](https://raw.githubusercontent.com/github/codeql/main/javascript/ql/src/Security/CWE-089/SqlInjection.ql) - `0710`.
- [Claude Code - sandboxing](https://code.claude.com/docs/en/sandboxing), [security](https://code.claude.com/docs/en/security), [permissions](https://code.claude.com/docs/en/permissions) - `0730` and `0740`.
- [MCP - security best practices](https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices), [Invariant Labs - tool poisoning](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks), [Trail of Bits - line jumping](https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/) - the named attack classes in `0720`.
- [Design patterns for securing LLM agents against prompt injection](https://arxiv.org/abs/2506.08837) - `0730`.

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
- **Adoption figures that measure delivery rather than activity.** Every available metric measures activity. `0960` says so rather than substituting a proxy.
