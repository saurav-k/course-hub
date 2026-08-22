# M06 L06 - Momentum: when averaging past gradients actually helps

**Provisional number `NNNN`.** Module M06, lesson 6 of 12. **Label:** `core` **Rung:** `med` / working **Target:** 10 min

## The single tight idea

Momentum is an exponential moving average of the gradient, and it earns its keep only while the *shape of the loss*, rather than the *sampling noise*, is what is holding you back.

## Prerequisites

| Needs | From |
|---|---|
| The zigzag, and the condition number | M06 L04 |
| Gradient noise, and why it does not vanish | M06 L05 |
| Geometric series | M01 Foundations |

## Beats, in order

1. **The update, both lines, every symbol named.** `v <- alpha*v - eta*g`, then `theta <- theta + v`.
2. **What `alpha` buys, exactly.** The terminal-velocity result below. `alpha = 0.9` is a ten-times speed multiplier, `alpha = 0.99` a hundred-times one. Goodfellow et al. advise thinking in `1/(1 - alpha)` rather than in `alpha`, and this page adopts that reading.
3. **Why it kills the zigzag.** The oscillating component alternates sign and cancels in the average; the consistent component agrees with itself and accumulates. Draw both, with the numbers from the worked example.
4. **Nesterov, as a one-line modification.** Same shape, gradient evaluated *after* the momentum jump: `v <- mu*v - eta*grad f(theta + mu*v)`. In the deterministic convex case it improves `O(1/T)` to `O(1/T^2)`.
5. **The honest limit, and the beat that makes this page worth writing.** SGD on a smooth convex objective is `O(L/T + sigma/sqrt(T))`; an accelerated method is `O(L/T^2 + sigma/sqrt(T))`. **Momentum only helps while the first term dominates.** Once noise is in charge the two are equally effective. That is why momentum was written off in the 1990s and rediscovered for deep networks: deep training spends nearly all its time in the transient phase.
6. **Trade-off.** A second hyperparameter that interacts with the first, and overshoot near the optimum.

## Named theorem and its stated proof (D4)

**Result 1 (terminal velocity).** Under a constant gradient `g`, the momentum velocity converges to `v_inf = -eta*g/(1 - alpha)`, so the step size is multiplied by `1/(1 - alpha)` relative to plain gradient descent.

**Proof.** With `g` constant, unrolling `v_k = alpha*v_{k-1} - eta*g` from `v_0 = 0` gives
`v_k = -eta*g * (1 + alpha + alpha^2 + ... + alpha^(k-1)) = -eta*g * (1 - alpha^k)/(1 - alpha)`.
For `0 <= alpha < 1`, `alpha^k -> 0`, so `v_k -> -eta*g/(1 - alpha)`. **QED**
The page shows the unrolling explicitly for `k = 1, 2, 3` before writing the general term, because the geometric sum is the whole content and it is easy to state and hard to see.

**Result 2 (stated, not proved here).** Nesterov's accelerated gradient on a convex `beta`-smooth objective satisfies `f(y_t) - f(x*) <= 2*beta*||x_1 - x*||^2 / t^2` (Bubeck Thm 3.19).
**Why this page states rather than proves it.** The proof needs the estimate-sequence machinery, which is a page of its own and buys the reader nothing here. `pedagogy.md` allows a stated result with a linked source; what the page owes is the *comparison* to L03's `1/(t-1)`, which is the thing the reader can act on. **The PR must say that this is a stated result with a proof deliberately deferred, rather than a proof omitted by accident.**

## Planned figures

1. **Orientation, `flowchart`.** "L04: gradient descent zigzags on a stretched bowl" into "THIS PAGE - average the gradient across steps" into "L07 Adam, which is this plus a per-parameter rate", with "only while the surface, not the noise, is in charge" dotted in.
2. **`svg.chart`.** The stretched contours from L04 with two paths: plain descent zigzagging in `s-stat`, momentum in `s-sky` cutting along the valley floor. Same start, same `eta`, step counts labelled. Kills "momentum makes the steps bigger": it changes their direction.
3. **`svg.chart`.** Log-axis bar chart of `1/(1 - alpha)` at `alpha` = 0, 0.5, 0.9, 0.99: bars of 1, 2, 10, 100 in `m-sky`. Kills reading 0.9 and 0.99 as similar numbers.
4. **`svg.chart`.** `L/T` in `s-sky` and `sigma/sqrt(T)` in `s-noise` against `T` on log-log axes, crossing marked "after here, momentum stops helping".

## The worked example, in eight parts

Four momentum steps by hand on a two-coordinate problem, `eta = 0.1`, `alpha = 0.9`.

1. Coordinate one receives gradients `+1, -1, +1, -1`: the zigzag direction.
2. Coordinate two receives `+0.2` every step: the valley floor.
3. Coordinate one, step by step: `-0.1`, then `+0.01`, then `-0.091`, then `+0.0181`.
4. It never leaves a band of about `0.1` around zero, because each new gradient cancels most of what the last one built.
5. Coordinate two, step by step: `-0.02`, `-0.038`, `-0.0542`, `-0.0688`.
6. It grows monotonically, heading for the terminal `-0.1 * 0.2 / 0.1 = -0.2`.
7. After four steps the "useful" coordinate has accumulated about 3.8 times the velocity of the "useless" one, from gradients of comparable size.
8. **The sentence to carry: that contrast is the entire mechanism.** Momentum is a direction change, not a step-size change, and the arithmetic shows which is which.

## Quiz seeds

**Q1.** Momentum with `alpha = 0.9` multiplies the terminal step size by 10.
Distractors: 0.9 (reads `alpha` as the multiplier rather than the decay); 1.9 (counts two terms of an infinite series); 9 (the off-by-one from summing from `k = 1` instead of `k = 0`).

**Q2 (misconception).** When does momentum stop helping an SGD run?
Correct: once gradient noise, not curvature, limits progress. Distractors: "once the learning rate decays below 0.001" (a number with no mechanism); "once the objective becomes non-convex" (backwards - deep non-convex training is where it helps most); "once the batch size passes a few thousand" (confuses a cause with a correlate: a bigger batch lowers noise, which makes momentum *more* useful).

## Practice seed

**Stem.** With `eta = 0.1` and `alpha = 0.9`, run four steps for a coordinate whose gradient alternates `+1, -1, +1, -1` and for one whose gradient is `+0.2` throughout. Report both velocities, then say which is nearer its terminal value and why.
**Hint.** Run the two coordinates as two completely separate scalar recursions. Momentum never mixes coordinates, which is the fact that makes this problem doable by hand and also the fact L07 is about to change.
**Solution.** Oscillating: `-0.1, +0.01, -0.091, +0.0181`. Consistent: `-0.02, -0.038, -0.0542, -0.0688`, against a terminal `-0.2`, so it is about 34% of the way. The oscillating coordinate has no terminal value to approach at all, because its driving gradient has no constant part.
**`.p-check`.** The oscillating coordinate's velocity must change sign every step and shrink in magnitude relative to the first step. If it grows without changing sign you have used `alpha*v + eta*g` and lost the minus sign, which is the update for gradient *ascent*.

## Code and dataset

**Program:** `code/m06-06-momentum.py`. **Dataset:** `datasets/m06-credit.csv`, standardised, using the naturally ill-conditioned subset of columns so the zigzag is real.
**What it computes twice:** the number of iterations to reach a fixed objective gap, once for plain gradient descent and once for momentum at the same `eta`, from the same start. The program also verifies the terminal-velocity formula directly by feeding a constant gradient and comparing the converged velocity against `-eta*g/(1 - alpha)`; the two agree exactly at every `alpha` tested.

**The measured result changed this page's beat 3, and for the better.** Running the comparison on `f(x) = 0.5*(x1^2 + gamma*x2^2)` at `eta = 1/lambda_max` from `x0 = (gamma, 1)`, iterations to a `1e-8` gap:

| `kappa` | plain GD | momentum(0.9) | Nesterov(0.9) | speed-up |
|---|---|---|---|---|
| 2 | 14 | 150 | 18 | **0.1x** |
| 10 | 106 | 190 | 94 | 0.6x |
| 50 | 633 | 199 | 134 | 3.2x |
| 200 | 2,826 | 234 | 184 | **12.1x** |
| 1,000 | 15,764 | 1,421 | 1,437 | 11.1x |

**Momentum is ten times SLOWER at `kappa = 2` and twelve times faster at `kappa = 200`.** On the real credit problem, where `kappa` is only 26.5, it is behind plain gradient descent at two of three targets and ahead at the third.

So the page must not say "momentum helps". It must say **momentum is a cure for a stretched bowl**, show the table, and name the two reasons it can lose: a well-conditioned problem has little zigzag to cancel, and the extra effective step size can overshoot. Nesterov is the more stable of the two at every `kappa` measured, which is a concrete reason to prefer it and one the page can now state from evidence rather than from authority.

**This is also where beat 5's honesty lands.** A reader who has seen momentum lose a race will believe the noise-floor caveat. A reader who has only been told it accelerates will not.

## Sources, primary only

- Goodfellow, Bengio & Courville, ch. 8, eq 8.17 and algorithm 8.2, for the update and the terminal velocity.
- Sutskever, Martens, Dahl & Hinton, ICML 2013, eqs 3-4 for NAG in momentum form and section 2 for the `O(L/T + sigma/sqrt(T))` comparison.
- Bubeck, arXiv:1405.4980, Thm 3.19 for the accelerated rate.
