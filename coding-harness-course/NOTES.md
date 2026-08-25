# Notes

How this course teaches, and what the authoring cost.
Read `MISSION.md` first for why it exists, then `BUILDER-SPEC.md` for what differs from the house standard.

## Learner profile

A working engineer, three to fifteen years in, who drives a coding agent daily from the outside: they type prompts, review diffs, and have opinions about which agent is better, but have never read a line of any harness.
They are fluent in shell, git, and HTTP APIs, so curl-level analogies land and nothing about terminals needs explaining.
What reads as friction: being told abstractions ("the harness manages context") without the artifact behind them.
They asked, in effect, for the tour they cannot give themselves - "what am I actually running?"

## Cadence

One page is one concern, 900 to 1,400 prose words, four to six figures.
The orientation figure on a mechanism page draws where the concern sits in the seven-layer stack; on a deep dive it draws that harness's loop shape against the generic turn.
Quizzes come after the idea is worked; one practice problem per page invites the reader to run or read something real.

The deep dives repeat a skeleton deliberately.
Repetition of structure is how fifteen artifacts become comparable instead of fifteen separate essays.

## Teaching preferences

- **The contrast carries the teaching.** "Gemini CLI repairs a failed edit with a second model call; Codex CLI repairs it with a grammar-tolerant re-match" teaches more than either fact alone.
- **Name things.** `apply_patch`, `.mcp.json`, `PreToolUse`, `MEMORY.md` - real identifiers from pinned sources, not generic nouns.
- **Trust postures get symmetrical treatment.** Ask-first, sandbox-first, classify-first, and nothing-at-all each get their failure mode named in the same breath as their benefit.
- **Never mock the wrapper believer.** The cold spot is reasonable - early harnesses were thin wrappers. The teaching move is showing what changed and when, not condescension.

## Structure decisions

- **Lesson numbers step in tens** (0000, 0010 ... 0270) because the issue numbers are the spine and inserting a page later costs nothing. Recorded in `BUILDER-SPEC.md`; every author must follow it.
- **Deep dives sit after all mechanism modules**, not interleaved, so a mechanism page can forward-reference "you will see this again in the Claude Code deep dive" without a cycle.
- **The models module sits before the deep dives**: per-family behavior is vocabulary the deep dives use constantly (why Codex speaks patch dialect, why opencode swaps edit tools off).

## Known gotchas

- **Mermaid labels full of tool names.** This subject's text is full of parentheses, dots, and dashes (`Bash(npm run test *)`, `mcp__server__tool`). Every Mermaid node label must be double-quoted, always - bare labels break on the first parenthesis.
- **Underscores render as emphasis in figcaptions.** Write `mcp__server__tool` inside `<code>` in captions and prose, never bare.
- **Sequence diagrams want participant names short.** The turn-cycle diagrams name real stages but keep participants to one word (`Harness`, `Gate`, `Tools`); long names blow out width and shrink below legibility.
- **Token numbers age fast.** Startup token estimates are version-specific measurements. Every figure quoting one says the version and marks the estimate as illustrative, and the prose never leans on the exact value.

## Honesty notes

- Five harnesses (Claude Code, Cursor, Windsurf, Antigravity core, Copilot ghost-text) are closed; pages about them say so and cite documentation, never decompilation folklore. Each closed-source page carries the limit in its `.callout.warn`.
- Where a report recorded "retry behavior undocumented", the lesson records exactly that rather than guessing from behavior observed once.

## Open threads

- Deep dives 0120 through 0260 are unwritten; each is an issue in the epic with its report already in hand.
- Whether code mode (issue 0090) deserves a second page once Codex and opencode implementations are compared closely.
- The capstone scope (0270): minimal loop plus permission gate is the current plan; whether MCP client support fits in the word ceiling is undecided until the Extending module is written.
