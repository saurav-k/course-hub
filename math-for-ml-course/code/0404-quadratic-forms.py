"""0404 - Quadratic forms: reading a matrix as a bowl, a saddle or a valley.

Brackets x^T S x over unit vectors two ways: by sampling many random directions,
and by reading the extreme eigenvalues. Sampling can only ever find values
inside the bracket, which is the point. Then confirms that rotating into the
eigenbasis removes the cross terms.

Needs numpy and pandas only:  python3 0404-quadratic-forms.py
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

def sample_form(matrix: np.ndarray, draws: int, seed: int) -> tuple[float, float]:
    """Evaluate x^T A x over random unit vectors and report the extremes found."""
    rng = np.random.default_rng(seed)
    directions = rng.normal(size=(draws, matrix.shape[0]))
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    quadratic = np.einsum("ij,jk,ik->i", directions, matrix, directions)
    return float(quadratic.min()), float(quadratic.max())


def main() -> None:
    cov = covariance(load_channels())
    eigenvalues = np.linalg.eigvalsh(cov)
    low, high = float(eigenvalues.min()), float(eigenvalues.max())

    print("x^T S x over unit vectors, on the 24x24 channel covariance")
    print(f"  from the spectrum : [{low:.9f}, {high:.9f}]")
    for draws in (1_000, 100_000):
        found_low, found_high = sample_form(cov, draws, seed=7)
        print(f"  {draws:>7,} samples : [{found_low:.9f}, {found_high:.9f}]")
        # Sampling can never escape the bracket, and gets closer as it grows.
        assert found_low >= low - 1e-12, "a sample fell below the smallest eigenvalue"
        assert found_high <= high + 1e-12, "a sample rose above the largest eigenvalue"

    print("\nsampling can only ever find values INSIDE the bracket, never outside,")
    print("which is why the two eigenvalues answer the question and sampling does not")

    # Rotating into the eigenbasis removes every cross term.
    _, Q = np.linalg.eigh(cov)
    rotated = Q.T @ cov @ Q
    off_diagonal = np.abs(rotated - np.diag(np.diag(rotated))).max()
    print(f"\nlargest off-diagonal entry of Q^T S Q : {off_diagonal:.3e}")
    assert off_diagonal < 1e-12, "the rotation should leave a diagonal matrix"
    print("so in the eigenbasis the form is a plain sum of squares, no cross terms")

    # The graph-Laplacian example from the page, worked at n = 5.
    print("\nthe Laplacian of a 5-node path, as a quadratic form:")
    adjacency = np.diag(np.ones(4), 1) + np.diag(np.ones(4), -1)
    laplacian = np.diag(adjacency.sum(axis=1)) - adjacency
    for name, labels in (("ramp", [1, 2, 3, 4, 5]), ("alternating", [1, 5, 1, 5, 1])):
        f = np.array(labels, dtype=float)
        by_matrix = float(f @ laplacian @ f)
        by_edges = float(sum((f[i] - f[i + 1]) ** 2 for i in range(4)))
        print(f"  {name:<12} f^T L f = {by_matrix:6.1f}   sum over edges = {by_edges:6.1f}")
        assert np.isclose(by_matrix, by_edges), "the two readings should agree"
    print("  the alternating labelling scores 16x rougher, which is what the form measures")


if __name__ == "__main__":
    main()
