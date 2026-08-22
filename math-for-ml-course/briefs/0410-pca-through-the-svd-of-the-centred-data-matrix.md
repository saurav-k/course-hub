# 0410 - PCA, derived through the SVD of the centred data matrix

**Placeholder number.** Module M04, position 10, and the module's capstone. **Label:** `core`. **Rung:** frontier (`pill hard`).

## The single tight idea

Take the SVD of the centred data matrix and the principal components fall out of it directly, because the right singular vectors are exactly the eigenvectors of the covariance matrix and the squared singular values are its eigenvalues.

## Prerequisites, by page number

- `0403` the spectral theorem
- `0405` positive semidefiniteness
- `0407` the SVD and its existence proof
- `0409` low-rank approximation and Eckart-Young
- `02xx` the covariance of two columns, worked by hand (M02)

**Ownership, so nothing is derived twice.** M08 owns the covariance matrix as a statistical object, meaning what `Cov(X_i, X_j)` says about random variables. This page owns its linear algebra and takes the matrix as given. **M06 owns the variational route:** maximising `b^T S b` subject to `||b|| = 1` using a Rayleigh quotient or a Lagrange multiplier arrives at the same answer, and it is presented there as a second explanation of a result the reader already has. Deriving PCA through the SVD is what keeps this page calculus-free, which is what lets the whole of M04 precede M05. This page names that second route and does not walk it.

**Notation.** `X` is `n x d`: one row per sample, one column per feature, per the course-wide convention (D7). Every formula here is in that orientation, and the page says so where a source the reader might open uses the other one.

## Beats, in order

1. The problem, stated on real data before any method: 24 correlated channels, and the suspicion that far fewer numbers carry the same information.
2. Centre the data, and say why in one sentence that is about the mathematics rather than about hygiene: covariance is defined on deviations from the mean, so `X^T X` on uncentred data is not a covariance at all and its leading direction points at where the cloud *is* rather than at how it *spreads*.
3. Define the sample covariance matrix `S = (1/(n-1)) X_c^T X_c`, and note from `0405` that it is symmetric positive semidefinite for free, so `0403` applies to it and an orthonormal eigenbasis exists.
4. State the goal: find orthonormal directions such that projecting onto the first `M` of them loses as little as possible.
5. **The SVD route** and its proof, part one (below). Take the SVD of `X_c` and the eigenvectors of `S` are handed over with no extra work.
6. **The reconstruction identity** and its proof, part two (below): the average squared reconstruction error from keeping `M` directions is exactly the sum of the eigenvalues you dropped.
7. Read the consequence rather than deriving it again: total variance `trace(S)` is fixed, so keeping the largest eigenvalues and dropping the smallest simultaneously maximises what is kept and minimises what is lost. There is no trade-off between the two goals because they are one accounting identity, and this is where `0409`'s Eckart-Young result is doing the work under a different name.
8. Explained variance ratio, defined and immediately bounded: `lambda_i / sum(lambda)` is a share of *input variance*, not an accuracy on any task. A scree plot with a real cliff is better evidence than any percentage threshold.
9. **What is not pinned down**, promised on `0401` and `0403` and paid off here: if `v` is a principal direction so is `-v`, so two runs, two libraries or two machines may hand you opposite signs and both are right. Any code that branches on the sign of a loading is wrong. Where two eigenvalues are equal, the entire plane they span is an eigenspace and even the directions are not determined.
10. **What PCA cannot see**, and it is a warning callout. PCA never looks at labels. The direction that separates two classes can be a small-variance direction that PCA discards first. Variance is not importance, and a page that leaves the reader thinking otherwise has taught the wrong lesson.
11. Scale sensitivity, in one paragraph pointing at the dataset built for it: PCA on covariance and PCA on correlation are different analyses, and choosing between them is a modelling decision about whether the features share a meaningful unit. `sensors.csv` is generated to punish getting this wrong; `spectra.csv`, used here, shares one unit across all channels and so does not.

## Named results and their stated proofs (D4)

**Result 1 (the SVD gives PCA).** Let `X_c` be the centred `n x d` data matrix with SVD `X_c = U Sigma V^T`. Then the columns of `V` are eigenvectors of the sample covariance `S = (1/(n-1)) X_c^T X_c`, with eigenvalues `lambda_i = sigma_i^2 / (n - 1)`.

*Proof.* Substitute the SVD directly:
`X_c^T X_c = (U Sigma V^T)^T (U Sigma V^T) = V Sigma^T U^T U Sigma V^T = V (Sigma^T Sigma) V^T`,
using `U^T U = I`. Now `Sigma^T Sigma` is the `d x d` diagonal matrix with entries `sigma_i^2`. Dividing by `n - 1`,
`S = V diag(sigma_i^2 / (n-1)) V^T`.
`V` is orthogonal and the middle factor is diagonal, so this **is** a spectral decomposition of `S` in the sense of `0403`. Reading it column by column, `S v_i = (sigma_i^2 / (n-1)) v_i`.

*The step that does the real work:* `U^T U = I` collapsing in the middle. It is the same cancellation as `0404`'s principal-axes proof, and it is available for the same reason: the factor is orthogonal. Note what the proof did **not** need: no derivatives, no constrained optimisation, no Lagrange multiplier. That absence is why this page can sit before M05.

**Result 2 (the reconstruction identity).** Let `B` hold the first `M` columns of `V`. Projecting each centred sample onto that subspace and back gives `x_tilde = B B^T x`. Then
`(1/(n-1)) sum_over_samples ||x - x_tilde||^2 = lambda_{M+1} + ... + lambda_d`,
the sum of the eigenvalues that were dropped.

*Proof.* The columns `v_1, ..., v_d` of `V` form an orthonormal basis, so every centred sample expands as `x = sum_j (v_j^T x) v_j`. The projection keeps only the first `M` terms, so the residual is exactly the tail:
`x - x_tilde = sum_{j > M} (v_j^T x) v_j`.
Because the `v_j` are orthonormal, the squared length of that sum is the sum of the squared coefficients:
`||x - x_tilde||^2 = sum_{j > M} (v_j^T x)^2`.
Sum over samples and divide by `n - 1`, then exchange the two sums:
`(1/(n-1)) sum_x sum_{j>M} (v_j^T x)^2 = sum_{j>M} v_j^T [ (1/(n-1)) sum_x x x^T ] v_j = sum_{j>M} v_j^T S v_j`.
The bracket is `S` by definition. And `v_j^T S v_j = v_j^T (lambda_j v_j) = lambda_j` by Result 1 and `v_j^T v_j = 1`. So the total is `sum_{j>M} lambda_j`.

*The step that does the real work:* exchanging the two sums to reveal `(1/(n-1)) sum_x x x^T` as the covariance matrix. Before that exchange the expression is about individual samples; after it, it is about the matrix, and the eigenvalues can be substituted in. Everything else is orthonormality.

**The honest boundary.** Result 2 shows that the eigenvector subspace achieves an error of `sum_{j>M} lambda_j`. That no *other* `M`-dimensional subspace does better is the genuine optimality claim, and it is `0409`'s Eckart-Young theorem applied to `X_c`, which the page cites rather than reproving. The variational statement, that `v_1` maximises `b^T S b` over unit `b`, is true, is equivalent, and belongs to M06 by the ownership split above.

## Planned figures

1. **Orientation figure**, `flowchart LR`: `Spectral theorem (0403)`, `The SVD (0407)` and `Eckart-Young (0409)` feed `THIS PAGE - PCA is the SVD of the centred data`, which feeds, out of module, `The variational route (M06)`, `Covariance as a statistical object (M08)` and `Curse of dimensionality (M10)`.
2. **`svg.chart`, required floor.** The six-point hand example as a scatter with the mean marked, the PC1 line drawn through it, and each point's perpendicular drop to that line shown. Beside it, on the same points, a least-squares line with the *vertical* residuals drawn. Two visibly different lines on identical data. Kills: "PCA is just a regression line", the misconception this module most needs to prevent.
3. **`svg.chart`.** The measured scree plot of `spectra.csv`: 24 eigenvalue bars with the cliff after the fourth, and the cumulative-variance curve overlaid on a second axis with 69.98, 91.47, 96.82 and 98.16 percent marked at `k = 1..4`. Kills: choosing `k` by a percentage habit when the data has a visible answer.
4. **`svg.chart`.** The see-saw: a stacked bar of `trace(S)` split into kept and discarded, drawn for `M = 1, 2, 3, 4`, with the kept portion growing exactly as the discarded portion shrinks and the total pinned. Kills: believing maximum variance and minimum reconstruction are two objectives to trade off.
5. **`flowchart TD`.** Two routes converging: `SVD of X_c` and `eigendecomposition of S` both arriving at the same box `v_i, lambda_i = sigma_i^2/(n-1)`, with the note that only the first avoids ever forming `S`. Kills: thinking the library is doing something different from the derivation.

## The worked example, in eight parts

Six samples, two features, chosen so every intermediate number is exact.
`X = [(1,2), (2,1), (3,4), (4,3), (5,6), (6,5)]`.

1. **Goal.** Find the principal directions and say how much of the spread each one carries.
2. **Centre.** The mean is `(3.5, 3.5)`. The centred rows are `(-2.5,-1.5), (-1.5,-2.5), (-0.5,0.5), (0.5,-0.5), (1.5,2.5), (2.5,1.5)`. They sum to `(0,0)`, which is the check that centring worked.
3. **Covariance.** `sum x_1^2 = 17.5`, `sum x_2^2 = 17.5`, `sum x_1 x_2 = 14.5`. Dividing by `n - 1 = 5`, `S = [[3.5, 2.9], [2.9, 3.5]]`.
4. **Eigenvalues.** For a matrix `[[a, b], [b, a]]` the eigenvalues are `a + b` and `a - b`, so `6.4` and `0.6`, with eigenvectors `(1,1)/sqrt(2)` and `(-1,1)/sqrt(2)`. Perpendicular, as `0403` requires.
5. **Explained variance.** `trace(S) = 7`, so PC1 carries `6.4/7 = 91.43` percent and PC2 carries `0.6/7 = 8.57` percent.
6. **The same answer through the SVD, per Result 1.** The singular values of the centred matrix are `5.656854` and `1.732051`. Then `sigma_1^2/(n-1) = 32/5 = 6.4` and `sigma_2^2/(n-1) = 3/5 = 0.6`. Identical, and the covariance matrix was never formed.
7. **Sanity check (`.p-check`).** Three checks. `6.4 + 0.6 = 7 = trace(S)`. The reconstruction error from keeping only PC1 must be the discarded eigenvalue: projecting and measuring gives `0.6`, matching `lambda_2` exactly, which is Result 2 on six points. And the scores on PC1 are `-2.828, -2.828, 0, 0, +2.828, +2.828`, whose mean is zero, as projections of centred data must have.
8. **What changes if.** Skip step 2. Then `X^T X / (n-1)` has leading eigenvector very nearly `(0.707, 0.707)` again but for the wrong reason: it is chasing the mean at `(3.5, 3.5)`, which happens to lie along the same diagonal for this symmetric toy. Move one point to `(1, 20)` and the uncentred leading direction swings towards the new mean while the centred one does not. The lesson is that agreement on a symmetric example is a coincidence, not a licence.

## Quiz seeds

**Q1, tests a misconception.** PCA's first component and an ordinary least-squares line fitted to the same two columns are: Answer: different lines, because one minimises perpendicular distance to the line and the other minimises vertical distance. Distractors: the same line, since both follow the trend (the misconception); the same whenever the correlation is above 0.9 (they converge but never coincide); different only when the columns have different units (names a real effect on PCA, but the two criteria differ even in identical units).

**Q2, tests a misconception.** The eigenvalues of a covariance matrix are `6.4` and `0.6`. What is the average squared reconstruction error if you keep only the first component? Answer: `0.6`, the discarded eigenvalue. Distractors: `6.4`, the variance kept, which is the complementary quantity; `7.0`, the total; `0.0857`, which is the discarded *ratio* and answers a different question, as the feedback must say.

## Practice seeds

**P1.** Four samples, two features: `(0,0), (2,1), (4,4), (6,7)`. Centre them, form `S`, find both eigenvalues, and report the explained-variance ratios.
*Hint:* Centre first and check the centred rows sum to zero before going on. The covariance divides by `n - 1 = 3`.
*Solution:* Mean `(3, 3)`. Centred: `(-3,-3), (-1,-2), (1,1), (3,4)`. `sum x_1^2 = 9+1+1+9 = 20`, `sum x_2^2 = 9+4+1+16 = 30`, `sum x_1 x_2 = 9+2+1+12 = 24`. So `S = [[20/3, 8], [8, 10]] = [[6.6667, 8], [8, 10]]`. `trace = 16.6667`, `det = 66.667 - 64 = 2.6667`. So `lambda^2 - 16.6667 lambda + 2.6667 = 0`, discriminant `277.778 - 10.667 = 267.111`, square root `16.3436`, roots `16.5051` and `0.1616`. Ratios `99.03` percent and `0.97` percent.
*`.p-check`:* `16.5051 + 0.1616 = 16.6667 = trace(S)` and `16.5051 x 0.1616 = 2.667 = det(S)`. Both invariants reproduced, so the quadratic was solved correctly. The near-100 percent first ratio is the signature of four nearly collinear points, which is what the data is.

**P2, `depth`.** Prove that the scores on any principal component have mean zero, and that the scores on two different components have zero covariance.
*Hint:* A score is `v_j^T x` for centred `x`. For the second part, use Result 1.
*Solution:* The mean score on component `j` is `(1/n) sum_x v_j^T x = v_j^T ((1/n) sum_x x) = v_j^T 0 = 0`, because centring made the sample mean the zero vector. For the covariance between components `j` and `k` with `j != k`, since both score sets have mean zero their covariance is
`(1/(n-1)) sum_x (v_j^T x)(v_k^T x) = v_j^T [(1/(n-1)) sum_x x x^T] v_k = v_j^T S v_k = lambda_k (v_j^T v_k) = 0`,
using Result 1 and then orthogonality of `v_j` and `v_k`. So PCA does not merely rotate the data, it **decorrelates** it.
*`.p-check`:* On the worked six-point example, the PC1 scores are `-2.828, -2.828, 0, 0, 2.828, 2.828` and the PC2 scores are `+0.707, -0.707, +0.707, -0.707, +0.707, -0.707`. Each set sums to zero, and their inner product is `-2 + 2 + 0 - 0 + 2 - 2 = 0`. Both claims hold on real numbers.

## Code and dataset plan

`code/0410-pca-through-the-svd.py`. Dataset `datasets/spectra.csv`.

Computes twice, and this program is the module's centrepiece:
1. **From the definition.** Centre the data, form the `24 x 24` covariance `S` explicitly, and take its eigendecomposition with `numpy.linalg.eigh`.
2. **Through the SVD, per Result 1.** Take `numpy.linalg.svd` of the centred matrix and form `sigma_i^2/(n-1)`, never building `S` at all.
3. **Assert they agree** on the eigenvalues to a tight tolerance, and on the directions **up to sign**, with the sign handling commented as the executable form of beat 9. The measured agreement on this dataset is to within `6.1e-16`.

It then verifies Result 2 directly rather than trusting it: for `M = 1, 2, 3, 4, 6` it projects and reconstructs, measures the average squared error, and asserts it equals the sum of the discarded eigenvalues. Measured, these agree to `5.6e-17` or better at every `M`.

It prints the scree table with cumulative variance `69.98, 91.47, 96.82, 98.16` percent for the first four components, and prints the noise floor so the elbow at four is visible as a number.

Finally it makes beat 9 concrete without depending on library behaviour: it asserts that `-v` satisfies the eigenvector equation exactly as well as `v` does, which is a mathematical fact rather than an accident of a routine. It also prints a short note that on this dataset the two routines happen to return the **same** signs, which is precisely why relying on that agreement is unsafe.

## Sources

- Deisenroth, Faisal and Ong, *MML*, Sections 10.2 to 10.4, for the reconstruction identity and the two perspectives. Note the orientation difference: MML writes the data matrix with samples as columns, and this page uses rows, per D7. `https://mml-book.github.io/book/mml-book.pdf`
- Shlens, "A Tutorial on Principal Component Analysis", arXiv:1404.1100, for the explicit assumptions behind beats 10 and 11. `https://arxiv.org/abs/1404.1100`
- Pearson, "On Lines and Planes of Closest Fit to Systems of Points in Space", *Philosophical Magazine* 2 (1901), 559-572, page 560, for the perpendicular-distance criterion in figure 2 and quiz Q1. `https://zenodo.org/records/1430636`
