"""Bessel's correction: why the sample variance divides by n-1.

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

Dataset: nimbus-sessions.csv, column page_views, generated as
Poisson(lambda = 7.4). For a Poisson the variance equals the mean.

One subtlety worth stating, because getting it wrong is the commonest error in
a bootstrap demonstration. Below we resample rows FROM THE COLUMN. That makes
the column itself the population, so the quantity the estimators are aiming at
is the column's own variance with ddof=0, not the generator's 7.4. The column
is a 25,000-row sample from Poisson(7.4) and its variance is one draw near but
not equal to 7.4. The theorem is about the population you are drawing from, so
that is the number the table must be read against.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

DATA = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-sessions.csv"
TRUE_LAMBDA = 7.4          # stated in datasets/generate_nimbus.py
TRUE_VARIANCE = TRUE_LAMBDA  # Poisson: variance equals the mean
SEED = 20260822


def sum_of_squared_deviations(x: np.ndarray) -> float:
    return float(((x - x.mean()) ** 2).sum())


def main() -> None:
    page_views = pd.read_csv(DATA)["page_views"].to_numpy(dtype=float)
    # We resample from this column, so the column IS the population here.
    sigma2 = float(page_views.var(ddof=0))
    sigma = float(np.sqrt(sigma2))
    print(f"the column: {page_views.size:,} sessions drawn from Poisson(lambda = {TRUE_LAMBDA})")
    print(f"  generator parameter, so the distribution's variance   {TRUE_VARIANCE:.6f}")
    print(f"  this column's own variance, ddof=0                    {sigma2:.6f}   <- the estimand below")
    print(f"  this column's own variance, ddof=1                    {page_views.var(ddof=1):.6f}")
    print("  the column's variance is a draw near 7.4, not 7.4 itself. Because we")
    print("  resample rows from the column, the theorem is about the first number")
    print("  above it, not about 7.4. At 25,000 rows ddof barely matters, which is")
    print("  why the correction looks like pedantry until the sample is small.\n")

    rng = np.random.default_rng(SEED)
    print(f"{'n':>5}  {'E[ddof=0]':>12}  {'E[ddof=1]':>12}  {'predicted (n-1)/n * s^2':>24}  {'bias of ddof=0':>16}")
    for n in (3, 5, 10, 30, 100):
        trials = 200_000
        draws = rng.choice(page_views, size=(trials, n), replace=True)
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
    sample = rng.choice(page_views, size=12, replace=True)
    lhs = sum_of_squared_deviations(sample)
    rhs = float(((sample - TRUE_LAMBDA) ** 2).sum() - sample.size * (sample.mean() - TRUE_LAMBDA) ** 2)
    print(f"  sum (x - xbar)^2                          = {lhs:.10f}")
    print(f"  sum (x - mu)^2  -  n (xbar - mu)^2        = {rhs:.10f}")
    print(f"  difference                                = {abs(lhs - rhs):.2e}")

    print("\none more thing the correction does not buy you:")
    trials, n = 200_000, 8
    draws = rng.choice(page_views, size=(trials, n), replace=True)
    s2 = ((draws - draws.mean(axis=1, keepdims=True)) ** 2).sum(axis=1) / (n - 1)
    print(f"  n = {n}:  E[s^2] = {s2.mean():.5f}  against sigma^2 = {sigma2:.5f}   unbiased")
    print(f"           E[s]   = {np.sqrt(s2).mean():.5f}  against sigma   = {sigma:.5f}   BIASED LOW")
    print("  an unbiased estimator of a variance is not an unbiased estimator of a")
    print("  standard deviation, because the square root is a concave function.")


if __name__ == "__main__":
    main()
