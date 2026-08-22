# 0163 MLE for the Bernoulli, the Poisson and the Uniform

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill med` |
| Class | core |
| Word budget | 1,100 to 1,400 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S05 and S06 |

## One tight idea

The recipe generalises, but "set the derivative to zero" is a step inside it and not the recipe itself.

## Prerequisites

`0162` for the recipe. `0129` for the Bernoulli, `0132` for the Poisson, `0130` for the uniform. M05 for differentiation.

## Downstream

`0164` does the two-parameter case. `0165` adds a prior to exactly these objectives. `0169` uses the Bernoulli result as the estimator every conversion rate is.

## Boundaries: what this page must not teach

- **Not the Gaussian.** `0164` owns it, because it is two parameters and it carries the loss-function payoff.
- **Not MAP.** No priors anywhere on this page.
- Not the general theory of boundary maxima. The uniform is shown as a concrete case, not as an instance of a KKT condition; M06 owns constrained optimisation.
- Do not claim MLEs are unbiased. This page is where that belief is killed, so it must not be reinforced earlier in it.

## Beats, in order

1. Bernoulli first, worked end to end, because the reader has already seen its likelihood curve on `0162` and now gets the algebra under it.
2. Poisson second, same three steps, and one extra move worth naming: the `log(x_i!)` term has no `lambda` in it, so it drops out of the derivative and never needs computing.
3. **The Poisson fit that fails**, which is the most useful thing on the page. Fit `lambda` to a real count column, get a number, and then check the model: a Poisson has variance equal to its mean, and this column's ratio is about 194. Maximum likelihood returned an answer whether or not the model was right.
4. The uniform third, and here the recipe visibly breaks: the likelihood `theta^-n` is decreasing wherever it is positive, so there is no stationary point and the maximum sits on a wall.
5. **The MLE is biased**, proved, with the size of the bias given exactly and the debiasing factor derived from it.
6. Tie back to `0161`: here is an estimator that is biased and consistent, which is the ordinary case rather than a curiosity.
7. Close on the reading habit: three distributions, one recipe, and two different ways the last step can go.

## Named theorems and their stated proofs (D4)

**Theorem 1 (Bernoulli).** For `x_1..x_n` in `{0,1}`, the MLE of `p` is `k/n` where `k = sum_i x_i`.
**Proof.** `L(p) = p^k (1-p)^(n-k)`, so `l(p) = k log p + (n-k) log(1-p)` and `l'(p) = k/p - (n-k)/(1-p)`. Setting this to zero gives `k(1-p) = (n-k)p`, hence `k = np` and `p = k/n`. Since `l''(p) = -k/p^2 - (n-k)/(1-p)^2 < 0` throughout `(0,1)`, `l` is strictly concave and the stationary point is the unique maximum. []

**Theorem 2 (Poisson).** For counts `x_1..x_n`, the MLE of `lambda` is `xbar`.
**Proof.** `l(lambda) = -n lambda + (sum_i x_i) log lambda - sum_i log(x_i!)`. The last term is free of `lambda`, so `l'(lambda) = -n + (sum_i x_i)/lambda`, which vanishes at `lambda = xbar`, and `l''(lambda) = -(sum_i x_i)/lambda^2 < 0`. []

**Theorem 3 (Uniform on `[0, theta]`).** The MLE is `max_i x_i`, and there is no stationary point.
**Proof.** `L(theta) = theta^(-n)` when `theta >= max_i x_i` and `0` otherwise, because any smaller `theta` assigns density zero to the largest observation. Where it is positive `L` is strictly decreasing in `theta`, so it is maximised at the smallest admissible value, `max_i x_i`. []

**Theorem 4 (and that MLE is biased).** `E[max_i X_i] = n theta/(n+1)`.
**Proof.** Let `M = max_i X_i`. For `0 <= t <= theta`, `P(M <= t) = (t/theta)^n` by independence, so `M` has density `n t^(n-1)/theta^n`. Then `E[M] = int_0^theta t . n t^(n-1)/theta^n dt = (n/theta^n) . theta^(n+1)/(n+1) = n theta/(n+1)`. The bias is `-theta/(n+1)`, negative for every finite `n`, and multiplying by `(n+1)/n` removes it exactly. []

**The honest boundary.** Theorem 4's bias is not a defect of maximum likelihood; it is a consequence of estimating a boundary from inside it. Every observation is at most `theta`, so their maximum is too. The debiased estimator is unbiased and can return a value larger than any observation, which is uncomfortable and correct.

## Figures

- **Orientation**, `flowchart`: *the recipe (`0162`)* -> **THIS PAGE: three distributions, and where the recipe bends** -> *`0164` two parameters, `0169` conversion rates*.
- **`svg.chart`**, required: `L(theta) = theta^-n` plotted with the hard vertical wall at `max(x_i)`, zero to its left and strictly decreasing to its right. Kills: "every maximum is a stationary point".
- **`svg.chart`**: the sampling distribution of `max_i X_i` for a known `theta`, sitting entirely to the left of it, with `E[max]` and `theta` both marked. Kills: "the MLE is unbiased".
- **`svg.chart`**: variance against mean for the count column, with the Poisson's `variance = mean` line drawn and the data far above it. Kills: fitting a model and never checking it.

## Worked example

`sessions.csv`. Bernoulli on `returning`: `k = 8,238` of `20,000`, so `p_hat = 0.4119`, with the log-likelihood tabulated either side of the peak. Poisson on `pages_viewed`: `lambda_hat = xbar = 5.8209`, then the check that kills it, variance `1,130.15` against mean `5.82`, a ratio of `194.2`, caused by the bots. Uniform on `screen_brightness`, which is genuinely `Uniform(0, 100)`: at the full 20,000 rows the bias `theta/(n+1)` is below the column's rounding, so subsample to `n = 2, 6, 20, 100` and watch `E[max]` track `n theta/(n+1)` while the debiased estimator sits on 100.

## Quiz seeds

1. **Misconception.** `theta_hat = max(x_i)` for `Uniform(0, theta)`. What kind of error does it make? Answer: it always underestimates. Distractors must include "it is unbiased for all n", with feedback giving `E[max] = n theta/(n+1)`.
2. **Mechanism.** Why does the derivative method fail for the uniform? Answer: the maximum sits at a boundary. Distractors: the likelihood is not continuous; the log-likelihood is undefined. Both are false and the feedback says why.

## Practice seed

**Stem.** Six draws from `Uniform(0, theta)`: `4.2, 8.6, 1.1, 7.3, 5.9, 2.8`. State the MLE. If the true `theta` were 10, compute `E[theta_hat]`, the bias, and an unbiased estimator evaluated on this sample.
**Hint.** The MLE needs no calculus. For the expectation use `E[max] = n theta/(n+1)`.
**Solution path.** `theta_hat = 8.6`; `E[max] = 6 x 10/7 = 8.571`; bias `-1.429`, which is `-theta/(n+1)`; debiased `(7/6) x 8.6 = 10.033`.
**`.p-check`.** The debiased estimate exceeds every observation in the sample. That is correct and is the point: the largest value you saw is evidence that `theta` is at least that big, and on average it is bigger.

## Code and dataset

`code/0163-mle-for-bernoulli-poisson-and-uniform.py` against `datasets/sessions.csv`, already on main from #57. It carries all three derivations as tables, the overdispersion check, and the `E[max]` simulation against the theorem. Reference it; do not rewrite it.

## Sources

- Hastie, Tibshirani and Friedman, *ESL* 2nd edition, section 8.2.2, for the maximum likelihood framework.
