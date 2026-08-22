"""M03 L07 - A matrix is a function, and the determinant is its area factor.

    python3 m03-l07-linear-maps.py

Three results, each checked twice.

1. Column j of a matrix is the image of the j-th basis vector. Checked by reading
   the columns off, and again by applying the map to e1 and e2.
2. |det A| is the factor by which A scales area. Checked against the determinant
   routine, and again by measuring the area of the transformed unit square with the
   shoelace formula.
3. The cofactor expansion computes the same determinant as the library, on 3x3 and
   4x4 matrices. This is the compressed determinant treatment: the expansion is
   here so a reader has seen it, not because anyone should use it above 3x3.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "points2d.csv"


def rotation(theta: float) -> np.ndarray:
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def shoelace(polygon: np.ndarray) -> float:
    """Signed area of a closed polygon given as an ordered list of corners."""
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


MAPS: dict[str, np.ndarray] = {
    "rotate 30 deg": rotation(np.pi / 6),
    "dilate (2, 0.5)": np.array([[2.0, 0.0], [0.0, 0.5]]),
    "shear k=1.5": np.array([[1.0, 1.5], [0.0, 1.0]]),
    "collapse": np.array([[1.0, 2.0], [2.0, 4.0]]),
}

UNIT_SQUARE = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])


def main() -> None:
    points = pd.read_csv(DATA)
    P = points[["x", "y"]].to_numpy(dtype=float)
    print(f"{len(P):,} points in the plane, in groups {sorted(points.group.unique())}")

    e1, e2 = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    print(f"\n{'map':<17} {'M e1':>18} {'M e2':>18} {'det':>8} {'rank':>5}")
    for name, M in MAPS.items():
        assert np.allclose(M @ e1, M[:, 0]) and np.allclose(M @ e2, M[:, 1])
        print(
            f"{name:<17} {str(np.round(M @ e1, 4)):>18} {str(np.round(M @ e2, 4)):>18}"
            f" {np.linalg.det(M):>8.4f} {np.linalg.matrix_rank(M):>5}"
        )
    print("checked twice: M @ e_j equals column j of M, for every map above")

    print("\n-- the determinant is the area factor --")
    for name, M in MAPS.items():
        image = UNIT_SQUARE @ M.T
        measured = abs(shoelace(image))
        print(
            f"  {name:<17} |det| = {abs(np.linalg.det(M)):.6f}   "
            f"measured area of the image = {measured:.6f}"
        )
        assert abs(measured - abs(np.linalg.det(M))) < 1e-9
    print("checked twice: the shoelace area of the transformed unit square is |det|")

    print("\n-- applied to all 10,000 points --")
    for name, M in MAPS.items():
        image = P @ M.T
        spread = image.std(axis=0)
        print(
            f"  {name:<17} x std {spread[0]:.4f}  y std {spread[1]:.4f}  "
            f"mean radius {np.linalg.norm(image, axis=1).mean():.4f}"
        )
    print("  the rotation leaves every radius alone; the collapse puts all 10,000 on one line")
    collapsed = P @ MAPS["collapse"].T
    direction = collapsed / np.linalg.norm(collapsed, axis=1, keepdims=True)
    # Two, not one: the image is a line through the origin, and a line has two rays.
    print(f"  after the collapse, the number of distinct unit directions (to 6 dp): "
          f"{len(np.unique(np.round(direction, 6), axis=0))} - the two rays of one line")

    print("\n-- composition: the order is the matrix product, and it does not commute --")
    R, S = MAPS["rotate 30 deg"], MAPS["dilate (2, 0.5)"]
    v = np.array([1.0, 1.0])
    print(f"  S then R: (R @ S) @ v = {np.round((R @ S) @ v, 4)}")
    print(f"  R then S: (S @ R) @ v = {np.round((S @ R) @ v, 4)}")
    assert not np.allclose(R @ S, S @ R)

    print("\n-- determinants the compressed way: cofactor expansion against the library --")
    rng = np.random.default_rng(4)
    for n in (2, 3, 4):
        A = rng.integers(-5, 6, size=(n, n)).astype(float)
        mine, theirs = det_by_cofactor(A), float(np.linalg.det(A))
        print(f"  {n}x{n}: cofactor {mine:>12.4f}   numpy {theirs:>12.4f}   agree {abs(mine - theirs) < 1e-6}")
        assert abs(mine - theirs) < 1e-6
    print("checked twice: same number, two routes")
    print("  the expansion costs about n! multiplications, so it is a definition, not a method:")
    for n in (3, 5, 10, 20):
        print(f"    n = {n:>2}: about {math.factorial(n):,} terms")


if __name__ == "__main__":
    main()
