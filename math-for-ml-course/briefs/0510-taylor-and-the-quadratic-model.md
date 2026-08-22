# 0510 - Taylor expansion: every loss is a quadratic if you stand close enough

> **PLACEHOLDER NUMBER.** Real number assigned by the scaffold (#41). Report label C10.

| | |
|---|---|
| Module | M05 Calculus |
| Rung | frontier (`pill hard`) |
| Label | `core` |
| Prerequisites | 0505, 0509. |
| Enables | M06's step sizes, trust regions and Newton's method |

## The single tight idea

The local quadratic model is the single object that ties the gradient, the curvature and
the largest safe step together.

## Beats, in order

1. **First order.** `f(x) ~= f(x0) + grad f(x0) . (x - x0)`. Draw it against the true
   function and mark where it stops tracking.
2. **Second order.** Add `(1/2)(x - x0)^T H (x - x0)`. Draw it. It tracks much further,
   and the figure should make "much further" a distance you can read off an axis.
3. **Substitute a gradient step** `x = x0 - eps g` and get three named terms: the current
   value, the promised improvement `-eps g^T g`, and the curvature correction
   `+(1/2) eps^2 g^T H g`.
4. **Read the third term.** When it is large the step goes uphill. This is the mechanism
   behind a diverging run, drawn rather than asserted.
5. **Solve for the step that minimises the model:** `eps* = g^T g / (g^T H g)`, and in the
   worst case `1/lambda_max`.
6. **Worked: the same regression before and after standardising the columns.**
7. **The conclusion the reader keeps.** Feature scaling is a curvature fix. It changes the
   Hessian's condition number, and the condition number is what limits the step. M06 owns
   what to do about it.

## Named theorem and its stated proof

**Taylor's theorem with the Lagrange remainder, one variable, then the multivariate form
this course actually uses.**

> **One variable.** If `f` is `n+1` times differentiable on an open interval containing
> `a` and `x`, then there exists `c` strictly between `a` and `x` with
>
>   `f(x) = sum_{k=0}^{n} f^(k)(a) (x-a)^k / k!  +  f^(n+1)(c) (x-a)^(n+1) / (n+1)!`.
>
> *Proof.* Fix `x != a`. Let `P(t)` be the degree-`n` Taylor polynomial of `f` about `t`
> evaluated at `x`, that is `P(t) = sum_{k=0}^{n} f^(k)(t)(x-t)^k / k!`, and define
>
>   `g(t) = f(x) - P(t) - M (x-t)^(n+1)`,
>
> choosing the constant `M` so that `g(a) = 0`. Also `g(x) = 0`, because `P(x) = f(x)` and
> the last term vanishes. So `g` vanishes at both endpoints and Rolle's theorem gives a
> `c` strictly between them with `g'(c) = 0`.
> Differentiating `P` telescopes: every term cancels against the next except the last, so
> `P'(t) = f^(n+1)(t)(x-t)^n / n!`. Hence
>
>   `g'(t) = -f^(n+1)(t)(x-t)^n / n! + M (n+1)(x-t)^n`.
>
> Setting `g'(c) = 0` and cancelling `(x-c)^n`, which is non-zero since `c != x`, gives
> `M = f^(n+1)(c) / (n+1)!`. Substituting that `M` back into `g(a) = 0` is exactly the
> statement of the theorem. **QED**
>
> **Multivariate, the form this course uses.** For `f : R^n -> R` twice continuously
> differentiable and any `h`, there exists `t` in `(0,1)` with
>
>   `f(x + h) = f(x) + grad f(x) . h + (1/2) h^T H(x + t h) h`.
>
> *Proof.* Apply the one-variable case with `n = 1` to `phi(s) = f(x + s h)` on `[0,1]`.
> The chain rule gives `phi'(s) = grad f(x + s h) . h` and
> `phi''(s) = h^T H(x + s h) h`. The one-variable statement reads
> `phi(1) = phi(0) + phi'(0) + phi''(t)/2` for some `t` in `(0,1)`, which is the display
> above. **QED**
>
> The remainder is what makes "how far can I trust this" answerable rather than a
> gesture, and it is the reason the second-order model is a model and not a guess. Keep
> it to this one statement and never use it again on the page: r1 D4 asks for the proof,
> not for a course in analysis.

## Figures

1. **Orientation, `flowchart LR`.** "Gradient (0505) and curvature (0509)" into "THIS
   PAGE: the local model that uses both" into "step sizes, trust regions and Newton (M06)".
2. **`svg.chart`.** One function with its first-order and second-order Taylor
   approximations at a point, all three drawn, with the interval where each stays within
   one per cent marked on the axis. *Kills:* "a Taylor series is an infinite thing".
   Two terms buy a usable neighbourhood, and you can see how wide.
3. **`svg.chart`, quantitative.** Predicted decrease against step size `eps`: the linear
   term falling, the quadratic correction rising, and their sum turning back up, with
   `eps*` marked. *Kills:* "a bigger step always goes further downhill".
4. **`svg.chart`, quantitative.** Contours of the same loss before and after
   standardisation, side by side at the same scale: a near-degenerate ellipse next to a
   near-circle, labelled with the two condition numbers.
   *Kills:* "feature scaling is cosmetic".

## Worked example, in eight parts

1. **Setting.** The housing regression at a starting guess. How big a step can the
   curvature tolerate, and what does standardising change?
2. **Symbolic.** `.math` for the three-term expansion and for `eps* = g^T g / (g^T H g)`,
   with a `.gloss` naming `eps`, `g`, `H`, and saying what each of the three terms is.
3. **Picture.** Figure 3, before the arithmetic.
4. **`ol.worked`.** Compute `g^T g`, then `g^T H g`, then `eps*`, then `1/lambda_max`,
   then repeat the whole thing on standardised columns.
5. **`.keynum`** on nothing: derived here.
6. **Sanity check.** `eps*` must be positive, because `g^T g > 0` and `g^T H g > 0` for a
   positive definite `H`. And `eps*` must be at least `1/lambda_max`, with equality when
   `g` is parallel to the top eigenvector. Both hold, and the near-equality is itself the
   diagnosis: `|cos angle(g, v_max)| = 0.999946`.
7. **What changes if** you standardise only the worst column and leave the others?
   The condition number falls but does not collapse, because the problem is the ratio
   between columns and fixing one moves the ratio without equalising it. That is why
   scaling is applied to the whole design matrix and not to the column that looks worst.
8. **In words.** Nothing about the data changed. Only the units did, and the largest step
   the curvature will tolerate rose by seven orders of magnitude.

## Quiz seeds

**Q1, misconception.** In
`f(x0 - eps g) ~= f(x0) - eps g^T g + (1/2) eps^2 g^T H g`, which term can make a
downhill step increase the loss?
*Answer:* the third, the curvature correction.
*Distractors:* "the first" is a constant; "the second" is always a decrease for
`eps > 0`; "none of them, a downhill step always decreases the loss" is the misconception.

**Q2.** Standardising the housing columns drops the Hessian condition number from
`1.22e9` to `10.8`. What follows for the step the curvature will tolerate?
*Answer:* it rises from about `6.4e-9` to about `0.22`, roughly thirty-four million times
larger.
*Distractors:* "it is unchanged, scaling only relabels the axes" is the trap; "it falls"
has the sign backwards; "it cannot be known without the gradient" ignores the worst-case
bound `1/lambda_max`.

## Practice seed

**Stem.** Starting from `theta = 0` on the raw housing regression, with
`g = (-850000, -862)` in the two-feature cut-down: compute `g^T g`, compute `g^T H g`
given `H = 2 X^T X`, compute `eps* = g^T g / (g^T H g)`, then compare it with
`1/lambda_max` and explain why they nearly agree.

**Hint.** They agree when the gradient is nearly parallel to the top eigenvector. Compute
that cosine before you try to explain the coincidence.

**Solution.** `g^T g = 7.225e11`, `g^T H g = 3.6125e18`, so `eps* = 2.0e-7`. And
`1/lambda_max = 2.0e-7`. They agree because `g` is almost exactly parallel to the top
eigenvector, which is what unscaled columns guarantee: the biggest column dominates both
the gradient and the curvature.

**`.p-check`.** `eps*` can never be smaller than `1/lambda_max`, because
`g^T H g <= lambda_max g^T g`. An answer below `1/lambda_max` is an arithmetic error.

## Code and dataset

`../code/m05_10_taylor_step.py` against `../datasets/m05-housing.csv` and
`../datasets/m05-scores.csv`. It measures how far each Taylor order stays accurate,
computes `eps*` and scans the true loss along the descent ray, and repeats the
conditioning analysis with standardised columns.

Verified output to quote. **A squared-error loss is exactly quadratic, so its second-order
Taylor model is not an approximation of it, it is it**: the second-order error column sits
at the floating-point floor (`0` to `2.2e-11`) and does not fall, because the third
derivative is zero. The rate demonstration therefore runs on a logistic loss instead,
where the measured error ratios per decade are `100.0` for first order and `1001.8` for
second, matching the distance squared and the distance cubed. Then `g^T g = 1.207e13`,
`g^T H g = 1.900e21`, `eps* = 6.352990e-09` against `1/lambda_max = 6.352310e-09` with
`|cos| = 0.999946`. The scan along `-g` gives loss `39,589.63` at `eps = 0`, `1,251.71`
at `eps*`, and **exactly `39,589.628830` again at `2 eps*`**, which is the quadratic's
exact symmetry and is worth showing. Standardising moves `kappa` from `1.22e9` to `10.8`
and `1/lambda_max` from `6.35e-9` to `0.218`.

**This correction is worth a `.callout` on the page.** The obvious demonstration of
Taylor error rates does not work on a squared-error loss, and a page that claimed a cubic
rate there while its own numbers sat at the floating-point floor would be teaching a
confident wrong thing. Use the logistic loss for the rates and say why.

## Sources

- Goodfellow, Bengio and Courville, *Deep Learning*, section 4.3.1, equations 4.8, 4.9
  and 4.10, for the second-order expansion, the three-term substitution, the observation
  that a large curvature term can move a gradient step uphill, `eps* = g^T g / (g^T H g)`,
  and the worst case `1/lambda_max`.
  `https://www.deeplearningbook.org/contents/numerical.html`
- Deisenroth, Faisal and Ong, *Mathematics for Machine Learning*, section 5.8, for
  linearisation as the first-order case and for the multivariate Taylor series.
  `https://mml-book.github.io/book/mml-book.pdf`
- Boyd and Vandenberghe, *Convex Optimization*, section 9.3, page 475, for the measured
  claim that convergence "depends greatly on the condition number" and that above about
  1000 the gradient method "is so slow that it is useless in practice".
  `https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf`
