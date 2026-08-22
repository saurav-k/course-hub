"""0410 - PCA through the SVD of the centred data matrix.

The module's centrepiece. Runs PCA two ways and checks they are the same thing:

  1. Form the covariance matrix and diagonalise it.
  2. Take the SVD of the centred data and use sigma_i^2 / (n-1), never forming
     the covariance matrix at all.

Then verifies the reconstruction identity directly: the average squared error
from keeping M directions equals the sum of the eigenvalues that were dropped.

Needs numpy and pandas only:  python3 0410-pca-through-the-svd.py
"""

from __future__ import annotations

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


def centred(values: np.ndarray) -> np.ndarray:
    """Subtract the per-column mean. Covariance is defined on deviations."""
    return values - values.mean(axis=0)

def pca_via_covariance(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Route 1: build S explicitly, then diagonalise it."""
    n = len(data)
    covariance = data.T @ data / (n - 1)
    eigenvalues, vectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1]
    return eigenvalues[order], vectors[:, order]


def pca_via_svd(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Route 2: SVD of the centred data. S is never formed."""
    n = len(data)
    _, singular, right = np.linalg.svd(data, full_matrices=False)
    return singular**2 / (n - 1), right.T


def main() -> None:
    data = centred(load_channels())
    n, d = data.shape
    print(f"centred data: {n} samples x {d} channels (rows are samples, D7)")

    cov_values, cov_directions = pca_via_covariance(data)
    svd_values, svd_directions = pca_via_svd(data)

    print("\neigenvalues, first six")
    print("  via covariance :", "  ".join(f"{v:.9f}" for v in cov_values[:6]))
    print("  via SVD        :", "  ".join(f"{v:.9f}" for v in svd_values[:6]))
    gap = float(np.abs(cov_values - svd_values).max())
    print(f"  largest disagreement anywhere: {gap:.3e}")
    assert gap < 1e-12, "the two routes should give the same eigenvalues"

    # Directions agree up to sign, and only up to sign.
    alignment = np.abs(np.einsum("ij,ij->j", cov_directions, svd_directions))
    print(f"\n|v_i . v_i| across all {d} directions: "
          f"min {alignment.min():.12f}, max {alignment.max():.12f}")
    assert np.allclose(alignment, 1.0), "directions should be parallel up to sign"

    # The sign freedom is a mathematical fact, not a quirk of a routine.
    covariance = data.T @ data / (n - 1)
    for i in (0, 1, 2):
        flipped = -cov_directions[:, i]
        assert np.allclose(covariance @ flipped, cov_values[i] * flipped)
    print("and -v solves S v = lambda v exactly as well as v does, so no code")
    print("may branch on the sign of a loading")
    same_sign = int((np.einsum("ij,ij->j", cov_directions, svd_directions) > 0).sum())
    print(f"(on this dataset the two routes happened to agree on {same_sign} of {d}")
    print(" signs, which is precisely why relying on that agreement is unsafe)")

    # The reconstruction identity, measured rather than trusted.
    print("\n  M | measured mean squared error | sum of discarded eigenvalues | gap")
    print("  " + "-" * 74)
    for m in (1, 2, 3, 4, 6, 12):
        basis = svd_directions[:, :m]
        rebuilt = data @ basis @ basis.T
        measured = float(((data - rebuilt) ** 2).sum() / (n - 1))
        discarded = float(svd_values[m:].sum())
        print(f"  {m:>2} | {measured:27.15f} | {discarded:28.15f} | "
              f"{abs(measured - discarded):.1e}")
        assert np.isclose(measured, discarded, rtol=1e-9, atol=1e-15), "identity failed"

    print("\nkeeping the largest eigenvalues and losing the smallest are the same act,")
    print("because the total is fixed:")
    print(f"  trace(S)           = {np.trace(covariance):.12f}")
    print(f"  sum of eigenvalues = {cov_values.sum():.12f}")
    assert np.isclose(np.trace(covariance), cov_values.sum())

    print("\n  k | eigenvalue | share of variance | cumulative")
    print("  " + "-" * 52)
    cumulative = np.cumsum(cov_values) / cov_values.sum()
    for k in range(6):
        print(f"  {k + 1} | {cov_values[k]:10.6f} | {cov_values[k] / cov_values.sum() * 100:16.4f}% | "
              f"{cumulative[k] * 100:9.4f}%")

    print("\nCumulative variance is a share of INPUT variance. It is not an accuracy")
    print("on any task, and PCA never saw a label. The cliff after k=4 is better")
    print("evidence than any percentage, and it was designed into this dataset.")


if __name__ == "__main__":
    main()
