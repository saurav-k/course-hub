"""0060 - Eigenvectors: the directions a matrix does not turn.

Computes the dominant eigenvector of a real covariance matrix two ways and
checks they agree: once from the definition by power iteration, once with
numpy.linalg.eigh. The interesting part of the check is the sign, which the
mathematics does not pin down and which the page says so on.

Needs numpy and pandas only. Run it anywhere:

    python3 0060-eigenvectors.py

Each program in this course is self-contained on purpose, including a copy of
the loader below, so that a single file pasted into Colab or a notebook runs
with no other file present.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

LOCAL = "../datasets/spectra.csv"
REMOTE = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/spectra.csv"
)


def load() -> pd.DataFrame:
    """Read the dataset from beside the course checkout, else over the network."""
    try:
        return pd.read_csv(LOCAL)
    except (FileNotFoundError, OSError):
        return pd.read_csv(REMOTE)


def covariance(values: np.ndarray) -> np.ndarray:
    """Sample covariance with the 1/(n-1) convention this course uses throughout.

    Rows are samples and columns are features (course convention D7), so the
    centring subtracts a per-column mean.
    """
    centred = values - values.mean(axis=0)
    return centred.T @ centred / (len(values) - 1)


def dominant_by_power_iteration(
    matrix: np.ndarray, steps: int = 500
) -> tuple[float, np.ndarray]:
    """The definition, run by hand: multiply, normalise, repeat.

    Each multiplication amplifies every eigendirection by its own eigenvalue, so
    the largest one wins and the vector swings onto it. Returns the Rayleigh
    quotient v^T A v, which is the eigenvalue once v has converged.
    """
    vector = np.ones(matrix.shape[0])
    vector /= np.linalg.norm(vector)
    for _ in range(steps):
        vector = matrix @ vector
        vector /= np.linalg.norm(vector)
    eigenvalue = float(vector @ matrix @ vector)
    return eigenvalue, vector


def main() -> None:
    frame = load()
    values = frame.drop(columns="sample_id").to_numpy(dtype=float)
    cov = covariance(values)
    print(f"{len(values)} samples, {values.shape[1]} channels")

    # Route 1: the definition.
    power_value, power_vector = dominant_by_power_iteration(cov)

    # Route 2: the library.
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    top = int(np.argmax(eigenvalues))
    library_value = float(eigenvalues[top])
    library_vector = eigenvectors[:, top]

    print(f"dominant eigenvalue, power iteration : {power_value:.12f}")
    print(f"dominant eigenvalue, numpy.linalg.eigh: {library_value:.12f}")
    assert np.isclose(power_value, library_value, rtol=1e-9), "eigenvalues disagree"

    # The eigenvectors agree only up to sign, because if A v = lambda v then
    # A (-v) = lambda (-v) just as truly. Comparing them directly would be a bug
    # that happens to pass whenever two routines make the same arbitrary choice.
    alignment = float(power_vector @ library_vector)
    print(f"v . v_library = {alignment:+.12f}  (magnitude is what must be 1)")
    assert np.isclose(abs(alignment), 1.0, atol=1e-8), "eigenvectors are not parallel"

    # The sign really is free, and this is a fact rather than a library quirk.
    flipped = -library_vector
    assert np.allclose(cov @ flipped, library_value * flipped), "flip should still solve"
    print("both v and -v satisfy A v = lambda v, so no code may branch on the sign")

    # The cheap check from the page, at a size nobody could do by hand.
    print(f"\ntrace(S)            = {np.trace(cov):.12f}")
    print(f"sum of eigenvalues  = {eigenvalues.sum():.12f}")
    assert np.isclose(np.trace(cov), eigenvalues.sum()), "trace check failed"

    share = library_value / eigenvalues.sum()
    print(f"\nthe dominant direction carries {share * 100:.2f}% of the total variance")


if __name__ == "__main__":
    main()
