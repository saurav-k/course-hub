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

7. **Never link a local `.md` file from a page.**
   The deploy syncs everything except `*.md`, so the link works from disk and returns a 404 on the live site. Name the file in `<code>` instead. The validator fails the pull request on it.

8. **Validate before you open the pull request.**

   ```bash
   python3 scripts/validate_site.py
   ```

   If it fails, fix it. Do not open a pull request you know is red.

## Before you write anything

Read, in this order:

0. `.claude/skills/course-authoring/SKILL.md` - the house standard for every page: the page
   contracts, the widget markup, the teaching bar, and the verification gate. Read it before the
   course-specific files below. Claude Code loads it on its own; every other agent has to open it.

1. The target course's `MISSION.md` - why the course exists and what is out of scope. This is canonical.
2. Its `NOTES.md` - teaching style, cadence, and known gotchas.
3. Its `BUILDER-SPEC.md` - the authoring spec, including exact widget markup.
4. Its `RESOURCES.md` - the sources the course already trusts.
5. Two or three neighbouring lessons - match their voice, depth, and structure.

Do not infer the house style from this file. Infer it from the lessons.

## Writing a lesson

- One tight idea per lesson, mental model first, then the mechanism, then the trade-offs.
- Full normal prose. Complete sentences. No terse fragments in published content, whatever style the chat conversation is using.
- Include active-recall widgets. Copy the exact markup documented in the `assets/hub.js` header; do not invent your own widget shape.
- A Mermaid diagram is a `<div class="mermaid">`, never a `<pre class="mermaid">`. `assets/hub.js` appends a copy button to every `<pre>`, and Mermaid renders from the element's `textContent`, so a `pre` silently picks up the word `copy` as a final line of graph source and the diagram renders as a syntax error. Nothing reaches the console, so always look at the figures rather than counting them.
- Make quiz options match in word and character count. A visibly longer correct answer leaks the answer.
- File it as `lessons/NNNN-kebab-case.html`, continuing the existing sequence.
- Link `../../assets/hub.css`, and load `../../assets/hub.js` and `../outline.js` from the head.
  Do not inline a copy of the design system.
- Run `python3 scripts/gen_outline.py <course-name>` after adding the lesson, and commit outline.js.
- Add a `← Course map` link back to `../index.html`.
- Register the lesson as a card in the course `index.html`. The validator fails the pull request otherwise.
- Cite primary sources - the paper, the RFC, the vendor docs. Add anything new to `RESOURCES.md`.
- Use relative links only. Cross-course links look like `../../llm-papers-course/index.html`.

## Adding a new course

Create a top-level folder with its own `index.html` and `lessons/`. It needs no `assets/`
folder unless it has rules of its own; it links the hub design system like every other course.
Generate its `outline.js` before opening the pull request, give it a hue in the course-accent
block of `assets/hub.css`, write its `MISSION.md` before any lesson, and add a card for it in
the hub `index.html`. Nothing else is needed: the pipeline syncs the whole hub, so merging the pull request publishes the new course on its own.

A course may instead ship a `routes.js` manifest, which lets one pool of lessons be read along several named routes. `llm-evolution-course` is the one that does; `llm-evolution-course/routes/README.md` is the reference for the mechanism, and `scripts/gen_outline.py` refuses to run against such a course.

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

There is now **one** design system and one copy of it: `assets/hub.css` plus `assets/hub.js`,
linked by every page in the hub. The old `assets/course.css` / `course.js` pair and its six
byte-identical copies are gone. A course owns only its palette, not the design system: the three
`assets/course-extras.css` files that remain, in `llm-evolution-course`, `llm-inference-course` and
`statistical-foundations-ml-course`, carry rules genuinely unique to those courses and are layered
*after* the hub sheet. They still restyle shared elements - `.lab h4` and `.stub-note h4` among
them - so before you change any element or widget selector, grep **every** `*.css` in the
repository for it, not just `hub.css`.

Every page also loads its course `outline.js`, generated by `scripts/gen_outline.py`, which is
what the sidebar reads. `llm-evolution-course` ships `routes.js` instead; see
`llm-evolution-course/routes/README.md`.

`hub.js` writes three attributes on `<html>` in its head phase, before the first paint:
`data-mode` and `data-palette` are the reader's choices, and `data-course` is the course folder,
read straight out of the URL. `hub.css` turns `data-course` into a hue offset and rotates the
palette accent by it in OKLCH, so each course wears a distinguishable accent drawn from whichever
palette the reader picked. **A new course needs a line in that block**; without one it falls back
to the plain palette accent. The rotated value reaches the page as `--course-accent` and its 14%
tint as `--course-soft`, and only the chrome uses them - the wordmark, the two progress bars, the
rail's current-lesson chip, a course-map section number and a card's hover border. Verify a new
hue against every palette surface in both modes before you ship it.

Seven traps in that design system, all found on the published site:

- **Theme tokens are declared four times** (`:root`, the `prefers-color-scheme: dark` block, and
  the two explicit-choice selectors, because the toggle must beat the OS). A token added to
  `:root` alone silently keeps its light value in dark mode. Add every new token to all the
  blocks that already carry one, and to `@media print` if it paints anything.
- **`@media print` cannot use a bare `:root`.** The explicit-choice selector out-specifies it in
  every medium, so a print rule written that way never applies to a reader who toggled dark.
  `hub.css` uses `!important` in the print block for exactly this reason.
- **A heading's tag and its size are separate decisions.** `h1`-`h4` set the outline a screen
  reader navigates by; `.h-sub` (the h3 face) and `.h-label` (the small uppercase h4 face) set how
  big it looks. Fix a broken heading order by retagging the heading and adding the matching class -
  never by leaving the tag wrong because the right one looks wrong.
- **A Mermaid line break must be written `&lt;br/&gt;`, never `<br/>`.** A literal `<br/>` inside a
  `<div class="mermaid">` is parsed by the browser as a real `BR` element. Mermaid's first render
  survives that, but `hub.js` stashes the graph source as `node.textContent` in order to repaint on
  a theme or palette change, and `textContent` drops the `BR` and joins the two halves **with no
  break and no space**. So the diagram is correct until the reader touches the appearance controls,
  and mangled from then on: `Hand-written rulesabout 1950 to 1990`. In a sequence diagram the join
  can merge two statements and the figure becomes a red error box instead. Writing the entity puts
  the literal characters into the text node, so Mermaid sees the tag it expects on every render.
  Relatedly, **a semicolon inside a Mermaid label is a statement separator** and breaks the diagram
  the same way; use a dash.
- **Mermaid ignores most of the theme it is handed for mindmaps, timelines and mindmap roots.**
  Branch colours come from its own `cScale`/`cScaleInv`/`cScalePeer` scale, which `hub.js` now
  supplies from the `--branch-0..7` tokens, and it numbers a section's colour one step ahead of the
  section itself. The root disc is not in that scale at all and is pinned in `hub.css` under
  `g.section-root`. If a diagram type ever appears with a colour that follows neither the palette
  nor those tokens, that is the shape of the bug.
- **Mermaid measures every label at render time**, so anything that changes text metrics after the
  render leaves the box cut to the wrong size and the last word clipped. `hub.js` waits on
  `document.fonts.ready` before the first render for this reason, and hands its off-screen print
  render a container that carries the same `--sans` rule as a real diagram. Both matter: measure in
  the wrong font and the clipping is back, and it looks perfect on the next repaint, which is how
  it survives review.
- **A diagram carries its colours inside the SVG, so it cannot follow the print stylesheet.**
  Re-rendering on `beforeprint` does not work either: `mermaid.run()` is asynchronous and the print
  snapshot is taken first, with the graph source back in the element, so the reader gets pages of
  raw Mermaid text. `hub.js` draws an ink-on-paper copy of every diagram while the browser is idle
  and swaps it in synchronously on `beforeprint`. Anything that changes how diagrams are rendered
  has to keep that copy correct too.

Anything that has to run after Mermaid renders - accessible names, focusable scroll boxes - must
tolerate Mermaid's async draw. `hub.js` drives the render itself and awaits `mermaid.run()`, so it
does the pass when that promise settles. Re-run the pass on `load` and on resize: web fonts and
column width decide what actually overflows, and a box that cannot scroll must never keep a tab
stop it has nothing to do with.

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
