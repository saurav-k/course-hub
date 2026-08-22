"""Lesson 0129 - the Bernoulli family, and the binomial computed two ways.

Bernoulli, binomial and categorical are one idea at three widths. This program
fits all three to real columns and then does the binomial the hard way and the
easy way.

The binomial PMF is computed twice:

  1. Straight from the definition, with the binomial coefficient written out as
     a ratio of factorials. Correct, and it overflows for large n.
  2. By a multiplicative recurrence that never forms a factorial at all.

They agree to machine precision at n = 256, and the program then shows route 1
failing at n = 5000 where route 2 keeps working. That is the reason libraries
do not implement the formula as written.

It closes by comparing the theoretical binomial against the 97 real batches, so
the reader sees theory and a finite sample side by side.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from math import factorial

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "requests.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/requests.csv"
)

BATCH = 256


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def binomial_from_the_definition(n: int, k: int, p: float) -> float:
    """C(n, k) p^k (1-p)^(n-k), with the coefficient written out in full."""
    coefficient = factorial(n) / (factorial(k) * factorial(n - k))
    return coefficient * (p ** k) * ((1 - p) ** (n - k))


def binomial_by_recurrence(n: int, k: int, p: float) -> float:
    """The same number, built up one factor at a time.

    Start at P(X = 0) = (1-p)^n and step upward using
    P(X = j+1) = P(X = j) x (n - j) / (j + 1) x p / (1 - p).
    No factorial is ever formed, so nothing overflows.
    """
    value = (1 - p) ** n
    odds = p / (1 - p)
    for j in range(k):
        value *= (n - j) / (j + 1) * odds
    return value


def main() -> None:
    frame = load()

    print("BERNOULLI: one trial, one parameter")
    for column in ("cache_hit", "verified_user", "flagged"):
        p = float(frame[column].mean())
        print(f"    {column:<14} p = {p:.5f}   variance p(1-p) = {p * (1 - p):.5f}")
    print("    variance is largest at p = 0.5: a fair coin is the hardest to predict")

    print("\nCATEGORICAL: one trial, k states, k-1 free parameters")
    shares = frame["route"].value_counts(normalize=True)
    for state, share in shares.items():
        print(f"    {state:<8} {share:.4f}")
    print(f"    they sum to {shares.sum():.10f}, which is what makes it a distribution")

    print("\nBINOMIAL: n independent trials at the same p")
    p = float(frame["flagged"].mean())
    print(f"    n = {BATCH}, p = {p:.5f}, so the mean is {BATCH * p:.4f}")
    print("      k   from the definition   by recurrence      difference")
    for k in range(4):
        a = binomial_from_the_definition(BATCH, k, p)
        b = binomial_by_recurrence(BATCH, k, p)
        print(f"      {k}         {a:.6f}         {b:.6f}      {abs(a - b):.2e}")
        assert abs(a - b) < 1e-12, "the two routes disagree"

    print("\n    the two routes have DIFFERENT breaking points, and neither is safe")
    print("    everywhere. This is worth seeing rather than being told.")

    # Small k: the coefficient is modest, and both routes are fine. Python's
    # exact integers carry factorial(5000) - all 16,326 digits of it - and the
    # ratio comes back down to a float, so the definition survives. It is
    # enormously wasteful, and it is not wrong.
    print(f"      n = 5000, k = 3:    definition "
          f"{binomial_from_the_definition(5000, 3, 0.001):.8f}"
          f"   recurrence {binomial_by_recurrence(5000, 3, 0.001):.8f}")

    # Large k: C(5000, 2500) has 1,504 digits, which is far past the largest
    # float of about 1.8e308, so the coefficient cannot be converted at all.
    try:
        binomial_from_the_definition(5000, 2500, 0.5)
        print("      n = 5000, k = 2500: definition survived")
    except OverflowError as error:
        print(f"      n = 5000, k = 2500: definition OVERFLOWS - {error}")
    print(f"      n = 5000, k = 2500: recurrence "
          f"{binomial_by_recurrence(5000, 2500, 0.5):.8f} - which is UNDERFLOW,")
    print("        not an answer: it starts from (1-p)^n = 0.5^5000, already 0.")
    print("      The real answer is about 0.0113. Getting it needs log space,")
    print("      which is Module 10's subject, and neither route here can reach it.")

    print("\nTHEORY AGAINST 97 REAL BATCHES")
    flags = frame["flagged"].to_numpy(dtype=bool)
    n_batches = len(flags) // BATCH
    observed = flags[: n_batches * BATCH].reshape(n_batches, BATCH).sum(axis=1)
    counts = np.bincount(observed, minlength=5)
    print("      k   binomial says   the file says   batches")
    for k in range(5):
        print(f"      {k}      {binomial_by_recurrence(BATCH, k, p):.4f}"
              f"          {counts[k] / n_batches:.4f}        {counts[k]:3d}")
    print(f"\n    P(no flag in a batch of {BATCH}) = "
          f"{binomial_by_recurrence(BATCH, 0, p):.4f}")
    print(f"    P(no flag in a batch of 1024) = "
          f"{binomial_by_recurrence(1024, 0, p):.4f}")
    print("    that is why people oversample a rare class")


if __name__ == "__main__":
    main()
