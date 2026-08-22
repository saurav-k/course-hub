# M06 L03 - Gradient descent is a first-order model, taken one step at a time

**Page `lessons/0102-gradient-descent-is-a-first-order-model.html`** &middot; module M06, lesson 3 of 12 &middot; program `code/0102-gradient-descent-is-a-first-order-model.py` &middot; dataset `datasets/m06-credit.csv`

## The single tight idea

Gradient descent is not "roll downhill". It is: build a linear approximation here, trust it for a bounded distance, throw it away, build another.

## Prerequisites

| Needs | From |
|---|---|
| Convexity, so "the minimum" means something | M06 L02 |
| **The gradient as the direction of steepest ascent, with its picture** | M05 Calculus (r1 edge 12) |
| **The first-order Taylor expansion** | M05 Calculus (r1 edge 13) |
| Vectors and the L2 norm | M03 |

M05 owns the gradient and Taylor. This page consumes both and re-derives neither.

## Beats, in order

1. **The first-order model at the current point**, every symbol named in words.
2. **The catch that motivates everything.** Minimising that linear model on its own sends you to minus infinity, because a line has no bottom. The model is only good near where it was built. So the step must be bounded, and `eta` is where the bound enters. **`eta` is part of the derivation, not a tuning afterthought.**
3. **The update rule.** Name `theta`, `eta`, `J` and the gradient again, here, in words.
4. **Three steps by hand** on a one-dimensional quadratic, arithmetic shown in full.
5. **What "it converges" is worth.** The theorem below, read in words: to get one more digit you do roughly ten times the steps. That is the *good* case.
6. **Trade-off.** Each step is cheap in thought and expensive in data - it reads every row. L05 is what happens when you refuse to pay that.

## Named theorem and its stated proof (D4)

**Theorem** (Bubeck, *Convex Optimization: Algorithms and Complexity*, Thm 3.3). Let `f` be convex and `beta`-smooth on `R^n`. Gradient descent with `eta = 1/beta` satisfies `f(x_t) - f(x*) <= 2*beta*||x_1 - x*||^2 / (t - 1)`.

**Stated proof, in the four steps the page carries.**

*Step 1, the descent lemma.* `beta`-smoothness means the gradient is `beta`-Lipschitz, which gives `f(y) <= f(x) + grad f(x).(y - x) + (beta/2)*||y - x||^2` for all `x, y`. Put `y = x - (1/beta)*grad f(x)`. The right-hand side becomes `f(x) - (1/beta)*||grad f(x)||^2 + (1/(2*beta))*||grad f(x)||^2`, so
**`f(x_{s+1}) - f(x_s) <= -(1/(2*beta))*||grad f(x_s)||^2`.** Every step strictly decreases `f` unless the gradient is zero.

*Step 2, convexity bounds the gap by the gradient.* Convexity gives `f(x*) >= f(x_s) + grad f(x_s).(x* - x_s)`, so with `d_s = f(x_s) - f(x*)` and Cauchy-Schwarz, `d_s <= ||grad f(x_s)|| * ||x_s - x*||`.

*Step 3, the distance to the optimum never grows.* This one has to be proved, not asserted, and it is the step most summaries skip.
Smoothness gives co-coercivity: `(grad f(x) - grad f(y)).(x - y) >= (1/beta)*||grad f(x) - grad f(y)||^2`.
Apply it with `y = x*`, where `grad f(x*) = 0`, and expand the square:
`||x_{s+1} - x*||^2 = ||x_s - (1/beta)*grad f(x_s) - x*||^2`
` = ||x_s - x*||^2 - (2/beta)*grad f(x_s).(x_s - x*) + (1/beta^2)*||grad f(x_s)||^2`.
Co-coercivity bounds the middle term below by `(2/beta^2)*||grad f(x_s)||^2`, so the last two terms together are at most `-(1/beta^2)*||grad f(x_s)||^2 <= 0`.
Hence `||x_{s+1} - x*|| <= ||x_s - x*||`, and every `||x_s - x*||` is at most `||x_1 - x*||`. Write `D = ||x_1 - x*||`.

*Step 4, combine and telescope.* Steps 2 and 3 give `||grad f(x_s)|| >= d_s / D`. Substituting into step 1: `d_{s+1} <= d_s - d_s^2 / (2*beta*D^2)`. Divide through by `d_s * d_{s+1}` and use `d_{s+1} <= d_s`:
`1/d_{s+1} - 1/d_s >= 1/(2*beta*D^2)`.
Summing that from `s = 1` to `t - 1` telescopes to `1/d_t >= (t - 1)/(2*beta*D^2)`, which rearranges to the theorem. **QED**

The page states each of the four steps and shows the telescoping line explicitly, because that line is where the `1/t` comes from and it is the only surprising algebra in the proof.

## Planned figures

1. **Orientation, `flowchart`.** "M05: the gradient points steepest uphill" into "THIS PAGE - trust the linear model for a bounded distance" into "L04: the learning rate is that bound", with "every training loop you will write" dotted in.
2. **`svg.chart`.** A curved objective in `s-signal`, the tangent line at the current point in `s-stat`, the step along it, and an `f-prob` band marking where the tangent is still a good approximation. Kills "the gradient tells you where the minimum is".
3. **`sequenceDiagram`.** Parameters, Loss, Gradient. Evaluate here, return the local slope, take a bounded step, **discard the model**, repeat. A flowchart cannot say "and then thrown away". No semicolon in any message, it is fatal in a sequence diagram.
4. **`svg.chart`.** Suboptimality against iteration on a log y-axis: the `O(1/t)` bound as a `ref` line, a real run on `m06-credit.csv` in `s-signal`. Kills "converges" being read as "arrives".

## The worked example, in eight parts

`J(w) = (w - 3)^2` from `w = 0`, at two learning rates.

1. `J'(w) = 2(w - 3)`, so the update is `w <- w - 2*eta*(w - 3)`, which is `w <- (1 - 2*eta)*w + 6*eta`.
2. At `eta = 0.1` the factor is `0.8`.
3. Five steps: 0, 0.6, 1.08, 1.464, 1.7712, 2.017.
4. Notice one: the steps shrink although `eta` never changed. The gradient shrinks near the optimum.
5. Notice two: after five steps `w` is still not two thirds of the way. **That is what `O(1/t)` feels like from inside.**
6. Now `eta = 0.6`, factor `1 - 1.2 = -0.2`.
7. Five steps: 0, 3.6, 2.88, 3.024, 2.9952, 3.001. It oscillates and still converges, because `|-0.2| < 1`.
8. **Ask, do not tell:** what happens at `eta = 1.0`? L04 is the answer, and the reader should arrive there with the question already formed.

## Quiz seeds

**Q1 (misconception).** Why does gradient descent take a bounded step?
Correct: the linear model it steps along is only local. Distractors: "a bigger step needs the second derivative" (that is Newton, L08); "the gradient points away from the minimum" (false); "a bigger step costs more time" (false, identical arithmetic).

**Q2.** The rate on a convex smooth objective with a well-chosen fixed step.
Correct: `1/t`. Distractors: `exp(-t)` (the *strongly* convex rate, an extra assumption this page has not made); `1/sqrt(t)` (SGD's rate - confusing the two is what L05 exists to prevent); `1/t^2` (Nesterov's, L06).

## Practice seed

**Stem.** Run five steps of `J(w) = (w - 3)^2` from `w = 0` at `eta = 0.1` and at `eta = 0.6`. Tabulate both. Then predict, without running it, what `eta = 1.0` does.
**Hint.** Rewrite the update as `w <- (1 - 2*eta)*w + 6*eta` first. Everything about the behaviour is in the single number `1 - 2*eta`, and you can read all three cases off it before computing anything.
**Solution.** The two tables above, then: at `eta = 1.0` the factor is `-1`, so `w` alternates 0, 6, 0, 6 forever. It neither converges nor diverges. That is exactly the boundary case L04 names.
**`.p-check`.** Your two sequences must both approach 3, and the second must cross it. If the `eta = 0.6` run is monotone you have used `1 - eta` instead of `1 - 2*eta` and dropped the factor of 2 from the derivative.

## Code and dataset

**Program:** `code/m06-03-gradient-descent.py`. **Dataset:** `datasets/m06-credit.csv`, standardised features.
**What it computes twice:** the descent direction, once as an analytic gradient and once by central finite differences on every coordinate. They must agree to about 1e-7. A gradient check is the single most useful habit this module can hand a reader, and running it here, before any optimizer exists, is the right place.

## Sources, primary only

- Bubeck, *Convex Optimization: Algorithms and Complexity*, arXiv:1405.4980, Theorem 3.3 and Lemmas 3.4 to 3.6 for the proof above.
- Boyd & Vandenberghe, 9.3, for gradient descent and its stopping criterion.
