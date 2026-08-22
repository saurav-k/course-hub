# M06 L10 - Constrained optimization: Lagrange multipliers and KKT

**Provisional number `NNNN`.** Module M06, lesson 10 of 12. **Label:** `core` **Rung:** `med` / working **Target:** 12 min

## The single tight idea

At a constrained optimum the objective's contour is tangent to the constraint, so their gradients are parallel, and the multiplier is the exchange rate between them.

## Prerequisites

| Needs | From |
|---|---|
| Convexity - it is what turns KKT from necessary into sufficient | M06 L02 |
| **The gradient** | M05 Calculus |
| **The dot product** | M03 |
| **Eigenvectors, and PCA as M04 derives it through the SVD** | M04 (for beat 7 only) |

**D5 note.** The captain's D5 puts PCA-via-SVD in M04 and keeps **the variational route in M06**. So beat 7 is this module's, by decision, and it is a second independent derivation of a known result rather than a duplication. The page says so in one line so a reader arriving from M04 knows why they are seeing PCA twice.

## Beats, in order

1. **The picture, before any Lagrangian.** Contours of the objective, one constraint curve, and the observation that at the best feasible point the contour just *touches* the curve. If it crossed, you could slide along the constraint and do better.
2. **Tangency means the gradients are parallel**, which means one is a multiple of the other: `grad f = nu * grad h`. The multiplier is born as "the multiple", not as a trick.
3. **The Lagrangian as bookkeeping** for that statement, every symbol named.
4. **Inequalities add exactly one new fact:** a constraint is either **active** - you are pressed against it and it has a price - or **irrelevant** - you are strictly inside and its price is zero. Never both.
5. **The four KKT conditions**, each named in English before its symbols: primal feasibility, dual feasibility (`lambda >= 0`), complementary slackness (`lambda_i * f_i(x) = 0`), stationarity.
6. **The fact that decides how much they are worth**, proved below: necessary in general when strong duality holds, and **sufficient** when the problem is convex with affine equalities. L02 is what earns that.
7. **Two ML payoffs.** PCA, where the multiplier turns out to be the eigenvalue (the worked example). And the SVM, where complementary slackness is not a fact bolted on afterwards - it *is* why only the support vectors matter.
8. **Trade-off.** KKT characterises an optimum. It does not find one.

## Named theorem and its stated proof (D4)

**Theorem (KKT sufficiency for a convex problem).** Suppose `f_0, ..., f_m` are convex and `h_1, ..., h_p` are affine. If points `x~`, `lambda~`, `nu~` satisfy
(i) `f_i(x~) <= 0` for all `i`, (ii) `h_j(x~) = 0` for all `j`, (iii) `lambda~_i >= 0`, (iv) `lambda~_i * f_i(x~) = 0`, and (v) `grad f_0(x~) + sum_i lambda~_i * grad f_i(x~) + sum_j nu~_j * grad h_j(x~) = 0`,
then `x~` is primal optimal and `(lambda~, nu~)` is dual optimal, with zero duality gap.

**Proof** (Boyd & Vandenberghe 5.5.3, restated in full).
Conditions (i) and (ii) say `x~` is primal feasible.
Because every `lambda~_i >= 0` by (iii), and every `f_i` is convex and every `h_j` affine, the Lagrangian `L(x, lambda~, nu~) = f_0(x) + sum_i lambda~_i f_i(x) + sum_j nu~_j h_j(x)` is a convex function of `x`: it is a non-negative combination of convex functions plus affine terms.
Condition (v) says the gradient of that convex function vanishes at `x~`. For a convex differentiable function, a vanishing gradient is a global minimum. So `x~` minimises `L(., lambda~, nu~)` over all `x`, which means the dual function satisfies `g(lambda~, nu~) = L(x~, lambda~, nu~)`.
Now evaluate it: `g(lambda~, nu~) = f_0(x~) + sum_i lambda~_i f_i(x~) + sum_j nu~_j h_j(x~)`.
Every term in the second sum is zero by complementary slackness (iv), and every term in the third is zero by primal feasibility (ii). So `g(lambda~, nu~) = f_0(x~)`.
Weak duality says `g(lambda, nu) <= p*` for every dual-feasible pair, and `p* <= f_0(x~)` for every primal-feasible `x~`. Together with the equality just shown, this forces `g(lambda~, nu~) = p* = f_0(x~)`.
So `x~` attains the primal optimum, `(lambda~, nu~)` attains the dual optimum, and the gap is zero. **QED**

**The one line the page must add after the proof**, because it is where readers over-claim: **in the non-convex case the KKT conditions are only necessary**, and only when strong duality holds. A point satisfying them in a non-convex problem may be a saddle - which is L09's subject and is not a coincidence.

**Companion result, derived on the page (the multiplier is a price).** For the problem `min f_0(x)` subject to `h(x) = b`, the optimal value `p*(b)` satisfies `dp*/db = nu*` under standard regularity. The page does not prove the general statement; it *measures* it, in the practice problem, which is the honest version at this rung.

## Planned figures

1. **Orientation, `flowchart`.** "L03 to L09: unconstrained minimisation" into "THIS PAGE - what an optimum looks like when the answer is fenced in" into "L11: regularization is one of those fences", with "PCA and the SVM" dotted in.
2. **`svg.chart`, the centrepiece.** Objective contours in `ink`, one constraint curve in `s-alarm`, the unconstrained optimum in `m-gold` outside the feasible set, the constrained optimum in `m-signal` on the curve, and the two gradient arrows at that point drawn parallel. Kills the multiplier arriving as algebra: it is the length ratio of two arrows in this figure.
3. **`stateDiagram-v2`.** Two states: "constraint active - pressed against the fence - price positive" and "constraint inactive - strictly inside - price zero", with the transitions labelled by what moves the optimum across. Kills the opacity of complementary slackness: written as `lambda_i * f_i(x) = 0` it is a puzzle; drawn as two states with no third, it is obvious.
4. **`flowchart`.** The four KKT conditions as four nodes, each labelled with the one thing it forbids: an infeasible point, a negative price, paying for a fence you are not touching, and a direction that still goes downhill.

## The worked example, in eight parts

PCA is a Lagrange multiplier problem, and the multiplier is the eigenvalue.

1. State the problem: maximise `w'Sw` subject to `w'w = 1`, where `S` is the sample covariance matrix of the standardised features of `m06-credit.csv`.
2. The Lagrangian: `L(w, lambda) = w'Sw - lambda*(w'w - 1)`.
3. Stationarity, differentiating with respect to `w`: `2*S*w - 2*lambda*w = 0`.
4. So `S*w = lambda*w`. **The stationary points are exactly the eigenvectors of `S`.** No eigenvalue was assumed; it fell out of the multiplier.
5. Substitute back: `w'Sw = w'(lambda*w) = lambda*(w'w) = lambda`, using the constraint. **The value of the objective at a stationary point is the multiplier itself.**
6. So the maximiser is the eigenvector of the largest eigenvalue, and the variance it captures *is* that eigenvalue.
7. Confirm on the real matrix: the largest eigenvalue of the 12-by-12 standardised covariance, computed two ways, once by `numpy.linalg.eigvalsh` and once by power iteration from a random start, agreeing to eight decimals.
8. **The sentence to carry: M04 reached this through the SVD and M06 reached it through a multiplier, and they are the same number.** That is also where the module's notation collision resolves: `lambda` is the multiplier *and* the eigenvalue because here they are one object.

## Quiz seeds

**Q1 (misconception).** Complementary slackness says a constraint you are not touching has a zero multiplier.
Distractors: every constraint has a strictly positive multiplier (contradicts it directly); the multipliers sum to one (confuses them with a probability distribution); an equality constraint has a non-negative multiplier - **a real KKT condition attached to the wrong kind of constraint**, since an equality multiplier is free to be negative. That is a genuinely easy slip and it earns its place.

**Q2.** Written as a constrained problem, PCA's Lagrange multiplier turns out to be the eigenvalue, which is the variance captured.
Distractors: the number of components kept; the reciprocal of the regularization strength; the norm of the loading vector - which the constraint has already fixed at 1, so it cannot be the multiplier, and the feedback should say exactly that.

## Practice seed

**Stem.** Minimise `x^2 + y^2` subject to `x + y = 2`. Then relax the constraint to `x + y = 2.1` and check whether the objective changes by about `lambda` times `0.1`.
**Hint.** Write the stationarity conditions for `x` and for `y` separately and compare them before you use the constraint at all. What they say about the relationship between `x` and `y` solves most of the problem on its own.
**Solution.** `L = x^2 + y^2 - lambda*(x + y - 2)`. Stationarity gives `2x = lambda` and `2y = lambda`, so `x = y`. The constraint then gives `x = y = 1`, `lambda = 2`, objective `2`. At `b = 2.1`: `x = y = 1.05`, objective `2 * 1.05^2 = 2.205`. The rise is `0.205` against the predicted `lambda * 0.1 = 0.2`. **The `0.005` difference is the second-order term, and saying so is the honest version** - the multiplier is a first-order price, exact only in the limit.
**`.p-check`.** Your `lambda` must come out positive here, and the objective must *rise* when you relax the constraint. If it falls, you have relaxed in the direction that makes the problem easier, and you should re-read which side of `x + y = b` the feasible set is on.

## Code and dataset

**Program:** `code/m06-10-kkt-pca.py`. **Dataset:** `datasets/m06-credit.csv`, standardised.
**What it computes twice:** the first principal direction and its captured variance, once by solving the eigenproblem `S*w = lambda*w` with `numpy.linalg.eigvalsh`, and once by projected gradient ascent on `w'Sw` with `w` renormalised to the unit sphere after every step - which is the constrained optimization this page teaches, run as an algorithm. The two must agree, and the program also prints `w'Sw` at the answer to show it equals `lambda`. A third block measures the shadow price numerically by re-solving the toy problem at a ladder of `b` values and differencing.

## Sources, primary only

- Boyd & Vandenberghe, *Convex Optimization*, 5.5.2 for complementary slackness, 5.5.3 for the KKT conditions and the sufficiency proof above.
- Goodfellow, Bengio & Courville, ch. 4 and section 7.2, for the generalized Lagrange function in the form L11 will reuse.
