"""0061 - The characteristic equation, the trace and the determinant.

Solves a 2x2 eigenproblem from the characteristic polynomial and checks it
against the library, then scales the two invariant identities up to 24x24 where
one of them needs a relative tolerance and the other does not. That contrast is
the page's numerical honesty made executable.

Needs numpy and pandas only:  python3 0061-characteristic-and-invariants.py
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


def eigenvalues_from_characteristic(block: np.ndarray) -> tuple[float, float]:
    """The definition, for 2x2: solve lambda^2 - trace*lambda + det = 0."""
    trace = block[0, 0] + block[1, 1]
    determinant = block[0, 0] * block[1, 1] - block[0, 1] * block[1, 0]
    discriminant = trace * trace - 4.0 * determinant
    assert discriminant >= 0.0, "a symmetric 2x2 always has real eigenvalues"
    root = np.sqrt(discriminant)
    return (trace + root) / 2.0, (trace - root) / 2.0


def main() -> None:
    values = load_channels()
    cov = covariance(values)

    block = cov[:2, :2]
    print("the leading 2x2 block of the channel covariance:")
    print(block)

    by_hand = eigenvalues_from_characteristic(block)
    by_library = tuple(sorted(np.linalg.eigvalsh(block), reverse=True))
    print(f"\nfrom the characteristic equation: {by_hand[0]:.12f}  {by_hand[1]:.12f}")
    print(f"from numpy.linalg.eigvalsh      : {by_library[0]:.12f}  {by_library[1]:.12f}")
    assert np.allclose(by_hand, by_library), "the two routes disagree"

    # Now the full 24x24, where the polynomial route is hopeless and the two
    # invariants are still free.
    eigenvalues = np.linalg.eigvalsh(cov)
    trace = np.trace(cov)
    determinant = np.linalg.det(cov)

    print(f"\ntrace(S)           = {trace:.12e}")
    print(f"sum of eigenvalues = {eigenvalues.sum():.12e}")
    assert np.isclose(trace, eigenvalues.sum()), "trace identity failed"
    print("  -> holds to an absolute tolerance: a sum of 24 small numbers is well behaved")

    product = np.prod(eigenvalues)
    print(f"\ndet(S)                 = {determinant:.12e}")
    print(f"product of eigenvalues = {product:.12e}")
    # A product of 24 numbers each around 1e-3 is around 1e-72, which is near the
    # bottom of double precision. The identity is exact in mathematics and only
    # approximately checkable here, so the tolerance has to be relative.
    assert np.isclose(determinant, product, rtol=1e-6), "determinant identity failed"
    print("  -> needs a RELATIVE tolerance: a product of 24 small numbers underflows")
    print("     toward zero, so an absolute comparison would be meaningless")


if __name__ == "__main__":
    main()
