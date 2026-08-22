"""M03 L09 - Span, linear independence, and basis.

    python3 m03-l09-span-basis.py

Two results, each checked twice.

1. Ax = b has a solution exactly when b lies in the span of the columns of A.
   Checked by solving, and again by testing whether adding b to the columns raises
   the rank: if it does, b was outside the span.
2. The expansion of a vector in a basis is unique. Checked by solving for the
   coefficients two different ways, and by confirming that a fourth vector in R^3
   must be dependent - the independence-dimension inequality, tested on 5,000
   random draws that never once come out independent.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "housing.csv"


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
        coeffs, residuals, *_ = np.linalg.lstsq(A, b, rcond=None)
        exact = np.allclose(A @ coeffs, b)
        print(
            f"  b = {label:<10} rank test says {in_span(A, b)!s:<5}"
            f" solve test says {exact!s:<5} coefficients {np.round(coeffs, 4)}"
        )
        assert in_span(A, b) == exact
    print("checked twice: the rank test and the solve test always agree")

    print("\n-- adding a dependent vector does not grow the span --")
    a3 = 2 * a1 + a2
    print(f"  rank[a1 a2]    = {np.linalg.matrix_rank(A)}")
    print(f"  rank[a1 a2 a3] = {np.linalg.matrix_rank(np.column_stack([a1, a2, a3]))}")
    print("  a3 was already reachable, so it adds nothing")

    print("\n-- the independence-dimension inequality, tested 5,000 times --")
    rng = np.random.default_rng(13)
    independent_fours = 0
    for _ in range(5_000):
        four = rng.normal(size=(3, 4))
        if np.linalg.matrix_rank(four) == 4:
            independent_fours += 1
    print(f"  four random vectors in R^3 came out independent {independent_fours} times in 5,000")
    print("  they cannot: an independent set of n-vectors has at most n members")
    assert independent_fours == 0

    print("\n-- a basis, and coordinates in it --")
    basis = np.column_stack([a1, a2, np.array([0.0, 0.0, 1.0])])
    print(f"  rank of the three = {np.linalg.matrix_rank(basis)}, so they are a basis of R^3")
    target = np.array([7.0, 11.0, 5.0])
    coords_solve = np.linalg.solve(basis, target)
    coords_lstsq, *_ = np.linalg.lstsq(basis, target, rcond=None)
    print(f"  coordinates of {target} in that basis: {np.round(coords_solve, 6)}")
    assert np.allclose(coords_solve, coords_lstsq)
    assert np.allclose(basis @ coords_solve, target)
    print("checked twice: two routes give the same coefficients, and they rebuild the vector")
    print(f"  the same point in the standard basis is just {target}: same point, two lists")

    print("\n-- the same idea on the data: which features are genuinely new? --")
    frame = pd.read_csv(DATA)
    cols = ["area_k_sqft", "bedrooms", "bathrooms", "age_years", "lot_sqft", "area_sqft"]
    M = frame[cols].to_numpy(dtype=float)
    print(f"  {len(cols)} feature columns over {M.shape[0]:,} rows")
    print(f"  rank = {np.linalg.matrix_rank(M)}, so one column is a combination of the others")
    without = frame[cols[:-1]].to_numpy(dtype=float)
    print(f"  drop area_sqft: rank = {np.linalg.matrix_rank(without)} of {without.shape[1]} columns")
    ratio = frame["area_sqft"].to_numpy(float) / frame["area_k_sqft"].to_numpy(float)
    print(f"  and the reason is visible: area_sqft / area_k_sqft is {ratio.min():.1f} for every row"
          f" (spread {ratio.max() - ratio.min():.2e})")


if __name__ == "__main__":
    main()
