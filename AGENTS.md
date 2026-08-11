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
   Do not run `deploy.sh`, `aws s3 sync`, or any other AWS mutation. Publishing belongs to `.github/workflows/deploy.yml` and to nothing else. `deploy.sh` exists as a human escape hatch only.

4. **Never touch credentials.**
   Do not read, print, copy, or modify AWS profiles, tokens, or repository secrets. Do not add credentials to any file.

5. **Never add yourself as a commit co-author.**
   No `Co-Authored-By` trailer naming an agent or tool.

6. **Never renumber or rename existing lessons.**
   Their URLs are public and linked. Add new numbers at the end of the sequence.

7. **Validate before you open the pull request.**

   ```bash
   python3 scripts/validate_site.py
   shellcheck -x deploy.sh
   ```

   If either fails, fix it. Do not open a pull request you know is red.

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

## Accuracy

These are teaching materials, so a confident wrong explanation is worse than no lesson.

- Ground every technical claim in a source you actually read. Link it.
- If you are unsure whether something is still true, say so in the pull request rather than asserting it in the lesson.
- Do not invent benchmark numbers, paper results, or API behaviour. Quote the source or leave it out.
- When a lesson summarises a paper, the paper's own claims are the ceiling. Do not extrapolate.

## Scope discipline

- Do the task you were given. Do not reformat, restructure, or "improve" lessons you were not asked to touch - it buries the real change in noise.
- Do not add a build step, a package manager, a framework, or a CSS toolchain. The zero-dependency static shape is deliberate.
- Do not change `.github/workflows/`, `deploy.config`, or `scripts/` unless the task is explicitly about the pipeline.
- If the task needs a decision you cannot make from the repository - a course's direction, a licence question, a deployment change - stop and ask. Do not guess.

## What "done" looks like

- The validator passes and `shellcheck -x deploy.sh` passes.
- You opened the page in a browser, clicked every link you touched, and answered every quiz you added.
- Commits are conventional, self-describing, and free of agent co-author trailers.
- The pull request explains what changed, why, and what you verified.
- You stopped at the open pull request and left the merge to a human.
