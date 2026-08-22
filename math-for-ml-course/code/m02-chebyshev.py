"""Chebyshev's inequality: a spread bound that assumes nothing about shape.

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
buys that tightness by assuming normality, which a latency column does not have.

Dataset: nimbus-sessions.csv. latency_ms is heavy-tailed, temp_c is close to
normal, and the gap between what Chebyshev guarantees and what each column
actually does is the point.

Needs numpy and pandas only.
"""

import pathlib

import numpy as np
import pandas as pd

LOCAL = pathlib.Path(__file__).resolve().parent.parent / "datasets" / "nimbus-sessions.csv"
URL = "https://<hub>/math-for-ml-course/datasets/nimbus-sessions.csv"
DATA = LOCAL if LOCAL.exists() else URL
EMPIRICAL_RULE = {1: 0.6827, 2: 0.9545, 3: 0.9973, 4: 0.999937}


def within_k_sd(x: np.ndarray, k: float) -> float:
    mu, sd = x.mean(), x.std(ddof=0)
    return float(np.mean(np.abs(x - mu) < k * sd))


def main() -> None:
    df = pd.read_csv(DATA)
    print(f"n = {len(df):,} sessions\n")
    print(f"{'k':>3}  {'Chebyshev floor':>16}  {'latency_ms':>12}  {'temp_c':>10}  {'normal (empirical rule)':>24}")
    for k in (1, 2, 3, 4):
        floor = 0.0 if k == 1 else 1 - 1 / k ** 2
        print(f"{k:>3}  {floor:>16.4f}  {within_k_sd(df.latency_ms.to_numpy(float), k):>12.4f}"
              f"  {within_k_sd(df.temp_c.to_numpy(float), k):>10.4f}  {EMPIRICAL_RULE[k]:>24.4f}")

    print("\nreading the table")
    print("  Every column beats the Chebyshev floor, as it must: the floor is a")
    print("  guarantee, not a prediction. At k = 1 the floor is 0, which is a true")
    print("  statement that tells you nothing, and that is the honest cost of")
    print("  assuming nothing.")
    print("  temp_c tracks the empirical rule closely because it was generated normal.")
    print("  latency_ms does not, and the direction surprises people. Its standard")
    print("  deviation is inflated by the cold starts, so almost everything sits")
    print("  inside 1 sd, well above the 0.68 a normal column gives. The mass that")
    print("  does escape then goes very much further out. The counts below are the")
    print("  same fact from the other end.")

    x = df.latency_ms.to_numpy(float)
    mu, sd = x.mean(), x.std(ddof=0)
    for k in (3, 4, 6, 10):
        beyond = int((np.abs(x - mu) >= k * sd).sum())
        print(f"    beyond {k:>2} sd: latency_ms has {beyond:>5} sessions"
              f"   Chebyshev allows up to {len(df) / k ** 2:>8.0f}"
              f"   a normal column would give about {len(df) * (1 - EMPIRICAL_RULE.get(k, 1.0)):>6.0f}")

    print("\n  Chebyshev is never violated and is never tight. That is the trade:")
    print("  it is the bound you can use when you do not know the shape.")


if __name__ == "__main__":
    main()
