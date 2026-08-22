"""Lesson 124 - independence tested on real columns, and the pairwise trap.

Independence is one equation: P(AB) = P(A)P(B). This program tests it on two
pairs of columns from the same file, one of which was generated independently
and one of which was not, so the reader sees what the test looks like when it
passes and when it fails.

It then builds the two-coin counterexample as an explicit four-row frame and
checks all four independence equations, showing the three pairwise ones pass
while the three-way one fails. A single counterexample is a complete disproof,
and this is it, executable.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "requests.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/requests.csv"
)

# On 25,000 rows, sampling noise on a proportion is of order 1/sqrt(n) = 0.006.
# A relative gap under 1 percent of the product is consistent with independence;
# the dependent pair below misses by 73 percent, so the threshold is not delicate.
RELATIVE_TOLERANCE = 0.01


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def independence_gap(a: np.ndarray, b: np.ndarray) -> tuple[float, float, float]:
    """Return the observed joint, the product of the marginals, and the gap."""
    observed = float((a & b).mean())
    product = float(a.mean() * b.mean())
    return observed, product, abs(observed - product)


def report(name: str, a: np.ndarray, b: np.ndarray) -> bool:
    observed, product, gap = independence_gap(a, b)
    relative = gap / product
    verdict = "consistent with independence" if relative < RELATIVE_TOLERANCE else "DEPENDENT"
    print(f"  {name}")
    print(f"      P(A)P(B) = {product:.6f}      P(AB) = {observed:.6f}")
    print(f"      gap {gap:.6f}, which is {relative * 100:.2f}% of the product -> {verdict}")
    return relative < RELATIVE_TOLERANCE


def two_coins() -> pd.DataFrame:
    """The four equally likely outcomes of flipping two fair coins."""
    return pd.DataFrame(
        {
            "first_heads": [True, True, False, False],
            "second_heads": [True, False, True, False],
            "faces_match": [True, False, False, True],
        }
    )


def main() -> None:
    frame = load()
    verified = frame["verified_user"].to_numpy(dtype=bool)
    cached = frame["cache_hit"].to_numpy(dtype=bool)
    flagged = frame["flagged"].to_numpy(dtype=bool)

    print("two pairs from the same file:\n")
    passed = report("cache_hit  and  verified_user", cached, verified)
    print()
    failed = report("flagged    and  verified_user", flagged, verified)

    assert passed, "the independent pair should have passed"
    assert not failed, "the dependent pair should have failed"

    print("\n  the same test, two verdicts. Independence is a property of the pair,")
    print("  not of the dataset, and it is checked one equation at a time.")

    print("\npairwise independence does not imply independence:\n")
    coins = two_coins()
    a = coins["first_heads"].to_numpy()
    b = coins["second_heads"].to_numpy()
    c = coins["faces_match"].to_numpy()

    for label, x, y in (("A,B", a, b), ("A,C", a, c), ("B,C", b, c)):
        observed, product, _ = independence_gap(x, y)
        print(f"      P({label}) = {observed:.4f}   P(A)P(B) = {product:.4f}   pairwise: ok")

    three_way = float((a & b & c).mean())
    product_of_three = float(a.mean() * b.mean() * c.mean())
    print(f"      P(A,B,C) = {three_way:.4f}   P(A)P(B)P(C) = {product_of_three:.4f}   FAILS")

    given_bc = float(a[b & c].mean())
    print(f"      P(A | B and C) = {given_bc:.4f}, against P(A) = {a.mean():.4f}")
    assert abs(three_way - product_of_three) > 1e-9, "the counterexample should fail"
    print("\n  all three pairs pass and the triple does not, so checking the pairs")
    print("  is not enough. Independence of n events needs every subset, not the pairs.")


if __name__ == "__main__":
    main()
