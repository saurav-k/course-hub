"""0403 - The spectral theorem for symmetric matrices.

Checks the theorem's three promises on a real symmetric matrix rather than
trusting them: real eigenvalues, orthonormal eigenvectors, and Q Lambda Q^T
reproducing the original. Then runs the same checks on a deliberately
non-symmetric matrix and watches the orthogonality promise fail, which is the
executable form of the page's misconception quiz.

Needs numpy and pandas only:  python3 0403-spectral-theorem.py
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

def orthonormality_defect(vectors: np.ndarray) -> float:
    """How far Q^T Q is from the identity. Zero means perfectly orthonormal."""
    gram = vectors.T @ vectors
    return float(np.abs(gram - np.eye(gram.shape[0])).max())


def main() -> None:
    cov = covariance(load_channels())
    assert np.allclose(cov, cov.T), "a covariance matrix is symmetric by construction"

    # Promise 1: the eigenvalues are real. Ask the general-purpose routine, which
    # does NOT assume symmetry, so it is free to return complex numbers.
    general = np.linalg.eigvals(cov)
    print(f"largest imaginary part returned by numpy.linalg.eigvals: "
          f"{np.abs(general.imag).max():.3e}")
    assert np.abs(general.imag).max() < 1e-12, "eigenvalues should be real"

    # Promise 2: an orthonormal basis of eigenvectors exists.
    eigenvalues, Q = np.linalg.eigh(cov)
    defect = orthonormality_defect(Q)
    print(f"max |Q^T Q - I| for the symmetric matrix : {defect:.3e}")
    assert defect < 1e-12, "eigenvectors should be orthonormal"

    # Promise 3: the factorisation reproduces the matrix.
    rebuilt = Q @ np.diag(eigenvalues) @ Q.T
    print(f"max |Q Lambda Q^T - S|                   : "
          f"{np.abs(rebuilt - cov).max():.3e}")
    assert np.allclose(rebuilt, cov), "Q Lambda Q^T should rebuild S"

    # The spectral sum: S as a stack of weighted rank-one projectors.
    stacked = sum(
        eigenvalues[i] * np.outer(Q[:, i], Q[:, i]) for i in range(len(eigenvalues))
    )
    print(f"max |sum lambda_i q_i q_i^T - S|         : "
          f"{np.abs(stacked - cov).max():.3e}")
    assert np.allclose(stacked, cov), "the spectral sum should rebuild S"

    # The contrast. Break the symmetry and the right angle goes with it.
    print("\nthe same three checks on a matrix that is NOT symmetric:")
    unsymmetric = np.array([[4.0, 1.0], [2.0, 3.0]])
    values, vectors = np.linalg.eig(unsymmetric)
    # eig returns complex arrays even when every root is real, so take the real
    # part before printing; the imaginary parts were asserted away above.
    vectors = vectors.real
    print(f"  eigenvalues {np.sort(values.real)[::-1]}  (real, but that was luck)")
    pair = float(vectors[:, 0] @ vectors[:, 1])
    print(f"  v_1 . v_2 = {pair:+.6f}  -> not zero, so NOT perpendicular")
    print(f"  max |V^T V - I| = {orthonormality_defect(vectors):.3f}")
    assert abs(pair) > 1e-6, "this matrix was chosen because its eigenvectors are not orthogonal"
    print("\nperpendicular eigenvectors come from SYMMETRY, not from being eigenvectors")


if __name__ == "__main__":
    main()
