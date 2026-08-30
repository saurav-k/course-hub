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

   Touching `assets/hub.css`, `assets/hub.js` or a course's `course-extras.css` adds four more
   commands, in the order the style job runs them, and they need Chrome:

   ```bash
   python3 scripts/style_snapshot.py
   python3 scripts/type_invariants.py --report
   python3 scripts/contrast_matrix.py
   python3 scripts/focus_walk.py
   ```

   Two branches that each add a check collide in `validate_site.py` on the numbers rather than on
   the code: both claim the next slot in the module docstring's list, both bump its "N checks"
   opening line, and both edit the "Checks 9 to N read the two shared asset files" sentence. Git
   reports it as one conflict and either side taken whole silently drops a check from `main()`.
   Keep both, renumber the later one, and count the list again. The same collision waits in
   `.github/workflows/validate.yml`, where two branches each append a step to the `Computed style`
   job, and in the widget reference, where two sections get inserted at one point.

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
- A figure carries two lines above the drawing: `.fig-cap` names the subject in two to five
  words and `.fig-claim` says in one sentence what the drawing proves, so the picture answers a
  question the reader has already asked. Both are direct children of `figure.diagram`, because
  `hub.css` selects them that way: one wrapped in a `div` for spacing takes no styling and renders
  as body text at figure width, which validates and reaches no console. `validate_site.py` check
  19 fails that shape, a claim with no label, a reversed pair, and either line below the drawing.
  Presence is never checked by machine and must not be: a label cannot be generated. The
  author-facing statement is `.claude/skills/course-authoring/references/widgets.md`, "What a
  figure is".
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
Generate its `outline.js` before opening the pull request, register it under the course
contract in `assets/hub.css`, write its `MISSION.md` before any lesson, and add a card for it in
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

## The panel shell, and the reader control panel

**A panel is built by one shell, `makePanel` in `hub.js`, and never by hand.** The shell owns the
whole contract: drag by pointer and keyboard, the viewport clamp, a position remembered under that
panel's own key, open and close, the focus contract and the settling glide. A panel supplies its
name, its store key, its title and what goes in its body, and it wears `.panel-shell` plus one class
of its own for the two lengths it states. Never copy the contract into a second panel; ask for a
shell. It is **non-modal, has no backdrop and does not close on an outside click**, and none of that
is configurable - a reader parks a panel in order to keep reading beside it. The author-facing
statement is `.claude/skills/course-authoring/references/widgets.md`, "The panel shell". Do not
restate it here.

`hub.js` builds one panel and it reaches every page, with no page markup anywhere. Six controls,
plus motion in the accessibility defaults and one reset: ground (mode and palette), body size,
reading face, measure, line spacing, density. Display face, mono face and eyebrow treatment are
**not** reader controls and must not become them - a reader sets one once and never returns to it,
while a course has every reason to differ on it, so they are author tokens on the course contract
below. The accent is not a control either: expanding it into a picker would put a contrast
criterion in the reader's hands.

**Every control is an input to a derivation.** The measure names characters, the body size names
apparent size, and `--measure`, `--fs-body`, `--fs-mono` and the per-face constants are outputs
nothing may write. See the derived axes under "Editing the shared assets" for why the four are
coupled.

**Density is the one control with a hard limit.** It scales the twenty prose-rhythm roles and
reaches nothing else, because there is no headroom in the chrome: one control already fails SC
2.5.8, seven more pass on the spacing exception, and the smallest compliant control has 2px of
margin. The limit is structural rather than promised - `hub.js` can only write `--*-user` names
that `hub.css` resolves, and those are the twenty-four reader-reachable tokens.

**Each panel has two openers, and a floating cluster in the bottom-right corner of every page is
the second.** Four controls, also built by `hub.js` with no page markup: light and dark, the
appearance launcher, the study notes launcher, and scroll-to-top. It exists because a control nobody finds is a control nobody has, and
the mode toggle is the part that teaches - one click repaints the page, so the launcher beside it
reads as an offer. Both openers wear `aria-expanded` and closing returns focus to whichever one was
used, and the shell owns that: `attachOpener` registers a button rather than replacing the last one,
so a third way in costs one call. Its bottom edge reads `--foot-h` rather than assuming
the foot of the viewport is free, and it sits under the rail's drawer scrim and under every panel
shell, so the corner needs none of the `!important` arms race the reference site's own cluster
carries. Its three tokens are `--dock-target`, `--dock-offset` and `--sp-inset-dock`, all on the
design axis.

The author-facing statement, including the focus contract in full, is
`.claude/skills/course-authoring/references/widgets.md`, "The reader control panel" and "The
floating control cluster". Do not restate it here.

**The second panel on the shell is the study notes panel, and its one hard rule is that the save
state is a fact.** It writes through `setChecked` / `dropChecked`, which set, read back and return
whether the store now holds it, and never through `set` / `drop`, which swallow - right for a
preference, and the defect itself for a document. A failed write shows `Not saved` in `--warn`,
keeps the reader's words in the editor, and fills the Export button. The four ways the reference
site loses text are closed and each closure is a rule: the debounce carries a 2s ceiling as well as
a 400ms pause; `visibilitychange`, `pagehide` and `blur` all commit; the shell's `onClose` commits
before the panel goes; and storage is never read over text the reader can still see. A note is
keyed `coursehub.note:` plus a tier and the course key and file name, which are the two identifiers
this repository has committed never to change - never a title. Tab is bound to nothing in the
editor, because indenting with it is a keyboard trap and fails SC 2.1.2. It opens from the topbar
and from the cluster, which is one `attachOpener` call each. The author-facing
statement is `.claude/skills/course-authoring/references/widgets.md`, "The study notes panel". Do
not restate it here.

**A band across the foot of every lesson carries the previous page, where you are and the next
page, and its order comes from the generated outline.** The end-of-page pager is at the end of the
page, so a reader who decides to move on pays a scroll before they can; the pager stays, because it
prints and it is what a page with no script has. `hub.js` builds the bar from
`window.COURSE_OUTLINE` and never from a page's own pager markup - the outline is generated from the
course map and gated by checks 3 and 7, a pager is hand-written per page, and only the outline is a
sequence rather than a claim about two neighbours. A page the outline does not name gets no bar.
**Everything fixed across the foot is summed once, in `--foot-h` on `body`**: the pre-production
strip, this bar and the device inset. The body's padding, the rail's scroll foot, the cluster's
offset and both panels' heights read that one token, so a third occupant is one term and no edit
anywhere else, and the panel shell's `bounds()` measures the two bars rather than assuming either.
`--chapbar-h` is the bar's height and the reserve reads the same token, so the two cannot disagree.
The author-facing statement is `.claude/skills/course-authoring/references/widgets.md`, "The fixed
chapter bar". Do not restate it here.

**The in-page section rail is chrome derived from the page itself, and that is the rule that
matters.** `hub.js` reads the page's own headings at runtime - an `h2` that is a direct child of the
content region and is not wearing `.h-label` or `.h-sub`, which is the rule `.numbered` already
applies - and builds a strip of ticks in the right-hand margin. No page's markup mentions it, no
lesson edit is ever needed, and there is no second model of a page's sections that could disagree
with the page. Four things are decided and none may be re-decided casually: the rail appears at four
sections and not fewer; a generated id is `sec-` plus the heading's slug, taking the next free `-2`,
`-3` only when the document already answers to the candidate; the reader is in the last section
whose heading has reached `--secrail-line`, which is also every direct-child `h2`'s
`scroll-margin-top` and is read back in pixels by `hub.js` rather than restated; and the
`IntersectionObserver` watches thresholds 0 **and** 1, because 0 alone lags by the height of a
heading and a one-pixel band is stepped over by a fast scroll. It runs at 1281px and up - below that
the gutter is `--pad: 2rem` and the strip would stand on the breakout band, and below 1041px the
course rail is already a drawer over the same prose - and it is not printed. The author-facing
statement is `.claude/skills/course-authoring/references/widgets.md`, "The in-page section rail". Do
not restate it here.

## The course contract

A course declares its identity through **seven tokens, in one block keyed on `data-course`, and
through nothing else**. `--course-hue` is required; `--font-display`, `--font-mono`,
`--eyebrow-family`, `--eyebrow-tracking`, `--eyebrow-case` and `--eyebrow-size` are optional.
Adding a course adds no framework code, and every control the framework offers works on the new
course automatically. The block and its reasoning are in `assets/hub.css` under "the course
contract"; the author-facing statement, including what an author may rely on, is
`.claude/skills/course-authoring/references/widgets.md`, "The course contract"; the registration
procedure with a worked example is that skill's `new-course.md`. Do not restate any of it here.

Four things are forbidden, and each is checked rather than asked for.

- **A course ships no CSS of its own.** The three `course-extras.css` sheets are grandfathered
  and no course gets a fourth: a widget a second course could want has one owner and it is
  `hub.css`.
- **A course declares nothing but the seven tokens**, and nothing outside their stated ranges. A
  hue is unitless, because inside a relative colour `h` is a number and `calc(h + 25deg)` is a
  type error that drops the whole declaration in silence.
- **A design block never writes a course token.** The six tokens both axes want carry two names:
  a design writes `--x-default`, a course writes `--x`, every rule reads `--x`, and the
  resolution line at bare `:root` is (0,1,0) so a course block at (0,2,0) wins it whatever the
  source order. Two writers on one name is a contest the cascade settles silently, which is how a
  course sheet's 24px lost to a design rule's 48px with nothing to warn.
- **Uppercase is for a label of about five words or fewer**, because capitals read 9.53% to
  19.01% slower than lowercase. There is no all-caps option for body text or for a heading that
  runs to a full line, and there must never be one.

`check_course_contract()` in `scripts/validate_site.py` checks the registration; assertion A3 in
`scripts/style_snapshot.py` proves in a browser that each token reaches the rules that read it and
reaches nothing else.

## Editing the shared assets

There is now **one** design system and one copy of it: `assets/hub.css` plus `assets/hub.js`,
linked by every page in the hub. The old `assets/course.css` / `course.js` pair and its six
byte-identical copies are gone. A course owns the seven tokens of the course contract, not the
design system: the three `assets/course-extras.css` files that remain, in `llm-evolution-course`,
`llm-inference-course` and `statistical-foundations-ml-course`, are layered *after* the hub sheet
and carry only rules
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
may read a `--*-user` property, and no reader control may write anything else. What sits after the
comma is the stylesheet's own answer and is not always a `-default`: a derived axis falls back to
its derivation, as `--lh-body` and `--measure` do. What is fixed is the head - a reader value is
read by one custom property, once, and by exactly one declaration in the sheet. The reason is
measured: the two reading preferences were applied as inline styles until 2026-08, an inline style
beats every rule that is not `!important`, and a reader who had widened the column was pinned there
for good. It also means a value with a viewport override belongs in a `-default` inside the media
query, not in a second rule on the element - `body { font-size: ... }` at a breakpoint would sit
after the body rule and out-argue the reader. The block at the head of `hub.css` states the rule in
full. Twenty-four tokens carry the form today and they are exactly the reader-reachable ones:
`--measure-chars`, `--measure`, `--fs-body`, `--lh-body` and the twenty prose-rhythm space roles.
**A resolution line never sits inside a design block.** A design block is `(0,2,0)`, so a line
written in one would be a second resolution line for the same reader value and source order between
two interchangeable designs would decide which answered. The twenty rhythm roles therefore resolve
at a bare `:root` just after the design blocks, in the shape of the course layer; the design writes
only the `-default`, and `var()` still picks it up because substitution reads the computed value of
that property rather than the declaration beside it.
Six further tokens carry a two-name form for the same reason on a different axis, and that is the
course contract above.
Everything else is a one-layer design token, because a `--*-user` layer on a value no control can
write is dead weight that still has to be kept right in every media query.
**Two reader choices are not `--*-user` properties.** They are registered axis attributes, because
what they carry does not compose into a single value: `data-body-face` selects a family together
with the three measured constants that have to travel with it, and `data-motion` selects a block of
rules. `AXIS_ATTRIBUTES` in `scripts/validate_site.py` is the registry, and `hub.js` may write no
attribute on `<html>` that is not in it.

**Type, rhythm and shape are tokens too, and a rule reads one rather than a literal.** One block
near the head of `hub.css`, marked "the design axis", carries 346 of them: `--font-display`,
`--font-ui` and `--font-mono` by role, the type scale, the leading set, weight, tracking, an
eight-step space ramp with a role layer over it, the reading frame, shape, motion and the eyebrow
treatment. Six of
them are declared there as a `-default` and resolved below the block, which is the course layer;
see "The course contract" above. A hard-coded
`1.05rem` in a rule is a value a second design cannot reach, which is the fork this hub already
paid once to remove. **A rule never reads a `--sp-1` to `--sp-8` ramp step**: those are the defaults the role
tokens are built from, and a ramp step in a rule puts a reading-rhythm distance and a chrome
distance on one token, which is what the split exists to prevent. Six role tokens are the reading
column's rhythm and a later density control may scale those and nothing else; the chrome is
permanently out of its reach, because seven pointer targets there pass SC 2.5.8 only on the spacing
exception. `references/widgets.md`, "The design tokens", is the author-facing summary.

**The design axis is the third reader axis, and two designs are registered.** `data-design` selects
a block of the token set above, and the default block is written once under two
selectors, `:root, :root[data-design="house"]`, exactly as the Paper palette is: the bare arm is
what a page with no script gets, the attribute arm is what the axis selects. `press` is the second,
the form half of the reference look, whose colour half is the `press` palette; either can be worn
without the other. **A design carries no
colour** - that is the palette and mode axes - so a design costs no row in the contrast matrix. What
a design also may not reach is the body size, which is resolved outside every design block so the
720px arm can move it, and the reading face, whose registry sits after the design blocks because a
face is a name plus three measured constants a design cannot supply. The
registry lives in `hub.js` as `DESIGNS`, an unknown stored key falls back to the first entry, and
withdrawing a design is deleting its entry: no deploy and no page edit. Three checks in
`validate_site.py` hold the halves together - registry and blocks name the same set, every design
declares the whole token set, and a design-axis token is declared in a design block and nowhere else
(a design block is `(0,2,0)` and would out-argue a media-query override in every viewport). A course
sheet that restates a design token must therefore write `:root[data-course="..."]`; a bare
`[data-course="..."]` is `(0,1,0)` and loses. That spelling is necessary and not sufficient: a
course block and a design block are both `(0,2,0)`, so for the six tokens both of them want, the
design writes a `-default` and the course writes the token, and the six resolution lines sit below
the design block rather than in it. See "The course contract" above.
`references/widgets.md`, "The design axis", is the author-facing summary.

**A palette states 18 raw values twice, and two of them are not colours.** Seven palettes are
registered. Sixteen of the eighteen are the `--l-*` / `--d-*` colour pairs the mode layer maps onto
the semantic tokens. `--*-wash` is the ground treatment, a `background-image` painted on the canvas:
`none` on six palettes and two 5% radial gradients on `press`, because a ground that is a flat fill
reads as a screen colour and one with a wash reads as paper. `--*-pane` is what the reading column
paints behind the prose: six palettes state their own `--surface`, and `press` states `transparent`
so the prose sits on the washed paper with cards and callouts as lighter veils over it. Both are
stated by every palette rather than only by the one that uses them, for the same reason the sixteen
are. Two of the sixteen are new with `press`: `--*-code-inline-bg` and `--*-code-inline-ink`, so a
design with a dark code plate does not drag inline code dark with it. Both pairs carry body text and
`scripts/contrast.py` holds both to 7:1.

**`main.wrap` must not gain a background that changes on a palette switch.** It is the scroller's
big child, and repainting it on a switch exposes a Chromium behaviour the computed-style harness
reads straight through: after a switch, an element inside a closed `<details>` keeps the computed
style it had while every ancestor updates correctly. It is measured, not inferred - the harness
printed the ancestor chain with the child a palette behind its parent - and it cannot be waited out,
because the stale value is perfectly stable; polling it is worse, because each read re-caches it.
That is why the reading pane is a palette value and why `press` paints none. Anything that gives
that element a switch-varying background again owes assertion A2 a re-run.

**A palette and a design are data, and nothing branches on either name.** No function in `hub.js`
and no rule in `hub.css` knows one by name: the two registries are plain arrays, the blocks are
keyed on the attribute, and the appearance panel builds its three grids by iterating. Registering
either must stay a block of values plus one array entry, and withdrawing either must stay one
deleted line. Never write `if (design === 'house')`, never key a rule on a palette name outside its
own value block, and never state a count of them in prose that a seventh or an eighth would falsify.
The captain's stated direction is that designs, palettes, fonts and course templates come from a
database rather than from these files; that is not work to do now, and it is a door not to close.

**Four of the reading axes are derived, and the block after the design axis is where.** They are
not independent, so offering them as four settings would let a reader move one control and silently
move a second. The measure names real characters and its width is computed, because `ch` is the
advance of the digit zero and one `ch` of Source Serif 4 is .5049em against a .4479em character;
the body size names apparent size on the Source Serif 4 scale, because the same nominal size is 21%
larger to the eye in Inter; the code size follows the reading face's x-height, because x-height
parity against JetBrains Mono is .822em under a serif and .993em under a sans; and the leading gets
a nudge above 80 characters that any explicit reader choice suppresses. All four are pure CSS, so a
page with the script blocked computes exactly what a page with it computes.

**A face is a name plus three measured constants** - average prose advance, x-height per em and
apparent-size factor - and the four are declared together in one `data-body-face` entry. Adding a
face means adding an entry, never setting `--font-body` on its own, and never picking a constant
out of a report: `scripts/type_invariants.py` refuses an entry that names a family without all
three, measures the advance from a committed corpus of real hub prose, and holds invariants M1 (a
`--measure-chars` of N realises N plus or minus one characters at 55, 68, 80 and 85) and M2 (the
code size stays inside .85 to .90 of the prose under a serif). It also re-runs the reflow matrix
and proves the whole layer with `hub.js` blocked. It is the third CI check and it takes about four
seconds. The three figures published for Source Serif 4's advance disagree, and M1 is what settles
that: `.4065` fails it by five to eight characters.

**The three faces are self-hosted, and what a page fetches is now a budget rather than a
guess.** Eight woff2 sit beside `hub.css`, 459.3K on disk, gated by `unicode-range` so an
English page fetches at most four of them: 152.8K with no italic, 241.0K once `<em>` appears in
the prose, which is 559 of the 796 pages. Each file was cut to the part of its `wght` axis a
rule can actually select, which is lossless - advance widths are bit-identical in Chrome at
every weight the hub uses - and `assets/fonts/README.md` carries the one command and the reason
only the lower bound of the axis may move. `validate_site.py` holds a total ceiling and a
latin-cut ceiling, refuses a face with no `font-display`, and refuses `font-display: optional`:
a face that misses the first-paint deadline is dropped for the life of that page load, and
`document.fonts.load()` does not bring it back, so the `data-body-face` axis would do nothing at
all until the next navigation. Both registry faces are on every page
already, so switching between them costs no fetch; **a third face is loaded in script**, through
the CSS Font Loading API, with `data-body-face` set only once the load settles - a `FontFace`
built that way carries its own `display` and is never subject to the descriptor above.
`references/widgets.md`, "The faces, and what a page pays for them", is the author-facing
summary.

**The framework is rendered at `design-system/index.html`, by itself.** Every token with the value
the browser resolved and a specimen painted by that token, every widget beside its markup, the
reader controls working, and the accessibility floor. Read it before you guess at what a token
does. It is a hub section rather than a course: it has no `lessons/`, so `check_pages.py` asks it
for no rail and no `MISSION.md`, and `course_directories()` in the two other scripts still counts
it, which is why it is linked from the hub `index.html` and named in `scripts/style-sample.txt`.
Two attributes name a token anywhere on the hub - `data-token` for a live-value cell, `data-spec`
for a specimen - and `validate_site.py` fails a name that `hub.css` does not declare, in a page or
in a stylesheet. **Adding a token means adding a row on that page** in the same pull request; the
page itself counts what it is missing and says so out loud. `references/widgets.md`, "The design
system reference page", is the author-facing summary.

Every page also loads its course `outline.js`, generated by `scripts/gen_outline.py`, which is
what the sidebar reads. `llm-evolution-course` ships `routes.js` instead; see
`llm-evolution-course/routes/README.md`.
**The generator slices a course map at each `.module-h` and runs the last slice to the end of the
file**, so any `href="lessons/..."` below the final module - in a footer, most easily - is collected
as an extra lesson of that module and shows up in the rail as a phantom entry under the wrong
heading. It renders, every link resolves, and `validate_site.py` stays green. Link a lesson from the
hero or from a card, never from below the last module.

`hub.js` writes up to seven attributes on `<html>` in its head phase, before the first paint:
`data-mode`, `data-palette`, `data-design`, `data-body-face` and `data-motion` are the reader's
choices, `data-course` is the course
folder, read straight out of the URL, and `data-env` is `preprod` when the hostname carries that word and
absent otherwise, which is what paints the pre-production bar. The two reading axes are written only
when the reader has chosen something other than the registered default, so a page with no stored
preference carries exactly the attributes it carried before those axes existed. Every `[data-env="preprod"]` rule in
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
extending outwards. Choose which gap by whose pages your reader actually holds open beside yours,
then prove the candidate with the
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
matters, for every class in the closed widget vocabulary, across seven palettes and both modes. The
snapshot is committed under `scripts/style-baseline/`, so the answer to "did that refactor move
anything" is a diff rather than a judgement, and the harness names the page, the element shape and
the property when something did move. It also checks the two render states a single capture cannot
see: a page with no `data-mode` under the operating system's preference must compute what the
explicit choice computes, and a page switched after load must compute what the same page computes
when loaded on that setting directly. Read the script's docstring before changing it - the sample,
the property list and the two assertions each carry the reason they are shaped that way.

**Every snapshot file is per page, and coverage is asserted rather than recorded.** The gate is only
as wide as the sample, so the run proves the sample renders every class in the closed vocabulary and
fails by name when it does not; `--coverage` prints the table behind that verdict, and the CI step
passes it so the table is in the job log. There is deliberately no committed count of it. A shared
generated file in this repository is not a record, it is a lock: `COVERAGE.txt` recomputed itself on
every run, so it held nothing the run did not already know, and requiring byte-equality on it
serialised eighteen per-course pull requests that touched nothing in common - each merge left the
other seventeen holding a stale count, red on that one line and nothing else. Never re-introduce a
shared generated file the whole hub has to rewrite; assert the property instead, and key anything
that must be stored per course, the way the page snapshots already are.

**The accessibility floor is measured, not asserted, and it is a gate.** A ground of a given
lightness bounds the best contrast any ink can reach on it, which is arithmetic rather than taste:
no ground between L\* 43.8 and 54.1 reaches AA with either of the hub's inks, and the two cross
over at L\* 48.9. The framework *prevents* that band rather than warning about it - the ground is a
discrete registered choice, a palette and a mode, so no reader input can land inside it - and three
checks keep the registered set outside. `scripts/contrast.py` runs inside `validate_site.py` and
needs no browser: every registered `--bg` is inside its band (light L\* 88 to 99, dark 3 to 16),
every `--ink` clears 7:1 and sits on the correct side of the crossover, and every other colour a
palette states clears the floor its role carries. `scripts/contrast_matrix.py` runs in the style
job and measures what only a browser can resolve - the nine `color-mix()` tints and the per-course
accent - over every registered palette, two modes and every registered course hue, because an OKLCH rotation
holds OKLCH lightness constant and WCAG luminance is not OKLCH lightness. **Both carry a list of
recorded breaches and neither list may grow**: a new breach fails, a recorded one that gets worse
fails, and a recorded one that is fixed fails until its line is deleted. `--report` and the plain
run print every number, which is what to read while choosing a colour. **If a check fails, the
answer is the palette, never the band.**

**One focus ring, five tokens, every element that can take focus.** `--focus-ring-color` is
`--accent-2` so the ring is never the link colour and never the fill of the control it surrounds;
`--focus-ring-offset` is 2px and `--focus-ring-offset-box` the 3px a scroll container takes, and
neither may be 0 because a ring on the border box of a scroll container is clipped by it. Always
`:focus-visible`, never `:focus`. `scripts/focus_walk.py` presses real Tab keys through three
pages, the appearance panel and a 700px viewport, in both modes, and fails on a stop that has no
ring, wears the browser's own, or sits flat on the border box. Two traps live in that script's
comments and both cost an afternoon: a computed style read straight after the key is half-applied
and looks exactly like the browser's ring, and `blur()` does not move the sequential focus
navigation starting point, so a walk after a click silently covers two thirds of the page.

Thirteen traps in that design system, all found on the published site:

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
- **A width media query is answered by the printed page box, so every one of them says `screen`.**
  A4 inside the browser's own margins is about 717px and US Letter about 739px, which straddles the
  hub's own 720px breakpoint: unqualified, the same lesson laid out as a phone on one paper and as a
  laptop on the other, and the 1040px drawer arm applied to both. That arm paints
  `body[data-rail="on"]::after`, a `position: fixed` pseudo-element carrying a literal
  `rgb(0 0 0 / .35)` that no token override can reach and that the browser repeats on every printed
  page - so every lesson printed with a 35% black rectangle over all of it, on every sheet, in a hub
  whose readers print. Nothing on screen was wrong, which is why it survived. `validate_site.py`
  check 15 now fails an unqualified width query, in `hub.css` and in every course sheet, and the
  PAPER block at the end of `hub.css` states paper's own values. **Paper is the third render state**:
  a rule that fixes one of screen, paper and the switched state can break another, and neither CI
  check renders a page, so prove a print change with a PDF at A4 *and* at US Letter and look at it.

- **`* { min-width: 0 }` at the head of the sheet takes the flex automatic minimum off every
  element, and a `white-space: nowrap` flex item then spills instead of shrinking.** The reset
  earns its place - it is what stops a long code line widening a grid or flex child - but the cost
  is that a `.spine` link is laid out narrower than its own text and the text runs out of the box,
  across the gap and over the next link. Nothing in the repository could see it: no box overlaps
  another, the row reports no overflow, `scrollWidth` equals `clientWidth`, and the computed-style
  harness records no geometry that moves. At 320px it was on 594 of the 796 pages, and on the
  fullest topbar in the hub it lasted up to 864px. Measure a nowrap row on its **rendered text** -
  a `Range` over each item's contents, intersected with the item's own box when the item clips -
  and never on `getBoundingClientRect` alone, which calls the worst of it correct.

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
