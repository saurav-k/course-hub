"""M03 L02 - Adding and scaling are the only two operations.

    python3 m03-l02-linear-combination.py

The result this checks twice: that a linear combination is exactly what the two
operations build. Once with NumPy's vectorised arithmetic, and once with a plain
Python loop over the entries, which is the definition written out.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "housing.csv"
FEATURES = ["area_k_sqft", "bedrooms", "bathrooms"]


def combination_by_definition(vectors: list[np.ndarray], weights: list[float]) -> np.ndarray:
    """c1*a1 + ... + ck*ak, one entry at a time, with no NumPy broadcasting."""
    length = len(vectors[0])
    out = [0.0] * length
    for vector, weight in zip(vectors, weights):
        for i in range(length):
            out[i] = out[i] + weight * vector[i]
    return np.array(out)


def main() -> None:
    frame = pd.read_csv(DATA)
    houses = frame[FEATURES].to_numpy(dtype=float)

    a, b, c = houses[0], houses[1], houses[2]
    print(f"three houses, as vectors of {FEATURES}")
    print(f"  a = {np.round(a, 3)}")
    print(f"  b = {np.round(b, 3)}")
    print(f"  c = {np.round(c, 3)}")

    print("\n-- the two operations --")
    print(f"a + b        = {np.round(a + b, 3)}")
    print(f"2 * a        = {np.round(2 * a, 3)}")
    print(f"-1 * a       = {np.round(-a, 3)}   (same length, opposite direction)")
    print(f"a - b        = {np.round(a - b, 3)}   (add a and -1 times b)")

    print("\n-- a linear combination, checked twice --")
    weights = [0.5, 0.3, 0.2]
    by_numpy = weights[0] * a + weights[1] * b + weights[2] * c
    by_hand = combination_by_definition([a, b, c], weights)
    print(f"0.5a + 0.3b + 0.2c = {np.round(by_numpy, 4)}")
    assert np.allclose(by_numpy, by_hand)
    print("checked twice: vectorised and entry-by-entry agree")

    print("\n-- a gradient step is one scale and one subtraction --")
    rng = np.random.default_rng(0)
    w = rng.normal(0.0, 0.5, size=len(FEATURES))
    g = rng.normal(0.0, 1.0, size=len(FEATURES))
    eta = 0.1
    w_new = w - eta * g
    print(f"w      = {np.round(w, 4)}")
    print(f"g      = {np.round(g, 4)}")
    print(f"w - {eta}g = {np.round(w_new, 4)}")
    assert np.allclose(w_new, combination_by_definition([w, g], [1.0, -eta]))
    print(f"which is the combination 1.0*w + {-eta}*g, checked twice")

    print("\n-- the whole dataset is 20,000 of these vectors --")
    print(f"mean house, as a combination with every weight 1/{len(houses)}:")
    print(f"  {np.round(houses.mean(axis=0), 4)}")


if __name__ == "__main__":
    main()
