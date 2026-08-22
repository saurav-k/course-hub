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

Dataset: sessions.csv, column session_seconds.
Needs numpy and pandas only.

----------------------------------------------------------------------
ALSO ON THIS PAGE: Bessel's correction, and why the sample variance divides by n-1
----------------------------------------------------------------------

Bessel's correction: why the sample variance divides by n-1.

THEOREM. Let X_1..X_n be independent draws with mean mu and variance sigma^2,
and let Xbar be the sample mean. Then
    E[ sum_i (X_i - Xbar)^2 ] = (n - 1) * sigma^2,
so  s^2 = sum_i (X_i - Xbar)^2 / (n - 1)  satisfies E[s^2] = sigma^2, while the
version dividing by n has expectation ((n-1)/n) * sigma^2 and is biased low.

PROOF. Write the deviation about the sample mean as the deviation about mu
minus the error in the mean:  X_i - Xbar = (X_i - mu) - (Xbar - mu).
Squaring and summing over i, the cross term collapses because
sum_i (X_i - mu) = n (Xbar - mu):
    sum_i (X_i - Xbar)^2 = sum_i (X_i - mu)^2 - n (Xbar - mu)^2.
Take expectations. The first term is n * sigma^2 because each summand has
expectation sigma^2. The second is n * Var(Xbar) = n * sigma^2/n = sigma^2.
So the expectation is n*sigma^2 - sigma^2 = (n-1)*sigma^2.  []

The n-1 is not a fudge. The deviations are taken about Xbar, which was itself
fitted to the same data and sits closer to the sample than mu does, so the raw
sum of squares is systematically too small by exactly one variance.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "sessions.csv"
URL = "https://<hub>/math-for-ml-course/datasets/sessions.csv"
DATA = LOCAL if LOCAL.exists() else URL
SEED = 20260822
# Or read it straight off the published site:
# DATA = "https://<hub>/math-for-ml-course/datasets/sessions.csv"


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


TRUE_LAMBDA = 7.4          # stated in datasets/generate_nimbus.py
TRUE_VARIANCE = TRUE_LAMBDA  # Poisson: variance equals the mean


def sum_of_squared_deviations(x: np.ndarray) -> float:
    return float(((x - x.mean()) ** 2).sum())


def section_bessel_correction() -> None:
    session_seconds = pd.read_csv(DATA)["session_seconds"].to_numpy(dtype=float)
    # We resample from this column, so the column IS the population here.
    sigma2 = float(session_seconds.var(ddof=0))
    sigma = float(np.sqrt(sigma2))
    print(f"the column: {session_seconds.size:,} session lengths in seconds")
    print(f"  this column's own variance, ddof=0                    {sigma2:.6f}   <- the estimand below")
    print(f"  this column's own variance, ddof=1                    {session_seconds.var(ddof=1):.6f}")
    print("  Because we resample rows from the column, the theorem is about that")
    print("  number. At 20,000 rows ddof barely changes it, which is why the")
    print("  correction looks like pedantry until the sample is small.\n")

    rng = np.random.default_rng(SEED)
    print(f"{'n':>5}  {'E[ddof=0]':>12}  {'E[ddof=1]':>12}  {'predicted (n-1)/n * s^2':>24}  {'bias of ddof=0':>16}")
    for n in (3, 5, 10, 30, 100):
        trials = 200_000
        draws = rng.choice(session_seconds, size=(trials, n), replace=True)
        ss = ((draws - draws.mean(axis=1, keepdims=True)) ** 2).sum(axis=1)
        biased = (ss / n).mean()
        unbiased = (ss / (n - 1)).mean()
        predicted = (n - 1) / n * sigma2
        print(f"{n:>5}  {biased:>12.5f}  {unbiased:>12.5f}  {predicted:>24.5f}  {biased - sigma2:>16.5f}")

    print(f"\n  the ddof=1 column sits on sigma^2 = {sigma2:.5f} at every n.")
    print(f"  the ddof=0 column sits on the prediction (n-1)/n * {sigma2:.5f} and climbs")
    print("  towards it only as n grows. The bias the theorem predicts is -sigma^2/n,")
    print(f"  which at n = 3 is {-sigma2 / 3:.5f}: a third of the variance goes missing.")
    print("  The simulated column differs from that in the fourth decimal, which is")
    print("  Monte Carlo error in 200,000 trials, not a discrepancy in the theorem.")

    print("\nand the identity the proof turns on, checked on one sample of 12:")
    sample = rng.choice(session_seconds, size=12, replace=True)
    lhs = sum_of_squared_deviations(sample)
    mu_ref = sigma2 * 0.0 + float(session_seconds.mean())
    rhs = float(((sample - mu_ref) ** 2).sum() - sample.size * (sample.mean() - mu_ref) ** 2)
    print(f"  sum (x - xbar)^2                          = {lhs:.10f}")
    print(f"  sum (x - mu)^2  -  n (xbar - mu)^2        = {rhs:.10f}")
    print(f"  difference                                = {abs(lhs - rhs):.2e}")

    print("\none more thing the correction does not buy you:")
    trials, n = 200_000, 8
    draws = rng.choice(session_seconds, size=(trials, n), replace=True)
    s2 = ((draws - draws.mean(axis=1, keepdims=True)) ** 2).sum(axis=1) / (n - 1)
    print(f"  n = {n}:  E[s^2] = {s2.mean():.5f}  against sigma^2 = {sigma2:.5f}   unbiased")
    print(f"           E[s]   = {np.sqrt(s2).mean():.5f}  against sigma   = {sigma:.5f}   BIASED LOW")
    print("  an unbiased estimator of a variance is not an unbiased estimator of a")
    print("  standard deviation, because the square root is a concave function.")


def main() -> None:
    sessions = pd.read_csv(DATA)
    x = sessions["session_seconds"].to_numpy(dtype=float)
    n = x.size

    xbar = mean_from_definition(x)
    med = median_from_definition(x)

    print(f"n = {n:,} sessions\n")
    print("centre")
    print(f"  mean    from definition {xbar:12.4f}   pandas {sessions.session_seconds.mean():12.4f}")
    print(f"  median  from definition {med:12.4f}   pandas {sessions.session_seconds.median():12.4f}")
    print(f"  mode    (rounded to 10ms bins) {float(sessions.session_seconds.round(-1).mode().iloc[0]):.1f}")

    print("\nspread")
    s2 = variance_from_definition(x, ddof=1)
    print(f"  sample variance  (n-1)  {s2:14.4f}   pandas {sessions.session_seconds.var():14.4f}")
    print(f"  population var   (n)    {variance_from_definition(x, ddof=0):14.4f}"
          f"   pandas {sessions.session_seconds.var(ddof=0):14.4f}")
    print(f"  sample sd               {np.sqrt(s2):14.4f}   pandas {sessions.session_seconds.std():14.4f}")
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
    print(f"  dropping the top 1.5% (the bot sessions): n = {clean.size:,}")
    print(f"    mean   {mean_from_definition(clean):10.4f}  was {xbar:10.4f}"
          f"   moved {abs(mean_from_definition(clean) - xbar):9.4f} s")
    print(f"    median {median_from_definition(clean):10.4f}  was {med:10.4f}"
          f"   moved {abs(median_from_definition(clean) - med):9.4f} s")
    print("  the mean answers to every value, so it followed the tail out; the median answers to rank")


    print("\n" + "=" * 72)
    print("BESSEL'S CORRECTION, AND WHY THE SAMPLE VARIANCE DIVIDES BY N-1")
    print("=" * 72 + "\n")
    section_bessel_correction()


if __name__ == "__main__":
    main()
