"""MLE for the Gaussian, and why squared error was a likelihood all along.

THEOREM (Gaussian MLE). For x_1..x_n drawn from Normal(mu, sigma^2), the
maximum likelihood estimates are
    mu_hat = xbar        and        sigma_hat^2 = (1/n) sum_i (x_i - xbar)^2.
Note the denominator: n, not n-1.
PROOF. The log-likelihood is
    l(mu, sigma^2) = -(n/2) log(2 pi sigma^2) - (1/(2 sigma^2)) sum_i (x_i - mu)^2.
Only the final term contains mu, and it enters with a minus sign, so maximising
over mu is minimising sum_i (x_i - mu)^2, which the least-squares argument puts
at mu = xbar. Substituting that and differentiating in sigma^2,
    dl/d(sigma^2) = -n/(2 sigma^2) + (1/(2 sigma^4)) sum_i (x_i - xbar)^2,
and setting it to zero gives sigma^2 = (1/n) sum_i (x_i - xbar)^2.  []

COROLLARY (the Gaussian variance MLE is biased). By Bessel's theorem the
numerator has expectation (n-1) sigma^2, so E[sigma_hat^2] = ((n-1)/n) sigma^2,
which is below sigma^2 for every finite n and converges to it. Maximum
likelihood is consistent, not unbiased.

THEOREM (Gaussian noise implies least squares). If y_i = a + b x_i + e_i with
e_i independent Normal(0, sigma^2), then the (a, b) maximising the likelihood
are exactly the (a, b) minimising sum_i (y_i - a - b x_i)^2.
PROOF. The log-likelihood is
    -(n/2) log(2 pi sigma^2) - (1/(2 sigma^2)) sum_i (y_i - a - b x_i)^2,
and a and b appear only in the final sum, preceded by a negative constant.
Maximising in (a, b) is therefore minimising that sum.  []

WHAT THIS BUYS. Squared error is not a convention someone chose. It is what a
Gaussian noise assumption implies. Change the assumption and the loss changes
with it: the same argument on a Bernoulli likelihood gives log loss, which the
program also shows. That is why a heavy-tailed target gets a different loss:
the Gaussian assumption was doing work that the data does not support.

Datasets: nimbus-adspend.csv (a known line and known noise) and
nimbus-sessions.csv (the converted column, for the Bernoulli half).

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent.parent / "datasets"
ADSPEND = HERE / "nimbus-adspend.csv"
SESSIONS = HERE / "nimbus-sessions.csv"
TRUE_INTERCEPT, TRUE_SLOPE, TRUE_SIGMA = 12.5, 3.20, 8.0
SEED = 20260822


def gaussian_loglik(residuals: np.ndarray, sigma2: float) -> float:
    n = residuals.size
    return float(-0.5 * n * np.log(2 * np.pi * sigma2) - (residuals ** 2).sum() / (2 * sigma2))


def main() -> None:
    ads = pd.read_csv(ADSPEND)
    x = ads["ad_spend_k"].to_numpy(float)
    y = ads["revenue_k"].to_numpy(float)
    n = x.size

    print("1. THE GAUSSIAN MLE FOR A MEAN, on the residuals of a known model")
    truth = TRUE_INTERCEPT + TRUE_SLOPE * x
    noise = y - truth
    print(f"   the true noise column, n = {n:,}, generated Normal(0, {TRUE_SIGMA}^2)")
    print(f"   mu_hat = mean            {noise.mean():>12.6f}   true mu    = 0")
    print(f"   sigma_hat^2 (divide n)   {float((noise ** 2).mean()):>12.6f}   true sigma^2 = {TRUE_SIGMA ** 2}")
    print(f"   s^2         (divide n-1) {float(noise.var(ddof=1)):>12.6f}")

    print("\n   the bias of the variance MLE, measured")
    rng = np.random.default_rng(SEED)
    print(f"   {'n':>5}  {'E[sigma_hat^2]':>16}  {'predicted (n-1)/n * sigma^2':>29}  {'E[s^2]':>12}")
    for m in (3, 5, 20, 100):
        draws = rng.normal(0.0, TRUE_SIGMA, size=(200_000, m))
        ss = ((draws - draws.mean(axis=1, keepdims=True)) ** 2).sum(axis=1)
        print(f"   {m:>5}  {float((ss / m).mean()):>16.5f}"
              f"  {(m - 1) / m * TRUE_SIGMA ** 2:>29.5f}  {float((ss / (m - 1)).mean()):>12.5f}")

    print("\n2. MAXIMISING THE LIKELIHOOD IS MINIMISING SQUARED ERROR")
    sxx = float(((x - x.mean()) ** 2).sum())
    sxy = float(((x - x.mean()) * (y - y.mean())).sum())
    b_ls = sxy / sxx
    a_ls = float(y.mean() - b_ls * x.mean())
    print(f"   least squares    a = {a_ls:.6f}   b = {b_ls:.6f}")
    print(f"   the truth        a = {TRUE_INTERCEPT}         b = {TRUE_SLOPE}")
    print(f"\n   {'candidate b':>14}  {'sum of squared errors':>23}  {'log-likelihood':>18}")
    sigma2 = float(((y - a_ls - b_ls * x) ** 2).mean())
    for b in (b_ls - 0.05, b_ls - 0.01, b_ls, b_ls + 0.01, b_ls + 0.05):
        a = float(y.mean() - b * x.mean())
        res = y - a - b * x
        mark = "  <- both extremes here" if abs(b - b_ls) < 1e-12 else ""
        print(f"   {b:>14.6f}  {float((res ** 2).sum()):>23.4f}"
              f"  {gaussian_loglik(res, sigma2):>18.4f}{mark}")
    print("   The squared-error column is smallest and the log-likelihood column is")
    print("   largest at the same b, and they are the same computation with a sign.")

    print("\n3. THE SAME MOVE ON A BERNOULLI LIKELIHOOD GIVES LOG LOSS")
    conv = pd.read_csv(SESSIONS)["converted"].to_numpy(float)
    k, m = float(conv.sum()), conv.size
    print(f"   {'candidate p':>14}  {'mean negative log-likelihood':>30}  {'sklearn-style log loss':>24}")
    for p in (0.030, 0.050, k / m, 0.070):
        nll = -float(np.mean(conv * np.log(p) + (1 - conv) * np.log1p(-p)))
        # The same number, written the way a training loop writes it.
        logloss = -float(np.mean(conv * np.log(p) + (1 - conv) * np.log(1 - p)))
        mark = "  <- the MLE" if abs(p - k / m) < 1e-12 else ""
        print(f"   {p:>14.6f}  {nll:>30.8f}  {logloss:>24.8f}{mark}")
    print("   Two names, one quantity. Binary cross-entropy IS the Bernoulli")
    print("   negative log-likelihood, and minimising it is maximum likelihood.")
    print("   (Cross-entropy as an information quantity belongs to the information")
    print("   module; the equivalence is derived here, once.)")


if __name__ == "__main__":
    main()
