"""0067 - The geometry of the SVD.

Checks that sigma_1 and sigma_min really do bracket how much a matrix can
stretch a unit vector, by sampling against the spectrum. Then applies V^T,
Sigma and U as three separate steps and shows the length changes only in the
middle one, which is the whole "rotate, stretch, rotate" reading.

Needs numpy and pandas only:  python3 0067-svd-geometry.py
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

def sampled_stretch(matrix: np.ndarray, draws: int, seed: int) -> tuple[float, float]:
    """Extremes of ||A x|| over random unit vectors x."""
    rng = np.random.default_rng(seed)
    directions = rng.normal(size=(draws, matrix.shape[1]))
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    lengths = np.linalg.norm(directions @ matrix.T, axis=1)
    return float(lengths.min()), float(lengths.max())


def main() -> None:
    data = centred(load_channels())
    # A small square map so every singular value is reachable by sampling.
    matrix = data[:6, :6]
    left, singular, right = np.linalg.svd(matrix)

    print("how much can this 6x6 map stretch a unit vector?")
    print(f"  from the spectrum : [{singular.min():.6f}, {singular.max():.6f}]")
    for draws in (1_000, 200_000):
        low, high = sampled_stretch(matrix, draws, seed=3)
        print(f"  {draws:>7,} samples : [{low:.6f}, {high:.6f}]")
        assert low >= singular.min() - 1e-9, "a sample shrank more than sigma_min"
        assert high <= singular.max() + 1e-9, "a sample stretched more than sigma_1"

    # sigma_1 is attained, and the vector that attains it is v_1.
    attained = np.linalg.norm(matrix @ right[0])
    print(f"\n||A v_1|| = {attained:.9f}   sigma_1 = {singular[0]:.9f}")
    assert np.isclose(attained, singular[0]), "v_1 should attain the maximum stretch"

    # The three motions, applied one at a time.
    rng = np.random.default_rng(5)
    x = rng.normal(size=6)
    x /= np.linalg.norm(x)
    after_v = right @ x
    after_sigma = singular * after_v
    after_u = left @ after_sigma
    print("\napplying the three factors in order to one unit vector:")
    print(f"  ||x||            = {np.linalg.norm(x):.9f}")
    print(f"  ||V^T x||        = {np.linalg.norm(after_v):.9f}   <- rotation, length unchanged")
    print(f"  ||Sigma V^T x||  = {np.linalg.norm(after_sigma):.9f}   <- the only step that scales")
    print(f"  ||U Sigma V^T x||= {np.linalg.norm(after_u):.9f}   <- rotation, length unchanged")
    assert np.isclose(np.linalg.norm(x), np.linalg.norm(after_v)), "V^T should preserve length"
    assert np.isclose(np.linalg.norm(after_sigma), np.linalg.norm(after_u)), "U should preserve length"
    assert np.allclose(after_u, matrix @ x), "the three steps should equal one multiply"

    # Volume: rotations do not change it, so only Sigma can.
    print(f"\n|det(A)|                    = {abs(np.linalg.det(matrix)):.6e}")
    print(f"product of singular values  = {np.prod(singular):.6e}")
    assert np.isclose(abs(np.linalg.det(matrix)), np.prod(singular), rtol=1e-9)
    print("equal, because rotations preserve volume and only the stretch changes it")

    print(f"\ncondition number sigma_1/sigma_min = {singular[0] / singular[-1]:.3f}")


if __name__ == "__main__":
    main()
