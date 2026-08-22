"""M03 L05 - A matrix product is a bag of dot products.

    python3 m03-l05-matmul.py

Two results, each checked twice.

1. The row reading and the column reading of A @ x are the same product. Computed
   once as one dot product per row and once as a weighted sum of columns.
2. Matrix multiplication is associative and is NOT commutative. Both are checked
   on real shapes taken from the housing table.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "housing.csv"
FEATURES = ["area_k_sqft", "bedrooms", "bathrooms", "age_years", "lot_sqft"]


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
    frame = pd.read_csv(DATA)
    X = frame[FEATURES].to_numpy(dtype=float)

    # A weight vector: a price per unit of each feature. A x is then one predicted
    # price per house, which is what a linear layer computes.
    w = np.array([232_000.0, 43_000.0, 21_000.0, -900.0, 3.1])

    small = X[:6]
    by_rows = matvec_by_rows(small, w)
    by_columns = matvec_by_columns(small, w)
    by_numpy = small @ w
    print("A @ x on six houses, three ways:")
    print(f"  by rows   : {np.round(by_rows, 2)}")
    print(f"  by columns: {np.round(by_columns, 2)}")
    print(f"  by numpy  : {np.round(by_numpy, 2)}")
    assert np.allclose(by_rows, by_columns) and np.allclose(by_rows, by_numpy)
    print("checked twice: the row reading and the column reading agree exactly")

    print(f"\nthe same product on all {X.shape[0]:,} houses is {X.shape[0]:,} dot products")
    print(f"  X.shape {X.shape} @ w.shape {w.shape} -> {(X @ w).shape}")

    print("\n-- the shape rule --")
    W = np.stack([w, w * 0.5, w * 2.0], axis=1)   # (5, 3): three price models at once
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
    print("  the two products do not even have the same shape, so they cannot be equal")

    print("\n-- but it IS associative, and the transpose reverses --")
    C = np.random.default_rng(2).normal(size=(3, 4))
    assert np.allclose((A @ B) @ np.eye(2), A @ (B @ np.eye(2)))
    left = (X[:50] @ W) @ np.ones((3, 2))
    right = X[:50] @ (W @ np.ones((3, 2)))
    print(f"  max |(XW)C - X(WC)| = {np.abs(left - right).max():.3e}")
    print(f"  max |(AB)^T - B^T A^T| = {np.abs((A @ B).T - B.T @ A.T).max():.3e}")
    assert np.allclose(left, right) and np.allclose((A @ B).T, B.T @ A.T)
    print("checked twice: associativity and the transpose rule both hold numerically")


if __name__ == "__main__":
    main()
