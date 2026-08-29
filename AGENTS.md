# AGENTS.md

Instructions for AI coding agents working in this repository.
`CLAUDE.md` is a symlink to this file, so Claude Code, Codex, Cursor, and any agent honouring `AGENTS.md` all read the same contract.

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) as well. It is the shared human contract and everything in it applies to you. This file adds what is specific to automated contributors.

## What this repository is

A **static course hub**, not a software project.
There is no build, no test suite, no package manifest, and no framework.
Each top-level folder is a self-contained course of hand-authored HTML lessons.
Your job here is almost always authoring or correcting teaching content, not shipping code.

The hub is published as a static website on Amazon S3, in two stages, from one repository.
A merge into `main` publishes to **pre-production**, the review site.
A push to `prod` publishes to **production**, the live hub.
The section below states the flow; treat it as the deployment contract.

## The two stages

`main` is the staging branch and `prod` is the release branch.

| Branch | Stage | Bucket | Who moves it |
|---|---|---|---|
| `main` | pre-production | `vars.S3_BUCKET_PREPROD` | any merged pull request |
| `prod` | production | `vars.S3_BUCKET` | the captain, by hand |

Nothing you do reaches readers. A merged pull request publishes to pre-production only.
Promotion is a separate human act: the captain opens a pull request from `main` into `prod` and merges it in the GitHub UI, which is a push to `prod` and fires the production publish.
There is no branch sync button for two branches in the same repository, so the promotion pull request is the mechanism, not a convenience.
No agent opens that pull request, merges it, or pushes to `prod` for any reason.

The pre-production site paints a red bar along the foot of every page.
If you are looking at a hub page with no bar, you are looking at the live site.

## Hard rules

1. **Never push to `main`, and never touch `prod` at all.**
   `main` is protected and every change lands through a pull request. Create a branch, commit, push the branch, open the pull request. Stop there.
   `prod` is the release branch. Do not push it, do not merge into it, do not open the promotion pull request, and do not branch your work from it. Promotion to production is the captain's own act.

2. **Never merge your own pull request.**
   A human reviews and merges. Merging publishes the pre-production site, which the captain then reviews before he promotes it.

3. **Never deploy directly.**
   Do not run `aws s3 sync` or any other AWS command, against either bucket. Publishing belongs to `.github/workflows/deploy.yml` and to nothing else. This repository deliberately ships no deploy script and no bucket configuration, so there is nothing here for you to run.

4. **Never touch credentials.**
   Do not read, print, copy, or modify AWS profiles, tokens, or repository secrets. Do not add credentials to any file.

5. **Never add yourself as a commit co-author.**
   No `Co-Authored-By` trailer naming an agent or tool.

6. **Never renumber or rename existing lessons.**
   Their URLs are public and linked. Add new numbers at the end of the sequence.

7. **Never link a local `.md` file from a page.**
   The deploy syncs everything except `*.md`, so the link works from disk and returns a 404 on both published sites. Name the file in `<code>` instead. The validator fails the pull request on it.

8. **Validate before you open the pull request.**

   ```bash
   python3 scripts/validate_site.py
   python3 scripts/check_pages_gate.py
   ```

   If either fails, fix it. Do not open a pull request you know is red.
   `check_pages_gate.py` gates on the difference from `scripts/check-pages-baseline.txt`, so it fails
   on a defect you introduced and never on the debt that was already there. A recorded failure that
   no longer happens also fails, and it prints the one command that takes it out of the file; that is
   how the list only ever gets shorter.

   Touching `assets/hub.css`, `assets/hub.js` or a course's `course-extras.css` adds a third command,
   and it needs Chrome:

   ```bash
   python3 scripts/style_snapshot.py
   ```

## Before you write anything

Read, in this order:

0. `.claude/skills/course-authoring/SKILL.md` - the house standard for every page: the page
   contracts, the widget markup, the teaching bar, and the verification gate. Read it before the
   course-specific files below. Claude Code loads it on its own; every other agent has to open it.

1. The target course's `MISSION.md` - why the course exists and what is out of scope. This is canonical.
2. Its `NOTES.md` - teaching style, cadence, and known gotchas.
3. Its `PLOT.md` - the true reading order: where every lecture and session sits, and what is planned but unwritten.
   Place any new material by it; never append to the bottom because it arrived last.
4. Its `BUILDER-SPEC.md` - the authoring spec, including exact widget markup.
5. Its `RESOURCES.md` - the sources the course already trusts.
6. Two or three neighbouring lessons - match their voice, depth, and structure.

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

Give it the five instruction files before the first lesson is written:
`AGENTS.md`, the course contract for agents, which points at the others rather than repeating them;
`CLAUDE.md`, a symlink to `AGENTS.md`;
`MISSION.md`;
`PLOT.md`, the sequence map - the true reading order, where every lecture and session sits, and everything planned but unwritten; and
`NOTES.md`.
`.claude/skills/course-authoring/templates/` carries starters for all five, and
`.claude/skills/course-authoring/new-course.md` carries the interview question that fills `PLOT.md`.
Fill each from what the course actually is. Eight near-identical generated files would satisfy the letter of this rule and be worthless: a short honest file beats a long generic one.

The order rule that goes into every `PLOT.md`: a course's reading order is its true order,
and a tutorial or lab session that follows a lecture sits after that lecture in the course map,
never in a separate list at the bottom.

A course may instead ship a `routes.js` manifest, which lets one pool of lessons be read along several named routes. `llm-evolution-course` is the one that does; `llm-evolution-course/routes/README.md` is the reference for the mechanism, and `scripts/gen_outline.py` refuses to run against such a course. Its `PLOT.md` names the default route as canonical and points at the manifest rather than duplicating every row.

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
`statistical-foundations-ml-course`, are layered *after* the hub sheet and carry only rules
genuinely unique to those courses. `llm-evolution-course`'s is the one that still restyles shared
elements - `.stub-note h4`, `.routecard`, `.route-map .module` among them - so before you change
any element or widget selector, grep **every** `*.css` in the repository for it, not just
`hub.css`. `llm-inference-course`'s is a comment now: the lab kit it invented, `.lab`, `.term`,
`.metric-grid`, `.checklist` and `.kpi`, was promoted whole into `hub.css` when a second course
needed it, and the file is kept because its pages link it. `statistical-foundations-ml-course`'s
carries `.parts` and `.pn`, which no other course uses.

**A widget has exactly one owner.** A rule that is promoted into `hub.css` is deleted from the
course sheet in the same pull request, and the responsive and print arms move with it rather than
being left behind in the other file. A copy left in a course sheet wins on source order, silently,
and every later change to the hub sheet stops at that course's pages.

**Anything a reader can set has three layers, and never fewer.** `hub.css` declares a
`--x-default`, `hub.js` writes only a `--x-user` property inline on `<html>`, and one resolved
token `--x: var(--x-user, var(--x-default))` is what every rule reads. Only that resolution line
may read a `--*-user` property, and no reader control may write anything else. The reason is
measured: the two reading preferences were applied as inline styles until 2026-08, an inline style
beats every rule that is not `!important`, and a reader who had widened the column was pinned there
for good. It also means a value with a viewport override belongs in a `-default` inside the media
query, not in a second rule on the element - `body { font-size: ... }` at a breakpoint would sit
after the body rule and out-argue the reader. The block at the head of `hub.css` states the rule in
full. Twenty-four tokens carry the form today and they are exactly the reader-reachable ones:
`--font-body`, `--fs-body`, `--lh-body`, `--measure` and the twenty prose-rhythm space roles.
Everything else is a one-layer design token, because a `--*-user` layer on a value no control can
write is dead weight that still has to be kept right in every media query.

**Type, rhythm and shape are tokens too, and a rule reads one rather than a literal.** One block
near the head of `hub.css`, marked "the design axis", carries 304 of them: the three faces by role
plus `--font-ui` for chrome, the type scale, the leading set, weight, tracking, an eight-step space
ramp with a role layer over it, shape, motion and the eyebrow treatment. A hard-coded `1.05rem` in a
rule is a value a second design cannot reach, which is the fork this hub already paid once to
remove. **A rule never reads a `--sp-1` to `--sp-8` ramp step**: those are the defaults the role
tokens are built from, and a ramp step in a rule puts a reading-rhythm distance and a chrome
distance on one token, which is what the split exists to prevent. Six role tokens are the reading
column's rhythm and a later density control may scale those and nothing else; the chrome is
permanently out of its reach, because seven pointer targets there pass SC 2.5.8 only on the spacing
exception. `references/widgets.md`, "The design tokens", is the author-facing summary.

Every page also loads its course `outline.js`, generated by `scripts/gen_outline.py`, which is
what the sidebar reads. `llm-evolution-course` ships `routes.js` instead; see
`llm-evolution-course/routes/README.md`.
**The generator slices a course map at each `.module-h` and runs the last slice to the end of the
file**, so any `href="lessons/..."` below the final module - in a footer, most easily - is collected
as an extra lesson of that module and shows up in the rail as a phantom entry under the wrong
heading. It renders, every link resolves, and `validate_site.py` stays green. Link a lesson from the
hero or from a card, never from below the last module.

`hub.js` writes four attributes on `<html>` in its head phase, before the first paint:
`data-mode` and `data-palette` are the reader's choices, `data-course` is the course folder,
read straight out of the URL, and `data-env` is `preprod` when the hostname carries that word and
absent otherwise, which is what paints the pre-production bar. Every `[data-env="preprod"]` rule in
`hub.css` is therefore dead on the live site, so keep the warning bar keyed off that attribute and
never give it a rule that can match without it. `hub.css` turns `data-course` into a hue offset and rotates the
palette accent by it in OKLCH, so each course wears a distinguishable accent drawn from whichever
palette the reader picked. **A new course needs a line in that block**; without one it falls back
to the plain palette accent. The rotated value reaches the page as `--course-accent` and its 14%
tint as `--course-soft`, and only the chrome uses them - the wordmark, the two progress bars, the
rail's current-lesson chip, a course-map section number and a card's hover border. Verify a new
hue against every palette surface in both modes before you ship it. Pick the offset on the circle,
not just on the offset grid: -175 and +175 differ by only 10 degrees of actual hue, so a full
offset list can collide once it wraps past 180. **The 25-degree grid is now full** - read the block
as absolute hue and every step is taken - so a new course splits a 25-degree gap rather than
extending outwards, and `new-course.md`'s "extend the grid" advice no longer applies. Choose which
gap by whose pages your reader actually holds open beside yours, then prove the candidate with the
canvas readback: `staff-ai-course/learning-records/0001-choosing-the-hue.md` carries the method and
a measured comparison table for four shipped hues. Compare against that table, not against the
paragraph in `hub.css`, whose "worst of the 84 course accents" figures were measured when the hub
had seven courses and were never re-run.

The Cloud Architecture category adds one data-driven widget to the shared system: the capability
matrix (`figure.cmatrix`), rendered by `hub.js` from `cloud-comparison-course/matrix.js`, which is
the single committed home of the capability taxonomy. `validate_site.py` gates that file - row
completeness, cell states, widget binding - and `--vendor-links` extends it with a live fetch of
every vendor link. The widget contract is in the widget reference's "The capability matrix"
section. Four cell states, and no two of them may look alike. The pair that matters is `absent`
against `elsewhere`: both arrive as a `gaps` entry in the same inventory and they make opposite
claims, so **NO EQUIVALENT is reserved for `absent`** and a cell must never imply a cloud cannot do
something it demonstrably can. Which gaps are which is a list the research directory holds, not
something to read out of the prose - the wording does not separate them.

**Prove a change to any of those sheets rather than arguing it.** `scripts/style_snapshot.py` loads
a fixed sample of pages in headless Chrome and records the computed value of every property that
matters, for every class in the closed widget vocabulary, across six palettes and both modes. The
snapshot is committed under `scripts/style-baseline/`, so the answer to "did that refactor move
anything" is a diff rather than a judgement, and the harness names the page, the element shape and
the property when something did move. It also checks the two render states a single capture cannot
see: a page with no `data-mode` under the operating system's preference must compute what the
explicit choice computes, and a page switched after load must compute what the same page computes
when loaded on that setting directly. Read the script's docstring before changing it - the sample,
the property list and the two assertions each carry the reason they are shaped that way.

Twelve traps in that design system, all found on the published site:

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
- **Not every screen token has an `--l-` paper twin, and a missing one is silent.** A canvas that
  redraws for print by swapping the `--` prefix for `--l-` works for `--ink`, `--surface`, `--gold`
  and `--accent`, and fails for the chart tokens: `hub.css` defines no `--l-stat`, `--l-alarm`,
  `--l-prob`, `--l-signal` or `--l-noise`. An undefined custom property is invalid at computed-value
  time, and for `color` that means `inherit`, so the probe hands back the surrounding text colour and
  every series prints in one hue with no error anywhere. Map chart tokens onto paper twins that
  exist (`--l-accent-2`, `--l-warn`, `--l-ink-soft`) rather than onto a name pattern, and always give
  the probe a fallback - `var(--l-stat, #333)` - so the next missing token is loud. Note the `@media
  print` block already greys these tokens for ordinary markup; a canvas cannot use that, because the
  bitmap is painted before the print stylesheet applies, which is why the `beforeprint` redraw exists.
- **Some chart classes are modifiers that colour nothing on their own.** `.ref` sets a dash pattern
  and a width but no stroke, because it is meant to ride on an `s-*` class that already carries the
  colour - `class="s-signal ref"`, not `class="ref"`. Written alone it computes to `stroke: none`
  and draws nothing at all, in every mode, every palette and print, and nothing warns you: the
  element is in the DOM, `getBBox` returns a real box, and a figcaption can happily describe a line
  no reader can see. `hub.css` now gives `.ref` a `var(--ink-faint)` default through
  `.chart :where(.ref)`, held at zero specificity so an `s-*` pairing still wins the colour. Before
  you add a chart class, check whether it sets a paint property or only modifies one, and **look at
  the figure** rather than trusting that the markup is present.
- **A hand-authored chart's text runs off the edge and is then cut there.** `svg.chart` scales its
  `viewBox` to the column, and SVG text neither wraps nor is bounded by the viewBox, so a caption
  or axis note longer than the width simply leaves the box - and the browser's own `overflow:
  hidden` on an outermost `<svg>` clips it at that edge, so the tail of the line is gone rather
  than merely untidy. It is invisible to every check in the repository, because the element is
  present and `getBBox` is happy. At the `640` width these charts use, a `.lbl-sm` line runs out of
  room somewhere past about ninety characters. Keep footnotes short or split them across two
  `<text>` elements, and check the widest line in the rendered figure rather than in the source.
- **Three accessibility floors sit in `hub.css`, and each looks like a rule you could delete.**
  `.chart text` pins `letter-spacing` and `word-spacing` to `normal !important`, so a reader's
  text-spacing stylesheet cannot push a fixed-coordinate label past the clip above - which also
  means **a tracking value added to a chart class does nothing**, because the pin outranks it.
  `.mermaid svg foreignObject` carries `overflow: visible` on the screen sheet, not only in print,
  because Mermaid writes each label's measured width onto the box and any later re-space clips what
  no longer fits. `.spine .home` carries `min-height: 24px` because it was the hub's one SC 2.5.8
  failure; seven neighbouring controls pass only on the spacing exception and the smallest
  compliant one has 2px of headroom, so nothing in the topbar or the rail may be tightened to pay
  for anything else.
- **Code has one size token, `--fs-mono`, and it is written in `em` on purpose.** Both `pre` and
  inline `code` read it, so both track whatever prose surrounds them: a custom property holding a
  relative length is substituted unresolved and resolves at each use, which is exactly what a `rem`
  cannot do. `pre` used to carry `.85rem` against inline code's `.86em` and the two rendered 17%
  apart, with only the `em` half surviving a change to the body size. Do not re-express either in
  `rem`, and do not add a `pre` size inside a media query - the small-screen `.78rem` was that same
  defect a second time. The value is a constant today and becomes a function of the reader's body
  face when the face registry lands; the call sites do not change when it does.

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
