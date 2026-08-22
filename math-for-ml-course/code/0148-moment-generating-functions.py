"""Moment generating functions: turning sums into products, and tails into bounds.

Lesson: Moment generating functions.

    python3 0809-moment-generating-functions.py

The MGF earns its place here as the rung of the tail-bound ladder that makes
Chernoff possible. Everything below is pointed at that.

What it checks twice:

  1. M(t) = E[e^tX] estimated from data, against the closed form for a
     distribution whose MGF is known. Two routes, one curve.
  2. The "moment generating" claim: the k-th derivative of M at t = 0 is E[X^k].
     Checked by numerical differentiation against the sample moments.
  3. The property the ladder needs: for INDEPENDENT variables the MGF of a sum
     is the PRODUCT of the MGFs. Checked against a direct estimate from the sum,
     and shown to FAIL on a dependent pair.
  4. The Chernoff bound built from it, against Markov and Chebyshev on the same
     tail, so the reader sees what the extra assumption bought.
"""

from __future__ import annotations

import numpy as np

RNG = np.random.default_rng(20260828)


def empirical_mgf(sample: np.ndarray, t: np.ndarray) -> np.ndarray:
    """E[e^tX] estimated by averaging, in a way that does not overflow.

    Averaging exp(t*x) directly overflows for even moderate t on a heavy tail, so
    this works in logs and exponentiates once at the end.
    """
    scaled = np.outer(t, sample)
    peak = scaled.max(axis=1, keepdims=True)
    return np.exp(peak.ravel() + np.log(np.exp(scaled - peak).mean(axis=1)))


def main() -> None:
    size = 400_000

    print("1. The MGF from data against its closed form")
    print("   Exponential(rate=2) has M(t) = rate / (rate - t) for t < rate.")
    rate = 2.0
    sample = RNG.exponential(1.0 / rate, size)
    grid = np.array([-1.0, -0.5, 0.0, 0.5, 1.0, 1.5])
    measured = empirical_mgf(sample, grid)
    closed = rate / (rate - grid)
    print(f"   {'t':>7}{'measured':>14}{'closed form':>14}{'rel gap':>10}")
    for t, m, c in zip(grid, measured, closed):
        print(f"   {t:>7.2f}{m:>14.6f}{c:>14.6f}{abs(m - c) / c:>10.5f}")
    assert np.allclose(measured, closed, rtol=0.02)
    print("   Agrees across the range. Note M(0) = 1 always, for every")
    print("   distribution: it is the integral of the density.")
    print("   Note also that the closed form blows up as t approaches the rate.")
    print("   An MGF need not exist for every t, and for a lognormal it exists")
    print("   for no positive t at all, which is a real limitation of this tool.")

    print("\n2. Why it is called MOMENT generating")
    print("   The k-th derivative of M at t = 0 is E[X^k].")
    h = 1e-4
    around = empirical_mgf(sample, np.array([-2 * h, -h, 0.0, h, 2 * h]))
    first = (around[3] - around[1]) / (2 * h)
    second = (around[3] - 2 * around[2] + around[1]) / h**2
    print(f"   M'(0)  numerically {first:>10.6f}   sample E[X]    {sample.mean():>10.6f}")
    print(f"   M''(0) numerically {second:>10.6f}   sample E[X^2]  {(sample**2).mean():>10.6f}")
    assert np.isclose(first, sample.mean(), rtol=0.01)
    assert np.isclose(second, (sample**2).mean(), rtol=0.02)
    print("   Differentiating the MGF reads moments off one at a time.")

    print("\n3. The property the ladder needs: sums become products")
    a = RNG.exponential(0.5, size)
    b = RNG.exponential(0.8, size)
    t_grid = np.array([0.1, 0.3, 0.5])
    print("   INDEPENDENT parts")
    print(f"   {'t':>7}{'M_sum(t)':>14}{'M_a(t)*M_b(t)':>16}{'rel gap':>10}")
    for t in t_grid:
        joint = empirical_mgf(a + b, np.array([t]))[0]
        product = empirical_mgf(a, np.array([t]))[0] * empirical_mgf(b, np.array([t]))[0]
        print(f"   {t:>7.2f}{joint:>14.6f}{product:>16.6f}{abs(joint - product) / product:>10.5f}")
        assert np.isclose(joint, product, rtol=0.02)
    dependent = a * 1.0
    print("\n   DEPENDENT parts (a with itself)")
    for t in t_grid:
        joint = empirical_mgf(a + dependent, np.array([t]))[0]
        product = empirical_mgf(a, np.array([t]))[0] * empirical_mgf(dependent, np.array([t]))[0]
        print(f"   {t:>7.2f}{joint:>14.6f}{product:>16.6f}{abs(joint - product) / product:>10.5f}")
    print("   The factorisation is an independence property, not an algebra one.")

    print("\n4. What that buys: three bounds on the same tail")
    print("   X is the mean of 1,000 independent Bernoulli(0.3) draws.")
    print("   Bound P(X >= 0.35), so a deviation of 0.05 above the mean.")
    n, p, threshold = 1_000, 0.3, 0.35
    trials = RNG.binomial(n, p, 200_000) / n
    truth = float((trials >= threshold).mean())

    markov = p / threshold
    variance = p * (1 - p) / n
    k = (threshold - p) / np.sqrt(variance)
    chebyshev = 1.0 / k**2
    # Chernoff for a mean of bounded variables (Hoeffding's form): the MGF of a
    # variable in [0,1] is bounded, and optimising t over that bound gives this.
    hoeffding = float(np.exp(-2 * n * (threshold - p) ** 2))

    print(f"\n   {'bound':<34}{'value':>12}{'times the truth':>18}")
    for name, value in (
        ("Markov, from the mean alone", markov),
        ("Chebyshev, adding the variance", chebyshev),
        ("Chernoff/Hoeffding, adding the MGF", hoeffding),
        ("the truth, measured", truth),
    ):
        ratio = value / truth if truth > 0 else float("inf")
        tail = f"{ratio:>18,.1f}" if name != "the truth, measured" else f"{'':>18}"
        print(f"   {name:<34}{value:>12.6f}{tail}")
    assert markov > chebyshev > hoeffding >= truth * 0.5
    print(
        "\n   Each rung costs one more assumption and buys an order of magnitude.\n"
        "   Markov knows only the mean, Chebyshev adds the variance, and Chernoff\n"
        "   adds independence and a bounded MGF. That last assumption is what turns\n"
        "   a bound that decays like 1/k^2 into one that decays exponentially in n,\n"
        "   and it is why every generalisation bound in learning theory is built on\n"
        "   this rung rather than the one below it."
    )


if __name__ == "__main__":
    main()
