# 0409 - Low-rank approximation, and Eckart-Young

**Placeholder number.** Module M04, position 9. **Label:** `core`. **Rung:** frontier (`pill hard`).

## The single tight idea

Cutting the SVD's rank-one sum off after `k` terms is not merely a reasonable approximation, it is provably the best rank-`k` approximation there is, and the error left over is exactly the singular values you threw away.

## Prerequisites, by page number

- `0407` the SVD and its rank-one sum
- `0408` the geometry, and `sigma_1` as the largest stretch
- `03xx` rank (M03)

## Beats, in order

1. The question, asked concretely on the real dataset before any theory: this matrix has 192,000 numbers in it, how few can I keep and still have it?
2. Truncate. Define `A_k` as the first `k` terms of the rank-one sum from `0407`. It is a rank-`k` matrix by construction, since it is a sum of `k` rank-one pieces.
3. Ask the sceptical question the page exists to answer: of all the rank-`k` matrices in the world, is this particular one the closest to `A`? There is no reason yet to think so.
4. Define what "closest" means, because the answer depends on it. Two norms: the spectral norm `||M||_2 = sigma_1(M)`, the worst stretch, from `0408`; and the Frobenius norm, the square root of the sum of every squared entry.
5. **State Eckart-Young-Mirsky and prove it** (below), for the spectral norm in full.
6. The two error identities, and they are worth memorising: `||A - A_k||_2 = sigma_{k+1}` and `||A - A_k||_F = sqrt(sigma_{k+1}^2 + ... + sigma_r^2)`. Both say the same thing in different words: the error *is* the discarded spectrum.
7. Choosing `k` honestly. Show the energy curve, define "energy kept" as `sum of kept sigma^2 / sum of all sigma^2`, and immediately say what it is not: a share of squared error in the original units, not an accuracy on any downstream task. Where a real cliff exists, as it does in this dataset by construction, the cliff is a better guide than any percentage.
8. Uniqueness: the best rank-`k` approximation is unique exactly when `sigma_k > sigma_{k+1}`. A tie means the choice is genuinely arbitrary, and that is the practical meaning of the free choice named in `0407`'s boundary.
9. When storage actually wins: rank-`k` costs `k(m + n + 1)` numbers against `mn`, so the saving exists only when `k` is well below `mn/(m+n)`. Do the arithmetic for the dataset rather than asserting it.
10. Where this is the whole technique, three named places with a cross-link each: image and signal compression; latent semantic analysis; and the low-rank weight update in `../../llm-papers-course/lessons/0028-lora.html`, where freezing a large weight matrix and training only a rank-`r` correction is exactly this idea used deliberately rather than as a compromise.
11. **The honest limit, and it is a warning callout.** "Best" here means best over a **fully observed** matrix in **these norms**. Change either and the theorem does not apply. A ratings matrix where most entries are missing is the standard case where it does not, and no amount of filling the blanks in recovers the guarantee.

## Named theorem and its stated proof (D4)

**Theorem (Eckart-Young-Mirsky, spectral norm).** Let `A` have SVD `A = U Sigma V^T` with `sigma_1 >= sigma_2 >= ...`, and let `A_k = sum_{i=1..k} sigma_i u_i v_i^T`. Then for every matrix `B` of rank at most `k`,
`||A - B||_2 >= sigma_{k+1} = ||A - A_k||_2`.
So `A_k` is a closest rank-`k` matrix to `A` in the spectral norm.

**Proof, in three moves.**

*Move 1, the value `A_k` achieves.* `A - A_k = sum_{i > k} sigma_i u_i v_i^T`. That is itself an SVD, already in the right form with orthonormal `u`'s and `v`'s, and its largest singular value is `sigma_{k+1}`. By `0408` beat 4, the spectral norm is the largest singular value, so `||A - A_k||_2 = sigma_{k+1}`.

*Move 2, set up a contradiction.* Suppose some `B` of rank at most `k` did better, so `||A - B||_2 < sigma_{k+1}`.

*Move 3, the dimension count.* Because `rank(B) <= k`, the null space of `B` has dimension at least `n - k`. Separately, let `W` be the span of `v_1, ..., v_{k+1}`, which has dimension `k + 1`. Two subspaces of an `n`-dimensional space whose dimensions sum to at least `(n - k) + (k + 1) = n + 1 > n` must share a non-zero vector. Take such an `x` and scale it to unit length.
Now bound `||Ax||` from above and below, and watch them collide.
*Above:* `x` is in the null space of `B`, so `Bx = 0`, hence `Ax = (A - B)x` and therefore `||Ax||_2 <= ||A - B||_2 ||x||_2 < sigma_{k+1}`.
*Below:* `x` is in `W`, so `x = c_1 v_1 + ... + c_{k+1} v_{k+1}` with `sum c_i^2 = 1`. Then `Ax = sum_i c_i sigma_i u_i`, and because the `u_i` are orthonormal, `||Ax||^2 = sum_{i <= k+1} c_i^2 sigma_i^2 >= sigma_{k+1}^2 sum c_i^2 = sigma_{k+1}^2`, using that every `sigma_i` with `i <= k+1` is at least `sigma_{k+1}`. So `||Ax|| >= sigma_{k+1}`.
The two bounds contradict each other. So no such `B` exists.

**The step that does the real work.** Move 3's dimension count. Everything else is bookkeeping about norms; the entire force of the theorem comes from the fact that a rank-`k` matrix must kill an `(n-k)`-dimensional subspace, and that such a subspace cannot avoid a `(k+1)`-dimensional one inside `R^n`. The pigeonhole is the proof.

**The Frobenius half, and the honest boundary.** The error formula in Frobenius is easy and the page proves it: the matrices `u_i v_i^T` are orthonormal under the Frobenius inner product, so
`||A - A_k||_F^2 = || sum_{i>k} sigma_i u_i v_i^T ||_F^2 = sum_{i>k} sigma_i^2`.
That `A_k` is also *optimal* in the Frobenius norm is true, and the course states it without proof: the argument needs an inequality relating the singular values of `A - B` to those of `A`, which is more machinery than this module carries. The page says so plainly rather than leaving the reader to assume the proof above covered both. The result in fact holds for every unitarily invariant norm, which is why the theorem carries three names.

## Planned figures

1. **Orientation figure**, `flowchart LR`: `The SVD (0407)` and `SVD geometry (0408)` feed `THIS PAGE - truncating is provably optimal`, which feeds `PCA (0410)` and, out of module, `Dimension and compression (M10)`.
2. **`svg.chart`, required floor.** The measured singular value decay of the centred `spectra.csv` matrix on a log axis, the cut at `k = 4` marked, and the discarded tail shaded. The shaded region is annotated as *being* the error rather than representing it. Kills: treating `k` as a hyperparameter to search when the error is readable off the tail.
3. **`svg.chart`, the credibility figure.** Measured `||A - A_k||_F` and `||A - A_k||_2` against `k` from 1 to 6, with the theoretical `sqrt(sum of tail squares)` and `sigma_{k+1}` overplotted as hollow dots landing exactly on the measured curves. Kills: doubting that the theorem is tight, by letting the reader watch theory and measurement coincide to six decimals.
4. **`quadrantChart`.** Compression ratio against energy kept, with `k = 1, 2, 3, 4, 5, 6` placed from the measured numbers so the elbow at four is a position on a chart rather than a claim.

## The worked example, in eight parts

`A = [[3, 2, 2], [2, 3, -2]]`, continued from `0407` where its SVD was found by hand, so the only new work is the truncation.

1. **Goal.** Find the best rank-one approximation to `A` and know exactly how wrong it is before computing it.
2. **Recall the SVD.** `sigma_1 = 5` with `u_1 = (1,1)/sqrt(2)` and `v_1 = (1,1,0)/sqrt(2)`; `sigma_2 = 3` with `u_2 = (1,-1)/sqrt(2)` and `v_2 = (1,-1,4)/(3 sqrt(2))`.
3. **Predict the error first.** By the theorem, the best rank-one approximation must be wrong by exactly `sigma_2 = 3` in the spectral norm. Write that down before building anything.
4. **Build `A_1 = sigma_1 u_1 v_1^T`.** The outer product `u_1 v_1^T` is `(1/2) [[1,1,0],[1,1,0]]`, so `A_1 = 5 x (1/2) [[1,1,0],[1,1,0]] = [[2.5, 2.5, 0], [2.5, 2.5, 0]]`.
5. **Form the residual.** `A - A_1 = [[0.5, -0.5, 2], [-0.5, 0.5, -2]]`.
6. **Measure it.** Frobenius: `sqrt(0.25 + 0.25 + 4 + 0.25 + 0.25 + 4) = sqrt(9) = 3`. Spectral: also `3`, since the residual is rank one and for a rank-one matrix the two norms coincide.
7. **Sanity check (`.p-check`).** The prediction in step 3 was `3` and the measurement in step 6 is `3`. Independently, `||A||_F^2 = 34` and `||A_1||_F^2 = 25`, and `34 - 25 = 9 = 3^2`, which is the Pythagorean statement that the kept and discarded parts are orthogonal. If your residual norm does not satisfy `||A||_F^2 = ||A_k||_F^2 + ||A - A_k||_F^2`, the truncation was built wrong.
8. **What changes if.** Go to `k = 2`. Then nothing is discarded, because `A` has rank 2, so `A_2 = A` exactly and the error is zero. This is the boundary case worth seeing: low-rank approximation of a matrix that is already low rank costs nothing at all, which is why the dataset on this page was built with a real rank in it.

## Quiz seeds

**Q1, tests a misconception.** You truncate a matrix whose singular values are `10, 8, 1, 0.5` at `k = 2`. What is `||A - A_2||_2`? Answer: `1`, the largest discarded singular value. Distractors: `0.5`, the smallest discarded one; `1.118`, which is the correct **Frobenius** error `sqrt(1 + 0.25)` and therefore answers a different question, which the feedback must say; `1.5`, the plain sum, which is neither norm.

**Q2, tests a misconception.** Keeping more singular values always gives a better result. True or false, and why? Answer: false, in the sense that matters. It always reduces the reconstruction error of *this* matrix, by the error formula, but when the matrix is a noisy measurement the extra components fit noise, and on a matrix with missing entries the guarantee does not hold at all. Distractors: true, because the error formula is decreasing in `k` (states a true fact and stops one step short of the question); false, because the error increases past the rank (false, it is exactly zero there); true, because more parameters always fit better (conflates fitting this matrix with being useful).

## Practice seeds

**P1.** A `100 x 40` matrix has singular values whose squares sum to `500`, and the first three squared values are `300`, `90` and `40`. Compute the energy kept at `k = 3`, the Frobenius error, and the storage ratio.
*Hint:* Energy is a ratio of sums of squares, and the error is the square root of what is left.
*Solution:* Kept energy `(300 + 90 + 40)/500 = 430/500 = 0.86`, that is 86 percent. Frobenius error `sqrt(500 - 430) = sqrt(70) = 8.3666`. Storage `3 x (100 + 40 + 1) = 423` numbers against `100 x 40 = 4000`, a ratio of `9.46`.
*`.p-check`:* Kept energy plus discarded energy must be exactly 1: `0.86 + 70/500 = 0.86 + 0.14 = 1.00`. If they do not sum to one, a squared value was used where a value belonged.

**P2, `depth`.** Show that `||A||_F^2 = sigma_1^2 + ... + sigma_r^2`, and use it to prove the energy-kept and error identities are the same statement.
*Hint:* The Frobenius norm squared is `trace(A^T A)`, and `0402` says the trace is the sum of the eigenvalues.
*Solution:* `||A||_F^2 = trace(A^T A)`, since the `i`-th diagonal entry of `A^T A` is the squared length of column `i` and summing them sums every squared entry. By `0402`, the trace equals the sum of the eigenvalues of `A^T A`, which by `0407` are exactly the `sigma_i^2`. So `||A||_F^2 = sum sigma_i^2`. Now split the sum at `k`: the first `k` terms are `||A_k||_F^2` by the same argument applied to `A_k`, and the rest are `||A - A_k||_F^2` by the error formula. So kept plus discarded equals the total, and dividing through by the total turns the error identity into the energy identity.
*`.p-check`:* On the worked `A`, `||A||_F^2 = 34` and `sigma_1^2 + sigma_2^2 = 25 + 9 = 34`. On the dataset, `trace` of the covariance times `(n-1)` must equal the sum of the squared singular values, which `code/0409` asserts.

## Code and dataset plan

`code/0409-low-rank-approximation.py`. Dataset `datasets/spectra.csv`, whose four-component construction is the point of this page.

Computes twice:
1. **From the definition.** Build `A_k` explicitly as a sum of `k` outer products `sigma_i u_i v_i^T`, then measure `||A - A_k||_F` and `||A - A_k||_2` directly from the residual matrix.
2. **From the theorem.** Compute `sqrt(sum of tail squared singular values)` and `sigma_{k+1}` from the spectrum alone, touching no residual.
3. **Assert they agree** to a tight tolerance at every `k` from 1 to 8, and print the two columns side by side so the agreement is visible rather than merely asserted. This is the executable form of figure 3 and it is the page's central claim.

The program also prints the storage arithmetic for each `k` and the energy kept, and it deliberately reports the noise floor: the standard deviation of `sigma_5` through `sigma_24` is small compared with their mean, which is the numerical signature of iid noise and the reason the elbow sits at four. It closes with a comment naming what it has **not** shown, namely that the guarantee survives missing entries, which it does not.

## Sources

- Damle, Cornell CS 3220, Theorem 1, Eckart-Young-Mirsky stated for both norms with the error formulas. `https://www.cs.cornell.edu/courses/cs3220/2019fa/SVD.pdf`
- Deisenroth, Faisal and Ong, *MML*, Theorem 4.24 and Theorem 4.25, whose spectral-norm argument is the one reproduced above. `https://mml-book.github.io/book/mml-book.pdf`
- Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models", arXiv:2106.09685, for the cross-link in beat 10. `https://arxiv.org/abs/2106.09685`
