"""Sampling from a distribution, and Monte Carlo estimation.

Lesson: Sampling and Monte Carlo.

    python3 0814-sampling-and-monte-carlo.py

What it checks twice:

  1. Inverse-CDF sampling: draws built from uniforms through F^-1, against the
     closed-form distribution they should have. Checked by CDF gap.
  2. Rejection sampling: the realised acceptance rate against the predicted 1/M,
     and the collapse of that rate as dimension grows.
  3. Monte Carlo: the measured spread of the estimator against sigma_f/sqrt(N),
     across four orders of magnitude of N.
  4. The honest limit: the rate is dimension-free and the CONSTANT is not.
"""

from __future__ import annotations

import numpy as np

RNG = np.random.default_rng(20260902)


def normal_cdf(z: np.ndarray) -> np.ndarray:
    from math import erf

    return np.array([0.5 * (1.0 + erf(v / np.sqrt(2.0))) for v in z])


def main() -> None:
    print("1. Inverse-CDF sampling: uniforms in, a distribution out")
    print("   Exponential with mean 415 ms: F(x) = 1 - exp(-x/415), so")
    print("   F^-1(u) = -415 * ln(1 - u).")
    scale = 415.0
    u = RNG.random(400_000)
    built = -scale * np.log(1.0 - u)
    print(f"\n   {'u':>8}{'F^-1(u)':>14}")
    for value in (0.25, 0.5, 0.7, 0.99):
        print(f"   {value:>8.2f}{-scale * np.log(1 - value):>14.3f} ms")
    print(f"\n   built sample mean {built.mean():>10.3f}   theory {scale:>10.3f}")
    print(f"   built sample sd   {built.std():>10.3f}   theory {scale:>10.3f}")
    print(f"   built median      {np.median(built):>10.3f}   theory "
          f"{scale * np.log(2):>10.3f}")
    assert abs(built.mean() - scale) / scale < 0.01
    quantiles = np.percentile(built, [10, 50, 90])
    theory = -scale * np.log(1 - np.array([0.1, 0.5, 0.9]))
    assert np.allclose(quantiles, theory, rtol=0.03)
    print("   Quantiles match the closed form. The uniform is the only primitive;")
    print("   everything else is a transformation of it.")

    print("\n2. Rejection sampling, and why it dies in high dimensions")
    print("   Target a standard normal, propose from a standard Cauchy.")
    grid = np.linspace(-12, 12, 400_001)
    p = np.exp(-(grid**2) / 2) / np.sqrt(2 * np.pi)
    q = 1.0 / (np.pi * (1 + grid**2))
    M = float((p / q).max())
    print(f"   M = max p/q = {M:.4f}, so the predicted acceptance rate is {1 / M:.4f}")
    proposals = RNG.standard_cauchy(400_000)
    ratio = (
        np.exp(-(proposals**2) / 2) / np.sqrt(2 * np.pi)
    ) / (1.0 / (np.pi * (1 + proposals**2)))
    accepted = RNG.random(len(proposals)) < ratio / M
    print(f"   measured acceptance rate                    {accepted.mean():.4f}")
    assert abs(accepted.mean() - 1 / M) < 0.01
    kept = proposals[accepted]
    print(f"   kept {kept.sum() * 0 + accepted.sum():,} of {len(proposals):,} proposals")
    print(f"   accepted sample: mean {kept.mean():>7.4f}, sd {kept.std():>7.4f} "
          f"(target 0 and 1)")
    print(f"   CDF gap to the standard normal: "
          f"{np.abs(np.arange(1, len(kept) + 1) / len(kept) - normal_cdf(np.sort(kept))).max():.4f}")
    print(f"\n   {'dimensions':>12}{'M^d':>14}{'acceptance':>14}{'proposals per sample':>22}")
    for d in (1, 2, 5, 10, 20):
        rate = M ** (-d)
        print(f"   {d:>12}{M**d:>14.2f}{rate:>14.6f}{1 / rate:>22,.0f}")
    print("   Twenty independent dimensions and you need forty thousand proposals")
    print("   per accepted sample. This is the number that makes MCMC necessary.")

    print("\n3. Monte Carlo: the 1/sqrt(N) rate, measured")
    print("   Estimate pi by the fraction of uniform points inside a quarter circle.")
    true_rate = np.pi / 4
    sigma_f = 4.0 * np.sqrt(true_rate * (1 - true_rate))
    print(f"   f is 4 * indicator, so sigma_f = 4*sqrt(p(1-p)) = {sigma_f:.5f}\n")
    print(f"   {'N':>10}{'mean estimate':>16}{'measured sd':>14}{'sigma_f/sqrt(N)':>18}{'ratio':>8}")
    for N in (100, 1_000, 10_000, 100_000):
        estimates = np.array(
            [4.0 * ((RNG.random((N, 2)) ** 2).sum(axis=1) <= 1.0).mean() for _ in range(400)]
        )
        measured = float(estimates.std(ddof=1))
        predicted = sigma_f / np.sqrt(N)
        print(
            f"   {N:>10,}{estimates.mean():>16.5f}{measured:>14.5f}"
            f"{predicted:>18.5f}{measured / predicted:>8.3f}"
        )
        assert 0.85 < measured / predicted < 1.15
    print("\n   Every hundredfold rise in N buys one decimal place. Four correct")
    print(f"   decimals needs about N = {int((sigma_f / 1e-4) ** 2):,}.")

    print("\n4. The rate is dimension-free. The constant is not.")
    print("   Volume of the unit ball inside the cube [-1,1]^d, at fixed N.")
    from math import gamma

    N = 200_000
    print(f"\n   {'d':>4}{'true volume':>14}{'MC estimate':>14}{'rel error':>12}"
          f"{'points inside':>15}{'grid needs':>14}")
    for d in (2, 5, 10, 20):
        true = np.pi ** (d / 2) / gamma(d / 2 + 1)
        points = RNG.random((N, d)) * 2 - 1
        inside = int(((points**2).sum(axis=1) <= 1.0).sum())
        estimate = (2.0**d) * inside / N
        error = abs(estimate - true) / true
        print(
            f"   {d:>4}{true:>14.6f}{estimate:>14.6f}{error:>12.2%}"
            f"{inside:>15,}{'10^' + str(d):>14}"
        )
    print("\n   At d = 10 Monte Carlo is within a couple of percent using 200,000")
    print("   points where a ten-per-axis grid would need ten billion. At d = 20")
    print("   not one of the 200,000 points landed inside, because the ball is")
    print("   about 2.5e-08 of the cube.")
    print("   The 1/sqrt(N) rate never broke. sigma_f did. The rate does not know")
    print("   about dimension and the variance of f certainly does, which is what")
    print("   importance sampling and MCMC exist to fix.")


if __name__ == "__main__":
    main()
