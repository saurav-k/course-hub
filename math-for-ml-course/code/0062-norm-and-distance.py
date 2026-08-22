"""Lesson 62 - norm, distance, and why the units decide the answer.

Two results, each checked twice.

1. The norm axioms. Absolute homogeneity and the triangle inequality are checked
   on 10,000 random pairs drawn from the data, alongside the claim that the
   non-zero count fails homogeneity and is therefore not a norm.
2. The unit choice decides who counts as a neighbour. The share of squared
   distance each sensor carries is measured raw and standardised, and the ten
   nearest readings are found both ways and compared.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.
"""

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "sensors.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/sensors.csv"

SENSORS = [
    "vibration_x", "vibration_y", "acoustic_db", "current_amp",
    "humidity_pct", "dust_index", "temp_c", "pressure_kpa",
]


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def l1(v: np.ndarray) -> float:
    return float(np.abs(v).sum())


def l2(v: np.ndarray) -> float:
    return float(np.sqrt(v @ v))


def linf(v: np.ndarray) -> float:
    return float(np.abs(v).max())


def nonzero_count(v: np.ndarray) -> float:
    """Sometimes miscalled the "L0 norm". It is not one - see the check below."""
    return float(np.count_nonzero(v))


def main() -> None:
    X = load()[SENSORS].to_numpy(dtype=float)

    v = np.array([3.0, -4.0, 0.0, 12.0])
    print("one vector, three sizes:  v = (3, -4, 0, 12)")
    print(f"  L1         = {l1(v):.0f}")
    print(f"  L2         = {l2(v):.0f}     (sqrt of 9 + 16 + 0 + 144 = sqrt 169)")
    print(f"  L-infinity = {linf(v):.0f}")
    print(f"  non-zeros  = {nonzero_count(v):.0f}     (not a norm)")

    print("\n-- the axioms, on 10,000 random pairs from the data --")
    rng = np.random.default_rng(11)
    idx = rng.integers(0, len(X), size=(10_000, 2))
    alphas = rng.normal(0.0, 3.0, size=10_000)
    worst = 0.0
    triangle_holds = True
    count_fails = 0
    for (i, j), alpha in zip(idx, alphas):
        a, b = X[i], X[j]
        worst = max(worst, abs(l2(alpha * a) - abs(alpha) * l2(a)))
        if l2(a + b) > l2(a) + l2(b) + 1e-9:
            triangle_holds = False
        if abs(alpha) > 1e-9 and nonzero_count(alpha * a) != abs(alpha) * nonzero_count(a):
            count_fails += 1
    print(f"L2 absolute homogeneity, worst error: {worst:.3e}")
    print(f"L2 triangle inequality holds every time: {triangle_holds}")
    print(f"the non-zero count breaks homogeneity in {count_fails:,} of 10,000 draws")
    assert triangle_holds and count_fails == 10_000

    print("\n-- which sensor decides who is a neighbour --")
    pairs = np.random.default_rng(3).integers(0, len(X), size=(2_000, 2))
    diffs = X[pairs[:, 0]] - X[pairs[:, 1]]
    raw_share = (diffs ** 2).sum(axis=0) / (diffs ** 2).sum()

    Z = (X - X.mean(axis=0)) / X.std(axis=0)
    zdiffs = Z[pairs[:, 0]] - Z[pairs[:, 1]]
    std_share = (zdiffs ** 2).sum(axis=0) / (zdiffs ** 2).sum()

    print(f"{'sensor':<14}{'raw share':>13}{'standardised':>14}")
    for name, r, s in zip(SENSORS, raw_share, std_share):
        print(f"{name:<14}{r:>12.6%} {s:>13.2%}")
    print(f"raw: one sensor carries {raw_share.max():.2%} of all squared distance")
    print(f"standardised: the largest share is {std_share.max():.2%} of eight")

    query = 0
    d_raw = np.linalg.norm(X - X[query], axis=1)
    d_std = np.linalg.norm(Z - Z[query], axis=1)
    d_raw[query] = d_std[query] = np.inf
    overlap = len(set(np.argsort(d_raw)[:10].tolist()) & set(np.argsort(d_std)[:10].tolist()))
    print(f"\nten nearest readings to row 0, raw against standardised: {overlap} in common of 10")

    print("\n-- a standard deviation is a norm --")
    x = X[:, 0]
    from_norm = l2(x - x.mean()) / np.sqrt(len(x))
    print(f"||x - mean|| / sqrt(n) = {from_norm:.6f}")
    print(f"numpy std(x)           = {x.std():.6f}")
    assert abs(from_norm - x.std()) < 1e-9
    print("checked twice: same number, two routes")

    print("\n-- two real uses of a norm --")
    g = np.array([0.4, -1.2, 3.5, 0.9, -2.8, 1.1])
    clipped = g * (1.0 / l2(g))
    print(f"gradient clipping: ||g|| = {l2(g):.4f}, scale {1.0 / l2(g):.4f}, "
          f"||clipped|| = {l2(clipped):.6f}, cosine = {g @ clipped / (l2(g) * l2(clipped)):.6f}")
    a = np.array([0.5, -1.5, 2.0, 1.0, -0.5, 0.5, 1.5, -2.0])
    rms = np.sqrt((a ** 2).mean())
    print(f"RMSNorm: ||a|| = {l2(a):.4f}, n = {len(a)}, RMS = {rms:.4f} "
          f"= ||a||/sqrt(n) = {l2(a) / np.sqrt(len(a)):.4f}")


if __name__ == "__main__":
    main()
