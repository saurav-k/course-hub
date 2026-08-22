# Mission

The record of the interview in `.claude/skills/course-authoring/new-course.md`.
This file is canonical: when a later authoring decision is argued, it is settled by re-reading this, not by re-deciding.

## Why this course exists

The hub uses mathematics constantly and teaches it in one place.

Measured across all seven courses that existed before this one, zero files contain `linear algebra`, `PCA`, `Jacobian`, `Taylor`, `convex`, `Lagrange`, `mutual information`, `p-value` or `bias-variance`.
Meanwhile `softmax` appears in twenty-one lessons of `llm-papers-course` and is never once derived, `cross-entropy` in six, `low-rank` in six, and `eigen` in exactly one.
A reader who finishes that course has met the softmax twenty-one times and has never been shown what it is.

This course supplies the substrate the rest of the hub stands on.

**The learner** is a working software engineer or architect with ten or more years in the job.
They reason fluently about systems, concurrency and failure, and they can read code in any language.
They are not a beginner at thinking.

**What it may assume:** programming, algorithmic thinking, and the patience to work something through on paper.

**The cold spot** is specific and it is not intelligence.
It is that the mathematics they met at university has gone cold, that the notation now reads as friction rather than as meaning, and that in several areas - linear algebra beyond matrix multiplication, optimization, information theory - they never met it at all.
So the on-ramp is genuinely from zero: the course defines its own notation, its own sets, its own logarithms, and assumes no symbol the reader has not been shown.

Two failure modes are equally fatal and the course is written against both.
Talking down to someone who ships distributed systems for a living is one.
Assuming a symbol they last saw in 2009 is the other.

## The source

Two, and they are not the same syllabus.

- The published lecture series that `statistical-foundations-ml-course` expands: IIT Bombay, Nikhil Karamchandani and D. Manjunath, whose twelve-lecture roadmap is a probability course ending at conditional expectation and MMSE.
- A set of EPGD-AI&DS course notes covering applied statistics and linear algebra, ending at regression inference.

Neither contains the other. The published roadmap has no MLE, no confidence intervals, no hypothesis testing and no regression; the notes have no moment generating functions, no law of large numbers, no conditional expectation and no MMSE.

**This course carries the union of the two**, which is the only coherent syllabus either of them points at.

The notes are a **syllabus signal and a topic checklist only**: what was covered, in what order, at what depth, and which worked examples the lecturer chose.
They are not copy. No prose, no figure and no table is lifted from them, and every claim on every page comes from a primary source the author fetched and read.
See `RESOURCES.md`.

## Success looks like

The learner can:

- Take any formula off a machine learning paper, name every symbol in it in words, and say what it computes.
- Read a matrix as a linear map and say what it does to space, not only what its entries are.
- Derive a gradient by the chain rule and say why gradient descent moves the way it does.
- Put a distribution on a quantity, defend the modelling assumption, and say where it stops being true.
- Read a confidence interval or a p-value and say precisely what it does and does not claim.
- Say why cross-entropy is the loss, in terms of both likelihood and information.
- Take any program in this course, point it at a hundred times more data, and trust the answer.

The failure that would still be a failure with every page accurate: a reader finishes it able to recite definitions and still cannot read the maths in a paper.
Every page is written against that, which is why every page carries a picture before its formula and a problem after it.

## Structure

**One shape, held for the whole course: the lesson.** One tight idea, one fully worked numeric example of that idea, at least two quizzes and at least one practice problem.

Eleven modules, roughly 133 content pages, 900 to 1,400 prose words each and 1,800 the ceiling.
Practice text and quiz text are not prose and do not count against that ceiling.

| # | Module | Owner |
|---|---|---|
| M01 | Foundations: notation, sets, functions, logs, counting, limits | r2 |
| M02 | Data and summaries: variables, charts, centre, spread, quantiles, correlation | r9 front |
| M03 | Vectors, matrices, and linear maps | r3 |
| M04 | Eigenvalues, SVD, and PCA | r4 |
| M05 | Calculus for machine learning | r5 |
| M06 | Optimization | r6 |
| M07 | Probability | r7 |
| M08 | Expectation, limits, and simulation | r8 |
| M09 | Estimation, testing, and inference | r9 back |
| M10 | Information, similarity, and dimension | r10 |
| M11 | Capstone: regression, end to end | named owner |

The order is a topological sort of the prerequisite graph, and **file numbers follow it**, so `lessons/NNNN` in ascending order is always a legal reading order.
Two consequences worth stating: M04 precedes M05 because everything in M04 is calculus-free once PCA is derived through the SVD, and M02 sits second because descriptive statistics needs nothing but M01 and a reader should meet a histogram long before they meet the Central Limit Theorem.

**Single route.** One order, no `routes.js`. Every page is additionally labelled `core` or `depth` in its brief: `core` is the roughly thirty-page path a reader needs to read a modern paper. That partition is recorded from day one so a fast-track route can be added later without renumbering anything, and `reference/by-subject.html` and `reference/interview-index.html` serve the other two orders as link indexes rather than as routes.

## The ladder

- **Foundation** (`pill easy`): arrives cold. Every term is defined here or in a named earlier page. M01, M02, and the opening of M03 and M07.
- **Working** (`pill med`): has the foundation pages. Can be given a mechanism and a trade-off directly. Most of M03, M05, M07, M08, M09.
- **Frontier** (`pill hard`): has the working pages. Can be handed an open question or a live disagreement. M04, the back of M06, the back of M10, and M11.

The ladder is a claim about dependencies, so it is checkable: read the map in order and confirm no page needs a page that comes later.

## Constraints

Six, and none of them restates the house standard.

1. **A stated proof for every named theorem.** Where the course names a theorem - the spectral theorem, the Central Limit Theorem, the law of large numbers, Bayes, rank-nullity, Eckart-Young - it states the proof rather than asserting the result. The proof is written to be read, not to be rigorous for its own sake: the shape of the argument, the step that does the real work, and honestly named where a full proof is beyond the course. A page that names a theorem and skips its proof is incomplete.

2. **Runnable code for every theorem or named result.** A self-contained Python program using only NumPy and Pandas, which implements the result and runs against a generated dataset large enough that hand calculation is impossible. It appears on the page in the code widget and as a downloadable `.py`. The hand-worked example stays: the code is the scale-up path, not a replacement. Layout, naming and the dataset standard are in `BUILDER-SPEC.md`.

3. **A picture before every formula, and a problem after it.** The house standard asks for the mental model before the mechanism. Here that is literal: no formula appears on a page before a figure that shows what it means, and no page ends without at least one problem the reader works themselves.

4. **At least one hand-authored `svg.chart` on every content page.** Mermaid cannot draw a distribution, a density, a vector, a unit ball or a contour, and those are the figures this course is made of. A page whose only figures are flowcharts has drawn the filing system rather than the mathematics.

5. **Rows are samples, columns are features.** The data matrix has one orientation for the whole course. It is the machine learning convention and it is what the reader will meet in a paper. Every module obeys it, and a page that needs the transpose says so explicitly.

6. **One meaning, one colour, on every page.** The chart palette is fixed in `BUILDER-SPEC.md` and it does not drift between modules.

## Out of scope

- **Machine learning itself.** Models, training procedures, architectures. Owned by `llm-papers-course` for mechanism and `llm-evolution-course` for the story.
- **Measure-theoretic probability.** This is an engineering course. Where a result genuinely needs measure theory, the page says so and states the engineering version.
- **Numerical analysis as a subject.** Conditioning and stability appear where they change an answer; algorithms for their own sake do not.
- **Statistical software and library tutorials.** The code in this course is NumPy and Pandas used as arithmetic, never as an API to be learned. `Basic Statistics on NumPy Arrays` is not a mathematics lesson.
- **Deep learning specifics.** Backpropagation appears as the chain rule; architectures do not.

## Siblings

- **`statistical-foundations-ml-course`** is a separate, live course and this one does not touch it. It expands one IIT Bombay lecture across nine pages, deck-faithful, with every number matched to the slide it came from. This course covers the same probability and statistics ground in M02 and M07 to M09, and covers a great deal more besides, so the two overlap on purpose rather than by accident.

  **The boundary, stated so the two do not re-converge.** That course answers "what did that specific lecture say, worked in full". This one answers "what maths does machine learning stand on". Where they meet, **this course links there and never the other way**: a page here may point a reader at the deck-faithful treatment, and nothing there is edited to point back. Neither re-derives the other, and neither is a prerequisite for the other.
- **`llm-papers-course`** is where every result in this course gets used. The softmax, cross-entropy, low-rank adaptation and the scaling laws all live there. Cross-link out; never re-teach the paper.
- **`production-systems-course`** owns percentiles and queueing arithmetic as operational tools. This course owns the distributions underneath them.

## Revisit when

M02 is finished, which is the first module written to the full bar including the proof constraint and the code constraint.
At that point check three things: whether 900 to 1,400 prose words survives contact with a stated proof plus a runnable program, whether one practice problem per page is enough, and whether the `core`/`depth` partition drawn on paper still matches the pages that exist.
