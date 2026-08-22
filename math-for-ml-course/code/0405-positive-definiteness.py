"""0405 - Positive definiteness and its eigenvalue test.

Tests definiteness two ways: by sampling the quadratic form, and by the smallest
eigenvalue. Then duplicates a channel and watches the smallest eigenvalue
collapse to zero while sampling stays stubbornly positive, because a random
vector almost never lands exactly on the null direction. That gap is why
"I sampled a lot and it was fine" is not a proof.

Needs numpy and pandas only:  python3 0405-positive-definiteness.py
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


def covariance(values: np.ndarray) -> np.ndarray:
    """Sample covariance, 1/(n-1) convention, used everywhere in this course."""
    centred = values - values.mean(axis=0)
    return centred.T @ centred / (len(values) - 1)

def sampled_minimum(matrix: np.ndarray, draws: int, seed: int) -> float:
    """Smallest value of x^T A x found over random unit vectors."""
    rng = np.random.default_rng(seed)
    directions = rng.normal(size=(draws, matrix.shape[0]))
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    return float(np.einsum("ij,jk,ik->i", directions, matrix, directions).min())


def main() -> None:
    values = load_channels()
    cov = covariance(values)

    smallest = float(np.linalg.eigvalsh(cov).min())
    sampled = sampled_minimum(cov, 200_000, seed=11)
    print("the 24 channels as measured:")
    print(f"  smallest eigenvalue            {smallest:.12f}")
    print(f"  smallest of 200,000 samples    {sampled:.12f}")
    assert smallest > 0.0, "this covariance should be positive definite"
    assert sampled >= smallest - 1e-12, "sampling cannot beat the smallest eigenvalue"
    print("  -> positive definite, decided by ONE number rather than 200,000")

    # Now make one channel an exact copy of another and repeat.
    duplicated = np.column_stack([values, values[:, 0]])
    cov_dup = covariance(duplicated)
    smallest_dup = float(np.linalg.eigvalsh(cov_dup).min())
    sampled_dup = sampled_minimum(cov_dup, 200_000, seed=11)
    print("\nwith channel 1 duplicated as a 25th column:")
    print(f"  smallest eigenvalue            {smallest_dup:.3e}")
    print(f"  smallest of 200,000 samples    {sampled_dup:.12f}")
    assert abs(smallest_dup) < 1e-12, "an exact duplicate should give a zero eigenvalue"
    assert sampled_dup > 1e-6, "random sampling should miss the null direction entirely"
    print("  -> semidefinite, NOT definite. Sampling never noticed.")

    # Build the null direction explicitly and evaluate there.
    null = np.zeros(duplicated.shape[1])
    null[0], null[-1] = 1.0, -1.0
    null /= np.linalg.norm(null)
    at_null = float(null @ cov_dup @ null)
    print(f"\nevaluated on the direction 'channel 1 minus its copy': {at_null:.3e}")
    assert abs(at_null) < 1e-12, "the form should vanish on the null direction"
    print("exactly zero, because that direction has no spread at all:")
    print("a duplicate column is an exact linear dependence, and the spectrum says so")

    # The X^T X fact needs no eigenvalue computation at all.
    centred = values - values.mean(axis=0)
    projected = centred @ np.linalg.eigh(cov)[1][:, :3]
    assert (np.einsum("ij,ij->i", projected, projected) >= 0).all()
    print("\nand every Gram matrix is semidefinite for free, because x^T X^T X x")
    print("is ||Xx||^2, a squared length, which cannot be negative")


if __name__ == "__main__":
    main()
