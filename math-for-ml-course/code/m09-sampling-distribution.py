"""A statistic is a random variable, and its distribution is the whole subject.

THEOREM (mean and variance of the sample mean). Let X_1..X_n be independent
draws with mean mu and variance sigma^2, and Xbar = (1/n) sum_i X_i. Then
    E[Xbar] = mu        and        Var(Xbar) = sigma^2 / n.
PROOF. Expectation is linear, so E[Xbar] = (1/n) sum_i E[X_i] = (1/n)(n mu) = mu.
For the variance, scaling pulls out as a square and independence makes the
variances add:
    Var(Xbar) = Var((1/n) sum_i X_i) = (1/n^2) Var(sum_i X_i)
              = (1/n^2) sum_i Var(X_i) = (1/n^2)(n sigma^2) = sigma^2/n.  []
The standard error is the square root of that, sigma/sqrt(n). The square root
is the whole economics of measurement: four times the data buys half the error.

THEOREM (mean and variance of a sample proportion). A proportion is a sample
mean of 0/1 draws, so if each X_i is Bernoulli(p),
    E[p_hat] = p        and        Var(p_hat) = p(1-p)/n.
PROOF. Apply the theorem above with mu = p and sigma^2 = Var(X) = p - p^2,
using E[X^2] = E[X] = p because X only takes the values 0 and 1.  []

THE DISTINCTION THIS PAGE EXISTS FOR. The standard deviation describes the
data. The standard error describes the estimate. They differ by sqrt(n), and
putting the first on an error bar overstates uncertainty by that factor.

Dataset: nimbus-sessions.csv. The column is treated as the population and
resampled, so the estimand is the column's own mean and variance.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-sessions.csv"
URL = "https://<hub>/math-for-ml-course/datasets/nimbus-sessions.csv"
DATA = LOCAL if LOCAL.exists() else URL
SEED = 20260822
TRIALS = 40_000


def main() -> None:
    df = pd.read_csv(DATA)
    x = df["session_minutes"].to_numpy(float)
    mu, sigma = float(x.mean()), float(x.std(ddof=0))
    rng = np.random.default_rng(SEED)

    print(f"the column is the population: N = {x.size:,}")
    print(f"  mu    = {mu:.6f}")
    print(f"  sigma = {sigma:.6f}   <- describes the DATA\n")

    print(f"{'n':>6}  {'E[xbar]':>12}  {'bias':>10}  {'sd of xbar':>12}"
          f"  {'predicted sigma/sqrt(n)':>24}  {'ratio':>7}")
    for n in (5, 25, 100, 400, 1600):
        draws = rng.choice(x, size=(TRIALS, n), replace=True)
        means = draws.mean(axis=1)
        predicted = sigma / np.sqrt(n)
        print(f"{n:>6}  {means.mean():>12.6f}  {means.mean() - mu:>10.6f}"
              f"  {means.std(ddof=1):>12.6f}  {predicted:>24.6f}"
              f"  {means.std(ddof=1) / predicted:>7.4f}")
    print("  The bias column is noise around zero at every n: the sample mean is")
    print("  unbiased and no amount of data is what makes it so. The last column is")
    print("  the measured spread over the predicted one, and it sits on 1.")

    print("\nthe square root, stated as the thing you have to buy")
    base = sigma / np.sqrt(100)
    for factor in (1, 4, 16, 100):
        n = 100 * factor
        print(f"  n = {n:>6,}  ({factor:>3}x the data)   standard error {sigma / np.sqrt(n):.6f}"
              f"   = {base / (sigma / np.sqrt(n)):.1f}x better")
    print("  A hundred times the data for a tenfold improvement. This is why an")
    print("  experiment that needs to detect a small effect needs a very large n,")
    print("  and why that is a budget question before it is a statistics question.")

    print("\nstandard deviation against standard error, on one sample")
    sample = rng.choice(x, size=400, replace=False)
    print(f"  a sample of {sample.size}: mean {sample.mean():.4f}")
    print(f"    sample sd  {sample.std(ddof=1):.6f}   'sessions vary by about this much'")
    print(f"    standard error {sample.std(ddof=1) / np.sqrt(sample.size):.6f}"
          f"   'this estimate would move by about this much'")
    print(f"    the two differ by sqrt(n) = {np.sqrt(sample.size):.1f}")

    print("\nthe same theorem for a proportion, on the converted column")
    conv = df["converted"].to_numpy(float)
    p = float(conv.mean())
    print(f"  population rate p = {p:.6f},  so p(1-p) = {p * (1 - p):.6f}")
    print(f"  {'n':>6}  {'E[p_hat]':>12}  {'sd of p_hat':>13}  {'predicted':>12}")
    for n in (100, 1000, 12000):
        draws = rng.choice(conv, size=(TRIALS, n), replace=True)
        phats = draws.mean(axis=1)
        print(f"  {n:>6}  {phats.mean():>12.6f}  {phats.std(ddof=1):>13.6f}"
              f"  {np.sqrt(p * (1 - p) / n):>12.6f}")
    print("  This is the line every accuracy number and every conversion rate in the")
    print("  rest of the module is built on.")


if __name__ == "__main__":
    main()
