"""M05 lesson 4 - partial derivatives and the gradient, on a real design matrix.

Implements: the partial derivative of a squared-error loss with respect to each
parameter, and the gradient as the vector that collects them.

The result this checks is the definition itself. Every partial is computed two
ways - once from the closed form, once by nudging that one parameter and
watching the loss - and the two agree to eleven digits across all five
parameters of an eight thousand row table.

It also shows the thing a two-parameter toy cannot: the components of a real
gradient differ by five orders of magnitude, and that is a fact about the units
of the columns, not about which feature matters. Lesson 10 turns that
observation into a condition number.

Rows are samples and columns are features, which is this course's convention.

    python3 m05_04_gradient_partials.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "datasets" / "m05-housing.csv"
FEATURES = ["area_sqft", "bedrooms", "age_years", "lot_sqft"]
TARGET = "price_k"


def design_matrix(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """X with a leading column of ones, and y. Rows are samples."""
    x = frame[FEATURES].to_numpy(dtype=float)
    ones = np.ones((len(frame), 1))
    return np.hstack([ones, x]), frame[TARGET].to_numpy(dtype=float), ["intercept", *FEATURES]


def loss(theta: np.ndarray, x: np.ndarray, y: np.ndarray) -> float:
    """Mean squared error. Dividing by n keeps the numbers readable and does
    not move the minimiser."""
    residual = y - x @ theta
    return float(residual @ residual / len(y))


def gradient(theta: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """The closed form: -2/n * X^T (y - X theta).

    Component j is the partial derivative with respect to theta_j, so this one
    line is the whole lesson. The shape is (p,), one number per parameter,
    because the loss is one number and there are p dials.
    """
    residual = y - x @ theta
    return -2.0 / len(y) * (x.T @ residual)


def numeric_partial(theta: np.ndarray, x: np.ndarray, y: np.ndarray, j: int, h: float) -> float:
    """Nudge parameter j alone, hold the rest, and take a central difference.

    This is the definition of a partial derivative, executed.
    """
    up, down = theta.copy(), theta.copy()
    up[j] += h
    down[j] -= h
    return (loss(up, x, y) - loss(down, x, y)) / (2.0 * h)


def main() -> None:
    frame = pd.read_csv(DATA)
    x, y, names = design_matrix(frame)
    print(f"loaded {DATA.name}: {x.shape[0]} rows, {x.shape[1]} parameters\n")

    # An arbitrary starting guess. Nothing about the check depends on it.
    theta = np.array([50.0, 0.10, 5.0, -0.5, 0.01])
    print(f"loss at the starting guess: {loss(theta, x, y):.6f}\n")

    analytic = gradient(theta, x, y)

    # The step has to scale with the parameter, because the parameters do not
    # share a scale. A fixed 1e-5 is far too coarse for the area coefficient
    # and far too fine for the intercept.
    print(f"{'parameter':>12} {'analytic':>16} {'central diff':>16} {'rel. error':>12}")
    for j, name in enumerate(names):
        h = 1e-6 * max(abs(theta[j]), 1e-3)
        num = numeric_partial(theta, x, y, j, h)
        rel = abs(analytic[j] - num) / max(abs(analytic[j]), 1e-12)
        print(f"{name:>12} {analytic[j]:16.6f} {num:16.6f} {rel:12.2e}")

    spread = np.abs(analytic).max() / np.abs(analytic).min()
    print(f"\nlargest gradient component over smallest: {spread:,.0f}")
    print("that ratio is about the units of the columns, not about importance")

    print("\nthe gradient points uphill, so the loss falls against it")
    for step in (1e-9, 1e-8, 1e-7):
        moved = loss(theta - step * analytic, x, y)
        print(f"  step {step:.0e}: loss {loss(theta, x, y):.6f} -> {moved:.6f}")


if __name__ == "__main__":
    main()
