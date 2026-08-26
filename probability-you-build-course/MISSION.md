# Mission

The record of the commissioning interview, held against the three design reports for this
course (`pai-w12`, `pai-w34`, `pai-w56`) and Stanford's public PAI1 pages.
This file is canonical: when a later authoring decision is argued, it is settled by
re-reading this, not by re-deciding.

## Why this course exists

This is the build-first probability course. Every week exists so the learner ships a
working, demonstrable browser artifact, and every concept arrives at the moment the build
needs it - never earlier. A reader who finishes a week has something running they can show
another person. The build is the spine; theory serves it.

It is modelled on Stanford's *Probability for AI* (PAI1, Chris Piech and Mehran Sahami,
October 2026 cohort): a free six-week programme whose certificate is "a public portfolio of
your work", whose weekly table pairs each topic with one build, and whose stated workload
is "a few focused hours each week". One divergence is deliberate and recorded here so
nobody later mistakes it for a misreading: PAI1 tells its general-public audience that no
coding is needed. Our learner is a working engineer, so this course goes further than PAI1
and has the reader **write** the decision logic, the optimiser and the audit harness as
vanilla JavaScript in the lesson page itself. Everything else - algebra-only prerequisite,
portfolio artifact per week, build as spine - we keep.

## The learner

A working software engineer who ships AI features and is comfortable in JavaScript or any
C-family language. University probability has gone cold or was never formalised; comfort
with algebra is all the maths this course assumes, exactly as PAI1 does. The learner is not
a beginner in thinking - they reason about systems, trade-offs and failure daily. They are
a beginner again in reading their own uncertainty as numbers, and the builds exist to fix
that with running code rather than notation.

## Success looks like

The learner can:

- Compute, from first principles and in code they wrote, the cheapest policy that clears a
  quality bar for an inference request, and revise it by Bayes when evidence arrives (Week 1).
- Sample from any distribution with an invertible CDF using uniforms they generated, and
  read a histogram against its theoretical curve (Week 2).
- Point an instrument at counted data, write the likelihood of that data under competing
  hypotheses, and say how much the winning hypothesis can be trusted (Week 3).
- Train a logistic-regression classifier they wrote line by line, predict before running
  where it will fail, and be right (Week 4).
- Read a network's internal state as probabilities and explain a large language model's
  sampling behaviour as the softmax they just watched concentrate (Week 5).
- Refuse to accept any model claim that lacks an interval, a calibration statement, and a
  who-pays-for-errors analysis (Week 6).
- Assemble the six weeks into one public project that survives a sceptical reviewer (capstone).

The failure that would still be a failure even if every page were accurate: a reader who
finishes able to recite the theory but with nothing running. If a week ends without a
demonstrable artifact, the week has failed its mission regardless of how correct its pages are.

## The source

Stanford PAI1's six-week You Learn / You Build table is the spine:

| Week | Learns | Builds |
|---|---|---|
| 1 | Core probability | Spend Planner - an inference-time resource decision maker |
| 2 | Random variables | Distribution Garden - probabilistic artwork |
| 3 | Maximum likelihood | Hidden pyramid chamber, phone tracker, zero-failure paradox |
| 4 | Logistic regression | An adversarial test suite for the model |
| 5 | Neural networks | Glass Network + Sampling Bench |
| 6 | Probabilistic evaluation | Audit Bench - calibration and fairness critique |
| Beyond | Final project | Portfolio capstone |

Only PAI1's public claims are sourced (its internal course detail is behind a sign-in wall);
the three design reports expand each week into build-ready specifications, and those
specifications are the ceiling for what a week's lessons claim.

## Structure

One page is one tight idea plus, on build-bearing pages, one slice of the week's milestone
path. A week is eight to ten lesson pages following one build thread, where each milestone
stays independently runnable - a reader who stops mid-week keeps something working.
Lesson numbers live in reserved blocks of one hundred per week so weeks can be written in
parallel without collision; see [`PLOT.md`](PLOT.md).

Every interactive build renders inside the shared `.build` wrapper documented in
`.claude/skills/course-authoring/references/widgets.md`: canvas, controls, readout,
caption. Build scripts live in `assets/builds/` and are plain JavaScript with zero
dependencies. Data is either generated in-page from a seeded generator or enters as a
frozen, dated, cited snapshot; nothing calls an API at runtime.

## Constraints

- **Zero dependencies.** No framework, no chart library, no CDN beyond the hub's Mermaid.
  Every build runs offline off `file://`.
- **The artifact must run inside the lesson**, not beside it. A Python file the reader
  cannot see running would defeat the mission.
- **Frozen data over live data.** Prices, latencies and any external figures enter as
  dated snapshots cited to their vendor pages, isolated in clearly marked constants, so
  staleness stays harmless. No keys, no network at runtime, ever.
- **Simulation is the verification.** Where a page states an analytic result, the build
  shows the simulated number beside it and the two must agree within the stated tolerance.
- **Cross-link, never re-derive.** Formal treatments belong to the sibling courses named below.
- Full prose, complete sentences, plain dash, never an em dash.

## Out of scope

- Measure-theoretic probability and proofs as ritual. `statistical-foundations-ml-course`
  owns the careful foundations; link to its pages instead of re-deriving them.
- Optimisation theory beyond grid search and hand-coded gradient ascent. Newton's method,
  BFGS and friends are named once in a callout and go no further; the mechanics behind them
  belong to `math-for-ml-course` (gradient descent family, lessons 0102-0108).
- Multiclass softmax, minibatching SGD, and architecture design. Named where the build
  touches them, deferred to the courses that own them.
- Live API calls of any kind, and any dependency requiring installation.

## Siblings

- `statistical-foundations-ml-course` - the formal lecture treatment: probability axioms,
  conditional probability, Bayes, confidence intervals, deck-faithful, deliberately no
  programming exercises. When a concept page here needs the derivation done carefully,
  it links there (for example Bayes at `lessons/0023-bayes-rule.html`).
- `math-for-ml-course` - owns MLE in the abstract (lesson 0162), gradient descent
  (0102-0108), backpropagation (0086) and entropy/cross-entropy (0180-0181).
- `llm-inference-course` - where the serving-side economics behind Week 1's spend decisions
  are treated at production depth.

## Revisit when

Week 1 lands. At that point check whether ten pages per week is the right grain, whether
the `.build` wrapper carries every control shape the weeks actually use, and whether the
cross-link density to the sibling courses is right or needs a standing map.
