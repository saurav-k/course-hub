"""Lesson 0502 - the chain rule, checked on a real cross-entropy.

Implements the identity every binary classifier depends on:

    d/dz  of  -[y log sigma(z) + (1-y) log(1 - sigma(z))]  =  sigma(z) - y

The point of running it on twenty thousand real logits rather than on one
number is that the identity is not a coincidence at a convenient point. The
program computes the derivative two ways for every row - once by the closed
form the chain rule gives, once by a central difference - and asserts they
agree across the whole table.

It also shows why the fused form exists: written the way it reads on paper, the
loss overflows at logits a real model produces.

The logits are not handed over in the dataset. The program fits the model
itself by Newton's method, because a score that arrives from nowhere teaches
nothing about where scores come from.

Needs only numpy and pandas. Runs in a codebase, in Jupyter, or in Colab.

    python3 0502-the-chain-rule.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "failures.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/failures.csv"

TARGET = "failed"


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


def sigmoid(z: np.ndarray) -> np.ndarray:
    """Logistic function, evaluated in whichever of its two algebraically equal
    forms cannot overflow at the sign of z."""
    out = np.empty_like(z, dtype=float)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    e = np.exp(z[~pos])
    out[~pos] = e / (1.0 + e)
    return out


def design(frame: pd.DataFrame) -> np.ndarray:
    """Rows are samples, columns are features, per the course convention.

    The functional forms - a log on hours, a square on load - are the ones the
    generator used. Recovering them is not this lesson's subject; using a model
    that fits is, because a badly fitted model makes a dull gradient.
    """
    columns = [
        np.ones(len(frame)),
        np.log(frame["hours_since_service"].to_numpy(dtype=float)),
        frame["load_pct"].to_numpy(dtype=float) ** 2,
        np.log(frame["vibration_mm_s"].to_numpy(dtype=float)),
        frame["coolant_c"].to_numpy(dtype=float),
    ]
    x = np.column_stack(columns)
    # Standardise every column but the intercept, so Newton's method is not
    # fighting the same conditioning problem lesson 0510 is about.
    scale = x.std(axis=0)
    scale[0] = 1.0
    centre = x.mean(axis=0)
    centre[0] = 0.0
    return (x - centre) / scale


def fit_logistic(x: np.ndarray, y: np.ndarray, steps: int = 50) -> np.ndarray:
    """Newton's method on the cross-entropy. Ten lines, no library.

    The gradient and the Hessian are exactly the objects lessons 0504 and 0509
    define, which is why this fit belongs in the module rather than in a
    dependency.
    """
    w = np.zeros(x.shape[1])
    for _ in range(steps):
        p = sigmoid(x @ w)
        gradient = x.T @ (p - y) / len(y)
        weights = np.clip(p * (1.0 - p), 1e-12, None)
        hessian = (x * weights[:, None]).T @ x / len(y)
        w -= np.linalg.solve(hessian + 1e-10 * np.eye(len(w)), gradient)
    return w


def loss_from_logit(z: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Binary cross-entropy as a function of the logit, in the stable form.

    log(1 + e^z) is written max(z,0) + log(1 + e^-|z|), which is the same
    number and never exponentiates a large positive value.
    """
    return np.maximum(z, 0.0) - z * y + np.log1p(np.exp(-np.abs(z)))


def loss_naive(z: np.ndarray, y: np.ndarray) -> np.ndarray:
    """The same loss written the way it reads on paper. Kept because the
    lesson's point is that this one loses to floating point."""
    p = sigmoid(z)
    return -(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))


def gradient_by_chain_rule(z: np.ndarray, y: np.ndarray) -> np.ndarray:
    """What the chain rule gives, after the sigmoid and the log cancel."""
    return sigmoid(z) - y


def gradient_by_definition(z: np.ndarray, y: np.ndarray, h: float = 1e-5) -> np.ndarray:
    """The derivative straight from its definition, one central difference per row."""
    return (loss_from_logit(z + h, y) - loss_from_logit(z - h, y)) / (2.0 * h)


def main() -> None:
    frame = load()
    y = frame[TARGET].to_numpy(dtype=float)
    x = design(frame)
    print(f"loaded failures.csv: {len(frame)} rows, {int(y.sum())} positive\n")

    w = fit_logistic(x, y)
    z = x @ w
    print(f"fitted by Newton's method in 50 steps, {len(w)} coefficients")
    print(f"logits run from {z.min():.3f} to {z.max():.3f}\n")

    chain = gradient_by_chain_rule(z, y)
    definition = gradient_by_definition(z, y)
    gap = np.abs(chain - definition)

    print("the chain rule against the definition, every row")
    print(f"  largest absolute disagreement : {gap.max():.3e}")
    print(f"  mean absolute disagreement    : {gap.mean():.3e}")
    assert gap.max() < 1e-7, "the chain rule and the definition must agree"
    print("  assertion passed: the two agree to better than 1e-7 on all rows")

    print("\nwhat the fitted model looks like")
    print(f"  mean cross-entropy : {loss_from_logit(z, y).mean():.6f}")
    print(f"  mean gradient      : {chain.mean():+.6e}")
    print("  the mean gradient is zero because a fitted intercept forces it to be:")
    print("  it IS the intercept's partial derivative, and Newton drove that to zero.")

    print("\nthe gradient is the prediction error, so it is bounded by one")
    print(f"  most negative : {chain.min():+.6f}   (confident zero on a positive row)")
    print(f"  most positive : {chain.max():+.6f}   (confident one on a negative row)")

    print("\nwhy the fused form exists")
    extreme = np.array([-800.0, -40.0, 0.0, 40.0, 800.0])
    labels = np.array([1.0, 1.0, 1.0, 0.0, 0.0])
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        naive = loss_naive(extreme, labels)
    stable = loss_from_logit(extreme, labels)
    print(f"  {'logit':>8} {'naive':>14} {'stable':>14}")
    for zi, n, s in zip(extreme, naive, stable):
        print(f"  {zi:8.0f} {n:14.6f} {s:14.6f}")
    print("  the naive column returns inf where the stable column is finite and right")


if __name__ == "__main__":
    main()
