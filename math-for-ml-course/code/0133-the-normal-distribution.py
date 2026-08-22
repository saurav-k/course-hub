"""Lesson 0133 - the normal distribution, and where it stops describing the data.

Two halves.

First, the standard normal CDF computed two ways: once by numerically adding up
the area under the density on a fine grid, and once in closed form with erf.
The first is what a CDF IS, and seeing them agree to six decimals is the point.
No library is doing anything you have not been shown.

Second, the honest half. It fits a normal to latency_ms and reports the band
occupancies against what the normal predicts. On the bulk under 300 ms the fit
is almost exact. On the whole column it is not: there are 227 rows beyond three
standard deviations where the normal predicts 34, which is 6.7 times too many.

That table is generated here rather than typed on the page, so the warning the
page carries is evidence rather than assertion.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from math import erf, sqrt

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "requests.csv"
URL = (
    "https://raw.githubusercontent.com/saurav-k/course-hub/main/"
    "math-for-ml-course/datasets/requests.csv"
)

BULK_CUTOFF = 300.0


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def standard_normal_density(z: np.ndarray) -> np.ndarray:
    """The bell curve itself: exp(-z^2 / 2) divided by sqrt(2 pi)."""
    return np.exp(-(z ** 2) / 2.0) / np.sqrt(2.0 * np.pi)


def cdf_by_adding_up_the_area(z: float, steps: int = 200_000) -> float:
    """Phi(z), by trapezoid rule from -12 up to z.

    This is what a CDF is: the area under the density to the left of z. The
    lower limit of -12 is far enough out that the missing tail is about 1e-33.
    """
    grid = np.linspace(-12.0, z, steps)
    return float(np.trapezoid(standard_normal_density(grid), grid))


def cdf_in_closed_form(z: float) -> float:
    """The same Phi(z), from the error function."""
    return 0.5 * (1.0 + erf(z / sqrt(2.0)))


def band_table(values: np.ndarray, label: str) -> None:
    mean = float(values.mean())
    sd = float(values.std(ddof=1))
    print(f"    {label}: n = {len(values):,}, mean {mean:.2f}, sd {sd:.2f}")
    print("        within   observed   normal says    gap")
    for k in (1, 2, 3):
        observed = float(np.mean(np.abs(values - mean) <= k * sd))
        predicted = erf(k / sqrt(2.0))
        print(f"          {k} sd    {observed * 100:6.2f}%     {predicted * 100:6.2f}%"
              f"      {(observed - predicted) * 100:+6.2f} pp")
    beyond = int(np.sum(values > mean + 3 * sd))
    expected = (1 - cdf_in_closed_form(3.0)) * len(values)
    print(f"        beyond +3 sd: {beyond} rows observed, {expected:.1f} predicted"
          f"   ({beyond / expected:.1f}x)")


def main() -> None:
    print("THE CDF, two ways")
    print("        z    by adding up the area   from erf      difference")
    for z in (-2.0, -1.0, 0.0, 1.0, 2.0, 3.0):
        area = cdf_by_adding_up_the_area(z)
        closed = cdf_in_closed_form(z)
        print(f"    {z:+5.1f}          {area:.6f}         {closed:.6f}     "
              f"{abs(area - closed):.2e}")
        assert abs(area - closed) < 1e-6, "the two CDF routes disagree"
    print("    adding up the area IS the definition - erf is a faster route to it")

    print("\n    the three bands, from the closed form")
    for k in (1, 2, 3):
        inside = erf(k / sqrt(2.0))
        print(f"      within {k} sd: {inside * 100:7.4f}%   outside: "
              f"{(1 - inside) * 100:7.4f}%")

    frame = load()
    latency = frame["latency_ms"].to_numpy()
    bulk = latency[latency < BULK_CUTOFF]

    print("\nWHERE THE NORMAL FITS, AND WHERE IT DOES NOT")
    band_table(bulk, f"bulk only, under {BULK_CUTOFF:.0f} ms")
    print()
    band_table(latency, "the whole column")

    mean = float(bulk.mean())
    sd = float(bulk.std(ddof=1))
    print(f"\n    standardising one request against the bulk fit:")
    for value in (150.0, 240.0):
        print(f"      {value:.0f} ms -> z = ({value:.0f} - {mean:.2f}) / {sd:.2f} = "
              f"{(value - mean) / sd:+.4f}, "
              f"so P(slower than this) = {1 - cdf_in_closed_form((value - mean) / sd):.4f}")

    predicted_p99 = mean + 2.326 * sd
    actual_p99 = float(np.quantile(latency, 0.99))
    print(f"\n    99th percentile the bulk fit predicts: {predicted_p99:.1f} ms")
    print(f"    99th percentile the file actually has: {actual_p99:.2f} ms")
    print(f"    the normal is short by {actual_p99 - predicted_p99:.1f} ms, because")
    print("    the fit deliberately excluded the tail it is being asked about")


if __name__ == "__main__":
    main()
