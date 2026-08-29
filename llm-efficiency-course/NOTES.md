# Notes

How this course teaches. Read `MISSION.md` first for why it exists.

## Learner profile

Fluent in Python and the shell; has deployed something with Docker; reads a trace without flinching. Not fluent in quantization error analysis or low-rank algebra, and mildly embarrassed about it - so the tone is direct, never remedial. They asked, in their own words, "can I actually run this thing on the hardware I already bought, and how much work will it do."

## Cadence

One page is one idea at 900 to 1,400 prose words, three or more diagrams in at least two kinds, two or more quizzes, one practice problem, one chart. The orientation figure on every page draws the course spine: the wall (bandwidth), the shrink (quantization), the steer (adapters), the multiply (speculation), the deploy (case studies) - and shows where this page's idea sits on it. A page ends where the next mechanism begins; no page straddles two.

Quizzes follow the worked idea, never precede it. The practice problem always reuses the running model or hardware numbers so the arithmetic compounds instead of resetting.

## Teaching preferences

- Arithmetic on the page, every time a number appears. A derived figure is labelled `derived`, never dressed up as a measurement.
- The one analogy of the course: memory bandwidth is the narrow doorway; compute is the wide room behind it. Quantization makes the boxes smaller, LoRA sends a memo instead of the whole staff, speculation sends several boxes with one inspection.
- Charts are drawn with the hub's inline `svg.chart` shapes, one per page minimum, because this course asserts magnitudes.
- GLM-5.3-Flash numbers recur across pages; introduce them once on `0002` and reference thereafter.

## Structure decisions

- Lessons, not chapters: each page develops one mechanism. The two case-study pages and the Module 05 capstone and lab reuse every prior mechanism in one worked deployment, which is what makes the shape lesson rather than reference.
- The wider-PEFT page sits after QLoRA, not before, because DoRA and IA3 only make sense once low-rank updates and 4-bit bases are in hand.
- Mac case study after the Spark case study: the cluster page introduces the KV-budget and parallelism concepts the solo-machine page reuses.

## Known gotchas

- Mermaid: `&lt;br/&gt;` for line breaks, no semicolons in labels, `<div class="mermaid">` only.
- The FP8 checkpoint is ~306 GiB and does NOT fit two Sparks; every fit claim in this course runs on NVFP4 derivations. Say "derived" every time.
- Reading-time pill = prose words / 200 plus half a minute per figure and quiz, rounded.
- Answer indexes must vary across the course; check with a Counter before the PR.
- `hub.js` binds the quiz classes; a hand-rolled quiz shape is inert. Copy `widgets.md` character for character.
