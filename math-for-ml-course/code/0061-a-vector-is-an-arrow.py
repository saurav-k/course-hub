"""Lesson 61 - adding and scaling are the only two operations.

The result this checks twice is that a linear combination is exactly what those
two operations build. Once with NumPy's vectorised arithmetic, and once with a
plain Python loop over the entries, which is the definition written out.

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


def combination_by_definition(vectors: list[np.ndarray], weights: list[float]) -> np.ndarray:
    """c1*a1 + ... + ck*ak, one entry at a time, with no broadcasting anywhere."""
    length = len(vectors[0])
    out = [0.0] * length
    for vector, weight in zip(vectors, weights):
        for i in range(length):
            out[i] = out[i] + weight * vector[i]
    return np.array(out)


def main() -> None:
    frame = load()
    readings = frame[SENSORS[:3]].to_numpy(dtype=float)
    a, b, c = readings[0], readings[1], readings[2]

    print(f"three readings, as vectors of {SENSORS[:3]}")
    for name, v in (("a", a), ("b", b), ("c", c)):
        print(f"  {name} = {np.round(v, 4)}")

    print("\n-- the two operations --")
    print(f"a + b  = {np.round(a + b, 4)}")
    print(f"2 * a  = {np.round(2 * a, 4)}")
    print(f"-1 * a = {np.round(-a, 4)}   (same length, opposite direction)")
    print(f"a - b  = {np.round(a - b, 4)}   (which is a plus -1 times b)")

    print("\n-- a linear combination, checked twice --")
    weights = [0.5, 0.3, 0.2]
    by_numpy = weights[0] * a + weights[1] * b + weights[2] * c
    by_hand = combination_by_definition([a, b, c], weights)
    print(f"0.5a + 0.3b + 0.2c = {np.round(by_numpy, 6)}")
    assert np.allclose(by_numpy, by_hand)
    print("checked twice: vectorised and entry-by-entry agree")

    print("\n-- a gradient step is one scale and one subtraction --")
    rng = np.random.default_rng(0)
    w = rng.normal(0.0, 0.5, size=3)
    g = rng.normal(0.0, 1.0, size=3)
    eta = 0.1
    print(f"w        = {np.round(w, 4)}")
    print(f"g        = {np.round(g, 4)}")
    print(f"w - {eta}g = {np.round(w - eta * g, 4)}")
    assert np.allclose(w - eta * g, combination_by_definition([w, g], [1.0, -eta]))
    print(f"which is the combination 1.0*w + {-eta}*g, checked twice")

    print("\n-- the whole dataset is 12,000 of these --")
    X = frame[SENSORS].to_numpy(dtype=float)
    print(f"mean reading, a combination with every weight 1/{len(X)}:")
    print(f"  {np.round(X.mean(axis=0), 4)}")


if __name__ == "__main__":
    main()
