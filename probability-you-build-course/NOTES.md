# Notes

How this course teaches, and what the authoring cost.
Read `MISSION.md` first for why it exists, then `BUILDER-SPEC.md` for the markup contract
and `.claude/skills/course-authoring/references/widgets.md` for the `.build` wrapper.

## Learner profile

- A working engineer who ships AI features. Fluent in JavaScript or any C-family language;
  reading code costs them nothing and writing a ten-line loop is not an event.
- University probability gone cold or never formalised. Comfort with algebra is the whole
  mathematical prerequisite, inherited from PAI1.
- The tone difference that matters: this learner is not a beginner in thinking. Never pad.
  What they lack is the habit of quantifying their own uncertainty, and every build exists
  to build that habit in running code.

## Cadence

- One page is one tight idea plus one slice of the week's milestone path, sized to a single
  sitting: roughly 8 to 12 minutes of prose plus the time spent with the build.
- Every page opens with the orientation figure before its first body section, per the house
  standard. In this course the orientation figure usually shows where this idea sits inside
  the week's artifact - which panel of the planner it fills, which layer of the garden it draws.
- Quizzes come after the idea has been worked and the build slice has run, never as a gate.
- A week's first page is its build hub: what the finished artifact does, the milestone list,
  and the provenance of any frozen data it uses.

## Teaching preferences

- **Derive it, then code it, then check it by simulation.** The analytic result is worked on
  the page; the build computes the same quantity by Monte Carlo beside it; the reader sees
  the two agree within the stated tolerance. This triple is the course's signature move.
- **Predict-then-run.** Where the reader is about to observe a behaviour (Week 4 above all),
  the page asks for a written prediction first and the harness grades the prediction, not
  the model. State the honour-system rule where it applies.
- **Frozen data is labelled data.** Any price, latency or benchmark figure is a dated,
  cited snapshot isolated in one clearly marked constant object, so staleness cannot rot a
  derivation. Live API calls do not exist here.
- **Seeded randomness everywhere.** Builds use a seeded LCG (seed 42 by convention) so two
  readers see byte-identical points and screenshots match the prose.
- **Cross-link the formal treatment, never re-derive it.** Bayes, confidence intervals,
  axioms: link to `statistical-foundations-ml-course`; gradient descent mechanics, MLE in
  the abstract, backprop theory: link to `math-for-ml-course`. Verify the target anchor
  exists before committing the link.

## Structure decisions

- **Builds live inside lesson pages**, mounted into the shared `.build` wrapper, because the
  artifact is the teaching. A standalone repo the reader must clone would split the course
  in two. Build scripts shared across a week's pages live in `assets/builds/<name>.js`.
- **The `.build` wrapper rather than ad-hoc markup** because six weeks of builds need one
  consistent frame: canvas, controls, readout, caption. Its exact markup is frozen in
  `references/widgets.md`; do not invent a second shape.
- **Canvas + DOM, no frameworks**, because the hub is zero-dependency static HTML and the
  prototype evidence says everything these weeks need runs at interactive speed in plain JS:
  full MLP training with backprop included, 40k-trial Monte Carlo, 80x80 likelihood heatmaps.

## Known gotchas

Each as symptom, cause, fix.

- **Symptom:** the build looks right on load and wrong after the reader toggles theme or
  palette. **Cause:** `hub.js` repaints Mermaid but knows nothing of canvases, and a canvas
  bakes colours into pixels at draw time. **Fix:** draw only from tokens read at draw time,
  and re-draw when the theme changes - observe `data-mode` / `data-palette` on `<html>` with
  a MutationObserver and call the same render function the controls call. Store state outside
  closures so a redraw is lossless.
- **Symptom:** printed page shows the canvas in dark colours on white paper. **Cause:** the
  print stylesheet recolours CSS, not pixels; the canvas keeps whatever it drew last.
  **Fix:** for builds whose dark rendering is unusable on paper, add a `beforeprint`
  listener that redraws with print-safe ink (`--ink` on white), and redraw normally after
  `afterprint`. At minimum, say in the caption what the printed figure shows.
- **Symptom:** `C(n,k)` returns `Infinity`. **Cause:** factorials overflow double precision
  past 171!. **Fix:** compute the binomial coefficient with the multiplicative loop, never
  factorials.
- **Symptom:** gradient ascent oscillates or crawls depending on dataset size. **Cause:**
  raw-sum gradients change scale with n, so one learning rate cannot fit both. **Fix:**
  divide the update by the number of measurements (mean gradient) and keep one trainer
  configuration for the whole suite.
- **Symptom:** softmax bars show `NaN` after logits are dragged to extremes. **Cause:**
  bare exponentials overflow. **Fix:** subtract the max logit before exponentiating; say in
  the lesson that real stacks do exactly this.
- **Symptom:** a separation case "passes" trivially. **Cause:** float saturation freezes
  training near |z| = 37, so weight-norm probes stop moving. **Fix:** assert on the minimum
  confidence observable instead of the norm still growing.
- **Symptom:** quiz answers leak. **Cause:** options unmatched in length. **House rule, restated
  because it bites here:** match options to within 12 characters before committing.
- Everything documented in the root `AGENTS.md` about Mermaid (`<div class="mermaid">`,
  `&lt;br/&gt;`, no semicolons in labels) applies here at full force; this subject's labels
  are full of parentheses and maths.

## Honesty notes

- PAI1's internal course detail is behind a sign-in wall. Only public-page claims are
  sourced; no lesson may assert internal PAI1 specifics.
- Week 3's pyramid simulation runs on teaching constants, not the ScanPyramids paper's flux
  values; the geometry matches the published description, and lessons say so plainly. Do not
  state emulsion exposure durations or plate counts; they were never machine-read from the paper.
- The cos-squared angular law is standard folklore, cited as a "standard approximation".
- Platt scaling is cited from the bibliographic record; fetch the chapter before quoting it directly.

## Open threads

- Nothing is written yet. When Week 1 lands: check the ten-page grain, whether the `.build`
  wrapper carries every control shape used, and whether the cross-link map to siblings needs
  a standing table in `BUILDER-SPEC.md`.
- Whether each week wants a consolidated problems page inside its own block (the designs
  suggest yes for Weeks 3 and 4) - decide per week at build time.
