"""Lesson 40 - shape is the contract: axes, indexing, and broadcasting.

The result this checks twice is NumPy's broadcasting rule. Once by letting NumPy
apply it, and once by expanding both operands by hand with np.repeat, which is
what broadcasting is a shorthand for. If those ever disagreed, the rule as the
lesson states it would be wrong.

It then shows the failure the lesson exists to warn about: centring a data matrix
on the wrong axis runs clean and centres nothing.

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


def broadcast_by_hand(column: np.ndarray, row: np.ndarray) -> np.ndarray:
    """What NumPy does when it broadcasts (n,1) against (n,), written out.

    An axis of size 1 is stretched to match the other operand, and a missing
    leading axis counts as size 1. Doing both explicitly is the check.
    """
    n = column.shape[0]
    left = np.repeat(column, n, axis=1)
    right = np.repeat(row.reshape(1, n), n, axis=0)
    return left - right


def main() -> None:
    frame = load()
    X = frame[SENSORS].to_numpy(dtype=float)

    print(f"rows (samples)    : {X.shape[0]:,}")
    print(f"columns (features): {X.shape[1]}")
    print(f"X.shape           : {X.shape}")
    print(f"X[0, :] is one reading : {np.round(X[0], 3)}")
    print(f"X[:, 0] is one sensor  : first three are {np.round(X[:3, 0], 3)}")

    batch, seq, d_model = 16, 1024, 4096
    total = batch * seq * d_model
    print(f"\na (batch, seq, d_model) tensor of ({batch}, {seq}, {d_model}) holds "
          f"{total:,} numbers, {total * 2 / 1e6:.1f} MB in fp16")

    print("\n-- the broadcasting trap, on the first eight readings --")
    values = X[:8, 0]
    column = values.reshape(8, 1)
    print(f"values.shape           : {values.shape}")
    print(f"column.shape           : {column.shape}")
    print(f"(values - values).shape: {(values - values).shape}   <- what you meant")
    print(f"(column - values).shape: {(column - values).shape}  <- what you get, silently")

    by_numpy = column - values
    by_hand = broadcast_by_hand(column, values)
    assert by_numpy.shape == by_hand.shape == (8, 8)
    assert np.array_equal(by_numpy, by_hand)
    print("checked twice: NumPy's broadcast equals the hand expansion, entry for entry")

    print("\n-- centring: the axis decides whether it is right --")
    feature_means = X.mean(axis=0)
    print(f"X.mean(axis=0).shape: {feature_means.shape}  (one mean per sensor)")
    print(f"max |column mean| after X - X.mean(axis=0): "
          f"{np.abs((X - feature_means).mean(axis=0)).max():.3e}")

    reading_means = X.mean(axis=1, keepdims=True)
    print(f"X.mean(axis=1, keepdims=True).shape: {reading_means.shape}  (one mean per reading)")
    print(f"max |column mean| after X - THAT          : "
          f"{np.abs((X - reading_means).mean(axis=0)).max():,.3f}")
    print("The second runs clean and centres nothing any model cares about.")


if __name__ == "__main__":
    main()
