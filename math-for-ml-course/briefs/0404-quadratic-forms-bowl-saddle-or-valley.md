# 0404 - Quadratic forms: reading a matrix as a bowl, a saddle or a valley

**Placeholder number.** Module M04, position 4. **Label:** `core`. **Rung:** working (`pill med`).

## The single tight idea

Feeding a vector into `x^T A x` turns a symmetric matrix into a surface over the input space, and the signs and sizes of its eigenvalues say exactly what shape that surface is.

## Prerequisites, by page number

- `0403` the spectral theorem
- `03xx` the dot product and matrix-vector products (M03)

Calculus-free by design. M05 owns the Hessian as a matrix of second partial derivatives, and M06 owns "a positive definite Hessian means a local minimum". This page owns the surface and nothing about derivatives.

## Beats, in order

1. From a matrix to a number: `q(x) = x^T A x` takes a vector in and returns one scalar. Evaluate it at three points by hand before any theory, so the reader sees it is just arithmetic.
2. Expand it for a 2x2 and get `a x_1^2 + 2b x_1 x_2 + d x_2^2`. Name the cross term. The cross term is the whole difficulty and everything after this removes it.
3. Only the symmetric part matters: for any `A`, `x^T A x = x^T ((A + A^T)/2) x`, because a number equals its own transpose. So assuming symmetry costs nothing, and page `0403` therefore applies to every quadratic form.
4. Rotate into the eigenbasis. Substituting `x = Q y` gives `q = y^T Lambda y = lambda_1 y_1^2 + ... + lambda_n y_n^2`. **No cross terms.** This is the payoff of `0403` and the reason anyone diagonalises anything.
5. The three shapes, read straight off the signs: all eigenvalues positive is a bowl, mixed signs is a saddle, a zero eigenvalue is a flat direction along the floor of a valley.
6. The level set `x^T A x = 1`. In the eigenbasis it is `sum lambda_i y_i^2 = 1`, so along eigenvector `i` it reaches `y_i = 1 / sqrt(lambda_i)`. **A large eigenvalue gives a short axis.**
7. **The trap, stated in the same breath, because separating them is what causes the error.** The data cloud whose covariance is `A` spreads by `sqrt(lambda_i)` along eigenvector `i`, so there a large eigenvalue gives a **long** axis. Two ellipses, from one matrix, behaving oppositely. Both are correct about different objects and the page draws them side by side.
8. One real quadratic form worked as a use rather than an exercise: the graph Laplacian, where `f^T L f` equals half the sum over edges of `w_ij (f_i - f_j)^2`, so the form literally scores how unsmooth a labelling is across a graph.

## Named result and its stated proof (D4)

**Result (principal axes).** For symmetric `A`, the substitution `x = Q y` with `Q` the orthonormal eigenvector matrix turns `x^T A x` into `lambda_1 y_1^2 + ... + lambda_n y_n^2`, a sum with no cross terms.

**Proof.** By `0403`, `A = Q Lambda Q^T` with `Q^T Q = I`. Substitute `x = Q y`:
`x^T A x = (Q y)^T (Q Lambda Q^T) (Q y) = y^T Q^T Q Lambda Q^T Q y = y^T Lambda y`,
using `Q^T Q = I` twice. Because `Lambda` is diagonal, `y^T Lambda y = sum_i lambda_i y_i^2`.

**The step that does the real work:** `Q^T Q = I` collapsing in the middle. It is available only because the eigenvectors are *orthonormal*, which is precisely what symmetry bought on `0403`. For a non-symmetric matrix the change of basis would leave a `P^-1` that does not cancel and the cross terms would survive.

**A note on what the substitution is.** `x = Q y` is a rotation of the coordinate system, not a change to the surface. The bowl does not move; the reader's axes turn to line up with it. The page says this, because "diagonalising changed my data" is a real misreading.

## Planned figures

1. **Orientation figure**, `flowchart LR`: `Spectral theorem (0403)` feeds `THIS PAGE - x^T A x as a surface`, which feeds `Positive definiteness (0405)`, and out of module to `Loss surfaces (M05)` and `Convexity (M06)`.
2. **`svg.chart`, required floor.** Three level-set panels on shared axes: `[[5,2],[2,2]]` (concentric ellipses, a bowl), `[[1,2],[2,1]]` (hyperbolas, a saddle), `[[1,2],[2,4]]` (parallel lines, a flat valley). Each annotated with its eigenvalue signs. Kills: "indefinite" as jargon rather than a picture.
3. **`svg.chart`.** The same quadratic before and after the rotation: tilted ellipse with the cross term written beside it, then axis-aligned with the cross term gone and the two parabolas `6 y_1^2` and `1 y_2^2` drawn underneath. Kills: not seeing why anyone bothers to diagonalise.
4. **`svg.chart`, the trap.** Two ellipses side by side from the same `S = [[5,2],[2,2]]`. Left, the level set `x^T S x = 1`, semi-axes `1/sqrt(6) = 0.408` and `1/sqrt(1) = 1`, so the big eigenvalue gives the **short** axis. Right, a scatter of points with covariance `S`, spreading `sqrt(6) = 2.449` and `sqrt(1) = 1`, so the big eigenvalue gives the **long** axis. Kills: the single most reversed fact in the module.
5. **`quadrantChart`.** Eigenvalue signs against surface type, placing bowl, dome, saddle and valley.

## The worked example, in eight parts

`S = [[5, 2], [2, 2]]`, continued from `0403` so the eigen-work is already trusted.

1. **Goal.** Say what shape `q(x) = x^T S x` is, and where its level set reaches furthest.
2. **Write it out.** `q(x) = 5 x_1^2 + 4 x_1 x_2 + 2 x_2^2`. The `4` is `2b` with `b = 2`.
3. **Evaluate three points.** `q(1,0) = 5`. `q(1,1) = 5 + 4 + 2 = 11`. `q(1,-2) = 5 - 8 + 8 = 5`. All positive so far, which is a hint and not a proof.
4. **Bring in the eigenvalues from `0403`:** `6` and `1`, with `q_1 = (2,1)/sqrt(5)` and `q_2 = (1,-2)/sqrt(5)`.
5. **Rotate.** In the eigenbasis, `q = 6 y_1^2 + 1 y_2^2`. Both coefficients positive, so it is a bowl and `q(x) > 0` for every non-zero `x`. The hint from step 3 is now a proof.
6. **Level set.** `6 y_1^2 + y_2^2 = 1` reaches `y_1 = 1/sqrt(6) = 0.408` along `q_1` and `y_2 = 1` along `q_2`. The ellipse is **short** along the direction with eigenvalue 6.
7. **Sanity check (`.p-check`).** Evaluate `q` at the two ellipse points. Along `q_1` at distance `0.408`: `6 (0.408)^2 = 0.999`, which is 1 to rounding. Along `q_2` at distance 1: `1 (1)^2 = 1`. Both land on the level set, so the semi-axis formula is right way up. Getting `2.449` and `1` instead means `sqrt(lambda)` was used where `1/sqrt(lambda)` belongs, which is beat 7's trap.
8. **What changes if.** Change `S` to `[[1,2],[2,1]]`. Then `trace = 2`, `det = -3`, eigenvalues `3` and `-1`. Now `q(1,1) = 1 + 4 + 1 = 6` is positive while `q(1,-1) = 1 - 4 + 1 = -2` is negative. One matrix, both signs: a saddle. Nothing about the method changed, only the eigenvalue signs.

## Quiz seeds

**Q1, tests a misconception.** For a positive definite `A`, along the eigenvector with the **largest** eigenvalue the level set `x^T A x = 1` is: Answer: shortest, because the semi-axis is `1/sqrt(lambda)`. Distractors: longest (the trap, true of the data cloud and not of the level set); unchanged (contradicts the equation); undefined there (not a real constraint). Feedback must name the data-cloud ellipse as the object the wrong answer is true about.

**Q2.** A symmetric matrix has eigenvalues `+4` and `-1`. What shape is `x^T A x`? Answer: a saddle. Distractors: a bowl (needs both positive); a flat plane (needs a zero eigenvalue, and `4` and `-1` do not cancel); a dome (needs both negative).

## Practice seeds

**P1.** For `A = [[2, -1], [-1, 2]]`, write `q(x)` out in full, find the eigenvalues, say what shape it is, and give both semi-axes of `x^T A x = 1`.
*Hint:* `trace` and `det` give the eigenvalues with no expansion.
*Solution:* `q(x) = 2 x_1^2 - 2 x_1 x_2 + 2 x_2^2`. `trace = 4`, `det = 3`, so `lambda^2 - 4 lambda + 3` and roots `3` and `1`. Both positive, so a bowl. Semi-axes `1/sqrt(3) = 0.577` along the eigenvector for `3`, which is `(1,-1)/sqrt(2)`, and `1` along `(1,1)/sqrt(2)`.
*`.p-check`:* Evaluate at `(1,-1)/sqrt(2)` scaled to length `0.577`: the vector is `(0.408, -0.408)`, and `q = 2(0.1667) - 2(-0.1667) + 2(0.1667) = 0.333 + 0.333 + 0.333 = 1.0`. On the level set, so the axes are the right way up.

**P2, `depth`.** For the path graph on five nodes with unit weights, compute `f^T L f` for `f = (1,2,3,4,5)` and for `f = (1,5,1,5,1)`, and say what the comparison means.
*Hint:* Use `f^T L f = sum over edges of (f_i - f_j)^2`. On a path there are four edges and you never have to build `L`.
*Solution:* Ramp: each of the four edge differences is `1`, so the sum is `4`. Alternating: the differences are `-4, 4, -4, 4`, each squaring to `16`, so the sum is `64`. The form has scored the alternating labelling sixteen times rougher.
*`.p-check`:* `f^T L f` can never be negative, because it is a sum of squares. If either answer came out negative, `L` was built with the wrong sign; it is `D - W`, not `W - D`.

## Code and dataset plan

`code/0404-quadratic-forms.py`. Dataset `datasets/spectra.csv`.

Computes twice:
1. **From the definition.** Take the 24x24 channel covariance `S`. Evaluate `x^T S x` directly for a batch of 10,000 random unit vectors, and report the minimum and maximum values found.
2. **From the spectrum.** Compute the smallest and largest eigenvalues of `S`.
3. **Assert they agree**: the sampled minimum is at or above `lambda_min` and the sampled maximum is at or below `lambda_max`, and both come close as the sample grows. This is the executable form of beat 5, and it also previews the Rayleigh quotient that M06 will use for the variational route to PCA, named but not derived here.

It also prints the same quantity computed after the rotation `x = Q y`, confirming the cross terms are gone: the off-diagonal mass of `Q^T S Q` is reported and asserted near zero.

## Sources

- Deisenroth, Faisal and Ong, *MML*, Section 3.2.3 and Chapter 4. `https://mml-book.github.io/book/mml-book.pdf`
- von Luxburg, "A Tutorial on Spectral Clustering", arXiv:0711.0189, Proposition 1, for the Laplacian identity in beat 8. `https://arxiv.org/pdf/0711.0189`
