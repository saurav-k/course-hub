# M06 L11 - Regularization is a constraint you can draw

**Page `lessons/0130-regularization-is-a-constraint-you-can-draw.html`** &middot; module M06, lesson 11 of 12 &middot; program `code/0130-regularization-is-a-constraint-you-can-draw.py` &middot; dataset `datasets/m06-credit.csv`

## The single tight idea

Adding a norm penalty to the loss is the same problem as forbidding the weights from leaving a ball, and the *shape* of that ball is the entire difference between ridge and lasso.

## Prerequisites

| Needs | From |
|---|---|
| KKT, which makes the equivalence a statement rather than an analogy | M06 L10 |
| **Norms, and the unit ball of each norm as a picture** | M03 (r1 edge 5: M03 owns the ball, M06 owns the corner) |
| **The eigen-decomposition of a symmetric matrix** | M04 |
| The Hessian of the objective | M05, and M06 L04 where it was measured |

**Boundary, held explicitly (r1 edge 24).** **M06 owns the geometry**: the balls, the corner, why L1 is sparse. **M09 owns the statistics**: regularization as a bias-variance trade, and L2 as a Gaussian prior under MAP. **One cross-link line to M09, no derivation.** Neither module redraws the other's picture.

**Watch the word ceiling.** Two mechanisms, two figures and an equivalence. The r6 report flagged this page with L07 as the likeliest to split. If the draft passes 1,800 prose words, split at the geometry/algebra boundary.

## Beats, in order

1. **The penalty form**, which the reader already met on L01.
2. **The constraint form, and the equivalence**, proved below.
3. **The caveat that keeps it honest.** You do not know which radius `k` your coefficient `alpha` corresponds to, because the relationship depends on the form of the loss. You control it in direction only: larger `alpha`, smaller region.
4. **The classic figure.** Elliptical loss contours growing outward from the unconstrained optimum until they touch the constraint region: a circle for L2, a diamond for L1. The diamond's corners sit on the axes. A growing ellipse touches a corner before it touches a flat face, and a corner is a coefficient that is exactly zero. **This figure is the reason the page exists.**
5. **The algebra under the picture**, so it is not just a picture. L2 rescales; L1 thresholds. Both proved below.
6. **Why L1 and not L0**, in Tibshirani's own words: `q = 1` is "the smallest value of `q` (i.e. closest to subset selection) that yields a convex problem". L02 is why that sentence is the whole answer.
7. **One line to M09** for the MAP reading, and no more.
8. **Trade-offs.** L1 gives a sparse answer and an unstable one: among correlated predictors it picks one more or less arbitrarily, which `m06-credit.csv` is built to demonstrate. And a `.callout.warn`: once the optimizer is adaptive, an L2 term in the loss is no longer weight decay, so this page's equivalence is stated for gradient descent and must not be carried to Adam.

## Named theorems and their stated proofs (D4)

**Result 1 (penalty and constraint are the same problem).**
Consider `min_theta J(theta) subject to Omega(theta) <= k`. Its generalized Lagrangian is `L(theta, alpha) = J(theta) + alpha*(Omega(theta) - k)` with `alpha >= 0`, and the constrained solution is `theta* = argmin_theta max_{alpha >= 0} L(theta, alpha)`.
Fix `alpha` at its optimal value `alpha*` and view the problem as a function of `theta` alone:
`theta* = argmin_theta L(theta, alpha*) = argmin_theta J(theta) + alpha* * Omega(theta) - alpha* * k`.
The term `alpha* * k` does not depend on `theta`, so dropping it changes no minimiser:
`theta* = argmin_theta J(theta) + alpha* * Omega(theta)`.
**That is exactly the penalised problem.** **QED**
So a norm penalty *is* a constraint on the weights: if `Omega` is the L2 norm the weights are confined to an L2 ball, and if it is the L1 norm, to a region of limited L1 norm.
**The caveat is part of the result, not a footnote:** you do not know `k` from `alpha*`, because "the relationship between `k` and `alpha*` depends on the form of `J`". All you know is the direction.

**Result 2 (L2 rescales in the Hessian eigenbasis, and never zeroes).**
Take a quadratic approximation to `J` around its unregularised minimiser `w*`, with Hessian `H`. The regularised objective's stationarity condition is `alpha*w~ + H*(w~ - w*) = 0`, so `(H + alpha*I)*w~ = H*w*`, so `w~ = (H + alpha*I)^-1 * H * w*`.
`H` is real symmetric, so write `H = Q*Lambda*Q'` with `Q` orthonormal. Then
`w~ = (Q*Lambda*Q' + alpha*I)^-1 * Q*Lambda*Q' * w* = Q*(Lambda + alpha*I)^-1*Lambda*Q'*w*`,
using `alpha*I = Q*(alpha*I)*Q'` and `Q'Q = I`.
So in the eigenbasis, the component of `w*` along the `i`-th eigenvector is multiplied by **`lambda_i/(lambda_i + alpha)`**. **QED**
Read it: where `lambda_i >> alpha` the factor is near 1 and regularization barely touches that direction. Where `lambda_i << alpha` the factor is near 0 and the component is nearly erased. And **for any finite `alpha` and any `lambda_i > 0` the factor is strictly positive**, so L2 shrinks and never zeroes. That last clause is the whole contrast with Result 3.

**Result 3 (L1 soft-thresholds, and zeroes exactly).**
Under the same quadratic approximation, and assuming `H` is diagonal - which holds when the features have been decorrelated, and the page must state that assumption - the regularised objective separates across coordinates:
`J~(w) = J(w*) + sum_i [ 0.5*H_ii*(w_i - w*_i)^2 + alpha*|w_i| ]`.
Minimise one coordinate. For `w_i > 0` the derivative is `H_ii*(w_i - w*_i) + alpha`, zero at `w_i = w*_i - alpha/H_ii`, which is a valid positive solution only when `w*_i > alpha/H_ii`. For `w_i < 0` the mirror argument gives `w_i = w*_i + alpha/H_ii`, valid only when `w*_i < -alpha/H_ii`. In between, the subgradient of `alpha*|w_i|` at zero is the whole interval `[-alpha, alpha]`, and the stationarity condition `H_ii*(0 - w*_i) + alpha*s = 0` has a solution with `s` in `[-1, 1]` precisely when `|w*_i| <= alpha/H_ii`.
Collecting the three cases:
**`w_i = sign(w*_i) * max(|w*_i| - alpha/H_ii, 0)`.** **QED**
This is the soft-thresholding operator, and it appears independently as `S(z, gamma) = sign(z)*(|z| - gamma)_+` in the glmnet paper. Below the threshold the answer is **exactly** zero, not small.

## Planned figures

1. **Orientation, `flowchart`.** "L01 a penalty term in the objective" and "L10 a constraint and its multiplier" both into "THIS PAGE - they are the same problem, and the ball's shape decides sparsity", into "L12 early stopping, the constraint you never wrote".
2. **`svg.chart`, the classic figure, two panels on one scale.** Left: elliptical contours in `ink` growing from the least-squares solution in `m-gold` until they touch a circle in `f-prob`, meeting on a flat arc so both coefficients stay non-zero. Right: the same ellipses touching a diamond at the corner on the vertical axis, so the horizontal coefficient is exactly zero. Kills "L1 gives sparsity" as an assertion: the corner is the reason and it is visible.
3. **`svg.chart`.** Output coefficient against input `w*`: L2's `lambda/(lambda+alpha)*w*` as a straight line through the origin with reduced slope in `s-sky`, L1's soft threshold as a flat zero segment then a parallel line offset by `alpha/H` in `s-signal`. Kills "L1 and L2 differ in strength": they differ in shape, and the flat segment is where zeros come from.
4. **`svg.chart`, a regularization path.** Coefficient against `log(alpha)` for the twelve features of `m06-credit.csv`: L1 in one panel with the four noise coefficients hitting exactly zero first, L2 in the other with all twelve decaying and none arriving.

## The worked example, in eight parts

What ridge and lasso do to the same coefficients. **Both formulas quoted, the table derived.**

1. Four coefficients from the quadratic approximation: `w* = (3.0, 0.4, -0.2, -2.0)`, with Hessian diagonal `H = (1.0, 1.0, 1.0, 0.5)`, at `alpha = 0.5`.
2. L1 thresholds are `alpha/H_ii = (0.5, 0.5, 0.5, 1.0)`.
3. L1 results: `(2.5, 0, 0, -1.0)`.
4. L2 results, `H_ii*w*/(H_ii + alpha)`: `(2.0, 0.267, -0.133, -1.0)`.
5. Rows two and three are the whole point: L1 sends small coefficients to exactly zero, L2 to small non-zero values. **Sparsity is a fact about the arithmetic, not a tendency.**
6. Compare rows one and three of the *original* list - same `w* = 3.0`, different curvature. Where the data pins a direction down, `H_ii` is large, the threshold is small, and both penalties barely move it. **Regularization spends its budget on the directions the data does not constrain**, which is the same statement `lambda/(lambda + alpha)` makes.
7. Row four is a coincidence worth pointing at: both methods return `-1.0`. Ask the reader to say why from the two formulas, and answer it in the practice problem.
8. **Then the tie to the picture: the zeros in the L1 column are the corners of the diamond, arrived at by algebra instead of by eye.**

## Quiz seeds

**Q1 (misconception).** Why does L1 produce exact zeros and L2 does not?
Correct: the L1 ball has corners on the axes and L2's does not. Distractors: L1 uses a larger coefficient (false at any matched strength); **"L1 is not differentiable, so the solver rounds down"** - the near-miss worth naming, because non-differentiability at zero is real and related, but it is a consequence of the corner rather than the cause of the sparsity; L1 is applied after fitting (false for both).

**Q2.** L2 rescales the coefficient along a Hessian eigendirection by `lambda/(lambda + alpha)`, so stiff directions barely move.
Distractors: `alpha/(lambda + alpha)` (inverted); `1 - alpha` in every direction (what "shrinkage" sounds like, and wrong because L2 is anisotropic - the whole point); **`max(lambda - alpha, 0)`** - which has the shape of L1's soft threshold, so a reader who picks it has confused the two mechanisms this page separates.

## Practice seed

**Stem.** Coefficients `w* = (3.0, 0.4, -0.2, -2.0)` with Hessian diagonal `H = (1.0, 1.0, 1.0, 0.5)`. At `alpha = 0.5`, compute the L1 and L2 results for each. Then find the smallest `alpha` that zeroes exactly three of them, and explain the fourth row's coincidence.
**Hint.** For the second part, do not search. Each coefficient has its own threshold, and you can write it down directly from the L1 formula - so the question is really "sort four numbers and read off the third".
**Solution.** At `alpha = 0.5`: L1 gives `(2.5, 0, 0, -1.0)`, L2 gives `(2.0, 0.267, -0.133, -1.0)`. A coefficient is zeroed once `alpha >= |w*| * H_ii`, so the four thresholds are `3.0, 0.4, 0.2, 1.0`. Sorted: `0.2, 0.4, 1.0, 3.0`. Three are zeroed once `alpha` passes `1.0`. The fourth row's coincidence: at `alpha = 0.5` and `H = 0.5`, L1 gives `-(2.0 - 1.0) = -1.0` and L2 gives `0.5*(-2.0)/1.0 = -1.0`. The two agree only because `alpha/H_ii` happens to equal `|w*| * alpha/(H_ii + alpha)` at these numbers; it is arithmetic, not a rule.
**`.p-check`.** Your L2 column must contain **no zeros at any `alpha` you try**. If one appears, you have applied the L1 formula twice.

## Code and dataset

**Program:** `code/m06-11-regularization.py`. **Dataset:** `datasets/m06-credit.csv`, standardised, with `credit_limit_inr` as the continuous target so the least-squares geometry is exact.
**What it computes twice:** the full lasso regularization path, once by coordinate descent using the soft-thresholding operator derived above, and once by a general-purpose subgradient method run to tight tolerance. The two paths must agree, and the coordinate-descent one is what `glmnet` actually does. The program prints, for each `alpha` on the path, how many coefficients are exactly zero under L1 and under L2 - the L2 count must be **zero at every `alpha`**, which is Result 2 made into a test rather than a claim. A third block demonstrates the correlated-predictor instability: refitting the lasso on bootstrap resamples and reporting how often it selects `utilisation_ratio` against `emi_to_income`, two columns correlated at 0.92 by construction.

## Sources, primary only

- Goodfellow, Bengio & Courville, ch. 7: eq 7.13 for the L2 rescaling, eqs 7.19 to 7.23 for the L1 subgradient and soft threshold, eqs 7.25 to 7.28 and the paragraph after for the constraint equivalence and its caveat.
- Friedman, Hastie & Tibshirani, *Regularization Paths for Generalized Linear Models via Coordinate Descent*, J. Stat. Soft. 33(1) 2010, eq 6, for the soft-thresholding operator and the coordinate-descent algorithm.
- Tibshirani, *Regression shrinkage and selection via the lasso: a retrospective*, JRSS-B 73(3) 2011, section 1, for the convexity argument in his own words.
- Loshchilov & Hutter, arXiv:1711.05101v3, for the `.callout.warn`.
- **Not opened:** the original 1996 lasso paper. The diamond-and-circle figure is credited to Goodfellow et al. figures 7.1 and 7.2, not to Tibshirani (1996). Do not credit the 1996 figure without opening it.
