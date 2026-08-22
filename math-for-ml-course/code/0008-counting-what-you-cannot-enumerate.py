"""0008 - Counting what you cannot enumerate.

Checks the three theorems this lesson proves by brute force rather than
believing them: it enumerates every subset of a real 12-feature set and asserts
the count equals 2^12 and equals the sum of the binomial coefficients; it
verifies Pascal's rule across a triangle built two ways; and it computes SHAP's
factorial weights and asserts every cardinality layer contributes exactly 1/M.

Needs only numpy and pandas.
"""

from itertools import combinations
from math import comb, factorial

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "tickets.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/tickets.csv"


def load() -> pd.DataFrame:
    """Relative to this file so the repository works offline, URL so Colab works."""
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def choose_from_definition(n: int, k: int) -> int:
    """n!/(k!(n-k)!), which is the ordered count divided by the overcount k!."""
    ordered = factorial(n) // factorial(n - k)
    return ordered // factorial(k)


def main() -> None:
    frame = load()
    counts = pd.Series(
        [t for tokens in frame["tokens"] for t in tokens.split()]
    ).value_counts()
    features = list(counts.head(12).index)
    n = len(features)
    print(f"taking the {n} most common tokens as a feature set:")
    print(f"  {', '.join(features)}\n")

    # ---- theorem 3, by brute force ---------------------------------------
    enumerated = 0
    by_size = {}
    for k in range(n + 1):
        subsets = list(combinations(features, k))
        by_size[k] = len(subsets)
        enumerated += len(subsets)
        assert len(subsets) == choose_from_definition(n, k), f"C({n},{k}) is wrong"
    print(f"  enumerated every subset explicitly : {enumerated:,}")
    print(f"  2^{n}                              : {2 ** n:,}")
    print(f"  sum over k of C({n},k)              : {sum(by_size.values()):,}")
    assert enumerated == 2 ** n == sum(by_size.values()), "the subset sum failed"
    print(f"  all three agree, which is the theorem checked rather than believed")

    print(f"\n  by size: {[by_size[k] for k in range(n + 1)]}")
    print(f"  symmetric, because C(n,k) = C(n,n-k):", end=" ")
    assert all(by_size[k] == by_size[n - k] for k in range(n + 1))
    print("confirmed")

    # ---- Pascal's rule, two ways -----------------------------------------
    triangle = [[1]]
    for row in range(1, 13):
        previous = triangle[-1]
        triangle.append([1] + [previous[i] + previous[i + 1] for i in range(len(previous) - 1)] + [1])
    for row in range(13):
        for k in range(row + 1):
            assert triangle[row][k] == comb(row, k), "Pascal's triangle and C(n,k) disagree"
    for row in range(1, 13):
        for k in range(1, row):
            assert comb(row, k) == comb(row - 1, k - 1) + comb(row - 1, k), "Pascal's rule failed"
    print(f"\n  Pascal's rule holds for every interior cell of 13 rows")
    print(f"  row {n} is {triangle[n]}")
    print(f"  and it sums to {sum(triangle[n]):,} = 2^{n}")
    assert sum(triangle[n]) == 2 ** n

    # ---- ordered against unordered, the overcount ------------------------
    k = 5
    ordered = factorial(n) // factorial(n - k)
    unordered = choose_from_definition(n, k)
    print(f"\n  choosing {k} of {n}:")
    print(f"    ordered   {ordered:,}")
    print(f"    unordered {unordered:,}")
    print(f"    ratio     {ordered // unordered} = {k}!, the overcount the proof divides out")
    assert ordered // unordered == factorial(k)

    # ---- where the factorials go when you are not counting ---------------
    print(f"\nSHAP weights for a model with M = 15 features")
    M = 15
    total = 0.0
    for s in range(M):
        weight = factorial(s) * factorial(M - s - 1) / factorial(M)
        layer = comb(M - 1, s) * weight
        total += layer
        if s in (0, 7, M - 1):
            print(f"  size {s:>2}: C({M-1},{s}) = {comb(M-1,s):>5} subsets, "
                  f"weight {weight:.6e}, layer {layer:.6f}")
        assert abs(layer - 1 / M) < 1e-12, f"layer {s} should contribute exactly 1/{M}"
    print(f"  every one of the {M} layers contributes exactly 1/{M} = {1/M:.6f}")
    print(f"  and they sum to {total:.10f}, as a weighted average must")
    assert abs(total - 1.0) < 1e-12

    print(f"\n  coalitions to evaluate: 2^{M} = {2 ** M:,}")
    print(f"  at 1 ms each that is {2 ** M / 1000:.0f} s for ONE explanation")
    print(f"  at M = 20 it is 2^20 = {2 ** 20:,}, or {2 ** 20 / 60000:.1f} minutes")

    # ---- where enumeration stops being possible --------------------------
    print(f"\n  the wall, at one nanosecond per subset:")
    for size in (20, 30, 40, 60):
        seconds = 2 ** size / 1e9
        unit = f"{seconds:.1f} s" if seconds < 3600 else f"{seconds / 31_557_600:.1f} years"
        print(f"    2^{size} = {2 ** size:>20,}  ->  {unit}")

    print("\nall assertions passed")


if __name__ == "__main__":
    main()
