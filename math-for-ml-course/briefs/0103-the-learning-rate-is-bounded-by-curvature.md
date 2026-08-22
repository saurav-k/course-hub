# M06 L04 - The learning rate is bounded by curvature

**Page `lessons/0103-the-learning-rate-is-bounded-by-curvature.html`** &middot; module M06, lesson 4 of 12 &middot; program `code/0103-the-learning-rate-is-bounded-by-curvature.py` &middot; dataset `datasets/m06-credit.csv`

## The single tight idea

The largest step that does not diverge is set by the curvature of the loss, not by taste, and every schedule ever proposed is a negotiation with that bound.

## Prerequisites

| Needs | From |
|---|---|
| The update rule and the bounded step | M06 L03 |
| **Eigenvalues, quadratic forms, positive definiteness** | M04 |
| **The condition number of a symmetric matrix** | M04 (see the amendment note below) |
| **The Hessian** | M05 Calculus |

**Boundary note for integration.** The r6 scout report's amendment A2 asked that **M04 own the definition of the condition number** as an eigenvalue ratio, and **M06 own its consequence for optimization**. If M04's briefs do not define it, this page defines it in one line and flags the duplication in the PR rather than silently taking it.

## Beats, in order

1. **One dimension, completely.** On `J(w) = 0.5*L*w^2`, gradient descent is `w <- (1 - eta*L)*w`. Derive the threshold below.
2. **Read the four regimes off that single factor.** `eta < 1/L` monotone; `1/L < eta < 2/L` oscillating and shrinking; `eta = 2/L` a permanent oscillation; `eta > 2/L` divergence. A first-epoch `NaN` is the fourth row.
3. **Many dimensions.** `L` becomes the *largest* Hessian eigenvalue. **One stiff direction caps the step for every direction, including the flat ones that needed a big step.** This is the page's key callout.
4. **Name the ratio.** Condition number `kappa = lambda_max / lambda_min`. Boyd's exact example: `f(x) = 0.5*(x1^2 + gamma*x2^2)` under exact line search from `x0 = (gamma, 1)` shrinks `f` by exactly `((gamma-1)/(gamma+1))^2` per step. At `gamma = 10` that is `0.6694`; at `gamma = 100`, `0.9608`. Numbers, not adjectives.
5. **Feature scaling is a curvature intervention, not hygiene.** The measured numbers are in the worked example and they are dramatic.
6. **The three schedules, each as a consequence of a beat above.** Warmup, because the Hessian early in training is not the Hessian later. Decay or cosine, because the final approach needs a smaller trust region. The learning-rate range test, because `2/L` is measurable even when `L` is not.
7. **Trade-off.** A small `eta` is always safe and always slow. No single value is both.

## Named theorem and its stated proof (D4)

**Result 1 (derived on the page).** Gradient descent on `J(w) = 0.5*L*w^2` converges to 0 from any start if and only if `0 < eta < 2/L`.

**Proof.** `J'(w) = L*w`, so the update is `w_{k+1} = w_k - eta*L*w_k = (1 - eta*L)*w_k`, hence `w_k = (1 - eta*L)^k * w_0`.
A geometric sequence `r^k * w_0` tends to 0 for every `w_0` exactly when `|r| < 1`.
Here `r = 1 - eta*L`, so the condition is `-1 < 1 - eta*L < 1`, that is `0 < eta*L < 2`, that is `0 < eta < 2/L`. **QED**
At `eta = 2/L` we get `r = -1` and `|w_k| = |w_0|` forever, which is the permanent oscillation in beat 2, and it converges for no starting point except `w_0 = 0`.

**Result 2 (quoted, with the source's own derivation of the key step).** For a strongly convex `f` with `m*I <= Hessian <= M*I`, gradient descent with exact line search satisfies `f(x_k) - p* <= c^k * (f(x_0) - p*)` with `c = 1 - m/M`.

**Stated proof** (Boyd & Vandenberghe 9.3.1). Smoothness gives the quadratic upper bound `f(x - t*grad f(x)) <= f(x) - t*||grad f(x)||^2 + (M*t^2/2)*||grad f(x)||^2`. The right-hand side is a quadratic in `t`, minimised at `t = 1/M`, where its value is `f(x) - (1/(2*M))*||grad f(x)||^2`. Exact line search does at least as well as that particular `t`, so `f(x+) <= f(x) - (1/(2*M))*||grad f(x)||^2`. Strong convexity gives `||grad f(x)||^2 >= 2*m*(f(x) - p*)`. Substituting, `f(x+) - p* <= (1 - m/M)*(f(x) - p*)`. Applying it recursively gives the theorem. **QED**
The consequence the page actually uses: the iteration count grows roughly linearly in `M/m`, because `log(1/c) = -log(1 - m/M)` is approximately `m/M` when `M/m` is large.

## Planned figures

1. **Orientation, `flowchart`.** "L03 the step is bounded" into "THIS PAGE - curvature sets the bound at 2/L" into "L05 SGD, L06 momentum, L07 Adam - all of them negotiate this bound", with "why feature scaling changes training time" dotted in.
2. **`svg.chart`, the centrepiece.** Four traces of `w` against iteration from the exact recursion with `L = 10`: `eta = 0.05` (`s-stat`, monotone), `0.19` (`s-sky`, oscillating and shrinking), `0.2` (`s-plum`, permanent oscillation), `0.21` (`s-alarm`, reaching 117.4 by step 50). Kills "too big a learning rate makes it slower": past `2/L` it diverges, and the two look nothing alike.
3. **`svg.chart`.** Elliptical contours of Boyd's `gamma = 10` quadratic in `ink` with the exact zigzag from `x0 = (10, 1)` in `s-signal`, beside circular contours reached almost directly. Kills "gradient descent walks towards the minimum": it walks perpendicular to the contour.
4. **`stateDiagram-v2`.** States `warmup`, `peak`, `decay`, `floor`, with transitions labelled by what changes. Kills reading a schedule as an arbitrary curve.

## The worked example, in eight parts

The measured conditioning of `m06-credit.csv`, raw against standardised. **All eight numbers are computed by `code/m06-04-learning-rate.py` and reproduced.**

1. Load the 12 feature columns and the `default` target. Feature scales run from a ratio in `[0, 1]` to an income in the hundreds of thousands.
2. Form the logistic Hessian at `theta = 0` on all 20,000 rows.
3. Raw eigenvalues: smallest `4.7367e-04`, largest `1.3366e+09`.
4. So the raw condition number is `2.8218e+12`, and the largest safe step is `2/L = 1.4963e-09`.
5. Standardise every feature to mean 0 and standard deviation 1. Recompute.
6. Standardised eigenvalues: smallest `1.9599e-02`, largest `5.1960e-01`.
7. So `kappa = 26.51` and the largest safe step is `3.8491`.
8. **The sentence to carry: standardising moved the condition number by a factor of `1.06e+11` and the largest safe learning rate from about `1.5e-9` to about `3.8`.** That is nine orders of magnitude in the one number a practitioner types. Feature scaling is not hygiene.

## Quiz seeds

**Q1 (misconception).** Gradient descent on `0.5*L*w^2` diverges once the learning rate exceeds `2/L`.
Distractors: `1/L` (where *oscillation* starts, not divergence, and the two look nothing alike); `L/2` (ratio upside down - steeper means a smaller safe step); `1` (drops the `L`).

**Q2.** Why does standardising features make gradient descent faster?
Correct: it lowers the condition number, so a larger step is safe. Distractors: fewer parameters (false, no dimensions change); "makes the gradient point at the minimum" (overclaims - it reduces the zigzag, it does not remove it); "removes correlation between features" (that is whitening or PCA, not standardising).

## Practice seed

**Stem.** A quadratic has Hessian eigenvalues 40, 4 and 0.4. Find the largest converging step size, the condition number, the per-step contraction `((k-1)/(k+1))^2` under exact line search, and roughly how many steps to reduce the objective by `1e-6`. Then say what happens to the last number if preprocessing brings `kappa` to 10.
**Hint.** Only two of the three eigenvalues matter, and they are not the two you might reach for. The step limit is set by the largest alone; the condition number needs the largest and the smallest. The middle eigenvalue is a decoy.
**Solution.** `2/40 = 0.05`. `kappa = 40/0.4 = 100`. `(99/101)^2 = 0.9608`. `log(1e-6)/log(0.9608) = 345.4`, so about 345 steps. At `kappa = 10` the contraction is `(9/11)^2 = 0.6694` and the count is `34.4`, so about 34 steps. **Ten times the conditioning, ten times the training time.**
**`.p-check`.** Your contraction factor must lie strictly between 0 and 1. If it is negative you have squared after subtracting rather than before, and if it exceeds 1 you have the ratio inverted - either way the step count comes out negative, which is the tell.

## Code and dataset

**Program:** `code/m06-04-learning-rate.py`. **Dataset:** `datasets/m06-credit.csv`.
**What it computes twice:** the largest safe learning rate, once analytically as `2/lambda_max` from `numpy.linalg.eigvalsh` of the Hessian, and once empirically by running gradient descent at a ladder of step sizes and finding the largest that survives. The empirical route is what a practitioner actually has, and seeing it land on the analytic answer is the point.

**And they do not always agree, which turned out to be a better beat than the one first planned.** Measured:

- **On least squares** the Hessian is `X'X/n`, constant everywhere, so `2/L` is exact. Analytic `2/L = 9.6228e-01`; the empirical boundary sits between `0.99x` and `1.01x` of it, and every rate at or above `1.01x` diverges. **The two routes agree to one per cent.**
- **On logistic regression they do not.** The empirical limit is `2.00x` the analytic one. The reason is measurable and the program measures it: the logistic Hessian carries weights `p*(1-p)`, which shrink as the model grows confident, so the largest eigenvalue falls from `5.1960e-01` at `theta = 0` to `3.0657e-01` at the optimum, a factor of `1.695`. **The bound moved while we were walking towards it.**

**The page must carry this contrast rather than hide it.** `2/L` is exact on a quadratic and a conservative guide on anything else, and a reader who takes it as a law will be puzzled the first time a logistic run survives a step size the formula forbade. Stating the scope of a threshold is part of teaching the threshold. This also gives the page an honest reason to introduce the least-squares objective, where the geometry it draws is exactly right.

## Sources, primary only

- Boyd & Vandenberghe, *Convex Optimization*, 9.3.1 for the strongly convex rate and 9.3.2 for the exact `gamma` example.
- The `2/L` threshold is derived on the page from the exact recursion, labelled as derived rather than quoted, per `pedagogy.md`.
