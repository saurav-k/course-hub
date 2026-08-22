"""Lesson 48 - span, linear independence, and basis.

Two results, each checked twice.

1. Ax = b has a solution exactly when b lies in the span of the columns of A.
   Checked by solving, and again by testing whether appending b raises the rank:
   if it does, b was outside the span.
2. The independence-dimension inequality. Tested on 5,000 random draws of four
   vectors in R^3, none of which ever comes out independent, and again by the
   argument that says it cannot.

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


def in_span(columns: np.ndarray, b: np.ndarray) -> bool:
    """b is in the span of the columns exactly when appending it adds no rank."""
    return np.linalg.matrix_rank(columns) == np.linalg.matrix_rank(np.column_stack([columns, b]))


def main() -> None:
    a1 = np.array([2.0, 3.0, 1.0])
    a2 = np.array([1.0, 4.0, 2.0])
    A = np.column_stack([a1, a2])

    print("two vectors in R^3:")
    print(f"  a1 = {a1},  a2 = {a2}")
    print(f"  a1 + a2  = {a1 + a2}")
    print(f"  2a1 + a2 = {2 * a1 + a2}")
    print(f"  rank[a1 a2] = {np.linalg.matrix_rank(A)}, so their span is a plane, not all of R^3")

    print("\n-- is b in the span? two independent tests --")
    for label, b in (("2a1 + a2", 2 * a1 + a2), ("(1, 1, 1)", np.array([1.0, 1.0, 1.0]))):
        coeffs, *_ = np.linalg.lstsq(A, b, rcond=None)
        exact = np.allclose(A @ coeffs, b)
        print(f"  b = {label:<10} rank test {in_span(A, b)!s:<6} solve test {exact!s:<6} "
              f"coefficients {np.round(coeffs, 4)}")
        assert in_span(A, b) == exact
    print("checked twice: the rank test and the solve test always agree")

    print("\n-- adding a dependent vector does not grow the span --")
    a3 = 2 * a1 + a2
    print(f"  rank[a1 a2]    = {np.linalg.matrix_rank(A)}")
    print(f"  rank[a1 a2 a3] = {np.linalg.matrix_rank(np.column_stack([a1, a2, a3]))}")

    print("\n-- the independence-dimension inequality, tested 5,000 times --")
    rng = np.random.default_rng(13)
    independent = sum(np.linalg.matrix_rank(rng.normal(size=(3, 4))) == 4 for _ in range(5_000))
    print(f"  four random vectors in R^3 came out independent {independent} times in 5,000")
    assert independent == 0

    print("\n-- a basis, and coordinates in it --")
    basis = np.column_stack([a1, a2, np.array([0.0, 0.0, 1.0])])
    target = np.array([7.0, 11.0, 5.0])
    coords = np.linalg.solve(basis, target)
    coords_lstsq, *_ = np.linalg.lstsq(basis, target, rcond=None)
    print(f"  rank of the three = {np.linalg.matrix_rank(basis)}, so they are a basis of R^3")
    print(f"  coordinates of {target} in that basis: {np.round(coords, 6)}")
    assert np.allclose(coords, coords_lstsq) and np.allclose(basis @ coords, target)
    print("checked twice: two routes give the same coefficients, and they rebuild the vector")
    print(f"  the same point in the standard basis is just {target}: one point, two lists")

    print("\n-- the same question on the data: which sensors are genuinely new? --")
    frame = load()
    M = frame[SENSORS].to_numpy(dtype=float)
    print(f"  {M.shape[1]} sensor columns over {M.shape[0]:,} rows, rank {np.linalg.matrix_rank(M)}")
    with_copy = np.column_stack([M, M[:, 0] * 1000.0])
    print(f"  add vibration_x again in different units: {with_copy.shape[1]} columns, "
          f"rank {np.linalg.matrix_rank(with_copy)}")
    print("  the ninth column was already reachable, so the span did not grow")


if __name__ == "__main__":
    main()
