# The gate

Three layers, cheapest first.
A page is done when all three pass, and not when the draft reads well.

## 1. The machines

```bash
python3 scripts/gen_outline.py <course>     # skip on a routed course; it refuses
python3 scripts/validate_site.py
python3 .claude/skills/course-authoring/scripts/check_pages.py <course-or-file>
```

`validate_site.py` gates the pull request.
It checks registration, links, that no page links a local `.md` file, and that each course `outline.js` names exactly the lessons on disk.
On a routed course it also checks the route manifest, every committed pager against its owning route, and the living-document metadata.

`check_pages.py` checks the house standard: the design-system links, the Mermaid traps, widget shapes, the orientation figure, the word ceilings, the diagram and quiz counts, the answer-index distribution, and the rung and reading-time pills.
Both green before you open the pull request.
A warning from `check_pages.py` is a decision you must be able to defend in the pull request body, not a line to scroll past.

Neither script checks arithmetic, whether a claim matches its source, or whether a diagram renders.
Those are layers two and three, and they are where the real defects live.

## 2. The browser

There is no build step, so serve the repository root and open the real page:

```bash
python3 -m http.server 8000
```

Serve it rather than opening the file directly: Chrome gives every `file://` page its own opaque origin, so the mode and palette the runtime persists cannot be read back, and the repaint path you are about to test is the one that will not run.

Walk this list. Every item has been a live defect on this site.

### Look at every diagram, in both render states

This is the check that catches the most and is skipped the most.

Two classes of diagram defect exist and they are visible at opposite times.
A `<pre class="mermaid">` is broken on **first paint**, because the copy button `hub.js` appends has already become the last line of graph source.
A literal `<br/>` in a label is correct on first paint and broken on **every repaint after it**, because the runtime stashes the graph source as `textContent` in order to redraw it, and `textContent` has no `BR` in it, so the two halves join with no space and a sequence diagram can merge two statements into a red error box.

So: load the page, look at every figure, then change the mode or the palette from the Appearance control, and look at every figure again.
Checking one state catches neither class reliably.

**Counting the SVGs proves nothing**, because a Mermaid error box is itself an SVG.
When you check by machine, match `.error-icon`:

```js
document.querySelectorAll('.mermaid .error-icon, .mermaid text.error-text').length   // must be 0
```

Then look anyway. A diagram that parses can still say the wrong thing.

### The rest of the browser pass

- **Every diagram legible at its authored size.** A wide Mermaid diagram scaled down to fit the reading column is unreadable, and its own caption will be larger than its labels. The figure should scroll inside its box rather than shrink. Check the widest figure on the page, and check it can be reached by keyboard: `hub.js` gives a box that genuinely overflows a tab stop and takes it back when the column grows.
- **Both modes and more than one palette.** Seven palettes and three modes exist, and the accent each course wears is the palette's accent rotated by that course's hue. A colour that reads on cream can disappear on near-black, and a literal hex in a hand-authored SVG is the usual cause.
- **Print preview.** Diagrams carry their colours inside the SVG, so `hub.js` draws an ink-on-paper copy of each one while the browser is idle and swaps it in on `beforeprint`. If a figure prints in screen colours or as raw graph source, that mechanism is what broke.
- **360px wide.** The figure may scroll; the page body may not. Horizontal scroll on the body is a bug every time.
- **Every quiz answered.** Click the right option and confirm it goes green; click a wrong one and read the feedback you wrote. A `data-answer` off by one is invisible until someone clicks it.
- **The sidebar rail.** Your new lesson appears in it, in the right module, and is marked as the current page. If it is missing, `outline.js` was not regenerated.
- **Every copy button.** They are injected into every `<pre>`; confirm the one you added copies what you meant.
- **Every link you touched**, including the ones back at the neighbours whose pagers you changed.

## 3. The reading

Read the page start to finish as the learner in `MISSION.md`, not as its author.

- **Cover the page and look only at the h1 and the orientation figure.** Can you say what this page is about and why it exists? That is the whole test, and it is the one the machine cannot run. If the answer is no, the figure is decoration and the page has no big picture.
- **Which paragraph does a figure already say?** Read every paragraph beside the figure nearest it. Where the two say the same thing, the paragraph goes. This is where a page comes down under the word ceiling, and cutting here costs the reader nothing.
- **Is there one idea?** If the summary needs "and", it is two pages.
- **Does anything arrive before its scaffold?** A symbol before its name, a formula before its picture, a mechanism before its model.
- **Is any step missing?** Where you compressed arithmetic, expand it. The reader must never reconstruct what you skipped.
- **Does every technique carry its cost?** A section listing only benefits is unfinished.
- **Did you fetch every source you cited, this session?** A link you did not open is a claim you did not check.
- **Would the distractors fool someone who half-knows this?** An implausible distractor is a wasted option, and four options with one plausible pair is a two-option question.

## What the pull request says

What changed, why, and what you verified from the list above.
Say explicitly that you looked at the diagrams in both render states, because that is the check whose absence is invisible.
Where you were unsure whether something is still true, say so in the pull request rather than asserting it in the lesson.

Then stop.
A human reviews and merges, and merging publishes the live site.
