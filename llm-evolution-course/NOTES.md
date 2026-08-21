# Notes: teaching style, cadence, and known gotchas

Working notes for anyone writing into this course.
`MISSION.md` says what the course is for and `BUILDER-SPEC.md` is the contract; this file is the softer material that does not fit either.

## Voice

Plain, calm, and specific.
Short sentences carrying one fact each.
The reader is intelligent and knows nothing about this subject, and those two things are not in tension.

Prefer the concrete noun to the abstraction.
"A list of a few hundred numbers" beats "a high-dimensional representation" every time, and the reader who meets the second phrase later will already know what it means.

Never write in the voice of someone who finds this obvious.

## Cadence

Each lesson is a small argument, and the argument has the same shape every time.

1. Here is what was not possible.
2. Here is why it was not possible.
3. Here is what somebody did about it.
4. Here is what that made possible next, which is the next lesson's problem.

Step four is what makes the course a story instead of a list.
Do not skip it, and do not write it as a summary; write it as a debt the next lesson collects.

## The self-containment tax, and how to pay it cheaply

Section 1 of `BUILDER-SPEC.md` requires every lesson to name and link what it refers back to.
Writers find this awkward for about a day and then find it improves the prose, because it forces a claim to be restated in one clause rather than gestured at.

Three habits make it cheap:

- Restate the fact, then link the lesson. "A fixed-size vector could not hold a long sentence ([the seq2seq lesson](...) measured the decline)" reads better than a bare cross-reference and survives any reading order.
- Put anything you need more than twice into the glossary and link it there instead.
- If a lesson genuinely cannot be read without another one, say so in the "Where this lesson starts" block and list it as a prerequisite. That is what the prerequisites block is for.

## Diagrams

The captain's stated bar is that this course is diagram-heavy with deliberately low cognitive load.
In practice that means:

- One idea per figure. Two ideas is two figures.
- A block diagram for a structure, a sequence diagram for anything with a time order or an exchange between parties, a chart for a measured quantity.
- A figure that needs a legend needs splitting.
- Real numbers wherever the source gives you real numbers. A diagram that says "large" teaches less than one that says "40 GB".
- Caption is a teaching sentence, not an inventory of what is in the picture.

The stubs already contain a working sketch for every planned figure, so nobody starts from a blank block.

## Known gotchas

- **A Mermaid block is a `div`, never a `pre`.** `hub.js` appends a copy button to every `<pre>` on the page, and Mermaid renders from the element's `textContent`, so a `<pre class="mermaid">` renders as "Syntax error in text" with `copy` as the last line of graph source. It fails silently in the sense that nothing reaches the console; the only symptom is a small red error box where the diagram should be. Always look at the figures, never just count them.
- **A line break inside a Mermaid block is `&lt;br/&gt;`, never `<br/>`.** Same root cause as the `pre` gotcha above, and much harder to spot. The browser turns a literal `<br/>` into a real `BR` element, and `hub.js` stashes the graph source as `node.textContent` so it can repaint the diagram when the reader changes theme or palette. `textContent` drops the `BR`, so the two halves of the label are joined with no break **and no space**. The figure is right on first paint and wrong from the first palette click onwards, which is exactly why this survived a live audit of the whole site: `Hand-written rulesabout 1950 to 1990`. On a sequence diagram the same join can merge two statements and produce a red error box. Fixed across the course in the pull request that added lessons 0011 to 0018, and every figure written since must use the entity.
- **A semicolon in a Mermaid label or note is a statement separator.** `Note over A,B: it stops moving; each pass helps` is a parse error, not a note. Use a dash.
- **Check the label text, and check it again after changing the palette.** The number of `<svg>` elements on a page tells you nothing: an error box is an SVG, and a lost line break leaves a valid diagram that reads wrongly. Click a palette, then read the labels. If you want it mechanical, count `.mermaid svg br` and `.mermaid svg text tspan` before and after and confirm neither total falls.
- **Keep a figure inside the column.** The merged chapters run 854 to 906 pixels wide against an 854-pixel column. A `flowchart LR` with five or six boxes in a row reaches 1,400 to 2,300 and the reader has to scroll the figure sideways. Turn the chain vertical with `flowchart TB` rather than leaving it to scroll.
- **Mermaid measures text at render time.** On a cold cache it measures in the fallback font and the real face then overflows, which is why `assets/hub.js` waits on `document.fonts.ready`. If a label looks clipped on a first load and perfect on reload, that is this, and it is already handled. Do not work around it in the diagram.
- **The route parameter is only added by JavaScript.** If you hand-write a link between lessons, write the plain `NNNN-name.html` and let `outline.js` add `?route=` when it applies. A hand-written `?route=` in the markup pins the reader to a route they did not choose, and it silently blocks the stamping pass, which skips any href that already has a query.
- **The pager and the breadcrumb are committed for the route that owns the page**, which is the first route in `routes.js` containing it: the default route for a deep dive, and the spine route for a spine chapter. That is what makes them correct with JavaScript off. The validator enforces it, so do not hand-edit them.
- **Two titles per lesson.** The `h1` and the title in `routes.js` must match, because the second is what the rail and the pager display. The validator compares them.
- **`.md` files are not published.** The deploy excludes them. Never link one from a page.
- **Spine chapters are only in the spine route.** A reader can still land on one from a shared link carrying another route. `outline.js` handles that by using the chapter's own route for its pager, and the route switcher shows the other routes struck through.

## Where the material came from

Four scout reports, read and reconciled when this course was scaffolded.
They are not in this repository, and the stubs carry everything from them that a writer needs.

- The pre-2017 story and the founding era: thirteen lessons, and a list of what is verified against a primary source versus what is only widely repeated.
- The Transformer through ChatGPT: fourteen lessons, and a finished script for the tokenization lesson.
- ChatGPT to now: sixteen lessons, the four claim labels, and the living-document mechanism.
- The hub audit: the overlap map against `llm-papers-course`, the boundary between the two courses, and the argument against making the statistics course a prerequisite.

Where the reports disagreed on how many lessons the course should have, the one-pool-four-routes shape resolved it rather than picking a side. `MISSION.md` records that reasoning.

## Things deliberately not done

- No JSON data files for the comparison tables yet. The modern-era scout recommended keeping the model comparison tables as data rather than prose, and that is the right idea, but there are no tables yet because there are no lessons yet. Build it when the first table exists, not before.
- No per-lesson estimated reading time. It invites padding.
- No difficulty pills. This course is one difficulty: a beginner who has read what the lesson says it assumes.
