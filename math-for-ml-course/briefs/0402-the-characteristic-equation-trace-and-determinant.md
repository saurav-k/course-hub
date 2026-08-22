# 0402 - The characteristic equation, and what the trace and determinant tell you

**Placeholder number.** Module M04, position 2. **Label:** `core`. **Rung:** working (`pill med`).

## The single tight idea

The eigenvalues are the roots of one polynomial built from the matrix, and two coefficients of that polynomial are the trace and the determinant, which is why those two numbers check an eigenvalue computation for free.

## Prerequisites, by page number

- `0401` eigenvalues and eigenvectors
- `03xx` the determinant, and what a zero determinant means (M03)

## Beats, in order

1. Recover the question from `0401`: `Av = lambda v` with `v != 0` means `(A - lambda I)v = 0` has a non-zero solution, which means `A - lambda I` is **singular**.
2. Singular means zero determinant. So `det(A - lambda I) = 0`. Name it the characteristic equation and the left side the characteristic polynomial.
3. Work it for a general 2x2 and get `lambda^2 - (a + d) lambda + (ad - bc)`, that is `lambda^2 - trace(A) lambda + det(A)`. The two coefficients are already the two numbers the reader knows.
4. State and prove the two identities (below).
5. Use them as a check, and be explicit that a check that costs one addition and one multiplication is worth doing every single time.
6. What the roots can do: two distinct real roots, one repeated root, or a complex conjugate pair. The discriminant decides, and this is the promised payoff of `0401` beat 7.
7. **The honest warning, and it is a warning callout.** The characteristic polynomial is the cleanest *definition* of an eigenvalue and among the worst *algorithms* for computing one. Root-finding on a polynomial of degree `n` is badly behaved for `n` past a handful, and no numerical library computes eigenvalues this way. This page shows it once, uses it on 2x2 matrices, and never uses it again.
8. What the determinant tells you on its own: `det(A) = 0` exactly when zero is an eigenvalue, exactly when some non-zero direction is collapsed to the origin, exactly when `A` is not invertible. Four statements, one fact. Page `0405` needs this and page `0409` measures it.

## Named theorems and their stated proofs (D4)

**Theorem.** For a square matrix `A` with eigenvalues `lambda_1, ..., lambda_n` listed with multiplicity, `det(A) = lambda_1 ... lambda_n` and `trace(A) = lambda_1 + ... + lambda_n`.

**Proof for the case the course needs, `n = 2`, in full.**
Expanding directly, `det(A - lambda I) = (a - lambda)(d - lambda) - bc = lambda^2 - (a + d) lambda + (ad - bc)`.
Because `lambda_1` and `lambda_2` are its roots and it is monic, the same polynomial equals `(lambda - lambda_1)(lambda - lambda_2) = lambda^2 - (lambda_1 + lambda_2) lambda + lambda_1 lambda_2`.
Two polynomials equal for every `lambda` have equal coefficients. Matching the `lambda` coefficient gives `lambda_1 + lambda_2 = a + d = trace(A)`; matching the constant gives `lambda_1 lambda_2 = ad - bc = det(A)`.

**The step that does the real work:** matching coefficients. It is legitimate only because the two expressions agree for *every* `lambda`, not merely at the roots, and the page says so.

**The honest boundary.** For general `n` the same argument runs, with two additions the course does not carry: the factorisation into `n` linear factors needs the fundamental theorem of algebra over the complex numbers, and picking out the `lambda^(n-1)` coefficient needs the observation that only the product of diagonal entries contributes to it. Both are true and neither is proved here. The determinant half is easier and the page shows it: set `lambda = 0` in `det(A - lambda I) = product of (lambda_i - lambda)` and read off `det(A) = product of lambda_i` immediately.

## Planned figures

1. **Orientation figure**, `flowchart LR`: `Eigenvectors (0401)` and `Determinant (03xx)` feed `THIS PAGE - the polynomial whose roots are the eigenvalues`, which feeds `Spectral theorem (0403)` and `Positive definiteness (0405)`.
2. **`svg.chart`, required floor.** The characteristic polynomial of `A = [[4,1],[2,3]]` plotted over `lambda` from 0 to 7, crossing the axis at exactly 5 and 2, with the two roots marked and the trace and determinant annotated as the coefficients they are. Kills: "the characteristic equation" as an incantation rather than a curve with visible roots.
3. **`svg.chart`.** Three polynomials on one axis for three matrices: two real roots, a repeated root (tangent to the axis), and no real root (the parabola clears the axis). Kills: expecting two eigenvalues always.
4. **`flowchart TD`.** The four equivalent readings of `det(A) = 0`: zero is an eigenvalue, some direction collapses, columns are dependent, `A` has no inverse. One box each, joined to one root. Kills: treating these as four separate facts to memorise.

## The worked example, in eight parts

`A = [[4, 1], [2, 3]]`, deliberately the same matrix as `0401` so the reader sees a second route to an answer they already trust.

1. **Goal.** Get the eigenvalues without hunting for directions.
2. **Set up.** `A - lambda I = [[4 - lambda, 1], [2, 3 - lambda]]`.
3. **Compute the determinant.** `(4 - lambda)(3 - lambda) - (1)(2)`.
4. **Expand.** `12 - 7 lambda + lambda^2 - 2 = lambda^2 - 7 lambda + 10`.
5. **Read the coefficients.** `7` is `trace(A) = 4 + 3`; `10` is `det(A) = 12 - 2`. The polynomial was already known before it was expanded.
6. **Solve.** `lambda = (7 +/- sqrt(49 - 40)) / 2 = (7 +/- 3) / 2`, so `5` and `2`.
7. **Sanity check (`.p-check`).** `5 + 2 = 7` and `5 x 2 = 10`. Both coefficients reproduced, so the arithmetic is sound. And these match `0401`, reached by a different route.
8. **What changes if.** Replace the lower-left `2` with `-2`. Then `det = 12 + 2 = 14`, the polynomial is `lambda^2 - 7 lambda + 14`, the discriminant is `49 - 56 = -7`, and there is no real root. The trace and determinant identities still hold, over the complex numbers.

## Quiz seeds

**Q1, tests a misconception.** Why does no numerical library compute eigenvalues from the characteristic polynomial? Answer: because finding polynomial roots is numerically unstable as the degree grows, so the route that defines an eigenvalue is not the route that computes one. Distractors: because the polynomial does not exist for non-symmetric matrices (false); because it gives complex roots (true of some matrices and not a reason to avoid the method); because the determinant is expensive to compute (true and beside the point, since the instability is the reason).

**Q2.** A 3x3 matrix has `trace = 6` and `det = 0`. What follows? Answer: zero is one of its eigenvalues and the matrix is not invertible. Distractors: all three eigenvalues are zero (would force trace 0); the eigenvalues are 2, 2, 2 (consistent with the trace, contradicted by the determinant); it has no real eigenvalues (contradicted, since zero is one).

## Practice seeds

**P1.** Find the eigenvalues of `A = [[6, -2], [-2, 9]]` and check both coefficients.
*Hint:* Write down the trace and the determinant first. You already have the polynomial.
*Solution:* `trace = 15`, `det = 54 - 4 = 50`, so `lambda^2 - 15 lambda + 50 = 0`, discriminant `225 - 200 = 25`, roots `(15 +/- 5)/2 = 10` and `5`.
*`.p-check`:* `10 + 5 = 15` and `10 x 5 = 50`. Both match, and both roots are positive, which page `0405` will call positive definite.

**P2, `depth`.** Show that if `lambda` is an eigenvalue of an invertible `A`, then `1/lambda` is an eigenvalue of `A^-1`, and say why `lambda` cannot be zero.
*Hint:* Start from `Av = lambda v` and hit both sides with `A^-1`.
*Solution:* From `Av = lambda v`, apply `A^-1`: `v = lambda A^-1 v`. Since `A` is invertible, `det(A) != 0`, and because the determinant is the product of the eigenvalues, no eigenvalue is zero. So divide by `lambda`: `A^-1 v = (1/lambda) v`, and `v` is the same eigenvector.
*`.p-check`:* `det(A^-1) = 1/det(A)`, and the product of the reciprocals of the eigenvalues is indeed the reciprocal of their product.

## Code and dataset plan

`code/0402-characteristic-and-invariants.py`. Dataset `datasets/spectra.csv`.

Computes twice:
1. **From the definition,** on a 2x2 block of the channel covariance: build the characteristic polynomial's coefficients from `trace` and `det` and solve the quadratic with the formula.
2. **The library way,** `numpy.linalg.eigvals` on the same block.
3. **Asserts they agree**, then scales up: on the full 24x24 covariance it asserts `trace == sum(eigenvalues)` and `det == prod(eigenvalues)` to a stated tolerance, and **prints why the determinant assertion needs a relative tolerance** while the trace one does not. That contrast is the page's numerical honesty made executable: a product of 24 small numbers underflows toward zero and a sum of 24 small numbers does not.

## Sources

- Axler, *LADR* 4e, Chapter 5 for the characteristic polynomial, and Chapter 10 for the trace and determinant identities. `https://linear.axler.net/LADR4e.pdf`
- Deisenroth, Faisal and Ong, *MML*, Theorems 4.16 and 4.17. `https://mml-book.github.io/book/mml-book.pdf`
