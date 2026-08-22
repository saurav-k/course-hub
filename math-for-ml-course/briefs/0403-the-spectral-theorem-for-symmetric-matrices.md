# 0403 - The spectral theorem for symmetric matrices

**Placeholder number.** Module M04, position 3. **Label:** `core`. **Rung:** working (`pill med`).

## The single tight idea

A real symmetric matrix always has a full set of eigenvectors that are mutually perpendicular and eigenvalues that are all real, and almost every matrix machine learning hands you is symmetric.

## Prerequisites, by page number

- `0401` eigenvalues and eigenvectors
- `0402` the characteristic equation
- `03xx` the dot product, orthogonality, and orthonormal bases (M03)
- `03xx` orthogonal matrices and `Q^-1 = Q^T` (M03)

## Beats, in order

1. Recap the three ways a general matrix disappoints, all met already: complex eigenvalues (`0402`), eigenvectors that are not perpendicular, and possibly too few of them.
2. Symmetry, defined in one line: `A = A^T`, the entries mirror across the diagonal.
3. State the theorem, as an equivalence rather than a one-way convenience. The "only if" direction is what makes it a characterisation, and it is what forbids the very common wrong claim that eigenvectors are perpendicular in general.
4. **The proof** (below), in three parts, with the load-bearing step called out.
5. The algebraic payoff: with `Q` holding orthonormal eigenvectors as columns, `Q^-1 = Q^T`, so `A = Q Lambda Q^T`. The sandwich from `0406` costs a transpose instead of an inversion, and it is a rotation rather than a general change of basis.
6. **The census, and this is the page's real payload.** Show that the covariance matrix, any Gram matrix `X^T X`, a kernel matrix, and a graph Laplacian are all symmetric by construction. The restriction to symmetric matrices is not a restriction in practice. One line each, no derivations, each pointing at the page that owns it.
7. The spectral sum `A = lambda_1 q_1 q_1^T + ... + lambda_n q_n q_n^T`. Each term is a rank-one piece, weighted by its eigenvalue. This shape returns on `0407` with two sets of vectors and on `0409` as the thing that gets truncated.
8. What is still free, and must be said here because `0410` depends on it: eigenvalue **signs** and eigenvector **signs** are not pinned down, and when two eigenvalues are equal the whole plane they span is an eigenspace, so any orthonormal pair in it will do. Perpendicular does not mean unique.

## Named theorem and its stated proof (D4)

**Theorem (spectral theorem, real symmetric case).** Let `A` be a real `n x n` matrix with `A = A^T`. Then every eigenvalue of `A` is real, and `R^n` has an orthonormal basis consisting of eigenvectors of `A`. Equivalently `A = Q Lambda Q^T` with `Q` orthogonal and `Lambda` real diagonal. Conversely, any matrix of that form is symmetric.

**Proof, in three parts.**

*Part 1, the eigenvalues are real.* Let `Av = lambda v` with `v != 0`, allowing complex entries for now, and let `v*` be the conjugate transpose. Then `v* A v = lambda (v* v)`. The number `v* v` is a sum of squared magnitudes, so it is real and strictly positive. The number `v* A v` is also real, because its conjugate transpose is `v* A^T v = v* A v` using `A` real and symmetric, and a `1 x 1` matrix equal to its own conjugate transpose is a real number. So `lambda` is a real number divided by a positive real number, hence real. Because `lambda` is real and `A` is real, `(A - lambda I)` is a real singular matrix and a **real** eigenvector can be chosen.

*Part 2, eigenvectors for different eigenvalues are perpendicular.* Let `Av = lambda v` and `Aw = mu w` with `lambda != mu`. Compute `v^T A w` two ways. Substituting for `Aw` gives `mu (v^T w)`. Using symmetry, `v^T A w = (A^T v)^T w = (A v)^T w = lambda (v^T w)`. So `(lambda - mu)(v^T w) = 0`, and since `lambda != mu` we get `v^T w = 0`.

*Part 3, there are enough of them.* Induct on `n`. For `n = 1` there is nothing to prove. For `n > 1`, part 1 supplies a real unit eigenvector `q_1` with real eigenvalue `lambda_1`. Let `W` be the set of vectors perpendicular to `q_1`. **`W` is carried into itself by `A`:** if `w` is in `W` then `(Aw)^T q_1 = w^T A^T q_1 = w^T A q_1 = lambda_1 (w^T q_1) = 0`, so `Aw` is in `W` too. The restriction of `A` to `W` is again symmetric, and `W` has dimension `n - 1`, so by the inductive hypothesis `W` has an orthonormal basis of eigenvectors. Adding `q_1` gives an orthonormal basis of `R^n`.

*Converse.* If `A = Q Lambda Q^T` then `A^T = (Q Lambda Q^T)^T = Q Lambda^T Q^T = Q Lambda Q^T = A`, since a diagonal matrix is its own transpose.

**The step that does the real work.** Part 3's invariance argument: that the perpendicular complement of an eigenvector is carried into itself. That single line is what turns "there is at least one eigenvector" into "there are `n` of them, perpendicular". It uses symmetry, and it is exactly the step that fails for a non-symmetric matrix. The page says this explicitly and immediately shows the failure with `A = [[4,1],[2,3]]` from `0401`, whose eigendirections `(1,1)` and `(1,-2)` have dot product `1 - 2 = -1`, not zero.

**The honest boundary.** Part 1 quietly used complex vectors to prove an entirely real statement, which is the standard route and not an accident. The complex analogue, where `A = A*` and the same conclusion holds, is called the Hermitian case; it is true, the proof is the same with conjugate transposes throughout, and the course does not need it. Part 3's induction also assumes an eigenvalue exists at all, which over the complex numbers is the fundamental theorem of algebra, named on `0402` and not proved here.

## Planned figures

1. **Orientation figure**, `flowchart LR`: `Eigenvectors (0401)` and `Orthonormal bases (03xx)` feed `THIS PAGE - symmetric means perpendicular eigenvectors, always`, which feeds `Quadratic forms (0404)`, `Positive definiteness (0405)`, `The SVD (0407)` and `PCA (0410)`.
2. **`svg.chart`, required floor.** Two panels on identical axes. Left: `S = [[5,2],[2,2]]`, its two eigendirections drawn as rays at exactly 90 degrees, aligned with the axes of the ellipse `S` maps the unit circle to. Right: `A = [[4,1],[2,3]]`, eigendirection rays at an acute angle and *not* aligned with the ellipse axes, with the angle annotated. Kills: "eigenvectors are perpendicular", the module's most common wrong belief.
3. **`mindmap`.** Root `Symmetric matrices in machine learning`, four branches: `From data` (covariance, Gram `X^T X`), `From the model` (Hessian, Fisher information), `From a graph` (adjacency, Laplacian), `From a kernel` (any kernel matrix). Kills: reading the theorem as a special case, when the special case is nearly everything.
4. **`svg.chart`.** The spectral sum as layers: `S` drawn as a 2x2 heat grid, then `6 q_1 q_1^T` and `1 q_2 q_2^T` as two fainter grids, then the two added back to `S` exactly. Kills: `A = sum lambda_i q_i q_i^T` read as notation rather than as a decomposition into weighted layers.

## The worked example, in eight parts

`S = [[5, 2], [2, 2]]`. Chosen because the eigenvalues and the eigenvector components are all integers before normalising.

1. **Goal.** Find the orthonormal eigenbasis the theorem promises, and verify `S = Q Lambda Q^T`.
2. **Invariants first.** `trace = 7`, `det = 10 - 4 = 6`, so the characteristic polynomial is `lambda^2 - 7 lambda + 6`.
3. **Solve.** `lambda = 6` and `lambda = 1`. Both real, as the theorem promised.
4. **Eigenvectors.** For `lambda = 6`, `(S - 6I) = [[-1, 2], [2, -4]]`, so `v_1 = 2 v_2` and `v = (2, 1)`. For `lambda = 1`, `(S - I) = [[4, 2], [2, 1]]`, so `2 v_1 + v_2 = 0` and `v = (1, -2)`.
5. **Check perpendicularity.** `(2)(1) + (1)(-2) = 0`. Exactly zero, as part 2 requires.
6. **Normalise.** Both have length `sqrt(5)`, so `q_1 = (2, 1)/sqrt(5) = (0.894427, 0.447214)` and `q_2 = (1, -2)/sqrt(5) = (0.447214, -0.894427)`.
7. **Sanity check (`.p-check`).** Reassemble: `6 q_1 q_1^T + 1 q_2 q_2^T` gives back `[[5, 2], [2, 2]]` exactly. If it does not, the eigenvectors were not normalised.
8. **What changes if.** Break the symmetry by changing one off-diagonal `2` to `3`, giving `[[5,3],[2,2]]`. The eigenvalues stay real here (`trace 7`, `det 4`, discriminant `33`), but the eigenvectors stop being perpendicular. Symmetry is what buys the right angle, not realness.

## Quiz seeds

**Q1, tests a misconception.** Which is **not** guaranteed for a real symmetric matrix? Answer: that its eigenvalues are distinct. Distractors, all guaranteed: real eigenvalues; an orthonormal basis of eigenvectors; that it can be written `Q Lambda Q^T`. The feedback names the identity matrix, which is symmetric with one eigenvalue repeated `n` times, and connects it to beat 8.

**Q2.** Which of these is **not** guaranteed to be symmetric? Answer: a single weight matrix from a trained network layer, which is usually not even square. Distractors, all symmetric by construction: `X^T X`; a covariance matrix; the graph Laplacian `D - W` of an undirected graph.

## Practice seeds

**P1.** Diagonalise `S = [[3, 1], [1, 3]]` orthogonally and verify the reassembly.
*Hint:* trace and determinant give the polynomial without expanding anything.
*Solution:* `trace = 6`, `det = 8`, so `lambda^2 - 6 lambda + 8`, roots `4` and `2`. For `4`: `(S - 4I) = [[-1,1],[1,-1]]` gives `(1,1)`. For `2`: `[[1,1],[1,1]]` gives `(1,-1)`. Perpendicular, both of length `sqrt(2)`, so `q_1 = (1,1)/sqrt(2)` and `q_2 = (1,-1)/sqrt(2)`.
*`.p-check`:* `4 q_1 q_1^T + 2 q_2 q_2^T = [[3,1],[1,3]]`. Also `4 + 2 = 6 = trace` and `4 x 2 = 8 = det`.

**P2, `depth`.** Prove that if `S` is symmetric then `S^2` has the same eigenvectors as `S`, with eigenvalues squared, and use this to show `S^2` never has a negative eigenvalue.
*Hint:* Apply `S` twice to an eigenvector.
*Solution:* If `S q = lambda q` then `S^2 q = S(lambda q) = lambda (S q) = lambda^2 q`. So each eigenvector of `S` is an eigenvector of `S^2` with eigenvalue `lambda^2`. Because the spectral theorem gives `n` orthonormal eigenvectors of `S`, these are all of `S^2`'s eigenvalues. Every `lambda^2` is at least zero, so `S^2` has no negative eigenvalue.
*`.p-check`:* On `S = [[5,2],[2,2]]`, `S^2 = [[29,14],[14,8]]`, whose trace is `37 = 36 + 1 = 6^2 + 1^2` and determinant `232 - 196 = 36 = (6 x 1)^2`. Page `0405` will call `S^2` positive semidefinite for exactly this reason.

## Code and dataset plan

`code/0403-spectral-theorem.py`. Dataset `datasets/spectra.csv`.

Computes twice:
1. **From the definition.** Form the 24x24 channel covariance. Get its eigenvalues and eigenvectors, then verify the theorem's three claims directly rather than trusting them: every eigenvalue has zero imaginary part; the matrix of eigenvectors satisfies `Q^T Q = I` to tolerance; and `Q Lambda Q^T` reproduces the covariance.
2. **The library way.** Compare `numpy.linalg.eigh`, which assumes symmetry, against `numpy.linalg.eig`, which does not, on the same matrix, and assert the eigenvalues agree after sorting.
3. **The contrast that teaches.** Run the same two routines on a deliberately non-symmetric matrix and show `eig` returning eigenvectors whose pairwise dot products are not zero, printed as a small table. The program's final assertion is that the maximum off-diagonal entry of `Q^T Q` is near zero for the symmetric case and demonstrably not for the other, which is the executable form of the misconception quiz.

## Sources

- Axler, *LADR* 4e, result 7.29, the real spectral theorem stated as a three-way equivalence. `https://linear.axler.net/LADR4e.pdf`
- Deisenroth, Faisal and Ong, *MML*, Theorem 4.15. `https://mml-book.github.io/book/mml-book.pdf`
