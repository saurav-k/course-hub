# Builder spec - the delta for Probability You Build

The house standard is `.claude/skills/course-authoring/`.
It carries the page contracts, the widget vocabulary, the teaching bar, and the verification gate, and it governs this course as it governs every other.

This file carries **only what is true of this course and not of the hub**.

Where this file and the skill disagree, the skill wins, and the disagreement is a bug to raise in the pull request.

## The gold page

None exists yet: no lesson is written. `lessons/0000-*` of Week 1 becomes the gold page the moment it lands, and every later page in this course is matched against it.
Until then the shape expectations are the house content-page contract plus the deltas below.

## What this course does differently

1. **Every interactive build uses the shared `.build` wrapper, with exactly this markup** (frozen by coordination contract; documented in full in `.claude/skills/course-authoring/references/widgets.md`):

   ```html
   <figure class="build" id="<build-id>">
     <div class="build-stage"><canvas class="build-canvas" width="..." height="..."></canvas></div>
     <div class="build-controls"> ... labelled inputs/buttons ... </div>
     <div class="build-readout"> ... live numeric output ... </div>
     <figcaption> ... what the reader should see and why ... </figcaption>
   </figure>
   ```

   Do not rename these classes and do not invent a second interactive shape. The `id` is required so a caption or quiz can link straight at a build.

2. **Build scripts live in `assets/builds/<name>.js`**, one file per build (muon chamber,
   tracker, planner, harness, glassnet, audit bench). A page loads its builds from the head:

   ```html
   <script src="../assets/builds/planner.js" defer></script>
   ```

   `defer` keeps head loading intact while guaranteeing the canvas exists when the script runs. Nothing loads at the end of `<body>`.
   A build file guards against double-initialisation and exposes nothing global except what
   a lesson page genuinely needs to call.

3. **Canvas code draws from tokens, and redraws on theme change.** Read colours at draw time
   via a probe element (`probe.style.color = 'var(--stat)'` then `getComputedStyle(probe).color`,
   normalised through a 1x1 canvas fill if you need hex), keep state outside closures, and
   re-render when the reader changes mode or palette:

   ```js
   new MutationObserver(render)
     .observe(document.documentElement, { attributes: true, attributeFilter: ['data-mode', 'data-palette'] });
   ```

4. **Frozen data enters as one dated constant object**, cited in a comment to the vendor page
   it came from, with the fetch date. Never scatter stale numbers through the logic, never
   fetch anything at runtime. Prefer neutral tier names (nano / standard / frontier) over
   brand-specific model names, with real anchors in comments.

5. **Randomness is seeded.** Builds use a seeded LCG (seed 42 by convention) rather than bare
   `Math.random()`, so two readers see identical data and screenshots match the prose. Where
   genuine randomness *is* the lesson (regenerate buttons), seed from a field the reader can set.

6. **The verification triple: derived, then coded, then simulated.** When a page states an
   analytic result that a build can exercise, the build shows the simulated value beside the
   analytic one and the caption states the agreement tolerance. This is the course's
   signature move; a build that asserts without verifying is half a build.

7. **Predict-then-run on Week 4's suite.** A case carries the learner's written prediction
   before the runner grades it. State the honour-system rule in the lesson text.

8. **Numbering blocks are reserved per week.** Week 1 owns `0000`-`0099`, Week 2
   `0100`-`0199`, and so on through the capstone at `0600`-`0699`; see [`PLOT.md`](PLOT.md).
   Take free numbers inside your own block only.

## The lesson map

**The map lives in `index.html`, and only there.**
Every week currently sits in it as a module section with a `.roadmap` list of its planned
pages, plain text, never links. When a week's pages are written they become real cards in
that same module, at the same position, and their roadmap entries are removed.
`scripts/gen_outline.py` reads the cards; the validator fails a pull request whose lessons
on disk disagree with the map.

## Cross-linking

`statistical-foundations-ml-course` owns the formal derivations (axioms, conditional
probability, Bayes at `lessons/0023-bayes-rule.html`, confidence intervals);
`math-for-ml-course` owns MLE in the abstract (0162), gradient descent (0102-0108),
backpropagation (0086) and cross-entropy (0180-0181); `llm-inference-course` owns serving
economics. Link to the page that derives, do not re-derive here, and verify the anchor
exists before committing: the validator strips fragments and will not catch a dead one.
