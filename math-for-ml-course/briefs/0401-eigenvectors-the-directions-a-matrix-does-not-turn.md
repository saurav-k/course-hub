# 0401 - Eigenvectors: the directions a matrix does not turn

**Placeholder number.** Real number adopted at scaffold rebase. Module M04, position 1.
**Label:** `core`
**Rung:** working (`pill med`)

## The single tight idea

A square matrix usually rotates a vector as well as stretching it, but a few special directions come out pointing exactly where they went in, and those directions with their stretch factors describe the whole matrix.

## Prerequisites, by page number

- `03xx` a matrix as a linear map, and the matrix-vector product (M03)
- `03xx` span, basis, and linear independence (M03)
- `01xx` subscript and vector notation (M01)

Nothing from M05 onward. This page is calculus-free, which is what lets M04 precede M05.

## Beats, in order

1. One 2x2 matrix, one ordinary vector, one picture: the output points somewhere else. This is the normal case and the reader must see it before the exception means anything.
2. Hunt for the exceptions. For this matrix two directions survive unturned. Show them found, not asserted.
3. State `Av = lambda v` with `v` non-zero. Name `A`, `v` and `lambda` in words directly under the formula, per the course contract.
4. What `lambda` means physically: the stretch factor along that direction. Negative flips, magnitude under one shrinks, zero collapses the direction onto the origin.
5. Why `v != 0` is in the definition and is not a technicality: the zero vector satisfies the equation for every `lambda`, so admitting it would make every scalar an eigenvalue and the definition would say nothing.
6. Scaling an eigenvector leaves it an eigenvector with the same eigenvalue. So an eigenvector is really a **direction**, and any page that prints one has silently chosen a length and a sign. Flag this here; page `0410` depends on the reader already knowing it.
7. The rotation that has none. A quarter-turn in the plane turns every real vector, so it has no real eigenvector at all. This is the first honest limit and it is what pages `0407` to `0410` exist to repair.
8. Three named places ML meets them, one line each, no derivations: the dominant eigenvector of a link matrix ranks pages; the eigenvectors of a covariance matrix are the directions data spreads along (page `0410`); the number of zero eigenvalues of a graph Laplacian counts the connected components.

## Named theorem and its proof

None named here. Beat 6 carries a one-line justification rather than a theorem: if `Av = lambda v` and `c != 0` then `A(cv) = c(Av) = c(lambda v) = lambda(cv)`, so `cv` is an eigenvector with the same eigenvalue.

## Planned figures

1. **Orientation figure**, `flowchart LR`, this page's slice of the prerequisite graph. `Matrix as a linear map (03xx)` and `Basis and span (03xx)` feed `THIS PAGE - the directions a matrix only stretches`, which feeds `Spectral theorem (0403)`, `Diagonalisation (0406)` and `PCA (0410)`. Takeaway: this is the first page of the module and everything after it is a consequence.
2. **`svg.chart`, required floor.** The unit circle and its image under `A = [[4,1],[2,3]]`, drawn as an ellipse. Three input arrows and their three images: the two along `(1,1)` and `(1,-2)` land on their own rays, the third visibly swings off. Kills: "an eigenvector is a special vector" said in words and never seen.
3. **`svg.chart`.** Same two eigendirections with four different lengths and both signs drawn along each ray, all labelled as the same eigenvector. Kills: thinking a printed eigenvector is a canonical object rather than one representative of a direction, which is the misconception quiz below and the sign surprise on page `0410`.
4. **`stateDiagram-v2`.** What a real 2x2 can be: `two real eigendirections`, `one repeated direction`, `no real eigendirection`. Each transition labelled by the discriminant sign. Kills: assuming the good case is the only case, and sets up `0402`.

Two kinds minimum is satisfied (`flowchart`, `svg.chart`, `stateDiagram-v2`). Not all flowchart.

## The worked example, in eight parts

`A = [[4, 1], [2, 3]]`. Chosen because every number in the answer is an integer.

1. **Goal.** Find every direction this matrix does not turn.
2. **Set up.** Ask for which `v != 0` and which `lambda` we get `Av = lambda v`, that is `(A - lambda I)v = 0`.
3. **Compute.** `(A - lambda I)` is singular exactly when `(4 - lambda)(3 - lambda) - 2 = 0`, so `lambda^2 - 7 lambda + 10 = 0`.
4. **Solve.** `lambda = 5` and `lambda = 2`.
5. **Back-substitute.** For `lambda = 5`, `(A - 5I) = [[-1, 1], [2, -2]]`, whose rows both say `v1 = v2`, so `v = (1, 1)`. For `lambda = 2`, `(A - 2I) = [[2, 1], [2, 1]]`, so `2 v1 + v2 = 0` and `v = (1, -2)`.
6. **Sanity check (`.p-check`).** `A(1,1) = (5,5) = 5(1,1)`, and `A(1,-2) = (2,-4) = 2(1,-2)`. Both hold exactly.
7. **Second sanity check.** `trace(A) = 7 = 5 + 2` and `det(A) = 10 = 5 x 2`. Page `0402` explains why this always works; here it is offered as a check that costs nothing.
8. **What changes if.** Change the `2` in the lower left to `-2`. The discriminant goes negative, both eigenvalues become complex, and the matrix has no real eigendirection at all. The method did not fail; the answer genuinely is that no real direction survives.

## Quiz seeds

**Q1, tests a misconception.** A textbook prints an eigenvector as `(1, 1)` and a library returns `(-0.7071, -0.7071)` for the same matrix. Which is right?
Answer: both, because they are the same direction at a different length and sign, and an eigenvector is determined only up to a non-zero scalar multiple.
Distractors, each a true statement answering a different question: the library normalises to unit length (true, and not what makes them equally correct); the textbook has chosen integer entries for readability (true, same); the sign differs because the library sorts eigenvalues descending (false and tempting).

**Q2.** `A` maps `v` to `3v`. What is `v`? Answer: an eigenvector with eigenvalue 3. Distractors: an eigenvector with eigenvalue zero; a singular vector with singular value 3 (names a different decomposition, taught on page `0407`); a basis vector of the column space (a claim about a subspace, not about stretching).

Answer indices assigned by the module owner at integration, per the course-wide 40% cap.

## Practice seeds

**P1.** For `A = [[2, 1], [1, 2]]`, find both eigenvalues and an eigenvector for each, then check your answers against the trace and the determinant.
*Hint:* `(A - lambda I)` must be singular, so start from its determinant. The arithmetic stays in whole numbers.
*Solution:* `det(A - lambda I) = (2 - lambda)^2 - 1 = lambda^2 - 4 lambda + 3`, so `lambda = 3` and `lambda = 1`. For `lambda = 3`, `(A - 3I) = [[-1,1],[1,-1]]` gives `v = (1,1)`. For `lambda = 1`, `(A - I) = [[1,1],[1,1]]` gives `v = (1,-1)`.
*`.p-check`:* `3 + 1 = 4 = trace(A)` and `3 x 1 = 3 = det(A)`. If your two eigenvalues do not reproduce both, the error is in the quadratic and not in the eigenvectors.

**P2, `depth`.** Show that a matrix and its transpose always have the same eigenvalues, then show by example that they need not have the same eigenvectors.
*Hint:* `det(M) = det(M^T)` for every square `M`. Apply it to `M = A - lambda I`.
*Solution:* `det(A^T - lambda I) = det((A - lambda I)^T) = det(A - lambda I)`, so both matrices have the same characteristic polynomial and therefore the same eigenvalues. For the example, `A = [[4,1],[2,3]]` has eigenvector `(1,1)` for `lambda = 5`, while `A^T = [[4,2],[1,3]]` has `A^T (1,1) = (6,4)`, not a multiple of `(1,1)`; its eigenvector for `lambda = 5` is `(2,1)`.
*`.p-check`:* Both matrices must give `trace = 7` and `det = 10`, and they do.

## Code and dataset plan

`code/0401-eigenvectors.py`, NumPy and Pandas only, self-contained, loads by relative path with a URL fallback.

Dataset: `datasets/spectra.csv` (8,000 rows x 24 channels, generated by `datasets/generate/make_spectra.py`, seed 20260822).

What it computes twice, per user story 27:
1. **From the definition.** Take the 24x24 covariance of the channels. Run power iteration by hand: start from a fixed non-zero vector, multiply by the matrix, normalise, repeat, and watch the ratio `||Av|| / ||v||` settle. Report the dominant eigenvalue and eigenvector.
2. **The library way.** `numpy.linalg.eigh` on the same matrix, taking the largest eigenvalue.
3. **Assert they agree** on the eigenvalue to a tolerance, and on the eigenvector **up to sign**, which is the code-level statement of beat 6 and of the misconception quiz. The sign handling is the point of the assertion and carries a comment saying so.

It also prints `trace` against the sum of eigenvalues so the page's cheap check is visible at a scale where nobody could do it by hand.

## Sources

- Axler, *Linear Algebra Done Right*, 4th edition, Chapter 5, for the definition and for eigenvector scaling. `https://linear.axler.net/LADR4e.pdf`
- Deisenroth, Faisal and Ong, *Mathematics for Machine Learning*, Section 4.2 and Example 4.9 for the link-matrix application. `https://mml-book.github.io/book/mml-book.pdf`

Primary only. No blog summarising either.
