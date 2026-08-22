"""Lesson 49 - rank: the number of directions a matrix really has.

Three results, each checked twice.

1. Column rank equals row rank, via the factorisation A = CR. Checked by comparing
   the two counts, and again by rebuilding A from C and R exactly.
2. Rank-nullity: rank(A) + nullity(A) = n. The nullity is measured by counting the
   columns of a null-space basis built here from the echelon form rather than by a
   library routine, and checked against n - rank.
3. Collinearity destroys a fit. Measured on the sensor table with and without a
   duplicated column, and by exhibiting two different coefficient vectors that fit
   equally well.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "sensors.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/sensors.csv"

SENSORS = [
    "vibration_x", "vibration_y", "acoustic_db", "current_amp",
    "humidity_pct", "dust_index", "temp_c", "pressure_kpa",
]


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


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
    return A[:, pivots], Z[: len(pivots), :]


def null_space_basis(A: np.ndarray) -> np.ndarray:
    """A basis for {x : Ax = 0}, from the echelon form rather than from a library."""
    Z, pivots = rref(A)
    free = [c for c in range(A.shape[1]) if c not in pivots]
    basis = np.zeros((A.shape[1], len(free)))
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

    column_rank, row_rank = np.linalg.matrix_rank(A), np.linalg.matrix_rank(A.T)
    print(f"\ncolumn rank {column_rank}, row rank {row_rank}, and r from A = C R is {C.shape[1]}")
    assert column_rank == row_rank == C.shape[1]
    print("checked twice: the two counts agree, and both equal the inner dimension of C R")

    print("\n-- rank-nullity --")
    N = null_space_basis(A)
    print(f"  A is {A.shape[0]}x{A.shape[1]}, so n = {A.shape[1]}")
    print(f"  rank = {column_rank}, nullity = {N.shape[1]}, and they add to {column_rank + N.shape[1]} = n")
    print(f"  max |A @ N| = {np.abs(A @ N).max():.3e}, so every counted vector really is killed by A")
    assert column_rank + N.shape[1] == A.shape[1] and np.abs(A @ N).max() < 1e-9
    print("checked twice: the count matches n - rank, and A kills what it counted")

    print("\n-- the four subspaces, by dimension --")
    m, n = A.shape
    left_null = null_space_basis(A.T)
    print(f"  column space of A   , in R^{m}: dimension {column_rank}")
    print(f"  left null space of A, in R^{m}: dimension {left_null.shape[1]}   ({column_rank} + "
          f"{left_null.shape[1]} = {m})")
    print(f"  row space of A      , in R^{n}: dimension {row_rank}")
    print(f"  null space of A     , in R^{n}: dimension {N.shape[1]}   ({row_rank} + {N.shape[1]} = {n})")
    print(f"  the row space and the null space are orthogonal: max |A @ N| = {np.abs(A @ N).max():.3e}")

    print("\n-- rank as a budget --")
    d = 12_288
    print(f"  a full {d} x {d} weight matrix: {d * d:,} numbers")
    for r in (1, 4, 64):
        print(f"    rank {r:>3}: {2 * d * r:>12,} numbers, {100 * 2 * d * r / (d * d):.4f}% of full")
    total = 2 * (96 * 2) * d * 4
    print(f"  LoRA on two matrices in 96 layers at r = 4: {total:,} trainable parameters, "
          f"{total * 2 / 1e6:.1f} MB in fp16")

    print("\n-- collinearity, on the sensor table --")
    frame = load()
    X = np.column_stack([np.ones(len(frame))] + [frame[s].to_numpy(float) for s in SENSORS])
    Xd = np.column_stack([X, frame["vibration_x"].to_numpy(float) * 1000.0])
    truth = np.array([12.5, 3.2, -1.8, 0.9, 2.4, -0.6, 1.1, 0.35, 0.07])
    y = X @ truth + np.random.default_rng(20260822).normal(0.0, 2.0, len(frame))

    for label, M in (("without the copy", X), ("with the copy", Xd)):
        print(f"  {label:<18} columns {M.shape[1]}  rank {np.linalg.matrix_rank(M)}  "
              f"cond(X) {np.linalg.cond(M):.3e}")

    print("\n  and the coefficients stop being unique")
    beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    fit = np.linalg.norm(Xd @ beta - y)
    shifted = beta.copy()
    shifted[1] += 1000.0
    shifted[-1] -= 1.0
    print(f"    one solution has vibration_x coefficients {beta[1]:.4f} and {beta[-1]:.6f}")
    print(f"    shifting them by +1000 and -1 changes the residual by "
          f"{abs(np.linalg.norm(Xd @ shifted - y) - fit):.3e}")
    print("    two different coefficient vectors, one fit: that is what rank deficiency means")


if __name__ == "__main__":
    main()
