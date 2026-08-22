# Page contracts

Four page types ship from this repository.
A course picks one content shape in its `MISSION.md` and stays in it.
Mixing shapes inside a course is why a reader cannot tell whether the next page is ten minutes or forty.

Every one of them opens with the big picture: a content page with its orientation figure, a map page with the map itself.
The counts behind that are in [`pedagogy.md`](pedagogy.md).

## The hub landing page

`index.html` at the repository root. One card per course, grouped by subject.

Owes: a `.hero`, a `section.module` per subject with its `.module-h` count kept accurate, and a `.lcard` per course carrying the course's page count, a one-paragraph pitch, and two pills.

The count in `.mcount` and the count in each card's `.ln` are facts about the repository.
A card claiming "38 lessons" beside a folder holding 39 is the cheapest kind of wrong and the easiest to avoid: count the files.

## The course map

`<course>/index.html`. Uses `main.wide wrap`.

Owes:

- A `.hero` whose `<h1>` is a claim rather than the course name repeated, and whose `.sub` says who the course is for and where to start.
- One `section.module` per module, in teaching order, each with an accurate `.mcount`.
- One `.lcard` per page, carrying a rung pill and a reading-time pill.
- A `.roadmap` list for anything planned and unwritten, in **plain text, never a link**.
- A card for each `reference/` sheet.
- A footer linking the glossary, any sibling course, and `../index.html`.

**A lesson's title lives in four places and they must agree**: the page's own `<h1>`, its `.lt` card in the course map, the rail entry `gen_outline.py` generates from that card, and the `.ttl` of every pager that points at it. Rewriting an `<h1>` without the other three leaves a reader clicking one title and landing on another, and every link still resolves so nothing else catches it. `scripts/check_titles.py` checks all four and runs in CI. A **pager** label may be a faithful abbreviation, because the control is narrow and the hub shortens widely; the test is that the `h1` begins with the label once both are reduced to lower-case alphanumerics. A card and a rail entry get no latitude, because they have the room and the rail is generated from the card.

**Every `section.module` closes before the next one opens.** This is the one structural break in a course map that has no symptom: the browser repairs the tree, every card still renders and is clickable, every link resolves, and `gen_outline.py` is unaffected because it splits the page at each `.module-h` rather than at each section. It reached `main` twice. Both times a card list ended with `</a>` and the next module's `.module-h` followed immediately, with the `</div></section>` pair missing between them, and the result was a module with no section of its own: its heading and all its cards became children of the module above it, so a screen reader navigating by region found one fewer region than the page appears to have. `scripts/validate_site.py` now matches the tags on a stack and fails the pull request on it.

This file is the course's single source of truth for its own map, and it is a **generator input**.
`scripts/gen_outline.py` parses it into `<course>/outline.js`, which every page in the course loads and the sidebar rail renders from, so the shapes in [`widgets.md`](widgets.md) are a parsing contract and not only a styling one.
Re-run the generator after every change here and commit the result; `validate_site.py` fails the pull request when the outline and the lessons on disk disagree.

A course that is read along several named orders ships a hand-written `routes.js` and a route-aware `outline.js` instead, and the generator refuses to run against it.
`llm-evolution-course` is the only one; `llm-evolution-course/routes/README.md` is the reference.

Do not restate the map in `BUILDER-SPEC.md`: the seven pre-existing courses did, and every one of those copies is now out of date.

## A content page

`<course>/lessons/NNNN-kebab-case.html`. Uses `main.wrap`.

One tight idea, 1,800 prose words at the most.
Whether it is called a lesson, a chapter, or a part is the course's own word for the same contract.

Owes, in this order:

1. `.eyebrow`: module, module name, and position.
2. `<h1>`: the one idea, phrased as a claim with a verb in it rather than a topic.
3. `.paper-meta`: rung pill, reading-time pill, and the attribution or framing line.
4. `.card.tldr`: the one-minute version.
5. **The orientation figure**: where this idea sits in the whole, before any body section.
6. The mental model, before any formula.
7. The mechanism, every symbol named in words.
8. The trade-off, named in the same section as the technique that incurs it.
9. Quizzes, after the idea is fully worked.
9b. **Practice problems**, under their own `<h2>Practice</h2>`, after the quizzes.
10. `.teacher-note`.
11. `Primary source to go deeper`.
12. `.pager`.
13. `<footer>`.

Item 9b comes after item 9 because the two ask different things of the reader.
A quiz is a conceptual check answered in the head, so it can close a reading session.
A practice problem needs paper and several minutes, so a reader can leave after the quizzes and come back for it.
That order also keeps the reading-time pill honest: the pill estimates reading, and practice is not reading, so the estimate for it goes in the heading (`<h2>Practice <span class="note-sm">about 15 minutes, with paper</span></h2>`) and never into the pill.
The markup is in [`widgets.md`](widgets.md).

Item 5 is the one that decides whether the page reads as a wall.
The reader gets the big picture before the detail, and every paragraph after it that the figure already says is a paragraph to cut.

The counts that make this a course page rather than a blog post are in [`pedagogy.md`](pedagogy.md).

### Two variants of a content page

A **chapter** indexes many topics rather than developing one, so a reader can use it during a review.
Every topic is its own `<h3 id="kebab-case">`, the id is what the glossary links to, and **an id is a public URL**: the validator strips fragments before checking a link, so a renamed anchor breaks the glossary silently.
A chapter still owes everything above, the word ceiling included.
Its diagram floor rises with its topic count, roughly one diagram per two topics, and its orientation figure is the map of the topics it indexes.
A chapter that cannot hold its topics under the ceiling is several chapters, and the fix is to split it rather than to cut it.

A **lab page** carries at least one `.lab` with a real goal, real commands, and a measurable outcome, and closes with a `ul.checklist` rather than only a quiz.
Prefer invocations that actually run. Note where a flag is version-sensitive.
The lab classes are styled today only in `llm-inference-course/assets/course-extras.css`; a second course that wants them promotes the rules into `assets/hub.css` rather than forking the file. See [`widgets.md`](widgets.md).

## A lecture hub page

Only for courses that nest a level deeper, where one source lecture is too much for one sitting.

A map, not a lesson: it states what the lecture delivers, carries the logistics, and links its parts in order.
It is numbered in the same continuous `lessons/` sequence as the parts, so a lecture of eight parts occupies nine numbers.
It carries diagrams but no quizzes: retrieval practice belongs on the page that taught the thing.

The course `index.html` groups the lecture as one `section.module` with the hub card first and a `<ul class="parts">` beneath it.

## Numbering, and what a URL costs

`NNNN-kebab-case.html`, zero-padded, continuing the sequence.

**Nothing already published is renumbered or renamed.**
New numbers go at the end even when the teaching order would prefer the middle; module grouping in `index.html` is what carries teaching order, and it is free to disagree with file order.

The same rule reaches one level deeper than most authors expect: an `<h3 id="...">` inside a chapter is linked from the glossary and from sibling chapters, so changing one is a rename.
Add anchors freely. Change them never.
