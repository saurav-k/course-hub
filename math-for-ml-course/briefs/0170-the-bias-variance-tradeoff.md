# 0170 The bias-variance tradeoff

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill hard` |
| Class | core |
| Word budget | 1,100 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S15 |

## One tight idea

Expected test error splits into three separate things, and model complexity can move only two of them.

## Prerequisites

`0161` for the identity applied to a parameter. M08 for expectation and variance. `0165` for regularization as a prior, which this page meets again as a position on a curve.

## Downstream

`0171` measures this curve with cross-validation and inherits its vocabulary.

## Boundaries: what this page must not teach

- **Not `0161` again.** That page estimated a parameter. This one predicts an outcome, and the extra term is the noise in the outcome itself. Say the difference explicitly in the first section; a reader who conflates them will misread every later figure.
- **Not the L1/L2 geometry.** M06's `0110` owns it.
- **Not cross-validation.** `0171` owns it.
- **Do not resolve double descent.** Name it, cite it, say it is an active area, stop.

## Beats, in order

1. Restate `0161`'s identity, then add the term it did not have: the target itself is noisy, and no model can remove that.
2. **The decomposition**, derived, with the cross term shown to vanish because the noise is independent of the training set.
3. Read the three terms as three different complaints: the model is systematically wrong, the model wobbles with the training set, and the world is noisy.
4. **The k-nearest-neighbour instance**, which is the cleanest concrete case in the subject: the variance term is exactly `sigma^2/k` and the bias term is the gap between `f(x0)` and the average of `f` over a widening neighbourhood. One knob, two terms, opposite directions.
5. The U-curve, drawn and then measured: bias falling, variance rising, total dipping.
6. **How much of the error was never yours.** At the optimum, report the irreducible share as a percentage. On the page's own data it is over 95 per cent, and that number changes how a reader thinks about a leaderboard.
7. Regularization arriving from the other side: the same knob `0165` described as a belief about the weights is a position on this curve.
8. **The honest limit**, in a `.callout.warn`: past the interpolation threshold test error can fall again. The classical U-curve describes the under-parameterised regime and not modern over-parameterised models.

## Named theorem and its stated proof (D4)

**Theorem (bias-variance decomposition of prediction error).** Suppose `Y = f(X) + e` with `E[e] = 0` and `Var(e) = sigma_e^2`, and let `f_hat` be fitted on a random training set. At a fixed input `x0`, under squared-error loss,

  `Err(x0) = E[(Y - f_hat(x0))^2 | X = x0] = sigma_e^2 + (E[f_hat(x0)] - f(x0))^2 + E[(f_hat(x0) - E[f_hat(x0)])^2]`.

**Proof.** Write `Y - f_hat(x0) = e + (f(x0) - f_hat(x0))`. Square and take expectations. The cross term is `2 E[e] E[f(x0) - f_hat(x0)]`, which is zero because `e` has mean zero and is independent of the training set that produced `f_hat`. So `Err(x0) = E[e^2] + E[(f(x0) - f_hat(x0))^2] = sigma_e^2 + E[(f(x0) - f_hat(x0))^2]`. Applying `0161`'s identity to `f_hat(x0)` as an estimator of the number `f(x0)` splits the second term into squared bias plus variance. []

This is equation 7.9 of Hastie, Tibshirani and Friedman.

**Corollary (the k-NN form).** `Err(x0) = sigma_e^2 + [ f(x0) - (1/k) sum_{l=1..k} f(x_(l)) ]^2 + sigma_e^2/k`, with the training inputs treated as fixed so the randomness is in the responses.

**The honest boundary.** The decomposition is exact and it is tied to squared-error loss. Under 0-1 loss the analogous split is not additive in the same way, and the literature carries several competing definitions. Say that, so a reader does not carry the identity into a classification setting expecting it to hold verbatim.

## Figures

- **Orientation**, `flowchart`: *the MSE identity (`0161`)* -> **THIS PAGE: three terms, and complexity moves two** -> *`0171` measuring the curve* -> *(dotted) M06's regularization*.
- **`svg.chart`**, required: the U-curve. `bias^2` falling, variance rising, total as their sum with the minimum marked, against model complexity, and the irreducible error drawn as a floor the total never crosses.
- **`svg.chart`**: the k-NN instance tabulated, `sigma^2/k` against `k` beside a bias term that grows, so the tradeoff is quantitative rather than a shape.
- **`svg.chart`**: the double-descent curve. The classical U, the interpolation threshold marked, then error falling again. Labelled as the honest limit, not as the page's claim.

## Worked example

`features.csv`, whose true coefficients are known, so bias is **measured** and not estimated. Fit on fresh 80-row training sets, 3,000 times, at complexities from 1 to 70 predictors, and tabulate `E[f_hat(x0)]`, bias, `bias^2`, variance and the total at each. The bias column collapses once the model is allowed the five real predictors; the variance column climbs the whole way because every extra column is another coefficient estimated from the same 80 rows. At the optimum, over 95 per cent of the remaining error is irreducible. Then the same U from the other direction: all thirty predictors with a ridge penalty swept, bias rising and variance falling.

## Quiz seeds

1. **Misconception.** Which term can no model reduce? Answer: the irreducible noise. Distractors: the squared bias; the variance of the fit; "the model complexity term", which is not a term at all.
2. **Mechanism.** In k-NN you increase `k`. What happens? Answer: bias rises, variance falls. Distractors: both fall, which is what you would want and is why the tradeoff has a name; and the reverse, which describes decreasing `k`.

## Practice seed

**Stem.** Take `sigma^2 = 1` and the k-NN decomposition `Err = sigma^2 + bias^2 + sigma^2/k`, and suppose the bias term grows as `0.002k`. Tabulate the three terms and the total at `k = 1, 5, 20, 50`. Which `k` minimises the total, and how much of the error there could any model have removed?
**Hint.** Only two of the three terms depend on `k`.
**Solution path.** Variance terms `1.000, 0.200, 0.050, 0.020`; bias terms `0.002, 0.010, 0.040, 0.100`; totals with the irreducible 1.0 added `2.002, 1.210, 1.090, 1.120`. The minimum is at `k = 20` with total `1.090`, of which `1.000` was never removable, so the model's own contribution is `0.090`.
**`.p-check`.** The total must never fall below 1.000 at any `k`. If yours does, the irreducible term was left out, and the page's central point went with it.

## Code and dataset

`code/0170-the-bias-variance-tradeoff.py` against `datasets/features.csv`, already on main from #57. Reference it; do not rewrite it.

## Sources

- Hastie, Tibshirani and Friedman, *ESL* 2nd edition, equation 7.9 and section 7.3, page 223, for the decomposition and the k-NN form.
- Belkin, Hsu, Ma and Mandal (2019), *PNAS*, "Reconciling modern machine-learning practice and the classical bias-variance trade-off", for double descent as the stated limit.
