# 0049 - Curvature is the second derivative, and the Hessian holds it for every direction at once

> Number claimed under #42 from the roadmap count in `../index.html`. Report label C09.

| | |
|---|---|
| Module | M05 Calculus |
| Rung | frontier (`pill hard`) |
| Label | `core` |
| Prerequisites | 0044. M04: symmetric matrices, eigenvalues and eigenvectors, positive definiteness, quadratic forms. |
| Enables | 0050, and M06's L08 and L09 |

## The single tight idea

The gradient promises a decrease and the curvature says whether the promise will be kept.

## Boundary note, and it is an amendment

`mlm-audit-r1` edge 8 assigns "positive-definite Hessian implies a local minimum" to M06.
But r1's own module order puts M05 before M06, and M06's saddle page opens by classifying
critical points from eigenvalue signs. **This page owns the test** and M06 owns its
consequences: that a positive-definite Hessian makes a Newton step well posed, and
everything about saddle prevalence, plateaus and what an optimiser does. The scout report
argues this as amendment A1 in its section 12.2. If the captain rules the other way, cut
beats 6 and 7 here and cross-link forward instead.

## Beats, in order

1. **The gradient at a point predicts a straight line.** The function is not a straight
   line. The gap is curvature, and it is the whole page.
2. **Three pictures side by side.** Negative curvature: the function falls faster than
   promised. Zero: exactly as promised. Positive: slower, and eventually uphill.
3. **In many dimensions there is a second derivative for every direction.** Collect them:
   the Hessian, `H[i][j] = d^2 f / d x_i d x_j`.
4. **Symmetry, with its hypothesis stated,** not assumed. See Theorem 1.
5. **The directional second derivative is `d^T H d`.** When `d` is an eigenvector it is
   the eigenvalue, and the extreme eigenvalues bracket every direction.
6. **The second-derivative test in full,** including the branch people forget.
7. **Worked: the Hessian of a real regression,** its eigenvalues, and the verdict.
8. **The honesty section, inherited from the withdrawn loss-surface page, as a
   `.callout.warn`.** A picture of a loss surface is not evidence unless it is
   filter-normalised, because rectified networks are scale-invariant in their weights and
   a network with large weights simply looks smoother.
9. **Forward pointer, one sentence and no teaching.** In high dimensions a critical point
   is almost never a minimum. M06's L09 owns that argument. This page owns only the test
   that makes it sayable.

## Named theorems and their stated proofs

**Theorem 1 (Schwarz, or Clairaut).**

> If `f : R^n -> R` has second partial derivatives `d^2 f / dx_i dx_j` and
> `d^2 f / dx_j dx_i` in a neighbourhood of `a` and both are continuous at `a`, then they
> are equal at `a`. Consequently the Hessian is symmetric wherever the second partials
> are continuous.
>
> *Proof (two variables; the general case fixes the other coordinates and reduces to it).*
> Fix `a = (p, q)` and for small `h, k != 0` define the second difference
>
>   `D(h,k) = f(p+h, q+k) - f(p+h, q) - f(p, q+k) + f(p, q)`.
>
> Let `phi(x) = f(x, q+k) - f(x, q)`. Then `D = phi(p+h) - phi(p)`, and the mean value
> theorem gives `D = h phi'(p + s h)` for some `s` in `(0,1)`, that is
> `D = h [f_x(p + s h, q + k) - f_x(p + s h, q)]`. Applying the mean value theorem again,
> now in the second argument to `f_x`, gives
>
>   `D = h k f_{yx}(p + s h, q + t k)` for some `t` in `(0,1)`.
>
> Running the identical argument with `psi(y) = f(p+h, y) - f(p, y)` first gives
>
>   `D = h k f_{xy}(p + s' h, q + t' k)` for some `s', t'` in `(0,1)`.
>
> Divide both by `h k` and let `(h,k) -> (0,0)`. Both interior points converge to `a`,
> and both mixed partials are continuous at `a`, so both sides converge to
> `f_{yx}(a)` and `f_{xy}(a)` respectively. Hence they are equal. **QED**
>
> **The hypothesis is not decoration.** Drop continuity and the conclusion fails. The
> standard witness is `f(x,y) = xy(x^2 - y^2)/(x^2 + y^2)` off the origin and `0` at it,
> for which `f_{xy}(0,0) = -1` and `f_{yx}(0,0) = +1`. Put it in a `.callout`, one line.
> Goodfellow states the continuity condition and then says most functions in deep
> learning satisfy it almost everywhere, which is the honest position and the one to take.

**Theorem 2 (the second-derivative test).**

> Let `f` be twice continuously differentiable and let `a` be a critical point, so
> `grad f(a) = 0`. Let `H` be the Hessian at `a`, with eigenvalues `l_1 <= ... <= l_n`.
> (i) If every `l_i > 0` then `a` is a strict local minimum.
> (ii) If every `l_i < 0` then `a` is a strict local maximum.
> (iii) If some `l_i > 0` and some `l_j < 0` then `a` is a saddle.
> (iv) If some `l_i = 0` and the non-zero eigenvalues share a sign, the test is silent.
>
> *Proof.* Taylor with remainder (0050, Theorem 1) at a critical point gives, for small `h`,
>
>   `f(a + h) = f(a) + (1/2) h^T H h + o(||h||^2)`,
>
> because the first-order term vanishes. Since `H` is real symmetric it has an orthonormal
> eigenbasis, and writing `h = sum c_i v_i` gives `h^T H h = sum l_i c_i^2`.
> **(i)** If all `l_i > 0` then `h^T H h >= l_1 ||h||^2 > 0`, so
> `f(a+h) - f(a) >= (l_1/2)||h||^2 + o(||h||^2)`, which is positive for all small enough
> non-zero `h` because the remainder is dominated. So `a` is a strict local minimum.
> **(ii)** Apply (i) to `-f`.
> **(iii)** Move along the eigenvector `v_i` with `l_i > 0`: `f` increases. Move along
> `v_j` with `l_j < 0`: `f` decreases. A point that is a minimum on one cross-section and
> a maximum on another is a saddle by definition.
> **(iv)** Along the eigenvector with `l = 0` the quadratic term contributes nothing and
> the sign of `f(a+h) - f(a)` is decided by the neglected `o(||h||^2)`, which the theorem
> says nothing about. Both outcomes occur: `f = x^2 + y^4` has a minimum at the origin and
> `f = x^2 - y^4` has a saddle, and both have Hessian `diag(2, 0)` there. **QED**
>
> Branch (iv) with its two witnesses is what turns the test from a rule into an
> understanding, and it is the branch every summary omits.

## Figures

1. **Orientation, `flowchart LR`.** "The gradient's promise (0044, 0045)" into "THIS PAGE:
   whether the promise is kept" into "the quadratic model (0050)" and "Newton-type
   methods (M06)".
2. **`svg.chart`.** Three panels: negative, zero and positive curvature, each with the
   true function solid, the gradient's straight-line prediction dashed, and the gap
   shaded. *Kills:* "the gradient tells you how far to go".
3. **`stateDiagram-v2`.** From `critical point`, four transitions labelled by the
   eigenvalue signature to `local minimum`, `local maximum`, `saddle`, and `inconclusive`.
   *Kills:* the reader who learned the test and forgot it has a failure case.
4. **`svg.chart`, quantitative, log axis.** The five Hessian eigenvalues of the housing
   loss before scaling and after. *Kills:* "condition number is an abstraction".
5. **`flowchart LR`, inherited from the withdrawn loss-surface page.** The
   filter-normalisation pipeline, with a second branch showing what an unnormalised plot
   claims. *Kills:* trusting any loss-surface picture that does not say how it was normalised.

## Worked example, in eight parts

1. **Setting.** The five-parameter housing regression. Is its critical point a minimum,
   and how badly conditioned is it?
2. **Symbolic.** `.math` for `H[i][j] = d^2 f/dx_i dx_j` and for `H = (2/n) X^T X`, with a
   `.gloss` naming every symbol including `n` and the shape of `X`.
3. **Picture.** Figure 2, then figure 3, before any eigenvalue.
4. **`ol.worked`.** Form `X^T X`, scale it, take eigenvalues, apply the test, divide the
   largest by the smallest.
5. **`.keynum`** on nothing: derived here from the committed dataset.
6. **Sanity check.** The eigenvalues of `(2/n) X^T X` must all be non-negative, because
   `h^T X^T X h = ||X h||^2 >= 0` for every `h`. A negative eigenvalue means the matrix
   was formed wrongly. And they must sum to the trace, which is a number you can compute
   independently in one line.
7. **What changes if** a column is duplicated? `X` loses rank, the smallest eigenvalue
   becomes exactly zero, and the test moves from branch (i) to branch (iv). The loss then
   has a flat valley of minimisers rather than one, which is the calculus statement of
   what collinearity does.
8. **In words.** The loss curves more than a billion times more steeply along one
   direction than another. The bowl is not a bowl; it is a canyon.

## Quiz seeds

**Q1.** At a critical point the Hessian has eigenvalues `+3`, `+1` and `-2`. What kind of
point is it?
*Answer:* a saddle.
*Distractors:* "a minimum" ignores the negative eigenvalue; "a maximum" ignores the two
positive ones; "inconclusive" is the answer only when a zero eigenvalue is present.

**Q2, misconception.** When is the multidimensional second-derivative test inconclusive?
*Answer:* when at least one eigenvalue is zero and every non-zero eigenvalue shares a sign.
*Distractors:* "when the Hessian is not symmetric" is a different problem; "when the
eigenvalues have mixed signs" is exactly the conclusive saddle case; "never in more than
one dimension" is backwards.

## Practice seed

**Stem.** For a two-feature squared-error loss with design matrix `X`: write
`H = 2 X^T X`, find its eigenvalues for the five-house table, classify the critical point,
and compute the condition number.

**Hint.** For a symmetric `2 x 2` you do not need a solver: the eigenvalues are the roots
of `l^2 - (trace) l + (determinant) = 0`.

**Solution.** For the centred five-house table, `H` has eigenvalues `0.6` and `5,000,005`.
Both positive, so the critical point is a local minimum, and because the loss is quadratic
it is the global one. `kappa = 5,000,005 / 0.6 = 8.33e6`.

**`.p-check`.** The two eigenvalues must sum to the trace of `H`. Compute the trace
independently and check. If they do not sum to it, the quadratic was solved wrongly.

## Code and dataset

`../code/m05_09_hessian_test.py` against `../datasets/m05-housing.csv`. It verifies
Schwarz numerically on three index pairs, checks `d^T H d` against a second central
difference along random rays, and runs the classifier on the housing loss and on four
constructed surfaces that exercise every branch of the test.

Verified output to quote: the analytic Hessian is exactly symmetric and all three numeric
mixed-partial pairs agree to `0.00e+00`; the five eigenvalues are
`1.2916e-01, 9.4741e-01, 6.0993e+02, 7.4028e+05, 1.5742e+08` giving
`kappa = 1,218,855,367.6`; every random-direction `d^T H d` matches its second central
difference and lies inside the eigenvalue bracket; and the verdict is **local minimum**.

**A correction worth recording, because it was found by running the code.** A first
version used a tolerance of `1e-9` times the largest eigenvalue to decide when an
eigenvalue counts as zero. On a Hessian with `kappa = 1.2e9` that threshold is `0.157`
and the smallest true eigenvalue is `0.129`, so a genuinely positive definite matrix was
classified "inconclusive". The tolerance must be tied to machine epsilon, not to a
fraction of the spectrum. With `eps * n * lambda_max = 1.75e-07` the smallest eigenvalue
clears it by a factor of `738,988` and the verdict is correct. **Put this in the page as a
`.callout.warn`:** on a badly conditioned Hessian, "is this eigenvalue zero" is a
numerical question and not only a mathematical one.

## Sources

- Goodfellow, Bengio and Courville, *Deep Learning*, section 4.3.1, for the Hessian's
  definition, for the Hessian as the Jacobian of the gradient, for the commutativity
  condition and the resulting symmetry, for `d^T H d` and the eigenvalue bracket, for the
  full four-branch second-derivative test including the inconclusive case, and for the
  condition number's effect on gradient descent.
  `https://www.deeplearningbook.org/contents/numerical.html`
- Deisenroth, Faisal and Ong, *Mathematics for Machine Learning*, section 5.7, for the
  Hessian as the collection of second partials and for the symmetry statement.
  **Note a slip in that section not to copy:** it defines
  `L(theta) = ||y - X theta||^2 / (2 sigma^2)` and then states the Hessian is `X^T X`,
  dropping the `1/sigma^2`. The conclusion survives because `sigma^2 > 0`, but the
  arithmetic does not. `https://mml-book.github.io/book/mml-book.pdf`
- Li, Xu, Taylor, Studer and Goldstein, "Visualizing the Loss Landscape of Neural Nets",
  arXiv:1712.09913, for filter normalisation and for the scale-invariance argument that
  makes unnormalised loss-surface plots incomparable.
  `https://ar5iv.labs.arxiv.org/html/1712.09913`
