# 0408 - The geometry of the SVD

**Placeholder number.** Module M04, position 8. **Label:** `core`. **Rung:** working (`pill med`).

## The single tight idea

Every matrix does exactly three things to space in exactly this order: it rotates, it stretches each axis by a singular value, and it rotates again, so the unit sphere always comes out as an ellipsoid whose semi-axes are the singular values.

## Prerequisites, by page number

- `0407` the SVD and its existence proof
- `03xx` orthogonal matrices as rotations and reflections (M03)

## Beats, in order

1. Read `A = U Sigma V^T` right to left as three motions rather than three matrices: `V^T` turns the input frame, `Sigma` stretches along the turned axes and changes dimension, `U` turns the result into the output frame.
2. Insist on the order and on which space each rotation happens in. `V^T` acts in the input space, `U` in the output space, and when the matrix is not square those are not the same space at all. This is the concrete meaning of "two bases" from `0407`.
3. **The ellipsoid result** and its proof (below). This is the page's payload: the picture is a theorem, not an analogy.
4. `sigma_1` is the largest stretch any unit vector receives, and `sigma_n` the smallest. So the singular values bracket what the matrix can do to a vector's length. Name `sigma_1` as the spectral norm and say what it measures.
5. The ratio `sigma_1 / sigma_n` says how differently the matrix treats its best and worst directions. A ratio near one means the ellipsoid is nearly a sphere; a large ratio means a long thin sliver. Name it the condition number, and state in one sentence where it bites: a matrix with a large ratio turns a small change in the input into a large change in the answer. M06 owns what that does to gradient descent; the SVD route on page `0410` avoids the problem rather than solving it.
6. What `Sigma` does when the matrix is not square: with more rows than columns it embeds a lower-dimensional ellipsoid in a bigger space; with more columns than rows it flattens, and the directions with `sigma = 0` are crushed to the origin. Those crushed directions are the null space, already met on `0407` beat 8.
7. Contrast with the eigendecomposition, geometrically rather than algebraically: `P D P^-1` changes basis, scales, then changes *back*, so it is one coordinate system used twice. The SVD uses two different ones and never undoes the first. That is why the SVD can describe a map between spaces of different dimension and the eigendecomposition cannot.
8. Determinant as a by-product: for a square matrix, `|det(A)| = sigma_1 sigma_2 ... sigma_n`, because rotations preserve volume and only `Sigma` changes it. The sign the determinant carries is orientation, which `Sigma` cannot express, which is why the absolute value is there.

## Named theorem and its stated proof (D4)

**Theorem (the image of the sphere).** Let `A` be `m x n` with SVD `A = U Sigma V^T` and singular values `sigma_1 >= ... >= sigma_n >= 0`. The image of the unit sphere in the input space is the ellipsoid whose axes point along `u_1, ..., u_n` and whose semi-axis lengths are `sigma_1, ..., sigma_n`.

**Proof.** Take any unit vector `x`. Because `V` is orthogonal it maps the unit sphere onto itself, so write `x = V y` where `y` is also a unit vector, and every unit `y` arises this way exactly once. Then
`A x = U Sigma V^T V y = U Sigma y`,
using `V^T V = I`. Write `z = Sigma y`, so that `z_i = sigma_i y_i`. Then `A x = U z`, and because `U` is orthogonal it preserves lengths and angles, so the shape traced by `A x` is the shape traced by `z`, merely re-expressed in the `u` basis.
Now ask what shape `z` traces. For every `i` with `sigma_i > 0` we have `y_i = z_i / sigma_i`, and since `y` is a unit vector, `sum_i y_i^2 = 1`, giving
`sum_i (z_i / sigma_i)^2 = 1`,
which is exactly the equation of an ellipsoid with semi-axis `sigma_i` along coordinate `i`. Transporting it by `U` puts those axes along `u_1, ..., u_n`.

**The step that does the real work.** `x = V y` at the start. It is legitimate only because `V` is orthogonal and therefore maps the unit sphere onto the whole unit sphere, losing nothing and adding nothing. That single substitution is what converts a statement about all unit `x` into a statement about the coordinates `Sigma` happens to be diagonal in. Everything after it is reading off an equation.

**The honest boundary.** When some `sigma_i = 0` the "ellipsoid" is degenerate: it is flat in those directions, an ellipse living inside a higher-dimensional space rather than a solid body. The equation above simply drops those terms, and the page draws the degenerate case rather than hiding it. For `m > n` the image is likewise an `n`-dimensional ellipsoid sitting inside `m`-dimensional space, which is not a defect and is exactly what a tall data matrix does.

## Planned figures

1. **Orientation figure**, `flowchart LR`: `The SVD (0407)` feeds `THIS PAGE - what the three factors do to space`, which feeds `Low-rank approximation (0409)` and, out of module, `Conditioning and convergence (M06)`.
2. **`svg.chart`, required floor, four panels.** The unit circle with two marked vectors; after `V^T` (rotated, marks moved to the axes); after `Sigma` (stretched into an axis-aligned ellipse with semi-axes labelled `sigma_1` and `sigma_2`); after `U` (rotated into final position). The two marked vectors are traceable through all four panels. Kills: the SVD as "three matrices" instead of three motions.
3. **`svg.chart`.** Two ellipses from two matrices with the same `sigma_1` but very different `sigma_2`: one nearly circular, one a thin sliver, with the ratio annotated on each. Kills: not feeling what a condition number is.
4. **`flowchart LR`.** Eigendecomposition drawn as `basis change, scale, basis change BACK` in one space, beside SVD drawn as `basis change in the input space, scale, different basis change in the output space`. Kills: thinking the SVD is the eigendecomposition with extra steps.

## The worked example, in eight parts

`A = [[1, 0.8], [0, 1]]`, a shear. Chosen because it is the matrix `0406` showed cannot be diagonalised usefully, so the reader watches the SVD succeed exactly where the eigendecomposition failed.

1. **Goal.** Describe what this shear does to the unit circle, given that its eigen-story is degenerate.
2. **Recall the failure.** Its only eigenvalue is `1`, twice, with a single eigendirection `(1,0)`. The eigendecomposition says almost nothing about it.
3. **Form the Gram matrix.** `A^T A = [[1, 0.8], [0.8, 1.64]]`.
4. **Diagonalise it.** `trace = 2.64`, `det = 1.64 - 0.64 = 1`, so `lambda^2 - 2.64 lambda + 1 = 0`, discriminant `6.9696 - 4 = 2.9696`, roots `(2.64 +/- 1.7233)/2`, giving `2.1817` and `0.4583`.
5. **Singular values.** `sigma_1 = sqrt(2.1817) = 1.4770` and `sigma_2 = sqrt(0.4583) = 0.6770`.
6. **Read the geometry.** The unit circle becomes an ellipse with semi-axes `1.4770` and `0.6770`. The shear stretches its best direction by about 48 percent and squeezes its worst by about 32 percent, and the two directions are perpendicular, unlike the single eigendirection.
7. **Sanity check (`.p-check`).** `det(A) = 1`, and `sigma_1 sigma_2 = 1.4770 x 0.6770 = 1.0000`. A shear preserves area, so the ellipse has the same area as the circle even though it is nowhere near circular. Also `sigma_1^2 + sigma_2^2 = 2.1817 + 0.4583 = 2.64`, matching the sum of squared entries `1 + 0.64 + 0 + 1`.
8. **What changes if.** Increase the shear to `[[1, 5], [0, 1]]`. The determinant is still `1` and the eigen-story is still `lambda = 1` twice, so both of those are blind to the change. The singular values move to about `5.1926` and `0.1926`, a ratio of about 27. The SVD sees a violent distortion where the eigenvalues see nothing at all.

## Quiz seeds

**Q1, tests a misconception.** A 2x2 matrix has `det = 1`. What does that say about how it distorts the unit circle? Answer: only that the area is preserved, and it can still be stretched arbitrarily in one direction and squeezed in the other. Distractors: the circle maps to a circle (the trap, true only when the singular values are equal); the singular values are both 1 (true only in that same special case); the matrix is a rotation (a rotation has `det = 1`, but so do infinitely many other matrices).

**Q2.** In `A = U Sigma V^T` applied to a vector, which factor acts first and in which space? Answer: `V^T`, in the input space. Distractors: `U`, in the input space (right factor, wrong space and wrong order); `Sigma`, because the stretch is the essential part (a value judgement, not the order); `U`, because matrix products read left to right (states the false rule that causes the error).

## Practice seeds

**P1.** For `A = [[3, 0], [0, 1]]`, describe the image of the unit circle, then do the same for `B = [[0, -1], [1, 0]]`, and say which one the determinant distinguishes.
*Hint:* Both matrices are already easy: one is diagonal, and the other is a rotation.
*Solution:* `A^T A = diag(9, 1)`, so `sigma = 3` and `1`: the circle becomes an ellipse with semi-axes 3 and 1 along the coordinate axes. `B^T B = I`, so both singular values are `1`: the circle maps to itself, a quarter-turn. `det(A) = 3` and `det(B) = 1`, so the determinant does distinguish them here, but it distinguishes them by area only.
*`.p-check`:* For each, `sigma_1 sigma_2` should equal `|det|`: `3 x 1 = 3` and `1 x 1 = 1`. Both hold.

**P2, `depth`.** Show that `sigma_1` is the largest value `||Ax||` takes over all unit vectors `x`.
*Hint:* Use the substitution from the theorem's proof and ask which unit `y` makes `||Sigma y||` biggest.
*Solution:* With `x = V y` and `||y|| = 1`, the proof gave `||Ax|| = ||Sigma y||` because `U` preserves length. Now `||Sigma y||^2 = sum_i sigma_i^2 y_i^2`. Since `sum_i y_i^2 = 1`, this is a weighted average of the numbers `sigma_i^2` with weights summing to one, so it is at most the largest of them, `sigma_1^2`, and it attains that value by putting all the weight on the first coordinate, `y = e_1`. Undoing the substitution, the maximiser is `x = V e_1 = v_1`, and the value is `sigma_1`.
*`.p-check`:* On the worked shear, `A v_1` should have length `1.4770`. And no unit vector should beat it: sampling a few thousand random unit vectors must never exceed `sigma_1`, which is what `code/0408` asserts.

## Code and dataset plan

`code/0408-svd-geometry.py`. Dataset `datasets/spectra.csv`.

Computes twice:
1. **From the definition, by sampling.** Draw 100,000 random unit vectors in 24 dimensions, apply the centred data matrix's first two rows as a 2x24 map, and record the maximum and minimum of `||Ax||`.
2. **From the SVD.** Take `sigma_1` and `sigma_min` of that same map.
3. **Assert the sampled extremes fall inside the bracket** `[sigma_min, sigma_1]` and approach it as the sample grows, which is the executable form of beat 4 and of practice P2.

The program also verifies the three-motion reading directly: it applies `V^T`, then `Sigma`, then `U` in three separate steps and asserts the result equals `A x` to tolerance, and prints the length of the vector after each step so a reader can see length change only at the middle step. Finally it prints `|det|` against the product of singular values for a square submatrix, checking beat 8.

## Sources

- Deisenroth, Faisal and Ong, *MML*, Section 4.5.1, the SVD as sequential basis change, scaling and basis change. `https://mml-book.github.io/book/mml-book.pdf`
- Damle, Cornell CS 3220, "The Singular Value Decomposition". `https://www.cs.cornell.edu/courses/cs3220/2019fa/SVD.pdf`
