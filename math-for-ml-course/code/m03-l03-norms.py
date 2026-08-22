"""M03 L03 - Norm, distance, and why the units decide the answer.

    python3 m03-l03-norms.py

Two results, each checked twice.

1. The norm axioms. Absolute homogeneity and the triangle inequality are checked
   on ten thousand random pairs drawn from the data, alongside the claim that the
   non-zero count fails homogeneity and is therefore not a norm.
2. The unit choice changes which houses are neighbours. The same nearest-neighbour
   search is run on raw features and on standardised features, and the two answers
   are different.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "housing.csv"
FEATURES = ["area_k_sqft", "bedrooms", "bathrooms", "age_years", "lot_sqft"]


def l1(v: np.ndarray) -> float:
    return float(np.abs(v).sum())


def l2(v: np.ndarray) -> float:
    return float(np.sqrt(v @ v))


def linf(v: np.ndarray) -> float:
    return float(np.abs(v).max())


def nonzero_count(v: np.ndarray) -> float:
    """Sometimes miscalled the "L0 norm". It is not a norm - see the check below."""
    return float(np.count_nonzero(v))


def main() -> None:
    frame = pd.read_csv(DATA)
    X = frame[FEATURES].to_numpy(dtype=float)

    v = np.array([3.0, -4.0, 0.0, 12.0])
    print("one vector, three sizes:  v = (3, -4, 0, 12)")
    print(f"  L1        = {l1(v):.0f}")
    print(f"  L2        = {l2(v):.0f}     (sqrt of 9 + 16 + 0 + 144 = sqrt 169)")
    print(f"  L-infinity= {linf(v):.0f}")
    print(f"  non-zeros = {nonzero_count(v):.0f}     (not a norm)")

    print("\n-- the axioms, on 10,000 random pairs from the data --")
    rng = np.random.default_rng(11)
    idx = rng.integers(0, len(X), size=(10_000, 2))
    alphas = rng.normal(0.0, 3.0, size=10_000)
    worst_homogeneity = 0.0
    triangle_holds = True
    homogeneity_fails_for_count = 0
    for (i, j), alpha in zip(idx, alphas):
        a, b = X[i], X[j]
        worst_homogeneity = max(worst_homogeneity, abs(l2(alpha * a) - abs(alpha) * l2(a)))
        if l2(a + b) > l2(a) + l2(b) + 1e-9:
            triangle_holds = False
        if abs(alpha) > 1e-9 and nonzero_count(alpha * a) != abs(alpha) * nonzero_count(a):
            homogeneity_fails_for_count += 1
    print(f"L2 absolute homogeneity, worst error over 10,000 draws: {worst_homogeneity:.3e}")
    print(f"L2 triangle inequality holds every time: {triangle_holds}")
    print(
        f"the non-zero count breaks homogeneity in {homogeneity_fails_for_count:,} of 10,000 draws,"
        " which is why it is not a norm"
    )

    print("\n-- distance depends on the units you chose --")
    # Which feature actually decides who is a neighbour? Take the mean share of
    # squared distance each feature contributes, over 2,000 random pairs.
    rng2 = np.random.default_rng(3)
    pairs = rng2.integers(0, len(X), size=(2_000, 2))
    diffs = X[pairs[:, 0]] - X[pairs[:, 1]]
    raw_share = (diffs**2).sum(axis=0) / (diffs**2).sum()

    Z = (X - X.mean(axis=0)) / X.std(axis=0)
    zdiffs = Z[pairs[:, 0]] - Z[pairs[:, 1]]
    std_share = (zdiffs**2).sum(axis=0) / (zdiffs**2).sum()

    print(f"{'feature':<12} {'raw share':>13} {'standardised':>14}")
    for name, r, s_ in zip(FEATURES, raw_share, std_share):
        print(f"{name:<12} {r:>12.8%} {s_:>13.2%}")
    print(f"raw: one feature carries {raw_share.max():.2%} of all squared distance")
    print(f"standardised: the largest share is {std_share.max():.2%} of five")

    # And it changes the answer, not only the bookkeeping.
    query = 0
    d_raw = np.linalg.norm(X - X[query], axis=1)
    d_std = np.linalg.norm(Z - Z[query], axis=1)
    d_raw[query] = np.inf
    d_std[query] = np.inf
    near_raw = set(np.argsort(d_raw)[:10].tolist())
    near_std = set(np.argsort(d_std)[:10].tolist())
    print(f"\n10 nearest houses to row 0, raw units vs standardised:")
    print(f"  houses in common: {len(near_raw & near_std)} of 10")

    print("\n-- standardisation is a norm fact before it is a statistics fact --")
    x = X[:, 0]
    demeaned = x - x.mean()
    std_from_norm = l2(demeaned) / np.sqrt(len(x))
    print(f"std(area) from the L2 norm of the de-meaned vector: {std_from_norm:.6f}")
    print(f"std(area) from numpy                              : {x.std():.6f}")
    assert abs(std_from_norm - x.std()) < 1e-9
    print("checked twice: a standard deviation is a norm divided by sqrt(n)")

    print("\n-- two real uses of a norm --")
    g = np.array([0.4, -1.2, 3.5, 0.9, -2.8, 1.1])
    threshold = 1.0
    clipped = g * (threshold / l2(g)) if l2(g) >= threshold else g
    print(f"gradient clipping: ||g|| = {l2(g):.4f} -> scale {threshold / l2(g):.4f}")
    print(f"  ||clipped|| = {l2(clipped):.6f}, cosine with g = {g @ clipped / (l2(g) * l2(clipped)):.6f}")
    a = np.array([0.5, -1.5, 2.0, 1.0, -0.5, 0.5, 1.5, -2.0])
    rms = np.sqrt((a**2).mean())
    print(f"RMSNorm: ||a||2 = {l2(a):.4f}, n = {len(a)}, RMS = {rms:.4f} = ||a||2/sqrt(n) = {l2(a)/np.sqrt(len(a)):.4f}")
    print(f"  RMS of a/RMS(a) = {np.sqrt(((a / rms) ** 2).mean()):.6f}")


if __name__ == "__main__":
    main()
