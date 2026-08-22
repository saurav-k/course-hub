# M06 L02 - Convexity, and the one guarantee it buys

**Page `lessons/0053-convexity-and-the-one-guarantee-it-buys.html`** &middot; module M06, lesson 2 of 12 &middot; program `code/0053-convexity-and-the-one-guarantee-it-buys.py` &middot; dataset `datasets/m06-credit.csv`

## The single tight idea

In a convex problem no local minimum is anything but the global one, and that single fact is the line between problems that are *solved* and problems that are *trained*.

## Prerequisites

| Needs | From |
|---|---|
| Learning framed as a minimisation | M06 L01 |
| Vectors, and the line segment between two points | M03 |
| A symmetric matrix being positive semi-definite | M04, quadratic forms |

**M06 owns convexity outright** (r1 edge 22). M09 consumes it and does not redefine it.

## Beats, in order

1. **Convex set, from the segment.** For any two members and any `t` in `[0,1]`, `t*x1 + (1-t)*x2` is also a member. One set that is, one that is not.
2. **Convex function, from the chord.** `f(t*x + (1-t)*y) <= t*f(x) + (1-t)*f(y)`. The chord lies above the graph. Words before symbols.
3. **The guarantee, and its proof.** See below. It is short enough to teach, and it is the reason the whole module exists.
4. **The ML ledger.** Convex: least squares, logistic regression, hinge plus L2, lasso, ridge. Not convex: k-means, matrix factorisation, any network with a hidden layer.
5. **What convexity does not buy.** Not speed - L04 is a whole page on a convex problem being slow. Not a unique minimiser - logistic regression on separable data has none. And non-convex is not hopeless - L09 is why.
6. **Trade-off.** The price of a convex objective is usually a model that is linear in its parameters.

## Named theorem and its stated proof (D4)

**Theorem.** In a convex optimization problem, every locally optimal point is globally optimal.

**Proof** (Boyd & Vandenberghe 4.2.2, restated in full).
Let `x` be locally optimal: `x` is feasible and `f0(x) = inf{ f0(z) : z feasible, ||z - x|| <= R }` for some `R > 0`.
Suppose `x` is not globally optimal. Then some feasible `y` has `f0(y) < f0(x)`.
Necessarily `||y - x|| > R`, because otherwise `y` would sit inside the ball and contradict local optimality directly.
Now take the point `z = (1 - t)*x + t*y` with `t = R / (2*||y - x||)`, which lies in `(0, 1)`.
Two facts about `z`. First, `||z - x|| = t*||y - x|| = R/2 < R`, so `z` is inside the ball. Second, `z` is feasible, because the feasible set is convex and `z` is on the segment between two feasible points.
By convexity of `f0`, `f0(z) <= (1 - t)*f0(x) + t*f0(y) < f0(x)`, the strict inequality because `t > 0` and `f0(y) < f0(x)`.
So `z` is feasible, within `R` of `x`, and strictly better than `x`. That contradicts local optimality. Hence no such `y` exists and `x` is globally optimal. **QED**

The page must draw this before writing it: the ball, the far better point, and the point on the segment that sneaks inside the ball.

## Planned figures

1. **Orientation, `flowchart`.** "L01 an objective to minimise" into "THIS PAGE - convex means local equals global" into two outcomes, "Solved: least squares, logistic regression" and "Trained: every neural network", with "which guarantees your optimizer gets" dotted in.
2. **`svg.chart`, two panels.** Left a convex curve with a chord above it, right a non-convex curve with a chord cutting below. Same axes, `s-signal` curves, `ink` chords. Kills "convex means bowl-shaped": it is a statement about chords.
3. **`svg.chart`.** Two `f-prob` regions, one convex one not, each with a segment between two of its points, the second segment leaving. Kills the convex-set against convex-function collision, which is what breaks readers here.
4. **`quadrantChart`.** "convex" against "has a closed form". Least squares both; logistic regression convex without; k-means neither; a deep net neither and badly conditioned. Kills "convex means easy".

## The worked example, in eight parts

Verifying convexity three ways on the real objective from L01.

1. State the chord test in one line.
2. Pick two parameter vectors `theta_A`, `theta_B` from the L01 page.
3. Evaluate the logistic objective at both, on `m06-credit.csv`.
4. Evaluate at the midpoint `0.5*theta_A + 0.5*theta_B`.
5. Compare the midpoint value against the average of the two. The chord test says the midpoint must be lower or equal.
6. Now the second route: form the Hessian of the same objective and read its smallest eigenvalue. Positive semi-definite is the second-derivative test.
7. Now the counterexample: the same three steps on `f(a,b) = (a*b - 1)^2`, where the midpoint comes out **higher** and the chord test fails.
8. **The sentence to carry:** two routes agree on the logistic objective and both reject the product objective, and the product objective is the shape of every matrix-factorisation model.

Numbers to state on the page: the smallest Hessian eigenvalue of the standardised logistic objective at `theta = 0` is `1.96e-2`, and the largest is `5.20e-1`, both computed on all 20,000 rows. Both positive, so positive definite there.

## Quiz seeds

**Q1 (misconception).** What exactly does convexity guarantee?
Correct: every local minimum is global. Distractors: a closed form exists (false both ways - least squares has one, logistic regression does not, both convex); gradient descent will be quick (L04 disproves it on a convex problem); the minimiser is unique (separable logistic regression has none).

**Q2.** A set is convex when the segment between any two of its points stays inside.
Distractors: "its boundary curves outward at every point" (a square is convex with flat sides); "described by one quadratic inequality" (a special case, not the definition); "every function over it is convex" (the term collision).

## Practice seed

**Stem.** Decide convexity for `f(w) = w^4`, `f(w) = |w|`, `f(w) = w^3`, and `f(a,b) = (a*b - 1)^2`, and justify each with the cheapest correct argument.
**Hint.** Two of these have a second derivative everywhere and one does not. For the one that does not, go back to the chord. For the two-parameter one, a single counterexample pair is a complete answer and is faster than any Hessian.
**Solution.** Convex, convex, not convex, not convex. `w^4`: `f'' = 12w^2 >= 0`. `|w|`: no second derivative at 0, but the chord test holds everywhere by the triangle inequality. `w^3`: `f'' = 6w < 0` for `w < 0`. `(a*b - 1)^2`: take `(1, 1)` and `(-1, -1)`, both giving 0, whose midpoint `(0, 0)` gives 1, which is above the chord.
**`.p-check`.** Your counterexample for the last one must give a midpoint value strictly greater than the average of the endpoint values. If it is equal, you have found an affine segment and proved nothing.

## Code and dataset

**Program:** `code/m06-02-convexity.py`. **Dataset:** `datasets/m06-credit.csv`.
**What it computes twice:** convexity of the logistic objective, once by sampling 5,000 random chords and checking the inequality on every one, and once by taking the smallest eigenvalue of the analytic Hessian. Sampling can only ever fail to find a counterexample; the eigenvalue is a proof at that point. The program prints both and says which is which, because that distinction is itself a teaching beat.

## Sources, primary only

- Boyd & Vandenberghe, *Convex Optimization*: 2.1.4 convex sets, 3.1.1 convex functions, 4.2.2 local equals global, 7.1.1 logistic regression is convex.
- Goodfellow, Bengio & Courville, ch. 8, for the non-convexity of neural network training.
