# Plot - the reading order

The course is one linear order, twenty-eight pages in seven modules.
Lesson numbers step in tens and mirror the epic's issue numbers; nothing is renumbered once published.

| Page | File | Issue | Status |
|---|---|---|---|
| 0000 What a coding harness is - the seven layers | `lessons/0000-what-is-a-coding-harness.html` | #123/#124 | **written** |
| 0010 Agentic system design - the principles behind every harness | `lessons/0010-agentic-system-design.html` | #125 | planned |
| 0020 The turn cycle - the loop every harness runs | `lessons/0020-turn-cycle.html` | #126 | planned |
| 0030 Context engineering - what actually fills the window | `lessons/0030-context-engineering.html` | #127 | planned |
| 0040 The edit problem - applying a change that does not apply | `lessons/0040-edit-problem.html` | #128 | planned |
| 0050 Permission postures - ask, sandbox, classify, or nothing | `lessons/0050-permission-postures.html` | #129 | planned |
| 0060 Identity, provenance and supply chain | `lessons/0060-identity-provenance.html` | #130 | planned |
| 0070 MCP and the tool ecosystem | `lessons/0070-mcp-tool-ecosystem.html` | #131 | planned |
| 0080 Skills, subagents, hooks and modes | `lessons/0080-skills-subagents-hooks-modes.html` | #132 | planned |
| 0090 Code mode - tool calls as generated programs | `lessons/0090-code-mode.html` | #133 | planned |
| 0100 Model affinity - tool-call encoding per family | `lessons/0100-model-affinity.html` | #134 | planned |
| 0110 Compatibility endpoints and model substitution | `lessons/0110-compatibility-endpoints.html` | #135 | planned |
| 0120 Aider - the repo map and the pre-agentic lineage | `lessons/0120-aider-repo-map.html` | #136 | planned |
| 0130 Claude Code - the classifier-gated loop | `lessons/0130-claude-code-classifier-gate.html` | #137 | planned |
| 0140 OpenAI Codex CLI - enforce first, ask second | `lessons/0140-codex-enforce-first.html` | #138 | planned |
| 0150 Cursor - the harness that trains its own models | `lessons/0150-cursor-trains-own-models.html` | #139 | planned |
| 0160 GitHub Copilot Chat - prompts as a component tree | `lessons/0160-copilot-component-tree.html` | #140 | planned |
| 0170 Gemini CLI - the self-healing edit pipeline | `lessons/0170-gemini-cli-self-healing.html` | #141 | planned |
| 0180 Windsurf - the human trajectory as context | `lessons/0180-windsurf-trajectory-context.html` | #142 | planned |
| 0190 Google Antigravity - artifacts as the review surface | `lessons/0190-antigravity-artifacts-review.html` | #143 | planned |
| 0200 Cline - plan and act as two programs | `lessons/0200-cline-plan-act.html` | #144 | planned |
| 0210 Roo Code - the mode system | `lessons/0210-roo-mode-system.html` | #145 | planned |
| 0220 opencode - model behavior as data | `lessons/0220-opencode-behavior-data.html` | #146 | planned |
| 0230 Goose - recipes, scheduling, and the self-scheduling agent | `lessons/0230-goose-recipes-scheduling.html` | #147 | planned |
| 0240 Pi - the agent loop as a library | `lessons/0240-pi-loop-library.html` | #148 | planned |
| 0250 pi-launcher - a signed identity for an agent | `lessons/0250-pi-launcher-signed-identity.html` | #149 | planned |
| 0260 Kimi CLI - model-driven context time travel | `lessons/0260-kimi-dmail-time-travel.html` | #150 | planned |
| 0270 Capstone - build a minimal harness | `lessons/0270-capstone-minimal-harness.html` | #151 | planned |

Planned slugs are working names until their page is written; when a page lands, its card moves out of `.roadmap` into a real one and this table's status flips.
The map in `index.html`, not this file, is what the generator parses.

## Order rules

Orientation first, mechanisms second (loop -> trust -> extending -> models), deep dives third, capstone last.
A deep dive may assume every mechanism module; a mechanism page may name a deep dive forward but never depend on it.
Within deep dives, order follows lineage and familiarity: pre-agentic (Aider) before agentic platforms, terminal agents before IDE forks, the minimal engines (Pi, pi-launcher) late, where they land as a reductio of everything before them.
