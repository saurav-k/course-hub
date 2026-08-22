# M06 L07 - Adaptive learning rates: one step size per parameter

**Page `lessons/0058-adaptive-learning-rates.html`** &middot; module M06, lesson 7 of 12 &middot; program `code/0058-adaptive-learning-rates.py` &middot; dataset `datasets/m06-credit.csv`

## The single tight idea

AdaGrad, RMSProp and Adam give every parameter its own step size, computed from how large that parameter's own recent gradients have been.

## Prerequisites

| Needs | From |
|---|---|
| The step-size ceiling | M06 L04 |
| Gradient noise and minibatching | M06 L05 |
| Momentum as an exponential moving average | M06 L06 |

**Watch the word ceiling.** This page carries four optimizers and three trade-offs. The r6 report flagged it as the module's likeliest split candidate. If the draft passes 1,800 prose words, split it at the AdaGrad/RMSProp boundary rather than cutting the trade-offs, per `pedagogy.md`.

## Beats, in order

1. **The problem they were built for, in the authors' words:** "find needles in haystacks in the form of very predictive but rarely seen features". A rare feature's weight sees a gradient once in ten thousand steps and a single global step size serves it badly.
2. **AdaGrad.** Divide the step by the square root of the running *sum* of that parameter's squared gradients. Rare parameters get large steps. The flaw is structural, and the page proves it below: a sum only grows.
3. **RMSProp.** Swap the sum for a moving average: `MeanSquare(w,t) = 0.9*MeanSquare(w,t-1) + 0.1*g^2`, then divide by its square root. **Teach the provenance honestly in a `.callout`:** RMSProp's primary source is slide 29 of Hinton's Coursera lecture 6e, which attributes it "(Tijmen Tieleman, unpublished)". A method used in millions of training runs has no paper, and `pedagogy.md`'s "no blog where a primary source exists" bar is satisfied by citing the slide, not by inventing a paper.
4. **Adam** = RMSProp plus momentum plus bias correction. Algorithm 1 verbatim, with its defaults `alpha = 0.001`, `beta1 = 0.9`, `beta2 = 0.999`, `eps = 1e-8`.
5. **Why bias correction exists**, with the proof below and the arithmetic in the worked example.
6. **The reading that makes `alpha` interpretable.** The step magnitude is approximately bounded by `alpha`, "establishing a trust region around the current parameter value". That is L03's trust-region idea arriving a second time.
7. **Three trade-offs, in the same section as the technique.** The convergence proof is wrong (Reddi et al.). Adaptive methods can generalize worse than SGD even at a lower training loss (Wilson et al.). And an L2 term in the loss is **not** weight decay once the optimizer is adaptive (Loshchilov & Hutter) - which is what the W in AdamW is.
8. **Cross-link out** to `llm-papers-course/lessons/0037-muon-optimizer.html`, which opens by presuming exactly what this page teaches.

## Named theorems and their stated proofs (D4)

**Result 1 (why bias correction is exactly `1 - beta^t`).**
Let `v_t = beta2*v_{t-1} + (1 - beta2)*g_t^2` with `v_0 = 0`. Unrolling,
`v_t = (1 - beta2) * sum_{i=1..t} beta2^(t-i) * g_i^2`.
Take expectations, and suppose for the moment the true second moment is stationary, `E[g_i^2] = E[g^2]`:
`E[v_t] = E[g^2] * (1 - beta2) * sum_{i=1..t} beta2^(t-i) = E[g^2] * (1 - beta2^t)`,
because the geometric sum `sum_{i=1..t} beta2^(t-i) = (1 - beta2^t)/(1 - beta2)`.
So `v_t` underestimates `E[g^2]` by exactly the factor `(1 - beta2^t)`, and dividing by that factor removes the bias. **QED**
The stationarity assumption is what the source calls `zeta`, the residual left when the true second moment drifts; the page must name it rather than quietly assume it away.

**Result 2 (why AdaGrad's effective rate is monotonically non-increasing).**
AdaGrad accumulates `r_t = r_{t-1} + g_t^2` with `r_0 = 0` and steps with `eta/sqrt(r_t)`.
Since `g_t^2 >= 0`, the sequence `r_t` is non-decreasing, so `sqrt(r_t)` is non-decreasing, so `eta/sqrt(r_t)` is non-increasing, for every coordinate, on every problem, with no assumption at all. **QED**
That is the entire argument, and it is why AdaGrad stalls on a long non-convex run: the effective rate can only go down, and nothing in the algorithm can ever raise it again. RMSProp's moving average is precisely the repair, because a moving average can decrease.

**Result 3 (stated, with its construction given in full).** Reddi, Kale & Kumar (ICLR 2018) exhibit a convex problem on which Adam has non-zero average regret.
The construction, which the page states because it is short: the feasible set is `F = [-1, 1]`, and the cost at step `t` is `f_t(x) = C*x` when `t mod 3 = 1` and `-x` otherwise, with `C > 2`. Over any block of three steps the total is `(C - 2)*x`, which is minimised at `x = -1`.
Adam with `beta1 = 0` and `beta2 = 1/(1 + C^2)` converges to `x = +1`.
**The mechanism, which is the teachable part:** the one informative gradient `C` arrives once every three steps and is divided by a second-moment estimate that it itself dominates, so it is scaled down by roughly `C`; the two misleading gradients of `-1` are not. The average of the three scaled steps points the wrong way.
The page runs the construction rather than only describing it - see the worked example.

## Planned figures

1. **Orientation, `timeline`.** Five columns, inside the six-column limit: `2011 : AdaGrad`, `2012 : RMSProp`, `2015 : Adam`, `2018 : the proof is wrong`, `2019 : AdamW`. Kills the sense that Adam arrived whole; it is a chain of four fixes and the page is that chain.
2. **`flowchart`.** Adam's five lines as five nodes, each labelled with what it contributes, with AdaGrad and RMSProp branching in to show which line each gave.
3. **`svg.chart`.** The bias-correction inflation `1/(1 - 0.999^t)` on a log y-axis: 1000 at `t=1`, 100.5 at `t=10`, 10.5 at `t=100`, 1.6 at `t=1000`, 1.0 by `t=5000`. Kills "bias correction is a numerical detail".
4. **`svg.chart`.** The Reddi run: `x` against `t` on a log x-axis climbing 0 to `+1` in `s-alarm`, the true optimum `-1` in `m-gold`, the feasible interval shaded `f-prob`. Kills "Adam is proven to converge" by showing it walk to the worst point.

## The worked example, in eight parts

Adam's first step, and Adam walking to the worst point.

1. A parameter's gradient is `0.1`. Defaults `beta1 = 0.9`, `beta2 = 0.999`, `alpha = 0.001`, `eps = 1e-8`.
2. `m_1 = 0.9*0 + 0.1*0.1 = 0.01`. `v_1 = 0.999*0 + 0.001*0.01 = 1e-5`.
3. Corrected: `m_hat = 0.01/(1 - 0.9) = 0.1`. `v_hat = 1e-5/(1 - 0.999) = 0.01`.
4. Step: `0.001 * 0.1 / (sqrt(0.01) + 1e-8) = 0.001`. Exactly `alpha`.
5. Without the corrections: `0.001 * 0.01 / (sqrt(1e-5) + 1e-8) = 0.003162`. Three times larger, and in the wrong proportion.
6. Now the counterexample, with `C = 3` so `beta2 = 1/(1+9) = 0.1`, on `F = [-1, 1]`.
7. Adam's `x` over time: `0.0045` at `t = 3`, `0.146` at `t = 30`, `0.674` at `t = 300`, `1.000` by `t = 3,000`, and still `1.000` at two million.
8. **The optimum is `x = -1`. Adam converges to `+1`, the worst point in the feasible set.** State it plainly and let the figure carry it.

## Quiz seeds

**Q1 (misconception).** What does Adam's bias correction fix?
Correct: moment estimates start at zero, so early ones are too small. Distractors: bias in the dataset (a different sense of the word entirely); the L2-against-weight-decay mismatch (that is AdamW - a strong distractor because it is a real Adam problem); drift in the second moment on a long run (that is what the moving average itself handles).

**Q2.** What did Reddi, Kale and Kumar show about Adam in 2018?
Correct: Adam can converge to the worst point of a convex set. Distractors: it always generalises worse than SGD (that is Wilson et al., a *different* real result, which makes it the strongest distractor here); it needs a larger epsilon (false - they showed no constant epsilon rescues it); its memory grows with steps (that is AdaGrad's decay, misremembered as memory).

## Practice seed

**Stem.** A parameter's gradient is `0.1` for 100 steps and then `10.0` once. With Adam's defaults, give the update magnitude at `t = 1`, at `t = 100`, and at `t = 101`, and say why the spike does not produce a hundred-fold step.
**Hint.** Compute `m_hat` and `v_hat` separately at each `t` and look at their ratio, not at either one alone. Then ask which of the two moving averages the spike moves more, given that one has decay 0.9 and the other 0.999.
**Solution.** At `t = 1` the step is `0.001`, exactly `alpha`, as worked above. By `t = 100` both corrections are near their limits and the ratio `m_hat/sqrt(v_hat)` is near 1, so the step is again near `alpha`. At `t = 101` the spike lifts `m_hat` far more than `v_hat`, because `beta1 = 0.9` averages over roughly ten steps while `beta2 = 0.999` averages over roughly a thousand - so the numerator moves and the denominator barely does. The step rises but stays within a small multiple of `alpha`, because the ratio is bounded by construction.
**`.p-check`.** Every one of your three update magnitudes must be within a factor of about ten of `alpha = 0.001`. If any comes out near `10.0` you have used the raw gradient rather than the ratio, and you have lost the property that makes `alpha` easy to set.

## Code and dataset

**Program:** `code/m06-07-adam.py`. **Dataset:** `datasets/m06-credit.csv`, standardised, plus the self-contained Reddi construction which needs no data.
**What it computes twice:** Adam's parameter trajectory, once from Algorithm 1 written out line by line as the page states it, and once in a vectorised form over all coordinates at once. They must agree to machine precision. The program also runs the same problem with bias correction switched off, so the reader can see the first fifty steps differ and the last fifty do not, and it runs the Reddi construction to reproduce the table above.

## Sources, primary only

- Kingma & Ba, arXiv:1412.6980v9, Algorithm 1, section 2 (the trust-region reading) and section 3 (the bias-correction derivation).
- Reddi, Kale & Kumar, arXiv:1904.09237, section 3 and Theorems 1, 2 and 6.
- Tieleman & Hinton, Coursera lecture 6e slides 26-31, for RMSProp and its attribution.
- Duchi, Hazan & Singer, JMLR 12 (2011) 2121-2159, abstract, for AdaGrad's own motivation.
- Loshchilov & Hutter, arXiv:1711.05101v3, for decoupled weight decay.
- Wilson, Roelofs, Stern, Srebro & Recht, arXiv:1705.08292v2, for the generalization finding.
- Goodfellow, Bengio & Courville, ch. 8, algorithms 8.5 and 8.7.
