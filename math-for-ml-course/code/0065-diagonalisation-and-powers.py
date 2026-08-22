"""0065 - Diagonalisation and matrix powers.

Computes A^k two ways: by the sandwich P D^k P^-1, and by repeated
multiplication. Asserts they agree, then times both as k grows, where the point
lands: the sandwich pays for one eigendecomposition and then k scalar powers.

Also runs the routine on a defective matrix and reports the condition number of
P rather than crashing, showing how defectiveness announces itself numerically.

Needs numpy and pandas only:  python3 0065-diagonalisation-and-powers.py
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd

LOCAL = "../datasets/spectra.csv"
REMOTE = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/spectra.csv"
)


def load_channels() -> np.ndarray:
    """Read the dataset from beside the course checkout, else over the network.

    Rows are samples and columns are features, the course convention (D7).
    """
    try:
        frame = pd.read_csv(LOCAL)
    except (FileNotFoundError, OSError):
        frame = pd.read_csv(REMOTE)
    return frame.drop(columns="sample_id").to_numpy(dtype=float)


def covariance(values: np.ndarray) -> np.ndarray:
    """Sample covariance, 1/(n-1) convention, used everywhere in this course."""
    centred = values - values.mean(axis=0)
    return centred.T @ centred / (len(values) - 1)

def power_by_sandwich(matrix: np.ndarray, k: int) -> np.ndarray:
    """P D^k P^-1, using the symmetric routine since a covariance is symmetric."""
    eigenvalues, vectors = np.linalg.eigh(matrix)
    return vectors @ np.diag(eigenvalues**k) @ vectors.T


def main() -> None:
    cov = covariance(load_channels())

    for k in (2, 8):
        sandwich = power_by_sandwich(cov, k)
        repeated = np.linalg.matrix_power(cov, k)
        largest = np.abs(sandwich - repeated).max()
        scale = np.abs(repeated).max()
        print(f"k={k:>3}  max |P D^k P^-1 - A^k| = {largest:.3e}   "
              f"relative to {scale:.3e}")
        assert np.allclose(sandwich, repeated, rtol=1e-8, atol=1e-30), "routes disagree"

    print("\ncost as k grows (the eigendecomposition is paid once):")
    for k in (10, 200, 4000):
        start = time.perf_counter()
        power_by_sandwich(cov, k)
        sandwich_ms = (time.perf_counter() - start) * 1e3
        start = time.perf_counter()
        np.linalg.matrix_power(cov, k)
        repeated_ms = (time.perf_counter() - start) * 1e3
        print(f"  k={k:>5}   sandwich {sandwich_ms:7.3f} ms   "
              f"repeated multiply {repeated_ms:7.3f} ms")

    # A defective matrix has no usable P, and it says so through P's conditioning.
    print("\nthe same idea on a defective matrix, the shear [[1,1],[0,1]]:")
    shear = np.array([[1.0, 1.0], [0.0, 1.0]])
    _, vectors = np.linalg.eig(shear)
    condition = np.linalg.cond(vectors.real)
    print(f"  eigenvector matrix P =\n{vectors.real}")
    print(f"  cond(P) = {condition:.3e}")
    print("  both eigenvectors are the same direction, so P is singular and there")
    print("  is no P D P^-1. Yet the powers exist:")
    print(f"  shear^5 =\n{np.linalg.matrix_power(shear, 5)}")
    assert condition > 1e8, "a defective matrix should give a badly conditioned P"


if __name__ == "__main__":
    main()
