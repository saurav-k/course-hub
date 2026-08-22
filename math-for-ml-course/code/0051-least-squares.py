"""Lesson 51 - least squares: the normal equations, and why they are a projection.

Three results, each checked twice.

1. The normal equations give the minimiser of ||Ax - b||. Checked by solving them,
   and again by confirming 50,000 random nearby coefficient vectors are all worse.
2. The fit is a projection: X beta equals P y, X^T r is zero, and Pythagoras holds
   in 12,000 dimensions.
3. The same coefficients arrive by three routes, and the condition numbers say why
   the normal equations are the least safe of the three.

The target is built here from a stated rule plus noise, so the fit has a truth to
recover rather than only a number to report.

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


TRUTH = np.array([12.5, 3.2, -1.8, 0.9, 2.4, -0.6, 1.1, 0.35, 0.07])
NOISE_SD = 2.0


def solve_normal_equations(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.linalg.solve(X.T @ X, X.T @ y)


def solve_qr(X: np.ndarray, y: np.ndarray) -> np.ndarray:
    Q, R = np.linalg.qr(X)
    return np.linalg.solve(R, Q.T @ y)


def main() -> None:
    frame = load()
    X = np.column_stack([np.ones(len(frame))] + [frame[s].to_numpy(float) for s in SENSORS])
    y = X @ TRUTH + np.random.default_rng(20260822).normal(0.0, NOISE_SD, len(frame))
    names = ["intercept"] + SENSORS

    print(f"design matrix X is {X.shape[0]:,} x {X.shape[1]}, target y is {y.shape[0]:,} values")
    print(f"over-determined: {X.shape[0]:,} equations, {X.shape[1]} unknowns")

    beta = solve_normal_equations(X, y)
    print(f"\n{'coefficient':<14}{'fitted':>12}{'truth':>10}{'difference':>13}")
    for name, value, truth in zip(names, beta, TRUTH):
        print(f"{name:<14}{value:>12.4f}{truth:>10.4f}{value - truth:>13.4f}")
    print(f"largest slope error: {np.abs(beta[1:] - TRUTH[1:]).max():.4f}")
    print("the intercept is the loosest coefficient, because no sensor sits near zero")

    residual = y - X @ beta
    print(f"\nroot mean square residual = {np.linalg.norm(residual) / np.sqrt(len(y)):.4f}, "
          f"against a noise standard deviation of {NOISE_SD}")

    print("\n-- the orthogonality principle, in numbers --")
    print(f"  max |X^T r| = {np.abs(X.T @ residual).max():.3e}")
    print(f"  relative to ||X|| ||r||: "
          f"{np.abs(X.T @ residual).max() / (np.linalg.norm(X) * np.linalg.norm(residual)):.3e}")

    print("\n-- is it really the minimum? 50,000 challengers --")
    rng = np.random.default_rng(17)
    best = float(residual @ residual)
    scale = np.abs(beta) * 1e-3 + 1e-6
    beaten = 0
    margin = np.inf
    for _ in range(50_000):
        trial = beta + rng.normal(0.0, 1.0, size=len(beta)) * scale
        value = float(np.sum((y - X @ trial) ** 2))
        beaten += value < best
        margin = min(margin, value - best)
    print(f"  challengers that beat it: {beaten} of 50,000")
    print(f"  smallest gap seen       : {margin:.6e}, never negative")
    assert beaten == 0
    print("checked twice: the normal-equations answer is the minimiser")

    print("\n-- the fit IS a projection --")
    fitted = X @ beta
    print(f"  max |X beta - P y|     = {np.abs(fitted - X @ np.linalg.solve(X.T @ X, X.T @ y)).max():.3e}")
    print(f"  ||y||^2                = {y @ y:.6e}")
    print(f"  ||fitted||^2 + ||r||^2 = {fitted @ fitted + residual @ residual:.6e}")
    assert abs((fitted @ fitted + residual @ residual) - y @ y) / (y @ y) < 1e-12
    print("  Pythagoras, in 12,000 dimensions, because fitted and residual are orthogonal")

    print("\n-- three routes to the same coefficients --")
    beta_qr = solve_qr(X, y)
    beta_np, *_ = np.linalg.lstsq(X, y, rcond=None)
    print(f"  normal equations against QR   : max difference {np.abs(beta - beta_qr).max():.3e}")
    print(f"  normal equations against numpy: max difference {np.abs(beta - beta_np).max():.3e}")
    print(f"  cond(X)     = {np.linalg.cond(X):.3e}")
    print(f"  cond(X^T X) = {np.linalg.cond(X.T @ X):.3e}   <- squared, the price of the shortcut")
    assert np.allclose(beta, beta_qr, rtol=1e-6) and np.allclose(beta, beta_np, rtol=1e-6)
    print("checked twice: all three agree, and the condition numbers say why QR is safer")


if __name__ == "__main__":
    main()
