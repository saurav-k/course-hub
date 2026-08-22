"""The law of large numbers, its proof, and the case where it fails.

Lesson: The law of large numbers.

    python3 0812-law-of-large-numbers.py

What it checks twice:

  1. The weak law's PROOF, made arithmetic. Chebyshev applied to the sample mean
     gives P(|Xbar - mu| >= eps) <= sigma^2 / (n eps^2). The program computes
     that bound and the measured probability side by side as n grows, so the
     reader watches the proof's own quantity go to zero.
  2. Convergence measured on real data: the sample mean of a heavy-tailed real
     column approaching its population mean.
  3. The failure. A Cauchy has no mean, and its running average never settles.
     The program shows the Cauchy running average is as spread out at n = 100,000
     as at n = 10, which is the honest statement of "it does not converge".
  4. The gambler's fallacy, killed with arithmetic: after a run of one-sided
     outcomes, the excess is DILUTED, never corrected. Both quantities printed.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "inference_runs.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/inference_runs.csv"
)
RNG = np.random.default_rng(20260831)


def load() -> pd.DataFrame:
    """Read the committed dataset, falling back to the published URL.

    The path is resolved from this file rather than the working directory, so the
    program runs from anywhere. The URL fallback is what lets it be pasted into
    Colab or a notebook with no checkout at all.
    """
    return pd.read_csv(DATA) if DATA.exists() else pd.read_csv(URL)


def main() -> None:
    frame = load()
    latency = frame["latency_ms"].to_numpy(dtype=float)
    mu, sigma = latency.mean(), latency.std()
    print(f"population: mean {mu:.4f} ms, sd {sigma:.4f} ms, {len(latency):,} rows\n")

    print("1. The proof, watched. Chebyshev on the sample mean.")
    print("   Var(Xbar) = sigma^2/n, so P(|Xbar - mu| >= eps) <= sigma^2/(n eps^2).")
    eps = 10.0
    print(f"\n   eps = {eps} ms")
    print(f"   {'n':>8}{'Chebyshev bound':>18}{'measured':>12}{'bound valid':>13}")
    for n in (10, 100, 1_000, 10_000):
        bound = min(1.0, sigma**2 / (n * eps**2))
        means = np.array([RNG.choice(latency, n, replace=True).mean() for _ in range(4_000)])
        measured = float((np.abs(means - mu) >= eps).mean())
        assert measured <= bound + 0.02, "Chebyshev should bound this"
        print(f"   {n:>8,}{bound:>18.6f}{measured:>12.6f}{'yes':>13}")
    print("\n   The bound has an n in the denominator, so it goes to zero, and the")
    print("   measured probability is squeezed to zero underneath it. That is the")
    print("   whole proof of the weak law: it is Chebyshev plus Var(Xbar)=sigma^2/n.")

    print("\n2. What convergence looks like, on one run")
    order = RNG.permutation(len(latency))
    running = np.cumsum(latency[order]) / np.arange(1, len(latency) + 1)
    print(f"   {'n':>8}{'running mean':>15}{'error':>12}{'sigma/sqrt(n)':>16}")
    for n in (10, 100, 1_000, 10_000, 40_000):
        print(
            f"   {n:>8,}{running[n - 1]:>15.4f}{running[n - 1] - mu:>12.4f}"
            f"{sigma / np.sqrt(n):>16.4f}"
        )
    print("   The error tracks sigma/sqrt(n) in size, and it is not monotone.")
    print("   Convergence is a trend, not a staircase.")

    print("\n3. Where it fails: a distribution with no mean")
    print("   A Cauchy's running average has the SAME distribution for every n.")
    print(f"   {'n':>8}{'normal: sd of Xbar':>22}{'cauchy: IQR of Xbar':>23}")
    for n in (10, 1_000, 100_000):
        normal_means = np.array([RNG.normal(0, 1, n).mean() for _ in range(2_000)])
        cauchy_means = np.array([RNG.standard_cauchy(n).mean() for _ in range(2_000)])
        iqr = float(np.percentile(cauchy_means, 75) - np.percentile(cauchy_means, 25))
        print(f"   {n:>8,}{normal_means.std():>22.6f}{iqr:>23.4f}")
    print("\n   The normal column shrinks like 1/sqrt(n), by a factor of 100 across")
    print("   these rows. The Cauchy column does not shrink at all. Averaging one")
    print("   hundred thousand Cauchy draws is no better than averaging ten.")
    print("   The strong law needs E|X| < infinity, and that is not a technicality:")
    print("   it is the difference between these two columns.")

    print("\n4. The gambler's fallacy, as arithmetic")
    print("   Ten heads in a row, then 10,000 more fair flips.")
    excess_start = 10.0
    trials = 20_000
    later = RNG.binomial(10_000, 0.5, trials) - 5_000.0
    total_excess = excess_start + later
    print(f"   mean excess heads after the later flips   {total_excess.mean():>10.4f}")
    print(f"   it started at                             {excess_start:>10.4f}")
    print("   The excess was not repaid. Its expectation is unchanged.")
    n_total = 10_010
    print(f"\n   but the excess as a FRACTION of all flips:")
    print(f"     after the run of 10:      {excess_start / 10:>10.6f}")
    print(f"     after 10,010 flips:       {total_excess.mean() / n_total:>10.6f}")
    print("   Diluted by a factor of a thousand, and never corrected. The law of")
    print("   large numbers is a statement about the second number, and people")
    print("   hear it as a promise about the first.")


if __name__ == "__main__":
    main()
