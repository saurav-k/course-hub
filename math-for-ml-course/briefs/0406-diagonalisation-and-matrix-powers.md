# 0406 - Diagonalisation, and matrix powers

**Placeholder number.** Module M04, position 6. **Label:** `core`. **Rung:** working (`pill med`).

## The single tight idea

When a matrix has a full set of independent eigenvectors it can be written as "change to the eigenbasis, scale each axis, change back", and that single rewrite turns a matrix power into `n` scalar powers.

## Prerequisites, by page number

- `0401` eigenvalues and eigenvectors
- `0403` the spectral theorem, which is the case where this always works and works orthogonally
- `03xx` change of basis, and the matrix inverse (M03)

## Beats, in order

1. Collect the eigenvectors as the columns of `P` and the eigenvalues on the diagonal of `D`. Then `AP = PD`, because column `i` of each side is `A v_i` and `lambda_i v_i`.
2. If `P` is invertible, `A = P D P^-1`. State the condition plainly: `P` is invertible exactly when the `n` eigenvectors are linearly independent.
3. Read the sandwich right to left as three physical steps: `P^-1` rewrites the vector in eigenvector coordinates, `D` scales each coordinate, `P` writes the answer back in the original coordinates. Nothing is being approximated.
4. **The powers result** and its proof (below). This is why anyone cares.
5. Consequence, drawn rather than asserted: repeatedly applying `A` to almost any starting vector makes the largest `|lambda|` dominate, so the result swings onto the dominant eigendirection. That is power iteration, which is how `code/0401` already computed an eigenvector.
6. Two conditions that guarantee diagonalisability, in increasing usefulness: `n` distinct eigenvalues is sufficient but not necessary; symmetry (page `0403`) is the case that matters here and it gives the stronger orthogonal form `A = Q Lambda Q^T`.
7. **When it fails.** A shear such as `[[1,1],[0,1]]` has `lambda = 1` twice and only a one-dimensional eigenspace, so `P` cannot be invertible. Such a matrix is called defective. Say plainly that this is not a curiosity to wave away: it is why pages `0407` to `0410` use a different factorisation entirely.
8. Name the sibling without teaching it: the long-run behaviour of a Markov chain is this same computation, and M08 owns it.

## Named theorems and their stated proofs (D4)

**Theorem 1 (diagonalisability).** An `n x n` matrix `A` can be written `P D P^-1` with `D` diagonal if and only if `A` has `n` linearly independent eigenvectors.

*Proof.* Suppose `A = P D P^-1` with `D` diagonal. Then `AP = PD`. Reading column `i`: `A p_i = d_ii p_i`, so each column of `P` is an eigenvector, and they are linearly independent because `P` is invertible. Conversely, if `A` has `n` independent eigenvectors, put them in the columns of `P`, which is then invertible, and put the matching eigenvalues in `D`. Column `i` of `AP` is `A p_i = lambda_i p_i`, which is column `i` of `PD`, so `AP = PD` and therefore `A = P D P^-1`.

**Theorem 2 (powers).** If `A = P D P^-1` then `A^k = P D^k P^-1` for every positive integer `k`, and `D^k` is the diagonal matrix of `k`-th powers of the eigenvalues.

*Proof, by telescoping.* Write out the product:
`A^k = (P D P^-1)(P D P^-1) ... (P D P^-1)`, `k` copies.
Between each neighbouring pair sits `P^-1 P = I`, which vanishes. Every interior pair cancels this way, leaving `P D^k P^-1`. And `D^k` is diagonal with entries `lambda_i^k`, because multiplying diagonal matrices multiplies corresponding entries.
Formally this is an induction: it holds for `k = 1`; and if `A^k = P D^k P^-1` then `A^(k+1) = A^k A = P D^k P^-1 P D P^-1 = P D^k D P^-1 = P D^(k+1) P^-1`.

**The step that does the real work.** The interior cancellation `P^-1 P = I`. It is the whole content of the theorem, and it is available only because `P` is invertible, which is exactly the condition of Theorem 1. A defective matrix has no such `P` and no such shortcut.

**The honest boundary.** Every defective matrix still has a Jordan form, which is nearly diagonal and recovers a version of the powers result. The course names it here and does not build it, because the SVD on page `0407` solves the practical problem better and needs no extra theory.

## Planned figures

1. **Orientation figure**, `flowchart LR`: `Eigenvectors (0401)` and `Change of basis (03xx)` feed `THIS PAGE - A = P D P^-1 and A^k = P D^k P^-1`, which feeds `The SVD (0407)` as the repair for the case where it fails.
2. **`flowchart LR`.** The sandwich as four boxes with the vector annotated at each stage: `x`, then `P^-1 x` labelled "now in eigenvector coordinates", then `D P^-1 x` labelled "each coordinate scaled", then `A x`. Kills: reading `P D P^-1` as an algebraic identity rather than three motions.
3. **`svg.chart`, required floor.** A fan of eight starting vectors, then the same fan after `A`, `A^2`, `A^4` and `A^8` for `A = [[4,1],[2,3]]`, visibly collapsing onto the `(1,1)` direction. The angle of each fan-mean is annotated so the convergence is a number and not an impression. Kills: not seeing why the dominant eigenvalue dominates.
4. **`stateDiagram-v2`.** Three states a square matrix can be in: `diagonalisable`, `orthogonally diagonalisable` as a substate reached by symmetry, and `defective`, with the transitions labelled by the property that puts it there. Kills: treating "defective" as a footnote instead of the reason the next four pages exist.

## The worked example, in eight parts

`A = [[4, 1], [2, 3]]`, third appearance, so the eigen-work is trusted and only the new step is new.

1. **Goal.** Compute `A^5` without multiplying five matrices.
2. **Collect.** From `0401`, eigenvalues `5` and `2` with eigenvectors `(1,1)` and `(1,-2)`. So `P = [[1, 1], [1, -2]]` and `D = diag(5, 2)`.
3. **Check `P` is invertible.** `det(P) = (1)(-2) - (1)(1) = -3`, non-zero, so the two eigenvectors are independent and Theorem 1 applies.
4. **Invert.** `P^-1 = (1/-3) [[-2, -1], [-1, 1]] = [[2/3, 1/3], [1/3, -1/3]]`.
5. **Power the diagonal.** `D^5 = diag(5^5, 2^5) = diag(3125, 32)`. Two scalar powers, not five matrix products.
6. **Reassemble.** `A^5 = P D^5 P^-1 = [[2094, 1031], [2062, 1063]]`.
7. **Sanity check (`.p-check`).** Multiplying `A` by itself five times gives the same matrix, entry for entry. Cheaper still: `trace(A^5)` must be `5^5 + 2^5 = 3157`, and `2094 + 1063 = 3157`. And `det(A^5)` must be `10^5 = 100000`, since the determinant of a power is the power of the determinant.
8. **What changes if.** Use the shear `[[1,1],[0,1]]`. Its only eigenvalue is `1`, and solving `(A - I)v = 0` gives `[[0,1],[0,0]]v = 0`, so `v_2 = 0` and every eigenvector is a multiple of `(1,0)`. There is only one eigendirection, `P` cannot be invertible, and the method stops. Yet `A^5 = [[1,5],[0,1]]` plainly exists: the matrix has powers, it just has no diagonalisation.

## Quiz seeds

**Q1, tests a misconception.** Why can a quarter-turn rotation matrix not be diagonalised over the real numbers? Answer: because it turns every real vector, so no real eigenvector exists. Distractors: because its determinant is 1 (a true fact about rotations with no bearing); because it is symmetric and symmetric matrices resist diagonal form (doubly wrong, and the feedback says so); because its trace is zero (a true number, irrelevant).

**Q2.** A 3x3 matrix has three distinct eigenvalues. Which follows? Answer: it is diagonalisable, because eigenvectors for distinct eigenvalues are independent. Distractors: its eigenvectors are perpendicular (needs symmetry, page `0403`); it is invertible (needs all eigenvalues non-zero, and distinct does not mean non-zero); it is symmetric (the implication runs the other way, and not even then).

## Practice seeds

**P1.** For `A = [[3, 0], [1, 2]]`, diagonalise it and compute `A^4` two ways.
*Hint:* It is triangular, so read the eigenvalues off the diagonal before doing any algebra.
*Solution:* Eigenvalues `3` and `2`. For `3`: `(A - 3I) = [[0,0],[1,-1]]` gives `v = (1,1)`. For `2`: `(A - 2I) = [[1,0],[1,0]]` gives `v_1 = 0`, so `v = (0,1)`. `P = [[1,0],[1,1]]`, `det(P) = 1`, `P^-1 = [[1,0],[-1,1]]`. `D^4 = diag(81,16)`, and `A^4 = P D^4 P^-1 = [[81, 0], [65, 16]]`.
*`.p-check`:* `trace(A^4) = 81 + 16 = 97`, matching `3^4 + 2^4`. `det(A^4) = 81 x 16 = 1296 = 6^4 = det(A)^4`. Both hold.

**P2, `depth`.** Show that a diagonalisable matrix with every `|lambda| < 1` has `A^k` tending to the zero matrix, and say what happens if one eigenvalue has magnitude exactly 1.
*Hint:* Powers only ever touch `D`.
*Solution:* `A^k = P D^k P^-1`, and `D^k` has entries `lambda_i^k`. If every `|lambda_i| < 1` then each `lambda_i^k` tends to zero, so `D^k` tends to the zero matrix and `A^k = P D^k P^-1` tends to `P 0 P^-1 = 0`. If one eigenvalue has magnitude exactly 1, that entry does not shrink: the corresponding term survives and `A^k` tends to a rank-one-or-more limit rather than to zero. That surviving direction is the stationary state M08 studies.
*`.p-check`:* On `A = 0.5 I`, `A^k = 0.5^k I`, which visibly vanishes. On `A = diag(1, 0.5)`, `A^k` tends to `diag(1, 0)`, not to zero, exactly as the argument predicts.

## Code and dataset plan

`code/0406-diagonalisation-and-powers.py`. Dataset `datasets/spectra.csv`.

Computes twice:
1. **From the definition.** Build `P` and `D` from the eigendecomposition of the 24x24 channel covariance, then form `P D^k P^-1` for `k = 8`.
2. **The library way.** `numpy.linalg.matrix_power` on the same matrix and the same `k`.
3. **Assert they agree** to a relative tolerance, and **print the wall-clock cost of each** at `k = 10`, `200` and `4000`. Be accurate about what the timing shows: the sandwich is genuinely flat, because it pays for one eigendecomposition and then raises 24 scalars to the power `k`. Repeated multiplication does grow, but only logarithmically, because `numpy.linalg.matrix_power` squares repeatedly rather than multiplying `k` times. The page must not claim a linear cost it did not measure; the honest statement is that one route is constant in `k` and the other is not.

The program then does the honest counterpart: it runs the same routine on the defective `[[1,1],[0,1]]`, catches the near-singular `P`, and reports the condition number of `P` rather than crashing, showing that defectiveness announces itself numerically as an eigenvector matrix that is almost not invertible.

## Sources

- Axler, *LADR* 4e, Chapter 5 on diagonalisability and Chapter 8 on the Jordan boundary in the note. `https://linear.axler.net/LADR4e.pdf`
- Deisenroth, Faisal and Ong, *MML*, Section 4.4 on the eigendecomposition and its geometric reading. `https://mml-book.github.io/book/mml-book.pdf`
