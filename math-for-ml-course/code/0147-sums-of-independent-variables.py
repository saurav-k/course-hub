"""Sums of independent random variables, and what survives the sum.

Lesson: Sums of independent random variables.

    python3 0808-sums-of-independent.py

What it checks twice:

  1. The mean and variance of a sum, predicted from the parts against measured
     from the sum, for independent and for dependent parts. Means always add;
     variances only add under independence.
  2. Convolution: the exact PMF of a sum of independent discrete variables, by
     numpy convolve against direct simulation. This is what "the distribution of
     a sum" means, and it is a convolution rather than a sum of distributions.
  3. Stability: a sum of independent normals is normal with the parameters
     adding, and a sum of independent Poissons is Poisson. Checked against the
     closed form. Most families are NOT stable, and the program shows one that
     is not, so the reader does not over-generalise.
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


def load() -> pd.DataFrame:
    """Read the committed dataset, falling back to the published URL.

    The path is resolved from this file rather than the working directory, so the
    program runs from anywhere. The URL fallback is what lets it be pasted into
    Colab or a notebook with no checkout at all.
    """
    return pd.read_csv(DATA) if DATA.exists() else pd.read_csv(URL)


def main() -> None:
    frame = load()
    print(f"rows {len(frame):,}\n")

    print("1. Mean and variance of a sum")
    cases = (
        ("independent (latency, dpi)  ", "latency_ms", "screen_dpi"),
        ("dependent   (prompt, output)", "prompt_tokens", "output_tokens"),
    )
    for label, left_name, right_name in cases:
        left = frame[left_name].to_numpy(dtype=float)
        right = frame[right_name].to_numpy(dtype=float)
        total = left + right
        print(f"\n   {label}")
        print(
            f"     mean:      measured {total.mean():>14,.3f}   "
            f"E[X]+E[Y] {left.mean() + right.mean():>14,.3f}"
        )
        assert np.isclose(total.mean(), left.mean() + right.mean())
        print(
            f"     variance:  measured {total.var():>14,.3f}   "
            f"Var+Var   {left.var() + right.var():>14,.3f}"
        )
        print(f"     the gap is 2Cov(X, Y) = {2 * np.cov(left, right, ddof=0)[0, 1]:>14,.3f}")
    print("\n   Means added in both rows. Variances added in one.")

    print("\n2. The distribution of a sum is a CONVOLUTION")
    print("   Two independent queue-depth-like counts, exact PMF against simulation.")
    rng = np.random.default_rng(20260827)
    pmf_a = np.array([0.10, 0.25, 0.30, 0.20, 0.10, 0.05])
    pmf_b = np.array([0.30, 0.40, 0.20, 0.10])
    exact = np.convolve(pmf_a, pmf_b)
    draws_a = rng.choice(len(pmf_a), size=400_000, p=pmf_a)
    draws_b = rng.choice(len(pmf_b), size=400_000, p=pmf_b)
    simulated = np.bincount(draws_a + draws_b, minlength=len(exact)) / 400_000
    print(f"   {'sum':>5}{'exact (convolve)':>20}{'simulated':>14}{'gap':>10}")
    for value, (e, s) in enumerate(zip(exact, simulated)):
        print(f"   {value:>5}{e:>20.5f}{s:>14.5f}{abs(e - s):>10.5f}")
    assert np.allclose(exact, simulated, atol=0.003), "convolution disagreed with simulation"
    assert np.isclose(exact.sum(), 1.0)
    print(f"   exact PMF sums to {exact.sum():.10f}")
    print("   Note what did NOT happen: the two PMFs were not added. Adding")
    print("   random variables convolves their distributions.")

    print("\n3. Which families survive being added, and which do not")
    size = 300_000
    normal_sum = rng.normal(3.0, 2.0, size) + rng.normal(-1.0, 1.5, size)
    print("   Normal(3, 2^2) + Normal(-1, 1.5^2)")
    print(f"     measured mean {normal_sum.mean():>8.4f}   predicted {3.0 - 1.0:>8.4f}")
    print(
        f"     measured sd   {normal_sum.std():>8.4f}   "
        f"predicted {np.sqrt(2.0**2 + 1.5**2):>8.4f}   (variances add, not sds)"
    )
    poisson_sum = rng.poisson(2.0, size) + rng.poisson(3.5, size)
    print("\n   Poisson(2.0) + Poisson(3.5)")
    print(f"     measured mean {poisson_sum.mean():>8.4f}   predicted {5.5:>8.4f}")
    print(f"     measured var  {poisson_sum.var():>8.4f}   predicted {5.5:>8.4f}")
    print("     mean equals variance, the Poisson signature, so the family survived.")
    uniform_sum = rng.uniform(0, 1, size) + rng.uniform(0, 1, size)
    counts, edges = np.histogram(uniform_sum, bins=10, range=(0, 2), density=True)
    print("\n   Uniform(0,1) + Uniform(0,1) is NOT uniform")
    print("     density by decile of the range 0 to 2:")
    print("    ", np.round(counts, 3))
    print("     A flat density would read 0.5 across. It is a triangle instead.")
    print("     Stability is a property of particular families, not of addition.")


if __name__ == "__main__":
    main()
