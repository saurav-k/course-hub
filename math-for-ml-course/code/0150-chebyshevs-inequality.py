"""Chebyshev's inequality, two-sided and one-sided.

Lesson: Chebyshev's inequality, one-sided and two-sided (0170).

    python3 0811-chebyshev.py

What it checks twice:

  1. The two-sided bound P(|X - mu| >= k*sigma) <= 1/k^2, checked on real data
     and on several distributions. It is a claim about EVERY distribution, so
     the program tries hard to break it.
  2. The proof, made arithmetic: Chebyshev is Markov applied to (X - mu)^2. The
     program runs Markov on that squared column and shows the same number comes
     out, so the reader sees it is not a new idea.
  3. Tightness: the three-point distribution that attains it exactly.
  4. The one-sided form, Cantelli: P(X - mu >= k*sigma) <= 1/(1 + k^2), which is
     strictly better than halving the two-sided bound, and the program shows a
     case where using 1/(2k^2) would be WRONG.
"""

from __future__ import annotations

from pathlib import Path

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "inference_runs.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/inference_runs.csv"
)
RNG = np.random.default_rng(20260830)


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
    print(f"latency: mean {mu:.3f}, sd {sigma:.3f}\n")

    print("1. Two-sided Chebyshev, on real data and on four distributions")
    families = {
        "latency_ms (real)": latency,
        "normal": RNG.normal(0, 1, 500_000),
        "uniform": RNG.uniform(-1, 1, 500_000),
        "exponential": RNG.exponential(1.0, 500_000),
        "lognormal(0, 1.5)": RNG.lognormal(0, 1.5, 500_000),
    }
    print(f"   {'distribution':<20}{'k':>4}{'bound 1/k^2':>14}{'true tail':>12}{'holds':>8}")
    for name, sample in families.items():
        m, s = sample.mean(), sample.std()
        for k in (2.0, 3.0):
            bound = 1.0 / k**2
            truth = float((np.abs(sample - m) >= k * s).mean())
            assert truth <= bound + 1e-9, f"Chebyshev violated by {name}"
            print(f"   {name:<20}{k:>4.0f}{bound:>14.6f}{truth:>12.6f}{'yes':>8}")
    print("   Held every time, on every shape. That universality is what it is for,")
    print("   and it is also why it is loose on any particular one.")

    print("\n2. The proof: Chebyshev IS Markov, applied to the squared deviation")
    k = 3.0
    squared = (latency - mu) ** 2
    threshold = (k * sigma) ** 2
    markov_on_squared = squared.mean() / threshold
    chebyshev = 1.0 / k**2
    print(f"   |X - mu| >= {k}*sigma is the same event as (X - mu)^2 >= ({k}*sigma)^2")
    print(f"   Markov on the squared column: E[(X-mu)^2] / ({k}sigma)^2 = {markov_on_squared:.10f}")
    print(f"   Chebyshev as usually written:                  1/{k}^2 = {chebyshev:.10f}")
    assert np.isclose(markov_on_squared, chebyshev, rtol=1e-6)
    print("   The same number, because E[(X-mu)^2] is the variance and it cancels.")
    print("   Squaring is the entire trick: it turns a two-sided event into a")
    print("   one-sided event about a non-negative quantity, which is what Markov")
    print("   needs. Nothing else was added.")

    print("\n3. Chebyshev is attained, so it cannot be improved")
    print("   Put mass 1/(2k^2) at -k, 1/(2k^2) at +k, and the rest at 0.")
    for k in (2.0, 3.0, 5.0):
        p_tail = 1.0 / (2 * k**2)
        values = np.array([-k, 0.0, k])
        probabilities = np.array([p_tail, 1 - 2 * p_tail, p_tail])
        m = float((values * probabilities).sum())
        var = float((probabilities * (values - m) ** 2).sum())
        truth = float(probabilities[[0, 2]].sum())
        bound = 1.0 / k**2
        print(
            f"   k={k:<4.0f} mean {m:>6.3f}  sd {np.sqrt(var):>6.4f}  "
            f"true tail {truth:.6f}  bound {bound:.6f}  ratio {truth / bound:.6f}"
        )
        assert np.isclose(truth, bound)
    print("   Ratio exactly 1 every time.")

    print("\n4. One-sided: Cantelli beats halving")
    print("   The two-sided bound is symmetric, so halving it is tempting. That")
    print("   is not valid, and the right one-sided bound is 1/(1 + k^2).")
    print(f"\n   {'k':>4}{'1/k^2 (two-sided)':>20}{'1/(2k^2) (wrong)':>20}{'1/(1+k^2)':>13}")
    for k in (1.0, 2.0, 3.0):
        print(f"   {k:>4.0f}{1 / k**2:>20.6f}{1 / (2 * k**2):>20.6f}{1 / (1 + k**2):>13.6f}")

    print("\n   A distribution where halving would be WRONG: put all the deviation")
    print("   on one side. X = 0 with probability 1-p and X = 1 with probability p.")
    for p in (0.2, 0.1):
        values = np.array([0.0, 1.0])
        probabilities = np.array([1 - p, p])
        m = float((values * probabilities).sum())
        s = float(np.sqrt((probabilities * (values - m) ** 2).sum()))
        k = (1.0 - m) / s
        truth = p
        halved = 1.0 / (2 * k**2)
        cantelli = 1.0 / (1 + k**2)
        verdict = "VIOLATED" if truth > halved else "ok"
        print(
            f"   p={p:<5} k={k:>6.3f}  true {truth:.4f}  "
            f"halved {halved:.4f} [{verdict}]  Cantelli {cantelli:.4f} [ok]"
        )
        assert truth <= cantelli + 1e-12, "Cantelli must never be violated"
    print("\n   Halving is violated by a distribution that is entirely one-sided,")
    print("   and Cantelli is attained by it exactly. Two-sided bounds do not")
    print("   halve, because the mass does not have to be symmetric.")


if __name__ == "__main__":
    main()
