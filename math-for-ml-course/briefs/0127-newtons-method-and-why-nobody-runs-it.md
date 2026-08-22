# M06 L08 - Newton's method, and why nobody runs it at scale

**Page `lessons/0127-newtons-method-and-why-nobody-runs-it.html`** &middot; module M06, lesson 8 of 12 &middot; program `code/0127-newtons-method-and-why-nobody-runs-it.py` &middot; dataset `datasets/m06-credit.csv`

## The single tight idea

The second-order model gives a step that does not care how you scaled your features, and computing it costs the square of your parameter count in memory and the cube in time, every iteration.

## Prerequisites

| Needs | From |
|---|---|
| The first-order model and its bounded step | M06 L03 |
| The condition number, and why it caps the step | M06 L04 |
| **The second-order Taylor expansion and the Hessian** | M05 Calculus |
| **Positive definiteness, and what inverting a matrix costs** | M04 |

## Beats, in order

1. **Build the second-order model** where L03 built the first-order one, and minimise it exactly. The step is `-H^-1 * grad`.
2. **On a quadratic it lands on the optimum in one step, from anywhere.** Numbers, not words. This is the most persuasive thirty seconds in the module.
3. **The real prize is affine invariance.** Newton is "insensitive to the choice of coordinates, or the condition number of the sublevel sets". Everything L04 spent a page on simply does not apply. So why is the field using first-order methods?
4. **The first answer is arithmetic.** `k^2` entries, an `O(k^3)` inversion, and because the parameters move, "the inverse Hessian has to be computed at every training iteration". The worked example does the number for GPT-3 and settles it.
5. **The second answer is that the step only points downhill if `H` is positive definite**, and in a deep network it is not. L09 is the whole story of what it does instead, and this page hands the question over rather than answering it.
6. **What survives**, one line each so the reader can recognise them later: L-BFGS, Gauss-Newton, K-FAC, and the honest reading of Adam as a cheap diagonal preconditioner. Point back at L01: the reader's own `LogisticRegression(solver='lbfgs')` call has been running a quasi-Newton method all along.
7. **Trade-off.** Every practical second-order method buys tractability by approximating `H`, and the approximation is exactly where its failure mode lives.

## Named theorems and their stated proofs (D4)

**Result 1 (Newton is exact on a quadratic in one step).**
Let `f(x) = 0.5*x'Ax - b'x + c` with `A` symmetric positive definite. Then `grad f(x) = A*x - b` and the Hessian is `A` everywhere.
The Newton step from any `x_0` is `x_1 = x_0 - A^-1*(A*x_0 - b) = x_0 - x_0 + A^-1*b = A^-1*b`.
And `A^-1*b` is the unique stationary point, since `grad f(x) = 0` gives `A*x = b`, which has the unique solution `A^-1*b` because `A` is invertible.
So `x_1` is the minimiser, from **any** starting point, in **one** step. **QED**
The page follows this immediately with the observation that costs the method its crown: the step required solving a linear system in `A`, which for a real model is the whole difficulty rather than a detail.

**Result 2 (affine invariance).**
Let `x = T*y` for an invertible `T`, and let `g(y) = f(T*y)`. Then `grad g(y) = T' * grad f(x)` and `Hess g(y) = T' * Hess f(x) * T`.
The Newton step in `y` is
`-Hess g(y)^-1 * grad g(y) = -(T' H T)^-1 * T' * grad f(x) = -T^-1 * H^-1 * T'^-1 * T' * grad f(x) = -T^-1 * H^-1 * grad f(x)`.
Mapping back to `x` multiplies by `T`, giving exactly `-H^-1 * grad f(x)`: the same step.
**So Newton's iterates under any invertible linear change of coordinates are the images of its iterates in the original ones.** Rescaling a feature column changes nothing. **QED**
Contrast in one line, which is the beat: the gradient step `-eta * grad g(y) = -eta * T' * grad f(x)` is **not** the image of `-eta * grad f(x)` unless `T` is orthogonal. That single asymmetry is why L04 exists and this page does not need it.

## Planned figures

1. **Orientation, `flowchart`.** "L04: first-order methods are capped by curvature" into "THIS PAGE - the second-order step ignores curvature entirely, and cannot be afforded" into "so we approximate: Adam, L-BFGS, K-FAC", with "L09 saddle points, where it also fails" dotted in.
2. **`svg.chart`.** One objective curve in `s-signal`; the first-order model at a point as a straight line in `s-stat`; the second-order model as a parabola in `s-sky`; each model's minimum marked, with the parabola's sitting on the true one. Kills "second order means more accurate gradients": it means a different *model*.
3. **`svg.chart`.** Log-scale bar chart of Hessian storage in bytes for the three model sizes in the worked example. Kills "we could do it with a bigger machine". **No reference line unless a citable capacity figure is found** - an uncited reference line would fail the sourcing bar.
4. **`flowchart`, a decision.** "Is `k` under a few thousand?" and "Is the Hessian positive definite here?" into Newton, quasi-Newton, or first-order. Kills the impression that Newton is obsolete: it is standard inside logistic-regression solvers.

## The worked example, in eight parts

The Hessian that does not fit on Earth. **Quoted:** GPT-3's parameter count and the `O(k^3)` cost. **Derived:** everything after, with the assumptions named.

1. `k = 175,000,000,000` (Brown et al., arXiv:2005.14165: "an autoregressive language model with 175 billion parameters").
2. The Hessian is `k` by `k`, so it has `k^2 = 3.063e+22` entries.
3. At two bytes an entry - **assumption: bfloat16, stated on the page** - that is `6.13e+22` bytes.
4. Which is `61` zettabytes, for one matrix.
5. Inverting it is on the order of `k^3 = 5.36e+33` floating-point operations - **assumption: the textbook cubic bound, not a measured cost**.
6. And because the parameters change, all of it is redone **every iteration**.
7. Turn the question round: solve `2*k^2 = 80e9` for the largest `k` whose Hessian fits one 80 GB accelerator. `k = 200,000`.
8. **The sentence to carry: a model small enough for a full Newton step is smaller than a single layer of anything modern.** Then the counterweight, so the page is not a dismissal: the reader's `LogisticRegression(solver='lbfgs')` from L01 has `k = 13` here, and for that problem the second-order route is simply the right one.

## Quiz seeds

**Q1.** The main obstacle to Newton's method on a large network.
Correct: the Hessian has `k^2` entries and inverting it costs `k^3`. Distractors: the entries are too noisy (a real secondary problem, not the blocker); the second derivative does not exist for ReLU nets (true only at a measure-zero set, and not what stops Newton); the Newton step needs an unstable learning rate (backwards - the pure Newton step takes no learning rate).

**Q2 (misconception).** What does Newton buy that gradient descent cannot?
Correct: invariance to how the features have been scaled. Distractors: convergence from any start (false, pure Newton can diverge); a cheaper step (exactly backwards); **"an escape from saddle points that first-order methods miss"** - which is precisely backwards and is the most valuable distractor in this module, because L09 shows Newton is *attracted* to saddles.

## Practice seed

**Stem.** Compute the memory a full Hessian needs, at 2 bytes an entry, for `k = 10^4`, `k = 10^7` and `k = 1.75 * 10^11`. Then find the largest `k` whose Hessian fits in one 80 GB accelerator, and say what fraction of the total cost that number actually accounts for.
**Hint.** The last part is the one with teeth. Storage is not the only bill, and the other term grows faster - so a `k` that just fits in memory is not a `k` you can actually run.
**Solution.** `2*k^2` bytes: `2e8` (200 MB), `2e14` (200 TB), `6.13e22` (61 ZB). Solving `2*k^2 = 8e10` gives `k = 200,000`. Storage accounts for only part of it: at `k = 200,000` the inversion is about `8e15` operations *per iteration*, so the model that just fits in memory still needs of the order of a petaflop-scale computation for every single step.
**`.p-check`.** Your three memory figures must each be exactly `2 * k^2`, so moving from `10^4` to `10^7` - a factor of 1,000 in `k` - must move the memory by a factor of 1,000,000. If your ratio is 1,000 you have computed `2*k` and not `2*k^2`.

## Code and dataset

**Program:** `code/m06-08-newton.py`. **Dataset:** `datasets/m06-credit.csv`, standardised.
**What it computes twice:** the optimum of the logistic objective, once by Newton's method (which is iteratively reweighted least squares here) and once by gradient descent run to convergence. They must agree to several decimals while the iteration counts differ by orders of magnitude, and the program prints both counts. It also demonstrates Result 1 directly by taking a single Newton step on a quadratic from a random start and checking it lands on `A^-1*b` to machine precision, and demonstrates Result 2 by rescaling a feature column by `1e6` and confirming Newton's iterate count is unchanged while gradient descent's is not.

## Sources, primary only

- Goodfellow, Bengio & Courville, ch. 8, section 8.6.1, for the `O(k^3)` cost and the every-iteration point.
- Boyd & Vandenberghe, 9.5.3, for affine invariance and the summary of Newton's properties.
- Brown et al., arXiv:2005.14165, abstract, for the parameter count.
- He, Zhang, Ren & Sun, arXiv:1512.03385, Table 1 - **note: this paper gives ResNet-50 as 3.8 billion FLOPs and states no parameter count.** The widely repeated 25.6M figure is not in it. The middle bar of figure 3 needs a citable source or the chart shows two models.
