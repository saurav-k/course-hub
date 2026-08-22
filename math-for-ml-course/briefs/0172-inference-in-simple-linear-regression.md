# 0172 Inference in simple linear regression

| | |
|---|---|
| Module | M09 Estimation, testing, and inference |
| Rung | `pill hard` |
| Class | core |
| Word budget | 1,200 to 1,500 prose words, excluding practice and quiz text |
| Source scout | `mlm-stats-r9` S14 |

## One tight idea

A fitted slope is an estimate, so it has a standard error, an interval and a test, and everything from `0160` to `0167` applies to it unchanged.

## Prerequisites

`0164` for least squares as the Gaussian MLE, `0161` for bias, `0166` for the interval, `0167` for the test. M03 for least squares as a projection, which owns the geometry this page does not redraw. M05 for partial derivatives.

## Downstream

`0173` closes the module. M11's capstone reports a regression coefficient with an interval and assumes this page.

## Boundaries: what this page must not teach

- **Not multiple regression.** One predictor. Every extra one changes the degrees of freedom and opens collinearity, and neither belongs here.
- **Not least squares as linear algebra.** M03 owns the normal equations and the projection picture. Cross-link, do not re-derive.
- **Not model diagnostics as a checklist.** Residual plots get one figure and one sentence; a diagnostics page is a different page.
- **Not causal interpretation of a coefficient.** `0026` and `0169` own that boundary, and this page points at them rather than restating them.

## Beats, in order

1. Restate the model in one line and name every symbol: `Y_i = alpha + beta x_i + e_i` with the `x_i` fixed and the `e_i` independent `Normal(0, sigma^2)`.
2. **Least squares is the MLE here**, which is `0164`'s theorem with a line instead of a constant. One paragraph, because the reader has already met the argument.
3. `sigma_hat^2 = SSE/(n-2)`, and **why `n-2`**: two parameters were fitted to the same data, so two degrees of freedom are spent. It is `0022`'s `n-1` with one more parameter estimated, and saying so is what makes it a pattern rather than a rule.
4. **The slope's sampling distribution**, derived: `B ~ Normal(beta, sigma^2/S_xx)`. The proof is short and it pays off immediately.
5. Read `Var(B) = sigma^2/S_xx` as a design lever: spreading the `x` values out buys precision, and `S_xx` is the half of that expression under your control. This is the beat practitioners find most useful and it is usually omitted.
6. The `t` statistic, because `sigma` is unknown and is replaced by its estimate, with `n-2` degrees of freedom. Test `H0: beta = 0` once.
7. **The two intervals that are not the same.** For the mean response at `x0`, the width carries `sqrt(1/n + (x0 - xbar)^2/S_xx)`. For a single new observation it carries `sqrt(1 + 1/n + (x0 - xbar)^2/S_xx)`. The extra 1 is the new draw's own noise, and it is why a prediction interval never shrinks towards zero however much data you collect.
8. Both are widest far from `xbar`, which is the mathematics telling you not to extrapolate. Close there, with a row of the worked example sitting outside the observed range.

## Named theorems and their stated proofs (D4)

**Theorem 1 (the slope's sampling distribution).** `B ~ Normal(beta, sigma^2/S_xx)`, where `S_xx = sum_i (x_i - xbar)^2`.
**Proof.** `B` is linear in the responses: with `w_i = (x_i - xbar)/S_xx`, `B = sum_i w_i Y_i`, because `sum_i w_i = 0` makes the `ybar` term drop out. Then `E[B] = sum_i w_i (alpha + beta x_i) = alpha sum_i w_i + beta sum_i w_i x_i = beta`, using `sum_i w_i = 0` and `sum_i w_i x_i = 1`. By independence, `Var(B) = sum_i w_i^2 sigma^2 = sigma^2 sum_i (x_i - xbar)^2 / S_xx^2 = sigma^2/S_xx`. A linear combination of independent normals is normal. []

**Theorem 2 (the unbiased noise estimate).** `E[SSE/(n-2)] = sigma^2`, where `SSE = sum_i (Y_i - A - B x_i)^2`.
**Stated with its reason, and the distributional half taken on citation.** The full result is `SSE/sigma^2 ~ chi-square(n-2)` with `SSE` independent of `A` and `B`. The unbiasedness follows from the mean of that chi-square being `n-2`. The degrees-of-freedom count is the part the page derives: the residuals satisfy two linear constraints, `sum_i e_hat_i = 0` and `sum_i x_i e_hat_i = 0`, because those are exactly the two normal equations, so the `n` residuals live in an `(n-2)`-dimensional space. The chi-square distribution itself is quoted from the source and not proved here.

**The honest boundary.** Everything on this page rests on the noise being independent, equal-variance and normal. Normality buys the exact `t` distribution; without it the test is still approximately valid at large `n` by the same Central Limit Theorem the module has leaned on throughout. Independence and equal variance are the assumptions that fail silently and do real damage, and neither is checked by any number the page computes. One figure of residuals against fitted values, and one sentence saying that looking at it is not optional.

## Figures

- **Orientation**, `flowchart`: *the Gaussian MLE (`0164`), the interval (`0166`), the test (`0167`)* -> **THIS PAGE: the same machinery on a slope** -> *`0173`, M11's capstone* -> *(dotted) M03's projection*.
- **`svg.chart`**, required: the scatter with the fitted line and the confidence band for the mean response drawn around it, visibly narrowest at `xbar` and flaring outwards, with the prediction band drawn wider outside it. Kills: "the two intervals are the same thing", and shows the `(x0 - xbar)^2` term as a shape.
- **`svg.chart`**: the sampling distribution of the slope under `H0: beta = 0`, with the observed slope and the `t` critical values marked.
- **`svg.chart`**: `se(B)` against three `x`-ranges of the same width count, showing precision bought purely by spreading the design out.

## Worked example

`features.csv`, regressing `y` on `x01` alone. The predictors are mutually independent, so the simple slope still estimates `x01`'s true coefficient of 4.0 and the true intercept is 0. Recovered: slope `4.0586`, intercept `-0.0440`, `S_xx = 4047.21`, `se(B) = 0.0666`, `t = 60.94` against a critical value near 1.96, so reject overwhelmingly, and the 95 per cent interval for `beta` contains 4.0.

One thing the page must say rather than hide: `sigma_hat^2` comes out at about `17.95`, not the generator's `9.0`. That is correct. In a simple regression `sigma^2` is everything the model does not see, which here is the noise **plus** the four other real predictors, `9.0 + 2.5^2 + 1.5^2 + 1.0^2 + 0.6^2 = 18.86`. The reader can predict the number before computing it, which is the best possible demonstration of what the residual variance actually contains.

Then the contrast: regress `y` on `x20`, a predictor with true coefficient zero. Slope `-0.0574`, `se` `0.0926`, `t = -0.62`, fail to reject, correctly.

## Quiz seeds

1. **Misconception.** Why does the residual sum of squares get divided by `n-2`? Answer: two parameters were estimated from the same data. Distractors: two data points are dropped; the `t` distribution requires it, which reverses cause and effect.
2. **Mechanism.** The confidence band for the mean response is narrowest where? Answer: at the mean of the `x` values. Distractors: at the smallest `x`; uniformly along the line.

## Practice seed

**Stem.** Anscombe's set 1, with `S_xx = 110.0`, slope `0.500`, `n = 11` and `SSE = 13.76`. Compute `sigma_hat^2`, `se(B)`, the `t` statistic for `H0: beta = 0`, compare with `t(9, 0.975) = 2.262`, and give the 95 per cent interval for the slope.
**Hint.** `se(B) = sqrt(sigma_hat^2 / S_xx)`, and `sigma_hat^2` uses `n-2`, not `n-1`.
**Solution path.** `sigma_hat^2 = 13.76/9 = 1.529`; `se(B) = sqrt(1.529/110.0) = 0.1179`; `t = 0.500/0.1179 = 4.24`; `4.24 > 2.262` so reject; interval `0.500 +/- 2.262 x 0.1179 = [0.233, 0.767]`.
**`.p-check`.** Now run the identical arithmetic on Anscombe's set 4 and you get the same `t` from a dataset whose entire slope rests on one point at `x = 19`. The test cannot see that. Only the plot can, which is `0026`'s lesson arriving where it does the most damage.

## Code and dataset

`code/0172-inference-in-simple-linear-regression.py` against `datasets/features.csv`, already on main from #57. It prints the fit, the `n-2` demonstration across four divisors, the measured sampling distribution of the slope against its predicted standard deviation, the design-lever table, and both intervals at four `x0` including one outside the observed range. Reference it; do not rewrite it.

## Sources

- Ross, *A First Course in Probability*, and any standard regression text, for the chi-square distribution of `SSE/sigma^2` with `n-2` degrees of freedom, quoted here and not proved.
