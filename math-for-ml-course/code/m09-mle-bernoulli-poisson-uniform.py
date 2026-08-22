"""Maximum likelihood for three distributions, and the two ways it surprises you.

THE RECIPE. Write the likelihood L(theta) = prod_i f(x_i | theta), take its
logarithm to turn the product into a sum, and maximise. The log is monotone so
it does not move the argmax, and it turns a product that underflows into a sum
that does not.

THEOREM (Bernoulli). For x_1..x_n in {0,1} the MLE of p is the sample
proportion, p_hat = (sum_i x_i)/n.
PROOF. With k = sum_i x_i, L(p) = p^k (1-p)^(n-k), so
    l(p) = k log p + (n-k) log(1-p),
    l'(p) = k/p - (n-k)/(1-p).
Setting l'(p) = 0 gives k(1-p) = (n-k)p, hence k = np and p = k/n. The second
derivative is -k/p^2 - (n-k)/(1-p)^2 < 0 throughout (0,1), so l is strictly
concave and this stationary point is the unique maximum.  []

THEOREM (Poisson). For counts x_1..x_n the MLE of lambda is the sample mean.
PROOF. l(lambda) = -n lambda + (sum_i x_i) log lambda - sum_i log(x_i!). The
last term has no lambda in it, so l'(lambda) = -n + (sum_i x_i)/lambda, which
vanishes at lambda = xbar. l''(lambda) = -(sum_i x_i)/lambda^2 < 0.  []

THEOREM (Uniform on [0, theta]). The MLE is theta_hat = max_i x_i, and there is
no stationary point anywhere.
PROOF. L(theta) = theta^(-n) if theta >= max_i x_i, and 0 otherwise, because
any smaller theta assigns density zero to the largest observation. On the
region where it is positive L is strictly decreasing in theta, so it is
maximised at the smallest admissible value, which is max_i x_i.  []

THEOREM (and that MLE is biased). E[max_i X_i] = n.theta/(n+1).
PROOF. Let M = max_i X_i. For 0 <= t <= theta, P(M <= t) = (t/theta)^n by
independence, so M has density n t^(n-1)/theta^n. Then
    E[M] = int_0^theta t . n t^(n-1)/theta^n dt = (n/theta^n) . theta^(n+1)/(n+1)
         = n.theta/(n+1).
So the bias is -theta/(n+1), always negative: every observation is at most
theta, so their maximum is too. Multiplying by (n+1)/n removes it exactly.  []

Datasets: nimbus-sessions.csv (converted for Bernoulli, page_views for Poisson)
and simulated uniform draws, because no column in the course is uniform.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-sessions.csv"
URL = "https://<hub>/math-for-ml-course/datasets/nimbus-sessions.csv"
DATA = LOCAL if LOCAL.exists() else URL
SEED = 20260822


def bernoulli_loglik(p: float, k: int, n: int) -> float:
    return k * np.log(p) + (n - k) * np.log1p(-p)


def poisson_loglik_core(lam: float, total: int, n: int) -> float:
    """Dropping the constant -sum log(x_i!), which does not depend on lambda."""
    return -n * lam + total * np.log(lam)


def main() -> None:
    df = pd.read_csv(DATA)

    print("1. BERNOULLI on the converted column")
    conv = df["converted"].to_numpy(int)
    k, n = int(conv.sum()), conv.size
    print(f"   k = {k:,} conversions in n = {n:,} sessions")
    print(f"   p_hat = k/n = {k / n:.6f}")
    print(f"   {'candidate p':>14}  {'log-likelihood':>18}")
    for p in (0.030, 0.045, k / n, 0.070, 0.090):
        mark = "   <- the MLE" if abs(p - k / n) < 1e-12 else ""
        print(f"   {p:>14.6f}  {bernoulli_loglik(p, k, n):>18.4f}{mark}")
    print("   The peak is at k/n, and the curve falls away either side of it.")

    print("\n2. POISSON on the page_views column")
    views = df["page_views"].to_numpy(int)
    total, m = int(views.sum()), views.size
    print(f"   sum = {total:,} over n = {m:,} sessions")
    print(f"   lambda_hat = xbar = {total / m:.6f}   (the generator used 7.4)")
    print(f"   {'candidate lambda':>18}  {'log-likelihood (up to a constant)':>36}")
    for lam in (6.8, 7.1, total / m, 7.7, 8.0):
        mark = "   <- the MLE" if abs(lam - total / m) < 1e-12 else ""
        print(f"   {lam:>18.6f}  {poisson_loglik_core(lam, total, m):>36.4f}{mark}")

    print("\n3. UNIFORM on [0, theta], where the derivative method has nothing to do")
    rng = np.random.default_rng(SEED)
    theta = 10.0
    for n_draw in (6, 50, 500):
        sample = rng.uniform(0.0, theta, size=n_draw)
        mle = float(sample.max())
        debiased = (n_draw + 1) / n_draw * mle
        print(f"   n = {n_draw:>4}:  max = {mle:.6f}   debiased (n+1)/n * max = {debiased:.6f}"
              f"   true theta = {theta}")

    print("\n   the bias, measured against the theorem")
    print(f"   {'n':>6}  {'E[max]':>12}  {'predicted n.theta/(n+1)':>25}  {'E[debiased]':>13}")
    for n_draw in (2, 6, 20, 100):
        draws = rng.uniform(0.0, theta, size=(200_000, n_draw))
        maxes = draws.max(axis=1)
        predicted = n_draw * theta / (n_draw + 1)
        print(f"   {n_draw:>6}  {maxes.mean():>12.6f}  {predicted:>25.6f}"
              f"  {((n_draw + 1) / n_draw * maxes).mean():>13.6f}")
    print("   The MLE column sits on the prediction and is below 10 at every n.")
    print("   The debiased column sits on 10. A maximum likelihood estimator is")
    print("   consistent, not unbiased, and this is the cleanest case of that.")

    print("\n   why calculus never appeared: the likelihood has a wall, not a peak")
    sample = rng.uniform(0.0, theta, size=8)
    biggest = float(sample.max())
    print(f"   a sample of 8 with max = {biggest:.4f}")
    print(f"   {'theta':>10}  {'L(theta) = theta^-8':>22}")
    for t in (biggest - 0.5, biggest - 0.001, biggest, biggest + 0.001, biggest + 1.0, biggest + 3.0):
        value = t ** -8 if t >= biggest else 0.0
        label = "  <- the MLE" if abs(t - biggest) < 1e-12 else ""
        print(f"   {t:>10.4f}  {value:>22.10e}{label}")
    print("   Zero to the left of the maximum, then a jump, then a strictly")
    print("   decreasing curve. The maximum is at the wall, where the derivative")
    print("   does not exist. 'Set the derivative to zero' is a step in the recipe,")
    print("   not the recipe.")


if __name__ == "__main__":
    main()
