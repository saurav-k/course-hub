# Coding Harness Engineering - Resources

The sources this course trusts.
A page cites from here; anything new goes in here first, in the same pull request.

## The canon

Primary only: the repository at the commit a report pinned, or the vendor documentation.
The sixteen research reports behind this course pinned each of these; where a report read source, the commit lives in that report and the lesson links the repository plus the file path it cites.

### The harnesses

- [anthropics/claude-code](https://github.com/anthropics/claude-code) + [official docs](https://code.claude.com/docs/en/overview) - closed source; docs are the evidence. Deep dive 0130, cited throughout the mechanism modules.
- [openai/codex](https://github.com/openai/codex) - Rust CLI, Apache-2.0. `apply_patch` grammar, Seatbelt/bubblewrap sandboxes, execpolicy amendments. Deep dive 0140.
- [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) - TypeScript, Apache-2.0. Self-healing edit cascade (`FixLLMEditWithInstruction`), GEMINI.md tiers. Deep dive 0170.
- [Aider-AI/aider](https://github.com/Aider-AI/aider) - Python, Apache-2.0. Repo map (tree-sitter PageRank), SEARCH/REPLACE edit blocks, architect/editor split. Deep dive 0120.
- [Anysphere Cursor](https://cursor.com/docs) - closed; official documentation only. Run modes, sandbox profiles, Composer/Tab training loop. Deep dive 0150.
- [microsoft/vscode](https://github.com/microsoft/vscode) Copilot Chat sources + [Copilot docs](https://docs.github.com/en/copilot) - MIT chat half; prompts in prompt-tsx. Deep dive 0160.
- [Windsurf Docs](https://docs.windsurf.com) - closed; Cascade, AI Flow trajectory, memories. Deep dive 0180.
- [Google Antigravity](https://antigravity.google/docs) - core closed; SDK Apache-2.0. Artifacts as review surface, nsjail/sandbox-exec/AppContainer grants. Deep dive 0190.
- [ClineBot/cline](https://github.com/ClineBot/cline) - TypeScript, Apache-2.0. Plan/Act session rebuild, checkpoint refs. Deep dive 0200.
- [RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code) - TypeScript, Apache-2.0. Mode system, apply_diff fuzzy matcher. Deep dive 0210.
- [anomalyco/opencode](https://github.com/anomalyco/opencode) - Bun/TypeScript, MIT. Model-behavior compiler over models.dev catalog; nine-stage fuzzy replace. Deep dive 0220.
- [block/goose](https://github.com/block/goose) - Rust, Apache-2.0. Recipes, scheduler-as-tool, MCP-everything extensions. Deep dive 0230.
- [badlogic/pi-mono](https://github.com/badlogic/pi-mono) (earendil-works/pi) - TypeScript, MIT. Agent loop as three libraries; absence-as-architecture. Deep dive 0240.
- [kunchenguid/pi-launcher](https://github.com/kunchenguid/pi-launcher) - C11, MIT. Signed process identity for an agent. Deep dive 0250.
- [MoonshotAI/kimi-cli](https://github.com/MoonshotAI/kimi-cli) - Python, Apache-2.0. D-Mail context time travel, kosong step machine. Deep dive 0260.

### The layer underneath

- [sst/models.dev](https://github.com/sst/models.dev) + [models.dev](https://models.dev) - the capability catalog several harnesses compile from; per-provider quirks in one place. Models module (0100, 0110).
- [Model Context Protocol specification](https://modelcontextprotocol.io) - the tool/resource/prompt protocol every harness in the cast now speaks. Extending module (0070).
- [Agent Skills standard](https://agentskills.io) + Anthropic's skills engineering posts - the SKILL.md contract shared across at least eight harnesses in the cast. Extending module (0080).
- [Anthropic Messages API](https://docs.claude.com/en/api/messages), [OpenAI Responses/Chat APIs](https://platform.openai.com/docs/api-reference), [Gemini API](https://ai.google.dev/gemini-api/docs) - the three wire dialects; thinking-block replay rules live here. Models module.

## Supporting sources

Cited once or twice, by page.

### Orientation

- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) - the agentic loop described by the most-deployed harness; cited by `lessons/0000-what-is-a-coding-harness.html`.
- [The agent SDK agent loop](https://code.claude.com/docs/en/agent-sdk/agent-loop) - turn/message vocabulary (AssistantMessage, tool_use, ResultMessage); cited by lessons 0000 and 0020.
- [Explore the context window](https://code.claude.com/docs/en/context-window) - documented startup token breakdown used as an illustrative measurement in lesson 0000's chart.

### Models module

- [Anthropic: define tools](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools) - `tool_use`/`tool_result` encoding, `tool_choice` semantics, and the constructed tool system prompt; lesson 0100.
- [Anthropic: prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) - prefix order tools/system/messages, breakpoint pricing (1.25x/2x write, 0.1x read), thinking-block retention rules; lesson 0100.
- [OpenAI: function calling](https://platform.openai.com/docs/guides/function-calling) - `function_call` items, strict-mode schema requirements, functions injected into the system message; lesson 0100.
- [OpenAI: prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching) - implicit default breakpoints, GPT-5.6+ explicit mode, effort changes and prefix reuse; lesson 0100.
- [Gemini: thought signatures](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/thinking/thought-signatures) - validation rules, 400-error behavior, ordering rule, `skip_thought_signature_validator`; lesson 0100.
- [Aider model-settings.yml](https://github.com/Aider-AI/aider/blob/main/aider/resources/model-settings.yml) - per-model edit formats and capability flags; lesson 0100.
- [opencode registry.ts](https://github.com/anomalyco/opencode/blob/main/packages/opencode/src/tool/registry.ts) - the GPT apply_patch/edit-write tool swap; lesson 0100.
- [Cline model-tool-routing.ts](https://github.com/ClineBot/cline/blob/main/sdk/packages/core/src/extensions/tools/model-tool-routing.ts) - declarative per-family tool routing rules; lesson 0100.
- [Codex model-provider-info lib.rs](https://github.com/openai/codex/blob/main/codex-rs/model-provider-info/src/lib.rs) - the single-variant `WireApi` enum; lesson 0100.
- [Claude Code: model configuration](https://code.claude.com/docs/en/model-config) - alias slot table per provider, `ANTHROPIC_DEFAULT_*_MODEL`, fallback chains, classifier fallback; cited by lessons 0100 and 0110.
- [Z.ai: Claude Code with GLM Coding Plan](https://docs.z.ai/devpack/tool/claude) - compat base URL, slot remapping, compaction-window patch; lesson 0110.
- [Moonshot: Use Kimi in Claude Code](https://platform.kimi.ai/docs/guide/claude-code-kimi) - all four slots plus subagent, silent-failure table, thinking requirements, `/status` verification; lesson 0110.
- [OpenRouter: Anthropic Messages endpoint](https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-messages) and the [Claude Code integration cookbook](https://openrouter.ai/docs/cookbook/coding-agents/claude-code-integration) - the "Anthropic Skin" and its first-party-only guarantee; lesson 0110.
- [xAI: Grok Build 0.1](https://docs.x.ai/developers/models/grok-code-fast-1) - OpenAI-shapes-only serving, cached-input pricing; lesson 0110.
- [sst/models.dev provider TOMLs](https://github.com/sst/models.dev/tree/main/providers) - `kimi-for-coding` registered under the Anthropic adapter for thinking-block replay; Z.ai coding-plan effort mapping; lesson 0110.
- [MoonshotAI/Kimi-K2 issue #129](https://github.com/MoonshotAI/Kimi-K2/issues/129) - community probe of the unpublished `/anthropic` contract, temperature rescaling; lesson 0110.

## Wisdom

Where practitioners argue, for a reader who wants to test their understanding against people who do this.

- Each harness repository's issues and discussions - design arguments (edit formats, permission defaults) play out in public on the open-source half of the cast.

## Not used, and why

- Third-party "harness internals" blog series and decompiled-bundle walkthroughs - unverifiable provenance next to pinned-commit reports; not needed while primary sources cover the claim.
- Vendor benchmarks (SWE-bench leaderboard claims) - model-plus-harness-plus-scaffold entangled; no clean harness-only signal, so the course teaches mechanisms instead of rankings.

## Gaps

Claims this course would like to make and cannot source.

- Claude Code's exact system-prompt text and per-model prompt differences - unpublished; the course says what the docs say about behavior and marks the rest as not publicly documented.
- Cursor's failed-edit retry path - undocumented in official docs as of the report's fetch date.
- Windsurf `edit_file` retry behavior after a failed apply - undocumented.
