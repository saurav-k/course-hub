"""Lesson 0131 - the geometric distribution, and memorylessness tested on real data.

The retries column counts attempts until an upstream call succeeded, which is a
geometric random variable. This program does three things with it.

First it computes the PMF two ways, once from the formula (1-p)^(k-1) p and once
by counting the column, and prints them side by side.

Second it recovers p from the data. For a geometric the mean is 1/p, so 1/mean
should return the p the generator used.

Third, and this is the part worth running, it tests MEMORYLESSNESS directly:
P(L > n + k | L > n) should equal P(L > k) for every n and k. The program
computes both sides by filtering the actual column, and it reports how many rows
sit behind each estimate, because the deep-tail estimates rest on very few rows
and a program that hides that is lying.

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

# The generator's success probability, quoted from its docstring.
TRUE_P = 0.85


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def geometric_pmf(k: int, p: float) -> float:
    """P(L = k) = (1-p)^(k-1) p, on the trials-until-success convention.

    Support starts at k = 1, because you always run at least one trial. The
    other convention counts FAILURES BEFORE the first success and starts at 0,
    and its mean is (1-p)/p rather than 1/p.
    """
    return (1 - p) ** (k - 1) * p


def geometric_tail(k: int, p: float) -> float:
    """P(L > k) = (1-p)^k, because the first k trials all had to fail."""
    return (1 - p) ** k


def conditional_tail(values: np.ndarray, n: int, k: int) -> tuple[float, int]:
    """P(L > n + k | L > n), computed by filtering, with its sample size."""
    survived = values[values > n]
    if survived.size == 0:
        return float("nan"), 0
    return float((survived > n + k).mean()), int(survived.size)


def main() -> None:
    frame = load()
    retries = frame["retries"].to_numpy()

    print("the PMF, from the formula and from the column")
    observed = pd.Series(retries).value_counts(normalize=True).sort_index()
    print("      k   formula   observed   rows")
    counts = pd.Series(retries).value_counts().sort_index()
    for k in range(1, 6):
        print(f"      {k}    {geometric_pmf(k, TRUE_P):.4f}     "
              f"{observed.get(k, 0.0):.4f}   {int(counts.get(k, 0)):5d}")
    print(f"    largest value in the column: {retries.max()}")

    print("\nrecovering p from the data, because the mean is 1/p")
    mean = float(retries.mean())
    print(f"    observed mean      {mean:.4f}")
    print(f"    1 / mean           {1 / mean:.4f}   against a true p of {TRUE_P}")
    print(f"    theoretical mean   {1 / TRUE_P:.4f}")
    print(f"    the OTHER convention would predict a mean of "
          f"{(1 - TRUE_P) / TRUE_P:.4f},")
    print("    which is off by exactly one - that is the convention trap")

    print("\nthe tail, which is cleaner than the PMF")
    print("      k   formula   observed")
    for k in range(0, 4):
        print(f"      {k}    {geometric_tail(k, TRUE_P):.5f}   "
              f"{float((retries > k).mean()):.5f}")

    print("\nMEMORYLESSNESS: P(L > n+k | L > n) should equal P(L > k)")
    print("      n   k   conditional   unconditional   rows behind it")
    for n, k in ((1, 1), (1, 2), (2, 1)):
        conditional, sample = conditional_tail(retries, n, k)
        unconditional = float((retries > k).mean())
        print(f"      {n}   {k}     {conditional:.5f}       {unconditional:.5f}"
              f"        {sample:5d}")
    print("\n    Row 1 agrees to three decimals. Rows 2 and 3 wobble, for two")
    print("    different reasons worth telling apart:")
    print(f"      row 2 has 3,800 rows in the denominator but only "
          f"{int((retries > 3).sum())} in the numerator")
    print(f"      row 3 has only {int((retries > 2).sum())} rows in the denominator at all")
    print("    Both are sampling noise, not a failure of memorylessness. An")
    print("    estimate built on 77 rows is worth about two decimals, and")
    print("    saying how many decimals an estimate is worth is Module 09.")


if __name__ == "__main__":
    main()
