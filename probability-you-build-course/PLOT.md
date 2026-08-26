# Plot - the reading order of Probability You Build

This file records the true reading order of the course: where every week and every lesson
sits, and everything planned but unwritten.

The order rule, which holds for this course and every course in the hub: **a course's
reading order is its true order, and a build milestone that follows a concept page sits
after that concept page in the course map, never in a separate list at the bottom.**
When this file and the course `index.html` disagree, one of them is wrong, and it gets
fixed before anything new is added.
New material takes its real position here and in `index.html`; it is never appended to
the end just because it arrived last.

Status marks used below:

- **written** - on the site today.
- **in progress** - being written right now, not yet on this branch.
- **reserved** - the position is held; nothing else may take it; nothing is written.

## The numbering blocks

Six weeks are being written in parallel, so each week owns a reserved block of one hundred
lesson numbers. Week 1 starts at `0000`. **Never renumber anything**: the moment a week's
first page is published its URLs are public, and a collision between two parallel workers
is resolved by taking free numbers inside a block, never by moving a published page.

| Block | Owner | Status | Notes |
|---|---|---|---|
| `0000`-`0099` | Week 1 - Core probability | reserved | The Spend Planner. |
| `0100`-`0199` | Week 2 - Random variables | reserved | The Distribution Garden. |
| `0200`-`0299` | Week 3 - Maximum likelihood | reserved | Pyramid chamber, phone tracker, zero-failure paradox. |
| `0300`-`0399` | Week 4 - Logistic regression | reserved | The adversarial test suite. |
| `0400`-`0499` | Week 5 - Neural networks | reserved | Glass Network + Sampling Bench. |
| `0500`-`0599` | Week 6 - Probabilistic evaluation | reserved | The Audit Bench. |
| `0600`-`0699` | Capstone | reserved | The portfolio final project. |

## The sequence

Every row below is reserved: the titles come from the week design reports and are the
contract for what each page does, but nothing is written yet. A week worker may adjust a
slug or split a page inside its own block freely; it may not reach into another block.

| # | Position | Status | Notes |
|---|---|---|---|
| 1 | **Week 1: Core probability - the Spend Planner** | reserved | Ten pages planned, `0000`-`0009`: a build hub, then sample spaces, axioms and the complement rule, conditional probability via the escalation check, the multiplication rule, total probability as the cascade decision, Bayes updating of model reliability, independence and when it lies, counting for majority vote, expected cost and the assembled planner. Milestones M1-M5 each stay independently runnable. |
| 2 | **Week 2: Random variables - the Distribution Garden** | reserved | Nine pages planned, `0100`-`0108`: a build hub, then the random variable as a function, PMF and histograms, PDF as brightness with rejection sampling, the CDF and the u-machine (inverse transform), normal splats and visible variance, joints and marginals at the canvas edges, walks and sums and the bell, then the gallery: compose, caption, share. |
| 3 | **Week 3: Maximum likelihood - three instruments** | reserved | Eight pages planned plus room for one consolidated problems page inside `0200`-`0299`: the method that found a hidden chamber, counting muons, sliding the hypothesis (the likelihood function), why the log, when algebra finds the peak, when only a computer will do (grid search then hand-coded ascent), how wrong can the answer be, where MLE breaks. Builds: muon tomography, the phone tracker, the zero-failure paradox. |
| 4 | **Week 4: Logistic regression - the test suite** | reserved | Eight pages planned plus room for one consolidated problems page inside `0300`-`0399`: a test suite for a classifier, logistic regression is maximum likelihood, the gradient derived then coded, the geometry of the boundary, separation and imbalance, correlated features and insufficient capacity, outliers label noise and six points, reading coefficients honestly. The artifact is the predict-then-run report, not the model. |
| 5 | **Week 5: Neural networks - the Glass Network** | reserved | Eight pages planned, `0400`-`0407`: the neuron you already met, why one line is not enough, stacking neurons into a network, open the hood (forward pass and activations), backpropagation slowly then yours, softmax as one distribution over many classes, temperature shaping a distribution, and the honest bridge from glass network to large model (overfitting islands ride inside the last page). The Sampling Bench grows across the softmax and temperature pages. |
| 6 | **Week 6: Probabilistic evaluation - the Audit Bench** | reserved | Nine pages planned, `0500`-`0508`: ninety-five percent sure and useless, one table six dials (confusion matrix and thresholds), two curves two questions (PR and ROC), do the probabilities mean anything (reliability and ECE), fixing the numbers without touching the model (temperature scaling), scores you cannot game (proper scoring rules), three definitions of fair one impossible, price the claim (bootstrap intervals, aleatoric vs epistemic), and the audit card itself. |
| 7 | **Capstone: Beyond PAI - the final project** | reserved | Block `0600`-`0699`, exact split decided by its worker. Planned content: the brief, the proposal menu with graded ambition, the rubric, publishing guidance, and the failure catalogue. The learner assembles their own six-week arc into one public artifact. |

## Reference sheets

Reference material reads alongside and holds no position in the sequence. None is planned
yet; if a week ships a cheat sheet it lives in `reference/` and is linked from the course
map's Reference module, following the house pattern.

## Adding a session to this course

1. Read `BUILDER-SPEC.md`, `.claude/skills/course-authoring/references/widgets.md` (the
   `.build` wrapper section in particular) and two neighbouring pages first.
2. Take free numbers inside your week's own block. Never renumber anything, never cross a
   block boundary without updating this file first.
3. Insert the new material at its true position in this file and in `index.html`.
4. Re-run `python3 scripts/gen_outline.py probability-you-build-course`, commit the
   regenerated `outline.js`, run `python3 scripts/validate_site.py`, and open the changed
   pages in both themes before opening the pull request.
