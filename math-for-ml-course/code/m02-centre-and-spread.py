"""Centre and spread, computed from the definitions and checked against pandas.

THEOREM (deviations sum to zero). For any sample x_1..x_n with mean xbar,
    sum_i (x_i - xbar) = 0.
PROOF. sum_i (x_i - xbar) = sum_i x_i - n*xbar = n*xbar - n*xbar = 0. The mean
is the one constant with this property, which is why a spread built on raw
deviations would always be zero and why the definition squares them.

THEOREM (the mean is the least-squares centre). The value c minimising
    S(c) = sum_i (x_i - c)^2
is c = xbar.
PROOF. S'(c) = -2 * sum_i (x_i - c) = -2n(xbar - c), which is zero only at
c = xbar, and S''(c) = 2n > 0, so that stationary point is the minimum.

THEOREM (the median is the least-absolute-deviation centre). Any median m
minimises sum_i |x_i - c|.
PROOF SKETCH. For c not a data point, the derivative of sum_i |x_i - c| is
(number of x_i below c) - (number above c). It is negative while fewer than
half the points lie below c and positive once more than half do, so the sum
falls until c reaches the middle order statistic and rises after. The turning
point is the median.

Dataset: nimbus-sessions.csv, column latency_ms.
Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

DATA = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-sessions.csv"
# Or read it straight off the published site:
# DATA = "https://<hub>/math-for-ml-course/datasets/nimbus-sessions.csv"


def mean_from_definition(x: np.ndarray) -> float:
    return float(x.sum() / x.size)


def median_from_definition(x: np.ndarray) -> float:
    """The middle order statistic, or the average of the middle two."""
    s = np.sort(x)
    n = s.size
    mid = n // 2
    return float(s[mid]) if n % 2 else float((s[mid - 1] + s[mid]) / 2.0)


def variance_from_definition(x: np.ndarray, ddof: int) -> float:
    xbar = mean_from_definition(x)
    return float(((x - xbar) ** 2).sum() / (x.size - ddof))


def sum_of_squares_about(x: np.ndarray, c: float) -> float:
    return float(((x - c) ** 2).sum())


def sum_of_absolute_about(x: np.ndarray, c: float) -> float:
    return float(np.abs(x - c).sum())


def main() -> None:
    sessions = pd.read_csv(DATA)
    x = sessions["latency_ms"].to_numpy(dtype=float)
    n = x.size

    xbar = mean_from_definition(x)
    med = median_from_definition(x)

    print(f"n = {n:,} sessions\n")
    print("centre")
    print(f"  mean    from definition {xbar:12.4f}   pandas {sessions.latency_ms.mean():12.4f}")
    print(f"  median  from definition {med:12.4f}   pandas {sessions.latency_ms.median():12.4f}")
    print(f"  mode    (rounded to 10ms bins) {float(sessions.latency_ms.round(-1).mode().iloc[0]):.1f}")

    print("\nspread")
    s2 = variance_from_definition(x, ddof=1)
    print(f"  sample variance  (n-1)  {s2:14.4f}   pandas {sessions.latency_ms.var():14.4f}")
    print(f"  population var   (n)    {variance_from_definition(x, ddof=0):14.4f}"
          f"   pandas {sessions.latency_ms.var(ddof=0):14.4f}")
    print(f"  sample sd               {np.sqrt(s2):14.4f}   pandas {sessions.latency_ms.std():14.4f}")
    print("  the two variances differ because ddof does; pandas defaults to 1, numpy to 0")

    print("\ndeviations sum to zero")
    total = float((x - xbar).sum())
    print(f"  sum of (x - xbar) = {total:.6e}   (floating point, not algebra, is why it is not exactly 0)")
    print(f"  relative to the scale of the data: {abs(total) / float(np.abs(x).sum()):.3e}")

    print("\nthe mean minimises squared deviation, the median minimises absolute deviation")
    print(f"  {'candidate c':>22}  {'sum (x-c)^2':>18}  {'sum |x-c|':>14}")
    for label, c in (("mean", xbar), ("median", med), ("mean - 10", xbar - 10), ("median + 10", med + 10)):
        print(f"  {label:>22}  {sum_of_squares_about(x, c):18,.1f}  {sum_of_absolute_about(x, c):14,.1f}")
    print("  the smallest squared column is the mean's row; the smallest absolute column is the median's")

    print("\nwhat one outlier does")
    clean = x[x < np.quantile(x, 0.985)]
    print(f"  dropping the top 1.5% (the cold starts): n = {clean.size:,}")
    print(f"    mean   {mean_from_definition(clean):10.4f}  was {xbar:10.4f}"
          f"   moved {abs(mean_from_definition(clean) - xbar):9.4f} ms")
    print(f"    median {median_from_definition(clean):10.4f}  was {med:10.4f}"
          f"   moved {abs(median_from_definition(clean) - med):9.4f} ms")
    print("  the mean answers to every value, so it followed the tail out; the median answers to rank")


if __name__ == "__main__":
    main()
