# 0161 Bias, variance, and the MSE that reconciles them

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill med` |
| Class | core |
| Word budget | 1,000 to 1,300 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S04 |

## One tight idea

An estimator can be wrong on average, wrong by a lot each time, or both, and mean squared error is the one number that trades the two against each other.

## Prerequisites

`0160` for the sampling distribution. M08 for expectation and variance as operators.

## Downstream

`0164` needs it to say the Gaussian variance MLE is biased. `0165` needs it to say what a prior buys. `0170` is this identity applied to a predictor instead of a parameter, and says so explicitly.

## Boundaries: what this page must not teach

- **This page is about estimating a parameter.** `0170` is about predicting an outcome. The two decompositions look alike for a reason and the reader must not conflate them. Say the difference in one sentence here and again on `0170`.
- **Not regularization.** `0165` and M06 own it. This page shows shrinkage on a single number so the idea arrives without a model attached.
- Not efficiency or the Cramer-Rao bound. Name that a best-possible variance exists and stop.

## Beats, in order

1. Four dartboards before any algebra: low and high bias against low and high variance. The reader should be able to name the four cases before meeting a formula.
2. Bias defined, `E[theta_hat] - theta`, in words first: where the cloud of estimates is centred relative to the truth.
3. Variance defined: how wide the cloud is. Note that neither definition mentions your one estimate, which is the point.
4. **The decomposition**, derived in three lines, with the cross term shown to vanish rather than asserted to.
5. Read the identity as a menu: four estimators of the same quantity, tabulated, and the observation that neither bias nor variance alone ranks them.
6. **Unbiased is not the goal.** A shrinkage sweep on a single parameter, where the deliberately biased estimator wins on MSE by a factor of two. This is the beat the page exists for.
7. Consistency, defined and distinguished: an estimator can be biased and consistent, which is the ordinary case, and unbiased and inconsistent, which is a warning.
8. One line forward to `0165`: the shrinkage knob here becomes a prior there, and to `0170`: the same trade governs model complexity.

## Named theorem and its stated proof (D4)

**Theorem.** For an estimator `theta_hat` of a fixed parameter `theta`, `MSE(theta_hat) = Bias(theta_hat)^2 + Var(theta_hat)`.

**Proof.** Let `m = E[theta_hat]` and split the error at `m`: `theta_hat - theta = (theta_hat - m) + (m - theta)`. Square and take expectations. The cross term is `2(m - theta) E[theta_hat - m]`, and `E[theta_hat - m] = 0` by the definition of `m`, while `(m - theta)` is a constant, so the cross term is zero. What remains is `E[(theta_hat - m)^2] + (m - theta)^2`, which is the variance plus the squared bias. []

**The honest boundary.** The identity is exact and assumes nothing beyond the existence of the second moment. What it does not do is tell you which term to prefer: that is a decision about the cost of being wrong, and MSE encodes one particular answer, namely that errors cost quadratically. A different loss gives a different trade, and a page that treats MSE as the definition of "good" has smuggled that assumption in.

## Figures

- **Orientation**, `flowchart`: *the sampling distribution (`0160`)* -> **THIS PAGE: two ways to be wrong, and their sum** -> *`0164` biased MLEs, `0165` priors, `0170` the tradeoff*.
- **`svg.chart`**, required: the four-panel dartboard, four scatter clusters against a common bullseye, each panel labelled with its bias and variance.
- **`svg.chart`**: the shrinkage sweep. `bias^2`, `variance` and their sum plotted against the shrinkage weight `w`, the total dipping visibly below its value at `w = 0`. Kills: "unbiased means best".
- **`stateDiagram-v2`** or a small `flowchart`: biased/unbiased crossed with consistent/inconsistent, with an example named in each cell.

## Worked example

`sessions.csv`, `session_seconds` as the population so `mu` is known. Samples of `n = 12`, 60,000 repeats, four estimators tabulated: the sample mean, the sample median, the first observation alone, and the constant 12. Print bias, `bias^2`, variance, their sum, and the separately measured MSE, so the identity is visible row by row rather than claimed. Then the shrinkage sweep `est = (1-w) xbar + w g` towards a fixed guess, where the minimum sits at `w = 0.5` at about 0.46 times the unbiased estimator's MSE.

## Quiz seeds

1. **Misconception.** An estimator is unbiased. What does that guarantee about your one estimate? Answer: nothing at all about this one. Distractors must include "it is the best available estimate", which shrinkage disproves on the same page.
2. **Mechanism.** Which term does collecting more data usually shrink? Answer: the variance term only. Feedback notes that a biased MLE's bias can also shrink with `n`, which is consistency and a different property.

## Practice seed

**Stem.** Five draws from a normal population: `3.1, 4.5, 2.8, 5.2, 3.9`. Compute the MLE variance (divide by 5) and the sample variance (divide by 4). The true `sigma^2` is 4. Which is unbiased, and what is the expected value of the other?
**Hint.** Compute the squared deviations once and divide the same sum two ways.
**Solution path.** `xbar = 3.9`; squared deviations `0.64, 0.36, 1.21, 1.69, 0.00` summing to `3.90`; MLE variance `0.780`, sample variance `0.975`; the sample variance is unbiased and `E[MLE] = (n-1)/n x 4 = 3.2`.
**`.p-check`.** Both numbers here land far below 4 on this particular sample, which is the page's own quiz arriving as an experience: unbiasedness is a statement about the average over repeats and says nothing about the draw in front of you.

## Code and dataset

`code/0161-bias-variance-and-the-mse.py` against `datasets/sessions.csv`, already on main from #57. It prints the four-estimator table with `bias^2 + variance` beside the measured MSE, then the shrinkage sweep with the winning `w` and its ratio. Reference it; do not rewrite it.

## Sources

- Wasserman, *All of Statistics*, section 6.3, for bias, variance and the MSE decomposition.
