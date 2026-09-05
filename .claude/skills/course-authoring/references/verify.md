# The gate

Three layers, cheapest first.
A page is done when all three pass, and not when the draft reads well.

## 1. The machines

```bash
python3 scripts/gen_outline.py <course>     # skip on a routed course; it refuses
python3 scripts/validate_site.py
python3 scripts/check_pages_gate.py
python3 .claude/skills/course-authoring/scripts/check_pages.py <course-or-file>
python3 .claude/skills/course-authoring/scripts/check_pages.py <course> --links   # fetches every external link once
python3 scripts/render_sweep.py <course-or-file> --narrow                          # needs Chrome and the network
```

`validate_site.py` gates the pull request.
It checks registration, links, that no page links a local `.md` file, and that each course `outline.js` names exactly the lessons on disk.
On a routed course it also checks the route manifest, every committed pager against its owning route, and the living-document metadata.

`check_pages.py` checks the house standard: the design-system links, the Mermaid traps, widget shapes, the learning contract and the recap, the orientation figure, a worked instance before the formula, the word and paragraph ceilings, the diagram, quiz and practice counts, the answer-index distribution, the rung word on the rung pill, the pager against the course map, and that the page links a source at all.
`check_pages_gate.py` is the same checker as a gate on the difference from `scripts/check-pages-baseline.txt`, and it is what CI runs; a FAIL you fixed turns it red until the baseline is refreshed, which is the last commit of a retrofit.
All green before you open the pull request.
A warning from `check_pages.py` is a decision you must be able to defend in the pull request body, not a line to scroll past.

`render_sweep.py` is the machine half of layer two below.
It renders every page in headless Chrome with the network on, counts Mermaid error boxes and blank renders, reads every diagram's label text, and checks that the body does not scroll sideways; then it presses the reader's own light-and-dark control, waits for the repaint, and does all of it again.
With `--narrow` it also lays each page out at 360px.
It cannot read a drawing, so it replaces the counting in layer two and none of the looking.

One of those warnings is an estimate rather than a reading, and it is worth knowing which.
**The label-edge warning** measures where each `<text>` in a hand-drawn `svg.chart` ends and says so when the estimate puts it outside the figure's own `viewBox`, which is where the browser cuts it.
It is an approximation of a font metric the script does not have: the width of a string is estimated from the character count, the size the class is painted at, and one advance per face - `.d-mono` is JetBrains Mono at exactly .6em a glyph, everything else is Inter at the .4739em `hub.css` measures, rounded down so a proportional label is under-stated.
So it is a WARN and it under-reports on purpose.
A label it names is a figure to open and read at full width, not a coordinate to nudge until the warning stops.
Nothing it stays quiet about is proven safe: the browser pass below is still the check.

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

The runtime redraws every diagram on a mode or palette change, from a stash of the graph source it took as `textContent` before the first render, with every colour token re-resolved against the new ground.
A literal `<br/>` in a label is therefore joined with no space in both states - the stash never had the `BR` - and the browser is where you see `first halfsecond half`; a colour that reads on cream and vanishes on near-black, and a repaint that never happens, are visible only after the switch.

So: load the page, look at every figure, then change the mode or the palette from the Appearance control, and look at every figure again.
`scripts/render_sweep.py` does the counting half of that for a whole course; the looking is still yours.

**Counting the SVGs proves nothing**, because a Mermaid error box is itself an SVG.
When you check by machine, match `.error-icon`:

```js
document.querySelectorAll('.mermaid .error-icon, .mermaid text.error-text').length   // must be 0
```

Then look anyway. A diagram that parses can still say the wrong thing.

**What the repaint is compared on is the rendered label text.**
Read every label out of every diagram on first paint, repaint, read them again, and diff the two lists; `render_sweep.py` does exactly this.
A difference means the stash and the authored source disagree, which is the shape every repaint defect takes, and it is what an error-box count cannot see.
One trap in the diff: Mermaid writes its `classDef` colours into the SVG's own `<style>` element, which changes with the palette by design, so strip that element before comparing or every palette switch reports two false positives.
And one limit: a `<br/>` joined on first paint is joined the same way after it, so the diff is quiet and the static FAIL in `check_pages.py` is the catch, with your eyes on the label as the proof.

**Twice over, on two different palettes, when the sweep is a whole course.**
Seven palettes and two modes exist and a repaint is a repaint, so one switch proves the mechanism; a second switch to a different palette is what catches a colour that only fails on one ground.
The sweep this list comes from ran 87 pages on the shipped default, again on `ink` + `dark`, and again on `sage` + `dark`.

### The rest of the browser pass

- **Every diagram legible at its authored size.** A wide Mermaid diagram scaled down to fit the reading column is unreadable, and its own caption will be larger than its labels. The figure should scroll inside its box rather than shrink. Check the widest figure on the page, and check it can be reached by keyboard: `hub.js` gives a box that genuinely overflows a tab stop and takes it back when the column grows.
- **Both modes and more than one palette.** Seven palettes and three modes exist, and the accent each course wears is the palette's accent rotated by that course's hue. A colour that reads on cream can disappear on near-black, and a literal hex in a hand-authored SVG is the usual cause.
- **Print preview.** Diagrams carry their colours inside the SVG, so `hub.js` draws an ink-on-paper copy of each one while the browser is idle and swaps it in on `beforeprint`. If a figure prints in screen colours or as raw graph source, that mechanism is what broke. Driving `beforeprint` and `afterprint` by hand is enough for a spot check and it also proves the screen state comes back: the print path opens every content disclosure and has to restore each one exactly.
- **360px wide.** The figure may scroll; the page body may not. Horizontal scroll on the body is a bug every time. This is a pass over the whole course rather than a look at one page, because what spills at 360px is a nowrap row and those are in the chrome, not in the lesson you wrote.
- **The longest line of text in every hand-drawn figure, at 360px and at full width.** SVG text neither wraps nor is bounded by the `viewBox`, and the browser's own `overflow: hidden` cuts it at the frame edge, so the tail of a long label is simply gone. Nothing reports it: the element is in the DOM, `getBBox` returns a real box, and a figcaption can happily describe words no reader can see.
- **Every hand-drawn figure read for what its roles claim.** The `d-*` classes make fill mean something, so a box drawn `d-ghost` with a live `d-flow` into it says "removed" and "reading" at once. Nothing in the repository catches a figure that contradicts itself; it renders, it validates, and it teaches the wrong thing.
- **Every interactive figure operated, once with the mouse and once from the keyboard.** One pass per shape on the page, not one pass per page: a stepper, an assembler, a calculator, a scorecard and a taint map fail in five different ways. Tab to each control, drive it - Enter on a stepper's Next, arrow keys on a range, Space on a checkbox - and confirm the focus ring travels with you. Then read the **readout and the output together**: an assembler that writes its file into the wrong element still updates its readout correctly beside it, which is how one shipped inert past every check in this repository.
- **Every interactive figure read once with the script blocked.** Turn JavaScript off and reload. Every step, every fix, every block and every committed default value must be there and must be right, because that is what the page shows a reader with no script and what every printed copy shows. An assembler is the one to look at hardest: its `<pre>` is committed by hand and is the one default in these five that can drift from the templates beside it.
- **Every quiz answered.** Click the right option and confirm it goes green; click a wrong one and read the feedback you wrote. A `data-answer` off by one is invisible until someone clicks it.
- **The sidebar rail.** Your new lesson appears in it, in the right module, and is marked as the current page. If it is missing, `outline.js` was not regenerated.
- **Every copy button.** They are injected into every `<pre>`; confirm the one you added copies what you meant.
- **Every link you touched**, including the ones back at the neighbours whose pagers you changed.

## 3. The reading

Read the page start to finish as the learner in `MISSION.md`, not as its author.

- **Read each figure's two lines without looking at the drawing.** The label should name a subject and the claim should state something you could argue with. If the claim only describes the picture, the figure has a title and no point; if the label argues, the two lines have swapped jobs.

- **Cover the page and look only at the h1 and the orientation figure.** Can you say what this page is about and why it exists? That is the whole test, and it is the one the machine cannot run. If the answer is no, the figure is decoration and the page has no big picture.
- **Read the learning contract as a stranger.** Could you be watched doing each outcome? Does the prerequisite line name a page you could open, or say plainly that none is needed? An outcome that names a topic rather than an action - "understand attention" - is the one-minute version wearing the wrong card.
- **Read the recap against the one-minute version.** No point repeats a bullet from the top, every point is something the reader can now say unprompted, and the next step gives a reason and not only a title.
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
