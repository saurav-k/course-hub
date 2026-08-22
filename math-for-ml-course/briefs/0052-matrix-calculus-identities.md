# 0052 - Six matrix-calculus identities, and the layout convention that breaks them

> Number claimed under #42 from the roadmap count in `../index.html`. Report label C13.

| | |
|---|---|
| Module | M05 Calculus, and it is the module's last page |
| Rung | frontier (`pill hard`) |
| Label | `depth` |
| Prerequisites | 0044, 0046, 0049. M03: matrix multiplication, transpose, the data matrix, and its L12 least-squares page. M04: quadratic forms. |
| Enables | M06's derivations, M09's estimator algebra, the M11 capstone |

## Provenance, which the writer needs to know

**This page is not in the M05 brief as originally scoped.** `mlm-audit-r1` section 4.3
moves it out of M04 and into M05 as the module's last page, to break a slice-level cycle:
M05's Hessian needs M04's quadratic forms, and M04's matrix-calculus identities need M05's
gradient. Moving one page breaks the cycle without splitting a module.

**M04's report still carries it as its Lesson 11**, because M04 finalised before r1's
report existed and says explicitly that r1 may re-slot its boundaries. Two reports
currently plan one page. This is an open question for the captain (scout report section
11, Q3). If the captain leaves it with M04, delete this brief and the module is eleven
pages; nothing else changes.

**M04's beats are sound and this brief adopts them** rather than inventing a rival
structure. The additions below are only what comes from sitting at the end of M05 rather
than the end of M04: the synthesis with M03's projection route, and the ridge beat.

## The single tight idea

Differentiate a loss written in matrix form once, instead of index by index, and the only
thing that reliably goes wrong is which layout convention you are in.

## Beats, in order

1. **Motivate.** A loss written with index sums takes a page to differentiate and a line
   in matrix form. Show both for the same loss.
2. **State the layout problem before the first identity, not after.** Numerator layout
   makes `d(scalar)/dx` a row; denominator layout makes it a column. Show one identity
   written both ways, from two sources that genuinely disagree, and say plainly that
   neither is wrong.
3. **The house rule, once, and held everywhere:** a gradient has the shape of the thing
   you differentiate by. This is the rule 0044 declared, and this page is where it earns
   its keep.
4. **The six identities, each with its shape check.**
5. **Worked, and it is the page's reason to exist:** `d/d theta ||y - X theta||^2` in
   three lines, arriving at `X^T X theta = X^T y`.
6. **The synthesis beat, which is why this page sits at the end of the module.** This is
   the same answer M03's L12 reached through the orthogonality principle, by a completely
   different route. M03 got there without calculus, on purpose. Put the two side by side
   and say what it means that they agree. Neither page re-derives the other.
7. **Trade-off.** The identities are a lookup table, and a lookup table is only safe if
   the shapes are checked. Give the shape check as a habit, not as an appendix.

## The six identities and their derivations

Under D4 each identity is a named result and owes a derivation. These are short, and
writing them out is what stops the page being a table the reader cannot audit.

Throughout, `x` is a column in `R^n`, `a` a constant column, `A` a constant matrix, and
the house rule applies: `d(scalar)/dx` is a column.

> **1. `d(a^T x)/dx = a`.**
> `a^T x = sum_k a_k x_k`, so `d/dx_i` picks out the single term with `k = i`, giving
> `a_i`. Stacking over `i` gives `a`.
>
> **2. `d(x^T A x)/dx = (A + A^T) x`, and `= 2 A x` when `A` is symmetric.**
> `x^T A x = sum_{j,k} A_{jk} x_j x_k`. Differentiating in `x_i`, the terms that survive
> are those with `j = i` (giving `sum_k A_{ik} x_k`) and those with `k = i` (giving
> `sum_j A_{ji} x_j`); the term with `j = k = i` is differentiated as `A_{ii} x_i^2`, whose
> derivative `2 A_{ii} x_i` is exactly the sum of the two contributions, so no term is
> double counted. Stacking gives `A x + A^T x`. When `A = A^T` this is `2 A x`.
>
> **3. `d(||x||^2)/dx = 2x`.** Identity 2 with `A = I`.
>
> **4. `d(A x)/dx = A`.** This one is a Jacobian, not a gradient: the output is a vector.
> Entry `(i, j)` is `d(sum_k A_{ik} x_k)/dx_j = A_{ij}`. So the Jacobian is `A` itself,
> shape `m x n` for `A` in `R^{m x n}`, exactly as 0046's shape rule says.
>
> **5. `d(||y - X b||^2)/db = -2 X^T (y - X b)`.**
> Expand: `||y - Xb||^2 = y^T y - 2 y^T X b + b^T X^T X b`. The first term is constant.
> The second is `-2 (X^T y)^T b`, so identity 1 gives `-2 X^T y`. The third has the
> symmetric matrix `X^T X`, so identity 2 gives `2 X^T X b`. Summing,
> `-2 X^T y + 2 X^T X b = -2 X^T (y - X b)`.
>
> **6. `d tr(A X)/dX = A^T`.**
> `tr(A X) = sum_i (A X)_{ii} = sum_{i,k} A_{ik} X_{ki}`. Differentiating in `X_{pq}` keeps
> the single term with `k = p` and `i = q`, giving `A_{qp}`. So entry `(p, q)` of the
> derivative is `A_{qp}`, which is `A^T`.

**And the theorem the page is really for.**

> **The normal equations.** For `X` in `R^{n x p}` of full column rank, the unique
> minimiser of `||y - X b||^2` satisfies `X^T X b = X^T y`.
>
> *Proof.* By identity 5 the gradient is `-2 X^T (y - X b)`, which vanishes exactly when
> `X^T X b = X^T y`. The Hessian is `2 X^T X` by identity 2, and for any non-zero `h`,
> `h^T (X^T X) h = ||X h||^2 > 0` because full column rank means `X h != 0`. So the
> Hessian is positive definite, the loss is strictly convex, and the single critical point
> is the unique global minimum by 0049's Theorem 2. **QED**
>
> **The same theorem, M03's way, in one line for the comparison beat.** The minimiser of
> `||y - Xb||` is the point of the column space closest to `y`, and the closest point is
> the orthogonal projection, so the residual `y - Xb` must be perpendicular to every
> column of `X`, that is `X^T (y - X b) = 0`. Identical equation, no derivative anywhere.

## Figures

1. **Orientation, `flowchart LR`.** "The gradient and the Jacobian (0044, 0046)" into
   "THIS PAGE: doing it in matrix form, once" into "every derivation in M06 and M09", with
   "M03 L12, the same answer without calculus" dotted in.
2. **`flowchart TB`.** The layout fork drawn as a fork: one identity, two branches, two
   shapes, both labelled correct, and under each the shape check that catches a mistake.
   *Kills:* "one of these conventions is wrong". Neither is, and the bug is mixing them.
3. **`svg.chart`.** A shape ledger drawn as nested rectangles: operand shapes on one side,
   derivative shape on the other, for all six identities. Not a table, a picture, so a
   reader can pattern-match rather than look up.
   *Kills:* the transposed-gradient bug, which is the only bug this page exists to prevent.
4. **`flowchart LR`.** Two routes to `X^T X theta = X^T y`, M03's orthogonality route and
   this page's calculus route, converging on one node.
   *Kills:* "these are two different results".

## Worked example, in eight parts

1. **Setting.** M03 already told the reader the least-squares fit satisfies
   `X^T X theta = X^T y`, by dropping a perpendicular. Get there again, from the other end.
2. **Symbolic.** `.math` for `L(theta) = ||y - X theta||^2` with a `.gloss` naming `y`,
   `X`, `theta`, `n`, `p`, and stating the rows-as-samples convention explicitly.
3. **Picture.** Figure 4, the two routes, before either is walked.
4. **`ol.worked`.** Expand. Differentiate term by term with identities 1 and 2. Set to
   zero. Then solve on the real table and compare with the projection route.
5. **`.keynum`** on nothing: derived here.
6. **Sanity check.** `X^T X` must be symmetric, and its determinant must be non-zero for
   the solve to be unique. For the five-parameter housing table both hold, and the fitted
   coefficients must land near the rule the dataset was generated from:
   area `0.152`, bedrooms `11.0`, age `-0.85`, lot `0.021`. They do.
7. **What changes if** you switch to numerator layout in step 4? Every gradient becomes a
   row, both identities transpose, and the final line reads `theta^T X^T X = y^T X`, which
   is the same equation. Nothing about the answer changes; only the shape of every
   intermediate does. That is the page's whole argument about conventions, made once, on a
   result the reader already trusts.
8. **In words.** Geometry says the residual must be perpendicular to everything you can
   fit. Calculus says the loss must stop changing. They are the same statement, and a
   reader who sees both stops thinking of least squares as a formula.

## Quiz seeds

**Q1, misconception.** Two textbooks give different shapes for `d(a^T x)/dx`. What follows?
*Answer:* nothing about correctness. They are in different layout conventions and each is
right inside its own.
*Distractors:* "one of them has a typo" is the trap and is what most readers conclude;
"the derivative depends on whether `a` is a row or a column" confuses the operand with the
layout; "transpose whichever one disagrees with your code" is advice rather than an
explanation, and it is how the bug survives.

**Q2.** M03 derives `X^T X theta = X^T y` from perpendicularity and this page derives it
from a gradient. What is the relationship between the two results?
*Answer:* they are the same equation, reached by disjoint routes, and neither is an
approximation of the other.
*Distractors:* "the calculus one is more general" is a true-sounding claim about a
different question, since the projection argument holds in any inner-product space; "the
projection one needs full rank and the calculus one does not" is false, both do; "they
agree only for centred data" is simply false.

## Practice seed

**Stem.** Differentiate `L(theta) = ||y - X theta||^2 + lambda ||theta||^2` with respect
to `theta`, set it to zero, and solve. Then say in one sentence what `lambda` does to the
Hessian.

**Hint.** Exactly two identities, plus `||theta||^2 = theta^T I theta`. No new machinery.

**Solution.** The gradient is `-2 X^T y + 2 X^T X theta + 2 lambda theta`, so
`(X^T X + lambda I) theta = X^T y` and `theta = (X^T X + lambda I)^-1 X^T y`. The Hessian
becomes `2(X^T X + lambda I)`, so every eigenvalue rises by `2 lambda`. The smallest one
moves furthest in relative terms, which is why ridge regression conditions a badly
conditioned problem.

**`.p-check`.** At `lambda = 0` the answer must collapse to the ordinary normal
equations, and it does. As `lambda` grows without bound `theta` must tend to zero, and it
does. Either limit failing means a sign is wrong.

**Boundary, and the page must say it.** The **geometry** of L2 regularisation, the ball
and the contour, is M06's under r1 edge 26, and the **statistics**, L2 as a Gaussian prior
under MAP, is M09's. This problem is neither. It is a shape-checked differentiation whose
by-product happens to be the ridge estimator, and the page links both ways.

## Code and dataset

`../code/m05_13_matrix_calculus.py` against `../datasets/m05-housing.csv`. Every one of
the six identities is checked against a finite-difference derivative, then the normal
equations are solved twice, once by the calculus route and once by the projection route,
and the residual is checked for perpendicularity.

Verified output to quote: the six identities agree with the definition to between
`1.1e-10` and `2.5e-09`; the two routes to the normal equations agree to between
`5.9e-16` and `1.3e-12` on all five coefficients; the fitted values are intercept
`41.83`, area `0.15166`, bedrooms `10.478`, age `-0.84937`, lot `0.021063` against a
generating rule of `40, 0.152, 11.0, -0.85, 0.021`; `max |X^T r| = 6.59e-06`, so the
residual is perpendicular to every column; and ridge at `lambda = 10,000` drops `kappa`
from `1.22e9` to `5.99e7` while `||theta||` falls from `43.13` to `5.45`.

## Sources

- Deisenroth, Faisal and Ong, *Mathematics for Machine Learning*, sections 5.4 and 5.5 for
  gradients of matrices and the useful identities, and section 9.2 for the least-squares
  gradient and the normal equations. **Note the slip flagged in brief 0049**: section 9.2
  states the Hessian of `||y - X theta||^2 / (2 sigma^2)` is `X^T X`, dropping the
  `1/sigma^2`. `https://mml-book.github.io/book/mml-book.pdf`
- Goodfellow, Bengio and Courville, *Deep Learning*, section 4.3.1, for the Jacobian and
  Hessian definitions the shape checks rely on.
  `https://www.deeplearningbook.org/contents/numerical.html`
