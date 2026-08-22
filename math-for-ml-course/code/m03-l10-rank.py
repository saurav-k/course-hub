"""M03 L10 - Rank: the number of directions a matrix really has.

    python3 m03-l10-rank.py

Three results, each checked twice.

1. Column rank equals row rank, via the factorisation A = CR. Checked by comparing
   the two counts directly, and again by rebuilding A from C and R exactly.
2. Rank-nullity: rank(A) + dim(null(A)) = n, the number of columns. The nullity is
   measured by counting the columns of an explicit null-space basis, built without
   a decomposition routine, and checked against n - rank.
3. Collinearity destroys a fit. Measured on the housing table with and without the
   redundant area column.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "housing.csv"

STRANG = np.array([[1.0, 2.0, 11.0, 17.0], [3.0, 7.0, 37.0, 57.0], [4.0, 9.0, 48.0, 74.0]])


def rref(A: np.ndarray, tol: float = 1e-9) -> tuple[np.ndarray, list[int]]:
    """Reduced row echelon form by Gauss-Jordan elimination, and the pivot columns."""
    M = A.astype(float).copy()
    rows, cols = M.shape
    pivots: list[int] = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        candidate = r + int(np.argmax(np.abs(M[r:, c])))
        if abs(M[candidate, c]) < tol:
            continue
        M[[r, candidate]] = M[[candidate, r]]
        M[r] = M[r] / M[r, c]
        for other in range(rows):
            if other != r and abs(M[other, c]) > tol:
                M[other] = M[other] - M[other, c] * M[r]
        pivots.append(c)
        r += 1
    return M, pivots


def factor_cr(A: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """A = C R, with C the independent columns of A and R the nonzero rows of rref(A)."""
    Z, pivots = rref(A)
    C = A[:, pivots]
    R = Z[: len(pivots), :]
    return C, R


def null_space_basis(A: np.ndarray) -> np.ndarray:
    """A basis for {x : Ax = 0}, built from the echelon form rather than from a library."""
    Z, pivots = rref(A)
    cols = A.shape[1]
    free = [c for c in range(cols) if c not in pivots]
    basis = np.zeros((cols, len(free)))
    for k, f in enumerate(free):
        basis[f, k] = 1.0
        for row, p in enumerate(pivots):
            basis[p, k] = -Z[row, f]
    return basis


def main() -> None:
    A = STRANG
    print("A =")
    print(A)
    C, R = factor_cr(A)
    print(f"\nA = C R with C {C.shape} and R {R.shape}")
    print("C =\n", C)
    print("R =\n", R)
    assert np.allclose(C @ R, A)
    print("checked: C @ R rebuilds A exactly")

    column_rank = np.linalg.matrix_rank(A)
    row_rank = np.linalg.matrix_rank(A.T)
    print(f"\ncolumn rank = {column_rank}, row rank = {row_rank}, r from A = C R is {C.shape[1]}")
    assert column_rank == row_rank == C.shape[1]
    print("checked twice: the two counts agree, and both equal the inner dimension of C R")

    print("\n-- rank-nullity --")
    N = null_space_basis(A)
    print(f"  A is {A.shape[0]}x{A.shape[1]}, so n = {A.shape[1]}")
    print(f"  rank    = {column_rank}")
    print(f"  nullity = {N.shape[1]}  (columns of an explicit null-space basis)")
    print(f"  rank + nullity = {column_rank + N.shape[1]} = n")
    print(f"  max |A @ N| = {np.abs(A @ N).max():.3e}, so every basis vector really is in the null space")
    assert column_rank + N.shape[1] == A.shape[1]
    assert np.abs(A @ N).max() < 1e-9
    print("checked twice: the count matches n - rank, and A kills every vector it counted")

    print("\n-- the four subspaces, by dimension --")
    m, n = A.shape
    left_null = null_space_basis(A.T)
    print(f"  column space of A   , in R^{m}: dimension {column_rank}")
    print(f"  null space of A     , in R^{n}: dimension {N.shape[1]}")
    print(f"  row space of A      , in R^{n}: dimension {row_rank}")
    print(f"  left null space of A, in R^{m}: dimension {left_null.shape[1]}")
    print(f"  the two in R^{n} add to {row_rank + N.shape[1]} = n; the two in R^{m} add to"
          f" {column_rank + left_null.shape[1]} = m")
    print(f"  and they are orthogonal: max |row space . null space| ="
          f" {np.abs(A @ N).max():.3e}")

    print("\n-- rank as a budget --")
    d = 12_288
    print(f"  a full {d} x {d} weight matrix: {d * d:,} numbers")
    for r in (1, 4, 64):
        print(f"    rank {r:>3}: {2 * d * r:>12,} numbers, {100 * 2 * d * r / (d * d):.4f}% of full")
    total = 2 * (96 * 2) * d * 4
    print(f"  LoRA on two matrices in 96 layers at r=4: {total:,} trainable parameters")
    print(f"    which is {total * 2 / 1e6:.1f} MB in fp16")

    print("\n-- collinearity, on the housing table --")
    frame = pd.read_csv(DATA)
    clean_cols = ["area_k_sqft", "bedrooms", "bathrooms", "age_years", "lot_sqft"]
    Xc = np.column_stack([np.ones(len(frame))] + [frame[c].to_numpy(float) for c in clean_cols])
    Xd = np.column_stack([Xc, frame["area_sqft"].to_numpy(float)])
    y = frame["price_usd"].to_numpy(float)

    for label, X in (("without area_sqft", Xc), ("with area_sqft", Xd)):
        rank = np.linalg.matrix_rank(X)
        cond = np.linalg.cond(X)
        G = X.T @ X
        print(f"  {label:<18} columns {X.shape[1]}  rank {rank}  cond(X) {cond:.3e}"
              f"  det(X^T X) {np.linalg.det(G):.3e}")

    print("\n  and it is not only a number: the coefficients stop being unique")
    beta_a, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    fit_a = np.linalg.norm(Xd @ beta_a - y)
    print(f"    a minimum-norm solution has area coefficients"
          f" {beta_a[1]:,.2f} per k-sqft and {beta_a[-1]:,.2f} per sqft")
    shifted = beta_a.copy()
    shifted[1] += 1000.0
    shifted[-1] -= 1.0
    print(f"    shifting them by +1000 and -1 changes the residual by"
          f" {abs(np.linalg.norm(Xd @ shifted - y) - fit_a):.3e}")
    print("    two different coefficient vectors, the same fit: that is what rank deficiency means")


if __name__ == "__main__":
    main()
