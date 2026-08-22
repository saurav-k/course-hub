"""Skewness and kurtosis: which tail is longer, and how far it reaches.

DEFINITIONS. With mu the mean and sigma the standard deviation, the population
skewness and kurtosis are the third and fourth standardised moments:
    skew = E[ ((X - mu)/sigma)^3 ]
    kurt = E[ ((X - mu)/sigma)^4 ]
Excess kurtosis is kurt - 3, so that a normal distribution scores 0.

RESULT (what kurtosis is a statement about). Kurtosis is driven almost entirely
by the tails, and says essentially nothing about the shape of the peak.
WHY. The summand ((x - mu)/sigma)^4 is below 1 for every observation inside one
standard deviation and grows as the fourth power outside it. A point at 1 sd
contributes 1; a point at 5 sd contributes 625. The centre cannot compete: the
share of the total contributed by everything within 1 sd of the mean is tiny,
and the program prints that share so it can be read rather than believed.
Distributions with identical kurtosis can have sharp, flat or bimodal peaks,
so "peakedness" is not a reading the number supports.

RESULT (skewness and the mean-median gap). For a right-skewed column the long
tail pulls the mean above the median. The sign of the skewness and the sign of
(mean - median) agree for the columns here, which is the usable everyday form
of the statistic. The agreement is a strong regularity, not a theorem: it can
be broken by constructed multimodal counterexamples.

Dataset: sessions.csv. latency_ms is right-skewed and heavy-tailed by
construction, temp_c is normal, and satisfaction is left-skewed.

Needs numpy and pandas only.

----------------------------------------------------------------------
ALSO ON THIS PAGE: Chebyshev's inequality, a spread bound that assumes no shape
----------------------------------------------------------------------

Chebyshev's inequality: a spread bound that assumes nothing about shape.

THEOREM (Markov). If Y >= 0 and E[Y] exists, then for any a > 0,
    P(Y >= a) <= E[Y] / a.
PROOF. Split the expectation at a. Since Y >= 0,
    E[Y] = E[Y . 1{Y >= a}] + E[Y . 1{Y < a}] >= E[Y . 1{Y >= a}] >= a . P(Y >= a),
where the last step replaces Y by the smaller value a on the event Y >= a.
Divide by a.  []

THEOREM (Chebyshev). If X has mean mu and finite variance sigma^2, then for
any k > 0,
    P(|X - mu| >= k.sigma) <= 1 / k^2,   equivalently   P(|X - mu| < k.sigma) >= 1 - 1/k^2.
PROOF. Apply Markov to Y = (X - mu)^2, which is non-negative, with
a = k^2.sigma^2:
    P((X - mu)^2 >= k^2 sigma^2) <= E[(X - mu)^2] / (k^2 sigma^2) = sigma^2/(k^2 sigma^2) = 1/k^2.
The event (X - mu)^2 >= k^2 sigma^2 is exactly |X - mu| >= k.sigma.  []

The bound holds for every distribution with a finite variance, which is what
makes it useful and also what makes it loose. The empirical rule is tighter and
buys that tightness by assuming normality, which neither column here has.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "sessions.csv"
URL = "https://<hub>/math-for-ml-course/datasets/sessions.csv"
DATA = LOCAL if LOCAL.exists() else URL
def standardised(x: np.ndarray) -> np.ndarray:
    return (x - x.mean()) / x.std(ddof=0)


def skewness(x: np.ndarray) -> float:
    return float((standardised(x) ** 3).mean())


def kurtosis(x: np.ndarray) -> float:
    return float((standardised(x) ** 4).mean())


def tail_share_of_kurtosis(x: np.ndarray, inside: float = 1.0) -> tuple[float, float]:
    """What fraction of the kurtosis sum comes from inside `inside` sd, and what fraction of the rows."""
    z = standardised(x)
    contribution = z ** 4
    core = np.abs(z) < inside
    return float(contribution[core].sum() / contribution.sum()), float(core.mean())


EMPIRICAL_RULE = {1: 0.6827, 2: 0.9545, 3: 0.9973, 4: 0.999937}


def within_k_sd(x: np.ndarray, k: float) -> float:
    mu, sd = x.mean(), x.std(ddof=0)
    return float(np.mean(np.abs(x - mu) < k * sd))


def section_chebyshev() -> None:
    df = pd.read_csv(DATA)
    print(f"n = {len(df):,} sessions\n")
    print(f"{'k':>3}  {'Chebyshev floor':>16}  {'session_seconds':>16}  {'screen_brightness':>18}  {'a normal column':>17}")
    for k in (1, 2, 3, 4):
        floor = 0.0 if k == 1 else 1 - 1 / k ** 2
        print(f"{k:>3}  {floor:>16.4f}  {within_k_sd(df.session_seconds.to_numpy(float), k):>16.4f}"
              f"  {within_k_sd(df.screen_brightness.to_numpy(float), k):>18.4f}  {EMPIRICAL_RULE[k]:>17.4f}")

    print("\nreading the table")
    print("  Every column beats the Chebyshev floor, as it must: the floor is a")
    print("  guarantee, not a prediction. At k = 1 the floor is 0, which is a true")
    print("  statement that tells you nothing, and that is the honest cost of")
    print("  assuming nothing.")
    print("  Neither column is normal, and they miss in opposite directions.")
    print("  session_seconds is heavy-tailed: its standard deviation is inflated by")
    print("  the long tail, so far MORE than 68 per cent of rows sit inside 1 sd, and")
    print("  the mass that does escape goes very much further out.")
    print("  screen_brightness is uniform and has no tail at all, so it fills its")
    print("  range and then stops: past about 1.8 sd there is simply nothing.")
    print("  The counts below are the same fact from the other end.")

    x = df.session_seconds.to_numpy(float)
    mu, sd = x.mean(), x.std(ddof=0)
    for k in (3, 4, 6, 10):
        beyond = int((np.abs(x - mu) >= k * sd).sum())
        print(f"    beyond {k:>2} sd: session_seconds has {beyond:>5} rows"
              f"   Chebyshev allows up to {len(df) / k ** 2:>8.0f}"
              f"   a normal column would give about {len(df) * (1 - EMPIRICAL_RULE.get(k, 1.0)):>6.0f}")

    print("\n  Chebyshev is never violated and is never tight. That is the trade:")
    print("  it is the bound you can use when you do not know the shape.")


def main() -> None:
    df = pd.read_csv(DATA)
    columns = ["session_seconds", "screen_brightness", "spend", "pages_viewed"]

    print(f"n = {len(df):,} sessions\n")
    print(f"{'column':>16}  {'mean':>10}  {'median':>10}  {'mean-median':>12}  {'skew':>8}  {'kurtosis':>10}  {'excess':>9}")
    for name in columns:
        x = df[name].to_numpy(float)
        k = kurtosis(x)
        print(f"{name:>16}  {x.mean():>10.3f}  {np.median(x):>10.3f}  {x.mean() - np.median(x):>12.3f}"
              f"  {skewness(x):>8.3f}  {k:>10.3f}  {k - 3:>9.3f}")

    print("\n  Compare the skew column with the mean-median column: the signs agree.")
    print("  session_seconds and spend are dragged right by their tails, pages_viewed")
    print("  is dragged much further by its bots, and screen_brightness is symmetric.")
    print("  Read excess kurtosis against 0, which is what a normal column scores.")
    print("  screen_brightness scores about -1.2, the uniform distribution's value,")
    print("  and negative excess kurtosis is what 'no tail' looks like as a number.")

    print("\nwhere the kurtosis actually comes from")
    print(f"  {'column':>16}  {'rows within 1 sd':>18}  {'share of kurtosis from them':>29}")
    for name in columns:
        share, rows = tail_share_of_kurtosis(df[name].to_numpy(float))
        print(f"  {name:>16}  {rows:>17.2%}  {share:>28.4%}")
    print("  For pages_viewed almost every row sits within 1 sd and those rows supply a")
    print("  fraction of one per cent of the statistic. The number is a report on the")
    print("  handful of rows that are far out. That is why 'peakedness' is the wrong")
    print("  word: the peak is where the statistic is least sensitive.")

    print("\nthe same point as a controlled experiment")
    print("  Two columns are built with the SAME variance and the SAME contaminating")
    print("  tail, differing only in the shape of the middle: one has a sharp Laplace")
    print("  peak, the other a flat uniform slab. If kurtosis measured peakedness,")
    print("  these two would score far apart.")
    rng = np.random.default_rng(20260822)
    n = 400_000
    sharp_core = rng.laplace(0.0, 1.0 / np.sqrt(2.0), size=n)   # variance 1
    flat_core = rng.uniform(-np.sqrt(3.0), np.sqrt(3.0), size=n)  # variance 1
    tail = rng.normal(0.0, 12.0, size=n)
    u = rng.random(n)

    print(f"\n  {'contamination rate':>20}  {'sharp peak':>12}  {'flat peak':>12}  {'difference':>12}")
    for rate in (0.005, 0.01, 0.02, 0.05, 0.12):
        pick = u < rate
        sharp = kurtosis(np.where(pick, tail, sharp_core)) - 3.0
        flat = kurtosis(np.where(pick, tail, flat_core)) - 3.0
        print(f"  {rate:>20.3f}  {sharp:>12.3f}  {flat:>12.3f}  {abs(sharp - flat):>12.3f}")

    pick = u < 0.02
    sharp_mix = np.where(pick, tail, sharp_core)
    flat_mix = np.where(pick, tail, flat_core)
    print("\n  The two columns agree on kurtosis to about a tenth of a unit out of")
    print("  eighty. Now look at the peaks they were supposed to be describing:")
    for label, col in (("sharp", sharp_mix), ("flat", flat_mix)):
        inside = float(np.mean(np.abs(col) < 0.5))
        print(f"    {label:>6} peak: {inside:6.2%} of rows within 0.5 of centre,"
              f"   median |x| = {float(np.median(np.abs(col))):.4f}")
    print("  Half the sharp column sits in that narrow band against well under a")
    print("  third of the flat one. Same kurtosis, different peak. It was never")
    print("  reporting on the peak, and the earlier table already said why: the peak")
    print("  contributes a fraction of a per cent of the sum.")

    print("\n" + "=" * 72)
    print("CHEBYSHEV'S INEQUALITY, A SPREAD BOUND THAT ASSUMES NO SHAPE")
    print("=" * 72 + "\n")
    section_chebyshev()


if __name__ == "__main__":
    main()
