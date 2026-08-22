"""Covariance, correlation, and the covariance matrix.

Lesson: Covariance, correlation, and the covariance matrix (0082).

    python3 0805-covariance-correlation.py

What it checks twice:

  1. Cov(X, Y) = E[(X - mux)(Y - muy)] against E[XY] - E[X]E[Y], and against the
     centred dot product divided by n - 1. Three routes, one number. The third
     route is the one that matters later: covariance IS a dot product.
  2. Correlation as covariance over the two standard deviations, against
     pandas .corr(). And the Cauchy-Schwarz bound |r| <= 1 checked on every pair.
  3. The failure that matters: a column pair that is EXACTLY dependent and still
     has correlation zero. resid_energy is literally log_resid squared.
  4. Why squaring a skewed column does not demonstrate the same thing, with the
     third central moment computed to explain the difference.
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
COLUMNS = ["prompt_tokens", "output_tokens", "queue_depth", "gpu_util", "latency_ms"]


def load() -> pd.DataFrame:
    """Read the committed dataset, falling back to the published URL.

    The path is resolved from this file rather than the working directory, so the
    program runs from anywhere. The URL fallback is what lets it be pasted into
    Colab or a notebook with no checkout at all.
    """
    return pd.read_csv(DATA) if DATA.exists() else pd.read_csv(URL)


def covariance_three_ways(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    """Sample covariance by definition, by the computational form, and as a dot product."""
    n = len(x)
    xc, yc = x - x.mean(), y - y.mean()
    by_definition = float((xc * yc).sum() / (n - 1))
    by_computational = float((n / (n - 1)) * ((x * y).mean() - x.mean() * y.mean()))
    by_dot_product = float(np.dot(xc, yc) / (n - 1))
    return by_definition, by_computational, by_dot_product


def main() -> None:
    frame = load()
    n = len(frame)
    print(f"rows {n:,}\n")

    print("1. Covariance three ways, on prompt_tokens against output_tokens")
    x = frame["prompt_tokens"].to_numpy(dtype=float)
    y = frame["output_tokens"].to_numpy(dtype=float)
    definition, computational, dot = covariance_three_ways(x, y)
    print(f"   sum of centred products / (n-1)   {definition:.6f}")
    print(f"   E[XY] - E[X]E[Y], rescaled        {computational:.6f}")
    print(f"   centred dot product / (n-1)       {dot:.6f}")
    print(f"   pandas .cov()                     {frame['prompt_tokens'].cov(frame['output_tokens']):.6f}")
    assert np.isclose(definition, computational, rtol=1e-8)
    assert np.isclose(definition, dot, rtol=1e-12)
    print("   All four agree. The third is the one to remember: centre the two")
    print("   columns and covariance is their dot product, scaled by 1/(n-1).\n")

    print("2. Correlation, and what the denominator buys")
    pairs = (
        ("prompt_tokens", "output_tokens"),
        ("queue_depth", "gpu_util"),
        ("latency_ms", "screen_dpi"),
        ("latency_ms", "gpu_util"),
    )
    print(f"   {'pair':<32}{'covariance':>16}{'r by hand':>12}{'r pandas':>10}")
    for left, right in pairs:
        a = frame[left].to_numpy(dtype=float)
        b = frame[right].to_numpy(dtype=float)
        cov = covariance_three_ways(a, b)[0]
        by_hand = cov / (a.std(ddof=1) * b.std(ddof=1))
        by_pandas = float(frame[left].corr(frame[right]))
        assert np.isclose(by_hand, by_pandas, rtol=1e-8)
        assert abs(by_hand) <= 1.0 + 1e-12, "Cauchy-Schwarz violated"
        print(f"   {left + ' vs ' + right:<32}{cov:>16,.3f}{by_hand:>12.4f}{by_pandas:>10.4f}")
    print("\n   Read the covariance column on its own and you cannot rank these")
    print("   pairs: the units differ. The r column is comparable because the")
    print("   denominator divided the units out, and Cauchy-Schwarz is what")
    print("   forces every entry into [-1, 1].\n")

    print("3. Exactly dependent, and still uncorrelated")
    signal = frame["log_resid"].to_numpy(dtype=float)
    energy = frame["resid_energy"].to_numpy(dtype=float)
    reconstructed = signal**2
    print(f"   resid_energy equals log_resid squared, exactly? "
          f"{np.allclose(reconstructed, energy, atol=1e-3)}")
    print(f"   so knowing log_resid determines resid_energy with no error at all")
    print(f"   correlation between them                 r = {np.corrcoef(signal, energy)[0, 1]:>8.4f}")
    print(f"   correlation between |log_resid| and it   r = "
          f"{np.corrcoef(np.abs(signal), energy)[0, 1]:>8.4f}")
    print("\n   The first number is indistinguishable from zero. The second is near")
    print("   one. Same two columns; the only change is looking for the")
    print("   relationship that is actually there. Correlation answers exactly one")
    print("   question, 'how straight is this line', and answers it honestly.\n")

    print("4. Why the demonstration needs a SYMMETRIC column")
    print("   Cov(X, X^2) = E[X^3] - E[X]E[X^2], which for a centred column is the")
    print("   third central moment. Symmetric columns have zero third moment.")
    print(f"   {'column':<22}{'skew':>10}{'r with its own square':>24}")
    for name in ("log_resid", "output_tokens", "latency_ms", "screen_dpi"):
        column = frame[name].to_numpy(dtype=float)
        centred = column - column.mean()
        skew = float((centred**3).mean() / centred.std() ** 3)
        r = float(np.corrcoef(centred, centred**2)[0, 1])
        print(f"   {name:<22}{skew:>10.3f}{r:>24.4f}")
    print("\n   The two symmetric columns land on zero. The two skewed ones do not,")
    print("   and output_tokens reaches 0.65. An early draft of this dataset used")
    print("   that column and the demonstration silently failed.")


if __name__ == "__main__":
    main()
