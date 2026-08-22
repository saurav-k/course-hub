# 0164 MLE for the Gaussian, and why squared error was a likelihood all along

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill med` |
| Class | core |
| Word budget | 1,100 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S07 |

## One tight idea

Assume Gaussian noise and least squares is not a choice you made, it is a consequence you inherited.

## Prerequisites

`0162` for the recipe, `0163` for two worked cases, `0133` for the normal density, `0161` for bias. M05 for partial derivatives.

## Downstream

`0165` adds a prior to this exact objective and gets ridge. `0172` is this argument again with a line instead of a constant. M10's cross-entropy page consumes the Bernoulli half of the equivalence.

## Boundaries: what this page must not teach

- **One cross-link line to M10 and no more.** This module owns the equivalence "minimising cross-entropy is maximising likelihood" and derives it exactly once, here. M10 owns cross-entropy as an information quantity.
- **Not regression.** `0172` owns the line. This page fits a constant and a variance.
- **Not robust losses as a technique.** Name Huber in one sentence as what you reach for when the assumption fails, and stop.
- Do not present `n` against `n-1` as a convention. It is a consequence, and `0161` supplied the reason.

## Beats, in order

1. Write the Gaussian log-likelihood once, in full, with every symbol named on this page.
2. **The reveal, and it should land before the algebra finishes.** The only term containing `mu` is `sum_i (x_i - mu)^2`, and it carries a minus sign. Maximising the log-likelihood over `mu` *is* minimising the sum of squared errors. Nothing was added; the loss was already there.
3. Solve for `mu_hat`, which is `xbar`, and for `sigma_hat^2`, which divides by `n`.
4. **The variance MLE is biased**, and by exactly the amount `0161` predicts: `E[sigma_hat^2] = ((n-1)/n) sigma^2`. Maximum likelihood is consistent, not unbiased, and this is the second instance the reader has met.
5. Run the same move on a Bernoulli likelihood and land on binary log loss. Two losses, two distributional assumptions, one derivation.
6. **The trade-off, in the same section.** The assumption is doing the work. Squared error is optimal *given* Gaussian noise, which is why a heavy-tailed target gets a different loss. Tie back to `0024`'s kurtosis: the reader has already measured a tail that would break this.
7. Close on the reframe: a loss function is a statement about the noise you believe in, and choosing one is choosing that belief.

## Named theorems and their stated proofs (D4)

**Theorem 1 (Gaussian MLE).** For `x_1..x_n` from `Normal(mu, sigma^2)`, `mu_hat = xbar` and `sigma_hat^2 = (1/n) sum_i (x_i - xbar)^2`.
**Proof.** `l(mu, sigma^2) = -(n/2) log(2 pi sigma^2) - (1/(2 sigma^2)) sum_i (x_i - mu)^2`. Only the last term contains `mu`, and it enters negatively, so maximising over `mu` is minimising `sum_i (x_i - mu)^2`, which `0022`'s least-squares result puts at `xbar`. Substituting and differentiating in `sigma^2`, `dl/d(sigma^2) = -n/(2 sigma^2) + (1/(2 sigma^4)) sum_i (x_i - xbar)^2`, which vanishes at `sigma^2 = (1/n) sum_i (x_i - xbar)^2`. []

**Corollary (it is biased).** By Bessel's theorem from `0022`, the numerator has expectation `(n-1) sigma^2`, so `E[sigma_hat^2] = ((n-1)/n) sigma^2 < sigma^2` for every finite `n`, converging to `sigma^2` as `n` grows.

**Theorem 2 (Gaussian noise implies least squares).** If `y_i = a + b x_i + e_i` with `e_i` independent `Normal(0, sigma^2)`, the `(a, b)` maximising the likelihood are exactly those minimising `sum_i (y_i - a - b x_i)^2`.
**Proof.** The log-likelihood is `-(n/2) log(2 pi sigma^2) - (1/(2 sigma^2)) sum_i (y_i - a - b x_i)^2`, and `a` and `b` appear only in that final sum, preceded by a negative constant. Maximising in `(a, b)` is therefore minimising it. []

**The honest boundary.** The equivalence runs one way from an assumption. It says squared error is what Gaussian noise implies; it does not say Gaussian noise is what your data has. When it does not, the loss is still computable and no longer optimal, and nothing in the arithmetic will warn you. `0163` already showed a fitted model that was wrong and silent about it.

## Figures

- **Orientation**, `flowchart`: *the recipe (`0162`), the normal density (`0133`)* -> **THIS PAGE: the loss you already use was a likelihood** -> *`0165` add a prior, `0172` fit a line* -> *(dotted) M10 cross-entropy*.
- **`svg.chart`**, required: a scatter with a candidate line, every residual drawn as a vertical segment, and beside it those residuals collected into a Gaussian density. Kills: squared error as an arbitrary convention.
- **`svg.chart`**: the sum of squared errors and the log-likelihood plotted against a candidate parameter on twinned axes, one minimised and one maximised at the same place.
- **`svg.chart`**: `E[sigma_hat^2]` against `n` for both divisors with the true `sigma^2` as a reference, the `n` curve approaching from below.

## Worked example

`features.csv`, whose true coefficients and noise level are stated in its generator. Take the residuals against the true coefficients, which are exactly the generated `Normal(0, 3.0)` noise, and recover `mu_hat` near zero and `sigma_hat^2` near 9. Then the bias table at `n = 3, 5, 20, 100` against the predicted `((n-1)/n) sigma^2`. Then regress `y` on `x01` and tabulate the sum of squared errors and the log-likelihood at five candidate slopes, both extremal at the same value. Close on the Bernoulli half using `sessions.csv`'s `returning` column, showing the mean negative log-likelihood and binary log loss print the identical number.

## Quiz seeds

1. **Misconception.** Under a Gaussian noise model, minimising the sum of squared errors is equivalent to what? Answer: maximising the log-likelihood. Distractors must include "minimising the model's variance", which confuses the noise parameter with the loss.
2. **Mechanism.** Your regression target has heavy tails. What does that break? Answer: the Gaussian noise assumption. Distractors: the chain rule in the gradient; the independence of the samples. Feedback notes independence can hold perfectly well alongside heavy tails.

## Practice seed

**Stem.** Four residuals from a fitted model, with the mean already fitted at zero: `-2.0, 1.0, 0.5, -1.5`. Write the Gaussian log-likelihood as a function of `sigma^2`, differentiate, solve, and compare with the `n-1` version.
**Hint.** With the mean fixed at zero the sum of squares is just the sum of the squared residuals.
**Solution path.** Sum of squares `4.00 + 1.00 + 0.25 + 2.25 = 7.50`; `l(sigma^2) = -(4/2) log(2 pi sigma^2) - 7.50/(2 sigma^2)`; the derivative vanishes at `sigma_hat^2 = 7.50/4 = 1.875`; the `n-1` version gives `2.500`.
**`.p-check`.** The MLE must be the smaller of the two, always, because it divides the same sum by the larger number. If yours is larger, the divisors were swapped.

## Code and dataset

`code/0164-mle-for-the-gaussian.py` against `datasets/features.csv` and `datasets/sessions.csv`, already on main from #57. Reference it; do not rewrite it.

## Sources

- Hastie, Tibshirani and Friedman, *ESL* 2nd edition, section 8.2.2, for maximum likelihood and its relation to least squares.
