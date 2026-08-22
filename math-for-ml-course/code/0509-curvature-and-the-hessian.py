"""Lesson 0509 - curvature, the Hessian, and the second-derivative test.

Implements three named results.

1.  Schwarz's theorem. Where the second partials are continuous the order of
    differentiation does not matter, so the Hessian is symmetric. Checked by
    computing both mixed partials numerically and comparing.

2.  The directional second derivative is d^T H d, it equals the eigenvalue
    when d is an eigenvector, and the extreme eigenvalues bracket every
    direction. Checked against a second central difference along random rays.

3.  The second-derivative test. At a critical point, all positive eigenvalues
    means a minimum, all negative a maximum, mixed signs a saddle, and a zero
    eigenvalue with the rest one sign is inconclusive. Applied to the housing
    loss, and to three constructed surfaces that exercise every branch.

    python3 0509-curvature-and-the-hessian.py
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
SEED = 20260822


def design_matrix(frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    x = frame[FEATURES].to_numpy(dtype=float)
    return np.hstack([np.ones((len(frame), 1)), x]), frame[TARGET].to_numpy(dtype=float)


def loss(theta: np.ndarray, x: np.ndarray, y: np.ndarray) -> float:
    r = y - x @ theta
    return float(r @ r / len(y))


def hessian(x: np.ndarray, n: int) -> np.ndarray:
    """For a squared-error loss the Hessian is 2/n X^T X and does not depend on
    theta at all. A quadratic has constant curvature, which is exactly what
    makes it the surface every other surface is compared against."""
    return 2.0 / n * (x.T @ x)


def numeric_mixed_partial(fn, theta: np.ndarray, i: int, j: int, h: float) -> float:
    """The four-point stencil for d^2 f / d theta_i d theta_j."""
    def shift(di: float, dj: float) -> float:
        t = theta.copy()
        t[i] += di
        t[j] += dj
        return fn(t)

    return (shift(h, h) - shift(h, -h) - shift(-h, h) + shift(-h, -h)) / (4.0 * h * h)


def classify(eigenvalues: np.ndarray) -> str:
    """The second-derivative test, including the branch people forget.

    The tolerance is the one place this is delicate. An eigenvalue is treated
    as zero only when it is below what the eigenvalue solver itself can
    resolve, which is roughly machine epsilon times the size of the matrix
    times the largest eigenvalue. A looser rule, say a fixed fraction of the
    largest eigenvalue, calls a badly conditioned but genuinely positive
    definite Hessian singular, which is the wrong verdict for the right reason.
    """
    scale = max(float(np.abs(eigenvalues).max()), 1.0)
    tol = np.finfo(float).eps * len(eigenvalues) * scale
    zero = np.abs(eigenvalues) <= tol
    positive = eigenvalues > tol
    negative = eigenvalues < -tol
    if zero.any() and not (positive.any() and negative.any()):
        return "inconclusive - a zero eigenvalue and no sign disagreement"
    if positive.all():
        return "local minimum - every direction curves up"
    if negative.all():
        return "local maximum - every direction curves down"
    return "saddle - at least one direction up and one down"


def main() -> None:
    frame = load()
    x, y = design_matrix(frame)
    n = len(y)
    h = hessian(x, n)
    print(f"loaded sensors.csv: {n} rows, {x.shape[1]} parameters\n")

    print("1. Schwarz: the Hessian is symmetric")
    # Start from the intercept-only model: predict every reading's temperature
    # as the overall average and nothing else. It is the honest zero-knowledge
    # guess, and it is defined whatever the column count happens to be.
    theta = np.zeros(x.shape[1])
    theta[0] = float(y.mean())
    print(f"   analytic asymmetry ||H - H^T||_max : {np.abs(h - h.T).max():.3e}")
    pairs = [(0, 1), (1, 3), (2, 4)]
    for i, j in pairs:
        step = 1e-3 * max(abs(theta[i]), abs(theta[j]), 1e-2)
        ij = numeric_mixed_partial(lambda t: loss(t, x, y), theta, i, j, step)
        ji = numeric_mixed_partial(lambda t: loss(t, x, y), theta, j, i, step)
        print(f"   d2/d{i}d{j} = {ij:14.6f}   d2/d{j}d{i} = {ji:14.6f}   gap {abs(ij - ji):.2e}")

    print("\n2. the directional second derivative is d^T H d")
    values = np.linalg.eigvalsh(h)
    print(f"   eigenvalues: {np.array2string(values, precision=4, suppress_small=False)}")
    print(f"   smallest {values[0]:.6e}   largest {values[-1]:.6e}")
    print(f"   condition number kappa = {values[-1] / values[0]:,.1f}")

    rng = np.random.default_rng(SEED)
    print(f"   {'random unit d':>16} {'d^T H d':>16} {'2nd central diff':>18}")
    for _ in range(3):
        d = rng.normal(size=len(theta))
        d /= np.linalg.norm(d)
        quad = float(d @ h @ d)
        step = 1e-4
        f0 = loss(theta, x, y)
        fp = loss(theta + step * d, x, y)
        fm = loss(theta - step * d, x, y)
        numeric = (fp - 2 * f0 + fm) / step**2
        print(f"   {'':>16} {quad:16.6f} {numeric:18.6f}")
    print(f"   every one lies between {values[0]:.4e} and {values[-1]:.4e}, as it must")

    print("\n3. the second-derivative test on the sensor-regression loss")
    print(f"   {classify(values)}")
    print("   the loss is quadratic, so this verdict holds at every point, "
          "including its one critical point")
    tol = np.finfo(float).eps * len(values) * float(np.abs(values).max())
    print(f"   how close the call is: the smallest eigenvalue is {values[0]:.4e}")
    print(f"   and the numerical-zero threshold is {tol:.4e}, "
          f"a factor of {values[0] / tol:,.0f} apart")
    print("   comfortable here, and it is the ratio to watch when kappa is large")

    print("\n   the test on three surfaces that exercise the other branches")
    cases = {
        "f = x^2 + y^2      ": np.array([[2.0, 0.0], [0.0, 2.0]]),
        "f = -(x^2 + y^2)   ": np.array([[-2.0, 0.0], [0.0, -2.0]]),
        "f = x^2 - y^2      ": np.array([[2.0, 0.0], [0.0, -2.0]]),
        "f = x^2 + y^4      ": np.array([[2.0, 0.0], [0.0, 0.0]]),
    }
    for label, mat in cases.items():
        vals = np.linalg.eigvalsh(mat)
        print(f"   {label} eigenvalues {vals}  ->  {classify(vals)}")
    print("   the last one really is a minimum, and the test cannot see it:")
    print("   a zero eigenvalue means the quadratic model is silent in that direction")


if __name__ == "__main__":
    main()
