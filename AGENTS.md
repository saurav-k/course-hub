# AGENTS.md

Instructions for AI coding agents working in this repository.
`CLAUDE.md` is a symlink to this file, so Claude Code, Codex, Cursor, and any agent honouring `AGENTS.md` all read the same contract.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) as well. It is the shared human contract and everything in it applies to you. This file adds what is specific to automated contributors.

## What this repository is

A **static course hub**, not a software project.
There is no build, no test suite, no package manifest, and no framework.
Each top-level folder is a self-contained course of hand-authored HTML lessons.
Your job here is almost always authoring or correcting teaching content, not shipping code.

The hub is published as a static website on Amazon S3. A merge into `main` deploys it.

## Hard rules

1. **Never push to `main`.**
   `main` is protected and every change lands through a pull request. Create a branch, commit, push the branch, open the pull request. Stop there.

2. **Never merge your own pull request.**
   A human reviews and merges. Merging publishes the live site.

3. **Never deploy directly.**
   Do not run `aws s3 sync` or any other AWS command. Publishing belongs to `.github/workflows/deploy.yml` and to nothing else. This repository deliberately ships no deploy script and no bucket configuration, so there is nothing here for you to run.

4. **Never touch credentials.**
   Do not read, print, copy, or modify AWS profiles, tokens, or repository secrets. Do not add credentials to any file.

5. **Never add yourself as a commit co-author.**
   No `Co-Authored-By` trailer naming an agent or tool.

6. **Never renumber or rename existing lessons.**
   Their URLs are public and linked. Add new numbers at the end of the sequence.

7. **Validate before you open the pull request.**

   ```bash
   python3 scripts/validate_site.py
   ```

   If it fails, fix it. Do not open a pull request you know is red.

## Before you write anything

Read, in this order:

1. The target course's `MISSION.md` - why the course exists and what is out of scope. This is canonical.
2. Its `NOTES.md` - teaching style, cadence, and known gotchas.
3. Its `BUILDER-SPEC.md` - the authoring spec, including exact widget markup.
4. Its `RESOURCES.md` - the sources the course already trusts.
5. Two or three neighbouring lessons - match their voice, depth, and structure.

Do not infer the house style from this file. Infer it from the lessons.

## Writing a lesson

- One tight idea per lesson, mental model first, then the mechanism, then the trade-offs.
- Full normal prose. Complete sentences. No terse fragments in published content, whatever style the chat conversation is using.
- Include active-recall widgets. Copy the exact markup documented in the course `assets/course.js` header; do not invent your own widget shape.
- Make quiz options match in word and character count. A visibly longer correct answer leaks the answer.
- File it as `lessons/NNNN-kebab-case.html`, continuing the existing sequence.
- Link `../assets/course.css` and `../assets/course.js`. Do not inline a copy of the design system.
- Add a `← Course map` link back to `../index.html`.
- Register the lesson as a card in the course `index.html`. The validator fails the pull request otherwise.
- Cite primary sources - the paper, the RFC, the vendor docs. Add anything new to `RESOURCES.md`.
- Use relative links only. Cross-course links look like `../../llm-papers-course/index.html`.

## Adding a new course

Create a top-level folder with its own `index.html`, `assets/`, and `lessons/`, write its `MISSION.md` before any lesson, and add a card for it in the hub `index.html`. Nothing else is needed: the pipeline syncs the whole hub, so merging the pull request publishes the new course on its own.

## Accuracy

These are teaching materials, so a confident wrong explanation is worse than no lesson.

- Ground every technical claim in a source you actually read. Link it.
- If you are unsure whether something is still true, say so in the pull request rather than asserting it in the lesson.
- Do not invent benchmark numbers, paper results, or API behaviour. Quote the source or leave it out.
- When a lesson summarises a paper, the paper's own claims are the ceiling. Do not extrapolate.

## Scope discipline

- Do the task you were given. Do not reformat, restructure, or "improve" lessons you were not asked to touch - it buries the real change in noise.
- Do not add a build step, a package manager, a framework, or a CSS toolchain. The zero-dependency static shape is deliberate.
- Do not change `.github/workflows/` or `scripts/` unless the task is explicitly about the pipeline.
- If the task needs a decision you cannot make from the repository - a course's direction, a licence question, a deployment change - stop and ask. Do not guess.

## Editing the shared assets

`assets/course.css` and `assets/course.js` exist as **six byte-identical copies**: the hub root
plus each course except `statistical-foundations-ml-course`, which keeps its own retuned pair.
Nothing enforces this - the validator only checks structure and links - so edit the root copy,
then `cp` it over the five course copies and confirm with `md5 assets/course.css */assets/course.css`.
A drifted copy ships silently and only shows up on the live site.

Two traps in that design system, both found on the published site:

- **Theme tokens are declared three times** (`:root`, the `prefers-color-scheme: dark` block, and
  `:root[data-theme="dark"|"light"]`, because the toggle sets `data-theme` and must beat the OS).
  A token added to `:root` alone silently keeps its light value in dark mode. Add every new token
  to all the blocks that already carry one.
- **`@media print` cannot use a bare `:root`.** `:root[data-theme="dark"]` out-specifies it in every
  medium, so a print rule written that way never applies to a reader who toggled dark. Restate print
  overrides at each theme selector.

Anything that has to run after Mermaid renders - accessible names, focusable scroll boxes - lives in
`course.js` and must tolerate Mermaid's async draw; there is no completion hook under `startOnLoad`.

## Maintaining this file

Keep this file for knowledge useful to almost every future agent session in this project.
Do not repeat what the codebase already shows; point to the authoritative file or command instead.
Prefer rewriting or pruning existing entries over appending new ones.
When updating this file, preserve this bar for all agents and keep entries concise.

## What "done" looks like

- The validator passes.
- You opened the page in a browser, clicked every link you touched, and answered every quiz you added.
- Commits are conventional, self-describing, and free of agent co-author trailers.
- The pull request explains what changed, why, and what you verified.
- You stopped at the open pull request and left the merge to a human.
