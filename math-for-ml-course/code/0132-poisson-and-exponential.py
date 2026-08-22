"""Lesson 0132 - one arrival stream, read as counts and as gaps.

The arrival_s column is a Poisson process. That single claim has two testable
consequences, and this program checks both against the same 25,000 arrivals:

  1. The count in a one-second window is Poisson(lambda).
  2. The gap between consecutive arrivals is Exponential(lambda).

The rate is estimated twice, once from the mean gap and once from the count per
window, and the two must agree - they are the same parameter seen through two
different windows onto one process.

It also computes the Poisson PMF two ways (an explicit factorial and a stable
recurrence), shows the Poisson limit of the binomial converging, tests
memorylessness on the real gaps, and demonstrates the scale trap that costs
people a factor of five.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from math import exp, factorial

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "requests.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/requests.csv"
)

SEED = 20260822
TRUE_RATE = 2.3


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def poisson_pmf_from_the_definition(k: int, lam: float) -> float:
    """lambda^k e^-lambda / k!, exactly as written. Overflows for large k."""
    return lam ** k * exp(-lam) / factorial(k)


def poisson_pmf_by_recurrence(k: int, lam: float) -> float:
    """Start at e^-lambda and step up with P(j+1) = P(j) x lambda / (j+1)."""
    value = exp(-lam)
    for j in range(k):
        value *= lam / (j + 1)
    return value


def exponential_tail(t: float, lam: float) -> float:
    """P(T > t) = e^(-lambda t). The gap survives past t only if nothing arrived."""
    return exp(-lam * t)


def main() -> None:
    frame = load()
    arrivals = frame["arrival_s"].to_numpy()
    gaps = np.diff(np.concatenate([[0.0], arrivals]))

    horizon = float(arrivals.max())
    second = np.floor(arrivals).astype(int)
    counts = np.bincount(second, minlength=int(np.floor(horizon)) + 1)[:-1]

    print("ONE PROCESS, TWO ESTIMATES OF THE SAME RATE")
    from_gaps = 1.0 / gaps.mean()
    from_counts = counts.mean()
    print(f"    mean gap {gaps.mean():.5f} s, so 1 / mean gap = {from_gaps:.4f} per second")
    print(f"    {len(arrivals):,} arrivals over {len(counts):,} one-second windows")
    print(f"                             = {from_counts:.4f} per second")
    print(f"    the generator used         {TRUE_RATE}")
    assert abs(from_gaps - from_counts) < 0.01, "the two estimates disagree"
    print("    a duration and a count give the same parameter, which is the")
    print("    whole claim that these are one process rather than two")

    lam = float(from_counts)

    print(f"\nCOUNTS in a one-second window, against Poisson({lam:.4f})")
    print("      k   observed   Poisson    definition vs recurrence")
    empirical = np.bincount(counts, minlength=9)[:9] / len(counts)
    for k in range(9):
        a = poisson_pmf_from_the_definition(k, lam)
        b = poisson_pmf_by_recurrence(k, lam)
        assert abs(a - b) < 1e-12, "the two Poisson routes disagree"
        print(f"      {k}    {empirical[k]:.4f}    {a:.4f}      agree to {abs(a - b):.0e}")
    print(f"    mean {counts.mean():.4f}, variance {counts.var(ddof=1):.4f}")
    print("    a Poisson forces variance to equal mean - that ratio is the diagnostic")

    print("\nGAPS, against the exponential")
    for t in (0.5, 1.0, 2.0):
        print(f"      P(gap > {t}) observed {float((gaps > t).mean()):.5f}   "
              f"formula {exponential_tail(t, lam):.5f}")

    print("\nMEMORYLESSNESS in continuous time")
    for s, t in ((0.5, 1.0), (1.0, 1.0)):
        survived = gaps[gaps > s]
        conditional = float((survived > s + t).mean())
        print(f"      P(gap > {s}+{t} | gap > {s}) = {conditional:.5f}   "
              f"against P(gap > {t}) = {float((gaps > t).mean()):.5f}   "
              f"on {survived.size:,} gaps")

    print("\nTHE POISSON LIMIT OF THE BINOMIAL, on this file's flag rate")
    p = float(frame["flagged"].mean())
    n = 256
    print(f"      binomial(n={n}, p={p:.5f}) against Poisson({n * p:.4f})")
    for k in range(4):
        binom = (
            np.prod([(n - j) / (j + 1) for j in range(k)])
            * p ** k
            * (1 - p) ** (n - k)
        )
        print(f"      k={k}   binomial {binom:.5f}   Poisson "
              f"{poisson_pmf_by_recurrence(k, n * p):.5f}")
    print("    many trials, each rare, product fixed - and the two agree to 4 places")

    print("\nTHE SCALE TRAP")
    rng = np.random.default_rng(SEED)
    right = rng.exponential(scale=1.0 / lam, size=200_000)
    wrong = rng.exponential(scale=lam, size=200_000)
    print(f"      rng.exponential(scale=1/lambda) mean {right.mean():.4f}  correct")
    print(f"      rng.exponential(scale=lambda)   mean {wrong.mean():.4f}  wrong by "
          f"{wrong.mean() / right.mean():.2f}x")
    print("      numpy and scipy take the SCALE, which is 1/lambda, not the rate")


if __name__ == "__main__":
    main()
