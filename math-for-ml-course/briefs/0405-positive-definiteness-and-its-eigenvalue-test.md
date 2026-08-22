# 0405 - Positive definiteness and its eigenvalue test

**Placeholder number.** Module M04, position 5. **Label:** `core`. **Rung:** working (`pill med`).

## The single tight idea

A symmetric matrix is positive definite exactly when all its eigenvalues are positive, which is the matrix version of "this number is positive" and is what makes a bowl a bowl.

## Prerequisites, by page number

- `0403` the spectral theorem
- `0404` quadratic forms and the three shapes

M06 owns "a positive definite Hessian implies a local minimum". M08 owns "a covariance matrix is positive semidefinite" as a statistical statement. This page owns the linear algebra: the definition, the eigenvalue test, and the `R^T R` characterisation.

## Beats, in order

1. Definition, from `0404`'s bowl: `A` is positive definite when `x^T A x > 0` for every non-zero `x`. Positive semidefinite replaces `>` with `>=`.
2. Name the terminology clash once and move on: parts of the mathematics literature call the semidefinite case simply "positive". This course always writes definite or semidefinite and never bare "positive" for a matrix.
3. **The eigenvalue test** and its proof (below). This is the workable criterion and everything else on the page is a consequence or a shortcut.
4. Why the definition alone is unusable: it quantifies over infinitely many `x`. The eigenvalue test replaces "check every vector" with "check `n` numbers".
5. **The `R^T R` fact, in one line.** For any real `X`, `x^T (X^T X) x = (Xx)^T (Xx) = ||Xx||^2 >= 0`. So every Gram matrix is positive semidefinite, free, with no eigenvalue computation. Every covariance matrix and every kernel matrix is of this form, so all of them are PSD.
6. Semidefinite but not definite, and what it means about the data: an eigenvalue of exactly zero is a direction with no spread at all, which is an exact linear dependence among the features. Show it by duplicating a column.
7. **The determinant trap.** `det(A) > 0` does **not** imply positive definite: in even dimensions two negative eigenvalues also give a positive determinant, and `[[-1,0],[0,-1]]` has determinant `+1`. The correct determinant-flavoured test is Sylvester's criterion, which requires **every** leading principal minor positive, not only the last.
8. Where it is a requirement rather than a bonus: a kernel matrix must be PSD for the kernel to define an inner product at all (M10 owns kernels). And the repair when a matrix is only semidefinite: adding `c I` shifts every eigenvalue up by `c`, which M06 will recognise as ridge regularisation. This page owns only the spectral fact, not the statistics.

## Named theorem and its stated proof (D4)

**Theorem.** Let `A` be real symmetric. Then `A` is positive definite if and only if every eigenvalue of `A` is strictly positive. The same statement holds with "semidefinite" and "non-negative".

**Proof.**

*If all eigenvalues are positive, then `A` is positive definite.* By `0403`, write `A = Q Lambda Q^T` with `Q` orthogonal. Take any `x != 0` and set `y = Q^T x`. Because `Q` is orthogonal it is invertible, so `y != 0` too. By `0404`'s principal-axes result, `x^T A x = sum_i lambda_i y_i^2`. At least one `y_i` is non-zero, its square is strictly positive, every `lambda_i` is strictly positive, and no term is negative. So the sum is strictly positive.

*If `A` is positive definite, then all eigenvalues are positive.* Let `lambda` be an eigenvalue with unit eigenvector `q`, which `0403` guarantees is real. Then `0 < q^T A q = q^T (lambda q) = lambda (q^T q) = lambda`, since `q^T q = 1`. So `lambda > 0`.

**The step that does the real work.** In the forward direction, the fact that `y != 0` whenever `x != 0`. It holds because `Q` is invertible, and it is what stops the argument from silently allowing the all-zero `y` that would make the sum zero. In the reverse direction, the real work is that the definition applies to *every* non-zero vector, so it may be applied to an eigenvector in particular. That is the whole trick.

**The honest boundary.** Sylvester's criterion in beat 7 is stated, used, and not proved: its proof needs a determinant argument the course has not built. The page says so plainly rather than implying the reader missed a step.

## Planned figures

1. **Orientation figure**, `flowchart LR`: `Spectral theorem (0403)` and `Quadratic forms (0404)` feed `THIS PAGE - when the bowl always points up`, which feeds `Low-rank approximation (0409)` and `PCA (0410)`, and out of module to `Convexity (M06)` and `Kernels (M10)`.
2. **`svg.chart`, required floor.** Eigenvalue spectra as bar charts for three real matrices side by side: `[[5,2],[2,2]]` (bars at 6 and 1, both above the axis, definite); `[[1,2],[2,4]]` (bars at 5 and 0, one touching the axis, semidefinite); `[[1,2],[2,1]]` (bars at 3 and -1, one below the axis, indefinite). Kills: thinking definite and semidefinite differ by a technicality. One bar touching zero is the entire difference and it is visible.
3. **`svg.chart`.** The 24 eigenvalues of the `spectra.csv` channel covariance on a log axis, all strictly above zero, next to the same covariance computed after duplicating a channel, where the smallest eigenvalue drops to the floor of the plot. Kills: not connecting "collinear features" to "zero eigenvalue".
4. **`flowchart TD`.** The four tests as branches from one root, each leaf annotated with its cost and its failure mode, including the explicit dead end `det > 0` with `[[-1,0],[0,-1]]` attached to it. Kills: the determinant trap.

## The worked example, in eight parts

Two matrices side by side, `A_1 = [[9, 6], [6, 5]]` and `A_2 = [[9, 6], [6, 3]]`, which differ in one entry.

1. **Goal.** Decide definiteness for both, two different ways, and see which test is cheaper.
2. **Invariants.** `A_1`: `trace = 14`, `det = 45 - 36 = 9`. `A_2`: `trace = 12`, `det = 27 - 36 = -9`.
3. **The determinant read, for `A_2` only.** A negative determinant in 2x2 forces one eigenvalue of each sign, so `A_2` is indefinite and no further work is needed.
4. **Eigenvalues of `A_1`.** `lambda^2 - 14 lambda + 9 = 0`, discriminant `196 - 36 = 160`, roots `(14 +/- 12.6491)/2`, so `13.3246` and `0.6754`. Both positive, so `A_1` is positive definite.
5. **The other route for `A_1`, completing the square.** `9 x_1^2 + 12 x_1 x_2 + 5 x_2^2 = (3 x_1 + 2 x_2)^2 + x_2^2`. A sum of two squares, zero only when `x_2 = 0` and `3 x_1 = 0`, that is only at the origin. Positive definite, with no eigenvalue computed at all.
6. **The other route for `A_2`.** Try to complete the square: `9 x_1^2 + 12 x_1 x_2 + 3 x_2^2 = (3 x_1 + 2 x_2)^2 - x_2^2`. The minus sign is the failure, and it hands you a counterexample directly: take `3 x_1 + 2 x_2 = 0` and `x_2 = 1`, so `x = (-2/3, 1)`, giving `q = -1 < 0`.
7. **Sanity check (`.p-check`).** Test the counterexample against the original matrix: `q(-2/3, 1) = 9(4/9) + 12(-2/3) + 3 = 4 - 8 + 3 = -1`. Negative, confirming step 6. For `A_1`, the same vector gives `4 - 8 + 5 = 1 > 0`, as a positive definite matrix must.
8. **What changes if.** Set the lower right entry to exactly `4`, giving `[[9,6],[6,4]]` with `det = 0`. Now the square completes as `(3 x_1 + 2 x_2)^2` with nothing left over, which is zero along the whole line `3 x_1 + 2 x_2 = 0`. Semidefinite, not definite, and the zero eigenvalue's eigenvector is exactly that line.

## Quiz seeds

**Q1, tests a misconception.** A symmetric 2x2 has `det(A) = +4`. Is it positive definite? Answer: not necessarily, because two negative eigenvalues also multiply to a positive determinant. Distractors: yes, a positive determinant is the test (the trap); no, never (overcorrects); only if it is also invertible (a positive determinant already gives invertibility, so this answers a different question).

**Q2.** Why is `X^T X` positive semidefinite for every real `X`? Answer: because `x^T X^T X x` equals `||Xx||^2`, which cannot be negative. Distractors: because its diagonal entries are sums of squares (true, but proves only the diagonal); because it is symmetric and symmetric matrices are semidefinite (false, and `[[0,1],[1,0]]` refutes it); because its determinant is a square (false).

## Practice seeds

**P1.** Decide whether `A = [[4, 2], [2, 3]]` is positive definite, twice: once by eigenvalues and once by completing the square.
*Hint:* `trace` and `det` first. Then try to write `q(x)` as a sum of squares.
*Solution:* `trace = 7`, `det = 12 - 4 = 8`, so `lambda^2 - 7 lambda + 8`, discriminant `49 - 32 = 17`, roots `(7 +/- 4.1231)/2` = `5.5616` and `1.4384`. Both positive. Completing the square: `4 x_1^2 + 4 x_1 x_2 + 3 x_2^2 = (2 x_1 + x_2)^2 + 2 x_2^2`, a sum of squares vanishing only at the origin.
*`.p-check`:* `5.5616 + 1.4384 = 7.0000 = trace` and `5.5616 x 1.4384 = 8.0000 = det`. Both routes must agree that it is definite, and they do.

**P2, `depth`.** Show that if `A` is positive definite then `A` is invertible, and that `A^-1` is positive definite too.
*Hint:* Use the eigenvalue test in both directions, and page `0402`'s result about the eigenvalues of an inverse.
*Solution:* All eigenvalues are positive, so none is zero, so `det(A) = product of eigenvalues != 0` and `A` is invertible. By `0402`, the eigenvalues of `A^-1` are the reciprocals `1/lambda_i`, and the reciprocal of a positive number is positive. `A^-1` is symmetric because `(A^-1)^T = (A^T)^-1 = A^-1`. Symmetric with all eigenvalues positive is positive definite.
*`.p-check`:* For `A = [[9,6],[6,5]]`, `A^-1 = (1/9)[[5,-6],[-6,9]]`, whose trace is `14/9 = 1.5556` and this must equal `1/13.3246 + 1/0.6754 = 0.0751 + 1.4806 = 1.5556`. It does.

## Code and dataset plan

`code/0405-positive-definiteness.py`. Dataset `datasets/spectra.csv`.

Computes twice:
1. **From the definition, by sampling.** Draw 200,000 random non-zero vectors and evaluate `x^T S x` on the 24x24 channel covariance, recording the minimum. Sampling can only ever *fail* to find a negative value, and the program says so in a comment: this is evidence, not proof.
2. **From the spectrum.** Compute the smallest eigenvalue, which decides the question outright.
3. **Assert they are consistent** and print the gap, making the point that the cheap test is also the conclusive one.

The program then does the thing sampling cannot: it appends a duplicate of one channel, recomputes the covariance, and shows the smallest eigenvalue collapsing to within floating-point noise of zero while the sampled minimum stays stubbornly positive because a random vector almost never lands exactly on the null direction. It finishes by constructing that null direction explicitly and evaluating the form there, getting zero. That contrast is the executable form of beat 6 and of why "I sampled a lot and it was fine" is not a proof.

## Sources

- Axler, *LADR* 4e, results 7.34 and 7.38, including the terminology note in beat 2. `https://linear.axler.net/LADR4e.pdf`
- Deisenroth, Faisal and Ong, *MML*, Definition 3.4 and Section 3.2.3, including the `A_1`/`A_2` pair used in the worked example. `https://mml-book.github.io/book/mml-book.pdf`
