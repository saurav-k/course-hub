"""M03 L01 - Shape is the contract: axes, indexing, and broadcasting.

Runs against datasets/housing.csv. Needs numpy and pandas and nothing else.

    python3 m03-l01-shapes.py

The result this checks twice: NumPy's broadcasting rule. Once by letting NumPy
apply it, and once by expanding the arrays by hand with np.repeat, which is what
broadcasting is a shorthand for. If the two ever disagreed, the rule as the page
states it would be wrong.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "datasets" / "housing.csv"
FEATURES = ["area_k_sqft", "bedrooms", "bathrooms", "age_years", "lot_sqft"]


def broadcast_by_hand(column: np.ndarray, row: np.ndarray) -> np.ndarray:
    """What NumPy does when it broadcasts (n,1) against (n,), written out.

    An axis of size 1 is stretched to match the other operand, and a missing
    leading axis is treated as size 1. Doing it explicitly is the check.
    """
    n = column.shape[0]
    left = np.repeat(column, n, axis=1)          # (n,1) -> (n,n)
    right = np.repeat(row.reshape(1, n), n, axis=0)  # (n,) -> (1,n) -> (n,n)
    return left - right


def main() -> None:
    frame = pd.read_csv(DATA)
    X = frame[FEATURES].to_numpy(dtype=float)

    print(f"rows (samples)   : {X.shape[0]:,}")
    print(f"columns (features): {X.shape[1]}")
    print(f"X.shape          : {X.shape}")
    print(f"X[0, :]  is one sample : {np.round(X[0], 3)}")
    print(f"X[:, 0]  is one feature: first three are {np.round(X[:3, 0], 3)}")

    # A stand-in for a batch of token activations: three axes, each counting
    # something different. Reading a shape is reading three questions.
    batch, seq, d_model = 16, 1024, 4096
    print(
        f"\na (batch, seq, d_model) tensor of ({batch}, {seq}, {d_model}) holds "
        f"{batch * seq * d_model:,} numbers, {batch * seq * d_model * 2 / 1e6:.1f} MB in fp16"
    )

    print("\n-- the broadcasting trap, on the first eight areas --")
    areas = X[:8, 0]
    column = areas.reshape(8, 1)
    print(f"areas.shape          : {areas.shape}")
    print(f"column.shape         : {column.shape}")
    print(f"(areas - areas).shape: {(areas - areas).shape}   <- what you meant")
    print(f"(column - areas).shape: {(column - areas).shape}  <- what you get, silently")

    by_numpy = column - areas
    by_hand = broadcast_by_hand(column, areas)
    assert by_numpy.shape == by_hand.shape == (8, 8)
    assert np.array_equal(by_numpy, by_hand)
    print("checked twice: NumPy's broadcast equals the hand expansion, exactly")

    print("\n-- centring: the axis decides whether it is right --")
    feature_means = X.mean(axis=0)
    centred_right = X - feature_means
    print(f"X.mean(axis=0).shape : {feature_means.shape}  (one mean per feature)")
    print(f"max |column mean| after centring: {np.abs(centred_right.mean(axis=0)).max():.3e}")

    sample_means = X.mean(axis=1, keepdims=True)
    centred_wrong = X - sample_means
    print(f"X.mean(axis=1, keepdims=True).shape: {sample_means.shape}  (one mean per sample)")
    print(f"max |column mean| after THAT      : {np.abs(centred_wrong.mean(axis=0)).max():,.1f}")
    print("The second runs clean and centres nothing a model cares about.")


if __name__ == "__main__":
    main()
