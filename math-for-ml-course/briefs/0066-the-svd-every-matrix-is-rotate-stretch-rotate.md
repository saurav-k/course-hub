# 0066 - The SVD: every matrix is a rotation, a stretch and a rotation

**Placeholder number.** Module M04, position 7. **Label:** `core`. **Rung:** working (`pill med`).

## The single tight idea

Every matrix whatsoever, of any shape, factors as `A = U Sigma V^T` with two orthogonal matrices and one non-negative diagonal, which is what the eigendecomposition would have been if it had never had exceptions.

## Prerequisites, by page number

- `0062` the spectral theorem
- `0064` positive semidefiniteness and the `X^T X` fact
- `0065` diagonalisation and where it fails
- `03xx` rank, and the column and null spaces (M03)

## Beats, in order

1. Collect the four ways the eigendecomposition has already disappointed, all met on earlier pages: complex eigenvalues (`0061`), non-perpendicular eigenvectors (`0062`), too few eigenvectors (`0065`), and the one that has not been said yet.
2. Say it: a non-square matrix has no eigenvectors at all, because `Av` lives in a different space from `v` and `Av = lambda v` cannot even be written down. A data matrix is almost never square, so this is the common case and not the exotic one.
3. State the SVD, with every shape spelled out: `A` is `m x n`, `U` is `m x m` orthogonal, `Sigma` is `m x n` diagonal with non-negative entries in decreasing order, `V` is `n x n` orthogonal.
4. Name the parts in words: the columns of `V` are the right singular vectors and live in the input space; the columns of `U` are the left singular vectors and live in the output space; the `sigma_i` are the singular values and say how much each paired direction is stretched.
5. **Where the singular values come from** and the existence proof (below). The whole factorisation is the spectral theorem applied to `A^T A`, which `0064` already proved is symmetric positive semidefinite. Nothing new is assumed.
6. Two things that differ from eigenvalues and must be said explicitly: singular values are never negative, and they come in a conventional decreasing order. Eigenvalues have neither property.
7. The rank-one sum `A = sigma_1 u_1 v_1^T + ... + sigma_r u_r v_r^T`, the same shape as `0062`'s spectral sum but with two different vectors in each term instead of one repeated. Page `0068` truncates exactly this sum.
8. Rank becomes countable: the rank of `A` is the number of non-zero singular values. This makes rank a measured quantity rather than a symbolic one, and page `0068` shows why the distinction matters when the small values are not exactly zero.
9. The comparison table, one row each: what the spectral theorem covers against what the SVD covers, one basis against two, symmetric-only against everything.

## Named theorem and its stated proof (D4)

**Theorem (existence of the SVD).** Every real `m x n` matrix `A` can be written `A = U Sigma V^T` with `U` and `V` orthogonal and `Sigma` diagonal with non-negative decreasing entries.

**Proof, constructive, in four steps.**

*Step 1, build `V` and the singular values.* The matrix `A^T A` is `n x n`, symmetric (because `(A^T A)^T = A^T A`), and positive semidefinite by `0064`'s one-line fact. By the spectral theorem `0062` it has an orthonormal basis of eigenvectors `v_1, ..., v_n` with real eigenvalues `lambda_1 >= ... >= lambda_n >= 0`, the non-negativity coming from `0064`. Define `sigma_i = sqrt(lambda_i)`, which is real because `lambda_i >= 0`. Let `r` be the number of strictly positive `sigma_i`.

*Step 2, build the first `r` columns of `U`.* For `i <= r` define `u_i = A v_i / sigma_i`, which is legal because `sigma_i > 0`.

*Step 3, check those `u_i` are orthonormal.* Compute
`u_i^T u_j = (A v_i)^T (A v_j) / (sigma_i sigma_j) = v_i^T (A^T A) v_j / (sigma_i sigma_j) = lambda_j (v_i^T v_j) / (sigma_i sigma_j)`.
If `i != j` then `v_i^T v_j = 0` and the whole thing is zero. If `i = j` then `v_i^T v_i = 1` and it is `lambda_i / sigma_i^2 = 1`. So they are orthonormal. Extend them to a full orthonormal basis `u_1, ..., u_m` of the output space, which is always possible.

*Step 4, check the factorisation reproduces `A`.* For `i <= r`, `A v_i = sigma_i u_i` by the definition in step 2. For `i > r`, `sigma_i = 0`, so `||A v_i||^2 = v_i^T A^T A v_i = lambda_i = 0`, hence `A v_i = 0`. So `A v_i = sigma_i u_i` for **every** `i`. Stacking these `n` statements as columns gives `A V = U Sigma`, and multiplying on the right by `V^T` with `V^T = V^-1` gives `A = U Sigma V^T`.

**The step that does the real work.** Step 3's middle equality, `(A v_i)^T (A v_j) = v_i^T (A^T A) v_j`. It is what lets the orthonormality of the `v`'s, which the spectral theorem handed us in the *input* space, transfer to the `u`'s in the *output* space. Everything else is bookkeeping. Notice also step 4's second half: the directions with zero singular value are exactly the null space, which is beat 8 arriving as a by-product rather than a separate claim.

**The honest boundary.** The proof assumed `A` is real; the complex case is identical with conjugate transposes throughout. It also quietly used that any orthonormal set extends to an orthonormal basis, which is Gram-Schmidt and is M03's. And the factorisation is not unique when singular values repeat or when `r < m`: the extension in step 3 involved a free choice. Page `0068` says exactly when that freedom matters.

## Planned figures

1. **Orientation figure**, `flowchart LR`: `Spectral theorem (0062)` and `Positive semidefiniteness (0064)` feed `THIS PAGE - every matrix factors, any shape`, which feeds `SVD geometry (0067)`, `Low-rank approximation (0068)` and `PCA (0069)`.
2. **`svg.chart`, required floor.** The measured singular value spectrum of the centred `spectra.csv` matrix: four tall bars at 49.17, 27.25, 13.59 and 6.80, then twenty short bars sitting flat near 1.85. The cliff is annotated with the ratio 3.65. Kills: treating rank as symbolic when here it is a visible cliff, and previews `0068`.
3. **`flowchart LR`.** Two lanes side by side: `eigendecomposition` requiring square and rewarding symmetry, returning one basis; `SVD` requiring nothing, returning two. Each lane annotated with what it cannot do. Kills: believing singular values are eigenvalues.
4. **`svg.chart`.** For the small worked matrix, the two chains `A v_1 = sigma_1 u_1` and `A v_2 = sigma_2 u_2` drawn as arrows from the input plane to the output plane, with lengths 5 and 3 marked. Kills: not seeing that the SVD pairs up two different sets of directions.

## The worked example, in eight parts

`A = [[3, 2, 2], [2, 3, -2]]`, a 2x3 matrix. Chosen because its singular values are exactly 5 and 3, with no decimals anywhere in the main line.

1. **Goal.** Factor a matrix that is not square and therefore has no eigenvectors at all.
2. **Choose the cheaper Gram matrix.** `A^T A` is 3x3 and `A A^T` is 2x2, so work with the small one. `A A^T = [[9+4+4, 6+6-4], [6+6-4, 4+9+4]] = [[17, 8], [8, 17]]`.
3. **Diagonalise it.** `trace = 34`, `det = 289 - 64 = 225`, so `lambda^2 - 34 lambda + 225 = 0` with roots `25` and `9`.
4. **Singular values.** `sigma_1 = sqrt(25) = 5` and `sigma_2 = sqrt(9) = 3`.
5. **Left singular vectors, from `A A^T`.** For `25`: `[[-8,8],[8,-8]]` gives `u_1 = (1,1)/sqrt(2)`. For `9`: `[[8,8],[8,8]]` gives `u_2 = (1,-1)/sqrt(2)`.
6. **Right singular vectors, by the proof's own formula run backwards.** `v_i = A^T u_i / sigma_i`. So `v_1 = A^T (1,1)/sqrt(2) / 5 = (5,5,0)/(5 sqrt(2)) = (1,1,0)/sqrt(2)`, and `v_2 = A^T (1,-1)/sqrt(2) / 3 = (1,-1,4)/(3 sqrt(2))`.
7. **Sanity check (`.p-check`).** Three checks, each catching a different slip. `A v_1` should be `5 u_1`, and it is. The squared singular values should sum to `sum of all squared entries of A`: `25 + 9 = 34`, and `9+4+4+4+9+4 = 34`. And `A^T A` must have eigenvalues `25`, `9` and `0`, the extra zero appearing because `A` maps a three-dimensional space into a two-dimensional one and must collapse one direction.
8. **What changes if.** Transpose `A` to get a 3x2 matrix. The singular values are unchanged at 5 and 3, because `A^T A` and `A A^T` share their non-zero eigenvalues. The roles of `U` and `V` simply swap. Nothing about the factorisation cares which way up the matrix was written.

## Quiz seeds

**Q1, tests a misconception.** How do the singular values of `A` relate to the eigenvalues of `A^T A`? Answer: they are the non-negative square roots of them. Distractors: they are equal one for one (the most common form of the error, forgetting the square root); they are the reciprocals (describes the pseudoinverse); they are unrelated (contradicts the construction the page just gave).

**Q2.** What can the SVD do that the eigendecomposition cannot? Answer: factor a matrix that is rectangular, defective or non-symmetric. Distractors, all true of both and therefore non-distinguishing: return a diagonal middle factor; reveal how much the matrix stretches space; multiply back to recover the original.

## Practice seeds

**P1.** Find the SVD of `A = [[2, 0], [0, -3]]` by hand, and explain why the singular values are not the eigenvalues.
*Hint:* `A^T A` is diagonal, so no algebra is needed for it.
*Solution:* `A^T A = [[4, 0], [0, 9]]`, eigenvalues `9` and `4`, so `sigma_1 = 3` and `sigma_2 = 2`, ordered decreasing. `v_1 = (0,1)`, `v_2 = (1,0)`. Then `u_1 = A v_1 / 3 = (0,-3)/3 = (0,-1)` and `u_2 = A v_2 / 2 = (2,0)/2 = (1,0)`. The eigenvalues of `A` itself are `2` and `-3`. The singular values are `3` and `2`: the magnitudes, reordered. The negative sign has moved out of `Sigma` and into `u_1`, because `Sigma` is required to be non-negative.
*`.p-check`:* `sigma_1^2 + sigma_2^2 = 9 + 4 = 13`, and the sum of squared entries of `A` is `4 + 9 = 13`. Also `|det(A)| = 6 = sigma_1 sigma_2 = 3 x 2`.

**P2, `depth`.** Show that `A` and `A^T` always have the same non-zero singular values.
*Hint:* Take the SVD of `A` and transpose it.
*Solution:* If `A = U Sigma V^T` then `A^T = (U Sigma V^T)^T = V Sigma^T U^T`. This is a valid SVD of `A^T`: `V` and `U` are still orthogonal, and `Sigma^T` is still diagonal with the same non-negative entries, merely reshaped from `m x n` to `n x m`. Since the singular values of a matrix are the diagonal entries of the middle factor in any SVD, `A^T` has the same ones. Equivalently, `A^T A` and `A A^T` have the same non-zero eigenvalues.
*`.p-check`:* On the worked `A = [[3,2,2],[2,3,-2]]`, `A^T A` is 3x3 with eigenvalues `25, 9, 0` and `A A^T` is 2x2 with eigenvalues `25, 9`. The non-zero ones match; the extra zero is bookkeeping about shape.

## Code and dataset plan

`code/0066-the-svd.py`. Dataset `datasets/spectra.csv`.

Computes twice:
1. **From the definition, following the existence proof exactly.** Form `A^T A`, run `numpy.linalg.eigh` on it, take square roots of the eigenvalues for the singular values, build `u_i = A v_i / sigma_i` for the non-zero ones, and verify orthonormality of the constructed `U` by checking `U^T U` against the identity.
2. **The library way.** `numpy.linalg.svd` on the same matrix.
3. **Assert they agree** on the singular values to tolerance, and on the singular *vectors* **up to sign**, with a comment saying that the sign freedom is exactly the non-uniqueness the proof's boundary paragraph named. It also asserts `A = U Sigma V^T` reproduces the original to tolerance.

The program then prints the rank as a **threshold sweep** rather than as one number: `numpy.linalg.matrix_rank` says 24, and counting singular values above 0.5, 1.0, 5.0 and 10.0 gives 24, 24, 4 and 3. Every singular value is non-zero because noise is present, so the numerical rank is genuinely full; only a threshold placed inside the cliff recovers the four components the data was built from. Rank here is a choice about where signal stops, and that is the hook page `0068` picks up.

## Sources

- Axler, *LADR* 4e, Section 7E, results 7.70 to 7.78 and the spectral-theorem comparison table. `https://linear.axler.net/LADR4e.pdf`
- Damle, Cornell CS 3220, "The Singular Value Decomposition", Definitions 1 and 2. `https://www.cs.cornell.edu/courses/cs3220/2019fa/SVD.pdf`
- Deisenroth, Faisal and Ong, *MML*, Section 4.5. `https://mml-book.github.io/book/mml-book.pdf`
