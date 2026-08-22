"""Lesson 64 - a matrix product is a bag of dot products.

Two results, each checked twice.

1. The row reading and the column reading of A @ x are the same product. Computed
   once as one dot product per row and once as a weighted sum of the columns.
2. Matrix multiplication is associative and is NOT commutative, and the transpose
   of a product reverses the order. All three checked on real shapes.

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


def matvec_by_rows(A: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Entry i of the output is the dot product of row i with x."""
    return np.array([A[i] @ x for i in range(A.shape[0])])


def matvec_by_columns(A: np.ndarray, x: np.ndarray) -> np.ndarray:
    """The output is a linear combination of the columns, weighted by x."""
    out = np.zeros(A.shape[0])
    for j in range(A.shape[1]):
        out = out + x[j] * A[:, j]
    return out


def main() -> None:
    X = load()[SENSORS].to_numpy(dtype=float)
    # A health score: one weight per sensor. X @ w is one score per reading,
    # which is exactly what a linear layer computes.
    w = np.array([0.8, 0.8, 1.5, 2.0, -0.4, -0.6, 0.9, 0.05])

    small = X[:6]
    by_rows = matvec_by_rows(small, w)
    by_columns = matvec_by_columns(small, w)
    print("A @ x on six readings, three ways:")
    print(f"  by rows   : {np.round(by_rows, 4)}")
    print(f"  by columns: {np.round(by_columns, 4)}")
    print(f"  by numpy  : {np.round(small @ w, 4)}")
    assert np.allclose(by_rows, by_columns) and np.allclose(by_rows, small @ w)
    print("checked twice: the row reading and the column reading agree exactly")

    print(f"\nthe same product on all {X.shape[0]:,} readings is {X.shape[0]:,} dot products")
    print(f"  X.shape {X.shape} @ w.shape {w.shape} -> {(X @ w).shape}")

    print("\n-- the shape rule --")
    W = np.stack([w, w * 0.5, w * 2.0], axis=1)
    print(f"  X {X.shape} @ W {W.shape} -> {(X @ W).shape}")
    try:
        _ = W @ X
    except ValueError as exc:
        print(f"  W {W.shape} @ X {X.shape} -> ValueError: {str(exc).split(' (')[0]}")

    print("\n-- AB is not BA --")
    A = np.array([[-1.5, 3.0, 2.0], [1.0, -1.0, 0.0]])
    B = np.array([[-1.0, -1.0], [0.0, -2.0], [1.0, 0.0]])
    print(f"  A is {A.shape}, B is {B.shape}")
    print(f"  AB is {(A @ B).shape}:\n{A @ B}")
    print(f"  BA is {(B @ A).shape}:\n{B @ A}")
    print("  different shapes, so equality is not even a question that can be asked")

    print("\n-- associativity, and the transpose rule --")
    left = (X[:50] @ W) @ np.ones((3, 2))
    right = X[:50] @ (W @ np.ones((3, 2)))
    print(f"  max |(XW)C - X(WC)|    = {np.abs(left - right).max():.3e}")
    print(f"  max |(AB)^T - B^T A^T| = {np.abs((A @ B).T - B.T @ A.T).max():.3e}")
    assert np.allclose(left, right) and np.allclose((A @ B).T, B.T @ A.T)
    print("checked twice: both identities hold numerically")


if __name__ == "__main__":
    main()
