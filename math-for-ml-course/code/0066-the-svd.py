"""0066 - The SVD: every matrix is a rotation, a stretch and a rotation.

Builds the SVD by following the existence proof literally: diagonalise A^T A,
take square roots for the singular values, then construct u_i = A v_i / sigma_i
and check they came out orthonormal. Compares against numpy.linalg.svd.

Also prints the rank two ways and shows they can disagree, which is the hook
page 0068 picks up.

Needs numpy and pandas only:  python3 0066-the-svd.py
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

def svd_from_the_proof(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Construct the SVD exactly as the existence proof does.

    Step 1: A^T A is symmetric positive semidefinite, so the spectral theorem
    gives it an orthonormal eigenbasis with non-negative eigenvalues.
    Step 2: sigma_i = sqrt(lambda_i), and u_i = A v_i / sigma_i where sigma_i > 0.
    """
    gram = matrix.T @ matrix
    eigenvalues, vectors = np.linalg.eigh(gram)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues, vectors = eigenvalues[order], vectors[:, order]
    # Tiny negatives are floating-point dust on an exactly-zero eigenvalue.
    singular = np.sqrt(np.clip(eigenvalues, 0.0, None))
    keep = singular > singular[0] * 1e-12
    left = (matrix @ vectors[:, keep]) / singular[keep]
    return left, singular[keep], vectors[:, keep].T


def main() -> None:
    data = centred(load_channels())
    print(f"centred data matrix: {data.shape[0]} x {data.shape[1]}")

    left, singular, right = svd_from_the_proof(data)
    lib_left, lib_singular, lib_right = np.linalg.svd(data, full_matrices=False)

    print("\nsingular values, first six")
    print("  from the proof :", "  ".join(f"{s:9.4f}" for s in singular[:6]))
    print("  from numpy.svd :", "  ".join(f"{s:9.4f}" for s in lib_singular[:6]))
    assert np.allclose(singular, lib_singular[: len(singular)]), "singular values differ"

    # Step 3 of the proof claimed the constructed u_i are orthonormal. Check it.
    gram_of_u = left.T @ left
    defect = np.abs(gram_of_u - np.eye(gram_of_u.shape[0])).max()
    print(f"\nmax |U^T U - I| for the CONSTRUCTED U: {defect:.3e}")
    assert defect < 1e-10, "the proof's construction should give orthonormal columns"

    # And the factorisation must rebuild the matrix.
    rebuilt = (left * singular) @ right
    print(f"max |U Sigma V^T - A|                : {np.abs(rebuilt - data).max():.3e}")
    assert np.allclose(rebuilt, data), "the factorisation should rebuild A"

    # Singular vectors agree only up to sign, exactly as eigenvectors do.
    alignment = np.abs(np.einsum("ij,ij->j", left[:, :4], lib_left[:, :4]))
    print(f"\n|u_i . u_i_library| for i=1..4: {np.round(alignment, 12)}")
    assert np.allclose(alignment, 1.0), "singular vectors should be parallel up to sign"
    print("magnitudes are 1, so the directions match; the signs are free")

    # Rank, two ways, and the two answers are both defensible.
    numerical = int(np.linalg.matrix_rank(data))
    print(f"\nrank by numpy.linalg.matrix_rank : {numerical}")
    print("counting singular values above a threshold:")
    for cut in (0.5, 1.0, 5.0, 10.0):
        print(f"  above {cut:>5.1f} : {int((lib_singular > cut).sum()):>3}")
    assert numerical == data.shape[1], "with noise present every singular value is non-zero"
    assert int((lib_singular > 5.0).sum()) == 4, "the four built-in components sit above the floor"
    print("\nEvery singular value is non-zero, so the numerical rank is full at 24.")
    print("But this matrix was built from four components plus noise, and only a")
    print("threshold placed INSIDE the cliff recovers that. Rank is not one number")
    print("here, it is a choice about where signal stops. Page 0068 makes the choice.")


if __name__ == "__main__":
    main()
