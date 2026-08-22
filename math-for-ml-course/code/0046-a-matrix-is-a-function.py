"""Lesson 46 - a matrix is a function, and the determinant is its area factor.

Three results, each checked twice.

1. Column j of a matrix is the image of the j-th basis vector: read off the
   columns, and again by applying the map to e1 and e2.
2. |det A| is the factor by which A scales area: against the determinant routine,
   and again by measuring the transformed unit square with the shoelace formula.
3. The cofactor expansion computes the same determinant as the library. This is
   the compressed determinant treatment - the expansion is here so a reader has
   seen it, not because anyone should use it above 3x3.

The maps are applied to 12,000 real points: the two vibration sensors, standardised,
which form a visibly elongated cloud because they correlate at 0.987.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "sensors.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/sensors.csv"

SENSORS = [
    "vibration_x", "vibration_y", "acoustic_db", "current_amp",
    "humidity_pct", "dust_index", "temp_c", "pressure_kpa",
]


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


import math


def rotation(theta: float) -> np.ndarray:
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def shoelace(polygon: np.ndarray) -> float:
    """Signed area of a closed polygon given as ordered corners."""
    x, y = polygon[:, 0], polygon[:, 1]
    return 0.5 * float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


def det_by_cofactor(A: np.ndarray) -> float:
    """The cofactor expansion along the first row. Correct, and O(n!) - see below."""
    n = A.shape[0]
    if n == 1:
        return float(A[0, 0])
    if n == 2:
        return float(A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0])
    total = 0.0
    for j in range(n):
        minor = np.delete(np.delete(A, 0, axis=0), j, axis=1)
        total += ((-1.0) ** j) * A[0, j] * det_by_cofactor(minor)
    return total


MAPS = {
    "rotate 30 deg": rotation(np.pi / 6),
    "dilate (2, 0.5)": np.array([[2.0, 0.0], [0.0, 0.5]]),
    "shear k=1.5": np.array([[1.0, 1.5], [0.0, 1.0]]),
    "collapse": np.array([[1.0, 2.0], [2.0, 4.0]]),
}
UNIT_SQUARE = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])


def main() -> None:
    frame = load()
    P = frame[["vibration_x", "vibration_y"]].to_numpy(dtype=float)
    P = (P - P.mean(axis=0)) / P.std(axis=0)
    print(f"{len(P):,} points: the two vibration sensors, standardised")
    print(f"they correlate at {np.corrcoef(P[:, 0], P[:, 1])[0, 1]:.4f}, so the cloud is a thin diagonal streak")

    e1, e2 = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    print(f"\n{'map':<17}{'M e1':>18}{'M e2':>18}{'det':>9}{'rank':>6}")
    for name, M in MAPS.items():
        assert np.allclose(M @ e1, M[:, 0]) and np.allclose(M @ e2, M[:, 1])
        print(f"{name:<17}{str(np.round(M @ e1, 4)):>18}{str(np.round(M @ e2, 4)):>18}"
              f"{np.linalg.det(M):>9.4f}{np.linalg.matrix_rank(M):>6}")
    print("checked twice: M @ e_j equals column j of M, for every map above")

    print("\n-- the determinant is the area factor --")
    for name, M in MAPS.items():
        measured = abs(shoelace(UNIT_SQUARE @ M.T))
        print(f"  {name:<17}|det| = {abs(np.linalg.det(M)):.6f}   measured area of the image = {measured:.6f}")
        assert abs(measured - abs(np.linalg.det(M))) < 1e-9
    print("checked twice: the shoelace area of the transformed unit square is |det|")

    print("\n-- applied to all 12,000 points --")
    for name, M in MAPS.items():
        image = P @ M.T
        print(f"  {name:<17}x std {image.std(axis=0)[0]:.4f}  y std {image.std(axis=0)[1]:.4f}  "
              f"mean radius {np.linalg.norm(image, axis=1).mean():.4f}")
    before = np.linalg.norm(P, axis=1)
    after = np.linalg.norm(P @ MAPS["rotate 30 deg"].T, axis=1)
    print(f"  the rotation changes no radius: max difference {np.abs(before - after).max():.3e}")
    collapsed = P @ MAPS["collapse"].T
    direction = collapsed / np.linalg.norm(collapsed, axis=1, keepdims=True)
    print(f"  the collapse leaves {len(np.unique(np.round(direction, 6), axis=0))} distinct unit directions "
          f"among 12,000 points - the two rays of one line")

    print("\n-- composition: the order is the product, and it does not commute --")
    R, S = MAPS["rotate 30 deg"], MAPS["dilate (2, 0.5)"]
    v = np.array([1.0, 1.0])
    print(f"  S then R, which is (R @ S) @ v = {np.round((R @ S) @ v, 4)}")
    print(f"  R then S, which is (S @ R) @ v = {np.round((S @ R) @ v, 4)}")
    assert not np.allclose(R @ S, S @ R)

    print("\n-- determinants, the compressed way: cofactor against the library --")
    rng = np.random.default_rng(4)
    for n in (2, 3, 4):
        A = rng.integers(-5, 6, size=(n, n)).astype(float)
        mine, theirs = det_by_cofactor(A), float(np.linalg.det(A))
        print(f"  {n}x{n}: cofactor {mine:>11.4f}   numpy {theirs:>11.4f}   agree {abs(mine - theirs) < 1e-6}")
        assert abs(mine - theirs) < 1e-6
    print("  checked twice: same number, two routes")
    print("  the expansion costs about n! multiplications, so it is a definition, not a method:")
    for n in (3, 5, 10, 20):
        print(f"    n = {n:>2}: about {math.factorial(n):,} terms")


if __name__ == "__main__":
    main()
