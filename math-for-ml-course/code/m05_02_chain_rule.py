"""M05 lesson 2 - the chain rule, checked on a real cross-entropy.

Implements: the chain rule, and the identity every binary classifier depends on

    d/dz  of  -[y log sigma(z) + (1-y) log(1 - sigma(z))]  =  sigma(z) - y

The point of running this on twenty thousand real logits rather than on one
number is that the identity is not a coincidence at a convenient point. The
program differentiates the composition two ways for every row of the dataset -
once by the closed form above, once by a central difference - and reports the
largest disagreement across the whole table.

It also shows why the fused form exists: evaluated the naive way, the loss
overflows for logits a real model produces.

    python3 m05_02_chain_rule.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "datasets" / "m05-scores.csv"


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Logistic function, evaluated in whichever of its two algebraically equal
    forms cannot overflow at the sign of z."""
    out = np.empty_like(z, dtype=float)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    e = np.exp(z[~pos])
    out[~pos] = e / (1.0 + e)
    return out


def bce_from_logit(z: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Binary cross-entropy as a function of the logit, in the stable form.

    log(1 + e^z) is written as max(z,0) + log(1 + e^-|z|), which is the same
    number and never exponentiates a large positive value.
    """
    return np.maximum(z, 0.0) - z * y + np.log1p(np.exp(-np.abs(z)))


def bce_naive(z: np.ndarray, y: np.ndarray) -> np.ndarray:
    """The same loss written the way it reads on paper. Kept in the file
    because the lesson's point is that this one loses to floating point."""
    p = sigmoid(z)
    return -(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))


def analytic_grad(z: np.ndarray, y: np.ndarray) -> np.ndarray:
    """The chain rule's answer: sigma(z) - y."""
    return sigmoid(z) - y


def numeric_grad(z: np.ndarray, y: np.ndarray, h: float = 1e-5) -> np.ndarray:
    """Central difference in the logit, one per row."""
    return (bce_from_logit(z + h, y) - bce_from_logit(z - h, y)) / (2.0 * h)


def main() -> None:
    frame = pd.read_csv(DATA)
    z = frame["logit"].to_numpy(dtype=float)
    y = frame["label"].to_numpy(dtype=float)
    print(f"loaded {DATA.name}: {len(frame)} rows\n")

    analytic = analytic_grad(z, y)
    numeric = numeric_grad(z, y)
    gap = np.abs(analytic - numeric)

    print("the chain rule against a central difference, all rows")
    print(f"  largest absolute disagreement : {gap.max():.3e}")
    print(f"  mean absolute disagreement    : {gap.mean():.3e}")
    print(f"  rows disagreeing by over 1e-7 : {(gap > 1e-7).sum()}")

    print("\nmean loss and mean gradient over the table")
    print(f"  mean cross-entropy : {bce_from_logit(z, y).mean():.6f}")
    print(f"  mean gradient      : {analytic.mean():+.6f}")

    # The mean gradient is the calibration residual: it is the average
    # predicted probability minus the base rate.
    print(f"  mean score - base rate : {sigmoid(z).mean() - y.mean():+.6f}")

    print("\nwhy the fused form exists")
    extreme = np.array([-800.0, -40.0, 0.0, 40.0, 800.0])
    labels = np.array([1.0, 1.0, 1.0, 0.0, 0.0])
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        naive = bce_naive(extreme, labels)
    stable = bce_from_logit(extreme, labels)
    print(f"{'logit':>8} {'naive':>14} {'stable':>14}")
    for zi, n, s in zip(extreme, naive, stable):
        print(f"{zi:8.0f} {n:14.6f} {s:14.6f}")
    print("  the naive column returns inf where the stable column is finite and correct")


if __name__ == "__main__":
    main()
