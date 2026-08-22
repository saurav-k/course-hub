"""Quantiles, percentiles, the IQR, and the box plot's fences.

DEFINITION. For 0 < q < 1, a q-quantile of a sample is a value Q such that at
least a fraction q of the data is <= Q and at least a fraction (1-q) is >= Q.
The median is the 0.5-quantile. Percentiles are quantiles named in hundredths.

RESULT (why a quantile is robust and a mean is not). Moving any observation
that lies strictly above the q-quantile further upwards leaves the q-quantile
unchanged, because it changes no order relation at the cut. The mean moves by
the shift divided by n. This is the breakdown-point argument in its simplest
form: a quantile at level q tolerates a fraction min(q, 1-q) of the data being
sent to infinity before it moves without bound, so the median tolerates 50 per
cent, while the mean tolerates a single observation.

NOTE ON DEFINITIONS. Sample quantiles need an interpolation rule when n*q is
not an integer, and there is more than one convention in use. numpy's default
is linear interpolation between order statistics, which is what pandas uses
too. The program prints two conventions so the reader sees that the choice is
real and small, rather than discovering it later as a mystery.

Dataset: nimbus-sessions.csv, column latency_ms.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

DATA = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-sessions.csv"


def quantile_lower(x: np.ndarray, q: float) -> float:
    """The 'lower' convention: the smallest order statistic at or past the cut."""
    s = np.sort(x)
    idx = int(np.ceil(q * s.size)) - 1
    return float(s[max(idx, 0)])


def main() -> None:
    df = pd.read_csv(DATA)
    x = df["latency_ms"].to_numpy(float)
    n = x.size
    print(f"n = {n:,} sessions, column latency_ms\n")

    print(f"{'q':>7}  {'linear (numpy default)':>23}  {'lower order statistic':>23}  {'gap':>8}")
    for q in (0.01, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 0.999):
        a = float(np.quantile(x, q))
        b = quantile_lower(x, q)
        print(f"{q:>7.3f}  {a:>23.2f}  {b:>23.2f}  {a - b:>8.2f}")
    print("  The two conventions differ by less than the measurement precision here,")
    print("  which is the usual case. They can differ visibly on small samples.")

    q1, q2, q3 = (float(np.quantile(x, q)) for q in (0.25, 0.5, 0.75))
    iqr = q3 - q1
    lo_fence, hi_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    print("\nthe five-number summary and the box plot it draws")
    print(f"  min {x.min():.2f}   Q1 {q1:.2f}   median {q2:.2f}   Q3 {q3:.2f}   max {x.max():.2f}")
    print(f"  IQR = Q3 - Q1 = {iqr:.2f} ms, the width of the middle half of the data")
    print(f"  fences at Q1 - 1.5*IQR = {lo_fence:.2f} and Q3 + 1.5*IQR = {hi_fence:.2f}")
    beyond = int((x > hi_fence).sum())
    print(f"  {beyond:,} sessions ({beyond / n:.2%}) sit beyond the upper fence")
    print("  The 1.5 is a convention, not a theorem. On a normal column it flags")
    print("  about 0.7 per cent of points; on this column it flags many more,")
    print("  because the column is not normal and the fence does not know that.")

    print("\nrobustness, measured rather than asserted")
    worst = int(np.argmax(x))
    for factor in (1, 10, 100, 1000):
        bumped = x.copy()
        bumped[worst] = x[worst] * factor
        print(f"  slowest session x{factor:<5}  mean {bumped.mean():>12.2f}"
              f"   median {float(np.median(bumped)):>8.2f}"
              f"   p95 {float(np.quantile(bumped, 0.95)):>9.2f}")
    print("  The mean tracks the single value it was given. The median and the p95")
    print("  do not move at all, because no order relation at their cut changed.")

    print("\nwhat a service-level objective is actually written in")
    for q in (0.50, 0.95, 0.99):
        print(f"  p{int(q * 100):<3} = {float(np.quantile(x, q)):>9.2f} ms")
    print(f"  mean = {x.mean():.2f} ms, which is above p{int((x < x.mean()).mean() * 100)}"
          f" of sessions: {(x < x.mean()).mean():.2%} of requests are faster than 'the average'.")


if __name__ == "__main__":
    main()
