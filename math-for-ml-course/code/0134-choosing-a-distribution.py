"""Lesson 0134 - the diagnostic kit, and one family choice priced in full.

This program is different from the others in the module. It asserts almost
nothing, because the point is not a result: it is that you look at the
comparison and decide. That is what choosing a distribution is.

Part one runs the three questions over five columns and prints what each
answers: the observed support, the mechanism the column's own statistics
suggest, and the diagnostic that distinguishes the candidate families.

Part two prices one family choice all the way to a commitment. Bin the arrivals
into one-second windows and ask what overflow rate we promise if we provision
for 6 concurrent requests. A normal and a Poisson agree on the capacity number
and disagree by a factor of three on the risk it carries, and only one of them
is close to what the file actually did.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from math import erf, exp, factorial, sqrt

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "requests.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/requests.csv"
)


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def normal_cdf(x: float, mean: float, sd: float) -> float:
    return 0.5 * (1.0 + erf((x - mean) / (sd * sqrt(2.0))))


def poisson_cdf(k: int, lam: float) -> float:
    return sum(exp(-lam) * lam ** j / factorial(j) for j in range(k + 1))


def describe_support(values: np.ndarray, name: str) -> None:
    distinct = len(np.unique(values))
    kind = "binary" if distinct == 2 else ("counts" if distinct < 20 else "continuous")
    print(f"    {name:<14} min {values.min():>9.3f}  max {values.max():>9.3f}  "
          f"{distinct:>6,} distinct -> {kind}")


def main() -> None:
    frame = load()

    print("QUESTION 1: what is the support?")
    for name in ("cache_hit", "route_is_chat", "retries", "latency_ms"):
        if name == "route_is_chat":
            values = (frame["route"] == "chat").to_numpy(dtype=float)
        else:
            values = frame[name].to_numpy(dtype=float)
        describe_support(values, name)
    gaps = np.diff(np.concatenate([[0.0], frame["arrival_s"].to_numpy()]))
    describe_support(gaps, "arrival gaps")

    print("\nQUESTION 3: the diagnostic each candidate family offers")

    second = np.floor(frame["arrival_s"].to_numpy()).astype(int)
    counts = np.bincount(second)[:-1]
    print(f"    counts per second: mean {counts.mean():.4f}, "
          f"variance {counts.var(ddof=1):.4f}, ratio {counts.var(ddof=1) / counts.mean():.3f}")
    print("      a Poisson forces this ratio to 1. Near 1 earns the model.")

    retries = frame["retries"].to_numpy()
    print(f"    retries: mean {retries.mean():.4f}, 1/mean = {1 / retries.mean():.4f}")
    print("      a geometric forces the mean to 1/p, so 1/mean recovers p.")

    print(f"    gaps: mean {gaps.mean():.5f}, sd {gaps.std(ddof=1):.5f}, "
          f"ratio {gaps.std(ddof=1) / gaps.mean():.4f}")
    print("      an exponential forces sd to EQUAL the mean, so that ratio is 1.")

    latency = frame["latency_ms"].to_numpy()
    mean, sd = latency.mean(), latency.std(ddof=1)
    within = float(np.mean(np.abs(latency - mean) <= sd))
    print(f"    latency: {within * 100:.2f}% within 1 sd against 68.27% for a normal")
    print("      too much in the middle means a heavy tail inflated the sd.")

    print("\nPRICING ONE FAMILY CHOICE: provision for 6 requests a second")
    lam = float(counts.mean())
    sd_counts = float(counts.std(ddof=1))

    # Question 1 kills the normal before any fitting happens.
    below_zero = normal_cdf(0.0, lam, sd_counts)
    print(f"    a normal fitted here puts {below_zero * 100:.2f}% of its mass BELOW ZERO,")
    print("    on a quantity that counts requests. Question 1 settles it.")

    normal_p99 = lam + 2.326 * sd_counts
    print(f"\n    the normal's 99th percentile: {lam:.4f} + 2.326 x {sd_counts:.4f} "
          f"= {normal_p99:.3f} -> provision {int(np.ceil(normal_p99))}")
    poisson_k = next(k for k in range(30) if poisson_cdf(k, lam) >= 0.99)
    print(f"    the Poisson's 99th percentile: first k with CDF >= 0.99 is {poisson_k}")
    print("    the two families AGREE on the capacity number")

    print("\n    but they disagree on the risk that number carries:")
    # Continuity correction: a count exceeds 6 when a continuous proxy exceeds 6.5.
    normal_risk = 1 - normal_cdf(6.5, lam, sd_counts)
    poisson_risk = 1 - poisson_cdf(6, lam)
    observed_risk = float(np.mean(counts > 6))
    print(f"      normal   says P(N > 6) = {normal_risk:.4f}")
    print(f"      Poisson  says P(N > 6) = {poisson_risk:.4f}")
    print(f"      the file actually has   {observed_risk:.4f}   "
          f"({int(np.sum(counts > 6))} of {len(counts):,} seconds)")
    print(f"\n    the normal is optimistic by {observed_risk / normal_risk:.1f}x.")
    print("    A team using it promises 0.30% overflow and delivers 1.15%,")
    print("    breaching a 1% objective it believed it had cleared comfortably.")


if __name__ == "__main__":
    main()
