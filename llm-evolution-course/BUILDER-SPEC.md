# Builder spec: How Language Models Happened

Read `MISSION.md` first, then this, then two or three neighbouring lessons.
This file is the authoring contract.
Where it disagrees with your instinct, it wins; where it disagrees with the repository's `AGENTS.md` or `CONTRIBUTING.md`, those win.

---

## 1. The rule that makes this course work

**Every lesson must be readable in more than one order.**

Four routes travel the same pool of pages, so a lesson cannot know what the reader read last.
That single fact drives everything below, and it is the difference between this course working and this course being an ordinary linear course with a confusing menu on top.

Three obligations follow, and they are not negotiable.

### 1.1 State the problem before assuming the context

Every lesson opens with a `.callout.key` block titled **Where this lesson starts** that says, in two or three sentences, what problem the lesson addresses and what it assumes.
That block is already in every stub.
Keep it, tighten it, and never delete it.

A reader arriving from any of the four routes must be able to read that block and know whether they are ready.

### 1.2 Never say "as we saw earlier" without naming and linking it

Banned, in every form:

> as we saw in the previous lesson, the fixed vector could not hold a long sentence

Required:

> [Sequence to sequence, and the eight thousand numbers](0019-sequence-to-sequence-and-the-bottleneck.html) ended with a fixed-size vector that could not hold a long sentence

The rule applies to "earlier", "above", "previously", "the last lesson", "we already know", and every other phrasing that assumes a reading order.
There is no exception for a lesson that is adjacent in three of the four routes.

Grep your own draft before you open the pull request:

```bash
grep -nEi 'as we saw|previous lesson|last lesson|earlier we|we already (know|saw)|two lessons ago|the next lesson' lessons/NNNN-your-lesson.html
```

Every hit is either a rewrite or a link. The scaffold's own opening blocks are written to this rule, so copy their shape: name the lesson, link it, and restate the fact in one clause rather than assuming the reader is carrying it.

### 1.3 Introduce every term you use, or link the glossary

A lesson may assume the terms named in its own prerequisites block and nothing else.
Anything else gets one clause of definition on first use, plus an entry in `reference/glossary.html` in the same pull request.

The glossary exists precisely so that this obligation costs one clause rather than a paragraph.

---

## 2. What a lesson is

One tight idea.
Fourteen hundred to two thousand words of full prose, complete sentences, no fragments.
Mental model first, then the mechanism only as far as the story needs it, then what it made possible.

Every lesson, in order:

| Part | Required | Notes |
|---|---|---|
| `.crumbs` breadcrumb | yes | Committed for the route that owns the page. JavaScript rewrites the section name for whichever route is active. Do not hand-edit. |
| `.routebar` | yes | Four real links. Do not edit them by hand; the scaffold generated them and the validator checks the pager that goes with them. |
| `.eyebrow` | yes | Kind, era, lesson number. |
| `h1` | yes | The title. Also the title in `routes.js`. Change both together or the validator fails. |
| `p.lead` | yes | The one tight idea, in one sentence. |
| `.lesson-status` | yes | Zone, as-of date, review date. See section 5. |
| `.callout.key` "Where this lesson starts" | yes | Section 1.1. |
| The lesson body | yes | Numbered `h2` sections. Replaces the stub's sections 2 and 3. |
| Figures | at least two | Section 3. |
| "Where this hands off" | yes | Section 4 of the stub. Keep it. |
| "Sources to read first" | yes | Section 5 of the stub. Keep it. |
| `.quiz` | yes | Three or four questions. Section 4 below. |
| `.pager` | yes | Generated. Do not hand-edit. |
| `footer` | yes | |

The stub's `.stub-note` card and every `.stub-todo` paragraph are removed as you write.
A lesson with no `.stub-todo` left in it is a lesson that claims to be finished.

**No runnable code.
No derivation.
At most one intuition-level formula, in prose.**
When you want more, link `llm-papers-course`.

---

## 3. Figures

This course is diagram-heavy with deliberately low cognitive load.
That is the whole point of it, so the figures are not decoration.

- **At least two figures per lesson**, and the marquee lessons carry three.
- Every figure is a `<figure class="diagram">` holding a `<div class="mermaid">` block and a `<figcaption>`.
  `assets/hub.js` renders it with the palette's own colours and re-renders it when the reader changes palette.
  **It must be a `div`, never a `pre`.**
  `hub.js` appends a copy button to every `<pre>` on the page, and the Mermaid renderer reads the element's `textContent`, so a `<pre class="mermaid">` silently picks up the word `copy` as a final line of graph source and every diagram on the page renders as a syntax error instead.
  This scaffold shipped that bug for about an hour, which is how we know.
- **Every stub already contains working Mermaid that renders today.**
  It is a sketch of the right shape, not a placeholder.
  Replace it with the finished diagram the caption describes; do not delete it and leave nothing.
- The caption's `.fig-brief` span states what the finished diagram must show.
  Once the diagram shows it, rewrite the caption as a teaching caption: what the reader should take from the picture, not what the picture contains.
- **Sequence diagrams and block diagrams must both render.**
  Sweep the page in a real browser before you open the pull request and look at every figure in both light and dark.
- **Check the rendered label text, not just that a figure rendered.**
  Counting SVGs proves nothing, because an error box is itself an SVG, and a lost line break leaves
  a perfectly valid diagram with two words run together. **Change the palette, then look again**:
  the `<br/>` defect above only appears on the repaint, so a figure that is right on first paint can
  be wrong for any reader who touches the appearance controls. The mechanical version of that check
  is to count `.mermaid svg br` plus `.mermaid svg text tspan` before and after a palette click and
  confirm the totals do not fall.

Mermaid rules that keep diagrams from breaking:

- Quote every node label: `A["like this"]`, never `A[like this]`.
- Quote edge labels too: `A -->|"like this"| B`.
- **Write a line break as `&lt;br/&gt;`, never as `<br/>`.** This is the one that has already cost
  this course a full sweep, so it is worth understanding rather than memorising. A literal `<br/>`
  inside a `<div class="mermaid">` is parsed by the browser into a real `BR` element. Mermaid's
  first render copes, but `hub.js` stashes the graph source as `node.textContent` so it can repaint
  on a theme or palette change, and `textContent` drops the `BR` and joins the two halves **with no
  break and no space**. The diagram is therefore correct until the reader touches the appearance
  controls and mangled afterwards - `Hand-written rulesabout 1950 to 1990` - and in a sequence
  diagram the join can merge two statements and turn the figure into a red error box. The entity
  puts the literal characters into the text node, so Mermaid sees the tag on every render.
- **No semicolons inside a label or a note.** Mermaid treats `;` as a statement separator, so it
  breaks the diagram exactly as above. Use a dash.
- Write square brackets as `&#91;` and `&#93;` inside a label.
- Avoid raw ampersands and percent signs in labels.
- Keep one idea per figure. If a figure needs a legend to be understood, it is two figures.
- Keep a figure inside the content column. The merged chapters sit between 854 and 906 pixels wide
  against an 854-pixel column; a long horizontal chain of boxes reaches two or three times that and
  the reader has to scroll a figure sideways to read it. Redraw it `flowchart TB` instead.

---

## 4. Retrieval practice

Three or four questions per lesson, in one `.quiz` block, using the exact markup from a finished lesson in `llm-papers-course`: a `.q` div with `data-answer` holding the zero-based index, four `button.q-opt` options, and a `.q-fb` explanation.

- Test whether the tight idea landed, not whether a date was memorised.
- **Options must match in word and character count.**
  A visibly longer correct answer leaks the answer, and it is the single easiest way to make a quiz worthless.
- The explanation is one sentence and it explains, rather than repeating the correct option.

---

## 5. The living-document rules

The field moves; the course must not need rewriting every six months.
Three zones and one date do that work.

| Zone | Contains | Edit rule |
|---|---|---|
| `settled` | Mechanisms and events whose interpretation is stable. Everything behind the horizon date. | Append-only for corrections. Never rewritten to accommodate a new event. |
| `moving` | Roughly the last eighteen months. | Rewritten freely. Explicitly provisional. Carries a review date. |
| `open` | Named questions with no answer. | A question is retired with its answer and the date. Never silently deleted. |

The settled horizon is **30 June 2025** and it lives in exactly one place, `reference/chronicle.html`.
Moving it forward promotes a batch of moving lessons into settled, and that is a deliberate reviewed act on a schedule rather than a drift.

Rules:

- `data-zone` and `data-asof` are mandatory on every lesson, settled ones included.
  `scripts/validate_site.py` fails the pull request without them.
- `data-review` is mandatory on moving and open lessons, six months out.
- Events go in `reference/chronicle.html`, never straight into a lesson.
  A lesson about a mechanism needs editing when the mechanism changes, not when another model ships.
  Getting that split right is what makes the spine survive.
- Unanswered questions go in `reference/what-to-watch.html`, the second living page.
  The chronicle records what has already happened; the frontier watch records what has not happened yet and what would count as it happening.
  Every entry carries six fields in a fixed order: the question, the meta pills, the claim, why it matters, the source with a read date, and any correction appended underneath.
  The page states its own five append-only rules and the promotion rule, so read the page before you append to it.
- Every numeric claim about a model that does not come from a document the reader can open carries a claim label: `known`, `inferred`, `marketing` or `unverifiable`.
  Anything not `known` carries a link to whatever evidence does exist.
- **Do not name the current frontier model in body prose.**
  Say "the frontier models of 2026" and put the names in a table, the chronicle, or the frontier watch.
  This one habit prevents most of the rot.
- Do not put dates in URLs, and do not version the course.

The promotion ritual, every six months, recorded in the chronicle: sweep the review dates, promote or rewrite each moving lesson, fold chronicle entries that changed a meaning into their lesson, move each frontier-watch entry that has been confirmed across two cycles into the lesson its third pill names, retire answered open questions with their answers, and move the horizon only if it is warranted.

---

## 6. Accuracy

These are teaching materials, so a confident wrong explanation is worse than no lesson.

- The "Sources to read first" list in a stub is a **research pointer left by the scaffold, not a citation**.
  Open every one and confirm it says what the brief claims before it appears in prose.
  If a pointer is wrong, fix it in the same pull request and say so.
- Ground every technical claim in a source you actually read, and link it.
  Add anything new to `RESOURCES.md`.
- Every stub carries a `.callout.warn` block titled **Do not overclaim**.
  Those are the specific traps the scouts found for that lesson.
  Read it before you write and check it again afterwards.
- When a source is contested, state the date, state each side in one sentence, and do not adjudicate.
- Do not invent benchmark numbers, paper results or API behaviour.
- When a lesson summarises a paper, the paper's own claims are the ceiling.

---

## 7. Adding a lesson

1. Take the next free number.
   **Numbers are identity, routes are order.**
   A lesson that belongs chronologically in the middle still gets the next number at the end; the routes put it in the right place.
   Never renumber or rename an existing page.
2. Create `lessons/NNNN-kebab-case.html`.
   Copy the head block and the page frame from a neighbouring lesson exactly.
3. Add it to `routes.js`: one entry in `pages`, and one entry in **every** route whose declared `kinds` include its kind.
   Missing one is a validator failure with the file name in the message.
4. Add a card for it in `index.html`, inside every route map it belongs to.
   The validator fails the pull request otherwise.
5. Fix the static `.pager` on both of its new neighbours in the route that owns it, and its own.
   The validator checks that the committed pagers match the owning route exactly.
6. Run `python3 scripts/validate_site.py`.
7. Open the page in a browser, click through all four routes, and answer every quiz you added.

Adding a whole route is `routes/README.md`.

---

## 8. What never to do here

- Never link a `.md` file from a published HTML page. The deploy excludes `*.md`, so the link works locally and 404s live. The validator now fails on it.
- Never run `scripts/gen_outline.py` against this course. Its `outline.js` is hand-written and route-aware; the generator refuses, and if it did not it would destroy the mechanism.
- Never put the route in a lesson's path or file name.
- Never add a build step, a package manager or a framework.
- Never inline a copy of the design system. Link `../../assets/hub.css` and then `../assets/course-extras.css`, in that order.
