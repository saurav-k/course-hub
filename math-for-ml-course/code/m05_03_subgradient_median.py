"""M05 lesson 3 - two losses, two minimisers, and one missing derivative.

Implements the two named results:

    argmin_c  sum (x_i - c)^2   =  the mean      (derivative exists, one root)
    argmin_c  sum |x_i - c|     =  the median    (derivative does not exist,
                                                  and the minimising set is an
                                                  interval, not a point)

Run on five thousand real daily spends with a long right tail, where the two
answers are far apart, so the difference is a fact about the data and not a
contrived example.

The interval is the part worth seeing. For an even number of points every c
between the two middle values gives exactly the same total absolute error, so
"the median" names one point of a flat bottom.

    python3 m05_03_subgradient_median.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "datasets" / "m05-spend.csv"


def sse(x: np.ndarray, c: float) -> float:
    """Total squared error of the single summary c."""
    return float(np.sum((x - c) ** 2))


def sae(x: np.ndarray, c: float) -> float:
    """Total absolute error of the single summary c."""
    return float(np.sum(np.abs(x - c)))


def sse_derivative(x: np.ndarray, c: float) -> float:
    """d/dc sum (x_i - c)^2 = -2 sum (x_i - c). Defined everywhere."""
    return float(-2.0 * np.sum(x - c))


def sae_subgradient(x: np.ndarray, c: float) -> tuple[float, float]:
    """The subdifferential of sum |x_i - c| at c, as a closed interval.

    Away from every data point the derivative is (count below) - (count above).
    At a data point the two one-sided derivatives differ, and every slope
    between them supports the function. Ties contribute [-1, +1] each, which is
    exactly what widens the point into an interval.
    """
    below = int(np.sum(x < c))
    above = int(np.sum(x > c))
    ties = int(np.sum(x == c))
    return float(below - above - ties), float(below - above + ties)


def minimising_interval(x: np.ndarray) -> tuple[float, float]:
    """The whole set of minimisers of the absolute loss.

    For an even count it is the closed interval between the two middle order
    statistics. For an odd count it collapses to the single middle value.
    """
    ordered = np.sort(x)
    n = len(ordered)
    if n % 2 == 1:
        middle = ordered[n // 2]
        return float(middle), float(middle)
    return float(ordered[n // 2 - 1]), float(ordered[n // 2])


def main() -> None:
    frame = pd.read_csv(DATA)
    x = frame["spend_inr"].to_numpy(dtype=float)
    print(f"loaded {DATA.name}: {len(x)} rows\n")

    mean = float(np.mean(x))
    median = float(np.median(x))
    lo, hi = minimising_interval(x)

    print(f"mean   {mean:12.4f}")
    print(f"median {median:12.4f}")
    print(f"the two middle values are {lo:.2f} and {hi:.2f}\n")

    print("squared loss: the derivative exists and has one root")
    print(f"  d/dc at the mean   : {sse_derivative(x, mean):+.6e}   (zero, to rounding)")
    print(f"  d/dc at the median : {sse_derivative(x, median):+.6e}")
    print(f"  SSE at the mean    : {sse(x, mean):.4f}")
    print(f"  SSE at the median  : {sse(x, median):.4f}   (larger, as it must be)")

    print("\nabsolute loss: no derivative, and a flat bottom")
    print(f"  SAE at the mean            : {sae(x, mean):.4f}")
    print(f"  SAE at the median          : {sae(x, median):.4f}   (smaller, as it must be)")
    print(f"  SAE at the interval ends   : {sae(x, lo):.4f} and {sae(x, hi):.4f}")
    midpoint = (lo + hi) / 2.0
    print(f"  SAE at the interval middle : {sae(x, midpoint):.4f}")
    print(f"  SAE just outside, at {lo - 1:.2f}  : {sae(x, lo - 1.0):.4f}   (larger)")
    print(f"  SAE just outside, at {hi + 1:.2f}  : {sae(x, hi + 1.0):.4f}   (larger)")

    g_lo, g_hi = sae_subgradient(x, midpoint)
    print(f"\n  subgradient at the interval middle : [{g_lo:.0f}, {g_hi:.0f}]  contains zero")
    g_lo, g_hi = sae_subgradient(x, lo - 1.0)
    print(f"  subgradient one rupee below        : [{g_lo:.0f}, {g_hi:.0f}]  does not contain zero")

    print("\nrobustness, the reason any of this matters")
    worst = int(np.argmax(x))
    bumped = x.copy()
    bumped[worst] *= 10.0
    print(f"  multiply the single largest spend, Rs {x[worst]:.2f}, by ten:")
    print(f"    mean   {mean:10.4f} -> {np.mean(bumped):10.4f}")
    print(f"    median {median:10.4f} -> {np.median(bumped):10.4f}   (unchanged)")


if __name__ == "__main__":
    main()
