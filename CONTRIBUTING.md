# Contributing to Course Hub

Thanks for helping improve these courses.
This document is the complete contract for both humans and coding agents.
If you are an agent, also read [`AGENTS.md`](AGENTS.md), which adds the rules specific to automated contributors.

## The one rule that matters

`main` is protected.
Nobody pushes to it, including the repository owner.
Every change - a typo fix, a new lesson, a whole new course - lands through a pull request that a reviewer approves and that passes its checks.

Merging into `main` triggers the publish workflow, which syncs the site to its S3 bucket.
So a merged pull request is a live deployment. Treat it that way.

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
   python3 scripts/validate_site.py   # structure and link checks
   ```

   It must pass. The same check runs on your pull request and gates the merge.

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
   Once the checks are green and a reviewer approves, the merge publishes the site within a couple of minutes.

## Repository layout

```
index.html               the hub landing page; every course is a card here
assets/                  the hub design system: hub.css, hub.js, fonts/. Every page links these.
scripts/validate_site.py the structure and link checker that gates every pull request
scripts/gen_outline.py   generates a course outline.js from its index.html
.github/workflows/       validate on pull request, publish on merge to main

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
3. Add a card for it in the hub `index.html`.
4. Generate its `outline.js` with `python3 scripts/gen_outline.py <course-name>`.
5. Run the validator. It checks that the hub links your course and that your course links every one of its lessons.
6. Open a pull request. No deploy configuration change is needed - the workflow syncs the whole hub.

## What not to commit

- Secrets, access keys, or `.env` files of any kind.
- Anything personal: resumes, private notes, employer-internal material.
- Generated or vendored bundles, unless a lesson genuinely needs offline assets.
- `.DS_Store` and editor state. `.gitignore` already covers the usual suspects.

## Reporting problems

Open an issue. A technical error in a lesson, a broken link, or a confusing explanation are all worth filing, and a pull request that fixes one is even more welcome.

## Licensing your contribution

By contributing you agree that your code is released under the [MIT License](LICENSE) and your course content under [CC BY 4.0](LICENSE-CONTENT), the same terms as the rest of the repository.
