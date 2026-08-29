# Contributing to Course Hub

Thanks for helping improve these courses.
This document is the complete contract for both humans and coding agents.
If you are an agent, also read [`AGENTS.md`](AGENTS.md), which adds the rules specific to automated contributors.

## The one rule that matters

`main` is protected.
Nobody pushes to it, including the repository owner.
Every change - a typo fix, a new lesson, a whole new course - lands through a pull request that a reviewer approves and that passes its checks.

## Two stages, two branches

The hub publishes from one repository to two S3 buckets.

| Branch | Stage | What it is |
|---|---|---|
| `main` | pre-production | the review site, closed to search engines, a red bar along the foot of every page |
| `prod` | production | the live hub readers see |

Merging into `main` triggers the publish workflow, which syncs the site to the pre-production bucket.
So a merged pull request is a deployment to the review site, not to the live one. Treat it that way.

Production moves only when the repository owner promotes it.
He opens a pull request from `main` into `prod` and merges it in the GitHub UI; two branches in the same repository have no sync button, so the promotion pull request is the mechanism.
That merge is a push to `prod`, and the push is what publishes the live hub.
Nobody else pushes `prod`, and no coding agent goes near it.

## Workflow

1. **Fork or branch.**
   External contributors fork the repository.
   Contributors with write access branch directly.

2. **Name the branch for the work.**
   Use `<type>/<short-kebab-description>`, for example `lesson/mixture-of-depths`, `fix/broken-glossary-link`, `course/rust-async`.
   Types in use: `lesson`, `course`, `fix`, `docs`, `chore`.

3. **Make the change.** Follow the authoring rules below.

4. **Validate locally before you push.**

   ```bash
   python3 scripts/validate_site.py       # structure, links, and the design-system head contract
   python3 scripts/check_pages_gate.py    # the house standard, against its recorded baseline
   ```

   Both must pass. The same two run on your pull request and gate the merge.

   If you changed `assets/hub.css`, `assets/hub.js` or a course's
   `course-extras.css`, run the computed-style harness as well. It needs Chrome
   and takes a few minutes:

   ```bash
   python3 scripts/style_snapshot.py
   ```

   It loads a fixed sample of pages in every palette and both modes and compares
   every component's computed style against the committed snapshot. Nothing
   moved is the answer you want. If something moved on purpose, re-record with
   `--write`, commit the snapshot, and say in the pull request what moved and
   why.

5. **Preview in a browser.**
   There is no build step. Open the file directly:

   ```bash
   open index.html                                   # the hub landing page
   open llm-papers-course/lessons/0001-attention-is-all-you-need.html
   ```

   Click through every link you touched and answer every quiz you added.

6. **Commit in whole, self-describing units.**
   Use [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.
   One lesson per commit is a good default.
   Never add an agent or tool as a commit co-author.

7. **Open a pull request into `main`.**
   Fill in the pull request template.
   Say what changed, why, and what you checked in the browser.

8. **Get it reviewed and merged.**
   Once the checks are green and a reviewer approves, the merge publishes the pre-production site within a couple of minutes.

9. **Check it on pre-production.**
   Open the review site and look at what you changed on a real host rather than from disk.
   Every page there carries a red pre-production bar; a page without one is the live site and you are in the wrong place.
   The live hub gets your change when the repository owner promotes `main` into `prod`.

## Repository layout

```
index.html               the hub landing page; every course is a card here
assets/                  the hub design system: hub.css, hub.js, fonts/. Every page links these.
scripts/validate_site.py the structure and link checker that gates every pull request
scripts/check_pages_gate.py  runs the house-standard page checker against its recorded baseline
scripts/style_snapshot.py    the computed-style harness; proves a stylesheet change moved nothing
scripts/style-sample.txt     the fixed sample of pages the harness loads
scripts/style-baseline/      the committed snapshot the harness compares against
scripts/gen_outline.py   generates a course outline.js from its index.html
.github/workflows/       validate on pull request, publish on push: main to pre-production, prod to production

<course-name>/
  index.html             the course map; every lesson is linked from here
  assets/                optional course-extras.css only, for rules unique to this course
  outline.js             generated from index.html by scripts/gen_outline.py; the sidebar reads it
  lessons/NNNN-kebab.html    the lessons, zero-padded and in teaching order
  reference/*.html       print-friendly cheat sheets and glossaries
  learning-records/*.md  progress notes; never published to the site
  MISSION.md             why the course exists and what is out of scope
  NOTES.md               teaching style and working notes
  RESOURCES.md           the high-trust sources the lessons cite
  BUILDER-SPEC.md        the authoring spec for that course
```

## How a course gets built here

This section is orientation only.
Every rule it mentions is written somewhere else, and that other file is the authoritative one.

### Which file governs what

| What you need to know | Read |
|---|---|
| The workflow: branch, validate, pull request, review | This file |
| What a page must contain to be one of these courses | [`.claude/skills/course-authoring/SKILL.md`](.claude/skills/course-authoring/SKILL.md) and the `references/` beside it |
| How the shared design system behaves, and the traps in it | The "Editing the shared assets" section of [`AGENTS.md`](AGENTS.md) |
| This course's voice, scope, cadence, and trusted sources | That course's `MISSION.md`, `NOTES.md`, `RESOURCES.md`, and `BUILDER-SPEC.md` |
| Where a session sits in that course's reading order | That course's `PLOT.md` |
| The one course that presents its lessons along several routes | [`llm-evolution-course/routes/README.md`](llm-evolution-course/routes/README.md) |

The course-authoring skill lives under `.claude/` because Claude Code loads it from there on its own.
That path is the only thing about it that is agent-specific.
It is the house standard for every published page, whoever or whatever writes that page.

### Three constraints, and the cost behind each one

The rules below look arbitrary until you know what they were paid for.

**A course owns a hue, not a stylesheet.**
The hub used to carry six byte-identical copies of an earlier design system, one per course.
They drifted, one copy received a rendering fix that the other five never got, and because a broken diagram here reaches no console, the pages that rendered wrong stayed that way until somebody looked at a figure.
De-forking them ran from pull request #14 to #32, and it is why there is now one `assets/hub.css` and one `assets/hub.js`.
So a new course adds a hue offset to the course-accent block of `assets/hub.css` and nothing else.
A shape the design system does not have is added to the design system and documented in [`references/widgets.md`](.claude/skills/course-authoring/references/widgets.md), in the same pull request that uses it.
Never by forking the sheet, and never by an inline style.

**A lesson may not assume what the reader read before it.**
`llm-evolution-course` writes each lesson once and presents that one pool of pages along four named routes, so two readers can reach the same lesson from different neighbours.
That is what makes "as we saw in the previous lesson" wrong there: name the lesson and link it instead.
`llm-evolution-course/BUILDER-SPEC.md` states the rule and gives a grep that finds every phrasing of it.
The habit is worth keeping in single-route courses too, because a reader who arrives from a search engine has no previous lesson either.

**Verification here is looking, not counting.**
The defects that matter most are silent: the page validates, the browser reports nothing, and the figure is an error box or a run-together label.
Two of those defect classes are inverses of each other, one wrong on the first paint and one wrong only after a repaint, which is why a page has to be checked in both render states rather than one.
The skill lists the five of them, and `AGENTS.md` carries the mechanism behind each.

## Authoring rules

These keep the courses consistent, so read the course's own `MISSION.md`, `NOTES.md`, and `BUILDER-SPEC.md` before you write a lesson.

- **One tight idea per lesson.** Lead with the mental model, then the detail.
- **Active recall over passive reading.** Every lesson carries quiz or flashcard widgets. Retrieval builds storage strength; re-reading does not.
- **Quiz options must match in length.** If the correct answer is visibly longer than the distractors, the formatting gives it away.
- **Number lessons `NNNN-kebab-case.html`,** continuing the existing sequence in that course. Do not renumber existing lessons; their URLs are public.
- **Register the lesson.** Add it to the course `index.html`. The validator fails the pull request if you forget.
- **Link the hub design system.** From a lesson, link `../../assets/hub.css`, then `../../assets/hub.js` and `../outline.js` in the head. Do not inline a private copy, and do not add a second stylesheet unless the rule is genuinely unique to this course, in which case put it in `<course>/assets/course-extras.css`. A course owns only its palette, not the design system.
- **Regenerate the outline.** After adding or renaming a lesson, run `python3 scripts/gen_outline.py <course-name>` and commit the result. The validator fails the pull request if the outline and the lessons on disk disagree.
- **Use relative links only.** Courses are siblings under one bucket root, so cross-course links look like `../../llm-papers-course/index.html`. Absolute paths break the site.
- **Cite primary sources.** Link the paper, the RFC, or the vendor documentation - not a blog post summarising it. Add anything new to the course `RESOURCES.md`.
- **Write full prose.** Lessons are teaching material: complete sentences, no shorthand.

## Adding a whole new course

1. Create `<course-name>/` with its own `index.html` and `lessons/`. It needs no `assets/` folder unless it has rules of its own; it links the hub design system like every other course. Give it a hue in the course-accent block of `assets/hub.css` so it does not wear the same accent as its neighbours.
2. Write its `MISSION.md` first: why it exists, what "done" looks like, and what is out of scope.
3. Give it the five instruction files before any lesson: `AGENTS.md`, `CLAUDE.md` as a symlink to `AGENTS.md`, `MISSION.md`, `PLOT.md`, and `NOTES.md`. `PLOT.md` records the reading order - where every lecture and session sits, and everything planned but unwritten - and a tutorial or lab that follows a lecture sits after it in the course map, never in a separate list at the bottom. `.claude/skills/course-authoring/templates/` carries starters for all five, and writing each from what the course actually is matters more than filling them fast: a short honest file beats a long generic one.
4. Add a card for it in the hub `index.html`.
5. Generate its `outline.js` with `python3 scripts/gen_outline.py <course-name>`.
6. Run the validator. It checks that the hub links your course and that your course links every one of its lessons.
7. Open a pull request. No deploy configuration change is needed - the workflow syncs the whole hub.

The full procedure, including the interview questions that fill these files, is in [`.claude/skills/course-authoring/new-course.md`](.claude/skills/course-authoring/new-course.md).

## What not to commit

- Secrets, access keys, or `.env` files of any kind.
- Anything personal: resumes, private notes, employer-internal material.
- Generated or vendored bundles, unless a lesson genuinely needs offline assets.
- `.DS_Store` and editor state. `.gitignore` already covers the usual suspects.

## Reporting problems

Open an issue. A technical error in a lesson, a broken link, or a confusing explanation are all worth filing, and a pull request that fixes one is even more welcome.

## Licensing your contribution

By contributing you agree that your code is released under the [MIT License](LICENSE) and your course content under [CC BY 4.0](LICENSE-CONTENT), the same terms as the rest of the repository.
