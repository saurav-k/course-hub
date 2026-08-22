"""0009 - Sequences, limits, and how to read a Big-O claim.

Three checks, all of them things the page claims and none of them asserted
without evidence:

  * the p-series test decides which learning-rate schedules can converge, and
    the answer is a range of p rather than "smaller is safer";
  * (1 - 1/n)^n tends to 1/e, which is the bootstrap's out-of-bag fraction,
    checked by resampling the real 9,000 tickets;
  * an asymptotic bound does not settle a race: self-attention and a recurrent
    layer cross at exactly n = d.

Needs only numpy and pandas.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "tickets.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/tickets.csv"
TERMS = 2_000_000


def load() -> pd.DataFrame:
    """Relative to this file so the repository works offline, URL so Colab works."""
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def partial_sum(power: float, terms: int) -> float:
    k = np.arange(1, terms + 1, dtype=float)
    return float(np.sum(k ** (-power)))


def main() -> None:
    # ---- the p-series test, and the two SGD conditions --------------------
    print("Deep Learning Book equations 8.12 and 8.13, for eps_k = 1/k^p")
    print("  8.12 wants sum eps_k to DIVERGE   - the steps must still reach anywhere")
    print("  8.13 wants sum eps_k^2 to CONVERGE - the sampling noise must die\n")
    print(f"  {'p':>6}  {'sum 1/k^p':>14}  {'sum 1/k^2p':>14}  verdict")
    for power in (0.0, 0.5, 0.75, 1.0, 2.0):
        first = partial_sum(power, TERMS)
        second = partial_sum(2 * power, TERMS)
        diverges = power <= 1.0            # the theorem
        converges = 2 * power > 1.0        # the theorem, applied to the squares
        verdict = "BOTH HOLD" if (diverges and converges) else (
            "fails 8.13, noise never dies" if diverges else "fails 8.12, steps run out"
        )
        print(f"  {power:>6}  {first:>14,.2f}  {second:>14,.4f}  {verdict}")
        # A divergent partial sum must still be growing at the end.
        if diverges:
            assert partial_sum(power, TERMS) > partial_sum(power, TERMS // 2), (
                f"p = {power} should still be growing"
            )
    print("\n  both conditions hold exactly when 0.5 < p <= 1")
    print("  so a constant rate fails, and decaying too hard fails as well:")
    print("  'smaller is safer' is wrong in both directions at once")

    # The convergent one really does approach pi^2/6.
    tail = partial_sum(2.0, TERMS)
    print(f"\n  sum 1/k^2 to {TERMS:,} terms = {tail:.8f}, and pi^2/6 = {np.pi ** 2 / 6:.8f}")
    assert abs(tail - np.pi ** 2 / 6) < 1e-5, "the p = 2 series should be near pi^2/6"

    # And the divergent one grows like ln n, which is why it is slow to notice.
    for terms in (10 ** 3, 10 ** 4, 10 ** 5, 10 ** 6):
        harmonic = partial_sum(1.0, terms)
        print(f"    sum 1/k to {terms:>9,} = {harmonic:>7.4f}   ln n + gamma = {np.log(terms) + 0.5772157:.4f}")

    # ---- (1 - 1/n)^n -> 1/e, checked by resampling real data -------------
    print("\nthe bootstrap's out-of-bag fraction")
    print(f"  {'n':>8}  {'(1 - 1/n)^n':>12}")
    for n in (10, 100, 1_000, 10_000, 100_000):
        print(f"  {n:>8,}  {(1 - 1 / n) ** n:>12.5f}")
    print(f"  {'limit':>8}  {1 / np.e:>12.5f}   = 1/e")
    assert abs((1 - 1 / 100_000) ** 100_000 - 1 / np.e) < 1e-4

    frame = load()
    rng = np.random.default_rng(2026)
    n = len(frame)
    left_out = [1 - len(set(rng.integers(0, n, n).tolist())) / n for _ in range(200)]
    mean_left_out = float(np.mean(left_out))
    print(f"\n  200 bootstrap resamples of the real {n:,} tickets")
    print(f"    mean fraction left out = {mean_left_out:.5f}")
    print(f"    1/e                    = {1 / np.e:.5f}")
    print(f"    Breiman states 'about 37%'; the 0.3679 is this course's own derivation")
    assert abs(mean_left_out - 1 / np.e) < 0.01, "resampling should land on 1/e"

    # ---- an asymptotic bound does not settle a race ----------------------
    print("\nself-attention O(n^2 d) against a recurrent layer O(n d^2), d = 512")
    d = 512
    print(f"  {'n':>6}  {'n^2 d':>18}  {'n d^2':>18}  cheaper")
    for length in (128, 256, 512, 1024, 2048):
        attention = length ** 2 * d
        recurrent = length * d ** 2
        cheaper = "attention" if attention < recurrent else ("equal" if attention == recurrent else "recurrent")
        print(f"  {length:>6}  {attention:>18,}  {recurrent:>18,}  {cheaper}")
    assert 512 ** 2 * d == 512 * d ** 2, "the crossover should be exactly at n = d"
    ratio = (2048 ** 2 * d) / (2048 * d ** 2)
    print(f"\n  at n = 2048 the ratio is exactly {ratio:.0f}, which is n/d")
    assert ratio == 2048 / d

    # The base of a logarithm is a constant factor, which is what O discards.
    big_n = 1_000_000
    print(f"\n  N/log N at N = {big_n:,}: natural {big_n / np.log(big_n):,.0f}, "
          f"base 2 {big_n / np.log2(big_n):,.0f}")
    print(f"  different numbers, same complexity class, because log_b N = ln N / ln b")
    assert np.isclose(np.log2(big_n), np.log(big_n) / np.log(2))

    print("\nall assertions passed")


if __name__ == "__main__":
    main()
