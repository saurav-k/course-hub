"""The Central Limit Theorem, in both forms, and the n >= 30 rule measured.

Lesson: The Central Limit Theorem, for the sum and for the sample mean.

    python3 0813-central-limit-theorem.py

What it checks twice:

  1. Both standardisations. For the SUM, (S_n - n*mu) / (sigma*sqrt(n)). For the
     SAMPLE MEAN, (Xbar - mu) / (sigma/sqrt(n)). The program shows they are the
     same standardised quantity, which is why one theorem covers both, and a
     reader who has only seen one form usually thinks they are two theorems.
  2. Convergence in shape, measured by the largest gap between the empirical CDF
     of the standardised mean and the normal CDF, as n grows.
  3. Berry-Esseen: that gap must be at most 3*rho/(sigma^3*sqrt(n)). The program
     computes the bound and the realised gap side by side.
  4. The n >= 30 rule of thumb, tested rather than repeated: the true coverage of
     a nominal 95 percent interval, by distribution and by n.
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
RNG = np.random.default_rng(20260901)


def load() -> pd.DataFrame:
    """Read the committed dataset, falling back to the published URL.

    The path is resolved from this file rather than the working directory, so the
    program runs from anywhere. The URL fallback is what lets it be pasted into
    Colab or a notebook with no checkout at all.
    """
    return pd.read_csv(DATA) if DATA.exists() else pd.read_csv(URL)


def normal_cdf(z: np.ndarray) -> np.ndarray:
    """Phi(z) without scipy, using the erf built into numpy's math module."""
    from math import erf

    return np.array([0.5 * (1.0 + erf(v / np.sqrt(2.0))) for v in z])


def ks_gap(standardised: np.ndarray) -> float:
    """Largest absolute gap between the empirical CDF and the standard normal CDF."""
    ordered = np.sort(standardised)
    empirical = np.arange(1, len(ordered) + 1) / len(ordered)
    theoretical = normal_cdf(ordered)
    return float(np.max(np.abs(empirical - theoretical)))


def main() -> None:
    frame = load()
    latency = frame["latency_ms"].to_numpy(dtype=float)
    mu, sigma = latency.mean(), latency.std()
    print(f"latency: mean {mu:.4f}, sd {sigma:.4f}, skew {pd.Series(latency).skew():.4f}\n")

    print("1. The two forms are one standardisation")
    n, reps = 200, 5_000
    draws = RNG.choice(latency, size=(reps, n), replace=True)
    sums = draws.sum(axis=1)
    means = draws.mean(axis=1)
    z_sum = (sums - n * mu) / (sigma * np.sqrt(n))
    z_mean = (means - mu) / (sigma / np.sqrt(n))
    print(f"   sum form:        (S_n - n*mu) / (sigma*sqrt(n))")
    print(f"   sample-mean form:  (Xbar - mu) / (sigma/sqrt(n))")
    print(f"   largest gap between the two standardised samples: {np.abs(z_sum - z_mean).max():.2e}")
    assert np.allclose(z_sum, z_mean)
    print("   They are the same numbers. Dividing the sum by n divides the centre")
    print("   by n and the spread by n, so the ratio is untouched. One theorem.")
    print(f"\n   standardised mean over {reps:,} repeats: mean {z_mean.mean():>7.4f}, "
          f"sd {z_mean.std():>7.4f}")
    print("   (should be 0 and 1, and it is)")

    print("\n2. Convergence in shape, and 3. the Berry-Esseen bound on it")
    centred = latency - mu
    rho = float((np.abs(centred) ** 3).mean())
    print(f"   E|X - mu|^3 = rho = {rho:,.2f}, sigma^3 = {sigma**3:,.2f}")
    print(f"   so rho/sigma^3 = {rho / sigma**3:.4f}, and the bound is that over sqrt(n), times 3\n")
    print(f"   {'n':>8}{'measured CDF gap':>20}{'Berry-Esseen bound':>22}{'inside?':>10}")
    for n in (5, 30, 100, 1_000):
        draws = RNG.choice(latency, size=(20_000, n), replace=True)
        z = (draws.mean(axis=1) - mu) / (sigma / np.sqrt(n))
        gap = ks_gap(z)
        bound = 3.0 * rho / (sigma**3 * np.sqrt(n))
        print(f"   {n:>8,}{gap:>20.5f}{bound:>22.5f}{'yes' if gap <= bound else 'NO':>10}")
        assert gap <= bound, "Berry-Esseen violated"
    print("\n   The measured gap shrinks like 1/sqrt(n) and stays under the bound.")
    print("   Be honest about that bound though: a probability gap can never exceed")
    print("   1, so any row where the bound is above 1 is telling you nothing at")
    print("   all. With rho/sigma^3 = 3.43 here, 3*rho/(sigma^3*sqrt(n)) only drops")
    print("   below 1 past n = 107. Berry-Esseen is a statement about the RATE, and")
    print("   its constant is too loose to size a real sample with.")
    print("   Read the bound's shape: rho/sigma^3 is a skewness-like quantity, so")
    print("   the MORE SKEWED the source, the larger n has to be. That is the")
    print("   honest answer to 'how large is large enough', and it is not 30.")

    print("\n4. The n >= 30 rule, measured")
    print("   True coverage of a nominal 95% interval, xbar +/- 1.96*s/sqrt(n).")
    cases = {
        "normal(0,1)": (lambda k: RNG.normal(0, 1, k), 0.0),
        "latency_ms (real)": (lambda k: RNG.choice(latency, k, replace=True), mu),
        "exponential(1)": (lambda k: RNG.exponential(1.0, k), 1.0),
        "lognormal(0,2)": (lambda k: RNG.lognormal(0, 2, k), float(np.exp(2.0))),
        "cache_hit, p=0.012": (
            lambda k: RNG.choice(frame["cache_hit"].to_numpy(dtype=float), k, replace=True),
            float(frame["cache_hit"].mean()),
        ),
    }
    sizes = (10, 30, 100, 1_000)
    print(f"\n   {'distribution':<22}" + "".join(f"{f'n={s}':>10}" for s in sizes))
    for name, (draw, truth) in cases.items():
        row = ""
        for size in sizes:
            reps = 4_000
            covered = 0
            for _ in range(reps):
                sample = draw(size)
                half = 1.96 * sample.std(ddof=1) / np.sqrt(size)
                if sample.mean() - half <= truth <= sample.mean() + half:
                    covered += 1
            row += f"{covered / reps:>10.3f}"
        print(f"   {name:<22}{row}")
    print("\n   Read the n=30 column against the rule it is named after. A normal is")
    print("   fine. Real latency is passable. A 1.2 percent cache-hit rate is not")
    print("   close: the interval that claims 95 percent delivers a fraction of it,")
    print("   because at n=30 the expected number of hits is 0.36 and most samples")
    print("   contain none at all, which collapses the interval to a point.")
    print("\n   The rule that actually works for a proportion is n*p >= 10 and")
    print("   n*(1-p) >= 10. At p = 0.012 that needs n >= 833, which is why this")
    print("   row only becomes usable in the last column.")


if __name__ == "__main__":
    main()
