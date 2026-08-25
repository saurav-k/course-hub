# MISSION - Herdr from Zero

## Why this course exists

[Herdr](https://herdr.dev) is a background terminal server that owns the panes your
coding agents run in, classifies each agent's state (working, blocked, idle, done) by
reading the pane, and lets plugins extend it as plain executables behind one manifest.
Nothing else in this hub covers its three ideas - a server that owns real terminals, an
agent-state detector, and a plugin system where the whole contract is a manifest plus
ordinary commands - and a reader who meets them cold has nowhere to start.

This course is that starting point. It teaches Herdr from nothing: no terminal
multiplexer experience assumed, no coding-agent experience assumed.

## Who it is for

A developer who has never used tmux, zellij, or screen, and who may never have run a
coding agent in a terminal. Every term is defined where it first appears or in a named
earlier lesson. The ladder:

- **foundation** (`pill easy`) - arrives cold; Lessons 01, 05, 08, 09.
- **working** (`pill med`) - has the foundation pages; can be handed a mechanism and a
  trade-off directly. Lessons 02, 03, 04, 06, 07, 10, 11, 12, 13.
- **frontier** - not used. Nothing here is an open research question, and pretending
  otherwise would be dishonest.

## What done looks like

After the five modules the learner can:

1. Explain what Herdr is and how the keeper/viewer split works (01-02).
2. Name the object model and say how agent-state detection works (03-04).
3. Install, configure, update and reach Herdr on their own machine (05-07).
4. Say which of their own workflows it fits, and which it does not (08).
5. Write, test and publish a working plugin (09-13).

## What is out of scope

- **The agents themselves.** How Claude Code, Codex, Cursor or opencode work is those
  projects' business. This course treats an agent as "a process in a pane" and stops
  there. The hub's Production Agent Engineering course owns the agents side.
- **General terminal-multiplexer teaching.** tmux appears only as contrast. A reader
  who wants to learn tmux should learn tmux.
- **Contributing to Herdr's Rust internals.** The course reads the repository as
  evidence for how the shipped binary behaves; it does not teach the codebase.
- **The full ~100-method socket API.** Lesson 12 covers the surface plugins get and
  names where the complete API reference lives.

## Shape and canon

One content-page shape throughout: one tight idea per lesson, mental model first,
mechanism second, trade-off third. The canon every lesson returns to is the herdr.dev
documentation and the [Herdr repository](https://github.com/herdrdev/herdr) at
0.8.2-era master, cited file-and-line; see `RESOURCES.md`.

Three recurring metaphors are introduced once and reused: the night watchman (the
server), sticky notes (detection manifests), and the hotel that photographs every room
nightly (persistence).
