"""Lesson 0128 - PMF, PDF and CDF, and the round trip between them.

Three descriptions of one object, and the program shows they really are one.

Discrete, on `retries`: build the PMF by counting, build the CDF by cumulative
sum, then recover the PMF from the CDF by differencing and assert it matches
the original. That round trip is the theorem "the PMF is the jump in the CDF",
executed.

Continuous, on `latency_ms`: build the empirical CDF two ways, once by sorting
and taking rank over n and once by counting rows at or below each threshold,
and assert they agree. Then show P(X = v) is zero for a continuous quantity by
counting exact ties, and show a density exceeding 1 on a narrow interval.

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


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def pmf_by_counting(values: np.ndarray) -> pd.Series:
    """P(X = k) for each attainable k, as a count over the total."""
    counts = pd.Series(values).value_counts().sort_index()
    return counts / len(values)


def cdf_from_pmf(pmf: pd.Series) -> pd.Series:
    """F(c) = P(X <= c), by accumulating the mass from the left."""
    return pmf.cumsum()


def pmf_from_cdf(cdf: pd.Series) -> pd.Series:
    """The jump in the CDF at each point, which is the mass sitting there."""
    return cdf.diff().fillna(cdf.iloc[0])


def empirical_cdf_by_sorting(values: np.ndarray, at: np.ndarray) -> np.ndarray:
    """F(c) from a sorted array: how far into the sort does c fall."""
    ordered = np.sort(values)
    return np.searchsorted(ordered, at, side="right") / len(values)


def empirical_cdf_by_counting(values: np.ndarray, at: np.ndarray) -> np.ndarray:
    """F(c) by asking, for each threshold, how many rows are at or below it."""
    return np.array([(values <= threshold).mean() for threshold in at])


def main() -> None:
    frame = load()

    print("DISCRETE: the retries column")
    retries = frame["retries"].to_numpy()
    pmf = pmf_by_counting(retries)
    cdf = cdf_from_pmf(pmf)
    recovered = pmf_from_cdf(cdf)

    print("     k     PMF      CDF    PMF recovered from the CDF")
    for k in pmf.index[:5]:
        print(f"    {k:2d}   {pmf[k]:.4f}   {cdf[k]:.4f}      {recovered[k]:.4f}")
    assert np.allclose(pmf.to_numpy(), recovered.to_numpy()), "the round trip failed"
    print("    the round trip closes: the PMF IS the jump in the CDF")
    print(f"    F(1.5) = {float((retries <= 1.5).mean()):.4f}, the same as F(1) - "
          f"a CDF is flat between attainable values")

    print("\nCONTINUOUS: the latency_ms column")
    latency = frame["latency_ms"].to_numpy()
    grid = np.array([150.0, 180.0, 200.0, 300.0])
    by_sorting = empirical_cdf_by_sorting(latency, grid)
    by_counting = empirical_cdf_by_counting(latency, grid)
    assert np.allclose(by_sorting, by_counting), "the two CDF routes disagree"
    for threshold, value in zip(grid, by_counting):
        print(f"    F({threshold:5.0f}) = {value:.4f}")
    print(f"    the 0.99 quantile is {np.quantile(latency, 0.99):.2f} ms, "
          f"which is a CDF statement read backwards")

    # For a genuinely continuous quantity every value is unique, so no single
    # value carries mass. This column is rounded to 2 decimals, so ties exist
    # from the rounding, and the program says so rather than pretending.
    unique = len(np.unique(latency))
    print(f"\n    distinct latency values: {unique:,} of {len(latency):,} rows")
    print("    ties here come from rounding to 2 decimals, not from real mass:")
    print("    for a continuous X, P(X = v) = 0 at every single v")

    print("\nA DENSITY IS NOT A PROBABILITY")
    for a, b in ((0.0, 0.5), (0.0, 4.0), (-0.07655, 0.07655)):
        width = b - a
        print(f"    Uniform({a}, {b}): width {width:.5f}, "
              f"density {1 / width:.4f}, area {width * (1 / width):.4f}")
    print("    the last one is Glorot's initialiser for a 512-to-512 layer")


if __name__ == "__main__":
    main()
