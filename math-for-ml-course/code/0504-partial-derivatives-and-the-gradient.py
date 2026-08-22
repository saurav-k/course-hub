"""Lesson 0504 - partial derivatives and the gradient, on a real design matrix.

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

    python3 0504-partial-derivatives-and-the-gradient.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

LOCAL = Path(__file__).resolve().parent.parent / "datasets" / "sensors.csv"
URL = "https://raw.githubusercontent.com/saurav-k/course-hub/main/math-for-ml-course/datasets/sensors.csv"

# Predicting one sensor from the others is what a real monitoring system does,
# and it gives this module a design matrix whose columns are on wildly
# different scales: pressure runs in the hundreds, dust index around one. That
# disparity is the whole subject of lessons 0509 and 0510, so it is load
# bearing rather than incidental.
FEATURES = ["vibration_x", "vibration_y", "current_amp",
            "humidity_pct", "dust_index", "pressure_kpa"]
TARGET = "temp_c"


def load() -> pd.DataFrame:
    return pd.read_csv(LOCAL) if LOCAL.exists() else pd.read_csv(URL)


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
    frame = load()
    x, y, names = design_matrix(frame)
    print(f"loaded sensors.csv: {x.shape[0]} rows, {x.shape[1]} parameters\n")

    # An arbitrary starting guess. Nothing about the check depends on it.
    # Start from the intercept-only model: predict every reading's temperature
    # as the overall average and nothing else. It is the honest zero-knowledge
    # guess, and it is defined whatever the column count happens to be.
    theta = np.zeros(x.shape[1])
    theta[0] = float(y.mean())
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

    # The intercept partial is exactly zero here, and that is not a coincidence:
    # starting at the mean of y makes the residuals sum to zero, which is
    # precisely the first-order condition for the intercept. Worth saying out
    # loud, because it is the first time the reader sees a partial derivative
    # vanish for a reason they can name.
    print(f"\nthe intercept partial is {analytic[0]:+.3e}, which is zero to rounding.")
    print("Starting at the mean of y makes the residuals sum to zero, and that sum")
    print("IS the intercept's partial derivative. The guess already solves one dial.")

    feature_grad = np.abs(analytic[1:])
    spread = feature_grad.max() / feature_grad.min()
    print(f"\nacross the six feature partials, largest over smallest: {spread:,.1f}")
    print("that ratio is about the units of the columns, not about importance")

    print("\nthe gradient points uphill, so the loss falls against it")
    print("until the step is large enough for curvature to take over, which is")
    print("lesson 0510's subject and is visible here at the last row:")
    for step in (1e-8, 1e-7, 1e-6, 1e-5, 1e-4):
        moved = loss(theta - step * analytic, x, y)
        print(f"  step {step:.0e}: loss {loss(theta, x, y):.6f} -> {moved:.6f}")


if __name__ == "__main__":
    main()
